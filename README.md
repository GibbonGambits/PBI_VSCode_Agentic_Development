# Power BI + GitHub Copilot starter template

A starting point for building, evaluating and changing Power BI reports with GitHub Copilot in VS Code. It holds the instructions, skills, standards, shipped examples, theme, checklist and check scripts that Copilot follows. Copilot builds things itself: it copies a shipped example, runs the checks, and asks you only for what no file can tell it. It works with any AI model you pick in Copilot and holds no company data.

## What you need installed

| For | Install |
|---|---|
| Running the checks and tests | **Python 3.8 or later.** Nothing else: the scripts use only Python's standard library. No `pip install`. |
| Working with Copilot | VS Code with GitHub Copilot set up and signed in, used in agent mode. |
| Opening and looking at reports | Power BI Desktop, saving in Power BI project format (PBIP), with the model as TMDL and the report as PBIR. |
| Optional: Copilot reloads and looks at pages itself | Microsoft's Desktop Bridge tools (Windows, Power BI Desktop of June 2026 or later). See "Optional tools from Microsoft". |
| Optional: Copilot reads facts about the data itself | Microsoft's Power BI Authoring MCP Server, the local one. See "Optional tools from Microsoft". |
| Version control | Git. |

If `python` is not found, use `py` (Windows) or `python3` (macOS, Linux) in the commands below.

## What is in the template

```
.github/copilot-instructions.md      rules Copilot always loads (short)
the root instruction file           for an agent that reads a root instruction file in place of .github/: it loads
                                     those same rules. The settings file in the hidden folder beside it lists what
                                     that agent may run without asking: the scripts, the tests, and Git status, diff,
                                     log, add and commit. Pushing is refused
.github/instructions/                rules loaded when Copilot works on model files (*.tmdl) or report files (*.Report)
.github/skills/pbi-semantic-model/   model work, and the model standards: measures, relationships and dates, DAX,
                                     Power Query, storage modes and security, model objects, the DAX function index
.github/skills/pbi-report/           report work, and the report standards: layout, report features, theme rules
.github/skills/pbi-checklist-review/ evaluation against the 79-item checklist; the list of native features to suggest
.github/skills/pbi-improve/          evaluate an existing report, then fix it without waiting for approvals
.github/skills/pbi-lookup/           looking things up on Microsoft Learn, DAX Guide and SQLBI, and nowhere else
.github/skills/business-definitions/ starter definitions for eight business areas, read one at a time
.github/skills/pbi-lessons/          the improvement loop: what Copilot does when it gets something wrong
.github/skills/pbi-practice-library/ a reference library of practice notes on DAX and modelling, restated from public
                                     SQLBI articles and white papers: one index, topic files. Information, not rules
checklist/checklist.md               the 79 checklist items, word for word
theme/theme.json                     the report theme, unchanged
docs/report-brief.md                 what you tell Copilot before it builds
docs/lessons.md                      each Copilot mistake, its correction, and where the fix went
scripts/                             machine checks, the tools Copilot builds with, the flow tool and the lessons tool
scripts/schemas/                     a copy of every version of Microsoft's schemas for report files (MIT), used by the checks
tests/                               tests of the scripts, on made-up data
tests/fixtures/examples/             one working example of every native object kind, with INDEX.md
evals/prompts.md                     test prompts for the guidance (not yet run)
evals/first-test.md                  how to try the whole flow on a report nobody here built
maintenance/                         the template's own working papers: coverage, feature inventory, decisions, sources,
                                     and the working paper and removal record of the practice library
THIRD_PARTY_NOTICES.md               licence notices for what the template follows or ships
```

Two of the eight business areas (reliability; energy and gas) apply to electric and gas utilities only.

Copilot is told not to read `maintenance/`. It is for whoever maintains the template.

Two words used below: an **annotation** is a name-and-value entry in a visual's `visual.json` file that Power BI Desktop ignores; a **label** is a readable name for a visual in the form `Page_Type_Subject`.

## 1. Create your repository

Create your own repository from this template and clone it. Keep the clone out of OneDrive and SharePoint folders. Do everything below in that clone. Open its root folder in VS Code (not a subfolder), so Copilot finds `.github`.

Power BI Desktop writes Windows line endings. Microsoft advises turning on Git's `autocrlf` setting to keep diffs clean.

## 2. Add a project

A repository holds one Power BI project. Use one of the two routes.

### Route A: a new report

Ask Copilot: "Make a new project called Sales". Or run it yourself:

