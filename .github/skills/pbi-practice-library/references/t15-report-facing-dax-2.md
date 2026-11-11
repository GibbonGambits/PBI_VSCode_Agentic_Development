# Report-facing DAX and report design

Part 2 of 5 of this topic. Covers: Measures written for visuals; Model support for reports; Tooltips, drillthrough and detail rows.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### Measures written for visuals

**T15-A163-3.** When a measure turns a table result into text and the table may hold several rows, use CONCATENATEX; do not rely on VALUES being converted to a scalar, which works only for exactly one row and one column.
- Should. 2019. https://www.sqlbi.com/articles/using-concatenatex-in-measures/
- When: A text measure where a single-row table cannot be assumed.

**T15-A222-1.** Weigh the report's requirements before a measure shows zero where it would be blank. A visible zero says the item had no activity; a dropped row hides the item as if it did not matter. Zeros suit some reports and not others.
- Consider. 2021. https://www.sqlbi.com/articles/how-to-return-0-instead-of-blank-in-dax/
- When: Deciding whether a report should show combinations with no data, such as products without sales.

**T15-A351-2.** Do not add each detail attribute as one more row field of a matrix: every field becomes another hierarchy level, which hampers navigation, can slow the query and blurs the layout.
- Should. 2026. https://www.sqlbi.com/articles/show-transaction-details-on-the-matrix-visual-in-power-bi/
- When: Detail attributes are wanted beside the rows of a matrix.

**T15-A351-12.** Leave out a possible optimisation that makes DAX longer or harder to read and maintain, unless the gain measured in a real environment justifies it.
- Should. 2026. https://www.sqlbi.com/articles/show-transaction-details-on-the-matrix-visual-in-power-bi/
- When: Any performance rewrite of a formula.

### Model support for reports

**T15-A072-4.** Power BI Desktop stores the full file path inside each import query. One dedicated query that holds the path, referenced by every table query, lets a developer on another machine change it in one place.
- Option. Check. 2016. https://www.sqlbi.com/articles/the-space-report-under-the-hood/
- When: Several tables come from the same local file and developers work on different machines.
- Version: From 2016. A query on a local file path also needs the gateway decision recorded (P005).

**T15-A072-5.** Set a column's type in the query step that loads the data, not on the model column. Later measures and default formats then behave as expected, and bad data in a later refresh fails in the query, where it is easier to fix.
- Should. 2016. https://www.sqlbi.com/articles/the-space-report-under-the-hood/
- When: Loading untyped sources such as Excel files, where the guessed type may be Any.

**T15-A188-7.** Measures that exist only to support visual formatting, such as the rank and band measures behind row colouring, can be hidden.
- Option. 2020. https://www.sqlbi.com/articles/applying-color-banding-by-document-number-in-power-bi/
- When: A model holds helper measures whose only role is to improve a visual.

**T15-A296-15.** Measures that exist only as a format string variant of another measure are narrow-purpose: isolate them from the rest of the model by hiding them and stating the intended use case in the description.
- Should. 2024. https://www.sqlbi.com/articles/improving-data-labels-with-format-strings/
- When: Report-specific formats are handled by adding variant measures to the model.
- Version: Here measures stay in the one measures table (model standard rule 1); a separate table needs an exception row (M001).

**T15-A300-9.** Be careful not to add too many field parameters to a semantic model. They are reporting objects; too many clutter the model and confuse developers and model consumers alike.
- Consider. 2024. https://www.sqlbi.com/articles/using-scatterplots-to-find-details-in-reports/
- When: Adding field parameters to a model.

**T15-A312-9.** Keep model objects that exist only to serve one visual apart from the core semantic model: hide those measures, calculation groups and calculated tables, so they do not clutter the model or confuse users and other developers.
- Should. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: Models holding helper objects built for specific visual requirements.
- Version: Here measures stay in the one measures table (model standard rule 1); a separate table needs an exception row (M001).

