# DAX authoring style

Part 1 of 2 of this topic. Covers: Formatting, naming and references; Variables and their evaluation; BLANK handling and conditions.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### Formatting, naming and references

**T02-A025-1.** In a formula split over several lines, each function call should start a line of its own, with its operator in front of it.
- Should. Check. 2012. https://www.sqlbi.com/articles/rules-for-dax-code-formatting/
- When: Formatting a DAX expression that continues over several lines and contains function calls.
- Version: Formatting rules from 2012.

**T02-A025-20.** To apply the formatting rule set for DAX code (spacing, line breaks, one argument per line), one option is the website www.daxformatter.com.
- Option. Check. 2012. https://www.sqlbi.com/articles/rules-for-dax-code-formatting/
- When: DAX code is to be formatted to that rule set.
- Version: Stated in 2012; the DAX Editor tool supported the style then.

**T02-A100-3.** Repeat the name check whenever columns are added, also through a source query or a calculated table: inside a row context of the new column's table, the unqualified name is read as the column, so existing measures can break or return different numbers.
- Should. 2017. https://www.sqlbi.com/articles/duplicated-names-in-dax/
- When: Columns enter a model by a calculated column, a source query change or a calculated table change.

**T02-A100-8.** One possible convention: give the column that a measure aggregates a name unlike the measure's, such as a descriptive variant, or a leading underscore that marks it as a column to hide.
- Option. 2017. https://www.sqlbi.com/articles/duplicated-names-in-dax/
- When: A measure aggregates a column that would naturally take the same name.

**T02-A100-9.** Columns that hold the same content in different tables should have the same name; in particular, the two columns of a relationship should share one name.
- Should. 2017. https://www.sqlbi.com/articles/duplicated-names-in-dax/
- When: Naming columns that carry the same content across tables, including relationship keys.

**T02-A100-10.** Do not rely on the editor's colour highlighting to tell a measure reference from a column reference: it is not always clear, and not every editor offers it.
- Consider. Check. 2017. https://www.sqlbi.com/articles/duplicated-names-in-dax/
- When: Reading or reviewing DAX where a name could be a measure or a column.
- Version: In 2017 the Power BI formula editor showed measure references in purple.

**T02-A143-2.** When a measure needs the row-by-row product of two columns of one table, compute it with an iterator such as SUMX over that table. Do not follow the error hint and SUM each column: the product of two sums is another result.
- Should. 2019. https://www.sqlbi.com/articles/dax-error-messages-in-power-bi/
- When: A measure multiplies column references directly and raises the single-value error.

**T02-A143-3.** Do not check a column's spelling when the error says a single value for it cannot be determined: the message confirms the column exists. The cause is a missing row context for its table.
- Must. Check. 2019. https://www.sqlbi.com/articles/dax-error-messages-in-power-bi/
- When: Also when an iterator gives a row context, but over a different table.
- Version: Message wording as described in 2019.

**T02-A143-4.** Inside an iterator over one table, a column of another table that is part of the iterated table's expanded table can be read with RELATED. The error hint to add an aggregation does not apply here.
- Option. 2019. https://www.sqlbi.com/articles/dax-error-messages-in-power-bi/
- When: The single-value error names a column of a related table referenced inside an iterator.

**T02-A143-5.** When the error reports that a column is not found or is not usable in the expression, look for the right column name: the reference may be misspelled, since this message means the column exists nowhere in the model.
- Should. Check. 2019. https://www.sqlbi.com/articles/dax-error-messages-in-power-bi/
- When: A formula fails with the cannot-be-found error for a column.
- Version: Message wording as described in 2019.

**T02-A143-6.** With columns always qualified and measures never, an error about a missing object reads reliably: a message without a table name points to a missing measure, one with a table name to a missing column.
- Should. Check. 2019. https://www.sqlbi.com/articles/dax-error-messages-in-power-bi/
- When: Reading an error message about an object a formula cannot find.
- Version: Message wording as described in 2019.

