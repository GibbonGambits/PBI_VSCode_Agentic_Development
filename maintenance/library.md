# Practice library: working paper

How the practice library (skill `pbi-practice-library`) was built, the decisions made without asking, and what was checked. GitHub Copilot does not read this folder. The work was done on 11 November 2026; a second round of fixes after an independent review followed on 12 November 2026.

## The job

Put the notes drawn from public SQLBI articles into the template as a reference library: information that Copilot opens when a task calls for it, not rules to enforce. Every note is kept unless one of six removals applies (the sixth, out of scope, was added in the second round). The kept notes are rewritten short, sorted by topic on two shelves, and listed in one index. `library-removed.md` in this folder holds one row for each removed note, by ID only.

## Where the work stands

Finished, in two rounds. In the first, all sixteen topics were compared with the repository, rewritten and rendered; duplicates across topics were removed; the index, the tests, the README, the notices, the sources record, the coverage file and the test prompts are updated; the reviews ran and their findings are dealt with. The second round fixed what an independent review of the pull request found (section "Second round" below). Nothing is open.

## Numbers

### Counts

| Step | Notes |
|---|---:|
| At the start | 2318 |
| Removed, group 1: outdated | 35 |
| Removed, group 2: conflicts with the checklist | 20 |
| Removed, group 3: the repository already says it | 141 |
| Removed, group 4: not adopted: a higher source says otherwise | 48 |
| Removed, group 5: duplicate of a note kept in another topic | 62 |
| Removed, group 6: out of scope: depends on a custom visual, another vendor's tool or another system, or on publishing or deploying | 120 |
| **Kept in the library** | **1892** |

### Kept notes by topic and shelf

| Topic | Files | General practice | Special-case techniques and facts | Total | Marked Check |
|---|---:|---:|---:|---:|---:|
| T01 DAX evaluation context | 2 | 47 | 107 | 154 | 16 |
| T02 DAX authoring style | 2 | 58 | 50 | 108 | 14 |
| T03 DAX table functions and queries | 2 | 46 | 108 | 154 | 38 |
| T04 Time intelligence and date tables | 2 | 40 | 109 | 149 | 45 |
| T05 Relationships and filter propagation | 1 | 19 | 48 | 67 | 13 |
| T06 Data model design | 2 | 48 | 68 | 116 | 14 |
| T07 DAX performance and optimization | 3 | 63 | 108 | 171 | 39 |
| T08 Storage engine, model size and memory | 1 | 9 | 20 | 29 | 2 |
| T09 Storage modes | 2 | 37 | 49 | 86 | 42 |
| T10 Security | 1 | 10 | 33 | 43 | 10 |
| T11 Calculation groups and field parameters | 2 | 21 | 64 | 85 | 16 |
| T12 Window functions and visual calculations | 1 | 33 | 44 | 77 | 8 |
| T13 User-defined functions in DAX | 1 | 27 | 20 | 47 | 4 |
| T14 Business calculation patterns | 4 | 47 | 196 | 243 | 68 |
| T15 Report-facing DAX and report design | 4 | 81 | 171 | 252 | 34 |
| T16 Tooling, workflow and AI assistance | 2 | 56 | 55 | 111 | 23 |
| **All** | **32** | **642** | **1250** | **1892** | **386** |

By strength: Must 307, Should 483, Consider 144, Option 531, Fact 427.

### Checklist conflicts (group 2), by checklist item

| Checklist item | Notes removed |
|---|---|
| 12 | T01-A228-3, T05-A078-3, T05-A236-2, T11-A268-2, T15-A166-5 |
| 14 | T03-A291-8, T05-A095-3, T05-A095-4, T14-A015-3, T15-A166-2 |
| 25 | T06-A173-2 |
| 31 | T06-A035-4 |
| 32 | T03-A045-3 |
| 33 | T07-A044-4 |
| 35 | T14-A323-10 |
| 38 | T06-A290-10, T14-A326-7 |
| 49 | T15-A325-17 |
| 68 | T07-A156-2, T09-W380-2 |

### Not adopted (group 4)

