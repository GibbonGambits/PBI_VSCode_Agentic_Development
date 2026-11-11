# Reports in more than one language

Copilot reads this file when the brief asks for one report that readers open in more than one language: values in the reader's format, report text, page navigation and translated data.
Metadata translations (cultures, translated names of tables, columns and measures) are in the file `model-objects.md` beside this one, section D; they are not repeated here.

## Terms

"A multiple-language report" below means a model with at least one culture file that holds `translations`, or a brief that names two or more languages. The checks V020 and V021 use the first test; for a report on a published model there is no model here, so the check cannot tell.

## A. Values that follow the reader's locale

**1. How Power BI knows the reader's language.** The service reads a culture name such as `nl-NL` (language, then region) from the browser and uses it for the whole report. Measure names fall back to the nearest culture (`fr-CA` finds `fr-FR`); table and column names need an exact match, or the default names show. Microsoft calls the second a known issue. So add a culture file for every culture name the brief lists, not one per language. No check: the list of cultures is the brief's. Source: https://learn.microsoft.com/en-us/power-bi/guidance/multiple-language-locale

**2. Format strings do the locale work.** Visuals format dates and numbers for the reader by themselves, if the format string is one that follows the region. For dates, Microsoft recommends `Short Date` or `Long Date` (in TMDL: `formatString: Short Date`); a fixed pattern such as `dd/mm/yyyy` shows every reader the same order. No check: no Microsoft Learn page shows that Power BI Desktop writes the named formats this way in TMDL (rule 17). Source: the locale page in rule 1.

**3. Translations for the default language.** Microsoft advises using them sparingly: Desktop shows only object names, so the report looks different in Desktop and in the service. No check: Microsoft allows it and leaves how much to the author. Source: the locale page in rule 1.

**4. USERCULTURE works in measures.** In a measure it returns the reader's culture name. In a calculated column or table it does not. The two Microsoft pages disagree on what it returns there: the guidance page says the model's default culture; the DAX page says, for import, a value fixed at refresh (an invariant locale for scheduled refresh), and for DirectQuery the reader's locale. Either way an imported table cannot hold per-reader text. Check: M524 (warn; USERCULTURE in a calculated column or a calculated table of a table that is not DirectQuery. A warning and not a fail, because the two pages disagree on what it returns. A user-context calculated column, which is a preview feature, is left out). Source: the locale page in rule 1; https://learn.microsoft.com/en-us/dax/userculture-function-dax

**5. USERCULTURE outside the model.** The DAX page says it may return the wrong locale from queries and from report-level measures of a live-connected report; inside the model (measures, row-level security, calculation items) it is correct. Write label measures in the model. Check: V019 (warn; USERCULTURE in `reportExtensions.json`). Source: the USERCULTURE page in rule 4.

**6. FORMAT with a locale.** `FORMAT ( value, format, locale )` takes a culture name as its third argument; `FORMAT ( TODAY (), "dddd", USERCULTURE () )` gives the weekday in the reader's language. A format that does not depend on the locale (`mm/dd/yyyy`) ignores the third argument. The FORMAT page is not consistent on the default: it says named formats use the model culture, and elsewhere that dates use the user's locale. FORMAT returns text, so a chart cannot use the result; for numbers prefer a format string (note U005 in the file `model-objects.md` beside this one). No new check: U005 covers text from FORMAT. Source: https://learn.microsoft.com/en-us/dax/format-function-dax ; the USERCULTURE page in rule 4.

## B. Designing a report for translation

**7. Plan it from the start.** Microsoft says adding languages later mostly means undoing designs that cannot be translated. Both packaging choices work: one project with model and report, or a shared model with report-only projects. No check. Source: https://learn.microsoft.com/en-us/power-bi/guidance/multiple-language-best-practice

**8. What cannot be translated.** Power BI translates the model only, never text stored in the report layout: typed text in text boxes, buttons and shapes, a typed visual title, and page tab names. Source: https://learn.microsoft.com/en-us/power-bi/guidance/multiple-language-translation ; https://learn.microsoft.com/en-us/power-bi/guidance/translation-builder-localize-label
- Check: V020 (warn; one finding for each report on a model with translations: it counts the text boxes and the visual titles typed as text). Typed text in a shape or a button is not counted: how PBIR stores it is not confirmed (rule 17).
- A project that ships a culture file but serves one language lists V020 and V021 in section 10 of the brief, with `-` for the page and the visual.

**9. Titles.** The title Power BI makes from field names is translated, because it is built from translated names. Microsoft says: keep that title, or take the title from a label measure; never type one. This template's code A003 and checklist item 55 warn on the made-up title. A title from a label measure satisfies both, so use that. No new check. Source: the labels page in rule 8; `report-standard.md` in the skill pbi-report, rules 49 and 50.

