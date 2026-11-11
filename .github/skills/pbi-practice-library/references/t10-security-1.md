# Security

Part 1 of 1 of this topic. Covers: Dynamic security, relationships and testing; Role filter performance; Totals under row-level security; Object-level security and active roles.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### Dynamic security, relationships and testing

**T10-A069-1.** Never imitate a security role by wrapping a query in an outer CALCULATETABLE. Real role filters are enforced inside the storage engine, so even ALL over a secured table cannot bring back the rows the role hides.
- Must. 2016. https://www.sqlbi.com/articles/security-cost-in-analysis-services-tabular/
- When: Trying to reproduce in a query what a security role would show.

**T10-A297-5.** If only one role of a role-playing dimension must be restricted, for example order date but not delivery date, never put the security filter on the shared dimension: it restricts the whole dimension, and so hides data for every role it plays.
- Must. 2024. https://www.sqlbi.com/articles/dax-limitations-with-inactive-relationships-and-row-level-security-rls/
- When: Security targets one of several relationships between a dimension and a fact table.

**T10-A297-7.** Browsing the report as a chosen user with View as can also bring out errors that measures raise only when security is applied, besides showing what that user sees.
- Option. 2024. https://www.sqlbi.com/articles/dax-limitations-with-inactive-relationships-and-row-level-security-rls/
- When: A model has row-level security roles, including dynamic roles that filter by the signed-in user.

### Role filter performance

**T10-A069-2.** To learn whether a role filter runs as an embedded filter expression or as a cached bitmap index, read the xmSQL generated for the query. The usual pattern of filter complexity and table size is not enough, because the heuristic is undocumented.
- Should. Check. 2016. https://www.sqlbi.com/articles/security-cost-in-analysis-services-tabular/
- When: Analysing query performance in a model with security roles.
- Version: When written, DAX Studio could not trace queries run under a role; the choice may change.

**T10-A069-3.** When a model with security roles is slow, measure first and find the bottleneck of that particular model before choosing a fix: different cases can need different approaches.
- Must. Check. 2016. https://www.sqlbi.com/articles/security-cost-in-analysis-services-tabular/
- When: A performance problem appears while security roles are in use.
- Version: When written, DAX Studio could not trace queries run with a role applied.

**T10-A069-6.** A role filter that ends up filtering a large fact table, whether defined on it or arriving through a relationship, must stay very simple: it becomes an extra filter in the storage engine query, where an embedded filter expression can use the storage engine cache.
- Must. 2016. https://www.sqlbi.com/articles/security-cost-in-analysis-services-tabular/
- When: Role filters reach a large fact table, directly or from a related table.

**T10-A069-7.** When a role filters a large fact table, confirm that the resulting storage engine query holds no CallbackDataID. A callback keeps the result out of the storage engine cache, which removes the benefit of the embedded filter expression.
- Must. Check. 2016. https://www.sqlbi.com/articles/security-cost-in-analysis-services-tabular/
- When: A security role places a filter on a large fact table.
- Version: A currency column compared with a constant caused a callback in SSAS 2012 and 2014, not from SSAS 2016 on.

**T10-A069-8.** Weigh carefully how many dimension tables get a security filter. Filters on many dimensions always add several joins with the fact table, even to very simple queries.
- Consider. 2016. https://www.sqlbi.com/articles/security-cost-in-analysis-services-tabular/
- When: Designing security roles.

**T10-A069-9.** Before a large model goes to production, test its performance with the security roles applied: the constraints that security filters bring can affect optimisations made during development.
- Should. Check. 2016. https://www.sqlbi.com/articles/security-cost-in-analysis-services-tabular/
- When: A large model that uses security roles is about to be released.
- Version: When written, DAX Studio could not trace queries run with a role applied.

### Totals under row-level security

**T10-A090-3.** When several fact tables share dimension tables, as a hidden pre-aggregated table for non-visual totals does with the original fact table, relate each fact table to the shared dimensions in a single direction, not with both-direction filters.
- Should. 2016. https://www.sqlbi.com/articles/implement-non-visual-totals-with-power-bi-security-roles/
- When: Several fact tables share dimensions, including a hidden table added for non-visual totals.

