/**
 * Claude Code Collector
 * Collects prompts and conversations from Claude Code local data
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
  type: 'user' | 'assistant' | 'queue-operation';
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

  async collect(): Promise<CollectorResult> {
    const result = this.createEmptyResult();

    if (!this.isConfigured()) {
      result.warnings.push('Claude collector not configured or Claude data not found');
      return result;
    }

    try {
      // 1. Collect from history.jsonl (user prompts)
      const historyPath = path.join(this.claudeDataPath, 'history.jsonl');
      if (fs.existsSync(historyPath)) {
        const historyEvents = await this.collectHistory(historyPath);
        this.logInfo(`Found ${historyEvents.length} prompts in history`);
        result.events.push(...historyEvents);
      }

      // 2. Collect from project sessions
      const projectsPath = path.join(this.claudeDataPath, 'projects');
      if (fs.existsSync(projectsPath)) {
        const sessionEvents = await this.collectProjectSessions(projectsPath);
        this.logInfo(`Found ${sessionEvents.length} session messages`);
        result.events.push(...sessionEvents);
      }

      // 3. Collect memory.md if exists
      const memoryPath = path.join(this.claudeDataPath, 'memory.md');
      if (fs.existsSync(memoryPath)) {
        const memoryEvent = await this.collectMemory(memoryPath);
        if (memoryEvent) {
          result.events.push(memoryEvent);
        }
      }

      result.recordCount = result.events.length;
      this.logInfo(`Collected ${result.recordCount} events from Claude Code`);
    } catch (error: any) {
      result.errors.push(`Claude collection failed: ${error.message}`);
    }

    return result;
  }

  private async collectHistory(historyPath: string): Promise<ActivityEvent[]> {
    const events: ActivityEvent[] = [];
    const content = fs.readFileSync(historyPath, 'utf-8');
    const lines = content.split('\n').filter((l) => l.trim());

    for (const line of lines) {
      try {
        const entry: ClaudeHistoryEntry = JSON.parse(line);
        const timestamp = new Date(entry.timestamp);

        // Filter by date range
        if (timestamp < this.dateRange.start || timestamp > this.dateRange.end) {
          continue;
        }

        // Skip empty prompts
        if (!entry.display || entry.display.trim().length === 0) {
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

    return events;
  }

  private async collectProjectSessions(projectsPath: string): Promise<ActivityEvent[]> {
    const events: ActivityEvent[] = [];
    const projectDirs = fs.readdirSync(projectsPath);

    for (const projectDir of projectDirs) {
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

        // Only collect user and assistant messages
        if (msg.type !== 'user' && msg.type !== 'assistant') continue;
        if (!msg.message || !msg.timestamp) continue;

        const timestamp = new Date(msg.timestamp);

        // Filter by date range
        if (timestamp < this.dateRange.start || timestamp > this.dateRange.end) {
          continue;
        }

        const messageText = this.extractMessageText(msg.message);
        if (!messageText || messageText.trim().length === 0) continue;

        const projectName = this.extractProjectName(projectDir);
        const isUser = msg.type === 'user';

        const sourcePointers: SourcePointer[] = [{
          pointer_id: generatePointerId('claude_session', msg.uuid || msg.sessionId + msg.timestamp),
          type: isUser ? 'claude_prompt' : 'claude_response',
          display_text: `Claude ${isUser ? 'prompt' : 'response'} in ${projectName}`,
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

        const title = isUser
          ? this.createPromptTitle(messageText, projectName)
          : `[Claude Response] ${messageText.slice(0, 80)}...`;

        events.push({
          event_id: generateEventId('claude', msg.sessionId, msg.uuid || msg.timestamp),
          source_system: 'claude',
          source_record_id: msg.uuid || `${msg.sessionId}-${msg.timestamp}`,
          actor_user_id: isUser ? this.userId : 'claude',
          actor_display_name: isUser ? 'User' : 'Claude',
          event_timestamp_utc: formatUTC(timestamp),
          event_timestamp_local: formatLocalTime(timestamp, this.dateRange.timezone),
          event_type: isUser ? 'prompt' : 'response',
          title: title,
          body_text_excerpt: messageText.slice(0, 500),
          references,
          source_pointers: sourcePointers,
          pii_redaction_applied: false,
          confidence: 'high',
          raw_data: { type: msg.type, cwd: msg.cwd, gitBranch: msg.gitBranch },
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
