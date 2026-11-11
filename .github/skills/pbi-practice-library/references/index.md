# Practice library: index

Read this file first, then open only the file that fits the task. Never read the whole library for one task.

Each entry names one file in this folder, what it covers, and the DAX functions and Power BI features its notes mention (most frequent first). A function or feature can appear in several files: pick the file whose topic fits the question. How to use a note is set out in the skill file one folder up.

| Topic | Files | Notes |
|---|---|---:|
| DAX evaluation context | `t01-evaluation-context-1.md` to `t01-evaluation-context-3.md` | 165 |
| DAX authoring style | `t02-dax-authoring-style-1.md` to `t02-dax-authoring-style-2.md` | 123 |
| DAX table functions and queries | `t03-table-functions-and-queries-1.md` to `t03-table-functions-and-queries-2.md` | 162 |
| Time intelligence and date tables | `t04-time-intelligence-and-dates-1.md` to `t04-time-intelligence-and-dates-3.md` | 172 |
| Relationships and filter propagation | `t05-relationships-1.md` | 75 |
| Data model design | `t06-data-model-design-1.md` to `t06-data-model-design-2.md` | 136 |
| DAX performance and optimization | `t07-dax-performance-1.md` to `t07-dax-performance-3.md` | 190 |
| Storage engine, model size and memory | `t08-storage-engine-and-model-size-1.md` | 36 |
| Storage modes | `t09-storage-modes-1.md` to `t09-storage-modes-2.md` | 101 |
| Security | `t10-security-1.md` | 48 |
| Calculation groups and field parameters | `t11-calculation-groups-and-field-parameters-1.md` to `t11-calculation-groups-and-field-parameters-2.md` | 92 |
| Window functions and visual calculations | `t12-window-functions-and-visual-calculations-1.md` | 79 |
| User-defined functions in DAX | `t13-user-defined-functions-1.md` | 49 |
| Business calculation patterns | `t14-business-calculation-patterns-1.md` to `t14-business-calculation-patterns-5.md` | 257 |
| Tooling, workflow and AI assistance | `t16-tooling-and-workflow-1.md` to `t16-tooling-and-workflow-3.md` | 157 |

## DAX evaluation context

### `t01-evaluation-context-1.md` (55 notes)

- Covers: KEEPFILTERS and arbitrary filters; CALCULATE filter arguments; Visual queries and auto-exist.
- DAX functions: CALCULATE, KEEPFILTERS, FILTER, ALL, CALCULATETABLE, CROSSJOIN, VALUES, SUMMARIZE, SUMMARIZECOLUMNS, OR, ISFILTERED, LASTDATE, AND, AVERAGEX, REMOVEFILTERS, MAX, CONTAINS, IF.
- Features: iterators, DAX queries, auto-exist, filter context, cardinality, context transition, slicers, variables, totals and subtotals, error handling, sort by column, blank handling, Excel and MDX clients, storage engine, expanded tables, running totals, dimension tables.

### `t01-evaluation-context-2.md` (55 notes)

- Covers: Reading the selected value; Row context and iterators; Relationships, expanded tables and lineage.
- DAX functions: CALCULATE, RELATED, VALUES, SELECTEDVALUE, SUMX, HASONEVALUE, ISINSCOPE, RELATEDTABLE, ALL, USERELATIONSHIP, TRUE, SUM, IF, SELECTCOLUMNS, TREATAS, SUMMARIZE, COUNTROWS, MIN, ADDCOLUMNS, RANKX, CROSSFILTER, ERROR, FALSE, AVERAGE, MAX, MINX, AVERAGEX, MAXX, ALLEXCEPT, FILTER, LOOKUPVALUE, CALCULATETABLE.
- Features: iterators, relationships, row context, calculated columns, dimension tables, filter context, slicers, error handling, inactive relationships, totals and subtotals, context transition, DAX queries, fact tables, data lineage, blank row of an invalid relationship, blank handling, bidirectional filters, matrix visual, budget and forecast, virtual relationships, limited relationships, storage engine, hierarchies, expanded tables.

### `t01-evaluation-context-3.md` (55 notes)

