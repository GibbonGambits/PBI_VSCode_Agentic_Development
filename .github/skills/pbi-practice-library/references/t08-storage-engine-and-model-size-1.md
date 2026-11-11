# Storage engine, model size and memory

Part 1 of 1 of this topic. Covers: Reducing column cardinality; Calculated column and table storage; Measuring model size; Analysis Services processing.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### Reducing column cardinality

**T08-A016-5.** Split full timestamps into a date and a time column: the date column then holds at most 365 distinct values per year stored, and the time column is bounded by its grain, 86,400 values at one second.
- Should. 2012. https://www.sqlbi.com/articles/optimizing-high-cardinality-columns-in-vertipaq/
- When: A date-time column holds full event timestamps.

**T08-A030-2.** Also usually useless for analysis, and best left out of the import: a fact table's primary key or identity column, which serves neither analysis nor lookups from other tables, and housekeeping columns such as replication or audit identifiers, last-update dates and last-update users.
- Should. 2013. https://www.sqlbi.com/articles/checklist-for-memory-optimizations-in-powerpivot-and-tabular-models/
- When: Choosing which source columns to import into a Tabular model.

**T08-A030-5.** A column that can be derived from other columns should not be imported: load only the base columns, which have fewer distinct values, and compute the result in a measure, for example quantity times price summed with SUMX in place of a stored amount.
- Should. 2013. https://www.sqlbi.com/articles/checklist-for-memory-optimizations-in-powerpivot-and-tabular-models/
- When: A source table holds denormalised columns, such as an amount beside quantity and price.

**T08-A030-6.** A derived value that was left out of the import to save memory should not return as a calculated column: it would still take the memory of a column with many distinct values. Compute it in a measure.
- Should. 2013. https://www.sqlbi.com/articles/checklist-for-memory-optimizations-in-powerpivot-and-tabular-models/
- When: A derivable column, such as a sales amount, was dropped from the import.

**T08-A030-9.** Numbers count too: round to whole values where decimals do not matter to the analysis. Where a time is stored with milliseconds, cut it at least to the second. The data type alone changes nothing; distinct values must fall.
- Should. 2013. https://www.sqlbi.com/articles/checklist-for-memory-optimizations-in-powerpivot-and-tabular-models/
- When: Extra precision in a numeric or time column is not needed for analysis.

**T08-A030-10.** Take care when lowering precision: a change of data type alone frees no memory. The column shrinks only when it ends up holding fewer distinct values.
- Consider. 2013. https://www.sqlbi.com/articles/checklist-for-memory-optimizations-in-powerpivot-and-tabular-models/
- When: Reducing the precision of a column to save memory.

### Measuring model size

**T08-A059-1.** When optimising a data model, analyse the memory size of its tables and columns, so that the columns that cost the most are found first.
- Should. 2013. https://www.sqlbi.com/articles/checklist-for-memory-optimizations-in-powerpivot-and-tabular-models/ ; https://www.sqlbi.com/articles/data-model-size-with-vertipaq-analyzer/
- When: Reducing the size of a model in Power BI, Analysis Services Tabular or Power Pivot.
- Version: Older sources: the DMV $system.Discover_object_memory_usage, and helper workbooks for Power Pivot and Analysis Services.

**T08-A059-2.** To study object sizes in one database, VertiPaq Analyzer is an option: it collects the size of every object in one pass and ranks the costliest columns across all tables, where DMVs must be queried one by one and cannot group or join.
- Option. Check. 2015. https://www.sqlbi.com/articles/data-model-size-with-vertipaq-analyzer/
- When: Analysing the size of the objects of one specific database.
- Version: Its first version was a Power Pivot workbook; from version 2 only its entities and measures still apply.

**T08-A107-2.** For accurate dictionary sizes in a Power BI file, run VertiPaq Analyzer straight after opening the file, with no refresh and no edit of a calculated table's expression in between. After either, save, close and reopen the file before measuring again.
- Must. 2017. https://www.sqlbi.com/articles/measuring-the-dictionary-size-of-a-column-correctly/
- When: Measuring column dictionary sizes of a Power BI model with VertiPaq Analyzer.

**T08-A108-6.** When comparing the storage compression of tables or columns with VertiPaq Analyzer, apply the procedure for measuring dictionary size correctly, so that inflated dictionary figures do not distort the comparison.
- Should. 2017. https://www.sqlbi.com/articles/storage-differences-between-calculated-columns-and-calculated-tables/
- When: Comparing the storage compression of different techniques with VertiPaq Analyzer.

## Special-case techniques and facts

### Reducing column cardinality

**T08-A016-2.** A needed column with very many distinct values can also be stored as two or more part columns that each hold far fewer distinct values, and be put together again when the original value is wanted; each part gets a much smaller dictionary.
- Option. 2012. https://www.sqlbi.com/articles/optimizing-high-cardinality-columns-in-vertipaq/
- When: The column cannot be dropped; reading the original value then costs extra work, worth it in large tables.

