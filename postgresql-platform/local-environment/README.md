# Local PostgreSQL Environment

## Northstar Health Operations

---

**Primary Audience:** Data engineers, contributors, and reviewers running the Northstar PostgreSQL platform locally

**Writing Layer:** Layer 2 — Operational / Analyst

**Architectural Purpose:** Defines the reproducible PostgreSQL 18 local runtime, connection method, readiness checks, and controlled lifecycle operations.

**Document Type:** Local Environment Guide

**Authority Level:** Approved Implementation Guidance

**Status:** Approved — Issue #6 Environment

**Depends On:** PostgreSQL Platform Repository Structure, Enterprise Database Platform Decision, Naming Convention Standards, and Project Governance Standards

---

# Purpose

This directory contains the repository-controlled configuration required to run PostgreSQL 18 locally through Docker Compose.

The local environment starts PostgreSQL only. It does not create schema namespaces, tables, migration logic, triggers, validation rules, or governed source data.

This configuration is for local development and validation. It does not represent or imply a production deployment configuration.

---

# Controlled Files

| File | Responsibility |
|---|---|
| `compose.yaml` | Defines the local PostgreSQL service, persistent storage, host binding, and health check. |
| `.env.example` | Provides non-secret local configuration names and approved development defaults. |
| `.env` | Supplies local credentials and configuration. This file is required at runtime and must remain uncommitted. |

The PostgreSQL image is pinned to `postgres:18.4-bookworm`. Persistent database files are stored in the named Docker volume `northstar-postgresql-data` and are not written into the repository.

---

# Prerequisites

Before starting the environment, confirm that the following are available:

* Docker Desktop or Docker Engine with Docker Compose
* a terminal opened in `postgresql-platform/local-environment/`
* an available local TCP port, using `5432` by default

Confirm Docker Compose is available:

```bash
docker compose version
```

---

# Local Configuration

Create the required local `.env` from the committed template.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS, Linux, or Git Bash:

```bash
cp .env.example .env
```

Open `.env` and assign a local password to `POSTGRES_PASSWORD`. The environment will refuse to start when this value is missing or empty.

The `.env` file is excluded through `postgresql-platform/.gitignore`. Never commit the local password or replace `.env.example` with real credentials.

---

# Start and Readiness

Create or start the local environment:

```bash
docker compose --env-file .env up --detach
```

View service and health status:

```bash
docker compose --env-file .env ps
```

The `postgresql` service is ready when its status reports `healthy`.

Run the container-level readiness check directly:

```bash
docker compose --env-file .env exec postgresql sh -c 'pg_isready --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB"'
```

A successful readiness check reports that the server is accepting connections. Readiness does not independently prove that password authentication succeeds.

---

# Validate an Authenticated Connection

Run a password-authenticated TCP connection from inside the PostgreSQL container:

```bash
docker compose --env-file .env exec postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --command="SELECT current_database(), current_user, version();"'
```

The command must return:

* `northstar` as the current database
* `northstar_local_admin` as the current user
* PostgreSQL 18.4 in the version result

This confirms that the server is ready, the configured database and role exist, and the local password succeeds over a TCP connection.

---

# Connect with an Approved SQL Client

Use these values in `psql`, pgAdmin, DBeaver, or another approved local SQL client:

| Setting | Value |
|---|---|
| Host | `127.0.0.1` |
| Port | Value of `POSTGRES_HOST_PORT` in `.env` |
| Database | Value of `POSTGRES_DB` in `.env` |
| User | Value of `POSTGRES_USER` in `.env` |
| Password | Local value of `POSTGRES_PASSWORD` in `.env` |

The host binding is restricted to `127.0.0.1`. The PostgreSQL port is not exposed on other host network interfaces.

---

# Lifecycle Commands

Run all lifecycle commands from `postgresql-platform/local-environment/`.

## Start or Reconcile

Create the environment or reconcile it with `compose.yaml` while preserving the named data volume:

```bash
docker compose --env-file .env up --detach
```

## Stop

Stop the service while preserving its container, network, and named data volume:

```bash
docker compose --env-file .env stop
```

Restart a stopped service:

```bash
docker compose --env-file .env start
```

## Teardown

Remove the local service container and Compose network while preserving the named data volume:

```bash
docker compose --env-file .env down
```

Recreate the service later with the start or reconcile command. The existing local database state will be reused.

## Reset

The following command permanently deletes the local PostgreSQL data volume, including all locally created schemas and loaded data:

```bash
docker compose --env-file .env down --volumes
```

Use reset only when intentional loss of the complete local database state is acceptable. Recreate an empty local PostgreSQL environment afterward:

```bash
docker compose --env-file .env up --detach
```

Reset applies only to this reproducible local environment. It does not authorize destructive action against any shared or external database.

---

# Troubleshooting

View PostgreSQL container logs:

```bash
docker compose --env-file .env logs postgresql
```

Follow new log output:

```bash
docker compose --env-file .env logs --follow postgresql
```

If port `5432` is already in use, stop the conflicting local service or choose another unused host port in `.env`. Do not change the container-side PostgreSQL port in `compose.yaml`.

Changes to `POSTGRES_DB`, `POSTGRES_USER`, or `POSTGRES_PASSWORD` do not modify an already initialized database volume. Apply those initialization changes only by performing an intentional local reset and accepting the resulting data loss.

---

# Implementation Boundary

No initialization directory is mounted, and no SQL file is executed automatically. Starting PostgreSQL must remain separate from creating the database definition, loading governed source data, and running validation.

Schema namespaces and Tier 0–5 relational structures remain governed by their separate implementation issues.
