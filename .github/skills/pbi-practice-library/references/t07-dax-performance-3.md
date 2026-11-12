# DAX performance and optimization

Part 3 of 3 of this topic. Covers: Iterators and materialization; Conditional logic and variables; Text search and its index.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### Iterators and materialization

**T07-A133-1.** Iterating only the distinct values a calculation uses limits materialization, which grows with iterator cardinality. Versus one row-level fact table iterator it can be slightly slower on floating point columns, faster on Fixed Decimal Number ones, and does not duplicate the measure's logic.
- Should. 2018. https://www.sqlbi.com/articles/optimizing-nested-iterators-in-dax/
- When: Nested iterators, or iterators that call measures, whenever such a reduction is possible.

**T07-A133-5.** When tuning DAX with nested iterators, balance the size of the materialization against the work done by the storage engine; do not simply push as much work as possible there. The cost comes from the cardinality materialized at the lowest level of context transition.
- Should. 2018. https://www.sqlbi.com/articles/optimizing-nested-iterators-in-dax/
- When: Expressions whose iterators reference measures or otherwise cause context transition.

**T07-A134-1.** Before rewriting an iteration over a large fact table to iterate distinct combinations of a few columns, run a query that compares the fact table's row count with the count of those combinations: a count far below the row count suggests a large possible gain.
- Should. 2018. https://www.sqlbi.com/articles/optimizing-dax-with-cardinality-estimation-computing-working-days/
- When: An iterator over a fact table returns the same result for all rows sharing those column values.

**T07-A134-2.** When an iterator's expression over a fact table depends on a few columns only, iterate the distinct combinations of those columns and weight each result by the count of fact rows for that combination. The optimizer often does not shrink the iteration by itself.
- Should. 2018. https://www.sqlbi.com/articles/optimizing-dax-with-cardinality-estimation-computing-working-days/
- When: Not needed when the expression uses no other fact column: the optimizer may already reduce the iteration.

**T07-A174-1.** When you optimize DAX, always check how many rows the formula engine iterates. Large iterations often come from careless handling of blanks: dimension combinations with no data that the engine must walk so that blank and zero stay equivalent.
- Must. 2019. https://www.sqlbi.com/articles/optimizing-conditions-involving-blank-values-in-dax/
- When: Optimizing any slow DAX measure or query.

**T07-A181-1.** FIRSTNONBLANK, FIRSTNONBLANKVALUE, LASTNONBLANK and LASTNONBLANKVALUE shorten code but must be used with care. They are iterators that evaluate their second argument row by row, often with a context transition, and can materialize data at the granularity of their first argument's column.
- Must. 2020. https://www.sqlbi.com/articles/optimizing-lastnonblank-and-lastnonblankvalue-calculations/
- When: Looking for a first, previous, next or last item while iterating a table.

**T07-A287-1.** Keep the expression an iterator evaluates within what the VertiPaq storage engine can compute, such as a plain multiplication of two columns: the engine then computes it in aggregated form, very fast, and such iterators need not be feared. It is not always possible.
- Should. 2023. https://www.sqlbi.com/articles/optimizing-callbacks-in-a-sumx-iterator/
- When: Iterators such as SUMX over model tables.

**T07-A287-3.** When performance matters, work toward fewer callbacks in DAX code, above all inside iterations over large tables. Removing every callback is hard, and callbacks used sensibly can still go with good performance.
- Should. 2023. https://www.sqlbi.com/articles/optimizing-callbacks-in-a-sumx-iterator/
- When: Performance-sensitive DAX; callbacks are an essential Tabular feature.

**T07-A372-6.** Read these as signs that a measure can probably be optimized: several levels of nested iterators; nested iterations over columns or tables of large cardinality, whose product leaves many rows to evaluate; CALCULATETABLE inside an iterator such as SUMX, which can build large temporary variables.
- Consider. 2026. https://www.sqlbi.com/articles/optimizing-dax-with-ai/
- When: Reviewing a measure that is functionally correct.

**T07-A372-7.** When a measure leans heavily on the formula engine, shrink the temporary tables it builds, for example by fetching only the historical rows inside the window the algorithm needs. Rows outside it are useless; in one case this gave the largest gain.
- Should. 2026. https://www.sqlbi.com/articles/optimizing-dax-with-ai/
- When: Look-backs over a fixed number of days; rows added only for the look-back are filtered out before aggregating.

