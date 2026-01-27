# TMS Complete Learning - 2026-01-27

## Overview

This document captures all learnings from the Ticket Management System (TMS) creation process, including research findings, validation cycles, and corrections made.

---

## 1. Project Context

**Goal:** Create a comprehensive Ticket Management System SOP for TestBox TSA team
**Duration:** 2 days (2026-01-26 to 2026-01-27)
**Final Location:** [CODA Solutions Central](https://coda.io/d/Solutions-Central_djfymaxsTtA/Linear-Ticket-Management_sukx4jIV)

---

## 2. Research Methodology

### Sources Consulted (5 Parallel Agents)

| Source | Volume | Key Findings |
|--------|--------|--------------|
| **Slack** | 500+ TSA msgs, 10800 Thiago msgs | Real communication patterns, daily report format |
| **Linear API** | 20 teams, 100+ labels | Actual labels (Customer Issues, NOT Bug) |
| **Local Projects** | 14 mapped | SpineHUB methodology |
| **Obsidian** | Master Memory, 47+ sessions | Historical context |
| **Claude Sessions** | 11 global + specific | Previous decisions |

### Confidence Evolution

| Phase | Confidence | Notes |
|-------|------------|-------|
| Initial draft | 60% | Based on industry patterns |
| After deep learning | 90% | Real data verified |
| After user validation | 95% | Final corrections applied |

---

## 3. Critical Corrections Made

### 3.1 On-Call TSA - DOES NOT EXIST

**Original assumption:** TSA has on-call rotation for Sentry alerts
**Reality:** On-call is ONLY for developers (Eyji, Kalel)

**Evidence from Slack:**
> "toda semana tem dois devs definidos como on-call
> - nivel 1 (Eyji essa semana), responsavel por responder a alertas
> - nivel 2 (Kalel essa semana), serve como primeiro escalation point"

**Correction:** Sentry alerts go to #dev-on-call, handled by Developer on-call

---

### 3.2 Main Communication Channel

**Original assumption:** #tsa-internal is the main TSA channel
**Reality:** #scrum-of-scrums is the MAIN channel for TSA daily reports

**Evidence:** All daily reports from Thiago, Carlos, Diego, Gabrielle, Alexandra go to #scrum-of-scrums

**Correction:** Reference #scrum-of-scrums as primary channel

---

### 3.3 TSA Daily Meeting

**Original assumption:** TSA Daily is a synchronous meeting
**Reality:** TSA Daily is ASYNC - written reports on Slack

**Real TSA meeting structure:**
- 09:30: Diego 1:1
- 09:45: Gabrielle 1:1
- 10:00: Carlos 1:1
- 10:15: Alexandra 1:1
- 10:45: Sync escalation
- Thursday = no meeting day

**Correction:** Changed "TSA Daily" references to "#scrum-of-scrums daily report"

---

### 3.4 Linear Labels

**Labels that DON'T EXIST (verified via API):**
- Bug (use "Customer Issues")
- Technical Debt (use "Refactor")
- Worklog (doesn't exist)

**Labels that EXIST:**
- Customer Issues
- Feature
- Spike (3 instances)
- RCA
- Internal Request
- Customer Request
- Refactor

---

### 3.5 State Ownership

**Original:** "TSA owns until Refinement"
**Corrected:** "TSA owns until Backlog. Refinement is Engineering only."

**User validation:** Confirmed by Thiago - TSA hands off at Backlog, returns for Production QA

---

### 3.6 DoR/DoD Terminology

**Original:** "Definition of Ready (DoR)" / "Definition of Done (DoD)"
**Corrected:** "Before Creating a Ticket (Checklist)" / "Before Closing a Ticket (Checklist)"

**Reason:** TestBox doesn't use DoR/DoD acronyms formally

---

### 3.7 Key Contact Titles

**Lucas Wakigawa:**
- Original: "Solutions Manager"
- Corrected: "Tech Lead / Manager"

**Added contacts:**
- Katherine (Kat) - GTM Lead
- Lucas Soranzo - Engineering Lead

---

## 4. TMS Final Structure

```
A. The Flow (End-to-End)
   1. INTAKE - Request Sources
   2. TRIAGE - Priority Levels
   3. DUE DILIGENCE - Investigation Checklist
   4. TICKET CREATION - Format & Standards
   5. EXECUTION - State Flow & Ownership
   6. MONITORING - Follow-up Standards
   7. VALIDATION → DELIVERY → CLOSEOUT

B. Critical Visibility Protocol
   - Escalation rules
   - Sam's guidance quote
   - KPI tracking

C. Who Does What (RACI Matrix)
   - Requestor, TSA, Eng, GTM columns
   - No separate QA column (QA done by TSA + Dev)

D. Linear Standard
   - Priorities (P0-P3)
   - Labels (corrected)
   - Checklists (pre-creation, pre-close)

E. Templates (11 types)
   - RAC-44 through RAC-54

F. Resources & Contacts
```

---

## 5. Templates Created

| # | Template | Linear ID | Use Case |
|---|----------|-----------|----------|
| 1 | Bug | RAC-44 | Something broke |
| 2 | Feature | RAC-45 | New functionality |
| 3 | Spike | RAC-46 | Investigation |
| 4 | RCA | RAC-47 | Post-incident |
| 5 | Internal | RAC-48 | Internal request |
| 6 | Customer | RAC-49 | Customer request |
| 7 | Tech Debt | RAC-50 | Refactoring |
| 8 | Deploy | RAC-51 | Release |
| 9 | Onboarding | RAC-52 | Customer setup |
| 10 | Worklog | RAC-53 | Documentation |
| 11 | Implementation | RAC-54 | Feature build |

---

## 6. Key Quotes Discovered

### Sam Senior (CEO) on Escalation:
> "When you are stuck for more than a couple of hours, please escalate quickly to the GTM owner. This is not a failure or incompetence. It shows ownership and care."

### Core Philosophy:
> "Silence is the only unacceptable behavior."

---

## 7. Process Learnings

### What Worked Well
1. **Parallel agent research** - 5 sources simultaneously = comprehensive data
2. **User validation loop** - 4 key questions answered = 100% confidence
3. **API verification** - Linear API confirmed labels, states
4. **Iterative refinement** - v1.0 → critical analysis → v2.0

### What to Improve
1. **Don't assume industry patterns** - TestBox has its own culture
2. **Verify channels exist AND are active** - #tsa-internal exists but unused
3. **Ask about terminology** - DoR/DoD not used, "checklist" is better
4. **Check real people titles** - Lucas = Tech Lead, not Solutions Manager

---

## 8. Files Generated

| File | Location | Purpose |
|------|----------|---------|
| TMS v2.0 | `knowledge-base/sops/ticket-management-system-v2.md` | Local reference |
| Critical Analysis | `Downloads/TMS_CRITICAL_ANALYSIS.md` | Initial analysis |
| Analysis with Real Data | `Downloads/TMS_ANALYSIS_WITH_REAL_DATA.md` | Post-research findings |
| Templates Table | `Downloads/templates_table_for_coda.md` | CODA-ready format |
| CODA Final | `Downloads/TMS_CODA_FINAL.md` | Extracted from live CODA |

---

## 9. Integration Points

### CODA
- Document: Solutions Central
- Page: Linear Ticket Management
- URL: https://coda.io/d/Solutions-Central_djfymaxsTtA/Linear-Ticket-Management_sukx4jIV

### Linear
- Team: PLA (Platypus) for production
- Team: RAC (Raccoons) for templates
- Templates: RAC-44 to RAC-54

### Slack Channels
- #scrum-of-scrums - Daily reports (MAIN)
- #customer-requests - Customer incoming
- #dev-on-call - Urgent/on-call

---

## 10. Future Improvements

1. **Add Meetings section to CODA** - C. Meetings & Rituals not yet added
2. **Update version to 2.0** - CODA still shows 1.0
3. **Sync templates with corrected labels** - Use "Customer Issues" not "Bug"
4. **Add daily report format** - Template for #scrum-of-scrums posts

---

## Metadata

**Created:** 2026-01-27
**Author:** Thiago Rodrigues + Claude
**Confidence:** 95%
**Next Review:** When process changes

---

*This learning document ensures knowledge is preserved for future sessions and team members.*
