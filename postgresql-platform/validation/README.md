# Validation

## Northstar Enterprise

---

**Primary Audience:** Data engineers, analysts, subsystem maintainers, and reviewers verifying PostgreSQL implementation quality

**Writing Layer:** Layer 2 — Operational / Analyst

**Architectural Purpose:** Defines the repository boundary for repeatable structural, migration, data-quality, and relational-integrity validation.

---

# Purpose

This directory contains repeatable checks that demonstrate whether the PostgreSQL implementation matches approved architecture and governed source data.

Validation reports failures. It must not silently repair data or alter the approved database definition.

---

# Validation Scope

Future approved validation may include:

* PostgreSQL version and namespace checks
* table, column, key, and constraint verification
* Tier 0–5 dependency verification
* source-to-target row-count reconciliation
* identifier and foreign-key integrity checks
* migration exception verification
* approved cross-table and aggregate rule checks
* reset and rebuild repeatability checks

Validation should be read-only wherever practical. Any check requiring temporary objects or transaction-scoped test data must document and contain those effects.

---

# Implemented Validation

| File | Responsibility |
|---|---|
| `schema-namespaces/validate-schema-namespaces.sql` | Fails when an approved namespace is missing and reports all six namespace owners when validation succeeds. |
| `tier-0/validate-tier-0-tables.sql` | Fails on any governed Tier 0 structural mismatch and reports all 23 validated columns, primary keys, and table owners when validation succeeds. |
| `tier-1/validate-tier-1-tables.sql` | Fails on any governed Tier 1 structural mismatch and reports the validated five-table, 58-column, key, foreign-key, unique-constraint, index, ownership, and zero-row boundary when validation succeeds. |
| `tier-2/validate-tier-2-tables.sql` | Fails on any governed Tier 2 structural mismatch and reports the validated five-table, 47-column, key, foreign-key, unique-constraint, index, ownership, and zero-row boundary when validation succeeds. |
| `implementation-foundation/validate-implementation-foundation.sql` | Fails when the runtime identity, namespace ownership, exact 13-table pre-migration object inventory, empty `public` schema, deferred Ticket relationship boundary, or zero-row boundary differs from the approved state. |
| `source-data/ticket-source-encoding-validation.md` | Records the successful Issue #17 runtime evidence proving Windows-1252-to-UTF-8 conversion, source preservation, Unicode and CSV equivalence, generated-output exclusion, and a clean repository state. |

The namespace validation reads `information_schema.schemata`. It does not create missing namespaces, transfer ownership, or otherwise repair the database.

Tier 0 validation reads PostgreSQL metadata for exactly `core.location`, `workforce.employee`, and `vendor.vendor`. It does not use schema-wide table counts that would conflict with later approved tiers in the `workforce` and `vendor` schemas. PostgreSQL 18 `NOT NULL` constraints are verified through their distinct `pg_constraint` records, while ordinary `CHECK` constraints are rejected.

Tier 1 validation scopes its checks to `inventory.inventory_item`, `ticketing.ticket`, `workforce.assignment`, `workforce.coverage_schedule`, and `workforce.workload_record`. It validates exact column definitions, constraint names and properties, the absence of the deferred Ticket foreign keys, six constraint-backed indexes, and zero rows without rejecting later approved tables that may share a schema.

Tier 2 validation scopes its checks to `vendor.shipment`, `inventory.replenishment`, `inventory.location_inventory`, `workforce.workforce_escalation`, and `relationships.assignment_ticket`. It validates exact column definitions, constraint names and properties, the absence of unapproved constraints and supporting objects, six constraint-backed indexes, and zero rows without relying on shared-schema table counts.

The implementation-foundation validator owns the checks that would be inappropriate in the narrower validators: exact PostgreSQL version, database and user identity, schema ownership, absence of unapproved schemas and user-defined objects, the empty `public` exception, preservation of the two deferred Ticket foreign keys, the exact 13-table inventory, and empty Tier 0–2 tables before migration. PostgreSQL-managed `pg_catalog`, `information_schema`, `pg_toast`, `pg_temp_*`, and `pg_toast_temp_*` namespaces are excluded from the user-defined inventory.

Execution commands and expected results are documented in [Schema Namespaces](../database-definition/schema-namespaces/README.md#validate-the-namespaces), [Tier 0 Tables](../database-definition/tier-0/README.md#validate-the-tier-0-tables), [Tier 1 Tables](../database-definition/tier-1/README.md#validation), [Tier 2 Tables](../database-definition/tier-2/README.md#validation), and [Implementation Foundation Validation](implementation-foundation/README.md).

---

# Execution Boundary

Validation runs at controlled checkpoints. Structural validation follows database creation, migration validation accompanies data loading, and end-to-end validation follows the completed migration.

Repository-controlled validation must return clear pass or fail results and identify the object, rule, and affected record when a failure occurs. Generated validation output remains uncommitted.

---

# Current Boundary

Issues #7–#9 introduced validation for the approved schema namespaces, the complete Tier 0 table structure, and the initial empty implementation foundation. Issue #29 extended live validation through Tier 1. Issue #32 extends live validation through the Tier 2 structural boundary.

The tier-specific validators now cover 13 approved tables and 128 columns. The cumulative validator accepts exactly those 13 empty tables across the six governed schemas.

The committed Issue #9, Tier 1, and Tier 2 lifecycle evidence remain unchanged as historical implementation-foundation records. Issue #17 adds the first source-data validation record: [Ticket Source Encoding Normalization Validation Evidence](source-data/ticket-source-encoding-validation.md).

The Ticket encoding-normalization boundary is validated and complete. Ticket value correction, reference reconciliation, staging, PostgreSQL loading, deferred foreign-key enforcement, later-tier structures, triggers, and cross-table integrity remain governed by their respective implementation issues.