### Object-level security and active roles

**T10-A279-8.** Data security should rest on the security roles alone. No part of it should be handled in the report layer, even when reports are customised by the user's active roles.
- Should. 2023. https://www.sqlbi.com/articles/reading-active-power-bi-security-roles-in-dax/
- When: Reports are customised according to the active security roles of the user.

## Special-case techniques and facts

### Dynamic security, relationships and testing

**T10-A282-1.** One option for security by hierarchy node: keep a small user-to-node table and derive a calculated table of every node below each assigned node, so the role filter needs no string search. Match full-path identifiers by their start with LEFT; PATHCONTAINS suits unique names.
- Option. 2023. https://www.sqlbi.com/articles/managing-hierarchical-organizations-in-power-bi-security-roles/
- When: Dynamic security on an organization hierarchy stored in level columns, with access kept in a configuration table.

**T10-A282-2.** Between an expanded permissions table and the organization table it secures, neither side is unique, and Power BI proposes a both-direction filter by default. Do not accept it: the filter must run one way only, from permissions to organization.
- Must. 2023. https://www.sqlbi.com/articles/managing-hierarchical-organizations-in-power-bi-security-roles/
- When: A relationship of many-to-many cardinality links the expanded permissions table to the secured organization table.

**T10-A282-3.** One way to define a hierarchy-based dynamic role: a plain equality between the user column of the expanded permissions table and the signed-in user, with the single-direction relationship carrying the filter to the organization table. Minimal DAX there keeps formula-engine work and materialization low.
- Option. Check. 2023. https://www.sqlbi.com/articles/managing-hierarchical-organizations-in-power-bi-security-roles/
- When: An expanded permissions table holding user and visible node already exists.

**T10-A282-4.** When node names in an organization hierarchy can repeat, the security configuration must identify each node by its full path from the top of the hierarchy, never by name alone: two managers can share a name.
- Must. 2023. https://www.sqlbi.com/articles/managing-hierarchical-organizations-in-power-bi-security-roles/
- When: Dynamic security is granted per hierarchy node and duplicate node names are possible.

**T10-A282-5.** Every entry of a hierarchy-based security configuration table must equal, character by character, the path of an existing node of the organization table. A mistyped path leaves that node not enabled, and security does not behave as intended.
- Must. 2023. https://www.sqlbi.com/articles/managing-hierarchical-organizations-in-power-bi-security-roles/
- When: A configuration table assigns hierarchy nodes to users for dynamic security.

**T10-A282-6.** To find mistyped node paths, a report can list the user and assigned-node columns of the expanded permissions table, filtered to rows whose expanded node column is blank.
- Option. 2023. https://www.sqlbi.com/articles/managing-hierarchical-organizations-in-power-bi-security-roles/
- When: Hierarchy-based dynamic security uses an expanded permissions calculated table built from a configuration table.

**T10-A297-1.** USERELATIONSHIP cannot override a relationship that carries a row-level security filter, also when security reaches the table only through a chain of relationships. The engine enforces this to avoid security holes: the query fails, nothing bypasses it, and the error names USERELATIONSHIP and CROSSFILTER.
- Fact. 2024. https://www.sqlbi.com/articles/dax-limitations-with-inactive-relationships-and-row-level-security-rls/
- When: A measure activates an inactive relationship of a dimension whose active relationship carries a security filter.

**T10-A297-2.** When row-level security blocks USERELATIONSHIP, a measure can instead apply the dimension's current values to the fact column of the inactive relationship with TREATAS over VALUES of the dimension key, or move the filter between the tables some other way.
- Option. 2024. https://www.sqlbi.com/articles/dax-limitations-with-inactive-relationships-and-row-level-security-rls/
- When: The active relationship of a dimension transfers a security filter; the result needs checking against the security intent.

