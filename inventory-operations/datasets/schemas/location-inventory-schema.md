\# Location Inventory Schema  



\## Northstar Health Operations



\---



\# Purpose



This document defines the schema for the `location-inventory.csv` dataset within the Inventory Operations subsystem.



The purpose of this schema is to:



\- define location-level inventory tracking fields

\- standardize operational stock visibility

\- support replenishment monitoring

\- support shortage detection

\- preserve shared identifier consistency

\- support operational location analysis

\- support future SQL integration

\- support future Power BI modeling



This schema serves as the primary reference for operational inventory position records across Northstar Health Operations locations.



\---



\# Dataset Overview



The `location-inventory.csv` dataset captures inventory stock levels by operational location.



This dataset functions as:



\# the operational inventory state layer



within the Inventory Operations subsystem.



The dataset is intended to support analysis of:



\- current stock visibility

\- reorder threshold exposure

\- replenishment pressure

\- shortage risk

\- operational inventory stability

\- location-level inventory monitoring



\---



\# Dataset Location



```text

inventory-operations/datasets/location-inventory.csv

```



\---



\# Dataset Grain



Each row represents:



\# one inventory item at one operational location



Each combination of:



```text

item\_id + location\_id

```



should appear only once in the dataset.



\---



\# Composite Primary Key



| Field | Purpose |

|---|---|

| item\_id | Inventory item identifier |

| location\_id | Operational location identifier |



Example:



```text

ITEM-1001 + LOC-RALEIGH-03

```



\---



\# Foreign Keys and Shared Identifiers



This dataset should use shared identifiers to support cross-system relationships.



| Field | Related Dataset | Purpose |

|---|---|---|

| item\_id | inventory-items.csv | Connects stock records to inventory item master data |

| location\_id | operational locations | Connects stock records to operational facilities |

| preferred\_vendor\_id | vendor-master.csv | Connects inventory records to preferred vendor relationships |



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

LocationID

itemQty

reorderPoint

vendorRef

```



Preferred:



```text

location\_id

current\_quantity

reorder\_threshold

preferred\_vendor\_id

```



\---



\# Schema Definition



| Field Name | Data Type | Required | Description |

|---|---|---|---|

| item\_id | Text | Yes | Inventory item identifier |

| location\_id | Text | Yes | Operational location identifier |

| current\_quantity | Number | Yes | Current on-hand inventory quantity |

| reorder\_threshold | Number | Yes | Quantity level that triggers replenishment attention |

| max\_capacity | Number | Yes | Maximum recommended inventory level |

| inventory\_status | Text | Yes | Operational inventory condition |

| preferred\_vendor\_id | Text | Yes | Preferred vendor supporting replenishment |

| last\_restock\_date | Date | No | Most recent inventory restock date |

| shortage\_risk\_flag | Boolean | Yes | Indicates whether inventory is currently at shortage risk |

| notes | Text | No | Operational notes related to inventory conditions |



\---



\# Field Definitions



\---



\## item\_id



\### Purpose



Identifies the inventory item associated with the stock record.



\### Format



```text

ITEM-####

```



\### Example



```text

ITEM-1001

```



\### Governance Rule



The `item\_id` field should align with valid inventory items defined in:



```text

inventory-items.csv

```



\---



\## location\_id



\### Purpose



Identifies the operational location where inventory is tracked.



\### Format



```text

LOC-\[CITY]-##

```



\### Example



```text

LOC-DURHAM-07

```



\### Governance Rule



Location identifiers should remain stable and standardized across all operational datasets.



\---



\## current\_quantity



\### Purpose



Defines the current quantity of inventory available at the operational location.



\### Example



```text

75

```



\### Governance Rule



Current quantity values should never be negative.



\---



\## reorder\_threshold



\### Purpose



Defines the quantity level at which replenishment attention is required.



\### Example



```text

25

```



\### Governance Rule



Reorder thresholds should reflect operational replenishment planning standards.



\---



\## max\_capacity



\### Purpose



Defines the recommended maximum inventory level for the item at the location.



\### Example



```text

150

```



\### Governance Rule



Maximum capacity should reflect realistic operational storage limits.



\---



\## inventory\_status



\### Purpose



Classifies the operational inventory condition.



\### Example Values



```text

Stable

Low Stock

Critical

Overstocked

Pending Replenishment

