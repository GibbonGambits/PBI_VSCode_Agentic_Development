---
name: Semantic model files (TMDL)
description: Hard rules for Power BI semantic model files in TMDL format.
applyTo: "**/*.tmdl"
---
# Rules for TMDL files

`python scripts/check_project.py .` enforces rules 1, 3, 4, 8, 9 and 11 and lists every placeholder left by rule 2. How-to detail is in the skill `pbi-semantic-model`.

1. Every visible table, column and measure has a `///` description directly above it. So does every shared query and parameter (`expression`). No blank line between the description and the object.
2. A description says only what the brief, the model or the developer states. Unknown meaning becomes one `///` line, `/// TODO(owner): <question>`, and the work goes on. `python scripts/list_todos.py .` prints them; ask about them at the end of the task.
3. No `//` comments, except inside a Power Query (M) or DAX expression.
4. Inside a Power Query query, every step has a `//` comment line directly above it that says what the step does (a `/* */` comment also counts). This is a convention of this template.
5. Indent with tabs, the way Power BI Desktop writes these files.
6. Do not write `lineageTag` on new objects and do not touch existing ones. Do not add annotations whose names start with `PBI_`. Power BI manages both.
7. Hiding a table or column is decided under checklist items 19 and 25, never by the description check.
8. A new measure goes in the table `_Measures`, with a business name, a format string and a display folder of exactly two levels, `Subject\Type`. If the model has no `_Measures` table, make it: `python scripts/scaffold.py measures-table .`. Whether a measure that already exists may move or be renamed is decided by section 3 of the brief (always-on rules).
9. A calculated column or calculated table carries `annotation CalculatedReason = <why it is calculated in the model>`, in the developer's words; a table the standards define (a calculated `_Measures` table, a field parameter) carries the standard's own line.
10. Never turn summarisation off on an existing column without the developer's decision. A data type changes only on that decision too, or as a row of the kind Data in the skill `pbi-improve`.
11. Every name a formula or a property uses exists in the model: a relationship's columns, a sort column, a hierarchy level, a `Table[Column]` in DAX. Divide with DIVIDE unless the divisor is a fixed number. Write DAX in the style of the DAX standard (skill `pbi-semantic-model`).
12. New syntax comes from an object of that kind in this model, or from the shipped example of that kind (`tests/fixtures/examples/INDEX.md`). Never from memory.
13. Read only, never edited by hand: `diagramLayout.json` (Microsoft says so) and, by this template's rule, `.platform` and everything in a `.pbi` folder. `definition.pbism` is copied from a shipped example and left as it is.

Checklist items: 8, 19, 22, 23, 25, 27, 28, 33
