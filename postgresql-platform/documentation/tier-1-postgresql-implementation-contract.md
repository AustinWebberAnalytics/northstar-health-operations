# Tier 1 PostgreSQL Implementation Contract

## Northstar Health Operations

---

**Primary Audience:** Northstar architects, data engineers, subsystem maintainers, and reviewers implementing or validating the approved Tier 1 PostgreSQL structures

**Writing Layer:** Layer 2 — Operational / Architectural

**Architectural Purpose:** Defines the physical PostgreSQL types, column order, nullability, keys, constraint names, staged-reference treatment, file responsibilities, validation boundaries, and documentation changes governing Tier 1 implementation.

**Document Type:** PostgreSQL Implementation Contract

**Authority Level:** Approved Physical Implementation Contract

**Status:** Approved — Issue #28 Tier 1 Contract

**Depends On:** Enterprise Relational Schema, Enterprise Relational Foundation, Enterprise Database Platform Decision, Enterprise Logical Model, Cross-System Identifier Dictionary, Naming Convention Standards, Project Governance Standards, and the completed PostgreSQL implementation foundation

---

# Purpose

This contract translates the locked, platform-neutral Tier 1 relational design into an exact PostgreSQL 18 implementation boundary before executable Tier 1 SQL is created.

The locked architecture remains authoritative for object meaning, relationships, identifiers, logical types, and nullability. This document resolves only the physical decisions explicitly delegated to SQL implementation: PostgreSQL type mapping, `NUMERIC` precision and scale, constraint names and properties, file responsibilities, validator boundaries, and required documentation changes.

If this contract conflicts with a newer approved governance or architecture artifact, the newer higher-authority artifact controls and the discrepancy must be resolved before implementation continues.

---

# Implementation Boundary

Issue #28 approves a physical implementation contract only.

This issue does not create tables, execute SQL, load source data, perform migration, reconcile Ticket references, enforce the deferred Ticket foreign keys, normalize source files, create provisional `CHECK` constraints, add triggers, add manually defined indexes, or implement Tier 2–5 structures.

Executable Tier 1 work remains governed by issue #29. Lifecycle validation and completion evidence remain governed by issue #30.

---

# Approved Tier 1 Inventory

| Table | Columns | Required | Nullable | Primary Keys | Immediate Foreign Keys | Deferred Foreign Keys | Business-Key Unique Constraints |
|---|---:|---:|---:|---:|---:|---:|---:|
| `inventory.inventory_item` | 7 | 6 | 1 | 1 | 1 | 0 | 0 |
| `ticketing.ticket` | 22 | 10 | 12 | 1 | 0 | 2 | 0 |
| `workforce.assignment` | 10 | 8 | 2 | 1 | 1 | 0 | 0 |
| `workforce.coverage_schedule` | 9 | 5 | 4 | 1 | 1 | 0 | 0 |
| `workforce.workload_record` | 10 | 7 | 3 | 1 | 1 | 0 | 1 |
| **Total** | **58** | **36** | **22** | **5** | **4** | **2** | **1** |

The 58-column total is derived directly from the locked Enterprise Relational Schema. Together with the 23 approved Tier 0 columns, the eight-table pre-migration state contains 81 columns.

---

# Approved PostgreSQL Type Rules

| Logical Type | PostgreSQL Type | Tier 1 Treatment |
|---|---|---|
| `TEXT` | `TEXT` | No governed length limit is introduced. |
| `INTEGER` | `INTEGER` | Direct mapping. |
| `DECIMAL` representing elapsed or workload hours | `NUMERIC(10,2)` | Stores exact hundredth-hour values with a broad operational range. |
| `DECIMAL` representing a percentage | `NUMERIC(5,2)` | Stores exact hundredth-percentage-point values through `999.99` without implying a `0`–`100` rule. |
| `BOOLEAN` | `BOOLEAN` | Native PostgreSQL Boolean type. |
| `DATE` | `DATE` | Native PostgreSQL date type. |
| `TIMESTAMP` | `TIMESTAMP WITHOUT TIME ZONE` | Preserves the approved timezone-naive source boundary. |

