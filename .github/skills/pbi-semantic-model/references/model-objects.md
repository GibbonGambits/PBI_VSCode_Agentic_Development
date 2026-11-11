# Model objects: when to use each, and how to build it

This file says, for each kind of model object, when to use it, how it is written in TMDL, which shipped example to copy, what the check reads, and what Microsoft says can go wrong.
The rule: copy the shipped example, change names and fields, run `python scripts/check_project.py .`; ask only when no example exists.
The index of examples is `tests/fixtures/examples/INDEX.md`. All example paths below start at `tests/fixtures/examples/`.
Nothing in the examples has been opened in Power BI Desktop yet, so the developer looks at the first use of each kind in Desktop.

A suggestion (a note that starts with U) is mentioned once, at the end of a task. Build it only after the developer's yes; a preview feature also needs its row in section 11 of the brief. Source: `.github/skills/pbi-semantic-model/SKILL.md` ("A better native feature").

## A. User-defined functions

**1. Release status.** Generally available in Power BI Desktop and the service since the June 2026 release. The model needs compatibility level 1702 or higher. Microsoft Learn names the release, not a build; the update archive lists the June 2026 Desktop as version 2.155.756.0. Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions ; https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-latest-update-archive

**2. What it is for.** A function holds one piece of DAX logic once. Measures, calculated columns, visual calculations and other functions then call it like a built-in function. Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-user-defined-functions-overview

**3. When to suggest one.**
- The check gives note U001 when three or more measures have the same formula with only names and texts changed (formulas of 12 tokens or more).
- Microsoft suggests a function to share the logic of dynamic format strings. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-dynamic-format-strings
- Microsoft suggests a function in place of a measure that is reused as a format string, because a calculation group turns every measure into the variant type. Source: https://learn.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups ("Considerations")

**4. How it is written.** All functions go in `definition/functions.tmdl`. One function: a `///` description line, then `function Name = ( parameter : TYPE ) => body`. A parameter with `= value` after its type is optional. Source: the Learn page in rule 1.

Copied from `Examples.SemanticModel/definition/functions.tmdl`:

```tmdl
/// Example of a user-defined function with typed parameters: returns the amount including tax; the rate is optional and is 0.21 when left out.
function AddTax = ( amount : NUMERIC, taxRate : NUMERIC = 0.21 ) => amount * ( 1 + taxRate )
```

**5. Parameter types and modes.** A function takes 0 to 256 parameters. With no type, a parameter is `AnyVal val`. Source: the Learn page in rule 1.

| Family | Types | Mode |
|---|---|---|
| Values: worked out once, before the call, in the caller's row and filter context | `AnyVal`, `Scalar`, `Table`. A scalar may name a subtype: `Variant`, `Int64`, `Decimal`, `Double`, `String`, `DateTime`, `Boolean`, `Numeric` (a subtype alone implies `Scalar`) | `val` (default) or `expr` |
| References: passed as they are and worked out inside the function, with the filter context only | `AnyRef`, `CalendarRef`, `ColumnRef`, `MeasureRef`, `TableRef` | `expr` only; `val` is not allowed |

- Use `val` when the value must be fixed before the function runs. Use `expr` when the function must change the context, for example inside CALCULATE.
- Value types convert the argument to the type; reference types do not.

**6. Names.** Microsoft's must-rules: a function name is unique in the model; it holds letters, digits and underscores, with single dots between parts (no dot at the start or end, no two dots in a row); it is not the name of a built-in DAX function or a reserved word. A parameter name holds letters, digits and underscores, no dots, and is not a reserved word. Check: M802 (fail). It reads the function name only, and also refuses a function named like a table. Source: the Learn page in rule 1.

Guidance, not checked: SQLBI advises names in PascalCase, a dot prefix that groups related functions (a model-specific prefix such as `Local.` for functions tied to this model, a library or company prefix for shared ones), parameters in camelCase, and a reference parameter whose name ends with its kind (for example `...Column`, `...Measure`). Source: https://www.sqlbi.com/articles/model-dependent-and-model-independent-user-defined-functions-in-dax/ ; https://www.sqlbi.com/articles/understanding-parameter-types-in-dax-user-defined-functions-udf/

