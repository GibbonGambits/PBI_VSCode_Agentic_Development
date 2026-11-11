# Time intelligence and date tables

Part 3 of 3 of this topic. Covers: Date columns, sorting and formats; Blank and placeholder dates; Calendar-based time intelligence.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

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

### Calendar-based time intelligence

**T04-A345-3.** In a calendar, give a category to every Date table column used for hierarchical navigation, even though the calendar-based functions also work when some categories have no column.
- Should. 2025. https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/
- When: Defining a calendar for calendar-based time intelligence.
- Version: Preview feature since the September 2025 release: use it only with the developer's yes.

**T04-A345-4.** Map a column to a complete category (Year, Quarter, Month, Week, Date) only when each value identifies one point in time by itself. A column whose values repeat every year, such as Q1 to Q4, goes to the partial category, such as Quarter of Year.
- Must. 2025. https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/
- When: Defining calendar categories; a Quarter column needs one value per quarter of each year.
- Version: Preview feature since the September 2025 release: use it only with the developer's yes.

**T04-A345-5.** A column used in more than one calendar of the same Date table must be mapped to the same category in each of them.
- Must. 2025. https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/
- When: Date tables with several calendars that share columns.
- Version: Preview feature since the September 2025 release: use it only with the developer's yes.

**T04-A345-6.** Every column tagged in a calendar must be sortable, by its own values or through a sort-by column, because time intelligence has to find the periods before and after the current one. Sort-by columns count as associated columns automatically.
- Must. 2025. https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/
- When: Columns tagged in calendars for calendar-based time intelligence.
- Version: Preview feature since the September 2025 release: use it only with the developer's yes.

**T04-A345-7.** Each calendar category has exactly one primary column, the one the calendar-based functions return in their results; every other column with the same meaning, such as a short month name, is added as an associated column.
- Must. 2025. https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/
- When: Defining calendars, also in TMDL, where each category is a calendarColumnGroup.
- Version: Preview feature since the September 2025 release: use it only with the developer's yes.

**T04-A345-11.** With several calendars on one Date table, check with care which filters a calendar-based function clears and which it keeps: the clearing reaches the columns of the affected levels in every calendar, not only in the calendar the function names.
- Consider. 2025. https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/
- When: Date tables with more than one calendar, for example Gregorian, ISO and fiscal together.
- Version: Preview feature since the September 2025 release: use it only with the developer's yes.

**T04-A352-3.** The developer chooses the Extension and Truncation arguments of calendar-based DATEADD, but must first go through the pros and cons of each option with the report users: no option is right in every case.
- Must. 2026. https://www.sqlbi.com/articles/understanding-dateadd-parameters-with-calendar-based-time-intelligence/
- When: Calendar-based shifts between periods of different length, such as Gregorian months.
- Version: Calendar-based time intelligence is a preview feature: use it only with the developer's yes.

**T04-A352-6.** Keep in mind that the Extension and Truncation behaviour of DATEADD also applies to other time intelligence functions, such as DATESINPERIOD: many of them use DATEADD internally.
- Consider. 2026. https://www.sqlbi.com/articles/understanding-dateadd-parameters-with-calendar-based-time-intelligence/
- When: Calendar-based time intelligence functions other than DATEADD.
- Version: Calendar-based time intelligence is a preview feature: use it only with the developer's yes.

**T04-A352-7.** Calendar-based functions know no calendar by themselves: the Date table must hold columns that say how a year divides into periods, each mapped to its category in one or more calendars. Classic time intelligence needs only the date column and assumes a Gregorian calendar.
- Must. 2025. https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/ ; https://www.sqlbi.com/articles/understanding-dateadd-parameters-with-calendar-based-time-intelligence/
- When: Models using calendar-based time intelligence functions.
- Version: Preview feature since the September 2025 release: use it only with the developer's yes.

**T04-A352-8.** Learn how the calendar-based time intelligence functions behave and set their arguments and metadata to fit what the report requires: some automatic behaviour of the classic functions is gone, and unfitting parameters return unexpected results.
- Must. 2026. https://www.sqlbi.com/articles/understanding-dateadd-parameters-with-calendar-based-time-intelligence/
- When: Measures that use calendar-based time intelligence functions.
- Version: Calendar-based time intelligence is a preview feature: use it only with the developer's yes.

