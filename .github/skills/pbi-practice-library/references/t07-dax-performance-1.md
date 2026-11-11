# DAX performance and optimization

Part 1 of 3 of this topic. Covers: Filters, counts and emptiness tests; Measuring and testing performance; Formula and storage engine.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### Filters, counts and emptiness tests

**T07-A040-2.** Keep the number of items that filter arguments iterate low: give each needed column its own filter over its distinct values, not one filter scanning every row of the table. In one example this made iterating the filter conditions roughly ten times faster.
- Should. 2014. https://www.sqlbi.com/articles/filter-vs-calculatetable-optimization-using-cardinality-estimation/
- When: Most CALCULATE or CALCULATETABLE filters; possible exception: several context-dependent filters evaluated together with a distinct count.

**T07-A040-6.** When one filter holds conditions on two or more columns joined by AND, always test whether a separate filter on each column performs better: separate column filters are faster in several cases.
- Must. 2014. https://www.sqlbi.com/articles/filter-vs-calculatetable-optimization-using-cardinality-estimation/
- When: Filter arguments that combine conditions on different columns with AND.

**T07-A041-1.** To test whether a table expression returns no rows, prefer ISEMPTY; the next choice is ISBLANK over COUNTROWS, and comparing COUNTROWS with zero comes last. ISEMPTY is simpler, clearer and faster: a COUNTROWS test counts every row of a non-empty table for nothing.
- Should. Check. 2014. https://www.sqlbi.com/articles/check-empty-table-condition-with-dax/
- When: Any DAX test of whether a table or filtered table is empty, typically the condition of an IF.
- Version: ISEMPTY arrived in SQL Server 2012 SP1 CU4; in 2014 Excel 2013 lacked it, breaking upgraded Excel 2010 models.

**T07-W378-1.** When one business entity appears in the fact table as several rows, one per status change, count the entity with a distinct count over its identifier, not by counting rows: a row count adds up every status transition and returns wrong numbers.
- Must. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: A fact table stores each status change of an entity as its own row and a measure counts entities.

**T07-A079-2.** When a measure sums copies of one base measure that differ only in the value each CALCULATE filters on the same column, rewrite it as one CALCULATE whose single filter on that column admits all wanted values: one storage engine query, not one per value.
- Should. Check. 2016. https://www.sqlbi.com/articles/optimizing-dax-expressions-involving-multiple-measures/
- When: The added measures each filter a different value of one column; confirm the gain on your model.
- Version: The July 2016 engine did not merge such sums; a later engine may make the rewrite unnecessary.

**T07-A171-1.** DISTINCTCOUNT is normally the better way to count distinct values, compared with DISTINCT iterated inside SUMX. The exception is dense reports whose measure applies filters that do not match the visual's grouping granularity, as time intelligence calculations always do.
- Should. 2019. https://www.sqlbi.com/articles/analyzing-distinctcount-performance-in-dax/
- When: Choosing how to write a distinct count measure.

**T07-A171-4.** Never write a distinct count as SUMX over DISTINCT in a DirectQuery model: that pattern usually costs more than the DISTINCTCOUNT that the data source runs natively.
- Must. 2019. https://www.sqlbi.com/articles/analyzing-distinctcount-performance-in-dax/
- When: DirectQuery models.

**T07-A171-6.** Weigh this: DISTINCTCOUNT leans on the storage engine and is usually quicker per cell, but more cells or per-cell filters raise its storage engine queries. SUMX over DISTINCT needs fewer queries, yet materializes data, possibly large, and counts in the formula engine.
- Consider. 2019. https://www.sqlbi.com/articles/analyzing-distinctcount-performance-in-dax/
- When: Choosing an implementation for a distinct count measure used in several reports.

### Measuring and testing performance

**T07-W378-33.** Build a set of test queries that reflects how users really query the model, record their baseline execution times, and keep those results with the project's documents.
- Should. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Any model whose query speed matters.

**T07-W378-34.** Once the model is in production, collect the queries users actually run, at regular intervals: these real queries save a lot of time when architecture decisions come up later.
- Should. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: A model in production use.

**T07-W378-37.** Before going live with many concurrent users, consider a load test on a test server that simulates them, measuring how many users one server supports and how fast queries run under load. One Tabular query can use every core, so single-query speed says little.
- Consider. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Multi-user deployments with hundreds of concurrent users.
- Version: Described for Analysis Services Tabular in SQL Server 2012 and 2014.

