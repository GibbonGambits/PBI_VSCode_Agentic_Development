---
name: pbi-improve
description: Use this skill when asked to evaluate an existing Power BI report and model and then improve it in one go - "evaluate and improve this report", "review and fix", "bring this report up to the standard". It keeps the original safe, evaluates against the 79-item checklist, writes a fix plan sorted by kind, applies every fix it can without asking for approval and without holding any back, and ends with one answer - the counts before and after, what was skipped, and the questions that need a person. Trigger words - evaluate and improve, review and fix, improve this report, fix the findings, bring up to standard.
---
# Evaluate, then improve

Do the steps in order. Do not rely on memory: before each step run

```
python scripts/improve.py next
```

It reads the files and Git, and prints the step you are on and what to run. If it names a different step from the one you expected, follow the script.

## How this flow treats the developer

- **No approvals.** Nothing waits for a yes. The branch, the copy in `_before/` and one commit for each kind of fix are the safeguard: each kind can be undone alone.
- **One moment at the start, one answer at the end.** At the start the developer saves and closes the project. Ask nothing until your final answer. A fact you cannot find becomes a question in that answer.
- **Nothing is held back.** Measures move and names are corrected like every other fix. A report that reads a published copy of this model names a measure with its table, so it may break, and no file here can show such a report: say so in your final answer, and nothing more.
- **A missing data source never stops a fix.** The kind Data is applied like every other kind. A table whose query, partition or data type changed, and a new table, are empty until Power BI Desktop refreshes the model: say so in your final answer, and nothing more.

## Steps

1. **Safety first.** The project must be saved and closed in Power BI Desktop (Microsoft Learn: `report.json` is not reloaded into an open session), and everything committed: if `git status` shows anything, commit it yourself, without asking, with the message `Before improve: the report as found`. Run `python scripts/improve.py start`. It stops if anything is not committed, if no branch is checked out, or if an earlier flow left its plan, its first review or `_before/` behind; then tell the developer what it said and wait. It makes a new branch, so the original stays untouched on the old one, and copies the project unchanged into `_before/`. If it says it made no copy, say why in your final answer; the branch is then the safeguard. Never edit, check or commit `_before/`.
2. **Evaluate.** Use the skill `pbi-checklist-review` from start to finish, without asking the developer anything. It writes `docs/checklist-review.md`. Then run `python scripts/improve.py snapshot` to keep that review as the "before".
3. **Write the fix plan.** Run `python scripts/improve.py plan`. It writes `docs/fix-plan.md` with one row for every error, every warning and every failed item, each with a kind and a status:
   - **Theme**: the owner's theme is registered in the report.
   - **Mechanical**: descriptions, format strings, display folders, hiding, header icons and tooltips, alt text and titles, a data category that a column's name states, the DAX style, two rewrites that cannot change a result (M518, M519), styling that the theme should do.
   - **Layout**: positions and sizes, by the numbers in `.github/skills/pbi-report/references/layout-standard.md`; a back button on a drillthrough page; tab order.
   - **Measures**: every measure moves to `_Measures`; the table is made when it is missing.
   - **Renames**: names that the naming standard rejects.
   - **Data**: changes that need a refresh: a comment line in a query (P001), a partition's name (M117), a floating-point column (M108), and the removal of a column nothing uses.
   - **Needs a person**: a fact or a decision that no file holds: why something is calculated in the model, a threshold, whether key values are unique or whole, summarisation, formulas whose result would change, relationships, security roles, access, user testing, export tests, performance runs. These rows are questions for your final answer.
   Notes are listed apart, for information, and are never fix rows; those whose codes start with U are suggestions.
   Then finish the plan yourself. Give every `?` row a kind. Fill in every `<...>` cell: what will change, which files, what could break. Never give a row a kind it does not have to make the plan look better: a fix that changes what a number means stays under "Needs a person". Run `python scripts/improve.py release`: it gives the rows you sorted their status. Run `python scripts/improve.py check-plan` until it reports no problem.
4. **Apply each kind in order**, as `python scripts/improve.py next` names it: Theme, Mechanical, Layout, Measures, Renames, Data. Apply every row whose status is `to do`. As each row is finished write `done` in its Status, or `skipped: <why>` when it cannot be done (the brief gives no format for it, a reference cannot be confirmed). After each kind run `python scripts/check_project.py .`, fix what it reports, and commit with the message the script gives. How each kind is done:
   - **Theme**: `python scripts/scaffold.py theme .` Say in your final answer that the theme was registered by script, and that Microsoft Learn describes importing it in Power BI Desktop as the supported route.
   - **Mechanical**: the skills `pbi-semantic-model` and `pbi-report`, with `python scripts/set_visual_defaults.py .` for header icons, tooltips and labels and `python scripts/set_model_properties.py . --set "<object>.<property>=<value>"` for folders, formats and hiding. Before header icons and tooltips are switched off, keep what the report uses: see "Features a visual uses" in `.github/skills/pbi-report/references/theme.md`. Alt text, titles, labels and the DAX style are written by you, as the report standard and the DAX standard set out. A reformatted formula keeps every token: only spaces and line breaks change. The two rewrites change tokens and never a result: DIVIDE by a fixed number becomes `/` (M518), and ALL as a filter argument of CALCULATE becomes REMOVEFILTERS (M519).
   - **Layout**: the layout standard, with `python scripts/set_positions.py`.
   - **Measures** and **Renames**: the model standard ("Existing models: moving and renaming"). Every measure moves in one commit. A new name follows the naming standard and keeps the meaning of the old one; when the standard does not settle the name, the row is `skipped: no name follows from the standard` and becomes a question.
   - **Data**: last, so that it can be undone alone.
   When a Data row was done or this flow made the `_Measures` table, `compare` prints one line: Power BI Desktop must refresh the model once. Put that line first in your final answer.
5. **Evaluate again** with the skill `pbi-checklist-review`: go through all 79 items in order, not only the rows you expect to change. `docs/checklist-review.md` is replaced without asking; the first review is kept.
6. **One final answer.** Run `python scripts/improve.py compare` and give the developer, in this order: the counts before and after; what changed, by kind; the pages to look at in Power BI Desktop (look yourself where the Desktop Bridge is agreed: `.github/skills/pbi-report/references/desktop-bridge.md`); what was skipped; the questions, grouped, with the open `TODO(owner)` lines (`python scripts/list_todos.py .`); and any tool that was not set up or failed. Ask nothing else.
7. **Afterwards.** When the developer answers a question, do the work yourself and write `answered` in that row.

## Never in this flow

- Ask for an approval, or stop between the first step and the final answer.
- Build a suggested native feature (a note whose code starts with U) without the developer's yes.
- Turn summarisation off, change a relationship or a security role, or rewrite a formula so that its result changes: those rows are questions.
- Change `checklist/checklist.md`, `theme/theme.json` or any template file. If a fix seems to need a template change, use the skill `pbi-lessons`.
- Publish, deploy or merge.
- Write a business meaning that the brief or the developer did not give. Unknown meaning stays a `TODO(owner)` question.
- Mark an item Not applicable, hide a column, add an exception row or loosen anything just to make a check pass.

If a check fails on something you changed in step 4, that starts the improvement loop: skill `pbi-lessons`.

## Evaluating only

If the developer asks only for an evaluation, use the skill `pbi-checklist-review` and stop there. Report every breach and change nothing.

Checklist items: 47
