"""KPI Pipeline Orchestrator — runs the full pipeline in correct order.

Pipeline: refresh_linear_cache → merge_opossum_data → normalize_data → build_html_dashboard

Usage:
  python kpi/orchestrate.py          # Full pipeline (requires LINEAR_API_KEY)
  python kpi/orchestrate.py --skip-refresh  # Skip API refresh, use cached data
  python kpi/orchestrate.py --build-only    # Only rebuild dashboard from existing data

Can be scheduled via Windows Task Scheduler for automated daily runs.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import os, subprocess, time
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable

STEPS = [
    ('refresh_linear_cache.py', 'Refreshing Linear cache from API...'),
    ('merge_opossum_data.py', 'Merging Linear data into dashboard...'),
    ('normalize_data.py', 'Normalizing data quality...'),
    ('build_html_dashboard.py', 'Building HTML dashboard...'),
    ('upload_dashboard_drive.py', 'Uploading to Google Drive...'),
]


def run_step(script, description, cwd):
    """Run a pipeline step and return (success, duration, output)."""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"  Script: {script}")
    print(f"{'='*60}")

    script_path = os.path.join(SCRIPT_DIR, script)
    if not os.path.exists(script_path):
        print(f"  ERROR: Script not found: {script_path}")
        return False, 0, f"Script not found: {script_path}"

    start = time.time()
    try:
        result = subprocess.run(
            [PYTHON, script_path],
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=120,
        )
        duration = time.time() - start
        output = result.stdout + (('\nSTDERR: ' + result.stderr) if result.stderr else '')
        print(output)

        if result.returncode != 0:
            print(f"\n  FAILED (exit code {result.returncode}) in {duration:.1f}s")
            return False, duration, output
        else:
            print(f"\n  OK in {duration:.1f}s")
            return True, duration, output

    except subprocess.TimeoutExpired:
        duration = time.time() - start
        print(f"\n  TIMEOUT after {duration:.1f}s")
        return False, duration, "Timed out after 120s"
    except Exception as e:
        duration = time.time() - start
        print(f"\n  ERROR: {e}")
        return False, duration, str(e)


def main():
    args = sys.argv[1:]
    skip_refresh = '--skip-refresh' in args
    build_only = '--build-only' in args

    print(f"{'='*60}")
    print(f"  KPI Pipeline Orchestrator")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Mode: {'build-only' if build_only else ('skip-refresh' if skip_refresh else 'full')}")
    print(f"{'='*60}")

    cwd = os.path.join(SCRIPT_DIR, '..')
    results = []

    steps_to_run = STEPS[:]
    if build_only:
        steps_to_run = [STEPS[3]]  # Only build
    elif skip_refresh:
        steps_to_run = STEPS[1:]  # Skip refresh

    total_start = time.time()
    all_ok = True

    for script, desc in steps_to_run:
        ok, dur, output = run_step(script, desc, cwd)
        results.append((script, ok, dur))
        if not ok:
            all_ok = False
            print(f"\n  Pipeline STOPPED at {script}. Fix the error and retry.")
            break

    total_dur = time.time() - total_start

    # Summary
    print(f"\n{'='*60}")
    print(f"  PIPELINE SUMMARY")
    print(f"{'='*60}")
    for script, ok, dur in results:
        status = 'OK' if ok else 'FAILED'
        print(f"  [{status}] {script} ({dur:.1f}s)")
    print(f"\n  Total: {total_dur:.1f}s | Status: {'ALL OK' if all_ok else 'FAILED'}")
    print(f"  Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if all_ok:
        dashboard_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'KPI_DASHBOARD.html')
        print(f"\n  Dashboard: {dashboard_path}")

    sys.exit(0 if all_ok else 1)


if __name__ == '__main__':
    main()
