# Calculation groups and field parameters

Part 2 of 2 of this topic. Covers: Calculation group precedence; Per-user defaults and slicers; Field parameters; Selection expressions.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### Calculation group precedence

**T11-A190-1.** An example of precedence that changes the meaning: a year-to-date item must apply before a daily-average item, so that the days are counted over the year-to-date period. A wrong order gives incorrect results that are hard to debug.
- Must. 2019. https://www.sqlbi.com/articles/understanding-calculation-group-precedence/ ; https://www.sqlbi.com/articles/avoiding-pitfalls-in-calculation-groups-precedence/
- When: Items of different groups can be active together, through several slicers or CALCULATE filters.

**T11-A190-6.** In every model with calculation groups, tune precedence values, measures and calculation items together, so that users get a smooth experience. A report measure that applies a calculation item through CALCULATE can break calculations designed with care.
- Must. 2020. https://www.sqlbi.com/articles/avoiding-pitfalls-in-calculation-groups-precedence/
- When: Any model that contains calculation groups.

**T11-A190-7.** Before adding more than one calculation group to a model, spend ample time learning in depth how the groups work and what using them implies. Several groups in one model can be extremely hard to manage.
- Must. 2020. https://www.sqlbi.com/articles/avoiding-pitfalls-in-calculation-groups-precedence/
- When: Planning a model with several calculation groups.

**T11-A162-4.** Choose the precedence of every calculation group with care while the model is being designed, and do not adjust it afterwards: a changed precedence can alter the numbers of reports already in production.
- Must. 2019. https://www.sqlbi.com/articles/understanding-calculation-group-precedence/
- When: A model with more than one calculation group, which needs distinct precedence values.

**T11-A162-5.** With several calculation groups in a model, check that calculations return the expected result for every combination of calculation items across the groups. Without that testing a wrong precedence is easy to miss.
- Should. 2019. https://www.sqlbi.com/articles/understanding-calculation-group-precedence/
- When: A model holds more than one calculation group.

### Per-user defaults and slicers

**T11-A280-3.** Narrowing slicer items per user through a selection table only helps users focus; it secures nothing. When the items must really be protected, build the model and code with security roles.
- Must. 2023. https://www.sqlbi.com/articles/filtering-calculation-items-in-a-slicer/
- When: Reducing slicer items for specific users where a security requirement also exists.

### Field parameters

**T11-A286-3.** Never read the selected entry of a field parameter's display column with SELECTEDVALUE. That column has group-by columns, where VALUES, which SELECTEDVALUE relies on, does not work. Read it with an aggregation such as MAX and handle multiple selections separately.
- Must. 2023. https://www.sqlbi.com/articles/using-field-parameters-and-calculation-groups-for-conditional-formatting/
- When: Reading the selection from the display column of a field parameter table made by Power BI.

### Selection expressions

**T11-A332-6.** Be careful when a calculation group's noSelectionExpression acts as a hidden default selection. The slicer shows nothing selected while a specific calculation runs, which can mislead users.
- Consider. Check. 2025. https://www.sqlbi.com/articles/controlling-empty-or-multiple-selections-in-calculation-groups/
- When: A noSelectionExpression is defined on a calculation group shown in a slicer.
- Version: Described as a preview in May 2025; needs compatibility level 1605.

**T11-A332-11.** Always test performance before releasing a model update that uses multipleOrEmptySelectionExpression or noSelectionExpression. They add work on top of what calculation groups already cost, which can slow every report.
- Must. Check. 2025. https://www.sqlbi.com/articles/controlling-empty-or-multiple-selections-in-calculation-groups/
- When: A model update introduces either selection expression on a calculation group.
- Version: Described as a preview in May 2025.

## Special-case techniques and facts

### Calculation group precedence

**T11-A190-3.** When one CALCULATE filters items of several calculation groups, the items are applied by the precedence of their groups, highest first, whatever the order of the filter arguments. Applying an item rewrites the expression; it is a separate step from evaluating it.
- Fact. 2020. https://www.sqlbi.com/articles/avoiding-pitfalls-in-calculation-groups-precedence/
- When: A single CALCULATE holds calculation items from more than one group.

**T11-A190-4.** Nesting CALCULATE calls that each filter a different calculation item, around one measure reference, does not let the developer choose the order of application. The precedence of the groups still decides it.
- Fact. 2020. https://www.sqlbi.com/articles/avoiding-pitfalls-in-calculation-groups-precedence/
- When: Nested CALCULATE over a single measure reference; several measure references make it far more complicated.