**T10-A297-3.** When TREATAS stands in for an inactive relationship while the active one still exists, also remove the filter on that dimension in the same CALCULATE, for example with ALL on the dimension table. Otherwise the active relationship keeps filtering the wrong fact column.
- Must. 2024. https://www.sqlbi.com/articles/dax-limitations-with-inactive-relationships-and-row-level-security-rls/
- When: A measure emulates an inactive relationship with TREATAS between tables that also share an active relationship.

**T10-A297-4.** After TREATAS replaces a USERELATIONSHIP call that row-level security blocked, verify that results still respect the intended security semantics: the workaround can hide values that should be shown, and the original error can point to worse problems such as disclosure of secured data.
- Must. 2024. https://www.sqlbi.com/articles/dax-limitations-with-inactive-relationships-and-row-level-security-rls/
- When: Any measure that moves a filter with TREATAS in place of a blocked inactive relationship.

### Role filter performance

**T10-A069-4.** When a role applies a very complex filter to a large dimension table, one option is snowflaking: move the security filter to a smaller table. Above the bitmap index row limit no cached bitmap index is used, so the expression runs in every query.
- Option. 2016. https://www.sqlbi.com/articles/security-cost-in-analysis-services-tabular/
- When: A very complex role filter sits on a dimension with more rows than the bitmap index limit.
- Version: Bitmap index row limit: 131,072 rows; 524,288 in the Power BI Service from June 2026.

**T10-A069-5.** On a dimension table above the bitmap index row limit, simplifying a very complex role filter is one possible fix: such a table never gets a cached bitmap index, so the expression is evaluated again in every query.
- Option. 2016. https://www.sqlbi.com/articles/security-cost-in-analysis-services-tabular/
- When: A very complex role filter sits on a dimension with more rows than the bitmap index limit.
- Version: Bitmap index row limit: 131,072 rows; 524,288 in the Power BI Service from June 2026.

**T10-A069-10.** Role filters are not worked out once when a user connects. Starting with the first query, the engine adds them to each storage engine query that touches a table they filter, either directly or through relationships.
- Fact. 2016. https://www.sqlbi.com/articles/security-cost-in-analysis-services-tabular/
- When: A model has active security roles.
- Version: Stated for every version of Power BI and Analysis Services.

**T10-A069-11.** From observation, a complex role filter on a table below the bitmap index row limit becomes a cached bitmap index, evaluated once per row per session; a simple filter, or a larger table, gives an embedded filter expression. Greater-than is already complex, equality simple.
- Fact. 2016. https://www.sqlbi.com/articles/security-cost-in-analysis-services-tabular/
- When: Predicting how a role filter will perform; the heuristic is undocumented and can differ.
- Version: Limit 131,072 rows; 524,288 in the Power BI Service from June 2026. Behaviour may change.

### Totals under row-level security

**T10-A090-2.** The hidden pre-aggregated table that supplies non-visual totals can be a calculated table: it is built at refresh time, so it can read every row of the fact table.
- Option. 2016. https://www.sqlbi.com/articles/implement-non-visual-totals-with-power-bi-security-roles/
- When: Implementing non-visual totals in a model with security roles.
- Version: Said to work in Power BI and in any version of Analysis Services Tabular.

**T10-A090-4.** One approach to non-visual totals: rename each original measure as an internal one and expose a new measure that returns the internal measure when ISCROSSFILTERED reports the secured table as cross-filtered, and otherwise sums the hidden pre-aggregated table.
- Option. 2016. https://www.sqlbi.com/articles/implement-non-visual-totals-with-power-bi-security-roles/
- When: Non-visual totals built on a hidden pre-aggregated table under security roles.

**T10-A288-1.** ALL on a dimension secured by row-level security clears every filter on it except the security filter, which DAX cannot remove. A percentage whose denominator uses ALL on that dimension is therefore computed only over rows the user may see.
- Fact. 2023. https://www.sqlbi.com/articles/computing-accurate-percentages-with-row-level-security-in-power-bi/
- When: Percentage-of-total measures with roles on a dimension; sometimes a share of visible data is what is wanted.

