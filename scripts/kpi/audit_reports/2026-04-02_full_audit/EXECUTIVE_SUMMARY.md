# Executive Summary — KPI Dashboard Audit

**Project**: TSA KPI Dashboard (scripts/kpi/)
**Audit Date**: 2026-04-02
**Engine**: AUDIT_ENGINE v3.1 (37 auditors, 3 layers)
**Health Score**: 68/100 🟡 YELLOW

## Assessment

The KPI Dashboard is a functional, well-documented internal tool with strong data integrity rules (59+ documented rules) and iterative quality improvement. However, its core metric — ETA Accuracy (KPI1) — has a **critical calculation inconsistency** where the same metric is computed differently in two pipeline stages using different ETA baselines. This undermines confidence in the dashboard's primary purpose.

Secondary concerns include: **phantom dependencies** preventing clean installs, **6 of 8 core modules lacking tests**, **configuration fragmented across 6+ files**, and a **security exposure** from the HTTP server binding to all interfaces.

## Top 5 Findings

| # | Severity | Finding | Fix Effort |
|---|----------|---------|-----------|
| 1 | **CRITICAL** | Dual calc_perf with different ETA baselines — KPI1 calculation path is ambiguous | 2 hours |
| 2 | **HIGH** | Phantom dependencies (pystray, Pillow not in requirements.txt) | 5 minutes |
| 3 | **HIGH** | 6/8 core modules have zero test coverage + no CI | 4 hours |
| 4 | **HIGH** | HTTP server binds to 0.0.0.0 + ngrok has no auth | 10 minutes |
| 5 | **HIGH** | Customer mapping in 3 separate locations + file naming inconsistency | 1 hour |

## Recommended Immediate Actions

1. **Remove `calc_perf` call from `merge_opossum_data.py`** — normalize always recalculates. Eliminates the CRITICAL finding.
2. **Add pystray and Pillow to `requirements.txt`**
3. **Change `kpi_tray.py` L194 from `0.0.0.0` to `127.0.0.1`**
4. **Unify `KPI_DASHBOARD.html` / `RACCOONS_KPI_DASHBOARD.html` naming**
5. **Consolidate customer maps into `team_config.py`**

**Full report**: `audit_reports/2026-04-02_full_audit/SYNTHESIS_REPORT.md`
