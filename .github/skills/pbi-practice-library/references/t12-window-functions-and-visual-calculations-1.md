# Window functions and visual calculations

Part 1 of 1 of this topic. Covers: Measure or visual calculation; Window functions and apply semantics; Ranking with RANK and RANKX; Visual context and virtual table; Running totals and performance.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### Measure or visual calculation

**T12-A302-9.** Choose between a visual calculation and a model measure only after weighing both for the scenario at hand. A well-designed measure, though more intricate to write, still works when the hierarchy columns are missing from the visual, and can become a calculation item.
- Must. 2024. https://www.sqlbi.com/articles/using-expand-and-collapse-in-visual-calculations/
- When: Deciding where a calculation for a report should live.

**T12-A327-1.** When a value exists only to drive conditional formatting in one visual, such as a font or background colour, consider a visual calculation over a model measure: simpler to write, independent of the slicing column, and it keeps visual-specific logic out of the model.
- Consider. Check. 2025. https://www.sqlbi.com/articles/using-visual-calculations-for-conditional-formatting/
- When: Formatting tied to one visual; even somewhat complex logic gets very hard to write as a visual calculation.
- Version: From the February 2025 release visual calculations can drive conditional formatting; a preview then, generally available since May 2026.

**T12-A357-1.** Avoid model measures whose only job is the look of one visual, such as highlighting rows; put that logic in a visual calculation. Such measures multiply, clutter the model and need rewriting when the visual's structure changes.
- Should. 2026. https://www.sqlbi.com/articles/using-visual-calculations-to-highlight-an-entire-row/
- When: Formatting logic tied to one visual; the code can be less intuitive, moving through the lattice with EXPAND and COLLAPSE.

**T12-A357-2.** When a visual calculation would repeat the same column and measure names in several places, move the generic logic into a user-defined function that takes the matrix table, the needed columns and the expression as parameters, so the names appear only in the call.
- Should. 2026. https://www.sqlbi.com/articles/using-visual-calculations-to-highlight-an-entire-row/
- When: Visual calculations that must be adapted to visuals with different measures or column layouts.
- Version: This template suggests a function at the end of a task and builds it after the developer's yes (native features; U001).

### Window functions and apply semantics

**T12-A266-1.** INDEX, OFFSET and WINDOW are one way to write calculations that move across a sorted table: a month against the previous one, the price change since the previous sale, a moving average. Other DAX can do the same; these aim to be simpler and faster.
- Option. 2023. https://www.sqlbi.com/articles/introducing-window-functions-in-dax/
- When: A calculation needs absolute or relative rows of a sorted, possibly partitioned table.
- Version: INDEX, OFFSET and WINDOW were added to DAX in December 2022.

**T12-A266-5.** When writing OFFSET, check two filter contexts with care: the one coming from the visual, and the one in which OFFSET itself is evaluated. A filter on years can leave the default source table without a previous row for the first visible year.
- Should. 2023. https://www.sqlbi.com/articles/introducing-window-functions-in-dax/
- When: Calculations that use OFFSET to reach a previous or next row.

**T12-A266-7.** Before putting ALL in the source table of a window function, weigh what the previous or next row should be for that dimension. With ALL the neighbour no longer follows what the visual shows: mostly wanted for dates, not right for every dimension.
- Consider. 2023. https://www.sqlbi.com/articles/introducing-window-functions-in-dax/
- When: Reaching previous or next rows over any dimension with a window function.

**T12-A266-8.** Apply semantics can turn the single row that INDEX or OFFSET would return into several rows when several current rows exist, and makes WINDOW return the union of the windows of all current rows. Give WINDOW results extra attention.
- Consider. 2023. https://www.sqlbi.com/articles/introducing-window-functions-in-dax/
- When: Window functions evaluated where more than one current row exists.

**T12-A266-9.** Watch performance when using window functions: they are usually very fast, but in some scenarios more traditional DAX code runs faster.
- Consider. 2023. https://www.sqlbi.com/articles/introducing-window-functions-in-dax/
- When: Choosing between INDEX, OFFSET or WINDOW and an older DAX formulation.

