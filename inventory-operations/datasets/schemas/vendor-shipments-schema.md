\# Vendor Shipments Schema  



\## Northstar Health Operations



\---



\# Purpose



This document defines the schema for the `vendor-shipments.csv` dataset within the Inventory Operations subsystem.



The purpose of this schema is to:



\- define vendor shipment tracking fields

\- standardize inbound shipment monitoring

\- support vendor delivery analysis

\- support replenishment visibility

\- preserve shared identifier consistency

\- support inventory continuity monitoring

\- support future SQL integration

\- support future Power BI modeling



This schema serves as the primary reference for vendor shipment records within the Inventory Operations subsystem.



\---



\# Dataset Overview



The `vendor-shipments.csv` dataset captures inbound vendor shipment activity connected to inventory operations.



This dataset functions as:



\# the inbound vendor shipment tracking layer



within the Inventory Operations subsystem.



The dataset is intended to support analysis of:



\- shipment delivery status

\- inbound supply movement

\- delayed shipment activity

\- partial fulfillment risk

\- replenishment dependency

\- vendor shipment reliability

\- inventory continuity exposure



\---



\# Dataset Location



```text

inventory-operations/datasets/vendor-shipments.csv

```



\---



\# Dataset Grain



Each row represents:



\# one vendor shipment record



A vendor shipment record may represent:



\- completed inbound shipment

\- delayed shipment

\- pending shipment

\- partial shipment

\- vendor-supported replenishment activity



The primary identifier for each record is:



```text

shipment\_id

```



\---



\# Primary Key



| Field | Purpose |

|---|---|

| shipment\_id | Unique identifier for each vendor shipment |



Example:



```text

SHIP-1001

```



\---



\# Foreign Keys and Shared Identifiers



This dataset should use shared identifiers to support cross-system relationships.



| Field | Related Dataset | Purpose |

|---|---|---|

| vendor\_id | vendor-master.csv | Connects shipment record to vendor identity |

| item\_id | inventory-items.csv | Connects shipment record to inventory item |

| location\_id | location-inventory.csv | Connects shipment record to receiving location |

| related\_ticket\_id | tickets-v1.csv | Connects shipment record to operational escalation when applicable |



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

ShipmentID

VendorID

arrivalDate

ticketReference

```



Preferred:



```text

shipment\_id

vendor\_id

expected\_arrival\_date

related\_ticket\_id

```



\---



\# Schema Definition



| Field Name | Data Type | Required | Description |

|---|---|---|---|

| shipment\_id | Text | Yes | Unique shipment identifier |

| vendor\_id | Text | Yes | Vendor associated with the shipment |

| item\_id | Text | Yes | Inventory item associated with the shipment |

| location\_id | Text | Yes | Operational location receiving the shipment |

| shipment\_date | Date | Yes | Date shipment was sent or initiated |

| expected\_arrival\_date | Date | Yes | Expected shipment arrival date |

| actual\_arrival\_date | Date | No | Actual shipment arrival date, if received |

| shipment\_status | Text | Yes | Current or final shipment status |

| expected\_quantity | Number | Yes | Quantity expected in the shipment |

| received\_quantity | Number | Yes | Quantity received from the shipment |

| delay\_flag | Boolean | Yes | Indicates whether shipment was delayed |

| partial\_shipment\_flag | Boolean | Yes | Indicates whether shipment was partially received |

| operational\_impact\_level | Text | Yes | Operational impact associated with the shipment |

| escalation\_required\_flag | Boolean | Yes | Indicates whether escalation was required |

| related\_ticket\_id | Text | No | Related operational ticket identifier |

| notes | Text | No | Operational notes related to the shipment |



\---



\# Field Definitions



\---



\## shipment\_id



\### Purpose



Uniquely identifies each vendor shipment.



\### Format



```text

SHIP-####

```



\### Example



```text

SHIP-1001

```



\### Governance Rule



The `shipment\_id` field should remain stable and unique across all vendor shipment records.



\---



\## vendor\_id



\### Purpose



Identifies the vendor associated with the shipment.



\### Format



```text

VEND-###

```



\### Example



```text

VEND-003

```



\### Governance Rule



The `vendor\_id` field should align with valid vendor identifiers where vendor master data exists.



\---



\## item\_id



\### Purpose



Identifies the inventory item associated with the shipment.



\### Format



```text

ITEM-####

```



\### Example



```text

ITEM-1002

```



\### Governance Rule



The `item\_id` field should align with valid inventory item identifiers.



\---



\## location\_id



\### Purpose



Identifies the operational location receiving the shipment.



\### Format



```text

LOC-\[CITY]-##

```



\### Example



```text

LOC-RALEIGH-03

```



\### Governance Rule



Location identifiers should remain standardized across all operational datasets.



\---



\## shipment\_date



\### Purpose



Defines the date the shipment was sent or initiated.



\### Example



```text

2026-05-21

```



\### Governance Rule



Date values should remain internally consistent across the dataset.



\---



\## expected\_arrival\_date



\### Purpose



Defines the expected arrival date for the shipment.



\### Example



```text

2026-05-23

```



\---



\## actual\_arrival\_date



\### Purpose



Defines the actual arrival date for the shipment.



\### Example



```text

2026-05-24

