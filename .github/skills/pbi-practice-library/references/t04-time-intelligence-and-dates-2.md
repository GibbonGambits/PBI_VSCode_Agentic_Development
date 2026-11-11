# Time intelligence and date tables

Part 2 of 3 of this topic. Covers: Incomplete periods and future dates; Period-over-period comparisons; Building a Date table.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### Incomplete periods and future dates

**T04-A144-1.** To hide dates after the last data, change the filter context; do not delete rows from the Date table, which would break the behaviour of several time intelligence functions.
- Should. 2019. https://www.sqlbi.com/articles/hiding-future-dates-for-calculations-in-dax/
- When: Models that use DAX time intelligence functions.

**T04-A144-4.** To stop time intelligence measures showing values past the last data, add a Boolean calculated column to the Date table, true up to the final date reports should show (for example the latest fact date), and let every time intelligence function use only flagged dates.
- Should. 2019. https://www.sqlbi.com/articles/hiding-future-dates-for-calculations-in-dax/
- When: The model can be changed and the cut-off date does not vary, for example from measure to measure.

**T04-A144-5.** When fact tables hold data for different date ranges, give the Date table one date-flag calculated column per fact table, and let each measure filter on the flag of its own fact table.
- Should. 2019. https://www.sqlbi.com/articles/hiding-future-dates-for-calculations-in-dax/
- When: Future dates are hidden with a Date table flag column and several fact tables differ in range.

**T04-A144-7.** Avoid hiding future dates with an IF that returns blank when the filtered dates lie past the last data. It only hides rows: prior-year figures still cover whole periods, and an inner IF is lost once a time shift is applied.
- Should. 2019. https://www.sqlbi.com/articles/hiding-future-dates-for-calculations-in-dax/
- When: Hiding dates past the last data; IF may do for plain year-to-date, not for prior-year comparisons.

### Period-over-period comparisons

**T04-A217-7.** To make one visual alone use a calculation item, select that item in the visual-level filters of the visual.
- Should. 2021. https://www.sqlbi.com/articles/show-previous-6-months-of-data-from-single-slicer-selection/
- When: A calculation item should apply to a single visual, such as a chart of the months before a slicer date.

**T04-A281-9.** Keep CALCULATE and context transition out of a calculated column meant for a relationship: they can cause circular dependencies, and avoiding those takes a far longer formula.
- Should. 2023. https://www.sqlbi.com/articles/comparing-different-school-terms-in-power-bi/
- When: A calculated column that will be a relationship key, such as a sequential period number in Date.

### Building a Date table

**T04-A121-2.** A new model can start from a template file that already holds a complete Date table as a calculated table, which avoids rewriting its DAX and setting display formats, hierarchies and column visibility again each time.
- Option. Check. 2018. https://www.sqlbi.com/articles/reference-date-table-in-dax-and-power-bi/
- When: Creating new models that need a custom Date table.
- Version: The template is a PBIT file; a 2023 note adds that Bravo for Power BI can generate a Date table.

**T04-A121-9.** The first year of a Date table can be computed dynamically from the earliest year of data in the other tables of the model.
- Option. 2018. https://www.sqlbi.com/articles/reference-date-table-in-dax-and-power-bi/
- When: Generating a calculated Date table.

**T04-A121-10.** When the model permits future dates, derive the last year of a generated Date table from the last year of data in the other tables, not from the year of the reference date.
- Should. 2018. https://www.sqlbi.com/articles/reference-date-table-in-dax-and-power-bi/
- When: A calculated Date table in a model set up to allow future dates.

**T04-A152-4.** Auto Date/Time is enabled by default; its switch sits under Data Load in the Options dialog of Power BI Desktop.
- Option. 2019. https://www.sqlbi.com/articles/automatic-time-intelligence-in-power-bi/
- When: Checking or changing the Auto Date/Time setting.

**T04-A153-6.** A basic date table can be extended with more columns as requirements ask, for example the weekday as text or number, the quarter, and fiscal months and years.
- Option. 2019. https://www.sqlbi.com/articles/creating-a-simple-date-table-in-dax/
- When: Reports or calculations need date attributes beyond those of a basic date table.

**T04-A319-2.** A model needs one single Date table as soon as it holds more than one date column, whether the columns sit in one table or in several.
- Must. 2024. https://www.sqlbi.com/articles/using-weekly-calendars-in-power-bi/
- When: Any model with two or more date columns.

## Special-case techniques and facts

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

