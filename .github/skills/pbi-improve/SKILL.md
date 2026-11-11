---
name: pbi-improve
description: Use this skill when asked to evaluate an existing Power BI report and model and then improve it in one go - "evaluate and improve this report", "review and fix", "bring this report up to the standard". It keeps the original safe, evaluates against the 79-item checklist, writes a fix plan sorted into Mechanical, Layout and Needs a person, stops for the developer's approval, applies only what was approved, and shows the counts before and after. Trigger words - evaluate and improve, review and fix, improve this report, fix the findings, bring up to standard.
---
# Evaluate, then improve

Do the steps in order. Do not rely on memory: before each step run

```
python scripts/improve.py next
```

It reads the files and Git, and prints the step you are on and what to run. If it names a different step from the one you expected, follow the script.

## Steps

1. **Safety first.** Ask the developer to save in Power BI Desktop and to commit everything. Then run `python scripts/improve.py start`. It stops if anything is not committed. It makes a new branch, so the original stays untouched on the old one, and copies the project unchanged into `_before/`, so the developer can open before and after side by side. If it says it made no copy, tell the developer why; the branch is then the safeguard. Never edit, check or commit `_before/`.
2. **Evaluate.** Use the skill `pbi-checklist-review` from start to finish. It writes `docs/checklist-review.md`. Then run `python scripts/improve.py snapshot` to keep that review as the "before".
3. **Write the fix plan.** Run `python scripts/improve.py plan`. It writes `docs/fix-plan.md` with one row for every finding and every failed item, sorted into three kinds:
   - **Mechanical**: descriptions, format strings, display folders, hiding, header icons and tooltips.
   - **Layout**: positions and sizes, by the numbers in `.github/skills/pbi-report/references/layout-standard.md`.
   - **Needs a person**: access, user testing, export tests, performance runs; renames and moves; data types; summarisation; and anything a file cannot settle.
   Then finish the plan yourself. Give every `?` row a kind. Fill in every `<...>` cell: what will change, which files, what could break. Never move a row out of "Needs a person" to make the plan look better. Run `python scripts/improve.py check-plan` until it reports no problem.
4. **Stop.** Show the developer the plan. They approve all of it, one kind, or single rows. Write `yes` or `no` and the date in the Approved column of each row they answered. Change no report or model file before this.
5. **Apply the approved Mechanical rows**, and only those, with the skills `pbi-semantic-model` and `pbi-report` and these scripts:
   - `python scripts/set_visual_defaults.py .` for header icons, tooltips and labels;
   - `python scripts/set_model_properties.py . --set "<object>.<property>=<value>"` for folders, formats, hiding and the reason line of a calculated object. Values come from the brief or the developer, never from you.
   Run `python scripts/check_project.py .` and fix what it reports. Commit with the message `Improve: mechanical fixes`.
6. **Apply the approved Layout rows**, and only those, as set out in the layout standard, with `python scripts/set_positions.py`. Run the check. Commit with the message `Improve: layout fixes`. The two commits stay separate, so each can be undone alone.
7. **Evaluate again** with the skill `pbi-checklist-review`. Then run `python scripts/improve.py compare` and give the developer its output: Pass, Fail and Not applicable before and after, the items that changed, the pages to reload and look at in Power BI Desktop, and the rows that need a person.

## Never in this flow

- Rename or move an existing object without a clear yes for that object. Measures move to `_Measures` only by the developer's hand in Power BI Desktop.
- Change a data type, or turn summarisation off, as a Mechanical fix.
- Change `checklist/checklist.md`, `theme/theme.json` or any template file. If a fix seems to need a template change, use the skill `pbi-lessons`.
- Publish, deploy or merge.
- Write a business meaning that the brief or the developer did not give. Unknown meaning stays a `TODO(owner)` question.
- Hide a column, add an exception row or loosen anything just to make a check pass.

If a check fails on something you changed in steps 5 or 6, that starts the improvement loop: skill `pbi-lessons`.

## Evaluating only

If the developer asks only for an evaluation, use the skill `pbi-checklist-review` and stop there. Report every breach and change nothing.

Checklist items: 47
