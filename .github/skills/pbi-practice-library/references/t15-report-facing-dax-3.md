# Report-facing DAX and report design

Part 3 of 4 of this topic. Covers: Conditional formatting and KPIs; Format strings in reports.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### Conditional formatting and KPIs

**T15-A188-3.** ALLSELECTED over one column, used as a table function, returns every value of the column unless the column is actively filtered. For the values visible in the current visual, evaluate VALUES of the column with `ALLSELECTED ()` as a modifier, for example inside CALCULATETABLE.
- Consider. 2020. https://www.sqlbi.com/articles/applying-color-banding-by-document-number-in-power-bi/
- When: A measure needs the values of a column shown in the visual, and the column may carry no explicit filter.

**T15-A188-4.** When RANKX ranks a column value, not a measure, pass the value to rank in its third argument, for example the current item read with SELECTEDVALUE. Without it RANKX evaluates the expression again in the outer context, where a column has no row context.
- Must. 2020. https://www.sqlbi.com/articles/applying-color-banding-by-document-number-in-power-bi/
- When: Ranking a column such as order numbers in a visual where each row shows exactly one item.

**T15-A188-6.** A conditional formatting rule meant to colour whole rows of a table must be applied to each displayed column, one by one: Power BI has no conditional formatting at row level.
- Must. Check. 2020. https://www.sqlbi.com/articles/applying-color-banding-by-document-number-in-power-bi/
- When: Background conditional formatting, such as banding by document, should cover full rows.
- Version: As of 2020; check the current product. Theme colours only (V009).

**T15-A189-4.** Small formatting measures tied to one layout, such as a min and max highlighter, are best defined as report measures in the one report they serve: their only purpose is to make that report easier to read.
- Should. 2020. https://www.sqlbi.com/articles/highlighting-the-minimum-and-maximum-values-in-a-power-bi-matrix/
- When: A measure exists only to format one visual of one report.
- Version: Here a report-level measure also takes the report prefix (V012).

**T15-A206-1.** A KPI's Status and Trend expressions must return what the client expects. Power BI: integers -2 to 2 (5 states) or -1 to 1 (3 states). Excel: a decimal from -1 to 1 (5 states); an integer in that range works for 3.
- Must. Check. 2020. https://www.sqlbi.com/articles/kpi-in-tabular-models-for-power-bi-and-excel/
- When: Defining the Status or Trend expression of a KPI in a tabular model.
- Version: Seen in 2020; check how current Power BI and Excel render KPI graphics.

**T15-A206-3.** Take care when choosing a KPI graphic with 5 states: Excel maps the states with decimal numbers and Power BI with integers, so the two clients render the same expression value differently.
- Consider. Check. 2020. https://www.sqlbi.com/articles/kpi-in-tabular-models-for-power-bi-and-excel/
- When: Choosing the Status or Trend graphic of a KPI that both clients may show.
- Version: Seen in 2020; check how current Power BI and Excel render KPI graphics.

**T15-A206-5.** When KPIs may be shown in both Power BI and Excel, keep Status and Trend graphics to three states and choose from Road Signs, Shapes, Traffic Light and Traffic Light - Single, which the two clients render the same way.
- Should. Check. 2020. https://www.sqlbi.com/articles/kpi-in-tabular-models-for-power-bi-and-excel/
- When: The model may be used from both clients, including a Power BI model reached through Analyze in Excel.
- Version: Seen in 2020; check how current Power BI and Excel render KPI graphics.

**T15-A206-6.** For KPIs seen in Excel as well as Power BI, prefer the Shapes graphic to Cylinder or Smiley Face: all three give the same output in both clients, and the name Shapes describes that output best.
- Should. Check. 2020. https://www.sqlbi.com/articles/kpi-in-tabular-models-for-power-bi-and-excel/
- When: The model's KPIs may be used from both Power BI and Excel.
- Version: Seen in 2020; check how current Power BI and Excel render KPI graphics.