The five Tier 1 `NUMERIC` fields are approved as follows:

| Table | Column | PostgreSQL Type | Basis |
|---|---|---|---|
| `ticketing.ticket` | `resolution_hours` | `NUMERIC(10,2)` | Current calculated values use no more than two decimal places; fractional elapsed hours remain meaningful. |
| `ticketing.ticket` | `response_hours` | `NUMERIC(10,2)` | Current calculated values use no more than two decimal places; fractional elapsed hours remain meaningful. |
| `workforce.workload_record` | `estimated_hours` | `NUMERIC(10,2)` | Current source values are whole hours, but planned effort may legitimately require fractional hours. |
| `workforce.workload_record` | `actual_hours` | `NUMERIC(10,2)` | Current source values are whole hours, but recorded effort may legitimately require fractional hours. |
| `workforce.workload_record` | `capacity_utilization_percent` | `NUMERIC(5,2)` | Exact percentage storage is required; values above `100.00` remain representable without approving a range constraint. |

Precision and scale define storage representation only. They do not authorize minimum-value, maximum-value, sign, formula, or cross-field `CHECK` constraints.

---

# Column Contract

Column order follows the locked Enterprise Relational Schema rather than source-file order.

## `inventory.inventory_item`

| Ordinal | Column | PostgreSQL Type | Nullable | Key or Relationship Treatment |
|---:|---|---|---|---|
| 1 | `item_id` | `TEXT` | No | Primary key |
| 2 | `item_category` | `TEXT` | No | None |
| 3 | `criticality_level` | `TEXT` | No | None |
| 4 | `unit_of_measure` | `TEXT` | No | None |
| 5 | `preferred_vendor_id` | `TEXT` | Yes | Immediate foreign key to `vendor.vendor.vendor_id` |
| 6 | `active_flag` | `BOOLEAN` | No | None |
| 7 | `item_name` | `TEXT` | No | None |

`preferred_vendor_id` represents only the approved preferred-sourcing role. It does not implement the deferred canonical Vendor-to-Inventory Item many-to-many relationship.

## `ticketing.ticket`

| Ordinal | Column | PostgreSQL Type | Nullable | Key or Relationship Treatment |
|---:|---|---|---|---|
| 1 | `ticket_id` | `TEXT` | No | Primary key |
| 2 | `category` | `TEXT` | No | None |
| 3 | `priority` | `TEXT` | No | None |
| 4 | `status` | `TEXT` | No | None |
| 5 | `escalation_flag` | `BOOLEAN` | No | None |
| 6 | `reopened_flag` | `BOOLEAN` | No | None |
| 7 | `pending_flag` | `BOOLEAN` | No | None |
| 8 | `sla_target_hours` | `INTEGER` | No | None |
| 9 | `sla_met_flag` | `BOOLEAN` | Yes | None |
| 10 | `requesting_location` | `TEXT` | Yes | Retained legacy source value |
| 11 | `location_id` | `TEXT` | Yes | Canonical Location reference column; foreign key deferred |
| 12 | `assigned_department` | `TEXT` | No | None |
| 13 | `assigned_owner` | `TEXT` | Yes | Retained legacy source value |
| 14 | `employee_id` | `TEXT` | Yes | Canonical Employee reference column; foreign key deferred |
| 15 | `created_at` | `TIMESTAMP WITHOUT TIME ZONE` | No | None |
| 16 | `first_response_at` | `TIMESTAMP WITHOUT TIME ZONE` | Yes | None |
| 17 | `resolved_at` | `TIMESTAMP WITHOUT TIME ZONE` | Yes | None |
| 18 | `closed_at` | `TIMESTAMP WITHOUT TIME ZONE` | Yes | None |
| 19 | `resolution_hours` | `NUMERIC(10,2)` | Yes | Stored calculated value; not generated through Tier 1 DDL |
| 20 | `response_hours` | `NUMERIC(10,2)` | Yes | Stored calculated value; not generated through Tier 1 DDL |
| 21 | `summary` | `TEXT` | Yes | None |
| 22 | `resolution_notes` | `TEXT` | Yes | None |

