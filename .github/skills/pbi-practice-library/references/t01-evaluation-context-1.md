# DAX evaluation context

Part 1 of 2 of this topic. Covers: KEEPFILTERS and arbitrary filters; CALCULATE filter arguments; Visual queries and auto-exist; Reading the selected value; Row context and iterators.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### KEEPFILTERS and arbitrary filters

**T01-A002-2.** Consider wrapping the table an iterator scans, such as VALUES of a column, in KEEPFILTERS, so that the filter created for each iterated value is intersected with an existing multi-column filter instead of overriding it.
- Consider. 2011. https://www.sqlbi.com/articles/keepfilters-a-new-dax-feature-to-correctly-compute-over-arbitrary-shaped-sets/
- When: The measure may run under an arbitrarily shaped filter over several columns of the iterated table.

**T01-A002-4.** To keep an arbitrarily shaped selection intact, prefer KEEPFILTERS to an outer filter on the whole table: the table filter also works when all filtered columns share one table, but is hard to build once the combination spans several tables.
- Should. 2011. https://www.sqlbi.com/articles/keepfilters-a-new-dax-feature-to-correctly-compute-over-arbitrary-shaped-sets/
- When: A measure must respect a selection that ties values of two or more columns.

**T01-A250-1.** With KEEPFILTERS, a column condition restricts what the outer filter already allows and no longer forces its own value: the measure returns a value only where the outer filter includes the requested value. Whether to override or combine is the developer's choice.
- Option. 2021. https://www.sqlbi.com/articles/when-to-use-keepfilters-over-iterators/ ; https://www.sqlbi.com/articles/introducing-calculate-in-dax/ ; https://www.sqlbi.com/articles/using-keepfilters-in-dax-updated/
- When: A CALCULATE or CALCULATETABLE filter argument targets columns the outer filter context may already filter.

**T01-A250-3.** A CALCULATE condition that tests several columns at once, such as an OR over two columns, replaces the outer filters on every column it names, so a slicer on one of them is ignored. KEEPFILTERS around it can merge it with those filters.
- Option. 2021. https://www.sqlbi.com/articles/specifying-multiple-filter-conditions-in-calculate/ ; https://www.sqlbi.com/articles/using-keepfilters-in-dax-updated/
- When: One CALCULATE condition names several columns that the outer filter context may also filter.

**T01-A111-2.** To restrict one column while keeping its existing filter, prefer the predicate wrapped in KEEPFILTERS to FILTER over VALUES of that column: same result, simpler code and one small storage engine query less, though the speed gain is negligible.
- Should. 2017. https://www.sqlbi.com/articles/using-keepfilters-in-dax/
- When: The existing filter on the column must be intersected, not replaced.

**T01-A111-3.** For a CALCULATE condition on several columns that must keep the existing selection, wrap FILTER over ALL of those columns in KEEPFILTERS and do not filter SUMMARIZE of the table: it is usually faster, more so as the cardinality of the combinations grows.
- Should. Check. 2017. https://www.sqlbi.com/articles/using-keepfilters-in-dax/
- When: Test further when the condition holds complex expressions or causes CallbackDataID in storage engine queries.

**T01-A219-4.** Iterate a column whose cardinality matches the calculation, such as one with a distinct value for each month of each year, not a column like month name whose values repeat across years. The result is then correct without KEEPFILTERS.
- Should. 2021. https://www.sqlbi.com/articles/when-to-use-keepfilters-over-iterators/
- When: The iterated column alone does not identify the grain, as with a monthly average over several years.

**T01-A305-2.** A filter on one column can select several values whenever its predicate uses IN, <, >, <=, >= or <>; only = or == selects one. Wrap such a filter in KEEPFILTERS unless a specific exception to the rule can be described.
- Should. 2024. https://www.sqlbi.com/articles/best-practices-for-using-keepfilters-in-dax/
- When: A CALCULATE filter argument tests one column with an operator other than equals.

**T01-A305-4.** When a CALCULATE filter deliberately departs from the usual KEEPFILTERS choice (none for one value of one column, KEEPFILTERS for several values or columns), you must add a code comment that gives the reason, so maintainers see it was intended.
- Must. 2024. https://www.sqlbi.com/articles/best-practices-for-using-keepfilters-in-dax/
- When: A requirement-driven exception to the usual KEEPFILTERS choice; the ordinary case needs no comment.

### CALCULATE filter arguments

