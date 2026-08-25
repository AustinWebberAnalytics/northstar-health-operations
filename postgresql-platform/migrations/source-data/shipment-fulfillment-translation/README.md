# Shipment and Fulfillment Event Translation

## Northstar Enterprise

---

**Primary Audience:** Data engineers, analysts, vendor-performance maintainers, inventory-operations maintainers, and reviewers preparing Shipment and Fulfillment Event data for governed migration

**Writing Layer:** Layer 2 — Operational / Analyst

**Architectural Purpose:** Records the approved authority and translation rules for repeated Shipment and Fulfillment Event fields and defines the repeatable comparison process that preserves both source representations while rejecting contradictions.

**Document Type:** Migration Procedure and Approved Translation Decision

**Authority Level:** Approved Issue #21 Implementation

**Status:** Implementation Complete — Runtime Validation Pending

**Approval Date:** August 25, 2026

**Depends On:** Enterprise Relational Schema, Enterprise Logical Model, Enterprise Relational Foundation, Enterprise Database Platform Decision, and Phase 4 Data Reconciliation Readiness Review

---

# Purpose

Shipment represents physical inventory movement. Fulfillment Event represents the vendor-performance assessment of a referenced Shipment. The sources intentionally repeat operational references, dates, quantities, flags, and delivery-state information, but the repeated fields do not all share the same semantics.

This procedure validates the approved Issue #21 authority model without overwriting either source. It generates a pair-level comparison file and a separate exception report under the ignored migration-output boundary.

---

# Current Source Profile

The approved profile covers six Shipment records and six Fulfillment Event records.

* all six current Shipments have exactly one referenced Fulfillment Event
* every `shipment_id` and `fulfillment_event_id` is unique in the current sources
* Vendor, Inventory Item, Location, related Ticket, order date, expected delivery date, actual delivery date, ordered or expected quantity, and `delay_flag` agree across all six pairs
* four received-quantity pairs agree exactly
* `SHIP-1003` and `SHIP-1004` use blank Shipment `received_quantity` and Fulfillment Event `received_quantity = 0` while both assessments remain pending
* the same two pending pairs use blank Shipment `fulfillment_accuracy_flag` and Fulfillment Event `FALSE`
* Shipment and Fulfillment Event delivery-status vocabularies answer different operational questions and are not directly equated

The current one-to-one profile is migration evidence, not a new business candidate key. The approved architecture still permits multiple Fulfillment Events for one Shipment if future business activity requires repeated assessments.

---

# Approved Authority Model

## Physical-Movement Authority

Shipment is authoritative for:

* `vendor_id`
* `item_id`
* `location_id`
* `related_ticket_id`
* `order_date`
* `expected_delivery_date`
* `actual_delivery_date`
* `ordered_quantity`
* physical `received_quantity`
* Shipment lifecycle state

The repeated Fulfillment Event values remain independently stored assessment evidence, but they must satisfy the governed comparison rules.

## Assessment Authority

Fulfillment Event remains authoritative for its assessment-only fields, including:

* `fulfillment_status`
* vendor-performance delivery timing in `delivery_status`
* `delay_days`
* `partial_fulfillment_flag`
* `emergency_fulfillment_flag`
* `operational_impact_level`
* `escalation_required_flag`
* `notes`

Issue #21 does not collapse these fields into Shipment or remove the Fulfillment Event source values.

---

# Governed Decision Artifacts

| Responsibility | Path |
|---|---|
| Field authority and comparison matrix | `postgresql-platform/migrations/source-data/shipment-fulfillment-translation/shipment-fulfillment-field-rules.csv` |
| Status-combination matrix | `postgresql-platform/migrations/source-data/shipment-fulfillment-translation/shipment-fulfillment-status-rules.csv` |
| Validation process | `postgresql-platform/migrations/source-data/shipment-fulfillment-translation/validate-shipment-fulfillment-translation.py` |
| Shipment source | `inventory-operations/datasets/data/vendor-shipments.csv` |
| Fulfillment Event source | `vendor-performance/datasets/data/vendor-fulfillment-events.csv` |
| Generated pair comparison | `postgresql-platform/migration-output/shipment-fulfillment-translation/shipment-fulfillment-comparison.csv` |
| Generated exception report | `postgresql-platform/migration-output/shipment-fulfillment-translation/shipment-fulfillment-translation-exceptions.csv` |

Generated outputs remain ignored and uncommitted.

---

# Pending Null, Zero, and Accuracy Rules

A blank Shipment `received_quantity` means the physical receipt quantity is not yet finalized. It is not silently converted to zero.

