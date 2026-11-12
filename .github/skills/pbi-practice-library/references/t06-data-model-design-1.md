# Data model design

Part 1 of 2 of this topic. Covers: Dates, time and sort keys; Calculated columns versus measures; Source views, names, data types; Star schema and fact tables.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### Dates, time and sort keys

**T06-A005-1.** When a date-and-time column is split, the date part relates to the Date table and the time of day can carry its own set of attributes, such as hour and minute, for analysis at time levels.
- Option. 2011. https://www.sqlbi.com/articles/separate-date-and-time-in-powerpivot-and-bism-tabular/
- When: An imported column holds date and time, and the time of day matters to the business.

**T06-A009-4.** Consider a Date table column that shows the month name together with its year, for month-by-month charts and for a year, month, day hierarchy: the year a month belongs to is then plain to the reader.
- Consider. 2011. https://www.sqlbi.com/articles/sorting-dates-columns-in-powerpivot-v2-and-bism-tabular/
- When: Reports plot data month by month or use a year-month-day hierarchy.

**T06-A192-1.** The match between a label and its sort key must be one to one: a month name that includes the year needs a separate key value for each month of each year.
- Must. 2020. https://www.sqlbi.com/articles/sorting-duplicated-names-in-a-level-of-a-hierarchy-with-dax/
- When: Any column sorted by another column.

**T06-A224-3.** If the model already uses whole-number date keys and needs no calculations on those dates, the key's data type can simply follow what the data source uses: without date calculations the type makes no difference.
- Option. 2021. https://www.sqlbi.com/articles/choosing-between-date-or-integer-to-represent-dates-in-power-bi-and-tabular/
- When: Models with whole-number date keys and no date calculations.

### Calculated columns versus measures

**T06-A062-2.** Avoid leaving a complex calculated-column formula split over several intermediate calculated columns in a production model: each one is stored in memory. The split is a development aid only.
- Should. 2015. https://www.sqlbi.com/articles/calculated-columns-and-measures-in-dax/
- When: A complex calculated column was broken into intermediate columns while it was being developed.

**T06-A062-3.** A ratio shown at an aggregated level, such as a margin percentage, must be a measure that divides the aggregated numerator by the aggregated denominator. Aggregating a per-row ratio kept in a calculated column gives a sum of ratios, never the ratio of the sums.
- Must. 2015. https://www.sqlbi.com/articles/calculated-columns-and-measures-in-dax/
- When: Any percentage or ratio shown above row level.

**T06-A062-4.** A column, not a measure, is required when the result is used in a slicer, on rows, columns or a chart axis, or as a filter condition; when the expression has meaning only for one row; or when it groups values into bands.
- Must. 2015. https://www.sqlbi.com/articles/calculated-columns-and-measures-in-dax/
- When: Choosing between a calculated column and a measure for a new calculation.

**T06-A062-5.** A measure is worked out for each report cell in that cell's context, so it follows slicers, rows, columns, axes and filters; a calculated column is computed per row at refresh and ignores what the user selects.
- Must. 2015. https://www.sqlbi.com/articles/calculated-columns-and-measures-in-dax/
- When: A value must react to the user's selection and show in the values area of a visual.

**T06-A062-7.** Consider dropping calculated columns that are only intermediate steps for a measure: an iterator inside the measure, such as SUMX over the table, can evaluate the same row-level expression.
- Consider. 2015. https://www.sqlbi.com/articles/calculated-columns-and-measures-in-dax/
- When: A measure adds up a row-by-row result, such as quantity times price, kept in a calculated column.

**T06-A062-8.** A measure that needs several steps can hold each step in a variable, so the logic reads step by step and nothing is kept in intermediate calculated columns.
- Option. 2015. https://www.sqlbi.com/articles/calculated-columns-and-measures-in-dax/
- When: A measure whose logic takes several row-level aggregation steps.
- Version: VAR syntax: Power BI Desktop, or the 2016 versions of Excel and Analysis Services, or later.

