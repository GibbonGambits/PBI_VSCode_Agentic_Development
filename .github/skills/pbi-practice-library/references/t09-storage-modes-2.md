# Storage modes

Part 2 of 2 of this topic. Covers: Choosing a storage mode; Composite models; Push datasets.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### Choosing a storage mode

**T09-W380-1.** Consider the trade-offs per model, then tune the model for the mode chosen: DirectQuery gives current data with no processing, memory limit or data copy, but loses in-memory speed and moves the query work to the database.
- Consider. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Deciding between DirectQuery and Import for a model.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-4.** Before choosing DirectQuery, check that the relational server can serve report queries while it handles its normal update workload: every query goes to the engine that receives the updates, whereas an in-memory model reads the source once.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Deciding whether a source can carry DirectQuery.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-5.** When a source table feeds an in-memory model, tune the source for one large read of the whole table during processing; indexes bring no benefit to that workload, which is a single SELECT over every row.
- Must. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Preparing source tables for import.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-6.** If a source table that feeds an in-memory model is partitioned, make its partitions match the partitions defined in the Tabular model.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Only where the source table needs partitioning.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-8.** On SQL Server, give tables that a DirectQuery model queries a columnstore index; for tables that only feed an in-memory model such an index is far from ideal. The source design has to match how the model uses it.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Choosing indexes for model source tables on SQL Server.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-9.** Before committing a project to DirectQuery, build a prototype, collect the SQL queries your DAX formulas produce and take time to understand them: knowing that workload helps you design the best relational data model.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Evaluating DirectQuery for a new project.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-30.** When only recent data must be real time, build two models: a small DirectQuery model for the last few days with simple calculations, and an in-memory model for the full history with the complex calculations.
- Should. Check. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Real-time needs cover only recent days.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-42.** Avoid enabling paging for an in-memory Tabular model.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Configuring memory for an Analysis Services in-memory model.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-43.** When an in-memory model does not fit in memory, prefer adding RAM: reducing the memory the data model uses is the harder alternative, because optimising it is a complex task.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: An Analysis Services in-memory model outgrows the memory of its server.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-W380-44.** Build solid DAX skills before adopting DirectQuery, so you can judge how each calculation behaves there: which functions a project needs, and how much data they materialise, is hard to foresee at the start.
- Should. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Planning a DirectQuery project.
- Version: Analysis Services 2016 Tabular; 2017 white paper.

**T09-A234-1.** Avoid making a whole model DirectQuery only because a handful of dashboards need real-time data: a pure DirectQuery model puts the cost of every query on the source. DirectQuery mainly fits when data cannot be imported fast enough for most reports.
- Should. Check. 2021. https://www.sqlbi.com/articles/creating-real-time-dashboards-in-power-bi-with-push-datasets/
- When: Everything else in the model could be imported.

### Composite models

**T09-A212-1.** Avoid architectures in which a composite model federates tens of data sources into one virtual semantic model on top of smaller models, and approach new architectures built on composite models with caution.
- Should. Check. 2020. https://www.sqlbi.com/articles/new-composite-models-in-power-bi-a-milestone-in-business-intelligence/
- When: Designing solutions on composite models over published models and Analysis Services.
- Version: Written in December 2020, when this composite model feature was still a preview in Power BI Desktop.

**T09-A237-5.** To see whether a visual of a composite model runs wholesale, you can capture its query with Performance Analyzer; that is only the local query, which is turned into a separate DAX query for the remote server and can be run there by hand.
- Option. 2021. https://www.sqlbi.com/articles/introducing-wholesale-and-retail-execution-in-composite-models/
- When: Composite models connected to a remote model.

**T09-A238-4.** Consider that wholesale or retail execution is chosen per sub-expression: a measure that mixes both gets remote calculation items applied to only part of its code, giving mixed results that are very hard to debug.
- Consider. Check. 2022. https://www.sqlbi.com/articles/understanding-the-interactions-between-composite-models-and-calculation-groups/
- When: The remote model of a composite model defines calculation groups.
- Version: Described in 2022; check current behaviour.

