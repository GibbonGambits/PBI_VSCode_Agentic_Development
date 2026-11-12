# Time intelligence and date tables

Part 1 of 2 of this topic. Covers: Time intelligence functions; Week-based and fiscal calendars; Mark as date table; Incomplete periods and future dates.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### Time intelligence functions

**T04-A024-1.** Take care: a bare date column passed as the dates argument of a time intelligence function such as LASTDATE is implicitly wrapped in CALCULATETABLE and VALUES. Under a row context, context transition can then leave only the current row's date, not the expected period.
- Consider. 2012. https://www.sqlbi.com/articles/usage-of-dates-argument-in-a-row-context/
- When: Any time intelligence function with a dates argument, evaluated under a row context, such as FILTER over the date table.

**T04-A329-2.** Treat a Day of Week column as one whose filter is preserved: a time intelligence calculation should leave its selection as it is while it moves other date filters such as Year and Month. Users mostly want the same weekdays compared across periods.
- Should. Check. 2025. https://www.sqlbi.com/articles/filtering-weekdays-in-dax/
- When: Date tables whose weekday columns are used as slicers together with time intelligence measures.
- Version: Stated in 2025 for the classic functions; check current behaviour.

**T04-A202-1.** When the first or last date of the current period is needed as a value, use MIN and MAX over the date column, not FIRSTDATE and LASTDATE: those return tables needing conversion and trigger context transition; MIN and MAX run entirely in the storage engine.
- Should. 2020. https://www.sqlbi.com/articles/understanding-the-difference-between-lastdate-and-max-in-dax/
- When: Scalar date arithmetic, such as the days between the first and last date of a selection.

**T04-A202-2.** Keep table-returning time intelligence functions such as FIRSTDATE, LASTDATE, NEXTDAY and PREVIOUSDAY for places that need a table, like a CALCULATE filter argument. Where an expression needs one value, pick a scalar function: the implicit table-to-value conversion is costly.
- Should. 2020. https://www.sqlbi.com/articles/understanding-the-difference-between-lastdate-and-max-in-dax/
- When: One of these functions would otherwise sit inside a simple calculation, not a filter.

**T04-A294-6.** Before choosing a short-form time intelligence function, look at the DATEADD or PARALLELPERIOD expression it stands for, so that you decide how the measure behaves at other levels and over several intervals.
- Should. 2024. https://www.sqlbi.com/articles/differences-between-dateadd-and-parallelperiod-in-dax/
- When: Writing measures with time intelligence functions that are short forms of DATEADD or PARALLELPERIOD.

### Week-based and fiscal calendars

**T04-A029-7.** On any custom calendar, helper columns in the calendar table, such as a day-of-year number, are a way to keep the time intelligence DAX simple.
- Option. Check. 2013. https://www.sqlbi.com/articles/week-based-time-intelligence-in-dax/
- When: Custom calendar tables of any kind, not only ISO calendars.
- Version: Written in 2013; a 2020 note points to a newer, more optimised pattern for week-based calculations.

**T04-A319-7.** The standard time intelligence functions can be used only when each year of the calendar begins on the same day of the month: they do not handle years that start on different dates.
- Must. Check. 2024. https://www.sqlbi.com/articles/using-weekly-calendars-in-power-bi/
- When: Models using the standard DAX time intelligence functions.
- Version: Stated in 2024 for the classic functions; check current behaviour.

### Mark as date table

**T04-A199-2.** With a non-Date key such as an integer YYYYMMDD and no date table mark, the filter DATESYTD returns touches the date column only and is combined with the year and month filters already there: year-to-date then equals the plain measure.
- Must. Check. 2016. https://www.sqlbi.com/articles/time-intelligence-in-power-bi-desktop/ ; https://www.sqlbi.com/articles/mark-as-date-table/
- When: The Date table relates to other tables through a column whose type is not Date.
- Version: Power BI Desktop has Mark as Date Table since its February 2018 release.

**T04-A199-3.** Mark the Date table even when its relationship uses a Date-typed column, where DAX already clears the other Date table filters whenever the date column is filtered: the mark adds model metadata that lets client tools give a better experience.
- Should. Check. 2020. https://www.sqlbi.com/articles/mark-as-date-table/
- When: The fact table relates to the Date table on a column of Date data type.

