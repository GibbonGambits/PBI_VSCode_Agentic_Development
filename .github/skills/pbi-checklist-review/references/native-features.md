# Native features: when to suggest one

## How suggestions work

1. When a native feature would do a job better than what the project does now, Copilot says so in a note at the end of its answer and in the review. Never as a question in the middle of a task.
2. `python scripts/check_project.py .` prints some of these notes by itself, with codes that start with U (next section).
3. The checklist review lists suggestions in a section of their own, apart from the Pass and Fail rows.
4. A suggestion names the feature, what it would replace in this project, and its status: generally available, preview, or retiring.
5. Copilot builds it only after the developer's yes. A preview feature also needs its row in section 11 of `docs/report-brief.md`.
6. Never suggest a custom visual, another vendor's tool, or a feature marked retiring or deprecated.

## What the script notices by itself

| Code | What it sees in the files | Feature it suggests |
|---|---|---|
| U001 | Three or more measures whose formulas (12 tokens or more) have the same shape once names and text are blanked out | DAX user-defined function |
| U002 | Six or more measures that call a time intelligence function, and no calculation group in the model | Calculation group |
| U003 | A measure that uses both SWITCH and SELECTEDVALUE and names three or more objects in brackets, and no field parameter table in the model | Field parameter |
| U004 | Tables in DirectQuery mode, and no column anywhere that is an aggregation of another (`alternateOf`) | User-defined aggregations (an imported aggregation table) |
| U005 | A measure whose formula starts with FORMAT | Dynamic format string |
| U006 | A table at the end of two or more inactive relationships | One copy of the dimension per role (role-playing dimension) |
| U007 | A table with no hierarchy, not a measure table, whose visible columns include Year and Month, Country and City, or Category and Subcategory | Hierarchy |
| U101 | A slicer on one field placed on two or more pages and not synced on all of them (tooltip and drillthrough pages are not counted) | Sync slicers |
| U102 | A page with three or more buttons, shapes or images whose switched-on action goes to a page | Page navigator |
| U103 | Two data visuals of the same type in the same place, which bookmarks show one at a time | Field parameter |

## The list

- "Suggest it when" gives the sign and the Microsoft Learn page that states it. A feature with no such page is never suggested on its own; Copilot builds it when the developer asks.
- "Instead of" names a workaround only where Microsoft names one; "-" means it does not.
- GA also stands for a feature whose Learn page carries no preview or retiring label. Preview and retiring statuses are as Microsoft stated them on 11 November 2026.
- In the last column, a file name is followed by its skill; codes are findings of `python scripts/check_project.py .`; "example" means `tests/fixtures/examples/INDEX.md` lists a shipped one.

### Model

