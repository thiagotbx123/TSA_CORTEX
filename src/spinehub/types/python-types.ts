/**
 * TypeScript Types for Python Bridge Responses
 *
 * These types map to the responses from python/bridge.py handlers.
 */

// ============================================================================
// CODE ANALYZERS
// ============================================================================

export interface Issue {
  file: string;
  line: number;
  column: number;
  code: string;
  message: string;
  severity: 'error' | 'warning' | 'info' | 'security';
  tool: string;
  fix_available: boolean;
}

export interface AnalyzerResult {
  tool: string;
  success: boolean;
  issues: Issue[];
  summary: Record<string, number>;
  error?: string;
}

export interface ToolStatus {
  ruff: boolean;
  bandit: boolean;
  vulture: boolean;
  radon: boolean;
}

export interface RunAllAnalyzersResult {
  tools_status: ToolStatus;
  results: Record<string, AnalyzerResult>;
  total_issues: number;
  by_severity: Record<string, number>;
}

// ============================================================================
// QUALITY VALIDATOR (RAC-14)
// ============================================================================

export interface ValidationViolation {
  rule: string;
  message: string;
  line?: number;
  context?: string;
}

export interface ValidationReport {
  timestamp: string;
  passed: boolean;
  score: number;
  errors: ValidationViolation[];
  warnings: ValidationViolation[];
  metrics: {
    total_rules: number;
    passed_rules: number;
    failed_rules: number;
    word_count: number;
    line_count: number;
  };
}

export interface QualityValidationResult {
  passed: boolean;
  score: number;
  report: ValidationReport;
  formatted_report: string;
}

// ============================================================================
// CREDENTIALS MANAGER
// ============================================================================

export interface CredentialStatus {
  service: string;
  key_name: string;
  is_set: boolean;
  is_valid?: boolean;
  error?: string;
  last_checked?: string;
}

export interface AllCredentialsStatus {
  [service: string]: CredentialStatus[];
}

export interface MCPStatus {
  config_path?: string;
  server_count?: number;
  servers: string[];
  error?: string;
}

export interface CopyCredentialsResult {
  target: string;
  copied: number;
  total: number;
  services: string[];
}

// ============================================================================
// LINEAR TEMPLATES
// ============================================================================

export interface IssueTemplate {
  id: string;
  name: string;
  title_pattern: string;
  body_template: string;
  labels: string[];
  variables: string[];
}

export interface TemplateListResult {
  templates: IssueTemplate[];
}

export interface ApplyTemplateResult {
  title: string;
  body: string;
  labels: string[];
}

// ============================================================================
// PRIVACY UTILS
// ============================================================================

export interface RedactionConfig {
  redact_emails?: boolean;
  redact_phone_numbers?: boolean;
  redact_ssn?: boolean;
  redact_credit_cards?: boolean;
  redact_cpf_cnpj?: boolean;
  redact_ip_addresses?: boolean;
  custom_patterns?: string[];
}

export interface RedactionResult {
  text: string;
  redacted_count: number;
  types: string[];
}

// ============================================================================
// DATETIME UTILS
// ============================================================================

export interface DateRange {
  start: string; // ISO 8601
  end: string; // ISO 8601
  timezone: string;
}

export interface DateTimeInfo {
  utc: string;
  local: string;
  timezone: string;
  display: string;
}

// ============================================================================
// SLACK UTILS
// ============================================================================

export interface ChannelMapping {
  channel_id: string;
  channel_name: string;
  theme: string;
  category: string;
}