**10. Page titles.** Rule 70 of `report-standard.md` puts a text box title on every page (note V018). In a multiple-language report that text box must not hold typed text: Microsoft's example shows the title in a rectangle shape whose text comes from a label measure. V018 still notes a page without a text box; accept the note. No new check. Source: the labels page in rule 8.

**11. Room for longer text.** A label that fits in English can wrap or be cut off in another language. Leave generous space round every label and test each language. No check: a file does not show the rendered width. Source: the best practice page in rule 7.

**12. Test in the service.** Metadata and label translations do not work in Power BI Desktop; data translations do. Add `?language=<culture>` to the report address in the service to test a language without changing settings. Mark this as the developer's step. No check. Source: https://learn.microsoft.com/en-us/power-bi/guidance/data-translation-synchronize-field ; the locale page in rule 1.

**13. Publish to web** does not support multiple-language reports. No check: publishing happens in the service. Source: the planning page in rule 8.

## C. The labels table

**14. What it is.** Translations Builder, a separate Microsoft tool this template does not use, keeps report text as measures so that translations can be stored like metadata. What it leaves in the model:
- `Localized Labels`: a hidden table with one hidden measure per label (report title, visual titles, button text). The translations sit on the measure names, as `caption:` lines in each culture file.
- `Translated Localized Labels`: a visible table with one measure per label whose name ends in `Label` (measure names must be unique in the model). Each formula is SWITCH over USERCULTURE: one text per culture name, then the default language's text last. These are the measures a page uses.
- The tool deletes and rebuilds the second table each time it runs; hand edits there are lost.
- Source: the labels page in rule 8; the locale page in rule 1 for the SWITCH pattern.

**15. Building the same by hand in TMDL.** When the brief asks for labels and the developer does not use the tool, the visible measures alone do the work. One measure per label, with a `///` line saying where it appears (made-up example, style of section B of the file `dax-standard.md` beside this one):

```tmdl
	/// Title of the store page, in the reader's language.
	measure 'Sales by Store Label' =
			SWITCH (
			    USERCULTURE (),
			    "nl-NL",
			    "Verkoop per winkel",
			    "de-DE",
			    "Umsatz nach Filiale",
			    "Sales by Store"
			)
```

If the developer will maintain labels with the tool later, also add the hidden table: each of its measures gets a caption per culture, written like this in `definition/cultures/nl-NL.tmdl`:

```tmdl
cultureInfo nl-NL
	translations
		model Model
			table 'Localized Labels'
				measure 'Sales by Store'
					caption: Verkoop per winkel
```

**16. Rules for label measures.**
- The last argument of the SWITCH is the default language's text, so an unknown culture still gets a label. Check: M525 (warn; a SWITCH whose first argument calls USERCULTURE and that has no default value). Source: the locale page in rule 1; the labels page in rule 8.
- Every culture name in that SWITCH, other than the model's own culture, has a culture file, so tables and columns translate too (rule 1). Check: M525 (warn; a culture name in that SWITCH that is neither the model's own culture nor a culture file). Source: the locale page in rule 1.
- This template's measure rules still apply. A second measure table needs a row in section 9 of the brief with M001, and a hidden one also with M002; the folder types of rule 2 of the file `model-standard.md` beside this one have no type for labels, so each label folder needs a row with M004 until the owner adds one. No new check.

**17. Not confirmed** from Microsoft: the formula, partition and columns of the hidden `Localized Labels` table; whether the tool sets display folders or annotations; how PBIR stores the text of a shape or button bound to a measure. Also, for the rest of this file: that Desktop writes `formatString: Short Date` in TMDL (shipped test files use it, no Learn page shows it); that the `bookmarkGuid` value is the `name` in the PBIR bookmark file.

## D. Page navigation

**18. Hide the tabs.** Page tab names cannot be translated. Hide every page but one: then the published report shows no tabs at all and opens on the visible page. Check: V021 (warn; a report on a model with translations with more than one page that is not hidden). Source: https://learn.microsoft.com/en-us/power-bi/guidance/multiple-language-page-navigation ; the planning page in rule 8.

**19. Buttons with label text.** Microsoft's menu is a row of buttons. Each button's action is a bookmark that holds only the page (Data and Display off, Current Page on); its text comes from a label measure through the fx button. In PBIR the options are `suppressData` and `suppressDisplay` true and `suppressActiveSection` absent or false; this mapping is read from Microsoft's bookmark schema, not from the page. A screen reader reads each button on its own, not as one group like tabs. No check: the button text rule is covered by rule 8. Source: the navigation page in rule 18.