| Note | Higher source | Where the repository says otherwise | Reason |
|---|---|---|---|
| T01-A020-4 | Microsoft | `dax-standard.md`, rule 8 | The DAX standard, following Microsoft's skill, asks for one CALCULATE with all its filters or variables, and warns on CALCULATE written directly inside CALCULATE (M521). |
| T01-A064-7 | Template rule | `dax-standard.md`, rule 21 | The DAX standard has derived measures call the base measure and never repeat its aggregation; a variable evaluated before the iteration gives the same result. |
| T01-A228-7 | Microsoft | `dax-standard.md`, rule 20 | ALLEXCEPT is used only when the kept column is filtered directly; otherwise the standard asks for REMOVEFILTERS plus VALUES, not a longer ALLEXCEPT list. |
| T01-A124-6 | Microsoft | `storage-and-security.md`, rule 17, check M105 | A dimension attribute that a Power Query merge can supply is not built as a DAX calculated column. |
| T02-A068-4 | Microsoft | `dax-standard.md`, rule 7, check M506 | Blanks stay blank: a measure does not add zero to a result, so the zero case is handled another way. |
| T02-A154-5 | Template rule | `dax-standard.md`, rule 30 | The template names a column that a formula makes with a leading @ (M520 checks it), so a name written in table[column] form cannot be used. |
| T02-A154-6 | Microsoft | `dax-standard.md`, rule 31 (and rule 30) | Variables get plain names with no underscore prefix, following Microsoft Learn, and a column that a formula makes is marked with a leading @, not with a variable name as table prefix. |
| T02-A316-4 | Microsoft | `dax-standard.md`, rule 37 | A speed rewrite is kept only when it returns the same numbers; this one changes totals through rounding. |
| T03-A022-3 | Template rule | `dax-standard.md`, rule 32 | The DAX standard lets SUMMARIZE only group and adds every computed column with ADDCOLUMNS (M522); the note keeps computed columns inside SUMMARIZE in two cases. |
| T03-A094-9 | Microsoft | `dax-standard.md`, rule 4 | The DAX standard reads one selected value with SELECTEDVALUE and warns (M504) on IF with HASONEVALUE and VALUES, the form this rule requires. |
| T03-A106-4 | Template rule | `dax-standard.md`, rule 30 | The DAX standard starts the name of a column made by SELECTCOLUMNS or ADDCOLUMNS with @ (M520), not with a table prefix. |
| T03-A129-2 | Template rule | `model-standard.md`, rule 1 | The model standard keeps every measure in the one visible table _Measures (M001, M002); this recipe hosts its helper measures in a separate hidden calculated table. |
| T03-A341-2 | Microsoft | `dax-standard.md`, rule 32; Where sources disagree (SUMMARIZECOLUMNS inside a measure) | The DAX standard records that Microsoft's skill uses SUMMARIZECOLUMNS by default for grouping with values, also inside a measure, and that this wins over keeping it for advanced cases. |
| T04-A073-4 | Microsoft | `relationships-and-dates.md`, rule 30, check M402 | A model with time intelligence marks its date table; a workaround in place of the mark is not used. |
| T04-A073-6 | Microsoft | `relationships-and-dates.md`, rule 30, check M402 | A model with time intelligence marks its date table; a dummy table in place of the mark is not used. |
| T04-A073-7 | Microsoft | `relationships-and-dates.md`, rule 30, check M402 | A model with time intelligence marks its date table; rewriting measures in place of the mark is not used. |
| T04-A199-6 | Microsoft | `relationships-and-dates.md`, rule 30 | The template requires a marked date table wherever time intelligence is used (M402 fails otherwise), as Microsoft Learn and Microsoft's best practice rule ask; clearing filters in each measure does not replace the mark. |
| T05-A158-6 | Template rule | `model-standard.md`, rule 1 | The model standard keeps every measure in the one visible table _Measures (M001, M002); a separate hidden table for slicer helper measures breaks that rule. |
| T06-A009-3 | Microsoft | `storage-and-security.md`, rule 17, check M105 | A sortable year-month number is a row value Power Query can supply; it is not built as a DAX calculated column. |
| T06-A035-3 | Microsoft | `relationships-and-dates.md`, rule 17 | The standard says a fact key with no match in its dimension is put right at the source; the note leaves such keys unmatched on purpose. |
| T06-A062-11 | Microsoft | `dax-standard.md`, section B, SQLBI rules the template does not check | Measures are written in TMDL, which always uses the form measure 'Name' =, so the standard records that the := form does not apply. |
| T06-A062-6 | Microsoft | `storage-and-security.md`, rule 17, checklist item 27 | A calculated column is used only when the formula needs a measure or a DAX-only function; the note treats both forms as equal when size is no concern. |
| T06-A075-18 | Microsoft | `relationships-and-dates.md`, rule 30 | The standard requires a marked date table wherever time intelligence is used, whatever the key type (M402 fails otherwise); it does not accept that a date-typed key makes the mark unnecessary. |
| T06-A191-3 | Microsoft | `storage-and-security.md`, rule 17, check M105 | A padded unique name built from a rank by code is a value Power Query can supply; it is not built as a DAX calculated column. |
| T06-A192-3 | Microsoft | `storage-and-security.md`, rule 17, check M105 | A unique sort key from column values needs no measure; Power Query or the source supplies it, not a DAX calculated column. |
| T06-A224-2 | Microsoft | `relationships-and-dates.md`, rule 27 | The standard, following Microsoft's best practice rule, prefers whole-number relationship keys, date keys included (M110 warns on a date key), and the shipped example relates facts to the date table on a whole-number key. |
| T06-A360-5 | Microsoft | `more-model-features.md`, rule 7; storage and security rule 17 | A user-context calculated column is kept for values that depend on the reader; plain row arithmetic comes from Power Query. |
| T06-A360-6 | Microsoft | `native-features.md`, calculated columns row; storage and security rule 17 | A user-context calculated column is kept for values that depend on the reader; plain row arithmetic comes from Power Query. |
| T07-W378-16 | Microsoft | `relationships-and-dates.md`, rule 1 | The standard, following Microsoft's star schema guidance, never mixes the job of a fact table and of a dimension in one table; the note weighs folding a dimension into the fact table. |
| T07-A061-5 | Microsoft | `relationships-and-dates.md`, rule 1 | The standard, following Microsoft's star schema guidance, keeps descriptive columns in dimension tables; the note weighs merging a large dimension into the table on the many side. |
| T08-A039-1 | Microsoft | `storage-and-security.md`, rule 17, check M105 | The last process time is not a NOW () calculated column: a value Power Query can supply comes from Power Query. |
| T08-A039-2 | Microsoft | `storage-and-security.md`, rule 17, check M105 | It depends on the NOW () calculated column of T08-A039-1, which the storage standard rules out in favour of Power Query. |
| T09-W380-15 | Template rule | `model-standard.md`, rule 1 | For Power BI today the template gives a DirectQuery model a calculated _Measures table, so calculated tables do exist there; the limit belongs to Analysis Services 2016 only. |
| T09-A237-3 | Microsoft | `storage-and-security.md`, rule 23 | The repository, following Microsoft on composite models, says a calculated column or calculated table cannot depend on a chained (remote) model; this recipe is built on a calculated column of a remote table. |
| T09-A237-4 | Microsoft | `storage-and-security.md`, rule 23 | It describes a relationship on a calculated column of a remote table; the repository, following Microsoft, says a calculated column cannot depend on a chained (remote) model. |
| T10-A090-4 | Template rule | `copilot-instructions.md`, existing objects keep their names | Existing measures keep their names; the approach renames every original measure. |
| T10-A279-9 | Template rule | `report-standard.md`, rule 36 | The report standard sets no colour on a single visual and lets conditional formatting use theme colours only (V009); making a visual transparent by formatting breaks that rule. |
| T10-A282-3 | Microsoft | `storage-and-security.md`, rule 32 | Microsoft's best practice rule says not to put a role's filter on a table with a many-to-many relationship (M604); the note builds its role on exactly that. |
| T10-A288-6 | Microsoft | `relationships-and-dates.md`, rule 9, check M106 | A generated key added to the fact table as a calculated column is not how this template builds relationship keys. |
| T10-A297-6 | Microsoft | `storage-and-security.md`, rule 29 | The security standard, following Microsoft's guidance, puts a role's filter on a dimension table and lets the relationship carry it; a rule on a fact table is listed as a common mistake (M602). |
| T12-A196-4 | Microsoft | `dax-standard.md`, rules 21, 20 and 6 | A time variant calls the base measure and never repeats the aggregation; FILTER over ALL of the fact table removes every filter, not only the date. |
| T14-A019-5 | Template rule | `model-standard.md`, rule 7 | The model standard keeps a column that a hierarchy level uses visible (M104 warns on a hidden one); this recipe builds the hierarchy on copies of the columns and hides those copies. |
| T14-A213-12 | Microsoft | `visual-features.md`, block 16, column widths | A column width is fixed only when the column must not move, not to hide a column. |
| T15-A072-2 | Template rule | `model-standard.md`, rule 3 | Measure names follow the model standard's naming rules (M007, M008), not the wording of one report's labels; a visual can show its own label. |
| T15-A139-4 | Microsoft | `storage-and-security.md`, rule 17, check M105 | A row value that Power Query can supply comes from Power Query, not a DAX calculated column. |
| T15-A222-7 | Microsoft | `relationships-and-dates.md`, rule 19, check M406 | A table at a higher date grain stores the first date of its period and relates one-to-many to the date table. |
| T15-A317-13 | Template rule | `model-standard.md`, rule 1 | The model standard keeps every measure in the one visible table _Measures (M001, M002), so SVG measures get no table of their own to mark private. |
| T16-A221-19 | Template rule | `native-features.md`, Power BI Project format row, check F001; project instructions | The template works on Power BI project files in TMDL; a Visual Studio Analysis Services project is never the starting point. |

