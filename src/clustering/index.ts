/**
 * Topic Clustering
 * Groups related events into workstreams/topics
 */

import {
  ActivityEvent,
  TopicCluster,
  ClusterType,
  SourcePointer,
} from '../types';
import { generateClusterId } from '../utils/hash';

export interface ClusteringResult {
  clusters: TopicCluster[];
  unclustered: ActivityEvent[];
}

// Keywords for cluster type detection
const CLUSTER_KEYWORDS: Record<ClusterType, string[]> = {
  customer: ['customer', 'client', 'support', 'ticket', 'request', 'feedback'],
  project: ['project', 'milestone', 'sprint', 'epic', 'roadmap', 'planning'],
  incident: ['incident', 'outage', 'bug', 'error', 'fix', 'hotfix', 'urgent', 'critical'],
  feature: ['feature', 'implement', 'build', 'develop', 'create', 'add'],
  ops: ['deploy', 'release', 'infrastructure', 'monitoring', 'devops', 'ci/cd'],
  internal: ['internal', 'team', 'meeting', 'sync', 'standup', '1:1', 'retro'],
  meeting: ['meeting', 'call', 'sync', 'standup', 'review', 'demo'],
  documentation: ['doc', 'readme', 'wiki', 'guide', 'tutorial', 'documentation'],
  other: [],
};

export class TopicClusterer {
  cluster(events: ActivityEvent[]): ClusteringResult {
    const clusters: TopicCluster[] = [];
    const unclustered: ActivityEvent[] = [];
    const eventToClusters = new Map<string, TopicCluster>();

    // First pass: detect cluster types and group by Linear issues
    const issueGroups = this.groupByIssue(events);

    for (const [issueId, issueEvents] of issueGroups) {
      if (issueId !== 'no_issue') {
        const cluster = this.createClusterFromIssue(issueId, issueEvents);
        clusters.push(cluster);

        for (const event of issueEvents) {
          eventToClusters.set(event.event_id, cluster);
        }
      }
    }

    // Second pass: cluster remaining events by type/keywords
    const remainingEvents = events.filter((e) => !eventToClusters.has(e.event_id));
    const keywordClusters = this.clusterByKeywords(remainingEvents);

    for (const cluster of keywordClusters) {
      if (cluster.events.length >= 2) {
        clusters.push(cluster);
        for (const event of cluster.events) {
          eventToClusters.set(event.event_id, cluster);
        }
      }
    }

    // Collect unclustered events
    for (const event of events) {
      if (!eventToClusters.has(event.event_id)) {
        unclustered.push(event);
      }
    }

    // Sort clusters by event count and recency
    clusters.sort((a, b) => {
      if (b.events.length !== a.events.length) {
        return b.events.length - a.events.length;
      }
      const aLatest = Math.max(...a.events.map((e) => new Date(e.event_timestamp_utc).getTime()));
      const bLatest = Math.max(...b.events.map((e) => new Date(e.event_timestamp_utc).getTime()));
      return bLatest - aLatest;
    });

    return { clusters, unclustered };
  }

  private groupByIssue(events: ActivityEvent[]): Map<string, ActivityEvent[]> {
    const groups = new Map<string, ActivityEvent[]>();

    for (const event of events) {
      let issueId = 'no_issue';

      // Check references for issue IDs
      for (const ref of event.references) {
        if (ref.type === 'issue_id') {
          issueId = ref.value;
          break;
        }
      }

      // Also check title for issue identifiers like "ABC-123"
      const titleMatch = event.title.match(/\[([A-Z]+-\d+)\]/);
      if (titleMatch) {
        issueId = titleMatch[1];
      }

      if (!groups.has(issueId)) {
        groups.set(issueId, []);
      }
      groups.get(issueId)!.push(event);
    }

    return groups;
  }

  private createClusterFromIssue(issueId: string, events: ActivityEvent[]): TopicCluster {
    const clusterType = this.detectClusterType(events);
    const title = this.extractIssueTitle(events);

    // Collect all source pointer IDs
    const sourcePointerIds = new Set<string>();
    for (const event of events) {
      for (const pointer of event.source_pointers) {
        sourcePointerIds.add(pointer.pointer_id);
      }
    }

    return {
      cluster_id: generateClusterId(),
      cluster_name: title || issueId,
      cluster_type: clusterType,
      events: events.sort(
        (a, b) =>
          new Date(a.event_timestamp_utc).getTime() - new Date(b.event_timestamp_utc).getTime()
      ),
      summary: this.generateSummary(events),
      antecedents: [],
      actions_taken: this.extractActions(events),
      outcomes: [],
      follow_ons: [],
      status: this.detectStatus(events),
      source_pointer_ids: Array.from(sourcePointerIds),
    };
  }

