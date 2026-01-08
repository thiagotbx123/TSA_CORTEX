/**
 * SpineHub Utils Module
 */

// Privacy
export {
  redactPII,
  maskEmail,
  maskPhone,
  truncateText,
  sanitizeForLog,
  DEFAULT_REDACTION_CONFIG,
  RedactionConfig,
  RedactionResult,
} from './privacy';

// DateTime
export {
  getDefaultDateRange,
  parseDateRange,
  nowBrasil,
  formatDisplay,
  formatLocalTime,
  slackTsToDate,
  dateToSlackTs,
  isWithinDateRange,
  getRelativeTime,
  DEFAULT_TIMEZONE,
  DEFAULT_RANGE_DAYS,
  DateRange,
  DateTimeInfo,
} from './datetime';

// Slack Channels
export {
  getChannelTheme,
  getChannelCategory,
  getChannelMapping,
  groupChannelsByCategory,
  inferThemeFromContent,
  isCustomerChannel,
  isInternalChannel,
  getChannelPriority,
  sortChannelsByPriority,
  CHANNEL_THEME_MAP,
  ChannelMapping,
} from './slack-channels';
