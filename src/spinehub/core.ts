/**
 * SpineHub Core - The Central Knowledge Graph
 *
 * SpineHub is the BACKBONE of TSA_CORTEX, not just a layer.
 * It provides:
 * - Persistent storage of all entities, relations, and artifacts
 * - Cross-execution memory and learning
 * - Automatic pattern recognition
 * - Single source of truth for all data
 *
 * Design Principle: RAC-14 quality output is the benchmark.
 * The SpineHub must enable, not hinder, narrative generation.
 */

import * as fs from 'fs';
import * as path from 'path';
import { Entity, EntityType, Relation, RelationType, Pattern, Artifact } from './entities';
import { SpineHubStorage } from './storage';

export interface SpineHubConfig {
  storagePath: string;
  ownerName: string;
  ownerId: string;
}

export interface IngestResult {
  entitiesCreated: number;
  entitiesUpdated: number;
  relationsCreated: number;
  artifactsIndexed: number;
  patternsIdentified: number;
}

export interface QueryContext {
  startDate: Date;
  endDate: Date;
  sources?: string[];
  themes?: string[];
}

export interface NarrativeContext {
  // Period info
  period: { start: Date; end: Date };
  owner: { id: string; name: string };

  // Counts for summary table
  counts: {
    slack: number;
    linear: number;
    drive: number;
    local: number;
    claude: number;
    total: number;
  };

  // Entities involved in this period
  people: Entity[];
  projects: Entity[];
  channels: Entity[];

  // Relations active in this period
  collaborations: Array<{
    person: string;
    context: string;
    strength: number;
  }>;

  // Themes inferred from data
  themes: Array<{
    name: string;
    description: string;
    artifacts: Artifact[];
    relatedPeople: string[];
    eventCount: number;
  }>;

  // All artifacts with resolved links
  artifacts: Artifact[];

  // Raw data for deep analysis (Claude reads this)
  rawSlack: any[];
  rawDrive: any[];
  rawLinear: any[];
  rawLocal: any[];
  rawClaude: any[];
}

/**
 * SpineHub - The Central Nervous System of CORTEX
 */
export class SpineHub {
  private storage: SpineHubStorage;
  private config: SpineHubConfig;
  private initialized: boolean = false;

  constructor(config: SpineHubConfig) {
    this.config = config;
    this.storage = new SpineHubStorage(config.storagePath);
  }

  /**
   * Initialize SpineHub - loads existing data or creates new store
   */
  async initialize(): Promise<void> {
    if (this.initialized) return;

    await this.storage.load();
    this.initialized = true;

    console.log('🧠 SpineHub initialized');
    console.log(`   Entities: ${this.storage.getEntityCount()}`);
    console.log(`   Relations: ${this.storage.getRelationCount()}`);
    console.log(`   Artifacts: ${this.storage.getArtifactCount()}`);
    console.log(`   Patterns: ${this.storage.getPatternCount()}`);
  }

  /**
   * Ingest data from a collector
   * This is called after each collector runs
   */
  async ingest(source: string, data: any[]): Promise<IngestResult> {
    const result: IngestResult = {
      entitiesCreated: 0,
      entitiesUpdated: 0,
      relationsCreated: 0,
      artifactsIndexed: 0,
      patternsIdentified: 0,
    };

    switch (source) {
      case 'slack':
        await this.ingestSlack(data, result);
        break;
      case 'drive':
        await this.ingestDrive(data, result);
        break;
      case 'linear':
        await this.ingestLinear(data, result);
        break;
      case 'local':
        await this.ingestLocal(data, result);
        break;
      case 'claude':
        await this.ingestClaude(data, result);
        break;
    }

    // Identify patterns after ingestion
    result.patternsIdentified = await this.identifyPatterns();

    // Save after ingestion
    await this.storage.save();

    return result;
  }