**T02-A169-4.** In a temporary table too, refer to a column that carries the data lineage of a model column by its full table and column name.
- Should. 2019. https://www.sqlbi.com/articles/naming-temporary-columns-in-dax/
- When: Referencing columns of temporary tables built in DAX code.

**T02-A169-5.** Do not put the @ prefix on columns returned as the result of a DAX query: give them names that read clearly in the user interface, because a report or a calculated table consumes them.
- Should. 2019. https://www.sqlbi.com/articles/naming-temporary-columns-in-dax/
- When: Columns in the output of a DAX query.

**T02-A255-4.** When iterating a table held in a variable, prefix its model columns with the original table name: DAX has no syntax that uses the variable name as a column prefix.
- Must. 2022. https://www.sqlbi.com/articles/variables-in-dax/
- When: A table variable whose columns come from a model table.

### Variables and their evaluation

**T02-A054-1.** A VAR ... RETURN block can be written anywhere DAX accepts an expression, giving names to parts of a formula.
- Option. 2015. https://www.sqlbi.com/articles/variables-in-dax-2015/
- When: Writing any DAX expression.
- Version: Variables exist since DAX 2015.

**T02-A054-2.** A value an iteration needs from the outer filter context can be computed in a variable before the iteration, instead of inside it with CALCULATE and ALL. The variable still honours outer filters; the inner CALCULATE with ALL does not.
- Option. 2015. https://www.sqlbi.com/articles/variables-in-dax-2015/
- When: A filter condition inside an iteration compares against a value from the outer filter context.
- Version: Variables exist since DAX 2015.

**T02-A082-2.** Intermediate steps of a calculation can be written as variables instead of nested ADDCOLUMNS calls. Nesting lengthens the code and can cost a large materialization; variables keep the speed and name each step.
- Option. 2016. https://www.sqlbi.com/articles/dax-coding-style-using-variables/
- When: Each step uses the previous one, which without variables would need nested ADDCOLUMNS.
- Version: Variables: Power BI, Excel 2016, Analysis Services 2016 or later.

**T02-A082-3.** Consider a variable for a table too, such as a FILTER result that one expression repeats: it reads better and in certain conditions can also run faster. It helps most in long, complex expressions.
- Consider. 2016. https://www.sqlbi.com/articles/dax-coding-style-using-variables/
- When: The same table filter appears several times in one DAX expression.

**T02-A082-4.** Name the intermediate steps of a calculation with variables, so that the variable names document what the code does.
- Should. 2016. https://www.sqlbi.com/articles/dax-coding-style-using-variables/
- When: Writing DAX that has intermediate calculation steps.

**T02-A116-7.** Split a long or complex calculation into smaller steps and hold each intermediate result in a named variable.
- Should. 2016. https://www.sqlbi.com/articles/dax-coding-style-using-variables/ ; https://www.sqlbi.com/articles/how-to-handle-blank-in-dax-measures/
- When: Writing a long or complex DAX calculation.

**T02-A154-1.** The steps of a complex calculation can be stored in variables that hold intermediate numbers, strings or tables.
- Option. 2019. https://www.sqlbi.com/articles/table-and-column-references-using-dax-variables/
- When: A complex DAX calculation can be split into smaller steps.

**T02-A255-1.** Use variables extensively, and when unsure whether to introduce one, introduce it. Rare exception: a variable can hurt performance by forcing eager evaluation of a conditional statement.
- Should. 2022. https://www.sqlbi.com/articles/variables-in-dax/
- When: Writing any DAX expression.
- Version: Variables exist since DAX 2015.

**T02-A255-3.** Before a repeated sub-expression becomes a variable, verify that every occurrence is evaluated in the same filter context. If one sits inside a CALCULATE that changes the filters, the variable gives a wrong result.
- Must. 2022. https://www.sqlbi.com/articles/variables-in-dax/
- When: Refactoring a formula where the same sub-expression appears more than once.

