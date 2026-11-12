# Business calculation patterns

Part 1 of 5 of this topic. Covers: Totals and hierarchy levels; Budget, currency and financial calculations.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### Totals and hierarchy levels

**T14-A186-2.** When a measure's total must equal the sum of its values at a detail level, build that level into the formula: iterate its items in the current context, for example SUMX over the year-month column, evaluate the logic per item and add up the results.
- Must. Check. 2019. https://www.sqlbi.com/articles/summing-values-for-the-total/ ; https://www.sqlbi.com/articles/obtaining-accurate-totals-in-dax/
- When: A total recomputed in its own filter context is wrong; below the iterated level values stay counterintuitive.

**T14-A186-3.** When a total looks wrong, check the grain the formula works at. Take from the business requirement the level (day, month or another period) at which the condition must be tested, and make the formula iterate at that level.
- Should. 2020. https://www.sqlbi.com/articles/obtaining-accurate-totals-in-dax/
- When: A measure's totals or subtotals differ from what report users expect.

**T14-A187-1.** For a measure designed for a minimum level of detail, such as month and above, work out beforehand where it would return wrong numbers, decide what it must return below that level, and build that behaviour into the DAX. Never just leave the inaccurate result.
- Must. 2020. https://www.sqlbi.com/articles/working-below-a-dax-formulas-granularity/
- When: A measure whose logic holds only at or above one grain can be shown at a finer grain.

### Budget, currency and financial calculations

**T14-A138-3.** A CALCULATE filter on the key column of a marked date table overrides every filter already on that table. When the result must stay inside the selected period, as when a forecast is limited to dates after the last sale, wrap the filter in KEEPFILTERS.
- Must. 2018. https://www.sqlbi.com/articles/showing-actuals-and-forecasts-in-the-same-chart-with-power-bi/
- When: A filter on the key column of a marked date table that must respect the current selection.

**T14-A138-4.** Treat the adjustment of budget figures by a correction factor as a business requirement, and handle it with great care.
- Should. 2018. https://www.sqlbi.com/articles/showing-actuals-and-forecasts-in-the-same-chart-with-power-bi/
- When: A forecast or budget is to be corrected with a factor.

**T14-A326-13.** Prefer external data preparation to a DAX calculated table for the snapshot tables of the events-in-progress pattern: external preparation allows incremental updates.
- Should. 2025. https://www.sqlbi.com/articles/account-receivable-aging-in-power-bi/
- When: Snapshot tables that speed up events-in-progress calculations such as open receivables.

## Special-case techniques and facts

### Totals and hierarchy levels

**T14-A010-1.** A parent-group total can be had with CALCULATE and ALLEXCEPT on the item table, keeping only the group column: every other filter on that table is cleared, the one on the current item included, so the group's total is left.
- Option. 2011. https://www.sqlbi.com/articles/ratio-over-subtotals-with-normalized-tables-in-dax/
- When: The parent-group column sits in the same table as the item column shown.
- Version: From 2011. The DAX standard uses ALLEXCEPT only when the kept column is filtered directly; otherwise REMOVEFILTERS with VALUES (rule 20).

**T14-A010-2.** ALLEXCEPT works on one table only. It cannot return the total of a parent group whose column sits in another table reached through relationships, such as a category table linked to products through a subcategory table.
- Fact. 2011. https://www.sqlbi.com/articles/ratio-over-subtotals-with-normalized-tables-in-dax/
- When: A normalized or snowflake model where the parent-group column is outside the item table.

**T14-A010-3.** For the total of a parent group whose column sits in a related table, give CALCULATE a SUMMARIZE of the item table that returns only that group column. Do not iterate all items with FILTER and a CONTAINS test: that scans every item.
- Should. 2011. https://www.sqlbi.com/articles/ratio-over-subtotals-with-normalized-tables-in-dax/
- When: A normalized model: the group column is in a table related to the item table, perhaps through another table.

**T14-A010-4.** When the query also filters another item column, such as model, the CALCULATE that returns a related-table group total must also clear the fact table with ALL. Otherwise items of the same group under other values of that column are left out.
- Must. 2011. https://www.sqlbi.com/articles/ratio-over-subtotals-with-normalized-tables-in-dax/
- When: A parent-group total on a related-table column, in a report that filters other columns of the item table.

