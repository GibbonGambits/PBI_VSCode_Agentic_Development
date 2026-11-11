# Tooling, workflow and AI assistance

Part 2 of 3 of this topic. Covers: Query tracing and debugging; Reusable libraries and templates; AI assistants and agents.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### Query tracing and debugging

**T16-A123-3.** When the durations of the captured queries add up to clearly less than the time the page needs to refresh its visuals, consider the number and complexity of the visuals on the page as a possible cause.
- Consider. 2018. https://www.sqlbi.com/articles/capturing-power-bi-queries-using-dax-studio/
- When: Analysing a page's captured queries in DAX Studio, whose Duration column gives milliseconds per query.

**T16-A123-4.** Clear the cache before re-running a captured slow query in DAX Studio for performance optimisation.
- Should. 2018. https://www.sqlbi.com/articles/capturing-power-bi-queries-using-dax-studio/
- When: Tuning a long-running query copied from the All Queries list into the DAX Studio editor.

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

### Reusable libraries and templates

**T16-A311-1.** Look for model and report elements that can be reused many times and gather them in a library. Give priority to base objects first, then patterns, then visuals.
- Should. 2024. https://www.sqlbi.com/articles/using-atomic-design-in-report-and-model-development/
- When: Building several models or reports; atomic design is one structured way to organise this work.

**T16-A311-2.** Reusing building blocks of models and reports requires three steps: select the objects, patterns, visuals and reports worth reusing; store them in an easy-to-search library that keeps growing and tracks changes; and agree a simple way to apply the templates to new and existing work.
- Must. 2024. https://www.sqlbi.com/articles/using-atomic-design-in-report-and-model-development/
- When: Reusing modular parts (objects, patterns, visuals, pages or reports) in other models and reports.

**T16-A311-3.** Build recurring report elements, such as a title area, by copying them from a library of ready-made pieces instead of recreating them in every report.
- Should. 2024. https://www.sqlbi.com/articles/using-atomic-design-in-report-and-model-development/
- When: Most useful when fixed styles or functions, such as a help button to a central portal, apply to many reports.

**T16-A311-4.** Reusable model objects and patterns can be generated by scripts instead of copied by hand between files: DAX templates in Bravo (such as date tables with time intelligence measures), C# scripts saved as Tabular Editor macros, or Python in Fabric notebooks with semantic-link-labs.
- Option. 2024. https://www.sqlbi.com/articles/using-atomic-design-in-report-and-model-development/
- When: Adding stored model objects or patterns to a model; the approach more advanced users prefer.
- Version: As of 2024: DAX scripts need Tabular Editor 3; Fabric notebooks need a Fabric capacity and consume capacity units.

**T16-A311-5.** For a library of DAX objects and patterns that can be applied repeatably, a developer should script them in C# with Tabular Editor.
- Should. 2024. https://www.sqlbi.com/articles/using-atomic-design-in-report-and-model-development/
- When: Building a reusable library of DAX objects and patterns specifically.

**T16-A311-6.** The built-in quick measures of Power BI Desktop can be a starting point for self-service authors or for the most common patterns, but they are limited: the set cannot be customised, and some quick measures place requirements on the model.
- Option. 2024. https://www.sqlbi.com/articles/using-atomic-design-in-report-and-model-development/
- When: Choosing a source of ready-made measure patterns.

**T16-A311-9.** Catalogue reusable visuals in a dedicated, documented Power BI Desktop file, or several files that each show ways to display things such as actual versus target or trends, and keep them together with the theme files that hold fonts, colours and other styles.
- Should. Check. 2024. https://www.sqlbi.com/articles/using-atomic-design-in-report-and-model-development/
- When: Maintaining visual templates; applying them or their changes in bulk is possible but hard.
- Version: As of 2024, fields of a template visual can be swapped only with on-object interaction.

