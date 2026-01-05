/**
 * Linear Intuit Search - Busca apenas issues relacionadas a Intuit
 * Usando search API com menos requests
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

  const searchTerms = [
    'intuit',
    'quickbooks',
    'qbo',
    'tco',
    'wfs',
    'workforce',
    'construction',
    'canada dataset',
    'manufacturing',
    'negative inventory',
    'fall release',
    'winter release'
  ];

  const allIssues = new Map(); // dedupe by id

  console.log('\n🔍 Buscando issues por termo...\n');

  for (const term of searchTerms) {
    console.log(`  Buscando: "${term}"...`);

    try {
      const result = await client.issueSearch(term, { first: 50 });

      for (const issue of result.nodes) {
        if (!allIssues.has(issue.id)) {
          const state = await issue.state;
          const team = await issue.team;

          allIssues.set(issue.id, {
            id: issue.id,
            identifier: issue.identifier,
            title: issue.title,
            description: issue.description?.slice(0, 300),
            state: state?.name || 'Unknown',
            priority: issue.priority,
            team: team?.name || 'Unknown',
            createdAt: issue.createdAt.toISOString(),
            updatedAt: issue.updatedAt.toISOString(),
            url: issue.url,
            searchTerm: term
          });
        }
      }

      console.log(`     Encontradas: ${result.nodes.length} (total único: ${allIssues.size})`);

      // Pequeno delay para evitar rate limit
      await new Promise(r => setTimeout(r, 200));

    } catch (error) {
      console.error(`     ❌ Erro: ${error.message}`);
    }
  }

  const issues = Array.from(allIssues.values());

  console.log(`\n✅ Total único: ${issues.length} issues\n`);

  // Análise
  const byTeam = {};
  const byState = {};
  const byPriority = { 0: 'No Priority', 1: 'Urgent', 2: 'High', 3: 'Medium', 4: 'Low' };

  for (const issue of issues) {
    byTeam[issue.team] = (byTeam[issue.team] || 0) + 1;
    byState[issue.state] = (byState[issue.state] || 0) + 1;
  }

  console.log('📊 Por Time:');
  Object.entries(byTeam).sort((a,b) => b[1] - a[1]).forEach(([k,v]) => console.log(`   ${k}: ${v}`));

  console.log('\n📊 Por Estado:');
  Object.entries(byState).sort((a,b) => b[1] - a[1]).forEach(([k,v]) => console.log(`   ${k}: ${v}`));

  // Listar issues
  console.log('\n📋 Issues encontradas:');
  for (const issue of issues) {
    const pName = byPriority[issue.priority] || '?';
    console.log(`\n   [${issue.identifier}] ${issue.title}`);
    console.log(`      State: ${issue.state} | Priority: ${pName} | Team: ${issue.team}`);
    console.log(`      URL: ${issue.url}`);
  }

  // Salvar
  const outputPath = path.join(__dirname, '..', 'raw_exports', 'linear_intuit_issues.json');
  fs.writeFileSync(outputPath, JSON.stringify(issues, null, 2));
  console.log(`\n💾 Salvo em: ${outputPath}`);
}

main().catch(console.error);
