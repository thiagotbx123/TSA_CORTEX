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
import { generateWorklog, renderWorklogMarkdown, renderNarrativeWorklog } from '../worklog';
import { postToLinear, NarrativeOptions } from '../linear';
import {
  buildSpineHub,
  SpineHubData,
  CodeAnalyzer,
  QualityValidator,
  CredentialsManager,
  LinearTemplates,
} from '../spinehub';
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
      const startTime = Date.now();

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

      // Step 3.5: Build SpineHub (Content Hub)
      console.log('\n🌐 Step 3.5: Building SpineHub (Content Hub)...');
      const rawExportsDir = getOutputPaths().rawExports;
      let spineHub: SpineHubData | undefined;
      try {
        spineHub = await buildSpineHub(
          rawExportsDir,
          userId,
          userDisplayName,
          dateRange.start,
          dateRange.end
        );
        console.log(`  Narrative blocks: ${spineHub.narrativeBlocks.length}`);
        console.log(`  Owner messages: ${spineHub.slack.ownerMessages.length}`);
      } catch (e) {
        console.log('  SpineHub skipped (no raw exports or error)');
      }

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
      const generationTimeMs = Date.now() - startTime;
      const narrativeOpts: NarrativeOptions = {
        generationTimeMs,
        version: '1.0.0',
        spineHub,
      };
      if (!options.dryRun) {
        console.log('\n📤 Step 5: Posting to Linear...');
        const result = await postToLinear(worklog, config, role, false, narrativeOpts);

        if (result.success) {
          console.log(`  ✅ Ticket created: ${result.issue_url}`);
        } else {
          console.error(`  ❌ Failed: ${result.error_message}`);
        }
      } else {
        console.log('\n📤 Step 5: Dry run - skipping Linear post');
        await postToLinear(worklog, config, role, true, narrativeOpts);
      }

      console.log('\n✅ Worklog generation complete!');
      console.log(`📁 Outputs saved to: ${outputDir}`);
    } catch (error: any) {
      console.error(`\n❌ Error: ${error.message}`);
      process.exit(1);
    }
  });

