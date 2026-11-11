# The DAX standard

How every DAX formula in a model built from this template is written: measures, calculated columns, calculation items, functions and role filters. `python scripts/check_project.py .` checks it; the code after each rule is the finding it gives (M5xx, M908, M909, M010, M806, M807). An exception passes only when section 9 of `docs/report-brief.md` lists the code and the object as the check prints it (`[Measure]`, `Table[Column]`, `calculation item 'Name'`, `function Name`), with a reason.
Formulas are read by a scanner (`scripts/formula_scanner.py`), not by a DAX parser: it knows names, texts, comments and brackets, not what a formula means. A warning is a strong hint; read the formula before you change it.

## A. Rules Microsoft gives

**1. Error functions.** Do not use IFERROR or ISERROR. Why: they add scans of the data and hide errors that should be fixed at the source. Use DIVIDE for a division, test the cause with IF, and clean bad values in Power Query. Check: M501 (warn). Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-error-functions ; rule AVOID_USING_THE_IFERROR_FUNCTION in https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json

**2. Division.** Divide with DIVIDE whenever the divisor is a measure, a column or any expression. Why: DIVIDE returns blank for a zero or blank divisor, and does so faster than an IF test. Check: M502 (fail; checklist item 33 asks for DIVIDE in 100% of such divisions unless the reason is written down).

```dax
DIVIDE (
    [Total Sales],
    [# Orders]
)
```

- Not `[Total Sales] / [# Orders]`.
- A fixed number written directly after the sign passes: `[Total Sales] / 1000`. Here Microsoft prefers the operator. The reverse, DIVIDE by a fixed number such as `DIVIDE ( [Total Sales], 1000 )`, gives M518 (warn): write `[Total Sales] / 1000` instead.
- Inside an iterator over many rows, Microsoft's skill and SQLBI accept `/` once rows with a zero divisor are filtered out first. Such a formula needs a row in section 9 with M502 and that reason.
- Leave out DIVIDE's third argument (rule 7).
- Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-divide-function-operator ; https://learn.microsoft.com/en-us/dax/divide-function-dax ; rule USE_THE_DIVIDE_FUNCTION_FOR_DIVISION in the best practice rules above; https://www.sqlbi.com/articles/divide-performance/

**3. Counting rows.** Count rows with `COUNTROWS ( Sales )`, not `COUNT ( Sales[Order Key] )`. Why: it says what you mean, is faster, and does not skip rows where one column is blank. Check: M503 (warn; a measure that is one COUNT or COUNTA over a column). If the measure really counts the non-blank values of one column, list it in section 9. Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-countrows

**4. One selected value.** Read a single selected value with `SELECTEDVALUE ( Store[City] )`, not IF with HASONEVALUE and VALUES. Give a second argument when "none or several" needs its own result. Why: one function does both steps. Check: M504 (warn). Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-selectedvalue

**5. VALUES compared with one value.** Never compare VALUES of a column with one value, as in `VALUES ( Store[City] ) = "Utrecht"`. Why: it returns an error as soon as two or more values are in the filter. Use SELECTEDVALUE. Check: M517 (warn). Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-selectedvalue

**6. FILTER as a filter argument.** In CALCULATE and CALCULATETABLE, filter the column, not FILTER over a whole table. Why: a column filter is faster and clearer. Checklist item 32 allows 0 avoidable cases. Check: M505 (warn).

```dax
CALCULATE (
    [Total Sales],
    KEEPFILTERS ( Store[City] = "Utrecht" )
)
```

- Not `CALCULATE ( [Total Sales], FILTER ( Store, Store[City] = "Utrecht" ) )`.
- KEEPFILTERS: a plain column test replaces any filter already on that column; FILTER over the table kept it. Wrap the test in KEEPFILTERS to keep the old result. SQLBI adds: a test on one value of one column needs no KEEPFILTERS; several values, or several columns, do (no check).
- When the test needs a measure, FILTER stays, but over `VALUES ( Store[City] )`, not over the table `Store`.
- Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-avoid-filter-as-filter-argument ; rule FILTER_COLUMN_VALUES in the best practice rules; https://www.sqlbi.com/articles/best-practices-for-using-keepfilters-in-dax/

