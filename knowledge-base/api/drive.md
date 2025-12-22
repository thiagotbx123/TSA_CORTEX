# Google Drive API - TSA_CORTEX

## Visão Geral

Usamos a [googleapis](https://www.npmjs.com/package/googleapis) para coletar metadados de arquivos do Google Drive.

## Autenticação OAuth2

```typescript
import { google } from 'googleapis';

const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET
);

oauth2Client.setCredentials({
  refresh_token: process.env.GOOGLE_REFRESH_TOKEN,
});

const drive = google.drive({ version: 'v3', auth: oauth2Client });
```

## Escopos Necessários

```
https://www.googleapis.com/auth/drive.readonly
https://www.googleapis.com/auth/drive.metadata.readonly
```

## Endpoints Utilizados

### files.list
Lista arquivos modificados em um período.
```typescript
const response = await drive.files.list({
  q: `modifiedTime >= '${startDate}' and modifiedTime <= '${endDate}' and trashed = false`,
  fields: 'nextPageToken, files(id, name, mimeType, createdTime, modifiedTime, webViewLink, owners, parents, size)',
  pageSize: 100,
  pageToken: nextPageToken,
});
```

### files.get
Obtém detalhes de um arquivo específico.
```typescript
const response = await drive.files.get({
  fileId: fileId,
  fields: 'id, name, mimeType, createdTime, modifiedTime, webViewLink, owners, parents, size',
});
```

## Query Syntax

```
# Arquivos modificados no período
modifiedTime >= '2024-12-01T00:00:00' and modifiedTime <= '2024-12-22T23:59:59'

# Excluir lixeira
trashed = false

# Excluir pastas específicas
not 'folderId' in parents

# Por tipo MIME
mimeType = 'application/vnd.google-apps.document'
```

## Tipos MIME Comuns

| Tipo | MIME |
|------|------|
| Docs | application/vnd.google-apps.document |
| Sheets | application/vnd.google-apps.spreadsheet |
| Slides | application/vnd.google-apps.presentation |
| Forms | application/vnd.google-apps.form |
| Folders | application/vnd.google-apps.folder |

## Estrutura de Dados

```typescript
interface DriveFile {
  id: string;
  name: string;
  mimeType: string;
  createdTime: string;
  modifiedTime: string;
  webViewLink: string;
  owners?: Array<{
    displayName: string;
    emailAddress: string;
  }>;
  parents?: string[];
  size?: string;
}
```

## Rate Limits

- 12000 queries/min por usuário
- 1000 queries/100seg por usuário

## Como Obter Refresh Token

1. Criar projeto no Google Cloud Console
2. Habilitar Drive API
3. Criar credenciais OAuth2
4. Usar OAuth Playground ou script para obter refresh token

## Referências

- [Drive API Docs](https://developers.google.com/drive/api/v3/reference)
- [Node.js Quickstart](https://developers.google.com/drive/api/quickstart/nodejs)
