\# Inventory Items Schema  



\## Northstar Health Operations



\---



\# Purpose



This document defines the schema for the `inventory-items.csv` dataset within the Inventory Operations subsystem.



The purpose of this schema is to:



\- define inventory item master fields

\- standardize inventory item classification

\- preserve shared identifier consistency

\- support replenishment and shortage analysis

\- support vendor relationship tracking

\- support future SQL integration

\- support future Power BI modeling

\- maintain governance-first dataset construction



This schema serves as the primary reference for the inventory item master dataset.



\---



\# Dataset Overview



The `inventory-items.csv` dataset contains one record per inventory item used by Northstar Health Operations.



This dataset functions as:



\# the inventory item dimension foundation



within the Inventory Operations subsystem.



The dataset is intended to support relationships with:



\- location inventory records

\- replenishment events

\- shortage events

\- inventory discrepancy records

\- vendor shipment records

\- vendor fulfillment events

\- future executive reporting artifacts



\---



\# Dataset Location



```text

inventory-operations/datasets/inventory-items.csv

```



\---



\# Dataset Grain



Each row represents:



\# one unique inventory item



Each inventory item should appear only once in the dataset.



The primary identifier for each record is:



```text

item\_id

```



\---



\# Primary Key



| Field | Purpose |

|---|---|

| item\_id | Unique identifier for each inventory item |



Example:



```text

ITEM-1001

```



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

ItemID

itemName

vendorID

categoryName

```



Preferred:



```text

item\_id

item\_name

vendor\_id

item\_category

```



\---



\# Schema Definition



| Field Name | Data Type | Required | Description |

|---|---|---|---|

| item\_id | Text | Yes | Unique inventory item identifier |

| item\_name | Text | Yes | Business-readable item name |

| item\_category | Text | Yes | Operational category of the inventory item |

| criticality\_level | Text | Yes | Operational importance of the item |

| unit\_of\_measure | Text | Yes | Standard unit used to track the item |

| preferred\_vendor\_id | Text | Yes | Preferred vendor associated with the item |

| active\_item\_flag | Boolean | Yes | Indicates whether the item is currently active |

| notes | Text | No | Operational notes related to the inventory item |



\---



\# Field Definitions



\---



\## item\_id



\### Purpose



Uniquely identifies each inventory item across the Northstar Health Operations ecosystem.



\### Format



```text

ITEM-####

```



\### Example



```text

ITEM-1001

```



\### Governance Rule



The `item\_id` field should remain stable across all datasets and should not be renamed or replaced by subsystem-local alternatives.



Avoid:



```text

inventory\_item\_id

item\_number

item\_code

sku

```



Preferred:



```text

item\_id

```



\---



\## item\_name



\### Purpose



Provides the business-readable name of the inventory item.



\### Example



```text

Sterile Gauze Packs

```



\### Governance Rule



Item names should remain readable, consistent, and operationally meaningful across datasets and reporting artifacts.



\---



\## item\_category



\### Purpose



Classifies the inventory item by operational category.



\### Example Values



```text

Medical Supplies

Clinical Equipment

General Operations

Emergency Supplies

```



\### Governance Rule



Item category values should remain consistent across the dataset to support grouping, filtering, and future reporting.



\---



\## criticality\_level



\### Purpose



Classifies the operational importance of the item.



\### Example Values



```text

Low

Moderate

High

Critical

```



\### Governance Rule



Criticality should reflect the operational risk created if the item becomes unavailable.



\---



\## unit\_of\_measure



\### Purpose



Defines the standard unit used to track the inventory item.



\### Example Values



```text

Each

Box

Case

Pack

Unit

```



\### Governance Rule



Units of measure should remain consistent and business-readable.



\---



\## preferred\_vendor\_id



\### Purpose



Identifies the preferred vendor associated with the inventory item.



\### Format



```text

VEND-###

```



\### Example



```text

VEND-001

