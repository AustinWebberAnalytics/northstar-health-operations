\# Inventory Discrepancies Schema  



\## Northstar Health Operations



\---



\# Purpose



This document defines the schema for the `inventory-discrepancies.csv` dataset within the Inventory Operations subsystem.



The purpose of this schema is to:



\- define inventory discrepancy tracking fields

\- standardize reconciliation activity

\- support inventory integrity monitoring

\- support discrepancy investigation analysis

\- preserve shared identifier consistency

\- support operational audit readiness

\- support future SQL integration

\- support future Power BI modeling



This schema serves as the primary reference for inventory discrepancy records across Northstar Health Operations.



\---



\# Dataset Overview



The `inventory-discrepancies.csv` dataset captures inventory variance, reconciliation, receiving, damage, and system correction issues across operational locations.



This dataset functions as:



\# the inventory integrity and reconciliation layer



within the Inventory Operations subsystem.



The dataset is intended to support analysis of:



\- count variances

\- damaged inventory

\- receiving errors

\- missing inventory

\- reconciliation workload

\- operational audit exposure

\- inventory visibility accuracy

\- discrepancy resolution performance



\---



\# Dataset Location



```text

inventory-operations/datasets/inventory-discrepancies.csv

```



\---



\# Dataset Grain



Each row represents:



\# one inventory discrepancy event



A discrepancy event may represent:



\- physical count variance

\- receiving mismatch

\- damaged inventory

\- missing inventory

\- system entry correction

\- reconciliation investigation



The primary identifier for each record is:



```text

discrepancy\_event\_id

```



\---



\# Primary Key



| Field | Purpose |

|---|---|

| discrepancy\_event\_id | Unique identifier for each inventory discrepancy event |



Example:



```text

DISC-1001

```



\---



\# Foreign Keys and Shared Identifiers



This dataset should use shared identifiers to support cross-system relationships.



| Field | Related Dataset | Purpose |

|---|---|---|

| item\_id | inventory-items.csv | Connects discrepancy event to inventory item |

| location\_id | location-inventory.csv | Connects discrepancy event to operational location |

| vendor\_id | vendor-master.csv | Connects discrepancy event to vendor when applicable |

| shipment\_id | vendor shipment records | Connects discrepancy event to receiving or shipment activity |

| related\_ticket\_id | tickets-v1.csv | Connects discrepancy event to operational escalation or investigation ticket |



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

DiscrepancyID

itemIssue

varianceQty

ticketReference

```



Preferred:



```text

discrepancy\_event\_id

item\_id

variance\_quantity

related\_ticket\_id

```



\---



\# Schema Definition



| Field Name | Data Type | Required | Description |

|---|---|---|---|

| discrepancy\_event\_id | Text | Yes | Unique inventory discrepancy event identifier |

| item\_id | Text | Yes | Inventory item associated with the discrepancy |

| location\_id | Text | Yes | Operational location where discrepancy was identified |

| vendor\_id | Text | No | Vendor associated with discrepancy when applicable |

| shipment\_id | Text | No | Shipment associated with receiving or fulfillment discrepancy |

| discrepancy\_detected\_date | Date | Yes | Date discrepancy was identified |

| discrepancy\_type | Text | Yes | Operational classification of the discrepancy |

| expected\_quantity | Number | Yes | Expected inventory quantity |

| actual\_quantity | Number | Yes | Actual observed inventory quantity |

| variance\_quantity | Number | Yes | Difference between expected and actual quantity |

| discrepancy\_status | Text | Yes | Current or final discrepancy status |

| investigation\_required\_flag | Boolean | Yes | Indicates whether investigation was required |

| escalation\_required\_flag | Boolean | Yes | Indicates whether escalation was required |

| related\_ticket\_id | Text | No | Related operational ticket identifier |

| resolution\_date | Date | No | Date discrepancy was resolved |

| resolution\_action | Text | No | Action taken to resolve or reconcile the discrepancy |

| notes | Text | No | Operational notes related to the discrepancy |



\---



\# Field Definitions



\---



\## discrepancy\_event\_id



\### Purpose



Uniquely identifies each inventory discrepancy event.



\### Format



```text