**T04-A199-7.** A model may hold more than one marked date table. In each of them, a filter on the date column chosen at marking clears the other filters on that same table.
- Option. 2020. https://www.sqlbi.com/articles/mark-as-date-table/
- When: A model holds two or more tables marked as date tables.

### Incomplete periods and future dates

**T04-A144-1.** To hide dates after the last data, change the filter context; do not delete rows from the Date table, which would break the behaviour of several time intelligence functions.
- Should. 2019. https://www.sqlbi.com/articles/hiding-future-dates-for-calculations-in-dax/
- When: Models that use DAX time intelligence functions.

**T04-A144-4.** To stop time intelligence measures showing values past the last data, add a Boolean calculated column to the Date table, true up to the final date reports should show (for example the latest fact date), and let every time intelligence function use only flagged dates.
- Should. 2019. https://www.sqlbi.com/articles/hiding-future-dates-for-calculations-in-dax/
- When: The model can be changed and the cut-off date does not vary, for example from measure to measure.
- Version: Only when Power Query cannot supply the value, with its CalculatedReason (storage and security, rule 17; M105).

**T04-A144-5.** When fact tables hold data for different date ranges, give the Date table one date-flag calculated column per fact table, and let each measure filter on the flag of its own fact table.
- Should. 2019. https://www.sqlbi.com/articles/hiding-future-dates-for-calculations-in-dax/
- When: Future dates are hidden with a Date table flag column and several fact tables differ in range.
- Version: Only when Power Query cannot supply the values, with a CalculatedReason (storage and security, rule 17; M105).

**T04-A144-7.** Avoid hiding future dates with an IF that returns blank when the filtered dates lie past the last data. It only hides rows: prior-year figures still cover whole periods, and an inner IF is lost once a time shift is applied.
- Should. 2019. https://www.sqlbi.com/articles/hiding-future-dates-for-calculations-in-dax/
- When: Hiding dates past the last data; IF may do for plain year-to-date, not for prior-year comparisons.

## Special-case techniques and facts

### Time intelligence functions

**T04-A024-2.** To get the intended last date inside a row context, one option is to call LASTDATE directly, not through a measure, with an explicit VALUES of the date column as its dates argument: VALUES reads the filter context first and no automatic CALCULATETABLE is added.
- Option. 2012. https://www.sqlbi.com/articles/usage-of-dates-argument-in-a-row-context/
- When: A time intelligence function with a dates argument runs inside a row context, such as FILTER iterating the date table.

**T04-A024-3.** Another option inside a row context: evaluate the measure that wraps LASTDATE inside CALCULATE, with VALUES of the date column as a filter argument.
- Option. 2012. https://www.sqlbi.com/articles/usage-of-dates-argument-in-a-row-context/
- When: A measure based on LASTDATE is referenced inside a row context, such as FILTER iterating the date table.

**T04-A147-1.** Working days between two dates can be counted as COUNTROWS of the date table inside CALCULATE, filtered by DATESBETWEEN to the span and to rows whose working-day flag is true, for instance in a calculated column of the fact table.
- Option. 2019. https://www.sqlbi.com/articles/counting-working-days-in-dax/
- When: A day count must skip weekends and holidays, and the date table flags working days.
- Version: Only when Power Query cannot supply the value, with its CalculatedReason (storage and security, rule 17; M105).

**T04-A147-3.** A simple way to fill the working-day flag of a date table is to mark a date as non-working when WEEKDAY places it on a Saturday or a Sunday.
- Option. 2019. https://www.sqlbi.com/articles/counting-working-days-in-dax/
- When: A date table needs a working-day flag for working-day calculations.
- Version: Only when Power Query cannot supply the flag, with its CalculatedReason (storage and security, rule 17; M105).

**T04-A329-3.** With a weekday filter active, a shift such as DATEADD moves the dates the weekday filter selected: a previous-month measure returns the matching dates of the month before, not the same weekdays.
- Fact. 2025. https://www.sqlbi.com/articles/filtering-weekdays-in-dax/
- When: A slicer on a Date column such as Day of Week together with a measure that shifts dates.

**T04-A329-4.** To keep a weekday filter through a DATEADD shift: clear the Date filters with ALLEXCEPT keeping the weekday columns, and wrap the shifted dates, worked out with the weekday filter removed, in KEEPFILTERS. An older view drops time intelligence functions for custom filter logic.
- Option. Check. 2025. https://www.sqlbi.com/articles/filtering-weekdays-in-dax/ ; https://www.sqlbi.com/articles/year-to-date-filtering-weekdays-in-dax/
- When: Measures such as previous month that must keep a Day of Week selection; every part of the pattern matters.
- Version: Stated in 2025 for the classic functions; check current behaviour.

