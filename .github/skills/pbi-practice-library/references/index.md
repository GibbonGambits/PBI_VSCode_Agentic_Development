# Practice library: index

Read this file first, then open only the file that fits the task, two at most. Never read the whole library for one task.

Each entry names one file in this folder, what it covers, and the DAX functions and Power BI features its notes mention (most frequent first). A function is listed when a note names it; a function or feature can appear in several files, so pick the file whose topic fits the question. How to use a note is set out in the skill file one folder up.

| Topic | Files | Notes |
|---|---|---:|
| DAX evaluation context | `t01-evaluation-context-1.md` to `t01-evaluation-context-2.md` | 156 |
| DAX authoring style | `t02-dax-authoring-style-1.md` to `t02-dax-authoring-style-2.md` | 112 |
| DAX table functions and queries | `t03-table-functions-and-queries-1.md` to `t03-table-functions-and-queries-2.md` | 154 |
| Time intelligence and date tables | `t04-time-intelligence-and-dates-1.md` to `t04-time-intelligence-and-dates-3.md` | 166 |
| Relationships and filter propagation | `t05-relationships-1.md` | 67 |
| Data model design | `t06-data-model-design-1.md` to `t06-data-model-design-2.md` | 127 |
| DAX performance and optimization | `t07-dax-performance-1.md` to `t07-dax-performance-3.md` | 180 |
| Storage engine, model size and memory | `t08-storage-engine-and-model-size-1.md` | 33 |
| Storage modes | `t09-storage-modes-1.md` to `t09-storage-modes-2.md` | 95 |
| Security | `t10-security-1.md` | 45 |
| Calculation groups and field parameters | `t11-calculation-groups-and-field-parameters-1.md` to `t11-calculation-groups-and-field-parameters-2.md` | 87 |
| Window functions and visual calculations | `t12-window-functions-and-visual-calculations-1.md` | 78 |
| User-defined functions in DAX | `t13-user-defined-functions-1.md` | 48 |
| Business calculation patterns | `t14-business-calculation-patterns-1.md` to `t14-business-calculation-patterns-5.md` | 244 |
| Report-facing DAX and report design | `t15-report-facing-dax-1.md` to `t15-report-facing-dax-5.md` | 290 |
| Tooling, workflow and AI assistance | `t16-tooling-and-workflow-1.md` to `t16-tooling-and-workflow-3.md` | 151 |

## DAX evaluation context

### `t01-evaluation-context-1.md` (82 notes)

- Covers: KEEPFILTERS and arbitrary filters; CALCULATE filter arguments; Visual queries and auto-exist; Reading the selected value; Row context and iterators.
- DAX functions: CALCULATE, KEEPFILTERS, FILTER, VALUES, ALL, SELECTEDVALUE, CROSSJOIN, CALCULATETABLE, SUMMARIZE, SUMX, HASONEVALUE, ISINSCOPE, RELATED, TRUE, SUM, SUMMARIZECOLUMNS, OR, AVERAGEX, AND, ISFILTERED, DISTINCT, REMOVEFILTERS, LASTDATE, IF, CROSSFILTER, ERROR, FALSE, RELATEDTABLE, AVERAGE, MAX, MIN, SELECTCOLUMNS, MAXX, MINX.
- Features: iterators, DAX queries, filter context, row context, slicers, error handling, totals and subtotals, relationships, context transition, cardinality, auto-exist, blank handling, Excel and MDX clients, variables, calculated columns, storage engine, sort by column, blank row of an invalid relationship, matrix visual, expanded tables, hierarchies, dimension tables, parameter tables.

### `t01-evaluation-context-2.md` (74 notes)

