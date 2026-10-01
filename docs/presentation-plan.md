# Final presentation plan (target 17-18 min)

| Time | Segment | Content |
|---|---|---|
| 0:00-1:00 | Intro | Name, show government ID to camera, one-sentence product pitch |
| 1:00-2:30 | Problem & users | Personas, pain points, product vision, scope |
| 2:30-11:30 | Live demo (deployed) | Story by story, see script below |
| 11:30-14:00 | Architecture | contexts, Ports & Adapters, events, Alert state machine, patterns, data model |
| 14:00-16:00 | Quality | CI pipeline run, test inventory & coverage, ML metrics, RAG hit rate, ZAP, Locust |
| 16:00-17:00 | Process | board, 3 sprints, demos, retros, AI-assisted development |
| 17:00-18:00 | Wrap-up | deployment options & cost, lessons, future work |

## Demo script (inputs chosen to show positive, negative and edge cases)
1. Login (wrong password once -> error message; then success) — US-13
2. Dashboard: healthy platform, SLA statuses, open the `orders_daily` charts — US-04
3. Chaos: **normal run** -> no alert (negative case) — US-08, US-05
4. Chaos: **volume drop 60%** -> volume alert with expected vs actual — US-05
5. Chaos: **schema change** and **late run** -> alerts — US-06
6. Explain the volume alert -> cause, evidence, citations; open a cited runbook — US-10
7. Suggest preventive test -> dbt test YAML, copy — US-11
8. Chaos: **failure with prompt-injection log** -> copilot flags suspicious content, ignores it — US-12
9. Acknowledge -> resolve with note; try illegal action on resolved alert (rejected) — US-07
10. Metrics page: MTTR updated, SLA compliance; pipeline risk score — US-14, US-09
11. API: POST invalid payload / wrong key -> 422/401 (Swagger UI) — US-02

## Recording checklist
Warm up the Render instance 5 min before; reset + seed demo DB; close notifications;
1080p; mic test; record in one take or edit into ONE .mp4; check length; upload and test link
in incognito.
