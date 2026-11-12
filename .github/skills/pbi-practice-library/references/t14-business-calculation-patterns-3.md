# Business calculation patterns

Part 3 of 4 of this topic. Covers: Semi-additive and running totals; Ranking and top N.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### Semi-additive and running totals

**T14-A149-2.** A semi-additive measure can be built with CALCULATE whose filter narrows the selected dates to one date: LASTDATE for the period end, FIRSTDATE for its start. LASTDATE assumes data on each period's last day; without it the period and its totals can show no value.
- Option. Check. 2013. https://www.sqlbi.com/articles/semi-additive-measures-in-dax-for-power-pivot/
- When: Balances or inventory; safe with a daily snapshot, not with working-day rows or periods past the last load.
- Version: Described in 2013.

**T14-A149-5.** The expression given as second argument to LASTNONBLANK should be evaluated through context transition, with an explicit or an implicit CALCULATE. Without it the expression is not filtered by each date scanned, and the result equals that of LASTDATE.
- Should. Check. 2013. https://www.sqlbi.com/articles/semi-additive-measures-in-dax-for-power-pivot/
- When: Semi-additive measures that use LASTNONBLANK to find the last date with data.
- Version: Described in 2013.

**T14-A149-7.** To filter on the last selected date through MAX, CALCULATE can take a FILTER over ALL values of the date column that keeps the date equal to its MAX. Shorter: store that MAX in a variable and use it in a plain equality test.
- Option. Check. 2013. https://www.sqlbi.com/articles/semi-additive-measures-in-dax-for-power-pivot/
- When: A semi-additive measure that takes the last selected date through MAX, not LASTDATE.

**T14-A149-8.** Use LASTDATE in filter arguments. For a true-or-false condition evaluated in a row context, MAX is the better choice: LASTDATE causes a context transition there, which hides the filter context that comes from outside.
- Should. Check. 2013. https://www.sqlbi.com/articles/semi-additive-measures-in-dax-for-power-pivot/
- When: Choosing between LASTDATE and MAX for the last date of a selection.
- Version: Described in 2013.

**T14-A037-1.** Never sum snapshot balances, such as account balances or stock units, across dates: for a period return the value of one date, its last or first day. They still add up across other dimensions, and additive columns of the same table keep a plain sum.
- Must. 2013. https://www.sqlbi.com/articles/semi-additive-measures-in-dax-for-power-pivot/ ; https://www.sqlbi.com/articles/semi-additive-measures-in-dax/
- When: Semi-additive values in tables that hold snapshots over time.

**T14-A052-1.** The first argument of FIRSTNONBLANK and LASTNONBLANK can be any table expression with a single column, such as VALUES, ALL or FILTER. A plain column reference there is shorthand for VALUES of that column.
- Option. 2015. https://www.sqlbi.com/articles/alternative-use-of-firstnonblank-and-lastnonblank/
- When: Any use of FIRSTNONBLANK or LASTNONBLANK.

**T14-A323-4.** For large snapshot tables, consider producing the snapshot in SQL or another ETL tool: a DAX calculated table is recomputed every time the model changes and whenever the file is opened, which with a very large snapshot can make opening take minutes.
- Consider. 2025. https://www.sqlbi.com/articles/optimizing-incremental-inventory-calculations-in-dax/
- When: Large snapshot tables.

**T14-A323-5.** Do not carry the size results of a published snapshot example over to your own model. Always check your own model's metrics, such as whether the snapshot really has fewer rows than the transaction tables it summarises: that depends on dimension cardinality and data distribution.
- Must. 2025. https://www.sqlbi.com/articles/optimizing-incremental-inventory-calculations-in-dax/
- When: Designing snapshot tables for balance calculations.

### Ranking and top N

**T14-A091-3.** Set up the Sort By Column settings of the model first, and only then write measures that iterate one or more columns: a setting added later can change how existing measures with iterators over that column are evaluated.
- Should. 2016. https://www.sqlbi.com/articles/use-of-rankx-in-power-bi-measures/
- When: Power BI models with measures that iterate columns.
- Version: Excel is not affected: it queries the model through MDX.

**T14-A091-4.** When a Sort By Column setting is added to a column, check whether any measure iterates that column and whether its result could change: the setting can break a measure that already exists.
- Should. 2016. https://www.sqlbi.com/articles/use-of-rankx-in-power-bi-measures/
- When: A Sort By Column setting is added to an existing Power BI model.
- Version: Excel is not affected: it queries the model through MDX.

