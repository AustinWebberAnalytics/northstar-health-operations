# Validation

## Northstar Health Operations

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
| `implementation-foundation/validate-implementation-foundation.sql` | Fails when the runtime identity, namespace ownership, exact eight-table pre-migration object inventory, empty `public` schema, or zero-row boundary differs from the approved state. |

The namespace validation reads `information_schema.schemata`. It does not create missing namespaces, transfer ownership, or otherwise repair the database.

Tier 0 validation reads PostgreSQL metadata for exactly `core.location`, `workforce.employee`, and `vendor.vendor`. It does not use schema-wide table counts that would conflict with later approved tiers in the `workforce` and `vendor` schemas. PostgreSQL 18 `NOT NULL` constraints are verified through their distinct `pg_constraint` records, while ordinary `CHECK` constraints are rejected.

Tier 1 validation scopes its checks to `inventory.inventory_item`, `ticketing.ticket`, `workforce.assignment`, `workforce.coverage_schedule`, and `workforce.workload_record`. It validates exact column definitions, constraint names and properties, the absence of the deferred Ticket foreign keys, six constraint-backed indexes, and zero rows without rejecting later approved tables that may share a schema.

The implementation-foundation validator owns the checks that would be inappropriate in the narrower validators: exact PostgreSQL version, database and user identity, schema ownership, absence of unapproved schemas and user-defined objects, the empty `public` exception, the exact eight-table inventory, and empty Tier 0–1 tables before migration. PostgreSQL-managed `pg_catalog`, `information_schema`, `pg_toast`, `pg_temp_*`, and `pg_toast_temp_*` namespaces are excluded from the user-defined inventory.

Execution commands and expected results are documented in [Schema Namespaces](../database-definition/schema-namespaces/README.md#validate-the-namespaces), [Tier 0 Tables](../database-definition/tier-0/README.md#validate-the-tier-0-tables), [Tier 1 Tables](../database-definition/tier-1/README.md#validation), and [Implementation Foundation Validation](implementation-foundation/README.md).

---

# Execution Boundary

Validation runs at controlled checkpoints. Structural validation follows database creation, migration validation accompanies data loading, and end-to-end validation follows the completed migration.

Repository-controlled validation must return clear pass or fail results and identify the object, rule, and affected record when a failure occurs. Generated validation output remains uncommitted.

---

# Current Boundary

Issues #7–#9 introduced validation for the approved schema namespaces, the complete Tier 0 table structure, and the initial empty implementation foundation. Issue #29 extends live validation through the Tier 1 structural boundary.

The tier-specific validators now cover eight approved tables and 81 columns. The cumulative validator accepts exactly those eight empty tables across the six governed schemas.

The committed issue #9 evidence remains unchanged as historical evidence. Tier 1 lifecycle execution and its separate evidence record are governed by issue #30. Migration, source-data quality, later-tier structures, triggers, and cross-table integrity remain governed by their respective implementation issues.
