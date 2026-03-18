const { google } = require('googleapis');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });

const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET
);
oauth2Client.setCredentials({ refresh_token: process.env.GOOGLE_REFRESH_TOKEN });

const drive = google.drive({ version: 'v3', auth: oauth2Client });

const THREE_MONTHS_AGO = new Date(Date.now() - 90 * 24 * 60 * 60 * 1000).toISOString();

async function findMeetingNotes() {
  console.log('Searching meeting notes from last 3 months...\n');

  let allFiles = [];
  let pageToken = null;

  // Search for Gemini notes (Google Docs) and meeting recordings
  const query = `(
    name contains 'Notes by Gemini' or
    name contains 'Chat' or
    name contains 'Standup' or
    name contains 'Daily' or
    name contains 'Retro' or
    name contains 'All Pedals'
  ) and mimeType = 'application/vnd.google-apps.document' and modifiedTime >= '${THREE_MONTHS_AGO}' and trashed = false`;

  do {
    const res = await drive.files.list({
      q: query,
      fields: 'nextPageToken, files(id, name, mimeType, modifiedTime, createdTime)',
      pageSize: 100,
      pageToken,
      orderBy: 'modifiedTime desc'
    });
    if (res.data.files) allFiles = allFiles.concat(res.data.files);
    pageToken = res.data.nextPageToken;
  } while (pageToken);

  console.log(`Found ${allFiles.length} meeting docs\n`);
  return allFiles;
}

async function exportAndScan(file) {
  try {
    const res = await drive.files.export({
      fileId: file.id,
      mimeType: 'text/plain'
    }, { responseType: 'text' });

    const content = res.data;
    const lines = content.split('\n');
    const matches = [];

    const searchTerms = [/taco/i, /heytaco/i, /taqueria/i, /recognition/i, /sticker/i];

    for (let i = 0; i < lines.length; i++) {
      for (const term of searchTerms) {
        if (term.test(lines[i])) {
          // Get context: 2 lines before and after
          const start = Math.max(0, i - 2);
          const end = Math.min(lines.length - 1, i + 2);
          const context = lines.slice(start, end + 1).join('\n');
          matches.push({
            line: i + 1,
            term: term.source,
            context: context.trim()
          });
          break; // avoid duplicate matches on same line
        }
      }
    }

    return { file, matches, totalLines: lines.length };
  } catch (err) {
    return { file, matches: [], error: err.message };
  }
}

async function main() {
  console.log('MEETING NOTES TACO SCAN');
  console.log(`Scanning last 3 months (since ${THREE_MONTHS_AGO.split('T')[0]})`);
  console.log('Search terms: taco, heytaco, taqueria, recognition, sticker\n');

  const files = await findMeetingNotes();

  let totalMatches = 0;

  for (const file of files) {
    const result = await exportAndScan(file);

    if (result.error) {
      console.log(`[ERROR] ${file.name}: ${result.error}`);
      continue;
    }

    if (result.matches.length > 0) {
      totalMatches += result.matches.length;
      console.log(`\n${'='.repeat(70)}`);
      console.log(`MATCH: ${file.name}`);
      console.log(`Date: ${file.createdTime}`);
      console.log(`Matches: ${result.matches.length}`);
      console.log('='.repeat(70));

      for (const m of result.matches) {
        console.log(`\n  [Line ${m.line}] (term: ${m.term})`);
        console.log('  ' + '-'.repeat(50));
        console.log('  ' + m.context.split('\n').join('\n  '));
      }
    }
  }

  console.log(`\n\n${'='.repeat(70)}`);
  console.log(`SUMMARY`);
  console.log(`${'='.repeat(70)}`);
  console.log(`Total meeting docs scanned: ${files.length}`);
  console.log(`Total matches found: ${totalMatches}`);
  console.log(`Docs with matches: ${files.filter(f => f._hasMatches).length || 'see above'}`);
}

main().catch(err => console.error('FATAL:', err.message));