## Special-case techniques and facts

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
- Must. 2026. https://www.sqlbi.com/articles/continuous-axis-for-any-date-table-in-power-bi/ ; https://www.sqlbi.com/articles/creating-a-simpler-and-chart-friendly-date-table-in-power-bi/
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

### Calendar-based time intelligence

**T04-A345-1.** Calendar-based time intelligence takes the shape of the year from Date table columns, not from the Gregorian calendar, so it also handles a 13-month calendar. The older answer for week calendars was hand-written measures built from CALCULATE, FILTER and VALUES.
- Option. 2025. https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/ ; https://www.sqlbi.com/articles/week-based-time-intelligence-in-dax/
- When: Calendars whose periods are built from weeks or otherwise differ from Gregorian months.
- Version: Preview feature since the September 2025 release: use it only with the developer's yes.

**T04-A345-8.** Calendar-based time intelligence does not clear the whole Date table: only columns tagged in some calendar get their filters changed, and untagged Date columns keep theirs. Columns whose filter should stay are so easier to handle than with the classic functions.
- Fact. 2025. https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/
- When: Models using calendar-based time intelligence functions.
- Version: Preview feature since the September 2025 release: use it only with the developer's yes.

**T04-A345-9.** A Date column that fits no category but whose filter should be cleared, such as a season, a moon phase or a relative label like Today, can be added to the calendar with no category, as a time-related column; lateral shifts still keep its filter.
- Option. 2025. https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/
- When: Calendar-based time intelligence, where untagged columns would otherwise keep their filters.
- Version: Preview feature since the September 2025 release: use it only with the developer's yes.

**T04-A345-10.** In calendar-based time intelligence, DATEADD and SAMEPERIODLASTYEAR, the lateral shifts, keep the filters on time-related columns; every other function, a hierarchical shift such as DATESYTD or NEXTMONTH, clears them.
- Fact. 2025. https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/
- When: Calendars that hold time-related columns, that is, columns added with no category.
- Version: Preview feature since the September 2025 release: use it only with the developer's yes.

**T04-A345-12.** When a calendar-based function such as SAMEPERIODLASTYEAR shifts a period, it picks the period at the same relative position inside the shifted parent level, going by the sort order of the calendar columns, not by what a name such as February means.
- Fact. 2025. https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/
- When: Calendar-based functions that shift a selection; the parent is the shifted level, Year for a one-year shift.
- Version: Preview feature since the September 2025 release: use it only with the developer's yes.

**T04-A352-2.** Calendar-based DATEADD by default maps the last day of a shorter month to all remaining days of the longer target month. The daily rows then add up to the month total, but one day can be compared with several, unlike classic DATEADD.
- Fact. 2026. https://www.sqlbi.com/articles/understanding-dateadd-parameters-with-calendar-based-time-intelligence/
- When: Calendar-based DATEADD by month at day level, when the selection holds the last day of a shorter month.
- Version: Calendar-based time intelligence is a preview feature: use it only with the developer's yes.

**T04-A352-4.** Calendar-based DATEADD lets you choose how edge days map. Extension (target period longer): EXTENDING, default; PRECISE, same day number as classic; ENDALIGNED, last day to last day, also sets truncation. Truncation (target shorter): ANCHORED, missing days map to its last day; BLANKS, they return blank.
- Option. 2026. https://www.sqlbi.com/articles/understanding-dateadd-parameters-with-calendar-based-time-intelligence/
- When: Selections finer than the shift interval, between periods of different length, such as days shifted by month.
- Version: Calendar-based time intelligence is a preview feature: use it only with the developer's yes.

**T04-A352-5.** A moving average over a trailing number of months built with calendar-based DATESINPERIOD must pass ENDALIGNED as the Extension argument, so a month end moves to the target month's end; otherwise the window can start a day early and take in an extra month.
- Must. 2026. https://www.sqlbi.com/articles/understanding-dateadd-parameters-with-calendar-based-time-intelligence/
- When: Calendar-based DATESINPERIOD going back by months from the last date of a month shorter than the target month.
- Version: Calendar-based time intelligence is a preview feature: use it only with the developer's yes.