**T15-A206-7.** For the Trend of a KPI used in Excel as well as Power BI, Standard Arrow is a possible graphic, provided only three states are used and its different rendering in Excel is acceptable.
- Option. Check. 2020. https://www.sqlbi.com/articles/kpi-in-tabular-models-for-power-bi-and-excel/
- When: The model's KPIs may be used from both Power BI and Excel.
- Version: Seen in 2020; check how current Power BI and Excel render KPI graphics.

**T15-A206-8.** KPI Status and Trend expressions should return whole numbers: for a result with a fractional part, such as 1.4, Power BI shows the raw number and not the icon.
- Should. Check. 2020. https://www.sqlbi.com/articles/kpi-in-tabular-models-for-power-bi-and-excel/
- When: The KPI is shown in Power BI, also in a model that serves Excel too.
- Version: Seen in 2020; check how current Power BI and Excel render KPI graphics.

**T15-A206-9.** For Power BI-only KPIs choose: 3-state Status from Traffic Light, Traffic Light - Single, Shapes, Road Signs, Three Stars Colored, Three Flags Colored, Three Symbols Uncircled Colored; 5-state Status from Five Bars Colored, Five Boxes Colored, both Gauge graphics; 5-state Trend: the Standard Arrow graphics.
- Should. Check. 2020. https://www.sqlbi.com/articles/kpi-in-tabular-models-for-power-bi-and-excel/
- When: Power BI alone displays the KPIs; integers from -1 to 1 (3 states) or -2 to 2 (5 states).
- Version: Seen in 2020; check how current Power BI and Excel render KPI graphics.

**T15-A206-10.** When only Power BI shows the KPIs, any 5-state graphic can serve as a 3-state one if the expression returns only -2, 0 or 2.
- Option. Check. 2020. https://www.sqlbi.com/articles/kpi-in-tabular-models-for-power-bi-and-excel/
- When: Power BI is the only client that displays the KPIs of a tabular model.
- Version: Seen in 2020; check how current Power BI and Excel render KPI graphics.

**T15-A206-11.** When only Excel shows the KPIs, pick Status from Road Signs, Shapes, Traffic Light or Traffic Light - Single (3 states), or the two Gauge graphics, Ascending and Descending (5); Trend from Variance Arrow (3), or Standard Arrow and its Ascending and Descending forms (5).
- Should. Check. 2020. https://www.sqlbi.com/articles/kpi-in-tabular-models-for-power-bi-and-excel/
- When: Excel alone displays the KPIs; the expression yields a decimal from -1 to 1.
- Version: Seen in 2020; check how current Power BI and Excel render KPI graphics.

**T15-A206-12.** When only Excel shows the KPIs, any 5-state graphic can serve as a 3-state one if the expression returns an integer between -1 and 1.
- Option. Check. 2020. https://www.sqlbi.com/articles/kpi-in-tabular-models-for-power-bi-and-excel/
- When: Excel is the only client that displays the KPIs of a tabular model.
- Version: Seen in 2020; check how current Power BI and Excel render KPI graphics.

**T15-A322-10.** Hold conditional formatting logic in measures that return a colour as text (a hex code, a CSS colour name or RGBA) and reuse them across visuals, so one change reaches every use; static styles stay in the theme.
- Should. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/ ; https://www.sqlbi.com/articles/highlighting-the-minimum-and-maximum-values-in-a-power-bi-matrix/
- When: The same conditional formatting is needed in several visuals, pages or reports.
- Version: Theme colours only; a colour code needs an exception row (V009). A 2020 view required a numeric result.

**T15-A322-15.** Keep measures used only for report formatting apart from the rest: a display folder (or, possibly, a table of their own), names that show the purpose, and a description of how to use each, its condition, its colours and any theme colour it reads.
- Must. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: A model holds measures used for conditional formatting.
- Version: Measures stay in the one measures table; a separate table (M001) or new folder type (M004) needs an exception row.

### Format strings in reports

**T15-A276-1.** The DAX expression behind a measure's dynamic format string must always return a valid format string, whatever filter context or measure value it reacts to.
- Must. Check. 2023. https://www.sqlbi.com/articles/introducing-dynamic-format-strings-for-dax-measures/
- When: A measure whose format string is dynamic.
- Version: A preview feature in 2023; this template now lists dynamic format strings as generally available.

