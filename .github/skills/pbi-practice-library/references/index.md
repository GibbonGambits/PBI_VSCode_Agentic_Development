# Practice library: index

Read this file first, then open only the file that fits the task, two at most. Never read the whole library for one task.

Each entry names one file in this folder, what it covers, and the DAX functions and Power BI features its notes mention (most frequent first). A function is listed when a note names it; a function or feature can appear in several files, so pick the file whose topic fits the question. How to use a note is set out in the skill file one folder up.

| Topic | Files | Notes |
|---|---|---:|
| DAX evaluation context | `t01-evaluation-context-1.md` to `t01-evaluation-context-2.md` | 154 |
| DAX authoring style | `t02-dax-authoring-style-1.md` to `t02-dax-authoring-style-2.md` | 108 |
| DAX table functions and queries | `t03-table-functions-and-queries-1.md` to `t03-table-functions-and-queries-2.md` | 154 |
| Time intelligence and date tables | `t04-time-intelligence-and-dates-1.md` to `t04-time-intelligence-and-dates-2.md` | 149 |
| Relationships and filter propagation | `t05-relationships-1.md` | 67 |
| Data model design | `t06-data-model-design-1.md` to `t06-data-model-design-2.md` | 116 |
| DAX performance and optimization | `t07-dax-performance-1.md` to `t07-dax-performance-3.md` | 171 |
| Storage engine, model size and memory | `t08-storage-engine-and-model-size-1.md` | 29 |
| Storage modes | `t09-storage-modes-1.md` to `t09-storage-modes-2.md` | 86 |
| Security | `t10-security-1.md` | 43 |
| Calculation groups and field parameters | `t11-calculation-groups-and-field-parameters-1.md` to `t11-calculation-groups-and-field-parameters-2.md` | 85 |
| Window functions and visual calculations | `t12-window-functions-and-visual-calculations-1.md` | 77 |
| User-defined functions in DAX | `t13-user-defined-functions-1.md` | 47 |
| Business calculation patterns | `t14-business-calculation-patterns-1.md` to `t14-business-calculation-patterns-4.md` | 243 |
| Report-facing DAX and report design | `t15-report-facing-dax-1.md` to `t15-report-facing-dax-4.md` | 252 |
| Tooling, workflow and AI assistance | `t16-tooling-and-workflow-1.md` to `t16-tooling-and-workflow-2.md` | 111 |

## DAX evaluation context

### `t01-evaluation-context-1.md` (82 notes)

- Covers: KEEPFILTERS and arbitrary filters; CALCULATE filter arguments; Visual queries and auto-exist; Reading the selected value; Row context and iterators.
- DAX functions: CALCULATE, KEEPFILTERS, FILTER, VALUES, ALL, SELECTEDVALUE, CROSSJOIN, CALCULATETABLE, SUMMARIZE, SUMX, HASONEVALUE, ISINSCOPE, RELATED, TRUE, SUM, SUMMARIZECOLUMNS, OR, AVERAGEX, AND, ISFILTERED, DISTINCT, REMOVEFILTERS, LASTDATE, IF, CROSSFILTER, ERROR, FALSE, RELATEDTABLE, MIN, AVERAGE, MAX, SELECTCOLUMNS, MINX, MAXX.
- Features: iterators, DAX queries, filter context, row context, slicers, error handling, relationships, totals and subtotals, context transition, cardinality, auto-exist, blank handling, Excel and MDX clients, variables, calculated columns, storage engine, sort by column, blank row of an invalid relationship, matrix visual, expanded tables, hierarchies, dimension tables, parameter tables.

### `t01-evaluation-context-2.md` (72 notes)

- Covers: Relationships, expanded tables and lineage; Context transition; Removing filters with ALL; ALLSELECTED and shadow filters; Totals and additivity.
- DAX functions: CALCULATE, ALL, ALLSELECTED, REMOVEFILTERS, RELATED, CALCULATETABLE, VALUES, ALLEXCEPT, FILTER, RELATEDTABLE, ALLCROSSFILTERED, MAX, SUMMARIZE, USERELATIONSHIP, ADDCOLUMNS, TREATAS, SELECTEDVALUE, LASTDATE, COUNTROWS, MIN, EARLIER, DISTINCT, MINX, MAXX, SUMMARIZECOLUMNS.
- Features: iterators, filter context, row context, relationships, context transition, calculated columns, totals and subtotals, fact tables, shadow filter context, dimension tables, DAX queries, expanded tables, variables, error handling, limited relationships, Excel and MDX clients, data lineage, budget and forecast, inactive relationships, matrix visual, bidirectional filters, virtual relationships, DirectQuery.