**T16-A311-14.** Keeping visual templates strict and consistent is an option that makes a page template easy to adapt: one visual can simply be swapped for another to suit particular users.
- Option. 2024. https://www.sqlbi.com/articles/using-atomic-design-in-report-and-model-development/
- When: A page template is adapted for specific users instead of being used unchanged.

**T16-A331-2.** Create the theme file at the start of report work and reuse its formatting across visuals and reports: this ranks among the highest-impact tasks. Theme files are complex and slow to write by hand; a dedicated design tool can help.
- Should. 2025. https://www.sqlbi.com/articles/tools-in-power-bi/
- When: Starting work on a report or a set of reports.

**T16-A366-4.** Move shared logic into a user-defined function also when just two measures repeat it and differ only in the last step: for example both build the same table variable, then one counts its rows and the other uses it as a CALCULATE filter.
- Should. 2026. https://www.sqlbi.com/articles/creating-dax-functions-with-ai-to-remove-duplicated-code/
- When: Measures compute the same intermediate result and use it differently at the end; AI-generated code sometimes needs this.

### AI assistants and agents

**T16-A331-5.** Besides DAX and Power Query code, generative AI tools can draft documentation content and suggest measure descriptions or translations; a person then corrects each suggestion.
- Option. 2025. https://www.sqlbi.com/articles/tools-in-power-bi/
- When: Building a model with AI help; in this template a description's meaning still comes from the brief or developer.
- Version: Named in 2025 for suggesting descriptions or translations: Copilot for Power BI, TMDL scripts, C# scripts in Tabular Editor.

**T16-A339-1.** The tools of an MCP server are code: an untrusted server could run code locally or misuse data. Before adopting an open-source or third-party server, a person should check and validate it carefully, above all one from a source they do not trust.
- Should. 2025. https://www.sqlbi.com/articles/ai-in-power-bi-time-to-pay-attention/
- When: Deciding which MCP servers an AI assistant may use; Microsoft's own, or self-built on Microsoft APIs, are regarded as safe.

**T16-A339-2.** Before users query a semantic model through today's conversational BI tools, the model must be prepared for AI, with significant effort: very specific naming conventions, a linguistic schema, AI instructions, and limits on the fields the AI can see and use.
- Must. 2025. https://www.sqlbi.com/articles/ai-in-power-bi-time-to-pay-attention/
- When: Users will ask questions through existing conversational BI tools; access through an MCP server may need less preparation.
- Version: State of 2025. AI instructions belong to Prep data for AI, a preview feature that needs the developer's yes.

**T16-A339-3.** When users query a model through an AI tool and an MCP server, you can have the tool ask clarifying questions before it uses fields, correct it to improve answers, and optionally add a server that gives it persistent memory of what it learns.
- Option. 2025. https://www.sqlbi.com/articles/ai-in-power-bi-time-to-pay-attention/
- When: The tool, the server and the host application are under the team's control.

**T16-A339-4.** Critical figures, such as current-month sales and performance against target, must be visible at a glance in a report or dashboard, so nobody has to ask a chat interface for them. The best and worst performing categories should usually be shown there too.
- Must. 2025. https://www.sqlbi.com/articles/ai-in-power-bi-time-to-pay-attention/
- When: Conversational BI is offered beside reports; it suits deeper or ad hoc exploration by trained users on well-built models.

**T16-A339-5.** Take into account the limits that language models bring to conversational BI: the same prompt and context can give different answers, generated code or text can be inaccurate or invented, and reliable usage patterns are not yet known.
- Consider. 2025. https://www.sqlbi.com/articles/ai-in-power-bi-time-to-pay-attention/
- When: Planning conversational BI; robust MCP server tools do not stop direct language model output from varying.

**T16-A343-2.** When working with AI applications, keep the project files under source control in a remote repository, such as GitHub or Azure DevOps Repos: a remote repository can be connected to those applications.
- Should. 2025. https://www.sqlbi.com/articles/introducing-ai-and-agentic-development-for-business-intelligence/
- When: Power BI project files are developed with AI applications.