**T10-A288-2.** Security roles give visual totals only: once a dimension is secured, its filter reaches the fact table and totals over hidden rows cannot be computed from it. The separate unsecured table must hold values aggregated without the entity the roles filter.
- Must. 2016. https://www.sqlbi.com/articles/implement-non-visual-totals-with-power-bi-security-roles/ ; https://www.sqlbi.com/articles/computing-accurate-percentages-with-row-level-security-in-power-bi/
- When: Some users must not see detail rows, yet totals must include those rows.
- Version: Tabular and Power BI roles give visual totals only; SSAS Multidimensional would default to non-visual totals.

**T10-A288-3.** Avoid storing the unsecured grand total as a one-row calculated table: no dimension of the model can slice such a table, which makes it too rigid and of very little use.
- Should. 2023. https://www.sqlbi.com/articles/computing-accurate-percentages-with-row-level-security-in-power-bi/
- When: Providing totals that ignore row-level security on a dimension.

**T10-A288-4.** Build the unsecured table as a calculated table that summarizes the fact table by the keys of the dimensions without security, omitting the secured dimension's key. Relate it to those dimensions only and use it as the denominator, which then still reacts to report filters.
- Should. 2023. https://www.sqlbi.com/articles/computing-accurate-percentages-with-row-level-security-in-power-bi/
- When: Percentages must compare visible values with totals that include rows hidden on one secured dimension.

**T10-A288-5.** Before exposing non-visual totals, weigh carefully what they reveal. Hiding the unsecured summary table does not stop users from connecting to the model and querying all its content, and a correct percentage indirectly discloses the total.
- Consider. 2023. https://www.sqlbi.com/articles/computing-accurate-percentages-with-row-level-security-in-power-bi/
- When: A model adds an unsecured summary table for non-visual totals beside row-level security.

**T10-A288-6.** To slice unsecured totals by some attributes of a secured dimension, one approach: a separate dimension of only those attributes plus a generated key. Add its key to the fact table as a calculated column, carry it into the summary table, and relate the two.
- Option. 2023. https://www.sqlbi.com/articles/computing-accurate-percentages-with-row-level-security-in-power-bi/
- When: Non-visual totals need slicing by some attributes of the secured dimension while its other attributes stay hidden.

**T10-A288-7.** Reports that slice non-visual totals by attributes of a secured dimension must take those attributes from the separate attribute dimension, never from the secured one: only the attribute dimension filters the unsecured summary table.
- Must. 2023. https://www.sqlbi.com/articles/computing-accurate-percentages-with-row-level-security-in-power-bi/
- When: Users under row-level security see non-visual total measures together with attributes of the secured dimension.

**T10-A288-8.** Treat non-visual totals as advanced calculations and plan extensive training and communication. The total behind a ratio is not shown in the report, so users may find the numbers hard to read and decide they are wrong.
- Should. 2023. https://www.sqlbi.com/articles/computing-accurate-percentages-with-row-level-security-in-power-bi/
- When: Reports show percentages or totals computed against data hidden by row-level security.

### Object-level security and active roles

**T10-A253-1.** To hide one measure from some users while its tables and columns stay visible, one way is to reference a dedicated empty table in an unused variable of the measure and hide that table with object-level security. Execution plan and performance do not change.
- Option. Check. 2022. https://www.sqlbi.com/articles/hiding-measures-by-using-object-level-security-in-power-bi/
- When: Some users must not see a measure, while every existing table and column stays visible to them.
- Version: Written in 2022, when Power BI Desktop set only row filters and object permissions needed an external tool.

**T10-A253-2.** An empty table that exists only so that measures can reference it for object-level security should be made invisible to users.
- Should. Check. 2022. https://www.sqlbi.com/articles/hiding-measures-by-using-object-level-security-in-power-bi/
- When: An empty helper table was added to hide measures through object-level security.

