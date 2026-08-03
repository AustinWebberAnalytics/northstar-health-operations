# Tier 2 PostgreSQL Implementation Contract

## Northstar Enterprise

---

**Primary Audience:** Northstar architects, data engineers, subsystem maintainers, and reviewers implementing or validating the approved Tier 2 PostgreSQL structures

**Writing Layer:** Layer 2 — Operational / Architectural

**Architectural Purpose:** Defines the physical PostgreSQL types, column order, nullability, keys, constraint names, source-transition treatment, file responsibilities, validation boundaries, documentation changes, and lifecycle-evidence responsibility governing Tier 2 implementation.

**Document Type:** PostgreSQL Implementation Contract

**Authority Level:** Approved Physical Implementation Contract

**Status:** Approved — Issue #31 Tier 2 Contract

**Depends On:** Enterprise Relational Schema, Enterprise Relational Foundation, Enterprise Database Platform Decision, Enterprise Logical Model, Enterprise Relational Model, Enterprise Object Model, Cross-System Identifier Dictionary, Enterprise Identifier Governance Review, Naming Convention Standards, Project Governance Standards, the completed PostgreSQL implementation foundation, and the completed Tier 1 PostgreSQL boundary at commit `547998a080c543811e820f12d9d5b0732e7e54b8`

---

# Purpose

This contract translates the locked, platform-neutral Tier 2 relational design into an exact PostgreSQL 18 implementation boundary before executable Tier 2 SQL is created.

The locked architecture remains authoritative for object meaning, relationships, identifiers, logical types, and nullability. This document resolves only the physical decisions explicitly delegated to SQL implementation: PostgreSQL type mapping, constraint names and properties, file responsibilities, validator boundaries, required documentation changes, and lifecycle-evidence responsibility.

If this contract conflicts with a newer approved governance or architecture artifact, the newer higher-authority artifact controls and the discrepancy must be resolved before implementation continues.

---

# Implementation Boundary

Issue #31 approves a physical implementation contract only.

This issue does not create tables, execute SQL, load source data, perform migration, reconcile Ticket references, enforce the two deferred foreign keys on `ticketing.ticket`, normalize source files, create provisional `CHECK` constraints, add triggers, add manually defined indexes, or implement Tier 3–5 structures.

Executable Tier 2 work remains governed by issue #32. Lifecycle validation and completion evidence remain governed by issue #33.

---

# Approved Tier 2 Inventory

| Table | Columns | Required | Nullable | Primary Keys | Foreign Keys | Business-Key Unique Constraints |
|---|---:|---:|---:|---:|---:|---:|
| `vendor.shipment` | 13 | 9 | 4 | 1 | 4 | 0 |
| `inventory.replenishment` | 12 | 7 | 5 | 1 | 4 | 0 |
| `inventory.location_inventory` | 9 | 5 | 4 | 1 | 2 | 1 |
| `workforce.workforce_escalation` | 11 | 6 | 5 | 1 | 1 | 0 |
| `relationships.assignment_ticket` | 2 | 2 | 0 | 1 composite | 2 | 0 |
| **Total** | **47** | **29** | **18** | **5** | **13** | **1** |

The 47-column total is derived directly from the locked Enterprise Relational Schema. Together with the 81 approved Tier 0–1 columns, the 13-table pre-migration state contains 128 columns.

The five Tier 2 primary keys and the Location Inventory business-key unique constraint produce exactly six PostgreSQL-managed constraint indexes. No manually defined Tier 2 index is authorized.

---

# Approved PostgreSQL Type Rules

| Logical Type | PostgreSQL Type | Tier 2 Treatment |
|---|---|---|
| `TEXT` | `TEXT` | No governed length limit is introduced. |
| `INTEGER` | `INTEGER` | Direct mapping. |
| `BOOLEAN` | `BOOLEAN` | Native PostgreSQL Boolean type. |
| `DATE` | `DATE` | Native PostgreSQL date type. |

