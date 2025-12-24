/**
 * Claude Code Collector
 * Collects ONLY user prompts from Claude Code local data
 *
 * FILTROS APLICADOS:
 * - Apenas prompts do usuário (type: user)
 * - Apenas projetos relevantes (não system32, não home genérico)
 * - Respeita range de datas
 * - Ignora: assistant responses, tool_use, snapshots
 */

import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { BaseCollector, CollectorResult } from './base';
import {
  ActivityEvent,
  SourceSystem,
  SourcePointer,
  EventReference,
} from '../types';
import { formatUTC, formatLocalTime } from '../utils/datetime';
import { generateEventId, generatePointerId } from '../utils/hash';

// Claude Code data structures
interface ClaudeHistoryEntry {
  display: string;
  pastedContents?: Record<string, unknown>;
  timestamp: number; // ms since epoch
  project: string;
  sessionId: string;
}

interface ClaudeSessionMessage {
  type: 'user' | 'assistant' | 'queue-operation' | 'file-history-snapshot';
  message?: {
    role: string;
    content: string | Array<{ type: string; text?: string }>;
  };
  timestamp: string;
  sessionId: string;
  cwd?: string;
  gitBranch?: string;
  uuid?: string;
}

// Projetos genéricos que devem ser ignorados
const IGNORED_PROJECT_PATTERNS = [
  'system32',
  'C--windows',
  'windows-system32',
];

// Prompts curtos demais para serem relevantes
const MIN_PROMPT_LENGTH = 5;

export class ClaudeCollector extends BaseCollector {
  private claudeDataPath: string;

  constructor(config: any, dateRange: any, userId: string) {
    super(config, dateRange, userId);
    // Claude Code stores data in ~/.claude on all platforms
    this.claudeDataPath = path.join(os.homedir(), '.claude');
  }

  get source(): SourceSystem {
    return 'claude';
  }

  isConfigured(): boolean {
    if (!this.config.collectors.claude?.enabled) {
      return false;
    }
    // Check if Claude data directory exists
    return fs.existsSync(this.claudeDataPath);
  }

  /**
   * Verifica se um projeto deve ser coletado
   */
  private isRelevantProject(projectPath: string): boolean {
    if (!projectPath) return false;

    const lowerPath = projectPath.toLowerCase();

    // Ignorar projetos genéricos
    for (const pattern of IGNORED_PROJECT_PATTERNS) {
      if (lowerPath.includes(pattern.toLowerCase())) {
        return false;
      }
    }

    return true;
  }

  /**
   * Verifica se um prompt é relevante (não é ruído)
   */
  private isRelevantPrompt(text: string): boolean {
    if (!text || text.trim().length < MIN_PROMPT_LENGTH) {
      return false;
    }

    const trimmed = text.trim().toLowerCase();

    // Ignorar comandos muito curtos/genéricos
    const ignoredCommands = ['c', 'y', 'n', 'yes', 'no', 'ok', 'b', 's'];
    if (ignoredCommands.includes(trimmed)) {
      return false;
    }

    return true;
  }

  async collect(): Promise<CollectorResult> {
    const result = this.createEmptyResult();

    if (!this.isConfigured()) {
      result.warnings.push('Claude collector not configured or Claude data not found');
      return result;
    }

    try {
      // ============================================
      // FONTE PRINCIPAL: history.jsonl (prompts do usuário)
      // ============================================
      const historyPath = path.join(this.claudeDataPath, 'history.jsonl');
      if (fs.existsSync(historyPath)) {
        const historyEvents = await this.collectHistory(historyPath);
        this.logInfo(`Found ${historyEvents.length} user prompts in history`);
        result.events.push(...historyEvents);

        // Salvar raw data para debug
        result.rawData = historyEvents.map(e => e.raw_data);
      }

      // ============================================
      // OPCIONAL: Sessões de projetos relevantes
      // Apenas se configurado para incluir contexto de sessão
      // ============================================
      const claudeConfig = this.config.collectors.claude as any;
      const includeSessionContext = claudeConfig?.include_session_context === true;

      if (includeSessionContext) {
        const projectsPath = path.join(this.claudeDataPath, 'projects');
        if (fs.existsSync(projectsPath)) {
          const sessionEvents = await this.collectProjectSessions(projectsPath);
          this.logInfo(`Found ${sessionEvents.length} session prompts (context)`);
          result.events.push(...sessionEvents);
        }
      }

      // ============================================
      // OPCIONAL: memory.md (se modificado no período)
      // ============================================
      const includeMemory = claudeConfig?.include_memory !== false;
      if (includeMemory) {
        const memoryPath = path.join(this.claudeDataPath, 'memory.md');
        if (fs.existsSync(memoryPath)) {
          const memoryEvent = await this.collectMemory(memoryPath);
          if (memoryEvent) {
            result.events.push(memoryEvent);
          }
        }
      }

      // Estatísticas
      const byProject = new Map<string, number>();
      for (const event of result.events) {
        const proj = (event.raw_data as any)?.project || 'unknown';
        const projName = this.extractProjectName(proj);
        byProject.set(projName, (byProject.get(projName) || 0) + 1);
      }

      result.recordCount = result.events.length;
      this.logInfo(`Collected ${result.recordCount} events from Claude Code`);
      this.logInfo(`  By project: ${Array.from(byProject.entries()).map(([k, v]) => `${k}(${v})`).join(', ')}`);
    } catch (error: any) {
      result.errors.push(`Claude collection failed: ${error.message}`);
    }

    return result;
  }