**T09-A238-6.** When calculation groups are part of the design of a published model, it is best to stop others from building composite models on it: retail sub-queries skip a remote calculation group, so results can mix two kinds of calculation.
- Should. 2022. https://www.sqlbi.com/articles/understanding-the-interactions-between-composite-models-and-calculation-groups/
- When: Published models with calculation groups; skilled DAX developers could cope, but prohibiting is safer.

**T09-A239-1.** A model that might later be extended through composite models must have its DAX reviewed with extra care, chiefly how calculation groups are handled and how ALLSELECTED behaves: both act differently once the model is the remote part.
- Must. 2022. https://www.sqlbi.com/articles/using-allselected-in-composite-models/
- When: Authoring a semantic model others may extend.

**T09-A239-2.** In a model expected to be extended through composite models, avoid ALLSELECTED without arguments in any DAX expression: the remote model knows nothing of the structure of the local model, so such measures can surprise and every composite report needs far more checking.
- Should. Check. 2022. https://www.sqlbi.com/articles/using-allselected-in-composite-models/
- When: Models planned as the remote model of composite models.
- Version: Described in 2022; check current behaviour.

## Special-case techniques and facts

### Choosing a storage mode

**T09-W380-3.** In one benchmark, queries took 1.5 to 2.9 times as long in DirectQuery as in memory, varying with the query and its number of joins; DirectQuery was never the faster of the two.
- Fact. Check. 2017. https://www.sqlbi.com/whitepapers/directquery-in-analysis-services-2016/
- When: Measured on a 4-billion-row fact table in a SQL Server clustered columnstore; results may differ elsewhere.
- Version: Analysis Services 2016 benchmark published in 2017.

### Composite models

**T09-A212-2.** A composite model on a published model suits a slightly different view of it (a custom grouping, an Excel budget, a link to another model) instead of an Excel export: it keeps the original measures and relationships, sees refreshed data and duplicates nothing.
- Option. Check. 2020. https://www.sqlbi.com/articles/new-composite-models-in-power-bi-a-milestone-in-business-intelligence/
- When: Users need local additions to a model already published on the service.
- Version: Written in December 2020, when this composite model feature was still a preview in Power BI Desktop.

**T09-A227-2.** In a hybrid model that keeps most tables in Import mode and a few DirectQuery tables for current data, some calculations cannot be split across the imported and the DirectQuery tables; DISTINCTCOUNT is one such case.
- Fact. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: Measures combine in-memory aggregation with results from DirectQuery tables.

**T09-A237-1.** A composite-model query is wholesale when it touches only one DirectQuery island or only the local VertiPaq part, and retail when it mixes islands or local data with an island; retail queries involve at least two DAX engines and are much harder to optimise.
- Fact. 2021. https://www.sqlbi.com/articles/introducing-wholesale-and-retail-execution-in-composite-models/
- When: Composite models that combine a remote model with local tables.

**T09-A237-2.** A calculated column on a remote table that reads a local table fails with an error: the column would have to be computed by the remote server, and the remote model has no access to local tables.
- Fact. 2021. https://www.sqlbi.com/articles/introducing-wholesale-and-retail-execution-in-composite-models/
- When: Adding columns to remote tables of a composite model.

**T09-A238-1.** A calculation group defined locally in a composite model applies to every sub-query; one defined in the remote model applies only to wholesale sub-queries and is ignored by retail ones, because the local engine cannot see remote calculation items.
- Fact. Check. 2022. https://www.sqlbi.com/articles/understanding-the-interactions-between-composite-models-and-calculation-groups/
- When: Calculation groups exist in the local or the remote model.
- Version: Described in 2022; check current behaviour.

**T09-A238-3.** A composite-model measure that combines a remote measure with a local value can iterate the local table and call the remote measure, so the remote part runs wholesale and only the final arithmetic is local, instead of iterating the remote fact table with LOOKUPVALUE.
- Option. Check. 2022. https://www.sqlbi.com/articles/understanding-the-interactions-between-composite-models-and-calculation-groups/
- When: A local table is reached through a limited relationship; complex code can still end up partly retail.
- Version: Described in 2022; check current behaviour.

