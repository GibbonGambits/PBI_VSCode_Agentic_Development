# Calculation groups and field parameters

Part 1 of 2 of this topic. Covers: Calculation group design patterns; Calculation item application; Format string expressions.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail. A note may name a tool, a website or a custom visual that this template does not use, or describe publishing, deploying or changing a deployed model: that is information for the developer. You do not install, call or suggest such a tool, and nothing is published or deployed from this template.

## General practice

### Calculation group design patterns

**T11-A159-1.** A calculation group suits variations that are simple variants of one shared pattern, as time intelligence is for a set of base measures. The design gets hard to keep right once a model holds several groups, or measures use calculation items in their own code.
- Option. Check. 2019. https://www.sqlbi.com/articles/introducing-calculation-groups/
- When: Many base measures each need the same recurring variations, such as year-to-date.
- Version: Needs compatibility level 1470; in June 2019 only Analysis Services offered it.

**T11-A201-9.** Consider a calculation group, applied through CALCULATE inside measures, to carry a report parameter into measures in place of IF or SWITCH logic. The variants then live in one separate place that is easy to maintain and extend, and the measure's code stays unchanged.
- Consider. 2020. https://www.sqlbi.com/articles/using-calculation-groups-to-selectively-replace-measures-in-dax-expressions/
- When: A report parameter selects between calculation logics for a measure; measure the speed, it can go either way.

**T11-A201-10.** Measure the speed of a calculation group solution; never assume it beats IF or SWITCH logic. Test several solutions and give users the best one for that model, because the outcome depends on other details of the model.
- Must. 2020. https://www.sqlbi.com/articles/using-calculation-groups-to-selectively-replace-measures-in-dax-expressions/
- When: Choosing between a calculation group and IF or SWITCH logic; larger, complex models may favour the group.

**T11-A207-1.** Never add up values recorded in different units of measure, such as weights held in ounces, pounds and grams. The total has no meaning.
- Must. 2020. https://www.sqlbi.com/articles/dynamic-format-strings-with-calculation-groups/
- When: Each row stores a value together with its own unit of measure.

**T11-A240-1.** A calculation group can be written and shared as a DAX script, which holds every expression and property of the group in one readable place. Tabular Editor can generate the script from an existing group with its Script DAX command.
- Option. Check. 2022. https://www.sqlbi.com/articles/scripting-syntax-for-calculation-groups/
- When: Reading, copying or sharing the full definition of a calculation group.
- Version: DAX script syntax for calculation groups arrived with Tabular Editor 3; in 2019 no text form existed.

**T11-A240-2.** A calculation group in DAX script starts with CALCULATIONGROUP, the group name and its column name, then optional Description, Visible and Precedence. Each CALCULATIONITEM has a quoted name, `=` and its expression, then optional Description, Ordinal and FormatString; without FormatString the measure's format stays.
- Option. 2022. https://www.sqlbi.com/articles/scripting-syntax-for-calculation-groups/
- When: Writing a calculation group as a DAX script in a tool that supports that syntax.
- Version: Script syntax of an external tool, not TMDL: this template writes calculation groups in TMDL from the shipped example.

**T11-A268-5.** Do not assume a published speed comparison holds for your model. Repeat the measurements on your own system before choosing between a calculation group and a period bridge table; results reflect one model and its data distribution.
- Must. 2023. https://www.sqlbi.com/articles/using-calculation-groups-or-many-to-many-relationships-for-time-intelligence-selection/
- When: Choosing between a calculation group and a both-direction period bridge table.

### Calculation item application

**T11-A159-5.** Inside a calculation item, test the current measure with ISSELECTEDMEASURE, not by comparing SELECTEDMEASURENAME with a text. A mistyped name gives an error with the first and a silent FALSE with the second, and only ISSELECTEDMEASURE follows a renamed measure.
- Should. 2019. https://www.sqlbi.com/articles/introducing-calculation-groups/
- When: An item's logic depends on the measure evaluated; a measure list kept outside DAX is the exception.