No Tier 2 attribute has the logical type `DECIMAL`. This contract therefore authorizes zero Tier 2 `NUMERIC` columns, and no Tier 2 precision or scale decision is required. The Tier 2 validator must reject an unexpected `NUMERIC` implementation rather than infer precision or scale that the locked schema does not contain.

The absence of Tier 2 `NUMERIC` columns does not alter the five approved Tier 1 `NUMERIC` definitions. Those definitions remain governed by the Tier 1 PostgreSQL Implementation Contract.

PostgreSQL type selection defines storage representation only. It does not authorize minimum-value, maximum-value, sign, formula, date-order, controlled-vocabulary, or cross-field `CHECK` constraints.

---

# Column Contract

Column order follows the locked Enterprise Relational Schema rather than source-file order.

## `vendor.shipment`

| Ordinal | Column | PostgreSQL Type | Nullable | Key or Relationship Treatment |
|---:|---|---|---|---|
| 1 | `shipment_id` | `TEXT` | No | Primary key |
| 2 | `vendor_id` | `TEXT` | No | Foreign key to `vendor.vendor.vendor_id` |
| 3 | `item_id` | `TEXT` | No | Foreign key to `inventory.inventory_item.item_id` |
| 4 | `location_id` | `TEXT` | No | Foreign key to `core.location.location_id` |
| 5 | `related_ticket_id` | `TEXT` | Yes | Optional foreign key to `ticketing.ticket.ticket_id` |
| 6 | `delivery_status` | `TEXT` | No | Provisional source-observed vocabulary; no hard `CHECK` constraint |
| 7 | `ordered_quantity` | `INTEGER` | No | None |
| 8 | `received_quantity` | `INTEGER` | Yes | Nullable while receipt is incomplete |
| 9 | `order_date` | `DATE` | No | None |
| 10 | `expected_delivery_date` | `DATE` | No | None |
| 11 | `actual_delivery_date` | `DATE` | Yes | Nullable while delivery is incomplete |
| 12 | `fulfillment_accuracy_flag` | `BOOLEAN` | Yes | Stored calculated value; not generated through Tier 2 DDL |
| 13 | `delay_flag` | `BOOLEAN` | No | Stored calculated value; not generated through Tier 2 DDL |

Shipment preserves one Inventory Item per record. `item_id` remains single-valued, and no Shipment Line table or repeated item group is authorized.

`related_ticket_id` is an immediately enforceable nullable foreign key because its referenced Tier 1 table already exists. Its optionality does not make the constraint itself deferred.

## `inventory.replenishment`

| Ordinal | Column | PostgreSQL Type | Nullable | Key or Relationship Treatment |
|---:|---|---|---|---|
| 1 | `replenishment_id` | `TEXT` | No | Primary key |
| 2 | `item_id` | `TEXT` | No | Foreign key to `inventory.inventory_item.item_id` |
| 3 | `location_id` | `TEXT` | No | Foreign key to `core.location.location_id` |
| 4 | `vendor_id` | `TEXT` | Yes | Conditional, nullable foreign key to `vendor.vendor.vendor_id` |
| 5 | `related_ticket_id` | `TEXT` | Yes | Optional foreign key to `ticketing.ticket.ticket_id` |
| 6 | `replenishment_type` | `TEXT` | No | Provisional source-observed vocabulary; no hard `CHECK` constraint |
| 7 | `replenishment_status` | `TEXT` | No | Provisional source-observed vocabulary; no hard `CHECK` constraint |
| 8 | `requested_quantity` | `INTEGER` | No | None |
| 9 | `approved_quantity` | `INTEGER` | Yes | Nullable before approval or when approval is not recorded |
| 10 | `request_date` | `DATE` | No | None |
| 11 | `expected_arrival_date` | `DATE` | Yes | Nullable before an arrival expectation is established |
| 12 | `received_date` | `DATE` | Yes | Nullable until receipt |

