# Layer 2 Findings — Contextual Audit (15 Auditors)

---

## A09 — Business Logic Auditor

### A09-001 | CRITICAL | `calc_perf` in merge uses `originalEta` field name but reads `dueDate` directly
- **Evidence**: `merge_opossum_data.py:527` calls `calc_perf(status, due, effective_delivery)` where `due = iss.get('dueDate')`. But `normalize_data.py:159` uses `originalEta` for the same comparison. These measure different things: `dueDate` is the CURRENT ETA; `originalEta` is the FIRST ETA ever set.
- **Impact**: KPI1 (ETA Accuracy) is measured against different baselines in merge vs normalize. If a TSA member negotiated an extension, merge says "on time" (vs current ETA) but normalize says "late" (vs original ETA). The normalize version overwrites merge's `perf` field, so final dashboard uses original ETA — but intermediate data is inconsistent.
- **Recommendation**: Clarify which ETA is canonical for KPI1. Document the decision. Remove the redundant calc_perf call in merge (normalize always recalculates anyway).
- **Confidence**: HIGH

### A09-002 | HIGH | Admin-close detection may misclassify real tickets
- **Evidence**: `normalize_data.py:409-420` — Pattern: `not startedAt AND not deliveryDate AND not inReviewDate` → admin close → force `On Time`.
- **Impact**: A ticket that was genuinely worked on but lacks startedAt (Linear doesn't always set this) would be incorrectly classified as admin-close and given a free "On Time". This inflates ETA Accuracy.
- **Recommendation**: Add a guard: also check if the ticket has history events (at least 2 state transitions = real work happened).
- **Confidence**: MEDIUM

### A09-003 | MEDIUM | Parent ticket exclusion may miss nested subtasks
- **Evidence**: `merge_opossum_data.py:413-418` — Identifies parents by checking `parentId` in all issues. But this only finds direct parents. If there's a grandparent → parent → child chain, the parent is excluded but the grandparent isn't.
- **Impact**: Low in current data (Linear typically uses 1-level nesting). But if nesting increases, grandparents would appear as standalone tickets in KPI calculations.
- **Recommendation**: Document the 1-level-only assumption. Consider recursive parent detection if needed.
- **Confidence**: LOW

---

## A10 — UX/DX Auditor

### A10-001 | MEDIUM | Pipeline output is wall-of-text with no summary at the end
- **Evidence**: `orchestrate.py:115-127` — prints a summary table but it's buried after pages of per-step output.
- **Impact**: When running full pipeline, the user must scroll up to find the summary. No clear "SUCCESS" or "FAILED" banner.
- **Recommendation**: Add a colored/bold banner at the very end: `===== PIPELINE OK (4 steps, 12.3s) =====`
- **Confidence**: LOW

### A10-002 | LOW | Dashboard has no loading indicator
- **Evidence**: `build_html_dashboard.py` JS — no loading state. Chart.js renders immediately from embedded data.
- **Impact**: For large datasets, initial render may cause a brief freeze. Not an issue at current scale (1368 records) but could be for 10K+.
- **Recommendation**: N/A at current scale. Note for future.
- **Confidence**: LOW

---

## A11 — Data Flow Auditor

### A11-001 | HIGH | Data can get stuck in intermediate state if pipeline fails mid-way
- **Evidence**: `orchestrate.py:99-110` — If normalize fails, `_dashboard_data.json` already has merge's output (with stale perf labels). Build step would use this stale data if manually triggered.
- **Impact**: A partial pipeline run produces a dashboard with unrecalculated performance labels. The user sees stale or incorrect KPIs.
- **Recommendation**: Write merge output to a temp file (`_dashboard_data_staging.json`). Only promote to `_dashboard_data.json` after normalize succeeds.
- **Confidence**: MEDIUM

### A11-002 | MEDIUM | Cache file freshness check has 24h threshold but no hard block
- **Evidence**: `merge_opossum_data.py:228-229` — Prints WARNING if cache is >24h old but continues processing.
- **Impact**: Dashboard can be built from week-old data without any visible indicator on the dashboard itself (the staleness warning in M11 uses build date, not cache date).
- **Recommendation**: Pass cache age to the dashboard and display a red banner if data is >48h old.
- **Confidence**: MEDIUM

---

## A12 — Integration Auditor

### A12-001 | MEDIUM | Linear API rate limits not handled
- **Evidence**: `refresh_linear_cache.py:322` — `requests.post()` with no rate limit handling. Linear allows ~1500 req/hr for standard plans.
- **Impact**: With 7 members × 2 queries × pagination, we're at ~40 requests per refresh. Not close to limits now, but bulk retries or rapid manual refreshes could trigger throttling.
- **Recommendation**: Add a 429 handler with backoff.
- **Confidence**: LOW

### A12-002 | LOW | Google Drive upload has no version/conflict detection
- **Evidence**: `upload_dashboard_drive.py:39-48` — Overwrites existing file by ID without checking modifiedTime.
- **Impact**: If someone manually edits the Drive file, the upload silently overwrites their changes.
- **Recommendation**: Not critical (file is auto-generated), but could add a warning if Drive modifiedTime > last build time.
- **Confidence**: LOW

---

## A13 — Observability Auditor

### A13-001 | HIGH | No structured logging anywhere in the pipeline
- **Evidence**: All 8 core files use `print()` exclusively. No log levels, no timestamps in output (except orchestrate's start/end), no request IDs.
- **Impact**: Cannot grep for errors, cannot set up alerting, cannot correlate issues across pipeline steps. The tray server writes to a flat log file that grows unboundedly.
- **Recommendation**: Introduce Python `logging` module with `{timestamp} [{level}] {module}: {message}` format.
- **Confidence**: HIGH

### A13-002 | MEDIUM | Tray server log file grows without rotation
- **Evidence**: `kpi_tray.py:24` — opens `kpi_tray.log` in append mode (`'a'`). No rotation, no max size.
- **Impact**: Over months, the log file can grow to hundreds of MB. No automatic cleanup.
- **Recommendation**: Use `logging.handlers.RotatingFileHandler` with max 5MB, 3 backups.
- **Confidence**: MEDIUM

---

## A14 — Deployment Auditor

### A14-001 | MEDIUM | No CI/CD pipeline
- **Evidence**: No `.github/workflows/`, no `Makefile`, no deployment scripts except `kpi_publish.bat`.
- **Impact**: All deployment is manual. No automated testing before deployment. No way to catch regressions.
- **Recommendation**: Add a GitHub Actions workflow that runs `pytest` on push to master.
- **Confidence**: MEDIUM

### A14-002 | LOW | No rollback mechanism
- **Evidence**: Dashboard is a single HTML file overwritten on each build. No versioning.
- **Impact**: If a build produces a corrupt dashboard, there's no quick rollback except re-running the pipeline.
- **Recommendation**: Keep the last 3 builds: `KPI_DASHBOARD.html`, `KPI_DASHBOARD.prev1.html`, `KPI_DASHBOARD.prev2.html`.
- **Confidence**: LOW

---

## A15 — Scalability Auditor

### A15-001 | LOW | In-memory data processing limits dataset size
- **Evidence**: All pipeline steps load the full JSON into memory. At ~1368 records (~2MB), this is fine.
- **Impact**: Would not scale to 100K+ records without refactoring. Not a concern at current scale.
- **Recommendation**: N/A at current scale. Note for future.
- **Confidence**: LOW

---

## A16 — Documentation Auditor

### A16-001 | MEDIUM | CLAUDE.md is comprehensive but has no rendered examples
- **Evidence**: `CLAUDE.md` documents KPIs, rules, pipeline steps. But no screenshots, no expected output examples, no "what does the dashboard look like" section.
- **Impact**: New team members must run the pipeline to understand what it produces.
- **Recommendation**: Add a screenshot or link to a live dashboard in TEAM_README.md.
- **Confidence**: LOW

### A16-002 | LOW | Code comments reference rule IDs (D.LIE, H, M, A, C, L, P, F) without a glossary
- **Evidence**: Throughout all files — e.g., `# D.LIE20:`, `# H6:`, `# M14:`, `# C3:`, `# A32:`
- **Impact**: These are well-documented in CLAUDE.md, but in-code they're opaque without reading the full doc. A developer seeing `# M6: unified to Staircase` must look up what M6 means.
- **Recommendation**: Add a one-line comment after each rule ID: `# M6 (customer normalization): unified Gainsight to Staircase`
- **Confidence**: LOW

---

## A17 — Accessibility Auditor

### A17-001 | MEDIUM | Dashboard HTML has limited keyboard navigation
- **Evidence**: `build_html_dashboard.py` JS — tabs are clickable divs, not `<button>` elements. Audit collapse headers use `role="button"` and `tabindex="0"` (good) but chart interactions are mouse-only.
- **Impact**: Keyboard-only users can navigate tabs and collapsible sections but cannot interact with charts or tooltips.
- **Recommendation**: Add `role="tab"` and `aria-selected` to tab elements. Chart.js tooltips are inherently mouse-based; add a data table alternative.
- **Confidence**: MEDIUM

---

## A18 — Compliance Auditor

### A18-001 | LOW | Employee performance data exposed via public ngrok URL
- **Evidence**: `kpi_tray.py:75` — Public ngrok URL serves dashboard with individual performance data (names, ticket counts, on-time rates).
- **Impact**: While not PII in the legal sense, employee performance metrics are sensitive. Public exposure could violate internal HR policies.
- **Recommendation**: Add authentication to the ngrok tunnel (see A04-004).
- **Confidence**: MEDIUM

---

## A19 — Architecture Auditor

### A19-001 | MEDIUM | Pipeline uses subprocess instead of function calls
- **Evidence**: `orchestrate.py:46` — `subprocess.run([PYTHON, script_path])` for each step.
- **Impact**: Each step is a separate Python process. No shared state, no transactional integrity, higher startup cost. Module-level execution makes this the only viable approach currently.
- **Recommendation**: Refactor modules to expose `main()` functions, then call them directly from orchestrate. This enables atomic rollback and in-memory data passing.
- **Confidence**: MEDIUM

### A19-002 | LOW | Two HTTP servers for the same purpose
- **Evidence**: `serve_kpi.py` (standalone, port 8787) and `kpi_tray.py` (embedded, port 8080) both serve the dashboard.
- **Impact**: Confusion about which server to use. Port conflicts if both are running.
- **Recommendation**: Deprecate `serve_kpi.py` — the tray server is the canonical entry point now.
- **Confidence**: LOW

---

## A20 — Maintainability Auditor

### A20-001 | MEDIUM | Bus factor = 1
- **Evidence**: Single contributor (Thiago) in git history. No CONTRIBUTING.md.
- **Impact**: If the maintainer is unavailable, no one else can modify or fix the pipeline. The codebase has 59+ data integrity rules with subtle interactions.
- **Recommendation**: Document the top 10 most common maintenance tasks. Add a "troubleshooting" section to CLAUDE.md.
- **Confidence**: HIGH

---

## A31 — Formula Validator Auditor

### A31-001 | HIGH | ETA Accuracy denominator inconsistency
- **Evidence**: CLAUDE.md says KPI1 = "tickets with ETA delivered on time / total tickets with ETA". But `normalize_data.py:159` uses `originalEta` (first-ever ETA) while `merge_opossum_data.py:527` uses current `dueDate`.
- **Impact**: If a ticket's ETA was changed 3 times, the "accuracy" is measured differently depending on which stage last wrote the `perf` field.
- **Recommendation**: Standardize: use `originalEta` everywhere (measures commitment accuracy) or `finalEta` (measures delivery accuracy). Document which one and why.
- **Confidence**: HIGH

### A31-002 | MEDIUM | Division-by-zero in ETA Coverage
- **Evidence**: Previous commit `7deeafb` fixed this for 0/0 case. But `calc_perf_with_history` returns 'N/A' for invalid dates, which could be mixed with intentional N/A for canceled tickets.
- **Impact**: A canceled ticket and a ticket with a corrupted date both show as N/A. The dashboard treats them identically, which is wrong for KPI calculation.
- **Recommendation**: Use distinct labels: `'N/A (canceled)'` vs `'N/A (parse error)'`.
- **Confidence**: LOW

---

## A32 — State Machine Auditor

### A32-001 | MEDIUM | No validation of state transition legality
- **Evidence**: `merge_opossum_data.py:96-128` — processes all state transitions as-is from Linear history without validating they're legal (e.g., Backlog → Done skipping In Progress).
- **Impact**: Unusual transitions (direct Triage → Done) could mean tickets are being bulk-closed without actual work, inflating velocity.
- **Recommendation**: Flag tickets with unusual transition sequences (e.g., never entered In Progress but went to Done).
- **Confidence**: MEDIUM

---

## A33 — Filter Interaction Auditor

### A33-001 | MEDIUM | Dashboard "External" filter hides internal tickets that have customer names
- **Evidence**: `normalize_data.py:309-312` — tickets with customer names that are in `NOT_REAL_CLIENTS` get category=Internal. But in the dashboard, the "External" segment filter hides them entirely.
- **Impact**: TSA work tagged `[ChurnZero]` or `[Coda]` is invisible in the default External view. Users must know to switch to "All" to see them.
- **Recommendation**: Add a "Borderline" category or show a count of hidden tickets below the filter.
- **Confidence**: LOW
