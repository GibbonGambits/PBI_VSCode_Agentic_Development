# Practice library: working paper

How the practice library (skill `pbi-practice-library`) was built, the decisions made without asking, and where the work stands. GitHub Copilot does not read this folder.

## The job

Put the notes drawn from public SQLBI articles into the template as a reference library: information that Copilot opens when a task calls for it, not rules to enforce. Every note is kept unless one of five removals applies; the kept notes are rewritten short, sorted by topic, and listed in one index. `library-removed.md` in this folder holds one row for each removed note.

## Where the work stands

Updated at every commit, so that a stop loses nothing.

| Topic | State |
|---|---|
| T02 DAX authoring style | Compared with the repository, rewritten, rendered |
| T03 DAX table functions and queries | Compared with the repository, rewritten, rendered |
| T05 Relationships and filter propagation | Compared with the repository, rewritten, rendered |
| T01 DAX evaluation context | Compared with the repository, rewritten, rendered |
| T04 Time intelligence and date tables | Compared with the repository, rewritten, rendered |
| T06 Data model design | Compared with the repository, rewritten, rendered |
| T08 Storage engine, model size and memory | Compared with the repository, rewritten, rendered |
| The other nine topics | Not yet done |
| Duplicates across topics | Not yet done |
| Index, tests, README, notices, evals | Index started; the rest not yet done |
| Two read-only reviews | Not yet done |

## Decisions

1. **Name of the skill:** `pbi-practice-library`, for what it holds.
2. **Shelves.** "General practice" holds advice that applies to most models. "Special-case techniques and facts" holds a technique for one situation and every note of strength Fact, whatever its kind.
3. **Layout of a note.** Its ID and the note on one line; then the strength, the mark Check where it applies, the year of the article and the article's address; then when it applies; then a version line where one matters.
4. **Group 4 is wider than Microsoft.** A note that cannot be followed together with a rule of this template's own standards (for example the one measures table, or `@` for columns a formula makes) is also not adopted, and is counted in group 4 with the words "template rule". The standards win over the library.
5. **A note about a preview feature is kept.** It can be followed after the developer's yes, so it does not contradict the rule on preview features. Its version line says that the feature is a preview here.
6. **A note that builds on a function Microsoft does not document** (it is not in the DAX function index) is not adopted: the DAX standard calls only listed functions.
7. **A note that names a tool outside this template** (for example DAX Studio or Tabular Editor) is kept as information for the developer. The skill says that Copilot never installs or calls such a tool.
8. **The eight-word check and the fixed snapshot.** Helpers compared the notes with a copy of the repository as it was before the library was added, so that no note could be judged "already said" by the library itself.
