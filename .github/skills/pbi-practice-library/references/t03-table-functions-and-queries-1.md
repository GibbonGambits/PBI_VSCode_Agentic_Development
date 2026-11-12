# DAX table functions and queries

Part 1 of 2 of this topic. Covers: Grouping and adding columns; Writing DAX queries; Filter and text conditions.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### Grouping and adding columns

**T03-A007-8.** Consider ADDCOLUMNS rather than SUMMARIZE when columns of a query result must be computed under different filter contexts, or when the writer reasons in MDX terms. SUMMARIZE applies the filter context already on its table before grouping and computing the columns.
- Consider. 2011. https://www.sqlbi.com/articles/converting-mdx-to-dax-first-steps/
- When: Shaping a query result; SUMMARIZE can still be exactly what is needed, and feels natural from SQL.

**T03-A048-2.** Avoid using SUMMARIZE to produce subtotals. The feature works, but the semantics of SUMMARIZE are convoluted enough that the results may be unexpected; only its grouping is safe.
- Should. 2021. https://www.sqlbi.com/articles/all-the-secrets-of-summarize/
- When: A query or formula that would use the subtotal feature of SUMMARIZE.

**T03-A048-3.** When ADDCOLUMNS computes a column over rows grouped by SUMMARIZE, wrap every aggregation such as SUM in CALCULATE, so that a context transition takes place. ADDCOLUMNS gives only a row context; without CALCULATE the aggregation does not see the current group.
- Must. 2012. https://www.sqlbi.com/articles/best-practices-using-summarize-and-addcolumns/ ; https://www.sqlbi.com/articles/introducing-summarizecolumns/ ; https://www.sqlbi.com/articles/all-the-secrets-of-summarize/
- When: ADDCOLUMNS over SUMMARIZE; not needed for a scalar expression that only reads a column of the SUMMARIZE output.

**T03-A048-5.** Give SUMMARIZE the smallest possible table as its first argument, for example the dimension table and not the fact table, so that clusters are narrower. Clusters from a large expanded table make huge filters, large materialization and poor performance.
- Should. 2021. https://www.sqlbi.com/articles/all-the-secrets-of-summarize/
- When: Choosing the base table of SUMMARIZE; grouping the dimension also returns items absent from the fact table.

**T03-A046-1.** When ADDCOLUMNS iterates the values of a grouping column to add an aggregated column, wrap the aggregation in CALCULATE, so the row context of the iteration becomes a filter context. SUMMARIZE evaluates its expressions in each group's filter context; ADDCOLUMNS provides only a row context.
- Must. 2014. https://www.sqlbi.com/articles/from-sql-to-dax-grouping-data/
- When: Grouping with ADDCOLUMNS over VALUES of a column instead of with SUMMARIZE.

**T03-A071-8.** Use GROUPBY only for grouping what another calculation has already materialized, such as the output of SUMMARIZE. GROUPBY does not benefit from VertiPaq: the formula engine materializes the rows it has to group.
- Should. 2016. https://www.sqlbi.com/articles/nested-grouping-using-groupby-vs-summarize/
- When: Choosing GROUPBY for a grouping operation.

**T03-A283-1.** For grouping by model columns, SUMMARIZE with ADDCOLUMNS is also preferred to GROUPBY: GROUPBY always materializes the whole table it groups, so the wrong choice costs a lot of performance.
- Should. 2023. https://www.sqlbi.com/articles/differences-between-groupby-and-summarize/
- When: Grouping by model columns or columns already present in the query.

**T03-A106-1.** When several new columns of a table expression share sub-expressions, an alternative to ADDCOLUMNS is GENERATE whose second argument declares variables in the row context and returns them through one ROW call, so every column can use every variable.
- Option. 2017. https://www.sqlbi.com/articles/using-generate-and-row-instead-of-addcolumns-in-dax/
- When: Table expressions in which several column expressions repeat the same logic.

**T03-A106-5.** With the GENERATE and ROW pattern, variables can be declared only for expressions used more than once, with the others written directly inside ROW, to shorten the code; performance is the same. One variable per column is easier to read and change.
- Option. 2017. https://www.sqlbi.com/articles/using-generate-and-row-instead-of-addcolumns-in-dax/
- When: Tables with many columns and few shared expressions.