```



\### Governance Rule



Inventory status values should remain consistent and operationally meaningful.



\---



\## preferred\_vendor\_id



\### Purpose



Identifies the preferred vendor associated with replenishment support.



\### Format



```text

VEND-###

```



\### Example



```text

VEND-001

```



\### Governance Rule



Preferred vendor references should align with valid vendor identifiers where vendor master data exists.



\---



\## last\_restock\_date



\### Purpose



Tracks the most recent restock activity date for the inventory item at the location.



\### Example



```text

2026-05-20

```



\### Governance Rule



This field may remain blank if no recent restock activity exists.



\---



\## shortage\_risk\_flag



\### Purpose



Indicates whether the inventory position is currently at operational shortage risk.



\### Format



```text

TRUE

FALSE

```



\### Governance Rule



This field should generally be `TRUE` when inventory levels are at or below reorder thresholds.



\---



\## notes



\### Purpose



Provides optional operational context related to inventory conditions.



\### Example



```text

Recent shipment delay increased replenishment pressure for this location.

```



\### Governance Rule



Notes should remain concise and operationally relevant.



\---



\# Required Fields



The following fields are required:



```text

item\_id

location\_id

current\_quantity

reorder\_threshold

max\_capacity

inventory\_status

preferred\_vendor\_id

shortage\_risk\_flag

```



Optional fields include:



```text

last\_restock\_date

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

shortage\_risk\_flag

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



Inventory status fields should use business-readable values.



Examples:



```text

Stable

Low Stock

Critical

Overstocked

Pending Replenishment

```



Status values should remain:



\- consistent

\- readable

\- operationally meaningful

\- reporting-friendly



\---



\# Relationship Standards



The `location-inventory.csv` dataset is expected to connect to operational inventory activity through:



```text

item\_id

location\_id

```



Expected relationships may include:



```text

inventory-items\[item\_id] → location-inventory\[item\_id]

location-inventory\[item\_id] → replenishment-events\[item\_id]

location-inventory\[item\_id] → shortage-events\[item\_id]

location-inventory\[item\_id] → vendor-fulfillment-events\[item\_id]

```



Vendor relationships may also connect through:



```text

preferred\_vendor\_id

```



\---



\# Cross-System Usage



The `location-inventory.csv` dataset may connect operational inventory conditions to:



\- replenishment events

\- shortage events

\- discrepancy investigations

\- vendor shipment delays

\- vendor fulfillment disruptions

\- operational escalation activity



This supports:



\- location-level inventory visibility

\- replenishment risk monitoring

\- shortage exposure analysis

\- vendor dependency visibility

\- operational continuity monitoring



\---



\# Data Quality Rules



The `location-inventory.csv` dataset should be reviewed for:



\- duplicate `item\_id + location\_id` combinations

\- missing required fields

\- negative quantity values

\- invalid reorder thresholds

\- invalid vendor references

\- inconsistent boolean values

\- inventory statuses inconsistent with quantity levels

\- naming inconsistencies across related datasets



Each inventory-location combination should remain unique and stable.



\---



\# Future SQL Readiness



This schema supports future SQL integration by defining:



\- composite inventory-location keys

\- relational inventory state modeling

\- location-based inventory visibility

\- replenishment trigger analysis

\- vendor dependency relationships



Future SQL queries may use this dataset to analyze:



\- low-stock exposure by location

\- inventory stability trends

\- replenishment pressure

\- vendor dependency by item

\- shortage risk concentration



\---



\# Future Power BI Readiness



This schema supports future Power BI modeling by functioning as an operational inventory fact/state table.



Potential model relationships include:



```text

inventory-items\[item\_id] → location-inventory\[item\_id]

vendor-master\[vendor\_id] → location-inventory\[preferred\_vendor\_id]

```



This supports reporting by:



\- location

\- inventory status

\- shortage risk

\- preferred vendor

\- replenishment pressure

\- operational inventory stability



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



\- operational inventory state modeling

\- location-based inventory architecture

\- replenishment monitoring design

\- relational data governance

\- SQL readiness awareness

\- Power BI modeling awareness

\- enterprise systems thinking

\- scalable inventory subsystem construction



The `location-inventory.csv` schema strengthens the Inventory Operations subsystem by establishing a standardized operational inventory visibility layer supporting replenishment monitoring, shortage analysis, vendor dependency analysis, and operational continuity reporting.

