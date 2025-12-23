/**
 * Slack Collector - Channel and Search-based
 * Collects ALL messages from target channels and DMs
 */

import { WebClient } from "@slack/web-api";
import { BaseCollector, CollectorResult } from "./base";
import {
  ActivityEvent,
  SourceSystem,
  RawSlackMessage,
  SourcePointer,
  EventReference,
} from "../types";
import { formatUTC, formatLocalTime } from "../utils/datetime";
import { generateEventId, generatePointerId } from "../utils/hash";
import { getSlackCredentials } from "../utils/config";
import { redactPII } from "../utils/privacy";

export class SlackCollector extends BaseCollector {
  private client: WebClient | null = null;

  get source(): SourceSystem {
    return "slack";
  }

  isConfigured(): boolean {
    if (!this.config.collectors.slack.enabled) {
      return false;
    }
    const creds = getSlackCredentials();
    return !!creds.userToken;
  }

  async collect(): Promise<CollectorResult> {
    const result = this.createEmptyResult();

    if (!this.isConfigured()) {
      result.errors.push("Slack collector requires SLACK_USER_TOKEN with search:read scope");
      return result;
    }

    const creds = getSlackCredentials();
    this.client = new WebClient(creds.userToken);

    try {
      const slackConfig = this.config.collectors.slack as any;
      const targetChannels: string[] = slackConfig.target_channels || [];
      const collectDMs = slackConfig.collect_dms !== false;
      const searchFromMe = slackConfig.search_from_me !== false;
      const keywords: string[] = slackConfig.search_keywords || [];

      const startDate = this.formatDateForSearch(this.dateRange.start);
      const endDate = this.formatDateForSearch(this.dateRange.end);

      // 1. Collect ALL messages from target channels
      for (const channel of targetChannels) {
        this.logInfo("Collecting all messages from #" + channel + "...");
        const query = "in:#" + channel + " after:" + startDate + " before:" + endDate;
        const channelMessages = await this.searchMessages(query);
        this.logInfo("Found " + channelMessages.length + " messages in #" + channel);

        for (const msg of channelMessages) {
          this.addMessageIfNotExists(result, msg);
        }
      }

      // 2. Collect ALL DMs
      if (collectDMs) {
        this.logInfo("Collecting all DMs...");
        const dmQuery = "is:dm after:" + startDate + " before:" + endDate;
        const dmMessages = await this.searchMessages(dmQuery);
        this.logInfo("Found " + dmMessages.length + " DM messages");

        for (const msg of dmMessages) {
          this.addMessageIfNotExists(result, msg);
        }
      }

      // 3. Collect messages from user (safety net)
      if (searchFromMe) {
        this.logInfo("Collecting messages from user...");
        const query = "from:me after:" + startDate + " before:" + endDate;
        const fromMeMessages = await this.searchMessages(query);
        this.logInfo("Found " + fromMeMessages.length + " messages from user");

        for (const msg of fromMeMessages) {
          this.addMessageIfNotExists(result, msg);
        }
      }

      // 4. Optional: keyword search (backward compatible)
      for (const keyword of keywords) {
        this.logInfo("Searching for keyword: " + keyword);
        const query = keyword + " after:" + startDate + " before:" + endDate;
        const keywordMessages = await this.searchMessages(query);
        this.logInfo("Found " + keywordMessages.length + " messages for " + keyword);

        for (const msg of keywordMessages) {
          this.addMessageIfNotExists(result, msg);
        }
      }

      result.recordCount = result.events.length;
      this.logInfo("Collected " + result.recordCount + " events from Slack");
    } catch (error: any) {
      result.errors.push("Slack collection failed: " + error.message);
    }

    return result;
  }

  private addMessageIfNotExists(result: CollectorResult, msg: RawSlackMessage): void {
    const exists = result.rawData.some((m: any) => m.ts === msg.ts && m.channel === msg.channel);
    if (!exists) {
      result.rawData.push(msg);
      const event = this.transformMessage(msg);
      if (event) result.events.push(event);
    }
  }

