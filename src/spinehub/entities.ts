/**
 * SpineHub Entities - Core Data Types
 *
 * Defines the fundamental types for the SpineHub knowledge graph:
 * - Entity: People, projects, channels, topics
 * - Relation: Connections between entities
 * - Pattern: Learned patterns from data
 * - Artifact: Files, documents, links with full metadata
 */

// ============================================
// ENTITY TYPES
// ============================================

export type EntityType = 'person' | 'project' | 'channel' | 'topic' | 'team';

export interface Entity {
  id: string;                    // Unique identifier
  type: EntityType;              // Type of entity
  name: string;                  // Display name
  aliases: string[];             // Alternative names/identifiers
  firstSeen: Date;               // First occurrence
  lastSeen: Date;                // Most recent occurrence
  occurrenceCount: number;       // How many times seen
  metadata: Record<string, any>; // Type-specific metadata
}

export interface PersonEntity extends Entity {
  type: 'person';
  metadata: {
    email?: string;
    slackId?: string;
    linearId?: string;
    role?: string;
    team?: string;
  };
}

export interface ProjectEntity extends Entity {
  type: 'project';
  metadata: {
    source: 'linear' | 'claude' | 'drive' | 'slack';
    identifier?: string;  // e.g., "RAC" for Linear
    status?: string;
  };
}

export interface ChannelEntity extends Entity {
  type: 'channel';
  metadata: {
    slackId: string;
    isPrivate?: boolean;
    memberCount?: number;
  };
}

// ============================================
// RELATION TYPES
// ============================================

export type RelationType =
  | 'works_with'       // Person <-> Person
  | 'works_on'         // Person -> Project
  | 'owns'             // Person -> Artifact
  | 'participates_in'  // Person -> Channel
  | 'mentions'         // Any -> Any
  | 'created'          // Person -> Artifact
  | 'reviewed'         // Person -> Artifact
  | 'discussed_in'     // Topic -> Channel
  | 'related_to';      // Any -> Any

export interface Relation {
  from: string;              // Entity ID
  to: string;                // Entity ID
  type: RelationType;        // Type of relation
  weight: number;            // Strength (more interactions = higher)
  firstSeen: Date;           // When first observed
  lastSeen: Date;            // Most recent observation
  evidence: string[];        // Source pointers proving this relation
}

// ============================================
// PATTERN TYPES
// ============================================

export interface Pattern {
  id: string;
  description: string;       // Human-readable description
  entities: string[];        // Entity IDs involved
  type: PatternType;
  confidence: number;        // 0.0 - 1.0
  occurrences: number;       // How many times observed
  firstSeen: Date;
  lastSeen: Date;
  metadata: Record<string, any>;
}

export type PatternType =
  | 'collaboration'    // "Thiago + Katherine = WFS"
  | 'workflow'         // "After meeting X, document Y is updated"
  | 'recurring'        // "Every Monday, sync with team"
  | 'dependency';      // "Project A depends on Project B"

// ============================================
// ARTIFACT TYPES
// ============================================

export interface Artifact {
  id: string;                    // Unique identifier
  source: ArtifactSource;        // Where it came from
  name: string;                  // Display name
  url: string;                   // Web link or file path
  mimeType: string;              // Content type
  createdAt: Date;               // Creation date
  modifiedAt: Date;              // Last modification
  owners: string[];              // Owner names
  metadata: Record<string, any>; // Source-specific metadata
}

export type ArtifactSource = 'drive' | 'local' | 'linear' | 'slack' | 'claude';

export interface DriveArtifact extends Artifact {
  source: 'drive';
  metadata: {
    driveId: string;
    parents?: string[];
    size?: string;
    webViewLink: string;
  };
}

export interface LocalArtifact extends Artifact {
  source: 'local';
  metadata: {
    path: string;
    extension: string;
    sizeBytes: number;
    hash?: string;
  };
}

export interface LinearArtifact extends Artifact {
  source: 'linear';
  metadata: {
    identifier: string;   // e.g., "RAC-14"
    state: string;        // e.g., "Done"
    description?: string;
  };
}

// ============================================
// HELPER FUNCTIONS
// ============================================

/**
 * Create a new entity with defaults
 */
export function createEntity(partial: Partial<Entity> & { id: string; type: EntityType; name: string }): Entity {
  return {
    aliases: [],
    firstSeen: new Date(),
    lastSeen: new Date(),
    occurrenceCount: 1,
    metadata: {},
    ...partial,
  };
}

/**
 * Create a new relation with defaults
 */
export function createRelation(partial: Partial<Relation> & { from: string; to: string; type: RelationType }): Relation {
  return {
    weight: 1,
    firstSeen: new Date(),
    lastSeen: new Date(),
    evidence: [],
    ...partial,
  };
}

/**
 * Create a new artifact with defaults
 */
export function createArtifact(partial: Partial<Artifact> & { id: string; source: ArtifactSource; name: string; url: string }): Artifact {
  return {
    mimeType: 'application/octet-stream',
    createdAt: new Date(),
    modifiedAt: new Date(),
    owners: [],
    metadata: {},
    ...partial,
  };
}

/**
 * Generate a stable ID for an entity
 */
export function generateEntityId(type: EntityType, identifier: string): string {
  const clean = identifier.replace(/[^a-z0-9]/gi, '_').toLowerCase();
  return `${type}_${clean}`;
}

/**
 * Generate a stable ID for a relation
 */
export function generateRelationId(from: string, to: string, type: RelationType): string {
  return `rel_${from}_${type}_${to}`;
}

/**
 * Check if two entities are the same (by ID or aliases)
 */
export function isSameEntity(a: Entity, b: Entity): boolean {
  if (a.id === b.id) return true;
  if (a.aliases.includes(b.id) || b.aliases.includes(a.id)) return true;
  if (a.aliases.some(alias => b.aliases.includes(alias))) return true;
  return false;
}

/**
 * Merge two entities (when we discover they're the same)
 */
export function mergeEntities(existing: Entity, incoming: Entity): Entity {
  return {
    ...existing,
    aliases: [...new Set([...existing.aliases, ...incoming.aliases, incoming.id])],
    firstSeen: existing.firstSeen < incoming.firstSeen ? existing.firstSeen : incoming.firstSeen,
    lastSeen: existing.lastSeen > incoming.lastSeen ? existing.lastSeen : incoming.lastSeen,
    occurrenceCount: existing.occurrenceCount + incoming.occurrenceCount,
    metadata: { ...existing.metadata, ...incoming.metadata },
  };
}
