/**
 * Local Files Collector
 * Scans local directories for files created or modified within the date range
 */

import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { BaseCollector, CollectorResult } from './base';
import {
  ActivityEvent,
  SourceSystem,
  RawLocalFile,
  SourcePointer,
  Config,
} from '../types';
import { DateRange, formatUTC, formatLocalTime, isWithinDateRange } from '../utils/datetime';
import { generateEventId, generatePointerId, hashFileSync } from '../utils/hash';
import { truncateText } from '../utils/privacy';

export class LocalCollector extends BaseCollector {
  get source(): SourceSystem {
    return 'local';
  }

  isConfigured(): boolean {
    return this.config.collectors.local.enabled;
  }

  async collect(): Promise<CollectorResult> {
    const result = this.createEmptyResult();

    if (!this.isConfigured()) {
      result.errors.push('Local collector is not configured');
      return result;
    }

    const localConfig = this.config.collectors.local;

    for (const scanPath of localConfig.scan_paths) {
      const resolvedPath = this.resolvePath(scanPath);

      if (!fs.existsSync(resolvedPath)) {
        result.warnings.push(`Path does not exist: ${scanPath}`);
        continue;
      }

      try {
        const files = await this.scanDirectory(resolvedPath);
        this.logInfo(`Found ${files.length} files in ${scanPath}`);

        result.rawData.push(...files);

        for (const file of files) {
          const event = this.transformFile(file);
          if (event) {
            result.events.push(event);
          }
        }
      } catch (error: any) {
        result.warnings.push(`Failed to scan ${scanPath}: ${error.message}`);
      }
    }

    result.recordCount = result.events.length;
    this.logInfo(`Collected ${result.recordCount} events from local files`);

    return result;
  }

  private resolvePath(inputPath: string): string {
    // Handle ~ for home directory
    if (inputPath.startsWith('~')) {
      return path.join(os.homedir(), inputPath.slice(1));
    }
    return path.resolve(inputPath);
  }

  private async scanDirectory(dirPath: string): Promise<RawLocalFile[]> {
    const files: RawLocalFile[] = [];
    const localConfig = this.config.collectors.local;
    const maxSize = localConfig.max_file_size_mb * 1024 * 1024;

    const scanRecursive = async (currentPath: string): Promise<void> => {
      let entries: fs.Dirent[];

      try {
        entries = fs.readdirSync(currentPath, { withFileTypes: true });
      } catch {
        return; // Skip directories we can't read
      }

      for (const entry of entries) {
        const fullPath = path.join(currentPath, entry.name);

        // Check denylist patterns
        if (this.matchesDenylist(fullPath, localConfig.denylist_patterns)) {
          continue;
        }

        if (entry.isDirectory()) {
          await scanRecursive(fullPath);
        } else if (entry.isFile()) {
          try {
            const stats = fs.statSync(fullPath);

            // Check size limit
            if (stats.size > maxSize) {
              continue;
            }

            // Check if modified within date range
            const modifiedAt = stats.mtime.toISOString();
            const createdAt = stats.birthtime.toISOString();

            const isInRange =
              isWithinDateRange(modifiedAt, this.dateRange) ||
              isWithinDateRange(createdAt, this.dateRange);

            if (!isInRange) {
              continue;
            }

            // Calculate hash
            let fileHash: string;
            try {
              fileHash = hashFileSync(fullPath);
            } catch {
              fileHash = 'hash_failed';
            }

            const ext = path.extname(entry.name).toLowerCase();

            files.push({
              path: fullPath,
              name: entry.name,
              extension: ext,
              size_bytes: stats.size,
              created_at: createdAt,
              modified_at: modifiedAt,
              file_hash_sha256: fileHash,
            });
          } catch {
            // Skip files we can't stat
          }
        }
      }
    };

    await scanRecursive(dirPath);
    return files;
  }

  private matchesDenylist(filePath: string, patterns: string[]): boolean {
    const normalizedPath = filePath.replace(/\\/g, '/');

    for (const pattern of patterns) {
      // Simple glob matching
      if (pattern.includes('**')) {
        const regex = pattern
          .replace(/\*\*/g, '.*')
          .replace(/\*/g, '[^/]*')
          .replace(/\./g, '\\.');
        if (new RegExp(regex).test(normalizedPath)) {
          return true;
        }
      } else if (pattern.startsWith('*.')) {
        // Extension pattern
        const ext = pattern.slice(1);
        if (normalizedPath.endsWith(ext)) {
          return true;
        }
      } else if (normalizedPath.includes(pattern)) {
        return true;
      }
    }

    return false;
  }

  private transformFile(file: RawLocalFile): ActivityEvent | null {
    // Determine event type based on dates
    const createdAt = new Date(file.created_at);
    const modifiedAt = new Date(file.modified_at);

    const isNewFile = isWithinDateRange(file.created_at, this.dateRange);
    const eventType: ActivityEvent['event_type'] = isNewFile
      ? 'file_created'
      : 'file_modified';

    const timestamp = isNewFile ? file.created_at : file.modified_at;

    return {
      event_id: generateEventId('local', file.file_hash_sha256, timestamp),
      source_system: 'local',
      source_record_id: file.file_hash_sha256,
      actor_user_id: this.userId,
      actor_display_name: this.userId,
      event_timestamp_utc: formatUTC(new Date(timestamp)),
      event_timestamp_local: formatLocalTime(new Date(timestamp), this.dateRange.timezone),
      event_type: eventType,
      title: file.name,
      body_text_excerpt: `${file.extension || 'no extension'} - ${this.formatFileSize(file.size_bytes)}`,
      references: [
        { type: 'file_id', value: file.file_hash_sha256, display_text: file.name },
      ],
      source_pointers: [
        {
          pointer_id: generatePointerId('local_file_path', file.path),
          type: 'local_file_path',
          path: file.path,
          file_hash_sha256: file.file_hash_sha256,
          display_text: `Local: ${file.name}`,
        },
      ],
      pii_redaction_applied: false,
      confidence: 'high',
      raw_data: file as unknown as Record<string, unknown>,
    };
  }

  private formatFileSize(bytes: number): string {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`;
  }
}