Fulfillment Event `received_quantity = 0` means zero units have been received as of the pending assessment snapshot. It does not establish a final confirmed zero for the Shipment.

The blank and zero values form an allowed translated pair only when:

* Shipment `delivery_status` is `Pending` or `Delayed`
* Fulfillment Event `fulfillment_status` is `Pending`
* Fulfillment Event `delivery_status` is the allowed status from the status matrix
* both actual-delivery dates are blank
* Shipment `fulfillment_accuracy_flag` is blank
* Fulfillment Event `fulfillment_accuracy_flag` is `FALSE`

When Shipment `received_quantity` is populated, Fulfillment Event `received_quantity` must match it exactly and both fulfillment-accuracy flags must be populated and agree.

A future nonblank Shipment `received_quantity = 0` would represent a physically confirmed zero. No current record or approved final-failure status supports that state, so it requires governance review rather than reuse of the pending translation.

---

# Independent Status Dimensions

The three status fields remain distinct:

* Shipment `delivery_status` describes physical lifecycle or the dominant current movement condition
* Fulfillment Event `delivery_status` describes delivery timing or outcome
* Fulfillment Event `fulfillment_status` describes quantity completeness

The status matrix permits combinations, not direct word substitutions. For example, Shipment `Partial` may pair with Fulfillment Event delivery `Delivered` or `Delayed`, but it must pair with fulfillment `Partial`. Shipment `Delayed` must pair with Fulfillment Event delivery `Delayed`, while completeness may remain `Pending`, `Partial`, or `Complete`.

The approved matrix governs migration validation only. It does not promote the observed vocabularies into PostgreSQL `CHECK` constraints. A new source value or combination requires governance review.

---

# Execute the Validation

From the repository root:

```powershell
python postgresql-platform/migrations/source-data/shipment-fulfillment-translation/validate-shipment-fulfillment-translation.py
```

The process uses only the Python standard library.

---

# Validation Contract

Before reporting success, the process must verify:

* both source datasets and both decision artifacts are strict UTF-8 without a byte-order mark
* the two decision artifacts exactly match the Issue #21 approval
* all current source identifiers are present and unique
* every Fulfillment Event references an existing Shipment
* every current Shipment participates in the comparison profile
* repeated Vendor, Inventory Item, Location, Ticket, date, ordered or expected quantity, and delay fields agree
* received quantities and fulfillment-accuracy flags follow the exact pending or assessable rules
* every status combination exists in the approved status matrix
* record-level dates, quantities, flags, and statuses are internally consistent
* both source representations remain present in the comparison output
* every contradiction is written to the exception report and blocks success
* both generated outputs are strict UTF-8 without a byte-order mark
* all governed inputs remain byte-for-byte unchanged
* generated outputs remain inside the ignored migration-output boundary

Success ends with:

```text
SHIPMENT FULFILLMENT TRANSLATION VALIDATION: PASS
```

---

# Exception Handling

The validator never overwrites a Shipment or Fulfillment Event value. A missing reference, field disagreement, unsupported status combination, invalid pending-state representation, or internal lifecycle contradiction produces a field-level exception containing both source values and a reason.

Any generated exception blocks the affected translation boundary from passing. Resolution requires source correction supported by authority, an approved rule change, or a documented exception decision. Silent precedence, approximate translation, and source-value replacement are prohibited.

---

# Enforcement Boundary

Issue #21 separates two enforcement stages:

* migration validation compares the current files before canonical loading
* later approved cross-table trigger or equivalent integrity work enforces repeated-field agreement after Shipment and Fulfillment Event exist in PostgreSQL

Row-level checks may validate internal date, quantity, flag, and status consistency during migration. No trigger, hard vocabulary constraint, Tier 3 table, or PostgreSQL data load is implemented here.

---

# Validation Evidence

Runtime validation has not yet been executed on the approved repository commit. Issue #21 remains open until the governed runtime result, generated-output exclusion, and clean working-tree state are confirmed and recorded.

---

# Implementation Boundary

Issue #21 defines Shipment and Fulfillment Event authority, translation, validation, and exception rules only.

It does not:

* modify either source dataset
* collapse Shipment and Fulfillment Event into one entity
* convert Shipment nulls to zero
* treat Fulfillment Event pending zero as a final confirmed zero
* impose a one-Fulfillment-Event-per-Shipment candidate key
* create staging or canonical load tables
* load PostgreSQL
* implement triggers
* promote provisional vocabularies into hard database constraints
* implement Tier 3 DDL
* approve allocation timing or quantity-ceiling rules governed by Issue #22
