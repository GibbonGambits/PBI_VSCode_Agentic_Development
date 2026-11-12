# Business calculation patterns

Part 2 of 4 of this topic. Covers: Customer, product and campaign analysis.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### Customer, product and campaign analysis

**T14-A330-10.** Keep the measures written only to show a data point's details in a visual's tooltips few: every measure in the tooltip area is computed once per data point.
- Should. 2025. https://www.sqlbi.com/articles/dynamic-pareto-analysis-in-power-bi/
- When: Line charts with tooltip measures, such as the name or amount of the item at each position.
- Version: Tooltips are off in this template: needs the visual's exception row in the brief.

**T14-A330-11.** When a visual has very many data points, consider moving its tooltip content to a separate report page: tooltip measures are computed once for each data point of the visual.
- Consider. 2025. https://www.sqlbi.com/articles/dynamic-pareto-analysis-in-power-bi/
- When: Visuals with many data points and tooltip measures.
- Version: Tooltips are off in this template: needs the visual's exception row in the brief.

**T14-A349-3.** To filter for rows that are, or are not, linked to a dimension member, test the dimension's key column, not the fact table's foreign key: fact rows whose key matches no dimension row then fall on the blank row, and the parts still add up.
- Should. 2025. https://www.sqlbi.com/articles/measuring-the-impact-of-promotions-on-sales-in-power-bi/
- When: Splitting a measure into linked and unlinked parts when the fact table may hold keys missing from the dimension.

## Special-case techniques and facts

### Customer, product and campaign analysis

**T14-A031-1.** When the transaction history covers several years, group transactions by the customer's age at the time of each transaction, not by the customer's age today: it gives a better analysis over such a history.
- Should. 2013. https://www.sqlbi.com/articles/grouping-transactions-by-age-of-customers-in-dax/
- When: Analysis by customer age over a transaction history of several years.

**T14-A031-2.** The customer's age at each transaction can be kept in a calculated column of the fact table, worked out from the transaction's order date and the birth date that RELATED fetches from the customer table.
- Option. 2013. https://www.sqlbi.com/articles/grouping-transactions-by-age-of-customers-in-dax/
- When: The customer table has a birth date and the fact table an order date, both typed as dates.
- Version: Presented in 2013 for PowerPivot and Analysis Services Tabular models. A calculated column needs its reason line; the standard prefers the source or Power Query (M105, M106).

**T14-A031-3.** To group fact rows into bands that a separate table defines by minimum and maximum, do not relate the fact table to the band table. Copy the band into the fact table with a calculated column returning the one band that encloses the row's value.
- Should. 2013. https://www.sqlbi.com/articles/grouping-transactions-by-age-of-customers-in-dax/
- When: Bands such as age groups: the band table has no row for every single value.
- Version: In 2013 the band table was a linked table in PowerPivot or a regular table in Tabular. A calculated column needs its reason line; the standard prefers the source or Power Query (M105, M106). The unrelated band table needs its M411 row.

**T14-A031-4.** When a band label is copied into the fact table, copy the band's position column there as well, hide it, and make it the Sort by Column of the band column.
- Should. 2013. https://www.sqlbi.com/articles/grouping-transactions-by-age-of-customers-in-dax/
- When: The band table carries a position column that orders the bands.

**T14-A031-5.** A calculated column that returns the one matching band through VALUES fails with an error when the table is refreshed if the band table holds overlapping intervals.
- Fact. 2013. https://www.sqlbi.com/articles/grouping-transactions-by-age-of-customers-in-dax/
- When: A band lookup written as a calculated column that filters the band table by minimum and maximum.

**T14-A031-6.** Once the band and its position are columns of the fact table, the intermediate age column can go: compute both straight from the order date and the related birth date. The age column has far more distinct values; the longer formula runs only at refresh.
- Option. 2013. https://www.sqlbi.com/articles/grouping-transactions-by-age-of-customers-in-dax/
- When: Large fact tables, such as a sales table with millions of rows.
- Version: Only when the source or Power Query cannot supply it, with its CalculatedReason (storage and security, rule 17; M105).

