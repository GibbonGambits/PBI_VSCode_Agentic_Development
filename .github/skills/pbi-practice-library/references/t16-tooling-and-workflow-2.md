# Tooling, workflow and AI assistance

Part 2 of 3 of this topic. Covers: Model edits with external tools; Query tracing and debugging.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### Query tracing and debugging

**T16-A123-3.** When the durations of the captured queries add up to clearly less than the time the page needs to refresh its visuals, consider the number and complexity of the visuals on the page as a possible cause.
- Consider. 2018. https://www.sqlbi.com/articles/capturing-power-bi-queries-using-dax-studio/
- When: Analysing a page's captured queries in DAX Studio, whose Duration column gives milliseconds per query.

**T16-A123-7.** Report performance can be improved step by step by repeating one cycle: trace the page's queries, fix the measure behind the slowest query, then trace again.
- Option. 2018. https://www.sqlbi.com/articles/capturing-power-bi-queries-using-dax-studio/
- When: Optimising the DAX measures of a report page with DAX Studio traces.

**T16-A123-9.** Every visual on a page sends its own DAX query. Once no captured query is slow and the measures cannot be improved further, showing fewer visuals is the remaining option for a faster page.
- Option. 2018. https://www.sqlbi.com/articles/capturing-power-bi-queries-using-dax-studio/
- When: A page whose queries all run quickly after DAX optimisation, for example in 20 milliseconds or less.

**T16-A265-2.** A measure can be debugged in DAX Studio: run the visual's query, captured with Performance Analyzer, with a query-scoped definition of the measure, edit that query measure until it is right, and copy the fix into the model only after testing it in different queries.
- Option. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: Debugging a measure without touching the model or the reports; needs skill in shaping DAX queries.

**T16-A265-3.** A measure fixed and validated as a query measure in DAX Studio must still be corrected in the model itself, in Power BI Desktop: DAX Studio cannot change the structure or the data of the model it analyses.
- Must. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: Debugging a measure in DAX Studio with a query-scoped measure definition.

**T16-A265-4.** To check a measure for one cell, a simpler option is a DAX Studio query that evaluates it inside a table constructor wrapped in CALCULATETABLE with the cell's filter conditions. More measures can join the table constructor to be seen under the same filter context.
- Option. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: The measure's logic does not depend on the shadow filter context that ALLSELECTED reads from the report query.

**T16-A265-8.** EVALUATEANDLOG calls slow down report execution, so every one of them must be removed from the measures as soon as the investigation is over.
- Must. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: Measures that were instrumented with EVALUATEANDLOG for debugging.

**T16-A265-11.** Tabular Editor 3 can debug a measure cell by cell: run a DAX query that uses the measure, such as a visual's query captured with Performance Analyzer, choose Debug cell on a result cell, and step through the expression, watching evaluation context and intermediate values.
- Option. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: Investigating a wrong measure result; the debugger starts from a DAX query that runs the measure.
- Version: The DAX Debugger is a feature of Tabular Editor 3.

**T16-A353-1.** One way to debug a measure with a wrong number: build it as a chain of variables ending in a Result variable, then temporarily return an intermediate variable so its value shows in the report and can be compared with the expected one.
- Option. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/ ; https://www.sqlbi.com/articles/debugging-dax-variables-using-tojson-and-tocsv/
- When: Debugging a measure that returns wrong numbers; several levels of nested measures may need test reports instead.

**T16-A353-2.** To see a table variable while debugging, a measure can temporarily return TOCSV or TOJSON of that variable. Both turn the table into text a visual can show, without listing columns or a format as a custom CONCATENATEX would require.
- Option. 2026. https://www.sqlbi.com/articles/debugging-dax-variables-using-tojson-and-tocsv/
- When: Debugging a measure with intermediate table variables, inside Power BI without another tool.

**T16-A353-3.** Place a debugging measure that shows a table variable as text in a matrix, not a card: the content then appears in the very cell whose result is wrong, without rebuilding that cell's filters with slicers and the filter pane.
- Should. 2026. https://www.sqlbi.com/articles/debugging-dax-variables-using-tojson-and-tocsv/
- When: A measure is wrong only in specific matrix cells, such as one year and category, or a subtotal.

**T16-A353-4.** When a measure builds its result through several table variables, the faulty step can be found without guessing: return each variable in turn through TOCSV or TOJSON, confirm its content, and move on until the step that goes wrong appears.
- Option. 2026. https://www.sqlbi.com/articles/debugging-dax-variables-using-tojson-and-tocsv/
- When: A multi-step measure, each step in a variable, does not return the expected result.

