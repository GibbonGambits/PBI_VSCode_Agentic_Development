# Storage modes

Part 1 of 2 of this topic. Covers: DirectQuery DAX and limits; DirectQuery model and source design; Choosing a storage mode.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### DirectQuery DAX and limits

**T09-W380-20.** Review the MaxIntermediateRowsetSize setting carefully when a DirectQuery model runs complex calculations over large tables: DAX functions not optimised for DirectQuery can force a large SQL result to be held in Analysis Services memory.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: A DirectQuery model with complex calculations on large tables.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-21.** In DirectQuery measures, avoid functions not optimised for DirectQuery, such as MEDIANX: they run in the formula engine, so the source must return the needed columns for every row of the table, which is slow and can pass the row limit.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Writing measures for a DirectQuery model.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-45.** In a DAX query on a DirectQuery model, SUMMARIZECOLUMNS can replace ADDCOLUMNS over ALL of the grouping column; this removes the extra SQL query that only fetches the grouping values, sent so that values without data still appear.
- Option. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Grouping in DAX queries against DirectQuery.
- Version: Analysis Services 2016, whose engine removes redundant joins; 2017 white paper.

**T09-A295-1.** Time intelligence functions tend to generate complex SQL in DirectQuery; explicit filter logic you write yourself gives simpler SQL and keeps the query plan under your control, so prefer it where feasible.
- Should. Check. 2024. https://www.sqlbi.com/articles/optimizing-time-intelligence-in-directquery/
- When: Time intelligence calculations on DirectQuery over SQL.
- Version: Tested in 2024; engine behaviour can change.

**T09-A295-2.** When tuning time intelligence measures in VertiPaq, prefer DAX logic that does not rely on the built-in time intelligence functions: they mostly fetch data at day granularity and aggregate it in the formula engine, which materialises many day-level rows.
- Should. Check. 2024. https://www.sqlbi.com/articles/optimizing-time-intelligence-in-directquery/
- When: Optimising time intelligence on VertiPaq; DirectQuery over SQL needs the same patterns for other reasons.
- Version: Tested in 2024; engine behaviour can change.

**T09-A295-5.** Before relying on any DAX optimisation pattern, verify it on the specific Tabular engine version you use: the engine changes over time, so the effect of an optimisation cannot be assumed.
- Must. 2024. https://www.sqlbi.com/articles/optimizing-time-intelligence-in-directquery/
- When: Applying any DAX optimisation pattern.

### DirectQuery model and source design

**T09-W380-7.** For DirectQuery, the source tuning includes the right indexes and probably partitioning to cut I/O: each query reads the table at least once and often needs only a small part of it.
- Must. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Preparing the relational source of a DirectQuery model.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-10.** Test how the specific relational database behind DirectQuery behaves before you settle modelling decisions: databases differ in function semantics, features and speed, so query plans and performance differ per source type.
- Must. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Designing a model in DirectQuery mode.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-11.** Base every table of a DirectQuery model on one source database. On SQL Server, views in that database may read other databases or servers; Analysis Services does not see this, and speed then depends on the SQL Server setup.
- Must. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Building a pure DirectQuery model.
- Version: Analysis Services 2016 Tabular, where a DirectQuery model takes one data source; 2017 white paper.

**T09-W380-13.** Feed a Tabular model, DirectQuery ones included, from views created in the SQL source, not from the physical tables: views keep the model independent of the physical structure of the database.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Choosing what the tables of a model read from a SQL database.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-14.** Keep the SQL behind a DirectQuery table simple too, with no complex joins or convoluted code: it runs again inside every query that fetches a slice of data, where an in-memory model runs it once.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Writing the SQL statement or view that a DirectQuery table reads.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-22.** In DirectQuery, consider storing a complex calculated column in the source database: the engine recomputes a model calculated column for every row each time a query uses it. Simple expressions are not a problem.
- Consider. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: A DirectQuery table needs a complex derived column.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-23.** When a DirectQuery calculated column is used as a filter, precompute it as a physical column in the database, despite the extra storage: filtering a calculated column scans the whole table however selective the filter. Columns used only in results are fine.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: A calculated column of a DirectQuery table is filtered on.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-24.** In a DirectQuery model, consider that every generated SQL query carries the extra predicates and joins of the role filters, which can make queries complex and slow; define those filters with close attention to detail.
- Consider. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: A DirectQuery model uses security roles.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-25.** When the relational database already enforces row-level security and Windows integrated security is in use, set the DirectQuery model to impersonate the current user, so queries run as that person and the database applies its own security.
- Must. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Source-side security exists; model roles are usually the alternative, but both can be combined.
- Version: Analysis Services 2016 Tabular; SQL Server 2016 row-level security as the example; 2017 white paper.