**T14-A091-8.** Avoid computing a total that adds up only the visible top N rows of a ranking report: on a large table such a total has performance implications.
- Should. 2016. https://www.sqlbi.com/articles/use-of-rankx-in-power-bi-measures/
- When: Ranking reports over large tables.

**T14-A136-7.** For a sorted top N list in one visual, such as a matrix or bar chart, the visual-level Top N filter is an alternative that performs better than ranking with measures. It returns more than N rows when the Nth position is tied.
- Option. 2018. https://www.sqlbi.com/articles/displaying-nth-element-in-dax/
- When: A visual with a sorted list; hard to use where positions sit in separate elements.

**T14-A209-3.** In a calculated column that ranks over all rows of its own table, wrap the table in ALL although it is not technically needed: a reader then sees at once that the ranking spans every row.
- Should. 2020. https://www.sqlbi.com/articles/rankx-on-multiple-columns-with-dax-and-power-bi/
- When: Writing a ranking in a calculated column over the whole table.

**T14-A209-6.** In a ranking measure, put as much work as possible in variables that do not depend on the cell, such as a model-wide maximum taken with REMOVEFILTERS: the engine works them out once for all cells. Otherwise a ranking measure easily becomes very slow.
- Should. 2020. https://www.sqlbi.com/articles/rankx-on-multiple-columns-with-dax-and-power-bi/
- When: Writing a dynamic ranking as a measure.

**T14-A257-1.** The table given to RANKX as first argument must hold every value that takes part in the ranking, so it has to ignore the current cell's filter context. VALUES of the ranked column is wrong: it holds only the current item, so everything ranks 1.
- Must. Check. 2022. https://www.sqlbi.com/articles/introducing-rankx-in-dax/
- When: Ranking items, such as brands, shown on the rows of a matrix.
- Version: Described in 2022.

**T14-A257-2.** For the list of items given to RANKX, prefer ALLSELECTED to ALL on the ranked column: the list is then the set of items visible in the visual, which behaves better when slicers reduce them.
- Should. Check. 2022. https://www.sqlbi.com/articles/introducing-rankx-in-dax/
- When: Slicers can reduce the items shown in the visual that holds the ranking.
- Version: Described in 2022.

**T14-A257-3.** Always guard a RANKX calculation with at least a HASONEVALUE test on the ranked column, so the value being ranked has the same grain as the values in the lookup list. A value that covers several items, such as several brands, gets a wrong rank.
- Must. Check. 2022. https://www.sqlbi.com/articles/introducing-rankx-in-dax/
- When: Any ranking measure built on RANKX.
- Version: Described in 2022.

**T14-A257-6.** When ranked values can tie, the fifth argument of RANKX decides the result. SKIP, the default, keeps duplicate values in the lookup list; DENSE removes them, so equal values count as one. The ranks that follow a tie differ between the two.
- Option. Check. 2022. https://www.sqlbi.com/articles/introducing-rankx-in-dax/
- When: Duplicate values can appear in the lookup list, for example after rounding the measure.
- Version: Described in 2022.

**T14-A346-8.** When a computed table of keys is passed to CALCULATE as a filter argument, wrap it in KEEPFILTERS, so it does not replace a filter the report already puts on that column. Without it a report that filters the key column gets wrong results.
- Should. 2025. https://www.sqlbi.com/articles/find-the-products-in-the-top-10-every-year-with-dax/
- When: Measures that filter a computed set of items, such as best products by key, inside CALCULATE.

## Special-case techniques and facts

### Semi-additive and running totals

**T14-A033-1.** For stock analysis, weigh computing units in stock at query time from a movements table against storing a daily snapshot table, case by case, on memory against query speed. When most products seldom move, the snapshot can be several times larger than the movements table.
- Consider. 2013. https://www.sqlbi.com/articles/inventory-in-power-pivot-and-dax-snapshot-vs-dynamic-calculation/
- When: Stock over time; with many daily movements for most products the snapshot is the smaller table.
- Version: Described in 2013 for Power Pivot and Analysis Services Tabular, which hold all data in memory.

**T14-A033-2.** Before a stock calculation done at query time goes into production, test both its query speed and its memory saving on your own data: the outcome depends on how the data is distributed, and it was generally slower for small result sets.
- Should. 2013. https://www.sqlbi.com/articles/inventory-in-power-pivot-and-dax-snapshot-vs-dynamic-calculation/
- When: Choosing between a daily snapshot table and a stock measure worked out from a movements table.

