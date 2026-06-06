# Replenishment Events Schema

## Purpose

The Replenishment Events dataset tracks inventory replenishment requests and fulfillment activity across operational locations.

It provides visibility into replenishment demand, approval activity, vendor involvement, inventory recovery efforts, and replenishment status.

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
|replenishment_type|Type of replenishment activity being performed|
|requested_quantity|Quantity requested for replenishment|
|approved_quantity|Quantity approved for replenishment|
|request_date|Date the replenishment request was initiated|
|expected_arrival_date|Expected inventory arrival date|
|received_date|Date inventory was received|
|replenishment_status|Current status of the replenishment event|
|vendor_id|Vendor associated with the replenishment activity|
|related_ticket_id|Related operational ticket identifier, if applicable|

---

## Data Quality Considerations

* Each replenishment_id should remain unique.
* Item, location, vendor, and ticket references should align with approved subsystem identifiers when present.
* Requested and approved quantities should not be negative.
* Approved quantities should align with operational replenishment decisions.
* Expected arrival and received dates should reflect actual replenishment activity.
* Replenishment status values should remain standardized.

---

## Operational Usage

This dataset supports:

* Replenishment tracking
* Inventory recovery monitoring
* Vendor coordination visibility
* Replenishment turnaround analysis
* Supply continuity monitoring
* Inventory performance reporting

The Replenishment Events dataset provides visibility into how inventory needs are requested, approved, fulfilled, and tracked across operational locations.