| Feature | Suggest it when (the sign in the files or in the request) | Instead of | Status | Where it is covered here |
|---|---|---|---|---|
| Calculation groups (with selection expressions) | Many measures are variants of others: time periods, currency conversion. https://learn.microsoft.com/en-us/power-bi/transform-model/calculation-groups | One measure per variant (Sales YTD, Sales PY, ...) | GA | `dax-standard.md` and `model-objects.md` (pbi-semantic-model); U002, M811-M814; example |
| Field parameters | Readers should switch the measures or fields a visual shows, from a slicer. https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters | - | GA | `report-standard.md` (pbi-report), `model-objects.md` (pbi-semantic-model); U003, U103, M821, M822; item 64; example |
| Numeric range (what-if) parameters | No Microsoft guidance on when: not suggested by itself | - | GA | `model-objects.md` (pbi-semantic-model); example |
| Hierarchies | Columns form a natural drill path, such as calendar or product levels. https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization | - | GA | `relationships-and-dates.md` (pbi-semantic-model); U007, M902, M119; item 59; example |
| Display folders | Columns of one thing are split over a second table only to group them. https://learn.microsoft.com/en-us/power-bi/guidance/relationships-one-to-one | A second table related one-to-one | GA | `model-standard.md` (pbi-semantic-model); M003, M004; example |
| Descriptions (`///` lines; also written in DAX query view or by Copilot in Power BI) | Tables, columns or measures lack a line on what they hold and how to use them. https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization | - | GA | `descriptions.md` (pbi-semantic-model); D001 |
| Data categories (place, web URL, image URL, barcode, mobile geo-filtering) | A column holds places, links or images. https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization | - | GA | `relationships-and-dates.md` (pbi-semantic-model); M114; example |
| Sort by column | Month names or other labels sort A to Z instead of in their own order. https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-sort-by-column | - | GA | `relationships-and-dates.md` (pbi-semantic-model); M113, M903; example |
| Data types and format strings | An amount used in sums or RANKX is a Decimal number (floating point). https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-data-types | Decimal number, or rounding in each formula | GA | `model-standard.md`, `storage-and-security.md` (pbi-semantic-model); M009, M109, M110, M112 |
| Hide fields, summarization, Is available in MDX | Authors can pick keys, or sum a number that must never be summed. https://learn.microsoft.com/en-us/power-bi/guidance/star-schema | - | GA | `model-standard.md` (pbi-semantic-model); M102, M103, M107, M301, M907; example |
| Auto date/time | Only for simple calendars or ad hoc models; this template keeps it off. https://learn.microsoft.com/en-us/power-bi/guidance/auto-date-time | - | GA | `relationships-and-dates.md` (pbi-semantic-model); M401 |
| Mark as date table | Classic time intelligence functions are used, or dates relate through a whole-number key. https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables | - | GA | `relationships-and-dates.md` (pbi-semantic-model); M402-M404; example |
| Calendars (calendar-based time intelligence) | Fiscal, week-based or other non-Gregorian calendars, or best speed. https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-time-intelligence | Offset columns; in most cases the marked date table | Preview (needs the developer's yes) | `relationships-and-dates.md` (pbi-semantic-model); example |
| Relationships: one-to-many, one-to-one | One-to-one only for a part split off a fact table with matching rows. https://learn.microsoft.com/en-us/power-bi/guidance/relationships-one-to-one | - | GA | `relationships-and-dates.md` (pbi-semantic-model); M409, M413, M901; example |
| Inactive relationships, or one dimension copy per role | A copy per role when visuals must filter by several roles at once; otherwise inactive plus USERELATIONSHIP. https://learn.microsoft.com/en-us/power-bi/guidance/relationships-active-inactive | Special measures per role | GA | `relationships-and-dates.md` (pbi-semantic-model); U006, M410, M414, M415; example |
| Many-to-many relationships | Facts at a coarser grain than a dimension that is not a date. https://learn.microsoft.com/en-us/power-bi/guidance/relationships-many-to-many | - | GA | `relationships-and-dates.md` (pbi-semantic-model); M406, M407; example |
| Filtering in both directions | One relationship of a many-to-many bridge must carry filters to the facts. https://learn.microsoft.com/en-us/power-bi/guidance/relationships-bidirectional-filtering | - | GA | `relationships-and-dates.md` (pbi-semantic-model); M405, M408; example |
| Row-level security | One report serves many audiences, filtered by who signs in. https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security | - | GA | `storage-and-security.md` (pbi-semantic-model); M601-M605; example |
| Object-level security | A table or column, name included, must be out of a role's reach. https://learn.microsoft.com/en-us/fabric/security/service-admin-object-level-security | Hiding the field (not security) | GA | `storage-and-security.md` (pbi-semantic-model); M606-M608; example |
| Perspectives | Personalize visuals or Explore should offer a smaller field list (not security). https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-personalize-visuals | - | GA | `model-objects.md` (pbi-semantic-model); M831; example |
| Translations (cultures) | No Microsoft guidance on when: not suggested by itself | - | GA | `model-objects.md` (pbi-semantic-model); example |
| KPIs and detail rows (model objects) | No Microsoft guidance on when: not suggested by itself | - | KPIs GA; detail rows: no status stated by Microsoft | `model-objects.md` (pbi-semantic-model); example |
| Grouping and binning | No Microsoft guidance on when: not suggested by itself | - | GA | `model-standard.md` (pbi-semantic-model) |
| Value filter behavior (Coalesced, Independent) | No Microsoft guidance on when: not suggested by itself | - | Preview (needs the developer's yes) | - |
| Prep data for AI (AI data schema, AI instructions, verified answers) | No Microsoft guidance on when: not suggested by itself | - | Preview (needs the developer's yes) | `model-standard.md` (pbi-semantic-model), rule 17 |
| Linguistic schema and synonyms for Q&A | Never: goes with Q&A | - | Deprecated (Q&A ends December 2026 or February 2027; Learn pages differ): do not suggest; say it is retiring when you find one in a report | `model-standard.md` (pbi-semantic-model); example |
| Unicode character behavior (GB18030-2022) | The organization must comply with GB18030-2022. https://learn.microsoft.com/en-us/dax/best-practices/dax-unicode-character-behavior | - | GA | - |

### DAX

| Feature | Suggest it when (the sign in the files or in the request) | Instead of | Status | Where it is covered here |
|---|---|---|---|---|
| Measures and quick measures | Authors summarize columns, or use Excel PivotTables, which need explicit measures. https://learn.microsoft.com/en-us/power-bi/guidance/star-schema | Implicit sums of columns | GA | `model-standard.md` (pbi-semantic-model); M103, M107; example |
| Calculated columns (user-context-aware ones too) | Only when the formula needs measures or DAX-only functions. https://learn.microsoft.com/en-us/power-bi/guidance/import-modeling-data-reduction | - | GA; user-context-aware columns preview (needs the developer's yes) | `model-standard.md`, `storage-and-security.md` (pbi-semantic-model); M105, M106; example |
| Calculated tables | A date table from CALENDAR or CALENDARAUTO, or a copy of a dimension for a role. https://learn.microsoft.com/en-us/power-bi/guidance/model-date-tables | - | GA | `relationships-and-dates.md` (pbi-semantic-model); M105; example |
| User-defined functions | Many measures or columns repeat one formula. https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-user-defined-functions-overview | The same formula copied into each measure | GA | `dax-standard.md`, `model-objects.md` (pbi-semantic-model); U001, M801-M805; example |
| Dynamic format strings | A measure turns its number into text to format it. https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-dynamic-format-strings | FORMAT, which returns text that no longer sorts or charts | GA | `dax-standard.md` (pbi-semantic-model); U005; example |
| Visual calculations | Running sums, moving averages, percent of parent or previous-item comparisons inside one visual. https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-visual-calculations-overview | An equivalent model measure (Microsoft: often slower) | GA; ORDERBY parameter preview (needs the developer's yes) | `report-standard.md` (pbi-report), section L; example |
| Functions Microsoft prefers: DIVIDE, COUNTROWS, SELECTEDVALUE, VAR, KEEPFILTERS | A formula divides with `/` by an expression, counts a column to count rows, tests HASONEVALUE then VALUES, repeats an expression, or filters a whole table. https://learn.microsoft.com/en-us/dax/best-practices/dax-divide-function-operator and its sibling pages | `/`, COUNT, IF with VALUES, repeated code, FILTER over a table | GA | `dax-standard.md` (pbi-semantic-model); M501-M507, M517 |
| Classic time intelligence functions | No Microsoft guidance on when: not suggested by itself (they need a marked date table) | - | GA | `dax-standard.md` (pbi-semantic-model); M402, M513; example |
| Window functions (WINDOW, OFFSET, INDEX, RANK, ROWNUMBER) | No Microsoft guidance on when: not suggested by itself | - | GA | `dax-standard.md` (pbi-semantic-model); M516 |
| Other function families: NAMEOF, TABLEOF, INFO, SELECTEDMEASURE, EXTERNALMEASURE, LINEST, TOJSON, USERCULTURE, USERPRINCIPALNAME, EVALUATEANDLOG | No Microsoft guidance on when: not suggested by itself | - | GA; new NAMEOF options preview | `dax-functions.md` (pbi-semantic-model); M512 (EVALUATEANDLOG left in) |
| APPROXIMATEDISTINCTCOUNT on Import, full-text search functions | No Microsoft guidance on when: not suggested by itself | - | Preview (needs the developer's yes) | - |

### Power Query and storage

| Feature | Suggest it when (the sign in the files or in the request) | Instead of | Status | Where it is covered here |
|---|---|---|---|---|
| Import mode | The default choice. https://learn.microsoft.com/en-us/power-bi/guidance/composite-model-guidance | - | GA | `storage-and-security.md` (pbi-semantic-model), rule 22 |
| DirectQuery mode | Data too big to import, or needed near real time, from one source. https://learn.microsoft.com/en-us/power-bi/guidance/composite-model-guidance | - | GA | `storage-and-security.md` (pbi-semantic-model); M513, M701-M706; example |
| Dual mode | Dimensions are queried with DirectQuery facts from the same source. https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-storage-mode | Limited relationships between Import and DirectQuery tables | GA | `storage-and-security.md` (pbi-semantic-model); example |
| Assume referential integrity | DirectQuery relationships whose many side has no blank or unmatched keys. https://learn.microsoft.com/en-us/power-bi/guidance/directquery-model-guidance | - | GA | `storage-and-security.md` (pbi-semantic-model), rule 24 |
| Composite models (also on a published model; option to discourage DirectQuery to this one) | A DirectQuery model would gain from Dual tables and aggregations. https://learn.microsoft.com/en-us/power-bi/guidance/directquery-model-guidance | - | GA | `storage-and-security.md` (pbi-semantic-model), rule 23 |
| Live connection to a published model | Modelers and report authors differ, or one model feeds several reports. https://learn.microsoft.com/en-us/power-bi/guidance/report-separate-from-model | A model copied into each report file | GA | `report-standard.md` (pbi-report), section L |
| Direct Lake (on OneLake, on SQL; also from Fabric SQL and mirrored databases) | Data already in Fabric Delta tables is too large to import. https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview | Copying the data by import | GA | `storage-and-security.md` (pbi-semantic-model), rule 27; example |
| Direct Lake with Import tables, calculated columns or calculated tables | No Microsoft guidance on when: not suggested by itself | - | Preview (needs the developer's yes) | `storage-and-security.md` (pbi-semantic-model) |
| User-defined aggregations | A very large DirectQuery fact table answers summary queries slowly. https://learn.microsoft.com/en-us/power-bi/transform-model/aggregations-advanced | - | GA | `storage-and-security.md` (pbi-semantic-model), rule 25; U004; item 17; example |
| Incremental refresh | A large fact table keeps growing. https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview | - | GA | `model-standard.md` rule 14, `storage-and-security.md` rule 26 (pbi-semantic-model); M707-M709; example |
| Hybrid tables (real-time DirectQuery partition) | The newest rows of an incrementally refreshed table must be real time. https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview | Frequent refreshes | GA | `storage-and-security.md` (pbi-semantic-model), rule 26 |
| Partitions | No Microsoft guidance on when: not suggested by itself | - | GA | `model-standard.md` (pbi-semantic-model), rule 14; M117 |
| Query folding | Always for DirectQuery and Dual; for Import from a database, as far as it goes. https://learn.microsoft.com/en-us/power-bi/guidance/power-query-folding | - | GA | `storage-and-security.md` (pbi-semantic-model), rules 2-3; P002, M701; item 3 |
| Query parameters | A server, database or other value is typed into several queries. https://learn.microsoft.com/en-us/power-query/best-practices | The same literal in each query | GA | `storage-and-security.md` (pbi-semantic-model), rule 8; example |
| Enable load off, Include in report refresh off | A query only feeds other queries, or a source never changes. https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-include-in-report-refresh | Loading staging queries as tables | GA | `storage-and-security.md` (pbi-semantic-model), rule 12; example |
| Power Query columns (custom column, column from examples) | A new column needs no measure and no DAX-only function. https://learn.microsoft.com/en-us/power-bi/guidance/import-modeling-data-reduction | A DAX calculated column | GA | `storage-and-security.md` (pbi-semantic-model), rule 17; M105 |
| Other Power Query features: dynamic M query parameters, combine files, fuzzy matching, enter data, Python and R scripts | No Microsoft guidance on when: not suggested by itself | - | GA | `storage-and-security.md` (pbi-semantic-model); example (entered table) |
| Dataflow (Gen1) as a source | Never: Microsoft labels it legacy and points to Dataflow Gen2 | - | Deprecated (legacy): do not suggest; say it is legacy when you find one in a report | `storage-and-security.md` (pbi-semantic-model) |

### Report pages and navigation

| Feature | Suggest it when (the sign in the files or in the request) | Instead of | Status | Where it is covered here |
|---|---|---|---|---|
| Pages: size, hidden pages, page tabs, landing page, automatic page refresh | No Microsoft guidance on when: not suggested by itself | - | GA | `layout-standard.md`, `pages-and-visuals.md` (pbi-report); V011 |
| Filters pane: lock, hide, format | A filter only cleans data, or readers may see but not change it. https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-report-filter | - | GA | `report-standard.md` (pbi-report), section I; example |
| Filter types: Top N, relative date, include and exclude | A table visual over a large table has no restrictive filter. https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization | - | GA | `report-standard.md` (pbi-report); example |
| Visual interactions | Visuals cross-filter each other where nobody needs it, above all on DirectQuery. https://learn.microsoft.com/en-us/power-bi/guidance/directquery-model-guidance | - | GA | item 60; example |
| Query reduction (Apply buttons, no cross-highlighting) | The report runs on DirectQuery. https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-optimize-ribbon | A query on every slicer click | GA | item 69 |
| Report settings: persistent filters, personalize visuals, query limits, format locale | Turn persistent filters off when bookmarks drive the report. https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-troubleshoot | - | GA | `report-standard.md` (pbi-report) |
| Drillthrough (also across reports, service only) | Readers go from a summary to a page about one item, or need to interact with the detail. https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-drillthrough | Detail visuals crowding the summary page | GA | `report-standard.md` (pbi-report), section D; V001; example |
| Report page tooltips | Readers need more detail on hover without leaving the page. https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-tooltips | Extra visuals on the page | GA | `report-standard.md` section C, `theme.md` (pbi-report); V002-V005; example |
| Bookmarks | No Microsoft guidance on when: not suggested by itself | - | GA | `report-standard.md` (pbi-report), section B; V010; example |
| Buttons and their actions | A button only changes page: use the page navigation action. https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-buttons | A bookmark per destination | GA | `report-standard.md` (pbi-report), section B; V008; example |
| Page navigator, bookmark navigator | A row of buttons leads to pages or bookmarks one by one. https://learn.microsoft.com/en-us/power-bi/create-reports/button-navigators | Hand-built rows of buttons | GA | `report-standard.md` (pbi-report), rule 12; U102; example |
| Apply all slicers, Clear all slicers buttons | A page has many slicers. https://learn.microsoft.com/en-us/power-bi/create-reports/buttons-apply-all-clear-all-slicers | A query after each slicer change | GA | `report-standard.md` (pbi-report) |
| Sync slicers (and sync groups) | One selection must hold on several pages, or across source groups of a composite model. https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-slicers | A relationship across source groups | GA | `report-standard.md` (pbi-report), section E; U101; item 61; example |
| Mobile layout | The report is read on phones. https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-create-mobile-optimized-report-about | - | GA | `report-standard.md` (pbi-report), section G |
| Report-level measures | The report sits on a live connection and needs a measure of its own. https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-report-lifecycle-datasets | - | GA | `report-standard.md` (pbi-report), section L; example |
| Themes (with style presets) | Visuals need the same title and text styles. https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-customize-title-background-and-legend | Formatting each visual by hand | GA; organizational themes preview | `theme.md` (pbi-report); T001, V009 |
| Drill mode, multi-select, lasso, groups, spotlight | No Microsoft guidance on when: not suggested by itself | - | GA | `layout-standard.md` (pbi-report); example (group) |
| Translytical task flows (data function buttons) | No Microsoft guidance on when: not suggested by itself (needs Fabric user data functions) | - | GA | - |

### Visuals

| Feature | Suggest it when (the sign in the files or in the request) | Instead of | Status | Where it is covered here |
|---|---|---|---|---|
| Bar and column charts (stacked, clustered, 100%) | Comparing categories: columns over time, bars for long names. https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualizations-overview | - | GA | `report-standard.md` (pbi-report), section H; example |
| Line and area charts (stacked, 100%) | A trend over a continuous axis; areas for the size of change. https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualizations-overview | - | GA | `report-standard.md` (pbi-report), section H; example |
| Combo charts (line with stacked or clustered columns) | Two measures with very different ranges. https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-tips-and-tricks-for-creating-reports | Millions and thousands on one axis | GA | `report-standard.md` (pbi-report), section H; example |
| Ribbon, waterfall and funnel charts | Changes of rank; running increases and decreases; stages in sequence. https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualizations-overview | - | GA | `report-standard.md` (pbi-report), section H; example |
| Scatter and bubble charts | Two measures that may move together; give it a Details field. https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualizations-overview | - | GA | example |
| Pie, donut and treemap | Part of a whole with fewer than eight slices; treemap for large hierarchies. https://learn.microsoft.com/en-us/power-bi/create-reports/service-dashboards-design-tips | - | GA | `report-standard.md` (pbi-report), section H; example |
| Azure Maps | A report has a map or filled map. https://learn.microsoft.com/en-us/azure/azure-maps/power-bi-visual-conversion | Map and filled map (Bing) | GA | example |
| Shape map | No Microsoft guidance on when: not suggested by itself | - | GA by the June 2026 release notes; some Learn pages still say preview | example |
| Card (new), KPI, gauge | One key number; progress to a goal; status against a goal. https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualizations-overview | - | GA | example |
| Card (legacy), multi-row card | Many single-number cards on a DirectQuery page: one multi-row card. https://learn.microsoft.com/en-us/power-bi/guidance/directquery-model-guidance | Many cards | Legacy card GA; multi-row card: no status stated | example |
| Slicer (list, dropdown, between, relative date, date picker, hierarchy), button slicer, input slicer | A slicer should list only items with data: filter it with a measure. https://learn.microsoft.com/en-us/power-bi/guidance/relationships-bidirectional-filtering | A both-direction relationship | GA | `report-standard.md` (pbi-report); example |
| List slicer | No Microsoft guidance on when: not suggested by itself | - | Preview (needs the developer's yes) | example |
| Table and matrix | Exact values; a matrix for several dimensions and drill. https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualizations-overview | - | GA | example |
| Totals, subtotals, custom totals | On DirectQuery, switch off totals nobody needs. https://learn.microsoft.com/en-us/power-bi/guidance/directquery-model-guidance | - | GA | - |
| Small multiples | The same chart is copied once per category. https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualizations-overview | Several copies of one chart | GA; on the new card preview | - |
| Conditional formatting (tables, chart lines, legends, plot area) | Colours should come from one measure, consistent across visuals. https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-conditional-formatting | Many rules in the dialog | GA | `report-standard.md` (pbi-report), section F; example |
| Titles from a measure | A title must follow the selection or the reader's language. https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-conditional-format-visual-titles | - | GA | `report-standard.md` (pbi-report), section I; A003 |
| Show items with no data | Every group must show even without a value. https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-converting-blank | A measure that turns blank into zero | GA | `dax-standard.md` (pbi-semantic-model); M506 |
| Text box, image, shapes | A result does not add up, and readers need a line on why. https://learn.microsoft.com/en-us/power-bi/guidance/relationships-many-to-many | - | GA | `layout-standard.md` (pbi-report); example |
| Accessibility: alt text, tab order, Selection pane | Always, before publishing. https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports | - | GA | `report-standard.md` (pbi-report), section J; A001-A004 |
| Decomposition tree, key influencers, narrative visual (smart narrative, Copilot mode) | No Microsoft guidance on when: not suggested by itself | - | GA | example |
| Paginated report visual, Power Apps and Power Automate visuals | No Microsoft guidance on when: not suggested by itself | - | GA | example (paginated); the other two not built |
| Metrics (scorecard) visual, Gantt (core visual) | No Microsoft guidance on when: not suggested by itself | - | Metrics GA; Gantt preview (needs the developer's yes) | not built |
| Analytics pane, show value as, high-density sampling, sparklines | No Microsoft guidance on when: not suggested by itself | - | GA (sparklines: some Learn pages still say preview) | - |
| Format pane and axis options | No Microsoft guidance on when: not suggested by itself | - | GA | `theme.md` (pbi-report); V009 |
| Visual tooltips, help tooltips, visual header icons | No Microsoft guidance on when: not suggested by itself | - | GA | `theme.md` (pbi-report): off unless the brief lists an exception; H001, H002 |
| Links and images in tables and matrices | No Microsoft guidance on when: not suggested by itself | - | GA | example (web URL category) |
| Visual-level format strings | No Microsoft guidance on when: not suggested by itself | - | Preview at the last release note (needs the developer's yes) | - |
| Retiring visuals: Q&A visual, map, filled map, R and Python visuals | Never | Azure Maps for the two maps | Retiring (Q&A December 2026 or February 2027; maps without a date; R and Python May 2027): do not suggest; say it is retiring when you find one in a report | not built, except R and Python (empty) |

### Tooling Copilot can use

| Feature | Suggest it when (the sign in the files or in the request) | Instead of | Status | Where it is covered here |
|---|---|---|---|---|
| Power BI Project format: PBIR report, TMDL model, public JSON schemas, diagram layout, enhanced metadata | Required here: without it the check stops with F001 | - | GA | `tmdl.md` (pbi-semantic-model), `pages-and-visuals.md` (pbi-report) |
| Editing a project outside Desktop, then reloading | No Microsoft guidance on when: not suggested by itself | - | Preview (needs the developer's yes) | `desktop-bridge.md` (pbi-report) |
| Git for project files (also build pipelines and fabric-cicd) | No Microsoft guidance on when: not suggested by itself | - | GA | `.github/copilot-instructions.md` (work on a branch; no deploying) |
| TMDL extension for Visual Studio Code | No Microsoft guidance on when: not suggested by itself | - | GA | `tmdl.md` (pbi-semantic-model) |
| Power BI modeling MCP server (local) | No Microsoft guidance on when: not suggested by itself | - | GA | `.github/copilot-instructions.md`: read and check only, never change a model through it |
| Report skill and semantic model authoring skill (agentic experiences) | No Microsoft guidance on when: not suggested by itself | - | Report skill GA; model authoring skill preview | Not called by this template |
| Report pages made by Copilot in Power BI | No Microsoft guidance on when: not suggested by itself | - | GA (the Desktop entry point is preview) | - |

### Outside the project files

These live in Power BI Desktop options, the Power BI service or Fabric, not in the project files. They are outside this template: Copilot may name one to explain a gap or answer a question, and never sets one up.

| Feature | What it is for | Status |
|---|---|---|
| Sensitivity labels | Classify and protect content; not supported in PBIP files | GA |
| Endorsement (promoted, certified) | Show which content others can trust | GA |
| Email subscriptions, also per recipient | Send pages on a schedule | GA; Copilot summaries in them preview |
| Alerts: data alerts on dashboard tiles, Set alert (Fabric Activator) on visuals | Warn or act when a value passes a threshold | GA (the Activator article still says preview) |
| Deployment pipelines | Move content from development to test to production | GA (new interface preview) |
| Fabric Git integration | Keep a workspace in a repository | GA (some item types preview) |
| Semantic model version history | Restore an earlier state of a model edited in the service | GA |
| Performance Analyzer (Desktop and web) | Time each visual's query and drawing | GA |
| DAX query view | Write and run DAX queries | GA |
| TMDL view | Edit the model as script inside Desktop | GA in Desktop; preview on the web |
| Model explorer and Model view | Browse model objects; diagrams | GA by the May 2024 note; one Learn heading still says preview |
| Copilot in Power BI (report pane, Desktop pane, standalone, DAX queries) | Summaries, answers, drafts of pages and queries | Report pane GA; Desktop and standalone preview; DAX queries unclear |
| Q&A (setup, teach Q&A, featured questions) | Questions in plain language | Deprecated (December 2026 or February 2027) |
| Explore | Ad hoc analysis of a model | Preview |
| Metrics and scorecards | Track goals | GA (scorecard hierarchies removed April 2026) |
| Workspace apps and org apps, with audiences | Hand content to groups of readers | GA |
| Export: data from a visual, PDF, PowerPoint | Take content out of the service | GA |
| Publish to web, secure embed, SharePoint and Teams | Show reports in other places | GA |
| Dashboards, personal bookmarks, comments | Tiles from several reports; readers keep views and discuss | GA |
| Analyze in Excel, featured tables | Use the model from Excel | GA |
| Paginated reports | Pixel-exact, printable reports | GA |
| Dataflows | Shared Power Query logic outside a model | Gen1 labelled legacy |
| Refresh in the service: schedules, summaries, enhanced refresh, partitions made by incremental refresh | Keep data current | GA |
| XMLA endpoint | Read and write models with tools | GA |
| Lineage view and impact analysis | See what depends on a model | GA |
| Usage metrics | See who opens a report | Classic GA; new preview |
| Web modeling (Copilot in it too) | Edit a model in the browser | GA; Copilot in it preview |
| On-premises data gateway, cloud connections | Reach sources from the service | GA |
| Large model storage format, scale-out, query caching | Capacity settings for big or busy models | GA |
| Query diagnostics, data profiling | See what Power Query does and what the data holds | GA |
| Power BI Desktop Bridge | Link an agent to a running Desktop | Preview by the external editing page |
| Desktop options: gridlines, on-object formatting, Design ribbon, parallel loading | How Desktop looks and loads | GA; on-object preview |
| Optimize ribbon, report templates (.pbit), external tools ribbon, notebooks with semantic link | Authoring aids around the model | GA |

The full inventory of native features, with versions and limits, is kept in the template's maintenance papers.

## Sources

Microsoft Learn, read on 11 November 2026, restated in this template's own words:

- Release notes: https://learn.microsoft.com/en-us/power-bi/fundamentals/whats-new ; https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-latest-update-archive
- Guidance: https://learn.microsoft.com/en-us/power-bi/guidance/ (optimization, star schema, data reduction, date tables, auto date/time, relationship pages, DirectQuery, composite models, RLS, separate reports, tooltips, drillthrough)
- DAX best practices: https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions and its sibling pages
- Model: https://learn.microsoft.com/en-us/power-bi/transform-model/calculation-groups ; https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-dynamic-format-strings ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-time-intelligence ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-storage-mode ; https://learn.microsoft.com/en-us/power-bi/transform-model/aggregations-advanced ; https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview ; https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview
- Security: https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security ; https://learn.microsoft.com/en-us/fabric/security/service-admin-object-level-security
- Report: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters ; https://learn.microsoft.com/en-us/power-bi/create-reports/button-navigators ; https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-slicers ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-visual-calculations-overview ; https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualizations-overview ; https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports
- Power Query: https://learn.microsoft.com/en-us/power-query/best-practices ; https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-include-in-report-refresh
- Project files: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview ; https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report

Checklist items: 17, 59, 61, 64
