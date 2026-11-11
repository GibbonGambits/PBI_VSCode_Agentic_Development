# DAX performance and optimization

Part 2 of 3 of this topic. Covers: Model design, relationships and memory; Server, processing and hardware; Report visuals and Excel clients.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### Model design, relationships and memory

**T07-W378-4.** Before committing to an in-memory Tabular model, analyse the current and expected data size and forecast the memory the model will need over time: the whole database must fit in RAM, and a server's memory is hard to enlarge after a wrong first estimate.
- Should. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Any in-memory Tabular model, above all when the final data set will be very large.

**T07-W378-5.** Estimate the memory a Tabular model needs by loading test data and measuring, not with a formula: compression makes physical size differ too much from logical size. One way is to measure at several growing row counts and draw a growth curve.
- Should. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Sizing the memory of a Tabular model.

**T07-W378-6.** To improve compression, besides cutting the number of distinct values in columns, look for the sort order that compresses best, and expect to get there by trial and error: memory size depends heavily on the compression ratio achieved.
- Consider. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Reducing the memory size of a Tabular model.

**T07-W378-11.** When tuning query speed, consider whether parts of the calculation can be computed in advance during ETL: work done before the query runs makes the query faster.
- Consider. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Tuning the query speed of a Tabular model.

**T07-W378-38.** Design and review the security of a Tabular model with the specific security features of Tabular in mind: its security layer is somewhat less powerful than the Multidimensional one.
- Must. Check. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: A solution with security requirements is built on Tabular.
- Version: Described for Analysis Services Tabular in SQL Server 2012 and 2014.

**T07-A061-2.** Check the memory size of each relationship structure, for example on the Relationships page of VertiPaq Analyzer, and treat it as a concern once it exceeds the CPU cache: the engine reads these structures often, and RAM access can then hurt queries severely.
- Should. Check. 2015. https://www.sqlbi.com/articles/costs-of-relationships-in-dax/
- When: Any model with relationships; no absolute limit exists, it depends on hardware and concurrent activity.

**T07-A061-3.** Determine the cardinality of every column that takes part in a relationship: the memory size of the relationship structure grows directly with it.
- Should. 2015. https://www.sqlbi.com/articles/costs-of-relationships-in-dax/
- When: Reviewing the relationships of a model for query performance.

**T07-A061-4.** Try to avoid relationships whose lookup table on the one side holds more than 5 to 10 million rows: VertiPaq scans very large tables well, but suffers more from the cardinality of a relationship column.
- Should. Check. 2015. https://www.sqlbi.com/articles/costs-of-relationships-in-dax/
- When: Relationships to lookup tables above roughly 5 to 10 million rows.
- Version: Row figures date from 2015.

**T07-A061-6.** Watch closely the performance of relationships whose lookup table has between 200,000 and 5,000,000 rows. If it degrades on the hardware in use, consider denormalizing, or moving low-cardinality columns into a smaller separate table.
- Consider. Check. 2015. https://www.sqlbi.com/articles/costs-of-relationships-in-dax/
- When: Relationships to lookup tables of 200,000 to 5,000,000 rows.
- Version: Row figures date from 2015.

**T07-A061-8.** A star schema is also the design suggested for the VertiPaq engine: in one example, denormalizing a header and detail pair of tables into a star saved 61% of query time. Dimensions above about 1 to 2 million rows can still become a bottleneck.
- Should. 2015. https://www.sqlbi.com/articles/costs-of-relationships-in-dax/
- When: Models queried through the VertiPaq engine.

**T07-A350-2.** Avoid many-to-many cardinality relationships on keys with millions of distinct values. On keys with few distinct values, ideally thousands or fewer, they can be acceptable: the cost of a relationship follows the number of unique values in the key column.
- Should. 2026. https://www.sqlbi.com/articles/analyzing-the-performance-of-limited-and-regular-relationships/
- When: Deciding whether a many-to-many cardinality relationship is acceptable for a given key column.

**T07-A350-5.** Keep in mind that the cost of crossing a relationship depends strongly on how many rows the table on its one side holds. A slow relationship slows every measure that crosses it; grouping by a smaller one-side table ran faster in one test.
- Consider. 2026. https://www.sqlbi.com/articles/analyzing-the-performance-of-limited-and-regular-relationships/
- When: Evaluating the cost of a relationship that queries group or filter through.

### Server, processing and hardware

**T07-W378-23.** Design the model so that no query needs more than a few seconds, and compute the answer of a slow but valuable query earlier, in ETL. Long queries hold up the lock that commits processed data, which slows the refresh and every other query.
- Should. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Fast or frequent processing is required; some long what-if queries will always remain.