- Covers: Relationships, expanded tables and lineage; Context transition; Removing filters with ALL; ALLSELECTED and shadow filters; Totals and additivity.
- DAX functions: CALCULATE, ALL, ALLSELECTED, RELATED, CALCULATETABLE, VALUES, ALLEXCEPT, REMOVEFILTERS, FILTER, RELATEDTABLE, ALLCROSSFILTERED, TREATAS, MAX, SUMMARIZE, USERELATIONSHIP, ADDCOLUMNS, SELECTEDVALUE, LASTDATE, COUNTROWS, MIN, EARLIER, DISTINCT, MAXX, MINX, SUMMARIZECOLUMNS.
- Features: iterators, filter context, relationships, row context, context transition, calculated columns, totals and subtotals, fact tables, shadow filter context, dimension tables, DAX queries, expanded tables, variables, error handling, limited relationships, Excel and MDX clients, inactive relationships, data lineage, budget and forecast, virtual relationships, matrix visual, bidirectional filters, DirectQuery.

## DAX authoring style

### `t02-dax-authoring-style-1.md` (65 notes)

- Covers: Formatting, naming and references; Variables and their evaluation; BLANK handling and conditions.
- DAX functions: IF, BLANK, SWITCH, DIVIDE, ADDCOLUMNS, CALCULATE, ISBLANK, COALESCE, VAR, TOPN, SUMX, VALUES, DISTINCT, FILTER, FALSE, COUNTROWS, ALL, TREATAS, CONCATENATEX, RELATEDTABLE, ERROR, AVERAGEX, MINX, MAXX.
- Features: variables, blank handling, iterators, error handling, DAX queries, filter context, relationships, blank row of an invalid relationship, data types, row context, calculated columns, calculated tables, naming, data lineage, Excel and MDX clients, totals and subtotals.

### `t02-dax-authoring-style-2.md` (47 notes)

- Covers: IN operator and constructors; Data types and comparisons.
- DAX functions: CALCULATE, OR, NOT, FILTER, ALL, CONTAINSROW, CONTAINS, TREATAS, CALCULATETABLE, SUMX, VALUES, EXCEPT, AND, SUMMARIZE, ISEMPTY, INTERSECT, UNION, CONVERT, INT.
- Features: data types, error handling, testing and debugging, iterators, fact tables, currency conversion, virtual relationships, DAX formatting, conditional formatting, totals and subtotals.

## DAX table functions and queries

### `t03-table-functions-and-queries-1.md` (79 notes)

- Covers: Grouping and adding columns; Writing DAX queries; Filter and text conditions.
- DAX functions: SUMMARIZE, ADDCOLUMNS, CALCULATE, GROUPBY, CALCULATETABLE, FILTER, CURRENTGROUP, SEARCH, SELECTCOLUMNS, DEFINE, EVALUATE, CONTAINSSTRING, DETAILROWS, CONTAINS, MAXX, VALUES, GENERATE, ROW, DISTINCT, LEFT, ISEMPTY, ALL, FIND, AND, SUM, DATATABLE, OR, TREATAS, KEEPFILTERS, REMOVEFILTERS, MAX, BLANK, CROSSJOIN, ALLEXCEPT, SUBSTITUTE, CONTAINSSTRINGEXACT, RIGHT, RELATEDTABLE. Also named, though missing from the function index of the model skill: TOPNSKIP.
- Features: DAX queries, iterators, variables, Excel and MDX clients, relationships, filter context, blank handling, totals and subtotals, row context, context transition, fact tables, materialization, slicers, expanded tables, dimension tables, formula engine, query plans, testing and debugging, blank row of an invalid relationship, external tools, detail rows.

### `t03-table-functions-and-queries-2.md` (75 notes)

- Covers: Calculated and static tables; SUMMARIZECOLUMNS behaviour; Joins and lookups; Set functions.
- DAX functions: SUMMARIZECOLUMNS, LOOKUPVALUE, NATURALLEFTOUTERJOIN, SUMMARIZE, NATURALINNERJOIN, UNION, TREATAS, EXCEPT, INTERSECT, ADDCOLUMNS, GENERATE, VALUES, RELATED, SELECTCOLUMNS, ROW, GENERATESERIES, DATATABLE, CROSSJOIN, CALCULATETABLE, FILTER, CONTAINS, CALCULATE, SELECTEDVALUE, RELATEDTABLE, DISTINCT, CURRENCY, CALENDAR, GENERATEALL, CONVERT, ALL, COALESCE, NOT.
- Features: relationships, data lineage, Excel and MDX clients, fact tables, error handling, virtual relationships, calculated tables, DAX queries, blank handling, variables, data types, query plans, storage engine, row context, expanded tables, limited relationships, auto-exist, iterators, calculated columns, currency conversion, compression, Power Query, blank row of an invalid relationship.

