# User-defined functions in DAX

Part 1 of 1 of this topic. Covers: Naming and model-independent functions; Functions, measures and calculation groups; Parameters, types and passing modes; Calendar filters and result checks.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### Naming and model-independent functions

**T13-A344-1.** Give user-defined functions PascalCase names for this reason: built-in DAX functions are written wholly in capitals, so the casing shows at a glance which functions are your own and which are native.
- Should. 2025. https://www.sqlbi.com/articles/introducing-user-defined-functions-in-dax/
- When: Naming any user-defined function.
- Version: User-defined functions exist from the September 2025 version of DAX.

**T13-A358-6.** The full list of suffixes for reference parameters: Expr for ANYREF, Measure for MEASUREREF, Column for COLUMNREF, Table for TABLEREF, Calendar for CALENDARREF. With ANYREF the type alone tells a caller nothing about what is expected, so a consistent name has to.
- Should. 2026. https://www.sqlbi.com/articles/understanding-parameter-types-in-dax-user-defined-functions-udf/
- When: Naming a parameter declared with a reference type.

**T13-A347-2.** Keep queries or scripts that confirm each model-dependent function still works in its model: a change to a model object can break the functions that refer to it.
- Should. 2025. https://www.sqlbi.com/articles/model-dependent-and-model-independent-user-defined-functions-in-dax/
- When: Functions that name specific tables, columns or measures of the model.
- Version: User-defined functions came as a preview in September 2025. Copilot writes query or script files only when the developer asks, never inside a model folder (more model features, rules 21 and 25).

**T13-A347-3.** Write a function meant for a library, or for several models, as model-independent: it gets every table, column and measure it needs through parameters and names no model object. It then fits any model, and the caller answers for valid arguments.
- Should. 2025. https://www.sqlbi.com/articles/model-dependent-and-model-independent-user-defined-functions-in-dax/
- When: Functions written for reusable libraries, not for one model.
- Version: Functions came as a preview in September 2025.

**T13-A347-4.** After importing a model-independent function, add a model-dependent function that calls it with this model's own tables and columns. Other formulas in the model then call that wrapper with fewer parameters.
- Should. 2025. https://www.sqlbi.com/articles/model-dependent-and-model-independent-user-defined-functions-in-dax/
- When: A model-independent function has been imported into a specific model.
- Version: User-defined functions came as a preview in September 2025.

**T13-A347-6.** To make a function model-independent, every column and measure reference in its body must become an EXPR parameter, including the columns it expects in a table argument. Any reference left behind is a dependency that makes reuse harder.
- Must. 2025. https://www.sqlbi.com/articles/model-dependent-and-model-independent-user-defined-functions-in-dax/
- When: Converting a function that relies on specific columns or measures into a model-independent one.
- Version: User-defined functions came as a preview in September 2025.

**T13-A347-7.** Naming details: `Local.` also keeps a model's functions from clashing with DAX functions added later; add a company prefix when the company shares several libraries; no part of a dotted name may be `Dax` or another DAX keyword; EXPR suffixes include Table, Expr and Calendar.
- Should. Check. 2025. https://www.sqlbi.com/articles/model-dependent-and-model-independent-user-defined-functions-in-dax/
- When: Naming user-defined functions and their parameters.
- Version: DAX keywords are those the DISCOVER_KEYWORDS view lists. Stated for the 2025 preview; may have changed.

**T13-A347-9.** A model-independent function must not call a model-dependent function, nor refer, directly or indirectly, to specific tables, columns, calendars or measures. It may call other model-independent functions. Any such reference, however indirect, makes the function model-dependent itself.
- Must. 2025. https://www.sqlbi.com/articles/model-dependent-and-model-independent-user-defined-functions-in-dax/
- When: Writing or reviewing a function meant to be model-independent.
- Version: User-defined functions came as a preview in September 2025.

**T13-A354-1.** One way to make measure or calculated-table logic reusable: put all the business logic in a model-independent function whose tables and columns are parameters, and add a small `Local.` function that only maps this model's objects onto them. Later optimisations are then made once.
- Option. 2026. https://www.sqlbi.com/articles/creating-functions-for-the-like-for-like-dax-pattern/
- When: Logic, such as a published pattern, that otherwise needs manual adapting to each model's names.
- Version: This template suggests a function at the end of a task and builds it after the developer's yes (native features; U001).

