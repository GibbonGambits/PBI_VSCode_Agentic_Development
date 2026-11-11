# Report-facing DAX and report design

Part 3 of 5 of this topic. Covers: Choosing and building charts.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail. A note may name a tool, a website or a custom visual that this template does not use, or describe publishing, deploying or changing a deployed model: that is information for the developer. You do not install, call or suggest such a tool, and nothing is published or deployed from this template.

## General practice

### Choosing and building charts

**T15-A325-1.** Weigh limiting a pie or doughnut chart to about three categories: angles and areas are judged less accurately than lengths or positions, so more slices, or slices of similar size, are hard to compare. The limit is approximate.
- Consider. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: A pie or doughnut shows shares; a chart that highlights one or two key categories is an exception.
- Version: The checklist's review line stays more than 5 categories (item 54).

**T15-A325-10.** When a pie or doughnut chart has more than three colour-coded categories, take care that the slice colours do not form a gradient, which suggests quantity; schemes of red, blue and green likewise imply volume or sentiment.
- Must. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: A chart with more than three colour-coded categories.

**T15-A325-11.** Judge a chart on filtered data as well: a report is interactive, and a chart that works on the unfiltered data can stop working after readers apply a few filters.
- Must. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: Choosing or reviewing any chart in an interactive report.

**T15-A300-1.** One way to improve a report built around a large detail table or matrix is a scatterplot beside it: readers spot outliers and interesting groups quickly and cross-filter to the details, where the table alone makes them sort, drill and filter.
- Option. 2024. https://www.sqlbi.com/articles/using-scatterplots-to-find-details-in-reports/
- When: Many data points whose spread, outliers or clusters matter.

**T15-A300-5.** The details behind interesting scatterplot points can be given by a details table beside or below the chart: selecting points cross-filters it, so it lists the selected ones only. Tooltips are another way.
- Option. Check. 2024. https://www.sqlbi.com/articles/using-scatterplots-to-find-details-in-reports/
- When: Readers of a scatterplot want more detail on chosen points.
- Version: Written in 2024 before lasso select was available; check the current product. Tooltips need the visual's exception row.

**T15-A300-10.** Scatterplot variants by question: standard for two measures, animated for change over time, bubble for a third measure, quadrant for four segments, volcano for change between two periods, connected for movement, joint, rug, swarm or strip for distributions, binned for many points.
- Option. 2024. https://www.sqlbi.com/articles/using-scatterplots-to-find-details-in-reports/
- When: Choosing a kind of scatterplot.
- Version: Connected, joint, rug, swarm, strip and binned plots need custom visuals or a notebook, outside this template.

**T15-A300-11.** In a dense scatterplot, overlapping points can hide many items. Treat it as an exploratory view for spotting possible segments, and plan a deeper analysis before drawing final conclusions.
- Consider. 2024. https://www.sqlbi.com/articles/using-scatterplots-to-find-details-in-reports/
- When: Scatterplots with many closely packed points.

**T15-A308-11.** Alternatives to a simple bar chart for actuals against a target, such as bullet charts, bar charts with variance or dumbbell charts, may take extra effort to build and support.
- Consider. 2024. https://www.sqlbi.com/articles/introducing-the-3-30-300-rule-for-better-reports/
- When: Choosing an alternative to a simple bar chart.
- Version: These chart types are not core Power BI visuals; custom visuals are outside this template's standards.

## Special-case techniques and facts

### Choosing and building charts

**T15-A325-2.** A pie or doughnut with many categories can still work when it draws attention to one or two of them: colour those, leave the other slices neutral, and possibly merge the rest into one others slice.
- Option. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: One or two of more than about three categories matter most; a dynamic others slice is hard to maintain.
- Version: Theme colours only (V009). Power BI offers static grouping and binning.

**T15-A325-4.** Do not line up several pie or doughnut charts to track progress against a target such as the prior year: a stacked bar chart shows the proportions, and a bullet chart compares each category with the prior year, more clearly.
- Should. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: Current figures are compared with a target or an earlier period.
- Version: A bullet chart is not a core Power BI visual; custom visuals are outside this template's standards.