**T07-A079-4.** After merging several separately filtered CALCULATE measures into one filtered CALCULATE for speed, check that it really is faster on your own model, and review the choice again each time the DAX engine is upgraded.
- Should. 2016. https://www.sqlbi.com/articles/optimizing-dax-expressions-involving-multiple-measures/
- When: Sums of separately filtered measures were replaced by one combined filter.
- Version: A future DAX engine with a better query plan could make the rewrite unnecessary.

**T07-A128-2.** Before relying on any DAX rewrite made for speed, measure the original and the rewritten version on the concrete use case: which one is faster can change with the details of the requirement and with how the data is distributed.
- Should. 2018. https://www.sqlbi.com/articles/optimizing-mutually-exclusive-calculations/
- When: Choosing between alternative formulations of the same calculation.

**T07-A128-6.** Know more than one way to write a given DAX calculation: a slow measure is fixed by rewriting its DAX to obtain a better execution plan, and which formulation performs better depends on the requirement and on how the data is distributed.
- Should. Check. 2018. https://www.sqlbi.com/articles/optimizing-mutually-exclusive-calculations/
- When: A performance issue arises in a DAX calculation.

**T07-A334-4.** Never assume one formulation of a DAX calculation is the fastest in every scenario, even for a simple-looking measure. Test the alternatives extensively and choose with the results in hand before production: the winner depends on model size, data distribution, compression and the measure's complexity.
- Must. 2018. https://www.sqlbi.com/articles/optimizing-dax-with-cardinality-estimation-computing-working-days/ ; https://www.sqlbi.com/articles/finding-products-without-sales-by-using-dax/ ; https://www.sqlbi.com/articles/understanding-how-dax-evaluates-if-statements/
- When: Any measure rewritten for speed, especially when performance is critical.

**T07-A156-1.** When timing visuals with Performance Analyzer, base the analysis mainly on the durations recorded after pressing Refresh visuals, not on the first load of the page: the first run also allocates memory structures for visuals and model queries.
- Should. 2019. https://www.sqlbi.com/articles/introducing-the-power-bi-performance-analyzer/
- When: Analysing visual durations captured by Performance Analyzer in Power BI Desktop.
- Version: Performance Analyzer exists in Power BI Desktop since May 2019.

**T07-A156-5.** For a visual with a long DAX Query time, one way to dig further is to copy its query from Performance Analyzer and run it in DAX Studio with the Query Plan and Server Timings traces on. Causes: a slow measure, model or data source.
- Option. Check. 2019. https://www.sqlbi.com/articles/introducing-the-power-bi-performance-analyzer/
- When: A visual whose DAX Query duration in Performance Analyzer is large; a slow source is likeliest with DirectQuery.
- Version: Performance Analyzer exists in Power BI Desktop since May 2019.

**T07-A156-6.** When you run again in DAX Studio a query taken from Performance Analyzer, consider clearing the engine cache before the run: Performance Analyzer leaves the Tabular engine cache in place between executions.
- Consider. 2019. https://www.sqlbi.com/articles/introducing-the-power-bi-performance-analyzer/
- When: Repeating in DAX Studio a DAX query copied from Performance Analyzer.
- Version: Performance Analyzer exists in Power BI Desktop since May 2019.

**T07-A157-1.** To find a report's slowest queries, one option is to export the Performance Analyzer capture from Power BI Desktop as a JSON file, open it in DAX Studio with Load Perf Data, and sort by Query Ms descending; the list also names the visual responsible.
- Option. Check. 2019. https://www.sqlbi.com/articles/importing-performance-analyzer-data-in-dax-studio/
- When: A Performance Analyzer capture has been recorded and exported.
- Version: DAX Studio imports Performance Analyzer data from version 2.9.0.

**T07-A157-2.** When saving the Performance Analyzer export for DAX Studio, you may change the file name, but keep the .json extension.
- Should. 2019. https://www.sqlbi.com/articles/importing-performance-analyzer-data-in-dax-studio/
- When: Exporting Performance Analyzer data, saved by default as PowerBIPerformanceData.JSON, to load into DAX Studio.
- Version: DAX Studio imports Performance Analyzer data from version 2.9.0.

**T07-A157-3.** After loading Performance Analyzer data in DAX Studio, you can double-click the Query text of a query to send it to the editor, then run it again with Query Plan and Server Timings enabled to see why it is slow.
- Option. Check. 2019. https://www.sqlbi.com/articles/importing-performance-analyzer-data-in-dax-studio/
- When: Investigating a query from a capture loaded into DAX Studio; the copied code starts with a metrics comment.
- Version: DAX Studio imports Performance Analyzer data from version 2.9.0.

