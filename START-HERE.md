# Start here (Day 1 checklist)

1. Create an empty GitHub repo `dataops-copilot`, copy these files in, first commit, push.
   Replace `@CHANGE_ME_GITHUB_USERNAME` in `.github/CODEOWNERS`.
2. Protect `main` (require PR + passing CI). Add collaborator `quantic-grader` (read access).
3. `gh auth login`, then `python scripts/create_github_issues.py` → 16 issues with labels.
   Create a GitHub Project (board), add the issues, columns Backlog / Sprint / In progress /
   Review / Done. Put the board URL in README.
4. Create free Postgres with pgvector (e.g. Neon) and a Render web service from the repo
   (Docker). Set env vars from `.env.example`. Put the URL in README.
5. Open the repo in Claude Code and run:
   - `/sprint-start 1`  → sprint goal, subtasks, risks in docs/sprint-log.md
   - `/story US-01`     → implement test-first; then `/review` (or ask the code-reviewer agent)
   - `/standup` every morning, `/sprint-review 1` at the end of Day 2, then record the demo.
6. Use the `qa-engineer` agent for test design and `/docs-sync` on Day 5.
