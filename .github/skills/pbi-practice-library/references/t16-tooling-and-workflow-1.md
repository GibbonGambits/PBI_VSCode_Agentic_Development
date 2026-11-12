# Tooling, workflow and AI assistance

Part 1 of 2 of this topic. Covers: Scripting with TOM and APIs; Translations and renaming objects; Model edits with external tools; Query tracing and debugging; Choosing development tools.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### Scripting with TOM and APIs

**T16-A014-2.** Custom .NET code that queries an Analysis Services database should use the ADOMD.NET client library, not an OLE DB connection, for DAX, MDX and DMX alike: its command object accepts parameters and still returns results through a DataReader.
- Should. Check. 2012. https://www.sqlbi.com/articles/execute-dax-queries-through-ole-db-and-adomd-net/
- When: Your own .NET code sends DAX, MDX or DMX queries to an Analysis Services Tabular database.
- Version: In 2012 ADOMD.NET was a separate download in the SQL Server Feature Pack.

### Translations and renaming objects

**T16-A050-2.** Weigh a rename against clients outside the project too: an Excel PivotTable connected to the model drops the measures and columns renamed since its last refresh.
- Consider. Check. 2014. https://www.sqlbi.com/articles/frictionless-renaming-in-tabular-models-with-analysis-services/
- When: Renaming a table, column or measure of a model that Excel workbooks already use.
- Version: Written in 2014 for Power Pivot and Analysis Services Tabular, which then offered no rename refactoring.

### Query tracing and debugging

**T16-A123-7.** Report performance can be improved step by step by repeating one cycle: trace the page's queries, fix the measure behind the slowest query, then trace again.
- Option. 2018. https://www.sqlbi.com/articles/capturing-power-bi-queries-using-dax-studio/
- When: Optimising the DAX measures of a report page with query traces.

**T16-A123-9.** Every visual on a page sends its own DAX query. Once no captured query is slow and the measures cannot be improved further, showing fewer visuals is the remaining option for a faster page.
- Option. 2018. https://www.sqlbi.com/articles/capturing-power-bi-queries-using-dax-studio/
- When: A page whose queries all run quickly after DAX optimisation, for example in 20 milliseconds or less.

**T16-A265-2.** A measure can be debugged in a DAX query: run the visual's query, captured with Performance Analyzer, with a query-scoped definition of the measure, edit that query measure until right, and copy the fix into the model only after testing it in different queries.
- Option. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: Debugging a measure without touching the model or the reports; needs skill in shaping DAX queries.

**T16-A265-4.** To check a measure for one cell, a simpler option is a DAX query that evaluates it inside a table constructor wrapped in CALCULATETABLE with the cell's filter conditions. More measures can join the table constructor to be seen under the same filter context.
- Option. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: The measure's logic does not depend on the shadow filter context that ALLSELECTED reads from the report query.

**T16-A265-8.** EVALUATEANDLOG calls slow down report execution, so every one of them must be removed from the measures as soon as the investigation is over.
- Must. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: Measures that were instrumented with EVALUATEANDLOG for debugging.

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

**T16-A353-5.** Once debugging is finished, put back the measure's own RETURN expression: the TOCSV or TOJSON call served only to inspect a value for a while and never belonged to the measure's logic.
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

**T16-A353-11.** When it matters which rows appear, pick them yourself before passing the table to TOCSV or TOJSON, for example with TOPN and the sort order needed: both emit rows in engine order, which may vary. TOPN does not sort its output; CONCATENATEX can.
- Should. 2026. https://www.sqlbi.com/articles/debugging-dax-variables-using-tojson-and-tocsv/
- When: Debugging with TOCSV or TOJSON when it matters which rows appear.

### Choosing development tools

**T16-A221-1.** Decide at the very start of a project whether the Tabular model is built in Power BI Desktop or in Visual Studio: a project cannot move from one of these two to the other later.
- Should. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Starting a Tabular model project with Microsoft tools.
- Version: Describes the tools as of 2021.

**T16-A221-18.** Do not expect one all-in-one tool. For each need, select the tools that reach the required model features most productively: no single monolithic tool serves model authors, report authors and business users alike.
- Should. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Assembling the toolset for model authors, report authors and business users.