**T15-A312-10.** In the description of each helper object that exists only for a report, record which visuals rely on it and how it works.
- Should. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: Model objects created only to support specific visuals.

### Tooltips, drillthrough and detail rows

**T15-A113-9.** Keep measure references and context transitions out of detail rows expressions; work out per-line values such as line amount or line cost from columns. Drillthrough may be evaluated for every row of a large table, so a context transition costs much memory and time.
- Should. Check. 2017. https://www.sqlbi.com/articles/controlling-drillthrough-using-detail-rows-expressions-in-dax/
- When: Writing a detail rows expression over a large table.
- Version: The source notes that Excel returns only the first 1,000 drillthrough rows by default.

**T15-A231-12.** Whoever builds the model must keep its drillthrough expressions efficient: their speed is that person's responsibility.
- Must. 2021. https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/
- When: Defining a detail rows expression or a default detail rows expression in a tabular model.

**T15-A318-4.** Extra context such as absolute figures can go in a tooltip, with three limits in mind: tooltips offer little formatting, readers must hover, and comparing categories within or across visuals becomes impractical.
- Option. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: A visual shows a variance but lacks supporting figures.
- Version: Tooltips are off by default here: the visual needs its exception row in the brief.

## Special-case techniques and facts

### Measures written for visuals

**T15-A072-3.** Where the requirement is to show zero, not blank, for a selection without matching rows, adding zero to the measure result is one way. A blank result can otherwise make the item vanish from a chart or table.
- Option. 2016. https://www.sqlbi.com/articles/the-space-report-under-the-hood/
- When: Only when the report must display zero in place of hiding the item.
- Version: Departs from the blank-stays-blank default (M506): only for a zero the brief asks for, listed as an exception.

**T15-A072-9.** Visibility logic a visual cannot apply, such as the top three of one group plus the top one of another, can go into the measure: it returns blank for members to hide, and a parameter table sets how many to show.
- Option. 2016. https://www.sqlbi.com/articles/the-space-report-under-the-hood/
- When: The filter logic a visual needs cannot be configured on the visual itself.

**T15-A163-1.** A measure that returns the name of the top item as text must return every tied item when there is a tie, for example by joining the rows TOPN returns into one string with CONCATENATEX. Showing one of them hides the tie.
- Must. 2019. https://www.sqlbi.com/articles/using-concatenatex-in-measures/
- When: A text measure reports the best performer or a similar top item, and ties are possible.

**T15-A163-2.** When values tie, TOPN returns every tied row, so a request for one row can return several.
- Fact. 2019. https://www.sqlbi.com/articles/using-concatenatex-in-measures/
- When: TOPN is used to pick a single top row and ties are possible.

**T15-A163-4.** To put each item that CONCATENATEX joins on its own line, give it a delimiter, its third argument, that contains the line feed from `UNICHAR ( 10 )`, for example after a comma.
- Option. 2019. https://www.sqlbi.com/articles/using-concatenatex-in-measures/
- When: A text measure may list several items, such as tied top performers.

**T15-A222-2.** Power BI builds most of its queries on SUMMARIZECOLUMNS, which drops every row whose computed values are all blank. Combinations with no data therefore vanish from the visual; they do not show as empty or zero. This is by design, to keep reports short.
- Fact. 2021. https://www.sqlbi.com/articles/how-to-return-0-instead-of-blank-in-dax/
- When: Explaining why items without data are missing from a visual.

**T15-A222-3.** When zeros should appear only for some combinations, do not just add zero to the measure result: that turns every blank into zero, also for combinations that never had data, such as years that exist only in the Date table. The logic must be selective.
- Must. 2021. https://www.sqlbi.com/articles/how-to-return-0-instead-of-blank-in-dax/
- When: A measure must show zero for a controlled subset of combinations, not for all of them.
- Version: Any zero-for-blank logic needs the brief's request and an exception to the blank rule (M506).

