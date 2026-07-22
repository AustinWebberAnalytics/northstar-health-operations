# Tier 0 Tables

## Northstar Health Operations

---

**Primary Audience:** Northstar architects, data engineers, subsystem maintainers, and reviewers implementing the approved PostgreSQL foundation tables

**Writing Layer:** Layer 2 — Operational / Architectural

**Architectural Purpose:** Defines the controlled creation, validation, and rerun boundary for the three approved Tier 0 PostgreSQL tables.

**Document Type:** Database Definition Guide

**Authority Level:** Approved Implementation Guidance

**Status:** Approved — Issue #8 Tier 0 DDL

**Depends On:** Enterprise Relational Schema, Enterprise Database Platform Decision, Enterprise Relational Foundation, Cross-System Identifier Dictionary, Naming Convention Standards, and Issue #7 Schema Namespaces

---

# Purpose

This directory contains the repository-controlled SQL that creates Northstar's three approved Tier 0 tables.

Tier 0 establishes the independent foundation objects required by later dependency tiers. It implements the locked relational schema without adding migration logic, controlled-vocabulary enforcement, or relationships that belong to later issues.

---

# Approved Tier 0 Structures

| Table | Columns | Primary Key | Foreign Keys |
|---|---:|---|---|
| `core.location` | 1 | `location_id` | None |
| `workforce.employee` | 11 | `employee_id` | None |
| `vendor.vendor` | 11 | `vendor_id` | None |

The three tables contain exactly 23 columns. Column names, order, PostgreSQL types, and nullability are governed by the locked Enterprise Relational Schema.

---

# Controlled File

| File | Responsibility |
|---|---|
| `create-tier-0-tables.sql` | Creates the three approved Tier 0 tables and their primary keys in one transaction. |

The file uses schema-qualified table names. It creates no foreign keys, defaults, identity columns, generated expressions, ordinary `CHECK` constraints, manually defined supporting indexes, or data.

PostgreSQL automatically creates one unique B-tree index for each primary key. Those three primary-key indexes are the only indexes authorized by this implementation.

---

# Execution Prerequisites

Before running the Tier 0 definition, confirm that:

* the PostgreSQL 18 local environment is running and healthy
* issue #7's six schema namespaces have been created and validated
* the terminal is open in `postgresql-platform/local-environment/`
* the local `.env` contains the approved development database and role configuration

Starting the Docker environment does not run this SQL automatically.

---

# Create the Tier 0 Tables

Run the appropriate command from `postgresql-platform/local-environment/`.

Windows PowerShell:

```powershell
Get-Content -Raw ..\database-definition\tier-0\create-tier-0-tables.sql | docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1'
```

macOS, Linux, or Git Bash:

```bash
docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1' < ../database-definition/tier-0/create-tier-0-tables.sql
```

The first successful execution reports `BEGIN`, three `CREATE TABLE` results, and `COMMIT`. `ON_ERROR_STOP` makes `psql` return a failure when a statement cannot be completed. The transaction prevents partial Tier 0 creation if an error occurs.

---

# Rerun and Recovery Behavior

This file deliberately does not use `CREATE TABLE IF NOT EXISTS`. PostgreSQL does not guarantee that an existing table matches the requested definition when `IF NOT EXISTS` is used, so silently skipping a table could hide structural drift.

A second execution against an existing Tier 0 build is expected to fail loudly when PostgreSQL reaches `core.location`. The transaction aborts without changing the existing Tier 0 structures. This is intentional and differs from the safely repeatable namespace creation step.

Do not treat simple re-execution as a repair action. If the local database must be rebuilt, use the intentional [local-environment reset](../../local-environment/README.md#reset), accept the resulting loss of all local database state, recreate and validate the schema namespaces, and then execute Tier 0 again. No automatic drop, replacement, or repair behavior is authorized.

---

# Validate the Tier 0 Tables

Run the repository-controlled validation immediately after creation:

Windows PowerShell:

```powershell
Get-Content -Raw ..\validation\tier-0\validate-tier-0-tables.sql | docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1'
```

macOS, Linux, or Git Bash:

```bash
docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1' < ../validation/tier-0/validate-tier-0-tables.sql
```

Validation must report `DO` and then display all 23 columns with their schema, table, ordinal position, PostgreSQL type, nullability, primary-key participation, and table owner. Any governed structural mismatch causes the command to fail.

---

# Validation Scope Boundary

Tier 0 validation is scoped to the three fully qualified tables `core.location`, `workforce.employee`, and `vendor.vendor`.

It validates every column and approved constraint on those tables. It does not count every table in the `workforce` or `vendor` schemas because those namespaces are designed to receive approved Tier 1–5 tables later. Future tables in those schemas must not create false Tier 0 failures.

---

# Implementation Boundary

Issue #8 authorizes only the three Tier 0 tables, their primary keys, structural validation, and the required documentation updates.

No source data, migration logic, Tier 1–5 table, foreign key, controlled-vocabulary `CHECK` constraint, default, identity behavior, generated expression, role, grant, trigger, view, manually defined supporting index, `search_path` change, or automatic initialization is introduced through this implementation.
