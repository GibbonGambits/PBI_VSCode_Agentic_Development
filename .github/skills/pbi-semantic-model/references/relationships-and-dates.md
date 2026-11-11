# Star schema, relationships, dates and names

How the tables of a model built from this template fit together: fact and dimension tables, relationships, the date table, columns with a special job, and the names of tables and columns.
`python scripts/check_project.py .` checks it; the code after each rule is the finding it gives (M401 to M417, M113 to M120, M901 to M907; M908 and M909 are in the file `dax-standard.md` beside this one).
An exception passes only when section 9 of `docs/report-brief.md` lists the code and the object exactly as the check prints it, with a reason: a relationship as `Sales[Store Key] to Store[Store Key]`, a column as `Table[Column]`, a table by its name, and a finding on the whole model as `model`.

## A. The star schema

**1. Facts and dimensions.** Every table is either a fact table (events or measurements, one row per event, summed by measures) or a dimension table (the things you filter and group by). Never mix both jobs in one table. A fact table holds rows of one grain only, for example one row per order line; a target set per month goes in its own table. When the source is one wide extract, split it into fact and dimension tables in Power Query. The files do not show grain: ask the developer. No check. Checklist item 10. Source: https://learn.microsoft.com/en-us/power-bi/guidance/star-schema ; https://learn.microsoft.com/en-us/power-bi/guidance/relationships-many-to-many (facts at a higher grain)

- Junk dimension: many small attributes with few values each (an order status, an age group) can be merged into one dimension table with one row per combination and a surrogate key. Build it at the source or in Power Query, and merge the key into the fact query so the relationship is one-to-many. It means fewer tables in the Data pane and a smaller model. No check: the files do not show it. Source: https://learn.microsoft.com/en-us/power-bi/guidance/star-schema
- Degenerate dimension: a fact attribute that readers filter by but that has no table of its own, such as an order number, stays a column of the fact table. This is the one allowed mix of jobs in a table. When several such columns are needed together (order number and order line number), a separate table can be the better design (rule 22). No check. Source: https://learn.microsoft.com/en-us/power-bi/guidance/star-schema ; https://learn.microsoft.com/en-us/power-bi/guidance/relationships-one-to-one
- One model per subject: build each model around one subject and its central facts, not one model for everything. No check: ask the developer. Source: https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-modeling-guidance-for-power-platform
- Wide tables: a table with more than about 30 visible columns usually mixes jobs or holds what belongs in other dimensions. Split it into a proper star. Check: M120 (warn; more than 30 visible columns). Source: Microsoft's skill, https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/modeling-guidelines.md

**2. No fact-to-fact relationship.** Two fact tables never relate to each other directly. They share dimensions instead: each fact relates one-to-many to the same dimension table, so one slicer filters both. Checklist item 10 allows 0 unless the reason is written down. No check of its own; a many-to-many relationship between two facts also raises M406. Source: checklist item 10; https://learn.microsoft.com/en-us/power-bi/guidance/relationships-many-to-many ; Microsoft's skill, https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/modeling-guidelines.md (shared conformed dimension)

**3. Snowflakes.** Flatten a chain of dimension tables (Product, Subcategory, Category) into one dimension table in Power Query, and add a hierarchy for the levels. Keep the chain only when size or use clearly gains from it, and list the table in section 9 with M412. Check: M412 (warn; a table that is the many side of one relationship and the one side of another). Source: https://learn.microsoft.com/en-us/power-bi/guidance/star-schema ; Microsoft's best practice rule 'Consider a star-schema instead of a snowflake architecture', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; checklist item 10

**4. Every table is related.** A data table without any relationship filters nothing and is filtered by nothing. Relate it, or list it in section 9 with M411 and its purpose (a table that only feeds a slicer or a formula is a valid reason). The check leaves out the measures table, calculation groups, field parameters and numeric range parameters; this list of exempt tables is this template's choice. It runs only when the model has two or more other tables. Check: M411 (warn). Source: Microsoft's best practice rule 'Ensure tables have relationships', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; Microsoft's skill, modeling-guidelines.md (address in rule 2: every table except utility tables)