**T12-A303-4.** MATCHBY can state which columns a window function uses in the matching step that finds the current row. Only model columns can be listed in it.
- Option. 2024. https://www.sqlbi.com/articles/understanding-apply-semantics-for-window-functions-in-dax/
- When: Controlling how a window function identifies its current row.

**T12-A303-5.** Never assume that a measure containing a window function will always be evaluated in one particular filter context. Write it so that it works in any scenario: correct behaviour in every filter context is a basic principle of DAX measures.
- Must. 2024. https://www.sqlbi.com/articles/understanding-apply-semantics-for-window-functions-in-dax/
- When: Measures that use window functions such as OFFSET.

### Ranking with RANK and RANKX

**T12-A278-4.** Build the source table of a window function such as RANK beforehand, with the ordering value already computed in it, instead of building it inside the call. The code reads more clearly, and the query plan is sometimes better.
- Should. 2023. https://www.sqlbi.com/articles/introducing-the-rank-window-function-in-dax/
- When: Writing RANK or another window function over a computed table.

**T12-A278-5.** When writing the source table of a ranking, work out exactly which parts of the filter context it replaces. Columns it does not override keep filtering, so the ranking turns local to them: overriding only brand restarts the rank within each category.
- Should. 2023. https://www.sqlbi.com/articles/introducing-the-rank-window-function-in-dax/
- When: Ranking with RANK over a precomputed source table.

**T12-A348-1.** Prefer RANK to RANKX for ranking, in measures and in visual calculations: it is faster, simpler to write and more flexible. Rare exceptions: placing a value within a lookup table, and a table made only of columns added by DAX table functions.
- Should. 2023. https://www.sqlbi.com/articles/introducing-the-rank-window-function-in-dax/ ; https://www.sqlbi.com/articles/using-rank-instead-of-rankx-in-dax/
- When: Writing a new ranking calculation.
- Version: RANK joined the DAX window functions in 2023; RANKX is the older ranking function.

**T12-A348-2.** For a simple ranking that may respond to every filter on the visual (a local ranking), rank over ROWS in a visual calculation, not in a measure. It works whatever column is on the axis; a measure turns blank when its ranked column is swapped.
- Should. 2025. https://www.sqlbi.com/articles/using-rank-instead-of-rankx-in-dax/
- When: Rankings that should not depend on the column shown; not for a global ranking that ignores report filters.

**T12-A348-4.** Wrap a ranking in an IF test so that no rank appears on the total row: ISINSCOPE for a RANKX measure, ISATLEVEL for a RANK visual calculation. Without the test both show a value on the total; a RANK measure needs none.
- Must. 2025. https://www.sqlbi.com/articles/using-rank-instead-of-rankx-in-dax/
- When: A ranking measure that uses RANKX, or a ranking visual calculation, in a visual with a total row.

**T12-A348-6.** When the ranking expression is a floating-point value, use RANK, not RANKX: RANKX can return a wrong ranking on such values, an issue RANK does not have. This also holds for existing RANKX measures that otherwise work.
- Should. 2025. https://www.sqlbi.com/articles/using-rank-instead-of-rankx-in-dax/
- When: Ranking over decimal (floating-point) expressions.
- Version: Changing a measure that works needs the developer's yes (model skill, existing models; pbi-improve).

**T12-A348-8.** Existing RANKX measures that return correct results can stay as they are; replacing them with RANK is not required. The exception is a RANKX measure that ranks floating-point values, where RANK works better.
- Option. 2025. https://www.sqlbi.com/articles/using-rank-instead-of-rankx-in-dax/
- When: Reviewing existing ranking measures.

### Visual context and virtual table

