/**
 * Detailed Worklog Generator
 * Collects ALL messages from target channels and DMs, generates comprehensive report
 */

const { WebClient } = require('@slack/web-api');
const { LinearClient } = require('@linear/sdk');
const { google } = require('googleapis');
const fs = require('fs');
require('dotenv').config();

const TARGET_CHANNELS = [
  'intuit-internal',
  'testbox-intuit-wfs-external20251027',
  'testbox-intuit-mailchimp-external',
  'external-testbox-apollo',
  'dev-on-call',
  'product',
  'go-to-market',
  'tsa-data-engineers',
  'team-koala',
  'brevo-internal',
  'archer-internal',
];

async function collectSlackMessages(startDate, endDate) {
  const client = new WebClient(process.env.SLACK_USER_TOKEN);
  const allMessages = [];

  console.log('\\n=== COLLECTING SLACK ===');

  // Collect from target channels
  for (const channel of TARGET_CHANNELS) {
    const query = `in:#${channel} after:${startDate} before:${endDate}`;
    let page = 1;
    let channelMessages = [];

    while (page <= 20) {
      try {
        const result = await client.search.messages({
          query,
          count: 100,
          page,
          sort: 'timestamp',
          sort_dir: 'asc'
        });

        if (!result.messages?.matches?.length) break;

        for (const msg of result.messages.matches) {
          channelMessages.push({
            channel: channel,
            user: msg.username || msg.user,
            text: msg.text || '',
            ts: msg.ts,
            permalink: msg.permalink,
            timestamp: new Date(parseFloat(msg.ts) * 1000)
          });
        }

        const totalPages = Math.ceil((result.messages.total || 0) / 100);
        if (page >= totalPages) break;
        page++;
        await new Promise(r => setTimeout(r, 100));
      } catch (e) {
        break;
      }
    }

    console.log(`  #${channel}: ${channelMessages.length} messages`);
    allMessages.push(...channelMessages);
  }

  // Collect DMs
  const dmQuery = `is:dm after:${startDate} before:${endDate}`;
  let page = 1;
  let dmMessages = [];

  while (page <= 20) {
    try {
      const result = await client.search.messages({
        query: dmQuery,
        count: 100,
        page,
        sort: 'timestamp',
        sort_dir: 'asc'
      });

      if (!result.messages?.matches?.length) break;

      for (const msg of result.messages.matches) {
        dmMessages.push({
          channel: 'DM',
          user: msg.username || msg.user,
          text: msg.text || '',
          ts: msg.ts,
          permalink: msg.permalink,
          timestamp: new Date(parseFloat(msg.ts) * 1000)
        });
      }

      const totalPages = Math.ceil((result.messages.total || 0) / 100);
      if (page >= totalPages) break;
      page++;
      await new Promise(r => setTimeout(r, 100));
    } catch (e) {
      break;
    }
  }

  console.log(`  DMs: ${dmMessages.length} messages`);
  allMessages.push(...dmMessages);

  // Collect messages from me
  const fromMeQuery = `from:me after:${startDate} before:${endDate}`;
  page = 1;
  let myMessages = [];

  while (page <= 20) {
    try {
      const result = await client.search.messages({
        query: fromMeQuery,
        count: 100,
        page,
        sort: 'timestamp',
        sort_dir: 'asc'
      });

      if (!result.messages?.matches?.length) break;

      for (const msg of result.messages.matches) {
        const exists = allMessages.some(m => m.ts === msg.ts);
        if (!exists) {
          myMessages.push({
            channel: msg.channel?.name || 'other',
            user: msg.username || msg.user,
            text: msg.text || '',
            ts: msg.ts,
            permalink: msg.permalink,
            timestamp: new Date(parseFloat(msg.ts) * 1000)
          });
        }
      }

      const totalPages = Math.ceil((result.messages.total || 0) / 100);
      if (page >= totalPages) break;
      page++;
      await new Promise(r => setTimeout(r, 100));
    } catch (e) {
      break;
    }
  }

  console.log(`  From me (other channels): ${myMessages.length} messages`);
  allMessages.push(...myMessages);

  console.log(`  TOTAL SLACK: ${allMessages.length} messages`);
  return allMessages;
}

async function collectLinearActivity(startDate, endDate) {
  const client = new LinearClient({ apiKey: process.env.LINEAR_API_KEY });
  const activities = [];

  console.log('\\n=== COLLECTING LINEAR ===');

  try {
    const me = await client.viewer;
    console.log(`  User: ${me.name}`);

    // Get all issues where user is involved
    const issues = await client.issues({
      filter: {
        or: [
          { creator: { id: { eq: me.id } } },
          { assignee: { id: { eq: me.id } } }
        ],
        updatedAt: {
          gte: new Date(startDate),
          lte: new Date(endDate)
        }
      },
      first: 100
    });

    for (const issue of issues.nodes) {
      const state = await issue.state;
      const comments = await issue.comments({ first: 50 });

      activities.push({
        type: 'issue',
        identifier: issue.identifier,
        title: issue.title,
        description: issue.description,
        state: state?.name,
        url: issue.url,
        createdAt: issue.createdAt,
        updatedAt: issue.updatedAt,
        comments: comments.nodes.map(c => ({
          body: c.body,
          createdAt: c.createdAt
        }))
      });
    }

    console.log(`  Issues: ${activities.length}`);
  } catch (e) {
    console.log(`  Error: ${e.message}`);
  }

  return activities;
}

