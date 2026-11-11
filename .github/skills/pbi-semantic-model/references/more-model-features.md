# More model features: when to use each, and how it is stored

This file covers model features that the other files beside it leave out: extra partitions, more storage forms, model-wide switches, and the files of a model folder that no instruction names.
For each one it says when Microsoft says to use it, its release status, the limits Microsoft lists, the exact keywords in the files, the shipped example to copy (or why there is none), and what the check reads.
All example paths below start at `tests/fixtures/examples/`. Nothing there has been opened in Power BI Desktop, and Microsoft's library, which wrote the files, does not parse DAX or Power Query: look at the first use of each kind in Desktop.

A preview feature is used only after the developer's yes, recorded in section 11 of `docs/report-brief.md`. Source: `.github/skills/pbi-semantic-model/SKILL.md` ("A better native feature").

## A. Partitions and storage

**1. Several partitions on one table.**
- When: a very large table whose parts load or refresh apart from each other. Desktop does not show partitions; incremental refresh makes them for you; anything more is done through the XMLA endpoint.
- Status: no preview label. Limits: a table holds at most one DirectQuery partition; partitions must not overlap, because the engine does not check it.
- Stored: one `partition '<Name>' = m` block per partition in the same table, each with its own `mode:` and `source =`.
- Example: `storage/Hybrid.SemanticModel/definition/tables/Sales History.tmdl` ('Sales History Recent', import; 'Sales History Older', DirectQuery).
- Check: M117 warns only when a table has one partition named unlike the table.
- Source: https://learn.microsoft.com/en-us/analysis-services/tom/table-partitions ; https://learn.microsoft.com/en-us/analysis-services/tabular-models/define-partitions-in-directquery-models-ssas-tabular

**2. Hybrid table (incremental refresh with real-time data).**
- When: a fact table needs its newest rows at once, while older rows stay imported.
- Status: GA. Limits: Premium, Premium Per User or Embedded, never Pro; all partitions read one source; no step that does not fold; related tables should be Dual; once published, publishing again from Desktop drops the partitions and their data. An aggregation table cannot sit on a hybrid table (the file `storage-and-security.md` beside this one, rule 25).
- Stored: `refreshPolicy` with `mode: hybrid` above the usual policy lines; the service adds the DirectQuery partition itself.
- Example: `storage/Hybrid.SemanticModel/definition/tables/Sales.tmdl`, with `Date` in Dual mode beside it.
- Check: M707 and M709, as for any refresh policy.
- Source: https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview ; https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla

**3. Data coverage definition.**
- When: a table has an import partition for recent rows and a DirectQuery partition for old ones. The definition says which rows the DirectQuery partition holds, so queries on recent data leave the source alone.
- Status: no preview label; compatibility level 1603 or higher.
- Limits: fixed values only, never `TODAY ()` and the like; a dimension reached through RELATED must be Dual; a wrong definition gives wrong numbers, so compare results with and without it; refresh after each change; a hybrid policy drops the definition when it remakes its DirectQuery partition.
- Stored: under the DirectQuery partition, after its source: `dataCoverageDefinition = RELATED ( 'Date'[Year] ) IN { 2022, 2023 }`.
- Example: the partition 'Sales History Older' in `storage/Hybrid.SemanticModel/definition/tables/Sales History.tmdl`. A `///` line may sit directly above `dataCoverageDefinition`: Microsoft's serializer writes descriptions there, and the check accepts one.
- Source: https://learn.microsoft.com/en-us/analysis-services/tom/table-partitions ; https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.datacoveragedefinition