## DAX authoring style

### `t02-dax-authoring-style-1.md` (47 notes)

- Covers: Variables and their evaluation; BLANK handling and conditions.
- DAX functions: IF, BLANK, DIVIDE, SWITCH, CALCULATE, ISBLANK, COALESCE, VAR, SUMX, DISTINCT, VALUES, ADDCOLUMNS, TOPN, FALSE, ALL, FILTER, CONCATENATEX, RELATEDTABLE, ERROR, COUNTROWS, MAXX, MINX, AVERAGEX.
- Features: variables, blank handling, iterators, DAX queries, filter context, error handling, blank row of an invalid relationship, relationships, data types, Excel and MDX clients, totals and subtotals.

### `t02-dax-authoring-style-2.md` (61 notes)

- Covers: IN operator and constructors; Formatting, naming and references; Data types and comparisons.
- DAX functions: CALCULATE, OR, NOT, TREATAS, FILTER, ALL, ADDCOLUMNS, CONTAINSROW, CONTAINS, CALCULATETABLE, SUMX, EXCEPT, VALUES, AND, SUMMARIZE, ISEMPTY, INTERSECT, TOPN, UNION, INT, CONVERT.
- Features: error handling, data types, variables, iterators, testing and debugging, virtual relationships, row context, calculated tables, data lineage, fact tables, currency conversion, naming, DAX queries, DAX formatting, conditional formatting.

## DAX table functions and queries

### `t03-table-functions-and-queries-1.md` (79 notes)

- Covers: Grouping and adding columns; Writing DAX queries; Filter and text conditions.
- DAX functions: SUMMARIZE, ADDCOLUMNS, CALCULATE, GROUPBY, CALCULATETABLE, FILTER, CURRENTGROUP, SEARCH, SELECTCOLUMNS, DEFINE, EVALUATE, CONTAINSSTRING, DETAILROWS, CONTAINS, MAXX, TOPNSKIP, VALUES, GENERATE, ROW, DISTINCT, LEFT, ISEMPTY, ALL, FIND, AND, SUM, OR, DATATABLE, TREATAS, KEEPFILTERS, REMOVEFILTERS, MAX, BLANK, CROSSJOIN, ALLEXCEPT, CONTAINSSTRINGEXACT, SUBSTITUTE, RIGHT, RELATEDTABLE.
- Features: DAX queries, iterators, variables, relationships, Excel and MDX clients, filter context, blank handling, totals and subtotals, row context, context transition, fact tables, materialization, slicers, expanded tables, dimension tables, formula engine, row-level security, query plans, testing and debugging, blank row of an invalid relationship, detail rows.

### `t03-table-functions-and-queries-2.md` (75 notes)

- Covers: Calculated and static tables; SUMMARIZECOLUMNS behaviour; Joins and lookups; Set functions.
- DAX functions: SUMMARIZECOLUMNS, LOOKUPVALUE, NATURALLEFTOUTERJOIN, SUMMARIZE, NATURALINNERJOIN, UNION, EXCEPT, TREATAS, INTERSECT, ADDCOLUMNS, GENERATE, VALUES, RELATED, SELECTCOLUMNS, ROW, CALCULATETABLE, GENERATESERIES, DATATABLE, CROSSJOIN, FILTER, CONTAINS, CALCULATE, SELECTEDVALUE, RELATEDTABLE, DISTINCT, CURRENCY, CALENDAR, GENERATEALL, CONVERT, ALL, COALESCE, NOT.
- Features: relationships, data lineage, Excel and MDX clients, fact tables, error handling, virtual relationships, calculated tables, DAX queries, blank handling, variables, data types, query plans, storage engine, Power Query, row context, expanded tables, limited relationships, auto-exist, iterators, calculated columns, currency conversion, compression, blank row of an invalid relationship.

## Time intelligence and date tables

### `t04-time-intelligence-and-dates-1.md` (69 notes)

