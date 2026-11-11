---
name: Semantic model files (TMDL)
description: Hard rules for Power BI semantic model files in TMDL format.
applyTo: "**/*.tmdl"
---
# Rules for TMDL files

`python scripts/check_project.py .` enforces rules 1, 3 and 4 and lists every placeholder left by rule 2. How-to detail is in the skill `pbi-semantic-model`.

1. Every visible table, column and measure has a `///` description directly above it. So does every shared query and parameter (`expression`). No blank line between the description and the object.
2. A description says only what the brief, the model or the developer states. The placeholder for unknown meaning (project instructions) goes here as a `///` line: `/// TODO(owner): <question>`.
3. No `//` comments, except inside a Power Query (M) or DAX expression.
4. Inside a Power Query query, every step has a `//` comment line directly above it that says what the step does (a `/* */` comment also counts). This is a convention of this template.
5. Indent with tabs, the way Power BI Desktop writes these files.
6. Do not write `lineageTag` on new objects and do not touch existing ones. Do not add annotations whose names start with `PBI_`. Power BI manages both.
7. Hiding a table or column is decided under checklist items 19 and 25, never by the description check.

Checklist items: 8, 19, 23, 25
