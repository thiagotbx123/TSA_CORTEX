/**
 * Linear Simple Scan - Busca issues com query otimizada (menos requests)
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

  // 6 meses atrás (reduzir escopo)
  const sixMonthsAgo = new Date();
  sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);

  console.log(`\n🔍 Buscando issues desde ${sixMonthsAgo.toISOString().split('T')[0]}...\n`);

  // Usar GraphQL direto para query mais eficiente
  const query = `
    query AllIssues($after: String, $first: Int, $filter: IssueFilter) {
      issues(after: $after, first: $first, filter: $filter) {
        nodes {
          id
          identifier
          title
          description
          priority
          createdAt
          updatedAt
          url
          state {
            name
          }
          team {
            name
          }
          assignee {
            name
          }
          labels {
            nodes {
              name
            }
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  `;

  const allIssues = [];
  let hasMore = true;
  let cursor = null;
  let page = 0;

  while (hasMore) {
    page++;
    console.log(`  Página ${page}...`);

    try {
      const result = await client.client.rawRequest(query, {
        after: cursor,
        first: 100,
        filter: {
          createdAt: { gte: sixMonthsAgo.toISOString() }
        }
      });

      const issues = result.data.issues;

      for (const issue of issues.nodes) {
        allIssues.push({
          id: issue.id,
          identifier: issue.identifier,
          title: issue.title,
          description: issue.description?.slice(0, 300),
          state: issue.state?.name || 'Unknown',
          priority: issue.priority,
          team: issue.team?.name || 'Unknown',
          assignee: issue.assignee?.name || 'Unassigned',
          labels: issue.labels?.nodes?.map(l => l.name) || [],
          createdAt: issue.createdAt,
          updatedAt: issue.updatedAt,
          url: issue.url
        });
      }

      hasMore = issues.pageInfo.hasNextPage;
      cursor = issues.pageInfo.endCursor;

      // Salvar progresso parcial a cada 5 páginas
      if (page % 5 === 0) {
        const partialPath = path.join(__dirname, '..', 'raw_exports', 'linear_partial.json');
        fs.writeFileSync(partialPath, JSON.stringify(allIssues, null, 2));
        console.log(`   [${allIssues.length} issues salvas parcialmente]`);
      }

    } catch (error) {
      console.error(`\n❌ Erro na página ${page}: ${error.message}`);
      break;
    }
  }

  console.log(`\n✅ Total: ${allIssues.length} issues encontradas\n`);

  // Análise
  const byTeam = {};
  const byState = {};
  const byPriority = { 0: 'No Priority', 1: 'Urgent', 2: 'High', 3: 'Medium', 4: 'Low' };
  const priorityCounts = {};

  for (const issue of allIssues) {
    byTeam[issue.team] = (byTeam[issue.team] || 0) + 1;
    byState[issue.state] = (byState[issue.state] || 0) + 1;
    const pName = byPriority[issue.priority] || 'Unknown';
    priorityCounts[pName] = (priorityCounts[pName] || 0) + 1;
  }

  console.log('📊 Por Time:');
  Object.entries(byTeam).sort((a,b) => b[1] - a[1]).forEach(([k,v]) => console.log(`   ${k}: ${v}`));

  console.log('\n📊 Por Estado:');
  Object.entries(byState).sort((a,b) => b[1] - a[1]).forEach(([k,v]) => console.log(`   ${k}: ${v}`));

  console.log('\n📊 Por Prioridade:');
  Object.entries(priorityCounts).sort((a,b) => b[1] - a[1]).forEach(([k,v]) => console.log(`   ${k}: ${v}`));

  // Buscar issues Intuit
  const intuitKeywords = ['intuit', 'qbo', 'quickbooks', 'tco', 'wfs', 'workforce', 'construction', 'canada', 'manufacturing', 'negative inventory', 'login', 'ecs', 'fall release', 'winter release'];

  console.log('\n🎯 Issues relacionadas a Intuit/QBO/WFS:');
  const intuitIssues = allIssues.filter(issue => {
    const text = `${issue.title} ${issue.description || ''} ${issue.labels.join(' ')} ${issue.team}`.toLowerCase();
    return intuitKeywords.some(kw => text.includes(kw));
  });

  console.log(`   Encontradas: ${intuitIssues.length}`);

  for (const issue of intuitIssues.slice(0, 30)) {
    console.log(`\n   [${issue.identifier}] ${issue.title}`);
    console.log(`      State: ${issue.state} | Priority: ${byPriority[issue.priority]} | Team: ${issue.team}`);
    if (issue.labels.length) console.log(`      Labels: ${issue.labels.join(', ')}`);
  }

  if (intuitIssues.length > 30) {
    console.log(`\n   ... e mais ${intuitIssues.length - 30} issues`);
  }

  // Salvar
  const outputPath = path.join(__dirname, '..', 'raw_exports', 'linear_full_scan.json');
  fs.writeFileSync(outputPath, JSON.stringify(allIssues, null, 2));
  console.log(`\n💾 Salvo em: ${outputPath}`);

  const intuitPath = path.join(__dirname, '..', 'raw_exports', 'linear_intuit_issues.json');
  fs.writeFileSync(intuitPath, JSON.stringify(intuitIssues, null, 2));
  console.log(`💾 Issues Intuit em: ${intuitPath}`);
}

main().catch(console.error);