- Covers: Time intelligence functions; Week-based and fiscal calendars; Mark as date table; Incomplete periods and future dates.
- DAX functions: CALCULATE, DATEADD, LASTDATE, VALUES, PARALLELPERIOD, FILTER, DATESYTD, SAMEPERIODLASTYEAR, CALCULATETABLE, ALLEXCEPT, DATESINPERIOD, ALL, FIRSTDATE, PREVIOUSDAY, KEEPFILTERS, FILTERS, AVERAGEX, SELECTEDMEASURE, YEAR, MONTH, QUARTER, CONTAINS, REMOVEFILTERS, MAX, MIN, NEXTDAY, IF, COUNTROWS, DATESBETWEEN, WEEKDAY, DAY, PREVIOUSMONTH, NEXT, PREVIOUSYEAR, PREVIOUSQUARTER, TOTALYTD, EDATE, TODAY, TREATAS.
- Features: date table, time intelligence, calendar-based time intelligence, week-based calendars, relationships, calculated columns, Power Query, blank handling, row context, DAX queries, slicers, filter context, iterators, moving averages, calculation groups, context transition, fact tables, totals and subtotals, data types, fiscal calendars, variables, Excel and MDX clients.

### `t04-time-intelligence-and-dates-2.md` (80 notes)

- Covers: Period-over-period comparisons; Building a Date table; Date columns, sorting and formats; Blank and placeholder dates; Calendar-based time intelligence.
- DAX functions: CALCULATE, DATEADD, DATESINPERIOD, REMOVEFILTERS, CALENDARAUTO, KEEPFILTERS, ALLEXCEPT, SAMEPERIODLASTYEAR, FORMAT, NOT, ISBLANK, USERELATIONSHIP, ALLSELECTED, SELECTEDMEASURE, RANKX, IFERROR, ERROR, SELECTCOLUMNS, CALENDAR, MIN, MAX, BLANK, DATESBETWEEN, FILTER, VALUES, DATESYTD, NEXTMONTH.
- Features: date table, calendar-based time intelligence, time intelligence, slicers, charts, blank handling, relationships, hierarchies, format strings, fact tables, blank row of an invalid relationship, fiscal calendars, totals and subtotals, data categories and geography, calculated columns, inactive relationships, sort by column, calculation groups, visual-level filters, calculated tables, naming, TMDL and project files, auto date/time.

## Relationships and filter propagation

### `t05-relationships-1.md` (67 notes)

- Covers: Many-to-many relationships; Virtual relationships in DAX; Bidirectional filters and propagation; Blank row and limited relationships; Inactive relationships and date roles.
- DAX functions: CALCULATE, USERELATIONSHIP, TREATAS, FILTER, INTERSECT, ALL, VALUES, CONTAINS, SUMMARIZE, CROSSFILTER, AND, IF, NOT, ISEMPTY, ISFILTERED, CALCULATETABLE, COUNTROWS, ISCROSSFILTERED, CROSSJOIN, REMOVEFILTERS, INT, OR, RANKX, DISTINCT, ALLNOBLANKROW, LOOKUPVALUE, RELATED.
- Features: relationships, many-to-many, dimension tables, virtual relationships, bidirectional filters, cardinality, blank handling, inactive relationships, bridge tables, blank row of an invalid relationship, limited relationships, slicers, visual-level filters, date table, totals and subtotals, Excel and MDX clients, Power Query, storage engine, query plans, calculated tables, formula engine, composite models, calculated columns, charts.

## Data model design

### `t06-data-model-design-1.md` (61 notes)

- Covers: Dates, time and sort keys; Calculated columns versus measures; Source views, names, data types; Star schema and fact tables.
- DAX functions: SUMX, RELATED, VAR, VALUES, REMOVEFILTERS, LOOKUPVALUE, SUM, IGNORE.
- Features: calculated columns, dimension tables, Power Query, fact tables, import mode, star schema, relationships, data types, naming, date table, memory, slicers, refresh and processing, compression, auto-exist, hierarchies, totals and subtotals, SQL views, blank handling, charts, iterators, DAX queries, data categories and geography, dictionaries.

### `t06-data-model-design-2.md` (55 notes)

