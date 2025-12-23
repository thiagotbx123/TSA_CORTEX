/**
 * SpineHub - Layer 3.5: Content Consolidation Hub
 *
 * Reads raw content from all sources and consolidates into a navigable structure
 * This is the missing layer between collection and narrative generation
 */

import * as fs from 'fs';
import * as path from 'path';
import { getOutputPaths } from '../utils/config';

// Types for consolidated content
export interface SlackMessage {
  timestamp: string;
  channel: string;
  channelName: string;
  user: string;
  userName: string;
  text: string;
  permalink: string;
  isOwner: boolean;
  threadTs?: string;
}

export interface DriveFile {
  id: string;
  name: string;
  mimeType: string;
  modifiedTime: string;
  webViewLink: string;
  owners: string[];
  content?: string; // If we can read it
}

export interface LocalFile {
  path: string;
  name: string;
  extension: string;
  modifiedAt: string;
  content?: string; // If we can read it
  sizeBytes: number;
}

export interface ClaudeInteraction {
  timestamp: string;
  project: string;
  type: 'prompt' | 'response';
  text: string;
}

export interface LinearIssue {
  id: string;
  identifier: string;
  title: string;
  description: string;
  state: string;
  url: string;
  comments: Array<{ body: string; createdAt: string; user: string }>;
}

export interface SpineHubData {
  metadata: {
    generatedAt: string;
    period: { start: string; end: string };
    ownerId: string;
    ownerName: string;
    filters: FiltersSummary;
  };
  slack: {
    ownerMessages: SlackMessage[];
    contextMessages: SlackMessage[];
    channelsSummary: Map<string, { count: number; topics: string[] }>;
  };
  drive: {
    files: DriveFile[];
    byType: Map<string, DriveFile[]>;
  };
  local: {
    files: LocalFile[];
    readable: LocalFile[]; // Files we can read content from
  };
  claude: {
    interactions: ClaudeInteraction[];
    byProject: Map<string, ClaudeInteraction[]>;
  };
  linear: {
    issues: LinearIssue[];
  };
  // The consolidated narrative content
  narrativeBlocks: NarrativeBlock[];
}

export interface NarrativeBlock {
  theme: string;
  context: string;
  events: Array<{
    date: string;
    time: string;
    description: string; // Natural language, not "Worked on: file.xlsx"
    sources: string[];
  }>;
  outcome?: string;
}

export interface FiltersSummary {
  dateRange: string;
  slackChannels: string[];
  slackUserFilter: string;
  driveOwnerFilter: string;
  localPaths: string[];
  excludedPatterns: string[];
}

/**
 * Build the SpineHub from raw exports
 */
export async function buildSpineHub(
  rawExportsPath: string,
  ownerId: string,
  ownerName: string,
  startDate: Date,
  endDate: Date
): Promise<SpineHubData> {
  console.log('\n🧠 Building SpineHub (Content Consolidation)...\n');

  const hub: SpineHubData = {
    metadata: {
      generatedAt: new Date().toISOString(),
      period: { start: startDate.toISOString(), end: endDate.toISOString() },
      ownerId,
      ownerName,
      filters: {
        dateRange: `${startDate.toISOString().split('T')[0]} to ${endDate.toISOString().split('T')[0]}`,
        slackChannels: [],
        slackUserFilter: `user_id == ${ownerId}`,
        driveOwnerFilter: `owner == ${ownerName}`,
        localPaths: ['~/Downloads', '~/Documents'],
        excludedPatterns: ['*.env', 'client_secret*.json', 'credentials*.json', '~$*'],
      },
    },
    slack: {
      ownerMessages: [],
      contextMessages: [],
      channelsSummary: new Map(),
    },
    drive: {
      files: [],
      byType: new Map(),
    },
    local: {
      files: [],
      readable: [],
    },
    claude: {
      interactions: [],
      byProject: new Map(),
    },
    linear: {
      issues: [],
    },
    narrativeBlocks: [],
  };

  // Load and process each source
  await processSlack(hub, rawExportsPath, ownerId);
  await processDrive(hub, rawExportsPath, ownerName);
  await processLocal(hub, rawExportsPath);
  await processClaude(hub, rawExportsPath);
  await processLinear(hub, rawExportsPath);

  // Generate narrative blocks from consolidated content
  generateNarrativeBlocks(hub);

  console.log('\n✅ SpineHub built successfully');
  console.log(`   Owner messages: ${hub.slack.ownerMessages.length}`);
  console.log(`   Context messages: ${hub.slack.contextMessages.length}`);
  console.log(`   Drive files: ${hub.drive.files.length}`);
  console.log(`   Local files: ${hub.local.files.length}`);
  console.log(`   Claude interactions: ${hub.claude.interactions.length}`);
  console.log(`   Linear issues: ${hub.linear.issues.length}`);
  console.log(`   Narrative blocks: ${hub.narrativeBlocks.length}`);

  return hub;
}

