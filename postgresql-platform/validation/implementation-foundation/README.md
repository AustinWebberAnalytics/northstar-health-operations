# Implementation Foundation Validation

## Northstar Health Operations

---

**Primary Audience:** Northstar architects, data engineers, subsystem maintainers, and reviewers validating the initial PostgreSQL implementation foundation

**Writing Layer:** Layer 2 — Operational / Architectural

**Architectural Purpose:** Defines the controlled repository, runtime, persistence, reset, rebuild, and evidence procedure used to validate the PostgreSQL implementation foundation.

**Document Type:** Validation Procedure

**Authority Level:** Approved Implementation Guidance

**Status:** Active Validation — Issue #9

**Depends On:** PostgreSQL Platform Repository Structure, PostgreSQL 18 Local Environment, Schema Namespaces, Tier 0 DDL, Enterprise Database Platform Decision, Enterprise Relational Schema, Naming Convention Standards, and Project Governance Standards

---

# Purpose

This directory contains the repeatable process used to prove that Northstar's initial PostgreSQL implementation foundation is governed, structurally exact, reproducible from repository-controlled files, and ready for later dependency tiers.

The procedure validates an empty implementation foundation. It does not authorize source-data migration, Tier 1–5 structures, foreign keys, controlled-vocabulary constraints, supporting indexes, triggers, or cross-table integrity.

---

# Controlled Files

| File | Responsibility |
|---|---|
| `validate-implementation-foundation.sql` | Fails when the runtime identity, schema ownership, exact user-defined object inventory, empty `public` schema, or pre-migration data boundary differs from the approved foundation. |
| `implementation-foundation-validation.md` | Records the curated execution evidence after the complete controlled lifecycle passes. Created in a separate evidence commit. |

The SQL validator is read-only. It does not create, repair, drop, or modify database objects or data.

---

# Three-Validator Responsibility Boundary

The issue #9 foundation result depends on three validators executed in order.

| Validator | Primary Responsibility |
|---|---|
| `schema-namespaces/validate-schema-namespaces.sql` | Confirms that all six approved namespace names exist and displays their owners. |
| `tier-0/validate-tier-0-tables.sql` | Confirms the exact three-table, 23-column Tier 0 structure, primary keys, nullability, prohibited constraints, defaults, generated behavior, and supporting-index absence. |
| `implementation-foundation/validate-implementation-foundation.sql` | Confirms PostgreSQL 18.4, database and user identity, namespace ownership, the exact foundation-wide object inventory, empty Tier 0 tables, and an empty `public` schema. |

The foundation validator excludes PostgreSQL-managed `pg_catalog`, `information_schema`, `pg_toast`, `pg_temp_*`, and `pg_toast_temp_*` namespaces from the user-defined inventory. The existing `public` schema is permitted only while it contains no relation objects, routines, triggers, or policies.

---

# Safety Boundary

Run this procedure only against the repository-controlled local Docker Compose environment defined in `postgresql-platform/local-environment/compose.yaml`.

Normal teardown preserves the named `northstar-postgresql-data` volume. The later reset step permanently deletes that local volume and all database state stored in it. Stop before the reset and obtain separate human authorization immediately before executing `docker compose --env-file .env down --volumes`.

The procedure does not authorize any command against a shared, external, or production database. No command may display the contents of `.env` or record the PostgreSQL password.

---

# Phase 1 — Repository Boundary

Run repository checks from the repository root at the exact commit being validated.

Record the tested commit:

```bash
git rev-parse HEAD
```

Confirm that the working tree is clean. A passing result has no output:

```bash
git status --short
```

Review the repository-controlled platform structure:

```bash
git ls-files postgresql-platform
```

Confirm that the local `.env` is ignored and has never been committed. Neither command displays its contents:

```bash
git check-ignore -v postgresql-platform/local-environment/.env
git log --all --oneline -- postgresql-platform/local-environment/.env
```

The ignore check must identify `postgresql-platform/.gitignore`. The history check must return no commits.

Confirm that no committed platform file assigns a nonempty PostgreSQL password.

Windows PowerShell:

```powershell
$credentialName = 'POSTGRES_' + 'PASSWORD'
git grep -I -E -q "$($credentialName)=.+`$" -- postgresql-platform
if ($LASTEXITCODE -eq 0) { throw 'A committed PostgreSQL password assignment was found.' }
Write-Output 'No committed PostgreSQL password assignment found.'
```

macOS, Linux, or Git Bash:

```bash
credential_name='POSTGRES_''PASSWORD'
if git grep -I -E -q "${credential_name}=.+$" -- postgresql-platform; then
    echo 'A committed PostgreSQL password assignment was found.' >&2
    exit 1