**7. Rules and codes.**
- A model with a function is at compatibility level 1702 or higher (`compatibilityLevel: 1702` in `database.tmdl`). Check: M801 (fail). Source: the Learn page in rule 1.
- The name follows rule 6. Check: M802 (fail).
- Every function has a `///` description that says what it returns and what each parameter means; a `//` comment does not show in IntelliSense. Check: M803 (warn). Source: the Learn page in rule 1.
- Every parameter has a type. Check: M804 (warn). Source: the Learn page in rule 1 (type hints make a function safer and more predictable).
- A function never calls itself, directly or through another function. Check: M805 (fail; it sees a direct call only). Source: the Learn page in rule 1.
- Inside a function, write every column with its table. Microsoft reads a bare name as a measure, so renames and dependency tracking can miss it. No check (M010 does not read functions). Source: the Learn page in rule 1; rule 10 of the file `dax-standard.md` beside this one.

**8. Limits Microsoft lists.** No recursion and no overloading. No declared return type, no parameter descriptions, no enum return value. A function cannot be hidden, put in a display folder or translated. Not supported in a model without tables. Object-level security does not flow into a function: a function that names a secured measure is not secured itself, so never name secured objects in a function's name or description. A measure of a composite model cannot call a function of the source model. In a calculated column, return one scalar type (wrap the call in CONVERT if needed). IntelliSense is limited in the VS Code TMDL extension. Source: the Learn page in rule 1, "Considerations and limitations".

**9. How a measure calls one.** In `Examples.SemanticModel/definition/tables/_Measures.tmdl`, the measure `Total Sales with Tax` calls `AddTax ( [Total Sales] )` and leaves out the optional rate. The measure `Store Share of Sales (%)` passes a measure and a column to `ShareOfAll`, whose parameters are `MEASUREREF` and `COLUMNREF`.

**10. What the check reads.** In `functions.tmdl`: each function's name, its `///` line, its parameter list (a parameter with no `:` has no type) and the calls in its body. In `database.tmdl`: `compatibilityLevel`. It does not read parameter names, modes or defaults.

## B. Calculation groups

**1. What it is.** A calculation group is a table whose calculation items apply one pattern to whatever measure is in the visual, through `SELECTEDMEASURE ()`. Microsoft says it can sharply cut the number of redundant measures, most often time intelligence variants. Status: generally available. Source: https://learn.microsoft.com/en-us/power-bi/transform-model/calculation-groups ; https://learn.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups

**2. When to suggest one.** The check gives note U002 when six or more measures use time intelligence functions and the model has no calculation group. Checklist item 35 asks to keep base measures apart from their variants; a calculation group gives every base measure the same variants.

**3. How it is written.** Copy `Examples.SemanticModel/definition/tables/Time Calculation.tmdl`.
- `table` with a `///` description, then `calculationGroup` with `precedence:` and one `calculationItem` per variant, each with its own `///` line.
- An item that needs its own format gets `formatStringDefinition = "<format>"` below its formula (the item `PY Change (%)` uses `"0.0%"`).
- A visible text column with `sourceColumn: Name` and `sortByColumn: Ordinal`; a hidden whole-number column `Ordinal` with `sourceColumn: Ordinal`. The order of items does not change how they are evaluated.
- `partition '<table>' = calculationGroup` with `mode: import`.
- Source: the two Learn pages in rule 1.

Copied from `Examples.SemanticModel/definition/tables/Time Calculation.tmdl` (the start):

```tmdl
table 'Time Calculation'

	/// Example of a calculation group with a precedence.
	calculationGroup
		precedence: 10

		/// The measure as it is.
		calculationItem Current = SELECTEDMEASURE ()
```

**4. Implicit measures off.** `model.tmdl` carries `discourageImplicitMeasures`. Why: calculation items apply to explicit measures only, and Power BI requires this setting before it makes a calculation group. Check: M814 (warn). Source: the AS page in rule 1.