Initial Tier 1 creation must not add a foreign key on `location_id` or `employee_id`. Both canonical columns remain nullable while `requesting_location` and `assigned_owner` preserve the source values needed for reconciliation.

Before Ticket migration or validation begins, `ticketing-system/datasets/data/tickets-v1.csv` must be normalized from Windows-1252 to UTF-8 through its separately governed migration prerequisite. Issue #28 does not modify that file.

## `workforce.assignment`

| Ordinal | Column | PostgreSQL Type | Nullable | Key or Relationship Treatment |
|---:|---|---|---|---|
| 1 | `assignment_id` | `TEXT` | No | Primary key |
| 2 | `employee_id` | `TEXT` | No | Immediate foreign key to `workforce.employee.employee_id` |
| 3 | `assignment_category` | `TEXT` | No | None |
| 4 | `assignment_status` | `TEXT` | No | None |
| 5 | `start_date` | `DATE` | No | None |
| 6 | `end_date` | `DATE` | Yes | None |
| 7 | `assignment_name` | `TEXT` | No | None |
| 8 | `priority_level` | `TEXT` | No | None |
| 9 | `estimated_hours_per_week` | `INTEGER` | Yes | None |
| 10 | `cross_functional_flag` | `BOOLEAN` | No | None |

No business-key unique constraint is approved for Assignment. Assignment-to-Ticket and Assignment-to-Corrective Action relationships remain governed through later associative entities, not through new Tier 1 columns.

## `workforce.coverage_schedule`

| Ordinal | Column | PostgreSQL Type | Nullable | Key or Relationship Treatment |
|---:|---|---|---|---|
| 1 | `coverage_schedule_id` | `TEXT` | No | Primary key; canonical replacement for legacy `schedule_id` |
| 2 | `employee_id` | `TEXT` | No | Immediate foreign key to `workforce.employee.employee_id` |
| 3 | `schedule_date` | `DATE` | No | None |
| 4 | `shift_type` | `TEXT` | No | None |
| 5 | `coverage_status` | `TEXT` | No | None |
| 6 | `scheduled_hours` | `INTEGER` | Yes | None |
| 7 | `coverage_area` | `TEXT` | Yes | Descriptive text; not a Location reference |
| 8 | `coverage_priority` | `TEXT` | Yes | None |
| 9 | `backup_required_flag` | `BOOLEAN` | Yes | None |

No `location_id`, business-key unique constraint, overlap constraint, time-boundary column, or Assignment relationship is authorized. The overlap rule remains structurally deferred because no governed coverage start/end times or shift-window definition exists.

## `workforce.workload_record`

| Ordinal | Column | PostgreSQL Type | Nullable | Key or Relationship Treatment |
|---:|---|---|---|---|
| 1 | `workload_record_id` | `TEXT` | No | Primary key; canonical replacement for legacy `workload_id` |
| 2 | `employee_id` | `TEXT` | No | Immediate foreign key to `workforce.employee.employee_id` |
| 3 | `reporting_period` | `TEXT` | No | Second column of approved business key |
| 4 | `workload_status` | `TEXT` | No | None |
| 5 | `assigned_tasks` | `INTEGER` | No | None |
| 6 | `completed_tasks` | `INTEGER` | No | None |
| 7 | `open_tasks` | `INTEGER` | No | None |
| 8 | `estimated_hours` | `NUMERIC(10,2)` | Yes | Stored value; not generated through Tier 1 DDL |
| 9 | `actual_hours` | `NUMERIC(10,2)` | Yes | Stored value; not generated through Tier 1 DDL |
| 10 | `capacity_utilization_percent` | `NUMERIC(5,2)` | Yes | Stored calculated value; not generated through Tier 1 DDL |

The business candidate key is (`employee_id`, `reporting_period`). It must be implemented as a unique constraint and must not replace `workload_record_id` as the primary key.

---

# Constraint Contract

## Naming Rule