**T15-A276-5.** Keep dynamic format string expressions simple so they evaluate fast. Each one adds to the query Power BI sends; the cost grows when the expression calls other measures or reads the current measure through SELECTEDMEASURE.
- Should. 2023. https://www.sqlbi.com/articles/introducing-dynamic-format-strings-for-dax-measures/
- When: Writing the expression of a dynamic format string.

**T15-A276-10.** Never reuse one measure's dynamic format string expression by referring to it from another measure or from another measure's format string expression. SELECTEDMEASURE inside it still means the original measure, so the borrower is formatted from the wrong value.
- Must. 2023. https://www.sqlbi.com/articles/introducing-dynamic-format-strings-for-dax-measures/
- When: Measures with dynamic format strings.
- Version: To share format logic, this template points to a user-defined function instead.

**T15-A296-1.** Changing the display format of a measure or column leaves the stored data as it is. To really lower precision or model size, transform the data in Power Query or in an upstream ETL tool.
- Must. 2024. https://www.sqlbi.com/articles/improving-data-labels-with-format-strings/
- When: Fewer decimals are wanted to shrink a model or reduce precision.

**T15-A296-2.** When the formats offered in the Power BI Desktop ribbon are not enough, write a custom format string. Examples: a duration as minutes and seconds, a unit suffix, a custom date style, or several currencies in one measure.
- Must. 2024. https://www.sqlbi.com/articles/improving-data-labels-with-format-strings/
- When: Value formatting beyond the ribbon's built-in choices.

**T15-A296-3.** Enclose any literal text or symbol in a custom or dynamic format string in double quotes. In a format string expression, concatenate an escaped double quote (four double-quote characters) before and after the text. Unquoted characters such as `#`, `0` and `m` act as placeholders.
- Must. 2024. https://www.sqlbi.com/articles/improving-data-labels-with-format-strings/
- When: Adding words, letters or suffixes to a format string; a likely cause of strange dynamic format results.

**T15-A296-4.** Take into account that the limits of dynamic format strings, on measures and in calculation groups alike, weigh most when the model is read from client tools other than Power BI Desktop.
- Consider. 2024. https://www.sqlbi.com/articles/improving-data-labels-with-format-strings/
- When: Deciding whether to use a dynamic format string in a model other tools consume.

**T15-A296-6.** Symbols in a measure's format string can make data labels easier to read: currency symbols for different currencies, arrows for trend or performance against target, coloured symbols or emojis that signal good or bad, and function hints such as a link icon beside a URL.
- Option. 2024. https://www.sqlbi.com/articles/improving-data-labels-with-format-strings/
- When: Data labels for comparison and achievement calculations above all.

**T15-A296-7.** Words or letters in a measure's format string can make numbers clearer or shorter: a unit of measure such as pieces or millimetres, a clarifying prefix or suffix such as previous year or month to date, or a rounding suffix such as K or M.
- Option. 2024. https://www.sqlbi.com/articles/improving-data-labels-with-format-strings/
- When: Labels need a unit, a period marker or a rounding scale.

**T15-A296-11.** Watch performance when measures use dynamic format strings: time how long the format strings take, and compare query times with and without them. The risk is highest in visuals with many data points and in complex models.
- Should. Check. 2023. https://www.sqlbi.com/articles/introducing-dynamic-format-strings-for-dax-measures/ ; https://www.sqlbi.com/articles/improving-data-labels-with-format-strings/
- When: Models whose measures use dynamic format strings.
- Version: Part of this advice dates from the 2023 preview; check current behaviour.

**T15-A296-12.** Isolate format strings and format string expressions made for one report or visual, so that people building their own reports, pivot tables or analyses on the model cannot easily see or use them. No single way fits every model.
- Should. 2024. https://www.sqlbi.com/articles/improving-data-labels-with-format-strings/
- When: A format string is tailored to one report or visual.

## Special-case techniques and facts

### Conditional formatting and KPIs

