r"""
KPI Dashboard — System Tray Server
Runs pipeline, starts HTTP server + ngrok, sits in system tray.
Icon: green = all healthy, yellow = partial, red = both down.
"""
import sys
import os
import io

# pythonw has no stdout/stderr — redirect to log file before anything else
_LOG_DIR = os.path.join(os.path.expanduser('~'), 'Downloads', 'kpi-serve')
_LOG_PATH = os.path.join(_LOG_DIR, 'kpi_tray.log')
try:
    os.makedirs(_LOG_DIR, exist_ok=True)
except Exception:
    pass

def _safe_stream():
    """Ensure stdout/stderr are writable — pythonw sets them to None."""
    for attr in ('stdout', 'stderr'):
        stream = getattr(sys, attr, None)
        if stream is None:
            try:
                f = open(_LOG_PATH, 'a', encoding='utf-8')
            except Exception:
                f = io.StringIO()
            setattr(sys, attr, f)
        else:
            try:
                stream.reconfigure(encoding='utf-8', errors='replace')
            except Exception:
                pass

_safe_stream()

import subprocess
import threading
import time
import signal
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
from functools import partial

import pystray
from PIL import Image, ImageDraw, ImageFont


# ─── Single Instance (PID lockfile) ───
_LOCK_PATH = os.path.join(os.path.expanduser('~'), 'Downloads', 'kpi-serve', 'kpi_tray.pid')

def _kill_old_instance():
    """Kill previous tray instance if its PID file exists."""
    if os.path.exists(_LOCK_PATH):
        try:
            old_pid = int(open(_LOCK_PATH).read().strip())
            if old_pid != os.getpid():
                subprocess.run(['taskkill', '/F', '/PID', str(old_pid)],
                               capture_output=True, timeout=5)
                time.sleep(1)
        except Exception:
            pass
    # Write our PID
    os.makedirs(os.path.dirname(_LOCK_PATH), exist_ok=True)
    with open(_LOCK_PATH, 'w') as f:
        f.write(str(os.getpid()))

_kill_old_instance()

# ─── Config ───
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVE_DIR = os.path.join(os.path.expanduser('~'), 'Downloads', 'kpi-serve')
DASHBOARD_SRC = os.path.join(os.path.expanduser('~'), 'Downloads', 'KPI_DASHBOARD.html')
ORCHESTRATE = os.path.join(SCRIPT_DIR, 'orchestrate.py')
ICO_PATH = os.path.join(SCRIPT_DIR, 'kpi_dashboard.ico')
NGROK_URL = 'uneffused-hoyt-unpunctually.ngrok-free.dev'
PUBLIC_URL = f'https://{NGROK_URL}/KPI_DASHBOARD.html'
HTTP_PORT = 8080
HEALTH_INTERVAL = 30  # seconds between health checks

# ─── State ───
http_server = None
ngrok_proc = None
tray_icon = None
status = {'http': False, 'ngrok': False, 'last_build': None}


# ─── Icon generation ───
def make_icon(color='green'):
    """Create a simple colored circle icon with KPI text."""
    colors = {'green': '#27AE60', 'yellow': '#F39C12', 'red': '#E74C3C', 'gray': '#95A5A6'}
    fill = colors.get(color, colors['gray'])
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Filled circle
    draw.ellipse([4, 4, 60, 60], fill=fill)
    # "K" letter in center
    try:
        font = ImageFont.truetype('segoeui.ttf', 30)
    except Exception:
        font = ImageFont.load_default()
    draw.text((32, 32), 'K', fill='white', font=font, anchor='mm')
    return img


def load_ico():
    """Try to load .ico file, fallback to generated icon."""
    try:
        return Image.open(ICO_PATH)
    except Exception:
        return make_icon('gray')


# ─── Health checks ───
def check_http():
    try:
        r = urllib.request.urlopen(f'http://localhost:{HTTP_PORT}/KPI_DASHBOARD.html', timeout=3)
        return r.status == 200
    except Exception:
        return False


def check_ngrok():
    try:
        r = urllib.request.urlopen('http://127.0.0.1:4040/api/tunnels', timeout=3)
        return r.status == 200
    except Exception:
        return False


def get_status_color():
    h, n = status['http'], status['ngrok']
    if h and n:
        return 'green'
    if h or n:
        return 'yellow'
    return 'red'


def get_status_text():
    h = 'OK' if status['http'] else 'DOWN'
    n = 'OK' if status['ngrok'] else 'DOWN'
    return f'KPI Dashboard  |  HTTP: {h}  |  ngrok: {n}'


# ─── Pipeline ───
def run_pipeline(full_refresh=False):
    """Run orchestrate.py to rebuild dashboard.
    full_refresh=False uses --skip-refresh (fast, <1s).
    full_refresh=True fetches fresh data from Linear API (~15s).
    """
    args = [sys.executable, ORCHESTRATE]
    if not full_refresh:
        args.append('--skip-refresh')
    try:
        r = subprocess.run(
            args, cwd=SCRIPT_DIR,
            capture_output=True, text=True, timeout=300
        )
        if r.returncode == 0:
            status['last_build'] = time.strftime('%H:%M')
            os.makedirs(SERVE_DIR, exist_ok=True)
            if os.path.exists(DASHBOARD_SRC):
                import shutil
                shutil.copy2(DASHBOARD_SRC, SERVE_DIR)
            return True
        else:
            print(f'Pipeline error:\n{r.stderr}')
            return False
    except Exception as e:
        print(f'Pipeline exception: {e}')
        return False