**T09-W380-26.** When a DirectQuery model impersonates the current user and Analysis Services runs on a different server from the relational database, also configure Kerberos delegation, so the user token reaches the database (the Windows double-hop problem).
- Must. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Impersonation across two servers.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-28.** On a DirectQuery model, assume that detail rows, subtotals and grand totals come from separate SQL queries run at different moments: with no cache, a total may not equal the sum of its lines when data changes.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Building or reviewing reports on DirectQuery; simple additive calculations sometimes need a single SQL query.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-29.** For Power BI reports on a DirectQuery model, you choose between bypassing the Power BI client cache (slower, more accurate) and using it (faster, but visuals can show stale data and totals that differ). The Refresh button clears the cache.
- Option. Check. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Report visuals on DirectQuery data that keeps changing.
- Version: Power BI as described in a 2017 white paper; check current behaviour.

**T09-W380-31.** When you create a DirectQuery model in SSDT, set the DirectQuery Mode property of the model to On before importing tables: data imported while it is Off is lost when the property is switched On.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Starting a new DirectQuery model in SSDT, which creates models with the property Off.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-33.** Remove every sample-data partition from a DirectQuery model before switching it back to in-memory mode: an in-memory model cannot contain sample data.
- Must. Check. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Switching a DirectQuery model with sample partitions to in-memory mode.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-35.** For SQL Server tables queried through DirectQuery, choose numeric types wide enough for aggregated results, not only single values, such as BIGINT rather than INT for a quantity summed over a huge fact table: SQL Server sums in the column type and can overflow.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Designing source columns; compression and clustered columnstore indexes can limit the extra storage.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-36.** Inner joins give the SQL optimiser more ways to push filters toward the fact table, which made most test queries faster. In SSDT of December 2016 the property had to be added in model.bim and set again after each edit of the relationship.
- Should. Check. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Relationships of a DirectQuery model whose source keeps referential integrity.
- Version: Analysis Services 2016 Tabular; SSDT as of December 2016.

**T09-W380-46.** To make the source answer DirectQuery queries on star or snowflake schemas quickly, you can apply the established data warehouse modelling practices for relational databases: the generated SQL is a plain pattern of joins, filters and grouping.
- Option. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Designing the relational database behind a DirectQuery model.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-A126-1.** In DirectQuery, a relationship on one native column always gives a better query plan than one that depends on several columns.
- Should. 2018. https://www.sqlbi.com/articles/using-combinevalues-to-optimize-directquery-performance/
- When: Choosing the key of a relationship in any Tabular model, DirectQuery included.

**T09-A126-2.** Consider a need to relate two tables on several columns as a sign that the model usually needs more denormalisation to reach a proper star schema.
- Consider. 2018. https://www.sqlbi.com/articles/using-combinevalues-to-optimize-directquery-performance/
- When: A relationship would need two or more columns; true most of the time, not always.

### Choosing a storage mode

