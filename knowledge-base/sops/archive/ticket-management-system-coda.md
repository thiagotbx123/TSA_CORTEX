# 🎫 Ticket Management System
## TSA TestBox - How We Get Things Done

**Version:** 1.0 | **Date:** 2026-01-26 | **Author:** Thiago Rodrigues | **Tool:** [Linear](https://linear.app/testbox/team/PLA)

---

## 📋 Why does this document exist?

Because "I'll document it later" never works. And when a ticket gets lost, everyone suffers - the customer, the GTM team, the dev, and you who has to explain what happened.

This system exists so **anyone** can look at a ticket and understand:
- What needs to be done
- Why it matters
- Who owns it
- When it will be ready

---

# 🔄 A. The Flow (End-to-End)

**Summary:** Request comes in → TSA investigates → Ticket is created → Engineering builds → We deliver → We learn.

---

## 1️⃣ INTAKE - "Houston, We Have a Problem"

The moment a request lands on our radar.

### 📥 Request Sources

| 🏷️ Source | 📍 Channel | 👤 First Responder |
|-----------|------------|-------------------|
| 🤝 Customer request | #customer-requests | TSA assigned to customer |
| 🏠 Internal team | #tsa-internal | Available TSA |
| 🚨 Sentry alert | Alerts / #tsa-bugs | On-call TSA |
| ⚡ Escalation | #escalations | TSA Lead |

### 🎯 The TSA Role

The TSA acts as a **bridge between GTM/Customers and Engineering** - part Solutions Architect, part Project Manager:

- **Investigate** - Dig into the problem, gather context, understand impact
- **Qualify** - Determine if it's a real issue, a feature request, or a misunderstanding
- **Coordinate** - Connect the right people, manage expectations
- **Document** - Ensure everything is captured properly
- **Drive** - Keep things moving, remove blockers, follow through

> 💡 **Think of it as:** You're the person who makes sure nothing falls through the cracks between "customer has a problem" and "problem is solved."

---

## 2️⃣ TRIAGE - "How Big Is the Fire?"

Decide the priority based on business impact and time pressure.

### 🚦 Priority Levels

| Priority | What it means | When to use |
|:--------:|---------------|-------------|
| 🔴 **P0** | Drop everything | Production down, enterprise blocked |
| 🟠 **P1** | Ship today | Critical feature broken |
| 🟡 **P2** | This week | Has workaround but needs fixing |
| 🟢 **P3** | Sprint | Planned improvements |

### 📊 Quick Decision Guide

|  | ⏰ Can't wait | ⏰ This week | ⏰ Can plan |
|--|:---:|:---:|:---:|
| 💥 **Critical** | P0 | P1 | P1 |
| ⚠️ **High** | P1 | P1 | P2 |
| 📌 **Medium** | P1 | P2 | P3 |
| 📎 **Low** | P2 | P3 | P3 |

---

## 3️⃣ DUE DILIGENCE - "Understand Before You Act"

Investigate properly before creating a ticket.

### ✅ Investigation Checklist

- [ ] Can I reproduce it?
- [ ] Who and how many are affected?
- [ ] Was there a similar ticket? (search Linear)
- [ ] Does it involve other teams?
- [ ] Do I have a hypothesis?
- [ ] Did I collect evidence (logs, screenshots)?

**When required:**
- P0/P1: Always mandatory
- P2: If cause is unclear
- P3: If it's complex

---

## 4️⃣ TICKET CREATION

### 📝 Standard Format

```
## Overview
[WHAT is happening + WHY it matters]
[Link to thread/CODA]

## Requirements
* [Specific action needed]

## Acceptance Criteria
* [How we know it's done]

## References
- [Links]
```

### 🏷️ Title Format

`[CUSTOMER] Verb + Object`

Examples:
- ✅ [QuickBooks] Fix failing login task
- ✅ [Gong] Refactor Engage templates
- ✅ [SPIKE] Investigate landing page issue

### 📋 Required Fields

| Field | Value |
|-------|-------|
| Title | `[Customer] Description` |
| Team | Platypus (PLA) |
| Priority | P0/P1/P2/P3 |
| Labels | Sprint + Type |
| State | Backlog |

---

## 5️⃣ EXECUTION

### 🔀 State Flow & Ownership

| State | Owner | Description |
|-------|-------|-------------|
| 📥 Backlog | TSA | New ticket, not yet prioritized |
| 📝 Refinement | TSA → Eng | Being detailed, TSA hands off to Eng |
| ✅ Refined | Eng Lead | Ready for sprint |
| 📋 Todo | Eng Lead | Prioritized for current sprint |
| 🔨 In Progress | Developer | Being built |
| 👀 Needs Review | Developer | PR open |
| 🚀 Ready for Deploy | Reviewer | PR approved |
| 🧪 Production QA | QA/TSA | Validating in prod |
| ✅ Done | - | Completed |

**Key point:** TSA owns the ticket until Refinement. After that, Engineering takes over.

---

## 6️⃣ MONITORING - "Don't Let It Die"

| Priority | Check frequency |
|:--------:|-----------------|
| 🔴 P0 | Constantly |
| 🟠 P1 | Multiple times/day |
| 🟡 P2 | Daily |
| 🟢 P3 | Standup/Review |

### When a ticket stalls:
1. Find the reason
2. Unblock it
3. Escalate if needed
4. Document what happened

---

## 7️⃣ VALIDATION → DELIVERY → CLOSEOUT

**Validation:** Confirm acceptance criteria are met.

**Delivery:** Deploy and monitor.

**Closeout:**
- Move to Done
- Add final comment
- Notify stakeholders
- Update CODA

---

# ⚠️ B. Critical Visibility Protocol

## 🚨 When to Escalate Immediately

If you identify a situation that is a **blocker** or **critical issue**, you must:

### 1️⃣ Communicate Fast
- Post in **#tsa-internal** or **#escalations** immediately
- Tag relevant people: TSA Lead, GTM stakeholders
- Don't wait for the next meeting

### 2️⃣ Sync with Leadership
- Bring it to **TSA Daily** with the Lead
- Update **GTM team** if customer-facing
- Use Slack threads for async updates

### 3️⃣ Keep Everyone in the Loop
- Update ticket status frequently
- Respond to questions quickly
- Create visibility through any documented channel (Slack, meetings, CODA)

> 🎯 **Rule:** The moment you realize something is critical, you should be communicating. Silence is the enemy.

---

# 👥 C. Who Does What

## 📊 RACI Matrix

| Stage | 📣 Requestor | 🎯 TSA | 🔧 Eng | 🧪 QA | 💼 GTM |
|-------|:------------:|:------:|:------:|:-----:|:------:|
| 📥 Intake | ✅ **R** | 📋 A | ℹ️ I | - | ℹ️ I |
| 🔍 Triage | 💬 C | ✅ **R/A** | ℹ️ I | - | 💬 C |
| 🔎 Due Diligence | ℹ️ I | ✅ **R/A** | 💬 C | - | 💬 C |
| 🎫 Ticket Creation | ℹ️ I | ✅ **R/A** | 💬 C | - | ℹ️ I |
| 🔨 Execution | - | ℹ️ I | ✅ **R/A** | ℹ️ I | - |
| 👀 Monitoring | ℹ️ I | ✅ **R** | 📋 A | ℹ️ I | ℹ️ I |
| ✅ Validation | - | 💬 C | ℹ️ I | ✅ **R/A** | 💬 C |
| 🚀 Closeout | ℹ️ I | ✅ **R/A** | ℹ️ I | ℹ️ I | ℹ️ I |

### Legend
| Symbol | Meaning |
|:------:|---------|
| ✅ **R** | Responsible - Does the work |
| 📋 **A** | Accountable - Final decision maker |
| 💬 **C** | Consulted - Provides input |
| ℹ️ **I** | Informed - Kept in the loop |

---

# 📐 D. Linear Standard

## 🚦 Priorities

| Level | Name | Meaning |
|:-----:|------|---------|
| 🔴 | P0 - Emergency | System on fire |
| 🟠 | P1 - Urgent | Must ship today |
| 🟡 | P2 - High | This week |
| 🟢 | P3 - Normal | In the sprint |

## 🏷️ Labels

| Label | When to Use |
|-------|-------------|
| 🐛 `Bug` | Something broke |
| ✨ `Feature` | New functionality |
| 🔍 `Spike` | Investigation |
| 📋 `RCA` | Post-incident analysis |
| 🏠 `Internal Request` | Internal need |
| 🤝 `Customer Request` | Customer need |
| 🔧 `Technical Debt` | Refactoring |
| 📝 `Worklog` | Documentation |

## ✅ Definition of Ready (DoR)

Before a ticket enters a sprint:
- [ ] Standard title format
- [ ] Clear overview
- [ ] Specific requirements
- [ ] Measurable acceptance criteria
- [ ] Priority set
- [ ] Labels applied

## ✅ Definition of Done (DoD)

Before closing a ticket:
- [ ] All acceptance criteria met
- [ ] In production (if applicable)
- [ ] Tests passing
- [ ] Stakeholders notified
- [ ] Final comment added

---

# 📝 E. Templates

| # | Template | Use Case | Key Fields |
|:-:|----------|----------|------------|
| 1 | 🐛 Bug | Something broke | Problem, Impact, Evidence |
| 2 | ✨ Feature | New functionality | Objective, Requirements |
| 3 | 🔍 Spike | Investigation | Question, Timebox |
| 4 | 📋 RCA | Post-incident | Timeline, Root Cause |
| 5 | 🏠 Internal | Internal request | Requester, Justification |
| 6 | 🤝 Customer | Customer request | Customer, Urgency |
| 7 | 🔧 Tech Debt | Refactoring | Current/Desired State |
| 8 | 🚀 Deploy | Release | Changes, Rollback Plan |
| 9 | 👋 Onboarding | Customer setup | Pre-requisites, Steps |
| 10 | 📝 Worklog | Documentation | Context, Learnings |

---

# 🔗 Resources & Contacts

## 📍 Where to Find Things

| Resource | Link |
|----------|------|
| 🎫 Linear (PLA) | [linear.app/testbox/team/PLA](https://linear.app/testbox/team/PLA) |
| 📚 CODA Solutions Central | [coda.io/d/_djfymaxsTtA](https://coda.io/d/_djfymaxsTtA) |
| 💬 #tsa-internal | Slack - TSA team |
| 💬 #customer-requests | Slack - Customer requests |
| 💬 #escalations | Slack - Urgent issues |

## 👥 Key Contacts

| Name | Role | Slack |
|------|------|-------|
| 🎯 Thiago Rodrigues | TSA Lead | @thiago |
| 📊 Lucas Wakigawa | Solutions Manager | @waki |

---

**Version 1.0** | January 26, 2026 | Thiago Rodrigues

---

> *"Where there is organization, it looks like there is no work. That's the goal - make the hard stuff look easy."*