**T14-A010-5.** A group-total measure that finds the group with a CONTAINS test on the values of a related group column returns an error when the query does not group by that column: CONTAINS then receives several groups where it needs one value.
- Fact. 2011. https://www.sqlbi.com/articles/ratio-over-subtotals-with-normalized-tables-in-dax/
- When: A measure built with FILTER over all items plus CONTAINS on VALUES of a related group column.

**T14-A010-6.** In DAX the formula for the total of an item's group changes with the model's structure, for example a group column in the item's own table or in related normalized tables. A correct and efficient formula therefore needs knowledge of the data model.
- Fact. 2011. https://www.sqlbi.com/articles/ratio-over-subtotals-with-normalized-tables-in-dax/
- When: Any measure that returns the total of the group an item belongs to.

**T14-A019-1.** A ratio-to-parent measure should return blank at hierarchy levels where the ratio has no meaning, such as a product-over-subcategory ratio on subcategory or category rows. There it would show a pointless 100% or a wrong number.
- Should. Check. 2012. https://www.sqlbi.com/articles/clever-hierarchy-handling-in-dax/
- When: Ratio measures shown in a report that browses a hierarchy.
- Version: Described in 2012.

**T14-A019-2.** To find the hierarchy level being browsed with ISFILTERED, test for an intermediate level that its own column is filtered and the column of the level below is not; a filter on the lowest column means the lowest level.
- Should. Check. 2012. https://www.sqlbi.com/articles/clever-hierarchy-handling-in-dax/
- When: Measures that behave differently per hierarchy level; a slicer on the same columns fools the test.
- Version: Described in 2012, when ISFILTERED was new in DAX.

**T14-A019-3.** Separate ratio-to-parent measures, one per hierarchy level, can be merged into one measure that picks the ratio for the level it detects. The report then shows the share of the parent in a single column, not three columns of which two are blank.
- Option. Check. 2012. https://www.sqlbi.com/articles/clever-hierarchy-handling-in-dax/
- When: A report browses a hierarchy and needs the ratio over the parent at every level.
- Version: Described in 2012.

**T14-A019-4.** A measure that detects the hierarchy level with ISFILTERED on the hierarchy columns returns meaningless numbers once a user filters one of those columns with a slicer: that column then counts as filtered at every level.
- Fact. Check. 2012. https://www.sqlbi.com/articles/clever-hierarchy-handling-in-dax/
- When: Level detection built on ISFILTERED over columns that users can also put in slicers.
- Version: Described in 2012.

**T14-A019-6.** Prefer working out an item's share of its parent level inside a DAX measure over the reporting client's built-in ratio-to-parent display option: logic in the formula is far more flexible and needs no action from the user.
- Should. Check. 2012. https://www.sqlbi.com/articles/clever-hierarchy-handling-in-dax/
- When: Reports that show each item's share of its parent in a hierarchy.
- Version: The comparison made in 2012 was with the ratio-over-parent option of Excel PivotTables.

**T14-A150-3.** Adding a condition to a measure, such as returning blank when sales are zero, does not correct its total. The total evaluates the condition once in its own filter context, where it is met, so rows hidden at detail level are still counted.
- Fact. 2019. https://www.sqlbi.com/articles/summing-values-for-the-total/
- When: Measures such as a working-day count that should include only periods with sales.

**T14-A186-4.** A measure built to iterate at one grain, such as month, still returns values when a report drills below that grain, for example to days. Those values go against intuition: the formula runs at a grain it was not designed for.
- Fact. 2020. https://www.sqlbi.com/articles/obtaining-accurate-totals-in-dax/
- When: A visual shows a grain-specific measure at a finer level than the one it iterates.

**T14-A187-2.** To show on each day its month's result, run the per-month logic in CALCULATE with ALLEXCEPT on the Date table, keeping only the month column: day filters go, the month filter from context transition stays. ALLEXCEPT is right here, though ALL with VALUES is usual.
- Should. 2020. https://www.sqlbi.com/articles/working-below-a-dax-formulas-granularity/
- When: A month-grain measure, iterating months, must return the enclosing month's value below month level.

**T14-A187-3.** Inside an iteration over months, CALCULATE with ALL on the Date table plus VALUES of the month column gives a wrong grand total: VALUES is worked out before context transition, when no month filter is active yet. ALLEXCEPT, a modifier, applies after context transition.
- Fact. 2020. https://www.sqlbi.com/articles/working-below-a-dax-formulas-granularity/
- When: Moving a calculation to month grain inside an iterator over the month column.

