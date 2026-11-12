# The theme, header icons, tooltips, and what they mean for the checklist

Sources: Microsoft's report theme schema (version 2.159); Microsoft Learn pages on report themes, custom themes, visual defaults, the format pane, visual tooltips, drill mode, drillthrough, export data, export to PDF, and accessible reports.

## The theme

`theme/theme.json` is the owner's theme. It must stay exactly as it is. Every report gets it (owner's rule). There are two routes:

- The developer imports it once in Power BI Desktop (Design ribbon > Import theme). This is the route Microsoft Learn describes: it supports changing a file under `RegisteredResources` only for a resource that Desktop itself registered.
- A script registers it in the files, the way Microsoft's own report skill does: `python scripts/scaffold.py theme .` for a report that exists, `python scripts/scaffold.py project <Name> --register-theme` for a new one. The evaluate-and-improve flow uses this route without a question. The project must be closed in Power BI Desktop: Microsoft Learn says `report.json` is not reloaded into an open session. Tell the developer the theme was registered by script, and ask them to look at the colours when the report is first opened.

The report's base theme stays as it is; the custom theme sits on top of it.

It sets: 32 data colours; background, foreground and table accent colours; the three colours for colour-scale conditional formatting (maximum green, minimum red, null grey); four text classes (label 10 pt, title 11 pt, callout 28 pt, header); filter pane text sizes; and, for every visual type, Header icons off and Tooltips off.

Use theme colours and theme text styles. Do not set colours, fonts or sizes on single visuals unless the developer asks (items 50, 70, 74). Formatting set on a visual wins over the theme until the visual is reset to default.

## Header icons and Tooltips are off everywhere

This template sets both off twice: in the theme, and on every visual (rule in the PBIR instructions; mechanics in `pages-and-visuals.md`, beside this file).

- Header icons are the row of icons at the top of a visual. Microsoft lists: visual information, warning and error, drill on dropdown, drill up, drill down, show next level, expand to next level, pin, focus mode, "See data" layout, More options, filter, help tooltip, smart narrative, Copilot summary, and in the service comment, personalize visual, copy and set alert. More options holds "Export data".
- Microsoft states that header icon visibility takes effect only in reading view. In Power BI Desktop, and while editing, the icons still show.
- Microsoft states that turning Tooltips off hides the tooltip for that visual. A visual pinned to a dashboard still shows a basic tooltip.

Not confirmed from Microsoft: whether Power BI Desktop keeps and applies the two visual-level settings on text boxes, shapes, images and buttons; whether adding them changes a visual's padding (Microsoft's report skill says a visual-level container setting can stop theme padding from applying); whether a report-page tooltip can still appear on a visual whose Tooltips are off; whether right-click drill, keyboard shortcuts and "Export data" still work in reading view when the header is hidden. Ask the developer to test these in a published report when they matter.

## Features a visual uses

Before header icons and tooltips are switched off on an existing report, keep what the report uses. Do this yourself, without a question:

1. Run `python scripts/list_visuals.py .` and read each visual's file.
2. A visual keeps **header icons** when it uses something only the header gives: a hierarchy or more than one field on an axis, so that the reader drills with the header's drill icons; or a help tooltip written for the visual (`visualHelpTooltip`).
3. A visual keeps **tooltips** when it has a report page tooltip (its tooltip names a page), fields in its Tooltips well, or a tooltip text written for it.
4. For each such visual add a row to section 7 of `docs/report-brief.md` with the reason "the report uses it: <feature>", add the annotation `HeaderTooltipException` (rule 5 of the PBIR instructions), and turn off only the other setting. Then run `python scripts/set_visual_defaults.py .`: it leaves the excepted setting alone.
5. List these visuals in your final answer. The developer can remove a row afterwards; you then switch that setting off.

A feature that only might be used (focus mode, export data on a visual with no drill) is not a reason: the owner's rule is off.

## When a visual needs them back

The rule and the annotation are in the PBIR instructions (rule 5) and `pages-and-visuals.md`. The developer can turn the setting on in Desktop (Format pane > General > Header icons, or Tooltips), or you set that one `show` to true. The theme makes header icons white: ask the developer to check in reading view that the icons can be seen, and to set an icon colour on that visual if not.

## What this means for checklist items

| Item | Effect of the theme and the rule | What to do |
|---|---|---|
| 37 | Definitions cannot rely on tooltips or the help-tooltip icon | Put definitions in model descriptions and on the page: a subtitle, a text box, or an Info page (item 75) |
| 50 | One deliberate theme is in place | Keep visual-level colour and font overrides out |
| 51, 63 | No header icons to lean on for moving around | Give visible buttons or on-page instructions, and a back button on drillthrough pages |
| 57, 58 | The theme's green and red are almost equally light (contrast 1.02 to 1) | Never show status by red against green alone; add an icon, a sign or a word |
| 59 | Drill icons are hidden in reading view. Microsoft documents right-click drill and drillthrough as separate routes | Tell users on the page how to drill, or add a drillthrough button; or ask for an exception on that visual |
| 65 | No hover tooltips | Not applicable unless the developer asks for a tooltip exception |
| 66 | Card and header text is grey #777777 on white: contrast 4.48 to 1, just under the 4.5 to 1 in Microsoft's accessibility checklist. 16 of the 32 data colours are under 3 to 1 on white, and the last is white | Tell the developer. Do not use the light colours for text or thin lines. Pair colour with a label or shape |
| 67 | Label text is 10 pt and the title class 11 pt. Microsoft's table shows that visual titles and small labels use classes derived from these; the sizes they get under this theme are not documented | Ask the developer to check sizes on screen. Do not change the theme |
| 70 | Four text classes are defined | Use them; no fonts or sizes per visual |
| 74 | Brand colours come from the theme | No hex colours on visuals |
| 77 | "Export data" for one visual sits in the header's More options menu. Export to PDF is on the report's own menu | If users must export a visual's data, ask for an exception on that visual and test it |

Contrast figures were worked out with the standard WCAG contrast formula from the colours in the theme file.

Checklist items: 37, 50, 51, 57, 58, 59, 63, 65, 66, 67, 70, 74, 75, 77
