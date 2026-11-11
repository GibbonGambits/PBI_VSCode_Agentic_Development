# Finance and accounting

Every row is an industry-standard starter with its public source beside it. It is **not** a confirmed definition of the company. The owner of a definition confirms the row and changes its status, or adds a row under "Company-specific terms". Copilot does not edit this file.

| Term | Usual definition | Additive? | Ask before using | Status | Owner | Public source |
| --- | --- | --- | --- | --- | --- | --- |
| Actual | Amounts actually incurred, as distinguished from forecast amounts; in budget reporting, the amounts that result from carrying out the budget | Yes | Which ledger and as of which close? Accruals included? | industry standard |  | [Federal Acquisition Regulation 31.001 Definitions (Acquisition.gov)](https://www.acquisition.gov/far/31.001) and [IPSAS 24, Presentation of Budget Information in Financial Statements, paragraph 13](https://ifacweb.blob.core.windows.net/publicfiles/2024-12/A33-IPSAS-24.pdf) |
| Budget / plan | The approved budget for the period: the spending authority approved for it | Yes | Original or revised? Which version? | industry standard |  | [IPSAS 24, Presentation of Budget Information in Financial Statements, paragraph 7 (IPSASB handbook chapter, published by IFAC)](https://ifacweb.blob.core.windows.net/publicfiles/2024-12/A33-IPSAS-24.pdf) |
| Forecast (estimate at completion) | Actuals to date plus the estimate for the remainder (in project reporting, the estimate at completion) | Yes | Which forecast cycle? | industry standard |  | [NASA PP&C Glossary, entry 'Estimate at Completion (EAC)'](https://www.nasa.gov/ocfo/ppc-corner/ppc-glossary/) |
| Variance | The difference between actual and budget; state which is subtracted from which | Yes | Sign convention: is positive good or bad? It flips between cost and revenue lines | industry standard |  | [IPSAS 24, Presentation of Budget Information in Financial Statements, paragraph 15 (IPSASB handbook chapter, published by IFAC)](https://ifacweb.blob.core.windows.net/publicfiles/2024-12/A33-IPSAS-24.pdf) |
| Variance % | Variance / budget, as a percentage (in the source: variance at completion / budget at completion x 100) | No: recompute | What to show when budget is zero or negative? | industry standard |  | [NASA Earned Value Management (EVM) Reference Card](https://www.nasa.gov/wp-content/uploads/2018/06/nasa-evm-reference-card.pdf) |
| O&M expense | Operating and maintenance cost, expensed in the period | Yes | Which cost elements? Net of credits? | industry standard |  | [FERC Uniform System of Accounts, 18 CFR Part 101, Operating Expense Instruction 4, which uses the term; the same part lists the Operation and Maintenance Expense Accounts](https://www.ecfr.gov/current/title-18/chapter-I/subchapter-C/part-101) |
| Capital expenditure | Spend to acquire, add to or improve property, plant and equipment | Yes | Spend or additions to plant in service? With overheads? | industry standard |  | [U.S. Bureau of Economic Analysis Glossary, entry 'Capital expenditures'](https://www.bea.gov/help/glossary) |
| Year to date | Period 1 through the current period | Derived: sum of periods for flows such as spend; a balance is taken as of the period end | Fiscal calendar and current-period rule (last closed, or today)? | industry standard |  | [SEC Regulation S-X, 17 CFR 210.10-01(c)(2), Interim financial statements](https://www.ecfr.gov/current/title-17/chapter-II/part-210/subject-group-ECFR4b741595bf06dbe/section-210.10-01) |
| Headcount cost / labour | Employer costs for wages, salaries and employee benefits (labour cost) | Yes | Straight time, overtime, burdens? See the traps in `workforce.md` | industry standard |  | [U.S. Bureau of Labor Statistics Glossary, entry 'Compensation'](https://www.bls.gov/bls/glossary.htm) |

## Traps

- State the sign convention once per report and show favourable/unfavourable with a label or icon, not colour alone.
- Do not mix budget versions in one visual unless each is labelled (for example original and final budget).
- Mid-period numbers move until close. Show "as of" and whether the period is closed.
- Regulatory and financial-statement views can classify the same spend differently, for example in rate-regulated companies. Name the view.
- Reports that feed financial reporting or controls may need change evidence, such as the pull request, its reviewer and a reconciliation to the ledger. Ask the owner what is required and record it in `docs/report-brief.md`.
- Unreleased results can be restricted. Ask the owner before sharing screenshots.

## Company-specific terms

| Term | Definition | Additive? | Source of truth | Confirmed (date, by) |
| --- | --- | --- | --- | --- |
| | | | | |