- Covers: Context transition; Removing filters with ALL; ALLSELECTED and shadow filters; Totals and additivity.
- DAX functions: CALCULATE, ALL, ALLSELECTED, VALUES, CALCULATETABLE, REMOVEFILTERS, ALLEXCEPT, FILTER, ALLCROSSFILTERED, MAX, SUMMARIZE, SUMX, SELECTEDVALUE, SUMMARIZECOLUMNS, LASTDATE, DISTINCTCOUNT, AVERAGEX, IF, SUM, ADDCOLUMNS, SAMEPERIODLASTYEAR, RELATEDTABLE, EARLIER, MAXX, MINX.
- Features: iterators, filter context, context transition, row context, totals and subtotals, shadow filter context, DAX queries, calculated columns, fact tables, variables, relationships, limited relationships, dimension tables, time intelligence, error handling, matrix visual, expanded tables.

## DAX authoring style

### `t02-dax-authoring-style-1.md` (75 notes)

- Covers: Formatting, naming and references; Variables and their evaluation; BLANK handling and conditions.
- DAX functions: IF, BLANK, SWITCH, DIVIDE, SUMX, ADDCOLUMNS, ISBLANK, CALCULATE, VALUES, COALESCE, VAR, FILTER, TOPN, AVERAGEX, NOT, FALSE, COUNTROWS, MINX, SUM, RELATED, ALL, CALCULATETABLE, VALUE, TREATAS, CONCATENATEX, RELATEDTABLE, ERROR, MAXX.
- Features: variables, blank handling, iterators, error handling, DAX queries, filter context, relationships, blank row of an invalid relationship, row context, data types, DAX formatting, calculated columns, calculated tables, naming, data lineage, testing and debugging, totals and subtotals.

### `t02-dax-authoring-style-2.md` (48 notes)

- Covers: IN operator and constructors; Data types and comparisons.
- DAX functions: CALCULATE, NOT, ALL, FILTER, OR, CONTAINSROW, INT, CONVERT, CONTAINS, TREATAS, SUMMARIZE, CALCULATETABLE, SUMX, EXCEPT, VALUES, AND, INTERSECT, ISEMPTY, DIVIDE, LOWER, UNION.
- Features: data types, error handling, iterators, testing and debugging, fact tables, currency conversion, virtual relationships, DAX formatting, conditional formatting, totals and subtotals.

## DAX table functions and queries

### `t03-table-functions-and-queries-1.md` (84 notes)

- Covers: Grouping and adding columns; Writing DAX queries; Filter and text conditions.
- DAX functions: SUMMARIZE, ADDCOLUMNS, CALCULATE, CALCULATETABLE, GROUPBY, FILTER, CURRENTGROUP, SEARCH, SELECTCOLUMNS, DEFINE, EVALUATE, CONTAINSSTRING, ISEMPTY, MAXX, DETAILROWS, VALUES, GENERATE, CONTAINS, ROW, LEFT, OR, ALL, FIND, AND, ROLLUP, SUM, COUNTROWS, NOT, DATATABLE, TREATAS, KEEPFILTERS, REMOVEFILTERS, MAX, BLANK, CROSSJOIN, TOPN, ALLEXCEPT, CONTAINSSTRINGEXACT, SUBSTITUTE, RIGHT, IFERROR, RELATEDTABLE.
- Features: DAX queries, iterators, variables, relationships, filter context, Excel and MDX clients, totals and subtotals, blank handling, row context, context transition, fact tables, materialization, testing and debugging, query plans, slicers, expanded tables, dimension tables, formula engine, blank row of an invalid relationship, external tools, detail rows.

### `t03-table-functions-and-queries-2.md` (78 notes)

- Covers: Calculated and static tables; SUMMARIZECOLUMNS behaviour; Joins and lookups; Set functions.
- DAX functions: SUMMARIZECOLUMNS, LOOKUPVALUE, SUMMARIZE, NATURALLEFTOUTERJOIN, NATURALINNERJOIN, ADDCOLUMNS, UNION, TREATAS, INTERSECT, EXCEPT, VALUES, RELATED, CROSSJOIN, SELECTCOLUMNS, GENERATE, CALCULATE, GENERATESERIES, FILTER, CONTAINS, ROW, CALCULATETABLE, SELECTEDVALUE, DATATABLE, RELATEDTABLE, CURRENCY, CALENDAR, IF, HASONEVALUE, GENERATEALL, CONVERT, ISBLANK, ALL, REMOVEFILTERS, COALESCE, NOT.
- Features: relationships, data lineage, virtual relationships, fact tables, error handling, calculated tables, DAX queries, blank handling, variables, data types, query plans, storage engine, iterators, row context, filter context, expanded tables, limited relationships, auto-exist, calculated columns, currency conversion, compression, parameter tables, blank row of an invalid relationship.