- Covers: Business-rule grain and testing; Duplicate names, Group By Columns; Circular dependency errors; Sankey chart funnels; User-context calculated columns.
- DAX functions: CALCULATE, ALLNOBLANKROW, DISTINCT, VALUES, ALLEXCEPT, SELECTEDVALUE, ALL, SUMMARIZE, AVERAGE, HASONEVALUE, USERCULTURE, LOOKUPVALUE, MAX, MIN, REMOVEFILTERS, FILTER, COMBINEVALUES, SUMMARIZECOLUMNS, TREATAS, ISFILTERED, USERELATIONSHIP, CALCULATETABLE, USERPRINCIPALNAME, USERNAME, USEROBJECTID, CUSTOMDATA, FALSE.
- Features: calculated columns, relationships, error handling, context transition, blank handling, calculated tables, Excel and MDX clients, slicers, iterators, totals and subtotals, blank row of an invalid relationship, DAX queries, refresh and processing, row-level security, testing and debugging, DirectQuery, naming, composite models, memory, cardinality.

## DAX performance and optimization

### `t07-dax-performance-1.md` (54 notes)

- Covers: Filters, counts and emptiness tests; Measuring and testing performance; Formula and storage engine.
- DAX functions: CALCULATE, DISTINCTCOUNT, SUMX, ISEMPTY, DISTINCT, COUNTROWS, IF, FILTER, CALCULATETABLE, KEEPFILTERS, LASTNONBLANK, AND, ISBLANK, ALL, BLANK, NOT, FIRSTNONBLANK, EXCEPT, INTERSECT, DIVIDE, MIN, AVERAGE.
- Features: distinct counts, storage engine, DAX queries, fact tables, formula engine, testing and debugging, query plans, iterators, refresh and processing, filter context, materialization, Performance Analyzer, totals and subtotals, memory, relationships, cardinality, date table, CallbackDataID.

### `t07-dax-performance-2.md` (49 notes)

- Covers: Model design, relationships and memory; Server, processing and hardware; Report visuals and Excel clients.
- DAX functions: IF, CALCULATE.
- Features: memory, relationships, refresh and processing, Excel and MDX clients, cardinality, storage engine, partitions, compression, many-to-many, DAX queries, fact tables, import mode, VertiPaq, star schema, dimension tables, query plans, testing and debugging.

### `t07-dax-performance-3.md` (68 notes)

- Covers: Iterators and materialization; Conditional logic and variables; Text search and its index.
- DAX functions: IF, SEARCH, SWITCH, CONTAINSSTRING, CALCULATE, LASTNONBLANKVALUE, LASTNONBLANK, FILTER, SELECTEDVALUE, SUMX, RANKX, COUNTROWS, DATESBETWEEN, LOOKUPVALUE, MAX, FIRSTNONBLANK, FIRSTNONBLANKVALUE, CALCULATETABLE, SUMMARIZECOLUMNS, RELATED, NATURALLEFTOUTERJOIN, TREATAS, ROUND, ADDCOLUMNS, SUMMARIZE, OFFSET, NOT, ISBLANK, IF.EAGER, FIND, CONTAINSSTRINGEXACT.
- Features: iterators, storage engine, DAX queries, variables, formula engine, fact tables, blank handling, slicers, CallbackDataID, materialization, cardinality, context transition, memory, filter context, testing and debugging, query plans, refresh and processing, dimension tables, row context, calculated columns, ranking, totals and subtotals, Power Query.

## Storage engine, model size and memory

### `t08-storage-engine-and-model-size-1.md` (29 notes)

- Covers: Reducing column cardinality; Measuring model size; Analysis Services processing; Calculated column and table storage.
- DAX functions: SUMX, DISTINCTCOUNT, COUNTROWS, SUMMARIZE, MOD, INT, LOOKUPVALUE, MONTH, RELATED, ALL, CROSSJOIN.
- Features: memory, dictionaries, refresh and processing, calculated columns, compression, calculated tables, fact tables, data types, partitions, AI assistance.

## Storage modes

### `t09-storage-modes-1.md` (41 notes)

- Covers: DirectQuery DAX and limits; DirectQuery model and source design.
- DAX functions: NOT, CALCULATE, BLANK, COMBINEVALUES, MEDIANX, ALL, SUMMARIZECOLUMNS, ADDCOLUMNS, INT, ISEMPTY, LASTNONBLANK, MID, LEFT, SEARCH, REPLACE, LEN, CEILING, TRIM, SUBSTITUTE, POWER, SECOND, LOG, REMOVEFILTERS, SAMEPERIODLASTYEAR, DATESBETWEEN, DATEADD, DATESYTD.
- Features: DirectQuery, relationships, memory, calculated columns, time intelligence, row-level security, import mode, formula engine, DAX queries, VertiPaq, partitions, error handling, granularity, query plans, totals and subtotals, detail rows, fact tables, blank handling.

