# Time intelligence and date tables

Part 2 of 3 of this topic. Covers: Period-over-period comparisons; Building a Date table; Date columns, sorting and formats; Blank and placeholder dates.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

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

**T04-A321-5.** Relate the one Date table one-to-many to every date column that users may want to aggregate by, not just to one date column of each fact table.
- Should. 2024. https://www.sqlbi.com/articles/blank-in-date-columns-and-dax-time-intelligence-functions/
- When: Several date columns, such as an order date and a delivery date, with all but one relationship inactive.

### Date columns, sorting and formats

**T04-A121-5.** One naming option for a Date table: hidden helper columns, used in internal calculations or to sort other columns, get Pascal case without spaces, which sets them apart from the columns meant for report users.
- Option. 2018. https://www.sqlbi.com/articles/reference-date-table-in-dax-and-power-bi/
- When: Naming the columns of a Date table.

**T04-A121-6.** In a Date table each text period label (year, quarter, month, week) can sort by its own integer column; a label that combines a period with its year, such as month and year, sorts by an integer that keeps increasing across years.
- Option. 2018. https://www.sqlbi.com/articles/reference-date-table-in-dax-and-power-bi/
- When: Designing the text period columns of a Date table.

**T04-A204-7.** Custom format strings in Power BI resemble the FORMAT function's syntax but are not identical. Check each one against Microsoft's documentation of the supported custom format syntax; do not assume FORMAT codes carry over. A quarter number, for instance, cannot be shown.
- Must. 2020. https://www.sqlbi.com/articles/creating-a-simpler-and-chart-friendly-date-table-in-power-bi/
- When: Writing custom format strings for model columns in Power BI.

**T04-A204-8.** In a custom format string, put a backslash before every literal character that must show as written, such as each letter of a fiscal-year prefix, so that it is not read as a format code.
- Should. 2020. https://www.sqlbi.com/articles/creating-a-simpler-and-chart-friendly-date-table-in-power-bi/
- When: A fixed text prefix is added to a value shown through a custom format string.

### Blank and placeholder dates

**T04-A321-1.** Store a missing date as blank, not as a placeholder code or a far-future date: blank says the information is absent and matches the blank row of the Date table without adding unused dates to the calendar.
- Should. 2024. https://www.sqlbi.com/articles/blank-in-date-columns-and-dax-time-intelligence-functions/
- When: Date columns where a missing value is normal, such as a delivery date of orders not yet shipped.

**T04-A321-2.** The Date table's date column never holds a placeholder for a missing date, such as 00000000: real dates only, plus the blank of an invalid relationship. Moving the placeholder to a number or text key does not help: time intelligence needs a true date column.
- Must. 2024. https://www.sqlbi.com/articles/blank-in-date-columns-and-dax-time-intelligence-functions/
- When: Models that use DAX time intelligence and mark missing dates with a code.

**T04-A321-7.** To hide the blank Date row in one slicer only, set a filter that excludes blank on that slicer visual: a visual-level filter has no effect on the other visuals of the report.
- Option. 2024. https://www.sqlbi.com/articles/blank-in-date-columns-and-dax-time-intelligence-functions/
- When: The blank row that blank fact dates add to Date should not be shown in a slicer.

**T04-A321-8.** When a page-level filter hides the blank Date row, put the not-blank test on the date column of the Date table, not on another Date column: it reaches every column of Date and leaves real blanks, such as an empty holiday name, alone.
- Should. 2024. https://www.sqlbi.com/articles/blank-in-date-columns-and-dax-time-intelligence-functions/
- When: The blank Date row is hidden for a whole page, not per visual.

**T04-A321-10.** Do not turn the relationship between Date and a fact table into a many-to-many, limited one just to stop the blank row in Date: totals then need extra measure logic, time intelligence gets slower, and dates missing from Date show only in the total.
- Should. 2024. https://www.sqlbi.com/articles/blank-in-date-columns-and-dax-time-intelligence-functions/
- When: A blank date in the fact table creates a blank row in the Date table.