DISC-####

```



\### Example



```text

DISC-1001

```



\### Governance Rule



The `discrepancy\_event\_id` field should remain stable and unique across all discrepancy records.



\---



\## item\_id



\### Purpose



Identifies the inventory item associated with the discrepancy event.



\### Format



```text

ITEM-####

```



\### Example



```text

ITEM-1004

```



\### Governance Rule



The `item\_id` field should align with valid inventory items defined in:



```text

inventory-items.csv

```



\---



\## location\_id



\### Purpose



Identifies the operational location where the discrepancy was identified.



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



\## vendor\_id



\### Purpose



Identifies the vendor associated with the discrepancy when the discrepancy is connected to receiving, shipment, or fulfillment activity.



\### Format



```text

VEND-###

```



\### Example



```text

VEND-004

```



\### Governance Rule



This field may remain blank when no vendor relationship is directly associated with the discrepancy.



\---



\## shipment\_id



\### Purpose



Identifies the shipment associated with the discrepancy when the discrepancy is related to receiving or fulfillment activity.



\### Format



```text

SHIP-####

```



\### Example



```text

SHIP-1004

```



\### Governance Rule



This field may remain blank when no shipment relationship is directly associated with the discrepancy.



\---



\## discrepancy\_detected\_date



\### Purpose



Defines the date the discrepancy was identified.



\### Example



```text

2026-05-21

```



\### Governance Rule



Date values should remain internally consistent across operational datasets.



\---



\## discrepancy\_type



\### Purpose



Classifies the type of inventory discrepancy.



\### Example Values



```text

Count Variance

Receiving Error

Missing Inventory

Damaged Inventory

System Entry Correction

```



\### Governance Rule



Discrepancy type values should remain consistent and operationally meaningful.



\---



\## expected\_quantity



\### Purpose



Defines the expected inventory quantity.



\### Example



```text

80

```



\### Governance Rule



Expected quantity values should not be negative.



\---



\## actual\_quantity



\### Purpose



Defines the actual observed inventory quantity.



\### Example



```text

72

```



\### Governance Rule



Actual quantity values should not be negative.



\---



\## variance\_quantity



\### Purpose



Defines the difference between actual and expected quantity.



\### Example



```text

\-8

```



\### Governance Rule



Variance quantity may be negative, zero, or positive depending on the discrepancy condition.



\---



\## discrepancy\_status



\### Purpose



Defines the current or final discrepancy state.



\### Example Values



```text

Open

Under Review

Resolved

Escalated

```



\### Governance Rule



Discrepancy status values should remain standardized and operationally meaningful.



\---



\## investigation\_required\_flag



\### Purpose



Indicates whether investigation was required.



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



Connects the discrepancy event to operational ticketing activity.



\### Format



```text

INC-######

```



\### Example



```text

INC-100012

```



\### Governance Rule



This field may remain blank if no escalation or investigation ticket exists.



\---



\## resolution\_date



\### Purpose



Defines the date the discrepancy was resolved.



\### Example



```text

2026-05-24

```



\### Governance Rule



This field may remain blank if the discrepancy remains unresolved.



\---



\## resolution\_action



\### Purpose



Describes the action taken to resolve or reconcile the discrepancy.



\### Example Values



```text

Inventory Count Corrected

Receiving Record Updated

Damaged Item Removed

System Entry Corrected

Investigation Closed

```



\### Governance Rule



Resolution actions should remain concise, business-readable, and operationally meaningful.



\---



\## notes



\### Purpose



Provides optional operational context related to the discrepancy event.



\### Example



```text

Receiving mismatch identified during shipment intake review.

```



\### Governance Rule



Notes should remain concise and operationally relevant.



\---



\# Required Fields



The following fields are required:



```text

