# Report-facing DAX and report design

Part 4 of 4 of this topic. Covers: Custom and SVG visuals; Themes and report templates.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit or condition. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. **Paper** means the note comes from a white paper: its link opens only a summary, and the paper itself is on a download site that `pbi-lookup` does not open, so confirm the point on Microsoft Learn instead. The article holds the detail. A note may name another product in passing, such as Analysis Services or Excel: that is information for the developer. Nothing is installed, published or deployed from this template.

## General practice

### Custom and SVG visuals

**T15-A328-6.** Look for answers first in trusted sources, such as official documentation, peer-reviewed papers or unbiased community experts, and check whatever an AI tool says against them: its output can be wrong, misleading, outdated or incomplete.
- Should. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Any question an AI tool could also answer.

**T15-A328-10.** Read, try out and understand the code an AI assistant generates; do not just send each failure back and ask it to try again. For simple cases, sending the error back may be fine.
- Should. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: AI-generated code, above all in a language you know little or for complex output.

**T15-A328-11.** When generated code raises an error, one option is to look up the failing part in the documentation first, and then point the AI assistant to the specific line that fails where possible.
- Option. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Code from an AI assistant returns an error.

**T15-A328-15.** Do not send sensitive information to AI tools, unless the organisation has an enterprise plan that covers it or the language model runs locally on your own machine.
- Should. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Any prompt, file or data given to an AI tool.

**T15-A317-5.** When you decide not to build the visual that users asked for, go back to them with an alternative proposal and work towards a compromise.
- Must. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: A requested visual has been turned down.

**T15-A317-8.** The maintenance burden of an SVG-generating DAX measure can be lowered by commenting and documenting its code and teaching colleagues how to maintain it: such a measure grows long, and teammates who did not build it may struggle to fix it.
- Option. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: SVG images produced by DAX measures.

**T15-A317-12.** Keep DAX measures that produce SVG images apart from the rest of the semantic model, and hidden: such a measure serves one visual requirement only.
- Should. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: Models that hold SVG measures for report visuals.
- Version: Here measures stay in the one measures table (model standard rule 1); a separate table needs an exception row (M001).

**T15-A317-15.** When core visuals cannot meet a requirement directly, one route is core visuals bent by unusual formatting; another is SVG images from DAX measures. Each suits a different situation.
- Option. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: A reporting requirement that core Power BI visuals cannot meet directly.

### Themes and report templates

**T15-A322-5.** A free or commercial theme file from the community can be the starting point for a theme, adjusted afterwards, in place of writing one from nothing.
- Option. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: A new theme is needed.
- Version: This template's theme is fixed and is not changed.

**T15-A322-9.** Tips to weigh for a shared theme: involve users in the design; prefer general formatting that suits most cases; use accessible colours and fonts without heavy colour, thick lines or large text; try it on several reports, sizes and devices; document and share it.
- Consider. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: Building and rolling out a theme for static formatting, above all one shared with others.
- Version: This template's theme is fixed and is not changed.

**T15-A322-13.** Write down, for the other people who work on the reports, how the formatting measures that return theme colour names are meant to work.
- Must. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: Measures that return theme colour names drive conditional formatting.

**T15-A322-17.** Once a theme file exists, go on to make a Power BI template (one at least) with the theme applied and a sample page (one at least) showing its styles: examples help self-service authors adopt the theme.
- Should. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: An organisation has made its own theme.
- Version: This template's theme is fixed and is not changed; .pbit files sit outside its project files.

**T15-A322-18.** When editing a theme JSON file by hand, you can look up the properties that exist in the published JSON schema for Power BI themes; theme files are complex, with default styles for every visual type.
- Option. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: Creating or editing a theme JSON file by hand.
- Version: Schema on GitHub, updated monthly (2024). This template's theme is fixed and is not changed.

**T15-A322-19.** A template built around a theme can also carry guidance for report authors: how to use the theme well, and how to keep formatting logic in measures.
- Option. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: A Power BI template is made to promote a theme.
- Version: This template's theme is fixed and is not changed; .pbit files sit outside its project files.

## Special-case techniques and facts

