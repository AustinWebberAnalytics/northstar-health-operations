# Tier 1 Tables

## Northstar Health Operations

---

**Primary Audience:** Northstar architects, data engineers, subsystem maintainers, and reviewers creating or validating the approved Tier 1 PostgreSQL structures

**Writing Layer:** Layer 2 — Operational / Architectural

**Architectural Purpose:** Defines the controlled prerequisites, inventory, execution, validation, rerun behavior, legacy aliases, and exclusions for the five approved Tier 1 tables.

**Document Type:** Database Definition Guide

**Authority Level:** Approved Implementation Guidance

**Status:** Implemented — Issue #29 Tier 1 Structural Boundary

**Depends On:** Tier 1 PostgreSQL Implementation Contract, Enterprise Relational Schema, completed schema namespaces, and completed Tier 0 DDL

---

# Purpose

This directory contains the single governed SQL file that creates the five approved Tier 1 PostgreSQL tables.

The creation file implements the approved physical contract. It does not load source data, perform migration, reconcile Ticket references, or authorize later dependency tiers.

---

# Prerequisites

Before running the Tier 1 creation file:

1. Start the repository-controlled PostgreSQL 18 environment.
2. Create all six approved schema namespaces.
3. Create and validate the three Tier 0 tables.
4. Confirm that `core.location`, `workforce.employee`, and `vendor.vendor` exist and are owned by `northstar_local_admin`.
5. Confirm that no Tier 1 table already exists.

Tier 1 depends on the Tier 0 Vendor and Employee tables through four immediately enforceable foreign keys.

---

# Approved Inventory

| Table | Columns | Required | Nullable | Primary Keys | Immediate Foreign Keys | Unique Constraints |
|---|---:|---:|---:|---:|---:|---:|
| `inventory.inventory_item` | 7 | 6 | 1 | 1 | 1 | 0 |
| `ticketing.ticket` | 22 | 10 | 12 | 1 | 0 | 0 |
| `workforce.assignment` | 10 | 8 | 2 | 1 | 1 | 0 |
| `workforce.coverage_schedule` | 9 | 5 | 4 | 1 | 1 | 0 |
| `workforce.workload_record` | 10 | 7 | 3 | 1 | 1 | 1 |
| **Total** | **58** | **36** | **22** | **5** | **4** | **1** |

The five primary keys and the Workload Record business-key unique constraint create six PostgreSQL-managed indexes. No manually defined Tier 1 index is approved.

---

# Controlled Creation

Run `create-tier-1-tables.sql` only after the namespace and Tier 0 creation files succeed.

Windows PowerShell users should use the `Invoke-NorthstarSqlFile` helper defined in the implementation-foundation validation procedure:

```powershell
Invoke-NorthstarSqlFile -Path (Join-Path $repoRoot 'postgresql-platform\database-definition\tier-1\create-tier-1-tables.sql')
```

macOS, Linux, or Git Bash users should run this command from `postgresql-platform/local-environment/`:

```bash
docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1' < ../database-definition/tier-1/create-tier-1-tables.sql
```

The file creates all five tables in one transaction. PostgreSQL rolls back the complete Tier 1 creation if any statement fails.

---

# Validation

Run the validators in this order after Tier 1 creation:

1. `validation/schema-namespaces/validate-schema-namespaces.sql`
2. `validation/tier-0/validate-tier-0-tables.sql`
3. `validation/tier-1/validate-tier-1-tables.sql`
4. `validation/implementation-foundation/validate-implementation-foundation.sql`

The Tier 1 validator confirms the five-table, 58-column physical structure. The cumulative validator confirms the exact eight-table pre-migration repository boundary. Both must report `PASS` before issue #29 can complete.

---

# Rerun Behavior

The creation file is intentionally not idempotent. Rerunning it against an existing Tier 1 structure fails instead of silently accepting, replacing, or altering existing objects.

Rerun the file only against a verified clean database after the separately governed local reset procedure. Do not add `IF NOT EXISTS`, `DROP`, or repair logic to bypass a structural discrepancy.

---

# Legacy Identifier Aliases

| Source Field | Canonical PostgreSQL Column | Treatment |
|---|---|---|
| `schedule_id` | `coverage_schedule_id` | Rename during migration transformation. Do not create `schedule_id` in the canonical table. |
| `workload_id` | `workload_record_id` | Rename during migration transformation. Do not create `workload_id` in the canonical table. |

Ticket `requesting_location` and `assigned_owner` are retained source-value columns, not aliases. Their nullable canonical partners, `location_id` and `employee_id`, remain unconstrained until later reconciliation is complete.

---

# Implementation Exclusions

This Tier 1 checkpoint does not introduce:

* source data, staging, `INSERT`, or `COPY` logic
* Ticket foreign keys on `location_id` or `employee_id`
* `schedule_id` or `workload_id` canonical columns
* controlled-vocabulary, range, sign, formula, or cross-field `CHECK` constraints
* defaults, identity columns, or generated expressions
* triggers, routines, policies, views, grants, or roles
* manually defined indexes
* migration or source-normalization logic
* Tier 2–5 structures or associative entities

Every later addition requires its own governed issue, review, validation, and approval.