async function collectDriveFiles(startDate, endDate) {
  const files = [];

  console.log('\\n=== COLLECTING DRIVE ===');

  try {
    const auth = new google.auth.OAuth2(
      process.env.GOOGLE_CLIENT_ID,
      process.env.GOOGLE_CLIENT_SECRET
    );
    auth.setCredentials({ refresh_token: process.env.GOOGLE_REFRESH_TOKEN });

    const drive = google.drive({ version: 'v3', auth });

    const response = await drive.files.list({
      q: `modifiedTime >= '${startDate}T00:00:00' and modifiedTime <= '${endDate}T23:59:59' and trashed = false`,
      fields: 'files(id, name, mimeType, modifiedTime, webViewLink)',
      orderBy: 'modifiedTime desc',
      pageSize: 200
    });

    for (const file of response.data.files || []) {
      files.push({
        name: file.name,
        type: file.mimeType,
        modifiedTime: file.modifiedTime,
        url: file.webViewLink
      });
    }

    console.log(`  Files: ${files.length}`);
  } catch (e) {
    console.log(`  Error: ${e.message}`);
  }

  return files;
}

function generateDetailedWorklog(slackMessages, linearActivity, driveFiles, startDate, endDate) {
  const lines = [];

  lines.push('# DETAILED WORKLOG REPORT');
  lines.push('');
  lines.push(`**Period:** ${startDate} to ${endDate}`);
  lines.push(`**Generated:** ${new Date().toISOString()}`);
  lines.push('');
  lines.push('---');
  lines.push('');

  // Group messages by day
  const messagesByDay = {};
  for (const msg of slackMessages) {
    const day = msg.timestamp.toISOString().split('T')[0];
    if (!messagesByDay[day]) messagesByDay[day] = [];
    messagesByDay[day].push(msg);
  }

  // Sort days
  const sortedDays = Object.keys(messagesByDay).sort();

  // Detailed day-by-day breakdown
  lines.push('## DAILY ACTIVITY BREAKDOWN');
  lines.push('');

  for (const day of sortedDays) {
    const dayDate = new Date(day + 'T12:00:00');
    const dayName = dayDate.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });

    lines.push(`### ${dayName}`);
    lines.push('');

    const dayMessages = messagesByDay[day].sort((a, b) => a.timestamp - b.timestamp);

    // Group by channel
    const byChannel = {};
    for (const msg of dayMessages) {
      if (!byChannel[msg.channel]) byChannel[msg.channel] = [];
      byChannel[msg.channel].push(msg);
    }

    for (const [channel, msgs] of Object.entries(byChannel)) {
      lines.push(`#### #${channel} (${msgs.length} messages)`);
      lines.push('');

      for (const msg of msgs) {
        const time = msg.timestamp.toTimeString().slice(0, 5);
        const text = (msg.text || '').replace(/<[^>]+>/g, '').substring(0, 500);
        const link = msg.permalink ? ` [view](${msg.permalink})` : '';

        lines.push(`- **${time}** ${text}${link}`);
      }
      lines.push('');
    }
  }

  // Linear activity
  if (linearActivity.length > 0) {
    lines.push('---');
    lines.push('');
    lines.push('## LINEAR ACTIVITY');
    lines.push('');

    for (const issue of linearActivity) {
      lines.push(`### [${issue.identifier}] ${issue.title}`);
      lines.push('');
      lines.push(`**Status:** ${issue.state}`);
      lines.push(`**URL:** ${issue.url}`);
      lines.push('');

      if (issue.description) {
        lines.push('**Description:**');
        lines.push(issue.description.substring(0, 1000));
        lines.push('');
      }

      if (issue.comments?.length > 0) {
        lines.push('**Comments:**');
        for (const comment of issue.comments.slice(0, 5)) {
          lines.push(`- ${comment.body?.substring(0, 300)}`);
        }
        lines.push('');
      }
    }
  }

  // Drive files
  if (driveFiles.length > 0) {
    lines.push('---');
    lines.push('');
    lines.push('## MODIFIED FILES');
    lines.push('');

    // Group by day
    const filesByDay = {};
    for (const file of driveFiles) {
      const day = file.modifiedTime.split('T')[0];
      if (!filesByDay[day]) filesByDay[day] = [];
      filesByDay[day].push(file);
    }

    for (const [day, files] of Object.entries(filesByDay).sort()) {
      lines.push(`### ${day}`);
      lines.push('');
      for (const file of files) {
        const link = file.url ? ` [open](${file.url})` : '';
        lines.push(`- ${file.name}${link}`);
      }
      lines.push('');
    }
  }

  // Summary statistics
  lines.push('---');
  lines.push('');
  lines.push('## SUMMARY');
  lines.push('');
  lines.push(`- **Slack Messages:** ${slackMessages.length}`);
  lines.push(`- **Linear Issues:** ${linearActivity.length}`);
  lines.push(`- **Drive Files:** ${driveFiles.length}`);
  lines.push(`- **Days Covered:** ${sortedDays.length}`);

  return lines.join('\\n');
}

async function main() {
  const startDate = process.argv[2] || '2025-12-10';
  const endDate = process.argv[3] || '2025-12-18';

  console.log(`\\nGenerating detailed worklog for ${startDate} to ${endDate}`);

  const slackMessages = await collectSlackMessages(startDate, endDate);
  const linearActivity = await collectLinearActivity(startDate, endDate);
  const driveFiles = await collectDriveFiles(startDate, endDate);

  const worklog = generateDetailedWorklog(slackMessages, linearActivity, driveFiles, startDate, endDate);

  const filename = `output/detailed_worklog_${startDate}_${endDate}.md`;
  fs.writeFileSync(filename, worklog);
  console.log(`\\nSaved to: ${filename}`);
  console.log(`\\nPreview (first 3000 chars):\\n`);
  console.log(worklog.substring(0, 3000));
}

main().catch(console.error);
