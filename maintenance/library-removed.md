# Practice library: notes that were removed

One row for each note that did not go into the practice library (skill `pbi-practice-library`), by ID only. GitHub Copilot does not read this folder.

The library started from 2,318 notes drawn from public SQLBI articles. Notes were removed in six groups, in this order:

1. Outdated: the advice no longer holds in current Power BI.
2. Conflicts with the owner's checklist. The checklist wins.
3. The repository already says it, at the same level of detail or deeper. The file that says it is named.
4. Not adopted: it cannot be followed together with guidance in the repository that rests on a higher source (Microsoft, or a rule of this template). The file that holds that guidance is named; the reasons are in `library.md` in this folder.
5. Duplicate of a note kept in another topic. The library file that holds the kept copy is named.
6. Out of scope: the advice depends on a custom visual, another vendor's tool or another system, or on publishing or deploying, which this template leaves out. The rule that leaves it out is named. A duplicate whose kept copy was removed in group 3, 4 or 6 is counted in that group.

| Group | Removed |
|---|---:|
| 1. Outdated | 35 |
| 2. Conflicts with the checklist | 20 |
| 3. The repository already says it | 141 |
| 4. Not adopted: a higher source says otherwise | 32 |
| 5. Duplicate of a note kept in another topic | 62 |
| 6. Out of scope: depends on a custom visual, another vendor's tool or another system, or on publishing or deploying | 120 |
| Kept in the library | 1908 |

