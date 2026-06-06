# Inventory Discrepancies Schema

## Purpose

The Inventory Discrepancies dataset tracks inventory variances, reconciliation issues, receiving errors, damaged inventory, and system corrections.

It provides visibility into inventory integrity, discrepancy resolution activity, and operational risks associated with inaccurate inventory records.

---

## Dataset Grain

One record per inventory discrepancy event.

---

## Primary Key

discrepancy_event_id

---

## Fields

|Field Name|Description|
|-|-|
|discrepancy_event_id|Unique inventory discrepancy event identifier|
|item_id|Inventory item associated with the discrepancy|
|location_id|Operational location where the discrepancy was identified|
|vendor_id|Vendor associated with the discrepancy, if applicable|
|shipment_id|Shipment associated with the discrepancy, if applicable|
|discrepancy_detected_date|Date the discrepancy was identified|
|discrepancy_type|Classification of the discrepancy|
|expected_quantity|Expected inventory quantity|
|actual_quantity|Actual observed inventory quantity|
|variance_quantity|Difference between expected and actual quantity|
|discrepancy_status|Current or final discrepancy status|
|investigation_required_flag|Indicates whether investigation was required|
|escalation_required_flag|Indicates whether escalation was required|
|related_ticket_id|Related operational ticket identifier, if applicable|
|resolution_date|Date the discrepancy was resolved|
|resolution_action|Action taken to resolve the discrepancy|
|notes|Optional operational notes related to the discrepancy|

---

## Data Quality Considerations

* Each discrepancy_event_id should remain unique.
* Item, location, vendor, shipment, and ticket references should align with approved subsystem identifiers when present.
* Expected and actual quantity values should not be negative.
* Variance quantities should accurately reflect the difference between expected and actual values.
* Discrepancy types and status values should remain standardized.
* Resolved discrepancies should include a resolution_date and resolution_action.
* Escalated discrepancies should include a related_ticket_id when applicable.
* Boolean fields should use TRUE or FALSE consistently.

---

## Operational Usage

This dataset supports:

* Inventory integrity monitoring
* Reconciliation analysis
* Receiving error investigation
* Damaged inventory tracking
* Escalation visibility
* Audit readiness reporting

The Inventory Discrepancies dataset provides visibility into inventory accuracy issues and supports monitoring of discrepancy investigation and resolution activity.

