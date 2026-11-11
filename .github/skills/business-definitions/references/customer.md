# Customer

Every row is an industry-standard starter with its public source beside it. It is **not** a confirmed definition of the company. The owner of a definition confirms the row and changes its status, or adds a row under "Company-specific terms". Copilot does not edit this file.

| Term | Usual definition | Additive? | Ask before using | Status | Owner | Public source |
| --- | --- | --- | --- | --- | --- | --- |
| Customer | A person or business that has contracted with the company to obtain goods or services in exchange for payment | No: distinct count | Is the report counting people, accounts, premises or meters? These differ by a lot | industry standard |  | [FASB Accounting Standards Update No. 2014-09, Revenue from Contracts with Customers (Topic 606), Section A - Glossary](https://storage.fasb.org/ASU%202014-09_Section%20A.pdf) |
| Account | A billing account: the group of products and services a customer buys under an agreement, used for billing and payment | No: distinct count | Can one customer hold several accounts? Active only? As of which date? | industry standard |  | [NAESB REQ.21 Energy Services Provider Interface (ESPI) customer.xsd, Version 4.0 (published schema, 13 Dec 2023), complexType CustomerAccount](https://www.naesb.org/espi/customer.xsd) |
| Premise / service point | A physical location (land and buildings) / the point of connection between the utility's facilities and the premises wiring | No: distinct count | Electric, gas or both? One home with both services counts once or twice? | industry standard |  | [Public Utility Commission of Texas, 16 TAC 25.5 Definitions (Premises)](https://ftp.puc.texas.gov/public/puct-info/agency/rulesnlaws/subrules/electric/25.5/25.5.pdf) and [OSHA 29 CFR 1910.399 Definitions (Service point)](https://www.govinfo.gov/content/pkg/CFR-2024-title29-vol5/xml/CFR-2024-title29-vol5-sec1910-399.xml) |
| Average handle time | Average time spent handling a contact, including talk, hold and after-call wrap-up | No: recompute | Does the company's figure include talk, hold and after-call work, as the public definition does? | industry standard |  | [IRS Internal Revenue Manual 1.4.21, Accounts Management and Compliance Guide for System Administrators/Analysts - glossary](https://www.irs.gov/irm/part1/irm_01-004-021) |
| First-contact resolution | Inquiries resolved during the customer's first contact, without a follow-up / total inquiries | No: recompute | Repeat window in days? | industry standard |  | [GSA Centers of Excellence, How to Measure Contact Center Performance (28 May 2019)](https://coe.gsa.gov/2019/05/28/cc-update-2.html) and [New York State, The New York Experience (NYX) - Call Center Standards ("First Call Resolution")](https://www.ny.gov/new-york-experience-nyx/call-center-standards) |
| Satisfaction score | Score from a customer survey that asks customers to rate their experience | No | Which survey, which scale, top-box or mean? Minimum responses to show a score? | industry standard |  | [New York State, The New York Experience (NYX) - Call Center Standards](https://www.ny.gov/new-york-experience-nyx/call-center-standards) |

## Traps

- "Customers" on two reports may not mean the same count. Write the counting unit in every title or footnote.
- A count of customers over a year is not the sum of twelve monthly counts.
- Names, addresses, account numbers, usage and payment status can be personal data. Default to aggregates. Ask the owner what a customer-level table needs (for example row-level security and an approval) and record the answer in `docs/report-brief.md`.
- Programme and rate enrolment can reveal income or medical circumstances. Ask the owner how it must be handled.

## Company-specific terms

| Term | Definition | Additive? | Source of truth | Confirmed (date, by) |
| --- | --- | --- | --- | --- |
| | | | | |