**T14-A033-4.** When stock is a running total of all movements up to the last selected date, an IF test on whether the selected period has any rows in the movements table stops the balance from repeating into periods with no transactions.
- Option. 2013. https://www.sqlbi.com/articles/inventory-in-power-pivot-and-dax-snapshot-vs-dynamic-calculation/
- When: Stock worked out at query time by adding all movements dated up to the date evaluated.

**T14-A149-3.** When a snapshot table may lack a row for some days, LASTNONBLANK over the date column can replace LASTDATE as the CALCULATE filter: the measure takes the last date that has data and carries that value forward. FIRSTNONBLANK does the same for a period's start.
- Option. Check. 2013. https://www.sqlbi.com/articles/inventory-in-power-pivot-and-dax-snapshot-vs-dynamic-calculation/ ; https://www.sqlbi.com/articles/semi-additive-measures-in-dax-for-power-pivot/
- When: Snapshots kept only for working days, or periods that run past the last loaded date.
- Version: Described in 2013.

**T14-A149-9.** CLOSINGBALANCEMONTH, CLOSINGBALANCEQUARTER and CLOSINGBALANCEYEAR equal CALCULATE filtered by ENDOFMONTH, ENDOFQUARTER or ENDOFYEAR; OPENINGBALANCEMONTH, OPENINGBALANCEQUARTER and OPENINGBALANCEYEAR equal CALCULATE filtered by the day before STARTOFMONTH, STARTOFQUARTER or STARTOFYEAR. Either set can show an enclosing period's balance, such as quarter-end values on month rows.
- Option. Check. 2013. https://www.sqlbi.com/articles/semi-additive-measures-in-dax-for-power-pivot/
- When: The selection is smaller than the period; none of these functions skips boundary dates without data.
- Version: Described in 2013.

**T14-A149-10.** When opening or closing balances must skip dates without data, replace OPENINGBALANCEMONTH, CLOSINGBALANCEMONTH and their QUARTER and YEAR forms by CALCULATE filtered with LASTNONBLANK, widening the period considered through PARALLELPERIOD: none of those functions checks for non-blank values.
- Should. Check. 2013. https://www.sqlbi.com/articles/semi-additive-measures-in-dax-for-power-pivot/
- When: Snapshot data that stops before the end of a period or misses some days.
- Version: Described in 2013.

**T14-A037-2.** For a semi-additive last-balance measure, find the last date that has data as the maximum date in the snapshot table, not with LASTDATE on the Date table. LASTDATE sees only the Date table, so periods whose final calendar date has no snapshot row return blank.
- Should. Check. 2019. https://www.sqlbi.com/articles/semi-additive-measures-in-dax/
- When: Snapshot data that is not present on the last calendar day of every period.

**T14-A037-3.** When entities such as customers have their last balance on different dates, decide from the business requirement how the grand total behaves: use the latest date across all entities, leaving blank those without data on that date, or add up each entity's own last balance.
- Consider. Check. 2019. https://www.sqlbi.com/articles/semi-additive-measures-in-dax/
- When: Last-balance measures where entities report on different last dates within one period.

**T14-A037-4.** When a last-balance measure uses the latest date across all entities, add a label to the report stating the last day the calculation used. The numbers are right but hard to read, for example when a slicer removes the entity that holds the latest date.
- Should. 2019. https://www.sqlbi.com/articles/semi-additive-measures-in-dax/
- When: Semi-additive measures that take the last date across every entity, not per entity.

**T14-A037-5.** To total each entity's last balance, prefer a table of entities with their last date, given the lineage of the entity and Date columns with TREATAS and passed as a CALCULATE filter, over iterating the entities with SUMX, which may be slow with many entities.
- Should. Check. 2019. https://www.sqlbi.com/articles/semi-additive-measures-in-dax/
- When: Last-balance measures whose grand total is the sum of per-entity last balances.
- Version: Described in 2019.

**T14-A037-6.** In last-balance measures, remember that an entity's last date may lie outside the current filter context: the entity can show blank in one period yet return an older value at a higher level, changing totals. Showing values that predate the selection needs more complex code.
- Consider. Check. 2019. https://www.sqlbi.com/articles/semi-additive-measures-in-dax/
- When: Some entities have no snapshot data inside the selected period.

**T14-A037-7.** Reserve LASTNONBLANK for last-date logic that the simpler and faster maximum date of the fact table cannot handle, such as elaborate business conditions coded in a measure. LASTNONBLANK is an iterator and usually the slower of the two.
- Should. Check. 2019. https://www.sqlbi.com/articles/semi-additive-measures-in-dax/
- When: Choosing how a semi-additive measure finds the last date.
- Version: Performance as described in 2019.