**T02-A255-6.** A variable may hold a table, not only a scalar value: for example the result of TOPN, which a later step iterates.
- Option. 2022. https://www.sqlbi.com/articles/variables-in-dax/
- When: An expression computes an intermediate table that a later step iterates.

**T02-A255-8.** To debug a complex measure, return a variable's value temporarily to inspect an intermediate result, or examine the variables in a DAX debugger.
- Option. 2022. https://www.sqlbi.com/articles/variables-in-dax/
- When: Complex measures built with variables.
- Version: In 2022 the Tabular Editor 3 debugger could inspect variable values.

**T02-A313-1.** End an expression that uses variables by assigning the final computation to a variable named Result and returning only that variable: while debugging, any intermediate variable can be returned and the original restored by returning Result again.
- Should. 2024. https://www.sqlbi.com/articles/when-are-variables-evaluated-in-dax/
- When: Expressions defined with VAR and RETURN, such as measures.

**T02-A313-2.** A VAR ... RETURN block can replace any expression, including an iterator's argument, so blocks can nest. Each block needs its own RETURN; a variable can use those defined earlier in its block or an outer one; an inner name hides the same outer name.
- Option. 2022. https://www.sqlbi.com/articles/variables-in-dax/ ; https://www.sqlbi.com/articles/when-are-variables-evaluated-in-dax/
- When: Rather complex code; the usual layout is variables at the top and one RETURN.

**T02-A313-3.** Declare each variable where it gives the right value: one that holds a value for the row being iterated goes inside the iterator. Declared before the iterator it is computed once and holds the same value, such as a grand total, for every row.
- Must. 2024. https://www.sqlbi.com/articles/when-are-variables-evaluated-in-dax/
- When: Measures that combine variables with iterators such as SUMX.

**T02-A313-4.** Declare the variable that stores a repeated expression where the filter context it needs applies: inside the iterator when the value is per iterated row. Declared before the iterator, it is computed once and returns the same total for every row.
- Should. 2024. https://www.sqlbi.com/articles/when-are-variables-evaluated-in-dax/
- When: A measure referenced several times, for example inside IF, is stored in a variable.

**T02-A313-5.** A variable is worth introducing purely to give a value a name, such as a constant factor, even when it brings no performance benefit: the code reads more easily.
- Should. 2024. https://www.sqlbi.com/articles/when-are-variables-evaluated-in-dax/
- When: A formula contains a value whose meaning a name would make clear.

**T02-A313-6.** Be careful about declaring a variable inside an iteration when its value should not depend on the iterated row, such as an average over the whole table: it may mislead a reader into seeing a bug and risks being computed once per row.
- Consider. 2024. https://www.sqlbi.com/articles/when-are-variables-evaluated-in-dax/
- When: Variables declared within an iterator, for example SUMX over a customer table.

**T02-A313-7.** Treat a variable as a constant, not as an alias for its expression. To evaluate a calculation under another filter context, such as CALCULATE with dates shifted one year back, reference the measure or expression itself, not a variable that already holds its result.
- Must. 2024. https://www.sqlbi.com/articles/when-are-variables-evaluated-in-dax/
- When: A variable would be passed as the expression to evaluate in CALCULATE.

**T02-A313-8.** Assume every variable referenced anywhere in an expression is evaluated, even if the branch that uses it never runs. Do not rely on the engine dropping it in advance: that happens rarely, so variables computed but unused may cost performance.
- Must. 2024. https://www.sqlbi.com/articles/when-are-variables-evaluated-in-dax/
- When: A variable is referenced inside a conditional branch decided at run time; an unreferenced variable is never evaluated.
- Version: Static removal was seen in an Import mode example; DirectQuery code evaluates the variable.

**T02-A313-10.** When unsure whether to introduce a variable, introduce it. Do not assume variables slow a formula because they are always evaluated: cases where removing one helps are rare next to those where variables improve performance.
- Must. 2024. https://www.sqlbi.com/articles/when-are-variables-evaluated-in-dax/
- When: Deciding whether a value deserves a variable.

