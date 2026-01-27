const https = require('https');
require('dotenv').config({ path: '../.env' });

const TEAM_ID = '5a021b9f-bb1a-49fa-ad3b-83422c46c357'; // RAC - Raccoons
const API_KEY = process.env.LINEAR_API_KEY;

const templates = [
  {
    title: '[TEMPLATE] 🐛 Bug Report - How to Report Issues',
    description: `## 🎯 How to Use This Template

*This is a reference template. Copy the structure below when creating bug tickets.*
*Delete all italic guidance text before submitting.*

---

## Overview

*Describe WHAT is happening and WHY it matters in 2-3 sentences.*
*Include the customer/integration name and a link to the original request (Slack/CODA).*

**Example:**
> Login task is failing for all QuickBooks sandbox accounts since Jan 25. This blocks 3 enterprise demos scheduled for this week.
> Thread: [#customer-requests](link)

---

## Evidence

*Attach proof of the issue. The more context, the faster the fix.*

- **Slack thread:** *[link to original report]*
- **Screenshot/Video:** *[attach or link]*
- **Sentry/Logs:** *[link if available]*
- **Error message:** *[exact error text]*

---

## Environment

*Where is this happening?*

| Field | Value |
|-------|-------|
| **Env** | *Production / Staging / Local* |
| **Service** | *e.g., Integration Services, Fleet, UI* |
| **Customer/Tenant** | *e.g., QuickBooks - Keystone Construction* |
| **Browser/Device** | *if UI issue: Chrome 120, macOS* |

---

## Steps to Reproduce

*Numbered steps to recreate the issue. Be specific.*

1. *Go to [URL or screen]*
2. *Click on [element]*
3. *Enter [data]*
4. *Observe [error]*

**Frequency:** *Always / Intermittent (X out of Y attempts) / Once*

---

## Expected vs Actual

| | Description |
|---|-------------|
| **Expected** | *What SHOULD happen* |
| **Actual** | *What IS happening* |

---

## Business Impact

*Why does this matter? Who is affected?*

- **Users affected:** *e.g., All QBO users, 1 enterprise customer*
- **Revenue impact:** *e.g., Blocks $50k deal demo*
- **Urgency:** *e.g., Demo scheduled for tomorrow*

---

## Root Cause (if known)

*Optional: If you have a hypothesis or found the cause during investigation.*

---

## Requirements

*What needs to be done to fix this?*

- [ ] *Specific action 1*
- [ ] *Specific action 2*

---

## Acceptance Criteria

*How do we know it's fixed? Be measurable.*

- [ ] *Login task completes successfully for QBO sandboxes*
- [ ] *No errors in Sentry for 24h after deploy*
- [ ] *Customer confirms issue resolved*

---

## References

| Type | Link |
|------|------|
| Related tickets | *RAC-XXXX, PLA-XXXX* |
| Documentation | *CODA page, Confluence* |
| Code location | *file.ts:123* |

---

## 📋 Process Reminder (TSA Ticket Lifecycle)

### Before Creating This Ticket
1. ✅ Can I reproduce it?
2. ✅ Who and how many are affected?
3. ✅ Did I search for similar tickets in Linear?
4. ✅ Did I collect evidence (logs, screenshots)?

### After Creating
1. Set **Priority** (P0-P3) based on impact
2. Add **Labels**: \`Bug\` + Sprint if applicable
3. Set **State**: \`Backlog\`
4. **TSA owns until Refinement** → then Engineering takes over

### Monitoring
| Priority | Check Frequency |
|:--------:|-----------------|
| 🔴 P0 | Constantly |
| 🟠 P1 | Multiple times/day |
| 🟡 P2 | Daily |
| 🟢 P3 | Standup/Review |

---

*Template v1.0 | TSA Ticket Management System | [Full Guide](https://coda.io/d/Solutions-Central_djfymaxsTtA/Linear-Ticket-Management_sukx4jIV)*`
  },
  {
    title: '[TEMPLATE] ✨ Feature Request - New Functionality',
    description: `## 🎯 How to Use This Template

*This is a reference template for requesting new features or enhancements.*
*Delete all italic guidance text before submitting.*

---

## Overview

*What do you want to build and WHY does it matter?*
*Include the customer/business context and link to original request.*

**Example:**
> Add bulk export functionality to the Reports page. Enterprise customers need to export 100+ reports at once for quarterly audits.
> Request: [#customer-requests thread](link)

---

## Objective

*What is the goal? What problem does this solve?*

- **User Story:** As a [persona], I want to [action] so that [benefit]
- **Business Value:** *e.g., Reduces manual work by 80%, enables $100k deal*

---

## Requirements

*What specifically needs to be built? Be detailed.*

### Functional Requirements
- [ ] *Requirement 1 - what it must do*
- [ ] *Requirement 2 - what it must do*
- [ ] *Requirement 3 - what it must do*

### Non-Functional Requirements
- [ ] *Performance: e.g., Must handle 1000 items in <5s*
- [ ] *Security: e.g., Must respect existing permissions*
- [ ] *Compatibility: e.g., Must work on Chrome, Firefox, Safari*

---

## Scope

### In Scope
- *Item 1*
- *Item 2*

### Out of Scope
- *Item explicitly NOT included*
- *Future enhancement (v2)*

---

## Design / Mockups

*Attach wireframes, mockups, or describe the expected UI/UX.*

- **Mockup:** *[link or attach image]*
- **Figma:** *[link if available]*
- **Reference:** *[similar feature in another product]*

---

## Technical Considerations

*Any technical constraints, dependencies, or suggestions?*

- **API changes:** *e.g., New endpoint needed*
- **Database:** *e.g., New table/column required*
- **Dependencies:** *e.g., Requires Feature X to be completed first*
- **Risks:** *e.g., May impact performance of Y*

---

## Acceptance Criteria

*How do we know it's done? Be specific and testable.*

- [ ] *User can do X*
- [ ] *System shows Y when Z happens*
- [ ] *Performance meets threshold of W*
- [ ] *Automated tests cover the new functionality*

---

## References

| Type | Link |
|------|------|
| Original request | *Slack/CODA link* |
| Related tickets | *RAC-XXXX* |
| Documentation | *Spec doc, PRD* |
| Competitor reference | *How others do it* |

---

## 📋 Process Reminder (TSA Ticket Lifecycle)

### Before Creating This Ticket
1. ✅ Is this a real need or a nice-to-have?
2. ✅ Did I validate with stakeholders?
3. ✅ Did I search for existing similar requests?
4. ✅ Is the scope clear and achievable?

### After Creating
1. Set **Priority** (P0-P3) based on business value
2. Add **Labels**: \`Feature\` + Sprint if applicable
3. Set **State**: \`Backlog\`
4. **TSA owns until Refinement** → then Engineering takes over

---

*Template v1.0 | TSA Ticket Management System | [Full Guide](https://coda.io/d/Solutions-Central_djfymaxsTtA/Linear-Ticket-Management_sukx4jIV)*`
  },
  {
    title: '[TEMPLATE] 🔍 Spike - Technical Investigation',
    description: `## 🎯 How to Use This Template

*This is a reference template for investigation/research tasks.*
*A Spike is time-boxed research to reduce uncertainty before committing to work.*
*Delete all italic guidance text before submitting.*

---

## Overview

*What are we investigating and WHY?*
*Include context on what triggered this investigation.*

**Example:**
> Investigate feasibility of migrating from REST to GraphQL for the Reporting API. Current REST endpoints are hitting performance limits with complex queries.
> Context: [Engineering discussion](link)

---

## Question(s) to Answer

*What specific questions need to be answered?*

1. *Primary question - the main thing we need to learn*
2. *Secondary question - additional insight needed*
3. *Tertiary question - nice to know*

---

## Hypothesis

*What do we think the answer might be? (Optional but helpful)*

> *We believe that [approach X] will solve [problem Y] because [reason Z].*

---

## Timebox

*How much time should be spent on this investigation?*

| Field | Value |
|-------|-------|
| **Max Duration** | *e.g., 4 hours / 1 day / 3 days* |
| **Deadline** | *e.g., Before sprint planning on Monday* |
| **Checkpoint** | *e.g., Update after 2 hours* |

> ⚠️ **Important:** If timebox expires without answer, document findings and escalate for decision.

---

## Investigation Approach

*How will we investigate? What steps?*

1. *Step 1 - e.g., Review existing documentation*
2. *Step 2 - e.g., Build proof of concept*
3. *Step 3 - e.g., Test with sample data*
4. *Step 4 - e.g., Document findings*

---

## Resources Needed

*What do you need to complete this investigation?*

- **Access:** *e.g., Production logs, specific environment*
- **People:** *e.g., 30 min with backend engineer*
- **Tools:** *e.g., Profiler, specific test account*

---

## Expected Output

*What will be delivered at the end?*

- [ ] Written summary of findings
- [ ] Recommendation (go/no-go)
- [ ] If go: rough estimate for implementation
- [ ] If no-go: alternative approaches identified
- [ ] Risks and unknowns documented

---

## Success Criteria

*When is this spike "done"?*

- [ ] All questions answered (or documented as unanswerable)
- [ ] Clear recommendation provided
- [ ] Findings shared with team
- [ ] Next steps defined

---

## References

| Type | Link |
|------|------|
| Related context | *Slack thread, meeting notes* |
| Documentation | *Existing docs, RFCs* |
| Similar past spikes | *RAC-XXX* |

---

## 📋 Process Reminder (TSA Ticket Lifecycle)

### Before Creating This Spike
1. ✅ Is investigation really needed? (vs just doing the work)
2. ✅ Is the question clear and answerable?
3. ✅ Is the timebox realistic?
4. ✅ Who needs the answer and by when?

### After Creating
1. Set **Priority** based on urgency of decision
2. Add **Labels**: \`Spike\`
3. **Respect the timebox** - don't let it drag
4. **Document even partial findings** - they're valuable

---

*Template v1.0 | TSA Ticket Management System | [Full Guide](https://coda.io/d/Solutions-Central_djfymaxsTtA/Linear-Ticket-Management_sukx4jIV)*`
  },
  {
    title: '[TEMPLATE] 📋 RCA - Root Cause Analysis',
    description: `## 🎯 How to Use This Template

*This is a reference template for post-incident Root Cause Analysis.*
*RCAs help us learn from incidents and prevent recurrence.*
*Delete all italic guidance text before submitting.*

---

## Incident Summary

| Field | Value |
|-------|-------|
| **Incident ID** | *e.g., INC-2024-001* |
| **Date/Time** | *e.g., 2024-01-15 14:30 UTC* |
| **Duration** | *e.g., 2 hours 15 minutes* |
| **Severity** | *P0 / P1 / P2* |
| **Affected Systems** | *e.g., Integration Services, QuickBooks* |
| **Affected Customers** | *e.g., 15 enterprise accounts* |
| **Incident Commander** | *Name* |

---

## Executive Summary

*2-3 sentence summary of what happened, impact, and resolution.*

**Example:**
> On Jan 15, the QuickBooks integration experienced a 2-hour outage due to an expired API credential. This affected 15 enterprise customers and blocked approximately 500 sync operations. The issue was resolved by rotating the credentials and implementing automated monitoring.

---

## Timeline

*Chronological sequence of events. Be precise with timestamps.*

| Time (UTC) | Event |
|------------|-------|
| 14:30 | *First alert triggered - API errors spike* |
| 14:35 | *On-call engineer paged* |
| 14:45 | *Initial investigation - identified auth failures* |
| 15:00 | *Root cause identified - expired credential* |
| 15:15 | *Fix deployed - new credential rotated* |
| 15:30 | *Monitoring confirmed - errors resolved* |
| 16:45 | *Incident closed - all systems nominal* |

---

## Root Cause

*What was the underlying cause? Go deep - ask "why" 5 times.*

### Primary Cause
*The direct technical cause*
> *e.g., API credential expired after 90-day rotation policy*

### Contributing Factors
- *Factor 1 - e.g., No automated credential rotation*
- *Factor 2 - e.g., No alerting on credential expiration*
- *Factor 3 - e.g., Documentation outdated*

### 5 Whys Analysis
1. **Why did the integration fail?** *API returned 401 Unauthorized*
2. **Why was it unauthorized?** *Credential had expired*
3. **Why did the credential expire?** *90-day rotation policy*
4. **Why wasn't it rotated?** *Manual process, no reminder*
5. **Why no reminder?** *No monitoring on credential age*

---

## Impact

*Quantify the damage*

| Metric | Value |
|--------|-------|
| **Downtime** | *2 hours 15 minutes* |
| **Failed Operations** | *~500 sync attempts* |
| **Customers Affected** | *15 enterprise accounts* |
| **Revenue Impact** | *$X delayed / at risk* |
| **SLA Breach** | *Yes/No - details* |
| **Customer Complaints** | *3 support tickets* |

---

## Resolution

*How was the incident resolved?*

### Immediate Actions (During Incident)
- [ ] *Action 1 - e.g., Rotated API credential*
- [ ] *Action 2 - e.g., Restarted affected services*
- [ ] *Action 3 - e.g., Communicated to customers*

### Verification
- [ ] *Confirmed all systems operational*
- [ ] *Verified no data loss*
- [ ] *Checked all affected customers*

---

## Action Items (Prevention)

*What will we do to prevent this from happening again?*

| # | Action | Owner | Priority | Due Date | Status |
|:-:|--------|-------|:--------:|----------|:------:|
| 1 | *Implement automated credential rotation* | *@engineer* | P1 | *2024-01-22* | 🔲 |
| 2 | *Add alerting for credential expiration (7 days before)* | *@engineer* | P1 | *2024-01-22* | 🔲 |
| 3 | *Update runbook with credential management* | *@tsa* | P2 | *2024-01-25* | 🔲 |
| 4 | *Quarterly credential audit process* | *@lead* | P3 | *2024-02-01* | 🔲 |

---

## Lessons Learned

*What did we learn? What went well? What could improve?*

### What Went Well
- *Fast detection - alerts fired within 5 minutes*
- *Clear escalation path*
- *Good communication during incident*

### What Could Improve
- *Credential management needs automation*
- *Runbook was outdated*
- *No proactive monitoring for expiration*

---

## References

| Type | Link |
|------|------|
| Incident channel | *#incident-2024-001* |
| Alerts | *PagerDuty/Sentry links* |
| Related tickets | *Fix tickets created* |
| Post-mortem meeting | *Recording/notes* |

---

## 📋 Process Reminder

### RCA Best Practices
- **Blameless:** Focus on systems, not individuals
- **Thorough:** Don't stop at surface cause
- **Actionable:** Every finding should have an action item
- **Time-bound:** Complete RCA within 5 business days
- **Shared:** Distribute learnings to broader team

---

*Template v1.0 | TSA Ticket Management System | [Full Guide](https://coda.io/d/Solutions-Central_djfymaxsTtA/Linear-Ticket-Management_sukx4jIV)*`
  },
  {
    title: '[TEMPLATE] 🏠 Internal Request - Team Needs',
    description: `## 🎯 How to Use This Template

*This is a reference template for internal team requests.*
*Use this for tooling, process improvements, or internal needs (not customer-facing).*
*Delete all italic guidance text before submitting.*

---

## Overview

*What do you need and WHY?*
*Include context on how this helps the team.*

**Example:**
> Need a script to automate weekly report generation. Currently takes 2 hours every Monday to compile data from 5 different sources manually.
> Requester: @thiago

---

## Requester Information

| Field | Value |
|-------|-------|
| **Requester** | *@name* |
| **Team** | *TSA / Engineering / GTM* |
| **Date Requested** | *2024-01-15* |
| **Urgency** | *Low / Medium / High* |

---

## Problem Statement

*What problem are you trying to solve?*

- **Current State:** *How things work today*
- **Pain Point:** *What's wrong or inefficient*
- **Frequency:** *How often this is a problem*
- **Time Wasted:** *Hours per week/month*

---

## Proposed Solution

*What do you want built/changed?*

- *Requirement 1*
- *Requirement 2*
- *Requirement 3*

---

## Justification

*Why should we prioritize this?*

| Factor | Impact |
|--------|--------|
| **Time Saved** | *e.g., 8 hours/month* |
| **Error Reduction** | *e.g., Eliminates manual mistakes* |
| **Team Benefit** | *e.g., All 5 TSAs will use this* |
| **Dependencies** | *e.g., Blocks other improvements* |

---

## Acceptance Criteria

*How do we know it's done?*

- [ ] *Criteria 1*
- [ ] *Criteria 2*
- [ ] *Criteria 3*

---

## Alternatives Considered

*Did you consider other approaches?*

| Alternative | Pros | Cons | Why Not |
|-------------|------|------|---------|
| *Option A* | *...* | *...* | *...* |
| *Option B* | *...* | *...* | *...* |

---

## References

| Type | Link |
|------|------|
| Related discussion | *Slack thread* |
| Similar tools | *Existing solution reference* |
| Documentation | *Specs, requirements* |

---

## 📋 Process Reminder (TSA Ticket Lifecycle)

### Before Creating This Ticket
1. ✅ Is this really needed? (vs nice-to-have)
2. ✅ Did I check if something similar exists?
3. ✅ Did I discuss with the team first?
4. ✅ Can I justify the time investment?

### After Creating
1. Set **Priority** based on impact
2. Add **Labels**: \`Internal Request\`
3. Be patient - internal requests are usually P2/P3

---

*Template v1.0 | TSA Ticket Management System | [Full Guide](https://coda.io/d/Solutions-Central_djfymaxsTtA/Linear-Ticket-Management_sukx4jIV)*`
  },
  {
    title: '[TEMPLATE] 🤝 Customer Request - Client Needs',
    description: `## 🎯 How to Use This Template

*This is a reference template for customer-originated requests.*
*Use this when a customer asks for something specific.*
*Delete all italic guidance text before submitting.*

---

## Overview

*What does the customer need and WHY?*
*Include the business context and urgency.*

**Example:**
> Acme Corp needs the ability to filter reports by custom date ranges. Their finance team runs monthly audits and current weekly-only filter doesn't meet compliance requirements.
> Customer contact: John Smith (john@acme.com)

---

## Customer Information

| Field | Value |
|-------|-------|
| **Customer** | *Company Name* |
| **Contact** | *Name, email* |
| **Account Type** | *Enterprise / Growth / Startup* |
| **ARR** | *$XXX,XXX* |
| **CSM/Account Lead** | *@name* |
| **Request Date** | *2024-01-15* |

---

## Request Details

*What exactly is the customer asking for?*

### The Ask
*In the customer's words (paraphrased)*
> *"We need to be able to..."*

### Translated Requirements
- *Technical requirement 1*
- *Technical requirement 2*
- *Technical requirement 3*

---

## Urgency & Impact

| Factor | Value |
|--------|-------|
| **Urgency** | *🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low* |
| **Deadline** | *e.g., Before Q2 audit on March 31* |
| **Blocker?** | *Yes - blocks renewal / No* |
| **Revenue at Risk** | *$XXX,XXX ARR* |
| **Other Customers** | *X others have asked for similar* |

---

## Business Context

*Why does the customer need this?*

- **Use Case:** *How they'll use it*
- **Current Workaround:** *What they do today (if any)*
- **Compliance/Legal:** *Any regulatory requirements*
- **Competitive:** *Do competitors offer this?*

---

## Proposed Solution

*How might we solve this?*

### Option A: *[Name]*
- Description: *...*
- Effort: *S / M / L*
- Pros: *...*
- Cons: *...*

### Option B: *[Name]* (if applicable)
- Description: *...*
- Effort: *S / M / L*
- Pros: *...*
- Cons: *...*

---

## Acceptance Criteria

*How do we know the customer is satisfied?*

- [ ] *Customer can do X*
- [ ] *Feature works as specified*
- [ ] *Customer confirms satisfaction*

---

## Communication Plan

| Milestone | Who Communicates | To Whom | When |
|-----------|------------------|---------|------|
| Request received | TSA | Customer | Immediately |
| Prioritization decision | CSM | Customer | Within 1 week |
| Development started | TSA | Customer | When work begins |
| Ready for testing | TSA | Customer | Before release |
| Released | CSM | Customer | At launch |

---

## References

| Type | Link |
|------|------|
| Original request | *Email / Slack / Support ticket* |
| Customer CODA page | *Solutions Central link* |
| Related tickets | *Similar requests* |
| Salesforce | *Opportunity link if applicable* |

---

## 📋 Process Reminder (TSA Ticket Lifecycle)

### Before Creating This Ticket
1. ✅ Did I understand the REAL need (not just the ask)?
2. ✅ Did I validate urgency with CSM/Account Lead?
3. ✅ Did I check if we already have this or similar?
4. ✅ Did I set proper expectations with customer?

### After Creating
1. Set **Priority** based on customer impact + revenue
2. Add **Labels**: \`Customer Request\` + customer name if available
3. **Keep customer updated** - silence is the enemy
4. **Close the loop** when resolved

---

*Template v1.0 | TSA Ticket Management System | [Full Guide](https://coda.io/d/Solutions-Central_djfymaxsTtA/Linear-Ticket-Management_sukx4jIV)*`
  },
  {
    title: '[TEMPLATE] 🔧 Tech Debt - Refactoring & Cleanup',
    description: `## 🎯 How to Use This Template

*This is a reference template for technical debt items.*
*Use this for refactoring, cleanup, or improving code quality.*
*Delete all italic guidance text before submitting.*

---

## Overview

*What technical debt are we addressing and WHY now?*

**Example:**
> The authentication module has grown organically over 2 years and now has 15 different auth methods scattered across 8 files. This makes adding new auth providers error-prone and increases onboarding time for new engineers.

---

## Current State

*Describe the problem in detail*

### What's Wrong
- *Problem 1 - e.g., Code duplication across 8 files*
- *Problem 2 - e.g., No test coverage for auth flows*
- *Problem 3 - e.g., Inconsistent error handling*

### Evidence
- **Code Locations:** *file1.ts:100-200, file2.ts:50-150*
- **Metrics:** *e.g., 45% code duplication, 12% test coverage*
- **Incidents:** *e.g., Last 3 auth bugs traced to this code*

### Impact of NOT Fixing
- *Risk 1 - e.g., High probability of bugs when adding features*
- *Risk 2 - e.g., 2x longer onboarding for new engineers*
- *Risk 3 - e.g., Security vulnerabilities harder to audit*

---

## Desired State

*What should it look like after refactoring?*

### Goals
- *Goal 1 - e.g., Single source of truth for auth logic*
- *Goal 2 - e.g., 80%+ test coverage*
- *Goal 3 - e.g., Clear interfaces for adding new providers*

### Architecture / Design
*Describe or link to the target architecture*

\`\`\`
*ASCII diagram or link to design doc*
\`\`\`

---

## Approach

*How will we tackle this?*

### Strategy
- [ ] *Phase 1 - e.g., Extract common interfaces*
- [ ] *Phase 2 - e.g., Consolidate implementations*
- [ ] *Phase 3 - e.g., Add comprehensive tests*
- [ ] *Phase 4 - e.g., Remove deprecated code*

### Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| *Breaking existing functionality* | *Feature flags, incremental rollout* |
| *Scope creep* | *Strict phase boundaries* |

---

## Effort Estimate

| Phase | Effort | Dependencies |
|-------|--------|--------------|
| Phase 1 | *X days* | *None* |
| Phase 2 | *X days* | *Phase 1* |
| Phase 3 | *X days* | *Phase 2* |
| **Total** | *X days* | |

---

## Acceptance Criteria

*How do we know the debt is paid?*

- [ ] *All auth logic consolidated in single module*
- [ ] *Test coverage > 80%*
- [ ] *No code duplication (DRY)*
- [ ] *Documentation updated*
- [ ] *Old code removed (not just deprecated)*

---

## References

| Type | Link |
|------|------|
| Code locations | *GitHub links to problematic code* |
| Design doc | *RFC or architecture doc* |
| Related incidents | *Past bugs caused by this debt* |
| Similar refactors | *Past successful cleanups* |

---

## 📋 Process Reminder (TSA Ticket Lifecycle)

### Before Creating This Ticket
1. ✅ Is this debt actually causing problems? (vs theoretical)
2. ✅ Did I quantify the impact?
3. ✅ Is now the right time? (vs other priorities)
4. ✅ Did I get engineering buy-in?

### After Creating
1. Set **Priority** based on risk + frequency of pain
2. Add **Labels**: \`Technical Debt\`
3. **Be realistic** about effort - refactoring always takes longer
4. **Don't gold-plate** - fix the problem, don't rewrite everything

---

*Template v1.0 | TSA Ticket Management System | [Full Guide](https://coda.io/d/Solutions-Central_djfymaxsTtA/Linear-Ticket-Management_sukx4jIV)*`
  },
  {
    title: '[TEMPLATE] 🚀 Deploy - Release Checklist',
    description: `## 🎯 How to Use This Template

*This is a reference template for deployment/release tickets.*
*Use this to track releases and ensure nothing is missed.*
*Delete all italic guidance text before submitting.*

---

## Release Summary

| Field | Value |
|-------|-------|
| **Release Name** | *e.g., v2.5.0 / Feature X Launch* |
| **Target Date** | *2024-01-20* |
| **Release Manager** | *@name* |
| **Environment** | *Production / Staging* |
| **Type** | *Feature / Hotfix / Maintenance* |

---

## What's Being Released

*List all changes included in this release*

### Features
- [ ] *Feature 1 - [TICKET-123](link)*
- [ ] *Feature 2 - [TICKET-124](link)*

### Bug Fixes
- [ ] *Fix 1 - [TICKET-125](link)*
- [ ] *Fix 2 - [TICKET-126](link)*

### Other Changes
- [ ] *Config change - description*
- [ ] *Database migration - description*

---

## Pre-Deployment Checklist

*Complete before deploying*

### Code Ready
- [ ] All PRs merged to release branch
- [ ] Code review completed
- [ ] All tests passing (CI green)
- [ ] No critical/blocking issues open

### Testing
- [ ] QA sign-off obtained
- [ ] Staging deployment successful
- [ ] Smoke tests passed
- [ ] Performance testing done (if applicable)

### Documentation
- [ ] Release notes prepared
- [ ] Runbook updated (if needed)
- [ ] Customer-facing docs updated (if needed)

### Communication
- [ ] Team notified of release window
- [ ] Stakeholders informed
- [ ] Support team briefed on changes

---

## Deployment Steps

*Step-by-step deployment procedure*

1. [ ] *Announce deployment start in #deployments*
2. [ ] *Run database migrations (if any)*
3. [ ] *Deploy backend services*
4. [ ] *Deploy frontend*
5. [ ] *Verify health checks*
6. [ ] *Run smoke tests*
7. [ ] *Monitor error rates for 15 minutes*
8. [ ] *Announce deployment complete*

---

## Rollback Plan

*How to revert if something goes wrong*

### Rollback Trigger
*When do we rollback?*
- Error rate > X%
- P0 bug discovered
- Customer-reported critical issue

### Rollback Steps
1. [ ] *Step 1 - e.g., Revert deployment in CI/CD*
2. [ ] *Step 2 - e.g., Run rollback migration*
3. [ ] *Step 3 - e.g., Verify previous version running*
4. [ ] *Step 4 - e.g., Notify team*

### Rollback Owner
*@name - who has authority to decide*

---

## Post-Deployment Checklist

*Complete after deploying*

- [ ] All services healthy
- [ ] Error rates normal
- [ ] Key flows verified in production
- [ ] Monitoring dashboards checked
- [ ] Release notes published
- [ ] Stakeholders notified of completion

---

## Monitoring

*What to watch after release*

| Metric | Normal Range | Dashboard |
|--------|--------------|-----------|
| Error rate | < 0.1% | *[Link]* |
| Latency p99 | < 500ms | *[Link]* |
| CPU/Memory | < 70% | *[Link]* |

---

## References

| Type | Link |
|------|------|
| Release branch | *GitHub link* |
| CI/CD pipeline | *Link* |
| Monitoring | *Datadog/Grafana* |
| Incident channel | *#incidents* |

---

## 📋 Process Reminder

### Release Best Practices
- **Never deploy on Friday** (unless hotfix)
- **Have rollback ready** before starting
- **Monitor actively** for at least 30 minutes
- **Communicate early and often**
- **Document any issues** for future releases

---

*Template v1.0 | TSA Ticket Management System | [Full Guide](https://coda.io/d/Solutions-Central_djfymaxsTtA/Linear-Ticket-Management_sukx4jIV)*`
  },
  {
    title: '[TEMPLATE] 👋 Onboarding - Customer Setup',
    description: `## 🎯 How to Use This Template

*This is a reference template for customer onboarding tasks.*
*Use this to track new customer setup and ensure consistent experience.*
*Delete all italic guidance text before submitting.*

---

## Customer Overview

| Field | Value |
|-------|-------|
| **Customer** | *Company Name* |
| **Contract Start** | *2024-01-15* |
| **Account Type** | *Enterprise / Growth / Startup* |
| **ARR** | *$XXX,XXX* |
| **CSM** | *@name* |
| **TSA Assigned** | *@name* |
| **Target Go-Live** | *2024-02-01* |

---

## Onboarding Scope

*What's included in this onboarding?*

### Products/Integrations
- [ ] *Integration 1 - e.g., Salesforce*
- [ ] *Integration 2 - e.g., HubSpot*
- [ ] *Feature 1 - e.g., Custom Reports*

### Users
| User | Role | Email |
|------|------|-------|
| *Admin 1* | *Admin* | *email@company.com* |
| *User 1* | *Viewer* | *email@company.com* |

---

## Pre-Requisites

*What needs to be ready before we start?*

### From Customer
- [ ] *Credentials for integration X*
- [ ] *Admin access to system Y*
- [ ] *Data export from legacy system*
- [ ] *User list with roles*

### From TestBox
- [ ] *Environment provisioned*
- [ ] *Sandbox accounts created*
- [ ] *API keys generated*

---

## Onboarding Steps

*Track progress through onboarding phases*

### Phase 1: Environment Setup
- [ ] Create customer environment
- [ ] Configure integrations
- [ ] Import initial data
- [ ] Verify connections

### Phase 2: Configuration
- [ ] Set up user accounts
- [ ] Configure permissions
- [ ] Customize settings per requirements
- [ ] Set up automations

### Phase 3: Data & Content
- [ ] Import/create sample data
- [ ] Configure reports/dashboards
- [ ] Set up templates
- [ ] Verify data accuracy

### Phase 4: Training & Handoff
- [ ] Schedule training sessions
- [ ] Deliver admin training
- [ ] Deliver user training
- [ ] Provide documentation

### Phase 5: Go-Live
- [ ] Final review with customer
- [ ] Production cutover
- [ ] Monitor for 48 hours
- [ ] Official handoff to CSM

---

## Timeline

| Phase | Target Date | Status |
|-------|-------------|--------|
| Environment Setup | *2024-01-17* | 🔲 |
| Configuration | *2024-01-22* | 🔲 |
| Data & Content | *2024-01-25* | 🔲 |
| Training | *2024-01-29* | 🔲 |
| Go-Live | *2024-02-01* | 🔲 |

---

## Risks & Blockers

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| *Customer delays on credentials* | Medium | High | *Send reminder 3 days before* |
| *Data quality issues* | Medium | Medium | *Validate sample first* |

---

## Success Criteria

*How do we know onboarding is successful?*

- [ ] All integrations connected and syncing
- [ ] All users can log in and access features
- [ ] Customer confirms data accuracy
- [ ] Training completed with positive feedback
- [ ] Customer actively using the platform

---

## Communication Plan

| Event | Channel | Audience |
|-------|---------|----------|
| Kickoff | Video call | Customer + TSA + CSM |
| Weekly updates | Email | Customer + CSM |
| Blockers | Slack | Internal team |
| Go-live | Video call | Customer + TSA + CSM |

---

## References

| Type | Link |
|------|------|
| Customer CODA page | *Solutions Central link* |
| Contract/SOW | *Link* |
| Technical requirements | *Link* |
| Training materials | *Link* |

---

## 📋 Process Reminder (TSA Ticket Lifecycle)

### Onboarding Best Practices
1. **Set clear expectations** from day 1
2. **Overcommunicate** - silence worries customers
3. **Document everything** - future you will thank you
4. **Escalate early** if timeline at risk
5. **Celebrate go-live** - it's a big deal for the customer

---

*Template v1.0 | TSA Ticket Management System | [Full Guide](https://coda.io/d/Solutions-Central_djfymaxsTtA/Linear-Ticket-Management_sukx4jIV)*`
  },
  {
    title: '[TEMPLATE] 📝 Worklog - Documentation & Learning',
    description: `## 🎯 How to Use This Template

*This is a reference template for documenting work and capturing learnings.*
*Use this for weekly updates, knowledge capture, or activity logging.*
*Delete all italic guidance text before submitting.*

---

## Summary

| Field | Value |
|-------|-------|
| **Period** | *2024-01-08 to 2024-01-14* |
| **Author** | *@name* |
| **Role** | *TSA / Engineer / PM* |

---

## Work Completed

*What did you accomplish this period?*

### Project/Customer 1: *[Name]*

**Context:** *Brief background on what this is about*

**Activities:**
- *Activity 1 - what you did*
- *Activity 2 - what you did*

**Outcomes:**
- *Outcome 1 - what was achieved*
- *Outcome 2 - what was achieved*

**Artifacts:**
- [Document Name](link)
- [Ticket](link)

---

### Project/Customer 2: *[Name]*

**Context:** *Brief background*

**Activities:**
- *Activity 1*
- *Activity 2*

**Outcomes:**
- *Outcome 1*
- *Outcome 2*

**Artifacts:**
- [Link](url)

---

## Blockers & Escalations

*What's stuck or needs help?*

| Blocker | Impact | Owner | Status |
|---------|--------|-------|--------|
| *Description* | *High/Med/Low* | *@name* | *Waiting/Escalated/Resolved* |

---

## Learnings & Insights

*What did you learn that others should know?*

### Technical
- *Learning 1 - e.g., "Discovered that API X has a rate limit of 100/min"*
- *Learning 2*

### Process
- *Learning 1 - e.g., "Customer prefers async updates over meetings"*
- *Learning 2*

### Product
- *Learning 1 - e.g., "Feature Y is most requested by enterprise segment"*
- *Learning 2*

---

## Next Period Focus

*What will you work on next?*

- [ ] *Priority 1 - description*
- [ ] *Priority 2 - description*
- [ ] *Priority 3 - description*

---

## Metrics (Optional)

| Metric | This Period | Previous | Trend |
|--------|-------------|----------|-------|
| *Tickets closed* | *X* | *Y* | *↑↓* |
| *Customer calls* | *X* | *Y* | *↑↓* |
| *Docs created* | *X* | *Y* | *↑↓* |

---

## References

| Type | Link |
|------|------|
| Related tickets | *Links* |
| Documents created | *Links* |
| Meeting recordings | *Links* |

---

## 📋 Process Reminder

### Worklog Best Practices
1. **Write in third person** - "Thiago worked on..." not "I worked on..."
2. **Focus on outcomes** - not just activities
3. **Include artifacts** - link to everything you created
4. **Capture learnings** - knowledge is valuable
5. **Be honest about blockers** - visibility enables help

---

*Template v1.0 | TSA Ticket Management System | [Full Guide](https://coda.io/d/Solutions-Central_djfymaxsTtA/Linear-Ticket-Management_sukx4jIV)*`
  },
  {
    title: '[TEMPLATE] 🛠️ Implementation - Feature Build',
    description: `## 🎯 How to Use This Template

*This is a reference template for implementation/development tickets.*
*Use this when building features that require detailed specs and phases.*
*Delete all italic guidance text before submitting.*

---

## Overview

*What are we building and WHY?*
*Include business context and link to original request/PRD.*

**Example:**
> Implement bulk export functionality for Reports module. This enables enterprise customers to export 100+ reports at once for compliance audits, which is blocking a $200k expansion deal.
> PRD: [Link](url) | Request: [TICKET-123](link)

---

## Objective

| Field | Value |
|-------|-------|
| **Goal** | *One sentence describing success* |
| **User Story** | *As a [user], I want [action] so that [benefit]* |
| **Success Metric** | *How we measure success* |
| **Owner** | *@engineer* |
| **TSA** | *@tsa* |

---

## Requirements

### Functional Requirements

*What the system must DO*

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | *System shall allow selection of multiple reports* | Must |
| FR-2 | *System shall export in CSV and PDF formats* | Must |
| FR-3 | *System shall show progress indicator* | Should |
| FR-4 | *System shall email when export complete* | Could |

### Non-Functional Requirements

*How the system must PERFORM*

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Performance | *Export 100 reports in <60s* |
| NFR-2 | Scalability | *Handle 1000 concurrent exports* |
| NFR-3 | Security | *Respect user permissions* |
| NFR-4 | Availability | *99.9% uptime* |

---

## Technical Design

### Architecture

*High-level design - how components interact*

\`\`\`
*ASCII diagram or link to design doc*

[UI] → [Export Service] → [Queue] → [Worker] → [Storage]
                                         ↓
                                   [Notification]
\`\`\`

### API Design

*New or modified endpoints*

\`\`\`
POST /api/v1/reports/export
{
  "report_ids": ["id1", "id2"],
  "format": "csv" | "pdf"
}

Response: { "job_id": "xxx", "status_url": "/api/v1/jobs/xxx" }
\`\`\`

### Database Changes

*New tables, columns, or migrations*

| Change | Description |
|--------|-------------|
| *New table: export_jobs* | *Tracks export job status* |
| *New column: reports.export_count* | *Analytics tracking* |

### Dependencies

*What this depends on / what depends on this*

- **Depends on:** *Queue service, Storage service*
- **Blocked by:** *TICKET-100 must be complete first*
- **Blocks:** *TICKET-200 waiting for this*

---

## Implementation Phases

*Break down into deliverable chunks*

### Phase 1: Backend Foundation
**Target:** *2024-01-20*

- [ ] Create export_jobs table and model
- [ ] Implement export service
- [ ] Add queue integration
- [ ] Unit tests

**PR:** *[Link when ready]*

### Phase 2: Worker & Processing
**Target:** *2024-01-25*

- [ ] Implement export worker
- [ ] CSV generation logic
- [ ] PDF generation logic
- [ ] Integration tests

**PR:** *[Link when ready]*

### Phase 3: UI & Polish
**Target:** *2024-01-30*

- [ ] Selection UI component
- [ ] Progress indicator
- [ ] Error handling
- [ ] E2E tests

**PR:** *[Link when ready]*

---

## Testing Strategy

### Unit Tests
- [ ] Export service methods
- [ ] Worker processing logic
- [ ] Format converters

### Integration Tests
- [ ] API endpoint behavior
- [ ] Queue processing
- [ ] Storage integration

### E2E Tests
- [ ] Full export flow
- [ ] Error scenarios
- [ ] Performance under load

---

## Acceptance Criteria

*Definition of Done - how we verify completion*

- [ ] User can select multiple reports (up to 100)
- [ ] Export starts within 5 seconds of request
- [ ] Progress is visible during export
- [ ] Completed export is downloadable for 24 hours
- [ ] Email notification sent on completion
- [ ] Errors are logged and user-friendly message shown
- [ ] All tests passing (unit, integration, E2E)
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Deployed to production

---

## Rollout Plan

| Stage | Date | Scope | Rollback |
|-------|------|-------|----------|
| Staging | *2024-01-28* | Internal testing | *Delete jobs table* |
| Beta | *2024-02-01* | 3 customers | *Feature flag off* |
| GA | *2024-02-05* | All customers | *Feature flag off* |

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| *Large exports timeout* | Medium | High | *Implement chunking* |
| *Storage costs increase* | Low | Medium | *Auto-delete after 24h* |
| *Queue overwhelmed* | Low | High | *Rate limiting* |

---

## References

| Type | Link |
|------|------|
| PRD | *Product requirements doc* |
| Design doc | *Technical design* |
| Figma | *UI mockups* |
| Related tickets | *Dependencies* |

---

## 📋 Process Reminder (TSA Ticket Lifecycle)

### Before Starting Implementation
1. ✅ Requirements clear and approved?
2. ✅ Design reviewed by team?
3. ✅ Dependencies identified and unblocked?
4. ✅ Testing strategy defined?

### During Implementation
1. **Update ticket daily** - show progress
2. **Raise blockers early** - don't wait
3. **Write tests as you go** - not at the end
4. **Keep PRs small** - easier to review

### After Implementation
1. **Demo to stakeholders** - get feedback
2. **Monitor post-deploy** - watch for issues
3. **Document learnings** - help future you

---

*Template v1.0 | TSA Ticket Management System | [Full Guide](https://coda.io/d/Solutions-Central_djfymaxsTtA/Linear-Ticket-Management_sukx4jIV)*`
  }
];