### Group 3 by covering file

| File | Notes |
|---|---:|
| `.github/skills/pbi-semantic-model/references/dax-standard.md` | 50 |
| `.github/skills/pbi-semantic-model/references/relationships-and-dates.md` | 34 |
| `.github/skills/pbi-semantic-model/references/model-objects.md` | 15 |
| `.github/skills/pbi-semantic-model/references/storage-and-security.md` | 15 |
| `checklist/checklist.md` | 10 |
| `.github/skills/pbi-semantic-model/references/model-standard.md` | 5 |
| `.github/skills/pbi-report/references/report-standard.md` | 5 |
| `.github/skills/pbi-checklist-review/references/native-features.md` | 3 |
| `.github/skills/pbi-semantic-model/SKILL.md` | 2 |
| `.github/skills/pbi-semantic-model/references/more-model-features.md` | 1 |
| `.github/skills/pbi-report/references/theme.md` | 1 |

Kept notes that hold only the detail the repository lacked: 640 of 1892.

## Decisions

1. **Name of the skill:** `pbi-practice-library`, for what it holds.
2. **Shelves.** "General practice" holds advice that applies to most models. "Special-case techniques and facts" holds a technique for one situation and every note of strength Fact, whatever its kind.
3. **Layout of a note.** Its ID and the note on one line (at most 45 words); then the strength, the mark Check where it applies, the year of the article and the article's address; then when it applies; then a version line where one matters.
4. **Files.** No file is longer than 400 lines. A large topic is split into parts by sub-topic, each part about the same size; the index says which sub-topics each part holds.
5. **The comparison used a fixed copy of the repository,** taken before the library was added, so that no note could be judged "already said" by the library itself.
6. **"Already says" was read strictly:** the same advice at the same level of detail or deeper, with the passage named. Where the repository says part of it, the note was kept and holds only the added detail; the numbers above say how many notes that is.
7. **Group 4 is wider than Microsoft.** A note that cannot be followed together with a rule of this template's own standards (the one measures table, `@` for columns a formula makes, no colour on a single visual, a hierarchy level stays visible) is also not adopted. The table above says which higher source applies to each note.
8. **A note about a preview feature is kept.** It can be followed after the developer's yes, so it does not contradict the rule on preview features. Its version line says that the feature is a preview here.
9. **A note that fits only inside an exception the standards provide for** (a tooltip or header icon on a listed visual, a colour code, a zero the brief asks for, a second measures table) is kept, and its version line names the condition.
10. **A note whose advice depends on a custom visual, another vendor's tool or another system, or on publishing or deploying,** is removed as out of scope (group 6, second round). Where such a thing was only a passing mention, the note was kept and the mention dropped.
11. **A version line may carry this template's own record** (for example that Microsoft now lists push semantic models as retiring, from `feature-inventory.md`). The rest of a note comes from its article only.
12. **Where a note mentions an older view** that came from an older article, the older article's address stands on the note's source line beside the newer one.
13. **One more checklist conflict was found in this job:** T15-A325-17 (one data visual laid over another) against checklist item 49, which allows 0 overlapping visuals. That makes 20 in group 2, not 19.
14. **Duplicates across topics.** The 219 earlier pairs were judged again on the shortened notes: a pair counts as a duplicate only when a reader who has one note gains nothing from the other. Four further duplicates were found by reading the whole list. Duplicates inside one topic were not looked for again: the earlier work had already merged those.
15. **The look-up skill gained a fifth case** (confirming a note marked Check, or reading the article behind a note). Without it the two skills would have said different things.