  private async collectHistory(historyPath: string): Promise<ActivityEvent[]> {
    const events: ActivityEvent[] = [];
    const content = fs.readFileSync(historyPath, 'utf-8');
    const lines = content.split('\n').filter((l) => l.trim());

    let skippedByDate = 0;
    let skippedByProject = 0;
    let skippedByContent = 0;

    for (const line of lines) {
      try {
        const entry: ClaudeHistoryEntry = JSON.parse(line);
        const timestamp = new Date(entry.timestamp);

        // Filter by date range
        if (timestamp < this.dateRange.start || timestamp > this.dateRange.end) {
          skippedByDate++;
          continue;
        }

        // Filter by project relevance (skip system32, etc)
        if (!this.isRelevantProject(entry.project)) {
          skippedByProject++;
          continue;
        }

        // Filter by prompt content (skip empty, single chars, etc)
        if (!this.isRelevantPrompt(entry.display)) {
          skippedByContent++;
          continue;
        }

        const projectName = this.extractProjectName(entry.project);
        const sourcePointers: SourcePointer[] = [{
          pointer_id: generatePointerId('claude_prompt', entry.sessionId + entry.timestamp),
          type: 'claude_prompt',
          display_text: `Claude prompt in ${projectName}`,
        }];

        const references: EventReference[] = [{
          type: 'session_id',
          value: entry.sessionId,
          display_text: `Session ${entry.sessionId.slice(0, 8)}`,
        }];

        if (entry.project) {
          references.push({
            type: 'project',
            value: entry.project,
            display_text: projectName,
          });
        }

        const title = this.createPromptTitle(entry.display, projectName);

        events.push({
          event_id: generateEventId('claude', entry.sessionId, String(entry.timestamp)),
          source_system: 'claude',
          source_record_id: `${entry.sessionId}-${entry.timestamp}`,
          actor_user_id: this.userId,
          actor_display_name: 'User',
          event_timestamp_utc: formatUTC(timestamp),
          event_timestamp_local: formatLocalTime(timestamp, this.dateRange.timezone),
          event_type: 'prompt',
          title: title,
          body_text_excerpt: entry.display,
          references,
          source_pointers: sourcePointers,
          pii_redaction_applied: false,
          confidence: 'high',
          raw_data: entry as unknown as Record<string, unknown>,
        });
      } catch (e) {
        // Skip malformed lines
      }
    }

    this.logInfo(`  Filtered: ${skippedByDate} by date, ${skippedByProject} by project, ${skippedByContent} by content`);
    return events;
  }

  private async collectProjectSessions(projectsPath: string): Promise<ActivityEvent[]> {
    const events: ActivityEvent[] = [];
    const projectDirs = fs.readdirSync(projectsPath);

    for (const projectDir of projectDirs) {
      // Skip generic/system projects
      if (!this.isRelevantProject(projectDir)) {
        continue;
      }

      const projectPath = path.join(projectsPath, projectDir);
      if (!fs.statSync(projectPath).isDirectory()) continue;

      const sessionFiles = fs.readdirSync(projectPath).filter((f) => f.endsWith('.jsonl'));

      for (const sessionFile of sessionFiles) {
        const sessionPath = path.join(projectPath, sessionFile);
        const sessionEvents = await this.collectSessionFile(sessionPath, projectDir);
        events.push(...sessionEvents);
      }
    }

    return events;
  }

