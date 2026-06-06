# Vendor Shipments Schema

## Purpose

The Vendor Shipments dataset tracks inbound shipment activity associated with inventory operations.

It provides visibility into shipment performance, delivery reliability, replenishment support, and operational impacts resulting from delayed or incomplete shipments.

---

## Dataset Grain

One record per vendor shipment.

---

## Primary Key

shipment_id

---

## Fields

|Field Name|Description|
|-|-|
|shipment_id|Unique shipment identifier|
|vendor_id|Vendor associated with the shipment|
|item_id|Inventory item associated with the shipment|
|location_id|Operational location receiving the shipment|
|shipment_date|Date the shipment was initiated|
|expected_arrival_date|Expected shipment arrival date|
|actual_arrival_date|Actual shipment arrival date, if received|
|shipment_status|Current or final shipment status|
|expected_quantity|Quantity expected in the shipment|
|received_quantity|Quantity received from the shipment|
|delay_flag|Indicates whether the shipment was delayed|
|partial_shipment_flag|Indicates whether the shipment was partially received|
|operational_impact_level|Operational impact associated with the shipment|
|escalation_required_flag|Indicates whether escalation was required|
|related_ticket_id|Related operational ticket identifier, if applicable|
|notes|Optional operational notes related to the shipment|

---

## Data Quality Considerations

* Each shipment_id should remain unique.
* Vendor, item, location, and ticket references should align with approved subsystem identifiers when present.
* Expected and received quantities should not be negative.
* Shipment status values should remain standardized.
* Delivered shipments should include an actual_arrival_date.
* Escalated shipments should include a related_ticket_id when applicable.
* Boolean fields should use TRUE or FALSE consistently.
* Operational impact values should remain standardized and reporting-friendly.

---

## Operational Usage

This dataset supports:

* Vendor delivery monitoring
* Shipment performance analysis
* Replenishment visibility
* Delay tracking
* Operational disruption analysis
* Escalation reporting

The Vendor Shipments dataset provides visibility into inbound inventory movement and supports monitoring of vendor delivery performance and supply continuity.