**T11-A190-5.** A measure whose code applies a calculation item to another measure fixes the order of application and overrides group precedence. It can return a different number than the same items chosen in a slicer or on a visual's rows or columns, where precedence orders them.
- Fact. 2020. https://www.sqlbi.com/articles/avoiding-pitfalls-in-calculation-groups-precedence/
- When: Some measures apply calculation items internally while users also select items in filters or visuals.

**T11-A162-3.** Applying calculation items only to single measures does not guarantee correct numbers when several groups are active. The item applied first rewrites the measure, and a later item rewrites only the measure references left in that code, so a wrong precedence still gives wrong results.
- Fact. 2019. https://www.sqlbi.com/articles/understanding-calculation-group-precedence/
- When: Items of several calculation groups act on one measure, also when a visual asks for a single measure.

**T11-A184-4.** Precedence is set for a whole calculation group, never for one item, and only the relative order of the values counts. The same order governs the format string expressions of calculation items, not only their value expressions.
- Fact. 2019. https://www.sqlbi.com/articles/understanding-calculation-group-precedence/ ; https://www.sqlbi.com/articles/controlling-format-strings-in-calculation-groups/
- When: A model has several calculation groups whose items change values or set format strings.

**T11-A184-5.** When an item of a higher-precedence group must know which measure is shown, and a lower-precedence group can switch the measure, read that group's selection from the filter context. Fall back to SELECTEDMEASURENAME when the switching group is unused or has no valid selection.
- Must. 2020. https://www.sqlbi.com/articles/controlling-format-strings-in-calculation-groups/
- When: Users choose the measure directly or through a measure-switching calculation group.

### Per-user defaults and slicers

**T11-A223-1.** To give each user a default selection on some columns while allowing other choices, a calculation group item can test whether the report already filters those columns. If so, it returns SELECTEDMEASURE untouched; otherwise it filters them with defaults stored for the user USERPRINCIPALNAME returns.
- Option. Check. 2021. https://www.sqlbi.com/articles/customizing-default-values-for-each-user-in-power-bi-reports/
- When: A starting selection per user, not security; row-level security serves the separate goal of blocking data.
- Version: Written in 2021, when the model had no property to set a default filter on a column.

**T11-A223-2.** A report that applies default filters per user should show a visible label that tells the user which values are currently displayed. Without it, users cannot tell they are looking at part of the data.
- Should. 2021. https://www.sqlbi.com/articles/customizing-default-values-for-each-user-in-power-bi-reports/
- When: Defaults are applied to columns when the user has made no explicit selection.

**T11-A223-3.** When one column alone needs a per-user default, store user and value pairs in a table related many-to-many to the model table, filtering towards it. The calculation item filters that table by USERPRINCIPALNAME when ISCROSSFILTERED under ALLSELECTED finds no explicit filter; otherwise it returns SELECTEDMEASURE.
- Option. 2021. https://www.sqlbi.com/articles/customizing-default-values-for-each-user-in-power-bi-reports/
- When: A single column needs a default value; the approach fails with two or more default columns.
- Version: A many-to-many cardinality relationship needs its exception row in the brief (M406).

**T11-A223-4.** In a per-user default item covering several columns, do not filter a defaults table in CALCULATE when the user has explicitly filtered its matching model column. That filter travels to the model table and hides every value absent from the defaults table, explicit choices included.
- Must. 2021. https://www.sqlbi.com/articles/customizing-default-values-for-each-user-in-power-bi-reports/
- When: Defaults tables related to model tables, with two or more default columns.

**T11-A223-5.** With exactly two default columns, a calculation item can test each column for an existing filter and use SWITCH to run CALCULATE with only the defaults tables whose columns are still unfiltered: both, one or none.
- Option. 2021. https://www.sqlbi.com/articles/customizing-default-values-for-each-user-in-power-bi-reports/
- When: Per-user defaults on two columns only; more columns multiply the branches, and it is slower than one column.

**T11-A223-6.** One CALCULATE cannot make a filter argument conditional; only the argument's content can vary. Passing every row of a table as a filter, such as ALL of it in a variable, differs from no filter: values absent from that table still vanish from related tables.
- Fact. 2021. https://www.sqlbi.com/articles/customizing-default-values-for-each-user-in-power-bi-reports/
- When: Code that tries to turn filters on and off inside a single CALCULATE.