**T14-A037-8.** Use STARTOFMONTH, STARTOFQUARTER, STARTOFYEAR, ENDOFMONTH, ENDOFQUARTER and ENDOFYEAR for opening or closing balances only when snapshot data exists on every period's start and end date. They work on the Date table alone, so otherwise write custom last-date logic.
- Should. Check. 2019. https://www.sqlbi.com/articles/semi-additive-measures-in-dax/
- When: Opening and closing balances over snapshot data.

**T14-A037-9.** Be careful with semi-additive measures: pin down the exact behaviour required first. A formula can look right in one layout and still fail when the report is arranged differently or the data changes.
- Consider. 2019. https://www.sqlbi.com/articles/semi-additive-measures-in-dax/
- When: Any semi-additive calculation.

**T14-A052-2.** FIRSTNONBLANK and LASTNONBLANK scan a column's values in its native sort order, which depends on its data type, and take columns of any data type, not only dates. Elsewhere in DAX the order of values in a table or column usually cannot be assumed.
- Fact. 2015. https://www.sqlbi.com/articles/alternative-use-of-firstnonblank-and-lastnonblank/
- When: Any use of FIRSTNONBLANK or LASTNONBLANK.

**T14-A146-1.** A running total that must keep growing across year boundaries cannot use DATESYTD, which restarts each year. It needs an explicit CALCULATE filter keeping every date up to the latest date visible in the current filter context and dropping the other Date table filters.
- Must. Check. 2019. https://www.sqlbi.com/articles/computing-running-totals-in-dax/
- When: Running totals over dates that continue past year end.

**T14-A146-2.** A running-total measure over dates can keep an explicit ALL on the Date table even where the engine adds that removal itself, as with a DateTime relationship column or a marked date table. The measure is clearer and still works with other key types.
- Option. Check. 2019. https://www.sqlbi.com/articles/computing-running-totals-in-dax/
- When: Running totals over dates in any model.
- Version: Engine behaviour as described in 2019. In this template, write the removal with REMOVEFILTERS, not ALL (DAX standard, rule 20; M519).

**T14-A146-3.** The running-total filter pattern also works on attributes other than dates, such as an ordered customer-class number, to accumulate values from the first group down to the current one. ABC classification is one such case.
- Option. Check. 2019. https://www.sqlbi.com/articles/computing-running-totals-in-dax/
- When: Running totals over a dimension or attribute that is not a date.

**T14-A323-1.** A balance or stock measure that adds up every transaction from the start of history to each reporting date is simple to write but can get extremely slow. Its cost depends on the number of report cells, transaction volume and the cardinality of the dimensions.
- Fact. 2025. https://www.sqlbi.com/articles/optimizing-incremental-inventory-calculations-in-dax/
- When: The source holds every transaction since a zero state, so the balance is a running sum from the first date.

**T14-A323-2.** To make a running-total balance fast without a snapshot for every date, the measure must combine snapshot and transactions: take the stored balance of the latest snapshot on or before the reporting date, then add the net movements after it up to that date.
- Must. 2025. https://www.sqlbi.com/articles/optimizing-incremental-inventory-calculations-in-dax/
- When: Running-total balances where snapshot memory must be weighed against query speed; simple cases can be faster without snapshots.

**T14-A323-3.** A snapshot table alone moves the cost and does not remove it. A snapshot for every date and all needed dimensions can be very costly in processing time and memory; a monthly or quarterly one limits trend analysis and gives nothing below its date grain.
- Fact. 2025. https://www.sqlbi.com/articles/optimizing-incremental-inventory-calculations-in-dax/
- When: Speeding up running-total balances, such as stock or account balances, with a precomputed snapshot table.

**T14-A323-6.** In larger models, consider adding further, smaller snapshot tables that keep fewer dimensions: they speed up queries that do not filter every dimension of the detailed snapshot, such as reports that never filter by store.
- Consider. 2025. https://www.sqlbi.com/articles/optimizing-incremental-inventory-calculations-in-dax/
- When: Larger models that use snapshot tables for balances; at modest volume and cardinality a second snapshot is not needed.

**T14-A323-7.** With several snapshot tables of different grain, you can hide the measure written for each snapshot and expose one measure that tests with ISCROSSFILTERED which tables are filtered, then reads the smallest snapshot that still covers the detail the query asks for.
- Option. 2025. https://www.sqlbi.com/articles/optimizing-incremental-inventory-calculations-in-dax/
- When: Several snapshots kept to speed up high-level aggregations in very large models.