**5. Rules and codes.**
- Every group has at least one item. Check: M811 (warn).
- Every item has a `///` description. Check: M812 (warn). Source: checklist item 30 (every calculation group documented).
- The group's table has a `///` description that states its purpose. Check: D001 (fail). Source: checklist item 30.
- With two or more groups, each has its own `precedence` number. A higher number wraps the lower ones, and only the highest group's format string applies. Check: M813 (warn). Source: the AS page in rule 1 ("Precedence").
- Checklist item 30 also asks that each item's format string and result are tested. No script can do that: list the items for the developer to check in Desktop.

**6. What breaks, from Microsoft.**
- Once a group exists, reports read every measure as the variant type. A measure reused as a dynamic format string can then fail: use `FORMAT ( [Measure], "" )` or a user-defined function.
- An item that does arithmetic on a text measure (a dynamic title, a format-string measure) gives "Cannot convert value ... of type Text". Guard the item with `ISNUMERIC ( SELECTEDMEASURE () )`.
- Implicit column totals do not work.
- Not supported: object-level or row-level security on the group's table, detail rows expressions, the smart narrative visual. With a live connection, the group's format strings do not reach report-level measures.
- An item takes effect only when exactly one item of the group is in the filter. An item may refer to another item of the same group through CALCULATE; no other recursion.
- Source: the AS page in rule 1 ("Considerations", "Limitations", "Sideways recursion"); the Power BI page in rule 1.

**7. What the check reads.** A table is a calculation group when it holds `calculationGroup`. The check reads its items and their `///` lines, its `precedence`, the table's `///` line, and `discourageImplicitMeasures` in `model.tmdl`. It does not read what an item does.

**8. In the report.** Put the group's visible column (here `'Time Calculation'[Time Calculation]`) in a slicer, or on the columns of a matrix that shows a measure. Source: the AS page in rule 1.

## C. Field parameters

**1. When to suggest one.** When two or more measures or fields compete for the same place on a page, so readers switch them with one slicer. Source: checklist item 64; https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters
- Note U003: a measure switches between measures with SWITCH and SELECTEDVALUE, and the model has no field parameter.
- Note U103 on the report side: bookmarks swap two visuals of the same kind in the same place.
- Status: no preview label on Microsoft Learn; the update archive lists it as generally available since July 2025.

**2. The model side, exactly.** A calculated table. Source: microsoft/skills-for-fabric, skill semantic-model-authoring, `field-parameters.md` and `tmdl-guidelines.md`; the tuple form also on the Learn page in rule 1.
- The partition `= calculated`, `mode: import`, and a source that is a list of tuples: `("<label>", NAMEOF('<Table>'[<Field>]), <order>)`. Columns and measures may be mixed.
- Three columns, bound to `[Value1]`, `[Value2]` and `[Value3]`:
  - the label column (`[Value1]`): visible, `dataType: string`, `sortByColumn:` the order column, and `relatedColumnDetails` with `groupByColumn:` the fields column;
  - the fields column (`[Value2]`): hidden, `sortByColumn:` the order column, and `extendedProperty ParameterMetadata = {"version":3,"kind":2}`;
  - the order column (`[Value3]`): hidden, `dataType: int64`.
- The value `{"version":3,"kind":2}` comes from Microsoft's own skill and from saved projects. No Microsoft Learn page states it. The check knows a field parameter only by this property.
- `annotation CalculatedReason = ...`: this template's rule for every calculated table (rule 8 of the file `model-standard.md` beside this one; M105, fail). For a field parameter the reason line simply says it is a field parameter.
- `///` descriptions on the table and on the label column (D001, fail).

Copied from `Examples.SemanticModel/definition/tables/Sales Metric.tmdl` (the two hidden columns and the partition):

```tmdl
	column 'Sales Metric Fields'
		dataType: string
		isHidden
		summarizeBy: none
		sourceColumn: [Value2]
		sortByColumn: 'Sales Metric Order'

		extendedProperty ParameterMetadata = {"version":3,"kind":2}

	column 'Sales Metric Order'
		dataType: int64
		isHidden
		summarizeBy: none
		sourceColumn: [Value3]

	partition 'Sales Metric' = calculated
		mode: import
		source =
				{
				    ("Total Sales", NAMEOF('_Measures'[Total Sales]), 0),
				    ("# Order Lines", NAMEOF('_Measures'[# Order Lines]), 1),
				    ("Average Line Amount", NAMEOF('_Measures'[Average Line Amount]), 2)
				}
```