// Collect only command - Now exports context_for_narrative.json for Claude to generate narrative
program
  .command('collect')
  .description('Collect data from sources and export context for Claude narrative generation')
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
      const userDisplayName = getEnvVar('USER_DISPLAY_NAME') || userId;

      console.log('📥 Collecting data from sources...\n');
      const results = await runAllCollectors(config, dateRange, userId);

      // Save raw data
      const outputDir = options.output || getOutputPaths().rawExports;
      ensureDir(outputDir);

      const counts: Record<string, number> = {};
      for (const [source, result] of results) {
        const filename = path.join(outputDir, `raw_events_${source}.json`);
        fs.writeFileSync(filename, JSON.stringify(result.rawData, null, 2));
        console.log(`  Saved ${result.recordCount} events to ${filename}`);
        counts[source] = result.recordCount;
      }

      // Build SpineHub for artifact resolution and context
      console.log('\n🧠 Building SpineHub for context...');
      const spineHub = await buildSpineHub(
        outputDir,
        userId,
        userDisplayName,
        dateRange.start,
        dateRange.end
      );

      // Generate context_for_narrative.json - This is what Claude reads to generate the narrative
      console.log('\n📋 Generating context for Claude narrative generation...');
      const contextForNarrative = {
        metadata: {
          generatedAt: new Date().toISOString(),
          period: {
            start: dateRange.start.toISOString(),
            end: dateRange.end.toISOString(),
            startDisplay: dateRange.start.toISOString().split('T')[0],
            endDisplay: dateRange.end.toISOString().split('T')[0],
            daysSpan: Math.ceil((dateRange.end.getTime() - dateRange.start.getTime()) / (1000 * 60 * 60 * 24)),
          },
          owner: {
            id: userId,
            name: userDisplayName,
          },
          counts: {
            ...counts,
            total: Object.values(counts).reduce((a, b) => a + b, 0),
          },
        },
        // Slack: Owner messages + context summary (never quote directly per RAC-14)
        slack: {
          ownerMessages: spineHub.slack.ownerMessages.slice(0, 100).map(m => ({
            timestamp: m.timestamp,
            channel: m.channelName,
            text: m.text.slice(0, 500),
            permalink: m.permalink,
          })),
          contextSummary: {
            totalContextMessages: spineHub.slack.contextMessages.length,
            channelsActive: Array.from(spineHub.slack.channelsSummary.keys()),
          },
        },
        // Drive: Files with URLs for linking
        drive: {
          files: spineHub.drive.files.slice(0, 50).map(f => ({
            name: f.name,
            mimeType: f.mimeType,
            modifiedTime: f.modifiedTime,
            url: f.webViewLink,
            owners: f.owners,
          })),
        },
        // Linear: Issues with URLs
        linear: {
          issues: spineHub.linear.issues.map(i => ({
            identifier: i.identifier,
            title: i.title,
            state: i.state,
            url: i.url,
            description: i.description?.slice(0, 500),
          })),
        },
        // Local: Files modified
        local: {
          files: spineHub.local.files.slice(0, 50).map(f => ({
            name: f.name,
            path: f.path,
            extension: f.extension,
            modifiedAt: f.modifiedAt,
          })),
        },
        // Claude: Interactions (prompts only)
        claude: {
          interactions: spineHub.claude.interactions
            .filter(i => i.type === 'prompt')
            .slice(0, 50)
            .map(i => ({
              timestamp: i.timestamp,
              project: i.project,
              text: i.text.slice(0, 300),
            })),
        },
        // Pre-computed narrative blocks from SpineHub
        narrativeBlocks: spineHub.narrativeBlocks,
        // RAC-14 Quality Rules Reminder
        qualityRules: {
          language: 'English 100%',
          person: 'Third person ("Thiago worked on...")',
          slackRule: 'NEVER quote Slack messages directly. Use for CONTEXT ONLY.',
          titleRule: 'Use "Worklog" for periods < 7 days, "Weekly Worklog" for >= 7 days',
          artifactRule: 'Always include clickable links [Artifact Name](URL)',
          outcomeRule: 'Each theme must have a concrete outcome',
          signatureRule: 'End with markdown signature table',
        },
      };

      // Save context file to output directory
      const contextPath = path.join(getOutputPaths().output, 'context_for_narrative.json');
      ensureDir(getOutputPaths().output);
      fs.writeFileSync(contextPath, JSON.stringify(contextForNarrative, null, 2));
      console.log(`  Saved context to: ${contextPath}`);

      console.log('\n✅ Collection complete!');
      console.log('\n📝 NEXT STEP: Claude will read context_for_narrative.json to generate the worklog narrative.');
      console.log(`   File: ${contextPath}`);
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

// ============================================
// SPINEHUB INTEGRATION COMMANDS
// ============================================

// Analyze command - Run code analyzers
program
  .command('analyze')
  .description('Run code analysis (Ruff, Bandit, Vulture, Radon)')
  .argument('[paths...]', 'Paths to analyze (default: current directory)')
  .option('-t, --tool <tool>', 'Run specific tool only (ruff|bandit|vulture|radon)')
  .option('--check-tools', 'Check which tools are installed')
  .action(async (paths, options) => {
    try {
      const analyzer = new CodeAnalyzer();

      if (options.checkTools) {
        console.log('🔧 Checking installed analysis tools...\n');
        const status = await analyzer.checkTools();
        console.log('Tool Status:');
        for (const [tool, available] of Object.entries(status)) {
          const icon = available ? '✅' : '❌';
          console.log(`  ${icon} ${tool}`);
        }
        return;
      }

      const targetPaths = paths.length > 0 ? paths : ['.'];
      console.log(`🔍 Analyzing code in: ${targetPaths.join(', ')}\n`);

      if (options.tool) {
        console.log(`Running ${options.tool} only...\n`);
        const result = await analyzer.runSingle(options.tool, targetPaths);
        console.log(`\n${options.tool.toUpperCase()} Results:`);
        console.log(`  Issues found: ${result.issues.length}`);
        if (result.issues.length > 0) {
          for (const issue of result.issues.slice(0, 10)) {
            console.log(`  ${issue.file}:${issue.line} - ${issue.code}: ${issue.message}`);
          }
          if (result.issues.length > 10) {
            console.log(`  ... and ${result.issues.length - 10} more`);
          }
        }
      } else {
        console.log('Running all analyzers...\n');
        const results = await analyzer.runAll(targetPaths);
        console.log(analyzer.formatReport(results));
      }
    } catch (error: any) {
      console.error(`\n❌ Error: ${error.message}`);
      process.exit(1);
    }
  });

