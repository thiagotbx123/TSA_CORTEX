/**
 * Slack Collector
 * Collects messages, threads, mentions, and file shares from Slack
 */

import { WebClient } from '@slack/web-api';
import { BaseCollector, CollectorResult } from './base';
import {
  ActivityEvent,
  SourceSystem,
  RawSlackMessage,
  SourcePointer,
  EventReference,
  Config,
} from '../types';
import { DateRange, slackTsToDate, formatUTC, formatLocalTime, dateToSlackTs } from '../utils/datetime';
import { generateEventId, generatePointerId } from '../utils/hash';
import { getSlackCredentials } from '../utils/config';
import { redactPII, truncateText } from '../utils/privacy';

export class SlackCollector extends BaseCollector {
  private client: WebClient | null = null;
  private userToken: string | null = null;

  get source(): SourceSystem {
    return 'slack';
  }

  isConfigured(): boolean {
    if (!this.config.collectors.slack.enabled) {
      return false;
    }
    const creds = getSlackCredentials();
    return !!(creds.botToken || creds.userToken);
  }

  async collect(): Promise<CollectorResult> {
    const result = this.createEmptyResult();

    if (!this.isConfigured()) {
      result.errors.push('Slack collector is not configured');
      return result;
    }

    const creds = getSlackCredentials();
    this.client = new WebClient(creds.botToken || creds.userToken);
    this.userToken = creds.userToken || null;

    try {
      // Get all channels the user has access to
      const channels = await this.getChannels();
      this.logInfo(`Found ${channels.length} channels to scan`);

      // Collect messages from each channel
      for (const channel of channels) {
        try {
          const messages = await this.getChannelMessages(channel.id, channel.name);
          result.rawData.push(...messages);

          for (const msg of messages) {
            const event = this.transformMessage(msg);
            if (event) {
              result.events.push(event);
            }
          }
        } catch (error: any) {
          result.warnings.push(`Failed to collect from channel ${channel.name}: ${error.message}`);
        }
      }

      // Collect direct messages if user token is available
      if (this.userToken) {
        try {
          const dms = await this.getDirectMessages();
          result.rawData.push(...dms);

          for (const dm of dms) {
            const event = this.transformMessage(dm);
            if (event) {
              result.events.push(event);
            }
          }
        } catch (error: any) {
          result.warnings.push(`Failed to collect DMs: ${error.message}`);
        }
      }

      result.recordCount = result.events.length;
      this.logInfo(`Collected ${result.recordCount} events from Slack`);
    } catch (error: any) {
      result.errors.push(`Slack collection failed: ${error.message}`);
    }

    return result;
  }

  private async getChannels(): Promise<Array<{ id: string; name: string }>> {
    const channels: Array<{ id: string; name: string }> = [];

    try {
      // Get public channels
      let cursor: string | undefined;
      do {
        const response = await this.client!.conversations.list({
          types: 'public_channel,private_channel',
          limit: 200,
          cursor,
        });

        if (response.channels) {
          for (const ch of response.channels) {
            if (ch.id && ch.name && ch.is_member) {
              channels.push({ id: ch.id, name: ch.name });
            }
          }
        }

        cursor = response.response_metadata?.next_cursor;
      } while (cursor);
    } catch (error: any) {
      this.logWarn(`Failed to list channels: ${error.message}`);
    }

    return channels;
  }

  private async getChannelMessages(
    channelId: string,
    channelName: string
  ): Promise<RawSlackMessage[]> {
    const messages: RawSlackMessage[] = [];
    const creds = getSlackCredentials();
    const oldest = dateToSlackTs(this.dateRange.start);
    const latest = dateToSlackTs(this.dateRange.end);

    let cursor: string | undefined;

    do {
      const response = await this.client!.conversations.history({
        channel: channelId,
        oldest,
        latest,
        limit: 200,
        cursor,
      });

      if (response.messages) {
        for (const msg of response.messages) {
          // Only include messages from the user or mentioning the user
          const isFromUser = msg.user === creds.userId;
          const mentionsUser = msg.text?.includes(`<@${creds.userId}>`);

          if (isFromUser || mentionsUser) {
            const rawMsg: RawSlackMessage = {
              ts: msg.ts!,
              channel: channelId,
              channel_name: channelName,
              user: msg.user || 'unknown',
              text: msg.text || '',
              thread_ts: msg.thread_ts,
              reply_count: msg.reply_count,
              reactions: msg.reactions as any,
              files: msg.files as any,
            };

            // Get permalink
            try {
              const permalinkResp = await this.client!.chat.getPermalink({
                channel: channelId,
                message_ts: msg.ts!,
              });
              rawMsg.permalink = permalinkResp.permalink;
            } catch {
              // Ignore permalink errors
            }

            messages.push(rawMsg);

            // Get thread replies if configured
            if (
              this.config.collectors.slack.include_threads &&
              msg.thread_ts &&
              msg.reply_count &&
              msg.reply_count > 0
            ) {
              const replies = await this.getThreadReplies(channelId, channelName, msg.thread_ts);
              messages.push(...replies);
            }
          }
        }
      }

      cursor = response.response_metadata?.next_cursor;
    } while (cursor);

    return messages;
  }

