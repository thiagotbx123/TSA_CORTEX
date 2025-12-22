/**
 * Linear Collector
 * Collects issues, comments, and status changes from Linear
 */

import { LinearClient } from '@linear/sdk';
import { BaseCollector, CollectorResult } from './base';
import {
  ActivityEvent,
  SourceSystem,
  RawLinearIssue,
  SourcePointer,
  EventReference,
  Config,
} from '../types';
import { DateRange, formatUTC, formatLocalTime, isWithinDateRange } from '../utils/datetime';
import { generateEventId, generatePointerId } from '../utils/hash';
import { getLinearCredentials } from '../utils/config';
import { redactPII, truncateText } from '../utils/privacy';

export class LinearCollector extends BaseCollector {
  private client: LinearClient | null = null;

  get source(): SourceSystem {
    return 'linear';
  }

  isConfigured(): boolean {
    if (!this.config.collectors.linear.enabled) {
      return false;
    }
    const creds = getLinearCredentials();
    return !!creds.apiKey;
  }

  async collect(): Promise<CollectorResult> {
    const result = this.createEmptyResult();

    if (!this.isConfigured()) {
      result.errors.push('Linear collector is not configured');
      return result;
    }

    const creds = getLinearCredentials();
    this.client = new LinearClient({ apiKey: creds.apiKey! });

    try {
      // Get current user
      const me = await this.client.viewer;
      const userId = me.id;
      this.logInfo(`Collecting Linear data for user: ${me.name}`);

      // Get issues created by user
      const createdIssues = await this.getIssuesCreatedBy(userId);
      this.logInfo(`Found ${createdIssues.length} issues created by user`);

      // Get issues assigned to user
      const assignedIssues = await this.getIssuesAssignedTo(userId);
      this.logInfo(`Found ${assignedIssues.length} issues assigned to user`);

      // Get issues where user commented
      const commentedIssues = await this.getIssuesCommentedOn(userId);
      this.logInfo(`Found ${commentedIssues.length} issues with user comments`);

      // Merge and deduplicate issues
      const allIssues = this.deduplicateIssues([
        ...createdIssues,
        ...assignedIssues,
        ...commentedIssues,
      ]);

      result.rawData = allIssues;

      // Transform to events
      for (const issue of allIssues) {
        const events = this.transformIssue(issue, userId);
        result.events.push(...events);
      }

      result.recordCount = result.events.length;
      this.logInfo(`Collected ${result.recordCount} events from Linear`);
    } catch (error: any) {
      result.errors.push(`Linear collection failed: ${error.message}`);
    }

    return result;
  }

  private async getIssuesCreatedBy(userId: string): Promise<RawLinearIssue[]> {
    const issues: RawLinearIssue[] = [];

    try {
      const result = await this.client!.issues({
        filter: {
          creator: { id: { eq: userId } },
          createdAt: {
            gte: this.dateRange.start,
            lte: this.dateRange.end,
          },
        },
        first: 100,
      });

      for (const issue of result.nodes) {
        const rawIssue = await this.fetchFullIssue(issue.id);
        if (rawIssue) {
          issues.push(rawIssue);
        }
      }
    } catch (error: any) {
      this.logWarn(`Failed to get created issues: ${error.message}`);
    }

    return issues;
  }

  private async getIssuesAssignedTo(userId: string): Promise<RawLinearIssue[]> {
    const issues: RawLinearIssue[] = [];

    try {
      const result = await this.client!.issues({
        filter: {
          assignee: { id: { eq: userId } },
          updatedAt: {
            gte: this.dateRange.start,
            lte: this.dateRange.end,
          },
        },
        first: 100,
      });

      for (const issue of result.nodes) {
        const rawIssue = await this.fetchFullIssue(issue.id);
        if (rawIssue) {
          issues.push(rawIssue);
        }
      }
    } catch (error: any) {
      this.logWarn(`Failed to get assigned issues: ${error.message}`);
    }

    return issues;
  }

  private async getIssuesCommentedOn(userId: string): Promise<RawLinearIssue[]> {
    const issues: RawLinearIssue[] = [];
    const seenIds = new Set<string>();

    try {
      // Get user's comments within date range
      const comments = await this.client!.comments({
        filter: {
          user: { id: { eq: userId } },
          createdAt: {
            gte: this.dateRange.start,
            lte: this.dateRange.end,
          },
        },
        first: 100,
      });

      for (const comment of comments.nodes) {
        const issue = await comment.issue;
        if (issue && !seenIds.has(issue.id)) {
          seenIds.add(issue.id);
          const rawIssue = await this.fetchFullIssue(issue.id);
          if (rawIssue) {
            issues.push(rawIssue);
          }
        }
      }
    } catch (error: any) {
      this.logWarn(`Failed to get commented issues: ${error.message}`);
    }

    return issues;
  }

