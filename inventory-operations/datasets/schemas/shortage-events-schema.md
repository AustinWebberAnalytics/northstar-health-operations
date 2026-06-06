\# Shortage Events Schema  



\## Northstar Health Operations



\---



\# Purpose



This document defines the schema for the `shortage-events.csv` dataset within the Inventory Operations subsystem.



The purpose of this schema is to:



\- define operational shortage event tracking fields

\- standardize shortage visibility

\- support operational disruption analysis

\- support replenishment failure analysis

\- support escalation monitoring

\- preserve shared identifier consistency

\- support future SQL integration

\- support future Power BI modeling



This schema serves as the primary reference for operational shortage event records across Northstar Health Operations.



\---



\# Dataset Overview



The `shortage-events.csv` dataset captures operational inventory shortage conditions affecting Northstar Health Operations locations.



This dataset functions as:



\# the operational inventory disruption layer



within the Inventory Operations subsystem.



The dataset is intended to support analysis of:



\- inventory shortage frequency

\- shortage severity

\- operational disruption exposure

\- replenishment instability

\- vendor-supported recovery activity

\- escalation pressure

\- operational continuity risk



\---



\# Dataset Location



```text

inventory-operations/datasets/shortage-events.csv

```



\---



\# Dataset Grain



Each row represents:



\# one operational shortage event



A shortage event may represent:



\- low-stock escalation

\- critical inventory depletion

\- replenishment failure exposure

\- vendor delay impact

\- emergency shortage response activity



The primary identifier for each record is:



```text

shortage\_event\_id

```



\---



\# Primary Key



| Field | Purpose |

|---|---|

| shortage\_event\_id | Unique identifier for each shortage event |



Example:



```text

SHORT-1001

```



\---



\# Foreign Keys and Shared Identifiers



This dataset should use shared identifiers to support cross-system relationships.



| Field | Related Dataset | Purpose |

|---|---|---|

| item\_id | inventory-items.csv | Connects shortage event to inventory item |

| location\_id | location-inventory.csv | Connects shortage event to operational location |

| vendor\_id | vendor-master.csv | Connects shortage event to vendor dependency |

| replenishment\_event\_id | replenishment-events.csv | Connects shortage event to recovery activity |

| related\_ticket\_id | tickets-v1.csv | Connects shortage event to operational escalation |



\---



\# Field Naming Standards



All fields should use:



```text

snake\_case

```



Field names should remain:



\- lowercase

\- business-readable

\- operationally descriptive

\- consistent with enterprise naming standards



Avoid:



```text

ShortageLevel

stockIssue

vendorRef

ticketReference

```



Preferred:



```text

shortage\_severity

inventory\_status

vendor\_id

related\_ticket\_id

```



\---



\# Schema Definition



| Field Name | Data Type | Required | Description |

|---|---|---|---|

| shortage\_event\_id | Text | Yes | Unique shortage event identifier |

| item\_id | Text | Yes | Inventory item associated with the shortage event |

| location\_id | Text | Yes | Operational location affected by the shortage event |

| vendor\_id | Text | No | Vendor associated with shortage recovery or dependency |

| shortage\_detected\_date | Date | Yes | Date shortage condition was identified |

| shortage\_severity | Text | Yes | Operational severity classification |

| inventory\_quantity\_at\_detection | Number | Yes | Inventory quantity when shortage was identified |

| reorder\_threshold | Number | Yes | Reorder threshold at the time of shortage detection |

| operational\_impact\_level | Text | Yes | Operational disruption level associated with the shortage |

| shortage\_status | Text | Yes | Current or final shortage state |

| replenishment\_event\_id | Text | No | Related replenishment recovery event |

| emergency\_replenishment\_flag | Boolean | Yes | Indicates whether emergency replenishment was required |

| escalation\_required\_flag | Boolean | Yes | Indicates whether escalation was required |

| related\_ticket\_id | Text | No | Related operational escalation ticket |

| shortage\_resolved\_flag | Boolean | Yes | Indicates whether the shortage was resolved |

| shortage\_resolution\_date | Date | No | Date the shortage condition was resolved |

| notes | Text | No | Operational notes related to the shortage event |



\---



\# Field Definitions



\---



\## shortage\_event\_id