Constraint names use lowercase `snake_case`, begin with the governed table name, name the governed column or columns where needed, and end with the PostgreSQL-standard purpose suffix:

| Constraint Type | Pattern |
|---|---|
| Primary key | `<table>_pkey` |
| Foreign key | `<table>_<column>_fkey` |
| Business-key unique constraint | `<table>_<column_1>_<column_2>_key` |

Schema names are excluded from constraint names because the governed table name already supplies the operational object identity and matches the established Tier 0 primary-key convention.

## Primary Keys

| Table | Constraint Name | Column |
|---|---|---|
| `inventory.inventory_item` | `inventory_item_pkey` | `item_id` |
| `ticketing.ticket` | `ticket_pkey` | `ticket_id` |
| `workforce.assignment` | `assignment_pkey` | `assignment_id` |
| `workforce.coverage_schedule` | `coverage_schedule_pkey` | `coverage_schedule_id` |
| `workforce.workload_record` | `workload_record_pkey` | `workload_record_id` |

## Immediately Enforceable Foreign Keys

| Table | Constraint Name | Column | Referenced Column | Nullability | Delete Behavior |
|---|---|---|---|---|---|
| `inventory.inventory_item` | `inventory_item_preferred_vendor_id_fkey` | `preferred_vendor_id` | `vendor.vendor.vendor_id` | Nullable | `ON DELETE RESTRICT` |
| `workforce.assignment` | `assignment_employee_id_fkey` | `employee_id` | `workforce.employee.employee_id` | Required | `ON DELETE RESTRICT` |
| `workforce.coverage_schedule` | `coverage_schedule_employee_id_fkey` | `employee_id` | `workforce.employee.employee_id` | Required | `ON DELETE RESTRICT` |
| `workforce.workload_record` | `workload_record_employee_id_fkey` | `employee_id` | `workforce.employee.employee_id` | Required | `ON DELETE RESTRICT` |

These foreign keys use PostgreSQL's default `MATCH SIMPLE`, `ON UPDATE NO ACTION`, nondeferrable, and initially-immediate behavior. No alternate match, update, or deferrability behavior is authorized.

## Deferred Ticket Foreign Keys

| Table | Reserved Constraint Name | Column | Future Referenced Column | Initial Tier 1 Treatment |
|---|---|---|---|---|
| `ticketing.ticket` | `ticket_location_id_fkey` | `location_id` | `core.location.location_id` | Column created nullable; constraint absent |
| `ticketing.ticket` | `ticket_employee_id_fkey` | `employee_id` | `workforce.employee.employee_id` | Column created nullable; constraint absent |

The names are reserved for the later governed enforcement step. Reserving them does not authorize their creation through issue #29.

## Workload Record Business Key

| Table | Constraint Name | Columns |
|---|---|---|
| `workforce.workload_record` | `workload_record_employee_id_reporting_period_key` | (`employee_id`, `reporting_period`) |

The five primary keys and one business-key unique constraint produce exactly six PostgreSQL-managed constraint indexes on Tier 1 tables. No manually defined index is authorized. Foreign-key declarations do not authorize supporting indexes through this issue.

---

# Legacy Identifier Alias Contract

| Source Field | Canonical PostgreSQL Column | Treatment |
|---|---|---|
| `schedule_id` | `coverage_schedule_id` | Rename during migration transformation; preserve `schedule_id` only in source-mapping documentation. |
| `workload_id` | `workload_record_id` | Rename during migration transformation; preserve `workload_id` only in source-mapping documentation. |

The canonical Tier 1 tables must not contain `schedule_id` or `workload_id` columns. The aliases are migration inputs, not competing identifiers.

Ticket `requesting_location` and `assigned_owner` are different: they are approved staged source-value columns retained temporarily beside nullable canonical references. They are not identifier aliases for `location_id` or `employee_id` and must not be treated as direct renames.

---

# Controlled File Responsibilities

## Issue #28 Contract File

| File | Responsibility |
|---|---|
| `postgresql-platform/documentation/tier-1-postgresql-implementation-contract.md` | Records the approved physical contract and the boundary governing issues #29 and #30. Contains no executable SQL. |