`vendor_id` remains nullable because an Internal Transfer replenishment may not involve a Vendor. The source-supported distinction between Internal Transfer and Vendor Reorder does not authorize a cross-field Vendor-presence `CHECK` constraint through Tier 2 DDL.

`vendor_id` and `related_ticket_id` are immediately enforceable nullable foreign keys. A non-null value must reference an existing governed parent row.

## `inventory.location_inventory`

| Ordinal | Column | PostgreSQL Type | Nullable | Key or Relationship Treatment |
|---:|---|---|---|---|
| 1 | `location_inventory_id` | `TEXT` | No | Primary key |
| 2 | `item_id` | `TEXT` | No | Foreign key to `inventory.inventory_item.item_id`; second column of business key |
| 3 | `location_id` | `TEXT` | No | Foreign key to `core.location.location_id`; first column of business key |
| 4 | `current_stock` | `INTEGER` | No | None |
| 5 | `stock_status` | `TEXT` | No | Provisional source-observed vocabulary; no hard `CHECK` constraint |
| 6 | `reorder_point` | `INTEGER` | Yes | None |
| 7 | `target_stock_level` | `INTEGER` | Yes | None |
| 8 | `safety_stock_level` | `INTEGER` | Yes | None |
| 9 | `last_count_date` | `DATE` | Yes | None |

The governed business candidate key is (`location_id`, `item_id`). It must be implemented as a unique constraint and must not replace `location_inventory_id` as the primary key.

The table represents the current stock position only. The deferred Shipment-to-Location Inventory analytical and historical relationship remains outside Tier 2.

## `workforce.workforce_escalation`

| Ordinal | Column | PostgreSQL Type | Nullable | Key or Relationship Treatment |
|---:|---|---|---|---|
| 1 | `escalation_id` | `TEXT` | No | Primary key |
| 2 | `related_ticket_id` | `TEXT` | Yes | Optional foreign key to `ticketing.ticket.ticket_id`; new implementation column |
| 3 | `department` | `TEXT` | No | Organizational text |
| 4 | `escalation_type` | `TEXT` | No | Provisional source-observed vocabulary; no hard `CHECK` constraint |
| 5 | `severity_level` | `TEXT` | No | Provisional source-observed vocabulary; no hard `CHECK` constraint |
| 6 | `current_status` | `TEXT` | No | Provisional source-observed vocabulary; no hard `CHECK` constraint |
| 7 | `escalation_date` | `DATE` | No | None |
| 8 | `affected_team` | `TEXT` | Yes | Organizational text |
| 9 | `root_cause` | `TEXT` | Yes | Narrative text; no controlled enumeration |
| 10 | `resolution_owner` | `TEXT` | Yes | Organizational role text; not an Employee reference |
| 11 | `business_impact` | `TEXT` | Yes | Narrative text |

`related_ticket_id` does not exist in the current Workforce Escalations source dataset. It is an approved new nullable column for future records. Tier 2 must not manufacture or backfill historical Ticket values.

No `employee_id`, Coverage Schedule relationship, Workload Record relationship, or other deferred workforce relationship is authorized. `resolution_owner` remains role text and must not receive an Employee foreign key.

## `relationships.assignment_ticket`

| Ordinal | Column | PostgreSQL Type | Nullable | Key or Relationship Treatment |
|---:|---|---|---|---|
| 1 | `assignment_id` | `TEXT` | No | First column of composite primary key; foreign key to `workforce.assignment.assignment_id` |
| 2 | `ticket_id` | `TEXT` | No | Second column of composite primary key; foreign key to `ticketing.ticket.ticket_id` |

The composite key (`assignment_id`, `ticket_id`) is the complete identity of this associative relationship. The table must contain exactly these two columns and must not contain a surrogate identifier, timestamps, status, notes, or other relationship-level attributes.

No current source dataset represents Assignment-to-Ticket pairings. The table begins empty and is populated only through separately governed future operational or migration work.

---

# Source-Transition Contract