**T12-A298-1.** Before writing complex visual calculations, learn how they are implemented: the hierarchical structure of their virtual table, the visual context, what ROWS and COLUMNS mean, how CALCULATE behaves there, and the EXPAND and COLLAPSE modifiers.
- Should. Check. 2024. https://www.sqlbi.com/articles/introducing-visual-shape-for-visual-calculations-in-power-bi/
- When: Complex visual calculations; simple ones are straightforward.
- Version: Visual calculations arrived as a preview in February 2024; generally available since Microsoft's May 2026 release notes.

**T12-A301-1.** Do not reason about a visual calculation with row context or filter context. It runs in a separate visual context: no row context exists, nothing is iterated by default, and the visual context, not the filter context, drives the filtering.
- Must. 2024. https://www.sqlbi.com/articles/introducing-expand-and-collapse-for-visual-calculations/
- When: Writing or reviewing visual calculations, above all for people used to DAX measures.

**T12-A301-4.** When a visual calculation evaluates an expression after EXPAND, wrap column references in an aggregation function so that one scalar value results: EXPAND moves down one or more levels and exposes several descendant rows of the current row.
- Must. 2024. https://www.sqlbi.com/articles/introducing-expand-and-collapse-for-visual-calculations/
- When: Visual calculations using EXPAND; also after COLLAPSE when the engine cannot tell that only one row results.

**T12-A301-5.** When a visual calculation applies a filter through CALCULATE, always check that the filtered column is available in two places: the filter argument, and the expression that CALCULATE evaluates.
- Must. 2024. https://www.sqlbi.com/articles/introducing-expand-and-collapse-for-visual-calculations/
- When: A visual calculation filters with CALCULATE while navigating the visual context with EXPAND or COLLAPSE.

**T12-A301-6.** EXPAND, EXPANDALL, COLLAPSE and COLLAPSEALL can be written in scalar form, taking the expression directly, instead of as modifiers inside CALCULATE. The scalar form is only shorthand for the CALCULATE form.
- Option. 2024. https://www.sqlbi.com/articles/introducing-expand-and-collapse-for-visual-calculations/
- When: Visual calculations that navigate the visual context.

**T12-A302-1.** Control how a visual calculation is displayed by giving it a format string, in preference to turning its result into text with FORMAT inside the expression.
- Should. 2024. https://www.sqlbi.com/articles/using-expand-and-collapse-in-visual-calculations/
- When: Formatting the result of a visual calculation.
- Version: Not possible in 2024. A format string set on one visual counts as preview here: needs the developer's yes.

**T12-A302-3.** In a visual calculation of more than trivial complexity, first move the visual context to the level the calculation requires, with EXPAND and COLLAPSE, and only then compute it. The result is not correct otherwise.
- Must. 2024. https://www.sqlbi.com/articles/using-expand-and-collapse-in-visual-calculations/
- When: Visual calculations beyond simple ones such as the predefined templates.

**T12-A302-6.** When a visual calculation iterates the rows of the current visual context, wrap ROWS in VALUES or DISTINCT; do not iterate ROWS directly. In the visual context, ROWS by itself behaves like ALL applied to ROWS.
- Must. 2024. https://www.sqlbi.com/articles/using-expand-and-collapse-in-visual-calculations/
- When: Iterations over the ROWS axis in a visual calculation.

**T12-A302-11.** Predefined visual calculation templates, percentage of the parent among them, let an author add such calculations without managing the visual context, its level in the lattice, or the moves between levels.
- Option. 2024. https://www.sqlbi.com/articles/using-expand-and-collapse-in-visual-calculations/
- When: A common calculation is needed on one visual.

### Running totals and performance

**T12-A320-6.** Base the performance choice between visual calculations and regular DAX measures on a study of the specific scenario: neither is faster as a rule.
- Must. 2024. https://www.sqlbi.com/articles/computing-open-orders-with-visual-calculations-in-dax/
- When: Choosing between a visual calculation and a measure for speed.
- Version: This template restates Microsoft: an equivalent model measure is often slower. Test the case.

