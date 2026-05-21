\# Vendor Master Schema  



\## Northstar Health Operations



\---



\# Purpose



This document defines the schema for the `vendor-master.csv` dataset within the Vendor Performance subsystem.



The purpose of this schema is to:



\- define vendor identity fields

\- standardize vendor classification

\- support vendor performance analysis

\- preserve shared identifier consistency

\- support future SQL integration

\- support future Power BI modeling

\- strengthen cross-system operational reporting

\- maintain governance-first dataset construction



This schema serves as the primary reference for the vendor master dataset.



\---



\# Dataset Overview



The `vendor-master.csv` dataset contains one record per vendor used by Northstar Health Operations.



This dataset functions as:



\# the vendor dimension foundation



within the Vendor Performance subsystem.



The dataset is intended to support relationships with:



\- vendor fulfillment events

\- vendor SLA tracking

\- vendor escalations

\- vendor scorecards

\- inventory operations datasets

\- future executive reporting artifacts



\---



\# Dataset Location



```text

vendor-performance/datasets/vendor-master.csv

```



\---



\# Dataset Grain



Each row represents:



\# one unique vendor



Each vendor should appear only once in the dataset.



The primary identifier for each record is:



```text

vendor\_id

```



\---



\# Primary Key



| Field | Purpose |

|---|---|

| vendor\_id | Unique identifier for each vendor |



Example:



```text

VEND-001

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

VendorID

vendorNumber

supplier\_id

vendorName

```



Preferred:



```text

vendor\_id

vendor\_name

vendor\_type

```



\---



\# Schema Definition



| Field Name | Data Type | Required | Description |

|---|---|---|---|

| vendor\_id | Text | Yes | Unique vendor identifier |

| vendor\_name | Text | Yes | Business-readable vendor name |

| vendor\_type | Text | Yes | Operational classification of the vendor |

| primary\_service\_category | Text | Yes | Main supply or service category supported by the vendor |

| support\_level | Text | Yes | Vendor support role within operations |

| risk\_tier | Text | Yes | Operational risk classification |

| preferred\_vendor\_flag | Boolean | Yes | Indicates whether the vendor is a preferred vendor |

| emergency\_fulfillment\_flag | Boolean | Yes | Indicates whether the vendor may support emergency fulfillment |

| active\_vendor\_flag | Boolean | Yes | Indicates whether the vendor is currently active |

| primary\_contact\_team | Text | No | Internal team responsible for vendor coordination |

| notes | Text | No | Operational notes related to vendor usage or risk |



\---



\# Field Definitions



\---



\## vendor\_id



\### Purpose



Uniquely identifies each vendor across the Northstar Health Operations ecosystem.



\### Format



```text

VEND-###

```



\### Example



```text

VEND-003

```



\### Governance Rule



The `vendor\_id` field should remain stable across all datasets and should not be renamed or replaced by subsystem-local alternatives.



Avoid:



```text

vendor\_number

supplier\_id

vendor\_code

```



Preferred:



```text

vendor\_id

```



\---



\## vendor\_name



\### Purpose



Provides the business-readable name of the vendor.



\### Example



```text

MedSupply Partners

```



\### Governance Rule



Vendor names should be readable and consistent across all datasets and reporting artifacts.



\---



\## vendor\_type



\### Purpose



Classifies the vendor by operational role.



\### Example Values



```text

Primary Supplier

Backup Supplier

Emergency Supplier

Specialty Supplier

Logistics Partner

```



\### Governance Rule



Vendor type values should remain consistent across the dataset to support filtering, grouping, and future reporting.



\---



\## primary\_service\_category



\### Purpose



Identifies the primary category of supplies or services supported by the vendor.



\### Example Values



```text

Medical Supplies

Clinical Equipment

General Operations

Distribution Support

Emergency Supplies

```



\### Governance Rule



Service categories should remain business-readable and operationally meaningful.



\---



\## support\_level



\### Purpose



Defines how the vendor supports Northstar Health Operations.



\### Example Values



```text

Core Operational Support

Supplemental Support

Emergency Support

Specialty Support

Logistics Support

```



\### Governance Rule



Support level should reflect the vendor’s operational role rather than only its purchasing relationship.



\---



\## risk\_tier



\### Purpose



Classifies the vendor’s operational risk level.



\### Example Values



```text

Low

Moderate

High

Critical

```



\### Governance Rule



Risk tier should be based on operational dependency, fulfillment stability, escalation history, or service importance.



\---



\## preferred\_vendor\_flag



\### Purpose



Indicates whether the vendor is a preferred operational vendor.



\### Format



