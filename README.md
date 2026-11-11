# Power BI + GitHub Copilot starter template

A starting point for building, evaluating and changing Power BI reports with GitHub Copilot in VS Code. It holds the instructions, skills, theme, checklist and check scripts that Copilot follows. It works with any AI model you pick in Copilot and holds no company data.

## What you need installed

| For | Install |
|---|---|
| Running the checks and tests | **Python 3.8 or later.** Nothing else: the scripts use only Python's standard library. No `pip install`. |
| Working with Copilot | VS Code with GitHub Copilot set up and signed in, used in agent mode. |
| Opening and saving reports | Power BI Desktop, saving in Power BI project format (PBIP), with the model as TMDL and the report as PBIR. |
| Version control | Git. |

If `python` is not found, use `py` (Windows) or `python3` (macOS, Linux) in the commands below.

## What is in the template

```
.github/copilot-instructions.md      rules Copilot always loads (short)
.github/instructions/                rules loaded when Copilot works on model files (*.tmdl) or report files (*.Report)
.github/skills/pbi-semantic-model/   model work: tables, measures, Power Query, descriptions; the model standard
.github/skills/pbi-report/           report work: pages, visuals, layout, labels, theme rules; the layout standard
.github/skills/pbi-checklist-review/ evaluation against the 79-item checklist
.github/skills/pbi-improve/          evaluate an existing report, then fix what was approved
.github/skills/business-definitions/ starter definitions for eight business areas, read one at a time
.github/skills/pbi-lessons/          the improvement loop: what Copilot does when it gets something wrong
checklist/checklist.md               the 79 checklist items, word for word
theme/theme.json                     the report theme, unchanged
docs/report-brief.md                 what you tell Copilot before it builds
docs/lessons.md                      each Copilot mistake, its correction, and where the fix went
scripts/                             machine checks, the fix tools, the flow tool and the lessons tool
tests/                               tests of the scripts, on made-up data
evals/prompts.md                     test prompts for the guidance (not yet run)
evals/first-test.md                  how to try the whole flow on one of Microsoft's sample reports
THIRD_PARTY_NOTICES.md               Microsoft's MIT notice for the rules and examples that follow its skills
```

Two of the eight business areas (reliability; energy and gas) apply to electric and gas utilities only.

Two words used below: an **annotation** is a name-and-value entry in a visual's `visual.json` file that Power BI Desktop ignores; a **label** is a readable name for a visual in the form `Page_Type_Subject`.

## 1. Create your repository

Create your own repository from this template and clone it. Keep the clone out of OneDrive and SharePoint folders. Do everything below in that clone. Open its root folder in VS Code (not a subfolder), so Copilot finds `.github`.

Power BI Desktop writes Windows line endings. Microsoft advises turning on Git's `autocrlf` setting to keep diffs clean.

## 2. Add a project

A repository holds one Power BI project. Use one of the two routes.

### Route A: a new report

Microsoft supports a theme file inside a project only after Power BI Desktop itself has registered it, so the starter project is made in Desktop, not by hand.

1. Open Power BI Desktop with a blank report. (For a report on a published model, connect the blank report to that model in Desktop first. Such a project has no `.SemanticModel` folder: skip step 2 and ignore the model parts below.)
2. Turn off Auto date/time for this file: File > Options and settings > Options, the Current File page, the Time intelligence section. Clear the option.
3. Apply the theme: Design ribbon > Import theme, and choose `theme/theme.json` from your clone.
4. Make the measures table. The model standard keeps every measure in one table named `_Measures`, made the way Microsoft Learn describes:
   - Home ribbon > Enter data. Keep the one column, name the table `_Measures`, and select Load.
   - In Model view, hide that column (right-click > Hide in report view). Do not hide the table.
   - Create measures there, or move one there with its Home table setting. The table then shows at the top of the Data pane.
   - A Direct Lake model: make `_Measures` as a calculated table instead (New table, with a formula that names no other table), because an entered table is an imported table. Tell Copilot why, so it can write the reason line the standard asks for.
   - A report on a published model has no model here: skip this step.