**T12-A320-7.** Visual calculations can serve to try out a calculation technique that is then rewritten as a regular DAX measure with better performance.
- Option. 2024. https://www.sqlbi.com/articles/computing-open-orders-with-visual-calculations-in-dax/
- When: Prototyping a calculation before it is optimised.

**T12-A365-1.** Consider a visual calculation for speed when a visual applies further computation, such as a year-over-year comparison with PREVIOUS, on top of a few expensive base measures: it reuses values already in the virtual table instead of sending more storage engine queries.
- Consider. 2026. https://www.sqlbi.com/articles/analyzing-the-performance-impact-of-visual-calculations/
- When: A few heavy base measures, such as distinct counts, in a modest-size visual; speed is not their main goal.

**T12-A365-2.** Never assume a visual calculation is faster than the equivalent measure. It can make a report several times slower when the visual's virtual table is large, because the densification step it requires can take long on large tables.
- Must. 2026. https://www.sqlbi.com/articles/analyzing-the-performance-impact-of-visual-calculations/
- When: Small virtual tables suit visual calculations; the risk grows with the size of the virtual table.
- Version: This template restates Microsoft: an equivalent model measure is often slower. Test the case.

**T12-A365-3.** Keep in mind that a measure-based matrix computes only the levels currently visible. A visual calculation always makes the engine build the complete densified virtual table at leaf granularity, whether or not the levels are expanded.
- Consider. 2026. https://www.sqlbi.com/articles/analyzing-the-performance-impact-of-visual-calculations/
- When: Matrix visuals with hierarchies whose levels may stay collapsed.

**T12-A365-5.** Test performance extensively on your own model, measures and report before choosing between visual calculations and measures for speed. Results can differ widely from a demo model; on a small database the storage engine cost becomes negligible, which skews the comparison.
- Should. 2026. https://www.sqlbi.com/articles/analyzing-the-performance-impact-of-visual-calculations/
- When: Performance decisions about visual calculations versus measures.

## Special-case techniques and facts

### Measure or visual calculation

**T12-A196-1.** A model measure is one expression, evaluated for every cell of a visual. Unlike spreadsheet cells, the cells of a visual cannot each hold a formula of their own, so the logic has to work the same way on every row.
- Fact. 2020. https://www.sqlbi.com/articles/a-proposal-for-visual-calculations-in-dax/
- When: Writing any measure that a report visual will show.

**T12-A196-2.** A model measure cannot refer to what a visual displays, such as the preceding row of a matrix or the subtotal at year level: the engine that evaluates measures knows tables and relationships, not visuals.
- Fact. Check. 2020. https://www.sqlbi.com/articles/a-proposal-for-visual-calculations-in-dax/
- When: A calculation needs a value from another row or level of the same visual.
- Version: Stated in 2020, before visual calculations existed.

**T12-A196-3.** A measure that returns the share of the category total by naming the category column explicitly is right only while the report is sliced by category. Sliced by any other column, it fails.
- Fact. Check. 2020. https://www.sqlbi.com/articles/a-proposal-for-visual-calculations-in-dax/
- When: Percent-of-parent measures written against specific model columns.
- Version: Stated in 2020, when DAX offered no calculation that worked whatever the slicing column.

**T12-A196-5.** A share of the grand total shown can divide the sales total by the same total under CALCULATE with ALLSELECTED and no arguments. Adding VALUES of the category column gives the share of the category total, right only while the report slices by category.
- Option. Check. 2020. https://www.sqlbi.com/articles/a-proposal-for-visual-calculations-in-dax/
- When: Percentage-of-total measures in the model.

**T12-A302-8.** When a visual calculation needs a few constant values per member, such as a rate for each year, define them in a visual calculation with SWITCH, not in a model table. Visual calculations exist so that calculations can be added without changing the model.
- Should. 2024. https://www.sqlbi.com/articles/using-expand-and-collapse-in-visual-calculations/
- When: Calculations built with visual calculations where the model is to stay unchanged.
- Version: The values come from the brief or the developer, with a comment where they live (descriptions; checklist item 8).