### BLANK handling and conditions

**T02-A068-1.** Test for blank with ISBLANK, never with an equality comparison against BLANK. In a comparison a blank is converted to zero or an empty string, so zero and empty text also match.
- Must. 2015. https://www.sqlbi.com/articles/blank-handling-in-dax/
- When: Comparing any DAX expression with blank.

**T02-A068-2.** In nested IF tests against blank, zero or an empty string, weigh the order of the tests: all three can satisfy the same comparison, so only the first matching test takes effect, and another order can even raise an error.
- Consider. 2015. https://www.sqlbi.com/articles/blank-handling-in-dax/
- When: Nested IF conditions compare an expression with BLANK, zero or an empty string.

**T02-A068-3.** When a SWITCH may receive a blank, list the BLANK comparison first: SWITCH matches a blank input to the first blank or FALSE value in its list, so an earlier FALSE would win.
- Should. 2015. https://www.sqlbi.com/articles/blank-handling-in-dax/
- When: The tested expression of SWITCH can be blank and the value list includes BLANK.

**T02-A068-4.** Add zero to a COUNTROWS result that must be a number, such as the value a SWITCH tests: COUNTROWS of an empty table returns blank, not zero, so the zero case would be missed.
- Must. 2015. https://www.sqlbi.com/articles/blank-handling-in-dax/
- When: COUNTROWS over a table that may be empty feeds a test that needs a number.

**T02-A116-1.** Do not treat BLANK as SQL NULL. Wherever part of an expression may be BLANK, follow how it flows through each operation: it does not propagate through all of them, and additions and subtractions turn it into 0.
- Consider. 2017. https://www.sqlbi.com/articles/how-to-handle-blank-in-dax-measures/
- When: An intermediate result or operand of a DAX expression can be BLANK.

**T02-A116-4.** Prefer a formula whose arithmetic already gives the right result for BLANK inputs to an IF with ISBLANK guard around it: the IF adds complexity and may be slower. More complex calculations may still need the IF.
- Should. 2017. https://www.sqlbi.com/articles/how-to-handle-blank-in-dax-measures/
- When: Handling BLANK inputs of a measure such as a ratio.

**T02-A116-5.** A measure that leaves out a BLANK-protecting IF for performance must still return the expected result in every edge case where a BLANK can occur.
- Must. 2017. https://www.sqlbi.com/articles/how-to-handle-blank-in-dax-measures/
- When: Parts of a measure can be BLANK and no IF guard is used.

**T02-A116-6.** When IF with ISBLANK is meant to detect items with no transactions, test the base measure, such as the amount, not a derived ratio variable: the ratio can be BLANK for another reason, such as no discount.
- Must. 2017. https://www.sqlbi.com/articles/how-to-handle-blank-in-dax-measures/
- When: A ratio measure is guarded by IF and ISBLANK.

**T02-A178-1.** Prefer the simplest DAX syntax that does the job. Move to a more complex equivalent only for performance, after a proper benchmark shows it is faster: small syntax differences between seemingly equal expressions can change the result.
- Should. 2019. https://www.sqlbi.com/articles/from-sql-to-dax-implementing-nullif-and-coalesce-in-dax/
- When: Choosing among alternative DAX expressions for the same logic.

**T02-A178-3.** Never assume that DIVIDE runs faster than IF or SWITCH when it replaces conditional logic: whether it is more efficient depends on several factors.
- Must. 2019. https://www.sqlbi.com/articles/from-sql-to-dax-implementing-nullif-and-coalesce-in-dax/
- When: Rewriting IF or SWITCH logic as DIVIDE for performance.

**T02-A178-4.** Replace IF or SWITCH logic with an equivalent DIVIDE expression only when the speed gain can be measured and repeats over several queries and tests, verified before production: the DIVIDE form is less readable and only sometimes faster.
- Should. 2019. https://www.sqlbi.com/articles/from-sql-to-dax-implementing-nullif-and-coalesce-in-dax/
- When: Considering DIVIDE in place of IF or SWITCH as an optimisation.

