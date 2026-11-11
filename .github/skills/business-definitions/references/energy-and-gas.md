# Energy, demand and gas

Electric and gas utilities only. Starter rows are standard industry definitions from the public glossaries beside each row.

Every row is an industry-standard starter with its public source beside it. It is **not** a confirmed definition of the company. The owner of a definition confirms the row and changes its status, or adds a row under "Company-specific terms". Copilot does not edit this file.

| Term | Usual definition | Additive? | Ask before using | Status | Owner | Public source |
| --- | --- | --- | --- | --- | --- | --- |
| Energy (kWh, MWh, GWh) | Electric power generated or used over a period of time. 1 MWh = 1,000 kWh | Yes, across time and customers | Metered, billed or estimated? Net of generation or gross? | industry standard |  | [NERC Glossary of Terms Used in NERC Reliability Standards - "Electrical Energy"](https://www.nerc.com/glossary-of-terms) and [EIA Glossary - "Megawatthour (MWh)"](https://www.eia.gov/tools/glossary/index.php?id=M) |
| Demand (kW, MW) | Rate of energy use at a moment or averaged over an interval | No: never sum over time. Sum across customers only for the same interval | Interval length? Coincident with system peak or each customer's own peak? | industry standard |  | [NERC Glossary of Terms Used in NERC Reliability Standards - "Demand"](https://www.nerc.com/glossary-of-terms) |
| Peak demand | Highest demand in the period, either averaged over an interval or instantaneous | No: take the maximum | Peak of what: system, circuit, customer? Which interval? | industry standard |  | [U.S. Energy Information Administration (EIA) Glossary - "Peak demand"](https://www.eia.gov/tools/glossary/index.php?id=P) and [NERC Glossary of Terms - "Peak Demand"](https://www.nerc.com/glossary-of-terms) |
| Average demand | Energy in the period / hours in the period | No: recompute |  | industry standard |  | [California Energy Commission - Energy Glossary - "AVERAGE DEMAND"](https://www.energy.ca.gov/resources/energy-glossary) |
| Load factor | Average demand / peak demand over the same period | No: recompute | Same period and same boundary for both parts? | industry standard |  | [U.S. Energy Information Administration (EIA) Glossary - "Load factor"](https://www.eia.gov/tools/glossary/index.php?id=L) |
| Interval data | Energy per fixed interval. (Arithmetic, not from the source: kWh in a 15-minute interval = average kW x 0.25, because 15 minutes is 0.25 hour) | Yes for kWh | Interval-ending or interval-beginning timestamps? | industry standard |  | [FERC-731 Demand Response/Time-Based Rate Programs and Advanced Metering - General Instructions and Glossary ("Interval Usage")](https://ferc.gov/sites/default/files/2020-06/Instructions-Glossary.pdf) |
| Therm | 100,000 Btu. 1 decatherm = 10 therms | Yes | Billed therms or measured volume converted? | industry standard |  | [U.S. Energy Information Administration (EIA) Glossary - "Therm"](https://www.eia.gov/tools/glossary/index.php?id=T) and [EIA Glossary - "Decatherm"](https://www.eia.gov/tools/glossary/index.php?id=D) |
| Gas volume (CCF, MCF) | 100 and 1,000 cubic feet | Yes | Volume becomes energy only through a heating-value factor that varies by place and time. Which factor? | industry standard |  | [U.S. Energy Information Administration (EIA) FAQ - How do I convert natural gas prices in dollars per cubic feet to dollars per British thermal unit or therm?](https://www.eia.gov/tools/faqs/faq.php?id=45&t=8) |

## Traps

- Adding up kW readings over time does not give energy unless each reading is multiplied by the length of its interval. If the user wants a total, they want kWh.
- Daylight saving: where clocks change, one day a year has 23 hours and one has 25. Hourly reports must not drop or double an hour. Ask which time zone the data is stored in and which one the report shows.
- Billing periods are often not calendar months. Say which one a "monthly" figure uses.
- Customer-level usage can be personal data. Default to aggregates, ask the owner what may be shown, and record the answer in `docs/report-brief.md`.
- Weather-normalised and actual figures are different measures. Label them.

## Company-specific terms

| Term | Definition | Additive? | Source of truth | Confirmed (date, by) |
| --- | --- | --- | --- | --- |
| | | | | |