**T15-A222-4.** One selective way to show zero for blank: the measure finds the first and last transaction dates and adds zero only when the current date, or the selected date range, falls inside that span. It is fast and gives correct results.
- Option. 2021. https://www.sqlbi.com/articles/how-to-return-0-instead-of-blank-in-dax/
- When: Simple cases; it cannot start the zeros before the first sale, for example at a product launch date.
- Version: Any zero-for-blank logic needs the brief's request and an exception to the blank rule (M506).

**T15-A222-5.** For general or complex rules on where zero replaces blank, keep the logic out of DAX: list the combinations that should show zero in a physical table related to the relevant dimensions, and add zero only where it has rows; cost moves to processing time.
- Should. 2021. https://www.sqlbi.com/articles/how-to-return-0-instead-of-blank-in-dax/
- When: Complex requirements; when the start depends on the product alone, a column in the Product table is enough.
- Version: Any zero-for-blank logic needs the brief's request and an exception to the blank rule (M506).

**T15-A222-8.** The zero-for-blank logic written for one measure can move into a calculation group, so that it applies to any measure and report users choose between showing blank and showing zero.
- Option. 2021. https://www.sqlbi.com/articles/how-to-return-0-instead-of-blank-in-dax/
- When: Several measures need the same choice between blank and zero.
- Version: Any zero-for-blank logic needs the brief's request and an exception to the blank rule (M506).

**T15-A312-1.** A measure that calls RAND returns a new random value at every interaction with the report, so chart positions driven by it keep moving. Readers find that irritating and may think the visual is being filtered.
- Fact. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: A visual, such as a jitter plot, whose axis is driven by a RAND-based measure.

**T15-A312-2.** Random jitter values stay stable when computed once with RAND in a column of a calculated table, or in a calculated column, with the axis measure reading the stored value. A stored column changes only when its table refreshes.
- Option. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: Visuals that need random offsets, such as a jitter plot on a scatterplot.
- Version: A calculated column or table here carries its reason line (M105).

**T15-A312-15.** A chart that compares one selected item with the distribution of all others can end with a title from a measure that states the selected value and, where useful, context such as how many data points fall below it.
- Option. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: Charts comparing a selected item against all others.

**T15-A318-2.** To compare a year still in progress with the same period a year earlier, the SAMEPERIODLASTYEAR dates in the prior-year measure can be limited to those flagged by a date-table calculated column that marks dates with sales. No cumulative year-to-date calculation is then needed.
- Option. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: A previous-year target measure set against a current year that is not complete.
- Version: The calculated column carries its reason line (M105).

**T15-A351-1.** To show many attributes of a business entity or transaction, above all in a matrix, combine the relevant fields into one column instead of one column per attribute: many columns take space, force horizontal scrolling and read badly.
- Should. 2026. https://www.sqlbi.com/articles/show-transaction-details-on-the-matrix-visual-in-power-bi/
- When: Many descriptive attributes must be visible for each item.

**T15-A351-4.** The details of a unique identifier, such as an order, product or customer code, can be shown in the matrix itself by a details measure placed after the other measures, in place of a separate table visual that readers must click to sync.
- Option. 2026. https://www.sqlbi.com/articles/show-transaction-details-on-the-matrix-visual-in-power-bi/
- When: A matrix lists items by a unique identifier and readers want their details.

**T15-A351-5.** The layout of a details measure can first be checked with a prototype measure that returns a fixed text for one chosen item, before the real logic is written.
- Option. 2026. https://www.sqlbi.com/articles/show-transaction-details-on-the-matrix-visual-in-power-bi/
- When: Starting a details measure.

**T15-A351-6.** A details measure can be guarded with ISINSCOPE on the identifier column, so that it returns text only when the identifier is really a row of the visual, and not when it is merely filtered from outside.
- Option. 2026. https://www.sqlbi.com/articles/show-transaction-details-on-the-matrix-visual-in-power-bi/
- When: A details measure must stay blank on rows where several items share a value.

