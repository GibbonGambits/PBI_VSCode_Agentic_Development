# Practice library: working paper

How the practice library (skill `pbi-practice-library`) was built, the decisions made without asking, and what was checked. GitHub Copilot does not read this folder. The work was done on 11 November 2026.

## The job

Put the notes drawn from public SQLBI articles into the template as a reference library: information that Copilot opens when a task calls for it, not rules to enforce. Every note is kept unless one of five removals applies. The kept notes are rewritten short, sorted by topic on two shelves, and listed in one index. `library-removed.md` in this folder holds one row for each removed note, by ID only.

## Where the work stands

Finished. All sixteen topics were compared with the repository, rewritten and rendered; duplicates across topics were removed; the index, the tests, the README, the notices, the sources record, the coverage file and the test prompts are updated; the reviews ran and their findings are dealt with. Nothing is open.

## Numbers

### Counts

| Step | Notes |
|---|---:|
| At the start | 2318 |
| Removed, group 1: outdated | 35 |
| Removed, group 2: conflicts with the checklist | 20 |
| Removed, group 3: the repository already says it | 139 |
| Removed, group 4: not adopted: a higher source says otherwise | 26 |
| Removed, group 5: duplicate of a note kept in another topic | 65 |
| **Kept in the library** | **2033** |

### Kept notes by topic and shelf

| Topic | Files | General practice | Special-case techniques and facts | Total | Marked Check |
|---|---:|---:|---:|---:|---:|
| T01 DAX evaluation context | 2 | 47 | 109 | 156 | 16 |
| T02 DAX authoring style | 2 | 61 | 51 | 112 | 16 |
| T03 DAX table functions and queries | 2 | 46 | 108 | 154 | 38 |
| T04 Time intelligence and date tables | 3 | 40 | 126 | 166 | 56 |
| T05 Relationships and filter propagation | 1 | 19 | 48 | 67 | 13 |
| T06 Data model design | 2 | 51 | 76 | 127 | 17 |
| T07 DAX performance and optimization | 3 | 70 | 110 | 180 | 43 |
| T08 Storage engine, model size and memory | 1 | 10 | 23 | 33 | 4 |
| T09 Storage modes | 2 | 37 | 58 | 95 | 49 |
| T10 Security | 1 | 10 | 35 | 45 | 10 |
| T11 Calculation groups and field parameters | 2 | 23 | 64 | 87 | 17 |
| T12 Window functions and visual calculations | 1 | 33 | 45 | 78 | 9 |
| T13 User-defined functions in DAX | 1 | 28 | 20 | 48 | 4 |
| T14 Business calculation patterns | 5 | 47 | 197 | 244 | 68 |
| T15 Report-facing DAX and report design | 5 | 94 | 196 | 290 | 36 |
| T16 Tooling, workflow and AI assistance | 3 | 68 | 83 | 151 | 32 |
| **All** | **36** | **684** | **1349** | **2033** | **428** |