```text

TRUE

FALSE

```



\### Governance Rule



Boolean fields should use `TRUE` or `FALSE`.



\---



\## emergency\_fulfillment\_flag



\### Purpose



Indicates whether the vendor may support emergency fulfillment needs.



\### Format



```text

TRUE

FALSE

```



\### Governance Rule



This field supports operational continuity planning and emergency replenishment analysis.



\---



\## active\_vendor\_flag



\### Purpose



Indicates whether the vendor is currently active within Northstar Health Operations.



\### Format



```text

TRUE

FALSE

```



\### Governance Rule



Inactive vendors should remain in the dataset if historical records depend on their `vendor\_id`.



\---



\## primary\_contact\_team



\### Purpose



Identifies the internal Northstar team primarily responsible for coordinating with the vendor.



\### Example Values



```text

Supply \& Inventory Operations

Operations Coordination Center

Vendor \& Service Management

Data Quality \& Compliance

```



\### Governance Rule



Team names should align with established Northstar organizational language.



\---



\## notes



\### Purpose



Provides optional operational context about the vendor.



\### Example



```text

Used for emergency replenishment during high-priority supply shortages.

```



\### Governance Rule



Notes should remain concise and operationally relevant.



\---



\# Required Fields



The following fields are required:



```text

vendor\_id

vendor\_name

vendor\_type

primary\_service\_category

support\_level

risk\_tier

preferred\_vendor\_flag

emergency\_fulfillment\_flag

active\_vendor\_flag

```



Optional fields include:



```text

primary\_contact\_team

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

preferred\_vendor\_flag

emergency\_fulfillment\_flag

active\_vendor\_flag

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

Primary Supplier

Backup Supplier

Emergency Supplier

Specialty Supplier

Logistics Partner

```



Classification values should remain:



\- consistent

\- readable

\- operationally meaningful

\- reporting-friendly



\---



\# Relationship Standards



The `vendor-master.csv` dataset is expected to connect to future vendor subsystem datasets through:



```text

vendor\_id

```



Expected relationships may include:



```text

vendor-master\[vendor\_id] → vendor-fulfillment-events\[vendor\_id]

vendor-master\[vendor\_id] → vendor-sla-tracking\[vendor\_id]

vendor-master\[vendor\_id] → vendor-escalations\[vendor\_id]

vendor-master\[vendor\_id] → vendor-scorecards\[vendor\_id]

```



The dataset may also support cross-system relationships with inventory and ticketing records through related vendor activity.



\---



\# Cross-System Usage



The `vendor\_id` field may connect vendor records to:



\- inventory replenishment activity

\- shipment events

\- shortage events

\- operational escalations

\- ticketing records

\- executive reporting summaries



This supports:



\- vendor reliability analysis

\- fulfillment trend reporting

\- escalation contribution analysis

\- replenishment risk monitoring

\- operational disruption visibility



\---



\# Data Quality Rules



The `vendor-master.csv` dataset should be reviewed for:



\- duplicate `vendor\_id` values

\- missing required fields

\- inconsistent boolean values

\- inconsistent vendor type labels

\- unclear risk tier values

\- inactive vendors with active event records

\- naming inconsistencies across related datasets



Each `vendor\_id` should be unique and stable.



\---



\# Future SQL Readiness



This schema supports future SQL integration by defining:



\- a stable vendor primary key

\- consistent field naming

\- business-readable classification fields

\- relational join readiness

\- dimension-style vendor structure



Future SQL queries may use this dataset to analyze:



\- vendor fulfillment trends

\- escalation frequency by vendor

\- vendor risk tier distribution

\- active versus inactive vendor behavior

\- vendor support role performance



\---



\# Future Power BI Readiness



This schema supports future Power BI modeling by acting as a vendor dimension table.



Potential model relationships include:



```text

vendor-master\[vendor\_id] → vendor-fulfillment-events\[vendor\_id]

vendor-master\[vendor\_id] → vendor-sla-tracking\[vendor\_id]

vendor-master\[vendor\_id] → vendor-scorecards\[vendor\_id]

```



This supports filtering and reporting by:



\- vendor name

\- vendor type

\- risk tier

\- support level

\- service category

\- active vendor status



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



\- data modeling discipline

\- vendor dimension design

\- relational architecture planning

\- operational data governance

\- SQL readiness awareness

\- Power BI modeling awareness

\- enterprise systems thinking

\- scalable subsystem construction



The `vendor-master.csv` schema strengthens the Vendor Performance subsystem by establishing a stable vendor identity foundation for future fulfillment, escalation, SLA, and scorecard analysis.