**T03-A011-1.** Grouping with SUMMARIZE is the DAX counterpart of SQL SELECT DISTINCT, and the more efficient way to get the distinct combinations of some columns: write such a query with it.
- Should. 2020. https://www.sqlbi.com/articles/from-sql-to-dax-projection/
- When: Projecting columns of a plain table reference while removing duplicate rows.

**T03-A011-4.** Use SELECTCOLUMNS or ADDCOLUMNS for a projection in which duplicate rows of the source must stay: both return every row of the source table expression, duplicates included.
- Should. 2020. https://www.sqlbi.com/articles/from-sql-to-dax-projection/
- When: Projections that must not remove duplicate rows; for a distinct result use SUMMARIZE.
- Version: SELECTCOLUMNS was introduced in 2015.

### Writing DAX queries

**T03-A104-1.** Variables are also worth considering in DAX queries written against a model, to make the query code simpler.
- Consider. 2017. https://www.sqlbi.com/articles/defining-variables-in-dax-queries/
- When: Writing DAX queries against a model.

**T03-A104-2.** In a query batch with several EVALUATE statements, consider declaring the variables that more than one of them needs a single time, in DEFINE ahead of the first EVALUATE. A variable repeated inside each EVALUATE is evaluated once per statement.
- Consider. 2017. https://www.sqlbi.com/articles/defining-variables-in-dax-queries/
- When: Batches that return several result sets through several EVALUATE statements.

### Filter and text conditions

**T03-A012-7.** For performance, avoid CONTAINSSTRING and SEARCH unless a wildcard pattern is really needed. To test whether a text starts with a given value, use LEFT instead of SEARCH; that may be 5 to 10 times faster.
- Should. Check. 2011. https://www.sqlbi.com/articles/from-sql-to-dax-string-comparison/
- When: Filtering or comparing text in DAX.
- Version: Speed figure reported in 2011.

**T03-A045-2.** Never treat CALCULATETABLE as automatically the better choice over FILTER. Internally it executes at least one FILTER itself, so what usually decides speed is how fine-grained those inner filters are, though the engine may optimise beyond that.
- Must. 2014. https://www.sqlbi.com/articles/from-sql-to-dax-filtering-data/
- When: Choosing between FILTER and CALCULATETABLE to filter a table.

**T03-A045-4.** When a row filter contains nested calculations, consider CALCULATETABLE instead of plain FILTER: put shared filters, such as a calendar year, in its filter arguments, so the inner CALCULATE expressions inherit them instead of repeating them. Those filters change the context of every nested expression.
- Consider. 2014. https://www.sqlbi.com/articles/from-sql-to-dax-filtering-data/
- When: Filtering a table by conditions that evaluate aggregations.

**T03-A045-5.** Pay close attention to filters set by an outer CALCULATETABLE or CALCULATE: they alter the filter context of every expression nested inside them.
- Consider. 2014. https://www.sqlbi.com/articles/from-sql-to-dax-filtering-data/
- When: Relying on an outer CALCULATETABLE or CALCULATE to pass filters to inner expressions.

**T03-A046-4.** A filter on a calculated result is evaluated by the formula engine. Only a condition on an aggregated value, which cannot be a filter argument of CALCULATE or CALCULATETABLE, requires FILTER over the computed result.
- Should. 2014. https://www.sqlbi.com/articles/from-sql-to-dax-grouping-data/
- When: Choosing between a filter argument and FILTER over a computed result.

**T03-A070-4.** Avoid filtering a column on a list of values by testing membership in an inline DATATABLE: its query plan is much slower than the same condition written with the OR operator.
- Should. Check. 2016. https://www.sqlbi.com/articles/create-static-tables-in-dax-using-the-datatable-function/
- When: Filtering on a list of values; the DATATABLE form is shorter only for a very long list.
- Version: Stated for the 2016 engine; a 2018 update points to the IN operator with a braces list.

**T03-A226-1.** CONTAINS is a reasonable choice for checking whether at least one row of a table matches given values on some of its columns. It is shorter than ISEMPTY over FILTER, may be faster in complex cases, and reads more easily than IN or TREATAS.
- Option. 2021. https://www.sqlbi.com/articles/using-contains-in-dax/
- When: An existence check on some columns of one table; not the virtual relationship pattern, where TREATAS can be better.

