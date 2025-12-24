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
      const keywords: string[] = slackConfig.search_keywords || [];

      const startDate = this.formatDateForSearch(this.dateRange.start);
      const endDate = this.formatDateForSearch(this.dateRange.end);

      // ============================================
      // DMs: Coletar TUDO no range de data
      // (conversa direta = sempre relevante)
      // ============================================
      if (collectDMs) {
        this.logInfo("Collecting ALL DMs in date range...");
        const dmQuery = "is:dm after:" + startDate + " before:" + endDate;
        const dmMessages = await this.searchMessages(dmQuery);
        this.logInfo("Found " + dmMessages.length + " DM messages");

        for (const msg of dmMessages) {
          // DMs: marcar como my_work se EU mandei, senão context
          msg.ownership = (msg.user === this.userId) ? "my_work" : "context";
          this.addMessageIfNotExists(result, msg);
        }
      }

      // ============================================
      // CHANNELS/GROUPS/THREADS: Só quando EU participei
      // ============================================

      // 1. FROM ME in channels: Mensagens que EU mandei em canais
      this.logInfo("Collecting messages I sent in channels (from:me -is:dm)...");
      const fromMeChannelQuery = "from:me -is:dm after:" + startDate + " before:" + endDate;
      const fromMeMessages = await this.searchMessages(fromMeChannelQuery);
      this.logInfo("Found " + fromMeMessages.length + " messages I sent in channels");

      for (const msg of fromMeMessages) {
        msg.ownership = "my_work";
        this.addMessageIfNotExists(result, msg);
      }

      // 2. MENTIONS: Onde fui @mencionado em canais
      if (this.userId) {
        this.logInfo("Collecting messages where I was @mentioned...");
        const mentionQuery = "<@" + this.userId + "> -is:dm after:" + startDate + " before:" + endDate;
        const mentionMessages = await this.searchMessages(mentionQuery);
        this.logInfo("Found " + mentionMessages.length + " messages mentioning me");

        for (const msg of mentionMessages) {
          msg.ownership = "mentioned";
          this.addMessageIfNotExists(result, msg);
        }
      }

      // 3. THREADS where I replied: Threads onde EU respondi
      // Slack Search não tem filtro direto para "threads I replied to"
      // Mas from:me já captura minhas respostas em threads
      // Vamos buscar o contexto da thread (parent message) para minhas respostas
      const myThreadReplies = result.events.filter(e => {
        const raw = e.raw_data as any;
        return raw?.thread_ts && raw.thread_ts !== raw.ts;
      });

      if (myThreadReplies.length > 0) {
        this.logInfo("Found " + myThreadReplies.length + " thread replies I made");
        // Thread context já está capturado via from:me
      }

      // 4. KEYWORD SEARCH: Opcional (apenas em canais onde participei)
      if (keywords.length > 0) {
        // Primeiro identificar canais onde participei
        const myActiveChannels = new Set<string>();
        for (const event of result.events) {
          const raw = event.raw_data as any;
          if (raw?.channel_name && raw.ownership === "my_work") {
            myActiveChannels.add(raw.channel_name);
          }
        }

        for (const keyword of keywords) {
          for (const channel of myActiveChannels) {
            this.logInfo("Searching '" + keyword + "' in #" + channel);
            const query = keyword + " in:#" + channel + " after:" + startDate + " before:" + endDate;
            const keywordMessages = await this.searchMessages(query, 20);

            for (const msg of keywordMessages) {
              if (!msg.ownership) {
                msg.ownership = "keyword_match";
              }
              this.addMessageIfNotExists(result, msg);
            }
          }
        }
      }

      // ============================================
      // Estatísticas finais
      // ============================================
      const stats = {
        my_work: 0,
        mentioned: 0,
        context: 0,
        keyword_match: 0
      };

      for (const event of result.events) {
        const ownership = (event.raw_data as any)?.ownership || "context";
        stats[ownership as keyof typeof stats]++;
      }

      result.recordCount = result.events.length;
      this.logInfo("Collected " + result.recordCount + " events from Slack");
      this.logInfo("  MY_WORK: " + stats.my_work + " | MENTIONED: " + stats.mentioned + " | CONTEXT: " + stats.context + " | KEYWORD: " + stats.keyword_match);
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

  private async searchMessages(query: string, limit?: number): Promise<RawSlackMessage[]> {
    const messages: RawSlackMessage[] = [];
    let page = 1;
    const maxPages = limit ? Math.ceil(limit / 100) : 10;
    const maxResults = limit || 1000;

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