**T07-A372-8.** Avoid calling SUMMARIZECOLUMNS inside a row context, even after a context transition: the interplay between its logic and the row and filter contexts is very hard to manage.
- Should. 2026. https://www.sqlbi.com/articles/optimizing-dax-with-ai/
- When: Iterators whose expression would build a table with SUMMARIZECOLUMNS.

### Conditional logic and variables

**T07-A137-1.** A variable helps when the repeats share one filter and row context, such as the condition and the result of an IF, also inside an iterator. The engine may reuse a measure result by itself, but not always; the gain shows on large iterated tables.
- Should. Check. 2018. https://www.sqlbi.com/articles/optimizing-duplicated-dax-expressions-using-variables/ ; https://www.sqlbi.com/articles/optimizing-if-and-switch-expressions-using-variables/
- When: A measure reference or sub-expression such as a CALCULATE is evaluated more than once in one context.
- Version: As of January 2018 the engine did not recognise such repeats; this could change.

**T07-A137-2.** Do not declare a variable before an IF or SWITCH when only one branch uses it; declare it inside that branch. A variable declared before the conditional is evaluated whatever the condition is, which loses short-circuit evaluation and can hurt performance severely.
- Must. 2018. https://www.sqlbi.com/articles/optimizing-if-and-switch-expressions-using-variables/
- When: Especially when disconnected slicers drive one measure that returns one of several measures.

**T07-A137-3.** A variable declared before an IF or SWITCH can be used in the first argument of that IF or SWITCH without any performance cost.
- Option. 2018. https://www.sqlbi.com/articles/optimizing-if-and-switch-expressions-using-variables/
- When: A value is needed by the condition of an IF or the tested expression of a SWITCH.

**T07-A128-1.** When the branches of an IF or SWITCH return one base measure under different filters, choose the filter value with the condition first, then evaluate the measure in a single CALCULATE. With one CALCULATE per branch the engine is likely to compute every branch.
- Should. 2018. https://www.sqlbi.com/articles/optimizing-mutually-exclusive-calculations/
- When: A condition picks a filtered variant of one measure; simple cases may gain nothing and the code gets harder.

**T07-A176-3.** Prefer strict (short-circuit) evaluation of IF for very complex branches, sparse results without an else branch, complex calculations or very selective conditions. Prefer eager evaluation when branches share a sub-expression, or for simple calculations and unselective conditions. Simplifications, not fixed rules.
- Should. 2019. https://www.sqlbi.com/articles/understanding-eager-vs-strict-evaluation-in-dax/
- When: Conditional expressions in DAX measures or queries; complex ones need deeper evaluation and testing.

**T07-A176-4.** For an IF inside an iteration over a large table, consider whether the engine will evaluate it strictly or eagerly. Strict evaluation is not always the more efficient, and on large queries or complex measures the gap between the modes can be very noticeable.
- Consider. 2019. https://www.sqlbi.com/articles/understanding-eager-vs-strict-evaluation-in-dax/
- When: An IF used inside an iteration over a large table.

**T07-A176-5.** Never choose strict or eager evaluation for a formula without proper testing, and give complex measures or queries a deeper evaluation first: the best formula for one model may not be the best for another.
- Must. 2019. https://www.sqlbi.com/articles/understanding-eager-vs-strict-evaluation-in-dax/
- When: Choosing between strict and eager evaluation of a conditional.

## Special-case techniques and facts

### Iterators and materialization

**T07-A044-3.** One way to remove zero denominators before a row-by-row division: a CALCULATE filter argument, or iterating a FILTER of the table, then the plain operator. The plan stays in the storage engine, without CALLBACKDATAID, and is cacheable; one test ran over twice as fast.
- Option. 2014. https://www.sqlbi.com/articles/divide-performance/
- When: Iterations over large tables; it might not work for complex formulas and models, so test both.
- Version: The plain operator needs its exception row in the brief (M502).

**T07-A102-1.** Number rows by an ordering rule, such as each customer's sales by order date, with RANKX over the relevant rows, not COUNTROWS over FILTER of earlier rows. FILTER rescans the table per row and can be very slow and memory-hungry; RANKX uses an optimized operator.
- Should. Check. 2017. https://www.sqlbi.com/articles/how-to-compute-index-numbers-at-top-speed/
- When: Index or ranking numbers in a calculated column or a query; results differ where rows tie.