**T16-A353-5.** Once debugging is finished, restore the measure's original RETURN expression: the TOCSV or TOJSON call was a temporary inspection aid and never part of the measure's logic.
- Should. 2026. https://www.sqlbi.com/articles/debugging-dax-variables-using-tojson-and-tocsv/
- When: After a measure's RETURN was changed temporarily to display an intermediate variable.

**T16-A353-6.** TOCSV tends to suit a quick visual look, as its output is compact; TOJSON suits cases that need the source table's row count or output pasted into another tool, as its structure is fixed. Otherwise the choice is mostly taste and readability.
- Option. 2026. https://www.sqlbi.com/articles/debugging-dax-variables-using-tojson-and-tocsv/
- When: Choosing a function to display a table variable as text while debugging.

**T16-A353-8.** TOCSV and TOJSON return only 10 rows by default. Their MaxRows argument can be raised when the problem shows only further down the intermediate table, or when all of its content must be checked.
- Option. 2026. https://www.sqlbi.com/articles/debugging-dax-variables-using-tojson-and-tocsv/
- When: Displaying a table variable as text with TOCSV or TOJSON while debugging.

**T16-A353-9.** Be careful about raising MaxRows of TOCSV or TOJSON by much: a very long text may be cut off by the visual and the measure can take longer. For most debugging sessions 10 to 20 rows is a sensible range.
- Consider. 2026. https://www.sqlbi.com/articles/debugging-dax-variables-using-tojson-and-tocsv/
- When: Displaying a table variable as text with TOCSV or TOJSON while debugging.

**T16-A353-10.** To examine an intermediate table of many hundreds or thousands of rows, consider DAX Studio or Tabular Editor 3 instead of showing it as text with TOCSV or TOJSON in a report: those tools suit exploring large amounts of data.
- Consider. 2026. https://www.sqlbi.com/articles/debugging-dax-variables-using-tojson-and-tocsv/
- When: Debugging a measure whose intermediate table is too large to read as text in a visual.
- Version: Tabular Editor 3 is commercial and has a step-by-step DAX debugger; DAX Studio is free.

**T16-A353-11.** When row order matters, sort the table yourself before passing it to TOCSV or TOJSON, for example with TOPN: both emit rows in engine order, which may not be deterministic. TOPN picks the rows without sorting the output; CONCATENATEX can sort, with extra arguments.
- Should. 2026. https://www.sqlbi.com/articles/debugging-dax-variables-using-tojson-and-tocsv/
- When: Debugging with TOCSV or TOJSON when it matters which rows appear.

## Special-case techniques and facts

### Model edits with external tools

**T16-A110-1.** A Power BI Desktop model takes its culture from the operating system locale when the file is created, and the user interface cannot change it. Regional Settings in Options change only query behaviour, not the formatting that DAX functions such as FORMAT produce.
- Fact. Check. 2017. https://www.sqlbi.com/articles/changing-the-culture-of-a-power-bi-desktop-file/
- When: DAX formatting must follow a culture other than that of the machine that created the file.
- Version: Stated in 2017; check whether current Power BI Desktop still behaves this way.

**T16-A110-2.** One way to change a model's culture: save the report as a .pbit template, open it in Tabular Editor with unsupported Power BI features allowed, set the model's culture property, save, and open the template in Power BI, which builds a new model.
- Option. Check. 2017. https://www.sqlbi.com/articles/changing-the-culture-of-a-power-bi-desktop-file/
- When: The culture inherited from the creating machine is wrong; an undocumented edit at your own risk.
- Version: Tabular Editor replaced an earlier text-editor approach in April 2018.

**T16-A110-3.** Before changing a Power BI Desktop file's culture by editing its template outside Power BI, always keep a backup copy of every file you modify: the procedure alters an undocumented file at your own risk.
- Must. 2017. https://www.sqlbi.com/articles/changing-the-culture-of-a-power-bi-desktop-file/
- When: Editing a Power BI template file with Tabular Editor to change the model culture.

**T16-A110-4.** A culture change made through a template cannot keep the data already loaded. The edited template holds no data, so the new model must be processed again by reading the data sources.
- Fact. 2017. https://www.sqlbi.com/articles/changing-the-culture-of-a-power-bi-desktop-file/
- When: Changing the model culture of a Power BI Desktop file through a template.