**4. Direct Lake on SQL or on OneLake.**
- On OneLake when: data from one or more Fabric items; Import or DirectQuery tables mixed in; OneLake security; calculated columns or tables over Direct Lake data (preview). It never falls back to DirectQuery.
- On SQL when: security rules live in the SQL analytics endpoint, or tables are SQL views. It can fall back to DirectQuery. The model property `directLakeBehavior` decides: `automatic` (the default, written by leaving the line out), `directLakeOnly` (a query fails instead; for development), `directQueryOnly` (to measure fallback). Microsoft advises the default in production.
- Stored on OneLake: the shared expression calls `AzureStorage.DataLake` with the workspace and item IDs (`storage/DirectLake.SemanticModel/definition/expressions.tmdl`).
- Stored on SQL: the shared expression calls `Sql.Database` with the endpoint and the endpoint's ID, never its friendly name (`storage/DirectLakeSql.SemanticModel/definition/expressions.tmdl`, expression `DatabaseQuery`; `directLakeBehavior: directLakeOnly` in its `model.tmdl`).
- Both: `partition <Name> = entity`, `mode: directLake`, `entityName`, `schemaName`, `expressionSource`.
- Fabric SQL databases, mirrored databases and mirrored catalogs use the same two forms; for a warehouse the OneLake form takes a warehouse ID in place of a lakehouse ID. No separate example.
- Status: GA. Limits: the file `storage-and-security.md` beside this one, rule 27. No check.
- Source: https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-develop ; https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview ; https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-how-it-works ; https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/ontology-definition

**5. Direct Lake on OneLake plus Import tables.**
- When: large facts stay in OneLake while a small table comes from any other source.
- Status: the Learn pages read carry no preview label; an earlier reading recorded it as preview, so the example sits under `preview/`, beside the two preview features it also shows.
- Limits: Direct Lake on SQL cannot mix; import tables are added in web modeling, not in Desktop; relationships between the two kinds are regular ones.
- Stored: an ordinary import table (`partition ... = m`, `mode: import`) beside entity partitions.
- Example: `preview/DirectLakeComposite.SemanticModel` (Date imported; Sales and Store in Direct Lake). No check.
- Source: https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-web-modeling ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-composite-models

**6. Calculated table over Direct Lake data (preview).**
- When: a small summary that the lakehouse cannot give. Prefer making it in the lakehouse.
- Limits: Direct Lake on OneLake only; on SQL only calculation groups and parameter tables are allowed.
- Stored: `partition ... = calculated` whose formula names a Direct Lake table, with `annotation CalculatedReason`.
- Example: `preview/DirectLakeComposite.SemanticModel/definition/tables/Daily Sales.tmdl`. Check: M105 (fail) for the reason line; M841 (warn) until section 11 of the brief has a row named `calculated tables over Direct Lake`.
- Source: https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview

**7. User-context calculated column (preview).**
- When: the value depends on the reader, through USERCULTURE, USERPRINCIPALNAME, USEROBJECTID, USERNAME or CUSTOMDATA, such as names in the reader's language.
- Limits: worked out at query time and never stored, so it is slower and cannot carry a relationship; in Direct Lake on OneLake it is the only kind of calculated column; Direct Lake on SQL has none.
- Stored: `expressionContext: userContext` under the calculated column. Microsoft's library requires compatibility level 1705.
- Example: 'Store Name Local' in `preview/DirectLakeComposite.SemanticModel/definition/tables/Store.tmdl`. Check: M105 (fail) for the reason line; M841 (warn) until section 11 of the brief has a row named `user-context calculated columns`.
- Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-calculated-columns ; https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.calculatedcolumn.expressioncontext

**8. Composite model on a published model, and EXTERNALMEASURE.**
- When: a team extends a published semantic model, or an Analysis Services model, with tables of its own.
- Status: GA. Limits: the remote model is in the same tenant; tenant switches must allow it; security on the source model is not copied; keys of relationships across sources stay small.
- EXTERNALMEASURE calls a measure of the remote model by name, with a type and the connection name; it works only in such a model.
- Not built: Microsoft Learn gives no file form for the remote connection or its tables. Make it in Desktop (Make changes to this model); afterwards copy only from that model's own files.
- Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-composite-models ; https://learn.microsoft.com/en-us/dax/externalmeasure-function-dax