**T14-A323-8.** To choose between a detailed and a coarser snapshot without naming dimension tables, you can evaluate ISCROSSFILTERED on the detailed one inside CALCULATE with REMOVEFILTERS on the coarser. TRUE means a filter on a dimension the coarser lacks: use the detailed snapshot; otherwise the coarser.
- Option. 2025. https://www.sqlbi.com/articles/optimizing-incremental-inventory-calculations-in-dax/
- When: The coarser snapshot's dimensions are a subset of the detailed one's; all relationships are regular one-to-many.

### Ranking and top N

**T14-A052-4.** A measure that returns the top item with TOPN 1, such as the best-selling product, can wrap the TOPN result in FIRSTNONBLANK. A tie then gives one item, the first in alphabetical order; TOPN alone returns two or more rows and the measure fails.
- Option. 2015. https://www.sqlbi.com/articles/alternative-use-of-firstnonblank-and-lastnonblank/
- When: A measure returns one name based on a ranking, and ties are possible.

**T14-A091-1.** When a column has the Sort By Column property set, Power BI adds its sort column to every query that uses the column. A RANKX measure iterating only the displayed column, with context transition, then gets a sort-column filter per row and ranks wrongly.
- Fact. 2016. https://www.sqlbi.com/articles/use-of-rankx-in-power-bi-measures/
- When: An iterator over the one column shown, with context transition; plain aggregations are usually unaffected.
- Version: Excel is not affected: it queries through MDX.

**T14-A091-2.** When RANKX ranks the values of one column that has a Sort By Column setting, the sort column can be included beside it in the ALL table argument. Context transition then replaces the filter on both columns and the ranking comes out as expected.
- Option. 2016. https://www.sqlbi.com/articles/use-of-rankx-in-power-bi-measures/
- When: Ranking over one column that the model sorts by another column of the same table.

**T14-A091-5.** An iterator over a physical table, not over a column, is not expected to suffer from the Sort By Column ranking problem. The table may have the wrong granularity for the calculation, though, and context transition over a whole table can cost more.
- Fact. 2016. https://www.sqlbi.com/articles/use-of-rankx-in-power-bi-measures/
- When: Choosing what a ranking measure iterates.

**T14-A091-6.** To show the top N items under the current report filters, a measure that returns blank outside the top N ranks can be used in place of a calculated column: Power BI tables and matrices hide rows where every displayed measure is blank.
- Option. 2016. https://www.sqlbi.com/articles/use-of-rankx-in-power-bi-measures/
- When: Power BI table and matrix visuals.

**T14-A091-7.** A top N measure that blanks rows ranked below N can add a check, such as HASONEVALUE on the ranked column, so the total row returns blank. Without it the total includes the hidden rows too and is not the sum of the visible ones.
- Option. 2016. https://www.sqlbi.com/articles/use-of-rankx-in-power-bi-measures/
- When: The top N measure is shown in a visual with a total.

**T14-A136-1.** When several visuals each show the item at a different rank position, write one shared measure that reads the position from a parameter in the filter context. Each visual's measure is that shared measure in CALCULATE with a filter on its position.
- Should. 2018. https://www.sqlbi.com/articles/displaying-nth-element-in-dax/
- When: Layouts that show specific ranking positions in separate visuals, such as cards.
- Version: The position table can be made with the New Parameter feature of Power BI, which also adds the measure. This template adds a numeric range parameter only when the developer asks for one (native features).

**T14-A136-3.** A measure that returns the item at the Nth rank can build the list of items to rank with ALLSELECTED. It then also works in a matrix or chart with the rank position on an axis, or to highlight one position in a complex visual.
- Option. 2018. https://www.sqlbi.com/articles/displaying-nth-element-in-dax/
- When: The Nth-item measure is reused beyond single cards.

**T14-A136-4.** One way to return exactly one item per rank position: rank by a value that no two items share, for example an amount plus a tiny fraction derived from the item's integer key, then pick the single item at the Nth rank.
- Option. Check. 2018. https://www.sqlbi.com/articles/displaying-nth-element-in-dax/
- When: The data must allow it: here amounts had at most two decimals and the key was divided by 1,000,000.

**T14-A136-5.** When ties must be shown, or a unique ranking value is impossible, RANKX with dense ties can be used and the names of the items at the Nth position joined into one string with CONCATENATEX. Any of them gives the amount: tied items share it.
- Option. 2018. https://www.sqlbi.com/articles/displaying-nth-element-in-dax/
- When: The report must handle ties, or a unique value per item cannot be guaranteed.

