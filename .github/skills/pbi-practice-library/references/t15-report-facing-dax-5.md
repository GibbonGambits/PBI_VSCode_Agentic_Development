# Report-facing DAX and report design

Part 5 of 5 of this topic. Covers: Custom and SVG visuals; Themes and report templates.

Practice notes drawn from public SQLBI articles, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail.

## General practice

### Custom and SVG visuals

**T15-A328-2.** Before building a custom visual, always decide whether it is worth the extra time and complexity: the effort to define, test and optimise it, its upkeep and likely future changes, and any licence fee. Showing users simpler alternatives that answer the same questions helps decide.
- Must. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/ ; https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: A requirement that core visuals and existing templates cannot easily meet.
- Version: Custom visuals are outside this template's standards.

**T15-A328-6.** Look for answers first in trusted sources, such as official documentation, peer-reviewed papers or unbiased community experts, and check whatever an AI tool says against them: its output can be wrong, misleading, outdated or incomplete.
- Should. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Any question an AI tool could also answer.

**T15-A328-10.** Read, try out and understand the code an AI assistant generates; do not just send each failure back and ask it to try again. For simple cases, sending the error back may be fine.
- Should. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: AI-generated code, above all in a language you know little or for complex output.

**T15-A328-11.** When generated code raises an error, one option is to look up the failing part in the documentation first, and then point the AI assistant to the specific line that fails where possible.
- Option. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Code from an AI assistant returns an error.

**T15-A328-12.** When an AI assistant must extend or comment an existing specification, tell it plainly to leave all other code as it is unless asked otherwise.
- Should. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Adding the next mark, or comments, to the same specification.

**T15-A328-15.** Do not send sensitive information to AI tools, unless the organisation has an enterprise plan that covers it or the language model runs locally on your own machine.
- Should. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Any prompt, file or data given to an AI tool.

**T15-A328-16.** When an AI-assisted coding session is so tangled that progress stops, consider a new conversation that starts from the last working specification, or a pause to study the problem area first.
- Consider. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Work with an AI assistant has stalled.

**T15-A328-21.** Plan what you will build in the chosen tool before you prompt an AI assistant for a specification: planning shows where the assistant helps most. Someone who knows the technology well may plan only briefly.
- Should. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Before asking an AI assistant for visual code.

**T15-A328-22.** Weigh how AI tools differ before choosing one for visual code: cost and daily limits; whether it accepts images of the design; step-by-step reasoning for complex tasks; web search; how recent its training data is; how well it does the task; policy or regional access.
- Consider. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Choosing an AI tool to help generate custom visual code.

**T15-A317-2.** Look at simpler options with core visuals first, and build a custom visual only when it gives readers a clear business benefit. If a useful report can be built in a more direct way, that way is probably right.
- Should. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: Deciding whether to create a custom visual for a requirement.
- Version: Custom visuals are outside this template's standards; it never suggests one itself.

**T15-A317-3.** Reasons to weigh not building a custom visual at all: core visuals can already produce it; the team lacks the skills or maturity to build and maintain it; time is short; it performs too slowly; or its only benefit is looks.
- Consider. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: Deciding whether to create a custom visual for a requirement.
- Version: Custom visuals are outside this template's standards.

**T15-A317-5.** When you decide not to build the visual that users asked for, go back to them with an alternative proposal and work towards a compromise.
- Must. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: A requested custom visual has been turned down.

**T15-A317-6.** When choosing the method for a custom visual, weigh three things: whether the method can produce the required design, how long building and testing will take, and how mature the team is in Power BI and how skilled with the tool or language.
- Should. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: A custom visual has been judged worth building.
- Version: Custom visuals are outside this template's standards.

**T15-A317-7.** The effort of building custom visuals can be cut by starting from validated templates, such as scripts or Deneb templates: defining, testing and optimising from nothing takes extra time, above all with custom code.
- Option. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: Creating custom visuals, especially ones that need code.
- Version: Deneb is a custom visual from AppSource, outside this template's standards.

**T15-A317-8.** The maintenance burden of a custom visual can be lowered by commenting and documenting its code and teaching colleagues how to maintain it. An SVG-generating DAX measure grows long, and teammates who did not build it may struggle to fix it.
- Option. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: Custom visuals, including SVG visuals produced by DAX measures.

**T15-A317-12.** Keep DAX measures that produce SVG images apart from the rest of the semantic model, and hidden: such a measure serves one visual requirement only.
- Should. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: Models that hold SVG measures for report visuals.
- Version: Here measures stay in the one measures table (model standard rule 1); a separate table needs an exception row (M001).

**T15-A317-15.** When core visuals cannot meet a requirement, six routes exist, each suiting a different situation: core visuals bent by unusual formatting, ready-made AppSource visuals, SVG images from DAX measures, Deneb with Vega or Vega-Lite, Python or R visuals, and JavaScript visuals on the visual API.
- Option. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: A reporting requirement that core Power BI visuals cannot meet directly.
- Version: AppSource, Deneb and JavaScript visuals are custom visuals, outside this template; R and Python visuals are retiring (V016).

