# Sprint plan — 3 sprints x 2 days (compressed schedule)

The course defines sprints as 1-4 weeks; the Capstone requires >= 3 sprints. Because the project
must be delivered in 6 days by a solo developer, sprints are compressed to 2 days each. Every Scrum
event is kept: planning, daily stand-up (async, `standups.md`), review with a recorded demo for
the Product Owner, and retrospective (`sprint-log.md`).

| Sprint | Days | Goal | Stories |
|---|---|---|---|
| 1 | 1-2 | Deployed skeleton that ingests runs, shows pipeline health and raises statistical alerts | US-01..US-06 |
| 2 | 3-4 | Full triage loop: chaos scenario -> alert -> AI explanation with citations -> resolve | US-07..US-12 |
| 3 | 5-6 | Hardening, quality gates, metrics, documentation, final presentation | US-13..US-16 (+ docs, recording) |

## Survival rule
End of Day 4: the full triage loop must work on the **deployed** app. If behind, cut in this order:
US-15 -> Locust part of US-16 -> Playwright reduced to 1 flow -> US-09 UI (keep notebook+metrics)
-> ZAP. Never cut: task board, sprint demo recordings, design & testing doc, README links.

## Day-by-day
- **Day 1:** board + backlog import (`scripts/create_github_issues.py`), sprint 1 planning,
  US-01 (CI + Render + Postgres), US-02, start US-03.
- **Day 2:** US-03, US-04, US-05, US-06. Sprint 1 review, demo recording (3-5 min), retro.
- **Day 3:** Sprint 2 planning. US-07, US-08, US-09 (notebook/script + CI threshold).
- **Day 4:** US-10, US-12, US-11. Sprint 2 review + recording. Triage loop works deployed.
- **Day 5:** Sprint 3 planning. US-13, US-14, US-16; `/docs-sync`; diagrams; cost section.
- **Day 6:** freeze at noon, bugfixes, share repo with `quantic-grader`, rehearse, record final
  presentation (target 17-18 min), upload to Google Drive (anyone with link), submit.
