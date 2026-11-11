# Practice library: index

Read this file first, then open only the file that fits the task. Never read the whole library for one task.

Each entry names one file in this folder, what it covers, and the DAX functions and Power BI features its notes mention (most frequent first). A function or feature can appear in several files: pick the file whose topic fits the question. How to use a note is set out in the skill file one folder up.

| Topic | Files | Notes |
|---|---|---:|
| DAX evaluation context | `t01-evaluation-context-1.md` to `t01-evaluation-context-2.md` | 157 |
| DAX authoring style | `t02-dax-authoring-style-1.md` to `t02-dax-authoring-style-2.md` | 116 |
| DAX table functions and queries | `t03-table-functions-and-queries-1.md` to `t03-table-functions-and-queries-2.md` | 155 |
| Time intelligence and date tables | `t04-time-intelligence-and-dates-1.md` to `t04-time-intelligence-and-dates-3.md` | 168 |
| Relationships and filter propagation | `t05-relationships-1.md` | 69 |
| Data model design | `t06-data-model-design-1.md` to `t06-data-model-design-2.md` | 130 |
| DAX performance and optimization | `t07-dax-performance-1.md` to `t07-dax-performance-3.md` | 185 |
| Storage engine, model size and memory | `t08-storage-engine-and-model-size-1.md` | 33 |
| Storage modes | `t09-storage-modes-1.md` to `t09-storage-modes-2.md` | 99 |
| Security | `t10-security-1.md` | 48 |
| Calculation groups and field parameters | `t11-calculation-groups-and-field-parameters-1.md` to `t11-calculation-groups-and-field-parameters-2.md` | 90 |
| Window functions and visual calculations | `t12-window-functions-and-visual-calculations-1.md` | 79 |
| User-defined functions in DAX | `t13-user-defined-functions-1.md` | 49 |
| Business calculation patterns | `t14-business-calculation-patterns-1.md` to `t14-business-calculation-patterns-5.md` | 247 |
| Report-facing DAX and report design | `t15-report-facing-dax-1.md` to `t15-report-facing-dax-5.md` | 294 |
| Tooling, workflow and AI assistance | `t16-tooling-and-workflow-1.md` to `t16-tooling-and-workflow-3.md` | 154 |

## DAX evaluation context

### `t01-evaluation-context-1.md` (82 notes)

- Covers: KEEPFILTERS and arbitrary filters; CALCULATE filter arguments; Visual queries and auto-exist; Reading the selected value; Row context and iterators.
- DAX functions: CALCULATE, KEEPFILTERS, FILTER, VALUES, ALL, SELECTEDVALUE, CALCULATETABLE, SUMX, CROSSJOIN, SUMMARIZE, HASONEVALUE, ISINSCOPE, IF, RELATED, TRUE, SUM, SUMMARIZECOLUMNS, OR, ISFILTERED, RELATEDTABLE, AVERAGEX, SELECTCOLUMNS, AND, RANKX, REMOVEFILTERS, LASTDATE, CONTAINS, CROSSFILTER, ERROR, COUNTROWS, FALSE, MIN, MAX, AVERAGE, MINX, MAXX.
- Features: iterators, DAX queries, filter context, row context, slicers, error handling, totals and subtotals, relationships, context transition, cardinality, auto-exist, blank handling, variables, calculated columns, Excel and MDX clients, storage engine, sort by column, blank row of an invalid relationship, matrix visual, expanded tables, hierarchies, dimension tables, parameter tables.

### `t01-evaluation-context-2.md` (75 notes)

- Covers: Relationships, expanded tables and lineage; Context transition; Removing filters with ALL; ALLSELECTED and shadow filters; Totals and additivity.
- DAX functions: CALCULATE, ALL, ALLSELECTED, CALCULATETABLE, RELATED, VALUES, ALLEXCEPT, REMOVEFILTERS, FILTER, RELATEDTABLE, ALLCROSSFILTERED, TREATAS, ADDCOLUMNS, MAX, SUMMARIZE, USERELATIONSHIP, SELECTEDVALUE, SUMMARIZECOLUMNS, LASTDATE, DISTINCTCOUNT, SUMX, AVERAGEX, COUNTROWS, SELECTCOLUMNS, MIN, SUM, EARLIER, MINX, MAXX.
- Features: iterators, filter context, relationships, row context, context transition, calculated columns, totals and subtotals, fact tables, shadow filter context, dimension tables, DAX queries, expanded tables, variables, error handling, limited relationships, inactive relationships, data lineage, bidirectional filters, budget and forecast, virtual relationships, matrix visual, DirectQuery.

