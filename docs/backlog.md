# Product Backlog — DataOps Copilot

Format: user story (INVEST), acceptance criteria (Given/When/Then). Priority uses MoSCoW.
Story ids are referenced in commits (`feat(ctx): US-07 ...`) and GitHub issues.

## Epics
- **E1 Platform & delivery** — repo, CI/CD, deployment, auth, observability
- **E2 Ingestion & simulation** — run ingestion API, synthetic platform, chaos scenarios
- **E3 Monitoring** — dashboard, SLA status, run timeline
- **E4 Detection & alerts** — detectors, ML risk model, alert lifecycle
- **E5 Incident Copilot** — RAG explanations, similar incidents, preventive tests, AI safety

---

### US-01 — Deployed walking skeleton with CI
**Epic:** E1 | **Sprint:** 1 | **Priority:** Must
As the product owner, I need a deployed skeleton with automated checks, so that every later change is tested and shippable.
- Given a push or PR to `main`, when GitHub Actions runs, then lint, bandit and tests run and the PR cannot merge if any fail.
- Given the app is deployed on Render, when I open `/health`, then it returns 200 with app version and DB status.
- Given the repo, when a grader opens README, then it links to the deployed app, task board and design doc.

### US-02 — Ingest a pipeline run
**Epic:** E2 | **Sprint:** 1 | **Priority:** Must
As a data platform, I need to report each pipeline run to DataOps Copilot, so that runs can be monitored.
- Given a valid API key and payload (pipeline, run_id, status, started_at, ended_at, rows_loaded, schema_hash, log_excerpt), when I POST `/api/runs`, then 201 is returned and a `RunIngested` event is published.
- Given a duplicate run_id, when I POST it again, then 409 is returned and nothing is stored twice.
- Given a missing/invalid API key or invalid payload (negative rows, end before start), then 401/422 with a clear error.

### US-03 — Synthetic platform history
**Epic:** E2 | **Sprint:** 1 | **Priority:** Must
As a developer and demo presenter, I need 30 days of realistic run history for ~8 pipelines, so that detectors have a baseline.
- Given `make seed` with a fixed seed, when it runs twice, then it produces identical data (deterministic).
- Given the seeded data, then each pipeline has daily runs with plausible seasonality (weekends lower volume) and ~2% historical failures with resolved incidents.

### US-04 — Pipeline health dashboard
**Epic:** E3 | **Sprint:** 1 | **Priority:** Must
As an analytics consumer, I need to see whether each pipeline is healthy today, so that I know if my dashboards can be trusted.
- Given seeded data, when I open `/`, then I see every pipeline with last run status, SLA status (on time/late/failed) and open alert count, using text + colour.
- Given I click a pipeline, then I see duration and row-count charts for the last 30 days with anomalies highlighted.
- Given no runs exist, then an empty state explains how to seed or ingest data.

### US-05 — Detect row-volume anomalies
**Epic:** E4 | **Sprint:** 1 | **Priority:** Must
As an on-call data engineer, I need an alert when a run loads unusually few or many rows, so that I can stop bad data early.
- Given >= 7 historical successful runs, when a run's row count has |z| >= 3 versus the same weekday baseline, then an `AnomalyDetected` event and an Open alert with expected vs actual values are created within 5 s.
- Given a value inside the normal band, then no alert is created.
- Given fewer than 7 historical runs, then the detector abstains (no alert, reason logged).

### US-06 — Detect late, slow, failed and schema-changed runs
**Epic:** E4 | **Sprint:** 1 | **Priority:** Must
As an on-call data engineer, I need alerts for failures, SLA lateness, abnormal duration and schema changes, so that no incident type goes unnoticed.
- Given a failed run, then an alert of type FAILURE is opened including the log excerpt.
- Given a run ending after the pipeline's SLA time, then a LATE alert is opened.
- Given a schema_hash differing from the previous successful run, then a SCHEMA_CHANGE alert is opened.
- Detectors are independent Strategy implementations registered in one place.

### US-07 — Alert lifecycle
**Epic:** E4 | **Sprint:** 2 | **Priority:** Must
As an on-call data engineer, I need to acknowledge, resolve or mute alerts with a note, so that the team knows who handles what.
- Given an Open alert, when I acknowledge it, then its state is Acknowledged with my name and timestamp.
- Given an Acknowledged alert, when I resolve it with a resolution note, then it is Resolved and MTTR is computed.
- Given a Resolved alert, when I try to acknowledge it, then the action is rejected with an explanation (illegal transition).
- Every transition is stored in an audit trail shown on the alert page.

