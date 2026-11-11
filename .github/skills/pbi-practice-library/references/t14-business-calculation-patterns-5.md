# Business calculation patterns

Part 5 of 5 of this topic. Covers: Events, durations and sequences; Averages, working days and trends.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### Events, durations and sequences

**T14-A086-1.** Keeping date and time in two columns also makes the model easier to use. The price is that calculations which put events in sequence become more complex.
- Should. 2016. https://www.sqlbi.com/articles/numbering-sequence-of-events-in-dax/
- When: A model that splits date and time and still has to order events.

**T14-A088-2.** With the inactive relationship switched on inside the measure, the one Date table slices correctly by both dates and stays the only date dimension of the model; in this view, reporting by the second date needs no second date table.
- Should. 2016. https://www.sqlbi.com/articles/analyzing-events-with-a-duration-in-dax/
- When: A fact table with two date columns related to one Date table, one relationship inactive.

**T14-A088-11.** Model an event that lasts over time, such as a contract or an order from order date to ship date, with two date or time columns on its row, one for the start and one for the end, not one point in time.
- Should. 2016. https://www.sqlbi.com/articles/analyzing-events-with-a-duration-in-dax/
- When: Events with a start and an end, analysed for what happens between the two dates.

**T14-A088-12.** When designing a model for events that have a duration, always weigh usability, clarity and performance against one another.
- Must. 2016. https://www.sqlbi.com/articles/analyzing-events-with-a-duration-in-dax/
- When: Models of events with a start and an end, lasting minutes (orders) or years (insurance contracts).

### Averages, working days and trends

**T14-A252-3.** Keep the working-day information as a true-or-false column of the Date table: working days hold TRUE and rest days hold FALSE.
- Should. 2022. https://www.sqlbi.com/articles/rolling-average-with-working-days-in-dax/
- When: Calculations must tell working days from rest days.

**T14-A304-11.** Before choosing the aggregation an item is compared with, such as an average, look at how the data is distributed. Outliers or diverging distributions may be better served by another measure of central tendency.
- Should. 2024. https://www.sqlbi.com/articles/comparing-cumulative-values-for-events-in-different-periods/
- When: Comparing a selected item with a summary of a group of items.

**T14-A369-4.** In a production model, when transaction dates cannot be trusted for this, define the observation period of a per-day average with precise dates of data availability: the first and last transactions do not prove when data collection began or ended.
- Should. 2026. https://www.sqlbi.com/articles/the-hidden-complexity-of-a-daily-average-in-dax/
- When: Transaction dates are not a reliable guide to data availability.

**T14-A369-5.** Avoid deriving the observation boundaries of a per-day average after removing only the Date filter. Clear all report filters, so the same period applies to every product, customer and store selection; otherwise selecting a product can shift the boundaries.
- Should. 2026. https://www.sqlbi.com/articles/the-hidden-complexity-of-a-daily-average-in-dax/
- When: Boundaries are taken from the first and last transaction dates.

**T14-A369-6.** Do not bound each month by its own earliest and latest transaction in a per-day average. Days of the month inside the overall observation period must be counted even before the month's first sale.
- Must. 2026. https://www.sqlbi.com/articles/the-hidden-complexity-of-a-daily-average-in-dax/
- When: One observation period is defined for the whole history.

**T14-A369-7.** The denominator of a per-day average must count only the dates actually selected that fall inside the observation period, days without sales included. Never count the days elapsed from the first selected date to the last: that would include periods the user left out.
- Must. 2026. https://www.sqlbi.com/articles/the-hidden-complexity-of-a-daily-average-in-dax/
- When: Any date selection, including single days or weekdays, or January and March without February.

**T14-A369-8.** Consider telling zero from blank in a per-day average: return zero when observed days are selected but nothing was sold, and blank when no observed day is selected. Zero says the period was observed without sales; blank says it stays out of the average.
- Consider. 2026. https://www.sqlbi.com/articles/the-hidden-complexity-of-a-daily-average-in-dax/
- When: A per-day average over an observation period.
- Version: Any zero-for-blank logic needs the brief's request and an exception to the blank rule (M506).

**T14-A369-12.** Reuse a per-day average function only for additive amounts whose date relationship, observation period and policy on zeros match. A balance or a distinct count needs separate analysis first: an aggregate divided by a day count is not generally the average of daily values.
- Must. 2026. https://www.sqlbi.com/articles/the-hidden-complexity-of-a-daily-average-in-dax/
- When: The same per-day average logic is considered for another amount, such as a balance or distinct customer count.

## Special-case techniques and facts

### Events, durations and sequences