## DAX authoring style

### `t02-dax-authoring-style-1.md` (69 notes)

- Covers: Formatting, naming and references; Variables and their evaluation; BLANK handling and conditions.
- DAX functions: IF, BLANK, SWITCH, DIVIDE, ADDCOLUMNS, ISBLANK, CALCULATE, SUMX, COALESCE, VAR, TOPN, AVERAGEX, NOT, VALUES, FILTER, FALSE, COUNTROWS, ALL, CALCULATETABLE, VALUE, TREATAS, CONCATENATEX, RELATEDTABLE, ERROR, MINX, MAXX.
- Features: variables, blank handling, iterators, error handling, DAX queries, filter context, relationships, blank row of an invalid relationship, data types, DAX formatting, row context, calculated columns, calculated tables, naming, data lineage, totals and subtotals.

### `t02-dax-authoring-style-2.md` (47 notes)

- Covers: IN operator and constructors; Data types and comparisons.
- DAX functions: CALCULATE, NOT, OR, CONTAINSROW, FILTER, INT, CONVERT, ALL, CONTAINS, TREATAS, SUMMARIZE, CALCULATETABLE, SUMX, EXCEPT, VALUES, AND, ISEMPTY, INTERSECT, DIVIDE, UNION, LOWER.
- Features: data types, error handling, testing and debugging, iterators, fact tables, currency conversion, virtual relationships, DAX formatting, conditional formatting, totals and subtotals.

## DAX table functions and queries

### `t03-table-functions-and-queries-1.md` (80 notes)

- Covers: Grouping and adding columns; Writing DAX queries; Filter and text conditions.
- DAX functions: SUMMARIZE, ADDCOLUMNS, CALCULATE, CALCULATETABLE, GROUPBY, FILTER, CURRENTGROUP, SEARCH, SELECTCOLUMNS, DEFINE, EVALUATE, CONTAINSSTRING, MAXX, DETAILROWS, VALUES, GENERATE, ISEMPTY, CONTAINS, ROW, LEFT, ALL, FIND, AND, ROLLUP, SUM, OR, DATATABLE, TREATAS, KEEPFILTERS, REMOVEFILTERS, MAX, BLANK, CROSSJOIN, TOPN, ALLEXCEPT, CONTAINSSTRINGEXACT, SUBSTITUTE, IFERROR, RIGHT, RELATEDTABLE.
- Features: DAX queries, iterators, variables, relationships, filter context, Excel and MDX clients, totals and subtotals, blank handling, row context, context transition, fact tables, materialization, slicers, expanded tables, dimension tables, formula engine, query plans, testing and debugging, blank row of an invalid relationship, detail rows.

### `t03-table-functions-and-queries-2.md` (75 notes)

- Covers: Calculated and static tables; SUMMARIZECOLUMNS behaviour; Joins and lookups; Set functions.
- DAX functions: SUMMARIZECOLUMNS, LOOKUPVALUE, SUMMARIZE, NATURALLEFTOUTERJOIN, NATURALINNERJOIN, ADDCOLUMNS, UNION, EXCEPT, TREATAS, INTERSECT, RELATED, CROSSJOIN, GENERATE, SELECTCOLUMNS, VALUES, CALCULATE, GENERATESERIES, ROW, CALCULATETABLE, FILTER, DATATABLE, CONTAINS, SELECTEDVALUE, RELATEDTABLE, CURRENCY, CALENDAR, GENERATEALL, CONVERT, ALL, ISBLANK, REMOVEFILTERS, COALESCE, NOT.
- Features: relationships, data lineage, fact tables, error handling, virtual relationships, calculated tables, DAX queries, blank handling, variables, data types, query plans, storage engine, row context, expanded tables, limited relationships, auto-exist, iterators, calculated columns, currency conversion, compression, blank row of an invalid relationship.

