---
name: pbi-lessons
description: Use this skill when the developer points out a mistake in your work or corrects it, when a check script fails on something you created or changed, or when asked to improve this template's instructions, skills or scripts. It records the lesson in the lessons file and, when the same mistake comes back, proposes a change to the template that a person approves by pull request. Trigger words - mistake, wrong, not right, correction, lesson, check failed, improve the template.
---
# Learning from mistakes

## When this starts

- **The developer points it out**: they say something you produced is wrong, or they correct it.
- **A check fails**: `scripts/check_project.py`, `scripts/check_template.py` or the tests report an error in something you created or changed in this task. An error that was already in a report before you touched it is a gap for the review, not a lesson.

## Steps

1. Put the mistake right in the report or model, and run the check again.
2. Read `docs/lessons.md`. If an earlier lesson is the same kind of mistake, reuse its key.
3. Record the lesson, one for each kind of mistake in this task, however many places it showed up:
   `python scripts/lessons.py add --trigger developer --key <key> --mistake "<what was wrong>" --correction "<what is right>"`
   Use `--trigger check` when a check failed, with the finding code as the key (for example `D001`). Otherwise the key is a short name in lower-case words joined by hyphens. Write what the developer said or the check reported. Do not guess at causes.
4. If the script reports X003, the mistake has come back and must be built into the template. Work out the proposal, but change nothing yet:
   - A check already catches it (the key is a finding code): propose the one line of guidance that would have prevented it. Do not add or change a check.
   - No check catches it, but it shows in the files: propose a new check in `scripts/check_project.py`, with a test in `tests/test_checks.py` that fails on a broken example and passes on a correct one.
   - A script cannot catch it: propose one line in the file where the rule belongs. A hard rule for model or report files goes in `.github/instructions/`; how-to detail goes in a skill or its reference file; only a rule for every task goes in the project instructions. Prefer correcting an existing line to adding one.
5. Ask the developer. Show the exact change and the file it goes in, and wait for a clear yes.
   - No: record the decision as a new lesson with the same key and `--fix "declined: <reason>"`.
   - Yes: make a new branch from the current one and make the change there. Run `python -m unittest discover -s tests`. The developer opens the pull request and tells you its number or address. Then add a lesson with the same key, `--fix "<file changed>, <second file>"` and `--approved "<pull request number or address>"`, commit it to that branch, and run `python scripts/check_template.py` (until that row is added, X003 is expected). Merging the pull request is the approval. Never merge it yourself.

## Limits

- Never change a template file without asking first (the list is in the project instructions).
- Never change `checklist/checklist.md` or `theme/theme.json` this way, nor the two hashes that guard them in `scripts/check_template.py`. If a lesson seems to call for it, tell the developer and stop.
- Never loosen or remove a check, or soften an existing rule, so that something passes.
- Never edit the business-definitions reference files through a lesson.
- Never edit or delete an earlier lesson.

Checklist items: none