discrepancy\_event\_id

item\_id

location\_id

discrepancy\_detected\_date

discrepancy\_type

expected\_quantity

actual\_quantity

variance\_quantity

discrepancy\_status

investigation\_required\_flag

escalation\_required\_flag

```



Optional fields include:



```text

vendor\_id

shipment\_id

related\_ticket\_id

resolution\_date

resolution\_action

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

investigation\_required\_flag

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

Count Variance

Receiving Error

Missing Inventory

Damaged Inventory

System Entry Correction



Open

Under Review

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



The `inventory-discrepancies.csv` dataset is expected to connect to operational inventory, vendor, shipment, and ticket activity through:



```text

item\_id

location\_id

vendor\_id

shipment\_id

related\_ticket\_id

```



Expected relationships may include:



```text

inventory-items\[item\_id] → inventory-discrepancies\[item\_id]

location-inventory\[location\_id] → inventory-discrepancies\[location\_id]

vendor-master\[vendor\_id] → inventory-discrepancies\[vendor\_id]

vendor-shipments\[shipment\_id] → inventory-discrepancies\[shipment\_id]

tickets-v1\[ticket\_id] → inventory-discrepancies\[related\_ticket\_id]

```



\---



\# Cross-System Usage



The `inventory-discrepancies.csv` dataset may connect discrepancy activity to:



\- inventory item records

\- location inventory conditions

\- vendor shipment records

\- operational escalation activity

\- audit and reconciliation workflows

\- executive reporting summaries



This supports:



\- discrepancy trend monitoring

\- reconciliation workload analysis

\- receiving error visibility

\- damaged inventory tracking

\- vendor-related discrepancy analysis

\- operational audit readiness



\---



\# Data Quality Rules



The `inventory-discrepancies.csv` dataset should be reviewed for:



\- duplicate `discrepancy\_event\_id` values

\- missing required fields

\- invalid item references

\- invalid location references

\- invalid vendor references

\- invalid shipment references

\- inconsistent boolean values

\- unresolved discrepancies with resolution dates

\- resolved discrepancies missing resolution actions

\- escalated discrepancies missing ticket references



Each `discrepancy\_event\_id` should remain unique and stable.



\---



\# Future SQL Readiness



This schema supports future SQL integration by defining:



\- stable discrepancy event keys

\- inventory reconciliation relationships

\- vendor and shipment relationship fields

\- escalation-aware discrepancy modeling

\- audit-ready operational structure



Future SQL queries may use this dataset to analyze:



\- discrepancy frequency by item

\- discrepancy frequency by location

\- vendor-related receiving discrepancies

\- unresolved discrepancy volume

\- reconciliation resolution timelines

\- escalation-linked discrepancy activity



\---



\# Future Power BI Readiness



This schema supports future Power BI modeling by functioning as an inventory discrepancy event fact table.



Potential model relationships include:



```text

inventory-items\[item\_id] → inventory-discrepancies\[item\_id]

location-inventory\[location\_id] → inventory-discrepancies\[location\_id]

vendor-master\[vendor\_id] → inventory-discrepancies\[vendor\_id]

vendor-shipments\[shipment\_id] → inventory-discrepancies\[shipment\_id]

```



This supports reporting by:



\- discrepancy type

\- discrepancy status

\- operational location

\- inventory item

\- vendor

\- shipment

\- escalation activity

\- resolution status



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



\- inventory reconciliation modeling

\- discrepancy investigation tracking

\- operational audit readiness

\- escalation-aware systems thinking

\- relational data governance

\- SQL readiness awareness

\- Power BI modeling awareness

\- scalable operational subsystem construction



The `inventory-discrepancies.csv` schema strengthens the Inventory Operations subsystem by establishing a standardized discrepancy event layer supporting inventory integrity monitoring, reconciliation analysis, vendor receiving visibility, and operational audit readiness.