**T15-A188-1.** A table can switch its row colour each time a document number, such as an order number, changes: use background conditional formatting driven by a measure that alternates between two values from one document to the next. The built-in alternating-row style cannot do this.
- Option. 2020. https://www.sqlbi.com/articles/applying-color-banding-by-document-number-in-power-bi/
- When: All lines of one document should share a background colour so readers can tell documents apart.
- Version: Colours must be theme colours; a colour code needs an exception row in the brief (V009).

**T15-A188-2.** For the two-value band, rank the visible documents by number with RANKX, which grows by one per document, and take the rank modulo 2 with MOD. Parity of the raw document number is not enough: two consecutive visible documents may both be even.
- Option. Check. 2020. https://www.sqlbi.com/articles/applying-color-banding-by-document-number-in-power-bi/
- When: Writing the measure behind row banding by document number.
- Version: Stated in 2020; check current behaviour.

**T15-A189-1.** To highlight the largest and smallest cells of a matrix, drive background conditional formatting with a measure that rebuilds every cell in a temporary table under ALLSELECTED, takes MINX and MAXX, and returns one code for the minimum, another for the maximum, blank otherwise.
- Option. 2020. https://www.sqlbi.com/articles/highlighting-the-minimum-and-maximum-values-in-a-power-bi-matrix/
- When: A matrix full of numbers should point out its best and worst combinations.
- Version: Colours must be theme colours; a colour code needs an exception row in the brief (V009).

**T15-A189-3.** A formatting measure that rebuilds the values of a matrix is tied to that matrix's layout: when a user swaps an attribute on rows or columns, for example continent for year, the formatting stops working or gives unexpected results.
- Fact. 2020. https://www.sqlbi.com/articles/highlighting-the-minimum-and-maximum-values-in-a-power-bi-matrix/
- When: A formatting measure recomputes the matrix result, as in min and max highlighting.

**T15-A189-5.** A measure that flags cells and drives background conditional formatting can also highlight cells by other business rules, such as large transactions behind an aggregated value, or a gap from a reference value beyond a set threshold.
- Option. 2020. https://www.sqlbi.com/articles/highlighting-the-minimum-and-maximum-values-in-a-power-bi-matrix/
- When: Report cells should be highlighted according to a business rule.
- Version: Colours must be theme colours; a colour code needs an exception row in the brief (V009).

**T15-A189-6.** To find the minimum and maximum inside each group and not across the whole matrix, limit the ALLSELECTED modifier of the measure to the tables or columns whose filters should go, for example ALLSELECTED over the product table for the extremes of each continent.
- Option. 2020. https://www.sqlbi.com/articles/highlighting-the-minimum-and-maximum-values-in-a-power-bi-matrix/
- When: Min and max highlighting should be evaluated per group of a matrix.

**T15-A206-2.** The names of the KPI graphic options do not always describe the icons shown: Thermometer and Smiley Face, for instance, look different from what their names suggest, in Power BI and in Excel.
- Fact. Check. 2020. https://www.sqlbi.com/articles/kpi-in-tabular-models-for-power-bi-and-excel/
- When: Choosing the Status or Trend graphic of a KPI in a tabular model.
- Version: Seen in 2020; check how current Power BI and Excel render KPI graphics.

**T15-A206-4.** Power BI shows only the number for an unrecognised KPI value or graphic. Excel uses a default graphic (Traffic Light - Single for Status, Status Arrow - Ascending for Trend), the icon of 1 above 1, nothing below -1, a blank icon at -2.
- Fact. Check. 2020. https://www.sqlbi.com/articles/kpi-in-tabular-models-for-power-bi-and-excel/
- When: A tabular model's KPIs are shown in Power BI, Excel or both.
- Version: Seen in 2020; check how current Power BI and Excel render KPI graphics.

**T15-A206-13.** The Status Description and Trend Description properties of a tabular KPI are not used by the Excel and Power BI clients.
- Fact. Check. 2020. https://www.sqlbi.com/articles/kpi-in-tabular-models-for-power-bi-and-excel/
- When: Filling in the properties of a KPI in a tabular model.
- Version: Seen in 2020; check how current Power BI and Excel render KPI graphics.

