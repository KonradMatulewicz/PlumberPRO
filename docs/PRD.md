# DataOps Copilot — Product Requirements (MVP)

**Product Owner / Scrum Master / Developer:** Konrad Matulewicz (solo)
**Timebox:** 6 days, 3 sprints x 2 days (compressed schedule, see `sprint-plan.md`)
**Type:** AI system (Capstone option a) — ML anomaly/risk models + LLM copilot with RAG

## Problem
Data engineers lose hours triaging data-pipeline incidents. Hard failures are obvious; silent ones
(half the usual rows loaded, a late upstream, a changed schema) reach dashboards before anyone
notices. Alerts are noisy, and the root cause hides in logs and in the memory of whoever fixed a
similar incident last time.

## Vision
Help an on-call data engineer go from "something is wrong" to "I know why and how to prevent it"
in minutes, and let data consumers know whether today's data can be trusted.

## Personas
- **Dana — on-call data engineer (primary).** Wants early, low-noise alerts and a fast root cause.
- **Alex — analytics consumer.** Wants to know whether a dashboard's source data is healthy today.
- **Morgan — data platform lead.** Wants SLA compliance and MTTR trends.

## Scope (MVP)
1. Ingest pipeline-run metadata through a REST API (Airflow/dbt-like payload), API-key protected.
2. Synthetic simulator of a fictional company's data platform (~8 pipelines, 30 days history) and
   a **chaos-scenario panel** that injects incidents on demand (volume drop, late run, schema
   change, failure with log, failure whose log contains a prompt-injection attempt).
3. Dashboard: pipeline health, SLA status, run timeline (duration/rows charts).
4. Anomaly detection: statistical detectors (z-score on duration and row count, freshness,
   schema change) and an ML **SLA-breach risk** model (random forest vs logistic-regression baseline).
5. Alert lifecycle state machine: Open -> Acknowledged -> Resolved, or Muted; full audit trail.
6. Copilot (RAG) over runbooks and resolved incidents: probable root cause with citations,
   similar past incidents, suggested preventive dbt test. Deterministic fallback without LLM.
7. Platform metrics: open alerts, MTTR, SLA compliance; `/health` endpoint.

## Out of scope (documented as future work)
Executing data-quality checks against real warehouses, lineage graph UI, multi-tenant RBAC,
Slack/email notifications, Kubernetes deployment (manifests are a stretch goal), real Airflow.

## Non-functional requirements / SLOs
- Ingest API p95 latency < 300 ms at 20 req/s (Locust).
- Alert created within 5 s of ingesting an anomalous run.
- Copilot answer < 15 s; always returns something (fallback) — never a 500 during demo.
- Unit+integration coverage >= 80% of `app/`.
- Security: SAST (bandit) clean of high severity, OWASP ZAP baseline with no high alerts,
  secrets only via env vars, untrusted log text sanitised before reaching the LLM.
- Accessibility: semantic HTML, keyboard-usable controls, colour not the only status signal.

## Ethics & data
Synthetic data only; no personal data processed. The copilot discloses that answers are AI
generated, cites its sources and never executes changes (read-only tools, least privilege).