  private async fetchFullIssue(issueId: string): Promise<RawLinearIssue | null> {
    try {
      const issue = await this.client!.issue(issueId);
      const state = await issue.state;
      const assignee = await issue.assignee;
      const creator = await issue.creator;

      // Get comments
      const commentsResult = await issue.comments({ first: 50 });
      const comments: RawLinearIssue['comments'] = [];

      for (const comment of commentsResult.nodes) {
        const user = await comment.user;
        comments.push({
          id: comment.id,
          body: comment.body,
          user: { id: user?.id || 'unknown', name: user?.name || 'Unknown' },
          createdAt: comment.createdAt.toISOString(),
        });
      }

      return {
        id: issue.id,
        identifier: issue.identifier,
        title: issue.title,
        description: issue.description,
        state: { name: state?.name || 'Unknown' },
        assignee: assignee ? { id: assignee.id, name: assignee.name } : undefined,
        creator: creator ? { id: creator.id, name: creator.name } : undefined,
        createdAt: issue.createdAt.toISOString(),
        updatedAt: issue.updatedAt.toISOString(),
        comments,
        url: issue.url,
      };
    } catch (error: any) {
      this.logWarn(`Failed to fetch issue ${issueId}: ${error.message}`);
      return null;
    }
  }

  private deduplicateIssues(issues: RawLinearIssue[]): RawLinearIssue[] {
    const seen = new Map<string, RawLinearIssue>();
    for (const issue of issues) {
      seen.set(issue.id, issue);
    }
    return Array.from(seen.values());
  }

  private transformIssue(issue: RawLinearIssue, userId: string): ActivityEvent[] {
    const events: ActivityEvent[] = [];

    // Create event for issue creation if within range
    if (
      issue.creator?.id === userId &&
      isWithinDateRange(issue.createdAt, this.dateRange)
    ) {
      events.push(this.createIssueEvent(issue, 'issue_created', issue.createdAt));
    }

    // Create events for comments
    if (issue.comments && this.config.collectors.linear.include_comments) {
      for (const comment of issue.comments) {
        if (
          comment.user.id === userId &&
          isWithinDateRange(comment.createdAt, this.dateRange)
        ) {
          events.push(this.createCommentEvent(issue, comment));
        }
      }
    }

    // If issue was updated in range and user is assignee
    if (
      issue.assignee?.id === userId &&
      isWithinDateRange(issue.updatedAt, this.dateRange) &&
      !events.some((e) => e.event_type === 'issue_created')
    ) {
      events.push(this.createIssueEvent(issue, 'issue_updated', issue.updatedAt));
    }

    return events;
  }

  private createIssueEvent(
    issue: RawLinearIssue,
    eventType: ActivityEvent['event_type'],
    timestamp: string
  ): ActivityEvent {
    const redacted = redactPII(issue.description || '', this.config.privacy);

    return {
      event_id: generateEventId('linear', issue.id, timestamp),
      source_system: 'linear',
      source_record_id: issue.id,
      actor_user_id: issue.creator?.id || 'unknown',
      actor_display_name: issue.creator?.name || 'Unknown',
      event_timestamp_utc: formatUTC(new Date(timestamp)),
      event_timestamp_local: formatLocalTime(new Date(timestamp), this.dateRange.timezone),
      event_type: eventType,
      title: `[${issue.identifier}] ${issue.title}`,
      body_text_excerpt: truncateText(redacted.text),
      references: [
        { type: 'issue_id', value: issue.identifier, display_text: issue.identifier },
        { type: 'url', value: issue.url, display_text: issue.identifier },
      ],
      source_pointers: [
        {
          pointer_id: generatePointerId('linear_issue_url', issue.url),
          type: 'linear_issue_url',
          url: issue.url,
          display_text: `Linear ${issue.identifier}`,
        },
      ],
      pii_redaction_applied: redacted.redactedCount > 0,
      confidence: 'high',
      raw_data: issue as unknown as Record<string, unknown>,
    };
  }

  private createCommentEvent(
    issue: RawLinearIssue,
    comment: NonNullable<RawLinearIssue['comments']>[0]
  ): ActivityEvent {
    const redacted = redactPII(comment.body, this.config.privacy);
    const commentUrl = `${issue.url}#comment-${comment.id}`;

    return {
      event_id: generateEventId('linear', comment.id, comment.createdAt),
      source_system: 'linear',
      source_record_id: comment.id,
      actor_user_id: comment.user.id,
      actor_display_name: comment.user.name,
      event_timestamp_utc: formatUTC(new Date(comment.createdAt)),
      event_timestamp_local: formatLocalTime(new Date(comment.createdAt), this.dateRange.timezone),
      event_type: 'comment',
      title: `Comment on [${issue.identifier}] ${issue.title}`,
      body_text_excerpt: truncateText(redacted.text),
      references: [
        { type: 'issue_id', value: issue.identifier, display_text: issue.identifier },
      ],
      source_pointers: [
        {
          pointer_id: generatePointerId('linear_comment_url', commentUrl),
          type: 'linear_comment_url',
          url: commentUrl,
          display_text: `Comment on ${issue.identifier}`,
        },
      ],
      pii_redaction_applied: redacted.redactedCount > 0,
      confidence: 'high',
    };
  }
}
