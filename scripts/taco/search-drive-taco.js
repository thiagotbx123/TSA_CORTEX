/**
 * Search Google Drive for anything related to "TACO" / "HeyTaco"
 * - File names containing taco
 * - File content containing taco (fullText search)
 * - Comments, sharing activity
 */

const { google } = require('googleapis');
require('dotenv').config({ path: require('path').join(__dirname, '..', '.env') });

const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET
);

oauth2Client.setCredentials({
  refresh_token: process.env.GOOGLE_REFRESH_TOKEN
});

const drive = google.drive({ version: 'v3', auth: oauth2Client });

async function searchFiles(query, label) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`SEARCH: ${label}`);
  console.log(`Query: ${query}`);
  console.log('='.repeat(60));

  let allFiles = [];
  let pageToken = null;

  try {
    do {
      const res = await drive.files.list({
        q: query,
        fields: 'nextPageToken, files(id, name, mimeType, modifiedTime, createdTime, owners, sharingUser, shared, webViewLink, lastModifyingUser, permissions)',
        pageSize: 100,
        pageToken: pageToken,
        includeItemsFromAllDrives: true,
        supportsAllDrives: true,
        orderBy: 'modifiedTime desc'
      });

      if (res.data.files) {
        allFiles = allFiles.concat(res.data.files);
      }
      pageToken = res.data.nextPageToken;
    } while (pageToken);

    console.log(`Found: ${allFiles.length} files\n`);

    allFiles.forEach((f, i) => {
      console.log(`--- File ${i + 1} ---`);
      console.log(`  Name: ${f.name}`);
      console.log(`  Type: ${f.mimeType}`);
      console.log(`  Created: ${f.createdTime}`);
      console.log(`  Modified: ${f.modifiedTime}`);
      console.log(`  Link: ${f.webViewLink || 'N/A'}`);
      if (f.owners) console.log(`  Owner: ${f.owners.map(o => `${o.displayName} <${o.emailAddress}>`).join(', ')}`);
      if (f.lastModifyingUser) console.log(`  Last Modified By: ${f.lastModifyingUser.displayName} <${f.lastModifyingUser.emailAddress}>`);
      if (f.shared) console.log(`  Shared: YES`);
      if (f.sharingUser) console.log(`  Shared By: ${f.sharingUser.displayName} <${f.sharingUser.emailAddress}>`);
      console.log('');
    });

    return allFiles;
  } catch (err) {
    console.error(`Error in "${label}":`, err.message);
    return [];
  }
}

async function getFileComments(fileId, fileName) {
  try {
    const res = await drive.comments.list({
      fileId: fileId,
      fields: 'comments(id, content, author, createdTime, modifiedTime, resolved, replies)',
      includeDeleted: false
    });

    if (res.data.comments && res.data.comments.length > 0) {
      console.log(`\n  COMMENTS on "${fileName}":`);
      res.data.comments.forEach((c, i) => {
        console.log(`    Comment ${i + 1}: "${c.content}"`);
        console.log(`      By: ${c.author.displayName} at ${c.createdTime}`);
        if (c.replies) {
          c.replies.forEach(r => {
            console.log(`      Reply: "${r.content}" by ${r.author.displayName} at ${r.createdTime}`);
          });
        }
      });
      return res.data.comments;
    }
    return [];
  } catch (err) {
    // Comments API may not be available for all files
    return [];
  }
}

async function getFileRevisions(fileId, fileName) {
  try {
    const res = await drive.revisions.list({
      fileId: fileId,
      fields: 'revisions(id, modifiedTime, lastModifyingUser)',
      pageSize: 20
    });

    if (res.data.revisions && res.data.revisions.length > 0) {
      console.log(`\n  REVISIONS on "${fileName}" (last ${res.data.revisions.length}):`);
      res.data.revisions.slice(-5).forEach((r, i) => {
        const user = r.lastModifyingUser ? `${r.lastModifyingUser.displayName} <${r.lastModifyingUser.emailAddress}>` : 'unknown';
        console.log(`    Rev ${i + 1}: ${r.modifiedTime} by ${user}`);
      });
    }
    return res.data.revisions || [];
  } catch (err) {
    return [];
  }
}

