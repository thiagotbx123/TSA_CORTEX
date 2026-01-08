/**
 * Quality Validator - TypeScript wrapper for worklog validation
 *
 * Provides both:
 * - Local TypeScript validation (fast, for real-time checks)
 * - Python bridge validation (comprehensive RAC-14 benchmark)
 *
 * The Python validator has more detailed rules and produces
 * formatted reports suitable for review.
 */

import * as fs from 'fs';
import { getPythonBridge, BridgeResponse } from '../bridge';
import { QualityValidationResult, ValidationReport, ValidationViolation } from '../types';
import { validateWorklogQuality as validateLocal, QUALITY_RULES } from '../benchmark';

export interface ValidatorOptions {
  usePython?: boolean;
  minScore?: number;
  strictMode?: boolean;
}

/**
 * QualityValidator - Unified validation interface
 */
export class QualityValidator {
  private options: ValidatorOptions;

  constructor(options: ValidatorOptions = {}) {
    this.options = {
      usePython: options.usePython ?? true,
      minScore: options.minScore ?? 70,
      strictMode: options.strictMode ?? false,
    };
  }

  /**
   * Validate worklog content string
   */
  async validate(content: string): Promise<QualityValidationResult> {
    if (this.options.usePython) {
      return this.validateWithPython(content);
    }
    return this.validateLocally(content);
  }

  /**
   * Validate worklog from file
   */
  async validateFile(filePath: string): Promise<QualityValidationResult> {
    if (!fs.existsSync(filePath)) {
      return {
        passed: false,
        score: 0,
        report: {
          timestamp: new Date().toISOString(),
          passed: false,
          score: 0,
          errors: [{ rule: 'FILE_001', message: `File not found: ${filePath}` }],
          warnings: [],
          metrics: { total_rules: 0, passed_rules: 0, failed_rules: 1, word_count: 0, line_count: 0 },
        },
        formatted_report: `Error: File not found: ${filePath}`,
      };
    }

    const content = fs.readFileSync(filePath, 'utf-8');
    return this.validate(content);
  }

  /**
   * Quick validation check - returns true/false only
   */
  async isValid(content: string): Promise<boolean> {
    const result = await this.validate(content);
    return result.passed && result.score >= this.options.minScore!;
  }

  /**
   * Get quality rules reference
   */
  getRules(): typeof QUALITY_RULES {
    return QUALITY_RULES;
  }

  // ============================================
  // Private Methods
  // ============================================

  private async validateWithPython(content: string): Promise<QualityValidationResult> {
    const bridge = getPythonBridge();
    const response = await bridge.call<QualityValidationResult>('quality.validate', {
      content,
    });

    if (!response.success) {
      // Fallback to local validation
      console.warn('Python validation failed, falling back to local:', response.error);
      return this.validateLocally(content);
    }

    return response.data!;
  }

  private validateLocally(content: string): QualityValidationResult {
    const localResult = validateLocal(content);

    // Convert to QualityValidationResult format
    const errors: ValidationViolation[] = [];
    const warnings: ValidationViolation[] = [];

    for (const issue of localResult.issues) {
      // Classify issues
      if (issue.includes('Portuguese') || issue.includes('Slack') || issue.includes('first person')) {
        errors.push({
          rule: this.issueToRule(issue),
          message: issue,
        });
      } else {
        warnings.push({
          rule: this.issueToRule(issue),
          message: issue,
        });
      }
    }

    const wordCount = content.split(/\s+/).length;
    const lineCount = content.split('\n').length;

    const report: ValidationReport = {
      timestamp: new Date().toISOString(),
      passed: localResult.valid,
      score: localResult.score,
      errors,
      warnings,
      metrics: {
        total_rules: 8,
        passed_rules: 8 - errors.length - warnings.length,
        failed_rules: errors.length + warnings.length,
        word_count: wordCount,
        line_count: lineCount,
      },
    };

    return {
      passed: localResult.valid && localResult.score >= this.options.minScore!,
      score: localResult.score,
      report,
      formatted_report: this.formatReport(report),
    };
  }

  private issueToRule(issue: string): string {
    if (issue.includes('Portuguese')) return 'LANG_001';
    if (issue.includes('Slack')) return 'SLACK_001';
    if (issue.includes('first person')) return 'PERS_001';
    if (issue.includes('Objective')) return 'STRUCT_001';
    if (issue.includes('Outcome')) return 'STRUCT_002';
    if (issue.includes('References')) return 'STRUCT_003';
    if (issue.includes('signature')) return 'META_001';
    if (issue.includes('Count')) return 'META_002';
    return 'UNKNOWN';
  }

  private formatReport(report: ValidationReport): string {
    const lines: string[] = [];

    lines.push('=' .repeat(60));
    lines.push('         WORKLOG QUALITY VALIDATION');
    lines.push('=' .repeat(60));
    lines.push('');

    const status = report.passed ? 'PASSED' : 'FAILED';
    lines.push(`Status: ${status}`);
    lines.push(`Score: ${report.score}/100`);
    lines.push('');

    lines.push('[METRICS]');
    lines.push(`  Word Count: ${report.metrics.word_count}`);
    lines.push(`  Line Count: ${report.metrics.line_count}`);
    lines.push(`  Rules Passed: ${report.metrics.passed_rules}/${report.metrics.total_rules}`);
    lines.push('');

    if (report.errors.length > 0) {
      lines.push('[ERRORS]');
      for (const err of report.errors) {
        lines.push(`  [${err.rule}] ${err.message}`);
      }
      lines.push('');
    }

    if (report.warnings.length > 0) {
      lines.push('[WARNINGS]');
      for (const warn of report.warnings) {
        lines.push(`  [${warn.rule}] ${warn.message}`);
      }
      lines.push('');
    }

    if (report.errors.length === 0 && report.warnings.length === 0) {
      lines.push('[OK] All quality checks passed!');
      lines.push('');
    }

    lines.push('=' .repeat(60));

    return lines.join('\n');
  }
}

/**
 * Quick validation function for CLI usage
 */
export async function validateWorklog(content: string): Promise<QualityValidationResult> {
  const validator = new QualityValidator();
  return validator.validate(content);
}

/**
 * Validate worklog file
 */
export async function validateWorklogFile(filePath: string): Promise<QualityValidationResult> {
  const validator = new QualityValidator();
  return validator.validateFile(filePath);
}

/**
 * Quick check if content passes minimum quality
 */
export async function isWorklogValid(content: string, minScore: number = 70): Promise<boolean> {
  const validator = new QualityValidator({ minScore });
  return validator.isValid(content);
}