**T09-W380-1.** Consider the trade-offs per model, then tune the model for the mode chosen: DirectQuery gives current data with no processing, memory limit or data copy, but loses in-memory speed and moves the query work to the database.
- Consider. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Deciding between DirectQuery and Import for a model.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-4.** Before choosing DirectQuery, check that the relational server can serve report queries while it handles its normal update workload: every query goes to the engine that receives the updates, whereas an in-memory model reads the source once.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Deciding whether a source can carry DirectQuery.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-5.** When a source table feeds an in-memory model, tune the source for one large read of the whole table during processing; indexes bring no benefit to that workload, which is a single SELECT over every row.
- Must. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Preparing source tables for import.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-6.** If a source table that feeds an in-memory model is partitioned, make its partitions match the partitions defined in the Tabular model.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Only where the source table needs partitioning.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-8.** On SQL Server, give tables that a DirectQuery model queries a columnstore index; for tables that only feed an in-memory model such an index is far from ideal. The source design has to match how the model uses it.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Choosing indexes for model source tables on SQL Server.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-9.** Before committing a project to DirectQuery, build a prototype, collect the SQL queries your DAX formulas produce and take time to understand them: knowing that workload helps you design the best relational data model.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Evaluating DirectQuery for a new project.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-30.** When only recent data must be real time, build two models: a small DirectQuery model for the last few days with simple calculations, and an in-memory model for the full history with the complex calculations.
- Should. Check. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Real-time needs cover only recent days.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-42.** Avoid enabling paging for an in-memory Tabular model.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Configuring memory for an Analysis Services in-memory model.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-43.** When an in-memory model does not fit in memory, prefer adding RAM: reducing the memory the data model uses is the harder alternative, because optimising it is a complex task.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: An Analysis Services in-memory model outgrows the memory of its server.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-44.** Build solid DAX skills before adopting DirectQuery, so you can judge how each calculation behaves there: which functions a project needs, and how much data they materialise, is hard to foresee at the start.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Planning a DirectQuery project.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-A234-1.** Avoid making a whole model DirectQuery only because a handful of dashboards need real-time data: a pure DirectQuery model puts the cost of every query on the source. DirectQuery mainly fits when data cannot be imported fast enough for most reports.
- Should. Check. 2021. https://www.sqlbi.com/articles/creating-real-time-dashboards-in-power-bi-with-push-datasets/
- When: Everything else in the model could be imported.

## Special-case techniques and facts

### DirectQuery DAX and limits

**T09-A083-3.** Consider keeping the Analysis Services setting MaxIntermediateRowsetSize well below extreme values such as 100 million: with too high a cap, a DirectQuery query can run out of memory or time out before the cap stops it.
- Consider. Check. 2016. https://www.sqlbi.com/articles/tuning-query-limits-for-directquery/
- When: Tuning the DirectQuery row limit of an Analysis Services Tabular instance.
- Version: 2016 advice for Analysis Services; in Power BI the setting cannot be changed in a supported way.

**T09-W380-18.** The one-million-row default applies to each SQL query DirectQuery sends. A DAX query that makes the source return detail rows, such as every existing pair of two columns, instead of an aggregate fails with an error; Power BI offers no supported way to raise it.
- Fact. Check. 2016. https://www.sqlbi.com/articles/tuning-query-limits-for-directquery/ ; https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: A DirectQuery query moves detail rows to the engine instead of letting the source aggregate.
- Version: Stated in 2016-2017 for Analysis Services 2016 and for models made with Power BI Desktop.

**T09-W380-19.** On a server with ample memory and good bandwidth to the source, raise MaxIntermediateRowsetSize above the row count of the largest dimension, but not far beyond: about 10 million suits dimensions of 4 and 8 million rows.
- Should. Check. 2016. https://www.sqlbi.com/articles/tuning-query-limits-for-directquery/ ; https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Analysis Services Tabular in DirectQuery mode; the setting is added by hand to msmdsrv.ini.
- Version: Analysis Services 2016 Tabular (2016-2017); cannot be changed in Power BI in a supported way.

**T09-W380-37.** In DirectQuery, a time intelligence calculation over a non-additive measure such as a distinct count sends one SQL query per row of the result, so its cost grows with the number of result rows.
- Fact. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Speed stays fair on SQL Server when the fact table has a clustered columnstore index.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-38.** In a DirectQuery model, when LASTNONBLANK looks for the last date with data, test that fact rows exist with NOT ISEMPTY inside CALCULATE instead of evaluating the measure: the existence test reads only the date column and is easier for SQL Server to optimise.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Finding the last date with data in DirectQuery.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-40.** In DirectQuery mode a division by zero or by BLANK raises an error, though the same expression is valid in an in-memory model; only BLANK divided by BLANK returns BLANK in both modes, because SQL Server has no notion of infinity.
- Fact. Check. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Division with the / operator in a DirectQuery model.
- Version: Analysis Services 2016 Tabular on SQL Server; 2017 white paper; check current behaviour.