**T04-A289-1.** Take care showing the latest period with a Relative Date slicer or a TODAY-based filter: 'This Day' or 'This Month' can be empty when data stops the day before, and 'This Month' ends at month end, which can break month-to-date comparisons with the previous month.
- Consider. 2023. https://www.sqlbi.com/articles/computing-mtd-qtd-ytd-in-power-bi-for-the-current-period/
- When: Reports meant to show MTD, QTD and YTD values for the latest available period.

**T04-A289-2.** To show MTD, QTD and YTD for the latest period, filter the visual or page on the last transaction date with a filter that updates by itself; a date picked by hand is wrong as soon as a refresh brings later data.
- Should. 2023. https://www.sqlbi.com/articles/computing-mtd-qtd-ytd-in-power-bi-for-the-current-period/
- When: Visuals or pages that must reflect the most recent date with data.

**T04-A289-3.** One option: a calculated column in the Date table marks the last date with transactions with a fixed text, and a visual, page or report filter selects that text. Inside the column, find the last date in CALCULATE with REMOVEFILTERS, because of context transition.
- Option. 2023. https://www.sqlbi.com/articles/computing-mtd-qtd-ytd-in-power-bi-for-the-current-period/
- When: Reports showing the latest period in the data; needs a Date column flagging dates with transactions.
- Version: A Date table generated by Bravo already has the column that flags dates with transactions.

**T04-A289-4.** Another option: a calculation group whose item finds the last date with transactions and evaluates SELECTEDMEASURE filtered to it. Used as a visual filter, it makes every measure, MTD, QTD and YTD too, use that date; further items can select its whole month or quarter.
- Option. 2023. https://www.sqlbi.com/articles/computing-mtd-qtd-ytd-in-power-bi-for-the-current-period/
- When: Reports that show time intelligence results for the latest period available in the data.

**T04-A289-5.** A calculation item that selects the month of the last date with data through a Date column other than the date column, such as a year-month number, must clear the Date filters itself with REMOVEFILTERS: only a filter on the date column removes them automatically.
- Must. 2023. https://www.sqlbi.com/articles/computing-mtd-qtd-ytd-in-power-bi-for-the-current-period/
- When: Calculation items that move the filter to a whole period through a Date column other than the date column.

**T04-A289-6.** Without a year-month or year-quarter number column, a calculation item can still select the whole month or quarter of the last date with data: turn that date into a Date filter with TREATAS and give it to PARALLELPERIOD with zero intervals of MONTH or QUARTER.
- Option. 2023. https://www.sqlbi.com/articles/computing-mtd-qtd-ytd-in-power-bi-for-the-current-period/
- When: The Date table has no year-month or year-quarter number column.

### Period-over-period comparisons

**T04-A114-1.** A report where users pick two independent periods with slicers and compare them needs a second date table in the model. It can be a calculated table that simply duplicates the existing Date table.
- Must. Check. 2017. https://www.sqlbi.com/articles/filtering-and-comparing-different-time-periods-with-power-bi/
- When: Two custom periods chosen by slicers, each with its own start and length.

**T04-A114-2.** A second date table for a two-period comparison can be linked to the main Date table by one inactive one-to-one relationship, not by an inactive relationship to every fact table. It is less intuitive, and while inactive it leaves calculations sliced by Date untouched.
- Option. Check. 2017. https://www.sqlbi.com/articles/filtering-and-comparing-different-time-periods-with-power-bi/
- When: The model has several fact tables; with one fact table a direct relationship to its date is enough.

**T04-A114-3.** The measure for the second period must, in one CALCULATE, remove every filter on the main Date table and activate the inactive relationship from the second date table with USERELATIONSHIP. The second selection then moves onto Date and filters every related fact table.
- Must. Check. 2017. https://www.sqlbi.com/articles/filtering-and-comparing-different-time-periods-with-power-bi/
- When: A second date table is linked to the main Date table through an inactive relationship.

**T04-A114-4.** When two compared periods differ in length, the comparison-period value must be scaled by a normalization factor. Which factor to use is mainly a business decision, not a technical one.
- Must. Check. 2017. https://www.sqlbi.com/articles/filtering-and-comparing-different-time-periods-with-power-bi/
- When: Two user-selected periods of different duration, such as one month against a full year.

**T04-A114-5.** A simple normalization for periods of different length uses day counts: divide the comparison-period value by its number of days to get a daily average, then multiply by the day count of the current selection.
- Option. Check. 2017. https://www.sqlbi.com/articles/filtering-and-comparing-different-time-periods-with-power-bi/
- When: Two user-selected periods of different duration.