# ─── HTTP Server ───
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # silent

    def handle(self):
        try:
            super().handle()
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            pass


def start_http():
    global http_server
    if check_http():
        status['http'] = True
        return
    os.makedirs(SERVE_DIR, exist_ok=True)
    handler = partial(QuietHandler, directory=SERVE_DIR)
    try:
        http_server = HTTPServer(('0.0.0.0', HTTP_PORT), handler)
        t = threading.Thread(target=http_server.serve_forever, daemon=True)
        t.start()
        time.sleep(1)
        status['http'] = check_http()
    except OSError as e:
        print(f'HTTP server error: {e}')
        status['http'] = False


def stop_http():
    global http_server
    if http_server:
        http_server.shutdown()
        http_server = None
    status['http'] = False


# ─── ngrok ───
def start_ngrok():
    global ngrok_proc
    if check_ngrok():
        status['ngrok'] = True
        return
    try:
        ngrok_proc = subprocess.Popen(
            ['ngrok', 'http', f'--url={NGROK_URL}', str(HTTP_PORT)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        time.sleep(4)
        status['ngrok'] = check_ngrok()
    except FileNotFoundError:
        print('ngrok not found in PATH')
        status['ngrok'] = False


def stop_ngrok():
    global ngrok_proc
    if ngrok_proc:
        ngrok_proc.terminate()
        ngrok_proc = None
    status['ngrok'] = False


# ─── Health monitor ───
def health_loop():
    while True:
        time.sleep(HEALTH_INTERVAL)
        status['http'] = check_http()
        status['ngrok'] = check_ngrok()

        # Auto-restart if down
        if not status['http']:
            start_http()
        if not status['ngrok']:
            start_ngrok()

        # Update tray icon
        if tray_icon:
            tray_icon.icon = make_icon(get_status_color())
            tray_icon.title = get_status_text()


# ─── Tray menu actions ───
def on_open_dashboard(icon, item):
    os.startfile(PUBLIC_URL)


def on_open_local(icon, item):
    os.startfile(f'http://localhost:{HTTP_PORT}/KPI_DASHBOARD.html')


def on_refresh(icon, item):
    """Quick rebuild from cached data (<1s)."""
    def _refresh():
        icon.icon = make_icon('yellow')
        icon.title = 'KPI Dashboard  |  Rebuilding...'
        run_pipeline(full_refresh=False)
        status['http'] = check_http()
        status['ngrok'] = check_ngrok()
        icon.icon = make_icon(get_status_color())
        icon.title = get_status_text()
    threading.Thread(target=_refresh, daemon=True).start()


def on_full_refresh(icon, item):
    """Full refresh: fetch fresh data from Linear API (~15s)."""
    def _refresh():
        icon.icon = make_icon('yellow')
        icon.title = 'KPI Dashboard  |  Fetching Linear data...'
        run_pipeline(full_refresh=True)
        status['http'] = check_http()
        status['ngrok'] = check_ngrok()
        icon.icon = make_icon(get_status_color())
        icon.title = get_status_text()
    threading.Thread(target=_refresh, daemon=True).start()


def on_status(icon, item):
    pass  # status is shown in title on hover


def on_exit(icon, item):
    stop_ngrok()
    stop_http()
    icon.stop()


# ─── Main ───
def main():
    global tray_icon

    print('=' * 50)
    print('  KPI Dashboard — System Tray Server')
    print('=' * 50)

    # 1. Run pipeline
    print('\n[1/4] Running KPI pipeline...')
    run_pipeline()

    # 2. Start servers
    print('[2/4] Starting HTTP server + ngrok...')
    start_http()
    start_ngrok()

    # 3. Open dashboard in browser
    print('[3/4] Opening dashboard...')
    status['http'] = check_http()
    status['ngrok'] = check_ngrok()
    import webbrowser
    if status['http']:
        webbrowser.open(f'http://localhost:{HTTP_PORT}/KPI_DASHBOARD.html')
    elif os.path.exists(DASHBOARD_SRC):
        os.startfile(DASHBOARD_SRC)

    # 4. Launch tray icon
    print('[4/4] Launching system tray icon...')

    menu = pystray.Menu(
        pystray.MenuItem('Open Dashboard', on_open_dashboard, default=True),
        pystray.MenuItem('Open Local', on_open_local),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Rebuild (cached)', on_refresh),
        pystray.MenuItem('Full Refresh (Linear API)', on_full_refresh),
        pystray.MenuItem(lambda item: get_status_text(), on_status, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Exit', on_exit),
    )

    tray_icon = pystray.Icon(
        name='KPI Dashboard',
        icon=make_icon(get_status_color()),
        title=get_status_text(),
        menu=menu,
    )

    # Start health monitor
    threading.Thread(target=health_loop, daemon=True).start()

    h = 'OK' if status['http'] else 'FAIL'
    n = 'OK' if status['ngrok'] else 'FAIL'
    print(f'\n  HTTP: {h}  |  ngrok: {n}')
    print(f'  URL: {PUBLIC_URL}')
    print(f'\n  Tray icon active — right-click for options.')
    print('  Close from tray icon > Exit')

    # This blocks until icon.stop()
    tray_icon.run()


if __name__ == '__main__':
    main()
