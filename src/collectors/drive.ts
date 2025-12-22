/**
 * Google Drive Collector
 * Collects files created or modified within the date range
 */

import { google, drive_v3 } from 'googleapis';
import { BaseCollector, CollectorResult } from './base';
import {
  ActivityEvent,
  SourceSystem,
  RawDriveFile,
  SourcePointer,
  Config,
} from '../types';
import { DateRange, formatUTC, formatLocalTime, isWithinDateRange } from '../utils/datetime';
import { generateEventId, generatePointerId } from '../utils/hash';
import { getGoogleCredentials } from '../utils/config';
import { truncateText } from '../utils/privacy';

export class DriveCollector extends BaseCollector {
  private drive: drive_v3.Drive | null = null;

  get source(): SourceSystem {
    return 'drive';
  }

  isConfigured(): boolean {
    if (!this.config.collectors.drive.enabled) {
      return false;
    }
    const creds = getGoogleCredentials();
    return !!(creds.clientId && creds.clientSecret && creds.refreshToken);
  }

  async collect(): Promise<CollectorResult> {
    const result = this.createEmptyResult();

    if (!this.isConfigured()) {
      result.errors.push('Google Drive collector is not configured');
      return result;
    }

    try {
      await this.initializeClient();

      // Get files modified within date range
      const files = await this.getModifiedFiles();
      this.logInfo(`Found ${files.length} files modified in date range`);

      result.rawData = files;

      // Transform to events
      for (const file of files) {
        const event = this.transformFile(file);
        if (event) {
          result.events.push(event);
        }
      }

      result.recordCount = result.events.length;
      this.logInfo(`Collected ${result.recordCount} events from Google Drive`);
    } catch (error: any) {
      result.errors.push(`Google Drive collection failed: ${error.message}`);
    }

    return result;
  }

  private async initializeClient(): Promise<void> {
    const creds = getGoogleCredentials();

    const oauth2Client = new google.auth.OAuth2(
      creds.clientId,
      creds.clientSecret
    );

    oauth2Client.setCredentials({
      refresh_token: creds.refreshToken,
    });

    this.drive = google.drive({ version: 'v3', auth: oauth2Client });
  }

  private async getModifiedFiles(): Promise<RawDriveFile[]> {
    const files: RawDriveFile[] = [];
    const driveConfig = this.config.collectors.drive;

    // Build query
    const startDate = this.dateRange.start.toISOString();
    const endDate = this.dateRange.end.toISOString();

    let query = `modifiedTime >= '${startDate}' and modifiedTime <= '${endDate}'`;
    query += ` and trashed = false`;

    // Add denylist folders
    for (const folder of driveConfig.denylist_folders) {
      query += ` and not '${folder}' in parents`;
    }

    // Add denylist extensions
    for (const ext of driveConfig.denylist_extensions) {
      query += ` and not name contains '${ext}'`;
    }

    let pageToken: string | undefined;

    do {
      try {
        const response = await this.drive!.files.list({
          q: query,
          fields: 'nextPageToken, files(id, name, mimeType, createdTime, modifiedTime, webViewLink, owners, parents, size)',
          pageSize: 100,
          pageToken,
        });

        if (response.data.files) {
          for (const file of response.data.files) {
            const rawFile: RawDriveFile = {
              id: file.id!,
              name: file.name!,
              mimeType: file.mimeType!,
              createdTime: file.createdTime!,
              modifiedTime: file.modifiedTime!,
              webViewLink: file.webViewLink!,
              owners: file.owners?.map((o) => ({
                displayName: o.displayName!,
                emailAddress: o.emailAddress!,
              })),
              parents: file.parents,
              size: file.size,
            };

            // Check allowlist if specified
            if (driveConfig.allowlist_folders.length > 0) {
              const isInAllowlist = file.parents?.some((p) =>
                driveConfig.allowlist_folders.includes(p)
              );
              if (!isInAllowlist) {
                continue;
              }
            }

            files.push(rawFile);
          }
        }

        pageToken = response.data.nextPageToken || undefined;
      } catch (error: any) {
        this.logWarn(`Failed to list files: ${error.message}`);
        break;
      }
    } while (pageToken);

    return files;
  }

  async getFileById(fileId: string): Promise<RawDriveFile | null> {
    if (!this.drive) {
      await this.initializeClient();
    }

    try {
      const response = await this.drive!.files.get({
        fileId,
        fields: 'id, name, mimeType, createdTime, modifiedTime, webViewLink, owners, parents, size',
      });

      const file = response.data;
      return {
        id: file.id!,
        name: file.name!,
        mimeType: file.mimeType!,
        createdTime: file.createdTime!,
        modifiedTime: file.modifiedTime!,
        webViewLink: file.webViewLink!,
        owners: file.owners?.map((o) => ({
          displayName: o.displayName!,
          emailAddress: o.emailAddress!,
        })),
        parents: file.parents,
        size: file.size,
      };
    } catch (error: any) {
      this.logWarn(`Failed to get file ${fileId}: ${error.message}`);
      return null;
    }
  }

  private transformFile(file: RawDriveFile): ActivityEvent | null {
    const creds = getGoogleCredentials();

    // Determine event type based on dates
    const createdTime = new Date(file.createdTime);
    const modifiedTime = new Date(file.modifiedTime);

    const isNewFile = isWithinDateRange(file.createdTime, this.dateRange);
    const eventType: ActivityEvent['event_type'] = isNewFile
      ? 'file_created'
      : 'file_modified';

    const timestamp = isNewFile ? file.createdTime : file.modifiedTime;

    // Get owner info
    const owner = file.owners?.[0];
    const isOwner = owner?.emailAddress === creds.userEmail;

    return {
      event_id: generateEventId('drive', file.id, timestamp),
      source_system: 'drive',
      source_record_id: file.id,
      actor_user_id: owner?.emailAddress || 'unknown',
      actor_display_name: owner?.displayName || 'Unknown',
      event_timestamp_utc: formatUTC(new Date(timestamp)),
      event_timestamp_local: formatLocalTime(new Date(timestamp), this.dateRange.timezone),
      event_type: eventType,
      title: file.name,
      body_text_excerpt: `${file.mimeType} - ${this.formatFileSize(file.size)}`,
      references: [
        { type: 'file_id', value: file.id, display_text: file.name },
        { type: 'url', value: file.webViewLink, display_text: file.name },
      ],
      source_pointers: [
        {
          pointer_id: generatePointerId('drive_file_url', file.webViewLink),
          type: 'drive_file_url',
          url: file.webViewLink,
          display_text: `Drive: ${file.name}`,
        },
      ],
      pii_redaction_applied: false,
      confidence: isOwner ? 'high' : 'medium',
      raw_data: file,
    };
  }

  private formatFileSize(size?: string): string {
    if (!size) return 'Unknown size';

    const bytes = parseInt(size, 10);
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`;
  }
}