### Custom and SVG visuals

**T15-A325-13.** Small pie or doughnut shapes can be drawn as SVG images inside cards or tables, as micro-visuals for a KPI, an achievement or simple shares of two or three categories.
- Option. 2025. https://www.sqlbi.com/articles/using-pie-charts-is-not-the-end-of-the-world/
- When: Micro-visuals in cards or tables, small multiples of pies or doughnuts included.
- Version: In 2025 SVG was the only way to get small multiples of pie or doughnut charts.

**T15-A328-5.** For a complex multi-element visual, weigh the routes: overlaid core visuals are fragile, and SVG in DAX means very complex code.
- Consider. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Core visuals cannot produce the design directly.
- Version: Overlapping data visuals need an exception (G002).

**T15-A317-9.** A DAX measure shows SVG markup as a picture only when its text starts with `data:image/svg+xml;utf8,`, the markup is valid SVG and a valid DAX string (inner double quotes doubled or replaced by single quotes), and a visual that renders images uses it.
- Must. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: Building SVG images returned by DAX measures.
- Version: In 2024: tables, matrices, the new card, the new slicer and the scatter chart background render such images.

**T15-A317-10.** A long SVG string in a DAX measure can be split into variables, one per shape plus variables for key settings such as positions, colours and height, and then concatenated. It is easier to change and to make dynamic later.
- Option. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: DAX measures that build SVG images.

**T15-A317-11.** Handle data values that would draw SVG shapes beyond the edges of the image. For extremely large values, cap the plotted value at a maximum and add an arrow at the edge to show the real value is off the scale.
- Must. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: Dynamic SVG measures whose shape positions or lengths come from data values.

**T15-A318-15.** When a bullet chart only complements an existing table, matrix or card, consider an SVG image from a DAX measure in place of a separate visual. It renders in every report whatever the admin settings or licences, but is complex and harder to maintain.
- Consider. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: A small chart inside a table, matrix or card.

**T15-A318-16.** Train users to read and interpret small SVG visuals embedded in tables or matrices: they have no room for a legend or labels and can confuse.
- Should. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: SVG micro-visuals, such as bullet charts, inside table or matrix cells.

**T15-A318-17.** Provide a link to a short, visual FAQ page that explains how to read the small SVG visuals embedded in a table or matrix.
- Should. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: SVG micro-visuals, such as bullet charts, inside table or matrix cells.

### Themes and report templates

**T15-A322-3.** Theme settings apply from general to specific: top-level properties first, then text classes, then wildcard styles for all visuals, then styles for one visual type; each later kind overrides the earlier ones.
- Fact. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: Editing a theme JSON file by hand.
- Version: This template's theme is fixed and is not changed.

**T15-A322-4.** To give a theme formatting for specific visual types, export the current theme and edit its JSON in a text or code editor.
- Must. Check. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: A full theme must go beyond colours, fonts and sizes.
- Version: In 2024 Desktop could edit only a few theme properties. This template's theme is fixed and is not changed.

**T15-A322-6.** Before sharing a theme file with a generative AI tool, check its embedded images: a theme holds styling and rarely confidential data, but the images in it may be proprietary.
- Consider. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: A generative AI tool helps to create or change a theme.
- Version: This template's theme is fixed and is not changed.

**T15-A322-7.** A generative AI tool can create or change a theme when it is given the theme JSON schema and example themes; its output may still be incomplete, alter properties nobody asked about or invent invalid ones.
- Option. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: Editing a theme with AI help; from nothing Desktop likely rejects the result, and hand editing may be quicker.
- Version: This template's theme is fixed and is not changed.

**T15-A322-12.** A colour-returning measure can return the name of a top-level theme colour property, such as good, bad, neutral, minColor, midColor or maxColor, in place of a colour code: the measure holds the logic and the theme decides the colour.
- Option. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: Conditional formatting by measure; the main data colours, stored as an array, have no known name to return.

**T15-A322-14.** Power BI Desktop shows the theme's sentiment colours under other names than the theme file does: good appears as Positive and bad as Negative.
- Fact. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: Reading or returning theme sentiment colours, for example from a measure.