**T09-W380-41.** DirectQuery evaluates DAX with SQL semantics, so results or errors can differ from in-memory mode: mixed-type comparisons and casts, numeric overflow, out-of-range dates, currency limits, LOG of BLANK, SECOND, CEILING, POWER, and text functions such as TRIM, LEN, SUBSTITUTE, SEARCH, REPLACE, MID and LEFT.
- Fact. Check. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Porting or testing formulas between in-memory and DirectQuery modes.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-A087-1.** To study the SQL that one DAX or MDX query produces on a DirectQuery model, you can capture it with Server Timings in DAX Studio: the storage engine entries show SQL statements instead of xmSQL. This is easier than SQL Profiler for one query.
- Option. 2016. https://www.sqlbi.com/articles/analyze-directquery-requests-using-dax-studio/
- When: Analysing one query against a Power BI or Analysis Services model in DirectQuery mode.
- Version: DAX Studio 2.5 or later; Analysis Services up to 2017 also needs the DirectQuery Trace option.

**T09-A087-2.** On a server version that still needs it, turn on the DirectQuery Trace setting in the DAX Studio options before you try to capture DirectQuery trace events.
- Must. Check. 2016. https://www.sqlbi.com/articles/analyze-directquery-requests-using-dax-studio/
- When: Tracing DirectQuery requests from DAX Studio.
- Version: Needed for SQL Server Analysis Services up to 2017; not for Power BI, Azure Analysis Services or 2019.

**T09-A087-3.** Keep the DirectQuery Trace option of DAX Studio on only while you work on DirectQuery models, ideally when other users put little load on the server: it filters events on the client, which makes tracing costlier for every session.
- Should. Check. 2016. https://www.sqlbi.com/articles/analyze-directquery-requests-using-dax-studio/
- When: Servers where the DirectQuery Trace option is still needed.
- Version: Needed for SQL Server Analysis Services up to 2017; not for Power BI, Azure Analysis Services or 2019.

**T09-A087-4.** In DAX Studio Server Timings on a DirectQuery model the CPU figure is always zero, because time spent in the SQL source counts as waiting; the split of duration between formula engine and storage engine is still shown.
- Fact. Check. 2016. https://www.sqlbi.com/articles/analyze-directquery-requests-using-dax-studio/
- When: Reading Server Timings captured against a DirectQuery model.

**T09-A087-5.** On a DirectQuery model you can use the formula engine and storage engine durations of DAX Studio Server Timings to measure what a DAX rewrite gains, for example SUMMARIZECOLUMNS in place of ADDCOLUMNS around SUMMARIZE.
- Option. 2016. https://www.sqlbi.com/articles/analyze-directquery-requests-using-dax-studio/
- When: Optimising DAX queries against a DirectQuery model.

**T09-A087-6.** DAX measures on a DirectQuery model can be tuned with the general DAX optimisation principles, bearing in mind that the storage engine is different and has nothing like the VertiPaq storage engine cache.
- Option. 2016. https://www.sqlbi.com/articles/analyze-directquery-requests-using-dax-studio/
- When: Optimising measures of a model in DirectQuery mode.

**T09-A295-3.** A previous-year value by month can be computed without time intelligence functions: take the current sequential year-month number, remove the filters on the Date table with REMOVEFILTERS inside CALCULATE, and filter on that number minus 12.
- Option. Check. 2024. https://www.sqlbi.com/articles/optimizing-time-intelligence-in-directquery/
- When: The Date table has a sequential year-month number column; used for DirectQuery and VertiPaq alike.
- Version: In a 2024 DirectQuery test the time fell from about 3.2 seconds to under 2.

**T09-A295-4.** In DirectQuery only some time intelligence functions let the engine group at the granularity the query asks for: SAMEPERIODLASTYEAR and DATEADD do; DATESBETWEEN, DATESYTD and more complex queries still return day-level data to the formula engine, enlarging the datacache.
- Fact. Check. 2024. https://www.sqlbi.com/articles/optimizing-time-intelligence-in-directquery/
- When: Time intelligence over DirectQuery on SQL.
- Version: Observed in 2024; test on the Tabular version in use.

### DirectQuery model and source design

