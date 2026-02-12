# TSA_CORTEX v2.3

TSA Operations Hub - Worklog Automation, SOPs, and Investigation powered by multi-source data collection and SpineHub.

## Three Pillars

### 1. Worklog Automation
Collect evidence from Slack, Linear, Google Drive, Coda, and local files to generate traceable worklogs with automatic Linear ticket creation.

### 2. SOPs (Standard Operating Procedures)
Documented operational procedures for consistent execution, onboarding guides, and repeatable task automation.

### 3. Investigation & Research
Multi-source search and triangulation (Slack + Linear + Coda + Drive) with consolidated reports and root cause analysis.

## Features

- **5 data collectors**: Slack (Search API), Linear (SDK), Google Drive (OAuth2), Coda, Local files
- **SpineHub knowledge graph**: Dual TypeScript + Python implementation with JSON-RPC bridge
- **RAC-14 quality standard**: 8 validation rules (English, third person, no Slack quotes, artifacts with URLs)
- **Automatic normalization**: Deduplication, event merging, topic clustering
- **Traceable output**: Every worklog item has source pointers
- **Linear integration**: Auto-create tickets with configurable routing and TMS v2.0 labels
- **Privacy-first**: PII redaction before processing
- **Dual output**: Markdown for humans, JSON for machines

## Quick Start

```bash
# Install dependencies
npm install

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys (see docs/ONBOARDING.md)

# Run the full pipeline
npm run dev run

# Dry run (preview without posting to Linear)
npm run dev run --dry-run

# Check configuration status
npm run dev status
```

## CLI Commands

```bash
# Full pipeline (collect → normalize → cluster → spinehub → generate → post)
tsa-cortex run [options]
  -s, --start <date>     Start date (ISO format)
  -e, --end <date>       End date (ISO format)
  -t, --timezone <tz>    Timezone (default: America/Sao_Paulo)
  -r, --role <role>      Role for Linear routing (default: tsa)
  --dry-run              Generate without posting to Linear
  -c, --config <path>    Config file path
  -o, --output <dir>     Output directory

# Individual stages
tsa-cortex collect [options]       # Collect data from all sources
tsa-cortex generate [options]      # Generate worklog from collected data
tsa-cortex post -f <worklog.json>  # Post existing worklog to Linear

# Utilities
tsa-cortex status                  # Check configuration and credentials
tsa-cortex analyze [options]       # Run code analysis via SpineHub
tsa-cortex validate [options]      # Validate worklog quality (RAC-14)
tsa-cortex credentials [options]   # Manage API credentials
tsa-cortex templates [options]     # List/apply Linear issue templates
```

## Architecture

```
TSA_CORTEX/
├── src/                   # TypeScript source (~9,100 lines, 44 files)
│   ├── cli/               # CLI interface (commander.js)
│   ├── collectors/        # Data collectors (Slack, Linear, Drive, Coda, Local)
│   ├── normalizer/        # Event normalization and deduplication
│   ├── clustering/        # Topic clustering logic
│   ├── spinehub/          # SpineHub knowledge graph (TS core)
│   ├── worklog/           # Worklog generation (Markdown + JSON)
│   ├── linear/            # Linear API integration
│   ├── types/             # TypeScript type definitions (29 interfaces)
│   └── utils/             # Utilities (config, datetime, hash, privacy)
├── python/                # Python modules (~2,600 lines, 14 files)
│   ├── bridge.py          # JSON-RPC IPC handler for TS↔Python
│   ├── spinehub/          # SpineHub Python core + benchmark
│   ├── analyzers/         # Code analysis tools
│   ├── credentials/       # Credentials management
│   ├── linear/            # Linear issue templates
│   └── utils/             # Privacy, datetime, Slack channel mapping
├── config/                # Configuration files
│   ├── default.json       # Collectors, channels, role routing
│   └── spinehub.json      # Analyzer tools, quality rules, privacy
├── knowledge-base/        # SOPs, API docs, learnings, decisions
├── output/                # Generated outputs (organized by type)
│   ├── worklogs/          # Weekly worklog files
│   ├── dashboards/        # HTML dashboards and slides
│   ├── reports/           # DOCX/XLSX/CSV reports
│   ├── scripts-gen/       # Generated scripts
│   └── archive/           # Historical outputs
├── raw_exports/           # Raw collected data
└── sessions/              # Session history
```

## Pipeline

```
Collect → Normalize → Cluster → SpineHub → Generate → Post
  │          │           │          │           │        │
  │          │           │          │           │        └─ Linear ticket creation
  │          │           │          │           └─ Markdown + JSON output
  │          │           │          └─ Knowledge graph enrichment
  │          │           └─ Topic grouping
  │          └─ Dedup + merge
  └─ Slack, Linear, Drive, Coda, Local files
```

## Configuration

### Environment Variables (.env)

See `.env.example` for the full list with setup instructions. Required:

| Variable | Description |
|----------|-------------|
| `USER_DISPLAY_NAME` | Your name (appears in Linear ticket titles) |
| `SLACK_USER_TOKEN` | Slack User OAuth Token (xoxp-) |
| `SLACK_USER_ID` | Your Slack Member ID |
| `LINEAR_API_KEY` | Linear API key (lin_api_) |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret |
| `GOOGLE_REFRESH_TOKEN` | Google OAuth refresh token |

Optional: `CODA_API_TOKEN`, `GITHUB_TOKEN`, `ANTHROPIC_API_KEY`

### SpineHub Python Bridge

The Python bridge enables TypeScript to call SpineHub modules via subprocess:

```bash
echo '{"method": "quality.validate", "params": {"content": "..."}}' | python python/bridge.py
```

Available modules: `analyzers`, `quality`, `credentials`, `linear`, `privacy`, `datetime`, `slack`

## Development

```bash
npm run build          # Compile TypeScript
npm run dev            # Run with ts-node
npm test               # Run tests
npm run lint           # ESLint
```

## License

MIT
