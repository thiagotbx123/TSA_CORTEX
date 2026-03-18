const { google } = require('googleapis');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });

const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET
);
oauth2Client.setCredentials({ refresh_token: process.env.GOOGLE_REFRESH_TOKEN });

const drive = google.drive({ version: 'v3', auth: oauth2Client });

const FILES = [
  { id: '17nkJmfsgspJtzGX4qOhaapSErDKHBm8P', name: 'HEYTACO_DISRUPTIVE_PROPOSALS.md' },
  { id: '10H389iKAGwzXZIMdfrmi7pdM5YRzcFFb', name: 'HeyTaco_Guia_Produtividade.md' },
  { id: '1CyBTrmO1garleObdoecZC0qkubZMyjhv', name: 'alexandra_dm_full.txt' },
];

async function restrictFile(fileId, fileName) {
  console.log(`\n--- ${fileName} ---`);

  const res = await drive.permissions.list({
    fileId,
    fields: 'permissions(id, type, role, emailAddress, displayName, domain)'
  });

  const perms = res.data.permissions || [];
  console.log(`Current permissions: ${perms.length}`);

  let removed = 0;
  for (const p of perms) {
    const who = p.emailAddress || p.domain || p.type;
    if (p.role === 'owner') {
      console.log(`  KEEP: ${p.role} - ${p.displayName || ''} (${who})`);
      continue;
    }
    try {
      await drive.permissions.delete({ fileId, permissionId: p.id });
      console.log(`  REMOVED: ${p.role} - ${p.displayName || ''} (${who})`);
      removed++;
    } catch (err) {
      console.error(`  ERROR removing ${who}: ${err.message}`);
    }
  }

  console.log(`Removed ${removed} permissions. Only owner remains.`);

  // Verify
  const verify = await drive.permissions.list({
    fileId,
    fields: 'permissions(id, type, role, emailAddress, displayName, domain)'
  });
  console.log(`Verified permissions now: ${verify.data.permissions.length}`);
  verify.data.permissions.forEach(p => {
    console.log(`  ${p.role}: ${p.displayName || ''} (${p.emailAddress || p.domain || p.type})`);
  });
}

async function main() {
  console.log('Restricting TACO files to owner-only...\n');
  for (const f of FILES) {
    await restrictFile(f.id, f.name);
  }
  console.log('\nDone. All files are now private (owner-only).');
}

main().catch(err => console.error('FATAL:', err.message));