| Source | Canonical Tier 2 Treatment |
|---|---|
| `inventory-operations/datasets/data/vendor-shipments.csv` | Supplies the 13 governed Shipment fields. Physical column order follows the Enterprise Relational Schema, not the CSV header. No row is loaded through issue #32. |
| `inventory-operations/datasets/data/replenishment-events.csv` | Supplies the 12 governed Replenishment fields. `vendor_id` remains nullable. No Vendor-presence rule is promoted into DDL. No row is loaded through issue #32. |
| `inventory-operations/datasets/data/location-inventory.csv` | Supplies the 9 governed Location Inventory fields. The governed (`location_id`, `item_id`) business key is added as a database unique constraint. No row is loaded through issue #32. |
| `workforce-coordination/datasets/data/workforce-escalations.csv` | Supplies 10 source fields. The approved relational schema adds nullable `related_ticket_id` as the eleventh canonical column. No historical Ticket value is created, and no row is loaded through issue #32. |
| No current source dataset | `relationships.assignment_ticket` is created with exactly two required foreign-key columns and begins empty. |

All source field names retained by Tier 2 already match their approved canonical column names. No legacy identifier alias is required through this tier.

Source-data normalization, loading, migration, exception handling, and row-level reconciliation remain separately governed work. Issue #32 creates an empty structural boundary only.

---

# Constraint Contract

## Naming Rule

Constraint names use lowercase `snake_case`, begin with the governed table name, name the governed column or columns where needed, and end with the PostgreSQL-standard purpose suffix:

| Constraint Type | Pattern |
|---|---|
| Primary key | `<table>_pkey` |
| Foreign key | `<table>_<column>_fkey` |
| Business-key unique constraint | `<table>_<column_1>_<column_2>_key` |

Schema names are excluded from constraint names because the governed table name supplies the operational object identity and matches the established Tier 0–1 convention.

## Primary Keys

| Table | Constraint Name | Column or Columns |
|---|---|---|
| `vendor.shipment` | `shipment_pkey` | `shipment_id` |
| `inventory.replenishment` | `replenishment_pkey` | `replenishment_id` |
| `inventory.location_inventory` | `location_inventory_pkey` | `location_inventory_id` |
| `workforce.workforce_escalation` | `workforce_escalation_pkey` | `escalation_id` |
| `relationships.assignment_ticket` | `assignment_ticket_pkey` | (`assignment_id`, `ticket_id`) |

The Assignment Ticket column order is governed and must be preserved in both the table definition and the composite primary key.

## Foreign Keys

| Table | Constraint Name | Column | Referenced Column | Nullability | Delete Behavior |
|---|---|---|---|---|---|
| `vendor.shipment` | `shipment_vendor_id_fkey` | `vendor_id` | `vendor.vendor.vendor_id` | Required | `ON DELETE RESTRICT` |
| `vendor.shipment` | `shipment_item_id_fkey` | `item_id` | `inventory.inventory_item.item_id` | Required | `ON DELETE RESTRICT` |
| `vendor.shipment` | `shipment_location_id_fkey` | `location_id` | `core.location.location_id` | Required | `ON DELETE RESTRICT` |
| `vendor.shipment` | `shipment_related_ticket_id_fkey` | `related_ticket_id` | `ticketing.ticket.ticket_id` | Nullable | `ON DELETE RESTRICT` |
| `inventory.replenishment` | `replenishment_item_id_fkey` | `item_id` | `inventory.inventory_item.item_id` | Required | `ON DELETE RESTRICT` |
| `inventory.replenishment` | `replenishment_location_id_fkey` | `location_id` | `core.location.location_id` | Required | `ON DELETE RESTRICT` |
| `inventory.replenishment` | `replenishment_vendor_id_fkey` | `vendor_id` | `vendor.vendor.vendor_id` | Nullable | `ON DELETE RESTRICT` |
| `inventory.replenishment` | `replenishment_related_ticket_id_fkey` | `related_ticket_id` | `ticketing.ticket.ticket_id` | Nullable | `ON DELETE RESTRICT` |
| `inventory.location_inventory` | `location_inventory_item_id_fkey` | `item_id` | `inventory.inventory_item.item_id` | Required | `ON DELETE RESTRICT` |
| `inventory.location_inventory` | `location_inventory_location_id_fkey` | `location_id` | `core.location.location_id` | Required | `ON DELETE RESTRICT` |
| `workforce.workforce_escalation` | `workforce_escalation_related_ticket_id_fkey` | `related_ticket_id` | `ticketing.ticket.ticket_id` | Nullable | `ON DELETE RESTRICT` |
| `relationships.assignment_ticket` | `assignment_ticket_assignment_id_fkey` | `assignment_id` | `workforce.assignment.assignment_id` | Required | `ON DELETE RESTRICT` |
| `relationships.assignment_ticket` | `assignment_ticket_ticket_id_fkey` | `ticket_id` | `ticketing.ticket.ticket_id` | Required | `ON DELETE RESTRICT` |

