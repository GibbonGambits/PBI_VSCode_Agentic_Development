# Report-facing DAX and report design

Part 1 of 4 of this topic. Covers: Slicers and measure filters; Report design and requirements; Measures written for visuals.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### Slicers and measure filters

**T15-A325-22.** A whole-table filter in CALCULATE can also bring side effects, because its filter spreads through the expanded table. A table filter may still be needed for some optimisations or features that cannot be reached another way.
- Should. 2018. https://www.sqlbi.com/articles/using-or-conditions-between-slicers-in-dax/ ; https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: Deciding whether a measure may filter a table instead of columns, as in OR logic between slicers.

### Report design and requirements

**T15-A072-10.** When no visual property meets a report requirement, look for the answer in every layer of the tool: queries, data model and DAX, not only in the visual's settings.
- Should. 2016. https://www.sqlbi.com/articles/the-space-report-under-the-hood/
- When: A report requirement cannot be met by configuring a visual.
- Version: Written for 2016 Power BI.

**T15-A325-12.** When users insist on a pie chart, a short talk to learn their view and offer an alternative is one approach; if they still prefer the pie, accepting it is reasonable, and the talk may show it fits best.
- Option. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: Users ask for, or prefer, a pie chart.

**T15-A325-16.** Treat a guideline such as avoiding pie charts as a summary of deeper principles: know why it exists and when a deviation is justified, and do not apply it mechanically. Beginners can start from the simple rules.
- Must. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: Applying any chart or report design guideline.

**T15-A325-20.** In most reports, lay the page out by the 3-30-300 hierarchy: an overview of the key questions in about 3 seconds, filtering and zooming in about 30, details on demand in about 300. The times are illustrations; exploratory dashboards and paginated reports may differ.
- Should. 2024. https://www.sqlbi.com/articles/introducing-the-3-30-300-rule-for-better-reports/ ; https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: Reports whose aim is a short time to insight.

**T15-A308-2.** Usefulness is a report's first goal. Its design and looks must never reduce how well readers find their answers: a more attractive report can still make basic information slower to find.
- Should. 2024. https://www.sqlbi.com/articles/introducing-the-3-30-300-rule-for-better-reports/
- When: Weighing appearance against function in report design.

**T15-A308-4.** For requirements, research what existing reports show and speak with the business users yourself, in informal, interactive meetings, and let their input drive the choice of charts, formatting and content. Other approaches can be equally valid.
- Should. 2024. https://www.sqlbi.com/articles/introducing-the-3-30-300-rule-for-better-reports/
- When: Gathering requirements for a report.

**T15-A308-5.** Keep the 3-second overview concise: simple visuals such as cards or line charts near the top-left, along the top or the left, with pre-attentive cues (colour, arrow symbols, trend lines, bar lengths) and clear numbers. Avoid many visuals and labels; keep slicers, buttons, logos elsewhere.
- Should. 2024. https://www.sqlbi.com/articles/introducing-the-3-30-300-rule-for-better-reports/
- When: The overview that answers readers' most important questions at a glance.
- Version: Here the page title takes the top-left corner (layout standard) and colours come from the theme.

**T15-A308-6.** The 30-second filter-and-zoom area guides readers to the categories that matter: consistent, limited chart formatting, readable titles, axes and labels, conditional formatting on categories readers are likely to filter, and user training in cross-filtering and drilldown. Avoid too many visuals, interactions and redundant information.
- Should. 2024. https://www.sqlbi.com/articles/introducing-the-3-30-300-rule-for-better-reports/
- When: The part of a report where readers filter and zoom to areas they may act on.
- Version: Theme colours only; a colour code needs an exception row (V009).

**T15-A308-7.** The 300-second details area surfaces the key details for the filtered areas and is no raw data dump. Keep tables concise with few categories and values, let drillthrough pass only needed filters, link to supplemental information, and never build pages meant only for export.
- Should. 2024. https://www.sqlbi.com/articles/introducing-the-3-30-300-rule-for-better-reports/
- When: The details-on-demand part of a report, reached after overview and filtering.

**T15-A308-8.** Connect the filter step and the details step of a report, so readers need not rebuild their filters or search again for what they had found. End the flow as close as feasible to the actions readers take.
- Should. 2024. https://www.sqlbi.com/articles/introducing-the-3-30-300-rule-for-better-reports/
- When: Linking summary views to detail views or to other reports.

**T15-A308-9.** The 3-30-300 structure also works across report pages, reports or a Power BI app: overview views lead to more interactive and detailed ones, and cross-report drillthrough lets readers zoom into specific categories.
- Option. 2024. https://www.sqlbi.com/articles/introducing-the-3-30-300-rule-for-better-reports/
- When: Structuring several pages or reports for one audience.