**T07-A171-3.** Measure the alternative distinct count implementations on your own model and reports with DAX Studio, and study their query plans there: nothing else tells you what to expect, and the plans help foresee behaviour in other reports.
- Should. 2019. https://www.sqlbi.com/articles/analyzing-distinctcount-performance-in-dax/
- When: Choosing between alternative implementations of a distinct count.

**T07-A195-3.** To time each visual of a page, you can use the Performance Analyzer pane: start recording, refresh the visuals, sort by total time in descending order, and optionally export the events to a JSON file for closer analysis.
- Option. 2020. https://www.sqlbi.com/articles/optimizing-card-visuals-in-slow-power-bi-reports/
- When: Analyzing a slow Power BI report page.

**T07-A350-3.** Assess the performance of DAX and modelling choices on big models, where the many side holds tens of millions of rows and the one side millions, never on small samples: there, queries end so fast that repeated runs can vary by more than double.
- Must. 2026. https://www.sqlbi.com/articles/analyzing-the-performance-of-limited-and-regular-relationships/
- When: Performance testing of DAX code or model design choices such as relationship types.

**T07-A350-4.** When you compare DAX formulas or queries, judge them by storage engine CPU time and formula engine time, not by elapsed time or storage engine duration alone: parallelism shrinks durations, while CPU time shows the real processing cost.
- Should. 2023. https://www.sqlbi.com/articles/finding-products-without-sales-by-using-dax/ ; https://www.sqlbi.com/articles/analyzing-the-performance-of-limited-and-regular-relationships/
- When: Reading server timings while evaluating DAX or model performance.

**T07-A372-2.** When judging whether a rewritten DAX formula is faster, remember that the answer depends on the shape of the query: compare the versions across several query shapes, such as different groupings and granularities. A formula can win one test and lose others.
- Consider. 2026. https://www.sqlbi.com/articles/optimizing-dax-with-ai/
- When: Comparing the performance of alternative versions of a measure.

**T07-A372-3.** When optimizing DAX, take the data distribution into account: it changes which optimization fits best. Models with different proportions of entities and transactions, such as customers against transactions, call for different optimizations and give different results.
- Consider. 2026. https://www.sqlbi.com/articles/optimizing-dax-with-ai/
- When: Choosing among candidate optimizations for a measure.

**T07-A372-4.** When optimizing a measure, build a broad set of test queries that evaluate the original and the candidate measure on known edge cases, and check that their results match: this verifies that the new measure is functionally equivalent.
- Should. 2026. https://www.sqlbi.com/articles/optimizing-dax-with-ai/
- When: Rewriting an existing measure for performance.

**T07-A372-5.** Use an AI assistant to write and run the test queries of a DAX optimization, gather their results and report whether a new formula can replace the old one: running many tests by hand is tedious and error-prone.
- Should. 2026. https://www.sqlbi.com/articles/optimizing-dax-with-ai/
- When: Verifying a rewritten measure with many test queries.

**T07-A372-11.** One approach to DAX optimization combines human and AI work: a person proposes new optimization ideas and an AI assistant refines them. In one example the AI-refined human version won overall and was found much faster.
- Option. 2026. https://www.sqlbi.com/articles/optimizing-dax-with-ai/
- When: Optimizing a DAX formula with an AI assistant; drawn from one simple test, results may vary.
- Version: Initial 2026 findings, expected to change quickly as new language models appear.

### Formula and storage engine

**T07-A171-5.** Favour query plans that spend most of their time in the storage engine, not the formula engine: storage engine queries can be answered from cache, while formula engine work is done again at every run.
- Should. Check. 2019. https://www.sqlbi.com/articles/analyzing-distinctcount-performance-in-dax/
- When: Reading query plans; the cache stops helping once one DAX query exceeds the storage engine queries it keeps.
- Version: The cache kept 256 storage engine queries in 2019; check the current value.

**T07-A260-3.** Turn the horizontal fusion optimization on by hand if it is still a preview feature.
- Should. Check. 2022. https://www.sqlbi.com/articles/introducing-horizontal-fusion-in-dax/
- When: A Power BI version in which horizontal fusion is not yet on by default.
- Version: Arrived with Power BI September 2022, possibly as a preview; a preview feature needs the developer's yes.