All 13 foreign keys are immediately enforceable because every referenced Tier 0–1 table exists before Tier 2 creation. Nullable foreign-key columns permit `NULL`; every non-null value must match an existing parent key.

These foreign keys use PostgreSQL's default `MATCH SIMPLE`, `ON UPDATE NO ACTION`, nondeferrable, and initially-immediate behavior. No alternate match, update, or deferrability behavior is authorized.

The 13 Tier 2 foreign keys do not enforce or otherwise alter the still-deferred `ticket_location_id_fkey` and `ticket_employee_id_fkey` constraints on `ticketing.ticket`.

## Location Inventory Business Key

| Table | Constraint Name | Columns |
|---|---|---|
| `inventory.location_inventory` | `location_inventory_location_id_item_id_key` | (`location_id`, `item_id`) |

The unique-constraint column order follows the locked business key. The constraint prevents more than one current stock position for the same Inventory Item at the same Location while preserving `location_inventory_id` as the canonical primary key.

## Constraint-Backed Index Boundary

The five primary keys and one business-key unique constraint produce exactly six PostgreSQL-managed Tier 2 indexes. Foreign-key declarations do not authorize supporting indexes through issue #32.

No manually defined Tier 2 index is authorized. Supporting-index decisions remain outside this implementation checkpoint.

---

# Provisional Constraint Boundary

The following source-observed vocabularies remain provisional and must be stored as unconstrained `TEXT` through Tier 2:

* Shipment `delivery_status`
* Replenishment `replenishment_type`
* Replenishment `replenishment_status`
* Location Inventory `stock_status`
* Workforce Escalation `escalation_type`
* Workforce Escalation `severity_level`
* Workforce Escalation `current_status`

No current-source enumeration becomes a hard `CHECK` constraint without separate review and explicit approval.

The source-schema data-quality statements concerning nonnegative quantities, standardized statuses, or date relationships do not independently authorize physical constraints. Issue #32 must not introduce numeric-range, sign, date-order, cross-field conditional, formula, or lifecycle-state `CHECK` constraints.

---

# Controlled File Responsibilities

## Issue #31 Contract File

| File | Responsibility |
|---|---|
| `postgresql-platform/documentation/tier-2-postgresql-implementation-contract.md` | Records the approved physical contract and the boundary governing issues #32 and #33. Contains no executable SQL. |

## Issue #32 Implementation Files

| File | Responsibility |
|---|---|
| `postgresql-platform/database-definition/tier-2/README.md` | Documents prerequisites, exact Tier 2 inventory, controlled execution, validation, rerun behavior, source-transition treatment, and implementation exclusions. |
| `postgresql-platform/database-definition/tier-2/create-tier-2-tables.sql` | Creates all five Tier 2 tables, 47 columns, five primary keys, 13 foreign keys, and one business-key unique constraint in one transaction. |
| `postgresql-platform/validation/tier-2/validate-tier-2-tables.sql` | Validates the exact five-table Tier 2 physical structure without taking ownership of the cumulative repository-wide inventory. |
| `postgresql-platform/validation/implementation-foundation/validate-implementation-foundation.sql` | Evolves the cumulative pre-migration validator from the eight-table Tier 0–1 state to the approved 13-table Tier 0–2 state. |