**T04-A321-11.** Whenever a Date column is compared with < or <=, also test NOT ISBLANK on it: a blank date counts as earlier than every real date, so the blank row is picked up too. For > and >= the test is optional, as a safeguard.
- Must. 2024. https://www.sqlbi.com/articles/blank-in-date-columns-and-dax-time-intelligence-functions/
- When: Filters comparing Date table columns when the table can hold a blank row, as in cumulative totals.

**T04-A321-12.** Keep in mind when iterating the Date table: a plain table reference skips the blank row that an invalid relationship adds, while VALUES of the table includes it. Amounts on blank dates can so go missing without notice.
- Consider. 2024. https://www.sqlbi.com/articles/blank-in-date-columns-and-dax-time-intelligence-functions/
- When: Iterators over a Date table that may hold a blank row because a related fact table has blank dates.

## Special-case techniques and facts

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

### Date columns, sorting and formats

**T04-A121-7.** A Date table can carry a running day number, counted from a fixed origin and skipping February 29, to support moving annual totals that always span 365 days.
- Option. Check. 2018. https://www.sqlbi.com/articles/reference-date-table-in-dax-and-power-bi/
- When: Moving annual totals that must always cover 365 days.

**T04-A175-2.** For reports sliced by fiscal year, add a separate fiscal month-name column that copies the month name and sort it by a new fiscal month-number column. Do not renumber the existing month-number column: the calendar-year order would be lost.
- Should. 2019. https://www.sqlbi.com/articles/sorting-months-in-fiscal-calendars/
- When: A report replaces the calendar year with a fiscal year, for example one starting in July.

**T04-A204-1.** A Power BI line chart with a text column on its X axis treats the axis as Categorical: when many points fall in a small area it shows a scrollbar and does not fit all points.
- Fact. Check. 2020. https://www.sqlbi.com/articles/creating-a-simpler-and-chart-friendly-date-table-in-power-bi/
- When: A text attribute of the Date table, such as a month-and-year label, sits on the X axis.

**T04-A204-2.** A Date table can store period attributes such as Year and Year Month as dates, for example the period's last day, shown as text through a custom format string. They sort correctly and allow a continuous line-chart axis without extra or Sort by Column columns.
- Option. 2020. https://www.sqlbi.com/articles/creating-a-simpler-and-chart-friendly-date-table-in-power-bi/
- When: Period columns used in line charts; not for quarters, and a between slicer then lists every date.
- Version: Custom format strings were a recent addition to Power BI in 2020.

**T04-A204-3.** Where Year and Year Month columns hold dates shown through custom format strings, consider storing the first day of the year or month, not the last: reader feedback reports that line charts then look better.
- Consider. 2020. https://www.sqlbi.com/articles/creating-a-simpler-and-chart-friendly-date-table-in-power-bi/
- When: Date-typed Year and Year Month columns with custom format strings, used in line charts.

**T04-A204-5.** Month or Day of Week could be a single date column, mapping each month or weekday to one arbitrary date shown through a custom format string, in place of name and sort columns. Users gain nothing real; on line charts the axis must become Categorical.
- Option. 2020. https://www.sqlbi.com/articles/creating-a-simpler-and-chart-friendly-date-table-in-power-bi/
- When: Month and Day of Week attributes, which have 12 and 7 values across all years.

**T04-A204-6.** For quarters in a calendar hierarchy keep a text label with a numeric sort column, not a date column with a custom format string, which cannot display quarters. Drop the sort column only when the label sorts by itself, as with year before quarter.
- Should. 2020. https://www.sqlbi.com/articles/creating-a-simpler-and-chart-friendly-date-table-in-power-bi/
- When: A Date table that otherwise stores Year and Year Month as formatted dates.

**T04-A204-9.** A between slicer on a Year or Year Month column of datetime type lists every possible date although the real grain is the year or month. It still selects whole periods whose stored date falls in the range, but the view can mislead.
- Fact. Check. 2020. https://www.sqlbi.com/articles/creating-a-simpler-and-chart-friendly-date-table-in-power-bi/
- When: Year or Year Month columns stored as datetime values in a Date table, used in a between slicer.