**T06-A172-1.** The preference for a Power Query column over a DAX calculated column, for an expression on values of the same row, holds for Import models only: in DirectQuery a calculated column is evaluated at query time, much like a Power Query column.
- Should. 2019. https://www.sqlbi.com/articles/comparing-dax-calculated-columns-with-power-query-computed-columns/
- When: A new column whose expression reads only other columns of its own row.
- Version: This template still asks for a CalculatedReason and prefers the source (storage and security, rules 17 and 24; M105).

**T06-A172-2.** What remains for DAX calculated columns is logic that reads other rows or other tables: typically aggregations over other model tables, or lookups between tables from different data sources, where a Power Query merge would gain nothing from folding.
- Should. 2019. https://www.sqlbi.com/articles/comparing-dax-calculated-columns-with-power-query-computed-columns/
- When: Import models; deciding whether a derived column belongs in Power Query or in DAX.
- Version: Only with a CalculatedReason from the developer on why Power Query cannot supply it (storage and security, rule 17; M106).

**T06-A172-5.** When several derived columns are planned, prefer Power Query columns to DAX calculated columns, and accept that the overall effect varies: moving one column changes total model size almost unpredictably, because other columns may then compress worse.
- Should. 2019. https://www.sqlbi.com/articles/comparing-dax-calculated-columns-with-power-query-computed-columns/
- When: Import models; several derived columns are to be added.

### Source views, names, data types

**T06-A075-1.** When the source is a relational database, load views into the model and never the database tables themselves: a view per model table shields reports from later changes to the physical design, such as a renamed column or table.
- Must. 2016. https://www.sqlbi.com/articles/data-import-best-practices-in-power-bi/
- When: The source is a relational database, for example SQL Server or Oracle.

**T06-A075-2.** Organise source views so: one database schema per model, one view per model table, columns listed by name instead of selecting all, and after import the schema name removed from table names so only the view name stays.
- Should. Check. 2016. https://www.sqlbi.com/articles/data-import-best-practices-in-power-bi/
- When: A model loads its data through views from a relational database.
- Version: Power BI had no automatic way to drop the schema name on import; check current behaviour.

**T06-A075-5.** Give the source views and their columns the exact friendly names users will see, so naming serves the report user and not a developer typing names. Spaces and special characters are acceptable in view column names.
- Should. 2016. https://www.sqlbi.com/articles/data-import-best-practices-in-power-bi/
- When: Naming views and view columns that feed a model.

**T06-A075-6.** Give columns their final user-facing names inside the source views, and avoid renaming tables and columns in the model: a database administrator can then follow dependencies. The one rename left to the model is removing the schema name.
- Should. 2016. https://www.sqlbi.com/articles/data-import-best-practices-in-power-bi/
- When: A model loads its data through views from a relational database.

**T06-A075-7.** Give an imported column meant to be hidden a name that breaks the naming convention on purpose, such as a surrogate key written as one word ending in Key. An application key that users need may keep the normal spaced name and stay visible.
- Should. 2016. https://www.sqlbi.com/articles/data-import-best-practices-in-power-bi/
- When: Columns to hide, such as surrogate keys of a star schema.

**T06-A075-9.** Decide measure names up front. Import a number column that will be aggregated under a convention-based name that cannot be taken for a measure, so the explicit measure can carry the user-facing name without a clash.
- Should. 2016. https://www.sqlbi.com/articles/data-import-best-practices-in-power-bi/
- When: Number columns that will be aggregated, not shown as they are.

**T06-A075-11.** Avoid getting round a name clash between a measure and a column by giving the measure an awkward name, such as Sum of followed by the column name.
- Should. 2016. https://www.sqlbi.com/articles/data-import-best-practices-in-power-bi/
- When: A measure's intended name is already taken by a column.

**T06-A076-1.** Fixed Decimal Number suits financial values because, like whole numbers, it is stored exactly and its arithmetic is associative and fastest. A source column of two decimals may still import as floating point by default.
- Should. 2016. https://www.sqlbi.com/articles/choosing-numeric-data-types-in-dax/
- When: Columns that hold financial amounts.
- Version: Power BI calls the type Fixed Decimal Number; Power Pivot calls it Currency.

