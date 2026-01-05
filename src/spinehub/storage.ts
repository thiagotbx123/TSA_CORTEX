/**
 * SpineHub Storage - Persistent Knowledge Graph Storage
 *
 * Implements JSON-based storage for the SpineHub knowledge graph.
 * Future: Can be upgraded to SQLite for better performance at scale.
 *
 * Key features:
 * - Atomic saves (write to temp, then rename)
 * - Automatic backup on save
 * - Fast in-memory operations with lazy persistence
 */

import * as fs from 'fs';
import * as path from 'path';
import {
  Entity,
  Relation,
  Pattern,
  Artifact,
  createEntity,
  createRelation,
  mergeEntities,
} from './entities';

interface SpineHubData {
  version: string;
  lastUpdated: string;
  entities: Record<string, Entity>;
  relations: Record<string, Relation>;
  patterns: Record<string, Pattern>;
  artifacts: Record<string, Artifact>;
}

const CURRENT_VERSION = '1.0.0';

export class SpineHubStorage {
  private filePath: string;
  private data: SpineHubData;
  private dirty: boolean = false;

  constructor(filePath: string) {
    this.filePath = filePath;
    this.data = this.createEmptyData();
  }

  private createEmptyData(): SpineHubData {
    return {
      version: CURRENT_VERSION,
      lastUpdated: new Date().toISOString(),
      entities: {},
      relations: {},
      patterns: {},
      artifacts: {},
    };
  }

  /**
   * Load data from disk
   */
  async load(): Promise<void> {
    try {
      if (fs.existsSync(this.filePath)) {
        const content = fs.readFileSync(this.filePath, 'utf-8');
        const parsed = JSON.parse(content);

        // Migrate if needed
        this.data = this.migrate(parsed);

        // Convert date strings back to Date objects
        this.hydrateData();

        console.log(`   SpineHub loaded from ${path.basename(this.filePath)}`);
      } else {
        console.log('   SpineHub: Creating new knowledge graph');
        this.data = this.createEmptyData();
      }
    } catch (error) {
      console.warn(`   Warning: Could not load SpineHub, starting fresh: ${error}`);
      this.data = this.createEmptyData();
    }
  }

  /**
   * Save data to disk (atomic write with backup)
   */
  async save(): Promise<void> {
    if (!this.dirty) return;

    try {
      // Ensure directory exists
      const dir = path.dirname(this.filePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }

      // Create backup if file exists
      if (fs.existsSync(this.filePath)) {
        const backupPath = this.filePath.replace('.json', '.backup.json');
        fs.copyFileSync(this.filePath, backupPath);
      }

      // Update timestamp
      this.data.lastUpdated = new Date().toISOString();

      // Write to temp file first
      const tempPath = this.filePath + '.tmp';
      fs.writeFileSync(tempPath, JSON.stringify(this.data, null, 2));

      // Atomic rename
      fs.renameSync(tempPath, this.filePath);

      this.dirty = false;
      console.log(`   SpineHub saved: ${this.getEntityCount()} entities, ${this.getArtifactCount()} artifacts`);
    } catch (error) {
      console.error(`   Error saving SpineHub: ${error}`);
      throw error;
    }
  }

  // ============================================
  // ENTITY OPERATIONS
  // ============================================

  /**
   * Insert or update an entity
   * Returns the entity (merged if already existed)
   */
  upsertEntity(entity: Entity): Entity {
    const existing = this.data.entities[entity.id];

    if (existing) {
      // Merge with existing
      const merged = mergeEntities(existing, entity);
      this.data.entities[entity.id] = merged;
      this.dirty = true;
      return merged;
    } else {
      // Insert new
      this.data.entities[entity.id] = entity;
      this.dirty = true;
      return entity;
    }
  }

  getEntity(id: string): Entity | null {
    return this.data.entities[id] || null;
  }

  getEntitiesByType(type: string): Entity[] {
    return Object.values(this.data.entities).filter(e => e.type === type);
  }

  getAllEntities(): Entity[] {
    return Object.values(this.data.entities);
  }

  getEntityCount(): number {
    return Object.keys(this.data.entities).length;
  }

  // ============================================
  // RELATION OPERATIONS
  // ============================================

  /**
   * Insert or update a relation
   * Returns true if newly created, false if updated
   */
  upsertRelation(relation: Relation): boolean {
    const key = `${relation.from}_${relation.type}_${relation.to}`;
    const existing = this.data.relations[key];

    if (existing) {
      // Update existing - increase weight and update lastSeen
      existing.weight += relation.weight;
      existing.lastSeen = new Date();
      existing.evidence = [...new Set([...existing.evidence, ...relation.evidence])];
      this.dirty = true;
      return false;
    } else {
      // Insert new
      this.data.relations[key] = relation;
      this.dirty = true;
      return true;
    }
  }

  getRelation(from: string, to: string, type: string): Relation | null {
    const key = `${from}_${type}_${to}`;
    return this.data.relations[key] || null;
  }

  getRelationsFrom(entityId: string): Relation[] {
    return Object.values(this.data.relations).filter(r => r.from === entityId);
  }

  getRelationsTo(entityId: string): Relation[] {
    return Object.values(this.data.relations).filter(r => r.to === entityId);
  }

  getAllRelations(): Relation[] {
    return Object.values(this.data.relations);
  }

  getRelationCount(): number {
    return Object.keys(this.data.relations).length;
  }

