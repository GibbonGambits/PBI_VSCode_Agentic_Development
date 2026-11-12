# Data model design

Part 2 of 2 of this topic. Covers: Business-rule grain and testing; Duplicate names, Group By Columns; Circular dependency errors; Sankey chart funnels; User-context calculated columns.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### Business-rule grain and testing

**T06-A173-4.** Check new formulas against a small data set that can be understood at a glance, so the expected numbers are known beforehand; in a model with millions of rows errors are far harder to find.
- Must. 2019. https://www.sqlbi.com/articles/the-importance-of-star-schemas-in-power-bi/
- When: Testing a new formula.

**T06-A368-1.** Evaluate a business rule at the lowest level of detail where each of its inputs has one unambiguous value, and aggregate the results only afterwards.
- Should. 2026. https://www.sqlbi.com/articles/writing-dax-at-the-correct-granularity/
- When: A measure applies a rule, such as a rate or threshold, to data.

**T06-A368-2.** Never evaluate a business rule at a grain coarser than its business-rule grain, the level where no input needs an invented aggregation. A finer grain can still be correct.
- Must. 2026. https://www.sqlbi.com/articles/writing-dax-at-the-correct-granularity/
- When: Choosing the level at which a measure applies a rule.

**T06-A368-3.** A measure can iterate a SUMMARIZE of the columns that define the business-rule grain, not every source row: take the additive input per group from a measure through context transition, apply the rule per group, then sum. The coarsest unambiguous grain tends to be fastest.
- Option. 2026. https://www.sqlbi.com/articles/writing-dax-at-the-correct-granularity/
- When: A rule's inputs are unambiguous above the grain of the source rows.

**T06-A368-4.** Do not multiply an additive total by an AVERAGE, MIN or MAX of non-additive rates taken across rows with different rates: it looks right where one rate applies and is wrong on totals, since a simple average weights every rate equally.
- Must. 2026. https://www.sqlbi.com/articles/writing-dax-at-the-correct-granularity/
- When: A measure combines an amount with a rate that varies by row.

**T06-A368-6.** Make the measure enforce the business-rule grain inside itself; do not repair a wrong total by iterating whatever rows the visual shows. What a visual shows changes when users drill or add fields, while the rule's grain must hold in every layout.
- Should. 2026. https://www.sqlbi.com/articles/writing-dax-at-the-correct-granularity/
- When: A measure gives a wrong total.

**T06-A368-8.** Before writing a DAX formula, identify four grains: what one row of each source table is, where every rule input has one meaning, which rows the code iterates, and which grouping the report requests for the cell. They must fit together, not coincide.
- Should. 2026. https://www.sqlbi.com/articles/writing-dax-at-the-correct-granularity/
- When: Planning any measure that applies a business rule.

**T06-A368-9.** Before writing a measure, settle: what a row means in each source table; which keys make each rule input unambiguous; which inputs sum before the rule; which table to iterate; whether the grain depends on the visual's fields; what to return below the data's grain.
- Should. 2026. https://www.sqlbi.com/articles/writing-dax-at-the-correct-granularity/
- When: Planning a measure's grain; also look for a key lost upstream and verify a few rows by hand.

**T06-A368-10.** Do not validate a measure by first checking that the grand total matches the visible rows. Build a small table at the business-rule grain, check each of its rows, and only then check how they aggregate.
- Must. 2026. https://www.sqlbi.com/articles/writing-dax-at-the-correct-granularity/
- When: Testing a measure that applies a business rule.

**T06-A368-11.** When one non-additive value, such as a rate, is the only non-additive input of a rule, the iteration can group by that value alone, combining entities that share it: still correct and more efficient. Grouping also by the owning entity is simpler to adapt later.
- Option. 2026. https://www.sqlbi.com/articles/writing-dax-at-the-correct-granularity/
- When: A measure iterates groups to apply a rule with one non-additive input.

### Duplicate names, Group By Columns