## Time intelligence and date tables

### `t04-time-intelligence-and-dates-1.md` (60 notes)

- Covers: Time intelligence functions; Week-based and fiscal calendars; Mark as date table.
- DAX functions: CALCULATE, DATEADD, LASTDATE, VALUES, FILTER, PARALLELPERIOD, DATESYTD, CALCULATETABLE, ALLEXCEPT, DATESINPERIOD, SAMEPERIODLASTYEAR, ALL, FIRSTDATE, PREVIOUSDAY, KEEPFILTERS, FILTERS, AVERAGEX, YEAR, TOTALYTD, CONTAINS, MAX, MIN, NEXTDAY, COUNTROWS, DATESBETWEEN, WEEKDAY, SELECTEDMEASURE, MONTH, QUARTER, DAY, PREVIOUSYEAR, PREVIOUSMONTH, PREVIOUSQUARTER. Also named, though missing from the function index of the model skill: NEXT.
- Features: date table, calendar-based time intelligence, time intelligence, week-based calendars, relationships, fiscal calendars, row context, fact tables, iterators, moving averages, slicers, totals and subtotals, context transition, DAX queries, data types, filter context, calculated columns, blank handling, external tools, Power Query.

### `t04-time-intelligence-and-dates-2.md` (62 notes)

- Covers: Incomplete periods and future dates; Period-over-period comparisons; Building a Date table.
- DAX functions: CALCULATE, REMOVEFILTERS, SELECTEDMEASURE, KEEPFILTERS, ALLEXCEPT, CALENDARAUTO, IF, DATESYTD, SAMEPERIODLASTYEAR, EDATE, TODAY, TREATAS, MONTH, QUARTER, PARALLELPERIOD, USERELATIONSHIP, ALLSELECTED, DATESINPERIOD, SELECTEDVALUE, RANKX, IFERROR, ERROR, SELECTCOLUMNS, DATATABLE, CALENDAR, MAX, MIN.
- Features: date table, slicers, calculated columns, external tools, time intelligence, calculation groups, calendar-based time intelligence, fact tables, blank handling, charts, relationships, filter context, variables, DAX queries, visual-level filters, context transition, calculated tables, hierarchies, fiscal calendars, Excel and MDX clients, refresh and processing, inactive relationships, error handling, auto date/time.

### `t04-time-intelligence-and-dates-3.md` (44 notes)

- Covers: Date columns, sorting and formats; Blank and placeholder dates; Calendar-based time intelligence.
- DAX functions: DATEADD, DATESINPERIOD, SAMEPERIODLASTYEAR, FORMAT, ISBLANK, NOT, CALENDARAUTO, BLANK, DATESBETWEEN, VALUES, CALCULATE, FILTER, NEXTMONTH, DATESYTD.
- Features: date table, calendar-based time intelligence, time intelligence, blank handling, format strings, charts, hierarchies, blank row of an invalid relationship, slicers, relationships, totals and subtotals, data categories and geography, fiscal calendars, fact tables, sort by column, TMDL and project files.

## Relationships and filter propagation

### `t05-relationships-1.md` (67 notes)

- Covers: Many-to-many relationships; Virtual relationships in DAX; Bidirectional filters and propagation; Blank row and limited relationships; Inactive relationships and date roles.
- DAX functions: CALCULATE, USERELATIONSHIP, TREATAS, INTERSECT, FILTER, ALL, VALUES, CONTAINS, SUMMARIZE, CROSSFILTER, AND, IF, ISEMPTY, NOT, ISFILTERED, CALCULATETABLE, COUNTROWS, ISCROSSFILTERED, CROSSJOIN, INT, OR, RANKX, DISTINCT, ALLNOBLANKROW, RELATED, LOOKUPVALUE.
- Features: relationships, many-to-many, dimension tables, virtual relationships, cardinality, bidirectional filters, blank handling, inactive relationships, bridge tables, blank row of an invalid relationship, limited relationships, slicers, visual-level filters, date table, totals and subtotals, Excel and MDX clients, storage engine, query plans, calculated tables, formula engine, composite models, calculated columns, charts.