**T02-A335-1.** Use VALUES, not DISTINCT, as the default way to get the unique values of a column, and choose DISTINCT only for a reason that can be clearly explained: the blank row they may differ by can silently drop revenue or customers.
- Should. 2025. https://www.sqlbi.com/articles/choosing-between-distinct-and-values-in-dax/
- When: Retrieving the unique values of a column in a measure.

**T02-A335-3.** When an iterator such as SUMX or FILTER walks a column to compute a value that should include every contributing row, iterate VALUES of the column, not DISTINCT: DISTINCT skips the blank row and drops all unmatched many-side rows.
- Should. 2025. https://www.sqlbi.com/articles/choosing-between-distinct-and-values-in-dax/
- When: Columns at the one end of a regular relationship, when that relationship may become invalid.

## Special-case techniques and facts

### Formatting, naming and references

**T02-A100-11.** A new measure is refused when its name matches any column or measure in the model, but a new column in another table may take an existing measure's name. So a measure and a column come to share a name only when columns are added.
- Fact. 2017. https://www.sqlbi.com/articles/duplicated-names-in-dax/
- When: Adding measures or columns to a model.
- Version: In Power BI a column cannot be added to the table that holds a measure of that name.

**T02-A143-1.** The error that a single value for a column cannot be determined means the column is referenced without a row context. It does not mean too many rows are visible: it appears even for a one-row table.
- Fact. Check. 2019. https://www.sqlbi.com/articles/dax-error-messages-in-power-bi/
- When: A measure references a column directly, outside any iterator.
- Version: Message wording as described in 2019.

**T02-A154-3.** A table stored in a variable is not a new table with its own columns: a column reference that uses the variable name as table name fails with a cannot-find-table error. A reference must name a model column or a column a table function created.
- Fact. 2019. https://www.sqlbi.com/articles/table-and-column-references-using-dax-variables/
- When: Referencing columns of a table expression, such as a TOPN result, held in a variable.

**T02-A154-4.** A column added inside an expression can be referenced with an empty table name, two single quotes before the bracketed column name. This is valid DAX and keeps the reference explicit; it is usually unnecessary when the name is unique and the expression simple.
- Option. Check. 2019. https://www.sqlbi.com/articles/table-and-column-references-using-dax-variables/
- When: A column created by ADDCOLUMNS in a table variable is referenced later.
- Version: Power BI Desktop of April 2019 flagged the syntax in IntelliSense although it works.

**T02-A169-2.** A table built inside an expression can mix model columns, which take their table name, with temporary columns made by table functions. Temporary columns cannot be qualified, carry no lineage, and filter no model column unless TREATAS is applied.
- Fact. 2019. https://www.sqlbi.com/articles/naming-temporary-columns-in-dax/
- When: Expressions that build temporary tables with table functions, such as ADDCOLUMNS in a variable.

**T02-A169-6.** If a model measure's name starts with @, renaming the measure is one way to remove the clash with the @ convention for temporary columns.
- Option. 2019. https://www.sqlbi.com/articles/naming-temporary-columns-in-dax/
- When: A measure name starts with @ in code that uses @ for temporary columns.

**T02-A255-5.** A column created inside a measure, for example with ADDCOLUMNS, and held in a table variable may be referenced by its bare name, which reads better than the formally correct form with an empty table name.
- Option. 2022. https://www.sqlbi.com/articles/variables-in-dax/
- When: Only columns added inside the measure that belong to a table variable.

### Variables and their evaluation

**T02-A154-7.** When TOPN ranks rows by a measure that is needed again, for instance as the sort order in CONCATENATEX, first add the measure result as a column with ADDCOLUMNS and use that column in both places: TOPN does not keep the value it ranked by.
- Option. 2019. https://www.sqlbi.com/articles/table-and-column-references-using-dax-variables/
- When: A measure ranks rows with TOPN by a measure and reuses that measure's value.