async function createTicket(template, index) {
  return new Promise((resolve, reject) => {
    const query = `
      mutation CreateIssue($input: IssueCreateInput!) {
        issueCreate(input: $input) {
          success
          issue {
            id
            identifier
            url
            title
          }
        }
      }
    `;

    const variables = {
      input: {
        teamId: TEAM_ID,
        title: template.title,
        description: template.description,
        priority: 0
      }
    };

    const postData = JSON.stringify({ query, variables });

    const options = {
      hostname: 'api.linear.app',
      port: 443,
      path: '/graphql',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': API_KEY,
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.data && result.data.issueCreate && result.data.issueCreate.success) {
            resolve({
              success: true,
              index: index + 1,
              id: result.data.issueCreate.issue.identifier,
              url: result.data.issueCreate.issue.url,
              title: result.data.issueCreate.issue.title
            });
          } else {
            resolve({
              success: false,
              index: index + 1,
              title: template.title,
              error: JSON.stringify(result.errors || result)
            });
          }
        } catch (e) {
          resolve({
            success: false,
            index: index + 1,
            title: template.title,
            error: e.message
          });
        }
      });
    });

    req.on('error', (e) => {
      resolve({
        success: false,
        index: index + 1,
        title: template.title,
        error: e.message
      });
    });

    req.write(postData);
    req.end();
  });
}

