/**
 * Narrative Renderer - Layer 4
 * Generates worklog in chronological narrative format by theme
 * Output language: ENGLISH (content is translated if needed)
 *
 * KEY PRINCIPLE: Tell the STORY based on CONTENT, not just list files
 */

import { WorklogOutput, SourcePointer } from '../types';
import { SpineHubData, NarrativeBlock } from '../spinehub';

interface NarrativeConfig {
  ownerName: string;
  startDate: Date;
  endDate: Date;
  generatedAt: Date;
  generationTimeMs: number;
  version: string;
  spineHub?: SpineHubData; // Optional - if provided, uses real content
}

export function renderNarrativeWorklog(
  worklog: WorklogOutput,
  config: NarrativeConfig
): string {
  const lines: string[] = [];
  const pointerMap = new Map(worklog.source_index.map((p) => [p.pointer_id, p]));

  // Track references for the table
  const references: Array<{
    ref: number;
    source: string;
    description: string;
    link: string;
  }> = [];
  let refCounter = 1;

  // Helper to add reference and return [ref:N]
  const addRef = (pointerId: string): string => {
    const pointer = pointerMap.get(pointerId);
    if (!pointer) return '';

    const existing = references.find(r => r.description === pointer.display_text);
    if (existing) return `[ref:${existing.ref}]`;

    const ref = refCounter++;
    references.push({
      ref,
      source: pointer.type.includes('slack') ? 'Slack' :
              pointer.type.includes('drive') ? 'Drive' :
              pointer.type.includes('linear') ? 'Linear' :
              pointer.type.includes('claude') ? 'Claude' :
              pointer.type.includes('local') ? 'Local' : 'Other',
      description: pointer.display_text.slice(0, 50),
      link: pointer.url || pointer.path || 'N/A'
    });
    return `[ref:${ref}]`;
  };

  // ============================================
  // SECTION 1: TITLE
  // ============================================
  const titleDate = formatDateForTitle(config.endDate);
  lines.push(`# [Worklog]${titleDate} TSA ${config.ownerName}`);
  lines.push('');

  // ============================================
  // SECTION 2: SUMMARY
  // ============================================
  lines.push('## Summary');
  lines.push('');
  lines.push('| Field | Value |');
  lines.push('|-------|-------|');
  lines.push(`| Period | ${formatDateEN(config.startDate)} to ${formatDateEN(config.endDate)} |`);
  lines.push(`| Owner | ${config.ownerName} |`);
  lines.push(`| Generated | ${formatDateTimeEN(config.generatedAt)} |`);
  lines.push(`| Sources | ${worklog.run_metadata.sources_included.join(', ')} |`);
  lines.push('');

  // ============================================
  // SECTION 3: WEEKLY NARRATIVE (The STORY)
  // ============================================
  lines.push('## Weekly Narrative');
  lines.push('');

  if (config.spineHub && config.spineHub.narrativeBlocks.length > 0) {
    // Use SpineHub narrative blocks - REAL CONTENT
    for (const block of config.spineHub.narrativeBlocks.slice(0, 10)) {
      lines.push(`### ${block.theme}`);
      lines.push('');
      lines.push(`**Context:** ${block.context}`);
      lines.push('');

      if (block.events.length > 0) {
        // Group by date
        const byDate = new Map<string, typeof block.events>();
        for (const event of block.events) {
          if (!byDate.has(event.date)) {
            byDate.set(event.date, []);
          }
          byDate.get(event.date)!.push(event);
        }

        for (const [date, events] of byDate) {
          const dateObj = new Date(date);
          const weekday = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][dateObj.getDay()];
          lines.push(`**${weekday}, ${formatDateEN(dateObj)}**`);
          lines.push('');

          for (const event of events) {
            // Write as narrative, not "Worked on:"
            lines.push(`At ${event.time}, ${event.description}`);
            lines.push('');
          }
        }
      }

      if (block.outcome) {
        lines.push(`**Outcome:** ${block.outcome}`);
        lines.push('');
      }

      lines.push('---');
      lines.push('');
    }
  } else {
    // Fallback: use workstream data (less rich)
    const relevantWorkstreams = worklog.workstreams.filter(ws =>
      ws.what_happened.length > 0 &&
      !ws.name.startsWith('[RAC-') &&
      ws.cluster_type !== 'other'
    );

    for (const ws of relevantWorkstreams.slice(0, 8)) {
      lines.push(`### ${translateThemeName(ws.name)}`);
      lines.push('');
      lines.push(`**Context:** ${generateContext(ws.name, ws.cluster_type)}`);
      lines.push('');

      for (const event of ws.what_happened.slice(0, 5)) {
        const refStr = event.source_pointer_ids.length > 0
          ? ' ' + addRef(event.source_pointer_ids[0])
          : '';
        lines.push(`- ${cleanEventText(event.text)}${refStr}`);
      }
      lines.push('');

      if (ws.why_it_matters) {
        lines.push(`**Outcome:** ${translateToEnglish(ws.why_it_matters)}`);
        lines.push('');
      }

      lines.push('---');
      lines.push('');
    }
  }

  // ============================================
  // SECTION 4: REFERENCES
  // ============================================
  lines.push('## References');
  lines.push('');
  lines.push('| Ref | Source | Description | Link |');
  lines.push('|-----|--------|-------------|------|');

  for (const ref of references.slice(0, 50)) {
    const linkText = ref.link.startsWith('http')
      ? `[open](${ref.link})`
      : ref.link.slice(0, 30);
    lines.push(`| ${ref.ref} | ${ref.source} | ${ref.description} | ${linkText} |`);
  }

  if (references.length > 50) {
    lines.push(`| ... | | *+${references.length - 50} more references* | |`);
  }
  lines.push('');

  // ============================================
  // SECTION 5: DECISIONS AND BLOCKERS
  // ============================================
  if (worklog.decisions_and_blockers.length > 0) {
    lines.push('## Decisions and Blockers');
    lines.push('');

    const decisions = worklog.decisions_and_blockers.filter(d =>
      d.text.toLowerCase().includes('decision') ||
      d.text.toLowerCase().includes('decided') ||
      d.text.toLowerCase().includes('approved')
    );

    const blockers = worklog.decisions_and_blockers.filter(d =>
      d.text.toLowerCase().includes('blocker') ||
      d.text.toLowerCase().includes('waiting') ||
      d.text.toLowerCase().includes('pending')
    );

    if (decisions.length > 0) {
      lines.push('**Decisions Made:**');
      for (const d of decisions.slice(0, 5)) {
        const refStr = d.source_pointer_ids.length > 0
          ? ' ' + addRef(d.source_pointer_ids[0])
          : '';
        lines.push(`- ${translateToEnglish(d.text)}${refStr}`);
      }
      lines.push('');
    }

    if (blockers.length > 0) {
      lines.push('**Blockers Identified:**');
      for (const b of blockers.slice(0, 5)) {
        lines.push(`- ${translateToEnglish(b.text)}`);
      }
      lines.push('');
    }
  }

  // ============================================
  // SECTION 6: EXECUTIVE SUMMARY (Metrics only)
  // ============================================
  lines.push('## Executive Summary');
  lines.push('');

  const counts = worklog.run_metadata.record_counts_by_source;
  const slackCount = counts.slack || 0;
  const driveCount = counts.drive || 0;
  const linearCount = counts.linear || 0;
  const claudeCount = counts.claude || 0;
  const localCount = counts.local || 0;
  const total = slackCount + driveCount + linearCount + claudeCount + localCount;

  // Count meetings
  const meetingCount = worklog.source_index.filter(p =>
    p.display_text.toLowerCase().includes('recording') ||
    p.display_text.toLowerCase().includes('notes by gemini')
  ).length;

  // Extract unique channels
  const channels = new Set<string>();
  worklog.source_index.forEach(p => {
    const match = p.display_text.match(/#([\w-]+)/);
    if (match) channels.add(match[1]);
  });

  lines.push('| Metric | Value |');
  lines.push('|--------|-------|');
  lines.push(`| Owner Messages (Slack) | ${config.spineHub?.slack.ownerMessages.length || slackCount} |`);
  lines.push(`| Meetings Attended | ${Math.floor(meetingCount / 2)} |`);
  lines.push(`| Documents Touched | ${driveCount} |`);
  lines.push(`| Issues Worked | ${linearCount} |`);
  lines.push(`| Active Channels | ${channels.size} |`);
  lines.push(`| Total Evidence Items | ${total} |`);
  lines.push('');

  // ============================================
  // SECTION 7: FOOTER (Detailed Filters)
  // ============================================
  const genTimeStr = formatGenerationTime(config.generationTimeMs);
  lines.push('---');
  lines.push(`*Generated by TSA CORTEX v${config.version} in ${genTimeStr}*`);
  lines.push('');
  lines.push('**Collection Filters Applied:**');
  lines.push(`- Date Range: ${formatDateEN(config.startDate)} to ${formatDateEN(config.endDate)}`);
  lines.push(`- Slack: Messages from ${config.ownerName} (user_id filter)`);

  if (config.spineHub) {
    lines.push(`- Slack Channels: ${config.spineHub.metadata.filters.slackChannels.slice(0, 5).join(', ')}${config.spineHub.metadata.filters.slackChannels.length > 5 ? '...' : ''}`);
  }

  lines.push(`- Drive: Files owned or modified by ${config.ownerName}`);
  lines.push(`- Local: ~/Downloads, ~/Documents (modified in period)`);
  lines.push(`- Excluded: *.env, client_secret*.json, credentials*.json, temp files`);
  lines.push(`- Linear: Issues created, assigned, or commented by owner`);

  if (claudeCount > 0) {
    lines.push(`- Claude: ${claudeCount} prompts/responses from local sessions`);
  }

  lines.push('');
  lines.push('*Only owner actions included. Third-party work excluded.*');

  return lines.join('\n');
}

