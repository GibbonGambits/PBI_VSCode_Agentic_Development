---
name: pbi-report
description: Use this skill when creating, changing or checking Power BI report pages and visuals stored as PBIR files - add, move or resize a visual, lay out a page, name or label visuals, list visual positions, set header icons and tooltips, bring an existing report into the template. Covers new reports and existing ones. Trigger words - report, page, visual, chart, slicer, layout, align, resize, theme, tooltip, .Report, visual.json.
---
# Power BI report pages and visuals

Not for tables, measures or Power Query (skill `pbi-semantic-model`) and not for the full 79-item evaluation (skill `pbi-checklist-review`).

## Before you change anything

1. Read `docs/report-brief.md`: audience, pages, the question each page answers, page size, spacing. If something you need is missing, ask the developer. For a new report, propose the list of pages and what goes on each, and wait for a yes before creating files.
2. Run `python scripts/list_visuals.py .` to see every page and each visual's label, type, x, y, width, height and folder.
3. Find the model: open `*.Report/definition.pbir`. If it points to a folder in this repository (`byPath`), read field names from that model's TMDL files. If it points to a published model (`byConnection`), the model is not here: ask the developer for the tables, columns and measures. Do not connect to anything.

Checklist items are in `checklist/checklist.md`. Read only the items a step names, by searching for the heading, for example `## Item 49`.

## New page or new visual

1. Decide what the page must answer and which visual type fits: item 54.
2. Create the files as described in `references/pages-and-visuals.md`: names, `$schema`, position, Header icons off, Tooltips off. For a visual type the report does not have yet, ask the developer to place one in Desktop first; then follow its file.
3. Lay the page out: items 20, 49, 52. Method under "Layout" below.
4. Titles, labels and legends: item 55. Units and scales: item 56. Number and date formats: items 71, 72. Use model measures, not raw columns, for the numbers a visual shows: item 29.
5. Slicers: items 21, 61. Filters and their default state: items 53, 62. Interactions: items 60, 69. Navigation and drillthrough: items 51, 63. Field parameters: item 64.
6. Known limits go on an Info or Help page: item 75.
7. Colour, conditional formatting, text sizes, accessibility, and everything about header icons and tooltips: `references/theme.md`.

## Existing report

- Existing pages and visuals keep their names (project instructions).
- Set Header icons off and Tooltips off on all visuals in one step: run `python scripts/set_visual_defaults.py . --dry-run`, then the same without `--dry-run`. Then ask the developer to open one changed visual of each kind in Desktop and compare it with before.
- Give each existing visual a label. Propose labels from the `list_visuals.py` output, agree them with the developer, then run `python scripts/set_visual_defaults.py . --label <page folder>/<visual folder>=<Page_Type_Subject>`, with one `--label` for each visual.
- The theme is applied by the developer in Power BI Desktop (README, "Route B: an existing report").
- Document non-obvious interactions, bookmarks or filter logic where they live (item 8): in the brief, or in an annotation on the page or visual.
- To report gaps without changing anything, use the skill `pbi-checklist-review`. To evaluate and then fix in one request, use the skill `pbi-improve`.

## Layout

- You cannot see the page, so layout is done by numbers. Read `references/layout-standard.md` before you change any position: it holds the numbers, where the title and the slicers go, and what a move must not touch (groups, phone layout, tooltip pages).
- Read the page `width` and `height` from `page.json`. Keep every visual inside the page.
- Take the page size, outer margin, gap and grid step from the brief. If a field is empty, use the layout standard's number. For a page size the standard does not cover, ask. Do not make up numbers.
- Visuals in one row share `y` and `height`; visuals in one column share `x` and `width`; gaps are equal. No overlaps unless the developer asks for one.
- Work out each `x`, `y`, `width` and `height` by arithmetic and show the sums to the developer.
- Apply approved positions with `python scripts/set_positions.py` (`--dry-run` first). Check the result with `python scripts/list_visuals.py . --page <page>` and `python scripts/check_project.py .` (codes that start with G).
- After any layout change, name the pages that changed and ask the developer to reload them in Power BI Desktop and look.

## Only Desktop can tell

How the page looks, text that is cut off, real colours, slow visuals, export results (item 77). Ask the developer to look and tell you. Do not claim a page looks right from the files alone.

Checklist items: 8, 20, 21, 29, 37, 49-67, 69-75, 77
