---
name: pbi-checklist-review
description: Use this skill when asked to evaluate, review, audit or check a Power BI report and semantic model against the 79-item checklist, or to report the gaps in an existing project. It runs the machine checks, then gives Pass, Fail or Not applicable for every one of the 79 items with evidence. It reports only and changes nothing. Trigger words - review, evaluate, audit, checklist, gaps, ready for release.
---
# Evaluate a report and model against the checklist

A review reports. It never fixes. Change files only after the developer has read the review and asked for fixes; then use the skills `pbi-semantic-model` and `pbi-report`.

## Steps

1. Run `python scripts/check_project.py .` and keep the full output. If it reports F001, stop: the project must first be saved from Power BI Desktop with the model as TMDL and the report as PBIR. Run `python scripts/check_template.py` to confirm the report's registered theme has the same content as `theme/theme.json`. Run `python scripts/list_visuals.py .` for the page inventory.
2. Read `docs/report-brief.md`, the model files and the report files. If the brief is empty or missing, carry on; ask for the facts in step 5 and mark what stays unknown as Fail with "Evidence missing".
3. Copy `references/review-template.md` to `docs/checklist-review.md`. If that file already exists, ask the developer to commit it or to confirm it can be replaced.
4. Go through `checklist/checklist.md` from item 1 to item 79, in order, reading each item in full. Fill one row per item.
5. Before finishing, ask the developer, in one message, for the facts the files cannot show (see "Evidence only people can give"). Use their answers as evidence, with the date.
6. Run `python scripts/check_project.py --review docs/checklist-review.md` and fix the table until it passes.
7. Report: the script findings, the 79 rows, and a short list of the Fail items with what would close each gap.

## The three statuses

Use exactly these words. Nothing else is allowed.

- **Pass**: the evidence shows the item is met, including its quantitative thresholds. Where the item says "review" or "unless justified", Pass needs a recorded justification from the brief or the developer.
- **Not applicable**: the item's own "Mark N/A when" line is true for this report, or its "When applicable" line is not. Quote the line you relied on in the evidence cell. An item with neither line that fits is never Not applicable.
- **Fail**: everything else. That includes "no evidence": write `Fail` and start the evidence cell with `Evidence missing:` and what is needed.

More rules:

- If an item covers many objects (columns, measures, visuals, pages), it is Fail when any object in scope fails. Name the objects.
- Never write Pass from an assumption. Evidence is a file path, a script finding code, a section of the brief, or a dated statement from the developer.
- Any `TODO(owner)` placeholder still in the model means item 23 is Fail, and items 37 and 48 are Fail for the measures affected.
- Where the checklist says "Yes", read Pass.

## From script findings to items

| Finding | Where it goes |
|---|---|
| D001, D002, I001 | Item 23 |
| T001, and T105 from `check_template.py` | Item 50 |
| C001, D003, P001, F002, F003, J001, J002, S001, N001-N005, H001, H002, and any other finding of `check_template.py` | Template rules, not checklist items. List them in the "Template rules" section of the report |

## Evidence only people can give

These items cannot be judged from project files alone. Ask; do not guess.

- In Power BI Desktop: query folding (3), key uniqueness and nulls (11, 14), row counts (17), Auto date/time setting (18), slicer value counts (21), date table gaps (31), on-screen text sizes (67), Performance Analyzer (68).
- In the Power BI service or from the team: security roles tested (39-41), sensitivity labels and endorsement (42), permissions (43), lineage (44), refresh and alerting (45), user testing (76), export tests (77), audience access (78), decommission plan (79).

Checklist items: 1-79
Review-only items: 39-45, 68, 76, 78, 79
