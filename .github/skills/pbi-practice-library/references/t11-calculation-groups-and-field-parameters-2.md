# Calculation groups and field parameters

Part 2 of 2 of this topic. Covers: Selection expressions.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

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

### Selection expressions

**T11-A332-2.** To control what happens when several calculation items are selected together, multipleOrEmptySelectionExpression can hold, for example, an ERROR call whose own text tells the user that the combination is not allowed.
- Option. Check. 2025. https://www.sqlbi.com/articles/controlling-empty-or-multiple-selections-in-calculation-groups/
- When: A calculation group used from a slicer in which users may select several items.
- Version: Described as a preview in May 2025; compatibility level 1605; edited in TMDL view or an external editor.

**T11-A332-3.** multipleOrEmptySelectionExpression can settle a multiple selection by applying one of the selected items by a priority of your own, such as the highest ordinal, which keeps the model's item order. Write its formatStringDefinition the same way, so the format follows that item.
- Option. Check. 2025. https://www.sqlbi.com/articles/controlling-empty-or-multiple-selections-in-calculation-groups/
- When: Several items of one group are selected and a single prioritised item should apply.
- Version: Described as a preview in May 2025.

**T11-A332-4.** multipleOrEmptySelectionExpression can map given combinations of selected items to an existing item that gives the combined result, such as previous year plus year-to-date to previous year-to-date. Compare the selection with each known set and raise an error for any other.
- Option. Check. 2025. https://www.sqlbi.com/articles/controlling-empty-or-multiple-selections-in-calculation-groups/
- When: Users may select several items expecting a combined calculation; DAX has no recursion to stack them.
- Version: Described as a preview in May 2025.

**T11-A332-5.** For a calculation group, an empty selection means a filter is active but leaves no item, as when a saved report filters an item renamed later; multipleOrEmptySelectionExpression handles it. No selection means no direct or indirect filter on the group; noSelectionExpression handles that.
- Fact. Check. 2025. https://www.sqlbi.com/articles/controlling-empty-or-multiple-selections-in-calculation-groups/
- When: Writing either selection expression for a calculation group.
- Version: Described as a preview in May 2025; needs compatibility level 1605.

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
