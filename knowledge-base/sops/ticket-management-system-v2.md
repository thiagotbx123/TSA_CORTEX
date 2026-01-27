# 🎫 Ticket Management System
## TSA TestBox - How We Get Things Done

**Version:** 2.0 | **Date:** 2026-01-27 | **Author:** Thiago Rodrigues | **Tool:** [Linear](https://linear.app/testbox/team/PLA)

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
| 🏠 Internal team | #scrum-of-scrums | Available TSA |
| 🚨 Sentry alert | #dev-on-call | Developer on-call |
| ⚡ Escalation | DM to GTM owner | TSA Lead |

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
| 📝 Refinement | Engineering | Being detailed by Eng (TSA hands off here) |
| ✅ Refined | Eng Lead | Ready for sprint |
| 📋 Todo | Eng Lead | Prioritized for current sprint |
| 🔨 In Progress | Developer | Being built |
| ⏸️ Blocked/Paused | Developer | Waiting on dependency |
| 👀 Needs Review | Developer | PR open |
| 🚀 Ready for Deploy | Reviewer | PR approved |
| 🧪 Production QA | TSA | Validating in prod |
| ✅ Done | - | Completed |

**Key point:** TSA owns the ticket until Backlog. Once moved to Refinement, Engineering takes over completely. TSA returns for Production QA validation.

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

**Validation:** TSA confirms acceptance criteria are met in production.

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
- Post in **#scrum-of-scrums** for team visibility
- Post in **#dev-on-call** for urgent technical issues
- **DM the GTM owner directly** for customer-impacting issues
- Don't wait for the next meeting

### 2️⃣ Escalation Rule

> 🎯 **Sam's guidance:** "When you are stuck for more than a couple of hours, please escalate quickly to the GTM owner. This is not a failure or incompetence. It shows ownership and care."

### 3️⃣ Keep Everyone in the Loop
- Update ticket status frequently
- Respond to questions quickly
- Create visibility through any documented channel (Slack, meetings, CODA)

> 🎯 **Rule:** The moment you realize something is critical, you should be communicating. Silence is the enemy.

---

# 🗓️ C. Meetings & Rituals

## 📅 TSA Meeting Cadence

| Type | Frequency | Participants | Purpose |
|------|-----------|--------------|---------|
| **Daily 1:1** | Daily | TSA Lead + each TSA | Individual alignment, blockers, priorities |
| **TSA Standup** | Weekly | All TSAs together | Team sync, cross-project visibility |
| **Scrum of Scrums** | Daily (async) | TSA → #scrum-of-scrums | Written daily report, general visibility |
| **Eng Standup** | As needed | TSA + Engineering | Technical alignment, dependencies |
| **GTM Sync** | As needed | TSA + GTM | Customer status, expectations, deadlines |
| **Project Sync** | Ad-hoc | Relevant stakeholders | Project-specific decisions |

## 📝 Daily Report Format (Scrum of Scrums)

Post daily in **#scrum-of-scrums**:

```
[Daily Agenda – YYYY-MM-DD]

PROJECT (Description – Priority – ETA)
 • Current status
 ▪ Do: Specific action ETA MM-DD
 ▪ Do: Another action
 References: [links]

ESCALATION: None / [description]
BLOCKERS: None / [description]
```

## 📋 Meeting Best Practices

**Daily 1:1 (TSA Lead + TSA):**
- What did you do yesterday?
- What will you do today?
- Any blockers / need help?

**TSA Weekly Standup:**
- Highlights from each person
- Cross-project blockers
- Next week priorities

**Syncs (Eng/GTM/Project):**
- Agenda defined beforehand
- Decisions documented
- Action items with owner + deadline

---

# 👥 D. Who Does What

## 📊 RACI Matrix

| Stage | 📣 Requestor | 🎯 TSA | 🔧 Eng | 💼 GTM |
|-------|:------------:|:------:|:------:|:------:|
| 📥 Intake | ✅ **R** | 📋 A | ℹ️ I | ℹ️ I |
| 🔍 Triage | 💬 C | ✅ **R/A** | ℹ️ I | 💬 C |
| 🔎 Due Diligence | ℹ️ I | ✅ **R/A** | 💬 C | 💬 C |
| 🎫 Ticket Creation | ℹ️ I | ✅ **R/A** | 💬 C | ℹ️ I |
| 🔨 Execution | - | ℹ️ I | ✅ **R/A** | - |
| 👀 Monitoring | ℹ️ I | ✅ **R** | 📋 A | ℹ️ I |
| ✅ Validation | - | ✅ **R/A** | ℹ️ I | 💬 C |
| 🚀 Closeout | ℹ️ I | ✅ **R/A** | ℹ️ I | ℹ️ I |

### Legend
| Symbol | Meaning |
|:------:|---------|
| ✅ **R** | Responsible - Does the work |
| 📋 **A** | Accountable - Final decision maker |
| 💬 **C** | Consulted - Provides input |
| ℹ️ **I** | Informed - Kept in the loop |

---

# 📐 E. Linear Standard

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
| 🐛 `Customer Issues` | Something broke |
| ✨ `Feature` | New functionality |
| 🔍 `Spike` | Investigation |
| 📋 `RCA` | Post-incident analysis |
| 🏠 `Internal Request` | Internal need |
| 🤝 `Customer Request` | Customer need |
| 🔧 `Refactor` | Technical debt / Refactoring |

## ✅ Before Creating a Ticket (Checklist)

Make sure your ticket has:
- [ ] Standard title format `[Customer] Description`
- [ ] Clear overview explaining WHAT and WHY
- [ ] Specific requirements
- [ ] Measurable acceptance criteria
- [ ] Priority set (P0-P3)
- [ ] Appropriate labels applied

## ✅ Before Closing a Ticket (Checklist)

Verify that:
- [ ] All acceptance criteria are met
- [ ] Changes are in production (if applicable)
- [ ] Tests are passing
- [ ] Stakeholders have been notified
- [ ] Final comment added summarizing the resolution

---

# 📝 F. Templates

| # | Template | Use Case | Key Fields | 🔗 Template |
|:-:|----------|----------|------------|-------------|
| 1 | 🐛 Bug | Something broke | Problem, Impact, Evidence | [RAC-44](https://linear.app/testbox/issue/RAC-44) |
| 2 | ✨ Feature | New functionality | Objective, Requirements | [RAC-45](https://linear.app/testbox/issue/RAC-45) |
| 3 | 🔍 Spike | Investigation | Question, Timebox | [RAC-46](https://linear.app/testbox/issue/RAC-46) |
| 4 | 📋 RCA | Post-incident | Timeline, Root Cause | [RAC-47](https://linear.app/testbox/issue/RAC-47) |
| 5 | 🏠 Internal | Internal request | Requester, Justification | [RAC-48](https://linear.app/testbox/issue/RAC-48) |
| 6 | 🤝 Customer | Customer request | Customer, Urgency | [RAC-49](https://linear.app/testbox/issue/RAC-49) |
| 7 | 🔧 Tech Debt | Refactoring | Current/Desired State | [RAC-50](https://linear.app/testbox/issue/RAC-50) |
| 8 | 🚀 Deploy | Release | Changes, Rollback Plan | [RAC-51](https://linear.app/testbox/issue/RAC-51) |
| 9 | 👋 Onboarding | Customer setup | Pre-requisites, Steps | [RAC-52](https://linear.app/testbox/issue/RAC-52) |
| 10 | 📝 Worklog | Documentation | Context, Learnings | [RAC-53](https://linear.app/testbox/issue/RAC-53) |
| 11 | 🛠️ Implementation | Feature build | Specs, Phases, DoD | [RAC-54](https://linear.app/testbox/issue/RAC-54) |

---

# 🔗 Resources & Contacts

## 📍 Where to Find Things

| Resource | Link |
|----------|------|
| 🎫 Linear (PLA) | [linear.app/testbox/team/PLA](https://linear.app/testbox/team/PLA) |
| 📚 CODA Solutions Central | [coda.io/d/_djfymaxsTtA](https://coda.io/d/_djfymaxsTtA) |
| 💬 #scrum-of-scrums | Slack - Daily reports (MAIN) |
| 💬 #customer-requests | Slack - Customer requests |
| 💬 #dev-on-call | Slack - Urgent issues / On-call |

## 👥 Key Contacts

| Name | Role | Slack |
|------|------|-------|
| 🎯 Thiago Rodrigues | TSA Lead | @thiago |
| 📊 Lucas Wakigawa | Tech Lead / Manager | @lucas.w |
| 💼 Katherine (Kat) | GTM Lead | @kat |
| 🔧 Lucas Soranzo | Engineering Lead | @lucassoranzo |

---

**Version 2.0** | January 27, 2026 | Thiago Rodrigues

---

> *"Where there is organization, it looks like there is no work. That's the goal - make the hard stuff look easy."*