\### Purpose



Uniquely identifies each operational shortage event.



\### Format



```text

SHORT-####

```



\### Example



```text

SHORT-1001

```



\### Governance Rule



The `shortage\_event\_id` field should remain stable and unique across all shortage records.



\---



\## item\_id



\### Purpose



Identifies the inventory item associated with the shortage event.



\### Format



```text

ITEM-####

```



\### Example



```text

ITEM-1003

```



\### Governance Rule



The `item\_id` field should align with valid inventory item identifiers.



\---



\## location\_id



\### Purpose



Identifies the operational location affected by the shortage event.



\### Format



```text

LOC-\[CITY]-##

```



\### Example



```text

LOC-DURHAM-07

```



\### Governance Rule



Location identifiers should remain standardized across all operational datasets.



\---



\## vendor\_id



\### Purpose



Identifies the vendor associated with shortage recovery dependency or disruption exposure.



\### Format



```text

VEND-###

```



\### Example



```text

VEND-003

```



\### Governance Rule



This field may remain blank when no vendor relationship is directly associated with the shortage condition.



\---



\## shortage\_detected\_date



\### Purpose



Defines the date the shortage condition was identified.



\### Example



```text

2026-05-22

```



\### Governance Rule



Date values should remain internally consistent across operational datasets.



\---



\## shortage\_severity



\### Purpose



Classifies the operational severity of the shortage event.



\### Example Values



```text

Low

Moderate

High

Critical

```



\### Governance Rule



Shortage severity should reflect operational risk, service disruption exposure, or inventory instability.



\---



\## inventory\_quantity\_at\_detection



\### Purpose



Defines the inventory quantity available when the shortage condition was detected.



\### Example



```text

4

```



\### Governance Rule



Inventory quantity values should never be negative.



\---



\## reorder\_threshold



\### Purpose



Defines the reorder threshold active at the time of shortage detection.



\### Example



```text

20

```



\### Governance Rule



Threshold values should align with operational replenishment standards.



\---



\## operational\_impact\_level



\### Purpose



Classifies the operational disruption level associated with the shortage condition.



\### Example Values



```text

Low

Moderate

High

Critical

```



\### Governance Rule



Operational impact should reflect workflow disruption, escalation pressure, or continuity risk.



\---



\## shortage\_status



\### Purpose



Defines the current or final shortage condition.



\### Example Values



```text

Open

Monitoring

Resolved

Escalated

```



\### Governance Rule



Shortage status values should remain standardized and operationally meaningful.



\---



\## replenishment\_event\_id



\### Purpose



Connects shortage activity to replenishment recovery efforts.



\### Format



```text

REP-####

```



\### Example



```text

REP-1002

```



\### Governance Rule



This field may remain blank if replenishment recovery has not yet occurred.



\---



\## emergency\_replenishment\_flag



\### Purpose



Indicates whether emergency replenishment activity was required.



\### Format



```text

TRUE

FALSE

```



\---



\## escalation\_required\_flag



\### Purpose



Indicates whether operational escalation was required.



\### Format



```text

TRUE

FALSE

```



\---



\## related\_ticket\_id



\### Purpose



Connects the shortage event to operational ticketing activity.



\### Format



```text

INC-######

```



\### Example



```text

INC-100012

```



\### Governance Rule



This field may remain blank if no escalation ticket exists.



\---



\## shortage\_resolved\_flag



\### Purpose



Indicates whether the shortage condition has been resolved.



\### Format



```text

TRUE

FALSE

```



\---



\## shortage\_resolution\_date



\### Purpose



Defines the date the shortage condition was resolved.



\### Example



```text

2026-05-24

```



\### Governance Rule



This field may remain blank if the shortage remains unresolved.



\---



\## notes



\### Purpose



Provides optional operational context related to the shortage event.



\### Example



```text

Delayed specialty shipment increased operational shortage exposure for procedure readiness.

```



\### Governance Rule



Notes should remain concise and operationally relevant.



\---



\# Required Fields



The following fields are required:



```text

shortage\_event\_id

item\_id

location\_id

shortage\_detected\_date

shortage\_severity

inventory\_quantity\_at\_detection

reorder\_threshold

operational\_impact\_level

shortage\_status

emergency\_replenishment\_flag

escalation\_required\_flag

shortage\_resolved\_flag

```



