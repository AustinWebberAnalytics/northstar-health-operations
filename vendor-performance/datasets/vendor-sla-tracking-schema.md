\# Vendor SLA Tracking Schema  



\## Northstar Health Operations



\---



\# Purpose



This document defines the schema for the `vendor-sla-tracking.csv` dataset within the Vendor Performance subsystem.



The purpose of this schema is to:



\- define vendor SLA monitoring fields

\- standardize service-level agreement tracking

\- support vendor reliability analysis

\- support escalation timing analysis

\- preserve shared identifier consistency

\- support operational continuity monitoring

\- support future SQL integration

\- support future Power BI modeling



This schema serves as the primary reference for vendor SLA tracking records across Northstar Health Operations.



\---



\# Dataset Overview



The `vendor-sla-tracking.csv` dataset captures operational vendor SLA performance measurements related to fulfillment activity, shipment timing, escalation response, and operational support expectations.



This dataset functions as:



\# the vendor operational compliance layer



within the Vendor Performance subsystem.



The dataset is intended to support analysis of:



\- vendor SLA compliance

\- fulfillment timing performance

\- shipment response consistency

\- escalation responsiveness

\- operational disruption exposure

\- vendor reliability scoring

\- operational continuity risk



\---



\# Dataset Location



```text

vendor-performance/datasets/vendor-sla-tracking.csv

```



\---



\# Dataset Grain



Each row represents:



\# one SLA measurement event



An SLA tracking event may represent:



\- shipment delivery SLA evaluation

\- fulfillment timing review

\- escalation response review

\- emergency fulfillment response review

\- operational support compliance review



The primary identifier for each record is:



```text

sla\_event\_id

```



\---



\# Primary Key



| Field | Purpose |

|---|---|

| sla\_event\_id | Unique identifier for each SLA tracking event |



Example:



```text

SLA-1001

```



\---



\# Foreign Keys and Shared Identifiers



This dataset should use shared identifiers to support cross-system relationships.



| Field | Related Dataset | Purpose |

|---|---|---|

| vendor\_id | vendor-master.csv | Connects SLA event to vendor identity |

| shipment\_id | vendor-shipments.csv | Connects SLA event to shipment activity |

| fulfillment\_event\_id | vendor-fulfillment-events.csv | Connects SLA event to fulfillment performance |

| related\_ticket\_id | tickets-v1.csv | Connects SLA event to operational escalation activity |



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

slaStatus

responseTime

VendorID

ticketRef

```



Preferred:



```text

sla\_status

response\_time\_hours

vendor\_id

related\_ticket\_id

```



\---



\# Schema Definition



| Field Name | Data Type | Required | Description |

|---|---|---|---|

| sla\_event\_id | Text | Yes | Unique SLA tracking event identifier |

| vendor\_id | Text | Yes | Vendor associated with the SLA measurement |

| shipment\_id | Text | No | Shipment associated with SLA measurement |

| fulfillment\_event\_id | Text | No | Fulfillment event associated with SLA measurement |

| sla\_category | Text | Yes | Operational SLA category being evaluated |

| sla\_target\_hours | Number | Yes | Target SLA response or delivery threshold |

| actual\_response\_hours | Number | Yes | Actual measured response or delivery duration |

| sla\_status | Text | Yes | SLA compliance outcome |

| sla\_breach\_flag | Boolean | Yes | Indicates whether SLA expectations were breached |

| escalation\_required\_flag | Boolean | Yes | Indicates whether escalation was required |

| operational\_impact\_level | Text | Yes | Operational impact associated with SLA performance |

| related\_ticket\_id | Text | No | Related operational escalation ticket |

| review\_date | Date | Yes | Date SLA review was recorded |

| corrective\_action\_required\_flag | Boolean | Yes | Indicates whether corrective action was required |

| notes | Text | No | Operational notes related to SLA performance |



\---



\# Field Definitions



\---



\## sla\_event\_id



\### Purpose



Uniquely identifies each vendor SLA tracking event.



\### Format



```text

SLA-####

```



\### Example



```text

SLA-1001

```



\### Governance Rule



The `sla\_event\_id` field should remain stable and unique across all SLA records.



\---



\## vendor\_id



\### Purpose



Identifies the vendor associated with the SLA measurement.



\### Format



```text

VEND-###

```



\### Example



```text

VEND-002

```



\### Governance Rule



The `vendor\_id` field should align with valid vendor identifiers where vendor master data exists.



\---



\## shipment\_id



\### Purpose



Identifies the shipment associated with the SLA review when shipment activity is relevant.



\### Format



```text

SHIP-####

```



\### Example



```text

SHIP-1002

```



\### Governance Rule



This field may remain blank when SLA review is not tied directly to shipment activity.



\---



\## fulfillment\_event\_id



\### Purpose



Identifies the fulfillment event associated with the SLA review.



\### Format



```text

VF-####

```



\### Example



```text

VF-1002

```



\### Governance Rule



This field may remain blank when no fulfillment event relationship exists.



\---



\## sla\_category



\### Purpose



Classifies the operational SLA category being evaluated.



\### Example Values



```text

Delivery SLA

Fulfillment SLA

Escalation Response SLA

Emergency Response SLA

Operational Support SLA

```



\### Governance Rule



SLA categories should remain standardized and operationally meaningful.



\---



\## sla\_target\_hours



\### Purpose



Defines the operational SLA target threshold in hours.



\### Example



```text

