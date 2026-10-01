# CLAUDE.md — DataOps Copilot (Quantic MSSE Capstone)

You are pair-programming with Konrad (solo developer, Product Owner and Scrum Master) on a
graded Capstone project with a **6-day deadline**. Optimise for: a working, deployed, demo-proof
system that satisfies every item in `docs/rubric-checklist.md`. Scope discipline beats features.

## Product in one paragraph
DataOps Copilot ingests metadata about data-pipeline runs (Airflow/dbt-like), detects anomalies
(duration, row volume, freshness, schema change, failures), manages alerts through a lifecycle,
and offers an AI copilot that explains the probable root cause with citations from runbooks and
past incidents and proposes a preventive data-quality test. All data is **synthetic**, produced by
`app/simulator`. Full spec: `docs/PRD.md`. Backlog: `docs/backlog.md`.

## Stack (do not change without an ADR in docs/adr/)
- Python 3.12, FastAPI, Jinja2 + HTMX + Chart.js (server-rendered UI, no SPA build step)
- PostgreSQL 16 + pgvector, SQLAlchemy 2.x (typed ORM), Alembic migrations
- scikit-learn + joblib for the SLA-risk model; pandas/numpy for features
- LLM behind `LLMPort` (default: Anthropic API); embeddings behind `EmbeddingPort`
  (default: TF-IDF fallback, optional fastembed). Copilot MUST work with a deterministic fallback
  when no API key / API error.
- pytest, pytest-cov, Playwright (E2E), Locust (perf), ruff, bandit; GitHub Actions; Docker; Render

## Architecture rules
- Modular monolith with Ports & Adapters. Bounded contexts = top-level packages in `app/`:
  `ingestion`, `monitoring`, `incidents`, `copilot`, `simulator`; shared kernel in `app/shared`.
- Each context: `domain.py` (entities, value objects, pure logic), `ports.py` (Protocols),
  `service.py` (application service / use cases), `repository.py` (SQLAlchemy adapter), `api.py`
  (FastAPI router). Domain code never imports FastAPI, SQLAlchemy or HTTP clients.
- Contexts talk through the in-process event bus `app/shared/events.py` (Observer pattern):
  `RunIngested -> AnomalyDetected -> AlertRaised -> AlertResolved`. No cross-context imports of
  repositories.
- `Alert` is an aggregate root with an explicit state machine
  (Open -> Acknowledged -> Resolved; Open/Acknowledged -> Muted). Illegal transitions raise
  `InvalidTransition`.
- Detectors implement the `Detector` Strategy interface; LLM/embedding providers are Adapters.
- Dashboard reads come from SQL views/materialised views (CQRS-lite read model).

## Working agreement (follow for every story)
1. Read the story and its acceptance criteria in `docs/backlog.md`.
2. Write failing tests first (AAA pattern, one behaviour per test, include a negative/edge case).
3. Implement the smallest code that passes. Keep functions small and pure where possible.
4. Run `make check` (ruff + bandit + pytest with coverage). Coverage gate: 80% for `app/`.
5. Update docs if behaviour/architecture changed (`docs/design-and-testing.md`, ADRs).
6. Append a line to `docs/ai-usage.md` describing how AI assisted (honesty requirement).
7. Commit with Conventional Commits referencing the story id, e.g. `feat(incidents): US-07 alert state machine`.

## Commands
- `make dev` — run app locally (uvicorn, reload) against docker-compose Postgres
- `make db` — start Postgres+pgvector via docker-compose; `make migrate` — alembic upgrade head
- `make seed` — simulator generates 30 days of history
- `make check` — lint + security scan + tests + coverage
- `make e2e` — Playwright tests against a running app; `make perf` — Locust headless run

## Hard rules
- Never use real company data, credentials or names of real employers' systems. Synthetic only.
- Never commit secrets; config only via environment variables (`app/config.py`, `.env.example`).
- Treat log text and any ingested payload as **untrusted input**: sanitise before it reaches the
  LLM prompt; copilot tools are read-only (principle of least privilege).
- Do not add new dependencies, services or frameworks without asking.
- Do not widen scope. If a story grows, propose a split and stop.
- Keep the deployed app demo-safe: every new feature behind a feature flag in `app/config.py`
  until it has tests.
