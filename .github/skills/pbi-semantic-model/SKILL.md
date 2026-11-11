---
name: pbi-semantic-model
description: Use this skill when creating, changing or checking a Power BI semantic model stored as TMDL files - tables, columns, measures, DAX, relationships, Power Query (M) queries and steps, descriptions, display folders, format strings. Covers new models and existing ones. Trigger words - model, table, column, measure, DAX, Power Query, M, description, .tmdl.
---
# Power BI semantic model

Not for report pages or visuals (skill `pbi-report`) and not for the full 79-item evaluation (skill `pbi-checklist-review`).

## Before you change anything

1. Read `docs/report-brief.md`. If it does not answer what you need, ask the developer. Do not fill the gap yourself.
2. Read the model under `*.SemanticModel/definition/`: one file per table in `tables/`, shared queries and parameters in `expressions.tmdl`, relationships in `relationships.tmdl`.

Checklist items are in `checklist/checklist.md`. Read only the items a step names, by searching for the heading, for example `## Item 23`.

## The model standard

`references/model-standard.md` is the one standard for where measures live, folders, names, hiding, calculated objects, summarising, data types and formats. Read it before you add or change a measure, a column or a table. It adds detail to the checklist and never overrides it. `python scripts/check_project.py .` checks it (codes that start with M) and reads its exceptions from section 9 of the brief.

## New model, or new objects in a model

Work in this order.

1. Sources and queries: items 1-6 and 9. Query and step descriptions: `references/descriptions.md`.
2. Tables and relationships: items 10-17 and 38.
3. Date handling: items 18 and 31. Auto date/time is switched off by the developer in Desktop (see "Only Desktop can tell").
4. Columns: items 19, 22, 24, 25, 26, and part B of the model standard (hiding, summarising, data types, formats, the reason line of a calculated column). File syntax: `references/tmdl.md`.
5. Measures: items 27-35 and 64, and part A of the model standard. Every new measure goes in the table `_Measures`, with a description, a format string and a display folder of two levels, `Subject\Type`. If the model has no `_Measures` table yet, ask the developer to make it in Power BI Desktop; do not write it from memory.
6. Names: items 7 and 28. Measure names follow the model standard, unless the brief names another standard. For tables and columns use the brief; if it says nothing, follow the names already in the model, or ask.
7. Descriptions: items 8, 23, 37, 46, 48. Rules: `references/descriptions.md`.
8. Formats: items 36, 71, 72. File syntax: `references/tmdl.md`.

## Existing model

- New objects follow the model standard. Existing objects keep their names and their home table. A breach in what already exists is reported, not changed: it is changed only when the developer asks, or through the skill `pbi-improve`.
- Microsoft notes that renaming a field may break report visuals that use it, and that a formula naming a measure with its table breaks when the measure moves. The model standard ("Existing models") says what to tell the developer first. The rename rule is in the project instructions.
- To set a display folder, a format string, hidden, or the reason line of a calculated object on something that exists, use `python scripts/set_model_properties.py` with `--dry-run` first. It changes that one line and nothing else. The value comes from the brief or the developer.
- When you add a description, change nothing else on that object.
- A measure's DAX shows how it is calculated, not what it means to the business. If the brief and the developer do not state the meaning, use the placeholder in `references/descriptions.md`.
- To report gaps without changing anything, use the skill `pbi-checklist-review`.

## Only Desktop can tell

- Auto date/time (item 18): the developer turns it off in Power BI Desktop under File > Options and settings > Options, on the Current File page, in the Time intelligence section. Ask them to do it and to note it in the brief. Do not try to set it in files.
- Facts about the data: which steps fold (item 3), whether keys are unique (items 11, 14), row counts (item 17), gaps in the date table (item 31). Ask the developer. Do not assume.
- Syntax you have no example of (relationships, roles, calculation groups, storage modes, a kind of data source): follow an object of the same kind in this model. If there is none, ask the developer to create the first one in Desktop. Do not write it from memory.

## Gotcha

TMDL depends on indentation. One wrong tab stops the whole model from loading.

Checklist items: 1-19, 22-38, 46, 48, 59, 64, 71, 72