**T07-A102-2.** An index made with RANKX and one made by counting preceding rows with COUNTROWS and FILTER can hold different numbers where rows tie on the ordering value. This mismatch is expected behaviour.
- Fact. 2017. https://www.sqlbi.com/articles/how-to-compute-index-numbers-at-top-speed/
- When: Switching an index calculation from COUNTROWS and FILTER to RANKX, on data that contains ties.

**T07-A133-2.** A measure called inside an iterator can hide an iterator of its own, often the innermost. Only that one reaches the storage engine; the outer ones run in the formula engine and can materialize as many rows as the iterated tables have existing combinations.
- Fact. 2018. https://www.sqlbi.com/articles/optimizing-nested-iterators-in-dax/
- When: Nested iterators whose innermost level is a measure reference.

**T07-A133-3.** One iterator over the fact table reading dimension attributes through RELATED has drawbacks: the called measure's logic must be copied in, and differing data types or complex expressions can cause a CallbackDataID per fact row. With Fixed Decimal Number, results can differ through rounding.
- Option. 2018. https://www.sqlbi.com/articles/optimizing-nested-iterators-in-dax/
- When: Replacing nested iterators over dimension tables that call a measure.

**T07-A133-4.** Turning a nested iterator that calls a measure into one row-by-row iterator can change the result when the model uses the Fixed Decimal Number (currency) type, because rounding takes place at different steps. With floating point Decimal Number values the results stay the same.
- Fact. 2018. https://www.sqlbi.com/articles/optimizing-nested-iterators-in-dax/
- When: Rewriting iterator-based calculations over currency columns.

**T07-A134-3.** When an iteration filters an intermediate table that grows with the gap between two dates, such as the dates from DATESBETWEEN, you can count the smaller complementary set, for example non-working days kept in a variable, and subtract it from the total number of days.
- Option. Check. 2018. https://www.sqlbi.com/articles/optimizing-dax-with-cardinality-estimation-computing-working-days/
- When: Long durations, such as several years; slower and harder to read when durations are a few days.

**T07-A134-5.** For a value complex to compute, such as working days between pairs of existing dates, prefer precomputing it for every existing input combination in a hidden calculated table; the measure then only retrieves it, for example with LOOKUPVALUE. Do not precompute just any value.
- Should. Check. 2018. https://www.sqlbi.com/articles/optimizing-dax-with-cardinality-estimation-computing-working-days/
- When: A measure's logic is complex and its inputs form existing combinations that a table can hold.
- Version: An unrelated table needs its brief row (relationships and dates, rule 4; M411), and M105 asks why DAX is needed.

**T07-A134-6.** When a measure retrieves precomputed values for many key combinations, it can join the iterated combinations to the precomputed table with NATURALLEFTOUTERJOIN, not call LOOKUPVALUE for each one. This cuts LOOKUPVALUE calls and allows more formula engine optimization.
- Option. 2018. https://www.sqlbi.com/articles/optimizing-dax-with-cardinality-estimation-computing-working-days/
- When: One measure iterates many key combinations; one test showed no visible gain, other data may differ.

**T07-A181-4.** Rewriting CALCULATE over LASTNONBLANK in the shorter LASTNONBLANKVALUE form does not necessarily make it faster: the iterator keeps the same cardinality and similar bottlenecks, and in one benchmark the LASTNONBLANKVALUE version was slower.
- Fact. 2020. https://www.sqlbi.com/articles/optimizing-lastnonblank-and-lastnonblankvalue-calculations/
- When: Retrieving a measure's value for the last or first non-blank item.

**T07-A181-5.** To find the previous date or order, prefer MAX over the matching fact table column, under a filter for earlier values, to LASTNONBLANK or LASTNONBLANKVALUE: much faster and lighter on query memory through less materialization, though simple reports may not show the gain.
- Should. 2020. https://www.sqlbi.com/articles/optimizing-lastnonblank-and-lastnonblankvalue-calculations/
- When: Only when having fact rows is enough to count an item as non-blank.

**T07-A181-6.** To return a measure for the previous item found with MAX, you can turn that value into a filter with TREATAS on the target column and evaluate the measure under it, not LASTNONBLANKVALUE. Less materialization helps the measure scale with many concurrent users.
- Option. 2020. https://www.sqlbi.com/articles/optimizing-lastnonblank-and-lastnonblankvalue-calculations/
- When: Only when having fact rows is enough to count an item as non-blank.