| Note | Group | Covered by |
|---|---|---|
| T01-A020-4 | 4 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 8 |
| T01-A064-7 | 4 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 21 |
| T01-A064-8 | 5 | `.github/skills/pbi-practice-library/references/t02-dax-authoring-style-1.md`, kept copy: T02-A054-2 |
| T01-A074-1 | 1 | - |
| T01-A074-8 | 1 | - |
| T01-A228-3 | 2 | `checklist/checklist.md`, item 12 |
| T01-A314-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 6 |
| T01-A105-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 4 |
| T01-A105-3 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 4 |
| T01-A105-7 | 3 | `.github/skills/pbi-semantic-model/references/model-objects.md`, section D, Numeric range parameter |
| T01-A118-5 | 5 | `.github/skills/pbi-practice-library/references/t04-time-intelligence-and-dates-1.md`, kept copy: T04-A024-1 |
| T01-A120-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 34 |
| T01-A120-4 | 3 | `checklist/checklist.md`, Item 34 |
| T01-A085-5 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 20 |
| T01-A124-4 | 5 | `.github/skills/pbi-practice-library/references/t05-relationships-1.md`, kept copy: T05-A036-1 |
| T01-A124-5 | 5 | `.github/skills/pbi-practice-library/references/t05-relationships-1.md`, kept copy: T05-A036-2 |
| T01-A135-2 | 5 | `.github/skills/pbi-practice-library/references/t06-data-model-design-1.md`, kept copy: T06-A173-5 |
| T01-A135-3 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 1 |
| T01-A220-4 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 6 |
| T01-A245-2 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 18 |
| T01-A254-5 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 34 |
| T01-A338-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 34 |
| T01-A361-6 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 20 |
| T01-A259-3 | 5 | `.github/skills/pbi-practice-library/references/t14-business-calculation-patterns-1.md`, kept copy: T14-A186-2 |
| T01-A263-6 | 5 | `.github/skills/pbi-practice-library/references/t04-time-intelligence-and-dates-1.md`, kept copy: T04-A202-2 |
| T01-A305-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 6 |
| T01-A305-3 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 6 |
| T01-A309-4 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 6 |
| T01-A361-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 20 |
| T01-A338-2 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 34 |
| T01-A336-5 | 5 | `.github/skills/pbi-practice-library/references/t02-dax-authoring-style-1.md`, kept copy: T02-A335-1 |
| T01-A361-2 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 20 |
| T01-A361-7 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 34 |
| T02-A025-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, section B, rule 27 |
| T02-A025-20 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T02-A054-3 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 9 |
| T02-A054-4 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 8 |
| T02-A068-4 | 4 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 7, check M506 |
| T02-A082-3 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 8; checklist item 34 |
| T02-A082-4 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 8 and rule 31 |
| T02-A116-7 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 8 and rule 31 |
| T02-A096-5 | 1 | - |
| T02-A096-6 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-1.md`, kept copy: T01-A220-1 |
| T02-A100-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 10 |
| T02-A100-2 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 10 |
| T02-A100-4 | 3 | `.github/skills/pbi-semantic-model/references/model-standard.md`, rule 3 (M005) |
| T02-A100-5 | 3 | `.github/skills/pbi-semantic-model/references/model-standard.md`, rule 3 (M006) |
| T02-A100-6 | 3 | `.github/skills/pbi-semantic-model/references/model-standard.md`, rule 3 |
| T02-A100-7 | 3 | `checklist/checklist.md`, Item 7 |
| T02-A100-8 | 5 | `.github/skills/pbi-practice-library/references/t06-data-model-design-1.md`, kept copy: T06-A075-9 |
| T02-A116-3 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 15 |
| T02-A143-1 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-1.md`, kept copy: T01-A310-1 |
| T02-A143-2 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-1.md`, kept copy: T01-A244-2 |
| T02-A143-4 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-2.md`, kept copy: T01-A249-1 |
| T02-A154-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 8 |
| T02-A154-5 | 4 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 30 |
| T02-A154-6 | 4 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 31 (and rule 30) |
| T02-A169-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 10 |
| T02-A169-3 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 30 |
| T02-A185-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 7 |
| T02-A185-2 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 7 |
| T02-A255-8 | 5 | `.github/skills/pbi-practice-library/references/t16-tooling-and-workflow-1.md`, kept copy: T16-A353-1 |
| T02-A335-2 | 5 | `.github/skills/pbi-practice-library/references/t05-relationships-1.md`, kept copy: T05-A165-2 |
| T03-A012-4 | 1 | - |
| T03-A022-1 | 1 | - |
| T03-A022-2 | 1 | - |
| T03-A022-3 | 4 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 32 |
| T03-A045-3 | 2 | `checklist/checklist.md`, item 32 |
| T03-A053-1 | 5 | `.github/skills/pbi-practice-library/references/t02-dax-authoring-style-2.md`, kept copy: T02-A242-1 |
| T03-A053-3 | 5 | `.github/skills/pbi-practice-library/references/t07-dax-performance-1.md`, kept copy: T07-A041-1 |
| T03-A053-6 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 37 |
| T03-A070-3 | 1 | - |
| T03-A071-10 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 32 |
| T03-A094-11 | 1 | - |
| T03-A094-9 | 4 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 4 |
| T03-A283-3 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 32 |
| T03-A098-6 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 14 |
| T03-A106-3 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 10 |
| T03-A106-4 | 4 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 30 |
| T03-A109-4 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-1.md`, kept copy: T01-A105-4 |
| T03-A115-2 | 1 | - |
| T03-A115-8 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T03-A129-2 | 4 | `.github/skills/pbi-semantic-model/references/model-standard.md`, rule 1 |
| T03-A198-2 | 1 | - |
| T03-A214-1 | 1 | - |
| T03-A215-1 | 1 | - |
| T03-A215-2 | 1 | - |
| T03-A215-3 | 1 | - |
| T03-A215-4 | 1 | - |
| T03-A215-5 | 1 | - |
| T03-A048-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 32 |
| T03-A226-2 | 5 | `.github/skills/pbi-practice-library/references/t05-relationships-1.md`, kept copy: T05-A182-1 |
| T03-A226-3 | 5 | `.github/skills/pbi-practice-library/references/t05-relationships-1.md`, kept copy: T05-A080-4 |
| T03-A291-8 | 2 | `checklist/checklist.md`, item 14 |
| T03-A341-10 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 33 |
| T03-A341-2 | 4 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 32; Where sources disagree (SUMMARIZECOLUMNS inside a measure) |
| T04-A121-11 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T04-A121-12 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T04-A121-13 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T04-A121-14 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T04-A121-4 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T04-A152-1 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 29 |
| T04-A147-2 | 5 | `.github/skills/pbi-practice-library/references/t14-business-calculation-patterns-5.md`, kept copy: T14-A252-3 |
| T04-A153-1 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 32 |
| T04-A153-2 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rules 30 and 31 |
| T04-A199-1 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 30 |
| T04-A152-4 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 29 |
| T04-A175-1 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 35 |
| T04-A199-6 | 4 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 30 |
| T04-A204-11 | 5 | `.github/skills/pbi-practice-library/references/t15-report-facing-dax-2.md`, kept copy: T15-A139-3 |
| T04-A204-4 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 35 |
| T04-A043-4 | 1 | - |
| T04-A217-8 | 3 | `.github/skills/pbi-semantic-model/references/model-objects.md`, numeric range parameter |
| T04-A264-1 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T04-A264-2 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T04-A264-3 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T04-A264-4 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T04-A264-5 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T04-A264-6 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T04-A319-2 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 30 |
| T04-A319-4 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T04-A319-9 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T04-A321-12 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-1.md`, kept copy: T01-A336-1 |
| T04-A321-3 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 31 |
| T04-A321-5 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 7 |
| T04-A371-1 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rules 29 and 30 |
| T05-A078-3 | 2 | `checklist/checklist.md`, item 12 |
| T05-A080-2 | 1 | - |
| T05-A099-2 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-2.md`, kept copy: T01-A122-5 |
| T05-A141-2 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 17 and rule 18 |
| T05-A141-3 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 18 |
| T05-A158-1 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 18 |
| T05-A158-2 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 18 (check M405) |
| T05-A158-6 | 4 | `.github/skills/pbi-semantic-model/references/model-standard.md`, rule 1 |
| T05-A165-3 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-1.md`, kept copy: T01-A336-1 |
| T05-A182-12 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T05-A182-6 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 19 |
| T05-A182-9 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 20 (check M407) |
| T05-A194-1 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 7 |
| T05-A095-3 | 2 | `checklist/checklist.md`, item 14 |
| T05-A095-4 | 2 | `checklist/checklist.md`, item 14 |
| T05-A036-3 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-1.md`, kept copy: T01-A124-1 |
| T05-A236-2 | 2 | `checklist/checklist.md`, item 12 |
| T05-A236-6 | 5 | `.github/skills/pbi-practice-library/references/t07-dax-performance-2.md`, kept copy: T07-A350-6 |
| T05-A258-1 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 7 |
| T05-A267-3 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 17 |
| T05-A333-4 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-1.md`, kept copy: T01-A047-4 |
| T06-A009-1 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 35 |
| T06-A035-1 | 5 | `.github/skills/pbi-practice-library/references/t04-time-intelligence-and-dates-2.md`, kept copy: T04-A321-1 |
| T06-A035-3 | 4 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 17 |
| T06-A035-4 | 2 | `checklist/checklist.md`, item 31 |
| T06-A062-11 | 4 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, section B, SQLBI rules the template does not check |
| T06-A062-6 | 4 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 17, checklist item 27 |
| T06-A062-9 | 3 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 17 |
| T06-A075-10 | 5 | `.github/skills/pbi-practice-library/references/t02-dax-authoring-style-2.md`, kept copy: T02-A100-11 |
| T06-A075-13 | 3 | `checklist/checklist.md`, Item 29 |
| T06-A075-14 | 3 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 13 |
| T06-A075-15 | 3 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 18 |
| T06-A075-16 | 3 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 20 |
| T06-A075-17 | 5 | `.github/skills/pbi-practice-library/references/t04-time-intelligence-and-dates-1.md`, kept copy: T04-A199-3 |
| T06-A075-18 | 4 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 30 |
| T06-A075-3 | 3 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 5 (and rule 2) |
| T06-A130-1 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rules 1 to 3 |
| T06-A173-2 | 2 | `checklist/checklist.md`, item 25 |
| T06-A173-3 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 1 |
| T06-A218-1 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 1 |
| T06-A224-2 | 4 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 27 |
| T06-A233-3 | 5 | `.github/skills/pbi-practice-library/references/t07-dax-performance-2.md`, kept copy: T07-A350-5 |
| T06-A290-1 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T06-A290-10 | 2 | `checklist/checklist.md`, item 38 |
| T06-A290-2 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T06-A290-3 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T06-A290-5 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T06-A290-6 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T06-A290-8 | 5 | `.github/skills/pbi-practice-library/references/t02-dax-authoring-style-1.md`, kept copy: T02-A178-1 |
| T06-A360-6 | 4 | `.github/skills/pbi-checklist-review/references/native-features.md`, calculated columns row; storage and security rule 17 |
| T06-A368-5 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-2.md`, kept copy: T01-A259-5 |
| T07-W378-16 | 4 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 1 |
| T07-W378-27 | 1 | - |
| T07-W378-40 | 1 | - |
| T07-W378-43 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T07-W378-9 | 5 | `.github/skills/pbi-practice-library/references/t08-storage-engine-and-model-size-1.md`, kept copy: T08-A030-9 |
| T07-A044-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 2 |
| T07-A044-4 | 2 | `checklist/checklist.md`, item 33 |
| T07-A061-1 | 5 | `.github/skills/pbi-practice-library/references/t05-relationships-1.md`, kept copy: T05-A080-1 |
| T07-A061-5 | 4 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 1 |
| T07-A119-3 | 3 | `checklist/checklist.md`, Item 34 |
| T07-A127-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 8 |
| T07-A128-2 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 37 |
| T07-A334-4 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 37 |
| T07-A156-2 | 2 | `checklist/checklist.md`, item 68 |
| T07-A156-5 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T07-A156-6 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T07-A157-1 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T07-A157-2 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T07-A157-3 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T07-A179-2 | 1 | - |
| T07-A181-7 | 5 | `.github/skills/pbi-practice-library/references/t14-business-calculation-patterns-3.md`, kept copy: T14-A052-2 |
| T07-A235-1 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T07-A251-4 | 5 | `.github/skills/pbi-practice-library/references/t06-data-model-design-2.md`, kept copy: T06-A269-9 |
| T07-A272-3 | 3 | `.github/skills/pbi-semantic-model/references/model-objects.md`, section C rule 1 (note U003) |
| T07-A287-7 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 32 |
| T07-A334-2 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-2.md`, kept copy: T01-A259-5 |
| T07-A350-1 | 3 | `checklist/checklist.md`, Item 11 |
| T07-A372-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 37 |
| T07-A372-11 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T07-A372-5 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T08-A016-1 | 3 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 20 |
| T08-A016-12 | 5 | `.github/skills/pbi-practice-library/references/t06-data-model-design-1.md`, kept copy: T06-A005-4 |
| T08-A016-6 | 3 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 18 |
| T08-A030-1 | 3 | `checklist/checklist.md`, Item 5 |
| T08-A030-3 | 5 | `.github/skills/pbi-practice-library/references/t06-data-model-design-2.md`, kept copy: T06-A112-2 |
| T08-A030-8 | 3 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 18 |
| T08-A039-1 | 4 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 17, check M105 |
| T08-A059-2 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T08-A107-4 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T08-A108-3 | 5 | `.github/skills/pbi-practice-library/references/t06-data-model-design-1.md`, kept copy: T06-A172-9 |
| T09-A087-1 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T09-A087-2 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T09-A087-3 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T09-A087-4 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T09-A087-5 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T09-W380-1 | 3 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 22 |
| T09-W380-12 | 3 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 3 (M701) |
| T09-W380-13 | 5 | `.github/skills/pbi-practice-library/references/t06-data-model-design-1.md`, kept copy: T06-A075-1 |
| T09-W380-14 | 3 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 24 |
| T09-W380-15 | 4 | `.github/skills/pbi-semantic-model/references/model-standard.md`, rule 1 |
| T09-W380-2 | 2 | `checklist/checklist.md`, item 68 |
| T09-W380-32 | 1 | - |
| T09-W380-34 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T09-W380-36 | 3 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 24 |
| T09-A227-1 | 1 | - |
| T09-A227-12 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T09-A227-5 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T09-A234-2 | 1 | - |
| T09-A234-5 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T09-A237-3 | 4 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 23 |
| T09-A237-4 | 4 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 23 |
| T09-A238-2 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-2.md`, kept copy: T01-A249-3 |
| T09-A295-1 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 17 |
| T10-A090-3 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 18 |
| T10-A090-4 | 4 | `.github/copilot-instructions.md`, existing objects keep their names |
| T10-A279-9 | 4 | `.github/skills/pbi-report/references/report-standard.md`, rule 36 |
| T10-A282-3 | 4 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 32 |
| T10-A288-5 | 3 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 38 |
| T10-A288-6 | 4 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 9, check M106 |
| T10-A297-6 | 4 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 29 |
| T11-A159-2 | 3 | `.github/skills/pbi-semantic-model/references/model-objects.md`, section B, rule 5 (M813) |
| T11-A160-3 | 3 | `.github/skills/pbi-semantic-model/references/model-objects.md`, section B, rules 1 and 5 |
| T11-A184-3 | 5 | `.github/skills/pbi-practice-library/references/t14-business-calculation-patterns-1.md`, kept copy: T14-A183-9 |
| T11-A210-1 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 7 |
| T11-A210-2 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 7 |
| T11-A240-1 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T11-A240-2 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T11-A248-1 | 3 | `.github/skills/pbi-report/references/report-standard.md`, rules 2 to 5 |
| T11-A248-2 | 3 | `.github/skills/pbi-semantic-model/references/model-objects.md`, section C, rule 3 |
| T11-A248-6 | 3 | `.github/skills/pbi-semantic-model/references/model-objects.md`, section C, rule 2 |
| T11-A268-2 | 2 | `checklist/checklist.md`, item 12 |
| T11-A280-6 | 5 | `.github/skills/pbi-practice-library/references/t05-relationships-1.md`, kept copy: T05-A158-4 |
| T11-A332-1 | 3 | `.github/skills/pbi-semantic-model/references/model-objects.md`, section B, rule 6 |
| T11-A332-5 | 3 | `.github/skills/pbi-semantic-model/references/more-model-features.md`, rule 13 |
| T11-A340-3 | 3 | `.github/skills/pbi-semantic-model/references/model-objects.md`, section A, rules 2, 3 and 7 |
| T11-A340-4 | 3 | `.github/skills/pbi-semantic-model/references/model-objects.md`, section B, rule 6 |
| T12-A266-3 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 11 |
| T13-A344-3 | 3 | `.github/skills/pbi-semantic-model/references/model-objects.md`, section A, rule 5 |
| T13-A344-6 | 3 | `.github/skills/pbi-semantic-model/references/model-objects.md`, section A, rule 5 |
| T13-A347-8 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T14-A015-1 | 1 | - |
| T14-A015-3 | 2 | `checklist/checklist.md`, item 14 |
| T14-A015-5 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 19 |
| T14-A019-5 | 4 | `.github/skills/pbi-semantic-model/references/model-standard.md`, rule 7 |
| T14-A034-2 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 35 |
| T14-A149-4 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 31 |
| T14-A149-6 | 1 | - |
| T14-A052-3 | 1 | - |
| T14-A066-3 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 32 |
| T14-A086-5 | 1 | - |
| T14-A088-1 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 7 |
| T14-A088-2 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rule 7 |
| T14-A088-7 | 3 | `.github/skills/pbi-semantic-model/references/model-standard.md`, rule 7 |
| T14-A136-2 | 1 | - |
| T14-A150-2 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-1.md`, kept copy: T01-A002-2 |
| T14-A183-7 | 3 | `.github/skills/pbi-checklist-review/references/native-features.md`, The list, Model: row "Calculation groups" |
| T14-A186-1 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-2.md`, kept copy: T01-A259-5 |
| T14-A213-5 | 5 | `.github/skills/pbi-practice-library/references/t06-data-model-design-2.md`, kept copy: T06-A013-6 |
| T14-A252-8 | 3 | `.github/skills/pbi-report/references/report-standard.md`, rule 65 |
| T14-A257-4 | 5 | `.github/skills/pbi-practice-library/references/t12-window-functions-and-visual-calculations-1.md`, kept copy: T12-A348-4 |
| T14-A304-3 | 3 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 17 |
| T14-A323-10 | 2 | `checklist/checklist.md`, item 35 |
| T14-A323-11 | 5 | `.github/skills/pbi-practice-library/references/t02-dax-authoring-style-1.md`, kept copy: T02-A178-1 |
| T14-A323-12 | 5 | `.github/skills/pbi-practice-library/references/t06-data-model-design-2.md`, kept copy: T06-A290-4 |
| T14-A323-9 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 35 |
| T14-A326-7 | 2 | `checklist/checklist.md`, item 38 |
| T14-A346-10 | 5 | `.github/skills/pbi-practice-library/references/t13-user-defined-functions-1.md`, kept copy: T13-A358-4 |
| T14-A346-3 | 5 | `.github/skills/pbi-practice-library/references/t03-table-functions-and-queries-1.md`, kept copy: T03-A283-5 |
| T14-A346-9 | 3 | `.github/skills/pbi-semantic-model/references/model-objects.md`, section A, rules 2, 3 and 5 |
| T14-A349-4 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 6 |
| T14-A369-10 | 5 | `.github/skills/pbi-practice-library/references/t10-security-1.md`, kept copy: T10-A288-1 |
| T14-A369-14 | 5 | `.github/skills/pbi-practice-library/references/t16-tooling-and-workflow-2.md`, kept copy: T16-A367-4 |
| T15-A072-2 | 4 | `.github/skills/pbi-semantic-model/references/model-standard.md`, rule 3 |
| T15-A072-4 | 3 | `.github/skills/pbi-semantic-model/references/storage-and-security.md`, rule 8 |
| T15-A125-5 | 5 | `.github/skills/pbi-practice-library/references/t01-evaluation-context-1.md`, kept copy: T01-A250-3 |
| T15-A145-1 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A145-8 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A145-9 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A166-2 | 2 | `checklist/checklist.md`, item 14 |
| T15-A166-5 | 2 | `checklist/checklist.md`, item 12 |
| T15-A166-6 | 3 | `.github/skills/pbi-semantic-model/references/model-standard.md`, rule 7 |
| T15-A188-5 | 5 | `.github/skills/pbi-practice-library/references/t14-business-calculation-patterns-4.md`, kept copy: T14-A257-3 |
| T15-A189-2 | 1 | - |
| T15-A231-13 | 5 | `.github/skills/pbi-practice-library/references/t03-table-functions-and-queries-1.md`, kept copy: T03-A129-1 |
| T15-A231-14 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A231-4 | 1 | - |
| T15-A276-2 | 3 | `.github/skills/pbi-semantic-model/references/model-objects.md`, section D, Dynamic format string |
| T15-A317-13 | 4 | `.github/skills/pbi-semantic-model/references/model-standard.md`, rule 1 |
| T15-A317-14 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A317-2 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A317-3 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A317-4 | 3 | `.github/skills/pbi-report/references/report-standard.md`, rule 44 (checklist item 54) |
| T15-A317-6 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A317-7 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-2 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A318-10 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A318-11 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A318-13 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A318-14 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A318-18 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A318-20 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A318-9 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-14 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A322-1 | 3 | `checklist/checklist.md`, Item 50 |
| T15-A322-16 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T15-A322-2 | 3 | `.github/skills/pbi-report/references/theme.md`, section The theme, third paragraph (V009) |
| T15-A322-8 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A325-15 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A325-17 | 2 | `checklist/checklist.md`, Item 49 |
| T15-A325-19 | 3 | `.github/skills/pbi-report/references/report-standard.md`, rule 44 |
| T15-A325-21 | 3 | `.github/skills/pbi-semantic-model/references/relationships-and-dates.md`, rules 17 to 19 |
| T15-A325-3 | 3 | `.github/skills/pbi-report/references/report-standard.md`, rule 44 (checklist item 54) |
| T15-A328-12 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-13 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-16 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-17 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-18 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-19 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-21 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-22 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-23 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-24 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-3 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-4 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-7 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-8 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A328-9 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T15-A351-12 | 5 | `.github/skills/pbi-practice-library/references/t02-dax-authoring-style-1.md`, kept copy: T02-A178-1 |
| T15-A351-3 | 1 | - |
| T15-A362-12 | 5 | `.github/skills/pbi-practice-library/references/t12-window-functions-and-visual-calculations-1.md`, kept copy: T12-A357-1 |
| T16-A049-1 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A050-1 | 5 | `.github/skills/pbi-practice-library/references/t06-data-model-design-1.md`, kept copy: T06-A075-5 |
| T16-A081-1 | 3 | `.github/skills/pbi-semantic-model/references/model-objects.md`, section D, "Translations and cultures" |
| T16-A081-2 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A081-9 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A084-1 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T16-A084-2 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T16-A084-3 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T16-A084-4 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T16-A084-6 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T16-A084-7 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T16-A084-8 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T16-A084-9 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T16-A110-2 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A123-10 | 3 | `checklist/checklist.md`, Item 68 |
| T16-A123-2 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A123-3 | 3 | `checklist/checklist.md`, Item 68 |
| T16-A123-4 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A123-5 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A123-6 | 3 | `.github/skills/pbi-semantic-model/references/dax-standard.md`, rule 6 (M505) |
| T16-A200-3 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A200-4 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A205-1 | 1 | - |
| T16-A221-10 | 1 | - |
| T16-A221-12 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A221-13 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A221-14 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A221-16 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A221-17 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T16-A221-3 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A221-4 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A221-5 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A221-6 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T16-A221-7 | 1 | - |
| T16-A221-8 | 3 | `.github/skills/pbi-semantic-model/SKILL.md`, section "Before you change anything", step 2 |
| T16-A221-9 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A265-10 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A265-11 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A265-12 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A265-3 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A265-6 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A311-12 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T16-A311-13 | 6 | `.github/copilot-instructions.md`, no publishing, deploying or connecting to a workspace |
| T16-A311-4 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A311-5 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A331-1 | 3 | `.github/skills/pbi-checklist-review/references/native-features.md`, table "Tooling Copilot can use", row "Power BI Project format" |
| T16-A331-2 | 3 | `checklist/checklist.md`, Item 50 |
| T16-A331-4 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A331-6 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A339-1 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A343-1 | 3 | `.github/skills/pbi-checklist-review/references/native-features.md`, section "Tooling Copilot can use", row "Power BI Project format" (F001) |
| T16-A353-10 | 6 | `.github/skills/pbi-checklist-review/references/native-features.md`, rule 6: no custom visual or other vendor's tool |
| T16-A366-1 | 3 | `.github/skills/pbi-semantic-model/SKILL.md`, section "What the files cannot tell", third point (whether the model loads and the numbers are right) |