**T15-A351-7.** Once a measure has checked that exactly one item is in scope and has visible rows, it can read column values with VALUES, not SELECTEDVALUE, which costs more because it rests on a DISTINCTCOUNT.
- Option. 2026. https://www.sqlbi.com/articles/show-transaction-details-on-the-matrix-visual-in-power-bi/
- When: Only after a test such as ISINSCOPE plus a non-empty check on the fact table.
- Version: The DAX standard reads one value with SELECTEDVALUE (rule 4); keep this form only for a measured gain.

**T15-A351-8.** Several attribute values can be joined into one text by putting them in a table constructor, dropping the empty entries with FILTER and joining the rest with CONCATENATEX and a fixed separator; the result is BLANK when every value is empty.
- Option. 2026. https://www.sqlbi.com/articles/show-transaction-details-on-the-matrix-visual-in-power-bi/
- When: A measure builds one text from several columns, some of which may be empty.

**T15-A351-9.** Filtering one fact-table identifier does not filter the related dimension: a details measure that shows dimension columns must pass the filter from the fact table to that dimension, for example with CROSSFILTER set to both directions inside CALCULATE or CALCULATETABLE.
- Must. 2026. https://www.sqlbi.com/articles/show-transaction-details-on-the-matrix-visual-in-power-bi/
- When: Details grouped by a fact-table identifier show attributes of a related dimension.

**T15-A351-10.** In a details measure, prefer an outer CONCATENATEX over the one related row, obtained with CALCULATETABLE, with the columns read directly in an inner concatenation, to fetching each column with VALUES: fewer storage engine queries and a plain list of columns.
- Should. 2026. https://www.sqlbi.com/articles/show-transaction-details-on-the-matrix-visual-in-power-bi/
- When: The identifier is in scope, so the outer iterator sees one row only.

**T15-A351-11.** The variant of a details measure built on SUMMARIZE needs no both-direction filter and can mix columns of several tables, but lists the columns twice: use it only when you can prove it is faster and needed.
- Should. 2026. https://www.sqlbi.com/articles/show-transaction-details-on-the-matrix-visual-in-power-bi/
- When: Choosing the form of a details measure.

**T15-A351-13.** For details of each line of an order, not of the order as a whole, a measure can iterate the fact rows with CONCATENATEX, read dimension columns with RELATED, and separate the lines with a new-line character from UNICHAR.
- Option. 2026. https://www.sqlbi.com/articles/show-transaction-details-on-the-matrix-visual-in-power-bi/
- When: Per-line details, for example per product, of the selected order.

**T15-A351-14.** The repeated inner step of a details measure, which drops empty values and concatenates the list, can move into a user-defined function used by several measures; it shortens the code and changes nothing in performance.
- Option. 2026. https://www.sqlbi.com/articles/show-transaction-details-on-the-matrix-visual-in-power-bi/
- When: Several details measures repeat the same concatenation logic.
- Version: User-defined functions need compatibility level 1702 or higher (M801).

### Model support for reports

**T15-A072-6.** A shared dimension the source lacks can be built in Power Query: combine the attribute column from each table, remove duplicates and blanks, and relate the result to all those tables.
- Option. 2016. https://www.sqlbi.com/articles/the-space-report-under-the-hood/
- When: The same attribute sits in several tables and has no source table of its own.

**T15-A072-8.** When data cannot be bound to a visual in its present shape, a dedicated table shaped for that visual, even a redundant one, is an option: for example several sources appended, with a column that names the origin of each row.
- Option. 2016. https://www.sqlbi.com/articles/the-space-report-under-the-hood/
- When: One visual must show data from different tables or sources together.

