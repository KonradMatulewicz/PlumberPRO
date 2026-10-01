---
description: Implement one user story test-first, following CLAUDE.md working agreement
argument-hint: <story id, e.g. US-04>
---
Implement story $ARGUMENTS.

1. Read the story and acceptance criteria in `docs/backlog.md`. Restate them as a checklist.
2. Show me a short plan (files to touch, tests to add) and wait for my "go".
3. Write failing tests first (unit; integration if it touches the DB or HTTP). Use AAA.
   Cover at least one positive, one negative and one edge case.
4. Implement until `make check` passes. Respect the architecture rules in CLAUDE.md.
5. Update `docs/design-and-testing.md` if a pattern, decision or test type was added.
6. Append one line to `docs/ai-usage.md`: date, story, what you (AI) did, what I reviewed.
7. Propose a Conventional Commit message referencing $ARGUMENTS. Do not push.