**T12-A302-10.** A visual calculation depends on the structure of its visual: changing that structure can quickly break it and force a major rewrite. One built on year and month stops working when the visual is sliced by brand instead.
- Fact. 2024. https://www.sqlbi.com/articles/using-expand-and-collapse-in-visual-calculations/
- When: Deciding whether logic belongs in a visual calculation; changing a visual that has one.

**T12-A302-12.** In a model measure, a few lookup values such as a yearly rate can live in a table held by a variable inside the measure, with the per-period structures derived from the model at evaluation time. No separate column is needed to store them.
- Option. 2024. https://www.sqlbi.com/articles/using-expand-and-collapse-in-visual-calculations/
- When: Model measures that need small constant inputs, such as yearly inflation rates.
- Version: The values come from the brief or the developer, with a comment in the DAX (descriptions; checklist item 8).

**T12-A327-2.** A visual calculation that returns text, such as a colour name, must have its data type set to Text in the visual's format options (Format, General, Data Format, Format Options) before it can be picked as a conditional-formatting source.
- Must. Check. 2025. https://www.sqlbi.com/articles/using-visual-calculations-for-conditional-formatting/
- When: A text-returning visual calculation feeds the conditional formatting of a measure in the same visual.
- Version: A workaround for the 2025 preview, which treated every visual calculation as a number; a later fix was announced.

**T12-A327-3.** A model measure that picks a conditional-formatting colour by comparing each value with an average over the values of one specific column, say product category, gives wrong colours once the user slices the visual by a different column.
- Fact. 2025. https://www.sqlbi.com/articles/using-visual-calculations-for-conditional-formatting/
- When: Measures written to drive conditional formatting by comparing a value with the average of the items shown.

**T12-A327-4.** When a displayed column is sorted by another column, the sort column filters the evaluation too, and context transition inside an AVERAGEX over the displayed column's values leaves that filter in place. Removing it takes an unusual CALCULATE and ALLEXCEPT combination that beginners rarely find.
- Fact. 2025. https://www.sqlbi.com/articles/using-visual-calculations-for-conditional-formatting/
- When: A measure iterates the values of a displayed column that has a sort-by column and relies on context transition.

**T12-A357-3.** To highlight a matrix row by the highest value in the last column, a visual calculation can build the matrix content with ROWS COLUMNS, using COLLAPSEALL and EXPAND, find the last column header with LAST, and return a colour only for rows with the maximum.
- Option. 2026. https://www.sqlbi.com/articles/using-visual-calculations-to-highlight-an-entire-row/
- When: The highlight of a full row depends only on the rightmost matrix column; ties can highlight several rows.
- Version: Theme colours only; a colour code needs an exception row (V009).

### Window functions and apply semantics

**T12-A266-2.** INDEX needs every row of its source table to be unique. If the extra sort columns it adds by itself still cannot make the rows unique, it fails; for a model table, uniqueness has to come from a primary key.
- Fact. Check. 2023. https://www.sqlbi.com/articles/introducing-window-functions-in-dax/
- When: Any use of INDEX, above all over a model table.
- Version: As described in 2023; verify on current versions.

**T12-A266-4.** A window function called with no source table uses ALLSELECTED over the ORDERBY columns. The shorter code can miss expected rows: an OFFSET previous-year measure shows nothing for the earliest year a year filter leaves visible, since that year has no previous row.
- Fact. Check. 2023. https://www.sqlbi.com/articles/introducing-window-functions-in-dax/
- When: Window functions whose source table argument is left out.
- Version: As described in 2023; verify on current versions.

**T12-A266-6.** For a previous-year value computed with OFFSET, pass an explicit source table that drops the existing filters on the year column, with ALL on that column. Under the default source table the first visible year has no previous row and shows no value.
- Should. 2023. https://www.sqlbi.com/articles/introducing-window-functions-in-dax/
- When: Previous-period calculations over dates, when the visual or query filters the years shown.

