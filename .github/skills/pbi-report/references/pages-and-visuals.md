# Report files: pages, visuals, names and positions

Sources: Microsoft Learn "Power BI Desktop project report folder" (file layout, naming, annotations); Microsoft's published report schemas (`page`, `visualContainer`, `visualConfiguration`, `semanticQuery`); Microsoft Learn Fabric REST "Report definition" (example of the value form).

## Files

```
<Name>.Report/definition/
    report.json
    version.json
    pages/
        pages.json                      page order and active page
        <page name>/
            page.json
            visuals/
                <visual name>/
                    visual.json
```

- `page.json` needs `$schema`, `name`, `displayName`, `displayOption`, and `width` and `height` in pixels (the canvas size of checklist item 52).
- `visual.json` needs `$schema`, `name`, `position`, and either `visual` (a single visual) or `visualGroup` (a group).
- When you add a page, add its `name` to `pageOrder` in `pages.json` if that file exists.

## `$schema`

Take `$schema` from another `page.json` or `visual.json` already in this report. If the report has none yet, these are the newest addresses in Microsoft's schema repository (checked November 2026). Not confirmed: whether an older Power BI Desktop accepts these versions. If Desktop reports a schema error, ask the developer to add one visual in Desktop and take the address from that.

- page: `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json`
- visual: `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json`

## Names and labels

- `name` and folder name: letters, digits, underscore, hyphen only. `name` at most 50 characters and unique on its page. If a name breaks the character rule, Power BI Desktop ignores the file or folder, so the page or visual no longer appears when the report opens.
- Label pattern: `Page_Type_Subject`.
  - Page: the page's `name`. If an existing page still has a generated id as its name, use its tab name with spaces and punctuation removed (`Sales Detail` becomes `SalesDetail`).
  - Type: one short word for the kind of visual, for example Card, KPI, Bar, Line, Table, Matrix, Slicer, Text, Image, Button, Shape, Map, Group.
  - Subject: what it shows, for example `TotalSales`.
- New visual: the label is the `name` and the folder name.
- Existing visual: keep `name` and folder; add the label as an annotation. Power BI Desktop ignores annotations.
- New page: readable `name` and folder. The `displayName` is the tab text and is what checklist item 73 judges.
- Microsoft notes that renaming a `name` might break references to it inside and outside the report, and that Desktop must be restarted after a rename. The rename rule is in the project instructions. If the developer confirms a page rename, change the folder name, `name` in `page.json`, and the same name in `pageOrder` and `activePageName` of `pages.json`; then search the report folder for the old name and tell the developer what else refers to it.

## A new visual

```json
{
  "$schema": "<copied as described above>",
  "name": "Overview_Card_TotalSales",
  "position": { "x": 24, "y": 24, "z": 0, "width": 300, "height": 120, "tabOrder": 0 },
  "visual": {
    "visualType": "card",
    "visualContainerObjects": {
      "visualHeader": [ { "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } } ],
      "visualTooltip": [ { "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } } ]
    }
  }
}
```

- `position`: `x`, `y`, `width`, `height` are required, in pixels from the page's top-left corner. `z` is the stacking order (higher is on top). `tabOrder` is the keyboard order.
- The two `show` entries are Header icons off and Tooltips off. Their place and names (`visual.visualContainerObjects.visualHeader` and `.visualTooltip`, each a list of `{ "properties": { ... } }`, switch named `show`) are defined in Microsoft's `visualConfiguration` schema, for every visual type. That schema does not fix how the value is written. The written form used here, `{ "expr": { "Literal": { "Value": "false" } } }` with `"false"` as lowercase text, follows Microsoft's `semanticQuery` schema (a literal's `Value` is a string), the report.json example on Microsoft Learn, and the examples in Microsoft's `powerbi-report-cli` skill. A visual may also have a `mobile.json` with the same two cards for the phone layout; the check fails if either is on there.
- Fields and formatting (`visual.query`, `visual.objects`): the role names and property names differ for every visual type. Follow a visual of the same type already in this report. If there is none, ask the developer to place one in Desktop first. Do not write them from memory.
- A group is a `visual.json` with `visualGroup` in place of `visual`. Groups carry no header or tooltip setting.

## An existing visual

Add to the top level of its `visual.json`, leaving everything else as it is:

```json
"annotations": [
  { "name": "VisualLabel", "value": "Overview_Bar_SalesByMonth" }
]
```

and set the two `show` entries shown above inside its `visual.visualContainerObjects`. `scripts/set_visual_defaults.py` does both. It changes no other value, but it writes the whole file again, so spacing may differ in the diff.

A visual listed in section 7 of the brief keeps what the brief names switched on. It also carries this annotation, next to its `VisualLabel`. The value starts with `header:`, `tooltip:` or `both:` and then gives the reason; the setting that is not named stays off.

```json
{ "name": "HeaderTooltipException", "value": "header: drill buttons are needed on this chart" }
```

## Tools

- `python scripts/list_visuals.py . --page <page>` lists label, type, x, y, width, height and folder for one page. Use it to count the visuals on a page (item 20) and to check alignment (item 49).
- `python scripts/set_visual_defaults.py .` sets Header icons off and Tooltips off on every visual; `--label` adds labels.
- `python scripts/set_positions.py .` writes approved positions; see `layout-standard.md`, beside this file.
- `python scripts/check_project.py .` fails on a bad name, a missing label, a visual with header icons or tooltips on or not set, a visual outside its page, two data visuals that overlap, and a field the model does not have.

Checklist items: 20, 49, 52, 73
