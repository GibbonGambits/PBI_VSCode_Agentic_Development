# Reliability (electric)

Electric utilities only. Starter rows follow the usual IEEE 1366 definitions, as restated in the public sources beside each row.

Every row is an industry-standard starter with its public source beside it. It is **not** a confirmed definition of the company. The owner of a definition confirms the row and changes its status, or adds a row under "Company-specific terms". Copilot does not edit this file.

| Term | Usual definition | Additive across areas or time? | Ask before using | Status | Owner | Public source |
| --- | --- | --- | --- | --- | --- | --- |
| Customer minutes interrupted (CMI) | Sum over sustained interruptions of customers affected x minutes out | Yes | What counts as sustained (IEEE: longer than 5 minutes)? Planned outages in or out? | industry standard |  | [U.S. Energy Information Administration, Form EIA-861 Annual Electric Power Industry Report Instructions, Schedule 3 Part B (Distribution System Reliability Information - IEEE)](https://www.eia.gov/survey/form/eia_861/instructions.pdf) and [IEEE PES Distribution Reliability Working Group, 2024 panel, slide 7 (abbreviation CMI)](https://cmte.ieee.org/pes-drwg/wp-content/uploads/sites/61/IEEE-1366-Panel-Presentation.pptx) |
| Customers interrupted (CI) | Count of sustained customer interruptions | Yes | Same exclusions as CMI? Is one customer interrupted twice counted twice? | industry standard |  | [U.S. Energy Information Administration, Form EIA-861 Annual Electric Power Industry Report Instructions, Schedule 3 Part B](https://www.eia.gov/survey/form/eia_861/instructions.pdf) and [IEEE PES Distribution Reliability Working Group, 2024 panel, slide 7 (abbreviation CI)](https://cmte.ieee.org/pes-drwg/wp-content/uploads/sites/61/IEEE-1366-Panel-Presentation.pptx) |
| Customers served | Average number of customers served in the area during the reporting period; if a different count is used (for example period end), say which | No: a snapshot or period average, never summed over months | Period end or average? Which customer count (see `customer.md`)? | industry standard |  | [IEEE PES Distribution Reliability Working Group, "Proposed Changes to IEEE 1366" (working-group markup of the guide's text, posted January 11, 2010), definition 3.21](https://cmte.ieee.org/pes-drwg/wp-content/uploads/sites/61/2009-11-17-Proposed-Changes-to-IEEE-1366.pdf) |
| SAIDI | CMI / customers served | No: recompute from CMI and customers served | With or without major event days? Planned outages? Transmission-caused? Minutes or hours? | industry standard |  | [U.S. Energy Information Administration, Form EIA-861 Annual Electric Power Industry Report Instructions, Schedule 3 Part B](https://www.eia.gov/survey/form/eia_861/instructions.pdf) |
| SAIFI | CI / customers served | No: recompute | Same variant as the SAIDI beside it? | industry standard |  | [U.S. Energy Information Administration, Form EIA-861 Annual Electric Power Industry Report Instructions, Schedule 3 Part B](https://www.eia.gov/survey/form/eia_861/instructions.pdf) |
| CAIDI | CMI / CI (equals SAIDI / SAIFI) | No: recompute | Same variant as SAIDI and SAIFI? | industry standard |  | [IEEE PES Distribution Reliability Working Group, "IEEE Std 1366: Background, definitions and benchmarking" (2024 panel), slide 7](https://cmte.ieee.org/pes-drwg/wp-content/uploads/sites/61/IEEE-1366-Panel-Presentation.pptx) |
| MAIFI | Momentary customer interruptions / customers served | No: recompute | Momentary threshold? Events or individual interruptions? | industry standard |  | [Pennsylvania Code, Title 52 (Public Utility Commission), Section 57.192 Definitions](https://www.pacodeandbulletin.gov/Display/pacode?file=/secure/pacode/data/052/chapter57/s57.192.html) |
| CEMI-n | Customers with n or more sustained interruptions / customers served | No | Is it "n or more" or "more than n"? Which n? Rolling 12 months? | industry standard |  | [IEEE PES Distribution Reliability Working Group, "IEEE Std 1366: Background, definitions and benchmarking" (2024 panel), slide 8](https://cmte.ieee.org/pes-drwg/wp-content/uploads/sites/61/IEEE-1366-Panel-Presentation.pptx) |
| Major event day (MED) | A day whose system SAIDI exceeds a threshold set from history (IEEE 2.5 beta method) | n/a | Which threshold and history window? Who publishes the MED list? | industry standard |  | [IEEE PES Distribution Reliability Working Group, "IEEE 1366 & Regulatory Implications" (posted July 6, 2006), slide 16](https://cmte.ieee.org/pes-drwg/wp-content/uploads/sites/61/2006-07-IEEE1366-Regulatory-Implications.pdf) and [IEEE PES Distribution Reliability Working Group, 2024 panel, slide 6 (threshold from five years of daily SAIDI)](https://cmte.ieee.org/pes-drwg/wp-content/uploads/sites/61/IEEE-1366-Panel-Presentation.pptx) |

## Traps

- An area's SAIDI is not the average of its sub-areas' SAIDI. Sum CMI, sum customers served, then divide.
- A year-to-date SAIDI uses year-to-date CMI over one customer count, not the sum of monthly SAIDI values unless the customer count is held fixed. Ask which.
- "With MED" and "without MED" are different measures. Never show one unlabelled.
- Outage data can change after events are reviewed. Ask whether it does, and show a "data as of" date.
- Outage and asset location data can be restricted. Ask the owner what may be shown before adding maps or circuit-level detail, and record the answer in `docs/report-brief.md`.

## Company-specific terms

| Term | Definition | Additive? | Source of truth | Confirmed (date, by) |
| --- | --- | --- | --- | --- |
| | | | | |
