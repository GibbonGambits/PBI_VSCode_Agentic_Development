# Descriptions for model objects and Power Query

## Where a description goes

- Tables, columns and measures: `///` lines directly above the object, with no blank line between. Several `///` lines are allowed. (Microsoft Learn, "TMDL overview".)
- Do not use a `description` property. (Microsoft's `semantic-model-authoring` skill.)
- `scripts/check_project.py` fails when a visible table, column or measure has no description. A calculation group's table is checked like any table (D001), and a calculation item without a description gives M812 (warn). Hierarchy levels are not checked by the script; describe them too (checklist items 23 and 30).

## What to write

- Put the most important words first. Microsoft's skill says Copilot in Power BI reads only the first 200 characters of a description.
- State the grain (what one row or one value stands for), the unit, the exclusions and the caveats that checklist items 37 and 46 ask for.
- Do not repeat the object's name as its description.
- Write only what `docs/report-brief.md`, the model or the developer states. Never write a business meaning from your own knowledge.
- A starter row from the skill `business-definitions` is not a confirmed definition. Ask the developer to confirm it before it goes into a description (item 48 asks for definitions people can find).

## When the meaning is not stated

Write a placeholder and carry on with the work. A missing meaning never stops a task, and the placeholder is the only record of the question: do not keep a second list. At the end of the task run `python scripts/list_todos.py .` and ask the developer about all the open questions in one message.

```
	/// TODO(owner): Does Returned mean any return, or full returns only?
	column Returned
```

A placeholder is not a description. While one remains, checklist item 23 is not met, and the project check lists it as a note (I001). When the developer answers, replace the line with the description and record a confirmed definition in section 5 of the brief.

## Power Query: queries and steps

Microsoft's Power Query guidance asks for meaningful names and descriptions on queries and steps. Microsoft does not document how Power BI Desktop stores them in the model files, so this template uses its own convention:

- A query that loads a table: the table's `///` description is the query's description.
- A shared query or parameter: `///` directly above its `expression` in `expressions.tmdl`.
- A step: a name that says what the step does, and a `//` line directly above the step that describes it.

```
				let
				    // Build a small in-line table of order lines.
				    #"Created Order Lines" = #table(type table [OrderId = Int64.Type, Amount = number], {{1, 120.5}, {2, 80}}),
				    // Keep only order lines at or above the MinimumAmount parameter.
				    #"Kept Qualifying Amounts" = Table.SelectRows(#"Created Order Lines", each [Amount] >= MinimumAmount)
				in
				    #"Kept Qualifying Amounts"
```

Optional style from Microsoft's skill: start a step name with a past-tense verb and keep it to 50 characters; keep the comment to 225 characters, do not start it with "Step" or a number, and do not repeat the code.

The developer can also type a description in Power BI Desktop: right-click a step or a query and choose Properties. Whether Desktop shows the text written under this convention in those boxes is not confirmed.

## Comments

- `//` is allowed only inside a Power Query (M) or DAX expression. Anywhere else in a TMDL file the check fails.
- Power Query also allows `/* ... */`. For DAX, use `//`.
- In DAX, checklist item 8 asks for documentation where a rule lives: comment a hard-coded business rule, an exception or a manual override. Plain DAX needs no comment. (Power Query steps are different: every step gets its line, as set out above.)

Checklist items: 8, 23, 30, 37, 46, 48
