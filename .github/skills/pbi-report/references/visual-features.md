# Visual and page features: when to use each, and how it is stored

This file covers the features of visuals and pages beyond the visual type: filters, slicers, drill, table and chart options, titles, bookmarks, page settings, action buttons and report settings.
When the project has no example of a feature, copy the shipped example named in its block (all are listed in `tests/fixtures/examples/INDEX.md`), change its fields, and run `python scripts/check_project.py .`.
Colours, fonts, text sizes, spacing, padding, dividers, borders, shadows, backgrounds and fixed sizes are styling: the theme does that work, so no block here sets them on a visual (`theme.md`, beside this file).

How to read a block:

- **Use** says when Microsoft points to the feature, with the page address. **Limits** are the limits Microsoft lists there.
- **Stored** gives the property names, copied exactly, and the schema (copies in `scripts/schemas`) or Microsoft source that gives them.
- **Copy** names the shipped example: a page folder under `tests/fixtures/examples/Examples.Report/definition/pages/` and the visual's name. "Set it in Power BI Desktop" means no Microsoft source gives the file form.
- **Status** is Microsoft's release status; a block that names none is generally available. A preview feature is used only after the developer's yes, written in section 11 of `docs/report-brief.md`.
- **Check** names what `python scripts/check_project.py .` reads, when a check exists.

## A. Filters

