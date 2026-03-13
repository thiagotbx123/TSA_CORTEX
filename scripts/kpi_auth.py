"""Shared Google Sheets auth for KPI scripts. Reads credentials from .env."""
import os
import requests

def get_env():
    """Load .env from project root."""
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    env_vars[key.strip()] = val.strip()
    return env_vars

def get_access_token():
    """Get a fresh Google OAuth access token."""
    env = get_env()
    client_id = os.environ.get('GOOGLE_CLIENT_ID') or env.get('GOOGLE_CLIENT_ID', '')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET') or env.get('GOOGLE_CLIENT_SECRET', '')
    refresh_token = os.environ.get('GOOGLE_REFRESH_TOKEN') or env.get('GOOGLE_REFRESH_TOKEN', '')

    if not all([client_id, client_secret, refresh_token]):
        raise ValueError('Missing Google OAuth credentials. Check .env file.')

    resp = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    })
    return resp.json()['access_token']

# Sheet IDs
KPI_SHEET = '1SPyvjXW9OJ4_CywHqroRwKbSbdGI98O0xxkc4y1Sy9w'
SOURCE_SHEET = '1XaJgJCExt_dQ-RBY0eINP-0UCnCH7hYjGC3ibPlluzw'
THIAGO_SID = 165687443
THAIS_SID = 1989068677
MAP_SID = 1884049126
