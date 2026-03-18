"""Build the historical reference ticket content for Linear."""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from datetime import datetime

TASKS = [
    {"row":1,"linear":"RAC-275","status":"Done","customer":"WFS","focus":"SOW improvement","demand_type":"External(Customer)","date_add":"2026-01-07","eta":"2026-01-22","delivery":"2026-01-22"},
    {"row":2,"linear":"RAC-290","status":"Done","customer":"WFS","focus":"Environment decision (Pro/Cons)","demand_type":"External(Customer)","date_add":"2026-01-12","eta":"2026-01-16","delivery":"2026-01-16"},
    {"row":3,"linear":"RAC-294","status":"Done","customer":"HockeyStack","focus":"Handover to Thiago","demand_type":"Data Gen.","date_add":"2026-01-12","eta":"2026-01-16","delivery":"2026-01-16"},
    {"row":4,"linear":"RAC-288","status":"Done","customer":"QBO","focus":"Onboarding & handover","demand_type":"Routine","date_add":"2026-01-07","eta":"2026-01-08","delivery":"2026-01-08"},
    {"row":5,"linear":"RAC-289","status":"In Progress","customer":"QBO","focus":"Onboarding & handover (hypercare)","demand_type":"Routine","date_add":"2026-07-01","eta":"2026-03-31","delivery":""},
    {"row":6,"linear":"RAC-286","status":"Done","customer":"QBO","focus":"Documentation review","demand_type":"External(Customer)","date_add":"2026-01-12","eta":"2026-01-16","delivery":"2026-01-16"},
    {"row":7,"linear":"RAC-287","status":"Done","customer":"QBO","focus":"Documentation review (features)","demand_type":"External(Customer)","date_add":"2026-01-12","eta":"2026-01-19","delivery":"2026-01-19"},
    {"row":8,"linear":"RAC-291","status":"Done","customer":"WFS","focus":"Environment decision (first draft)","demand_type":"External(Customer)","date_add":"2026-01-07","eta":"2026-01-09","delivery":"2026-01-09"},
    {"row":9,"linear":"RAC-280","status":"Done","customer":"QBO","focus":"Features review (TCO)","demand_type":"External(Customer)","date_add":"2026-01-12","eta":"2026-02-02","delivery":"2026-02-02"},
    {"row":10,"linear":"RAC-281","status":"Canceled","customer":"QBO","focus":"Features review (Construction Sales)","demand_type":"External(Customer)","date_add":"2026-01-12","eta":"2026-02-09","delivery":""},
    {"row":11,"linear":"RAC-282","status":"Canceled","customer":"QBO","focus":"Features review (Construction Events)","demand_type":"External(Customer)","date_add":"2026-01-12","eta":"2026-02-16","delivery":""},
    {"row":12,"linear":"RAC-276","status":"Done","customer":"WFS","focus":"SOW draft","demand_type":"External(Customer)","date_add":"2026-01-19","eta":"2026-01-22","delivery":"2026-01-22"},
    {"row":13,"linear":"RAC-283","status":"Done","customer":"QBO","focus":"Doc prep (features list for Intuit)","demand_type":"External(Customer)","date_add":"2026-01-19","eta":"2026-01-21","delivery":"2026-01-21"},
    {"row":14,"linear":"RAC-284","status":"Done","customer":"QBO","focus":"Doc prep (IES rerun validation)","demand_type":"External(Customer)","date_add":"2026-01-28","eta":"2026-01-28","delivery":"2026-01-28"},
    {"row":15,"linear":"RAC-297","status":"Done","customer":"QBO","focus":"Support on UAT Environment","demand_type":"External(Customer)","date_add":"2026-01-27","eta":"2026-01-27","delivery":"2026-01-27"},
    {"row":16,"linear":"RAC-269","status":"Done","customer":"QBO","focus":"Ticket analysis PLA-3201","demand_type":"External(Customer)","date_add":"2026-01-22","eta":"2026-01-22","delivery":"2026-01-22"},
    {"row":17,"linear":"RAC-270","status":"Done","customer":"QBO","focus":"Ticket analysis PLA-3202","demand_type":"External(Customer)","date_add":"2026-01-23","eta":"2026-01-23","delivery":"2026-01-23"},
    {"row":18,"linear":"RAC-271","status":"Done","customer":"QBO","focus":"Ticket analysis PLA-3224","demand_type":"External(Customer)","date_add":"2026-01-26","eta":"2026-01-26","delivery":"2026-01-26"},
    {"row":19,"linear":"RAC-272","status":"Done","customer":"QBO","focus":"Ticket analysis PLA-3227","demand_type":"External(Customer)","date_add":"2026-01-27","eta":"2026-01-28","delivery":"2026-01-28"},
    {"row":20,"linear":"RAC-295","status":"Done","customer":"QBO","focus":"Intuit Winter Release docs review","demand_type":"External(Customer)","date_add":"2026-01-28","eta":"2026-01-30","delivery":"2026-01-30"},
    {"row":21,"linear":"RAC-277","status":"Paused","customer":"WFS","focus":"SOW improvement (scope lock)","demand_type":"External(Customer)","date_add":"2026-01-28","eta":"TBD","delivery":""},
    {"row":22,"linear":"RAC-278","status":"Paused","customer":"WFS","focus":"SOW milestones draft","demand_type":"External(Customer)","date_add":"2026-02-04","eta":"TBD","delivery":""},
    {"row":23,"linear":"RAC-285","status":"Done","customer":"QBO","focus":"Doc prep (FY26 tracker update)","demand_type":"External(Customer)","date_add":"2026-02-04","eta":"2026-02-13","delivery":"2026-02-13"},
    {"row":24,"linear":"RAC-264","status":"Done","customer":"QBO","focus":"Env prep (UAT delivery)","demand_type":"External(Customer)","date_add":"2026-02-02","eta":"2026-02-10","delivery":"2026-02-10"},
    {"row":25,"linear":"RAC-265","status":"Done","customer":"QBO","focus":"Env prep (TestBook)","demand_type":"External(Customer)","date_add":"2026-02-02","eta":"2026-02-04","delivery":"2026-02-04"},
    {"row":26,"linear":"RAC-266","status":"Done","customer":"QBO","focus":"Env prep (TestBook run + evidence)","demand_type":"External(Customer)","date_add":"2026-02-02","eta":"2026-02-05","delivery":"2026-02-05"},
    {"row":27,"linear":"RAC-273","status":"Done","customer":"QBO","focus":"Ticket analysis KLA-2399","demand_type":"External(Customer)","date_add":"2026-01-27","eta":"2026-01-28","delivery":"2026-01-28"},
    {"row":28,"linear":"RAC-279","status":"Done","customer":"WFS","focus":"SOW improvement (internal review)","demand_type":"External(Customer)","date_add":"2026-01-30","eta":"2026-02-03","delivery":"2026-02-03"},
    {"row":29,"linear":"RAC-267","status":"Done","customer":"QBO","focus":"Env prep (data ingestion UAT/Sales)","demand_type":"External(Customer)","date_add":"2026-02-05","eta":"2026-02-10","delivery":"2026-02-10"},
    {"row":30,"linear":"RAC-268","status":"Done","customer":"QBO","focus":"Env prep (TestBook rerun UAT)","demand_type":"External(Customer)","date_add":"2026-02-10","eta":"2026-02-12","delivery":"2026-02-12"},
    {"row":31,"linear":"RAC-238","status":"Done","customer":"QBO","focus":"WR: Review ingestion tickets","demand_type":"External(Customer)","date_add":"2026-02-10","eta":"2026-02-12","delivery":"2026-02-12"},
    {"row":32,"linear":"RAC-239","status":"Done","customer":"QBO","focus":"WR: Action plan","demand_type":"External(Customer)","date_add":"2026-02-10","eta":"2026-02-11","delivery":"2026-02-11"},
    {"row":33,"linear":"RAC-240","status":"Done","customer":"QBO","focus":"WR: IES Construction validation","demand_type":"External(Customer)","date_add":"2026-02-12","eta":"2026-02-19","delivery":"2026-02-19"},
    {"row":34,"linear":"RAC-241","status":"Done","customer":"QBO","focus":"WR: Evidence Construction UAT","demand_type":"External(Customer)","date_add":"2026-02-12","eta":"2026-02-19","delivery":"2026-02-19"},
    {"row":35,"linear":"RAC-242","status":"Done","customer":"QBO","focus":"WR: Evidence Construction Events","demand_type":"External(Customer)","date_add":"2026-02-12","eta":"2026-02-19","delivery":"2026-02-19"},
    {"row":36,"linear":"RAC-243","status":"Done","customer":"QBO","focus":"WR: Evidence Construction Sales","demand_type":"External(Customer)","date_add":"2026-02-12","eta":"2026-02-19","delivery":"2026-02-19"},
    {"row":37,"linear":"RAC-244","status":"Done","customer":"QBO","focus":"WR: Validate IES + daily updates","demand_type":"External(Customer)","date_add":"2026-02-10","eta":"2026-02-23","delivery":"2026-02-23"},
    {"row":38,"linear":"RAC-245","status":"Done","customer":"QBO","focus":"WR: Answer Intuit tracker comments","demand_type":"External(Customer)","date_add":"2026-02-17","eta":"2026-02-19","delivery":"2026-02-19"},
    {"row":39,"linear":"RAC-246","status":"Done","customer":"QBO","focus":"WR: Answer Intuit Slack comments","demand_type":"External(Customer)","date_add":"2026-02-17","eta":"2026-02-19","delivery":"2026-02-23"},
    {"row":40,"linear":"RAC-247","status":"Done","customer":"QBO","focus":"WR: Close gaps all environments","demand_type":"External(Customer)","date_add":"2026-02-17","eta":"2026-02-23","delivery":"2026-02-24"},
    {"row":41,"linear":"RAC-248","status":"In Progress","customer":"QBO","focus":"WR: Backlog tickets review","demand_type":"External(Customer)","date_add":"2026-03-09","eta":"2026-03-31","delivery":""},
    {"row":42,"linear":"RAC-249","status":"Done","customer":"QBO","focus":"WR: Evidence TCO","demand_type":"External(Customer)","date_add":"2026-03-02","eta":"2026-03-09","delivery":"2026-03-09"},
    {"row":43,"linear":"RAC-250","status":"Done","customer":"QBO","focus":"WR: Evidence Professional Services","demand_type":"External(Customer)","date_add":"2026-03-02","eta":"2026-03-09","delivery":"2026-03-09"},
    {"row":44,"linear":"RAC-251","status":"Done","customer":"QBO","focus":"WR: Evidence QBOA","demand_type":"External(Customer)","date_add":"2026-03-02","eta":"2026-03-13","delivery":""},
    {"row":45,"linear":"RAC-252","status":"Done","customer":"QBO","focus":"WR: Evidence Events","demand_type":"External(Customer)","date_add":"2026-03-02","eta":"2026-03-09","delivery":"2026-03-09"},
    {"row":46,"linear":"RAC-253","status":"Done","customer":"QBO","focus":"WR: Evidence Non Profit","demand_type":"External(Customer)","date_add":"2026-03-02","eta":"2026-03-13","delivery":""},
    {"row":47,"linear":"RAC-254","status":"Done","customer":"QBO","focus":"WR: Validate TCO","demand_type":"External(Customer)","date_add":"2026-03-02","eta":"2026-03-09","delivery":"2026-03-09"},
    {"row":48,"linear":"RAC-255","status":"Done","customer":"QBO","focus":"WR: Validate Prof. Services","demand_type":"External(Customer)","date_add":"2026-03-02","eta":"2026-03-13","delivery":""},
    {"row":49,"linear":"RAC-256","status":"Done","customer":"QBO","focus":"WR: Validate QBOA","demand_type":"External(Customer)","date_add":"2026-03-02","eta":"2026-03-13","delivery":""},
    {"row":50,"linear":"RAC-257","status":"Done","customer":"QBO","focus":"WR: Validate Events","demand_type":"External(Customer)","date_add":"2026-03-02","eta":"2026-03-09","delivery":"2026-03-09"},
    {"row":51,"linear":"RAC-258","status":"Done","customer":"QBO","focus":"WR: Evidence Manufacturing","demand_type":"External(Customer)","date_add":"2026-03-02","eta":"2026-03-13","delivery":""},
    {"row":52,"linear":"RAC-259","status":"Done","customer":"QBO","focus":"WR: Validate Manufacturing","demand_type":"External(Customer)","date_add":"2026-03-02","eta":"2026-03-13","delivery":""},
    {"row":53,"linear":"RAC-260","status":"Done","customer":"QBO","focus":"WR: Validate Non Profit","demand_type":"External(Customer)","date_add":"2026-03-02","eta":"2026-03-09","delivery":""},
    {"row":54,"linear":"RAC-296","status":"In Progress","customer":"QBO","focus":"Playbook Preparation","demand_type":"Improvement","date_add":"2026-03-04","eta":"2026-03-20","delivery":""},
    {"row":55,"linear":"RAC-292","status":"Done","customer":"WFS","focus":"Pre scoping (questions)","demand_type":"External(Customer)","date_add":"2026-03-03","eta":"2026-03-04","delivery":"2026-03-04"},
    {"row":56,"linear":"RAC-261","status":"Done","customer":"QBO","focus":"WR: Action plan remaining envs","demand_type":"External(Customer)","date_add":"2026-03-03","eta":"2026-03-04","delivery":"2026-03-04"},
    {"row":57,"linear":"RAC-274","status":"Done","customer":"QBO","focus":"Ticket analysis PLA-3308","demand_type":"Maintenance","date_add":"2026-02-25","eta":"2026-02-26","delivery":"2026-02-26"},
    {"row":58,"linear":"RAC-262","status":"Done","customer":"QBO","focus":"WR: End-to-end support","demand_type":"External(Customer)","date_add":"2026-02-01","eta":"2026-03-11","delivery":""},
    {"row":59,"linear":"RAC-298","status":"In Progress","customer":"QBO","focus":"Environment improvements & risk reduction","demand_type":"External(Customer)","date_add":"2026-03-11","eta":"TBD","delivery":""},
    {"row":60,"linear":"RAC-263","status":"In Progress","customer":"QBO","focus":"WR: Lessons learned","demand_type":"External(Customer)","date_add":"2026-03-11","eta":"2026-03-27","delivery":""},
    {"row":61,"linear":"RAC-293","status":"In Progress","customer":"WFS","focus":"Pre scoping (next steps)","demand_type":"External(Customer)","date_add":"2026-03-11","eta":"2026-03-17","delivery":""},
]

