# DAX table functions and queries

Part 2 of 2 of this topic. Covers: Calculated and static tables; SUMMARIZECOLUMNS behaviour; Joins and lookups; Set functions.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail. A note may name a tool, a website or a custom visual that this template does not use, or describe publishing, deploying or changing a deployed model: that is information for the developer. You do not install, call or suggest such a tool, and nothing is published or deployed from this template.

## General practice

### Calculated and static tables

**T03-A070-2.** When defining a static calculated table directly in DAX, prefer DATATABLE to a UNION of ROW expressions. The ROW form repeats the column names in every row and only infers data types; DATATABLE declares a data type for each column.
- Should. Check. 2016. https://www.sqlbi.com/articles/create-static-tables-in-dax-using-the-datatable-function/
- When: Creating a calculated table of constant rows whose values should stay visible in the model.
- Version: From 2016; a 2018 update notes that table constructors now exist and some techniques are obsolete.

### SUMMARIZECOLUMNS behaviour

**T03-A094-3.** SUMMARIZECOLUMNS yields a more efficient query plan than SUMMARIZE or ADDCOLUMNS over SUMMARIZE: one storage engine query and fewer physical plan steps in the comparison made. Before replacing, weigh how its filter table argument works, the missing row context on grouped columns, and version support.
- Should. Check. 2017. https://www.sqlbi.com/articles/introducing-summarizecolumns/
- When: A query that groups data and computes values.
- Version: Introduced with Power BI, Analysis Services 2016 and Excel 2016, the last with a limitation.

**T03-A094-8.** Inside an expression of SUMMARIZECOLUMNS, read the current value of a grouping column through VALUES, never by referencing the column directly. SUMMARIZECOLUMNS gives its expressions a filter context only, with no row context on the grouped columns; SUMMARIZE provides both.
- Must. 2017. https://www.sqlbi.com/articles/introducing-summarizecolumns/
- When: A single value of the column is active, which holds when the expression is not evaluated in a rollup.
- Version: Where a single value is compared or returned, the DAX standard prefers SELECTEDVALUE (rules 4 and 5).

**T03-A094-10.** Before relying on SUMMARIZECOLUMNS, consider whether the product and version that will run the DAX code support it.
- Consider. Check. 2017. https://www.sqlbi.com/articles/introducing-summarizecolumns/
- When: Writing DAX that uses SUMMARIZECOLUMNS.
- Version: Unsupported before Analysis Services 2016 and Excel 2016; Excel 2016 not inside measures; Power BI lifted that limit January 2017.

**T03-A341-3.** For grouping with no measure, use VALUES when only the values of one column are needed, and SUMMARIZE for the existing combinations of several columns, not SUMMARIZECOLUMNS, which is more than this task needs.
- Should. 2025. https://www.sqlbi.com/articles/summarizecolumns-best-practices/
- When: Grouping without measures where only regular relationships are involved.

**T03-A341-4.** When the columns to group by are connected through limited relationships, group with SUMMARIZECOLUMNS, not SUMMARIZE: SUMMARIZE groups over the expanded table, and expansion does not cross limited relationships.
- Should. 2025. https://www.sqlbi.com/articles/summarizecolumns-best-practices/
- When: Grouping in a model where limited relationships are involved, even when no measure is computed.

**T03-A341-5.** When SUMMARIZECOLUMNS groups columns without any measure or aggregation expression, always pass a table, such as the fact table, as a filter table argument. It drives auto-exists, so only combinations existing in that table return; without it the result is the full cross-join.
- Must. 2017. https://www.sqlbi.com/articles/introducing-summarizecolumns/ ; https://www.sqlbi.com/articles/summarizecolumns-best-practices/
- When: SUMMARIZECOLUMNS with grouping columns only; the filter table goes after them and before any name and expression pair.