## Data model design

### `t06-data-model-design-1.md` (64 notes)

- Covers: Dates, time and sort keys; Calculated columns versus measures; Source views, names, data types; Star schema and fact tables.
- DAX functions: SUMX, RELATED, VAR, VALUES, REMOVEFILTERS, RANKX, LOOKUPVALUE, SUM, IGNORE.
- Features: calculated columns, dimension tables, fact tables, import mode, Power Query, star schema, relationships, date table, data types, memory, naming, slicers, refresh and processing, compression, auto-exist, hierarchies, totals and subtotals, SQL views, blank handling, sort by column, charts, model size, iterators, DAX queries.

### `t06-data-model-design-2.md` (63 notes)

- Covers: Business-rule grain and testing; Duplicate names, Group By Columns; Circular dependency errors; Sankey chart funnels; User-context calculated columns.
- DAX functions: CALCULATE, ALLNOBLANKROW, VALUES, DISTINCT, ALLEXCEPT, ALL, SELECTEDVALUE, SUMMARIZE, AVERAGE, HASONEVALUE, TREATAS, USERCULTURE, LOOKUPVALUE, MAX, MIN, REMOVEFILTERS, FILTER, IF, COMBINEVALUES, SUMMARIZECOLUMNS, ISFILTERED, USERELATIONSHIP, CALCULATETABLE, CUSTOMDATA, USEROBJECTID, USERPRINCIPALNAME, USERNAME, FALSE.
- Features: calculated columns, relationships, error handling, charts, SVG and custom visuals, context transition, blank handling, slicers, iterators, calculated tables, Excel and MDX clients, totals and subtotals, blank row of an invalid relationship, cardinality, testing and debugging, DAX queries, external tools, refresh and processing, row-level security, storage engine, CallbackDataID, virtual relationships, composite models, memory.

## DAX performance and optimization

### `t07-dax-performance-1.md` (62 notes)

- Covers: Filters, counts and emptiness tests; Measuring and testing performance; Formula and storage engine.
- DAX functions: CALCULATE, DISTINCTCOUNT, SUMX, ISEMPTY, DISTINCT, IF, COUNTROWS, FILTER, CALCULATETABLE, KEEPFILTERS, LASTNONBLANK, AND, ISBLANK, ALL, BLANK, NOT, FIRSTNONBLANK, EXCEPT, INTERSECT, DIVIDE, AVERAGE, MIN.
- Features: distinct counts, storage engine, DAX queries, external tools, fact tables, Performance Analyzer, formula engine, query plans, testing and debugging, iterators, refresh and processing, filter context, materialization, totals and subtotals, DirectQuery, memory, relationships, AI assistance, cardinality, date table, CallbackDataID, import mode.

### `t07-dax-performance-2.md` (50 notes)

- Covers: Model design, relationships and memory; Server, processing and hardware; Report visuals and Excel clients.
- DAX functions: IF, CALCULATE.
- Features: memory, relationships, refresh and processing, Excel and MDX clients, cardinality, storage engine, partitions, compression, VertiPaq, many-to-many, DAX queries, fact tables, import mode, external tools, star schema, dimension tables, query plans, testing and debugging.

### `t07-dax-performance-3.md` (68 notes)