**T16-A221-19.** Starting a Tabular project in Visual Studio (Analysis Services Projects) can open more features shared with Analysis Services, such as custom partitions. In return, Power BI-specific features such as Incremental Refresh are out of reach, and Power BI Desktop cannot edit the deployed model.
- Option. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Choosing the authoring tool at the start of a Tabular project for Analysis Services or Power BI Premium.
- Version: Describes the tools as of 2021.

**T16-A331-3.** No tool is mandatory; pick one for a specific model task. Power BI's own include DAX query view, TMDL view, Performance Analyzer and Analyze in Excel; VS Code edits the project files.
- Option. 2025. https://www.sqlbi.com/articles/tools-in-power-bi/
- When: Choosing a tool for model design, DAX debugging, optimisation, testing or bulk changes.

## Special-case techniques and facts

### Scripting with TOM and APIs

**T16-A014-1.** A .NET program that sends a DAX query through the OLE DB classes with the MSOLAP provider fails with an error as soon as a command parameter is attached to the query. The only known way around it is ADOMD.NET.
- Fact. Check. 2012. https://www.sqlbi.com/articles/execute-dax-queries-through-ole-db-and-adomd-net/
- When: Custom .NET code running parameterised DAX queries on Analysis Services over an OLE DB connection.
- Version: Reported in 2012 as an unfixed defect of the .NET OLE DB assembly; check whether it still applies.

**T16-A084-5.** Although a measure name is unique in the whole model, each measure belongs to one table, and that home table influences Q&A semantics in Power BI and drillthrough behaviour in Excel.
- Fact. 2016. https://www.sqlbi.com/articles/adding-a-measure-to-a-tabular-model/
- When: Judging what the home table of a measure changes for client tools.
- Version: Stated in 2016. This template keeps every measure in one measures table (model standard rule 1). This template changes a model only in its files, never through a server or a library.

**T16-A205-2.** Token-acquisition code is not enough. The application must also be registered and configured in Azure Active Directory, API permissions included, so that the service principal the code relies on exists and is authorised.
- Must. Check. 2020. https://www.sqlbi.com/articles/creating-a-service-principal-account-for-power-bi-api/
- When: An application uses a service principal to obtain an access token for the Power BI API.
- Version: Written in 2020 under the name Azure Active Directory.

**T16-A205-3.** The Power BI API does not authenticate callers itself. A service principal gets its access token from Azure Active Directory services, reached through separate libraries such as the Microsoft Authentication Library (MSAL).
- Fact. Check. 2020. https://www.sqlbi.com/articles/creating-a-service-principal-account-for-power-bi-api/
- When: Building an application that calls the Power BI API under a service principal identity.
- Version: Written in 2020 under the name Azure Active Directory.

### Translations and renaming objects

**T16-A050-3.** Translations can serve as a renaming layer: build the model in a language no user works in, or add a translation for the model's own locale, and set the user-facing names there. Clients show the translated names; DAX and MDX queries keep the originals.
- Option. Check. 2014. https://www.sqlbi.com/articles/frictionless-renaming-in-tabular-models-with-analysis-services/
- When: User-facing names must change without editing DAX; possibly unsupported by Microsoft, so test first and accept the risk.
- Version: 2014 technique for Analysis Services Tabular, not Power Pivot. This template uses default-language translations sparingly (multiple languages, rule 3).

**T16-A081-3.** Save a Tabular translation file as Unicode UTF-8, the encoding the export writes and the import expects. In Visual Studio set it explicitly with Save with Encoding (Advanced Save Options): a JSON file with no character above code 127 is otherwise saved as ANSI.
- Must. Check. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: Editing JSON translation files of an Analysis Services Tabular model.
- Version: Visual Studio behaviour as described in 2016.

**T16-A081-4.** An Excel PivotTable whose connection string forces a specific culture shows translated metadata and so can check Tabular translations; Analyze in Excel in Visual Studio lets you choose that culture.
- Must. Check. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: Testing metadata translations of an Analysis Services Tabular model.
- Version: In July 2016 Excel was the only Microsoft client showing Tabular translations; Power BI live connections did not.

**T16-A081-5.** Translate hidden objects as well. The translation file lists every object whatever its visibility, although hidden objects are never displayed to users, so this is not strictly needed.
- Should. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: Translating the metadata of an Analysis Services Tabular model.