**T06-A269-2.** When different entities can share one display value, such as two customers with one name, prefer a model that keeps them on separate rows whatever fields report authors pick, over counting on every report to add the key column.
- Should. 2023. https://www.sqlbi.com/articles/understanding-group-by-columns-in-power-bi/
- When: A descriptive column is not unique across the entities it describes.

### Circular dependency errors

**T06-A013-5.** In calculated tables and calculated columns, avoid functions that take the blank row into account, for example write DISTINCT where VALUES would go: the object may later join a relationship, and code that depends on the blank row then gives a circular dependency.
- Must. 2021. https://www.sqlbi.com/articles/understanding-circular-dependencies/
- When: Every calculated table and calculated column, since either could become part of a relationship.

**T06-A112-3.** In a calculated column that uses CALCULATE, add ALLEXCEPT keeping only the table's primary key (REMOVEFILTERS can serve the same end), so context transition filters just that key. The fix rests on DAX semantics, not on an engine optimisation, so it holds everywhere.
- Should. 2021. https://www.sqlbi.com/articles/understanding-circular-dependencies/ ; https://www.sqlbi.com/articles/avoiding-circular-dependency-errors-in-dax/
- When: A calculated column with CALCULATE in a table that has a primary key column.

**T06-A112-4.** Be cautious with CALCULATE inside a calculated column of a table that has no primary key: context transition there is likely to give unexpected results.
- Consider. 2021. https://www.sqlbi.com/articles/avoiding-circular-dependency-errors-in-dax/
- When: A calculated column in a table without a primary key.

**T06-A112-5.** When a calculated column references a measure, put the measure inside CALCULATE with ALLEXCEPT keeping only the primary key column of the table: a measure call always implies CALCULATE. On a one-side table it is not required, yet still advised.
- Should. 2021. https://www.sqlbi.com/articles/avoiding-circular-dependency-errors-in-dax/
- When: Every calculated column that references a measure, even when no error appears.

**T06-A290-4.** In a calculated table that will take part in relationships, write a filter on a source column as FILTER over ALLNOBLANKROW of that column, to avoid circular dependencies when the relationships are created.
- Must. 2023. https://www.sqlbi.com/articles/preparing-a-data-model-for-sankey-charts-in-power-bi/
- When: A calculated table filters a source table and is then related to other tables.

### User-context calculated columns

**T06-A360-5.** A User Context column also suits a simple row-level expression the storage engine computes at query time at minimal cost, such as arithmetic between columns of one table: nothing is stored, the logic stays in one place, and filters, slicers and visuals can use it.
- Should. 2026. https://www.sqlbi.com/articles/introducing-user-aware-calculated-columns-in-power-bi/
- When: Table functions or elaborate IF logic need the formula engine; cost may show on very large or high-cardinality tables.
- Version: User-context calculated columns are a preview feature (May 2026) that needs the developer's yes.

**T06-A360-7.** Keep a calculated column Standard when its expression is not simple or query speed comes first: an expression the storage engine cannot compute triggers a formula-engine callback for each row at query time, and that cost can grow significantly.
- Should. 2026. https://www.sqlbi.com/articles/introducing-user-aware-calculated-columns-in-power-bi/
- When: Choosing between a Standard and a User Context calculated column.
- Version: User-context calculated columns are a preview feature (May 2026) that needs the developer's yes.

**T06-A360-14.** Keep a calculated column that exists only to feed a relationship, such as a key built with COMBINEVALUES or a price-range column for static segmentation, as a Standard column, and accept its storage cost.
- Must. 2026. https://www.sqlbi.com/articles/introducing-user-aware-calculated-columns-in-power-bi/
- When: A relationship is built on a calculated column.
- Version: User-context calculated columns are a preview feature (May 2026) that needs the developer's yes.

## Special-case techniques and facts

### Business-rule grain and testing

**T06-A368-7.** The alternative to returning blank below the grain is an explicit allocation rule that produces the detail. The developer must make that choice and never leave it to AVERAGE or a matrix total: repeating the higher-level value on each row is duplication, not allocation.
- Must. 2026. https://www.sqlbi.com/articles/writing-dax-at-the-correct-granularity/
- When: A report asks for a value, such as a budget, at finer detail than its data holds.

