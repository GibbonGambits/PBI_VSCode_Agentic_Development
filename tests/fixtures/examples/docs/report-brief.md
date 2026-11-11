# Report brief

Brief for the shipped model examples in this folder. The models hold one working example of every semantic model object kind, with made-up data for a small shop. They are not a report. The project check reads section 9 of this file when it runs on this folder.

## 1. Purpose and audience

- Report name: none; model examples only.
- Who uses it, and which decision or action it supports: Developers and the coding assistant of this template, who copy an example when a project has none of its own.
- How they see it: laptop, meeting-room screen, phone, print or export (52, 67, 77): not applicable.

## 2. Pages

| Tab name | The question this page answers | Notes |
|---|---|---|
| | | No pages: these examples hold models only. |

- Page size in pixels, width x height (52):
- Outer margin in pixels (49):
- Gap between visuals in pixels (49):
- Grid step in pixels (49):

## 3. Data

- Semantic model: four example models in this folder: Examples.SemanticModel (import), storage/DirectQuery.SemanticModel (composite: DirectQuery, Dual and an imported aggregation table), storage/DirectLake.SemanticModel (Direct Lake), preview/Calendar.SemanticModel (a preview feature).
- Sources, and the environments they exist in, such as development, test, production (1, 2): made-up data written in the queries, or made-up source names.
- Import, DirectQuery or both, and why (16): one example model for each storage mode.
- How often the data must refresh (45): not applicable.

## 4. Standards to follow

- Naming standard for tables, columns and measures (7, 28): the model standard of this template.
- Measure folder subjects (22):
- Acronyms and words with their own spelling (7, 28):
- Measure table: `_Measures`, made in Power BI Desktop with Enter data; for a Direct Lake model a calculated table. Write here if this model differs, and why: the DirectQuery example also uses a calculated table, so that the measure table adds no import table.
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
| M414 | model | Shipped examples of security roles and of an inactive relationship (ship date) in one model |
| M607 | model | Shipped examples show a role with row rules and a role with object rules side by side; a real model puts both kinds in one role |
| M009 | [Store Page Link] | Shipped example of the data category WebUrl on a measure: the measure returns text, so it has no format string |

## 10. Exceptions to the layout standard

| Code | Page | Visual | Reason |
|---|---|---|---|
| | | | |

## 11. Preview features and optional tools the developer agreed to

| Feature or tool | Agreed by | Date | Notes |
|---|---|---|---|
| calendar-based time intelligence | The template (shipped example) | 2026-11-11 | The example under `preview/` exists to show the form; a real project needs the developer's own yes |