**T04-A177-1.** Be aware that time intelligence comparisons built on consecutive periods may not work well when a report shows a selection of non-consecutive periods: the period shown just before the current one in a visual may not be the previous period in the model.
- Consider. 2019. https://www.sqlbi.com/articles/comparing-with-previous-selected-time-period-in-dax/
- When: Differences must be shown between selected periods that are not consecutive.

**T04-A177-2.** To compare each visual row with the previous selected period: find the highest period number below the current one within ALLSELECTED of the Date table, with KEEPFILTERS on that condition, then CALCULATE the measure for that period number after REMOVEFILTERS on the Date table.
- Option. Check. 2019. https://www.sqlbi.com/articles/comparing-with-previous-selected-time-period-in-dax/
- When: Each row shows one period in natural order, and only selected, visible periods count.

**T04-A217-1.** When a slicer filters the Date table to one month, a visual cannot show other months from that same table on its rows, columns or axis: which axis values appear does not depend on the measure.
- Fact. 2021. https://www.sqlbi.com/articles/show-previous-6-months-of-data-from-single-slicer-selection/
- When: One visual should show months outside the month picked in a Date table slicer.

**T04-A217-2.** To chart the months before a month picked in a slicer, the axis must use columns of a second copy of the Date table that the slicer does not filter; a measure then returns blank for the months that should stay hidden.
- Must. 2021. https://www.sqlbi.com/articles/show-previous-6-months-of-data-from-single-slicer-selection/
- When: A slicer picks one month and a visual must still show earlier months, such as the previous six.

**T04-A217-3.** Relate the Date copy used on the axis to the original Date table, not straight to the fact table, and leave that relationship inactive: the calculation turns it on when the filter worked out on the copy must reach Date.
- Should. 2021. https://www.sqlbi.com/articles/show-previous-6-months-of-data-from-single-slicer-selection/
- When: A Date table copy added so that a visual shows months outside a single slicer selection.

**T04-A217-4.** A calculation that shows the months before the slicer date through a Date table copy should clear every filter already on the Date table with REMOVEFILTERS: the new filter over several months has to take the place of the active one.
- Should. 2021. https://www.sqlbi.com/articles/show-previous-6-months-of-data-from-single-slicer-selection/
- When: Calculations that filter a Date table copy to show prior months from one slicer selection.

**T04-A217-5.** In a calculation that shows prior months through a Date table copy, the filter spanning several months must be applied with KEEPFILTERS: it has to intersect the single month coming from the visual, not replace the existing filter context.
- Must. 2021. https://www.sqlbi.com/articles/show-previous-6-months-of-data-from-single-slicer-selection/
- When: Calculations that filter a Date table copy to show prior months from one slicer selection.

**T04-A217-6.** One option that works with any measure is a calculation item: it takes the last visible date of the Date table, builds the filter of earlier months on the Date table copy with DATESINPERIOD, and evaluates SELECTEDMEASURE under that filter in CALCULATE.
- Option. 2021. https://www.sqlbi.com/articles/show-previous-6-months-of-data-from-single-slicer-selection/
- When: A chart must show any measure over a number of prior months from one slicer selection.

**T04-A217-8.** When readers must choose how many prior months a visual shows, the fixed month count in the calculation must give way to their choice from a parameter table, read with SELECTEDVALUE.
- Must. 2021. https://www.sqlbi.com/articles/show-previous-6-months-of-data-from-single-slicer-selection/
- When: Only when the reader chooses the number of months; a fixed requirement keeps the hard-coded count.

**T04-A281-1.** Use the sequential-number technique for comparing custom periods, such as school terms, seasons or campaigns, only when no two periods overlap. With overlapping periods build something else, for example the pattern for comparing different time periods.
- Should. 2023. https://www.sqlbi.com/articles/comparing-different-school-terms-in-power-bi/
- When: Periods that do not match calendar months, quarters or years; a day belongs to one period or none.

**T04-A281-2.** Give every custom period, across all years, one sequential number of its own and filter on that number, not on a pair such as year and period number: an earlier period is then plain arithmetic, also across a year boundary.
- Should. 2023. https://www.sqlbi.com/articles/comparing-different-school-terms-in-power-bi/
- When: Custom periods that do not overlap, such as school terms.

**T04-A281-3.** Work out the sequential number of a custom period with a formula that always gives the same value for a given year and period; do not rank the periods present, for example with RANKX. Saved report filters then keep their meaning when the table changes.
- Should. 2023. https://www.sqlbi.com/articles/comparing-different-school-terms-in-power-bi/
- When: Building the sequential index for a table of custom periods.