  private async getThreadReplies(
    channelId: string,
    channelName: string,
    threadTs: string
  ): Promise<RawSlackMessage[]> {
    const replies: RawSlackMessage[] = [];
    const creds = getSlackCredentials();

    try {
      const response = await this.client!.conversations.replies({
        channel: channelId,
        ts: threadTs,
        limit: 100,
      });

      if (response.messages) {
        for (const msg of response.messages) {
          if (msg.ts === threadTs) continue; // Skip parent message

          const isFromUser = msg.user === creds.userId;
          const mentionsUser = msg.text?.includes(`<@${creds.userId}>`);

          if (isFromUser || mentionsUser) {
            replies.push({
              ts: msg.ts!,
              channel: channelId,
              channel_name: channelName,
              user: msg.user || 'unknown',
              text: msg.text || '',
              thread_ts: threadTs,
            });
          }
        }
      }
    } catch (error: any) {
      this.logWarn(`Failed to get thread replies: ${error.message}`);
    }

    return replies;
  }

  private async getDirectMessages(): Promise<RawSlackMessage[]> {
    const messages: RawSlackMessage[] = [];
    // Implementation for DMs would go here
    // Requires user token and im:history scope
    return messages;
  }

  private transformMessage(raw: RawSlackMessage): ActivityEvent | null {
    const creds = getSlackCredentials();
    const timestamp = slackTsToDate(raw.ts);

    // Determine event type
    let eventType: ActivityEvent['event_type'] = 'message';
    if (raw.thread_ts && raw.thread_ts !== raw.ts) {
      eventType = 'thread_reply';
    }
    if (raw.files && raw.files.length > 0) {
      eventType = 'file_created';
    }

    // Build source pointers
    const sourcePointers: SourcePointer[] = [];
    if (raw.permalink) {
      sourcePointers.push({
        pointer_id: generatePointerId('slack_message_permalink', raw.permalink),
        type: raw.thread_ts ? 'slack_thread_permalink' : 'slack_message_permalink',
        url: raw.permalink,
        display_text: `Slack message in #${raw.channel_name}`,
      });
    }

    // Build references
    const references: EventReference[] = [];
    if (raw.channel) {
      references.push({
        type: 'channel_id',
        value: raw.channel,
        display_text: raw.channel_name,
      });
    }

    // Extract URLs from message
    const urlMatches = raw.text.match(/<(https?:\/\/[^|>]+)(\|[^>]+)?>/g);
    if (urlMatches) {
      for (const match of urlMatches) {
        const url = match.replace(/<([^|>]+).*>/, '$1');
        references.push({
          type: 'url',
          value: url,
        });
      }
    }

    // Redact PII
    const redacted = redactPII(raw.text, this.config.privacy);

    return {
      event_id: generateEventId('slack', raw.ts, raw.channel),
      source_system: 'slack',
      source_record_id: raw.ts,
      actor_user_id: raw.user,
      actor_display_name: raw.user_name || raw.user,
      event_timestamp_utc: formatUTC(timestamp),
      event_timestamp_local: formatLocalTime(timestamp, this.dateRange.timezone),
      event_type: eventType,
      title: `Message in #${raw.channel_name}`,
      body_text_excerpt: truncateText(redacted.text),
      references,
      source_pointers: sourcePointers,
      pii_redaction_applied: redacted.redactedCount > 0,
      confidence: 'high',
      raw_data: raw,
    };
  }
}
