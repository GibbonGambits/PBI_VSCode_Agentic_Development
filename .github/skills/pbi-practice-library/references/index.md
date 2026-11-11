# Practice library: index

Read this file first, then open only the file that fits the task. Never read the whole library for one task.

Each entry names one file in this folder, what it covers, and the DAX functions and Power BI features its notes mention (most frequent first). A function or feature can appear in several files: pick the file whose topic fits the question. How to use a note is set out in the skill file one folder up.

| Topic | Files | Notes |
|---|---|---:|
| DAX evaluation context | `t01-evaluation-context-1.md` to `t01-evaluation-context-3.md` | 165 |
| DAX authoring style | `t02-dax-authoring-style-1.md` to `t02-dax-authoring-style-2.md` | 123 |
| DAX table functions and queries | `t03-table-functions-and-queries-1.md` to `t03-table-functions-and-queries-2.md` | 159 |
| Time intelligence and date tables | `t04-time-intelligence-and-dates-1.md` to `t04-time-intelligence-and-dates-3.md` | 172 |
| Relationships and filter propagation | `t05-relationships-1.md` | 75 |
| Data model design | `t06-data-model-design-1.md` to `t06-data-model-design-2.md` | 136 |
| DAX performance and optimization | `t07-dax-performance-1.md` to `t07-dax-performance-3.md` | 190 |
| Storage engine, model size and memory | `t08-storage-engine-and-model-size-1.md` | 36 |
| Storage modes | `t09-storage-modes-1.md` to `t09-storage-modes-2.md` | 101 |
| Security | `t10-security-1.md` | 48 |

## DAX evaluation context

### `t01-evaluation-context-1.md` (68 notes)

- Covers: KEEPFILTERS and arbitrary filters; CALCULATE filter arguments; Visual queries and auto-exist; Reading the selected value.
- DAX functions: CALCULATE, KEEPFILTERS, FILTER, ALL, VALUES, CALCULATETABLE, SELECTEDVALUE, CROSSJOIN, SUMMARIZE, HASONEVALUE, ISINSCOPE, IF, TRUE, SUMMARIZECOLUMNS, OR, ISFILTERED, LASTDATE, AND, RELATED, RANKX, AVERAGEX, REMOVEFILTERS, MAX, CONTAINS, CROSSFILTER, ERROR, COUNTROWS, SELECTCOLUMNS, FALSE.
- Features: measures, iterators, DAX queries, filter context, slicers, auto-exist, naming, testing and debugging, cardinality, totals and subtotals, error handling, context transition, variables, Excel and MDX clients, storage engine, sort by column, dimension tables, relationships, blank handling, expanded tables, running totals, hierarchies, parameter tables, matrix visual.

### `t01-evaluation-context-2.md` (79 notes)

- Covers: Row context and iterators; Relationships, expanded tables and lineage; Context transition; Removing filters with ALL.
- DAX functions: CALCULATE, ALL, VALUES, RELATED, CALCULATETABLE, SUMX, ALLEXCEPT, REMOVEFILTERS, RELATEDTABLE, FILTER, SUM, USERELATIONSHIP, MAX, SUMMARIZE, ALLCROSSFILTERED, SELECTEDVALUE, TREATAS, ADDCOLUMNS, MIN, SELECTCOLUMNS, LASTDATE, AVERAGE, MINX, MAXX, AVERAGEX, COUNTROWS, LOOKUPVALUE, SAMEPERIODLASTYEAR, SUMMARIZECOLUMNS.
- Features: iterators, row context, relationships, calculated columns, context transition, measures, filter context, dimension tables, fact tables, totals and subtotals, DAX queries, error handling, inactive relationships, slicers, expanded tables, limited relationships, data lineage, blank row of an invalid relationship, blank handling, bidirectional filters, variables, aggregations, budget and forecast, naming, virtual relationships, time intelligence, cardinality, DirectQuery.

### `t01-evaluation-context-3.md` (18 notes)

