---
name: pbi-report
description: Use this skill when creating, changing or checking Power BI report pages and visuals stored as PBIR files - add, move or resize a visual, lay out a page, name or label visuals, add a button, bookmark, slicer, tooltip page, drillthrough page or field parameter, set alt text and titles, list visual positions, set header icons and tooltips, bring an existing report into the template. Covers new reports and existing ones. Trigger words - report, page, visual, chart, slicer, button, bookmark, layout, align, resize, theme, tooltip, drillthrough, .Report, visual.json.
---
# Power BI report pages and visuals

Not for tables, measures or Power Query (skill `pbi-semantic-model`) and not for the full 79-item evaluation (skill `pbi-checklist-review`).

You build the pages yourself. When the report has no visual of the type you need, you copy the shipped example of that type and run the checks. You ask the developer only for what no file can tell you.

## Before you change anything

1. Read `docs/report-brief.md`: audience, pages, the question each page answers, page size, spacing. For a new report, propose the list of pages and what goes on each, and wait for a yes before creating files. A fact the brief lacks and no file holds: ask once, in one message.
2. Run `python scripts/list_visuals.py .` to see every page and each visual's label, type, x, y, width, height and folder.
3. Find the model: open `*.Report/definition.pbir`. If it points to a folder in this repository (`byPath`), read field names from that model's TMDL files. If it points to a published model (`byConnection`), the model is not here; see "A report on a published model" below.
4. No project yet? `python scripts/scaffold.py project <Name>` makes one from the shipped starter.

Checklist items are in `checklist/checklist.md`. Read only the items a step names, by searching for the heading, for example `## Item 49`.

## The standards

`python scripts/check_project.py .` checks all of them. Exceptions go in section 10 of the brief (section 7 for header icons and tooltips).

| For | Read | Codes |
|---|---|---|
| File layout, names, labels, `$schema`, a new visual, the shipped examples | `references/pages-and-visuals.md` | N00x, H00x, J00x, S001 |
| Positions and sizes | `references/layout-standard.md` | G00x |
| Field parameters, bookmarks and buttons, tooltip and drillthrough pages, sync slicers, conditional formatting, phone layout, chart choice, titles, filters, accessibility, page density | `references/report-standard.md` | V0xx, A00x, U1xx |
| Features inside a visual and on a page: filter kinds, drilling, small multiples, totals, sparklines, analytics lines, more slicers and buttons, cross-report drillthrough; what has no file form | `references/visual-features.md` | V022 |
| Colour, text sizes, header icons and tooltips | `references/theme.md` | H00x, V009, T001 |
| Reloading and looking at pages yourself (optional) | `references/desktop-bridge.md` | - |

## New page or new visual

1. Decide what the page must answer and which visual type fits: item 54 and the table in `references/report-standard.md`.
2. Create the files as described in `references/pages-and-visuals.md`: names, `$schema`, position, Header icons off, Tooltips off. Follow a visual of the same type already in the report. If there is none, copy the shipped example of that type from `tests/fixtures/examples/INDEX.md`, then change its name, its fields and its position.
3. Lay the page out: items 20, 49, 52. Method under "Layout" below.
4. Titles, labels and legends: item 55. Every visual that shows data gets a written title and alt text. Units and scales: item 56. Number and date formats: items 71, 72. Use model measures, not raw columns, for the numbers a visual shows: item 29.
5. Slicers: items 21, 61. Filters and their default state: items 53, 62. Interactions: items 60, 69. Navigation and drillthrough: items 51, 63. Field parameters: item 64. The rules for each are in `references/report-standard.md`.
6. Known limits go on an Info or Help page: item 75.
7. Run `python scripts/check_project.py .` and fix every error. Then reload and look ("Looking at the result").

## Existing report

- Existing pages and visuals keep their names (project instructions).
- Set Header icons off and Tooltips off on all visuals in one step: run `python scripts/set_visual_defaults.py . --dry-run`, then the same without `--dry-run`.
- Give each existing visual a label. Write the labels from the `list_visuals.py` output, as the naming rule sets out, list them in your final answer, and run `python scripts/set_visual_defaults.py . --label <page folder>/<visual folder>=<Page_Type_Subject>`, with one `--label` for each visual.
- The theme: the developer imports `theme/theme.json` once in Power BI Desktop (Design ribbon > Import theme). `python scripts/check_template.py` then confirms the copy.
- Document non-obvious interactions, bookmarks or filter logic where they live (item 8): in the brief, or in an annotation on the page or visual.
- To report gaps without changing anything, use the skill `pbi-checklist-review`. To evaluate and then fix in one request, use the skill `pbi-improve`.

## A report on a published model

The field list comes from the first of these that exists:

1. Model files in this repository.
2. `docs/model-fields.md`, the saved list: one table with the columns Table, Field and Kind (column, measure or hierarchy), and above it the model's name, the date and where the list came from.
3. Microsoft's modeling server, if the developer has already set up that connection: read the tables, columns and measures, read only (the file data-facts.md of the skill `pbi-semantic-model`), and save them as `docs/model-fields.md`. This is the one case in which you read from a workspace.
4. Otherwise ask the developer once for the list, and save it as `docs/model-fields.md`.

Never set up a connection to a workspace yourself. The check compares every field a report file names with the saved list (B001), and says so when there is no list (B002).

## Layout

- Layout is done by numbers. Read `references/layout-standard.md` before you change any position: it holds the numbers, where the title and the slicers go, and what a move must not touch (groups, phone layout, tooltip pages).
- Take the page size, outer margin, gap and grid step from the brief. If a field is empty, use the layout standard's number.
- Work out each `x`, `y`, `width` and `height` by arithmetic and show the sums to the developer.
- Apply positions with `python scripts/set_positions.py` (`--dry-run` first). Check the result with `python scripts/list_visuals.py . --page <page>` and `python scripts/check_project.py .`.

## Looking at the result

Files that pass the checks can still look wrong: text that is cut off, real colours, a visual with an error icon.

- Where the Desktop Bridge is installed (the script says "not available" when it is not): reload and take a picture of each page yourself, look at the pictures, and delete them (`references/desktop-bridge.md`).
- Otherwise name the pages that changed and ask the developer to reload the project in Power BI Desktop and to look at them.
- Never say a page looks right from the files alone. Slow visuals and export results (items 68, 77) need a person.

## A better native feature

The check prints notes with codes that start with U: sync slicers for the same slicer on several pages, a page navigator in place of rows of buttons, a field parameter in place of stacked visuals switched by bookmarks. The full list is in `.github/skills/pbi-checklist-review/references/native-features.md`. Mention a suggestion once, at the end of your answer; never stop a task to ask about one; build it only after the developer's yes.

## When you are stuck

A check fails and you cannot see why: skill `pbi-lookup`. Do not guess a property name.

Checklist items: 8, 20, 21, 29, 37, 49-67, 69-75, 77
