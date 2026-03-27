"""Upload TSA KPI Dashboard HTML to 09. Raccoons Daily Routine on Google Drive.

Usage: python kpi/upload_dashboard_drive.py
- Creates file if not exists, updates if already there
- Searches in the Raccoons folder first, falls back to any location
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import os, json, requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from kpi_auth import get_access_token

DASHBOARD_FILE = os.path.join(os.path.expanduser('~'), 'Downloads', 'RACCOONS_KPI_DASHBOARD.html')
FILE_NAME = 'RACCOONS_KPI_DASHBOARD.html'
RACCOONS_FOLDER = '1TY3aoQHbZf8f21V_BoPEyw4aPF6mgZaV'  # TSA KPI Dashboard (shared with team)

token = get_access_token()
headers = {'Authorization': f'Bearer {token}'}

print(f"Target folder: 09. Raccoons Daily Routine")
print(f"File: {FILE_NAME}")

# Check if file already exists in the folder
search = requests.get(
    'https://www.googleapis.com/drive/v3/files',
    headers=headers,
    params={
        'q': f"name='{FILE_NAME}' and '{RACCOONS_FOLDER}' in parents and trashed=false",
        'fields': 'files(id,name,modifiedTime)'
    }
)
existing = search.json().get('files', [])

with open(DASHBOARD_FILE, 'rb') as f:
    content = f.read()
print(f"Size: {len(content)//1024}KB")

if existing:
    file_id = existing[0]['id']
    print(f"Updating existing ({existing[0].get('modifiedTime','')[:16]})...")
    resp = requests.patch(
        f'https://www.googleapis.com/upload/drive/v3/files/{file_id}',
        headers={**headers, 'Content-Type': 'text/html'},
        params={'uploadType': 'media'},
        data=content
    )
else:
    print("Creating new file...")
    metadata = json.dumps({
        'name': FILE_NAME,
        'parents': [RACCOONS_FOLDER],
        'mimeType': 'text/html'
    })
    resp = requests.post(
        'https://www.googleapis.com/upload/drive/v3/files',
        headers={**headers},
        params={'uploadType': 'multipart'},
        files={
            'metadata': ('metadata', metadata, 'application/json'),
            'file': (FILE_NAME, content, 'text/html')
        }
    )

result = resp.json()
if 'id' in result:
    print(f"\nDONE: https://drive.google.com/file/d/{result['id']}/view")
else:
    print(f"\nERROR: {result}")
    sys.exit(1)