**T04-A329-5.** VALUES of a Date column returns only the values that cross-filtering leaves, so putting a weekday filter back with VALUES after a date shift can blank the result at day level. FILTERS returns the values filtered directly and ignores cross-filtering.
- Fact. 2025. https://www.sqlbi.com/articles/filtering-weekdays-in-dax/
- When: Restoring a Day of Week filter inside a time intelligence calculation.

**T04-A329-6.** To restore a weekday filter in a time intelligence measure, prefer ALLEXCEPT on Date keeping the weekday columns to FILTERS of the weekday column: FILTERS always adds a filter table, seven values even with nothing selected, while ALLEXCEPT does nothing when no filter is active.
- Should. Check. 2025. https://www.sqlbi.com/articles/filtering-weekdays-in-dax/
- When: Time intelligence measures that keep a Day of Week selection; the shifted dates must be wrapped in KEEPFILTERS.
- Version: Stated in 2025 for the classic functions; check current behaviour.

**T04-A329-7.** The place of a filter argument inside CALCULATE does not set when it runs: modifiers such as ALLEXCEPT run before the explicit filters are applied, in whatever order they are written.
- Fact. 2025. https://www.sqlbi.com/articles/filtering-weekdays-in-dax/
- When: Any CALCULATE or CALCULATETABLE that mixes modifiers and explicit filters.

**T04-A202-3.** LASTDATE returns a table of one row and one column holding the date, not a date value. Where a scalar is expected DAX silently converts it, so the result is right but carries an extra performance cost.
- Fact. 2020. https://www.sqlbi.com/articles/understanding-the-difference-between-lastdate-and-max-in-dax/
- When: LASTDATE used where one value is expected, such as arithmetic between dates.

**T04-A043-1.** A rolling average over the last N months can average the measure with AVERAGEX over the months inside the DATESINPERIOD window used as CALCULATE filter. The window reaches back N months from the end of the selected period and includes the selected month.
- Option. Check. 2021. https://www.sqlbi.com/articles/rolling-12-months-average-in-dax/
- When: The rolling period is counted in days, months, quarters or years, the units DATESINPERIOD supports.

**T04-A043-2.** In a rolling average filtered by DATESINPERIOD, the grain depends on the column AVERAGEX iterates: dates in place of year-month values give a daily moving average, because the DATESINPERIOD filter always works on days.
- Option. Check. 2021. https://www.sqlbi.com/articles/rolling-12-months-average-in-dax/
- When: Rolling averages on a DATESINPERIOD filter; daily averages are not comparable with monthly amounts in a month-level chart.

**T04-A043-3.** For a month-level rolling average where speed matters, the month-based technique of the month-related calculations pattern is an alternative to a DATESINPERIOD filter, which filters at day grain in every case.
- Option. Check. 2021. https://www.sqlbi.com/articles/rolling-12-months-average-in-dax/
- When: Rolling or moving averages at month level whose performance needs tuning.

**T04-A043-5.** A rolling-average measure becomes a calculation item when SELECTEDMEASURE replaces the specific measure: one calculation group then applies the rolling average to any measure, and reports can show rolling averages of different lengths.
- Option. 2021. https://www.sqlbi.com/articles/rolling-12-months-average-in-dax/
- When: Rolling averages are needed for several measures or several period lengths.

**T04-A294-1.** DATEADD and PARALLELPERIOD return the same at the level of their interval argument and differ below it: one YEAR back, DATEADD gives each month the same month of the year before, while PARALLELPERIOD gives every month the whole year before.
- Fact. 2024. https://www.sqlbi.com/articles/differences-between-dateadd-and-parallelperiod-in-dax/
- When: Prior-period measures shown at a finer level, such as months, than the interval passed, such as YEAR.

**T04-A294-2.** With a MONTH, QUARTER or YEAR interval, DATEADD moves a fully selected month as a whole and the days of a partly selected month one by one, so the day count can change. Fully selected means all its dates are visible in the filter context.
- Fact. Check. 2024. https://www.sqlbi.com/articles/differences-between-dateadd-and-parallelperiod-in-dax/
- When: DATEADD with month, quarter or year intervals over whole or partial months.
- Version: Stated in 2024 for the classic functions; check current behaviour.

