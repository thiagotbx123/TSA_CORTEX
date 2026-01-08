/**
 * Privacy Utils - TypeScript wrapper for PII redaction
 *
 * Provides GDPR/LGPD compliant PII detection and redaction.
 * Supports US and Brazilian document formats.
 */

import { getPythonBridge, BridgeResponse } from '../bridge';
import { RedactionConfig, RedactionResult } from '../types';

// Re-export types
export { RedactionConfig, RedactionResult };

/**
 * Default redaction configuration
 */
export const DEFAULT_REDACTION_CONFIG: RedactionConfig = {
  redact_emails: true,
  redact_phone_numbers: true,
  redact_ssn: true,
  redact_credit_cards: true,
  redact_cpf_cnpj: true,
  redact_ip_addresses: false,
  custom_patterns: [],
};

/**
 * Redact PII from text using Python module
 */
export async function redactPII(
  text: string,
  config: Partial<RedactionConfig> = {}
): Promise<RedactionResult> {
  const bridge = getPythonBridge();
  const fullConfig = { ...DEFAULT_REDACTION_CONFIG, ...config };

  const response = await bridge.call<RedactionResult>('privacy.redact', {
    text,
    config: fullConfig,
  });

  if (!response.success) {
    // Fallback to local basic redaction
    return redactPIILocal(text, fullConfig);
  }

  return response.data!;
}

/**
 * Mask email address (e.g., j***@domain.com)
 */
export async function maskEmail(email: string): Promise<string> {
  const bridge = getPythonBridge();
  const response = await bridge.call<{ masked: string }>('privacy.mask_email', { email });

  if (!response.success) {
    return maskEmailLocal(email);
  }

  return response.data?.masked || email;
}

/**
 * Mask phone number (e.g., ***-***-1234)
 */
export async function maskPhone(phone: string): Promise<string> {
  const bridge = getPythonBridge();
  const response = await bridge.call<{ masked: string }>('privacy.mask_phone', { phone });

  if (!response.success) {
    return maskPhoneLocal(phone);
  }

  return response.data?.masked || phone;
}

/**
 * Truncate text preserving word boundaries
 */
export function truncateText(text: string, maxLength: number = 500): string {
  if (text.length <= maxLength) return text;

  const truncated = text.substring(0, maxLength);
  const lastSpace = truncated.lastIndexOf(' ');

  if (lastSpace > maxLength * 0.8) {
    return truncated.substring(0, lastSpace) + '...';
  }

  return truncated + '...';
}

/**
 * Sanitize text for safe logging
 */
export function sanitizeForLog(text: string, maxLength: number = 200): string {
  return text
    .replace(/\n/g, ' ')
    .replace(/\r/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .substring(0, maxLength);
}

// ============================================
// Local Fallback Implementations
// ============================================

const PATTERNS = {
  email: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,
  phone: /(\+?[0-9]{1,3}[-.\\s]?)?\(?[0-9]{2,3}\)?[-.\\s]?[0-9]{3,5}[-.\\s]?[0-9]{4}/g,
  ssn: /\b\d{3}-\d{2}-\d{4}\b/g,
  credit_card: /\b(?:\d{4}[-\s]?){3}\d{4}\b/g,
  cpf: /\b\d{3}\.\d{3}\.\d{3}-\d{2}\b/g,
  cnpj: /\b\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}\b/g,
  ip_address: /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/g,
};

function redactPIILocal(text: string, config: RedactionConfig): RedactionResult {
  let result = text;
  const types: string[] = [];
  let redactedCount = 0;

  if (config.redact_emails) {
    const matches = result.match(PATTERNS.email) || [];
    if (matches.length > 0) {
      redactedCount += matches.length;
      types.push('email');
      result = result.replace(PATTERNS.email, '[EMAIL_REDACTED]');
    }
  }

  if (config.redact_phone_numbers) {
    const matches = result.match(PATTERNS.phone) || [];
    if (matches.length > 0) {
      redactedCount += matches.length;
      types.push('phone');
      result = result.replace(PATTERNS.phone, '[PHONE_REDACTED]');
    }
  }

  if (config.redact_ssn) {
    const matches = result.match(PATTERNS.ssn) || [];
    if (matches.length > 0) {
      redactedCount += matches.length;
      types.push('ssn');
      result = result.replace(PATTERNS.ssn, '[SSN_REDACTED]');
    }
  }

  if (config.redact_credit_cards) {
    const matches = result.match(PATTERNS.credit_card) || [];
    if (matches.length > 0) {
      redactedCount += matches.length;
      types.push('credit_card');
      result = result.replace(PATTERNS.credit_card, '[CC_REDACTED]');
    }
  }

  if (config.redact_cpf_cnpj) {
    const cpfMatches = result.match(PATTERNS.cpf) || [];
    if (cpfMatches.length > 0) {
      redactedCount += cpfMatches.length;
      types.push('cpf');
      result = result.replace(PATTERNS.cpf, '[CPF_REDACTED]');
    }

    const cnpjMatches = result.match(PATTERNS.cnpj) || [];
    if (cnpjMatches.length > 0) {
      redactedCount += cnpjMatches.length;
      types.push('cnpj');
      result = result.replace(PATTERNS.cnpj, '[CNPJ_REDACTED]');
    }
  }

  if (config.redact_ip_addresses) {
    const matches = result.match(PATTERNS.ip_address) || [];
    if (matches.length > 0) {
      redactedCount += matches.length;
      types.push('ip_address');
      result = result.replace(PATTERNS.ip_address, '[IP_REDACTED]');
    }
  }

  return {
    text: result,
    redacted_count: redactedCount,
    types: [...new Set(types)],
  };
}

function maskEmailLocal(email: string): string {
  if (!email.includes('@')) return '[INVALID_EMAIL]';

  const [local, domain] = email.split('@');
  const maskedLocal = local.length > 0 ? local[0] + '***' : '***';

  return `${maskedLocal}@${domain}`;
}

function maskPhoneLocal(phone: string): string {
  const digits = phone.replace(/\D/g, '');
  if (digits.length < 4) return '[INVALID_PHONE]';

  return `***-***-${digits.slice(-4)}`;
}