**T11-A160-6.** To understand what a calculation item does in a formula, rewrite the formula by hand with the item applied and write out in full the code the engine will run. Expanding it this way shows exactly what happens inside the engine.
- Should. 2019. https://www.sqlbi.com/articles/understanding-calculation-groups/
- When: Reasoning about any formula that a calculation item is applied to.

**T11-A161-1.** When CALCULATE filters a calculation item, make its first argument one measure reference, never a compound expression. Put logic over several measures in a measure of its own first. A second view accepts very simple expressions, at the price of extra thought.
- Must. 2019. https://www.sqlbi.com/articles/understanding-calculation-groups/ ; https://www.sqlbi.com/articles/understanding-the-application-of-calculation-items/
- When: DAX a developer writes with a calculation item as a CALCULATE filter; visuals already query single measures.

**T11-A340-1.** Keep sideways recursion, a calculation item that invokes another item of its own group, to a minimum, and accept some repeated code in return. Such expressions become hard to read and tend to return results that were not expected.
- Should. 2025. https://www.sqlbi.com/articles/sideways-recursion-in-dax-calculation-groups/
- When: Writing calculation items; hidden groups managed only by code are the safe case.

**T11-A340-5.** Be aware that a recursion loop can arise even when calculation items never name each other, for example when items reference measures that themselves filter a calculation item of the same group. The items then reach each other through the measures.
- Consider. 2025. https://www.sqlbi.com/articles/sideways-recursion-in-dax-calculation-groups/
- When: Measures that filter a calculation item are referenced from items of that same group.

### Format string expressions

**T11-A160-1.** A calculation item with no format string expression shows its result in the format of the underlying measure, so a ratio appears as 0.12 and not 12%. Give the item a format of its own when it changes the nature of the result.
- Should. 2019. https://www.sqlbi.com/articles/understanding-calculation-groups/
- When: An item turns an amount into a percentage; a difference in the same unit can keep the measure's format.

**T11-A184-1.** A calculation item whose formula changes how a measure's number must be read needs a format string expression, so the format shown follows the changed result. Not every visual fully honours such formats: custom visuals are affected, and others can be.
- Must. Check. 2020. https://www.sqlbi.com/articles/controlling-format-strings-in-calculation-groups/
- When: A calculation item changes the numeric representation of the measures it is applied to.
- Version: The visual limitation was reported as still unfixed in October 2021; check current behaviour.

## Special-case techniques and facts

### Calculation group design patterns

**T11-A159-3.** To let report users choose which measure a visual shows, a calculation group can hold items that each return one named measure and never call SELECTEDMEASURE. Such an item replaces the measure in the visual; it does not vary it.
- Option. 2019. https://www.sqlbi.com/articles/introducing-calculation-groups/
- When: Users pick the metric in a slicer; with a second group for time variants, precedence sets the order.

**T11-A201-5.** When a calculation item must change one measure wherever other measures reference it, hide the calculation group and never let report users select it directly. A group placed in a report is applied at the top level, to the queried measure, not the inner reference.
- Must. 2020. https://www.sqlbi.com/articles/using-calculation-groups-to-selectively-replace-measures-in-dax-expressions/
- When: Replacing one measure inside other measures; hiding gives a smooth experience but cannot stop deliberate misuse.

**T11-A201-6.** To let a slicer switch one measure's implementation while other measures build on it, move its code to a hidden measure. The public measure evaluates it in CALCULATE, filtering a hidden calculation group through TREATAS with values selected in a visible copy of its items.
- Should. 2020. https://www.sqlbi.com/articles/using-calculation-groups-to-selectively-replace-measures-in-dax-expressions/
- When: One measure's implementation must switch from a slicer while measures that reference it keep working.

