#!/usr/bin/env python3
"""Deploy DBBuilder.gs.js to Apps Script and run buildDB."""
import os, json
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()

SCRIPT_ID = '1RkaFVSPODWbruk9I1iKW1i4Nh3zp7WRiPtXIWadpuQovur6xC9KKFVQX'
GS_FILE = os.path.join(os.path.dirname(__file__), 'DBBuilder.gs.js')

creds = Credentials(
    token=None,
    refresh_token=os.getenv('GOOGLE_REFRESH_TOKEN'),
    token_uri='https://oauth2.googleapis.com/token',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    scopes=[
        'https://www.googleapis.com/auth/script.projects',
        'https://www.googleapis.com/auth/spreadsheets'
    ]
)

service = build('script', 'v1', credentials=creds)

# Read current code
with open(GS_FILE, 'r', encoding='utf-8') as f:
    code = f.read()

print(f"Code length: {len(code)} chars")

# Get current project content to preserve manifest
try:
    content = service.projects().getContent(scriptId=SCRIPT_ID).execute()
    print(f"Current files: {[f['name'] for f in content.get('files', [])]}")
except Exception as e:
    print(f"Warning getting content: {e}")
    content = {'files': []}

# Build new files list - keep manifest, replace/add Code.gs
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
            "runtimeVersion": "V8"
        })
    })

new_files.append({
    'name': 'Code',
    'type': 'SERVER_JS',
    'source': code
})

# Update project
print("Deploying to Apps Script...")
result = service.projects().updateContent(
    scriptId=SCRIPT_ID,
    body={'files': new_files}
).execute()
print(f"Deployed! Files: {[f['name'] for f in result.get('files', [])]}")

# Run buildDB
print("\nRunning buildDB...")
try:
    run_result = service.scripts().run(
        scriptId=SCRIPT_ID,
        body={'function': 'buildDB'}
    ).execute()
    if 'error' in run_result:
        print(f"Error: {run_result['error']}")
    else:
        print("buildDB completed successfully!")
except Exception as e:
    print(f"Run error (may need Apps Script API enabled): {e}")
    print("You can run buildDB manually from the spreadsheet menu.")
