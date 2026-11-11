---
name: Report files (PBIR)
description: Hard rules for Power BI report files in PBIR format.
applyTo: "**/*.Report/**"
---
# Rules for report files

`python scripts/check_project.py .` enforces rules 1 to 4, the annotation format of rule 5, rules 10 and 11, and Microsoft's schema for every file (J003). How-to detail is in the skill `pbi-report`.

1. Page and visual names, and their folder names, use only letters, digits, underscore and hyphen. A page or visual `name` is at most 50 characters. If a name breaks the character rule, Power BI Desktop ignores that file or folder.
2. A new visual gets one label, `Page_Type_Subject`, as both its `name` and its folder name. Example: `Overview_Card_TotalSales`.
3. An existing visual gets the same kind of label in an annotation, not a new name: `{ "name": "VisualLabel", "value": "Overview_Bar_SalesByMonth" }`.
4. Every visual sets Header icons off and Tooltips off on itself: `visualHeader` and `visualTooltip` under `visual.visualContainerObjects`, each with `show` false. This applies to charts, tables, cards, slicers, text boxes, shapes, images and buttons.
5. An exception to rule 4 is allowed only for a visual listed in section 7 of `docs/report-brief.md`. If the developer asks for one that is not listed, ask for the reason and add the row first. Turn on only what was asked, keep the other setting off, and add the annotation `HeaderTooltipException` with the value `header: <reason>`, `tooltip: <reason>` or `both: <reason>`.
6. A new page gets a readable `name` and folder, such as `Overview`. Its `displayName` is the tab text people read: plain words, no jargon.
7. Take `$schema` from a file of the same kind already in the report. If the report has none, copy the shipped example of that kind (`tests/fixtures/examples/INDEX.md`). Never type one from memory.
8. Read JSON, change it, and write it back as JSON, saved as UTF-8 without a byte-order mark. No find-and-replace on raw text.
9. Read only, never edited by hand. Microsoft says so for: `definition.pbir`, `mobileState.json`, `semanticModelDiagramLayout.json` and a `report.json` beside `definition.pbir` (the older format). This template adds: anything under `StaticResources`, `.platform` and `.pbi` folders. The developer imports the theme in Power BI Desktop; `scripts/scaffold.py --register-theme` is the one other route, and only after the developer's yes.
10. No visual reaches outside its page, and no two visuals that show data overlap. Positions follow the layout standard (skill `pbi-report`). Never move or resize a group or a visual inside a group, and never edit `mobile.json`.
11. A drillthrough page has a back button. A page has at most 16 visuals that show data. A visual sets no colour, font or size of its own: the theme does that. Every visual that shows data has alt text and a written title. These and the other rules of the report standard are in the skill `pbi-report` (codes that start with V and A).

Checklist items: 20, 49, 50, 59, 63, 65, 73