# Calculate KPIs
on_time = 0
late = 0
total_deliverable = 0
total_delta = 0
within_1_week = 0
durations = []

for t in TASKS:
    if t['eta'] and t['delivery'] and t['eta'] != 'TBD' and t['delivery']:
        try:
            eta_d = datetime.strptime(t['eta'][:10], '%Y-%m-%d')
            del_d = datetime.strptime(t['delivery'][:10], '%Y-%m-%d')
            d = (del_d - eta_d).days
            total_deliverable += 1
            total_delta += abs(d)
            if d <= 0:
                on_time += 1
            else:
                late += 1
            if abs(d) <= 7:
                within_1_week += 1
        except:
            pass
    if t['date_add'] and t['delivery'] and t['delivery']:
        try:
            add_d = datetime.strptime(t['date_add'][:10], '%Y-%m-%d')
            del_d = datetime.strptime(t['delivery'][:10], '%Y-%m-%d')
            durations.append((del_d - add_d).days)
        except:
            pass

# Build description
desc = []
desc.append('# TSA Historical Data — Alexandra Lacerda')
desc.append('')
desc.append('> **Purpose:** This ticket preserves the original dates and KPI-critical fields from the TSA Tasks Consolidate spreadsheet (Jan-Mar 2026). Linear migration happened on 2026-03-17, so `createdAt` and `completedAt` on migrated issues reflect the migration date, NOT original dates. Use THIS ticket as the authoritative source for historical KPI calculations.')
desc.append('')
desc.append('---')
desc.append('')
desc.append('## KPI Snapshot (Jan 7 — Mar 17, 2026)')
desc.append('')
desc.append(f'| Metric | Value |')
desc.append(f'|--------|-------|')
desc.append(f'| Total tasks | {len(TASKS)} |')
desc.append(f'| Done | {sum(1 for t in TASKS if t["status"]=="Done")} |')
desc.append(f'| In Progress | {sum(1 for t in TASKS if t["status"]=="In Progress")} |')
desc.append(f'| Canceled | {sum(1 for t in TASKS if t["status"]=="Canceled")} |')
desc.append(f'| Paused (BBC) | {sum(1 for t in TASKS if t["status"]=="Paused")} |')
desc.append(f'| Tasks with ETA+Delivery | {total_deliverable} |')
if total_deliverable:
    desc.append(f'| **On-time rate** | **{100*on_time/total_deliverable:.1f}%** ({on_time}/{total_deliverable}) |')
    desc.append(f'| Late deliveries | {late} |')
    desc.append(f'| Avg absolute delta | {total_delta/total_deliverable:.1f} days |')
    desc.append(f'| **Within 1 week (Waki target >90%)** | **{100*within_1_week/total_deliverable:.1f}%** ({within_1_week}/{total_deliverable}) |')
