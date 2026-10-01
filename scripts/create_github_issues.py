"""Create GitHub labels and one issue per user story from docs/backlog.md.

Usage:  python scripts/create_github_issues.py --dry-run
        python scripts/create_github_issues.py            # needs `gh auth login` in the repo
Then add the issues to a GitHub Project (board) with columns Backlog / Sprint / In progress /
Review / Done, and a "Sprint" field (1-3).
"""

import argparse
import re
import subprocess  # nosec B404 - calls the trusted GitHub CLI with argument lists
from pathlib import Path

BACKLOG = Path(__file__).resolve().parents[1] / "docs" / "backlog.md"
HEADER = re.compile(r"^### (US-\d+) — (.+)$", re.MULTILINE)
META = re.compile(r"\*\*Epic:\*\* (E\d) \| \*\*Sprint:\*\* (\d) \| \*\*Priority:\*\* (\w+)")


def parse_stories(text: str) -> list[dict]:
    stories = []
    matches = list(HEADER.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[m.end():end].strip().split("\n---")[0].strip()
        meta = META.search(body)
        if not meta:
            raise ValueError(f"Missing metadata line for {m.group(1)}")
        epic, sprint, priority = meta.groups()
        stories.append({"id": m.group(1), "title": m.group(2).strip(), "epic": epic,
                        "sprint": sprint, "priority": priority, "body": body})
    return stories


def gh(args: list[str], dry_run: bool) -> None:
    print("gh", " ".join(args[:4]), "...")
    if not dry_run:
        subprocess.run(["gh", *args], check=False)  # nosec B603 B607


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    stories = parse_stories(BACKLOG.read_text(encoding="utf-8"))
    labels = {"user-story"} | {s["epic"] for s in stories} | {f"sprint-{s['sprint']}" for s in stories} \
        | {s["priority"].lower() for s in stories}
    for label in sorted(labels):
        gh(["label", "create", label, "--force"], args.dry_run)
    for s in stories:
        gh(["issue", "create", "--title", f"{s['id']}: {s['title']}", "--body", s["body"],
            "--label", f"user-story,{s['epic']},sprint-{s['sprint']},{s['priority'].lower()}"],
           args.dry_run)
    print(f"{len(stories)} stories processed")


if __name__ == "__main__":
    main()