**T03-A226-5.** When optimising code where CONTAINS sits inside an iterator, aim to remove the iterator by using a table function, not to swap CONTAINS for another predicate. No predicate is faster than CONTAINS, while the engine optimises table functions better than iterators.
- Should. 2021. https://www.sqlbi.com/articles/using-contains-in-dax/
- When: Code that calls CONTAINS inside an iterator.

## Special-case techniques and facts

### Grouping and adding columns

**T03-A007-2.** When SUMMARIZE groups a table that CALCULATETABLE filtered on a column, a measure in an added column cannot override that filter with its own CALCULATE on the same column. Only groups with data under the outer filter return, with a blank for that measure.
- Fact. 2011. https://www.sqlbi.com/articles/converting-mdx-to-dax-first-steps/
- When: A query filters the table argument of SUMMARIZE through CALCULATETABLE and its measures filter the same column.

**T03-A022-6.** To match SUMMARIZE over a filtered table with ADDCOLUMNS: store the filtered table in a variable, group it with SUMMARIZE, and compute the added column with CALCULATE, passing the variable inside KEEPFILTERS as a filter argument. This is more complex and performs no better.
- Option. 2012. https://www.sqlbi.com/articles/best-practices-using-summarize-and-addcolumns/
- When: SUMMARIZE groups a filtered table and its computed column would move to ADDCOLUMNS.

**T03-A048-4.** In an expression computed inside SUMMARIZE, each group is filtered on every column of the clustered table, including related-table columns reached by table expansion, not only on the group-by columns. REMOVEFILTERS on the group-by column therefore does not return the total for all values.
- Fact. Check. 2021. https://www.sqlbi.com/articles/all-the-secrets-of-summarize/
- When: Expressions computed inside SUMMARIZE, especially ones that change the filter on the grouped columns.

**T03-A048-6.** SUMMARIZE can group only by columns of its base table's expanded table: columns of tables reached through regular many-to-one relationships. It does not work across limited relationships, such as many-to-many cross-filter or cross-island ones. An older view held that it follows relationships in both directions.
- Fact. 2021. https://www.sqlbi.com/articles/all-the-secrets-of-summarize/ ; https://www.sqlbi.com/articles/converting-mdx-to-dax-first-steps/
- When: Grouping by columns of related tables with SUMMARIZE.
- Version: The both-directions view dates from 2011; the expanded-table limit from 2021.

**T03-A048-7.** When SUMMARIZE groups a fact table by a dimension column, only combinations present in the fact table come back, so dimension items without transactions, such as products never sold, are missing from the result.
- Fact. 2021. https://www.sqlbi.com/articles/all-the-secrets-of-summarize/
- When: Choosing whether to run SUMMARIZE over the fact table or over the dimension table.

**T03-A048-8.** SUMMARIZE is the only DAX function that creates both a row context, holding the group-by columns, and a filter context, holding all cluster columns, while computing its columns. A CALCULATE inside SUMMARIZE therefore also triggers a context transition on the group-by columns.
- Fact. Check. 2021. https://www.sqlbi.com/articles/all-the-secrets-of-summarize/
- When: Expressions computed inside SUMMARIZE.

**T03-A048-10.** One way to make SUMMARIZE less complex is to shrink its clusters to the group-by columns only, for instance by giving the outer SUMMARIZE an inner SUMMARIZE of just those columns as its base table. Removing a group-by filter then behaves intuitively.
- Option. 2021. https://www.sqlbi.com/articles/all-the-secrets-of-summarize/
- When: Expressions are computed inside SUMMARIZE; a step towards replacing the outer SUMMARIZE with ADDCOLUMNS.

**T03-A046-2.** Grouping a table by a related lookup column with SUMMARIZE differs from iterating that column's values with ADDCOLUMNS. SUMMARIZE keeps only the lookup values reached from the rows of its first argument; the ADDCOLUMNS form also returns lookup values with no matching rows.
- Fact. 2014. https://www.sqlbi.com/articles/from-sql-to-dax-grouping-data/
- When: Grouping by a column of a different, related table than the one being aggregated.

**T03-A071-1.** Simple aggregation functions such as MAX work only on physical columns of the model. Applying one to a column computed in the same query, such as a column added by ADDCOLUMNS and then grouped again with SUMMARIZE, raises an error.
- Fact. 2016. https://www.sqlbi.com/articles/nested-grouping-using-groupby-vs-summarize/
- When: Nested grouping where an outer level aggregates a value calculated by an inner grouping.