## Time intelligence and date tables

### `t04-time-intelligence-and-dates-1.md` (60 notes)

- Covers: Time intelligence functions; Week-based and fiscal calendars; Mark as date table.
- DAX functions: CALCULATE, DATEADD, LASTDATE, FILTER, VALUES, DATESYTD, ALL, CALCULATETABLE, PARALLELPERIOD, REMOVEFILTERS, FIRSTDATE, ALLEXCEPT, DATESINPERIOD, SAMEPERIODLASTYEAR, TOTALYTD, CONTAINS, NEXTDAY, PREVIOUSDAY, KEEPFILTERS, FILTERS, AVERAGEX, YEAR, MIN, MAX, COUNTROWS, DATESBETWEEN, WEEKDAY, SELECTEDMEASURE, QUARTER, MONTH, DAY, NEXTQUARTER, PREVIOUSQUARTER, NEXTMONTH, NEXTYEAR, PREVIOUSYEAR, PREVIOUSMONTH.
- Features: date table, time intelligence, calendar-based time intelligence, week-based calendars, relationships, fiscal calendars, row context, fact tables, iterators, moving averages, slicers, totals and subtotals, context transition, DAX queries, data types, filter context, calculated columns, blank handling, external tools, Power Query.

### `t04-time-intelligence-and-dates-2.md` (64 notes)

- Covers: Incomplete periods and future dates; Period-over-period comparisons; Building a Date table.
- DAX functions: CALCULATE, REMOVEFILTERS, MAX, SAMEPERIODLASTYEAR, DATESYTD, LASTNONBLANK, ALLEXCEPT, TODAY, SELECTEDVALUE, YEAR, DIVIDE, DATESBETWEEN, FILTER, SELECTEDMEASURE, KEEPFILTERS, CALENDARAUTO, CALCULATETABLE, IF, ALL, VALUES, EDATE, QUARTER, TREATAS, MONTH, PARALLELPERIOD, ALLNOBLANKROW, USERELATIONSHIP, COUNTROWS, ALLSELECTED, DATESINPERIOD, RANKX, ERROR, IFERROR, SELECTCOLUMNS, DATATABLE, CALENDAR, MIN.
- Features: date table, slicers, calculated columns, time intelligence, external tools, calculation groups, fact tables, blank handling, charts, relationships, calendar-based time intelligence, filter context, auto date/time, DAX queries, visual-level filters, context transition, calculated tables, hierarchies, fiscal calendars, refresh and processing, inactive relationships, error handling.

### `t04-time-intelligence-and-dates-3.md` (44 notes)

- Covers: Date columns, sorting and formats; Blank and placeholder dates; Calendar-based time intelligence.
- DAX functions: DATEADD, DATESINPERIOD, SAMEPERIODLASTYEAR, FORMAT, NOT, ISBLANK, CALENDARAUTO, BLANK, DATESBETWEEN, CALCULATE, FILTER, VALUES, REMOVEFILTERS, NEXTMONTH, DATESYTD.
- Features: date table, calendar-based time intelligence, time intelligence, blank handling, format strings, charts, hierarchies, blank row of an invalid relationship, slicers, relationships, totals and subtotals, data categories and geography, fiscal calendars, fact tables, sort by column, TMDL and project files.

## Relationships and filter propagation

### `t05-relationships-1.md` (69 notes)

- Covers: Many-to-many relationships; Virtual relationships in DAX; Bidirectional filters and propagation; Blank row and limited relationships; Inactive relationships and date roles.
- DAX functions: CALCULATE, TREATAS, USERELATIONSHIP, FILTER, INTERSECT, ALL, VALUES, ISEMPTY, CONTAINS, SUMMARIZE, CROSSFILTER, AND, COUNTROWS, IF, NOT, ISFILTERED, CALCULATETABLE, ISCROSSFILTERED, CROSSJOIN, INT, OR, RANKX, SUMMARIZECOLUMNS, ALLNOBLANKROW, LOOKUPVALUE, RELATED.
- Features: relationships, many-to-many, dimension tables, virtual relationships, bidirectional filters, cardinality, blank handling, inactive relationships, bridge tables, blank row of an invalid relationship, date table, slicers, visual-level filters, limited relationships, totals and subtotals, storage engine, query plans, fact tables, calculated tables, formula engine, calculated columns, charts.

