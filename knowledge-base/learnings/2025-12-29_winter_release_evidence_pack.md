# Learning: Winter Release Evidence Pack - Complete Process

## Data: 2025-12-29
## Projeto: INTUIT-BOOM
## Tipo: Process Documentation + Technical Patterns

---

## 1. Screenshot Capture Process

### Problema
Screenshots iniciais capturados sem esperar carregamento resultavam em telas de loading.

### Solucao
```python
# Esperar DOM carregar
page.goto(url, wait_until="domcontentloaded", timeout=30000)

# Esperar conteudo renderizar (8-15 segundos dependendo da feature)
time.sleep(10)

# Verificar loading states
try:
    page.wait_for_selector(".loading, .spinner", state="detached", timeout=5000)
except:
    pass

# Screenshot
page.screenshot(path=filepath, full_page=False)
```

### Quality Assessment
```python
size_kb = os.path.getsize(filepath) // 1024

if size_kb >= 200: quality = "EXCELLENT"
elif size_kb >= 100: quality = "GOOD"
elif size_kb >= 50: quality = "ACCEPTABLE"
else: quality = "WEAK"  # Provavelmente loading screen
```

---

## 2. Google Drive API Integration

### Setup OAuth2
```python
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CREDS_FILE = "client_secret_*.json"
TOKEN_FILE = "token_drive.pickle"

# Primeira vez - abre browser para login
flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
creds = flow.run_local_server(port=0)

# Salvar token para uso futuro
with open(TOKEN_FILE, 'wb') as token:
    pickle.dump(creds, token)
```

### Listar Arquivos em Pasta
```python
drive = build('drive', 'v3', credentials=creds)

# Buscar subpasta
results = drive.files().list(
    q=f"'{folder_id}' in parents and name='TCO'",
    fields="files(id, name)"
).execute()

# Listar arquivos
results = drive.files().list(
    q=f"'{tco_id}' in parents and mimeType='image/png'",
    fields="files(id, name)",
    pageSize=50
).execute()

# Gerar links
for f in results.get('files', []):
    link = f"https://drive.google.com/file/d/{f['id']}/view?usp=drive_link"
```

---

## 3. Excel Hyperlinks com openpyxl

### Criar Hyperlink
```python
from openpyxl import load_workbook

wb = load_workbook(xlsx_path)
ws = wb.active

# Adicionar hyperlink
ws.cell(row=row, column=col).value = "Display Text"
ws.cell(row=row, column=col).hyperlink = "https://drive.google.com/..."
ws.cell(row=row, column=col).style = "Hyperlink"

wb.save(output_path)
```

### Google Sheets Formula (alternativa)
```
=HYPERLINK("url", "display_text")
```

---

## 4. Playwright CDP Connection

### Conectar a Browser Existente
```python
from playwright.sync_api import sync_playwright

p = sync_playwright().start()
browser = p.chromium.connect_over_cdp("http://localhost:9222")
context = browser.contexts[0]
page = context.pages[0]

# Criar nova aba
new_page = context.new_page()
new_page.goto(url)
```

### Iniciar Chrome com Debug
```bash
chrome.exe --remote-debugging-port=9222
```

---

## 5. File Organization Pattern

### Estrutura Local
```
intuit-boom/
├── EvidencePack/
│   └── WinterRelease/
│       ├── TCO/           # Screenshots finais (29)
│       └── archive/       # Screenshots antigos (41)
├── docs/
│   └── WINTER_RELEASE_VALIDATION_WITH_LINKS.xlsx
└── drive_links.json       # Mapeamento filename -> URL
```

### Estrutura Google Drive
```
08. Intuit/
└── 06. Winter Release/
    ├── WINTER_RELEASE_VALIDATION_WITH_LINKS.xlsx
    └── TCO/
        └── WR-001 a WR-029 screenshots
```

---

## 6. Credenciais e Tokens

### Localizacao
| Item | Path |
|------|------|
| OAuth Credentials | C:/Users/adm_r/Downloads/client_secret_486245165530-*.json |
| Drive Token | C:/Users/adm_r/token_drive.pickle |
| QBO Session | Browser CDP porta 9222 |

### Contas
| Servico | Email | Uso |
|---------|-------|-----|
| Google | thiago@testbox.com | Drive API, Sheets |
| QBO TCO | quickbooks-testuser-tco-tbxdemo@tbxofficial.com | Screenshots TCO |
| QBO Construction | quickbooks-test-account@tbxofficial.com | Screenshots Construction |

---

## 7. Metricas de Sucesso

### Winter Release TCO
- Features validadas: 29/29 (100%)
- Screenshots EXCELLENT: 17 (59%)
- Screenshots GOOD: 8 (28%)
- Screenshots N/A: 4 (13%)
- Hyperlinks funcionais: 29/29

### Tempo de Execucao
- Captura inicial: ~30 min
- Recaptura + analise: ~45 min
- Organizacao Drive: ~15 min
- Hyperlinks: ~10 min
- **Total: ~2 horas**

---

## 8. Proximos Passos

### Para CONSTRUCTION
1. Trocar para conta Construction no QBO
2. Identificar features aplicaveis (subset do Winter Release)
3. Capturar screenshots com mesmo processo
4. Criar pasta Construction no Drive
5. Gerar tracker com hyperlinks

### Reuso
- Token OAuth2 ja configurado
- Processo de captura documentado
- Scripts Python prontos para adaptar

---

## Tags
#winter-release #evidence-pack #google-drive-api #playwright #screenshots #hyperlinks #tco #intuit