**T07-A287-2.** A function the storage engine cannot run, such as ROUND, placed in the expression of an iterator brings in the formula engine through callbacks. On a large table this can multiply the storage engine CPU cost by a very large factor.
- Fact. 2023. https://www.sqlbi.com/articles/optimizing-callbacks-in-a-sumx-iterator/
- When: Iterating large tables with a per-row expression the storage engine cannot execute.

**T07-A287-4.** One way to avoid computing a formula-engine-only function at query time is to store its result in a calculated column of the fact table. It is rarely the right choice: the fact table grows by a column that can be large.
- Option. 2023. https://www.sqlbi.com/articles/optimizing-callbacks-in-a-sumx-iterator/
- When: An iterator applies a function the storage engine cannot run to a fact table column.
- Version: Only when Power Query cannot supply the value, with its CalculatedReason annotation (storage and security, rule 17; M105).

**T07-A287-5.** When an iterator over a large table applies a formula-engine-only function to a column, iterate that column's distinct values, aggregate the other columns per value through context transition, and apply the function once per value. Callbacks disappear and the cache is used far better.
- Should. 2023. https://www.sqlbi.com/articles/optimizing-callbacks-in-a-sumx-iterator/
- When: The transformed column has far fewer distinct values than the table has rows.

**T07-A287-6.** In the distinct-values iterator rewrite, moving the per-value calculations into variables that build the table with ADDCOLUMNS over SUMMARIZE is slower than the single expression: ADDCOLUMNS always computes both the added columns and the distinct values it extends, a second fact table scan.
- Fact. 2023. https://www.sqlbi.com/articles/optimizing-callbacks-in-a-sumx-iterator/
- When: Refactoring the distinct-values iterator for readability; a rare case where variables harm performance.

**T07-A372-9.** OFFSET is one way to fetch the previous row within a partition, such as the previous order date of the same customer.
- Option. 2026. https://www.sqlbi.com/articles/optimizing-dax-with-ai/
- When: Calculations that compare each row with the one before it within a group.
- Version: Called a new function when written, which is why it was expected to be well optimized.

**T07-A372-10.** Rather than computing a measure for every row of a large table of candidate combinations, you can filter the candidates first, then compute the measure once with CALCULATE, passing the filtered table as a filter. In one set of tests this version won overall.
- Option. 2026. https://www.sqlbi.com/articles/optimizing-dax-with-ai/
- When: Measures that build a table of combinations, such as customer and date pairs, then keep some.

### Conditional logic and variables

**T07-A127-2.** The optimizer does not detect that references to one measure in one filter context return the same value. Each, as in the arguments of an IF, can trigger its own evaluation and storage engine request, even for identical branches; the DAX cache is storage-engine only.
- Fact. Check. 2018. https://www.sqlbi.com/articles/optimizing-duplicated-dax-expressions-using-variables/ ; https://www.sqlbi.com/articles/optimizing-if-conditions-using-variables/
- When: One measure appears several times in a single filter context, for example in an IF.
- Version: Described as of January 2018; it could change.

**T07-A137-4.** Short-circuit evaluation in IF and SWITCH works by changing the filter context of the branches. That change does not reach variables declared before the IF or SWITCH, so those variables, and the measures they reference, are all evaluated whichever branch is chosen.
- Fact. 2018. https://www.sqlbi.com/articles/optimizing-if-and-switch-expressions-using-variables/
- When: A measure declares branch results in variables ahead of the conditional, for example behind a disconnected slicer.

**T07-A128-3.** When IF picks one of two measures that are the same base measure under different filters, the query plan is likely to compute both, even if the report shows only one. Short-circuit evaluation may happen in simple expressions but is often unavailable in complex reports.
- Fact. 2018. https://www.sqlbi.com/articles/optimizing-mutually-exclusive-calculations/
- When: Conditional measures whose branches are differently filtered versions of one base measure.

**T07-A128-4.** IF and SWITCH return scalar values only. They cannot choose which table, such as the dates produced by one of several time intelligence functions, becomes the filter of a CALCULATE.
- Fact. 2018. https://www.sqlbi.com/articles/optimizing-mutually-exclusive-calculations/
- When: Building a single CALCULATE filter whose content depends on a condition.

**T07-A128-5.** To apply one of several date ranges chosen by a condition inside a single CALCULATE, one approach is to compute the first and the last date with IF or SWITCH and pass both to one DATESBETWEEN used as the filter, stored in a variable.
- Option. 2018. https://www.sqlbi.com/articles/optimizing-mutually-exclusive-calculations/
- When: A measure switches among periods picked in a slicer; the gain is expected to grow with database size.

