# TSA_CORTEX

Weekly Worklog Automation System - Collect evidence from Slack, Linear, Google Drive, and local files to generate traceable worklogs.

## Features

- **Multi-source data collection**: Slack, Linear, Google Drive, Local files
- **Automatic normalization**: Deduplication and event merging
- **Topic clustering**: Group related events into workstreams
- **Traceable output**: Every worklog item has source pointers
- **Linear integration**: Auto-create tickets with configurable routing
- **Privacy-first**: PII redaction before processing
- **Dual output**: Markdown for humans, JSON for machines

## Quick Start

```bash
# Install dependencies
npm install

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys

# Run the full pipeline
npm run dev run

# Dry run (preview without posting to Linear)
npm run dev run --dry-run

# Check configuration status
npm run dev status
```

## CLI Commands

```bash
# Full pipeline
tsa-cortex run [options]
  -s, --start <date>     Start date (ISO format)
  -e, --end <date>       End date (ISO format)
  -t, --timezone <tz>    Timezone (default: America/Sao_Paulo)
  -r, --role <role>      Role for Linear routing (default: tsa)
  --dry-run              Generate without posting to Linear
  -c, --config <path>    Config file path
  -o, --output <dir>     Output directory

# Collect only
tsa-cortex collect [options]

# Post existing worklog
tsa-cortex post -f <worklog.json> [options]

# Check status
tsa-cortex status
```

## Configuration

### Environment Variables (.env)

```env
# Slack
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_USER_TOKEN=xoxp-your-token
SLACK_USER_ID=U0123456789

# Linear
LINEAR_API_KEY=lin_api_your_key
LINEAR_USER_ID=your-id

# Google Drive
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-secret
GOOGLE_REFRESH_TOKEN=your-token
GOOGLE_USER_EMAIL=you@domain.com

# General
DEFAULT_TIMEZONE=America/Sao_Paulo
DEFAULT_RANGE_DAYS=7
USER_ROLE=tsa
```

### Role Routing (config/default.json)

```json
{
  "role_routing": {
    "tsa": {
      "linear_team": "raccoons",
      "labels": ["worklog", "weekly"]
    },
    "default": {
      "linear_team": "ops",
      "labels": ["worklog", "weekly"]
    }
  }
}
```

## Architecture

```
src/
├── cli/           # Command-line interface
├── collectors/    # Data collectors (Slack, Linear, Drive, Local)
├── normalizer/    # Event normalization and deduplication
├── clustering/    # Topic clustering logic
├── worklog/       # Worklog generation (Markdown + JSON)
├── linear/        # Linear API integration
├── types/         # TypeScript type definitions
└── utils/         # Utilities (config, datetime, hash, privacy)
```

## Output Structure

### Worklog JSON Schema

```typescript
interface WorklogOutput {
  run_metadata: WorklogRun;
  executive_summary: WorklogBullet[];
  workstreams: WorklogWorkstream[];
  timeline: WorklogTimelineEntry[];
  decisions_and_blockers: WorklogBullet[];
  gaps_and_data_quality: string[];
  source_index: SourcePointer[];
}
```

### Source Pointer Types

- `slack_message_permalink`
- `slack_thread_permalink`
- `linear_issue_url`
- `linear_comment_url`
- `drive_file_url`
- `local_file_path`

## Development

```bash
# Build
npm run build

# Run tests
npm test

# Lint
npm run lint
```

## License

MIT