### Duplicate names, Group By Columns

**T06-A191-1.** Power BI groups a visual by the name column shown, so different entities with the same name, such as two customers, appear as one row with combined, misleading totals.
- Fact. 2020. https://www.sqlbi.com/articles/handling-customers-with-the-same-name-in-power-bi/
- When: A visual shows the name column and no column that tells the entities apart, such as a customer code.

**T06-A191-2.** One way to keep entities with the same name apart is to join the unique code onto the name, so every name is distinct; it is reliable, but the visible code clutters the name column.
- Option. 2020. https://www.sqlbi.com/articles/handling-customers-with-the-same-name-in-power-bi/
- When: Different entities share one display name.

**T06-A191-3.** Duplicate names can be made unique without a visible change by a calculated column that ranks the entities sharing a name by their code and appends zero-width characters (Unicode 8204), one fewer than the rank: the engine then sees different values.
- Option. 2020. https://www.sqlbi.com/articles/handling-customers-with-the-same-name-in-power-bi/
- When: Different entities share a display name that must look unchanged; test the model's culture first.

**T06-A191-4.** Consider showing the unique-name column under the plain name label and hiding the original name column, so same-name entities are kept apart by default. Keep the original in the model: it is still needed to test for an empty name.
- Consider. 2020. https://www.sqlbi.com/articles/handling-customers-with-the-same-name-in-power-bi/
- When: A unique-name column padded with zero-width characters has been created.

**T06-A191-5.** Before relying on zero-width characters to make names unique, check that appending them leaves names displayed unchanged in the model's culture and language: the zero-width space has a meaning of its own in some languages.
- Consider. 2020. https://www.sqlbi.com/articles/handling-customers-with-the-same-name-in-power-bi/
- When: Zero-width characters are used to make duplicate names unique.

**T06-A269-1.** Adopt the Group By Columns property on a column only once its internal behaviour is understood and it is accepted that Excel clients cannot work with it: the property is not compatible with MDX queries.
- Must. 2023. https://www.sqlbi.com/articles/understanding-group-by-columns-in-power-bi/
- When: Considering Group By Columns for a column of a Power BI model.
- Version: In 2023: Power BI from compatibility level 1400; not Analysis Services.

**T06-A269-3.** To make Power BI always group a descriptive column by the table's primary key without showing the key, mark the key column as the table key and set Keep Unique Rows to true on the descriptive column.
- Option. Check. 2023. https://www.sqlbi.com/articles/understanding-group-by-columns-in-power-bi/
- When: The descriptive column is unique through the table's primary key; Excel and other MDX clients ignore the setting.
- Version: Keep Unique Rows could not be set in the Power BI Desktop interface; check current options.

**T06-A269-4.** MDX, and therefore Excel, ignores Keep Unique Rows: a PivotTable over the descriptive column still merges different entities that share a display value, giving inaccurate figures with no error.
- Fact. 2023. https://www.sqlbi.com/articles/understanding-group-by-columns-in-power-bi/
- When: A model that relies on Keep Unique Rows is browsed from Excel.

**T06-A269-5.** When a column's values are unique only together with other non-key columns, such as a city name with state and country, its Group By Columns property can be set to the columns that identify each value.
- Option. 2023. https://www.sqlbi.com/articles/understanding-group-by-columns-in-power-bi/
- When: Keep Unique Rows does not fit; Excel PivotTables raise an error unless every listed column is in the report.
- Version: In 2023 Power BI only, from compatibility level 1400.

**T06-A269-6.** When setting Group By Columns for a column, add the column holding the displayed value itself to the list; without it, a slicer selection filters only the other listed columns and returns every value sharing them, such as all cities of the selected states.
- Should. 2023. https://www.sqlbi.com/articles/understanding-group-by-columns-in-power-bi/
- When: Configuring Group By Columns on a column.
- Version: In 2023: Power BI only, from compatibility level 1400.

