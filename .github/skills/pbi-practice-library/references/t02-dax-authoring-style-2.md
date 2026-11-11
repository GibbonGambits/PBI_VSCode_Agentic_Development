# DAX authoring style

Part 2 of 2 of this topic. Covers: IN operator and constructors; Data types and comparisons.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### IN operator and constructors

**T02-A096-3.** When NOT negates an IN test, put the IN condition in parentheses after NOT, although they are optional: the code reads more easily.
- Should. 2017. https://www.sqlbi.com/articles/the-in-operator-in-dax/
- When: Writing NOT in front of an IN condition.

**T02-A096-8.** In a table constructor with one column, the parentheses of a row constructor around each value can be left out. Row constructors are normally kept for lists with two or more columns.
- Option. 2017. https://www.sqlbi.com/articles/the-in-operator-in-dax/
- When: Writing a table constructor, or the left side of IN, with only one column.

**T02-A242-1.** To test one column against a list of values, write the column, IN, and a table constructor with the values, instead of equality tests joined by OR. IN does not replace OR in general: OR also combines different columns and expressions.
- Option. 2017. https://www.sqlbi.com/articles/the-in-operator-in-dax/ ; https://www.sqlbi.com/articles/understanding-the-in-operator-in-dax/
- When: A filter or condition compares a single column with a list of values.
- Version: Power BI since November 2016; Excel 2016 since Version 1701; Analysis Services after SQL Server 2016.

**T02-A242-3.** For membership checks, the IN operator can replace the CONTAINS and CONTAINSROW functions: it offers the same capability in a handier form.
- Option. 2022. https://www.sqlbi.com/articles/understanding-the-in-operator-in-dax/
- When: Testing whether a value or row is present in a table.

**T02-A242-6.** When IN compares several columns, supply a value for every column of the searched table and group the values of each row in parentheses. With a single column the parentheses are not needed.
- Must. 2022. https://www.sqlbi.com/articles/understanding-the-in-operator-in-dax/
- When: Writing an IN condition that matches more than one column.

**T02-A242-7.** For a "not in list" test, build the IN condition and negate its Boolean result with NOT placed in front of it. Putting NOT directly before the IN keyword, as SQL does, is not the DAX form.
- Must. 2017. https://www.sqlbi.com/articles/the-in-operator-in-dax/ ; https://www.sqlbi.com/articles/understanding-the-in-operator-in-dax/
- When: Testing that a value is absent from a list or table.

**T02-A242-8.** When NOT negates an IN condition, the parentheses around the IN part can be left out in most scenarios: IN has higher precedence than NOT, so NOT acts on the IN result, not on the column.
- Option. 2022. https://www.sqlbi.com/articles/understanding-the-in-operator-in-dax/
- When: Negating an IN condition with NOT.

**T02-A293-1.** A condition that combines two or more columns with OR can instead put the columns in a tuple, followed by IN and a table constructor listing the valid combinations. It mainly reads better when there are many options.
- Option. 2024. https://www.sqlbi.com/articles/using-tuple-syntax-in-dax-expressions/
- When: Conditions on combinations of values across columns, such as month and year.

**T02-A293-2.** For a filter argument of CALCULATE or CALCULATETABLE on a combination of columns, prefer TREATAS with a table constructor to a tuple with IN: it is slightly more efficient. In a small model the easier syntax may win. Older guidance wrapped such tests in FILTER.
- Should. 2024. https://www.sqlbi.com/articles/using-tuple-syntax-in-dax-expressions/ ; https://www.sqlbi.com/articles/the-in-operator-in-dax/
- When: Multi-column filter arguments of CALCULATE or CALCULATETABLE.
- Version: A tuple with IN as a direct filter argument is the 2024 view.

### Data types and comparisons

**T02-A140-1.** Use the Decimal data type, not Currency, whenever values need more than four decimal digits: Currency is stored as a 64-bit integer scaled by 10,000, so it holds only four.
- Must. 2018. https://www.sqlbi.com/articles/understanding-numeric-data-type-conversions-in-dax/
- When: Choosing a numeric type for values or calculations that need more than four decimal digits.
- Version: Power BI calls the Currency data type Fixed Decimal Number.

**T02-A140-2.** Where an expression multiplies or divides operands of different numeric types, check whether a Currency value takes part: the order of multiplications, and Currency in a division numerator, change where the conversion to Currency happens, and so the result.
- Consider. 2018. https://www.sqlbi.com/articles/understanding-numeric-data-type-conversions-in-dax/
- When: Multiplications or divisions mix Integer, Decimal and Currency operands.

