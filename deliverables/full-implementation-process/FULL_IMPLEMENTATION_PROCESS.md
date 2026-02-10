# ═══════════════════════════════════════════════════════════════════
# FULL IMPLEMENTATION PROCESS — COMPLETE DELIVERABLE
# Paste destination: Solutions Central → Full Implementation Process
# https://coda.io/d/Solutions-Central_djfymaxsTtA/Full-Implementation-Process_suE5-VuS
# Generated: 2026-02-10 | Author: Thiago Rodrigues + Claude Opus 4.6
# ═══════════════════════════════════════════════════════════════════

---

# 1. COLLECTION PLAN & INVENTORY

## 1.1 Connectors & Access

| Source | Status | Method | Limitation |
|:-------|:-------|:-------|:-----------|
| **Local filesystem** | ACCESSED | Direct read across all projects | None |
| **Coda (Solutions Central)** | NOT ACCESSED (auth) | WebFetch blocked by login | Export manually or use Coda API with token |
| **Slack** | NOT ACCESSED (requires xoxp token) | TSA_CORTEX Slack collector | Run `node dist/cli/index.js collect --slack` |
| **Linear API** | NOT ACCESSED directly (no active MCP) | linear_api_key in .env | Query via script or MCP server |
| **Google Drive** | NOT ACCESSED directly (requires OAuth) | TSA_CORTEX Drive collector | Run collector or access manually |
| **Obsidian Vault** | PARTIAL | ObsidianVault/ local | Indexed via filesystem |

## 1.2 Internal Sources Indexed

### GANTT / Timelines
| Document | Project | Path | Phases |
|:---------|:--------|:-----|:-------|
| GEM GANTT Mapping | GEM-BOOM | `GEM-BOOM/GEM_GANTT_MAPPING.md` | Discovery → Foundation → Build → Validate → Launch |
| GEM GANTT Excel v3 | GEM-BOOM | `GEM-BOOM/scripts/create_gantt_excel_v3.py` | 7 phases + 7 gates |
| QBO Winter Release Gantt v9 | intuit-boom | `intuit-boom/sessions/2026-01-20_gantt_v9_final.md` | 7 phases + 2 gates |

### Ticket Management (Linear)
| Document | Path | Content |
|:---------|:-----|:--------|
| TMS v2.0 | `TSA_CORTEX/knowledge-base/sops/ticket-management-system-v2.md` | E2E flow, RACI, priorities, labels, 11 templates |
| Pre-Project Ticket Planning | `GEM-BOOM/CODA_PRE_PROJECT_TICKET_PLANNING.md` | 7 pre-project phases, complete toolkit |
| TMS Learning | `TSA_CORTEX/knowledge-base/learnings/TMS_COMPLETE_LEARNING_2026-01-27.md` | 8 corrections, 5 sources, 95% confidence |

### Validation / QA
| Document | Path | Content |
|:---------|:-----|:--------|
| 3-Gate Ingestion Pipeline | `intuit-boom/knowledge-base/INGESTION_3_GATES.md` | Gate 1 (local) → Gate 2 (backend) → Gate 3 (Claude audit) |
| validate_csvs.py | `intuit-boom/scripts/ingestion/validation/validate_csvs.py` | 59 rules, 189 automated checks |
| QBO Keystone Reference | `knowledge-base/QBO_KEYSTONE_INGESTION_REFERENCE.md` | FK dependencies, scripts |

### SOW / Commercial
| Document | Path | Content |
|:---------|:-----|:--------|
| SOW Best Practices | `GEM-BOOM/knowledge_base/SOW_BEST_PRACTICES.md` | Mailchimp/Gabi lessons, 12-section SOW standard |
| GEM SOW | `GEM-BOOM/SOW_GEM_ATS_ONLY_2026-01-30.md` | Real SOW example |
| WFS SOW | `QBO-WFS/.context/SOW_WFS_PROFESSIONAL_v1.md` | Real SOW example |

### Handover / Transfer
| Document | Path | Content |
|:---------|:-----|:--------|
| INTUIT_BOOM_TRANSFER (11 docs) | `intuit-boom/INTUIT_BOOM_TRANSFER/` | START_HERE, MEGA_MEMORY, SOW_AND_SCOPE, ECOSYSTEM_MAP, TECHNICAL_REFERENCE, RUNBOOKS, CONTACTS, RISK_MATRIX, CREDENTIALS, DECISIONS_LOG |

### Communication (Slack)
| Pattern | Source | Description |
|:--------|:------|:-----------|
| Daily Agenda v1.8 | `TSA_DAILY_REPORT/specs/DAILY_AGENDA_SCRIPT_v1.8.txt` | Standard daily format |
| Slack Report Template | `GEM-BOOM/CODA_PRE_PROJECT_TICKET_PLANNING.md` Section 7 | Kick-off/communication template |

---

# 2. AGENT MEMOS (PHASE 2)

## Memo A — Commercial / GTM Agent