**T09-A238-5.** Remote calculation groups behave without surprises only for measures sure to run wholesale, which is the case only when the composite model adds no local tables and connects to a single data island.
- Fact. Check. 2022. https://www.sqlbi.com/articles/understanding-the-interactions-between-composite-models-and-calculation-groups/
- When: A composite model built on a remote model with calculation groups.
- Version: Described in 2022; check current behaviour.

**T09-A239-3.** A remote-model measure that calls ALLSELECTED with no arguments can return wrong numbers in a composite model: when a visual groups by local-table columns, the query runs retail, the remote engine cannot restore the shadow filters, and the measure may just equal its base measure.
- Fact. Check. 2022. https://www.sqlbi.com/articles/using-allselected-in-composite-models/
- When: Rows come from a local-only table; with only the slicer on the local table results stayed correct.
- Version: Described in 2022; check current behaviour.

**T09-A239-4.** The same argument-free ALLSELECTED logic written as a measure in the local model of a composite model sees both local and remote tables, and returns the correct result where the remote version fails.
- Fact. Check. 2022. https://www.sqlbi.com/articles/using-allselected-in-composite-models/
- When: A report groups by columns of a local table.
- Version: Described in 2022; check current behaviour.

### Push datasets

**T09-A227-3.** Push dataset limits: 75 tables; 75 columns per table; 5,000,000 rows per table, or 200,000 with FIFO retention; 10,000 rows per POST; 1,000,000 rows per hour; 5 pending POST requests; 120 POST requests per minute, or per hour above 250,000 rows; strings of 4,000 characters.
- Fact. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: Designing or loading a Power BI push dataset.
- Version: Limits as stated in 2021; push semantic models are now listed as retiring: check current figures.

**T09-A227-4.** A push dataset cannot hold inactive relationships, measures that call USERELATIONSHIP, measures that refer to invalid or missing measures, hierarchies, or a table marked as a date table; a copy of a regular model may need changes to drop them.
- Fact. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: Building a push dataset from an existing Tabular model.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A227-5.** Before turning a Tabular model into a push dataset, validate it to find the objects a push dataset cannot hold. Invalid objects can stay, since only valid ones are published; user hierarchies are dropped without a warning.
- Should. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: Deriving a push dataset from a regular model.
- Version: Validation run with the Power BI Push Tools on a .bim file (2021); push models now listed as retiring.

**T09-A227-6.** A push dataset cannot contain a table called Date; one workaround is another name, such as Dates or Calendar, given inside Power BI Desktop so that every reference to the table follows the new name.
- Option. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: The date table of the source model is named Date.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A227-7.** When loading a table would break the push dataset row limits (5 million rows per table, 1 million added per hour), shrink the table, for example to the coarser grain the real-time dashboard needs, such as one row per order date and store.
- Must. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: First load of a push dataset from larger source tables; less history cuts rows further.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A227-8.** A push dataset can keep the full table list of the original model: tables the real-time reports do not need can stay empty instead of being deleted, so only the initial daily load has to be adapted.
- Option. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: The original model has no more than the push dataset maximum of 75 tables.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A227-9.** When fact rows are grouped to a coarser grain for a push dataset, quantities can be summed, but each grouped row must carry prices recomputed so that price times quantity gives the same total as the detailed data.
- Must. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: Measures of a pre-aggregated push dataset multiply unit prices or costs by quantity.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A227-10.** Grouping fact rows and rewriting price values to load a push dataset changes what those columns mean, so a measure such as an average net price returns wrong results on the grouped data.
- Fact. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: A push dataset holds pre-aggregated rows with prices recalculated for the new grain.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A227-11.** Build and test the DAX queries that fill a push dataset in DAX Studio, and check that their results are consistent.
- Should. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: Writing the DAX queries that load a push dataset from the original model.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A227-12.** When a tool loads a push dataset by matching DAX result column names to the destination, name every result column with its full table and column name, using the destination table name; a destination column missing from the query stays blank. Column order is free.
- Must. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: Loading push dataset tables from DAX queries with the Power BI Push Tools.
- Version: Behaviour of the Power BI Push Tools in 2021; push semantic models are now listed as retiring.