**T06-A269-7.** Grouping or filtering a column with Group By Columns in DAX or MDX needs all its group-by columns, else a composite-key error. ALL and ALLNOBLANKROW on the column run; SUMMARIZE, SUMMARIZECOLUMNS, DISTINCT, VALUES, HASONEVALUE, SELECTEDVALUE and context transition over ALL of it fail.
- Fact. 2023. https://www.sqlbi.com/articles/understanding-group-by-columns-in-power-bi/
- When: Hand-written DAX, and Excel PivotTables that leave those columns out; Power BI adds them to its own queries.

**T06-A269-8.** To filter a column that has Group By Columns in DAX, you must pass one filter table holding the column together with all its group-by columns, for example TREATAS over a list of value tuples mapped to those columns.
- Must. 2023. https://www.sqlbi.com/articles/understanding-group-by-columns-in-power-bi/
- When: A CALCULATE condition on the column alone, or separate conditions per column, fails with the composite-key error.

**T06-A269-9.** To read the single selected value of a column that has Group By Columns, replace SELECTEDVALUE by a table that summarises the column with its group-by columns, keep only the column, and return its value when the table has exactly one row.
- Option. 2023. https://www.sqlbi.com/articles/understanding-group-by-columns-in-power-bi/
- When: SELECTEDVALUE and HASONEVALUE fail on a column with Group By Columns.

**T06-A269-10.** In Power BI a filter, page filter or slicer on a column with Group By Columns produces a DAX filter on the group-by columns only, not on the column shown, and the saved selection holds those group-by values.
- Fact. 2023. https://www.sqlbi.com/articles/understanding-group-by-columns-in-power-bi/
- When: A column with Group By Columns is used in a filter or slicer.

**T06-A269-11.** When a measure uses ISFILTERED to detect a slicer selection on a column with Group By Columns, the column to test is the group-by column: Power BI filters that one, and the column shown is absent from the generated query.
- Fact. 2023. https://www.sqlbi.com/articles/understanding-group-by-columns-in-power-bi/
- When: A measure reacts to a selection on a column that has Group By Columns.

**T06-A269-12.** Measures in a model that uses Group By Columns must allow for two side effects: grouping by the column requires all its group-by columns, and report filters and slicers filter only the group-by columns, not the column shown.
- Must. 2023. https://www.sqlbi.com/articles/understanding-group-by-columns-in-power-bi/
- When: Writing measures in a model where a column has Group By Columns.

**T06-A269-13.** When an entity's code matters more than its description, the code column can be set as Group By Columns of the description column, so filter and slicer selections are saved as codes and survive renamed or translated descriptions.
- Option. 2023. https://www.sqlbi.com/articles/understanding-group-by-columns-in-power-bi/
- When: Saved selections must outlive changes to descriptions; Excel does not handle this fully consistently.
- Version: In 2023: supported in Power BI from compatibility level 1400, not in Analysis Services.

### Circular dependency errors

**T06-A013-3.** Be careful when relying on a relationship to avoid circular dependencies between calculated columns that use CALCULATE: on the one side, context transition filters only the table's unique column, but that is an optimisation that can be switched off, for example by USERELATIONSHIP.
- Consider. Check. 2021. https://www.sqlbi.com/articles/understanding-circular-dependencies/
- When: Calculated columns with CALCULATE in a table that is the one side of a relationship.
- Version: Local calculated columns over remote tables of a composite model do not get this optimisation; check current behaviour.

**T06-A013-6.** In a calculated table or column that will join a relationship, use ALLNOBLANKROW in place of ALL. That includes the ALL that DAX creates for each predicate filter argument of CALCULATE or CALCULATETABLE: rewrite such a predicate as an explicit filter over ALLNOBLANKROW.
- Must. 2021. https://www.sqlbi.com/articles/understanding-circular-dependencies/
- When: Creating the relationship raises a circular dependency because the calculated object depends on the blank row.

**T06-A013-7.** A circular dependency error is never a false alarm: the model cannot be processed until the cycle is removed. The cycle is often hidden, in context transition of a calculated column with CALCULATE, or in the blank row a relationship on a calculated object adds.
- Fact. 2021. https://www.sqlbi.com/articles/understanding-circular-dependencies/
- When: A calculated column or a relationship is refused with a circular dependency error.