**T14-A136-6.** Use measures that show the item at a given rank position only for very few items in a report, and confirm on real data that users accept the cost: the measure runs many times and costs more than the Top N visual filter.
- Should. 2018. https://www.sqlbi.com/articles/displaying-nth-element-in-dax/
- When: Measures that display the item at a given rank position.

**T14-A164-1.** To show only each group's top N items in a visual, write one dedicated measure, such as a rank within the group, and use it in the visual-level filter. Do not add rank-and-blank logic to every measure shown: that changes each measure and hurts performance.
- Should. Check. 2019. https://www.sqlbi.com/articles/filtering-the-top-3-products-for-each-category-in-power-bi/
- When: Visuals with the top N per group; subtotals then cover the visible items only.
- Version: In 2019 the Power BI interface had no easy way to show the top N of each group. The DAX standard (rule 37) notes that a measure filter on a visual works the measure out twice: measure both ways.

**T14-A164-2.** A measure that ranks items within their group in a visual must build the ranking table as CALCULATETABLE over VALUES of the item column with ALLSELECTED on that column. ALLSELECTED of the column alone discards the visual's group filter and gives a wrong rank.
- Must. Check. 2019. https://www.sqlbi.com/articles/filtering-the-top-3-products-for-each-category-in-power-bi/
- When: Ranking items such as products within a group such as category; ISINSCOPE limits the rank to item level.

**T14-A164-3.** Building a top-N-per-group visual filter with TOPN and not RANKX brings no speed gain: internally TOPN costs as much as RANKX.
- Fact. 2019. https://www.sqlbi.com/articles/filtering-the-top-3-products-for-each-category-in-power-bi/
- When: Visual-level filter measures that select the top items of each group.

**T14-A164-4.** A visual-filter measure that builds the list of top items per group with GENERATE and TOPN must compute that list under ALLSELECTED. The list then does not depend on the item being evaluated: it is the same for every item and is evaluated once.
- Must. 2019. https://www.sqlbi.com/articles/filtering-the-top-3-products-for-each-category-in-power-bi/
- When: Filter measures that return 1 for items to keep and 0 otherwise, with KEEPFILTERS joining list and selection.
- Version: In 2019 Power BI took no table as a visual-level filter, hence a measure returning 1 or 0.

**T14-A164-5.** Be aware that a top N filter measure built with GENERATE and TOPN is tied to the specific set of columns placed in the visual: it has to be designed for that exact combination of columns.
- Consider. 2019. https://www.sqlbi.com/articles/filtering-the-top-3-products-for-each-category-in-power-bi/
- When: Visual-level filter measures that generate the top items per group.

**T14-A164-6.** When a visual-level filter keeps only some items, a group subtotal that should include all items needs its own measure: it returns the normal value at item level and removes the filter on the item column at every higher level, the grand total included.
- Must. 2019. https://www.sqlbi.com/articles/filtering-the-top-3-products-for-each-category-in-power-bi/
- When: Visuals with only the top items of each group, where subtotals or group sorting must reflect all items.

**T14-A164-7.** To rank groups and items in a visual with a visual-level filter, the rank measure must switch its RANKX arguments by hierarchy level with ISINSCOPE. At group level, ranking ALLSELECTED groups by the measure that ignores the item filter orders groups by all their items.
- Must. Check. 2019. https://www.sqlbi.com/articles/filtering-the-top-3-products-for-each-category-in-power-bi/
- When: A ranking at group and item level while a visual-level filter hides some items.

**T14-A164-8.** When groups are ranked by the value of only the items visible in the visual, the current group's value must be saved in a variable before switching to ALLSELECTED and passed as the value argument of RANKX: ALLSELECTED replaces the current filter context.
- Must. Check. 2019. https://www.sqlbi.com/articles/filtering-the-top-3-products-for-each-category-in-power-bi/
- When: Group-level ranking in a visual whose items are reduced by a visual-level filter.

**T14-A164-9.** A measure written only to drive a visual-level filter can pick any custom set of items for a visual, beyond the choices of the filter pane. The model's other measures keep working unchanged, because only the filter measure decides which items appear.
- Option. 2019. https://www.sqlbi.com/articles/filtering-the-top-3-products-for-each-category-in-power-bi/
- When: The item selection cannot be expressed with standard filters; values of excluded items need further measures.
- Version: Presented in 2019 as a way round the limits of Power BI's filter options.