**T16-A200-1.** A KPI defined on the measure is one option: Excel, through Analyze in Excel, and every Power BI visual reuse it with identical properties, whereas indicators built from extra measures and conditional formatting take much effort and must be redone for Excel.
- Option. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: A measure needs a goal-based status and a trend indicator in both Power BI and Excel.
- Version: Power BI Desktop models accept KPIs through external tools since July 2020; earlier only Analysis Services or Premium models.

**T16-A200-2.** Turning a measure into a KPI replaces it in the Fields pane: Power BI lists the KPI, with Trend added when one is defined, instead of the measure. The original measure stays usable in DAX code and serves as the KPI Value.
- Fact. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: A KPI is created on top of an existing measure.

**T16-A200-3.** A KPI can be built in Tabular Editor, started from the External Tools ribbon: right-click the measure, choose Create New, KPI, then give Status and Trend a description, expression and graphic, and Target an expression and format string. Power BI shows Target as Goal.
- Option. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: Creating a KPI directly in a Power BI Desktop model.
- Version: Relies on the External Tools support of Power BI Desktop, July 2020 version or later.

**T16-A200-4.** After changing a KPI in Tabular Editor, save the project there, from the menu or with Ctrl+S. Power BI Desktop is updated only by that save, which is what pushes the KPI into it.
- Must. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: Editing a Power BI Desktop model through Tabular Editor as an external tool.

**T16-A200-5.** The Status expression of a KPI must return an integer that matches one state of the chosen graphic, for example -1, 0 and 1 for bad, average and good on a traffic light. The Trend expression is technically another status and follows the same pattern.
- Must. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: Defining the Status or Trend expression of a KPI.

**T16-A200-6.** A KPI generates measures named after the base measure, with a leading underscore and a Goal, Status or Trend suffix. They behave as ordinary measures, so DAX can reference them, for instance the goal measure inside the Status expression.
- Option. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: Writing DAX that needs the goal, status or trend of a KPI.

**T16-A200-7.** If the Trend property of a new KPI does not show in Power BI Desktop, collapse and re-expand the Fields pane to force the field list to refresh.
- Must. Check. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: Trend is missing from the KPI in the Fields pane after saving the KPI from Tabular Editor.
- Version: Seen in 2020; check whether current Power BI Desktop still needs it.

**T16-A200-8.** Rename the KPI Value, Status and Trend fields inside the visual that shows them: the generated names are long, waste space in the visual headers and cannot be changed in the model.
- Should. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: Report visuals that display KPI properties.

**T16-A200-9.** When building KPIs, be aware that three areas carry further important details beyond the basic steps: the graphics available, the numeric values Status and Trend return, and how a KPI behaves when the model also has calculation groups.
- Consider. Check. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: Designing KPI Status and Trend graphics and values, or using KPIs beside calculation groups.

**T16-A232-1.** One way to give an ordinary numeric column the slicer Single Value option of New Parameter columns: in Tabular Editor, add to the column an extended property named ParameterMetadata whose value is the JSON text `{"version":0}`, then save the model.
- Option. Check. 2021. https://www.sqlbi.com/articles/how-to-enable-the-single-value-option-in-a-power-bi-slicer/
- When: A slicer on your own numeric column should offer Single Value; unsupported by Microsoft, so back up first.
- Version: Described in 2021; the steps are the same in the free and commercial Tabular Editor.

**T16-A232-2.** Always back up the Power BI file before adding the ParameterMetadata extended property to a column with Tabular Editor: the change is not supported by Microsoft and is made at your own risk.
- Should. 2021. https://www.sqlbi.com/articles/how-to-enable-the-single-value-option-in-a-power-bi-slicer/
- When: Adding the ParameterMetadata extended property to enable the slicer Single Value option.

**T16-A232-3.** The ParameterMetadata extended property enables the slicer Single Value option for numeric columns only; on a date column the option does not appear.
- Fact. Check. 2021. https://www.sqlbi.com/articles/how-to-enable-the-single-value-option-in-a-power-bi-slicer/
- When: Using the ParameterMetadata extended property to get Single Value in a slicer.
- Version: Observed in 2021; check current behaviour.

**T16-A232-4.** Be careful about changing a column's data type after the ParameterMetadata extended property has been added to it: the change may harm how the slicer behaves.
- Consider. 2021. https://www.sqlbi.com/articles/how-to-enable-the-single-value-option-in-a-power-bi-slicer/
- When: A column carries the ParameterMetadata extended property for the slicer Single Value option.