**T16-A343-3.** When using AI for BI development, combine five building blocks instead of relying on one model, tool or feature: a language model that suits the scenario, sufficient but not excessive context, a well-written prompt, built-in or custom tools, and an environment managed for safety.
- Should. 2025. https://www.sqlbi.com/articles/introducing-ai-and-agentic-development-for-business-intelligence/
- When: Setting up AI-assisted BI development; models, tools and features change very quickly.

**T16-A343-4.** In agentic development, all context curated for the agent, meaning instructions, design documents and agent documents, must describe the business and technical situation accurately.
- Must. 2025. https://www.sqlbi.com/articles/introducing-ai-and-agentic-development-for-business-intelligence/
- When: Coding agents work on semantic models, reports or other BI artifacts.

**T16-A343-6.** A person must supervise and orchestrate agents closely, refining what they produce over several iterations and validating it.
- Must. Check. 2025. https://www.sqlbi.com/articles/introducing-ai-and-agentic-development-for-business-intelligence/
- When: Agents read and write project files and use tools to work on semantic models or reports.
- Version: Describes agents as they were in 2025.

**T16-A343-10.** Establish a mature development process before adding AI agents to BI work. AI layered on a process whose basics are not settled is unlikely to help and may make the mess more complicated.
- Must. 2025. https://www.sqlbi.com/articles/introducing-ai-and-agentic-development-for-business-intelligence/
- When: A team considers bringing AI agents into BI development.

**T16-A343-12.** Plan time and effort for learning about AI chat assistants and agents, configuring them and getting value from them, before expecting help with BI work.
- Must. 2025. https://www.sqlbi.com/articles/introducing-ai-and-agentic-development-for-business-intelligence/
- When: Adopting AI assistants or agents; they help people and teams in the right scenarios.

**T16-A366-2.** When asking AI for DAX code, state exactly what you want, so that the code can come out right at the first attempt.
- Should. 2026. https://www.sqlbi.com/articles/creating-dax-functions-with-ai-to-remove-duplicated-code/
- When: Authoring DAX code with AI.

**T16-A366-3.** AI does not use user-defined functions consistently, so whenever DAX is written or reviewed with AI, always check for places where a user-defined function could centralise code.
- Must. 2026. https://www.sqlbi.com/articles/creating-dax-functions-with-ai-to-remove-duplicated-code/
- When: Authoring or reviewing DAX code produced with AI.

**T16-A370-1.** Before writing any measure, however simple, write its contract first: a business-language document giving the rules that compute values in this specific model, free of obvious statements; it may cover several measures and algorithms. With an AI assistant this is the most important step.
- Should. 2026. https://www.sqlbi.com/articles/understanding-dax-contracts-when-using-ai/
- When: Developing a semantic model, in particular when writing DAX with an AI assistant.

**T16-A370-2.** Do not start by asking an AI assistant to write the measure. Start by asking which questions must be answered before the calculation can be written, and build the contract from that dialogue.
- Must. 2026. https://www.sqlbi.com/articles/understanding-dax-contracts-when-using-ai/
- When: Writing a new measure with an AI assistant.

**T16-A370-4.** The AI assistant can be asked to save the contract as a document, and not merely to apply it when writing the measure.
- Option. 2026. https://www.sqlbi.com/articles/understanding-dax-contracts-when-using-ai/
- When: Defining a contract with an AI assistant.

**T16-A370-5.** After an AI assistant has saved a contract, ask it to show the version it stored: the assistant keeps its own wording and structure, which probably differ from what you gave it.
- Should. 2026. https://www.sqlbi.com/articles/understanding-dax-contracts-when-using-ai/
- When: Defining a contract with an AI assistant.