**5. One column, one place.** A fact table does not repeat a descriptive column of the dimension it relates to (City in Sales when Store has City). Keep it in the dimension. Check: M115 (warn; a column of the many-side table with the same name as a column of its one-side table, outside the relationship). Source: Microsoft's best practice rule 'Remove redundant columns in related tables', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; https://learn.microsoft.com/en-us/power-bi/guidance/star-schema

**6. No column per month.** Twelve number columns named after the months are unpivoted in Power Query into one month column and one value column. Check: M417 (warn). Source: Microsoft's best practice rule 'Unpivot pivoted (month) data', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; Microsoft's skill, modeling-guidelines.md (address in rule 2)

**7. Role-playing dimensions.** One dimension can filter a fact in more than one role: Date filters Sales by order date and by ship date. Microsoft describes two designs.

- One dimension, several relationships. Only one can be active; the others are inactive, and a measure turns one on with USERELATIONSHIP. The shipped example: the relationship below and the measure `Total Sales by Ship Date` in `tests/fixtures/examples/Examples.SemanticModel/definition/tables/_Measures.tmdl`.
- One copy of the dimension per role (Date, Ship Date), each with one active relationship. Make the copy as a referencing query in Power Query (a duplicated query for DirectQuery) or as a calculated table whose formula is the original table's name; a calculated copy needs its reason line (M105, rule 8 of the file `model-standard.md` beside this one). A copy made in DAX takes over the columns only: set formats, descriptions and hierarchies again. Give its columns role names (Ship Year) and its table a description that says which fact column it filters. A copy named with Date also needs the marks of rule 30, or M404 reports it.
- Prefer copies when a visual must filter by two roles at once, when authors build visuals without measures, or when the model has security roles (rule 24). Inactive relationships suit a role that a few measures need.
- With two or more inactive relationships to one table, the check suggests copies. Checklist item 15: two or more business meanings of a date need one of the two designs; two or more active date roles on one fact need a review.

```
relationship 'Sales ship date to Date (inactive)'
	isActive: false
	fromColumn: Sales.'Ship Date Key'
	toColumn: Date.'Date Key'
```

Check: U006 (note). Source: https://learn.microsoft.com/en-us/power-bi/guidance/star-schema ; https://learn.microsoft.com/en-us/power-bi/guidance/relationships-active-inactive ; https://learn.microsoft.com/en-us/power-bi/guidance/model-date-tables (clone with DAX); checklist items 13 and 15

**8. Slowly changing dimensions.** Type 1 keeps only the latest value of a column: a change overwrites the old one, and a full refresh of the table gives this result. Type 2 keeps every version of a member: each version is a row with its own surrogate key, a start and an end date, and often a current-version flag; facts carry the key of the version that was valid on the fact's date. Power Query cannot build type 2: load it from a warehouse that keeps the versions. In the model, give one column to pick the member and another to pick a version, with a label that shows the validity dates. The files do not show it: no check. Source: https://learn.microsoft.com/en-us/power-bi/guidance/star-schema

**9. Keys.** A relationship joins one column on each side, and the one side must be unique.

- When a dimension has no single unique column, add a surrogate key (a Power Query index column, merged into the fact query too) or take one from the source.
- Keys are whole numbers (M110, rule 27).
- A key made of several values is built in the source, never by joining texts in a calculated column of the model.
- Do not add surrogate keys to fact tables.
- Checklist item 14: 0 concatenated relationship keys unless justified, 0 blanks in one-side keys, at most 0.1% blanks in many-side keys. The files do not show data: ask the developer.
- A key that must never be blank gets `isNullable: false` (Is Nullable off in Power BI Desktop). A refresh that meets a blank in that column then fails, and the model keeps the data of the last good refresh, so the problem is seen instead of showing as a blank item. Microsoft offers it as a choice, so the check is a note. Check: M416 (note; one note per table whose relationship key allows blanks). The shipped examples do not carry it yet; `Store[Store Key]` can show it later. Source: https://learn.microsoft.com/en-us/power-bi/guidance/relationships-many-to-many ; https://learn.microsoft.com/en-us/dax/best-practices/dax-error-functions
- Check: M110 (warn). Source: https://learn.microsoft.com/en-us/power-bi/guidance/star-schema ; https://learn.microsoft.com/en-us/power-bi/guidance/directquery-model-guidance (no relationship on a concatenated calculated column); Microsoft's skill, modeling-guidelines.md (address in rule 2: no composite keys, no surrogate keys on facts); checklist item 14

