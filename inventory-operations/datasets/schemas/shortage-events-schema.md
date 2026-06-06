# Shortage Events Schema

## Purpose

The Shortage Events dataset tracks inventory shortage conditions that may affect operational continuity.

It provides visibility into shortage severity, affected items, impacted locations, replenishment response, and escalation activity.

---

## Dataset Grain

One record per shortage event.

---

## Primary Key

shortage_event_id

---

## Fields

|Field Name|Description|
|-|-|
|shortage_event_id|Unique shortage event identifier|
|item_id|Inventory item associated with the shortage|
|location_id|Operational location affected by the shortage|
|vendor_id|Vendor associated with shortage recovery or dependency, if applicable|
|shortage_detected_date|Date the shortage condition was identified|
|shortage_severity|Severity level of the shortage event|
|inventory_quantity_at_detection|Inventory quantity available when the shortage was identified|
|reorder_threshold|Reorder threshold at the time of shortage detection|
|operational_impact_level|Operational impact associated with the shortage|
|shortage_status|Current or final shortage status|
|replenishment_event_id|Related replenishment event, if applicable|
|emergency_replenishment_flag|Indicates whether emergency replenishment was required|
|escalation_required_flag|Indicates whether escalation was required|
|related_ticket_id|Related operational ticket identifier, if applicable|
|shortage_resolved_flag|Indicates whether the shortage was resolved|
|shortage_resolution_date|Date the shortage was resolved, if applicable|
|notes|Optional operational notes related to the shortage event|

---

## Data Quality Considerations

* Each shortage_event_id should remain unique.
* Item, location, vendor, replenishment, and ticket references should align with approved subsystem identifiers when present.
* Inventory quantities and reorder thresholds should not be negative.
* Shortage severity and operational impact values should remain standardized.
* Resolved shortages should include a shortage_resolution_date.
* Escalated shortages should include a related_ticket_id when applicable.
* Boolean fields should use TRUE or FALSE consistently.

---

## Operational Usage

This dataset supports:

* Shortage monitoring
* Inventory continuity analysis
* Replenishment recovery tracking
* Escalation visibility
* Operational risk reporting
* Vendor dependency review

The Shortage Events dataset provides visibility into inventory disruption conditions and supports monitoring of shortage recovery activity.

