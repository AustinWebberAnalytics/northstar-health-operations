# Inventory Discrepancies Schema

## Purpose

The Inventory Discrepancies dataset tracks differences between expected and counted inventory quantities identified during inventory validation activities.

It provides visibility into inventory variances, discrepancy investigations, reconciliation efforts, and inventory accuracy concerns.

---

## Dataset Grain

One record per inventory discrepancy event.

---

## Primary Key

discrepancy_id

---

## Fields

|Field Name|Description|
|-|-|
|discrepancy_id|Unique inventory discrepancy identifier|
|item_id|Inventory item associated with the discrepancy|
|location_id|Operational location where the discrepancy was identified|
|expected_quantity|Expected inventory quantity|
|counted_quantity|Actual inventory quantity counted|
|variance_quantity|Difference between expected and counted quantities|
|discrepancy_type|Classification of the discrepancy|
|investigation_status|Current investigation or resolution status|
|discovered_date|Date the discrepancy was identified|
|resolved_date|Date the discrepancy was resolved, if applicable|
|related_ticket_id|Related operational ticket identifier, if applicable|

---

## Data Quality Considerations

* Each discrepancy_id should remain unique.
* Item, location, and ticket references should align with approved subsystem identifiers when present.
* Expected and counted quantities should not be negative.
* Variance quantities should accurately reflect the difference between expected and counted values.
* Discrepancy type values should remain standardized.
* Investigation status values should remain standardized.
* Resolved discrepancies should include a resolved_date when applicable.

---

## Operational Usage

This dataset supports:

* Inventory variance monitoring
* Reconciliation analysis
* Inventory accuracy reporting
* Discrepancy investigation tracking
* Operational issue visibility
* Audit support activities

The Inventory Discrepancies dataset provides visibility into inventory accuracy issues and supports monitoring of discrepancy investigation and resolution activity.