## The DAX function index (fixed in the second round)

The first round found that `.github/skills/pbi-semantic-model/references/dax-functions.md` missed functions that Microsoft Learn documents, because its builder read only the function groups of Microsoft Learn's table of contents. The builder, `python scripts/refresh_sources.py dax-index`, now also reads Microsoft Learn's sitemap and adds every DAX function page and statement page that the table of contents leaves out. HIGHESTPARENT and LOWESTPARENT, which the first round listed among the missing names, are option values of a function, not functions, and are not added. The version lines that said a function was missing from the index were removed. The second-round section below lists what was added.

## Checks that were run

- **Eight words in a row.** A script that stays outside the repository compared every line of the library with the private file of exact SQLBI sentences (26,686 sentences) and with the saved text of every article. Result on the final files: 0 runs of 8 or more shared words.
- **Notes reworded because of that check: 80.** Every one was checked against its article by a reviewer that had not written it: 77 kept their meaning, 3 were corrected (T05-A078-4, T07-A179-5, T15-A328-9).
- **Source review.** 272 notes in all were checked against their articles: every reworded note, and a random sample of 12 further notes per topic. 265 were right, 7 were corrected. After the removal of duplicates at least 11 reviewed notes remain in every topic.
- **Links.** Every address in the library was opened on 11 November 2026: 339 addresses, all answered. The two sites that notes name without an address also opened.
- **Tests.** `python -m unittest discover -s tests` and `python scripts/check_template.py` pass. `tests/test_library.py` holds the tests of the skill, the topic files, the index and the removal record.

