# Coverage

This working paper proves, row by row, how far the template covers the native practices of Power BI. It lists one row per practice from five baselines, and says where the template covers each one. Built on 11 November 2026 from the research of that day, and brought up to date with the repository later that day. It is a maintenance paper: Copilot does not read this folder (`.github/copilot-instructions.md`).

## Status words

- **covered**: the template has guidance in its own words with the source address, a shipped example where one applies, and a script check where the project files can show the breach. When the files cannot show it, the Check column says "files cannot show it" and guidance is enough.
- **soft**: the practice is only touched lightly: a checklist item, or guidance with no check although the files could show the breach (this paper uses soft for both; the Check column says which). It should not remain.
- **missing**: nothing in the template. It should not remain.
- **out of scope**: custom visuals; other vendors' tools; other systems such as email; publishing and deployment steps; paginated reports, migration, adoption roadmap, implementation planning, Center of Excellence, gateway sizing, activity log; a source's own styling choices.
- **outside this template**: a native feature that lives outside the project files (a Desktop option, a service or workspace setting).
- **not adopted**: a rule a source gives that Microsoft does not support, or that a higher source overrules; the reason is given.

A row is judged by its main practice. A smaller point inside it that has no check is named in the row, and does not change its status unless the row is about that point. A page row in A and B takes the weakest status of its practices in A2.

Order of trust (a lower source never overrides a higher one): 1 the owner's checklist; 2 Microsoft Learn; 3 Microsoft's skills (microsoft/skills-for-fabric), best practice rules (microsoft/Analysis-Services) and schemas (microsoft/json-schemas); 4 SQLBI, for DAX; 5 data-goblin/power-bi-agentic-development (GPL: ideas only); 6 github/awesome-copilot; 7 Mofaji/Agentic-PBIP-Template.

## How to refresh this file

Follow the routine at the top of `scripts/refresh_sources.py`: run `python scripts/refresh_sources.py check`; for each source that moved, read what changed and update the guidance, the checks and this file where a rule changed; refresh the schemas and the DAX index; run the tests and `python scripts/check_template.py`; open one pull request. When a guidance file or a check changes, re-read the rows that name it here.

## Short names used in the tables