- Covers: ALLSELECTED and shadow filters; Totals and additivity.
- DAX functions: ALLSELECTED, VALUES, CALCULATE, SUMX, DISTINCTCOUNT, AVERAGEX, IF, EARLIER, ALL, MAXX, MINX, SUMMARIZECOLUMNS.
- Features: iterators, filter context, shadow filter context, measures, totals and subtotals, DAX queries, variables, matrix visual.

## DAX authoring style

### `t02-dax-authoring-style-1.md` (75 notes)

- Covers: Formatting, naming and references; Variables and their evaluation; BLANK handling and conditions.
- DAX functions: IF, BLANK, SWITCH, DIVIDE, SUMX, ADDCOLUMNS, ISBLANK, CALCULATE, VALUES, COALESCE, VAR, FILTER, TOPN, AVERAGEX, NOT, FALSE, COUNTROWS, MINX, SUM, RELATED, ALL, CALCULATETABLE, VALUE, TREATAS, CONCATENATEX, RELATEDTABLE, ERROR, MAXX.
- Features: variables, measures, blank handling, naming, iterators, testing and debugging, error handling, DAX queries, filter context, relationships, blank row of an invalid relationship, row context, aggregations, data types, DAX formatting, calculated columns, calculated tables, data lineage, totals and subtotals, translations.

### `t02-dax-authoring-style-2.md` (48 notes)

- Covers: IN operator and constructors; Data types and comparisons.
- DAX functions: CALCULATE, NOT, ALL, FILTER, OR, CONTAINSROW, INT, CONVERT, CONTAINS, TREATAS, SUMMARIZE, CALCULATETABLE, SUMX, VALUES, EXCEPT, AND, INTERSECT, ISEMPTY, DIVIDE, LOWER, UNION.
- Features: testing and debugging, data types, error handling, iterators, fact tables, currency conversion, measures, virtual relationships, naming, DAX formatting, conditional formatting, totals and subtotals.

## DAX table functions and queries

### `t03-table-functions-and-queries-1.md` (81 notes)

- Covers: Grouping and adding columns; Writing DAX queries; Filter and text conditions.
- DAX functions: SUMMARIZE, ADDCOLUMNS, CALCULATE, GROUPBY, CALCULATETABLE, FILTER, CURRENTGROUP, SEARCH, DEFINE, SELECTCOLUMNS, EVALUATE, CONTAINSSTRING, ISEMPTY, MAXX, DETAILROWS, VALUES, GENERATE, CONTAINS, ROW, LEFT, OR, ALL, FIND, AND, ROLLUP, SUM, COUNTROWS, NOT, DATATABLE, TREATAS, KEEPFILTERS, REMOVEFILTERS, MAX, BLANK, CROSSJOIN, ALLEXCEPT, CONTAINSSTRINGEXACT, SUBSTITUTE, RIGHT, IFERROR, RELATEDTABLE.
- Features: DAX queries, aggregations, iterators, testing and debugging, measures, variables, relationships, filter context, Excel and MDX clients, totals and subtotals, blank handling, translations, row context, context transition, fact tables, materialization, query plans, naming, slicers, expanded tables, dimension tables, formula engine, SQL views, blank row of an invalid relationship, external tools, detail rows.

### `t03-table-functions-and-queries-2.md` (78 notes)

- Covers: Calculated and static tables; SUMMARIZECOLUMNS behaviour; Joins and lookups; Set functions.
- DAX functions: SUMMARIZECOLUMNS, LOOKUPVALUE, SUMMARIZE, NATURALLEFTOUTERJOIN, NATURALINNERJOIN, ADDCOLUMNS, UNION, TREATAS, INTERSECT, EXCEPT, VALUES, RELATED, CROSSJOIN, GENERATE, SELECTCOLUMNS, CALCULATE, GENERATESERIES, FILTER, CONTAINS, ROW, CALCULATETABLE, SELECTEDVALUE, DATATABLE, RELATEDTABLE, CURRENCY, CALENDAR, IF, HASONEVALUE, GENERATEALL, CONVERT, ALL, ISBLANK, REMOVEFILTERS, COALESCE, NOT.
- Features: relationships, measures, data lineage, virtual relationships, naming, fact tables, error handling, calculated tables, DAX queries, blank handling, variables, data types, query plans, storage engine, aggregations, testing and debugging, iterators, row context, filter context, expanded tables, limited relationships, auto-exist, calculated columns, currency conversion, compression, parameter tables, blank row of an invalid relationship.