**T15-A308-10.** Do not design a report to answer every possible question. Tailor it to a set of key questions, so that a target audience can decide and act quickly.
- Should. 2024. https://www.sqlbi.com/articles/introducing-the-3-30-300-rule-for-better-reports/
- When: Scoping a report.

**T15-A308-12.** In requirements meetings, aim to understand: the business process the report supports, the outcomes wanted, who the users are and their responsibilities, the decisions and actions they take, the questions they must answer, and the data needed as measures and dimensions.
- Should. 2024. https://www.sqlbi.com/articles/introducing-the-3-30-300-rule-for-better-reports/
- When: Gathering requirements before designing a report.

**T15-A328-1.** Before designing, creating, changing or migrating a model or report, first understand the business process it reports on. Before designing a report, also pin down the data questions its users are trying to answer.
- Must. 2024. https://www.sqlbi.com/articles/introducing-the-3-30-300-rule-for-better-reports/ ; https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: The start of any model or report work.

**T15-A328-20.** Design a chart step by step together with its users while requirements are gathered, starting from a simple wireframe or a more refined mock-up.
- Should. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Requirements for a new chart or visual are being gathered.

**T15-A318-1.** Give report visuals enough context to interpret the numbers, most often by comparing actual values with a target: a budget, a forecast, an earlier period, or an average or median per category.
- Should. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: Any visual that shows a number readers must judge.

**T15-A318-3.** The difference between actual and target can be shown as a percentage or as an amount, chosen by the report's purpose: the percentage shows which category does worst against its own target, the amount shows which categories move the overall result most.
- Option. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: Visualising variance between actuals and a target by category.

**T15-A318-5.** Avoid packing every measure and target into one huge table or matrix to supply context: such tables overwhelm readers, who lose time searching through the numbers.
- Should. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: Reports where many categories, measures and targets need context.

**T15-A318-6.** Gather good requirements to decide which context a report shows, from the business problems and questions it must address and the information people need for their work. Showing everything is inefficient; a single measure can omit what some need.
- Should. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: Deciding which comparisons and targets a report shows.

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

## Special-case techniques and facts

### Slicers and measure filters

**T15-A067-1.** To count only the customers who bought in every category picked in one slicer, group sales by customer and category, keep the customers whose category count equals the number of categories selected, and pass that customer table to CALCULATE as a filter.
- Must. 2015. https://www.sqlbi.com/articles/apply-and-logic-to-multiple-selection-in-dax-slicer/
- When: A measure needs AND logic across the items of one slicer; keep the customer key in the filter table.

**T15-A067-2.** When the wanted result is only the number of such customers, COUNTROWS over the filtered customer table gives it directly, with no measure evaluated through CALCULATE.
- Option. 2015. https://www.sqlbi.com/articles/apply-and-logic-to-multiple-selection-in-dax-slicer/
- When: AND logic across one slicer's items, and only the customer count is asked for.

**T15-A067-3.** AND logic across the items of a slicer is written measure by measure and needs a named entity, such as a customer table, to carry the filter. No single generic calculation applies it to every slicer and every existing measure.
- Fact. 2015. https://www.sqlbi.com/articles/apply-and-logic-to-multiple-selection-in-dax-slicer/
- When: Planning AND logic for slicer selections.

**T15-A067-4.** The filter logic for 'all selected items' can sit in a calculation item, so that one given slicer and one filtered entity get the same treatment under any existing measure.
- Option. 2015. https://www.sqlbi.com/articles/apply-and-logic-to-multiple-selection-in-dax-slicer/
- When: Several measures need the same AND logic for one specific slicer and entity.

**T15-A125-1.** Items picked inside one slicer combine as OR; separate slicers combine as AND when they filter standard measures. A measure can take control of the filter context so that the selections of two slicers act as OR.
- Fact. 2018. https://www.sqlbi.com/articles/using-or-conditions-between-slicers-in-dax/
- When: Slicers in Power BI reports and Excel PivotTables; OR between slicers is needed only in specific cases.

**T15-A125-2.** For OR between two slicers, give CALCULATE one filter over the two sliced columns together. Two variants exist, one built from crossjoins and one that scans the fact data; choose by how the data is distributed.
- Should. 2018. https://www.sqlbi.com/articles/using-or-conditions-between-slicers-in-dax/
- When: A measure must show data that matches the selection of either of two slicers.

**T15-A125-3.** One OR filter for two slicers is the union of two crossjoins: the selected values of the first column with all values of the second, plus all values of the first with the selected values of the second. It is usually the faster variant.
- Option. 2018. https://www.sqlbi.com/articles/using-or-conditions-between-slicers-in-dax/
- When: Neither slicer has hundreds or more distinct values; the filter may hold pairs that never occur in the data.

