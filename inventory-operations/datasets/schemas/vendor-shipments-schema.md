# Vendor Shipments Schema

## Purpose

The Vendor Shipments dataset tracks inbound inventory shipments from vendors to operational locations.

It provides visibility into shipment timing, delivery performance, fulfillment accuracy, and vendor-related inventory support activities.

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
|ordered_quantity|Quantity ordered from the vendor|
|received_quantity|Quantity received from the vendor|
|order_date|Date the shipment order was initiated|
|expected_delivery_date|Expected shipment delivery date|
|actual_delivery_date|Actual shipment delivery date|
|delivery_status|Current or final delivery status|
|fulfillment_accuracy_flag|Indicates whether the shipment was fulfilled accurately|
|delay_flag|Indicates whether the shipment experienced a delay|
|related_ticket_id|Related operational ticket identifier, if applicable|

---

## Data Quality Considerations

* Each shipment_id should remain unique.
* Vendor, item, location, and ticket references should align with approved subsystem identifiers when present.
* Ordered and received quantities should not be negative.
* Delivery status values should remain standardized.
* Fulfillment accuracy and delay indicators should use TRUE or FALSE consistently.
* Delivered shipments should include an actual_delivery_date when applicable.
* Expected and actual delivery dates should accurately reflect shipment activity.

---

## Operational Usage

This dataset supports:

* Vendor delivery monitoring
* Shipment performance analysis
* Fulfillment accuracy tracking
* Delivery delay monitoring
* Replenishment support visibility
* Vendor performance reporting

The Vendor Shipments dataset provides visibility into vendor shipment activity and supports monitoring of delivery reliability and inventory fulfillment performance.

