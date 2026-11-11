# DAX evaluation context

Part 2 of 3 of this topic. Covers: Row context and iterators; Relationships, expanded tables and lineage; Context transition; Removing filters with ALL.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

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

**T01-A336-5.** To iterate the distinct values of one column, use VALUES as the default choice.
- Should. 2025. https://www.sqlbi.com/articles/using-values-in-iterators/
- When: An iterator walks the unique values of a single column.

### Relationships, expanded tables and lineage

**T01-A124-7.** When reading or reviewing DAX code, reason about it in terms of expanded tables: table expansion is the concept that explains why DAX behaves as it does.
- Should. 2018. https://www.sqlbi.com/articles/expanded-tables-in-dax/
- When: Reading or reviewing any DAX code.

**T01-A142-5.** Before making DAX code more complex to speed it up, be aware that the complex form stops later engine releases from choosing a faster plan for the original, simpler formula.
- Must. 2019. https://www.sqlbi.com/articles/understanding-data-lineage-in-dax/
- When: Rewriting a measure into a more complex form for performance.
- Version: In February 2023 tests, one original measure outperformed all of its earlier optimised versions.

**T01-A245-2.** Never enable bidirectional filtering on a relationship unless the model author firmly grasps both DAX and data modeling theory: it is a powerful but dangerous tool.
- Must. 2022. https://www.sqlbi.com/articles/filter-context-in-dax/
- When: Deciding whether a relationship should also filter from its many side to its one side.

**T01-A249-1.** In a row context on the many-side table, such as a calculated column of a fact table, you must read a column of a related one-side table through RELATED; a direct reference fails. RELATED works only when every relationship it crosses is regular, not limited.
- Must. 2022. https://www.sqlbi.com/articles/using-related-and-relatedtable-in-dax/
- When: Code in a row context needs a value from a related lookup (one-side) table.

**T01-A249-2.** One RELATED call can reach a column several relationships away, such as a category seen from a sales row, with no step through each table in between.
- Option. 2022. https://www.sqlbi.com/articles/using-related-and-relatedtable-in-dax/
- When: Every relationship in the chain is many-to-one from the iterated table and none is limited.

**T01-A249-4.** In a row context on the one side of a relationship, RELATEDTABLE can return the set of related many-side rows; RELATED cannot be used in that direction, because many rows may match.
- Option. 2022. https://www.sqlbi.com/articles/using-related-and-relatedtable-in-dax/
- When: A row context iterates the one-side table, such as a dimension column counting its fact rows.

### Context transition

**T01-A315-2.** When an iterator needs a total over all the iterated items in the current filter context, such as sales of all customers, compute it in a variable before the iteration starts; recomputing it for every row is not ideal for performance.
- Should. 2024. https://www.sqlbi.com/articles/context-transition-in-dax-explained-visually/
- When: A measure iterates a table and compares each row with a total of all iterated items.

**T01-A118-4.** Never call LASTDATE inside a row context; use MAX there. LASTDATE is a time intelligence function: its column argument is implicitly wrapped in CALCULATETABLE over VALUES, which performs a context transition whenever a row context is active.
- Must. Check. 2018. https://www.sqlbi.com/articles/context-transition-and-filters-in-calculate/
- When: Any expression evaluated in a row context.

**T01-A247-1.** When writing or reviewing DAX, always track every point where CALCULATE or CALCULATETABLE runs inside a row context, including the implicit CALCULATE around a measure reference: the row context becomes an equivalent filter context there. Most such errors come from forgetting it happens.
- Must. 2022. https://www.sqlbi.com/articles/understanding-context-transition-in-dax/
- When: A row context from an iterator or a calculated column meets CALCULATE, CALCULATETABLE or a measure reference.

**T01-A247-2.** Keep in mind that the engine wraps every measure reference in CALCULATE: a measure referenced in an iterator or a calculated column triggers context transition with no CALCULATE in sight, and overlooking this can introduce errors.
- Consider. 2015. https://www.sqlbi.com/articles/understanding-context-transition/ ; https://www.sqlbi.com/articles/understanding-context-transition-in-dax/
- When: Any expression that references a measure where a row context exists.

### Removing filters with ALL