**T06-A076-2.** Weigh the data type of every column, and review the types after adding a table: the type picked automatically on import can be unwanted, as when a decimal source column that would fit Fixed Decimal Number arrives as floating point.
- Consider. Check. 2016. https://www.sqlbi.com/articles/choosing-numeric-data-types-in-dax/
- When: Building a model or adding a table to it.
- Version: Default type mapping described in 2016; check current behaviour.

**T06-A076-5.** Consider another data type for very large numbers stored as whole number or Fixed Decimal Number: their total keeps the same type and could exceed its range, and the engine does not detect that overflow.
- Consider. 2016. https://www.sqlbi.com/articles/choosing-numeric-data-types-in-dax/
- When: Columns of very large values whose sums could pass the range of their type.
- Version: A type change is the developer's decision, and a floating-point type needs its M108 row (model standard, rule 10).

**T06-A076-6.** Keep a column's data type apart from its format string and do not take one for the other: the name Currency has been used for both.
- Should. 2016. https://www.sqlbi.com/articles/choosing-numeric-data-types-in-dax/
- When: Setting data types and formats, above all in Power Pivot.
- Version: Power Pivot uses Currency for type and format; Power BI names the type Fixed Decimal Number.

### Star schema and fact tables

**T06-A173-1.** Treat the star schema as the rule every time: a report over one flattened table can return wrong numbers, while a star schema gives accurate results and better performance. Only expert modellers who fully understand the consequences may depart from it.
- Must. 2019. https://www.sqlbi.com/articles/the-importance-of-star-schemas-in-power-bi/
- When: Choosing between a star schema and a single flattened table.

**T06-A173-5.** When a report slices one fact table by several attributes, such as gender and job, move each attribute into its own dimension table: auto-exist merges filters on columns of one table and hides valid combinations. The step is required but may not suffice alone.
- Must. Check. 2019. https://www.sqlbi.com/articles/the-importance-of-star-schemas-in-power-bi/
- When: Several attributes used together in one visual are columns of the fact table.
- Version: Described in 2019; check current auto-exist behaviour.

**T06-A173-6.** Do not rely on fact rows to learn how one attribute maps to another, for example an item's group: keep the mapping in a dimension table and point REMOVEFILTERS and VALUES at its columns. With no fact rows left, the measure would return blank.
- Must. 2019. https://www.sqlbi.com/articles/the-importance-of-star-schemas-in-power-bi/
- When: A measure reads an attribute of the current item from a table the report can filter.

**T06-A218-8.** When a single fat table is proposed as the data model, measure its performance and weigh the extra cost it brings before accepting it.
- Consider. 2021. https://www.sqlbi.com/articles/power-bi-star-schema-or-single-table/
- When: Someone proposes replacing a star schema with one denormalised table.

**T06-A233-1.** When the source has header and detail tables, such as orders and order lines, move the header attributes into the detail table so one fact table relates to every dimension. In one simple test the header-detail form used about 15 times more CPU.
- Should. 2021. https://www.sqlbi.com/articles/header-detail-vs-star-schema-models-in-tabular-and-power-bi/
- When: Source data shaped as header and detail; a separate header is kept only to optimise particular calculations.

**T06-A233-2.** A table linked to dimensions is a fact table, so a header table and a detail table that both link to dimensions are two fact tables, and a relationship between them breaks the star schema.
- Must. 2021. https://www.sqlbi.com/articles/header-detail-vs-star-schema-models-in-tabular-and-power-bi/
- When: Header and detail designs, and any model where two tables linked to dimensions are related.

## Special-case techniques and facts

### Dates, time and sort keys

**T06-A005-3.** A column with a different value on nearly every row is the costliest kind: a date-time kept to the second over 15 million rows of one month gives a dictionary of about 2.5 million distinct values for that column alone.
- Fact. 2011. https://www.sqlbi.com/articles/separate-date-and-time-in-powerpivot-and-bism-tabular/
- When: Judging the memory cost of a date-time column kept at one-second detail in a large table.

