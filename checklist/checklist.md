# Power BI model and report checklist (79 items)

The text of every item below is the owner's checklist, word for word and in the original order.
Do not edit, reword, merge, reorder or drop anything in this file. `scripts/check_template.py` compares it with the original spreadsheet.

Each item has the four spreadsheet columns: Area, Category, Topic, Microsoft documentation.
To read one item, search for its heading, for example `## Item 23`.

## Item 1

- Area: Model
- Category: Data Sources & Query Layer (Power Query / M)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-query/power-query-query-parameters)
- Topic:

~~~text
Assess whether source connections should be parameterized for environment switching (for example: server, database, workspace, file path, URL, date boundary).
• When applicable: the same report/model must move across environments or source boundaries without code edits
• Mark N/A when: the report intentionally targets one fixed source/environment and parameterization would add complexity without a deployment benefit
• Guidance: record the connection types reviewed and whether parameters are truly needed for this report
• Quantitative threshold: 2 or more environments (for example: Dev/Test/Prod) = parameterization expected
• Quantitative threshold: 2 or more source endpoints, workspaces, databases, URLs, or file paths for the same report = parameterization expected
~~~

## Item 2

- Area: Model
- Category: Data Sources & Query Layer (Power Query / M)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-onprem)
- Topic:

~~~text
Assess whether the model avoids local file system data sources (for example: desktop file paths) unless a gateway-backed design is explicitly intended.
~~~

## Item 3

- Area: Model
- Category: Data Sources & Query Layer (Power Query / M)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/power-query-folding)
- Topic:

~~~text
Assess whether query folding is preserved where possible and whether expensive non-folding steps are pushed late.
• When applicable: the connector supports folding or source pushdown
• Mark N/A when: folding does not apply (for example: flat files, static tables, or connectors that do not support it)
• Guidance: state which steps can fold, where row/column reduction occurs, and which non-folding steps are justified
• Quantitative threshold: 0 known non-folding steps before the first major row filter or column reduction is preferred
• Quantitative threshold: 100% of easy pushdown steps (row filters, column selection, simple renames/types) should occur before any known non-folding step
~~~

## Item 4

- Area: Model
- Category: Data Sources & Query Layer (Power Query / M)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/power-query-referenced-queries)
- Topic:

~~~text
Assess whether a Staging → Reference pattern is actually warranted.
• When applicable: multiple outputs share heavy transformations, source logic is reused, or branching queries increase maintenance cost
• Mark N/A when: the query layer is small/simple and staging would add more complexity than value
• Guidance: do not fail this item just because staging tables are absent; first decide whether the report needs them
• Quantitative threshold: 2 or more downstream queries reusing the same heavy transformation = staging/reference expected
• Quantitative threshold: 2 or more branches from the same source query = staging/reference should be considered
~~~

## Item 5

- Area: Model
- Category: Data Sources & Query Layer (Power Query / M)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/import-modeling-data-reduction)
- Topic:

~~~text
Assess whether only required columns and rows are loaded, with row filters and column reduction applied as early as practical.
• When applicable: the report imports or materializes data into the model
• Guidance: note any intentionally retained helper fields or extra history that is required for the report
• Quantitative threshold: 0 clearly unused loaded columns unless justified
• Quantitative threshold: review when more than 10% of loaded columns are not used in relationships, calculations, or visuals
~~~

## Item 6

- Area: Model
- Category: Data Sources & Query Layer (Power Query / M)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-query/data-types)
- Topic:

~~~text
Assess whether data typing is controlled at the correct layer.
• When applicable: the report depends on typed values for sorting, relationships, visuals, or DAX behavior
• Mark N/A when: typing is intentionally governed upstream (for example: source/dataflow) and repeated typing in Power Query is unnecessary
• Guidance: avoid uncontrolled Any/variant behavior and document where type governance actually lives
• Quantitative threshold: 0 model-facing columns with uncontrolled Any/variant behavior unless justified
• Quantitative threshold: 100% of relationship keys, sort-by columns, date columns, and numeric measure-source columns must be explicitly typed somewhere
~~~

## Item 7

- Area: Model
- Category: Data Sources & Query Layer (Power Query / M)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization)
- Topic:

~~~text
Assess whether query, table, column, and measure names follow a consistent naming standard that fits the intended audience.
• When applicable: report authors or support staff use the semantic model directly
• Guidance: prefer descriptive business names for author-facing fields and consistent technical naming where appropriate
• Quantitative threshold: 0 duplicate visible field names in the same table
• Quantitative threshold: 0 placeholder names such as Column1, Table, or Query1 in visible author-facing fields
~~~

## Item 8

- Area: Model
- Category: Data Sources & Query Layer (Power Query / M)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-query-overview)
- Topic:

~~~text
Assess whether business rules and assumptions are documented at the layer where they are implemented.
• When applicable: the report contains non-obvious logic in source shaping, DAX, model design, or report interactions
• Mark N/A when: the report contains little or no transformation/business logic at that layer
• Guidance: document where the logic actually lives instead of forcing comments where no rule exists
• Quantitative threshold: 100% of non-obvious transformations should be documented
• Quantitative threshold: 100% of exception-handling logic should be documented
• Quantitative threshold: 1 or more manual overrides or hard-coded business rules = documentation required
~~~

## Item 9

- Area: Model
- Category: Data Sources & Query Layer (Power Query / M)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-dynamic-m-query-parameters)
- Topic:

~~~text
Assess whether parameterized filters (date ranges, environment selectors, source boundaries) are actually needed.
• When applicable: they solve a real deployment, refresh, or maintenance problem
• Mark N/A when: fixed upstream shaping is intentional and parameterization would not improve performance, deployment, or maintainability
• Guidance: do not fail this item only because parameters are absent; decide whether the report needs them first
~~~

