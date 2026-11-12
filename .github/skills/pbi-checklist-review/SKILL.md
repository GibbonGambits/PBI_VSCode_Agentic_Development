---
name: pbi-checklist-review
description: Use this skill when asked to evaluate, review, audit or check a Power BI report and semantic model against the 79-item checklist, or to report the gaps in an existing project. It runs the machine checks, then gives Pass, Fail or Not applicable for every one of the 79 items with evidence. It reports only and changes nothing. Trigger words - review, evaluate, audit, checklist, gaps, ready for release.
---
# Evaluate a report and model against the checklist

A review reports. It never fixes. Change files only after the developer has read the review and asked for fixes; then use the skills `pbi-semantic-model` and `pbi-report`.

## Steps

1. Run `python scripts/check_project.py .` and keep the full output. If it reports F001, stop: the project must first be saved from Power BI Desktop with the model as TMDL and the report as PBIR. Run `python scripts/check_template.py` to confirm the report's registered theme has the same content as `theme/theme.json`. Run `python scripts/list_visuals.py .` for the page inventory.
2. Read `docs/report-brief.md`, the model files and the report files. If the brief is empty or missing, carry on, and mark what stays unknown as Fail with "Evidence missing".
3. Copy `references/review-template.md` to `docs/checklist-review.md`. If that file already exists: inside the skill `pbi-improve` replace it without asking (that flow keeps the first review); otherwise say at the start that you will replace it, and go on when the developer does not object.
4. Go through `checklist/checklist.md` from item 1 to item 79, in order, reading each item in full. Fill one row per item. A second review of the same project does the same: all 79 items again, never only the rows you expect to have changed.
5. Get the facts the files cannot show (see "Evidence only people can give") without asking during the review. Facts about the data: read them yourself where the developer has set up Microsoft's modeling server (the file data-facts.md of the skill `pbi-semantic-model`), and check whether a local source file is there before you say a fact cannot be had. A fact that the brief or an earlier answer gives is evidence, with its date. Everything else is Fail with "Evidence missing:", and its question goes into your report (step 7). If the server is not set up, or does not answer, say so in the report. Where the Desktop Bridge is agreed, look at the pages yourself for what only the screen shows (the file desktop-bridge.md of the skill `pbi-report`).
6. Run `python scripts/check_project.py --review docs/checklist-review.md` and fix the table until it passes.
7. Report: the script findings, the 79 rows, a short list of the Fail items with what would close each gap, the questions for the facts only a person can give (one list, like questions together), the open `TODO(owner)` questions (`python scripts/list_todos.py .`), the suggestions, and any tool that was not set up or failed. When the developer answers, update those rows.

## The three statuses

Use exactly these words. Nothing else is allowed.

- **Pass**: the evidence shows the item is met, including its quantitative thresholds. Where the item says "review" or "unless justified", Pass needs a recorded justification from the brief or the developer.
- **Not applicable**: the item's own "Mark N/A when" line is true for this report, or its "When applicable" line is not. Write the line you relied on in the evidence cell, word for word, and why it holds for this report: the review check refuses the row otherwise (R007). An item with neither line that fits is never Not applicable. Nor is an item whose fact nobody gave, or one that "does not matter for a test": that is Fail with "Evidence missing:".
- **Fail**: everything else. That includes "no evidence": write `Fail` and start the evidence cell with `Evidence missing:` and what is needed.

More rules:

- If an item covers many objects (columns, measures, visuals, pages), it is Fail when any object in scope fails. Name the objects.
- Never write Pass from an assumption. Evidence is a file path, a script finding code, a section of the brief, or a dated statement from the developer.
- Any `TODO(owner)` placeholder still in the model means item 23 is Fail, and items 37 and 48 are Fail for the measures affected.
- Where the checklist says "Yes", read Pass.

## From script findings to items

