/**
 * TSA_CORTEX - Core Type Definitions
 * Weekly Worklog Automation System
 */

// ============================================================================
// CONFIGURATION TYPES
// ============================================================================

export interface Config {
  default_timezone: string;
  default_range_days: number;
  role_routing: Record<string, RoleRouting>;
  collectors: CollectorConfig;
  privacy: PrivacyConfig;
  retention: RetentionConfig;
}

export interface RoleRouting {
  linear_team: string;
  labels: string[];
  project?: string;
  assignee?: string;
}

export interface CollectorConfig {
  slack: SlackConfig;
  linear: LinearConfig;
  drive: DriveConfig;
  local: LocalConfig;
  claude: ClaudeConfig;
}

export interface SlackConfig {
  enabled: boolean;
  include_threads: boolean;
  include_mentions: boolean;
  include_file_shares: boolean;
}

export interface LinearConfig {
  enabled: boolean;
  include_comments: boolean;
  include_status_changes: boolean;
  include_mentions: boolean;
}

export interface DriveConfig {
  enabled: boolean;
  allowlist_folders: string[];
  denylist_folders: string[];
  denylist_extensions: string[];
  include_referenced_files: boolean;
}

export interface LocalConfig {
  enabled: boolean;
  scan_paths: string[];
  denylist_patterns: string[];
  max_file_size_mb: number;
}

export interface ClaudeConfig {
  enabled: boolean;
  export_path?: string;
}

export interface PrivacyConfig {
  redact_emails: boolean;
  redact_phone_numbers: boolean;
  redact_patterns: string[];
  encrypt_raw_exports: boolean;
}

export interface RetentionConfig {
  raw_exports_days: number;
  normalized_exports_days: number;
  worklog_outputs_days: number;
}

// ============================================================================
// RUN METADATA
// ============================================================================

export interface WorklogRun {
  run_id: string;
  person_id: string;
  person_display_name: string;
  start_datetime: string; // ISO 8601
  end_datetime: string; // ISO 8601
  timezone: string;
  created_at: string; // ISO 8601
  collector_version: string;
  record_counts_by_source: Record<SourceSystem, number>;
  sources_included: SourceSystem[];
  sources_missing: SourceSystem[];
  warnings: string[];
  status: 'pending' | 'collecting' | 'normalizing' | 'clustering' | 'generating' | 'posting' | 'completed' | 'failed';
}

export interface Manifest {
  run: WorklogRun;
  files: ManifestFile[];
  checksums: Record<string, string>;
}

export interface ManifestFile {
  filename: string;
  source: SourceSystem;
  record_count: number;
  file_hash_sha256: string;
  created_at: string;
}

// ============================================================================
// SOURCE SYSTEMS
// ============================================================================

export type SourceSystem = 'slack' | 'linear' | 'drive' | 'local' | 'claude';

// ============================================================================
// ACTIVITY EVENT (Canonical Schema)
// ============================================================================

export interface ActivityEvent {
  event_id: string; // stable hash
  source_system: SourceSystem;
  source_record_id: string;
  actor_user_id: string;
  actor_display_name: string;
  event_timestamp_utc: string; // ISO 8601
  event_timestamp_local: string; // ISO 8601 with timezone
  event_type: EventType;
  title: string;
  body_text_excerpt: string; // max 500 chars
  references: EventReference[];
  source_pointers: SourcePointer[];
  pii_redaction_applied: boolean;
  confidence: 'low' | 'medium' | 'high';
  raw_data?: Record<string, unknown>; // optional raw data for debugging
}

export type EventType =
  | 'message'
  | 'comment'
  | 'status_change'
  | 'file_created'
  | 'file_modified'
  | 'meeting_note'
  | 'artifact_generated'
  | 'issue_created'
  | 'issue_assigned'
  | 'issue_mentioned'
  | 'issue_updated'
  | 'thread_reply'
  | 'reaction'
  | 'link_shared';

export interface EventReference {
  type: 'url' | 'file_id' | 'issue_id' | 'user_id' | 'channel_id' | 'project_id';
  value: string;
  display_text?: string;
}

// ============================================================================
// SOURCE POINTERS
// ============================================================================

export interface SourcePointer {
  pointer_id: string; // stable id for referencing
  type: SourcePointerType;
  url?: string;
  path?: string;
  file_hash_sha256?: string;
  display_text: string;
}