## Item 10

- Area: Model
- Category: Model Structure & Relationships
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema)
- Topic:

~~~text
Assess whether the model follows a star-schema-friendly design where practical: fact tables for events/observations, dimensions for filtering/grouping, and snowflaking only when it clearly helps more than it hurts.
• When applicable: the report uses a semantic model with relationships and reusable fields
• Guidance: focus on whether the chosen structure improves usability and correctness for this report, not on blindly forcing a textbook pattern
• Quantitative threshold: 0 fact-to-fact relationships unless justified
• Quantitative threshold: 0 snowflake chains longer than 1 hop unless justified
~~~

## Item 11

- Area: Model
- Category: Model Structure & Relationships
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-create-and-manage-relationships)
- Topic:

~~~text
Assess whether relationship cardinality is appropriate, preferring one-to-many where the business grain supports it.
• When applicable: the report model has relationships between reusable entities
• Guidance: only flag many-to-many as an issue when it is avoidable or unjustified for the business requirement
• Quantitative threshold: 100% of one-side relationship keys must be unique
• Quantitative threshold: 0 avoidable many-to-many relationships
~~~

## Item 12

- Area: Model
- Category: Model Structure & Relationships
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/relationships-bidirectional-filtering)
- Topic:

~~~text
Assess whether relationship direction and filter propagation are correct, and whether bi-directional filtering is minimized and justified when used.
• When applicable: the report relies on model relationships for filter behavior
• Guidance: record active filter directions and why any bi-directional relationships are required
• Quantitative threshold: target 0 bi-directional relationships
• Quantitative threshold: 1 bi-directional relationship requires review; 2 or more require strong justification
~~~

## Item 13

- Area: Model
- Category: Model Structure & Relationships
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/relationships-active-inactive)
- Topic:

~~~text
Assess whether inactive relationships are needed for alternate contexts (for example: multiple date roles) and whether measures use them cleanly with USERELATIONSHIP where appropriate.
• When applicable: multiple valid filter paths exist and must be activated deliberately
• Mark N/A when: the model has only one relevant path/context
• Guidance: do not mark this incomplete simply because inactive relationships are absent
~~~

## Item 14

- Area: Model
- Category: Model Structure & Relationships
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema)
- Topic:

~~~text
Assess whether key design is appropriate for the model.
• When applicable: the report depends on dimensional joins or key-based relationships
• Mark N/A when: this concern is handled upstream or is not material to the report design
• Guidance: prefer stable unique keys and avoid fragile concatenated keys unless clearly justified
• Quantitative threshold: 0 concatenated relationship keys unless justified
• Quantitative threshold: 0 nulls on one-side relationship keys
• Quantitative threshold: many-side key null rate should be <=0.1% unless intentionally allowed
~~~

## Item 15

- Area: Model
- Category: Model Structure & Relationships
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/relationships-active-inactive)
- Topic:

~~~text
Assess whether role-playing dimensions are needed (for example: Order Date vs Ship Date).
• When applicable: the report analyzes the same business entity in multiple valid roles/contexts
• Mark N/A when: the report has only one relevant date/context path
• Guidance: separate dimension instances or alternate patterns are useful only when the business meaning actually differs
• Quantitative threshold: 2 or more distinct business date meanings = role-playing design or explicit alternate context pattern required
• Quantitative threshold: 2 or more active analytical date roles on the same fact = review required
~~~

## Item 16

- Area: Model
- Category: Model Structure & Relationships
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/composite-model-guidance)
- Topic:

~~~text
Assess whether Composite models and DirectQuery are used only when necessary, and whether the trade-offs are documented.
• When applicable: the report mixes storage modes, requires near-real-time access, or cannot reasonably import the required data
• Mark N/A when: the report is a clean import design and DirectQuery is not needed
• Guidance: mark Yes for a deliberate import design when it satisfies the requirement
• Quantitative threshold: freshness requirement <=15 minutes or near-real-time access may justify DirectQuery/composite
• Quantitative threshold: interactive visual latency target above 2 seconds in import due to size/freshness constraints = review storage mode choice
~~~

## Item 17

- Area: Model
- Category: Model Structure & Relationships
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/aggregations-advanced)
- Topic:

~~~text
Assess whether aggregations are needed for DirectQuery or very large models.
• When applicable: the report has large detail tables, repeated slow detail queries, or DirectQuery workloads that would benefit
• Mark N/A when: the model is import-only, already summarized appropriately, or too small/simple to benefit
• Guidance: do not force aggregation tables where scale does not justify them
• Quantitative threshold: fact table >=50 million rows = review aggregations
• Quantitative threshold: DirectQuery detail queries repeatedly >2 seconds = review aggregations
~~~

## Item 18

- Area: Model
- Category: Model Structure & Relationships
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/auto-date-time)
- Topic:

~~~text
Assess whether Auto Date-Time is disabled and whether a deliberate date-table strategy is used instead.
• When applicable: the report uses dates for filtering, grouping, or time intelligence
• Guidance: verify that hidden auto date tables are not creating clutter or conflicting date behavior
~~~

## Item 19

- Area: Model
- Category: Model Structure & Relationships
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization)
- Topic:

~~~text
Assess whether technical-only keys, helper columns, sort-by columns, and duplicate raw columns should be hidden from Report view.
• When applicable: the field is truly technical-only for report authors
• Guidance: do not mark this as an issue just because a field looks technical; if authors genuinely need it for visuals, export, drillthrough, reconciliation, or troubleshooting, keeping it visible can be correct
• Quantitative threshold: 100% of visible technical-looking fields must have a valid use case (visual, export, drillthrough, reconciliation, or troubleshooting)
• Quantitative threshold: review when 1 or more visible technical-only fields have no real author/support use case
~~~