if durations:
    desc.append(f'| Avg duration (Date Add → Delivery) | {sum(durations)/len(durations):.1f} days |')
    desc.append(f'| Median duration | {sorted(durations)[len(durations)//2]} days |')
    desc.append(f'| Max duration | {max(durations)} days |')

desc.append('')
desc.append('### Waki KPI Assessment')
desc.append('')
desc.append(f'1. **ETA Accuracy (<1 week, >90%):** {100*within_1_week/total_deliverable:.1f}% of delivered tasks within 1 week of ETA')
desc.append(f'2. **Faster Implementations (4-week target):** Avg {sum(durations)/len(durations):.1f} days, median {sorted(durations)[len(durations)//2]} days')
desc.append(f'3. **Implementation Reliability (90%):** {100*on_time/total_deliverable:.1f}% on-time delivery rate')
desc.append('')
desc.append('---')
desc.append('')
desc.append('## Customer Breakdown')
desc.append('')
from collections import Counter
cust = Counter(t['customer'] for t in TASKS)
for c, n in cust.most_common():
    done = sum(1 for t in TASKS if t['customer']==c and t['status']=='Done')
    desc.append(f'- **{c}**: {n} tasks ({done} done)')
desc.append('')
desc.append('## Demand Type Breakdown')
desc.append('')
dt = Counter(t['demand_type'] for t in TASKS)
for d, n in dt.most_common():
    desc.append(f'- **{d}**: {n}')

