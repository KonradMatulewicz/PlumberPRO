# Sprint log — planning, reviews, retrospectives
<!-- /sprint-start and /sprint-review write here -->

## Sprint 1 planning

**Dates:** Day 1-2 (2026-10-01 -> 2026-10-02)
**Sprint goal:** Deployed skeleton that ingests runs, shows pipeline health and raises
statistical alerts (US-01..US-06), so the triage loop has a foundation to build on in Sprint 2.

### Stories, subtasks, tests

#### US-01 — Deployed walking skeleton with CI (Must)
AC: CI (lint+bandit+tests) gates `main`; `/health` returns 200 with version + DB status; README
links deployed app, task board, design doc.
- [ ] Add a DB engine/session factory (`app/shared/db.py`) reading `DATABASE_URL`; a `SELECT 1`
  liveness check.
  - Test: `test_health_ok_when_db_reachable` (fake session returns success).
- [ ] Extend `/health` to report `status: "degraded"` (still HTTP 200) when the DB check fails,
  keeping `version`/`env` always present.
  - Test: `test_health_degraded_when_db_unreachable` (fake session raises).
- [ ] Create the Neon (Postgres+pgvector) database and the Render web service from this repo;
  set env vars from `.env.example`; enable "Auto-Deploy after CI checks pass".
  - Test: manual smoke — `curl <deployed-url>/health` returns 200 after deploy.
- [ ] Add a post-deploy smoke step (CI job or documented manual curl) and record the deployed URL.
  - Test: smoke job green in Actions (or documented manual run before each review).
- [ ] Update `README.md` / `design-and-testing.md` TODO links once the app, board and Neon/Render
  are live.

#### US-02 — Ingest a pipeline run (Must)
AC: valid POST `/api/runs` with API key -> 201 + `RunIngested`; duplicate `run_id` -> 409;
missing/invalid key or invalid payload -> 401/422.
- [ ] `app/ingestion/domain.py`: `Run` entity + validation (rows_loaded >= 0, ended_at >=
  started_at) raising a domain `InvalidRun` error.
  - Test: `test_run_rejects_negative_rows`, `test_run_rejects_end_before_start`.
- [ ] `app/ingestion/ports.py` + `repository.py`: `RunRepository` Protocol and SQLAlchemy adapter;
  Alembic migration for `runs` (UNIQUE `run_id`, CHECK constraints).
  - Test (integration, Postgres): insert + unique-constraint violation on duplicate `run_id`.
- [ ] `app/ingestion/service.py`: `ingest_run()` — duplicate check, persist, publish
  `RunIngested` on `app/shared/events.bus`.
  - Test: service publishes exactly once per new run, zero times on duplicate.
- [ ] `app/ingestion/api.py`: `POST /api/runs`, API-key dependency (`settings.ingest_api_key`),
  pydantic request schema; map domain/duplicate/auth errors to 422/409/401.
  - Test (integration): happy path 201; duplicate 409 (row not duplicated); missing key 401;
    negative `rows_loaded` 422.
- [ ] Wire router into `app/main.py`; `make migrate` runs clean on a fresh DB.

#### US-03 — Synthetic platform history (Must)
AC: `make seed --seed 42` deterministic across runs; ~8 pipelines, 30 days, weekend seasonality,
~2% historical failures with resolved incidents.
- [ ] `app/simulator/pipelines.py`: ~8 fictional pipeline configs (name, SLA time, baseline
  rows/duration, weekday/weekend multipliers).
- [ ] `app/simulator/generator.py`: pure functions producing 30 days of runs per pipeline from a
  seeded `random.Random` (no global random state).
  - Test: `test_generator_deterministic_with_fixed_seed` — two runs, same seed, identical output.
  - Test: `test_weekend_volume_lower_than_weekday_baseline`.
- [ ] `app/simulator/seed.py` CLI (`--days`, `--seed`): persists generated runs (reusing the
  ingestion repository, not raw SQL) and marks ~2% as historical FAILURE with a matching
  Resolved alert row for later MTTR baselines (US-14).
  - Test (integration): after seeding, failure rate across all runs is within an expected band
    and every pipeline has 30 rows.
- [ ] Decide and document reseed strategy (truncate-then-reseed vs idempotent upsert) in
  `design-and-testing.md`.

#### US-04 — Pipeline health dashboard (Must)
AC: `/` lists every pipeline with last status, SLA status, open alert count (text+colour);
pipeline page shows 30-day duration/row charts with anomalies highlighted; empty state when no
runs exist.
- [ ] `app/monitoring/read_model.py`: CQRS-lite read query (SQLAlchemy Core) — latest run +
  open-alert count per pipeline.