## Data model design

### `t06-data-model-design-1.md` (67 notes)

- Covers: Dates, time and sort keys; Calculated columns versus measures; Source views, names, data types; Star schema and fact tables.
- DAX functions: SUMX, RELATED, VALUES, REMOVEFILTERS, RANKX, LOOKUPVALUE, SUM, IGNORE, SUMMARIZECOLUMNS.
- Features: calculated columns, dimension tables, fact tables, import mode, Power Query, star schema, date table, relationships, SQL views, data types, memory, naming, slicers, refresh and processing, compression, auto-exist, blank handling, hierarchies, totals and subtotals, sort by column, charts, model size, iterators, DAX queries.

### `t06-data-model-design-2.md` (63 notes)

- Covers: Business-rule grain and testing; Duplicate names, Group By Columns; Circular dependency errors; Sankey chart funnels; User-context calculated columns.
- DAX functions: CALCULATE, SUMMARIZE, ALLEXCEPT, ALLNOBLANKROW, VALUES, ALL, SELECTEDVALUE, SUMX, AVERAGE, FILTER, IF, CALCULATETABLE, UNICHAR, HASONEVALUE, TREATAS, COUNTROWS, USERELATIONSHIP, USERCULTURE, LOOKUPVALUE, MIN, MAX, REMOVEFILTERS, COMBINEVALUES, REPT, RANKX, ADDCOLUMNS, SUMMARIZECOLUMNS, SELECTCOLUMNS, ISFILTERED, CUSTOMDATA, USERNAME, USEROBJECTID, USERPRINCIPALNAME, FALSE.
- Features: calculated columns, relationships, error handling, context transition, blank handling, slicers, charts, iterators, calculated tables, Excel and MDX clients, totals and subtotals, blank row of an invalid relationship, cardinality, testing and debugging, DAX queries, refresh and processing, row-level security, storage engine, CallbackDataID, virtual relationships, memory.

## DAX performance and optimization

### `t07-dax-performance-1.md` (64 notes)

- Covers: Filters, counts and emptiness tests; Measuring and testing performance; Formula and storage engine.
- DAX functions: CALCULATE, ISEMPTY, DISTINCTCOUNT, SUMX, COUNTROWS, FILTER, IF, LASTNONBLANK, CALCULATETABLE, KEEPFILTERS, VALUES, AND, ISBLANK, ALL, BLANK, SUM, FIRSTNONBLANK, NOT, SUMMARIZECOLUMNS, EXCEPT, INTERSECT, SELECTEDVALUE, DIVIDE, MIN, AVERAGE.
- Features: distinct counts, storage engine, DAX queries, fact tables, Performance Analyzer, formula engine, external tools, testing and debugging, query plans, iterators, refresh and processing, filter context, materialization, totals and subtotals, DirectQuery, memory, relationships, AI assistance, cardinality, date table, CallbackDataID, import mode.

### `t07-dax-performance-2.md` (52 notes)

- Covers: Model design, relationships and memory; Server, processing and hardware; Report visuals and Excel clients.
- DAX functions: IF, CALCULATE.
- Features: memory, relationships, refresh and processing, Excel and MDX clients, cardinality, storage engine, compression, fact tables, partitions, VertiPaq, dimension tables, many-to-many, DAX queries, import mode, star schema, query plans, testing and debugging.

### `t07-dax-performance-3.md` (69 notes)

- Covers: Iterators and materialization; Conditional logic and variables; Text search and its index.
- DAX functions: IF, CONTAINSSTRING, SEARCH, SWITCH, CALCULATE, LASTNONBLANKVALUE, SUMX, COUNTROWS, LASTNONBLANK, FILTER, SELECTEDVALUE, RANKX, DATESBETWEEN, LOOKUPVALUE, MAX, SUMMARIZE, SUM, ALL, FIRSTNONBLANK, FIRSTNONBLANKVALUE, CALCULATETABLE, SUMMARIZECOLUMNS, RELATED, NATURALLEFTOUTERJOIN, TREATAS, ROUND, ADDCOLUMNS, OFFSET, ISBLANK, NOT, IF.EAGER, CONTAINSSTRINGEXACT, FIND.
- Features: iterators, storage engine, DAX queries, variables, formula engine, fact tables, blank handling, slicers, CallbackDataID, materialization, cardinality, context transition, filter context, query plans, memory, testing and debugging, refresh and processing, dimension tables, row context, calculated columns, ranking, totals and subtotals.