### `t09-storage-modes-2.md` (45 notes)

- Covers: Choosing a storage mode; Composite models; Push datasets.
- DAX functions: ALLSELECTED, DISTINCTCOUNT, LOOKUPVALUE, USERELATIONSHIP.
- Features: push datasets, composite models, DirectQuery, memory, import mode, calculation groups, refresh and processing, DAX queries, relationships, fact tables, date table.

## Security

### `t10-security-1.md` (43 notes)

- Covers: Dynamic security, relationships and testing; Role filter performance; Totals under row-level security; Object-level security and active roles.
- DAX functions: ALL, USERELATIONSHIP, TREATAS, VALUES, CALCULATETABLE, PATHCONTAINS, LEFT, CROSSFILTER, REMOVEFILTERS, CALCULATE, FALSE, FILTER, SELECTEDVALUE, CONCATENATEX, CONTAINSSTRING, IF, ERROR.
- Features: row-level security, dimension tables, relationships, fact tables, totals and subtotals, calculated tables, object-level security, storage engine, error handling, hierarchies, dynamic security, inactive relationships, virtual relationships, blank handling, DAX queries.

## Calculation groups and field parameters

### `t11-calculation-groups-and-field-parameters-1.md` (43 notes)

- Covers: Calculation group design patterns; Calculation item application; Format string expressions.
- DAX functions: CALCULATE, ISSELECTEDMEASURE, SELECTEDMEASURE, IF, SELECTEDMEASURENAME, SELECTEDMEASUREFORMATSTRING, SWITCH, FALSE, TREATAS, USERELATIONSHIP, SELECTEDVALUE, SAMEPERIODLASTYEAR, DATESYTD.
- Features: calculation groups, format strings, DAX queries, relationships, dynamic format strings, totals and subtotals, bidirectional filters, bridge tables, error handling, slicers, time intelligence, calculated tables, parameter tables, filter context, fact tables.

### `t11-calculation-groups-and-field-parameters-2.md` (42 notes)

- Covers: Calculation group precedence; Per-user defaults and slicers; Field parameters; Selection expressions.
- DAX functions: CALCULATE, SELECTEDMEASURE, ISCROSSFILTERED, USERPRINCIPALNAME, SELECTEDVALUE, VALUES, MAX, SELECTEDMEASURENAME, ALLSELECTED, SWITCH, ALL, CONCATENATEX, NAMEOF, ERROR.
- Features: calculation groups, slicers, field parameters, relationships, parameter tables, format strings, many-to-many, currency conversion, testing and debugging, row-level security, dynamic format strings, dynamic security, cardinality, variables, formula engine, hierarchies, Excel and MDX clients, DAX formatting, conditional formatting, error handling.

## Window functions and visual calculations

### `t12-window-functions-and-visual-calculations-1.md` (77 notes)

- Covers: Measure or visual calculation; Window functions and apply semantics; Ranking with RANK and RANKX; Visual context and virtual table; Running totals and performance.
- DAX functions: RANK, RANKX, EXPAND, COLLAPSE, OFFSET, CALCULATE, ORDERBY, INDEX, WINDOW, ALL, COLLAPSEALL, VALUES, ALLSELECTED, ISINSCOPE, PREVIOUS, PARTITIONBY, MATCHBY, IF, ISATLEVEL, EXPANDALL, FORMAT, DISTINCT, SWITCH, AVERAGEX, ALLEXCEPT, LAST, ADDCOLUMNS, HASONEVALUE, MINX, FILTER, NEXT, CALCULATETABLE, RUNNINGSUM, SUMMARIZECOLUMNS.
- Features: visual calculations, ranking, totals and subtotals, window functions, hierarchies, DAX queries, matrix visual, filter context, running totals, iterators, DAX formatting, partitions, blank handling, distinct counts, granularity, slicers, conditional formatting, moving averages, row context, variables, fact tables, storage engine, relationships, comments.

## User-defined functions in DAX

### `t13-user-defined-functions-1.md` (47 notes)