**T04-A281-4.** In a model that compares custom periods, the sequential period number and the helper period number are hidden as technical columns: they tell report users nothing. Only the descriptive period columns stay visible.
- Should. 2023. https://www.sqlbi.com/articles/comparing-different-school-terms-in-power-bi/
- When: Custom periods such as school terms compared through a sequential index column.

**T04-A281-5.** A table of custom periods with start and end dates can be used in two ways: copy its columns into the Date table as calculated columns, or keep it visible and relate Date to it many-to-one on the sequential period number, hidden in Date.
- Option. 2023. https://www.sqlbi.com/articles/comparing-different-school-terms-in-power-bi/
- When: Custom periods such as terms, seasons or campaigns kept in their own table.

**T04-A281-6.** In a calculated column of the Date table that looks up the custom period holding each date, one option is to trap the lookup error with IFERROR and raise your own message with ERROR, pointing to overlapping periods, so the refresh log names the cause.
- Option. 2023. https://www.sqlbi.com/articles/comparing-different-school-terms-in-power-bi/
- When: The periods table might hold overlapping date ranges, which make such columns fail and stop the refresh.
- Version: IFERROR is allowed here only as a justified guard, recorded as an exception to M501.

**T04-A281-7.** A measure that moves from the selected custom period to another by filtering the sequential period number must also clear the filters already on the Date table, with REMOVEFILTERS inside the same CALCULATE.
- Must. 2023. https://www.sqlbi.com/articles/comparing-different-school-terms-in-power-bi/
- When: Previous period or same period last year measures built on a sequential index of custom periods.

**T04-A281-8.** When some Date filters must survive the move to another custom period, for example the weekday or the working-day flag, ALLEXCEPT naming the columns to keep can clear the Date filters in place of REMOVEFILTERS; a slicer on a kept column then still works.
- Option. 2023. https://www.sqlbi.com/articles/comparing-different-school-terms-in-power-bi/
- When: Custom period comparison measures where certain Date columns must keep their filters.

**T04-A281-10.** When the Date table relates many-to-one to a custom periods table, clearing the filters of Date also clears those on the periods table, because it belongs to the expanded Date table. No separate removal is needed.
- Fact. 2023. https://www.sqlbi.com/articles/comparing-different-school-terms-in-power-bi/
- When: A periods table such as school terms related to Date; also holds when ALLEXCEPT is used on Date.

**T04-A281-11.** For arbitrary time periods, describe the periods in columns of the Date table; do not let DAX work out each period's date range at query time. The comparison code stays simpler and runs faster.
- Should. 2023. https://www.sqlbi.com/articles/comparing-different-school-terms-in-power-bi/
- When: Comparing terms, seasons or campaigns that do not match calendar months or quarters.

**T04-A281-12.** With one sequential period number, the previous period is the selected number minus one, and the same period a year earlier is the number minus the count of periods in a year, for example three for school terms.
- Should. 2023. https://www.sqlbi.com/articles/comparing-different-school-terms-in-power-bi/
- When: Comparison measures over non-overlapping custom periods with one sequential number, one period selected.

### Building a Date table

**T04-A121-3.** Remove unwanted columns from the DAX expression of a calculated Date table only as the last customization step: a removed column leaves the table with its hierarchies, and comes back without its hierarchy, visibility and format settings.
- Should. 2018. https://www.sqlbi.com/articles/reference-date-table-in-dax-and-power-bi/
- When: Customizing a calculated Date table by removing or commenting columns in its SELECTCOLUMNS list.

**T04-A121-4.** Edit the long DAX expression of a calculated Date table in an external DAX editor, and move the code between that editor and the model by copy and paste.
- Should. Check. 2018. https://www.sqlbi.com/articles/reference-date-table-in-dax-and-power-bi/
- When: Changing the DAX expression of a calculated Date table.
- Version: Stated in 2018, when the Power BI editor displayed only a limited number of rows.

**T04-A121-8.** When the data ends a few days before today, the reference date behind the relative week, month, quarter and year columns of a Date table can be moved away from the current date, so those relative positions come out right.
- Option. 2018. https://www.sqlbi.com/articles/reference-date-table-in-dax-and-power-bi/
- When: A Date table numbers periods relative to a reference day, by default today, and the data lags behind.