**T15-A222-6.** Build the helper table that lists where a measure shows zero for blank in Power Query, not as a DAX calculated table: built in DAX it exposes the model to circular dependencies.
- Should. 2021. https://www.sqlbi.com/articles/how-to-return-0-instead-of-blank-in-dax/
- When: A model uses a physical table to drive where zero replaces blank.

**T15-A222-7.** If the helper table listing where zero replaces blank grows too large, it can be stored by month and related to the Date table through a many-to-many cardinality relationship on a year-month column. The smaller table offsets the added complexity; speed is similar.
- Option. 2021. https://www.sqlbi.com/articles/how-to-return-0-instead-of-blank-in-dax/
- When: The day-level helper table is too big; a month grain rules out a regular relationship with Date.
- Version: A many-to-many relationship is listed with its reason as an exception (M406).

**T15-A296-14.** Report-specific formatted measures can live in a proxy composite model that the reports connect to, while other users keep using the original model. It adds management overhead and composite model limits, and its author can override the original measures' formats and definitions.
- Option. 2024. https://www.sqlbi.com/articles/improving-data-labels-with-format-strings/
- When: Report-specific format strings must stay out of the main model.

**T15-A312-11.** A helper calculated table built only for a visual can also be marked private. A private object stays out of view even when hidden objects are shown, and DAX autocomplete does not offer it.
- Option. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: A report-only helper table, such as a disconnected table of category names used for highlighting.
- Version: A calculated table carries its reason line (M105); one without a relationship is listed as an exception (M411).

### Tooltips, drillthrough and detail rows

**T15-A113-3.** In a detail rows expression, return only the columns that help the reader, and show readable descriptions such as product, store and customer names in place of internal keys.
- Should. 2017. https://www.sqlbi.com/articles/controlling-drillthrough-using-detail-rows-expressions-in-dax/
- When: Choosing the columns that drillthrough on a measure returns.

**T15-A113-4.** Give DETAILROWS one measure as its argument, not a more complex expression: the design tool only warns, but after deployment such a call makes the user's query fail with an unexpected-exception error.
- Should. Check. 2017. https://www.sqlbi.com/articles/controlling-drillthrough-using-detail-rows-expressions-in-dax/
- When: Any use of DETAILROWS, which returns a table and combines with other table expressions.
- Version: Seen in 2017 with Analysis Services tooling; check current behaviour.

**T15-A113-5.** For a measure built from two other measures, the detail rows expression can call DETAILROWS on each, join the two results with NATURALINNERJOIN, which drops the columns they share, and add derived columns with ADDCOLUMNS.
- Option. Check. 2017. https://www.sqlbi.com/articles/controlling-drillthrough-using-detail-rows-expressions-in-dax/
- When: A measure such as a margin combines the detail rows of sales and cost.
- Version: Stated in 2017; check current behaviour.

**T15-A113-6.** When a measure evaluates a base measure under a changed filter context, write its detail rows expression as DETAILROWS of the base measure inside CALCULATETABLE, with the same filter modifiers the measure uses.
- Should. 2017. https://www.sqlbi.com/articles/controlling-drillthrough-using-detail-rows-expressions-in-dax/
- When: Year-to-date, prior-year and similar variants of a base measure.

**T15-A113-8.** When one measure's drillthrough should equal another's, call DETAILROWS on that other measure; do not copy its detail rows expression.
- Should. 2017. https://www.sqlbi.com/articles/controlling-drillthrough-using-detail-rows-expressions-in-dax/
- When: For example a year-over-year percentage that reuses the detail rows of the year-over-year difference.

**T15-A231-1.** Without a detail rows expression, drillthrough on a measure returns all columns of the measure's own table, hidden ones included and none from related tables, for the visible rows. It ignores filter changes inside the measure and returns nothing useful for a separate measures table.
- Fact. 2017. https://www.sqlbi.com/articles/controlling-drillthrough-using-detail-rows-expressions-in-dax/ ; https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/
- When: A PivotTable drills into a measure that has no detail rows expression; Excel returns 1,000 rows by default.

