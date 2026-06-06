# Location Inventory Schema

## Purpose

The Location Inventory dataset tracks current inventory levels, stock thresholds, and stock status by operational location.

It provides visibility into inventory availability, reorder conditions, safety stock coverage, and location-level inventory health.

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
|current_stock|Current inventory quantity available at the location|
|reorder_point|Inventory threshold that triggers replenishment review|
|target_stock_level|Desired inventory level for the item at the location|
|safety_stock_level|Minimum buffer inventory level maintained for operational continuity|
|stock_status|Current inventory condition or status|
|last_count_date|Most recent inventory count date|

---

## Data Quality Considerations

* Each location_inventory_id should remain unique.
* Item and location references should align with approved subsystem identifiers.
* Current stock, reorder point, target stock level, and safety stock level values should not be negative.
* Stock status values should remain standardized across locations.
* Last count dates should reflect the most recent inventory validation activity.

---

## Operational Usage

This dataset supports:

* Inventory availability monitoring
* Replenishment planning
* Safety stock review
* Stockout risk identification
* Location-level inventory analysis
* Inventory performance reporting

The Location Inventory dataset provides operational visibility into inventory conditions across organizational locations.

