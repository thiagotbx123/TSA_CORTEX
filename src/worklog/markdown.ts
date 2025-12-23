/**
 * Markdown Renderer
 * Converts WorklogOutput to formatted Markdown
 */

import { WorklogOutput, SourcePointer } from '../types';
import { formatDisplay } from '../utils/datetime';

export function renderWorklogMarkdown(worklog: WorklogOutput): string {
  const lines: string[] = [];
  const pointerMap = new Map(worklog.source_index.map((p) => [p.pointer_id, p]));

  // Helper to format source references
  const formatRefs = (ids: string[]): string => {
    if (ids.length === 0) return '';
    const refs = ids
      .map((id) => {
        const p = pointerMap.get(id);
        return p ? `[${p.pointer_id.slice(0, 8)}]` : '';
      })
      .filter(Boolean)
      .join(' ');
    return refs ? ` ${refs}` : '';
  };

  // Header
  lines.push('# Weekly Worklog');
  lines.push('');

  // Run Metadata
  lines.push('## Run Metadata');
  lines.push('');
  lines.push(`- **Person**: ${worklog.run_metadata.person_display_name}`);
  lines.push(`- **Timezone**: ${worklog.run_metadata.timezone}`);
  lines.push(`- **Period**: ${formatDisplay(worklog.run_metadata.start_datetime, worklog.run_metadata.timezone)} to ${formatDisplay(worklog.run_metadata.end_datetime, worklog.run_metadata.timezone)}`);
  lines.push(`- **Sources Included**: ${worklog.run_metadata.sources_included.join(', ') || 'None'}`);
  lines.push(`- **Sources Missing**: ${worklog.run_metadata.sources_missing.join(', ') || 'None'}`);
  lines.push('');

  // Executive Summary
  lines.push('## Executive Summary');
  lines.push('');
  for (const bullet of worklog.executive_summary) {
    lines.push(`- ${bullet.text}${formatRefs(bullet.source_pointer_ids)}`);
  }
  lines.push('');

  // Workstreams
  lines.push('## Workstreams');
  lines.push('');

  for (const ws of worklog.workstreams) {
    lines.push(`### ${ws.name}`);
    lines.push('');
    lines.push(`**Type**: ${ws.cluster_type} | **Status**: ${ws.status_now}`);
    lines.push('');

    lines.push('**What happened:**');
    for (const item of ws.what_happened) {
      lines.push(`- ${item.text}${formatRefs(item.source_pointer_ids)}`);
    }
    lines.push('');

    lines.push(`**Why it matters:** ${ws.why_it_matters}`);
    lines.push('');

    if (ws.next_actions.length > 0) {
      lines.push('**Next actions:**');
      for (const action of ws.next_actions) {
        lines.push(`- ${action.text}${formatRefs(action.source_pointer_ids)}`);
      }
      lines.push('');
    }
  }

  // Timeline
  lines.push('## Timeline');
  lines.push('');
  lines.push('| Time | Activity | Sources |');
  lines.push('|------|----------|---------|');

  for (const entry of worklog.timeline.slice(0, 50)) {
    const time = entry.timestamp_local.split('T')[1]?.slice(0, 5) || entry.timestamp_local;
    const date = entry.timestamp_local.split('T')[0];
    const refs = entry.source_pointer_ids
      .slice(0, 2)
      .map((id) => {
        const p = pointerMap.get(id);
        return p?.url ? `[link](${p.url})` : id.slice(0, 8);
      })
      .join(', ');
    lines.push(`| ${date} ${time} | ${entry.description.slice(0, 60)} | ${refs} |`);
  }

  if (worklog.timeline.length > 50) {
    lines.push(`| ... | _${worklog.timeline.length - 50} more entries_ | |`);
  }
  lines.push('');

  // Decisions and Blockers
  if (worklog.decisions_and_blockers.length > 0) {
    lines.push('## Decisions and Blockers');
    lines.push('');
    for (const item of worklog.decisions_and_blockers) {
      lines.push(`- ${item.text}${formatRefs(item.source_pointer_ids)}`);
    }
    lines.push('');
  }

  // Gaps and Data Quality
  if (worklog.gaps_and_data_quality.length > 0) {
    lines.push('## Gaps and Data Quality Issues');
    lines.push('');
    for (const gap of worklog.gaps_and_data_quality) {
      lines.push(`- ${gap}`);
    }
    lines.push('');
  }

  // Source Index
  lines.push('## Source Index');
  lines.push('');
  lines.push('| ID | Type | Link |');
  lines.push('|----|------|------|');

  for (const pointer of worklog.source_index.slice(0, 100)) {
    const link = pointer.url
      ? `[${pointer.display_text}](${pointer.url})`
      : pointer.path || pointer.display_text;
    lines.push(`| ${pointer.pointer_id.slice(0, 12)} | ${pointer.type} | ${link} |`);
  }

  if (worklog.source_index.length > 100) {
    lines.push(`| ... | _${worklog.source_index.length - 100} more sources_ | |`);
  }
  lines.push('');

  // Footer
  lines.push('---');
  lines.push(`_Generated at ${new Date().toISOString()} by TSA_CORTEX v1.0.0_`);

  return lines.join('\n');
}

