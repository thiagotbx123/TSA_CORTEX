/**
 * TSA_CORTEX - Weekly Worklog Automation
 * Main entry point for programmatic usage
 */

// Export types
export * from './types';

// Export utilities
export * from './utils';

// Export collectors
export {
  BaseCollector,
  CollectorResult,
  SlackCollector,
  LinearCollector,
  DriveCollector,
  LocalCollector,
  createCollector,
  getAllCollectors,
  runAllCollectors,
} from './collectors';

// Export normalizer
export { EventNormalizer, normalizeEvents, NormalizationResult } from './normalizer';

// Export clustering
export { TopicClusterer, clusterEvents, ClusteringResult } from './clustering';

// Export worklog generator
export { WorklogGenerator, generateWorklog, renderWorklogMarkdown, renderLinearBody } from './worklog';

// Export Linear poster
export { LinearPoster, postToLinear } from './linear';

// Main pipeline function
import { Config, WorklogOutput, SourceSystem } from './types';
import { loadConfig } from './utils/config';
import { parseDateRange, DateRange } from './utils/datetime';
import { runAllCollectors } from './collectors';
import { normalizeEvents } from './normalizer';
import { clusterEvents } from './clustering';
import { generateWorklog } from './worklog';
import { postToLinear } from './linear';

export interface PipelineOptions {
  startDate?: string;
  endDate?: string;
  timezone?: string;
  role?: string;
  dryRun?: boolean;
  configPath?: string;
  userId: string;
  userDisplayName: string;
}

export interface PipelineResult {
  worklog: WorklogOutput;
  linearUrl?: string;
  errors: string[];
}

export async function runPipeline(options: PipelineOptions): Promise<PipelineResult> {
  const config = loadConfig(options.configPath);
  const timezone = options.timezone || config.default_timezone;
  const dateRange = parseDateRange(
    options.startDate,
    options.endDate,
    timezone,
    config.default_range_days
  );

  // Collect
  const collectorResults = await runAllCollectors(config, dateRange, options.userId);

  // Normalize
  const normalization = normalizeEvents(
    collectorResults,
    dateRange,
    options.userId,
    options.userDisplayName
  );

  // Cluster
  const clustering = clusterEvents(normalization.events);

  // Generate worklog
  const worklog = generateWorklog(
    normalization.manifest.run,
    normalization.events,
    clustering
  );

  // Post to Linear
  let linearUrl: string | undefined;
  const errors: string[] = [];

  if (!options.dryRun) {
    const result = await postToLinear(
      worklog,
      config,
      options.role || 'tsa',
      false
    );

    if (result.success) {
      linearUrl = result.issue_url;
    } else {
      errors.push(result.error_message || 'Failed to post to Linear');
    }
  }

  return {
    worklog,
    linearUrl,
    errors,
  };
}
