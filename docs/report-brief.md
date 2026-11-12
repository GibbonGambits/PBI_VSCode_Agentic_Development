# Report brief

Fill this in before building, and keep it up to date. GitHub Copilot reads it and does not fill gaps by itself: leave a field empty rather than guess. For a meaning the brief does not give, Copilot writes a `TODO(owner)` question in the model, carries on, and asks about all of them at the end of the task. For a fact about the data that no file holds, it asks once. Numbers in brackets are the checklist items a field gives evidence for.

## 1. Purpose and audience

- Report name:
- Who uses it, and which decision or action it supports:
- How they see it: laptop, meeting-room screen, phone, print or export (52, 67, 77):

## 2. Pages

| Tab name | The question this page answers | Notes |
|---|---|---|
| | | |

- Page size in pixels, width x height (52):
- Outer margin in pixels (49):
- Gap between visuals in pixels (49):
- Grid step in pixels (49):

An empty field means the layout standard: 1280 x 720, margin 24, gap 16, grid 8. For a 1920 x 1080 page the standard gives margin 32 and gap 24. An existing report keeps its own page size: write it above. The check script reads these four fields.

## 3. Data

- Semantic model: new in this project / already in this project / a published model (give its name):
- Sources, and the environments they exist in, such as development, test, production (1, 2):
- Import, DirectQuery or both, and why (16):
- How often the data must refresh (45):

## 4. Standards to follow

- Naming standard for tables, columns and measures (7, 28): the standards of this template (business words with spaces, a capital first letter, no technical prefixes), unless another is written here:
- Measure folder subjects (22):
- Acronyms and words with their own spelling (7, 28):
- Measure table: `_Measures`. Copilot makes it: an imported one-column table, or a calculated table when the model reads its data in Direct Lake or DirectQuery mode. Write here if this model differs, and why:
- Facts about the data that Copilot was given or read (row counts, distinct values, unique keys, steps that fold), each with its date and where it came from (3, 11, 14, 17, 31):
- Large tables: row counts, and the decision on incremental refresh or partitions:
- Prefix for report-level measures (empty means an underscore, `_`):
- Excel check on (yes or no):
- Power BI Copilot check on (yes or no):
- Number formats and date formats (71, 72):
- Logos and other brand assets (74):
- Who may see what: security roles, sensitive fields (39, 40, 41):

## 5. Business definitions confirmed by their owners

Copilot writes model descriptions from this table. It does not write business meaning from anywhere else (37, 46, 48).

| Term or measure | Definition, what is left out, caveats | Confirmed by | Date |
|---|---|---|---|
| | | | |

## 6. Decisions and justifications

Record anything a checklist item asks to be justified or done by hand. Examples: Auto date/time turned off in Power BI Desktop (18); why a relationship filters in both directions (12); why a page has more visuals than usual (20).

| Checklist item | Decision or justification | By | Date |
|---|---|---|---|
| | | | |

## 7. Exceptions to "Header icons off, Tooltips off"

Every visual has both off. List each visual that must keep one on, and why. Copilot adds the exception annotation to a visual only when it is listed here, and turns on only what the row names. On an existing report Copilot adds a row itself for a visual that uses drill-down, a help tooltip, a tooltip page or tooltip fields, with the reason "the report uses it"; remove the row to have it switched off.

| Page | Visual | What stays on (header, tooltip or both) | Reason |
|---|---|---|---|
| | | | |

## 8. Known limits to tell users about (75)

-

## 9. Exceptions to the model standard

The model standard is `.github/skills/pbi-semantic-model/references/model-standard.md`. A check passes only for an object listed here with a reason. Code: the finding code, for example `M107`. Object: as the check prints it, `Table[Column]`, `[Measure]` or `Table`. A second measure table is listed with the code `M001` and its table name.

| Code | Object | Reason |
|---|---|---|
| | | |

## 10. Exceptions to the layout standard

The layout standard is `.github/skills/pbi-report/references/layout-standard.md`. Page and Visual: as `python scripts/list_visuals.py .` prints them. For a finding about a whole page (`G007`), write `-` under Visual. A full-page background shape is listed with the code `G004`.

| Code | Page | Visual | Reason |
|---|---|---|---|
| | | | |

## 11. Preview features and optional tools the developer agreed to

Copilot uses a preview feature, or one of Microsoft's optional tools, only after the developer's yes. Write one row for each yes. Feature or tool: for example `calendar-based time intelligence`, `Desktop Bridge`, `Microsoft's modeling server`, `registering the theme in the files`.

| Feature or tool | Agreed by | Date | Notes |
|---|---|---|---|
| | | | |