**T01-A361-8.** When several columns must be kept while the table's other filters are removed, use SUMMARIZE of the table by those columns in place of VALUES. ALLEXCEPT remains a choice for maximum performance and for advanced cases such as removing circular dependencies in calculated columns.
- Should. 2016. https://www.sqlbi.com/articles/using-allexcept-vs-all-values/ ; https://www.sqlbi.com/articles/using-allexcept-versus-all-and-values/ ; https://www.sqlbi.com/articles/all-vs-allselected-vs-allexcept-vs-removefilters/
- When: Measures keep one grouping grain and remove the rest, such as a share of the group total.

**T01-A361-9.** REMOVEFILTERS or ALL can take one column, a whole table to clear the filters on all its columns, or, less commonly, no argument, which clears every filter on every table of the model.
- Option. 2026. https://www.sqlbi.com/articles/all-vs-allselected-vs-allexcept-vs-removefilters/
- When: Choosing how wide a filter removal in CALCULATE should be.

**T01-A132-1.** When a measure removes the filter from a column sorted by another column, list both the displayed column and its sort-by column in the same ALL call: Power BI queries include both, and a share that clears only the displayed one always returns 100%.
- Should. 2018. https://www.sqlbi.com/articles/side-effects-in-dax-of-the-sort-by-column-setting/
- When: A measure removes or changes the filter on a column with Sort by Column set.

**T01-A324-3.** Do not replace every existing ALL with ALLCROSSFILTERED as a blanket change. In a model with no limited relationships ALL already works correctly; ALLCROSSFILTERED suits models where filters from cross-filtering tables must also be removed.
- Should. 2025. https://www.sqlbi.com/articles/differences-between-all-and-allcrossfiltered/
- When: Reviewing or refactoring existing DAX that uses ALL.

## Special-case techniques and facts

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

### Relationships, expanded tables and lineage

**T01-A063-3.** A filter context moves through relationships by itself, only along the cross filter direction: with single direction, filtering Product narrows Sales but not the customers who bought them. With bidirectional filtering, a filtered table also filters every table on the one side of its relationships.
- Fact. 2015. https://www.sqlbi.com/articles/row-context-and-filter-context-in-dax/
- When: Working out which tables a filter reaches.
- Version: Power Pivot for Excel supports single direction only; Power BI Desktop and Analysis Services Tabular 2016 allow bidirectional filtering.

**T01-A228-1.** When a budget is stored per brand while the Product dimension is per product, one option is an intermediate Brand table related to both Product and Budget, so a brand filter reaches products, sales and budget together.
- Option. 2016. https://www.sqlbi.com/articles/using-allexcept-vs-all-values/
- When: Two fact tables share a dimension at different granularities.
- Version: Offered for SSAS 2012/2014 and Power Pivot for Excel; another design is described for Power BI and SSAS 2016.

**T01-A228-2.** With an intermediate Brand table linking Product and a brand-level Budget, hide the brand column of Product so users slice brands only through the Brand table: a selection on Product's own brand column cannot reach Budget.
- Should. 2016. https://www.sqlbi.com/articles/using-allexcept-vs-all-values/
- When: The intermediate table is the only path for brand filters to reach the budget.
- Version: Tied to the intermediate-table design for SSAS 2012/2014 and Power Pivot for Excel.

**T01-A228-4.** To stop a brand-level budget showing below its grain, compare COUNTROWS of Product in the current filter context with the count at brand granularity and return the budget only when they match. Build the brand-level count with ALL plus VALUES, not ALLEXCEPT on brand alone.
- Should. 2016. https://www.sqlbi.com/articles/using-allexcept-vs-all-values/
- When: A report slices a coarser-grain fact by finer dimension attributes, such as category.

**T01-A097-2.** Tables are expanded along many-to-one relationships, so a table used as a CALCULATE filter, such as FILTER over a fact table, also filters every column of the related lookup tables and replaces the filters already on those columns.
- Fact. 2017. https://www.sqlbi.com/articles/context-transition-and-expanded-tables/
- When: The table a filter argument returns is the many-side table of some relationships.

**T01-A314-2.** A table used as a CALCULATE filter acts on its expanded table. Two table filters on fact tables that share dimensions intersect on the dimension columns and keep only combinations present in both tables, so the result is smaller than expected.
- Fact. 2024. https://www.sqlbi.com/articles/filter-columns-not-tables-in-dax/
- When: Table filters on two fact tables related to the same dimensions; models of any size.

