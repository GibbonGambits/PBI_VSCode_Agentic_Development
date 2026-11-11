# Performance, storage modes, Power Query and security

How queries, data volume, storage modes and security roles are built in a model made from this template. The code after a rule is the finding it gives.
`python scripts/check_project.py .` checks it: codes M6xx, M7xx, P0xx and the note U004. A practice marked "No check" is guidance only, because the files do not show it.
An exception passes only when section 9 of `docs/report-brief.md` lists the code and the object exactly as the check prints it: `Role/Table` for a role rule (`Own Store/Store`), the table name for a query or storage finding, `Table[Column]` for a column, the query name for P003, `model` for M607 and U004. P001 takes no exception.

## A. Power Query standard

**1. Every step described.** Each step of a query's outer `let` has its own line, with a `//` line directly above it that says in plain words what the step does. A query is never written on one line. This is the template's convention; Microsoft's skill asks for the same comment above each step. Check: P001 (fail). Source: template convention; microsoft/skills-for-fabric, skill semantic-model-authoring, tmdl-guidelines.md; https://learn.microsoft.com/en-us/power-query/best-practices

```
	partition Store = m
		mode: import
		source =
				let
				    // Build a small made-up list of stores.
				    Source = #table(type table [#"Store Key" = Int64.Type, Region = text], {{1, "North"}, {2, "South"}}),
				    // Keep the stores of the region that the Store Region parameter names.
				    #"Kept Region" = Table.SelectRows(Source, each [Region] = #"Store Region")
				in
				    #"Kept Region"
```

**2. Query folding.** Folding means Power Query turns the steps into one query that the source runs itself. Checklist item 3.