**T03-A341-6.** For grouping with measures from a single fact table, the preference for SUMMARIZECOLUMNS over ADDCOLUMNS with SUMMARIZE is slight: test both for speed and choose on the results. The two are not fully equivalent in the combinations returned and in how outer filters act.
- Should. 2025. https://www.sqlbi.com/articles/summarizecolumns-best-practices/
- When: Grouping plus measures over one fact table.

**T03-A341-8.** When the measures to group come from more than one fact table, use SUMMARIZECOLUMNS: SUMMARIZE needs one source table, and a single fact table can miss combinations that exist only in another.
- Should. 2025. https://www.sqlbi.com/articles/summarizecolumns-best-practices/
- When: Grouping with measures from several fact tables; keep to its grouping features, without filter arguments.

**T03-A341-11.** Before depending on SUMMARIZECOLUMNS, above all inside a measure, make sure the engine that runs the model fully supports it. Measures in Power BI queries almost always run inside an outer SUMMARIZECOLUMNS, so calling it inside an iteration or another SUMMARIZECOLUMNS must be supported.
- Must. Check. 2025. https://www.sqlbi.com/articles/summarizecolumns-best-practices/
- When: Using SUMMARIZECOLUMNS inside measures or relying on its full feature set.
- Version: Fine in recent Power BI; Analysis Services up to 2022 and Excel as of 2025 lack full support.

**T03-A342-1.** Set the model's value filter behavior to Independent, and do not switch it back to Coalesced afterwards.
- Should. Check. 2025. https://www.sqlbi.com/articles/summarizecolumns-best-practices/ ; https://www.sqlbi.com/articles/understanding-value-filter-behavior-in-summarizecolumns/
- When: Any semantic model, and above all code that uses SUMMARIZECOLUMNS.
- Version: Independent arrived in 2025; Coalesced was the default before. A preview feature here: needs the developer's yes.

**T03-A337-4.** A SUMMARIZECOLUMNS call written inside a measure should include an aggregation, not list group-by columns only. A call without one may return the correct number, yet falls outside the good practices for the function.
- Should. 2025. https://www.sqlbi.com/articles/using-values-in-summarize/
- When: SUMMARIZECOLUMNS used within a measure.

### Joins and lookups

**T03-A098-7.** Avoid NATURALINNERJOIN and NATURALLEFTOUTERJOIN for joining two physical tables of the model. They match only columns sharing name, data type and lineage, which native model columns cannot do unless their lineage is removed; they suit tables produced by table expressions.
- Should. 2017. https://www.sqlbi.com/articles/lookup-multiple-values-in-dax/
- When: Choosing a way to join two tables in DAX.

**T03-A055-1.** Join tables in DAX by relying on physical relationships in the model rather than on join functions or expressions. Relationships give simpler and faster DAX code.
- Should. 2018. https://www.sqlbi.com/articles/from-sql-to-dax-joining-tables/
- When: Combining data from two tables in DAX.

**T03-A055-2.** DAX join techniques that do not use relationships are an option for building calculated tables, or small tables inside complex expressions of measures and calculated columns. The price is slower and more complex code than relationships give.
- Option. 2018. https://www.sqlbi.com/articles/from-sql-to-dax-joining-tables/
- When: Calculated tables, or small tables within complex expressions in measures and calculated columns.

**T03-A055-4.** To add lookup-table columns to each row of a table without aggregating, one way is ADDCOLUMNS with RELATED over the relationship to the one side.
- Option. 2018. https://www.sqlbi.com/articles/from-sql-to-dax-joining-tables/
- When: A relationship exists from the table to the lookup table on the one side and nothing is aggregated.

**T03-A055-6.** A cross join of two tables can be written with CROSSJOIN. Relationships in the model cannot produce cross join behaviour.
- Option. 2018. https://www.sqlbi.com/articles/from-sql-to-dax-joining-tables/
- When: A result needs every combination of the rows of two tables.