**T01-A074-7.** Weigh the granularity of each complex CALCULATE filter argument: its cost is the row count of the table it produces. FILTER over a whole table is usually the easiest valid form but can mean a large iteration and, through the expanded table, a costlier filter.
- Consider. 2016. https://www.sqlbi.com/articles/filter-arguments-in-calculate/
- When: Writing complex filter arguments; speed differences show only on larger models.

**T01-A309-1.** Before writing a measure, describe the filter context each term of the calculation needs, such as numerator and denominator of a ratio, and compare it with the starting filter context to see which filters to remove, add or replace.
- Should. 2024. https://www.sqlbi.com/articles/filter-context-in-dax-explained-visually/
- When: Designing any measure that changes the filter context with CALCULATE.

**T01-A220-1.** When a CALCULATE condition involves several columns of one table, use FILTER over ALL of just those columns, wrapped in KEEPFILTERS when it replaces a whole-table FILTER and the result must not change. Filtering the whole table instead is a frequent mistake that performs worse.
- Should. 2021. https://www.sqlbi.com/articles/specifying-multiple-filter-conditions-in-calculate/
- When: A CALCULATE filter condition references more than one column of the same table.

**T01-A220-2.** A CALCULATE filter argument can be one Boolean predicate that names several columns of a single table, with no explicit FILTER; it replaces filters already on those columns. Earlier guidance, when a predicate could name only one column, required an explicit table expression.
- Option. 2021. https://www.sqlbi.com/articles/specifying-multiple-filter-conditions-in-calculate/ ; https://www.sqlbi.com/articles/filter-arguments-in-calculate/
- When: A filter condition needs more than one column of the same table.
- Version: Available since the March 2021 release of Power BI Desktop.

**T01-A220-7.** Put several columns in one CALCULATE predicate only when the logic needs it. Split a plain AND between columns into separate filter arguments, one per column: they run faster.
- Should. 2021. https://www.sqlbi.com/articles/specifying-multiple-filter-conditions-in-calculate/
- When: A CALCULATE condition joins tests on different columns with a simple AND.
- Version: The March 2021 multi-column predicate syntax does not change this.

**T01-A263-5.** When a CALCULATE filter predicate needs a value computed with CALCULATE, compute it in a variable before the outer CALCULATE and compare the column with the variable. Do not wrap the predicate in an explicit FILTER: the inner CALCULATE would add an unwanted context-transition filter.
- Should. 2022. https://www.sqlbi.com/articles/solving-errors-in-calculate-filter-arguments/
- When: A filter predicate compares a column with a value that itself needs CALCULATE.

**T01-A263-7.** Compute an aggregation such as the last visible date in a variable before CALCULATE and use the variable in the filter predicate. It gives the intended value and is evaluated fewer times.
- Should. 2022. https://www.sqlbi.com/articles/solving-errors-in-calculate-filter-arguments/
- When: A CALCULATE predicate compares a column with an aggregated value, as in a cumulative total.

**T01-A263-8.** When a CALCULATE filter predicate compares a column with a measure, such as one returning a slicer or parameter selection, store the measure result in a variable before CALCULATE and compare the column with it. A measure reference inside the predicate raises the PLACEHOLDER error.
- Should. 2022. https://www.sqlbi.com/articles/solving-errors-in-calculate-filter-arguments/
- When: The predicate already names the column to filter, so the filter target is known.

**T01-A263-9.** When a CALCULATE filter condition is only a measure compared with a value, with no column, the filter target is undefined. You must first settle with the requirement which entity is filtered, so the measure is evaluated per item; a variable does not solve this.
- Must. 2022. https://www.sqlbi.com/articles/solving-errors-in-calculate-filter-arguments/
- When: A predicate filter argument holds a measure reference and no table or column reference.

### Visual queries and auto-exist

**T01-A132-2.** To test whether a column that uses Sort by Column is filtered, check both the column and its sort-by column with two ISFILTERED calls joined by OR: Power BI queries include both columns, so a test on one alone can give an unexpected answer.
- Should. 2018. https://www.sqlbi.com/articles/side-effects-in-dax-of-the-sort-by-column-setting/
- When: A measure tests the filter state of a column with Sort by Column set.

**T01-A132-4.** In a DAX query, always state the wanted row order with ORDER BY, and return every column that ORDER BY names in the query result: beyond each data type's natural order DAX applies no implicit order, so Sort by Column is not honoured by itself.
- Must. 2018. https://www.sqlbi.com/articles/side-effects-in-dax-of-the-sort-by-column-setting/
- When: Writing any DAX query whose row order matters.