## Item 20

- Area: Model
- Category: Performance & Load
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization)
- Topic:

~~~text
Assess whether visual density per page is reasonable for the page size, audience, and interaction pattern.
• When applicable: the page contains multiple visuals, heavy custom formatting, or many interactions
• Guidance: there is no universal hard limit, but high visual counts increase queueing, rendering, and validation complexity
• Quantitative threshold: <=8 active visuals = low density; 9–12 = normal; 13–16 = review; >16 = high density and justification required
• Quantitative threshold: count each dominant large table/matrix as 2 visuals for review purposes
~~~

## Item 21

- Area: Model
- Category: Performance & Load
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-slicers)
- Topic:

~~~text
Assess whether high-cardinality slicers are necessary.
• When applicable: the report uses slicers over large text/ID domains
• Mark N/A when: the report has no such slicers
• Guidance: when they exist, prefer search, hierarchy, relative date, drillthrough, field parameters, or filter-pane patterns where they improve usability/performance
• Quantitative threshold: <=500 distinct slicer values = normal; 501–2,000 = review; 2,001–10,000 = require search/hierarchy/filter-pane/alternate pattern; >10,000 = avoid unless strongly justified
~~~

## Item 22

- Area: Model
- Category: Tables & Columns
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/model-explorer)
- Topic:

~~~text
Assess whether display folders are used where they materially improve discoverability for report authors.
• When applicable: the model exposes enough measures or reusable attributes that the field list becomes hard to navigate
• Mark N/A when: the model is small enough that folders add little value or create unnecessary nesting
• Guidance: prefer simple, business-oriented folder groupings rather than deep technical folder trees
• Quantitative threshold: 10 or more visible measures in one table = review display folders
• Quantitative threshold: 20 or more visible author-facing fields in one table = folders should be considered
~~~

## Item 23

- Area: Model
- Category: Tables & Columns
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/model-explorer)
- Topic:

~~~text
Assess whether descriptive metadata is filled out for visible tables, columns, measures, hierarchies, and other author-facing elements.
• When applicable: report authors or support staff will browse the model directly
• Mark N/A when: the model is tiny and the visible elements are fully self-explanatory
• Guidance: prioritize visible measures, KPI fields, calculated fields, and any non-obvious business terms
• Quantitative threshold: 100% of visible measures should have descriptions
• Quantitative threshold: 100% of visible non-obvious author-facing fields should have descriptions
~~~

## Item 24

- Area: Model
- Category: Tables & Columns
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-sort-by-column)
- Topic:

~~~text
Assess whether Sort by Column is set correctly for labels that have a business order different from alphabetical order.
• When applicable: the report contains month names, weekday names, bands, stages, fiscal periods, or other ordered labels
• Mark N/A when: all displayed labels are naturally sorted as-is
• Guidance: review visible ordered labels, including custom categories and staged process values
• Quantitative threshold: 100% of displayed ordinal labels should have correct Sort by Column set
• Quantitative threshold: 0 visibly mis-sorted month/day/band labels
~~~

## Item 25

- Area: Model
- Category: Tables & Columns
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization)
- Topic:

~~~text
Assess whether only necessary author-facing columns are exposed in Report view and whether unused columns are hidden.
• When applicable: the model is intended for report authoring, self-service, or shared semantic use
• Mark N/A when: a visible field is genuinely needed for visuals, export, drillthrough, reconciliation, troubleshooting, or support workflows
• Guidance: do not hide fields only because they look technical; hide them only when they are truly unnecessary for authors
• Quantitative threshold: 0 clearly unused visible columns unless justified
• Quantitative threshold: 100% of visible technical-looking fields should have a documented author/support use case
~~~

## Item 26

- Area: Model
- Category: Tables & Columns
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-data-categorization)
- Topic:

~~~text
Assess whether applicable data categories are set for fields such as URL, image, address, city, country, latitude, and longitude.
• When applicable: the model exposes fields used in maps, links, images, or geospatial visuals
• Mark N/A when: the report has no fields where data categorization affects behavior
• Guidance: review author-facing geo, URL, and image fields; do not over-categorize fields that do not need it
• Quantitative threshold: 100% of author-facing geo, URL, and image fields should have correct categories
• Quantitative threshold: 0 map-critical latitude/longitude fields left uncategorized
~~~

## Item 27

- Area: Model
- Category: Measures & DAX
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-measures)
- Topic:

~~~text
Assess whether measures are used instead of calculated columns where the logic is aggregation-oriented or presentation-oriented.
• When applicable: the report needs reusable business calculations, KPI logic, percentages, or aggregations across filter context
• Mark N/A when: the logic is truly row-level and belongs in a calculated column or upstream data shaping
• Guidance: favor measures for aggregated business logic and reserve calculated columns for row-by-row derivation that cannot be handled upstream
• Quantitative threshold: 100% of aggregation-oriented business calculations should be exposed as measures
• Quantitative threshold: 0 visuals should rely on calculated columns for logic that should behave dynamically by filter context
~~~

## Item 28

- Area: Model
- Category: Measures & DAX
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization)
- Topic:

~~~text
Assess whether measure naming and prefixes/suffixes follow a consistent standard that helps authors understand measure type and usage.
• When applicable: the model exposes reusable measures to report authors
• Mark N/A when: the team intentionally uses a no-prefix standard and that standard is applied consistently
• Guidance: keep naming readable and consistent; do not introduce prefix noise unless it truly helps authors
• Quantitative threshold: 0 visible measures should violate the chosen naming standard without justification
• Quantitative threshold: 0 duplicate visible measure names
~~~

## Item 29

- Area: Model
- Category: Measures & DAX
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/model-explorer)
- Topic:

~~~text
Assess whether explicit measures are used for report metrics instead of relying on implicit aggregations of raw columns.
• When applicable: the report exposes business metrics, KPIs, or reusable calculations
• Mark N/A when: a raw column is used only for simple ad hoc exploration and not as a governed published metric
• Guidance: prefer explicit measures for governed metrics so behavior, naming, formatting, and logic stay consistent
• Quantitative threshold: 100% of published business metrics should use explicit measures
• Quantitative threshold: 0 KPI or business-critical visuals should rely on implicit aggregation of raw columns
~~~

## Item 30

- Area: Model
- Category: Measures & DAX
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/model-explorer)
- Topic:

~~~text
Assess whether calculation groups, if used, are documented, tested, and safe for author consumption.
• When applicable: the model uses calculation groups for time intelligence, formatting, or reusable calculation logic
• Mark N/A when: the model does not use calculation groups
• Guidance: if used, review format string behavior, precedence, test coverage, and author guidance
• Quantitative threshold: 100% of calculation groups should have documented purpose
• Quantitative threshold: 100% of calculation items should have test coverage for format string and intended behavior
~~~

## Item 31

- Area: Model
- Category: Measures & DAX
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/model-date-tables)
- Topic:

~~~text
Assess whether time intelligence uses a robust Date table with unique continuous dates and the correct date-table setup.
• When applicable: the report uses dates for filtering, grouping, or time-based calculations
• Mark N/A when: the report does not perform time-based analysis
• Guidance: review date continuity, uniqueness, blanks, full-year coverage, and whether the intended date table strategy is correctly implemented
• Quantitative threshold: 1 dedicated date table expected for standard time intelligence
• Quantitative threshold: 0 blanks and 0 duplicate values in the date column
• Quantitative threshold: 0 missing dates in the covered range
~~~

## Item 32

- Area: Model
- Category: Measures & DAX
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-avoid-filter-as-filter-argument)
- Topic:

~~~text
Assess whether DAX context-modifying functions such as FILTER, ALL, and ALLEXCEPT are used intentionally and do not accidentally remove needed filter context.
• When applicable: the model contains measures using context-modifying functions
• Mark N/A when: the model does not use these patterns
• Guidance: review each usage for whether the removed or preserved context matches the business intent
• Quantitative threshold: 100% of measures using ALL or ALLEXCEPT should have clear business intent
• Quantitative threshold: 0 avoidable FILTER-as-filter-argument patterns for simple predicates
~~~

## Item 33

- Area: Model
- Category: Measures & DAX
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/divide-function-dax)
- Topic:

~~~text
Assess whether DAX divisions use DIVIDE where appropriate instead of the / operator.
• When applicable: the model contains division logic in measures or calculation items
• Mark N/A when: the denominator is guaranteed non-zero and the design intentionally does not need DIVIDE behavior
• Guidance: prefer DIVIDE for safer handling of zero or blank denominators
• Quantitative threshold: 100% of non-trivial DAX divisions should use DIVIDE unless explicitly justified otherwise
~~~

## Item 34

- Area: Model
- Category: Measures & DAX
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/best-practices/dax-variables)
- Topic:

~~~text
Assess whether repeated DAX expressions are cached with VAR where it improves readability or performance.
• When applicable: the same subexpression is used more than once in a measure or calculation item
• Mark N/A when: the expression is simple enough that VAR adds no meaningful value
• Guidance: use VAR when it reduces repeated evaluation or makes complex DAX easier to understand and maintain
• Quantitative threshold: 2 or more repeated subexpressions inside the same measure = review VAR usage
~~~

## Item 35

- Area: Model
- Category: Measures & DAX
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization)
- Topic:

~~~text
Assess whether reusable base measures are separated from presentation measures such as KPI wrappers, percentages, and time variants.
• When applicable: the model exposes multiple related presentations of the same business metric
• Mark N/A when: the model is too small/simple for a layered measure pattern to add value
• Guidance: base measures should hold core logic, while presentation measures build on them for readability and reuse
• Quantitative threshold: 2 or more presentation variants of the same metric = review for base-measure pattern
~~~

## Item 36

- Area: Model
- Category: Measures & DAX
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-measures)
- Topic:

~~~text
Assess whether visible measures have correct explicit formatting such as decimals, thousand separators, percentages, and currency.
• When applicable: the report exposes reusable measures to authors or end users
• Guidance: review format strings on visible measures and keep semantically identical metrics formatted consistently
• Quantitative threshold: 100% of visible measures should have intentional formatting
• Quantitative threshold: 0 repeated business metrics should display with inconsistent units or decimal precision unless justified
~~~

## Item 37

- Area: Model
- Category: Measures & DAX
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/report-page-tooltips)
- Topic:

~~~text
Assess whether metric definitions, exclusions, and caveats are surfaced through descriptions, tooltips, or other author/user-facing documentation.
• When applicable: the report contains business-critical KPIs, exception-heavy measures, or metrics that can be misunderstood without context
• Mark N/A when: the metric is fully self-explanatory and has no material exclusions or caveats
• Guidance: prioritize definitions for KPIs, percentages, exception-based metrics, and regulated numbers
• Quantitative threshold: 100% of business-critical KPIs should have a visible definition path (tooltip, description, or help text)
~~~

## Item 38

- Area: Model
- Category: Measures & DAX
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-query/dataflows/best-practices-for-dimensional-model-using-dataflows)
- Topic:

~~~text
Assess whether calculated tables are avoided for ETL-style shaping that should happen upstream.
• When applicable: the model contains calculated tables or table-building logic beyond small helper scenarios
• Mark N/A when: a calculated table is intentionally used for semantic-only purposes such as disconnected parameters, small helper tables, or controlled calculation patterns
• Guidance: use upstream dataflows/source shaping for ETL tasks and reserve calculated tables for semantic-model needs
• Quantitative threshold: 0 calculated tables should be used solely for ETL-style source reshaping
~~~