- Covers: Iterators and materialization; Conditional logic and variables; Text search and its index.
- DAX functions: IF, SEARCH, SWITCH, CONTAINSSTRING, CALCULATE, LASTNONBLANKVALUE, LASTNONBLANK, FILTER, SELECTEDVALUE, SUMX, COUNTROWS, RANKX, DATESBETWEEN, LOOKUPVALUE, MAX, FIRSTNONBLANK, FIRSTNONBLANKVALUE, CALCULATETABLE, SUMMARIZECOLUMNS, RELATED, NATURALLEFTOUTERJOIN, TREATAS, ROUND, ADDCOLUMNS, SUMMARIZE, OFFSET, ISBLANK, NOT, IF.EAGER, FIND, CONTAINSSTRINGEXACT.
- Features: iterators, storage engine, DAX queries, variables, formula engine, fact tables, blank handling, slicers, CallbackDataID, materialization, cardinality, context transition, memory, filter context, testing and debugging, query plans, refresh and processing, dimension tables, row context, calculated columns, ranking, totals and subtotals.

## Storage engine, model size and memory

### `t08-storage-engine-and-model-size-1.md` (33 notes)

- Covers: Reducing column cardinality; Measuring model size; Analysis Services processing; Calculated column and table storage.
- DAX functions: NOW, SUMX, COUNTROWS, DISTINCTCOUNT, SUMMARIZE, INT, MOD, MAX, RELATED, MONTH, LOOKUPVALUE, CROSSJOIN, ALL.
- Features: memory, refresh and processing, dictionaries, calculated columns, VertiPaq, external tools, compression, calculated tables, fact tables, data types, partitions.

## Storage modes

### `t09-storage-modes-1.md` (47 notes)

- Covers: DirectQuery DAX and limits; DirectQuery model and source design.
- DAX functions: SUMMARIZECOLUMNS, ADDCOLUMNS, NOT, CALCULATE, BLANK, COMBINEVALUES, MEDIANX, ALL, INT, ISEMPTY, LASTNONBLANK, CEILING, TRIM, MID, LEFT, SUBSTITUTE, SEARCH, LOG, LEN, POWER, REPLACE, SECOND, SUMMARIZE, REMOVEFILTERS, SAMEPERIODLASTYEAR, DATESYTD, DATEADD, DATESBETWEEN.
- Features: DirectQuery, memory, relationships, formula engine, calculated columns, import mode, external tools, DAX queries, time intelligence, partitions, row-level security, storage engine, VertiPaq, error handling, granularity, query plans, totals and subtotals, detail rows, refresh and processing, fact tables, blank handling, Excel and MDX clients.

### `t09-storage-modes-2.md` (48 notes)

- Covers: Choosing a storage mode; Composite models; Push datasets.
- DAX functions: ALLSELECTED, DISTINCTCOUNT, LOOKUPVALUE, USERELATIONSHIP.
- Features: push datasets, composite models, DirectQuery, memory, import mode, calculation groups, refresh and processing, DAX queries, relationships, fact tables, date table, hierarchies, blank handling.

## Security

### `t10-security-1.md` (45 notes)

- Covers: Dynamic security, relationships and testing; Role filter performance; Totals under row-level security; Object-level security and active roles.
- DAX functions: ALL, USERELATIONSHIP, TREATAS, VALUES, CALCULATETABLE, PATHCONTAINS, LEFT, CROSSFILTER, CALCULATE, ISCROSSFILTERED, FILTER, FALSE, SELECTEDVALUE, CONCATENATEX, CONTAINSSTRING, IF, ERROR.
- Features: row-level security, dimension tables, relationships, totals and subtotals, fact tables, calculated tables, object-level security, storage engine, error handling, external tools, hierarchies, dynamic security, inactive relationships, virtual relationships, blank handling, DAX queries.

## Calculation groups and field parameters

### `t11-calculation-groups-and-field-parameters-1.md` (45 notes)

- Covers: Calculation group design patterns; Calculation item application; Format string expressions.
- DAX functions: CALCULATE, ISSELECTEDMEASURE, SELECTEDMEASURE, IF, SELECTEDMEASURENAME, SELECTEDMEASUREFORMATSTRING, SWITCH, FALSE, TREATAS, USERELATIONSHIP, SELECTEDVALUE, SAMEPERIODLASTYEAR, DATESYTD.
- Features: calculation groups, format strings, DAX queries, dynamic format strings, totals and subtotals, bidirectional filters, bridge tables, error handling, slicers, relationships, time intelligence, external tools, SVG and custom visuals, calculated tables, filter context, fact tables.

