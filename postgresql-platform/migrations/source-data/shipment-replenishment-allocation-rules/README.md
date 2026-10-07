# Shipment Replenishment Allocation Rules

## Northstar Enterprise

---

**Primary Audience:** Inventory-operations maintainers, data engineers, analysts, and reviewers preparing Shipment Replenishment Allocation for governed implementation

**Writing Layer:** Layer 2 — Operational / Analyst

**Architectural Purpose:** Records the approved Issue #22 timing and aggregate quantity-ceiling rules for Shipment Replenishment Allocation and defines a repeatable validation process without creating allocation history.

**Document Type:** Migration Procedure and Approved Business-Rule Decision

**Authority Level:** Approved Issue #22 Implementation

**Status:** Implementation and Runtime Validation Complete

**Approval Date:** October 7, 2026

**Depends On:** Enterprise Relational Schema, Enterprise Logical Model, Enterprise Relational Foundation, Enterprise Database Platform Decision, Phase 4 Data Reconciliation Readiness Review, and approved Issue #22 decision

---

# Purpose

Shipment Replenishment Allocation records how much inventory actually received through one Shipment is assigned toward one approved Replenishment. The relationship stores one current total per (`shipment_id`, `replenishment_id`) pair and supports partial or multi-parent allocation while preventing aggregate over-allocation.

No authoritative allocation source currently exists. This procedure therefore validates the parent data and the approved rules, but it does not infer or create operational allocation rows.

---

# Current Source Profile

The governed profile covers six Shipment records and five Replenishment records.

* four Shipments have known `received_quantity` values
* two pending Shipments have blank `received_quantity` values
* all five Replenishments have known `approved_quantity` values
* two current item-and-location candidate pairs involve Shipments whose received quantity is still unknown
* no source file records Shipment Replenishment Allocation relationships

Candidate pairs are profiling evidence only. Matching identifiers, items, locations, vendors, dates, or quantities do not prove that an allocation occurred.

---

# Approved Timing Model

An allocation may be recorded only when both governing quantities are known:

* Shipment `received_quantity` must be nonblank
* Replenishment `approved_quantity` must be nonblank
* `allocated_quantity` must be greater than zero

A delivery or replenishment status does not substitute for a missing numeric quantity. `ordered_quantity` and `requested_quantity` remain planning values and do not authorize allocation.

The model deliberately excludes advance or planned allocation. The current relationship has no allocation lifecycle state and no allocation date, so using the same row for both planned and actual quantities would create two meanings for `allocated_quantity`.

---

# Approved Aggregate Ceilings

For every Shipment:

```text
SUM(allocated_quantity) <= shipment.received_quantity
```

For every Replenishment:

```text
SUM(allocated_quantity) <= replenishment.approved_quantity
```

Shipment `received_quantity` is the physical availability ceiling. Replenishment `approved_quantity` is the authorization ceiling.

Partial receipts may be allocated up to the quantity actually received. A Shipment does not need to be fully received before its known quantity can be allocated.

If a governing parent quantity is reduced, the change must not leave existing allocations above the new ceiling. A later aggregate-trigger implementation must reject an uncoordinated reduction or allow the parent and allocation corrections to complete together through an approved transactional mechanism. It must never silently delete or reduce allocation evidence.

---

# Governed Artifacts

| Responsibility | Path |
|---|---|
| Approved rule matrix | `postgresql-platform/migrations/source-data/shipment-replenishment-allocation-rules/shipment-replenishment-allocation-rules.csv` |
| Repeatable validator | `postgresql-platform/migrations/source-data/shipment-replenishment-allocation-rules/validate-shipment-replenishment-allocation-rules.py` |
| Shipment source | `inventory-operations/datasets/data/vendor-shipments.csv` |
| Replenishment source | `inventory-operations/datasets/data/replenishment-events.csv` |
| Generated scenario report | `postgresql-platform/migration-output/shipment-replenishment-allocation-rules/shipment-replenishment-allocation-rule-validation.csv` |

The generated scenario report remains ignored and uncommitted.

Successful runtime evidence is recorded in [Shipment Replenishment Allocation Rule Validation Evidence](../../../validation/source-data/shipment-replenishment-allocation-rule-validation.md).

---

# Execute the Validation

From the repository root:

```powershell
python postgresql-platform/migrations/source-data/shipment-replenishment-allocation-rules/validate-shipment-replenishment-allocation-rules.py
```

The validator uses only the Python standard library.

---

# Validation Contract

Before reporting success, the validator must verify:

* both parent sources and the rule artifact are strict UTF-8 without a byte-order mark
* the rule artifact exactly matches the approved Issue #22 decision
* all current parent identifiers are present and unique
* Shipment and Replenishment quantity fields are structurally valid
* the current known and unknown governing-quantity profile is unchanged
* a full receipt can be allocated up to its received quantity
* a partial receipt can be allocated up to its received quantity
* a blank Shipment `received_quantity` blocks allocation
* a blank Replenishment `approved_quantity` blocks allocation
* aggregate Shipment over-allocation is rejected
* aggregate Replenishment over-allocation is rejected
* zero or negative allocation is rejected
* a duplicate Shipment/Replenishment pair is rejected
* parent-quantity reductions that would violate existing allocations are rejected
* all governed inputs remain byte-for-byte unchanged
* the generated report is strict UTF-8 and remains inside the ignored migration-output boundary
* no operational allocation source or inferred allocation row is created

Success ends with:

```text
SHIPMENT REPLENISHMENT ALLOCATION RULE VALIDATION: PASS
```

---

# Exception Handling

A missing governing quantity, nonpositive allocation, duplicate relationship, missing parent, aggregate ceiling breach, or parent reduction below allocated quantity blocks the affected change and must be reported clearly.

Resolution requires a supported parent-data correction, an allocation adjustment, or a governed rule change. The implementation must not substitute ordered or requested quantities, infer authorization from a status, or silently overwrite operational evidence.

---

# Enforcement Boundary

Issue #22 approves the business rules that later trigger work must enforce. It does not implement the Tier 3 relationship table or trigger family.

Later enforcement must cover:

* inserts and updates to `allocated_quantity`
* deletion of an allocation without deleting parent evidence
* changes to Shipment `received_quantity`
* changes to Replenishment `approved_quantity`
* aggregate totals across all relationships sharing either parent

Clear object-specific errors are required. Parent corrections and allocation adjustments may require an approved deferred transactional mechanism during Issue #24 integrity implementation.

---

# Implementation Boundary

Issue #22 does not:

* create Shipment Replenishment Allocation records
* infer allocations from matching source fields
* modify Shipment or Replenishment source data
* use `ordered_quantity` or `requested_quantity` as an allocation ceiling
* allow allocation while either governing quantity is unknown
* create Tier 3 DDL
* implement triggers or supporting indexes
* load PostgreSQL
* alter the approved composite-key relationship structure