By strength: Must 331, Should 519, Consider 158, Option 589, Fact 436.

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
| T02-A154-5 | Template rule | `dax-standard.md`, rule 30 | The template names a column that a formula makes with a leading @ (M520 checks it), so a name written in table[column] form cannot be used. |
| T02-A154-6 | Microsoft | `dax-standard.md`, rule 31 (and rule 30) | Variables get plain names with no underscore prefix, following Microsoft Learn, and a column that a formula makes is marked with a leading @, not with a variable name as table prefix. |
| T03-A022-3 | Template rule | `dax-standard.md`, rule 32 | The DAX standard lets SUMMARIZE only group and adds every computed column with ADDCOLUMNS (M522); the note keeps computed columns inside SUMMARIZE in two cases. |
| T03-A094-9 | Microsoft | `dax-standard.md`, rule 4 | The DAX standard reads one selected value with SELECTEDVALUE and warns (M504) on IF with HASONEVALUE and VALUES, the form this rule requires. |
| T03-A106-4 | Template rule | `dax-standard.md`, rule 30 | The DAX standard starts the name of a column made by SELECTCOLUMNS or ADDCOLUMNS with @ (M520), not with a table prefix. |
| T03-A129-2 | Template rule | `model-standard.md`, rule 1 | The model standard keeps every measure in the one visible table _Measures (M001, M002); this recipe hosts its helper measures in a separate hidden calculated table. |
| T03-A341-2 | Microsoft | `dax-standard.md`, rule 32; Where sources disagree (SUMMARIZECOLUMNS inside a measure) | The DAX standard records that Microsoft's skill uses SUMMARIZECOLUMNS by default for grouping with values, also inside a measure, and that this wins over keeping it for advanced cases. |
| T04-A199-6 | Microsoft | `relationships-and-dates.md`, rule 30 | The template requires a marked date table wherever time intelligence is used (M402 fails otherwise), as Microsoft Learn and Microsoft's best practice rule ask; clearing filters in each measure does not replace the mark. |
| T05-A158-6 | Template rule | `model-standard.md`, rule 1 | The model standard keeps every measure in the one visible table _Measures (M001, M002); a separate hidden table for slicer helper measures breaks that rule. |
| T06-A035-3 | Microsoft | `relationships-and-dates.md`, rule 17 | The standard says a fact key with no match in its dimension is put right at the source; the note leaves such keys unmatched on purpose. |
| T06-A062-11 | Microsoft | `dax-standard.md`, section B, SQLBI rules the template does not check | Measures are written in TMDL, which always uses the form measure 'Name' =, so the standard records that the := form does not apply. |
| T06-A075-18 | Microsoft | `relationships-and-dates.md`, rule 30 | The standard requires a marked date table wherever time intelligence is used, whatever the key type (M402 fails otherwise); it does not accept that a date-typed key makes the mark unnecessary. |
| T06-A224-2 | Microsoft | `relationships-and-dates.md`, rule 27 | The standard, following Microsoft's best practice rule, prefers whole-number relationship keys, date keys included (M110 warns on a date key), and the shipped example relates facts to the date table on a whole-number key. |
| T07-W378-16 | Microsoft | `relationships-and-dates.md`, rule 1 | The standard, following Microsoft's star schema guidance, never mixes the job of a fact table and of a dimension in one table; the note weighs folding a dimension into the fact table. |
| T07-A061-5 | Microsoft | `relationships-and-dates.md`, rule 1 | The standard, following Microsoft's star schema guidance, keeps descriptive columns in dimension tables; the note weighs merging a large dimension into the table on the many side. |
| T09-W380-15 | Template rule | `model-standard.md`, rule 1 | For Power BI today the template gives a DirectQuery model a calculated _Measures table, so calculated tables do exist there; the limit belongs to Analysis Services 2016 only. |
| T09-A237-3 | Microsoft | `storage-and-security.md`, rule 23 | The repository, following Microsoft on composite models, says a calculated column or calculated table cannot depend on a chained (remote) model; this recipe is built on a calculated column of a remote table. |
| T09-A237-4 | Microsoft | `storage-and-security.md`, rule 23 | It describes a relationship on a calculated column of a remote table; the repository, following Microsoft, says a calculated column cannot depend on a chained (remote) model. |
| T10-A279-9 | Template rule | `report-standard.md`, rule 36 | The report standard sets no colour on a single visual and lets conditional formatting use theme colours only (V009); making a visual transparent by formatting breaks that rule. |
| T10-A282-3 | Microsoft | `storage-and-security.md`, rule 32 | Microsoft's best practice rule says not to put a role's filter on a table with a many-to-many relationship (M604); the note builds its role on exactly that. |
| T10-A297-6 | Microsoft | `storage-and-security.md`, rule 29 | The security standard, following Microsoft's guidance, puts a role's filter on a dimension table and lets the relationship carry it; a rule on a fact table is listed as a common mistake (M602). |
| T14-A019-5 | Template rule | `model-standard.md`, rule 7 | The model standard keeps a column that a hierarchy level uses visible (M104 warns on a hidden one); this recipe builds the hierarchy on copies of the columns and hides those copies. |
| T15-A072-2 | Template rule | `model-standard.md`, rule 3 | Measure names follow the model standard's naming rules (M007, M008), not the wording of one report's labels; a visual can show its own label. |
| T15-A317-13 | Template rule | `model-standard.md`, rule 1 | The model standard keeps every measure in the one visible table _Measures (M001, M002), so SVG measures get no table of their own to mark private. |

### Group 3 by covering file

| File | Notes |
|---|---:|
| `.github/skills/pbi-semantic-model/references/dax-standard.md` | 49 |
| `.github/skills/pbi-semantic-model/references/relationships-and-dates.md` | 34 |
| `.github/skills/pbi-semantic-model/references/storage-and-security.md` | 15 |
| `.github/skills/pbi-semantic-model/references/model-objects.md` | 14 |
| `checklist/checklist.md` | 10 |
| `.github/skills/pbi-semantic-model/references/model-standard.md` | 5 |
| `.github/skills/pbi-report/references/report-standard.md` | 5 |
| `.github/skills/pbi-checklist-review/references/native-features.md` | 3 |
| `.github/skills/pbi-semantic-model/SKILL.md` | 2 |
| `.github/skills/pbi-semantic-model/references/more-model-features.md` | 1 |
| `.github/skills/pbi-report/references/theme.md` | 1 |

