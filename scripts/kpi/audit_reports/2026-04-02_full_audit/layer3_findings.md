# Layer 3 Findings — Symbiotic Audit (14 Auditors)

---

## A21 — Narrative Auditor

### A21-001 | MEDIUM | CLAUDE.md claims 3 KPIs but KPI3 (Reliability) is "NOT ACTIVE"
- **Evidence**: `CLAUDE.md` describes 3 KPIs. `build_html_dashboard.py:14` — `C1: KPI3 marked as NOT ACTIVE until rework labels are in use`.
- **Impact**: Stakeholders may expect 3 KPIs but only 2 are operational. The dashboard shows a KPI3 cell but it's greyed out.
- **Recommendation**: Update CLAUDE.md to clarify KPI3's status: "KPI3 is designed but not active — awaiting rework label adoption by the team."
- **Confidence**: HIGH

### A21-002 | LOW | File naming inconsistency
- **Evidence**: Output is `KPI_DASHBOARD.html` but upload targets `RACCOONS_KPI_DASHBOARD.html`. Dashboard title says "KPI Dashboard" but team-facing name is "TSA KPI Dashboard".
- **Impact**: Confusion about which file is authoritative. The build creates `KPI_DASHBOARD.html` but upload looks for `RACCOONS_KPI_DASHBOARD.html`.
- **Recommendation**: Unify to one name. Update `upload_dashboard_drive.py:14` to match `build_html_dashboard.py:34` output.
- **Confidence**: HIGH

---

## A22 — Evolution Auditor

### A22-001 | LOW | Codebase shows positive evolution trend
- **Evidence**: Git history shows systematic pattern: identify issue → create D.LIE/H/M rule → implement fix → add test. 20+ commits follow this pattern.
- **Impact**: Positive. The codebase is improving with each iteration.
- **Recommendation**: Continue this pattern. Consider automating rule enforcement (e.g., pytest markers for each rule).
- **Confidence**: HIGH

---

## A23 — Risk Auditor

### A23-001 | HIGH | Compound risk: duplicate calc_perf + admin-close override = gameable KPIs
- **Evidence**: Combines A01-001 (duplicate calc_perf) + A09-001 (merge vs normalize using different ETAs) + A09-002 (admin-close → On Time).
- **Impact**: A team member could: (1) set an ETA on a ticket that was already completed, (2) close it the same day → admin-close detection → forced "On Time". This inflates KPI1 without detection.
- **Recommendation**: Add a `retroactiveEta` flag (already partially implemented) and exclude retroactive ETAs from KPI1 calculation by default.
- **Confidence**: MEDIUM

### A23-002 | MEDIUM | Single point of failure: `_dashboard_data.json`
- **Evidence**: All pipeline steps depend on this single file. Corruption = no dashboard.
- **Impact**: If the file is corrupted (partial write, disk full, concurrent access), the entire pipeline fails.
- **Recommendation**: Atomic writes (already implemented via `.tmp` + `os.replace`) mitigate this. But add a backup: keep `_dashboard_data.json.bak` from the previous successful build.
- **Confidence**: MEDIUM

---

## A24 — Cost Auditor

### A24-001 | LOW | ngrok free tier may have session limits
- **Evidence**: `kpi_tray.py:219` — uses ngrok with a custom domain (indicating a paid plan).
- **Impact**: If the ngrok subscription lapses, the public URL breaks. Local access (port 8080) continues working.
- **Recommendation**: Document ngrok as a paid dependency. Add graceful degradation (dashboard works fully offline).
- **Confidence**: LOW

---

## A25 — Ethics Auditor

### A25-001 | LOW | Individual performance tracking may create pressure
- **Evidence**: Dashboard shows per-person KPI scores (ETA Accuracy %, velocity) visually ranked.
- **Impact**: Public visibility of individual performance can create unhealthy competition or anxiety, especially if metrics don't account for ticket complexity.
- **Recommendation**: Consider adding a team-level aggregate view as default, with individual drill-down. Add complexity weighting if estimate data is available.
- **Confidence**: LOW

---

## A26 — Red Team Auditor

### A26-001 | MEDIUM | Data injection via Linear ticket titles
- **Evidence**: Ticket titles are injected into the dashboard HTML via JSON. While `json.dumps(ensure_ascii=True)` escapes most vectors, the data passes through multiple `.replace()` chains.
- **Impact**: A crafted ticket title like `{"key": "value</script><script>alert(1)"}` would be escaped by json.dumps. **Current mitigation is adequate.** But the `innerHTML` usage in JS tooltip rendering could be a secondary vector.
- **Recommendation**: Audit all `innerHTML` assignments in the embedded JS. Replace with `textContent` where possible.
- **Confidence**: MEDIUM

---

## A27 — Game Theory Auditor

### A27-001 | MEDIUM | ETA gaming: set ETA = delivery date for guaranteed On Time
- **Evidence**: `merge_opossum_data.py:575-577` — `retroactiveEta` flag detects this pattern (ETA == delivery AND <=1 ETA change). But the flag is only informational — it doesn't exclude from KPI1.
- **Impact**: A member can game KPI1 by always setting ETA = today when they're about to deliver. The `retroactiveEta` flag catches it but doesn't penalize.
- **Recommendation**: In the dashboard, show "Organic ETA Accuracy" (excluding retroactive) vs "Total ETA Accuracy" (including all). This is already partially implemented per commit `d376ad8`.
- **Confidence**: HIGH

---

## A28 — Ecosystem Auditor

### A28-001 | LOW | Single-contributor project with no community
- **Evidence**: Internal tool. 1 contributor. No external users, no issues, no PRs.
- **Impact**: Acceptable for an internal tool. Bus factor is the main concern (see A20-001).
- **Recommendation**: N/A for internal tools.
- **Confidence**: HIGH

