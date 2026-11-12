# Improving the design of a report

Use this page when the developer asks to improve the design of an existing report, and for the kind Design of the evaluate-and-improve flow (skill `pbi-improve`). Not every report needs the same work. A page that already works is left alone; a page that fails is changed until it works. You judge, you change, you look at the result: nothing waits for a yes.

## 1. Judge each page first

1. Look at every page: `python scripts/desktop_bridge.py screenshots .` (open the project first when Desktop does not have it: `desktop_bridge.py open .`), and `python scripts/list_visuals.py .`. Read the visual files of each page.
2. Judge the page against the design items of the checklist: 54 (the chart fits the question), 55 (titles, labels and legends), 56 (units and scales), 57 and 58 (colour carries one meaning, used the same way everywhere), 66 (contrast, and never colour alone), 70 (one set of text styles). Search `checklist/checklist.md` for `## Item 54` and so on.
3. Write one line per page in the plan or the change log: "works" or "fails item <n>: <what the reader sees>". A page that works gets no change. Never change a page only to make it look like the other pages.

## 2. What you may change on a page that fails

- **The visual type**, to fit the question it answers: the table in section H of `report-standard.md`, beside this file. A part-to-whole visual with more than 5 categories becomes a bar chart sorted by value; a trend gets an ordered date axis; a gauge used as a KPI becomes a card or a KPI visual.
- **Add, replace, resize or remove visuals.** No information may be lost: every field and measure that the page showed is still shown on that page. Removing a visual is allowed only when another visual on the page shows the same fields and measures. A retired map type (`map`, `filledMap`) keeps its type: Azure Maps can be switched off by an administrator. Name it in your final answer as a note.
- **Positions and sizes**: by the numbers in `layout-standard.md`, with `python scripts/set_positions.py`. A new visual is copied from a visual of the same type in the report, or from the shipped example of that type (`tests/fixtures/examples/INDEX.md`), as `pages-and-visuals.md` sets out.
- **Titles and subtitles** (item 55): each title says what the visual shows. A subtitle that repeats the title or the field names is switched off (`subTitle` `show` false); keep one only when it adds something, such as the period or the unit. Code V025 lists visuals that may show an automatic subtitle.
- **Text** (item 70): the theme's text classes only. Remove font, size and colour settings on single visuals (V009).
- **Colour** (items 57, 58, 66): section 3.
- **Tab order**: after any visual moves, is added or is removed, run `python scripts/set_tab_order.py .` (`--dry-run` first). It sets the keyboard order to the reading order, without a yes.

Not in this kind: a measure's formula, a new business meaning, the theme file, the phone layout. A threshold the brief does not give is a `TODO(owner)` question.

## 3. Colour by meaning

Decide first what the colour says. Then use the theme's colours for that meaning, and nothing else.

| What the colour says | Colours | When |
|---|---|---|
| Which category (a region, a product) | The theme's data colours, in their order: remove colours set on the visual so the theme gives them | Always for categories |
| How much (an amount where more is only more: revenue, count, hours) | One colour, light to dark. With this template's theme: `#A4DDEE` for the lowest value to `#1B4D5C` for the highest (two of the theme's data colours of the same blue). With another theme: a light and a dark data colour of the same hue | The default for every colour scale, a filled map included |
| Good or bad (a KPI against a threshold, a variance to target) | The theme's `minimum` (red) for bad and `maximum` (green) for good; the theme's `background` in the middle | Only when the brief or the developer says which direction is good and where the threshold lies (item 58). Always add an icon, a sign or a word: the theme's red and green are almost equally light, and red with green is a hard pair (rules 37 and 60 of `report-standard.md`) |

- An amount never gets red to green: that says low is bad, a meaning nobody gave. When the direction is not known, use "how much" and ask in your final answer.
- At most 2 colour systems that carry meaning in one report (item 57), and the same colour means the same thing on every page.
- No light data colour for text or thin lines (item 66; `theme.md`, beside this file, lists the contrast).
- Inside a colour scale (`FillRule`) colours are written as codes: Microsoft's report skill says `ThemeDataColor` does not work there. V009 accepts there the theme's data colours, `background`, `minimum`, `center`, `maximum` and `null`. Replace colours only; never remove part of a scale (V024).

## 4. Look at the result

1. `python scripts/check_project.py .`, and fix every error.
2. `python scripts/desktop_bridge.py reload .`, then `screenshots .`. On each page you changed, look for: an error icon or an empty visual, text that is cut off, overlaps, colours that do not match section 3, an automatic subtitle that repeats the field names. Fix what you find, then look again.
3. `python scripts/desktop_bridge.py clean <folder of pictures>`.
4. When the Bridge is not available, say in your final answer that you could not see the pages, and name them.

## Sources

Checklist items 54 to 58, 66 and 70. Microsoft Learn: "Visualization types in Power BI"; "Apply conditional formatting in tables and matrixes"; "Design Power BI reports for accessibility"; "Create custom report themes". Microsoft's report skill (`skills-for-fabric`, MIT), its files chart-selection.md and design/color.md. Restated in this template's own words.

Checklist items: 54, 55, 56, 57, 58, 66, 70