### Reading the selected value

**T01-A105-2.** Where a row context exists, read the column directly, through RELATED when it lives in a lookup table, not with SELECTEDVALUE or VALUES: those look at the filter context, not at the current row.
- Should. 2017. https://www.sqlbi.com/articles/using-the-selectedvalue-function-in-dax/
- When: The expression runs in a row context.

**T01-A105-10.** Use SELECTEDVALUE, or the equivalent HASONEVALUE with VALUES, only in top-level calculations, not in measures evaluated many times inside large iterations: they work like DISTINCT internally and can multiply storage engine requests when filters flow through limited relationships.
- Should. 2017. https://www.sqlbi.com/articles/using-the-selectedvalue-function-in-dax/
- When: A measure that reads a selection would be called for many cells or rows.

**T01-A193-2.** Use ISINSCOPE when the check is about the visual itself, such as which hierarchy level is browsed or special behaviour at the grand total: it tells the visual's grouping from a slicer filter. When it is TRUE the column can still have zero values.
- Should. 2020. https://www.sqlbi.com/articles/distinguishing-hasonevalue-from-isinscope/
- When: A measure must react to the grouping of the visual, not to slicer selections.

**T01-A193-3.** Use HASONEVALUE when a measure makes sense only with one selected value, whether that value comes from the visual's grouping or from a slicer, such as a year-to-date figure for one year. It is slower than ISINSCOPE, because it counts the visible values.
- Should. 2020. https://www.sqlbi.com/articles/distinguishing-hasonevalue-from-isinscope/
- When: A measure is meaningful only if exactly one value of a column is visible.

**T01-A193-4.** When it matters whether a grouped column has no value or one, guard the calculation with HASONEVALUE, not ISINSCOPE, although ISINSCOPE is faster: ISINSCOPE can be TRUE with no visible value. This does not make HASONEVALUE the better choice in general.
- Should. Check. 2020. https://www.sqlbi.com/articles/distinguishing-hasonevalue-from-isinscope/
- When: A visual groups by columns of different tables and many combinations have no rows.

### Row context and iterators

**T01-A063-1.** A measure must aggregate a column, for instance with SUM, and not reference the column's value on its own: with no row context a bare column reference raises an error.
- Must. 2015. https://www.sqlbi.com/articles/row-context-and-filter-context-in-dax/
- When: Measure expressions outside any iteration; a row context exists only in iterators and calculated columns.

**T01-A244-2.** To aggregate a row-by-row expression such as quantity times price, you must use an iterator such as SUMX over the table that holds every column the expression uses. Never multiply separate SUM results: a product of sums is a wrong number.
- Must. 2022. https://www.sqlbi.com/articles/row-context-in-dax/
- When: A measure aggregates a calculation over several columns of each row.

**T01-A310-2.** Compute an expression that does not depend on the row context, such as reading a slicer selection, before the iterator and not inside the iterated expression. This makes plain that it does not depend on the current row.
- Should. 2024. https://www.sqlbi.com/articles/row-context-in-dax-explained-visually/
- When: An expression inside an iterator does not use the row context.

**T01-A336-3.** Do not wrap every iterated table in VALUES by habit. Decide for each calculation whether the blank row produced by an invalid relationship should take part in the iteration.
- Should. 2025. https://www.sqlbi.com/articles/using-values-in-iterators/
- When: Writing or reviewing an iterator over a table reference.

**T01-A336-4.** An existing SUMX over a bare table reference may stay without VALUES when the expression uses only column references, performs no context transition, or no column of the table is the one-side end of a regular relationship: both forms then return the same values.
- Option. 2025. https://www.sqlbi.com/articles/using-values-in-iterators/
- When: Reviewing existing SUMX iterations; a needless VALUES costs nothing if the meaning stays right.

## Special-case techniques and facts

### KEEPFILTERS and arbitrary filters

**T01-A002-3.** In a DAX query where SUMMARIZE groups a CROSSJOIN of columns and CALCULATETABLE applies an arbitrarily shaped filter on them, the CROSSJOIN can be wrapped in KEEPFILTERS; otherwise it ignores that filter and even measures that use KEEPFILTERS return wrong values.
- Option. Check. 2011. https://www.sqlbi.com/articles/keepfilters-a-new-dax-feature-to-correctly-compute-over-arbitrary-shaped-sets/
- When: A query reproduces a multi-column selection by filtering a crossjoin, then groups by those columns.

