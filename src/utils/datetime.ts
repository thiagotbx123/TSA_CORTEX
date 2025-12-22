/**
 * Date/time utilities with timezone support
 */

import { format, subDays, parseISO, isWithinInterval, startOfDay, endOfDay } from 'date-fns';
import { utcToZonedTime, zonedTimeToUtc, formatInTimeZone } from 'date-fns-tz';

export interface DateRange {
  start: Date;
  end: Date;
  timezone: string;
}

export function getDefaultDateRange(timezone: string, days: number = 7): DateRange {
  const now = new Date();
  const end = now;
  const start = subDays(now, days);

  return {
    start: startOfDay(utcToZonedTime(start, timezone)),
    end: endOfDay(utcToZonedTime(end, timezone)),
    timezone,
  };
}

export function parseDateRange(
  startStr: string | undefined,
  endStr: string | undefined,
  timezone: string,
  defaultDays: number = 7
): DateRange {
  const now = new Date();

  let end: Date;
  let start: Date;

  if (endStr) {
    end = parseISO(endStr);
    end = endOfDay(utcToZonedTime(end, timezone));
  } else {
    end = endOfDay(utcToZonedTime(now, timezone));
  }

  if (startStr) {
    start = parseISO(startStr);
    start = startOfDay(utcToZonedTime(start, timezone));
  } else {
    start = startOfDay(subDays(end, defaultDays));
  }

  return { start, end, timezone };
}

export function isWithinDateRange(dateStr: string, range: DateRange): boolean {
  const date = parseISO(dateStr);
  return isWithinInterval(date, { start: range.start, end: range.end });
}

export function formatLocalTime(date: Date | string, timezone: string): string {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return formatInTimeZone(d, timezone, "yyyy-MM-dd'T'HH:mm:ssXXX");
}

export function formatUTC(date: Date | string): string {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return d.toISOString();
}

export function formatDisplay(date: Date | string, timezone: string): string {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return formatInTimeZone(d, timezone, 'yyyy-MM-dd HH:mm');
}

export function toUnixTimestamp(date: Date): number {
  return Math.floor(date.getTime() / 1000);
}

export function fromUnixTimestamp(ts: number): Date {
  return new Date(ts * 1000);
}

export function slackTsToDate(ts: string): Date {
  const unixTs = parseFloat(ts);
  return fromUnixTimestamp(unixTs);
}

export function dateToSlackTs(date: Date): string {
  return (date.getTime() / 1000).toFixed(6);
}
