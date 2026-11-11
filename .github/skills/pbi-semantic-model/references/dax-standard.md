# The DAX standard

How every DAX formula in a model built from this template is written: measures, calculated columns, calculation items, functions and role filters. `python scripts/check_project.py .` checks it; the code after each rule is the finding it gives (M5xx, M908, M909, M010). An exception passes only when section 9 of `docs/report-brief.md` lists the code and the object as the check prints it (`[Measure]`, `Table[Column]`, `calculation item 'Name'`, `function Name`), with a reason.
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
- A fixed number written directly after the sign passes: `[Total Sales] / 1000`. Here Microsoft prefers the operator, and does not want DIVIDE by a constant (no check).
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

**8. Variables.** When one expression appears twice in a formula, store it in a variable. Why: it is worked out once and the formula reads better. Checklist item 34: two or more repeats in one measure is a review point. Also break deep CALCULATE nesting into variables (Microsoft's skill; no check). Check: M507 (warn; a call of six tokens or more written twice).

```dax
VAR _UtrechtSales =
    CALCULATE (
        [Total Sales],
        Store[City] = "Utrecht"
    )
RETURN
    _UtrechtSales - _UtrechtSales * 0.1
```

Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-variables ; https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/dax-guidelines.md

**9. EARLIER and EARLIEST.** Do not use them. Store the outer value in a variable before the inner row context starts. Why: a variable is clearer and does the same. Check: M514 (warn). Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-variables

**10. Column and measure references.** Write a column with its table, `Sales[Amount]`, and a measure without one, `[Total Sales]`. Why: a measure written with its table breaks when the measure moves to another table, and a bare name then always means a measure. M010 reads measures and calculated columns. It reports a bare name that is a column, and a measure written with a table. It does not read calculation items, functions or role filters: follow the rule there too. Microsoft Learn also asks for table names on columns inside functions. This is rule 5 of the model standard. Check: M010 (warn). Source: https://learn.microsoft.com/en-us/dax/best-practices/dax-column-measure-references ; https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions ; rules DAX_COLUMNS_FULLY_QUALIFIED and DAX_MEASURES_UNQUALIFIED in the best practice rules

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
VAR _Sales = [Total Sales]
RETURN
    DIVIDE (
        _Sales - [Total Cost],
        _Sales
    )
```

Source: rule AVOID_USING_'1-(X/Y)'_SYNTAX in the best practice rules; Microsoft's skill (address in rule 8)

**16. EVALUATEANDLOG.** It is a testing aid. Remove it before the model is published. Check: M512 (warn). Source: rule EVALUATEANDLOG_SHOULD_NOT_BE_USED_IN_PRODUCTION_MODELS in the best practice rules; Microsoft's skill (address in rule 8)

**17. Time intelligence in a DirectQuery model.** When any table is DirectQuery, time intelligence functions can be slow. If visuals are slow, use columns in the date table or prior-period values prepared at the source, with plain filters. Check: M513 (warn; a measure or calculation item calls a function from the time intelligence group of the function index). Source: rule MEASURES_USING_TIME_INTELLIGENCE_AND_MODEL_IS_USING_DIRECT_QUERY in the best practice rules

**18. Names the model does not have.** Every `Table[Name]` must be a column of that table or a measure. Why: otherwise the formula returns an error. Read the table's file before you write a name. The check only sees names written with a table that exists; check bare `[Name]` references yourself. Check: M908 (fail). Source: https://learn.microsoft.com/en-us/dax/dax-syntax-reference

**19. Functions that do not exist.** Call only functions in the file `dax-functions.md` beside this one, or a user-defined function of this model. Look up a function before you use it for the first time (skill `pbi-lookup`); never invent one. Check: M909 (warn). Source: https://learn.microsoft.com/en-us/dax/dax-function-reference ; the index is built from https://learn.microsoft.com/en-us/dax/toc.json

**20. Removing filters on purpose.** Every ALL, ALLEXCEPT and REMOVEFILTERS must match the business question: which filters the measure ignores, and why. Checklist item 32 asks for 100% of them. If the brief does not say, ask the developer. Judged in the review.

- Use REMOVEFILTERS when the aim is only to clear filters inside CALCULATE (Microsoft's skill).
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
27. When an expression goes on to the next line, start that line with the operator. The only operator that may end a line is the `=` of `VAR _Name =`. M520: "start a continued line with the operator".
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
			VAR _OnlineSales =
			    CALCULATE (
			        [Total Sales],
			        Store[Store Type] = "Online"
			    )
			VAR _AllSales = [Total Sales]
			RETURN
			    DIVIDE (
			        _OnlineSales,
			        _AllSales
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

A pattern is looked up on its page before it is used (skill `pbi-lookup`), never written from memory and never pasted. Write the measure for THIS model, with its own tables and names, in this standard's style.

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

## Sources

Read on 11 November 2026. Every rule is restated in this template's own words.

- Microsoft Learn, DAX best practices: https://learn.microsoft.com/en-us/dax/best-practices/dax-error-functions ; https://learn.microsoft.com/en-us/dax/best-practices/dax-divide-function-operator ; https://learn.microsoft.com/en-us/dax/best-practices/dax-countrows ; https://learn.microsoft.com/en-us/dax/best-practices/dax-selectedvalue ; https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-avoid-filter-as-filter-argument ; https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-converting-blank ; https://learn.microsoft.com/en-us/dax/best-practices/dax-variables ; https://learn.microsoft.com/en-us/dax/best-practices/dax-column-measure-references ; https://learn.microsoft.com/en-us/dax/best-practices/dax-understand-orderby ; https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions
- Microsoft Learn, other: https://learn.microsoft.com/en-us/dax/divide-function-dax ; https://learn.microsoft.com/en-us/dax/dax-syntax-reference ; https://learn.microsoft.com/en-us/dax/dax-function-reference ; https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization ; https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-time-intelligence
- Microsoft's best practice rules (MIT), category "DAX Expressions" and the DirectQuery time intelligence rule: https://github.com/microsoft/Analysis-Services/blob/master/BestPracticeRules/BPARules.json
- Microsoft's skill `semantic-model-authoring` (MIT), DAX guidelines: https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/skills/semantic-model-authoring/references/dax-guidelines.md
- SQLBI: https://www.sqlbi.com/articles/rules-for-dax-code-formatting/ ; https://www.sqlbi.com/articles/naming-temporary-columns-in-dax/ ; https://www.sqlbi.com/articles/divide-performance/ ; https://www.sqlbi.com/articles/best-practices-for-using-keepfilters-in-dax/ ; https://www.sqlbi.com/articles/all-vs-allselected-vs-allexcept-vs-removefilters/ ; the 23 pattern pages of https://www.daxpatterns.com/ listed in section C.
- The owner's checklist, `checklist/checklist.md`, items 32 to 35.

Where sources disagree, and what was decided. Order of trust: the owner's checklist; Microsoft Learn; Microsoft's skills and best practice rules; SQLBI for DAX; then others. A lower source never overrides a higher one.

- IFERROR: Microsoft Learn says avoid it; Microsoft's skill accepts it as a single guard on one value. Learn wins: M501 warns on every use. A justified guard goes in section 9.
- `/` inside iterators: Microsoft's skill and SQLBI accept it once zero divisors are removed. Checklist item 33 asks for DIVIDE unless justified: M502 fails, and the reason goes in section 9.
- DIVIDE by a constant: Microsoft's skill says DIVIDE by default; Microsoft Learn prefers `/` for a constant. Learn wins: `/ 1000` passes.
- M010: Microsoft Learn says a measure written with its table breaks. The check only warns, because a text scanner cannot be certain (the level rule at the top of `scripts/model_rules.py`). Treat the rule as a must.
- Table quotes: SQLBI quotes only when needed; Microsoft's skill always quotes. SQLBI's rule is not adopted; no check.
- Variable names: Microsoft's skill starts them with `_`; Microsoft Learn's page on variables (https://learn.microsoft.com/dax/best-practices/dax-variables) and SQLBI write plain names. Microsoft Learn is the higher source, so the `_` prefix is not adopted (rule 31).
- SUMMARIZECOLUMNS inside a measure: Microsoft's skill uses it by default; SQLBI keeps it for advanced cases. Microsoft's skill wins. Both put its filters in an outer CALCULATETABLE. No check.
- Percent in names: SQLBI's patterns write a bare `%`; the model standard writes `(%)`. The model standard wins.
- Future dates: SQLBI's standard time pattern puts a hidden helper measure in the date table. M001 wants every measure in `_Measures`: put it there, or list it in section 9 with M001.
- Calendar-based time intelligence: Microsoft Learn recommends it, but it is a preview. The template uses the classic functions with a marked date table; calendars only with the developer's yes (owner's rule).

Not confirmed: that Power BI Desktop keeps a formula's line breaks and spaces when it saves (a re-indented formula would raise M520); that the DirectQuery time intelligence note of the best practice rules still holds (Microsoft Learn's DirectQuery guidance does not repeat it); that the "1 -" form is slower (only the best practice rules say so); SQLBI's KEEPFILTERS advice beyond what Microsoft Learn says.

Checklist items: 32, 33, 34, 35
