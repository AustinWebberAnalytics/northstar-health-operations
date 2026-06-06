# Inventory Items Schema

## Purpose

The Inventory Items dataset serves as the primary item reference table for the Inventory Operations subsystem.

It defines inventory item attributes used to support stock monitoring, replenishment activity, shortage analysis, discrepancy review, and vendor relationship tracking.

---

## Dataset Grain

One record per inventory item.

---

## Primary Key

item_id

---

## Fields

|Field Name|Description|
|-|-|
|item_id|Unique inventory item identifier|
|item_name|Name of the inventory item|
|item_category|Operational category of the item|
|criticality_level|Relative operational importance of the item|
|unit_of_measure|Measurement unit used for inventory tracking|
|preferred_vendor_id|Preferred vendor associated with the item|
|active_flag|Indicates whether the item is currently active|

---

## Data Quality Considerations

* Each item_id should remain unique.
* Item names should be clear and consistently formatted.
* Criticality levels should reflect operational importance.
* Preferred vendor references should align with vendor records when applicable.
* Inactive items should remain available for historical reporting when needed.

---

## Operational Usage

This dataset supports:

* Inventory item reference management
* Stock monitoring
* Replenishment analysis
* Shortage analysis
* Discrepancy investigation
* Vendor relationship visibility

The Inventory Items dataset provides the item-level foundation for Inventory Operations reporting and analysis.