**T07-A334-1.** A top-level IF in a measure does not run once per group: the engine computes the condition's inputs for all groups, sorts them into true and false sets in the formula engine, then queries the storage engine per branch, possibly with several fact table scans.
- Fact. 2025. https://www.sqlbi.com/articles/understanding-how-dax-evaluates-if-statements/
- When: IF as a top-level function of a measure; inside an iteration behaviour may differ.

**T07-A334-3.** For a top-level IF whose condition and both branches use one measure, you can assign it to a variable before the IF: the engine computes it for all groups in one storage engine query. Not always better: measure complexity, model size and grouping-column cardinality decide.
- Option. 2025. https://www.sqlbi.com/articles/understanding-how-dax-evaluates-if-statements/
- When: A measure whose top-level IF reuses one measure in its condition and branches.

**T07-A174-2.** A measure that returns a value for combinations without fact rows forces the engine to evaluate the full cross-join of the grouping columns. One cause: blank compares as zero, so `x >= 0` is true for every empty combination. IF itself is not the cost.
- Fact. 2019. https://www.sqlbi.com/articles/optimizing-conditions-involving-blank-values-in-dax/
- When: Grouping by columns of different tables, where auto-exist does not apply.

**T07-A174-3.** When zero results do not matter, one fix for a slow conditional measure is to test strictly greater than zero, not greater than or equal to zero: blanks then fail the condition and the engine evaluates only the relevant rows.
- Option. 2019. https://www.sqlbi.com/articles/optimizing-conditions-involving-blank-values-in-dax/
- When: A condition that blank, read as zero, satisfies, and zeros need not be kept.

**T07-A174-4.** One possible fix is an explicit outer test, built with NOT and ISBLANK, that discards blank aggregations before the condition is checked. The code is longer, but it helps the optimizer choose a fast plan, nearly as fast as a strict comparison.
- Option. 2019. https://www.sqlbi.com/articles/optimizing-conditions-involving-blank-values-in-dax/
- When: A conditional measure slow because blanks satisfy its condition and missing combinations get evaluated.

**T07-A174-5.** One option for a conditional measure slowed by blanks: hold the aggregation in a variable used in both the condition and the result of IF. The engine then aggregates all rows in one block first, so only existing combinations return values; fastest version tested.
- Option. 2019. https://www.sqlbi.com/articles/optimizing-conditions-involving-blank-values-in-dax/
- When: A conditional measure slow because blanks satisfy its condition, even with a greater-or-equal-to-zero test.

**T07-A176-1.** Where eager evaluation of a conditional suits a formula better, consider IF.EAGER in place of IF: it enforces eager evaluation without rewriting the expression with variables.
- Consider. 2019. https://www.sqlbi.com/articles/understanding-eager-vs-strict-evaluation-in-dax/
- When: A formula with a conditional for which eager evaluation is the more convenient mode.
- Version: IF.EAGER was introduced as a new function in January 2020.

**T07-A176-2.** To get eager evaluation of a conditional, you can compute every value its branches need into variables before the IF, which then only picks among stored values. In one example this retrieved all the measures in a single storage engine query.
- Option. 2019. https://www.sqlbi.com/articles/understanding-eager-vs-strict-evaluation-in-dax/
- When: Eager evaluation is the better evaluation mode for the conditional.

**T07-A251-2.** Keep in mind that a SWITCH testing a column only cross-filtered through another column can cost extra formula engine work: not knowing one value remains, the engine prepares every branch. Overhead grows with branches and their measures; storage engine requests stay optimized.
- Consider. 2022. https://www.sqlbi.com/articles/understanding-the-optimization-of-switch/
- When: For example a SWITCH over a hidden sort index while the slicer filters the name column.

**T07-A251-5.** A SWITCH over SELECTEDVALUE of a column loses its formula engine optimization when that column gets two filters in one visual, such as a page filter and a slicer, even if one value remains: the engine then evaluates branches that return nothing.
- Fact. Check. 2022. https://www.sqlbi.com/articles/understanding-the-optimization-of-switch/
- When: Report users' filters create it, not the model author; storage engine requests stay optimized.
- Version: Consistent behaviour in 2022 that could change and improve in later versions.

