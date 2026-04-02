# Layer 1 Findings — Blind Audit (8 Auditors)

---

## A01 — Data Integrity Auditor

### A01-001 | HIGH | Duplicate `calc_perf` implementations
- **Evidence**: `merge_opossum_data.py:316-349` and `normalize_data.py:112-148`
- **Impact**: Two versions of the same function with subtly different logic. merge version has no `Not Started` path for Backlog/Todo/Triage; normalize version does. If only one is updated, calculations silently diverge.
- **Recommendation**: Extract to `team_config.py` or a shared `kpi_utils.py`. Import in both files.
- **Confidence**: HIGH

### A01-002 | MEDIUM | Customer mapping defined in 3 separate locations
- **Evidence**: `merge_opossum_data.py:281-296` (extract_customer cust_map), `merge_opossum_data.py:475-491` (proj_map), `normalize_data.py:40-67` (CUSTOMER_MAP)
- **Impact**: Adding a new customer requires edits in 3 places. If one is missed, customer categorization becomes inconsistent. Already happened historically (Gainsight/Staircase).
- **Recommendation**: Consolidate into `team_config.py` as a single CUSTOMER_MAP dict.
- **Confidence**: HIGH

### A01-003 | MEDIUM | State IDs hardcoded without validation
- **Evidence**: `merge_opossum_data.py:24-44` — STATE_NAMES dict with 15 UUIDs
- **Impact**: If Linear changes state IDs (team restructure), the pipeline silently produces incorrect history analysis. The `_all_unknown_state_ids` warning (L603) helps but requires manual monitoring.
- **Recommendation**: Add a startup validation that queries Linear for current workflow states and compares against hardcoded IDs.
- **Confidence**: HIGH

### A01-004 | LOW | `bare except` on cache comparison
- **Evidence**: `refresh_linear_cache.py:411` — `except: pass`
- **Impact**: Swallows all exceptions including KeyboardInterrupt. Could mask real errors in the count-drop safety check.
- **Recommendation**: Change to `except (json.JSONDecodeError, IOError, ValueError): pass`
- **Confidence**: HIGH

---

## A02 — Error Handling Auditor

### A02-001 | HIGH | Pipeline errors are print-only, no structured logging
- **Evidence**: All files use `print()` for errors. No `logging` module, no log levels, no log rotation.
- **Impact**: When pipeline fails in background (via tray), errors go to a log file with no structure. No way to filter, alert, or parse errors programmatically.
- **Recommendation**: Replace `print()` with `logging.getLogger('kpi')` calls. Configure file + console handlers.
- **Confidence**: HIGH

### A02-002 | MEDIUM | HTTP timeout handling in `kpi_tray.py` is silent
- **Evidence**: `kpi_tray.py:114-119` (check_http), `kpi_tray.py:122-127` (check_ngrok) — both catch all exceptions and return False.
- **Impact**: Connection refused, DNS failures, and timeouts all look the same. No diagnostic info for debugging intermittent failures.
- **Recommendation**: Log the exception type in the catch block.
- **Confidence**: MEDIUM

### A02-003 | MEDIUM | `upload_dashboard_drive.py` has no retry on network failure
- **Evidence**: `upload_dashboard_drive.py:25-63` — Single request with no retry/backoff.
- **Impact**: Transient network issues cause the upload step to fail. The pipeline marks it as optional (orchestrate.py L27), but the user gets no upload without manual retry.
- **Recommendation**: Add exponential backoff (max 3 retries) for the upload request.
- **Confidence**: HIGH

### A02-004 | LOW | `serve_kpi.py` refresh endpoint leaks internal error details
- **Evidence**: `serve_kpi.py:90` — `json.dumps({"success": False, "message": str(e)})` returns raw exception text.
- **Impact**: Internal paths, module names, and error details exposed to any client calling `/refresh`.
- **Recommendation**: Return generic "Internal error" message; log the details server-side.
- **Confidence**: HIGH

---

## A03 — Code Quality Auditor

### A03-001 | HIGH | `build_html_dashboard.py` is 2829 lines with embedded HTML/CSS/JS
- **Evidence**: `build_html_dashboard.py` — entire dashboard (CSS ~230 lines, HTML ~170 lines, JS ~1640 lines) embedded as a raw Python string.
- **Impact**: No syntax highlighting, no linting, no IDE support for the JS. Extremely hard to maintain. Any change requires understanding the interplay between Python string manipulation and JS logic.
- **Recommendation**: Extract HTML template to a separate `.html` file. Use Jinja2 or simple `{{placeholder}}` replacement. Keep the Python script as just the data injection layer.
- **Confidence**: HIGH

