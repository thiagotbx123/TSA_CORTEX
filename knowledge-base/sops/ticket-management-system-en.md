# Ticket Management System
## TSA TestBox - How We Get Things Done

```
 _____ _      _        _     __  __                                            _
|_   _(_) ___| | _____| |_  |  \/  | __ _ _ __   __ _  __ _  ___ _ __ ___   ___ _ __ | |_
  | | | |/ __| |/ / _ \ __| | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '_ ` _ \ / _ \ '_ \| __|
  | | | | (__|   <  __/ |_  | |  | | (_| | | | | (_| | (_| |  __/ | | | | |  __/ | | | |_
  |_| |_|\___|_|\_\___|\__| |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_| |_| |_|\___|_| |_|\__|
                                                     |___/
```

> **Version:** 1.0 Draft
> **Date:** 2026-01-26
> **Author:** Thiago Rodrigues
> **Scope:** TSA/Platypus Team
> **Tool:** [Linear](https://linear.app/testbox/team/PLA)

---

## Why does this document exist?

Because "I'll document it later" never works. And when a ticket gets lost, everyone suffers - the customer, the dev, and you who has to explain what happened.

This system exists so **anyone** can look at a ticket and understand:
- What needs to be done
- Why it matters
- Who owns it
- When it will be ready (or at least an honest guess)

---

## Index

- [A. The Flow (End-to-End)](#a-the-flow-end-to-end)
- [B. Who Does What](#b-who-does-what)
- [C. Linear Standard](#c-linear-standard)
- [D. CODA (Our Wiki)](#d-coda-our-wiki)
- [E. Templates](#e-templates)
- [F. Quality Gates](#f-quality-gates)
- [G. Metrics](#g-metrics)
- [Resources & Contacts](#resources--contacts)

---

## A. The Flow (End-to-End)

### Ticket Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                      │
│   "Hey,                                                                             │
│    something      INTAKE ──▶ TRIAGE ──▶ DUE DILIGENCE ──▶ TICKET ──▶ EXECUTION      │
│    broke!"            │                                                    │         │
│        │              │                                                    ▼         │
│        │              │                                              MONITORING      │
│        │              │                                                    │         │
│        │              │                                                    ▼         │
│   "Thanks,       RETRO ◀── CLOSEOUT ◀── DELIVERY ◀── VALIDATION ◀────────┘         │
│    looks great!"                                                                     │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

**TL;DR:** Someone asks → we understand → we build → we deliver → we learn.

---

### 1. INTAKE - "Houston, We Have a Problem"

**What it is:** The moment someone asks for help.

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│   [Customer]  [Internal]  [Sentry]  [Slack Thread]    │
│       │           │          │           │            │
│       └───────────┴──────────┴───────────┘            │
│                       │                               │
│                       ▼                               │
│            ┌──────────────────┐                       │
│            │  REGISTER        │                       │
│            │  - Who?          │                       │
│            │  - What?         │                       │
│            │  - Urgent?       │                       │
│            └────────┬─────────┘                       │
│                     │                                 │
│                     ▼                                 │
│            [ASSIGN TSA OWNER]                         │
│                     │                                 │
│                     ▼                                 │
│               [→ TRIAGE]                              │
│                                                       │
└────────────────────────────────────────────────────────┘
```

**Where requests come from:**

| Source | Channel | Who Picks Up |
|--------|---------|--------------|
| Customer request | #customer-requests | TSA owner of the customer |
| Internal team | #tsa-internal | First TSA who sees it |
| Sentry alert | Alerts / #tsa-bugs | On-call TSA |
| Escalation | #escalations | TSA Lead |

**TSA Responsibility:** The TSA must actively monitor ticket creation, follow up on progress, and keep stakeholders engaged. Ownership means staying on top of it from start to finish.

---

### 2. TRIAGE - "How Big Is the Fire?"

**What it is:** Decide if it's a real fire or just smoke.

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│            ┌──────────────────┐                        │
│            │   EVALUATE:      │                        │
│            │   Impact +       │                        │
│            │   Urgency        │                        │
│            └────────┬─────────┘                        │
│                     │                                  │
│         ┌──────────┬┴──────────┐                       │
│         ▼          ▼           ▼                       │
│       [P0]       [P1]        [P2/P3]                  │
│    "DROP ALL"  "Today"     "Sprint"                   │
│         │          │           │                       │
│         └──────────┴───────────┘                       │
│                     │                                  │
│                     ▼                                  │
│            [Need investigation?]                       │
│              Yes → Due Diligence                       │
│              No  → Ticket directly                     │
│                                                        │
└────────────────────────────────────────────────────────┘
```

**Priority System - No BS:**

| Priority | Translation | When to Use | Real Example |
|:--------:|-------------|-------------|--------------|
| **P0** | "Drop everything" | Production down, enterprise customer blocked | System down, data corrupted |
| **P1** | "Needs to ship today" | Critical functionality failing | Login broken, ingestion stopped |
| **P2** | "This week" | Real problem, but has workaround | Bug affecting some users |
| **P3** | "In the sprint" | Improvement or new feature | Tech debt, optimizations |

**Decision Matrix (for table lovers):**

| | Critical Urgency | High Urgency | Normal Urgency |
|---|:---:|:---:|:---:|
| **Critical Impact** | P0 | P1 | P1 |
| **High Impact** | P1 | P1 | P2 |
| **Medium Impact** | P1 | P2 | P3 |
| **Low Impact** | P2 | P3 | P3 |

---

### 3. DUE DILIGENCE - "Let's Understand Before We Code"

**What it is:** Investigate the problem properly before creating a ticket. No guessing.

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│   ┌──────────────┐    ┌──────────────┐                │
│   │  REPRODUCE   │───▶│  MAP SCOPE   │                │
│   │  the issue   │    │  - Who's hit │                │
│   └──────────────┘    │  - Since when│                │
│          │            │  - Related?  │                │
│          ▼            └──────┬───────┘                │
│   [Can't reproduce]          │                        │
│        │                     ▼                        │
│        ▼            ┌──────────────┐                  │
│   [Ask for more    │  COLLECT     │                  │
│    context]        │  EVIDENCE    │                  │
│                    │  - Logs      │                  │
│                    │  - Sentry    │                  │
│                    │  - Screenshot│                  │
│                    └──────┬───────┘                  │
│                           │                          │
│                           ▼                          │
│                   [HYPOTHESIS/SOLUTION]              │
│                           │                          │
│                           ▼                          │
│                     [→ TICKET]                       │
│                                                      │
└────────────────────────────────────────────────────────┘
```

**When to do it:**
- P0 and P1: **Always** (mandatory)
- P2: If cause is not obvious
- P3: Only if it's mysterious

**Quick Checklist:**
- [ ] Can I reproduce it?
- [ ] Do I know who/how many are affected?
- [ ] Was there a similar ticket? (search Linear)
- [ ] Does it involve other teams?
- [ ] Do I have a solution hypothesis?
- [ ] Did I collect evidence?

---

### 4. TICKET CREATION - "Now Let's Create It"

**What it is:** Create a ticket anyone can understand.

**Standard Format:**

```markdown
## Overview
[WHAT is happening + WHY it matters]
[Link to thread/CODA if available]

## Requirements
* [What needs to be done - be specific]
* [Another requirement]

## Acceptance Criteria
* [How we know it's done - measurable]
* [Another criterion]

## References
- [Relevant links]
```

**Title:**
```
[CUSTOMER] Verb + Object

Good examples:
[QuickBooks] Fix failing login task
[Gong] Refactor Engage email templates
[SPIKE] Investigate landing page issues
[CORTEX] Document worklog process
```

**Required Fields in Linear:**

| Field | What to put |
|-------|-------------|
| Title | `[Customer] Description` |
| Team | Platypus (PLA) |
| Priority | P0/P1/P2/P3 |
| Labels | Sprint (`2026.02`) + Type (`Bug`) |
| State | Backlog |

---

### 5. EXECUTION - "Let's Build"

**Linear State Flow:**

```
[Backlog] ──▶ [Refinement] ──▶ [Refined] ──▶ [Todo]
                                              │
                                              ▼
                                        [In Progress]
                                         /    │    \
                                        /     │     \
                                       ▼      ▼      ▼
                                [Blocked] [Paused]  [PR]
                                        \     │     /
                                         \    │    /
                                          ▼   ▼   ▼
                                       [Needs Review]
                                             │
                                             ▼
                                     [Ready for Deploy]
                                             │
                                             ▼
                                      [Production QA]
                                             │
                                             ▼
                                          [Done] 🎉
```

**Rules:**
- Don't skip states without justification
- Blocked = must explain WHY
- Paused = only with Lead's OK

---

### 6. MONITORING - "Don't Let It Die in Limbo"

**What it is:** Keep an eye to make sure the ticket is moving.

**Cadence by priority:**

| Priority | How often to check | Why |
|:--------:|-------------------|-----|
| **P0** | Constantly | It's an emergency, dropped everything |
| **P1** | Multiple times a day | Urgent, needs to ship |
| **P2** | Daily | Important but controlled |
| **P3** | Standup/Review | Normal pace |

**When a ticket stalls:**

1. **Find the reason** - Blocker? Question? Overload?
2. **Unblock it** - Answer question, ping dependency, renegotiate
3. **Escalate if needed** - Can't solve? Call the Lead
4. **Document** - Record what happened in the ticket

*Stalled ticket = customer waiting = problem.*

---

### 7-9. VALIDATION → DELIVERY → CLOSEOUT

**Validation:** Make sure it meets acceptance criteria before going to prod.

**Delivery:** Deploy and monitor stability.

**Closeout:**
- Move to Done
- Add final comment explaining what was done
- Notify stakeholders
- Update CODA if needed

---

### 10. RETRO - "What Did We Learn?"

**When to do it:**
- Every P0 (mandatory)
- P1 that took longer than expected
- Anything that was chaotic

**Simple Template:**

```markdown
## Ticket: PLA-XXXX - [Title]

### Timeline
- Intake: DD/MM
- Resolution: DD/MM
- Total: X days

### What worked
- [good thing 1]

### What to improve
- [thing to improve 1]

### Actions
- [ ] [Action] - @owner - deadline
```

---

## B. Who Does What

### RACI (Who Owns What)

| Stage | Requestor | TSA | Eng | QA |
|-------|:---------:|:---:|:---:|:--:|
| Intake | **R** | A | I | - |
| Triage | C | **R/A** | I | - |
| Due Diligence | I | **R/A** | C | - |
| Ticket | I | **R/A** | C | - |
| Execution | - | I | **R/A** | I |
| Monitoring | I | **R** | A | I |
| Validation | - | C | I | **R/A** |
| Closeout | I | **R/A** | I | I |

**R** = Does it | **A** = Accountable | **C** = Consulted | **I** = Informed

---

### TSA by Customer

| Customer | TSA Owner | Backup |
|----------|-----------|--------|
| QuickBooks | Thiago Rodrigues | Diego |
| Gong | Carlos | Thiago Rodrigues |
| Apollo | Carlos | Diego |
| Brevo | Diego | Carlos |
| CallRail | Diego | Carlos |
| People.ai | Diego | Gabrielle |
| Dixa | Gabrielle | Alexandra |
| Zendesk | Gabrielle | Alexandra |
| Mailchimp | Gabrielle | Diego |
| mParticle | Alexandra | Gabrielle |
| Syncari | Alexandra | Gabrielle |

---

## C. Linear Standard

### Priorities

| | Name | Translation |
|:-:|------|-------------|
| **P0** | Emergency | System on fire |
| **P1** | Urgent | Needs to ship today |
| **P2** | High | This week |
| **P3** | Normal | In the sprint |

### Labels

| Label | When to Use |
|-------|-------------|
| `Bug` | Something broke |
| `Feature` | New thing |
| `Spike` | Investigation |
| `RCA` | Post-incident analysis |
| `Internal Request` | Internal request |
| `Customer Request` | Customer request |
| `Technical Debt` | Refactoring |
| `Worklog` | Documentation/Process |

### Definition of Ready (DoR)

Ticket ready for sprint when:
- [ ] Standard title
- [ ] Overview explains the problem
- [ ] Clear requirements
- [ ] Measurable acceptance criteria
- [ ] Priority defined
- [ ] Labels applied

### Definition of Done (DoD)

Ticket closed when:
- [ ] Acceptance Criteria OK
- [ ] In production (if applicable)
- [ ] Tests passing
- [ ] Stakeholders notified
- [ ] Final comment on ticket

---

## D. CODA (Our Wiki)

### Where Things Are

| Process | Location | When to Use |
|---------|----------|-------------|
| Post-Launch Request | Solutions Central | New customer requests |
| Blockers | Customer page | Document blockers |
| Playbooks | Per customer | Setup/Ingestion |

### Customer Structure

```
[Customer]/
├── Customer Overview    ← General status
├── Maintained Accounts  ← Active accounts
├── Instance Creation    ← How to setup
├── Dataset              ← Data
├── Running Automations  ← What's running
└── Feature by Feature   ← Status per feature
```

---

## E. Templates

### Quick Matrix

| # | Template | Use | Main Fields |
|:-:|----------|-----|-------------|
| 1 | Bug | Something broke | Problem, Impact, Evidence |
| 2 | Feature | New thing | Objective, Requirements, Out of Scope |
| 3 | Spike | Investigation | Question, Timebox |
| 4 | RCA | Post-incident | Timeline, Root Cause |
| 5 | Internal | Internal request | Requester, Justification |
| 6 | Customer | Customer request | Customer, Urgency |
| 7 | Tech Debt | Refactoring | Current/Desired State |
| 8 | Deploy | Releases | Changes, Rollback |
| 9 | Onboarding | Customer setup | Pre-req, Steps |
| 10 | Worklog | Documentation | Context, Artifacts, Learnings |

*(Full templates in reference files)*

---

### Template 1: Bug Report

```markdown
## Overview
**Problem:** [What's broken]
**Impact:** [Who's suffering]
**Frequency:** [Always/Sometimes/Once]
**Evidence:** [Link to Sentry/log/screenshot]

## Requirements
* Identify root cause
* Fix it
* Tests to prevent regression

## Acceptance Criteria
* Can't reproduce anymore
* Tests passing
* Evidence in prod

## References
- Sentry: [link]
```

---

### Template 10: Worklog/CORTEX

```markdown
## Overview
**Type:** [Documentation/Automation/Process]
**Context:** [Why we're doing this]
**System:** CORTEX

## Objective
[What we want to achieve]

## Scope
* [What's included]
* **Out of scope:** [What's NOT]

## Artifacts
| What | Where | Status |
|------|-------|--------|
| [item] | [path] | [Draft/Final] |

## Learnings
* [What we discovered]

## Next Steps
- [ ] [Action]

## Acceptance Criteria
* Functional
* Reviewed
* Committed
```

---

## F. Quality Gates

### Quick Summary

| Gate | Transition | What's needed | Who approves |
|:----:|------------|---------------|--------------|
| 1 | Intake → Triage | Context, TSA owner | TSA |
| 2 | Triage → DD/Ticket | Priority | TSA |
| 3 | DD → Ticket | Problem understood | TSA |
| 4 | Ticket → Refinement | DoR OK | TSA + Eng |
| 5 | Refinement → Refined | Estimate | Eng Lead |
| 6 | Exec → Review | Code + tests | Dev |
| 7 | Review → Deploy | PR approved | Reviewer |
| 8 | Deploy → QA | Smoke tests | DevOps |
| 9 | QA → Done | DoD OK | QA/TSA |
| 10 | Done → Retro | Learnings | TSA Lead |

---

## G. Metrics

### What We Measure

| Type | Metric | Target |
|------|--------|--------|
| **Volume** | Created/week | Baseline |
| | Closed/week | >= created |
| | Backlog size | Stable |
| **Quality** | DoR compliance | > 95% |
| | DoD compliance | > 95% |
| | Reopen rate | < 5% |
| **Speed** | Lead time P0/P1 | Minimize |
| | SLA compliance | > 90% |

### When We Review

| Ceremony | Frequency | Who | Focus |
|----------|-----------|-----|-------|
| Standup | Daily | TSA | Blockers |
| Sprint Review | 2 weeks | TSA + Eng | Deliveries |
| Metrics Review | Monthly | TSA Lead | KPIs |
| Process Retro | Quarterly | Everyone | Improvement |

---

## Resources & Contacts

```
╔═══════════════════════════════════════════════════════════════════════╗
║                         WHERE TO FIND THINGS                          ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  LINEAR           https://linear.app/testbox/team/PLA                ║
║                   Where tickets live                                  ║
║                                                                       ║
║  CODA             https://coda.io/d/_djfymaxsTtA                     ║
║                   Customer documentation                              ║
║                                                                       ║
║  SLACK            #tsa-internal      → TSA Team                      ║
║                   #customer-requests → Requests                       ║
║                   #tsa-bugs          → Bugs                          ║
║                   #escalations       → Urgencies                      ║
║                                                                       ║
║  GITHUB           TestBoxLab/integrations                            ║
║                   Integration code                                    ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════╗
║                           WHO TO CALL                                 ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  THIAGO RODRIGUES                                                    ║
║  TSA Lead | @thiago                                                  ║
║  Standardization, Metrics, Process                                   ║
║                                                                       ║
║  ─────────────────────────────────────────────────────────────────   ║
║                                                                       ║
║  LUCAS WAKIGAWA                                                      ║
║  Solutions Manager | @waki                                           ║
║  Strategy, Escalations, Executive Alignment                          ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

### History

| Version | Date | Author | What changed |
|---------|------|--------|--------------|
| 1.0 | 2026-01-26 | Thiago Rodrigues | Initial version - "No more chaos" |

---

*"A good process is one nobody notices, because it just works."*

**End of Document** 🚀