24

```



\### Governance Rule



SLA targets should reflect realistic operational service expectations.



\---



\## actual\_response\_hours



\### Purpose



Defines the actual measured response or fulfillment duration in hours.



\### Example



```text

31

```



\### Governance Rule



Actual response durations should never be negative.



\---



\## sla\_status



\### Purpose



Defines the SLA compliance outcome.



\### Example Values



```text

Met

Breached

Monitoring

Escalated

```



\### Governance Rule



SLA status values should remain standardized and operationally meaningful.



\---



\## sla\_breach\_flag



\### Purpose



Indicates whether SLA expectations were breached.



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



\## operational\_impact\_level



\### Purpose



Classifies the operational impact associated with the SLA performance outcome.



\### Example Values



```text

Low

Moderate

High

Critical

```



\### Governance Rule



Operational impact should reflect disruption exposure, continuity risk, escalation severity, or vendor dependency pressure.



\---



\## related\_ticket\_id



\### Purpose



Connects SLA activity to operational escalation activity when applicable.



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



\## review\_date



\### Purpose



Defines the date the SLA review was recorded.



\### Example



```text

2026-05-24

```



\### Governance Rule



Date values should remain internally consistent across operational datasets.



\---



\## corrective\_action\_required\_flag



\### Purpose



Indicates whether corrective action or vendor follow-up was required.



\### Format



```text

TRUE

FALSE

```



\---



\## notes



\### Purpose



Provides optional operational context related to SLA performance.



\### Example



```text

Repeated delayed fulfillment response triggered vendor escalation review.

```



\### Governance Rule



Notes should remain concise and operationally relevant.



\---



\# Required Fields



The following fields are required:



```text

sla\_event\_id

vendor\_id

sla\_category

sla\_target\_hours

actual\_response\_hours

sla\_status

sla\_breach\_flag

escalation\_required\_flag

operational\_impact\_level

review\_date

corrective\_action\_required\_flag

```



Optional fields include:



```text

shipment\_id

fulfillment\_event\_id

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

sla\_breach\_flag

escalation\_required\_flag

corrective\_action\_required\_flag

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

Delivery SLA

Fulfillment SLA

Escalation Response SLA

Emergency Response SLA



Met

Breached

Monitoring

Escalated



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



The `vendor-sla-tracking.csv` dataset is expected to connect to operational vendor activity through:



```text

vendor\_id

shipment\_id

fulfillment\_event\_id

related\_ticket\_id

```



Expected relationships may include:



```text

vendor-master\[vendor\_id] → vendor-sla-tracking\[vendor\_id]

vendor-shipments\[shipment\_id] → vendor-sla-tracking\[shipment\_id]

vendor-fulfillment-events\[fulfillment\_event\_id] → vendor-sla-tracking\[fulfillment\_event\_id]

tickets-v1\[ticket\_id] → vendor-sla-tracking\[related\_ticket\_id]

```



\---



\# Cross-System Usage



The `vendor-sla-tracking.csv` dataset may connect SLA performance activity to:



\- shipment reliability

\- fulfillment consistency

\- escalation workflows

\- operational disruption exposure

\- vendor corrective action tracking

\- leadership operational reporting



This supports:



\- SLA compliance monitoring

\- vendor reliability scoring

\- escalation analysis

\- operational continuity visibility

\- corrective action analysis

\- vendor performance trend reporting



\---



\# Data Quality Rules



The `vendor-sla-tracking.csv` dataset should be reviewed for:



\- duplicate `sla\_event\_id` values

\- missing required fields

\- invalid vendor references

\- invalid shipment references

\- invalid fulfillment references

\- inconsistent boolean values

\- negative response hour values

\- breached SLA events missing escalation indicators

\- escalated SLA events missing ticket references



Each `sla\_event\_id` should remain unique and stable.



\---



\# Future SQL Readiness



This schema supports future SQL integration by defining:



\- stable SLA tracking keys

\- vendor performance relationships

\- shipment and fulfillment SLA modeling

\- escalation-aware compliance analysis

\- operational continuity measurement structure



Future SQL queries may use this dataset to analyze:



\- vendor SLA compliance rates

\- breach frequency

\- escalation-driven SLA failures

\- vendor response performance

\- operational disruption exposure

\- corrective action trends



\---



\# Future Power BI Readiness



This schema supports future Power BI modeling by functioning as a vendor SLA fact table.



Potential model relationships include:



```text

vendor-master\[vendor\_id] → vendor-sla-tracking\[vendor\_id]

vendor-shipments\[shipment\_id] → vendor-sla-tracking\[shipment\_id]

vendor-fulfillment-events\[fulfillment\_event\_id] → vendor-sla-tracking\[fulfillment\_event\_id]

```



This supports reporting by:



\- vendor

\- SLA category

\- SLA status

\- breach frequency

\- operational impact level

\- escalation requirement

\- corrective action requirement



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



\- vendor SLA modeling

\- operational compliance tracking

\- escalation-aware systems thinking

\- vendor reliability measurement

\- relational data governance

\- SQL readiness awareness

\- Power BI modeling awareness

\- scalable operational subsystem construction



The `vendor-sla-tracking.csv` schema strengthens the Vendor Performance subsystem by establishing a standardized SLA compliance layer supporting vendor reliability analysis, operational continuity monitoring, escalation visibility, and leadership operational reporting.