**T08-A016-3.** A column split meant to shrink the model must be made in the source query or in data preparation, before import. Deriving the parts with calculated columns saves nothing, because the original column then stays stored.
- Must. 2012. https://www.sqlbi.com/articles/optimizing-high-cardinality-columns-in-vertipaq/
- When: A column with very many distinct values is split into several columns to save memory.

**T08-A016-4.** After a column is stored as split parts, DISTINCTCOUNT on one column no longer gives its distinct count. COUNTROWS over a SUMMARIZE grouped by every part column returns the same number, but can be far slower and press hard on query memory.
- Fact. 2012. https://www.sqlbi.com/articles/optimizing-high-cardinality-columns-in-vertipaq/
- When: A many-valued column was split into parts; worst when many rows enter the calculation.

**T08-A016-7.** For an integer column with very many distinct values, such as a transaction ID, one option is to import two or more integer columns made by integer division and remainder instead. One test: 100 million IDs fell from about 3 GB to under 200 MB.
- Option. 2012. https://www.sqlbi.com/articles/optimizing-high-cardinality-columns-in-vertipaq/
- When: The identifier is still needed, for example to find one transaction.

**T08-A016-8.** When an integer ID exists only as high and low part columns, a measure can return the original ID: the high part multiplied by the split factor, plus the low part, with blank returned where that expression cannot be worked out.
- Option. 2012. https://www.sqlbi.com/articles/optimizing-high-cardinality-columns-in-vertipaq/
- When: The original identifier column was not imported, only its split parts.

**T08-A016-9.** A search for one original ID in a table that holds only its split parts must filter each part column by its own part: work out the parts of the searched value by integer division and remainder with the split factor (INT, MOD).
- Must. 2012. https://www.sqlbi.com/articles/optimizing-high-cardinality-columns-in-vertipaq/
- When: An integer identifier was imported as high and low part columns only.

**T08-A016-10.** Before splitting an integer column with very many distinct values into more than two parts for extra savings, weigh processing time and the number of cores beside storage size: more parts need more resources to process, and with few cores processing takes longer.
- Consider. 2012. https://www.sqlbi.com/articles/optimizing-high-cardinality-columns-in-vertipaq/
- When: A split into three or more part columns is considered; partitioned tables need a deeper evaluation.

**T08-A016-11.** When a text column with too many distinct values is split, such as a transaction ID holding letters, cut it with string functions at a position picked from how the values are distributed, so that the parts fill two small dictionaries.
- Should. 2012. https://www.sqlbi.com/articles/optimizing-high-cardinality-columns-in-vertipaq/
- When: A many-valued text column must stay in the model; the split is made before import.

**T08-A016-12.** One option when a date-time is split into a date and a time column: cut the time down to whole seconds in the source query, so the time column can never pass 86,400 distinct values.
- Option. 2012. https://www.sqlbi.com/articles/optimizing-high-cardinality-columns-in-vertipaq/
- When: An event timestamp is split into date and time columns before import.

**T08-A030-7.** A column with too many distinct values that cannot go, such as a fact table's transaction ID kept for drillthrough, is worth considering for a split into several parts: each part has few distinct values and together they use less memory.
- Consider. 2013. https://www.sqlbi.com/articles/checklist-for-memory-optimizations-in-powerpivot-and-tabular-models/
- When: A many-valued column has to stay in the model.

### Calculated column and table storage

**T08-A030-3.** Take care with calculated columns in a fact table that use CALCULATE, or refer to a measure: as soon as a second one is defined, a circular reference error appears. A fact table seldom needs such columns.
- Consider. 2013. https://www.sqlbi.com/articles/checklist-for-memory-optimizations-in-powerpivot-and-tabular-models/
- When: Adding calculated columns to a fact table.

**T08-A108-1.** Why a calculated column can compress worse: the engine leaves it out when it searches for the row order that compresses best, so it inherits the order picked for the native columns. The weaker compression can also slow queries that scan the column.
- Fact. 2017. https://www.sqlbi.com/articles/storage-differences-between-calculated-columns-and-calculated-tables/
- When: Calculated columns in imported tables, except those tied one-to-one to a native column.

**T08-A108-2.** A calculated column tied one-to-one to a native column, at the same cardinality, such as a key brought in with RELATED or LOOKUPVALUE, reuses that column's sort order and may compress as well. One that changes cardinality, such as MONTH of a date, may not.
- Fact. 2017. https://www.sqlbi.com/articles/storage-differences-between-calculated-columns-and-calculated-tables/
- When: Comparing a calculated column with native columns of the same table.

**T08-A108-3.** Calculated columns can lengthen processing against native columns for this reason: their DAX expressions are evaluated one after another, and several calculated columns may not be worked out fully in parallel.
- Fact. 2017. https://www.sqlbi.com/articles/storage-differences-between-calculated-columns-and-calculated-tables/
- When: Judging the refresh cost of calculated columns.

**T08-A108-4.** Every column a calculated table's expression returns is compressed like a native column, as in a table loaded from a source or a Power Query query. Calculated columns added on top of a calculated table still behave as calculated columns.
- Fact. 2017. https://www.sqlbi.com/articles/storage-differences-between-calculated-columns-and-calculated-tables/
- When: Judging the compression of calculated tables.
- Version: Calculated tables: Analysis Services 2016 and Power BI; not in Power Pivot as of August 2017.

