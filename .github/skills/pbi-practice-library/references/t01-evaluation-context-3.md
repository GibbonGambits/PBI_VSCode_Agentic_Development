# DAX evaluation context

Part 3 of 3 of this topic. Covers: Context transition; Removing filters with ALL; ALLSELECTED and shadow filters; Totals and additivity.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

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

### ALLSELECTED and shadow filters

**T01-A120-2.** Rely on variables so that ALLSELECTED does not have to be called inside an iteration; this is possible in most scenarios, not all.
- Should. 2018. https://www.sqlbi.com/articles/the-definitive-guide-to-allselected/
- When: Code would otherwise call ALLSELECTED inside an iteration.

**T01-A254-2.** Choose the argument of ALLSELECTED with care after checking the requirement: a column restores the outer filters on that column, a table on all its columns, and no argument on every table of the model.
- Consider. 2022. https://www.sqlbi.com/articles/introducing-allselected-in-dax/
- When: Writing any ALLSELECTED call.

### Totals and additivity

**T01-A259-1.** Avoid forcing a naturally non-additive measure, such as a distinct count, to be additive by iterating a column and summing the partial results so the total matches the rows. The forced total is mostly wrong and changes with the column the report is sliced by.
- Should. 2022. https://www.sqlbi.com/articles/why-power-bi-totals-might-seem-inaccurate/
- When: Users want a total to equal the sum of rows; adding an iteration is only occasionally right.

**T01-A259-2.** When users ask that the total of an average measure be the average of the visible rows, keep the total as a new average over all underlying data. An average of averages is a different, rarely wanted number.
- Should. 2022. https://www.sqlbi.com/articles/why-power-bi-totals-might-seem-inaccurate/
- When: Average measures shown with totals in a matrix or table.

**T01-A259-3.** When a requirement is defined at a specific level of detail, such as summing sales only for countries above a threshold, you must agree that level with the users, iterate over it in the measure and aggregate the per-item results afterwards.
- Must. 2022. https://www.sqlbi.com/articles/why-power-bi-totals-might-seem-inaccurate/
- When: A measure's logic must be evaluated per item of some entity, such as a threshold per country.

## Special-case techniques and facts

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

### ALLSELECTED and shadow filters

**T01-A120-3.** In nested iterations, one way to reach the outer selection from the inner iteration is to evaluate ALLSELECTED into a variable before the inner iterator starts: ALLSELECTED cannot step back past the latest shadow filter context, as EARLIER can for row contexts.
- Option. 2018. https://www.sqlbi.com/articles/the-definitive-guide-to-allselected/
- When: Code in an inner iteration needs the values selected at the outer iteration's level.

**T01-A120-5.** A Power BI matrix and an Excel pivot table compute the measure in each cell through the equivalent of a DAX iterator over the combinations of the attributes placed on rows and columns.
- Fact. 2018. https://www.sqlbi.com/articles/the-definitive-guide-to-allselected/
- When: Reasoning about ALLSELECTED in measures shown in a matrix or pivot table.

**T01-A120-6.** Every iterator creates a shadow filter context holding the rows it iterates. It is inactive and changes no result unless ALLSELECTED turns it on, so shadow filter contexts can be ignored except where ALLSELECTED is used.
- Fact. 2018. https://www.sqlbi.com/articles/the-definitive-guide-to-allselected/
- When: Whenever ALLSELECTED is used.

**T01-A120-7.** With a column argument, ALLSELECTED ignores the current filter context, explicit filters and cross-filters alike, and returns the column's values from the most recent shadow filter context that filters it, or all values if none does. VALUES and DISTINCT always respect the filter context.
- Fact. 2018. https://www.sqlbi.com/articles/the-definitive-guide-to-allselected/
- When: ALLSELECTED is called with one column.

**T01-A120-8.** With a table argument, ALLSELECTED applies the most recent shadow filter to each column that has one and keeps explicit filters on the other columns; with no shadow filter context it returns the rows of the last explicit filter context.
- Fact. 2018. https://www.sqlbi.com/articles/the-definitive-guide-to-allselected/
- When: ALLSELECTED is called with a table, which differs from the column form.

**T01-A120-9.** ALLSELECTED with no argument is not a table function: it works only as a CALCULATE filter argument, restoring the latest shadow filter context on each column that has one. In nested iterators the results can look wrong; an older explanation blamed a removed context-transition filter.
- Fact. 2018. https://www.sqlbi.com/articles/the-definitive-guide-to-allselected/ ; https://www.sqlbi.com/articles/understanding-allselected/
- When: ALLSELECTED without arguments in CALCULATE, above all inside nested iterators.

**T01-A120-10.** As a CALCULATE filter argument, ALLSELECTED turns the shadow filter context into an explicit filter that takes precedence over the context-transition filter; it seems to remove that filter, but nothing is removed. An older explanation said it drops the latest context-transition filter.
- Fact. 2018. https://www.sqlbi.com/articles/the-definitive-guide-to-allselected/ ; https://www.sqlbi.com/articles/understanding-allselected/
- When: ALLSELECTED is a CALCULATE filter argument where a context transition also occurs.

**T01-A120-11.** ALLSELECTED with a column, as a CALCULATE filter argument, works much like ALL and removes filters on that column. With no shadow filter context from an iterator it applies no filter itself: a restricted list of values inside comes from cross-filtering seen by VALUES.
- Fact. 2018. https://www.sqlbi.com/articles/the-definitive-guide-to-allselected/
- When: ALLSELECTED on a column is used as a CALCULATE modifier.

**T01-A254-3.** ALLSELECTED can also be a table expression that returns the values selected outside the current visual, for example to iterate the selected brands with MINX and MAXX. It is treated as safe only in a measure placed directly in the report.
- Option. 2022. https://www.sqlbi.com/articles/introducing-allselected-in-dax/
- When: A calculation must consider only the items selected outside the current visual.

**T01-A338-3.** When an iteration needs the total of the current selection from a measure based on ALLSELECTED, call that measure before the iteration starts: with no shadow filter context it returns all the selected items, not only those of the current group.
- Should. 2025. https://www.sqlbi.com/articles/allselected-best-practices/
- When: A measure iterates rows and compares each with a selection-wide total from an ALLSELECTED measure.

**T01-A338-4.** ALLSELECTED has no notion of a visual. Evaluated directly in SUMMARIZECOLUMNS it removes the filter on the current group-by column and restores the filter SUMMARIZECOLUMNS set; inside an iterator it restores the last shadow filter context, which holds only the rows being iterated.
- Fact. 2025. https://www.sqlbi.com/articles/allselected-best-practices/
- When: ALLSELECTED evaluated inside an iterator, as opposed to directly in the query Power BI generates.
- Version: Power BI uses SUMMARIZECOLUMNS for nearly all visuals; early versions used iterators such as ADDCOLUMNS.

### Totals and additivity

**T01-A259-4.** Combining a context-dependent value with a constant, such as subtracting a fixed number from a count, gives a non-additive measure: its total applies the constant once, not once per row.
- Fact. 2022. https://www.sqlbi.com/articles/why-power-bi-totals-might-seem-inaccurate/
- When: A measure combines a constant with a value that depends on the filter context.

**T01-A259-5.** Power BI computes a total by evaluating the measure at the aggregated level, not by adding up the rows shown. A total that looks wrong therefore points to a non-additive calculation in the DAX code.
- Fact. 2022. https://www.sqlbi.com/articles/why-power-bi-totals-might-seem-inaccurate/
- When: A total in a visual does not equal the sum of its rows.