**T04-A294-3.** PARALLELPERIOD returns, for each year, quarter or month holding at least one input date, that whole interval moved by the given number of intervals. Zero returns the whole current intervals. The DAY interval is not accepted.
- Fact. Check. 2024. https://www.sqlbi.com/articles/differences-between-dateadd-and-parallelperiod-in-dax/
- When: Any use of PARALLELPERIOD.
- Version: Stated in 2024 for the classic functions; check current behaviour.

**T04-A294-4.** SAMEPERIODLASTYEAR is a short form of DATEADD moving back one year and behaves exactly like that call; the two differ only in how they read.
- Fact. 2024. https://www.sqlbi.com/articles/differences-between-dateadd-and-parallelperiod-in-dax/
- When: Choosing between SAMEPERIODLASTYEAR and DATEADD for a prior-year measure.

**T04-A294-5.** PREVIOUSDAY, PREVIOUSMONTH, PREVIOUSQUARTER and PREVIOUSYEAR read only the first selected date, the NEXT functions the last, so each returns at most one interval. PREVIOUSYEAR is blank when several years are filtered, as in totals; PARALLELPERIOD one year back returns every year but the last.
- Fact. 2024. https://www.sqlbi.com/articles/differences-between-dateadd-and-parallelperiod-in-dax/
- When: Selections or total rows that span several intervals.

**T04-A352-1.** With classic time intelligence, a one-month DATEADD shift at day level maps each day to the same day number of the month before. Extra days of a longer previous month land on no row, so month total and daily rows differ; this cannot be changed.
- Fact. 2026. https://www.sqlbi.com/articles/understanding-dateadd-parameters-with-calendar-based-time-intelligence/
- When: Classic DATEADD by month seen per day, when the target month has more days than the current one.

### Week-based and fiscal calendars

**T04-A029-1.** TOTALYTD, SAMEPERIODLASTYEAR and the other built-in time intelligence functions assume a day of a month sits in the same quarter every year, and SAMEPERIODLASTYEAR matches the same day and month. On a week-based calendar their year-to-date and year-over-year results are invalid.
- Fact. Check. 2013. https://www.sqlbi.com/articles/week-based-time-intelligence-in-dax/
- When: ISO week calendars, and retail or manufacturing calendars such as 4-4-5, 4-5-4 or 5-4-4.
- Version: Written in 2013; a 2020 note points to a newer, more optimised pattern for week-based calculations.

**T04-A029-3.** Do not try to make DATESYTD fit a week-based calendar through its optional year-end-date argument: the last day of such a year usually changes from one year to the next.
- Must. Check. 2013. https://www.sqlbi.com/articles/week-based-time-intelligence-in-dax/
- When: Year-to-date on a week-based calendar such as ISO.
- Version: Written in 2013; a 2020 note points to a newer, more optimised pattern for week-based calculations.

**T04-A029-4.** Period-to-date on an ISO calendar can be a CALCULATE whose date filter keeps the days of the current period up to the current date, tested on the ISO year column, plus the ISO quarter, month or week column, not on the calendar year column.
- Option. Check. 2013. https://www.sqlbi.com/articles/week-based-time-intelligence-in-dax/
- When: The calendar table has ISO year, quarter, month and week columns.
- Version: Written in 2013; a 2020 note points to a newer, more optimised pattern for week-based calculations.

**T04-A029-5.** For previous-year values on an ISO calendar, add to the calendar table a column with each date's day number within its ISO year, and filter the previous ISO year for the same day numbers; SAMEPERIODLASTYEAR matches calendar day and month, which is wrong here.
- Must. Check. 2013. https://www.sqlbi.com/articles/week-based-time-intelligence-in-dax/
- When: Previous-year and year-over-year measures on a week-based calendar, when the DAX should stay simple.
- Version: Written in 2013; a 2020 note points to a newer, more optimised pattern for week-based calculations.

**T04-A029-6.** Previous-year-to-date on an ISO calendar can combine the period-to-date filter with the day-number technique: the ISO day-of-year number, not the date, finds the previous-year day that ends the period.
- Option. Check. 2013. https://www.sqlbi.com/articles/week-based-time-intelligence-in-dax/
- When: The week-based calendar table has an ISO year day number column.
- Version: Written in 2013; a 2020 note points to a newer, more optimised pattern for week-based calculations.