| Finding | Where it goes |
|---|---|
| D001, D002, I001, M803, M812 | Item 23 |
| T001, and T105 from `check_template.py` | Item 50 |
| M005, M006, M007, M008, M118, M119 | Items 7 and 28 |
| M101 | Item 22 |
| M102, M103, M104 | Items 19 and 25 |
| M105, M106 | Items 27 and 38 |
| M107 | Item 29 |
| M109, M110, M413, M416 | Items 6 and 14 |
| M009 | Item 36 |
| M112 | Items 71 and 72 |
| M201, M115, M120, P007 | Items 5 and 25 |
| P005 | Item 2 |
| P002, P006, M702, M708 | Item 3 |
| P003 | Item 4 |
| M411, M412, M417 | Item 10 |
| M406, M409 | Item 11 |
| M405, M407, M408 | Item 12 |
| M410 | Item 13 |
| U006 | Item 15 |
| M513, M701, M703, M704, M705, M706, M711, U008, U104, U106 | Item 16 |
| U004 | Item 17 |
| M401 | Item 18 |
| M113 | Item 24 |
| M114 | Item 26 |
| M811, M812, M813, M814, M815 | Item 30 (M812 also counts for item 23) |
| M402, M403, M404 | Item 31 |
| M505 | Item 32 |
| M502 | Item 33 (Fail: the item asks for DIVIDE in every division that is not trivial) |
| M507, M514 | Item 34 |
| M508, M509 | Item 35 |
| M414, M415, M601, M602, M604, M609 | Item 39 |
| M606, M607, M608, M806 | Item 40 |
| M603, M605 | Item 41 |
| G001, G002 | Item 49 (Fail: the item asks for 0 overlapping visuals) |
| G003, G004, G005, G006 | Item 49 (Fail when they name 3 or more visuals on one page, unless the brief justifies it) |
| V009, V024 | Items 50, 70 and 74 (V024 is Fail: the report does not load) |
| V008, U102 | Item 51 |
| G007 | Item 52 |
| V010 | Item 53 |
| A003 | Item 55 |
| U007 | Item 59 |
| U101 | Item 61 |
| V001, V013, V014, V023 | Item 63 (V001 is Fail: the item asks for back navigation on every drillthrough page; V013 on a tooltip page goes to item 65) |
| M821, M822, U003, U103 | Item 64 |
| V002, V003, V004, V005 | Item 65 |
| A001, A002, A004 | Item 66 |
| V006, V007 | Item 20 (V006 is Fail unless the brief gives the reason) |
| M001-M004, M010, M108, M111, M116, M117, M301, M302, M303, M501, M503, M504, M506, M510, M511, M512, M516, M517-M525, M707, M709, M801, M802, M804, M805, M807, M831-M833, M841, M901-M910, P004, V011, V012, V015-V022, B001, B002, G008, C001, D003, P001, F002, F003, J001-J004, S001, N001-N005, H001, H002, U001, U002, U005, U105, and any other finding of `check_template.py` | Template rules, not checklist items. List them in the "Template rules" section of the report |

A warning or a note from the script is evidence, not a verdict: read the item and judge it by its own thresholds. Item 22 is judged by the checklist's thresholds; the two-level measure folders (M003, M004) are a template rule. A finding excused in section 9 or 10 of the brief counts as justified; quote the row.

Notes whose codes start with U are suggestions: a native feature may do a job better. List them in their own section, "Suggestions", with the feature, what it would replace and its release status (`references/native-features.md`). A suggestion never makes an item Fail, and nothing is built from one without the developer's yes.

Some rules have no script. Judge them from the files and the brief: hierarchies for natural drill paths beyond the three column pairs that note U007 knows (item 59); the decision on incremental refresh or partitions for large tables (section 4 of the brief; ask for row counts; report it under "Template rules"); abbreviations in names (item 7); and overlaps on a page that has groups, which the script compares only inside each group (item 49: ask the developer to look).

## Evidence only people can give

These items cannot be judged from project files alone. Do not guess: read the fact yourself where a tool is set up, otherwise mark the item Fail and put the question in your report.

- In Power BI Desktop: query folding (3), key uniqueness and nulls (11, 14), row counts (17), Auto date/time setting (18), slicer value counts (21), date table gaps (31), on-screen text sizes (67), Performance Analyzer (68).
- In the Power BI service or from the team: security roles tested (39-41), sensitivity labels and endorsement (42), permissions (43), lineage (44), refresh and alerting (45), user testing (76), export tests (77), audience access (78), decommission plan (79).

Checklist items: 1-79
Review-only items: 42-45, 68, 76, 78, 79