**T13-A354-2.** A model-independent function must not name a measure: measure names belong to one specific model. Pass the calculation to evaluate as an argument instead.
- Must. 2026. https://www.sqlbi.com/articles/creating-functions-for-the-like-for-like-dax-pattern/
- When: A model-independent function whose logic evaluates a measure.

**T13-A354-3.** When the logic of a model-independent function is not tied to one kind of entity, it can use neutral names and values, such as Active and Inactive in place of Open and Closed, so that it fits any entity. More generic means more reusable.
- Option. 2026. https://www.sqlbi.com/articles/creating-functions-for-the-like-for-like-dax-pattern/
- When: The only entity-specific parts of the logic are table and column names that are already parameters.

**T13-A354-4.** Once a calculation developed in a measure gives the right result, ask whether its logic should be made more generic for reuse elsewhere, and whether it then belongs in a model-dependent or a model-independent function. Some code gains nothing from this.
- Should. 2026. https://www.sqlbi.com/articles/creating-functions-for-the-like-for-like-dax-pattern/
- When: A calculation was first built and debugged in a measure.
- Version: This template suggests a function at the end of a task and builds it after the developer's yes (native features; U001).

### Functions, measures and calculation groups

**T13-A344-10.** User-defined functions can break a model's DAX into small pieces that are tested and debugged on their own. Once checked and tuned, each piece serves as a building block, which makes the whole project sturdier.
- Option. 2025. https://www.sqlbi.com/articles/introducing-user-defined-functions-in-dax/
- When: Organising the DAX code of a semantic model.
- Version: User-defined functions exist from the September 2025 version of DAX. This template suggests a function at the end of a task and builds it after the developer's yes (native features; U001).

**T13-A355-1.** Decide between a measure and a calculation group by what report users must see and interact with. How the underlying logic is shared is a separate, internal decision; user-defined functions are one tool for it, and they only help the developer organise code.
- Should. 2026. https://www.sqlbi.com/articles/dax-user-defined-functions-udf-vs-calculation-groups/
- When: Deciding how to expose a calculation to report users and how to share its logic.

**T13-A355-2.** Use a calculation group when report users need one choice, for example in a single slicer, that changes all measures in a visual alike: a shared filter such as the period to analyse, or a shared transformation such as scaling to thousands or millions.
- Should. 2026. https://www.sqlbi.com/articles/dax-user-defined-functions-udf-vs-calculation-groups/
- When: The same filter or transformation must apply to every measure, without distinction.

**T13-A355-3.** Do not use a calculation group as the way to share code between calculations: share it through user-defined functions with explicit parameters. A calculation group has no parameters, so shared code gets its input through a changed filter context, which can add query-time work.
- Should. 2026. https://www.sqlbi.com/articles/dax-user-defined-functions-udf-vs-calculation-groups/
- When: Sharing logic between calculations; the cost grows with complex logic and repeated calls in one query.
- Version: Before user-defined functions, calculation groups were the only way to share logic; their arrival is a reason to revisit that. This template suggests a function at the end of a task and builds it after the developer's yes (native features; U001).

**T13-A355-4.** Besides a repeated formula, a function suits business logic that is complex enough to deserve one definition, or whose parameters may vary. Calculation items, like measures, call the function and pass the fitting parameters.
- Should. 2026. https://www.sqlbi.com/articles/dax-user-defined-functions-udf-vs-calculation-groups/
- When: Business logic that is complex, takes varying parameters, or is applied in several places.
- Version: Without a repeated formula, this template builds a function only when the developer asks (native features; U001).

**T13-A355-5.** Do not wrap a simple calculation, such as a plain SUM or a straightforward subtraction, in a user-defined function: write it in the measure. The function adds nothing there and hides the calculation, which makes it harder to read.
- Should. 2026. https://www.sqlbi.com/articles/dax-user-defined-functions-udf-vs-calculation-groups/
- When: Simple calculations; a simple period calculation item may not need a function of its own either.

### Parameters, types and passing modes