**20. Sources differ on navigation.** Rule 12 of `report-standard.md` prefers a page navigator, and the page navigation action over a bookmark. The multiple-language page mentions neither; it shows only bookmark buttons. Page names cannot be translated (rule 18), and no page says whether a navigator can show anything else, so use buttons here, or a navigator only after the developer has tested it in the service. No check. Source: the navigation page in rule 18.

## E. Translated data

**21. Decide first.** Data translation is needed only when readers of different languages see the same data. Power BI has no feature for it: you build it. Weigh the number of distinct values, how long they are, and the upkeep, since new rows bring new text. Short names (products, categories) suit it; long descriptions do not. No check. Source: https://learn.microsoft.com/en-us/power-bi/guidance/data-translation

**22. The design Microsoft describes** has two parts, used together. First, the source gets one column per language for each translated field (for example Product Name English, Product Name Dutch); Microsoft's naming is entity, the word Translation, language; it is not required, but Translations Builder treats such columns specially. Second, a field parameter over those columns, not over measures, gives authors one field that switches column. Microsoft mentions that other designs exist but describes none. No check. Source: https://learn.microsoft.com/en-us/power-bi/guidance/data-translation-extend-schema

**23. The translation field parameter.** Build it like the shipped field parameter (section C of the file `model-objects.md` beside this one), with two changes. Source: https://learn.microsoft.com/en-us/power-bi/guidance/data-translation-implement-field
- Each label is the translated name of the field ("Product", "Product" in Dutch, and so on), not the column name: the label is the column header readers see. No check: a fourth value in a field parameter can hold anything, so the files do not show for certain that it is a language.
- Each tuple gets a fourth value, a lower-case language code such as "nl"; the new column (`[Value4]`) is renamed, hidden, and sorted by the order column. A visible language column already gives M822. No new check.

**24. The languages table.** One row per language: name, language code, culture name, sort order. Microsoft builds it in Power Query. Each translation field parameter gets a one-to-one relationship from its language column to this table. Then one filter on the table's language name, in "Filters on all pages" with "Require single selection", switches every translated field. Source: https://learn.microsoft.com/en-us/power-bi/guidance/data-translation-add-language-table ; https://learn.microsoft.com/en-us/power-bi/guidance/data-translation-synchronize-field
- Without the relationship, the parameter shows every language at once. Without the single-selection filter, a reader can pick two languages. No check: the files do not show for certain which column is the language column (rule 23).
- Microsoft's pages use the filter pane, not a slicer, and never tie this table to USERCULTURE. Copilot does not invent such a link.

**25. More than one translated field.** Repeat the field parameter per field and relate each one to the same languages table; one filter keeps them all in step. No new check: rule 24 covers each one. Source: the synchronize page in rule 24.

**26. Translated calendar names.** Build month and weekday name tables in Power Query: `Date.MonthName` and `Date.DayOfWeekName` take a culture name as their second argument; loop over the culture column of the languages table, one column per language. Relate them to the date table on month number and day number; sort each name column by its number column; then add a field parameter per table, related to the languages table. M113 already warns on a month-name column with no sort column; nothing checks weekday names. Source: https://learn.microsoft.com/en-us/power-bi/guidance/data-translation-calendar-table ; https://learn.microsoft.com/en-us/powerquery-m/date-dayofweekname

**27. Loading in the reader's language.** The `language` parameter of the report address sets metadata and label translations, but not the data language. For data, make one bookmark per language that only filters the languages table (Data on; Display and Current Page off) and add `bookmarkGuid=` with that bookmark's identifier to the address, after the `language` parameter. The mobile apps ignore the `language` parameter and use the device's setting. An embedded report sets `localeSettings.language` and filters the languages table in its `loaded` event. Source: https://learn.microsoft.com/en-us/power-bi/guidance/data-translation-load-report-bookmark ; the locale page in rule 1.
- No check: how the bookmark options map to the file properties is read from Microsoft's schema, not confirmed by a Microsoft Learn page (rule 17).

## What Copilot does

- Asks nothing in the middle of a task. What it cannot decide goes in the end note.
- Builds from the shipped examples in `tests/fixtures/examples/INDEX.md`: the field parameter `Sales Metric` (and `Sales Breakdown` for columns), the culture `nl-NL` and the label measure `Sales by Store Label`. A label measure returns text, so it has no format string: list it in section 9 of the brief with M009.
- Adds a language, a culture file or a label only when the brief names it.
- Marks for the developer what only Power BI Desktop or the service can do: testing each language in the service, the width of translated labels, publishing, and any bookmark captured in Desktop.

Checklist items: 7, 28, 55