  private async collectSessionFile(sessionPath: string, projectDir: string): Promise<ActivityEvent[]> {
    const events: ActivityEvent[] = [];
    const content = fs.readFileSync(sessionPath, 'utf-8');
    const lines = content.split('\n').filter((l) => l.trim());

    for (const line of lines) {
      try {
        const msg: ClaudeSessionMessage = JSON.parse(line);

        // ============================================
        // APENAS mensagens do USUÁRIO (não assistant, não tool_use, não snapshot)
        // ============================================
        if (msg.type !== 'user') continue;
        if (!msg.message || !msg.timestamp) continue;

        const timestamp = new Date(msg.timestamp);

        // Filter by date range
        if (timestamp < this.dateRange.start || timestamp > this.dateRange.end) {
          continue;
        }

        const messageText = this.extractMessageText(msg.message);

        // Filter by content relevance
        if (!this.isRelevantPrompt(messageText)) {
          continue;
        }

        const projectName = this.extractProjectName(projectDir);

        const sourcePointers: SourcePointer[] = [{
          pointer_id: generatePointerId('claude_session', msg.uuid || msg.sessionId + msg.timestamp),
          type: 'claude_prompt',
          display_text: `Claude prompt in ${projectName}`,
        }];

        const references: EventReference[] = [{
          type: 'session_id',
          value: msg.sessionId,
          display_text: `Session ${msg.sessionId.slice(0, 8)}`,
        }];

        if (msg.cwd) {
          references.push({
            type: 'project',
            value: msg.cwd,
            display_text: path.basename(msg.cwd),
          });
        }

        if (msg.gitBranch) {
          references.push({
            type: 'git_branch',
            value: msg.gitBranch,
            display_text: `Branch: ${msg.gitBranch}`,
          });
        }

        const title = this.createPromptTitle(messageText, projectName);

        events.push({
          event_id: generateEventId('claude', msg.sessionId, msg.uuid || msg.timestamp),
          source_system: 'claude',
          source_record_id: msg.uuid || `${msg.sessionId}-${msg.timestamp}`,
          actor_user_id: this.userId,
          actor_display_name: 'User',
          event_timestamp_utc: formatUTC(timestamp),
          event_timestamp_local: formatLocalTime(timestamp, this.dateRange.timezone),
          event_type: 'prompt',
          title: title,
          body_text_excerpt: messageText.slice(0, 500),
          references,
          source_pointers: sourcePointers,
          pii_redaction_applied: false,
          confidence: 'high',
          raw_data: { type: msg.type, cwd: msg.cwd, gitBranch: msg.gitBranch, project: projectDir },
        });
      } catch (e) {
        // Skip malformed lines
      }
    }

    return events;
  }

  private async collectMemory(memoryPath: string): Promise<ActivityEvent | null> {
    try {
      const stats = fs.statSync(memoryPath);
      const timestamp = new Date(stats.mtime);

      // Check if memory was modified in date range
      if (timestamp < this.dateRange.start || timestamp > this.dateRange.end) {
        return null;
      }

      const content = fs.readFileSync(memoryPath, 'utf-8');

      return {
        event_id: generateEventId('claude', 'memory', stats.mtime.toISOString()),
        source_system: 'claude',
        source_record_id: 'memory.md',
        actor_user_id: this.userId,
        actor_display_name: 'User',
        event_timestamp_utc: formatUTC(timestamp),
        event_timestamp_local: formatLocalTime(timestamp, this.dateRange.timezone),
        event_type: 'file_modified',
        title: 'Claude Memory Updated',
        body_text_excerpt: content.slice(0, 500),
        references: [{
          type: 'file',
          value: memoryPath,
          display_text: 'memory.md',
        }],
        source_pointers: [{
          pointer_id: generatePointerId('claude_memory', memoryPath),
          type: 'claude_memory',
          path: memoryPath,
          display_text: 'Claude persistent memory',
        }],
        pii_redaction_applied: false,
        confidence: 'high',
        raw_data: { content: content.slice(0, 1000) },
      };
    } catch (e) {
      return null;
    }
  }

  private extractProjectName(projectPath: string): string {
    if (!projectPath) return 'Unknown';
    // Handle encoded project names like C--Users-adm-r-intuit-boom
    const decoded = projectPath.replace(/--/g, '/').replace(/-/g, ' ');
    const parts = decoded.split('/').filter(Boolean);
    return parts[parts.length - 1] || 'Unknown';
  }

  private extractMessageText(message: { role: string; content: string | Array<{ type: string; text?: string }> }): string {
    if (typeof message.content === 'string') {
      return message.content;
    }
    if (Array.isArray(message.content)) {
      return message.content
        .filter((c) => c.type === 'text' && c.text)
        .map((c) => c.text)
        .join('\n');
    }
    return '';
  }

  private createPromptTitle(text: string, projectName: string): string {
    const cleaned = text
      .replace(/\n+/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();

    if (!cleaned) {
      return `[${projectName}] (empty prompt)`;
    }

    const maxLen = 100;
    if (cleaned.length <= maxLen) {
      return `[${projectName}] ${cleaned}`;
    }

    const truncated = cleaned.substring(0, maxLen);
    const lastSpace = truncated.lastIndexOf(' ');
    if (lastSpace > maxLen * 0.7) {
      return `[${projectName}] ${truncated.substring(0, lastSpace)}...`;
    }

    return `[${projectName}] ${truncated}...`;
  }
}