1. **Filter kinds**. Use: a filter card limits a visual, a page or the whole report; Microsoft lists basic, advanced, Top N, relative date, relative time, include and exclude filters. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-report-filter-types
   - Stored: each entry of `filterConfig.filters[]` has `name`, `field`, `type`, `filter` and `howCreated`. `type` is one of `Categorical`, `Range`, `Advanced`, `Passthrough`, `TopN`, `Include`, `Exclude`, `RelativeDate`, `Tuple`, `RelativeTime`, `VisualTopN` (schema `filterConfiguration` 1.3.0). In `filter.Where`, a column names its table by the alias from `From` (`Source`), never by `Entity` (Microsoft's report skill, its file filters.md).
   - Check: V015 warns when `Where` uses an alias that `From` does not declare. B001 fails when a filter names a field the model lacks.
2. **Advanced filter**. Use it for a rule a list cannot express: contains, starts with, greater than, joined with and or or. Source: power-bi-report-filter-types page above.
   - Stored: `type` `Advanced`; the condition is `And` or `Or` with `Left` and `Right`, holding `Comparison`, `Contains`, `StartsWith` or `Not` (filters.md and expressions.md of Microsoft's skill). Contains and starts with work on text only.
   - Copy: `Filters_Kinds_ClusteredColumn_AdvancedFilter` on page folder `Filters_Kinds`. A filter that removes blanks is on the same page (`PageFilterHiddenNoBlankProduct` in its page.json).
3. **Relative date and relative time filters**. Use them when a visual must always show a moving window, such as the last 12 months. Source: https://learn.microsoft.com/en-us/power-bi/visuals/desktop-slicer-filter-date-range; https://learn.microsoft.com/en-us/power-bi/create-reports/slicer-filter-relative-time
   - Limits: the column must be a date or date/time column, not the auto date/time hierarchy; times are read as UTC; weeks start on Sunday; relative time is not offered in publish to web, and the browser cache can return an earlier result.
   - Stored: `type` `RelativeDate` or `RelativeTime`; `Where` holds `Between` with `LowerBound` and `UpperBound` built from `DateSpan`, `DateAdd` and `Now`. `TimeUnit`: 0 day, 1 week, 2 month, 3 year, 4 decade, 5 second, 6 minute, 7 hour (filters.md of Microsoft's skill).
   - Copy: `Filters_Kinds_Line_RelativeDate` and `Filters_Kinds_Line_RelativeTime` on page folder `Filters_Kinds`.
4. **Include and exclude filters**. Power BI adds them when a reader picks Include or Exclude on a data point. Authors can lock, hide, sort or delete them, but not edit them. Source: power-bi-report-filter-types page above.
   - Stored: `type` and `howCreated` are both `Include` or both `Exclude`; the entry has no `field` (filters.md of Microsoft's skill).
   - Copy: `Filters_Kinds_ClusteredColumn_IncludeFilter` and `Filters_Kinds_ClusteredColumn_ExcludeFilter`.
5. **Locked, hidden and ordered filters**. Lock a filter that readers may see but not change; hide one that only cleans data. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-report-filter
   - Stored: `isLockedInViewMode` and `isHiddenInViewMode` on the filter; `filterSortOrder` (`Ascending`, `Descending`, `Custom`) beside `filters`, and `ordinal` on each filter for `Custom` (schema `filterConfiguration` 1.3.0).
   - Copy: the page.json of page folder `Filters_Kinds`. The rule on when to lock or hide is rule 52 of `report-standard.md`, beside this file.
6. **Filter card options**. Single select, and selecting all values but some. Source: power-bi-report-filter page above.
   - Stored: the filter's `objects.general[].properties` holds `requireSingleSelect` or `isInvertedSelectionMode` (schema `filterConfiguration` 1.3.0, untyped there). An inverted selection also wraps the `In` condition in `Not` (filters.md of Microsoft's skill).
   - Copy: `Filters_Kinds_ClusteredColumn_SingleSelectFilter` and `Filters_Kinds_ClusteredColumn_InvertedFilter`.
7. **Showing, hiding or collapsing the Filters pane**. Readers lose the pane when the author hides it in reading view. Source: power-bi-report-filter page above.
   - Stored: `report.json` `objects.outspacePane` (schema `report` 3.3.0); `page.json` also has `outspacePane` and `filterCard`. Their values are not given by any Microsoft source: set the pane in Power BI Desktop. Its look (colours, text) is styling.

## B. Slicers

8. **Relative date slicer**. A compact "last N days, months or years" control on a date column. Source: desktop-slicer-filter-date-range page above. Limits as in block 3.
   - Stored: `objects.data` `mode` `'Relative'` (or `'RelativeTime'` with `relativeTimePeriod` for minutes and hours), with `relativeRange`, `relativePeriod`, `relativeDuration`; `dateRange.includeToday`; and a matching `general.filter` (Microsoft's skill, its file slicers-part-02.md; enum values from Microsoft's visual catalogue). The calendar picker is mode `'RelativeDatePicker'`.
   - Copy: `Slicers_More_Slicer_RelativeDate` on page folder `Slicers_More`.
9. **Hierarchy slicer**. One slicer over several fields, which readers open level by level. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-slicer-hierarchy-multiple-fields
   - Limits: blank values at a level make a ragged hierarchy; on a live connection to Analysis Services, blank members show even when the model hides them.
   - Stored: two or more projections in `Values`. Only the `slicer` in `Basic` or `Dropdown` mode and the `listSlicer` take more than one (slicers.md of Microsoft's skill). An expanded node is saved in `expansionStates` (block 12).
   - Copy: `Slicers_More_Slicer_ProductLevels` on page folder `Slicers_More`.
10. **Apply all slicers and Clear all slicers buttons**. Use them on a page with several slicers, so that one round of choices sends one round of queries. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/buttons-apply-all-clear-all-slicers
    - Limits: both act on every slicer of the page, never on the Filters pane, and you cannot choose slicers. Hiding the last Apply all button returns the slicers to instant apply.
    - Stored: `visualContainerObjects.visualLink` with `type` `'ApplyAllSlicers'` or `'ClearAllSlicers'` (button-part-02.md and button-part-03.md of Microsoft's skill). The button alone does the work. The report-wide query reduction options are `report.json` `slowDataSourceSettings`: `isSlicerSelectionsButtonEnabled`, `isFilterSelectionsButtonEnabled`, `isApplyAllButtonEnabled`, `isFieldWellButtonEnabled`, `isCrossHighlightingDisabled` (schema `report` 3.3.0). The shipped report sets none of them.
    - Copy: `Slicers_More_Button_ApplyAll` and `Slicers_More_Button_ClearAll`. Rule 54 of `report-standard.md`, beside this file, says when to consider them.
    - Check: U104 suggests an Apply button on a DirectQuery page with 2 or more slicers; it reads two of the `slowDataSourceSettings` switches: `isSlicerSelectionsButtonEnabled` and `isApplyAllButtonEnabled`.

## C. Drill and hierarchies

11. **A model hierarchy on a visual**. Use it when readers drill from a total to its detail, such as year to month. Source: https://learn.microsoft.com/en-us/power-bi/explore-reports/end-user-drill
    - Stored: one projection per level, each a `HierarchyLevel` over a `Hierarchy` of the table (schema `semanticQuery` 1.4.0; expressions.md of Microsoft's skill). `active` true marks the level shown first. This template writes `queryRef` as `Table.Hierarchy.Level`; the schema asks only for a name unique in the visual.
    - Copy: `Charts_Features_ClusteredColumn_CalendarDrill` (chart) and `Tables_Features_Matrix_ProductHierarchy` (matrix).
    - Check: B001 reports a hierarchy the model does not have. Header icons are off, so a text box tells readers how to drill (`Charts_Features_Text_HowToDrill`; rule 28 of `report-standard.md`, beside this file).
12. **Expansion state**. Saves which nodes of a matrix or hierarchy slicer stand open. Source: schema `visualConfiguration` 2.8.0.
    - Stored: `visual.expansionStates[]` with `roles`, `levels` (`queryRefs`, `identityKeys`, `isCollapsed`) and `root.children` (`identityValues`, `isToggled`). `identityKeys` go on the level that can open, not on the last level (expressions.md and slicers.md of Microsoft's skill).
    - Copy: `Tables_Features_Matrix_ProductHierarchy`. A state that depends on real values is best saved in Power BI Desktop.
13. **Drilling one visual filters the others**. By default it does not; the author can switch it on. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/service-reports-visual-interactions
    - Stored: `drillFilterOtherVisuals` on the visual, or `settings.defaultDrillFilterOtherVisuals` in `report.json` for the whole report (schemas `visualConfiguration` 2.8.0 and `report` 3.3.0). The shipped report sets it on two visuals only.
    - Copy: `Charts_Features_ClusteredColumn_CalendarDrill`.
14. **Auto-expand and inline hierarchy labels**. Inline labels show every level together after Expand all. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-inline-hierarchy-labels; https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-customize-x-axis-and-y-axis
    - Stored: `categoryAxis.autoExpand`, which Microsoft's catalogue describes as expanding the axis when a field is added (shipped on the drill chart above). How an expanded axis is saved is not given: set Expand all in Power BI Desktop.

## D. Tables and matrices

15. **Totals and subtotals**. Turn a total off when it adds nothing, such as a total of percentages. Source: https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-matrix-visual-format-settings
    - Stored: table `total.totals`; matrix `subTotals` with `rowSubtotals`, `columnSubtotals`, `perRowLevel`, `perColumnLevel`, `rowSubtotalsPosition` (Microsoft's visual catalogue). Custom totals (sum, average and the like) have a schema form (`QueryCustomTotalMetadata`, schema `semanticQuery` 1.4.0) that no source shows in use: set them in Power BI Desktop.
    - Copy: `Tables_Features_Table_TotalsOffWidths` (total off) and `Tables_Features_Matrix_ProductHierarchy` (row subtotals on, column subtotals off).
16. **Column widths**. Fix a width only when a column must not move; otherwise leave the automatic sizing. Source: https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-tables
    - Limits: a width a reader drags lasts for that session only.
    - Stored: `columnHeaders.columnAdjustment` `'fixedWidth'` with `autoSizeColumnWidth` false, then one `columnWidth` entry per column with `value` and a `metadata` selector naming the column's queryRef. `'growToFit'` and `'fitToContent'` are the automatic choices (table.md of Microsoft's skill). The Learn page also describes a width driven by a measure; Microsoft's skill says its validator rejects a data-bound width, so never write one by hand. Freezing matrix row headers (`rowHeaders.unfrozen` in the catalogue) has no source that shows it: set it in Power BI Desktop.
    - Copy: `Tables_Features_Table_TotalsOffWidths`.
17. **Sparklines**. A small trend line inside each row of a table or matrix. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-sparklines-tables
    - Limits: at most five per visual and 52 points each; a matrix with sparklines takes at most 25 columns; not on on-premises Analysis Services; such a visual cannot be pinned.
    - Stored: a projection whose field is `SparklineData` with `Measure`, `Groupings` and `PointsPerSparkline` 52 (schema `semanticQuery` 1.4.0). Its look sits in the `sparklines` object; leave that to the theme.
    - Copy: `Tables_Features_Table_Sparklines`. Status: generally available per the June 2025 release notes; the Learn page still says preview.
18. **Show value as**. Shows a value as a share of the grand, row or column total. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-show-value-as
    - Stored: no source gives the form. Set it in Power BI Desktop, or write a measure with DIVIDE in the model.
19. **Show items with no data**. Keeps rows or columns that have no value for the measure. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-show-items-no-data
    - Limits: it behaves differently in small multiples, and high-density line sampling does not support it.
    - Stored: `showAll` true on the role's `ProjectionState` (schema `visualConfiguration` 2.8.0).
    - Copy: `Tables_Features_Matrix_ItemsWithNoData`.
20. **Conditional formatting: data bars, colour scale, chart lines and legends**. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-conditional-table-formatting; https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-conditional-formatting-chart-line-legends
    - Stored: data bars are `columnFormatting` `dataBars` with `positiveColor`, `negativeColor`, `axisColor`, `reverseDirection`, `hideText` and a `metadata`-only selector (conditional-formatting-part-06.md of Microsoft's skill). Use theme colours (`ThemeDataColor`) only.
    - A colour scale needs a `FillRule`, and Microsoft's skill says `ThemeDataColor` does not work inside one (its file design/color.md). With no colour codes allowed, ask the developer to set a colour scale in Power BI Desktop with the theme's colour-scale colours, or show the state with an icon (`Tables_Table_StoreSales` on page folder `Tables`). Lines and legends formatted by a rule need the same.
    - Copy: `Tables_Features_Table_DataBars`. Check: V009 warns on a colour code; a theme colour passes.
21. **Web addresses and pictures in tables**. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-images-tables; https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-onelake-files
    - Limits: picture addresses must open without sign-in, except OneDrive embed codes and OneLake files; OneLake pictures need read access and fail in publish to web; a moved or renamed file breaks its address.
    - Stored: the link or picture comes from the column's data category in the model (WebUrl, ImageUrl), not from the report. `values.urlIcon` shows a link as an icon (conditional-formatting-part-06.md of Microsoft's skill).
    - Copy: `Tables_Features_Table_WebUrl` for a link. For a picture: the column `Product[Product Image]` of the shipped model carries `dataCategory: ImageUrl`; put it in a table like any column. The model side is in the skill pbi-semantic-model.
    - A picture from a measure in an image visual: `objects.image` with `sourceType` `'imageData'` and the measure in `sourceField`, and no `query` (Microsoft's skill, its file authoring/image.md). The measure or column needs `dataCategory: ImageUrl`, or the picture stays empty. Copy: `Elements_Image_FromMeasure` on page folder `Elements`, with the measure [Selected Product Image].

## E. Charts

22. **Small multiples**. One small chart per value of a field, on a shared axis. Source: https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-small-multiples
    - Limits: forecast, trend lines, axis zoom, concatenated labels and total labels on stacked charts are off; show items with no data may surprise.
    - Stored: the field goes in the `Rows` role (display name Small multiples); `smallMultiplesLayout` is layout and styling (cartesian-part-03.md of Microsoft's skill).
    - Copy: `Charts_Features_ClusteredColumn_SmallMultiples`.
23. **Analytics lines, error bars, forecast and anomalies**. Use a constant line for a fixed threshold. Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-analytics-pane; https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-anomaly-detection
    - Limits: percentile lines need imported data or a newer Analysis Services; anomaly detection needs a line chart on a time axis, no legend, at least four points, and no forecast or other analytics lines.
    - Stored: a constant line is `y1AxisReferenceLine` with `show`, `displayName`, `value` and `dataLabelShow` (Microsoft's visual catalogue; design/visual-cookbook.md of Microsoft's skill).
    - Average, minimum, maximum, median, percentile and trend lines, error bars (`error`), forecast (`forecast`) and anomalies (`anomalyDetection`) keep their settings in parts no source shows: set them in Power BI Desktop.
    - Copy: `Charts_Features_Line_ConstantLine`.
24. **Axis settings**. Axis titles help on a dual axis; a value axis should start at zero. Source: power-bi-visualization-customize-x-axis-and-y-axis page above.
    - Limits: you cannot set the step between ticks; date labels follow the locale.
    - Stored: `categoryAxis` and `valueAxis` with `show`, `showAxisTitle`, `start`, `end`, `invertAxis`, `logAxisScale`, `roundRange` (Microsoft's visual catalogue). Their colours and fonts are styling.
    - Copy: `Charts_Features_ClusteredColumn_AxisSettings`. Rule 46 of `report-standard.md`, beside this file, applies.
25. **Series labels and leader lines**. Names each line at its end, so the legend can go. Source: https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-line-chart
    - Stored: `seriesLabels` with `show` and `leaderLines`; `legend.show` false (Microsoft's visual catalogue).
    - Copy: `Charts_Features_Line_SeriesLabels`.
26. **High-density sampling**. Better sampling for line and scatter charts with many points. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-high-density-sampling; https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-high-density-scatter-charts
    - Limits: tooltips may show only at sampled points; above 60 series, series are dropped in alphabetical order; not for text values.
    - Stored: `query.options` with `allowBinnedLineSample` or `allowOverlappingPointsSample` (schema `visualConfiguration` 2.8.0). Copy: `Charts_Lines_Line_SalesByMonth` and `Charts_Lines_Scatter_StoreSalesAndLines` on page folder `Charts_Lines`.

## F. Titles, number formats, cards and visual calculations

27. **Title or subtitle from a measure**. The text follows the filters. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-conditional-format-visual-titles
    - Limits: the measure must return text and live in the model, not in the report; not for R, Python or key influencers visuals; lost when pinned to a dashboard.
    - Stored: `title.text` or `subTitle.text` holds `{"expr": {"Measure": ...}}` (conditional-formatting.md of Microsoft's skill).
    - Copy: `Charts_Features_ClusteredBar_DynamicSubtitle`. Check: A003 counts such a title as written.
28. **Format string on one visual**. Changes the number format in one visual only. Source: schema `visualConfiguration` 2.8.0 (`RoleProjection.format`).
    - Stored: `format` on the projection. Status: preview in the release notes; needs the developer's yes. Prefer the model's format string. Check: V022 (warn) until section 11 of the brief has a row named `format string on a visual`.
    - Copy: `Tables_Features_Table_VisualFormatString`.
29. **Card visual categories, images and layout**. Several measures and a category in one card visual. Source: https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-card
    - Stored: categories go in the `Rows` role of `cardVisual` (Microsoft's visual catalogue). Images, callout layout and fixed card sizes have no shown form, or are styling: set them in Power BI Desktop.
    - Copy: `Cards_KPIs_Card_SalesByChannel` on page folder `Cards_KPIs`.
30. **ORDERBY in a visual calculation**. Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-visual-calculations-overview
    - Stored: it is DAX text inside `NativeVisualCalculation.Expression`; the file form does not change (rule 67 of `report-standard.md`, beside this file). Status: preview; needs the developer's yes.

## G. Bookmarks and pages

31. **Spotlight in a bookmark**. Fades every other visual of the page. Source: https://learn.microsoft.com/en-us/power-bi/explore-reports/end-user-spotlight
    - Limits: readers set a spotlight in the Power BI service; a bookmark captured with it keeps it.
    - Stored: in the bookmark, `singleVisual.display.mode` `spotlight` (schema `bookmark` 2.1.0).
    - Copy: `tests/fixtures/examples/Examples.Report/definition/bookmarks/Bookmark_SpotlightChart.bookmark.json`. Check: V010 reports a bookmark that holds a visual or page that is gone.
32. **Bookmark groups and navigators**. A group lets one bookmark navigator show only its bookmarks. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/button-navigators
    - Limits: two navigators whose bookmarks change the same settings may show the wrong selected button.
    - Stored: in `bookmarks.json`, a group is `name`, `displayName`, `children` (schema `bookmarksMetadata` 1.0.0). The navigator's `bookmarks.bookmarkGroup` has no shown form: pick the group in Power BI Desktop (rule 13 of `report-standard.md`, beside this file).
    - Copy: `tests/fixtures/examples/Examples.Report/definition/bookmarks/bookmarks.json`.
33. **Landing page**. The page every reader sees first. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-set-landing-page
    - Limits: one page only; a hidden page can be the landing page.
    - Stored: `pages.json` `landingPageName`, a page `name`; it wins over `activePageName` (schema `pagesMetadata` 1.1.0).
    - Copy: `tests/fixtures/examples/Examples.Report/definition/pages/pages.json`. Status: generally available since May 2026. Check: V011 warns when the name is not a page.
34. **Cross-report drillthrough**. Lets readers drill from another report into this one. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-drillthrough
    - Limits: Power BI service only; both reports in the same workspace; field names and data types must match.
    - Stored: on the target page `pageBinding.referenceScope` `CrossReport` (schema `page` 2.1.0), and in the target's `report.json` `settings.useCrossReportDrillthrough` true (schema `report` 3.3.0).
    - Copy: page folder `Drillthrough_CrossReport`. Rule 27 of `report-standard.md`, beside this file, applies. Check: V001 asks for its back button; V013 reports filter values left in it; V023 (warn) reports such a page in a report whose `report.json` does not switch the setting on.
35. **Automatic page refresh**. For DirectQuery pages that watch fast-changing data. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-automatic-page-refresh
    - Limits: not for import models; the capacity admin sets a minimum interval and can turn it off; outside a Premium workspace the fixed interval is 30 minutes. This template asks a written reason below 30 seconds (rule 54 of `report-standard.md`, beside this file).
    - Stored: `page.json` `objects.pageRefresh` (schema `page` 2.1.0 lists `show`, `refreshType`, `duration`, `checkEvery`, `measure`, untyped). The values are not given: set it in Power BI Desktop.

## H. Action buttons and other visuals

36. **Data function button**. Runs a Fabric user data function from the report, for write-back or in-report alerts. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/translytical-task-flow-overview; https://learn.microsoft.com/en-us/power-bi/create-reports/translytical-task-flow-button; https://learn.microsoft.com/en-us/power-bi/create-reports/translytical-task-flow-report-alerts
    - Limits: the function must return text; embedding works only as secure embed; the button keeps its workspace and function and is not rebound by a deployment.
    - Stored: `visualLink` `type` `'DataFunction'` with `dataFunction` (`kind` `ItemLocation`, `byReference.itemId`, `byReference.workspaceId`, and `metadata.dataFunction` with `name` and `parameters[]`); a slicer parameter names the slicer visual (button-part-02.md of Microsoft's skill).
    - Copy: `Data_Function_Button_SendStore` on page folder `Data_Function`. Its ids are made up; the developer picks the real function in Power BI Desktop.
37. **Power Apps, Power Automate, metrics and Gantt visuals**. Source: https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-powerapp; https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-automate-visual; https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-scorecard-visual; https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-gantt
    - Limits: the Power Automate visual handles at most 1,000 records and does not work in embedded analytics or publish to web; the Gantt visual takes up to 1,000 rows.
    - Stored: the Gantt visual is `ganttChart` with the roles `Task` (required), `StartDate`, `EndDate`, `Progress`, `Category`, `Columns` (Microsoft's visual catalogue). The other three have no identifier or binding in any Microsoft source: insert them in Power BI Desktop.
    - Copy: `Charts_Features_Gantt_ProductTasks`. Status: Gantt is preview; needs the developer's yes. Check: V022 (warn) until section 11 of the brief has a row named `Gantt visual`.

## I. Report settings

38. **Report settings**. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-report-settings
    - Stored: `report.json` `settings` (schema `report` 3.3.0), among them `isPersistentUserStateDisabled`, `exportDataMode` (`AllowSummarized`, `AllowSummarizedAndUnderlying`, `None`), `allowChangeFilterTypes`, `disableFilterPaneSearch`, `filterPaneHiddenInEditMode`, `allowInlineExploration`, `pagesPosition`, `useCrossReportDrillthrough`, `defaultDrillFilterOtherVisuals`, `defaultFilterActionIsDataFilter`, `hideVisualContainerHeader`.
    - A report has one `report.json`, so no second example exists. The shipped one sets `useCrossReportDrillthrough` only. Change a setting only after the developer's yes; persistent filters follow rule 15 of `report-standard.md`, beside this file.
39. **Base theme under the owner's theme**. Every report has a base theme (Fluent 2 for new reports); a custom theme sits on top of it. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-reports-visual-defaults
    - Stored: `themeCollection.baseTheme` and `themeCollection.customTheme` (schema `report` 3.3.0). Power BI Desktop writes the base theme; never write it by hand. The owner's theme is `customTheme` (`theme.md`, beside this file).
40. **Visual query limits**. Stop a heavy visual before it fails for readers. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-set-visual-query-limits
    - Limits: older reports have no limit; limits apply to queries from report view only.
    - Stored: `settings.queryLimitOption` (`None`, `Shared`, `Premium`, `SQLServerAS`, `AzureAS`, `Custom`, `Auto`) with `customMemoryLimit` and `customTimeoutLimit` (schema `report` 3.3.0). Set it in Power BI Desktop.
41. **Format string locale**. Fixes the number and date format for every reader. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-default-format-string-locale
    - Limits: USERCULTURE and translations still follow the reader's browser.
    - Stored: `settings.locale` (schema `report` 3.3.0). Write the locale the brief names, after the developer's yes.
42. **DirectQuery variable overrides**. `dataSourceVariables` in `report.json` and in bookmarks (schemas `report` 3.3.0, `bookmark` 2.1.0). No Learn page read explains them: leave them as Power BI Desktop wrote them.

## J. Styling that stays with the theme

43. **Container cards for spacing, padding, divider and lock aspect**. `visualContainerObjects` `spacing`, `padding`, `divider`, `lockAspect` (schema `visualConfiguration` 2.8.0), like colours, fonts, borders, shadows and backgrounds, are styling. Leave them to the theme (`theme.md`, beside this file). Check: V009 warns on fonts, colours, borders, shadows and backgrounds set on a visual.

## Sources

Read on 11 November 2026. Restated in this template's own words; property names are copied exactly.

- Microsoft Learn: every page named with its full address in the blocks above.
- Microsoft's report schemas (copies in `scripts/schemas`): `report` 3.3.0, `page` 2.1.0, `pagesMetadata` 1.1.0, `visualConfiguration` 2.8.0, `bookmark` 2.1.0, `bookmarksMetadata` 1.0.0, `filterConfiguration` 1.3.0, `semanticQuery` 1.4.0.
- microsoft/skills-for-fabric (MIT), skill powerbi-report-cli: its files filters.md, expressions.md, slicers.md, slicers-part-02.md, table.md, cartesian-part-03.md, button-part-02.md, button-part-03.md, conditional-formatting.md, conditional-formatting-part-06.md, formatting.md; design/color.md and design/visual-cookbook.md.
- Microsoft's visual catalogue, npm package @microsoft/powerbi-core-visual-schema 0.1.3: formatting objects, their properties and enum values, and data roles.
- Microsoft's command-line validator, `powerbi-report-author validate` 0.5.0, run offline on a copy of the examples: no finding on roles, types, filters, bookmarks or layout.

## Not confirmed from Microsoft

- The `queryRef` of a hierarchy level (`Table.Hierarchy.Level`), and the `queryRef` and `nativeQueryRef` of a sparkline column: names of this template's own.
- The bounds of a relative time filter as Power BI Desktop saves them: the example follows the one template Microsoft's skill gives for both relative types.
- `ThemeDataColor` inside data bars; the value form of `requireSingleSelect`, `isInvertedSelectionMode` and `valueAxis.start`; whether a constant line or series labels need a selector.
- How show value as, inline labels, analytics lines other than the constant line, error bars, forecast, anomalies, page refresh, card images, custom totals, frozen row headers and a navigator's bookmark group are stored.
- The identifiers of the Power Apps, Power Automate and metrics visuals.
- Nothing in the shipped examples has been opened in Power BI Desktop.

Checklist items: 53, 54, 56, 57, 59, 60, 62, 69
