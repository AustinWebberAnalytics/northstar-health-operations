\# Vendor Fulfillment Events Schema  



\## Northstar Health Operations



\---



\# Purpose



This document defines the schema for the `vendor-fulfillment-events.csv` dataset within the Vendor Performance subsystem.



The purpose of this schema is to:



\- define vendor fulfillment event fields

\- standardize shipment and delivery tracking

\- support fulfillment reliability analysis

\- monitor shipment delays and partial fulfillment

\- preserve shared identifier consistency

\- support cross-system operational reporting

\- support future SQL integration

\- support future Power BI modeling



This schema serves as the primary reference for vendor fulfillment event records.



\---



\# Dataset Overview



The `vendor-fulfillment-events.csv` dataset captures vendor shipment and fulfillment activity across Northstar Health Operations.



This dataset functions as:



\# the transactional fulfillment event layer



within the Vendor Performance subsystem.



The dataset is intended to support analysis of:



\- on-time delivery performance

\- fulfillment accuracy

\- partial shipment activity

\- shipment delay frequency

\- vendor reliability

\- operational disruption exposure

\- inventory replenishment stability



\---



\# Dataset Location



```text

vendor-performance/datasets/vendor-fulfillment-events.csv

```



\---



\# Dataset Grain



Each row represents:



\# one vendor fulfillment event



A fulfillment event may represent:



\- a completed shipment

\- a delayed shipment

\- a partially fulfilled shipment

\- a failed fulfillment event

\- an emergency fulfillment event



The primary identifier for each record is:



```text

fulfillment\_event\_id

```



\---



\# Primary Key



| Field | Purpose |

|---|---|

| fulfillment\_event\_id | Unique identifier for each vendor fulfillment event |



Example:



```text

VF-1001

```



\---



\# Foreign Keys and Shared Identifiers



This dataset should use shared identifiers to support cross-system relationships.



| Field | Related Dataset | Purpose |

|---|---|---|

| vendor\_id | vendor-master.csv | Connects fulfillment event to vendor record |

| shipment\_id | vendor shipment records / future shipment tracking | Connects event to shipment activity |

| item\_id | inventory-items.csv | Connects event to inventory item |

| location\_id | location inventory / operational locations | Connects event to impacted location |

| related\_ticket\_id | tickets-v1.csv | Connects event to operational ticket when applicable |



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

VendorID

ShipmentDate

deliveryStatus

ticketRef

```



Preferred:



```text

vendor\_id

shipment\_id

expected\_delivery\_date

delivery\_status

related\_ticket\_id

```



\---



\# Schema Definition



| Field Name | Data Type | Required | Description |

|---|---|---|---|

| fulfillment\_event\_id | Text | Yes | Unique identifier for each vendor fulfillment event |

| vendor\_id | Text | Yes | Vendor associated with the fulfillment event |

| shipment\_id | Text | Yes | Shipment identifier connected to the fulfillment event |

| item\_id | Text | Yes | Inventory item associated with the fulfillment event |

| location\_id | Text | Yes | Operational location affected by the fulfillment event |

| order\_date | Date | Yes | Date the vendor order or fulfillment request was initiated |

| expected\_delivery\_date | Date | Yes | Expected delivery date for the shipment |

| actual\_delivery\_date | Date | No | Actual delivery date, if delivered |

| delivery\_status | Text | Yes | Current or final delivery outcome |

| fulfillment\_status | Text | Yes | Fulfillment completeness status |

| expected\_quantity | Number | Yes | Quantity expected from the vendor |

| received\_quantity | Number | Yes | Quantity actually received |

| fulfillment\_accuracy\_flag | Boolean | Yes | Indicates whether fulfillment matched expectation |

| delay\_flag | Boolean | Yes | Indicates whether delivery was delayed |

| delay\_days | Number | Yes | Number of calendar days delayed |

| partial\_fulfillment\_flag | Boolean | Yes | Indicates whether shipment was partially fulfilled |

| emergency\_fulfillment\_flag | Boolean | Yes | Indicates whether the event involved emergency fulfillment |

| operational\_impact\_level | Text | Yes | Operational severity of the fulfillment event |

| escalation\_required\_flag | Boolean | Yes | Indicates whether escalation was required |

| related\_ticket\_id | Text | No | Related operational ticket identifier, if applicable |

| notes | Text | No | Operational notes related to the fulfillment event |



\---



\# Field Definitions



\---



\## fulfillment\_event\_id



\### Purpose



Uniquely identifies each vendor fulfillment event.



\### Format



```text