## The repository review

Four fresh, read-only reviewers read the repository's guidance and every library file (the review was split into four parts because of its size). They listed 47 notes as already said elsewhere in the repository, 59 notes as clashing with a checklist item, a standard or a check without saying under which condition they fit, 7 places where two files said different things, and 28 other points. What was done with them:

- **34 notes were moved to group 3** (the repository already says it). A note that adds a reason, a mechanism, a number or an example the repository lacks was kept; two such notes were cut down to that added part.
- **6 notes were moved to group 4** (not adopted): they cannot be followed together with the star schema rule, the rule on unmatched keys, the rule on roles beside a many-to-many relationship, the rule that SUMMARIZE only groups, or the measure naming rule.
- **83 notes got a condition on their version line,** in the same words as their neighbours: the exception row a both-direction, many-to-many or one-to-one relationship needs; the row for a table without relationships; the reason line of a calculated column or table; the floating-point type; a tooltip; a colour; a zero in place of a blank; a tool or a deployment step outside this template.
- **Every topic file now says once, at the top,** that a note may name a tool, a website or a custom visual this template does not use, or describe publishing or deploying, and that this is information for the developer.
- **12 notes were reworded** because they could not be understood without their article. Each was compared with its source sentences afterwards.
- **Between files:** the test prompt E37 now cites checklist items 11 and 12; the project instructions, the README and the look-up skill agree on the fifth look-up case; the library skill says that a failed check is looked up first; its topic table no longer promises Direct Lake notes; the skill and the README say "articles and white papers"; the trigger word SQLBI stays with the look-up skill only; "two files at most" is said in the skill, the index and the README.
- **The index** now lists, for each file, only the DAX functions its notes name.
- **Left as they are:** notes inside one topic that say nearly the same thing from two articles (the removal group is duplicates across topics); notes whose strength word is the article's although they read like a fact; about twenty notes on Analysis Services servers that no Power BI project file can act on.

## Notes reworded after the eight-word check, with the result of the review