**T07-A251-6.** If a page filter that hides items of a selector slicer slows a SWITCH measure down, a report-side workaround is to put that exclusion as a visual-level filter on the slicer: the visual then receives only the slicer selection and gets the optimized plan.
- Option. Check. 2022. https://www.sqlbi.com/articles/understanding-the-optimization-of-switch/
- When: A page filter and a slicer both filter the column SELECTEDVALUE reads inside a SWITCH.
- Version: Behaviour seen in 2022; check that it still applies.

**T07-A272-1.** The column to test is the one the slicer shows, not its sort-by column, with one value selected and no other filter on it; only the chosen branch then reaches the query plans. Exception: a column named in the shown column's Group By Columns property.
- Should. 2022. https://www.sqlbi.com/articles/understanding-the-optimization-of-switch/ ; https://www.sqlbi.com/articles/optimizing-switch-on-slicer-selection-with-group-by-columns/
- When: A slicer passing a parameter into a measure that branches with SWITCH.

**T07-A272-2.** If slicer-driven SWITCH logic must test a column other than the one shown, such as a hidden index, one workaround is to set the shown column's Group By Columns property to it: Power BI filters that column directly. SELECTEDVALUE can no longer read the name.
- Option. Check. 2022. https://www.sqlbi.com/articles/understanding-the-optimization-of-switch/ ; https://www.sqlbi.com/articles/optimizing-switch-on-slicer-selection-with-group-by-columns/
- When: Existing models consumed only by Power BI, where changing the code late would be expensive.
- Version: Power BI only: MDX queries, so Excel reports, do not support Group By Columns. Workaround added in March 2023.

### Text search and its index

**T07-A275-1.** Without the text search index, a contains-style filter (SEARCH or CONTAINSSTRING) on a text column with many distinct values is evaluated by the formula engine for every distinct value. The storage engine cache does not remove that cost: each query and visual pays again.
- Fact. Check. 2023. https://www.sqlbi.com/articles/optimizing-text-search-in-dax/
- When: Columns with a large dictionary: a few thousand unique values may already hurt, hundreds of thousands certainly.
- Version: Power BI Desktop before October 2022, and on-premises Analysis Services older than 2022 without later updates: every text column.

**T07-A275-2.** To get the automatic text search index for SEARCH and CONTAINSSTRING, make sure every value of the searched column holds ASCII characters only: a single non-ASCII character anywhere in the column stops the index from being built.
- Must. Check. 2023. https://www.sqlbi.com/articles/optimizing-text-search-in-dax/
- When: Columns filtered with SEARCH or CONTAINSSTRING, for example through contains filters in a report.
- Version: October 2022 onward: Azure Analysis Services and Power BI, not SQL Server Analysis Services 2022; a 2026 preview persists it.

**T07-A275-3.** Keep the ? wildcard out of SEARCH and CONTAINSSTRING search strings when you rely on the text search index: the index supports only the * wildcard, and with ? the engine falls back to a CallbackDataID plan.
- Must. Check. 2023. https://www.sqlbi.com/articles/optimizing-text-search-in-dax/
- When: Text searches on columns meant to benefit from the automatic text search index.
- Version: October 2022 onward: Azure Analysis Services and Power BI, not SQL Server Analysis Services 2022; a 2026 preview persists it.

**T07-A275-4.** When a searched text column holds accented letters, you can add a second column with the diacritics replaced by plain letters, for example in Power Query, keep the original, and search the new column so that the index can be used.
- Option. Check. 2023. https://www.sqlbi.com/articles/optimizing-text-search-in-dax/
- When: Non-ASCII characters keep a text column from being indexed. Searching the plain copy can match other rows: check first.
- Version: October 2022 onward: Azure Analysis Services and Power BI, not SQL Server Analysis Services 2022; a 2026 preview persists it.

**T07-A275-5.** Be aware that searching an ASCII-converted copy of a text column can return other rows, and so other report totals, than searching the original: SEARCH and CONTAINSSTRING are accent-sensitive, so removing diacritics changes which values match.
- Consider. 2023. https://www.sqlbi.com/articles/optimizing-text-search-in-dax/
- When: A column with diacritics is replaced by an ASCII-only version for text search.