## B. Relationships

In `relationships.tmdl`, `fromColumn` is the many side and `toColumn` the one side. A relationship with no cardinality lines is many-to-one; with no `crossFilteringBehavior` it filters in one direction. Write a new relationship like one in this model or in `tests/fixtures/examples/Examples.SemanticModel/definition/relationships.tmdl`. Source: Microsoft's skill, https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/tmdl-guidelines.md

The next seven rules catch files that Power BI refuses to load, or that break a field. Source for all seven: https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-how-to (TMDL that breaks the model's metadata rules is refused), plus the source in each rule.

**10. Relationship columns exist.** Both columns a relationship names are in their tables. Check: M901 (fail). Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand

**11. Hierarchy levels exist.** Each level of a hierarchy names a column of the same table. Check: M902 (fail). Source: https://learn.microsoft.com/en-us/analysis-services/tabular-models/hierarchies-ssas-tabular ; Microsoft's skill, modeling-guidelines.md (address in rule 2)

**12. Sort columns exist.** The column named in `sortByColumn` is in the same table. Check: M903 (fail). Source: Microsoft's skill, modeling-guidelines.md (address in rule 2)

**13. Data columns name their source.** Every column that is not calculated has `sourceColumn`, with the column name the table's query returns. Columns of calculated tables and calculation groups are left out. Check: M904 (fail). Source: Microsoft's skill, modeling-guidelines.md (address in rule 2)

**14. No empty formula.** A measure, calculated column or calculation item has a formula. Check: M905 (fail). Source: https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-how-to

**15. No control characters.** Names hold no tab, line break or other control character. The check also reads descriptions. Check: M906 (fail). Source: Microsoft's best practice rules 'Avoid invalid characters in names' and 'Object names must not contain special characters', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json

**16. Columns with a job stay available.** A column that sorts another, is sorted by another, or is a hierarchy level never has `isAvailableInMdx: false`. Check: M907 (fail). Source: Microsoft's best practice rule 'Set IsAvailableInMdx to true on necessary columns', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json

**17. The normal form.** A relationship is one-to-many, from a dimension key to a fact column, filtering one way: from the one side to the many side. Every other form needs a reason.

- Between two tables only one path of relationships can be active. A second path must be inactive, or Power BI reports an ambiguous path.
- A fact key with no match in the dimension shows up as a blank item in visuals. Fix the data at the source.
- Checklist item 11: 100% unique one-side keys, 0 avoidable many-to-many relationships.
- No check of its own; rules 18 to 22 report the other forms. Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand ; Microsoft's skill, modeling-guidelines.md (address in rule 2); checklist item 11

**18. Both directions.** Avoid them: they can slow queries and make filter paths ambiguous. The checklist targets 0; one needs a review, two or more a strong reason. When one measure must filter across a fact (for example to count dimension rows with sales), use CROSSFILTER inside that measure. For a slicer that should show only items with data, use a visual filter on the slicer instead. First ask whether a slicer list that changes with the data helps readers at all: it can also confuse them (no check). A bridge table of a many-to-many design needs one both-direction relationship: list it in section 9 with M405 and that reason. Check: M405 (warn; one-to-one and many-to-many relationships are left to rules 19 and 22). Source: https://learn.microsoft.com/en-us/power-bi/guidance/relationships-bidirectional-filtering ; checklist item 12

**19. Many-to-many.** Between two dimensions, use a bridge table with one-to-many relationships to both. A fact at a higher grain (targets per category) may relate many-to-many to its dimension. A fact at a higher date grain stores the first date of its period and relates one-to-many to the date table. Hide the bridge table. The shipped example: `Sales Target[Category] to Product[Category]`. Check: M406 (warn). Source: https://learn.microsoft.com/en-us/power-bi/guidance/relationships-many-to-many ; checklist item 11

- A fact at a higher grain gives a wrong figure below its grain: every product of a category shows the whole category target. Hide its number columns, so that only measures add them up, and let the measure return blank below the grain. Test the levels below with ISFILTERED, or with ISINSCOPE when a hierarchy drives the visual. No check: the files do not show the grain. A measure written for the shipped table `'Sales Target'` (an illustration; it is not in the examples):

```dax
IF (
    NOT ISFILTERED ( Product[Subcategory] )
        && NOT ISFILTERED ( Product[Product Name] ),
    [Total Target]
)
```

- Source of this point: https://learn.microsoft.com/en-us/power-bi/guidance/relationships-many-to-many

**20. Many-to-many filters one way.** A many-to-many relationship filters from the dimension to the fact only. Check: M407 (warn). Source: Microsoft's best practice rule 'Many-to-many relationships should be single-direction', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; https://learn.microsoft.com/en-us/power-bi/guidance/relationships-many-to-many

**21. Not too many special relationships.** When more than 30% of all relationships filter both ways or are many-to-many, review the design. Check: M408 (warn, object `model`). Source: Microsoft's best practice rule 'Avoid excessive bi-directional or many-to-many relationships', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json

**22. One-to-one.** When two tables describe the same thing, merge them in Power Query into one table and use display folders. A one-to-one relationship always filters both ways, and rows without a match give blanks. The shipped example: `Store Detail[Store Key] to Store[Store Key]`. Check: M409 (warn). Source: https://learn.microsoft.com/en-us/power-bi/guidance/relationships-one-to-one ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand

**23. Inactive relationships are used.** An inactive relationship that no formula turns on with USERELATIONSHIP does nothing. Use it in a measure, or ask the developer whether to remove it (deleting needs a clear yes, project instructions in `.github/copilot-instructions.md`). Check: M410 (warn). Source: https://learn.microsoft.com/en-us/power-bi/guidance/relationships-active-inactive ; Microsoft's best practice rule 'Inactive relationships that are never activated', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json

**24. Inactive relationships and security.** A row-level security filter never travels over an inactive relationship, not even inside a measure with USERELATIONSHIP. In a model with roles, prefer active relationships (role copies, rule 7) and test each role. Check: M414 (warn, object `model`). Rules for roles: the file `storage-and-security.md` beside this one. Source: https://learn.microsoft.com/en-us/power-bi/guidance/relationships-active-inactive

**25. No USERELATIONSHIP towards a secured table.** A formula never uses USERELATIONSHIP towards a table that a role filters: the visual that uses it returns an error. Prefer an active relationship to a role copy (rule 7). Check: M415 (fail). Source: Microsoft's best practice rule 'Avoid the USERELATIONSHIP function and RLS against the same table', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; Microsoft's skill, modeling-guidelines.md (address in rule 2)

**26. Mark the one-side key.** The key column on the one side carries `isKey`, as `Store[Store Key]` does in the shipped example. A marked date table is left out (rule 30). Check: M413 (warn). Source: Microsoft's best practice rule 'Mark primary keys', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json

**27. Key types.** Both columns of a relationship have the same data type (M109, fail), preferably whole number (M110, warn); a datetime key also compares the time part. Rule 10 of the file `model-standard.md` beside this one. Source: https://learn.microsoft.com/en-us/power-bi/guidance/relationships-troubleshoot ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand ; Microsoft's best practice rules 'Relationship columns should be of the same data type' and 'Relationship columns should be of integer data type', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json

**28. Hide the many-side key.** The fact table's key column is hidden (M102, warn), rule 7 of the file `model-standard.md` beside this one. Source: Microsoft's best practice rule 'Hide foreign keys', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; https://learn.microsoft.com/en-us/power-bi/guidance/relationships-many-to-many

## C. Dates

**29. Auto date/time is off.** With it on, Power BI makes a hidden date table for each date column; those tables grow the model and one date filter cannot reach several fact tables.

- The check reads two signs: hidden tables named `LocalDateTable_...` or `DateTableTemplate_...`, and the annotation `__PBI_TimeIntelligenceEnabled = 1` in `model.tmdl`. The annotation was seen in projects Power BI Desktop saved; Microsoft does not document it.
- Turning it off is a Power BI Desktop option (File > Options and settings > Options, Current File, Time intelligence). Copilot does not set it in files: ask the developer, and record it in section 6 of the brief.
- Turning it off removes the hidden tables, so visuals and filters that used them must be fixed.
- Check: M401 (warn, object `model`). Source: https://learn.microsoft.com/en-us/power-bi/guidance/auto-date-time ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-auto-date-time ; Microsoft's best practice rule 'Remove auto-date table', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; checklist item 18

**30. One marked date table.** A model with time intelligence has one dedicated date table, and it is marked. In the files, marked means `dataCategory: Time` on the table and `isKey` on its date column, which has the type `dateTime`. Marking is also required when relationships to the date table use a whole-number key, as in the shipped example.

```
table Date
	dataCategory: Time

	/// The calendar day.
	column Date
		dataType: dateTime
		isKey
		formatString: Short Date
		summarizeBy: none
		sourceColumn: Date
```

- A time intelligence function with no marked table and no calendar: M402 (fail). Checklist item 31 expects one dedicated date table.
- Date columns but no marked table: M403 (warn).
- A table whose name holds Date or Calendar without both marks: M404 (warn).
- Source: https://learn.microsoft.com/en-us/power-bi/guidance/model-date-tables ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables ; Microsoft's best practice rules 'Model should have a date table' and 'Date/calendar tables should be marked as a date table', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; Microsoft's skill, modeling-guidelines.md (address in rule 2); checklist item 31

**31. What a date table holds.** A column of type date with one row per day: every value unique, no blanks, no missing day between the first and the last, and whole years (a fiscal year counts). With the date and time type, every value has the same time. Checklist item 31: 0 blanks, 0 duplicates, 0 missing dates. The files do not show the data: ask the developer. Source: https://learn.microsoft.com/en-us/power-bi/guidance/model-date-tables ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables ; checklist item 31

**32. How Copilot builds one.**

- First choice: the date table of the source, if it has one.
- Otherwise copy the shape of `tests/fixtures/examples/Examples.SemanticModel/definition/tables/Date.tmdl`: the marks, a hidden whole-number `Date Key`, Year, Quarter, month and weekday names sorted by hidden numbers, and the `Calendar` hierarchy.
- Its rows are a made-up sample of four days with gaps. A real table covers every day of whole years.
- Build the rows in Power Query, or as a calculated table with CALENDAR or CALENDARAUTO. A calculated table needs its reason line (M105).
- Relate it to each fact table that has a date. Source: https://learn.microsoft.com/en-us/power-bi/guidance/model-date-tables ; Microsoft's skill, modeling-guidelines.md (address in rule 2)

**33. Date and time in one column.** A column that holds both is reported for review; split it in Power Query. Check: M111 (warn), rule 11 of the file `model-standard.md` beside this one. Source: Microsoft's best practice rule 'Split date and time', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json

**34. Calendars are a preview.** Calendar-based time intelligence is a preview feature. A table with a calendar counts as a date table for M402. It cannot be combined with Auto date/time tables, nor used in composite or live-connected models. Use it only with the developer's yes (the rule for preview features in `.github/skills/pbi-report/references/report-standard.md`). Example: `tests/fixtures/examples/preview/Calendar.SemanticModel`. Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-time-intelligence

## D. Columns

**35. Sort columns.** A label with its own order (month, weekday, band, stage, fiscal period) has `sortByColumn` set to a number column. Each value of the label maps to exactly one sort value, otherwise Power BI refuses the sort; sorting a month name by a date fails for that reason. The sort column is hidden (M102). The shipped example: `Date[Month Name]` sorted by `Month Number`. Checklist item 24 wants 100% of shown ordered labels sorted; the check only reads text columns whose name holds "month", the rest is judged in the review. Check: M113 (warn). Source: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-sort-by-column ; Microsoft's best practice rule 'Month (as a string) must be sorted', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; checklist item 24

**36. Data categories.** A field that a map, link or image reads gets a data category: city, country, address, latitude, longitude, web address, image address. Copy the spelling from the shipped `Store` table (`dataCategory: City`, `dataCategory: WebUrl`); do not categorise fields that do not need it. The check reads visible text columns whose name holds country, continent or city, and decimal columns named Latitude or Longitude; addresses, links and images are judged in the review. Checklist item 26: 100% of such author-facing fields. Check: M114 (warn). Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-data-categorization ; Microsoft's best practice rule 'Add data category for columns', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; checklist item 26

**37. Flag columns.** A visible yes-or-no column shows the words Yes and No, not 1 and 0. Check: M116 (warn; a visible whole-number column whose name starts with Is, or a visible column ending in " Flag" that is not text). Source: Microsoft's best practice rule 'Format flag columns as Yes/No value strings', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; Microsoft's skill, modeling-guidelines.md (address in rule 2)

**38. Column and hierarchy names differ.** A column never has the name of a hierarchy of its table. Check: M119 (warn). Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-column-measure-references

**39. Partition name.** A table with one partition gives it the table's name: `partition Store = m`. Check: M117 (warn). Source: Microsoft's best practice rule 'Partition name should match table name for single partition tables', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json

**40. Hierarchies.** A natural drill path gets a hierarchy in its table: year, quarter, month, day; category, subcategory, product. A hierarchy has two levels or more, all from its own table. The shipped examples: `Calendar` in `Date`, `Product Hierarchy` in `Product`. Checklist item 59: two or more natural levels call for a review of the drill path. Check: U007 (note; a table with visible Year and Month, Country and City, or Category and Subcategory columns and no hierarchy). Source: https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization ; https://learn.microsoft.com/en-us/analysis-services/tabular-models/hierarchies-ssas-tabular ; Microsoft's skill, modeling-guidelines.md (address in rule 2); checklist item 59

## E. Names of tables and columns - the default

When "Naming standard" in section 4 of the brief names no other standard, tables, columns and hierarchies follow this default (checklist item 7). Measure names are in rule 3 of the file `model-standard.md` beside this one.

**41. Business words.** Names are words a report author knows, with spaces between them: `Store Name`, `Order Date`. No placeholder names such as Column1, Table or Query1 on visible fields (checklist item 7 allows 0); this is judged in the review. Source: https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization ; Microsoft's skill, https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/naming-conventions.md ; checklist item 7

**42. The form of a name.** M118 (warn) reports each of these:

- A first letter in lower case. Source: Microsoft's best practice rule 'First letter of objects must be capitalized', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json
- Underscores instead of spaces, and words run together (`StoreName`). A name that starts with an underscore, such as `_Measures`, passes. Source: Microsoft's skill, naming-conventions.md (address in rule 41)
- A technical prefix: Dim, Fact or Stg. The check also reports tbl and vw. Source: Microsoft's skill, naming-conventions.md (address in rule 41)
- A space at either end. Source: Microsoft's best practice rule 'Trim object names', https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json ; Microsoft's skill, naming-conventions.md

**43. What M118 reads.** Only names report authors can see: visible tables, and the visible columns and hierarchies of visible tables. Hidden keys keep their source names (`StoreKey` passes when hidden). Reading visible names only is this template's choice. A word with its own spelling (kWh) passes when the brief lists it under "Acronyms and words with their own spelling". Check: M118 (warn).

**44. Renaming.** In an existing model, names stay as they are. Renaming a table or column can break visuals, filters and other reports on the model, so it needs the developer's clear yes first (project instructions in `.github/copilot-instructions.md`). Source: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-tmdl-view ; Microsoft's skill, naming-conventions.md (address in rule 41: keep the patterns of an existing model)

**45. More from Microsoft's skill.** No check. Name fact tables in the plural (Sales, Orders) and dimension tables in the singular (Product, Date). The skill also says the main label column of a dimension may take the table's name (`Product`), but advises table-qualified names (`Product Name`) when Copilot or data agents read the model; see below. Source: Microsoft's skill, naming-conventions.md (address in rule 41)

## Sources

Read on 11 November 2026. Every rule is restated in this template's own words.

- Microsoft Learn, guidance: https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-modeling-guidance-for-power-platform ; https://learn.microsoft.com/en-us/dax/best-practices/dax-error-functions ; https://learn.microsoft.com/en-us/power-bi/guidance/star-schema ; https://learn.microsoft.com/en-us/power-bi/guidance/model-date-tables ; https://learn.microsoft.com/en-us/power-bi/guidance/auto-date-time ; https://learn.microsoft.com/en-us/power-bi/guidance/relationships-one-to-one ; https://learn.microsoft.com/en-us/power-bi/guidance/relationships-many-to-many ; https://learn.microsoft.com/en-us/power-bi/guidance/relationships-active-inactive ; https://learn.microsoft.com/en-us/power-bi/guidance/relationships-bidirectional-filtering ; https://learn.microsoft.com/en-us/power-bi/guidance/relationships-troubleshoot ; https://learn.microsoft.com/en-us/power-bi/guidance/directquery-model-guidance ; https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization
- Microsoft Learn, product pages: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-auto-date-time ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-time-intelligence ; https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-sort-by-column ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-data-categorization ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-tmdl-view ; https://learn.microsoft.com/en-us/analysis-services/tabular-models/hierarchies-ssas-tabular ; https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-how-to ; https://learn.microsoft.com/en-us/dax/best-practices/dax-column-measure-references
- Microsoft's best practice rules (MIT), each named by its rule name: https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json
- Microsoft's skill `semantic-model-authoring` (MIT): https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/modeling-guidelines.md ; https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/naming-conventions.md ; https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/tmdl-guidelines.md (`fromColumn` is the many side)
- The owner's checklist, `checklist/checklist.md`, items 7, 10 to 15, 18, 24, 26, 31 and 59.

Where sources disagree, and what was decided:

- Which key to hide: Microsoft's DirectQuery guidance hides the one-side key and lets the many-side key stay visible; the many-to-many guidance and the best practice rule hide the many-side key, as M102 does. Both keys can be hidden. M102 is unchanged.
- Keys on dates: the best practice rule prefers whole-number relationship columns (M110 warns on a date key), while a date table is marked on its date column. The shipped example relates on the whole-number `Date Key` and marks the `Date` column; Microsoft Learn requires the mark in exactly that case.
- `isKey` on a dimension key: the best practice rule 'Mark primary keys' asks for it; Microsoft's skill lists it among the things not to do, which reads like a misplaced line. M413 follows the rule.
- Building a date table: Microsoft Learn says DAX is often easier; Microsoft's skill prefers Power Query and DAX only without a source table. Both agree the source's date table comes first. Rule 32 allows both; a calculated table carries its reason line.
- Snowflakes: checklist item 10 counts chains longer than one hop; M412 warns on every snowflaked table. A justified single hop goes in section 9 with M412.
- Both directions on a bridge table: the many-to-many guidance needs one; checklist item 12 targets none. M405 still warns; the bridge goes in section 9 with its reason.
- Flags: Microsoft's skill also accepts the Boolean type; the best practice rule and M116 report any non-text column ending in " Flag". A Boolean flag that must stay goes in section 9 with M116.
- Label column of a dimension: Microsoft's skill says both `Product` and `Product Name`. The shipped examples use `Store Name` and `Product Name`. Both pass; no check.
- Auto date/time: Microsoft Learn accepts it for simple, ad hoc models; checklist item 18 and the best practice rule want it off. M401 warns.
- Calendars: Microsoft Learn recommends calendar-based time intelligence, but it is a preview. The template uses a marked date table (rule 30); calendars only as rule 34 says.

Not confirmed from Microsoft:

- The annotation `__PBI_TimeIntelligenceEnabled`: seen in saved projects, not documented.
- That `dataCategory: Time` plus `isKey` on the date column is what Desktop's "Mark as date table" writes. Microsoft Learn describes the Desktop action; Microsoft's skill and the best practice rules read the two properties.
- That each case of rules 10 to 14 stops a model from loading. Microsoft documents that TMDL breaking the model's rules is refused, not each case.
- The prefixes tbl and vw in M118: no source names them.
- The TMDL spelling `isNullable`: it follows the Tabular Object Model property IsNullable; the Learn pages give only the Desktop label Is Nullable.
- M906 on descriptions: the best practice rules cover names only.

Checklist items: 7, 10-15, 18, 24, 26, 31, 59
