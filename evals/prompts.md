# Test prompts for the Copilot guidance

Status: **not tested**. GitHub Copilot could not be reached from the environment where this template was built. The steps below let you run the tests yourself. The check scripts are tested separately (`python -m unittest discover -s tests -v`).

## How to run one test

1. Make a scratch branch. Copy the folder `tests/fixtures/good` to the repository root as your starting project (it is made-up data), and commit, so every run starts from the same files. While that copy is in the root, `python scripts/check_template.py` reports a theme difference, because the made-up project registers a stub theme; that is expected on the scratch branch.
2. In VS Code open the repository root. Open Copilot Chat in agent mode and pick the model you want to test.
3. Check that the guidance is found: the five skills and the instruction files should be listed in the Agent Customizations editor without errors.
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
| E4 | pbi-report | Add a second card, showing Return Rate, to the Overview page, to the right of the existing card. | New folder and `name` are the same `Overview_<Type>_<Subject>` label. Header icons and Tooltips are off on the visual. Position does not overlap other visuals. Existing visuals are not renamed. No errors from the check. |
| E5 | pbi-report | Turn on tooltips for the sales by month chart. | Copilot checks section 7 of the brief, asks for the reason because the chart is not listed, adds the row, turns on only Tooltips, and adds a `HeaderTooltipException` annotation starting with `tooltip:`. Header icons stay off. The visual is not renamed. |
| E6 | pbi-checklist-review | Evaluate this report and model against the checklist and tell me the gaps. | No project file was changed. `docs/checklist-review.md` has 79 rows, each Pass, Fail or Not applicable with evidence, and passes `python scripts/check_project.py --review docs/checklist-review.md`. Item 23 is Fail because of the placeholder on the Returned column. |
| E7 | business-definitions | We need a turnover rate measure for an HR page. What definition should I use? | Copilot reads only the workforce file, presents the row as a starter, names its source, and asks you to confirm the company's definition before building anything. |
| E8 | (always-on rules) | Rename the sales by month chart to Overview_Bar_Sales. | Copilot renames nothing yet. It says what a rename may break, offers to change the chart's `VisualLabel` annotation instead, and renames only after you answer with a clear yes. |
| E9 | pbi-lessons | First: "Add a measure called Order Count to the Sales table." Then, whatever format Copilot chose: "Counts are always shown with a thousands separator and no decimals." | Copilot corrects the format string, then adds one row to `docs/lessons.md` with trigger `developer`. No template file is changed. `python scripts/lessons.py check` passes. |
| E10 | pbi-lessons | Run E9 a second time in a new chat. Reset the project files but keep `docs/lessons.md` from E9. | Copilot reuses the key from the first lesson, says the mistake has come back, proposes one exact change to a skill, an instruction file or a script, and asks before making it. It does not touch `checklist/checklist.md` or `theme/theme.json`. |
| E11 | pbi-lessons | By hand, delete the `///` line above the Amount column in Sales.tmdl. Then: "Run the project check and deal with what it finds." | Copilot treats the missing description as a gap that was already there, not as its own mistake: it asks for the meaning or writes a `TODO(owner)` placeholder, and records no lesson. |

## Results log

Add one row per run. Always record the model.

| Date | Model | Prompt id | With skill? | Run no. | Pass or fail | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |
