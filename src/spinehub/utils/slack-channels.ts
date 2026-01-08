/**
 * Slack Channel Utils - Channel to theme mapping
 *
 * Provides utilities for:
 * - Mapping Slack channels to worklog themes
 * - Channel categorization
 * - Theme inference from channel activity
 */

import { ChannelMapping } from '../types';

// Re-export types
export { ChannelMapping };

/**
 * Known channel mappings for TSA projects
 */
export const CHANNEL_THEME_MAP: Record<string, { theme: string; category: string }> = {
  // Customer Projects
  'intuit-internal': { theme: 'Intuit WFS Project', category: 'customer' },
  'testbox-intuit-wfs-external': { theme: 'WFS External Coordination', category: 'customer' },
  'testbox-intuit-mailchimp-external': { theme: 'Mailchimp Integration', category: 'customer' },
  'external-testbox-apollo': { theme: 'Apollo Project', category: 'customer' },
  'brevo-internal': { theme: 'Brevo Integration', category: 'customer' },
  'archer-internal': { theme: 'Archer Project', category: 'customer' },

  // Team Channels
  'tsa-data-engineers': { theme: 'TSA Team Sync', category: 'team' },
  'team-koala': { theme: 'Koala Team', category: 'team' },
  'dev-on-call': { theme: 'Engineering Support', category: 'ops' },

  // Company Channels
  'product': { theme: 'Product Discussions', category: 'internal' },
  'go-to-market': { theme: 'GTM Strategy', category: 'internal' },
  'engineering': { theme: 'Engineering', category: 'internal' },
  'general': { theme: 'General', category: 'internal' },
};

/**
 * Get theme for a channel
 */
export function getChannelTheme(channelName: string): string {
  // Direct match
  if (CHANNEL_THEME_MAP[channelName]) {
    return CHANNEL_THEME_MAP[channelName].theme;
  }

  // Partial match
  const lowerChannel = channelName.toLowerCase();
  for (const [pattern, mapping] of Object.entries(CHANNEL_THEME_MAP)) {
    if (lowerChannel.includes(pattern.toLowerCase())) {
      return mapping.theme;
    }
  }

  // Default to channel name
  return `Channel: #${channelName}`;
}

/**
 * Get category for a channel
 */
export function getChannelCategory(channelName: string): string {
  // Direct match
  if (CHANNEL_THEME_MAP[channelName]) {
    return CHANNEL_THEME_MAP[channelName].category;
  }

  // Partial match
  const lowerChannel = channelName.toLowerCase();
  for (const [pattern, mapping] of Object.entries(CHANNEL_THEME_MAP)) {
    if (lowerChannel.includes(pattern.toLowerCase())) {
      return mapping.category;
    }
  }

  // Infer category from name patterns
  if (lowerChannel.includes('external') || lowerChannel.includes('client')) {
    return 'customer';
  }
  if (lowerChannel.includes('team') || lowerChannel.includes('squad')) {
    return 'team';
  }
  if (lowerChannel.includes('oncall') || lowerChannel.includes('ops') || lowerChannel.includes('incident')) {
    return 'ops';
  }

  return 'internal';
}

/**
 * Get full channel mapping
 */
export function getChannelMapping(channelId: string, channelName: string): ChannelMapping {
  return {
    channel_id: channelId,
    channel_name: channelName,
    theme: getChannelTheme(channelName),
    category: getChannelCategory(channelName),
  };
}

/**
 * Group channels by category
 */
export function groupChannelsByCategory(
  channels: Array<{ id: string; name: string }>
): Record<string, ChannelMapping[]> {
  const grouped: Record<string, ChannelMapping[]> = {
    customer: [],
    team: [],
    ops: [],
    internal: [],
  };

  for (const channel of channels) {
    const mapping = getChannelMapping(channel.id, channel.name);
    if (!grouped[mapping.category]) {
      grouped[mapping.category] = [];
    }
    grouped[mapping.category].push(mapping);
  }

  return grouped;
}

/**
 * Infer theme from channel content
 */
export function inferThemeFromContent(channelName: string, sampleMessages: string[]): string {
  const combinedText = sampleMessages.join(' ').toLowerCase();

  // Check for specific keywords
  if (combinedText.includes('release') || combinedText.includes('deploy')) {
    return `${getChannelTheme(channelName)} - Release`;
  }
  if (combinedText.includes('bug') || combinedText.includes('fix') || combinedText.includes('issue')) {
    return `${getChannelTheme(channelName)} - Bug Investigation`;
  }
  if (combinedText.includes('meeting') || combinedText.includes('sync') || combinedText.includes('call')) {
    return `${getChannelTheme(channelName)} - Coordination`;
  }
  if (combinedText.includes('document') || combinedText.includes('spec') || combinedText.includes('doc')) {
    return `${getChannelTheme(channelName)} - Documentation`;
  }
  if (combinedText.includes('review') || combinedText.includes('pr') || combinedText.includes('merge')) {
    return `${getChannelTheme(channelName)} - Code Review`;
  }

  return getChannelTheme(channelName);
}

/**
 * Check if channel is customer-facing
 */
export function isCustomerChannel(channelName: string): boolean {
  return getChannelCategory(channelName) === 'customer';
}

/**
 * Check if channel is internal
 */
export function isInternalChannel(channelName: string): boolean {
  return getChannelCategory(channelName) === 'internal';
}

/**
 * Get priority of channel for worklog ordering
 */
export function getChannelPriority(channelName: string): number {
  const category = getChannelCategory(channelName);

  // Priority: customer > ops > team > internal
  const priorities: Record<string, number> = {
    customer: 1,
    ops: 2,
    team: 3,
    internal: 4,
  };

  return priorities[category] || 5;
}

/**
 * Sort channels by worklog priority
 */
export function sortChannelsByPriority(channels: string[]): string[] {
  return [...channels].sort((a, b) => {
    return getChannelPriority(a) - getChannelPriority(b);
  });
}
