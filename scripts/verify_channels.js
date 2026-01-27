const https = require('https');
require('dotenv').config({ path: '../.env' });

const token = process.env.SLACK_USER_TOKEN;
const channelsToFind = ['customer-requests', 'tsa-internal', 'escalations', 'tsa-bugs'];

const options = {
  hostname: 'slack.com',
  path: '/api/conversations.list?types=public_channel,private_channel&limit=500',
  headers: { 'Authorization': `Bearer ${token}` }
};

https.get(options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const result = JSON.parse(data);
    if (!result.ok) {
      console.log('Error:', result.error);
      return;
    }

    console.log('=== SLACK CHANNEL VERIFICATION ===\n');

    channelsToFind.forEach(name => {
      const exact = result.channels.find(c => c.name === name);
      const partial = result.channels.filter(c => c.name.includes(name.replace('-', '')));

      if (exact) {
        console.log(`✅ #${name} - EXISTS`);
      } else if (partial.length > 0) {
        console.log(`⚠️ #${name} - NOT FOUND, but similar: ${partial.map(c => '#' + c.name).join(', ')}`);
      } else {
        console.log(`❌ #${name} - NOT FOUND`);
      }
    });

    console.log('\n=== ALL CHANNELS WITH "TSA" ===');
    result.channels.filter(c => c.name.toLowerCase().includes('tsa')).forEach(c => {
      console.log(`  #${c.name}`);
    });

    console.log('\n=== ALL CHANNELS WITH "ESCALAT" ===');
    result.channels.filter(c => c.name.toLowerCase().includes('escalat')).forEach(c => {
      console.log(`  #${c.name}`);
    });

    console.log('\n=== ALL CHANNELS WITH "CUSTOMER" ===');
    result.channels.filter(c => c.name.toLowerCase().includes('customer')).forEach(c => {
      console.log(`  #${c.name}`);
    });
  });
});
