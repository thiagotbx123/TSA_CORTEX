/**
 * Script para obter Google OAuth Refresh Token
 *
 * Uso:
 * 1. Configure GOOGLE_CLIENT_ID e GOOGLE_CLIENT_SECRET no .env
 * 2. Execute: node scripts/get-google-token.js
 * 3. Abra a URL no navegador e autorize
 * 4. Copie o refresh_token exibido
 */

require('dotenv').config();
const { google } = require("googleapis");
const http = require("http");
const url = require("url");

const CLIENT_ID = process.env.GOOGLE_CLIENT_ID;
const CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET;
const REDIRECT_URI = "http://localhost:3000/callback";
const SCOPES = ["https://www.googleapis.com/auth/drive.readonly"];

if (!CLIENT_ID || !CLIENT_SECRET) {
  console.error("ERROR: Configure GOOGLE_CLIENT_ID e GOOGLE_CLIENT_SECRET no .env primeiro!");
  console.error("");
  console.error("Passos:");
  console.error("1. Acesse https://console.cloud.google.com");
  console.error("2. Crie credenciais OAuth (Desktop app)");
  console.error("3. Adicione ao .env:");
  console.error("   GOOGLE_CLIENT_ID=seu-client-id.apps.googleusercontent.com");
  console.error("   GOOGLE_CLIENT_SECRET=GOCSPX-sua-secret");
  process.exit(1);
}

const oauth2Client = new google.auth.OAuth2(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI);

const authUrl = oauth2Client.generateAuthUrl({
  access_type: "offline",
  scope: SCOPES,
  prompt: "consent",
});

console.log("===========================================");
console.log("Google OAuth - Obter Refresh Token");
console.log("===========================================");
console.log("");
console.log("1. Abra esta URL no navegador:");
console.log("");
console.log(authUrl);
console.log("");
console.log("2. Autorize o acesso ao Google Drive");
console.log("3. O refresh_token aparecera aqui");
console.log("");
console.log("Aguardando callback em http://localhost:3000 ...");

const server = http.createServer(async (req, res) => {
  const queryParams = url.parse(req.url, true).query;
  if (queryParams.code) {
    try {
      const { tokens } = await oauth2Client.getToken(queryParams.code);
      console.log("");
      console.log("===========================================");
      console.log("SUCESSO! Adicione ao seu .env:");
      console.log("===========================================");
      console.log("");
      console.log("GOOGLE_REFRESH_TOKEN=" + tokens.refresh_token);
      console.log("");
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end("<h1>Sucesso!</h1><p>Volte ao terminal para copiar o refresh_token.</p>");
      setTimeout(() => process.exit(0), 1000);
    } catch (e) {
      console.error("Erro:", e.message);
      res.end("Erro - verifique o terminal");
    }
  }
});

server.listen(3000);