### Query tracing and debugging

**T16-A123-1.** Before capturing a page's DAX queries with DAX Studio, add an empty page, save the file with that page active, then close and reopen Power BI Desktop: no query then runs, and the cache is empty, until you move to another page.
- Should. 2018. https://www.sqlbi.com/articles/capturing-power-bi-queries-using-dax-studio/
- When: Collecting every DAX query that one report page sends to the engine.

**T16-A123-2.** Connect DAX Studio to the open Power BI Desktop model while the empty page is shown, start the All Queries trace, and confirm in the Output pane that the trace has started before switching to the page to analyse.
- Must. Check. 2018. https://www.sqlbi.com/articles/capturing-power-bi-queries-using-dax-studio/
- When: Capturing the DAX queries a Power BI Desktop report page generates.
- Version: DAX Studio interface as described in 2018.

**T16-A123-5.** To isolate the queries a slicer selection causes in a DAX Studio trace, either note the StartTime of the last captured query, or empty the list with Clear All, before clicking the slicer.
- Option. Check. 2018. https://www.sqlbi.com/articles/capturing-power-bi-queries-using-dax-studio/
- When: Capturing the queries generated by interaction with one or more slicers.
- Version: DAX Studio interface as described in 2018.

**T16-A123-8.** The order in which a report's queries appear in a trace can change from one run to the next, particularly when their durations change.
- Fact. 2018. https://www.sqlbi.com/articles/capturing-power-bi-queries-using-dax-studio/
- When: Comparing DAX Studio traces of the same report before and after an optimisation.

**T16-A265-5.** A DAX query that tests a measure relying on ALLSELECTED must group with SUMMARIZECOLUMNS, as the query captured from the report visual does: SUMMARIZECOLUMNS keeps the shadow filter context that ALLSELECTED depends on in the report.
- Must. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: Debugging a measure that contains ALLSELECTED outside the report, with a DAX query.

**T16-A265-6.** DAX Studio shows query results without the measure's format string, so a percentage appears as a plain decimal number. Putting a % symbol in the result column name makes DAX Studio show the column as a percentage.
- Option. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: Reading percentage measures in DAX Studio query results.

**T16-A265-7.** EVALUATEANDLOG wrapped around a sub-expression logs its value and still returns it; the optional label argument tells the logged expressions apart. The log is read in an external tool, and reading it calls for deep knowledge of the way the engine works out a measure.
- Option. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: Inspecting an intermediate value or temporary table inside a measure; other techniques are quicker in common cases.
- Version: In 2023 the evaluation log was shown with SQL Server Profiler or DAX Debug Output.

**T16-A265-9.** An EVALUATEANDLOG log entry does not match one report cell. The engine evaluates a measure for all combinations of the same granularity in one step, so an entry can hold a whole table of values that must be mapped to cells through the report query.
- Fact. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: Reading the DAX evaluation log that EVALUATEANDLOG produces for a measure used in a visual.

**T16-A265-10.** Connect DAX Debug Output to the Power BI Desktop instance before opening the report page whose measures use EVALUATEANDLOG. If the page is already shown, Refresh visuals in the Performance Analyzer pane runs the queries again so the log is captured.
- Should. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: Capturing the DAX evaluation log of a Power BI Desktop report with DAX Debug Output.

**T16-A265-12.** The Evaluation Context window of the Tabular Editor 3 DAX Debugger lists the stack of applied filters, innermost on top. A filter shown in the stack is not necessarily active: a later directive in the stack may remove it.
- Fact. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: Reading the evaluation context while stepping through a measure in the Tabular Editor 3 DAX Debugger.
- Version: Version 3.4 did not strike through filters ALLSELECTED removed; the filter checkboxes showed which ones it ignores.

**T16-A265-13.** To compare a value with the same items over all periods selected in the report, apply ALLSELECTED to the Date table only. With no argument, ALLSELECTED removes every grouping filter of the query, other tables included, and returns one value for all rows.
- Must. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: A ratio against all selected periods, in a visual grouped by date and by another table.

**T16-A353-7.** For an empty table TOJSON returns nothing, while TOCSV still returns the column names. TOJSON is therefore a poor way to inspect a table that may turn out to be empty.
- Fact. 2026. https://www.sqlbi.com/articles/debugging-dax-variables-using-tojson-and-tocsv/
- When: Debugging table variables that may contain no rows.