5. Save: File > Save as, choose the Power BI project file type (`.pbip`), name it `Starter` (or the report's name), and save it in the root folder of your clone.
6. Close Power BI Desktop and check the result:

```bash
python scripts/check_project.py .
```

```bash
python scripts/check_template.py
```

The second command confirms that the theme copy Desktop registered has the same content as `theme/theme.json`.

7. Commit the `.pbip` file and the `.Report` and `.SemanticModel` folders.

You should see a `definition` folder inside the `.SemanticModel` folder (TMDL files) and inside the `.Report` folder (PBIR files). If you see `model.bim` or a single `report.json` there instead, your Desktop is saving an older format, and `scripts/check_project.py` will say so. Microsoft documents PBIR as the default report format in current Power BI Desktop, so update Desktop and save again.

The first page has a generated 20-character name. Leave it; it is not shown to report readers.

**Give Copilot something to follow.** Copilot is told never to write Power BI file syntax from memory. It follows what is already in the project. In a blank project there is nothing to follow, so before you ask Copilot to build, make these in Desktop and save: one table loaded from your source, the `_Measures` table from step 4, one relationship if the model needs any, and one visual of each type you plan to use. Copilot then extends them: more tables, measures, descriptions, pages and visuals.

Visuals you make in Desktop count as existing visuals: run steps 4 and 5 of Route B on them, now and whenever you add a visual in Desktop later.

### Route B: an existing report

For an evaluation only, steps 1 and 3 are enough: the later steps change the report.

1. Get it into project format. A `.pbix` file: open it in Power BI Desktop and use File > Save as with the Power BI project file type, saving into the root of your clone. A project that already exists: copy its `.pbip` file and its `.Report` and `.SemanticModel` folders into the root. Commit.
2. Apply the theme in Power BI Desktop: Design ribbon > Import theme, choose `theme/theme.json`, then save and close. Microsoft notes that importing a custom theme removes customizations already added to the report.
3. Confirm the theme and see where the project stands:

```bash
python scripts/check_template.py
```

```bash
python scripts/check_project.py .
```

4. Set Header icons off and Tooltips off on every existing visual. Look first, then apply. The script changes only these two settings, but writes each changed file again as a whole, so commit before running it:

```bash
python scripts/set_visual_defaults.py . --dry-run
```

```bash
python scripts/set_visual_defaults.py .
```

5. Give existing visuals their labels. Existing visuals are not renamed; each gets a `VisualLabel` annotation instead. List what is there, agree the labels, then apply them. Copilot can do this with you ("Label the existing visuals"), or you can run it yourself, using the page folder and the visual folder that the list shows. The `Page` part of a label is the page's name, or its tab name without spaces or punctuation (the tab "Sales Detail" gives `SalesDetail_...`). A run with `--label` also sets Header icons off and Tooltips off, as in step 4:

```bash
python scripts/list_visuals.py .
```

```bash
python scripts/set_visual_defaults.py . --label "<page folder>/<visual folder>=<Page_Type_Subject>"
```

To see which visual a 20-character folder name belongs to, compare its type and position in the list with the page in Desktop.

6. Reload in Desktop and open one changed visual of each kind to confirm it looks as before.

## 3. Work with Copilot

Fill in `docs/report-brief.md` first. Then ask Copilot in agent mode.

| Job | Ask Copilot something like | What happens |
|---|---|---|
| Build new | "Add a page that shows sales by month" | Copilot follows the model and report skills, gives new visuals a `Page_Type_Subject` name, and runs the checks |
| Evaluate | "Evaluate this report against the checklist" | Copilot runs every check and gives Pass, Fail or Not applicable for all 79 items in a new file, `docs/checklist-review.md`. It changes nothing else |
| Evaluate and improve | "Evaluate and improve this report" | Copilot makes a branch and an untouched copy, evaluates, writes a fix plan, stops for your approval, applies what you approved in two commits, evaluates again and shows the counts before and after. See section 5 |
| Change existing | "Add descriptions to the Sales table" or "Move the slicers to the top" | Copilot edits pages, visuals, measures and descriptions, and does not rename what already exists |

After Copilot edits files, reload in Power BI Desktop and look at the result (see "Reloading in Desktop").

Where each case is covered:

| Case | README | Copilot guidance | Scripts |
|---|---|---|---|
| New report on a new model | Section 2, Route A; then "Build new" above | `pbi-semantic-model` ("New model, or new objects in a model"), then `pbi-report` ("New page or new visual", "Layout"); both instruction files | `check_project.py` after every change; `check_template.py` once the project is saved; `list_visuals.py` |
| New report on an existing model | A published model: Section 2, Route A, step 1. A model that is already a project: Route B, then add pages to its report | `pbi-report` ("Before you change anything", step 3, finds the model; then "New page or new visual"); `pbi-semantic-model` ("Existing model") for added measures | `check_project.py`, `list_visuals.py` |
| Evaluate an existing report and model | Section 2, Route B, steps 1 and 3; then "Evaluate" above | `pbi-checklist-review` (all of it) | `check_project.py`, `check_template.py`, `list_visuals.py`, `check_project.py --review` |
| Modify an existing report and model | Section 2, Route B; then "Change existing" above | `pbi-report` ("Existing report", "Layout"), `pbi-semantic-model` ("Existing model"), and the rename rule in the project instructions | `set_visual_defaults.py`, `set_model_properties.py`, `set_positions.py`, `list_visuals.py`, `check_project.py` |
| Evaluate an existing report and model, then improve it | Section 2, Route B, steps 1 to 3; then section 5 | `pbi-improve` (all of it), which uses the three skills above | `improve.py`, and every script above |

Not covered: making a second report folder beside an existing one in the same project. Do that in Power BI Desktop.

## 4. The improvement loop

The template learns from Copilot's mistakes. `docs/lessons.md` records each mistake, its correction, and where the fix went.

**What starts it**

- You point out a problem ("that is wrong", "this should be...").
- A check fails on something Copilot created or changed. When `scripts/check_project.py` finds errors, its last line tells Copilot to record a lesson for each finding code. The checks of the model standard, the layout standard and field references (codes that start with M, G and B) count like any other. A warning or a note does not start the loop.

Both triggers work through Copilot's guidance; no script records a lesson by itself.

**What Copilot then does** (skill `pbi-lessons`)

1. Puts the mistake right in the report or model.
2. Records one lesson with `python scripts/lessons.py add`. Lessons of the same kind share a key: the finding code for a failed check (for example `D001`), or a short name.
3. When the same key comes back, the lesson must be built into the template: a new script check with a test where a script can catch the mistake, otherwise one line in the right skill or instruction file. If the mistake returns twice more after that, the loop starts again.
4. Copilot always asks before changing any template file. It shows you the exact change and waits for a clear yes. It then makes the change on a new branch; you open the pull request, and merging it is the approval. If you say no, the lesson is recorded as declined.

Template files are everything under `.github/`, `scripts/`, `tests/` and `evals/`, and the root files `README.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, `.gitignore` and `.gitattributes`. The brief and the lessons file are your project's own content.

The model standard, the layout standard, their checks, the fix scripts and the skill `pbi-improve` are template files too, so they are inside the loop. A lesson may propose a change to any of them. Copilot always asks first, and a person approves by pull request.

**What can never happen this way**

- `checklist/checklist.md` and `theme/theme.json` are never changed through a lesson. They stay outside the loop; nothing in this template changes them.
- No check is loosened or removed, and no rule softened, to make something pass.
- Old lessons are not edited or deleted.

The script enforces what it can:

```bash
python scripts/lessons.py check
```

It fails when a lesson is badly formed, when a fix points at the checklist or the theme, when a template change has no pull request number or address, or when a mistake has come back and has been neither built into the template nor declined. `python scripts/check_template.py` runs the same check. A script cannot check that Copilot asked first, or that nobody reworded or removed the newest lessons; the pull request diff is the safeguard for both.

## 5. Evaluate and improve an existing report

One request, such as "Evaluate and improve this report", runs these steps in order (skill `pbi-improve`). Copilot does not have to remember them: `python scripts/improve.py next` reads the files and Git and says which step comes next.

1. **Safety first.** Save in Power BI Desktop and commit. `python scripts/improve.py start` stops unless everything is committed and no earlier flow left its files behind. It makes a new branch, and copies the project unchanged into the folder `_before/`, so you can open before and after side by side. Git ignores that folder and the checks skip it.
2. **Evaluate.** The checklist review writes `docs/checklist-review.md`.
3. **Fix plan.** `docs/fix-plan.md` lists every finding and every failed item as Mechanical (descriptions, format strings, folders, hiding, header icons and tooltips), Layout (positions and sizes, by the numbers of the layout standard) or Needs a person (access, user testing, export tests, performance runs, renames and moves, data types, summarisation, and anything a file cannot settle). Each row says what will change, which files, and what could break.
4. **Stop.** You approve all of it, one kind, or single rows. Nothing changes before that, and only a plain yes counts: Copilot writes yes or no in every row, and the script will not go on while a row has no answer or a doubtful one.
5. **Mechanical fixes**, then the checks, then one commit. **Layout fixes**, then the checks, then a second commit. Each commit can be undone alone.
6. **Evaluate again.** `python scripts/improve.py compare` prints Pass, Fail and Not applicable before and after, the pages to reload and look at in Power BI Desktop, and the rows that need a person.

Never in this flow: a rename or a move without your yes, a change to the checklist, the theme or a template file, publishing, deploying or merging.

Why the copy is safe: the `.pbip` file points to the report folder, and the report points to the model, both by relative path, so the three are copied together with their names unchanged and nothing inside is edited. Each `.platform` file holds an identifier that must stay unique within a Git branch, which is why the copy is never committed. If Git would not ignore `_before/`, or a path would pass 260 characters, the script makes no copy, says so, and the branch is the safeguard.

To try the flow end to end, see `evals/first-test.md`.

## The rules the checks enforce

`scripts/check_project.py` enforces these. Errors change its exit code; warnings and notes do not. It cannot tell a new visual from an existing one, or check that a header or tooltip exception is listed in the brief; people and the review do that.

- Every visible table, column and measure has a `///` description directly above it; so does every shared query and parameter. Unknown meaning becomes `/// TODO(owner): question`, which the check lists.
- `//` comments appear only inside Power Query (M) or DAX expressions.
- Every Power Query step has a `//` comment line above it describing it (a `/* */` comment also counts). This, and using `///` for a query's description, is a convention of this template: Microsoft does not document how Desktop stores query and step descriptions in project files.
- Page and visual names use only letters, digits, underscore and hyphen, and are at most 50 characters.
- Every visual has a `Page_Type_Subject` name, or a `VisualLabel` annotation carrying one.
- Every visual has Header icons off and Tooltips off set on the visual itself, as well as in the theme. A visual that must keep one on carries a `HeaderTooltipException` annotation that says what stays on and why (and is listed in section 7 of the brief).
- A custom theme is registered in the report.
- The model standard (`.github/skills/pbi-semantic-model/references/model-standard.md`). Errors: a measure outside the table `_Measures`; a measure without a display folder of exactly two levels, `Subject\Type`; a duplicate, code-style or column-like measure name; a visible measure without a format string; a calculated column or table without its `CalculatedReason` annotation; a visible number column that still totals by default; relationship columns of different types. Warnings: name details, DAX reference style, column folders, keys left visible, the floating-point type, date with time, missing column formats.
- The layout standard (`.github/skills/pbi-report/references/layout-standard.md`). Errors: a visual outside its page; two data visuals that overlap. Warnings: positions off the 8-pixel grid, margins, gaps, row heights, page size.
- No report file names a table, column or measure that the model in the project does not have.

For the model, layout and field checks, an exception counts only when section 9 or 10 of `docs/report-brief.md` lists the same code and object with a reason. The script reads the brief; it also takes the page size, margin, gap, grid step, folder subjects and the two optional checks (Excel, Copilot in Power BI) from there.

## Running the checks

```bash
python scripts/check_project.py .
```

Checks every project under the folder. Exit code 0 means no errors, 1 means errors, 2 means nothing was found to check. Each line starts with a code (for example `D001`); the list of codes is at the top of the script.

```bash
python scripts/list_visuals.py . --page Overview
```

Lists label, type, x, y, width, height and folder of each visual on one page. Leave out `--page` for every page.

```bash
python scripts/set_model_properties.py . --dry-run --set "Sales[Amount].isHidden=true"
```

Sets one property of one model object: display folder, format string, hidden, summarisation off, or the reason line of a calculated object. It changes that one line and nothing else, and never chooses a value itself. Leave out `--dry-run` to apply.

```bash
python scripts/set_positions.py . --dry-run --move "Overview/Overview_Card_TotalSales=24,24,608,120"
```

Writes an approved position and size. It refuses groups, visuals inside a group, rotated visuals and anything that would leave the page, and it names the pages to look at afterwards.

```bash
python scripts/improve.py next
```

Says which step of the evaluate-and-improve flow comes next (section 5).

```bash
python scripts/check_project.py --review docs/checklist-review.md
```

Checks that a finished review has all 79 rows, an allowed status and evidence in each. The file does not exist until an evaluation has been run.

```bash
python scripts/check_template.py --xlsx "path/to/PowerBI_Modeling_Full_Checklist_Guide.xlsx"
```

Checks the template itself, and that the theme registered in the project is `theme/theme.json`. With `--xlsx` it also compares the checklist, cell by cell, with the original spreadsheet. The spreadsheet is not kept in this repository; pass the path to your copy. Without `--xlsx` it still detects any edit to the checklist or the theme.

```bash
python -m unittest discover -s tests -v
```

Runs the tests of the scripts: each check is shown to fail on a broken example and pass on a correct one.

```bash
python scripts/lessons.py check
```

Checks the lessons file (see "The improvement loop").

## Reloading in Desktop

Save in Power BI Desktop before Copilot edits files. After the edit, either:

- close and reopen the project in Power BI Desktop; or
- if you use Power BI Desktop from August 2026 or later, turn on the preview feature "Detect and reload external PBIP changes" (File > Options and settings > Options > Preview features), restart Desktop once, and from then on select "Apply external changes" in the banner that appears.

Header icons always show while you edit. Microsoft applies the "off" setting only in reading view, so check it in a published report.

## The theme and the checklist are fixed

`theme/theme.json` and `checklist/checklist.md` must not be edited. `scripts/check_template.py` fails if either changes. If the owner replaces one on purpose, update the matching hash at the top of that script.

What the theme means for drill, tooltips, export, contrast and text size is set out in `.github/skills/pbi-report/references/theme.md`.

## Not tested, and not confirmed

- Copilot prompt tests have not been run. Steps are in `evals/prompts.md`.
- Nothing here has been opened in Power BI Desktop by the template's builder. Check the starter project and one changed visual in Desktop before relying on the template.
- Not confirmed from Microsoft's documentation: how Desktop stores Power Query query and step descriptions; whether Desktop keeps annotations when it saves; what "Tooltips off" does to report-page tooltips; whether right-click drill and "Export data" still work in reading view when header icons are off; where the Selection pane name of a single visual is stored.
- The visual-level "Header icons off, Tooltips off" entries: Microsoft's schema defines where they go and what they are called, for every visual type, but not how the value is written; the written form follows Microsoft's own examples. Not confirmed: whether Desktop keeps and applies them on text boxes, shapes, images and buttons, and whether adding them changes a visual's padding (Microsoft's report skill warns that it can).
- The scripts were run on Linux with Python 3.13. They use nothing newer than Python 3.8, but were not run on Windows or on 3.8.
- The Power Query step check is a plain text check of each query's outer `let`. Unusual layouts can escape it.
- The DAX checks (reference style, columns a measure totals, unused hidden objects) read text. They are not a DAX parser.
- Not confirmed from Microsoft's documentation, for the standards and the flow: whether Power BI Desktop accepts the measure names `# Orders` and `Gross Margin (%)` (Microsoft's "DAX syntax" page lists `%` and brackets as not valid in names; against that, Microsoft's TMDL overview shows such names, Microsoft's own saved projects hold measure names with `%` and brackets, and `#` is not on the list); whether Desktop keeps a `CalculatedReason` annotation when it saves; whether a group member's position counts from the page or from its group (so the scripts never move groups or their members); whether Desktop repairs visuals when a measure's table changes in the files (so measures are moved in Desktop only); what turning summarisation off does to visuals that already total the column (so it is never a mechanical fix); whether a phone layout made automatically changes when desktop positions change.
- Check once in Power BI Desktop, in this order: (1) measures named `# Orders` and `Gross Margin (%)` load and work in a visual; (2) a `_Measures` table made with Enter data shows at the top of the Data pane, and a display folder written as `Finance\Base` shows as two levels; (3) a `CalculatedReason` annotation is still in the file after Desktop saves; (4) a copy in `_before/` opens beside the working project; (5) one page after a layout fix, including its tab order and phone layout.

## Acknowledgements

Some working practices in this template were informed by Kurt Buhler's public writing and repository on agentic Power BI development (`data-goblin/power-bi-agentic-development`) and by the Tabular Editor blog: short always-loaded guidance, detail loaded on demand, hard rules enforced by scripts, a written brief before building. Several rules of the model standard and the layout standard also started as ideas there: a measures table, the order of a measure name, column folders, what to hide, a recorded reason for calculated objects, equal margins and gaps. These are ideas only. No text, code or files were taken from them, and the `pbir` command-line tool (authors: Kurt Buhler, Maxim Anatsko) is not used.

The two standards also follow Microsoft's best practice rules for tabular models (`microsoft/Analysis-Services`), Microsoft's skills for Fabric and GitHub's `awesome-copilot` modeling skill; each standard file names its sources. File-format facts come from Microsoft's published documentation, schemas and skills; see `THIRD_PARTY_NOTICES.md` for Microsoft's notice.

## Licence

MIT. See `LICENSE`.
