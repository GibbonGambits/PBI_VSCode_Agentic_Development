# Relationships and filter propagation

Part 1 of 1 of this topic. Covers: Many-to-many relationships; Virtual relationships in DAX; Bidirectional filters and propagation; Blank row and limited relationships; Inactive relationships and date roles.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### Many-to-many relationships

**T05-A182-11.** When talking about a model, call relationship cardinalities SMR (one-to-many) and MMR (many-to-many cardinality). Keep the words many-to-many for the logical link between two dimensions that is built from two one-to-many relationships.
- Should. 2020. https://www.sqlbi.com/articles/relationships-in-power-bi-and-tabular-models/
- When: Describing or documenting the relationships of a Tabular model.

### Virtual relationships in DAX

**T05-A080-1.** Prefer a physical relationship in the model to a virtual relationship written in DAX when a filter on one table must reach another. The storage engine carries the filter of a physical relationship; the virtual forms cost more.
- Should. 2016. https://www.sqlbi.com/articles/physical-and-virtual-relationships-in-dax/
- When: A filter has to pass from one table to another.

**T05-A080-6.** Read the query plan of whichever virtual relationship technique a measure uses. The relative speed of the techniques depends on the engine version and can change.
- Should. 2016. https://www.sqlbi.com/articles/physical-and-virtual-relationships-in-dax/
- When: Tables without a physical relationship are linked in DAX.

**T05-A182-1.** TREATAS is also preferred to the older IN and FILTER with CONTAINS forms of a virtual relationship. Write it as a CALCULATE filter argument that applies the lookup column's values to the matching column of the target table. FILTER with CONTAINS is slower than INTERSECT.
- Should. 2016. https://www.sqlbi.com/articles/physical-and-virtual-relationships-in-dax/ ; https://www.sqlbi.com/articles/relationships-in-power-bi-and-tabular-models/
- When: A filter moves between tables by equal column values, inside CALCULATE or CALCULATETABLE.
- Version: TREATAS exists in Power BI and in Analysis Services from 2017.

**T05-A182-12.** One recommended editor for Power BI and Analysis Services Tabular models is Tabular Editor; the modelling concepts are the same whichever tool is used.
- Should. 2020. https://www.sqlbi.com/articles/relationships-in-power-bi-and-tabular-models/
- When: A person edits the objects of a Power BI or Analysis Services Tabular model outside this template's files.

**T05-A095-1.** To pass a filter between tables, use a physical relationship whenever one is possible, and a virtual one with TREATAS only otherwise. The FILTER pattern is the last resort, for a DAX version that has neither TREATAS nor INTERSECT.
- Should. Check. 2020. https://www.sqlbi.com/articles/propagate-filters-using-treatas-in-dax/
- When: Choosing how a filter travels between two tables; virtual is acceptable when few values are passed.
- Version: FILTER works in every DAX version, INTERSECT since 2016, TREATAS since Power BI Desktop of February 2017.

**T05-A095-2.** When a virtual relationship passes many unique values, look at a physical relationship in its place. A virtual one is an alternative only while the values stay in the hundreds; on a high-cardinality key the physical form can be ten to a hundred times faster.
- Consider. 2020. https://www.sqlbi.com/articles/propagate-filters-using-treatas-in-dax/
- When: A virtual relationship in a model that could hold a physical one.

**T05-A095-5.** Before keeping a virtual relationship, time it on your own model and confirm that its cost is acceptable. On a small number of values it differs little from a physical one, and it leaves the model unchanged.
- Should. 2020. https://www.sqlbi.com/articles/propagate-filters-using-treatas-in-dax/
- When: A virtual relationship is considered in place of a physical one.

**T05-A095-7.** When an INTERSECT virtual relationship is rewritten with TREATAS, swap the arguments: TREATAS takes first the table expression read from the filter context, then the target column or columns.
- Must. 2020. https://www.sqlbi.com/articles/propagate-filters-using-treatas-in-dax/
- When: Converting a virtual relationship from INTERSECT to TREATAS.

### Bidirectional filters and propagation

**T05-A141-2.** When a both-direction relationship is used, verify that it leaves no more than one filter path between any two tables of the model.
- Must. 2018. https://www.sqlbi.com/articles/bidirectional-relationships-and-ambiguity-in-dax/
- When: One of the few cases where a both-direction relationship is worth having.