  /**
   * Query SpineHub for narrative context
   * This is what Claude reads to generate the worklog
   */
  async queryForNarrative(context: QueryContext): Promise<NarrativeContext> {
    const { startDate, endDate } = context;

    // Load raw data files
    const rawPath = path.join(path.dirname(this.config.storagePath), '..', 'raw_exports');

    const rawSlack = this.loadJsonSafe(path.join(rawPath, 'raw_events_slack.json'));
    const rawDrive = this.loadJsonSafe(path.join(rawPath, 'raw_events_drive.json'));
    const rawLinear = this.loadJsonSafe(path.join(rawPath, 'raw_events_linear.json'));
    const rawLocal = this.loadJsonSafe(path.join(rawPath, 'raw_events_local.json'));
    const rawClaude = this.loadJsonSafe(path.join(rawPath, 'raw_events_claude.json'));

    // Get entities active in period
    const people = this.storage.getEntitiesByType('person')
      .filter(e => this.wasActiveInPeriod(e, startDate, endDate));

    const projects = this.storage.getEntitiesByType('project');
    const channels = this.storage.getEntitiesByType('channel');

    // Calculate collaborations
    const collaborations = this.calculateCollaborations(rawSlack);

    // Infer themes from data
    const themes = this.inferThemes(rawSlack, rawDrive, rawLinear, rawClaude);

    // Get all artifacts with resolved links
    const artifacts = this.storage.getAllArtifacts();

    return {
      period: { start: startDate, end: endDate },
      owner: { id: this.config.ownerId, name: this.config.ownerName },
      counts: {
        slack: rawSlack.length,
        linear: rawLinear.length,
        drive: rawDrive.length,
        local: rawLocal.length,
        claude: rawClaude.length,
        total: rawSlack.length + rawLinear.length + rawDrive.length + rawLocal.length + rawClaude.length,
      },
      people,
      projects,
      channels,
      collaborations,
      themes,
      artifacts,
      rawSlack,
      rawDrive,
      rawLinear,
      rawLocal,
      rawClaude,
    };
  }

  /**
   * Resolve an artifact by name, returning its full details including URL
   */
  resolveArtifact(name: string): Artifact | null {
    return this.storage.findArtifactByName(name);
  }

  /**
   * Get all artifacts matching a pattern
   */
  findArtifacts(pattern: string): Artifact[] {
    return this.storage.findArtifactsByPattern(pattern);
  }

  // ============================================
  // PRIVATE: Ingestion Methods
  // ============================================

  private async ingestSlack(data: any[], result: IngestResult): Promise<void> {
    const seenUsers = new Map<string, Entity>();
    const seenChannels = new Map<string, Entity>();

    for (const msg of data) {
      // Create/update user entity
      if (msg.user_name && !seenUsers.has(msg.user)) {
        const entity = this.storage.upsertEntity({
          id: `slack_user_${msg.user}`,
          type: 'person',
          name: msg.user_name,
          aliases: [msg.user],
          firstSeen: new Date(),
          lastSeen: new Date(),
          occurrenceCount: 1,
          metadata: { slackId: msg.user },
        });
        seenUsers.set(msg.user, entity);
        if (entity.occurrenceCount === 1) result.entitiesCreated++;
        else result.entitiesUpdated++;
      }

      // Create/update channel entity
      if (msg.channel_name && !seenChannels.has(msg.channel)) {
        const entity = this.storage.upsertEntity({
          id: `slack_channel_${msg.channel}`,
          type: 'channel',
          name: msg.channel_name,
          aliases: [msg.channel],
          firstSeen: new Date(),
          lastSeen: new Date(),
          occurrenceCount: 1,
          metadata: { slackId: msg.channel },
        });
        seenChannels.set(msg.channel, entity);
        if (entity.occurrenceCount === 1) result.entitiesCreated++;
        else result.entitiesUpdated++;
      }

      // Create relation: user -> channel
      if (msg.user && msg.channel) {
        const created = this.storage.upsertRelation({
          from: `slack_user_${msg.user}`,
          to: `slack_channel_${msg.channel}`,
          type: 'participates_in',
          weight: 1,
          firstSeen: new Date(),
          lastSeen: new Date(),
          evidence: [msg.permalink || msg.ts],
        });
        if (created) result.relationsCreated++;
      }
    }
  }

  private async ingestDrive(data: any[], result: IngestResult): Promise<void> {
    for (const file of data) {
      // Index artifact with full details
      const artifact: Artifact = {
        id: `drive_${file.id}`,
        source: 'drive',
        name: file.name,
        url: file.webViewLink,
        mimeType: file.mimeType,
        createdAt: new Date(file.createdTime),
        modifiedAt: new Date(file.modifiedTime),
        owners: file.owners?.map((o: any) => o.displayName) || [],
        metadata: {
          driveId: file.id,
          parents: file.parents,
          size: file.size,
        },
      };

      this.storage.upsertArtifact(artifact);
      result.artifactsIndexed++;

      // Create owner entities
      for (const owner of file.owners || []) {
        const entity = this.storage.upsertEntity({
          id: `person_${owner.emailAddress?.replace(/[^a-z0-9]/gi, '_') || owner.displayName}`,
          type: 'person',
          name: owner.displayName,
          aliases: [owner.emailAddress].filter(Boolean),
          firstSeen: new Date(),
          lastSeen: new Date(),
          occurrenceCount: 1,
          metadata: { email: owner.emailAddress },
        });
        if (entity.occurrenceCount === 1) result.entitiesCreated++;
      }
    }
  }

