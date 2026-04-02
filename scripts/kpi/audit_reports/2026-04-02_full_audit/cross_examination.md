# Cross-Examination Matrix

## 1. Agreement Amplification (Corroborated Findings)

| Finding | Corroborated By | Layers | Boost |
|---------|----------------|--------|-------|
| Duplicate calc_perf / ETA baseline inconsistency | A01-001, A09-001, A31-001, A30-003 | L1+L2+L3 | → CRITICAL |
| Configuration fragmentation (3 customer maps, hardcoded paths) | A01-002, A07-001, A07-002, A07-003, A30-001 | L1+L3 | → HIGH |
| 6/8 modules untested + no CI | A08-001, A03-002, A14-001, A30-002 | L1+L2+L3 | → HIGH |
| No structured logging | A02-001, A13-001 | L1+L2 | → HIGH |
| Phantom dependencies (pystray, Pillow) | A06-001 | L1 | Stays HIGH |
| HTTP server on 0.0.0.0 + ngrok without auth | A04-003, A04-004, A18-001 | L1+L2 | → HIGH |
| Admin-close may inflate KPI1 | A09-002, A23-001, A27-001 | L2+L3 | → HIGH |
| Dashboard HTML embeds 2829 lines | A03-001, A04-001 | L1 | Stays HIGH |

## 2. Disagreement Investigation

| Finding A | Finding B | Resolution |
|-----------|-----------|------------|
| A05-002 (too many API calls) | A12-001 (rate limits OK at ~40 req) | No contradiction. A05-002 is optimization; A12-001 confirms current load is safe. Both valid. |
| A09-002 (admin-close inflates) | A22-001 (positive evolution) | A09-002 identifies a risk; A22-001 notes the team is addressing issues iteratively. Compatible — the risk exists but is being mitigated over time. |

## 3. Blind Spot Detection

| Area | Covered By | Gap |
|------|-----------|-----|
| JavaScript in dashboard HTML (~1640 lines) | A04-001 (XSS), A17-001 (a11y) | No JS-specific code quality, memory leak, or correctness audit. Embedded JS is the largest code block. |
| `variants/` directory (10 files, 5534 lines) | A03-003 (dead code) | Not deeply analyzed — assumed dead code. Could contain useful patterns. |
| `implementation_timeline.json` | Not audited | Content and schema not validated. |
| `kpi_auth.py` (external dependency) | A06-003 | Not available for audit. |
| `build_gantt_draft.py` (455 lines) | Not audited | Purpose unclear — may be dead code like variants. |

## 4. Severity Calibration

| Finding | Original | Calibrated | Reason |
|---------|----------|-----------|--------|
| A01-001 / A09-001 / A31-001 | HIGH / CRITICAL / HIGH | **CRITICAL** | Core KPI calculation inconsistency — fundamental to project purpose |
| A03-001 | HIGH | HIGH | Maintainability concern but doesn't affect correctness |
| A04-003 | MEDIUM→HIGH | **HIGH** | Bind to 0.0.0.0 is a real security exposure |
| A09-002 | HIGH | HIGH | KPI gaming risk confirmed by A23-001 and A27-001 |
| A25-001 | LOW | LOW | Ethical concern but team is aware and consenting |
| A29-001 | MEDIUM | **LOW** | Python 3.14 works; the referenced path is just a local install |