**T16-A370-6.** To change how a measure behaves, one option is to edit its contract and ask AI to update the DAX code to match, instead of reviewing the code yourself. Contract rules need not be fixed up front; they can be refined by trial and error.
- Option. 2026. https://www.sqlbi.com/articles/understanding-dax-contracts-when-using-ai/
- When: A behaviour not considered at the start is discovered, or the measure must change later.

**T16-A370-7.** An AI agent can be used to check that all the code in a semantic model follows the rules written in its contract documentation.
- Option. 2026. https://www.sqlbi.com/articles/understanding-dax-contracts-when-using-ai/
- When: Semantic models whose calculations are documented in a contract.

**T16-A370-8.** A well-defined contract does not replace validation: carefully check a measure that AI generated from a contract before it goes into production.
- Should. 2026. https://www.sqlbi.com/articles/understanding-dax-contracts-when-using-ai/
- When: Measures written by AI from a contract.

**T16-A370-9.** A first contract may leave questions open. The AI assistant can point out the unresolved details and small inconsistencies it finds, and each is settled by adding a rule to the contract.
- Option. 2026. https://www.sqlbi.com/articles/understanding-dax-contracts-when-using-ai/
- When: Defining a contract with an AI assistant.

## Special-case techniques and facts

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

### Reusable libraries and templates

**T16-A311-7.** The rolling average quick measure relies on the date hierarchy that Power BI generates automatically. That hierarchy does not exist when Auto date/time is turned off in the application or file options.
- Fact. Check. 2024. https://www.sqlbi.com/articles/using-atomic-design-in-report-and-model-development/
- When: Using quick measures in a model where Auto date/time is off.
- Version: Stated in 2024; check the current quick measure.

**T16-A311-8.** Some reusable model patterns work only on data of a particular shape: currency conversion needs an exchange rate table plus source or target currency tables, each built in a set way. Applying a stored pattern therefore always takes human judgment.
- Fact. 2024. https://www.sqlbi.com/articles/using-atomic-design-in-report-and-model-development/
- When: Applying a stored pattern; a distinct calendar or several exchange rate types add to the adaptation.

**T16-A311-10.** A template visual placed in another report lets its fields be replaced only through on-object interaction. If the target model lacks a field it uses, the visual shows a grey error box until another field is chosen; its formatting is then kept.
- Fact. Check. 2024. https://www.sqlbi.com/articles/using-atomic-design-in-report-and-model-development/
- When: Reusing a template visual where the model lacks a referenced field; format painter or themes carry container formatting.
- Version: Behaviour described in 2024; check it in the current Power BI Desktop.

**T16-A311-11.** One option for cataloguing and distributing report layouts and report-wide formatting is the Power BI Template (.pbit) file. It holds model and report metadata, so it can also carry a theme, background images and common model patterns such as date tables and calculation groups.
- Option. 2024. https://www.sqlbi.com/articles/using-atomic-design-in-report-and-model-development/
- When: Sharing standard layouts or model patterns across reports.

**T16-A311-12.** Another option: a team can store each report definition as JSON in a remote repository and deploy it to a workspace through the Fabric REST APIs, optionally changing the definition by code on the way.
- Option. 2024. https://www.sqlbi.com/articles/using-atomic-design-in-report-and-model-development/
- When: A person or pipeline deploys reports from a repository; verify any change that code makes during deployment.
- Version: Described in 2024 for Microsoft Fabric, with Azure Repos or GitHub as example repositories.

**T16-A311-13.** When code changes report definitions during deployment, test the resulting report thoroughly to confirm that the changes had no unintended effect.
- Should. 2024. https://www.sqlbi.com/articles/using-atomic-design-in-report-and-model-development/
- When: Deploying report definitions programmatically and modifying them on the way.

**T16-A366-5.** One option to keep measures that share logic very short: a model-dependent user-defined function whose only parameter is the expression to compute, evaluated for the subset the function defines. A model-independent function taking the columns as arguments also works, but each call needs more arguments.
- Option. 2026. https://www.sqlbi.com/articles/creating-dax-functions-with-ai-to-remove-duplicated-code/
- When: Several measures share the same logic and differ only in what they compute.