async function main() {
  console.log('🚀 Creating 11 templates in Linear (RAC - Raccoons)...\n');

  const results = [];

  for (let i = 0; i < templates.length; i++) {
    console.log(`Creating ${i + 1}/11: ${templates[i].title.substring(0, 50)}...`);
    const result = await createTicket(templates[i], i);
    results.push(result);

    if (result.success) {
      console.log(`  ✅ ${result.id} - ${result.url}\n`);
    } else {
      console.log(`  ❌ Failed: ${result.error}\n`);
    }

    // Small delay to avoid rate limiting
    await new Promise(r => setTimeout(r, 500));
  }

  console.log('\n========================================');
  console.log('📊 SUMMARY - Templates Created');
  console.log('========================================\n');

  console.log('| # | Template | Linear ID | URL |');
  console.log('|:-:|----------|-----------|-----|');

  results.forEach(r => {
    if (r.success) {
      const shortTitle = r.title.replace('[TEMPLATE] ', '').substring(0, 30);
      console.log(`| ${r.index} | ${shortTitle} | ${r.id} | ${r.url} |`);
    } else {
      console.log(`| ${r.index} | FAILED | - | ${r.error} |`);
    }
  });

  const successCount = results.filter(r => r.success).length;
  console.log(`\n✅ ${successCount}/11 templates created successfully`);
}

main();