**T12-A266-10.** WINDOW can frame common totals over a sorted table. Moving average: relative start some rows back, relative end at the current row. Running total: absolute start at the first row, relative end at the current row; partitioned by year, that gives year-to-date.
- Option. 2023. https://www.sqlbi.com/articles/introducing-window-functions-in-dax/
- When: Running totals, moving averages and similar totals over a sorted table.

**T12-A266-11.** INDEX can fetch the row at a given position of a sorted table, for example the best-selling brand: a positive position counts from the top, a negative one from the bottom. With PARTITIONBY it returns one such row for each group.
- Option. 2023. https://www.sqlbi.com/articles/introducing-window-functions-in-dax/
- When: Fetching the first, last or nth row of a sorted table, also within each group.

**T12-A303-1.** When OFFSET or WINDOW cannot identify one current row, apply semantics treats every matching source row as a current row, runs the function once for each and unions the results. A value still comes back, by a precise algorithm, but can be confusing to read.
- Fact. 2024. https://www.sqlbi.com/articles/understanding-apply-semantics-for-window-functions-in-dax/
- When: The filter context holds several values for a source-table column, or the query does not group by the ORDERBY column.

**T12-A303-2.** To find the current row, a window function matches each model column of its source table to the innermost row context that holds it, or else to all its VALUES in the filter context, crossjoined without auto-exist. More model columns mean more combinations to scan.
- Fact. 2024. https://www.sqlbi.com/articles/understanding-apply-semantics-for-window-functions-in-dax/
- When: Judging the cost or the result of a window function over a wide source table.

**T12-A303-3.** Only columns carrying the lineage of a model column take part in finding a window function's current row, even under another name. A column computed by an expression, for instance with ADDCOLUMNS, is local: it is used only afterwards, when the source table is filtered.
- Fact. 2024. https://www.sqlbi.com/articles/understanding-apply-semantics-for-window-functions-in-dax/
- When: Window functions whose source table mixes model columns and computed columns.

### Ranking with RANK and RANKX

**T12-A278-3.** To give tied items different positions, RANK can take several ORDERBY columns, for example the ranking value and then the item name in alphabetical order. RANKX puts ties on one position, and making it separate them is complex.
- Option. 2023. https://www.sqlbi.com/articles/introducing-the-rank-window-function-in-dax/
- When: Tied values must be ranked apart; equal positions for ties are sometimes the wanted result.

**T12-A278-6.** When the ranked column has a sort-by column, such as a month name sorted by month number, the source table of RANK must override both columns. The sort-by column is part of the query and keeps filtering otherwise, which gives wrong rankings.
- Must. 2023. https://www.sqlbi.com/articles/introducing-the-rank-window-function-in-dax/
- When: Ranking the items of a column that has a sort-by column.

**T12-A278-7.** RANK helps with the subtle and rare RANKX issue that can affect rankings over decimal numbers, because it relies on the current row that window functions have.
- Fact. 2023. https://www.sqlbi.com/articles/introducing-the-rank-window-function-in-dax/
- When: Ranking on decimal numbers.

**T12-A348-3.** When a ranking must ignore the filters coming from slicers and other visuals (a global ranking), use a measure that ranks over ALL of the column with RANK or RANKX, not a visual calculation, which sees only the data present in its visual.
- Should. 2025. https://www.sqlbi.com/articles/using-rank-instead-of-rankx-in-dax/
- When: Ranking requirements that must be independent of report filters.

**T12-A348-5.** In a measure, RANK returns blank where no single current row exists, such as on totals, so it needs no ISINSCOPE or HASONEVALUE guard. A RANKX measure without such checks shows a meaningless value on the grand total and every subtotal of a matrix.
- Fact. 2023. https://www.sqlbi.com/articles/introducing-the-rank-window-function-in-dax/ ; https://www.sqlbi.com/articles/using-rank-instead-of-rankx-in-dax/
- When: Ranking measures placed in a matrix with totals or subtotals.

