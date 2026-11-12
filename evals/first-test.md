# First test: the whole flow on a Microsoft sample report

Status: **run once with the earlier flow, on a sample whose data source could not be reached; not run yet with this one**. One page to try "evaluate and improve" end to end on a report nobody here built. Allow about an hour. Do it in a scratch copy of your repository.

The sample is Microsoft's and is not kept in this repository. Do not commit it to a public repository. In a clone of a public repository, block pushing first: `git remote set-url --push origin no-push`.

## Set up

1. Pick a sample whose data you can refresh on your computer. Both of these are in the folder `2026 Power BI Samples Revamp` of `microsoft/powerbi-desktop-samples` on GitHub; their queries were read, and neither has been refreshed here:
   - `Revenue Opportunities.pbix`: 3 pages, 12 visuals, 6 measures in a table named Calculations, its own theme. Seven tables hold their data inside the query and the eighth combines two of them, so it refreshes anywhere. Start with this one.
   - `AdventureWorks Sales.pbix`: 1 page, 17 visuals, 20 measures in two tables. Seven tables read one Excel workbook, which is in the same repository: `AdventureWorks Sales Sample/AdventureWorks Sales.xlsx`. Download it too, then in Power BI Desktop choose Transform data > Data source settings > Change Source, point it at your copy, and refresh once.
   Do not use a sample whose source you cannot reach (`Corporate Spend.pbix` reads a workbook on its builder's computer): a table whose query or partition changes shows no data until it is refreshed.
2. Open it in Power BI Desktop. File > Save as, file type Power BI project (`.pbip`), into the root of your scratch clone. Close Desktop.
3. Do not import the theme and do not fix anything by hand: the test is what the flow finds and does.
4. Fill in two lines of `docs/report-brief.md`, and leave the rest empty:
   - Section 2: the page size of the report (an existing report keeps its size).
   - Section 3: `Other reports use this model (yes or no): no`. Nothing else reads this sample.
5. Commit everything.
6. Record the starting point, in a file **outside** the folder (a new file inside it would stop the first step):

```bash
python scripts/check_project.py . > ../before.txt
```

## Run

In VS Code, in the chat of your AI agent in agent mode, with the model you want to test, ask exactly:

> Evaluate and improve this report.

Then answer nothing until the final answer. The flow has no approvals. The one question it may ask, at the start, is the one the brief already answers.

At any time you can ask the script where the flow stands:

```bash
python scripts/improve.py next
```

## What to record

| What | Where to find it |
|---|---|
| The AI model and the date | the chat |
| Errors, warnings and notes at the start | the line of `before.txt` that starts with "Checked" (the last line, or the one before it when there are errors) |
| Pass, Fail and Not applicable before and after; how many Fail items only a person's fact can close | `python scripts/improve.py compare` |
| Rows in the plan by kind and by status | `python scripts/improve.py check-plan` |
| What was held, and why (nothing should be, with "no" in the brief) | the "Held:" lines of `compare` |
| The commits, one for each kind | `git log --oneline` |
| Every question the agent asked between its first step and its final answer (there should be none) | your notes |
| Every place where it guessed, skipped a step, needed a reminder, or handed work back to you that it could have done | your notes |
| What it looked up, and where | its answers: every address should be on Microsoft Learn, dax.guide or sqlbi.com |
| What looked different in Desktop, page by page | open `_before/` and the working project side by side |
| Each finding that was wrong (a false alarm), with the object | your notes; each one is a lesson for the template |

In Power BI Desktop also check these, because no document settles them: the report opens with the theme the script registered, and Desktop keeps it when you save; after one refresh every page shows its data; a measure named with `#` or `(%)` works; display folders written as `Subject\Type` show as two levels; any `CalculatedReason` annotation is still in the file after you save; the tab order and the phone layout of a page whose visuals moved.

## What a good result looks like

- A new branch `improve/<date>`; the branch you started on did not move; `_before/` opens in Desktop and is not in Git.
- The agent asked nothing after its first step, and waited for no approval.
- The review has all 79 rows and passes `python scripts/check_project.py --review docs/checklist-review.md`. Every "Not applicable" row quotes the checklist's own line for that item.
- The plan sorts every finding into a kind, and every row has a status. Notes whose codes start with U are listed as suggestions, not as fix rows.
- The theme is registered: `python scripts/check_project.py .` reports no T001, and the report's `StaticResources/RegisteredResources/` folder holds the theme file.
- Every measure is in `_Measures`, not one or two: no M001, no M002, and no M908 or B001 for a moved measure. The model has one measures table, and the agent did not ask you to do a move in Desktop.
- No row is held, and every row of the kind Data is done, in the last commit. The final answer starts by saying that the model must be refreshed once; after that refresh every page shows the same data as in `_before/`.
- A visual that uses drill-down, a help tooltip, a tooltip page or tooltip fields kept its header icons or its tooltip, with a row in section 7 of the brief.
- One commit for each kind that had rows, in this order: `Improve: theme`, `Improve: mechanical fixes`, `Improve: layout fixes`, `Improve: measures moved`, `Improve: renames`, `Improve: changes that need a refresh`. Undoing one with `git revert` leaves the others in place.
- Fewer Fail items after than before, and no item that went from Pass to Fail. `compare` says how many of the remaining Fail items wait for a fact from a person.
- `python scripts/check_project.py .` reports no G001 and no G002, and fewer errors than `before.txt`.
- Every description the agent wrote comes from the brief or is a `TODO(owner)` question. All questions come once, in the final answer, with rows that ask the same thing shown once.
- The agent named the pages to look at, and said plainly if a tool it may call was not set up or failed.
- `python scripts/check_template.py` still passes: the checklist and the theme are unchanged.

A sample report will not pass everything, and it should not: about twenty items rest on facts only its owner has (access, user testing, export tests, performance runs), and they stay Fail until someone answers. Expect many warnings from the standards on DAX style, alt text, titles and relationships: on a report nobody here built they are gaps for the review, not lessons.

## Afterwards

Add one row per run to the results log in `evals/prompts.md` (prompt id E15). For every wrong finding or missed step, tell the agent; it records a lesson (skill `pbi-lessons`), and a repeated lesson becomes a proposed change to the template.
