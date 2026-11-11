# Practice library: index

Read this file first, then open only the file that fits the task. Never read the whole library for one task.

Each entry names one file in this folder, what it covers, and the DAX functions and Power BI features its notes mention (most frequent first). A function or feature can appear in several files: pick the file whose topic fits the question. How to use a note is set out in the skill file one folder up.

| Topic | Files | Notes |
|---|---|---:|
| DAX authoring style | `t02-dax-authoring-style-1.md` to `t02-dax-authoring-style-2.md` | 123 |
| DAX table functions and queries | `t03-table-functions-and-queries-1.md` to `t03-table-functions-and-queries-2.md` | 159 |

## DAX authoring style

### `t02-dax-authoring-style-1.md` (75 notes)

- Covers: Formatting, naming and references; Variables and their evaluation; BLANK handling and conditions.
- DAX functions: IF, BLANK, SWITCH, DIVIDE, SUMX, ADDCOLUMNS, ISBLANK, CALCULATE, VALUES, COALESCE, VAR, FILTER, TOPN, AVERAGEX, NOT, FALSE, COUNTROWS, MINX, SUM, RELATED, ALL, CALCULATETABLE, VALUE, TREATAS, CONCATENATEX, RELATEDTABLE, ERROR, MAXX.
- Features: variables, measures, blank handling, naming, iterators, testing and debugging, error handling, DAX queries, filter context, relationships, blank row of an invalid relationship, row context, aggregations, data types, DAX formatting, calculated columns, calculated tables, data lineage, totals and subtotals, translations.

### `t02-dax-authoring-style-2.md` (48 notes)

- Covers: IN operator and constructors; Data types and comparisons.
- DAX functions: CALCULATE, NOT, ALL, FILTER, OR, CONTAINSROW, CONVERT, INT, CONTAINS, TREATAS, SUMMARIZE, CALCULATETABLE, SUMX, VALUES, EXCEPT, AND, ISEMPTY, INTERSECT, DIVIDE, UNION, LOWER.
- Features: testing and debugging, data types, error handling, iterators, fact tables, currency conversion, measures, virtual relationships, naming, DAX formatting, conditional formatting, totals and subtotals.

## DAX table functions and queries

### `t03-table-functions-and-queries-1.md` (81 notes)

- Covers: Grouping and adding columns; Writing DAX queries; Filter and text conditions.
- DAX functions: SUMMARIZE, ADDCOLUMNS, CALCULATE, GROUPBY, CALCULATETABLE, FILTER, CURRENTGROUP, SEARCH, DEFINE, SELECTCOLUMNS, EVALUATE, CONTAINSSTRING, ISEMPTY, MAXX, DETAILROWS, VALUES, GENERATE, CONTAINS, ROW, LEFT, OR, ALL, FIND, AND, ROLLUP, SUM, NOT, COUNTROWS, DATATABLE, TREATAS, KEEPFILTERS, REMOVEFILTERS, MAX, BLANK, CROSSJOIN, ALLEXCEPT, CONTAINSSTRINGEXACT, SUBSTITUTE, IFERROR, RIGHT, RELATEDTABLE.
- Features: DAX queries, aggregations, iterators, testing and debugging, measures, variables, relationships, filter context, Excel and MDX clients, totals and subtotals, blank handling, translations, row context, context transition, fact tables, materialization, query plans, naming, slicers, expanded tables, dimension tables, formula engine, SQL views, blank row of an invalid relationship, external tools, detail rows.

### `t03-table-functions-and-queries-2.md` (78 notes)

- Covers: Calculated and static tables; SUMMARIZECOLUMNS behaviour; Joins and lookups; Set functions.
- DAX functions: SUMMARIZECOLUMNS, LOOKUPVALUE, SUMMARIZE, NATURALLEFTOUTERJOIN, NATURALINNERJOIN, ADDCOLUMNS, UNION, TREATAS, EXCEPT, INTERSECT, VALUES, RELATED, CROSSJOIN, SELECTCOLUMNS, GENERATE, CALCULATE, GENERATESERIES, FILTER, CONTAINS, ROW, CALCULATETABLE, SELECTEDVALUE, DATATABLE, RELATEDTABLE, CURRENCY, CALENDAR, IF, HASONEVALUE, GENERATEALL, CONVERT, ALL, ISBLANK, REMOVEFILTERS, COALESCE, NOT.
- Features: relationships, measures, data lineage, virtual relationships, naming, fact tables, error handling, calculated tables, DAX queries, blank handling, variables, data types, query plans, storage engine, aggregations, testing and debugging, iterators, row context, filter context, expanded tables, limited relationships, auto-exist, calculated columns, currency conversion, compression, parameter tables, blank row of an invalid relationship.