Kept notes that hold only the detail the repository lacked: 662 of 2033.

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
10. **A note that names a tool or a custom visual outside this template** (for example DAX Studio or Tabular Editor) is kept as information for the developer. The skill says that Copilot never installs, calls or suggests such a tool by itself.
11. **A version line may carry this template's own record** (for example that Microsoft now lists push semantic models as retiring, from `feature-inventory.md`). The rest of a note comes from its article only.
12. **Where a note mentions an older view** that came from an older article, the older article's address stands on the note's source line beside the newer one.
13. **One more checklist conflict was found in this job:** T15-A325-17 (one data visual laid over another) against checklist item 49, which allows 0 overlapping visuals. That makes 20 in group 2, not 19.
14. **Duplicates across topics.** The 219 earlier pairs were judged again on the shortened notes: a pair counts as a duplicate only when a reader who has one note gains nothing from the other. Four further duplicates were found by reading the whole list. Duplicates inside one topic were not looked for again: the earlier work had already merged those.
15. **The look-up skill gained a fifth case** (confirming a note marked Check, or reading the article behind a note). Without it the two skills would have said different things.

## A finding for the owner: the DAX function index misses functions

`.github/skills/pbi-semantic-model/references/dax-functions.md` says that a function it does not list is not a DAX function Microsoft documents. Microsoft Learn does have pages for TOPNSKIP, PREVIOUS, NEXT, FIRST, LAST, EXPAND, EXPANDALL, COLLAPSE, COLLAPSEALL and ISATLEVEL (opened on 11 November 2026), and its table of contents also names HIGHESTPARENT, LOWESTPARENT and SAMPLEAXISWITHLOCALMINMAX (not opened). The index is built from the function groups of the table of contents, and these functions are not placed in a group there. The index was not changed in this job. Notes that name one of these functions were kept, each with a version line saying that the function is missing from the index and that DAX standard rule 19 applies until the index lists it.

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
| T04-A121-14 | meaning kept |
| T04-A264-3 | meaning kept |
| T04-A281-10 | meaning kept |
| T04-A281-8 | meaning kept |
| T04-A319-9 | meaning kept |
| T04-A321-6 | meaning kept |
| T05-A078-4 | corrected: Version remark overstates: the source says only that Excel 2016 cannot set the both-direction filter in the data model; its engine does filter both ways through CROSSFILTER. |
| T05-A333-2 | meaning kept |
| T06-A062-5 | meaning kept |
| T06-A062-8 | meaning kept |
| T06-A112-7 | meaning kept |
| T06-A192-3 | meaning kept |
| T06-A360-13 | meaning kept |
| T07-A041-2 | meaning kept |
| T07-A127-2 | meaning kept |
| T07-A156-1 | meaning kept |
| T07-A156-3 | meaning kept |
| T07-A156-5 | meaning kept |
| T07-A156-6 | meaning kept |
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
| T15-A328-9 | corrected: Minor: in the reworded list "nobody expected" has unclear scope; "transformations" can read as a bare item and hard-coded values as only the unexpected ones. |
| T16-A221-11 | meaning kept |
| T16-A221-12 | meaning kept |
| T16-A265-7 | meaning kept |
| T16-A311-12 | meaning kept |

## Helpers

The comparison and rewriting ran in 24 helpers (one topic, or one part of a large topic, each), followed by one helper for duplicates, three for the source review, the helpers of the repository review and one that proposed candidates for future checks. At most three ran at once, and no two wrote the same file. The model and effort of each are in the pull request, not here: no file of this repository names an AI model.

## Could not be verified

- No note was tried in Power BI Desktop. The library restates what the articles say; whether each statement still holds in today's product was judged only through the earlier currency marks (Check, or no sign of change).
- The comparison with the repository and the judgement "same advice" are readings by helpers. The final repository review looked for misses; it cannot prove there are none.
- The source review covered 258 of the 2033 kept notes. The others were written from the earlier, already checked, long form of each note and were not compared with their articles again in this job.
- GitHub Copilot was not run against the new skill. The four new test prompts in `evals/prompts.md` are not tested.
