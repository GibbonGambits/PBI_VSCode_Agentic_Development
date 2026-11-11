# Power BI project instructions

This repository holds a Power BI project in PBIP format: a semantic model (`*.SemanticModel`, TMDL text files) and a report (`*.Report`, PBIR JSON files). You change those files directly, and you build things yourself: when a shipped example and the checks let you do the work, you do not hand it back to the developer. Three kinds of job are supported: building new, evaluating what exists, and changing what exists.

## Which skill to use

- Model work (tables, columns, measures, DAX, relationships, security roles, Power Query, descriptions): skill `pbi-semantic-model`.
- Report work (pages, visuals, layout, buttons, bookmarks, slicers, visual labels): skill `pbi-report`.
- Evaluating a report and model against the 79-item checklist: skill `pbi-checklist-review`.
- Evaluating an existing report and then improving it, in one request: skill `pbi-improve`.
- A business term in reliability, energy and gas, customer, safety, finance, workforce, IT and security, or work management: skill `business-definitions`.
- The developer corrects you, or a check fails on something you created or changed: skill `pbi-lessons`.
- A check fails and the cause is not clear, a DAX error, a function that is new to this model, or a lesson about to be written: skill `pbi-lookup`.
- Background practice the standards do not give (a DAX or model design choice, a performance question, an unusual requirement, a failed check that a look-up did not explain): skill `pbi-practice-library`. It is information: the checklist and the standards win, and a note marked Check is confirmed with skill `pbi-lookup` first.

## Rules for every task

- One chat per task. If this chat already holds another finished task, ask the developer to start a new chat for the new one: a long chat loses its early instructions.
- Never invent meaning. Definitions, descriptions and thresholds come from `docs/report-brief.md`, the model, or the developer. If none of them says it, write `/// TODO(owner): <question>` and carry on: a missing description never blocks the work. That line is the only record. Ask about all of them together at the end of the task (`python scripts/list_todos.py .`).
- Never guess a Power BI property name, value or file layout. Follow the pattern of a file of that kind already in this project, or read the Microsoft schema named on the file's `$schema` line. If neither exists, copy a shipped example, then run the checks. Ask only when no example exists.
- The shipped examples of every object kind are listed in `tests/fixtures/examples/INDEX.md`. Copies of Microsoft's schemas are in `scripts/schemas`. Files that Microsoft says not to edit by hand are read only; the two instruction files name them.
- Existing objects keep their names. Do not rename or delete existing tables, columns, measures, pages or visuals, and do not move a measure to another table. If the developer asks for a rename, a move or a deletion, say what may break, here and in other reports on the same model, and wait for a clear yes. After the yes, do the work yourself when `python scripts/find_references.py` can confirm every reference in this project, and list anything it cannot confirm.
- Do not change `theme/theme.json` or `checklist/checklist.md`.
- Do not change a template file without asking first. Template files are everything under `.github/`, `scripts/`, `tests/`, `evals/` and `maintenance/`, and the root files `README.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, `.gitignore` and `.gitattributes`. A person approves such a change by pull request.
- Do not read the folder `maintenance/`. It holds the template's own working papers, not guidance for a report.
- Do not publish, deploy or connect to any Power BI or Fabric workspace. You may call Microsoft's own agent tools that this template names (the Desktop Bridge tools behind `scripts/desktop_bridge.py`, Microsoft's Power BI modeling server, Microsoft's Learn server), and only to read, check, reload and take screenshots. Never install them, never change a model through them, and call no other Power BI tool or server. Everything works without them. One exception to the workspace rule: for a report on a published model, read the field list through Microsoft's modeling server if the developer has already set that connection up (skill `pbi-report`).
- A preview feature is used only after the developer's yes, recorded in section 11 of the brief.
- When a native feature would do a job better, say so as a note at the end of your answer (the checks print such notes with codes that start with U). Never ask about it in the middle of a task, and act on it only after the developer's yes.
- Before you edit, the project must be saved in Power BI Desktop: ask the developer, or read it with `python scripts/desktop_bridge.py status` where the developer has agreed to the Desktop Bridge. After you edit, reload and look at the pages that changed: with `scripts/desktop_bridge.py` where it is agreed, otherwise ask the developer. Files that pass the checks can still look wrong on screen.
- After every change to project files, run `python scripts/check_project.py .` and fix each error it lists. Never hide a column, delete an object or add an exception just to make a check pass.
- Work on a branch and keep changes small. Say what changed and why in each commit message: that history is the change log. Commit only when the developer asks.

Checklist items: 47