**3. Adding or removing a field.** Rewrite the whole tuple list; a field left out is gone. Keep the order numbers from 0 with no gaps. Leave the three columns, the sort-by, the group-by and `ParameterMetadata` as they are. Renaming the table or the label column changes what report slicers bind to: run `python scripts/find_references.py . "<Table>"` first. Source: microsoft/skills-for-fabric, skill semantic-model-authoring, `field-parameters.md`.

**4. Rules and codes.**
- Every NAMEOF names a column or measure the model has, written with its table (`NAMEOF('_Measures'[Total Sales])`, not `NAMEOF([Total Sales])`). The check reads only NAMEOF calls that name a table, and finds the field among that table's columns and measures. Check: M821 (fail; the check's own reason: the table then fails to load). Source: the Learn page in rule 1 (each entry is a label, a NAMEOF reference and an order number; no extra columns).
- Exactly one visible column, the label; it carries `relatedColumnDetails` with `groupByColumn`; the fields column is hidden. This is the shape Power BI Desktop writes. Check: M822 (warn). Source: microsoft/skills-for-fabric, skill semantic-model-authoring, `tmdl-guidelines.md`.
- A field parameter is not asked for a relationship (M411 skips it).

**5. Limits Microsoft lists.** A date column in a field parameter loses its auto date/time hierarchy. AI visuals and Q&A do not support field parameters. Readers cannot pick "none"; no selection means all. A live connection needs a local model first. Implicit measures cannot be used: make explicit measures. A field parameter cannot be the linked field of a drillthrough or tooltip page. Source: the Learn page in rule 1.

**6. The report side** is in the file report-standard.md of the skill pbi-report.

**7. Examples.** Over measures: `Examples.SemanticModel/definition/tables/Sales Metric.tmdl` (Sales Metric). Over columns: `Examples.SemanticModel/definition/tables/Sales Breakdown.tmdl` (Sales Breakdown).

## D. Other object kinds

**Measures table.** Every measure lives in `_Measures` (rule 1 of the file `model-standard.md` beside this one; M001, M002, fail). If the model has none: `python scripts/scaffold.py measures-table .`. It picks the form from the storage modes: an imported table with one hidden column and no rows (`measures-table/import.tmdl`), or, for Direct Lake or DirectQuery, a calculated table `ROW ( "Placeholder", BLANK () )` with its reason line (`measures-table/calculated.tmdl`). `--form import|calculated` overrides. Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-measures

**Numeric range ("what-if") parameter.** For a reader to pick a number that measures use, such as a discount. A calculated table made with GENERATESERIES, one column bound to `[Value]`, plus a measure that reads the pick with SELECTEDVALUE and a default. Example: `Examples.SemanticModel/definition/tables/Discount Percentage.tmdl` and the measure `Discount Percentage Value` in `_Measures.tmdl`. It needs `CalculatedReason` (M105, fail). Microsoft: more than 1,000 values are sampled; it is meant for measures, and in a calculated column the value may be wrong. Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-what-if

**Dynamic format string.** For a measure whose format depends on the value or the selection while the result stays a number. Write `formatStringDefinition =` with DAX under the measure; refer to the value with `SELECTEDMEASURE ()`. Note U005: a measure returns text made with FORMAT. Cannot be used with report-level measures. Visuals with display units on Auto can override it. Example: the measure `Total Sales After Discount` in `Examples.SemanticModel/definition/tables/_Measures.tmdl`. Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-dynamic-format-strings

**KPI on a measure.** For a base measure with a target and a status. Under the measure: `kpi` with `targetExpression`, `statusExpression` and `statusGraphic`. Example: `Total Sales vs Target (%)` in `_Measures.tmdl`. Microsoft shows model KPIs in tables, matrices and cards as Value, Goal and Status. No check. Source: https://learn.microsoft.com/en-us/analysis-services/tabular-models/kpis-ssas-tabular ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-import-and-display-kpis