**T15-A318-9.** If AppSource custom visuals are disabled in the tenant and you need them, consider building a business case for an exception that explains the value of allowing approved or certified visuals.
- Consider. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: The option to get more visuals is missing because the administrator disabled custom visuals.
- Version: Tenant settings and AppSource custom visuals are outside this template.

**T15-A318-10.** For a common chart type such as a bullet chart, a ready-made AppSource custom visual can be used: it is usually quicker to set up and maintain, and a paid one may repay its cost in time saved. It offers only its developer's options.
- Option. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: A common chart type is missing from the core visuals.
- Version: AppSource custom visuals are outside this template, which never suggests one itself.

**T15-A318-18.** Use a custom visual only when it brings users a clear benefit, never just because it looks attractive. Balance simplicity and maintainability against business value, or the report becomes overcomplicated, hard to read and hard to maintain.
- Must. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: Choosing among approaches to build a custom visual, such as a bullet chart.
- Version: Custom visuals are outside this template's standards.

### Themes and report templates

**T15-A322-1.** Build one theme for the team or organisation and let it carry the default static formatting; do this early when several pages or reports are planned.
- Should. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: Several pages or reports are planned and should share one look.
- Version: This template's theme is fixed and is not changed.

**T15-A322-5.** A free or commercial theme file from the community can be the starting point for a theme, adjusted afterwards, in place of writing one from nothing.
- Option. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: A new theme is needed.
- Version: This template's theme is fixed and is not changed.

**T15-A322-8.** Judge a third-party theme generator against your own needs; one that uses generative AI brings the same risk of invented or unintended changes.
- Consider. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: Choosing a tool to build a theme.
- Version: Third-party generators are outside this template, whose theme is fixed and is not changed.

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

**T15-A328-3.** Before building a custom visual, have a validated semantic model at hand, and identify which of its fields and calculations the visual needs.
- Must. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Starting work on any custom visual.
- Version: Custom visuals are outside this template's standards.

**T15-A328-4.** With little experience of Deneb and Vega, write the specification in Vega-Lite: it is simpler and shorter than Vega, with fewer options. Vega may be needed for advanced cases.
- Should. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Choosing the specification language of a Deneb visual.
- Version: Deneb is a custom visual from AppSource, outside this template's standards.

**T15-A328-5.** For a complex multi-element visual, weigh the routes: overlaid core visuals are fragile; an AppSource visual helps only if it matches; SVG in DAX means very complex code; Python or R visuals suit statistical charts; JavaScript visuals are a last resort without experience.
- Consider. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Core visuals cannot produce the design directly.
- Version: Custom visuals are outside this template; R and Python visuals are retiring (V016); overlapping data visuals need an exception (G002).

**T15-A328-7.** Give an AI assistant a detailed prompt for a Deneb specification: an image of the design, each element with its model fields, the expected interactivity, that data comes from the Power BI model, the layered marks, an example specification and a description of the dataset.
- Should. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Asking an AI assistant to generate a Deneb specification.
- Version: Deneb is a custom visual from AppSource, outside this template's standards.

**T15-A328-8.** Generate a complex visual specification one mark at a time, and go on only when the current mark looks and behaves as expected. Expect new problems when separately made marks are combined.
- Should. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Visuals with many marks and encodings.

**T15-A328-9.** Before running an AI-made specification you can format it and check for misspelled or wrong field names, surplus code unusual for Deneb, hard-coded values, transformations, filters or encodings nobody expected, flagged errors and warnings, and unasked changes from the previous version.
- Option. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: A specification comes back from an AI assistant.
- Version: Deneb is a custom visual from AppSource, outside this template's standards.

**T15-A328-13.** Consider working out a value that a Deneb visual needs, such as which month is the latest for conditional formatting, in a new measure and not in a transformation inside the specification.
- Consider. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: An AI assistant tends to put everything in Vega-Lite; a calculation inside the visual is sometimes right.
- Version: Deneb is a custom visual from AppSource, outside this template's standards.

**T15-A328-14.** Test a custom visual you built under many conditions, not only in its default view: apply filters, slicers and other interactions, and try heavy filtering, blanks and very small or very large values, to confirm it behaves as expected.
- Must. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/ ; https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Custom visuals you define yourself, for example Deneb specifications in Vega or Vega-Lite.
- Version: Deneb is a custom visual from AppSource, outside this template's standards.

**T15-A328-17.** Deneb hands the fields added to the visual to the specification as one table named dataset; a period in a field name becomes an underscore, and the specification names fields that way under its field key.
- Fact. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Writing a Deneb specification.
- Version: Deneb is a custom visual from AppSource, outside this template's standards.