**T07-A271-2.** Before rewriting existing measures to go beyond horizontal fusion, weigh whether the extra speed is really needed: the rewrite may duplicate logic across measures and raise maintenance cost, because changes to the specialized measures stop flowing into the combined one.
- Consider. 2023. https://www.sqlbi.com/articles/optimizing-fusion-optimization-for-dax-measures/
- When: Changing an existing solution; horizontal fusion itself is a first step that needs no code change.

## Special-case techniques and facts

### Filters, counts and emptiness tests

**T07-A040-1.** A Boolean condition written directly as a filter argument of CALCULATE or CALCULATETABLE still costs an iteration: the engine turns it into an equivalent FILTER, so it only looks cheaper than an explicit FILTER because the iteration is hidden.
- Fact. 2014. https://www.sqlbi.com/articles/filter-vs-calculatetable-optimization-using-cardinality-estimation/
- When: A logical expression is passed as a filter argument of CALCULATE or CALCULATETABLE.

**T07-A040-3.** When a distinct count runs under several CALCULATE filter arguments that each depend on the outer context, consider merging them into one FILTER condition. It costs more by itself, but separate filters can build a temporary Cartesian product that is slower than one table scan.
- Consider. Check. 2014. https://www.sqlbi.com/articles/filter-vs-calculatetable-optimization-using-cardinality-estimation/
- When: Only with several context-dependent filters plus a distinct count, worst with a many-to-many relationship; benchmark first.
- Version: Reported in 2014; later engine releases were expected to make the merged filter unnecessary.

**T07-A040-5.** For a distinct count limited by conditions on two columns of one fact table, a possibly better option than filtering the whole table is one FILTER over ALL of just those two columns, wrapped in KEEPFILTERS.
- Option. Check. 2014. https://www.sqlbi.com/articles/filter-vs-calculatetable-optimization-using-cardinality-estimation/
- When: The conditions depend on the outer context; always test separate single-column filters too, which are often faster.
- Version: Option described in May 2018.

**T07-A041-2.** In DAX queries over a Multidimensional model (DAXMD), test for an empty table with ISEMPTY and avoid every variant built on COUNTROWS: the speed gain of ISEMPTY matters a great deal there.
- Should. 2014. https://www.sqlbi.com/articles/check-empty-table-condition-with-dax/
- When: DAX queries against an Analysis Services Multidimensional model.
- Version: ISEMPTY needs build 11.00.3368 (CU4 of SQL Server 2012 SP1) or later.

**T07-A041-3.** COUNTROWS over an empty table returns BLANK, not zero. Comparing that result with zero for equality is still true, because BLANK is converted to 0 in scalar and logical expressions.
- Fact. 2014. https://www.sqlbi.com/articles/check-empty-table-condition-with-dax/
- When: The result of COUNTROWS is used to detect an empty table.

**T07-W378-12.** Distinct counts in Tabular are very fast on low-cardinality columns, with a few hundred values, but slow down as the cardinality of the counted column rises.
- Fact. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: A distinct count measure runs over a column with many distinct values, such as a unique contact id.
- Version: Cumulative update 9 for SQL Server 2012 SP1 improved distinct counts on columns with many values.

**T07-W378-13.** When a high-cardinality id column exists in the fact table only to be distinct-counted and every query stays within one business unit or similar group, you can replace it with a group id plus an id unique within the group: fewer distinct values, nothing lost.
- Option. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: The id column is used only for counting and all analysis is done within one group at a time.

**T07-W378-39.** Tabular computes distinct counts with good performance without tuning and without extra processing time, and better than Analysis Services Multidimensional; some optimization can still be needed.
- Fact. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Choosing an engine for a model whose measures rely heavily on distinct counts.
- Version: Described for Analysis Services Tabular in SQL Server 2012 and 2014.

**T07-A079-3.** In a profit-and-loss model whose measures select accounts, total all accounts of the same sign in one intermediate measure, with one CALCULATE that filters all of them, then subtract one intermediate measure from the other. Do not add and subtract a separate measure per account.
- Should. Check. 2016. https://www.sqlbi.com/articles/optimizing-dax-expressions-involving-multiple-measures/
- When: Measures that each filter specific accounts are combined by addition and subtraction; confirm the gain.
- Version: A future DAX engine with a better query plan could make this unnecessary.

**T07-A156-7.** A possible fix for a slow CALCULATE around DISTINCTCOUNT: replace a FILTER over the whole fact table with the equivalent filter on the single column, written with KEEPFILTERS. A table filter with DISTINCTCOUNT gives an inefficient query plan; one query then fell below 10 milliseconds.
- Option. 2019. https://www.sqlbi.com/articles/introducing-the-power-bi-performance-analyzer/
- When: A table filter on the fact table surrounds a DISTINCTCOUNT and an equivalent column filter exists.