**T08-A108-5.** Processing a calculated table with very many rows may first hold the whole table uncompressed in memory. The need depends on the row count and the query plan: CROSSJOIN materialises only its two arguments, while ALL may materialise every existing combination of its columns.
- Fact. 2017. https://www.sqlbi.com/articles/storage-differences-between-calculated-columns-and-calculated-tables/
- When: Calculated tables with very many rows; tens of thousands of rows or fewer are rarely an issue.

### Measuring model size

**T08-A107-1.** Right after a refresh, the dictionary size VertiPaq Analyzer or the storage DMV reports for a column is the memory reserved: it starts at 1 MB a column, is not trimmed, and can far overstate the real size. Reopening the file gives the true figure.
- Fact. Check. 2017. https://www.sqlbi.com/articles/measuring-the-dictionary-size-of-a-column-correctly/
- When: Columns with a dictionary (all text columns, many numeric ones), measured after a refresh.

**T08-A107-3.** A calculated table whose DAX expression depends on no other table is not rebuilt by a refresh. Any change to that expression, even new indentation only, does rebuild it, and its columns show inflated dictionary sizes again.
- Fact. 2017. https://www.sqlbi.com/articles/measuring-the-dictionary-size-of-a-column-correctly/
- When: Calculated tables with no dependency on other tables, when dictionary sizes are measured.

**T08-A107-4.** For correct dictionary sizes of a Power Pivot model, one way is to save the workbook, import it into Power BI with its existing data and no reprocessing, and run VertiPaq Analyzer on that model without pressing Refresh.
- Option. Check. 2017. https://www.sqlbi.com/articles/measuring-the-dictionary-size-of-a-column-correctly/
- When: Measuring a Power Pivot model; figures stay right only until Refresh is used in Power BI.
- Version: Written when VertiPaq Analyzer could not connect to a Power Pivot model directly (2017).

### Analysis Services processing

**T08-A039-1.** One way to show when a Tabular database was last processed: a calculated column defined as NOW () and a measure returning its MAX. The column holds a single value on all rows, so it takes almost no memory at any table size.
- Option. 2014. https://www.sqlbi.com/articles/last-process-date-in-ssas-tabular/
- When: Last process time shown in DAX or MDX queries; reliable only if the column's table is in every process operation.

**T08-A039-2.** A NOW () calculated column that records the last process time must sit in a table that every process operation includes. When other tables are processed without it, the time shown can be wrong; a Process Full of the whole database is always right.
- Must. 2014. https://www.sqlbi.com/articles/last-process-date-in-ssas-tabular/
- When: The last process time of an Analysis Services Tabular database is kept in a calculated column.

**T08-A039-3.** Where single tables or partitions may be processed, read the last process time from the MDSCHEMA_CUBES DMV, taking the latest LAST_DATA_UPDATE, and not from the XMLA Discover result: that one moves only on a full process of the whole database.
- Must. Check. 2014. https://www.sqlbi.com/articles/last-process-date-in-ssas-tabular/
- When: Finding the last process time of an Analysis Services Tabular database with partial processing.

**T08-A039-4.** Convert the LAST_DATA_UPDATE value that Analysis Services returns to local time before showing it: the server gives the date and time in UTC.
- Must. 2014. https://www.sqlbi.com/articles/last-process-date-in-ssas-tabular/
- When: Reading the last process time from XMLA or from the MDSCHEMA_CUBES DMV.

**T08-A107-5.** On Analysis Services Tabular, these bring an oversized dictionary allocation down to the minimum: detaching and re-attaching the database; restoring it from a backup; restarting the instance or its machine, which hits every user; for an integrated workspace, closing and reopening the Visual Studio solution.
- Option. 2017. https://www.sqlbi.com/articles/measuring-the-dictionary-size-of-a-column-correctly/
- When: A new table's first processing likely left more dictionary memory allocated than needed.
- Version: On Azure Analysis Services, pausing and starting the service counts as a restart.

**T08-A107-6.** On Analysis Services the extra dictionary memory that VertiPaq Analyzer shows is truly allocated, not a reporting error; only a detach and attach, a restore or a restart frees it. It seldom matters on a large database; small databases with hundreds of columns may gain.
- Fact. 2017. https://www.sqlbi.com/articles/measuring-the-dictionary-size-of-a-column-correctly/
- When: Analysis Services Tabular databases showing inflated dictionary sizes.

**T08-A107-7.** Dictionaries on an always-on Analysis Services server can exceed the size needed. Process Full (database or table) and Process Data (table) always build new dictionaries for hash-encoded columns; other processing adds overhead only to columns receiving values new to their dictionary.
- Consider. 2017. https://www.sqlbi.com/articles/measuring-the-dictionary-size-of-a-column-correctly/
- When: Reading dictionary sizes on a server running all day; partial refresh leaves a mix of column states.
