# The model standard

One fixed standard for every model built from this template, so that models look the same over time and across projects. `python scripts/check_project.py .` checks it; the code after each rule is the finding it gives. "Item" is the checklist item a rule supports; "beyond" means the rule goes further than the checklist.

- New model, or new objects: follow every rule.
- Evaluating an existing model: report every breach. Change nothing.
- Changing an existing model: see "Existing models" at the end. Never rename or move without a clear yes.

## A. Measures

**1. Home.** Every measure lives in one table named `_Measures`. The table is visible. It has exactly one column, and that column is hidden. Item: beyond. Checks: M001, M002 (fail).

- The developer makes the table in Power BI Desktop, the way Microsoft Learn describes: Enter data, one column, name the table `_Measures`, load it, then hide the column and not the table. Do not write this table from memory; ask the developer to make it.
- Direct Lake model: an entered table is an imported table and would make the model composite. There the developer makes `_Measures` as a calculated table whose formula names no Direct Lake table (Microsoft's skill shows `ROW("Dummy", BLANK())`). It then needs its reason line (rule 8).
- DirectQuery model: an entered table also makes the model composite. Ask the developer which form they want and record it in section 4 of the brief.
- More than one measure table is allowed only when section 9 of the brief lists the extra table with the code `M001` and the reason.

**2. Folders.** Every measure has one display folder with exactly two levels: subject, then type. Never one level, never three, never a list of folders. Item 22. Checks: M003, M004 (fail).

- Subject comes from "Measure folder subjects" in the brief. If that field is empty the list is: Reliability, Energy and Gas, Customer, Safety, Finance, Workforce, IT and Security, Work Management.
- Type is one of: Base, Time Intelligence, Comparisons, Ratios, Counts.
- The levels are separated by one backslash, written plainly: `displayFolder: Finance\Base`. A forward slash does not make a second level.

**3. Names.** Items 7 and 28.

- Title Case, business words, spaces. Acronyms in capitals. No snake_case, CamelCase or ALL_CAPS, and no abbreviation a report author would not know. A word with its own spelling, such as kWh, is allowed when the brief lists it. Check: M007 (fail).
- Order: base name, then period, then comparison, then unit: `Total Sales`, `Total Sales YTD`, `Total Sales vs Budget`, `Total Sales vs PY (%)`.
- Periods are spelled YTD, QTD, MTD, PY.
- A unit goes in brackets at the end, and only when the measure has more than one variant: `Gross Margin (%)`.
- A count starts with `#`: `# Orders`.
- A comparison uses `vs`.
- The folder type follows the name: `#` goes in Counts, `vs` in Comparisons, a period in Time Intelligence. Check for these five points: M008 (warn).
- A name is used once in the model (M005, fail), has no space at either end (M007), and is never the name of a column in any table (M006, fail).

**4. Description and format string.** Every measure has both. A measure that is only a text value needs no format string. Items 23 and 36. Checks: D001, M009 (fail). The format comes from the brief (item 71).

**5. References in DAX.** Write a column as `Table[Column]` and a measure as `[Measure]`. Item: beyond. Check: M010 (warn; the script reads text and is not a DAX parser).

## B. Columns and tables

**6. Column folders.** In a table that shows 20 or more fields, every visible column sits in one of four folders, with the same names in every table: Attributes, Keys, Facts, Hierarchy. Item 22. Check: M101 (warn).

**7. Hiding.** Items 19 and 25. Checks: M102, M103, M104 (warn).

- Hide surrogate keys, foreign keys, sort-by keys and technical columns.
- Hide a numeric column when a measure already totals it.
- Hide a table that only links other tables or only feeds formulas (a bridge or helper table). Never hide `_Measures`.
- Never hide a column that a hierarchy or a visual needs.
- Items 19 and 25 come first: a technical-looking field stays visible when authors need it. Then section 9 of the brief lists it with its use.

**8. Calculated columns and calculated tables.** They get no special name. Each carries one line that says why it is calculated in the model and why it cannot come from the source, as an annotation: `annotation CalculatedReason = <one line>`. Never invent the reason; ask the developer. More than five calculated columns in a model, or one that uses RELATED, is reported for review. Items 27 and 38. Checks: M105 (fail), M106 (warn).

**9. Summarise.** A visible number column does not total by default: `summarizeBy: none`. Authors use a measure instead (item 29). A column that analysts must total ad hoc is listed in section 9 of the brief. Check: M107 (fail). Turning it off in an existing model is the developer's decision: Microsoft documents this setting as the default used when a field is added, and does not say what happens to visuals that already total the column.

**10. Data types.** Item 6. No floating-point type (`double`, called "Decimal number" in Desktop): use fixed decimal or whole number. Check: M108 (warn). Both columns of a relationship have the same type (M109, fail); whole number is preferred (M110, warn). A type change is always the developer's decision, never a script fix: it changes stored precision.

**11. Date and time together.** A column that holds both is reported for review. The files do not show the data, so the script reports a date column whose format shows a time, is `General Date`, or is missing. Item: beyond. Check: M111 (warn).

**12. Formats.** A visible date column and a visible number column have a format string, taken from the brief. Items 71 and 72. Check: M112 (warn).

## C. Assess only (no failure)

**13. Hierarchies** exist for natural drill paths, such as year, quarter, month, date. Item 59. Judged in the review.

**14. Large tables** use incremental refresh or partitions; section 4 of the brief records the row counts and the decision. Ask the developer for row counts. Judged in the review.

**15. Unused hidden objects.** A hidden column or hidden measure that nothing refers to is listed. Items 5 and 25. Note M201.

## D. Off unless the brief turns them on

**16. Excel.** With "Excel check on: yes", the script lists hidden columns that are not a sort key, are not sorted by another column and are in no hierarchy. Turning `isAvailableInMdx` off on them saves memory, but removes them from Excel PivotTables. Report the list and that risk. Change nothing without the developer's yes. Note M301.

**17. Copilot in Power BI.** With "Power BI Copilot check on: yes":

- Microsoft states that Copilot reads the model's fields, the synonyms in the model's linguistic schema, and descriptions only up to 200 characters. So put the key words of a description first. Note M302 lists longer descriptions.
- Synonyms are set by a person in Power BI ("Prep data for AI"). Do not write them into files. Propose only words that people in the organisation really use, and let the developer enter them.

## Exceptions

A check passes only for an object that section 9 of the brief lists with the same code and a reason. If the developer asks for an exception that is not listed, ask for the reason and add the row first. Never add a row just to make a check pass.

## Existing models: moving and renaming

Before a measure moves to `_Measures`, or anything is renamed, tell the developer what can break, then wait for a clear yes (rename rule in the project instructions).

- DAX: a formula that names the measure with its table (`Sales[Total Sales]`) breaks when the measure's table changes. Formulas that write `[Total Sales]` keep working.
- Report visuals: a visual stores the measure's table beside its name, so a move or a rename can break visuals, filters and bookmarks in this report.
- Other reports connected to a published model can break in the same way. Say so every time.
- A move is done by the developer in Power BI Desktop: Model view, select the measure, set Home table. Do not move measures by editing files.
- Afterwards run `python scripts/check_project.py .`. B001 lists every report file that names a field the model no longer has; M010 lists formulas that still name a measure with its table.

## Sources

Read on 11 November 2026. Rules are restated in this template's own words.

- Microsoft Learn: "Create measures for data analysis in Power BI Desktop" (Organize your measures: home table, display folders, backslash, measures table); "Column and measure references"; "Measures in tabular models" and "Calculated Columns" (Analysis Services); "Data types in Power BI Desktop"; "Work with aggregates"; "Direct Lake overview"; "Use composite models"; "Use Copilot with semantic models"; "TMDL view" (renaming may break visuals); "TMDL overview".
- Microsoft's `skills-for-fabric` repository (MIT), skill `semantic-model-authoring`: modeling guidelines, naming conventions, TMDL guidelines, AI readiness.
- Microsoft's `Analysis-Services` repository (MIT), `BestPracticeRules/BPARules.json`: the rules on names, references, hiding, calculated columns and tables, summarising, data types, date and time, format strings, unused objects and `IsAvailableInMdx`. Each rule's expression was read, not only its name.
- GitHub's `awesome-copilot` repository (MIT), skill `powerbi-modeling`: measure table name, naming, references, display folders.
- Microsoft's `BCApps` repository (MIT): Power BI project files saved with nested display folders, entered tables, calculated columns and annotations; used as evidence of what a saved project holds.
- Microsoft's report schema `semanticQuery`: how a visual names a measure.
- Kurt Buhler's `power-bi-agentic-development` repository (GPL-3.0): ideas only, for measure tables, naming order, column folders, hiding, the reason for calculated objects and synonyms. No text was copied.

Where sources disagree, and what was decided:

- One measures table: Microsoft Learn, awesome-copilot and Kurt Buhler describe it; Microsoft's skill advises against it. The owner chose one table.
- Folder separator: Microsoft Learn and Microsoft's saved projects use a backslash; Kurt Buhler's repository says forward slash. Backslash.
- Folder depth: no source says "exactly two". It is the owner's rule. Checklist item 22 is still judged by its own thresholds.
- Period spelling: Microsoft's skill writes `(ytd)`; awesome-copilot puts the period first. The owner chose a capital suffix.
- Characters in names: Microsoft Learn "DAX syntax" lists `%` and brackets as not valid in names, while Microsoft's own TMDL examples use `'Sales (ly)'` and `'# Products'`. Not settled by the documentation; check `# Orders` and `Gross Margin (%)` once in Power BI Desktop.
- Summarising: Microsoft's skill names identifiers, years and the like; the best practice rule covers every visible number column. The owner chose every column, with exceptions in the brief.
- Column formats: the best practice rules demand fixed formats; items 71 and 72 leave the format to the organisation. The check only asks that a format exists.

Not confirmed from Microsoft's documentation: that Power BI Desktop keeps a `CalculatedReason` annotation when it saves (Microsoft's saved projects do keep annotations of other tools); that a hidden column keeps working in a hierarchy or slicer; whether Desktop repairs visuals when a measure's table changes in the files.

Checklist items: 5, 6, 7, 19, 22, 23, 25, 27, 28, 29, 36, 38, 59, 71, 72