**T15-A325-5.** To show how part-of-whole proportions change over time, think of a stacked area or 100% stacked area chart; stacked bars stay suitable for discrete periods such as years.
- Consider. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: Shares of a whole are followed over time.

**T15-A325-6.** Pie charts, doughnut charts and many other part-of-whole charts cannot show negative values, nor percentages above 100% such as overachievement.
- Fact. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: Choosing a part-of-whole chart.

**T15-A325-7.** Break down a total that has negative parts, such as costs inside a margin, with a waterfall chart, not a pie or doughnut; the waterfall is among the few charts that show both part-of-whole and negative values.
- Should. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: A part-of-whole breakdown where some parts are negative.

**T15-A325-8.** For a breakdown whose parts follow an implied flow or process, such as open orders that are past due, current or future, prefer a waterfall chart to a pie or doughnut, with a custom sort order where it helps.
- Should. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: Part-of-whole breakdowns with an implied sequence, such as order-to-cash or demand planning.

**T15-A325-9.** Do not show achievement against a target with a pie or doughnut when going past 100% has a meaning of its own in the business process, as in a bonus plan: the overachievement disappears. A bullet chart or connected dot plot may serve better.
- Should. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: KPI or target visuals where values above 100% carry meaning.
- Version: Bullet charts and connected dot plots are not core Power BI visuals; custom visuals are outside this template's standards.

**T15-A325-14.** Before placing pie charts on a map, ask critically whether another chart type, such as a stacked bar chart, would show the data more clearly.
- Consider. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: A report shows proportions by geography with pies on a map.

**T15-A325-15.** Before using a sunburst (multi-level pie) chart for proportions across hierarchy levels, give its readers good explanations and training: this variant is harder for most audiences to read.
- Must. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: Proportions are shown across the levels of a hierarchy.
- Version: In 2025 a sunburst needed a custom visual, outside this template's standards; check the current product.

**T15-A325-18.** Pulling one or more slices out of a pie (an exploded pie) emphasises them, but weigh that readers may then find the slices harder to compare.
- Consider. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: A pie chart must emphasise certain slices.

**T15-A139-1.** A date hierarchy on the axis of a line chart first shows only its top level, the year, so the chart may hold very few points.
- Fact. 2018. https://www.sqlbi.com/articles/improving-temporal-line-charts-in-power-bi-with-dax/
- When: A line chart has a year, quarter and month hierarchy on its axis, from a Date table or auto date/time.

**T15-A139-2.** In a categorical line chart drilled to quarter or month, switching off the X axis option Concatenate Labels is a partial workaround for labels that repeat the year. The gain is small, and more than three years stay hard to show.
- Option. Check. 2018. https://www.sqlbi.com/articles/improving-temporal-line-charts-in-power-bi-with-dax/
- When: A categorical line chart has an expanded date hierarchy on its axis.
- Version: As of 2018; check the current product.

**T15-A139-3.** A line chart can use the Continuous X-axis type at month or quarter grain when the axis holds a date-typed column that maps each period to one date, most naturally its last date. All points then fit without a scrollbar.
- Option. 2018. https://www.sqlbi.com/articles/improving-temporal-line-charts-in-power-bi-with-dax/
- When: A trend line at a grain coarser than day, where the period column would otherwise be text.

**T15-A139-4.** For the end-of-period date on each Date row, EOMONTH serves months of a standard calendar. For any grain and for custom calendars, take MAX of the date in CALCULATE with ALLEXCEPT that keeps only the columns identifying the period.
- Option. 2018. https://www.sqlbi.com/articles/improving-temporal-line-charts-in-power-bi-with-dax/
- When: Building a date-typed period column, for example for a continuous line chart axis.

**T15-A139-5.** When grouping Date rows by period, identify the period by one column that is unique across years; failing that, keep every column that together identifies it, such as year and quarter number.
- Should. 2018. https://www.sqlbi.com/articles/improving-temporal-line-charts-in-power-bi-with-dax/
- When: Computing a period-level value, such as the end-of-period date, with ALLEXCEPT over the period columns.

**T15-A139-6.** End-of-month and end-of-quarter date columns used on a continuous axis can take the format string `MMMM yyyy`; by default the tooltip labels a point with the full end-of-period date.
- Option. 2018. https://www.sqlbi.com/articles/improving-temporal-line-charts-in-power-bi-with-dax/
- When: A continuous line chart whose axis column stores the last date of each month or quarter.

