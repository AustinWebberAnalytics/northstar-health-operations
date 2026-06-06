\# Replenishment Events Schema  



\## Northstar Health Operations



\---



\# Purpose



This document defines the schema for the `replenishment-events.csv` dataset within the Inventory Operations subsystem.



The purpose of this schema is to:



\- define replenishment event tracking fields

\- standardize inventory replenishment activity

\- support operational inventory recovery analysis

\- support shortage prevention monitoring

\- preserve shared identifier consistency

\- support vendor fulfillment relationships

\- support future SQL integration

\- support future Power BI modeling



This schema serves as the primary reference for replenishment event records across Northstar Health Operations.



\---



\# Dataset Overview



The `replenishment-events.csv` dataset captures operational inventory replenishment activity across locations and inventory items.



This dataset functions as:



\# the inventory replenishment movement layer



within the Inventory Operations subsystem.



The dataset is intended to support analysis of:



\- replenishment timing

\- inventory stabilization

\- vendor-supported inventory recovery

\- shortage prevention

\- replenishment delays

\- operational supply continuity

\- replenishment workload trends



\---



\# Dataset Location



```text

inventory-operations/datasets/replenishment-events.csv

```



\---



\# Dataset Grain



Each row represents:



\# one replenishment event



A replenishment event may represent:



\- routine replenishment

\- emergency replenishment

\- shortage recovery replenishment

\- vendor-supported replenishment

\- inventory stabilization activity



The primary identifier for each record is:



```text

replenishment\_event\_id

```



\---



\# Primary Key



| Field | Purpose |

|---|---|

| replenishment\_event\_id | Unique identifier for each replenishment event |



Example:



```text

REP-1001

```



\---



\# Foreign Keys and Shared Identifiers



This dataset should use shared identifiers to support cross-system relationships.



| Field | Related Dataset | Purpose |

|---|---|---|

| item\_id | inventory-items.csv | Connects replenishment event to inventory item |

| location\_id | location-inventory.csv | Connects replenishment event to operational location |

| vendor\_id | vendor-master.csv | Connects replenishment event to supporting vendor |

| shipment\_id | vendor shipment records | Connects replenishment activity to shipment events |

| related\_ticket\_id | tickets-v1.csv | Connects replenishment event to escalation or shortage tickets |



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

RestockDate

itemQty

vendorRef

ticketReference

```



Preferred:



```text

replenishment\_date

replenishment\_quantity

vendor\_id

related\_ticket\_id

```



\---



\# Schema Definition



| Field Name | Data Type | Required | Description |

|---|---|---|---|

| replenishment\_event\_id | Text | Yes | Unique replenishment event identifier |

| item\_id | Text | Yes | Inventory item associated with the replenishment event |

| location\_id | Text | Yes | Operational location receiving replenishment |

| vendor\_id | Text | Yes | Vendor supporting the replenishment event |

| shipment\_id | Text | No | Shipment identifier associated with replenishment activity |

| replenishment\_date | Date | Yes | Date replenishment activity occurred |

| replenishment\_type | Text | Yes | Operational classification of replenishment activity |

| replenishment\_quantity | Number | Yes | Quantity added during replenishment |

| replenishment\_status | Text | Yes | Current or final replenishment outcome |

| emergency\_replenishment\_flag | Boolean | Yes | Indicates whether replenishment was emergency-driven |

| shortage\_recovery\_flag | Boolean | Yes | Indicates whether replenishment supported shortage recovery |

| replenishment\_delay\_flag | Boolean | Yes | Indicates whether replenishment activity was delayed |

| operational\_impact\_level | Text | Yes | Operational severity associated with replenishment activity |

| related\_ticket\_id | Text | No | Related operational escalation or shortage ticket |

| notes | Text | No | Operational notes related to replenishment activity |



\---



\# Field Definitions



\---



\## replenishment\_event\_id



\### Purpose



Uniquely identifies each replenishment event.



\### Format



```text

REP-####

```



\### Example



```text

REP-1001

```



\### Governance Rule



The `replenishment\_event\_id` field should remain stable and unique across all replenishment records.



\---



\## item\_id



\### Purpose



Identifies the inventory item associated with the replenishment event.



\### Format



```text

ITEM-####

```



\### Example



```text

ITEM-1002

```



\### Governance Rule



The `item\_id` field should align with valid inventory items defined in:



```text

inventory-items.csv

```



\---



\## location\_id



\### Purpose



Identifies the operational location receiving replenishment inventory.



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



Identifies the vendor supporting the replenishment event.



\### Format



```text

VEND-###

```



\### Example



```text

VEND-001

```



\### Governance Rule



Vendor references should align with valid vendor identifiers where vendor master data exists.



\---



\## shipment\_id



\### Purpose



Identifies the shipment associated with replenishment activity.



\### Format



```text

SHIP-####

```



\### Example



```text

SHIP-1005

```



\### Governance Rule



This field may remain blank when replenishment activity is not directly tied to a shipment event.



\---



\## replenishment\_date



\### Purpose



Defines the date replenishment activity occurred.



\### Example



```text

2026-05-21

```



\### Governance Rule



Date values should remain internally consistent across operational datasets.



\---



\## replenishment\_type



\### Purpose



Classifies the operational replenishment activity.



\### Example Values



```text

Routine Replenishment

Emergency Replenishment

Shortage Recovery

Vendor Stabilization

```



\### Governance Rule



Replenishment types should remain operationally meaningful and business-readable.



\---



\## replenishment\_quantity



\### Purpose



Defines the quantity added during replenishment activity.



\### Example



```text