```



\### Governance Rule



This field may remain blank when the shipment is pending or unresolved.



\---



\## shipment\_status



\### Purpose



Defines the current or final shipment condition.



\### Example Values



```text

Delivered

Delayed

Pending

Cancelled

Failed

```



\### Governance Rule



Shipment status values should remain standardized and operationally meaningful.



\---



\## expected\_quantity



\### Purpose



Defines the expected quantity for the shipment.



\### Example



```text

75

```



\### Governance Rule



Expected quantities should not be negative.



\---



\## received\_quantity



\### Purpose



Defines the quantity received from the shipment.



\### Example



```text

60

```



\### Governance Rule



If the shipment is pending and no quantity has been received, this value should be:



```text

0

```



\---



\## delay\_flag



\### Purpose



Indicates whether the shipment was delayed.



\### Format



```text

TRUE

FALSE

```



\---



\## partial\_shipment\_flag



\### Purpose



Indicates whether the shipment was partially received.



\### Format



```text

TRUE

FALSE

```



\---



\## operational\_impact\_level



\### Purpose



Classifies the operational impact associated with the shipment.



\### Example Values



```text

Low

Moderate

High

Critical

```



\### Governance Rule



Operational impact should reflect inventory dependency, shortage exposure, escalation pressure, or continuity risk.



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



Connects shipment activity to operational tickets when applicable.



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



Provides optional operational context related to the shipment.



\### Example



```text

Delayed shipment increased shortage exposure at Durham location.

```



\### Governance Rule



Notes should remain concise and operationally relevant.



\---



\# Required Fields



The following fields are required:



```text

shipment\_id

vendor\_id

item\_id

location\_id

shipment\_date

expected\_arrival\_date

shipment\_status

expected\_quantity

received\_quantity

delay\_flag

partial\_shipment\_flag

operational\_impact\_level

escalation\_required\_flag

```



Optional fields include:



```text

actual\_arrival\_date

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

delay\_flag

partial\_shipment\_flag

escalation\_required\_flag

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

Delivered

Delayed

Pending

Cancelled

Failed



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



The `vendor-shipments.csv` dataset is expected to connect to inventory, vendor, and ticket activity through:



```text

shipment\_id

vendor\_id

item\_id

location\_id

related\_ticket\_id

```



Expected relationships may include:



```text

vendor-master\[vendor\_id] → vendor-shipments\[vendor\_id]

inventory-items\[item\_id] → vendor-shipments\[item\_id]

location-inventory\[location\_id] → vendor-shipments\[location\_id]

tickets-v1\[ticket\_id] → vendor-shipments\[related\_ticket\_id]

vendor-shipments\[shipment\_id] → vendor-fulfillment-events\[shipment\_id]

```



\---



\# Cross-System Usage



The `vendor-shipments.csv` dataset may connect shipment activity to:



\- vendor performance records

\- inventory item records

\- operational location records

\- replenishment activity

\- shortage exposure

\- discrepancy investigations

\- operational escalation activity



This supports:



\- shipment reliability analysis

\- vendor delivery monitoring

\- replenishment dependency visibility

\- delayed shipment tracking

\- operational disruption reporting

\- leadership inventory risk summaries



\---



\# Data Quality Rules



The `vendor-shipments.csv` dataset should be reviewed for:



\- duplicate `shipment\_id` values

\- missing required fields

\- invalid vendor references

\- invalid item references

\- invalid location references

\- inconsistent boolean values

\- negative quantity values

\- pending shipments with received quantities greater than zero unless operationally justified

\- delivered shipments missing actual arrival dates

\- escalated shipments missing ticket references



Each `shipment\_id` should remain unique and stable.



\---



\# Future SQL Readiness



This schema supports future SQL integration by defining:



\- stable shipment event keys

\- vendor shipment relationships

\- inventory item relationships

\- location-based receiving activity

\- escalation-aware shipment modeling

\- cross-system shipment references



Future SQL queries may use this dataset to analyze:



\- shipment delay frequency

\- partial shipment frequency

\- delivery performance by vendor

\- shipment impact by location

\- shipment-related escalation activity

\- vendor shipment reliability trends



\---



\# Future Power BI Readiness



This schema supports future Power BI modeling by functioning as an inbound shipment fact table.



Potential model relationships include:



```text

vendor-master\[vendor\_id] → vendor-shipments\[vendor\_id]

inventory-items\[item\_id] → vendor-shipments\[item\_id]

location-inventory\[location\_id] → vendor-shipments\[location\_id]

vendor-shipments\[shipment\_id] → vendor-fulfillment-events\[shipment\_id]

```



This supports reporting by:



\- vendor

\- shipment status

\- operational location

\- inventory item

\- delay status

\- partial shipment activity

\- operational impact level

\- escalation requirement



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



\- vendor shipment modeling

\- inbound logistics tracking

\- inventory replenishment dependency analysis

\- escalation-aware systems thinking

\- relational data governance

\- SQL readiness awareness

\- Power BI modeling awareness

\- scalable operational subsystem construction



The `vendor-shipments.csv` schema strengthens the Inventory Operations subsystem by establishing a standardized inbound shipment layer supporting inventory continuity, vendor reliability monitoring, replenishment visibility, and operational disruption analysis.