**T11-A201-7.** A disconnected table that users slice in place of a hidden calculation group must hold exactly the same values as that group. A calculated table built from the columns of the calculation group is one way to make it.
- Must. 2020. https://www.sqlbi.com/articles/using-calculation-groups-to-selectively-replace-measures-in-dax-expressions/
- When: A hidden calculation group is applied inside a measure from the selection in a visible disconnected table.

**T11-A201-8.** The items of a calculation group that is hidden and applied only from inside chosen measures can leave out their tests on the selected measure, which makes them faster. The developer controls every place the group is applied, so the safety tests are not needed.
- Option. 2020. https://www.sqlbi.com/articles/using-calculation-groups-to-selectively-replace-measures-in-dax-expressions/
- When: Only an internal group applied through CALCULATE in chosen measures, never one that users select.

**T11-A207-2.** For a measure over values stored in mixed units, one possibility is to return a result only when the filter context holds a single unit of measure, and nothing otherwise.
- Option. 2020. https://www.sqlbi.com/articles/dynamic-format-strings-with-calculation-groups/
- When: Each row stores a value together with its own unit of measure.

**T11-A207-6.** To show totals over values held in mixed units, a calculation group can offer one item per reporting unit. Each item computes the measure per source unit, multiplies it by a conversion factor from a small factor table, and sums the results.
- Option. 2020. https://www.sqlbi.com/articles/dynamic-format-strings-with-calculation-groups/
- When: Rows store a value with its own unit, and users want to choose the reporting unit.

**T11-A210-3.** To let report users choose which date drives the numbers, a calculation group can hold one item per relationship to the Date table. The item for the active relationship returns SELECTEDMEASURE unchanged; each other item evaluates it in CALCULATE with USERELATIONSHIP.
- Option. Check. 2020. https://www.sqlbi.com/articles/using-calculation-groups-to-switch-between-dates/
- When: Several relationships between a fact table and Date, one active; with no selection the active one applies.

**T11-A268-1.** To let users pick relative periods such as last month, previous month or last six months, a calculation group can hold one item per period. Each item evaluates SELECTEDMEASURE under a date filter whose bounds come from the latest date in the fact table.
- Option. 2023. https://www.sqlbi.com/articles/using-calculation-groups-or-many-to-many-relationships-for-time-intelligence-selection/
- When: Users compare relative time periods; bounds taken from fact data stay current after each refresh.

**T11-A268-3.** Choosing between a calculation group and a period bridge table for selecting time periods, weigh flexibility against effort. The group defines periods freely but needs new DAX and a deployment per period; the bridge table needs one configuration row, if the period fits its grain.
- Consider. 2023. https://www.sqlbi.com/articles/using-calculation-groups-or-many-to-many-relationships-for-time-intelligence-selection/
- When: Deciding how to implement relative time periods that users select.
- Version: The bridge rests on a both-direction relationship: it needs its reason and exception row in the brief (M405; checklist item 12).

**T11-A268-4.** In tests on a large model, a period bridge table with a both-direction relationship beat a calculation group for additive measures: one storage engine query against one small query per item driven by the formula engine. Small models and distinct counts performed about the same.
- Fact. 2023. https://www.sqlbi.com/articles/using-calculation-groups-or-many-to-many-relationships-for-time-intelligence-selection/
- When: Relative period selection; both-direction filters are usually slow, but this bridge holds only a few hundred rows.
- Version: A both-direction relationship needs its reason and its exception row in the brief (M405; checklist item 12).

**T11-A286-5.** To tell a formatting measure which calculation item is selected, add a disconnected calculated table of item names. Each item, when ISSELECTEDMEASURE finds the formatting measure, evaluates it with a filter on its own name in that table; the measure reads the name with SELECTEDVALUE.
- Option. 2023. https://www.sqlbi.com/articles/using-field-parameters-and-calculation-groups-for-conditional-formatting/
- When: Conditional formatting or other logic must change with the calculation item selected.

### Calculation item application