**T05-A236-1.** Sending a filter to the one side always costs more than sending it to the many side. One safe both-direction case: between a dimension and an intermediate table built only to link tables of different grain, where the filter still flows one way.
- Should. 2018. https://www.sqlbi.com/articles/bidirectional-relationships-and-ambiguity-in-dax/ ; https://www.sqlbi.com/articles/relationships-in-power-bi-and-tabular-models/ ; https://www.sqlbi.com/articles/different-options-to-model-many-to-many-relationships-in-power-bi-and-tabular/
- When: Deciding whether a one-to-many or many-to-many relationship should filter both ways.

**T05-A158-5.** Give measures that exist only to filter slicers a recognisable prefix, such as Slicer, so they stand out among the other measures of a model.
- Should. 2019. https://www.sqlbi.com/articles/syncing-slicers-in-power-bi/
- When: Helper measures used only as a slicer's visual filter.

### Blank row and limited relationships

**T05-A165-6.** Never build on invalid relationships: make a check for many-side keys without a one-side match part of the data quality process.
- Must. 2019. https://www.sqlbi.com/articles/blank-row-in-dax/
- When: Every model with relationships.

**T05-A165-7.** When a model may hold invalid relationships, review each measure and confirm whether its logic includes or ignores the blank row.
- Must. 2019. https://www.sqlbi.com/articles/blank-row-in-dax/
- When: Many-side key values may lack a matching one-side row.

**T05-A267-2.** Build reports with extra care on a limited relationship that has unmatched keys. No blank row is made, so the unmatched amount shows on no row and readers see a total that differs from the sum of its rows.
- Must. 2023. https://www.sqlbi.com/articles/understanding-blank-row-and-limited-relationships/
- When: Cross-island or many-to-many cardinality relationships where some keys do not match.

**T05-A167-2.** Keep in mind that a limited relationship gets no blank row for keys missing on the one side: the unmatched many-side values belong to no item, so the total differs from the sum of the items shown.
- Consider. 2019. https://www.sqlbi.com/articles/strong-and-weak-relationships-in-power-bi/
- When: Any limited relationship, above all one that is really one-to-many inside one storage.

**T05-A167-4.** A limited relationship can be relied on while its join column has few values, up to roughly 100 to 200. Above that, treat it with great care: no join structure is built at refresh, so queries scan the fact table several times.
- Consider. Check. 2019. https://www.sqlbi.com/articles/strong-and-weak-relationships-in-power-bi/
- When: A many-to-many cardinality or cross-source relationship, judged by its join column.

**T05-A167-5.** Be wary of many-to-many cardinality on data that is really one-to-many. The setting alone makes the relationship limited, even inside one Import storage, so keys missing on the one side get no blank row.
- Consider. 2019. https://www.sqlbi.com/articles/strong-and-weak-relationships-in-power-bi/
- When: Two tables in the same storage whose data is one-to-many.

### Inactive relationships and date roles

**T05-A194-2.** USERELATIONSHIP can only switch on a relationship that the model already defines. It cannot create a new one.
- Must. 2020. https://www.sqlbi.com/articles/using-userelationship-in-dax/
- When: Any formula that calls USERELATIONSHIP.

**T05-A194-3.** By convention the first argument of USERELATIONSHIP is the many-side column and the second the one-side column. The reverse order returns the same result.
- Option. 2020. https://www.sqlbi.com/articles/using-userelationship-in-dax/
- When: Writing a USERELATIONSHIP call.

**T05-A258-1.** When a fact has several date columns, start from one shared Date table related to each, one relationship active. Measures on different dates can then share one date axis in a visual. Add more date tables only when a visual needs two dates.
- Should. 2022. https://www.sqlbi.com/articles/using-cross-highlight-with-order-and-delivery-dates-in-power-bi/
- When: A fact table with two or more date columns for one event.

**T05-A258-2.** With one shared Date table, every pairing of a calculation with a non-default date that reports use needs its own measure, each switching on the inactive relationship with USERELATIONSHIP in CALCULATE.
- Must. 2022. https://www.sqlbi.com/articles/using-cross-highlight-with-order-and-delivery-dates-in-power-bi/
- When: A shared Date table related to several date columns, one relationship active.

## Special-case techniques and facts

### Many-to-many relationships