VF-####

```



\### Example



```text

VF-1001

```



\### Governance Rule



The `fulfillment\_event\_id` field should remain stable and unique across all vendor fulfillment records.



\---



\## vendor\_id



\### Purpose



Identifies the vendor associated with the fulfillment event.



\### Format



```text

VEND-###

```



\### Example



```text

VEND-003

```



\### Governance Rule



The `vendor\_id` field should match a valid vendor in:



```text

vendor-master.csv

```



\---



\## shipment\_id



\### Purpose



Identifies the shipment associated with the fulfillment event.



\### Format



```text

SHIP-####

```



\### Example



```text

SHIP-1002

```



\### Governance Rule



The `shipment\_id` field should remain stable across fulfillment, shipment, and future logistics records.



\---



\## item\_id



\### Purpose



Identifies the inventory item associated with the fulfillment event.



\### Format



```text

ITEM-####

```



\### Example



```text

ITEM-1003

```



\### Governance Rule



The `item\_id` field should align with established inventory item identifiers.



\---



\## location\_id



\### Purpose



Identifies the operational location affected by the fulfillment event.



\### Format



```text

LOC-\[LOCATION]-##

```



\### Example



```text

LOC-DURHAM-07

```



\### Governance Rule



The `location\_id` field should align with established operational location identifiers.



\---



\## order\_date



\### Purpose



Identifies the date the vendor order or fulfillment request was initiated.



\### Example



```text

2026-05-01

```



\### Governance Rule



Date values should remain internally consistent within the dataset.



\---



\## expected\_delivery\_date



\### Purpose



Identifies the expected delivery date for the fulfillment event.



\### Example



```text

2026-05-04

```



\---



\## actual\_delivery\_date



\### Purpose



Identifies the actual date the shipment was delivered.



\### Example



```text

2026-05-06

```



\### Governance Rule



This field may remain blank when the shipment is still pending or unresolved.



\---



\## delivery\_status



\### Purpose



Describes the delivery outcome of the fulfillment event.



\### Example Values



```text

Delivered

Delayed

Pending

Cancelled

Failed

```



\### Governance Rule



Delivery status values should remain consistent and business-readable.



\---



\## fulfillment\_status



\### Purpose



Describes whether the expected fulfillment was complete.



\### Example Values



```text

Complete

Partial

Not Fulfilled

Pending

```



\### Governance Rule



Fulfillment status values should remain consistent and operationally meaningful.



\---



\## expected\_quantity



\### Purpose



Defines the quantity expected from the vendor.



\### Example



```text

120

```



\---



\## received\_quantity



\### Purpose



Defines the quantity actually received from the vendor.



\### Example



```text

90

```



\### Governance Rule



If fulfillment is pending and no quantity has been received, this value should be:



```text

0

```



\---



\## fulfillment\_accuracy\_flag



\### Purpose



Indicates whether received fulfillment matched expected fulfillment.



\### Format



```text

TRUE

FALSE

```



\### Governance Rule



This field should be `TRUE` only when the expected item and expected quantity were fulfilled correctly.



\---



\## delay\_flag



\### Purpose



Indicates whether the fulfillment event was delayed.



\### Format



```text

TRUE

FALSE

```



\---



\## delay\_days



\### Purpose



Tracks the number of calendar days between expected delivery and actual delivery or current unresolved delay.



\### Example



```text

2

```



\### Governance Rule



If no delay occurred, this value should be:



```text

0

```



\---



\## partial\_fulfillment\_flag



\### Purpose



Indicates whether the fulfillment event was only partially fulfilled.



\### Format



```text

TRUE

FALSE

```



\---



\## emergency\_fulfillment\_flag



\### Purpose



Indicates whether the event involved emergency fulfillment.



\### Format



```text

TRUE

FALSE

```



\---



\## operational\_impact\_level



\### Purpose



Classifies the operational impact of the fulfillment event.



\### Example Values



```text

Low

Moderate

High

Critical

```



\### Governance Rule



Operational impact level should reflect workflow disruption, shortage exposure, escalation pressure, or service continuity risk.



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



Connects the fulfillment event to an operational ticket when applicable.



\### Format



```text

INC-######

```



\### Example



```text

INC-100012

```



\### Governance Rule



This field should remain blank when no ticket relationship exists.



\---



\## notes



\### Purpose



Provides optional operational context about the fulfillment event.



\### Example



```text