async function processSlack(hub: SpineHubData, rawPath: string, ownerId: string): Promise<void> {
  const filePath = path.join(rawPath, 'raw_events_slack.json');
  if (!fs.existsSync(filePath)) return;

  const rawData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  const channels = new Set<string>();

  for (const msg of rawData) {
    channels.add(msg.channel_name);

    const slackMsg: SlackMessage = {
      timestamp: msg.ts,
      channel: msg.channel,
      channelName: msg.channel_name,
      user: msg.user,
      userName: msg.user_name,
      text: msg.text || '',
      permalink: msg.permalink,
      isOwner: msg.user === ownerId,
      threadTs: msg.thread_ts,
    };

    if (slackMsg.isOwner) {
      hub.slack.ownerMessages.push(slackMsg);
    } else {
      hub.slack.contextMessages.push(slackMsg);
    }

    // Update channel summary
    if (!hub.slack.channelsSummary.has(msg.channel_name)) {
      hub.slack.channelsSummary.set(msg.channel_name, { count: 0, topics: [] });
    }
    hub.slack.channelsSummary.get(msg.channel_name)!.count++;
  }

  hub.metadata.filters.slackChannels = Array.from(channels);
  console.log(`   [Slack] ${hub.slack.ownerMessages.length} owner messages, ${hub.slack.contextMessages.length} context`);
}

async function processDrive(hub: SpineHubData, rawPath: string, ownerName: string): Promise<void> {
  const filePath = path.join(rawPath, 'raw_events_drive.json');
  if (!fs.existsSync(filePath)) return;

  const rawData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

  for (const file of rawData) {
    const driveFile: DriveFile = {
      id: file.id,
      name: file.name,
      mimeType: file.mimeType,
      modifiedTime: file.modifiedTime,
      webViewLink: file.webViewLink,
      owners: file.owners?.map((o: any) => o.displayName || o.emailAddress) || [],
    };

    hub.drive.files.push(driveFile);

    // Group by type
    const ext = path.extname(file.name).toLowerCase() || 'no-extension';
    if (!hub.drive.byType.has(ext)) {
      hub.drive.byType.set(ext, []);
    }
    hub.drive.byType.get(ext)!.push(driveFile);
  }

  console.log(`   [Drive] ${hub.drive.files.length} files`);
}

async function processLocal(hub: SpineHubData, rawPath: string): Promise<void> {
  const filePath = path.join(rawPath, 'raw_events_local.json');
  if (!fs.existsSync(filePath)) return;

  const rawData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  const readableExtensions = ['.txt', '.md', '.json', '.csv', '.log'];

  for (const file of rawData) {
    const localFile: LocalFile = {
      path: file.path,
      name: file.name,
      extension: file.extension,
      modifiedAt: file.modified_at,
      sizeBytes: file.size_bytes || 0,
    };

    // Try to read content for readable files
    if (readableExtensions.includes(file.extension?.toLowerCase()) && file.size_bytes < 100000) {
      try {
        if (fs.existsSync(file.path)) {
          localFile.content = fs.readFileSync(file.path, 'utf-8').slice(0, 5000);
          hub.local.readable.push(localFile);
        }
      } catch {
        // Can't read, skip
      }
    }

    hub.local.files.push(localFile);
  }

  console.log(`   [Local] ${hub.local.files.length} files (${hub.local.readable.length} readable)`);
}