## Time intelligence and date tables

### `t04-time-intelligence-and-dates-1.md` (78 notes)

- Covers: Time intelligence functions; Week-based and fiscal calendars; Mark as date table; Incomplete periods and future dates.
- DAX functions: CALCULATE, DATEADD, SAMEPERIODLASTYEAR, DATESYTD, LASTDATE, REMOVEFILTERS, VALUES, FILTER, ALL, CALCULATETABLE, MAX, PARALLELPERIOD, ALLEXCEPT, FIRSTDATE, DATESBETWEEN, DATESINPERIOD, TOTALYTD, CONTAINS, LASTNONBLANK, PREVIOUSDAY, NEXTDAY, KEEPFILTERS, FILTERS, AVERAGEX, SELECTEDMEASURE, YEAR, QUARTER, MONTH, TODAY, MIN, IF, COUNTROWS, WEEKDAY, DAY, PREVIOUSYEAR, NEXTMONTH, NEXTQUARTER, PREVIOUSMONTH, PREVIOUSQUARTER, NEXTYEAR, DIVIDE, EDATE, TREATAS.
- Features: date table, measures, time intelligence, calendar-based time intelligence, week-based calendars, relationships, calculated columns, fact tables, blank handling, fiscal calendars, row context, DAX queries, slicers, filter context, iterators, moving averages, calculation groups, context transition, totals and subtotals, data types, external tools, Power Query.

### `t04-time-intelligence-and-dates-2.md` (76 notes)

- Covers: Period-over-period comparisons; Building a Date table; Date columns, sorting and formats; Blank and placeholder dates.
- DAX functions: CALCULATE, REMOVEFILTERS, SELECTEDVALUE, MAX, CALENDARAUTO, YEAR, ISBLANK, KEEPFILTERS, DATESINPERIOD, ALLEXCEPT, FORMAT, NOT, SUMX, VALUES, ALLNOBLANKROW, USERELATIONSHIP, DIVIDE, COUNTROWS, ALLSELECTED, SELECTEDMEASURE, RANKX, IFERROR, ERROR, SELECTCOLUMNS, TODAY, DATATABLE, CALENDAR, FILTER, MIN, BLANK, DATESBETWEEN.
- Features: date table, slicers, charts, blank handling, measures, relationships, fact tables, naming, format strings, external tools, hierarchies, blank row of an invalid relationship, calendar-based time intelligence, calculated columns, fiscal calendars, auto date/time, time intelligence, totals and subtotals, inactive relationships, sort by column, calculation groups, visual-level filters, calculated tables, testing and debugging, error handling, SQL views.

### `t04-time-intelligence-and-dates-3.md` (18 notes)

- Covers: Calendar-based time intelligence.
- DAX functions: DATEADD, DATESINPERIOD, SAMEPERIODLASTYEAR, CALCULATE, FILTER, VALUES, REMOVEFILTERS, NEXTMONTH, DATESYTD.
- Features: calendar-based time intelligence, time intelligence, date table, data categories and geography, naming, hierarchies, measures.

## Relationships and filter propagation

### `t05-relationships-1.md` (75 notes)

- Covers: Many-to-many relationships; Virtual relationships in DAX; Bidirectional filters and propagation; Blank row and limited relationships; Inactive relationships and date roles.
- DAX functions: CALCULATE, TREATAS, USERELATIONSHIP, FILTER, ALL, INTERSECT, VALUES, ISEMPTY, CONTAINS, SUMMARIZE, COUNTROWS, CROSSFILTER, AND, IF, NOT, SUMMARIZECOLUMNS, RELATED, ISFILTERED, CALCULATETABLE, ISCROSSFILTERED, CROSSJOIN, INT, OR, RANKX, ALLNOBLANKROW, LOOKUPVALUE.
- Features: relationships, measures, many-to-many, dimension tables, virtual relationships, bidirectional filters, blank handling, cardinality, blank row of an invalid relationship, inactive relationships, bridge tables, limited relationships, date table, slicers, visual-level filters, testing and debugging, totals and subtotals, fact tables, calculated columns, storage engine, query plans, external tools, import mode, calculated tables, formula engine, error handling, row context, charts.

