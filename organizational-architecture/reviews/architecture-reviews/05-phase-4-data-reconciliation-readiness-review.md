# Phase 4 Data Reconciliation Readiness Review

## Northstar Health Operations

---

**Primary Audience:** Northstar architects, data engineers, subsystem maintainers, and reviewers preparing for SQL implementation
**Writing Layer:** Layer 2 — Operational / Architectural
**Architectural Purpose:** Records source-data conditions that affect migration and foreign-key enforcement without reopening the approved enterprise architecture.

---

# Purpose

This review validates whether current repository datasets can satisfy the approved relational design without transformation, exception handling, or source correction.

The findings do not block Tier 5 schema derivation. They do block strict SQL referential-integrity enforcement until the documented issues are resolved.

---

# Validation Findings

## Employee Identity and Ticket Ownership

The workforce roster contains 15 employees and includes both `employee_id` and `employee_name`.

The ticket dataset contains 15 records. Only 3 tickets map by exact `assigned_owner` name to the workforce roster, all through the name `Jordan Lee`.

Four distinct ticket-owner names do not appear in the current roster:

- Avery Patel
- Marcus Nguyen
- Samantha Ortiz
- Taylor Brooks

**Readiness decision:** create Ticket `employee_id` as nullable during migration. Do not enforce `NOT NULL` or strict ownership completeness until the roster or ticket source is reconciled.

## Ticket Location Reconciliation

The ticket dataset contains four distinct free-text location names. They have clear candidate mappings to the four governed location identifiers:

| Ticket source value | Candidate governed identifier |
|---|---|
| Cary Distribution Hub 01 | `LOC-CARY-HUB-01` |
| Durham Outpatient Clinic 07 | `LOC-DURHAM-07` |
| Raleigh Specialty Clinic 03 | `LOC-RALEIGH-03` |
| Wake Forest Clinic 11 | `LOC-WAKEFOREST-11` |

**Readiness decision:** mapping appears complete by inspection but must be formally validated and recorded before strict enforcement.

## Orphaned Ticket References

Three current `related_ticket_id` values do not exist in `tickets-v1.csv`:

| Missing Ticket | Referencing dataset |
|---|---|
| `INC-100018` | `inventory-discrepancies.csv` |
| `INC-100031` | `inventory-discrepancies.csv` |
| `INC-100021` | `shortage-events.csv` |

**Readiness decision:** strict Ticket foreign keys cannot be enabled for these tables until each reference is added, corrected, or explicitly retired.

## Source Encoding

`tickets-v1.csv` is Windows-1252 encoded. The other current operational CSVs are UTF-8 or UTF-8 with BOM.

**Readiness decision:** the migration pipeline must normalize source files to UTF-8 before type validation and load.

## Corrective Action Ownership

Current Corrective Action `assigned_owner` values are organizational functions:

- Vendor Management
- Supply Chain Operations
- Operational Support
- Inventory Leadership

**Readiness decision:** preserve `assigned_owner` as text. Do not infer an Employee relationship or generate `employee_id` values from these fields.

## Fulfillment and Shipment Consistency

Current Fulfillment Event records agree with their referenced Shipment on Vendor, Inventory Item, Location, order date, expected delivery date, actual delivery date, and expected quantity.

Pending received quantity is represented differently across the two datasets: Shipment uses blank while Fulfillment Event uses `0`.

Shipment and Fulfillment Event also use different delivery-status vocabularies.

**Readiness decision:** enforce Vendor, Inventory Item, and Location consistency. Defer date, quantity, and status equivalence until SQL Implementation defines authoritative source and translation rules.

---

# Readiness Classification

| Work Area | Status |
|---|---|
| Tier 5 schema derivation | Ready after final repository ZIP validation |
| Platform-neutral schema completion | Ready |
| SQL DDL implementation | Not yet authorized |
| Strict Ticket FK enforcement | Blocked by orphaned references and owner reconciliation |
| Ticket source load | Requires encoding normalization |
| Corrective Action Employee relationship | Not approved |

---

# Required Pre-SQL Actions

1. Choose the target platform.
2. Confirm the default deletion policy.
3. Normalize Ticket source encoding.
4. Approve and document Ticket location mappings.
5. Resolve unmatched Ticket owner names.
6. Resolve the three orphaned Ticket references.
7. Decide authoritative translation rules for duplicated Shipment and Fulfillment fields.
8. Implement cross-table consistency validation according to the approved schema.