**T02-A255-2.** A variable is a constant: it is computed once, in the filter context where it is defined. A later reference inside CALCULATE with different filters still returns that same value.
- Fact. 2022. https://www.sqlbi.com/articles/variables-in-dax/
- When: A variable is referenced inside CALCULATE or another context-changing function.

**T02-A255-7.** A table stored in a variable keeps the relationships of the base tables its columns come from, so functions that need relationships, such as RELATEDTABLE, still work while iterating it.
- Fact. 2022. https://www.sqlbi.com/articles/variables-in-dax/
- When: Iterating a table variable built from model tables.

**T02-A313-9.** A quick check of whether a variable is evaluated: make that variable raise an error, for example with ERROR. If the whole formula fails, it was evaluated; if no error appears, it was not. This is simpler than reading the query plan.
- Option. 2024. https://www.sqlbi.com/articles/when-are-variables-evaluated-in-dax/
- When: Investigating the performance cost of variables that may not be used.

### BLANK handling and conditions

**T02-A068-5.** Instead of adding zero, a SWITCH that tests a COUNTROWS result can list an explicit BLANK value, ahead of the other values, to catch an empty table.
- Option. 2015. https://www.sqlbi.com/articles/blank-handling-in-dax/
- When: SWITCH tests a COUNTROWS or other table-to-scalar result that is blank for an empty table.

**T02-A068-6.** An IF that returns a Boolean never returns blank: a BLANK in that logical expression is cast to FALSE. A column already of Boolean type that is copied into the expression keeps its blanks.
- Fact. 2015. https://www.sqlbi.com/articles/blank-handling-in-dax/
- When: IF, or SWITCH, whose result is Boolean.
- Version: Power BI, Excel 2016 and Analysis Services 2016 onward; earlier DAX versions allowed blank Boolean results.

**T02-A068-7.** In a calculated column, an IF whose two branches have different data types returns a variant, and the column raises an error. A literal BLANK branch takes the type of the other branch; a measure defined as BLANK counts as Whole Number.
- Fact. 2015. https://www.sqlbi.com/articles/blank-handling-in-dax/
- When: Defining a calculated column with IF.

**T02-A068-8.** A blank does not carry through an expression as a SQL null does: it becomes zero or an empty string, by the data type needed. Exception: as a term of a multiplication, the result stays blank.
- Fact. 2015. https://www.sqlbi.com/articles/blank-handling-in-dax/
- When: Any DAX expression that receives a blank value.

**T02-A116-2.** Addition and subtraction turn BLANK into 0, while multiplication and division keep the result BLANK. So two algebraically equal formulas can return different results when their operands can be BLANK.
- Fact. 2017. https://www.sqlbi.com/articles/how-to-handle-blank-in-dax-measures/
- When: Rewriting or reviewing arithmetic over measures that can be BLANK.

**T02-A178-2.** COALESCE can be called directly, with the same syntax as in SQL; hand-written equivalents remain relevant only for performance optimisation.
- Option. 2019. https://www.sqlbi.com/articles/from-sql-to-dax-implementing-nullif-and-coalesce-in-dax/
- When: Translating SQL COALESCE logic to DAX.
- Version: COALESCE is in DAX since early 2020; check product version support.

**T02-A178-5.** An IF with only a condition and a numeric result can be rewritten as DIVIDE with the expression as numerator and the condition as denominator: true counts as 1, false gives blank. It is less readable and only sometimes gives a better plan.
- Option. Check. 2019. https://www.sqlbi.com/articles/from-sql-to-dax-implementing-nullif-and-coalesce-in-dax/
- When: A two-argument IF with a numeric result, where a measured, consistent gain exists.
- Version: Engine behaviour as observed in 2019.

