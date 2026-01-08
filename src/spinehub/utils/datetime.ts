/**
 * DateTime Utils - TypeScript wrapper for timezone-aware date handling
 *
 * Provides utilities for:
 * - Date range calculations
 * - Timezone conversions (Brazil-focused)
 * - Slack timestamp handling
 */

import { getPythonBridge, BridgeResponse } from '../bridge';
import { DateRange, DateTimeInfo } from '../types';

// Re-export types
export { DateRange, DateTimeInfo };

export const DEFAULT_TIMEZONE = 'America/Sao_Paulo';
export const DEFAULT_RANGE_DAYS = 7;

/**
 * Get default date range (last N days)
 */
export async function getDefaultDateRange(
  timezone: string = DEFAULT_TIMEZONE,
  days: number = DEFAULT_RANGE_DAYS
): Promise<DateRange> {
  const bridge = getPythonBridge();
  const response = await bridge.call<DateRange>('datetime.get_default_range', {
    timezone,
    days,
  });

  if (!response.success) {
    return getDefaultDateRangeLocal(timezone, days);
  }

  return response.data!;
}

/**
 * Parse date range from strings
 */
export async function parseDateRange(
  startStr?: string,
  endStr?: string,
  timezone: string = DEFAULT_TIMEZONE,
  defaultDays: number = DEFAULT_RANGE_DAYS
): Promise<DateRange> {
  const bridge = getPythonBridge();
  const response = await bridge.call<DateRange>('datetime.parse_range', {
    start_str: startStr,
    end_str: endStr,
    timezone,
    default_days: defaultDays,
  });

  if (!response.success) {
    return parseDateRangeLocal(startStr, endStr, defaultDays);
  }

  return response.data!;
}

/**
 * Get current time in Brazil timezone
 */
export async function nowBrasil(): Promise<Date> {
  const bridge = getPythonBridge();
  const response = await bridge.call<{ datetime: string }>('datetime.now_brasil', {});

  if (!response.success) {
    return new Date();
  }

  return new Date(response.data!.datetime);
}

/**
 * Format date for display (YYYY-MM-DD HH:MM)
 */
export async function formatDisplay(
  date: Date | string,
  timezone: string = DEFAULT_TIMEZONE
): Promise<string> {
  const bridge = getPythonBridge();
  const dateStr = typeof date === 'string' ? date : date.toISOString();

  const response = await bridge.call<{ formatted: string }>('datetime.format_display', {
    date: dateStr,
    timezone,
  });

  if (!response.success) {
    return formatDisplayLocal(date);
  }

  return response.data!.formatted;
}

/**
 * Format date to local time with timezone offset
 */
export async function formatLocalTime(
  date: Date | string,
  timezone: string = DEFAULT_TIMEZONE
): Promise<string> {
  const bridge = getPythonBridge();
  const dateStr = typeof date === 'string' ? date : date.toISOString();

  const response = await bridge.call<{ formatted: string }>('datetime.format_local', {
    date: dateStr,
    timezone,
  });

  if (!response.success) {
    return new Date(dateStr).toISOString();
  }

  return response.data!.formatted;
}

/**
 * Convert Slack timestamp to Date
 */
export function slackTsToDate(ts: string): Date {
  const unixTs = parseFloat(ts);
  return new Date(unixTs * 1000);
}

/**
 * Convert Date to Slack timestamp format
 */
export function dateToSlackTs(date: Date): string {
  return (date.getTime() / 1000).toFixed(6);
}

/**
 * Check if date is within a date range
 */
export function isWithinDateRange(date: Date | string, range: DateRange): boolean {
  const checkDate = typeof date === 'string' ? new Date(date) : date;
  const start = new Date(range.start);
  const end = new Date(range.end);

  return checkDate >= start && checkDate <= end;
}

/**
 * Get relative time description (e.g., "2 days ago")
 */
export function getRelativeTime(date: Date | string): string {
  const now = new Date();
  const then = typeof date === 'string' ? new Date(date) : date;
  const diffMs = now.getTime() - then.getTime();

  const diffSecs = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffSecs / 60);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffDays > 0) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
  if (diffHours > 0) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
  if (diffMins > 0) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
  return 'just now';
}

// ============================================
// Local Fallback Implementations
// ============================================

function getDefaultDateRangeLocal(timezone: string, days: number): DateRange {
  const now = new Date();
  const end = new Date(now);
  end.setHours(23, 59, 59, 999);

  const start = new Date(now);
  start.setDate(start.getDate() - days);
  start.setHours(0, 0, 0, 0);

  return {
    start: start.toISOString(),
    end: end.toISOString(),
    timezone,
  };
}

function parseDateRangeLocal(
  startStr?: string,
  endStr?: string,
  defaultDays: number = 7
): DateRange {
  const now = new Date();
  const timezone = DEFAULT_TIMEZONE;

  let end: Date;
  if (endStr) {
    end = new Date(endStr);
    end.setHours(23, 59, 59, 999);
  } else {
    end = new Date(now);
    end.setHours(23, 59, 59, 999);
  }

  let start: Date;
  if (startStr) {
    start = new Date(startStr);
    start.setHours(0, 0, 0, 0);
  } else {
    start = new Date(end);
    start.setDate(start.getDate() - defaultDays);
    start.setHours(0, 0, 0, 0);
  }

  return {
    start: start.toISOString(),
    end: end.toISOString(),
    timezone,
  };
}

function formatDisplayLocal(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  const year = d.getFullYear();
  const month = (d.getMonth() + 1).toString().padStart(2, '0');
  const day = d.getDate().toString().padStart(2, '0');
  const hours = d.getHours().toString().padStart(2, '0');
  const mins = d.getMinutes().toString().padStart(2, '0');

  return `${year}-${month}-${day} ${hours}:${mins}`;
}
