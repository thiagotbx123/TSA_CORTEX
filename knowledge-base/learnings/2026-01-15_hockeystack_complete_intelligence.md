# HockeyStack Complete Intelligence
> Learning consolidation from full project analysis
> Date: 2026-01-15
> Source: Slack channels, Drive files, SOW analysis

---

## EXECUTIVE SUMMARY

HockeyStack is a B2B Revenue Attribution Platform prospect with SOW signed Dec 2025. POC has been **completed successfully** with Proof of Life achieved. Deal is in final commercial negotiation ($59.5k, 3yr).

---

## PROJECT METADATA

| Field | Value |
|-------|-------|
| **Project** | HockeyStack |
| **Type** | Prospect (SOW Dec 2025) |
| **Status** | POC Complete, Commercial Negotiation |
| **Deal Value** | $59.5k (3yr), $33k buyout |
| **Primary Contact** | James Hong (Solutions Lead) |
| **TestBox Lead** | Josh Hendricks |
| **TSA Assignment** | Alexandra (assigned but not active in Slack) |
| **Squad** | Toucan |
| **Linear Ticket** | TOU-801 |

---

## KEY LEARNINGS

### 1. Integration Architecture

**Learning**: HockeyStack uses S3 DataSync, NOT direct API for data ingestion.

```
TestBox Data Generator → AWS S3 Bucket → HockeyStack DataSync
```

This simplifies implementation but requires:
- Proper S3 bucket structure (separate folders per entity)
- CSV format with specific headers
- HockeyStack-side configuration for each sync type

### 2. POC Success Factors

**What worked**:
- S3 bucket with IAM role authentication
- Separate folders for each data type (companies, users, deals, etc.)
- Dataset aligned with HockeyStack schema

**What didn't work initially**:
- Single folder for all CSVs (sync ignored them)
- Permission issues (sts:AssumeRole blocked)
- Metadata imports (date format issues)

### 3. Stakeholder Mapping

**HockeyStack Decision Makers**:
- Bugra (CEO) - Technical decisions, very hands-on
- Emir (CRO) - Commercial decisions
- James Hong (Solutions Lead) - Champion, ex-People.ai

**TestBox Team**:
- Josh Hendricks - Lead AE/SA, primary contact
- Gabriel Taufer - CE Lead, AWS/S3 setup
- Sam - Sales leadership, relationship with Emir

### 4. Competitive Context

**Critical insight**: Saleo promised similar capability but failed to deliver. HockeyStack has board mandate to 3x in 2026 and is behind schedule.

This creates:
- High urgency from prospect
- Pressure on TestBox to deliver
- Risk of demanding customer behavior

### 5. Product Quality Concerns

TestBox team noted:
- HockeyStack DataSync has many bugs
- Product not well built
- Customer is demanding

This suggests need for:
- Buffer time in estimates
- Clear scope boundaries
- Escalation paths defined

---

## TECHNICAL SPECIFICATIONS

### Data Schema (Confirmed by Bugra)

| Entity | Key Fields | S3 Folder |
|--------|------------|-----------|
| Companies | company_id, domain, industry, revenue | /companies/ |
| Users | user_id, email, role | /users/ |
| Deals | deal_id, amount, stage, close_date | /deals/ |
| Website Actions | identity, event_time, page_url, utm_* | /touchpoints/ |
| Campaigns | campaign_id, name, type | /campaigns/ |
| Ads Metadata | date, campaign_id, spend, clicks | /ads/ |

### Value Stories (10 max per SOW)

**CMO (5)**:
1. Executive Revenue Overview
2. Budget Allocation by Channel
3. Marketing Sourced Forecast
4. Launch Campaign Impact
5. Board Prep (CAC/Coverage)

**Head of Demand Gen (5)**:
6. Daily Pipeline Pulse
7. Paid/Webinar Optimization
8. Channel Path Attribution
9. Lift Report Experiment
10. Next Quarter Planning

### Timeline (SOW)

| Phase | Duration | Status |
|-------|----------|--------|
| Phase 1: Discovery | 1-2 weeks | COMPLETE |
| Phase 2a: Infrastructure | 4-6 weeks | IN PROGRESS |
| Phase 2b: Data Generation | 4-6 weeks | IN PROGRESS |
| Phase 3: Refinement | 2-4 weeks | PENDING |
| Phase 4: Enablement | 1 week | PENDING |