No additional Tier 2 creation file, migration file, generated output, trigger file, index file, data file, or source-correction file is authorized through issue #32.

## Issue #33 Lifecycle-Evidence File

| File | Responsibility |
|---|---|
| `postgresql-platform/validation/implementation-foundation/tier-2-lifecycle-validation.md` | Preserves repository-controlled evidence that the approved Tier 0–2 boundary persists across normal teardown and can be reconstructed from committed files after a separately authorized clean local reset. Contains no executable SQL. |

Issue #33 must not rewrite `implementation-foundation-validation.md` or `tier-1-lifecycle-validation.md`. Both remain unchanged historical evidence for their earlier tested boundaries.

---

# Validation Boundaries

## Schema Namespace Validator

`postgresql-platform/validation/schema-namespaces/validate-schema-namespaces.sql` remains unchanged. It continues to validate the six approved schemas and ownership without counting later objects.

## Tier 0 Structural Validator

`postgresql-platform/validation/tier-0/validate-tier-0-tables.sql` remains unchanged. It continues to validate only `core.location`, `workforce.employee`, and `vendor.vendor`. Tier 2 objects must not create false Tier 0 failures.

## Tier 1 Structural Validator

`postgresql-platform/validation/tier-1/validate-tier-1-tables.sql` remains unchanged. It continues to validate only the five approved Tier 1 tables and must not reject approved Tier 2 tables that share the `inventory` or `workforce` schemas.

## Tier 2 Structural Validator

The Tier 2 validator must validate exactly the five named Tier 2 tables and all 47 columns, including:

* schema and table identity
* column order and names
* PostgreSQL types
* the absence of Tier 2 `NUMERIC` columns
* exact nullability, including all 29 approved `NOT NULL` columns
* absence of defaults, identity behavior, and generated expressions
* table ownership by `northstar_local_admin`
* the five governed primary-key names, columns, and column order
* the 13 governed foreign-key names, columns, references, nullability states, and deletion behavior
* PostgreSQL default `MATCH SIMPLE`, `ON UPDATE NO ACTION`, nondeferrable, and initially-immediate foreign-key behavior
* the Location Inventory business-key unique constraint
* absence of provisional ordinary `CHECK` constraints and other unapproved constraints
* exactly six Tier 2 constraint-backed indexes and no manually defined Tier 2 indexes
* the exact two-column Assignment Ticket boundary
* zero rows in all five Tier 2 tables before migration

The Tier 2 validator must scope structural checks to the five fully qualified Tier 2 tables. It must not use shared-schema table counts that would falsely reject later approved tiers.

## Cumulative Pre-Migration Validator

The cumulative implementation-foundation validator must evolve to accept exactly:

* PostgreSQL `18.4`
* database `northstar`
* authenticated user and schema owner `northstar_local_admin`
* the six approved schemas
* the three approved Tier 0 tables
* the five approved Tier 1 tables
* the five approved Tier 2 tables
* exactly 13 approved tables across the governed schemas
* zero rows across all 13 tables
* an empty `public` schema
* no Tier 3–5 table, unapproved relation, routine, trigger, policy, event trigger, or other user-defined supporting object

The cumulative validator owns the exact 13-table repository-wide inventory. The namespace, Tier 0, Tier 1, and Tier 2 validators retain their narrower structural responsibilities. Together, the tier-specific validators confirm the exact 128-column Tier 0–2 boundary; the cumulative validator must not duplicate or weaken those column-level contracts.

The committed issue #9 evidence file, `postgresql-platform/validation/implementation-foundation/implementation-foundation-validation.md`, and the committed Tier 1 evidence file, `postgresql-platform/validation/implementation-foundation/tier-1-lifecycle-validation.md`, must remain byte-for-byte unchanged. Evolving the live validator and procedure does not rewrite past evidence.