**T11-A223-7.** For per-user defaults on any number of columns, work out in a variable, per column, the values to keep on the model column itself: all visible values when it is already filtered, otherwise the user's defaults. Apply all variables in one CALCULATE around SELECTEDMEASURE.
- Must. 2021. https://www.sqlbi.com/articles/customizing-default-values-for-each-user-in-power-bi-reports/
- When: Two or more default columns; relationships to defaults tables are no longer needed. Expect a heavy formula engine cost.
- Version: Each unrelated defaults table needs its M411 row in the brief (relationships and dates, rule 4).

**T11-A223-8.** The label that describes the values in view can be a measure which, for each column with a default, tests ISCROSSFILTERED and then either lists the visible values with CONCATENATEX or states that all values are shown.
- Option. 2021. https://www.sqlbi.com/articles/customizing-default-values-for-each-user-in-power-bi-reports/
- When: A report applies per-user default filters and shows a label of the current selection.

**T11-A223-9.** Expect per-user default filters built with a calculation group to slow reports considerably beyond one column. One column costs little, two columns are slower, and the general version leans on the formula engine and slows further with each added column.
- Consider. 2021. https://www.sqlbi.com/articles/customizing-default-values-for-each-user-in-power-bi-reports/
- When: Per-user default values implemented with a calculation group.

**T11-A280-1.** A slicer that lists too many values can be split into a hierarchy, shown as one slicer over several columns or as several single-column slicers. This fits natural hierarchies only, where each child belongs to one parent.
- Option. 2023. https://www.sqlbi.com/articles/filtering-calculation-items-in-a-slicer/
- When: A long slicer list whose values group naturally, such as countries within continents.

**T11-A280-2.** To show each user only the slicer values relevant to them when the grouping is not a natural hierarchy, build a table of allowed value and user pairs. Relate it many-to-many to the table that holds the values, filtering from the pairs table.
- Option. 2023. https://www.sqlbi.com/articles/filtering-calculation-items-in-a-slicer/
- When: A non-natural grouping, where the value column is not a key of the target table.
- Version: A many-to-many cardinality relationship needs its exception row in the brief (M406).

**T11-A280-4.** A calculation group cannot take part in a relationship. No other table can cross-filter its items, neither through a both-direction filter nor through a many-to-many relationship.
- Fact. 2023. https://www.sqlbi.com/articles/filtering-calculation-items-in-a-slicer/
- When: Trying to filter the calculation items shown in a slicer from another table.

**T11-A280-5.** To narrow a slicer of calculation items by a selection made in another table, write a measure that returns 1 when the current calculation item is among the values selected there. Apply it to the slicer as a visual filter that keeps the value 1.
- Option. 2023. https://www.sqlbi.com/articles/filtering-calculation-items-in-a-slicer/
- When: Slicer items come from a calculation group, which no relationship can filter.

### Field parameters

**T11-A248-3.** The calculated table behind a field parameter names its fields through NAMEOF. When a referenced column is renamed, the engine carries the new name into that table, as it does for any DAX formula, so the model stays stable through later renames.
- Fact. 2022. https://www.sqlbi.com/articles/fields-parameters-in-power-bi/
- When: A column referenced by a field parameter table that Power BI generated is renamed.

**T11-A248-4.** A visual driven by a field parameter sends one extra small query, to read the selected field names from the parameter table, and then the same query it would send with those fields placed directly. The feature adds no meaningful query cost.
- Fact. 2022. https://www.sqlbi.com/articles/fields-parameters-in-power-bi/
- When: Judging the speed of visuals that use field parameters.

**T11-A248-5.** Field parameters are information for the client tool, not part of the model's logic. They work only in client tools that read their metadata, and have no effect at all in a tool that cannot query through them.
- Fact. Check. 2022. https://www.sqlbi.com/articles/fields-parameters-in-power-bi/
- When: A model is also used from client tools other than Power BI.
- Version: In 2022 only Power BI used this metadata; Excel PivotTables ignored it, and later Excel support was left open.

**T11-A248-7.** Field parameters that switch the columns of a visual can be paired with a calculation group that switches the measure shown. Together they give users a highly adaptable report for little development work.
- Option. 2022. https://www.sqlbi.com/articles/fields-parameters-in-power-bi/
- When: Users should change both the slicing columns and the measure displayed.

