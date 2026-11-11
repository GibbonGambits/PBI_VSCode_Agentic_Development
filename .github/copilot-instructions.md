# Power BI project instructions

This repository holds a Power BI project in PBIP format: a semantic model (`*.SemanticModel`, TMDL text files) and a report (`*.Report`, PBIR JSON files). You change those files directly. Three kinds of job are supported: building new, evaluating what exists, and changing what exists.

## Which skill to use

- Model work (tables, columns, measures, DAX, Power Query, descriptions): skill `pbi-semantic-model`.
- Report work (pages, visuals, layout, visual labels): skill `pbi-report`.
- Evaluating a report and model against the 79-item checklist: skill `pbi-checklist-review`.
- A business term in reliability, energy and gas, customer, safety, finance, workforce, IT and security, or work management: skill `business-definitions`.
- The developer corrects you, or a check fails on something you created or changed: skill `pbi-lessons`.

## Rules for every task

- Never invent meaning. Definitions, descriptions and thresholds come from `docs/report-brief.md`, the model, or the developer. If none of them says it, ask, or write `TODO(owner): <question>` and tell the developer.
- Never guess a Power BI property name, value or file layout. Follow the pattern of a file of that kind already in this project, or read the Microsoft schema named on the file's `$schema` line. If the project has no example and you cannot confirm it, say so and ask the developer to create the first one in Power BI Desktop.
- Existing objects keep their names. Do not rename or delete existing tables, columns, measures, pages or visuals. If the developer asks for a rename or a deletion, say what may break and wait for a clear yes.
- Do not change `theme/theme.json` or `checklist/checklist.md`.
- Do not change a template file without asking first. Template files are everything under `.github/`, `scripts/`, `tests/` and `evals/`, and the root files `README.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, `.gitignore` and `.gitattributes`. A person approves such a change by pull request.
- Do not publish, deploy or connect to any Power BI or Fabric workspace. Do not install or call other Power BI command-line tools or servers.
- Before you edit, ask the developer to save in Power BI Desktop. After you edit, ask them to reload the project in Desktop and look at it: files that pass the checks can still look wrong on screen.
- After every change to project files, run `python scripts/check_project.py .` and fix each error it lists. Never hide a column, delete an object or add an exception annotation just to make a check pass.
- Work on a branch and keep changes small. Say what changed and why in each commit message: that history is the change log. Commit only when the developer asks.

Checklist items: 47
