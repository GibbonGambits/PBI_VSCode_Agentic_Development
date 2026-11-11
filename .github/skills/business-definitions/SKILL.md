---
name: business-definitions
description: Use this skill when a report or model needs a business term defined, or a measure built, in one of these eight areas - electric reliability (SAIDI, SAIFI, CAIDI), energy and gas units (kWh, demand, load factor, therms), customer and contact-centre measures, safety rates (recordable incidents, DART), finance (actual, budget, forecast, variance), workforce (headcount, FTE, turnover), IT and security (availability, MTBF, patching), work management (schedule compliance, backlog, unit cost). Read only the one file the task needs.
---
# Business definitions (starter rows)

Each file below holds starter definitions for one area. Read a file only when the report you are working on uses terms from that area, or when a row in the file you are reading points to another one.

| When the report is about | Read |
|---|---|
| Electric outage and reliability measures (electric utilities only) | `references/reliability.md` |
| Electricity and gas quantities and units (electric and gas utilities only) | `references/energy-and-gas.md` |
| Customers, accounts, contact-centre service | `references/customer.md` |
| Workplace safety and incident rates | `references/safety.md` |
| Actuals, budget, forecast, variance, spend | `references/finance.md` |
| Headcount, FTE, turnover, vacancies, overtime | `references/workforce.md` |
| System availability, failures, patching, vulnerabilities | `references/it-and-security.md` |
| Maintenance and work scheduling, backlog, unit cost | `references/work-management.md` |

Some rows in the customer, finance and work management files come from utility-sector or public-sector sources. The "Public source" column shows where each row comes from; check that it fits the report's business before using it.

## How to use a row

- Every row is an industry-standard starter with its public source beside it. It is not a confirmed definition of the company.
- Before a starter goes into a measure or a description, ask the developer the question in the row's "Ask before using" column and get the company's own definition confirmed.
- For a report, record the confirmed definition in section 5 of `docs/report-brief.md`. From there it goes into the `///` description of the measure (skill `pbi-semantic-model`).
- Do not edit the reference files. Their Status and Owner columns and their "Company-specific terms" tables are filled in by the people who own the definitions.
- If the term, or its whole area, is not here, do not make one up. Ask the developer.
- Do not add files for other areas.

Checklist items: 37, 48