**T04-A204-11.** For a continuous X axis over Date table periods, one option is to add columns holding the first or last day of each period and put those on the axis: every point fits without a scrollbar and label density adapts.
- Option. 2020. https://www.sqlbi.com/articles/creating-a-simpler-and-chart-friendly-date-table-in-power-bi/
- When: Line charts over periods of the Date table; the cost is extra columns in that table.

**T04-A371-2.** A continuous line-chart axis on years, quarters, months or weeks of your own Date table needs a hierarchy there: on top a year column with dataCategory Years, at the bottom the key date column with PaddedDateTableDates. Table-level dataCategory, once listed too, has no effect.
- Must. 2026. https://www.sqlbi.com/articles/continuous-axis-for-any-date-table-in-power-bi/
- When: Line charts on a date hierarchy above the day; other visuals, slicers and filters work as usual.
- Version: PaddedDateTableDates is an undocumented property.

**T04-A371-3.** Date-related dataCategory values on columns, such as PaddedDateTableDates or Years, must be written in the model definition itself, for example in the TMDL view or in Tabular Editor: the Data category list of Power BI Desktop does not offer them.
- Must. 2026. https://www.sqlbi.com/articles/continuous-axis-for-any-date-table-in-power-bi/
- When: Setting date-related column categories, for example for a continuous date axis on a line chart.
- Version: Power BI Desktop's Data category list shows only geography, URL, image and barcode values, none for dates.

**T04-A371-4.** When the month level of a continuous-axis date hierarchy already holds the year, as Year Month does, a separate hierarchy built from plain Quarter and Month columns lets the line chart tooltip show names without the year twice. The issue is mostly cosmetic.
- Option. 2026. https://www.sqlbi.com/articles/continuous-axis-for-any-date-table-in-power-bi/
- When: Line charts with a continuous axis on a date hierarchy whose lower-level labels repeat the year.

**T04-A371-5.** Setting dataCategory metadata on a Date hierarchy is an alternative to a Date table whose levels are DateTime columns shown through custom format strings. Choose it for more control over level names, or when other client tools do not fully support such columns as levels.
- Option. 2026. https://www.sqlbi.com/articles/continuous-axis-for-any-date-table-in-power-bi/
- When: A Date table for a continuous axis at month level or coarser.

### Blank and placeholder dates

**T04-A321-4.** When a calculated Date table finds its range by itself, as with CALENDARAUTO, a far-future placeholder date makes it hold every day up to that date: tens of thousands of rows, or even millions.
- Fact. 2024. https://www.sqlbi.com/articles/blank-in-date-columns-and-dax-time-intelligence-functions/
- When: Fact tables that use a far-future date, such as a day in 2199 or 9999, for a missing date.

**T04-A321-6.** A blank in a fact date column related to Date, through an inactive relationship too, also makes the engine add the blank row to Date; it then shows as a blank item in every slicer on a Date column.
- Fact. 2024. https://www.sqlbi.com/articles/blank-in-date-columns-and-dax-time-intelligence-functions/
- When: Fact table date columns that can be blank, related to Date by an active or inactive relationship.

**T04-A321-9.** A page-level filter that removes the blank Date row also acts on every measure of the page that uses the relationship from the date column with blanks: rows with no date in that column drop out of those measures.
- Fact. 2024. https://www.sqlbi.com/articles/blank-in-date-columns-and-dax-time-intelligence-functions/
- When: Pages that exclude the blank Date row and show measures over a date column with blanks.

**T04-A321-13.** BLANK can serve as an open boundary: in DATESBETWEEN it means no lower or no upper limit, and as the start date of DATESINPERIOD it acts as a date before 1900, returning the first dates of the Date table.
- Option. 2024. https://www.sqlbi.com/articles/blank-in-date-columns-and-dax-time-intelligence-functions/
- When: Open-ended date ranges; unrelated to blank values stored in date columns, which these functions never return.