  private async ingestLinear(data: any[], result: IngestResult): Promise<void> {
    for (const issue of data) {
      // Index as artifact
      const artifact: Artifact = {
        id: `linear_${issue.id}`,
        source: 'linear',
        name: `${issue.identifier}: ${issue.title}`,
        url: issue.url,
        mimeType: 'linear/issue',
        createdAt: new Date(issue.createdAt),
        modifiedAt: new Date(issue.updatedAt),
        owners: [issue.assignee?.name, issue.creator?.name].filter(Boolean),
        metadata: {
          identifier: issue.identifier,
          state: issue.state?.name,
          description: issue.description,
        },
      };

      this.storage.upsertArtifact(artifact);
      result.artifactsIndexed++;

      // Create project entity from issue identifier prefix
      const projectPrefix = issue.identifier?.split('-')[0];
      if (projectPrefix) {
        this.storage.upsertEntity({
          id: `linear_project_${projectPrefix}`,
          type: 'project',
          name: projectPrefix,
          aliases: [],
          firstSeen: new Date(),
          lastSeen: new Date(),
          occurrenceCount: 1,
          metadata: {},
        });
      }
    }
  }

  private async ingestLocal(data: any[], result: IngestResult): Promise<void> {
    for (const file of data) {
      const artifact: Artifact = {
        id: `local_${file.file_hash_sha256 || file.path}`,
        source: 'local',
        name: file.name,
        url: file.path, // Local path as URL
        mimeType: this.getMimeFromExtension(file.extension),
        createdAt: new Date(file.created_at),
        modifiedAt: new Date(file.modified_at),
        owners: [this.config.ownerName],
        metadata: {
          path: file.path,
          extension: file.extension,
          sizeBytes: file.size_bytes,
          hash: file.file_hash_sha256,
        },
      };

      this.storage.upsertArtifact(artifact);
      result.artifactsIndexed++;
    }
  }

  private async ingestClaude(data: any[], result: IngestResult): Promise<void> {
    const projects = new Set<string>();

    for (const item of data) {
      const project = item.project || 'unknown';
      projects.add(project);

      // Create project entity
      if (project !== 'unknown') {
        this.storage.upsertEntity({
          id: `claude_project_${project.replace(/[^a-z0-9]/gi, '_')}`,
          type: 'project',
          name: project,
          aliases: [],
          firstSeen: new Date(),
          lastSeen: new Date(),
          occurrenceCount: 1,
          metadata: { source: 'claude' },
        });
        result.entitiesCreated++;
      }
    }
  }

  // ============================================
  // PRIVATE: Analysis Methods
  // ============================================

  private calculateCollaborations(slackData: any[]): Array<{ person: string; context: string; strength: number }> {
    const collabs = new Map<string, { count: number; channels: Set<string> }>();

    for (const msg of slackData) {
      if (msg.user_name && msg.user !== this.config.ownerId) {
        if (!collabs.has(msg.user_name)) {
          collabs.set(msg.user_name, { count: 0, channels: new Set() });
        }
        const c = collabs.get(msg.user_name)!;
        c.count++;
        if (msg.channel_name) c.channels.add(msg.channel_name);
      }
    }

    return Array.from(collabs.entries())
      .map(([person, data]) => ({
        person,
        context: Array.from(data.channels).slice(0, 3).join(', '),
        strength: data.count,
      }))
      .sort((a, b) => b.strength - a.strength)
      .slice(0, 10);
  }