**T01-A315-3.** When an iterator over one column triggers context transition, the new filter replaces that column's part of an arbitrarily shaped filter; combinations never selected come in, so subtotals and totals can be wrong while the lowest level still looks right.
- Fact. 2011. https://www.sqlbi.com/articles/keepfilters-a-new-dax-feature-to-correctly-compute-over-arbitrary-shaped-sets/ ; https://www.sqlbi.com/articles/when-to-use-keepfilters-over-iterators/ ; https://www.sqlbi.com/articles/context-transition-in-dax-explained-visually/
- When: No KEEPFILTERS on the iterated table, and the outer selection is not a filter on the whole table.

**T01-A315-4.** To make context transition inside an iterator keep the existing filters on the iterated columns, you must wrap the iterator's table argument in KEEPFILTERS. The transition is not a filter argument and always overwrites, so that is the only place KEEPFILTERS can go.
- Must. 2021. https://www.sqlbi.com/articles/when-to-use-keepfilters-over-iterators/ ; https://www.sqlbi.com/articles/context-transition-in-dax-explained-visually/
- When: An iterator's expression triggers context transition and existing filters on the iterated columns must survive.

**T01-A074-5.** When a two-column CALCULATE filter built with ALL or CROSSJOIN should keep the existing filters on those columns and not replace them, one option is to wrap that filter in KEEPFILTERS.
- Option. 2016. https://www.sqlbi.com/articles/filter-arguments-in-calculate/
- When: The replacing behaviour of ALL or CROSSJOIN in a multi-column filter is not wanted.

**T01-A250-2.** Adding VALUES of the filtered column as an extra CALCULATE filter, or iterating VALUES instead of ALL inside FILTER, keeps an outer filter on one column as KEEPFILTERS does. The KEEPFILTERS form is usually more efficient.
- Fact. Check. 2022. https://www.sqlbi.com/articles/using-keepfilters-in-dax-updated/
- When: A CALCULATE filter on one column must intersect with an outer filter on that column.
- Version: The VALUES techniques come from writing that predates KEEPFILTERS in DAX.

**T01-A250-4.** To keep existing filters on a multi-column CALCULATE condition without KEEPFILTERS, SUMMARIZE of the table by those columns can be the filter, alone or inside FILTER. It lists only existing combinations and can include columns of tables joined by many-to-one relationships.
- Option. Check. 2016. https://www.sqlbi.com/articles/filter-arguments-in-calculate/ ; https://www.sqlbi.com/articles/using-keepfilters-in-dax-updated/
- When: The scan may be costly on big tables with low-cardinality columns; compare with the KEEPFILTERS form.
- Version: A 2017 note says SUMMARIZECOLUMNS should replace this in DAX queries but cannot in measures.

**T01-A250-5.** KEEPFILTERS can also wrap the table an iterator scans, such as the month values AVERAGEX walks. There it still acts as a CALCULATE modifier and changes how the context transition of a measure reference in the iteration applies its filter.
- Option. Check. 2022. https://www.sqlbi.com/articles/using-keepfilters-in-dax-updated/
- When: An iterator evaluates a measure reference, so context transition happens with no CALCULATE written.

**T01-A314-4.** For a condition on an expression that combines several columns of one table, such as an amount threshold, write one predicate over those columns in KEEPFILTERS. Applied to several fact tables, such column filters share no columns, so they do not interact.
- Should. 2024. https://www.sqlbi.com/articles/filter-columns-not-tables-in-dax/
- When: A filter needs a row-level condition that combines several columns, possibly on more than one fact table.

**T01-A219-3.** Watch for arbitrarily shaped filters and for iterations over tables that combine columns of different tables. When an iterator has to preserve such combinations, consider KEEPFILTERS on the iterated table; context transition would otherwise overwrite the existing filter. The need is uncommon.
- Consider. 2021. https://www.sqlbi.com/articles/when-to-use-keepfilters-over-iterators/
- When: An iterator triggers context transition over combined columns, or arbitrarily shaped filters may be present.