- A DirectQuery or Dual table: the whole query must fold.
- An Import table on a relational source: aim for full folding. Where the Power Query engine still has to work, keep that work small.
- Put the steps that fold first: choose columns, filter rows, rename, set types. Put steps that do not fold after them. Item 3 prefers no known non-folding step before the first big row filter or column cut.
- What breaks folding: a step the source cannot express (Microsoft's examples are Capitalize Each Word and Keep bottom rows), and every step after a native query, unless `EnableFolding=true` is set on a connector that supports it. Flat files and constant tables have nothing to fold; item 3 is then not applicable.
- A step that cannot fold belongs at the source: a database view, or a prepared warehouse table.
- The files do not show whether a step folds. Read it from the file `data-facts.md` beside this one when the developer has set up Microsoft's modeling server; otherwise ask the developer. In Power BI Desktop the developer right-clicks a step: if View Native Query is greyed out on a source that normally offers it, that step stops folding. Folding indicators exist in Power Query Online only.
- No check. Source: https://learn.microsoft.com/en-us/power-bi/guidance/power-query-folding ; https://learn.microsoft.com/en-us/power-query/query-folding-examples ; https://learn.microsoft.com/en-us/power-query/step-folding-indicators ; checklist item 3

**3. Native queries.** Write a native SQL query with `Value.NativeQuery` and pass values as its parameters; never build the statement by joining text. Put as much of the logic as possible inside the statement, because later steps do not fold. The account behind it gets read access to the data it needs and nothing more (no check). Check: P002 (warn). For a DirectQuery table the statement must be a plain SELECT: no common table expression, no stored procedure. Check: M701 (fail; the statement starts with WITH, EXEC or EXECUTE). Source: https://learn.microsoft.com/en-us/power-bi/guidance/power-query-folding

**4. Referencing queries.** A shared query (an `expression`) that two or more tables read runs once for each of them, so the source is read once per table. `Table.Buffer` in the shared query does not stop this. For a light query that is fine. For a heavy one, do the work at the source, or move the shared query to a dataflow (Dataflow Gen2) and read the dataflow. Checklist item 4: two or more queries that reuse one heavy transformation call for a staging query; a small query layer does not need one, so never fail item 4 only because staging is missing. Shipped example: `'Sales Source'` in `tests/fixtures/examples/Examples.SemanticModel/definition/expressions.tmdl`, read by the table Sales. Check: P003 (warn). Source: https://learn.microsoft.com/en-us/power-bi/guidance/power-query-referenced-queries ; checklist item 4

**5. Heavy reshaping.** An Import query that combines, joins, groups, sorts, pivots, unpivots, adds columns or removes duplicates does work the source or a dataflow could do once for every model. Filter early; leave expensive steps such as a sort to the end. Check: P006 (warn; three or more of `Table.Combine`, `Table.Join`, `Table.NestedJoin`, `Table.AddColumn`, `Table.Group`, `Table.Sort`, `Table.Pivot`, `Table.Unpivot`, `Table.UnpivotOtherColumns`, `Table.Distinct` in one query). Source: Microsoft's best practice rule 'Minimize Power Query transformations', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; https://learn.microsoft.com/en-us/power-query/best-practices

**6. Dataverse.** A query on `CommonDataService.Database` sets `CreateNavigationProperties=false`, unless it expands relationship columns. A native query on Dataverse runs through `Value.NativeQuery` with `EnableFolding=true`; without it nothing folds. Choose the columns in an early step: fetching every column can run past ten minutes and fail. Check: P004 (warn). Source: https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-modeling-guidance-for-power-platform

**7. Local files.** A query does not read a file from a local drive (`C:\...`): the published model cannot reach it without a gateway. Use a shared location the service can reach. If a gateway is the deliberate design, record it in section 6 of the brief and list the table in section 9 with P005. Check: P005 (warn). Source: checklist item 2; https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-onprem

**8. Parameters for environments.** When the model moves between two or more environments, or reads two or more servers, databases, workspaces, paths or URLs, those values are parameters (checklist item 1). Where one fixed source is intended, parameters are not added just to have them (item 9). A parameter is a shared `expression` with `meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]`; always give its type. Shipped examples: `'Store Region'` in `tests/fixtures/examples/Examples.SemanticModel/definition/expressions.tmdl` (used in rule 1) and `WorkspaceId`, `LakehouseId` in `tests/fixtures/examples/storage/DirectLake.SemanticModel/definition/expressions.tmdl`. Ask the developer how many environments exist; record it in section 3 of the brief. No check: the files do not show the environments. Source: checklist items 1 and 9; https://learn.microsoft.com/en-us/power-query/power-query-query-parameters ; microsoft/skills-for-fabric, skill semantic-model-authoring, modeling-guidelines.md

**9. Data types set in Power Query.** Every column gets its type in Power Query or at the source, above all from text and CSV files. No column reaches the model as type any. Item 6 asks that every key, sort-by column, date column and number column a measure reads is typed somewhere. In M, the type goes in the table type (`Int64.Type`, `Currency.Type`, `text`, `datetime`) or in a type step. No check: `dataType` in the table file is the model's type, not proof that Power Query set it. Source: checklist item 6; https://learn.microsoft.com/en-us/power-query/data-types ; https://learn.microsoft.com/en-us/power-query/best-practices

**10. Only the rows and columns needed.** Choose columns and filter rows as early as possible, in steps that fold. Keep First Rows is a development aid; remove it before publishing. Item 5: no loaded column nobody uses unless the reason is written down; review when more than 10% of loaded columns are unused. Part B gives the techniques. Source: checklist item 5; https://learn.microsoft.com/en-us/power-bi/guidance/import-modeling-data-reduction ; https://learn.microsoft.com/en-us/power-query/best-practices

**11. Background preview data.** Power Query keeps preview rows for every query, and fetching them can lengthen a refresh when a file has many queries. The setting is a Power BI Desktop option for the current file: File > Options and settings > Options > Data Load, "Allow data preview to download in the background". It is not in the project files. In a model with many queries, Copilot tells the developer about it once, and that preview data can then be stale (Refresh Preview on the Home ribbon updates it). The page's title and its text point different ways: see "Where sources disagree". No check. Source: https://learn.microsoft.com/en-us/power-bi/guidance/power-query-background-refresh

**12. Enable load and Include in report refresh.** A query that only feeds other queries is not loaded into the model. In this template it is a shared `expression`, as `'Sales Source'` is, never a hidden table. A query on data that never changes may have "Include in report refresh" off; it is then skipped by the service refresh too. Both are set by the developer in Power Query in Power BI Desktop; Copilot does not write them. No check. Source: https://learn.microsoft.com/en-us/power-bi/guidance/import-modeling-data-reduction ; https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-include-in-report-refresh

## B. Data reduction and data types

A smaller model refreshes faster, answers faster and fits its capacity. Each technique below is Microsoft's, restated as a rule. On an existing model, list what could go and change nothing without the developer's yes: removing a column can break reports. Source for the whole part: https://learn.microsoft.com/en-us/power-bi/guidance/import-modeling-data-reduction

**13. Columns nobody uses.** Keep a column only when reports use it or the model needs it (relationships, measures, security rules, colour formatting). Adding a column later is easier than removing one. Hidden columns and measures that nothing refers to are listed: M201 (note; model standard rule 15). Visible columns nobody uses are judged in the review (item 5).

**14. Rows nobody needs.** Do not load all history by default. Filter facts by date with parameters, or by a period relative to the refresh date. A model per region or business unit (filtering by entity) is another way, and can remove the need for row-level security. No check: ask the developer how much history reports need.

**15. Group and summarise.** Loading facts at a higher grain (per day instead of per order line, or per month) shrinks a model the most. The cost is lost detail. A DirectQuery detail table behind a drillthrough page can bring the detail back (rule 22). No check: the grain is the developer's decision; record it in section 4 of the brief.

**16. The right data type.** Number columns compress best. Where a text code has a fixed prefix (`SO123456`), remove the prefix at the source or in Power Query, store a whole number, and set `summarizeBy: none`. No floating-point `double`: M108 (warn; model standard rule 10). Remove binary columns before the end of the query: they can make a gateway refresh fail (no check). Source: also https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-data-types

**17. Power Query columns before calculated columns.** A column computed in Power Query or at the source compresses better and refreshes faster than a DAX calculated column. Use DAX only when the formula needs a measure or a DAX-only function. A calculated table is not for shaping data that belongs upstream (item 38). Checks: M105 (fail), M106 (warn); model standard rule 8. Source: also checklist item 38

**18. Date and time apart.** A column that holds a date and a time has many more distinct values than a date. Split it into a date column and a time column, or round the time away if nobody needs it. Check: M111 (warn; model standard rule 11). Source: also Microsoft's best practice rule 'Split date and time', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json

**19. Staging queries not loaded.** See rule 12. Auto date/time adds hidden tables too: rule in the file `relationships-and-dates.md` beside this one.

**20. Columns with too many distinct values.** A text column stores every distinct value once in a dictionary, so its size grows with the number of distinct values, not the number of rows. Such columns make the model bigger and refresh and queries slower. Typical ones: GUIDs, transaction numbers, keys glued from several columns, date-times, and long free text (Microsoft's rule flags text over 100 characters in more than 500,000 rows). Reduce them:

- Drop the column when no report or rule needs it.
- Split it: date from time, a glued key into its parts.
- Round it: the time to the hour or minute, or to midnight.
- Turn text into a number (rule 16).
- Avoid both-direction relationships on such a column.
- The files do not show distinct counts. Take them from the developer, or from the file `data-facts.md` beside this one when Microsoft's modeling server is set up, and record them in section 4 of the brief. No check.
- Source: also microsoft/skills-for-fabric, skill semantic-model-authoring, modeling-guidelines.md; Microsoft's best practice rules 'Reduce usage of long-length columns with high cardinality', 'Split date and time' and 'Avoid bi-directional relationships against high-cardinality columns', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json

**21. Large tables.** A large fact table gets partitions or incremental refresh (rule 26). Model standard rule 14 holds the line Microsoft's rule draws, and where the decision is recorded. A very large fact table can also move to DirectQuery, with an imported summary table for most visuals (rules 22 and 25).

## C. Storage modes

**22. Choose the mode on purpose.** Prefer Import. Choose another mode only for a reason, and record it in section 3 of the brief ("Import, DirectQuery or both, and why"). Checklist item 16: a freshness need of 15 minutes or less, or near real time, may justify DirectQuery; a visual slower than 2 seconds in Import because of size or freshness calls for a review of the mode. The mode is the `mode:` line under each `partition`.

- Import (`mode: import`): the default; fastest queries; data as fresh as the last refresh. Example: Sales in `tests/fixtures/examples/Examples.SemanticModel/definition/tables/Sales.tmdl`.
- DirectQuery (`mode: directQuery`): data too large to import, or needed near real time; every visual queries the source. Example: Sales in `tests/fixtures/examples/storage/DirectQuery.SemanticModel`.
- Dual (`mode: dual`): a dimension that DirectQuery facts from the same source use; answered from memory or from the source. Examples: Store and Date in the same folder.
- Direct Lake (`mode: directLake`, `partition X = entity`): data already in Delta tables in Fabric and too large to copy. Example: `tests/fixtures/examples/storage/DirectLake.SemanticModel`.
- A DirectQuery table changed to Import or Dual cannot be switched back in Power BI Desktop. Tell the developer before the change.
- No check of the choice itself. Source: checklist item 16; https://learn.microsoft.com/en-us/power-bi/guidance/composite-model-guidance ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-storage-mode

**23. Composite models.** A model that mixes modes can be slower and can give unexpected results; use one only when needed.

- An imported dimension that filters a DirectQuery fact from the same source becomes Dual, so its relationship is not limited. Check: M706 (warn).
- A relationship between source groups is limited: fact rows with no matching key disappear from results. Keep keys matching on both sides, and keep the related columns under 50,000 distinct values (no check).
- A calculated column in a DirectQuery table may only use values of its own row. With an iterator or CALCULATE it saves, then errors in a visual. Check: M705 (fail).
- A relationship on a calculated column of a DirectQuery table: use a real source column instead; COMBINEVALUES is the one allowed form. Check: M704 (warn).
- Values from one source can be sent inside queries to another source; Power BI Desktop warns about this. No check.
- The measures table of a DirectQuery or Direct Lake model is a calculated table (model standard rule 1; the shipped `_Measures.tmdl` in both storage examples).
- Source: https://learn.microsoft.com/en-us/power-bi/guidance/composite-model-guidance ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-storage-mode ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-composite-models ; https://learn.microsoft.com/en-us/power-bi/guidance/directquery-model-guidance

**24. DirectQuery tables.** Much of the tuning belongs in the source; involve the people who run it.

- Each query maps to one source table or view, with no transformation or type steps: every step is repeated in every query sent to the source. Check: M702 (warn).
- No filter on the current date in Power Query (`DateTime.LocalNow` and similar); keep relative-period columns in the date table instead. Check: M703 (warn).
- Time intelligence functions can be slow: M513 (warn; DAX standard rule 17).
- Relationships: single direction; no keys of GUID type; an "unknown" row at the source for fact keys with no match; Assume Referential Integrity turned on in Power BI Desktop when the source guarantees matches, so inner joins are used. No check.
- Source: https://learn.microsoft.com/en-us/power-bi/guidance/directquery-model-guidance ; Microsoft's best practice rule 'Measures using time intelligence and model is using Direct Query', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json

**25. Aggregations.** An aggregation table holds the facts of a large DirectQuery table at a higher grain, usually imported. Power BI answers summary queries from it and goes to the detail table only for detail. Report authors see the detail table; the aggregation table is hidden.

- Requirements Microsoft lists: the detail table is DirectQuery; each aggregation column has the data type of its base column (counts excepted); no chain across three or more tables; no column mapped twice; no grouping by a key whose only relationship is inactive and turned on with USERELATIONSHIP.
- Row-level security must filter the aggregation table and the detail table alike, or the aggregation is not used.
- Aim for at least ten times fewer rows than the detail table. A hybrid table (rule 26) cannot have aggregations. An aggregation table set to Import cannot change mode again.
- In the files, each column of the aggregation table carries `alternateOf`: `baseColumn` alone for a grouping column; `summarization` with `baseColumn` for sum, min, max or count of a column; `summarization: count` with `baseTable` for a row count. Copy the form from the table `'Sales Aggregate'` in `tests/fixtures/examples/storage/DirectQuery.SemanticModel`:

```
	column Amount
		dataType: decimal
		formatString: #,0.00
		summarizeBy: none
		sourceColumn: Amount

		alternateOf
			summarization: sum
			baseColumn: Sales.Amount
```

- A model with DirectQuery tables and no `alternateOf` anywhere gives note U004: a suggestion, never a request.
- Checklist item 17: review aggregations when a fact table has 50 million rows or more, or DirectQuery detail queries take over 2 seconds again and again. Do not force them where the scale does not call for it. Row counts and query times come from the developer.
- Source: https://learn.microsoft.com/en-us/power-bi/transform-model/aggregations-advanced ; https://learn.microsoft.com/en-us/power-bi/guidance/composite-model-guidance ; Microsoft's best practice rule 'Consider using aggregations if using Direct Query in Power BI', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; checklist item 17

**26. Incremental refresh.** A large, growing fact table refreshes only its newest period.

- Two parameters, spelled exactly `RangeStart` and `RangeEnd` (case matters), both of type Date/Time, even when the source column is a whole-number date key: convert in the filter. Check: M707 (fail; a parameter missing, or not Date/Time).
- The filter includes one end only: `>= RangeStart` and `< RangeEnd`. With `<=` on both ends a boundary row can load twice. Check: M709 (fail).
- The filter must fold, or each refresh reads every row. With a native query the filter may not fold: put the parameters inside the statement, or read a table or view. Check: M708 (warn).
- The table carries a `refreshPolicy`: how much history to keep (`rollingWindowGranularity`, `rollingWindowPeriods`), what to refresh (`incrementalGranularity`, `incrementalPeriods`) and the query (`sourceExpression`). Every table with a policy uses the same two parameters.
- A hybrid table adds a DirectQuery partition for the newest data on top of the policy; it needs Premium, Premium Per User or Embedded capacity.
- Once published, publishing again from Power BI Desktop replaces the partitions and their data. Tell the developer.
- Shipped example: Sales in `tests/fixtures/examples/Examples.SemanticModel/definition/tables/Sales.tmdl`, with both parameters in `expressions.tmdl` of the same model:

```
	refreshPolicy
		policyType: basic
		rollingWindowGranularity: year
		rollingWindowPeriods: 2
		incrementalGranularity: day
		incrementalPeriods: 7
		sourceExpression =
			let
			    // Start from the shared staging query of order lines.
			    Source = #"Sales Source",
			    // Keep the order lines inside the window that RangeStart and RangeEnd set.
			    #"Filtered Rows" = Table.SelectRows(Source, each [Order Date] >= RangeStart and [Order Date] < RangeEnd)
			in
			    #"Filtered Rows"
```

- Source: https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview ; https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-configure ; https://learn.microsoft.com/en-us/power-bi/guidance/power-query-folding

**27. Direct Lake.** For data that already lives in Delta tables in Fabric.

- Each table has an `entity` partition (`entityName`, `schemaName`, `expressionSource`) that points to one shared expression; no M in such a table. The shipped expression uses `AzureStorage.DataLake` with the `WorkspaceId` and `LakehouseId` parameters.
- The measures table is a calculated table that names no Direct Lake table: `ROW ( "Placeholder", BLANK () )`, as shipped (model standard rule 1).
- The key on the one side of a relationship must be unique, or queries fail. Related columns have the same data type. No binary or GUID columns.
- Direct Lake on SQL falls back to DirectQuery (for views and SQL security, for example); Direct Lake on OneLake never falls back. On SQL, Auto date/time does not work, and a calculated column or table may not refer to a Direct Lake table; on OneLake that is a preview. Mixing in Import tables works on OneLake only.
- Lakehouse tuning (V-Order, row groups) happens outside the model.
- No check. Source: https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview ; microsoft/skills-for-fabric, skill semantic-model-authoring, direct-lake-guidelines.md

## D. Security

Roles live in `definition/roles/`, one file per role. Who may see what is recorded in section 4 of the brief (items 39, 40, 41); ask the developer when it is empty.

**28. Row-level security.** A role filters the rows of a table; it cannot hide a table or column. A fixed rule names a value: `Store[City] = "Northport"` (role `'Northport Stores'`). A user-based rule compares a column with the signed-in user, through USERPRINCIPALNAME, never USERNAME: USERNAME gives a different form of name in Power BI Desktop and in the service. Check: M603 (warn). Item 41: when two or more audiences share the model with identity-based filtering, review a user-based role that compares the signed-in user with a mapping column or table. Shipped example, the role `'Own Store'` in `tests/fixtures/examples/Examples.SemanticModel/definition/roles`:

```
role 'Own Store'
	modelPermission: read

	tablePermission Store = Store[Manager Email] = USERPRINCIPALNAME ()
```

Source: https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security ; https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance ; checklist item 41

**29. Filter dimensions, not facts.** Put the rule on a dimension table and let the relationship carry it to the facts. Check: M602 (warn). Source: https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance

**30. Keep rules simple.** A rule runs for every row of every query. No LEFT, RIGHT, UPPER, LOWER, FIND or LOOKUPVALUE: store the value to compare in a column at the source and keep the rule a plain comparison. Check: M601 (warn). Source: Microsoft's best practice rule 'Limit row level security (RLS) logic', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance

**31. Unknown users see nothing.** A user-based rule whose last branch is TRUE shows every row to anyone it does not name. End in FALSE. Check: M605 (warn). Source: https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance ; checklist item 41 (fallback for unmatched users)

**32. Many-to-many next to a rule.** A table with a rule and a many-to-many relationship makes queries slow. Relate one dimension many-to-one to the security table instead. Check: M604 (warn). Source: Microsoft's best practice rule 'Avoid using many-to-many relationships on tables used for dynamic row level security', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json

**33. Inactive relationships.** A rule never travels over an inactive relationship, and USERELATIONSHIP towards a secured table errors: M414 and M415, in the file `relationships-and-dates.md` beside this one.

**34. Testing and members.** Roles are tested in Power BI Desktop (View as) and again in the service (Test as role). Members, preferably security groups, are assigned in the Power BI service, not in project files. Rules apply only to people with Viewer access to the workspace, or with Read permission on the model. Item 39: every required role tested, with at least one test case per role; item 41: every user-based mapping tested with representative identities. Only people can give this evidence: record the tests in section 6 of the brief. No check. Source: https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security ; https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance ; checklist items 39 and 41

**35. Object-level security.** Use it when a table or column, name included, must be out of reach of a role (item 40). Hiding a field in the field list is not security. A whole table: `tablePermission 'Sales Target'` with `metadataPermission: none` (role `'No Sales Targets'`). A column: `columnPermission 'Unit Cost' = none` (role `'No Product Cost'`). Measures that refer to a secured object are secured with it.

- A visual that uses a secured field looks broken to people in that role. Check: M606 (warn).
- Row rules and object rules for the same people go in one role: a person in a row-only role and an object-only role gets an error at query time. Check: M607 (warn).
- A table between two others in a chain of relationships cannot be secured as a whole: that errors at design time. Secure its columns instead. Check: M608 (fail).
- Limits Microsoft lists: not with Q&A, quick insights, smart narrative or the Excel Data Types gallery; not in a composite model built on a remote semantic model.
- Source: https://learn.microsoft.com/en-us/fabric/security/service-admin-object-level-security ; https://learn.microsoft.com/en-us/analysis-services/tabular-models/object-level-security ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-composite-models ; checklist item 40

**36. Common mistakes.**

- USERNAME in a rule: a different name form in Desktop and in the service (rule 28; https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security).
- A rule on the fact table instead of the dimension (rule 29; https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance).
- Hiding a column and calling it secured: hidden fields stay readable; use object-level security (rule 35; checklist item 40).
- Forgetting that roles add up: a person in two roles sees what either role allows, so a "deny" role never wins (https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance).
- Testing only as yourself: for a user-based rule, Test as role uses your own identity; test with other identities and with unexpected values (https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security ; https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance).
- Giving report readers Member or Contributor access: rules then do not apply to them (https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security).
- With aggregations, securing the detail table only (rule 25; https://learn.microsoft.com/en-us/power-bi/transform-model/aggregations-advanced).

## Sources

Read on 11 November 2026. Every rule is restated in this template's own words.

- Microsoft Learn, guidance: https://learn.microsoft.com/en-us/power-bi/guidance/power-query-folding ; https://learn.microsoft.com/en-us/power-bi/guidance/power-query-referenced-queries ; https://learn.microsoft.com/en-us/power-bi/guidance/power-query-background-refresh ; https://learn.microsoft.com/en-us/power-bi/guidance/import-modeling-data-reduction ; https://learn.microsoft.com/en-us/power-bi/guidance/directquery-model-guidance ; https://learn.microsoft.com/en-us/power-bi/guidance/composite-model-guidance ; https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance ; https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-modeling-guidance-for-power-platform ; https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization
- Microsoft Learn, Power Query: https://learn.microsoft.com/en-us/power-query/best-practices ; https://learn.microsoft.com/en-us/power-query/step-folding-indicators ; https://learn.microsoft.com/en-us/power-query/query-folding-examples ; https://learn.microsoft.com/en-us/power-query/power-query-query-parameters ; https://learn.microsoft.com/en-us/power-query/data-types
- Microsoft Learn, features: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-storage-mode ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-composite-models ; https://learn.microsoft.com/en-us/power-bi/transform-model/aggregations-advanced ; https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview ; https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-configure ; https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-include-in-report-refresh ; https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-onprem ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-data-types ; https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview
- Microsoft Learn, security: https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security ; https://learn.microsoft.com/en-us/fabric/security/service-admin-object-level-security ; https://learn.microsoft.com/en-us/analysis-services/tabular-models/object-level-security
- Microsoft's best practice rules (MIT), category "Performance" and the security rules; rule names are given without their category prefix: https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json
- Microsoft's skill (MIT), microsoft/skills-for-fabric, skill semantic-model-authoring: https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/modeling-guidelines.md ; .../references/tmdl-guidelines.md ; .../references/direct-lake-guidelines.md
- The owner's checklist, `checklist/checklist.md`, items 1 to 6, 9, 16, 17, 38 to 41.

Where sources disagree, and what was decided. Order of trust: the owner's checklist; Microsoft Learn; Microsoft's skills and best practice rules.

- Background preview: the Learn page is titled "Disable Power Query background refresh" and explains that fetching previews lengthens refresh, yet its recommendation (read on 11 November 2026) says to turn "Allow data preview to download in the background" on. The template takes no side: Copilot names the option, says the page is unclear, and the developer compares refresh times with the option on and off. No check either way.
- Folding indicators: Learn's folding pages point to them, but they exist in Power Query Online only. In Power BI Desktop, View Native Query is the test (rule 2).
- Native queries and incremental refresh: the folding guidance says incremental refresh cannot use a native query; the incremental refresh pages accept one that carries the parameters inside the statement. M708 warns rather than fails.
- Heavy reshaping: Microsoft's rule flags a query with any one of the listed functions (and any native query); P006 warns at three distinct functions in an Import query, so that a normal query does not warn. Native queries are handled by P002, M701 and M708.
- Rule functions: Microsoft's rule lists LEFT, RIGHT, UPPER, LOWER and FIND; Learn's RLS guidance adds LOOKUPVALUE. M601 checks all six.
- Hiding keys in DirectQuery: Learn's DirectQuery guidance lets the many-side key stay visible to save a join; model standard rule 7 hides it (M102). The model standard stands; a visible key in a DirectQuery model goes in section 9 with M102 and its reason.
- Large tables: Microsoft's rule draws the line at 25 million rows (partitions, model standard rule 14); checklist item 17 reviews aggregations at 50 million. They are different decisions; both stand.

Not confirmed from Microsoft: that Power BI Desktop saves a query with Enable load off as a shared `expression` (the shipped `'Sales Source'` follows this form); how "Include in report refresh" is written in TMDL; where the background preview option is stored; the TMDL spelling of Assume Referential Integrity, which is why the developer sets it in Desktop; that Microsoft's modeling server reports whether a step folds.

Checklist items: 1-6, 9, 16, 17, 38-41