**T10-A253-3.** The empty table that measures reference for object-level security can be a calculated table whose expression returns no rows, for example FILTER over a table with a condition that is always FALSE.
- Option. Check. 2022. https://www.sqlbi.com/articles/hiding-measures-by-using-object-level-security-in-power-bi/
- When: Creating the empty table used to hide measures through object-level security.

**T10-A253-4.** When several sensitive measures all depend on one base measure, the reference to the secured empty table can go in the base measure only: measures that depend on a hidden measure are hidden too.
- Option. Check. 2022. https://www.sqlbi.com/articles/hiding-measures-by-using-object-level-security-in-power-bi/
- When: Hiding a group of related measures with an empty table under object-level security.

**T10-A253-5.** The empty-table technique can also hide KPIs: make the KPI target expression depend on the hidden empty table that is secured for the restricted role. A status expression that uses the target then becomes unavailable to that role as well.
- Option. Check. 2022. https://www.sqlbi.com/articles/hiding-measures-by-using-object-level-security-in-power-bi/
- When: Some users must not see the goal or status KPI of a measure.

**T10-A253-6.** Object-level security cannot name a measure directly. A measure that refers, directly or indirectly, to a table or column hidden from the current user becomes invisible as well, so the hidden content cannot be inferred from measure results.
- Fact. Check. 2022. https://www.sqlbi.com/articles/hiding-measures-by-using-object-level-security-in-power-bi/
- When: Object-level security is applied to tables or columns that measures use.

**T10-A279-1.** To read the current user's active security roles in DAX, one approach is a hidden table with no relationships and one row per role name; the row filter of each role keeps only the row that equals its own name.
- Option. 2023. https://www.sqlbi.com/articles/reading-active-power-bi-security-roles-in-dax/
- When: DAX logic must react to the active roles; the table can be calculated or imported.
- Version: As of 2023, Power BI had functions for the user name but none that returned the active roles.

**T10-A279-2.** The role-name table can hold one extra value whose name matches no security role. No role filter keeps it, so it is visible only when no role applies, which tells DAX the user is an administrator.
- Option. 2023. https://www.sqlbi.com/articles/reading-active-power-bi-security-roles-in-dax/
- When: A disconnected role-name table is used and reports must tell administrators apart.

**T10-A279-3.** To show which security roles are active, use a measure that lists every visible role name with CONCATENATEX, not one that reads a single value with SELECTEDVALUE: the single-value measure returns blank for a user with more than one active role.
- Should. 2023. https://www.sqlbi.com/articles/reading-active-power-bi-security-roles-in-dax/
- When: Showing active roles from a disconnected role-name table; SELECTEDVALUE is acceptable only with one role per user.

**T10-A279-4.** Where possible, test whether one particular role is active with its own check, such as the role name IN VALUES of the role-name column, and do not work from the full list of active roles: a user can belong to many roles.
- Should. 2023. https://www.sqlbi.com/articles/reading-active-power-bi-security-roles-in-dax/
- When: DAX logic depends on whether the current user belongs to a given role.

**T10-A279-5.** Never test whether a role is active by running CONTAINSSTRING over a measure that concatenates the active role names: the search can be slow, and inaccurate when role names resemble each other.
- Must. 2023. https://www.sqlbi.com/articles/reading-active-power-bi-security-roles-in-dax/
- When: Testing role membership through a disconnected role-name table.

**T10-A279-6.** Measures and calculation groups that must behave differently by security role should build their logic on the per-role test measures: one true-or-false measure for each role.
- Should. 2023. https://www.sqlbi.com/articles/reading-active-power-bi-security-roles-in-dax/
- When: Measures or calculation groups must test for the presence of security roles.

**T10-A279-7.** A measure can raise an error, with ERROR inside IF, when the administrator value of the role-name table is visible, so a security test run as the wrong user fails with a clear message.
- Option. 2023. https://www.sqlbi.com/articles/reading-active-power-bi-security-roles-in-dax/
- When: Validating security roles when a measure must be checked only with security applied.