### AI assistants and agents

**T16-A339-6.** Visuals produced by general chat tools built on language models are usually plain HTML and CSS over a static extract of model data, with at most minimal interactivity such as tooltips and animations.
- Fact. Check. 2025. https://www.sqlbi.com/articles/ai-in-power-bi-time-to-pay-attention/
- When: Comparing chat-generated visuals with report visuals.
- Version: Observed in 2025; check whether it still holds.

**T16-A339-7.** When an MCP server runs DAX queries and reads items through the Power BI and Fabric APIs under the user's own sign-in, those APIs enforce that user's permissions and data security rules.
- Fact. 2025. https://www.sqlbi.com/articles/ai-in-power-bi-time-to-pay-attention/
- When: The MCP server authenticates as the user.
- Version: In 2025 these APIs, executeQueries included, were said not to require a Fabric capacity.

**T16-A343-5.** Agents that edit Power BI metadata files such as TMDL or PBIR are prone to errors, for two reasons: such content is scarce in training data, and semantic models and reports are complex.
- Fact. Check. 2025. https://www.sqlbi.com/articles/introducing-ai-and-agentic-development-for-business-intelligence/
- When: An agent writes or changes project metadata files.
- Version: Stated in 2025; check whether it still holds.

**T16-A343-7.** AI agents do not build reports or semantic models on their own: most of the development work still falls to the person, and getting value from agents takes understanding and critical thinking.
- Fact. Check. 2025. https://www.sqlbi.com/articles/introducing-ai-and-agentic-development-for-business-intelligence/
- When: Setting expectations for agentic Power BI development.
- Version: State of 2025; agents were not expected to handle most end-to-end development soon.

**T16-A343-8.** With agents, a remote repository can also give the work its structure, and a person can automate deployment to a Fabric workspace for testing through Git integration, tools or custom methods.
- Option. 2025. https://www.sqlbi.com/articles/introducing-ai-and-agentic-development-for-business-intelligence/
- When: Organising agentic work on Power BI project files.

**T16-A343-9.** Agents that work asynchronously without supervision have few realistic uses beyond narrowly scoped tasks and reviews; the person reviews the result afterwards, typically as a pull request.
- Fact. Check. 2025. https://www.sqlbi.com/articles/introducing-ai-and-agentic-development-for-business-intelligence/
- When: Considering unattended, asynchronous agents for BI work.
- Version: Situation in 2025.

**T16-A343-11.** A basic AI chat assistant with minimal setup offers limited use and a higher risk of wasted time or errors: the DAX it generates can be wrong, and the user typically copies it into the model to test it.
- Fact. 2025. https://www.sqlbi.com/articles/introducing-ai-and-agentic-development-for-business-intelligence/
- When: Using a chat assistant without added context or tools; its output can still be a starting point for beginners.

**T16-A343-13.** Agents that are given command-line tools need more context than they would otherwise, in order to use those tools successfully.
- Fact. 2025. https://www.sqlbi.com/articles/introducing-ai-and-agentic-development-for-business-intelligence/
- When: Agents are set up with command-line tools beside built-in tools and MCP servers.

**T16-A370-3.** Before requesting a customer ranking measure, its contract should settle: who competes (all, selected, same group), which report filters apply, ranking direction, tie handling, treatment of blank, zero or negative amounts, what identifies a customer, and where it shows, including totals.
- Should. 2026. https://www.sqlbi.com/articles/understanding-dax-contracts-when-using-ai/
- When: Defining a ranking measure over customers with an AI assistant.

**T16-A370-10.** A customer ranking measure that an AI assistant wrote from a contract can probably be made more efficient by rewriting it with the RANK function.
- Option. 2026. https://www.sqlbi.com/articles/understanding-dax-contracts-when-using-ai/
- When: Reviewing a customer ranking measure generated by an AI assistant.