---

# Tier 2 Lifecycle-Validation Boundary

Issue #33 must validate the exact committed Tier 2 implementation produced through issue #32. The lifecycle procedure must preserve the established safety separation between normal teardown and destructive local reset.

The Tier 2 evidence must demonstrate:

1. the tested commit and clean working-tree boundary
2. successful repository and credential-exclusion checks
3. runtime health and PostgreSQL `18.4` identity
4. successful execution of the namespace, Tier 0, Tier 1, Tier 2, and cumulative validators against the implemented 13-table state
5. persistence of the validated database state across normal teardown and restart
6. a separately authorized deletion of only the named local volume `northstar-postgresql-data`
7. clean recreation of the local environment
8. repository-controlled reconstruction in the exact order namespaces → Tier 0 → Tier 1 → Tier 2
9. successful rerun of all five validators after reconstruction
10. final confirmation of six schemas, 13 tables, 128 columns across the tier validators, zero rows, an empty `public` schema, and a healthy runtime

The lifecycle evidence must record actual observed output and the exact tested commit. Expected counts or internally consistent documentation do not substitute for execution evidence.

No destructive reset command is authorized by this contract. The reset step requires fresh user authorization during issue #33 that identifies `northstar-postgresql-data` as the only approved deletion target.

---

# Required README Boundary Changes for Issue #32

Issue #32 must update the following documentation in the same implementation checkpoint:

| File | Required Change |
|---|---|
| `postgresql-platform/README.md` | Replace the Tier 1 active-state language with the implemented Tier 2 boundary; add the Tier 2 definition and validation files to the governed tree; preserve earlier checkpoints as completed history. |
| `postgresql-platform/database-definition/README.md` | Add Tier 2 to the current executable boundary and record `tier-2/create-tier-2-tables.sql` in the controlled build order. |
| `postgresql-platform/database-definition/tier-2/README.md` | Create the controlled Tier 2 creation, validation, rerun, source-transition, and exclusion guide. |
| `postgresql-platform/validation/README.md` | Add the Tier 2 structural validator and describe the evolved 13-table cumulative boundary. |
| `postgresql-platform/validation/implementation-foundation/README.md` | Evolve the live procedure to rebuild namespaces → Tier 0 → Tier 1 → Tier 2, run all five validators, and expect six schemas, 13 tables, 128 columns across the tier-specific validators, zero rows, and `PASS`. Preserve earlier evidence files as historical evidence. |
| `postgresql-platform/documentation/README.md` | Register this contract as the Tier 2 traceability artifact governing issues #32 and #33. |

No change is required to `postgresql-platform/local-environment/README.md`, `postgresql-platform/migrations/README.md`, the locked enterprise architecture documents, the issue #9 evidence file, or the Tier 1 lifecycle-evidence file through Tier 2 structural implementation.

---

# Prohibited Tier 2 Additions

Issue #32 must not introduce:

* source data or `INSERT`, `COPY`, staging, or migration logic
* changes to the two deferred Ticket foreign keys on `ticketing.ticket.location_id` or `ticketing.ticket.employee_id`
* historical Workforce Escalation Ticket backfill or manufactured `related_ticket_id` values
* an Employee foreign key on Workforce Escalation `resolution_owner`
* Workforce Escalation `employee_id`, Coverage Schedule, or Workload Record relationship columns or tables
* a Shipment Line table or multi-item Shipment redesign
* Shipment Replenishment Allocation or any other Tier 3–5 structure
* a surrogate key or relationship-level attribute on Assignment Ticket
* a primary-key substitution for the Location Inventory business key
* provisional controlled-vocabulary `CHECK` constraints
* minimum, maximum, sign, date-order, formula, or cross-field `CHECK` constraints
* defaults, identity columns, or generated expressions
* triggers, functions, procedures, views, materialized views, policies, grants, or roles
* manually defined indexes
* persistent staging, reporting, or reference schemas
* source normalization, Ticket mapping, or exception-resolution logic

