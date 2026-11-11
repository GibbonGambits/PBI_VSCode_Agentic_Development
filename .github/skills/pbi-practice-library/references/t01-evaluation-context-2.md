# DAX evaluation context

Part 2 of 3 of this topic. Covers: Reading the selected value; Row context and iterators; Relationships, expanded tables and lineage.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

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

## Special-case techniques and facts

### Reading the selected value

**T01-A058-1.** To give a measure parameter values, one option is a hidden table per parameter holding every value needed: call the measure in CALCULATE with a filter that sets the column to the wanted value, and let the measure read it with VALUES.
- Option. Check. 2015. https://www.sqlbi.com/articles/parameters-in-dax-measures/
- When: Complex expressions compute a measure with different argument values; simple cases can keep the condition in inner measures.
- Version: Written in 2015, when DAX had no way to pass arguments to a measure.

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