**T03-A055-7.** When two tables are linked by a relationship, NATURALLEFTOUTERJOIN gives the equivalent of a SQL left outer join and NATURALINNERJOIN the equivalent of an inner join, each returning the columns of both tables.
- Option. 2018. https://www.sqlbi.com/articles/from-sql-to-dax-joining-tables/
- When: A relationship connects the two tables being joined.

**T03-A291-2.** When tables are already linked by relationships, prefer functions that use the relationships implicitly, such as RELATED inside SELECTCOLUMNS, SUMMARIZE, or GENERATE with RELATEDTABLE, over NATURALLEFTOUTERJOIN and NATURALINNERJOIN: they often give the same result more efficiently.
- Should. 2023. https://www.sqlbi.com/articles/using-join-functions-in-dax/
- When: Related tables; join functions still help when all columns of a one-to-many chain are needed.

**T03-A197-1.** In a LOOKUPVALUE call, store each value to search for in a variable and pass the variable, not the expression itself, in the argument list. This helps both readability and performance.
- Should. 2020. https://www.sqlbi.com/articles/introducing-lookupvalue/
- When: Writing a LOOKUPVALUE call whose search values are expressions.

**T03-A197-3.** Make the column and value pairs given to LOOKUPVALUE specific enough to identify one row only. When several values match, LOOKUPVALUE fails with an error: it received a table of several values where it expected a single one.
- Must. 2020. https://www.sqlbi.com/articles/introducing-lookupvalue/
- When: Any LOOKUPVALUE call whose search conditions could match more than one value.

**T03-A197-4.** When a lookup matches on one column only, create a relationship between the two tables instead of using LOOKUPVALUE: the relationship is faster and gives the model a clearer structure.
- Should. 2020. https://www.sqlbi.com/articles/introducing-lookupvalue/
- When: The LOOKUPVALUE search list holds a single column.

**T03-A198-5.** Keep LOOKUPVALUE rare. Where a relationship exists or could be created, fetch the value through it; when LOOKUPVALUE appears in many places, review the model and replace the lookups that stand in for relationships. Relationships push most work to the storage engine.
- Should. 2020. https://www.sqlbi.com/articles/introducing-lookupvalue/ ; https://www.sqlbi.com/articles/understanding-lookupvalue/
- When: Code that uses LOOKUPVALUE heavily; some cases still justify it, such as an exchange rate at query time.

### Set functions

**T03-A203-1.** UNION keeps duplicate rows: it returns every row of every argument table. When the combined result must hold no duplicates, one way is to apply DISTINCT to the output of UNION.
- Option. 2020. https://www.sqlbi.com/articles/set-functions-in-dax-union-intersect-and-except/
- When: Combining tables with UNION when the result should not contain duplicate rows.

**T03-A203-9.** UNION, INTERSECT and EXCEPT are not limited to DAX queries: they can be used inside measures to assemble complex filters. The data lineage of the resulting table is essential for it to filter; TREATAS can restore a lost lineage or assign a new one.
- Option. 2020. https://www.sqlbi.com/articles/set-functions-in-dax-union-intersect-and-except/
- When: Building filter tables for measures with set functions.
- Version: M510 warns on every INTERSECT: such a formula needs its exception row in the brief.

## Special-case techniques and facts

### Calculated and static tables

**T03-A070-1.** A static table of fixed values, such as settings, parameters or segment boundaries, can be a calculated table defined with DATATABLE, so its content is DAX that can be read and edited. Enter Data keeps typed values as an encoded, compressed JSON document instead.
- Option. Check. 2016. https://www.sqlbi.com/articles/create-static-tables-in-dax-using-the-datatable-function/
- When: Tables whose fixed rows cannot be refreshed and change only together with the model or its measures.
- Version: DATATABLE: Power BI Desktop and Analysis Services 2016 (compatibility level 1200); Power Pivot cannot create such a table in DAX. A calculated table needs its reason line (M105); the standard keeps DAX for what Power Query cannot do.