**T01-A314-3.** Table filters in CALCULATE can force the storage engine to retrieve the key combinations of related tables in order to intersect them. That builds a large datacache that is slow to process; the slowdown is smaller, but present, on a small database.
- Fact. 2024. https://www.sqlbi.com/articles/filter-columns-not-tables-in-dax/
- When: A CALCULATE filter argument is a whole table with related tables.

**T01-A124-2.** A table is expanded when it is defined: a table stored in a variable while USERELATIONSHIP had activated another relationship keeps that expansion, and RELATED over its rows later follows that relationship, not the one active when RELATED runs.
- Fact. 2018. https://www.sqlbi.com/articles/expanded-tables-in-dax/
- When: Variables or table expressions are built under USERELATIONSHIP and iterated later.

**T01-A124-3.** RELATED always uses the active relationship and has no way to name another. USERELATIONSHIP needs CALCULATE, which removes the row context RELATED requires, so a calculated column written that way fails with an error.
- Fact. 2018. https://www.sqlbi.com/articles/expanded-tables-in-dax/
- When: A calculated column needs a related value through an inactive relationship.
- Version: Stated in 2018: DAX then had no syntax for passing USERELATIONSHIP to RELATED.

**T01-A124-4.** In a calculated column that needs a dimension value through an inactive relationship, use LOOKUPVALUE on the key column. Never combine CALCULATE, USERELATIONSHIP, ALL on the dimension and an inner iterator calling RELATED: that returns the right value but is slower and less safe.
- Must. 2018. https://www.sqlbi.com/articles/expanded-tables-in-dax/
- When: A calculated column reads a related attribute through a key whose relationship is inactive.

**T01-A124-5.** USERELATIONSHIP adds no filter; it only changes which relationship table expansion uses inside CALCULATE. Context transition still follows the originally active relationship, so in a calculated column CALCULATE over VALUES of a dimension column, with USERELATIONSHIP and ALL on the dimension, sees every dimension row.
- Fact. 2018. https://www.sqlbi.com/articles/expanded-tables-in-dax/
- When: A calculated column tries to read a dimension attribute through an inactive relationship.

**T01-A124-6.** In a calculated column, one way to read a dimension attribute through an inactive relationship is CALCULATE with TREATAS, which moves the current row's key as a filter onto the dimension key; ALL on the dimension is not needed, since the TREATAS filter overrides it.
- Option. 2018. https://www.sqlbi.com/articles/expanded-tables-in-dax/
- When: The relationship on that key is inactive; the approach does not rely on table expansion.

**T01-A142-1.** A column in a table expression keeps its data lineage, and so can filter model tables, only as a plain column reference. Renaming keeps lineage; any expression around the column, even appending an empty string, gives a new lineage unrelated to the model.
- Fact. 2019. https://www.sqlbi.com/articles/understanding-data-lineage-in-dax/
- When: Columns of a table expression are expected to filter model tables.

**T01-A142-2.** A table used as a CALCULATE filter argument filters only through columns that carry model lineage: a column added with an aggregation such as MIN inside ADDCOLUMNS has no such lineage and applies no filter, so the result can be the unfiltered total.
- Fact. 2019. https://www.sqlbi.com/articles/understanding-data-lineage-in-dax/
- When: A filter table mixes model columns and computed columns, such as a product and its first sale date.

**T01-A142-3.** To let a computed table column filter the model, TREATAS can give it the lineage of a model column: it returns the input table with each column tagged as the model column listed.
- Option. 2019. https://www.sqlbi.com/articles/understanding-data-lineage-in-dax/
- When: A table built in DAX must filter model tables; rows without a match are dropped.
- Version: In a February 2023 retest the simpler original measure outperformed the TREATAS version; the technique may still suit other cases.

**T01-A142-4.** When TREATAS applies a model column's lineage to a table, rows whose values do not exist in that model column are dropped from the result.
- Fact. 2019. https://www.sqlbi.com/articles/understanding-data-lineage-in-dax/
- When: The table given to TREATAS may hold values with no match in the target column.

**T01-A249-3.** RELATED fails with an error when any relationship it must cross is limited instead of regular, as when the two tables sit in different data islands. DirectQuery alone is not the cause: with both tables in DirectQuery, RELATED works.
- Fact. 2022. https://www.sqlbi.com/articles/using-related-and-relatedtable-in-dax/
- When: RELATED is used between tables that may belong to different data islands.