## Time intelligence and date tables

### `t04-time-intelligence-and-dates-1.md` (61 notes)

- Covers: Time intelligence functions; Week-based and fiscal calendars; Mark as date table.
- DAX functions: CALCULATE, DATEADD, LASTDATE, VALUES, FILTER, DATESYTD, ALL, CALCULATETABLE, PARALLELPERIOD, REMOVEFILTERS, FIRSTDATE, ALLEXCEPT, DATESINPERIOD, SAMEPERIODLASTYEAR, TOTALYTD, CONTAINS, PREVIOUSDAY, NEXTDAY, KEEPFILTERS, FILTERS, AVERAGEX, YEAR, MAX, MIN, COUNTROWS, DATESBETWEEN, WEEKDAY, SELECTEDMEASURE, MONTH, QUARTER, DAY, PREVIOUSQUARTER, NEXTYEAR, NEXTQUARTER, PREVIOUSYEAR, PREVIOUSMONTH, NEXTMONTH.
- Features: date table, time intelligence, calendar-based time intelligence, week-based calendars, relationships, fiscal calendars, row context, fact tables, iterators, moving averages, slicers, totals and subtotals, context transition, DAX queries, data types, filter context, calculated columns, blank handling, external tools, Power Query.

### `t04-time-intelligence-and-dates-2.md` (65 notes)

- Covers: Incomplete periods and future dates; Period-over-period comparisons; Building a Date table.
- DAX functions: CALCULATE, REMOVEFILTERS, MAX, SAMEPERIODLASTYEAR, DATESYTD, LASTNONBLANK, ALLEXCEPT, TODAY, SELECTEDVALUE, YEAR, DIVIDE, DATESBETWEEN, FILTER, SELECTEDMEASURE, KEEPFILTERS, CALENDARAUTO, CALCULATETABLE, IF, ALL, VALUES, EDATE, MONTH, QUARTER, PARALLELPERIOD, TREATAS, ALLNOBLANKROW, USERELATIONSHIP, COUNTROWS, ALLSELECTED, DATESINPERIOD, RANKX, ERROR, IFERROR, SELECTCOLUMNS, DATATABLE, CALENDAR, MIN.
- Features: date table, slicers, calculated columns, time intelligence, external tools, fact tables, calculation groups, relationships, blank handling, charts, calendar-based time intelligence, filter context, auto date/time, DAX queries, visual-level filters, context transition, calculated tables, hierarchies, fiscal calendars, refresh and processing, inactive relationships, error handling.

### `t04-time-intelligence-and-dates-3.md` (46 notes)

- Covers: Date columns, sorting and formats; Blank and placeholder dates; Calendar-based time intelligence.
- DAX functions: DATEADD, DATESINPERIOD, ISBLANK, VALUES, SAMEPERIODLASTYEAR, FORMAT, NOT, SUMX, CALENDARAUTO, BLANK, DATESBETWEEN, FILTER, CALCULATE, REMOVEFILTERS, DATESYTD, NEXTMONTH.
- Features: date table, calendar-based time intelligence, blank handling, time intelligence, charts, format strings, blank row of an invalid relationship, hierarchies, relationships, slicers, fact tables, totals and subtotals, data categories and geography, fiscal calendars, sort by column, TMDL and project files.

## Relationships and filter propagation

### `t05-relationships-1.md` (75 notes)

- Covers: Many-to-many relationships; Virtual relationships in DAX; Bidirectional filters and propagation; Blank row and limited relationships; Inactive relationships and date roles.
- DAX functions: CALCULATE, TREATAS, USERELATIONSHIP, FILTER, ALL, INTERSECT, VALUES, ISEMPTY, CONTAINS, COUNTROWS, SUMMARIZE, CROSSFILTER, AND, IF, NOT, SUMMARIZECOLUMNS, RELATED, ISFILTERED, CALCULATETABLE, ISCROSSFILTERED, CROSSJOIN, INT, OR, RANKX, ALLNOBLANKROW, LOOKUPVALUE.
- Features: relationships, many-to-many, dimension tables, virtual relationships, bidirectional filters, blank handling, cardinality, blank row of an invalid relationship, inactive relationships, bridge tables, limited relationships, date table, slicers, visual-level filters, totals and subtotals, fact tables, calculated columns, storage engine, query plans, external tools, calculated tables, formula engine, error handling, row context.