**T06-A005-4.** When the time part is taken out in the source query it can be rounded to whole seconds, or to whole minutes when that is enough; hour and minute attributes are then derived in the model or in SQL.
- Option. Check. 2011. https://www.sqlbi.com/articles/separate-date-and-time-in-powerpivot-and-bism-tabular/
- When: A date-time column is split into date and time columns in SQL before import.
- Version: In older Power Pivot a time-only value still loaded as a date-time carrying the import day; check current behaviour.

**T06-A009-2.** A sort column that is coarser than the label, or lacks part of its key, raises no error but gives a wrong order: a year-month label sorted by a month number without the year is one case.
- Fact. 2011. https://www.sqlbi.com/articles/sorting-dates-columns-in-powerpivot-v2-and-bism-tabular/
- When: Setting Sort by Column on a combined label such as month and year.

**T06-A035-2.** Because a marked date table accepts no blank date, a classic Date dimension that keeps a dummy row for unknown dates (blank date, year and month number 0, an Unknown label) cannot be loaded as it is: its design has to change.
- Fact. 2013. https://www.sqlbi.com/articles/handling-wrong-or-missing-dates-in-tabular/
- When: A Date dimension with a dummy unknown-date row is imported and marked as a date table.
- Version: Stated for Tabular and Power Pivot; Analysis Services Multidimensional handles the dummy row well.

**T06-A192-2.** When a column should be ordered by a measure-like value such as population, prefer a sort-key column to sorting the visual by the measure: a measure sort also reorders outer levels of a matrix, needs the measure in the visual, and cannot reach a slicer.
- Should. 2020. https://www.sqlbi.com/articles/sorting-duplicated-names-in-a-level-of-a-hierarchy-with-dax/
- When: The order must hold for one hierarchy level only, or in visuals without the measure.

**T06-A192-4.** When one name appears under different parents in a hierarchy level, such as a county name in several states, and needs a key-based order, first make each name unique without changing its look, for example with zero-width characters, then sort that column by the key.
- Must. 2020. https://www.sqlbi.com/articles/sorting-duplicated-names-in-a-level-of-a-hierarchy-with-dax/
- When: Names at one level repeat across parents and their order differs by parent.

**T06-A192-5.** Categories, products, customers and similar entities can be given a custom order through ranking values computed in calculated columns, in place of the default alphabetical order, to bring the most relevant values to users first.
- Option. 2020. https://www.sqlbi.com/articles/sorting-duplicated-names-in-a-level-of-a-hierarchy-with-dax/
- When: A more specific order than alphabetical helps users; alphabetical order is not wrong.
- Version: Only when the ranking needs a measure or aggregate; otherwise rank in Power Query (storage and security, rule 17; M105).

**T06-A224-1.** As the key between a fact table and the Date dimension, a date-typed column and a whole-number column take the same storage and give the same query speed: VertiPaq hash-encodes every relationship column, storing dictionary indexes whatever the type.
- Fact. 2021. https://www.sqlbi.com/articles/choosing-between-date-or-integer-to-represent-dates-in-power-bi-and-tabular/
- When: Choosing the data type of the column that links a fact table to the Date table.

**T06-A224-4.** With whole-number date keys, when a row-context calculation needs the date behind a second, inactive date relationship, a hidden technical table of key and date pairs related to the fact table on that key lets the code use RELATED, much faster than LOOKUPVALUE.
- Option. 2021. https://www.sqlbi.com/articles/choosing-between-date-or-integer-to-represent-dates-in-power-bi-and-tabular/
- When: A second date column, such as a delivery date, has an inactive relationship and is used in a row context.

### Calculated columns versus measures

**T06-A062-10.** A DAX calculated column is a fitting choice when the value needs data from other tables of the model or rests on aggregated data, as in static segmentation or ABC classification.
- Option. 2015. https://www.sqlbi.com/articles/calculated-columns-and-measures-in-dax/
- When: A derived column depends on other tables or on aggregates, not only on its own row.
- Version: Only when the value needs data from other tables or aggregates, with its CalculatedReason (storage and security, rule 17; M106).