**T14-A034-1.** When a calculation needs each customer's first order date, keep that date in a calculated column of the customer table and do not work it out inside the measure: the stored value performs better.
- Should. 2013. https://www.sqlbi.com/articles/yearly-customer-historical-sales-in-dax/
- When: Analysis of customer sales by year counted from each customer's first purchase.
- Version: A calculated column needs its reason line; the standard prefers the source or Power Query (M105, M106).

**T14-A034-3.** Sales in a customer's first, second or third year can be computed without ETL: iterate the customers whose first order date falls in the selected dates and filter, with DATESINPERIOD, the 12 months from that date, moved one or two years on with DATEADD.
- Option. 2013. https://www.sqlbi.com/articles/yearly-customer-historical-sales-in-dax/
- When: Sales in the years after each customer's first order, honouring the date selection; needs the first order date.

**T14-A066-1.** To analyse how a customer's yearly category moves over time, build a calculated table with one row per customer and year holding the category and level of that year and the year before. Measures with dummy category dimensions are complex, and slow on large data.
- Should. Check. 2015. https://www.sqlbi.com/articles/transition-matrix-using-calculated-tables/
- When: Category set by yearly sales, and customers moving between categories are counted; plain dynamic segmentation needs none of this.
- Version: Needs calculated tables: in Power BI since September 2015, not in Excel 2016. Only when upstream shaping cannot supply the table, with its CalculatedReason (model standard, rule 8; checklist item 38; M105).

**T14-A066-2.** When a customer-by-year category table joins each customer-year to a category lookup with GENERATE, not GENERATEALL, customer-years lacking a category in the current or the previous year are dropped silently. New and lost customers are absent, so transition matrix totals can look wrong at first.
- Fact. Check. 2015. https://www.sqlbi.com/articles/transition-matrix-using-calculated-tables/
- When: A calculated table for a category transition matrix where customers may be new or may have stopped buying.
- Version: Described in 2015.

**T14-A066-4.** When measures work out the change of a customer's category from the previous year to the current one, they must handle, with an explicit condition, customers that did not exist in the previous year. Without it the change shown for those customers is wrong.
- Must. Check. 2015. https://www.sqlbi.com/articles/transition-matrix-using-calculated-tables/
- When: The year-over-year category change comes from measures, not from a precomputed customer-by-year table.
- Version: Described in 2015.

**T14-A066-5.** Where calculated tables are not available, a similar precomputed table can be made as a linked back table: a query over the data model whose result lands in an Excel table that is then loaded back into the model.
- Option. Check. 2015. https://www.sqlbi.com/articles/transition-matrix-using-calculated-tables/
- When: Only while the result stays under the 1M row limit of an Excel sheet.
- Version: Offered in 2015 for Excel 2016, which has no calculated tables.

**T14-A066-6.** When a calculated table needs several attributes, such as category name and level, from the matching row of a table of value bands, GENERATE with SELECTCOLUMNS over the band table limited to the matching band can return them all in one lookup.
- Option. Check. 2015. https://www.sqlbi.com/articles/transition-matrix-using-calculated-tables/
- When: A calculated table assigns each row to a category defined by minimum and maximum boundaries.
- Version: Described in 2015.

**T14-A077-1.** Consider counting new customers in two steps: derive each customer's first purchase date from the fact table with the Date filter removed, then count the customers whose first date falls in the selected period. Testing customer by customer for no earlier sales stays slow.
- Consider. Check. 2016. https://www.sqlbi.com/articles/computing-new-customers-in-dax/
- When: Counting new customers for any date selection; try it on your own model and read the query plan.
- Version: Performance as described in 2016.

**T14-A077-2.** In the first-purchase-date step of a new-customers measure, the first date per customer can be added with ADDCOLUMNS over VALUES of the customer key, with CALCULATE around the MIN, in place of grouping the fact table with SUMMARIZE. The speed gain was barely measurable.
- Option. Check. 2016. https://www.sqlbi.com/articles/computing-new-customers-in-dax/
- When: A new-customers measure that first works out each customer's first purchase date with the date filter removed.
- Version: Measured in 2016.

