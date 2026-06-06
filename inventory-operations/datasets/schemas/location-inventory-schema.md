# Location Inventory Schema

## Purpose

The Location Inventory dataset tracks inventory quantities and status information across operational locations.

It provides visibility into inventory availability, stock conditions, and location-level inventory performance.

---

## Dataset Grain

One record per inventory item per location.

---

## Primary Key

location_inventory_id

---

## Fields

|Field Name|Description|
|-|-|
|location_inventory_id|Unique location inventory record identifier|
|item_id|Inventory item identifier|
|location_id|Operational location identifier|
|quantity_on_hand|Current inventory quantity available|
|reorder_point|Inventory threshold that triggers replenishment review|
|inventory_status|Current inventory condition or status|
|last_updated_date|Most recent inventory update date|

---

## Data Quality Considerations

* Each location_inventory_id should remain unique.
* Item and location references should align with approved subsystem identifiers.
* Quantity values should accurately reflect inventory conditions.
* Reorder points should support replenishment planning requirements.
* Inventory status values should remain standardized across locations.

---

## Operational Usage

This dataset supports:

* Inventory availability monitoring
* Replenishment planning
* Shortage identification
* Location-level inventory analysis
* Inventory performance reporting

The Location Inventory dataset provides operational visibility into inventory conditions across organizational locations.