**9. Dynamic M query parameter.**
- When: in a DirectQuery model, a reader's pick in a slicer must reach the source query at a set place.
- Status: no preview label.
- Limits: one parameter per column and one column per parameter; no aggregations; no row-level security; the parameter name has no spaces and is no DAX reserved word; a table name has no spaces or special characters; the column's type matches the parameter's; many filter kinds do not pass the value on.
- Microsoft warns that joining the value into query text opens the source to injection: filter with a step that folds instead. P002 warns on a native query made by joining text.
- Stored: `parameterValuesColumn: '<Table>'.'<Column>'` under the parameter `expression`, plus a table of values with no relationship.
- Example: `storage/DynamicParameter.SemanticModel` (RegionParameter, table RegionChoice, Sales). The table of values gives M411 (warn) on purpose, and its one-word name gives M118 (warn) because of Microsoft's limit on table names: list both in section 9 of the brief with their reasons.
- Multi-select and Select all are switched on in Desktop; their stored form is not given.
- Source: https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-dynamic-m-query-parameters ; https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.namedexpression.parametervaluescolumn

**10. Python or R script as a data source.**
- It runs code on the developer's own machine at every refresh. Copilot never writes one; it may describe the option.
- Limits: the language is installed locally; a script stops after 30 minutes; nested tables fail; every source in the query has the privacy level Public; refresh in the service needs a personal gateway on the machine that holds the file and the language.
- Not built: guidance only. No check.
- Source: https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-python-scripts ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-python-in-query-editor ; https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-r-scripts ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-r-in-query-editor

## B. Columns and calculation groups

**11. Barcode.**
- When: a column holds product barcodes that the Power BI mobile app scans to filter a report.
- Status: no preview label. Limits: one barcode column across all tables of a report, or no filter happens; Microsoft lists the barcode formats it reads.
- Stored: `dataCategory: Barcode` on a text column.
- Example: Product[Barcode] in `Examples.SemanticModel/definition/tables/Product.tmdl`. Check: none (M114 reads place names only).
- Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-mobile-barcodes

**12. Groups and bins.**
- When: values go into a few named groups, or numbers and dates into bins of equal size. A bin works on a column, not on a measure.
- Not built: Learn shows only the Desktop dialog (New group), not how a group is stored. Make it in Desktop, or write a calculated column with SWITCH and its reason line.
- Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-grouping-and-binning

**13. Selection expressions of a calculation group.**
- When: the group must return something set when readers pick two or more items, or one that does not exist (`multipleOrEmptySelectionExpression`), or nothing (`noSelectionExpression`). Without them the group acts as if unfiltered. Each may carry its own `formatStringDefinition`.
- The model property `selectionExpressionBehavior` (`automatic`, `nonVisual`, `visual`) sets what happens when they are missing; `automatic` acts as `nonVisual` today.
- Status: no preview label; level 1605 for the expressions, 1609 for the property.
- Stored: inside `calculationGroup`, below `precedence`.
- Example: `Examples.SemanticModel/definition/tables/Time Calculation.tmdl` (blank for several picks, the plain measure for none) and `selectionExpressionBehavior: nonVisual` in `Examples.SemanticModel/definition/model.tmdl`. A `///` line may sit directly above each expression, as in rule 3.
- Check: none on the expressions.
- Source: https://learn.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups ("Selection expressions")

**14. Detail rows and calculation groups.**
- Microsoft states that detail rows expressions do not work in a model with a calculation group.
- The shipped `Examples.SemanticModel` holds both (`# Order Lines` and 'Time Calculation') only to show each form. A real model keeps one of the two; which one is the developer's decision.
- Check: M815 (warn). Source: https://learn.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups ("Limitations")

## C. Model-wide switches

**15. Discourage composite models.**
- When: no one should extend a published model with DirectQuery, so chains of models stop. Power BI honours it; other tools may not.
- Set in Desktop: Options, Current File, Published semantic model settings. Status: no preview label.
- Stored: the bare flag `discourageCompositeModels` in `model.tmdl`.
- Example: `storage/ModelOptions.SemanticModel/definition/model.tmdl`. No check.
- Source: https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-discourage-directquery-connections-to-dataset

