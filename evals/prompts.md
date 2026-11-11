# Test prompts for the Copilot guidance

Status: **not tested**. GitHub Copilot could not be reached from the environment where this template was built. The steps below let you run the tests yourself. The check scripts are tested separately (`python -m unittest discover -s tests -v`).

## How to run one test

1. Make a scratch branch. Copy the folder `tests/fixtures/good` to the repository root as your starting project (it is made-up data), and commit, so every run starts from the same files. While that copy is in the root, `python scripts/check_template.py` reports a theme difference, because the made-up project registers a stub theme; that is expected on the scratch branch.
2. In VS Code open the repository root. Open Copilot Chat in agent mode and pick the model you want to test.
3. Check that the guidance is found: the six skills and the instruction files should be listed in the Agent Customizations editor without errors.
4. Start a new chat. Paste the prompt exactly. Do not repeat any rule from the guidance in your prompt.
5. When Copilot finishes, judge the result against the pass criteria. They are fixed in advance; do not adjust them after seeing the result.
6. Add a row to the results log. Reset the files (`git checkout . && git clean -fd`) before the next run.
7. Optional comparison without a skill: move that skill's folder out of `.github/skills/` on the scratch branch, restart the chat, and run the same prompt with the same model. A skill that makes no difference to the result should be rewritten or removed.
8. Repeat for each model the team uses, and again after any change to the guidance.

## Prompts and pass criteria

| Id | Skill | Prompt | Pass when all of these are true |
|---|---|---|---|
| E1 | pbi-semantic-model | Add a measure called Average Order Value to the Sales table. | The measure has a `///` line above it. Its description is a `TODO(owner)` question or Copilot asked you for the meaning; no business meaning was made up. `python scripts/check_project.py .` reports no errors. |
| E2 | pbi-semantic-model | Add a short note in Sales.tmdl explaining that OrderId is a technical key. | The note is a `///` description or an in-expression comment, not a `//` line outside an expression. OrderId is still hidden. No errors from the check. |
| E3 | pbi-semantic-model | Add a step to the Sales query that removes orders with a zero amount. | The new step has a clear name and a `//` line above it. No errors from the check. |
| E4 | pbi-report | Add a second card, showing Return Rate, to the Overview page, to the right of the existing card. | New folder and `name` are the same `Overview_<Type>_<Subject>` label. Header icons and Tooltips are off on the visual. Position is x 648, y 24, width 608, height 120 (one 16-pixel gap from the card, same height, right edge at the 24-pixel margin), and Copilot showed the sums. Existing visuals are not renamed. No errors and no warnings from the check. Copilot names the Overview page to reload and look at. |
| E5 | pbi-report | Turn on tooltips for the sales by month chart. | Copilot checks section 7 of the brief, asks for the reason because the chart is not listed, adds the row, turns on only Tooltips, and adds a `HeaderTooltipException` annotation starting with `tooltip:`. Header icons stay off. The visual is not renamed. |
| E6 | pbi-checklist-review | Evaluate this report and model against the checklist and tell me the gaps. | No project file was changed. `docs/checklist-review.md` has 79 rows, each Pass, Fail or Not applicable with evidence, and passes `python scripts/check_project.py --review docs/checklist-review.md`. Item 23 is Fail because of the placeholder on the Returned column. |
| E7 | business-definitions | We need a turnover rate measure for an HR page. What definition should I use? | Copilot reads only the workforce file, presents the row as a starter, names its source, and asks you to confirm the company's definition before building anything. |
| E8 | (always-on rules) | Rename the sales by month chart to Overview_Bar_Sales. | Copilot renames nothing yet. It says what a rename may break, offers to change the chart's `VisualLabel` annotation instead, and renames only after you answer with a clear yes. |
| E9 | pbi-lessons | First: "Add a measure called Order Count to the Sales table." Then, whatever format Copilot chose: "Counts are always shown with a thousands separator and no decimals." | Copilot corrects the format string, then adds one row to `docs/lessons.md` with trigger `developer`. No template file is changed. `python scripts/lessons.py check` passes. |
| E10 | pbi-lessons | Run E9 a second time in a new chat. Reset the project files but keep `docs/lessons.md` from E9. | Copilot reuses the key from the first lesson, says the mistake has come back, proposes one exact change to a skill, an instruction file or a script, and asks before making it. It does not touch `checklist/checklist.md` or `theme/theme.json`. |
| E11 | pbi-lessons | By hand, delete the `///` line above the Amount column in Sales.tmdl. Then: "Run the project check and deal with what it finds." | Copilot treats the missing description as a gap that was already there, not as its own mistake: it asks for the meaning or writes a `TODO(owner)` placeholder, and records no lesson. |
| E12 | pbi-semantic-model | Add a measure called avg_order_value to the Sales table. | The measure is made in `_Measures`, not in Sales, and Copilot says why. Copilot proposes a business name such as Average Order Value, or asks; the code-style name is not used. The measure has a display folder of two levels from the lists, a format string, and a `///` description or a `TODO(owner)` question. No errors from the check. |
| E13 | pbi-semantic-model | Add a calculated column to Sales that flags orders over 100. | Copilot asks why the flag cannot come from the source or be a measure, or says so before building. If the column is made, it carries a `CalculatedReason` annotation in your words, not an invented reason. No errors from the check. |
| E14 | pbi-report | By hand, set the card's x to 27 and its width to 590, and commit. Then: "Tidy the layout of the Overview page." | Copilot reads the layout standard, shows old and new numbers with the sums, and waits for a yes. It runs `scripts/set_positions.py` with `--dry-run` first. The group is not moved. Afterwards the check gives no G finding, and Copilot names the Overview page to reload and look at. |
| E15 | pbi-improve | By hand, remove `displayFolder` from the Total Sales measure, remove `visualContainerObjects` from the card, set the card's x to 27, and commit. Then: "Evaluate and improve this report." | A new branch `improve/<date>` exists and the old branch did not move. `_before/` holds the untouched project and is not committed. `docs/checklist-review.md` and `docs/fix-plan.md` exist; the plan has the three kinds and passes `python scripts/improve.py check-plan`. Copilot stops and changes no project file before you approve. After "approve everything": two commits, `Improve: mechanical fixes` then `Improve: layout fixes`; the checks pass; Copilot shows the output of `python scripts/improve.py compare`, names the pages to look at and lists what needs a person. Nothing is merged, published or deployed. `checklist/checklist.md` and `theme/theme.json` are unchanged. |
| E16 | pbi-improve | Run E15 again, but at the approval step answer: "Only the layout rows." | Only layout rows are applied. There is one commit, `Improve: layout fixes`. The measure still has no display folder, and the final summary says so. |
| E17 | (always-on rules) | By hand, move the Total Sales measure from `_Measures.tmdl` to `Sales.tmdl`, and commit. Then: "Move all measures into the _Measures table." | Copilot edits no file. It says what a move can break (formulas that name the measure with its table, visuals in this report, other reports on a published model), and asks you to move the measure in Power BI Desktop with its Home table setting. It offers to run the check afterwards. |
| E18 | pbi-semantic-model | Turn off summarisation on every column and change Amount to a whole number. | Copilot does neither on its own. It says that Microsoft does not document what turning summarisation off does to visuals that already total a column, and that a type change alters stored values; it asks for your decision on each. |

## Results log

Add one row per run. Always record the model.

| Date | Model | Prompt id | With skill? | Run no. | Pass or fail | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |
