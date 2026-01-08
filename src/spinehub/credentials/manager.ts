/**
 * Credentials Manager - TypeScript wrapper for credential management
 *
 * Provides:
 * - Status of all configured credentials
 * - MCP server status
 * - Credential copying to projects
 */

import { getPythonBridge, BridgeResponse } from '../bridge';
import { AllCredentialsStatus, CredentialStatus, MCPStatus, CopyCredentialsResult } from '../types';

export type ServiceName = 'slack' | 'linear' | 'google' | 'github' | 'anthropic' | 'gem' | 'quickbooks';

export interface CredentialsManagerOptions {
  envFile?: string;
}

/**
 * CredentialsManager - Centralized credential management
 */
export class CredentialsManager {
  private options: CredentialsManagerOptions;

  constructor(options: CredentialsManagerOptions = {}) {
    this.options = options;
  }

  /**
   * Get status of all credentials
   */
  async getAllStatus(): Promise<AllCredentialsStatus> {
    const bridge = getPythonBridge();
    const response = await bridge.call<AllCredentialsStatus>('credentials.status', {
      env_file: this.options.envFile,
    });

    if (!response.success) {
      console.error('Failed to get credentials status:', response.error);
      return {};
    }

    return response.data!;
  }

  /**
   * Get status for a specific service
   */
  async getServiceStatus(service: ServiceName): Promise<CredentialStatus[]> {
    const allStatus = await this.getAllStatus();
    return allStatus[service] || [];
  }

  /**
   * Check if a service has all required credentials set
   */
  async isServiceConfigured(service: ServiceName): Promise<boolean> {
    const status = await this.getServiceStatus(service);
    return status
      .filter(s => !s.key_name.includes('optional'))
      .every(s => s.is_set);
  }

  /**
   * Get MCP servers status
   */
  async getMCPStatus(): Promise<MCPStatus> {
    const bridge = getPythonBridge();
    const response = await bridge.call<MCPStatus>('credentials.mcp_status', {});

    if (!response.success) {
      return {
        servers: [],
        error: response.error,
      };
    }

    return response.data!;
  }

  /**
   * Copy credentials to another project
   */
  async copyToProject(targetPath: string, services?: ServiceName[]): Promise<CopyCredentialsResult> {
    const bridge = getPythonBridge();
    const response = await bridge.call<CopyCredentialsResult>('credentials.copy_to_project', {
      target_path: targetPath,
      services,
    });

    if (!response.success) {
      return {
        target: targetPath,
        copied: 0,
        total: 0,
        services: services || [],
      };
    }

    return response.data!;
  }

  /**
   * Print formatted status report
   */
  async printStatusReport(): Promise<void> {
    const allStatus = await this.getAllStatus();
    const mcpStatus = await this.getMCPStatus();

    console.log('\n' + '=' .repeat(60));
    console.log('         CREDENTIALS STATUS');
    console.log('=' .repeat(60) + '\n');

    for (const [service, credentials] of Object.entries(allStatus)) {
      console.log(`[${service.toUpperCase()}]`);
      for (const cred of credentials) {
        const icon = cred.is_set ? '[OK]' : '[--]';
        console.log(`  ${icon} ${cred.key_name}`);
      }
      console.log();
    }

    console.log(`[MCP SERVERS] (${mcpStatus.server_count || 0} configured)`);
    for (const server of mcpStatus.servers || []) {
      console.log(`  [OK] ${server}`);
    }

    console.log('\n' + '=' .repeat(60) + '\n');
  }

  /**
   * Get credential value (requires Python bridge with env access)
   */
  async get(key: string): Promise<string | null> {
    const bridge = getPythonBridge();
    const response = await bridge.call<{ value: string | null }>('credentials.get', { key });

    if (!response.success) {
      return null;
    }

    return response.data?.value || null;
  }

  /**
   * Check if credential is set
   */
  async has(key: string): Promise<boolean> {
    const value = await this.get(key);
    return value !== null && value.length > 0;
  }
}

/**
 * Get credentials status for CLI
 */
export async function getCredentialsStatus(): Promise<AllCredentialsStatus> {
  const manager = new CredentialsManager();
  return manager.getAllStatus();
}

/**
 * Get MCP status for CLI
 */
export async function getMCPStatus(): Promise<MCPStatus> {
  const manager = new CredentialsManager();
  return manager.getMCPStatus();
}

/**
 * Print credentials report
 */
export async function printCredentialsReport(): Promise<void> {
  const manager = new CredentialsManager();
  return manager.printStatusReport();
}