**T07-A171-2.** Before you swap DISTINCTCOUNT for SUMX over DISTINCT to speed one report up, you must check that the swap does not slow many other reports down.
- Must. 2019. https://www.sqlbi.com/articles/analyzing-distinctcount-performance-in-dax/
- When: SUMX over DISTINCT beats DISTINCTCOUNT in one given report.

**T07-A181-2.** A measure that searches a previous item with LASTNONBLANK or FIRSTNONBLANK can sit inside an IF that tests NOT ISEMPTY on the fact table: the search then runs only where the filter context holds fact rows, and no previous date shows for dates without transactions.
- Option. 2020. https://www.sqlbi.com/articles/optimizing-lastnonblank-and-lastnonblankvalue-calculations/
- When: Measures shown to users that search earlier items, such as the previous date with sales.

**T07-A181-3.** Put the test for visible fact rows only in the measure shown to users, not in a hidden helper measure that only other measures call: testing once, in the visible measure, is more efficient.
- Should. 2020. https://www.sqlbi.com/articles/optimizing-lastnonblank-and-lastnonblankvalue-calculations/
- When: A hidden measure used only by visible measures that already test for fact rows.

**T07-A181-8.** When the search is for the previous order, not the previous date, you can remove the filters on the Date table inside the search, so that an earlier order placed on another date is still found.
- Option. 2020. https://www.sqlbi.com/articles/optimizing-lastnonblank-and-lastnonblankvalue-calculations/
- When: A measure looking up the previous order number in a report that also filters dates.

**T07-A181-9.** A measure that finds the previous date with data through LASTNONBLANK must change the filter context on the Date table, for example with CALCULATE and a filter keeping only dates before the one visible in the cell. Otherwise each cell considers only its own date.
- Must. 2020. https://www.sqlbi.com/articles/optimizing-lastnonblank-and-lastnonblankvalue-calculations/
- When: Retrieving the last earlier date with a transaction for the customers filtered in the report.

**T07-A285-2.** To flag items with no transactions in the current filter context, prefer ISEMPTY on the fact table to comparing an amount measure or a row count with zero: it only checks that a row exists. An amount ran slower; a row count hardly differed.
- Should. 2023. https://www.sqlbi.com/articles/finding-products-without-sales-by-using-dax/
- When: Only when every fact row is a sale; with negative returns, row presence is no valid test.

**T07-A285-3.** Checking for items without sales with INTERSECT or EXCEPT over the key values of the dimension and the fact table makes the engine also fetch the key column, which the report does not group by. These versions run slower than measures naming no specific column.
- Fact. 2023. https://www.sqlbi.com/articles/finding-products-without-sales-by-using-dax/
- When: The query groups by a descriptive column, such as a product name, not by the key.

**T07-A285-4.** Detecting missing sales by testing whether the single selected product key is IN the key values of the fact table adds a callback to the main storage engine query and performs very badly.
- Fact. 2023. https://www.sqlbi.com/articles/finding-products-without-sales-by-using-dax/
- When: A measure of this form, which assumes the outer query computes one product at a time.

### Measuring and testing performance

**T07-A040-4.** Always benchmark on your own data before you replace separate CALCULATE filter arguments with one merged filter to speed up a distinct count.
- Must. Check. 2014. https://www.sqlbi.com/articles/filter-vs-calculatetable-optimization-using-cardinality-estimation/
- When: A measure with many filter arguments and a distinct count is a candidate for merging its filters.

**T07-A195-4.** In Performance Analyzer, the time shown as Other for a visual is time spent waiting for other tasks to finish before its DAX query can run and its result be drawn. It appears when many visuals on a page send queries.
- Fact. 2020. https://www.sqlbi.com/articles/optimizing-card-visuals-in-slow-power-bi-reports/
- When: Reading Performance Analyzer results for a page with many visuals that send queries.

**T07-A235-1.** To find storage engine operations that do not spread their work over several cores, you can read the Par. column of the Server Timings pane in DAX Studio: each operation's CPU time divided by its duration.
- Option. Check. 2021. https://www.sqlbi.com/articles/analyzing-the-parallelism-of-storage-engine-operations-in-dax-studio/
- When: Queries on a model with imported data; no ratio shows when CPU or duration is zero.
- Version: The parallelism column was presented as new in DAX Studio 2.17.