**T03-A070-5.** In Power BI Desktop, a static table can also be made with Enter Data, by typing values into a grid or pasting them. The model then keeps the values inside a Power Query expression as an encoded, compressed JSON document.
- Option. Check. 2016. https://www.sqlbi.com/articles/create-static-tables-in-dax-using-the-datatable-function/
- When: Creating a static table in Power BI Desktop; a calculated table suits data that should remain visible.
- Version: The same storage is used when an Excel workbook containing a static table is imported.

**T03-A109-1.** A GENERATESERIES call with a decimal step produces floating-point values, so a value such as 0.81 can come out slightly off, with a tiny trailing fraction.
- Fact. 2017. https://www.sqlbi.com/articles/generating-a-series-of-numbers-in-dax/
- When: A number series built with a non-integer increment; usually harmless when values are only shown as two-decimal percentages.

**T03-A109-2.** When a number series generated with a decimal step needs exact values, one way is to turn each generated value into a fixed decimal number with CURRENCY, for instance inside SELECTCOLUMNS.
- Option. 2017. https://www.sqlbi.com/articles/generating-a-series-of-numbers-in-dax/
- When: More accuracy is needed than a display format with two decimal places gives.

**T03-A109-3.** Where GENERATESERIES is not available, a table of numbers can be built from CALENDAR, deriving each number from the generated date in SELECTCOLUMNS, because CALENDAR has no step argument.
- Option. Check. 2017. https://www.sqlbi.com/articles/generating-a-series-of-numbers-in-dax/
- When: GENERATESERIES cannot be used; the result can feed a parameter table where calculated tables exist.
- Version: GENERATESERIES is missing in Analysis Services 2016 and Power Pivot for Excel; Power Pivot cannot create calculated tables.

**T03-A109-5.** GENERATESERIES returns a single-column table, with the column named Value, running from a start value to an end value. The optional step defaults to 1 and may be any positive number, decimals included.
- Option. 2017. https://www.sqlbi.com/articles/generating-a-series-of-numbers-in-dax/
- When: Building a table that lists a series of numbers, such as a calculated table feeding a parameter slicer.
- Version: Exists in Power BI, in Azure Analysis Services, and in Analysis Services from 2017.

### SUMMARIZECOLUMNS behaviour

**T03-A094-4.** SUMMARIZECOLUMNS with grouping columns but no aggregation expression and no filter table returns every possible combination of the grouped values, like a crossjoin. With an aggregation expression, the engine infers the base table from it and the result matches the equivalent SUMMARIZE.
- Fact. 2017. https://www.sqlbi.com/articles/introducing-summarizecolumns/
- When: SUMMARIZECOLUMNS called with grouping columns only.

**T03-A094-6.** SUMMARIZECOLUMNS can receive several filter table arguments, which can help in queries against complex models with more than one fact table.
- Option. 2017. https://www.sqlbi.com/articles/introducing-summarizecolumns/
- When: Queries over complex data models that contain multiple fact tables.

**T03-A094-7.** A SUMMARIZE that computes no expressions produces the same query plan as SUMMARIZECOLUMNS with a filter table. Rewriting such a SUMMARIZE as SUMMARIZECOLUMNS brings no gain and is not required.
- Fact. 2017. https://www.sqlbi.com/articles/introducing-summarizecolumns/
- When: Only SUMMARIZE calls that contain no computed expressions.

**T03-A341-7.** SUMMARIZECOLUMNS and ADDCOLUMNS over SUMMARIZE are not fully equivalent. The latter starts from the combinations present in the scanned fact table under every filter reaching it; SUMMARIZECOLUMNS cross-joins the group-by values, ignores cross-filters, and drops a combination only when the measures are blank.
- Fact. 2025. https://www.sqlbi.com/articles/summarizecolumns-best-practices/
- When: Replacing one grouping pattern with the other when measures are computed.

