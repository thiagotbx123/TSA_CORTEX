const { google } = require('googleapis');
const fs = require('fs');
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

const DEST = path.join(require('os').homedir(), 'Downloads');

async function main() {
  for (const f of FILES) {
    try {
      const res = await drive.files.get(
        { fileId: f.id, alt: 'media' },
        { responseType: 'text' }
      );
      const dest = path.join(DEST, f.name);
      fs.writeFileSync(dest, res.data, 'utf-8');
      console.log(`Saved: ${dest}`);
    } catch (err) {
      console.error(`Error ${f.name}:`, err.message);
    }
  }
}

main().catch(err => console.error('FATAL:', err.message));