**T04-A029-8.** When CONTAINS inside a FILTER iteration gets the same column as search column and as value to find, the column is checked on each row of the searched table, while the value is computed once, in the outer FILTER's row context. This is easily misread.
- Fact. Check. 2013. https://www.sqlbi.com/articles/week-based-time-intelligence-in-dax/
- When: CONTAINS used inside FILTER, as in a previous-year measure over an ISO calendar.

**T04-A051-1.** When the matching previous-year period has exceptions in the data, such as an ISO week 53 that only some years have, solve the exception by shaping the data, not by writing DAX logic for it: the irregularity belongs to the data.
- Must. Check. 2015. https://www.sqlbi.com/articles/custom-year-over-year-calculation-in-dax/
- When: Year-over-year comparisons where no simple formula gives the previous-year period, whatever mapping the business chooses.

**T04-A051-2.** For a custom year-over-year comparison, give the date table a column that stores, for each day, the previous-year day it is compared with. The mapping logic then stays out of the DAX code.
- Should. Check. 2015. https://www.sqlbi.com/articles/custom-year-over-year-calculation-in-dax/
- When: Custom or ISO calendars where the business decides the mapping, for example what week 53 is compared with.

**T04-A051-3.** With a previous-year mapping column in the date table, a prior-period measure can use CONTAINS to pick the dates that match the mapping values of the current selection and hand them to CALCULATE as a new filter.
- Option. Check. 2015. https://www.sqlbi.com/articles/custom-year-over-year-calculation-in-dax/
- When: Any custom shift that compares the current selection of dates with another set of dates.

**T04-A051-4.** A year-over-year calculation that matches periods by relative week number compares an ISO week 53 with a week of the previous year that has no sales.
- Fact. Check. 2015. https://www.sqlbi.com/articles/custom-year-over-year-calculation-in-dax/
- When: ISO calendars, where week 53 exists only in some years.

**T04-A319-3.** A week-based calendar such as 4-4-5 is an option where the compared figures depend heavily on working days and weekends: each period is made of whole weeks and so holds the same number of working days, which Gregorian months do not.
- Option. Check. 2024. https://www.sqlbi.com/articles/using-weekly-calendars-in-power-bi/
- When: Businesses sensitive to weekends or working days, such as manufacturing and retail; periods no longer match Gregorian months.
- Version: As of October 2024 Power BI had no built-in feature for week-based calendars; check the current state.

**T04-A319-5.** In a week-based calendar, call the month-like units periods, or mark them, for example with an FM prefix for fiscal month, and name each after the Gregorian month most of its days fall in: they do not cover the same days as that month.
- Should. 2024. https://www.sqlbi.com/articles/using-weekly-calendars-in-power-bi/
- When: Week-based calendars such as 4-4-5.

**T04-A319-6.** A week-based calendar cannot give figures equal to Gregorian monthly totals, and its year total usually differs from the company's fiscal year, which can mislead users.
- Fact. 2024. https://www.sqlbi.com/articles/using-weekly-calendars-in-power-bi/
- When: Reports that must agree with Gregorian month totals or a fiscal year of whole Gregorian months.

**T04-A319-8.** For year-over-year on a Gregorian calendar, one option is to move the selection back 364 days, 52 weeks, with DATEADD: the prior period has the same number of days and weekdays, but its value will not equal the Gregorian prior year.
- Option. 2024. https://www.sqlbi.com/articles/using-weekly-calendars-in-power-bi/
- When: Matching the accounting books is not required and the model has no week-based calendar.

**T04-A319-10.** In a 52-week calendar, the extra week added from time to time to stay in line with the Gregorian calendar may be left out of period comparisons; there is no standard practice for that week.
- Option. 2024. https://www.sqlbi.com/articles/using-weekly-calendars-in-power-bi/
- When: Week-based calendars such as 4-4-5 that add a week to the last period every six to seven years.

### Mark as date table

**T04-A073-1.** Once a table is marked as a date table, every CALCULATE that filters the marked date column also gets an automatic ALL over the whole date table, which removes any filter on its other columns.
- Fact. Check. 2016. https://www.sqlbi.com/articles/time-intelligence-in-power-bi-desktop/
- When: The date table carries the Mark as Date Table setting.
- Version: Power Pivot and Analysis Services Tabular have the setting; Power BI Desktop since its February 2018 release.