**T07-W378-24.** Set a timeout in Analysis Services after which the waiting processing lock is granted and any query still running is cancelled. Ad hoc queries cannot be predicted, and the timeout stops one long query from degrading the server for everyone.
- Should. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Users run ad hoc queries, for example from Excel, while the model is being processed.
- Version: Described for Analysis Services Tabular in SQL Server 2012 and 2014.

**T07-W378-25.** When choosing hardware for a Tabular server, weigh CPU clock speed (fast cores matter more than many cores), CPU cache size per core (larger is better, the engine relies on it) and RAM speed (data outside the CPU cache is read from RAM).
- Consider. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Selecting or sizing hardware for an Analysis Services Tabular instance.
- Version: Described for Analysis Services Tabular in SQL Server 2012 and 2014.

**T07-W378-26.** Consider fast workstation-class machines for a Tabular server: maximum throughput and CPU cache nearly always matter most for this engine, and in one test workstation blades ran up to twice as fast as server-class blades.
- Consider. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Selecting hardware for an Analysis Services Tabular instance, provided the machine can handle the capacity.
- Version: Described for Analysis Services Tabular in SQL Server 2012 and 2014.

### Report visuals and Excel clients

**T07-W378-36.** For fixed, predefined reports you can write the report queries directly in DAX and tune them by hand: such queries performed very well and gave control over each query plan and over the load.
- Option. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Static Reporting Services reports, not ad hoc exploration where users generate their own queries.

**T07-A156-3.** If Performance Analyzer shows a long Visual display time, which is the time spent drawing the visual, weigh reducing the data it shows, such as fewer points in a chart or map, or swapping it for a different visual.
- Consider. 2019. https://www.sqlbi.com/articles/introducing-the-power-bi-performance-analyzer/
- When: A visual whose Visual display duration in Performance Analyzer is large.
- Version: Performance Analyzer exists in Power BI Desktop since May 2019.

**T07-A179-3.** To make an Excel report built on a PivotTable faster, consider optimizing the performance of the measures that the PivotTable uses.
- Consider. 2020. https://www.sqlbi.com/articles/why-reports-obtained-with-analyze-in-excel-can-be-slower/
- When: Excel reports based on a PivotTable.

**T07-A179-4.** To speed up an Excel PivotTable report, consider keeping CallbackDataID out of its measures, above all those referenced several times in the report: a storage engine query with a CallbackDataID skips the storage engine cache. An IF inside an iterator can produce one.
- Consider. 2020. https://www.sqlbi.com/articles/why-reports-obtained-with-analyze-in-excel-can-be-slower/
- When: Excel reports based on a PivotTable, mostly measures used many times in one report.

**T07-A195-1.** Each visual that shows data sends one or more DAX queries, which adds waiting time and server load, more so with concurrent users, and the parallelism Power BI applies to visuals is limited. Only the active page's visuals are queried and rendered.
- Should. 2020. https://www.sqlbi.com/articles/optimizing-card-visuals-in-slow-power-bi-reports/
- When: Counted per page: visuals on other pages do not affect the active one.

## Special-case techniques and facts

### Model design, relationships and memory

**T07-W378-2.** For UTC data read in local time zones: date and time filters must allow for zone and daylight saving time; values must be converted to the requested zone, in the model if users query from plain Excel PivotTables; time intelligence must adjust for daylight saving.
- Must. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Date and time values are stored in UTC and reports are requested in other time zones.

**T07-W378-3.** In a large model, do not add a pair of local date and time columns per time zone: about 40 zones would mean at least 80 columns. Convert at calculation time, in the model or the data warehouse, for the zone the user asks for.
- Should. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Reports must work in any time zone and the fact table is large; the query-time approach adds complexity.

**T07-W378-7.** In a Tabular model a small number of columns, usually those with the most distinct values, often account for most of the memory used.
- Fact. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Analysing where a Tabular model spends its memory.

**T07-W378-8.** Column memory depends on the different values within each segment, not only on the total of distinct values: the dictionary is table-wide, but each segment uses just the bits its own values need. Rarely changing columns compress far better than a time column.
- Fact. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Estimating or reducing the memory footprint of single columns.

**T07-W378-14.** Prefer smaller databases. When every query selects one tenant or business unit, a database per unit can speed queries up: one test ran 20 times slower on 20 GB than on 1 GB. Processing locks on a shared instance do not ease; they worsen slightly.
- Should. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Each query always targets one tenant or business unit; the size effect varies with the query.

**T07-W378-15.** A static Boolean condition over several columns of different tables, used as a CALCULATE filter, can be evaluated once in ETL as a true/false column of the fact table and filtered there. A calculated column would add processing time and model size.
- Option. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: The condition does not depend on the query and is costly to compute while the query runs.