## Data model design

### `t06-data-model-design-1.md` (71 notes)

- Covers: Dates, time and sort keys; Calculated columns versus measures; Source views, names, data types; Star schema and fact tables.
- DAX functions: SUMX, RELATED, REMOVEFILTERS, VALUES, RANKX, LOOKUPVALUE, SUM, IGNORE, SUMMARIZECOLUMNS.
- Features: calculated columns, dimension tables, fact tables, import mode, star schema, date table, relationships, Power Query, naming, SQL views, data types, memory, slicers, refresh and processing, compression, auto-exist, blank handling, hierarchies, totals and subtotals, sort by column, charts, model size, iterators, DAX queries.

### `t06-data-model-design-2.md` (65 notes)

- Covers: Business-rule grain and testing; Duplicate names, Group By Columns; Circular dependency errors; Sankey chart funnels; User-context calculated columns.
- DAX functions: CALCULATE, SUMMARIZE, ALLEXCEPT, ALLNOBLANKROW, VALUES, SELECTEDVALUE, ALL, SUMX, AVERAGE, FILTER, IF, CALCULATETABLE, UNICHAR, HASONEVALUE, TREATAS, COUNTROWS, USERELATIONSHIP, USERCULTURE, LOOKUPVALUE, MAX, MIN, REMOVEFILTERS, COMBINEVALUES, RANKX, REPT, SUMMARIZECOLUMNS, ADDCOLUMNS, SELECTCOLUMNS, ISFILTERED, USEROBJECTID, USERNAME, USERPRINCIPALNAME, CUSTOMDATA, FALSE.
- Features: calculated columns, relationships, error handling, context transition, blank handling, slicers, charts, iterators, totals and subtotals, calculated tables, Excel and MDX clients, testing and debugging, DAX queries, blank row of an invalid relationship, cardinality, refresh and processing, row-level security, storage engine, CallbackDataID, virtual relationships, memory.

## DAX performance and optimization

### `t07-dax-performance-1.md` (64 notes)

- Covers: Filters, counts and emptiness tests; Measuring and testing performance; Formula and storage engine.
- DAX functions: CALCULATE, ISEMPTY, DISTINCTCOUNT, SUMX, COUNTROWS, FILTER, IF, LASTNONBLANK, CALCULATETABLE, KEEPFILTERS, VALUES, AND, ISBLANK, ALL, BLANK, SUM, NOT, FIRSTNONBLANK, INTERSECT, EXCEPT, SUMMARIZECOLUMNS, SELECTEDVALUE, DIVIDE, AVERAGE, MIN.
- Features: distinct counts, storage engine, DAX queries, fact tables, Performance Analyzer, formula engine, external tools, testing and debugging, query plans, iterators, refresh and processing, filter context, materialization, totals and subtotals, DirectQuery, memory, relationships, AI assistance, cardinality, date table, CallbackDataID, import mode.

### `t07-dax-performance-2.md` (54 notes)

- Covers: Model design, relationships and memory; Server, processing and hardware; Report visuals and Excel clients.
- DAX functions: IF, CALCULATE.
- Features: memory, relationships, refresh and processing, Excel and MDX clients, cardinality, storage engine, compression, fact tables, partitions, VertiPaq, dimension tables, many-to-many, DAX queries, import mode, star schema, query plans, testing and debugging.

### `t07-dax-performance-3.md` (72 notes)

- Covers: Iterators and materialization; Conditional logic and variables; Text search and its index.
- DAX functions: IF, SEARCH, CONTAINSSTRING, SWITCH, CALCULATE, LASTNONBLANKVALUE, LASTNONBLANK, SUMX, SELECTEDVALUE, COUNTROWS, FILTER, SUMMARIZE, RANKX, DATESBETWEEN, LOOKUPVALUE, MAX, SUM, ALL, FIRSTNONBLANK, FIRSTNONBLANKVALUE, CALCULATETABLE, SUMMARIZECOLUMNS, RELATED, NATURALLEFTOUTERJOIN, TREATAS, ROUND, ADDCOLUMNS, OFFSET, ISBLANK, NOT, IF.EAGER, CONTAINSSTRINGEXACT, FIND.
- Features: iterators, storage engine, DAX queries, variables, formula engine, blank handling, slicers, fact tables, CallbackDataID, materialization, cardinality, context transition, filter context, query plans, memory, testing and debugging, totals and subtotals, refresh and processing, dimension tables, row context, calculated columns, ranking, data types.