**T15-A231-2.** Besides a detail rows expression on one measure, a table can carry a default detail rows expression, which every measure of that table without its own then uses. The client receives that table expression evaluated in the measure's filter context.
- Option. Check. 2017. https://www.sqlbi.com/articles/controlling-drillthrough-using-detail-rows-expressions-in-dax/ ; https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/
- When: Users drill through measures from a client such as an Excel PivotTable.
- Version: Compatibility level 1400 or higher; at first usable from Excel only. Not in a model with a calculation group.

**T15-A231-3.** The detail rows expression of a measure and the default detail rows expression of a table accept only a DAX table expression; an expression that returns a scalar gives an error.
- Fact. 2021. https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/
- When: Defining custom drillthrough for measures or tables in a tabular model.

**T15-A231-5.** A detail rows expression can give the chosen columns plain names without the table prefix and read descriptive attributes, such as product or customer names, from related tables with RELATED. The client still shows each name in square brackets, which cannot be removed.
- Option. 2021. https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/
- When: Shaping the columns that Excel drillthrough returns from a tabular model.

**T15-A231-6.** When a measure should share another measure's drillthrough, set its detail rows expression to DETAILROWS of that measure. For measures in a separate measures table, do this per measure and not as a table default, which later measures would inherit, suitable or not.
- Option. 2021. https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/
- When: Measures hosted in a measures table need the drillthrough of measures defined elsewhere.

**T15-A231-7.** For a measure that changes the filter context, such as a same-period-last-year measure, the detail rows expression can wrap DETAILROWS of the base measure in CALCULATETABLE with the same filter function. The default drillthrough ignores filter changes made inside the measure.
- Option. 2021. https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/
- When: Excel drillthrough on measures whose definition shifts or changes the filter context.

**T15-A231-8.** When users want a summarised drillthrough, as for a year-over-year difference, the detail rows expression must change the granularity and aggregate, for instance one row per date with current and prior-year values. An older alternative appends the detail rows of both periods with UNION.
- Must. 2021. https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/ ; https://www.sqlbi.com/articles/controlling-drillthrough-using-detail-rows-expressions-in-dax/
- When: Business users expect an aggregated drillthrough view, not every transaction of both periods.

**T15-A231-9.** Numeric columns returned by a detail rows expression have no format string that can be set, and rounding them in the expression removes the dropped digits for good. A measure format in a PivotTable only hides decimals and keeps the full number.
- Fact. 2021. https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/
- When: Writing detail rows expressions that return numeric columns.

**T15-A231-10.** A measure has one drillthrough behaviour, so several detail views for the same PivotTable filters need one dedicated measure per view: for example a measure that shows how many customers will be listed and whose drillthrough returns those distinct customers.
- Option. 2021. https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/
- When: Users need more than one kind of detail list, such as customers and products, for the same cell.

**T15-A231-11.** Where detailed data tables are a key need, Excel drillthrough with custom detail rows expressions can serve them efficiently: it runs as one DAX query and can return tens of thousands of rows in seconds, while a PivotTable with many attributes on rows is slow.
- Option. 2021. https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/
- When: Users need detail-level extracts from a tabular model in Excel.

**T15-A231-13.** A table expression needed in several places can be stored as the detail rows expression of a hidden measure and called with DETAILROWS, which gives a library of table functions. Those host measures are not meant to be seen or used by report users.
- Option. Check. 2021. https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/
- When: The same table expression is reused across a tabular model.
- Version: Older than user-defined functions, which this template suggests for logic held once; check current behaviour.

**T15-A231-14.** To try Analyze in Excel on a model open in Power BI Desktop without publishing it, one option is the external tool Analyze In Excel for Power BI Desktop, started from its button on the External Tools ribbon.
- Option. Check. 2021. https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/
- When: Testing PivotTable behaviour, such as custom drillthrough, on an unpublished Desktop model.
- Version: As of 2021; an external tool, outside this template's tools.