**T09-W380-16.** The limit to scalar functions that work in a row context also holds for row-level security filters of a DirectQuery model, because both must be translated into SQL expressions; aggregation functions, table functions and iterators are not allowed there.
- Fact. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Writing a security role filter or a calculated column in a DirectQuery model.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-17.** MDX sent to a DirectQuery model needs fully qualified names, allows no session-scope statements (query-scope WITH still works), no subselect tuples mixing levels, and no user-defined hierarchies, so Excel does not see them while DAX clients do.
- Fact. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: MDX clients other than Excel, or hand-written MDX, query a DirectQuery model.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-27.** For row-level security on an older SQL Server source, one option: a schema per user group holding same-named filtered views, each user given that default schema and SELECT rights on it, and DirectQuery partitions bound to SQL statements without schema names.
- Option. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: DirectQuery queries reach the source with the credentials of each user.
- Version: For SQL Server before 2016, which has row-level security of its own; 2017 white paper.

**T09-W380-34.** To test the data of a deployed model you can switch it between DirectQuery and in-memory mode, a faster alternative to sample partitions. After a switch to in-memory the database must be processed; a switch to DirectQuery needs no processing.
- Option. Check. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Each table of the deployed model has a single partition.
- Version: Analysis Services 2016 Tabular (2017 paper); not for Power BI Desktop, where a table set to Import cannot return.

**T09-W380-39.** In one comparison, bidirectional filtering, whether set on a relationship or switched on in DAX, made DirectQuery queries 3 to 30 times slower, depending on query complexity. In many-to-many models the size of the bridge table can also become a problem.
- Fact. Check. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: DirectQuery models with bidirectional filters.
- Version: Analysis Services 2016 tests published in 2017.

**T09-A087-7.** When a DirectQuery query is slow in the relational source, you can take the slowest captured SQL statement and run it directly on the database, for example in SQL Server Management Studio, to look for improvements on the source side.
- Option. 2016. https://www.sqlbi.com/articles/analyze-directquery-requests-using-dax-studio/
- When: The bottleneck of a DirectQuery query lies in the source database.

**T09-A126-3.** Where two tables can only be related on several columns, a single combined key suits small tables or cases where heavier reshaping is impossible; it has more distinct values than the original columns, which costs performance.
- Should. 2018. https://www.sqlbi.com/articles/using-combinevalues-to-optimize-directquery-performance/
- When: No single native column can carry the relationship.

**T09-A126-4.** In an import model a relationship performs best on one column with few distinct values; a key that concatenates several key columns ends up with more distinct values than any of them, and that hurts performance.
- Fact. 2018. https://www.sqlbi.com/articles/using-combinevalues-to-optimize-directquery-performance/
- When: In-memory models, where cardinality is the only concern of a concatenated key.

**T09-A126-5.** In DirectQuery a relationship on calculated columns built by string concatenation becomes a SQL join on expressions that build a string for every row of both tables; the source can hardly use its indexes for it, so queries slow down.
- Fact. 2018. https://www.sqlbi.com/articles/using-combinevalues-to-optimize-directquery-performance/
- When: A multi-column relationship is emulated with concatenated-string columns in DirectQuery.

**T09-A126-6.** COMBINEVALUES tells DirectQuery which columns lie beneath the key, so the generated SQL joins on the original columns, can partly use existing indexes and usually gets a much better plan than string concatenation.
- Should. 2018. https://www.sqlbi.com/articles/using-combinevalues-to-optimize-directquery-performance/
- When: DirectQuery tables need a relationship on several columns and no native single column exists.
- Version: As of Power BI April 2018 the SQL still held NULL checks, even for NOT NULL columns.

**T09-A126-7.** Assume referential integrity can also be turned on for a DirectQuery relationship on COMBINEVALUES key columns, giving an inner join instead of a left outer join; it does not remove the extra NULL-checking conditions in the join.
- Option. 2018. https://www.sqlbi.com/articles/using-combinevalues-to-optimize-directquery-performance/
- When: A DirectQuery relationship built on COMBINEVALUES calculated columns.
- Version: Observed with Power BI in 2018.

### Choosing a storage mode

**T09-W380-3.** In one benchmark, queries took 1.5 to 2.9 times as long in DirectQuery as in memory, varying with the query and its number of joins; DirectQuery was never the faster of the two.
- Fact. Check. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Measured on a 4-billion-row fact table in a SQL Server clustered columnstore; results may differ elsewhere.
- Version: Analysis Services 2016 benchmark published in 2017.