**T02-A140-3.** In a chain of multiplications that includes a Currency operand, choose the operand order that fits the business requirement: a product that passes through Currency keeps four decimal digits, so the order changes the final value.
- Should. 2018. https://www.sqlbi.com/articles/understanding-numeric-data-type-conversions-in-dax/
- When: Multiplying a Currency value with Integer and Decimal values, such as price, discount and quantity.

**T02-A140-4.** Do not equate the DAX Decimal data type with the decimal or numeric types of Transact-SQL. Its SQL counterpart is Float: a DAX decimal number is always a double-precision floating-point value.
- Must. 2018. https://www.sqlbi.com/articles/understanding-numeric-data-type-conversions-in-dax/
- When: Choosing or interpreting the Decimal data type, for example against SQL data types.
- Version: The user interface calls this type Decimal Number.

**T02-A241-3.** Choose the data type of each numeric column with care: a numeric overflow inside a complex expression causes a seemingly random calculation error whose cause is very hard to find.
- Should. 2022. https://www.sqlbi.com/articles/differences-between-int-and-convert-in-dax/
- When: Setting the data type of a numeric column.

**T02-A241-4.** Watch implicit and explicit data type conversions in DAX expressions, above all with large numbers and the intermediate values of long expressions: an error they cause can look random and be very hard to trace.
- Consider. 2022. https://www.sqlbi.com/articles/differences-between-int-and-convert-in-dax/
- When: Expressions that deal with large numbers.

**T02-A273-1.** Compare floating-point (Decimal Number) values with a tolerance range, not with the = or == operators: a stored value can differ slightly from the one displayed, so results that look equal can fail an equality test.
- Should. 2023. https://www.sqlbi.com/articles/rounding-errors-with-different-data-types-in-dax/
- When: Comparisons that involve Decimal Number values.

**T02-A273-3.** Choose between Fixed Decimal Number and Decimal Number by the operations performed and the accuracy required: Fixed Decimal loses no precision up to four decimal digits while the largest aggregated value stays below 900 trillion; Decimal has a wider range but rounding differences.
- Consider. 2023. https://www.sqlbi.com/articles/rounding-errors-with-different-data-types-in-dax/
- When: Choosing the data type of numeric columns.

**T02-A273-4.** When rounding differences do not matter for a calculation, also weigh the performance cost of data type conversions when choosing data types.
- Consider. 2023. https://www.sqlbi.com/articles/rounding-errors-with-different-data-types-in-dax/
- When: Choosing numeric data types where rounding differences are not a concern.

**T02-A273-5.** Take care when multiplying Fixed Decimal Number values: two Fixed Decimals give a floating-point result with 15 significant digits, useful when more than four decimal digits are needed, while Fixed Decimal times floating point is rounded to four decimal digits.
- Consider. 2023. https://www.sqlbi.com/articles/rounding-errors-with-different-data-types-in-dax/
- When: Multiplications with at least one Fixed Decimal Number operand.

**T02-A316-1.** Be careful with iterators that multiply a Decimal (floating point) column by a Fixed Decimal column over many rows: the storage engine cannot finish that multiplication and calls back to the formula engine for each row, using much CPU.
- Consider. Check. 2024. https://www.sqlbi.com/articles/impact-of-data-types-in-dax-arithmetical-calculations/
- When: For example SUMX over a large fact table multiplying an exchange rate by quantity and price.
- Version: Engine behaviour as observed in 2024.

**T02-A316-3.** As a general practice, avoid reducing the numeric precision of values at the level of single transactions: an error introduced that early is carried forward and grows through the later multiplications and sums.
- Should. 2024. https://www.sqlbi.com/articles/impact-of-data-types-in-dax-arithmetical-calculations/
- When: General guidance; the business decides whether a precision loss is acceptable.

**T02-A316-6.** A BI developer must understand that small rounding errors build up into larger differences in large models, in order to explain such differences to users and not waste time trying to fix a number that cannot be fixed.
- Must. 2024. https://www.sqlbi.com/articles/impact-of-data-types-in-dax-arithmetical-calculations/
- When: Large models where tiny early errors grow in the final results.

## Special-case techniques and facts

### IN operator and constructors

**T02-A096-4.** To compute a value for every item of a column except the selected ones, a CALCULATE filter can negate an IN test of the column against VALUES of that column. EXCEPT of ALL and VALUES gives the same result.
- Option. Check. 2017. https://www.sqlbi.com/articles/the-in-operator-in-dax/
- When: A measure must return the result for all values other than those in the current filter.
- Version: Described in 2017.

**T02-A096-7.** A table constructor passed directly to CALCULATE as a filter does not filter any model column: the table it returns has no data lineage.
- Fact. Check. 2017. https://www.sqlbi.com/articles/the-in-operator-in-dax/
- When: Using an anonymous table as a direct filter argument of CALCULATE.
- Version: Described in 2017.