**T06-A172-3.** Denormalising by a merge in Power Query, instead of importing the tables apart and fetching values with RELATED in calculated columns, pays when the source is a relational database that joins the tables efficiently. It applies to Import models only.
- Should. 2019. https://www.sqlbi.com/articles/comparing-dax-calculated-columns-with-power-query-computed-columns/
- When: Bringing attributes of a related table into another table.

**T06-A172-4.** Take care with a Power Query column that aggregates rows of other tables: the aggregation runs on the data source and can take long. If it runs too long there, consider a DAX calculated column instead.
- Consider. 2019. https://www.sqlbi.com/articles/comparing-dax-calculated-columns-with-power-query-computed-columns/
- When: Import models; a derived column aggregates rows from other tables.
- Version: Only with the developer's CalculatedReason recorded on the column (model standard, rule 8; M105).

**T06-A172-6.** The engine ignores DAX calculated columns when it picks the table's sort order for compression, so one may compress poorly, above all with few distinct values. A Power Query column is compressed like any other; better compression of one column can still worsen others.
- Fact. 2019. https://www.sqlbi.com/articles/comparing-dax-calculated-columns-with-power-query-computed-columns/
- When: Import models.

**T06-A172-7.** In an incremental or partition refresh, DAX calculated columns are recomputed for every row of the table, even when few rows change; Power Query columns are computed only for the rows being processed.
- Fact. 2019. https://www.sqlbi.com/articles/comparing-dax-calculated-columns-with-power-query-computed-columns/
- When: Import models with incremental refresh or partitions.

**T06-A172-8.** Adding a new DAX calculated column needs no full refresh of its table; adding a new Power Query column does.
- Fact. 2019. https://www.sqlbi.com/articles/comparing-dax-calculated-columns-with-power-query-computed-columns/
- When: Import models; a column is added to a table that is already loaded.

**T06-A172-9.** In a refresh, DAX calculated columns are computed row by row only after all partitions are loaded and compressed, one at a time in dependency order. A Power Query column is processed like a source column; with folding, cost and parallelism depend on the source.
- Fact. 2019. https://www.sqlbi.com/articles/comparing-dax-calculated-columns-with-power-query-computed-columns/
- When: Import models.

### Source views, names, data types

**T06-A075-4.** A model that loads views may not detect some existing relationships, because referential integrity constraints are defined on tables, not on views. Creating those relationships by hand is a small cost.
- Fact. 2016. https://www.sqlbi.com/articles/data-import-best-practices-in-power-bi/
- When: Views, not tables, are imported from a relational database.

**T06-A075-8.** Consider a leading prefix such as an underscore on the names of columns meant to be hidden: they sort to the top of the column list, which makes it easy to verify that all are hidden.
- Consider. 2016. https://www.sqlbi.com/articles/data-import-best-practices-in-power-bi/
- When: Columns meant to be hidden; not where users need the column for transformations or joins with other sources.

**T06-A075-12.** If the raw number columns are to stay visible, besides turning summarisation off give them names that follow the convention, and add an explicit measure for the row-by-row result, for example one that iterates the table with SUMX.
- Option. 2016. https://www.sqlbi.com/articles/data-import-best-practices-in-power-bi/
- When: The detail number columns must remain visible in the model.
- Version: Visible raw number columns need their use listed in the brief (model standard, rule 7; M103).

**T06-A076-3.** Read from SQL Server, NUMERIC and DECIMAL columns become floating point by default whatever their declared digits; only MONEY and SMALLMONEY map to Fixed Decimal Number.
- Fact. Check. 2016. https://www.sqlbi.com/articles/choosing-numeric-data-types-in-dax/
- When: Tables imported from SQL Server.
- Version: Described in 2016; check current import defaults.

**T06-A076-4.** A sum over a floating-point column, even a plain SUM, can return slightly different totals on different runs of one query: segments are scanned in parallel in no fixed order, and floating-point addition is not associative.
- Fact. 2016. https://www.sqlbi.com/articles/choosing-numeric-data-types-in-dax/
- When: Two or more cores aggregate the column; more likely as columns and data grow.

### Star schema and fact tables

