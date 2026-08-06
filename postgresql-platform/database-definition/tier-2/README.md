# Tier 2 Tables

## Northstar Enterprise

---

**Primary Audience:** Northstar architects, data engineers, subsystem maintainers, and reviewers creating or validating the approved Tier 2 PostgreSQL structures

**Writing Layer:** Layer 2 — Operational / Architectural

**Architectural Purpose:** Defines the controlled prerequisites, inventory, execution, validation, rerun behavior, source-transition treatment, and exclusions for the five approved Tier 2 tables.

**Document Type:** Database Definition Guide

**Authority Level:** Approved Implementation Guidance

**Status:** Implemented — Issue #32 Tier 2 Structural Boundary

**Depends On:** Tier 2 PostgreSQL Implementation Contract, Enterprise Relational Schema, completed schema namespaces, completed Tier 0 DDL, and completed Tier 1 DDL

---

# Purpose

This directory contains the single governed SQL file that creates the five approved Tier 2 PostgreSQL tables.

The creation file implements the approved physical contract. It does not load source data, perform migration, reconcile Ticket references, manufacture historical relationships, or authorize later dependency tiers.

---

# Prerequisites

Before running the Tier 2 creation file:

1. Start the repository-controlled PostgreSQL 18 environment.
2. Create all six approved schema namespaces.
3. Create and validate the three Tier 0 tables.
4. Create and validate the five Tier 1 tables.
5. Confirm that every referenced Tier 0–1 table exists and is owned by `northstar_local_admin`.
6. Confirm that no Tier 2 table already exists.

All 13 Tier 2 foreign keys are immediately enforceable because their referenced Tier 0–1 tables exist before Tier 2 creation.

---

# Approved Inventory

| Table | Columns | Required | Nullable | Primary Keys | Foreign Keys | Unique Constraints |
|---|---:|---:|---:|---:|---:|---:|
| `vendor.shipment` | 13 | 9 | 4 | 1 | 4 | 0 |
| `inventory.replenishment` | 12 | 7 | 5 | 1 | 4 | 0 |
| `inventory.location_inventory` | 9 | 5 | 4 | 1 | 2 | 1 |
| `workforce.workforce_escalation` | 11 | 6 | 5 | 1 | 1 | 0 |
| `relationships.assignment_ticket` | 2 | 2 | 0 | 1 composite | 2 | 0 |
| **Total** | **47** | **29** | **18** | **5** | **13** | **1** |

The five primary keys and the Location Inventory business-key unique constraint create six PostgreSQL-managed indexes. No manually defined Tier 2 index is approved.

---

# Controlled Creation

Run `create-tier-2-tables.sql` only after the namespace, Tier 0, and Tier 1 creation files succeed.

Windows PowerShell users should use the `Invoke-NorthstarSqlFile` helper defined in the implementation-foundation validation procedure:

```powershell
Invoke-NorthstarSqlFile -Path (Join-Path $repoRoot 'postgresql-platform\database-definition\tier-2\create-tier-2-tables.sql')
```

macOS, Linux, or Git Bash users should run this command from `postgresql-platform/local-environment/`:

```bash
docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1' < ../database-definition/tier-2/create-tier-2-tables.sql
```

The file creates all five tables in one transaction. PostgreSQL rolls back the complete Tier 2 creation if any statement fails.

---

# Validation

Run the validators in this order after Tier 2 creation:

1. `validation/schema-namespaces/validate-schema-namespaces.sql`
2. `validation/tier-0/validate-tier-0-tables.sql`
3. `validation/tier-1/validate-tier-1-tables.sql`
4. `validation/tier-2/validate-tier-2-tables.sql`
5. `validation/implementation-foundation/validate-implementation-foundation.sql`

The Tier 2 validator confirms the five-table, 47-column physical structure. The cumulative validator confirms the exact 13-table pre-migration repository boundary. Both must report `PASS` before issue #32 can complete.

---

# Rerun Behavior

The creation file is intentionally not idempotent. Rerunning it against an existing Tier 2 structure fails instead of silently accepting, replacing, or altering existing objects.

Rerun the file only against a verified clean database after the separately governed local reset procedure. Do not add `IF NOT EXISTS`, `DROP`, or repair logic to bypass a structural discrepancy.

---

# Source-Transition Treatment

| Source | Tier 2 Treatment |
|---|---|
| `inventory-operations/datasets/data/vendor-shipments.csv` | Supplies the 13 governed Shipment fields; no row is loaded through issue #32. |
| `inventory-operations/datasets/data/replenishment-events.csv` | Supplies the 12 governed Replenishment fields; `vendor_id` remains nullable and no Vendor-presence rule is added. |
| `inventory-operations/datasets/data/location-inventory.csv` | Supplies the 9 governed Location Inventory fields; (`location_id`, `item_id`) is enforced as the business-key unique constraint. |
| `workforce-coordination/datasets/data/workforce-escalations.csv` | Supplies 10 source fields; nullable `related_ticket_id` is added without historical backfill. |
| No current source dataset | `relationships.assignment_ticket` begins empty with exactly its two governed foreign-key columns. |

Physical column order follows the approved relational schema rather than source-file order. Source normalization and loading remain governed by `postgresql-platform/migrations/`.

---

# Implementation Exclusions

This Tier 2 checkpoint does not introduce:

* source data, staging, `INSERT`, `COPY`, or migration logic
* Ticket foreign keys on `ticketing.ticket.location_id` or `ticketing.ticket.employee_id`
* historical Workforce Escalation Ticket values or an Employee reference on `resolution_owner`
* a Shipment Line table or multi-item Shipment redesign
* a surrogate key or relationship attributes on Assignment Ticket
* controlled-vocabulary, range, sign, date-order, formula, or cross-field `CHECK` constraints
* defaults, identity columns, or generated expressions
* triggers, routines, policies, views, grants, or roles
* manually defined indexes
* Tier 3–5 structures, migration logic, source normalization, or data correction

Every later addition requires its own governed issue, review, validation, and approval.
