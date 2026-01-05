const { DriveCollector } = require('../dist/collectors/drive');
const config = require('../config/default.json');
const fs = require('fs');

const dateRange = {
  start: new Date(Date.now() - 180 * 24 * 60 * 60 * 1000),
  end: new Date(),
  timezone: 'America/Sao_Paulo'
};

const collector = new DriveCollector(config, dateRange, 'thiago@testbox.com');

async function main() {
  const result = await collector.collect();

  const keywords = ['intuit', 'quickbooks', 'qbo', 'wfs', 'dataset', 'ingest', 'fall release', 'canada', 'construction', 'manufacturing', 'tco', 'sow', 'testbox', 'tire', 'keystone', 'mineral', 'goco', 'payroll', 'workforce', 'ies', 'alpha', 'beta'];

  const relevant = result.events.filter(e => {
    const name = e.title.toLowerCase();
    return keywords.some(k => name.includes(k));
  });

  // Agrupar por tipo de arquivo
  const byType = {};
  relevant.forEach(e => {
    const ext = (e.body_text_excerpt || '').split(' - ')[0] || 'unknown';
    if (!byType[ext]) byType[ext] = [];
    byType[ext].push(e);
  });

  // Preparar output
  const output = {
    metadata: {
      generated_at: new Date().toISOString(),
      total_files: result.events.length,
      relevant_files: relevant.length,
      date_range: { start: dateRange.start.toISOString(), end: dateRange.end.toISOString() }
    },
    files_by_type: Object.fromEntries(Object.entries(byType).map(([k, v]) => [k, v.length])),
    files: relevant.map(e => ({
      name: e.title,
      type: (e.body_text_excerpt || '').split(' - ')[0] || 'unknown',
      link: (e.references && e.references.find(r => r.type === 'url')) ? e.references.find(r => r.type === 'url').value : '',
      date: (e.event_timestamp_local || '').split('T')[0] || '',
      event_type: e.event_type
    }))
  };

  const path = require('path');
const outputPath = path.join(require('os').homedir(), 'intuit-boom', 'drive-import', 'drive_inventory.json');
fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));
  console.log('Exported to drive_inventory.json');
  console.log('Total:', result.events.length);
  console.log('Relevant:', relevant.length);
  console.log('Files by type:', JSON.stringify(output.files_by_type, null, 2));
}

main().catch(err => console.error('Error:', err.message));