| Note | Result |
|---|---|
| T01-A097-2 | meaning kept |
| T01-A193-3 | meaning kept |
| T01-A249-1 | meaning kept |
| T01-A336-4 | meaning kept |
| T01-A336-5 | meaning kept (later removed as a duplicate) |
| T01-A361-3 | meaning kept |
| T02-A143-5 | meaning kept |
| T02-A169-2 | meaning kept |
| T02-A178-4 | meaning kept |
| T02-A293-6 | meaning kept |
| T02-A335-3 | meaning kept |
| T03-A046-4 | meaning kept |
| T03-A055-12 | meaning kept |
| T03-A055-13 | meaning kept |
| T03-A071-8 | meaning kept |
| T03-A104-2 | meaning kept |
| T03-A109-5 | meaning kept |
| T03-A115-4 | meaning kept |
| T03-A129-1 | meaning kept |
| T03-A197-3 | meaning kept |
| T03-A337-1 | meaning kept |
| T04-A029-1 | meaning kept |
| T04-A114-5 | meaning kept |
| T04-A121-14 | meaning kept (later removed as a duplicate) |
| T04-A264-3 | meaning kept (later removed as a duplicate) |
| T04-A281-10 | meaning kept |
| T04-A281-8 | meaning kept |
| T04-A319-9 | meaning kept (later removed as a duplicate) |
| T04-A321-6 | meaning kept |
| T05-A078-4 | corrected: Version remark overstates: the source says only that Excel 2016 cannot set the both-direction filter in the data model; its engine does filter both ways through CROSSFILTER. |
| T05-A333-2 | meaning kept |
| T06-A062-5 | meaning kept |
| T06-A062-8 | meaning kept |
| T06-A112-7 | meaning kept |
| T06-A192-3 | meaning kept (later removed as a duplicate) |
| T06-A360-13 | meaning kept |
| T07-A041-2 | meaning kept |
| T07-A127-2 | meaning kept |
| T07-A156-1 | meaning kept |
| T07-A156-3 | meaning kept |
| T07-A156-5 | meaning kept (later removed as a duplicate) |
| T07-A156-6 | meaning kept (later removed as a duplicate) |
| T07-A171-3 | meaning kept |
| T07-A179-5 | corrected: Version names Analysis Services in general; the page says the fix reached Power BI and the Azure service only, while the SQL Server product, 2019 included, has none. |
| T07-A179-6 | meaning kept |
| T07-A260-1 | meaning kept |
| T07-A275-10 | meaning kept |
| T07-A275-11 | meaning kept |
| T07-A275-12 | meaning kept |
| T07-A275-13 | meaning kept |
| T07-A275-2 | meaning kept |
| T07-A275-3 | meaning kept |
| T07-A275-4 | meaning kept |
| T07-A275-6 | meaning kept |
| T07-A275-7 | meaning kept |
| T07-A275-8 | meaning kept |
| T07-A275-9 | meaning kept |
| T07-A350-3 | meaning kept |
| T07-A350-5 | meaning kept |
| T07-A350-7 | meaning kept |
| T08-A059-1 | meaning kept |
| T09-A212-1 | meaning kept |
| T09-A212-2 | meaning kept |
| T09-W380-3 | meaning kept |
| T10-A253-1 | meaning kept |
| T13-A363-5 | meaning kept |
| T13-A364-1 | meaning kept |
| T13-A364-2 | meaning kept |
| T15-A166-4 | meaning kept |
| T15-A206-9 | meaning kept |
| T15-A276-11 | meaning kept |
| T15-A276-6 | meaning kept |
| T15-A308-4 | meaning kept |
| T15-A312-16 | meaning kept |
| T15-A322-17 | meaning kept |
| T15-A328-9 | corrected: Minor: in the reworded list "nobody expected" has unclear scope; "transformations" can read as a bare item and hard-coded values as only the unexpected ones. (later removed as a duplicate) |
| T16-A221-11 | meaning kept |
| T16-A221-12 | meaning kept (later removed as a duplicate) |
| T16-A265-7 | meaning kept |
| T16-A311-12 | meaning kept (later removed as a duplicate) |

## Second round: fixes after an independent review

A fresh read-only session reviewed the pull request. Its findings, and what was done with each:

