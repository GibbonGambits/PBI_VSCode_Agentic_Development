# Power BI project instructions

This repository holds a Power BI project in PBIP format: a semantic model (`*.SemanticModel`, TMDL text files) and a report (`*.Report`, PBIR JSON files). You change those files directly, and you build things yourself: when a shipped example and the checks let you do the work, you do not hand it back to the developer. Three kinds of job are supported: building new, evaluating what exists, and changing what exists.

## Which skill to use

- Model work (tables, columns, measures, DAX, relationships, security roles, Power Query, descriptions): skill `pbi-semantic-model`.
- Report work (pages, visuals, layout, buttons, bookmarks, slicers, visual labels): skill `pbi-report`.
- Evaluating a report and model against the 79-item checklist: skill `pbi-checklist-review`.
- Evaluating an existing report and then improving it, in one request ("improve", "improve the design", "apply best practices"): skill `pbi-improve`.
- A business term in reliability, energy and gas, customer, safety, finance, workforce, IT and security, or work management: skill `business-definitions`.
- The developer corrects you, or a check fails on something you created or changed: skill `pbi-lessons`.
- A check fails and the cause is not clear, a DAX error, a function that is new to this model, or a lesson about to be written: skill `pbi-lookup`.
- Background practice the standards do not give (a DAX or model design choice, a performance question, an unusual requirement, a failed check that a look-up did not explain): skill `pbi-practice-library`. It is information: the checklist and the standards win, and a note marked Check is confirmed with skill `pbi-lookup` first.

## Start of every task

1. Before anything else, run `python scripts/desktop_bridge.py status .`. When it says Microsoft's tools are not installed, put the setup lines it prints at the top of your first answer and carry on without them. When you need to see pages and Desktop does not have the project open, open it yourself: `python scripts/desktop_bridge.py open .`.
2. A request to improve an existing report that does not say what to improve gets one question, with three choices: improve the design, apply best practices, or both. Nothing else is asked before the work.

## Rules for every task

- One chat per task. If this chat already holds another finished task, ask the developer to start a new chat for the new one: a long chat loses its early instructions.
- Never invent meaning. Definitions, descriptions and thresholds come from `docs/report-brief.md`, the model, or the developer. If none of them says it, write `/// TODO(owner): <question>` and carry on: a missing description never blocks the work. That line is the only record. Ask about all of them together at the end of the task (`python scripts/list_todos.py .`). A choice that is not business meaning is different: a display folder, a number or date format, the reason line of a calculated object that already exists. Take the default the standard gives, add a row to section 6 of the brief with `assumed` under By, and list it under Assumptions in your final answer.
- Never guess a Power BI property name, value or file layout. Follow the pattern of a file of that kind already in this project, or read the Microsoft schema named on the file's `$schema` line. If neither exists, copy a shipped example, then run the checks. Ask only when no example exists.
- The shipped examples of every object kind are listed in `tests/fixtures/examples/INDEX.md`. Copies of Microsoft's schemas are in `scripts/schemas`. Files that Microsoft says not to edit by hand are read only; the two instruction files name them.
- Existing objects keep their names and their home table unless the developer asks for a change or the skill `pbi-improve` runs. When one of them applies, do the rename, the move or the deletion at once, yourself, without asking: repair every reference `python scripts/find_references.py` finds in this project and list anything it cannot confirm. Say in your final answer that a report on a published copy of this model names the object the old way and may break: no file here can show such a report.
- Do not change `theme/theme.json` or `checklist/checklist.md`.
- Do not change a template file without asking first. Template files are everything under `.github/`, `scripts/`, `tests/`, `evals/` and `maintenance/`, and the root files `README.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, `.gitignore` and `.gitattributes`. A person approves such a change by pull request.
- Do not read the folder `maintenance/`. It holds the template's own working papers, not guidance for a report.
- Do not publish, deploy or connect to any Power BI or Fabric workspace. You may call Microsoft's own agent tools that this template names (the Desktop Bridge tools behind `scripts/desktop_bridge.py`, Microsoft's Power BI modeling server, Microsoft's Learn server), and only to read, check, open this project, reload and take screenshots. Never install them, never change a model through them, and call no other Power BI tool or server. Everything works without them. One exception to the workspace rule: for a report on a published model, read the field list through Microsoft's modeling server if the developer has already set that connection up (skill `pbi-report`).
- A preview feature is used only after the developer's yes, recorded in section 11 of the brief.
- When a native feature would do a job better, say so as a note at the end of your answer (the checks print such notes with codes that start with U). Never ask about it in the middle of a task, and act on it only after the developer's yes.
- Ask only at the start of a task or at its end, never in the middle: what you cannot know becomes a `TODO(owner)` line or a question in your final answer. If a tool you may call is not set up or fails, say so in that answer.
- Before you edit, the project must be saved in Power BI Desktop (`status` says so). After you edit, reload (`--with-model` when `.tmdl` files changed) and look at screenshots of the pages that changed, without asking first; when the Bridge is not available, ask the developer. Files that pass the checks can still look wrong on screen. In DAX, write every table name in single quotes, also before a column (`'Sales'[Amount]`), and test every measure you write or change: a screenshot of a visual that uses it, or a query through Microsoft's modeling server. When neither was possible, say in your final answer which DAX is not tested. A formula that passes the checks can still fail in Power BI.
- After every change to project files, run `python scripts/check_project.py .` and fix each error it lists. Never hide a column, delete an object or add an exception just to make a check pass.
- Work on a branch and keep changes small. Say what changed and why in each commit message: that history is the change log. Commit only when the developer asks; asking for the skill `pbi-improve` is such an ask, and that flow makes one commit for each kind of fix.

Checklist items: 47