  private inferThemes(slack: any[], drive: any[], linear: any[], claude: any[]): Array<{
    name: string;
    description: string;
    artifacts: Artifact[];
    relatedPeople: string[];
    eventCount: number;
  }> {
    const themes: Map<string, {
      name: string;
      description: string;
      artifacts: Artifact[];
      relatedPeople: Set<string>;
      eventCount: number;
    }> = new Map();

    // Infer from Slack channels with my_work
    const channelWork = new Map<string, { count: number; people: Set<string> }>();
    for (const msg of slack) {
      if (msg.ownership === 'my_work' && msg.channel_name) {
        if (!channelWork.has(msg.channel_name)) {
          channelWork.set(msg.channel_name, { count: 0, people: new Set() });
        }
        const cw = channelWork.get(msg.channel_name)!;
        cw.count++;
        // Extract mentioned people
        const mentions = msg.text?.match(/<@[A-Z0-9]+>/g) || [];
        mentions.forEach((m: string) => cw.people.add(m));
      }
    }

    for (const [channel, data] of channelWork) {
      if (data.count >= 2) {
        themes.set(channel, {
          name: this.channelToTheme(channel),
          description: `Work coordination in #${channel}`,
          artifacts: [],
          relatedPeople: data.people,
          eventCount: data.count,
        });
      }
    }

    // Infer from Drive files
    for (const file of drive) {
      const category = this.categorizeFile(file.name);
      if (!themes.has(category)) {
        themes.set(category, {
          name: category,
          description: `Documentation and files related to ${category}`,
          artifacts: [],
          relatedPeople: new Set(),
          eventCount: 0,
        });
      }
      const artifact = this.storage.findArtifactByName(file.name);
      if (artifact) {
        themes.get(category)!.artifacts.push(artifact);
      }
      themes.get(category)!.eventCount++;
    }

    // Infer from Claude projects
    for (const item of claude) {
      const project = item.project || 'Development';
      if (!themes.has(project)) {
        themes.set(project, {
          name: `Development: ${project}`,
          description: `Technical development work on ${project}`,
          artifacts: [],
          relatedPeople: new Set(),
          eventCount: 0,
        });
      }
      themes.get(project)!.eventCount++;
    }

    return Array.from(themes.values())
      .map(t => ({
        ...t,
        relatedPeople: Array.from(t.relatedPeople),
      }))
      .filter(t => t.eventCount >= 2)
      .sort((a, b) => b.eventCount - a.eventCount);
  }

  private async identifyPatterns(): Promise<number> {
    // TODO: Implement pattern recognition
    // For now, return 0 - patterns will be added in future iterations
    return 0;
  }

  // ============================================
  // PRIVATE: Utility Methods
  // ============================================

  private loadJsonSafe(filePath: string): any[] {
    try {
      if (fs.existsSync(filePath)) {
        return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
      }
    } catch (e) {
      console.warn(`Warning: Could not load ${filePath}`);
    }
    return [];
  }

  private wasActiveInPeriod(entity: Entity, start: Date, end: Date): boolean {
    return entity.lastSeen >= start && entity.firstSeen <= end;
  }

  private channelToTheme(channel: string): string {
    const themeMap: Record<string, string> = {
      'intuit-internal': 'Intuit WFS Project',
      'testbox-intuit-wfs-external': 'WFS External Coordination',
      'tsa-data-engineers': 'TSA Team Sync',
      'dev-on-call': 'Engineering Support',
      'team-koala': 'Koala Team',
      'product': 'Product Discussions',
    };

    for (const [key, theme] of Object.entries(themeMap)) {
      if (channel.toLowerCase().includes(key)) {
        return theme;
      }
    }
    return `Channel: #${channel}`;
  }

  private categorizeFile(filename: string): string {
    const lower = filename.toLowerCase();
    if (lower.includes('sow') || lower.includes('statement')) return 'SOW Documents';
    if (lower.includes('retro')) return 'Retrospectives';
    if (lower.includes('sync') || lower.includes('meeting')) return 'Meetings';
    if (lower.includes('demo')) return 'Demos';
    if (lower.includes('spec') || lower.includes('requirements')) return 'Specifications';
    return 'Documents';
  }

  private getMimeFromExtension(ext: string): string {
    const mimeMap: Record<string, string> = {
      '.pdf': 'application/pdf',
      '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
      '.txt': 'text/plain',
      '.md': 'text/markdown',
      '.json': 'application/json',
    };
    return mimeMap[ext?.toLowerCase()] || 'application/octet-stream';
  }

  /**
   * Get statistics about SpineHub state
   */
  getStats(): {
    entities: number;
    relations: number;
    artifacts: number;
    patterns: number;
    lastUpdated: Date | null;
  } {
    return {
      entities: this.storage.getEntityCount(),
      relations: this.storage.getRelationCount(),
      artifacts: this.storage.getArtifactCount(),
      patterns: this.storage.getPatternCount(),
      lastUpdated: this.storage.getLastUpdated(),
    };
  }
}

/**
 * Factory function to create SpineHub instance
 */
export function createSpineHub(projectPath: string, ownerName: string, ownerId: string): SpineHub {
  const storagePath = path.join(projectPath, 'data', 'spinehub.json');

  // Ensure data directory exists
  const dataDir = path.dirname(storagePath);
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }

  return new SpineHub({
    storagePath,
    ownerName,
    ownerId,
  });
}