**T14-A187-4.** One way to return blank below a measure's supported grain: count the visible rows of the Date table, count them again in a filter context that enforces the supported grain, such as the month, and compute the result only when the two counts are equal.
- Option. 2020. https://www.sqlbi.com/articles/working-below-a-dax-formulas-granularity/
- When: A measure built for month level or above may be placed at a finer level such as day.

### Budget, currency and financial calculations

**T14-A015-2.** One way to compare detailed sales with a budget kept at a coarser grain is a table derived from sales and aggregated to the budget's grain. It needs an ETL step and is less flexible than measures that emulate a virtual relationship.
- Option. Check. 2012. https://www.sqlbi.com/articles/budget-and-other-data-at-different-granularities-in-powerpivot/
- When: A detailed fact table is compared with a coarser table, such as a monthly budget by category.
- Version: Described in 2012.

**T14-A015-4.** A coarse-grain budget can be summed through a virtual relationship: CALCULATE takes one filter per linking column, keeping the budget values found among the visible values of the matching lookup column, tested with CONTAINS over VALUES or by counting a FILTER over VALUES.
- Option. Check. 2012. https://www.sqlbi.com/articles/budget-and-other-data-at-different-granularities-in-powerpivot/
- When: A budget-like table at a coarser grain than the lookup tables, with no physical relationship to them.
- Version: Described in 2012; the shorter CONTAINS form needs the SQL Server 2012 version of PowerPivot or Tabular.

**T14-A015-6.** One test of whether the selection matches a budget table's grain: compare the row count of the detailed fact table in the current filter context with its row count after clearing all fact filters and reapplying only the current values of each virtual-relationship column.
- Option. Check. 2012. https://www.sqlbi.com/articles/budget-and-other-data-at-different-granularities-in-powerpivot/
- When: A budget-like table is linked to lookup tables through virtual relationships on a few columns.
- Version: Described in 2012.

**T14-A138-1.** To show actuals and forecast together, a remaining-forecast measure can return the forecast only for dates after the last date with sales and simply be added to the sales measure: on any day only one of the two has a value.
- Option. Check. 2018. https://www.sqlbi.com/articles/showing-actuals-and-forecasts-in-the-same-chart-with-power-bi/
- When: Actual sales up to the last sale and a budget-based forecast after it, on one chart.
- Version: Described in 2018, when the weak relationships used for the Budget table were new in Power BI.

**T14-A138-2.** When a forecast measure needs the last date with sales, it must remove all filters from the Sales table while working out that date, so that it gets the last date ever and not the last date of the current period.
- Must. 2018. https://www.sqlbi.com/articles/showing-actuals-and-forecasts-in-the-same-chart-with-power-bi/
- When: Measures that combine actuals with a forecast for the dates after the last sale.

**T14-A138-5.** A simple way to adjust a forecast: take the percentage gap between actual sales and budget over the dates that have sales so far, and multiply the remaining forecast by one plus that percentage before adding it to actual sales.
- Option. 2018. https://www.sqlbi.com/articles/showing-actuals-and-forecasts-in-the-same-chart-with-power-bi/
- When: The budget has turned out to differ from actual sales so far, for example because it was too low.

**T14-A138-6.** To chart the combined actuals and forecast measures as running year-to-date lines, it is enough to wrap each of them in CALCULATE with a DATESYTD filter.
- Option. 2018. https://www.sqlbi.com/articles/showing-actuals-and-forecasts-in-the-same-chart-with-power-bi/
- When: The actuals-and-forecast measures are used in a year-to-date line chart.

**T14-A180-1.** When the interest rate changes from year to year, do not use the single constant-rate future value formula. Multiply each invested amount by the product of (1 + rate) over every year in which that investment is active; PRODUCTX can compute it.
- Must. 2020. https://www.sqlbi.com/articles/computing-the-future-value-of-an-investment-based-on-compound-growth-in-dax/
- When: Compound growth where the rate of return differs between years.

**T14-A180-2.** For compound growth with investments added over time, do not model a year-after-year chain that reuses the prior year's result: DAX cannot refer to the previous year's result as a spreadsheet can. Compute the current value of each single investment, then add them up.
- Must. 2020. https://www.sqlbi.com/articles/computing-the-future-value-of-an-investment-based-on-compound-growth-in-dax/
- When: Compound interest or growth over a holding period with investments added over time.