**T07-W378-16.** For a small dimension, such as one holding only a code and a description, weigh dropping it and copying the description into the fact table to save a join. Test it first: denormalizing is not always faster, and filtering the dimension was sometimes much faster.
- Consider. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: A dimension with very few columns; the outcome depends on table sizes and compression.

**T07-A061-5.** When the lookup table on the one side of a relationship is large, consider denormalizing it into the many-side table, or moving its often-queried low-cardinality columns into a separate table with fewer rows. In one header and detail example, merging saved 61% of query time.
- Consider. Check. 2015. https://www.sqlbi.com/articles/costs-of-relationships-in-dax/
- When: Lookup tables above 5 to 10 million rows, or 200,000 to 5 million when performance degrades.
- Version: Row figures date from 2015.

**T07-A061-7.** In a star schema, large dimensions become a bottleneck: a dimension counts as large above 1 to 2 million rows, a hardware-dependent warning range runs from 500,000 to 2,000,000 rows, and above 10 million rows performance problems are certain.
- Fact. Check. 2015. https://www.sqlbi.com/articles/costs-of-relationships-in-dax/
- When: Star schema models with large dimension tables.
- Version: Row figures date from 2015.

**T07-A350-6.** A many-to-many cardinality relationship is always a limited relationship: the storage engine cannot resolve it in one query and needs a batch. In one test crossing it cost almost 20 times a regular relationship, on every scan, adding up across a report's measures.
- Fact. 2026. https://www.sqlbi.com/articles/analyzing-the-performance-of-limited-and-regular-relationships/
- When: Queries grouping a fact table by columns reached through a many-to-many cardinality relationship.

**T07-A350-7.** With a many-to-many cardinality relationship, the fusion optimization is off for measures that filter the related table on different values: each needs its own storage engine batch, because the storage engine cannot take such relationships as simple joins.
- Fact. 2026. https://www.sqlbi.com/articles/analyzing-the-performance-of-limited-and-regular-relationships/
- When: Several measures each filtering a different value of a column reached through such a relationship.

### Server, processing and hardware

**T07-W378-17.** Partitions do not make queries on a Tabular model faster: every query scans all partitions, so they serve data management only. That leaves more freedom in choosing the partitioning key than in Multidimensional, where date partitions help queries.
- Fact. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Designing a partitioning scheme for an in-memory Tabular model.

**T07-W378-18.** Use partitions to make refresh predictable: when rows keep changing until their item is closed, keep open items in their own small partition and partition closed items by closing date, not start date. Each refresh then reprocesses only the current-day partition and the open-items partition.
- Should. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Near real-time refresh of data whose rows stay incomplete until a closing event.

**T07-W378-19.** One way to handle rows that arrive incomplete is daily partitions with a full reprocess of each one after its day is over, which picks up the final state. It fails when items stay open for weeks while data is reprocessed every few minutes.
- Option. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Rows loaded during the day may belong to items that are not yet complete.

**T07-W378-20.** Reprocessing even one partition clears the whole cache of an Analysis Services database, so queries run slower until the cache is rebuilt. The effect is described as small and short-lived.
- Fact. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Frequent, near real-time processing of a Tabular database.
- Version: Described for Analysis Services Tabular in SQL Server 2012 and 2014.

**T07-W378-21.** When Analysis Services finishes processing it needs a lock to switch in the new data. While that lock waits for running queries to end, new queries are queued: one long query delays the refresh and every other user, and a burst of queued queries follows.
- Fact. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Processing runs while users are querying the server.
- Version: Described for Analysis Services Tabular in SQL Server 2012 and 2014.

**T07-W378-22.** The lock Analysis Services takes to commit processed data covers the whole instance: processing one database blocks queries on all databases of that instance. Splitting a model into several databases makes this locking slightly worse, not better.
- Fact. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Several databases share one Analysis Services instance and are processed often.
- Version: Described for Analysis Services Tabular in SQL Server 2012 and 2014.

**T07-W378-28.** On NUMA hardware, run each Tabular instance in a Hyper-V virtual machine bound to one NUMA node: the engine is not NUMA-aware but runs well inside one node, with no memory settings to change. Under load, one such instance degraded past about 370 concurrent users.
- Should. Check. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Tabular instances on NUMA servers.
- Version: From 2014; Windows System Resource Manager, the other way to set affinity, was already deprecated.

**T07-W378-29.** When an Analysis Services instance is tied to one NUMA node by process affinity, not by a virtual machine, lower its memory limits, such as TotalMemoryLimit and LowMemoryLimit in msmdsrv.ini, to fit that node: the defaults are percentages of the whole machine's RAM.
- Must. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Affinity is set on the process, for example with WSRM or a start parameter.
- Version: Described for Analysis Services Tabular in SQL Server 2012 and 2014.