**T03-A341-9.** Without SUMMARIZECOLUMNS, measures from several fact tables can be grouped by grouping each fact table apart, collecting the distinct group-by combinations and joining the partial results to them, or by ADDCOLUMNS over a hand-built cross-join of the grouping columns. Both are slower or more error-prone.
- Option. 2025. https://www.sqlbi.com/articles/summarizecolumns-best-practices/
- When: Grouping measures from several fact tables with basic functions; evaluate performance case by case.

**T03-A342-2.** With Coalesced, the merged filter of existing combinations is applied both when SUMMARIZECOLUMNS finds the group-by rows and when measures are evaluated. A measure that removes the filter from one column still sees the other limited to those combinations, and can return an unexpected number.
- Fact. 2025. https://www.sqlbi.com/articles/understanding-value-filter-behavior-in-summarizecolumns/
- When: SUMMARIZECOLUMNS receives filters on two columns and a measure removes the filter from one of them.

**T03-A342-3.** The value filter behavior setting does not change auto-exists. Even with Independent, SUMMARIZECOLUMNS still clusters filters when it determines the group-by rows, so rows for combinations that do not exist stay missing; only measure evaluation changes.
- Fact. 2025. https://www.sqlbi.com/articles/understanding-value-filter-behavior-in-summarizecolumns/
- When: Queries or visuals using SUMMARIZECOLUMNS with filters on several columns, whichever setting is selected.

**T03-A337-3.** To group columns of a one-side table inside a measure and keep the blank row of an invalid relationship, SUMMARIZECOLUMNS can replace SUMMARIZE: it returns that blank row when it exists.
- Option. 2025. https://www.sqlbi.com/articles/using-values-in-summarize/
- When: A measure iterates grouped one-side columns and must include the blank row of an invalid relationship.

### Joins and lookups

**T03-A098-1.** When each row needs several columns from a lookup table that has no relationship to it, consider an approach other than one LOOKUPVALUE call per column: each call repeats code and runs a separate subquery. LOOKUPVALUE remains a good choice for a single column.
- Consider. 2017. https://www.sqlbi.com/articles/lookup-multiple-values-in-dax/
- When: The lookup table has no relationship, so RELATED cannot be used, and several columns are needed.

**T03-A098-2.** One way to bring several columns from an unrelated lookup table into each row: GENERATE over the base table, whose second argument is a CALCULATETABLE of a ROW built from VALUES of the lookup columns, filtered by TREATAS on key values of the current row.
- Option. 2017. https://www.sqlbi.com/articles/lookup-multiple-values-in-dax/
- When: Lookup tables without a relationship; the query fails when several lookup rows match, and unmatched rows keep blanks.

**T03-A098-3.** GENERATE leaves out a row of its first table whenever the table expression in its second argument returns no rows for that row.
- Fact. 2017. https://www.sqlbi.com/articles/lookup-multiple-values-in-dax/
- When: Using GENERATE to combine each row of a table with a table expression.

**T03-A098-4.** When the data guarantees at most one lookup row per key combination, a faster option is GENERATE whose second argument is a CALCULATETABLE of SELECTCOLUMNS over the lookup table, keeping only needed columns and filtered with TREATAS. It also joins two tables on several columns.
- Option. 2017. https://www.sqlbi.com/articles/lookup-multiple-values-in-dax/
- When: Only with data trusted on that point; base rows with no matching lookup row are missing from the result.

**T03-A098-5.** GENERATEALL can replace GENERATE when every row of the first table must stay in the result even if the second table expression returns nothing for it. It is not needed when the second argument is a ROW call, which always returns one row.
- Option. 2017. https://www.sqlbi.com/articles/lookup-multiple-values-in-dax/
- When: GENERATE would drop rows of the first table that have no rows in the second expression.

**T03-A292-1.** To join unrelated tables with NATURALLEFTOUTERJOIN or NATURALINNERJOIN on model columns, rebuild the join columns on both sides with an expression that removes their data lineage, such as appending an empty string or CONVERT, and give them the same name and data type.
- Must. 2017. https://www.sqlbi.com/articles/lookup-multiple-values-in-dax/ ; https://www.sqlbi.com/articles/from-sql-to-dax-joining-tables/ ; https://www.sqlbi.com/articles/replacing-relationships-with-join-functions-in-dax/
- When: Natural-joining unrelated model tables, or table variables that keep model lineage; TREATAS is an alternative that performs better.

