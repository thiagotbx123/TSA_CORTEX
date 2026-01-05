const data = require('../raw_exports/linear_intuit_issues.json');

const prioMap = {1: 'Urgent', 2: 'High', 3: 'Medium', 4: 'Low', 0: 'None'};

const critical = data.filter(i =>
  i.priority === 1 ||
  i.priority === 2 ||
  i.state === 'Blocked' ||
  i.state === 'Investigating'
);

console.log('=== ISSUES CRITICAS INTUIT/QBO ===\n');

const byState = {};
critical.forEach(i => {
  if (!byState[i.state]) byState[i.state] = [];
  byState[i.state].push(i);
});

Object.entries(byState).forEach(([state, issues]) => {
  console.log(`\n## ${state} (${issues.length})`);
  issues.slice(0, 10).forEach(i => {
    console.log(`  [${i.identifier}] ${i.title.slice(0,70)}`);
    console.log(`    Priority: ${prioMap[i.priority]} | Team: ${i.team} | Assignee: ${i.assignee}`);
    if (i.labels.length) console.log(`    Labels: ${i.labels.join(', ')}`);
  });
  if (issues.length > 10) console.log(`  ... +${issues.length - 10} mais`);
});

console.log('\n\n=== RESUMO ===');
console.log(`Urgent: ${critical.filter(i => i.priority === 1).length}`);
console.log(`High: ${critical.filter(i => i.priority === 2).length}`);
console.log(`Blocked: ${critical.filter(i => i.state === 'Blocked').length}`);
console.log(`Investigating: ${critical.filter(i => i.state === 'Investigating').length}`);
