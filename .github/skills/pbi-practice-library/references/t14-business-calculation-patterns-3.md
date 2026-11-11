# Business calculation patterns

Part 3 of 5 of this topic. Covers: Semi-additive and running totals; Building and testing calculations.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

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

### Building and testing calculations

**T14-A034-2.** When SUMX or another iterator must run CALCULATE per row, the cost can be cut by iterating the coarsest values that still give the same result, such as distinct first-order dates and not every customer: the inner expression then runs once per group.
- Option. 2013. https://www.sqlbi.com/articles/yearly-customer-historical-sales-in-dax/
- When: CALCULATE is needed inside the iteration and a coarser set of values gives the same result.

**T14-A088-10.** Give the data model careful attention, even in a small report file, and do not settle for a naive design: with the right model formulas become simpler and faster, while a naive one leads to slower and more complex DAX.
- Should. 2016. https://www.sqlbi.com/articles/analyzing-events-with-a-duration-in-dax/
- When: Any model, small ones included.

**T14-A117-5.** Build a complex formula one step at a time: store each step in a variable and return that variable for a moment to check the partial result before moving on. A variable known to be right lets you work on the harder parts with confidence.
- Should. 2017. https://www.sqlbi.com/articles/computing-same-product-sales-in-dax/
- When: Writing complex formulas.

**T14-A117-6.** When an intermediate step of a measure produces a table, it can be tested by returning the row count of that table variable for a moment and checking the number in a report.
- Option. 2017. https://www.sqlbi.com/articles/computing-same-product-sales-in-dax/
- When: Writing and debugging a measure whose steps include a table variable.

**T14-A326-8.** When facing a new business requirement, consider breaking it down into a series of smaller steps, each solvable with an existing generic modelling or DAX pattern. Reusing well-known, optimised patterns lowers effort and the risk of errors, and brings their known performance gains.
- Consider. 2025. https://www.sqlbi.com/articles/account-receivable-aging-in-power-bi/
- When: Any new business requirement.

**T14-A346-4.** Inside GROUPBY, COUNTROWS cannot be the aggregation. To count the rows of each group, iterate CURRENTGROUP with SUMX over the constant 1: GROUPBY requires CURRENTGROUP to walk the rows of the group being aggregated.
- Must. 2025. https://www.sqlbi.com/articles/find-the-products-in-the-top-10-every-year-with-dax/
- When: Counting rows per group with GROUPBY.

**T14-A346-5.** When a measure has to manipulate tables, first write and debug its logic as a DAX query, checking the partial results. Only then move it into a measure and fix the problems the outer filter context causes.
- Should. 2025. https://www.sqlbi.com/articles/find-the-products-in-the-top-10-every-year-with-dax/
- When: Non-trivial measures that build and manipulate intermediate tables.

**T14-A369-13.** When defining a calculation, always check how it behaves in border cases: at the start or end of a time period, at subtotal and total level, under different selections, and with blank values in columns or partial results.
- Must. 2026. https://www.sqlbi.com/articles/the-hidden-complexity-of-a-daily-average-in-dax/
- When: Any calculation, even one that looks simple, such as an average.

**T14-A369-15.** When DAX code comes from an AI assistant, the person responsible has to state the business requirements, question the proposed code and check its results. Code that runs is no proof that it returns the number the business needs.
- Must. 2026. https://www.sqlbi.com/articles/the-hidden-complexity-of-a-daily-average-in-dax/
- When: Measures, functions or queries generated by an AI assistant.

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
- Version: Engine behaviour as described in 2019.

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

**T14-A323-9.** When an amount is a quantity measure multiplied by a product attribute such as unit cost, one way to cut the iterations is to iterate the distinct values of that attribute, not every product.
- Option. 2025. https://www.sqlbi.com/articles/optimizing-incremental-inventory-calculations-in-dax/
- When: Valuing a quantity measure at product cost; a plain column sum computed without calling the measure is faster still.

### Building and testing calculations

**T14-A326-14.** Before relying on an accounts receivable aging calculation in your own scenario, you can check that it is correct on a small sample model, editing the movements data to exercise the corner cases you care about.
- Option. 2025. https://www.sqlbi.com/articles/account-receivable-aging-in-power-bi/
- When: Adopting an aging model and its measures for a specific scenario.

**T14-A346-6.** Table logic that is right in a query with no outer filters can return wrong results once moved into a measure: the visual's filter context changes the table variables, and TOPN ranks by a measure evaluated in that current filter context.
- Fact. 2025. https://www.sqlbi.com/articles/find-the-products-in-the-top-10-every-year-with-dax/
- When: Moving query code that builds ranking tables into a measure shown in a visual such as a matrix.
