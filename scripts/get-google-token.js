const { google } = require("googleapis");
const http = require("http");
const url = require("url");

const CLIENT_ID = "YOUR_CLIENT_ID";
const CLIENT_SECRET = "YOUR_CLIENT_SECRET";
const REDIRECT_URI = "http://localhost:3000/callback";
const SCOPES = ["https://www.googleapis.com/auth/drive.readonly"];

const oauth2Client = new google.auth.OAuth2(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI);

const authUrl = oauth2Client.generateAuthUrl({
  access_type: "offline",
  scope: SCOPES,
  prompt: "consent",
});

console.log("Open this URL in your browser:");
console.log(authUrl);
console.log("");
console.log("Waiting for callback on http://localhost:3000 ...");

const server = http.createServer(async (req, res) => {
  const queryParams = url.parse(req.url, true).query;
  if (queryParams.code) {
    try {
      const { tokens } = await oauth2Client.getToken(queryParams.code);
      console.log("SUCCESS! Refresh token:");
      console.log(tokens.refresh_token);
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end("<h1>Success!</h1><p>Check terminal.</p>");
      setTimeout(() => process.exit(0), 1000);
    } catch (e) {
      console.error("Error:", e.message);
      res.end("Error");
    }
  }
});

server.listen(3000);