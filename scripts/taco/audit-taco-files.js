const { google } = require('googleapis');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });

const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET
);
oauth2Client.setCredentials({ refresh_token: process.env.GOOGLE_REFRESH_TOKEN });

const drive = google.drive({ version: 'v3', auth: oauth2Client });
const driveActivity = google.driveactivity({ version: 'v2', auth: oauth2Client });

const FILES = [
  { id: '17nkJmfsgspJtzGX4qOhaapSErDKHBm8P', name: 'HEYTACO_DISRUPTIVE_PROPOSALS.md' },
  { id: '10H389iKAGwzXZIMdfrmi7pdM5YRzcFFb', name: 'HeyTaco_Guia_Produtividade.md' },
  { id: '1CyBTrmO1garleObdoecZC0qkubZMyjhv', name: 'alexandra_dm_full.txt' },
];

// Try Drive Activity API (view history)
async function getFileActivity(fileId, fileName) {
  console.log(`\n${'='.repeat(70)}`);
  console.log(`ACTIVITY LOG: ${fileName}`);
  console.log(`File ID: ${fileId}`);
  console.log('='.repeat(70));

  try {
    const res = await driveActivity.activity.query({
      requestBody: {
        itemName: `items/${fileId}`,
        pageSize: 50,
      }
    });

    const activities = res.data.activities || [];
    console.log(`Total activities found: ${activities.length}\n`);

    for (const act of activities) {
      const time = act.timestamp || (act.timeRange ? act.timeRange.endTime : 'unknown');

      // Get actors
      const actors = (act.actors || []).map(a => {
        if (a.user && a.user.knownUser) return `user:${a.user.knownUser.personName}`;
        if (a.user && a.user.deletedUser) return 'deleted_user';
        if (a.user && a.user.unknownUser) return 'unknown_user';
        if (a.administrator) return 'admin';
        if (a.system) return 'system';
        if (a.impersonation) return 'impersonation';
        return JSON.stringify(a);
      });

      // Get action type
      const detail = act.primaryActionDetail || {};
      let actionType = Object.keys(detail)[0] || 'unknown';

      // Get targets
      const targets = (act.targets || []).map(t => {
        if (t.driveItem) return t.driveItem.title || t.driveItem.name;
        if (t.fileComment) return `comment on ${t.fileComment.parent?.title || 'file'}`;
        return JSON.stringify(t);
      });

      console.log(`  [${time}]`);
      console.log(`    Action: ${actionType}`);
      console.log(`    Actor(s): ${actors.join(', ')}`);
      if (targets.length) console.log(`    Target: ${targets.join(', ')}`);
      console.log('');
    }

    return activities;
  } catch (err) {
    console.log(`Drive Activity API error: ${err.message}`);
    console.log(`Status: ${err.status || 'N/A'}`);

    if (err.message.includes('not enabled') || err.message.includes('403') || err.message.includes('accessNotConfigured')) {
      console.log('\n>> Drive Activity API not enabled. Trying revisions + comments fallback...\n');
      return null;
    }
    return null;
  }
}

// Fallback: revisions
async function getRevisions(fileId, fileName) {
  console.log(`\n  REVISIONS:`);
  try {
    const res = await drive.revisions.list({
      fileId,
      fields: 'revisions(id, modifiedTime, lastModifyingUser, size)',
      pageSize: 100
    });
    const revs = res.data.revisions || [];
    console.log(`  Total revisions: ${revs.length}`);
    for (const r of revs) {
      const user = r.lastModifyingUser
        ? `${r.lastModifyingUser.displayName} <${r.lastModifyingUser.emailAddress}>`
        : 'unknown';
      console.log(`    [${r.modifiedTime}] by ${user}`);
    }
    return revs;
  } catch (err) {
    console.log(`    Error: ${err.message}`);
    return [];
  }
}

// Fallback: comments
async function getComments(fileId, fileName) {
  console.log(`\n  COMMENTS:`);
  try {
    const res = await drive.comments.list({
      fileId,
      fields: 'comments(id, content, author, createdTime, modifiedTime, resolved, replies, quotedFileContent)',
      includeDeleted: true
    });
    const comments = res.data.comments || [];
    if (comments.length === 0) {
      console.log(`    No comments.`);
      return [];
    }
    for (const c of comments) {
      console.log(`    [${c.createdTime}] ${c.author.displayName}: "${c.content}"`);
      if (c.replies) {
        for (const r of c.replies) {
          console.log(`      Reply [${r.createdTime}] ${r.author.displayName}: "${r.content}"`);
        }
      }
    }
    return comments;
  } catch (err) {
    console.log(`    Error: ${err.message}`);
    return [];
  }
}

// File metadata with view count
async function getFileMetadata(fileId, fileName) {
  console.log(`\n  METADATA:`);
  try {
    const res = await drive.files.get({
      fileId,
      fields: 'id,name,viewedByMe,viewedByMeTime,viewersCanCopyContent,shared,sharingUser,lastModifyingUser,modifiedTime,createdTime,ownedByMe,permissions,contentHints,quotaBytesUsed'
    });
    const f = res.data;
    console.log(`    Created: ${f.createdTime}`);
    console.log(`    Modified: ${f.modifiedTime}`);
    console.log(`    Last modifier: ${f.lastModifyingUser?.displayName} <${f.lastModifyingUser?.emailAddress}>`);
    console.log(`    Viewed by me: ${f.viewedByMe} (last: ${f.viewedByMeTime})`);
    console.log(`    Shared: ${f.shared}`);
    if (f.sharingUser) console.log(`    Shared by: ${f.sharingUser.displayName} <${f.sharingUser.emailAddress}>`);
    console.log(`    Size: ${f.quotaBytesUsed} bytes`);
    return f;
  } catch (err) {
    console.log(`    Error: ${err.message}`);
    return null;
  }
}

async function main() {
  console.log('TACO FILES - FULL AUDIT LOG');
  console.log(`Timestamp: ${new Date().toISOString()}\n`);

  for (const f of FILES) {
    const activities = await getFileActivity(f.id, f.name);

    // Always run fallbacks for extra data
    await getFileMetadata(f.id, f.name);
    await getRevisions(f.id, f.name);
    await getComments(f.id, f.name);
  }

  console.log('\n\nDone.');
}

main().catch(err => console.error('FATAL:', err.message));
