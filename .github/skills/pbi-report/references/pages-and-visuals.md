# Report files: pages, visuals, names and positions

Sources: Microsoft Learn "Power BI Desktop project report folder" (file layout, naming, annotations, schema errors) and "Edit PBIP files outside Power BI Desktop" (files not to edit); Microsoft's published report schemas (`page`, `visualContainer`, `visualConfiguration`, `semanticQuery`); Microsoft Learn Fabric REST "Report definition" (example of the value form).

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

Take `$schema` from a file of the same kind already in this report. If the report has none, copy it from the shipped example of that kind (`tests/fixtures/examples/INDEX.md`). The addresses the examples carry are the newest in Microsoft's schema repository when this template was last refreshed. A copy of every version Microsoft has published is in `scripts/schemas`, so a file saved by an older Power BI Desktop is checked against its own version:

- page: `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json`
- visual: `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json`

`python scripts/check_project.py .` checks every report file against the schema it names (J003), so a property that Microsoft's schema does not have is found before Power BI Desktop sees the file. To check one file: `python scripts/json_schema.py <file>`. Not confirmed: whether an older Power BI Desktop accepts these versions. If Desktop reports a schema error after a reload, tell the developer which version the file names; a Desktop update is the usual answer.

## Names and labels

- `name` and folder name: letters, digits, underscore, hyphen only. `name` at most 50 characters and unique on its page. If a name breaks the character rule, Power BI Desktop ignores the file or folder, so the page or visual no longer appears when the report opens.
- Label pattern: `Page_Type_Subject`.
  - Page: the page's `name`. If an existing page still has a generated id as its name, use its tab name with spaces and punctuation removed (`Sales Detail` becomes `SalesDetail`).
  - Type: one short word for the kind of visual, for example Card, KPI, Bar, Line, Table, Matrix, Slicer, Text, Image, Button, Shape, Map, Group.
  - Subject: what it shows, for example `TotalSales`.
- New visual: the label is the `name` and the folder name.
- Existing visual: keep `name` and folder; add the label as an annotation. Power BI Desktop ignores annotations.
- New page: readable `name` and folder. The `displayName` is the tab text and is what checklist item 73 judges.
- Microsoft notes that renaming a `name` might break references to it inside and outside the report, and that Desktop must be restarted after a rename. The rename rule is in the project instructions. If the developer confirms a page rename, do it yourself: change the folder name, `name` in `page.json`, and the same name in `pageOrder` and `activePageName` of `pages.json`; then search the report folder for the old name (buttons that go to the page, bookmarks, drillthrough and tooltip settings) and change each place you can confirm. Run the check: V008, V010 and V011 report what was missed. List for the developer anything you could not confirm.

## A new visual

```json
{
  "$schema": "<copied as described above>",
  "name": "Overview_Card_TotalSales",
  "position": { "x": 24, "y": 24, "z": 0, "width": 296, "height": 120, "tabOrder": 0 },
  "visual": {
    "visualType": "cardVisual",
    "visualContainerObjects": {
      "visualHeader": [ { "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } } ],
      "visualTooltip": [ { "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } } ]
    }
  }
}
```

- `position`: `x`, `y`, `width`, `height` are required, in pixels from the page's top-left corner. `z` is the stacking order (higher is on top). `tabOrder` is the keyboard order.
- The two `show` entries are Header icons off and Tooltips off. Their place and names (`visual.visualContainerObjects.visualHeader` and `.visualTooltip`, each a list of `{ "properties": { ... } }`, switch named `show`) are defined in Microsoft's `visualConfiguration` schema, for every visual type. That schema does not fix how the value is written. The written form used here, `{ "expr": { "Literal": { "Value": "false" } } }` with `"false"` as lowercase text, follows Microsoft's `semanticQuery` schema (a literal's `Value` is a string), the report.json example on Microsoft Learn, and the examples in Microsoft's `powerbi-report-cli` skill. A visual may also have a `mobile.json` with the same two cards for the phone layout; the check fails if either is on there.
- Fields and formatting (`visual.query`, `visual.objects`): the role names and property names differ for every visual type. Follow a visual of the same type already in this report. If there is none, copy the shipped example of that type (`tests/fixtures/examples/INDEX.md`): it holds the type's identifier and its roles, bound to made-up fields. Change the name, the fields and the position, then run the checks. Do not write role names from memory. Only when the index has no example of that type, ask the developer to place one in Desktop.
- No styling on a visual: no colour, font, size, border, shadow or background. The theme does that work (V009). Every visual that shows data gets alt text and a written title (A001, A003): `report-standard.md`, beside this file.
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
- `python scripts/check_project.py .` fails on a bad name, a missing label, a visual with header icons or tooltips on or not set, a visual outside its page, two data visuals that overlap, a field the model does not have, and a file that does not fit Microsoft's schema.
- `python scripts/desktop_bridge.py` reloads the project and takes a picture of each page, where the developer has agreed to it: `desktop-bridge.md`, beside this file.

## Read only

Microsoft says these are not to be edited outside Power BI Desktop: `definition.pbir`, `mobileState.json`, `semanticModelDiagramLayout.json`, and a `report.json` beside `definition.pbir` (the older report format). This template also leaves alone the `.platform` file, `.pbi` folders, every file already under `StaticResources` and every `mobile.json`. Two exceptions, and no other: an image file may be added to `StaticResources/RegisteredResources` and registered (rule 69 of `report-standard.md`, beside this file), and `scripts/set_visual_defaults.py` turns Header icons and Tooltips off in a `mobile.json` that has them on.

Checklist items: 20, 49, 52, 73