**T01-A246-3.** FILTER over a whole table, used in CALCULATE to keep the outer filter, returns the same numbers as a column condition in KEEPFILTERS. Because the table filter is far bigger and works on the expanded table, it is slower and can give semantically wrong results.
- Fact. 2022. https://www.sqlbi.com/articles/introducing-calculate-in-dax/
- When: A CALCULATE filter is meant to intersect with an existing filter on a column of that table.

**T01-A305-5.** The KEEPFILTERS rule of thumb is stated for column filters only. When a CALCULATE filter argument is a table filter, consider KEEPFILTERS for that filter on its own merits, after careful thought.
- Consider. 2024. https://www.sqlbi.com/articles/best-practices-for-using-keepfilters-in-dax/
- When: A CALCULATE filter argument is a table, not a column predicate.

### CALCULATE filter arguments

**T01-A020-1.** CALCULATE and CALCULATETABLE evaluate all their filter arguments first and only then the expression in the first argument, in the resulting filter context; most other DAX functions evaluate their arguments from left to right.
- Fact. 2012. https://www.sqlbi.com/articles/order-of-evaluation-in-calculate-parameters/
- When: Reading or writing any CALCULATE or CALCULATETABLE call.

**T01-A020-2.** In nested CALCULATE calls the outer filters apply before the inner call runs, so the inner filter arguments win: an inner ALL on a column cancels an outer filter on it, and an inner KEEPFILTERS filter under an outer ALL leaves only the inner value.
- Fact. 2012. https://www.sqlbi.com/articles/order-of-evaluation-in-calculate-parameters/
- When: Measures nest CALCULATE with filters, ALL or KEEPFILTERS on the same column.
- Version: Revised in December 2018 to match the DAX behaviour of that time.

**T01-A020-3.** The filter arguments of one CALCULATE are evaluated independently of each other: a FILTER over a table given as one argument scans every row of that table and is not narrowed by another filter argument of the same call.
- Fact. 2012. https://www.sqlbi.com/articles/order-of-evaluation-in-calculate-parameters/
- When: A CALCULATE has several filter arguments and one iterates a table with FILTER.

**T01-A047-2.** In a denormalized table, a CALCULATE that replaces the category filter with a fixed category leaves the subcategory filter active: it returns nothing where a subcategory of another category is filtered, and the fixed category's total where only category is filtered.
- Fact. 2014. https://www.sqlbi.com/articles/autoexist-and-normalization/
- When: A measure overrides one column's filter while a related column of the same table is on the report.

**T01-A074-3.** For a CALCULATE condition on two columns of one table, one option is FILTER over ALL of just those two columns: it iterates the value pairs present in the table and replaces any filter already on those columns.
- Option. Check. 2016. https://www.sqlbi.com/articles/filter-arguments-in-calculate/
- When: Listing existing pairs needs a table scan, costly on a big table whose columns have few distinct values.

**T01-A074-4.** For a CALCULATE condition on two columns, another option is FILTER over the CROSSJOIN of ALL of each column: it iterates every possible pair, replaces existing filters like ALL of both columns, and can combine columns of different tables, which ALL cannot.
- Option. 2016. https://www.sqlbi.com/articles/filter-arguments-in-calculate/
- When: It avoids a table scan but is costly for high-cardinality, strongly correlated columns.

**T01-A309-3.** The engine converts a Boolean predicate in CALCULATE into a filter over all values of its column, as if REMOVEFILTERS on that column were present. Filters on other columns stay in place, and on a column not yet filtered the predicate only adds a filter.
- Fact. 2017. https://www.sqlbi.com/articles/using-keepfilters-in-dax/ ; https://www.sqlbi.com/articles/introducing-calculate-in-dax/ ; https://www.sqlbi.com/articles/filter-context-in-dax-explained-visually/
- When: A filter argument touches a column the outer filter context may already filter.

**T01-A220-5.** One Boolean filter predicate in CALCULATE can reference columns of a single table only. A predicate that mixes columns of different tables is not valid DAX.
- Fact. 2021. https://www.sqlbi.com/articles/specifying-multiple-filter-conditions-in-calculate/
- When: A CALCULATE predicate combines conditions on columns of two or more tables.
- Version: Still true after the March 2021 change that allowed several columns of one table.

**T01-A220-6.** For a CALCULATE condition on columns of different tables, one approach is to build the filter from a CROSSJOIN of those columns. When the columns give too many combinations, other techniques may be needed to reduce the cardinality.
- Option. 2021. https://www.sqlbi.com/articles/specifying-multiple-filter-conditions-in-calculate/
- When: A CALCULATE filter condition references columns of more than one table.