desc.append('')
desc.append('---')
desc.append('')
desc.append('## Full Historical Record')
desc.append('')
desc.append('| # | Linear | Customer | Focus | Status | Date Add | ETA | Delivery | Delta |')
desc.append('|---|--------|----------|-------|--------|----------|-----|----------|-------|')
for t in TASKS:
    delta = ''
    if t['eta'] and t['delivery'] and t['eta'] != 'TBD' and t['delivery']:
        try:
            eta_d = datetime.strptime(t['eta'][:10], '%Y-%m-%d')
            del_d = datetime.strptime(t['delivery'][:10], '%Y-%m-%d')
            delta = str((del_d - eta_d).days)
        except:
            pass
    desc.append(f"| {t['row']} | {t['linear']} | {t['customer']} | {t['focus'][:35]} | {t['status']} | {t['date_add']} | {t['eta']} | {t['delivery'] or '-'} | {delta} |")

desc.append('')
desc.append('---')
desc.append('')
desc.append('*Generated by TSA_CORTEX migration script on 2026-03-17. Source: TSA_Tasks_Consolidate spreadsheet, ALEXANDRA tab.*')

content = '\n'.join(desc)
print(content)
print()
print('=== LENGTH ===')
print(f'{len(content)} chars')

# Also print the KPI summary for the user
print()
print('=== KPI SUMMARY FOR USER ===')
print(f'On-time rate: {100*on_time/total_deliverable:.1f}%')
print(f'Within 1 week: {100*within_1_week/total_deliverable:.1f}%')
print(f'Avg duration: {sum(durations)/len(durations):.1f} days')
print(f'Median duration: {sorted(durations)[len(durations)//2]} days')

# Save to file for the API call
with open('_history_ticket_body.md', 'w', encoding='utf-8') as f:
    f.write(content)
print('\nSaved to _history_ticket_body.md')