**T04-A073-2.** Filtering a Date-type column that is the primary key of a relationship also adds ALL over its table automatically, even without the date table mark, so time intelligence can seem to work without the setting.
- Fact. Check. 2016. https://www.sqlbi.com/articles/time-intelligence-in-power-bi-desktop/
- When: A date table related to other tables through a column of Date data type.

**T04-A073-5.** A Date column added to relate a table to the date table must not be a calculated column in Power BI Desktop: the hidden date tables Desktop creates automatically interfere with it. Build it in the source or in Power Query.
- Must. Check. 2016. https://www.sqlbi.com/articles/time-intelligence-in-power-bi-desktop/
- When: A non-Date relationship key is replaced by a Date column so that time intelligence works.
- Version: Only matters for Power BI Desktop before February 2018, which lacked Mark as Date Table.

**T04-A073-8.** A model built in Power Pivot, with the date table marked there, keeps working with every time intelligence function, scalar ones included, after import into Power BI, even when the relationship does not use a Date column.
- Option. Check. 2016. https://www.sqlbi.com/articles/time-intelligence-in-power-bi-desktop/
- When: Only models created in Power Pivot; a Power BI Desktop model cannot be imported there and would be rebuilt.
- Version: Only matters for Power BI Desktop before February 2018, which lacked Mark as Date Table.

**T04-A199-5.** Only a filter on the date column itself triggers the automatic clearing of other Date table filters. A filter on another column, such as calendar year, replaces that column's filter alone, so a measure forcing another year shows, per row, that year's matching month.
- Fact. 2020. https://www.sqlbi.com/articles/mark-as-date-table/
- When: A marked or Date-related Date table, and a measure that filters a column other than the date column.

**T04-A151-2.** A year-to-date or quarter-to-date measure that must honour a weekday selection has to put that column's filter back in CALCULATE, for example VALUES of the weekday column, beside the period filter: the implicit ALL on the date table removed it.
- Must. Check. 2019. https://www.sqlbi.com/articles/year-to-date-filtering-weekdays-in-dax/
- When: Period-to-date measures on a marked date table or a Datetime relationship; period comparisons need custom filter logic instead.

**T04-A329-1.** A filter on the Date table's date column, as CALCULATE sets with DATESYTD or DATEADD, silently removes every other Date table filter, but only with a Date-typed relationship column or a marked date table. A year-to-date measure therefore ignores a weekday slicer.
- Fact. Check. 2019. https://www.sqlbi.com/articles/year-to-date-filtering-weekdays-in-dax/ ; https://www.sqlbi.com/articles/mark-as-date-table/ ; https://www.sqlbi.com/articles/filtering-weekdays-in-dax/
- When: Time intelligence measures while the report filters other date table columns, such as day of the week.
- Version: Marking a date table is possible in Power BI since the February 2018 update.

### Incomplete periods and future dates

**T04-A093-1.** With a partly loaded current period, a prior-year comparison can be limited to matching days: take the latest selected date with a non-blank value, build the range from the first selected date to it, shift the range back one year, and evaluate the measure there.
- Option. Check. 2017. https://www.sqlbi.com/articles/compare-equivalent-periods-in-dax/
- When: Year-over-year where the latest period is incomplete and only days present for the current selection should count.
- Version: Without variables (Excel 2010/2013, Analysis Services Tabular 2012/2014) the code is less efficient.

**T04-A093-2.** In an equivalent-period comparison the cut-off can instead be the latest date with data for any store: run the last-non-blank date search with the store selection ignored, not under the current selection.
- Option. Check. 2017. https://www.sqlbi.com/articles/compare-equivalent-periods-in-dax/
- When: Year-over-year over an incomplete latest period, with one cut-off day shared across all stores.
- Version: Excel 2010/2013 and Analysis Services Tabular 2012/2014 have no variables for this measure.

**T04-A093-3.** Consider taking the cut-off day of an equivalent-period comparison from the data, not from the calendar (such as yesterday), when loads can be late: otherwise the prior-year side covers days the current data does not yet hold.
- Consider. Check. 2017. https://www.sqlbi.com/articles/compare-equivalent-periods-in-dax/
- When: Year-over-year over an incomplete latest period; a cut-off tied to today is less reliable when loads are delayed.