## Item 39

- Area: Documentation & Admin
- Category: Security & Governance
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance)
- Topic:

~~~text
Assess whether Row-Level Security roles are defined and tested wherever row filtering is required by audience or policy.
• When applicable: different audiences should see different data rows from the same model
• Mark N/A when: the dataset is intentionally open to all intended consumers and row filtering is not required
• Guidance: test roles in both Desktop and Service where deployment behavior matters
• Quantitative threshold: 100% of required RLS roles should be tested
• Quantitative threshold: 1 or more test cases per role should validate expected row access
~~~

## Item 40

- Area: Documentation & Admin
- Category: Security & Governance
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/fabric/security/service-admin-object-level-security)
- Topic:

~~~text
Assess whether Object-Level Security is used when columns or tables must be truly hidden for security reasons.
• When applicable: sensitive columns or tables must be inaccessible to certain audiences
• Mark N/A when: Report-view hiding is sufficient because the need is usability rather than security
• Guidance: do not confuse Report-view hiding with security; use OLS when data must not be accessible at all
• Quantitative threshold: 1 or more sensitive columns/tables requiring true restriction = review OLS
~~~

## Item 41

- Area: Documentation & Admin
- Category: Security & Governance
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security)
- Topic:

~~~text
Assess whether Dynamic RLS is implemented where identity-based row access is needed across multiple users or groups.
• When applicable: the same model serves multiple audiences with identity-driven row restrictions
• Mark N/A when: static roles are sufficient or row security is not needed
• Guidance: review identity mapping, group logic, and fallback behavior for unmatched users
• Quantitative threshold: 2 or more audiences sharing one model with identity-based row filtering = review Dynamic RLS
• Quantitative threshold: 100% of dynamic RLS mappings should be tested with representative identities
~~~

## Item 42

- Area: Documentation & Admin
- Category: Security & Governance
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-security-apply-data-sensitivity-labels)
- Topic:

~~~text
Assess whether sensitivity labels and endorsement/certification status are applied according to governance expectations.
• When applicable: the report or dataset is shared broadly, governed, or used as a reusable semantic asset
• Mark N/A when: the asset is ad hoc/personal and not subject to governance requirements
• Guidance: use the organization’s governance standard for labeling and endorsement rather than applying labels inconsistently
• Quantitative threshold: 100% of governed production datasets should have intentional endorsement/certification status
• Quantitative threshold: 100% of datasets subject to sensitivity policy should have the required label
~~~

## Item 43

- Area: Documentation & Admin
- Category: Security & Governance
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-permissions)
- Topic:

~~~text
Assess whether dataset permissions follow least-privilege principles and avoid unnecessary Build access.
• When applicable: the dataset is shared with report consumers, authors, or downstream self-service users
• Guidance: grant Build only to audiences who truly need semantic-model reuse or new-report authoring
• Quantitative threshold: 0 broad-audience Build grants unless justified
• Quantitative threshold: 100% of Build recipients should have a real authoring or downstream-use need
~~~

## Item 44

- Area: Documentation & Admin
- Category: Security & Governance
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-data-lineage)
- Topic:

~~~text
Assess whether lineage is accurate and dependencies are documented where lineage view alone is insufficient.
• When applicable: the asset is part of a governed reporting chain with upstream/downstream dependencies
• Guidance: review whether the published dependency picture matches the real delivery path of the report and semantic model
• Quantitative threshold: 100% of upstream/downstream production dependencies should be visible in lineage or documented elsewhere
~~~

## Item 45

- Area: Documentation & Admin
- Category: Security & Governance
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-scheduled-refresh)
- Topic:

~~~text
Assess whether refresh cadence, failure alerting, and recovery/runbook guidance are appropriate for the report’s SLA.
• When applicable: the dataset is refreshed on a schedule or is operationally important
• Mark N/A when: the dataset is manual/ad hoc and not expected to refresh automatically
• Guidance: review schedule frequency, ownership, alerting, and recovery instructions
• Quantitative threshold: 100% of production scheduled datasets should have an owner and alert path
• Quantitative threshold: 1 or more documented recovery/runbook steps should exist for refresh failure handling
~~~

## Item 46

- Area: Documentation & Admin
- Category: Quality, Testing & Documentation
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-query/best-practices)
- Topic:

~~~text
Assess whether null handling, outlier handling, and any approved business exceptions are documented.
• When applicable: the report logic treats blanks, nulls, exclusions, outliers, overrides, or capped values specially
• Mark N/A when: the report has no material special handling for nulls or outliers
• Guidance: focus on business-critical fields and metrics where special handling changes interpretation
• Quantitative threshold: 100% of critical null/outlier handling rules should be documented
• Quantitative threshold: 1 or more approval references should exist for manual overrides or approved exception rules
~~~

## Item 47

- Area: Documentation & Admin
- Category: Quality, Testing & Documentation
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-tmdl-view)
- Topic:

~~~text
Assess whether a changelog is maintained for production changes to the report or semantic model.
• When applicable: the asset is shared, production, or governed
• Mark N/A when: the asset is disposable/ad hoc and not maintained as a production artifact
• Guidance: track what changed, why, who changed it, and who approved it where applicable
• Quantitative threshold: 100% of production releases/changes should have a dated changelog entry with owner/reason
• Quantitative threshold: 1 or more approval references should be captured for governed changes
~~~

## Item 48

- Area: Documentation & Admin
- Category: Quality, Testing & Documentation
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-description)
- Topic:

~~~text
Assess whether KPI and dimension definitions are documented in a place users or support staff can find them.
• When applicable: the report exposes business terms, KPIs, or dimensions that are not universally understood
• Mark N/A when: the audience is extremely narrow and the business meaning is genuinely obvious
• Guidance: definitions can live in model descriptions, report help pages, dataset descriptions, or controlled documentation
• Quantitative threshold: 100% of business-critical KPIs should have documented definitions
• Quantitative threshold: 100% of non-obvious business dimensions should have a documented definition path
~~~

## Item 49

- Area: Visual
- Category: Visualizations (Reports, UX, Interactions)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-report-display-settings)
- Topic:

~~~text
Assess whether page layout follows a consistent grid, spacing, and alignment standard.
• When applicable: the report has multiple visuals or multiple pages intended for repeated use
• Guidance: review alignment, spacing rhythm, and whether similar visuals are placed consistently across pages
• Quantitative threshold: 0 overlapping visuals
• Quantitative threshold: review when 3 or more visuals are visibly off-grid or inconsistently aligned on the same page
~~~

## Item 50

- Area: Visual
- Category: Visualizations (Reports, UX, Interactions)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-report-themes)
- Topic:

~~~text
Assess whether a theme is applied intentionally for colors, fonts, palettes, and formatting consistency.
• When applicable: the report is shared, branded, or expected to follow organizational design standards
• Mark N/A when: the report is truly ad hoc and not intended for repeat distribution
• Guidance: prefer one approved or deliberately chosen theme rather than ad hoc formatting on every visual
• Quantitative threshold: 1 approved or intentionally documented theme expected for shared/production reports
• Quantitative threshold: 0 conflicting color systems or font systems across the report unless justified
~~~

## Item 51

- Area: Visual
- Category: Visualizations (Reports, UX, Interactions)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/button-navigators)
- Topic:

~~~text
Assess whether report navigation is intuitive, discoverable, and accessible.
• When applicable: the report has multiple pages, sections, states, or bookmarked navigation paths
• Mark N/A when: the report is a single simple page with no navigation need
• Guidance: review whether users can move through the report without guessing or getting stuck
• Quantitative threshold: 2 or more sections/pages with custom navigation = review navigation controls
• Quantitative threshold: 0 dead-end pages or hidden navigation paths without obvious access
~~~

## Item 52

- Area: Visual
- Category: Visualizations (Reports, UX, Interactions)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-report-display-settings)
- Topic:

~~~text
Assess whether canvas size and aspect ratio fit the intended devices and display context.
• When applicable: the report is designed for a known display target such as laptop, widescreen, kiosk, or embedded view
• Guidance: review whether the page design matches the intended consumption device and whether pages stay usable without awkward scrolling or clipping
• Quantitative threshold: 1 primary target aspect ratio should be used consistently unless page purpose differs
• Quantitative threshold: review mixed canvas sizes across pages unless clearly justified
~~~

## Item 53

- Area: Visual
- Category: Visualizations (Reports, UX, Interactions)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-report-settings)
- Topic:

~~~text
Assess whether persistent filters and default/reset behavior are designed intentionally.
• When applicable: the report uses slicers, bookmarks, or shared starting states that affect user experience
• Guidance: review whether the report should preserve user state, reset to authored defaults, or expose both behaviors clearly
• Quantitative threshold: 1 explicit decision should exist for persistent filters on production reports using slicers/bookmarks
~~~

## Item 54

- Area: Visual
- Category: Layout & Navigation
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualizations-overview)
- Topic:

~~~text
Assess whether each visual type matches the analytical intent of the question it answers.
• When applicable: the report contains charts used for comparison, distribution, trend, ranking, or part-to-whole analysis
• Guidance: review whether the chosen chart supports the question clearly and avoids avoidable distortion or clutter
• Quantitative threshold: part-to-whole visuals with more than 5 categories = review chart choice
• Quantitative threshold: trend visuals should use a true ordered time/category axis when showing change over sequence
~~~

## Item 55

- Area: Visual
- Category: Layout & Navigation
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-conditional-format-visual-titles)
- Topic:

~~~text
Assess whether titles, labels, and legends are concise, descriptive, and not misleading.
• When applicable: the report includes visuals that require interpretation by end users
• Guidance: remove placeholder text and make titles describe what the visual actually shows
• Quantitative threshold: 0 placeholder or ambiguous auto-generated titles on production visuals
~~~

## Item 56

- Area: Visual
- Category: Layout & Navigation
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualizations-overview)
- Topic:

~~~text
Assess whether units and scales are consistent where users are expected to compare visuals, and whether dual axes are avoided unless truly needed.
• When applicable: the report shows the same or related metrics across multiple visuals
• Guidance: review scale consistency, display units, and whether any dual-axis design is clearly labeled and justified
• Quantitative threshold: 0 unlabeled dual-axis visuals
• Quantitative threshold: 100% of repeated comparable metrics should use consistent display units unless justified
~~~

## Item 57

- Area: Visual
- Category: Layout & Navigation
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-conditional-formatting)
- Topic:

~~~text
Assess whether conditional formatting is used intentionally, consistently, and accessibly.
• When applicable: the report uses color, icons, or state formatting to communicate meaning
• Guidance: review semantic consistency of colors and avoid relying only on color for important meaning
• Quantitative threshold: no more than 2 semantic color systems should be used across one report unless justified
• Quantitative threshold: 0 critical states should be communicated by color alone without label/icon support
~~~

## Item 58

- Area: Visual
- Category: Layout & Navigation
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-conditional-formatting)
- Topic:

~~~text
Assess whether KPI thresholds are clear and color semantics are consistent across the report.
• When applicable: the report includes KPI or status visuals
• Mark N/A when: the report does not use KPI-style threshold logic
• Guidance: review whether threshold meaning is documented and whether the same colors always mean the same thing
• Quantitative threshold: 100% of KPI states should map to documented thresholds
• Quantitative threshold: 0 conflicting red/green semantics across KPI visuals unless explicitly explained
~~~

## Item 59

- Area: Visual
- Category: Layout & Navigation
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-drillthrough)
- Topic:

~~~text
Assess whether drill paths are available where useful and obvious enough for users to discover.
• When applicable: the report contains natural hierarchies, deeper levels, or drillthrough destinations
• Mark N/A when: the report is intentionally flat and no deeper navigation is needed
• Guidance: review whether drill affordances, labels, or instructions make the deeper path discoverable
• Quantitative threshold: 2 or more natural hierarchy levels or detail destinations = review drill path design
~~~

## Item 60

- Area: Visual
- Category: Interactivity & Filters
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/service-reports-visual-interactions)
- Topic:

~~~text
Assess whether cross-filtering and cross-highlighting behaviors are intentional and whether unexpected interactions are disabled.
• When applicable: multiple visuals on a page can interact with one another
• Guidance: review interaction behavior on each major visual and disable interactions that confuse the page story
• Quantitative threshold: 0 unexpected visual interactions on the page
~~~

## Item 61

- Area: Visual
- Category: Interactivity & Filters
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-slicers)
- Topic:

~~~text
Assess whether slicers are synced across pages where that improves continuity and whether slicers are organized clearly.
• When applicable: the same filter concept appears on 2 or more pages
• Mark N/A when: pages intentionally require different independent filter states
• Guidance: review repeated slicers and whether sync improves rather than harms the page workflow
• Quantitative threshold: the same slicer concept on 2 or more pages = review sync slicers
• Quantitative threshold: 0 duplicated repeated slicers left unsynced without a reason
~~~

## Item 62

- Area: Visual
- Category: Interactivity & Filters
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-bookmarks)
- Topic:

~~~text
Assess whether the report has an intentional default filter state and a clear way to return to it.
• When applicable: the report uses slicers, complex filter states, or bookmarks that change the page state
• Mark N/A when: the report has no meaningful filter state to reset
• Guidance: review entry-state behavior and whether users can reliably get back to the authored default
• Quantitative threshold: 1 clear reset/default path expected for reports with meaningful user-adjustable filter state
~~~

## Item 63

- Area: Visual
- Category: Interactivity & Filters
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/report-drillthrough)
- Topic:

~~~text
Assess whether drillthrough pages include clear instructions and back navigation.
• When applicable: the report uses drillthrough pages
• Mark N/A when: the report has no drillthrough pages
• Guidance: review whether users understand how to enter/leave drillthrough and what context the page expects
• Quantitative threshold: 100% of drillthrough pages should include back navigation
• Quantitative threshold: 100% of drillthrough pages should make their expected context obvious
~~~

## Item 64

- Area: Visual
- Category: Interactivity & Filters
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters)
- Topic:

~~~text
Assess whether field parameters are used where user-controlled switching would reduce page sprawl or improve flexibility.
• When applicable: users need to switch among 2 or more alternate metrics or dimensions in the same visual area
• Mark N/A when: the report is clearer with fixed visuals and does not benefit from parameter switching
• Guidance: consider field parameters when they reduce duplicate visuals or duplicate pages without harming clarity
• Quantitative threshold: 2 or more alternate metric/dimension choices competing for the same page space = review field parameters
~~~

## Item 65

- Area: Visual
- Category: Interactivity & Filters
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-tooltips)
- Topic:

~~~text
Assess whether tooltips provide useful context rather than repeating what is already obvious on the visual.
• When applicable: the report uses standard or report-page tooltips
• Mark N/A when: the report does not use tooltip enhancements
• Guidance: prioritize explanatory context, supporting detail, or related metrics that help the hovered value make sense
• Quantitative threshold: report-page tooltips should usually provide 3 or more context fields/metrics beyond the base hovered value
~~~

## Item 66

- Area: Visual
- Category: Accessibility
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports)
- Topic:

~~~text
Assess whether color contrast and non-color cues meet accessibility expectations.
• When applicable: the report uses color to communicate meaning or displays text over colored backgrounds
• Guidance: review contrast, label support, and whether important states are still understandable without color
• Quantitative threshold: text contrast should meet WCAG guidance where practical
• Quantitative threshold: 0 critical states should rely on color alone without icon/label support
~~~

## Item 67

- Area: Visual
- Category: Accessibility
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports)
- Topic:

~~~text
Assess whether text sizes remain readable on common consumption devices such as laptops and projected displays.
• When applicable: the report is intended for meetings, presentations, or standard desktop use
• Guidance: review title, body, axis, label, and footnote sizes under realistic viewing conditions
• Quantitative threshold: body text should generally be at least 10 pt
• Quantitative threshold: major titles should generally be at least 12 pt
~~~

## Item 68

- Area: Model
- Category: Performance & Load
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/performance-analyzer)
- Topic:

~~~text
Assess report performance with Performance Analyzer and review slow visuals/measures.
• When applicable: the report contains interactive visuals or users have reported slow behavior
• Guidance: also note whether the delay is mainly DAX query, visual display, or Other/queueing
• Quantitative threshold: repeated interactions — <100 ms excellent; 100–1000 ms acceptable; 1000–2000 ms investigate; 2000–3000 ms poor; >3000 ms bad; >10000 ms unacceptable without clear progress feedback
• Quantitative threshold: if DAX query time >1000 ms, treat as a model/DAX review candidate
• Quantitative threshold: if Other/queueing time >500 ms on repeated interaction, review page density/render order
~~~

## Item 69

