\# Cross-System Data Dictionary  

\## Northstar Health Operations



\---



\# Purpose



This document defines shared identifiers, common data fields, relational standards, naming expectations, and cross-system data conventions used across the Northstar Health Operations ecosystem.



The purpose of this data dictionary is to:

\- prevent naming drift

\- standardize shared identifiers

\- support relational analysis

\- improve future SQL integration

\- support future Power BI modeling

\- maintain cross-system consistency

\- preserve ecosystem scalability



This document serves as the enterprise relational language reference for the Northstar Health Operations ecosystem.



\---



\# Data Dictionary Philosophy



Northstar Health Operations uses standardized shared identifiers to connect operational activity across subsystems.



Shared identifiers allow separate operational domains to interact while remaining modular.



This supports:

\- subsystem independence

\- cross-system reporting

\- relational analysis

\- future database construction

\- enterprise KPI aggregation



\---



\# Core Shared Identifiers



| Identifier | Purpose | Example |

|---|---|---|

| ticket\_id | Unique ticket or incident record | INC-100012 |

| related\_ticket\_id | Connects non-ticket records to ticket records | INC-100012 |

| item\_id | Unique inventory item identifier | ITEM-1003 |

| location\_id | Unique operational location identifier | LOC-DURHAM-07 |

| vendor\_id | Unique vendor identifier | VEND-003 |

| employee\_id | Future workforce/team member identifier | EMP-1001 |

| shipment\_id | Unique vendor shipment identifier | SHIP-1002 |

| replenishment\_id | Unique replenishment workflow record | REPL-1002 |

| shortage\_id | Unique shortage event record | SHORT-1001 |

| discrepancy\_id | Unique inventory discrepancy record | DISC-1001 |



\---



\# Identifier Standards



\## ticket\_id



\### Purpose

Uniquely identifies a ticket in the Ticketing \& Incident Management subsystem.



\### Format

```text

INC-######

```



\### Example

```text

INC-100012

```



\### Primary Dataset

```text

ticketing-system/datasets/tickets-v1.csv

```



\---



\## related\_ticket\_id



\### Purpose

Connects non-ticket operational records to tickets when a workflow generates or relates to an incident.



\### Format

```text

INC-######

```



\### Example

```text

INC-100012

```



\### Used In

\- replenishment-events.csv

\- shortage-events.csv

\- inventory-discrepancies.csv

\- vendor-shipments.csv

\- future vendor performance datasets

\- future workforce escalation datasets



\### Governance Rule

Use `related\_ticket\_id` only when the record connects back to an existing or planned operational ticket.



\---



\## item\_id



\### Purpose

Uniquely identifies an inventory item.



\### Format

```text

ITEM-####

```



\### Example

```text

ITEM-1003

```



\### Primary Dataset

```text

inventory-operations/datasets/inventory-items.csv

```



\### Used In

\- location-inventory.csv

\- replenishment-events.csv

\- shortage-events.csv

\- inventory-discrepancies.csv

\- vendor-shipments.csv



\---



\## location\_id



\### Purpose

Identifies an operational location such as a clinic, distribution hub, or support center.



\### Format

```text

LOC-\[LOCATION]-##

```



\### Examples

```text

LOC-RALEIGH-03

LOC-DURHAM-07

LOC-WAKEFOREST-11

LOC-CARY-HUB-01

```



\### Used In

\- location-inventory.csv

\- replenishment-events.csv

\- shortage-events.csv

\- inventory-discrepancies.csv

\- vendor-shipments.csv

\- future workforce coordination datasets



\---



\## vendor\_id



\### Purpose

Uniquely identifies a vendor or supplier.



\### Format

```text

VEND-###

```



\### Example

```text

VEND-003

```



\### Used In

\- inventory-items.csv

\- replenishment-events.csv

\- vendor-shipments.csv

\- future vendor-performance datasets



\---



\# Dataset Naming Standards



Dataset filenames should be:

\- lowercase

\- hyphen-separated

\- business-readable

\- grain-aware

\- plural when representing multiple records



Examples:

```text

inventory-items.csv

location-inventory.csv

replenishment-events.csv

shortage-events.csv

inventory-discrepancies.csv

vendor-shipments.csv

tickets-v1.csv

```



\---



\# Field Naming Standards



Field names should use:

```text

snake\_case

```



Examples:

```text

related\_ticket\_id

current\_stock

reorder\_point

delivery\_status

resolution\_hours

```



Avoid:

\- spaces

\- camelCase

\- inconsistent abbreviations

\- unclear shorthand



\---



\# Date \& Timestamp Standards



\## Date-Only Fields



Date-only operational fields may use:

```text

MM/DD/YYYY

```



or normalized ISO date values:

```text

YYYY-MM-DD

```