**T02-A178-6.** To reproduce SQL NULLIF in DAX, write an expression that returns blank when the two expressions are equal and the first expression otherwise, for example with variables and IF.
- Option. 2019. https://www.sqlbi.com/articles/from-sql-to-dax-implementing-nullif-and-coalesce-in-dax/
- When: Translating SQL NULLIF logic to DAX.
- Version: As of 2019 DAX had no NULLIF function.

**T02-A178-7.** A hand-written COALESCE equivalent can use SWITCH instead of nested IF tests: it reads more easily but may be less efficient. Both forms work for any data type.
- Option. Check. 2019. https://www.sqlbi.com/articles/from-sql-to-dax-implementing-nullif-and-coalesce-in-dax/
- When: Writing COALESCE logic by hand instead of calling the function.
- Version: Efficiency as observed in 2019.

**T02-A178-8.** For numeric expressions that must never return blank, consider writing COALESCE logic as a sum of each expression multiplied by ISBLANK-based flags. To keep blank when all expressions are blank, wrap the sum in DIVIDE.
- Consider. 2019. https://www.sqlbi.com/articles/from-sql-to-dax-implementing-nullif-and-coalesce-in-dax/
- When: Numeric expressions only, where a blank result is not wanted.

**T02-A178-9.** For a NULLIF equivalent, prefer the form without IF: DIVIDE the first expression by the negated equality test of the two expressions, so the result is blank when they are equal. A better plan is possible, not guaranteed.
- Should. Check. 2019. https://www.sqlbi.com/articles/from-sql-to-dax-implementing-nullif-and-coalesce-in-dax/
- When: Writing NULLIF logic in DAX, where a measured, consistent performance gain exists.
- Version: Engine behaviour as observed in 2019.

**T02-A185-3.** COALESCE runs an IF condition internally, which is why moving an IF-based blank test to COALESCE brings no speed gain by itself.
- Fact. Check. 2020. https://www.sqlbi.com/articles/the-coalesce-function-in-dax/
- When: Replacing an IF test for blank with COALESCE.
- Version: As of 2020; later engine versions might optimise COALESCE.

**T02-A243-1.** To show blank instead of zero, one approach keeps the aggregation in a variable and wraps it in IF: BLANK when the variable is zero, the variable otherwise. It is the simpler code when performance is not critical.
- Option. 2022. https://www.sqlbi.com/articles/how-to-return-blank-instead-of-zero/
- When: A measure whose zero results should appear as blank, for example so a matrix drops those rows.

**T02-A243-2.** When a measure that turns zero into blank is performance-critical, consider multiplying the variable that holds the aggregation by DIVIDE of that variable by itself, instead of IF: the factor is 1 for non-zero values and blank for zero. It is less readable.
- Consider. 2022. https://www.sqlbi.com/articles/how-to-return-blank-instead-of-zero/
- When: The measure runs inside a high-cardinality iterator or for very many rows.

**T02-A243-3.** An IF inside a measure can be costly when its condition evaluates differently from one evaluation to the next, for instance once per customer; an arithmetic version built on DIVIDE follows the same execution path every time.
- Fact. 2022. https://www.sqlbi.com/articles/how-to-return-blank-instead-of-zero/
- When: A measure with IF is evaluated many times with a varying condition.

**T02-A335-2.** With a column reference, VALUES can return one extra blank row that DISTINCT never returns: when the column is on the one-side of an invalid regular relationship, the filter context keeps that blank row, and the filtered values hold no blank already.
- Fact. 2025. https://www.sqlbi.com/articles/choosing-between-distinct-and-values-in-dax/
- When: Regular relationships only; a limited relationship never adds the blank row.

**T02-A335-4.** For statistical iterators such as MINX, MAXX, AVERAGEX or percentiles, consider iterating DISTINCT instead of VALUES, so that unmatched rows are left out: through VALUES they would form one large blank member that biases the statistic.
- Consider. 2025. https://www.sqlbi.com/articles/choosing-between-distinct-and-values-in-dax/
- When: An invalid regular relationship can produce the blank row.
