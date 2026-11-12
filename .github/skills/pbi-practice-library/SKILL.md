---
name: pbi-practice-library
description: Use this skill when a task needs background practice that the standards do not give - writing or reviewing DAX, designing a semantic model, a performance question, an unusual requirement, or a check that fails for no clear reason. It is a reference library of practice notes on DAX and Power BI modelling, drawn from public SQLBI articles and white papers and restated in new words, sorted by topic with one index. It is information, never a rule to enforce - the checklist and the standards win. Read the index, then only the one file the task needs. Trigger words - best practice, good practice, pattern, technique, why does this measure, slow measure, optimise, unusual requirement, how should I model.
---
# Practice library

A library of practice notes on DAX and semantic models. Each note restates, in new words, one piece of advice or one fact from a public SQLBI article or white paper, and gives its address. The article holds the detail.

The library is information. It is not a standard and nothing checks it. It never changes what the checklist, the instruction files, the standards or the checks ask for.

## When to use it

- You write or review DAX and the DAX standard does not answer the question.
- You design a model, or part of one, and need the reasoning behind a design choice.
- A measure or a visual is slow, or the developer asks a performance question.
- The requirement is unusual: a calculation, a model shape or a report behaviour that no standard and no shipped example covers.
- A check fails and the finding and its standard do not explain why. Look it up first (skill `pbi-lookup`); open the library when the pages do not settle it.

Not for a business meaning (that comes from the brief or the developer), and not for file syntax (the standards and the shipped examples).

## How to use it

1. Read the standard for the work first (skills `pbi-semantic-model` and `pbi-report`). Open the library only when the standard leaves the question open.
2. Read `references/index.md`. For each file it says what the file covers and which DAX functions and Power BI features its notes mention.
3. Open only the file that fits, at most two for one task. Never read the whole library for one task.
4. Use the notes that apply. Each file has two shelves: "General practice" (advice that holds for most models) and "Special-case techniques and facts" (a technique for one situation, or how the engine behaves). A special-case note applies only when its "When" line is true for this model.
5. Say in your answer which notes you used, by ID, with the article's address, so that the developer can read the same page.

## What a note is worth

- Order of trust: the owner's checklist, then Microsoft, then SQLBI. A note never overrides a checklist item, an instruction file, a standard or a check. If a note and a standard disagree, follow the standard and tell the developer about the note.
- The strength word says how firmly the article puts it: Must, Should, Consider, Option (one possible way), Fact (how something behaves). It is the article's weight, not this template's.
- A note marked **Check** may no longer hold in current Power BI: the article is old, or the product has moved. Confirm it with the skill `pbi-lookup` (Microsoft Learn first) before you rely on it. If you cannot confirm it, do not rely on it, and say so.
- A note marked **Paper** comes from a white paper. Its link opens only a summary; the paper itself sits on a download site that `pbi-lookup` does not open, so the note cannot be confirmed there. Use it as background only. If it also links an article, read that article. Otherwise, before you rely on it, confirm the point on Microsoft Learn with `pbi-lookup`. If Microsoft Learn does not confirm it, do not base a change on it, and tell the developer the note is unconfirmed.
- The year on a note is the year of the article. A "Version" line names a release or a limit that the advice depends on.
- A note is no reason for an exception in the brief, and no reason to skip a check. The developer decides exceptions.
- A note that describes a preview feature does not make it agreed: the rule on preview features in the project instructions holds.
- Advice that depends on a custom visual, another vendor's tool or another system, or on publishing or deploying, was left out of the library. A note may still name another product in passing, such as Analysis Services or Excel. You never install or call another vendor's tool, and you do not suggest one: the rule on suggestions in `.github/skills/pbi-checklist-review/references/native-features.md` holds.
- For the detail behind a note, read its article through the skill `pbi-lookup`. Never copy SQLBI text, code or images into the project or into this template: write the formula for this model, in the style of the DAX standard.

## The improvement loop

The library records no lessons and proposes no template change by itself. When a lesson is written (skill `pbi-lessons`), its correction may point to a note by ID.

## Topics

| Topic | Files in `references/` begin with |
|---|---|
| DAX evaluation context: filter context, row context, context transition, CALCULATE | t01 |
| DAX authoring style: formatting, naming, variables, structure | t02 |
| DAX table functions and queries | t03 |
| Time intelligence and date tables | t04 |
| Relationships and filter propagation | t05 |
| Data model design | t06 |
| DAX performance and optimization | t07 |
| Storage engine, model size and memory | t08 |
| Storage modes: choosing a mode, DirectQuery, composite models, push datasets | t09 |
| Security | t10 |
| Calculation groups and field parameters | t11 |
| Window functions and visual calculations | t12 |
| User-defined functions in DAX | t13 |
| Business calculation patterns | t14 |
| Report-facing DAX and report design | t15 |
| Tooling, workflow and AI assistance | t16 |

Checklist items: none
