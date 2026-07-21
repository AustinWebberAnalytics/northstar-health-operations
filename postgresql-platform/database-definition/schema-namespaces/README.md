# Schema Namespaces

## Northstar Health Operations

---

**Primary Audience:** Northstar architects, data engineers, subsystem maintainers, and reviewers implementing the approved PostgreSQL namespace strategy

**Writing Layer:** Layer 2 — Operational / Architectural

**Architectural Purpose:** Defines the six approved PostgreSQL schema namespaces, their enterprise-domain ownership boundaries, and their controlled creation process.

**Document Type:** Database Definition Guide

**Authority Level:** Approved Implementation Guidance

**Status:** Approved — Issue #7 Schema Namespaces

**Depends On:** Enterprise Database Platform Decision, Enterprise Relational Schema, Naming Convention Standards, PostgreSQL Platform Repository Structure, and PostgreSQL 18 Local Environment

---

# Purpose

This directory contains the repository-controlled SQL that creates Northstar's six approved PostgreSQL schema namespaces.

The namespaces organize relational structures by authoritative enterprise domain. They establish containers only and do not independently authorize tables or any other database objects.

---

# Approved Namespace Ownership

| Schema | Intended Tables |
|---|---|
| `core` | `location` |
| `workforce` | `employee`, `assignment`, `coverage_schedule`, `workload_record`, `workforce_escalation` |
| `vendor` | `vendor`, `shipment`, `fulfillment_event`, `sla_event`, `corrective_action` |
| `inventory` | `inventory_item`, `location_inventory`, `inventory_discrepancy`, `shortage`, `replenishment` |
| `ticketing` | `ticket` |
| `relationships` | `assignment_ticket`, `assignment_corrective_action`, `shipment_replenishment_allocation`, `replenishment_shortage_response` |

No persistent `reporting`, `reference`, or `staging` schema is authorized in the canonical model at this stage.

---

# Controlled File

| File | Responsibility |
|---|---|
| `create-schema-namespaces.sql` | Creates the six approved namespaces in one transaction and assigns ownership to the executing PostgreSQL role. |

The file uses `CREATE SCHEMA IF NOT EXISTS` so the approved creation process can be rerun without failing when the namespaces already exist. It does not alter an existing schema or change an existing owner.

---

# Execution Prerequisites

Before running the namespace definition, confirm that:

* the PostgreSQL 18 local environment is running and healthy
* the terminal is open in `postgresql-platform/local-environment/`
* the local `.env` contains the approved development database and role configuration
* the executing role is authorized to create schemas in the target database

Starting the Docker environment does not run this SQL automatically.

---

# Create the Namespaces

Run the appropriate command from `postgresql-platform/local-environment/`.

Windows PowerShell:

```powershell
Get-Content -Raw ..\database-definition\schema-namespaces\create-schema-namespaces.sql | docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1'
```

macOS, Linux, or Git Bash:

```bash
docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1' < ../database-definition/schema-namespaces/create-schema-namespaces.sql
```

`ON_ERROR_STOP` makes `psql` return a failure when a statement cannot be completed. The SQL transaction prevents a partial first-time namespace creation if an error occurs.

---

# Validate the Namespaces

Run the repository-controlled validation immediately after creation:

Windows PowerShell:

```powershell
Get-Content -Raw ..\validation\schema-namespaces\validate-schema-namespaces.sql | docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1'
```

macOS, Linux, or Git Bash:

```bash
docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1' < ../validation/schema-namespaces/validate-schema-namespaces.sql
```

Validation must report all six namespace names and their owners. A missing approved namespace causes the command to fail.

---

# Qualification and Ownership Rules

Repository-controlled SQL must use schema-qualified object names. A configured `search_path` must not replace explicit qualification.

The creation file assigns each new schema to `CURRENT_USER`. In the approved local environment, execution as `northstar_local_admin` makes that role the owner. Re-execution does not silently transfer ownership if a namespace already exists; validation displays the current owner for review.

---

# Implementation Boundary

Issue #7 authorizes only the six schema namespace containers and their validation.

No tables, roles, grants, migrations, functions, triggers, views, indexes, data, `search_path` changes, or automatic initialization are created through this implementation. PostgreSQL's existing `public` and system schemas remain unchanged.
