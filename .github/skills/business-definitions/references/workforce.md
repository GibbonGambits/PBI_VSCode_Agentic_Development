# Workforce (HR)

Every row is an industry-standard starter with its public source beside it. It is **not** a confirmed definition of the company. The owner of a definition confirms the row and changes its status, or adds a row under "Company-specific terms". Copilot does not edit this file.

| Term | Usual definition | Additive? | Ask before using | Status | Owner | Public source |
| --- | --- | --- | --- | --- | --- | --- |
| Headcount | People employed on a given date | Across groups on one date: yes. Over time: no, it is a snapshot; never sum months | Regular only? Part-time, interns, leave of absence, contractors? | industry standard |  | [U.S. Office of Personnel Management, FedScope Employment Cube (June 2024) Raw Data Set documentation, section 4.17 Employment](https://www.opm.gov/data/datasets/Files/722/e8455624-c73b-44f1-88f6-d914a3db6af5.pdf) |
| FTE | Regular hours worked (excluding overtime) / full-time hours for the same period | Yes across people for the same period; not across periods | Full-time basis (hours per week)? | industry standard |  | [OMB Circular No. A-11 (2026), Section 85 - Estimating Employment Levels and the Employment Summary (Schedule Q), section 85.2](https://www.whitehouse.gov/wp-content/uploads/2025/08/s85.pdf) |
| Average headcount | Mean of headcount over the period | No: recompute | Mean of which counts: month-ends, or every pay period? | industry standard |  | [OSHA Forms for Recording Work-Related Injuries and Illnesses (Forms 300, 300A, 301 package), Worksheet to Help You Fill Out the Summary](https://www.osha.gov/sites/default/files/OSHA-RK-Forms-Package.pdf) |
| Turnover rate | Separations in period / average headcount | No: recompute | Voluntary only? Retirements? Annualised? | industry standard |  | [U.S. Bureau of Labor Statistics, Job Openings and Labor Turnover Survey News Release, March 16, 2018 (archived), annual total separations rates table footnote](https://www.bls.gov/news.release/archives/jolts_03162018.htm) |
| Vacancy rate | Open positions / approved positions | No: recompute | What counts as open? | industry standard |  | [U.S. Government Accountability Office, GAO-25-107121, DOD Cyberspace Operations: About 500 Organizations Have Roles, with Some Potential Overlap (September 2025), figure notes](https://files.gao.gov/reports/GAO-25-107121/index.html) |
| Time to fill | Days from requisition opened to offer accepted | No: average or median per requisition | Start and end events? Mean or median? | industry standard |  | [Society for Human Resource Management (SHRM), SHRM Benchmarking: Talent Access report, metric definitions](https://www.shrm.org/content/dam/en/shrm/executive-network/insights/Talent-Access-Report-TOTAL.pdf) |
| Overtime % | Overtime hours / total hours worked | No: recompute | Paid or worked? | industry standard |  | [U.S. Postal Service Office of Inspector General, Management of Overtime in the Northeast Area, Audit Report HR-AR-17-014, footnote 4](https://www.uspsoig.gov/sites/default/files/reports/2023-01/HR-AR-17-014.pdf) |

## Traps

- **Small groups identify people.** Ask HR whether figures for small groups must be hidden or rolled up, and at what minimum size; do not pick one. If they must, build the rule into the measure, not the visual, so it still holds when a slicer narrows a bigger group.
- Personal characteristics, pay, performance, medical and leave data are highly sensitive. Ask the owner what access control (for example row-level security) and approval are required, and record the answer in `docs/report-brief.md`.
- Organisation hierarchies change. Say whether history is shown as it was or as the organisation is today.

## Company-specific terms

| Term | Definition | Additive? | Source of truth | Confirmed (date, by) |
| --- | --- | --- | --- | --- |
| | | | | |
