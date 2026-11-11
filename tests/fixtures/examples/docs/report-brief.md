# Report brief

Brief for the shipped examples in this folder: the example models and the example report, with made-up data for a small shop. Together they hold one working example of every object kind listed in `INDEX.md`. They are examples to copy from, not a report for readers. The project check reads sections 7, 9, 10 and 11 of this file when it runs on this folder.

## 1. Purpose and audience

- Report name: Examples (one page for each group of examples; not a report for readers).
- Who uses it, and which decision or action it supports: Developers and the coding assistant of this template, who copy an example when a project has none of its own.
- How they see it: laptop, meeting-room screen, phone, print or export (52, 67, 77): not applicable.

## 2. Pages

| Tab name | The question this page answers | Notes |
|---|---|---|
| (every page of Examples.Report) | None: each page shows examples of one kind, as `INDEX.md` lists them | Not a report for readers |

- Page size in pixels, width x height (52):
- Outer margin in pixels (49):
- Gap between visuals in pixels (49):
- Grid step in pixels (49):

## 3. Data

- Semantic model: the example models in this folder: Examples.SemanticModel (import), the models under `storage/` (one for each storage form: DirectQuery with Dual and an aggregation table, Direct Lake in both forms, a hybrid table, a dynamic query parameter, model options) and the models under `preview/` (preview features). `INDEX.md` lists them all.
- Sources, and the environments they exist in, such as development, test, production (1, 2): made-up data written in the queries, or made-up source names.
- Import, DirectQuery or both, and why (16): one example model for each storage mode.
- How often the data must refresh (45): not applicable.

## 4. Standards to follow

- Naming standard for tables, columns and measures (7, 28): the model standard of this template.
- Measure folder subjects (22):
- Acronyms and words with their own spelling (7, 28):
- Measure table: `_Measures`: an imported one-column table, or a calculated table when the model reads its data in Direct Lake or DirectQuery mode. Every example follows this; none was made in Power BI Desktop.
- Large tables: row counts, and the decision on incremental refresh or partitions: the table Sales of the import example carries an incremental refresh policy as an example.
- Excel check on (yes or no): no
- Power BI Copilot check on (yes or no): no
- Number formats and date formats (71, 72): amounts `#,0.00`, counts `#,0`, percentages `0.0%`, dates `Short Date`.
- Logos and other brand assets (74): none.
- Who may see what: security roles, sensitive fields (39, 40, 41): the import example holds four example roles; no real people or data.

## 5. Business definitions confirmed by their owners

| Term or measure | Definition, what is left out, caveats | Confirmed by | Date |
|---|---|---|---|
| | Made-up examples; no business definitions. | | |

## 6. Decisions and justifications

| Checklist item | Decision or justification | By | Date |
|---|---|---|---|
| 12 | The relationship from Sales to Product filters in both directions, only to show how such a relationship is written. | Template | 2026-11-11 |

## 7. Exceptions to "Header icons off, Tooltips off"

| Page | Visual | What stays on (header, tooltip or both) | Reason |
|---|---|---|---|
| Charts_Bars | Charts_Bars_ClusteredBar_SalesByStore | tooltip | Shipped example of a report page tooltip: hovering a bar shows the page Tooltip_StoreSales |

## 8. Known limits to tell users about (75)

- These are examples of how each object is written. They parse with Microsoft's TMDL library and pass the project check, but have not yet been opened in Power BI Desktop.

## 9. Exceptions to the model standard

The model standard is `.github/skills/pbi-semantic-model/references/model-standard.md`. A check passes only for an object listed here with a reason. Each row below is a finding that an example causes on purpose.

| Code | Object | Reason |
|---|---|---|
| M405 | Sales[Product Key] to Product[Product Key] | Shipped example of a both-direction relationship |
| M406 | Sales Target[Category] to Product[Category] | Shipped example of a many-to-many relationship |
| M110 | Sales Target[Category] to Product[Category] | Shipped example of a many-to-many relationship, which joins on a text column (category) |
| M409 | Store Detail[Store Key] to Store[Store Key] | Shipped example of a one-to-one relationship |
| M408 | model | Shipped examples of a both-direction, a many-to-many and a one-to-one relationship in one small model |
| M815 | model | Shipped examples of a calculation group and of a detail rows expression in one model; a real model keeps one of the two |
| M414 | model | Shipped examples of security roles and of an inactive relationship (ship date) in one model |
| M607 | model | Shipped examples show a role with row rules and a role with object rules side by side; a real model puts both kinds in one role |
| M411 | Region Choice | Shipped example of the table of values for a dynamic M query parameter; it only feeds the parameter, so it has no relationship |
| M009 | [Store Page Link] | Shipped example of the data category WebUrl on a measure: the measure returns text, so it has no format string |
| M009 | [Sales by Store Label] | Shipped example of a label measure for a report in more than one language: the measure returns text, so it has no format string |
| M009 | [Selected Product Image] | Shipped example of the data category ImageUrl on a measure: the measure returns text, so it has no format string |

## 10. Exceptions to the layout standard

| Code | Page | Visual | Reason |
|---|---|---|---|
| V020 | - | - | The examples are in one language; the culture `nl-NL` is there only to show the file form of translations |
| V021 | - | - | The examples are in one language; the culture `nl-NL` is there only to show the file form of translations |
| V016 | AI_Visuals | AI_Visuals_RScript_StoreSales | Shipped example of the R visual, which Microsoft is retiring; it shows the file form only, and is not a model for new work |
| V016 | AI_Visuals | AI_Visuals_PythonScript_StoreSales | Shipped example of the Python visual, which Microsoft is retiring; it shows the file form only, and is not a model for new work |

## 11. Preview features and optional tools the developer agreed to

| Feature or tool | Agreed by | Date | Notes |
|---|---|---|---|
| calendar-based time intelligence | The template (shipped example) | 2026-11-11 | The example under `preview/` exists to show the form; a real project needs the developer's own yes |
| value filter behavior | The template (shipped example) | 2026-11-11 | As above: `preview/ValueFilter.SemanticModel` shows the form only |
| user-context calculated columns | The template (shipped example) | 2026-11-11 | As above: `preview/DirectLakeComposite.SemanticModel` shows the form only |
| calculated tables over Direct Lake | The template (shipped example) | 2026-11-11 | As above: `preview/DirectLakeComposite.SemanticModel` shows the form only |
| Gantt visual | The template (shipped example) | 2026-11-11 | As above: `Charts_Features_Gantt_ProductTasks` shows the form only |
| format string on a visual | The template (shipped example) | 2026-11-11 | As above: `Tables_Features_Table_VisualFormatString` shows the form only |