// Validate command - Validate worklog quality
program
  .command('validate')
  .description('Validate worklog quality (RAC-14 benchmark)')
  .argument('<file>', 'Path to worklog file (markdown or JSON)')
  .option('--min-score <score>', 'Minimum passing score (default: 70)', '70')
  .option('--strict', 'Use strict validation mode')
  .action(async (file, options) => {
    try {
      console.log(`🔍 Validating worklog: ${file}\n`);

      const validator = new QualityValidator({
        minScore: parseInt(options.minScore),
        strictMode: options.strict,
      });

      const result = await validator.validateFile(file);

      console.log(result.formatted_report);

      if (!result.passed) {
        process.exit(1);
      }
    } catch (error: any) {
      console.error(`\n❌ Error: ${error.message}`);
      process.exit(1);
    }
  });

// Credentials command - Show credentials status
program
  .command('credentials')
  .description('Show credentials and MCP server status')
  .option('--copy-to <path>', 'Copy credentials to another project')
  .option('--services <list>', 'Services to copy (comma-separated)')
  .action(async (options) => {
    try {
      const manager = new CredentialsManager();

      if (options.copyTo) {
        const services = options.services?.split(',') || undefined;
        console.log(`📋 Copying credentials to: ${options.copyTo}\n`);
        const result = await manager.copyToProject(options.copyTo, services);
        console.log(`  Copied ${result.copied} credentials`);
        console.log(`  Total in target: ${result.total}`);
        console.log(`  Target file: ${result.target}`);
      } else {
        await manager.printStatusReport();
      }
    } catch (error: any) {
      console.error(`\n❌ Error: ${error.message}`);
      process.exit(1);
    }
  });

// Templates command - Show Linear templates
program
  .command('templates')
  .description('List available Linear issue templates')
  .option('--get <id>', 'Get specific template by ID')
  .option('--apply <id>', 'Apply template with variables')
  .option('--vars <json>', 'Variables as JSON string')
  .action(async (options) => {
    try {
      const templates = new LinearTemplates();

      if (options.get) {
        const template = await templates.getTemplate(options.get);
        if (!template) {
          console.error(`❌ Template not found: ${options.get}`);
          process.exit(1);
        }
        console.log(`\n📋 Template: ${template.name}\n`);
        console.log(`ID: ${template.id}`);
        console.log(`Title Pattern: ${template.title_pattern}`);
        console.log(`Labels: ${template.labels.join(', ')}`);
        console.log(`Variables: ${template.variables.join(', ')}`);
        console.log(`\nBody Template:\n${template.body_template}`);
      } else if (options.apply) {
        const vars = options.vars ? JSON.parse(options.vars) : {};
        const result = await templates.applyTemplate(options.apply, vars);
        if (!result) {
          console.error(`❌ Failed to apply template: ${options.apply}`);
          process.exit(1);
        }
        console.log(`\n📝 Generated Issue:\n`);
        console.log(`Title: ${result.title}`);
        console.log(`Labels: ${result.labels.join(', ')}`);
        console.log(`\nBody:\n${result.body}`);
      } else {
        await templates.printTemplates();
      }
    } catch (error: any) {
      console.error(`\n❌ Error: ${error.message}`);
      process.exit(1);
    }
  });

// ============================================
// Helper functions
// ============================================

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