**T06-A112-1.** Two calculated columns whose expressions each depend on the other form a circular dependency; the remedy is to rewrite the code so the mutual reference disappears.
- Fact. 2021. https://www.sqlbi.com/articles/avoiding-circular-dependency-errors-in-dax/
- When: Calculated columns of one model that refer to each other directly.

**T06-A112-2.** A calculated column with CALCULATE anywhere in it performs context transition, which filters every column of its table, so it depends on all of them. A second such column in the table raises a circular dependency when created, even with an identical formula.
- Fact. Check. 2021. https://www.sqlbi.com/articles/understanding-circular-dependencies/ ; https://www.sqlbi.com/articles/avoiding-circular-dependency-errors-in-dax/
- When: The table has no column the engine treats as unique, or that optimisation is off; no ALLEXCEPT narrows the dependencies.
- Version: Local calculated columns over remote tables of a composite model can hit it even with a primary key.

**T06-A112-6.** A relationship is itself a dependency: the one-side table may gain a blank row depending on the many-side keys. So a relationship whose many side is a calculated column, or a calculated table built from the one-side table, can fail with a circular dependency.
- Fact. Check. 2021. https://www.sqlbi.com/articles/understanding-circular-dependencies/ ; https://www.sqlbi.com/articles/avoiding-circular-dependency-errors-in-dax/
- When: A DAX formula takes part in a relationship as a calculated table or a calculated key column.
- Version: Check current behaviour.

**T06-A112-7.** To clear the circular dependency, remove every blank-row function from the expression: DISTINCT for VALUES, ALLNOBLANKROW for ALL, functions that use VALUES inside (such as SELECTEDVALUE) expanded so DISTINCT can replace it, and compact CALCULATE filters rewritten in full table form with ALLNOBLANKROW.
- Must. Check. 2021. https://www.sqlbi.com/articles/avoiding-circular-dependency-errors-in-dax/
- When: A one-to-many relationship fails with a circular dependency and its many side is a calculated column or table.
- Version: Check current behaviour.

### Sankey chart funnels

**T06-A290-7.** Store each entity's first event type in a calculated column instead of hardcoding which event types count as start events.
- Should. 2023. https://www.sqlbi.com/articles/preparing-a-data-model-for-sankey-charts-in-power-bi/
- When: A funnel where users can hide events and a start event is treated differently from later ones.

**T06-A290-9.** If only a static funnel chart is needed, consider building the event table in Power Query or SQL and keeping DAX for the measures. A Power Query transformation can itself fail on memory during refresh when its steps do not fold into one request.
- Consider. 2023. https://www.sqlbi.com/articles/preparing-a-data-model-for-sankey-charts-in-power-bi/
- When: A funnel model that would otherwise need complex DAX calculated tables.

**T06-A290-11.** Before writing the measure that weights the flows of a funnel in which users can hide events, settle what hiding each kind means, for example: hiding a start event drops the customers who began with it; hiding a middle event only skips that step.
- Must. 2023. https://www.sqlbi.com/articles/preparing-a-data-model-for-sankey-charts-in-power-bi/
- When: Users may hide start and middle events of a funnel.

### User-context calculated columns

**T06-A360-1.** A calculated column whose expression reaches a user function, directly or through a measure or column it references, must have its Expression Context set to User Context: a Standard column is computed at processing time, when there is no user.
- Fact. 2026. https://www.sqlbi.com/articles/introducing-user-aware-calculated-columns-in-power-bi/
- When: A calculated column calls USERCULTURE, USERPRINCIPALNAME, USEROBJECTID, USERNAME or CUSTOMDATA.
- Version: User-context calculated columns are a preview feature (May 2026) that needs the developer's yes.

**T06-A360-2.** Base a User Context calculated column on the source column whose number of distinct values matches the result, such as month number for a month name, not on a higher-cardinality column giving the same output, such as the date: it is computed at query time.
- Should. 2026. https://www.sqlbi.com/articles/introducing-user-aware-calculated-columns-in-power-bi/
- When: Writing the expression of a User Context calculated column.
- Version: User-context calculated columns are a preview feature (May 2026) that needs the developer's yes.

