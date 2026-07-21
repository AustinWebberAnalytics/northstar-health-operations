# Validation

## Northstar Health Operations

---

**Primary Audience:** Data engineers, analysts, subsystem maintainers, and reviewers verifying PostgreSQL implementation quality

**Writing Layer:** Layer 2 — Operational / Analyst

**Architectural Purpose:** Defines the repository boundary for repeatable structural, migration, data-quality, and relational-integrity validation.

---

# Purpose

This directory will contain repeatable checks that demonstrate whether the PostgreSQL implementation matches approved architecture and governed source data.

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

# Execution Boundary

Validation runs at controlled checkpoints. Structural validation follows database creation, migration validation accompanies data loading, and end-to-end validation follows the completed migration.

Repository-controlled validation must return clear pass or fail results and identify the object, rule, and affected record when a failure occurs. Generated validation output remains uncommitted.

---

# Current Boundary

Issue #5 does not authorize validation SQL, test fixtures, or generated reports.
