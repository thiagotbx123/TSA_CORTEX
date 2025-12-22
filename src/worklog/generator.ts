/**
 * Worklog Generator
 * Produces Markdown and JSON outputs from normalized events and clusters
 */

import {
  ActivityEvent,
  TopicCluster,
  WorklogOutput,
  WorklogBullet,
  WorklogWorkstream,
  WorklogTimelineEntry,
  SourcePointer,
  WorklogRun,
  CoverageMetrics,
} from '../types';
import { ClusteringResult } from '../clustering';
import { formatDisplay } from '../utils/datetime';

export class WorklogGenerator {
  private run: WorklogRun;
  private events: ActivityEvent[];
  private clusters: TopicCluster[];
  private unclustered: ActivityEvent[];

  constructor(
    run: WorklogRun,
    events: ActivityEvent[],
    clusteringResult: ClusteringResult
  ) {
    this.run = run;
    this.events = events;
    this.clusters = clusteringResult.clusters;
    this.unclustered = clusteringResult.unclustered;
  }

  generate(): WorklogOutput {
    // Collect all source pointers
    const allPointers = this.collectAllPointers();

    // Generate workstreams from clusters
    const workstreams = this.generateWorkstreams();

    // Generate timeline
    const timeline = this.generateTimeline();

    // Generate executive summary
    const executiveSummary = this.generateExecutiveSummary();

    // Generate decisions and blockers
    const decisionsAndBlockers = this.generateDecisionsAndBlockers();

    // Generate gaps
    const gaps = this.generateGaps();

    return {
      run_metadata: this.run,
      executive_summary: executiveSummary,
      workstreams,
      timeline,
      decisions_and_blockers: decisionsAndBlockers,
      gaps_and_data_quality: gaps,
      source_index: allPointers,
    };
  }

  private collectAllPointers(): SourcePointer[] {
    const pointerMap = new Map<string, SourcePointer>();

    for (const event of this.events) {
      for (const pointer of event.source_pointers) {
        if (!pointerMap.has(pointer.pointer_id)) {
          pointerMap.set(pointer.pointer_id, pointer);
        }
      }
    }

    return Array.from(pointerMap.values());
  }

  private generateWorkstreams(): WorklogWorkstream[] {
    return this.clusters.map((cluster) => {
      const whatHappened: WorklogBullet[] = cluster.events
        .slice(0, 5)
        .map((event) => ({
          text: event.title,
          source_pointer_ids: event.source_pointers.map((p) => p.pointer_id),
        }));

      const nextActions: WorklogBullet[] = cluster.follow_ons.map((action) => ({
        text: action,
        source_pointer_ids: [],
      }));

      return {
        name: cluster.cluster_name,
        cluster_type: cluster.cluster_type,
        what_happened: whatHappened,
        why_it_matters: cluster.summary,
        status_now: cluster.status,
        next_actions: nextActions,
      };
    });
  }

  private generateTimeline(): WorklogTimelineEntry[] {
    return this.events
      .sort(
        (a, b) =>
          new Date(a.event_timestamp_utc).getTime() -
          new Date(b.event_timestamp_utc).getTime()
      )
      .map((event) => ({
        timestamp_local: event.event_timestamp_local,
        description: event.title,
        source_pointer_ids: event.source_pointers.map((p) => p.pointer_id),
      }));
  }

  private generateExecutiveSummary(): WorklogBullet[] {
    const summary: WorklogBullet[] = [];

    // Summary by cluster
    for (const cluster of this.clusters.slice(0, 5)) {
      summary.push({
        text: `${cluster.cluster_name}: ${cluster.events.length} activities (${cluster.status})`,
        source_pointer_ids: cluster.source_pointer_ids.slice(0, 3),
      });
    }

    // Add unclustered count if any
    if (this.unclustered.length > 0) {
      summary.push({
        text: `${this.unclustered.length} other activities`,
        source_pointer_ids: this.unclustered
          .slice(0, 3)
          .flatMap((e) => e.source_pointers.map((p) => p.pointer_id)),
      });
    }

    return summary;
  }

  private generateDecisionsAndBlockers(): WorklogBullet[] {
    const items: WorklogBullet[] = [];

    for (const cluster of this.clusters) {
      if (cluster.status === 'blocked') {
        items.push({
          text: `BLOCKED: ${cluster.cluster_name}`,
          source_pointer_ids: cluster.source_pointer_ids.slice(0, 2),
        });
      }
      if (cluster.status === 'completed') {
        items.push({
          text: `COMPLETED: ${cluster.cluster_name}`,
          source_pointer_ids: cluster.source_pointer_ids.slice(0, 2),
        });
      }
    }

    return items;
  }

  private generateGaps(): string[] {
    const gaps: string[] = [];

    // Check for missing sources
    for (const source of this.run.sources_missing) {
      gaps.push(`Data unavailable from ${source}`);
    }

    // Check for low confidence events
    const lowConfidenceCount = this.events.filter((e) => e.confidence === 'low').length;
    if (lowConfidenceCount > 0) {
      gaps.push(`${lowConfidenceCount} events have low confidence`);
    }

    // Add warnings
    for (const warning of this.run.warnings) {
      gaps.push(warning);
    }

    return gaps;
  }

  calculateMetrics(): CoverageMetrics {
    const sourceCoverage: CoverageMetrics['sources_coverage'] = {
      slack: { collected: 0, normalized: 0 },
      linear: { collected: 0, normalized: 0 },
      drive: { collected: 0, normalized: 0 },
      local: { collected: 0, normalized: 0 },
      claude: { collected: 0, normalized: 0 },
    };

    for (const event of this.events) {
      sourceCoverage[event.source_system].normalized++;
    }

    for (const [source, count] of Object.entries(this.run.record_counts_by_source)) {
      sourceCoverage[source as keyof typeof sourceCoverage].collected = count;
    }

    const eventsWithPointers = this.events.filter(
      (e) => e.source_pointers.length > 0
    ).length;

    return {
      total_events: this.events.length,
      events_with_source_pointers: eventsWithPointers,
      percent_with_pointers:
        this.events.length > 0
          ? Math.round((eventsWithPointers / this.events.length) * 100)
          : 0,
      cluster_count: this.clusters.length,
      gap_count: this.run.warnings.length + this.run.sources_missing.length,
      events_deduped: 0, // Set by normalizer
      percent_deduped: 0,
      sources_coverage: sourceCoverage,
    };
  }
}

export function generateWorklog(
  run: WorklogRun,
  events: ActivityEvent[],
  clusteringResult: ClusteringResult
): WorklogOutput {
  const generator = new WorklogGenerator(run, events, clusteringResult);
  return generator.generate();
}
