# The model standard

One fixed standard for every model built from this template, so that models look the same over time and across projects. `python scripts/check_project.py .` checks it; the code after each rule is the finding it gives. "Item" is the checklist item a rule supports; "beyond" means the rule goes further than the checklist.

- New model, or new objects: follow every rule.
- Evaluating an existing model: report every breach. Change nothing.
- Changing an existing model: see "Existing models" at the end. A rename or a move follows the rule there.

This file covers measures, folders, hiding, calculated objects, summarising, data types and formats. The rest of the standard is in the files beside it: `relationships-and-dates.md` (star schema, relationships, dates, names of tables and columns), `dax-standard.md` (DAX), `storage-and-security.md` (Power Query, storage modes, security) and `model-objects.md` (functions, calculation groups, field parameters and the other object kinds).

## A. Measures

**1. Home.** Every measure lives in one table named `_Measures`. The table is visible. It has exactly one column, and that column is hidden. Item: beyond. Checks: M001, M002 (fail).

- Copilot makes the table itself: `python scripts/scaffold.py measures-table .`. The script copies the shipped example and picks the form from the model's storage modes.
- Import model: an imported table with one hidden text column and no rows, read by a one-step Power Query query. This is the files' form of what Microsoft Learn describes for Power BI Desktop (Enter data, one column, load it, hide the column and not the table: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-measures). Microsoft Learn gives the table no name; the name `_Measures` is the owner's choice and is also the name used in GitHub's modeling skill and in an example of Microsoft's skill.
- Direct Lake model: an imported table would make the model composite. There `_Measures` is a calculated table whose formula names no other table (Microsoft's skill shows a one-row table made with ROW). It carries its reason line (rule 8); the script writes the standard's own reason.
- DirectQuery model: the same calculated form, for the same reason. This is the template's default; if the developer wants an imported table instead, they say so and section 4 of the brief records it.
- A report on a published model has no model here: its measures live in the published model.
- More than one measure table is allowed only when section 9 of the brief lists the extra table with the code `M001` and the reason.

**2. Folders.** Every measure has one display folder with exactly two levels: subject, then type. Never one level, never three, never a list of folders. Item 22. Checks: M003, M004 (fail).

- Subject comes from "Measure folder subjects" in the brief. If that field is empty the list is: Reliability, Energy and Gas, Customer, Safety, Finance, Workforce, IT and Security, Work Management (the eight business definition areas of this template). When no subject on the list fits what the model measures, do not leave the measure without a folder: take a subject from the model's own business (the name of what its fact table records, such as Sales Pipeline), add it to "Measure folder subjects" in the brief, and record it as an assumption (section 6 of the brief, `assumed` under By).
- Type is one of: Base, Time Intelligence, Comparisons, Ratios, Counts.
- Both lists are the owner's. No public source prescribes them.
- The levels are separated by one backslash, written plainly, with no space on either side of it: `displayFolder: Finance\Base`. A forward slash does not make a second level.

**3. Names.** Items 7 and 28.

- Business words with spaces. No snake_case, CamelCase or ALL_CAPS, and no space at either end. Check: M007 (fail). The script catches an underscore, two words run together, a name of two or more words all in capitals where one has five letters or more, and any word of six or more letters in capitals. A shorter word in capitals is read as an acronym. A word with its own spelling, such as kWh, or a long acronym, passes when the brief lists it.
- No abbreviation a report author would not know. No script can judge this; the review does (item 7).
- Title Case, with acronyms in capitals.
- Order: base name, then period, then comparison, then unit: `Total Sales`, `Total Sales YTD`, `Total Sales vs Budget`, `Total Sales vs PY (%)`.
- Periods are spelled YTD, QTD, MTD, PY.
- A unit goes in brackets at the end, and only when the measure has more than one variant: `Gross Margin (%)`.
- A count starts with `#`: `# Orders`.
- A comparison uses `vs`.
- The folder type follows the name: `#` goes in Counts, `vs` in Comparisons, a period in Time Intelligence.
- The last seven points give a warning, M008.
- A name is used once in the model, whatever its capitals (M005, fail), and is never the name of a column in any table (M006, fail).

**4. Description and format string.** Every measure has both. The script checks the visible ones, as items 23 and 36 do: D001 and M009 (fail). A measure that is only a text value needs no format string. The format comes from the brief (item 71). When the brief gives none, use the default and record it as an assumption: a count or whole number `#,0`; a number with decimals `#,0.00`; a ratio, share or probability `0.0%`; an amount of money, the currency format the model already uses, else `#,0.00`.

**5. References in DAX.** Write a column as `'Table'[Column]`, with the table name in single quotes, and a measure as `[Measure]`. Item: beyond. Check: M010 (warn; the script reads text and is not a DAX parser).

## B. Columns and tables

**6. Column folders.** In a table that shows 20 or more fields, every visible column sits in one of four folders, with the same names in every table: Attributes, Keys, Facts, Hierarchy. Item 22. Check: M101 (warn).

**7. Hiding.** Items 19 and 25. Checks: M102, M103, M104 (warn).

- Items 19 and 25 come first: a field stays visible when report authors have a real use for it. Section 9 of the brief then lists it with that use.
- Otherwise these are hidden: identifier columns, the many-side column of a relationship, a column that exists only to sort another one, and system columns.
- A number column is hidden once a measure adds it up, counts it or averages it; authors use the measure.
- A table that only bridges two tables, or only feeds formulas, is hidden. `_Measures` is never hidden.
- A column that a hierarchy level or a report visual uses stays visible, and no script proposes to hide it. This last point is the owner's rule. Microsoft states that a hidden column still works in the model and in queries; hiding only takes it out of the field list, so authors can no longer pick it.

**8. Calculated columns and calculated tables.** They get no special name. Each carries an annotation with one line of justification: `annotation CalculatedReason = <one line>`. The line states what makes a DAX calculation necessary here, and what stops the value being delivered by Power Query or the source system. The words are the developer's for a new object: ask for them. For an object that already exists, in the evaluate-and-improve flow, write the line yourself from what the files show (what the formula builds, and that no query or source table delivers it), record it as an assumption, and ask the owner to confirm it in your final answer. The tables the standards define carry the standard's own line and need no question: a calculated `_Measures` table (rule 1), a field parameter and a numeric range parameter (`model-objects.md`, beside this file). If the developer has no such reason, say that Microsoft's guidance is to push the logic upstream, and leave the finding open. More than five calculated columns in a model, or one that uses RELATED, is reported for review. The tables that Power BI makes for Auto date/time (`LocalDateTable_...`, `DateTableTemplate_...`) are left out; item 18 deals with them. Items 27 and 38. Checks: M105 (fail), M106 (warn).

**9. Summarise.** A visible number column does not total by default: `summarizeBy: none`. Authors use a measure instead (item 29). A column that analysts must total ad hoc is listed in section 9 of the brief. Check: M107 (fail). Turning it off in an existing model is the developer's decision: Microsoft documents this setting as the default used when a field is added, and does not say what happens to visuals that already total the column.

**10. Data types.** No floating-point type (`double`, called "Decimal number" in Desktop): use fixed decimal or whole number. Beyond the checklist. Check: M108 (warn). Both columns of a relationship have the same type (M109, fail); whole number is preferred, and the script reports every other type, dates included, as the best practice rule does (M110, warn). These two support item 6. A type change is always the developer's decision, never a script fix: it changes stored precision.

**11. Date and time together.** A column that holds both is reported for review. The files do not show the data, so the script reports a date column whose format shows a time, is `General Date`, or is missing. Item: beyond. Check: M111 (warn).

**12. Formats.** A visible date column and a visible number column have a format string, taken from the brief; when the brief gives none, the defaults of rule 4, and `Short Date` for a date, recorded as an assumption. Items 71 and 72. Check: M112 (warn).

## C. Assess only (no failure)

**13. Hierarchies** exist for natural drill paths, such as year, quarter, month, date. Item 59. Judged in the review.

**14. Large tables** use incremental refresh or partitions; section 4 of the brief records the row counts and the decision. Microsoft's best practice rule 'Large tables should be partitioned' draws the line at more than 25 million rows in a table with one partition (https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json). The files do not hold row counts: ask the developer. Beyond the checklist (item 17 is about aggregations, a different matter). Judged in the review.

**15. Unused hidden objects.** A hidden column or hidden measure that nothing refers to is listed. Items 5 and 25. Note M201.

Order inside a table file: write measures before columns. Microsoft's skill asks for it (tmdl-guidelines.md), and the TMDL examples on Microsoft Learn show it; Learn also says the order of columns and measures can be anything, so it does not change the model. No check. Source: https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/tmdl-guidelines.md ; https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview

## D. Off unless the brief turns them on

**16. Excel.** With "Excel check on: yes", the script lists hidden columns that are not a sort key, are not sorted by another column, are in no hierarchy and have no variation (the conditions of Microsoft's best practice rule). Turning `isAvailableInMdx` off on them saves memory, but removes them from Excel PivotTables. Report the list and that risk. Change nothing without the developer's yes. Note M301.

**17. Copilot in Power BI.** With "Power BI Copilot check on: yes":

- Microsoft states that Copilot reads the model's fields, the synonyms in the model's linguistic schema, and only the first 200 characters of a description (https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-evaluate-data). So put the key words of a description first. Note M302 lists longer descriptions.
- Synonyms are part of the model's linguistic setup, which a person edits in Power BI (the Q&A setup, or "Prep data for AI"). Microsoft's skill says an agent must not write their stored form, so do not write them into files. You may hand the developer a list of candidates: the different terms that departments already use for the same field. The developer decides and enters them.
- Mark the column that names each member of a dimension with `isDefaultLabel`, for example `Store[Store Name]`, so Copilot knows which column labels the table. Note M303 lists dimension tables with no column marked, when the brief turns the Copilot check on. The shipped `Store[Store Name]` carries it. Item: beyond. Source: Microsoft's skill, https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/semantic-model-ai-readiness.md

## Exceptions

A check passes only for an object that section 9 of the brief lists with the same code and a reason. If the developer asks for an exception that is not listed, ask for the reason and add the row first. Never add a row just to make a check pass.

## Existing models: moving and renaming

A move or a rename happens when the developer asks for it, or in the evaluate-and-improve flow, where every measure moves to `_Measures` in one commit and names the naming standard rejects are corrected in another. Do it at once, yourself, as set out below, without asking. It can break other reports that read a published copy of this model, and no file here shows them: say so in your final answer.

A new `_Measures` table is empty until Power BI Desktop refreshes the model. Say so whenever you make the table in an existing model.

What can break:

- DAX: a formula that names the measure with its table (`'Sales'[Total Sales]`) breaks when the measure's table changes. Formulas that write `[Total Sales]` keep working.
- Report visuals: a visual stores the measure's table beside its name, so a move or a rename can break visuals, filters and bookmarks in this report.
- Other reports connected to a published model can break in the same way, and no file here can show it. Say so every time.

Copilot does the work itself:

1. Run `python scripts/find_references.py . "<object>"`, written as `[Measure]`, `Table[Column]` or `Table`. It prints the references it recognises, and the text it cannot classify.
2. If the second list is not empty, show it to the developer and change only what they confirm. If the script cannot confirm the references at all (the object is not in the model, or a file cannot be read), stop and say so.
3. Moving a measure: cut the measure, with its description lines and its properties, from its table file and paste it into the `_Measures` file. Its name does not change. Rewrite every `OldTable[Measure]` and `'OldTable'[Measure]` in DAX to `[Measure]`. In report files, change the table (`Entity`) of that measure and the `OldTable.Measure` query names to the new table.
4. Renaming: change the definition and every reference in the first list: DAX, relationship columns, sort column, hierarchy level, group-by column, aggregation, perspective, translation, role, and in report files the `Property` and the `Table.Field` query names. Change no display text the developer typed (a title, a label in a field parameter) without asking.
5. Run `python scripts/check_project.py .`. M901 to M903 and M908 fail on a model reference that was missed; B001 fails on a report file that names a field the model no longer has; M010 lists formulas that still name a measure with its table. Fix until they are clean.
6. Reload and look (project instructions), then tell the developer what changed and repeat the warning about other reports.

Renaming a table is done the same way, and its file is renamed with it. Microsoft notes that Power BI Desktop must be restarted after a file or folder of a report is renamed.

## Sources

Read on 11 November 2026. Rules are restated in this template's own words.

- Microsoft Learn: "Create measures for data analysis in Power BI Desktop" (Organize your measures: home table, display folders, backslash, measures table); "Column and measure references"; "Measures in tabular models", "Calculated Columns" and "Column properties" (Analysis Services); "Data types in Power BI Desktop"; "Work with aggregates"; "Auto date/time in Power BI Desktop"; "Direct Lake overview"; "Use composite models"; "Use Copilot with semantic models" and "Evaluate your data for Copilot" (the first 200 characters of a description); "TMDL view" (renaming may break visuals); "TMDL overview".
- Microsoft's `skills-for-fabric` repository (MIT), skill `semantic-model-authoring`: modeling guidelines, naming conventions, TMDL guidelines, AI readiness.
- Microsoft's `Analysis-Services` repository (MIT), `BestPracticeRules/BPARules.json`: the rules on names, references, hiding, calculated columns and tables, summarising, data types, date and time, format strings, unused objects and `IsAvailableInMdx`. Each rule's expression was read, not only its name.
- GitHub's `awesome-copilot` repository (MIT), skill `powerbi-modeling`: measure table name, naming, references, display folders.
- Microsoft's `BCApps` repository (MIT): Power BI project files saved with nested display folders, entered tables, calculated columns and annotations; used as evidence of what a saved project holds.
- Microsoft's report schema `semanticQuery`: how a visual names a measure.
- Kurt Buhler's `power-bi-agentic-development` repository (GPL-3.0): ideas only, for a measures table, the order of a measure name, column folders, keeping hierarchy and slicer columns visible, and a recorded justification for calculated objects. No text was copied; every rule here is written in this template's own words.

Where sources disagree, and what was decided:

- One measures table: Microsoft Learn, awesome-copilot and Kurt Buhler describe it. Microsoft's skill advises against it in its modeling guidelines, yet shows a `_Measures` table in its TMDL guidelines. The owner chose one table.
- Folder separator: Microsoft Learn, Microsoft's saved projects and awesome-copilot use a backslash. Kurt Buhler's repository says forward slash in two files and backslash in a third. Backslash.
- Folder depth: no source says "exactly two". It is the owner's rule. Checklist item 22, which lets a small model go without folders, is still judged by its own thresholds.
- Period spelling and place: Microsoft's skill writes `(ytd)` and `(ly)` in brackets; awesome-copilot puts the period first (`YTD Sales`). The owner chose a capital suffix and PY.
- Counts and units: awesome-copilot shows `Count of Orders` and `Margin %`, and says to avoid special characters; Microsoft's skill shows `# Orders` and `Gross Margin (%)`. The owner chose the second. Checklist item 28 lets a team use no prefixes at all; here `#` is the chosen standard.
- Characters in names: Microsoft Learn "DAX syntax" lists `%` and brackets among characters not valid in names. Against that, Microsoft Learn's TMDL overview shows `'Sales (ly)'` and `'# Products'`, and Microsoft's saved projects hold measure names with `%` and brackets. `#` is not on the list. The documentation does not settle it; check `# Orders` and `Gross Margin (%)` once in Power BI Desktop.
- Summarising: Microsoft's skill names identifiers, years and the like; awesome-copilot keeps "sum" on amounts and accepts column totals for simple exploration; the best practice rule covers every visible number column. The owner chose every column, with exceptions in the brief.
- Column formats: the best practice rules demand fixed formats; items 71 and 72 leave the format to the organisation. The check only asks that a format exists.

- The measures table in a DirectQuery model: no source prescribes a form. The calculated form is this template's default, chosen so that Copilot can build it without a question.
- Moving a measure by editing files: Microsoft Learn describes the Home table setting of Power BI Desktop; it also documents TMDL files as open to outside edits. The template edits the files and then proves every reference with the checks.

Not confirmed from Microsoft's documentation: that Power BI Desktop keeps a `CalculatedReason` annotation when it saves (Microsoft's saved projects do keep annotations of other tools); what turning summarisation off does to visuals that already total the column; that an empty one-column imported table shows at the top of the Data pane the way a table made with Enter data does.

Checklist items: 5, 6, 7, 19, 22, 23, 25, 27, 28, 29, 36, 38, 59, 71, 72
