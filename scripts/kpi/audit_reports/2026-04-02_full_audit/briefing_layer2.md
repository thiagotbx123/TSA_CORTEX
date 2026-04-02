# Layer 2 Briefing — Contextual Audit

## Domain Context
KPI tracking system for a 7-person TSA team at TestBox. Measures 3 KPIs:
1. **ETA Accuracy** (KPI1): % of tickets delivered on/before due date
2. **Implementation Velocity** (KPI2): Throughput — tickets done per week
3. **Implementation Reliability** (KPI3): Rework rate — tickets reopened after Done

## Stakeholders
- Thiago (lead, architect), Carlos, Alexandra, Diego, Gabi (Raccoons squad)
- Thais, Yasmim (Opossum squad)
- Data source: Linear (project management), Google Sheets (historical backlog)

## Architecture
Linear pipeline: Fetch → Merge → Normalize → Build HTML → Upload to Drive
System tray app serves dashboard locally + via ngrok tunnel.

## Anti-Anchoring
This context is for orientation. You are expected to find things OUTSIDE this scope. The documentation may be wrong, incomplete, or aspirational. Trust the code over the docs.

## Layer 1 Findings
(Included inline with Layer 2 auditor execution)