**T13-A344-4.** Write the passing mode of every parameter of a user-defined function, VAL included, although VAL is what applies when no mode is written.
- Should. 2025. https://www.sqlbi.com/articles/introducing-user-defined-functions-in-dax/
- When: Declaring the parameters of a user-defined function.
- Version: User-defined functions exist from the September 2025 version of DAX.

**T13-A344-5.** A parameter must also be EXPR when an iterator in the body has to work the argument out again for each row. A VAL argument is computed before the call, so no context set in the body changes it; such glitches are hard to debug.
- Must. 2025. https://www.sqlbi.com/articles/introducing-user-defined-functions-in-dax/
- When: The body re-evaluates the argument under a filter context or row context that the body itself sets.
- Version: User-defined functions exist from the September 2025 version of DAX.

**T13-A344-9.** Make a function's body as efficient as you can: for example, work an EXPR argument out once per row and keep the results in a variable, not again in every iteration. Many measures and functions call it, so its speed weighs on the whole model.
- Should. 2025. https://www.sqlbi.com/articles/introducing-user-defined-functions-in-dax/
- When: Writing the body of a user-defined function, above all one that uses EXPR parameters in iterations.
- Version: User-defined functions exist from the September 2025 version of DAX.

**T13-A358-1.** For a reference parameter, choose the narrowest type that fits: MEASUREREF for a measure, COLUMNREF for a column, TABLEREF for a model table, CALENDARREF for a calendar. Keep ANYREF for a parameter that must accept any expression. Narrow types let engine and editors validate arguments.
- Should. 2026. https://www.sqlbi.com/articles/understanding-parameter-types-in-dax-user-defined-functions-udf/
- When: Writing or reviewing a parameter that receives a model object or an expression.
- Version: MEASUREREF, COLUMNREF, TABLEREF and CALENDARREF date from March 2026.

**T13-A358-2.** Do not pair the ANYVAL type with the EXPR passing mode on a parameter: the combination can confuse. ANYVAL is fine as the type of a VAL parameter that accepts any data type.
- Should. 2026. https://www.sqlbi.com/articles/understanding-parameter-types-in-dax-user-defined-functions-udf/
- When: Declaring a parameter with the ANYVAL type.

**T13-A358-4.** Inside the body, wrap an EXPR parameter in CALCULATE wherever the logic needs a context transition, such as in an iterator; do not count on callers to do it. The result is then right for a measure and for a plain formula alike.
- Should. 2025. https://www.sqlbi.com/articles/introducing-user-defined-functions-in-dax/ ; https://www.sqlbi.com/articles/understanding-parameter-types-in-dax-user-defined-functions-udf/
- When: EXPR or ANYREF parameters evaluated in a row context. Harmless for measure arguments; rules out column references as arguments.

**T13-A358-8.** When a function needs a column and the table that holds it, take only the column as a parameter and get its table with TABLEOF, wherever possible. The signature then has fewer parameters.
- Should. 2026. https://www.sqlbi.com/articles/understanding-parameter-types-in-dax-user-defined-functions-udf/
- When: A function receives a column reference and also needs the table where that column is defined.

**T13-A358-9.** For a table parameter, consider TABLE EXPR over TABLEREF: callers may then pass any table expression. Keep TABLEREF when the function must be sure of a real model table with all its columns and relationships, for instance to give it to ISFILTERED or ISCROSSFILTERED.
- Consider. 2026. https://www.sqlbi.com/articles/understanding-parameter-types-in-dax-user-defined-functions-udf/
- When: Choosing the type of a table parameter of a user-defined function.

**T13-A364-1.** Once one parameter has a default value, make every parameter after it optional too. DAX itself allows an optional parameter to be followed by a mandatory one, yet each caller must then write an empty argument position to reach it, which makes every call awkward.
- Should. 2026. https://www.sqlbi.com/articles/optional-parameters-in-dax-user-defined-functions/
- When: Defining optional parameters in a user-defined function.
- Version: Optional parameters with defaults were announced when user-defined functions became generally available.

## Special-case techniques and facts

### Naming and model-independent functions