export type SourcePointerType =
  | 'slack_message_permalink'
  | 'slack_thread_permalink'
  | 'slack_file_url'
  | 'linear_issue_url'
  | 'linear_comment_url'
  | 'drive_file_url'
  | 'local_file_path'
  | 'claude_conversation_url'
  | 'claude_project_artifact_id';

// ============================================================================
// TOPIC CLUSTERING
// ============================================================================

export interface TopicCluster {
  cluster_id: string;
  cluster_name: string;
  cluster_type: ClusterType;
  events: ActivityEvent[];
  summary: string;
  antecedents: string[];
  actions_taken: string[];
  outcomes: string[];
  follow_ons: string[];
  status: 'active' | 'completed' | 'blocked' | 'pending';
  source_pointer_ids: string[];
}

export type ClusterType =
  | 'customer'
  | 'project'
  | 'incident'
  | 'feature'
  | 'ops'
  | 'internal'
  | 'meeting'
  | 'documentation'
  | 'other';

// ============================================================================
// WORKLOG OUTPUT
// ============================================================================

export interface WorklogOutput {
  run_metadata: WorklogRun;
  executive_summary: WorklogBullet[];
  workstreams: WorklogWorkstream[];
  timeline: WorklogTimelineEntry[];
  decisions_and_blockers: WorklogBullet[];
  gaps_and_data_quality: string[];
  source_index: SourcePointer[];
}

export interface WorklogBullet {
  text: string;
  source_pointer_ids: string[];
}

export interface WorklogWorkstream {
  name: string;
  cluster_type: ClusterType;
  what_happened: WorklogBullet[];
  why_it_matters: string;
  status_now: string;
  next_actions: WorklogBullet[];
}

export interface WorklogTimelineEntry {
  timestamp_local: string;
  description: string;
  source_pointer_ids: string[];
}

// ============================================================================
// LINEAR INTEGRATION
// ============================================================================

export interface LinearPostRequest {
  team_id: string;
  title: string;
  body_markdown: string;
  labels: string[];
  project_id?: string;
  assignee_id?: string;
}

export interface LinearPostResult {
  success: boolean;
  issue_id?: string;
  issue_url?: string;
  error_message?: string;
  created_at: string;
}

// ============================================================================
// RAW DATA TYPES (from collectors)
// ============================================================================

export interface RawSlackMessage {
  ts: string;
  channel: string;
  channel_name?: string;
  user: string;
  user_name?: string;
  text: string;
  thread_ts?: string;
  reply_count?: number;
  reactions?: Array<{ name: string; count: number }>;
  files?: Array<{ id: string; name: string; url_private: string }>;
  permalink?: string;
}

export interface RawLinearIssue {
  id: string;
  identifier: string;
  title: string;
  description?: string;
  state: { name: string };
  assignee?: { id: string; name: string };
  creator?: { id: string; name: string };
  createdAt: string;
  updatedAt: string;
  comments?: Array<{
    id: string;
    body: string;
    user: { id: string; name: string };
    createdAt: string;
  }>;
  history?: Array<{
    id: string;
    field: string;
    fromValue: string;
    toValue: string;
    createdAt: string;
  }>;
  url: string;
}

export interface RawDriveFile {
  id: string;
  name: string;
  mimeType: string;
  createdTime: string;
  modifiedTime: string;
  webViewLink: string;
  owners?: Array<{ displayName: string; emailAddress: string }>;
  parents?: string[];
  size?: string;
}

export interface RawLocalFile {
  path: string;
  name: string;
  extension: string;
  size_bytes: number;
  created_at: string;
  modified_at: string;
  file_hash_sha256: string;
}

// ============================================================================
// CLI TYPES
// ============================================================================

export interface CLIOptions {
  startDate?: string;
  endDate?: string;
  timezone?: string;
  role?: string;
  dryRun?: boolean;
  sources?: SourceSystem[];
  outputDir?: string;
  configPath?: string;
}

// ============================================================================
// COVERAGE METRICS
// ============================================================================

export interface CoverageMetrics {
  total_events: number;
  events_with_source_pointers: number;
  percent_with_pointers: number;
  cluster_count: number;
  gap_count: number;
  events_deduped: number;
  percent_deduped: number;
  sources_coverage: Record<SourceSystem, { collected: number; normalized: number }>;
}