**T07-A275-6.** The automatic text search index is case-insensitive. Only SEARCH and CONTAINSSTRING benefit from it; FIND and CONTAINSSTRINGEXACT do not use it.
- Fact. 2023. https://www.sqlbi.com/articles/optimizing-text-search-in-dax/
- When: Choosing a text search function for a filter on a large text column.
- Version: October 2022 onward: Azure Analysis Services and Power BI, not SQL Server Analysis Services 2022; a 2026 preview persists it.

**T07-A275-7.** When you benchmark SEARCH or CONTAINSSTRING queries with a cleared cache, find the index build in the timings, shown as formula engine activity before the matching storage engine request, and leave its time out of the typical execution time you report.
- Must. Check. 2023. https://www.sqlbi.com/articles/optimizing-text-search-in-dax/
- When: Performance tests with the cache cleared on columns that get the text search index.
- Version: October 2022 onward: Azure Analysis Services and Power BI, not SQL Server Analysis Services 2022; a 2026 preview persists it.

**T07-A275-8.** Take into account that the first query needing the text search index builds it. In models refreshed or evicted from memory often, that build can cost users more than the CallbackDataID plan it replaces: the index pays off only when ready most of the time.
- Consider. Check. 2023. https://www.sqlbi.com/articles/optimizing-text-search-in-dax/
- When: Models with frequent refreshes or frequent eviction from memory.
- Version: October 2022 onward: Azure Analysis Services and Power BI, not SQL Server Analysis Services 2022; a 2026 preview persists it.

**T07-A275-9.** To spare the first user after a refresh the wait for the text search index, you can run queries that use SEARCH or CONTAINSSTRING on the column right after the refresh; the index then serves the user queries that follow.
- Option. Check. 2023. https://www.sqlbi.com/articles/optimizing-text-search-in-dax/
- When: Some specific scenarios with columns searched through SEARCH or CONTAINSSTRING.
- Version: October 2022 onward: Azure Analysis Services and Power BI, not SQL Server Analysis Services 2022; a 2026 preview persists it.

**T07-A275-10.** The text search index is lost on an explicit cache clear or whenever the database leaves memory: a restart of Analysis Services or Power BI Desktop, a refresh, eviction from memory in the Power BI service, and possibly memory pressure on Analysis Services.
- Fact. Check. 2023. https://www.sqlbi.com/articles/optimizing-text-search-in-dax/
- When: Relying on the text search index for SEARCH or CONTAINSSTRING filters.
- Version: October 2022 onward: Azure Analysis Services and Power BI, not SQL Server Analysis Services 2022; a 2026 preview persists it.

**T07-A275-11.** The cost of building the text search index falls on the first query calling SEARCH or CONTAINSSTRING on the column. A build that takes more than 25 seconds is abandoned, and that query runs without the index.
- Fact. 2023. https://www.sqlbi.com/articles/optimizing-text-search-in-dax/
- When: The first SEARCH or CONTAINSSTRING query on a column after the index was lost.
- Version: October 2022 onward: Azure Analysis Services and Power BI, not SQL Server Analysis Services 2022; a 2026 preview persists it.

**T07-A275-12.** To check whether the service supports the text search index, look for a Search function in the xmSQL of a query whose search string holds a wildcard: xmSQL shows that function only when the index is supported.
- Should. Check. 2023. https://www.sqlbi.com/articles/optimizing-text-search-in-dax/
- When: Queries using SEARCH or CONTAINSSTRING with a wildcard in the search string.
- Version: October 2022 onward: Azure Analysis Services and Power BI, not SQL Server Analysis Services 2022; a 2026 preview persists it.

**T07-A275-13.** To measure the real benefit of the text search index, you can keep the cache, and so the index, after the first run and repeat the test with a different search string: running the identical query again only returns the storage engine cache result.
- Option. 2023. https://www.sqlbi.com/articles/optimizing-text-search-in-dax/
- When: Benchmarking SEARCH or CONTAINSSTRING filters on a column that gets the text search index.
- Version: October 2022 onward: Azure Analysis Services and Power BI, not SQL Server Analysis Services 2022; a 2026 preview persists it.

**T07-A275-14.** A query plan without a SEARCH node is no proof the text search index went unused. Without wildcards, index use shows as a list of matching values in the xmSQL, with no earlier storage engine query reading the column; some engine versions omit the node.
- Fact. Check. 2023. https://www.sqlbi.com/articles/optimizing-text-search-in-dax/
- When: Reading Server Timings and query plans to confirm whether the text search index was used.
- Version: Azure Analysis Services might not show the SEARCH node, depending on the engine version.