**T14-A086-2.** To order one entity's events when date and time are separate columns, add a running sequence number per entity, starting at one, ideally from the data source. Do not add a combined date-time column or seek the earliest date and time at query time.
- Should. 2016. https://www.sqlbi.com/articles/numbering-sequence-of-events-in-dax/
- When: Events of a customer, product or session must be split into before and after a given event.

**T14-A086-3.** A per-entity event sequence number can be a calculated column that counts, for each row, the rows of the same entity with an earlier date, or with the same date and an earlier or equal time.
- Option. 2016. https://www.sqlbi.com/articles/numbering-sequence-of-events-in-dax/
- When: The data source cannot supply the number, or only at too high a cost; not for very large tables.

**T14-A086-4.** In a calculated column that uses context transition, for example through CALCULATETABLE, to fetch the rows of the same entity, remove the filters with ALLEXCEPT, keeping only the entity column. It is required there to avoid a circular reference.
- Must. 2016. https://www.sqlbi.com/articles/numbering-sequence-of-events-in-dax/
- When: A calculated column with context transition on its own table, such as a per-customer event sequence number.

**T14-A086-6.** With a per-entity sequence number on each event, a second calculated column can hold the sequence number of the entity's first event of a given kind, and a third can compare the two to label each event as before, at or after it, for slicing.
- Option. 2016. https://www.sqlbi.com/articles/numbering-sequence-of-events-in-dax/
- When: A per-entity sequence number column exists; not for very large tables.

**T14-A086-7.** Avoid the event sequence number calculated columns, and the columns derived from them, on very large tables: processing them can take very long and use much memory.
- Should. 2016. https://www.sqlbi.com/articles/numbering-sequence-of-events-in-dax/
- When: Very large tables; up to a few million rows the approach may still be convenient.

**T14-A086-8.** For an event sequence number on a table of at most a few million rows, a DAX calculated column may be the more convenient choice. Weigh it against SQL or Power Query, taking the available hardware into account, before deciding.
- Consider. 2016. https://www.sqlbi.com/articles/numbering-sequence-of-events-in-dax/
- When: The table holds no more than a few million rows.

**T14-A088-3.** For a count of events in progress, such as open orders, the measure's result above day level must be chosen explicitly, for example the count active at the end of the month or the average daily count over the selected period.
- Must. Check. 2016. https://www.sqlbi.com/articles/analyzing-events-with-a-duration-in-dax/
- When: Measures that count events with a start and an end date, shown by month or higher.

**T14-A088-4.** In an events-in-progress measure that iterates dates with AVERAGEX and counts orders in CALCULATE with conditions on the order and ship date keys, add ALL on the Date table as a CALCULATE filter: it removes the date filter that context transition would apply.
- Must. Check. 2016. https://www.sqlbi.com/articles/analyzing-events-with-a-duration-in-dax/
- When: Active orders are counted by iterating dates with start-date and end-date conditions inside CALCULATE.

**T14-A088-5.** A calculation that links events to dates through less-than and greater-than conditions spends most of its time in the formula engine and makes poor use of the cache; only a model change makes it faster. Physical relationships handle equality conditions only.
- Fact. Check. 2016. https://www.sqlbi.com/articles/analyzing-events-with-a-duration-in-dax/
- When: Measures over events with a duration, such as orders open between order date and ship date.
- Version: On SQL Server 2016 or Power BI the measure-only version was judged fast enough.

**T14-A088-6.** To speed up events-in-progress analysis, a calculated table with one row per event for each day it is open, holding date key and event identifier, can be materialized and its rows counted, so that no date range is evaluated at query time.
- Option. Check. 2016. https://www.sqlbi.com/articles/analyzing-events-with-a-duration-in-dax/
- When: The table is far larger than its source and fixes the grain at the event; weigh that first.
- Version: On SQL Server 2016 or Power BI the measure-only version was judged fast enough.

**T14-A088-8.** A precomputed events snapshot table fixes the grain at the event. If it cannot simply be related to the other dimensions needed, either raise the granularity of the snapshot table or guard the measures so they show no numbers the model cannot compute.
- Must. Check. 2016. https://www.sqlbi.com/articles/analyzing-events-with-a-duration-in-dax/
- When: A per-day open events table where relating dimensions such as customers to the events is not straightforward.

**T14-A088-9.** To report the daily value that events with a duration produce, each event's amount divided by its number of days can be precomputed and stored in the per-day open events table. The measure is then a plain SUM of that column.
- Option. Check. 2016. https://www.sqlbi.com/articles/analyzing-events-with-a-duration-in-dax/
- When: Events with an amount, a start and an end date; splitting by dimensions other than date needs allocation decisions.
- Version: Timings as measured in 2016.