  // ============================================
  // ARTIFACT OPERATIONS
  // ============================================

  /**
   * Insert or update an artifact
   */
  upsertArtifact(artifact: Artifact): void {
    const existing = this.data.artifacts[artifact.id];

    if (existing) {
      // Update with newer data
      this.data.artifacts[artifact.id] = {
        ...existing,
        ...artifact,
        // Keep the earliest createdAt
        createdAt: existing.createdAt < artifact.createdAt ? existing.createdAt : artifact.createdAt,
        // Keep the latest modifiedAt
        modifiedAt: existing.modifiedAt > artifact.modifiedAt ? existing.modifiedAt : artifact.modifiedAt,
      };
    } else {
      this.data.artifacts[artifact.id] = artifact;
    }
    this.dirty = true;
  }

  getArtifact(id: string): Artifact | null {
    return this.data.artifacts[id] || null;
  }

  /**
   * Find artifact by name (exact or partial match)
   */
  findArtifactByName(name: string): Artifact | null {
    const lower = name.toLowerCase();

    // Exact match first
    for (const artifact of Object.values(this.data.artifacts)) {
      if (artifact.name.toLowerCase() === lower) {
        return artifact;
      }
    }

    // Partial match
    for (const artifact of Object.values(this.data.artifacts)) {
      if (artifact.name.toLowerCase().includes(lower)) {
        return artifact;
      }
    }

    return null;
  }

  /**
   * Find artifacts matching a pattern
   */
  findArtifactsByPattern(pattern: string): Artifact[] {
    const regex = new RegExp(pattern, 'i');
    return Object.values(this.data.artifacts).filter(a => regex.test(a.name));
  }

  /**
   * Find artifact by URL
   */
  findArtifactByUrl(url: string): Artifact | null {
    for (const artifact of Object.values(this.data.artifacts)) {
      if (artifact.url === url) {
        return artifact;
      }
    }
    return null;
  }

  getAllArtifacts(): Artifact[] {
    return Object.values(this.data.artifacts);
  }

  getArtifactsBySource(source: string): Artifact[] {
    return Object.values(this.data.artifacts).filter(a => a.source === source);
  }

  getArtifactCount(): number {
    return Object.keys(this.data.artifacts).length;
  }

  // ============================================
  // PATTERN OPERATIONS
  // ============================================

  upsertPattern(pattern: Pattern): void {
    const existing = this.data.patterns[pattern.id];

    if (existing) {
      existing.occurrences += 1;
      existing.lastSeen = new Date();
      existing.confidence = Math.min(1.0, existing.confidence + 0.1);
    } else {
      this.data.patterns[pattern.id] = pattern;
    }
    this.dirty = true;
  }

  getPattern(id: string): Pattern | null {
    return this.data.patterns[id] || null;
  }

  getAllPatterns(): Pattern[] {
    return Object.values(this.data.patterns);
  }

  getPatternCount(): number {
    return Object.keys(this.data.patterns).length;
  }

  // ============================================
  // UTILITY METHODS
  // ============================================

  getLastUpdated(): Date | null {
    if (this.data.lastUpdated) {
      return new Date(this.data.lastUpdated);
    }
    return null;
  }

  /**
   * Export all data for debugging/inspection
   */
  export(): SpineHubData {
    return { ...this.data };
  }

  /**
   * Clear all data (for testing)
   */
  clear(): void {
    this.data = this.createEmptyData();
    this.dirty = true;
  }

  // ============================================
  // PRIVATE METHODS
  // ============================================

  /**
   * Migrate data from older versions if needed
   */
  private migrate(data: any): SpineHubData {
    // For now, just ensure all required fields exist
    return {
      version: data.version || CURRENT_VERSION,
      lastUpdated: data.lastUpdated || new Date().toISOString(),
      entities: data.entities || {},
      relations: data.relations || {},
      patterns: data.patterns || {},
      artifacts: data.artifacts || {},
    };
  }

  /**
   * Convert date strings back to Date objects
   */
  private hydrateData(): void {
    // Hydrate entities
    for (const entity of Object.values(this.data.entities)) {
      if (typeof entity.firstSeen === 'string') {
        entity.firstSeen = new Date(entity.firstSeen);
      }
      if (typeof entity.lastSeen === 'string') {
        entity.lastSeen = new Date(entity.lastSeen);
      }
    }

    // Hydrate relations
    for (const relation of Object.values(this.data.relations)) {
      if (typeof relation.firstSeen === 'string') {
        relation.firstSeen = new Date(relation.firstSeen);
      }
      if (typeof relation.lastSeen === 'string') {
        relation.lastSeen = new Date(relation.lastSeen);
      }
    }

    // Hydrate patterns
    for (const pattern of Object.values(this.data.patterns)) {
      if (typeof pattern.firstSeen === 'string') {
        pattern.firstSeen = new Date(pattern.firstSeen);
      }
      if (typeof pattern.lastSeen === 'string') {
        pattern.lastSeen = new Date(pattern.lastSeen);
      }
    }

    // Hydrate artifacts
    for (const artifact of Object.values(this.data.artifacts)) {
      if (typeof artifact.createdAt === 'string') {
        artifact.createdAt = new Date(artifact.createdAt);
      }
      if (typeof artifact.modifiedAt === 'string') {
        artifact.modifiedAt = new Date(artifact.modifiedAt);
      }
    }
  }
}