50

```



\### Governance Rule



Replenishment quantities should never be negative.



\---



\## replenishment\_status



\### Purpose



Describes the replenishment outcome.



\### Example Values



```text

Completed

Pending

Delayed

Cancelled

```



\### Governance Rule



Replenishment status values should remain standardized across the dataset.



\---



\## emergency\_replenishment\_flag



\### Purpose



Indicates whether replenishment activity was emergency-driven.



\### Format



```text

TRUE

FALSE

```



\---



\## shortage\_recovery\_flag



\### Purpose



Indicates whether replenishment activity supported operational shortage recovery.



\### Format



```text

TRUE

FALSE

```



\---



\## replenishment\_delay\_flag



\### Purpose



Indicates whether replenishment activity was delayed.



\### Format



```text

TRUE

FALSE

```



\---



\## operational\_impact\_level



\### Purpose



Classifies the operational impact associated with replenishment activity.



\### Example Values



```text

Low

Moderate

High

Critical

```



\### Governance Rule



Operational impact should reflect replenishment urgency, shortage exposure, escalation pressure, or operational continuity risk.



\---



\## related\_ticket\_id



\### Purpose



Connects replenishment activity to operational tickets when applicable.



\### Format



```text

INC-######

```



\### Example



```text

INC-100012

```



\### Governance Rule



This field may remain blank when no escalation relationship exists.



\---



\## notes



\### Purpose



Provides optional operational context related to replenishment activity.



\### Example



```text

Emergency replenishment initiated following delayed specialty shipment.

```



\### Governance Rule



Notes should remain concise and operationally relevant.



\---



\# Required Fields



The following fields are required:



```text

replenishment\_event\_id

item\_id

location\_id

vendor\_id

replenishment\_date

replenishment\_type

replenishment\_quantity

replenishment\_status

emergency\_replenishment\_flag

shortage\_recovery\_flag

replenishment\_delay\_flag

operational\_impact\_level

```



Optional fields include:



```text

shipment\_id

related\_ticket\_id

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

shortage\_recovery\_flag

replenishment\_delay\_flag

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

Routine Replenishment

Emergency Replenishment

Shortage Recovery

Vendor Stabilization



Completed

Pending

Delayed

Cancelled



Low

Moderate

High

Critical

```



Status and classification values should remain:



\- consistent

\- readable

\- operationally meaningful

\- reporting-friendly



\---



\# Relationship Standards



The `replenishment-events.csv` dataset is expected to connect to operational inventory and vendor activity through:



```text

item\_id

location\_id

vendor\_id

shipment\_id

related\_ticket\_id

```



Expected relationships may include:



```text

inventory-items\[item\_id] → replenishment-events\[item\_id]

location-inventory\[location\_id] → replenishment-events\[location\_id]

vendor-master\[vendor\_id] → replenishment-events\[vendor\_id]

vendor-fulfillment-events\[shipment\_id] → replenishment-events\[shipment\_id]

tickets-v1\[ticket\_id] → replenishment-events\[related\_ticket\_id]

```



\---



\# Cross-System Usage



The `replenishment-events.csv` dataset may connect replenishment activity to:



\- inventory stabilization

\- shortage recovery

\- vendor shipment activity

\- operational escalations

\- delayed fulfillment activity

\- emergency operational support

\- executive reporting summaries



This supports:



\- replenishment workload analysis

\- shortage recovery monitoring

\- vendor dependency visibility

\- operational continuity analysis

\- inventory recovery reporting



\---



\# Data Quality Rules



The `replenishment-events.csv` dataset should be reviewed for:



\- duplicate `replenishment\_event\_id` values

\- missing required fields

\- invalid item references

\- invalid vendor references

\- invalid location references

\- inconsistent boolean values

\- negative replenishment quantities

\- delayed replenishment events missing operational notes

\- escalation-linked replenishment events missing ticket references



Each `replenishment\_event\_id` should remain unique and stable.



\---



\# Future SQL Readiness



This schema supports future SQL integration by defining:



\- stable replenishment event keys

\- cross-system relational identifiers

\- replenishment event granularity

\- vendor-supported replenishment relationships

\- operational inventory recovery modeling



Future SQL queries may use this dataset to analyze:



\- replenishment frequency

\- replenishment delays

\- shortage recovery timelines

\- emergency replenishment trends

\- replenishment workload by location

\- vendor-supported inventory stabilization



\---



\# Future Power BI Readiness



This schema supports future Power BI modeling by functioning as a replenishment event fact table.



Potential model relationships include:



```text

inventory-items\[item\_id] → replenishment-events\[item\_id]

location-inventory\[location\_id] → replenishment-events\[location\_id]

vendor-master\[vendor\_id] → replenishment-events\[vendor\_id]

```



This supports reporting by:



\- replenishment type

\- operational location

\- inventory item

\- vendor

\- operational impact level

\- emergency replenishment activity

\- shortage recovery activity



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



\- operational replenishment modeling

\- inventory recovery workflow design

\- vendor-supported replenishment analysis

\- relational data governance

\- SQL readiness awareness

\- Power BI modeling awareness

\- enterprise systems thinking

\- scalable operational subsystem construction



The `replenishment-events.csv` schema strengthens the Inventory Operations subsystem by establishing a standardized replenishment event layer supporting inventory stabilization, shortage recovery analysis, vendor dependency visibility, and operational continuity reporting.