**T12-A348-7.** To rank by more than one column, prefer RANK with several columns in its ORDERBY argument to a RANKX workaround. RANKX has no built-in way to rank over several columns, and the code that makes it do so is intricate and error-prone.
- Should. 2025. https://www.sqlbi.com/articles/using-rank-instead-of-rankx-in-dax/
- When: Ranking based on multiple columns.

**T12-A348-9.** Use RANKX, not RANK, to rank over a table variable whose columns were all added by DAX table functions and carry no data lineage. RANK needs at least one model column to match the current row and raises an error without one.
- Should. 2025. https://www.sqlbi.com/articles/using-rank-instead-of-rankx-in-dax/
- When: Ranking over variables that hold only temporary columns; uncommon.

**T12-A348-10.** RANK cannot classify a value against a lookup or range table, such as sales segments with thresholds. RANKX with its third argument can; a simple iteration such as MINX over a FILTER of the range table is an alternative that is likely easier to read.
- Option. 2025. https://www.sqlbi.com/articles/using-rank-instead-of-rankx-in-dax/
- When: Ranking or classifying a measure value against a predefined lookup table built from another column or expression.

**T12-A348-11.** RANK behaves as expected when a measure ranks the current row of a visual. Ranking inside a calculated column, which has a row context and no filter context, is more problematic.
- Fact. 2025. https://www.sqlbi.com/articles/using-rank-instead-of-rankx-in-dax/
- When: Choosing where to compute a ranking with RANK.

### Visual context and virtual table

**T12-A298-2.** The query that feeds a matrix returns one flat table in which subtotal rows sit beside detail rows. Power BI tells them apart; for DAX all those rows are alike.
- Fact. 2024. https://www.sqlbi.com/articles/introducing-visual-shape-for-visual-calculations-in-power-bi/
- When: Reasoning about what a formula sees in a matrix with subtotals.

**T12-A298-3.** The axis keywords ROWS and COLUMNS are valid only inside visual calculations. A model measure cannot use them: it can sit in a matrix that has no visual calculation, where no axis exists.
- Fact. 2024. https://www.sqlbi.com/articles/introducing-visual-shape-for-visual-calculations-in-power-bi/
- When: Deciding where a formula that refers to a visual axis can live.

**T12-A298-4.** In a visual calculation, a previous-value lookup can use PREVIOUS with the ROWS or COLUMNS axis, without spelling out the PARTITIONBY and ORDERBY that OFFSET needs: the axis keyword already supplies grouping, partitioning and sort order.
- Option. 2024. https://www.sqlbi.com/articles/introducing-visual-shape-for-visual-calculations-in-power-bi/
- When: Reading the previous value along a visual axis; PREVIOUS and NEXT move along the axis only, not between hierarchy levels.

**T12-A301-2.** COLLAPSE given a column does not stop at that column's level: it moves to the lowest level of the axis hierarchy without the column, so collapsing on year returns the grand total. If the column is not in the current visual context, nothing moves.
- Fact. 2024. https://www.sqlbi.com/articles/introducing-expand-and-collapse-for-visual-calculations/
- When: Visual calculations that pass a column, not a number of levels, to COLLAPSE.

**T12-A301-3.** EXPAND given a column lands on the uppermost hierarchy level of that axis where the column is present, so EXPAND and COLLAPSE called with the same column end at different levels.
- Fact. 2024. https://www.sqlbi.com/articles/introducing-expand-and-collapse-for-visual-calculations/
- When: Visual calculations that pass a column to EXPAND or COLLAPSE.

**T12-A302-2.** The virtual-table columns a visual calculation can see depend on the hierarchy level its visual context points to. After COLLAPSE moves up a level, a column that exists only lower down, such as month at the year level, evaluates to blank.
- Fact. 2024. https://www.sqlbi.com/articles/using-expand-and-collapse-in-visual-calculations/
- When: Visual calculations that reference columns after moving the visual context with COLLAPSE.