**T14-A180-3.** In a compound growth measure over investments, group the invested amounts by year first and run the compounding iteration over years. The cost then depends on the number of years, not on the number of rows in the investments table, which is scanned once.
- Should. 2020. https://www.sqlbi.com/articles/computing-the-future-value-of-an-investment-based-on-compound-growth-in-dax/
- When: Simple version: every investment starts at the beginning of a year; other dates need a more complex calculation.

**T14-A180-4.** When investments can fall on any date, one way: sum investments by day once, work out each year's invested amount plus its interest accrued to year end at day granularity, then compound those yearly amounts at year level. This longer form is far more efficient.
- Option. 2020. https://www.sqlbi.com/articles/computing-the-future-value-of-an-investment-based-on-compound-growth-in-dax/
- When: Reports at year granularity only; capital reductions are negative amounts; quarters or months need a more complex variant.

**T14-A180-5.** For compound growth over investments on arbitrary dates, avoid a helper measure for the yearly accrued amount that the compounding formula then calls: it leads to nested iterators in the query plan. Prefer one longer measure, which performed much better in tests.
- Should. 2020. https://www.sqlbi.com/articles/computing-the-future-value-of-an-investment-based-on-compound-growth-in-dax/
- When: A compound growth calculation where investments can be made on any date.

**T14-A180-6.** Use the compound growth measure variant that supports quarter or month granularity only when the report truly needs those levels. It must compute accrued interest up to the last day of the selected period, so it is longer and slower; otherwise keep the year-level measure.
- Should. 2020. https://www.sqlbi.com/articles/computing-the-future-value-of-an-investment-based-on-compound-growth-in-dax/
- When: Compound growth measures that may be shown below the year.

**T14-A183-1.** When reports need amounts in one currency only, convert the amounts while the data is imported into the model, wherever possible, and not in DAX at query time: it lowers the complexity of the calculations at query time.
- Should. Check. 2020. https://www.sqlbi.com/articles/currency-conversion-in-power-bi-reports/
- When: Currency conversion where the report shows a single currency.
- Version: Described in 2020.

**T14-A183-2.** When users must pick the reporting currency at query time among several currencies, prefer a dynamic conversion in DAX measures, on a model designed for it, to precomputing the amounts in every reporting currency, which can be hard, costly or impractical.
- Should. Check. 2020. https://www.sqlbi.com/articles/currency-conversion-in-power-bi-reports/
- When: Reports that must be available in several currencies chosen at query time.
- Version: Described in 2020.

**T14-A183-3.** When source data arrives in several currencies and reports must also offer several currencies, one approach is to convert the data to a single currency during import. What is left is the case of single-currency data with several reporting currencies.
- Option. Check. 2020. https://www.sqlbi.com/articles/currency-conversion-in-power-bi-reports/
- When: Data recorded in several currencies, reports required in several currencies.
- Version: Described in 2020.

**T14-A183-4.** In a currency conversion measure, first total the amounts that share one currency and one exchange rate, for example per month when rates are monthly, and apply the rate to each total. Do not convert every single transaction: aggregated amounts perform better.
- Should. Check. 2020. https://www.sqlbi.com/articles/currency-conversion-in-power-bi-reports/
- When: Dynamic conversion in a measure where rates are stored at a coarser grain than the transactions.
- Version: Described in 2020.

**T14-A183-5.** Before relying on a currency conversion measure that groups amounts by month and applies that month's rate, confirm that the model really holds exactly one exchange rate per month and that only one currency is selected. If either fails, the measure returns inaccurate numbers.
- Should. Check. 2020. https://www.sqlbi.com/articles/currency-conversion-in-power-bi-reports/
- When: Dynamic conversion measures that iterate a month-level table of exchange rates.
- Version: Described in 2020.

**T14-A183-6.** A currency conversion measure that returns blank when two or more reporting currencies are selected can have that logic adapted to the requirements, for example to raise an error or to show a different result in that case.
- Option. Check. 2020. https://www.sqlbi.com/articles/currency-conversion-in-power-bi-reports/
- When: Dynamic conversion driven by a currency slicer that allows several selections.
- Version: Described in 2020.