Optional fields include:



```text

vendor\_id

replenishment\_event\_id

related\_ticket\_id

shortage\_resolution\_date

notes

```



\---



\# Boolean Standards



Boolean fields should use:



```text

TRUE

FALSE

```



Boolean fields in this dataset include:



```text

emergency\_replenishment\_flag

escalation\_required\_flag

shortage\_resolved\_flag

```



Avoid:



```text

Yes

No

Y

N

1

0

```



\---



\# Status and Classification Standards



Status and classification fields should use business-readable values.



Examples:



```text

Low

Moderate

High

Critical



Open

Monitoring

Resolved

Escalated

```



Status and classification values should remain:



\- consistent

\- readable

\- operationally meaningful

\- reporting-friendly



\---



\# Relationship Standards



The `shortage-events.csv` dataset is expected to connect to operational inventory and replenishment activity through:



```text

item\_id

location\_id

vendor\_id

replenishment\_event\_id

related\_ticket\_id

```



Expected relationships may include:



```text

inventory-items\[item\_id] → shortage-events\[item\_id]

location-inventory\[location\_id] → shortage-events\[location\_id]

vendor-master\[vendor\_id] → shortage-events\[vendor\_id]

replenishment-events\[replenishment\_event\_id] → shortage-events\[replenishment\_event\_id]

tickets-v1\[ticket\_id] → shortage-events\[related\_ticket\_id]

```



\---



\# Cross-System Usage



The `shortage-events.csv` dataset may connect shortage activity to:



\- replenishment recovery

\- vendor fulfillment disruption

\- operational escalation activity

\- delayed shipment exposure

\- emergency operational support

\- executive reporting summaries



This supports:



\- shortage trend monitoring

\- replenishment recovery analysis

\- operational disruption visibility

\- escalation pressure analysis

\- inventory continuity reporting



\---



\# Data Quality Rules



The `shortage-events.csv` dataset should be reviewed for:



\- duplicate `shortage\_event\_id` values

\- missing required fields

\- invalid item references

\- invalid vendor references

\- invalid replenishment references

\- inconsistent boolean values

\- negative inventory quantities

\- resolved shortages missing resolution dates

\- escalated shortages missing ticket references



Each `shortage\_event\_id` should remain unique and stable.



\---



\# Future SQL Readiness



This schema supports future SQL integration by defining:



\- stable shortage event keys

\- inventory disruption relationships

\- replenishment recovery relationships

\- escalation-aware operational modeling

\- vendor dependency visibility



Future SQL queries may use this dataset to analyze:



\- shortage frequency

\- shortage severity trends

\- replenishment recovery timelines

\- escalation-driven shortages

\- vendor-linked shortage exposure

\- operational continuity risk



\---



\# Future Power BI Readiness



This schema supports future Power BI modeling by functioning as an operational shortage event fact table.



Potential model relationships include:



```text

inventory-items\[item\_id] → shortage-events\[item\_id]

location-inventory\[location\_id] → shortage-events\[location\_id]

replenishment-events\[replenishment\_event\_id] → shortage-events\[replenishment\_event\_id]

```



This supports reporting by:



\- shortage severity

\- operational location

\- inventory item

\- escalation activity

\- replenishment recovery

\- operational disruption exposure



\---



\# Governance Alignment



This schema follows established Northstar governance standards, including:



\- subsystem-centered architecture

\- naming convention standards

\- shared identifier standards

\- dataset governance standards

\- cross-system relational planning

\- SQL readiness

\- Power BI readiness



Future changes to this schema should be made:



\# systematically



NOT:



\# reactively.



\---



\# Portfolio Significance



This schema demonstrates:



\- operational shortage modeling

\- inventory disruption analysis

\- replenishment recovery architecture

\- escalation-aware systems thinking

\- relational data governance

\- SQL readiness awareness

\- Power BI modeling awareness

\- scalable operational subsystem construction



The `shortage-events.csv` schema strengthens the Inventory Operations subsystem by establishing a standardized operational shortage event layer supporting disruption monitoring, replenishment recovery analysis, escalation visibility, and operational continuity reporting.