### `t11-calculation-groups-and-field-parameters-2.md` (42 notes)

- Covers: Calculation group precedence; Per-user defaults and slicers; Field parameters; Selection expressions.
- DAX functions: CALCULATE, SELECTEDMEASURE, ISCROSSFILTERED, USERPRINCIPALNAME, SELECTEDVALUE, VALUES, MAX, SELECTEDMEASURENAME, ALLSELECTED, SWITCH, ALL, CONCATENATEX, NAMEOF, ERROR.
- Features: calculation groups, slicers, field parameters, relationships, parameter tables, format strings, many-to-many, currency conversion, testing and debugging, row-level security, dynamic format strings, dynamic security, cardinality, variables, formula engine, hierarchies, Excel and MDX clients, DAX formatting, conditional formatting, error handling.

## Window functions and visual calculations

### `t12-window-functions-and-visual-calculations-1.md` (78 notes)

- Covers: Measure or visual calculation; Window functions and apply semantics; Ranking with RANK and RANKX; Visual context and virtual table; Running totals and performance.
- DAX functions: RANK, RANKX, OFFSET, CALCULATE, ORDERBY, INDEX, WINDOW, ALL, VALUES, ALLSELECTED, ISINSCOPE, FILTER, PARTITIONBY, MATCHBY, IF, FORMAT, DISTINCT, MAX, SUMX, SWITCH, ALLEXCEPT, AVERAGEX, ADDCOLUMNS, HASONEVALUE, MINX, CALCULATETABLE, RUNNINGSUM, SUMMARIZECOLUMNS. Also named, though missing from the function index of the model skill: EXPAND, COLLAPSE, COLLAPSEALL, PREVIOUS, ISATLEVEL, EXPANDALL, LAST, NEXT.
- Features: visual calculations, ranking, totals and subtotals, window functions, hierarchies, DAX queries, running totals, matrix visual, filter context, iterators, DAX formatting, partitions, blank handling, distinct counts, granularity, slicers, conditional formatting, moving averages, row context, variables, fact tables, storage engine, relationships, sort by column.

## User-defined functions in DAX

### `t13-user-defined-functions-1.md` (48 notes)

- Covers: Naming and model-independent functions; Functions, measures and calculation groups; Parameters, types and passing modes; Calendar filters and result checks.
- DAX functions: CALCULATE, REMOVEFILTERS, TABLEOF, SUMX, SUM, ISCROSSFILTERED, ISFILTERED, NAMEOF, ERROR, ISBLANK, BLANK, DATESINPERIOD, RANGE.
- Features: user-defined functions, calendar-based time intelligence, calculation groups, DAX queries, iterators, testing and debugging, row context, naming, context transition, error handling, filter context, data types, blank handling, time intelligence, visual calculations.

## Business calculation patterns

### `t14-business-calculation-patterns-1.md` (53 notes)

- Covers: Totals and hierarchy levels; Budget, currency and financial calculations.
- DAX functions: CALCULATE, VALUES, ALLEXCEPT, CONTAINS, FILTER, ALL, ISFILTERED, SUMX, KEEPFILTERS, REMOVEFILTERS, SUMMARIZE, DATESYTD, PRODUCTX.
- Features: totals and subtotals, iterators, budget and forecast, fact tables, relationships, hierarchies, blank handling, currency conversion, filter context, date table, slicers, context transition, virtual relationships, charts, DAX queries, snapshot tables, error handling, granularity, calculation groups.

### `t14-business-calculation-patterns-2.md` (49 notes)