**T01-A249-6.** Unlike RELATED, RELATEDTABLE can cross a limited relationship, because it works through context transition as CALCULATETABLE does. Calculated columns in DirectQuery tables cannot use RELATEDTABLE.
- Fact. 2022. https://www.sqlbi.com/articles/using-related-and-relatedtable-in-dax/
- When: A measure iterates a table that sits in a separate data island.

**T01-A249-7.** RELATED follows whichever relationship is currently active. Making it use an inactive relationship is far harder than it looks.
- Fact. 2022. https://www.sqlbi.com/articles/using-related-and-relatedtable-in-dax/
- When: A calculation needs RELATED across an inactive relationship.

### Context transition

**T01-A315-1.** When an expression inside an iterator must ignore the filter that context transition creates for the current row, one option is an explicit CALCULATE with REMOVEFILTERS on the iterated table. In simple cases, computing the value before the iteration is the better choice.
- Option. 2024. https://www.sqlbi.com/articles/context-transition-in-dax-explained-visually/
- When: Inside an iteration, a value must cover all iterated rows in the current filter context.

**T01-A064-2.** CALCULATE and CALCULATETABLE first turn every active row context into an equivalent filter context, then apply their filter arguments. Even with no filter argument, CALCULATE in a calculated column limits an aggregation to the current row, plus identical duplicates, and that filter reaches related tables.
- Fact. 2015. https://www.sqlbi.com/articles/understanding-context-transition/
- When: CALCULATE or CALCULATETABLE runs where a row context exists, such as a calculated column.

**T01-A064-3.** Context transition isolates exactly one row only in a table without duplicate rows, as a primary key guarantees: the filter is placed on the values of all columns of the row, not on a row number, so identical rows are all kept.
- Fact. Check. 2015. https://www.sqlbi.com/articles/understanding-context-transition/
- When: Code relies on CALCULATE's context transition to pick out one row.

**T01-A064-6.** An explicit CALCULATE around a measure reference adds nothing: the engine already surrounds every measure reference with CALCULATE.
- Fact. Check. 2015. https://www.sqlbi.com/articles/understanding-context-transition/
- When: Code wraps a measure in CALCULATE only to request context transition.

**T01-A064-8.** When a row-by-row condition must compare each item with an overall total, another way is to store the total in a variable evaluated outside the iteration and use it in the condition: a variable is evaluated in one context and can be used in another.
- Option. Check. 2015. https://www.sqlbi.com/articles/understanding-context-transition/
- When: A FILTER condition or other iteration needs a value not restricted to the current row.

**T01-A118-1.** Context transition by CALCULATE or CALCULATETABLE reaches only the first argument. Filter arguments are evaluated in the filter context that existed before the call, so FILTER or SELECTEDVALUE in a filter argument inside an iterator reads the outer context and not the iterated row.
- Fact. 2017. https://www.sqlbi.com/articles/context-transition-and-expanded-tables/ ; https://www.sqlbi.com/articles/context-transition-and-filters-in-calculate/
- When: CALCULATE runs in an iterator's row context with filter arguments that read the filter context.

**T01-A118-2.** When a CALCULATE filter argument must see the row an outer iterator is on, one fix is to wrap the expression inside that filter argument in its own CALCULATE or CALCULATETABLE, so that it gets a context transition.
- Option. 2018. https://www.sqlbi.com/articles/context-transition-and-filters-in-calculate/
- When: A filter argument inside an iterator reads the filter context, for example with SELECTEDVALUE.

**T01-A118-3.** When a CALCULATE filter argument needs the value of the row an outer iterator is on, another fix is to reference the iterated column directly: filter arguments get no context transition, so the outer row context is still available in them.
- Option. 2018. https://www.sqlbi.com/articles/context-transition-and-filters-in-calculate/
- When: A filter argument inside an iterator must use a value of the current row.

**T01-A118-5.** A time intelligence function given a column reference treats it as CALCULATETABLE over VALUES of the column, so it performs a context transition in a row context: SAMEPERIODLASTYEAR as a CALCULATE filter inside an iterator follows the iterated row with no extra CALCULATE.
- Fact. 2018. https://www.sqlbi.com/articles/context-transition-and-filters-in-calculate/
- When: Time intelligence functions receive a column reference while a row context exists.