// Helper functions

function formatDateForTitle(date: Date): string {
  const yy = date.getFullYear().toString().slice(2);
  const mm = (date.getMonth() + 1).toString().padStart(2, '0');
  const dd = date.getDate().toString().padStart(2, '0');
  return `${yy}_${mm}_${dd}`;
}

function formatDateEN(date: Date): string {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const dd = date.getDate();
  const mm = months[date.getMonth()];
  const yyyy = date.getFullYear();
  return `${mm} ${dd}, ${yyyy}`;
}

function formatDateTimeEN(date: Date): string {
  const dateStr = formatDateEN(date);
  const hh = date.getHours().toString().padStart(2, '0');
  const min = date.getMinutes().toString().padStart(2, '0');
  return `${dateStr} at ${hh}:${min}`;
}

function formatGenerationTime(ms: number): string {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;

  if (minutes > 0) {
    return `${minutes}min ${remainingSeconds}s`;
  }
  return `${seconds}s`;
}

function generateContext(name: string, type: string): string {
  const contexts: Record<string, string> = {
    'customer': 'Customer project work including analysis, documentation, and coordination.',
    'feature': 'Development of internal feature or tool.',
    'documentation': 'Creation and update of technical or process documentation.',
    'internal': 'Internal coordination with team and stakeholders.',
    'meeting': 'Participation in alignment and decision-making meetings.',
    'incident': 'Handling of reported incidents or issues.',
    'project': 'Execution of structured project with defined deliverables.',
    'ops': 'Operational and support activities.',
  };

  return contexts[type] || 'Activities related to the identified theme.';
}