async function getFilePermissions(fileId, fileName) {
  try {
    const res = await drive.permissions.list({
      fileId: fileId,
      fields: 'permissions(id, type, role, emailAddress, displayName, domain)'
    });

    if (res.data.permissions && res.data.permissions.length > 0) {
      console.log(`\n  PERMISSIONS on "${fileName}":`);
      res.data.permissions.forEach((p, i) => {
        const who = p.emailAddress || p.domain || p.type;
        console.log(`    ${p.role}: ${p.displayName || ''} (${who})`);
      });
    }
    return res.data.permissions || [];
  } catch (err) {
    return [];
  }
}

async function main() {
  console.log('Google Drive TACO Search');
  console.log('========================');
  console.log(`Timestamp: ${new Date().toISOString()}\n`);

  // 1. Full-text search for "taco" (searches file names AND content)
  const fullTextFiles = await searchFiles(
    "fullText contains 'taco' and trashed = false",
    'Full-text search: "taco" (name + content)'
  );

  // 2. Full-text search for "heytaco"
  const heyTacoFiles = await searchFiles(
    "fullText contains 'heytaco' and trashed = false",
    'Full-text search: "heytaco" (name + content)'
  );

  // 3. Name contains taco
  const nameFiles = await searchFiles(
    "name contains 'taco' and trashed = false",
    'Name contains: "taco"'
  );

  // 4. Search for "taqueria" (the HeyTaco Slack channel)
  const taqueriaFiles = await searchFiles(
    "fullText contains 'taqueria' and trashed = false",
    'Full-text search: "taqueria"'
  );

  // 5. Also check trashed files
  const trashedFiles = await searchFiles(
    "fullText contains 'taco' and trashed = true",
    'TRASHED files with "taco"'
  );

  // Collect all unique files
  const allFileIds = new Set();
  const allFiles = [];
  [fullTextFiles, heyTacoFiles, nameFiles, taqueriaFiles, trashedFiles].flat().forEach(f => {
    if (!allFileIds.has(f.id)) {
      allFileIds.add(f.id);
      allFiles.push(f);
    }
  });

  console.log(`\n${'='.repeat(60)}`);
  console.log(`TOTAL UNIQUE FILES FOUND: ${allFiles.length}`);
  console.log('='.repeat(60));

  // For each file, get comments, revisions, and permissions
  if (allFiles.length > 0) {
    console.log('\n--- DEEP INSPECTION ---\n');

    for (const f of allFiles) {
      console.log(`\nFile: "${f.name}" (${f.mimeType})`);
      console.log(`  Link: ${f.webViewLink || 'N/A'}`);

      await getFileComments(f.id, f.name);
      await getFileRevisions(f.id, f.name);
      await getFilePermissions(f.id, f.name);
    }
  }

  // Save results to JSON
  const output = {
    search_timestamp: new Date().toISOString(),
    total_unique_files: allFiles.length,
    searches: {
      fulltext_taco: fullTextFiles.length,
      fulltext_heytaco: heyTacoFiles.length,
      name_taco: nameFiles.length,
      fulltext_taqueria: taqueriaFiles.length,
      trashed_taco: trashedFiles.length
    },
    files: allFiles.map(f => ({
      id: f.id,
      name: f.name,
      mimeType: f.mimeType,
      createdTime: f.createdTime,
      modifiedTime: f.modifiedTime,
      webViewLink: f.webViewLink,
      owner: f.owners ? f.owners.map(o => ({ name: o.displayName, email: o.emailAddress })) : [],
      lastModifiedBy: f.lastModifyingUser ? { name: f.lastModifyingUser.displayName, email: f.lastModifyingUser.emailAddress } : null,
      shared: f.shared || false
    }))
  };

  const outputPath = require('path').join(__dirname, '..', 'output', 'drive_taco_search.json');
  require('fs').mkdirSync(require('path').dirname(outputPath), { recursive: true });
  require('fs').writeFileSync(outputPath, JSON.stringify(output, null, 2));
  console.log(`\nResults saved to: ${outputPath}`);
}

main().catch(err => {
  console.error('FATAL:', err.message);
  if (err.message.includes('invalid_grant')) {
    console.error('The refresh token may have expired. Run: node scripts/get-google-token.js');
  }
  process.exit(1);
});