**T16-A081-6.** Export each language to a translation file of its own. Several languages in one file can become complex to handle, above all without a dedicated editor.
- Should. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: Exporting translation files from an Analysis Services Tabular model.

**T16-A081-7.** Do not rename model objects once a translation file has been exported: importing a translation that names a since-renamed object fails. If a rename happened anyway, repeat it inside the translation file or restore the original name before the import.
- Should. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: A translation file has been exported from an Analysis Services Tabular model.

**T16-A081-8.** Leave the translation of model metadata to the very end of the project. Objects created after an export are not translated by the import, a new export always holds every object, and partial translations cannot be merged.
- Should. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: Projects that translate Analysis Services Tabular metadata through exported translation files.

**T16-A081-10.** A translation file is plain text, so no particular tool is needed: it can be edited in any text editor that handles UTF-8, or through a script of your own that turns the JSON into a simpler format.
- Option. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: Editing JSON translation files exported from an Analysis Services Tabular model, outside Visual Studio.

### Model edits with external tools

**T16-A110-1.** A Power BI Desktop model takes its culture from the operating system locale when the file is created, and the user interface cannot change it. Regional Settings in Options change only query behaviour, not the formatting that DAX functions such as FORMAT produce.
- Fact. Check. 2017. https://www.sqlbi.com/articles/changing-the-culture-of-a-power-bi-desktop-file/
- When: DAX formatting must follow a culture other than that of the machine that created the file.
- Version: Stated in 2017; check whether current Power BI Desktop still behaves this way.

**T16-A110-3.** Before changing a Power BI Desktop file's culture by editing its template outside Power BI, always keep a backup copy of every file you modify: the procedure alters an undocumented file at your own risk.
- Must. 2017. https://www.sqlbi.com/articles/changing-the-culture-of-a-power-bi-desktop-file/
- When: Editing a Power BI template file outside Power BI to change the model culture.

**T16-A110-4.** A culture change made through a template cannot keep the data already loaded. The edited template holds no data, so the new model must be processed again by reading the data sources.
- Fact. 2017. https://www.sqlbi.com/articles/changing-the-culture-of-a-power-bi-desktop-file/
- When: Changing the model culture of a Power BI Desktop file through a template.

**T16-A200-1.** A KPI defined on the measure is one option: Excel, through Analyze in Excel, and every Power BI visual reuse it with identical properties, whereas indicators built from extra measures and conditional formatting take much effort and must be redone for Excel.
- Option. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: A measure needs a goal-based status and a trend indicator in both Power BI and Excel.
- Version: Power BI Desktop models accept KPIs since July 2020; earlier only Analysis Services or Premium models.

**T16-A200-2.** Turning a measure into a KPI replaces it in the Fields pane: Power BI lists the KPI, with Trend added when one is defined, instead of the measure. The original measure stays usable in DAX code and serves as the KPI Value.
- Fact. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: A KPI is created on top of an existing measure.

**T16-A200-5.** The Status expression of a KPI must return an integer that matches one state of the chosen graphic, for example -1, 0 and 1 for bad, average and good on a traffic light. The Trend expression is technically another status and follows the same pattern.
- Must. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: Defining the Status or Trend expression of a KPI.

**T16-A200-6.** A KPI generates measures named after the base measure, with a leading underscore and a Goal, Status or Trend suffix. They behave as ordinary measures, so DAX can reference them, for instance the goal measure inside the Status expression.
- Option. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: Writing DAX that needs the goal, status or trend of a KPI.

**T16-A200-7.** If the Trend property of a new KPI does not show in Power BI Desktop, collapse and re-expand the Fields pane to force the field list to refresh.
- Must. Check. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: Trend is missing from the KPI in the Fields pane after the KPI was saved to the model.
- Version: Seen in 2020; check whether current Power BI Desktop still needs it.

**T16-A200-8.** Rename the KPI Value, Status and Trend fields inside the visual that shows them: the generated names are long, waste space in the visual headers and cannot be changed in the model.
- Should. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: Report visuals that display KPI properties.

**T16-A200-9.** Beyond the basic steps of building a KPI, three areas need a closer look before you rely on one: the graphics available, the numeric values that Status and Trend return, and how a KPI behaves when the model also has calculation groups.
- Consider. Check. 2020. https://www.sqlbi.com/articles/creating-kpis-in-power-bi-desktop/
- When: Designing KPI Status and Trend graphics and values, or using KPIs beside calculation groups.