async function processClaude(hub: SpineHubData, rawPath: string): Promise<void> {
  const filePath = path.join(rawPath, 'raw_events_claude.json');
  if (!fs.existsSync(filePath)) return;

  const rawData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

  for (const item of rawData) {
    const interaction: ClaudeInteraction = {
      timestamp: item.timestamp || new Date().toISOString(),
      project: item.project || 'unknown',
      type: item.type?.includes('prompt') ? 'prompt' : 'response',
      text: item.text || item.content || '',
    };

    hub.claude.interactions.push(interaction);

    // Group by project
    if (!hub.claude.byProject.has(interaction.project)) {
      hub.claude.byProject.set(interaction.project, []);
    }
    hub.claude.byProject.get(interaction.project)!.push(interaction);
  }

  console.log(`   [Claude] ${hub.claude.interactions.length} interactions`);
}

async function processLinear(hub: SpineHubData, rawPath: string): Promise<void> {
  const filePath = path.join(rawPath, 'raw_events_linear.json');
  if (!fs.existsSync(filePath)) return;

  const rawData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

  for (const issue of rawData) {
    const linearIssue: LinearIssue = {
      id: issue.id,
      identifier: issue.identifier,
      title: issue.title,
      description: issue.description || '',
      state: issue.state?.name || 'unknown',
      url: issue.url,
      comments: (issue.comments?.nodes || []).map((c: any) => ({
        body: c.body,
        createdAt: c.createdAt,
        user: c.user?.name || 'unknown',
      })),
    };

    hub.linear.issues.push(linearIssue);
  }

  console.log(`   [Linear] ${hub.linear.issues.length} issues`);
}

/**
 * Generate narrative blocks from consolidated content
 * This is where we turn raw data into STORIES
 */
function generateNarrativeBlocks(hub: SpineHubData): void {
  // Group owner messages by channel/theme
  const messagesByChannel = new Map<string, SlackMessage[]>();

  for (const msg of hub.slack.ownerMessages) {
    if (!messagesByChannel.has(msg.channelName)) {
      messagesByChannel.set(msg.channelName, []);
    }
    messagesByChannel.get(msg.channelName)!.push(msg);
  }

  // Create narrative block for each significant channel
  for (const [channel, messages] of messagesByChannel) {
    if (messages.length < 2) continue; // Skip channels with minimal activity

    // Analyze message content to determine theme
    const theme = inferTheme(channel, messages);
    const context = generateContext(channel, messages);

    // Convert messages to narrative events
    const events = messages.slice(0, 10).map(msg => {
      const date = new Date(parseFloat(msg.timestamp) * 1000);
      return {
        date: date.toISOString().split('T')[0],
        time: date.toTimeString().split(' ')[0].slice(0, 5),
        description: cleanMessageForNarrative(msg.text),
        sources: [msg.permalink],
      };
    });

    hub.narrativeBlocks.push({
      theme,
      context,
      events,
      outcome: inferOutcome(messages),
    });
  }

  // Add blocks for Claude projects with significant activity
  for (const [project, interactions] of hub.claude.byProject) {
    if (interactions.length < 3) continue;

    const prompts = interactions.filter(i => i.type === 'prompt');
    hub.narrativeBlocks.push({
      theme: `Development: ${project}`,
      context: `Technical work using Claude Code on ${project} project`,
      events: prompts.slice(0, 5).map(p => ({
        date: p.timestamp.split('T')[0],
        time: p.timestamp.split('T')[1]?.slice(0, 5) || '00:00',
        description: summarizePrompt(p.text),
        sources: [`claude:${project}`],
      })),
      outcome: `Completed ${prompts.length} development tasks`,
    });
  }

  // Add blocks for Linear issues
  for (const issue of hub.linear.issues) {
    hub.narrativeBlocks.push({
      theme: `Issue: ${issue.identifier}`,
      context: issue.title,
      events: [{
        date: new Date().toISOString().split('T')[0],
        time: '00:00',
        description: issue.description?.slice(0, 200) || issue.title,
        sources: [issue.url],
      }],
      outcome: `Status: ${issue.state}`,
    });
  }
}