export function renderLinearBody(worklog: WorklogOutput): string {
  const lines: string[] = [];
  const startDate = worklog.run_metadata.start_datetime.split('T')[0];
  const endDate = worklog.run_metadata.end_datetime.split('T')[0];

  const driveFiles = worklog.source_index.filter((p) => p.type.includes('drive'));
  const localFiles = worklog.source_index.filter((p) => p.type.includes('local'));
  const linearItems = worklog.source_index.filter((p) => p.type.includes('linear'));
  const slackItems = worklog.source_index.filter((p) => p.type.includes('slack'));
  const claudeItems = worklog.source_index.filter((p) => p.type.includes('claude'));

  lines.push('# Worklog - Weekly Update');
  lines.push('');
  lines.push('**Owner:** ' + worklog.run_metadata.person_display_name);
  lines.push('**Period:** ' + startDate + ' to ' + endDate);
  lines.push('');
  lines.push('---');
  lines.push('');

  lines.push('## Objective');
  lines.push('');
  lines.push('Document activities and deliverables from ' + startDate + ' to ' + endDate + ', consolidating work across customer projects, internal coordination, and technical development.');
  lines.push('');

  lines.push('## Scope and Deliverables');
  lines.push('');

  const spreadsheets = driveFiles.filter((f) => /\.(xlsx|xls|csv)/i.test(f.display_text));
  if (spreadsheets.length > 0) {
    lines.push('### Spreadsheets and Data Files');
    lines.push('');
    for (const f of spreadsheets.slice(0, 15)) {
      const name = f.display_text.replace(/^Drive:\s*/, '');
      lines.push('- ' + (f.url ? '[' + name + '](' + f.url + ')' : name));
    }
    if (spreadsheets.length > 15) {
      lines.push('- _... and ' + (spreadsheets.length - 15) + ' more spreadsheets_');
    }
    lines.push('');
  }

  const documents = driveFiles.filter((f) => /\.(docx|doc|pptx|ppt|pdf|txt|md)/i.test(f.display_text));
  if (documents.length > 0) {
    lines.push('### Documents and Presentations');
    lines.push('');
    for (const f of documents.slice(0, 15)) {
      const name = f.display_text.replace(/^Drive:\s*/, '');
      lines.push('- ' + (f.url ? '[' + name + '](' + f.url + ')' : name));
    }
    if (documents.length > 15) {
      lines.push('- _... and ' + (documents.length - 15) + ' more documents_');
    }
    lines.push('');
  }

  const recordings = driveFiles.filter((f) =>
    f.display_text.includes('Recording') ||
    f.display_text.includes('Notes by Gemini') ||
    f.display_text.includes('Transcript')
  );
  if (recordings.length > 0) {
    lines.push('### Meetings and Recordings');
    lines.push('');
    for (const f of recordings.slice(0, 10)) {
      const name = f.display_text.replace(/^Drive:\s*/, '');
      lines.push('- ' + (f.url ? '[' + name + '](' + f.url + ')' : name));
    }
    if (recordings.length > 10) {
      lines.push('- _... and ' + (recordings.length - 10) + ' more recordings_');
    }
    lines.push('');
  }

  if (localFiles.length > 0) {
    lines.push('### Local Files Modified');
    lines.push('');
    for (const f of localFiles.slice(0, 15)) {
      const filePath = f.path || f.display_text;
      lines.push('- `' + filePath + '`');
    }
    if (localFiles.length > 15) {
      lines.push('- _... and ' + (localFiles.length - 15) + ' more local files_');
    }
    lines.push('');
  }

  if (linearItems.length > 0) {
    lines.push('### Linear Issues and Activity');
    lines.push('');
    for (const item of linearItems.slice(0, 10)) {
      const name = item.display_text;
      lines.push('- ' + (item.url ? '[' + name + '](' + item.url + ')' : name));
    }
    lines.push('');
  }

  if (claudeItems.length > 0) {
    lines.push('### Claude Code Activity');
    lines.push('');
    const prompts = claudeItems.filter((c) => c.type === 'claude_prompt');
    const responses = claudeItems.filter((c) => c.type === 'claude_response');
    lines.push('Worked with Claude Code across ' + prompts.length + ' prompts and ' + responses.length + ' responses.');
    lines.push('');

    // Show sample prompts grouped by project
    const projectPrompts = new Map();
    for (const p of prompts) {
      const match = p.display_text.match(/in (.+)$/);
      const project = match ? match[1] : 'Unknown';
      if (!projectPrompts.has(project)) projectPrompts.set(project, []);
      projectPrompts.get(project).push(p);
    }

    for (const [project, pList] of Array.from(projectPrompts.entries()).slice(0, 5)) {
      lines.push('**' + project + '** (' + pList.length + ' prompts)');
      lines.push('');
    }
  }

  lines.push('## Collaboration and Process');
  lines.push('');

  const channelMentions = new Set<string>();
  for (const item of slackItems) {
    const match = item.display_text.match(/#([\w-]+)/);
    if (match) channelMentions.add(match[1]);
  }

  if (channelMentions.size > 0) {
    lines.push('Engaged across ' + slackItems.length + ' Slack interactions in channels:');
    lines.push('');
    for (const ch of Array.from(channelMentions).slice(0, 12)) {
      lines.push('- #' + ch);
    }
    lines.push('');
  } else {
    lines.push('Engaged in ' + slackItems.length + ' Slack interactions including DMs and channel discussions.');
    lines.push('');
  }

  if (worklog.workstreams.length > 0) {
    lines.push('## Key Work Areas');
    lines.push('');
    for (const ws of worklog.workstreams.slice(0, 8)) {
      const statusLabel = getStatusLabel(ws.status_now);
      lines.push('### ' + ws.name + ' (' + statusLabel + ')');
      lines.push('');
      if (ws.what_happened.length > 0) {
        for (const item of ws.what_happened.slice(0, 5)) {
          lines.push('- ' + item.text);
        }
        lines.push('');
      }
      if (ws.next_actions.length > 0) {
        lines.push('**Next:** ' + ws.next_actions[0].text);
        lines.push('');
      }
    }
  }

  lines.push('## Validation Summary');
  lines.push('');
  lines.push('| Source | Items Collected | Status |');
  lines.push('|--------|----------------|--------|');
  lines.push('| Slack | ' + slackItems.length + ' | Collected |');
  lines.push('| Google Drive | ' + driveFiles.length + ' | Collected |');
  lines.push('| Local Files | ' + localFiles.length + ' | Collected |');
  lines.push('| Linear | ' + linearItems.length + ' | Collected |');
  lines.push('| Claude Code | ' + claudeItems.length + ' | Collected |');
  lines.push('| **Total** | **' + worklog.source_index.length + '** | |');
  lines.push('');

  if (worklog.decisions_and_blockers.length > 0) {
    lines.push('## Blockers and Decisions');
    lines.push('');
    for (const item of worklog.decisions_and_blockers.slice(0, 8)) {
      lines.push('- ' + item.text);
    }
    lines.push('');
  }

  const relevantGaps = worklog.gaps_and_data_quality.filter(
    (g) => !g.includes('low confidence')
  );
  if (relevantGaps.length > 0) {
    lines.push('## Notes');
    lines.push('');
    for (const gap of relevantGaps.slice(0, 5)) {
      lines.push('- ' + gap);
    }
    lines.push('');
  }

  lines.push('---');
  lines.push('_Generated by TSA_CORTEX_');

  return lines.join('\n');
}

function getStatusLabel(status: string): string {
  switch (status) {
    case 'completed':
      return 'Done';
    case 'active':
      return 'In progress';
    case 'blocked':
      return 'Blocked';
    case 'pending':
      return 'Not started';
    default:
      return status;
  }
}