**T13-A358-7.** To free a function from one model, the columns it needs can arrive as COLUMNREF parameters that the caller supplies, not as names written in the body. Hard-coded column names tie it to one model structure; with parameters, every model dependency is exposed.
- Option. 2026. https://www.sqlbi.com/articles/understanding-parameter-types-in-dax-user-defined-functions-udf/
- When: A function meant for reuse across semantic models whose tables and columns are named differently.

**T13-A347-1.** A model-dependent function, one that names specific columns, tables or measures, works in another model only when every object it names exists there too. The function itself does not declare which objects it needs.
- Fact. Check. 2025. https://www.sqlbi.com/articles/model-dependent-and-model-independent-user-defined-functions-in-dax/
- When: Copying a model-dependent function from one semantic model to another.
- Version: In the 2025 preview, editing tools did not check these dependencies before a paste; may have changed.

**T13-A347-5.** A function that reads named columns of a table parameter depends on that table's structure and fails when they are missing. It counts as model-dependent although it names no model object. DAX has no keyword for this requirement: only a comment can state it.
- Fact. 2025. https://www.sqlbi.com/articles/model-dependent-and-model-independent-user-defined-functions-in-dax/
- When: A function has a table parameter and its body refers to specific column names.
- Version: User-defined functions came as a preview in September 2025.

### Functions, measures and calculation groups

**T13-A355-6.** To show measures with and without a business-logic filter side by side in one visual, standalone measures can call the function that holds the logic. A calculation group alone cannot do it: the selected item changes every measure in the visual.
- Option. 2026. https://www.sqlbi.com/articles/dax-user-defined-functions-udf-vs-calculation-groups/
- When: A visual shows, for example, sales for new customers beside measures without that segmentation.

### Parameters, types and passing modes

**T13-A344-2.** Each argument of a typed parameter is converted on its own, before the body runs, and with no error. Two decimals given to whole-number parameters become whole numbers first, so their sum can differ from the rounded total. This can confuse.
- Fact. 2025. https://www.sqlbi.com/articles/introducing-user-defined-functions-in-dax/
- When: A parameter is declared with a specific data type, such as a whole-number type.
- Version: User-defined functions exist from the September 2025 version of DAX.

**T13-A344-7.** Reading an EXPR parameter does not by itself trigger a context transition. A measure passed as the argument transitions through its implicit CALCULATE; an equivalent plain formula, such as a SUMX expression, ignores the row context of the body's iterators and can return nothing.
- Fact. 2025. https://www.sqlbi.com/articles/introducing-user-defined-functions-in-dax/
- When: An EXPR parameter is evaluated inside an iterator in the function body.
- Version: User-defined functions exist from the September 2025 version of DAX.

**T13-A358-3.** An ANYREF parameter is not limited to references to objects that exist in the model: any DAX formula can be its argument. It is passed in EXPR mode whether EXPR is written or not.
- Fact. 2026. https://www.sqlbi.com/articles/understanding-parameter-types-in-dax-user-defined-functions-udf/
- When: Designing or calling a function that declares an ANYREF parameter.

**T13-A358-5.** A MEASUREREF parameter accepts only a measure of the model, so evaluating it in a row context always performs a context transition. An explicit CALCULATE around it is not needed for that, though it does no harm.
- Fact. 2026. https://www.sqlbi.com/articles/understanding-parameter-types-in-dax-user-defined-functions-udf/
- When: A MEASUREREF parameter is used inside an iterator or another row context.

**T13-A358-10.** When a function's body assumes several COLUMNREF arguments belong to one table, columns from different tables give a misleading error that is hard to interpret. The body's own code that combines the columns, such as SUMX, raises it: the function does not validate its arguments.
- Fact. Check. 2026. https://www.sqlbi.com/articles/understanding-parameter-types-in-dax-user-defined-functions-udf/
- When: A function has two or more COLUMNREF parameters that must come from the same table.

**T13-A358-11.** A function with several COLUMNREF parameters can test that all come from one table: take TABLEOF of each column, compare the NAMEOF results, and raise its own message with ERROR when they differ. A specific message is easier to read than the default error.
- Option. Check. 2026. https://www.sqlbi.com/articles/understanding-parameter-types-in-dax-user-defined-functions-udf/
- When: The function's logic needs several column arguments to belong to one table.
- Version: In the preview implementation the engine's own error came first, so the custom message did not yet appear.