## Storage engine, model size and memory

### `t08-storage-engine-and-model-size-1.md` (36 notes)

- Covers: Reducing column cardinality; Calculated column and table storage; Measuring model size; Analysis Services processing.
- DAX functions: NOW, SUMX, SUMMARIZE, COUNTROWS, DISTINCTCOUNT, INT, CALCULATETABLE, MOD, CALCULATE, RELATED, LOOKUPVALUE, MONTH, ALL, CROSSJOIN, MAX.
- Features: refresh and processing, memory, dictionaries, calculated columns, VertiPaq, external tools, compression, calculated tables, fact tables, data types, partitions, error handling.

## Storage modes

### `t09-storage-modes-1.md` (63 notes)

- Covers: DirectQuery DAX and limits; DirectQuery model and source design; Choosing a storage mode.
- DAX functions: ADDCOLUMNS, SUMMARIZECOLUMNS, CALCULATE, BLANK, SAMEPERIODLASTYEAR, COMBINEVALUES, MEDIANX, ALL, INT, ISEMPTY, NOT, LASTNONBLANK, LOG10, TRIM, LEN, POWER, LOG, SUBSTITUTE, SECOND, LN, REPLACE, MID, CEILING, SEARCH, LEFT, SUMMARIZE, MAX, REMOVEFILTERS, DATESBETWEEN, DATEADD, DATESYTD.
- Features: DirectQuery, memory, import mode, relationships, formula engine, time intelligence, partitions, calculated columns, external tools, DAX queries, row-level security, refresh and processing, fact tables, storage engine, query plans, VertiPaq, error handling, granularity, materialization, totals and subtotals, detail rows, testing and debugging, blank handling, Excel and MDX clients.

### `t09-storage-modes-2.md` (38 notes)

- Covers: Composite models; Push datasets.
- DAX functions: ALLSELECTED, DISTINCTCOUNT, RELATED, LOOKUPVALUE, SUMX, USERELATIONSHIP, SUM.
- Features: push datasets, composite models, calculation groups, DAX queries, relationships, refresh and processing, DirectQuery, import mode, limited relationships, date table, hierarchies, blank handling.

## Security

### `t10-security-1.md` (48 notes)

- Covers: Dynamic security, relationships and testing; Role filter performance; Totals under row-level security; Object-level security and active roles.
- DAX functions: ALL, USERELATIONSHIP, TREATAS, VALUES, CALCULATETABLE, PATHCONTAINS, LEFT, CROSSFILTER, CALCULATE, ISCROSSFILTERED, SUMMARIZE, FALSE, FILTER, CONCATENATEX, SELECTEDVALUE, CONTAINSSTRING, ERROR, IF.
- Features: row-level security, dimension tables, totals and subtotals, relationships, fact tables, calculated tables, hierarchies, object-level security, storage engine, error handling, dynamic security, inactive relationships, virtual relationships, bidirectional filters, blank handling, DAX queries.

## Calculation groups and field parameters

### `t11-calculation-groups-and-field-parameters-1.md` (82 notes)

- Covers: Calculation group design patterns; Calculation item application; Format string expressions; Calculation group precedence; Per-user defaults and slicers; Field parameters.
- DAX functions: CALCULATE, SELECTEDMEASURE, ISSELECTEDMEASURE, VALUES, IF, SELECTEDMEASURENAME, USERPRINCIPALNAME, ISCROSSFILTERED, SWITCH, SELECTEDMEASUREFORMATSTRING, ALLSELECTED, FALSE, SELECTEDVALUE, CALCULATETABLE, TRUE, INT, MAX, TREATAS, SELECTCOLUMNS, HASONEVALUE, NATURALLEFTOUTERJOIN, ADDCOLUMNS, DATATABLE, SUMX, USERELATIONSHIP, DATESBETWEEN, SAMEPERIODLASTYEAR, DATESYTD, ALL, FILTER, CONCATENATEX, NAMEOF.
- Features: calculation groups, slicers, format strings, field parameters, DAX queries, dynamic format strings, parameter tables, relationships, totals and subtotals, bidirectional filters, bridge tables, error handling, calculated tables, filter context, formula engine, DAX formatting, conditional formatting, many-to-many, time intelligence, naming, SVG and custom visuals, testing and debugging, row-level security, visual-level filters.