```



\### Governance Rule



The `preferred\_vendor\_id` field should align with valid vendor identifiers where vendor master data exists.



\---



\## active\_item\_flag



\### Purpose



Indicates whether the item is currently active in operational inventory tracking.



\### Format



```text

TRUE

FALSE

```



\### Governance Rule



Inactive items should remain in the dataset if historical records depend on their `item\_id`.



\---



\## notes



\### Purpose



Provides optional operational context about the inventory item.



\### Example



```text

High criticality item used in procedure readiness workflows.

```



\### Governance Rule



Notes should remain concise and operationally relevant.



\---



\# Required Fields



The following fields are required:



```text

item\_id

item\_name

item\_category

criticality\_level

unit\_of\_measure

preferred\_vendor\_id

active\_item\_flag

```



Optional fields include:



```text

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

active\_item\_flag

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



Classification fields should use business-readable values.



Examples:



```text

Medical Supplies

Clinical Equipment

General Operations

Emergency Supplies

Low

Moderate

High

Critical

```



Classification values should remain:



\- consistent

\- readable

\- operationally meaningful

\- reporting-friendly



\---



\# Relationship Standards



The `inventory-items.csv` dataset is expected to connect to inventory and vendor activity through:



```text

item\_id

```



Expected relationships may include:



```text

inventory-items\[item\_id] → location-inventory\[item\_id]

inventory-items\[item\_id] → replenishment-events\[item\_id]

inventory-items\[item\_id] → shortage-events\[item\_id]

inventory-items\[item\_id] → inventory-discrepancies\[item\_id]

inventory-items\[item\_id] → vendor-shipments\[item\_id]

inventory-items\[item\_id] → vendor-fulfillment-events\[item\_id]

```



The dataset may also connect to vendor master records through:



```text

preferred\_vendor\_id

```



\---



\# Cross-System Usage



The `item\_id` field may connect inventory item records to:



\- current stock levels

\- replenishment activity

\- shortage events

\- discrepancy investigations

\- vendor shipments

\- vendor fulfillment events

\- executive reporting summaries



This supports:



\- inventory stability analysis

\- shortage trend reporting

\- replenishment risk monitoring

\- vendor dependency analysis

\- operational disruption visibility



\---



\# Data Quality Rules



The `inventory-items.csv` dataset should be reviewed for:



\- duplicate `item\_id` values

\- missing required fields

\- inconsistent boolean values

\- unclear item category labels

\- unclear criticality values

\- invalid preferred vendor references

\- inactive items with active event records

\- naming inconsistencies across related datasets



Each `item\_id` should be unique and stable.



\---



\# Future SQL Readiness



This schema supports future SQL integration by defining:



\- a stable inventory item primary key

\- consistent field naming

\- business-readable classification fields

\- relational join readiness

\- dimension-style item structure



Future SQL queries may use this dataset to analyze:



\- shortages by item

\- replenishment activity by item

\- inventory discrepancies by item

\- vendor fulfillment performance by item

\- operational risk by item criticality



\---



\# Future Power BI Readiness



This schema supports future Power BI modeling by acting as an inventory item dimension table.



Potential model relationships include:



```text

inventory-items\[item\_id] → location-inventory\[item\_id]

inventory-items\[item\_id] → shortage-events\[item\_id]

inventory-items\[item\_id] → replenishment-events\[item\_id]

inventory-items\[item\_id] → vendor-fulfillment-events\[item\_id]

```



This supports filtering and reporting by:



\- item name

\- item category

\- criticality level

\- preferred vendor

\- active item status



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



\- inventory master data modeling

\- item dimension design

\- relational architecture planning

\- operational data governance

\- SQL readiness awareness

\- Power BI modeling awareness

\- enterprise systems thinking

\- scalable subsystem construction



The `inventory-items.csv` schema strengthens the Inventory Operations subsystem by establishing a stable item identity foundation for replenishment, shortage, discrepancy, shipment, and vendor fulfillment analysis.

