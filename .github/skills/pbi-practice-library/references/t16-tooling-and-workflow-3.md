# Tooling, workflow and AI assistance

Part 3 of 3 of this topic. Covers: Testing measures.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### Testing measures

**T16-A367-2.** Tests for a filter-dependent measure must catch wrong inclusions and wrong exclusions, through four kinds of case: positive, negative, preventing a false positive (valid only under a narrower filter), and preventing a false negative (valid although the earlier purchase lies outside the selection).
- Must. 2026. https://www.sqlbi.com/articles/testing-dax-measures-by-using-ai/
- When: Testing a measure, such as a new customers count, whose result depends on report filters.

**T16-A367-3.** Tests of a measure must recreate the filter contexts that define its business rules, such as a category filter or several brands selected together, not just compare a few totals: a change can leave a simple case intact yet alter results under those filters.
- Must. 2026. https://www.sqlbi.com/articles/testing-dax-measures-by-using-ai/
- When: Testing measures whose business logic depends on the active filters.

**T16-A367-4.** Verify the expected value of every test case independently, for example by inspecting the underlying transactions by hand, before accepting the test. The measure under test must never decide its own expected result, or the test is circular.
- Must. 2026. https://www.sqlbi.com/articles/testing-dax-measures-by-using-ai/
- When: Accepting test cases, especially when AI chose the cases and generated the queries.

**T16-A367-5.** When asking an AI assistant for tests of a measure, give it the business rule, the dimensions that must vary, the purpose of each kind of test and the exact shape of each result; a vague request yields cases that miss the relevant filter behaviour.
- Should. 2026. https://www.sqlbi.com/articles/testing-dax-measures-by-using-ai/
- When: Generating DAX tests for a measure with an AI assistant.

**T16-A367-6.** An AI assistant connected to the semantic model can also automate test preparation: it inspects the model, searches for suitable test cases, and runs or validates the test queries, sparing repeated manual filtering and reading of each customer's transactions.
- Option. Check. 2026. https://www.sqlbi.com/articles/testing-dax-measures-by-using-ai/
- When: Building tests for the measures of a semantic model.
- Version: Shown in 2026 with a model open in Power BI Desktop, reached through the local Power BI modeling MCP server.

**T16-A367-9.** A failing test can be written to return the expected and the actual value together with an explanation of the likely cause, which gives the first information needed to investigate a regression.
- Option. 2026. https://www.sqlbi.com/articles/testing-dax-measures-by-using-ai/
- When: Writing DAX query tests for measures.

**T16-A367-10.** Run measure tests on controlled input data, because they depend on the sample data they were built on: when transactions or dimension values change, revisit the test cases, or run them on a test model whose data does not change.
- Must. 2026. https://www.sqlbi.com/articles/testing-dax-measures-by-using-ai/
- When: Running tests of measures, whether or not AI created the tests.

**T16-A367-12.** Once reviewed, generated test queries can be kept as ordinary DAX code with the project and run again later. With customers, dates, filters and expected values fixed, the queries are deterministic, even though the AI discovery that produced them was not.
- Option. 2026. https://www.sqlbi.com/articles/testing-dax-measures-by-using-ai/
- When: Maintaining measure tests first created with AI help; manual checks through report pages are hard to repeat.

**T16-A367-13.** In measure testing, let AI explore the model, find candidate cases and write the repetitive test code, while a person keeps control of what counts as correct: the business requirement and the expected results, which still need human validation.
- Should. 2026. https://www.sqlbi.com/articles/testing-dax-measures-by-using-ai/
- When: Creating tests for measures with an AI assistant connected to the semantic model.

## Special-case techniques and facts

### Testing measures

**T16-A367-1.** A measure that shows the right value for one product, customer or selection is not thereby proven correct for others. It is correct only when it returns the expected result in every filter context and with every data situation.
- Fact. 2026. https://www.sqlbi.com/articles/testing-dax-measures-by-using-ai/
- When: Judging a measure, above all one whose business logic varies with the applied filters.

**T16-A367-7.** A measure test suite can be built from DAX user-defined functions, one per test, each returning one row of the same shape (test name, pass or fail, description) through a shared result function. A final EVALUATE combines the chosen tests with UNION.
- Option. 2026. https://www.sqlbi.com/articles/testing-dax-measures-by-using-ai/
- When: Writing repeatable DAX query tests, to run the whole suite or only tests linked to a change.
- Version: User-defined functions need compatibility level 1702 or above; generally available since the June 2026 release.

**T16-A367-8.** In a test query, TREATAS can apply the filters of the case (customer, category, brands, date) to reproduce the report's filter context, and COALESCE can turn a blank result into zero when the case expects the customer not to be counted.
- Option. 2026. https://www.sqlbi.com/articles/testing-dax-measures-by-using-ai/
- When: Writing DAX query tests that reproduce report selections for a count measure; applies to the query, not the measure.

**T16-A367-11.** Passing every test in a suite does not prove a measure correct in all possible contexts. How complete a suite is depends on the calculation and on the model complexity that can affect the DAX expression.
- Fact. 2026. https://www.sqlbi.com/articles/testing-dax-measures-by-using-ai/
- When: Interpreting the results of a test suite for a measure.