**16. Unique names.**
- The bare flag `forceUniqueNames` stops a measure from taking the name of any column. This template asks the same already (M006).
- Only Microsoft's library reference documents it. Example: the same `model.tmdl` as rule 15.
- Source: https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.model.forceuniquenames

**17. Value filter behavior (preview).**
- When: filters on two columns of one table must stay apart, instead of merging into the combinations that exist.
- `independent` keeps them apart; `coalesced` merges them; `automatic` merges today and may change when the preview ends. Set in the model's Properties pane.
- Stored: `valueFilterBehavior: independent` in `model.tmdl` (level 1606).
- Example: `preview/ValueFilter.SemanticModel`, built on Microsoft's own scenario. Check: M841 (warn) until section 11 of the brief has a row named `value filter behavior`.
- Source: https://learn.microsoft.com/en-us/power-bi/transform-model/value-filter-behavior

**18. Data access options.**
- Settings of the Power Query engine that Power BI writes on new models.
- Stored: `dataAccessOptions`, with the bare flags `legacyRedirects` and `returnErrorValuesAsNull` one level deeper.
- Leave the lines as Power BI wrote them; never add or remove them by hand. Example: `storage/ModelOptions.SemanticModel/definition/model.tmdl`.
- Source: https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/semantic-model-definition ; https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.model.dataaccessoptions

**19. Automatic aggregations.**
- Training and query coverage are set in the semantic model settings in the service, for DirectQuery models on Premium, Premium Per User or Embedded.
- Microsoft keeps that setting outside the model, and the service manages the tables it makes: never edit them. Not built.
- Source: https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/aggregations-auto ; https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/aggregations-auto-configure

**20. Unicode character behaviour.**
- When: the model must meet China's GB18030-2022 standard.
- `codePoints` makes LEN, LEFT, MID, RIGHT, FIND and REPLACE count a character such as an emoji as one; the default `codeUnits` counts it as two. Microsoft sets it with an XMLA command, then a full refresh.
- Stored: `unicodeCharacterBehavior: codePoints` in `database.tmdl`.
- Example: `storage/ModelOptions.SemanticModel/definition/database.tmdl`.
- Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-unicode-character-behavior

## D. Files and folders of a model folder

**21. `TMDLScripts/` and `DAXQueries/`.**
- Desktop saves each tab of TMDL view as a `.tmdl` file in `TMDLScripts/`, and each tab of DAX query view as a `.dax` file in `DAXQueries/`; their tab settings sit in `.pbi`.
- They are scripts, not the model: a script changes the model only when a person applies it in Desktop. The model is `definition/`.
- Copilot may read them. It does not write or edit them unless the developer asks.
- A Git setup started from the workspace leaves TMDL view scripts out.
- Source: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-tmdl-view ; https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view

**22. `changedProperty` lines.**
- Power BI writes them under an object to record that one of its properties was changed (level 1567). This template reads them as marks of a person's change to an object that Power BI keeps in sync.
- Never write one by hand and never remove one; keep it when you edit the object. Microsoft Learn gives only the library class.
- Source: https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.changedproperty

**23. `Copilot/` (Prep data for AI, preview).**
- It holds what the developer sets in Prep data for AI: the AI data schema (`schema.json`: the fields Copilot uses, their visibility and synonyms), AI instructions (`Instructions/`), verified answers (`VerifiedAnswers/`), and `examplePrompts.json`, `settings.json`, `version.json`.
- Read only for Copilot: the developer sets all of it in Power BI. Why: Microsoft never says the files are edited by hand, and rule 17 of the file `model-standard.md` beside this one keeps linguistic setup in Power BI.
- Limits: Q&A is on; in Desktop only Import, DirectQuery and local composite models; instructions hold at most 10,000 characters and may not be followed; verified answers do not support Git integration, REST APIs or deployment pipelines, and do not fully respect row-level or object-level security; after a Git deployment, refresh the model in the service.
- Schemas: `scripts/schemas/fabric/item/semanticModel/copilot`.
- Source: https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-prepare-data-ai ; https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-prepare-data-ai-data-schema ; https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-prepare-data-ai-instructions ; https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-prepare-data-ai-verified-answers ; https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/semantic-model-definition