  private formatDateForSearch(date: Date): string {
    return date.toISOString().split("T")[0];
  }

  private async searchMessages(query: string): Promise<RawSlackMessage[]> {
    const messages: RawSlackMessage[] = [];
    let page = 1;
    const maxPages = 10;

    try {
      while (page <= maxPages) {
        const response = await this.client!.search.messages({
          query,
          sort: "timestamp",
          sort_dir: "desc",
          count: 100,
          page,
        });

        if (!response.messages?.matches || response.messages.matches.length === 0) {
          break;
        }

        for (const match of response.messages.matches) {
          messages.push({
            ts: match.ts!,
            channel: match.channel?.id || "",
            channel_name: match.channel?.name || "unknown",
            user: match.user || match.username || "unknown",
            user_name: match.username,
            text: match.text || "",
            permalink: match.permalink,
            thread_ts: (match as any).thread_ts,
          });
        }

        const totalPages = Math.ceil((response.messages.total || 0) / 100);
        if (page >= totalPages) break;
        page++;
      }
    } catch (error: any) {
      this.logWarn("Search failed: " + error.message);
    }

    return messages;
  }

  private transformMessage(raw: RawSlackMessage): ActivityEvent | null {
    const timestamp = new Date(parseFloat(raw.ts) * 1000);

    let eventType: ActivityEvent["event_type"] = "message";
    if (raw.thread_ts && raw.thread_ts !== raw.ts) {
      eventType = "thread_reply";
    }

    const sourcePointers: SourcePointer[] = [];
    if (raw.permalink) {
      sourcePointers.push({
        pointer_id: generatePointerId("slack_message_permalink", raw.permalink),
        type: "slack_message_permalink",
        url: raw.permalink,
        display_text: "Slack message in #" + raw.channel_name,
      });
    }

    const references: EventReference[] = [];
    if (raw.channel) {
      references.push({
        type: "channel_id",
        value: raw.channel,
        display_text: raw.channel_name,
      });
    }

    const redacted = redactPII(raw.text, this.config.privacy);

    // Create descriptive title from message content
    const title = this.createMessageTitle(redacted.text, raw.channel_name || "unknown");

    return {
      event_id: generateEventId("slack", raw.ts, raw.channel),
      source_system: "slack",
      source_record_id: raw.ts,
      actor_user_id: raw.user,
      actor_display_name: raw.user_name || raw.user,
      event_timestamp_utc: formatUTC(timestamp),
      event_timestamp_local: formatLocalTime(timestamp, this.dateRange.timezone),
      event_type: eventType,
      title: title,
      body_text_excerpt: redacted.text, // Store FULL text, not truncated
      references,
      source_pointers: sourcePointers,
      pii_redaction_applied: redacted.redactedCount > 0,
      confidence: "high",
      raw_data: raw as unknown as Record<string, unknown>,
    };
  }

  private createMessageTitle(text: string, channelName: string): string {
    // Clean up the text
    const cleaned = text
      .replace(/<[^>]+>/g, '') // Remove Slack formatting
      .replace(/\n+/g, ' ')    // Replace newlines with spaces
      .replace(/\s+/g, ' ')    // Collapse whitespace
      .trim();

    if (!cleaned) {
      return "[#" + channelName + "] (attachment/file)";
    }

    // Get first 120 chars as title
    const maxLen = 120;
    if (cleaned.length <= maxLen) {
      return "[#" + channelName + "] " + cleaned;
    }

    // Try to cut at word boundary
    const truncated = cleaned.substring(0, maxLen);
    const lastSpace = truncated.lastIndexOf(' ');
    if (lastSpace > maxLen * 0.7) {
      return "[#" + channelName + "] " + truncated.substring(0, lastSpace) + "...";
    }

    return "[#" + channelName + "] " + truncated + "...";
  }
}