**T02-A096-10.** Values in a row constructor can be expressions that read the current filter context or row context, so the list tested with IN can be built dynamically. Reading the row context there is uncommon.
- Option. Check. 2017. https://www.sqlbi.com/articles/the-in-operator-in-dax/
- When: The values to test with IN depend on the current selection or row.
- Version: Described in 2017.

**T02-A242-2.** IN and OR are not interchangeable, even when they return the same result: IN tests whether a value belongs to a table, built by a table constructor or by functions, while OR combines Boolean conditions over different columns and expressions.
- Fact. 2022. https://www.sqlbi.com/articles/understanding-the-in-operator-in-dax/
- When: Choosing between IN and OR for a condition.

**T02-A242-4.** CONTAINS cannot be a filter argument of CALCULATE: a list-membership filter built on it needs a longer FILTER over ALL of the column, while an IN condition can be passed to CALCULATE directly.
- Fact. 2022. https://www.sqlbi.com/articles/understanding-the-in-operator-in-dax/
- When: Filtering CALCULATE by checking a column against a list of values.

**T02-A242-5.** Give CONTAINSROW a table that holds only the columns being matched, for example ALL over just those columns: it takes no column names, so a value must be supplied for every column of the table.
- Must. 2022. https://www.sqlbi.com/articles/understanding-the-in-operator-in-dax/
- When: CONTAINSROW looks for a combination of values in some columns of a wider table.

**T02-A242-9.** A CALCULATE filter that joins several AND-combinations of values from two or more columns with OR can be rewritten as a parenthesised group of those columns, IN, and a table constructor of the allowed combinations. An older view required an explicit FILTER around it.
- Option. 2022. https://www.sqlbi.com/articles/understanding-the-in-operator-in-dax/ ; https://www.sqlbi.com/articles/the-in-operator-in-dax/
- When: Filtering on combinations of values across several columns, such as brand and colour pairs.
- Version: Direct use as a CALCULATE filter is the 2022 view; a 2017 text required FILTER.

**T02-A242-10.** Comparing a single column with IN keeps the syntax simpler and gives a more efficient query plan than a multi-column test, which is why single-column use is more common.
- Fact. 2022. https://www.sqlbi.com/articles/understanding-the-in-operator-in-dax/
- When: Choosing between a single-column and a multi-column IN test.

**T02-A293-3.** Outside a filter argument, one way to test whether the evaluated transactions include one specific combination of column values is a single tuple with IN against SUMMARIZE of the fact table by those columns. TREATAS would be longer and slower here.
- Option. 2024. https://www.sqlbi.com/articles/using-tuple-syntax-in-dax-expressions/
- When: Testing one tuple only, for example in a measure that drives conditional formatting.

**T02-A293-4.** To check whether any of two or more value combinations is present, use a table constructor that lists the combinations, for example with INTERSECT against the summarized columns and ISEMPTY, not the tuple-with-IN syntax, which suits a single tuple only.
- Should. 2024. https://www.sqlbi.com/articles/using-tuple-syntax-in-dax-expressions/
- When: Tests of two or more tuples, for example for conditional formatting.

**T02-A293-5.** A tuple is not a valid result of a DAX expression: it cannot be assigned to a variable, though it can be used with the IN operator.
- Fact. 2024. https://www.sqlbi.com/articles/using-tuple-syntax-in-dax-expressions/
- When: Using tuple syntax outside a table constructor.

**T02-A293-6.** For a small table of constant values, a calculated table written as a table constructor can replace the Enter data feature. Unlike Enter data, which generates a Power Query script of constants, its rows can also hold dynamic expressions.
- Option. 2024. https://www.sqlbi.com/articles/using-tuple-syntax-in-dax-expressions/
- When: A small table with constant values, or a mix of constant and calculated values.

### Data types and comparisons

**T02-A140-5.** An arithmetic result can differ in type from its operands. Adding or subtracting: any Decimal gives Decimal, otherwise any Currency gives Currency. Multiplying: Currency by a non-Currency gives Currency, two Currencies give Decimal. Dividing gives Decimal, except Currency by Integer or Decimal, which gives Currency.
- Fact. 2018. https://www.sqlbi.com/articles/understanding-numeric-data-type-conversions-in-dax/
- When: Arithmetic over Integer, Decimal and Currency values, also when all operands share one type.

**T02-A216-1.** DAX compares text without regard to letter case: strings that differ only in case are treated as equal.
- Fact. 2021. https://www.sqlbi.com/articles/letter-case-sensitivity-in-dax-power-bi-and-analysis-services/
- When: Any comparison of text values in DAX.
- Version: Always so in Power BI and Azure Analysis Services; SQL Server Analysis Services lets setup choose a case-sensitive collation.