## Storage engine, model size and memory

### `t08-storage-engine-and-model-size-1.md` (33 notes)

- Covers: Reducing column cardinality; Measuring model size; Analysis Services processing; Calculated column and table storage.
- DAX functions: NOW, SUMX, COUNTROWS, SUMMARIZE, DISTINCTCOUNT, MOD, CALCULATETABLE, INT, MAX, LOOKUPVALUE, MONTH, RELATED, ALL, CROSSJOIN.
- Features: memory, refresh and processing, dictionaries, calculated columns, VertiPaq, external tools, compression, calculated tables, fact tables, data types, partitions.

## Storage modes

### `t09-storage-modes-1.md` (50 notes)

- Covers: DirectQuery DAX and limits; DirectQuery model and source design.
- DAX functions: ADDCOLUMNS, SUMMARIZECOLUMNS, CALCULATE, BLANK, SAMEPERIODLASTYEAR, COMBINEVALUES, MEDIANX, ALL, INT, ISEMPTY, NOT, LASTNONBLANK, CEILING, LEFT, SECOND, SEARCH, SUBSTITUTE, TRIM, REPLACE, LEN, LOG10, MID, POWER, LN, LOG, SUMMARIZE, MAX, REMOVEFILTERS, DATEADD, DATESBETWEEN, DATESYTD.
- Features: DirectQuery, memory, relationships, import mode, formula engine, time intelligence, calculated columns, external tools, DAX queries, partitions, row-level security, storage engine, query plans, VertiPaq, fact tables, error handling, granularity, totals and subtotals, detail rows, refresh and processing, testing and debugging, blank handling, Excel and MDX clients.

### `t09-storage-modes-2.md` (49 notes)

- Covers: Choosing a storage mode; Composite models; Push datasets.
- DAX functions: ALLSELECTED, DISTINCTCOUNT, LOOKUPVALUE, SUMX, USERELATIONSHIP, SUM.
- Features: push datasets, composite models, DirectQuery, memory, import mode, refresh and processing, calculation groups, DAX queries, relationships, fact tables, date table, hierarchies, blank handling.

## Security

### `t10-security-1.md` (48 notes)

- Covers: Dynamic security, relationships and testing; Role filter performance; Totals under row-level security; Object-level security and active roles.
- DAX functions: ALL, USERELATIONSHIP, TREATAS, VALUES, CALCULATETABLE, LEFT, PATHCONTAINS, CROSSFILTER, CALCULATE, ISCROSSFILTERED, SUMMARIZE, FALSE, FILTER, SELECTEDVALUE, CONCATENATEX, CONTAINSSTRING, ERROR, IF.
- Features: row-level security, dimension tables, totals and subtotals, relationships, fact tables, calculated tables, hierarchies, object-level security, storage engine, error handling, dynamic security, inactive relationships, virtual relationships, bidirectional filters, blank handling, DAX queries.

## Calculation groups and field parameters

### `t11-calculation-groups-and-field-parameters-1.md` (47 notes)

- Covers: Calculation group design patterns; Calculation item application; Format string expressions.
- DAX functions: CALCULATE, ISSELECTEDMEASURE, SELECTEDMEASURE, IF, SELECTEDMEASURENAME, SELECTEDMEASUREFORMATSTRING, SWITCH, VALUES, FALSE, TREATAS, SELECTCOLUMNS, HASONEVALUE, ADDCOLUMNS, DATATABLE, SUMX, NATURALLEFTOUTERJOIN, USERELATIONSHIP, DATESBETWEEN, SELECTEDVALUE, CALCULATETABLE, DATESYTD, SAMEPERIODLASTYEAR.
- Features: calculation groups, format strings, DAX queries, dynamic format strings, totals and subtotals, bridge tables, error handling, slicers, time intelligence, bidirectional filters, SVG and custom visuals, calculated tables, filter context, relationships, fact tables.

