/**
 * Base collector interface and abstract class
 */

import { ActivityEvent, SourceSystem, Config } from '../types';
import { DateRange } from '../utils/datetime';

export interface CollectorResult {
  source: SourceSystem;
  events: ActivityEvent[];
  rawData: unknown[];
  errors: string[];
  warnings: string[];
  recordCount: number;
}

export abstract class BaseCollector {
  protected config: Config;
  protected dateRange: DateRange;
  protected userId: string;

  constructor(config: Config, dateRange: DateRange, userId: string) {
    this.config = config;
    this.dateRange = dateRange;
    this.userId = userId;
  }

  abstract get source(): SourceSystem;
  abstract isConfigured(): boolean;
  abstract collect(): Promise<CollectorResult>;

  protected createEmptyResult(): CollectorResult {
    return {
      source: this.source,
      events: [],
      rawData: [],
      errors: [],
      warnings: [],
      recordCount: 0,
    };
  }

  protected logInfo(message: string): void {
    console.log(`[${this.source.toUpperCase()}] ${message}`);
  }

  protected logWarn(message: string): void {
    console.warn(`[${this.source.toUpperCase()}] WARNING: ${message}`);
  }

  protected logError(message: string): void {
    console.error(`[${this.source.toUpperCase()}] ERROR: ${message}`);
  }
}