**T15-A300-7.** Points that need attention in a scatterplot can be flagged by conditional formatting driven by a measure, for example a Pareto cumulative percentage of the shortfall that colours the biggest contributors. Statistical methods such as clustering with PCA or t-SNE are another way.
- Option. 2024. https://www.sqlbi.com/articles/using-scatterplots-to-find-details-in-reports/
- When: Readers should find the important points first; the rule's threshold can be tightened or relaxed.
- Version: Theme colours only; a colour code needs an exception row (V009).

**T15-A312-5.** A selected item can be highlighted while others stay visible: group the visual by a disconnected calculated table of item names, tied to facts with TREATAS. A calculation group in the legend has a 'selected' item applying the slicer and an 'all' item; colour 'selected'.
- Option. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: A slicer on the grouping column would remove the other items from the visual.
- Version: Theme colours only (V009); the disconnected calculated table needs its reason line and exception row (M105, M411).

**T15-A312-6.** A conditional-formatting measure that returns a highlight colour is a simpler alternative to the calculation group for a selected point. It works in conditional formatting only and gives no control over drawing order or marker shape, so the highlighted point can vanish inside a cluster.
- Option. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: Highlighting a selected data point among all others in a chart.
- Version: Theme colours only; a colour code needs an exception row (V009).

**T15-A312-7.** Optionally give the 'selected' calculation item a higher ordinal than the 'all' item, so the highlighted point is drawn on top.
- Option. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: A calculation group in a chart's legend highlights a selected item against all items.

**T15-A318-7.** Before adding arbitrary qualitative ranges to a bullet chart, agree them with the users; otherwise they may not understand or accept the ranges.
- Should. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: Bullet charts where no data for qualitative ranges exists and the ranges would be invented.

**T15-A322-11.** Bind a colour-returning measure to a visual property with the Field value format style of the conditional formatting dialog; Power BI Desktop calls the measure a field in that option.
- Must. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: A measure that returns a colour drives conditional formatting.
- Version: Theme colours only; a colour code needs an exception row (V009).

**T15-A362-1.** When each level of a hierarchy needs its own formatting calculation, the formatting expression must first find the level of the current cell and then apply that level's logic; it can be a model measure or a visual calculation.
- Must. 2026. https://www.sqlbi.com/articles/dynamic-formatting-by-hierarchy-level-with-isinscope-and-isatlevel/
- When: Conditional formatting follows a different rule at each hierarchy level.

**T15-A362-2.** In a measure that picks a per-level rule with ISINSCOPE inside `SWITCH ( TRUE (), ... )`, order the tests from the most detailed level to the least detailed: at a lower level ISINSCOPE is also TRUE for every higher-level column.
- Should. 2026. https://www.sqlbi.com/articles/dynamic-formatting-by-hierarchy-level-with-isinscope-and-isatlevel/
- When: A measure branches on the current hierarchy level, as in per-level formatting of a matrix.

**T15-A362-3.** When the model has several columns for one hierarchy level, such as a full and a short month name, the ISINSCOPE test for that level can check each of them, so the branch fires whichever column the visual uses.
- Option. 2026. https://www.sqlbi.com/articles/dynamic-formatting-by-hierarchy-level-with-isinscope-and-isatlevel/
- When: A per-level measure where one level exists as alternative columns.

**T15-A362-4.** In a per-level formatting measure, ALLSELECTED can replace REMOVEFILTERS when the comparison with a grand total or an average should cover only the period the visual shows; REMOVEFILTERS compares with the whole model and ignores date slicers.
- Option. 2026. https://www.sqlbi.com/articles/dynamic-formatting-by-hierarchy-level-with-isinscope-and-isatlevel/
- When: The comparison should follow the selected time range.

**T15-A362-5.** A visual calculation for per-level formatting and a like measure that clears date filters with REMOVEFILTERS differ once dates are filtered outside the visual: the visual calculation sees only the periods shown, the measure still compares with the whole model.
- Fact. 2026. https://www.sqlbi.com/articles/dynamic-formatting-by-hierarchy-level-with-isinscope-and-isatlevel/
- When: Choosing between a measure and a visual calculation while outside filters keep only some periods.