**T01-A118-6.** CALCULATE evaluates its filter arguments in the existing filter context, then performs context transition, then applies the filter arguments. A filter argument can therefore overwrite the transition's filter: ALL on a column of the iterated table also removes the current row's filter on it.
- Fact. Check. 2015. https://www.sqlbi.com/articles/understanding-context-transition/ ; https://www.sqlbi.com/articles/context-transition-and-expanded-tables/ ; https://www.sqlbi.com/articles/context-transition-and-filters-in-calculate/
- When: CALCULATE in a row context has filter arguments on columns the context transition also filters.

**T01-A247-4.** Replacing a measure reference with the measure's own expression changes the result where a row context exists. In a calculated column of Customer, the reference returns the current customer's sales; the pasted expression lacks the implicit CALCULATE and returns the sales of all customers.
- Fact. 2022. https://www.sqlbi.com/articles/understanding-context-transition-in-dax/
- When: A measure's code runs in a row context, by reference or written inline.

**T01-A247-5.** Context transition filters every column the row context iterates. A transition while iterating a whole table therefore costs much more than one over a single-column table, and the time grows with the number of columns.
- Fact. 2022. https://www.sqlbi.com/articles/understanding-context-transition-in-dax/
- When: Context transition over an entire table, as in a calculated column, where all expanded-table columns are filtered.

**T01-A247-6.** In a running total whose FILTER over ALL dates compares each date with the latest date, a measure reference for that date triggers context transition and returns the iterated date: every cell shows the grand total. MAX used directly reads the outer filter context.
- Fact. 2022. https://www.sqlbi.com/articles/understanding-context-transition-in-dax/
- When: The condition of a running total is evaluated while iterating ALL of the date table.

**T01-A249-5.** RELATEDTABLE is CALCULATETABLE under another name. Its context transition turns every row context active at that point into filters, including outer row contexts over columns the inner iteration does not restrict.
- Fact. 2022. https://www.sqlbi.com/articles/using-related-and-relatedtable-in-dax/
- When: Nested row contexts, such as iterating year values inside a calculated column of a dimension.

### Removing filters with ALL

**T01-A085-2.** As a CALCULATE modifier ALLEXCEPT only removes filters. A listed column whose visible values come only from a cross-filter by another column of the same table keeps nothing, so every filter on the table goes; ALL on the table plus VALUES keeps those cross-filtered values.
- Fact. 2016. https://www.sqlbi.com/articles/using-allexcept-vs-all-values/ ; https://www.sqlbi.com/articles/using-allexcept-versus-all-and-values/
- When: The kept column is filtered indirectly or not at all, as when a coarser grouping column is filtered.

**T01-A085-3.** Consider ALLEXCEPT as a CALCULATE modifier for advanced cases, such as removing circular dependencies in calculated columns, not for everyday measures. It need not be avoided entirely: in some scenarios it makes sense and works well.
- Consider. 2021. https://www.sqlbi.com/articles/using-allexcept-versus-all-and-values/
- When: Advanced scenarios, for example a circular dependency between calculated columns.

**T01-A085-4.** When filters on several columns of a table must be kept after all its filters are removed, SUMMARIZE of the table by those columns can be the restoring filter in place of VALUES, which covers one column only.
- Option. 2021. https://www.sqlbi.com/articles/using-allexcept-versus-all-and-values/
- When: REMOVEFILTERS on a table, with more than one column filter to retain.

**T01-A228-7.** When ALLEXCEPT keeps a column's selection, an alternative fix for lost cross-filters is to also list every coarser column that groups its values. It needs fewer scans and is slightly faster, but the measure must be updated whenever such a column is added.
- Option. 2016. https://www.sqlbi.com/articles/using-allexcept-vs-all-values/
- When: Users may filter columns coarser than the kept one; the gain was hardly visible on a small table.

**T01-A361-3.** When a legacy DAX pattern depends on ALL working both as a table function and as a filter remover, write it with ALL.
- Should. 2026. https://www.sqlbi.com/articles/all-vs-allselected-vs-allexcept-vs-removefilters/
- When: Older patterns that need ALL as both table function and CALCULATE modifier.