**T07-A235-3.** When server timings leave out the cost of storage engine Batch events, a formula engine cost worked out as total query duration minus the sum of Scan events is distorted.
- Fact. 2021. https://www.sqlbi.com/articles/analyzing-the-parallelism-of-storage-engine-operations-in-dax-studio/
- When: Complex models where batch requests hold several storage engine operations.
- Version: DAX Studio up to 2.16 showed only Scan operations by default; 2.17 reports each Batch event's net cost.

### Formula and storage engine

**T07-W378-10.** A basic principle of Tabular query performance: the less memory a query has to scan, the faster it runs. The principle has many subtle variations.
- Fact. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Reasoning about the query speed of an in-memory Tabular model.

**T07-A044-2.** DIVIDE always runs in the formula engine. Row by row inside an iterator such as SUMX, it puts a CALLBACKDATAID in the storage engine query, which then cannot use the VertiPaq cache and often runs slower; an IF test inside the iterator does the same.
- Fact. 2014. https://www.sqlbi.com/articles/divide-performance/
- When: Row-by-row division inside an iterator over a large table; hard to see on small data.
- Version: First described before Power BI existed; the same behaviour shows on large Power BI models.

**T07-A208-1.** The formula engine runs on one thread and sends its storage engine requests one at a time, waiting for each to finish. Multi-core parallelism exists only inside a single storage engine request, so the formula engine can cap the parallelism reached overall.
- Fact. Check. 2020. https://www.sqlbi.com/articles/formula-engine-and-storage-engine-in-dax/
- When: Reasoning about why a DAX query does not use all cores.
- Version: Described in 2020; check against the current engine.

**T07-A208-2.** Two frequent performance problems, an oversized datacache materialization and too many storage engine requests, often trace back to a flaw in the data model or in the DAX formulas.
- Fact. 2020. https://www.sqlbi.com/articles/formula-engine-and-storage-engine-in-dax/
- When: Diagnosing a slow DAX query from its storage engine activity.

**T07-A235-2.** Inside a storage engine batch, usually only the last scan's result goes to the formula engine; results of earlier scans stay in the storage engine. Materialization handed to the formula engine costs more than materialization kept within the batch.
- Fact. 2021. https://www.sqlbi.com/articles/analyzing-the-parallelism-of-storage-engine-operations-in-dax-studio/
- When: Complex models where one formula engine batch request runs several storage engine operations.
- Version: DAX Studio 2.17 shows the Batch subclass in Server Timings by default.

**T07-A260-1.** Horizontal fusion computes in one storage engine query, grouped by a column, several similar calculations that differ only in the single value filtered on that column; aggregations need only fit one scan, as MIN and AVERAGE do. Earlier, differently filtered aggregations each ran separately.
- Fact. 2022. https://www.sqlbi.com/articles/introducing-horizontal-fusion-in-dax/ ; https://www.sqlbi.com/articles/optimizing-dax-expressions-involving-multiple-measures/
- When: Calculations that are subexpressions of the same measure or expression, under different single-value filters on one column.
- Version: Power BI has it from its September 2022 release.

**T07-A260-2.** Horizontal fusion does not merge storage engine queries when an aggregation of a very different query shape, such as DISTINCTCOUNT, is mixed in, when one calculation filters several values of the column, or when the calculations differ in values filtered on more than one column.
- Fact. Check. 2022. https://www.sqlbi.com/articles/introducing-horizontal-fusion-in-dax/
- When: Expecting several similar calculations to share one storage engine query.
- Version: As of 2022; the limits on several values and several columns might be improved later.

**T07-A260-4.** If you rely on horizontal fusion for a calculation whose filter holds several values of a column, confirm in your own tests how the engine really behaves: fusion does not apply when the filter context holds more than one value of the column.
- Should. Check. 2022. https://www.sqlbi.com/articles/introducing-horizontal-fusion-in-dax/
- When: Needing the horizontal fusion optimization while filtering multiple values of one column.
- Version: As of 2022; the limitation may be permanent or may be improved later.

**T07-A271-1.** A measure that adds up several measures, each filtering the same base aggregation differently, can evaluate the base measure once under one filter covering all values: one scan, where fusion still computes a column per measure. Later changes to those measures no longer reach it.
- Option. 2023. https://www.sqlbi.com/articles/optimizing-fusion-optimization-for-dax-measures/
- When: Measures that reference similar, differently filtered measures; first judge whether the extra speed is needed.
