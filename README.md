# DataOps Copilot

Monitoring, anomaly detection and an AI incident copilot for data pipelines.
Quantic MSSE Capstone (AI system), solo project.

| | |
|---|---|
| Deployed app | TODO https://<app>.onrender.com |
| Task board | TODO GitHub Project URL |
| Design & testing document | [docs/design-and-testing.md](docs/design-and-testing.md) |
| Presentation video | TODO Google Drive link |
| API docs | `<deployed-url>/docs` (OpenAPI/Swagger) |

## What it does
Ingests pipeline-run metadata, detects anomalies (volume, duration, lateness, schema change,
failures) with statistical detectors and an ML SLA-risk model, manages alerts through a
lifecycle, and explains incidents with a RAG copilot that cites runbooks and past incidents and
proposes preventive data-quality tests. All data is synthetic.

## Run locally
```bash
cp .env.example .env
make install
make db && make migrate && make seed
make dev            # http://localhost:8000
make check          # lint + SAST + tests + coverage
```

## Repository map
`app/` bounded contexts (ingestion, monitoring, incidents, copilot, simulator, web) ·
`tests/` unit / integration / e2e / perf · `ml/` model training & metrics ·
`knowledge/` RAG corpus · `docs/` PRD, backlog, ADRs, design & testing, sprint log ·
`.claude/` Claude Code commands and subagents used for AI-assisted development.

## AI-assisted development
Built with Claude Code as a pair programmer; see [docs/ai-usage.md](docs/ai-usage.md).
