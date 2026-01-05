const { DriveCollector } = require('../dist/collectors/drive');
const config = require('../config/default.json');
const fs = require('fs');
const path = require('path');

const dateRange = {
  start: new Date(Date.now() - 180 * 24 * 60 * 60 * 1000),
  end: new Date(),
  timezone: 'America/Sao_Paulo'
};

const collector = new DriveCollector(config, dateRange, 'thiago@testbox.com');

// Keywords por tema
const KEYWORD_THEMES = {
  wfs: ['wfs', 'workforce', 'hcm', 'goco', 'mineral', 'payroll', 'hr', 'onboarding'],
  qbo: ['quickbooks', 'qbo', 'qboa', 'intuit'],
  ies: ['ies', 'enterprise'],
  dataset: ['dataset', 'data set', 'seed', 'snapshot', 'refresh', 'golden', 'synthetic'],
  ingest: ['ingest', 'ingestao', 'pipeline', 'sync', 'connector', 'integration', 'validation'],
  fall_release: ['fall release', 'fall', 'release', 'uat', 'tracker'],
  winter_release: ['winter release', 'winter'],
  canada: ['canada', 'canadian', 'cra', 'gst', 'pst'],
  construction: ['construction', 'keystone', 'job costing', 'wip', 'retainage'],
  manufacturing: ['manufacturing', 'inventory', 'bom', 'assembly'],
  tco: ['tco', 'tire', 'traction', 'fleet'],
  contract: ['sow', 'statement of work', 'msa', 'dpa', 'contract', 'proposal', 'scope'],
  security: ['soc', 'security', 'compliance', 'nda'],
  reporting: ['report', 'p&l', 'balance sheet', 'consolidated'],
  multi_entity: ['multi entity', 'multi-entity', 'consolidation', 'intercompany']
};

// Classifica relevancia
function classifyRelevance(name) {
  const lower = name.toLowerCase();

  // High relevance patterns
  const highPatterns = ['sow', 'master', 'tracker', 'roadmap', 'strategy', 'scope', 'contract',
    'architecture', 'runbook', 'requirements', 'prd', 'status', 'health check'];
  if (highPatterns.some(p => lower.includes(p))) return 'high';

  // Medium relevance - main themes
  const allKeywords = Object.values(KEYWORD_THEMES).flat();
  if (allKeywords.some(k => lower.includes(k))) return 'medium';

  return 'low';
}

// Classifica doc_role
function classifyDocRole(name, type) {
  const lower = name.toLowerCase();

  if (lower.includes('sow') || lower.includes('contract') || lower.includes('msa') || lower.includes('dpa')) return 'contract';
  if (lower.includes('roadmap') || lower.includes('strategy') || lower.includes('plan')) return 'strategy';
  if (lower.includes('tracker') || lower.includes('status')) return 'ops';
  if (lower.includes('architecture') || lower.includes('design') || lower.includes('spec')) return 'engineering';
  if (lower.includes('dataset') || lower.includes('ingest') || lower.includes('data')) return 'data';
  if (lower.includes('training') || lower.includes('demo') || lower.includes('enablement')) return 'enablement';
  if (lower.includes('security') || lower.includes('soc') || lower.includes('compliance')) return 'security';
  if (lower.includes('finance') || lower.includes('pricing') || lower.includes('invoice')) return 'finance';
  if (type.includes('spreadsheet') || type.includes('csv')) return 'data';
  if (type.includes('presentation')) return 'strategy';

  return 'other';
}

// Extrai topic_tags
function extractTopicTags(name) {
  const lower = name.toLowerCase();
  const tags = [];

  for (const [theme, keywords] of Object.entries(KEYWORD_THEMES)) {
    if (keywords.some(k => lower.includes(k))) {
      tags.push(theme);
    }
  }

  return tags.length > 0 ? tags : ['other'];
}

// Classifica confidencialidade
function classifyConfidentiality(name) {
  const lower = name.toLowerCase();

  if (lower.includes('confidential') || lower.includes('internal only') || lower.includes('signed')) return 'confidential';
  if (lower.includes('[internal]') || lower.includes('draft')) return 'internal';

  return 'internal_public';
}

async function main() {
  console.log('Starting full Drive extraction...');
  const result = await collector.collect();
  console.log('Total files:', result.events.length);

  // Processa todos os arquivos
  const files = result.events.map(e => {
    const name = e.title || '';
    const type = (e.body_text_excerpt || '').split(' - ')[0] || 'unknown';
    const link = (e.references && e.references.find(r => r.type === 'url'))
      ? e.references.find(r => r.type === 'url').value
      : '';

    return {
      file_name: name,
      file_type: type,
      drive_link: link,
      folder_path: '',
      last_modified: (e.event_timestamp_local || '').split('T')[0] || '',
      owner: e.actor_display_name || '',
      relevance: classifyRelevance(name),
      confidentiality: classifyConfidentiality(name),
      doc_role: classifyDocRole(name, type),
      topic_tags: extractTopicTags(name),
      triage_reason: '',
      short_summary: '',
      event_type: e.event_type
    };
  });

  // Filtra apenas medium e high
  const relevant = files.filter(f => f.relevance !== 'low');

  // Stats
  const stats = {
    total: files.length,
    high: files.filter(f => f.relevance === 'high').length,
    medium: files.filter(f => f.relevance === 'medium').length,
    low: files.filter(f => f.relevance === 'low').length,
    by_role: {},
    by_theme: {},
    last_30_days: 0
  };

  const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
  files.forEach(f => {
    stats.by_role[f.doc_role] = (stats.by_role[f.doc_role] || 0) + 1;
    f.topic_tags.forEach(t => {
      stats.by_theme[t] = (stats.by_theme[t] || 0) + 1;
    });
    if (new Date(f.last_modified) >= thirtyDaysAgo) stats.last_30_days++;
  });

  const output = {
    run_metadata: {
      generated_at: new Date().toISOString(),
      total_files: files.length,
      relevant_files: relevant.length,
      stats
    },
    files_index: relevant,
    high_priority_files: files.filter(f => f.relevance === 'high').slice(0, 50)
  };

  const outputPath = path.join(require('os').homedir(), 'intuit-boom', 'knowledge-base', 'drive-cortex', 'full_inventory.json');
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));

  console.log('\\n=== EXTRACTION COMPLETE ===');
  console.log('Total:', stats.total);
  console.log('High:', stats.high);
  console.log('Medium:', stats.medium);
  console.log('Low:', stats.low);
  console.log('Last 30 days:', stats.last_30_days);
  console.log('\\nBy Role:', JSON.stringify(stats.by_role, null, 2));
  console.log('\\nBy Theme:', JSON.stringify(stats.by_theme, null, 2));
  console.log('\\nOutput:', outputPath);
}

main().catch(err => console.error('Error:', err.message));