### `t11-calculation-groups-and-field-parameters-2.md` (10 notes)

- Covers: Selection expressions.
- DAX functions: ERROR, ISCROSSFILTERED.
- Features: calculation groups, slicers, currency conversion, error handling, format strings, data categories and geography, naming, dynamic format strings, totals and subtotals.

## Window functions and visual calculations

### `t12-window-functions-and-visual-calculations-1.md` (79 notes)

- Covers: Measure or visual calculation; Window functions and apply semantics; Ranking with RANK and RANKX; Visual context and virtual table; Running totals and performance.
- DAX functions: RANK, OFFSET, RANKX, WINDOW, INDEX, ORDERBY, CALCULATE, ALL, ALLSELECTED, ISINSCOPE, VALUES, HASONEVALUE, FILTER, AVERAGEX, PARTITIONBY, BLANK, SUMMARIZECOLUMNS, DISTINCTCOUNT, RUNNINGSUM, SELECTEDVALUE, MATCHBY, IF, FORMAT, MAX, SUMX, SWITCH, ALLEXCEPT, CROSSJOIN, ADDCOLUMNS, MINX, CALCULATETABLE.
- Features: visual calculations, ranking, totals and subtotals, window functions, hierarchies, DAX queries, running totals, matrix visual, filter context, iterators, DAX formatting, partitions, blank handling, distinct counts, granularity, slicers, conditional formatting, moving averages, row context, variables, fact tables, storage engine, relationships, sort by column.

## User-defined functions in DAX

### `t13-user-defined-functions-1.md` (49 notes)

- Covers: Naming and model-independent functions; Functions, measures and calculation groups; Parameters, types and passing modes; Calendar filters and result checks.
- DAX functions: CALCULATE, REMOVEFILTERS, TABLEOF, SUMX, ISBLANK, BLANK, SUM, ISFILTERED, ISCROSSFILTERED, AVERAGEX, FILTER, IF, NAMEOF, ERROR, MAX, DATESINPERIOD, RANGE.
- Features: user-defined functions, calendar-based time intelligence, calculation groups, iterators, DAX queries, row context, testing and debugging, naming, context transition, error handling, filter context, data types, blank handling, visual calculations.

## Business calculation patterns

### `t14-business-calculation-patterns-1.md` (55 notes)

- Covers: Totals and hierarchy levels; Budget, currency and financial calculations.
- DAX functions: CALCULATE, VALUES, ALL, ALLEXCEPT, SUMX, CONTAINS, FILTER, ISFILTERED, KEEPFILTERS, SUMMARIZE, IF, COUNTROWS, SUM, MAX, DIVIDE, DATESYTD, PRODUCTX.
- Features: totals and subtotals, iterators, budget and forecast, fact tables, relationships, hierarchies, blank handling, currency conversion, filter context, date table, granularity, DAX queries, slicers, context transition, virtual relationships, charts, snapshot tables, error handling, calculation groups.

### `t14-business-calculation-patterns-2.md` (49 notes)

- Covers: Customer, product and campaign analysis.
- DAX functions: CALCULATE, REMOVEFILTERS, VALUES, ISBLANK, FILTER, CALCULATETABLE, MIN, SUMMARIZE, CROSSFILTER, RELATED, SUMX, GENERATE, EXCEPT, ALLSELECTED, SWITCH, WINDOW, ISINSCOPE, DATEADD, DATESINPERIOD, AVERAGE, GENERATEALL, SELECTCOLUMNS, ALL, COUNTROWS, CONTAINS, ADDCOLUMNS, INTERSECT, UNION, DATESBETWEEN, BLANK, ERROR, PARTITIONBY, KEEPFILTERS, DIVIDE, RELATEDTABLE, ISEMPTY.
- Features: fact tables, charts, blank handling, dimension tables, bridge tables, calculated tables, totals and subtotals, calculated columns, ABC and segmentation, DAX queries, slicers, relationships, tooltips, blank row of an invalid relationship, running totals, refresh and processing, error handling, matrix visual, variables, visual calculations.