**Detail rows.** For the rows a reader gets on drill to details, such as an Excel double-click. Under the measure: `detailRowsDefinition =` with SELECTCOLUMNS over the fact table. Example: `# Order Lines` in `_Measures.tmdl`. Not supported in a model with a calculation group. No check. Source: https://learn.microsoft.com/en-us/analysis-services/tutorial-tabular-1400/as-supplemental-lesson-detail-rows ; https://learn.microsoft.com/en-us/dax/detailrows-function-dax

**Hierarchies.** For natural drill paths, such as year to day or category to product (checklist item 59; rule 13 of the file `model-standard.md` beside this one). In the table: `hierarchy`, then `level` blocks with `column:`. Columns of one table only; no measures. Examples: `Calendar` in `Examples.SemanticModel/definition/tables/Date.tmdl`, `Product Hierarchy` in `Product.tmdl`. Note U007 is in the file `relationships-and-dates.md` beside this one. Source: https://learn.microsoft.com/en-us/analysis-services/tabular-models/hierarchies-ssas-tabular

**Display folders.** `displayFolder: Subject\Type` on measures (rule 2, M003, M004, fail) and one of four folders on columns of a wide table (rule 6, M101, warn), both in the file `model-standard.md` beside this one. A backslash makes a subfolder. Functions cannot go in folders. Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-measures

**Perspectives.** A named subset of tables, columns, measures and hierarchies, used by Personalize visuals and as the default view in Explore. A perspective is not security: every object stays reachable. File `definition/perspectives/<Name>.tmdl` with `perspective`, `perspectiveTable` (or `includeAll`), `perspectiveColumn`, `perspectiveMeasure`, `perspectiveHierarchy`, and `ref perspective` in `model.tmdl`. Example: `Examples.SemanticModel/definition/perspectives/Sales Overview.tmdl`. Check: M831 (warn) for a perspective that holds nothing. Source: https://learn.microsoft.com/en-us/analysis-services/tabular-models/perspectives-ssas-tabular ; https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-personalize-visuals

**Translations and cultures.** Translations change the names, descriptions and display folders readers see in their language; data values and report text are not translated. File `definition/cultures/<locale>.tmdl` with `cultureInfo`, `translations`, then `caption:` and `description:` per object, and `ref cultureInfo` in `model.tmdl`. Example: `Examples.SemanticModel/definition/cultures/nl-NL.tmdl`. Functions cannot be translated. Linguistic metadata (`linguisticMetadata`, as in `cultures/en-US.tmdl`) is edited by a person in Power BI, never written by hand: rule 17 of the file `model-standard.md` beside this one. Source: https://learn.microsoft.com/en-us/analysis-services/tabular-models/translations-in-tabular-models-analysis-services ; https://learn.microsoft.com/en-us/power-bi/guidance/multiple-language-translation

**Annotations and extended properties of your own.** For facts a tool keeps on an object. `annotation Name = value` or `extendedProperty Name = {json}`, one level below the object. Example: `ExampleSource` and `ExampleSettings` in `Examples.SemanticModel/definition/tables/Store.tmdl`. Never write names that start with `PBI_`: Power BI manages those. Source: `.github/instructions/tmdl.instructions.md` rule 6; https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.jsonextendedproperty?view=analysisservices-dotnet

**Shared expressions, parameters and query groups.** A staging query that several tables read, or a value the developer changes in one place. In `definition/expressions.tmdl`: `expression Name = <M>`, a parameter with `meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]`, and `queryGroup:` to file it under a folder declared with `queryGroup` in `model.tmdl`. Examples: `Sales Source`, `Store Region`, `RangeStart`, `RangeEnd` and the groups `Parameters` and `Staging`. Every shared query or parameter has a `///` line (D002, fail). Incremental refresh is in the file `storage-and-security.md` beside this one. Source: https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview ; https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.querygroup?view=analysisservices-dotnet

