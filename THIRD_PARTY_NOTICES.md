# Third-party notices

This template is licensed under the MIT licence (see `LICENSE`). Parts of its guidance follow rules and short examples from Microsoft's `skills-for-fabric` repository (https://github.com/microsoft/skills-for-fabric), which is also under the MIT licence. Its notice is reproduced here as that licence requires.

- Where: `.github/instructions/`, `.github/skills/pbi-semantic-model/`, `.github/skills/pbi-report/`, the made-up projects under `tests/fixtures/`, and the scripts, tests and README sections that restate these rules.
- What: the TMDL description, comment and annotation rules; the Power Query step naming and comment style; the place and written form of visual-level formatting values; the instruction to take `$schema` from an existing file; in the model standard, the naming, folder, hiding, data type and summarising rules and the calculated-table form of a measures table; in the layout standard, the 8-pixel grid, the margin and gap numbers, the title band and the slicer placement.

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

- Where: `.github/skills/pbi-semantic-model/references/model-standard.md`, and the checks in `scripts/check_project.py` whose codes start with M.
- What: the conditions for hiding foreign keys and summed columns, the list of totalling functions, the limit of five calculated columns, summarising, data types of columns and relationships, and unused hidden objects.

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

## GitHub awesome-copilot

The model standard also follows naming and folder guidance from the skill `powerbi-modeling` in GitHub's `awesome-copilot` repository (https://github.com/github/awesome-copilot), which is under the MIT licence ("Copyright GitHub, Inc."; the licence text is the MIT text shown above). The guidance is restated in this template's own words: the name `_Measures`, Title Case, the word "vs" in comparisons, and how columns and measures are written in DAX.

## Read for ideas or evidence only

- Kurt Buhler's `power-bi-agentic-development` repository is under GPL-3.0. It was read for ideas. No text, code or file from it is in this template.
- Microsoft's `BCApps` repository (MIT) holds Power BI project files. They were read as evidence of what a saved project contains. Nothing from them is in this template.

The checklist links and the definition sources point to public pages of their owners; no text of those pages is reproduced beyond short definitions with their source named beside them.