fi
echo 'No committed PostgreSQL password assignment found.'
```

Confirm that no excluded runtime artifact is tracked. A passing result has no output:

```bash
git ls-files -- ':(glob)postgresql-platform/**/.env' ':(glob)postgresql-platform/**/postgres-data/**' ':(glob)postgresql-platform/**/pgdata/**' ':(glob)postgresql-platform/**/*.backup' ':(glob)postgresql-platform/**/*.dump' ':(glob)postgresql-platform/**/*.sql.gz' ':(glob)postgresql-platform/**/output/**' ':(glob)postgresql-platform/**/validation-output/**' ':(glob)postgresql-platform/**/migration-output/**' ':(glob)postgresql-platform/**/*.log' ':(glob)postgresql-platform/**/.cache/**' ':(glob)postgresql-platform/**/.tmp/**'
```

Review `postgresql-platform/.gitignore` and `local-environment/compose.yaml` and confirm:

* runtime data, backups, logs, caches, generated output, and local `.env` files are excluded
* the image is `postgres:18.4-bookworm`
* the host port is bound to `127.0.0.1`
* the Compose project is `northstar-postgresql-platform`
* the only named data volume is `northstar-postgresql-data`
* no initialization directory, migration, or source-data path is mounted for automatic execution

Do not proceed if the repository is dirty, an exclusion fails, or the committed Compose boundary differs.

---

# Phase 2 — Initial Runtime and Structure

Open the terminal in `postgresql-platform/local-environment/`.

Confirm the service is running and healthy:

```bash
docker compose --env-file .env ps
docker compose --env-file .env exec postgresql sh -c 'pg_isready --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB"'
```

Confirm authenticated access without displaying the password:

```bash
docker compose --env-file .env exec postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --command="SHOW server_version; SELECT current_database(), current_user;"'
```

The result must report PostgreSQL `18.4`, database `northstar`, and user `northstar_local_admin`.

Run all three validators in their governed order.

Windows PowerShell:

```powershell
Get-Content -Raw ..\validation\schema-namespaces\validate-schema-namespaces.sql | docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1'

Get-Content -Raw ..\validation\tier-0\validate-tier-0-tables.sql | docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1'

Get-Content -Raw ..\validation\implementation-foundation\validate-implementation-foundation.sql | docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1'
```

macOS, Linux, or Git Bash:

```bash
docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1' < ../validation/schema-namespaces/validate-schema-namespaces.sql

docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1' < ../validation/tier-0/validate-tier-0-tables.sql

docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1' < ../validation/implementation-foundation/validate-implementation-foundation.sql
```

The foundation validator must report `DO` followed by one summary row with `18.4`, `northstar`, `northstar_local_admin`, six schemas, three tables, zero Tier 0 rows, and `PASS`.

---

# Phase 3 — Normal Teardown and Persistence

Confirm the named volume exists:

```bash
docker volume inspect northstar-postgresql-data --format '{{.Name}}'
```

Run normal teardown, then prove the volume remains:

```bash
docker compose --env-file .env down
docker volume inspect northstar-postgresql-data --format '{{.Name}}'
```

Restart the environment and confirm it becomes healthy:

```bash
docker compose --env-file .env up --detach
docker compose --env-file .env ps
```

Rerun all three Phase 2 validators. Every result must match the initial result. This proves that normal teardown removes the service container and network while preserving the governed database state in `northstar-postgresql-data`.

---

# Human Authorization Gate

Stop here.

The next command permanently deletes the complete local Northstar PostgreSQL volume. Confirm that:

* the active Compose project is the committed `northstar-postgresql-platform` project
* the target volume is exactly `northstar-postgresql-data`
* no local data must be preserved
* separate human authorization has been given for this reset

Record the authorization in the curated validation evidence. Do not record credentials or raw command output.

---

# Phase 4 — Destructive Local Reset and Clean Recreation

After separate authorization, remove only the local Compose environment and its named volume:

```bash
docker compose --env-file .env down --volumes
```

Confirm that `northstar-postgresql-data` is absent:

Windows PowerShell:

```powershell
docker volume inspect northstar-postgresql-data 2>$null
if ($LASTEXITCODE -eq 0) { throw 'The Northstar PostgreSQL data volume still exists.' }
Write-Output 'The Northstar PostgreSQL data volume was removed.'
```

macOS, Linux, or Git Bash:

```bash
if docker volume inspect northstar-postgresql-data >/dev/null 2>&1; then
    echo 'The Northstar PostgreSQL data volume still exists.' >&2
    exit 1