Partial shipment increased shortage pressure at Durham location.

```



\### Governance Rule



Notes should remain concise and operationally relevant.



\---



\# Required Fields



The following fields are required:



```text

fulfillment\_event\_id

vendor\_id

shipment\_id

item\_id

location\_id

order\_date

expected\_delivery\_date

delivery\_status

fulfillment\_status

expected\_quantity

received\_quantity

fulfillment\_accuracy\_flag

delay\_flag

delay\_days

partial\_fulfillment\_flag

emergency\_fulfillment\_flag

operational\_impact\_level

escalation\_required\_flag

```



Optional fields include:



```text

actual\_delivery\_date

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

fulfillment\_accuracy\_flag

delay\_flag

partial\_fulfillment\_flag

emergency\_fulfillment\_flag

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



Status fields should use business-readable values.



Delivery status examples:



```text

Delivered

Delayed

Pending

Cancelled

Failed

```



Fulfillment status examples:



```text

Complete

Partial

Not Fulfilled

Pending

```



Operational impact examples:



```text

Low

Moderate

High

Critical

```



Status and classification fields should remain:



\- consistent

\- readable

\- operationally meaningful

\- reporting-friendly



\---



\# Relationship Standards



The `vendor-fulfillment-events.csv` dataset is expected to connect to vendor records through:



```text

vendor\_id

```



Expected relationships may include:



```text

vendor-master\[vendor\_id] → vendor-fulfillment-events\[vendor\_id]

vendor-fulfillment-events\[related\_ticket\_id] → tickets-v1\[ticket\_id]

vendor-fulfillment-events\[item\_id] → inventory-items\[item\_id]

vendor-fulfillment-events\[location\_id] → location-inventory\[location\_id]

```



\---



\# Cross-System Usage



Vendor fulfillment records may connect to:



\- vendor master records

\- inventory item records

\- operational location records

\- ticketing records

\- replenishment activity

\- shortage events

\- executive reporting summaries



This supports:



\- fulfillment reliability analysis

\- vendor delay monitoring

\- shortage escalation visibility

\- operational disruption reporting

\- leadership vendor performance review



\---



\# Data Quality Rules



The `vendor-fulfillment-events.csv` dataset should be reviewed for:



\- duplicate `fulfillment\_event\_id` values

\- missing required fields

\- invalid `vendor\_id` values

\- invalid `item\_id` values

\- invalid `location\_id` values

\- inconsistent boolean values

\- negative quantity values

\- delay values inconsistent with date fields

\- partial fulfillment flags inconsistent with quantity values

\- missing ticket references for escalated high-impact events



Each `fulfillment\_event\_id` should be unique and stable.



\---



\# Future SQL Readiness



This schema supports future SQL integration by defining:



\- stable primary keys

\- foreign-key style relationships

\- shipment-level event granularity

\- consistent boolean fields

\- measurable fulfillment outcomes

\- operational impact classifications



Future SQL queries may use this dataset to analyze:



\- on-time delivery rate

\- partial fulfillment rate

\- vendor delay frequency

\- average shipment delay duration

\- escalation contribution by vendor

\- fulfillment accuracy by vendor

\- operational impact by location



\---



\# Future Power BI Readiness



This schema supports future Power BI modeling by functioning as a transactional event table.



Potential model relationships include:



```text

vendor-master\[vendor\_id] → vendor-fulfillment-events\[vendor\_id]

inventory-items\[item\_id] → vendor-fulfillment-events\[item\_id]

tickets-v1\[ticket\_id] → vendor-fulfillment-events\[related\_ticket\_id]

```



This supports reporting by:



\- vendor

\- item

\- location

\- delivery status

\- fulfillment status

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

\- workflow-centered operational intelligence

\- SQL readiness

\- Power BI readiness



Future changes to this schema should be made:



\# systematically



NOT:



\# reactively.



\---



\# Portfolio Significance



This schema demonstrates:



\- transactional data modeling

\- vendor fulfillment analysis design

\- operational event tracking

\- relational architecture planning

\- cross-system workflow awareness

\- SQL readiness awareness

\- Power BI modeling awareness

\- enterprise systems thinking



The `vendor-fulfillment-events.csv` schema strengthens the Vendor Performance subsystem by establishing a structured fulfillment event layer for supplier reliability, shipment stability, escalation monitoring, and operational disruption analysis.