**T15-A362-6.** In a visual calculation, mind that the argument of ISATLEVEL refers to the column under the name it has inside the visual, not to a model table and column; that name depends on how the hierarchy is set up in the visual.
- Consider. 2026. https://www.sqlbi.com/articles/dynamic-formatting-by-hierarchy-level-with-isinscope-and-isatlevel/
- When: A visual calculation detects the current level, as in per-level formatting of a matrix.

**T15-A362-7.** In a per-level visual calculation, the total of a higher level, such as the year total on a month row, can come from COLLAPSE and the grand total from COLLAPSEALL; both climb the visual's own hierarchy and do not work on the model.
- Option. 2026. https://www.sqlbi.com/articles/dynamic-formatting-by-hierarchy-level-with-isinscope-and-isatlevel/
- When: A visual calculation needs a higher-level total or the grand total.

**T15-A362-8.** When a visual calculation needs measures the visual does not show, add them to the visual as hidden fields: only fields placed in the visual are available to it.
- Must. 2026. https://www.sqlbi.com/articles/dynamic-formatting-by-hierarchy-level-with-isinscope-and-isatlevel/ ; https://www.sqlbi.com/articles/show-transaction-details-on-the-matrix-visual-in-power-bi/
- When: A visual calculation computes from measures not otherwise shown.
- Version: Earlier 2026 guidance said a table visual cannot hide such columns (zero width as workaround); check the current product.

**T15-A362-9.** Detect the hierarchy level in a model measure with ISINSCOPE when you own the semantic model and want the logic reused in several reports and visuals; creating it needs model authoring rights. A visual calculation may still suit presentation-only logic and is usually faster.
- Should. 2026. https://www.sqlbi.com/articles/dynamic-formatting-by-hierarchy-level-with-isinscope-and-isatlevel/
- When: Per-level formatting, with a model owner who wants reuse.

**T15-A362-10.** Write per-level formatting logic as a model measure with ISINSCOPE, not as a visual calculation, whenever it depends on data the visual does not hold: a visual calculation reaches nothing beyond the visual's own content.
- Must. 2026. https://www.sqlbi.com/articles/dynamic-formatting-by-hierarchy-level-with-isinscope-and-isatlevel/
- When: Per-level formatting needs model data that is not in the visual.

**T15-A362-11.** Detect the level in a visual calculation with ISATLEVEL when you cannot, or prefer not to, change the semantic model, as with a shared model another team owns: the calculation stays in the report and needs no extra rights.
- Should. 2026. https://www.sqlbi.com/articles/dynamic-formatting-by-hierarchy-level-with-isinscope-and-isatlevel/
- When: No rights to add measures; not when the logic needs data absent from the visual.

**T15-A362-13.** For speed, prefer a visual calculation to a model measure for per-level formatting logic as the usual choice: it works on the few rows that fill the visual, while a measure may trigger extra internal queries.
- Should. 2026. https://www.sqlbi.com/articles/dynamic-formatting-by-hierarchy-level-with-isinscope-and-isatlevel/
- When: Either form can do the job; a measure is required when the logic needs data not in the visual.

**T15-A362-14.** In a per-level formatting measure, a month cell can get its year total by clearing the filters of the date table while keeping the current year through VALUES (the REMOVEFILTERS with VALUES pattern); grand total and all-quarter average come after clearing the date filters.
- Option. 2026. https://www.sqlbi.com/articles/dynamic-formatting-by-hierarchy-level-with-isinscope-and-isatlevel/
- When: ISINSCOPE branches of a date hierarchy compare with a higher-level total or an average.

### Format strings in reports

**T15-A276-3.** To keep one unit (K, M and so on) in every cell of a visual, a dynamic format string can pick the unit from the measure's value at the total of the current selection, through CALCULATE with ALLSELECTED, and use it for rows and total.
- Option. 2023. https://www.sqlbi.com/articles/introducing-dynamic-format-strings-for-dax-measures/
- When: Rows and totals of one visual would otherwise show mixed units.

**T15-A276-4.** Report-level measures of a live-connected report run as query measures that hold DAX code only. A dynamic format string is stored in the model as a property of the measure, which a query measure lacks.
- Fact. 2023. https://www.sqlbi.com/articles/introducing-dynamic-format-strings-for-dax-measures/
- When: A report with a live connection to a remote model needs a dynamic format.