**7. Blanks stay blank.** A measure with nothing to show returns blank. Do not write `IF ( ISBLANK ( x ), 0, x )`, `COALESCE ( x, 0 )`, `DIVIDE ( a, b, 0 )` or `+ 0`. Why: a zero makes every item appear in a visual, which is slower and uses more memory. If all items must show, the developer turns on "Show items with no data" on the visual. A zero the brief asks for goes in section 9. Check: M506 (warn; measures only). Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-converting-blank

Where a fallback that is not a zero is allowed (a second measure, or a value the brief asks for), COALESCE says it more plainly than IF with ISBLANK; it is not faster. When the formula reads the same measure again, put it in a variable first, so it is worked out once (rule 8). No check. Source: https://www.sqlbi.com/articles/the-coalesce-function-in-dax/

**8. Variables.** When one expression appears twice in a formula, store it in a variable. Why: it is worked out once and the formula reads better. Checklist item 34: two or more repeats in one measure is a review point. Also break deep CALCULATE nesting into variables, or give one CALCULATE all its filters (Microsoft's skill; awesome-copilot): M521 (warn) reports CALCULATE written directly as the first argument of CALCULATE. Check: M507 (warn; a call of six tokens or more written twice).

```dax
VAR UtrechtSales =
    CALCULATE (
        [Total Sales],
        Store[City] = "Utrecht"
    )
RETURN
    UtrechtSales - UtrechtSales * 0.1
```

Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-variables ; https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/dax-guidelines.md ; https://github.com/github/awesome-copilot/blob/main/instructions/power-bi-dax-best-practices.instructions.md (one CALCULATE with several filters)

**9. EARLIER and EARLIEST.** Do not use them. Store the outer value in a variable before the inner row context starts. Why: a variable is clearer and does the same. Check: M514 (warn). Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-variables

**10. Column and measure references.** Write a column with its table, `Sales[Amount]`, and a measure without one, `[Total Sales]`. Why: a measure written with its table breaks when the measure moves to another table, and a bare name then always means a measure. M010 reads measures, calculated columns, calculation items, role filters and user-defined functions. It reports a bare name that is a column, and a measure written with a table. Microsoft Learn also asks for table names on columns inside functions (rule 39). This is rule 5 of the model standard. Check: M010 (warn). Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-column-measure-references ; https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions ; rules DAX_COLUMNS_FULLY_QUALIFIED and DAX_MEASURES_UNQUALIFIED in the best practice rules

**11. Window functions.** OFFSET, WINDOW, INDEX, RANK and ROWNUMBER always get ORDERBY, and PARTITIONBY when the order restarts per group. Why: columns that are added by default come in no fixed order, so results can surprise. When the ORDERBY and PARTITIONBY columns do not identify every row, add MATCHBY with columns that do (no check). Check: M516 (warn).

```dax
RANK (
    DENSE,
    ALLSELECTED ( Store[City] ),
    ORDERBY (
        [Total Sales],
        DESC
    )
)
```

Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-understand-orderby

**12. Two measures, one formula.** Keep one and use it everywhere. Spaces, comments and the capitals of function names do not count as a difference. Check: M508 (warn). Source: rule AVOID_DUPLICATE_MEASURES in the best practice rules

**13. A measure that only repeats another.** A measure whose whole formula is `[Total Sales]` adds nothing. Use the measure it repeats. Check: M509 (warn). Source: rule MEASURES_SHOULD_NOT_BE_DIRECT_REFERENCES_OF_OTHER_MEASURES in the best practice rules

**14. INTERSECT.** For a relationship made inside a formula, use TREATAS, not INTERSECT. Why: TREATAS performs better. Check: M510 (warn). Source: rule USE_THE_TREATAS_FUNCTION_INSTEAD_OF_INTERSECT in the best practice rules; Microsoft's skill (address in rule 8)

**15. One minus a ratio.** Divide the difference once. Not `1 - DIVIDE ( [Total Cost], [Total Sales] )`. Why: the "1 -" form always returns a value, so visuals show rows that should stay empty, and it is slower. Check: M511 (warn; a number plus or minus DIVIDE). The same thing written with `/` is reported as M502.

```dax
VAR Sales = [Total Sales]
RETURN
    DIVIDE (
        Sales - [Total Cost],
        Sales
    )
```

Source: rule AVOID_USING_'1-(X/Y)'_SYNTAX in the best practice rules; Microsoft's skill (address in rule 8)

**16. EVALUATEANDLOG.** It is a testing aid. Remove it before the model is published. Check: M512 (warn). Source: rule EVALUATEANDLOG_SHOULD_NOT_BE_USED_IN_PRODUCTION_MODELS in the best practice rules; Microsoft's skill (address in rule 8)

**17. Time intelligence in a DirectQuery model.** When any table is DirectQuery, time intelligence functions can be slow. If visuals are slow, use columns in the date table or prior-period values prepared at the source, with plain filters. Check: M513 (warn; a measure or calculation item calls a function from the time intelligence group of the function index). Source: rule MEASURES_USING_TIME_INTELLIGENCE_AND_MODEL_IS_USING_DIRECT_QUERY in the best practice rules

**18. Names the model does not have.** Every `Table[Name]` must be a column of that table or a measure. Why: otherwise the formula returns an error. Read the table's file before you write a name. The check only sees names written with a table that exists; check bare `[Name]` references yourself. Check: M908 (fail). Source: https://learn.microsoft.com/en-us/dax/dax-syntax-reference

**19. Functions that do not exist.** Call only functions in the file `dax-functions.md` beside this one, or a user-defined function of this model. Look up a function before you use it for the first time (skill `pbi-lookup`); never invent one. Check: M909 (warn). Source: https://learn.microsoft.com/en-us/dax/dax-function-reference ; the index is built from https://learn.microsoft.com/en-us/dax/toc.json

**20. Removing filters on purpose.** Every ALL, ALLEXCEPT and REMOVEFILTERS must match the business question: which filters the measure ignores, and why. Checklist item 32 asks for 100% of them. If the brief does not say, ask the developer. Judged in the review.

- Use REMOVEFILTERS when the aim is only to clear filters inside CALCULATE (Microsoft's skill). M519 (warn) reports ALL ( ... ) written directly as a filter argument of CALCULATE or CALCULATETABLE; ALL stays where a table is needed, such as the table an iterator walks.
- Use ALL when a table is needed, and ALLSELECTED for totals of what the visual shows (SQLBI).
- Use ALLEXCEPT only when the kept column is filtered directly; otherwise REMOVEFILTERS plus VALUES (Microsoft's skill and SQLBI).
- Source: checklist item 32; Microsoft's skill (address in rule 8); https://www.sqlbi.com/articles/all-vs-allselected-vs-allexcept-vs-removefilters/

**21. Base and presentation measures.** A base measure holds the core logic once (`Total Sales`). Ratios, KPIs and time variants call it (`Total Sales YTD` uses `[Total Sales]`) and never repeat `SUM ( Sales[Amount] )`. Two or more variants of one metric is a review point. Judged in the review. Source: checklist item 35, which points to https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization

## B. DAX style

The style is SQLBI's formatting rules, restated in new words; no SQLBI text, code or image is copied. M520 (warn) reads measures, calculated columns, calculation items, functions and role filters. It gives one warning per table file, names the formulas, and quotes each rule broken; its text starts with the words given below. An exception is listed per object, with M520.

22. Write CALCULATE in full, never `[Total Sales] ( Store[City] = "Utrecht" )`. M520: "write CALCULATE in full".
23. Put one space between a function name and `(`, and one before `)`: `SUM ( Sales[Amount] )`. An empty pair stays together: `SELECTEDMEASURE ()`. M520: "put a space between a function name and '('", "put a space before ')'".
24. Keep `(` on the line of its function name. M520: "keep '(' on the line of its function name".
25. Put each comma directly after its argument, and a space after it when the next argument is on the same line. M520: "put each comma directly after its argument", "put a space after a comma".
26. Put a space on both sides of an operator: `+ - * / & = < > <= >= <> && ||`. M520: "put a space on both sides of an operator".
27. When an expression goes on to the next line, start that line with the operator. The only operator that may end a line is the `=` of `VAR Name =`. M520: "start a continued line with the operator".
28. Write a column right after its table, with no space: `Sales[Amount]`. M520: "write a column directly after its table".
29. A call with two or more arguments, or with another call inside it, puts each argument on its own line. A call with one plain argument stays on one line. M520: "put each argument on its own line".
30. A column that a formula makes with ADDCOLUMNS or SELECTCOLUMNS gets a name that starts with `@`: `"@Store Sales"`. Why: it cannot be mistaken for a measure. M520 checks this in measures, calculation items and functions: "start the name of a column the formula makes with @".
31. Give a variable a plain name that says what it holds, such as `PriorSales`. No check. (A `_` prefix, which Microsoft's skill uses, is not adopted: see "Where sources disagree".)

SQLBI rules the template does not check:

- Indent arguments four spaces and line the closing bracket up with its call: TMDL adds its own tab indentation, so the check cannot judge it. Follow it anyway, as the shipped examples do.
- `:=` for measures: TMDL always writes `measure 'Name' =`. Does not apply.
- Name on its own line, formula below: TMDL does this for a formula of more than one line.
- Quotes round a table name only when needed: not adopted. Microsoft's skill writes quotes round every table name, and a higher source wins. Both forms pass. A name with a space or a reserved word always needs quotes: `'Date'[Date]`.

A complete measure in the style (made up):

```
	/// Share of total sales made by online stores.
	measure 'Online Sales Share (%)' =
			VAR OnlineSales =
			    CALCULATE (
			        [Total Sales],
			        Store[Store Type] = "Online"
			    )
			VAR AllSales = [Total Sales]
			RETURN
			    DIVIDE (
			        OnlineSales,
			        AllSales
			    )
		formatString: 0.0%
		displayFolder: Finance\Ratios
```

Source: https://www.sqlbi.com/articles/rules-for-dax-code-formatting/ ; https://www.sqlbi.com/articles/naming-temporary-columns-in-dax/ ; rule 31: Microsoft's skill (address in rule 8).

## C. DAX patterns

Pick a time pattern by the calendar (SQLBI, https://www.daxpatterns.com/time-patterns/):

- Standard: a Gregorian calendar whose fiscal year starts at a calendar quarter. Uses the built-in time functions.
- Month: reports never go below the month. Simpler and faster formulas.
- Week: a calendar built from weeks (ISO, 4-4-5). Custom: only when nothing else fits. Take the simplest that fits.

A pattern is never written from memory and never pasted. Before using one, read about it with the skill `pbi-lookup`: SQLBI's article on it when sqlbi.com has one, and the Microsoft Learn page of each function it uses. The daxpatterns.com addresses in this file name the source of each pattern for a person; the look-up skill does not open that site. Write the measure for THIS model, with its own tables and names, in this standard's style.

Rolling windows: the negative offset of DATESINPERIOD equals the length of the window, counted back from the last date. A 12-month window takes -12, a 3-month window -3; one less leaves a period out. A time function also needs a current date to start from: a date column on the visual or in its filters. A query or a ROW formula with no date of its own gets one from an outer CALCULATETABLE. No check. Source: Microsoft's skill (address in rule 8).

```dax
CALCULATE (
    [Total Sales],
    DATESINPERIOD (
        'Date'[Date],
        MAX ( 'Date'[Date] ),
        -12,
        MONTH
    )
)
```

Time intelligence needs a marked date table: rule in the file `relationships-and-dates.md` beside this one, checks M402 to M404. The shipped examples are `Total Sales YTD`, `Total Sales PY` and `Total Sales vs PY (%)` in `tests/fixtures/examples/Examples.SemanticModel/definition/tables/_Measures.tmdl`. Microsoft's calendar-based time intelligence is a preview feature (https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-time-intelligence). Example: `tests/fixtures/examples/preview/Calendar.SemanticModel`. Use it only with the developer's yes (owner's rule).

| When you need | Pattern | Address |
|---|---|---|
| To choose the time pattern that fits the calendar | Time patterns | https://www.daxpatterns.com/time-patterns/ |
| Year to date, prior period and growth on a Gregorian calendar | Standard time-related calculations | https://www.daxpatterns.com/standard-time-related-calculations/ |
| Time calculations when reports stop at the month | Month-related calculations | https://www.daxpatterns.com/month-related-calculations/ |
| Time calculations on a calendar made of weeks | Week-related calculations | https://www.daxpatterns.com/week-related-calculations/ |
| A fiscal calendar the built-in functions cannot handle | Custom time-related calculations | https://www.daxpatterns.com/custom-time-related-calculations/ |
| To compare two chosen periods of different length | Comparing different time periods | https://www.daxpatterns.com/comparing-different-time-periods/ |
| Balances or stock shown at the start or end of a period | Semi-additive calculations | https://www.daxpatterns.com/semi-additive-calculations/ |
| A running total, or a balance built from movements | Cumulative total | https://www.daxpatterns.com/cumulative-total/ |
| A slicer value that changes a calculation | Parameter table | https://www.daxpatterns.com/parameter-table/ |
| To put a number into fixed bands | Static segmentation | https://www.daxpatterns.com/static-segmentation/ |
| To group items by a measure under the current filters | Dynamic segmentation | https://www.daxpatterns.com/dynamic-segmentation/ |
| To class items A, B, C by their share of the total | ABC classification | https://www.daxpatterns.com/abc-classification/ |
| New, returning, lost and recovered customers per period | New and returning customers | https://www.daxpatterns.com/new-and-returning-customers/ |
| A distinct count limited to items with fact rows | Related distinct count | https://www.daxpatterns.com/related-distinct-count/ |
| To count things open between a start and an end date | Events in progress | https://www.daxpatterns.com/events-in-progress/ |
| A rank, or the top N in each group | Ranking | https://www.daxpatterns.com/ranking/ |
| A measure that knows its hierarchy level, such as share of parent | Hierarchies | https://www.daxpatterns.com/hierarchies/ |
| A tree of varying depth, such as accounts or an organisation | Parent-child hierarchies | https://www.daxpatterns.com/parent-child-hierarchies/ |
| To compare periods only for stores active in all of them | Like-for-like comparison | https://www.daxpatterns.com/like-for-like-comparison/ |
| How many items moved between categories over time | Transition matrix | https://www.daxpatterns.com/transition-matrix/ |
| Which products are bought together | Basket analysis | https://www.daxpatterns.com/basket-analysis/ |
| Amounts reported in another currency with rate tables | Currency conversion | https://www.daxpatterns.com/currency-conversion/ |
| A budget at a coarse grain shown beside actuals at a finer one | Budget | https://www.daxpatterns.com/budget/ |

## D. Functions that repeat a pattern

- When three or more measures share one formula pattern, the check gives note U001. Copilot may suggest a user-defined function that holds the pattern once (example: `tests/fixtures/examples/Examples.SemanticModel/definition/functions.tmdl`).
- When six or more measures use time intelligence and the model has no calculation group, the check gives note U002. Copilot may suggest a calculation group (example: the table 'Time Calculation' of the example model, listed in `tests/fixtures/examples/INDEX.md`).
- Both are suggestions for the summary at the end of a task, never a question in the middle of one.
- Details are in the file `model-objects.md` beside this one.

## E. Grouping, iteration, speed and functions

**32. SUMMARIZE only groups.** Use SUMMARIZE to list the combinations of columns that exist, never to add a column it computes (a quoted name with an expression inside the call). Why: a column computed inside SUMMARIZE is worked out in a context that is hard to predict, and can be wrong or slow. Group with SUMMARIZE and add the column with ADDCOLUMNS around it, or use SUMMARIZECOLUMNS, which Microsoft's skill prefers for grouping with values. When the table to group is filtered first, group the plain table and give the filters to an outer CALCULATETABLE (Microsoft's skill, pattern DAX005). SQLBI names a few special cases where a column inside SUMMARIZE is still needed: such a formula goes in section 9 with M522. Check: M522 (warn).

```dax
ADDCOLUMNS (
    SUMMARIZE (
        Sales,
        Store[City]
    ),
    "@City Sales", [Total Sales]
)
```

Source: https://www.sqlbi.com/articles/best-practices-using-summarize-and-addcolumns/ ; Microsoft's skill, patterns DAX002 and DAX005 in https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/dax-perf-patterns.md

**33. SUMMARIZECOLUMNS takes its filters from outside.** Inside a measure, give SUMMARIZECOLUMNS no filter argument (FILTER, TREATAS or KEEPFILTERS among its arguments). Wrap it in CALCULATETABLE and put the filters there. Why: Microsoft's skill and SQLBI both place them outside; inside, they can change which rows come back and add work. Check: M523 (warn).

```dax
CALCULATETABLE (
    SUMMARIZECOLUMNS (
        Store[City],
        "@City Sales", [Total Sales]
    ),
    Product[Category] = "Garden"
)
```

The model setting for how SUMMARIZECOLUMNS treats filters on values is in the file `more-model-features.md` beside this one. Source: Microsoft's skill, pattern DAX009 (address in rule 32); https://www.sqlbi.com/articles/summarizecolumns-best-practices/

**34. ALLSELECTED stays out of iterations.** A measure that uses ALLSELECTED is never called inside an iterator (SUMX, AVERAGEX, FILTER and the like), directly or through another measure. Why: ALLSELECTED is meant to bring back the filters of the visual; inside an iteration it can bring back the filters of the iteration instead, and the result is hard to predict. Keep such measures few, and use them at the top of a chain, the measure the visual shows. No check: it needs the chain of measures. Source: https://www.sqlbi.com/articles/allselected-best-practices/

**35. Context transition inside an iterator.** A measure reference or a CALCULATE inside SUMX or another iterator runs once for every row. Over a large table that is slow. In order of preference: write the row expression with columns only (`Sales[Quantity] * RELATED ( Product[Unit Cost] )`); walk only the distinct values that matter (`VALUES ( Store[Store Key] )`), not the whole table; or build the rows and their values once with SUMMARIZECOLUMNS and walk that. Each rewrite must return the same numbers. No check. Source: Microsoft's skill, patterns DAX006, DAX008 and DAX015 (address in rule 32)

**36. True or false as a number.** Inside an iterator, turn a test into 1 or 0 with `INT ( test )`, not with IF. To count the rows that pass a test, use `CALCULATE ( COUNTROWS ( Sales ), test )`, with no iterator. Microsoft's skill also multiplies a value by a test, so that sibling measures can share one scan of the fact table. That form returns 0 where rule 7 wants blank, and only suits sums: keep it only when a timing shows a gain. No check. Source: Microsoft's skill, patterns DAX007 and DAX017 (address in rule 32)

**37. More of Microsoft's speed patterns.** Microsoft's skill offers each as something to try and then measure, not as a rule to apply blindly: keep a rewrite only when it returns the same numbers and runs faster. No check.

- Filter a table with CALCULATETABLE, not FILTER over it, when the test is a plain column test (DAX010).
- Write each filter once; drop one that repeats another (DAX004).
- Keep base measures free of time functions; apply the time function once, in the measure that combines them (DAX019, DAX020).
- To count the unique key of a table, COUNTROWS of the table is enough (DAX014). Replacing DISTINCTCOUNT by SUMX over DISTINCT is sometimes faster: keep it only after a timing (DAX011).
- A measure that picks one of several measures with SWITCH reads the column the slicer filters directly, keeps each branch to one simple sum, and returns one data type (DAX013).
- Before changing a relationship that filters both ways or is many-to-many, try the other path inside one measure with TREATAS or CROSSFILTER (DAX016).
- A visual filter on a measure value, such as "over 1 million", works the measure out twice. A measure that returns blank under the threshold gives the same visual in one pass (QRY002). It changes the report: only with the developer's yes.
- Source: Microsoft's skill, sections 3 and 4 of the catalogue (address in rule 32)

**38. Model changes in the same catalogue.** Microsoft's skill lists model changes that make DAX faster. Each needs the developer's yes, and the skill advises trying it on a copy of the model first. No check. Most are rules already: flatten snowflakes (rule 3 of the file `relationships-and-dates.md` beside this one); whole-number keys and fewer distinct values, aggregation tables, and an "unknown" row so that every fact key matches (rules 16, 20, 24 and 25 of the file `storage-and-security.md` beside this one). The others:

- Try more than one layout for a many-to-many bridge, above all when it carries security, and measure each (MDL001).
- For a fixed comparison on a large DirectQuery table, store the prior-period value as a column of the fact table (MDL005).
- A time table with one row per period and date can replace time functions in measures (MDL006).
- Replace SEARCH or FIND in a filter by a true-or-false column made at the source (MDL008).
- Collapse old key values, beyond the history reports need, into one placeholder value at the source (MDL009).
- Source: Microsoft's skill, section 5 of the catalogue (address in rule 32)

**39. Inside user-defined functions.** How functions are written and named is in the file `model-objects.md` beside this one. Three DAX rules apply inside them:

- Write every column with its table. Inside a function, Microsoft reads a bare name as a measure, so renames and dependency tracking can miss the column. Check: M010 (warn; rule 10). Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions
- Never name a table or column that a role hides with object-level security. That security does not reach into a function. Check: M806 (warn). Source: the same page.
- Names, following SQLBI: a function name starts with a capital and holds no underscore, with dots to group related functions (such as `Local.` for a function tied to this model); a parameter name starts with a lower-case letter (`amount`, `taxRate`). Check: M807 (warn). Source: https://www.sqlbi.com/articles/model-dependent-and-model-independent-user-defined-functions-in-dax/ ; https://www.sqlbi.com/articles/understanding-parameter-types-in-dax-user-defined-functions-udf/

## Sources

Read on 11 November 2026. Every rule is restated in this template's own words.

- Microsoft Learn, DAX best practices: https://learn.microsoft.com/en-us/dax/best-practices/dax-error-functions ; https://learn.microsoft.com/en-us/dax/best-practices/dax-divide-function-operator ; https://learn.microsoft.com/en-us/dax/best-practices/dax-countrows ; https://learn.microsoft.com/en-us/dax/best-practices/dax-selectedvalue ; https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-avoid-filter-as-filter-argument ; https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-converting-blank ; https://learn.microsoft.com/en-us/dax/best-practices/dax-variables ; https://learn.microsoft.com/en-us/dax/best-practices/dax-column-measure-references ; https://learn.microsoft.com/en-us/dax/best-practices/dax-understand-orderby ; https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions
- Microsoft Learn, other: https://learn.microsoft.com/en-us/dax/divide-function-dax ; https://learn.microsoft.com/en-us/dax/dax-syntax-reference ; https://learn.microsoft.com/en-us/dax/dax-function-reference ; https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-time-intelligence
- Microsoft's best practice rules (MIT), category "DAX Expressions" and the DirectQuery time intelligence rule: https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json
- Microsoft's skill `semantic-model-authoring` (MIT), DAX guidelines: https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/dax-guidelines.md
- Microsoft's skill `semantic-model-authoring` (MIT), DAX performance catalogue: https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/dax-perf-patterns.md
- GitHub's `awesome-copilot` repository (MIT), DAX instructions: https://github.com/github/awesome-copilot/blob/main/instructions/power-bi-dax-best-practices.instructions.md
- SQLBI: https://www.sqlbi.com/articles/rules-for-dax-code-formatting/ ; https://www.sqlbi.com/articles/naming-temporary-columns-in-dax/ ; https://www.sqlbi.com/articles/divide-performance/ ; https://www.sqlbi.com/articles/best-practices-for-using-keepfilters-in-dax/ ; https://www.sqlbi.com/articles/all-vs-allselected-vs-allexcept-vs-removefilters/ ; https://www.sqlbi.com/articles/the-coalesce-function-in-dax/ ; https://www.sqlbi.com/articles/best-practices-using-summarize-and-addcolumns/ ; https://www.sqlbi.com/articles/summarizecolumns-best-practices/ ; https://www.sqlbi.com/articles/allselected-best-practices/ ; https://www.sqlbi.com/articles/model-dependent-and-model-independent-user-defined-functions-in-dax/ ; https://www.sqlbi.com/articles/understanding-parameter-types-in-dax-user-defined-functions-udf/ ; the 23 pattern pages of https://www.daxpatterns.com/ listed in section C.
- The owner's checklist, `checklist/checklist.md`, items 32 to 35.

Where sources disagree, and what was decided. Order of trust: the owner's checklist; Microsoft Learn; Microsoft's skills and best practice rules; SQLBI for DAX; then others. A lower source never overrides a higher one.

- IFERROR: Microsoft Learn says avoid it; Microsoft's skill accepts it as a single guard on one value. Learn wins: M501 warns on every use. A justified guard goes in section 9.
- `/` inside iterators: Microsoft's skill and SQLBI accept it once zero divisors are removed. Checklist item 33 asks for DIVIDE unless justified: M502 fails, and the reason goes in section 9.
- DIVIDE by a constant: Microsoft's skill says DIVIDE by default; Microsoft Learn prefers `/` for a constant. Learn wins: `/ 1000` passes, and M518 warns on DIVIDE by a fixed number.
- M010: Microsoft Learn says a measure written with its table breaks. The check only warns, because a text scanner cannot be certain (the level rule at the top of `scripts/model_rules.py`). Treat the rule as a must.
- Table quotes: SQLBI quotes only when needed; Microsoft's skill always quotes. SQLBI's rule is not adopted; no check.
- Variable names: Microsoft's skill starts them with `_`; Microsoft Learn's page on variables (https://learn.microsoft.com/dax/best-practices/dax-variables) and SQLBI write plain names. Microsoft Learn is the higher source, so the `_` prefix is not adopted (rule 31).
- SUMMARIZECOLUMNS inside a measure: Microsoft's skill uses it by default; SQLBI keeps it for advanced cases. Microsoft's skill wins. Both put its filters in an outer CALCULATETABLE: M523 (rule 33).
- Grouping with values: Microsoft's skill prefers SUMMARIZECOLUMNS; SQLBI writes ADDCOLUMNS around SUMMARIZE. Both pass; M522 reports only a column computed inside SUMMARIZE (rule 32).
- Multiplying by a test (rule 36): Microsoft's skill uses it for speed; it returns 0, which rule 7 (Microsoft Learn) avoids. Learn wins: the form is kept only for a measured gain.
- Function names: Microsoft Learn allows underscores; SQLBI's style has none and starts parameters in lower case. The style is adopted as a warning (M807); a function that keeps another style goes in section 9 with M807.
- Percent in names: SQLBI's patterns write a bare `%`; the model standard writes `(%)`. The model standard wins.
- Future dates: SQLBI's standard time pattern puts a hidden helper measure in the date table. M001 wants every measure in `_Measures`: put it there, or list it in section 9 with M001.
- Calendar-based time intelligence: Microsoft Learn recommends it, but it is a preview. The template uses the classic functions with a marked date table; calendars only with the developer's yes (owner's rule).

Not confirmed: that Power BI Desktop keeps a formula's line breaks and spaces when it saves (a re-indented formula would raise M520); that the DirectQuery time intelligence note of the best practice rules still holds (Microsoft Learn's DirectQuery guidance does not repeat it); that the "1 -" form is slower (only the best practice rules say so); SQLBI's KEEPFILTERS advice beyond what Microsoft Learn says; the speed gains of rules 35 to 38, which Microsoft's skill itself calls candidates to measure.

Checklist items: 32, 33, 34, 35
