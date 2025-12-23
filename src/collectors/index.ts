/**
 * Collectors barrel export and factory
 */

import { Config, SourceSystem } from '../types';
import { DateRange } from '../utils/datetime';
import { BaseCollector, CollectorResult } from './base';
import { SlackCollector } from './slack';
import { LinearCollector } from './linear';
import { DriveCollector } from './drive';
import { LocalCollector } from './local';
import { ClaudeCollector } from './claude';

export { BaseCollector, CollectorResult } from './base';
export { SlackCollector } from './slack';
export { LinearCollector } from './linear';
export { DriveCollector } from './drive';
export { LocalCollector } from './local';
export { ClaudeCollector } from './claude';

export function createCollector(
  source: SourceSystem,
  config: Config,
  dateRange: DateRange,
  userId: string
): BaseCollector | null {
  switch (source) {
    case 'slack':
      return new SlackCollector(config, dateRange, userId);
    case 'linear':
      return new LinearCollector(config, dateRange, userId);
    case 'drive':
      return new DriveCollector(config, dateRange, userId);
    case 'local':
      return new LocalCollector(config, dateRange, userId);
    case 'claude':
      return new ClaudeCollector(config, dateRange, userId);
    default:
      return null;
  }
}

export function getAllCollectors(
  config: Config,
  dateRange: DateRange,
  userId: string
): BaseCollector[] {
  const sources: SourceSystem[] = ['slack', 'linear', 'drive', 'local', 'claude'];
  const collectors: BaseCollector[] = [];

  for (const source of sources) {
    const collector = createCollector(source, config, dateRange, userId);
    if (collector && collector.isConfigured()) {
      collectors.push(collector);
    }
  }

  return collectors;
}

export async function runAllCollectors(
  config: Config,
  dateRange: DateRange,
  userId: string
): Promise<Map<SourceSystem, CollectorResult>> {
  const results = new Map<SourceSystem, CollectorResult>();
  const collectors = getAllCollectors(config, dateRange, userId);

  console.log(`Running ${collectors.length} collectors...`);

  for (const collector of collectors) {
    console.log(`\nCollecting from ${collector.source}...`);
    const result = await collector.collect();
    results.set(collector.source, result);

    if (result.errors.length > 0) {
      console.error(`  Errors: ${result.errors.join(', ')}`);
    }
    if (result.warnings.length > 0) {
      console.warn(`  Warnings: ${result.warnings.join(', ')}`);
    }
    console.log(`  Collected ${result.recordCount} events`);
  }

  return results;
}