**T03-A071-2.** Consider GROUPBY in place of an ADDCOLUMNS and SUMMARIZE combination when an iterator must work on the rows of each group. The combination is verbose and inefficient: each extra aggregate, such as a minimum and a maximum, repeats the inner SUMMARIZE.
- Consider. 2016. https://www.sqlbi.com/articles/nested-grouping-using-groupby-vs-summarize/
- When: Grouping an already materialized result where the rows of every group are iterated.

**T03-A071-3.** In a nested grouping where an outer level aggregates a column calculated by an inner grouping, the outer level must be a GROUPBY that aggregates that column with an X iterator, such as MAXX, over CURRENTGROUP. The innermost grouping may still use SUMMARIZE.
- Must. 2016. https://www.sqlbi.com/articles/nested-grouping-using-groupby-vs-summarize/
- When: Nested grouping operations that aggregate values calculated by an inner grouping.

**T03-A071-4.** CURRENTGROUP must be called inside the GROUPBY call itself. A column based on CURRENTGROUP cannot be added by wrapping the GROUPBY result in ADDCOLUMNS.
- Must. 2016. https://www.sqlbi.com/articles/nested-grouping-using-groupby-vs-summarize/
- When: Adding columns computed over the rows of each group of a GROUPBY.

**T03-A071-5.** Do not call CALCULATE or reference a measure inside a GROUPBY expression. A column that needs a filter context must be computed with ADDCOLUMNS; ADDCOLUMNS can be dropped only when the calculation is written as an explicit aggregation over CURRENTGROUP.
- Must. 2016. https://www.sqlbi.com/articles/nested-grouping-using-groupby-vs-summarize/
- When: Computing columns in a grouping built with GROUPBY.

**T03-A071-6.** Write every expression column of GROUPBY as an aggregation over CURRENTGROUP. A value that depends only on a grouping column is also wrapped in an iterator, such as MAXX over CURRENTGROUP; other expressions can give unexpected results.
- Should. 2016. https://www.sqlbi.com/articles/nested-grouping-using-groupby-vs-summarize/
- When: Any expression column added in a GROUPBY call.
- Version: A 2022 update: GROUPBY expressions that do not include CURRENTGROUP are no longer supported.

**T03-A071-7.** To leave out groups whose aggregation over CURRENTGROUP is blank, apply FILTER to the result of GROUPBY and exclude those rows.
- Should. Check. 2016. https://www.sqlbi.com/articles/nested-grouping-using-groupby-vs-summarize/
- When: A GROUPBY output that should not show rows whose aggregated value is blank.
- Version: Since 2022, Power BI and Azure Analysis Services keep such rows with a blank; GROUPBY removed them before.

**T03-A071-9.** When a GROUPBY column takes MAXX over CURRENTGROUP of a value that can be blank, and every group must show a value, one way is to make the iterated expression return 0 instead of BLANK.
- Option. Check. 2016. https://www.sqlbi.com/articles/nested-grouping-using-groupby-vs-summarize/
- When: A GROUPBY aggregation returns BLANK for some groups that should still appear with a value.
- Version: Written when GROUPBY dropped blank groups; since 2022 Power BI and Azure Analysis Services keep them as blank.

**T03-A283-2.** To group by a column computed in the query or expression, not stored in the model, avoid SUMMARIZE and use GROUPBY with CURRENTGROUP. SUMMARIZE groups such a column through clustering, which mostly gives unexpected results; GROUPBY groups without clustering.
- Should. 2021. https://www.sqlbi.com/articles/all-the-secrets-of-summarize/ ; https://www.sqlbi.com/articles/differences-between-groupby-and-summarize/
- When: Grouping a small intermediate table by a column computed on the fly, with a simple row-by-row aggregation.

**T03-A283-4.** In GROUPBY, the expression that iterates CURRENTGROUP cannot contain a context transition. Existing measures cannot be referenced there; their logic must be rewritten as a plain aggregation over the grouped rows.
- Fact. 2023. https://www.sqlbi.com/articles/differences-between-groupby-and-summarize/
- When: Adding columns to the result of GROUPBY.

