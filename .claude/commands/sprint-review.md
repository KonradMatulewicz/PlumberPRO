---
description: Close a sprint - review, retro notes and a script for the sprint demo recording
argument-hint: <sprint number 1-3>
---
Close Sprint $ARGUMENTS.
1. Compare delivered work (git log, tests, `docs/backlog.md`) against the sprint plan in
   `docs/sprint-log.md`. Mark each story Done / Partially / Not done with evidence.
2. Write "Sprint $ARGUMENTS review & retro" in `docs/sprint-log.md`: delivered, metrics
   (tests count, coverage %, deployed URL works?), what went well, what to improve, carry-over.
3. Produce a 3-5 minute demo script for recording the sprint demo for the Product Owner:
   ordered steps on the deployed app, inputs to use (positive, negative, edge), what to say.