### `t11-calculation-groups-and-field-parameters-2.md` (43 notes)

- Covers: Calculation group precedence; Per-user defaults and slicers; Field parameters; Selection expressions.
- DAX functions: CALCULATE, ISCROSSFILTERED, SELECTEDMEASURE, USERPRINCIPALNAME, VALUES, ALLSELECTED, SELECTEDVALUE, MAX, SELECTEDMEASURENAME, SWITCH, ALL, CALCULATETABLE, FILTER, CONCATENATEX, NAMEOF, ERROR.
- Features: calculation groups, slicers, field parameters, parameter tables, format strings, many-to-many, relationships, currency conversion, testing and debugging, row-level security, dynamic format strings, dynamic security, variables, formula engine, hierarchies, naming, DAX formatting, conditional formatting, error handling.

## Window functions and visual calculations

### `t12-window-functions-and-visual-calculations-1.md` (79 notes)

- Covers: Measure or visual calculation; Window functions and apply semantics; Ranking with RANK and RANKX; Visual context and virtual table; Running totals and performance.
- DAX functions: RANK, OFFSET, RANKX, WINDOW, INDEX, ORDERBY, CALCULATE, ALL, ALLSELECTED, ISINSCOPE, VALUES, HASONEVALUE, FILTER, AVERAGEX, PARTITIONBY, BLANK, SUMMARIZECOLUMNS, DISTINCTCOUNT, RUNNINGSUM, SELECTEDVALUE, MATCHBY, IF, FORMAT, MAX, SUMX, SWITCH, ALLEXCEPT, CROSSJOIN, ADDCOLUMNS, MINX, CALCULATETABLE.
- Features: visual calculations, ranking, totals and subtotals, window functions, hierarchies, DAX queries, running totals, matrix visual, filter context, iterators, DAX formatting, partitions, blank handling, distinct counts, granularity, slicers, conditional formatting, moving averages, row context, variables, fact tables, storage engine, relationships, sort by column.

## User-defined functions in DAX

### `t13-user-defined-functions-1.md` (49 notes)

- Covers: Naming and model-independent functions; Functions, measures and calculation groups; Parameters, types and passing modes; Calendar filters and result checks.
- DAX functions: CALCULATE, REMOVEFILTERS, TABLEOF, SUMX, ISBLANK, BLANK, SUM, ISFILTERED, ISCROSSFILTERED, FILTER, AVERAGEX, IF, ERROR, NAMEOF, DATESINPERIOD, MAX, RANGE.
- Features: user-defined functions, calendar-based time intelligence, calculation groups, iterators, DAX queries, row context, testing and debugging, naming, context transition, error handling, filter context, data types, blank handling, visual calculations.

## Business calculation patterns

### `t14-business-calculation-patterns-1.md` (53 notes)

- Covers: Totals and hierarchy levels; Budget, currency and financial calculations.
- DAX functions: CALCULATE, VALUES, ALL, ALLEXCEPT, CONTAINS, FILTER, ISFILTERED, SUMX, SUMMARIZE, IF, KEEPFILTERS, SUM, COUNTROWS, MAX, DIVIDE, DATESYTD, PRODUCTX.
- Features: totals and subtotals, iterators, budget and forecast, fact tables, relationships, hierarchies, blank handling, currency conversion, filter context, date table, slicers, context transition, virtual relationships, charts, DAX queries, snapshot tables, error handling, granularity, calculation groups.

### `t14-business-calculation-patterns-2.md` (49 notes)

- Covers: Customer, product and campaign analysis.
- DAX functions: CALCULATE, REMOVEFILTERS, VALUES, ISBLANK, FILTER, CALCULATETABLE, MIN, SUMMARIZE, CROSSFILTER, RELATED, SUMX, GENERATE, EXCEPT, ALLSELECTED, SWITCH, WINDOW, ISINSCOPE, DATEADD, DATESINPERIOD, AVERAGE, GENERATEALL, SELECTCOLUMNS, ALL, CONTAINS, COUNTROWS, ADDCOLUMNS, UNION, INTERSECT, DATESBETWEEN, BLANK, ERROR, PARTITIONBY, KEEPFILTERS, DIVIDE, RELATEDTABLE, ISEMPTY.
- Features: fact tables, charts, blank handling, dimension tables, bridge tables, calculated tables, totals and subtotals, calculated columns, ABC and segmentation, DAX queries, slicers, relationships, tooltips, blank row of an invalid relationship, running totals, refresh and processing, error handling, matrix visual, variables, visual calculations.