**T12-A302-4.** To get the rows of one specific hierarchy level whatever level the current cell is at, move the visual context to the top with COLLAPSEALL, then EXPAND on the column of the target level, then evaluate ROWS; the two moves can be nested CALCULATETABLE calls.
- Option. 2024. https://www.sqlbi.com/articles/using-expand-and-collapse-in-visual-calculations/
- When: A visual calculation needs a table at a fixed granularity, such as months.

**T12-A302-5.** When a value must be computed at one granularity, say month by month, yet shown at year and grand total too, run the iteration inside CALCULATE with EXPAND to the column of that granularity. Higher levels then iterate at that level; lower ones stay put.
- Option. 2024. https://www.sqlbi.com/articles/using-expand-and-collapse-in-visual-calculations/
- When: Visual calculations whose result cannot be computed directly at the upper levels of the hierarchy.

**T12-A302-7.** A hidden column the visual uses for sorting, such as a year-month number, is part of the virtual table. A visual calculation can refer to it freely, for example in the ORDERBY of a window function to put months in their right order.
- Option. 2024. https://www.sqlbi.com/articles/using-expand-and-collapse-in-visual-calculations/
- When: A visual calculation must sort virtual-table rows in the order a sort-by column defines.

### Running totals and performance

**T12-A320-1.** A running total of a distinct-count measure makes every cell compute on its own, each with a scan of the fact table, because distinct counts are not additive. The many queries slow the report as rows grow; window functions over the model help little.
- Fact. 2024. https://www.sqlbi.com/articles/computing-open-orders-with-visual-calculations-in-dax/
- When: Running totals over a distinct-count measure, such as open orders as received minus delivered.

**T12-A320-2.** For a running total over a non-additive measure such as a distinct count, RUNNINGSUM in a visual calculation can add up values the visual already aggregated instead of scanning the fact table again for each cell. An optimized model measure can still be faster.
- Option. 2024. https://www.sqlbi.com/articles/computing-open-orders-with-visual-calculations-in-dax/
- When: Open-orders or events-in-progress running totals in one visual; wrong if a slicer removes earlier periods.

**T12-A320-3.** A visual calculation cannot read model data outside its visual's virtual table. A running total built with one starts at the first period visible after slicers apply, as if nothing came before, and is wrong when earlier periods carry a balance.
- Fact. 2024. https://www.sqlbi.com/articles/computing-open-orders-with-visual-calculations-in-dax/
- When: Running totals or opening balances in visual calculations when a slicer or filter removes earlier periods.

**T12-A320-4.** When a running total built with visual calculations needs the balance from before the first period shown, create a model measure that returns that starting value, using ALLSELECTED so every row gets the same number, and add it inside the visual calculation.
- Should. 2024. https://www.sqlbi.com/articles/computing-open-orders-with-visual-calculations-in-dax/
- When: Slicers or filters hide earlier periods; the extra column carries a small performance cost.

**T12-A320-5.** To speed up a running total of a non-additive measure in a model measure, one option is a variable holding a temporary table at day granularity with the orders received and delivered; each cell then iterates that table instead of scanning the fact table.
- Option. 2024. https://www.sqlbi.com/articles/computing-open-orders-with-visual-calculations-in-dax/
- When: Open-orders running totals over distinct counts; a coarser column such as month is slightly faster but less flexible.

**T12-A320-8.** Open orders can be computed as a running total of orders received minus a running total of orders delivered. The numbers are correct, but in general it is not the most efficient approach.
- Option. 2024. https://www.sqlbi.com/articles/computing-open-orders-with-visual-calculations-in-dax/
- When: Sales linked to Date by an order-date and a delivery-date relationship; slow with distinct-count measures.

**T12-A365-4.** Adding a visual calculation makes the engine add VISUAL SHAPE to the source table, which densifies it: the full SUMMARIZECOLUMNS result is materialized and the combinations whose measures are all blank, normally left out, are added back. On large virtual tables this can take long.
- Fact. 2026. https://www.sqlbi.com/articles/analyzing-the-performance-impact-of-visual-calculations/
- When: Judging the cost of a visual calculation on a visual with many combinations.