**T14-A304-1.** When comparing series that start on different dates, standardise the timeline: measure the time elapsed since a common event, such as publication, first sale or release, and do not compare raw totals or calendar-date series. Older items have had more time to build up values.
- Should. 2024. https://www.sqlbi.com/articles/comparing-cumulative-values-for-events-in-different-periods/
- When: Series that begin at different points in time, such as products since their first sale.

**T14-A304-2.** A column that holds the time elapsed since an item's reference event, such as weeks since publication, has to be stored in the fact table: its value changes from one fact row to the next.
- Must. 2024. https://www.sqlbi.com/articles/comparing-cumulative-values-for-events-in-different-periods/
- When: Building a standardised timeline to compare series that start on different dates.

**T14-A304-4.** Create a dimension table of the elapsed-time values, relate it to the elapsed-time column of the fact table, and use it for the x-axis of the chart. A simple calculated table is enough.
- Should. 2024. https://www.sqlbi.com/articles/comparing-cumulative-values-for-events-in-different-periods/
- When: Charting series on a standardised timeline built from an elapsed-time column in the fact table.

**T14-A304-5.** When the goal is total performance since the reference event, the comparison has to use a measure that accumulates the values up to the current elapsed period, plotted against the elapsed-time dimension.
- Must. 2024. https://www.sqlbi.com/articles/comparing-cumulative-values-for-events-in-different-periods/
- When: Series compared on a timeline of time since an event, where total performance is of interest.

**T14-A304-6.** A cumulative measure on a standardised elapsed-time axis can carry a condition that hides the result for elapsed periods that still lie in the future.
- Option. 2024. https://www.sqlbi.com/articles/comparing-cumulative-values-for-events-in-different-periods/
- When: Cumulative measures plotted against time since an event, where some elapsed periods have not happened yet.

**T14-A304-7.** A measure meant to show the series of one selected item can be written to return a result only when a single item is selected, for example through HASONEVALUE. Users then see no unexpected result when they select no item or several.
- Option. 2024. https://www.sqlbi.com/articles/comparing-cumulative-values-for-events-in-different-periods/
- When: A report compares one selected item with others; the check is optional.

**T14-A304-8.** When there are too many items to compare on one chart, one option plots the selected item against the typical performance of a peer group, such as the average cumulative value of all items released in the same year or after a cut-off date.
- Option. 2024. https://www.sqlbi.com/articles/comparing-cumulative-values-for-events-in-different-periods/
- When: Comparing many series on a timeline standardised to time since an event.

**T14-A304-9.** The slicer that picks the item should be set to single selection.
- Should. 2024. https://www.sqlbi.com/articles/comparing-cumulative-values-for-events-in-different-periods/
- When: A report compares one selected item's series with an average of its peers.

**T14-A304-10.** A line chart of one selected item against an average can be improved: put the item title in small multiples and format that title, so it follows the slicer; rename the measures in the Values area to short names, so the series labels say more.
- Option. Check. 2024. https://www.sqlbi.com/articles/comparing-cumulative-values-for-events-in-different-periods/
- When: A line chart shows a selected item's measure beside an average, with a slicer on the item.
- Version: Described in 2024.

### Averages, working days and trends

**T14-A252-1.** The standard DAX time intelligence functions know nothing of working days and rest days. A calculation that must count working days only cannot be built on them.
- Fact. Check. 2022. https://www.sqlbi.com/articles/rolling-average-with-working-days-in-dax/
- When: Rolling or period calculations that consider working days only.
- Version: Described in 2022.

**T14-A252-2.** Avoid NETWORKDAYS for finding the range of dates that covers a given number of working days for a rolling calculation: it would add a slow filter just to work out that range.
- Should. 2022. https://www.sqlbi.com/articles/rolling-average-with-working-days-in-dax/
- When: A rolling average or similar calculation over the last N working days.

**T14-A252-4.** For a rolling calculation over N working days, give the Date table a calculated column with a running working-day number, growing by one per working day and repeating the previous number on rest days. Ranking working days by ascending date with RANKX builds it well.
- Should. 2022. https://www.sqlbi.com/articles/rolling-average-with-working-days-in-dax/
- When: A rolling average or similar calculation over a number of working days.

**T14-A252-5.** In a working-day rolling average, bound the end of the date range by the actual date of the current period, not by its working-day number. Rest days share the previous working day's number, so Friday would otherwise take in Saturday's sales.
- Must. 2022. https://www.sqlbi.com/articles/rolling-average-with-working-days-in-dax/
- When: A rolling average over working days where sales can also fall on rest days.