### `t14-business-calculation-patterns-3.md` (44 notes)

- Covers: Semi-additive and running totals; Building and testing calculations.
- DAX functions: CALCULATE, MAX, LASTDATE, ALL, LASTNONBLANK, SUMX, FIRSTNONBLANK, FILTER, SUM, VALUES, COUNTROWS, CLOSINGBALANCEMONTH, ENDOFMONTH, STARTOFMONTH, STARTOFQUARTER, ENDOFYEAR, OPENINGBALANCEYEAR, STARTOFYEAR, CLOSINGBALANCEQUARTER, ENDOFQUARTER, OPENINGBALANCEMONTH, CLOSINGBALANCEYEAR, OPENINGBALANCEQUARTER, TREATAS, ISCROSSFILTERED, FIRSTDATE, CURRENTGROUP, GROUPBY, IF, DATEADD, QUARTER, PARALLELPERIOD, YEAR, ADDCOLUMNS, CALCULATETABLE, DATESYTD, SELECTEDVALUE, TRUE, REMOVEFILTERS, TOPN.
- Features: snapshot tables, totals and subtotals, semi-additive measures, dimension tables, DAX queries, filter context, iterators, blank handling, variables, memory, running totals, date table, cardinality, context transition, testing and debugging, relationships.

### `t14-business-calculation-patterns-4.md` (53 notes)

- Covers: Ranking and top N.
- DAX functions: RANKX, ALLSELECTED, CALCULATE, TOPN, ISINSCOPE, ALL, GENERATE, VALUES, HASONEVALUE, KEEPFILTERS, MINX, FILTER, REMOVEFILTERS, FIRSTNONBLANK, SELECTEDVALUE, CONCATENATEX, CALCULATETABLE, MAX, GROUPBY.
- Features: ranking, visual-level filters, matrix visual, totals and subtotals, iterators, sort by column, variables, blank handling, calculated columns, DAX queries, filter context, context transition, calculated tables, charts, slicers, DAX formatting.

### `t14-business-calculation-patterns-5.md` (48 notes)

- Covers: Events, durations and sequences; Averages, working days and trends.
- DAX functions: COUNTROWS, AVERAGEX, LINESTX, ALLEXCEPT, FILTER, CALCULATE, SELECTCOLUMNS, DIVIDE, LINEST, CALCULATETABLE, VALUES, FALSE, TRUE, MIN, IF, ALL, GENERATE, ALLNOBLANKROW, SUM, HASONEVALUE, NETWORKDAYS, RANKX, ADDCOLUMNS, ISBLANK, COALESCE, KEEPFILTERS.
- Features: date table, calculated columns, moving averages, dimension tables, blank handling, DAX queries, calendar-based time intelligence, charts, relationships, fact tables, iterators, totals and subtotals, variables, context transition, calculated tables, running totals, slicers.

## Report-facing DAX and report design

### `t15-report-facing-dax-1.md` (51 notes)

- Covers: Slicers and measure filters; Report design and requirements.
- DAX functions: CALCULATE, OR, AND, FILTER, VALUES, ALL, SUMMARIZE, COUNTROWS, UNION, ALLSELECTED, SELECTEDMEASURE, GROUPBY, CROSSJOIN, CALCULATETABLE, SELECTCOLUMNS, SUMMARIZECOLUMNS, REMOVEFILTERS, KEEPFILTERS, SELECTEDVALUE, SWITCH.
- Features: slicers, granularity, charts, DAX queries, visual-level filters, matrix visual, DAX formatting, calculation groups, totals and subtotals, drillthrough, budget and forecast, relationships, many-to-many, cardinality, blank handling.

### `t15-report-facing-dax-2.md` (69 notes)