**T03-A283-5.** GROUPBY is the only DAX function able to group and compute values over a table whose columns carry no data lineage, such as a table built locally in the query.
- Fact. 2023. https://www.sqlbi.com/articles/differences-between-groupby-and-summarize/
- When: Grouping a table whose columns have no lineage.

**T03-A283-6.** To group a large table by a column derived from a model column, first group on the model column with ADDCOLUMNS and SUMMARIZE, computing the measure there; add the derived column to that small result; then apply GROUPBY, aggregating the precomputed value through CURRENTGROUP.
- Should. 2023. https://www.sqlbi.com/articles/differences-between-groupby-and-summarize/
- When: Grouping a large table by a local column computed from a model column, such as a size band.

**T03-A106-2.** A variable is visible only in the expression where it is declared. In a nested chain of ADDCOLUMNS or SELECTCOLUMNS calls, the expression of one column cannot use a variable declared for another column.
- Fact. 2017. https://www.sqlbi.com/articles/using-generate-and-row-instead-of-addcolumns-in-dax/
- When: Nested ADDCOLUMNS or SELECTCOLUMNS calls that try to share intermediate values through variables.

**T03-A011-2.** Keep DISTINCT over SELECTCOLUMNS as a fallback for removing duplicate rows from a projection: it is slower than SUMMARIZE, so use it only where SUMMARIZE cannot be used.
- Should. 2020. https://www.sqlbi.com/articles/from-sql-to-dax-projection/
- When: SUMMARIZE cannot apply, for instance because the first argument is a complex table expression, not a plain table.
- Version: SELECTCOLUMNS was introduced in 2015.

**T03-A011-3.** For distinct rows with renamed columns, wrap the SUMMARIZE result in SELECTCOLUMNS and rename there: SUMMARIZE cannot rename its grouping columns, and this form gives the best performance.
- Should. 2020. https://www.sqlbi.com/articles/from-sql-to-dax-projection/
- When: A distinct projection whose output columns need names different from the source columns.
- Version: SELECTCOLUMNS was introduced in 2015.

**T03-A337-1.** When SUMMARIZE groups the one-side table of a regular relationship and the blank row of an invalid relationship must be in the result, pass that table wrapped in VALUES. Without VALUES the blank row is left out and totals come out lower.
- Should. 2025. https://www.sqlbi.com/articles/using-values-in-summarize/
- When: Uncommon: the one-side table is the first argument of SUMMARIZE and the blank row is required.

**T03-A337-2.** With the one-side table of a regular relationship as first argument, SUMMARIZE returns no blank row for an invalid relationship, so an iteration over the result misses its values and totals lower. Grouping the same columns from the many-side table usually brings that row in.
- Fact. 2025. https://www.sqlbi.com/articles/using-values-in-summarize/
- When: The model has an invalid relationship and a measure iterates the result of SUMMARIZE.

### Writing DAX queries

**T03-A007-3.** When converting an MDX SELECT query to DAX, build the result with ADDCOLUMNS over ALL of the column on rows, inside a CALCULATETABLE carrying the slicer filter, not with SUMMARIZE. Unlike NON EMPTY in MDX, this also returns row values with no data.
- Should. Check. 2011. https://www.sqlbi.com/articles/converting-mdx-to-dax-first-steps/
- When: Converting an MDX SELECT statement into a DAX query.

**T03-A007-4.** One way to map MDX to DAX: turn the WHERE slicer into a filter argument of a CALCULATETABLE around the query, and each calculated MEMBER into a measure defined in the query that uses CALCULATE to reproduce the MDX tuple.
- Option. 2011. https://www.sqlbi.com/articles/converting-mdx-to-dax-first-steps/
- When: Converting an MDX query with a WHERE clause and calculated members into a DAX query.

**T03-A007-5.** To reproduce the MDX NON EMPTY clause in a DAX query, the result table can be wrapped in FILTER, keeping only the rows where the returned measures are not all equal to 0.
- Option. Check. 2011. https://www.sqlbi.com/articles/converting-mdx-to-dax-first-steps/
- When: A DAX query built with ADDCOLUMNS to mimic an MDX SELECT, which also returns rows without values.