1. **DAX function index.** The builder now reads Microsoft Learn's sitemap as well as its table of contents. It added 20 functions (ALLSELECTEDAPPLY, ALLSELECTEDREMOVE, ALWAYSAPPLY, COLLAPSE, COLLAPSEALL, DEPENDON, EXPAND, EXPANDALL, FILTERCLUSTER, FIRST, GROUPCROSSAPPLY, GROUPCROSSAPPLYTABLE, ISATLEVEL, LAST, NEXT, NONFILTER, PREVIOUS, SAMPLEAXISWITHLOCALMINMAX, SHADOWCLUSTER, TOPNSKIP) and two statements (Virtual Column, Virtual Table). Three pages that are not functions (the parent-child overview, the relationship functions overview, the table constructor) are no longer counted: 461 functions from the table of contents, 481 in all. The index no longer says that some functions are listed in two groups: none is. Tests in `tests/test_tools.py` keep this on a rebuild.
2. **Out of scope (group 6).** 117 notes whose advice depends on a custom visual, another vendor's tool or another system, or on publishing or deploying, were removed; 3 more duplicates whose kept copy was among them follow it, so group 6 holds 120. In 67 notes such a thing was only a passing mention: the note was kept and the mention dropped.
3. **Clashes with the repository.** Every kept note was swept, one topic per helper, against the checklist, every standard and reference file, the instruction files and the checks; each helper read those files in full first (confirmed from its transcript). 22 notes that clash firmly were removed as not adopted (group 4); 152 notes got a line naming the rule and the condition. Per topic:

| Topic | Notes swept | Removed (group 4) | Condition line added |
|---|---:|---:|---:|
| T01 DAX evaluation context | 156 | 2 | 5 |
| T02 DAX authoring style | 110 | 2 | 5 |
| T03 DAX table functions and queries | 154 | 0 | 13 |
| T04 Time intelligence and date tables | 152 | 3 | 10 |
| T05 Relationships and filter propagation | 67 | 0 | 14 |
| T06 Data model design | 122 | 6 | 11 |
| T07 DAX performance and optimization | 171 | 0 | 8 |
| T08 Storage engine, model size and memory | 31 | 2 | 5 |
| T09 Storage modes | 86 | 0 | 9 |
| T10 Security | 45 | 2 | 10 |
| T11 Calculation groups and field parameters | 85 | 0 | 7 |
| T12 Window functions and visual calculations | 78 | 1 | 4 |
| T13 User-defined functions in DAX | 47 | 0 | 7 |
| T14 Business calculation patterns | 244 | 1 | 20 |
| T15 Report-facing DAX and report design | 254 | 2 | 13 |
| T16 Tooling, workflow and AI assistance | 112 | 1 | 11 |
| **All** | **1914** | **22** | **152** |

Removed in this sweep (group 4):