**T14-A183-8.** In a calculation item that converts currency, the Format String Expression can switch to a format string stored for the selected currency, so that converted figures show the right currency symbol. A plain conversion measure keeps a format without the symbol.
- Option. Check. 2020. https://www.sqlbi.com/articles/currency-conversion-in-power-bi-reports/
- When: Readers choose a reporting currency and the conversion is a calculation item.
- Version: Written in 2020, when Analysis Services 2019 and Azure Analysis Services had calculation groups and Power BI did not.

**T14-A183-9.** A calculation item that converts currency should first test whether the current measure needs conversion at all, for example through a naming convention: measure names containing "#" mark quantities and names containing "%" mark percentages, and both stay unconverted.
- Should. Check. 2020. https://www.sqlbi.com/articles/currency-conversion-in-power-bi-reports/
- When: Currency conversion as a calculation item that may be applied to measures that are not amounts.
- Version: Written in 2020, when Analysis Services 2019 and Azure Analysis Services had calculation groups and Power BI did not.

**T14-A326-1.** For an accounts receivable aging report, reshape the source data into a model designed for the requirement; do not import it as it is. Unchanged source data usually forces complex DAX, and each new customer then needs different models and measures.
- Should. 2025. https://www.sqlbi.com/articles/account-receivable-aging-in-power-bi/
- When: Source data whose structure does not fit the aging analysis.

**T14-A326-2.** Avoid matching payments to due dates at query time. Build one accounts receivable fact table at the grain of payments due crossed with payments: each row is the part of a payment allocated to one due date of one invoice.
- Should. 2025. https://www.sqlbi.com/articles/account-receivable-aging-in-power-bi/
- When: Aging analysis where invoices, payments due and payments come from separate tables.

**T14-A326-3.** Before building the receivables detail fact table, prefer an intermediate step: a normalised movements table holding invoices, payments due and payments in one standard structure. The hard transformation to the detail table is then reusable; each new source only has to fill the movements table.
- Should. 2025. https://www.sqlbi.com/articles/account-receivable-aging-in-power-bi/
- When: The source keeps invoices and payments in separate tables with different columns and relationships.

**T14-A326-4.** In the payments table that feeds an accounts receivable model, a payment covering several invoices must be split into one row per invoice with the amount allocated to each. The model can then show a customer who leaves one invoice unpaid while paying later ones.
- Must. 2025. https://www.sqlbi.com/articles/account-receivable-aging-in-power-bi/
- When: Payment data that refers to the invoices it pays.

**T14-A326-5.** If payment data carries no invoice reference, only customer, payment date and amount, consider allocating each payment to the customer's invoices by their due dates.
- Consider. 2025. https://www.sqlbi.com/articles/account-receivable-aging-in-power-bi/
- When: Payments cannot be assigned to invoices from the source data.

**T14-A326-6.** You must allow for the latency of the transformation that builds the receivables detail table, wherever it runs. An aging report of this kind does not suit a real-time setup.
- Must. 2025. https://www.sqlbi.com/articles/account-receivable-aging-in-power-bi/
- When: Aging reports built on a derived detail fact table.

**T14-A326-9.** To compute the open receivable at a reporting date, you can apply the events-in-progress pattern: treat each detail row as an event that contributes its amount due to every reporting date between its due date and its payment date.
- Option. 2025. https://www.sqlbi.com/articles/account-receivable-aging-in-power-bi/
- When: A receivables detail fact table whose rows carry a due date and a payment date.

**T14-A326-10.** To spread open receivables over age ranges, you can apply the dynamic segmentation pattern and merge the open-amount logic and the age-range assignment into one measure, not separate measures: fewer context transitions make it run more efficiently.
- Option. 2025. https://www.sqlbi.com/articles/account-receivable-aging-in-power-bi/
- When: Aging reports that group open amounts by the ranges of an aging range table.

**T14-A326-11.** The aging buckets can live in a table of their own, which may be imported from an external source such as a SharePoint table: that gives users the most flexibility.
- Option. 2025. https://www.sqlbi.com/articles/account-receivable-aging-in-power-bi/
- When: Accounts receivable aging reports.

**T14-A326-12.** When receivable volumes grow large, consider a snapshot table that stores for each reporting date the open rows with their precomputed age range, related to the aging range table. The measure that reads it is simpler and much faster.
- Consider. 2025. https://www.sqlbi.com/articles/account-receivable-aging-in-power-bi/
- When: Large receivable models, about a million invoices in the test described, where the aging chart takes many seconds.