**T11-A159-4.** When a calculation item makes no sense for some measures, its formula can test which measure is being evaluated, with ISSELECTEDMEASURE or SELECTEDMEASURENAME, and act only where it fits. Without such a test the item acts on every measure.
- Option. 2019. https://www.sqlbi.com/articles/introducing-calculation-groups/
- When: The variation an item computes is not meaningful for every measure of the model.

**T11-A159-6.** Consider SELECTEDMEASURENAME in a calculation item whose behaviour must follow settings kept outside the DAX code, such as a table that lists the measures a behaviour is switched on for. The settings can then change with no edit to the formula.
- Consider. 2019. https://www.sqlbi.com/articles/introducing-calculation-groups/
- When: An item must transform results according to configuration stored outside its formula.

**T11-A161-2.** A calculation item filtered by an outer CALCULATE is not applied at that level to a measure inside a nested CALCULATE. Its filter stays active, and the item rewrites the inner measure reference in the inner filter context, where inner filters can override outer ones.
- Fact. 2019. https://www.sqlbi.com/articles/understanding-the-application-of-calculation-items/
- When: An outer CALCULATE filters a calculation item and no inner CALCULATE changes the filter on that group.

**T11-A190-2.** A calculation item works only by rewriting measure references. An expression with no measure reference, such as a constant, stays unchanged; with several references each is rewritten on its own, which differs from wrapping the whole expression and can give wrong totals.
- Fact. 2019. https://www.sqlbi.com/articles/understanding-calculation-groups/ ; https://www.sqlbi.com/articles/understanding-the-application-of-calculation-items/ ; https://www.sqlbi.com/articles/avoiding-pitfalls-in-calculation-groups-precedence/
- When: A filter on the calculation group is active while an expression with zero or several measure references runs.

**T11-A201-1.** A calculation item chosen in a report replaces only the measure references at report level. The replacement does not reach measures referenced inside other measures, so a report-level selection cannot change just one inner part of a larger calculation.
- Fact. 2020. https://www.sqlbi.com/articles/using-calculation-groups-to-selectively-replace-measures-in-dax-expressions/
- When: A selection should change one measure that other measures use in their own code.

**T11-A201-2.** A calculation item whose formula is a fixed calculation and never calls SELECTEDMEASURE turns every measure it is applied to into that calculation. Only the format string of the original measure survives.
- Fact. 2020. https://www.sqlbi.com/articles/using-calculation-groups-to-selectively-replace-measures-in-dax-expressions/
- When: An item meant to replace the formula of one specific measure is applied from a report.

**T11-A201-3.** A calculation item that wraps its formula in IF with ISSELECTEDMEASURE and has no else branch returns blank for every other measure while it is active. Returning SELECTEDMEASURE in the else branch gives those measures their original result.
- Fact. 2020. https://www.sqlbi.com/articles/using-calculation-groups-to-selectively-replace-measures-in-dax-expressions/
- When: An item written to change one measure; measures that reference it internally still get its default version.

**T11-A201-4.** An ISSELECTEDMEASURE test does not confine a calculation item to that measure. The item is applied once, to the measure at the top level, and only picks a different expansion for it; a reference to the tested measure inside another measure keeps its default behaviour.
- Fact. 2020. https://www.sqlbi.com/articles/using-calculation-groups-to-selectively-replace-measures-in-dax-expressions/
- When: An item should change one measure that other measures reference in their code.

**T11-A286-4.** A DAX measure cannot find out which calculation item has been applied: calculation items rewrite the DAX code before the query starts to run.
- Fact. 2023. https://www.sqlbi.com/articles/using-field-parameters-and-calculation-groups-for-conditional-formatting/
- When: Writing a measure that should react to the calculation item a user selected.