**T05-A021-1.** In a many-to-many measure over a bridge table, prefer filtering the fact with SUMMARIZE of the bridge, grouped by the intermediate dimension's key, to a FILTER over that dimension that runs CALCULATE with COUNTROWS of bridge rows once per row.
- Should. Check. 2012. https://www.sqlbi.com/articles/optimize-many-to-many-calculation-in-dax-with-summarize-and-cross-table-filtering/
- When: A measure sums a fact for dimension members that reach it only through a bridge table.
- Version: Written for the engines of 2012, which had no many-to-many relationship in the model.

**T05-A021-2.** A many-to-many measure can also give the bridge table itself to CALCULATE as a filter argument. Cross-table filtering then does the work and no key column is named, which suits generated code. Speed is about that of the SUMMARIZE form.
- Option. Check. 2012. https://www.sqlbi.com/articles/optimize-many-to-many-calculation-in-dax-with-summarize-and-cross-table-filtering/
- When: A fact is reached from a dimension only through a bridge table and an intermediate dimension.

**T05-A078-1.** With the bridge table as a CALCULATE filter argument, the bridge filter always applies. Fact rows whose intermediate-dimension member has no bridge row, such as an account without an owner, are left out, also from the grand total.
- Fact. 2016. https://www.sqlbi.com/articles/many-to-many-relationships-in-power-bi-and-excel-2016/
- When: A many-to-many measure filters by the bridge table and some members have no bridge row.
- Version: Shown for Power Pivot 2010 and 2013 and Analysis Services 2012 and 2014.

**T05-A078-2.** When the bridge filter must apply only while the far dimension is filtered, the measure must branch with IF on ISCROSSFILTERED over that dimension's key and hold the calculation twice: once with the bridge table as filter, once without.
- Must. Check. 2016. https://www.sqlbi.com/articles/many-to-many-relationships-in-power-bi-and-excel-2016/
- When: Many-to-many solved in DAX with the bridge as CALCULATE filter, without a both-direction relationship.
- Version: A technique for Power Pivot 2010 and 2013 and Analysis Services 2012 and 2014.

**T05-A078-4.** For a many-to-many bridge, CROSSFILTER set to Both on the relationship between the bridge and the intermediate dimension, inside CALCULATE, can stand in for a both-direction relationship in the model. Every measure that crosses the bridge must then carry it.
- Option. Check. 2016. https://www.sqlbi.com/articles/many-to-many-relationships-in-power-bi-and-excel-2016/
- When: The model cannot hold a both-direction filter on the bridge relationship.
- Version: CROSSFILTER arrived in 2016 (Excel, Analysis Services, Power BI); Excel 2016 cannot set both directions on a model relationship.

**T05-A182-8.** A coarser table, such as a budget by brand and country, can be linked through a calculated table of the distinct shared values from both sides. Relate it one-to-many to the dimension and to the coarse table, and let the dimension relationship filter both ways.
- Option. 2020. https://www.sqlbi.com/articles/relationships-in-power-bi-and-tabular-models/
- When: The coarse table's grain allows no one-to-many relationship to the dimension.

**T05-A182-10.** When the column of a different-grain relationship has thousands of values or more, weigh an intermediate calculated table with two one-to-many relationships against one many-to-many cardinality relationship, which has no index and is slower. With about 10 to 100 values the difference can be ignored.
- Consider. 2020. https://www.sqlbi.com/articles/relationships-in-power-bi-and-tabular-models/
- When: Tables at different grain joined by a many-to-many cardinality relationship.
- Version: Many-to-many cardinality relationships exist since 2018.

**T05-A236-3.** When a many-to-many between dimensions cannot use a both-direction relationship, relate both dimensions to the bridge and link the bridge to the fact by a many-to-many cardinality relationship that filters one way. Test well: some queries get faster, others slower.
- Option. 2021. https://www.sqlbi.com/articles/different-options-to-model-many-to-many-relationships-in-power-bi-and-tabular/
- When: A bridge design where a both-direction relationship would cause ambiguity.

**T05-A236-4.** Test performance thoroughly before a model goes to production with a bridge table tied to the fact by a limited many-to-many cardinality relationship. Its query plans are faster for some queries and slower for others than those of the both-direction bridge.
- Should. 2021. https://www.sqlbi.com/articles/different-options-to-model-many-to-many-relationships-in-power-bi-and-tabular/
- When: Adopting the limited bridge layout in place of a both-direction relationship.