---

## A29 — Future-Proofing Auditor

### A29-001 | MEDIUM | Python 3.14 is bleeding-edge
- **Evidence**: `kpi_publish.bat` references `C:\Python314\pythonw.exe`.
- **Impact**: Python 3.14 is pre-release. Library compatibility issues may arise. `pystray`, `Pillow`, `openpyxl` may not have wheels for 3.14.
- **Recommendation**: Test with a stable Python version (3.12 or 3.13). Pin Python version in documentation.
- **Confidence**: MEDIUM

### A29-002 | LOW | Linear API may deprecate GraphQL fields
- **Evidence**: Queries fetch 20+ fields per issue including `slaStartedAt`, `slaMediumRiskAt`, etc.
- **Impact**: If Linear deprecates or renames fields, the pipeline breaks silently (returns null instead of error).
- **Recommendation**: Add a schema validation step: after first fetch, verify expected fields exist in response.
- **Confidence**: LOW

---

## A30 — Synthesis Auditor

### A30-001 | Cross-layer pattern: Configuration fragmentation
- **Corroborated by**: A01-002 (3 customer maps), A07-001 (no .env.example), A07-002 (4 hardcoded output paths), A07-003 (hardcoded ports)
- **Pattern**: Configuration is scattered across 6+ files with no single source of truth beyond team_config.py.
- **Impact**: HIGH — Every configuration change requires touching multiple files. Error-prone.
- **Fix effort**: 4 hours — Create `kpi_config.py` with all constants, paths, and maps.

### A30-002 | Cross-layer pattern: Testing gap compounds deployment risk
- **Corroborated by**: A08-001 (6/8 untested), A03-002 (module-level I/O), A14-001 (no CI)
- **Pattern**: No automated quality gate between code change and deployment.
- **Impact**: HIGH — Any code change goes directly to production (the user's machine) untested.
- **Fix effort**: 4 hours — Refactor module-level I/O into main() functions + add CI.

### A30-003 | Cross-layer pattern: Dual calculation paths create audit trail confusion
- **Corroborated by**: A01-001 (duplicate calc_perf), A09-001 (different ETA baselines), A31-001 (formula inconsistency)
- **Pattern**: Performance labels are calculated twice with different inputs, then overwritten.
- **Impact**: CRITICAL — The most important metric (KPI1) has an ambiguous calculation path.
- **Fix effort**: 2 hours — Delete calc_perf from merge, rely solely on normalize's version.

---

## A34 — Regression Auditor

No previous AUDIT_ENGINE v3.1 audit exists for this project. This is the baseline audit.

---

## A35 — Metric Integrity Auditor

### A35-001 | HIGH | KPI1 measures "commitment accuracy" not "delivery speed"
- **Evidence**: KPI1 uses originalEta vs deliveryDate. This measures "did you meet your commitment?" not "did you deliver fast?". A member who sets generous ETAs (2 weeks for 1-day tasks) will score 100%.
- **Impact**: KPI1 incentivizes padding ETAs rather than setting accurate ones.
- **Recommendation**: Add a complementary metric: "ETA Tightness" = average (ETA - deliveryDate) days. High accuracy + high tightness = truly good performance.
- **Confidence**: HIGH

### A35-002 | MEDIUM | KPI2 (Velocity) counts tickets equally regardless of complexity
- **Evidence**: Dashboard counts "Done" tickets per week. A 1-point bug fix and a 13-point epic both count as 1.
- **Impact**: Incentivizes splitting work into many small tickets rather than tackling complex tasks.
- **Recommendation**: Show weighted velocity (sum of estimates) alongside count velocity. Linear `estimate` field is already fetched.
- **Confidence**: MEDIUM

---

## A36 — Similarity & Consistency Auditor

### A36-001 | MEDIUM | Status label inconsistency between merge and normalize
- **Evidence**: `merge_opossum_data.py:300-312` maps `Duplicate` → `Canceled`. But `normalize_data.py:80` lists `BBC_VARIANTS` for B.B.C normalization, which doesn't include 'Duplicate'.
- **Impact**: A Duplicate ticket gets mapped to Canceled in merge but wouldn't be caught by BBC_VARIANTS. Not a bug (different concepts) but confusing to audit.
- **Recommendation**: Add a comment in normalize clarifying that Duplicate → Canceled mapping happens in merge, not here.
- **Confidence**: LOW

---

## A37 — Propositional Coherence Auditor

### A37-001 | HIGH | Member card accuracy vs KPI1 global accuracy may diverge
- **Evidence**: Member cards show individual ETA accuracy. The KPI1 header cell shows team-level ETA accuracy. Both are calculated in the dashboard JS from the same data but with different filter scopes (member card = that person only; KPI1 = current segment filter).
- **Impact**: If a user clicks a member card while the "External" filter is active, the member card may show a different accuracy than the KPI1 header (which applies the segment filter). This is correct behavior but may confuse users.
- **Recommendation**: Add a tooltip to KPI1: "Filtered by current segment. Click a member card for their full stats."
- **Confidence**: MEDIUM

### A37-002 | MEDIUM | Staleness warning uses build date, not data freshness
- **Evidence**: `build_html_dashboard.py:63-64` — `latest_data_date` is the most recent `dateAdd` in data. But `dateAdd` reflects ticket creation, not when data was last fetched.
- **Impact**: The staleness warning could say "data from today" even if the API cache is a week old (because tickets created today appear in the data from an old fetch that happened to include recent tickets).
- **Recommendation**: Include the cache file's modification timestamp (when was _kpi_all_members.json last written?) as a separate "Last API refresh" indicator.
- **Confidence**: HIGH