**T14-A170-1.** For top N products plus an "Others" row, do not rely on the Power BI Top N visual filter: build a calculated table of every product name plus "Others", use its column in the visual, and put the top N logic in its own measure.
- Must. 2019. https://www.sqlbi.com/articles/showing-the-top-5-products-and-others-row/
- When: A report shows the top N items by a measure plus one row for the items not shown.
- Version: A 2021 note recommends a newer way of filtering top products alongside the others. The calculated table needs its CalculatedReason from the developer (model standard, rule 8; M105).

**T14-A213-1.** To show only the top N products inside each category of one visual, you can write a measure that returns a product's rank among the products of the visual's current selection only when it lies between 1 and N, then add it as visual filter.
- Option. Check. 2021. https://www.sqlbi.com/articles/filtering-the-top-products-alongside-the-other-products-in-power-bi/
- When: A visual must keep the top N items of every group under the current report selection.
- Version: Described in 2021.

**T14-A213-2.** In a top N report the number N can be fixed in the code, as a variable or constant in the measure, or offered to readers through a slicer on a What-if parameter, which supplies a parameter table and a measure returning the selected value.
- Option. Check. 2019. https://www.sqlbi.com/articles/showing-the-top-5-products-and-others-row/ ; https://www.sqlbi.com/articles/filtering-the-top-products-alongside-the-other-products-in-power-bi/
- When: A top N filter or measure, with or without an Others row.
- Version: This template adds a numeric range parameter only when the developer asks for one (native features).

**T14-A213-3.** In a top N visual with an extra "Others" row, sort the rows by the ranking measure, not by the sales value: that keeps Others after the top products of each category. An older approach put a two-value group column as first matrix level.
- Must. 2021. https://www.sqlbi.com/articles/filtering-the-top-products-alongside-the-other-products-in-power-bi/ ; https://www.sqlbi.com/articles/showing-the-top-5-products-and-others-row/
- When: A top N per category visual with one more aggregated row for the remaining items.
- Version: Sorting by the ranking measure dates from 2021; the group-column approach from 2019.

**T14-A213-4.** One way to show the top N products followed by an "Others" row: build a calculated table with every product name plus one extra "Others" value, relate it to the Product table on the product name, and put its column in the visual.
- Option. 2021. https://www.sqlbi.com/articles/filtering-the-top-products-alongside-the-other-products-in-power-bi/
- When: A report shows the top N items in detail and one dynamic row for all the rest.
- Version: The calculated table needs its CalculatedReason from the developer (model standard, rule 8; M105).

**T14-A213-6.** Relate the calculated table of product names plus "Others" to Product on the product name as one-to-many, names table on the one side, filtering one way towards Product. Check it: by default Power BI tends to suggest a one-to-one relationship filtering both ways.
- Must. Check. 2019. https://www.sqlbi.com/articles/showing-the-top-5-products-and-others-row/ ; https://www.sqlbi.com/articles/filtering-the-top-products-alongside-the-other-products-in-power-bi/
- When: The top N plus Others technique built on a calculated table of names related to Product.
- Version: A text key that makes Product a snowflake link needs M412 and M110 rows in the brief (relationships and dates, rules 3, 27).

**T14-A213-7.** When a visual uses the column of product names plus "Others", include a ranking measure that returns a value on the "Others" row. That name filters no product, so the sales measure is blank there and the visual would drop the row.
- Must. 2021. https://www.sqlbi.com/articles/filtering-the-top-products-alongside-the-other-products-in-power-bi/
- When: A visual groups by a calculated names table with an extra Others value, not by the product name column.

**T14-A213-8.** In the ranking measure that filters a top N plus "Others" visual, you can return N + 1 on the "Others" row and the normal rank for products, reading the selection from the names table, not from Product. Others then stays, after the top products.
- Option. 2021. https://www.sqlbi.com/articles/filtering-the-top-products-alongside-the-other-products-in-power-bi/
- When: A visual shows the top N items from a calculated names table with an extra Others value.

**T14-A213-9.** For an additive measure, the "Others" row can be computed as the total of all selected products minus the sum of the top N products, reducing the list of visible products before working out the top N.
- Option. 2021. https://www.sqlbi.com/articles/filtering-the-top-products-alongside-the-other-products-in-power-bi/
- When: The measure shown on the Others row of a top N visual is additive.

**T14-A213-10.** For a non-additive measure, the "Others" row can be computed by evaluating the original measure over the other products, selected with a filter. This is more flexible than taking a difference, and costs more to compute.
- Option. 2021. https://www.sqlbi.com/articles/filtering-the-top-products-alongside-the-other-products-in-power-bi/
- When: The measure shown on the Others row of a top N visual is not additive.