- Area: Model
- Category: Performance & Load
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/buttons-apply-all-clear-all-slicers)
- Topic:

~~~text
Assess whether query-reduction features were considered where they would help (for example: Apply buttons on slicers, avoiding unnecessary sync/cross-highlighting, disabling auto page refresh unless needed).
• When applicable: the report has interactive controls that can generate unnecessary repeated queries
• Mark N/A when: the report has no interactive controls that would materially benefit
• Guidance: do not fail this item simply because a report has no need for query-reduction features
• Quantitative threshold: review Apply-button/query-reduction patterns when a page has 2 or more slicers commonly changed together
• Quantitative threshold: review when a single slicer change refreshes 5 or more visuals
• Quantitative threshold: auto page refresh intervals under 30 seconds require explicit justification
~~~

## Item 70

- Area: Visual
- Category: Consistency & Standards
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/report-themes-create-custom)
- Topic:

~~~text
Assess whether typography is consistent across titles, subtitles, body text, and footnotes.
• When applicable: the report uses multiple text elements across one or more pages
• Guidance: review font families, weight hierarchy, and text-size bands so similar text roles look the same everywhere
• Quantitative threshold: no more than 4 text-style roles should be used unless justified
• Quantitative threshold: 0 conflicting title/body styles for the same semantic role
~~~

## Item 71

- Area: Visual
- Category: Consistency & Standards
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/report-themes-create-custom)
- Topic:

~~~text
Assess whether number formatting is consistent across visuals for repeated or comparable metrics.
• When applicable: the report shows the same metrics in multiple places or compares related metrics side by side
• Guidance: review decimal precision, display units, separators, currency symbols, and percentage formatting
• Quantitative threshold: 100% of repeated comparable metrics should display with consistent format unless justified
~~~

## Item 72

- Area: Visual
- Category: Consistency & Standards
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-data-types)
- Topic:

~~~text
Assess whether visible date formats match audience expectations and the organization’s standard.
• When applicable: the report displays dates or date-like labels to end users
• Guidance: prefer one audience-appropriate visible date style unless different formats are intentionally required for different use cases
• Quantitative threshold: 100% of visible dates should follow one audience-appropriate standard unless justified
~~~

## Item 73

- Area: Visual
- Category: Consistency & Standards
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/button-navigators)
- Topic:

~~~text
Assess whether page names are clear, user-friendly, and free of unnecessary jargon.
• When applicable: the report has multiple pages or a broad end-user audience
• Guidance: use names that describe the page purpose rather than internal project language where possible
• Quantitative threshold: 0 page names should rely only on unexplained internal jargon or cryptic abbreviations for end-user audiences
~~~

## Item 74

- Area: Visual
- Category: Consistency & Standards
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/create-reports/report-themes-create-custom)
- Topic:

~~~text
Assess whether branding assets follow organizational standards and remain visually clean.
• When applicable: the report is branded or customer-facing
• Mark N/A when: the report intentionally avoids branding
• Guidance: review logo quality, color compliance, and whether brand elements help rather than distract
• Quantitative threshold: 0 stretched or visibly pixelated logo/image assets
• Quantitative threshold: 100% branded colors should match approved palette where branding is required
~~~

## Item 75

- Area: Documentation & Admin
- Category: Validation & User Readiness
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-data)
- Topic:

~~~text
Assess whether known limitations and usage caveats are surfaced on an Info/Help page or equivalent user-facing location.
• When applicable: the report has refresh latency, known caveats, exclusions, delayed data, or operational constraints users should understand
• Mark N/A when: the report truly has no meaningful caveats to communicate
• Guidance: include practical limitations such as refresh cadence, data latency, as-of timing, and last refreshed context where useful
• Quantitative threshold: 100% of material user-facing limitations should be documented in a discoverable place
~~~

## Item 76

- Area: Documentation & Admin
- Category: Validation & User Readiness
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization)
- Topic:

~~~text
Assess whether QA was completed with representative target users and whether the feedback loop is documented.
• When applicable: the report is intended for production or repeated use by a defined audience
• Mark N/A when: the report is a personal/ad hoc artifact with no shared audience
• Guidance: seek at least one representative tester per major audience where practical
• Quantitative threshold: 1 or more representative testers per major audience should review production reports before release
~~~

## Item 77

- Area: Documentation & Admin
- Category: Validation & User Readiness
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/collaborate-share/end-user-pdf)
- Topic:

~~~text
Assess whether important export scenarios such as Excel and PDF were tested where those outputs matter.
• When applicable: users are expected to export, print, or circulate snapshots of report content
• Mark N/A when: the report is not intended to be exported or printed
• Guidance: test the pages and visuals that matter most to downstream consumers
• Quantitative threshold: 100% of critical export/print scenarios should be tested where export is part of the user workflow
~~~

## Item 78

- Area: Documentation & Admin
- Category: Security & Sharing (Report Layer)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-permissions)
- Topic:

~~~text
Assess whether audience access was validated across apps, workspaces, and permissions before release.
• When applicable: the report is shared or published to any audience beyond the author
• Guidance: verify that the intended users can access the report and that unintended users cannot
• Quantitative threshold: 100% of intended audience groups should be access-tested before release
~~~

## Item 79

- Area: Documentation & Admin
- Category: Optional Add-ons (keep if useful)
- Microsoft documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/fabric/governance/endorsement-overview)
- Topic:

~~~text
Assess whether there is a decommission plan for legacy reports or datasets replaced by this asset.
• When applicable: the report or model replaces older production content
• Mark N/A when: the asset is net-new and does not replace anything
• Guidance: identify which assets are being replaced, who owns them, and when they will be retired
• Quantitative threshold: 100% of replaced legacy assets should have an owner and retirement path documented
~~~