**T02-A216-2.** When a column receives strings that are equal apart from letter case, the engine stores them all in the casing of the variant added first, so the text shown can differ from the text supplied.
- Fact. 2021. https://www.sqlbi.com/articles/letter-case-sensitivity-in-dax-power-bi-and-analysis-services/
- When: Values are inserted into a table, for example by set functions such as UNION.

**T02-A216-3.** Give extra attention to imported text columns that hold internal codes or references in which letter case carries meaning: the engine may have mishandled such values during import.
- Must. 2021. https://www.sqlbi.com/articles/letter-case-sensitivity-in-dax-power-bi-and-analysis-services/
- When: Source codes where case matters; names of people or products are not a concern.

**T02-A216-4.** Do not choose a case-sensitive collation to keep codes that differ only in letter case apart. Handle it another way, for example with a new integer key: data exported to Power BI Desktop would meet the problem again.
- Should. 2021. https://www.sqlbi.com/articles/letter-case-sensitivity-in-dax-power-bi-and-analysis-services/
- When: Setting up an engine instance where the collation can be chosen.
- Version: Only a private SQL Server Analysis Services instance offers the collation choice, at setup.

**T02-A216-5.** Resolve data problems caused by codes whose letter case matters at the earliest possible point in the data supply chain.
- Must. 2021. https://www.sqlbi.com/articles/letter-case-sensitivity-in-dax-power-bi-and-analysis-services/
- When: Source data holds references or codes where case sensitivity matters.

**T02-A241-1.** CONVERT to INTEGER always returns the Integer data type. INT returns Integer for a floating-point (Decimal) argument but keeps a Currency (Fixed Decimal Number) argument as Currency, so the two can differ in borderline cases.
- Fact. 2022. https://www.sqlbi.com/articles/differences-between-int-and-convert-in-dax/
- When: Converting a value to an integer in DAX.
- Version: INT exists since the first DAX release; CONVERT since 2019.

**T02-A241-2.** Currency times Integer gives Currency, whose maximum is about 9.22E14; Integer times Integer stays Integer, maximum about 9.22E18. Beyond the limit the result overflows and keeps only the lowest digits that fit, and can even turn negative.
- Fact. 2022. https://www.sqlbi.com/articles/differences-between-int-and-convert-in-dax/
- When: Arithmetic that produces large numbers with a Currency (Fixed Decimal Number) operand.

**T02-A273-2.** With Decimal Number, sums and subtractions can return different results by evaluation order, so one column aggregated in different ways, such as a month value against its month-to-date value, can differ by a small fraction. Floating point keeps 15 significant digits.
- Fact. Check. 2023. https://www.sqlbi.com/articles/rounding-errors-with-different-data-types-in-dax/
- When: Aggregating Decimal Number columns, commonly with time intelligence functions.
- Version: As tested in 2023; a Fixed Decimal Number column showed no difference.

**T02-A273-6.** Integer and Fixed Decimal arithmetic wraps silently on overflow. Integer division returns floating point. Fixed Decimal times floating point returns Fixed Decimal rounded to four decimals and can raise an overflow error; Fixed Decimal times Fixed Decimal returns floating point and never does.
- Fact. 2023. https://www.sqlbi.com/articles/rounding-errors-with-different-data-types-in-dax/
- When: Arithmetic with Whole Number or Fixed Decimal Number operands, especially very large values.

**T02-A316-2.** Changing a Decimal column, such as an exchange rate, to Fixed Decimal speeds up its multiplication by Fixed Decimal values, but weigh whether the lost precision is tolerable: Fixed Decimal keeps only four decimal digits.
- Consider. 2024. https://www.sqlbi.com/articles/impact-of-data-types-in-dax-arithmetical-calculations/
- When: Whether the error is acceptable depends on the business requirements.

**T02-A316-4.** For a Decimal rate multiplied by Fixed Decimal amounts, iterate the distinct values of the rate column and multiply each by an aggregated measure, so far fewer multiplications run. Expect a larger datacache, and totals that differ from the row-by-row version through rounding.
- Should. Check. 2024. https://www.sqlbi.com/articles/impact-of-data-types-in-dax-arithmetical-calculations/
- When: The formula allows the amount to be aggregated per distinct rate value.
- Version: Engine behaviour as tested in 2024.

**T02-A316-5.** Two semantically equivalent formulas, even ones that differ only in the order of multiplications or the granularity of the iteration, can return noticeably different totals through rounding: every multiplication enlarges rounding errors already in the source values.
- Fact. 2024. https://www.sqlbi.com/articles/impact-of-data-types-in-dax-arithmetical-calculations/
- When: Calculations in large models, such as currency conversion over a large fact table.
