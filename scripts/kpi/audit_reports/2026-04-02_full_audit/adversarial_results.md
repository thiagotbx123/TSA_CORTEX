# Adversarial Challenge Results

## CRITICAL Findings

### A30-003 / A01-001 / A09-001 / A31-001 — Dual calc_perf / ETA inconsistency
- **Red Team**: Is this really a problem? → **YES**. The merge calc_perf runs first, then normalize overwrites. The merge version is dead code in effect — normalize always wins. But the intermediate `_dashboard_data.json` contains merge's labels, which could confuse anyone inspecting the data file directly.
- **Game Theory**: Who benefits? → Nobody intentionally. This is technical debt from incremental development.
- **Verdict**: **VALIDATED as CRITICAL**. The fix is trivial (remove calc_perf call from merge, rely on normalize) but the impact on KPI trust is high.

---

## HIGH Findings

### A06-001 — Phantom dependencies (pystray, Pillow)
- **Red Team**: Real problem? → **YES**. Fresh `pip install -r requirements.txt` will fail.
- **Verdict**: **VALIDATED as HIGH**

### A08-001 — 6/8 modules untested
- **Red Team**: Does this really cause damage? → Not directly, but it compounds deployment risk.
- **Verdict**: **VALIDATED as HIGH**

### A02-001 / A13-001 — No structured logging
- **Red Team**: The pipeline works fine with print(). Is structured logging overkill for an internal tool? → **DOWNGRADED**. For a 7-person internal tool, print() with tray log file is adequate. Structured logging would be nice but is not urgent.
- **Verdict**: **DOWNGRADED to MEDIUM**

### A04-003 + A04-004 — HTTP on 0.0.0.0 + ngrok no auth
- **Red Team**: Is the data actually sensitive? → Performance metrics of 7 employees. Moderately sensitive.
- **Game Theory**: What's the opportunity cost of fixing? → 10 minutes to change 0.0.0.0 → 127.0.0.1 and add `--basic-auth` to ngrok.
- **Verdict**: **VALIDATED as HIGH** (trivial fix, real exposure)

### A09-002 + A23-001 — Admin-close inflates KPI1
- **Red Team**: Does this actually happen? → The `retroactiveEta` flag already detects part of this pattern. Git history shows awareness.
- **Game Theory**: Would someone intentionally exploit this? → Unlikely in a 7-person team. But the metric should be trustworthy regardless.
- **Verdict**: **DOWNGRADED to MEDIUM** — awareness and partial mitigation exist

### A03-001 — 2829-line embedded HTML/CSS/JS
- **Red Team**: Does the recommended fix (extract template) create new problems? → Adds file management complexity. The current approach is ugly but works.
- **Verdict**: **VALIDATED as HIGH** — maintainability debt is real and growing

### A37-002 — Staleness warning uses build date not cache freshness
- **Red Team**: Real user confusion? → Yes. Users rely on the "data as of" label to trust dashboard freshness.
- **Verdict**: **VALIDATED as HIGH**

### A35-001 — KPI1 incentivizes ETA padding
- **Red Team**: Is this a code bug or a design choice? → Design flaw in the metric, not a code bug.
- **Verdict**: **DOWNGRADED to MEDIUM** — correct observation but requires metric redesign, not code fix

### A01-002 — Customer mapping in 3 locations
- **Red Team**: Has this caused bugs before? → Yes — Gainsight/Staircase issue in git history.
- **Verdict**: **VALIDATED as HIGH**

### A21-002 — File naming inconsistency (KPI vs RACCOONS_KPI)
- **Red Team**: Does this cause real problems? → Upload fails silently if filenames don't match.
- **Verdict**: **VALIDATED as HIGH** — actual functional bug risk
