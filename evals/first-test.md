# First test: the whole flow on Microsoft's "Corporate Spend" sample

Status: **not run yet**. One page to try "evaluate and improve" end to end on a report nobody here built. Allow about an hour. Do it in a scratch copy of your repository, on a scratch branch.

The sample is Microsoft's and is not kept in this repository. Do not commit it to a public repository.

## Set up

1. Download `Corporate Spend.pbix` from the folder `2026 Power BI Samples Revamp` of `microsoft/powerbi-desktop-samples` on GitHub.
2. Open it in Power BI Desktop. File > Save as, file type Power BI project (`.pbip`), into the root of your scratch clone. Close Desktop.
3. Do not import the theme and do not fix anything by hand: the test is what the flow finds.
4. Note the page size of the report in section 2 of `docs/report-brief.md` (an existing report keeps its size). Leave the rest of the brief empty.
5. Commit everything.
6. Record the starting point:

```bash
python scripts/check_project.py . > before.txt
```

## Run

In VS Code, in Copilot Chat in agent mode, with the model you want to test, ask exactly:

> Evaluate and improve this report.

When Copilot stops at the fix plan, first answer "Only the mechanical rows". When that is done, ask it to carry on and answer "Now the layout rows".

At any time you can ask the script where the flow stands:

```bash
python scripts/improve.py next
```

## What to record

| What | Where to find it |
|---|---|
| The AI model and the date | Copilot Chat |
| Errors, warnings and notes at the start | last line of `before.txt` |
| Pass, Fail, Not applicable before and after | `python scripts/improve.py compare` |
| Rows in the plan by kind, and how many you approved | `python scripts/improve.py check-plan` |
| Did Copilot stop before changing anything | `git log` on the new branch: no fix commit before your answer |
| The two commits | `git log --oneline` |
| Every place where Copilot guessed, skipped a step or needed a reminder | your notes |
| What looked different in Desktop, page by page | open `_before/` and the working project side by side |
| Each finding that was wrong (a false alarm), with the object | your notes; each one is a lesson for the template |

In Power BI Desktop also check these, because no document settles them: a measure named with `#` or `(%)` works; display folders written as `Subject\Type` show as two levels; any `CalculatedReason` annotation is still in the file after you save; the tab order and the phone layout of a page whose visuals moved.

## What a good result looks like

- A new branch `improve/<date>`; the branch you started on did not move; `_before/` opens in Desktop and is not in Git.
- The review has all 79 rows and passes `python scripts/check_project.py --review docs/checklist-review.md`.
- The plan sorts every finding. Moving measures to `_Measures`, renames, data types and summarisation are under "Needs a person", never under "Mechanical".
- Copilot changed nothing before your yes, and then only the kind you approved.
- One commit per kind, with the messages `Improve: mechanical fixes` and `Improve: layout fixes`. Undoing one with `git revert` leaves the other in place.
- Fewer Fail items after than before, and no item that went from Pass to Fail.
- `python scripts/check_project.py .` reports no G001 and no G002, and fewer errors than `before.txt`.
- Every description Copilot wrote comes from the brief or is a `TODO(owner)` question. Nothing was renamed. No group moved.
- Copilot named the pages to look at, and those pages look right in Desktop.
- `python scripts/check_template.py` still passes: the checklist and the theme are unchanged.

A sample report will not pass everything, and it should not: its measures do not live in `_Measures`, and that stays a row for a person.

## Afterwards

Add one row per run to the results log in `evals/prompts.md` (prompt id E15). For every wrong finding or missed step, tell Copilot; it records a lesson (skill `pbi-lessons`), and a repeated lesson becomes a proposed change to the template.