fi
echo 'The Northstar PostgreSQL data volume was removed.'
```

Recreate PostgreSQL from the committed Compose file and local uncommitted `.env`, then confirm the service becomes healthy:

```bash
docker compose --env-file .env up --detach
docker compose --env-file .env ps
```

Prove that the recreated database contains none of the six Northstar schemas or approved relations:

Windows PowerShell:

```powershell
$emptyEnvironmentCheck = "SELECT count(*) FILTER (WHERE nspname IN ('core', 'workforce', 'vendor', 'inventory', 'ticketing', 'relationships')) AS northstar_schema_count, (SELECT count(*) FROM pg_catalog.pg_class AS relations INNER JOIN pg_catalog.pg_namespace AS namespaces ON namespaces.oid = relations.relnamespace WHERE namespaces.nspname IN ('core', 'workforce', 'vendor', 'inventory', 'ticketing', 'relationships') AND relations.relkind IN ('r', 'p', 'S', 'v', 'm', 'f', 'c')) AS northstar_relation_count FROM pg_catalog.pg_namespace;"
$emptyEnvironmentCheck | docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1'
```

macOS, Linux, or Git Bash:

```bash
printf '%s\n' "SELECT count(*) FILTER (WHERE nspname IN ('core', 'workforce', 'vendor', 'inventory', 'ticketing', 'relationships')) AS northstar_schema_count, (SELECT count(*) FROM pg_catalog.pg_class AS relations INNER JOIN pg_catalog.pg_namespace AS namespaces ON namespaces.oid = relations.relnamespace WHERE namespaces.nspname IN ('core', 'workforce', 'vendor', 'inventory', 'ticketing', 'relationships') AND relations.relkind IN ('r', 'p', 'S', 'v', 'm', 'f', 'c')) AS northstar_relation_count FROM pg_catalog.pg_namespace;" | docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1'
```

Both counts must be zero.

---

# Phase 5 — Repository-Controlled Rebuild

Run the namespace and Tier 0 creation files in the approved order.

Windows PowerShell:

```powershell
Get-Content -Raw ..\database-definition\schema-namespaces\create-schema-namespaces.sql | docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1'

Get-Content -Raw ..\database-definition\tier-0\create-tier-0-tables.sql | docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1'
```

macOS, Linux, or Git Bash:

```bash
docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1' < ../database-definition/schema-namespaces/create-schema-namespaces.sql

docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1' < ../database-definition/tier-0/create-tier-0-tables.sql
```

Rerun all three Phase 2 validators. Leave PostgreSQL running and healthy after every check passes.

The clean rebuild must end with:

* exactly six approved schemas owned by `northstar_local_admin`
* exactly three approved Tier 0 tables and 23 approved columns
* no Tier 1–5 tables or unapproved user-defined database objects
* an empty `public` schema
* zero rows in all three Tier 0 tables
* PostgreSQL running and healthy

---

# Phase 6 — Curated Evidence

Create `implementation-foundation-validation.md` only after the complete lifecycle passes. The evidence file must record:

* validation date and tested repository commit
* PostgreSQL image and server version
* database, authenticated user, Compose project, and named volume
* repository-boundary and credential-exclusion results
* initial structural-validation results
* normal teardown and persistence results
* destructive reset authorization
* clean recreation and repository-controlled rebuild results
* final results from all three validators and final service health
* discrepancy or exception log
* relevant implementation and evidence commit links
* an explicit pass or fail result for every issue #9 acceptance criterion

Use the standard Northstar document preface with one blank line between every metadata field. Record concise curated results only. Do not commit passwords, `.env` content, generated logs, full raw command output, or machine-specific secrets.

The validation mechanism and its execution evidence belong in separate commits so the evidence can identify the exact committed mechanism it tested.

---

# Completion Boundary

Issue #9 is complete only after the full lifecycle passes, the curated evidence is committed, and the evidence links the implementation and evidence commits.

Operational source-data loading remains deferred to `postgresql-platform/migrations/`. Parent issue #4's broader load wording must be reconciled separately before that parent milestone is closed.