**T15-A139-7.** On a continuous line chart plotted on an end-of-period date column, switch on the X-axis title: the dates alone do not show whether a point stands for a month or a quarter.
- Should. 2018. https://www.sqlbi.com/articles/improving-temporal-line-charts-in-power-bi-with-dax/
- When: A continuous line chart whose axis column stores the last date of each month or quarter.

**T15-A139-8.** A continuous line chart at week grain needs a Date column grouping the days of each week: build a sequential week number from a fixed reference date with a settable first weekday (a hideable helper), then a date column with each week's last day.
- Must. 2018. https://www.sqlbi.com/articles/improving-temporal-line-charts-in-power-bi-with-dax/
- When: A line chart with a continuous axis at week granularity.

**T15-A139-9.** A measure can blank out the partial weeks at both ends of the user's date selection: read the selected range and the week boundaries with ALLSELECTED, then apply only the dates of complete weeks through DATESBETWEEN inside KEEPFILTERS. Totals and weekly averages then stay correct.
- Option. 2018. https://www.sqlbi.com/articles/improving-temporal-line-charts-in-power-bi-with-dax/
- When: A weekly chart on a calendar that is not week-based, where a date selection can cut the edge weeks.

**T15-A139-10.** A weekly line chart gains 52 points for each year it covers, so narrowing the date range the chart shows can help.
- Option. 2018. https://www.sqlbi.com/articles/improving-temporal-line-charts-in-power-bi-with-dax/
- When: A line chart at week grain spans several years; outside a week-based calendar the edge weeks may be incomplete.

**T15-A284-1.** One way to hold a chart's Y-axis still while slicers change: bind the axis maximum to a measure, the largest bar value, such as MAXX over the axis column, inside CALCULATE with REMOVEFILTERS on the slicer column. A typed maximum needs editing when data changes.
- Option. 2023. https://www.sqlbi.com/articles/using-dax-to-control-a-chart-range-in-power-bi/
- When: The axis should keep the range it shows with no selection; which filters to remove depends on requirements.

**T15-A284-2.** A measure that computes a chart's axis maximum can round its result up with ROUNDUP to a clean magnitude, such as whole millions, so the axis does not end at an odd value.
- Option. 2023. https://www.sqlbi.com/articles/using-dax-to-control-a-chart-range-in-power-bi/
- When: An axis maximum bound to a measure.

**T15-A284-3.** Two side-by-side charts that slice one value by different columns can share a Y-axis maximum: compute the largest value per grouping, take the larger of the two with MAX, and bind that one measure to the axis maximum of both charts.
- Option. 2023. https://www.sqlbi.com/articles/using-dax-to-control-a-chart-range-in-power-bi/
- When: Two charts meant to be compared by eye, each grouped by a different column.

**T15-A284-4.** Two charts, each filtered by its own slicer on one column, share one Y-axis range only when the slicers use two disconnected tables. Each chart's measure applies its slicer's selection with TREATAS; both axis maxima bind to one measure returning the highest value either reaches.
- Must. 2023. https://www.sqlbi.com/articles/using-dax-to-control-a-chart-range-in-power-bi/
- When: Comparing two free selections of one attribute, each chosen with its own slicer.
- Version: Each disconnected slicer table is listed with its purpose as an exception (M411).

**T15-A300-2.** A scatterplot with very many points may not show them all, so an unfiltered chart can miss data points. The core scatter visual shows 3,500 points by default, at most 10,000; most custom visuals allow up to 30,000 and R visuals 150,000.
- Fact. 2024. https://www.sqlbi.com/articles/using-scatterplots-to-find-details-in-reports/
- When: Charts with a very large number of points.
- Version: Limits as stated in 2024. R visuals are retiring (V016); custom visuals are outside this template.

**T15-A300-3.** For a volcano plot in a year-over-year review, put the target measure on the Y-axis and the comparison measure on the X-axis, and place the whole dimension hierarchy, not only its lowest-level name, in the Values well so readers can drill down.
- Should. 2024. https://www.sqlbi.com/articles/using-scatterplots-to-find-details-in-reports/
- When: Readers must see change between two periods and pick the items to analyse further.
- Version: Drill icons are off here: tell readers on the page how to drill, or list the visual's exception.

