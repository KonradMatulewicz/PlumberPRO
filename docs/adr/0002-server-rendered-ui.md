# ADR-0002: Server-rendered UI with Jinja2 + HTMX + Chart.js
Status: Accepted
## Context
Time budget is the main constraint; no separate front-end build or deployment wanted.
## Decision
Jinja2 templates, HTMX for partial updates (alert actions, copilot answers), Chart.js for charts.
## Consequences
+ one deployable, fast to build, accessible HTML by default. - less rich client interactivity
than a React SPA; acceptable for an operations dashboard.