---

## RESOURCES

### Documents

| Document | Location |
|----------|----------|
| SOW | `C:\Users\adm_r\Projects\hockeystack\knowledge-base\SOW_ANALYSIS.md` |
| Deep Master | `C:\Users\adm_r\Projects\hockeystack\knowledge-base\HOCKEYSTACK_DEEP_MASTER_v1.md` |
| Slack Intelligence | `C:\Users\adm_r\Projects\hockeystack\SLACK_INTELLIGENCE.md` |
| Implementation Plan | `C:\Users\adm_r\Projects\hockeystack\IMPLEMENTATION_PLAN.md` |
| Gap Analysis | `C:\Users\adm_r\Projects\hockeystack\GAPS_ANALYSIS.md` |
| Value Stories | `C:\Users\adm_r\Projects\hockeystack\knowledge-base\VALUE_STORIES.md` |
| ERD | `C:\Users\adm_r\Projects\hockeystack\knowledge-base\ERD_ANALYSIS.md` |

### External Links

| Resource | URL |
|----------|-----|
| SOW (Google Doc) | docs.google.com/document/d/1jj5vQ32qBpYPeAQJkNtY9Aocsq019PalZC3RsPaaLzc |
| Dataset Final | docs.google.com/spreadsheets/d/1TRh4s2fM_c4b7sKSQmtoIxr7Sx1rEKOX |
| Schema Oficial | docs.google.com/spreadsheets/d/1DOU8VoKwSxezaS6WZBtL20TPCUh8kmFn |
| Linear Ticket | linear.app/testbox/issue/TOU-801 |
| Value Stories | docs.google.com/spreadsheets/d/1q9jRv9uDptEvUsJZDW14Elz6UgjETiQ |

### Slack Channels

| Channel | ID | Purpose |
|---------|----|---------|
| hockeystack-internal | C0976RLSK7U | TestBox internal discussion |
| external-hockeystack-testbox | C09JP53FKTL | Joint channel with HockeyStack |

### Credentials

- Bitwarden: "HockeyStack TBX integrations" in Sales Demo Users collection
- AWS S3: Configured by Gabriel Taufer

---

## PATTERNS IDENTIFIED

### 1. Champion Pattern
James Hong (ex-People.ai) is internal champion. He:
- Pushes internally with Bugra/Emir
- Provides technical requirements
- Shares customer deployment examples

**Pattern**: Champions from successful companies (People.ai) carry best practices.

### 2. Urgency Pattern
Board mandate + competitor failure = high pressure.
- Saleo failed to deliver
- 3x growth mandate for 2026
- Behind schedule

**Pattern**: Failed competitor creates opportunity but also high expectations.

### 3. Technical Debt Pattern
HockeyStack DataSync had many bugs:
- Permission issues
- Date format issues
- Custom object issues

**Pattern**: Young products (Series A) have technical debt that impacts implementation.

---

## NEXT STEPS

### Immediate (This Week)

1. [ ] Commercial meeting 1/20 @ 1-1:30pm PST (Josh + James)
2. [ ] Confirm deal terms with Bugra/Emir
3. [ ] Prepare for kickoff post-signature

### Post-Signature

1. [ ] TSA assignment confirmation (Alexandra?)
2. [ ] CE handoff from Gabriel
3. [ ] Dashboard configuration from "golden config"
4. [ ] SDK integration testing

---

## ENTITIES TO ADD TO SPINEHUB

### Projects
- `project_hockeystack` - HockeyStack prospect

### People (HockeyStack)
- `person_bugra_hockeystack` - CEO
- `person_emir_hockeystack` - CRO
- `person_james_hong_hockeystack` - Solutions Lead

### People (TestBox)
- `person_josh_hendricks` - Lead AE/SA
- `person_gabriel_taufer` - CE Lead
- `person_alexandra` - TSA

### Channels
- `channel_hockeystack_internal` - C0976RLSK7U
- `channel_hockeystack_external` - C09JP53FKTL

---

*Learning created: 2026-01-15*
*Source: Full project analysis (Slack + Drive + Knowledge Base)*
