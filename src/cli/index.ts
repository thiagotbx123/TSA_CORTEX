#!/usr/bin/env node
/**
 * TSA_CORTEX CLI
 * Weekly Worklog Automation Tool
 */

import { Command } from 'commander';
import * as fs from 'fs';
import * as path from 'path';
import { config as dotenvConfig } from 'dotenv';

import { loadConfig, getOutputPaths, getEnvVar } from '../utils/config';
import { parseDateRange, getDefaultDateRange } from '../utils/datetime';
import { runAllCollectors, CollectorResult } from '../collectors';
import { normalizeEvents } from '../normalizer';
import { clusterEvents } from '../clustering';
import { generateWorklog, renderWorklogMarkdown } from '../worklog';
import { postToLinear } from '../linear';
import { Config, SourceSystem, WorklogOutput } from '../types';

// Load environment variables
dotenvConfig();

const program = new Command();

program
  .name('tsa-cortex')
  .description('Weekly Worklog Automation - Collect evidence and generate traceable worklogs')
  .version('1.0.0');

// Main run command
program
  .command('run')
  .description('Run full worklog generation pipeline')
  .option('-s, --start <date>', 'Start date (ISO format)')
  .option('-e, --end <date>', 'End date (ISO format)')
  .option('-t, --timezone <tz>', 'Timezone (default: America/Sao_Paulo)')
  .option('-r, --role <role>', 'Role for Linear routing (default: tsa)')
  .option('--dry-run', 'Generate worklog but do not post to Linear')
  .option('-c, --config <path>', 'Path to config file')
  .option('-o, --output <dir>', 'Output directory')
  .action(async (options) => {
    try {
      console.log('🚀 TSA_CORTEX - Weekly Worklog Automation\n');

      // Load config
      const config = loadConfig(options.config);
      const timezone = options.timezone || config.default_timezone;
      const role = options.role || getEnvVar('USER_ROLE') || 'tsa';

      // Parse date range
      const dateRange = parseDateRange(
        options.start,
        options.end,
        timezone,
        config.default_range_days
      );

      console.log(`📅 Date range: ${dateRange.start.toISOString()} to ${dateRange.end.toISOString()}`);
      console.log(`🌍 Timezone: ${timezone}`);
      console.log(`👤 Role: ${role}\n`);

      // Get user info
      const userId = getEnvVar('SLACK_USER_ID') || getEnvVar('LINEAR_USER_ID') || 'unknown';
      const userDisplayName = getEnvVar('USER_DISPLAY_NAME') || userId;

      // Step 1: Collect data
      console.log('📥 Step 1: Collecting data from sources...\n');
      const collectorResults = await runAllCollectors(config, dateRange, userId);

      // Step 2: Normalize events
      console.log('\n📊 Step 2: Normalizing events...');
      const normalization = normalizeEvents(
        collectorResults,
        dateRange,
        userId,
        userDisplayName
      );
      console.log(`  Total events: ${normalization.totalOriginal}`);
      console.log(`  After dedup: ${normalization.events.length}`);
      console.log(`  Duplicates removed: ${normalization.duplicatesRemoved}`);

      // Step 3: Cluster events
      console.log('\n🔗 Step 3: Clustering events into topics...');
      const clustering = clusterEvents(normalization.events);
      console.log(`  Clusters created: ${clustering.clusters.length}`);
      console.log(`  Unclustered events: ${clustering.unclustered.length}`);

      // Step 4: Generate worklog
      console.log('\n📝 Step 4: Generating worklog...');
      const worklog = generateWorklog(
        normalization.manifest.run,
        normalization.events,
        clustering
      );

      // Save outputs
      const outputDir = options.output || getOutputPaths().output;
      await saveOutputs(worklog, normalization.manifest, outputDir);

      // Step 5: Post to Linear (unless dry-run)
      if (!options.dryRun) {
        console.log('\n📤 Step 5: Posting to Linear...');
        const result = await postToLinear(worklog, config, role, false);

        if (result.success) {
          console.log(`  ✅ Ticket created: ${result.issue_url}`);
        } else {
          console.error(`  ❌ Failed: ${result.error_message}`);
        }
      } else {
        console.log('\n📤 Step 5: Dry run - skipping Linear post');
        await postToLinear(worklog, config, role, true);
      }

      console.log('\n✅ Worklog generation complete!');
      console.log(`📁 Outputs saved to: ${outputDir}`);
    } catch (error: any) {
      console.error(`\n❌ Error: ${error.message}`);
      process.exit(1);
    }
  });

