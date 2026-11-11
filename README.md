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
.github/skills/pbi-semantic-model/   model work: tables, measures, Power Query, descriptions
.github/skills/pbi-report/           report work: pages, visuals, layout, labels, theme rules
.github/skills/pbi-checklist-review/ evaluation against the 79-item checklist
.github/skills/business-definitions/ starter definitions for eight business areas, read one at a time
.github/skills/pbi-lessons/          the improvement loop: what Copilot does when it gets something wrong
checklist/checklist.md               the 79 checklist items, word for word
theme/theme.json                     the report theme, unchanged
docs/report-brief.md                 what you tell Copilot before it builds
docs/lessons.md                      each Copilot mistake, its correction, and where the fix went
scripts/                             machine checks, two visual tools, and the lessons tool
tests/                               tests of the checks, on made-up data
evals/prompts.md                     test prompts for the guidance (not yet run)
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
4. Save: File > Save as, choose the Power BI project file type (`.pbip`), name it `Starter` (or the report's name), and save it in the root folder of your clone.
5. Close Power BI Desktop and check the result:

```bash
python scripts/check_project.py .
```

```bash
python scripts/check_template.py
```

The second command confirms that the theme copy Desktop registered has the same content as `theme/theme.json`.

6. Commit the `.pbip` file and the `.Report` and `.SemanticModel` folders.

You should see a `definition` folder inside the `.SemanticModel` folder (TMDL files) and inside the `.Report` folder (PBIR files). If you see `model.bim` or a single `report.json` there instead, your Desktop is saving an older format, and `scripts/check_project.py` will say so. Microsoft documents PBIR as the default report format in current Power BI Desktop, so update Desktop and save again.

The first page has a generated 20-character name. Leave it; it is not shown to report readers.

**Give Copilot something to follow.** Copilot is told never to write Power BI file syntax from memory. It follows what is already in the project. In a blank project there is nothing to follow, so before you ask Copilot to build, make these in Desktop and save: one table loaded from your source, one relationship if the model needs any, and one visual of each type you plan to use. Copilot then extends them: more tables, measures, descriptions, pages and visuals.

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
| Change existing | "Add descriptions to the Sales table" or "Move the slicers to the top" | Copilot edits pages, visuals, measures and descriptions, and does not rename what already exists |

After Copilot edits files, reload in Power BI Desktop and look at the result (see "Reloading in Desktop").

Where each case is covered:

| Case | README | Copilot guidance | Scripts |
|---|---|---|---|
| New report on a new model | Section 2, Route A; then "Build new" above | `pbi-semantic-model` ("New model, or new objects in a model"), then `pbi-report` ("New page or new visual", "Layout"); both instruction files | `check_project.py` after every change; `check_template.py` once the project is saved; `list_visuals.py` |
| New report on an existing model | A published model: Section 2, Route A, step 1. A model that is already a project: Route B, then add pages to its report | `pbi-report` ("Before you change anything", step 3, finds the model; then "New page or new visual"); `pbi-semantic-model` ("Existing model") for added measures | `check_project.py`, `list_visuals.py` |
| Evaluate an existing report and model | Section 2, Route B, steps 1 and 3; then "Evaluate" above | `pbi-checklist-review` (all of it) | `check_project.py`, `check_template.py`, `list_visuals.py`, `check_project.py --review` |
| Modify an existing report and model | Section 2, Route B; then "Change existing" above | `pbi-report` ("Existing report", "Layout"), `pbi-semantic-model` ("Existing model"), and the rename rule in the project instructions | `set_visual_defaults.py`, `list_visuals.py`, `check_project.py` |

Not covered: making a second report folder beside an existing one in the same project. Do that in Power BI Desktop.

## 4. The improvement loop

The template learns from Copilot's mistakes. `docs/lessons.md` records each mistake, its correction, and where the fix went.

**What starts it**

- You point out a problem ("that is wrong", "this should be...").
- A check fails on something Copilot created or changed. When `scripts/check_project.py` finds errors, its last line tells Copilot to record a lesson for each finding code.

Both triggers work through Copilot's guidance; no script records a lesson by itself.

**What Copilot then does** (skill `pbi-lessons`)

1. Puts the mistake right in the report or model.
2. Records one lesson with `python scripts/lessons.py add`. Lessons of the same kind share a key: the finding code for a failed check (for example `D001`), or a short name.
3. When the same key comes back, the lesson must be built into the template: a new script check with a test where a script can catch the mistake, otherwise one line in the right skill or instruction file. If the mistake returns twice more after that, the loop starts again.
4. Copilot always asks before changing any template file. It shows you the exact change and waits for a clear yes. It then makes the change on a new branch; you open the pull request, and merging it is the approval. If you say no, the lesson is recorded as declined.

Template files are everything under `.github/`, `scripts/`, `tests/` and `evals/`, and the root files `README.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, `.gitignore` and `.gitattributes`. The brief and the lessons file are your project's own content.

**What can never happen this way**

- `checklist/checklist.md` and `theme/theme.json` are never changed through a lesson.
- No check is loosened or removed, and no rule softened, to make something pass.
- Old lessons are not edited or deleted.

The script enforces what it can:

```bash
python scripts/lessons.py check
```

It fails when a lesson is badly formed, when a fix points at the checklist or the theme, when a template change has no pull request number or address, or when a mistake has come back and has been neither built into the template nor declined. `python scripts/check_template.py` runs the same check. A script cannot check that Copilot asked first, or that nobody reworded or removed the newest lessons; the pull request diff is the safeguard for both.

## The rules the checks enforce

`scripts/check_project.py` enforces these. It cannot tell a new visual from an existing one, or check that an exception is listed in the brief; people and the review do that.

- Every visible table, column and measure has a `///` description directly above it; so does every shared query and parameter. Unknown meaning becomes `/// TODO(owner): question`, which the check lists.
- `//` comments appear only inside Power Query (M) or DAX expressions.
- Every Power Query step has a `//` comment line above it describing it (a `/* */` comment also counts). This, and using `///` for a query's description, is a convention of this template: Microsoft does not document how Desktop stores query and step descriptions in project files.
- Page and visual names use only letters, digits, underscore and hyphen, and are at most 50 characters.
- Every visual has a `Page_Type_Subject` name, or a `VisualLabel` annotation carrying one.
- Every visual has Header icons off and Tooltips off set on the visual itself, as well as in the theme. A visual that must keep one on carries a `HeaderTooltipException` annotation that says what stays on and why (and is listed in section 7 of the brief).
- A custom theme is registered in the report.

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

## Acknowledgements

Some working practices in this template were informed by Kurt Buhler's public writing and repository on agentic Power BI development (`data-goblin/power-bi-agentic-development`) and by the Tabular Editor blog: short always-loaded guidance, detail loaded on demand, hard rules enforced by scripts, a written brief before building. These are ideas only. No text, code or files were taken from them, and the `pbir` command-line tool (authors: Kurt Buhler, Maxim Anatsko) is not used. File-format facts come from Microsoft's published documentation, schemas and skills; see `THIRD_PARTY_NOTICES.md` for Microsoft's notice.

## Licence

MIT. See `LICENSE`.
