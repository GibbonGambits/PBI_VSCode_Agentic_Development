# The report standard

This file holds the rules for report features beyond layout: field parameters, bookmarks and buttons, tooltip and drillthrough pages, sync slicers, conditional formatting, phone layout, chart choice, titles and filters, accessibility, page density, and report-level calculations.
`python scripts/check_project.py .` checks it: the codes that start with V, A and U1.
An exception counts only when section 10 of `docs/report-brief.md` lists the code, the page and the visual (or `-` for a whole page) with a reason.

## What the script checks

| Code | Rule | Level |
|---|---|---|
| V001 | A drillthrough page has no back button (a button whose action is `Back`, switched on) | fail |
| V002 | A tooltip page is not hidden (`visibility` is not `HiddenInViewMode`) | warn |
| V003 | A tooltip page is wider than 640 or higher than 480 (twice the built-in 320 x 240) | warn |
| V004 | A tooltip page holds a slicer, a button or a navigator | warn |
| V005 | The visuals on a tooltip page use fewer than 3 fields in all | warn |
| V006 | A page that is not a tooltip page has more than 16 visuals that show data and are not hidden. A table or matrix that covers a third of the page or more counts as 2 | fail |
| V007 | Such a page has 13 to 16 of them | warn |
| V008 | A button's action goes to a bookmark or a page that the report does not have | warn |
| V009 | A visual sets its own font, size, colour, bold, italic or underline, writes a colour code, or switches on its own border, shadow or background. A theme colour passes, as a `ThemeDataColor` or as a theme keyword such as `'maxColor'` | warn |
| V010 | A bookmark holds a page or a visual that the report no longer has | warn |
| V011 | `pages.json` and the page folders disagree: a page listed twice, listed but missing, or not listed; an opening or landing page that does not exist | warn |
| V012 | A report-level measure's name does not start with the prefix: an underscore, or the prefix the brief gives | warn |
| V013 | Filter values are saved on a tooltip page or in a drillthrough filter (left over from design time) | warn |
| V014 | A drillthrough page is visible and has no button with a Bookmark action (a reset) | warn |
| V015 | A filter's `Where` clause uses a source name that its `From` list does not declare | warn |
| V016 | A visual type Microsoft is retiring or has deprecated: `map`, `filledMap`, `qnaVisual`, `scriptVisual` (R), `pythonVisual` | warn |
| V017 | A visual names an image or other resource that `report.json` does not register, or whose file is not in the report folder | warn |
| V018 | A page that is not a tooltip page has visuals but no text box (no visible page title) | note |
| V019 | A report-level measure calls USERCULTURE (the file `multiple-languages.md` in the skill pbi-semantic-model) | warn |
| V020 | A report on a model with translations holds typed text: text boxes and typed visual titles (one finding for each report) | warn |
| V021 | A report on a model with translations shows more than one page tab | warn |
| V022 | The report uses a preview feature that section 11 of the brief does not list: the Gantt visual, a format string on one visual (`visual-features.md`, beside this file) | warn |
| V023 | A cross-report drillthrough page in a report whose `report.json` does not have `settings.useCrossReportDrillthrough` on | warn |
| V025 | A visual that shows data and a title, in a report whose theme switches subtitles on (Microsoft's Fluent2 base themes do), with no `subTitle` of its own: it shows a second heading made of field names | warn |
| V026 | A colour scale that runs from the theme's `minimum` (red) to its `maximum` (green), by keyword (`'minColor'`, `'maxColor'`) or by code: it says low is bad, and red with green is a hard pair. An amount gets one colour from light to dark (`design.md`, beside this file, section 3). A good-or-bad scale with a known direction needs a row in section 10 of the brief | warn |
| V024 | Data bars (`dataBars`) without `positiveColor` or `negativeColor`. Seen once, with all colour parts removed: Power BI Desktop then fails to load the whole report | fail |
| A001 | A visual that shows data, or an image, has no alt text (hidden visuals are not checked; an image that is only decoration is listed in the brief) | warn |
| A004 | Alt text is longer than 250 characters | warn |
| A002 | Two visuals on one page share a tab order number (members of a group are not compared) | warn |
| A003 | A visual that shows data shows the title Power BI makes up from field names. Slicers and tooltip pages are not checked | warn |
| U101 | A slicer on one field is on 2 or more pages and is not synced on all of them (tooltip and drillthrough pages are not counted) | note |
| U102 | A page has 3 or more buttons that each go to a page | note |
| U103 | Two data visuals of the same kind sit in the same place, and bookmarks show one at a time | note |
| U104 | A report on a model with DirectQuery tables has a page with two or more slicers and no Apply button setting | note |
| U105 | A `multiRowCard` or a legacy `card`: the new card visual replaces them | note |
| U106 | A Top N filter or a filter on a measure, on a visual of a report whose model has DirectQuery tables (`storage-and-security.md` in the skill pbi-semantic-model, rule 24) | note |

- In section 10, write Page and Visual as `python scripts/list_visuals.py .` prints them; the script also accepts the visual's `name` or folder.
- For V010, write the bookmark's name under Page and `-` under Visual.

## A. Field parameters

1. Suggest a field parameter when 2 or more measures or fields compete for the same place on a page. Readers then switch them with one slicer, instead of meeting duplicate visuals or pages. Source: checklist item 64; https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters (Microsoft presents field parameters as the way to let readers change the measures or dimensions a visual analyses); https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization (field parameters are among the features to consider). The script gives U103 when bookmarks swap two visuals of the same kind in one place.
2. A field parameter has two halves: a table in the model, and on the page one slicer plus at least one target visual. Never leave a page with only one half. Source: microsoft/skills-for-fabric, skill powerbi-report-cli, its file field-parameters.md.
3. The model side is in the file model-objects.md of the skill pbi-semantic-model. The report work never edits the model. It reads the table only to recognise it: its hidden fields column carries `ParameterMetadata` with `"kind":2`. Source: the same file of Microsoft's skill.
4. The slicer binds the parameter's visible column (the labels), never the hidden fields column or order column. Source: the same file.
5. The target visual lists every field of the parameter as ordinary projections, in the parameter's order, in the role the parameter feeds. Beside `projections` in that role it has a `fieldParameters` entry: `parameterExpr` names the visible column, `index` is where its fields start in the role, `length` is how many there are, `sortDirection` is optional. Source: Microsoft's report schema `visualConfiguration` 2.8.0 (`ProjectionState`, `RoleFieldParameter`); the same file of Microsoft's skill.

```json
"fieldParameters": [ { "parameterExpr": { "Column": { "Expression": { "SourceRef": { "Entity": "Show By" } }, "Property": "Show By" } }, "index": 0, "length": 3 } ]
```

6. Limits Microsoft lists (https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters). Tell the developer the ones that apply before building:
   - a date column inside a parameter loses its automatic date hierarchy;
   - AI visuals and Q&A do not support them;
   - readers cannot pick "none": no selection shows all;
   - they cannot be made on a live connection without a local model;
   - implicit measures are not allowed: use an explicit measure;
   - a field parameter cannot be the linked field of a drillthrough or tooltip page;
   - fields show in the order the reader picks them.
- Copilot does: recognise the table, add the missing half on the page, show the developer the plan first.
- Only Desktop shows: whether each choice switches correctly. A wrong field reference can pass the schema and still show an error icon (Microsoft's skill, same file). Ask the developer to try every choice.

## B. Bookmarks, and buttons that switch views

7. A bookmark stores a captured state: page, filters, slicers, selection, sort, drill level, what is hidden, focus or spotlight. It does not store positions. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-bookmarks; Microsoft's report schema `bookmark` 2.1.0.
8. Each bookmark is a file `definition/bookmarks/<name>.bookmark.json` with `name`, `displayName`, `explorationState` and `options`. `bookmarks.json` lists each bookmark once, in order, in `items[]`; a group is `{name, displayName, children[]}`. Source: schemas `bookmark` 2.1.0 and `bookmarksMetadata` 1.0.0; Microsoft's skill, its file bookmark.md.
9. A bookmark that only switches what is shown must keep the reader's filters: `options.suppressData` true (the Desktop "Data" box off). The `suppress*` options are the inverse of the Desktop boxes. Source: desktop-bookmarks page above; Microsoft's skill, `bookmark.md`.
10. Saved state uses raw page, visual and filter ids, and adding a slicer to a page with bookmarks clears that slicer in them. A simple bookmark that shows one visual and hides another can be written from the shipped example. A bookmark that saves filters, slicer choices or drill state is captured in Desktop (Bookmarks pane, Update): list it for the developer. After any change to bookmarks, every one is clicked both ways, by you through pictures of the page or by the developer. Source: desktop-bookmarks page; Microsoft's skill, `bookmark.md`. A bookmark that names a page or visual that is gone gives V010.
11. A button's action is `visual.visualContainerObjects.visualLink`. `show` must be true. `type` is one of `'Back'`, `'Bookmark'`, `'PageNavigation'`, `'Drillthrough'`, `'WebUrl'`, `'Qna'`. The target sits in `bookmark`, `navigationSection`, `drillthroughSection` or `webUrl`, and is the bookmark's or page's `name`, never its `displayName`. Source: schema `visualConfiguration` 2.8.0 (`VisualLink`; the schema does not list the `type` values); Microsoft's skill, its file button-part-02.md, `button-part-03.md`, `bookmark.md`. A target that does not exist gives V008.

```json
"visualLink": [ { "properties": {
  "show": { "expr": { "Literal": { "Value": "true" } } },
  "type": { "expr": { "Literal": { "Value": "'PageNavigation'" } } },
  "navigationSection": { "expr": { "Literal": { "Value": "'SalesDetail'" } } } } } ]
```

12. Prefer a page navigator (`pageNavigator`) to a row of page buttons, and a bookmark navigator (`bookmarkNavigator`) to a row of bookmark buttons: navigators follow the page and bookmark lists by themselves. When a button only changes page, use the page navigation action, not a bookmark. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/button-navigators; https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-buttons. Three or more page buttons on one page give U102.
13. Keep a navigator that Desktop made. Do not guess how a bookmark navigator stores its bookmark group. Give every navigator alt text that says what it changes. Source: Microsoft's skill, `bookmark.md`; button-navigators page above.
14. In a report with 2 or more pages or sections with their own navigation: no dead-end page, and no hidden path without an obvious way in. Source: checklist item 51. Header icons are off, so every route is a visible button, navigator or written instruction (`theme.md`, beside this file).
15. Default state and reset (checklist items 53 and 62):
   - The filters in place when the report is saved are the state readers return to with Reset to default. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-report-add-filter.
   - Persistent filters are on by default and can give unexpected results with bookmarks. The switch is `settings.isPersistentUserStateDisabled` in `report.json` (schema `report` 3.3.0). Source: https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-troubleshoot.
   - Write one explicit decision on persistent filters in section 6 of `docs/report-brief.md`. Source: checklist item 53.
   - A report with real filter state has one clear reset path: Reset to default, or a reset bookmark on a button. Source: checklist item 62; Microsoft's skill, its file interactivity.md.
- Copilot does: buttons and their actions, checks that every target exists, and a simple bookmark written from the shipped example (rule 10). A bookmark that saves filters, slicer choices or drill state is proposed; the developer captures it in Desktop.
- The shipped example for bookmarks and buttons is listed in the examples index, `tests/fixtures/examples/INDEX.md`.

## C. Report page tooltips

16. Owner's rule: every visual has Tooltips off. A report page tooltip needs the hovered visual's Tooltips on. So it is allowed only for a visual listed in section 7 of `docs/report-brief.md`, which carries the annotation `HeaderTooltipException` with `tooltip: <reason>` (`.github/instructions/pbir.instructions.md`, rule 5; `pages-and-visuals.md`, beside this file). The shipped example for a tooltip page (listed in the examples index, `tests/fixtures/examples/INDEX.md`) carries its exception.
17. A tooltip page has `page.json` `type` `"Tooltip"` and a `pageBinding` with `type` `"Tooltip"`, its tooltip fields in `parameters[]`. A page with no tooltip fields shows blank. Source: schema `page` 2.1.0 (`PageBinding`, `BindingParameter`); https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-tooltips.
18. Hide every tooltip page: `visibility` `"HiddenInViewMode"` (V002). Keep it small, near the built-in Tooltip size of 320 x 240 (V003). Source: https://learn.microsoft.com/en-us/power-bi/guidance/report-page-tooltips.
19. A tooltip cannot be clicked: no slicers or buttons on it. When readers must interact, use a drillthrough page (V004). Source: report-page-tooltips guidance and desktop-tooltips page above.
20. A report page tooltip adds 3 or more facts beyond the value hovered over (V005). Source: checklist item 65.
21. Never put needed information only in a tooltip: Microsoft says that people with motor difficulties and people who do not use a mouse have trouble reaching tooltips. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports.
22. A visual points to a tooltip page through `visualContainerObjects.visualTooltip`: `show`, `type` and `section` (the tooltip page's `name`). Source: schema `visualConfiguration` 2.8.0 (`VisualTooltip`). The value of `type` for a report page is not confirmed: copy it from the shipped example or from a visual set up in Desktop.
- Copilot does: the page files, its hidden state and size, the binding, and the pointer on a visual listed in the brief.
- Only Desktop shows: whether the tooltip appears and fits. Remove design-time filter values from the tooltip page before publishing (report-page-tooltips guidance). Code V013 (warn).

## D. Drillthrough

23. Every drillthrough page has a back button: an `actionButton` whose `visualLink` has `type` `'Back'` and `show` true. Desktop adds one when the drillthrough field is set; keep it. Source: checklist item 63 (100% of drillthrough pages have back navigation); https://learn.microsoft.com/en-us/power-bi/guidance/report-drillthrough; Microsoft's skill, `button-part-03.md`. Code V001 (fail).
24. The binding: `page.json` `type` `"Drillthrough"`, and `pageBinding` with `type` `"Drillthrough"`, `referenceScope` (`Default` or `CrossReport`), `acceptsFilterContext` (`Default` or `None`) and `parameters[]`. Each parameter's `boundFilter` names a page filter in the page's `filterConfig` whose `howCreated` is `"Drillthrough"`. Source: schema `page` 2.1.0 (`PageBinding`); schema `filterConfiguration` 1.3.0; Microsoft's skill, its file authoring-workflows.md.
25. The drillthrough field must also be in the source visual, not summed or counted there, or the drillthrough does not appear. A field parameter cannot be a drillthrough field. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-drillthrough; field-parameters page.
26. The source page's page filters also pass to the target, as a second kind of drillthrough filter. Readers can edit or clear it; authors cannot lock or hide it. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-report-filter-types. Whether `acceptsFilterContext` is the Desktop "Keep all filters" switch is not confirmed: ask the developer to set that switch in Desktop.
27. Cross-report drillthrough works only in the Power BI service, between reports in the same workspace, with field names and data types that match exactly, and with the setting on in the target report: `settings.useCrossReportDrillthrough` in `report.json` (schema `report` 3.3.0), and `referenceScope` `CrossReport` on the target page. Source: desktop-drillthrough page above.
28. Header icons are off (owner's rule), so a text box tells readers how to drill through and what the drillthrough page expects. Make the expected context obvious on the page. Source: checklist items 59 and 63; report-drillthrough guidance (instructions in a text box).
29. Hide drillthrough pages. If one stays visible, add a button with a bookmark that clears its filters (V014, warn). Remove design-time drillthrough values before publishing (V013, warn). Source: report-drillthrough guidance above.
- Copilot does: the page type and binding, the back button, and the instruction text box.
- Only Desktop shows: whether the right-click menu offers the page, and whether visuals show blanks or errors under the drillthrough filter.

## E. Sync slicers

30. When the same slicer field is on 2 or more pages, sync it unless the pages need their own state. Leave no repeated slicer unsynced without a reason. Source: checklist item 61. Code U101 (note).
   - In a composite model, a visual takes its fields from one source group where it can: its queries are then faster. When two source groups each hold a copy of a dimension, a hidden slicer on the copy, synced to the visible slicer by the same group name, can replace a relationship between the groups. Hide the copies and describe why they exist. No check: the report files do not mark which source group a field comes from. Source: https://learn.microsoft.com/en-us/power-bi/guidance/composite-model-guidance ; https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-slicers (sync separate slicers).
31. Sync is stored on each slicer as `visual.syncGroup`: `groupName` (required), `fieldChanges` and `filterChanges` (plain true or false). Every slicer in a group has the same visual type and the same column. Source: schema `visualConfiguration` 2.8.0 (`VisualSyncGroup`, "only applies to slicer visuals"); Microsoft's skill, its file slicers-part-02.md.

```json
"syncGroup": { "groupName": "RegionSlicer", "fieldChanges": true, "filterChanges": true }
```

32. A slicer synced to a page where it is not shown still filters that page. Tell the developer. How such a hidden copy is stored is not confirmed. Source: https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-slicers.
33. Before publishing, clear saved slicer selections that do not suit every reader, above all with row-level security. Source: https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-troubleshoot.
- Copilot does: the same `syncGroup` on each slicer of the group, after the developer's yes to the U101 note.
- Where slicers sit stays in `layout-standard.md`, beside this file.
- Only Desktop shows: the full picture in the Sync slicers pane.

## F. Conditional formatting

34. Kinds: colour scale (gradient), rules (value ranges), field value (a measure that returns a colour), icons, data bars, and titles from a measure. Source: https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-conditional-formatting; https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-conditional-table-formatting.
35. In the files the formatted property holds an expression, scoped by a `selector`: `FillRule` (gradient), `Conditional` with `Cases` and `DefaultValue` (rules), `Measure` (field value), `ThemeDataColor` (a theme colour). Source: schema `semanticQuery` 1.4.0; schema `formattingObjectDefinitions` 1.5.0. Object names inside `objects` differ per visual type: copy them from a visual of the same type in this report.
36. Owner's rule: the theme is never changed, and no colour, font or size is set on a single visual (`theme.md`, beside this file). Use theme colours (`ThemeDataColor`), and inside a colour scale the theme file's colours chosen by meaning (`design.md`, beside this file, section 3), never another colour code. Codes V009 and V026. A colour code needs a row in section 10 of the brief.
37. Never carry meaning by colour alone: add a label, an icon or a marker. The theme's red and green are about equally light (`theme.md`, beside this file). Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports; checklist items 57 and 66.
38. At most 2 meaning-carrying colour systems in one report; the same colour always means the same thing; no conflicting red and green between KPI visuals. Write every KPI threshold in section 6 of the brief. Source: checklist items 57 and 58.
39. Rule bounds on a percentage are decimals with the Number option; a field-value measure returns text. Source: the two conditional formatting pages above.
- Only Desktop shows: the colours a rule really gives.

## G. Mobile layout

40. The phone layout is a second layout of a page. Only the Power BI phone apps show it, in portrait; browsers always show the web layout. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-create-mobile-optimized-report-about.
41. It is stored per visual in `definition/pages/<page>/visuals/<visual>/mobile.json` (schema `visualContainerMobileState` 2.8.0: its own `position`, `objects`, `visualContainerObjects`). Older reports have `mobileState.json`, which Microsoft says does not support editing outside Desktop. Source: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report.
42. Owner's rule: this template never edits `mobile.json` or `mobileState.json` (`.github/instructions/pbir.instructions.md`, rules 9 and 10). Why: Copilot cannot see the phone canvas; the phone position is separate from the web position; and auto-create in Desktop replaces any phone layout that exists (https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-create-mobile-optimized-report-mobile-layout-view).
43. Tell the developer, after any page change, to open Mobile layout in Desktop and check that page. Microsoft's advice for that work: only the key visuals; fonts not under 9 pt; at most 323 wide; no visuals side by side except cards, KPIs and buttons; tooltips are off on the phone canvas; slicer choices made there are not kept. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-create-mobile-optimized-report-best-practices; mobile-layout-view page above.

- Copilot does: nothing in the phone files; it names the pages that changed.

## H. Choosing the chart type

44. Pick the visual from the question it answers. Source: https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualizations-overview; https://learn.microsoft.com/en-us/power-bi/create-reports/service-dashboards-design-tips; Microsoft's skill, its file chart-selection.md.

| Question the visual answers | Visual type |
|---|---|
| Comparison of categories | Bar chart (long names) or column chart |
| Trend over time | Line chart on an ordered date axis; area when the size of change matters; columns for a few periods |
| Part of a whole | Donut or pie with few slices; 100% stacked bar; treemap for many or nested parts |
| Ranking | Bar chart sorted by the measure; ribbon chart when rank changes over time |
| Distribution | Column chart over binned values (Power BI has no built-in box plot) |
| Relationship of two measures | Scatter chart with a Details field; bubble for a third measure |
| Single number | Card; KPI for progress to a goal |
| Detail and exact values | Table; matrix for several dimensions and drill |
| Location | Azure map |
| Flow through stages | Funnel for stages; waterfall for increases and decreases; decomposition tree for a breakdown |

45. Review a part-to-whole visual with more than 5 categories. A trend uses a true ordered time or category axis. Source: checklist item 54.
   - Microsoft's skill gives rough limits per chart type, as guidance: a bar chart about 15 to 20 categories with one series; a clustered bar or column chart about 10 categories and 2 or 3 series; a line chart at most 5 lines; a pie or donut at most 5 slices; a scatter chart 3 to 5 colour groups; a treemap 20 to 30 tiles; a table or matrix 5 to 8 visible columns. Past a limit, group the rest as "Other", filter, or split the chart. The checklist's number for part-to-whole (more than 5) stays the review line. No check: it needs the data. Source: Microsoft's skill, its file chart-selection.md.
46. No unlabeled dual axis. Repeated comparable measures use the same display units unless justified. Avoid 3-D charts and value axes that do not start at zero. Source: checklist item 56; https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-tips-and-tricks-for-creating-reports.
   - Microsoft's skill lists the same mistakes and a few more; each is guidance.
   - No three-dimensional effects. No check: Microsoft documents no file property for them.
   - Bars and columns start at zero. No check: Microsoft's visual catalogue names the property (`valueAxis.start`), but no Microsoft source shows how its value is written, so the files do not show a breach for certain.
   - A second value axis only when both series share a unit, and then with a title; otherwise use two charts. No check, for the same reason.
   - A pie or donut with more than 5 slices becomes a bar chart sorted by value (rule 45). No check: it needs the data.
   - No gauge as a KPI: it takes much space for one number and shows no trend. Use a card, or a KPI visual for progress to a goal. No check: whether a gauge serves as a KPI is a judgement.
   - Sort bars by value, unless the categories have their own order (months, stages). No check: it needs a judgement on the categories.
   - Source: Microsoft's skill, its file design/anti-patterns.md and chart-selection.md; GitHub's awesome-copilot, https://github.com/github/awesome-copilot/blob/main/instructions/power-bi-report-design-best-practices.instructions.md (axes from zero, bars sorted by value, few categories).
47. Do not create retired or retiring visuals: the Q&A visual (it ends in December 2026 or February 2027; Microsoft Learn pages differ), and the Bing map and filled map (use Azure Maps). Microsoft's skill also says `cardVisual` instead of `multiRowCard`, and `azureMap` instead of `map` and `filledMap`. Source: visualizations overview above; https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-troubleshoot; Microsoft's skill, its file authoring-part-04.md.
   - By `visualType`: `map` and `filledMap` (deprecated; use `azureMap`), `qnaVisual` (the Q&A visual), `scriptVisual` (the R visual) and `pythonVisual` (both retiring in May 2027). Code V016 (warn). Source: also https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-map-visualizations-overview ; https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-q-and-a ; https://learn.microsoft.com/en-us/power-bi/create-reports/script-visuals-overview.
   - `multiRowCard` and the legacy `card`: new reports use the new card, `cardVisual`. Old cards are not converted by themselves; replacing one is a change the developer says yes to, or part of a design pass (`design.md`, beside this file). Code U105 (note). Source: also https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-card ; Microsoft's skill, its file authoring/card.md.
   - The shipped examples of `card`, `multiRowCard`, `scriptVisual` and `pythonVisual` (`tests/fixtures/examples/INDEX.md`) exist so that Copilot recognises these types in old reports. Never copy them into a new report.
48. Custom visuals are outside this template. `visualType` is free text in the schema: copy it from a visual of the same type in the report, or from the shipped example of that type (`tests/fixtures/examples/INDEX.md`). Ask the developer to place one in Desktop only when the index has no example of it.
- Only Desktop shows: whether the chart reads well with the real data.

## I. Titles, labels and filters

49. Every data visual has a title that says what it shows: `visualContainerObjects.title` with `show` and `text`; a subtitle is `subTitle`. No placeholder or field-name titles. A visual shows one heading: when you write a title, look at the subtitle too. A subtitle that repeats the title, or that Power BI made up from field names, is switched off (`subTitle` with `show` false); keep one only when it adds something, such as the period or the unit. Source: checklist item 55; schema `visualConfiguration` 2.8.0 (`Title`, `SubTitle`). Code A003.
50. A title from a measure needs a text measure in the model, not a report-level measure. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-conditional-format-visual-titles.
51. Filters sit at three levels, each in `filterConfig`: report (`report.json`), page (`page.json`), visual (`visual.json`). Each filter in `filters[]` has `name`, `field`, `type`, `filter`, `howCreated`, `isHiddenInViewMode`, `isLockedInViewMode`; the order is `filterSortOrder`. Source: schema `filterConfiguration` 1.3.0. Inside `filter`, a field in a `Where` condition points to the alias that the `From` list declares (`SourceRef` with `Source`), never to the table name (`Entity`); otherwise the filter silently does nothing. Code V015 (warn). Source: Microsoft's skill, its file authoring/filters.md and authoring-part-04.md.
52. Lock a filter that readers may see but not change; hide a filter that only cleans data. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-report-filter.
53. Interactions are in `page.json` `visualInteractions[]`: `source`, `target`, `type` (`Default`, `DataFilter`, `HighlightFilter`, `NoFilter`). Line charts, scatter charts and maps can be filtered but not highlighted. Switch off any interaction that confuses the page. Source: schema `page` 2.1.0; https://learn.microsoft.com/en-us/power-bi/create-reports/service-reports-visual-interactions; checklist item 60.
54. Query reduction (checklist item 69):
   - Consider "Apply all slicers" when a page has 2 or more slicers changed together, or one slicer change refreshes 5 or more visuals. Auto page refresh under 30 seconds needs a written reason. Source: checklist item 69.
   - The button action types are `'ApplyAllSlicers'` and `'ClearAllSlicers'`. Source: Microsoft's skill, `button-part-03.md`.
   - Both act on every slicer on the page, not on the Filters pane; hiding the last Apply all button returns slicers to instant apply. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/buttons-apply-all-clear-all-slicers.
   - On a model with DirectQuery tables, Microsoft advises the query reduction options from the start; code U104 (note) names a page with two or more slicers and no Apply button setting. Source: https://learn.microsoft.com/en-us/power-bi/guidance/directquery-model-guidance.
   - Report-wide query reduction options are in `report.json` `slowDataSourceSettings`: `isSlicerSelectionsButtonEnabled`, `isFilterSelectionsButtonEnabled`, `isCrossHighlightingDisabled`, `isApplyAllButtonEnabled`, `isFieldWellButtonEnabled`. Auto page refresh is page `objects.pageRefresh`. Source: schemas `report` 3.3.0 and `page` 2.1.0.
- Copilot does: titles, filter cards and interactions in the files.
- Only Desktop shows: which interactions surprise readers, and how many visuals one slicer refreshes (Performance analyzer).

## J. Accessibility

Microsoft's report accessibility checklist, restated. Source of rules 55 to 62 unless named: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports.

55. Alt text on every visual that is not decoration, at most 250 characters, saying the takeaway (the reader already hears the title and type). It is `altText` in `visualContainerObjects.general`; for a group, in `visualGroup.objects.general`. Schemas `visualConfiguration` 2.8.0 and `visualContainer` 2.13.0. Codes A001 and A004 check visuals that show data and images; give a text box that carries meaning alt text too. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports
56. Tab order follows reading order (left to right, top to bottom), one number per visual: `position.tabOrder` (schema `visualContainer` 2.13.0). Code A002. After visuals move, are added or are removed, run `python scripts/set_tab_order.py .`: it sets the numbers to the reading order, without a yes. Microsoft's schema does not say whether the low or the high number comes first; the script follows the page's own numbers, and otherwise gives the top of the page the high numbers, as most of Microsoft's sample reports do (not confirmed from Microsoft). Ask the developer to look at View > Selection > Tab order once.
57. Titles in plain words, without jargon or acronyms (rule 49, A003).
58. Decorative shapes and images are kept out of the tab order. The files do not show it; ask the developer to check the Selection pane.
59. Text contrast at least 4.5 to 1 against its background (WCAG 2.1, criterion 1.4.3). Microsoft's skill adds 3 to 1 for large text and chart marks (its file accessibility.md). What the theme means for contrast is in `theme.md`, beside this file.
60. No meaning by colour alone (rule 37). Avoid hard pairs on one visual or page: green with red, brown, blue, grey or black; light green with yellow; blue with purple or grey.
61. Line, area, combo, scatter and bubble charts with several series: markers on, a different marker shape per series. Labels readable, but not every label and marker switched on. Marker property names are not confirmed: ask the developer to set them in Desktop, or copy them from a visual that has them.
62. Test bookmarks and navigation with the keyboard only. Set each visual's sort order on purpose: the accessible data table follows it.
- Only Desktop shows: real contrast, text sizes (checklist item 67) and what a screen reader says.

## K. Page density

63. Count the visuals that show data on each page: up to 8 is low, 9 to 12 normal, 13 to 16 review (V007, warn), more than 16 needs a written reason (V006, fail). A large table or matrix counts as 2: the script counts one twice when it covers a third of the page or more (this template's reading of the checklist's "dominant large"). Source: checklist item 20.
64. To lower the count, move detail to drillthrough pages and report page tooltips. Source: https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization.
- The script does not count hidden visuals or tooltip pages. A reason goes in section 10 of the brief with the code, the page and `-`.
- Only Desktop shows: how long the page takes to draw (Performance analyzer).

## L. Report-level measures and visual calculations

65. A report-level measure lives in the report, not the model: `definition/reportExtensions.json`, `entities[].measures[]` with `name`, `expression`, `dataType`, `formatString`, `description` and more (schema `reportExtension` 1.0.0). A report on a live connection can add only such measures. Source: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report; https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-report-lifecycle-datasets.
66. Put a measure in the model when other reports would use it, when it drives a title from a measure, or when it needs a dynamic format string; report-level measures support neither of the last two. Give report-level measures a prefix, such as an underscore, so a new model measure cannot clash with them. The prefix is an underscore (Microsoft's example), or the one the brief gives in section 4. A report-level measure without it gives V012 (warn). Source: https://learn.microsoft.com/en-us/power-bi/guidance/report-separate-from-model; desktop-conditional-format-visual-titles page; https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-dynamic-format-strings. Model changes go through the skill pbi-semantic-model.
67. A visual calculation lives on one visual, as a field in its query: `NativeVisualCalculation` with `Language`, `Expression`, `Name`, `DataType` (schema `semanticQuery` 1.4.0). It suits running sums, moving averages, percent of parent and comparisons with the previous item. It cannot be reused on another visual, is left out of data exports, and cannot be pinned or published to web; a field must be on the visual before it is used. Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-visual-calculations-overview.
68. Release status: generally available. Microsoft's release notes of May 2026 list "Visual calculations and custom totals (Generally Available)", and the visual calculation pages carry no preview label. Check a feature's page for a preview label before relying on it. Source: https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-latest-update-archive
- Only Desktop shows: whether the result is right.

## M. Resources and page titles

69. An image, or another resource a visual names (`ResourcePackageItem` with its `ItemName`), is a file in `StaticResources/RegisteredResources/` of the report folder, and is registered in `report.json` under `resourcePackages`, in the package of type `RegisteredResources`: an item whose `name` equals the `ItemName` and whose `path` is the file name. Copy the file in first, then register it. Code V017 (warn). Source: Microsoft's skill, its file authoring/image.md and `page-formatting.md`.
70. Give every page that is not a tooltip page a title: a text box at the top left, in the title band of the layout standard (`layout-standard.md`, beside this file). Readers start there. Microsoft's skill puts the title, the main figure or the main chart in that place, so a title is this template's default and not a rule of Microsoft's: code V018 is a note (a page with visuals and no text box). Source: Microsoft's skill, its file design/layout.md; `layout-standard.md`.
- Copilot does: copies and registers images, and writes the title text box.

## Suggesting a better native feature

- A suggestion is a note: a code that starts with U in the check output, and a line in the review.
- Never ask about a suggestion in the middle of a task; list it at the end.
- Copilot acts on a suggestion only after the developer's yes.
- A preview feature is marked as preview and also needs the developer's yes.
- The full list of native features, and when each fits, is in the file native-features.md of the skill pbi-checklist-review.

## Sources

Read on 11 November 2026. Restated in this template's own words; property names are copied exactly.

- Microsoft Learn: every page named with its full address in the rules above.
- Microsoft Learn, added for rules 30, 47 and 54: https://learn.microsoft.com/en-us/power-bi/guidance/composite-model-guidance ; https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-slicers ; https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-map-visualizations-overview ; https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-q-and-a ; https://learn.microsoft.com/en-us/power-bi/create-reports/script-visuals-overview ; https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-card ; https://learn.microsoft.com/en-us/power-bi/guidance/directquery-model-guidance
- Microsoft's report schemas (copies in `scripts/schemas`): `report` 3.3.0, `page` 2.1.0, `pagesMetadata` 1.1.0, `visualContainer` 2.13.0, `visualConfiguration` 2.8.0, `visualContainerMobileState` 2.8.0, `bookmark` 2.1.0, `bookmarksMetadata` 1.0.0, `filterConfiguration` 1.3.0, `formattingObjectDefinitions` 1.5.0, `semanticQuery` 1.4.0, `reportExtension` 1.0.0.
- microsoft/skills-for-fabric (MIT), skill powerbi-report-cli: its file field-parameters.md, `bookmark.md`, `button-part-02.md`, `button-part-03.md`, `slicers-part-02.md`, `authoring-workflows.md`; its file authoring-part-04.md; its file chart-selection.md, `interactivity.md`, `accessibility.md`; its files design/anti-patterns.md, design/layout.md, authoring/filters.md, authoring/image.md, authoring/page-formatting.md, authoring/card.md. The button action values come from here; the schema does not list them.
- `checklist/checklist.md`, items 20, 51, 53 to 67 and 69.
- Owner's rules: Header icons and Tooltips off unless section 7 of the brief lists the visual; `mobile.json` and `mobileState.json` never edited; the theme never changed and no styling on a single visual.

Where sources disagree, and what was decided:

- Microsoft recommends report page tooltips, and header icon text to help readers find drillthrough; Microsoft's skill keeps headers on unless a visual is decoration. The owner's rule keeps header icons and Tooltips off unless the brief lists the visual. The owner's rule stays; exceptions are per visual (section 7), and drill instructions go in text boxes.
- Visuals per page: the checklist reviews from 13 and asks a reason above 16; Microsoft's skill warns above 12; Microsoft Learn gives no number. The checklist's numbers are used (V006, V007).
- Colours in conditional formatting: Microsoft's skill writes colour codes as gradient stops and as fixed colours per measure. The owner's rule forbids colour codes on visuals: V009 warns, and a colour code needs a row in section 10. One exception, because a colour scale cannot use `ThemeDataColor`: inside a colour scale (`linearGradient2`, `linearGradient3`) the theme file's own colours may be written as codes: its data colours, `background`, `minimum`, `center`, `maximum` and `null`. V009 passes them. Which of them to use follows the meaning of the colour: `design.md`, beside this file, section 3.
- Sync groups: rule 31 (Microsoft's skill) says every slicer in a group uses the same column; Microsoft Learn syncs slicers on two copies of a dimension in a composite model (rule 30). Learn wins for that case.
- The script is narrower than its sources: A001 looks only at visuals that show data and at images, not at text boxes; V005 counts the hovered field among the 3, while item 65 asks for 3 beyond it, so a page that passes can still fall short; V003's limit (twice 320 x 240) and the "third of the page" in V006 and V007 are this template's own readings of "keep it small" and "dominant large".

Not confirmed from Microsoft: the `visualTooltip` `type` value for a report page tooltip; whether `acceptsFilterContext` is "Keep all filters"; the action value for "Bookmark navigation"; how a synced slicer that is not shown is stored; how "out of the tab order" is stored; marker property names; the `visualType` `qnaVisual`, which comes from Microsoft's report tool catalogue (`tests/fixtures/examples/INDEX.md`), not from Learn.

Checklist items: 20, 51, 53-67, 69
