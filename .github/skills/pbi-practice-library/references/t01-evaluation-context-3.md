# DAX evaluation context

Part 3 of 3 of this topic. Covers: ALLSELECTED and shadow filters; Totals and additivity.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

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
- Fact. 2018. https://www.sqlbi.com/articles/the-definitive-guide-to-allselected/
- When: ALLSELECTED without arguments in CALCULATE, above all inside nested iterators.

**T01-A120-10.** As a CALCULATE filter argument, ALLSELECTED turns the shadow filter context into an explicit filter that takes precedence over the context-transition filter; it seems to remove that filter, but nothing is removed. An older explanation said it drops the latest context-transition filter.
- Fact. 2018. https://www.sqlbi.com/articles/the-definitive-guide-to-allselected/
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
