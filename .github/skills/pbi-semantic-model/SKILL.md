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

## New model, or new objects in a model

Work in this order.

1. Sources and queries: items 1-6 and 9. Query and step descriptions: `references/descriptions.md`.
2. Tables and relationships: items 10-17 and 38.
3. Date handling: items 18 and 31. Auto date/time is switched off by the developer in Desktop (see "Only Desktop can tell").
4. Columns: items 19, 22, 24, 25, 26. File syntax: `references/tmdl.md`.
5. Measures: items 27-35 and 64. Give every new measure a description, a format string, and a display folder when the table uses folders.
6. Names: items 7 and 28. Use the naming standard in the brief. If the brief has none, follow the names already in the model, or ask.
7. Descriptions: items 8, 23, 37, 46, 48. Rules: `references/descriptions.md`.
8. Formats: items 36, 71, 72. File syntax: `references/tmdl.md`.

## Existing model

- Follow the patterns the model already uses for names, folders and layout.
- Microsoft notes that renaming a field may break report visuals that use it. The rename rule is in the project instructions.
- When you add a description, change nothing else on that object.
- A measure's DAX shows how it is calculated, not what it means to the business. If the brief and the developer do not state the meaning, use the placeholder in `references/descriptions.md`.
- To report gaps without changing anything, use the skill `pbi-checklist-review`.

## Only Desktop can tell

- Auto date/time (item 18): the developer turns it off in Power BI Desktop under File > Options and settings > Options, on the Current File page, in the Time intelligence section. Ask them to do it and to note it in the brief. Do not try to set it in files.
- Facts about the data: which steps fold (item 3), whether keys are unique (items 11, 14), row counts (item 17), gaps in the date table (item 31). Ask the developer. Do not assume.
- Syntax you have no example of (relationships, roles, calculation groups, storage modes, a kind of data source): follow an object of the same kind in this model. If there is none, ask the developer to create the first one in Desktop. Do not write it from memory.

## Gotcha

TMDL depends on indentation. One wrong tab stops the whole model from loading.

Checklist items: 1-19, 22-38, 46, 48, 64, 71, 72