- Covers: Measures written for visuals; Model support for reports; Tooltips, drillthrough and detail rows.
- DAX functions: CONCATENATEX, DETAILROWS, CALCULATETABLE, TOPN, VALUES, CALCULATE, COUNTROWS, ISINSCOPE, SUMMARIZE, UNICHAR, BLANK, RAND, SAMEPERIODLASTYEAR, FILTER, CROSSFILTER, RELATED, SUMMARIZECOLUMNS, MIN, IF, MAX, SELECTEDVALUE, ISEMPTY, DISTINCTCOUNT, ADDCOLUMNS, NATURALINNERJOIN, UNION, DISTINCTCOUNTNOBLANK, MEASURE, FILTERS, ISFILTERED, DEFINE.
- Features: detail rows, blank handling, drillthrough, Excel and MDX clients, tooltips, charts, filter context, matrix visual, DAX queries, calculated tables, dimension tables, external tools, refresh and processing, DAX formatting, format strings, documentation and descriptions, testing and debugging, calculation groups, parameter tables, date table, calculated columns, fact tables, bidirectional filters, iterators.

### `t15-report-facing-dax-3.md` (47 notes)

- Covers: Choosing and building charts.
- DAX functions: MAX, CALCULATE, ALLEXCEPT, EOMONTH, DATE, INT, DIVIDE, DATESBETWEEN, MIN, IF, ALLSELECTED, KEEPFILTERS, MAXX, REMOVEFILTERS, ROUNDUP, TREATAS, SELECTEDVALUE, FLOOR, RAND.
- Features: charts, hierarchies, calendar-based time intelligence, DAX formatting, tooltips, ABC and segmentation, totals and subtotals, data categories and geography, week-based calendars, slicers, error handling.

### `t15-report-facing-dax-4.md` (67 notes)

- Covers: Conditional formatting and KPIs; Format strings in reports.
- DAX functions: ALLSELECTED, SELECTEDMEASURE, ISINSCOPE, REMOVEFILTERS, CALCULATETABLE, VALUES, RANKX, SWITCH, CALCULATE, FORMAT, SELECTEDVALUE, MOD, MINX, ADDCOLUMNS, SUMMARIZE, MAXX, TREATAS, TRUE, UNICODE, UNICHAR, TRUNC.
- Features: DAX formatting, format strings, dynamic format strings, KPIs, Excel and MDX clients, conditional formatting, visual calculations, hierarchies, DAX queries, matrix visual, totals and subtotals, calculation groups, charts, ranking, report themes, documentation and descriptions, blank handling, slicers, testing and debugging.

### `t15-report-facing-dax-5.md` (60 notes)

- Covers: Custom and SVG visuals; Themes and report templates.
- DAX functions: none named.
- Features: SVG and custom visuals, AI assistance, report themes, DAX formatting, charts, error handling, documentation and descriptions, conditional formatting, matrix visual, testing and debugging.

## Tooling, workflow and AI assistance

### `t16-tooling-and-workflow-1.md` (46 notes)

- Covers: Scripting with TOM and APIs; Choosing development tools; Translations and renaming objects.
- DAX functions: DB.
- Features: external tools, translations, Excel and MDX clients, refresh and processing, DAX queries, incremental refresh, VertiPaq, naming, partitions, testing and debugging.

### `t16-tooling-and-workflow-2.md` (47 notes)

- Covers: Model edits with external tools; Query tracing and debugging.
- DAX functions: TOCSV, TOJSON, ALLSELECTED, EVALUATEANDLOG, CONCATENATEX, CALCULATETABLE, TOPN, FORMAT, SUMMARIZECOLUMNS.
- Features: external tools, testing and debugging, DAX queries, variables, KPIs, slicers, refresh and processing, Performance Analyzer, filter context, shadow filter context, DAX formatting, format strings.

### `t16-tooling-and-workflow-3.md` (61 notes)

- Covers: Reusable libraries and templates; AI assistants and agents; Testing measures.
- DAX functions: CALCULATE, RANK, UNION, EVALUATE, COALESCE, TREATAS.
- Features: AI assistance, testing and debugging, DAX queries, user-defined functions, TMDL and project files, error handling, report themes, documentation and descriptions, filter context, date table, external tools, totals and subtotals, dimension tables, DAX formatting, ranking, blank handling.