### US-08 — Chaos scenarios panel
**Epic:** E2 | **Sprint:** 2 | **Priority:** Must
As a demo presenter, I need to inject a realistic incident on demand, so that I can show detection and triage live.
- Given the panel, when I choose a scenario (volume drop, late run, schema change, failure, failure with prompt-injection log, normal run) for a pipeline, then a matching run is ingested through the public API.
- Given "normal run", then no alert is created (negative case visible in the demo).

### US-09 — SLA-breach risk prediction
**Epic:** E4 | **Sprint:** 2 | **Priority:** Should
As a data platform lead, I need a risk score that a pipeline will breach its SLA today, so that we can act before it happens.
- Given the training notebook/script, then a random forest and a logistic-regression baseline are trained on simulator features with a train/test split and no data leakage (scaler fitted on train only); metrics (precision, recall, ROC AUC) are written to `ml/metrics.json`.
- Given CI, then a test fails if recall of the selected model drops below 0.70.
- Given the pipeline page, then the latest risk score and its top contributing features are shown.

### US-10 — Copilot explains an alert with citations
**Epic:** E5 | **Sprint:** 2 | **Priority:** Must
As an on-call data engineer, I need a probable root cause with sources, so that I can fix the incident faster and trust the answer.
- Given an alert, when I click "Explain", then the copilot retrieves the top-k relevant runbook/incident chunks and returns cause, evidence and next steps with citations linking to those sources.
- Given the LLM is unavailable or no API key is set, then a deterministic fallback answer built from the retrieved runbook is returned (no error page).
- Given the retrieval eval set (>= 20 questions), then hit rate@3 >= 0.8 is reported in docs.

### US-11 — Copilot suggests a preventive test
**Epic:** E5 | **Sprint:** 2 | **Priority:** Should
As an on-call data engineer, I need a suggested dbt/SQL data-quality test for the incident, so that it does not happen again.
- Given an explained alert, when I click "Suggest test", then a dbt test YAML or SQL check is shown with a short rationale and a copy button.
- Given the suggestion, then it is clearly marked as AI-generated and is never executed automatically.

### US-12 — Copilot is safe against prompt injection
**Epic:** E5 | **Sprint:** 2 | **Priority:** Must
As a platform owner, I need the copilot to treat log text as untrusted data, so that a malicious log line cannot hijack it.
- Given a failure whose log contains "ignore previous instructions ...", when explained, then the copilot does not follow it, flags "suspicious content in logs", and still answers the original task.
- Given the copilot's tools, then they are read-only (no write/delete capabilities exist).

### US-13 — Access control
**Epic:** E1 | **Sprint:** 3 | **Priority:** Should
As a platform owner, I need the UI protected by login and the ingest API by key, so that only authorised users act on alerts.
- Given I am not logged in, when I open any UI page except login and `/health`, then I am redirected to login.
- Given wrong credentials 5 times, then further attempts are rate-limited for 1 minute.

### US-14 — Platform metrics and health
**Epic:** E1 | **Sprint:** 3 | **Priority:** Should
As a data platform lead, I need open alerts, MTTR and SLA compliance over 7/30 days, so that I can report on reliability.
- Given resolved alerts, then MTTR is the mean time from Open to Resolved and matches a hand-computed test fixture.
- Given the app, then structured JSON logs include request id, route, latency and status.

### US-15 — Similar incidents
**Epic:** E5 | **Sprint:** 3 | **Priority:** Could
As an on-call data engineer, I need to see past incidents similar to the current alert, so that I can reuse known fixes.
- Given an alert, then up to 3 similar resolved incidents are listed with similarity score and resolution note.
- Stretch: incident log messages grouped with k-means (elbow method documented).

### US-16 — Quality gates: E2E, performance, DAST
**Epic:** E1 | **Sprint:** 3 | **Priority:** Should
As the product owner, I need automated end-to-end, performance and security checks, so that the release is trustworthy.
- Given CI, then Playwright runs the main flow (chaos scenario -> alert -> explain -> resolve).
- Given Locust headless run, then ingest p95 < 300 ms at 20 req/s is asserted and the report is stored.
- Given OWASP ZAP baseline against staging/deployed app, then no high-risk findings.