**T09-A227-13.** Set the report page filter correctly before pinning visuals to a real-time dashboard, even while the visuals still show blanks: a pinned tile keeps the filters of the moment of pinning, and later report filter changes do not reach it.
- Must. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: Pinning visuals of a push dataset report to a Power BI dashboard.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A227-14.** For a real-time report in production, make the page filter target the current date, for example with a relative date filter set to the current day.
- Should. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: Real-time reports and dashboards on a push dataset, set up before publishing.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A227-15.** Dashboard tiles update by themselves when a push dataset receives rows, but report pages do not; automatic page refresh is one option to make a report page show new rows without a manual refresh.
- Option. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: A report on a push dataset must show new data without user action.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A227-16.** An application that writes new data to a push dataset should batch rows into fewer POST requests, not send one row per request: the POST rows limits of the Power BI REST API make row-by-row sending impractical.
- Should. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: Writing real-time rows through the Power BI REST API.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A227-17.** Consider the cost before capturing new transactions for a push dataset with database triggers: extra load on the source works against the reason for choosing a push dataset over DirectQuery.
- Consider. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: The application producing the transactions is outside your control.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A227-18.** In production the application that generates the transactions must itself send new rows to the push dataset, through the PostRowsInGroup operation of the Power BI REST API; plan development skills and coordination with the IT team that runs the infrastructure.
- Must. Check. 2021. https://www.sqlbi.com/articles/implementing-real-time-updates-in-power-bi-using-push-datasets-instead-of-directquery/
- When: Moving a push dataset solution from simulation to production.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A234-3.** Design a push dataset within its size and throughput limits: initialise it at the start of each day with history summarised at a grain that fits, then add new data through the Power BI REST API during the day.
- Must. Check. 2021. https://www.sqlbi.com/articles/creating-real-time-dashboards-in-power-bi-with-push-datasets/
- When: Push datasets behind real-time dashboards; loading less history cuts size further.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A234-4.** A push dataset loaded with history summarised by store and date matches the original model only for queries at that grain; filtering or grouping by attributes that were aggregated away, such as product or customer, does not work.
- Fact. Check. 2021. https://www.sqlbi.com/articles/creating-real-time-dashboards-in-power-bi-with-push-datasets/
- When: History was pre-aggregated to fewer dimensions than the original model.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A234-5.** Run the push dataset initialisation first thing each morning, right after the import model it copies from has refreshed, and add the new transactions of the day afterwards.
- Should. Check. 2021. https://www.sqlbi.com/articles/creating-real-time-dashboards-in-power-bi-with-push-datasets/
- When: A push dataset initialised from a daily-refreshed import model.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A234-6.** To feed new transactions into a push dataset, prefer a developer-built service that captures them in the transactional system and sends them directly; polling the source, for example a Power Automate flow every 30 seconds, is the costlier fallback.
- Should. Check. 2021. https://www.sqlbi.com/articles/creating-real-time-dashboards-in-power-bi-with-push-datasets/
- When: Production real-time writes; the service must authenticate with the Power BI service, often the hardest part.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.

**T09-A234-7.** When the original model changes, confirm that the DAX queries that initialise the derived push dataset still work, and check whether its measure expressions need updating.
- Must. Check. 2021. https://www.sqlbi.com/articles/creating-real-time-dashboards-in-power-bi-with-push-datasets/
- When: Maintaining a push dataset derived from a regular model.
- Version: In 2021 push datasets worked alike on Pro and Premium; now listed as retiring.

**T09-A234-8.** When new transactions go into a push dataset table of more than 250,000 rows, group them so that one POST rows call goes out about every 30 seconds: such a table accepts 120 requests per hour, each carrying up to 10,000 rows.
- Must. Check. 2021. https://www.sqlbi.com/articles/creating-real-time-dashboards-in-power-bi-with-push-datasets/
- When: Real-time writes into a large push dataset table.
- Version: Written in 2021; Microsoft now lists push semantic models as retiring: check before building one.
