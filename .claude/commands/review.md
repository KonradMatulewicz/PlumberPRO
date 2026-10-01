---
description: Review the current diff like a strict code owner before merging
---
Review the uncommitted changes and the last commit (`git diff`, `git diff HEAD~1`).
Check, in this order, and report findings grouped as BLOCKER / SHOULD / NIT:
1. Acceptance criteria of the referenced story are met and tested.
2. Architecture rules from CLAUDE.md (no domain -> infrastructure imports, events, aggregate root).
3. Security: input validation, untrusted log text sanitised before LLM, no secrets, SQL via ORM.
4. Tests: AAA, negative/edge cases, no flaky time/network dependence (use fakes).
5. Readability: naming, small functions, code smells (bloaters, couplers, dispensables).
Do not modify files; only report.