### A03-002 | MEDIUM | Module-level execution in merge and normalize scripts
- **Evidence**: `merge_opossum_data.py` and `normalize_data.py` execute all logic at module level (outside functions). `test_kpi_calculations.py` has to mock `builtins.open` and `json.load` just to import them.
- **Impact**: Cannot import functions without triggering full file I/O. Makes testing fragile and increases coupling.
- **Recommendation**: Wrap main logic in `def main()` + `if __name__ == '__main__': main()`. Export pure functions for testing.
- **Confidence**: HIGH

### A03-003 | MEDIUM | 10 variant files in `variants/` appear unused
- **Evidence**: `variants/build_v1_executive.py` through `build_v10_dark.py` — not imported or referenced anywhere in the pipeline.
- **Impact**: 5,534 lines of dead code. Increases cognitive load and maintenance surface.
- **Recommendation**: Move to an `archive/` directory or delete entirely. If needed, they exist in git history.
- **Confidence**: HIGH

### A03-004 | LOW | Magic strings for performance labels
- **Evidence**: `'On Time'`, `'Late'`, `'No ETA'`, `'Not Started'`, `'Blocked'`, `'On Hold'`, `'N/A'` used as raw strings throughout merge, normalize, build, and tests.
- **Impact**: Typo in any one location creates a silent categorization error. No IDE autocomplete.
- **Recommendation**: Define as constants in `team_config.py`: `PERF_ON_TIME = 'On Time'`, etc.
- **Confidence**: MEDIUM

---

## A04 — Security Auditor

### A04-001 | HIGH | XSS via JSON injection partially mitigated
- **Evidence**: `build_html_dashboard.py:56-57` — escapes `</script>` but does not escape other vectors. Data is injected raw into an HTML string via `.replace('__DATA__', data_json_safe)`.
- **Impact**: If any Linear ticket title contains crafted HTML entities or JS-triggerable sequences (e.g., event handlers in data displayed as innerHTML), XSS is possible.
- **Recommendation**: Use `json.dumps()` with `ensure_ascii=True` (already done) AND verify all data rendering in JS uses `textContent` not `innerHTML`. Audit the JS for any `innerHTML` assignments with user data.
- **Confidence**: MEDIUM

### A04-002 | MEDIUM | API key loading from `.env` has no permission check
- **Evidence**: `refresh_linear_cache.py:18-27` — reads API key from `.env` file with no file permission validation.
- **Impact**: If `.env` is world-readable (common on Windows), any local process can read the Linear API key.
- **Recommendation**: Add a warning if `.env` file permissions are too open (on Unix: check mode; on Windows: check ACL).
- **Confidence**: MEDIUM

### A04-003 | MEDIUM | HTTP server binds to 0.0.0.0
- **Evidence**: `kpi_tray.py:194` — `HTTPServer(('0.0.0.0', HTTP_PORT), handler)`
- **Impact**: Dashboard is accessible from any network interface, not just localhost. If the machine is on an untrusted network, internal KPI data is exposed.
- **Recommendation**: Bind to `127.0.0.1` instead. ngrok handles external access with its own auth.
- **Confidence**: HIGH

### A04-004 | LOW | ngrok exposes dashboard publicly without auth
- **Evidence**: `kpi_tray.py:75` — Public ngrok URL with no authentication layer.
- **Impact**: Anyone with the ngrok URL can view team KPI data (names, performance, ticket details).
- **Recommendation**: Add `--basic-auth` flag to ngrok command, or use ngrok's built-in OAuth.
- **Confidence**: HIGH

---

## A05 — Performance Auditor

### A05-001 | MEDIUM | Redundant JSON reads across pipeline steps
- **Evidence**: Each pipeline step reads and writes `_dashboard_data.json` independently. merge writes it, normalize reads and rewrites it, build reads it again.
- **Impact**: 3 full JSON parse/serialize cycles for ~1368 records. Not a bottleneck now (~0.1s each) but wasteful.
- **Recommendation**: Consider piping data in-memory between steps (function calls instead of subprocess + file I/O). Would also enable atomic pipeline execution.
- **Confidence**: LOW

### A05-002 | MEDIUM | Linear API fetches 3 queries per person (7 people = 21 API calls minimum)
- **Evidence**: `refresh_linear_cache.py:356-384` — For each of 7 members: fetch by assignee + fetch by creator, with pagination.
- **Impact**: ~21+ API calls per refresh. With pagination, could be 40+. Takes 10-15 seconds.
- **Recommendation**: Consider a single team-level query with `filter: { team: { id: { in: [...] } } }` to reduce API calls.
- **Confidence**: MEDIUM

### A05-003 | LOW | `build_html_dashboard.py` string concatenation for 2829-line template
- **Evidence**: `build_html_dashboard.py:2818` — `.replace().replace().replace().replace().replace()`
- **Impact**: 5 full-string scans on a ~300KB string. Negligible cost but inelegant.
- **Recommendation**: Use a single `string.Template` or `str.format_map()` call.
- **Confidence**: LOW