- Covers: Naming and model-independent functions; Functions, measures and calculation groups; Parameters, types and passing modes; Calendar filters and result checks.
- DAX functions: CALCULATE, REMOVEFILTERS, TABLEOF, SUMX, SUM, ISFILTERED, ISCROSSFILTERED, ERROR, NAMEOF, BLANK, ISBLANK, DATESINPERIOD, RANGE.
- Features: user-defined functions, calendar-based time intelligence, calculation groups, DAX queries, iterators, testing and debugging, row context, naming, context transition, error handling, filter context, data types, blank handling, time intelligence, visual calculations.

## Business calculation patterns

### `t14-business-calculation-patterns-1.md` (53 notes)

- Covers: Totals and hierarchy levels; Budget, currency and financial calculations.
- DAX functions: CALCULATE, VALUES, ALLEXCEPT, FILTER, CONTAINS, ALL, REMOVEFILTERS, ISFILTERED, SUMX, KEEPFILTERS, SUMMARIZE, DATESYTD, PRODUCTX.
- Features: totals and subtotals, iterators, budget and forecast, fact tables, relationships, hierarchies, blank handling, currency conversion, filter context, date table, slicers, context transition, virtual relationships, charts, DAX queries, snapshot tables, error handling, granularity, calculation groups.

### `t14-business-calculation-patterns-2.md` (49 notes)

- Covers: Customer, product and campaign analysis.
- DAX functions: CALCULATE, REMOVEFILTERS, VALUES, CROSSFILTER, GENERATE, SUMMARIZE, ALLSELECTED, SWITCH, WINDOW, ISINSCOPE, RELATED, DATEADD, DATESINPERIOD, GENERATEALL, SELECTCOLUMNS, MIN, ADDCOLUMNS, UNION, EXCEPT, INTERSECT, DATESBETWEEN, ERROR, COLLAPSE, PARTITIONBY, ISBLANK, KEEPFILTERS, DIVIDE.
- Features: fact tables, charts, blank handling, dimension tables, bridge tables, calculated tables, totals and subtotals, relationships, calculated columns, Power Query, ABC and segmentation, DAX queries, slicers, tooltips, blank row of an invalid relationship, running totals, refresh and processing, error handling, Excel and MDX clients, matrix visual, variables, visual calculations.

### `t14-business-calculation-patterns-3.md` (84 notes)

- Covers: Semi-additive and running totals; Ranking and top N.
- DAX functions: RANKX, CALCULATE, ALLSELECTED, LASTDATE, LASTNONBLANK, ALL, TOPN, FIRSTNONBLANK, VALUES, REMOVEFILTERS, GENERATE, MAX, FILTER, HASONEVALUE, KEEPFILTERS, STARTOFMONTH, OPENINGBALANCEMONTH, STARTOFYEAR, ENDOFQUARTER, ENDOFYEAR, CLOSINGBALANCEMONTH, STARTOFQUARTER, ENDOFMONTH, ISCROSSFILTERED, ISINSCOPE, FIRSTDATE, IF, OPENINGBALANCEQUARTER, CLOSINGBALANCEYEAR, OPENINGBALANCEYEAR, CLOSINGBALANCEQUARTER, YEAR, PARALLELPERIOD, QUARTER, TREATAS, SUMX, DATESYTD, TRUE, CONCATENATEX, CALCULATETABLE.
- Features: ranking, snapshot tables, totals and subtotals, visual-level filters, semi-additive measures, blank handling, matrix visual, DAX queries, dimension tables, iterators, variables, filter context, context transition, sort by column, calculated tables, calculated columns, memory, running totals, date table, cardinality, Excel and MDX clients, slicers, relationships, charts.

### `t14-business-calculation-patterns-4.md` (57 notes)

- Covers: Events, durations and sequences; Building and testing calculations; Averages, working days and trends.
- DAX functions: LINESTX, AVERAGEX, LINEST, SELECTCOLUMNS, DIVIDE, CURRENTGROUP, COUNTROWS, GROUPBY, SUMX, TRUE, FALSE, ALLEXCEPT, CALCULATETABLE, ALL, REMOVEFILTERS, CALCULATE, SUM, HASONEVALUE, TOPN, NETWORKDAYS, RANKX, ADDCOLUMNS, KEEPFILTERS, COALESCE.
- Features: date table, calculated columns, variables, DAX queries, blank handling, moving averages, iterators, totals and subtotals, Power Query, dimension tables, calendar-based time intelligence, charts, testing and debugging, filter context, relationships, context transition, calculated tables, fact tables, running totals, slicers, ranking.