**T01-A246-4.** CALCULATE evaluates each filter argument separately, under the outer filter context, and applies the new filters only as its last step. A FILTER over a table in a filter argument sees only rows the outer filter leaves visible; an empty result makes the measure blank.
- Fact. 2022. https://www.sqlbi.com/articles/introducing-calculate-in-dax/
- When: A filter argument iterates a table already restricted by the outer filter, for example blue products filtered for red ones.

**T01-A263-1.** A Boolean predicate used as a CALCULATE filter argument is rewritten internally as FILTER over ALL of the columns it names. When that rewrite is impossible, a syntax error appears whose message is often hard to interpret.
- Fact. 2022. https://www.sqlbi.com/articles/solving-errors-in-calculate-filter-arguments/
- When: Predicate filter arguments in CALCULATE or CALCULATETABLE.

**T01-A263-2.** When a CALCULATE filter condition compares columns of different tables, you must write an explicit FILTER over a table that combines those columns, built with CROSSJOIN or SUMMARIZE. A plain predicate raises an error about columns from multiple tables.
- Must. 2022. https://www.sqlbi.com/articles/solving-errors-in-calculate-filter-arguments/
- When: A filter argument references columns of more than one table, such as customer country against store country.

**T01-A263-3.** When building the combined table for a filter condition across tables, prefer CROSSJOIN of the column values if those columns have few distinct values.
- Should. 2022. https://www.sqlbi.com/articles/solving-errors-in-calculate-filter-arguments/
- When: A filter argument compares columns of different tables and their cardinality is small.

**T01-A263-4.** A predicate filter argument of CALCULATE or CALCULATETABLE cannot contain anything that triggers context transition: CALCULATE, LASTDATE or any measure reference. The error names the function, or shows PLACEHOLDER when a measure reference is the cause.
- Fact. 2022. https://www.sqlbi.com/articles/solving-errors-in-calculate-filter-arguments/
- When: Writing a predicate as a CALCULATE or CALCULATETABLE filter argument.

### Visual queries and auto-exist

**T01-A047-1.** By default auto-exist removes non-existing combinations only among columns of one table. For columns of different tables the engine evaluates every combination and the PivotTable just hides blank ones, so normalized and denormalized models can show the same report yet compute it differently.
- Fact. 2014. https://www.sqlbi.com/articles/autoexist-and-normalization/
- When: Comparing a normalized model with one that copies category and subcategory into the product table.
- Version: Described as a server feature for MDX queries against Analysis Services or Power Pivot models.

**T01-A047-3.** When category and subcategory sit in separate related tables, a CALCULATE that overrides the category filter can show values for pairs that do not exist, because auto-exist does not act across tables and every pair is evaluated.
- Fact. 2014. https://www.sqlbi.com/articles/autoexist-and-normalization/
- When: A measure overrides a filter on a normalized dimension while a column of another related table is shown.

**T01-A047-4.** To tell whether auto-exist removed non-existing combinations or the PivotTable only hid empty rows, switch on the PivotTable option that shows items without data: combinations hidden for being blank then appear, those removed by auto-exist do not.
- Option. 2014. https://www.sqlbi.com/articles/autoexist-and-normalization/
- When: Checking how a PivotTable on a normalized or denormalized model handles attribute combinations.

**T01-A047-5.** In a normalized model, a measure that replaces the category filter can imitate auto-exist; one way is to also restrict the categories to those linked to the subcategories currently filtered, when a subcategory filter is active.
- Option. 2014. https://www.sqlbi.com/articles/autoexist-and-normalization/
- When: Category and subcategory are separate related tables and subcategories are on the report; other ways exist.

**T01-A132-3.** A Power BI visual showing a column sorted by another always queries both columns, so its filter context also filters the sort-by column. An Excel PivotTable query, in MDX, holds only the displayed column, so one measure can return different numbers in the two clients.
- Fact. 2018. https://www.sqlbi.com/articles/side-effects-in-dax-of-the-sort-by-column-setting/
- When: A report shows a column with Sort by Column set; showing only the sort-by column has no side effect.

**T01-A135-1.** After auto-exist in SUMMARIZECOLUMNS reduces filters on columns of one table to existing combinations, a measure that removes one column's filter with ALL cannot bring back the discarded values: its total can look like a bug. Across tables SUMMARIZECOLUMNS cross-joins the columns, which is slower.
- Fact. Check. 2018. https://www.sqlbi.com/articles/understanding-dax-auto-exist/
- When: Two or more filtered columns, such as slicers, belong to the same table.