**T15-A125-4.** Another OR filter for two slicers reads the combinations of the two columns that exist in the table the measure aggregates and keeps those matching either selection. It returns only existing pairs, usually costs more, and may win when both slicers have many values.
- Option. 2018. https://www.sqlbi.com/articles/using-or-conditions-between-slicers-in-dax/
- When: The table the measure aggregates is known; slicers with hundreds or more distinct values.

**T15-A125-7.** OR between slicers cannot be written once for every slicer of a report: it goes into measures for specific reports, where the slicers to combine are known in advance.
- Fact. 2018. https://www.sqlbi.com/articles/using-or-conditions-between-slicers-in-dax/
- When: Planning OR logic between slicers.

**T15-A131-1.** In a Power BI report a measure can act as a filter only in the filter section of a visual; page and report filters take columns only. A measure filter needs a target granularity, which only a visual's columns supply.
- Fact. Check. 2018. https://www.sqlbi.com/articles/applying-a-measure-filter-in-power-bi/
- When: Deciding where a filter on a measure value can go.
- Version: As observed in 2018; check the current product.

**T15-A131-2.** In a matrix, a filter on a measure is evaluated for each combination of the attributes on Rows, including levels hidden by drilling up. Attributes on Columns play no part in that granularity.
- Fact. 2018. https://www.sqlbi.com/articles/applying-a-measure-filter-in-power-bi/
- When: A matrix visual has a measure among its visual-level filters.

**T15-A131-4.** Changing the visual type while a measure filter is active can give unexpected results: each type may set the granularity of the filter by its own criteria, and a matrix and a chart do not do it alike.
- Fact. 2018. https://www.sqlbi.com/articles/applying-a-measure-filter-in-power-bi/
- When: A visual with a measure in its visual-level filters is switched to another type.

**T15-A131-5.** Without any DAX, an author can set the granularity of a visual-level measure filter by adding attributes that are not displayed, for example an extra attribute on matrix rows. The visual then filters an entity it does not show.
- Option. 2018. https://www.sqlbi.com/articles/applying-a-measure-filter-in-power-bi/
- When: Filtering by a measure at a granularity other than the one shown; the side effects must be understood.

**T15-A131-6.** When a visual-level measure filter works at another granularity than the visual shows, a complex displayed measure can return unexpected values: a year-to-date total that does not grow month after month, or a December value that differs from the year's.
- Fact. 2018. https://www.sqlbi.com/articles/applying-a-measure-filter-in-power-bi/
- When: A visual shows a measure such as year-to-date while a measure filter acts at another granularity.

**T15-A131-7.** Consider a separate measure meant only for the filter section, which computes at the granularity the filter needs, for example ignoring the month level to test a yearly amount. The displayed measure is then not reused as the filter.
- Consider. 2018. https://www.sqlbi.com/articles/applying-a-measure-filter-in-power-bi/
- When: A measure filter must act at another granularity than shown, such as yearly amounts under a monthly year-to-date.

**T15-A131-8.** Putting the filter logic into the displayed measure also avoids surprises from a visual-level measure filter that acts at another granularity than the one shown. The complexity then lives in DAX only, which helps people who build reports without knowing that behaviour.
- Consider. 2018. https://www.sqlbi.com/articles/applying-a-measure-filter-in-power-bi/
- When: A measure filter would need a granularity different from the one the visual shows.

**T15-A145-5.** In a chart, a visual-level filter on a measure is evaluated at the combined granularity of all attributes in Axis and Legend, including levels not shown; drilling up does not change it. A higher-level point therefore sums only the detail items that pass.
- Fact. 2018. https://www.sqlbi.com/articles/applying-a-measure-filter-in-power-bi/ ; https://www.sqlbi.com/articles/displaying-filter-context-in-power-bi-tooltips/
- When: Any visual with a measure condition in its visual-level filters; a line chart by month is one example.

**T15-A166-1.** One slicer can list values from several columns of a table (state, country, continent) through a separate calculated table: stack the columns with UNION and SELECTCOLUMNS, apply DISTINCT, pair each shown item with every key it must filter, and relate it to the table's key.
- Option. 2019. https://www.sqlbi.com/articles/creating-a-slicer-that-filters-multiple-columns-in-power-bi/
- When: Readers must filter alternative values held in different columns of one table through a single slicer.

**T15-A166-3.** In the one-slicer-over-several-columns pattern, relate the slicer table to the source table on their shared key with a many-to-many cardinality relationship whose filter flows one way only, from the slicer table to the source table.
- Must. 2019. https://www.sqlbi.com/articles/creating-a-slicer-that-filters-multiple-columns-in-power-bi/
- When: Keys with a few hundred unique values; with thousands, consider an intermediate table of distinct keys and regular relationships.
- Version: A many-to-many relationship is listed with its reason as an exception (M406).