- Covers: Customer, product and campaign analysis.
- DAX functions: CALCULATE, REMOVEFILTERS, VALUES, CROSSFILTER, GENERATE, SUMMARIZE, ALLSELECTED, SWITCH, WINDOW, ISINSCOPE, RELATED, DATEADD, DATESINPERIOD, GENERATEALL, SELECTCOLUMNS, MIN, ADDCOLUMNS, UNION, EXCEPT, INTERSECT, DATESBETWEEN, ERROR, PARTITIONBY, ISBLANK, KEEPFILTERS, DIVIDE. Also named, though missing from the function index of the model skill: COLLAPSE.
- Features: fact tables, charts, blank handling, dimension tables, bridge tables, calculated tables, totals and subtotals, calculated columns, ABC and segmentation, DAX queries, slicers, relationships, tooltips, blank row of an invalid relationship, Power Query, running totals, refresh and processing, error handling, Excel and MDX clients, matrix visual, variables, visual calculations.

### `t14-business-calculation-patterns-3.md` (32 notes)

- Covers: Semi-additive and running totals.
- DAX functions: CALCULATE, LASTDATE, LASTNONBLANK, ALL, FIRSTNONBLANK, FILTER, MAX, STARTOFQUARTER, ENDOFMONTH, CLOSINGBALANCEMONTH, STARTOFMONTH, STARTOFYEAR, ENDOFQUARTER, ENDOFYEAR, OPENINGBALANCEMONTH, ISCROSSFILTERED, FIRSTDATE, VALUES, IF, CLOSINGBALANCEYEAR, OPENINGBALANCEYEAR, CLOSINGBALANCEQUARTER, OPENINGBALANCEQUARTER, YEAR, PARALLELPERIOD, QUARTER, TREATAS, SUMX, DATESYTD, TRUE, REMOVEFILTERS.
- Features: snapshot tables, totals and subtotals, semi-additive measures, dimension tables, DAX queries, memory, running totals, blank handling, date table, filter context, cardinality, context transition, iterators, relationships.

### `t14-business-calculation-patterns-4.md` (53 notes)

- Covers: Ranking and top N.
- DAX functions: RANKX, ALLSELECTED, TOPN, ALL, CALCULATE, GENERATE, VALUES, HASONEVALUE, KEEPFILTERS, ISINSCOPE, REMOVEFILTERS, FIRSTNONBLANK, CONCATENATEX, CALCULATETABLE.
- Features: ranking, visual-level filters, matrix visual, totals and subtotals, iterators, sort by column, variables, blank handling, calculated columns, DAX queries, Excel and MDX clients, filter context, context transition, calculated tables, charts, slicers, DAX formatting.

### `t14-business-calculation-patterns-5.md` (57 notes)

- Covers: Events, durations and sequences; Building and testing calculations; Averages, working days and trends.
- DAX functions: LINESTX, AVERAGEX, LINEST, SELECTCOLUMNS, DIVIDE, COUNTROWS, SUMX, CURRENTGROUP, GROUPBY, TRUE, FALSE, ALLEXCEPT, CALCULATETABLE, CALCULATE, ALL, SUM, HASONEVALUE, TOPN, NETWORKDAYS, RANKX, ADDCOLUMNS, KEEPFILTERS, COALESCE.
- Features: date table, calculated columns, variables, DAX queries, blank handling, moving averages, iterators, totals and subtotals, dimension tables, calendar-based time intelligence, charts, testing and debugging, filter context, relationships, context transition, Power Query, calculated tables, fact tables, running totals, slicers, ranking.

## Report-facing DAX and report design

### `t15-report-facing-dax-1.md` (50 notes)

- Covers: Slicers and measure filters; Report design and requirements.
- DAX functions: OR, CALCULATE, AND, ALLSELECTED, COUNTROWS, UNION, SELECTCOLUMNS, DISTINCT, REMOVEFILTERS, SELECTEDMEASURE, KEEPFILTERS, FILTER, VALUES, SELECTEDVALUE, SWITCH.
- Features: slicers, granularity, charts, DAX queries, visual-level filters, matrix visual, DAX formatting, report themes, calculation groups, totals and subtotals, drillthrough, budget and forecast, relationships, many-to-many, cardinality, blank handling.

### `t15-report-facing-dax-2.md` (68 notes)