**T11-A340-2.** Sideways recursion between calculation items can be relied on safely when the calculation group is hidden, so that code manages it and users do not. Report users can write their own measures and trigger errors they cannot explain.
- Option. 2025. https://www.sqlbi.com/articles/sideways-recursion-in-dax-calculation-groups/
- When: A calculation group whose items invoke other items of the same group.

**T11-A340-6.** When calculation items lead back to themselves only through measures that filter calculation items, the engine detects the loop and raises no error. It ignores the filter that would apply an item a second time and computes the expression with no further calculation items.
- Fact. 2025. https://www.sqlbi.com/articles/sideways-recursion-in-dax-calculation-groups/
- When: The same calculation item would be applied twice through measures that filter items of its group.

**T11-A340-7.** Sideways recursion is hardest to reason about, and most prone to unexpected results, when measures apply calculation items internally with CALCULATE while report users also switch the selected item in the interface, for example with a slicer.
- Fact. 2025. https://www.sqlbi.com/articles/sideways-recursion-in-dax-calculation-groups/
- When: Measures filter calculation items in code and users select items in the report too.

**T11-A340-8.** For a simple previous-year year-to-date calculation item, combine DATESYTD and SAMEPERIODLASTYEAR in one expression in preference to invoking an existing year-to-date item of the same group. The combined form is already optimal and easier to read.
- Should. 2025. https://www.sqlbi.com/articles/sideways-recursion-in-dax-calculation-groups/
- When: A simple time intelligence item; in complex cases invoking earlier items can avoid repeated code.

### Format string expressions

**T11-A160-2.** The format string of a calculation item can be a DAX expression, not only a fixed text. SELECTEDMEASUREFORMATSTRING returns the format already set on the measure being evaluated, so the expression can build on it, for example by adding the selected currency's symbol.
- Option. 2019. https://www.sqlbi.com/articles/understanding-calculation-groups/
- When: A fixed format is not enough, as when the format must show a currency symbol that a measure returns.

**T11-A184-2.** In a calculation item's format string expression, returning SELECTEDMEASUREFORMATSTRING leaves the format untouched for measures the item should not reformat. The text it returns may already come from an item of a group with higher precedence, not from the measure itself.
- Option. 2020. https://www.sqlbi.com/articles/controlling-format-strings-in-calculation-groups/
- When: An item reformats only some measures, such as a currency conversion that skips non-currency measures.

**T11-A184-6.** Some Power BI visuals do not fully support custom format strings, which matters for formats set through calculation groups. Custom visuals are affected, and the problem reaches other visuals too.
- Fact. Check. 2020. https://www.sqlbi.com/articles/controlling-format-strings-in-calculation-groups/
- When: Reports that show measures whose format a calculation item controls.
- Version: A fix was announced in 2020 but reported as still missing in October 2021; check current behaviour.

**T11-A207-3.** A calculation group can give a regular measure a format string that follows the context, such as one showing the current unit of measure. Its item changes the format only when ISSELECTEDMEASURE finds that measure, and returns SELECTEDMEASUREFORMATSTRING for every other measure.
- Option. Check. 2020. https://www.sqlbi.com/articles/dynamic-format-strings-with-calculation-groups/
- When: A measure needs a context-dependent format; the report must keep the calculation group filtered.
- Version: From 2020, when regular measures had no dynamic format string of their own; check whether that still applies.

**T11-A207-4.** A calculation group used to give a regular measure a dynamic format string works only while the report applies a filter on that group. Every report that relies on it must carry such a filter.
- Must. Check. 2020. https://www.sqlbi.com/articles/dynamic-format-strings-with-calculation-groups/
- When: A calculation group exists to supply a dynamic format string to a regular measure.
- Version: Technique from 2020; check whether it is still needed.

**T11-A207-5.** A page-level filter is one way to keep a calculation group filtered at all times in a report without using any room on the page.
- Option. 2020. https://www.sqlbi.com/articles/dynamic-format-strings-with-calculation-groups/
- When: A report needs a calculation group always filtered, for example to apply a dynamic format string.