## Data model design

### `t06-data-model-design-1.md` (71 notes)

- Covers: Dates, time and sort keys; Calculated columns versus measures; Source views, names, data types; Star schema and fact tables.
- DAX functions: SUMX, RELATED, REMOVEFILTERS, VALUES, RANKX, LOOKUPVALUE, SUM, IGNORE, SUMMARIZECOLUMNS.
- Features: import mode, calculated columns, naming, measures, dimension tables, fact tables, star schema, date table, SQL views, relationships, Power Query, data types, memory, slicers, refresh and processing, compression, auto-exist, blank handling, testing and debugging, hierarchies, aggregations, totals and subtotals, sort by column, charts, model size, iterators, DAX queries, data categories and geography, dictionaries, error handling, ranking, VertiPaq, ABC and segmentation, partitions.

### `t06-data-model-design-2.md` (65 notes)

- Covers: Business-rule grain and testing; Duplicate names, Group By Columns; Circular dependency errors; Sankey chart funnels; User-context calculated columns.
- DAX functions: CALCULATE, SUMMARIZE, ALLEXCEPT, ALLNOBLANKROW, VALUES, ALL, SELECTEDVALUE, SUMX, AVERAGE, FILTER, IF, UNICHAR, CALCULATETABLE, HASONEVALUE, TREATAS, COUNTROWS, USERELATIONSHIP, USERCULTURE, LOOKUPVALUE, MAX, MIN, REMOVEFILTERS, COMBINEVALUES, REPT, RANKX, SUMMARIZECOLUMNS, ADDCOLUMNS, SELECTCOLUMNS, ISFILTERED, USERNAME, USEROBJECTID, USERPRINCIPALNAME, CUSTOMDATA, FALSE.
- Features: calculated columns, measures, relationships, naming, error handling, context transition, blank handling, slicers, charts, testing and debugging, iterators, totals and subtotals, calculated tables, Excel and MDX clients, DAX queries, blank row of an invalid relationship, cardinality, translations, refresh and processing, row-level security, storage engine, CallbackDataID, virtual relationships, memory.

## DAX performance and optimization

### `t07-dax-performance-1.md` (64 notes)

- Covers: Filters, counts and emptiness tests; Measuring and testing performance; Formula and storage engine.
- DAX functions: CALCULATE, ISEMPTY, DISTINCTCOUNT, SUMX, COUNTROWS, FILTER, IF, LASTNONBLANK, CALCULATETABLE, KEEPFILTERS, VALUES, AND, ISBLANK, ALL, BLANK, SUM, NOT, FIRSTNONBLANK, INTERSECT, SUMMARIZECOLUMNS, EXCEPT, SELECTEDVALUE, DIVIDE, MIN, AVERAGE.
- Features: measures, testing and debugging, distinct counts, storage engine, DAX queries, fact tables, Performance Analyzer, formula engine, external tools, query plans, iterators, refresh and processing, filter context, materialization, naming, totals and subtotals, aggregations, DirectQuery, memory, relationships, AI assistance, cardinality, date table, CallbackDataID.

### `t07-dax-performance-2.md` (54 notes)

- Covers: Model design, relationships and memory; Server, processing and hardware; Report visuals and Excel clients.
- DAX functions: IF, CALCULATE.
- Features: memory, relationships, testing and debugging, measures, refresh and processing, Excel and MDX clients, cardinality, storage engine, compression, fact tables, partitions, VertiPaq, dimension tables, many-to-many, DAX queries, star schema, query plans.

### `t07-dax-performance-3.md` (72 notes)