**T03-A292-2.** A new column defined as a plain reference to a model column keeps that column's lineage. Join functions applied to unrelated tables through such columns, or through same-named columns of variables that kept their lineage, fail with an error instead of joining.
- Fact. 2024. https://www.sqlbi.com/articles/replacing-relationships-with-join-functions-in-dax/
- When: Joining unrelated model tables or lineage-preserving table variables with NATURALLEFTOUTERJOIN or NATURALINNERJOIN.

**T03-A055-3.** Grouping a fact table by columns of related lookup tables behaves like a left join from the fact table, so fact rows with no matching lookup row are still returned.
- Fact. 2018. https://www.sqlbi.com/articles/from-sql-to-dax-joining-tables/
- When: Queries that group a fact table by columns of lookup tables reached through relationships.

**T03-A055-5.** An inner-join-like result over relationships can be obtained by taking a table extended with related columns and filtering out the rows whose looked-up column is blank.
- Option. 2018. https://www.sqlbi.com/articles/from-sql-to-dax-joining-tables/
- When: Only valid when blank is not a real value that the looked-up column can hold.

**T03-A055-10.** When natural-joining two unrelated physical tables on a same-named column, prefer TREATAS, which gives one table's columns the lineage of the other table's join column, over rewriting the columns to break lineage. The TREATAS approach performs better.
- Should. 2018. https://www.sqlbi.com/articles/from-sql-to-dax-joining-tables/
- When: Joining unrelated physical tables with NATURALLEFTOUTERJOIN or NATURALINNERJOIN.

**T03-A055-11.** Where the natural join functions are missing, an inner join can be written as FILTER over a CROSSJOIN of the two tables, comparing their key columns. Do not use it when the result has to be aggregated.
- Option. Check. 2018. https://www.sqlbi.com/articles/from-sql-to-dax-joining-tables/
- When: DAX versions without NATURALINNERJOIN.
- Version: Excel 2013 and Analysis Services 2012 and 2014, which lack the natural join functions.

**T03-A055-12.** For a left-join style lookup into the table at the one end of a many-to-one link, RELATED can be used when the relationship exists, and LOOKUPVALUE is a possible alternative when it does not. RELATED is the more efficient of the two.
- Option. 2018. https://www.sqlbi.com/articles/from-sql-to-dax-joining-tables/
- When: The left-side table is on the many side of a many-to-one link to the right-side table.
- Version: Presented as the way around the lack of a simple left join in DAX up to 2014.

**T03-A055-13.** When aggregating a left join done without relationships, consider cross-joining the distinct values of the grouping columns and evaluating a measure that filters the fact keys (FILTER, ALL, CONTAINS), dropping blank results, instead of grouping a LOOKUPVALUE-extended table. It can be faster.
- Consider. Check. 2018. https://www.sqlbi.com/articles/from-sql-to-dax-joining-tables/
- When: Few combinations of the grouped columns and a large number of rows in the aggregated table.
- Version: Written for the DAX of Excel 2013 and of Analysis Services 2012 and 2014.

**T03-A291-1.** NATURALLEFTOUTERJOIN and NATURALINNERJOIN follow regular relationships only. Limited relationships, such as many-to-many ones or those between different data islands, are never used as their join condition.
- Fact. 2023. https://www.sqlbi.com/articles/using-join-functions-in-dax/
- When: Joining model tables through existing relationships with the DAX join functions.

**T03-A291-3.** When chaining NATURALLEFTOUTERJOIN or NATURALINNERJOIN over more than two related tables, choose the argument order deliberately. Each call takes two tables; starting from the one-side table keeps all its rows, while starting from the many-side table drops one-side rows without matching data.
- Must. 2023. https://www.sqlbi.com/articles/using-join-functions-in-dax/
- When: Joins across a chain of one-to-many relationships with more than two tables.