### `t14-business-calculation-patterns-3.md` (48 notes)

- Covers: Semi-additive and running totals; Building and testing calculations.
- DAX functions: CALCULATE, MAX, LASTDATE, ALL, LASTNONBLANK, SUMX, FILTER, FIRSTNONBLANK, SUM, VALUES, COUNTROWS, GROUPBY, ENDOFMONTH, OPENINGBALANCEQUARTER, CLOSINGBALANCEMONTH, ENDOFQUARTER, STARTOFYEAR, CLOSINGBALANCEQUARTER, STARTOFMONTH, OPENINGBALANCEYEAR, STARTOFQUARTER, OPENINGBALANCEMONTH, ENDOFYEAR, CLOSINGBALANCEYEAR, TREATAS, ISCROSSFILTERED, FIRSTDATE, CURRENTGROUP, IF, DATEADD, YEAR, QUARTER, PARALLELPERIOD, ADDCOLUMNS, CALCULATETABLE, DATESYTD, SELECTEDVALUE, TRUE, REMOVEFILTERS, ALLNOBLANKROW, TOPN.
- Features: snapshot tables, totals and subtotals, semi-additive measures, dimension tables, DAX queries, variables, filter context, iterators, blank handling, memory, running totals, date table, cardinality, relationships, context transition, calculated tables, testing and debugging, AI assistance.

### `t14-business-calculation-patterns-4.md` (56 notes)

- Covers: Ranking and top N.
- DAX functions: RANKX, ALLSELECTED, CALCULATE, TOPN, ISINSCOPE, ALL, GENERATE, VALUES, HASONEVALUE, KEEPFILTERS, MINX, FILTER, REMOVEFILTERS, FIRSTNONBLANK, SELECTEDVALUE, CONCATENATEX, CALCULATETABLE, ALLNOBLANKROW, MAX, GROUPBY.
- Features: ranking, visual-level filters, matrix visual, totals and subtotals, iterators, sort by column, variables, blank handling, DAX queries, calculated columns, calculated tables, filter context, context transition, charts, slicers, relationships, DAX formatting.

### `t14-business-calculation-patterns-5.md` (49 notes)

- Covers: Events, durations and sequences; Averages, working days and trends.
- DAX functions: COUNTROWS, AVERAGEX, LINESTX, ALLEXCEPT, FILTER, CALCULATE, SELECTCOLUMNS, DIVIDE, LINEST, CALCULATETABLE, VALUES, TRUE, FALSE, MIN, IF, ALL, ALLNOBLANKROW, GENERATE, SUM, HASONEVALUE, NETWORKDAYS, RANKX, ADDCOLUMNS, KEEPFILTERS, ISBLANK, COALESCE, REMOVEFILTERS.
- Features: date table, calculated columns, moving averages, dimension tables, blank handling, DAX queries, calendar-based time intelligence, charts, relationships, fact tables, iterators, totals and subtotals, variables, context transition, calculated tables, running totals, slicers.

## Tooling, workflow and AI assistance

### `t16-tooling-and-workflow-1.md` (47 notes)

- Covers: Scripting with TOM and APIs; Choosing development tools; Translations and renaming objects.
- DAX functions: DB.
- Features: external tools, translations, Excel and MDX clients, refresh and processing, DAX queries, incremental refresh, VertiPaq, naming, partitions, testing and debugging.

### `t16-tooling-and-workflow-2.md` (48 notes)

- Covers: Model edits with external tools; Query tracing and debugging.
- DAX functions: TOJSON, TOCSV, ALLSELECTED, EVALUATEANDLOG, CONCATENATEX, CALCULATETABLE, TOPN, FORMAT, SUMMARIZECOLUMNS.
- Features: external tools, testing and debugging, DAX queries, variables, KPIs, slicers, refresh and processing, Performance Analyzer, filter context, shadow filter context, DAX formatting, format strings.

### `t16-tooling-and-workflow-3.md` (62 notes)

- Covers: Reusable libraries and templates; AI assistants and agents; Testing measures.
- DAX functions: CALCULATE, RANK, UNION, EVALUATE, COALESCE, TREATAS.
- Features: AI assistance, testing and debugging, DAX queries, report themes, user-defined functions, TMDL and project files, error handling, DAX formatting, ranking, documentation and descriptions, filter context, date table, external tools, totals and subtotals, dimension tables, blank handling.
