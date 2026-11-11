# Decisions of round 3

Each decision that was made without asking, with its reason. GitHub Copilot does not read this folder.

The three cases in which the work would have stopped to ask did not arise: no source was found that contradicts the checklist; nothing touched `checklist/checklist.md` or `theme/theme.json`; no licence problem (the GPL source was read only, and SQLBI's rules are restated in new words).

## Levels of the new checks

1. **Fail only when the files show it for certain.** A new check fails when Microsoft says the thing breaks or gives wrong numbers, or the checklist gives a hard number, and the files show the breach without a guess. Where the files can only suggest a breach (a text pattern, a name, something that depends on the data), the check warns even when Microsoft names a failure. Examples: M517 (VALUES compared with one value: Microsoft says it can error; the scanner cannot be sure of the context) and M606 (object-level security on a field a visual uses). Reason: a false failure would start the lessons loop on correct work.
2. **No existing check changed level.** M010 stays a warning although Microsoft says a measure written with its table breaks when the measure moves. Its reach grew: it now also reads role rules and calculation items.
3. **M502 (division) fails.** Checklist item 33 gives a hard number. "Trivial" is read as: the divisor is a fixed number, which is also the case in which Microsoft Learn prefers the operator.
4. **M402 fails** when time intelligence is used and no table is marked as a date table: checklist item 31 gives the number. Without time intelligence it is a warning (M403).
5. **V001 fails** (checklist item 63: back navigation on every drillthrough page). **V006 fails** above 16 visuals (item 20). "Count each dominant large table or matrix as 2" is read as: one that covers a third of the page or more. That reading is this template's.
6. **J003 fails.** Microsoft Learn calls a schema breach in a report file a blocking error. The schemas are copied into `scripts/schemas` (MIT) so that the check gives the same answer over time and needs no network.
7. **Findings grouped.** M520 (DAX style) gives one finding for each table file; A001 and A003 one for each page. An existing report would otherwise print one line for every formula and every visual.

## What was adopted, and what was not

8. **DAX style: SQLBI's rules**, restated. Checked by M520: spaces around brackets and operators, one argument per line for a function with two or more arguments or one that holds a function, CALCULATE written in full, a column directly after its table, commas after their argument, `@` for columns a formula makes. Not checked: the indentation of arguments and of the closing bracket (TMDL adds its own indentation). Not adopted: single quotes only when needed (Microsoft's own skill always writes them, and a higher source wins); `:=` for measures (TMDL writes `=`).
9. **Variable names with a `_` prefix: not adopted.** Microsoft's skill uses it; Microsoft Learn's own page on variables does not. Learn is the higher source.
10. **Fixed format strings from the best practice rules: not adopted in their exact form.** The checklist (items 71, 72) leaves the format to the organisation. The template checks that a format exists.
11. **"Remove roles with no members": outside this template.** Members are assigned in the Power BI service, not in project files.
12. **One measures table stays** (owner's rule) although Microsoft's skill advises spreading measures over tables.
13. **Header icons and tooltips stay off** (owner's rule) although Microsoft recommends report page tooltips and header icon text. Exceptions are per visual, in section 7 of the brief. The shipped tooltip example carries its exception.
14. **`mobile.json` stays untouched** (existing rule) although its schema is public; the one existing exception is `scripts/set_visual_defaults.py`, which turns Header icons and Tooltips off there. Phone layout is laid out in Power BI Desktop.
15. **Names of tables and columns: a default.** Business words with spaces, a capital first letter, no underscores, no words run together, no Dim, Fact or Stg prefix (Microsoft's skill and two best practice rules). M118 reads only names that report authors see: hidden keys keep their source names. That limit is this template's choice.
16. **Tables exempt from "no relationship" (M411):** the measures table, calculation groups, field parameters, numeric range parameters, and tables the brief lists. This template's choice.

## Copilot builds it itself

17. **A whole project from nothing: yes.** Microsoft documents PBIR and TMDL as formats that other tools may write. `scripts/scaffold.py` copies the shipped starter.
18. **Registering the theme by writing files: no, by default.** Microsoft Learn supports edits under `RegisteredResources` only for a resource Power BI Desktop registered itself. Microsoft's own report skill does register a theme by writing two entries in `report.json`; a lower source does not override Learn. So the developer imports the theme once in Desktop. `--register-theme` exists for a developer who says yes. Microsoft's command-line validator also expects a theme's inner name to equal its file name; the owner's theme may not be changed, so that cannot be met.
19. **The measures table.** Import model: an imported table with one hidden column and no rows, read by a one-step Power Query query (not the encoded form Desktop writes for Enter data, which cannot be written reliably by hand). Direct Lake and DirectQuery: a calculated table that names no other table, with the standard's own reason line. The DirectQuery default is new; before, the developer was asked.
20. **Moves and renames.** No script rewrites the files. `scripts/find_references.py` lists every reference and what it cannot classify; Copilot edits; the checks (M901 to M903, M908, B001, M010) then prove that nothing was missed. Reason: a rewriting tool that is wrong once does more harm than a reader that is wrong once.
21. **Descriptions never block.** `/// TODO(owner): <question>` is the only record; `scripts/list_todos.py` prints the list; Copilot asks at the end of the task. The reason line of a calculated column is still the developer's words.
22. **A report on a published model.** The field list is saved as `docs/model-fields.md` and the check reads it (B001, B002).

## Microsoft's tools

23. **Desktop Bridge: treated as a preview.** The September 2026 release notes list it without a preview label; the page on editing project files still calls it one. The script calls status, reload and screenshot-all, and for the model definition the authoring tool's reload. It never opens Desktop, publishes, packs or refreshes. Pictures go outside the project.
24. **Modeling server: the local one only, read only.** The developer installs it, accepts its licence terms and opens the connection. The guidance lists the operations Copilot may call and those it may never call.
25. **Look-ups.** The script is the main route because it enforces the four sites, also after a redirect, and marks page text as information. For DAX Guide and SQLBI a page must be in the sitemap the owner named.

## Examples

26. **How "verified" was reached.** Model examples were written by Microsoft's TMDL serializer from models built with Microsoft's library, then loaded and validated with the same library (version 19.118.3). Report examples pass Microsoft's schemas and the project check; Microsoft's offline validator was run once on a copy. The library and the validator were used while building and are not shipped. Nothing was opened in Power BI Desktop.
27. **Examples that break a rule on purpose** (a both-direction relationship, a many-to-many relationship, a one-to-one relationship, separate row and object roles, a calendar) are excused by rows in the examples' own brief, the way a real project would do it.
28. **Preview examples sit apart**, under `preview/`, and M841 warns when a model uses a preview feature the brief does not list.
29. **Not built:** the Q&A visual and the Bing maps (retiring or deprecated), visuals whose identifier or roles no Microsoft source gives, legacy data sources, and the partitions the service makes for a refresh policy. `tests/fixtures/examples/INDEX.md` lists each with its reason.

## The engine and the loop

30. **The scanner** replaces every pattern that was matched against raw formula text. Patterns on TMDL lines (a property name, a comment outside an expression) stay: they are not formulas.
31. **Suggestions are notes** with codes that start with U. `scripts/lessons.py` refuses to record a warning or a note as a failed check.
32. **Existing tests that changed**, and why: four tests of made-up visuals and measures now meet the new rules (a `queryRef` that Microsoft's schema requires; alt text and a title; a unique tab order number; DAX in the new style); the tests that list every finding of the broken fixture list the new codes; one test that expected a clean result for a relationship to a table that does not exist now expects M901; the test that a report on a published model is not checked now covers the saved field list.
33. **`maintenance/` is a template folder.** Copilot is told not to read it and not to change it without asking.

## Closing the open rows

34. **Levels of the checks added to close the coverage file.** Fail only for M833 (Microsoft's rule says Power BI does not support a legacy query partition on a structured data source). Notes, because the source words them as a choice or as one option among several: M416 (Is Nullable off on a key), M303 (isDefaultLabel, only with the Copilot check on), V018 (a page title text box: Microsoft's skill puts the title, the main figure or the main chart at the top left), U008, U104, U105. Every other new check warns.
35. **Report-level measure prefix (V012).** Microsoft Learn asks for a prefix and gives an underscore as its example. The check uses the underscore unless section 4 of the brief gives another prefix. The brief gained that one line.
36. **The good test project uses the new card visual.** The legacy card now gives the note U105, so the fixture that stands for a correct project was moved to `cardVisual`.
37. **Variable names.** The DAX standard's own snippets used the `_` prefix that its rule 31 does not adopt. The snippets were renamed; the rule did not change.

38. **Multiple-language reports are in scope.** The owner's list of pages that are out of scope does not name them, so the eleven guidance pages got a guidance file (`multiple-languages.md`), a shipped label measure and five checks (M524, M525, V019, V020, V021). A report counts as multiple-language when a culture file of its model holds translations. Checks that would rest on a file form no Microsoft Learn page confirms were not built; the guidance says so at each rule.
39. **Preview features in files.** M841 now also reads value filter behavior, user-context calculated columns and calculated tables over Direct Lake data; V022 reads the Gantt visual and a format string on one visual. Each needs its row in section 11 of the brief.
40. **Descriptions above three child objects** (`multipleOrEmptySelectionExpression`, `noSelectionExpression`, `dataCoverageDefinition`) no longer give D003: Microsoft's serializer writes descriptions there. This widens what an existing check accepts; its level did not change.
41. **The example report measure got the prefix** (`_Sales per Order Line`), so the shipped example follows V012 instead of being excused from it.
42. **Checkpoint commits.** Two commits on the branch hold examples that a helper was still writing; the commits after them complete the work. The branch is squashed or kept as the owner prefers.

43. **What the source review changed.** M523 became a note: Microsoft's skill passes filters to SUMMARIZECOLUMNS as arguments in its general guidelines, and only SQLBI and one performance pattern place them outside. M906 now fails only on control characters that are not white space, as Microsoft's rule defines them; a tab in a visible name is reported by M118. M904 stays a fail and now cites the rule that says processing gives an error. M821, M903 and M908 stay fails and now cite the Microsoft pages that say a missing name gives an error. The guidance on functions and object-level security, on tooltips and accessibility, on USERNAME, on the Desktop Bridge version, on the modeling server's operating systems and on visual calculations (generally available since May 2026) was reworded to what the pages say. The example table for a dynamic query parameter was renamed to one word, a limit Microsoft states.
44. **Existing fail checks the review questioned.** M001, M002 and P001 fail although no source says the thing breaks; they are owner's rules from earlier rounds, and this round was told not to change the level of an existing check.

## Could not be verified

- Anything that needs Power BI Desktop: every example, the starter project, the Desktop Bridge script.
- The modeling server guidance (not run).
- The monthly feature summary posts on Microsoft's blog (could not be opened): the inventory relies on Microsoft Learn's update pages.
- The value `ParameterMetadata` carries on a field parameter, and the annotation that records Auto date/time: both come from Microsoft's skill or from saved projects, not from Microsoft Learn.
