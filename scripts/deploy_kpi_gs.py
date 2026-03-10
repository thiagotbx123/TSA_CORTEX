#!/usr/bin/env python3
"""Deploy KPIDrillDown.gs.js to the KPI_Team_Raccoons spreadsheet's Apps Script project."""
import os, json, sys
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()

KPI_SPREADSHEET_ID = '1SPyvjXW9OJ4_CywHqroRwKbSbdGI98O0xxkc4y1Sy9w'
GS_FILE = os.path.join(os.path.dirname(__file__), 'KPIDrillDown.gs.js')

creds = Credentials(
    token=None,
    refresh_token=os.getenv('GOOGLE_REFRESH_TOKEN'),
    token_uri='https://oauth2.googleapis.com/token',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    scopes=[
        'https://www.googleapis.com/auth/script.projects',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
)

script_service = build('script', 'v1', credentials=creds)

# Read the GS code
with open(GS_FILE, 'r', encoding='utf-8') as f:
    code = f.read()
print(f"Code length: {len(code)} chars")

# Try to find existing script project bound to this spreadsheet
# The Apps Script API doesn't have a direct "list by parent" method,
# so we either need a known script ID or create a new project.
SCRIPT_ID_FILE = os.path.join(os.path.dirname(__file__), '.kpi_script_id')

script_id = None
if os.path.exists(SCRIPT_ID_FILE):
    with open(SCRIPT_ID_FILE, 'r') as f:
        script_id = f.read().strip()
    print(f"Found existing script ID: {script_id}")

if not script_id:
    # Create a new Apps Script project bound to the spreadsheet
    print("Creating new Apps Script project bound to KPI spreadsheet...")
    try:
        project = script_service.projects().create(body={
            'title': 'KPI Drill-Down',
            'parentId': KPI_SPREADSHEET_ID
        }).execute()
        script_id = project['scriptId']
        print(f"Created project: {script_id}")
        # Save for future deployments
        with open(SCRIPT_ID_FILE, 'w') as f:
            f.write(script_id)
    except Exception as e:
        print(f"Error creating project: {e}")
        print("\nIf this fails, you can manually create the project:")
        print("1. Open the KPI spreadsheet")
        print("2. Extensions > Apps Script")
        print("3. Copy the script ID from the URL (between /d/ and /edit)")
        print(f"4. Save it to: {SCRIPT_ID_FILE}")
        sys.exit(1)

# Get current project content to preserve manifest
try:
    content = script_service.projects().getContent(scriptId=script_id).execute()
    print(f"Current files: {[f['name'] for f in content.get('files', [])]}")
except Exception as e:
    print(f"Warning getting content: {e}")
    content = {'files': []}

# Build new files list
new_files = []
manifest_found = False
for f in content.get('files', []):
    if f['name'] == 'appsscript':
        new_files.append(f)
        manifest_found = True

if not manifest_found:
    new_files.append({
        'name': 'appsscript',
        'type': 'JSON',
        'source': json.dumps({
            "timeZone": "America/New_York",
            "dependencies": {},
            "exceptionLogging": "STACKDRIVER",
            "runtimeVersion": "V8",
            "oauthScopes": [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/script.container.ui"
            ]
        })
    })

new_files.append({
    'name': 'Code',
    'type': 'SERVER_JS',
    'source': code
})

# Deploy
print("Deploying to Apps Script...")
try:
    result = script_service.projects().updateContent(
        scriptId=script_id,
        body={'files': new_files}
    ).execute()
    print(f"Deployed! Files: {[f['name'] for f in result.get('files', [])]}")
    print(f"\nScript ID: {script_id}")
    print("Reload the KPI spreadsheet to see the '⚡ KPI Tools' menu.")
except Exception as e:
    print(f"Deploy error: {e}")
    sys.exit(1)
