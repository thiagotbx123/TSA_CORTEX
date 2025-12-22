/**
 * Privacy utilities for PII redaction
 */

import { PrivacyConfig } from '../types';

// Common patterns for PII
const EMAIL_PATTERN = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
const PHONE_PATTERN = /(\+?[0-9]{1,3}[-.\s]?)?\(?[0-9]{2,3}\)?[-.\s]?[0-9]{3,5}[-.\s]?[0-9]{4}/g;
const SSN_PATTERN = /\b\d{3}-\d{2}-\d{4}\b/g;
const CREDIT_CARD_PATTERN = /\b(?:\d{4}[-\s]?){3}\d{4}\b/g;
const CPF_PATTERN = /\b\d{3}\.\d{3}\.\d{3}-\d{2}\b/g;
const CNPJ_PATTERN = /\b\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}\b/g;

export interface RedactionResult {
  text: string;
  redactedCount: number;
  types: string[];
}

export function redactPII(text: string, config: PrivacyConfig): RedactionResult {
  let result = text;
  const types: string[] = [];
  let redactedCount = 0;

  if (config.redact_emails) {
    const matches = result.match(EMAIL_PATTERN);
    if (matches) {
      redactedCount += matches.length;
      types.push('email');
      result = result.replace(EMAIL_PATTERN, '[EMAIL_REDACTED]');
    }
  }

  if (config.redact_phone_numbers) {
    const matches = result.match(PHONE_PATTERN);
    if (matches) {
      redactedCount += matches.length;
      types.push('phone');
      result = result.replace(PHONE_PATTERN, '[PHONE_REDACTED]');
    }
  }

  // Always redact sensitive patterns
  const ssnMatches = result.match(SSN_PATTERN);
  if (ssnMatches) {
    redactedCount += ssnMatches.length;
    types.push('ssn');
    result = result.replace(SSN_PATTERN, '[SSN_REDACTED]');
  }

  const ccMatches = result.match(CREDIT_CARD_PATTERN);
  if (ccMatches) {
    redactedCount += ccMatches.length;
    types.push('credit_card');
    result = result.replace(CREDIT_CARD_PATTERN, '[CC_REDACTED]');
  }

  // Brazilian documents
  const cpfMatches = result.match(CPF_PATTERN);
  if (cpfMatches) {
    redactedCount += cpfMatches.length;
    types.push('cpf');
    result = result.replace(CPF_PATTERN, '[CPF_REDACTED]');
  }

  const cnpjMatches = result.match(CNPJ_PATTERN);
  if (cnpjMatches) {
    redactedCount += cnpjMatches.length;
    types.push('cnpj');
    result = result.replace(CNPJ_PATTERN, '[CNPJ_REDACTED]');
  }

  // Custom patterns
  for (const pattern of config.redact_patterns) {
    try {
      const regex = new RegExp(pattern, 'g');
      const matches = result.match(regex);
      if (matches) {
        redactedCount += matches.length;
        types.push('custom');
        result = result.replace(regex, '[REDACTED]');
      }
    } catch (e) {
      // Invalid regex pattern, skip
    }
  }

  return {
    text: result,
    redactedCount,
    types: [...new Set(types)],
  };
}

export function truncateText(text: string, maxLength: number = 500): string {
  if (text.length <= maxLength) {
    return text;
  }
  return text.substring(0, maxLength - 3) + '...';
}

export function sanitizeForLog(text: string): string {
  return text
    .replace(/\n/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .substring(0, 200);
}
