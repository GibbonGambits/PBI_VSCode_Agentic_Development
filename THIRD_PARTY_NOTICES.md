# Third-party notices

This template is licensed under the MIT licence (see `LICENSE`). Parts of its guidance follow rules and short examples from Microsoft's `skills-for-fabric` repository (https://github.com/microsoft/skills-for-fabric), which is also under the MIT licence. Its notice is reproduced here as that licence requires.

- Where: `.github/instructions/`, `.github/skills/pbi-semantic-model/`, `.github/skills/pbi-report/`, the made-up projects under `tests/fixtures/`, and the scripts, tests and README sections that restate these rules.
- What: the TMDL description, comment and annotation rules; the Power Query step naming and comment style; the place and written form of visual-level formatting values; the instruction to take `$schema` from an existing file; in the model standard, the naming, folder, hiding, data type and summarising rules and the calculated-table form of a measures table; in the layout standard, the 8-pixel grid, the margin and gap numbers, the title band and the slicer placement; in the standards added in round 3, the naming default for tables and columns, the form of a field parameter in the model and in a report, the values of a button's action, and the roles each visual type takes; in the shipped examples under `tests/fixtures/examples/`, the visual type identifiers and role names; in `scripts/desktop_bridge.py`, the commands of Microsoft's two Desktop Bridge tools (npm packages `@microsoft/powerbi-desktop-bridge-cli` and `@microsoft/powerbi-report-authoring-cli`, MIT, published from the same repository). The tools themselves are not shipped.

```
MIT License

Copyright (c) 2026 Microsoft Corporation

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Microsoft Analysis-Services (best practice rules)

Several rules of the model standard restate, in this template's own words, rules from `BestPracticeRules/BPARules.json` in Microsoft's `Analysis-Services` repository (https://github.com/microsoft/Analysis-Services), which is under the MIT licence.

- Where: the standard files under `.github/skills/pbi-semantic-model/references/`, and the checks in `scripts/check_project.py` and `scripts/model_rules.py` whose codes start with M.
- What: the conditions for hiding foreign keys and summed columns, the list of totalling functions, the limit of five calculated columns, summarising, data types of columns and relationships, and unused hidden objects; and, added in round 3, the rules on relationships (both directions, many-to-many, inactive, tables without one, snowflakes, primary keys), date tables, DAX (IFERROR, DIVIDE, FILTER, duplicate measures, TREATAS, time intelligence with DirectQuery), security rules, Power Query transformations, data categories, sort columns, flag columns, partition names, object names and invalid characters. Every one of the 71 rules is mapped in `maintenance/coverage.md`.

```
MIT License

Copyright (c) 2016 Microsoft

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Microsoft json-schemas (report schemas)

`scripts/schemas/` holds unchanged copies of every version of each schema Microsoft publishes for Power BI project files, from `microsoft/json-schemas` (https://github.com/microsoft/json-schemas), under the MIT licence ("Copyright (c) Microsoft Corporation"). Its licence file is kept beside the copies, as `scripts/schemas/LICENSE`. The copies are used by `scripts/json_schema.py` and the project check. `maintenance/sources.md` records the commit.

## GitHub awesome-copilot

The model standard also follows naming and folder guidance from the skill `powerbi-modeling` in GitHub's `awesome-copilot` repository (https://github.com/github/awesome-copilot), which is under the MIT licence ("Copyright GitHub, Inc."; the licence text is the MIT text shown above). The guidance is restated in this template's own words: the name `_Measures`, Title Case, the word "vs" in comparisons, and how columns and measures are written in DAX. In round 3 two of its instruction files were also read, for DAX practice (`power-bi-dax-best-practices.instructions.md`) and for report design (`power-bi-report-design-best-practices.instructions.md`); the DAX standard and the report standard name them at the rules they support, restated in new words.

## Mofaji Agentic-PBIP-Template

`Mofaji/Agentic-PBIP-Template` (https://github.com/Mofaji/Agentic-PBIP-Template) is under the MIT licence ("Copyright (c) 2026 Mofaji"; the licence text is the MIT text shown above). Every file was read: to map the topics it covers (`maintenance/coverage.md`), and to learn how Microsoft's Desktop Bridge tools are called. None of its text or code is in this template: `scripts/desktop_bridge.py` is written from the tools' own documentation, in Python.

## SQLBI

The DAX style, the DAX practice rules marked with a SQLBI address and the list of DAX patterns in `.github/skills/pbi-semantic-model/references/dax-standard.md` restate ideas from SQLBI's public articles (https://www.sqlbi.com), its DAX Patterns site (https://www.daxpatterns.com) and DAX Guide (https://dax.guide). SQLBI's material is not under an open licence. No text, code or image from it is in this template: each rule is written in new words and carries the address of the page, and the look-up skill forbids copying SQLBI text into a project.

The practice library (`.github/skills/pbi-practice-library/`) credits SQLBI as the source of its ideas. Its notes restate, one idea at a time, advice and facts from SQLBI's public articles and from two white papers that SQLBI's site links to as free downloads; the pages were read on 11 November 2026. Every note is written in this template's own words, is one or two lines long, and carries the year and the address of its article, which stays the place for the detail. No sentence, code sample or image of SQLBI is in the library, and no article is summarised. The skill tells Copilot to treat the notes as information and never to copy SQLBI material into a project.

## Microsoft Learn

Rules marked with a Microsoft Learn address restate Microsoft's public documentation in new words. The DAX function index lists function names and page addresses only. No page text is reproduced.

## Read for ideas or evidence only

- Kurt Buhler's `power-bi-agentic-development` repository is under GPL-3.0. It was read for ideas, again in round 3. No text, code or file from it is in this template. The Tabular Editor blog was read the same way, for working practices only.
- Microsoft's `powerbi-modeling-mcp` repository (MIT; the server itself is under Microsoft's own licence terms) was read to write the optional guidance on facts about the data. Nothing from it is in this template, and the template never installs it.
- Microsoft's Tabular Object Model library (NuGet package `Microsoft.AnalysisServices`) and Microsoft's report authoring command-line tool were used while building, to write and to check the shipped examples. Neither is shipped.
- Microsoft's `BCApps` repository (MIT) holds Power BI project files. They were read as evidence of what a saved project contains. Nothing from them is in this template.

The checklist links and the definition sources point to public pages of their owners; no text of those pages is reproduced beyond short definitions with their source named beside them.