**Calendars (preview).** For calendar-based time intelligence: fiscal, week-based or other calendars, without a marked date table. Only with the developer's yes and a row in section 11 of the brief. In the date table: `calendar '<Name>'` with `calendarColumnGroup = year`, `month`, `date` and so on, each with `primaryColumn:` and, if needed, `associatedColumn:`; a `calendarColumnGroup` with `column:` lines tags time-related columns. Example: `preview/Calendar.SemanticModel/definition/tables/Date.tmdl` (Shop Calendar) and the measure `Total Sales YTD` in its `_Measures.tmdl`. Microsoft's limits: not yet authored in the service; do not mix with auto date/time tables; not in live-connected or composite models; the table has fewer than 200 columns; a calendar uses only columns of its own table; calendar time intelligence calls cannot be nested; with row-level security on a fact table that holds the calendar, results can mislead. Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-time-intelligence

## E. What is not built here, and why

From `tests/fixtures/examples/INDEX.md`:
- Legacy data sources and `query` partitions: a Power BI project uses Power Query partitions.
- `policyRange` partitions: the service makes them when it applies a refresh policy.
- `variation`: it belongs to Auto date/time, which the standard turns off.
- Connection binding hints.
- Role members: they are assigned in the Power BI service.

## Sources

Read on 11 November 2026. Every rule is restated in this template's own words.

- Microsoft Learn, functions: https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-user-defined-functions-overview ; release dates: https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-latest-update-archive
- Microsoft Learn, calculation groups: https://learn.microsoft.com/en-us/power-bi/transform-model/calculation-groups ; https://learn.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups
- Microsoft Learn, field parameters: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters
- Microsoft Learn, other kinds: the pages named in section D; TMDL: https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview ; https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-reference-tabular-object
- microsoft/skills-for-fabric (MIT), skill semantic-model-authoring, `field-parameters.md` and `tmdl-guidelines.md`: https://github.com/microsoft/skills-for-fabric/tree/main/plugins/powerbi-authoring/skills/semantic-model-authoring
- SQLBI, function naming: https://www.sqlbi.com/articles/model-dependent-and-model-independent-user-defined-functions-in-dax/ ; https://www.sqlbi.com/articles/understanding-parameter-types-in-dax-user-defined-functions-udf/
- This template: `scripts/model_rules.py` (codes M8xx and notes U001 to U005), `scripts/scaffold.py`, `scripts/find_references.py`, `.github/instructions/tmdl.instructions.md`, the owner's checklist (`checklist/checklist.md`) items 30, 35, 59, 64.

Where sources disagree, and what was decided. Microsoft Learn is the higher source.

- Function form: Microsoft's skill shows a function written `function DoubleValue = DoubleValue(Value) = Value * 2`. Microsoft Learn writes `function Name = ( parameters ) => body`. Learn wins; the shipped example uses it.
- Function status: Microsoft Learn says generally available since June 2026. The message of note U001 in `scripts/model_rules.py` still calls functions a preview feature that needs the developer's yes. Learn wins: no row in section 11 is needed; the developer's yes for a suggestion still is.
- Compatibility level: Microsoft Learn's compatibility-level page still names 1700 as the latest level, while the function page requires 1702. The shipped models use 1702.
- Field parameter order column: Microsoft's skill gives it `formatString: 0` and `summarizeBy: sum`; the shipped examples use `summarizeBy: none`, as rule 9 of the model standard prefers. Both pass the check.
- Detail rows and calculation groups: Microsoft says they do not work together, yet the shipped `Examples.SemanticModel` holds both (`# Order Lines` and `Time Calculation`), each to show its syntax. In a real model, do not combine them.

Not confirmed from Microsoft:
- The extended property `ParameterMetadata = {"version":3,"kind":2}` (Microsoft's skill and saved projects only).
- The TMDL form of `kpi`, `detailRowsDefinition` and `queryGroup`: no Learn example; the shipped files were written by Microsoft's TMDL serializer.
- What Power BI Desktop writes on a numeric range parameter table; the shipped example carries no extended property.
- That Desktop keeps a `CalculatedReason` annotation when it saves.

Checklist items: 30, 35, 59, 64