---

# Issue #31 Acceptance Mapping

| Acceptance Criterion | Contract Resolution |
|---|---|
| All 47 Tier 2 columns reconciled | Five tables and 47 columns are enumerated with exact order, type, and nullability. |
| PostgreSQL types approved | Every column has an explicit PostgreSQL 18 type. |
| `NUMERIC` precision and scale approved | The locked Tier 2 schema contains zero `NUMERIC` columns; no precision or scale is invented. |
| Five primary keys confirmed | All five names and ordered columns are fixed, including the Assignment Ticket composite key. |
| Thirteen foreign keys confirmed | All 13 names, columns, references, nullability states, and `ON DELETE RESTRICT` behavior are fixed. |
| Optional Ticket and Vendor references preserved | Shipment, Replenishment, and Workforce Escalation optional references remain nullable and enforce non-null values. |
| Location Inventory business key confirmed | (`location_id`, `item_id`) is fixed as a named unique constraint without replacing the primary key. |
| Assignment Ticket boundary confirmed | Exactly two required columns, two foreign keys, and one composite primary key are authorized. |
| One-item-per-Shipment scope preserved | Shipment retains one `item_id`; Shipment Line is prohibited. |
| Conditional Replenishment Vendor nullability preserved | `vendor_id` is nullable and no cross-field Vendor-presence constraint is authorized. |
| Workforce Escalation transition preserved | `related_ticket_id` is new and nullable; historical backfill and Employee reinterpretation are prohibited. |
| Provisional vocabularies remain unimplemented | Seven source-observed vocabularies remain unconstrained `TEXT`. |
| Constraint names governed | Primary-key, foreign-key, and unique-constraint patterns and exact names are fixed. |
| Create-file and validator-file responsibilities approved | Exact issue #32 file paths and responsibilities are defined. |
| Cumulative validator boundary approved | The exact 13-table, zero-row pre-migration state is separated from tier-specific structural validation. |
| README responsibilities identified | Six documentation targets and their required changes are defined. |
| Lifecycle-evidence responsibility identified | Issue #33 owns one dedicated Tier 2 evidence file and must preserve earlier evidence unchanged. |
| No Tier 2 DDL created | This file contains no executable SQL and authorizes none through issue #31. |
| Completion evidence linked | Satisfied by the commit that introduces this file and its linkage in issue #31; the final commit cannot contain its own commit SHA. |

---

# Reconciliation Record

Issue #31 reconciliation confirmed the locked aggregate counts without changing architecture:

* Shipment: 13 columns
* Replenishment: 12 columns
* Location Inventory: 9 columns
* Workforce Escalation: 11 columns, including the approved new nullable `related_ticket_id`
* Assignment Ticket: 2 columns
* Tier 2 total: 47 columns, 29 required and 18 nullable

No Tier 2 `NUMERIC` field exists. The issue requirement to approve precision and scale is satisfied by recording that the authoritative schema authorizes zero such fields.

The four outbound Ticket foreign keys approved in the Tier 2 architecture consist of three nullable references—Shipment `related_ticket_id`, Replenishment `related_ticket_id`, and Workforce Escalation `related_ticket_id`—plus the required Assignment Ticket `ticket_id` relationship. None of these relationships authorizes enforcement of the separate deferred Location and Employee foreign keys on `ticketing.ticket`.

No canonical table, column, logical type, nullability rule, identifier, key, or relationship was changed through this physical reconciliation.

---

# Completion Boundary

Issue #31 is complete only when:

1. this one-file physical contract passes independent technical and governance review
2. any required corrections are applied and revalidated
3. the authority and status metadata are changed from proposed to approved
4. the approved file is committed separately without Tier 2 DDL or unrelated changes
5. the evidence commit is linked to issue #31
6. every issue #31 acceptance criterion is confirmed
7. issue #31 is closed as completed

Issue #32 must remain in Backlog until this completion boundary is satisfied.