**T04-A121-14.** Give the reference Date table template its parameters in the expected form: holiday country as a supported ISO country code (AU, BE, CA, DE, ES, FR, IT, NL, PT, UK, US); working days of the week and custom fiscal periods in DATATABLE syntax.
- Should. Check. 2018. https://www.sqlbi.com/articles/reference-date-table-in-dax-and-power-bi/
- When: Setting the holiday-country, working-days and custom-fiscal-periods parameters of the template.

**T04-A152-3.** Each hidden Auto Date/Time table filters only the table of its own column, so one date attribute also cannot slice two date columns of one table, such as order date and delivery date, in the same visual.
- Fact. Check. 2019. https://www.sqlbi.com/articles/automatic-time-intelligence-in-power-bi/
- When: A model relies on Auto Date/Time and has several date columns, in one table or across tables.

**T04-A153-3.** CALENDARAUTO takes its year range from every date column of the model, unrelated ones such as customer birth dates included, so its date table can hold many years nobody needs. CALENDAR needs its first and last date supplied.
- Fact. 2019. https://www.sqlbi.com/articles/creating-a-simple-date-table-in-dax/
- When: Generating a date table with CALENDARAUTO or CALENDAR.

**T04-A153-4.** A simple DAX date table: take the dates of CALENDARAUTO and drop those whose year lies outside the range of interest, with the first and last year held in variables computed from MIN and MAX of the transaction date column.
- Option. 2019. https://www.sqlbi.com/articles/creating-a-simple-date-table-in-dax/
- When: Creating a simple calculated date table as a starting point; the variables keep the rest portable between models.

**T04-A319-1.** The hidden Auto Date/Time tables cannot be customized: they hold Year, Quarter, Month and Date, no attribute can be added, and they offer no grouping by week, so no week-based chart or matrix can be built on them.
- Fact. Check. 2019. https://www.sqlbi.com/articles/automatic-time-intelligence-in-power-bi/ ; https://www.sqlbi.com/articles/using-weekly-calendars-in-power-bi/
- When: Users need date attributes beyond year, quarter, month and date; a 52-week year-over-year offset is the one exception.
- Version: As of October 2024 Power BI was described as having no built-in feature for week-based calendars.

**T04-A264-1.** When a predefined Bravo Date template lacks columns or measures you need, or holds some you do not want, you can build your own template and apply it to every model, so no model needs hand edits after the tool has run.
- Option. 2022. https://www.sqlbi.com/articles/customizing-date-and-time-intelligence-templates-in-bravo-for-power-bi/
- When: The predefined template does not fit; several models, or a whole company, share one Date table standard.

**T04-A264-2.** Never edit a Date table that a Bravo template generated: put your additions in new calculated columns. Applying the template again keeps calculated columns but replaces the table's expression with a new one.
- Must. 2022. https://www.sqlbi.com/articles/customizing-date-and-time-intelligence-templates-in-bravo-for-power-bi/
- When: A model is adjusted after the closest Bravo template was applied, with no custom template built.

**T04-A264-3.** Before customising a Bravo Date template, install Visual Studio Code and its Bravo Template Editor extension, and edit the template's JSON files there: each save rebuilds the template package, and a preview of the result shows template errors early.
- Should. Check. 2022. https://www.sqlbi.com/articles/customizing-date-and-time-intelligence-templates-in-bravo-for-power-bi/
- When: Authoring or changing a custom Bravo Date template; the preview needs Bravo open and a compatible model attached.
- Version: Described in 2022; check that the editor extension still works this way.

**T04-A264-4.** In a Bravo template workspace, change only the source files in the src folder; the tooling uses every other file internally.
- Should. 2022. https://www.sqlbi.com/articles/customizing-date-and-time-intelligence-templates-in-bravo-for-power-bi/
- When: Editing a Bravo Date template workspace in Visual Studio Code.

**T04-A264-5.** To go on editing a Bravo template on another computer, copy the whole template workspace folder there. The template package is made for distribution and holds the template in a form that cannot be edited.
- Must. 2022. https://www.sqlbi.com/articles/customizing-date-and-time-intelligence-templates-in-bravo-for-power-bi/
- When: Authoring of a custom Bravo Date template moves to another computer.

**T04-A264-6.** The configuration file of a custom Bravo Date template can change default parameter values, fix parameters so that people applying the template are not asked for them, and set parameters the Bravo screen does not show.
- Option. 2022. https://www.sqlbi.com/articles/customizing-date-and-time-intelligence-templates-in-bravo-for-power-bi/
- When: A custom Bravo Date template whose parameters should be preset for the people who apply it.