**T06-A360-3.** Set up a user-aware calculated column that translates data values so: call USERCULTURE in its expression, set Expression Context to User Context, set a Sort by Column where needed, and set Group By Columns to columns that identify a selection without the translated text.
- Should. 2026. https://www.sqlbi.com/articles/introducing-user-aware-calculated-columns-in-power-bi/
- When: Translating the data values of columns by user culture, not object names.
- Version: User-context calculated columns are a preview feature (May 2026) that needs the developer's yes.

**T06-A360-4.** Set Group By Columns of a translated user-aware column to its numeric counterpart, such as month number for month name or weekday number for weekday name: slicers then save numbers, so selections survive when the report is viewed in another language.
- Should. 2026. https://www.sqlbi.com/articles/introducing-user-aware-calculated-columns-in-power-bi/
- When: A selection made in one language must hold in another.
- Version: Preview feature (May 2026) that needs the developer's yes; property edited in the TMDL view.

**T06-A360-8.** To hide a sensitive column's values from some users without breaking visuals, the column can live in a separate hidden table whose row-level security filter is FALSE for the restricted role, read into the main table by a User Context calculated column with LOOKUPVALUE.
- Option. 2026. https://www.sqlbi.com/articles/introducing-user-aware-calculated-columns-in-power-bi/
- When: Restricted users may see that the column exists; its values show blank. The lookup runs per row per query.
- Version: User-context calculated columns are a preview feature (May 2026) that needs the developer's yes.

**T06-A360-9.** A hidden table that holds a sensitive column, hides all its rows from a role and is read through a User Context calculated column must have no relationship through which its filter could spread: restricted users would get an empty report, not a redacted one.
- Must. 2026. https://www.sqlbi.com/articles/introducing-user-aware-calculated-columns-in-power-bi/
- When: The hidden-table pattern for redacting a sensitive column.
- Version: User-context calculated columns are a preview feature (May 2026) that needs the developer's yes. A table with no relationship needs its row in the brief (M411).

**T06-A360-10.** Weigh the query-time cost before using LOOKUPVALUE in a User Context calculated column on a high-cardinality table: the lookup runs for every row where the column is evaluated, in every query. On a small table it is negligible.
- Consider. 2026. https://www.sqlbi.com/articles/introducing-user-aware-calculated-columns-in-power-bi/
- When: A User Context calculated column that looks up values in another table.
- Version: User-context calculated columns are a preview feature (May 2026) that needs the developer's yes.

**T06-A360-11.** Whether a calculated column is stored cannot be set directly: only a Standard column in an Import table is materialised; User Context columns and columns of DirectQuery or Direct Lake on OneLake tables are not. An older view held that every calculated column is stored.
- Fact. Check. 2026. https://www.sqlbi.com/articles/introducing-user-aware-calculated-columns-in-power-bi/ ; https://www.sqlbi.com/articles/calculated-columns-and-measures-in-dax/
- When: Judging the memory cost of a calculated column.
- Version: Preview feature (May 2026) that needs the developer's yes; not applicable to Direct Lake on SQL tables.

**T06-A360-12.** For a calculated column that must aggregate or inspect rows whatever the user's security roles, such as a best-products classification, consider a Standard column: a User Context column sees only the rows the current user's roles allow.
- Consider. 2026. https://www.sqlbi.com/articles/introducing-user-aware-calculated-columns-in-power-bi/
- When: The model has security roles and a classification must cover all rows.
- Version: User-context calculated columns are a preview feature (May 2026) that needs the developer's yes.

**T06-A360-13.** Standard calculated columns, calculated tables and row-level security expressions cannot reference a User Context column, whether directly or through other objects. Saving a model that breaks one of these three limits raises an error.
- Fact. Check. 2026. https://www.sqlbi.com/articles/introducing-user-aware-calculated-columns-in-power-bi/
- When: Using a User Context calculated column elsewhere in the model.
- Version: User-context calculated columns are a preview feature (May 2026) that needs the developer's yes.