- [ ] `app/monitoring/api.py` + `dashboard.html`: `GET /` renders the table with a text label next
  to every colour-coded status (accessibility, PRD NFR).
  - Test (integration): seeded DB -> 200 with pipeline names in the response body.
- [ ] `GET /pipelines/{name}` + `pipeline_detail.html`: last-30-days runs, Chart.js duration/rows
  charts, anomalous points marked distinctly.
  - Test (integration): unknown pipeline -> 404; known pipeline -> 200 with chart data present.
- [ ] Empty-state template/copy when `runs` is empty, pointing to `make seed` and `POST /api/runs`.
  - Test (integration): empty DB -> 200 with empty-state copy, not an error page.

#### US-05 — Detect row-volume anomalies (Must)
AC: >=7 historical successful runs and \|z\| >= 3 vs same-weekday baseline -> `AnomalyDetected` +
Open alert with expected/actual, within 5 s; in-band value -> no alert; <7 runs -> abstain (logged).
- [ ] `app/incidents/ports.py`: `Detector` Protocol; `app/incidents/detectors/__init__.py` registry
  list (single registration point, reused by US-06).
- [ ] `app/incidents/detectors/volume_zscore.py`: same-weekday baseline mean/std, abstain under 7
  samples, flag at \|z\| >= 3.
  - Test: abstains with <7 history; flags at \|z\|>=3 with correct expected/actual; no alert
    in-band.
- [ ] `app/incidents/domain.py`: minimal `Alert` aggregate (Open state) + `AlertRaised` event.
- [ ] Subscribe an `incidents` handler to `RunIngested`: load history, run registered detectors,
  persist Open `Alert`, publish `AlertRaised`.
  - Test (integration): POSTing an anomalous run via the API results in an Open alert row in the
    same request (synchronous in-process bus trivially satisfies the "within 5 s" NFR — document
    this rather than writing a timing-based test).

#### US-06 — Detect late, slow, failed and schema-changed runs (Must)
AC: failed run -> FAILURE alert with log excerpt; run ending after SLA -> LATE alert; changed
`schema_hash` vs previous successful run -> SCHEMA_CHANGE alert; detectors are independent
Strategy implementations registered in one place.
- [ ] `detectors/failure.py`: status == FAILED -> FAILURE alert carrying the log excerpt.
- [ ] `detectors/lateness.py`: `ended_at` vs pipeline's configured SLA time-of-day -> LATE alert.
- [ ] `detectors/schema_change.py`: `schema_hash` vs previous successful run for the same
  pipeline -> SCHEMA_CHANGE alert.
- [ ] `detectors/duration_zscore.py`: same pattern as US-05's volume detector (shared z-score
  helper) -> abnormal-duration alert.
- [ ] Register all five detectors in the one place from US-05; confirm a single run can raise more
  than one alert type without detectors interfering with each other.
  - Test: one unit test per detector (incl. negative case: no schema change -> no alert).
  - Test (integration): a run that is both late and schema-changed produces two independent
    alerts.

### Risks to the sprint goal
1. **No Neon/Render accounts yet** — "deployed" is part of US-01's AC. Mitigation: build and test
   against local `docker-compose` Postgres today; Konrad creates the accounts in parallel; if not
   ready by end of Day 2, demo against `localhost` and finish the deploy on Day 3 without letting
   it block Sprint 2 planning.
2. **Cross-context event wiring** (ingestion -> incidents) is the riskiest new mechanism and only
   gets built once, in US-05 — most likely place to lose time on the first attempt.
3. **First-time Alembic + pgvector on Neon** could stall if the extension needs explicit enabling;
   verify early (Day 1) rather than discovering it during US-02/US-03.
4. **Branch protection now requires the `quality` CI check to pass before merge** (set up today).
   Keeps history clean but will block a solo PR if CI is slow/flaky — keep PRs small, one per
   story.
5. `quantic-grader` could not be added as a collaborator yet (GitHub API rejected the invite,
   422) — does not block sprint work, but blocks the "repo shared with grader" rubric item; needs
   manual retry via the GitHub UI.

### Cut order if behind by end of Day 2
1. US-06: ship FAILURE + LATE only; defer SCHEMA_CHANGE and the duration z-score detector to
   Sprint 2 (additive Strategy implementations, safe to slot in later).
2. US-04: single combined duration+rows chart instead of two separate ones; skip anomaly
   highlighting on the chart itself (alerts are still visible in the alert list).
3. US-03: fewer pipelines (5 instead of 8); skip seeding historical resolved-incident detail
   beyond what MTTR needs (full incident corpus for the copilot is Sprint 2's concern, US-10/15).
4. **Never cut:** US-01 CI/health (everything depends on it), US-02 ingest API (blocks US-03,
   US-05, US-06), and at least one end-to-end detector happy path (US-05) — Sprint 2's triage-loop
   demo needs a real Open alert to act on.