## Issue #29 Implementation Files

| File | Responsibility |
|---|---|
| `postgresql-platform/database-definition/tier-1/README.md` | Documents prerequisites, exact Tier 1 inventory, controlled execution, validation, rerun behavior, and implementation exclusions. |
| `postgresql-platform/database-definition/tier-1/create-tier-1-tables.sql` | Creates all five Tier 1 tables, 58 columns, five primary keys, four immediate foreign keys, and one business-key unique constraint in one transaction. |
| `postgresql-platform/validation/tier-1/validate-tier-1-tables.sql` | Validates the exact five-table Tier 1 physical structure without taking ownership of the cumulative repository-wide inventory. |
| `postgresql-platform/validation/implementation-foundation/validate-implementation-foundation.sql` | Evolves the cumulative pre-migration validator from the three-table issue #9 state to the approved eight-table Tier 0–1 state. |

No additional Tier 1 creation file, migration file, generated output, trigger file, index file, or data file is authorized through issue #29.

---

# Validation Boundaries

## Schema Namespace Validator

`postgresql-platform/validation/schema-namespaces/validate-schema-namespaces.sql` remains unchanged. It continues to validate the six approved schemas and ownership without counting later objects.

## Tier 0 Structural Validator

`postgresql-platform/validation/tier-0/validate-tier-0-tables.sql` remains unchanged. It continues to validate only `core.location`, `workforce.employee`, and `vendor.vendor`. Tier 1 objects must not create false Tier 0 failures.

## Tier 1 Structural Validator

The Tier 1 validator must validate exactly the five named Tier 1 tables and all 58 columns, including:

* schema and table identity
* column order and names
* PostgreSQL types
* `NUMERIC` precision and scale
* exact nullability, including all 36 approved `NOT NULL` columns
* absence of defaults, identity behavior, and generated expressions
* table ownership by `northstar_local_admin`
* the five governed primary-key names and columns
* the four governed immediate foreign-key names, columns, references, and deletion behavior
* absence of `ticket_location_id_fkey` and `ticket_employee_id_fkey`
* the Workload Record business-key unique constraint
* absence of unapproved ordinary `CHECK` constraints and other constraints
* exactly six Tier 1 constraint-backed indexes and no manually defined Tier 1 indexes
* zero rows in all five Tier 1 tables before migration

The Tier 1 validator must scope structural checks to the five fully qualified Tier 1 tables. It must not use shared-schema table counts that would falsely reject later approved tiers.

## Cumulative Pre-Migration Validator

The cumulative implementation-foundation validator must evolve to accept exactly:

* PostgreSQL `18.4`
* database `northstar`
* authenticated user and schema owner `northstar_local_admin`
* the six approved schemas
* the three approved Tier 0 tables
* the five approved Tier 1 tables
* exactly eight approved tables across the governed schemas
* zero rows across all eight tables
* an empty `public` schema
* no Tier 2–5 table, unapproved relation, routine, trigger, policy, event trigger, or other user-defined supporting object

The cumulative validator owns the exact eight-table repository-wide inventory. The namespace, Tier 0, and Tier 1 validators retain their narrower structural responsibilities.

The committed issue #9 evidence file, `postgresql-platform/validation/implementation-foundation/implementation-foundation-validation.md`, must remain byte-for-byte unchanged as the historical record of the three-table foundation validation. Evolving the live validator and procedure does not rewrite past evidence.

---

# Required README Boundary Changes for Issue #29

Issue #29 must update the following documentation in the same implementation checkpoint:

| File | Required Change |
|---|---|
| `postgresql-platform/README.md` | Replace the issue #9 active-state language with the implemented Tier 1 boundary; add the Tier 1 definition and validation files to the governed tree; preserve issue #9 as completed history. |
| `postgresql-platform/database-definition/README.md` | Add Tier 1 to the current executable boundary and record `tier-1/create-tier-1-tables.sql` in the controlled build order. |
| `postgresql-platform/database-definition/tier-1/README.md` | Create the controlled Tier 1 creation, validation, rerun, and exclusion guide. |
| `postgresql-platform/validation/README.md` | Add the Tier 1 structural validator and describe the evolved eight-table cumulative boundary. |
| `postgresql-platform/validation/implementation-foundation/README.md` | Evolve the live procedure to rebuild namespaces → Tier 0 → Tier 1, run all four validators, and expect six schemas, eight tables, 81 columns across the tier-specific validators, zero rows, and `PASS`. Preserve the issue #9 evidence file as historical evidence. |
| `postgresql-platform/documentation/README.md` | Register this contract as the implemented Tier 1 traceability artifact. |

No change is required to `postgresql-platform/local-environment/README.md`, `postgresql-platform/migrations/README.md`, the locked enterprise architecture documents, or the issue #9 evidence file through Tier 1 structural implementation.

---

# Prohibited Tier 1 Additions

Issue #29 must not introduce:

* source data or `INSERT`, `COPY`, or staging logic
* `schedule_id` or `workload_id` canonical columns
* Ticket foreign keys on `location_id` or `employee_id`
* Ticket `NOT NULL` promotion for `location_id` or `employee_id`
* provisional controlled-vocabulary `CHECK` constraints
* minimum, maximum, sign, percentage-range, or cross-field `CHECK` constraints
* defaults, identity columns, or generated expressions
* triggers, functions, procedures, views, materialized views, policies, grants, or roles
* manually defined indexes
* persistent staging, reporting, or reference schemas
* Tier 2–5 tables or associative entities
* migration, source normalization, Ticket mapping, or exception-resolution logic

---

# Issue #28 Acceptance Mapping

| Acceptance Criterion | Contract Resolution |
|---|---|
| All Tier 1 columns reconciled | Five tables and 58 columns are enumerated with exact order, type, and nullability. |
| PostgreSQL types approved | Every column has an explicit PostgreSQL 18 type. |
| `NUMERIC` precision and scale approved | Four hour fields use `NUMERIC(10,2)` and one percentage field uses `NUMERIC(5,2)`. |
| Five primary keys confirmed | All five names and columns are fixed. |
| Four immediate Tier 0 foreign keys confirmed | All four names, columns, references, nullability states, and delete behavior are fixed. |
| Two Ticket foreign keys deferred | Both columns remain nullable and both reserved constraints remain absent. |
| Workload Record business key confirmed | (`employee_id`, `reporting_period`) is fixed as a named unique constraint. |
| Constraint names governed | Primary-key, foreign-key, and unique-constraint patterns and exact names are fixed. |
| Create-file and validator-file responsibilities approved | Exact issue #29 file paths and responsibilities are defined. |
| Cumulative validator boundary approved | The exact eight-table, zero-row pre-migration state is defined separately from tier-specific validation. |
| Legacy aliases documented | `schedule_id` and `workload_id` are limited to migration source mapping. |
| README changes identified | Six documentation targets and their required changes are defined. |
| No Tier 1 DDL created | This file contains no executable SQL and authorizes none through issue #28. |
| Completion evidence linked | Satisfied by the commit that introduces this file and its linkage in issue #28; the final commit cannot contain its own commit SHA. |

---

# Discrepancy Record

During issue #28 reconciliation, the planned aggregate count of 57 Tier 1 columns was found to be incorrect. The locked Enterprise Relational Schema contains 58 columns because Workload Record contains 10 columns. Issues #28 and #29 were corrected before this contract was drafted.

No canonical table, column, logical type, nullability rule, identifier, key, or relationship changed. The correction affected only the aggregate planning count.

---

# Completion Boundary

Issue #28 is complete only when:

1. this one-file physical contract passes independent technical and governance review
2. any required corrections are applied and revalidated
3. the approved file is committed separately without Tier 1 DDL or unrelated changes
4. the evidence commit is linked to issue #28
5. every issue #28 acceptance criterion is confirmed
6. issue #28 is closed as completed

Issue #29 must remain in Backlog until this completion boundary is satisfied.
