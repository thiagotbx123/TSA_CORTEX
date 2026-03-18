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

async function downloadFile(fileId, fileName) {
  console.log(`\n${'='.repeat(70)}`);
  console.log(`FILE: ${fileName}`);
  console.log('='.repeat(70));

  try {
    const res = await drive.files.get(
      { fileId, alt: 'media' },
      { responseType: 'text' }
    );
    console.log(res.data);
    return res.data;
  } catch (err) {
    console.error(`Error downloading ${fileName}:`, err.message);
    return null;
  }
}

async function main() {
  for (const f of FILES) {
    await downloadFile(f.id, f.name);
  }
}

main().catch(err => console.error('FATAL:', err.message));