**T04-A144-2.** With a Date table of complete years, a measure on a standard time intelligence function, such as year-to-date with DATESYTD, keeps returning values for periods after the last date with data, which can confuse readers.
- Fact. 2019. https://www.sqlbi.com/articles/hiding-future-dates-for-calculations-in-dax/
- When: The Date table extends past the last date with data.

**T04-A144-6.** When the model cannot be changed, hide future dates in the measure: reduce the dates visible in the filter context to those not later than the last date with data, and give that table to the time intelligence function in place of the date column.
- Should. 2019. https://www.sqlbi.com/articles/hiding-future-dates-for-calculations-in-dax/
- When: No flag column can be added, as with a live connection; the code is slower and more complex.

**T04-A168-1.** A previous-year measure that only shifts dates with SAMEPERIODLASTYEAR returns the whole prior period even when the current one has data for part of its days. At month and year level a full period then faces a partial one, so year-over-year percentages come out wrong.
- Fact. 2019. https://www.sqlbi.com/articles/hiding-future-dates-for-calculations-in-dax/ ; https://www.sqlbi.com/articles/previous-year-up-to-a-certain-date/
- When: The current period's fact data ends before the end of the month or year.

**T04-A168-2.** A previous-year figure can be limited to dates matching the current data with a Boolean calculated column in the Date table, true up to the last fact date moved back twelve months with EDATE, and a previous-year measure that also filters that column to true.
- Option. Check. 2019. https://www.sqlbi.com/articles/previous-year-up-to-a-certain-date/
- When: The current year's fact data ends at some date, and later dates of earlier years should be ignored.
- Version: Only when Power Query cannot supply the value, with its CalculatedReason (storage and security, rule 17; M105).

**T04-A289-1.** Take care showing the latest period with a Relative Date slicer or a TODAY-based filter: 'This Day' or 'This Month' can be empty when data stops the day before, and 'This Month' ends at month end, which can break month-to-date comparisons with the previous month.
- Consider. 2023. https://www.sqlbi.com/articles/computing-mtd-qtd-ytd-in-power-bi-for-the-current-period/
- When: Reports meant to show MTD, QTD and YTD values for the latest available period.

**T04-A289-2.** To show MTD, QTD and YTD for the latest period, filter the visual or page on the last transaction date with a filter that updates by itself; a date picked by hand is wrong as soon as a refresh brings later data.
- Should. 2023. https://www.sqlbi.com/articles/computing-mtd-qtd-ytd-in-power-bi-for-the-current-period/
- When: Visuals or pages that must reflect the most recent date with data.

**T04-A289-3.** One option: a calculated column in the Date table marks the last date with transactions with a fixed text, and a visual, page or report filter selects that text. Inside the column, find the last date in CALCULATE with REMOVEFILTERS, because of context transition.
- Option. 2023. https://www.sqlbi.com/articles/computing-mtd-qtd-ytd-in-power-bi-for-the-current-period/
- When: Reports showing the latest period in the data; needs a Date column flagging dates with transactions.
- Version: Only when Power Query cannot supply the value, with its CalculatedReason (storage and security, rule 17; M105).

**T04-A289-4.** Another option: a calculation group whose item finds the last date with transactions and evaluates SELECTEDMEASURE filtered to it. Used as a visual filter, it makes every measure, MTD, QTD and YTD too, use that date; further items can select its whole month or quarter.
- Option. 2023. https://www.sqlbi.com/articles/computing-mtd-qtd-ytd-in-power-bi-for-the-current-period/
- When: Reports that show time intelligence results for the latest period available in the data.

**T04-A289-5.** A calculation item that selects the month of the last date with data through a Date column other than the date column, such as a year-month number, must clear the Date filters itself with REMOVEFILTERS: only a filter on the date column removes them automatically.
- Must. 2023. https://www.sqlbi.com/articles/computing-mtd-qtd-ytd-in-power-bi-for-the-current-period/
- When: Calculation items that move the filter to a whole period through a Date column other than the date column.

**T04-A289-6.** Without a year-month or year-quarter number column, a calculation item can still select the whole month or quarter of the last date with data: turn that date into a Date filter with TREATAS and give it to PARALLELPERIOD with zero intervals of MONTH or QUARTER.
- Option. 2023. https://www.sqlbi.com/articles/computing-mtd-qtd-ytd-in-power-bi-for-the-current-period/
- When: The Date table has no year-month or year-quarter number column.
