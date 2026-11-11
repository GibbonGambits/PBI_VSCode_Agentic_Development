# The theme, header icons, tooltips, and what they mean for the checklist

Sources: Microsoft's report theme schema (version 2.159); Microsoft Learn pages on report themes, custom themes, visual defaults, the format pane, visual tooltips, drill mode, drillthrough, export data, export to PDF, and accessible reports.

## The theme

`theme/theme.json` is the owner's theme. It must stay exactly as it is. The developer applies it in Power BI Desktop (Design ribbon > Import theme).

It sets: 32 data colours; background, foreground and table accent colours; the three colours for colour-scale conditional formatting (maximum green, minimum red, null grey); four text classes (label 10 pt, title 11 pt, callout 28 pt, header); filter pane text sizes; and, for every visual type, Header icons off and Tooltips off.

Use theme colours and theme text styles. Do not set colours, fonts or sizes on single visuals unless the developer asks (items 50, 70, 74). Formatting set on a visual wins over the theme until the visual is reset to default.

## Header icons and Tooltips are off everywhere

This template sets both off twice: in the theme, and on every visual (rule in the PBIR instructions; mechanics in `pages-and-visuals.md`, beside this file).

- Header icons are the row of icons at the top of a visual. Microsoft lists: visual information, warning and error, drill on dropdown, drill up, drill down, show next level, expand to next level, pin, focus mode, "See data" layout, More options, filter, help tooltip, smart narrative, Copilot summary, and in the service comment, personalize visual, copy and set alert. More options holds "Export data".
- Microsoft states that header icon visibility takes effect only in reading view. In Power BI Desktop, and while editing, the icons still show.
- Microsoft states that turning Tooltips off hides the tooltip for that visual. A visual pinned to a dashboard still shows a basic tooltip.

Not confirmed from Microsoft: whether Power BI Desktop keeps and applies the two visual-level settings on text boxes, shapes, images and buttons; whether adding them changes a visual's padding (Microsoft's report skill says a visual-level container setting can stop theme padding from applying); whether a report-page tooltip can still appear on a visual whose Tooltips are off; whether right-click drill, keyboard shortcuts and "Export data" still work in reading view when the header is hidden. Ask the developer to test these in a published report when they matter.

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
