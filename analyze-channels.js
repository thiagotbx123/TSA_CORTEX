const data = require('./raw_exports/raw_events_slack.json');

const channels = new Map();
for (const msg of data) {
  const key = msg.channel_name;
  if (!channels.has(key)) {
    channels.set(key, { count: 0, myWork: 0, users: new Set(), sample: '' });
  }
  const ch = channels.get(key);
  ch.count++;
  if (msg.ownership === 'my_work') ch.myWork++;
  if (msg.user_name) ch.users.add(msg.user_name);
  if (!ch.sample && msg.text && msg.text.length > 10) {
    ch.sample = msg.text.slice(0, 80);
  }
}

console.log('=== CANAIS ÚNICOS COLETADOS ===\n');
const sorted = [...channels.entries()].sort((a, b) => b[1].count - a[1].count);

for (const [name, info] of sorted) {
  const users = [...info.users].slice(0, 4).join(', ');
  console.log(`📌 ${name}`);
  console.log(`   Total: ${info.count} | MY_WORK: ${info.myWork} | Users: ${users}`);
  if (info.sample) console.log(`   Sample: "${info.sample}..."`);
  console.log();
}

console.log('\n=== RESUMO ===');
console.log(`Total canais: ${channels.size}`);
console.log(`Total mensagens: ${data.length}`);