**T15-A145-1.** For a measure that lists the active filters, let DAX Studio's Define Filter Dump Measure command generate the code and copy it into a measure in Power BI Desktop; the hand-written version is long and repetitive.
- Should. 2019. https://www.sqlbi.com/articles/displaying-filter-context-in-power-bi-tooltips/
- When: Building a filter-listing measure for one table or all; drop the DEFINE and MEASURE lines when pasting.
- Version: DAX Studio 2.8 or later; DAX Studio is a tool outside this template.

**T15-A145-2.** To validate or debug a report, a measure that lists the active filters can go into the tooltip fields of a visual: it shows the filter context of each data point, including filters the standard filter display leaves out.
- Option. 2019. https://www.sqlbi.com/articles/displaying-filter-context-in-power-bi-tooltips/
- When: A measure returns unexpected results on a visual that supports tooltips.
- Version: Tooltips are off by default here: the visual needs its exception row in the brief.

**T15-A145-3.** The filter list in a visual's header shows the filters that come from outside the visual, such as slicers and cross-highlighting. It leaves out the visual-level filters, which can change results in non-obvious ways when they filter a measure.
- Fact. Check. 2019. https://www.sqlbi.com/articles/displaying-filter-context-in-power-bi-tooltips/
- When: Checking which filters affect a visual through its header.
- Version: Seen in 2019, with the updated filter pane setting on. Header icons here need an exception row in the brief.

**T15-A145-4.** Power BI evaluates a measure shown in a visual's tooltip without the cross-highlighting filter that comes from other visuals, so the tooltip value does not reflect that cross-highlight.
- Fact. 2019. https://www.sqlbi.com/articles/displaying-filter-context-in-power-bi-tooltips/
- When: Reading values or filter context through a tooltip measure while another visual cross-highlights this one.
- Version: Tooltips are off by default here: the visual needs its exception row in the brief.

**T15-A145-6.** To inspect a table or matrix with a filter-listing tooltip measure, the visual can be turned into a chart for a while, so that its tooltip properties become available.
- Option. Check. 2019. https://www.sqlbi.com/articles/displaying-filter-context-in-power-bi-tooltips/
- When: Debugging a table or matrix visual.
- Version: From 2019, when tables and matrices had no tooltips. Tooltips need the visual's exception row in the brief.

**T15-A145-7.** A report tooltip page holding a table or card that shows a filter-listing measure, with word wrap on, displays the filter context of table and matrix visuals. It takes some effort to set up.
- Option. Check. 2019. https://www.sqlbi.com/articles/displaying-filter-context-in-power-bi-tooltips/
- When: Showing the filter context behind cells of a table or matrix visual.
- Version: From 2019. Needs the visual's tooltip exception row; text size and font stay with the theme.

**T15-A145-8.** Tabular Editor users can run a script that creates a filter-listing measure directly in the model.
- Option. Check. 2019. https://www.sqlbi.com/articles/displaying-filter-context-in-power-bi-tooltips/
- When: A filter-listing measure is wanted without typing it by hand.
- Version: In 2019 the script supported Analysis Services; on Power BI at the user's own risk. Outside this template's tools.

**T15-A145-9.** In the filter-listing measure DAX Studio generates, a variable caps how many filtered values are listed per column, three as generated; raise it to list more. Beyond the cap the text shows that many values and then the count of selected items.
- Option. 2019. https://www.sqlbi.com/articles/displaying-filter-context-in-power-bi-tooltips/
- When: Using a filter dump measure generated by DAX Studio.

**T15-A312-8.** On a chart built with helper measures, a default tooltip can show confusing helper values such as jitter numbers. Where a tooltip is wanted there, a report-page tooltip keeps those values out of sight.
- Should. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: Final clean-up of charts built with helper measures.
- Version: A report-page tooltip needs the visual's exception row in the brief.