**T15-A276-6.** When a dynamic format string calls SELECTEDMEASURE, the measure's storage engine work is shared, but its formula engine work runs at least two times: one pass yields the value, another the format. For a measure heavy on formula engine work this is costly.
- Fact. Check. 2023. https://www.sqlbi.com/articles/introducing-dynamic-format-strings-for-dax-measures/
- When: A dynamic format string expression that references SELECTEDMEASURE.
- Version: Measured in 2023 while the feature was in preview; check current behaviour.

**T15-A276-8.** The result or speed of a dynamic format string can be debugged by querying the internal measure that computes it. Its name is the measure's name with an underscore in front and a space plus FormatString behind; reference it with its table name.
- Option. 2023. https://www.sqlbi.com/articles/introducing-dynamic-format-strings-for-dax-measures/
- When: A dynamic format string shows a wrong format or slows a query.
- Version: Uses the query from Performance Analyzer.

**T15-A276-9.** A measure name built from an underscore, another measure's name, a space and FormatString is reserved for internal format string measures. Power BI raises an error when a measure is created with such a name.
- Fact. 2023. https://www.sqlbi.com/articles/introducing-dynamic-format-strings-for-dax-measures/
- When: Naming measures in a model.

**T15-A276-11.** Inside a DAX query, a measure's format string expression can be expressed as a query measure. In that form it cannot call SELECTEDMEASURE; the rewritten expression names the measure itself in its place.
- Fact. 2023. https://www.sqlbi.com/articles/introducing-dynamic-format-strings-for-dax-measures/
- When: Testing a dynamic format string in a DAX query.

**T15-A276-12.** The hidden internal measure that computes a dynamic format string can be referenced in DAX only with its table name in front. Expect such table-qualified measure references in queries Power BI generates, not in hand-written formulas.
- Fact. 2023. https://www.sqlbi.com/articles/introducing-dynamic-format-strings-for-dax-measures/
- When: Referencing the internal format string measure (underscore prefix, FormatString suffix) from DAX.

**T15-A296-5.** A symbol in a dynamic format string can be produced with UNICHAR instead of pasting the character; UNICODE returns the code number of a given symbol. UNICHAR is the safer route when a text editor may not handle the pasted character.
- Option. 2024. https://www.sqlbi.com/articles/improving-data-labels-with-format-strings/
- When: Adding symbols to a dynamic format string expression.

**T15-A296-8.** When a format string expression embeds other numbers or measure values, first turn each into formatted text, for example with FORMAT, and then also wrap it in escaped double quotes. Unquoted, a leading zero triggers digit substitution and rounds the value.
- Must. 2024. https://www.sqlbi.com/articles/improving-data-labels-with-format-strings/
- When: A label combines separately computed parts, such as a percentage after a delta.

**T15-A296-9.** FORMAT with the pattern `"nn:ss"` on a duration held in days shows minutes and seconds only: 61:28 appears as 01:28. To show total minutes, format the whole minutes, cut with TRUNC, with a two-digit pattern, and use the time pattern for the seconds only.
- Fact. 2024. https://www.sqlbi.com/articles/improving-data-labels-with-format-strings/
- When: Durations must show total minutes above 60, as video players do.

**T15-A296-10.** A format string never changes how a measure sorts: sorting uses the underlying number, not the displayed text. A duration held as one number and shown as hours, minutes and seconds still sorts correctly; a wrongly formatted value sorts by its real number.
- Fact. 2024. https://www.sqlbi.com/articles/improving-data-labels-with-format-strings/
- When: Sorting a visual by a measure with a custom or dynamic format string.

**T15-A296-13.** A thin report, connected to a separate semantic model, cannot define format strings or format string expressions for the model's measures. Formatting there is limited to the visual's own formatting pane for labels and values.
- Fact. Check. 2024. https://www.sqlbi.com/articles/improving-data-labels-with-format-strings/
- When: A report connected to an external semantic model needs its own number formats.
- Version: Stated in 2024; a format string on one visual now exists as a preview needing the developer's yes (V022).
