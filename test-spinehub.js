/**
 * SpineHub Test Script
 * Validates the new SpineHub core with existing data
 */

const path = require('path');
const fs = require('fs');

// Since we're testing the compiled output
const { createSpineHub } = require('./dist/spinehub/core');
const { validateWorklogQuality, QUALITY_RULES } = require('./dist/spinehub/benchmark');

async function testSpineHub() {
  console.log('🧪 Testing SpineHub Core\n');
  console.log('='.repeat(50));

  const projectPath = __dirname;
  const ownerName = 'Thiago Rodrigues';
  const ownerId = 'U06KKCA68V0'; // From .env

  // Create SpineHub
  console.log('\n1. Creating SpineHub instance...');
  const spineHub = createSpineHub(projectPath, ownerName, ownerId);

  // Initialize
  console.log('\n2. Initializing SpineHub...');
  await spineHub.initialize();

  // Ingest existing data
  console.log('\n3. Ingesting existing raw exports...');
  const rawPath = path.join(projectPath, 'raw_exports');

  const sources = ['slack', 'drive', 'linear', 'local', 'claude'];
  for (const source of sources) {
    const filePath = path.join(rawPath, `raw_events_${source}.json`);
    if (fs.existsSync(filePath)) {
      const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
      const result = await spineHub.ingest(source, data);
      console.log(`   ${source}: ${data.length} items → ${result.entitiesCreated} entities, ${result.artifactsIndexed} artifacts`);
    } else {
      console.log(`   ${source}: (no data file)`);
    }
  }

  // Check stats
  console.log('\n4. SpineHub Stats:');
  const stats = spineHub.getStats();
  console.log(`   Entities: ${stats.entities}`);
  console.log(`   Relations: ${stats.relations}`);
  console.log(`   Artifacts: ${stats.artifacts}`);
  console.log(`   Patterns: ${stats.patterns}`);
  console.log(`   Last Updated: ${stats.lastUpdated}`);

  // Test artifact resolution
  console.log('\n5. Testing Artifact Resolution:');
  const testArtifacts = [
    'TSA\'s  Retro - Biweekly - 2025/12/23 10:00 GMT-03:00 - Notes by Gemini',
    'TSA\'s  Retro - Biweekly - 2025/12/23 10:00 GMT-03:00 - Recording',
    'SOW_WFS',
    '25.12.23_RETRO TSA.pptx',
  ];

  for (const name of testArtifacts) {
    const artifact = spineHub.resolveArtifact(name);
    if (artifact) {
      console.log(`   ✅ "${name.slice(0, 40)}..." → ${artifact.url.slice(0, 50)}...`);
    } else {
      console.log(`   ❌ "${name.slice(0, 40)}..." → NOT FOUND`);
    }
  }

  // Test query for narrative
  console.log('\n6. Testing Narrative Context Query:');
  const context = await spineHub.queryForNarrative({
    startDate: new Date('2025-12-22'),
    endDate: new Date('2025-12-23'),
  });

  console.log(`   Period: ${context.period.start.toISOString().split('T')[0]} to ${context.period.end.toISOString().split('T')[0]}`);
  console.log(`   Counts: Slack=${context.counts.slack}, Drive=${context.counts.drive}, Linear=${context.counts.linear}, Local=${context.counts.local}, Claude=${context.counts.claude}`);
  console.log(`   Total: ${context.counts.total}`);
  console.log(`   People: ${context.people.length}`);
  console.log(`   Themes: ${context.themes.length}`);
  console.log(`   Top Collaborations:`);
  context.collaborations.slice(0, 5).forEach(c => {
    console.log(`     - ${c.person} (strength: ${c.strength}) in ${c.context}`);
  });

  // Test benchmark validation
  console.log('\n7. Testing Benchmark Validation:');
  console.log('   Quality Rules:');
  console.log(`   - Language: ${QUALITY_RULES.LANGUAGE}`);
  console.log(`   - Person: ${QUALITY_RULES.PERSON}`);
  console.log(`   - Slack Rule: ${QUALITY_RULES.SLACK_RULE}`);

  // Test with sample bad output
  const badOutput = `
# Weekly Worklog
I worked on the project today.
Thiago said: "posso te chamar?"
Total: 100
`;
  const validation = validateWorklogQuality(badOutput);
  console.log(`\n   Sample validation (intentionally bad):`);
  console.log(`   Valid: ${validation.valid}`);
  console.log(`   Score: ${validation.score}/100`);
  console.log(`   Issues:`);
  validation.issues.forEach(i => console.log(`     - ${i}`));

  console.log('\n' + '='.repeat(50));
  console.log('✅ SpineHub Test Complete\n');

  // Verify persistence
  const dataPath = path.join(projectPath, 'data', 'spinehub.json');
  if (fs.existsSync(dataPath)) {
    const size = fs.statSync(dataPath).size;
    console.log(`📁 SpineHub data saved to: ${dataPath} (${(size / 1024).toFixed(1)} KB)`);
  }
}

testSpineHub().catch(console.error);
