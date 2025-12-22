/**
 * Event Normalizer
 * Merges, deduplicates, and normalizes events from all collectors
 */

import { ActivityEvent, SourceSystem, Manifest, WorklogRun } from '../types';
import { CollectorResult } from '../collectors';
import { DateRange } from '../utils/datetime';
import { generateChecksum, generateRunId } from '../utils/hash';

export interface NormalizationResult {
  events: ActivityEvent[];
  manifest: Manifest;
  duplicatesRemoved: number;
  totalOriginal: number;
}

export class EventNormalizer {
  private dateRange: DateRange;
  private userId: string;
  private userDisplayName: string;

  constructor(dateRange: DateRange, userId: string, userDisplayName: string) {
    this.dateRange = dateRange;
    this.userId = userId;
    this.userDisplayName = userDisplayName;
  }

  normalize(collectorResults: Map<SourceSystem, CollectorResult>): NormalizationResult {
    // Collect all events
    const allEvents: ActivityEvent[] = [];
    const recordCounts: Record<SourceSystem, number> = {
      slack: 0,
      linear: 0,
      drive: 0,
      local: 0,
      claude: 0,
    };

    const sourcesIncluded: SourceSystem[] = [];
    const sourcesMissing: SourceSystem[] = [];
    const warnings: string[] = [];

    for (const [source, result] of collectorResults) {
      if (result.errors.length > 0) {
        sourcesMissing.push(source);
        warnings.push(...result.errors);
      } else {
        sourcesIncluded.push(source);
        allEvents.push(...result.events);
        recordCounts[source] = result.recordCount;
      }
      warnings.push(...result.warnings);
    }

    const totalOriginal = allEvents.length;

    // Sort by timestamp
    allEvents.sort((a, b) =>
      new Date(a.event_timestamp_utc).getTime() - new Date(b.event_timestamp_utc).getTime()
    );

    // Deduplicate events
    const deduplicatedEvents = this.deduplicateEvents(allEvents);
    const duplicatesRemoved = totalOriginal - deduplicatedEvents.length;

    // Create manifest
    const run: WorklogRun = {
      run_id: generateRunId(),
      person_id: this.userId,
      person_display_name: this.userDisplayName,
      start_datetime: this.dateRange.start.toISOString(),
      end_datetime: this.dateRange.end.toISOString(),
      timezone: this.dateRange.timezone,
      created_at: new Date().toISOString(),
      collector_version: '1.0.0',
      record_counts_by_source: recordCounts,
      sources_included: sourcesIncluded,
      sources_missing: sourcesMissing,
      warnings,
      status: 'normalizing',
    };

    const manifest: Manifest = {
      run,
      files: [],
      checksums: {
        normalized_events: generateChecksum(deduplicatedEvents),
      },
    };

    return {
      events: deduplicatedEvents,
      manifest,
      duplicatesRemoved,
      totalOriginal,
    };
  }

  private deduplicateEvents(events: ActivityEvent[]): ActivityEvent[] {
    const seen = new Map<string, ActivityEvent>();

    for (const event of events) {
      // Create dedup key based on source pointers and content
      const dedupKey = this.createDedupKey(event);

      if (!seen.has(dedupKey)) {
        seen.set(dedupKey, event);
      } else {
        // Merge source pointers if same event from different contexts
        const existing = seen.get(dedupKey)!;
        this.mergeEvents(existing, event);
      }
    }

    return Array.from(seen.values());
  }

  private createDedupKey(event: ActivityEvent): string {
    // Use source pointers URLs/paths as primary dedup key
    const pointerUrls = event.source_pointers
      .map((p) => p.url || p.path || '')
      .filter(Boolean)
      .sort()
      .join('|');

    if (pointerUrls) {
      return `${event.source_system}:${pointerUrls}`;
    }

    // Fallback to event_id
    return event.event_id;
  }

  private mergeEvents(existing: ActivityEvent, incoming: ActivityEvent): void {
    // Merge source pointers
    const existingPointerIds = new Set(existing.source_pointers.map((p) => p.pointer_id));

    for (const pointer of incoming.source_pointers) {
      if (!existingPointerIds.has(pointer.pointer_id)) {
        existing.source_pointers.push(pointer);
      }
    }

    // Merge references
    const existingRefKeys = new Set(
      existing.references.map((r) => `${r.type}:${r.value}`)
    );

    for (const ref of incoming.references) {
      const key = `${ref.type}:${ref.value}`;
      if (!existingRefKeys.has(key)) {
        existing.references.push(ref);
      }
    }
  }
}

export function normalizeEvents(
  collectorResults: Map<SourceSystem, CollectorResult>,
  dateRange: DateRange,
  userId: string,
  userDisplayName: string
): NormalizationResult {
  const normalizer = new EventNormalizer(dateRange, userId, userDisplayName);
  return normalizer.normalize(collectorResults);
}
