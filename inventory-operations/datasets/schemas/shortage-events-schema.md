# Shortage Events Schema

## Purpose

The Shortage Events dataset tracks inventory shortage conditions that may affect operational continuity.

It provides visibility into shortage severity, operational impact, escalation activity, and resolution status across inventory locations.

---

## Dataset Grain

One record per shortage event.

---

## Primary Key

shortage_id

---

## Fields

|Field Name|Description|
|-|-|
|shortage_id|Unique shortage event identifier|
|item_id|Inventory item associated with the shortage|
|location_id|Operational location affected by the shortage|
|shortage_detected_date|Date the shortage condition was identified|
|shortage_severity|Severity classification of the shortage|
|estimated_days_of_stockout|Estimated duration of the shortage condition|
|operational_impact|Operational impact associated with the shortage|
|escalation_flag|Indicates whether escalation was required|
|related_ticket_id|Related operational ticket identifier, if applicable|
|resolution_status|Current or final shortage resolution status|

---

## Data Quality Considerations

* Each shortage_id should remain unique.
* Item, location, and ticket references should align with approved subsystem identifiers when present.
* Estimated days of stockout should not be negative.
* Shortage severity values should remain standardized.
* Operational impact values should remain standardized.
* Escalation flags should use TRUE or FALSE consistently.
* Resolution status values should remain standardized across records.

---

## Operational Usage

This dataset supports:

* Shortage monitoring
* Operational risk visibility
* Escalation tracking
* Service continuity analysis
* Inventory disruption reporting
* Resolution monitoring

The Shortage Events dataset provides visibility into inventory shortages and their operational impact across organizational locations.