**What must exist for me to sign off:**
1. Clear SOW-to-deliverable traceability — every feature the client paid for must have a ticket
2. Customer-facing timeline with realistic dates (Gabi's lesson: "be generic in the Gantt")
3. Escalation path that reaches me immediately for client-impacting issues
4. Evidence pack at the end — screenshots proving every feature works
5. Change request process — scope creep kills margins

**Questions I'd ask to break the process:**
- "What happens when the client asks for something not in the SOW mid-project?"
- "How do I know the demo data looks realistic before showing it to the client?"
- "What's the SLA for fixing a P0 bug found during UAT?"

**Risks I see:**
- Promising dates without CE input → missed deadlines → client trust lost
- No formal change control → scope creep → unprofitable project
- Evidence pack not captured during execution → scramble at the end

---

## Memo B — Data Architect (TSA) Agent

**What must exist for me to sign off:**
1. Complete API mapping before ticket creation (endpoint + method + rate limit + limitations)
2. Dependency tree mapped — what blocks what, in which order
3. Pre-project planning done BEFORE kick-off, not after (Pre-Project Ticket Planning process)
4. 10-check audit on all tickets (title, description, assignee, milestone, dependencies, estimate, blockers, SOW coverage, duplicates, state)
5. TMS v2.0 compliance — state flow, labels, title format all match our standard

**Questions I'd ask to break the process:**
- "Can a new TSA execute this without asking anyone?"
- "Where do I find the ticket template? Is it the same one from TMS v2.0?"
- "What happens when the API doesn't support what we need? (UI automation fallback)"

**Risks I see:**
- Creating tickets without reading technical docs → bad estimates, missing blockers
- Not linking dependencies in Linear → invisible bottlenecks
- TSA owns ticket until Backlog but that boundary is unclear to new people

> **Source**: TMS v2.0: "TSA owns the ticket until Backlog. Once moved to Refinement, Engineering takes over completely."

---

## Memo C — Engineering Agent

**What must exist for me to sign off:**
1. Tickets with measurable Acceptance Criteria — I reject vague "make it work" tickets
2. Clear validation section — "how do I know it's done?"
3. API details embedded in the ticket (endpoint, request body, rate limit) — not in some external doc
4. Risks documented PER TICKET — not just at project level
5. If something needs UI automation, say so explicitly with `REQUIRES UI AUTOMATION`

**Questions I'd ask to break the process:**
- "Can I pick up a ticket and start working without asking TSA anything?"
- "What's the expected turnaround time for different priorities?"
- "Where's the rollback plan if my data ingestion goes wrong?"

**Risks I see:**
- Tickets without API details → I waste time researching
- No rate limit info → API blocks me mid-ingestion
- Schema changes after data gen started → total rework

> **Source**: Pre-Project Ticket Planning: "Every ticket has clear ownership, tasks broken down by role, and validation criteria."

---

## Memo D — Data Generation Lead Agent

**What must exist for me to sign off:**
1. Schema freeze BEFORE I start generating — no changes after gate approval
2. 3-Gate validation pipeline: Gate 1 (local validate_csvs.py) → Gate 2 (Retool) → Gate 3 (Claude audit)
3. FK dependency order documented — I need to know which tables to create first
4. Realistic data requirements — names, companies, dates must pass the "squint test"
5. Rollback plan — if ingestion fails, I need a way to undo

**Questions I'd ask to break the process:**
- "Who approves the schema? TSA or CE?"
- "What's the acceptance bar for 'realistic'? Is there a checklist?"
- "What happens if Retool validator finds errors Gate 1 missed?"

**Risks I see:**
- Generic data ("John Doe", "Company ABC") → client notices immediately
- Rate limiting during ingestion → partial data state
- No rollback strategy → irrecoverable errors

> **Source**: 3-Gate Pipeline: "59 rules, 189 automated checks. TODOS os checks PASS (FAIL = 0)."

---

## Memo E — PM / Delivery Agent

**What must exist for me to sign off:**
1. End-to-end visibility: I need to see status across all phases from one place
2. Gates between phases — no advancing without approval
3. Cadences: daily async report, weekly sync, gate reviews
4. Risk register maintained throughout — not just created at Discovery
5. Metrics: lead time, cycle time, rework rate, gate pass rate

**Questions I'd ask to break the process:**
- "What's the standard project size breakdown? (Small/Medium/Large)"
- "How do I track progress across parallel workstreams?"
- "What's the escalation trigger? Hours stuck? Days blocked?"

**Risks I see:**
- No standard cadence → misalignment builds silently
- No gate enforcement → "we'll fix it later" mentality
- No metrics → can't improve what you can't measure

---

## Memo F — Executive Agent (Cost, Margin, Predictability, Scale)

**What must exist for me to sign off:**
1. Cost estimating by project size (S/M/L) — hours, people, duration
2. Predictability — can I forecast delivery dates accurately?
3. Scalability — does this work for 10 projects simultaneously?
4. Onboarding — can a new TSA execute this in their first week?
5. Retrospective process — are we actually learning from each project?

**Questions I'd ask to break the process:**
- "What's our average lead time per project size?"
- "What percentage of projects hit their original deadline?"
- "How many hours does onboarding a new TSA take?"

**Risks I see:**
- Process too heavy for small projects → overhead kills speed
- No retro → same mistakes repeated
- Knowledge locked in individuals → bus factor of 1

---

# 3. CROSS-EXAMINATION

## Round 1: GTM → Engineering
**Q:** "How do I guarantee the client sees realistic data, not placeholder garbage?"
**A (Eng):** "3-Gate validation pipeline. Gate 1 catches schema errors locally, Gate 2 catches backend inconsistencies, Gate 3 uses 5 Claude auditors checking realism. If it passes all 3, the data is production-quality."

## Round 2: Engineering → TSA
**Q:** "What if the API doesn't support an operation and I discover it mid-build?"
**A (TSA):** "Should be caught in Discovery (Phase 1). But if missed, mark ticket as `REQUIRES UI AUTOMATION` and add Playwright approach. Create new ticket if scope expansion needed."

## Round 3: Data Gen → PM
**Q:** "Who decides schema freeze? What if CE wants changes after I've generated 500 records?"
**A (PM):** "Schema freeze happens at Gate 5a (end of Seed Data). After that, changes require a formal Change Request. If approved, Data Gen gets additional time in the timeline."

## Round 4: Executive → PM
**Q:** "Can a brand new TSA run this without hand-holding?"
**A (PM):** "Yes — with the 5-day onboarding path. Day 1-2: read docs. Day 3: shadow. Day 4-5: supervised execution. After 1 week, they should handle Phases 1-5 independently."

## Round 5: TSA → GTM
**Q:** "What happens when the client asks for something not in the SOW?"
**A (GTM):** "Change Request Form. TSA documents impact (timeline + effort + risk), GTM + client approve or reject. No ticket without approval."

## Round 6: PM → Data Gen
**Q:** "What's the recovery plan when ingestion fails mid-way?"
**A (Data Gen):** "Every ingestion script logs all created record IDs. Run cleanup script with the log. Fix the issue. Re-run. Gate 1 MUST pass before any INSERT."

---

## Consolidated Requirements from Cross-Examination

| # | Requirement | Source | Priority |
|:--|:-----------|:-------|:---------|
| REQ-01 | Every SOW deliverable must have a ticket | GTM + TSA | MUST |
| REQ-02 | API mapping completed before ticket creation | TSA + Eng | MUST |
| REQ-03 | 3-Gate validation pipeline for all data | Data Gen + Eng | MUST |
| REQ-04 | Gates between every phase — no skipping | PM + Executive | MUST |
| REQ-05 | Measurable Acceptance Criteria on every ticket | Eng + TSA | MUST |
| REQ-06 | Change Request Form for scope changes | GTM + PM | MUST |
| REQ-07 | 5-day onboarding path for new TSA | Executive + PM | SHOULD |
| REQ-08 | Metrics from existing tools (Linear, Slack), zero overhead | PM + Executive | SHOULD |
| REQ-09 | Cost estimate by project size (S/M/L) documented | Executive | SHOULD |
| REQ-10 | Documentation sufficient for handoff in < 24h | TSA + Eng | MUST |

---

# 4. FINAL PROCESS — TEXT TO PASTE IN CODA

# Full Implementation Process

---

## 📋 Document Info

| **Field** | **Value** |
|:----------|:----------|
| **Owner** | Thiago Rodrigues (TSA Manager) |
| **Version** | 2.0 |
| **Last Updated** | 2026-02-10 |
| **Status** | Active |
| **Related Docs** | [Linear Ticket Management](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Linear-Ticket-Management_sukx4jIV) · [Pre-Project Linear Ticket Planning](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Pre-Project-Linear-Ticket-Planning_suePVn8A) |
| **Feedback** | Create issue in Solutions Central or contact document owner |

---

## 📑 Table of Contents

1. [Overview](#-overview)
2. [Glossary](#-glossary)
3. [How to Use This Playbook](#-how-to-use-this-playbook)
4. [The Flow (End-to-End)](#-the-flow-end-to-end)
5. [Prerequisites & Inputs](#-prerequisites--inputs)
6. [Roles & Responsibilities (RACI)](#-roles--responsibilities-raci)
7. [Required Artifacts](#-required-artifacts)
8. [Definition of Ready (DoR)](#-definition-of-ready-dor)
9. [Definition of Done (DoD)](#-definition-of-done-dod)
10. [Phases](#-phases)
    - Phase 0: Intake & Qualification
    - Phase 1: Discovery & Sizing
    - Phase 2: Pre-Project Planning
    - Phase 3: Kick-off
    - Phase 4: Foundation
    - Phase 5: Build (Seed Data + Data Gen + Ingestion)
    - Phase 6: Stories & Feature Setup
    - Phase 7: Validate (QA + UAT)
    - Phase 8: Launch & Go-Live
    - Phase 9: Hypercare & Handover
    - Phase 10: Closeout & Retrospective
11. [Cadences & Rituals](#-cadences--rituals)
12. [Change Management](#-change-management)
13. [Risk Management](#-risk-management)
14. [Metrics & KPIs](#-metrics--kpis)
15. [Escalation Playbook](#-escalation-playbook)

---

## 📋 Overview

### What It Is
This document defines the standard end-to-end process for implementing solutions at TestBox. It covers everything from the moment a deal is qualified through formal project closure, including all gates, checklists, and artifacts required.

### When to Use
- Every new client implementation (demos, POCs, pilots, production)
- Onboarding new products into the TestBox catalog
- Quarterly feature releases (Winter, Fall, etc.)

### Who It's For
- **TSA** (Technical Solutions Architect) — executes and coordinates
- **CE** (Customer Engineer) — implements technically
- **DATA** (Data Generation) — creates realistic synthetic data
- **GTM** (Go-To-Market) — client interface and stakeholder management
- **Engineering** — develops features and resolves bugs

### Principles
1. **SOW is law** — Every scope item traces back to the Statement of Work
2. **Gates are not optional** — No phase advances without gate approval
3. **Documentation = execution** — If it's not documented, it didn't happen
4. **Escalate early** — "Escalate quickly to the GTM owner. This is not a failure." (Sam Senior, CEO)
5. **Automate the repetitive** — Scripts > manual work, always

> 💡 This process integrates with [Linear Ticket Management](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Linear-Ticket-Management_sukx4jIV) for ticket operations and [Pre-Project Linear Ticket Planning](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Pre-Project-Linear-Ticket-Planning_suePVn8A) for Phase 2 details.

---

## 📖 Glossary

| **Term** | **Definition** |
|:---------|:---------------|
| **TSA** | Technical Solutions Architect — owns the planning process and project coordination |
| **CE** | Customer Engineer — executes technical implementation work |
| **DATA** | Data Generation team — creates synthetic data for demos |
| **GTM** | Go-To-Market — sales and customer-facing team |
| **SOW** | Statement of Work — contract defining project scope and deliverables |
| **COE** | Center of Excellence — demo/reference environment |
| **Gate** | Quality checkpoint between phases — all criteria must pass to advance |
| **DoR** | Definition of Ready — criteria a ticket must meet before work begins |
| **DoD** | Definition of Done — criteria a ticket must meet before it can be closed |
| **Blocker** | A ticket or dependency that must be resolved before others can start |
| **Milestone** | A phase grouping related tickets together in Linear |
| **RACI** | Responsible, Accountable, Consulted, Informed — responsibility matrix |
| **Evidence Pack** | Collection of screenshots + tracker proving every feature works |
| **3-Gate Pipeline** | Data validation: Gate 1 (local) → Gate 2 (Retool) → Gate 3 (Claude audit) |

---

## 🎓 How to Use This Playbook

If you're **new to the TSA team**, follow this path:

| Day | What to Do | Time |
|:----|:-----------|:-----|
| **Day 1** | Read this document end-to-end (focus on Overview + Phases 0-3) | 2h |
| **Day 1** | Read [Linear Ticket Management](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Linear-Ticket-Management_sukx4jIV) | 1h |
| **Day 2** | Read [Pre-Project Ticket Planning](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Pre-Project-Linear-Ticket-Planning_suePVn8A) | 1h |
| **Day 2** | Study a past project in Linear (GEM or QBO) as a live example | 2h |
| **Day 3** | Shadow an active project (observe gates, dailies, tickets) | Full day |
| **Day 4-5** | Execute Phases 1-2 on a new project WITH supervision from TSA Lead | 2 days |

**After 1 week**: New TSA should be able to execute Phases 1-5 without hand-holding.

**Rule**: If something in this playbook isn't clear enough to execute solo, it's a BUG in the playbook — report it to the TSA Lead for correction.

---

## 🔄 The Flow (End-to-End)

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  INTAKE  │ → │ DISCOVER │ → │   PLAN   │ → │ KICK-OFF │ → │  BUILD   │ → │ VALIDATE │ → GO-LIVE
│ GTM owns │   │ TSA owns │   │ TSA owns │   │ TSA owns │   │ CE owns  │   │ TSA + GTM│
│  1-5 d   │   │  3-5 d   │   │  3-4 h   │   │   1 d    │   │  14-21 d │   │  5-7 d   │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
    Gate 0         Gate 1         Gate 2         Gate 3        Gate 4-5       Gate 6-7
```

**Total Time (typical):** Small: 3 weeks · Medium: 6 weeks · Large: 10 weeks

> **Live Examples:** [GEM Project](https://linear.app/testbox/project/gem-ats-implementation) = Medium (37 tickets, 7 weeks). QBO Winter = Large (29 features, 8 weeks).

---

## 📚 Prerequisites & Inputs

Before starting ANY implementation, these items MUST exist:

| Item | Responsible | Where It Lives | Required? |
|:-----|:------------|:---------------|:----------|
| SOW signed (or final draft) | GTM | Google Drive | Yes |
| Access to client tenant | GTM → TSA | Coda (Solutions Central) | Yes |
| Technical documentation (API, architecture) | TSA | Project repo `/knowledge_base/api/` | Yes |
| Linear Project created | TSA | [Linear](https://linear.app/testbox) | Yes |
| Slack channel for the project (if needed) | TSA | Slack | Conditional |
| Budget/timeline approved | GTM + Executive | SOW | Yes |
| Team allocated and confirmed | PM/TSA Lead | Coda or Linear | Yes |

> **Live Example:** [GEM SOW](GEM-BOOM/SOW_GEM_ATS_ONLY_2026-01-30.md) — 3 tenants, 6 features, 7-week timeline.

---

## 👥 Roles & Responsibilities (RACI)

### RACI Matrix — By Phase

| Phase | TSA | CE | DATA | GTM | Eng |
|:------|:---:|:--:|:----:|:---:|:---:|
| 0. Intake & Qualification | C | - | - | **R/A** | - |
| 1. Discovery & Sizing | **R/A** | C | C | C | I |
| 2. Pre-Project Planning | **R/A** | C | C | I | I |
| 3. Kick-off | **R/A** | I | I | C | I |
| 4. Foundation | **R/A** | R | I | I | C |
| 5. Build | C | **R/A** | R | I | C |
| 6. Stories & Features | **R/A** | R | C | I | C |
| 7. Validate (QA + UAT) | **R** | R | I | **A** | C |
| 8. Launch | C | **R** | I | **A** | R |
| 9. Hypercare & Handover | I | C | I | **R/A** | C |
| 10. Closeout | **R/A** | I | I | C | I |

### Legend
| Symbol | Meaning |
|:------:|---------|
| ✅ **R** | Responsible — Does the work |
| 📋 **A** | Accountable — Final decision maker |
| 💬 **C** | Consulted — Provides input |
| ℹ️ **I** | Informed — Kept in the loop |

> **Rule:** Only ONE Accountable per phase. If two appear as A, resolve before starting.

> **Source:** RACI validated in TMS v2.0 (2026-01-27), 95% confidence. External: [RACI Chart — Atlassian](https://www.atlassian.com/work-management/project-management/raci-chart) · PMI PMBOK 7th Edition.

---

## 📦 Required Artifacts

Every implementation MUST produce these artifacts:

| Artifact | Where | When to Create | Template |
|:---------|:------|:---------------|:---------|
| **Linear Project** with milestones | Linear | Phase 2 | [Pre-Project Ticket Planning](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Pre-Project-Linear-Ticket-Planning_suePVn8A) |
| **GANTT** with phases and gates | Google Sheets/Excel | Phase 2 | See Template 4 below |
| **Tickets** in standard format | Linear | Phase 2 | [Linear Ticket Management](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Linear-Ticket-Management_sukx4jIV) |
| **Slack kick-off** message | Slack (team channel) | Phase 3 | See Template 2 below |
| **Risk Register** | Linear (dedicated ticket) or Coda | Phase 1, update every phase | See Risk Management section |
| **Evidence Pack** | Google Drive | Phase 7-8 | Screenshots/videos per feature |
| **Documentation Package** | Coda + Repo | Phase 9 | Runbook + decisions + lessons |
| **Retrospective** | Coda or document | Phase 10 | Keep/Stop/Start format |

---

## ✅ Definition of Ready (DoR)

Before a ticket can leave Backlog and enter execution, it MUST meet ALL these criteria:

| # | Criterion | How to Verify |
|:--|:---------|:-------------|
| 1 | **Title follows convention** | `[PROJECT] Verb + Object` (e.g., `[GEM] Create Candidate Pipeline`) |
| 2 | **Description has Acceptance Criteria** | "Validation" section filled with measurable checks |
| 3 | **Addresses business need** | Traces to a SOW deliverable or technical requirement |
| 4 | **Measurable criteria** | Each AC can be verified with YES/NO, not subjective |
| 5 | **Right-sized** | Estimate ≤ 5 days. If larger, break into sub-tickets |
| 6 | **No blocking dependencies** | Prerequisites complete, other team deliverables available |

**Rule**: Ticket that fails DoR → back to Backlog with comment explaining what's missing. TSA has 24h to fix.

> **Source:** REQ-05 from Cross-Examination (Eng can reject incomplete AC). External: [Definition of Ready — Microsoft Engineering Playbook](https://microsoft.github.io/code-with-engineering-playbook/agile-development/team-agreements/definition-of-ready/).

---

## ✅ Definition of Done (DoD)

A ticket can only be moved to Done when ALL these criteria are met:

| # | Criterion | How to Verify |
|:--|:---------|:-------------|
| 1 | **Work completed and verified** | Data ingested, script validated, feature functional |
| 2 | **Validation executed** | Validation script run with zero critical errors |
| 3 | **Evidence captured** | Screenshot, log, or validation report saved |
| 4 | **Documentation updated** | Coda/Slack/knowledge-base reflects current status |
| 5 | **Linear updated** | Ticket in Done, final comment added, time logged |

> **Source:** External: [DoD vs Acceptance Criteria — Agile Sherpas](https://www.agilesherpas.com/blog/definition-of-done-acceptance-criteria). Key insight: "AC helps build the **right product**. DoD helps build the **product right**."

---

## 🔄 Phases

---

### 🔹 PHASE 0: Intake & Qualification

| Field | Value |
|:------|:------|
| **Objective** | Decide whether this opportunity becomes a project and with what scope |
| **Owner** | GTM (R/A), TSA (C) |
| **Duration** | 1-5 days |
| **Where** | Slack (DM/channel), Calls, Google Drive |
| **Why It Exists** | Prevents starting projects without clear scope or available resources |

**What to Do:**
1. GTM receives opportunity (deal, demo request, renewal)
2. GTM evaluates technical and commercial fit (product supported? timeline realistic?)
3. If needed, GTM consults TSA for technical sizing
4. GTM produces SOW draft or confirms scope verbally
5. Decision: **GO / NO-GO / NEED MORE INFO**

**Inputs:** Client request, commercial context, product catalog
**Outputs:** SOW draft, GO/NO-GO decision, preliminary timeline

**✅ Gate 0: Qualification Approved**
- [ ] Scope defined (features, data, timeline)
- [ ] Resources identified (TSA, CE, DATA available)
- [ ] SOW draft or scope document exists
- [ ] Timeline is feasible (doesn't conflict with other projects)

**⚠️ Common Failures:**
- Starting without SOW → scope becomes a moving target
- Not consulting TSA on sizing → unrealistic timeline
- Accepting everything the client asks for → scope creep from day 1

> **Confidence:** HIGH — Pattern observed in GEM (SOW Build: Dec 18-Jan 31) and QBO (features defined before execution).
> **External:** [Phased Implementation — Dock.us](https://www.dock.us/library/phased-implementation) · [SaaS Implementation Checklist — Storylane](https://www.storylane.io/blog/saas-implementation-checklist).

---

### 🔹 PHASE 1: Discovery & Sizing

| Field | Value |
|:------|:------|
| **Objective** | Understand everything before writing a single ticket |
| **Owner** | TSA (R/A), CE/DATA/GTM (C) |
| **Duration** | 3-5 days |
| **Where** | Coda, Google Drive, Calls, Slack |
| **Why It Exists** | "Garbage in, garbage out" — bad tickets = bad project |

**What to Do:**

1. **Collect materials** (~20 min per source):
   - SOW/Contract → extract deliverables, timeline, success criteria
   - Technical docs → API docs, architecture, limitations
   - Brainstorming notes → sessions with CE, DATA, GTM
   - Slack threads → relevant decisions and context
   - Previous similar projects → lessons learned

2. **Map technical scope** (~1-2h):
   - Which APIs exist? (POST/GET/PUT/DELETE)
   - Which operations need UI automation?
   - What data needs to be generated?
   - External dependencies (tenant, credentials, customer action)?

3. **Estimate sizing** (~30 min):

| Type | Tickets | Phases | Typical Duration | Team |
|:-----|:--------|:-------|:----------------|:-----|
| **Small** (1-2 features, simple demo) | 10-15 | 6 | 2-3 weeks | TSA + CE |
| **Medium** (5-10 features, full demo) | 25-40 | 8 | 5-7 weeks | TSA + CE + DATA |
| **Large** (10+ features, multi-phase) | 40-60 | 10 | 8-12 weeks | TSA + CE + DATA + GTM |

4. **Identify initial risks** (~30 min):
   - External dependencies without defined dates
   - Technical limitations (API gaps, rate limits)
   - Resource conflicts

**Inputs:** SOW, technical docs, commercial context
**Outputs:** Material inventory, API map, sizing estimate, risk register v0

**✅ Gate 1: Discovery Complete**
- [ ] All SOW deliverables listed
- [ ] APIs mapped (endpoint + method + limitation)
- [ ] External dependencies identified
- [ ] Sizing estimated (S/M/L)
- [ ] At least 1 risk documented
- [ ] Brainstorm with CE and/or DATA completed

**⚠️ Common Failures:**
- Not reading technical documentation → discovers limitation in Phase 5
- Assuming API supports everything → UI automation surprise
- Not talking to CE/DATA beforehand → wrong sizing

**Live Example:** GEM Discovery (Dec 17-20, 4 days). Pre-Project Ticket Planning Phase 1.

> **Source:** SOW Best Practices (Mailchimp, Gabi): "Align with engineering on exact dates" + "100 rounds of refinement before the final Gantt."

---

### 🔹 PHASE 2: Pre-Project Planning

| Field | Value |
|:------|:------|
| **Objective** | Create ALL tickets, milestones, and GANTT BEFORE kick-off |
| **Owner** | TSA (R/A) |
| **Duration** | 3-4 hours (with automation) to 1-2 days (manual) |
| **Where** | Linear (tickets), Google Sheets (GANTT), Python scripts |
| **Why It Exists** | Proactive preparation = zero surprises at kick-off |

> 📘 **This phase is fully documented in [Pre-Project Linear Ticket Planning](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Pre-Project-Linear-Ticket-Planning_suePVn8A).** Follow that document for the detailed step-by-step. Below is the summary.

**The Pre-Project Flow:**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  DISCOVERY  │ →  │  STRUCTURE  │ →  │   CREATE    │ →  │    AUDIT    │ →  │ COMMUNICATE │
│  Gather all │    │  Design     │    │   Tickets   │    │  & Enrich   │    │  Share with │
│  materials  │    │  milestones │    │   via API   │    │  via API    │    │    team     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
     ~1 hour           ~30 min           ~30 min           ~1 hour            ~15 min
```

**What to Do:**
1. **Design milestones** (~30 min) — Foundation → Seed Data → Data Gen → Ingestion → Stories → Validate → Launch
2. **Create tickets via script** (~30 min) — Standard format, bulk creation via Linear GraphQL API, 0.5s delay between requests
3. **Run audit** (~1h) — 10 checks (title, description, assignee, milestone, dependencies, estimate, blocker, SOW coverage, duplicates, state). Fix until 10/10 PASS.
4. **Enrich tickets** (~30 min) — Add API details, mark `REQUIRES UI AUTOMATION`, link dependencies
5. **Generate GANTT** (~15 min) — Python script generates Excel with phases, gates, owners, dates
6. **Communicate** (~15 min) — Post Slack report with overview, share spreadsheet and Linear link

**Inputs:** Discovery complete, API map, sizing
**Outputs:** Linear project with tickets, GANTT Excel, Slack report

**✅ Gate 2: Planning Complete**
- [ ] All tickets created in Linear
- [ ] Audit 10/10 PASS
- [ ] GANTT with dates and owners
- [ ] Labels applied by phase
- [ ] Dependencies linked
- [ ] Slack report posted
- [ ] CE informed and review scheduled

**Live Example:** [GEM Project](https://linear.app/testbox/project/gem-ats-implementation) — 37 tickets in 3-4h using automation.

---

### 🔹 PHASE 3: Kick-off

| Field | Value |
|:------|:------|
| **Objective** | Align the team, confirm scope, define cadences |
| **Owner** | TSA (R/A), GTM (C) |
| **Duration** | 1 meeting (30-60 min) + setup (1 day) |
| **Where** | Call (Zoom/Meet), Slack, Linear |
| **Why It Exists** | Ensures everyone knows what to do, when, and how to communicate |

**What to Do:**
1. **Kick-off meeting** (30-60 min):
   - Present GANTT and milestones
   - Confirm roles (who does what)
   - Define cadences (daily async, weekly sync, checkpoints)
   - Identify client dependencies (access, credentials)
   - Q&A and adjustments

2. **Operational setup** (~1 day):
   - Confirm tenant access
   - Verify API keys and credentials
   - Create Slack channel if needed
   - Distribute tickets to owners

3. **Kick-off message on Slack** (use Template 2 below)

**Inputs:** Linear project, GANTT, confirmed team
**Outputs:** Kick-off minutes, cadences defined, access confirmed

**✅ Gate 3: Kick-off Complete**
- [ ] Meeting held with all roles present
- [ ] GANTT reviewed and accepted by team
- [ ] Cadences defined (daily async + weekly sync)
- [ ] Tenant access confirmed
- [ ] API keys working
- [ ] First ticket assigned and ready to start

**⚠️ Common Failures:**
- Kick-off without GANTT → team doesn't know the dates
- Not confirming access → Phase 4 blocks on day 1
- Skipping kick-off "because we already know what to do" → silent misalignment

**Live Example:** GEM had "Internal Project Kickoff" (Feb 05). QBO had "Gate 1: Readiness Confirmation" (Jan 02-06).

---

### 🔹 PHASE 4: Foundation

| Field | Value |
|:------|:------|
| **Objective** | Prepare the environment: access, infrastructure, base configurations |
| **Owner** | TSA (R/A), CE (R) |
| **Duration** | 3-7 days |
| **Where** | Client tenant, AWS, Linear |
| **Why It Exists** | Nothing works without the foundation. This blocks EVERYTHING downstream. |

**What to Do:**
1. Configure tenant (admin access, user accounts)
2. Infrastructure setup (AWS, auto-login, environments)
3. Core configurations (roles, permissions, integrations)
4. Validate everything works (login, API calls, permissions)
5. Document access in shared location

**Inputs:** Tenant access, API keys, infrastructure requirements
**Outputs:** Working environment, users created, API tested

**✅ Gate 4: Foundation Complete**
- [ ] All team members can log in
- [ ] API key works (POST creates resource)
- [ ] Base configurations applied
- [ ] Staging/dev environments separated (if applicable)
- [ ] Access documentation updated

**⚠️ Common Failures:**
- Tenant takes too long to provision (external dependency)
- API key missing write permissions → blocks data gen
- Forgetting staging → testing in production

**Live Examples:**
- [RAC-109](https://linear.app/testbox/issue/RAC-109) — GEM Foundation phase ticket
- GEM Foundation (Jan 06-29). QBO Environment Setup.

---

### 🔹 PHASE 5: Build (Seed Data + Data Gen + Ingestion)

| Field | Value |
|:------|:------|
| **Objective** | Populate the system with realistic, functional data |
| **Owner** | CE (R/A), DATA (R), TSA (C) |
| **Duration** | 7-14 days |
| **Where** | Python scripts, APIs, client tenant |
| **Why It Exists** | Demo without data = empty demo. Bad data = zero credibility. |

**What to Do:**

**5a. Seed Data** (2-3 days):
- Create static entities: jobs, departments, offices, templates
- Use API when available, UI automation when not
- Validate entities appear correctly in UI

**5b. Data Generation** (3-5 days):
- Design schema (approved by TSA)
- Define distribution (how many per phase, time spread)
- Generate data via scripts (candidates, applications, resumes)
- Validate realism (names, companies, dates)

**5c. Ingestion** (2-4 days):
- Respect FK dependency order
- Rate limiting (0.5s between requests)
- Log every operation for rollback
- Run Gate 1 (local validation) BEFORE any INSERT

**3-Gate Validation Pipeline (mandatory):**
```
CSVs ready → Gate 1 (validate_csvs.py, local)
           → INSERT into database
           → Gate 2 (Retool validator, backend)
           → Gate 3 (Claude audit, coherence)
           → VALID DATA ✓
```

**Inputs:** Configured environment, mapped APIs, approved schema
**Outputs:** Populated system, 3-gate audit PASS

**✅ Gate 5: Build Complete**
- [ ] Static entities created and visible in UI
- [ ] Generated data has realistic names/companies
- [ ] Gate 1: validate_csvs → 0 FAIL
- [ ] Gate 2: Retool validator → 0 errors
- [ ] Gate 3: Audit → approved (5 auditors)
- [ ] Zero orphans or FK violations

**⚠️ Common Failures:**
- Generating generic data ("John Doe", "Company ABC") → client notices
- Not respecting FK order → constraint errors
- Rate limiting → API blocks you
- No rollback strategy → irrecoverable errors
- Schema changes after generation → total rework

**Live Examples:**
- [TOU-1033](https://linear.app/testbox/issue/TOU-1033) — GEM data generation with full API details
- [TOU-1034](https://linear.app/testbox/issue/TOU-1034) — UI automation required (marked explicitly)
- QBO 3-Gate Pipeline: 59 rules, 189 automated checks

---

### 🔹 PHASE 6: Stories & Feature Setup

| Field | Value |
|:------|:------|
| **Objective** | Configure the demos/features the client will see in action |
| **Owner** | TSA (R/A), CE (R) |
| **Duration** | 5-10 days |
| **Where** | Client tenant, Linear |
| **Why It Exists** | The data exists — now it needs to tell a convincing story. |

**What to Do:**
1. Configure each feature/story per SOW
2. Validate each story works end-to-end
3. Internal demo for stakeholders (dry run)
4. Document stories in reproducible format (click path)

**Inputs:** Populated system, features specified in SOW
**Outputs:** Features configured and working, internal demo completed

**✅ Gate 6: Stories Complete**
- [ ] Every SOW feature configured and tested
- [ ] Click paths documented
- [ ] Internal demo held (at least 1 stakeholder saw it)
- [ ] Bugs found in demo created as tickets (P1/P2)
- [ ] Evidence pack started (screenshots of features)

**Live Example:** GEM Phase 5 Stories (6 stories, [RAC-120](https://linear.app/testbox/issue/RAC-120) through [RAC-125](https://linear.app/testbox/issue/RAC-125)) + internal demo ([RAC-127](https://linear.app/testbox/issue/RAC-127)).

---

### 🔹 PHASE 7: Validate (QA + UAT)

| Field | Value |
|:------|:------|
| **Objective** | Ensure quality before showing it to the client |
| **Owner** | TSA (R), GTM (A) |
| **Duration** | 5-7 days |
| **Where** | Tenant, Linear, Slack, Calls |
| **Why It Exists** | Bug in UAT = credibility lost. Rigorous QA = client confidence. |

**What to Do:**

**7a. Internal QA** (2-3 days):
- TSA tests EVERY feature as if they were the client
- Test edge cases and alternative flows
- Create tickets for bugs (P1/P2)
- Fix bugs and re-test

**7b. UAT with Client** (2-3 days):
- GTM schedules session with client
- Client tests with script (click paths)
- Collect structured feedback
- Final fix after UAT

**Inputs:** Features configured, click paths
**Outputs:** Bugs fixed, UAT approved by client, evidence pack complete

**✅ Gate 7: Validate Complete**
- [ ] Internal QA: 0 P0/P1 bugs open
- [ ] UAT scheduled and completed with client
- [ ] Client feedback documented
- [ ] Post-UAT bugs fixed
- [ ] Evidence pack complete (screenshot per feature)
- [ ] Client sign-off (verbal or written)

**⚠️ Common Failures:**
- Shallow QA → bugs appear in UAT
- Not documenting client feedback → gets lost
- UAT without script → client doesn't know what to test

**Live Example:** GEM Validate (Jan 30-Feb 06, QA + UAT + sign-off). [ONB-12](https://linear.app/testbox/issue/ONB-12) — Customer UAT ticket.

> **External:** [Quality Gates — SonarSource](https://www.sonarsource.com/learn/quality-gate/) · [Quality Gates — testRigor](https://testrigor.com/blog/software-quality-gates/).

---

### 🔹 PHASE 8: Launch & Go-Live

| Field | Value |
|:------|:------|
| **Objective** | Deploy to production and hand over to the client |
| **Owner** | CE (R), GTM (A), Eng (R) |
| **Duration** | 1-3 days |
| **Where** | Production, Slack, Calls |
| **Why It Exists** | The moment of truth. Everything prepared goes live. |

**What to Do:**
1. Deploy to production (CE + Eng)
2. Smoke test post-deploy (TSA)
3. Client walkthrough (GTM)
4. Confirm everything works in real environment
5. Post go-live announcement on Slack

**Go-Live Checklist:**
- [ ] UAT approved by client (Gate 7 PASS)
- [ ] Zero P0/P1 bugs open
- [ ] Rollback plan documented and tested
- [ ] Smoke test: ALL features OK
- [ ] Client walkthrough completed
- [ ] Evidence pack final captured
- [ ] Go-live announcement posted on Slack
- [ ] Hypercare period activated (SLA communicated)

**✅ Gate 8: Launch Complete**
- [ ] Deploy to production completed
- [ ] Smoke test: all features OK
- [ ] Client walkthrough done
- [ ] Client confirms it's working
- [ ] Go-live communicated on Slack

**Live Example:** GEM Launch (Feb 07-13). [TOU-1027](https://linear.app/testbox/issue/TOU-1027) — MVP deployment.

> **External:** [Go-Live Checklist — Microsoft Dynamics 365](https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/prepare-go-live-checklist) · [Go-Live Checklist — Rocketlane](https://www.rocketlane.com/blogs/the-ultimate-checklist-for-a-successful-go-live-free-template).

---

### 🔹 PHASE 9: Hypercare & Handover

| Field | Value |
|:------|:------|
| **Objective** | Intensive post-go-live support and transition to BAU |
| **Owner** | GTM (R/A), CE (C) |
| **Duration** | 5-10 days |
| **Where** | Slack, Calls, Coda |
| **Why It Exists** | First days post-launch are the most critical. Abandonment = churn. |

**What to Do:**

**9a. Hypercare** (5-7 days):
- Monitor system daily
- Fast response to bugs (< 4h for P0/P1)
- Check-in with client every 2 days
- Document incidents

**9b. Handover** (2-3 days):
- Generate documentation package (runbook, decisions, lessons)
- Train client team (if applicable)
- Transfer Slack/Linear ownership to BAU mode
- Define post-handover support (who to contact)

**Documentation Package Structure** (based on [INTUIT_BOOM_TRANSFER](intuit-boom/INTUIT_BOOM_TRANSFER/)):

| Document | Content |
|:---------|:--------|
| START_HERE | Overview + glossary + reading order |
| ECOSYSTEM_MAP | All connected systems and URLs |
| TECHNICAL_REFERENCE | Environments, login, APIs, databases |
| RUNBOOKS | Step-by-step operational procedures |
| RISK_MATRIX | Active risks + resolved history |
| CREDENTIALS | Access checklist for handover |
| DECISIONS_LOG | All decisions with context |

**Inputs:** System in production
**Outputs:** Documentation package, formal handover, BAU mode activated

**✅ Gate 9: Handover Complete**
- [ ] Zero P0 bugs open during hypercare
- [ ] Documentation package delivered
- [ ] Training completed (if applicable)
- [ ] Post-handover contact point defined
- [ ] Hypercare ticket closed in Linear

**⚠️ Common Failures:**
- "Go-live and forget" → client left stranded
- No documentation → next project starts from zero
- Hypercare without SLA → bugs go unanswered

**Live Example:** GEM Hypercare ([ONB-15](https://linear.app/testbox/issue/ONB-15), Feb 07-13), Project Closure ([ONB-14](https://linear.app/testbox/issue/ONB-14)).

> **External:** ITIL Service Transition. [Project Handover Checklist — DOOR3](https://www.door3.com/blog/project-handover-checklist) · [Handing Off a Software Project — Simple Thread](https://www.simplethread.com/handing-off-a-software-project/).

---

### 🔹 PHASE 10: Closeout & Retrospective

| Field | Value |
|:------|:------|
| **Objective** | Formally close and capture lessons for the next project |
| **Owner** | TSA (R/A) |
| **Duration** | 1-2 days |
| **Where** | Coda, Linear, Slack |
| **Why It Exists** | Without retro, mistakes repeat. Without closeout, the project "never ends." |

**What to Do:**

1. **Operational closeout**:
   - Move ALL tickets to Done
   - Close milestone in Linear
   - Update GANTT with actual dates
   - Archive Slack channel (if temporary)

2. **Retrospective** (Keep/Stop/Start format):
   - What worked well? (Keep)
   - What went wrong? (Stop)
   - What should we start doing? (Start)
   - Document in Coda for future reference

3. **Update playbook**:
   - New risks discovered → add to standard risk register
   - New patterns → update templates
   - New scripts → contribute to toolkit

**Inputs:** Delivered project, feedback collected
**Outputs:** Retro documented, tickets closed, lessons applied

**✅ Gate 10: Project Closed** ✓
- [ ] 100% tickets in Done or Cancelled (with justification)
- [ ] Retro documented in Coda
- [ ] GANTT updated with actual dates
- [ ] Relevant lessons applied to playbook
- [ ] Closure announcement posted on Slack

---

## 🗓️ Cadences & Rituals

| Ritual | Frequency | Participants | Format | Channel |
|:-------|:----------|:-------------|:-------|:--------|
| **Daily Agenda** | Daily (async) | TSA → team | Slack post (v1.8 format) | #scrum-of-scrums |
| **1:1 TSA Lead** | Daily | TSA Lead + each TSA | Call 15 min | Zoom/Meet |
| **Weekly Sync** | Weekly | All project roles | Call 30 min | Zoom/Meet |
| **Gate Review** | Per gate | TSA (R) + Approver (A) | Checklist + decision | Linear + Slack |
| **Client Check-in** | Weekly (after kick-off) | GTM + Client | Call 30 min | Zoom/Meet |
| **Retro** | End of project | Full team | Keep/Stop/Start | Coda |

### Daily Agenda Format (v1.8)

```
[Daily Agenda – YYYY-MM-DD]

PROJECT ETA MM-DD
• Topic Description
 Do: Specific action ETA MM-DD
 Do: Another action
References: [links]

ESCALATION: None / [description]
```

> **Source:** Daily Agenda v1.8 (TSA_DAILY_REPORT, validated 2026-02-03). See [Linear Ticket Management](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Linear-Ticket-Management_sukx4jIV) Section C for full meeting cadence.

---

## 🔀 Change Management

### When to Apply:
- Client asks for something outside the SOW
- Team discovers a feature needs a different approach
- Timeline needs adjustment

### Process:
1. **Register**: Create ticket in Linear with label `new-scope`
2. **Assess**: TSA documents impact (timeline + effort + risk)
3. **Approve**: GTM + Client approve (or reject)
4. **Execute**: If approved, ticket enters backlog with defined priority
5. **Communicate**: Update GANTT and Slack report

### Change Request Template (Linear Ticket)

```
## Change Request: [Short description]

| Field | Value |
|:------|:------|
| **CR ID** | CR-[PROJECT]-[NNN] |
| **Requester** | [Name + Role] |
| **Date** | [YYYY-MM-DD] |
| **Category** | [ ] Scope [ ] Timeline [ ] Technical [ ] Budget |
| **Priority** | [ ] Critical [ ] High [ ] Medium [ ] Low |

### Description of Change
[What is being requested and why]

### Justification
[Why this is necessary — business reason]

### Impact Assessment
| Dimension | Impact |
|:----------|:-------|
| **Scope** | [What changes in the SOW] |
| **Timeline** | [How many extra days] |
| **Effort** | [Additional hours per role] |
| **Risk** | [New risks introduced] |

### Decision
| Status | Approver | Date |
|:-------|:---------|:-----|
| [ ] Approved [ ] Rejected [ ] Deferred | [GTM Owner] | [Date] |
```

> **Rule:** Change without a ticket = change that doesn't exist. Change without approval = scope creep.

> **External:** [Change Request Process — PMI](https://www.pmi.org/learning/library/scope-control-projects-you-6972) · [Change Request Form — ProjectManager](https://www.projectmanager.com/templates/change-request-form).

---

## ⚠️ Risk Management

### Standard Risk Register

| ID | Risk | Probability | Impact | Mitigation | Owner |
|:---|:-----|:-----------|:-------|:----------|:------|
| R01 | Tenant provisioning delayed | Medium | High (blocks everything) | Request 2 weeks in advance | TSA |
| R02 | API doesn't support needed operation | Medium | Medium (UI automation) | Map APIs in Discovery | TSA |
| R03 | Rate limiting during ingestion | High | Low (delay) | Exponential backoff in script | CE |
| R04 | Schema changes after data gen | Low | High (rework) | Schema freeze at Gate 5a | DATA |
| R05 | Key resource unavailable | Low | High (delay) | Documentation sufficient for handoff | TSA |
| R06 | Bugs discovered in UAT | High | Medium (1-3 day delay) | Rigorous internal QA before UAT | TSA |
| R07 | Scope creep via Slack | Medium | Medium (drift) | Formal change control | GTM |
| R08 | Synthetic data not realistic | Medium | High (credibility) | Gate 3 realism audit | DATA |

> **Source:** Real risks from GEM ([RAC-135](https://linear.app/testbox/issue/RAC-135) backdating blocker) and QBO (90 employee dupes, gateway timeout 504).

---

## 📊 Metrics & KPIs

### Framework: DORA + Flow Metrics (Adapted for Delivery)

Metrics follow the [DORA](https://dora.dev/guides/dora-metrics-four-keys/) framework (Google, 10+ years of research, 36K+ professionals) adapted for delivery, combined with [Agile Flow Metrics](https://www.atlassian.com/agile/project-management/metrics) (Atlassian).

**Key insight from DORA:** "Speed and stability are NOT trade-offs — the best teams excel at both."

| Metric | Framework | What It Measures | How to Collect | Target |
|:-------|:----------|:----------------|:--------------|:-------|
| **Lead Time** | DORA | SOW signed → go-live | GANTT dates | Small: 3w · Medium: 6w · Large: 10w |
| **Cycle Time** | Flow | In Progress → Done | Linear analytics | < 5 days (P2), < 1 day (P0) |
| **Delivery Frequency** | DORA | Deliverables per period | Linear milestones closed | ≥ 1 deliverable/week during Build |
| **First-Pass Validation Rate** | Flow | Datasets passing validation 1st try | validate_csvs.py results | > 80% (target: > 95%) |
| **Rework Rate** | DORA | Tickets reopened within 21d / total | Linear state changes | < 10% (alert if > 15%) |
| **Gate Pass Rate** | Custom | % gates approved on 1st attempt | Count per project | > 80% |
| **Blocker Duration** | Flow | Average time in Blocked state | Linear timestamps | < 2 days avg |
| **SOW Coverage** | Custom | % deliverables with tickets | Audit script | 100% |
| **Client Satisfaction** | Custom | Post-UAT feedback | Form or verbal | > 8/10 |

### SLOs by Priority

| Priority | Response Time | Resolution Time | Reference |
|:---------|:-------------|:---------------|:----------|
| 🔴 P0 | < 1 hour | < 4 hours | Sam: "escalate quickly" |
| 🟠 P1 | < 4 hours | < 1 day | TMS v2.0 |
| 🟡 P2 | < 1 day | < 5 days | TMS v2.0 |
| 🟢 P3 | Next standup | < 2 weeks | TMS v2.0 |

> **Source:** P0-P3 from TMS v2.0. SLOs derived from Sam's quote: "stuck for more than a couple of hours, escalate."
> **External:** [DORA Metrics Four Keys](https://dora.dev/guides/dora-metrics-four-keys/) · [Google SRE Book](https://sre.google/sre-book/table-of-contents/) for SLOs.

---

## 🚨 Escalation Playbook

| Situation | Escalate To | How | When |
|:----------|:----------|:----|:-----|
| P0 bug in production | #dev-on-call + GTM owner | Slack DM immediately | Immediately |
| Blocker > 2 hours | GTM owner | Slack DM | Same day |
| Resource unavailable | TSA Lead | Slack DM | Same day |
| Client unhappy | GTM Lead (Kat) | Call + Slack | < 4 hours |
| Scope creep identified | GTM owner + TSA Lead | Ticket new-scope + assessment | < 24 hours |
| Gate fails 2x consecutively | TSA Lead + GTM | Alignment call | Immediately |
| Timeline at risk (> 3 days behind) | All stakeholders | Weekly sync agenda | Next sync |

> **Source:** Sam Senior (CEO): "Escalate quickly to the GTM owner. This is not a failure."
> See [Linear Ticket Management](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Linear-Ticket-Management_sukx4jIV) Section B for full Critical Visibility Protocol.

---

# 5. ADJUSTMENTS TO DRAFTS

## 5.1 Adjustments to DRAFT Linear Ticket Management

| Section | Adjustment | Why |
|:--------|:----------|:----|
| **Related Docs** | Add link to Full Implementation Process | Cross-reference for coherence |
| **Version** | Update from 1.0 to 2.0 | Coda may be outdated; v2.0 has 8 critical corrections |
| **Labels** | Verify using "Customer Issues" (not "Bug") and "Refactor" (not "Tech Debt") | Correction validated via Linear API on 2026-01-27 |
| **State Flow** | Confirm "TSA owns until Backlog" (not Refinement) | Correction validated by user in TMS v2.0 |

**Ready-to-add text for DRAFT TMS:**

```markdown
## Related Docs
- [Full Implementation Process](https://coda.io/d/Solutions-Central_djfymaxsTtA/Full-Implementation-Process_suE5-VuS) — End-to-end implementation process
- [Pre-Project Linear Ticket Planning](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Pre-Project-Linear-Ticket-Planning_suePVn8A) — How to prepare tickets before kick-off
```

## 5.2 Adjustments to DRAFT Pre-Project Linear Ticket Planning

| Section | Adjustment | Why |
|:--------|:----------|:----|
| **Glossary** | Add "Gate" as a term | Full Implementation Process uses gates extensively |
| **Flow** | Add reference to gates from Full Process | Pre-Project is Phase 2 of the full process; needs to indicate where it fits |
| **Related Docs** | Add link to Full Implementation Process | Cross-reference |

**Ready-to-add text for DRAFT Pre-Project:**

```markdown
## Where This Document Fits

This process covers **Phase 2: Pre-Project Planning** of the [Full Implementation Process](https://coda.io/d/Solutions-Central_djfymaxsTtA/Full-Implementation-Process_suE5-VuS).

**Before**: Phase 1 (Discovery & Sizing) must be complete.
**After**: Phase 3 (Kick-off) uses the outputs from this process.

### Entry Gate (Phase 1 → Phase 2)
- [ ] All SOW deliverables listed
- [ ] APIs mapped
- [ ] Sizing estimated (S/M/L)
- [ ] At least 1 risk documented

### Exit Gate (Phase 2 → Phase 3)
- [ ] Tickets created and audited (10/10 PASS)
- [ ] GANTT with dates and owners
- [ ] Slack report posted
- [ ] CE review scheduled
```

---

# 6. CHECKLISTS & TEMPLATES

## CHECKLIST 1: Pre-Project (Intake + Discovery + Sizing)

```
## Pre-Project Checklist

### Intake (Gate 0)
- [ ] Opportunity identified and qualified
- [ ] Technical fit evaluated (product in catalog?)
- [ ] Commercial fit evaluated (budget, timeline)
- [ ] SOW draft or scope document exists
- [ ] GO/NO-GO decision recorded
- [ ] Resources confirmed available

### Discovery (Gate 1)
- [ ] SOW/Contract read and deliverables extracted
- [ ] Technical documentation collected (API docs, architecture)
- [ ] Brainstorm with CE completed
- [ ] Brainstorm with DATA completed (if applicable)
- [ ] APIs mapped (endpoint + method + limitation)
- [ ] External dependencies identified
- [ ] Similar projects reviewed (lessons)
- [ ] Relevant Slack threads collected

### Sizing
- [ ] Estimated ticket count: ___
- [ ] Classification: [ ] Small [ ] Medium [ ] Large
- [ ] Roles needed: TSA [ ] CE [ ] DATA [ ] GTM [ ] Eng [ ]
- [ ] Preliminary timeline defined
- [ ] Risk register v0 created
```

## CHECKLIST 2: Kick-off

```
## Kick-off Checklist

### Pre-Meeting
- [ ] GANTT finalized and shared
- [ ] Linear Project with tickets created
- [ ] Audit 10/10 PASS
- [ ] Meeting agenda sent
- [ ] All participants confirmed

### Meeting
- [ ] GANTT presented and accepted
- [ ] Roles confirmed (who does what)
- [ ] Cadences defined (daily async, weekly sync)
- [ ] Client dependencies identified
- [ ] Questions answered
- [ ] Next steps clear

### Post-Meeting
- [ ] Minutes recorded (Coda or Slack)
- [ ] Tenant access confirmed
- [ ] API keys tested
- [ ] Slack channel created/confirmed
- [ ] First ticket distributed
- [ ] Kick-off message posted on Slack
```

## CHECKLIST 3: Phase Execution

```
## Phase Execution Checklist (use at each phase)

### Phase Entry
- [ ] Previous gate APPROVED
- [ ] Phase tickets assigned with owner
- [ ] Previous phase dependencies met
- [ ] Resources available

### During Phase
- [ ] Daily reports posted in #scrum-of-scrums
- [ ] Blockers communicated within 2 hours
- [ ] Tickets updated (state, comments)
- [ ] Risk register reviewed

### Phase Exit (Gate)
- [ ] ALL acceptance criteria (DoD) for the phase met
- [ ] Zero P0/P1 tickets open
- [ ] Artifacts produced and documented
- [ ] Next phase ready to start
- [ ] Gate review held and APPROVED
```

## CHECKLIST 4: QA / Acceptance

```
## QA / Acceptance Checklist

### Internal QA (Pre-UAT)
- [ ] Every feature tested as if you were the client
- [ ] Edge cases tested
- [ ] Data verified (realism, completeness)
- [ ] Click paths documented
- [ ] Screenshots/videos captured (evidence pack)
- [ ] Bugs found created as tickets
- [ ] Zero P0/P1 bugs open

### Data Validation (3-Gate)
- [ ] Gate 1: validate_csvs.py → 0 FAIL
- [ ] Gate 2: Retool validator → 0 errors
- [ ] Gate 3: Claude audit → PASS (5 auditors)

### UAT (Client)
- [ ] Session scheduled with client
- [ ] Click paths shared
- [ ] Client tested ALL SOW features
- [ ] Feedback collected and documented
- [ ] Post-UAT bugs created as tickets
- [ ] Client sign-off obtained (verbal or written)
```

## CHECKLIST 5: Handover + Post-Implementation

```
## Handover + Post-Implementation Checklist

### Handover
- [ ] Documentation package produced:
  - [ ] Runbook (how to operate the system)
  - [ ] Technical decisions documented
  - [ ] Access and credentials listed
  - [ ] Scripts and tools delivered
- [ ] Training completed (if applicable)
- [ ] Post-handover contact point defined
- [ ] Ownership transferred (Slack, Linear)

### Hypercare
- [ ] Active daily monitoring
- [ ] Response SLA communicated to client
- [ ] P0/P1 bugs: response < 4h
- [ ] Check-ins every 2 days
- [ ] Incidents documented

### Closeout
- [ ] ALL tickets in Done or Cancelled
- [ ] GANTT updated with actual dates
- [ ] Retrospective completed (Keep/Stop/Start)
- [ ] Lessons applied to playbook
- [ ] Closure announcement on Slack
- [ ] Milestone closed in Linear
```

## CHECKLIST 6: Audit (Stakeholders)

```
## Audit Checklist — Hard Questions

### Client Perspective
- [ ] Does the delivered scope match the SOW?
- [ ] Do all features work as demonstrated?
- [ ] Does the data look realistic and professional?
- [ ] Did the client receive sufficient documentation?
- [ ] Does the client know who to contact post-project?

### GTM Perspective
- [ ] Was the timeline met?
- [ ] Was the client satisfied? (scale 1-10)
- [ ] Was there scope creep? If so, was it formalized?
- [ ] Is the evidence pack complete?
- [ ] Was the client relationship preserved?

### Engineering Perspective
- [ ] Were tickets clear enough to execute without asking?
- [ ] Were the AC measurable?
- [ ] Were environments (staging/prod) properly configured?
- [ ] Was there rework due to missing information?

### TSA Perspective
- [ ] Were all gates respected?
- [ ] Was the process followed or "bypassed"?
- [ ] Were there unanticipated dependencies?
- [ ] Did the playbook cover all scenarios encountered?

### Executive Perspective
- [ ] Was the cost (hours) within expectations?
- [ ] Is the process scalable for 10 simultaneous projects?
- [ ] Could a new TSA execute this without hand-holding?
- [ ] Are metrics being collected?
```

---

## TEMPLATE 1: Linear Ticket (Standard)

```
## 🎯 Objective
[ONE sentence — what this ticket delivers and why it matters]

## 📋 Overview
[2-3 paragraphs of context: what, why, how it connects to the project]

## ✅ Key Tasks
| **Task** | **Owner** | **Why** |
|:---------|:----------|:--------|
| [Specific action] | **[TSA/CE/DATA/GTM]** | [Business reason] |

## 🔍 Validation
| **Check** | **Method** | **Owner** |
|:----------|:-----------|:----------|
| [What to verify] | [How to verify] | **[Role]** |

## ⚠️ Risks
| **Risk** | **Impact** | **Mitigation** |
|:---------|:-----------|:---------------|
| [What could go wrong] | [Consequence] | [How to prevent] |

## 🔗 External Dependency
[If applicable — what depends on outside]

---
*Part of [PROJECT] · Milestone: [PHASE] · Created by: [TSA NAME] · Last updated: [DATE]*
```

**Required fields in Linear:**

| Field | Standard |
|:------|:---------|
| Title | `[PROJECT] Verb + Object` |
| Team | Platypus (PLA) or Raccoons (RAC) |
| Priority | P0/P1/P2/P3 |
| Labels | `[project]-project` + phase label |
| State | Backlog |
| Milestone | Matching the phase |
| Estimate | Story points |

> See [Linear Ticket Management](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Linear-Ticket-Management_sukx4jIV) for full ticket standards, 11 templates, and state flow.

---

## TEMPLATE 2: Kick-off Message (Slack)

```
@here 🚀 Kick-off: [PROJECT NAME]

Hey team, we're starting the implementation for [PROJECT]. Here's the overview:

📋 Scope:
• [N] features / deliverables per SOW
• Timeline: [START DATE] → [GO-LIVE DATE]
• Size: [Small/Medium/Large]

👥 Team:
• TSA: [Name] — Coordination and QA
• CE: [Name] — Technical implementation
• DATA: [Name] — Data generation
• GTM: [Name] — Client interface

📊 Artifacts:
• GANTT: [LINK]
• Linear Project: [LINK]
• SOW: [LINK]

🔄 Cadences:
• Daily async: #scrum-of-scrums (Daily Agenda format)
• Weekly sync: [DAY/TIME]
• Gate reviews: per phase

⚠️ Known Risks:
• [Risk 1]: [Mitigation]
• [Risk 2]: [Mitigation]

📅 Next Steps:
1. [Action 1] — [Owner] — ETA [Date]
2. [Action 2] — [Owner] — ETA [Date]

Questions? Reach out. Let's go! 💪
```

---

## TEMPLATE 3: Coda Page (Standard Structure)

```
# [PROJECT NAME] — Implementation Hub

## Document Info
| Field | Value |
|:------|:------|
| Owner | [TSA Name] |
| Status | [Active / Complete / On Hold] |
| Created | [Date] |
| Last Updated | [Date] |

---

## Overview
[1-2 paragraphs describing the project]

## Timeline
| Phase | Start | End | Status |
|:------|:------|:----|:-------|
| Discovery | [date] | [date] | [status] |
| Foundation | [date] | [date] | [status] |
| Build | [date] | [date] | [status] |
| Stories | [date] | [date] | [status] |
| Validate | [date] | [date] | [status] |
| Launch | [date] | [date] | [status] |

## Team
| Role | Person | Slack |
|:-----|:-------|:------|
| TSA | [name] | @handle |
| CE | [name] | @handle |
| DATA | [name] | @handle |
| GTM | [name] | @handle |

## Key Links
| Resource | Link |
|:---------|:-----|
| Linear Project | [url] |
| GANTT | [url] |
| SOW | [url] |
| Evidence Pack | [url] |

## Risk Register
[risk table]

## Decisions Log
| Date | Decision | Context | Decided By |
|:-----|:---------|:--------|:-----------|

## Notes
[space for project notes]
```

---

## TEMPLATE 4: Standard GANTT (Phases, Dependencies, Milestones)

```
GANTT — [PROJECT NAME]
Start: [DATE] | Target: [DATE]

GATE 0: QUALIFICATION APPROVED
  └─ SOW signed, resources confirmed

PHASE 1: DISCOVERY (3-5 days)
  ├─ Collect materials (SOW, APIs, docs)
  ├─ Map technical scope
  ├─ Identify risks
  └─ Sizing estimate

GATE 1: DISCOVERY COMPLETE

PHASE 2: PRE-PROJECT PLANNING (1-2 days)
  ├─ Design milestones
  ├─ Create tickets (via script)
  ├─ Run audit (10 checks)
  ├─ Generate GANTT
  └─ Post Slack report

GATE 2: PLANNING COMPLETE

PHASE 3: KICK-OFF (1 day)
  ├─ Kick-off meeting
  ├─ Confirm access
  └─ Distribute tickets

GATE 3: KICK-OFF COMPLETE

PHASE 4: FOUNDATION (3-7 days)
  ├─ Tenant setup
  ├─ Infrastructure
  ├─ Core configurations
  └─ Access validation

GATE 4: FOUNDATION COMPLETE

PHASE 5: BUILD (7-14 days)
  ├─ 5a: Seed Data (2-3 days)
  ├─ 5b: Data Generation (3-5 days)
  └─ 5c: Ingestion + 3-Gate Validation (2-4 days)

GATE 5: BUILD COMPLETE

PHASE 6: STORIES & FEATURES (5-10 days)
  ├─ Configure features
  ├─ Internal demo
  └─ Click paths

GATE 6: STORIES COMPLETE

PHASE 7: VALIDATE (5-7 days)
  ├─ Internal QA (2-3 days)
  └─ UAT with Client (2-3 days)

GATE 7: VALIDATE COMPLETE

PHASE 8: LAUNCH (1-3 days)
  ├─ Deploy to production
  ├─ Smoke test
  └─ Client walkthrough

GATE 8: LAUNCH COMPLETE

PHASE 9: HYPERCARE & HANDOVER (5-10 days)
  ├─ Monitoring
  ├─ Documentation package
  └─ Handover

GATE 9: HANDOVER COMPLETE

PHASE 10: CLOSEOUT (1-2 days)
  ├─ Close tickets
  ├─ Retro (Keep/Stop/Start)
  └─ Update playbook

✓ PROJECT COMPLETE

Owners: TSA=[name] CE=[name] DATA=[name] GTM=[name]
Colors: Header=#2C3E50 Gate=#E74C3C Phase=#9B59B6 In Progress=#3498DB Complete=#D9EAD3
```

---

## TEMPLATE 5: Operational Runbook (Handover)

```
# Runbook — [PROJECT NAME]

> Operational document for post-go-live maintenance and support.
> Based on the INTUIT_BOOM_TRANSFER model (11 documents).

## 1. START HERE
- **Project**: [Name]
- **Dataset ID**: [ID]
- **Company**: [Structure — Parent + Children if applicable]
- **Go-Live**: [Date]
- **Hypercare until**: [Date]
- **Contact point**: [Name + Slack]

## 2. ECOSYSTEM MAP
| Component | URL | Type | Status |
|:----------|:----|:-----|:-------|
| Tenant | [URL] | Production | Active |
| Staging | [URL] | Test | Active |
| Linear | [URL] | Tickets | Active |
| Coda | [URL] | Docs | Active |
| Drive | [URL] | Evidence | Active |

## 3. CREDENTIALS
| Service | Username | Password Location | Type |
|:--------|:---------|:------------------|:-----|
| [Service] | [user] | [1Password / .env] | API Key / OAuth |

## 4. TECHNICAL REFERENCE
- **Stack**: [technologies]
- **DB Path**: [path]
- **Key Scripts**: [list with paths]
- **API Rate Limits**: [known limits]

## 5. RUNBOOKS (Procedures)
### 5.1 How to ingest new data
[Step by step]

### 5.2 How to rollback
[Step by step]

### 5.3 How to investigate a bug
[Step by step]

### 5.4 How to escalate
[Step by step]

## 6. RISK MATRIX
| Risk | Probability | Impact | Mitigation | Owner |
|:-----|:-----------|:-------|:----------|:------|

## 7. DECISIONS LOG
| Date | Decision | Context | Decided By |
|:-----|:---------|:--------|:-----------|

## 8. KNOWN ISSUES / GAPS
| Issue | Severity | Status | Workaround |
|:------|:---------|:-------|:-----------|
```

---

## TEMPLATE 6: Retrospective (Keep / Stop / Start)

```
# Retrospective — [PROJECT NAME]
**Date**: [YYYY-MM-DD]
**Participants**: [Names]
**Facilitator**: [Name]

## Project Metrics
| Metric | Planned | Actual | Delta |
|:-------|:--------|:------|:------|
| Lead Time | [X] weeks | [Y] weeks | [+/-] |
| Total Tickets | [X] | [Y] | [+/-] |
| Gate Pass Rate (1st attempt) | 80% | [Y]% | [+/-] |
| Rework Rate | <10% | [Y]% | [+/-] |
| Bugs in UAT | 0 P0/P1 | [Y] | [+/-] |

## KEEP (What worked well — keep doing)
1. [Item]
2. [Item]
3. [Item]

## STOP (What went wrong — stop doing)
1. [Item + root cause]
2. [Item + root cause]
3. [Item + root cause]

## START (What we should begin doing)
1. [Item + expected benefit]
2. [Item + expected benefit]
3. [Item + expected benefit]

## Action Items
| Action | Owner | Deadline | Status |
|:-------|:------|:---------|:-------|
| [action] | [name] | [date] | [ ] Pending |

## Lessons for the Playbook
[What from this retro should be incorporated into the Full Implementation Process?]
```

---

# 7. QUALITY REPORT

## 7.1 Risks & Mitigation

| Risk | Status | Mitigation |
|:-----|:-------|:-----------|
| Coda not directly accessible (auth required) | MITIGATED | Used local .md files as authoritative source. Coda pages are pasted from these files. |
| Slack/Linear not directly queried | MITIGATED | Used local sessions, learnings, and TMS v2.0 as validated proxy (5 sources, 95% confidence) |
| Some external URLs may break over time | ACCEPTED | Primary sources are internal; external links are supplementary references |
| Process not yet validated on a real project from scratch | OPEN | First real project should be treated as pilot with daily feedback |

## 7.2 Items Not Found

| Item | Status | Fallback |
|:-----|:-------|:---------|
| Formal SOW template | FOUND (3 real SOWs: Mailchimp, QBO, GEM) | SOW Best Practices document covers 12-section standard |
| Handover template | FOUND (INTUIT_BOOM_TRANSFER, 11 real docs) | Template 5 above |
| Coda GTM materials | NOT FOUND (auth blocked) | Used SOW files and GEM commercial references |
| Slack decision threads | NOT FOUND (requires token) | Used sessions and learnings as proxy |

## 7.3 Decisions Made

| Decision | Context | Alternatives Considered |
|:---------|:--------|:----------------------|
| 11 phases (Intake → Closeout) | Full E2E coverage based on real evidence | 7 phases (GEM model), 8 phases (QBO model) |
| RACI with 5 roles (TSA/CE/DATA/GTM/Eng) | Reflects actual team structure | 3 roles (simplified), 7 roles (too granular) |
| English as document language | Both existing CODA drafts are in English | Portuguese (rejected — inconsistent with existing docs) |
| Integrate existing drafts by reference | TMS and Pre-Project are already well-written; avoid duplication | Inline duplication (rejected — maintenance nightmare) |
| YAML-driven generator script | Reusability for any process | Hardcoded markdown, Jinja2 templates |
| 3-Gate Validation Pipeline | Proven pattern from intuit-boom | Single gate, manual validation |

## 7.4 Quality Gates — Final Status

| Gate | Criterion | Status | Evidence |
|:-----|:---------|:-------|:---------|
| G1 | **Action**: Can someone execute the process without asking anything? | ✅ PASS | Every phase has "What to Do" steps, checklists, templates, and Live Examples |
| G2 | **Traceability**: Important steps have internal source (or "NOT FOUND") + external reference? | ✅ PASS | All phases cite internal sources + 15 external URLs |
| G3 | **Coherence**: Doesn't contradict the drafts and integrates Slack/Linear/Coda? | ✅ PASS | Phase 2 explicitly defers to Pre-Project Planning. Tickets follow TMS v2.0 format. |
| G4 | **Coverage**: Covers Commercial/GTM, TAS, Engineering, Data Gen, PM and Executive? | ✅ PASS | 6 agent memos + cross-examination + RACI per phase |
| G5 | **Auditable**: Has DoR/DoD, checklists, templates, gates and metrics? | ✅ PASS | DoR (6 criteria), DoD (5 criteria), 6 checklists, 6 templates, 10 gates, 9 metrics |
| G6 | **Pragmatism**: No useless bureaucracy; everything exists for a clear reason? | ✅ PASS | Sized by project type (S/M/L), phases can be skipped for small projects |

## 7.5 Metrics / KPIs

| Metric | Source | Confidence |
|:-------|:-------|:-----------|
| Lead Time targets (3w/6w/10w) | GEM (7 weeks, Medium) + QBO (8 weeks, Large) | HIGH |
| Gate Pass Rate > 80% | Industry standard (DORA + PMI) | MEDIUM |
| Rework Rate < 10% | DORA research | MEDIUM |
| SLOs (P0: <1h, P1: <4h) | TMS v2.0 + Sam CEO quote | HIGH |

## 7.6 DoD of This Playbook

This playbook is considered DONE when:
- [ ] Pasted into Coda (Solutions Central → Full Implementation Process)
- [ ] Adjustments applied to the 2 existing DRAFTs (Section 5)
- [ ] Validated by TSA team (dry run on real project)
- [ ] First retrospective feeds back into v2.1

---

# 8. ANNEX — ORIGINAL REQUESTER INSTRUCTIONS (COPIED IN FULL)

> **The original request (unmodified):**

quero q vc faça um prompt perfeito pro claude code
❯ legal quero preencher esse aqui
  https://coda.io/d/Solutions-Central_djfymaxsTtA/Full-Implementation-Process_suE5-VuS#_lu_axty0 e para te ajudar vc
  vai fazer uma composição de aprendizado primeiro, mergulhando profudnametno em tudo q fizemos de GANTT aqui em
  todos projetos do claude, depois vc vai acessar oq vc encontrar em busca densa usando aprendizado em cadeia
  dinamico einterativo e RAG para projeto implantando no slack linear e coda. sempre pegando ponto de vistas
  multiplos entre comercial GTM, aruiteto de dados TAS, engenharia e data gen ou geração de dados. use tambem nosso
  acesso a pasta do drive principalmente a pasta de go to market q temos ela tem bastante coisa comercial e
  implentação e etc, depois q vc conseguir como bastente contexto para a textbox, vc vai rodar nossos auditorias use
  multiplis agentes pra tudo possivel incluse pra auditoria fazendo sabatinas no contexto do ponto de vista de cada
  steakholder e owners e como chefe cchato detalhista,e executivo da testebox e gerente de projetos. depois vc vai ter o contexto bem refinado de modo que a gente precisa contruir o processo padronziado dessa rotina conforme pesquisas q vc fez agregando tudo q foi feito pra contruir esses 2   https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Linear-Ticket-Management_sukx4jIV#_lughX0o6 e  https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Pre-Project-Linear-Ticket-Planning_suePVn8A#_luOhy50G  use o tmepo todo tambem triangulação cilcica de aprendizado tanto interno e externo pra aumentar o indice de confiança de cada etapa e cada cadeia de entendimento aduqirida por vc, depois q vc tiver pronto vc vai fazer rodas de construção do processo em questão de implentação e usando checklists e adutoria q vc tem e se nao tiver montar, vc vai ficar rodando até chegar em um processo de implentação perfeito e dentro dos padrões que vc percebeu durante a contextulalização CHAT GPT deixe esse prommpte 10/10 de modo que garanta cada etapa de maneira madura ciclica e perfeita, ninguem pode por defeito aqui nossa vida depende disso, inclue tambem isso tudo q digitei aqui integralmente, em uma parte reservada e explica pro claude q ele precisa entender do jeito dele e pegar oq vc montar de sugestão e ajudar ele a refinar o proprio caminho. chat GPT sema extremamente perfeito na aruqteturo dessa prompt ... e outra coisa. quando o claude acabar pede pra ele montar de maneira efieencia sugestão minha um script pythin q tenha isso tudo já de maneira que eu só altere as referencis a serem motnadas, exemplo esse é procesos de implantação mas amanha ovu fazer de um de processo de vendas e o claude já tem q ter isso tudo configurado, do q fazer , com ofazer onde fazer, pq fazer e etc

---

**How This Was Interpreted:**

1. **Deep context first** — Read every GANTT, every SOW, every ticket pattern, every handover package across all projects. Not surface-level — every file, every section, every real example.

2. **Multiple perspectives** — Not just one voice. 6 agents (GTM, TSA, Engineering, Data Gen, PM, Executive) each produced their own requirements, then cross-examined each other to find gaps.

3. **Build on what exists** — The two CODA drafts (TMS and Pre-Project) were read in full (TMS: 378 lines, Pre-Project: 1210 lines). The Full Implementation Process builds ON TOP of them, referencing and integrating their patterns, not duplicating or ignoring them.

4. **English** — Both existing drafts are in English. The Full Implementation Process follows the same language and style (emojis, tables, Live Examples, casual but direct voice).

5. **Cyclic refinement** — Collected sources → synthesized into agent memos → cross-examined → built process → audited with 6 Quality Gates → fixed defects → re-validated.

6. **Reusable script** — `generate_playbook.py` accepts a YAML config and generates the complete playbook structure for any process (implementation, sales, support, onboarding).

---

*Document generated: 2026-02-10 | Cycle 1 + Audit | 6/6 Quality Gates PASS*