**T03-A291-4.** NATURALLEFTOUTERJOIN can join two tables that are not directly related by following the whole relationship chain. The result differs from joining every table of the chain: the intermediate table's columns, and its rows without matches, are missing.
- Fact. 2023. https://www.sqlbi.com/articles/using-join-functions-in-dax/
- When: Joining two tables several relationships apart without including the intermediate tables.

**T03-A291-5.** To show the blank row a regular relationship adds on the one side for unmatched many-side rows, pass the one-side table wrapped in VALUES to NATURALLEFTOUTERJOIN. The blank row then collects all many-side rows without a match.
- Option. 2023. https://www.sqlbi.com/articles/using-join-functions-in-dax/
- When: Not for a table that only sits on the many side: it has no such blank row.

**T03-A291-6.** Without a relationship, NATURALLEFTOUTERJOIN and NATURALINNERJOIN join on column names only for columns with no data lineage to the model. Columns with lineage are matched by lineage whatever their names; two physical tables sharing an unrelated same-named column fail with 'No common join columns detected'.
- Fact. 2018. https://www.sqlbi.com/articles/from-sql-to-dax-joining-tables/ ; https://www.sqlbi.com/articles/using-join-functions-in-dax/
- When: Natural join functions on tables with no relationship between them, such as tables held in variables.

**T03-A291-7.** Tables whose columns lack data lineage can be joined on a composite key with NATURALLEFTOUTERJOIN or NATURALINNERJOIN: these functions match on every column that has the same name in both tables.
- Option. 2023. https://www.sqlbi.com/articles/using-join-functions-in-dax/
- When: Tables without data lineage, such as tables built in variables.

**T03-A197-2.** A LOOKUPVALUE search column can come from any table in the expanded table of the searched table, so one LOOKUPVALUE can search on a related table's column instead of first resolving a key with a nested LOOKUPVALUE.
- Option. 2020. https://www.sqlbi.com/articles/introducing-lookupvalue/
- When: The search value sits in a table related to the searched table, such as a code in Currency.

**T03-A197-5.** LOOKUPVALUE is the better choice than a model relationship when the lookup matches on several columns, or on a more complex condition built from several columns: there it is more flexible.
- Should. 2020. https://www.sqlbi.com/articles/introducing-lookupvalue/
- When: The lookup is defined by several columns or a complex multi-column condition, not one key column.

**T03-A197-6.** A calculated column that must fetch a value from another row of its own table can use LOOKUPVALUE to search that same table, because a table cannot have a relationship with itself.
- Option. Check. 2020. https://www.sqlbi.com/articles/introducing-lookupvalue/
- When: A calculated column looks up its own table, such as the previous order's price for a product.

**T03-A198-1.** LOOKUPVALUE disregards any filter that is currently active on the table it searches.
- Fact. Check. 2020. https://www.sqlbi.com/articles/understanding-lookupvalue/
- When: A LOOKUPVALUE call evaluated while the searched table is filtered.

**T03-A198-3.** Without its optional default value, LOOKUPVALUE raises an error when several values match the search. With the default value supplied, that value is returned both when nothing matches and when several values match.
- Fact. 2020. https://www.sqlbi.com/articles/understanding-lookupvalue/
- When: A LOOKUPVALUE search that may match no value or several values.

**T03-A198-4.** Consider leaving out the default-value argument of LOOKUPVALUE and supplying the fallback with COALESCE around the call: the default makes the engine verify a single value, giving complex plans with many storage engine queries. Measure both versions on the model before choosing.
- Consider. Check. 2020. https://www.sqlbi.com/articles/understanding-lookupvalue/
- When: Only when the data guarantees at most one matching value; otherwise the COALESCE form raises an error.