- Covers: Iterators and materialization; Conditional logic and variables; Text search and its index.
- DAX functions: IF, SEARCH, CONTAINSSTRING, SWITCH, CALCULATE, LASTNONBLANKVALUE, LASTNONBLANK, SUMX, SELECTEDVALUE, COUNTROWS, FILTER, SUMMARIZE, RANKX, DATESBETWEEN, LOOKUPVALUE, MAX, SUM, ALL, FIRSTNONBLANK, FIRSTNONBLANKVALUE, CALCULATETABLE, SUMMARIZECOLUMNS, RELATED, NATURALLEFTOUTERJOIN, TREATAS, ROUND, ADDCOLUMNS, OFFSET, NOT, ISBLANK, IF.EAGER, FIND, CONTAINSSTRINGEXACT.
- Features: measures, iterators, storage engine, DAX queries, testing and debugging, variables, formula engine, blank handling, slicers, fact tables, CallbackDataID, materialization, cardinality, context transition, filter context, query plans, memory, totals and subtotals, naming, refresh and processing, dimension tables, row context, calculated columns, ranking, data types, aggregations.

## Storage engine, model size and memory

### `t08-storage-engine-and-model-size-1.md` (36 notes)

- Covers: Reducing column cardinality; Calculated column and table storage; Measuring model size; Analysis Services processing.
- DAX functions: NOW, SUMX, SUMMARIZE, COUNTROWS, DISTINCTCOUNT, CALCULATETABLE, MOD, INT, CALCULATE, LOOKUPVALUE, RELATED, MONTH, ALL, CROSSJOIN, MAX.
- Features: refresh and processing, import mode, memory, dictionaries, calculated columns, VertiPaq, external tools, measures, compression, calculated tables, fact tables, data types, partitions, error handling.

## Storage modes

### `t09-storage-modes-1.md` (63 notes)

- Covers: DirectQuery DAX and limits; DirectQuery model and source design; Choosing a storage mode.
- DAX functions: SUMMARIZECOLUMNS, ADDCOLUMNS, CALCULATE, BLANK, SAMEPERIODLASTYEAR, COMBINEVALUES, MEDIANX, ALL, INT, LASTNONBLANK, ISEMPTY, NOT, LOG, LEFT, LOG10, SECOND, SEARCH, MID, TRIM, SUBSTITUTE, LN, CEILING, LEN, POWER, REPLACE, SUMMARIZE, REMOVEFILTERS, MAX, DATEADD, DATESBETWEEN, DATESYTD.
- Features: DirectQuery, memory, relationships, measures, formula engine, time intelligence, partitions, testing and debugging, calculated columns, import mode, external tools, DAX queries, SQL views, row-level security, refresh and processing, fact tables, storage engine, query plans, VertiPaq, error handling, granularity, materialization, totals and subtotals, detail rows, blank handling, Excel and MDX clients, naming.

### `t09-storage-modes-2.md` (38 notes)

- Covers: Composite models; Push datasets.
- DAX functions: ALLSELECTED, DISTINCTCOUNT, RELATED, LOOKUPVALUE, SUMX, USERELATIONSHIP, SUM.
- Features: push datasets, composite models, measures, calculation groups, DAX queries, relationships, refresh and processing, DirectQuery, testing and debugging, import mode, limited relationships, date table, hierarchies, naming, blank handling.

## Security

### `t10-security-1.md` (48 notes)

- Covers: Dynamic security, relationships and testing; Role filter performance; Totals under row-level security; Object-level security and active roles.
- DAX functions: ALL, USERELATIONSHIP, TREATAS, VALUES, CALCULATETABLE, PATHCONTAINS, LEFT, CROSSFILTER, CALCULATE, ISCROSSFILTERED, SUMMARIZE, FILTER, FALSE, SELECTEDVALUE, CONCATENATEX, CONTAINSSTRING, IF, ERROR.
- Features: row-level security, measures, dimension tables, totals and subtotals, relationships, naming, fact tables, calculated tables, testing and debugging, hierarchies, object-level security, storage engine, error handling, dynamic security, inactive relationships, virtual relationships, bidirectional filters, blank handling, DAX queries.
