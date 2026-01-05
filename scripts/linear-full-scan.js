/**
 * Linear Full Scan - Busca TODAS as issues do workspace do último ano
 */

const { LinearClient } = require('@linear/sdk');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });

async function main() {
  const apiKey = process.env.LINEAR_API_KEY;
  if (!apiKey) {
    console.error('LINEAR_API_KEY not found in .env');
    process.exit(1);
  }

  const client = new LinearClient({ apiKey });

  // Data de 1 ano atrás
  const oneYearAgo = new Date();
  oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);

  console.log(`\n🔍 Buscando issues desde ${oneYearAgo.toISOString().split('T')[0]}...\n`);

  const allIssues = [];
  let hasMore = true;
  let cursor = null;
  let page = 0;

  while (hasMore) {
    page++;
    console.log(`  Página ${page}...`);

    const result = await client.issues({
      filter: {
        createdAt: { gte: oneYearAgo }
      },
      first: 100,
      after: cursor
    });

    for (const issue of result.nodes) {
      const state = await issue.state;
      const assignee = await issue.assignee;
      const team = await issue.team;
      const labels = await issue.labels();

      allIssues.push({
        id: issue.id,
        identifier: issue.identifier,
        title: issue.title,
        description: issue.description?.slice(0, 500),
        state: state?.name || 'Unknown',
        priority: issue.priority,
        team: team?.name || 'Unknown',
        assignee: assignee?.name || 'Unassigned',
        labels: labels.nodes.map(l => l.name),
        createdAt: issue.createdAt.toISOString(),
        updatedAt: issue.updatedAt.toISOString(),
        url: issue.url
      });
    }

    hasMore = result.pageInfo.hasNextPage;
    cursor = result.pageInfo.endCursor;
  }

  console.log(`\n✅ Total: ${allIssues.length} issues encontradas\n`);

  // Análise por time
  const byTeam = {};
  const byState = {};
  const byPriority = { 0: 'No Priority', 1: 'Urgent', 2: 'High', 3: 'Medium', 4: 'Low' };
  const priorityCounts = {};
  const byLabel = {};

  for (const issue of allIssues) {
    // Por time
    byTeam[issue.team] = (byTeam[issue.team] || 0) + 1;

    // Por estado
    byState[issue.state] = (byState[issue.state] || 0) + 1;

    // Por prioridade
    const pName = byPriority[issue.priority] || 'Unknown';
    priorityCounts[pName] = (priorityCounts[pName] || 0) + 1;

    // Por label
    for (const label of issue.labels) {
      byLabel[label] = (byLabel[label] || 0) + 1;
    }
  }

  console.log('📊 Por Time:');
  Object.entries(byTeam).sort((a,b) => b[1] - a[1]).forEach(([k,v]) => console.log(`   ${k}: ${v}`));

  console.log('\n📊 Por Estado:');
  Object.entries(byState).sort((a,b) => b[1] - a[1]).forEach(([k,v]) => console.log(`   ${k}: ${v}`));

  console.log('\n📊 Por Prioridade:');
  Object.entries(priorityCounts).sort((a,b) => b[1] - a[1]).forEach(([k,v]) => console.log(`   ${k}: ${v}`));

  console.log('\n📊 Por Label (top 20):');
  Object.entries(byLabel).sort((a,b) => b[1] - a[1]).slice(0, 20).forEach(([k,v]) => console.log(`   ${k}: ${v}`));

  // Buscar issues relacionadas a Intuit/TCO/WFS
  const intuitKeywords = ['intuit', 'qbo', 'quickbooks', 'tco', 'wfs', 'workforce', 'construction', 'canada', 'manufacturing', 'negative inventory', 'login', 'ecs'];

  console.log('\n🎯 Issues relacionadas a Intuit/QBO/WFS:');
  const intuitIssues = allIssues.filter(issue => {
    const text = `${issue.title} ${issue.description || ''} ${issue.labels.join(' ')}`.toLowerCase();
    return intuitKeywords.some(kw => text.includes(kw));
  });

  console.log(`   Encontradas: ${intuitIssues.length}`);

  intuitIssues.forEach(issue => {
    console.log(`\n   [${issue.identifier}] ${issue.title}`);
    console.log(`      State: ${issue.state} | Priority: ${byPriority[issue.priority]} | Team: ${issue.team}`);
    console.log(`      Labels: ${issue.labels.join(', ') || 'none'}`);
    console.log(`      URL: ${issue.url}`);
  });

  // Salvar JSON completo
  const outputPath = path.join(__dirname, '..', 'raw_exports', 'linear_full_scan.json');
  fs.writeFileSync(outputPath, JSON.stringify(allIssues, null, 2));
  console.log(`\n💾 Salvo em: ${outputPath}`);

  // Salvar issues Intuit separado
  const intuitPath = path.join(__dirname, '..', 'raw_exports', 'linear_intuit_issues.json');
  fs.writeFileSync(intuitPath, JSON.stringify(intuitIssues, null, 2));
  console.log(`💾 Issues Intuit em: ${intuitPath}`);
}

main().catch(console.error);