**T03-A007-6.** To translate an MDX crossjoin of attributes on an axis, the row list can be built with CROSSJOIN over those columns. It returns every combination of their values, ignoring any other column and any relationship between them.
- Option. 2011. https://www.sqlbi.com/articles/converting-mdx-to-dax-first-steps/
- When: Converting an MDX query that crossjoins attributes on rows into a DAX query.

**T03-A007-7.** For rows holding only the existing combinations of two related columns, SUMMARIZE over ALL of the more detailed table, grouped by both columns, can build the list, somewhat like MDX autoexists. ALL shields the list from a surrounding CALCULATETABLE filter, which then affects only measures.
- Option. 2011. https://www.sqlbi.com/articles/converting-mdx-to-dax-first-steps/
- When: Converting an MDX crossjoin of related attributes into a DAX query.

**T03-A104-3.** A variable declared after an EVALUATE keyword exists only inside that EVALUATE's table expression. A later EVALUATE in the same batch that references it fails.
- Fact. 2017. https://www.sqlbi.com/articles/defining-variables-in-dax-queries/
- When: DAX query batches with more than one EVALUATE statement.

**T03-A104-4.** A variable declared in the DEFINE section of a query can be overridden by a variable of the same name declared in an EVALUATE statement or locally in any other DAX expression; there, the local definition is used.
- Fact. 2017. https://www.sqlbi.com/articles/defining-variables-in-dax-queries/
- When: DAX queries that declare variables both in DEFINE and inside EVALUATE statements or expressions.

**T03-A104-5.** A DAX query batch may hold many EVALUATE statements, but DEFINE may appear only once, and it must come before the first EVALUATE.
- Fact. 2017. https://www.sqlbi.com/articles/defining-variables-in-dax-queries/
- When: Writing a DAX query batch with DEFINE and EVALUATE.

**T03-A115-1.** To fetch a page of raw rows quickly, a DAX query can wrap the table in TOPNSKIP (rows to return, rows to skip, an optional sort column) inside SELECTCOLUMNS that lists every column.
- Option. Check. 2017. https://www.sqlbi.com/articles/querying-raw-data-to-tabular/
- When: Reading raw table rows in blocks, as Power BI does when a table is browsed in Data view.
- Version: Described in 2017 as undocumented and open to change; Microsoft Learn now has a TOPNSKIP page.

**T03-A115-3.** A TOPNSKIP raw-data query can be limited to some rows by wrapping it in CALCULATETABLE with the filter condition.
- Option. Check. 2017. https://www.sqlbi.com/articles/querying-raw-data-to-tabular/
- When: Raw-data DAX queries that page through a table with TOPNSKIP and need a filter.
- Version: In October 2017 Power BI accepted the syntax but did not support this filtering.

**T03-A115-4.** When sending SQL-syntax queries to a Tabular model, add SqlQueryMode=DataKeys; to the connection string.
- Should. Check. 2017. https://www.sqlbi.com/articles/querying-raw-data-to-tabular/
- When: Querying raw Tabular data with the SQL syntax used by SSDT and Power Pivot.
- Version: Found by analysing tool queries; undocumented by Microsoft, may change and might be unsupported.

**T03-A115-5.** In SQL-syntax queries against a Tabular model, start every reference with the [Model] identifier, put a $ before the table name, and enclose table and column names in square brackets every time, although brackets are strictly required only for names with spaces or special characters.
- Should. Check. 2017. https://www.sqlbi.com/articles/querying-raw-data-to-tabular/
- When: Raw-data SQL queries sent to a Tabular model.
- Version: Found by analysing tool queries; undocumented by Microsoft, may change and might be unsupported.

**T03-A115-6.** Do not read the RowNumber column, returned by a SQL SELECT * query against a Tabular table, as the row's position in the result or in the source. It is the zero-based physical position inside the engine's storage, which compression may rearrange.
- Must. Check. 2017. https://www.sqlbi.com/articles/querying-raw-data-to-tabular/
- When: Raw-data SQL queries to Tabular that use * instead of a column list; the column is unreachable from DAX.
- Version: Found by analysing tool queries; undocumented by Microsoft, may change and might be unsupported.

**T03-A115-7.** Raw-data queries that page, sort and filter on a column are one way to build drillthrough over a large table, or a tool that browses model data quickly.
- Option. Check. 2017. https://www.sqlbi.com/articles/querying-raw-data-to-tabular/
- When: A reporting environment where you control how queries are generated, or a custom data-browsing tool.
- Version: Rests on TOPNSKIP, described in 2017 as undocumented; Microsoft Learn now has its page.

