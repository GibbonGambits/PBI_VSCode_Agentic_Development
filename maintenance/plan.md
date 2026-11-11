# Round 3 plan

This folder holds the template's own working papers: the plan, the coverage file, the feature inventory, the decisions and the sources record. GitHub Copilot does not read this folder when it works on a report; the project instructions say so.

## Aims

1. Cover every native Power BI practice and feature.
2. Copilot builds things itself instead of handing work back to the developer.
3. Copilot can look things up when it is stuck.
4. The same result across time and across projects.

## Work order

| Step | Part | What | Where it lands |
|---|---|---|---|
| 1 | F | One-pass formula scanner, six states, separate rules for DAX and Power Query, hard test formulas | `scripts/formula_scanner.py`, `tests/test_scanner.py`, `scripts/check_project.py` |
| 2 | G | Sources record and its refresh routine | `maintenance/sources.md`, `scripts/refresh_sources.py` |
| 3 | A | Coverage file from the five baselines; guidance, example and check for every soft or missing row | `maintenance/coverage.md`, the skills' reference files, `scripts/check_project.py`, tests |
| 4 | B | Feature inventory; file-format walk; Git sync and deployment pipeline confirmation | `maintenance/feature-inventory.md` |
| 5 | C | Copilot builds it itself: shipped examples and their index, the measures table, moves and renames, Desktop Bridge, modeling server, field list of a published model, a project from nothing, the TODO list | `tests/fixtures/examples/`, new scripts, every file listed in item 17 |
| 6 | D | Look-up skill and script, four sites only | `.github/skills/pbi-lookup/`, `scripts/lookup.py` |
| 7 | E | DAX function index | `.github/skills/pbi-semantic-model/references/dax-functions.md` |
| 8 | F | Improve flow table and checklist-review skill updated for every new code; "one chat per task"; lessons loop not flooded | `scripts/improve.py`, the two skills, README |
| 9 | - | README, notices, evals, template check | root files, `evals/`, `scripts/check_template.py` |
| 10 | - | Two read-only review helpers; fix what they find; pull request | - |

## Rules of the work

- Order of trust: the owner's checklist; Microsoft Learn; Microsoft's own skills, best practice rules and schemas; SQLBI for DAX; `data-goblin/power-bi-agentic-development` (GPL: read only, nothing copied); `github/awesome-copilot`; `Mofaji/Agentic-PBIP-Template` (MIT). A lower source never overrides a higher one.
- Every rule added carries the address of its source and is written in new words. A rule no source supports is not added. A rule that is the owner's own choice is marked "owner's rule".
- New checks only: fail when Microsoft says it breaks something or gives wrong numbers, or the checklist gives a hard number; warn for every other rule; note for a suggestion. No existing check changes level.
- `checklist/checklist.md` and `theme/theme.json` never change.
- Stop and ask only when a source contradicts the checklist, a change would touch the checklist or the theme, or there is a licence problem. Otherwise decide, write it in `decisions.md`, and carry on.

## Where the work stands

See `status.md` in this folder. It is updated at every commit.