function inferTheme(channel: string, messages: SlackMessage[]): string {
  // Map channel names to themes
  const themeMap: Record<string, string> = {
    'intuit-internal': 'Intuit WFS Project',
    'testbox-intuit-wfs-external': 'Intuit WFS External',
    'dev-on-call': 'Engineering Support',
    'tsa-data-engineers': 'TSA Team Coordination',
    'team-koala': 'Koala Team',
    'brevo-internal': 'Brevo Integration',
    'archer-internal': 'Archer Project',
    'product': 'Product Discussions',
  };

  for (const [key, theme] of Object.entries(themeMap)) {
    if (channel.toLowerCase().includes(key)) {
      return theme;
    }
  }

  return `Channel: #${channel}`;
}

function generateContext(channel: string, messages: SlackMessage[]): string {
  // Analyze first few messages to understand context
  const sampleText = messages.slice(0, 5).map(m => m.text).join(' ');

  if (sampleText.includes('release') || sampleText.includes('deploy')) {
    return 'Release and deployment coordination';
  }
  if (sampleText.includes('bug') || sampleText.includes('fix') || sampleText.includes('issue')) {
    return 'Bug investigation and resolution';
  }
  if (sampleText.includes('meeting') || sampleText.includes('sync') || sampleText.includes('call')) {
    return 'Team alignment and meeting coordination';
  }
  if (sampleText.includes('document') || sampleText.includes('spec') || sampleText.includes('doc')) {
    return 'Documentation and specification work';
  }

  return `Coordination in #${channel}`;
}

function cleanMessageForNarrative(text: string): string {
  // Remove Slack formatting, mentions, and clean up
  let clean = text
    .replace(/<@[A-Z0-9]+\|?[^>]*>/g, '') // Remove mentions
    .replace(/<#[A-Z0-9]+\|?([^>]*)>/g, '#$1') // Clean channel refs
    .replace(/<([^|>]+)\|([^>]+)>/g, '$2') // Clean links
    .replace(/<([^>]+)>/g, '$1') // Clean remaining brackets
    .replace(/:[a-z_]+:/g, '') // Remove emoji codes
    .replace(/\n+/g, ' ')
    .trim();

  // Truncate if too long
  if (clean.length > 150) {
    clean = clean.slice(0, 147) + '...';
  }

  return clean || 'Activity recorded';
}

function summarizePrompt(text: string): string {
  // Get first meaningful line
  const lines = text.split('\n').filter(l => l.trim().length > 10);
  const first = lines[0] || text;

  if (first.length > 100) {
    return first.slice(0, 97) + '...';
  }
  return first;
}

function inferOutcome(messages: SlackMessage[]): string {
  const lastMessages = messages.slice(-3);
  const text = lastMessages.map(m => m.text.toLowerCase()).join(' ');

  if (text.includes('done') || text.includes('complete') || text.includes('finished')) {
    return 'Task completed successfully';
  }
  if (text.includes('blocked') || text.includes('waiting') || text.includes('pending')) {
    return 'Awaiting external dependency';
  }
  if (text.includes('thanks') || text.includes('great') || text.includes('perfect')) {
    return 'Positive resolution';
  }

  return 'Ongoing coordination';
}

/**
 * Export the SpineHub to a file for inspection
 */
export function saveSpineHub(hub: SpineHubData, outputPath: string): void {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const filePath = path.join(outputPath, `spinehub_${timestamp}.json`);

  // Convert Maps to objects for JSON serialization
  const serializable = {
    ...hub,
    slack: {
      ...hub.slack,
      channelsSummary: Object.fromEntries(hub.slack.channelsSummary),
    },
    drive: {
      ...hub.drive,
      byType: Object.fromEntries(hub.drive.byType),
    },
    claude: {
      ...hub.claude,
      byProject: Object.fromEntries(hub.claude.byProject),
    },
  };

  fs.writeFileSync(filePath, JSON.stringify(serializable, null, 2));
  console.log(`   Saved SpineHub to: ${filePath}`);
}
