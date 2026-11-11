# TMDL file syntax used by this template

Sources: Microsoft Learn "TMDL overview"; the Column, Measure and Table classes of Microsoft's Tabular Object Model (TMDL uses the same property names, written in camelCase); Microsoft's `semantic-model-authoring` skill.

## Layout

- One tab per level. An object is declared on one line; its properties are one level deeper.
- A property is `name: value` on one line. A true/false property can be written as the bare name, which means true (`isHidden`).
- An expression follows `=`. A one-line expression stays on the declaration line. A multi-line expression starts on the next line, one level deeper than the object's properties. Three backticks may enclose it.
- Put single quotes round a name that has a space, `.`, `=`, `:` or `'`. Double any `'` inside the name.
- A description is one or more `///` lines directly above the object.

```
/// One row per shipment.
table Shipments

	/// Carrier that moved the shipment.
	column Carrier
		dataType: string
		summarizeBy: none
		sourceColumn: Carrier

	column ShipmentKey
		dataType: int64
		isHidden
		sourceColumn: ShipmentKey

	partition Shipments = m
		mode: import
		source =
				let
				    // Build a small in-line table of shipments.
				    #"Created Shipments" = #table(type table [ShipmentKey = Int64.Type, Carrier = text, WeightKg = number], {{1, "North", 12.5}})
				in
				    #"Created Shipments"
```

A measure goes in the table `_Measures` (model standard, rule 1), in that table's file. If the model has no such table, `python scripts/scaffold.py measures-table .` makes it.

```
	/// Weight of all shipments, in kilograms.
	measure 'Shipped Weight' = SUM ( Shipments[WeightKg] )
		formatString: #,0
		displayFolder: Work Management\Base
```

The partition holds the table's Power Query query. Its layout (`partition <name> = m`, `mode: import`, `source =`, then the query) is the one shown in Microsoft's TMDL overview. For any other kind of source or storage mode, follow a partition already in this model; if there is none, copy the shipped example of that storage mode.

## Properties the checklist asks about

| Need | Property | Applies to | Checklist item |
|---|---|---|---|
| Hide a technical key or helper | `isHidden` | table, column, measure | 19, 25 |
| Group fields for report authors | `displayFolder` | column, measure | 22 |
| Order labels by another column | `sortByColumn` | column | 24 |
| Mark a URL, image, place and so on | `dataCategory` | column, measure, table | 26 |
| Number or date format | `formatString` | column, measure | 36, 71, 72 |
| Default totalling of a column | `summarizeBy` | column | 29 |
| Why a column or table is calculated in the model | `annotation CalculatedReason = <one line>` | calculated column, calculated table | 27, 38 |
| Mark the key column | `isKey` | column | - |

- A nested display folder is written with one backslash and no quotes: `displayFolder: Finance\Base`. Microsoft Learn names the backslash, and Microsoft's own saved projects hold it in this form. A forward slash does not nest.
- A value such as a data category must match what Power BI Desktop writes. Copy it from an object in this model that already has one. If there is none, copy it from the shipped example of that kind. Do not guess the spelling.
- A calculated column is declared with its formula, `column 'Name' = <DAX>`; a calculated table has `partition <name> = calculated`. Each needs the `CalculatedReason` annotation, one level below the column or the table.
- Use one format string for the same kind of number everywhere in the model (item 71). Take date formats from the brief (item 72).

## Shipped examples

`tests/fixtures/examples/INDEX.md` lists one working example of every object kind: relationships of each kind, roles, a calculation group, field parameters, user-defined functions, hierarchies, a marked date table, each storage mode, incremental refresh, an aggregation table, perspectives, translations and more. Every model file there was written by Microsoft's own TMDL serializer. When this model has no object of the kind you need, copy the example, change its names, and run the checks. A multi-line DAX formula sits one tab level deeper than the object's properties, as the examples show.

## Read only

Microsoft says `diagramLayout.json` is not to be edited outside Power BI Desktop. This template also never edits `.platform` or anything in a `.pbi` folder, and never writes `lineageTag` or `PBI_` annotations (TMDL instructions).

## Annotations

Your own annotations are allowed: `annotation Name = value`, one level below the object. Never add `PBI_Id` to a role; the other never-write rules are in the TMDL instructions.

Checklist items: 19, 22, 24, 25, 26, 36, 71, 72