**T07-W378-30.** Outside testing, do not rely on starting Analysis Services with the affinity start parameter to bind it to a NUMA node: it is a workaround that needs the user who started the service to stay logged on.
- Should. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Binding an Analysis Services instance to a NUMA node.
- Version: Described for Analysis Services Tabular in SQL Server 2012 and 2014.

**T07-W378-31.** Before configuring Tabular on a NUMA machine, find out its layout, for example with the Coreinfo utility: which processors belong to which node and what reaching memory on another node costs. Crossing nodes to reach RAM is the main factor in expected performance.
- Should. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Deploying Tabular on NUMA hardware or setting node affinity.

**T07-W378-32.** Large Azure virtual machines also expose NUMA nodes, so Tabular on them suffers the same cross-node slowdown as an on-premises server without affinity; no way to set node affinity there was found.
- Fact. Check. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Hosting Tabular on large Azure virtual machines.
- Version: Reported in 2014 for an Azure A7 machine with Analysis Services 2012 Tabular; expected to improve.

**T07-W378-41.** When a Windows System Resource Manager policy assigns the processors of one NUMA node to an Analysis Services instance, number the processors from zero: with 16 per node, the first node is 0 to 15, not 1 to 16.
- Must. Check. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Setting NUMA node affinity through a WSRM resource allocation policy.
- Version: WSRM was already listed as deprecated in 2014.

**T07-W378-42.** A Hyper-V virtual machine running Tabular can be kept on one NUMA node through its processor NUMA settings, sizing maximum memory and maximum NUMA nodes from one node's memory. Clearing the host option that lets machines span nodes should, in theory, work too.
- Option. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Hyper-V on a NUMA machine; the host-level option is reported as working only in theory.

**T07-W378-43.** When one Analysis Services instance can no longer serve all users, you can scale out: synchronize the database to further instances and spread requests across them with network load balancing.
- Option. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: More concurrent load than one Tabular instance can handle within its service levels.

### Report visuals and Excel clients

**T07-W378-35.** Excel PivotTables send MDX, not DAX, to a Tabular model, so hand-written DAX test queries do not represent the workload of Excel users. The queries Excel really runs can be captured with SQL Server Profiler.
- Fact. 2014. https://www.sqlbi.com/whitepapers/using-tabular-models-in-a-large-scale-commercial-solution/
- When: Building test workloads for a model that users browse with Excel.
- Version: Stated in 2014 for SQL Server 2012 and 2014: Excel then still queried Tabular in MDX.

**T07-A156-4.** Each visual on a page costs memory and CPU, and visuals are drawn one after another on a single thread: a page with dozens of visuals can take several seconds even when each is simple. A plain text box measured close to 100 milliseconds.
- Fact. 2019. https://www.sqlbi.com/articles/introducing-the-power-bi-performance-analyzer/
- When: Report pages that contain many visuals.

**T07-A179-1.** Excel PivotTables, also those made with Analyze in Excel, query the model in MDX. Such a report can run slower than an equivalent Power BI report, which queries in DAX: some optimizations made for DAX queries have no MDX counterpart.
- Fact. 2020. https://www.sqlbi.com/articles/why-reports-obtained-with-analyze-in-excel-can-be-slower/
- When: Excel reports connected to a Power BI model or an Analysis Services Tabular database.
- Version: Per a November 2020 update, still possible after the fusion optimization reached MDX queries in Power BI.

**T07-A179-5.** If an Excel PivotTable connected to Power BI still shows the slowdown of many storage engine queries caused by the missing fusion optimization, check that Power BI Desktop is an up-to-date version.
- Should. 2020. https://www.sqlbi.com/articles/why-reports-obtained-with-analyze-in-excel-can-be-slower/
- When: MDX queries still run a separate storage engine query for each measure.
- Version: October 2020: fixed in Power BI and Azure Analysis Services; SQL Server Analysis Services up to 2019 had no fix.

**T07-A179-6.** To study the query plans behind an Excel PivotTable report, you can connect Excel directly to the diagnostic port of the model open in Power BI Desktop. A report made through Analyze in Excel on the published model does not allow it.
- Option. 2020. https://www.sqlbi.com/articles/why-reports-obtained-with-analyze-in-excel-can-be-slower/
- When: Analyzing the MDX and storage engine queries an Excel report sends to a Power BI model.
- Version: DAX Studio, once connected to Power BI Desktop, displays that port.

**T07-A195-2.** A page of many separate cards that differ only by one attribute's value can become one visual repeating the measure per value: same layout, far fewer queries, an order-of-magnitude faster page in one test. That single visual renders slower than one simple card.
- Option. Check. 2020. https://www.sqlbi.com/articles/optimizing-card-visuals-in-slow-power-bi-reports/
- When: Report pages showing many card visuals that differ only by one attribute's value.
- Version: Tested in 2020 with a custom visual, before Power BI had a generic small multiples feature.
