# Discovery Report — KPI Dashboard
**Audit Engine v3.1 | 2026-04-02**

## 1. File Structure Scan

| Metric | Value |
|--------|-------|
| Total files | 38 (excl. .cache, __pycache__) |
| Python files | 24 |
| Total LOC (Python) | 13,794 |
| Total LOC (all) | ~15,062 |
| Primary language | Python 3.14 |
| Framework | None (stdlib + requests, openpyxl, pystray, PIL) |
| Entry point | `orchestrate.py` |

### File Tree
```
scripts/kpi/
├── orchestrate.py            (132 lines) — Pipeline orchestrator
├── refresh_linear_cache.py   (423 lines) — Linear API fetcher
├── merge_opossum_data.py     (649 lines) — Data merger + history extraction
├── normalize_data.py         (527 lines) — Data normalizer + perf calculator
├── build_html_dashboard.py   (2829 lines) — HTML dashboard generator
├── build_waki_dashboard.py   (712 lines) — XLSX executive report
├── team_config.py            (30 lines) — Shared team config
├── kpi_tray.py               (366 lines) — System tray server
├── _tray_launcher.py         (26 lines) — pythonw.exe launcher wrapper
├── serve_kpi.py              (110 lines) — Standalone HTTP server
├── upload_dashboard_drive.py (70 lines) — Google Drive uploader
├── _gen_audit_xlsx.py        (444 lines) — Audit XLSX generator
├── build_gantt_draft.py      (455 lines) — Gantt chart builder
├── kpi_publish.bat           (1 line) — Launch script
├── kpi_dashboard.ico         — Tray icon
├── implementation_timeline.json — Timeline data
├── requirements.txt          (2 deps)
├── CLAUDE.md                 (18KB) — Project documentation
├── TEAM_README.md            — Team usage guide
├── AUDIT_REPORT.md           — Previous audit
├── MEGA_AUDIT_20_AUDITORS.md — Previous comprehensive audit
├── tests/
│   └── test_kpi_calculations.py (690 lines) — Unit tests
└── variants/
    └── build_v1..v10_*.py    (10 files) — Dashboard variant experiments
```

## 2. Documentation

- **CLAUDE.md**: Comprehensive (18KB). Covers pipeline, KPIs, D.LIE rules, team config, Linear state IDs, customer mapping.
- **TEAM_README.md**: End-user guide for viewing the dashboard.
- **AUDIT_REPORT.md**: Previous audit findings.
- **No README.md** at project root.
- **No CONTRIBUTING.md**.
- **No CHANGELOG.md** (git log serves as implicit changelog).

## 3. Code Pattern Detection

- **Architecture**: Linear data pipeline (Fetch → Merge → Normalize → Build → Upload)
- **Data access**: Direct HTTP to Linear GraphQL API, Google Drive REST API
- **Auth**: API key from `.env` file, Google OAuth via `kpi_auth.py` (external)
- **Error handling**: Try/except with print statements; no structured logging
- **Testing**: unittest with heavy mocking (module-level I/O)
- **Design patterns**: Functional (no classes except HTTP handlers), atomic file writes
- **Config management**: `team_config.py` as shared config; hardcoded state IDs in merge

## 4. Data Flow

```
Linear API → _kpi_all_members.json → merge → _dashboard_data.json → normalize → _dashboard_data.json → build → KPI_DASHBOARD.html → upload → Google Drive
```

**Inputs**: Linear GraphQL API (7 team members, ~1368 issues)
**Transforms**: History extraction, customer mapping, perf calculation, date normalization
**Outputs**: Self-contained HTML dashboard, XLSX report, Google Drive upload
**Validation**: JSON decode check, count-drop protection (50% threshold), atomic writes
**External deps**: Linear API, Google Drive API, ngrok

## 5. Git History

- **20+ commits** on kpi/ files
- **1 contributor** (Thiago)
- **Most active files**: build_html_dashboard.py, normalize_data.py, merge_opossum_data.py
- **Recent focus**: Audit hardening, ETA accuracy, customer classification, tray server
- **No branches** (all on master)

## 6. Test Coverage

| Source File | Test File | Coverage |
|---|---|---|
| merge_opossum_data.py | test_kpi_calculations.py | Partial (calc_perf, date_to_week, extract_customer, extract_history_fields) |
| normalize_data.py | test_kpi_calculations.py | Partial (calc_perf_with_history) |
| refresh_linear_cache.py | — | None |
| build_html_dashboard.py | — | None |
| orchestrate.py | — | None |
| kpi_tray.py | — | None |
| serve_kpi.py | — | None |
| upload_dashboard_drive.py | — | None |

**Test framework**: unittest (690 lines, 45+ test cases)
**Coverage**: ~2 of 8 core modules tested. Only pure functions tested; no integration tests.

## 7. Configuration vs Hardcoded

| Item | Location | Type |
|---|---|---|
| LINEAR_API_KEY | `.env` file | Env var (OK) |
| Linear Team IDs | refresh_linear_cache.py L42-43 | Hardcoded |
| Linear User IDs | team_config.py | Hardcoded (but documented) |
| State IDs | merge_opossum_data.py L24-44 | Hardcoded |
| HTTP port | kpi_tray.py L77 | Hardcoded (8080) |
| ngrok URL | kpi_tray.py L75 | Hardcoded |
| Drive folder ID | upload_dashboard_drive.py L16 | Hardcoded |
| Customer mappings | merge/normalize (3 separate dicts) | Hardcoded |
| Output paths | Multiple files | Hardcoded to ~/Downloads/ |