| Note | Where the repository says otherwise | Reason |
|---|---|---|
| T01-A228-7 | `dax-standard.md`, rule 20 | ALLEXCEPT is used only when the kept column is filtered directly; otherwise the standard asks for REMOVEFILTERS plus VALUES, not a longer ALLEXCEPT list. |
| T01-A124-6 | `storage-and-security.md`, rule 17, check M105 | A dimension attribute that a Power Query merge can supply is not built as a DAX calculated column. |
| T02-A068-4 | `dax-standard.md`, rule 7, check M506 | Blanks stay blank: a measure does not add zero to a result, so the zero case is handled another way. |
| T02-A316-4 | `dax-standard.md`, rule 37 | A speed rewrite is kept only when it returns the same numbers; this one changes totals through rounding. |
| T04-A073-4 | `relationships-and-dates.md`, rule 30, check M402 | A model with time intelligence marks its date table; a workaround in place of the mark is not used. |
| T04-A073-6 | `relationships-and-dates.md`, rule 30, check M402 | A model with time intelligence marks its date table; a dummy table in place of the mark is not used. |
| T04-A073-7 | `relationships-and-dates.md`, rule 30, check M402 | A model with time intelligence marks its date table; rewriting measures in place of the mark is not used. |
| T06-A009-3 | `storage-and-security.md`, rule 17, check M105 | A sortable year-month number is a row value Power Query can supply; it is not built as a DAX calculated column. |
| T06-A062-6 | `storage-and-security.md`, rule 17, checklist item 27 | A calculated column is used only when the formula needs a measure or a DAX-only function; the note treats both forms as equal when size is no concern. |
| T06-A191-3 | `storage-and-security.md`, rule 17, check M105 | A padded unique name built from a rank by code is a value Power Query can supply; it is not built as a DAX calculated column. |
| T06-A192-3 | `storage-and-security.md`, rule 17, check M105 | A unique sort key from column values needs no measure; Power Query or the source supplies it, not a DAX calculated column. |
| T06-A360-5 | `more-model-features.md`, rule 7; storage and security rule 17 | A user-context calculated column is kept for values that depend on the reader; plain row arithmetic comes from Power Query. |
| T06-A360-6 | `native-features.md`, calculated columns row; storage and security rule 17 | A user-context calculated column is kept for values that depend on the reader; plain row arithmetic comes from Power Query. |
| T08-A039-1 | `storage-and-security.md`, rule 17, check M105 | The last process time is not a NOW () calculated column: a value Power Query can supply comes from Power Query. |
| T08-A039-2 | `storage-and-security.md`, rule 17, check M105 | It depends on the NOW () calculated column of T08-A039-1, which the storage standard rules out in favour of Power Query. |
| T10-A090-4 | `copilot-instructions.md`, existing objects keep their names | Existing measures keep their names; the approach renames every original measure. |
| T10-A288-6 | `relationships-and-dates.md`, rule 9, check M106 | A generated key added to the fact table as a calculated column is not how this template builds relationship keys. |
| T12-A196-4 | `dax-standard.md`, rules 21, 20 and 6 | A time variant calls the base measure and never repeats the aggregation; FILTER over ALL of the fact table removes every filter, not only the date. |
| T14-A213-12 | `visual-features.md`, block 16, column widths | A column width is fixed only when the column must not move, not to hide a column. |
| T15-A139-4 | `storage-and-security.md`, rule 17, check M105 | A row value that Power Query can supply comes from Power Query, not a DAX calculated column. |
| T15-A222-7 | `relationships-and-dates.md`, rule 19, check M406 | A table at a higher date grain stores the first date of its period and relates one-to-many to the date table. |
| T16-A221-19 | `native-features.md`, Power BI Project format row, check F001; project instructions | The template works on Power BI project files in TMDL; a Visual Studio Analysis Services project is never the starting point. |

4. **Small corrections.** Strength words: T06-A269-8 is now Must, T06-A269-11 and T08-A107-7 are Facts. Two repeats were removed as already said (group 3): T02-A082-3 (`dax-standard.md` rule 8, checklist item 34) and T04-A217-8 (`model-objects.md`, numeric range parameter). The eight-word check now drops link addresses inside the saved article text (they had broken word runs) and checks each whole note as well as each line; it found three more notes, which were reworded (T03-A046-3, T06-A112-5, T16-A353-5).
5. **White paper notes.** 75 kept notes come from the two white papers, whose pages hold only a summary; the papers sit on a download site the look-up skill does not open. They are marked **Paper**. The skill says what Copilot does with such a note: background only; read a linked article if there is one; otherwise confirm the point on Microsoft Learn, and if that fails, base no change on it and tell the developer.

**Checks after the fixes.** Eight-word check on every library line and every whole note: 0 runs. A fresh reviewer checked every changed note (229) against its article: 225 kept their meaning, 4 were corrected (T02-A178-8, T08-A016-7, T15-A317-9, T16-A221-2). A second fresh reviewer took 10 random notes per topic (160) and looked for clashes still unmarked: 10 condition findings and no firm one, so no topic was swept again; the 10 notes got their condition line. These 14 later changes were checked by the eight-word script but not by a further reviewer.

## Helpers

The comparison and rewriting ran in 24 helpers (one topic, or one part of a large topic, each), followed by one helper for duplicates, three for the source review, the helpers of the repository review and one that proposed candidates for future checks. The second round ran sixteen sweep helpers (one topic each), one source reviewer and one sample reviewer. At most three ran at once, and no two wrote the same file. The model and effort of each are in the pull request, not here: no file of this repository names an AI model.

## Could not be verified

- No note was tried in Power BI Desktop. The library restates what the articles say; whether each statement still holds in today's product was judged only through the earlier currency marks (Check, or no sign of change).
- The comparison with the repository and the judgement "same advice" are readings by helpers. The final repository review looked for misses; it cannot prove there are none.
- The source review covered 240 of the 1892 kept notes. The others were written from the earlier, already checked, long form of each note and were not compared with their articles again in this job.
- GitHub Copilot was not run against the new skill. The five new test prompts in `evals/prompts.md` (E35 to E39) are not tested.
