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
  const pointerMap = new Map(worklog.source_index.map((p) => [p.pointer_id, p]));

  // Compact format for Linear
  lines.push('## Summary');
  lines.push('');
  for (const bullet of worklog.executive_summary.slice(0, 7)) {
    lines.push(`- ${bullet.text}`);
  }
  lines.push('');

  // Workstreams (compact)
  lines.push('## Workstreams');
  lines.push('');
  for (const ws of worklog.workstreams.slice(0, 5)) {
    lines.push(`### ${ws.name} (${ws.status_now})`);
    for (const item of ws.what_happened.slice(0, 3)) {
      lines.push(`- ${item.text}`);
    }
    lines.push('');
  }

  // Key sources
  lines.push('## Key Sources');
  lines.push('');
  const keyPointers = worklog.source_index.filter((p) => p.url).slice(0, 10);
  for (const p of keyPointers) {
    lines.push(`- [${p.display_text}](${p.url})`);
  }
  lines.push('');

  // Gaps
  if (worklog.gaps_and_data_quality.length > 0) {
    lines.push('## Gaps');
    for (const gap of worklog.gaps_and_data_quality.slice(0, 5)) {
      lines.push(`- ${gap}`);
    }
  }

  return lines.join('\n');
}