**T13-A364-2.** An optional parameter in the middle can be skipped by leaving its place empty between two commas while a later argument is still given. It is valid, though not pleasant to read. Optional arguments at the end are simply left out.
- Option. 2026. https://www.sqlbi.com/articles/optional-parameters-in-dax-user-defined-functions/
- When: The caller wants to set only a later one of several optional parameters.

**T13-A364-3.** The default expression of an optional parameter cannot refer to another parameter of the same function. It must respect the parameter's type hints, runs only for calls that omit the argument, and may use built-in and user-defined functions.
- Fact. 2026. https://www.sqlbi.com/articles/optional-parameters-in-dax-user-defined-functions/
- When: Writing the default expression of an optional parameter.

**T13-A364-4.** To make a function behave differently when an optional argument is given or not, set the parameter's default to BLANK and test it with ISBLANK in the body.
- Option. 2026. https://www.sqlbi.com/articles/optional-parameters-in-dax-user-defined-functions/
- When: No sensible fixed default exists, typically when the choice is to apply a step or skip it.

**T13-A364-5.** Where a blank default is used to detect a missing optional argument, remember that an argument passed explicitly as blank is treated exactly like one left out: the function cannot tell the two apart.
- Consider. 2026. https://www.sqlbi.com/articles/optional-parameters-in-dax-user-defined-functions/
- When: Blank is a legitimate value a caller may want to pass; rarely a problem in practice.

### Calendar filters and result checks

**T13-A363-1.** The body of a user-defined function may be a CALCULATE modifier such as REMOVEFILTERS, not a scalar or a table: a call is expanded in place, so code that is invalid alone works in the right spot.
- Option. 2026. https://www.sqlbi.com/articles/using-removefilters-in-dax-user-defined-functions/
- When: Only when every call is a filter argument of CALCULATE; anywhere else it fails.

**T13-A363-2.** The filter-keep columns of a calendar whose filters must be cleared can be listed in one user-defined function that removes those filters with REMOVEFILTERS. The list, which may grow as the model develops, is then kept in a single place.
- Option. 2026. https://www.sqlbi.com/articles/using-removefilters-in-dax-user-defined-functions/
- When: A date table has extra columns, such as weekday names, that are neither calendar levels nor time-related columns.
- Version: Calendar-based time intelligence is a preview feature here: it needs the developer's yes. This template suggests a function at the end of a task and builds it after the developer's yes (native features; U001).

**T13-A363-3.** In place of a function that yields only a REMOVEFILTERS modifier, a function can take the calculation as an EXPR parameter and evaluate it inside its own CALCULATE, together with the filter removal.
- Option. 2026. https://www.sqlbi.com/articles/using-removefilters-in-dax-user-defined-functions/
- When: A function must clear a fixed set of filters around a calculation, such as a calendar's filter-keep columns.
- Version: Where the columns belong to a calendar: a preview feature here, which needs the developer's yes.

**T13-A363-4.** A measure that takes the last visible date as reference date for DATESINPERIOD with ENDALIGNED on a calendar must clear the filters on the calendar's filter-keep columns, such as weekday name and number, while computing that date. Otherwise the period can spill into later months.
- Must. 2026. https://www.sqlbi.com/articles/using-removefilters-in-dax-user-defined-functions/
- When: Calendar-based measures that must stay right under filters on filter-keep columns; built-in functions already handle these.
- Version: Calendar-based time intelligence is a preview feature here: it needs the developer's yes.

**T13-A363-5.** A measure can be checked for a time with two visual calculations: one works out the same figure as the measure, the other flags rows where the two differ. Remove both once verified. A flag makes wrong values easy to spot among many rows.
- Option. 2026. https://www.sqlbi.com/articles/using-removefilters-in-dax-user-defined-functions/
- When: Debugging a measure in a report visual; compare only at levels where both techniques should agree.

**T13-A363-6.** In a visual calculation, RANGE counts the current row as part of the range: a window of the last three rows therefore takes a step of -2, not -3.
- Fact. 2026. https://www.sqlbi.com/articles/using-removefilters-in-dax-user-defined-functions/
- When: A visual calculation uses RANGE with the current row included.
