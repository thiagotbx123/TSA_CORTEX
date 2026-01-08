/**
 * Python Bridge - IPC Handler for Python Modules
 *
 * Provides type-safe communication with Python SpineHUB modules
 * via subprocess using JSON-based IPC.
 */

import { spawn, ChildProcess } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

export interface PythonBridgeConfig {
  pythonPath?: string;
  bridgePath?: string;
  timeout?: number;
}

export interface BridgeResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  execution_time_ms?: number;
}

/**
 * PythonBridge - Communicates with Python modules via subprocess
 */
export class PythonBridge {
  private pythonPath: string;
  private bridgePath: string;
  private timeout: number;

  constructor(config: PythonBridgeConfig = {}) {
    // Find Python executable
    this.pythonPath = config.pythonPath || this.findPython();

    // Find bridge.py
    this.bridgePath = config.bridgePath || this.findBridge();

    // Default timeout: 60 seconds
    this.timeout = config.timeout || 60000;
  }

  /**
   * Call a Python method with parameters
   */
  async call<T = any>(method: string, params: Record<string, any> = {}): Promise<BridgeResponse<T>> {
    return new Promise((resolve) => {
      const request = JSON.stringify({ method, params });
      let stdout = '';
      let stderr = '';

      const child = spawn(this.pythonPath, [this.bridgePath], {
        cwd: path.dirname(this.bridgePath),
        env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
      });

      // Set timeout
      const timeoutId = setTimeout(() => {
        child.kill();
        resolve({
          success: false,
          error: `Timeout after ${this.timeout}ms`,
        });
      }, this.timeout);

      child.stdout.on('data', (data: Buffer) => {
        stdout += data.toString();
      });

      child.stderr.on('data', (data: Buffer) => {
        stderr += data.toString();
      });

      child.on('close', (code: number | null) => {
        clearTimeout(timeoutId);

        if (code !== 0) {
          resolve({
            success: false,
            error: stderr || `Process exited with code ${code}`,
          });
          return;
        }

        try {
          const response = JSON.parse(stdout.trim());
          resolve(response);
        } catch (e) {
          resolve({
            success: false,
            error: `Invalid JSON response: ${stdout}`,
          });
        }
      });

      child.on('error', (err: Error) => {
        clearTimeout(timeoutId);
        resolve({
          success: false,
          error: `Spawn error: ${err.message}`,
        });
      });

      // Send request to stdin
      child.stdin.write(request);
      child.stdin.end();
    });
  }

  /**
   * Check if bridge is available
   */
  async isAvailable(): Promise<boolean> {
    try {
      const response = await this.call('ping', {});
      return response.success && response.data === 'pong';
    } catch {
      return false;
    }
  }

  /**
   * Get bridge version info
   */
  async getVersion(): Promise<string | null> {
    const response = await this.call<{ version: string }>('version', {});
    return response.success ? response.data?.version || null : null;
  }

  // ============================================
  // Private Methods
  // ============================================

  private findPython(): string {
    // Try common Python paths
    const candidates = [
      'python',
      'python3',
      'py',
      'C:\\Python312\\python.exe',
      'C:\\Python311\\python.exe',
      'C:\\Python310\\python.exe',
      '/usr/bin/python3',
      '/usr/local/bin/python3',
    ];

    for (const candidate of candidates) {
      try {
        const result = require('child_process').spawnSync(candidate, ['--version']);
        if (result.status === 0) {
          return candidate;
        }
      } catch {
        continue;
      }
    }

    // Default to 'python'
    return 'python';
  }

  private findBridge(): string {
    // Look for bridge.py relative to this file
    const possiblePaths = [
      path.join(__dirname, '..', '..', '..', 'python', 'bridge.py'),
      path.join(__dirname, '..', '..', '..', '..', 'python', 'bridge.py'),
      path.join(process.cwd(), 'python', 'bridge.py'),
    ];

    for (const p of possiblePaths) {
      if (fs.existsSync(p)) {
        return p;
      }
    }

    // Default path
    return path.join(process.cwd(), 'python', 'bridge.py');
  }
}

// Singleton instance
let bridgeInstance: PythonBridge | null = null;

/**
 * Get shared PythonBridge instance
 */
export function getPythonBridge(config?: PythonBridgeConfig): PythonBridge {
  if (!bridgeInstance) {
    bridgeInstance = new PythonBridge(config);
  }
  return bridgeInstance;
}

/**
 * Reset bridge instance (for testing)
 */
export function resetPythonBridge(): void {
  bridgeInstance = null;
}