**T15-A166-4.** Once a relationship of many-to-many cardinality takes part in a visual, measures stop being additive: an item that belongs to several rows shows in each of them, while the total counts it once, so the total differs from the sum of the visible rows.
- Fact. 2019. https://www.sqlbi.com/articles/creating-a-slicer-that-filters-multiple-columns-in-power-bi/
- When: Any visual in which a many-to-many cardinality relationship takes part, such as a multi-column slicer table on matrix rows.

**T15-A229-1.** A measure used only as a visual filter, not among the visual's values, can be computed differently and give wrong results: the generated query evaluates it only over combinations where the displayed measures are not blank, which can shrink the filter ALLSELECTED restores inside it.
- Fact. Check. 2021. https://www.sqlbi.com/articles/deep-dive-into-measure-filters-in-power-bi-desktop/
- When: Rare: an unusual mix of columns in the visual and a filter-only measure that uses ALLSELECTED.
- Version: Seen in 2021; depends on the query Power BI generates, so check the current product.

**T15-A229-2.** When a measure used only as a visual filter gives wrong results, analyse the report's measures and the query Power BI generates in depth, and choose a fix for that case: no clean, generic remedy exists.
- Must. Check. 2021. https://www.sqlbi.com/articles/deep-dive-into-measure-filters-in-power-bi-desktop/
- When: A filter-only measure gives other results than when it is also displayed.
- Version: Seen in 2021; check the current product.

**T15-A229-3.** Workarounds for a filter-only measure that relies on ALLSELECTED, each with a cost: use REMOVEFILTERS in its place (no longer dynamic); make the displayed measure return zero for blank (zeros appear); or add the filtering measure to the values in a zero-width column (extra formatting).
- Option. Check. 2021. https://www.sqlbi.com/articles/deep-dive-into-measure-filters-in-power-bi-desktop/
- When: A measure used only in a visual's Filter pane is computed over a reduced set of combinations.
- Version: Seen in 2021. The zero variant needs the brief's exception to the blank rule (M506).

**T15-A308-13.** When readers compare results against several targets, such as forecast or prior year, the target can be made switchable, for example with navigation buttons, calculation groups or field parameters.
- Option. 2024. https://www.sqlbi.com/articles/introducing-the-3-30-300-rule-for-better-reports/
- When: Readers want more than one target for the same measure.

**T15-A359-1.** A slicer cannot filter a measure. Filters always apply to columns; a measure acts as a filter only once a granularity is defined, that is the column over which the measure is evaluated.
- Fact. 2026. https://www.sqlbi.com/articles/filtering-measures-through-slicers/
- When: A request to slice or filter by a measure value.

**T15-A359-2.** A filter on a measure in a visual's filter pane is evaluated at the granularity of the column the visual groups by; changing that column changes which rows pass, and the visual's total with them.
- Fact. 2026. https://www.sqlbi.com/articles/filtering-measures-through-slicers/
- When: A visual-level filter tests a measure value.

**T15-A359-3.** To serve a request to slice by a measure value, define explicitly the business entity, such as product, customer or store, whose measure value is tested; the slicer only sets parameters such as the threshold.
- Must. 2026. https://www.sqlbi.com/articles/filtering-measures-through-slicers/
- When: Users ask to filter a report by the value of a measure.

**T15-A359-4.** A slicer can filter by a measure threshold through a user-defined function that wraps the result in CALCULATE with KEEPFILTERS around a FILTER of the entity that tests the measure against a limit; calculation items call it with SELECTEDMEASURE and a fixed limit.
- Option. 2026. https://www.sqlbi.com/articles/filtering-measures-through-slicers/
- When: The filter granularity is fixed, set in the function by the table it filters.
- Version: Here FILTER as a filter argument walks VALUES of the entity's key column, not the whole table (M505).

**T15-A359-5.** Users can also pick the granularity of a measure filter when a disconnected table lists the entities for a second slicer: the function reads the choice with SELECTEDVALUE and uses SWITCH to filter the matching table.
- Option. 2026. https://www.sqlbi.com/articles/filtering-measures-through-slicers/
- When: Users choose both the threshold and the entity it applies to.
- Version: The disconnected table is listed with its purpose as an exception (M411).

### Report design and requirements

**T15-A072-1.** For a picture behind live values, put the visual on top of an image and set the stacking order so that the data layer stays in front.
- Should. Check. 2016. https://www.sqlbi.com/articles/the-space-report-under-the-hood/
- When: A report object needs a graphical background, such as a number label over an illustration.
- Version: From 2016 (Arrange menu). Any transparency must come from the theme, not from formatting on the visual.

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