**24. Other files.** Copilot edits none of them.
- `.gitignore` (project root): Desktop writes it only when none exists; it keeps `.pbi/localSettings.json` and `.pbi/cache.abf` out of Git. The developer may add lines. Source: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview
- `item.metadata.json` and `item.config.json`: the older form of `.platform` (type, display name, description; version and logicalId). A folder has the pair or `.platform`, never both; a commit replaces the pair. Never change the logicalId or the type. Source: https://learn.microsoft.com/en-us/fabric/cicd/git-integration/source-code-format
- `modelReference.json`: optional; points to a model hosted outside Power BI, with its connection string and type. Source: its schema, `scripts/schemas/fabric/item/semanticModel/modelReference`.
- `.schedules`: Fabric's file of scheduled jobs for an item under Git integration; set in Fabric, not by hand. Source: https://learn.microsoft.com/en-us/fabric/fundamentals/job-scheduler
- `.pbi/unappliedChanges.json`: Power Query edits saved with Apply later. Applying them overwrites the queries in the model, so an edit made outside Desktop to the same queries is lost. Tell the developer when the file exists. Source: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset

**25. Fabric Git integration.**
- A workspace admin connects a workspace to one branch and one folder, the Git folder setting; items then sync both ways.
- On every commit Fabric deletes files inside an item folder that are not part of the item: keep no file of your own inside a model or report folder.
- For several workspaces Microsoft advises one branch, with a Git folder of its own for each workspace.
- This template never connects to a workspace: that is the developer's decision.
- Source: https://learn.microsoft.com/en-us/fabric/cicd/git-integration/git-get-started ; https://learn.microsoft.com/en-us/fabric/cicd/git-integration/git-integration-process ; https://learn.microsoft.com/en-us/fabric/fundamentals/understand-best-practices-fabric-cicd

## Sources

Read on 11 November 2026. Every rule is restated in this template's own words; keywords are copied exactly.

- Microsoft Learn, partitions and refresh: https://learn.microsoft.com/en-us/analysis-services/tom/table-partitions ; https://learn.microsoft.com/en-us/analysis-services/tabular-models/define-partitions-in-directquery-models-ssas-tabular ; https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview ; https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla
- Microsoft Learn, Direct Lake and composite models: https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview ; https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-develop ; https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-how-it-works ; https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-web-modeling ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-composite-models ; https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/ontology-definition
- Microsoft Learn, columns, calculation groups and model properties: the pages named in each rule; https://learn.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups
- Microsoft Learn, files and Git: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview ; https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset ; https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/semantic-model-definition ; https://learn.microsoft.com/en-us/fabric/cicd/git-integration/source-code-format ; https://learn.microsoft.com/en-us/fabric/cicd/git-integration/git-integration-process
- Microsoft's Tabular Object Model library (NuGet Microsoft.AnalysisServices 19.118.3) and its TMDL serializer: the spelling of every keyword in the shipped examples, and the compatibility levels named above.
- This template: `scripts/model_rules.py` (M105, M117, M411, M707, M709), `scripts/check_project.py` (D003, P002), `tests/fixtures/examples/INDEX.md`.

## Not confirmed from Microsoft

- That Power BI Desktop opens a model at compatibility level 1705 (the user-context column needs it in Microsoft's library; Learn's compatibility-level page names 1700 as the latest).
- That Desktop keeps `mode: hybrid`, a second partition, `dataCoverageDefinition` or `unicodeCharacterBehavior` when it saves a project; Learn sets these through the XMLA endpoint.
- The spelling `nonVisual`: Learn writes `nonvisual`; the shipped example keeps the serializer's spelling.
- How Desktop stores multi-select and Select all of a dynamic M query parameter, and how it stores groups and bins.
- What each file of `Copilot/` holds beyond what its schema shows.
- A Microsoft page that says when Power BI writes `changedProperty`.

Checklist items: 16, 17, 30, 38