**T14-A252-6.** Make a rolling average return blank for dates after the last date with sales. Otherwise it shows values for future dates that slowly sink towards zero, which tells the reader nothing.
- Must. 2022. https://www.sqlbi.com/articles/rolling-average-with-working-days-in-dax/
- When: A rolling average shown over a date axis that runs past the last transaction date.

**T14-A252-7.** When a working-day rolling average cannot use calculated columns, the working-day number can be computed as a temporary column (ADDCOLUMNS over the dates) in a measure variable, and the range defined from it. Slower than a calculated column but acceptable: Date tables are seldom large.
- Option. Check. 2022. https://www.sqlbi.com/articles/rolling-average-with-working-days-in-dax/
- When: Calculated columns cannot be created, as in a report connected live to a model.
- Version: Described in 2022.

**T14-A277-1.** When a formula needs several of the values LINESTX returns, such as slope and intercept, evaluate LINESTX once into a variable and read each value from that variable with SELECTCOLUMNS. This is the most efficient form.
- Should. 2023. https://www.sqlbi.com/articles/implementing-linear-regression-in-power-bi/
- When: More than one output of a LINESTX result is used in the same formula.

**T14-A277-2.** DAX has no syntax to refer to a column of a table held in a variable. A value from such a table is taken out with SELECTCOLUMNS; the one-row, one-column table that results turns into a scalar automatically when a calculation uses it.
- Fact. 2023. https://www.sqlbi.com/articles/implementing-linear-regression-in-power-bi/
- When: Reading the single-row table returned by LINESTX or LINEST from a variable.

**T14-A277-3.** In the result of LINEST and LINESTX the slope columns are numbered Slope1 to SlopeN, one per X series. With a single X expression the slope is therefore read from Slope1, not from a column named Slope.
- Fact. 2023. https://www.sqlbi.com/articles/implementing-linear-regression-in-power-bi/
- When: Reading slope values from a LINEST or LINESTX result.

**T14-A277-4.** Prefer LINESTX for a regression over a chosen set of data points, such as the X values shown in a chart: its first argument is the table to iterate, and its Y and X arguments are expressions evaluated per row. LINEST takes column references.
- Should. 2023. https://www.sqlbi.com/articles/implementing-linear-regression-in-power-bi/
- When: A linear regression whose data points are defined by a table.

**T14-A369-1.** AVERAGEX skips iterations whose expression is blank and includes those that return zero. Averaging a sales measure over dates therefore gives the average over days with sales, not over calendar days, whether it iterates the Date table or the distinct dates.
- Fact. 2026. https://www.sqlbi.com/articles/the-hidden-complexity-of-a-daily-average-in-dax/
- When: Daily averages; the result is right only if the business means the average over selling days.

**T14-A369-2.** For an average per calendar day, one option uses DIVIDE to divide the amount by the count of visible rows of a one-row-per-day Date table. Turning blanks into zero inside AVERAGEX also fixes the day count for a period with sales, but is slower.
- Option. 2026. https://www.sqlbi.com/articles/the-hidden-complexity-of-a-daily-average-in-dax/
- When: The denominator must include days without sales; a calendar longer than the data needs more handling.

**T14-A369-3.** When the Date table covers days before the first or after the last available data, dividing an amount by all visible calendar days understates the daily average for partial months at both ends and for totals that include those days.
- Fact. 2026. https://www.sqlbi.com/articles/the-hidden-complexity-of-a-daily-average-in-dax/
- When: The calendar is longer than the date range of the transactions.

**T14-A369-9.** A per-day average over an observation period can keep the visible non-blank dates between the boundaries, count them, evaluate the amount over that set with KEEPFILTERS, COALESCE a blank amount to zero, and DIVIDE only when both boundaries exist and a date is kept.
- Option. 2026. https://www.sqlbi.com/articles/the-hidden-complexity-of-a-daily-average-in-dax/
- When: Boundaries come from the first and last transaction dates, computed with all report filters removed.
- Version: Any zero-for-blank logic needs the brief's request and an exception to the blank rule (M506).

**T14-A369-11.** When several measures need the same per-day average logic, one option is a user-defined function that takes the amount expression and the two boundary dates, and leaves it to the caller where the boundaries come from. It is bound to the model's Date table.
- Option. 2026. https://www.sqlbi.com/articles/the-hidden-complexity-of-a-daily-average-in-dax/
- When: Per-day average logic shared by several measures, in a model that has a Date table.
