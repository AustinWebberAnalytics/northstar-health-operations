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

The namespace validation reads `information_schema.schemata`. It does not create missing namespaces, transfer ownership, or otherwise repair the database.

Tier 0 validation reads PostgreSQL metadata for exactly `core.location`, `workforce.employee`, and `vendor.vendor`. It does not use schema-wide table counts that would conflict with later approved tiers in the `workforce` and `vendor` schemas. PostgreSQL 18 `NOT NULL` constraints are verified through their distinct `pg_constraint` records, while ordinary `CHECK` constraints are rejected.

Execution commands and expected results are documented in [Schema Namespaces](../database-definition/schema-namespaces/README.md#validate-the-namespaces) and [Tier 0 Tables](../database-definition/tier-0/README.md#validate-the-tier-0-tables).

---

# Execution Boundary

Validation runs at controlled checkpoints. Structural validation follows database creation, migration validation accompanies data loading, and end-to-end validation follows the completed migration.

Repository-controlled validation must return clear pass or fail results and identify the object, rule, and affected record when a failure occurs. Generated validation output remains uncommitted.

---

# Current Boundary

Issues #7 and #8 introduce validation for the approved schema namespaces and the complete Tier 0 table structure.

Tier 0 validation covers the three approved tables, exactly 23 columns, column order, PostgreSQL types, nullability, defaults, identity and generated behavior, primary keys, prohibited constraints, supporting-index absence, and owner visibility. Migration, source-data quality, later-tier structures, relationships, triggers, and cross-table integrity remain governed by their respective implementation issues.