  private clusterByKeywords(events: ActivityEvent[]): TopicCluster[] {
    const typeGroups = new Map<ClusterType, ActivityEvent[]>();

    for (const event of events) {
      const clusterType = this.detectEventClusterType(event);

      if (!typeGroups.has(clusterType)) {
        typeGroups.set(clusterType, []);
      }
      typeGroups.get(clusterType)!.push(event);
    }

    const clusters: TopicCluster[] = [];

    for (const [clusterType, typeEvents] of typeGroups) {
      if (typeEvents.length >= 2) {
        const sourcePointerIds = new Set<string>();
        for (const event of typeEvents) {
          for (const pointer of event.source_pointers) {
            sourcePointerIds.add(pointer.pointer_id);
          }
        }

        clusters.push({
          cluster_id: generateClusterId(),
          cluster_name: this.getClusterTypeName(clusterType),
          cluster_type: clusterType,
          events: typeEvents.sort(
            (a, b) =>
              new Date(a.event_timestamp_utc).getTime() -
              new Date(b.event_timestamp_utc).getTime()
          ),
          summary: this.generateSummary(typeEvents),
          antecedents: [],
          actions_taken: this.extractActions(typeEvents),
          outcomes: [],
          follow_ons: [],
          status: 'active',
          source_pointer_ids: Array.from(sourcePointerIds),
        });
      }
    }

    return clusters;
  }

  private detectClusterType(events: ActivityEvent[]): ClusterType {
    const text = events
      .map((e) => `${e.title} ${e.body_text_excerpt}`)
      .join(' ')
      .toLowerCase();

    for (const [type, keywords] of Object.entries(CLUSTER_KEYWORDS)) {
      if (type === 'other') continue;
      for (const keyword of keywords) {
        if (text.includes(keyword)) {
          return type as ClusterType;
        }
      }
    }

    return 'other';
  }

  private detectEventClusterType(event: ActivityEvent): ClusterType {
    const text = `${event.title} ${event.body_text_excerpt}`.toLowerCase();

    for (const [type, keywords] of Object.entries(CLUSTER_KEYWORDS)) {
      if (type === 'other') continue;
      for (const keyword of keywords) {
        if (text.includes(keyword)) {
          return type as ClusterType;
        }
      }
    }

    // Fallback based on event type
    switch (event.event_type) {
      case 'file_created':
      case 'file_modified':
        return 'documentation';
      case 'meeting_note':
        return 'meeting';
      default:
        return 'other';
    }
  }

  private extractIssueTitle(events: ActivityEvent[]): string {
    for (const event of events) {
      if (event.source_system === 'linear' && event.event_type === 'issue_created') {
        return event.title;
      }
    }
    return events[0]?.title || 'Untitled';
  }

  private generateSummary(events: ActivityEvent[]): string {
    const count = events.length;
    const sources = new Set(events.map((e) => e.source_system));
    const sourceList = Array.from(sources);

    // Generate natural summary based on event types
    const hasComments = events.some((e) => e.event_type === 'comment');
    const hasIssues = events.some((e) => e.event_type === 'issue_created' || e.event_type === 'issue_updated');
    const hasMessages = events.some((e) => e.event_type === 'message' || e.event_type === 'thread_reply');
    const hasFiles = events.some((e) => e.event_type === 'file_created' || e.event_type === 'file_modified');

    const activities: string[] = [];
    if (hasIssues) activities.push('issue updates');
    if (hasComments) activities.push('comments');
    if (hasMessages) activities.push('discussions');
    if (hasFiles) activities.push('file changes');

    if (activities.length === 0) {
      return `${count} activities tracked from ${sourceList.join(' and ')}`;
    }

    const activityText = activities.slice(0, 2).join(' and ');
    if (sourceList.length === 1) {
      return `Includes ${activityText} from ${sourceList[0]}`;
    }
    return `Includes ${activityText} across ${sourceList.length} sources`;
  }

  private extractActions(events: ActivityEvent[]): string[] {
    const actions: string[] = [];

    for (const event of events) {
      if (
        event.event_type === 'comment' ||
        event.event_type === 'issue_created' ||
        event.event_type === 'file_created'
      ) {
        actions.push(event.title);
      }
    }

    return actions.slice(0, 5); // Limit to 5 actions
  }

  private detectStatus(events: ActivityEvent[]): TopicCluster['status'] {
    const latestEvent = events[events.length - 1];

    // Check for completion indicators
    const completionKeywords = ['done', 'completed', 'closed', 'merged', 'shipped'];
    const text = `${latestEvent.title} ${latestEvent.body_text_excerpt}`.toLowerCase();

    for (const keyword of completionKeywords) {
      if (text.includes(keyword)) {
        return 'completed';
      }
    }

    // Check for blocked indicators
    const blockedKeywords = ['blocked', 'waiting', 'on hold', 'stuck'];
    for (const keyword of blockedKeywords) {
      if (text.includes(keyword)) {
        return 'blocked';
      }
    }

    return 'active';
  }

  private getClusterTypeName(type: ClusterType): string {
    const names: Record<ClusterType, string> = {
      customer: 'Customer Work',
      project: 'Project Work',
      incident: 'Incidents & Fixes',
      feature: 'Feature Development',
      ops: 'Operations & DevOps',
      internal: 'Internal & Team',
      meeting: 'Meetings',
      documentation: 'Documentation',
      other: 'Other Activities',
    };
    return names[type];
  }
}

export function clusterEvents(events: ActivityEvent[]): ClusteringResult {
  const clusterer = new TopicClusterer();
  return clusterer.cluster(events);
}