**T16-A232-1.** One way to give an ordinary numeric column the slicer Single Value option of New Parameter columns: add to the column an extended property named ParameterMetadata whose value is the JSON text `{"version":0}`, then save the model.
- Option. Check. 2021. https://www.sqlbi.com/articles/how-to-enable-the-single-value-option-in-a-power-bi-slicer/
- When: A slicer on your own numeric column should offer Single Value; unsupported by Microsoft, so back up first.
- Version: Described in 2021. The project check reads a column with this property as a field parameter (M822): expect that finding.

**T16-A232-2.** Always back up the Power BI file before adding the ParameterMetadata extended property to a column: the change is not supported by Microsoft and is made at your own risk.
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

**T16-A123-1.** Before capturing a page's DAX queries with a trace, add an empty page, save the file with that page active, then close and reopen Power BI Desktop: no query then runs, and the cache is empty, until you move to another page.
- Should. 2018. https://www.sqlbi.com/articles/capturing-power-bi-queries-using-dax-studio/
- When: Collecting every DAX query that one report page sends to the engine.

**T16-A123-8.** The order in which a report's queries appear in a trace can change from one run to the next, particularly when their durations change.
- Fact. 2018. https://www.sqlbi.com/articles/capturing-power-bi-queries-using-dax-studio/
- When: Comparing traces of the same report before and after an optimisation.

**T16-A265-5.** A DAX query that tests a measure relying on ALLSELECTED must group with SUMMARIZECOLUMNS, as the query captured from the report visual does: SUMMARIZECOLUMNS keeps the shadow filter context that ALLSELECTED depends on in the report.
- Must. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: Debugging a measure that contains ALLSELECTED outside the report, with a DAX query.

**T16-A265-7.** EVALUATEANDLOG wrapped around a sub-expression logs its value and still returns it; the optional label argument tells the logged expressions apart. The log is read outside the report, and reading it calls for deep knowledge of the way the engine works out a measure.
- Option. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: Inspecting an intermediate value or temporary table inside a measure; other techniques are quicker in common cases.

**T16-A265-9.** An EVALUATEANDLOG log entry does not match one report cell. The engine evaluates a measure for all combinations of the same granularity in one step, so an entry can hold a whole table of values that must be mapped to cells through the report query.
- Fact. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: Reading the DAX evaluation log that EVALUATEANDLOG produces for a measure used in a visual.

**T16-A265-13.** To compare a value with the same items over all periods selected in the report, apply ALLSELECTED to the Date table only. With no argument, ALLSELECTED removes every grouping filter of the query, other tables included, and returns one value for all rows.
- Must. 2023. https://www.sqlbi.com/articles/debugging-dax-measures-in-power-bi/
- When: A ratio against all selected periods, in a visual grouped by date and by another table.

**T16-A353-7.** For an empty table TOJSON returns nothing, while TOCSV still returns the column names. TOJSON is therefore a poor way to inspect a table that may turn out to be empty.
- Fact. 2026. https://www.sqlbi.com/articles/debugging-dax-variables-using-tojson-and-tocsv/
- When: Debugging table variables that may contain no rows.

### Choosing development tools

**T16-A221-2.** A Tabular model built in Visual Studio cannot be opened in Power BI Desktop, whether it reached Power BI Premium from Visual Studio or from an Analysis Services backup. Desktop-only features such as Incremental Refresh stay out of reach.
- Fact. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Moving an Analysis Services model, or one developed in Visual Studio, to Power BI Premium.
- Version: Stated in 2021; restoring an Analysis Services backup into Premium was announced from April 2021.

**T16-A221-11.** Visual Studio's relationship editor gives a many-to-many cardinality relationship a Both filter direction and offers no way to change it. Power BI Desktop can change it; for a Visual Studio model, edit model.bim by hand.
- Fact. Check. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: A model edited with Visual Studio needs a relationship of many-to-many cardinality.
- Version: Reported in 2021; many-to-many cardinality relationships exist since Analysis Services 2019.

**T16-A221-15.** In Visual Studio, prefer the integrated workspace to a separate Analysis Services workspace instance. Visual Studio keeps the workspace in step with every edit, so the workspace should sit close to the editor to keep latency low.
- Should. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Developing a Tabular model in Visual Studio.