**T05-A236-5.** Choose between the both-direction bridge and the limited many-to-many layout from the queries users will run. The both-direction bridge fits when the many-to-many path is rarely used; the limited layout pays off when every query goes through it.
- Should. 2021. https://www.sqlbi.com/articles/different-options-to-model-many-to-many-relationships-in-power-bi-and-tabular/
- When: Modelling a many-to-many relationship between two dimensions.

**T05-A236-7.** When a dimension reaches the fact only through the bridge table, every query that filters or groups by that dimension alone still passes the bridge. It runs much slower than with a direct one-to-many relationship to the fact.
- Fact. Check. 2021. https://www.sqlbi.com/articles/different-options-to-model-many-to-many-relationships-in-power-bi-and-tabular/
- When: A layout where both dimensions relate to the bridge and only the bridge relates to the fact.

**T05-A236-8.** With a both-direction bridge, queries that cross the bridge lean heavily on the formula engine, most of all when the both-direction filter combines with other relationships. Queries that skip the bridge are much faster, so speed varies widely.
- Fact. Check. 2021. https://www.sqlbi.com/articles/different-options-to-model-many-to-many-relationships-in-power-bi-and-tabular/
- When: A many-to-many between dimensions built with a bridge and a both-direction relationship.

**T05-A236-9.** An optimized layout keeps the bridge on a limited relationship to the fact and relates the dimension sharing the bridge key straight to the fact, so both filter one fact column. It tested fast, but counts across the two dimensions miss members without fact rows.
- Option. Check. 2021. https://www.sqlbi.com/articles/different-options-to-model-many-to-many-relationships-in-power-bi-and-tabular/
- When: A many-to-many between dimensions through a bridge table.

**T05-A236-10.** Where a dimension relates straight to the fact and no longer to the bridge, an inactive relationship between that dimension and the bridge can be added. Measures that must pass a filter between the two dimensions switch it on with USERELATIONSHIP in CALCULATE.
- Option. 2021. https://www.sqlbi.com/articles/different-options-to-model-many-to-many-relationships-in-power-bi-and-tabular/
- When: The optimized many-to-many layout, in which the bridge no longer links the two dimensions.

**T05-A236-11.** For extreme tuning only, a model can hold both many-to-many layouts, with measures that choose one per query through IF, CROSSFILTER and USERELATIONSHIP. It is possible but not advised: switching layout has its own cost and disables several optimizations.
- Option. 2021. https://www.sqlbi.com/articles/different-options-to-model-many-to-many-relationships-in-power-bi-and-tabular/
- When: Extreme optimization of a many-to-many relationship between dimensions.

### Virtual relationships in DAX

**T05-A080-4.** Where TREATAS does not exist, a virtual relationship can be INTERSECT of ALL of the target column with VALUES of the lookup column, as a CALCULATE filter argument. It needs less formula engine work than FILTER with CONTAINS, yet more than a physical relationship.
- Option. Check. 2016. https://www.sqlbi.com/articles/physical-and-virtual-relationships-in-dax/
- When: No physical relationship exists and the engine has no TREATAS.
- Version: INTERSECT exists since Excel 2016 and Analysis Services 2016; early Excel 2016 builds could fail on it.

**T05-A080-5.** A virtual relationship can also be a CALCULATE filter built with FILTER over ALL of the target key column, keeping the values that CONTAINS finds in VALUES of the lookup key column. It works but needs more storage engine queries; TREATAS is preferred when available.
- Option. Check. 2016. https://www.sqlbi.com/articles/physical-and-virtual-relationships-in-dax/
- When: No physical relationship exists between the two tables.
- Version: Works in every DAX version since Excel 2010.

**T05-A182-2.** A virtual relationship that matches on several columns performs poorly. A physical relationship on one column is faster by orders of magnitude.
- Fact. 2020. https://www.sqlbi.com/articles/relationships-in-power-bi-and-tabular-models/
- When: A filter moves between tables on a combination of columns.

**T05-A182-13.** A virtual relationship can rest on a condition, not only on equal values. To match rows to bands with a minimum and a maximum, such as prices to price ranges, a CALCULATE filter keeps the target values that fall inside the visible ranges.
- Option. 2020. https://www.sqlbi.com/articles/relationships-in-power-bi-and-tabular-models/
- When: A relationship based on a range, as in dynamic segmentation; it may be slower than a physical one.