**T14-A117-1.** A measure can compare sales of one fixed set of products across periods: find the first year with sales in the selection, collect the products sold that year in a table variable, and pass that variable as a filter to CALCULATE for each period's sales.
- Option. Check. 2017. https://www.sqlbi.com/articles/computing-same-product-sales-in-dax/
- When: Users want to leave out products introduced after the start of the selected period.
- Version: A 2020 note points to a fuller, optimised like-for-like comparison pattern.

**T14-A117-2.** The starting point of a same-product comparison cannot be the minimum selected date, because the selected products may have no sales on that date. It has to be the first date on which any selected product sold.
- Fact. 2017. https://www.sqlbi.com/articles/computing-same-product-sales-in-dax/
- When: Working out the starting year for a comparison of the same products across periods.

**T14-A117-3.** When the first year with sales for the selected products is found inside a report cell, the cell's filters on year and product must be removed with ALLSELECTED, so the calculation runs in the filter context of the report.
- Must. 2017. https://www.sqlbi.com/articles/computing-same-product-sales-in-dax/
- When: A same-product comparison in a report sliced by year and product.

**T14-A117-4.** After the Date filter is removed to find the first year with sales, CROSSFILTER inside the calculation can let Sales filter Date, and Product for the product list, so that only dates and products with sales stay visible.
- Option. 2017. https://www.sqlbi.com/articles/computing-same-product-sales-in-dax/
- When: The same-product comparison: finding the first year with sales and the products sold in it.

**T14-A117-7.** The approach of deriving a filter from one date and applying it to other periods can be extended: build the set of items needed with set functions such as UNION, EXCEPT and INTERSECT, then apply it as a filter with CALCULATE.
- Option. 2017. https://www.sqlbi.com/articles/computing-same-product-sales-in-dax/
- When: Comparisons that need a custom set of items held fixed across periods.

**T14-A256-1.** For sales in the days before or after a selected period among buyers of the selected brand in it, one way saves those customers in a variable and evaluates sales with REMOVEFILTERS on product and customer tables, the saved customers and DATESBETWEEN over those days.
- Option. 2022. https://www.sqlbi.com/articles/computing-sales-to-specific-customers-before-and-after-a-time-period/
- When: Customer segment defined by the brand bought in a chosen period; the day count can come from a slicer.

**T14-A256-2.** To split the before/after sales of the segment between the selected brand and all other brands, one option is a second before/after measure that keeps the product filter and removes only the customer filter; other-brand sales are the all-products figure minus it.
- Option. 2022. https://www.sqlbi.com/articles/computing-sales-to-specific-customers-before-and-after-a-time-period/
- When: Before/after sales of a brand-defined customer segment must be split into the selected brand and the rest.

**T14-A256-3.** A measure that returns other-brand sales as the difference between an all-products measure and a same-brand measure can be written so that it returns blank and not zero.
- Option. 2022. https://www.sqlbi.com/articles/computing-sales-to-specific-customers-before-and-after-a-time-period/
- When: Splitting before/after sales of a brand-defined customer segment between the selected brand and other brands.

**T14-A330-1.** A Pareto line chart comparing several groups, such as countries, must be built with measures over a disconnected numeric table numbered 1 to the item count, used as a continuous axis. Item names on a categorical axis add a scrollbar and leave groups unconnected.
- Must. 2025. https://www.sqlbi.com/articles/dynamic-pareto-analysis-in-power-bi/
- When: Pareto or cumulative-distribution line charts that show several groups in one chart.
- Version: The disconnected axis table needs its M411 row in the brief (relationships and dates, rule 4).

**T14-A330-2.** The numeric position table used as the continuous axis of a dynamic Pareto chart must stay visible to report authors in the model, although it has no relationships.
- Must. 2025. https://www.sqlbi.com/articles/dynamic-pareto-analysis-in-power-bi/
- When: A disconnected calculated table used as the X axis of a line chart.

**T14-A330-3.** To let users choose which measure an analysis works on, you can create a table that lists the measure names for a slicer, and a measure that switches with SWITCH to the measure the user picked.
- Option. 2025. https://www.sqlbi.com/articles/dynamic-pareto-analysis-in-power-bi/
- When: A calculation such as a Pareto analysis must run on a metric the user chooses.
- Version: Where the choice only swaps a visual's field, this template suggests a field parameter instead (U003).

