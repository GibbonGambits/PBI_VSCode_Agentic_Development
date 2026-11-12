---
name: pbi-semantic-model
description: Use this skill when creating, changing or checking a Power BI semantic model stored as TMDL files - tables, columns, measures, DAX, relationships, date tables, security roles, calculation groups, user-defined functions, field parameters, storage modes, Power Query (M) queries and steps, descriptions, display folders, format strings. Covers new models and existing ones. Trigger words - model, table, column, measure, DAX, relationship, role, Power Query, M, description, .tmdl.
---
# Power BI semantic model

Not for report pages or visuals (skill `pbi-report`) and not for the full 79-item evaluation (skill `pbi-checklist-review`).

You build the model yourself. When you have no example of a kind of object in this model, you copy the shipped example and run the checks. You ask the developer only for what no file can tell you: what something means, and facts about the data.

## Before you change anything

1. Read `docs/report-brief.md`. What it does not say about meaning becomes a `/// TODO(owner): <question>` line (rules in `references/descriptions.md`); you ask about those at the end of the task, not during it.
2. Read the model under `*.SemanticModel/definition/`: one file per table in `tables/`, shared queries and parameters in `expressions.tmdl`, relationships in `relationships.tmdl`, functions in `functions.tmdl`, roles in `roles/`.
3. No project yet? Make one: `python scripts/scaffold.py project <Name>`. It copies the shipped starter project. The developer then imports the theme once in Power BI Desktop (Design ribbon > Import theme); the script says so.

Checklist items are in `checklist/checklist.md`. Read only the items a step names, by searching for the heading, for example `## Item 23`.

## The standards

Read the file that fits the work before you write. `python scripts/check_project.py .` checks every one of them; the code after a rule is the finding it gives. Exceptions go in section 9 of the brief.

| For | Read | Codes |
|---|---|---|
| Where measures live, folders, measure names, hiding, calculated objects, summarising, data types, formats | `references/model-standard.md` | M0xx, M1xx to M112, M2xx, M3xx |
| Star schema, relationships, role-playing and slowly changing dimensions, keys, the date table, sort columns, names of tables and columns | `references/relationships-and-dates.md` | M4xx, M113 to M120, M901 to M907 |
| DAX rules, DAX style, DAX patterns, time intelligence | `references/dax-standard.md` | M5xx, M908, M909, M010 |
| Power Query, query folding, data reduction, storage modes, DirectQuery and composite models, aggregations, incremental refresh, security roles | `references/storage-and-security.md` | P0xx, M6xx, M7xx, M832, M833, M910 |
| User-defined functions, calculation groups, field parameters, perspectives, translations and the other object kinds | `references/model-objects.md` | M801 to M831, M841 |
| Hybrid tables, Direct Lake variants, dynamic query parameters, selection expressions, model options, value filter behavior, the other folders of a model item | `references/more-model-features.md` | M841 |
| One report for readers in several languages: locale, label measures, page navigation, translated data | `references/multiple-languages.md` | M524, M525, V019 to V021 |
| The names of all DAX functions, with their Microsoft Learn addresses | `references/dax-functions.md` | M909 |
| File syntax, and the shipped examples | `references/tmdl.md` | J001, C001, D00x |

## New model, or new objects in a model

Work in this order.

1. Sources and queries: items 1-6 and 9. Every step gets its description line (`references/descriptions.md`).
2. Tables and relationships: items 10-17 and 38.
3. Date handling: items 18 and 31. One marked date table: copy the shipped example.
4. Columns: items 19, 22, 24, 25, 26, and part B of the model standard.
5. Measures: items 27-35 and 64, and part A of the model standard. Every new measure goes in the table `_Measures`, with a description, a format string and a display folder of two levels, `Subject\Type`. If the model has no `_Measures` table, make it: `python scripts/scaffold.py measures-table .` (an imported one-column table; a calculated table when the model reads its data in Direct Lake or DirectQuery mode).
6. Names: items 7 and 28. Measure names follow the model standard. Tables and columns follow the brief; if it says nothing, the default in `references/relationships-and-dates.md`.
7. Descriptions: items 8, 23, 37, 46, 48.
8. Formats: items 36, 71, 72.
9. Run `python scripts/check_project.py .` and fix every error. Then `python scripts/list_todos.py .`, and ask the developer about the open questions in one message.

## Existing model

- New objects follow the standards. Existing objects keep their names and their home table. A breach in what already exists is reported, not changed: it is changed only when the developer asks, or through the skill `pbi-improve`.
- A rename or a move the developer asks for, or the skill `pbi-improve` makes: do it at once, without asking, and say in your final answer that reports on a published copy of the model may break. Run `python scripts/find_references.py . "<object>"` first, do the work yourself as set out in the model standard ("Existing models: moving and renaming"), and list the places the script cannot classify in your final answer.
- To set a display folder, a format string, hidden, or the reason line of a calculated object on something that exists, use `python scripts/set_model_properties.py` with `--dry-run` first. It changes that one line and nothing else. The value comes from the brief or the developer.
- When you add a description, change nothing else on that object.
- A measure's DAX shows how it is calculated, not what it means to the business. If the brief and the developer do not state the meaning, write the placeholder and carry on.
- To report gaps without changing anything, use the skill `pbi-checklist-review`.

## A better native feature

The check prints notes with codes that start with U when a native feature may do a job better: a user-defined function for a repeated formula, a calculation group for time variants, a field parameter in place of a switching measure, an aggregation table for DirectQuery, a dynamic format string, a hierarchy. The full list is in `.github/skills/pbi-checklist-review/references/native-features.md`. Mention a suggestion once, at the end of your answer. Never stop a task to ask about one. Build it only after the developer's yes; a preview feature also needs its row in section 11 of the brief.

## What the files cannot tell

- Auto date/time (item 18) is an option of Power BI Desktop: File > Options and settings > Options, the Current File page, Time intelligence. The check reports it when it is on (M401). Tell the developer once, and note it in section 6 of the brief. Do not set it in files.
- Facts about the data: whether keys are unique (items 11, 14), row counts (item 17), distinct values, gaps in the date table (item 31). Read them yourself when the developer has set up Microsoft's modeling server (`references/data-facts.md`). Otherwise ask the developer once, in one message, and record the answers in section 4 of the brief. Whether a step folds (item 3) is always in that one message: the server is not known to tell.
- Whether the model loads and the numbers are right. Reload through `python scripts/desktop_bridge.py reload . --with-model` where the Desktop Bridge is installed; otherwise ask the developer to reload and look.

## When you are stuck

A check fails and you cannot see why, DAX gives an error, or you are about to use a function that is new to this model: skill `pbi-lookup`. Do not guess.

## Gotcha

TMDL depends on indentation. One wrong tab stops the whole model from loading.

Checklist items: 1-19, 22-38, 46, 48, 59, 64, 71, 72
