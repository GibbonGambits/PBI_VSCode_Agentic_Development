# Sources record

Every source the template follows or was checked against, with the commit or the date it was read, and its licence. GitHub Copilot does not read this folder.

Order of trust: 1 the owner's checklist; 2 Microsoft Learn; 3 Microsoft's own skills, best practice rules and schemas; 4 SQLBI, for DAX; 5 `data-goblin/power-bi-agentic-development`; 6 `github/awesome-copilot`; 7 `Mofaji/Agentic-PBIP-Template`. A lower source never overrides a higher one.

## The record

| Source | Address | Commit or date | Licence | How it is used |
|---|---|---|---|---|
| Microsoft Learn: Power BI, DAX, Power Query, Fabric, Analysis Services documentation | https://learn.microsoft.com/power-bi/ | read 2026-11-11 | Microsoft Learn terms of use | Restated in new words, each rule with its page address. Nothing copied beyond property and function names |
| Microsoft Learn: DAX reference table of contents | https://learn.microsoft.com/en-us/dax/toc.json | read 2026-11-11 | Microsoft Learn terms of use | Names and addresses of the 464 functions in the DAX function index |
| microsoft/skills-for-fabric | https://github.com/microsoft/skills-for-fabric | f8fac110ac3b, 2026-11-05 | MIT | Rules restated; file forms followed (visual roles, button actions, field parameters, theme registration). Notice in `THIRD_PARTY_NOTICES.md` |
| microsoft/Analysis-Services (best practice rules) | https://github.com/microsoft/Analysis-Services | d3ccb5032c90, 2026-07-08 | MIT | All 71 rules read, each mapped in `coverage.md`; rules restated. Notice in `THIRD_PARTY_NOTICES.md` |
| microsoft/json-schemas | https://github.com/microsoft/json-schemas | 235796d8b03b, 2026-11-10 | MIT | Every published version of each report schema is copied into `scripts/schemas` with its licence file |
| microsoft/powerbi-modeling-mcp | https://github.com/microsoft/powerbi-modeling-mcp | 2b25defb9751, 2026-09-29 | MIT for the repository; the server itself is under Microsoft's licence terms, which the developer accepts | Read to write the optional data-facts guidance. Nothing shipped |
| npm: @microsoft/powerbi-desktop-bridge-cli | https://www.npmjs.com/package/@microsoft/powerbi-desktop-bridge-cli | version 1.0.0, 2026-09-22 | MIT | Read to write `scripts/desktop_bridge.py`. Not shipped, not installed by the template |
| npm: @microsoft/powerbi-report-authoring-cli | https://www.npmjs.com/package/@microsoft/powerbi-report-authoring-cli | version 0.5.0, 2026-10-05 | MIT | Read for the reload call; its offline validator was run once on a copy of the report examples. Not shipped |
| npm: @microsoft/powerbi-core-visual-schema | https://www.npmjs.com/package/@microsoft/powerbi-core-visual-schema | version 0.1.3 | as stated in the package | Read for visual type identifiers and role names of the report examples. Not shipped |
| NuGet: Microsoft.AnalysisServices (Tabular Object Model) | https://www.nuget.org/packages/Microsoft.AnalysisServices | version 19.118.3 | Microsoft software licence | Used while building, to write and to load the model examples. Not shipped |
| VS Code and GitHub Copilot documentation | https://code.visualstudio.com/docs | read 2026-11-11 | as stated on the site | How Copilot finds instructions and skills, reaches the web and approves commands |
| SQLBI articles | https://www.sqlbi.com/articles/rules-for-dax-code-formatting/ | read 2026-11-11 | All rights reserved | DAX style and practice, restated in new words with addresses. No text, code or image copied |
| SQLBI articles and two white papers (the practice library) | https://www.sqlbi.com/articles/ | read 2026-11-11 | All rights reserved | The source of the ideas in the skill `pbi-practice-library`: each note restates one idea in new words, with the year and the address of its article. No text, code or image copied. The notes that were removed are listed in `library-removed.md` |
| SQLBI: DAX Patterns | https://www.daxpatterns.com/ | read 2026-11-11 | All rights reserved | The list of patterns with addresses. No formulas copied |
| SQLBI: DAX Guide | https://dax.guide/ | read 2026-11-11 | All rights reserved | A look-up site. Nothing copied |
| data-goblin/power-bi-agentic-development | https://github.com/data-goblin/power-bi-agentic-development | aa13b20b0142, 2026-11-10 | GPL-3.0 | Read only, for ideas. No text, code or file copied |
| github/awesome-copilot | https://github.com/github/awesome-copilot | eaaffd5d020b, 2026-11-11 | MIT | Naming and folder guidance restated |
| Mofaji/Agentic-PBIP-Template | https://github.com/Mofaji/Agentic-PBIP-Template | 651ce095c8ff, 2026-09-16 | MIT | Every file read: topics mapped in `coverage.md`; how the Desktop Bridge tools are called. No code used |
| The owner's checklist and theme | this repository | as committed | the owner's | Never changed; guarded by hashes in `scripts/check_template.py` |

Could not be read: the monthly "Feature Summary" posts on Microsoft's Power BI blog (the site refused automated reading). The feature inventory uses Microsoft Learn's update pages instead.

## The routine for refreshing

Do this when Microsoft ships a Power BI Desktop release you want to follow, or every three months.

1. `python scripts/refresh_sources.py check` compares each Git source above with its repository today and lists the ones that moved. It reads the table in this file: the first 7 or more characters of the commit are enough.
2. For each source that moved, read what changed (`git log` and `git diff` between the recorded commit and the new one, in a clone outside this repository). Update the guidance and the checks where a rule changed, and the rows of `coverage.md` and `feature-inventory.md` that it touches. Keep the order of trust.
3. `python scripts/refresh_sources.py schemas <clone of microsoft/json-schemas>` copies every schema version. Then update the `$schema` addresses in the shipped examples if a new version exists, and run the tests.
4. `python scripts/refresh_sources.py dax-index` rebuilds the DAX function index from Microsoft Learn.
5. Read Microsoft Learn's "What's new" pages since the last date in the feature inventory's release-notes log, and add the new features as rows: status, version, limits, which standards touch them. A feature that lives in the files gets guidance, a shipped example and a check where the files can show a breach.
6. Check the release status of every row marked preview: a feature that became generally available loses its mark, and its example moves out of the `preview` folder.
7. Write the new commits and today's date in the table above.
8. `python -m unittest discover -s tests` and `python scripts/check_template.py`.
9. One pull request. A person approves it. Never push to main.

Nothing in this routine publishes, deploys or connects to a workspace.