**T01-A135-4.** Auto-exist is performed by SUMMARIZECOLUMNS, not by CALCULATETABLE: filters on columns of the same table passed to CALCULATETABLE are applied as written, without first being reduced to existing combinations.
- Fact. 2018. https://www.sqlbi.com/articles/understanding-dax-auto-exist/
- When: Comparing a SUMMARIZECOLUMNS query with the same filters given to CALCULATETABLE.

**T01-A135-5.** When a query really needs every combination of values, including those absent from the data, a table function such as CROSSJOIN can produce them; grouping under auto-exist returns existing combinations only.
- Option. 2018. https://www.sqlbi.com/articles/understanding-dax-auto-exist/
- When: The rare case where non-existing combinations of column values must be returned.

### Reading the selected value

**T01-A058-1.** To give a measure parameter values, one option is a hidden table per parameter holding every value needed: call the measure in CALCULATE with a filter that sets the column to the wanted value, and let the measure read it with VALUES.
- Option. Check. 2015. https://www.sqlbi.com/articles/parameters-in-dax-measures/
- When: Complex expressions compute a measure with different argument values; simple cases can keep the condition in inner measures.
- Version: Written in 2015, when DAX had no way to pass arguments to a measure. The DAX standard reads one value with SELECTEDVALUE (rule 4); user-defined functions now take parameters. Needs its M411 row in the brief (relationships and dates, rule 4).

**T01-A058-2.** Hide measures that read their parameter values from hidden parameter tables, so users never call them directly: with several values selected in a parameter table such a measure fails with an error.
- Should. 2015. https://www.sqlbi.com/articles/parameters-in-dax-measures/
- When: Measures receive parameter values through hidden parameter tables and CALCULATE filter arguments.

**T01-A105-4.** Where the DAX engine has no SELECTEDVALUE, the same patterns can be written with the equivalent IF combined with HASONEVALUE and VALUES.
- Option. Check. 2017. https://www.sqlbi.com/articles/using-the-selectedvalue-function-in-dax/
- When: The engine in use does not offer SELECTEDVALUE.
- Version: SELECTEDVALUE arrived in July 2017 in Power BI Desktop and Analysis Services; Power Pivot for Excel lacks it.

**T01-A105-5.** A measure that shows a dimension attribute with SELECTEDVALUE should also test that another measure returns data, when the attribute must appear only beside data; without the test it also shows values for items with no sales.
- Should. Check. 2017. https://www.sqlbi.com/articles/using-the-selectedvalue-function-in-dax/
- When: The attribute measure sits in a matrix, pivot table or table visual next to other measures.
- Version: As of March 2024 the Table visual behaves this way too; older Power BI versions did not.

**T01-A105-6.** To read a snowflaked lookup table's attribute from the filter context, wrap SELECTEDVALUE in CALCULATE with CROSSFILTER set to both directions on the relationships to cross; prefer this to passing the expanded base table as a filter, which may have side effects in complex models.
- Should. 2017. https://www.sqlbi.com/articles/using-the-selectedvalue-function-in-dax/
- When: The attribute is several relationships away, such as category from product, and is shown in a matrix.

**T01-A105-8.** When a parameter must not accept several selections, ERROR can be passed as the alternate result of SELECTEDVALUE so that the visual shows an error message; the message mentions MdxScript, which may look meaningless in Power BI Desktop.
- Option. 2017. https://www.sqlbi.com/articles/using-the-selectedvalue-function-in-dax/
- When: A calculation needs one selected value and must reject multiple selections.

**T01-A105-9.** Do not read a field parameter's slicer selection with SELECTEDVALUE: it cannot return a column grouped by other columns. Group the parameter table by its display and fields columns, for example with SUMMARIZE, and return the display column when that result has rows.
- Must. Check. 2017. https://www.sqlbi.com/articles/using-the-selectedvalue-function-in-dax/
- When: The value to read is the visible column of a table made by the field parameters feature.
- Version: Guidance added in June 2022.

**T01-A193-1.** HASONEVALUE and ISINSCOPE are not interchangeable. HASONEVALUE is TRUE when exactly one value of the column is visible, even because of a slicer; ISINSCOPE is TRUE only when the column is grouped by, as on a visual's rows. At the grand total both are FALSE.
- Fact. 2020. https://www.sqlbi.com/articles/distinguishing-hasonevalue-from-isinscope/
- When: A measure tests the hierarchy level or the selection with either function.