**T03-A214-2.** Avoid defining a query column with DEFINE COLUMN only to shorten a query, for example to replace an inline filter condition. Query columns are evaluated with different semantics from inline expressions or ADDCOLUMNS columns, so the shorter query can return very different numbers.
- Should. Check. 2021. https://www.sqlbi.com/articles/introducing-define-column-in-dax-queries/
- When: A query column would replace logic that runs in the query's filter context, such as FILTER inside CALCULATE.
- Version: DEFINE COLUMN: introduced December 2020 for composite models over Analysis Services; still a preview when described in 2021.

**T03-A214-3.** To make an ADDCOLUMNS column match a DEFINE COLUMN query column while the query applies filters, compute it inside CALCULATE with a filter that clears every filter except the one on the iterated table, for example ALLEXCEPT on the fact table. Context transition still applies.
- Must. Check. 2021. https://www.sqlbi.com/articles/introducing-define-column-in-dax-queries/
- When: Only when reproducing the behaviour of a DEFINE COLUMN query column inside a filtered table expression.
- Version: DEFINE COLUMN was introduced in December 2020.

### Filter and text conditions

**T03-A007-9.** A filter that CALCULATETABLE puts on a column of one table does not reach a table argument that has no relationship with that table. Passing an unrelated lookup table, such as Product under a filter on Date, leaves the filter without effect.
- Fact. 2011. https://www.sqlbi.com/articles/converting-mdx-to-dax-first-steps/
- When: Trying to fix a SUMMARIZE over a filtered fact table by passing a lookup table to CALCULATETABLE instead.

**T03-A012-1.** Case sensitivity of text comparison in DAX depends on the method. Comparison operators follow the collation and can be case-insensitive; FIND, SUBSTITUTE and CONTAINSSTRINGEXACT are always case-sensitive; SEARCH and CONTAINSSTRING are always case-insensitive.
- Fact. 2011. https://www.sqlbi.com/articles/from-sql-to-dax-string-comparison/
- When: Comparing or searching text in DAX.
- Version: CONTAINSSTRING and CONTAINSSTRINGEXACT exist only in more recent DAX versions.

**T03-A012-2.** FIND can be around 10% faster than SEARCH, a difference attributed only to FIND being case-sensitive.
- Fact. Check. 2011. https://www.sqlbi.com/articles/from-sql-to-dax-string-comparison/
- When: Choosing between FIND and SEARCH for a text search.
- Version: Speed figure reported in 2011.

**T03-A012-3.** To translate a SQL LIKE that tests whether a text contains a substring, use CONTAINSSTRING. Where it is not available, use SEARCH with a start position of 1 and a not-found value of 0, and test that the result is greater than 0.
- Option. 2011. https://www.sqlbi.com/articles/from-sql-to-dax-string-comparison/
- When: Rewriting SQL LIKE conditions with leading and trailing wildcards as DAX conditions.
- Version: CONTAINSSTRING: Power BI, Analysis Services 2019, Azure Analysis Services. Four-argument SEARCH: Tabular and Power Pivot v2 (SQL Server 2012).

**T03-A012-5.** When a SQL LIKE pattern is rewritten with SEARCH, the SQL wildcards must be replaced: % becomes * and _ becomes ?.
- Must. 2011. https://www.sqlbi.com/articles/from-sql-to-dax-string-comparison/
- When: Translating SQL LIKE conditions with a pattern more complex than a single substring.

**T03-A012-6.** A SQL LIKE pattern of wildcard-separated fragments whose last fragment must close the text has no equivalent built on SEARCH: the value SEARCH returns cannot show that the text ends with that fragment.
- Fact. 2011. https://www.sqlbi.com/articles/from-sql-to-dax-string-comparison/
- When: Translating SQL LIKE patterns that mix wildcards with a fixed ending.

**T03-A012-8.** Translate each SQL LIKE into the simplest DAX test: equality when there is no wildcard; LEFT for a fixed start; RIGHT for a fixed end; CONTAINSSTRING or SEARCH for a substring, with * between two ordered fragments; join two tests with AND for combined patterns.
- Should. Check. 2011. https://www.sqlbi.com/articles/from-sql-to-dax-string-comparison/
- When: Rewriting SQL LIKE filters as DAX conditions.
- Version: Without CONTAINSSTRING (Analysis Services 2012 to 2017, Power Pivot v2): SEARCH with start 1 and not-found 0.