**T11-A286-1.** When the colour of a value must change with the measure a user picks through a field parameter or a calculation group, drive the conditional formatting from a dedicated formatting measure that can detect which measure is selected.
- Must. 2023. https://www.sqlbi.com/articles/using-field-parameters-and-calculation-groups-for-conditional-formatting/
- When: Conditional formatting depends on a measure chosen through a field parameter or calculation group.

**T11-A286-2.** With a field parameter, a formatting measure can read the chosen entry from the parameter table's display column and return a colour name for it, or blank unless exactly one row is visible. The slicer's filter stays in the query, so measures see it.
- Option. 2023. https://www.sqlbi.com/articles/using-field-parameters-and-calculation-groups-for-conditional-formatting/
- When: Conditional formatting driven by the selection in a field parameter.
- Version: Theme colours only; a colour code needs an exception row (V009).

**T11-A286-6.** A calculation group can stand in for a field parameter when users choose which measure to display. Behaviour is similar, with more flexibility, because each calculation item can hold any DAX; field parameters are simpler but less flexible.
- Option. 2023. https://www.sqlbi.com/articles/using-field-parameters-and-calculation-groups-for-conditional-formatting/
- When: Letting report users choose the measure shown; field parameters do not work in Excel, for example.

### Selection expressions

**T11-A332-2.** To control what happens when several calculation items are selected together, multipleOrEmptySelectionExpression can hold, for example, an ERROR call whose own text tells the user that the combination is not allowed.
- Option. Check. 2025. https://www.sqlbi.com/articles/controlling-empty-or-multiple-selections-in-calculation-groups/
- When: A calculation group used from a slicer in which users may select several items.
- Version: Described as a preview in May 2025; compatibility level 1605; edited in the TMDL view.

**T11-A332-3.** multipleOrEmptySelectionExpression can settle a multiple selection by applying one of the selected items by a priority of your own, such as the highest ordinal, which keeps the model's item order. Write its formatStringDefinition the same way, so the format follows that item.
- Option. Check. 2025. https://www.sqlbi.com/articles/controlling-empty-or-multiple-selections-in-calculation-groups/
- When: Several items of one group are selected and a single prioritised item should apply.
- Version: Described as a preview in May 2025.

**T11-A332-4.** multipleOrEmptySelectionExpression can map given combinations of selected items to an existing item that gives the combined result, such as previous year plus year-to-date to previous year-to-date. Compare the selection with each known set and raise an error for any other.
- Option. Check. 2025. https://www.sqlbi.com/articles/controlling-empty-or-multiple-selections-in-calculation-groups/
- When: Users may select several items expecting a combined calculation; DAX has no recursion to stack them.
- Version: Described as a preview in May 2025.

**T11-A332-7.** A transformation that should reach all measures automatically, such as currency conversion, can go in the noSelectionExpression of a calculation group. It then runs whenever the group is not filtered, with no item to select in every report.
- Option. Check. 2025. https://www.sqlbi.com/articles/controlling-empty-or-multiple-selections-in-calculation-groups/
- When: A transformation is on by default for many measures; a slicer on the group then shows nothing selected.
- Version: Described as a preview in May 2025; needs compatibility level 1605.

**T11-A332-8.** Filtering any calculation item switches the noSelectionExpression off. For a hidden group that applies a default transformation there, either add an item that returns the measure unchanged, so users can turn it off, or duplicate that code so every measure is intercepted whatever is selected.
- Option. Check. 2025. https://www.sqlbi.com/articles/controlling-empty-or-multiple-selections-in-calculation-groups/
- When: A calculation group whose noSelectionExpression applies a default such as currency conversion.
- Version: Described as a preview in May 2025; needs compatibility level 1605.

**T11-A332-9.** Begin a noSelectionExpression, and its format string expression, with an ISCROSSFILTERED test on the table that triggers the transformation. The work is then skipped when the report does not use that table.
- Option. Check. 2025. https://www.sqlbi.com/articles/controlling-empty-or-multiple-selections-in-calculation-groups/
- When: The expression matters only when a given table, such as Currency, is used by the report.
- Version: Described as a preview in May 2025; needs compatibility level 1605.

**T11-A332-10.** When a default currency conversion leaves the total in the base currency with no symbol, either hide the total row of the report, or change the original measure's format string so the base currency symbol shows wherever currency is neither filtered nor grouped.
- Option. 2025. https://www.sqlbi.com/articles/controlling-empty-or-multiple-selections-in-calculation-groups/
- When: A noSelectionExpression converts amounts by currency and the report shows a total across currencies.
