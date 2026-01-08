/**
 * Linear Teams and Users Scan - Lista todos os times e membros
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

  console.log('\n=== LINEAR TEAMS AND USERS SCAN ===\n');

  // 1. Listar todos os times
  console.log('📋 TEAMS:\n');
  const teams = await client.teams();
  const teamsData = [];

  for (const team of teams.nodes) {
    const members = await team.members();
    const memberList = members.nodes.map(m => ({
      id: m.id,
      name: m.name,
      email: m.email,
      displayName: m.displayName
    }));

    teamsData.push({
      id: team.id,
      name: team.name,
      key: team.key,
      members: memberList
    });

    console.log(`\n🔹 ${team.name} (${team.key})`);
    console.log(`   Members: ${memberList.length}`);
    memberList.forEach(m => console.log(`   - ${m.name} <${m.email || 'no email'}>`));
  }

  // 2. Listar todos os usuários da organização
  console.log('\n\n📋 ALL USERS:\n');
  const users = await client.users();
  const usersData = [];

  for (const user of users.nodes) {
    usersData.push({
      id: user.id,
      name: user.name,
      email: user.email,
      displayName: user.displayName,
      active: user.active,
      admin: user.admin
    });
    console.log(`${user.active ? '✓' : '✗'} ${user.name} <${user.email || 'no email'}>${user.admin ? ' [ADMIN]' : ''}`);
  }

  // 3. Salvar resultado
  const output = {
    scannedAt: new Date().toISOString(),
    teams: teamsData,
    users: usersData
  };

  const outputPath = path.join(__dirname, '..', 'raw_exports', 'linear_teams_users.json');
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));
  console.log(`\n💾 Saved to: ${outputPath}`);

  // 4. Resumo
  console.log('\n=== SUMMARY ===');
  console.log(`Teams: ${teamsData.length}`);
  console.log(`Users: ${usersData.length} (${usersData.filter(u => u.active).length} active)`);
}

main().catch(console.error);
