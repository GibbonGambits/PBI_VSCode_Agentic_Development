# Practice library: index

Read this file first, then open only the file that fits the task. Never read the whole library for one task.

Each entry names one file in this folder, what it covers, and the DAX functions and Power BI features its notes mention (most frequent first). A function or feature can appear in several files: pick the file whose topic fits the question. How to use a note is set out in the skill file one folder up.

| Topic | Files | Notes |
|---|---|---:|
| DAX evaluation context | `t01-evaluation-context-1.md` to `t01-evaluation-context-3.md` | 165 |
| DAX authoring style | `t02-dax-authoring-style-1.md` to `t02-dax-authoring-style-2.md` | 123 |
| DAX table functions and queries | `t03-table-functions-and-queries-1.md` to `t03-table-functions-and-queries-2.md` | 159 |
| Relationships and filter propagation | `t05-relationships-1.md` | 75 |

## DAX evaluation context

### `t01-evaluation-context-1.md` (68 notes)

- Covers: KEEPFILTERS and arbitrary filters; CALCULATE filter arguments; Visual queries and auto-exist; Reading the selected value.
- DAX functions: CALCULATE, KEEPFILTERS, FILTER, ALL, VALUES, CALCULATETABLE, SELECTEDVALUE, CROSSJOIN, SUMMARIZE, HASONEVALUE, ISINSCOPE, IF, TRUE, SUMMARIZECOLUMNS, OR, ISFILTERED, LASTDATE, AND, RELATED, RANKX, AVERAGEX, REMOVEFILTERS, MAX, CONTAINS, CROSSFILTER, ERROR, COUNTROWS, SELECTCOLUMNS, FALSE.
- Features: measures, iterators, DAX queries, filter context, slicers, auto-exist, naming, testing and debugging, cardinality, totals and subtotals, error handling, context transition, variables, Excel and MDX clients, storage engine, sort by column, dimension tables, relationships, blank handling, expanded tables, running totals, hierarchies, parameter tables, matrix visual.

### `t01-evaluation-context-2.md` (79 notes)

- Covers: Row context and iterators; Relationships, expanded tables and lineage; Context transition; Removing filters with ALL.
- DAX functions: CALCULATE, ALL, VALUES, RELATED, CALCULATETABLE, SUMX, ALLEXCEPT, REMOVEFILTERS, RELATEDTABLE, FILTER, SUM, USERELATIONSHIP, MAX, SUMMARIZE, ALLCROSSFILTERED, SELECTEDVALUE, TREATAS, ADDCOLUMNS, MIN, SELECTCOLUMNS, LASTDATE, AVERAGE, AVERAGEX, MAXX, MINX, COUNTROWS, LOOKUPVALUE, SAMEPERIODLASTYEAR, SUMMARIZECOLUMNS.
- Features: iterators, row context, relationships, calculated columns, context transition, measures, filter context, dimension tables, fact tables, totals and subtotals, DAX queries, error handling, inactive relationships, slicers, expanded tables, limited relationships, data lineage, blank row of an invalid relationship, blank handling, bidirectional filters, variables, aggregations, budget and forecast, naming, virtual relationships, time intelligence, cardinality, DirectQuery.

### `t01-evaluation-context-3.md` (18 notes)

- Covers: ALLSELECTED and shadow filters; Totals and additivity.
- DAX functions: ALLSELECTED, VALUES, CALCULATE, SUMX, DISTINCTCOUNT, AVERAGEX, IF, EARLIER, ALL, MINX, MAXX, SUMMARIZECOLUMNS.
- Features: iterators, filter context, shadow filter context, measures, totals and subtotals, DAX queries, variables, matrix visual.

## DAX authoring style

### `t02-dax-authoring-style-1.md` (75 notes)

- Covers: Formatting, naming and references; Variables and their evaluation; BLANK handling and conditions.
- DAX functions: IF, BLANK, SWITCH, DIVIDE, SUMX, ADDCOLUMNS, ISBLANK, CALCULATE, VALUES, COALESCE, VAR, FILTER, TOPN, AVERAGEX, NOT, FALSE, COUNTROWS, MINX, SUM, RELATED, ALL, CALCULATETABLE, VALUE, TREATAS, CONCATENATEX, RELATEDTABLE, ERROR, MAXX.
- Features: variables, measures, blank handling, naming, iterators, testing and debugging, error handling, DAX queries, filter context, relationships, blank row of an invalid relationship, row context, aggregations, data types, DAX formatting, calculated columns, calculated tables, data lineage, totals and subtotals, translations.

