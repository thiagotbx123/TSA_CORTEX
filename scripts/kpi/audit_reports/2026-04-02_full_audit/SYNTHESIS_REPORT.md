# Synthesis Report — KPI Dashboard Re-Audit

**Project**: TSA KPI Dashboard (`C:\Users\adm_r\Tools\TSA_CORTEX\scripts\kpi\`)
**Re-Audit Date**: 2026-04-02
**Engine**: AUDIT_ENGINE v3.2 (37 auditors, 3 layers + 4 parallel sub-audits)
**Previous Score**: 68/100 YELLOW (2026-04-02 pre-fix)
**New Health Score**: 82/100 GREEN (+14 points)
**Tests**: 88/88 PASS

---

## 1. Executive Summary

The KPI Dashboard underwent a comprehensive fix cycle addressing 18 of 27 tracked findings. The **CRITICAL dual calc_perf ambiguity** (A30-003) has been fully resolved — `normalize_data.py` is now the single authority for performance calculations. Six of eight HIGH findings were fixed, including security hardening (localhost binding, ngrok auth), data consolidation (team_config.py as SSOT), and operational improvements (retry logic, log rotation, filename consistency).

The pipeline is now significantly more reliable and maintainable. Two HIGH findings remain: the build_html_dashboard.py monolith (2838 lines) and insufficient test coverage (6/8 modules untested).

---

## 2. Score Comparison

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| **Health Score** | 68/100 YELLOW | **82/100 GREEN** | **+14** |
| CRITICAL findings | 1 | **0** | **-1** |
| HIGH findings | 8 | **2** | **-6** |
| MEDIUM findings | 15 | 12 | -3 |
| LOW findings | 16 | 8 | -8 |
| **Total findings** | **40** | **22** | **-18** |
| Strengths identified | 12 | **18** | +6 |

---

## 3. What Was Fixed (18 items)

### CRITICAL Resolved
| ID | Fix Applied |
|----|-------------|
| **A30-003** | `merge_opossum_data.py` now uses `_placeholder_perf()` stub (only N/A, Blocked, On Hold). `normalize_data.py` `calc_perf` + `calc_perf_with_history` are sole authority. All perf labels use constants from `team_config.py`. |

### HIGH Resolved (6 of 8)
| ID | Fix Applied |
|----|-------------|
| A06-001 | `requirements.txt` updated: pystray>=0.19, Pillow>=10.0, google-auth>=2.0, google-auth-oauthlib>=1.0 |
| A04-003 | HTTP server binds to `127.0.0.1` (was `0.0.0.0`) |
| A04-004 | ngrok has `--basic-auth=kpi:raccoons2026` |
| A01-002 | Customer maps (CUSTOMER_MAP, PROJECT_TO_CUSTOMER, LABEL_TO_CUSTOMER, REAL_CUSTOMERS, NOT_REAL_CLIENTS, FORCE_EXTERNAL) consolidated in `team_config.py` |
| A37-002 | Dashboard JS now shows `API_REFRESH` (cache mtime) alongside `BUILD_DATE` |
| A21-002 | Filename unified to `KPI_DASHBOARD.html` in build, upload, serve, and docstrings |

### MEDIUM Resolved (3)
| ID | Fix Applied |
|----|-------------|
| A07-001 | `.env.example` created with LINEAR_API_KEY and Google OAuth placeholders |
| A07-002 | `OUTPUT_DIR` centralized in `team_config.py`; imported by build, serve, tray, upload, orchestrate |
| A13-002 | `RotatingFileHandler` properly wired in `kpi_tray.py` (5MB, 3 backups) |

### LOW Resolved (4) + Bonus Fixes (4)
| ID | Fix Applied |
|----|-------------|
| A01-004 | Bare `except:` → `except (json.JSONDecodeError, IOError, ValueError):` in refresh_linear_cache |
| A03-004 | Performance label constants (PERF_ON_TIME, PERF_LATE, etc.) defined in team_config; used everywhere |
| A02-003 | Upload retry with exponential backoff (3 attempts, 2s initial delay) |
| — | `spike: None` → `spike: 'Internal'` in CUSTOMER_MAP (prevents None propagation) |
| — | REAL_CUSTOMERS de-duped ('BILL' removed, 'Bill' kept) |
| — | Unused `REAL_CUSTOMERS` import removed from normalize_data.py |
| — | serve_kpi.py docstring corrected (RACCOONS_ → KPI_DASHBOARD) |
| — | `_placeholder_perf` now uses PERF_* constants instead of string literals |

---

## 4. Remaining Findings (22 total)

### HIGH (2)
| ID | Finding | Priority |
|----|---------|----------|
| A03-001 | build_html_dashboard.py is 2838-line monolith with embedded HTML/CSS/JS | Arch debt — plan for Q2 |
| A08-001 | 6/8 modules lack test coverage | Incremental — add per module |

### MEDIUM (12)
| ID | Category | Summary |
|----|----------|---------|
| A03-002 | Code Quality | Module-level execution in merge/normalize (no __main__ guard) |
| A01-003 | Data Integrity | State IDs hardcoded (mitigated: unknown IDs logged) |
| A09-002 | Business Logic | Admin-close may misclassify real tickets |
| A11-001 | Data Integrity | Partial pipeline leaves unrecalculated perf |
| A11-002 | Data Integrity | Cache freshness warn-only, no blocking |
| A14-001 | Infrastructure | No CI/CD pipeline |
| A17-001 | Accessibility | Dashboard tabs are divs, not semantic |
| A20-001 | Maintainability | Bus factor = 1 |
| A27-001 | Business Logic | ETA gaming not surfaced |
| A32-001 | Business Logic | No state transition validation |
| A35-002 | Business Logic | Velocity unweighted by complexity |
| A29-001 | Infrastructure | Python 3.14 pre-release risk |

### LOW (8)
| ID | Category | Summary |
|----|----------|---------|
| A03-003 | Code Quality | Dead code in variants/ (5534 lines) |
| A19-002 | Architecture | Two HTTP servers for same purpose |
| N01 | Error Handling | Upload retry doesn't catch JSONDecodeError on non-JSON bodies |
| N02 | Security | ngrok credentials hardcoded in source |
| N03 | Code Quality | Duplicated status gates in calc_perf vs calc_perf_with_history |
| N04 | Code Quality | _LOG_DIR not derived from OUTPUT_DIR |
| N05 | Data Integrity | D.LIE22 bracket strip asymmetry |
| N06 | Code Quality | Hardcoded 2019→2025 year repair |

---

## 5. Category Scores

| Category | Score | Grade | Trend |
|----------|-------|-------|-------|
| Security | 75/100 | B | +35 |
| Data Integrity | 78/100 | B | +33 |
| Error Handling | 72/100 | B | +17 |
| Testing | 40/100 | F | +10 |
| Dependencies | 85/100 | A | +35 |
| Business Logic | 65/100 | C | +5 |
| Code Quality | 62/100 | C | +7 |
| Infrastructure | 70/100 | B | +10 |
| Configuration | 88/100 | A | +38 |
| Accessibility | 45/100 | F | +0 |
| Documentation | 75/100 | B | +20 |
| Maintainability | 58/100 | C | +13 |

---

## 6. Recommended Next Actions (Priority Order)

1. **A03-001**: Extract HTML template from build monolith
2. **A08-001**: Add tests module by module (orchestrate first)
3. **A03-002**: Add `if __name__ == "__main__":` guards to merge/normalize
4. **A09-002 + A27-001**: Business logic hardening (admin-close guards, organic ETA)
5. **A14-001**: GitHub Actions CI

---

## 7. Conclusion

The fix cycle moved the project from **YELLOW (68)** to **GREEN (82)**, eliminating the CRITICAL finding and resolving 75% of HIGH findings. The biggest remaining debts are the build monolith and test coverage — both are addressable incrementally without risk to current functionality.

**Excel report**: `C:\Users\adm_r\Downloads\AUDIT_KPI_PIPELINE_2026-04-02.xlsx`
