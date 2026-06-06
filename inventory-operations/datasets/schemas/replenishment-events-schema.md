# Replenishment Events Schema

## Purpose

The Replenishment Events dataset tracks inventory replenishment activity across items and locations.

It provides visibility into restocking needs, replenishment status, and inventory recovery efforts.

---

## Dataset Grain

One record per replenishment event.

---

## Primary Key

replenishment_id

---

## Fields

|Field Name|Description|
|-|-|
|replenishment_id|Unique replenishment event identifier|
|item_id|Inventory item identifier|
|location_id|Operational location identifier|
|request_date|Date the replenishment request was initiated|
|requested_quantity|Quantity requested for replenishment|
|replenishment_status|Current status of the replenishment event|
|expected_delivery_date|Expected inventory delivery date|

---

## Data Quality Considerations

* Each replenishment_id should remain unique.
* Item and location references should align with approved subsystem identifiers.
* Requested quantities should accurately reflect replenishment needs.
* Replenishment status values should remain standardized.
* Expected delivery dates should support inventory planning and follow-up.

---

## Operational Usage

This dataset supports:

* Replenishment tracking
* Inventory recovery monitoring
* Shortage response
* Supply continuity analysis
* Inventory performance reporting

The Replenishment Events dataset provides visibility into how inventory needs are identified, requested, and addressed.