provided the dataset remains internally consistent.



Future SQL/Python workflows should normalize date-only fields during ingestion.



Examples:

```text

2026-05-21

5/21/2026

```



\---



\## Timestamp Fields



Timestamp fields should use:

```text

YYYY-MM-DD HH:MM:SS

```



Examples:

```text

2026-05-20 08:12:00

2026-05-20 11:02:00

```



Timestamp fields are required when calculating:

\- SLA response time

\- resolution time

\- workflow aging

\- escalation timing

\- operational turnaround



\---



\# Boolean Standards



Boolean fields should use:



```text

TRUE

FALSE

```



Examples:

```text

escalation\_flag

delay\_flag

active\_flag

fulfillment\_accuracy\_flag

```



Avoid:

\- Yes/No

\- Y/N

\- 1/0



unless a future system specifically requires conversion.



\---



\# Status Field Standards



Status fields should be:

\- business-readable

\- title case when displayed

\- consistent within each dataset



Examples:

```text

Closed

In Progress

Pending

Received

Delayed

Critical Low

Stockout

```



\---



\# Relationship Standards



Subsystems should connect through shared identifiers rather than duplicated descriptive text.



Example:



```text

shortage-events.csv

related\_ticket\_id = INC-100012

↓

tickets-v1.csv

ticket\_id = INC-100012

```



This enables:

\- future joins

\- cross-system analysis

\- relational reporting

\- Power BI model relationships

\- SQL integration



\---



\# Current Cross-System Relationships



\## Inventory to Ticketing



Inventory records may connect to tickets through:



```text

related\_ticket\_id

```



Used when inventory events create or relate to operational incidents.



Examples:

\- shortages

\- delayed replenishments

\- vendor shipment failures

\- discrepancy investigations



\---



\## Inventory to Vendor Performance



Inventory records connect to vendors through:



```text

vendor\_id

```



Used in:

\- preferred vendor tracking

\- shipment reporting

\- fulfillment analysis

\- vendor delay monitoring



\---



\## Inventory Item Relationships



Inventory item records connect to operational activity through:



```text

item\_id

```



Used across:

\- location stock levels

\- replenishments

\- shortages

\- discrepancies

\- vendor shipments



\---



\## Location Relationships



Operational location records connect across systems through:



```text

location\_id

```



Used across:

\- inventory tracking

\- shortage reporting

\- shipment receiving

\- future staffing/workforce coordination



\---



\# Future Entity Standards



Future subsystems may introduce:



| Identifier | Expected Purpose |

|---|---|

| employee\_id | Workforce/team member records |

| schedule\_id | Scheduling workflow records |

| department\_id | Department-level reporting |

| process\_id | Process improvement records |

| vendor\_scorecard\_id | Vendor performance evaluation records |



These should follow the same principles:

\- standardized prefix

\- stable identifier

\- clear dataset ownership

\- cross-system usability



\---



\# Data Quality Rules



Datasets should be reviewed for:

\- duplicate IDs

\- missing required fields

\- inconsistent date formats within the same dataset

\- inconsistent boolean values

\- broken shared identifiers

\- unclear status labels

\- mismatched naming conventions



\---



\# Future SQL Readiness



This dictionary supports future SQL work by standardizing:

\- primary keys

\- foreign-key style relationships

\- table naming expectations

\- field naming conventions

\- date normalization planning

\- boolean handling



This will allow future SQL queries to analyze:

\- inventory events tied to tickets

\- vendor shipments tied to shortages

\- discrepancy trends by location

\- SLA failures connected to operational supply issues



\---



\# Future Power BI Readiness



This dictionary supports future Power BI work by clarifying:

\- relationship keys

\- expected model relationships

\- fact-like datasets

\- dimension-like datasets

\- cross-system filter behavior



Future model relationships may include:

\- tickets-v1\[ticket\_id] → shortage-events\[related\_ticket\_id]

\- inventory-items\[item\_id] → location-inventory\[item\_id]

\- inventory-items\[item\_id] → vendor-shipments\[item\_id]

\- vendors\[vendor\_id] → vendor-shipments\[vendor\_id]



\---



\# Governance Rule



If a future subsystem introduces a shared identifier or repeated field concept, it should be added to this data dictionary before the subsystem expands.



This prevents:

\- naming drift

\- relational inconsistency

\- future SQL confusion

\- Power BI model instability

\- ecosystem fragmentation



\---



\# Portfolio Significance



This data dictionary demonstrates:

\- data architecture reasoning

\- relational modeling awareness

\- cross-system integration planning

\- operational data governance

\- SQL readiness

\- Power BI readiness

\- enterprise systems thinking

\- scalable portfolio architecture



This document strengthens the Northstar Health Operations ecosystem by creating a shared relational language across operational domains.