## Report-facing DAX and report design

### `t15-report-facing-dax-1.md` (78 notes)

- Covers: Slicers and measure filters; Report design and requirements; Measures written for visuals.
- DAX functions: OR, CALCULATE, CONCATENATEX, AND, VALUES, ALLSELECTED, FILTER, SELECTEDVALUE, TOPN, UNICHAR, RAND, ISINSCOPE, CALCULATETABLE, COUNTROWS, DISTINCT, SELECTCOLUMNS, UNION, REMOVEFILTERS, SELECTEDMEASURE, KEEPFILTERS, SWITCH, SUMMARIZECOLUMNS, SAMEPERIODLASTYEAR, DISTINCTCOUNT, BLANK, CROSSFILTER, SUMMARIZE, RELATED.
- Features: slicers, charts, blank handling, granularity, matrix visual, DAX queries, visual-level filters, DAX formatting, dimension tables, calculation groups, report themes, totals and subtotals, relationships, hierarchies, drillthrough, budget and forecast, calculated tables, many-to-many, cardinality, user-defined functions, parameter tables, refresh and processing, calculated columns, fact tables.

### `t15-report-facing-dax-2.md` (79 notes)

- Covers: Model support for reports; Tooltips, drillthrough and detail rows; Choosing and building charts.
- DAX functions: DETAILROWS, CALCULATETABLE, ADDCOLUMNS, NATURALINNERJOIN, RELATED, UNION, ALLEXCEPT, KEEPFILTERS, DATESBETWEEN, ALLSELECTED, CALCULATE, REMOVEFILTERS, MAXX, ROUNDUP, MAX, TREATAS, RAND.
- Features: charts, detail rows, drillthrough, calculation groups, Excel and MDX clients, tooltips, filter context, DAX queries, report themes, DAX formatting, format strings, error handling, documentation and descriptions, calculated tables, matrix visual, blank handling, slicers, hierarchies, field parameters, ABC and segmentation, dimension tables, Power Query, parameter tables, granularity.

### `t15-report-facing-dax-3.md` (67 notes)

- Covers: Conditional formatting and KPIs; Format strings in reports.
- DAX functions: ALLSELECTED, ISINSCOPE, SELECTEDMEASURE, REMOVEFILTERS, VALUES, RANKX, ISATLEVEL, FORMAT, CALCULATETABLE, SELECTEDVALUE, MOD, MINX, MAXX, TREATAS, TRUE, SWITCH, COLLAPSE, COLLAPSEALL, CALCULATE, UNICHAR, UNICODE, TRUNC.
- Features: DAX formatting, format strings, dynamic format strings, Excel and MDX clients, KPIs, conditional formatting, report themes, visual calculations, hierarchies, DAX queries, matrix visual, totals and subtotals, calculation groups, charts, ranking, documentation and descriptions, blank handling, slicers, testing and debugging.

### `t15-report-facing-dax-4.md` (28 notes)

- Covers: Custom and SVG visuals; Themes and report templates.
- DAX functions: none named.
- Features: report themes, SVG and custom visuals, AI assistance, DAX formatting, charts, matrix visual, documentation and descriptions, error handling, conditional formatting, TMDL and project files.

## Tooling, workflow and AI assistance

### `t16-tooling-and-workflow-1.md` (55 notes)

- Covers: Scripting with TOM and APIs; Translations and renaming objects; Model edits with external tools; Query tracing and debugging; Choosing development tools.
- DAX functions: TOCSV, TOJSON, ALLSELECTED, EVALUATEANDLOG, CONCATENATEX, CALCULATETABLE, TOPN, FORMAT, SUMMARIZECOLUMNS.
- Features: testing and debugging, DAX queries, variables, translations, Excel and MDX clients, KPIs, slicers, naming, refresh and processing, Performance Analyzer, filter context, shadow filter context, TMDL and project files, relationships, AI assistance, DAX formatting.

### `t16-tooling-and-workflow-2.md` (56 notes)

- Covers: Reusable libraries and templates; AI assistants and agents; Testing measures.
- DAX functions: CALCULATE, RANK, UNION, EVALUATE, TREATAS, COALESCE.
- Features: AI assistance, testing and debugging, TMDL and project files, DAX queries, user-defined functions, error handling, report themes, documentation and descriptions, filter context, totals and subtotals, dimension tables, DAX formatting, ranking, blank handling.