**T03-A045-1.** CALCULATETABLE combines its filter arguments with a logical AND and turns each one into an internal FILTER over a single column. That can be faster than FILTER over the table when each single-column condition returns relatively few values.
- Fact. 2014. https://www.sqlbi.com/articles/from-sql-to-dax-filtering-data/
- When: Filtering a table with several conditions, the counterpart of a SQL WHERE clause.

**T03-A046-3.** To keep only the groups whose aggregated value meets a condition, as SQL HAVING does, apply FILTER to the table returned by SUMMARIZE or ADDCOLUMNS and test the aggregated column there. CALCULATE and CALCULATETABLE cannot take an aggregation result as a filter argument.
- Must. Check. 2014. https://www.sqlbi.com/articles/from-sql-to-dax-grouping-data/
- When: Filtering grouped rows on the value of an aggregation computed in the grouping.

**T03-A053-2.** Where the IN operator cannot be used, one way to filter a column on a list of values is to keep the values in a separate table and check the column against that table.
- Option. Check. 2015. https://www.sqlbi.com/articles/from-sql-to-dax-in-and-exists/
- When: Filtering a column on a list of values without the IN operator.
- Version: The approach used before the IN operator existed (2016).

**T03-A053-4.** In an existence test over the rows related to the current lookup value, RELATEDTABLE can replace CALCULATETABLE to get the related rows. Behaviour and performance are the same, and it is more descriptive and easier to read.
- Option. 2015. https://www.sqlbi.com/articles/from-sql-to-dax-in-and-exists/
- When: Testing for related rows while iterating a lookup table that has a relationship with the tested table.

**T03-A053-5.** Where ISEMPTY is not available, an existence test for related rows can be written with CONTAINS over the related rows.
- Option. Check. 2015. https://www.sqlbi.com/articles/from-sql-to-dax-in-and-exists/
- When: Writing the SQL EXISTS equivalent without ISEMPTY.
- Version: For versions before SQL Server 2012 SP1 CU4 (build 11.0.3368), and for Excel 2013.

**T03-A129-1.** To avoid repeating one complex table filter in many measures, the table expression can be kept in one measure's Detail Rows Expression property, and each measure can pass DETAILROWS of that measure to CALCULATE as its filter.
- Option. Check. 2018. https://www.sqlbi.com/articles/creating-table-functions-in-dax-using-detailrows/
- When: Complex filters shared by several measures; the feature was not designed for this, so check performance.
- Version: Compatibility level 1400; in 2018 the only reusable table expression.

**T03-A129-3.** DETAILROWS used as a CALCULATE filter returns correct results, but its query plan can be worse than the same table expression written directly in CALCULATE, notably when the filter picks standard time intelligence functions from dynamic conditions.
- Fact. Check. 2018. https://www.sqlbi.com/articles/creating-table-functions-in-dax-using-detailrows/
- When: Measures that reuse a table filter through DETAILROWS, especially time intelligence filters chosen dynamically, for example by a slicer.

**T03-A129-4.** Always test measures that share a table expression through DETAILROWS against a realistic volume of data before relying on them: the technique can bring performance problems.
- Must. Check. 2018. https://www.sqlbi.com/articles/creating-table-functions-in-dax-using-detailrows/
- When: Any model that reuses table filters through the Detail Rows Expression property.

**T03-A129-5.** Keep a table expression used as a CALCULATE filter free of many conditional branches, whether it is written directly or called through DETAILROWS. The cost of DETAILROWS can be acceptable for simple, linear expressions.
- Should. Check. 2018. https://www.sqlbi.com/articles/creating-table-functions-in-dax-using-detailrows/
- When: Table expressions used as filter arguments of CALCULATE, including those shared through DETAILROWS.

**T03-A198-9.** One filter over several columns usually performs worse than separate single-column filters. The exception is a filter on very few combinations, which can beat two single-column filters of low selectivity.
- Fact. 2020. https://www.sqlbi.com/articles/understanding-lookupvalue/
- When: Shaping the filters of a lookup or a CALCULATE over two or more columns.
