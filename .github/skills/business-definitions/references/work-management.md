# Work management, scheduling and operations

Every row is an industry-standard starter with its public source beside it. It is **not** a confirmed definition of the company. The owner of a definition confirms the row and changes its status, or adds a row under "Company-specific terms". Copilot does not edit this file.

| Term | Usual definition | Additive? | Ask before using | Status | Owner | Public source |
| --- | --- | --- | --- | --- | --- | --- |
| Schedule compliance | Scheduled jobs completed in the period / jobs scheduled for the period | No: recompute | Is break-in work counted? Completed means field-complete or closed? | industry standard |  | [PNNL (U.S. DOE national laboratory, FEMP O&M Best Practices) - Applying Key Performance Indicators, Definitions](https://www.pnnl.gov/projects/om-best-practices/applying-key-performance-indicators) |
| Preventive maintenance compliance | PM tasks completed / PM tasks scheduled (the source calls this Preventive Maintenance Completion Percentage) | No: recompute | On time, or completed at all? Grace window? | industry standard |  | [U.S. DOE Federal Energy Management Program - Operations & Maintenance Best Practices Guide, Release 3.0, Chapter 3, Table 3.1.1 Industry O&M metrics and benchmarks](https://www1.eere.energy.gov/femp/pdfs/om_3.pdf) |
| Backlog | Valid work that is not in progress, complete, closed or waiting for approval, in jobs or estimated labor hours. Some sources count all open work orders, or only work past its required-by date | Yes on one date; not over time | Which statuses count? | industry standard |  | [U.S. Army Corps of Engineers Engineer Pamphlet EP 1130-2-557 (17 Dec 2025), Civil Works Facilities and Equipment Maintenance - Workflow and Work Order Requirements, Glossary](https://publibrary.sec.usace.army.mil/api/download?id=65e15cad-d153-4617-d282-02bbb69f94f5&filename=EP+1130-2-557+-+Workflow+and+Work+Order+Requirements+2025+12+09+-+Final.pdf&preview=true) and [NASA Reliability-Centered Maintenance Guide for Facilities and Collateral Equipment (September 2008), sec. 12.10.1-12.10.2](https://www.nasa.gov/wp-content/uploads/2023/06/nasa-rcmguide.pdf) and [PNNL, FEMP O&M Best Practices - Applying Key Performance Indicators, Definitions ('Backlog')](https://www.pnnl.gov/projects/om-best-practices/applying-key-performance-indicators) |
| Backlog weeks | Backlog hours / available crew hours per week | No: recompute | Which crews and which availability? | industry standard |  | [NASA Reliability-Centered Maintenance Guide for Facilities and Collateral Equipment (September 2008), sec. 12.10.2 Backlog of All Open Work Orders](https://www.nasa.gov/wp-content/uploads/2023/06/nasa-rcmguide.pdf) |
| Unit cost | The cost of a selected unit of a good or service. (Arithmetic, not from the source: cost / number of units) | No: recompute | Units completed, produced or delivered? Same period and scope for both parts? | industry standard |  | [FASAB - Glossary of Cost Accounting Terms Established in SFFAS 4, Managerial Cost Accounting Concepts and Standards for the Federal Government](https://files.fasab.gov/pdffiles/costacc_glossary.pdf) |
| Overall equipment effectiveness (OEE) | Availability x performance x quality | No: recompute each factor | Planned stops excluded from availability? | industry standard |  | [NIST Advanced Manufacturing Series 300-11, Recommendations for Collecting, Curating, and Re-Using Manufacturing Data (July 2020), sec. 2](https://nvlpubs.nist.gov/nistpubs/ams/NIST.AMS.300-11.pdf) |

## Traps

- A status's meaning ("complete", "closed") differs between systems. Write the status codes used in `docs/report-brief.md`.
- Period boundaries: a job scheduled in one week and finished the next counts where? Decide once.
- Asset identifiers and locations for critical equipment can be restricted. Ask the owner before adding detail tables or maps.

## Company-specific terms

| Term | Definition | Additive? | Source of truth | Confirmed (date, by) |
| --- | --- | --- | --- | --- |
| | | | | |
