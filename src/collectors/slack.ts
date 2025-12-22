/**
 * Slack Collector - Search-based
 * Uses Slack Search API to find messages by keywords and date range
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
import { redactPII, truncateText } from "../utils/privacy";

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
      const keywords: string[] = slackConfig.search_keywords || [];
      const searchFromMe = slackConfig.search_from_me !== false;

      const startDate = this.formatDateForSearch(this.dateRange.start);
      const endDate = this.formatDateForSearch(this.dateRange.end);

      if (searchFromMe) {
        this.logInfo("Searching for messages from user...");
        const query = "from:me after:" + startDate + " before:" + endDate;
        const fromMeMessages = await this.searchMessages(query);
        this.logInfo("Found " + fromMeMessages.length + " messages from user");

        for (const msg of fromMeMessages) {
          result.rawData.push(msg);
          const event = this.transformMessage(msg);
          if (event) result.events.push(event);
        }
      }

      for (const keyword of keywords) {
        this.logInfo("Searching for keyword: " + keyword);
        const query = keyword + " after:" + startDate + " before:" + endDate;
        const keywordMessages = await this.searchMessages(query);
        this.logInfo("Found " + keywordMessages.length + " messages for " + keyword);

        for (const msg of keywordMessages) {
          const exists = result.rawData.some((m: any) => m.ts === msg.ts && m.channel === msg.channel);
          if (!exists) {
            result.rawData.push(msg);
            const event = this.transformMessage(msg);
            if (event) result.events.push(event);
          }
        }
      }

      result.recordCount = result.events.length;
      this.logInfo("Collected " + result.recordCount + " events from Slack");
    } catch (error: any) {
      result.errors.push("Slack collection failed: " + error.message);
    }

    return result;
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

    return {
      event_id: generateEventId("slack", raw.ts, raw.channel),
      source_system: "slack",
      source_record_id: raw.ts,
      actor_user_id: raw.user,
      actor_display_name: raw.user_name || raw.user,
      event_timestamp_utc: formatUTC(timestamp),
      event_timestamp_local: formatLocalTime(timestamp, this.dateRange.timezone),
      event_type: eventType,
      title: "Message in #" + raw.channel_name,
      body_text_excerpt: truncateText(redacted.text),
      references,
      source_pointers: sourcePointers,
      pii_redaction_applied: redacted.redactedCount > 0,
      confidence: "high",
      raw_data: raw as unknown as Record<string, unknown>,
    };
  }
}
