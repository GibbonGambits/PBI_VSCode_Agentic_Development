# Time intelligence and date tables

Part 3 of 3 of this topic. Covers: Calendar-based time intelligence.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

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

### Calendar-based time intelligence

**T04-A345-1.** Calendar-based time intelligence takes the shape of the year from Date table columns, not from the Gregorian calendar, so it also handles a 13-month calendar. The older answer for week calendars was hand-written measures built from CALCULATE, FILTER and VALUES.
- Option. 2025. https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/
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