function translateThemeName(name: string): string {
  const translations: Record<string, string> = {
    'Documentação': 'Documentation',
    'Cliente': 'Customer',
    'Interno': 'Internal',
    'Reuniões': 'Meetings',
    'Projeto': 'Project',
    'Desenvolvimento': 'Development',
    'Incidentes': 'Incidents',
    'Operações': 'Operations',
  };

  let translated = name;
  for (const [pt, en] of Object.entries(translations)) {
    translated = translated.replace(new RegExp(pt, 'gi'), en);
  }
  return translated;
}

function translateToEnglish(text: string): string {
  const phrases: Record<string, string> = {
    'Inclui discussões': 'Includes discussions',
    'e mudanças de arquivo': 'and file changes',
    'através de': 'across',
    'fontes': 'sources',
    'fonte': 'source',
    'Aguardando': 'Waiting for',
    'Pendente': 'Pending',
    'Bloqueado': 'Blocked',
    'Concluído': 'Completed',
    'Em andamento': 'In progress',
  };

  let translated = text;
  for (const [pt, en] of Object.entries(phrases)) {
    translated = translated.replace(new RegExp(pt, 'gi'), en);
  }
  return translated;
}

function cleanEventText(text: string): string {
  let clean = text
    .replace(/\[#[\w-]+\]\s*/g, '')
    .replace(/\[Claude Response\]\s*/g, '')
    .replace(/\[.*?\]\s*/g, '')
    .replace(/\n+/g, ' ')
    .trim();

  if (clean.length > 200) {
    clean = clean.slice(0, 200) + '...';
  }

  return clean || 'Activity recorded';
}