// Collect only command
program
  .command('collect')
  .description('Only collect data from sources (no worklog generation)')
  .option('-s, --start <date>', 'Start date (ISO format)')
  .option('-e, --end <date>', 'End date (ISO format)')
  .option('-t, --timezone <tz>', 'Timezone')
  .option('-c, --config <path>', 'Path to config file')
  .option('-o, --output <dir>', 'Output directory')
  .action(async (options) => {
    try {
      const config = loadConfig(options.config);
      const timezone = options.timezone || config.default_timezone;
      const dateRange = parseDateRange(options.start, options.end, timezone, config.default_range_days);
      const userId = getEnvVar('SLACK_USER_ID') || 'unknown';

      console.log('📥 Collecting data from sources...\n');
      const results = await runAllCollectors(config, dateRange, userId);

      // Save raw data
      const outputDir = options.output || getOutputPaths().rawExports;
      ensureDir(outputDir);

      for (const [source, result] of results) {
        const filename = path.join(outputDir, `raw_events_${source}.json`);
        fs.writeFileSync(filename, JSON.stringify(result.rawData, null, 2));
        console.log(`  Saved ${result.recordCount} events to ${filename}`);
      }

      console.log('\n✅ Collection complete!');
    } catch (error: any) {
      console.error(`\n❌ Error: ${error.message}`);
      process.exit(1);
    }
  });

// Generate only command
program
  .command('generate')
  .description('Generate worklog from existing collected data')
  .option('-i, --input <dir>', 'Input directory with raw exports')
  .option('-o, --output <dir>', 'Output directory')
  .option('-c, --config <path>', 'Path to config file')
  .option('--dry-run', 'Preview without posting to Linear')
  .action(async (options) => {
    try {
      console.log('📝 Generating worklog from collected data...\n');
      // Implementation would load from saved raw exports
      console.log('Note: This command requires previously collected data.');
      console.log('Use "tsa-cortex run" for the full pipeline.');
    } catch (error: any) {
      console.error(`\n❌ Error: ${error.message}`);
      process.exit(1);
    }
  });

// Post only command
program
  .command('post')
  .description('Post existing worklog to Linear')
  .option('-f, --file <path>', 'Path to worklog JSON file')
  .option('-r, --role <role>', 'Role for Linear routing')
  .option('-c, --config <path>', 'Path to config file')
  .option('--dry-run', 'Preview without posting')
  .action(async (options) => {
    try {
      if (!options.file) {
        console.error('❌ Please specify a worklog file with --file');
        process.exit(1);
      }

      const config = loadConfig(options.config);
      const role = options.role || 'tsa';
      const worklogData = JSON.parse(fs.readFileSync(options.file, 'utf-8')) as WorklogOutput;

      console.log('📤 Posting worklog to Linear...\n');
      const result = await postToLinear(worklogData, config, role, options.dryRun);

      if (result.success) {
        console.log(`✅ Ticket created: ${result.issue_url}`);
      } else {
        console.error(`❌ Failed: ${result.error_message}`);
      }
    } catch (error: any) {
      console.error(`\n❌ Error: ${error.message}`);
      process.exit(1);
    }
  });

// Status command
program
  .command('status')
  .description('Check configuration and credentials status')
  .option('-c, --config <path>', 'Path to config file')
  .action(async (options) => {
    try {
      console.log('🔍 TSA_CORTEX Configuration Status\n');

      const config = loadConfig(options.config);
      console.log('Configuration:');
      console.log(`  Timezone: ${config.default_timezone}`);
      console.log(`  Range: ${config.default_range_days} days`);
      console.log('');

      console.log('Collectors:');
      const sources: SourceSystem[] = ['slack', 'linear', 'drive', 'local', 'claude'];
      for (const source of sources) {
        const enabled = (config.collectors as any)[source]?.enabled;
        const status = enabled ? '✅ Enabled' : '❌ Disabled';
        console.log(`  ${source}: ${status}`);
      }
      console.log('');

      console.log('Credentials:');
      console.log(`  Slack: ${getEnvVar('SLACK_BOT_TOKEN') ? '✅ Set' : '❌ Not set'}`);
      console.log(`  Linear: ${getEnvVar('LINEAR_API_KEY') ? '✅ Set' : '❌ Not set'}`);
      console.log(`  Google: ${getEnvVar('GOOGLE_CLIENT_ID') ? '✅ Set' : '❌ Not set'}`);
      console.log('');

      console.log('Role Routing:');
      for (const [role, routing] of Object.entries(config.role_routing)) {
        console.log(`  ${role}: team=${routing.linear_team}, labels=${routing.labels.join(',')}`);
      }
    } catch (error: any) {
      console.error(`\n❌ Error: ${error.message}`);
      process.exit(1);
    }
  });

// Helper functions
function ensureDir(dir: string): void {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

async function saveOutputs(
  worklog: WorklogOutput,
  manifest: any,
  outputDir: string
): Promise<void> {
  ensureDir(outputDir);

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const baseFilename = `worklog_${timestamp}`;

  // Save JSON
  const jsonPath = path.join(outputDir, `${baseFilename}.json`);
  fs.writeFileSync(jsonPath, JSON.stringify(worklog, null, 2));
  console.log(`  Saved JSON: ${jsonPath}`);

  // Save Markdown
  const mdPath = path.join(outputDir, `${baseFilename}.md`);
  const markdown = renderWorklogMarkdown(worklog);
  fs.writeFileSync(mdPath, markdown);
  console.log(`  Saved Markdown: ${mdPath}`);

  // Save manifest
  const manifestPath = path.join(outputDir, `${baseFilename}_manifest.json`);
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
  console.log(`  Saved Manifest: ${manifestPath}`);
}

// Run CLI
program.parse();