**T15-A328-18.** In a Deneb Vega-Lite specification, a text mark with no aggregate transform draws one label for every row of the visual's dataset, for example 12 overlapping labels for 12 months; an aggregate with a sum gives one total.
- Fact. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: A text mark should show one total.
- Version: Deneb is a custom visual from AppSource, outside this template's standards.

**T15-A328-19.** Splitting the container of a Deneb visual into parts to position elements stops the visual from scaling by itself when it is resized on the report page.
- Fact. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Laying out elements inside a Deneb visual.
- Version: Deneb is a custom visual from AppSource, outside this template's standards.

**T15-A328-23.** If the first answer of an AI assistant is a specification with errors or unexpected output, try again in a new chat; copy a result into the visual for inspection only when it shows no errors or odd elements.
- Should. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: Directly after the first prompt for a specification.

**T15-A328-24.** A visual of several marks can be generated in two ways: each mark as its own specification, combined later (slower, easier to troubleshoot), or mark after mark in one specification (quicker when it works, harder to fix).
- Option. 2025. https://www.sqlbi.com/articles/using-ai-assistance-to-create-power-bi-custom-visuals/
- When: An AI assistant helps to build a multi-mark visual.

**T15-A317-9.** A DAX measure shows SVG markup as a picture only when its text starts with `data:image/svg+xml;utf8,`, the markup is valid SVG and a valid DAX string (inner double quotes doubled or replaced by single quotes), and a visual that renders images uses it.
- Must. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: Building custom visuals as SVG images returned by DAX measures.
- Version: In 2024: tables, matrices, the new card, the new slicer and the scatter chart background render such images.

**T15-A317-10.** A long SVG string in a DAX measure can be split into variables, one per shape plus variables for key settings such as positions, colours and height, and then concatenated. It is easier to change and to make dynamic later.
- Option. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: DAX measures that build SVG images.

**T15-A317-11.** Handle data values that would draw SVG shapes beyond the edges of the image. For extremely large values, cap the plotted value at a maximum and add an arrow at the edge to show the real value is off the scale.
- Must. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: Dynamic SVG measures whose shape positions or lengths come from data values.

**T15-A317-14.** An SVG visual can be drawn in a design tool and its generated markup copied into the DAX measure instead of being written by hand. Such tools often turn elements like text into paths, which are hard to read or to make dynamic.
- Option. 2024. https://www.sqlbi.com/articles/creating-custom-visuals-in-power-bi-with-dax/
- When: Designing SVG images for DAX measures.
- Version: Figma is the design tool named; it is outside this template's tools.

**T15-A318-11.** Fixes for problems in AppSource custom visuals depend on their developers. An open-source visual can break after a Power BI update and stay broken until its developer is able or willing to repair it.
- Fact. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: Reports that rely on AppSource custom visuals, open-source ones above all.
- Version: AppSource custom visuals are outside this template's standards.

**T15-A318-13.** Test the performance of a self-built Deneb visual and optimise it where possible.
- Should. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: Custom visuals defined in Deneb.
- Version: Deneb is a custom visual from AppSource, outside this template's standards.

**T15-A318-14.** A team with high visual maturity can offset the extra effort of Deneb specifications by building and curating its own library of templates, reused across reports.
- Option. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: Teams that use Deneb for custom visuals.
- Version: Deneb is a custom visual from AppSource, outside this template's standards.

**T15-A318-15.** When a bullet chart only complements an existing table, matrix or card, consider an SVG image from a DAX measure in place of a separate visual. It renders in every report whatever the admin settings or licences, but is complex and harder to maintain.
- Consider. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: A small chart inside a table, matrix or card.

**T15-A318-16.** Train users to read and interpret small SVG visuals embedded in tables or matrices: they have no room for a legend or labels and can confuse.
- Should. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: SVG micro-visuals, such as bullet charts, inside table or matrix cells.

**T15-A318-17.** Provide a link to a short, visual FAQ page that explains how to read the small SVG visuals embedded in a table or matrix.
- Should. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: SVG micro-visuals, such as bullet charts, inside table or matrix cells.

**T15-A318-20.** Consider building your own visual in Deneb when ready-made custom visuals lack the options you need and you want pixel-perfect control without full Python or JavaScript code. It costs much more time and has a steeper learning curve, unless templates are used.
- Consider. 2024. https://www.sqlbi.com/articles/building-bullet-charts-in-power-bi-reports/
- When: Custom visuals must be allowed in the organisation; if they are disabled, Deneb is unavailable too.
- Version: Deneb is a custom visual from AppSource, outside this template's standards.

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

**T15-A322-16.** The semantic-link-labs Python library, run in a Fabric notebook, can apply a new theme to many published reports at once. Only the notebook needs a Fabric workspace; the reports may sit in a Pro workspace.
- Option. 2024. https://www.sqlbi.com/articles/re-using-visual-formatting-in-and-across-power-bi-reports/
- When: Many published reports rely on theme styles; the library is installed and the new theme is available to it.
- Version: Here the theme is fixed and nothing is published from the template; semantic-link-labs is an outside tool.