| Short name | File |
| --- | --- |
| CI | `.github/copilot-instructions.md` |
| TI | `.github/instructions/tmdl.instructions.md` |
| PI | `.github/instructions/pbir.instructions.md` |
| SM | `.github/skills/pbi-semantic-model/SKILL.md` |
| MS | `.github/skills/pbi-semantic-model/references/model-standard.md` |
| RD | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md` |
| DS | `.github/skills/pbi-semantic-model/references/dax-standard.md` |
| SS | `.github/skills/pbi-semantic-model/references/storage-and-security.md` |
| MO | `.github/skills/pbi-semantic-model/references/model-objects.md` |
| TM | `.github/skills/pbi-semantic-model/references/tmdl.md` |
| DE | `.github/skills/pbi-semantic-model/references/descriptions.md` |
| DF | `.github/skills/pbi-semantic-model/references/data-facts.md` |
| FX | `.github/skills/pbi-semantic-model/references/dax-functions.md` |
| MF | `.github/skills/pbi-semantic-model/references/more-model-features.md` |
| ML | `.github/skills/pbi-semantic-model/references/multiple-languages.md` |
| SR | `.github/skills/pbi-report/SKILL.md` |
| RS | `.github/skills/pbi-report/references/report-standard.md` |
| LS | `.github/skills/pbi-report/references/layout-standard.md` |
| PV | `.github/skills/pbi-report/references/pages-and-visuals.md` |
| TH | `.github/skills/pbi-report/references/theme.md` |
| DB | `.github/skills/pbi-report/references/desktop-bridge.md` |
| VF | `.github/skills/pbi-report/references/visual-features.md` |
| CR | `.github/skills/pbi-checklist-review/SKILL.md` |
| NF | `.github/skills/pbi-checklist-review/references/native-features.md` |
| LK | `.github/skills/pbi-lookup/SKILL.md` |
| PL | `.github/skills/pbi-practice-library/SKILL.md` and the files under its `references/` folder (information only: no check reads them) |
| EX | tests/fixtures/examples/INDEX.md (example names and paths in the tables start at tests/fixtures/examples/) |

A number after a short name is the rule number in that file (MS 7 is rule 7 of the model standard); a letter is a section (RS C). "Item N" is item N of `checklist/checklist.md`. "The brief" is `docs/report-brief.md`. Codes and levels (fail, warn, note) are those in the docstring at the top of `scripts/check_project.py`; the logic is in `scripts/check_project.py`, `scripts/model_rules.py` and `scripts/report_rules.py`.

## Summary

| Baseline | covered | out of scope | outside this template | not adopted | soft | missing | Rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A. Guidance index pages | 40 | 111 | 9 | 0 | 0 | 0 | 160 |
| A2. Practices on the in-scope pages | 205 | 5 | 26 | 0 | 0 | 0 | 236 |
| B. DAX best-practice pages | 10 | 0 | 1 | 0 | 0 | 0 | 11 |
| C. Best practice rules | 66 | 0 | 1 | 4 | 0 | 0 | 71 |
| D. Other sources, topic by topic | 154 | 6 | 6 | 23 | 0 | 0 | 189 |
| E. Mofaji/Agentic-PBIP-Template | 54 | 8 | 0 | 7 | 0 | 0 | 69 |
| F. The owner's minimum list | 57 | 0 | 0 | 0 | 0 | 0 | 57 |
| **Total** | **586** | **130** | **43** | **34** | **0** | **0** | **793** |

A and B count pages; A2 counts the practices on the in-scope pages of A and on the three DAX best-practice pages outside the index, so B repeats the DAX practices page by page. No row is still open (section G).

## A. Microsoft Learn: Power BI guidance pages

All 160 links of the table of contents of https://learn.microsoft.com/en-us/power-bi/guidance/ (read on 11 November 2026), in its order. The 19 pages on multiple-language reports were not read in that research; their status comes from their titles and from what the template holds. Eleven of them (rows 45, 46, 49, 51 and 56 to 62) are restated in ML, and have practice rows in A2.

| # | Page | Address | Status | Where it is covered (file; codes) |
| ---: | --- | --- | --- | --- |
| 1 | Power BI guidance documentation | https://learn.microsoft.com/en-us/power-bi/guidance/ | out of scope | the index page itself; its pages are the other rows |
| 2 | Optimization guide for Power BI (Overview) | https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization | covered | MS; RD; DS; SS; MO; RS; NF; codes M0xx-M1xx, D001, U00x, V006 |
| 3 | The importance of query folding (Transform and shape data) | https://learn.microsoft.com/en-us/power-bi/guidance/power-query-folding | covered | SS 2, 3, 26; P002, M701, M708 |
| 4 | Referencing Power Query queries (Transform and shape data) | https://learn.microsoft.com/en-us/power-bi/guidance/power-query-referenced-queries | covered | SS 4; P003 |
| 5 | Disable Power Query background refresh (Transform and shape data) | https://learn.microsoft.com/en-us/power-bi/guidance/power-query-background-refresh | covered | SS 11 (guidance; no example and no check: it is a Power BI Desktop option that no project file holds) |
| 6 | Best practices for dataflows (Transform and shape data) | https://learn.microsoft.com/en-us/power-bi/transform-model/dataflows/dataflows-introduction-self-service | outside this template | SS 4; NF (dataflows live in the service) |
| 7 | What is a star schema? (Data modeling) | https://learn.microsoft.com/en-us/power-bi/guidance/star-schema | covered | RD A (1, with junk and degenerate dimensions); MS 7, 9; M412, M406, M103, M107, M120, U006 |
| 8 | Reduce data model size (Data modeling) | https://learn.microsoft.com/en-us/power-bi/guidance/import-modeling-data-reduction | covered | SS B, 12; MS 8; M105, M106, M107, M201, M401, P007 |
| 9 | Design guidance for date tables (Data modeling) | https://learn.microsoft.com/en-us/power-bi/guidance/model-date-tables | covered | RD C; M402-M404 |
| 10 | Auto date/time guidance (Data modeling) | https://learn.microsoft.com/en-us/power-bi/guidance/auto-date-time | covered | RD 29; M401 |
| 11 | One-to-one relationships (Data modeling) | https://learn.microsoft.com/en-us/power-bi/guidance/relationships-one-to-one | covered | RD 22; M409 |
| 12 | Many-to-many relationships (Data modeling) | https://learn.microsoft.com/en-us/power-bi/guidance/relationships-many-to-many | covered | RD 9, 18-20; M405-M407, M416, M102; EX Store[Store Key] (isNullable: false) |
| 13 | Active vs inactive relationships (Data modeling) | https://learn.microsoft.com/en-us/power-bi/guidance/relationships-active-inactive | covered | RD 7, 23, 24; M410, M414, M415, U006 |
| 14 | Bi-directional relationships (Data modeling) | https://learn.microsoft.com/en-us/power-bi/guidance/relationships-bidirectional-filtering | covered | RD 18; M405, M408 |
| 15 | Relationship troubleshooting (Data modeling) | https://learn.microsoft.com/en-us/power-bi/guidance/relationships-troubleshoot | covered | RD 10-27; SS 24, 37; M901, M109, M110, M609, U008 |
| 16 | DirectQuery model guidance (Data modeling) | https://learn.microsoft.com/en-us/power-bi/guidance/directquery-model-guidance | covered | SS 23-24; RS 54; M513, M701-M706, U008, U104, U106 |
| 17 | Composite model guidance (Data modeling) | https://learn.microsoft.com/en-us/power-bi/guidance/composite-model-guidance | covered | SS 22-25; RS 30; MF 8; M705, M706, U004 |
| 18 | Row-level security (RLS) guidance (Data modeling) | https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance | covered | SS D (28-38); M601-M605, M609, M414, M415 |
| 19 | Power Platform modeling guidance (Data modeling) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-modeling-guidance-for-power-platform | covered | SS 6; RD 1; P004, M706 |
| 20 | Migrate AAS models to Power BI Premium (Data modeling) | https://learn.microsoft.com/en-us/power-bi/guidance/migrate-azure-analysis-services-to-power-bi | out of scope | migration |
| 21 | Migrate AAS models to Power BI Premium scenarios (Data modeling) | https://learn.microsoft.com/en-us/power-bi/guidance/migrate-azure-analysis-services-to-power-bi-migration-scenarios | out of scope | migration |
| 22 | Appropriate use of error functions (DAX) | https://learn.microsoft.com/en-us/dax/best-practices/dax-error-functions | covered | DS 1, 2; RD 9; M501, M502, M416; EX Store[Store Key] (isNullable: false) |
| 23 | Avoid converting BLANKs to values (DAX) | https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-converting-blank | covered | DS 7; M506 |
| 24 | Avoid using FILTER as a filter argument (DAX) | https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-avoid-filter-as-filter-argument | covered | DS 6; M505 |
| 25 | Column and measure references (DAX) | https://learn.microsoft.com/en-us/dax/best-practices/dax-column-measure-references | covered | DS 10; M010, M006, M119 |
| 26 | DIVIDE function vs divide operator (/) (DAX) | https://learn.microsoft.com/en-us/dax/best-practices/dax-divide-function-operator | covered | DS 2; M502, M518 |
| 27 | Use COUNTROWS instead of COUNT (DAX) | https://learn.microsoft.com/en-us/dax/best-practices/dax-countrows | covered | DS 3; M503 |
| 28 | Use SELECTEDVALUE instead of VALUES (DAX) | https://learn.microsoft.com/en-us/dax/best-practices/dax-selectedvalue | covered | DS 4, 5; M504, M517 |
| 29 | Use variables to improve formulas (DAX) | https://learn.microsoft.com/en-us/dax/best-practices/dax-variables | covered | DS 8, 9; M507, M514 |
| 30 | Sample model (DAX) | https://learn.microsoft.com/en-us/dax/dax-sample-model | out of scope | a sample model to download; states no practice |
| 31 | Separate reports from models (Power BI reports) | https://learn.microsoft.com/en-us/power-bi/guidance/report-separate-from-model | covered | RS L (65, 66); MS (Existing models); B001, V012 |
| 32 | Extend visuals with report page tooltips (Power BI reports) | https://learn.microsoft.com/en-us/power-bi/guidance/report-page-tooltips | covered | RS C; V002-V005, V013, H002 |
| 33 | Use report page drillthrough (Power BI reports) | https://learn.microsoft.com/en-us/power-bi/guidance/report-drillthrough | covered | RS D; V001, V013, V014 |
| 34 | When to use paginated reports (Power BI paginated reports) | https://learn.microsoft.com/en-us/power-bi/guidance/report-paginated-or-power-bi | out of scope | paginated reports |
| 35 | Data retrieval guidance (Power BI paginated reports) | https://learn.microsoft.com/en-us/power-bi/guidance/report-paginated-data-retrieval | out of scope | paginated reports |
| 36 | Performance and scalability considerations (Power BI paginated reports) | https://learn.microsoft.com/en-us/power-bi/guidance/report-paginated-performance-scalability-considerations | out of scope | paginated reports |
| 37 | Image use guidance (Power BI paginated reports) | https://learn.microsoft.com/en-us/power-bi/guidance/report-paginated-image | out of scope | paginated reports |
| 38 | Use cascading parameters (Power BI paginated reports) | https://learn.microsoft.com/en-us/power-bi/guidance/paginated-report-cascading-parameter | out of scope | paginated reports |
| 39 | Avoid blank pages when printing (Power BI paginated reports) | https://learn.microsoft.com/en-us/power-bi/guidance/report-paginated-blank-page | out of scope | paginated reports |
| 40 | Migrate .rdl reports to Power BI (Power BI paginated reports) | https://learn.microsoft.com/en-us/power-bi/guidance/migrate-ssrs-reports-to-power-bi | out of scope | paginated reports |
| 41 | Publish .rdl files to Power BI (Power BI paginated reports) | https://learn.microsoft.com/en-us/power-bi/guidance/publish-reporting-services-power-bi-service | out of scope | paginated reports |
| 42 | Retire unused .rdl files (Power BI paginated reports) | https://learn.microsoft.com/en-us/power-bi/guidance/retire-unused-reports-ssrs | out of scope | paginated reports |
| 43 | Develop scalable multitenancy applications (Development) | https://learn.microsoft.com/en-us/power-bi/guidance/develop-scalable-multitenancy-apps-with-powerbi-embedding | out of scope | embedding in another application (another system) |
| 44 | Plan translation for reports (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/multiple-language-translation | covered | MO D (Translations and cultures; this page is its source); EX cultures/nl-NL.tmdl; no check: files cannot show it (which languages are needed) |
| 45 | Use locale values in reports (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/multiple-language-locale | covered | ML A (1-6), 16; EX cultures/nl-NL.tmdl, Sales by Store Label; M524, M525, V019 |
| 46 | Use best practices to localize reports (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/multiple-language-best-practice | covered | ML B (7, 11, 12); no check: a file does not show the rendered width |
| 47 | Create reports with Translations Builder (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/translation-builder | outside this template | Translations Builder is a separate tool; what it writes (cultures) is covered in MO D |
| 48 | Add a language to a report (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/translation-builder-add-language | outside this template | a Translations Builder step; result covered in MO D |
| 49 | Add a Localized Labels table (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/translation-builder-localize-label | covered | ML C (14-17), 8-10; EX Sales by Store Label; M525, V020 |
| 50 | Generate machine translations (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/translation-builder-machine-translation | out of scope | another system (machine translation service) |
| 51 | Multiple-language page navigation (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/multiple-language-page-navigation | covered | ML D (18-20); V021 |
| 52 | Enable workflows for human translation (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/translation-workflow-human | outside this template | a translation workflow outside the files |
| 53 | Export translation sheets (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/translation-sheet-export | outside this template | a Translations Builder export |
| 54 | Import translation sheets (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/translation-sheet-import | outside this template | a Translations Builder import |
| 55 | Manage enterprise-level translations (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/translation-manage-data-model-enterprise | outside this template | a translation workflow across models |
| 56 | Implement data translation (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/data-translation | covered | ML 21; no check: the choice is the developer's |
| 57 | Support data translations (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/data-translation-extend-schema | covered | ML 22; EX Sales Breakdown (field parameter over columns) |
| 58 | Data translation with field parameters (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/data-translation-implement-field | covered | ML 23; EX Sales Breakdown; M822 |
| 59 | Add the languages table (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/data-translation-add-language-table | covered | ML 24; no check: the files do not show for certain which column is the language column |
| 60 | Synchronize field parameters (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/data-translation-synchronize-field | covered | ML 25, 12 |
| 61 | Data translation calendar table (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/data-translation-calendar-table | covered | ML 26; M113 |
| 62 | Load multiple-language reports (Build multiple-language reports) | https://learn.microsoft.com/en-us/power-bi/guidance/data-translation-load-report-bookmark | covered | ML 27; no check: the bookmark mapping is not confirmed |
| 63 | On-premises data gateway sizing (Admin and deployment) | https://learn.microsoft.com/en-us/power-bi/guidance/gateway-onprem-sizing | out of scope | gateway sizing |
| 64 | Monitor report performance (Admin and deployment) | https://learn.microsoft.com/en-us/power-bi/guidance/monitor-report-performance | outside this template | Desktop and service tools; CR (item 68) |
| 65 | Troubleshoot report performance (Admin and deployment) | https://learn.microsoft.com/en-us/power-bi/guidance/report-performance-troubleshoot | outside this template | service and Desktop tools; CR (item 68) |
| 66 | Deployment pipelines best practices (Admin and deployment) | https://learn.microsoft.com/en-us/fabric/cicd/best-practices-cicd | out of scope | deployment |
| 67 | Access the Power BI activity log (Admin and deployment) | https://learn.microsoft.com/en-us/power-bi/guidance/admin-activity-log | out of scope | activity log |
| 68 | Migration overview (Migrate to Power BI) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-migration-overview | out of scope | migration |
| 69 | Prepare to migrate (Migrate to Power BI) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-migration-pre-migration-steps | out of scope | migration |
| 70 | Gather requirements (Migrate to Power BI) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-migration-requirements | out of scope | migration |
| 71 | Plan deployment (Migrate to Power BI) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-migration-planning | out of scope | migration |
| 72 | Conduct proof of concept (Migrate to Power BI) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-migration-proof-of-concept | out of scope | migration |
| 73 | Create content (Migrate to Power BI) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-migration-create-validate-content | out of scope | migration |
| 74 | Deploy to Power BI (Migrate to Power BI) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-migration-deploy-support-monitor | out of scope | migration |
| 75 | Learn from customer Power BI migrations (Migrate to Power BI) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-migration-learn-from-customers | out of scope | migration |
| 76 | Introduction (Fabric adoption roadmap) | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap | out of scope | adoption roadmap |
| 77 | Maturity levels (Fabric adoption roadmap) | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-maturity-levels | out of scope | adoption roadmap |
| 78 | Data culture (Fabric adoption roadmap) | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-data-culture | out of scope | adoption roadmap |
| 79 | Executive sponsorship (Fabric adoption roadmap) | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-executive-sponsorship | out of scope | adoption roadmap |
| 80 | Business alignment (Fabric adoption roadmap) | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-business-alignment | out of scope | adoption roadmap |
| 81 | Content ownership (Fabric adoption roadmap) | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-content-ownership-and-management | out of scope | adoption roadmap |
| 82 | Content delivery scope (Fabric adoption roadmap) | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-content-delivery-scope | out of scope | adoption roadmap |
| 83 | Center of Excellence (Fabric adoption roadmap) | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-center-of-excellence | out of scope | adoption roadmap |
| 84 | Governance (Fabric adoption roadmap) | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-governance | out of scope | adoption roadmap |
| 85 | Mentoring and user enablement (Fabric adoption roadmap) | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-mentoring-and-user-enablement | out of scope | adoption roadmap |
| 86 | Community of practice (Fabric adoption roadmap) | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-community-of-practice | out of scope | adoption roadmap |
| 87 | User support (Fabric adoption roadmap) | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-user-support | out of scope | adoption roadmap |
| 88 | System oversight (Fabric adoption roadmap) | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-system-oversight | out of scope | adoption roadmap |
| 89 | Change management (Fabric adoption roadmap) | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-change-management | out of scope | adoption roadmap |
| 90 | Conclusion (Fabric adoption roadmap) | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-conclusion | out of scope | adoption roadmap |
| 91 | Introduction (Implementation planning) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-introduction | out of scope | implementation planning |
| 92 | BI strategy overview (Implementation planning > BI strategy) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-bi-strategy-overview | out of scope | implementation planning |
| 93 | BI strategic planning (Implementation planning > BI strategy) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-bi-strategy-bi-strategic-planning | out of scope | implementation planning |
| 94 | BI tactical planning (Implementation planning > BI strategy) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-bi-strategy-bi-tactical-planning | out of scope | implementation planning |
| 95 | BI solution planning (Implementation planning > BI strategy) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-bi-strategy-bi-solution-planning | out of scope | implementation planning |
| 96 | Tenant setup (Implementation planning) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-tenant-setup | out of scope | implementation planning |
| 97 | User tools and devices (Implementation planning) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-user-tools-devices | out of scope | implementation planning |
| 98 | Subscriptions, licenses, and trials (Implementation planning) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-subscriptions-licenses-trials | out of scope | implementation planning |
| 99 | Tenant administration (Implementation planning) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-tenant-administration | out of scope | implementation planning |
| 100 | Workspaces overview (Implementation planning > Workspaces) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-workspaces-overview | out of scope | implementation planning |
| 101 | Tenant-level planning (Implementation planning > Workspaces) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-workspaces-tenant-level-planning | out of scope | implementation planning |
| 102 | Workspace-level planning (Implementation planning > Workspaces) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-workspaces-workspace-level-planning | out of scope | implementation planning |
| 103 | CLM overview (Implementation planning > Content lifecycle management (CLM)) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-content-lifecycle-management-overview | out of scope | implementation planning |
| 104 | Plan and design content (Implementation planning > Content lifecycle management (CLM)) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-content-lifecycle-management-plan-design | out of scope | implementation planning |
| 105 | Develop and manage content (Implementation planning > Content lifecycle management (CLM)) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-content-lifecycle-management-develop-manage | out of scope | implementation planning |
| 106 | Validate content (Implementation planning > Content lifecycle management (CLM)) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-content-lifecycle-management-validate | out of scope | implementation planning |
| 107 | Deploy content (Implementation planning > Content lifecycle management (CLM)) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-content-lifecycle-management-deploy | out of scope | implementation planning |
| 108 | Support and monitor content (Implementation planning > Content lifecycle management (CLM)) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-content-lifecycle-management-support-monitor | out of scope | implementation planning |
| 109 | Retire and archive content (Implementation planning > Content lifecycle management (CLM)) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-content-lifecycle-management-retire-archive | out of scope | implementation planning |
| 110 | Content distribution and sharing (Implementation planning) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-content-distribution-sharing | out of scope | implementation planning |
| 111 | Security overview (Implementation planning > Security) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-security-overview | out of scope | implementation planning |
| 112 | Tenant-level planning (Implementation planning > Security) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-security-tenant-level-planning | out of scope | implementation planning |
| 113 | Report consumer planning (Implementation planning > Security) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-security-report-consumer-planning | out of scope | implementation planning |
| 114 | Content creator planning (Implementation planning > Security) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-security-content-creator-planning | out of scope | implementation planning |
| 115 | Info protection and DLP overview (Implementation planning > Information protection and data loss prevention) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-info-protection-data-loss-prevention-overview | out of scope | implementation planning |
| 116 | Org-level info protection (Implementation planning > Information protection and data loss prevention) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-organization-level-info-protection | out of scope | implementation planning |
| 117 | Info protection for Power BI (Implementation planning > Information protection and data loss prevention) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-info-protection | out of scope | implementation planning |
| 118 | DLP for Power BI (Implementation planning > Information protection and data loss prevention) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-data-loss-prevention | out of scope | implementation planning |
| 119 | Defender for Cloud Apps for Power BI (Implementation planning > Information protection and data loss prevention) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-defender-for-cloud-apps | out of scope | implementation planning |
| 120 | Auditing of info protection and DLP for Power BI (Implementation planning > Information protection and data loss prevention) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-auditing-info-protection-data-loss-prevention | out of scope | implementation planning |
| 121 | Data gateways (Implementation planning) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-data-gateways | out of scope | implementation planning |
| 122 | Integration with other services (Implementation planning) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-integration-with-other-services | out of scope | implementation planning |
| 123 | Auditing and monitoring overview (Implementation planning > Auditing and monitoring) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-auditing-monitoring-overview | out of scope | implementation planning |
| 124 | Report-level auditing (Implementation planning > Auditing and monitoring) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-auditing-monitoring-report-level-auditing | out of scope | implementation planning |
| 125 | Data-level auditing (Implementation planning > Auditing and monitoring) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-auditing-monitoring-data-level-auditing | out of scope | implementation planning |
| 126 | Tenant-level auditing (Implementation planning > Auditing and monitoring) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-auditing-monitoring-tenant-level-auditing | out of scope | implementation planning |
| 127 | Tenant-level monitoring (Implementation planning > Auditing and monitoring) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-auditing-monitoring-tenant-level-monitoring | out of scope | implementation planning |
| 128 | Adoption tracking (Implementation planning) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-adoption-tracking | out of scope | implementation planning |
| 129 | Usage scenarios overview (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-overview | out of scope | implementation planning |
| 130 | Personal BI (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-personal-bi | out of scope | implementation planning |
| 131 | Team BI (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-team-bi | out of scope | implementation planning |
| 132 | Departmental BI (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-departmental-bi | out of scope | implementation planning |
| 133 | Enterprise BI (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-enterprise-bi | out of scope | implementation planning |
| 134 | Managed self-service BI (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-managed-self-service-bi | out of scope | implementation planning |
| 135 | Customizable managed self-service BI (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-customizable-managed-self-service-bi | out of scope | implementation planning |
| 136 | Self-service data preparation (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-self-service-data-preparation | out of scope | implementation planning |
| 137 | Advanced data preparation (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-advanced-data-preparation | out of scope | implementation planning |
| 138 | Prototyping and sharing (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-prototyping-and-sharing | out of scope | implementation planning |
| 139 | Self-service content publishing (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-self-service-content-publishing | out of scope | implementation planning |
| 140 | Enterprise content publishing (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-enterprise-content-publishing | out of scope | implementation planning |
| 141 | Advanced data model management (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-advanced-data-model-management | out of scope | implementation planning |
| 142 | Self-service real-time analytics (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-self-service-real-time-analytics | out of scope | implementation planning |
| 143 | Embed for your organization (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-embed-for-your-organization | out of scope | implementation planning |
| 144 | Embed for your customers (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-embed-for-your-customers | out of scope | implementation planning |
| 145 | On-premises reporting (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-on-premises-reporting | out of scope | implementation planning |
| 146 | Usage scenario diagrams (Implementation planning > Usage scenarios) | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-diagrams | out of scope | implementation planning |
| 147 | Microsoft's BI transformation (Microsoft's Center of Excellence (COE)) | https://learn.microsoft.com/en-us/power-bi/guidance/center-of-excellence-microsoft-business-intelligence-transformation | out of scope | Center of Excellence |
| 148 | How Microsoft established a COE (Microsoft's Center of Excellence (COE)) | https://learn.microsoft.com/en-us/power-bi/guidance/center-of-excellence-establish | out of scope | Center of Excellence |
| 149 | BI solution architecture in the COE (Microsoft's Center of Excellence (COE)) | https://learn.microsoft.com/en-us/power-bi/guidance/center-of-excellence-business-intelligence-solution-architecture | out of scope | Center of Excellence |
| 150 | White papers overview (White papers) | https://learn.microsoft.com/en-us/power-bi/guidance/whitepapers | out of scope | tenant security and capacity papers (implementation planning) |
| 151 | Power BI security white paper (White papers) | https://learn.microsoft.com/en-us/power-bi/guidance/white-paper-powerbi-security | out of scope | tenant security and capacity papers (implementation planning) |
| 152 | Power BI Premium deployment (White papers) | https://learn.microsoft.com/en-us/power-bi/guidance/whitepaper-fabric-capacity-deployment | out of scope | tenant security and capacity papers (implementation planning) |
| 153 | Contribute to Fabric docs (Resources) | https://learn.microsoft.com/en-us/contribute/ | out of scope | a link, not a guidance page |
| 154 | Microsoft Q & A (Resources) | https://learn.microsoft.com/en-us/answers/ | out of scope | a link, not a guidance page |
| 155 | Fabric ideas (Resources > Provide feedback) | https://ideas.fabric.microsoft.com/ | out of scope | a link, not a guidance page |
| 156 | Azure feedback (Resources > Provide feedback) | https://feedback.azure.com/ | out of scope | a link, not a guidance page |
| 157 | Community (Resources) | https://community.fabric.microsoft.com/ | out of scope | a link, not a guidance page |
| 158 | Service updates (Resources) | https://azure.microsoft.com/updates/ | out of scope | a link, not a guidance page |
| 159 | Azure Status (Resources) | https://azure.status.microsoft/ | out of scope | a link, not a guidance page |
| 160 | Microsoft Learn training (Resources) | https://learn.microsoft.com/en-us/training/fabric/ | out of scope | a link, not a guidance page |

## A2. Practices on those pages

One row per practice of the in-scope pages, restated in new words.

| Page | Practice | Status | Guidance | Example | Check |
| --- | --- | --- | --- | --- | --- |
| Optimization | Choose Import, DirectQuery or a mix on purpose, and follow the page for that mode | covered | SS 22, 23 | EX Sales.tmdl (Import); storage/DirectQuery, storage/DirectLake | files cannot show it (the reason lives in the brief); M706, M702 (warn) on the mode's details |
| Optimization | Plain business names for tables, columns and measures | covered | MS 3; RD 41-43 | EX Examples.SemanticModel | M007 (fail), M008, M118 (warn) |
| Optimization | A description on every table, column and measure | covered | DE; TI 1 | every EX model file | D001 (fail), I001 (note) |
| Optimization | Hide keys and columns that a measure already totals | covered | MS 7 | EX Sales.tmdl (hidden keys) | M102, M103 (warn) |
| Optimization | Hierarchies for natural drill paths | covered | RD 40; MO D (Hierarchies) | EX Date.tmdl (Calendar), Product.tmdl | U007 (note), M902 (fail) |
| Optimization | Totals come from measures, so every report adds up the same way | covered | MS 9 | EX _Measures.tmdl | M107 (fail), M103 (warn) |
| Optimization | Default number and date formats set in the model | covered | MS 4, 12 | EX _Measures.tmdl, Date.tmdl | M009 (fail), M112 (warn) |
| Optimization | Data categories on places, links and images | covered | RD 36 | EX Store.tmdl (City, WebUrl) | M114 (warn) |
| Optimization | Consider calculation groups, field parameters, what-if parameters, grouping and binning | covered | MO B, C, D; NF (Model); MF 12 (groups and bins: not built, Learn shows only the Desktop dialog) | EX Time Calculation.tmdl, Sales Metric.tmdl, Discount Percentage.tmdl | U002, U003, U103 (note) |
| Optimization | Dashboard tiles come from a cache (per user with dynamic RLS) | outside this template | NF (Outside the project files: dashboards) | - | files cannot show it |
| Optimization | Use a dashboard as a cached landing page | outside this template | NF (Outside the project files: dashboards) | - | files cannot show it |
| Optimization | Give a large table visual the most restrictive filter, such as Top N | covered | NF (Report pages: filter types); RS 51-52 | EX Charts_Bars_Bar_LargestStores (Top N filter) | files cannot show it (row counts are not in the files) |
| Optimization | Only the visuals a page needs; detail to drillthrough and tooltip pages | covered | RS 63-64 | EX Drillthrough_Store, Tooltip_StoreSales | V006 (fail), V007 (warn) |
| Optimization | Test custom visuals for speed | out of scope | custom visuals (RS 48) | - | - |
| Optimization | Paginated report data retrieval and memory | out of scope | paginated reports | - | - |
| Optimization | Capacity settings, gateway size, sources and capacity in one region | outside this template | NF (Outside the project files: gateway, capacity) | - | files cannot show it |
| Optimization | Monitor performance in Desktop and in production | outside this template | Performance Analyzer is a Desktop tool: RS K, CR (item 68) | - | files cannot show it |
| Query folding | A DirectQuery or Dual table's query folds completely | covered | SS 2 | EX storage/DirectQuery.SemanticModel | files cannot show it (M702 warns on extra steps in a DirectQuery query) |
| Query folding | Import from a database: aim for full folding, keep engine work small | covered | SS 2; DF | - | files cannot show it |
| Query folding | Find the step that stops folding; put folding steps first | covered | SS 2 (View Native Query in Desktop) | - | files cannot show it |
| Query folding | Native SQL through Value.NativeQuery with parameters; logic inside the statement | covered | SS 3 | none (needs a real database) | P002 (warn) |
| Query folding | A DirectQuery native query is a plain SELECT: no CTE, no stored procedure | covered | SS 3 | - | M701 (fail) |
| Query folding | Incremental refresh and native queries do not mix well | covered | SS 26 (third bullet) | EX Sales.tmdl (refresh policy) | M708 (warn) |
| Query folding | The account behind a native query only reads what it needs | covered | SS 3 | - | files cannot show it |
| Query folding | Steps that cannot fold belong in the source (views, warehouse) | covered | SS 2 | - | files cannot show it |
| Referencing queries | Each referencing query runs the referenced query again | covered | SS 4 | EX expressions.tmdl (Sales Source) | P003 (warn) |
| Referencing queries | Table.Buffer in the shared query does not prevent this | covered | SS 4 | - | P003 (warn) fires with or without Table.Buffer |
| Referencing queries | When the source is overloaded, move the shared query to a dataflow | covered | SS 4 | - | files cannot show it (source load) |
| Background refresh | Background preview download for files with many queries; refresh previews by hand | covered | SS 11 (a Desktop option of the current file; the page reads two ways) | - | no check: files cannot show it |
| Dataflows | Dataflow Gen1 is legacy; use Dataflow Gen2 | outside this template | NF (Dataflow Gen1: do not suggest); SS 4 | - | files cannot show it |
| Dataflows | Share one set of transformations through a dataflow | outside this template | SS 4 (dataflows are built in the service) | - | files cannot show it |
| Star schema | Big volumes or slowly changing dimensions: build a warehouse first | covered | RD 8 | - | files cannot show it |
| Star schema | Split a flat extract into fact and dimension tables in Power Query | covered | RD 1 | EX Examples.SemanticModel (Sales, Store, Product) | files cannot show it (grain) |
| Star schema | A table is a fact or a dimension, never both | covered | RD 1 | EX Examples.SemanticModel | files cannot show it; M412 (warn) catches one form |
| Star schema | One grain per fact table | covered | RD 1 | EX Sales Target.tmdl (own table for targets) | files cannot show it |
| Star schema | Explicit measures, also for simple sums (Excel needs them) | covered | MS 9 | EX _Measures.tmdl | M107 (fail), M103 (warn) |
| Star schema | A column that must never be summed is hidden; measures do the allowed sums | covered | MS 7, 9 | EX Sales.tmdl | M103 (warn), M107 (fail) |
| Star schema | Surrogate key when a dimension has no unique column | covered | RD 9 | EX Date.tmdl, Store.tmdl (whole-number keys) | files cannot show it (uniqueness); M110 (warn) on key types |
| Star schema | Fold a snowflake into one dimension table | covered | RD 3 | EX Product.tmdl (flattened, with hierarchy) | M412 (warn) |
| Star schema | Type 2 slowly changing dimensions come from the source; label the version | covered | RD 8 | - | files cannot show it |
| Star schema | Role-playing dimensions: inactive relationships or one copy per role | covered | RD 7 | EX relationships.tmdl (ship date), measure Total Sales by Ship Date | U006 (note), M410 (warn) |
| Star schema | Role copies get role column names and a description of what they filter | covered | RD 7 (second bullet) | - | files cannot show it; D001 (fail) for the description |
| Star schema | Junk dimension: many small flags merged into one table with a key | covered | RD 1 (junk dimension) | - | files cannot show it |
| Star schema | Degenerate dimension (order number) stays on the fact table | covered | RD 1 (degenerate dimension) | - | files cannot show it |
| Star schema | Factless (bridging) table for many-to-many between dimensions | covered | RD 19 | relationship kinds shipped (EX relationships.tmdl); no bridge table | M406 (warn) |
| Data reduction | Load only columns that reports or the model need | covered | SS 13 | - | M201 (note) for hidden ones; files cannot show it for visible ones (other reports may use them) |
| Data reduction | Load only rows reports need: limit history, or one model per entity | covered | SS 14 | EX expressions.tmdl (Store Region parameter) | files cannot show it |
| Data reduction | Load facts at a higher grain where detail is not needed | covered | SS 15 | - | files cannot show it |
| Data reduction | Numbers instead of coded text; such columns do not summarise | covered | SS 16 | - | M107 (fail); files cannot show it for the text |
| Data reduction | Power Query columns before DAX calculated columns | covered | SS 17; MS 8 | EX Sales.tmdl (Order Size with its reason) | M105 (fail), M106 (warn) |
| Data reduction | Queries that only feed other queries are not loaded | covered | SS 12 | EX expressions.tmdl (Sales Source) | P007 (warn) |
| Data reduction | Turn Auto date/time off | covered | RD 29 | - | M401 (warn) |
| Data reduction | Very large facts in DirectQuery, with imported summaries | covered | SS 21, 22, 25 | EX storage/DirectQuery (Sales Aggregate) | U004 (note); files cannot show it (size) |
| Date tables | A date table: unique days, no blanks, no gaps, whole years | covered | RD 31 | EX Date.tmdl (shape; sample rows) | files cannot show it (data) |
| Date tables | Mark it as a date table for classic time intelligence | covered | RD 30 | EX Date.tmdl | M402 (fail), M403, M404 (warn) |
| Date tables | One date table design for the whole organisation (template or dataflow) | outside this template | a Desktop template or a dataflow lives outside a project; RD 32 starts from the source's table | - | files cannot show it |
| Date tables | Auto date/time only for simple or ad hoc models | covered | RD 29 | - | M401 (warn) |
| Date tables | Use the source's date dimension; for DirectQuery add one to the source | covered | RD 32 | - | files cannot show it |
| Date tables | CALENDAR or CALENDARAUTO can build the table in DAX | covered | RD 32 | EX Date.tmdl (Power Query form) | files cannot show it (a choice, not a breach); M105 (fail) asks the reason line |
| Date tables | A cloned date table copies columns only: set formats, descriptions, hierarchies again | covered | RD 7 (second bullet) | - | M112 (warn), D001 (fail), M404 (warn) on the copy |
| Auto date/time | Know its limits (one table per column, calendar years only, bigger model) | covered | RD 29 | - | M401 (warn) |
| Auto date/time | Months or quarters of an auto hierarchy without the year add up across years | covered | RD 29 (the standard keeps it off; fix visuals that used it) | - | M401 (warn) on the cause; no check of the visual itself |
| Auto date/time | Keep the option on only for simple needs | covered | RD 29 | - | M401 (warn) |
| Auto date/time | Turn the global Desktop option off for new files | outside this template | a global Desktop option; RD 29 and SM name the current-file option | - | files cannot show it |
| One-to-one | A part split off a fact table may relate one-to-one when rows match | covered | RD 22; NF (Relationships) | EX relationships.tmdl (Store Detail to Store) | M409 (warn); exception in section 9 of the brief |
| One-to-one | Avoid one-to-one when one thing's columns are spread over two tables | covered | RD 22 | EX relationships.tmdl | M409 (warn) |
| One-to-one | Merge the two queries, then use display folders and hierarchies | covered | RD 22 | EX Store.tmdl (column folders) | M409 (warn) |
| One-to-one | Rows on both sides must match, or blanks appear | covered | RD 22 | - | files cannot show it |
| One-to-one | Across source groups the relationship is limited and drops rows | covered | SS 23 (second bullet) | - | M409 (warn) on every one-to-one; files cannot show it (matching) |
| One-to-one | Two facts related one-to-one is unusual | covered | RD 2, 22 | - | M409 (warn) |
| Many-to-many | Two dimensions: a bridge table and two one-to-many relationships | covered | RD 19 | relationship kinds shipped; no bridge table | M406 (warn) |
| Many-to-many | In that design one relationship filters both ways, or totals are wrong | covered | RD 18 (bridge exception) | - | files cannot show it for certain (which table is a bridge is a design fact); M405 (warn) |
| Many-to-many | Turn Is Nullable off on keys that must never be blank | covered | RD 9 | EX Store[Store Key] (isNullable: false) | M416 (note) |
| Many-to-many | Hide the bridge table | covered | MS 7; RD 19 | - | files cannot show it for certain (which table is a bridge) |
| Many-to-many | Hide ID columns; if one stays visible, keep the one side and hide the many side | covered | MS 7; RD (Where sources disagree) | EX Sales.tmdl | M102 (warn) |
| Many-to-many | Explain results that do not add up (text box or description) | covered | DE (caveats); TH (item 37 row); header-icon tooltips not adopted (owner's rule, H001) | EX Elements_Text_PageTitle (text box) | files cannot show it |
| Many-to-many | Never relate two dimensions many-to-many directly | covered | RD 19 | - | M406 (warn) |
| Many-to-many | Never relate two facts many-to-many directly | covered | RD 2 | - | M406 (warn) |
| Many-to-many | A fact at a higher date grain stores the first date and relates one-to-many | covered | RD 19 | - | files cannot show it |
| Many-to-many | A fact at a higher non-date grain: many-to-many, one direction | covered | RD 19, 20 | EX relationships.tmdl (Sales Target to Product) | M406, M407 (warn) |
| Many-to-many | Measures over a higher-grain fact return blank below its grain (ISFILTERED); its number columns hidden | covered | RD 19 (higher grain); MS 7 | RD 19 shows a guard over Sales Target (not shipped) | M103 (warn), M107 (fail) for the columns; the guard: files cannot show it (the grain) |
| Active vs inactive | Prefer active relationships; one copy per role when visuals filter by several roles | covered | RD 7 | EX relationships.tmdl | U006 (note) |
| Active vs inactive | Refactor: remove inactive ones, copy the table per role, rename, describe | covered | RD 7 | - | U006 (note); D001 (fail) |
| Active vs inactive | Inactive relationships are fine when measures turn them on | covered | RD 7, 23 | EX Total Sales by Ship Date | M410 (warn) |
| Active vs inactive | A blank item can appear when the many side has unmatched keys | covered | RD 17 | - | files cannot show it |
| Active vs inactive | RLS never travels over an inactive relationship | covered | RD 24; SS 33 | - | M414 (warn), M415 (fail) |
| Both directions | Keep both-direction relationships to a minimum | covered | RD 18 | EX relationships.tmdl (Sales to Product) | M405, M408 (warn) |
| Both directions | One-to-one is always both ways; a bridge needs one both-direction relationship | covered | RD 18, 22 | - | M405, M409 (warn) |
| Both directions | A slicer that lists only items with data: a measure filter on the slicer | covered | RD 18; NF (Slicer row) | visual filters shipped (EX Charts_Bars visuals) | M405 (warn) on the both-direction alternative |
| Both directions | Ask whether a slicer list that changes with data helps readers at all | covered | RD 18 | - | files cannot show it |
| Both directions | Use CROSSFILTER inside one measure instead of a both-direction relationship | covered | RD 18 | - | M405 (warn) |
| Troubleshooting | When a visual is wrong: data loaded, relationship, cardinality, active, direction, columns | covered | RD 10-23 (one rule per point); LK (when stuck) | EX relationships.tmdl | M901 (fail), M405, M409, M410 (warn); files cannot show it for data |
| Troubleshooting | Related columns have the same data type | covered | RD 27; MS 10 | - | M109 (fail), M110 (warn) |
| Troubleshooting | Symptoms: unmatched keys, Assume Referential Integrity, 'apply security filter in both directions' | covered | unmatched keys RD 17; Assume Referential Integrity SS 24; the security-filter setting SS 37 | - | M609 (warn), U008 (note); files cannot show unmatched keys |
| DirectQuery | Work with the source's database people; tuning belongs there | covered | SS 24 | - | files cannot show it |
| DirectQuery | Source side: referential integrity, unknown row, indexes, materialised columns | covered | SS 24 | - | files cannot show it |
| DirectQuery | One query maps to one table or view: no transformation steps | covered | SS 24 | EX storage/DirectQuery Sales.tmdl | M702 (warn) |
| DirectQuery | No calculated columns or type changes on DirectQuery tables | covered | SS 23, 24 | - | M705 (fail), M704, M702 (warn) |
| DirectQuery | No relative-date filter in Power Query; offset columns in the date table | covered | SS 24 | - | M703 (warn) |
| DirectQuery | Start with simple measures; add complex CALCULATE logic while testing speed | covered | SS 24 | - | files cannot show it |
| DirectQuery | No relationship on a concatenated calculated column; COMBINEVALUES if needed | covered | SS 23 | - | M704 (warn) |
| DirectQuery | No relationships on GUID columns | covered | SS 24 | - | files cannot show it (no GUID type in the files) |
| DirectQuery | Hide the one-side key; the many-side key may stay visible | covered | SS and RD (Where sources disagree): M102 stays; exception in the brief | - | M102 (warn) |
| DirectQuery | Assume Referential Integrity on DirectQuery relationships | covered | SS 24 (set in Desktop; TMDL spelling not confirmed) | - | U008 (note) |
| DirectQuery | No both-direction relationship except on a bridge | covered | RD 18 | - | M405 (warn) |
| DirectQuery | Maximum connections per data source | outside this template | a Desktop setting, not in the project files | - | files cannot show it |
| DirectQuery | Query reduction options on from the start | covered | SS 24; RS 54; VF 10 | EX Slicers_More_Button_ApplyAll, Slicers_More_Button_ClearAll | U104 (note) |
| DirectQuery | Add filters before fields when building a visual (1 million row limit) | outside this template | a habit when building in Desktop; files are written whole | - | files cannot show it |
| DirectQuery | Few visuals per page; one card visual instead of many cards | covered | RS 63; NF (Card rows) | EX Cards_KPIs_Card_SalesFigures (one card, several values) | V006 (fail), V007 (warn) |
| DirectQuery | Switch off interactions nobody needs | covered | RS 53 | EX Charts_Bars page.json (NoFilter) | files cannot show it (which ones are needed) |
| DirectQuery | Measure filters, Top N filters and medians cost extra queries | covered | SS 24 | EX Filters_Kinds (a Top N filter) | U106 (note); medians: no check |
| DirectQuery | Multi-select slicers: Apply buttons | covered | RS 54; SS 24; VF 10 | EX Slicers_More_Button_ApplyAll | U104 (note) |
| DirectQuery | Turn off totals and subtotals nobody needs | covered | SS 24; VF 15 | EX Tables_Features_Table_TotalsOffWidths | No check: SS 24 says Microsoft Learn does not document the file property (VF 15 takes it from Microsoft's visual catalogue) |
| DirectQuery | Consider a composite model with Dual tables and aggregations | covered | SS 22-25 | EX storage/DirectQuery | M706 (warn), U004 (note) |
| DirectQuery | Tell authors and readers how DirectQuery behaves | covered | SR step 6 (Info page, item 75) | - | files cannot show it |
| Composite | Prefer Import; composite only when needed | covered | SS 22, 23 | - | files cannot show it (the reason lives in the brief) |
| Composite | To add data to an existing model, add it at the source | covered | SS 23 (first line) | - | files cannot show it |
| Composite | Mode per table: DirectQuery facts, Dual dimensions, Import for the rest, hybrid | covered | SS 22, 26 | EX storage/DirectQuery (Dual Date, Store) | M706 (warn) |
| Composite | Keep Dual and hybrid caches refreshed | outside this template | refresh schedules live in the service | - | files cannot show it |
| Composite | Matching values across source groups (limited relationships drop rows) | covered | SS 23 | - | files cannot show it |
| Composite | Aggregation tables: ten times fewer rows; none on a hybrid table | covered | SS 25 | EX Sales Aggregate.tmdl | U004 (note); files cannot show it (row counts) |
| Composite | Relationship columns across source groups: under 50,000 distinct values | covered | SS 23 | - | files cannot show it |
| Composite | Desktop does not fully validate relationships across source groups | covered | SS 23 (models on a published model) | - | files cannot show it (SS 23: none of these points a file here can show) |
| Composite | Test CALCULATE over a measure from a remote model | covered | SS 23 | none: not built (MF 8: no file form for the remote model) | files cannot show it |
| Composite | Calculated columns on DirectQuery tables: same-row logic only | covered | SS 23 | - | M705 (fail) |
| Composite | Calculated objects cannot rely on a chained (remote) model | covered | SS 23 | none: not built (MF 8) | files cannot show it (no file form for the remote model) |
| Composite | Test every calculation after adding calculated columns to a composite model | covered | SS 23 | - | files cannot show it |
| Composite | Calculation groups in a remote model can surprise | covered | SS 23 | - | files cannot show it |
| Composite | Star schema; dimensions in the same source group as their facts | covered | SS 23; RD A | EX storage/DirectQuery | M706 (warn) |
| Composite | RLS in composite models: per source group; not on a remote table | covered | SS 23 (roles per source group; remote roles not copied); SS 25 (aggregations) | none: not built (MF 8) | files cannot show it (no file form for remote tables) |
| Composite | Visuals from one source group; sync slicers instead of a cross-group relationship | covered | RS 30 (composite models); NF (Sync slicers row) | EX RegionSync slicers | No check: the report files do not mark which source group a field comes from |
| Composite | Do not rename models or workspaces a composite model reads | outside this template | a rename in the service; MS (Existing models) warns about other reports | - | files cannot show it |
| Composite | Keep the one trusted enterprise model free of composite parts | covered | SS 23 | - | files cannot show it |
| Composite | Check lineage before publishing composite changes | outside this template | lineage view lives in the service | - | files cannot show it |
| RLS | RLS filters rows; it cannot hide tables or columns | covered | SS 28, 35 | EX roles (Northport Stores, No Product Cost) | files cannot show it (a statement of fact) |
| RLS | Roles add up; prefer one role per kind of reader | covered | SS 36 | - | files cannot show it (members are in the service) |
| RLS | Rules on dimensions, carried by active relationships; no LOOKUPVALUE | covered | SS 29, 30, 33 | EX roles | M602, M601 (warn), M414 (warn), M415 (fail) |
| RLS | RLS on DirectQuery tables: tune the source | covered | SS 24 | - | files cannot show it |
| RLS | Measure RLS cost with Performance Analyzer and View as | outside this template | Desktop tools; SS 34 | - | files cannot show it |
| RLS | Map security groups, not single people | outside this template | SS 34 (members are assigned in the service) | - | files cannot show it |
| RLS | Test each role; unexpected values return no rows | covered | SS 31, 34, 36 | EX Own Store.tmdl | M605 (warn) |
| RLS | Share-of-all figures from a summary table RLS does not filter; totals must not leak | covered | SS 38 | - | files cannot show it (what a total gives away) |
| RLS | A few static rules: separate models per audience may be better | covered | SS 14 (filter by entity) | - | files cannot show it |
| RLS | Troubleshooting: directions, 'apply security filter in both directions', several roles, aggregations | covered | SS 37 (the security-filter setting); SS 36 (roles add up, aggregations) | - | M609 (warn) |
| RLS | A test measure that shows the signed-in user | covered | SS 34 (a temporary measure, removed before publishing) | - | files cannot show it |
| RLS | Readers get Read on the model, not workspace roles | outside this template | SS 34, 36 (workspace access lives in the service) | - | files cannot show it |
| Power Platform | Pick Import, Synapse Link or DirectQuery for Dataverse on purpose | covered | SS 22; SS 6 | - | files cannot show it |
| Power Platform | One model per subject, not one model for everything | covered | RD 1 (one model per subject) | - | files cannot show it |
| Power Platform | Star schema, not Dataverse's own table layout | covered | RD 1 | - | files cannot show it |
| Power Platform | Aim for query folding | covered | SS 2 | - | files cannot show it |
| Power Platform | Pick columns early; fetching all can run past ten minutes and fail | covered | SS 6 | - | P004 (warn) |
| Power Platform | Dataverse native queries with EnableFolding=true | covered | SS 6 | - | P004 (warn) |
| Power Platform | CreateNavigationProperties=false unless relationship columns are expanded | covered | SS 6 | - | P004 (warn) |
| Power Platform | Blank choice labels: publish customisations in Dataverse | out of scope | another system (Dataverse) | - | - |
| Power Platform | Synapse Link: friendly views, snapshot tables | out of scope | another system (Synapse) | - | - |
| Power Platform | DirectQuery to Dataverse: Dual dimensions, single sign-on, CURRENT_USER views, extra Import models | covered | SS 6 | - | M706 (warn) for Dual; the rest: files cannot show it (set in the service or decided with the developer) |
| DAX error functions | Avoid IFERROR and ISERROR | covered | DS 1 | - | M501 (warn) |
| DAX error functions | Clean bad values upstream and set types in Power Query | covered | DS 1; SS 9 | - | files cannot show it |
| DAX error functions | Is Nullable off where a blank must fail the refresh | covered | RD 9 | EX Store[Store Key] (isNullable: false) | M416 (note) |
| DAX error functions | Test the cause with IF rather than catch an error | covered | DS 1 | - | M501 (warn) |
| DAX error functions | Use functions that tolerate errors, such as DIVIDE | covered | DS 2 | EX Average Line Amount | M502 (fail) |
| DAX blanks | Return blank, not zero, when there is nothing to show | covered | DS 7 | EX _Measures.tmdl | M506 (warn) |
| DAX blanks | Use 'Show items with no data' when every group must show | covered | DS 7; NF (Show items with no data) | - | files cannot show it (a visual setting the developer turns on) |
| DAX FILTER | Filter a column (with KEEPFILTERS), not FILTER over a whole table | covered | DS 6 | - | M505 (warn) |
| DAX FILTER | FILTER only for measure tests or complex logic, over VALUES of a column | covered | DS 6 (third bullet) | - | M505 (warn) |
| DAX references | Columns always with their table | covered | DS 10; MS 5 | EX _Measures.tmdl | M010 (warn) |
| DAX references | Measures never with their table | covered | DS 10 | EX _Measures.tmdl | M010 (warn) |
| DAX references | A column never shares a name with a measure or hierarchy of its table | covered | MS 3; RD 38 | - | M006 (fail), M119 (warn) |
| DAX DIVIDE | DIVIDE when the divisor can be zero or blank | covered | DS 2 | EX Average Line Amount | M502 (fail) |
| DAX DIVIDE | The / operator when the divisor is a fixed number | covered | DS 2 (second bullet) | - | M518 (warn) |
| DAX DIVIDE | Usually leave out DIVIDE's third argument | covered | DS 2, 7 | - | M506 (warn) for a zero; other values unchecked |
| DAX COUNTROWS | COUNTROWS of a table, not COUNT of a column, to count rows | covered | DS 3 | EX # Order Lines | M503 (warn) |
| DAX SELECTEDVALUE | SELECTEDVALUE instead of IF, HASONEVALUE and VALUES | covered | DS 4 | - | M504 (warn) |
| DAX SELECTEDVALUE | Never compare VALUES of a column with one value | covered | DS 5 | - | M517 (warn) |
| DAX variables | Store a repeated expression in a variable | covered | DS 8 | EX Total Sales vs PY (%) | M507 (warn) |
| DAX variables | Name variables so the RETURN line reads well | covered | DS 31 | EX Total Sales vs PY (%) | files cannot show it (judgement) |
| DAX variables | Debug by returning a variable for a moment | covered | DS 16 (testing aids are removed before publishing) | - | files cannot show it |
| DAX variables | A variable instead of EARLIER or EARLIEST | covered | DS 9 | - | M514 (warn) |
| DAX ORDERBY | ORDERBY, PARTITIONBY and MATCHBY work only inside window functions | covered | DS 11 | - | M909 (warn) on unknown functions; files cannot show it otherwise |
| DAX ORDERBY | Always write ORDERBY (and PARTITIONBY where needed) | covered | DS 11 | - | M516 (warn) |
| DAX ORDERBY | Add MATCHBY when the order columns do not identify each row | covered | DS 11 | - | files cannot show it (uniqueness is data) |
| DAX GB18030 | Unicode character behaviour set to code points where GB18030 is required | outside this template | NF (Model: Unicode character behavior); set by an XMLA command on the published model | - | files cannot show it |
| DAX UDFs | Functions need compatibility level 1702 | covered | MO A1, A7 | EX database.tmdl, functions.tmdl | M801 (fail) |
| DAX UDFs | Naming rules for functions and parameters | covered | MO A6 | EX functions.tmdl | M802 (fail; function name only), M807 (warn; SQLBI style) |
| DAX UDFs | A /// description on every function | covered | MO A7 | EX functions.tmdl | M803 (warn) |
| DAX UDFs | Type hints on parameters; reference types use expr | covered | MO A5, A7 | EX functions.tmdl (AddTax, ShareOfAll) | M804 (warn) |
| DAX UDFs | In a calculated column a function returns one scalar type | covered | MO A8 | - | files cannot show it |
| DAX UDFs | Write columns with their table inside a function | covered | MO A7; DS 39 | EX functions.tmdl | M010 (warn) reads functions |
| DAX UDFs | OLS does not reach functions: never name secured objects in a function | covered | MO A7, A8; DS 39 | - | M806 (warn) |
| DAX UDFs | No recursion, no overloading; cannot hide, fold or translate a function | covered | MO A8 | - | M805 (fail, direct calls); M005-style duplicates not checked for functions |
| Separate reports | One file only for one report by one person; otherwise split model and report | covered | NF (Live connection); RS L; SR step 3 | EX starter (byPath) | files cannot show it (who builds what) |
| Separate reports | After publishing a model, delete its test report | out of scope | a publishing step | - | - |
| Separate reports | Do not break the model's interface (renames, types, home table) | covered | CI (rename rule); MS (Existing models); TI 10 | - | B001 (fail) in this project; files cannot show it for other reports |
| Separate reports | Prefix report-level measures so model measures cannot clash | covered | RS 66 | EX reportExtensions.json (_Sales per Order Line) | V012 (warn) |
| Separate reports | Find dependent reports in lineage before a breaking change | outside this template | lineage view lives in the service; MS (Existing models) says to warn | - | files cannot show it |
| Tooltip pages | Report page tooltips for another view, more detail or help | covered | RS C; tooltips are off unless the brief lists the visual (owner's rule) | EX Tooltip_StoreSales | V002-V005 (warn), H002 (fail) |
| Tooltip pages | No slicers or buttons on a tooltip page | covered | RS 19 | EX Tooltip_StoreSales | V004 (warn) |
| Tooltip pages | Keep it small, near 320 x 240 | covered | RS 18 | EX Tooltip_StoreSales | V003 (warn) |
| Tooltip pages | Design at Actual Size | outside this template | a Desktop view setting | - | files cannot show it |
| Tooltip pages | Use the report's theme | covered | TH | - | T001 (fail) |
| Tooltip pages | Remove design-time filter values before publishing | covered | RS C (last bullet) | - | V013 (warn) |
| Tooltip pages | Hide tooltip pages | covered | RS 18 | EX Tooltip_StoreSales | V002 (warn) |
| Drillthrough | Plan the path: page, data point, drillthrough, analysis, back | covered | RS D | EX Drillthrough_Store | files cannot show it |
| Drillthrough | Use the report's theme | covered | TH | - | T001 (fail) |
| Drillthrough | Remove design-time drillthrough values before publishing | covered | RS 29 | - | V013 (warn) |
| Drillthrough | No visuals that show blanks or errors under the drillthrough filter | covered | RS D (Only Desktop shows) | - | files cannot show it |
| Drillthrough | Hide drillthrough pages; a visible one gets a reset button | covered | RS 29 | EX Drillthrough_Store (hidden) | V014 (warn) |
| Drillthrough | Keep the back button | covered | RS 23 | EX Drillthrough_Store_Button_Back | V001 (fail) |
| Drillthrough | Tell readers how to drill through (text box) | covered | RS 28; header-icon text not adopted (owner's rule) | EX Elements_Text_PageTitle (text box) | files cannot show it |
| Locale values | Add a culture file for every culture name readers use; table and column names need an exact match | covered | ML 1 | EX cultures/nl-NL.tmdl | files cannot show it (the list of cultures is the brief's) |
| Locale values | Dates and numbers follow the reader through format strings such as Short Date | covered | ML 2 | - | No check: no Microsoft Learn page shows that Desktop writes the named formats this way in TMDL |
| Locale values | Use translations for the default language sparingly | covered | ML 3 | - | files cannot show it (Microsoft leaves how much to the author) |
| Locale values | USERCULTURE gives the reader's culture in measures, not in imported calculated columns or tables | covered | ML 4 | EX Sales by Store Label | M524 (warn) |
| Locale values | Label measures live in the model: USERCULTURE can be wrong in report-level measures | covered | ML 5 | EX Sales by Store Label | V019 (warn) |
| Locale values | FORMAT takes a culture name; for numbers prefer a format string | covered | ML 6 | EX Total Sales After Discount (dynamic format string) | U005 (note) |
| Localize reports | Plan a report for translation from the start | covered | ML 7 | - | files cannot show it |
| Localize reports | Leave room for longer text, and test each language in the service | covered | ML 11, 12 | - | files cannot show it (a file does not show the rendered width) |
| Localized Labels table | Text stored in the report layout is never translated: no typed text in text boxes, visual titles or page tabs | covered | ML 8 | EX Sales by Store Label | V020 (warn); typed text in shapes and buttons is not counted (stored form not confirmed) |
| Localized Labels table | Visual titles generated from field names or taken from a label measure; page titles from a label measure | covered | ML 9, 10 | EX Charts_Features_ClusteredBar_DynamicSubtitle (subtitle from a measure) | A003 (warn), V018 (note) |
| Localized Labels table | Label measures: SWITCH over USERCULTURE with the default language last; a culture file for each culture named | covered | ML 14-16 | EX Sales by Store Label | M525 (warn) |
| Language page navigation | Hide every page but one, so no page tab shows | covered | ML 18 | - | V021 (warn) |
| Language page navigation | Navigate with bookmark buttons whose text comes from label measures | covered | ML 19, 20 | EX Bookmarks_Button_ShowChart (bookmark buttons, without label text) | No check: the button text rule is covered by ML 8 |
| Data translation | Translate data only when readers of several languages see the same data; weigh values, length and upkeep | covered | ML 21 | - | files cannot show it |
| Data translation schema | One source column per language for each translated field | covered | ML 22 | - | files cannot show it |
| Data translation field parameters | A field parameter over the language columns, with translated labels and a language value per row | covered | ML 23 | EX Sales Breakdown (field parameter over columns) | No check: the files do not show for certain that a value is a language; M822 (warn) on a visible language column |
| Languages table | A languages table related one-to-one to each translation parameter; one single-select filter on all pages | covered | ML 24 | - | No check: the files do not show for certain which column is the language column |
| Synchronize field parameters | Every translated field related to the same languages table, so one filter keeps them in step | covered | ML 25 | - | files cannot show it (see the row above) |
| Translated calendar table | Month and weekday name tables per language from Power Query, sorted and related to the date table | covered | ML 26 | EX Date.tmdl (Month Name by Month Number) | M113 (warn) for month names; weekday names unchecked |
| Load in reader's language | One bookmark per language filters the languages table; the address names it after the language parameter | covered | ML 27 | - | No check: how the bookmark options map to the file properties is not confirmed |
| Monitor performance | Monitor slow refresh, queries and visuals | outside this template | CR (item 68: evidence people give) | - | files cannot show it |
| Monitor performance | Query Diagnostics for Power Query | outside this template | NF (Outside the project files) | - | files cannot show it |
| Monitor performance | Performance Analyzer per visual | outside this template | NF (Outside the project files); RS K | - | files cannot show it |
| Monitor performance | SQL Server Profiler on Desktop's local port | outside this template | a tool outside the files | - | files cannot show it |
| Monitor performance | Only supported model changes through the diagnostics port | outside this template | CI: never change a model through a tool or server | - | files cannot show it |
| Monitor performance | Capacity Metrics app | outside this template | a service app | - | files cannot show it |
| Troubleshoot performance | Follow the flowchart: capacity, time, region, device, then report and model | outside this template | service and Desktop tools; CR (item 68) | - | files cannot show it |

## B. Microsoft Learn: DAX best practices

The 11 pages of the DAX reference section "Best practices" (from https://learn.microsoft.com/en-us/dax/toc.json; the section has no index page). Their practices are rows in A2.

| Page | Practice | Status | Guidance | Example | Check |
| --- | --- | --- | --- | --- | --- |
| Appropriate use of error functions (https://learn.microsoft.com/en-us/dax/best-practices/dax-error-functions) | No IFERROR or ISERROR; clean upstream; test with IF; DIVIDE; Is Nullable off | covered | DS 1, 2; RD 9 | EX Store[Store Key] (isNullable: false) | M501 (warn), M502 (fail), M416 (note) |
| Avoid converting BLANKs to values (https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-converting-blank) | Return blank; use 'Show items with no data' when all groups must show | covered | DS 7 | EX _Measures.tmdl | M506 (warn) |
| Avoid using FILTER as a filter argument (https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-avoid-filter-as-filter-argument) | Column filters (KEEPFILTERS) in CALCULATE; FILTER only for measure tests | covered | DS 6 | - | M505 (warn) |
| Column and measure references (https://learn.microsoft.com/en-us/dax/best-practices/dax-column-measure-references) | Columns with their table, measures without; no shared names | covered | DS 10; MS 5; RD 38 | EX _Measures.tmdl | M010 (warn), M006 (fail), M119 (warn) |
| DIVIDE function vs divide operator (/) (https://learn.microsoft.com/en-us/dax/best-practices/dax-divide-function-operator) | DIVIDE for expressions; / for a fixed number; no third argument | covered | DS 2 | EX Average Line Amount | M502 (fail); M506 (warn); M518 (warn) for DIVIDE by a fixed number |
| Use COUNTROWS instead of COUNT (https://learn.microsoft.com/en-us/dax/best-practices/dax-countrows) | COUNTROWS to count rows | covered | DS 3 | EX # Order Lines | M503 (warn) |
| Use SELECTEDVALUE instead of VALUES (https://learn.microsoft.com/en-us/dax/best-practices/dax-selectedvalue) | SELECTEDVALUE; never compare VALUES with one value | covered | DS 4, 5 | - | M504, M517 (warn) |
| Use variables to improve your DAX formulas (https://learn.microsoft.com/en-us/dax/best-practices/dax-variables) | Variables for repeats, readability, debugging; not EARLIER | covered | DS 8, 9, 31 | EX Total Sales vs PY (%) | M507, M514 (warn) |
| Understanding ORDERBY, PARTITIONBY, and MATCHBY functions (https://learn.microsoft.com/en-us/dax/best-practices/dax-understand-orderby) | Explicit ORDERBY and PARTITIONBY; MATCHBY when rows are not unique | covered | DS 11 | - | M516 (warn); MATCHBY: files cannot show it |
| Configure Chinese coded character set (GB18030-2022) support (https://learn.microsoft.com/en-us/dax/best-practices/dax-unicode-character-behavior) | Code-point text behaviour where the standard is required | outside this template | NF (Model) | - | files cannot show it (set by XMLA on the published model) |
| Use DAX user-defined functions (https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions) | Level 1702, naming, descriptions, types, no recursion; qualify columns; OLS limits | covered | MO A; DS 39 | EX functions.tmdl | M801-M807; M010 (warn) reads functions |

## C. Microsoft's best practice rules

All 71 rules of BPARules.json in microsoft/Analysis-Services (folder BestPracticeRules), in file order. Each rule's expression was read. Rules that need data the files do not hold (row counts, cardinality and integrity annotations) say so.

| Rule | Category | Status | Guidance | Check |
| --- | --- | --- | --- | --- |
| Do not use floating point data types | Performance | covered | MS 10; SS 16 | M108 (warn) |
| Set IsAvailableInMdx to false on non-attribute columns | Performance | covered | MS 16 | M301 (note, when the brief turns it on) |
| Avoid bi-directional relationships against high-cardinality columns | Performance | covered | SS 20 (no both-direction relationship on such columns); RD 18 | files cannot show it (needs a cardinality annotation); M405 (warn) on every both-direction relationship |
| Reduce usage of long-length columns with high cardinality | Performance | covered | SS 20 | files cannot show it (needs row-length data) |
| Split date and time | Performance | covered | MS 11; RD 33; SS 18 | M111 (warn): the files hold no data, so it reads the format instead |
| Large tables should be partitioned | Performance | covered | MS 14; SS 21 | files cannot show it (row counts); judged in the review |
| Reduce usage of calculated columns that use the RELATED function | Performance | covered | MS 8 | M106 (warn) |
| Consider a star-schema instead of a snowflake architecture | Performance | covered | RD 3 | M412 (warn) |
| Model should have a date table | Performance | covered | RD 30 | M403 (warn) when date columns exist, M402 (fail) with time intelligence: narrower than the rule, which fires on any model |
| Date/calendar tables should be marked as a date table | Performance | covered | RD 30 | M404 (warn) |
| Remove auto-date table | Performance | covered | RD 29 | M401 (warn) |
| Avoid excessive bi-directional or many-to-many relationships | Performance | covered | RD 21 | M408 (warn), same 30% line |
| Limit row level security (RLS) logic | Performance | covered | SS 30 | M601 (warn); also LOOKUPVALUE |
| Consider using aggregations if using Direct Query in Power BI | Performance | covered | SS 25 | U004 (note) |
| Minimize Power Query transformations | Performance | covered | SS 5 | P006 (warn) at three of the listed functions, not one |
| Avoid using many-to-many relationships on tables used for dynamic row level security | Performance | covered | SS 32 | M604 (warn) |
| Unpivot pivoted (month) data | Performance | covered | RD 6 | M417 (warn) |
| Many-to-many relationships should be single-direction | Performance | covered | RD 20 | M407 (warn) |
| Reduce usage of calculated tables | Performance | covered | MS 8; SS 17 | M105 (fail): every calculated table needs its reason line, instead of a count |
| Remove redundant columns in related tables | Performance | covered | RD 5 | M115 (warn) |
| Measures using time intelligence and model is using Direct Query | Performance | covered | DS 17; SS 24 | M513 (warn) |
| Reduce number of calculated columns | Performance | covered | MS 8 | M106 (warn), same limit of five |
| Check if bi-directional and many-to-many relationships are valid | Performance | covered | RD 18, 19 | M405, M406 (warn) |
| Check if dynamic row level security (RLS) is necessary | Performance | covered | SS 28; item 41 (review user-based roles) | files cannot show it (whether a user-based rule is needed); M603 (warn) on USERNAME |
| Column references should be fully qualified | DAX Expressions | covered | DS 10 | M010 (warn) in measures, calculated columns, calculation items, role filters and functions; KPIs are not read |
| Measure references should be unqualified | DAX Expressions | covered | DS 10 | M010 (warn) |
| No two measures should have the same definition | DAX Expressions | covered | DS 12 | M508 (warn) |
| Use the TREATAS function instead of INTERSECT for virtual relationships | DAX Expressions | covered | DS 14 | M510 (warn) |
| Use the DIVIDE function for division | DAX Expressions | covered | DS 2 | M502 (fail); a fixed number after / passes |
| Avoid using the IFERROR function | DAX Expressions | covered | DS 1 | M501 (warn); also ISERROR |
| Measures should not be direct references of other measures | DAX Expressions | covered | DS 13 | M509 (warn) |
| Filter column values with proper syntax | DAX Expressions | covered | DS 6 | M505 (warn) |
| Filter measure values by columns, not tables | DAX Expressions | covered | DS 6 (third bullet) | M505 (warn): any FILTER over a whole table, whatever the test |
| Inactive relationships that are never activated | DAX Expressions | covered | RD 23 | M410 (warn) |
| Avoid using '1-(x/y)' syntax | DAX Expressions | covered | DS 15 | M511 (warn); the / form gives M502 |
| The EVALUATEANDLOG function should not be used in production models | DAX Expressions | covered | DS 16 | M512 (warn) |
| Data columns must have a source column | Error Prevention | covered | RD 13 | M904 (fail) |
| Expression-reliant objects must have an expression | Error Prevention | covered | RD 14 | M905 (fail) |
| Avoid structured data sources with provider partitions | Error Prevention | covered | SS 39 | M833 (fail) |
| Avoid the USERELATIONSHIP function and RLS against the same table | Error Prevention | covered | RD 25 | M415 (fail) |
| Relationship columns should be of the same data type | Error Prevention | covered | RD 27; MS 10 | M109 (fail) |
| Avoid invalid characters in names | Error Prevention | covered | RD 15 | M906 (fail) |
| Avoid invalid characters in descriptions | Error Prevention | covered | RD 15 | M906 (fail) reads descriptions too |
| Set IsAvailableInMdx to true on necessary columns | Error Prevention | covered | RD 16 | M907 (fail) |
| Remove unnecessary columns | Maintenance | covered | MS 15; SS 13 | M201 (note) |
| Remove unnecessary measures | Maintenance | covered | MS 15 | M201 (note) |
| Fix referential integrity violations | Maintenance | covered | RD 17 (fix unmatched keys at the source); RD 9 (item 14) | files cannot show it (needs an integrity annotation) |
| Remove data sources not referenced by any partitions | Maintenance | covered | SS 39 | M832 (warn) |
| Remove roles with no members | Maintenance | outside this template | SS 34; MO E (members are assigned in the Power BI service) | files cannot show it |
| Ensure tables have relationships | Maintenance | covered | RD 4 | M411 (warn); measure tables, calculation groups and parameter tables left out |
| Visible objects with no description | Maintenance | covered | DE; TI 1 | D001 (fail) |
| Perspectives with no objects | Maintenance | covered | MO D (Perspectives) | M831 (warn) |
| Calculation groups with no calculation items | Maintenance | covered | MO B5 | M811 (warn) |
| Partition name should match table name for single partition tables | Naming Conventions | covered | RD 39 | M117 (warn) |
| Object names must not contain special characters | Naming Conventions | covered | RD 15 | M906 (fail) |
| Trim object names | Naming Conventions | covered | MS 3; RD 42 | M007 (fail) for measures, M118 (warn) for visible tables, columns, hierarchies; other object kinds unchecked |
| Format flag columns as Yes/No value strings | Formatting | covered | RD 37 | M116 (warn) |
| Objects should not start or end with a space | Formatting | covered | MS 3; RD 42 | M007 (fail), M118 (warn) |
| Provide format string for "Date" columns | Formatting | not adopted | not adopted in its fixed form: checklist items 71 and 72 leave the format to the organisation; MS 12 asks for a format | M112 (warn): a format exists |
| Provide format string for "Month" columns | Formatting | not adopted | not adopted in its fixed form: checklist items 71 and 72 leave the format to the organisation; MS 12 | M112 (warn): a format exists |
| Provide format string for measures | Formatting | covered | MS 4 | M009 (fail) |
| Do not summarize numeric columns | Formatting | covered | MS 9 | M107 (fail) |
| Percentages should be formatted with thousands separators and 1 decimal | Formatting | not adopted | not adopted in its fixed form: checklist items 71 and 72 leave the format to the organisation; MS 4 | M009 (fail): a format exists |
| Whole numbers should be formatted with thousands separators and no decimals | Formatting | not adopted | not adopted in its fixed form: checklist items 71 and 72 leave the format to the organisation; MS 4 | M009 (fail): a format exists |
| Relationship columns should be of integer data type | Formatting | covered | RD 27; MS 10 | M110 (warn) |
| Add data category for columns | Formatting | covered | RD 36 | M114 (warn) |
| Hide foreign keys | Formatting | covered | MS 7; RD 28 | M102 (warn) |
| Mark primary keys | Formatting | covered | RD 26 | M413 (warn) |
| Hide fact table columns | Formatting | covered | MS 7 | M103 (warn) |
| First letter of objects must be capitalized | Formatting | covered | RD 42; MS 3 | M118 (warn); M008 (warn) for measure Title Case |
| Month (as a string) must be sorted | Formatting | covered | RD 35 | M113 (warn) |

## D. Other sources, topic by topic

No text of SQLBI or of the GPL repository is quoted; every practice is restated.

### D1. Microsoft's skills (microsoft/skills-for-fabric)

| Topic | Practice | Status | Where covered, or why not adopted |
| --- | --- | --- | --- |
| Names | Readable words with spaces; no code-style names or stray spaces | covered | MS 3; RD 41-42; M007 (fail), M118 (warn) |
| Names | No technical table prefixes (Dim, Fact, Stg) | covered | RD 42; M118 (warn) |
| Names | Facts plural, dimensions singular | covered | RD 45; files cannot show it for certain (which table is a fact) |
| Names | Main label column named after its table, or table-qualified for AI | covered | RD 45 and its disagreement note; both pass |
| Names | Spell words out; keep known acronyms; explain them | covered | MS 3 (item 7, judged in the review); brief lists own spellings |
| Names | Measure order base, period, unit; counts with # | covered | MS 3; M008 (warn). The skill's lower-case period in brackets, (ytd): not adopted (owner's suffix YTD, PY) |
| Names | No programmer-style measure names | covered | MS 3; M007 (fail) |
| Display folders | One folder layout per kind of table (Measures\Value and so on) | not adopted | the owner's rule wins: measures Subject\Type (MS 2, M003, M004), columns in four folders (MS 6, M101) |
| Descriptions | Every visible object has a description that says how to use it | covered | DE; D001 (fail); 'do not repeat the name' is guidance only |
| Modelling | Follow an existing model's patterns first | covered | MS (Existing models); SM (Existing model) |
| Modelling | Star schema by default; no snowflakes | covered | RD A; M412 (warn) |
| Modelling | Explicit measures; hide the column a measure totals; discourage implicit measures | covered | MS 7, 9; M103, M107; the model property only with calculation groups (M814) |
| Modelling | Lean model; costly high-cardinality columns | covered | SS 13, 20; files cannot show it (cardinality); M111 (warn) |
| Modelling | Every data column names its source; tables related except utility tables | covered | RD 4, 13; M904 (fail), M411 (warn) |
| Modelling | Data types: whole number keys, fixed decimal money, never double | covered | MS 10; M108, M110 (warn) |
| Modelling | Hide keys, system columns and totalled columns | covered | MS 7; M102, M103 (warn) |
| Modelling | Do not summarise IDs, years, codes | covered | MS 9; M107 (fail), stricter: every visible number |
| Modelling | isAvailableInMdx off on hidden columns with no job | covered | MS 16; M301 (note) |
| Modelling | Data categories on places | covered | RD 36; M114 (warn) |
| Modelling | Flags as Yes/No text | covered | RD 37; M116 (warn) |
| Modelling | Sort-by columns; sort columns stay available to MDX | covered | RD 12, 16, 35; M113 (warn), M903, M907 (fail) |
| Modelling | More than about 30 visible columns hints at a design problem | covered | RD 1 (wide tables); M120 (warn) |
| Modelling | Few calculated columns; none with RELATED | covered | MS 8; M105 (fail), M106 (warn) |
| Modelling | Measures spread over their own tables, not one measure table | not adopted | the owner's rule (MS 1, M001); the same skill's TMDL guide shows a _Measures table |
| Modelling | No duplicate measures; no measure that only repeats another | covered | DS 12, 13; M508, M509 (warn) |
| Modelling | Every visible measure has a format string | covered | MS 4; M009 (fail) |
| Relationships | Single direction, whole-number keys, same types, under 30% special, no unused inactive, no USERELATIONSHIP with RLS | covered | RD B; M102, M109, M110, M405, M408, M410, M415 |
| Relationships | isKey listed among things not to do | covered | RD (Where sources disagree): M413 follows the best practice rule |
| Date table | Source date table first; contiguous; marked; month names sorted; Auto date/time off | covered | RD C; M401-M404, M113; example Date.tmdl |
| Hierarchies | No single-level hierarchy; levels from one table | covered | RD 11, 40; M902 (fail); single-level not checked |
| RLS | Simple rules; no text functions; single direction on security tables | covered | SS 30; M601 (warn) |
| Calculation groups | For time variants; never empty; clear item names; item formats | covered | MO B; M811-M814; example Time Calculation.tmdl |
| Clean-up | Remove unused hidden objects, unused inactive relationships, empty perspectives | covered | MS 15; RD 23; MO D; M201 (note), M410, M831 (warn) |
| Parameters | Server and database as parameters | covered | SS 8; example expressions.tmdl |
| Pivoted data | Unpivot month columns | covered | RD 6; M417 (warn) |
| DAX | Variables for long formulas; names start with _ | covered | DS 8; M507 (warn). The _ prefix: not adopted (Microsoft Learn's page writes plain names; DS 31). |
| DAX | DIVIDE by default; / inside iterators only without zero divisors | covered | DS 2; M502 (fail); the iterator case goes in the brief |
| DAX | Column predicates or KEEPFILTERS, not FILTER over a table | covered | DS 6; M505 (warn) |
| DAX | TREATAS rather than INTERSECT | covered | DS 14; M510 (warn) |
| DAX | REMOVEFILTERS rather than ALL when only clearing filters | covered | DS 20; M519 (warn) |
| DAX | Columns with table, measures without | covered | DS 10; M010 (warn) |
| DAX | Avoid deep CALCULATE nesting | covered | DS 8; M521 (warn) |
| DAX | IFERROR acceptable as one guard | not adopted | Microsoft Learn (higher) says avoid it: DS 1, M501 |
| DAX | No EVALUATEANDLOG in production | covered | DS 16; M512 (warn) |
| DAX | No 1 - (x / y) | covered | DS 15; M511 (warn) |
| DAX | Rolling windows: the offset equals the window length; time functions need a date context | covered | DS C (rolling windows); no check |
| DAX | Function parameters typed; expr only when needed | covered | MO A5; M804 (warn) |
| DAX | Rules for saved DAX queries (DEFINE, ORDER BY) | outside this template | DAX query view lives in Desktop (NF, Outside the project files) |
| DAX performance | Tune with traces: warm-up, measured runs, no change without a yes | outside this template | tracing tools; the yes rule is in CI |
| DAX performance | Catalogue patterns Microsoft Learn also states (filters, variables, COUNTROWS, no zeros) | covered | DS A; M503, M505, M506, M507 |
| DAX performance | The other catalogue patterns (context transition in iterators, SUMMARIZE filters, Boolean multipliers, model patterns) | covered | DS 32, 35-38; no check: Microsoft's skill offers each as something to try and then measure |
| DAX performance | ALLEXCEPT only when the kept column is filtered directly | covered | DS 20; files cannot show it (depends on the query) |
| Direct Lake | Entity partitions pointing to one shared expression; no M | covered | SS 27; MF 4; example storage/DirectLake; M711 (warn) |
| Direct Lake | Shared expression with AzureStorage.DataLake; named DirectLake - Model | covered | SS 27; example DirectLake expressions.tmdl |
| Direct Lake | Columns map one-to-one; no binary columns | covered | SS 27; M904 (fail); binary not checked |
| Direct Lake | Lakehouse tuning (V-Order, row groups) | outside this template | SS 27 (outside the model) |
| TMDL | Tabs, quotes, /// descriptions, // only in expressions, no lineageTag | covered | TI; TM; D001, D003, C001 |
| TMDL | Measures before columns in a table | covered | MS C (order inside a table file); no check: Learn says the order does not change the model |
| TMDL | database declaration first; ref lines; powerBI_V3 for API import | covered | TM; F003, J checks; the API import is a publishing step (out of scope) |
| TMDL | No PBI_ annotations; own annotations allowed | covered | TI 6; TM; files cannot show it (Power BI's own PBI_ annotations are legitimate) |
| TMDL | One file per role; modelPermission; no PBI_Id on new roles | covered | TM; examples roles/*.tmdl |
| TMDL | Calendar objects for calendar time intelligence | covered | RD 34; MO D (Calendars); example preview/Calendar |
| TMDL | A comment above each Power Query step; step name rules | covered | DE; SS 1; P001 (fail); name rules optional (DE) |
| Project files | definition.pbism as shipped; byPath or byConnection | covered | TI 13; SR step 3; starter example |
| Project files | TMDL and PBIR preferred formats | covered | F001 (fail) |
| Agent tooling | With the modeling server connected, use it instead of files | not adopted | CI: the template works on files and never changes a model through a server |
| AI readiness | Ask how the model will be used before AI preparation | covered | MS 17 (brief switch) |
| AI readiness | Copilot on for the tenant; Q&A on for the model | outside this template | tenant setting; starter definition.pbism |
| AI readiness | Star schema, types, explicit measures, hierarchies first | covered | RD A, 40; MS 9, 10 |
| AI readiness | isDefaultLabel on each dimension's name column | covered | MS 17; M303 (note, when the brief turns it on); EX Store[Store Name] (isDefaultLabel) |
| AI readiness | Descriptions read for 200 characters; key words first | covered | MS 17; DE; M302 (note) |
| AI readiness | AI instructions, AI data schema, verified answers: set by a person | outside this template | Prep data for AI is set in Power BI (MS 17; NF) |
| Report design | Chart from the question | covered | RS H |
| Report design | Category and series caps per chart type | covered | RS 45 (Microsoft's skill's limits per chart type); no check: it needs the data |
| Report design | Anti-patterns: no 3-D, axes from zero, no dual axis, no crowded pies | covered | RS 46; VF 24 (example Charts_Features_ClusteredColumn_AxisSettings); no check: no Microsoft source shows how the value of valueAxis.start is written, so the files do not show a breach for certain; 3-D: no file property; crowded pies: it needs the data |
| Report design | Agent mistakes: hex colours, off-grid, empty alt text, chart type as title | covered | V009, G003, A001, A003 (warn) |
| Report design | Findings as advice in three levels | not adopted | the template's own levels (fail, warn, note) by its level rule |
| Report design | Pre-flight: titles, sort, grid, overlap, title band | covered | RS 49, 62; LS; A003, G001-G006 |
| Report design | Contrast, colour not alone, alt text, tab order | covered | RS J; TH; A001, A002, A004 |
| Report design | Keep visual headers on | not adopted | the owner's rule turns header icons off (PI 4; H001) |
| Report design | Overview first; every click changes something | covered | RS B, 53; files cannot show it |
| Report design | Tooltip pages small; drillthrough with back button | covered | RS C, D; V001-V005 |
| Report design | Bookmark naming, reset bookmark, test every one | covered | RS 8-10, 15; V010 (warn) |
| Report design | Slicers beside the title or in a left rail | covered | LS |
| Report design | Colour follows the data; one measure one colour | covered | TH; RS 37-38. Hex colours per visual: not adopted (owner's rule, V009) |
| Report design | At most four text sizes; 9 pt minimum | covered | TH (theme text classes); V009 (warn) |
| Report design | A design brief with tone and a signature element | out of scope | a source's own styling process |
| Report design | New reports at 1920 x 1080 | not adopted | the owner chose 1280 x 720 (LS) |
| Report mechanics | Three slicer kinds and their roles | covered | examples Slicers page (EX) |
| Report mechanics | Dropdown slicer with a header needs about 80 pixels | not adopted | LS (owner-approved) sets 56; DB step 4 looks for slicers too small for their text |
| Report mechanics | A visual with its own container formatting loses theme padding | covered | TH (listed as not confirmed; developer tests) |
| Report mechanics | A slicer's tooltip field needs tooltips on | covered | PI 5 (exception per visual); H002 |
| Report mechanics | In a filter's Where clause refer to the From alias | covered | RS 51; VF 1; V015 (warn) |
| Report mechanics | Bookmark files, bookmarks.json, suppressData, targets by name | covered | RS 8-11; V008, V010 (warn); examples bookmarks |
| Report mechanics | Button actions and their targets; back button on drillthrough | covered | RS 11, 23; V001 (fail), V008 (warn); examples |
| Report mechanics | Drillthrough page binding with boundFilter | covered | RS 24; example Drillthrough_Store; J003 (fail) |
| Report mechanics | Conditional formatting forms; icon names only from the catalogue | covered | RS F; example Tables_Table_StoreSales; icon names not restated (guidance gap) |
| Report mechanics | Never create multi-row card, map or filled map | covered | RS 47; V016 (warn) for map and filledMap, U105 (note) for multiRowCard and card; INDEX ships the legacy cards only to read old reports |
| Report mechanics | Table and matrix sizing and presets | out of scope | a source's own styling; table versus matrix choice is in RS H |
| Report mechanics | PBIR structure: pageOrder, unique names, schema | covered | PV; J003, N005, V011 |
| Report mechanics | Images in RegisteredResources and registered in report.json | covered | RS 69; example Elements_Image_ExampleMark; V017 (warn) |
| Report mechanics | KPI visual: indicator is a measure, trend on dates | covered | RS H; example Cards_KPIs_KPI_SalesAgainstTarget |
| Report mechanics | definition.pbir byPath or byConnection | covered | SR step 3; J002 |
| Report mechanics | Branch before editing; no commit without asking | covered | CI |
| Report mechanics | Optional mobile.json per visual | covered | RS G; PI 10 |
| Theming | Custom theme registered in report.json | covered | TH; T001 (fail) |
| Theming | Theme content rules (data colours, text classes, style presets) | not adopted | the owner's theme is fixed (CI, TH) |
| Theming | Hex colours on visuals survive a theme change | covered | TH; V009 (warn) |
| Theming | Generated base theme with padding | not adopted | the owner's theme is fixed |
| Field parameters | Three-column table with NAMEOF; slicer and target visual wired | covered | MO C; RS A; M821 (fail), M822 (warn), U003, U103; examples |

### D2. SQLBI (DAX)

| Topic | Practice | Status | Where covered, or why not adopted |
| --- | --- | --- | --- |
| Formatting | SQLBI's layout rules for DAX | covered | DS B 22-30; M520 (warn). Quotes only when needed: not adopted (Microsoft's skill quotes always); indentation not checked (TMDL tabs); := does not apply |
| References | Columns with table, measures without | covered | DS 10; M010 (warn) |
| Name clashes | A measure never shares a name with a column | covered | MS 3; M006 (fail) |
| Temporary columns | Columns a formula makes start with @ | covered | DS 30; M520 (warn) |
| Variables | Use variables; computed once where defined | covered | DS 8; M507 (warn) |
| DIVIDE | DIVIDE usually; plain / in iterators after removing zeros | covered | DS 2; M502 (fail); exception in the brief |
| IFERROR | Not recommended | covered | DS 1; M501 (warn) |
| SUMMARIZE | SUMMARIZE only to group; ADDCOLUMNS for new columns | covered | DS 32; M522 (warn) |
| SUMMARIZECOLUMNS | Filters in an outer CALCULATETABLE; value filter behaviour Independent | covered | DS 33; M523 (note). Value filter behaviour: MF 17 (preview; example preview/ValueFilter; M841 until section 11 of the brief lists it) |
| KEEPFILTERS | When to use KEEPFILTERS | covered | DS 6 (second bullet); files cannot show it (meaning) |
| Filter columns | Filter columns, not tables; split AND conditions | covered | DS 6; M505 (warn) |
| Removing filters | REMOVEFILTERS, ALL, ALLSELECTED, ALLEXCEPT each for its job | covered | DS 20; M519 (warn) for ALL as a filter argument; ALLSELECTED and ALLEXCEPT judged in the review (ALLEXCEPT depends on the query) |
| ALLSELECTED | Never call a measure with ALLSELECTED inside an iteration | covered | DS 34; no check: it needs the chain of measures |
| COALESCE | COALESCE for readability; store the measure in a variable | covered | DS 7 (second paragraph); no check |
| BLANK | Expressions that look equal can differ with BLANK | covered | DS 7; files cannot show it |
| Function names | PascalCase, dot prefixes, camelCase parameters | covered | MO A6; DS 39; M807 (warn) |
| Time names | Suffix acronyms (YTD, QTD, MTD, PY and more); % without brackets | covered | MS 3 (YTD, QTD, MTD, PY). Other acronyms and bare %: not adopted (owner's rule) |
| Auto date/time | Off; no column-variation syntax | covered | RD 29; M401 (warn); the .[Date] syntax not checked |
| Future dates | Hide time results after the last date with data | covered | DS (Where sources disagree: helper measure in _Measures) |
| Time patterns | Pick the simplest time pattern that fits the calendar | covered | DS C |
| Mark as date table | Explicit, marked date table | covered | RD 30; M402-M404 |
| DAX patterns | The 23 daxpatterns.com patterns, each for its question | covered | DS C (table of patterns; looked up before use, never pasted) |

### D2b. SQLBI articles and white papers: the practice library

The rows of D2 are the SQLBI practices this template adopts as standards. Beyond them, the skill `pbi-practice-library` (PL) is a second place where practices are covered, as information and not as standards: 2033 short notes, each restating one idea from a public SQLBI article or white paper, with its year and address. Copilot reads the index and one topic file when a task calls for it; the checklist and the standards win; no check reads the library. The notes are therefore not counted in the summary table above.

A note was left out of the library when it was outdated, when it conflicted with the checklist, when this repository already says it (the standards of D2 and of the other sections), when a higher source says otherwise, or when another topic keeps the same note. `library-removed.md` lists every such note with the file that covers it; `library.md` holds the numbers, the decisions and the checks.

| Topic | Files in PL `references/` | Notes |
| --- | --- | ---: |
| DAX evaluation context | `t01-evaluation-context-1.md` to `t01-evaluation-context-2.md` | 156 |
| DAX authoring style | `t02-dax-authoring-style-1.md` to `t02-dax-authoring-style-2.md` | 112 |
| DAX table functions and queries | `t03-table-functions-and-queries-1.md` to `t03-table-functions-and-queries-2.md` | 154 |
| Time intelligence and date tables | `t04-time-intelligence-and-dates-1.md` to `t04-time-intelligence-and-dates-3.md` | 166 |
| Relationships and filter propagation | `t05-relationships-1.md` | 67 |
| Data model design | `t06-data-model-design-1.md` to `t06-data-model-design-2.md` | 127 |
| DAX performance and optimization | `t07-dax-performance-1.md` to `t07-dax-performance-3.md` | 180 |
| Storage engine, model size and memory | `t08-storage-engine-and-model-size-1.md` | 33 |
| Storage modes | `t09-storage-modes-1.md` to `t09-storage-modes-2.md` | 95 |
| Security | `t10-security-1.md` | 45 |
| Calculation groups and field parameters | `t11-calculation-groups-and-field-parameters-1.md` to `t11-calculation-groups-and-field-parameters-2.md` | 87 |
| Window functions and visual calculations | `t12-window-functions-and-visual-calculations-1.md` | 78 |
| User-defined functions in DAX | `t13-user-defined-functions-1.md` | 48 |
| Business calculation patterns | `t14-business-calculation-patterns-1.md` to `t14-business-calculation-patterns-5.md` | 244 |
| Report-facing DAX and report design | `t15-report-facing-dax-1.md` to `t15-report-facing-dax-5.md` | 290 |
| Tooling, workflow and AI assistance | `t16-tooling-and-workflow-1.md` to `t16-tooling-and-workflow-3.md` | 151 |

### D3. data-goblin/power-bi-agentic-development (GPL: ideas only)

| Topic | Practice | Status | Where covered, or why not adopted |
| --- | --- | --- | --- |
| Layout | Summary top-left, detail bottom-right | not adopted | no Microsoft page states it; idea only |
| Page title | A title text box at the top-left of every page | covered | RS 70; LS (title band); V018 (note) |
| Spacing | Equal gaps and margins | covered | LS; G004, G006 (warn) |
| Theme | A custom theme; no one-off formatting | covered | TH; T001 (fail), V009 (warn) |
| Bindings | Every field a visual uses exists | covered | B001 (fail) |
| Report measures | Keep report-level measures and visual calculations rare | covered | RS 65-67; files cannot show it (reuse by other reports) |
| Limits | Visuals, cards and slicers per page | not adopted | checklist item 20 numbers win (RS 63; V006, V007) |
| Alt text | Alt text on every data visual | covered | RS 55; A001, A004 (warn) |
| KPIs | Prefer the KPI visual when a target exists | covered | RS H; example KPI. Colouring and rounding advice: a source's styling (out of scope) |
| Tables | Matrix for hierarchies; formatting advice | covered | RS H for the choice; the formatting is a source's styling (out of scope) |
| Anti-patterns | Gauge as KPI, unsorted bars, dual axis, 3-D | covered | RS 46; no check: the value form of the axis properties is not confirmed by a Microsoft source; the gauge and the sort are judgements; 3-D has no file property |
| Identity | One tone, one signature element | out of scope | a source's own styling |
| Evidence | Check callout numbers against the data | covered | SM (What the files cannot tell); DB; files cannot show it |
| Tooltip pages | Only for another view; no page filters | covered | RS C; V002-V005; design-time filters: V013 (warn) |
| Filter pane | Lock scope filters, hide clean-up filters | covered | RS 52, 54; example report filter |
| Phone layout | Never hand-write mobile.json | covered | RS 42; PI 10 |
| Report review | Usage, access, load times, accessibility | covered | CR (items 68, 76, 78 are people's evidence) |
| Naming checks | Regex checks for code-style names; no Dim/Fact prefixes | covered | M007 (fail), M118 (warn); 1YP-style periods not adopted (owner's PY) |
| TMDL naming | Key suffix, numbered folders, __Measures, % prefix | not adopted | owner's names: _Measures (MS 1), (%) suffix (MS 3); Keys folder agrees (MS 6) |
| Folder separator | Backslash or forward slash | covered | MS 2 (backslash) |
| Measure tables | One _Measures; calculated form for DirectQuery and Direct Lake | covered | MS 1; M001, M002 (fail); scaffold.py |
| DAX references | Never qualify measures; always quote tables | covered | DS 10; M010 (warn); quoting: both forms pass |
| UDF authoring | Signature, VAL versus EXPR, testing | covered | MO A; M801-M805 |
| Model review | Ambiguous paths, orphan tables, fail-open RLS, limited relationships | covered | RD; SS; M411, M605, M706 (warn) |
| Date marking | Marking with an integer date key | covered | RD 30; example Date.tmdl |
| Q&A retiring | Stop tuning Q&A; focus on descriptions and AI setup | covered | NF (linguistic schema: deprecated); MS 17 |
| Renaming | A rename must follow every stored name | covered | MS (Existing models); find_references.py; B001, M901-M908 |
| Security | Dynamic RLS fails closed; OLS limits | covered | SS 31, 35; M605, M607, M608 |
| Calculation groups | Precedence, recursion, type traps | covered | MO B5, B6; M813 (warn) |
| Direct Lake | OneLake versus SQL behaviour | covered | SS 27 |
| Power Query | Types early, prune early, no needless buffers | covered | SS A; P001 (fail) |
| Rule exceptions | Exceptions stored as model annotations | not adopted | the template records exceptions in the brief (sections 9 and 10) |
| Other plugins | Custom visuals, paginated, Fabric admin, other products | out of scope | custom visuals, paginated reports, other systems |

### D4. github/awesome-copilot

| Topic | Practice | Status | Where covered, or why not adopted |
| --- | --- | --- | --- |
| References | Qualify columns, never measures | covered | DS 10; M010 (warn) |
| Errors and BLANK | DIVIDE; no IFERROR; leave BLANK | covered | DS 1, 2, 7; M501, M502, M506 |
| Nesting | One CALCULATE with several filters | covered | DS 8; M521 (warn) |
| Layering | Base measures, then derived ones | covered | DS 21 (judged in the review); files cannot show it for certain |
| Measure names | Period first, Count of, category prefixes | not adopted | owner's rule (MS 3; M008) |
| DAX comments | Long comments with history in each measure | not adopted | meaning goes in /// descriptions (DE); history in commits (CI) |
| File targeting | Instruction files that never load for .tmdl | covered | TI targets .tmdl |
| Model basics | Star schema; _Measures; one-way filters; Unknown member | covered | RD A, B; MS 1; SS 24; M001, M405, M412 |
| Column names | CustomerKey, DimProduct style names | not adopted | Microsoft's skill (higher) asks for words with spaces, no prefixes (RD 42) |
| Summarise | Amounts summarise by Sum | not adopted | MS 9 and the best practice rule (higher): M107 |
| Running total | FILTER over the whole date table | not adopted | Microsoft Learn (higher): no FILTER over a table (DS 6, M505); DS C cumulative-total pattern |
| RLS | Dynamic rules end in FALSE; test roles; groups | covered | SS 31, 34; M605 (warn) |
| Report layout | 6 to 8 visuals; 8/16/24 spacing | covered | LS (spacing). 6 to 8 visuals: not adopted (item 20 numbers, V006, V007) |
| Charts | Axes from zero; sort by value; few categories | covered | RS 45, 46; VF 24; no check for axes from zero: the value form of valueAxis.start is not confirmed by a Microsoft source; the sort and the categories need a judgement or the data |
| Gauge | Gauge as a fast KPI visual | covered | NF (Card, KPI, gauge); example gauge |
| Text | Font sizes and families | not adopted | the owner's theme sets text classes (TH) |
| Interaction | Tooltip size; named bookmarks; documented interactions | covered | RS B, C, 53; V003 |
| Mobile | Portrait first; 44-pixel targets | not adopted | the template never edits phone layout (RS 42) |
| Accessibility | Contrast, alt text, keyboard, tab order | covered | RS J; A001-A004 |
| PBIP layout | A project tree with Model and measures folders | not adopted | wrong against Microsoft's layout (PV) |
| ALM | Branches, deployment pipelines, environment parameters | out of scope | deployment; branches and parameters covered (CI; SS 8) |
| Modelling skill | Connect through the modeling server | not adopted | the template works on files (CI) |
| Prompts | Performance Analyzer and other tracing tools | outside this template | Desktop and service tools; CR (item 68) |
| Custom visuals | pbiviz development | out of scope | custom visuals |

## E. Mofaji/Agentic-PBIP-Template

One row per native topic of the repository (MIT), then its out-of-scope topics. File names of that repository are not given as paths.

| Topic | Practice | Status | Where covered, or why not adopted |
| --- | --- | --- | --- |
| Project layout | .pbip, .Report and .SemanticModel folders | covered | PV (Files); TM; F001-F003 (fail) |
| Wrong project tree | A copied guide with a wrong tree, overridden | not adopted | wrong against Microsoft's layout; the template has no such guide |
| Start from a Desktop-made project | Ship a project Desktop saved | covered | scaffold.py; example starter |
| $schema versions | Keep the report's schema versions; exact version.json value | covered | PI 7; S001, J003 (fail). The exact version.json value: not adopted (no Microsoft source) |
| Forbidden properties | Keys that make Desktop refuse a file | covered | J003 (fail) checks every file against Microsoft's schema; single-key claims without a source not adopted |
| Page names | Pages keep their ids; reviews use display names | covered | PV; N001 (fail) |
| Page order | No repeated or orphan ids in pageOrder | covered | V011 (warn) |
| Resources registered | Every image or resource used is listed in report.json | covered | RS 69; V017 (warn); theme: T001 (fail) |
| Resource files exist | Every registered item exists on disk | covered | RS 69; V017 (warn) also reports a resource whose file is not in the report folder; theme: T001 (fail) |
| Model binding | .pbip to report to model chain | covered | SR step 3; J002 (fail) |
| .pbi files | Local settings are not committed or written | covered | PI 9; TI 13 |
| UTF-8 without BOM | No byte-order mark | covered | PI 8; J001 (fail) for JSON. For .tmdl: not adopted (no Microsoft source says a BOM blocks loading) |
| No // comments in TMDL | Comments only inside expressions | covered | TI 3; C001 (fail) |
| Tabs | Tab indentation | covered | TI 5; SM (Gotcha) |
| New TMDL objects with ids | Made-up lineageTag and PBI_Id | not adopted | TI 6 forbids them |
| Relationship ends | A relationship to a missing column blocks loading | covered | RD 10; M901 (fail) |
| Name clash | Measure named like a column; duplicates | covered | M005, M006 (fail); duplicate column names not checked |
| Unique measure names | One name once in the model | covered | MS 3; M005 (fail) |
| Unresolved DAX references | A Table[Column] that does not exist | covered | DS 18; M908 (fail) |
| Filter expressions | Filter conditions use kinds the schema knows | covered | J003 (fail) against the semanticQuery schema |
| Calculated table columns | sourceColumn matches the names SELECTCOLUMNS returns | covered | SS 40; M910 (warn; formulas built with ROW or SELECTCOLUMNS) |
| Calculated objects after a file edit | A new calculated table is empty until a refresh in Desktop | covered | SS 41; files cannot show it |
| Fresh project renders empty | No data until the first refresh | covered | SS 41 (a project made from the starter shows no data until its first refresh); files cannot show it |
| Auto date/time annotation | Do not flip the annotation by hand | covered | RD 29; M401 (warn); set in Desktop only |
| Desktop overwrites files | Save in Desktop before outside edits | covered | CI (save first); DB |
| report.json edited by the agent | Themes registered by editing report.json | not adopted | PI 9: the developer imports the theme; scaffold.py --register-theme only after a yes |
| Custom theme registration | Theme in RegisteredResources and report.json | covered | TH; T001 (fail) |
| Base theme | Desktop's base theme in SharedResources | covered | PI 9 (StaticResources read only) |
| Theme root keys | Only ten root keys allowed | not adopted | contradicted by Microsoft Learn's custom theme page |
| Theme cache | A changed theme needs a restart | not adopted | the template never edits the theme (TH) |
| Page background image | SVG page backgrounds | out of scope | a source's own styling |
| One measures table | Measures in _Measures | covered | MS 1; M001, M002 (fail) |
| Descriptions | Every measure described | covered | DE; D001 (fail) |
| Format strings | Key measures formatted | covered | MS 4; M009 (fail). Whole numbers everywhere: a source's styling |
| Star schema and relationships | Facts, dimensions, one-to-many, single direction, USERELATIONSHIP | covered | RD A, B; M405-M412 |
| Date table | Marked date table | covered | RD 30; M402-M404; example Date.tmdl |
| Month order | Month names sorted by number | covered | RD 35; M113 (warn) |
| DAX habits | Variables, DIVIDE, references, no FILTER over tables | covered | DS A; M010, M502, M505, M507 |
| Summarise and hide | IDs not summarised; keys hidden | covered | MS 7, 9; M102, M107 |
| RLS and OLS | Dimension filters, USERPRINCIPALNAME, deny by default, View as | covered | SS D; M601-M608 |
| Composite, DirectQuery, aggregations, incremental refresh | When to mix modes; Dual; aggregations; RangeStart and RangeEnd | covered | SS C; M701-M709, U004; examples |
| Field parameters | Three-column tables; fieldParameters on visuals | covered | MO C; RS A; M821, M822; examples |
| Image from a measure | An image visual that shows a picture a measure returns | covered | VF 21; EX Elements_Image_FromMeasure, measure [Selected Product Image], column Product[Product Image] (dataCategory ImageUrl); form from Microsoft's skill (authoring/image.md); V017 covers registered files only |
| SVG measures | Separate SVG measure table and drawing rules | not adopted | no Microsoft source; a separate table breaks MS 1 (M001) |
| Sorting in a visual | sortDefinition on charts | covered | RS 62; example sort definition. 'Always descending': a source's styling |
| Top N matches the title | A title promising N shows N | covered | RS 49; A003 (warn); files cannot show it (meaning) |
| Locked and reset filters | Locked report filters; reset button | covered | RS 15, 52; example report filter |
| Bookmarks that swap visuals | Stacked visuals switched by bookmarks | covered | RS B; LS (layered on purpose); U103; example Bookmarks page |
| Buttons with bookmarks | Button action type Bookmark | covered | RS 11; V008 (warn); example |
| Visual interactions | NoFilter in page.json | covered | RS 53; example |
| Visuals per page | Six to eight | not adopted | checklist item 20 numbers (V006, V007) |
| Tooltip and drillthrough pages | 320 x 240; back button; hidden | covered | RS C, D; V001-V003 |
| Accessibility | Contrast, colour, tab order | covered | RS J; TH; A001-A004 |
| Mobile layout | Portrait layout | covered | RS G (Copilot never edits it) |
| Documentation page | An SVG page that documents the project | covered | Info or Help page: SR step 6 (item 75). The SVG page itself: a source's styling (out of scope) |
| Visual chrome off | No titles, borders or backgrounds | out of scope | a source's own styling (clashes with item 55) |
| Valid JSON is not proof | Look at the rendered page | covered | CI (reload and look); DB |
| Screenshot review | What to look for on each picture | covered | DB step 4 |
| Load-error dialogs | Read Desktop's error dialogs | covered | DB (ask the developer what Desktop says); files cannot show it |
| Static checks before Desktop | Predict load errors from files | covered | check_project.py: M005, M006, M901-M909, B001, V011, J003 |
| JSON and structure | Parse every file; required files | covered | J001-J003, F001-F003 (fail) |
| Unused objects audit | Unused objects, missing formats, local paths, both-direction | covered | M201, M009, P005, M405, B001 |
| Spec before build | A spec per page | covered | docs/report-brief.md |
| Hooks with a fix budget | Automation that never traps a session | out of scope | another assistant's hooks (another tool) |
| Custom visuals | pbiviz skill and checks | out of scope | custom visuals |
| Email reports and alerts | Python mail and alert scripts | out of scope | other systems (email) |
| Deployment | CI/CD setup, deployment pipelines | out of scope | publishing and deployment |
| Other vendors' tools | Hosted model tests, third-party DAX and model editors | out of scope | other vendors' tools |
| Their styling | Chrome, labels, SVG cards, header band | out of scope | a source's own styling |

## F. The owner's minimum list

| Topic | Status | Guidance | Example | Check |
| --- | --- | --- | --- | --- |
| User-defined functions | covered | MO A; DS D | functions.tmdl; Total Sales with Tax | M801-M805; U001 (note) |
| Calculation groups | covered | MO B; DS D | Time Calculation.tmdl; matrix Tables_Matrix_SubcategoryByTime | M811-M814; U002 (note) |
| Measures with the same formula | covered | DS 12, 13 | - | M508, M509 (warn) |
| A default for table and column names | covered | RD E (41-45) | Examples.SemanticModel | M118, M119 (warn) |
| DAX style from SQLBI | covered | DS B (22-31) | _Measures.tmdl | M520 (warn) |
| DAX patterns including time intelligence | covered | DS C (23 patterns); RD C | Total Sales YTD, PY, vs PY (%); preview/Calendar | M402 (fail), M513 (warn) |
| Error functions | covered | DS 1 | - | M501 (warn) |
| DIVIDE | covered | DS 2 | Average Line Amount | M502 (fail) |
| COUNTROWS | covered | DS 3 | # Order Lines | M503 (warn) |
| SELECTEDVALUE | covered | DS 4, 5 | Discount Percentage Value | M504, M517 (warn) |
| Variables | covered | DS 8, 9 | Total Sales vs PY (%) | M507, M514 (warn) |
| FILTER as a filter argument | covered | DS 6 | - | M505 (warn) |
| Turning blanks into values | covered | DS 7 | - | M506 (warn) |
| Column and measure references | covered | DS 10; MS 5 | _Measures.tmdl | M010 (warn), M908 (fail) |
| Auto date/time tables | covered | RD 29 | - | M401 (warn) |
| The date table | covered | RD 30-34 | Date.tmdl | M402 (fail), M403, M404 (warn) |
| Star schema | covered | RD A | Examples.SemanticModel | M411, M412, M115, M417 (warn) |
| Role-playing dimensions | covered | RD 7 | relationships.tmdl (ship date); Total Sales by Ship Date | U006 (note), M410 (warn) |
| Slowly changing dimensions | covered | RD 8 | - | files cannot show it |
| Surrogate keys | covered | RD 9 | Date Key, Store Key | M110 (warn); uniqueness: files cannot show it |
| One-to-one relationships | covered | RD 22 | Store Detail to Store | M409 (warn) |
| Many-to-many relationships | covered | RD 19, 20 | Sales Target to Product | M406, M407 (warn) |
| Two-way relationships | covered | RD 18, 21 | Sales to Product | M405, M408 (warn) |
| Active versus inactive relationships | covered | RD 7, 23-25 | ship date relationship | M410, M414 (warn), M415 (fail) |
| Inactive relationships nothing uses | covered | RD 23 | - | M410 (warn) |
| Tables with no relationship | covered | RD 4 | - | M411 (warn) |
| Sort columns | covered | RD 12, 16, 35 | Date.tmdl (Month Name by Month Number) | M113 (warn), M903, M907 (fail) |
| Security: fixed and user-based role rules | covered | SS 28, 31 | roles Northport Stores, Own Store | M603, M605 (warn) |
| Security: object-level security | covered | SS 35 | roles No Product Cost, No Sales Targets | M606, M607 (warn), M608 (fail) |
| Security: filtering on dimension tables | covered | SS 29 | Own Store (rule on Store) | M602 (warn) |
| Security: common mistakes | covered | SS 36 | - | M601-M605, M414, M415; testing: files cannot show it |
| Performance: data reduction | covered | SS B (13-21) | Sales Source not loaded | M201 (note), M105, M111 |
| Performance: columns with too many distinct values | covered | SS 20 | - | files cannot show it (distinct counts); M111 (warn) |
| Performance: data types | covered | MS 10; SS 16 | - | M108, M110 (warn), M109 (fail) |
| Performance: slow DAX patterns | covered | DS A | - | M501-M517 (warn) |
| Performance: aggregations | covered | SS 25 | Sales Aggregate | U004 (note) |
| Performance: incremental refresh | covered | SS 26 | Sales refresh policy; RangeStart, RangeEnd | M707, M709 (fail), M708 (warn) |
| DirectQuery and composite models | covered | SS 22-24 (models on a published model: SS 23) | storage/DirectQuery (Dual, aggregation) | M513, M701-M706, U008, U104 |
| A Power Query standard | covered | SS A (1-12); DE | partitions in Examples.SemanticModel | P001 (fail), P002-P006 (warn) |
| Query folding | covered | SS 2, 3 | - | files cannot show it; P002, M708 (warn), M701 (fail) |
| Referencing queries | covered | SS 4 | expressions.tmdl (Sales Source) | P003 (warn) |
| Background refresh | covered | SS 11 (a Desktop option) | - | no check: files cannot show it |
| Field parameters: when to suggest | covered | RS 1; MO C1; NF | - | U003, U103 (note) |
| Field parameters: how built in model files | covered | MO C2-C4 | Sales Metric.tmdl, Sales Breakdown.tmdl | M821 (fail), M822 (warn) |
| Field parameters: slicer and visuals | covered | RS 2-5 | Field_Parameters page (slicers and chart) | J003 (fail); B001 (fail) |
| Field parameters: working example | covered | INDEX (EX) | Field_Parameters page; Sales Metric, Sales Breakdown | the examples pass check_project.py |
| Bookmarks and buttons that switch views | covered | RS B (7-15) | Bookmarks page; bookmarks folder | V008, V010 (warn), U103 (note) |
| Report page tooltips | covered | RS C (16-22) | Tooltip_StoreSales | V002-V005 (warn) |
| Drillthrough | covered | RS D (23-29) | Drillthrough_Store; back and drillthrough buttons | V001 (fail) |
| Sync slicers | covered | RS E (30-33) | RegionSync slicers | U101 (note) |
| Conditional formatting | covered | RS F (34-39) | Tables_Table_StoreSales (icons) | V009 (warn) |
| Mobile layout | covered | RS G (40-43; Copilot never edits it) | - (owner's rule) | files cannot show it (phone canvas); H001, H002 read mobile.json |
| Choosing the chart type | covered | RS H (44-48) | one example of every core visual | files cannot show it (fit to the question) |
| Accessibility: alt text | covered | RS 55 | every example data visual | A001, A004 (warn) |
| Accessibility: tab order | covered | RS 56 | positions in every example | A002 (warn) |
| Accessibility: titles | covered | RS 49, 57 | every example data visual | A003 (warn) |
| Accessibility: decorative shapes | covered | RS 58 | Elements_Shape_Rectangle | files cannot show it (how 'out of tab order' is stored is not confirmed) |

## G. Rows still open

None. Every row above is covered, out of scope, outside this template or not adopted, each with its reason in the row.