**T03-A198-6.** In currency conversion, LOOKUPVALUE is one possible way to fetch, at query time, the exchange rate valid on the order date.
- Option. 2020. https://www.sqlbi.com/articles/understanding-lookupvalue/
- When: Currency conversion needing the rate of the order date; still try relationships in place of LOOKUPVALUE where possible.

**T03-A198-7.** To steer the query plan, LOOKUPVALUE can be rewritten as CALCULATE with explicit filters. That allows forms LOOKUPVALUE lacks, such as one multi-column filter or TREATAS filters, including TREATAS over a two-column table; LOOKUPVALUE tests each search column separately.
- Option. 2020. https://www.sqlbi.com/articles/understanding-lookupvalue/
- When: A rarely needed optimisation for one model, data distribution or query; it requires extensive performance testing.

**T03-A198-8.** Test performance thoroughly before replacing LOOKUPVALUE with a hand-written CALCULATE version, or the reverse, and decide on the measured results: depending on data distribution and the columns searched, the rewrite can be slower as well as faster.
- Must. 2020. https://www.sqlbi.com/articles/understanding-lookupvalue/
- When: Choosing between LOOKUPVALUE and an equivalent CALCULATE formula for optimisation.

### Set functions

**T03-A203-2.** INTERSECT is not symmetrical: it returns the rows of its first table that also exist in the second and keeps duplicates only from the first table, so swapping the arguments can change the result.
- Fact. 2020. https://www.sqlbi.com/articles/set-functions-in-dax-union-intersect-and-except/
- When: Choosing the argument order of INTERSECT.

**T03-A203-3.** EXCEPT returns the rows of its first table that are absent from the second and keeps duplicates only from the first table, so the order of its two arguments is critical.
- Fact. 2020. https://www.sqlbi.com/articles/set-functions-in-dax-union-intersect-and-except/
- When: Choosing the argument order of EXCEPT.

**T03-A203-4.** UNION, INTERSECT and EXCEPT pair columns by position, not by name, and the result carries the column names of the first table.
- Fact. 2020. https://www.sqlbi.com/articles/set-functions-in-dax-union-intersect-and-except/
- When: Argument tables whose columns at the same position have different names.

**T03-A203-5.** When its argument tables have different data lineage, UNION returns a result with no lineage, while INTERSECT and EXCEPT keep the lineage of their first argument. A measure evaluated over a UNION result without lineage shows the same value on every row.
- Fact. 2020. https://www.sqlbi.com/articles/set-functions-in-dax-union-intersect-and-except/
- When: Set-function arguments of different lineage, such as a model column and a lineage-free table of the same values.

**T03-A203-6.** When a table used in a set function, or the function's result, has lost its data lineage, TREATAS can restore it or assign a new one, for example applied to a lineage-free table before it goes into UNION. Measures then return per-row values again.
- Option. 2020. https://www.sqlbi.com/articles/set-functions-in-dax-union-intersect-and-except/
- When: A set-function argument or result lacks the lineage of the model column it should filter.

**T03-A203-7.** UNION, INTERSECT and EXCEPT all raise an error when their argument tables have different numbers of columns.
- Fact. 2020. https://www.sqlbi.com/articles/set-functions-in-dax-union-intersect-and-except/
- When: Passing tables with different column counts to a set function.

**T03-A203-8.** With equal column counts but different data types at the same position, UNION converts numeric columns to text, while INTERSECT and EXCEPT convert nothing and raise an error. Conversions among numeric types work in all three.
- Fact. 2020. https://www.sqlbi.com/articles/set-functions-in-dax-union-intersect-and-except/
- When: Set-function arguments whose columns at the same position have different data types.

**T03-A226-4.** To find rows of one table with no match in another on several columns, build the unmatched key combinations as a table with EXCEPT and apply it as a filter. Row-by-row filtering with NOT CONTAINS or NOT IN is less efficient.
- Should. 2021. https://www.sqlbi.com/articles/using-contains-in-dax/
- When: Anti-join queries, such as listing stores in cities that have no customers.