**T06-A130-2.** Merging several fact tables, such as sales and purchases, into one table aggregated at a shared grain removes analysis by every attribute that was not kept, for example customer or delivery date.
- Fact. 2018. https://www.sqlbi.com/articles/power-bi-is-a-model-based-tool/
- When: Deciding whether to combine fact tables into one.

**T06-A173-7.** The merging of filters on several columns of one table is auto-exist: it drops combinations with no rows in that table, so a flattened table can show visibly wrong figures. Grouping by columns of separate tables does not trigger it.
- Fact. Check. 2019. https://www.sqlbi.com/articles/the-importance-of-star-schemas-in-power-bi/
- When: Visuals group or filter by several columns of one table, such as attributes left in a flattened fact table.
- Version: Described in 2019; check current behaviour.

**T06-A173-8.** To see whether auto-exist hides combinations, one check is to capture the visual's query, tidy it, and run it with every measure wrapped in IGNORE so blank rows stay: once grouped by the dimension columns, once by the fact-table columns, then compare.
- Option. 2019. https://www.sqlbi.com/articles/the-importance-of-star-schemas-in-power-bi/
- When: A report sliced by several attributes shows missing or wrong figures.
- Version: The query is captured with Performance Analyzer in Power BI.

**T06-A218-2.** In one test, moving all dimension columns into the fact table gave a model roughly 2.65 to 3 times larger in memory than the star schema, because of the many large columns added, so it costs more to host.
- Fact. 2021. https://www.sqlbi.com/articles/power-bi-star-schema-or-single-table/
- When: Comparing a single denormalised table with a star schema of the same data.
- Version: Measured on Analysis Services 2019, on premises.

**T06-A218-3.** A single-table model beats a star schema only on very simple queries, and only modestly. Once queries grow complex or are not pure storage-engine queries the star schema is much faster: the cost of crossing a relationship matters less as calculations grow.
- Fact. 2021. https://www.sqlbi.com/articles/power-bi-star-schema-or-single-table/
- When: Comparing query speed of one denormalised table with a star schema.
- Version: Measured on Analysis Services 2019, on premises.

**T06-A218-4.** In a single-table model every slicer or filter list is filled by scanning the whole fact table, and slicers on its columns cross-filter one another, which is heavy on CPU; in a star schema those values come from small dimension tables.
- Fact. 2021. https://www.sqlbi.com/articles/power-bi-star-schema-or-single-table/
- When: Reports with slicers and filters on a model whose attributes all live in the fact table.
- Version: Measured on Analysis Services 2019, on premises.

**T06-A218-5.** DAX is built and optimised around star schemas. When grouping and filtering columns all come from one table, auto-exist makes the engine work with arbitrarily shaped sets: larger filters and slower queries, over twice as slow in one year-to-date test.
- Fact. Check. 2021. https://www.sqlbi.com/articles/power-bi-star-schema-or-single-table/
- When: Queries on a flat single-table model that group and filter by several of its columns.
- Version: Measured on Analysis Services 2019; check current behaviour.

**T06-A218-6.** Without a separate Date dimension, as in a single-table model, a year-to-date calculation cannot use the time intelligence functions and must be written by hand in longer, more error-prone code.
- Fact. 2021. https://www.sqlbi.com/articles/power-bi-star-schema-or-single-table/
- When: A model with no Date dimension table.

**T06-A218-7.** VertiPaq run-length encoding compresses columns whose values change often far less well, so they are larger and slower. Flattening a fine-grained dimension such as time of day into the fact table creates many such columns.
- Fact. 2021. https://www.sqlbi.com/articles/power-bi-star-schema-or-single-table/
- When: Denormalising attributes of a dimension whose key changes often into the fact table.

**T06-A233-4.** A separate header table can be kept to speed up specific calculations, such as a distinct count of customers sliced by dimensions linked to the header (about five times faster in one test). Slicing by detail-side dimensions needs a both-direction relationship, which removes the gain.
- Option. 2021. https://www.sqlbi.com/articles/header-detail-vs-star-schema-models-in-tabular-and-power-bi/
- When: A header and detail source; the header table also takes much memory.
- Version: A fact-to-fact link needs its written reason, and a both-direction one its M405 row (relationships and dates, rules 2 and 18).