**T14-A213-11.** To highlight the "Others" row, a helper measure can return 1 for top N rows and subtotals, -1 for "Others", and blank or 0 for hidden rows. Use it as visual filter (keep what is not 0) and in a conditional formatting rule on -1.
- Option. 2021. https://www.sqlbi.com/articles/filtering-the-top-products-alongside-the-other-products-in-power-bi/
- When: A top N plus Others matrix whose Others row should stand out.

**T14-A213-13.** When a matrix column is made narrower than its header text, turn off Word wrap in the Column headers formatting options. Word wrap is on by default and makes the header taller once the column is narrower than its name.
- Must. Check. 2021. https://www.sqlbi.com/articles/filtering-the-top-products-alongside-the-other-products-in-power-bi/
- When: Narrowing a matrix column, such as a hidden sort-by ranking column, below the width of its name.
- Version: Described in 2021.

**T14-A213-14.** A measure that serves only as the visual-level filter of a matrix can be taken out of the Values area once the filter is set: it goes on filtering the visual and shows no column.
- Should. 2021. https://www.sqlbi.com/articles/filtering-the-top-products-alongside-the-other-products-in-power-bi/
- When: A top N plus Others matrix filtered by a helper flag measure that need not be shown.

**T14-A209-1.** RANKX ranks by one expression. A ranking on two numeric values can fold them into one number: multiply the main value by the maximum of the secondary value, then add the secondary value. The main value always dominates and the secondary one breaks ties.
- Option. Check. 2020. https://www.sqlbi.com/articles/rankx-on-multiple-columns-with-dax-and-power-bi/
- When: A ranking must use more than one column, by requirement or to break ties.
- Version: Described in 2020.

**T14-A209-2.** When the tie-breaking column of a multi-column ranking is text, it can first be turned into a whole number by ranking the text values in descending order, then combined with the main value. Names that come first alphabetically then end up ahead.
- Option. Check. 2020. https://www.sqlbi.com/articles/rankx-on-multiple-columns-with-dax-and-power-bi/
- When: Ranking by a numeric value with a text column, such as a customer name, as second criterion.
- Version: Described in 2020.

**T14-A209-4.** The dynamic part of a ranking measure cannot rest on calculated columns: helper columns built for a static ranking are of no use to a ranking that must react to report selections.
- Must. 2020. https://www.sqlbi.com/articles/rankx-on-multiple-columns-with-dax-and-power-bi/
- When: A dynamic ranking replaces a static one stored in a calculated column.

**T14-A209-5.** In a dynamic multi-column ranking measure, the helper values a static version keeps in calculated columns can be rebuilt as temporary columns of a table variable; RANKX then ranks the current item's combined value against that table.
- Option. Check. 2020. https://www.sqlbi.com/articles/rankx-on-multiple-columns-with-dax-and-power-bi/
- When: A multi-column ranking must be dynamic; a text tie-breaker needs one more temporary column holding its numeric rank.
- Version: Described in 2020.

**T14-A257-5.** To place a value within a configuration table, such as a sales segmentation table, RANKX can iterate that table with the table's own column as second argument and take the measure to classify as the optional third argument. By default one expression serves both purposes.
- Option. Check. 2022. https://www.sqlbi.com/articles/introducing-rankx-in-dax/
- When: The value to rank must be positioned against a list held in a separate configuration table.
- Version: Described in 2022.

**T14-A346-1.** Finding the top products for each year, or for any other group, requires GENERATE combined with TOPN, so that TOPN runs its table expression once per row of the first table.
- Must. 2025. https://www.sqlbi.com/articles/find-the-products-in-the-top-10-every-year-with-dax/
- When: Top-N selections by group, such as the top 10 products of every year.

**T14-A346-2.** To find items that stay among the best, you can build the top-N table per period, count for each item the periods it appears in, and keep the items whose count reaches a chosen share of all periods, such as 80%.
- Option. 2025. https://www.sqlbi.com/articles/find-the-products-in-the-top-10-every-year-with-dax/
- When: Finding products that are in the yearly top 10 in most years.

**T14-A346-7.** To compute a ranking list that ignores the filters of the visual's cells, you can evaluate the table variables that build it under ALLSELECTED. That alone does not stop the list, used as CALCULATE filter, from overriding a report filter on the same key column.
- Option. 2025. https://www.sqlbi.com/articles/find-the-products-in-the-top-10-every-year-with-dax/
- When: Measures that work out a set of best items, shown in a visual that filters those items.