- Covers: Measures written for visuals; Model support for reports; Tooltips, drillthrough and detail rows.
- DAX functions: CONCATENATEX, DETAILROWS, CALCULATETABLE, VALUES, TOPN, UNICHAR, RAND, ISINSCOPE, RELATED, SUMMARIZECOLUMNS, SAMEPERIODLASTYEAR, DISTINCTCOUNT, SELECTEDVALUE, FILTER, BLANK, CALCULATE, CROSSFILTER, SUMMARIZE, ADDCOLUMNS, NATURALINNERJOIN, UNION, MEASURE, DEFINE.
- Features: detail rows, blank handling, drillthrough, Excel and MDX clients, tooltips, charts, filter context, matrix visual, DAX queries, calculated tables, dimension tables, external tools, refresh and processing, DAX formatting, format strings, documentation and descriptions, calculation groups, testing and debugging, parameter tables, date table, calculated columns, fact tables, bidirectional filters, iterators.

### `t15-report-facing-dax-3.md` (46 notes)

- Covers: Choosing and building charts.
- DAX functions: MAX, CALCULATE, ALLEXCEPT, EOMONTH, KEEPFILTERS, ALLSELECTED, DATESBETWEEN, MAXX, REMOVEFILTERS, ROUNDUP, TREATAS, RAND.
- Features: charts, SVG and custom visuals, report themes, hierarchies, calendar-based time intelligence, tooltips, ABC and segmentation, totals and subtotals, data categories and geography, week-based calendars, slicers, error handling.

### `t15-report-facing-dax-4.md` (67 notes)

- Covers: Conditional formatting and KPIs; Format strings in reports.
- DAX functions: ALLSELECTED, ISINSCOPE, SELECTEDMEASURE, REMOVEFILTERS, VALUES, RANKX, FORMAT, CALCULATETABLE, SELECTEDVALUE, MOD, MAXX, MINX, TREATAS, SWITCH, TRUE, CALCULATE, UNICODE, UNICHAR, TRUNC. Also named, though missing from the function index of the model skill: ISATLEVEL, COLLAPSE, COLLAPSEALL.
- Features: DAX formatting, format strings, dynamic format strings, Excel and MDX clients, KPIs, conditional formatting, report themes, visual calculations, hierarchies, DAX queries, matrix visual, totals and subtotals, calculation groups, charts, ranking, documentation and descriptions, blank handling, slicers, external tools, testing and debugging.

### `t15-report-facing-dax-5.md` (59 notes)

- Covers: Custom and SVG visuals; Themes and report templates.
- DAX functions: none named.
- Features: SVG and custom visuals, AI assistance, report themes, charts, DAX formatting, error handling, documentation and descriptions, conditional formatting, matrix visual, testing and debugging, TMDL and project files, slicers.

## Tooling, workflow and AI assistance

### `t16-tooling-and-workflow-1.md` (44 notes)

- Covers: Scripting with TOM and APIs; Choosing development tools; Translations and renaming objects.
- DAX functions: none named.
- Features: external tools, translations, Excel and MDX clients, refresh and processing, DAX queries, AI assistance, incremental refresh, VertiPaq, naming, partitions, testing and debugging.

### `t16-tooling-and-workflow-2.md` (46 notes)

- Covers: Model edits with external tools; Query tracing and debugging.
- DAX functions: TOCSV, TOJSON, ALLSELECTED, EVALUATEANDLOG, CONCATENATEX, CALCULATETABLE, TOPN, FORMAT, SUMMARIZECOLUMNS.
- Features: external tools, testing and debugging, DAX queries, variables, KPIs, slicers, Performance Analyzer, refresh and processing, filter context, shadow filter context, DAX formatting, format strings.

### `t16-tooling-and-workflow-3.md` (61 notes)

- Covers: Reusable libraries and templates; AI assistants and agents; Testing measures.
- DAX functions: CALCULATE, RANK, EVALUATE, UNION, TREATAS, COALESCE.
- Features: AI assistance, testing and debugging, TMDL and project files, DAX queries, user-defined functions, error handling, external tools, report themes, documentation and descriptions, filter context, date table, totals and subtotals, dimension tables, DAX formatting, ranking, blank handling.
