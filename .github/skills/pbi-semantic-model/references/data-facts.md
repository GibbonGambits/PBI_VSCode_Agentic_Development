# Facts about the data: Microsoft's modeling server (optional)

The project files hold no data. Row counts, distinct values, whether a key is unique, gaps in a date table: no file shows them. Two ways to get such a fact:

1. Ask the developer once, in one message, and record the answers in section 4 of `docs/report-brief.md`. This always works.
2. Read it yourself through Microsoft's own server, when the developer has already set it up. This file says how.

Everything in the template works without the server. The template never installs it and never sets up a connection: that is the developer's decision.

## What it is

- Microsoft's Power BI Authoring MCP Server, the local one (repository `microsoft/powerbi-modeling-mcp`). Microsoft Learn lists the local server as generally available and the hosted one as preview. This template uses only the local one. Source: https://learn.microsoft.com/power-bi/developer/mcp/power-bi-authoring-mcp
- Microsoft says the local server does not support macOS. It states nothing else about the operating system; Power BI Desktop itself runs on Windows only.
- The developer installs it (the VS Code extension "Power BI Authoring MCP") and accepts Microsoft's licence terms for it. Never accept them yourself: do not call the tool `accept_eula`, and do not start the server with a flag that accepts them.
- Ask the developer to run it with `--readonly`. Microsoft describes that flag as a safe mode that prevents every write to the model.
- Query results pass through the chat. Microsoft says model metadata and query results may be sent to the AI service behind it. If the data is sensitive, the developer may prefer route 1.

## What you may call

Only operations that read. The server names every tool `<thing>_operations` with an `Operation` argument.

| Allowed | Tool and operation |
|---|---|
| See which models are open in Power BI Desktop | `connection_operations`: `ListLocalInstances`, `ListConnections`, `GetConnection` |
| Run a DAX query | `dax_query_operations`: `Execute`, `Validate` |
| Read the model's objects | the `List`, `Get` and `GetSchema` operations of the table, column, measure and relationship tools |

Never call: any `Create`, `Update`, `Delete`, `Rename` or `Move` operation; any `Refresh...` operation; `DeployToFabric`; `transaction_operations` `Commit`; `ClearCache`; `accept_eula`. The model is changed in its files, where the checks and Git see the change.

Opening a connection is the developer's step. If no connection to this project's model is open, say so and use route 1. The one case where you read from a workspace is the field list of a published model, and only over a connection the developer has already made (skill `pbi-report`).

## The queries

Write the table and column names as they are in the model. Each query returns one small row.

| Fact | DAX query |
|---|---|
| Rows in a table | `EVALUATE ROW ( "Rows", COUNTROWS ( 'Sales' ) )` |
| Distinct values of a column | `EVALUATE ROW ( "Distinct", DISTINCTCOUNT ( 'Sales'[Store Key] ) )` |
| Is a key unique, with no blanks? | `EVALUATE ROW ( "Rows", COUNTROWS ( 'Store' ), "Distinct", DISTINCTCOUNT ( 'Store'[Store Key] ), "Blanks", COUNTBLANK ( 'Store'[Store Key] ) )` : unique when Rows equals Distinct, and no blanks when Blanks is 0 |
| First and last date, and days present | `EVALUATE ROW ( "First", MIN ( 'Date'[Date] ), "Last", MAX ( 'Date'[Date] ), "Days", COUNTROWS ( 'Date' ) )` : no gaps when Days equals the number of days from First to Last |
| The field list of the model | `EVALUATE INFO.VIEW.TABLES ()`, `EVALUATE INFO.VIEW.COLUMNS ()`, `EVALUATE INFO.VIEW.MEASURES ()` |

Every function used here is in the file `dax-functions.md` beside this one.

- A model that was only just loaded from files may hold no data. A count of 0 then says nothing: tell the developer.
- Record each fact you use in section 4 of the brief, with the date and "read through Microsoft's modeling server".
- These facts answer checklist items 11, 14, 17, 21 and 31, and the rules on distinct values and large tables in the file `storage-and-security.md` beside this one.

## Not confirmed

- Whether the server asks the developer before it runs a query: Microsoft's notes on this differ between versions.
- Whether it can tell if a Power Query step folds. Until that is known, folding (item 3) stays a question for the developer.

Written, not run: the server could not be run where this template was built.

## Sources

Read on 11 November 2026. Restated in this template's own words.

- Microsoft Learn: https://learn.microsoft.com/power-bi/developer/mcp/power-bi-authoring-mcp ; https://learn.microsoft.com/power-bi/developer/mcp/mcp-servers-overview ; the DAX reference pages of COUNTROWS, DISTINCTCOUNT, COUNTBLANK and the INFO.VIEW functions (addresses in `dax-functions.md`).
- Microsoft's repository `microsoft/powerbi-modeling-mcp`: its README, change log and the list of tools in the package.

Checklist items: 3, 11, 14, 17, 21, 31