**T14-A330-4.** In a measure that switches between measures by a slicer selection, the fallback branch can call ERROR, so evaluation stops in plain sight when there is no valid selection and nobody is confused by a missing or wrong choice.
- Option. 2025. https://www.sqlbi.com/articles/dynamic-pareto-analysis-in-power-bi/
- When: Measures that return a user-selected measure through SWITCH.

**T14-A330-5.** For the cumulative Pareto value at position N of a numeric axis, one way builds a table of visible items with their metric values, keeps its first N rows ordered by value descending with WINDOW, and sums those values. WINDOW does this selection very efficiently.
- Option. 2025. https://www.sqlbi.com/articles/dynamic-pareto-analysis-in-power-bi/
- When: Dynamic Pareto measures plotted against a disconnected numeric position axis.

**T14-A330-6.** In a dynamic Pareto line chart on a numeric position axis, keep attributes of the ranked items, such as customer columns, off the X axis. The table of items and values is then computed once per visual, though the measure runs per data point.
- Should. 2025. https://www.sqlbi.com/articles/dynamic-pareto-analysis-in-power-bi/
- When: Pareto measures that build a table of all visible items inside the measure.

**T14-A330-7.** When Pareto curves of groups with different item counts are compared in one chart, show the cumulative value as a percentage of the group total, not as an absolute amount: in absolute amounts each group reaches 80% of its total at a different position.
- Must. 2025. https://www.sqlbi.com/articles/dynamic-pareto-analysis-in-power-bi/
- When: Pareto line charts that compare several groups such as countries.

**T14-A330-8.** For a table that shows each item's Pareto contribution inside one group, visual calculations can do the work: a hidden running sum over the rows of the visual, and a percentage that divides it by its total, obtained with COLLAPSE.
- Option. 2025. https://www.sqlbi.com/articles/dynamic-pareto-analysis-in-power-bi/
- When: A table visual lists the items of one selected group; several groups in one line chart need measures.

**T14-A330-9.** When Pareto visual calculations must show several groups at once, partition the running sum by the group column with PARTITIONBY inside WINDOW, so each item's percentage is relative to its own group, and use a matrix to make navigation easier.
- Should. 2025. https://www.sqlbi.com/articles/dynamic-pareto-analysis-in-power-bi/
- When: Running sum and percentage visual calculations shown for several groups such as countries.

**T14-A330-12.** In a tooltip measure returning values of the item at the current axis position, the item list can use ALLSELECTED, not VALUES or SUMMARIZE, when the returned item column is also on the X axis: the metric is needed for every item in the visual.
- Option. 2025. https://www.sqlbi.com/articles/dynamic-pareto-analysis-in-power-bi/
- When: Tooltip-only measures of a dynamic Pareto line chart, such as the customer name at a position.
- Version: Tooltips are off in this template: needs the visual's exception row in the brief.

**T14-A349-1.** To report both the sales directly tied to a grouping, such as a marketing campaign, and the wider sales it may have influenced, one model keeps a per-transaction column pointing to the grouping and adds a bridge table linking the grouping to its products.
- Option. 2025. https://www.sqlbi.com/articles/measuring-the-impact-of-promotions-on-sales-in-power-bi/
- When: Products link many-to-many to a grouping that can push sales nobody tracks explicitly.

**T14-A349-2.** When fact rows may have no value in the foreign key to a dimension, one approach lets those rows fall on the dimension's automatic blank row and adds no artificial 'not assigned' member: measures isolate them with ISBLANK and need no special value.
- Option. 2025. https://www.sqlbi.com/articles/measuring-the-impact-of-promotions-on-sales-in-power-bi/
- When: A regular one-to-many relationship where some fact rows have a blank key, such as sales with no campaign.
- Version: Blank keys on the many side must be intended and recorded (checklist item 14).

**T14-A349-5.** For a measure of sales linked to no dimension member, one design branches on ISINSCOPE: when the dimension column is a grouping level, intersect the blank-member filter with the selection through KEEPFILTERS; otherwise clear the dimension's filters with REMOVEFILTERS, then filter the blank member.
- Option. 2025. https://www.sqlbi.com/articles/measuring-the-impact-of-promotions-on-sales-in-power-bi/
- When: An 'unattributed' measure where the dimension's blank row holds the unlinked fact rows.