### `t02-dax-authoring-style-2.md` (48 notes)

- Covers: IN operator and constructors; Data types and comparisons.
- DAX functions: CALCULATE, NOT, ALL, FILTER, OR, CONTAINSROW, INT, CONVERT, CONTAINS, TREATAS, SUMMARIZE, CALCULATETABLE, SUMX, EXCEPT, VALUES, AND, ISEMPTY, INTERSECT, DIVIDE, UNION, LOWER.
- Features: testing and debugging, data types, error handling, iterators, fact tables, currency conversion, measures, virtual relationships, naming, DAX formatting, conditional formatting, totals and subtotals.

## DAX table functions and queries

### `t03-table-functions-and-queries-1.md` (81 notes)

- Covers: Grouping and adding columns; Writing DAX queries; Filter and text conditions.
- DAX functions: SUMMARIZE, ADDCOLUMNS, CALCULATE, GROUPBY, CALCULATETABLE, FILTER, CURRENTGROUP, SEARCH, DEFINE, SELECTCOLUMNS, EVALUATE, CONTAINSSTRING, ISEMPTY, MAXX, DETAILROWS, VALUES, GENERATE, CONTAINS, ROW, LEFT, OR, ALL, FIND, AND, ROLLUP, SUM, COUNTROWS, NOT, DATATABLE, TREATAS, KEEPFILTERS, REMOVEFILTERS, MAX, BLANK, CROSSJOIN, ALLEXCEPT, CONTAINSSTRINGEXACT, SUBSTITUTE, IFERROR, RIGHT, RELATEDTABLE.
- Features: DAX queries, aggregations, iterators, testing and debugging, measures, variables, relationships, filter context, Excel and MDX clients, totals and subtotals, blank handling, translations, row context, context transition, fact tables, materialization, query plans, naming, slicers, expanded tables, dimension tables, formula engine, SQL views, blank row of an invalid relationship, external tools, detail rows.

### `t03-table-functions-and-queries-2.md` (78 notes)

- Covers: Calculated and static tables; SUMMARIZECOLUMNS behaviour; Joins and lookups; Set functions.
- DAX functions: SUMMARIZECOLUMNS, LOOKUPVALUE, SUMMARIZE, NATURALLEFTOUTERJOIN, NATURALINNERJOIN, ADDCOLUMNS, UNION, TREATAS, EXCEPT, INTERSECT, VALUES, RELATED, CROSSJOIN, SELECTCOLUMNS, GENERATE, CALCULATE, GENERATESERIES, FILTER, CONTAINS, ROW, CALCULATETABLE, SELECTEDVALUE, DATATABLE, RELATEDTABLE, CURRENCY, CALENDAR, IF, HASONEVALUE, GENERATEALL, CONVERT, ISBLANK, ALL, REMOVEFILTERS, COALESCE, NOT.
- Features: relationships, measures, data lineage, virtual relationships, naming, fact tables, error handling, calculated tables, DAX queries, blank handling, variables, data types, query plans, storage engine, aggregations, testing and debugging, iterators, row context, filter context, expanded tables, limited relationships, auto-exist, calculated columns, currency conversion, compression, parameter tables, blank row of an invalid relationship.

## Relationships and filter propagation

### `t05-relationships-1.md` (75 notes)

- Covers: Many-to-many relationships; Virtual relationships in DAX; Bidirectional filters and propagation; Blank row and limited relationships; Inactive relationships and date roles.
- DAX functions: CALCULATE, TREATAS, USERELATIONSHIP, FILTER, ALL, INTERSECT, VALUES, ISEMPTY, CONTAINS, SUMMARIZE, COUNTROWS, CROSSFILTER, AND, IF, NOT, SUMMARIZECOLUMNS, RELATED, ISFILTERED, CALCULATETABLE, ISCROSSFILTERED, CROSSJOIN, INT, OR, RANKX, ALLNOBLANKROW, LOOKUPVALUE.
- Features: relationships, measures, many-to-many, dimension tables, virtual relationships, bidirectional filters, blank handling, cardinality, blank row of an invalid relationship, inactive relationships, bridge tables, limited relationships, date table, slicers, visual-level filters, testing and debugging, totals and subtotals, fact tables, calculated columns, storage engine, query plans, external tools, import mode, calculated tables, formula engine, error handling, row context, charts.