```bash
python scripts/scaffold.py project Sales
```

It copies the shipped starter project into the root of your clone: `Sales.pbip`, `Sales.Report` (PBIR, one empty page) and `Sales.SemanticModel` (TMDL, with the measures table `_Measures`). Then do these three things once, in Power BI Desktop:

1. Open `Sales.pbip`.
2. Import the theme: Design ribbon > Import theme, and choose `theme/theme.json` from your clone. Microsoft supports a theme file inside a project only after Power BI Desktop itself has registered it, so the script leaves the theme out. (`--register-theme` writes the theme into the files instead, the way Microsoft's own report skill does. Microsoft Learn does not describe that as supported, so Copilot uses it only when you say yes.)
3. Turn off Auto date/time for this file: File > Options and settings > Options, the Current File page, the Time intelligence section. Clear the option. Save, and close Desktop.

Then check the result and commit:

```bash
python scripts/check_project.py .
```

```bash
python scripts/check_template.py
```

The second command confirms that the theme copy Desktop registered has the same content as `theme/theme.json`. Until the theme is imported, the first command reports T001.

For a report on a published model, connect a blank report to that model in Power BI Desktop and save it as a project in the root of your clone. Such a project has no `.SemanticModel` folder. Connecting to a workspace is your decision; Copilot never does it.

**Copilot has something to follow from the start.** `tests/fixtures/examples/` holds one working example of every native object kind that Microsoft's sources give a file form for: the visual types (the index names the few that are not built, and why), every kind of relationship, roles, a calculation group, field parameters, user-defined functions, a date table, each storage mode, a hybrid table, filters of every kind, drilling, small multiples, a label measure for a second language and more. `tests/fixtures/examples/INDEX.md` lists them. When your project has no object of a kind, Copilot copies the example, changes its names and fields, and runs the checks. You do not need to make a first one in Desktop. The examples parse, pass Microsoft's schemas and pass the project check; none has been opened in Power BI Desktop by the template's builder, so look at the first use of each kind.

Visuals you make in Desktop yourself count as existing visuals: run steps 4 and 5 of Route B on them, now and whenever you add a visual in Desktop later.

You should see a `definition` folder inside the `.SemanticModel` folder (TMDL files) and inside the `.Report` folder (PBIR files). If you see `model.bim` or a single `report.json` there instead, your Desktop is saving an older format, and `scripts/check_project.py` will say so.

### Route B: an existing report

For an evaluation only, steps 1 and 3 are enough: the later steps change the report.

1. Get it into project format. A `.pbix` file: open it in Power BI Desktop and use File > Save as with the Power BI project file type, saving into the root of your clone. A project that already exists: copy its `.pbip` file and its `.Report` and `.SemanticModel` folders into the root. Commit.
2. Apply the theme in Power BI Desktop: Design ribbon > Import theme, choose `theme/theme.json`, then save and close. Microsoft notes that importing a custom theme removes customizations already added to the report. If you go on to "Evaluate and improve" (section 5), skip this step: that flow registers the theme by script.
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

6. Reload in Desktop and open one changed visual of each kind to confirm it looks as before (or let Copilot take the pictures: "Optional tools from Microsoft").

## 3. Work with Copilot

Fill in `docs/report-brief.md` first. Then ask Copilot in agent mode.

**One chat per task.** Start a new chat for each task. A long chat loses its early instructions, and a new chat reads the rules again. Copilot will say so when a chat already holds a finished task.

| Job | Ask Copilot something like | What happens |
|---|---|---|
| Build new | "Add a page that shows sales by month" | Copilot follows the model and report skills, copies the shipped example of any object kind the project lacks, gives new visuals a `Page_Type_Subject` name, and runs the checks |
| Evaluate | "Evaluate this report against the checklist" | Copilot runs every check and gives Pass, Fail or Not applicable for all 79 items in a new file, `docs/checklist-review.md`. It changes nothing else |
| Evaluate and improve | "Evaluate and improve this report" | Copilot makes a branch and an untouched copy, evaluates, writes a fix plan and applies it without waiting for an approval: the theme, the mechanical fixes, the layout, all measures into `_Measures`, names, and changes that need a refresh, one commit for each kind. It holds back only what could break other reports or leave tables without data, evaluates again, and ends with one answer: the counts before and after, what was held, and the questions. See section 5 |
| Change existing | "Add descriptions to the Sales table" or "Move the slicers to the top" | Copilot edits pages, visuals, measures and descriptions, and does not rename what already exists |
| Rename or move | "Rename the measure Total Sales to Net Sales" | The brief decides (section 3, "Other reports use this model"). With no, Copilot does the work at once and proves every reference with the checks. With yes or no answer, it lists every reference and what may break in other reports on the same model, and waits for your clear yes |

What Copilot asks you, and when:

- **Meaning.** What a column or measure means comes from the brief or from you. When neither says it, Copilot writes `/// TODO(owner): <question>` above the object and carries on. At the end of the task it asks about all of them in one message. `python scripts/list_todos.py .` prints the list.
- **Facts about the data.** Row counts, unique keys, whether a step folds. When you have set up Microsoft's modeling server Copilot reads the counts and the keys itself; otherwise the question goes into its final answer, in one list. Whether a step folds stays a question for you.
- **A yes.** For a preview feature; for a suggested native feature; for a change to a template file; and for a rename, a move or a deletion when other reports use the model or the brief does not say.
- **Never in the middle.** Copilot asks at the start of a task or in its final answer. A fact it cannot find becomes a `TODO(owner)` line or a question at the end, and a tool that was not set up or failed is named there.
- **A look.** Files that pass the checks can still look wrong on screen. Copilot asks you to reload and look, or does it itself through Microsoft's Desktop Bridge when you have agreed to that.

It does not ask you to make a first table, visual or measures table in Desktop: it copies a shipped example.

**Suggestions.** When a native feature would do a job better (a field parameter in place of stacked visuals, a calculation group in place of many time variants, sync slicers, an aggregation table), Copilot says so at the end of its answer, and the check prints a note whose code starts with U. It never stops a task to ask, and it builds the feature only after your yes.

**Looking things up.** When a check fails for no clear reason, DAX returns an error, a function is new to the model, a lesson is about to be written, or a note of the practice library needs confirming, Copilot looks it up: on Microsoft Learn and on the pages listed in the sitemaps of dax.guide and sqlbi.com, and nowhere else (`python scripts/lookup.py`). VS Code asks you to approve the command. With no network Copilot says so and carries on from the repository.

**The practice library.** The skill `pbi-practice-library` holds short practice notes on DAX and semantic model design. Each note restates, in new words, one piece of advice or one fact from a public SQLBI article or white paper, and gives its year and address; the article stays the place for the detail. The notes are sorted by topic, and each topic file has two shelves: general practice, and special-case techniques and facts. Copilot uses the library as information, when a task calls for it and the standards leave the question open: writing or reviewing DAX, designing a model, a performance question, an unusual requirement, or a failed check that a look-up did not explain. It reads the index (`.github/skills/pbi-practice-library/references/index.md`), then opens only the file it needs (two at most), never the whole library, and names the notes it used by ID. The library is not a standard and nothing checks it: the checklist and the standards win, and a note never justifies an exception. A note marked **Check** may no longer hold in current Power BI; Copilot confirms it through the look-up skill before it relies on it. A note marked **Paper** comes from a white paper whose full text is on a download site the look-up skill does not open; Copilot confirms it on Microsoft Learn instead. Advice that depends on a custom visual, another vendor's tool or another system, or on publishing or deploying, was left out of the library.

Where each case is covered:

| Case | README | Copilot guidance | Scripts |
|---|---|---|---|
| New report on a new model | Section 2, Route A; then "Build new" above | `pbi-semantic-model` ("New model, or new objects in a model"), then `pbi-report` ("New page or new visual", "Layout"); both instruction files | `scaffold.py`, then `check_project.py` after every change; `check_template.py` once the theme is imported; `list_visuals.py`; `list_todos.py` |
| New report on an existing model | A published model: Section 2, Route A, last paragraph. A model that is already a project: Route B, then add pages to its report | `pbi-report` ("A report on a published model"; then "New page or new visual"); `pbi-semantic-model` ("Existing model") for added measures | `check_project.py`, `list_visuals.py` |
| Evaluate an existing report and model | Section 2, Route B, steps 1 and 3; then "Evaluate" above | `pbi-checklist-review` (all of it) | `check_project.py`, `check_template.py`, `list_visuals.py`, `list_todos.py`, `check_project.py --review` |
| Modify an existing report and model | Section 2, Route B; then "Change existing" above | `pbi-report` ("Existing report", "Layout"), `pbi-semantic-model` ("Existing model"), and the rename rule in the project instructions | `set_visual_defaults.py`, `set_model_properties.py`, `set_positions.py`, `find_references.py`, `list_visuals.py`, `check_project.py` |
| Evaluate an existing report and model, then improve it | Section 2, Route B, steps 1 to 3; then section 5 | `pbi-improve` (all of it), which uses the three skills above | `improve.py`, and every script above |

Not covered: making a second report folder beside an existing one in the same project. Do that in Power BI Desktop.

## 4. The improvement loop

The template learns from Copilot's mistakes. `docs/lessons.md` records each mistake, its correction, and where the fix went.

**What starts it**

- You point out a problem ("that is wrong", "this should be...").
- A check fails on something Copilot created or changed. When `scripts/check_project.py` finds errors, its last line tells Copilot to record a lesson for each finding code. Every standard counts: codes that start with M, P, G, B, V and A. A warning or a note does not start the loop, and `scripts/lessons.py` refuses to record one as a failed check, so the many warnings an existing report can give do not flood the lessons file. One lesson is recorded for each kind of mistake in a task, not for each finding.

Both triggers work through Copilot's guidance; no script records a lesson by itself.

**What Copilot then does** (skill `pbi-lessons`)

1. Puts the mistake right in the report or model.
2. Records one lesson with `python scripts/lessons.py add`. Lessons of the same kind share a key: the finding code for a failed check (for example `D001`), or a short name.
3. When the same key comes back, the lesson must be built into the template: a new script check with a test where a script can catch the mistake, otherwise one line in the right skill or instruction file. If the mistake returns twice more after that, the loop starts again.
4. Copilot always asks before changing any template file. It shows you the exact change and waits for a clear yes. It then makes the change on a new branch; you open the pull request, and merging it is the approval. If you say no, the lesson is recorded as declined.

Template files are everything under `.github/`, `scripts/`, `tests/`, `evals/` and `maintenance/`, and the root files `README.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, `.gitignore` and `.gitattributes`. The brief and the lessons file are your project's own content.

Every standard, its checks, the shipped examples, the tools and the skills are template files too, so they are inside the loop, manual and automatic. A lesson may propose a change to any of them. Copilot always asks first, and a person approves by pull request. Before it writes a lesson, Copilot may look the right way up (skill `pbi-lookup`). A lesson may point to a note of the practice library by its ID; the library records no lessons and proposes no template change by itself.

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

**Nothing waits for an approval.** The safeguard is the branch, the untouched copy and one commit for each kind of fix: each kind can be undone alone with `git revert`. One gate holds a row back instead, and the plan says which rows.

- **Other reports.** A report that reads a published copy of the model names a measure with its table, so a move or a rename would break it, and no file here can show that. Measures are moved and names corrected only when section 3 of the brief answers "Other reports use this model" with no. This is the one question Copilot asks, at the start, when the brief does not answer it.
- **A missing data source never stops a fix.** A change to a query's text, a partition's name or a data type, and a new table, are applied like every other fix. Such a table is empty until Power BI Desktop refreshes the model, so refresh once after the run. Work on a report whose data sources you can reach.

1. **Safety first.** Save and close the project in Power BI Desktop, and commit. `python scripts/improve.py start` stops unless everything is committed and no earlier flow left its files behind. It makes a new branch, and copies the project unchanged into the folder `_before/`, so you can open before and after side by side. Git ignores that folder and the checks skip it.
2. **Evaluate.** The checklist review writes `docs/checklist-review.md`. Copilot asks nothing: a fact no file holds is a Fail with "Evidence missing", and its question goes into the final answer.
3. **Fix plan.** `docs/fix-plan.md` lists every finding and every failed item with a kind and a status (`to do`, `done`, `held: <why>`, `skipped: <why>`, and `question` or `answered` for a row that needs a person). The kinds, in the order they are applied:
   - **Theme**: the owner's theme is registered in the report (`python scripts/scaffold.py theme .`).
   - **Mechanical**: descriptions, format strings, folders, hiding, header icons and tooltips, alt text and titles, the DAX style, two rewrites that cannot change a result, styling the theme should do. A visual that uses drill-down, a help tooltip, a tooltip page or tooltip fields keeps that setting, with a row in section 7 of the brief.
   - **Layout**: positions and sizes by the numbers of the layout standard, a back button, tab order.
   - **Measures**: every measure moves to `_Measures`, with every reference repaired. Other-reports gate.
   - **Renames**: names the naming standard rejects. Other-reports gate.
   - **Data**: a comment line in a query, a partition's name, a floating-point column, an unused column removed. Applied last; refresh the model afterwards.
   - **Needs a person**: a fact or a decision no file holds: why something is calculated in the model, summarisation, formulas whose result would change, relationships, security roles, access, user testing, export tests, performance runs. These are questions, not approvals.
4. **Apply.** Each kind in turn, then the checks, then one commit for that kind.
5. **Evaluate again**, all 79 items. `python scripts/improve.py compare` prints Pass, Fail and Not applicable before and after; how many of the items that still fail can pass only on a fact from a person; the pages to look at; what was held and why; what was skipped; and the questions, with rows that ask the same thing shown once.
6. **One final answer** with all of that. When you answer a question, Copilot does the work. When the gate opens (you tell Copilot that no other report uses the model, and it writes that in the brief), `python scripts/improve.py release` frees the held rows and Copilot carries on.

Never in this flow: a change that would break another report, a change to the checklist, the theme file or a template file, a made-up business meaning, publishing, deploying or merging.

Why the copy is safe: the `.pbip` file points to the report folder, and the report points to the model, both by relative path, so the three are copied together with their names unchanged and nothing inside is edited. Each `.platform` file holds an identifier that must stay unique within a Git branch, which is why the copy is never committed. If Git would not ignore `_before/`, or a path would pass 260 characters, the script makes no copy, says so, and the branch is the safeguard.

To try the flow end to end, see `evals/first-test.md`.

## The rules the checks enforce

`scripts/check_project.py` enforces these. Errors change its exit code; warnings and notes do not. It cannot tell a new visual from an existing one, or check that a header or tooltip exception is listed in the brief; people and the review do that. The full list of codes is at the top of the script, and every code is named in the checklist-review skill. The fix plan sorts every error and warning of the standards; a file or syntax error (codes such as F001, J001, N001, S001) is listed there as a question for a person, and notes are listed for information.

- Every visible table, column and measure has a `///` description directly above it; so does every shared query and parameter. Unknown meaning becomes `/// TODO(owner): question`, which the check lists.
- `//` comments appear only inside Power Query (M) or DAX expressions.
- Every Power Query step has a `//` comment line above it describing it (a `/* */` comment also counts). This, and using `///` for a query's description, is a convention of this template: Microsoft does not document how Desktop stores query and step descriptions in project files.
- Page and visual names use only letters, digits, underscore and hyphen, and are at most 50 characters.
- Every visual has a `Page_Type_Subject` name, or a `VisualLabel` annotation carrying one.
- Every visual has Header icons off and Tooltips off set on the visual itself, as well as in the theme. A visual that must keep one on carries a `HeaderTooltipException` annotation that says what stays on and why (and is listed in section 7 of the brief).
- A custom theme is registered in the report.
- Every report file fits the Microsoft schema it names (J003). Microsoft Learn calls a schema breach a blocking error: Power BI Desktop refuses the file.
- No report file names a table, column or measure that the model in the project does not have; for a report on a published model, one that the saved field list does not have.

The standards, each in a file that names the source of every rule:

| Standard | File | Fails on (examples) | Warns on (examples) |
|---|---|---|---|
| Measures, folders, hiding, calculated objects, types, formats | `.github/skills/pbi-semantic-model/references/model-standard.md` | a measure outside `_Measures`; no two-level display folder; a code-style measure name; no format string; a visible number column that still totals | name details, reference style, keys left visible, the floating-point type |
| Star schema, relationships, dates, names | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md` | a relationship, sort column or hierarchy level on a column that does not exist; time intelligence with no marked date table; USERELATIONSHIP towards a secured table | both-direction, many-to-many and one-to-one relationships; an inactive relationship nothing uses; a table with no relationship; Auto date/time on; table and column names |
| DAX rules, style and patterns | `.github/skills/pbi-semantic-model/references/dax-standard.md` | a division by anything but a fixed number that does not use DIVIDE; a `Table[Column]` the model does not have | IFERROR, FILTER over a whole table, blanks turned into values, repeated expressions, two measures with one formula, DIVIDE by a fixed number, ALL where REMOVEFILTERS is meant, CALCULATE inside CALCULATE, the DAX style |
| Power Query, storage modes, security | `.github/skills/pbi-semantic-model/references/storage-and-security.md` | incremental refresh without its two Date/Time parameters or with both ends included; a DirectQuery native query with a stored procedure; object-level security on a table in the middle of a chain; a legacy query partition on a structured data source | steps in a DirectQuery query, a local file, a loaded table that only feeds other queries, role rules on a fact table, USERNAME, a security filter in both directions |
| Functions, calculation groups, field parameters | `.github/skills/pbi-semantic-model/references/model-objects.md` | a function below compatibility level 1702, with a reserved name, or calling itself; a field parameter that names a missing field | undocumented functions and calculation items; a function that names an object a role hides; a preview feature without your yes |
| Hybrid tables, Direct Lake variants, dynamic query parameters, model options, the other files of a model folder | `.github/skills/pbi-semantic-model/references/more-model-features.md` | - | a preview feature without your yes |
| One report for readers in several languages | `.github/skills/pbi-semantic-model/references/multiple-languages.md` | - | USERCULTURE in a calculated column or a report-level measure; a label measure with no default; typed text and page tabs in a report on a model with translations |
| Layout | `.github/skills/pbi-report/references/layout-standard.md` | a visual outside its page; two data visuals that overlap | grid, margins, gaps, row heights, page size |
| Report features and accessibility | `.github/skills/pbi-report/references/report-standard.md` | a drillthrough page without a back button; more than 16 data visuals on a page | tooltip pages, a button that goes nowhere, styling on a single visual, missing alt text and titles, shared tab order numbers, a report-level measure without its prefix, filter values left over from design time, a visual type Microsoft is retiring, an image that is not registered |
| Features inside a visual and on a page | `.github/skills/pbi-report/references/visual-features.md` | - | a preview feature without your yes |

How the levels were set for the checks added in round 3: a check fails when Microsoft says the thing breaks or gives wrong numbers, or the checklist gives a hard number, and the files show it for certain. Every other rule warns. A suggestion is a note.

An exception counts only when section 9 (model) or section 10 (report and layout) of `docs/report-brief.md` lists the same code and object with a reason. The script reads the brief; it also takes the page size, margin, gap, grid step, folder subjects, the prefix for report-level measures, the two optional checks (Excel, Copilot in Power BI) and the preview features you agreed to (section 11) from there.

Formulas are read by a small scanner (`scripts/formula_scanner.py`): one pass, six states (code, text, line comment, block comment, quoted name, bracketed name), with separate rules for DAX and for Power Query. A function name inside a comment, or a slash inside a text value, is not mistaken for code. It is a scanner, not a parser: it does not know what a formula means.

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

Writes a position and size worked out from the layout standard. It refuses groups, visuals inside a group, rotated visuals and anything that would leave the page, and it names the pages to look at afterwards.

```bash
python scripts/scaffold.py project Sales
```

Makes a new project from the shipped starter (section 2, Route A). `python scripts/scaffold.py measures-table .` adds the table `_Measures` to a model that has none: an imported one-column table, or a calculated table when the model reads its data in Direct Lake or DirectQuery mode. `python scripts/scaffold.py theme .` registers `theme/theme.json` as the custom theme of a report that already exists, in place of any custom theme it had; close the project in Power BI Desktop first.

```bash
python scripts/list_todos.py .
```

Prints every open `TODO(owner)` question, with its object and file.

```bash
python scripts/find_references.py . "Sales[Amount]"
```

Lists every place that refers to a column (`"Table[Column]"`), a measure (`"[Measure]"`) or a table (`"Table"`): the references it recognises, and the text it cannot classify. Used before a rename or a move.

```bash
python scripts/json_schema.py Sales.Report
```

Checks report files against Microsoft's schemas, offline. The project check does the same (J003).

```bash
python scripts/lookup.py search "selectedvalue"
```

Searches Microsoft Learn, DAX Guide and SQLBI, and `python scripts/lookup.py read <address>` prints one page. No other site is reachable through it.

```bash
python scripts/desktop_bridge.py status .
```

Optional (see "Optional tools from Microsoft"): `status`, `reload`, `screenshots` and `clean`.

```bash
python scripts/improve.py next
```

Says which step of the evaluate-and-improve flow comes next (section 5). `python scripts/improve.py release` gives new plan rows their status and frees held rows whose reason is gone; `python scripts/improve.py compare` prints the result.

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

The project must be saved in Power BI Desktop before Copilot edits files. After the edit, one of these:

- Copilot reloads the project and looks at the pages itself, through Microsoft's Desktop Bridge (next section); or
- you close and reopen the project in Power BI Desktop; or
- if you use Power BI Desktop from August 2026 or later, you turn on the preview feature "Detect and reload external PBIP changes" (File > Options and settings > Options > Preview features), restart Desktop once, and from then on select "Apply external changes" in the banner that appears.

Header icons always show while you edit. Microsoft applies the "off" setting only in reading view, so check it in a published report.

## Optional tools from Microsoft

Everything in the template works without these. Each one is your decision: you install it, and you say yes to it in section 11 of `docs/report-brief.md`. Copilot never installs a tool, never publishes or deploys, and never sets up a connection to a workspace.

| Tool | What Copilot does with it | What you set up |
|---|---|---|
| Desktop Bridge | Reloads the project in Power BI Desktop and takes a picture of every page, then looks at the pictures: `python scripts/desktop_bridge.py`. Guidance: `.github/skills/pbi-report/references/desktop-bridge.md` | Windows; Power BI Desktop of June 2026 (2.155.756.0) or later with the Desktop Bridge option on (Options > Security; on by default); Node.js 20 or later; the two npm packages `@microsoft/powerbi-desktop-bridge-cli` and `@microsoft/powerbi-report-authoring-cli`. You open the project in Desktop |
| Power BI Authoring MCP Server, the local one (`microsoft/powerbi-modeling-mcp`) | Reads facts about the data with DAX queries: row counts, distinct values, whether a key is unique. Read only. Guidance: `.github/skills/pbi-semantic-model/references/data-facts.md` | The VS Code extension "Power BI Authoring MCP"; you accept Microsoft's licence terms for it; run it with `--readonly`; you open the connection |
| Microsoft Learn MCP server | A second way to read Microsoft Learn pages. The look-up script needs no setup | Add the server in VS Code if you want it |

- The Desktop Bridge is treated as a preview feature: Microsoft's pages disagree on whether it still is one. The second npm package is a public preview.
- A reload does not refresh data, and the Bridge cannot read the error box Desktop shows when a file fails to load.
- Pictures of pages can show data. The script writes them outside the project and deletes them on request.
- Query results pass through the chat to the AI service behind it. If your data is sensitive, give Copilot the facts yourself instead.
- A report on a published model: Copilot takes the field list from model files in this repository; else from `docs/model-fields.md`; else through Microsoft's modeling server if you have already set that connection up (the one case in which it reads from a workspace); else it asks you once and saves the list.

## The theme and the checklist are fixed

`theme/theme.json` and `checklist/checklist.md` must not be edited. `scripts/check_template.py` fails if either changes. If the owner replaces one on purpose, update the matching hash at the top of that script.

What the theme means for drill, tooltips, export, contrast and text size is set out in `.github/skills/pbi-report/references/theme.md`.

## Not tested, and not confirmed

- Copilot prompt tests have not been run. Steps are in `evals/prompts.md`.
- The practice library is information drawn from articles, the oldest from 2011. No note was tried in Power BI Desktop. Notes whose advice may have aged carry the mark Check; a note without the mark showed no sign of change when it was written, which is not proof that it still holds.
- Nothing here has been opened in Power BI Desktop by the template's builder. That includes every shipped example and the starter project. They parse (the model files load in Microsoft's own Tabular Object Model library and pass its validation), pass Microsoft's schemas, and pass the project check. Microsoft's library does not parse DAX or Power Query, and Microsoft's own skill warns that a wrong field or role can pass validation and still show an error icon. Look at the first use of each kind in Desktop.
- Written, not run: `scripts/desktop_bridge.py` and the guidance for Microsoft's modeling server. Neither Power BI Desktop nor the server could be run where the template was built. The tests replace Microsoft's tools with stand-ins.
- The starter project's report holds an empty theme collection until you import the theme. Whether Power BI Desktop opens it without a remark is not confirmed.
- `scripts/scaffold.py project <Name> --register-theme` registers the theme in the files the way Microsoft's own report skill does. Microsoft Learn supports edits under `RegisteredResources` only for a resource Desktop registered itself, and Microsoft's command-line validator expects a theme's inner name to equal its file name, which the owner's theme does not do. The evaluate-and-improve flow uses this route for an existing report (`python scripts/scaffold.py theme .`) by the owner's rule that every report gets the theme; for a new project it stays off unless you pass the flag. Whether Power BI Desktop accepts a theme registered this way without a remark is not confirmed: look at the colours when the report is first opened.
- After the evaluate-and-improve flow, a table whose query, partition name or data type changed shows no data until the model is refreshed. This rests on one observation and on reasoning, not on a Microsoft page: in the first trial a run left a report without data, on a computer where the source file was missing. Microsoft Learn says only that a project's local data cache holds the model and data "when it was last edited". Which of those changes empties a table is not confirmed one by one.
- Release notes: the monthly feature summary posts on Microsoft's blog could not be opened. The feature inventory was built from Microsoft Learn's update pages, which are short for November 2024 to June 2025.
- Not confirmed from Microsoft's documentation: how Desktop stores Power Query query and step descriptions; whether Desktop keeps annotations when it saves; what "Tooltips off" does to report-page tooltips; whether right-click drill and "Export data" still work in reading view when header icons are off; where the Selection pane name of a single visual is stored; how "hidden from the tab order" is stored; the value `ParameterMetadata` carries on a field parameter (it comes from Microsoft's skill, not from Microsoft Learn); the annotation that records Auto date/time (seen in projects Desktop saved).
- The visual-level "Header icons off, Tooltips off" entries: Microsoft's schema defines where they go and what they are called, for every visual type, but not how the value is written; the written form follows Microsoft's own examples. Not confirmed: whether Desktop keeps and applies them on text boxes, shapes, images and buttons, and whether adding them changes a visual's padding (Microsoft's report skill warns that it can).
- The scripts were run on Linux with Python 3.13. They use nothing newer than Python 3.8, but were not run on Windows or on 3.8.
- The formula scanner knows where names, text and comments are. It is not a DAX or Power Query parser: a check that reads a formula can miss an unusual way of writing the same thing.
- Not confirmed from Microsoft's documentation, for the standards and the flow: whether Power BI Desktop accepts the measure names `# Orders` and `Gross Margin (%)` (Microsoft's "DAX syntax" page lists `%` and brackets as not valid in names; against that, Microsoft's TMDL overview shows such names, Microsoft's own saved projects hold measure names with `%` and brackets, and `#` is not on the list); whether Desktop keeps a `CalculatedReason` annotation when it saves; whether a group member's position counts from the page or from its group (so the scripts never move groups or their members); what turning summarisation off does to visuals that already total the column (so it is never a mechanical fix); whether a phone layout made automatically changes when desktop positions change.
- Fabric Git integration and deployment pipelines: read from Microsoft's documentation only; nothing was deployed. What was found is in `maintenance/feature-inventory.md`. In short: files outside the item folders are left alone; the example projects under `tests/fixtures` hold no `.platform` file and so are not items; Microsoft advises a Git folder of its own for the items when a repository holds other files too.
- Check once in Power BI Desktop, in this order: (1) a project made by `scripts/scaffold.py` opens, and the theme imports; (2) measures named `# Orders` and `Gross Margin (%)` load and work in a visual; (3) the `_Measures` table shows at the top of the Data pane, and a display folder written as `Finance\Base` shows as two levels; (4) a `CalculatedReason` annotation is still in the file after Desktop saves; (5) one visual copied from the shipped examples of each type you use; (6) a copy in `_before/` opens beside the working project; (7) one page after a layout fix, including its tab order and phone layout.

## Acknowledgements

The standards follow, in this order of trust: the owner's checklist; Microsoft Learn; Microsoft's own skills for Fabric (`microsoft/skills-for-fabric`), best practice rules for tabular models (`microsoft/Analysis-Services`) and report schemas (`microsoft/json-schemas`); SQLBI, for DAX; then the sources below. A lower source never overrides a higher one. Each standard file names its sources and where they disagree. `THIRD_PARTY_NOTICES.md` holds the licence notices.

- SQLBI's DAX formatting rules and DAX patterns are restated in the template's own words, with their addresses. The practice library (skill `pbi-practice-library`) restates ideas from SQLBI's public articles and two of its white papers the same way, one short note at a time, each with the address of its article. No SQLBI text, code or image is copied.
- Some working practices were informed by Kurt Buhler's public writing and repository on agentic Power BI development (`data-goblin/power-bi-agentic-development`, GPL-3.0) and by the Tabular Editor blog: short always-loaded guidance, detail loaded on demand, hard rules enforced by scripts, a written brief before building; and several ideas in the standards (a measures table, the order of a measure name, column folders, what to hide, a recorded reason for calculated objects, equal margins and gaps). These are ideas only. No text, code or files were taken from it, and the `pbir` command-line tool (authors: Kurt Buhler, Maxim Anatsko) is not used.
- GitHub's `awesome-copilot` repository (MIT): its modeling skill was read for naming and folder guidance, and two of its instruction files for DAX practice and report design.
- `Mofaji/Agentic-PBIP-Template` (MIT) was read in full: for the topics it covers and for how Microsoft's Desktop Bridge tools are called. None of its code is used.

## Licence

MIT. See `LICENSE`.