---

## A06 — Dependency Auditor

### A06-001 | HIGH | Phantom dependencies: pystray and Pillow
- **Evidence**: `kpi_tray.py:44-45` imports `pystray` and `PIL`. Neither is in `requirements.txt`.
- **Impact**: Fresh install from requirements.txt will fail when running the tray server. `pip install -r requirements.txt` is insufficient.
- **Recommendation**: Add `pystray>=0.19` and `Pillow>=10.0` to requirements.txt.
- **Confidence**: HIGH

### A06-002 | MEDIUM | No lock file
- **Evidence**: No `requirements.lock`, no `pip freeze` output, no `pyproject.toml`.
- **Impact**: Builds are not reproducible. Different machines may get different dependency versions.
- **Recommendation**: Add `pip freeze > requirements.lock` to the setup workflow, or migrate to `pyproject.toml` + `pip-tools`.
- **Confidence**: MEDIUM

### A06-003 | LOW | External dependency on `kpi_auth.py` not in project
- **Evidence**: `upload_dashboard_drive.py:12` — `from kpi_auth import get_access_token`. This file is not in the kpi/ directory.
- **Impact**: Upload step fails if `kpi_auth.py` is not in the Python path. Not self-contained.
- **Recommendation**: Document where `kpi_auth.py` lives, or bundle it in the project.
- **Confidence**: HIGH

---

## A07 — Configuration Auditor

### A07-001 | HIGH | No `.env.example` file
- **Evidence**: `.env` is referenced but not included; no template exists.
- **Impact**: New developers have no idea what environment variables are needed. `LINEAR_API_KEY` is the only one, but this must be documented.
- **Recommendation**: Create `.env.example` with `LINEAR_API_KEY=your_key_here`.
- **Confidence**: HIGH

### A07-002 | MEDIUM | Output path hardcoded to `~/Downloads/`
- **Evidence**: `build_html_dashboard.py:34`, `serve_kpi.py:25`, `kpi_tray.py:72`, `upload_dashboard_drive.py:14` — all use `os.path.expanduser('~'), 'Downloads'`.
- **Impact**: Cannot change output location without editing 4+ files. Doesn't work on non-standard setups.
- **Recommendation**: Define `OUTPUT_DIR` in a single config location (env var or team_config.py).
- **Confidence**: MEDIUM

### A07-003 | LOW | HTTP port and ngrok URL not configurable
- **Evidence**: `kpi_tray.py:75,77` — hardcoded `NGROK_URL` and `HTTP_PORT = 8080`.
- **Impact**: Port conflicts require code changes. Cannot run multiple instances.
- **Recommendation**: Read from env vars with defaults: `HTTP_PORT = int(os.environ.get('KPI_PORT', 8080))`.
- **Confidence**: MEDIUM

---

## A08 — Test Coverage Auditor

### A08-001 | HIGH | 6 of 8 core modules have zero test coverage
- **Evidence**: Only `merge_opossum_data.py` and `normalize_data.py` have tests (and only their pure functions). No tests for: `refresh_linear_cache.py`, `build_html_dashboard.py`, `orchestrate.py`, `kpi_tray.py`, `serve_kpi.py`, `upload_dashboard_drive.py`.
- **Impact**: Regressions in API fetching, HTML generation, pipeline orchestration, and server behavior go undetected.
- **Recommendation**: Add integration test for `orchestrate.py --build-only` (no API calls needed). Add smoke test for `build_html_dashboard.py` (valid HTML output).
- **Confidence**: HIGH

### A08-002 | MEDIUM | Tests require extensive mocking due to module-level I/O
- **Evidence**: `test_kpi_calculations.py:33-67` — `_load_merge_module()` and `_load_normalize_module()` patch 6+ builtins each.
- **Impact**: Fragile test setup. Any new module-level I/O in source files breaks tests without obvious cause.
- **Recommendation**: Refactor source modules to wrap I/O in `main()` functions (see A03-002).
- **Confidence**: HIGH

### A08-003 | MEDIUM | No edge case tests for history extraction with unknown state IDs
- **Evidence**: `test_kpi_calculations.py` tests Raccoons team state IDs only. No test for tickets from unknown teams (where STATE_NAMES lookup returns empty string).
- **Impact**: The `_all_unknown_state_ids` fallback path is untested.
- **Recommendation**: Add test with a state ID not in STATE_NAMES.
- **Confidence**: MEDIUM

### A08-004 | LOW | No negative test for count-drop protection
- **Evidence**: `refresh_linear_cache.py:404-410` — 50% drop guard exists but has no test.
- **Impact**: Safety mechanism could be accidentally broken without detection.
- **Recommendation**: Add test that verifies `sys.exit(1)` when new count < 50% of old.
- **Confidence**: MEDIUM