### Row context and iterators

**T01-A244-3.** A row context gives access only to the columns of the iterated table and does not follow relationships: reach the matching row of the parent table with RELATED, and iterate the related many-side rows with RELATEDTABLE.
- Fact. 2015. https://www.sqlbi.com/articles/row-context-and-filter-context-in-dax/ ; https://www.sqlbi.com/articles/row-context-in-dax/
- When: A calculated column or iterator needs data from a table related to the iterated one.

**T01-A244-4.** A row context does not filter its table: in a calculated column, SUM, AVERAGE, MIN or MAX without CALCULATE, or SUMX over the column's own table, scans the whole table (or related table), so every row gets the same value, the grand total for SUM.
- Fact. 2015. https://www.sqlbi.com/articles/understanding-context-transition/ ; https://www.sqlbi.com/articles/row-context-in-dax/
- When: Calculated columns aggregate without CALCULATE and expect a per-row value.

**T01-A247-3.** Iterating a column or table creates a row context, which does not filter the current value. Unless CALCULATE performs a context transition the iterated column carries no filter: filters come only from the filter context.
- Fact. 2022. https://www.sqlbi.com/articles/understanding-context-transition-in-dax/
- When: Code iterates a column, such as customer keys, and expects it to be filtered to the current row.

**T01-A124-1.** RELATED works only with an active row context. In a calculated column, wrapping RELATED in CALCULATE raises an error, because the context transition performed by CALCULATE removes the row context.
- Fact. 2018. https://www.sqlbi.com/articles/expanded-tables-in-dax/
- When: A calculated column evaluates RELATED inside CALCULATE.

**T01-A310-1.** A column reference needs a row context to return a value. A measure has none, so a bare column reference in a measure raises an error that a single value cannot be determined. Iterating a table with an iterator function provides a row context.
- Fact. 2022. https://www.sqlbi.com/articles/row-context-in-dax/ ; https://www.sqlbi.com/articles/row-context-in-dax-explained-visually/
- When: A measure references a column without an aggregation or an iterator.

**T01-A310-3.** Inside an iterator, the expression evaluated for each row sees both that row's row context and the filter context active outside the iterator.
- Fact. 2024. https://www.sqlbi.com/articles/row-context-in-dax-explained-visually/
- When: The iterated expression calls functions that read the filter context, such as a slicer selection.

**T01-A310-4.** An iterator runs once per row of the table expression it receives, so that expression sets the cardinality and the result. SELECTCOLUMNS removes columns but keeps the row count; SUMMARIZE groups, may return fewer rows and can change the total.
- Fact. 2024. https://www.sqlbi.com/articles/row-context-in-dax-explained-visually/
- When: Choosing or changing the table expression an iterator such as SUMX walks.

**T01-A310-5.** When every row of a SUMX iteration is divided by the same value that does not depend on the current row, put the division outside SUMX. Inside the iteration it hides that the divisor is independent of the row.
- Should. 2024. https://www.sqlbi.com/articles/row-context-in-dax-explained-visually/
- When: The divisor does not use the row context, such as a factor read from a slicer.

**T01-A245-1.** A cell of a matrix is computed under a filter context, not a row context; a row context exists only during an iteration. A matrix row for one brand is a filter on that brand and can aggregate many underlying rows.
- Fact. 2022. https://www.sqlbi.com/articles/filter-context-in-dax/
- When: Reasoning about how a measure is evaluated in the rows and cells of a matrix.

**T01-A336-1.** When an iterator such as SUMX over a table reference has to include the blank row added by an invalid relationship, iterate VALUES of that table: a bare table reference ignores that extra row.
- Should. 2025. https://www.sqlbi.com/articles/using-values-in-iterators/
- When: The iterated table can receive a blank row from an invalid relationship and the calculation must cover it.

**T01-A336-2.** With AVERAGEX, MINX, MAXX and similar iterators, such as the maximum sales per customer, you must iterate the bare table reference, not VALUES of the table. VALUES adds the blank row that gathers all unknown customers, and its combined amount inflates the result.
- Must. 2025. https://www.sqlbi.com/articles/using-values-in-iterators/
- When: The iterated table can receive a blank row from an invalid relationship.