**T05-A095-6.** To filter on a list of value combinations over columns of different tables, such as chosen colour and country pairs, TREATAS can take the table of combinations directly. INTERSECT over a CROSSJOIN of the columns first builds a table nobody needs.
- Option. 2020. https://www.sqlbi.com/articles/propagate-filters-using-treatas-in-dax/
- When: An arbitrarily shaped filter, above all on columns of different tables.

**T05-A095-8.** When a filter must travel on a combination of columns that no relationship can join, such as year and month from a daily Date table to a monthly table, TREATAS in CALCULATE can map a SUMMARIZE of those columns onto the target's columns.
- Option. 2020. https://www.sqlbi.com/articles/propagate-filters-using-treatas-in-dax/
- When: Grain set by two or more columns; good for hundreds of combinations, not for many more.

### Bidirectional filters and propagation

**T05-A099-1.** A filter on a dimension column, such as `Product[Color]`, is not turned into a filter on the fact's key column. ALL on either key column of the relationship leaves it active on the fact, because filters follow expanded tables, not keys.
- Fact. 2017. https://www.sqlbi.com/articles/filtering-tables/
- When: A measure removes filters with ALL in CALCULATE while a dimension column is filtered.

**T05-A099-2.** ALL over a whole fact table in CALCULATE clears the filters on every column of the expanded fact table, columns of related one-side dimensions included. ALL that lists only the fact's own columns leaves those dimension filters in place.
- Fact. 2017. https://www.sqlbi.com/articles/filtering-tables/
- When: A measure uses ALL in CALCULATE while columns of a related dimension are filtered.

**T05-A099-3.** To ignore a filter that reaches a fact through a bridge table with a both-direction relationship, apply ALL to the bridge table. ALL on the fact or on the intermediate dimension leaves it: such a filter is injected directly, not through table expansion.
- Must. 2017. https://www.sqlbi.com/articles/filtering-tables/
- When: A many-to-many bridge filters both ways and a measure must ignore the far dimension's selection.
- Version: Both-direction filtering exists from Analysis Services 2016 and in Power BI.

**T05-A141-4.** A model with more than one filter path between two tables is ambiguous even when no error appears: the engine may quietly choose a preferred path, by an algorithm people can hardly follow. No error is therefore no proof of a sound model.
- Fact. 2018. https://www.sqlbi.com/articles/bidirectional-relationships-and-ambiguity-in-dax/
- When: A both-direction relationship opens a second path, for example from Date to a fact through another fact.

**T05-A141-5.** In a model made ambiguous by a both-direction relationship, one calculation can send a filter along several paths at once. Which paths are used changes with the filters present and the relationships active, so measures that look alike return different numbers.
- Fact. 2018. https://www.sqlbi.com/articles/bidirectional-relationships-and-ambiguity-in-dax/
- When: Measures in an ambiguous model, for instance ones that switch a relationship off with CROSSFILTER.

**T05-A158-3.** A measure that only hides slicer items without fact rows should test `NOT ISEMPTY ( Sales )`, not work out a business measure such as a sales amount. The emptiness test is faster.
- Should. 2019. https://www.sqlbi.com/articles/syncing-slicers-in-power-bi/
- When: A measure used only as a visual filter on a slicer.

**T05-A158-4.** A measure made for a slicer's visual filter must return a whole number: wrap its true-or-false test in INT and keep the items where the result is 1. The visual filter cannot compare a Boolean value.
- Must. Check. 2019. https://www.sqlbi.com/articles/syncing-slicers-in-power-bi/
- When: A slicer filter measure whose logic is a true-or-false test, such as NOT ISEMPTY.

**T05-A158-7.** To keep the slicer items that meet two conditions together, two helper measures, one per condition, can both go into the slicer's visual filter. Filters on one visual combine with a logical AND.
- Option. 2019. https://www.sqlbi.com/articles/syncing-slicers-in-power-bi/
- When: All conditions must hold, for example colours with both sales and purchases.

**T05-A158-8.** To keep the slicer items that meet at least one of several conditions, write one helper measure that joins the conditions with OR and use it as the visual filter. Separate filters on a visual always combine with AND.
- Must. 2019. https://www.sqlbi.com/articles/syncing-slicers-in-power-bi/
- When: An item should show when any condition holds, such as sales or purchases.

**T05-A158-9.** Prefer a single helper measure that holds every condition of a slicer's visual filter to several separate measures. It is slightly easier to edit in the report and leaves room for more complex logic.
- Should. 2019. https://www.sqlbi.com/articles/syncing-slicers-in-power-bi/
- When: A slicer filtered by measures; with AND conditions, separate measures also give correct results.