**T01-A361-4.** Every ALL-prefixed function can be a table function or a CALCULATE modifier. As a filter argument it only removes filters and passes no table, so ALL over a fact table does not limit the result to its rows. REMOVEFILTERS is ALL's only alias, modifier only.
- Fact. 2018. https://www.sqlbi.com/articles/managing-all-functions-in-dax-all-allselected-allnoblankrow-allexcept/ ; https://www.sqlbi.com/articles/all-vs-allselected-vs-allexcept-vs-removefilters/
- When: An ALL-family function is written as a CALCULATE filter argument.
- Version: REMOVEFILTERS was introduced in August 2019.

**T01-A361-5.** REMOVEFILTERS and ALL clear the filters on a column whichever visual set them. A measure built with them also drops slicer and other-visual selections, and can show a total that nothing in the report lets users explain.
- Fact. 2026. https://www.sqlbi.com/articles/all-vs-allselected-vs-allexcept-vs-removefilters/
- When: A measure removes filters on a column filtered by both the current visual and a slicer.

**T01-A122-2.** When a CALCULATE filter needs the rows ALL returns, not just filter removal, one option is to wrap ALL in CALCULATETABLE, so that its table result is really used as the filter; ALL alone in a filter argument only removes filters.
- Option. 2018. https://www.sqlbi.com/articles/managing-all-functions-in-dax-all-allselected-allnoblankrow-allexcept/
- When: A filter argument must filter by all rows of a table, for example a fact table.

**T01-A122-3.** Another way to make ALL pass its rows to a CALCULATE filter is to wrap it in FILTER with a condition that is always true; this is the less elegant form.
- Option. 2018. https://www.sqlbi.com/articles/managing-all-functions-in-dax-all-allselected-allnoblankrow-allexcept/
- When: A filter argument must filter by all rows of a table, not just remove filters.

**T01-A122-5.** ALL with a table, as a CALCULATE filter argument, clears the filters of the whole expanded table: ALL on a fact table also removes the filters placed on its related dimension tables.
- Fact. 2018. https://www.sqlbi.com/articles/managing-all-functions-in-dax-all-allselected-allnoblankrow-allexcept/
- When: ALL with a table argument is written as a CALCULATE filter argument.

**T01-A122-6.** ALLEXCEPT with a fact table as first argument removes filters from that table's expanded version: every table reachable through many-to-one relationships, such as Customer, Date and Store, not only the fact table's own columns.
- Fact. 2018. https://www.sqlbi.com/articles/managing-all-functions-in-dax-all-allselected-allnoblankrow-allexcept/
- When: ALLEXCEPT is a CALCULATE filter argument on a table with many-to-one relationships.

**T01-A122-7.** To keep the filters on some related tables when ALLEXCEPT is used on a fact table, add those tables as further ALLEXCEPT arguments: any table or column within the expanded version of the first argument can be listed.
- Option. 2018. https://www.sqlbi.com/articles/managing-all-functions-in-dax-all-allselected-allnoblankrow-allexcept/
- When: ALLEXCEPT over a fact table must preserve filters on some dimension tables.

**T01-A324-1.** As a CALCULATE modifier with a table argument, ALL or REMOVEFILTERS clears filters only from that table's expanded table. Expansion follows regular relationships only, so filters arriving from tables linked through a limited relationship stay in place.
- Fact. 2025. https://www.sqlbi.com/articles/differences-between-all-and-allcrossfiltered/
- When: The model has limited relationships: many-to-many cardinality, different data islands, or local-to-remote tables in a composite model.

**T01-A324-2.** When every filter that affects a table must go, including filters from tables that cross-filter it through limited relationships or bidirectional cross-filters, use ALLCROSSFILTERED as the CALCULATE modifier instead of ALL or REMOVEFILTERS.
- Should. 2025. https://www.sqlbi.com/articles/differences-between-all-and-allcrossfiltered/
- When: Models with limited relationships or bidirectional cross-filters connected to the table.

**T01-A324-4.** ALLCROSSFILTERED is accepted only as a filter modifier inside CALCULATE and cannot return a table. Its single parameter is a table name.
- Fact. 2025. https://www.sqlbi.com/articles/differences-between-all-and-allcrossfiltered/
- When: Writing a call to ALLCROSSFILTERED.
