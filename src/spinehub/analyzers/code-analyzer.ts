/**
 * Code Analyzer - TypeScript wrapper for Python code analysis tools
 *
 * Provides access to:
 * - Ruff (fast Python linter)
 * - Bandit (security linter)
 * - Vulture (dead code detection)
 * - Radon (complexity analysis)
 */

import { getPythonBridge, BridgeResponse } from '../bridge';
import {
  ToolStatus,
  AnalyzerResult,
  Issue,
  RunAllAnalyzersResult,
} from '../types';

export type AnalyzerTool = 'ruff' | 'bandit' | 'vulture' | 'radon';

export interface CodeAnalyzerOptions {
  excludePaths?: string[];
  autoFix?: boolean;
}

/**
 * CodeAnalyzer - High-level interface for code analysis
 */
export class CodeAnalyzer {
  private options: CodeAnalyzerOptions;

  constructor(options: CodeAnalyzerOptions = {}) {
    this.options = {
      excludePaths: options.excludePaths || [],
      autoFix: options.autoFix || false,
    };
  }

  /**
   * Check which analysis tools are installed
   */
  async checkTools(): Promise<ToolStatus> {
    const bridge = getPythonBridge();
    const response = await bridge.call<ToolStatus>('analyzers.check_tools', {});

    if (!response.success) {
      console.error('Failed to check tools:', response.error);
      return {
        ruff: false,
        bandit: false,
        vulture: false,
        radon: false,
      };
    }

    return response.data!;
  }

  /**
   * Run all available analyzers on specified paths
   */
  async runAll(paths?: string[]): Promise<RunAllAnalyzersResult> {
    const bridge = getPythonBridge();
    const response = await bridge.call<RunAllAnalyzersResult>('analyzers.run_all', {
      paths: paths || ['.'],
      exclude: this.options.excludePaths,
    });

    if (!response.success) {
      console.error('Analysis failed:', response.error);
      return {
        tools_status: { ruff: false, bandit: false, vulture: false, radon: false },
        results: {},
        total_issues: 0,
        by_severity: {},
      };
    }

    return response.data!;
  }

  /**
   * Run a single analyzer
   */
  async runSingle(tool: AnalyzerTool, paths?: string[]): Promise<AnalyzerResult> {
    const bridge = getPythonBridge();
    const response = await bridge.call<AnalyzerResult>('analyzers.run_single', {
      tool,
      paths: paths || ['.'],
      exclude: this.options.excludePaths,
    });

    if (!response.success) {
      return {
        tool,
        success: false,
        issues: [],
        summary: {},
        error: response.error,
      };
    }

    return response.data!;
  }

  /**
   * Run Ruff linter
   */
  async runRuff(paths?: string[]): Promise<AnalyzerResult> {
    return this.runSingle('ruff', paths);
  }

  /**
   * Run Bandit security scanner
   */
  async runBandit(paths?: string[]): Promise<AnalyzerResult> {
    return this.runSingle('bandit', paths);
  }

  /**
   * Run Vulture dead code detector
   */
  async runVulture(paths?: string[]): Promise<AnalyzerResult> {
    return this.runSingle('vulture', paths);
  }

  /**
   * Run Radon complexity analyzer
   */
  async runRadon(paths?: string[]): Promise<AnalyzerResult> {
    return this.runSingle('radon', paths);
  }

  /**
   * Get issues filtered by severity
   */
  filterBySeverity(results: RunAllAnalyzersResult, severity: Issue['severity']): Issue[] {
    const allIssues: Issue[] = [];

    for (const result of Object.values(results.results)) {
      allIssues.push(...result.issues.filter(i => i.severity === severity));
    }

    return allIssues;
  }

  /**
   * Get security issues only (from Bandit)
   */
  getSecurityIssues(results: RunAllAnalyzersResult): Issue[] {
    return this.filterBySeverity(results, 'security');
  }

  /**
   * Format results as readable report
   */
  formatReport(results: RunAllAnalyzersResult): string {
    const lines: string[] = [];

    lines.push('=' .repeat(60));
    lines.push('         CODE ANALYSIS REPORT');
    lines.push('=' .repeat(60));
    lines.push('');

    // Tool status
    lines.push('[TOOLS]');
    for (const [tool, available] of Object.entries(results.tools_status)) {
      const status = available ? '[OK]' : '[--]';
      lines.push(`  ${status} ${tool}`);
    }
    lines.push('');

    // Summary
    lines.push('[SUMMARY]');
    lines.push(`  Total Issues: ${results.total_issues}`);
    for (const [severity, count] of Object.entries(results.by_severity)) {
      lines.push(`  ${severity}: ${count}`);
    }
    lines.push('');

    // Issues by tool
    for (const [tool, result] of Object.entries(results.results)) {
      if (result.issues.length === 0) continue;

      lines.push(`[${tool.toUpperCase()}] (${result.issues.length} issues)`);
      for (const issue of result.issues.slice(0, 10)) {
        lines.push(`  ${issue.file}:${issue.line} - ${issue.code}: ${issue.message}`);
      }
      if (result.issues.length > 10) {
        lines.push(`  ... and ${result.issues.length - 10} more`);
      }
      lines.push('');
    }

    lines.push('=' .repeat(60));

    return lines.join('\n');
  }
}

/**
 * Quick analysis function for CLI usage
 */
export async function analyzeCode(paths?: string[]): Promise<RunAllAnalyzersResult> {
  const analyzer = new CodeAnalyzer();
  return analyzer.runAll(paths);
}

/**
 * Check if analysis tools are available
 */
export async function checkAnalysisTools(): Promise<ToolStatus> {
  const analyzer = new CodeAnalyzer();
  return analyzer.checkTools();
}