**T14-A349-6.** A measure that clears every filter on the campaign dimension with REMOVEFILTERS can serve as a fixed reference total: it returns full sales whatever campaign is selected, so campaign-specific figures can be read against it.
- Option. 2025. https://www.sqlbi.com/articles/measuring-the-impact-of-promotions-on-sales-in-power-bi/
- When: Analysing one campaign against overall revenue.

**T14-A349-7.** With a bridge table between products and campaigns, one approach keeps both relationships filtering towards the bridge only, and turns on two-way filtering between the bridge and products with CROSSFILTER inside the measures that need all products of a campaign.
- Option. 2025. https://www.sqlbi.com/articles/measuring-the-impact-of-promotions-on-sales-in-power-bi/
- When: Influenced-sales style measures that must cover every product of the selected campaigns, however each transaction was attributed.

**T14-A349-8.** When a measure must reach the fact table through the bridge-and-product path only, switch off the direct relationship between the fact table and the campaign dimension inside the measure, with CROSSFILTER set to NONE. Left active, it limits the result to attributed transactions.
- Must. 2025. https://www.sqlbi.com/articles/measuring-the-impact-of-promotions-on-sales-in-power-bi/
- When: The fact table links to the campaign dimension both directly and through product and a bridge table.

**T14-A349-9.** In a measure that filters products through a bridge table, pass the visible values of the campaign column as an explicit CALCULATE filter. With no campaign selected, only products in at least one campaign then stay visible; otherwise every product would.
- Must. 2025. https://www.sqlbi.com/articles/measuring-the-impact-of-promotions-on-sales-in-power-bi/
- When: Influenced-sales style measures evaluated when the report may have no campaign selected.

**T14-A349-10.** To return zero for items that qualify but have no sales, and blank for items that do not qualify, one technique uses DIVIDE to divide the base measure plus zero by the true-or-false condition: a false condition gives blank through division by zero.
- Option. 2025. https://www.sqlbi.com/articles/measuring-the-impact-of-promotions-on-sales-in-power-bi/
- When: Measures such as influenced sales, where a product may be in a selected campaign yet have no transactions.
- Version: Any zero-for-blank logic needs the brief's request and an exception to the blank rule (M506).

**T14-A349-11.** For sales of products that never took part in any campaign, one technique builds the set of products whose related bridge rows are empty, evaluated with campaign filters removed, then evaluates the base measure over that set, again with campaign filters removed.
- Option. 2025. https://www.sqlbi.com/articles/measuring-the-impact-of-promotions-on-sales-in-power-bi/
- When: A model with a bridge table between products and campaigns.

**T14-A349-12.** Compute sales of products outside any campaign by filtering those products directly, not by subtracting total influenced sales from total sales. The subtraction is right only for additive measures; filtering the products works for any measure.
- Should. 2025. https://www.sqlbi.com/articles/measuring-the-impact-of-promotions-on-sales-in-power-bi/
- When: The base measure may be non-additive; for an additive amount both give the same value.

**T14-A349-13.** A measure of sales for products never in any campaign can use ISINSCOPE to return blank whenever the campaign column is a grouping level of the visual, and still return values when campaigns are only filtered by a slicer.
- Option. 2025. https://www.sqlbi.com/articles/measuring-the-impact-of-promotions-on-sales-in-power-bi/
- When: An organic-sales style measure that ignores campaign selections.

**T14-A349-14.** When several campaign measures are shown together in one report, the attributed-sales measure can stand in for the plain base measure: comparisons with the other measures get simpler.
- Option. 2025. https://www.sqlbi.com/articles/measuring-the-impact-of-promotions-on-sales-in-power-bi/
- When: Reports that put the campaign measures in the same visual.

**T14-A349-15.** To show influenced sales for every campaign whatever campaign is picked in the report, one technique evaluates the influenced-sales measure after clearing the campaign filters with REMOVEFILTERS and adding a filter that keeps all non-blank campaigns.
- Option. 2025. https://www.sqlbi.com/articles/measuring-the-impact-of-promotions-on-sales-in-power-bi/
- When: A bridge table links products and campaigns and an influenced-sales measure already exists.
