/**
 * Configuration loader and manager
 */

import { config as dotenvConfig } from 'dotenv';
import * as fs from 'fs';
import * as path from 'path';
import { Config, SourceSystem } from '../types';

dotenvConfig();

const DEFAULT_CONFIG_PATH = path.join(__dirname, '../../config/default.json');

export function loadConfig(customPath?: string): Config {
  const configPath = customPath || DEFAULT_CONFIG_PATH;

  if (!fs.existsSync(configPath)) {
    throw new Error(`Config file not found: ${configPath}`);
  }

  const configData = fs.readFileSync(configPath, 'utf-8');
  const config = JSON.parse(configData) as Config;

  // Override with environment variables
  if (process.env.DEFAULT_TIMEZONE) {
    config.default_timezone = process.env.DEFAULT_TIMEZONE;
  }

  if (process.env.DEFAULT_RANGE_DAYS) {
    config.default_range_days = parseInt(process.env.DEFAULT_RANGE_DAYS, 10);
  }

  return config;
}

export function getEnvVar(key: string, required = false): string | undefined {
  const value = process.env[key];
  if (required && !value) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
  return value;
}

export function getSlackCredentials() {
  return {
    botToken: getEnvVar('SLACK_BOT_TOKEN'),
    userToken: getEnvVar('SLACK_USER_TOKEN'),
    userId: getEnvVar('SLACK_USER_ID'),
  };
}

export function getLinearCredentials() {
  return {
    apiKey: getEnvVar('LINEAR_API_KEY'),
    userId: getEnvVar('LINEAR_USER_ID'),
  };
}

export function getGoogleCredentials() {
  return {
    clientId: getEnvVar('GOOGLE_CLIENT_ID'),
    clientSecret: getEnvVar('GOOGLE_CLIENT_SECRET'),
    refreshToken: getEnvVar('GOOGLE_REFRESH_TOKEN'),
    userEmail: getEnvVar('GOOGLE_USER_EMAIL'),
  };
}

export function getOutputPaths() {
  return {
    output: getEnvVar('OUTPUT_DIR') || './output',
    rawExports: getEnvVar('RAW_EXPORTS_DIR') || './raw_exports',
  };
}

export function isSourceEnabled(config: Config, source: SourceSystem): boolean {
  switch (source) {
    case 'slack':
      return config.collectors.slack.enabled;
    case 'linear':
      return config.collectors.linear.enabled;
    case 'drive':
      return config.collectors.drive.enabled;
    case 'local':
      return config.collectors.local.enabled;
    case 'claude':
      return config.collectors.claude.enabled;
    default:
      return false;
  }
}

export function hasCredentials(source: SourceSystem): boolean {
  switch (source) {
    case 'slack':
      const slack = getSlackCredentials();
      return !!(slack.botToken || slack.userToken);
    case 'linear':
      const linear = getLinearCredentials();
      return !!linear.apiKey;
    case 'drive':
      const google = getGoogleCredentials();
      return !!(google.clientId && google.clientSecret && google.refreshToken);
    case 'local':
      return true; // No credentials needed
    case 'claude':
      return !!getEnvVar('CLAUDE_EXPORT_PATH');
    default:
      return false;
  }
}