**T15-A300-4.** Make a volcano plot easier to use: an X-axis constant line at zero, minimum and maximum constant lines whose names label below-target and above-target, a size measure for emphasis, colour by the change measure or by category, and optionally zoom sliders.
- Should. 2024. https://www.sqlbi.com/articles/using-scatterplots-to-find-details-in-reports/
- When: A volcano-style scatterplot comparing a change against a target.
- Version: Theme colours only; a colour code, transparency or font set on the visual needs an exception row (V009).

**T15-A300-6.** In an exploratory report, consider two scatterplots that cross-filter each other. It helps most when studying how two closely linked attributes, such as product and region, relate.
- Consider. 2024. https://www.sqlbi.com/articles/using-scatterplots-to-find-details-in-reports/
- When: Exploratory reports.

**T15-A300-8.** When field parameters let readers switch the axes or grouping of a scatterplot, take care to offer only combinations that make sense: meaningless ones confuse.
- Consider. 2024. https://www.sqlbi.com/articles/using-scatterplots-to-find-details-in-reports/
- When: Scatterplots driven by field parameters, usually for advanced readers exploring several views on one page.

**T15-A312-3.** When a one-dimensional dot plot of a single measure has many overlapping points, the points can be spread randomly along the Y-axis (jitter). Overlap hides how many points there are and whether groups exist.
- Option. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: Showing the distribution of one measure across many items with a scatterplot.

**T15-A312-4.** When a scatterplot is repurposed as a jitter plot, turn off the Responsive setting in the general properties of the visual container.
- Should. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: A core scatterplot used as a jitter or swarm plot.

**T15-A312-12.** When a jitter plot holds very many points, a second chart can sit directly above it, such as a line chart of item counts per binned value with its X-axis aligned, with the selected item's value marked by an X-axis constant line (one value only).
- Option. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: A jitter plot comparing a selected item with all others, with too many points to judge clusters.

**T15-A312-13.** The random jitter offset can be kept narrow, for example by centring the RAND value on zero and scaling it down, so the points do not spread over too much vertical space and clutter the chart.
- Option. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: A jitter plot whose Y-axis position comes from a random offset.

**T15-A312-14.** Finish a chart assembled from several visuals with a clean-up pass: for example add a background container, and group and name all its visual containers in the selection pane.
- Should. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: Composite charts built from several visuals, such as a jitter plot with a joint plot.
- Version: Data visuals that overlap need an exception row in the brief (G002); visual names follow the template's label pattern.

**T15-A312-16.** In a scatterplot used as a dot or jitter plot, a Y-axis constant line named after the measure can serve as an axis label marking where the chart begins. It shows up when the minimum of the X-axis is moved below zero.
- Option. 2024. https://www.sqlbi.com/articles/highlighting-a-data-point-and-comparing-to-all-others-in-a-distribution/
- When: A core scatterplot repurposed as a one-measure dot or jitter plot.

**T15-A318-8.** A simple bullet chart can be made from the core bar chart: enable error bars, bind both the upper and the lower bound to the target measure, set bar width and marker width to the highest value and border width to zero.
- Option. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: Simple category comparisons; aggregate performance or qualitative ranges need other approaches.
- Version: The widths are sizes set on one visual, which the theme rule allows only when the developer asks.

**T15-A318-19.** A bullet chart made from a core bar chart with error bars can be refined: a wider gap between categories for thinner bars, conditional formatting on bars and data labels to flag underperforming categories, gridlines, and a title naming what actuals are compared with.
- Option. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: A bullet chart built from the core bar chart, with error bars marking the target.
- Version: Theme colours only; a colour code needs an exception row (V009). Bar spacing is set only when the developer asks.

**T15-A318-21.** Action dots can be added to an actual-versus-target chart to draw the eye to categories that over-perform or under-perform.
- Option. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: Charts comparing actuals with a target by category, such as a bullet chart.
- Version: Shown in Deneb, a custom visual from AppSource, outside this template's standards.