**T05-A158-10.** Weigh the cost before a measure that filters a slicer uses RANKX, for example to list only the top products of a period. RANKX is expensive and slows the page; it need not be avoided, only used with care.
- Consider. Check. 2019. https://www.sqlbi.com/articles/syncing-slicers-in-power-bi/
- When: A slicer's visual filter rests on a ranking measure.

**T05-A333-1.** A matrix with only columns from several tables and no measure makes Power BI look for a table they all filter, and use it as a bridge to limit the combinations. Without one the visual fails with "can't determine relationship between the fields".
- Fact. 2025. https://www.sqlbi.com/articles/understanding-the-cant-determine-relationship-between-the-fields-error-in-power-bi/
- When: A visual groups by columns of more than one table and has no measure.

**T05-A333-2.** To fix a visual that reports "can't determine relationship between the fields", add a measure that decides which combinations of values show. With any measure present, Power BI lets DAX decide the rows and stops looking for a bridge table.
- Should. 2025. https://www.sqlbi.com/articles/understanding-the-cant-determine-relationship-between-the-fields-error-in-power-bi/
- When: A visual with columns from several tables, no measure, and no table they all filter.

**T05-A333-3.** When a visual groups by columns of different tables, the values of each table are cross-joined and only the rows where every measure is blank are dropped. A measure that returns zero for blank therefore fills the visual with every combination.
- Fact. 2025. https://www.sqlbi.com/articles/understanding-the-cant-determine-relationship-between-the-fields-error-in-power-bi/
- When: A visual groups by columns that come from more than one table.

**T05-A333-4.** A combination of columns of one table that does not exist in the table is removed by auto-exists and can never be shown. A combination dropped only because every measure is blank can be brought back with Show items with no data.
- Fact. 2025. https://www.sqlbi.com/articles/understanding-the-cant-determine-relationship-between-the-fields-error-in-power-bi/
- When: A visual groups by several columns of one table, such as category and subcategory.

### Blank row and limited relationships

**T05-A182-3.** A limited relationship takes no part in table expansion. Every relationship with many-to-many cardinality is limited, even inside one data island, and so is one whose one-side key the engine cannot verify as unique. Older guidance required a unique column on one side.
- Fact. 2020. https://www.sqlbi.com/articles/relationships-in-power-bi-and-tabular-models/ ; https://www.sqlbi.com/articles/physical-and-virtual-relationships-in-dax/
- When: Judging how a relationship behaves in DAX.
- Version: Composite models and many-to-many cardinality relationships exist in Power BI since 2018.

**T05-A236-6.** Limited relationships are slow, because the engine does not materialize them.
- Fact. 2021. https://www.sqlbi.com/articles/different-options-to-model-many-to-many-relationships-in-power-bi-and-tabular/
- When: Any limited relationship in a model.

**T05-A165-2.** VALUES returns the blank row that an invalid relationship adds to the one-side table. DISTINCT never does: it returns only rows stored in the table. Counts built on the two functions therefore differ when a relationship is invalid.
- Fact. 2019. https://www.sqlbi.com/articles/blank-row-in-dax/
- When: Some many-side keys have no matching one-side row; otherwise both functions agree.

**T05-A165-3.** When a row count must include the blank row of an invalid relationship, use `COUNTROWS ( VALUES ( Product ) )`. A bare table reference never returns the blank row, so the blank item gets no count.
- Must. 2019. https://www.sqlbi.com/articles/blank-row-in-dax/
- When: The blank row must count as a row of a one-side table.

**T05-A165-4.** When a ratio of a filtered row count to the count of all rows does not total 100%, let both parts treat the blank row alike: VALUES of the table in the numerator, or ALLNOBLANKROW in place of ALL in the denominator.
- Option. 2019. https://www.sqlbi.com/articles/blank-row-in-dax/
- When: The table is the one side of an invalid relationship, so it has a blank row.

**T05-A165-5.** Agree with the users whether a calculation counts the blank row of an invalid relationship, and check the results with them: the possible versions differ slightly.
- Should. 2019. https://www.sqlbi.com/articles/blank-row-in-dax/
- When: Versions of a measure differ only in how they treat the blank row.

