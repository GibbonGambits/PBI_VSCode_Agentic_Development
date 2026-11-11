# IT and security

Every row is an industry-standard starter with its public source beside it. It is **not** a confirmed definition of the company. The owner of a definition confirms the row and changes its status, or adds a row under "Company-specific terms". Copilot does not edit this file.

| Term | Usual definition | Additive? | Ask before using | Status | Owner | Public source |
| --- | --- | --- | --- | --- | --- | --- |
| Availability % | (Agreed service time - downtime) / agreed service time | No: recompute | Planned maintenance counted as downtime? Which service hours? | industry standard |  | [UK Cabinet Office, Model Services Contract v2.2A (1 September 2025), Schedules (England & Wales): the text is in the attached combined schedules document, Schedule 3 (Performance Levels), Annex 1 Part B, para 2 'Service Availability'](https://www.gov.uk/government/publications/the-model-services-contract-schedules-england-wales) and [ITIL glossary and abbreviations, English (2011, Crown Copyright), entry 'availability'](https://htmlscript.auburn.edu/oit/ITILV3_Glossary.pdf) |
| Mean time to restore service (MTRS) | Average time taken to restore a service after a failure, measured from when it fails until it is fully restored | No: recompute | Clock starts at detection or report? Paused time excluded? The public glossary uses MTTR for mean time to repair, which leaves out recovery time: which does the company mean? | industry standard |  | [ITIL glossary and abbreviations, English (2011, Crown Copyright), entries 'mean time to restore service (MTRS)' and 'mean time to repair (MTTR)'](https://htmlscript.auburn.edu/oit/ITILV3_Glossary.pdf) |
| Mean time between failures (MTBF) | Operating time / failures | No: recompute | What counts as a failure? | industry standard |  | [NIST/SEMATECH e-Handbook of Statistical Methods, 8.4.5.1 Constant repair rate (HPP/exponential) model](https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm) |
| Incident count by priority | Count of incidents at each priority | Yes | Priority at open or at close? | industry standard |  | [Office of Management and Budget, Federal Information Security Modernization Act of 2014 Annual Report, Fiscal Year 2023, section 'Incidents by NCISS Priority Level' (Table 4)](https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/06/FY23-FISMA-Report.pdf) |
| Patch compliance | Assets patched by the maintenance plan's deadline / assets, as a percentage | No: recompute | Scope and policy window? Split by asset importance and vulnerability importance, as the source recommends? ("Patch compliance" is this row's name; the source does not name the measure.) | industry standard |  | [NIST SP 800-40 Rev. 4, Guide to Enterprise Patch Management Planning: Preventive Maintenance for Technology (April 2022), section 3.6 Choose Actionable Enterprise-Level Patching Metrics](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-40r4.pdf) |
| Open vulnerabilities | Count of open findings by severity | Yes on one date; not over time | Severity scale? Unique findings or finding-asset pairs? | industry standard |  | [NIST SP 800-40 Version 2.0, Creating a Patch and Vulnerability Management Program (November 2005; withdrawn July 2013, archived by NIST), section 3.2.1.1, under 'Number of Vulnerabilities'](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-40ver2.pdf) |

## Traps

- Security detail can be restricted: host names, IP addresses, open vulnerabilities and control gaps. Ask the owner before putting any of it in a broadly shared report or in a prompt, default to aggregates, and record the answer in `docs/report-brief.md`.
- Systems that support critical infrastructure can fall under extra protection rules. If a report touches them, stop and ask who must approve it.
- Averages hide the long tail. Show a median or a percentile beside a mean time.

## Company-specific terms

| Term | Definition | Additive? | Source of truth | Confirmed (date, by) |
| --- | --- | --- | --- | --- |
| | | | | |
