# ADR-0001: Modular monolith with Ports & Adapters
Status: Accepted
## Context
Solo developer, 6 days, free-tier hosting with cold starts. Course heuristic: if a monolith is
acceptable and business logic must not depend on the data layer -> Ports & Adapters.
## Decision
One deployable FastAPI service; bounded contexts as packages; in-process event bus between them.
## Consequences
+ simple deployment, one container, reliable demo, easy testing with fakes.
- single scaling unit; mitigated by event seams allowing later extraction (Strangler Fig) of
  detection worker and copilot service behind a message broker (e.g. Redis).