**T05-A267-1.** For an invalid regular relationship the engine adds one blank row to the one-side table and ties every unmatched many-side row to it, so report rows still sum to the total. A limited relationship gets none. VertiPaq Analyzer reports a referential integrity violation.
- Fact. 2019. https://www.sqlbi.com/articles/blank-row-in-dax/ ; https://www.sqlbi.com/articles/relationships-in-power-bi-and-tabular-models/ ; https://www.sqlbi.com/articles/understanding-blank-row-and-limited-relationships/
- When: A regular relationship where some many-side keys have no one-side match.

**T05-A167-1.** A relationship with many-to-many cardinality is limited too, even between two Import tables, and a developer can also define a relationship as limited. Limited and regular relationships behave differently in DAX.
- Fact. 2019. https://www.sqlbi.com/articles/strong-and-weak-relationships-in-power-bi/
- When: Judging whether a relationship is regular or limited.
- Version: Limited relationships came to Power BI in 2018 with composite models; Analysis Services 2019 allows them without composite models.

**T05-A167-3.** Take care with formulas that lean on table expansion when a limited relationship is involved: expansion does not cross a limited relationship.
- Consider. 2019. https://www.sqlbi.com/articles/strong-and-weak-relationships-in-power-bi/
- When: DAX code that relies on table expansion.

### Inactive relationships and date roles

**T05-A036-1.** Never use USERELATIONSHIP in a calculated column to reach another relationship. Fetch the value with LOOKUPVALUE, which does not depend on relationships. Where the active relationship serves, RELATED is faster than LOOKUPVALUE.
- Must. 2021. https://www.sqlbi.com/articles/userelationship-in-calculated-columns/
- When: A calculated column needs a value through an inactive relationship.

**T05-A036-2.** In a row context, CALCULATE with only USERELATIONSHIP returns the value of the default relationship. Context transition happens before the modifier applies and follows the default relationship; USERELATIONSHIP changes which relationship is active and filters nothing.
- Fact. 2021. https://www.sqlbi.com/articles/userelationship-in-calculated-columns/
- When: A calculated column or iteration where CALCULATE has no other filter argument.

**T05-A036-3.** RELATED cannot be called inside CALCULATE in a calculated column: CALCULATE removes the row context that RELATED needs, so the formula returns an error.
- Fact. 2021. https://www.sqlbi.com/articles/userelationship-in-calculated-columns/
- When: A calculated column that combines CALCULATE and RELATED.

**T05-A258-3.** A second date table beside the shared one can also be right when visuals based on different dates must cross-highlight each other, such as an order-date chart and a delivery-date chart. Keep the shared Date table, so measures can still share one axis.
- Option. 2022. https://www.sqlbi.com/articles/using-cross-highlight-with-order-and-delivery-dates-in-power-bi/
- When: Reports that need two dates of one event at the same time.

**T05-A258-4.** With an actively related second date table, the measure for that date can test it with ISFILTERED: when filtered, aggregate as is; otherwise switch on the inactive relationship to the shared Date table with USERELATIONSHIP. The active table then affects every measure.
- Option. 2022. https://www.sqlbi.com/articles/using-cross-highlight-with-order-and-delivery-dates-in-power-bi/
- When: Visuals on a shared and a second date table cross-highlight each other.

**T05-A258-5.** With an actively related second date table, a chart with that table on its axis can show the plain measure. Cross-highlighting from an order-date chart is then correct without extra DAX, though the order measure shows delivery amounts there, which is hard to explain.
- Option. 2022. https://www.sqlbi.com/articles/using-cross-highlight-with-order-and-delivery-dates-in-power-bi/
- When: An order-date chart cross-highlights a chart on the second date table.

**T05-A258-6.** If an active relationship from a second date table makes the model hard to use, because that table then changes every measure, consider making it inactive and switching it on only in the measures where its filter has a purpose.
- Consider. 2022. https://www.sqlbi.com/articles/using-cross-highlight-with-order-and-delivery-dates-in-power-bi/
- When: A shared Date table plus a second date table whose filter confuses users.

**T05-A258-7.** When the second date table's relationship is inactive, each measure that should react to it must test the table with ISFILTERED and, when filtered, switch that relationship on with USERELATIONSHIP. Other measures stay untouched by the table.
- Must. 2022. https://www.sqlbi.com/articles/using-cross-highlight-with-order-and-delivery-dates-in-power-bi/
- When: A shared Date table plus a second date table related inactively to the fact.
