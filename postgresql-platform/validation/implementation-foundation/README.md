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

Normal teardown preserves the named `northstar-postgresql-data` volume. The later reset step permanently deletes that local volume and all database state stored in it. Stop before the reset and obtain separate human authorization immediately before executing the applicable documented `down --volumes` command.

The procedure does not authorize any command against a shared, external, or production database. No command may display the contents of `.env` or record the PostgreSQL password.

---

# Windows PowerShell Session Setup

Windows PowerShell users must run this setup once in every new PowerShell session before Phase 1. Run it from any directory inside the Northstar repository checkout.

The setup uses a normal Git installation when one is available. Otherwise, it locates GitHub Desktop's bundled Git. It then resolves the repository root, anchors every Docker Compose command to the committed Compose file and approved project name, and defines checked helper functions used by the later phases. It verifies that the local `.env` exists but never reads or displays its contents.

```powershell
. {
    $gitCommand = Get-Command git -CommandType Application -ErrorAction SilentlyContinue

    if ($null -ne $gitCommand) {
        $git = $gitCommand.Source
    } else {
        $bundledGit = Get-ChildItem "$env:LOCALAPPDATA\GitHubDesktop\app-*\resources\app\git\cmd\git.exe" -File -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 1

        if ($null -eq $bundledGit) {
            throw 'Git was not found on PATH or in the GitHub Desktop installation.'
        }

        $git = $bundledGit.FullName
    }

    $repoRootOutput = & $git rev-parse --show-toplevel 2>$null
    $repoRootExitCode = $LASTEXITCODE

    if ($repoRootExitCode -ne 0 -or $null -eq $repoRootOutput) {
        throw 'The current directory is not inside a Git repository checkout.'
    }

    $repoRoot = ($repoRootOutput | Select-Object -First 1).Trim()
    $localEnvironmentDirectory = Join-Path $repoRoot 'postgresql-platform\local-environment'
    $composeFile = Join-Path $localEnvironmentDirectory 'compose.yaml'
    $environmentFile = Join-Path $localEnvironmentDirectory '.env'

    if (-not (Test-Path -LiteralPath $composeFile -PathType Leaf)) {
        throw "The committed Compose file was not found at $composeFile."
    }

    if (-not (Test-Path -LiteralPath $environmentFile -PathType Leaf)) {
        throw "The required uncommitted .env file was not found at $environmentFile."
    }

    $dockerCommand = Get-Command docker -CommandType Application -ErrorAction SilentlyContinue

    if ($null -eq $dockerCommand) {
        throw 'Docker was not found on PATH.'
    }

    $composeVersionOutput = docker compose version
    $composeVersionExitCode = $LASTEXITCODE

    if ($composeVersionExitCode -ne 0) {
        throw "Docker Compose version detection failed with exit code $composeVersionExitCode."
    }

    $composeUpHelpOutput = docker compose up --help
    $composeUpHelpExitCode = $LASTEXITCODE

    if ($composeUpHelpExitCode -ne 0 -or ($composeUpHelpOutput -join "`n") -notmatch '--wait-timeout') {
        throw 'The installed Docker Compose version does not support the required startup health-wait options.'
    }

    function Assert-NativeSuccess {
        param(
            [Parameter(Mandatory = $true)]
            [int]$ExitCode,

            [Parameter(Mandatory = $true)]
            [string]$Operation
        )

        if ($ExitCode -ne 0) {
            throw "$Operation failed with exit code $ExitCode."
        }
    }

    function Invoke-NorthstarSqlFile {
        param(
            [Parameter(Mandatory = $true)]
            [string]$Path
        )

        $resolvedPath = (Resolve-Path -LiteralPath $Path -ErrorAction Stop).Path
        $sqlText = Get-Content -LiteralPath $resolvedPath -Raw -ErrorAction Stop

        $sqlText | docker compose --project-name northstar-postgresql-platform --file $composeFile --env-file $environmentFile exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1'
        Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation "SQL execution for $resolvedPath"
    }

    function Invoke-NorthstarValidators {
        Invoke-NorthstarSqlFile -Path (Join-Path $repoRoot 'postgresql-platform\validation\schema-namespaces\validate-schema-namespaces.sql')
        Invoke-NorthstarSqlFile -Path (Join-Path $repoRoot 'postgresql-platform\validation\tier-0\validate-tier-0-tables.sql')
        Invoke-NorthstarSqlFile -Path (Join-Path $repoRoot 'postgresql-platform\validation\implementation-foundation\validate-implementation-foundation.sql')
    }

    function Confirm-NorthstarRuntime {
        docker compose --project-name northstar-postgresql-platform --file $composeFile --env-file $environmentFile ps
        Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'Docker Compose service-status check'

        docker compose --project-name northstar-postgresql-platform --file $composeFile --env-file $environmentFile exec --no-TTY postgresql sh -c 'pg_isready --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB"'
        Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'PostgreSQL readiness check'

        docker compose --project-name northstar-postgresql-platform --file $composeFile --env-file $environmentFile exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --command="SHOW server_version; SELECT current_database(), current_user;"'
        Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'PostgreSQL authenticated-connection check'
    }

    function Start-NorthstarRuntime {
        docker compose --project-name northstar-postgresql-platform --file $composeFile --env-file $environmentFile up --detach --wait --wait-timeout 60
        Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'Docker Compose startup and health wait'
        Confirm-NorthstarRuntime
    }

    Set-Location $repoRoot
    $composeVersionOutput
    Write-Output 'Windows PowerShell validation session is ready.'
}
```

Do not continue if the setup throws an error. Keep the same PowerShell session open through the remaining phases. If the session is closed, rerun the setup before resuming.

---

# Phase 1 — Repository Boundary

Run repository checks at the exact commit being validated.

Windows PowerShell:

```powershell
. {
    $testedCommitOutput = & $git -C $repoRoot rev-parse HEAD
    $testedCommitExitCode = $LASTEXITCODE
    Assert-NativeSuccess -ExitCode $testedCommitExitCode -Operation 'Tested-commit check'
    $testedCommit = ($testedCommitOutput | Select-Object -First 1).Trim()
    Write-Output "Tested commit: $testedCommit"

    $workingTreeState = & $git -C $repoRoot status --short
    $workingTreeExitCode = $LASTEXITCODE
    Assert-NativeSuccess -ExitCode $workingTreeExitCode -Operation 'Working-tree check'

    if ($workingTreeState) {
        Write-Output 'Unexpected working-tree entries:'
        $workingTreeState
        throw 'The repository is not clean.'
    }

    Write-Output 'Repository working tree is clean.'

    $platformFiles = & $git -C $repoRoot ls-files -- ':(top)postgresql-platform'
    $platformInventoryExitCode = $LASTEXITCODE
    Assert-NativeSuccess -ExitCode $platformInventoryExitCode -Operation 'PostgreSQL platform file-inventory check'
    $platformFiles

    $ignoreResult = & $git -C $repoRoot check-ignore -v postgresql-platform/local-environment/.env
    $ignoreExitCode = $LASTEXITCODE
    Assert-NativeSuccess -ExitCode $ignoreExitCode -Operation '.env ignore check'
    $ignoreResult

    if ($ignoreResult -notmatch 'postgresql-platform/\.gitignore') {
        throw 'The local .env is not excluded by postgresql-platform/.gitignore.'
    }

    $envHistory = & $git --no-pager -C $repoRoot log --all --oneline -- postgresql-platform/local-environment/.env
    $envHistoryExitCode = $LASTEXITCODE
    Assert-NativeSuccess -ExitCode $envHistoryExitCode -Operation '.env history check'

    if ($envHistory) {
        Write-Output 'Unexpected .env history entries:'
        $envHistory
        throw 'The local .env appears in repository history.'
    }

    Write-Output 'The local .env has never been committed.'

    $credentialPattern = '^[[:space:]]*POSTGRES_PASSWORD[[:space:]]*=[[:space:]]*[^[:space:]]'
    $matchedCredentialFiles = & $git -C $repoRoot grep -I -E -l $credentialPattern -- postgresql-platform
    $credentialCheckExitCode = $LASTEXITCODE

    if ($credentialCheckExitCode -eq 0) {
        Write-Output 'Potential PostgreSQL password assignments were found in:'
        $matchedCredentialFiles
        throw 'A committed platform file assigns a nonempty PostgreSQL password.'
    } elseif ($credentialCheckExitCode -eq 1) {
        Write-Output 'No committed PostgreSQL password assignment found.'
    } else {
        throw "The committed-password search failed with exit code $credentialCheckExitCode."
    }

    $runtimeArtifactPathspecs = @(
        ':(glob)postgresql-platform/**/.env',
        ':(glob)postgresql-platform/**/postgres-data/**',
        ':(glob)postgresql-platform/**/pgdata/**',
        ':(glob)postgresql-platform/**/*.backup',
        ':(glob)postgresql-platform/**/*.dump',
        ':(glob)postgresql-platform/**/*.sql.gz',
        ':(glob)postgresql-platform/**/output/**',
        ':(glob)postgresql-platform/**/validation-output/**',
        ':(glob)postgresql-platform/**/migration-output/**',
        ':(glob)postgresql-platform/**/*.log',
        ':(glob)postgresql-platform/**/.cache/**',
        ':(glob)postgresql-platform/**/.tmp/**'
    )

    $trackedRuntimeArtifacts = & $git -C $repoRoot ls-files -- $runtimeArtifactPathspecs
    $runtimeArtifactExitCode = $LASTEXITCODE
    Assert-NativeSuccess -ExitCode $runtimeArtifactExitCode -Operation 'Tracked runtime-artifact check'

    if ($trackedRuntimeArtifacts) {
        Write-Output 'Unexpected tracked runtime artifacts:'
        $trackedRuntimeArtifacts
        throw 'Excluded runtime artifacts are tracked.'
    }

    Write-Output 'No excluded runtime artifacts are tracked.'
}
```

The credential search treats a blank or whitespace-only template value as empty, including a blank `.env.example` value stored with Windows CRLF line endings. It reports filenames only when it finds a potential nonempty assignment; it never prints an assigned value.

macOS, Linux, or Git Bash:

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
git --no-pager log --all --oneline -- postgresql-platform/local-environment/.env
```

The ignore check must identify `postgresql-platform/.gitignore`. The history check must return no commits.

Confirm that no committed platform file assigns a nonempty PostgreSQL password. The search returns filenames only and does not print assigned values:

```bash
credential_name='POSTGRES_''PASSWORD'
credential_pattern="^[[:space:]]*${credential_name}[[:space:]]*=[[:space:]]*[^[:space:]]"

if matched_files=$(git grep -I -E -l "$credential_pattern" -- postgresql-platform); then
    echo 'Potential PostgreSQL password assignments were found in:' >&2
    printf '%s\n' "$matched_files" >&2
    exit 1
else
    credential_check_exit_code=$?

    if [ "$credential_check_exit_code" -eq 1 ]; then
        echo 'No committed PostgreSQL password assignment found.'
    else
        echo "The committed-password search failed with exit code $credential_check_exit_code." >&2
        exit "$credential_check_exit_code"
    fi
fi
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

Windows PowerShell users must use the same session initialized by the Windows PowerShell setup. macOS, Linux, and Git Bash users must open the terminal in `postgresql-platform/local-environment/`.

Confirm the service is running and healthy:

Windows PowerShell:

```powershell
. {
    Set-Location $localEnvironmentDirectory
    Confirm-NorthstarRuntime
}
```

macOS, Linux, or Git Bash:

```bash
docker compose --env-file .env ps
docker compose --env-file .env exec postgresql sh -c 'pg_isready --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB"'
```

macOS, Linux, or Git Bash users must also confirm authenticated access without displaying the password:

```bash
docker compose --env-file .env exec postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --command="SHOW server_version; SELECT current_database(), current_user;"'
```

The result must report PostgreSQL `18.4`, database `northstar`, and user `northstar_local_admin`.

Run all three validators in their governed order.

Windows PowerShell:

```powershell
. {
    Set-Location $localEnvironmentDirectory
    Invoke-NorthstarValidators
}
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

Windows PowerShell:

```powershell
. {
    Set-Location $localEnvironmentDirectory

    docker volume inspect northstar-postgresql-data --format '{{.Name}}'
    Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'Initial named-volume check'

    docker compose --project-name northstar-postgresql-platform --file $composeFile --env-file $environmentFile down
    Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'Normal Docker Compose teardown'

    docker volume inspect northstar-postgresql-data --format '{{.Name}}'
    Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'Post-teardown named-volume persistence check'

    Start-NorthstarRuntime
    Invoke-NorthstarValidators
}
```

macOS, Linux, or Git Bash:

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
docker compose --env-file .env up --detach --wait --wait-timeout 60
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

Windows PowerShell:

```powershell
. {
    Set-Location $localEnvironmentDirectory

    docker compose --project-name northstar-postgresql-platform --file $composeFile --env-file $environmentFile down --volumes
    Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'Authorized local Docker Compose reset'

    docker info --format '{{.ServerVersion}}' | Out-Null
    Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'Docker daemon availability check'

    $remainingVolumes = @(docker volume ls --quiet --filter name=northstar-postgresql-data)
    Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'Post-reset named-volume inventory check'

    if ($remainingVolumes -contains 'northstar-postgresql-data') {
        throw 'The Northstar PostgreSQL data volume still exists.'
    } else {
        Write-Output 'The Northstar PostgreSQL data volume was removed.'
    }
}
```

macOS, Linux, or Git Bash:

```bash
docker compose --env-file .env down --volumes
```

Confirm that `northstar-postgresql-data` is absent:

```bash
if ! docker info --format '{{.ServerVersion}}' >/dev/null; then
    echo 'Docker daemon availability check failed.' >&2
    exit 1
fi

if ! remaining_volumes="$(docker volume ls --quiet --filter name=northstar-postgresql-data)"; then
    echo 'Post-reset named-volume inventory check failed.' >&2
    exit 1
fi

if printf '%s\n' "$remaining_volumes" | grep --fixed-strings --line-regexp --quiet 'northstar-postgresql-data'; then
    echo 'The Northstar PostgreSQL data volume still exists.' >&2
    exit 1
fi
echo 'The Northstar PostgreSQL data volume was removed.'
```

Recreate PostgreSQL from the committed Compose file and local uncommitted `.env`, then confirm the service becomes healthy:

Windows PowerShell:

```powershell
. {
    Set-Location $localEnvironmentDirectory
    Start-NorthstarRuntime
}
```

macOS, Linux, or Git Bash:

```bash
docker compose --env-file .env up --detach --wait --wait-timeout 60
docker compose --env-file .env ps
```

Prove that the recreated database contains none of the six Northstar schemas or approved relations:

Windows PowerShell:

```powershell
. {
    Set-Location $localEnvironmentDirectory
    $emptyEnvironmentCheck = "SELECT count(*) FILTER (WHERE nspname IN ('core', 'workforce', 'vendor', 'inventory', 'ticketing', 'relationships')) AS northstar_schema_count, (SELECT count(*) FROM pg_catalog.pg_class AS relations INNER JOIN pg_catalog.pg_namespace AS namespaces ON namespaces.oid = relations.relnamespace WHERE namespaces.nspname IN ('core', 'workforce', 'vendor', 'inventory', 'ticketing', 'relationships') AND relations.relkind IN ('r', 'p', 'S', 'v', 'm', 'f', 'c')) AS northstar_relation_count FROM pg_catalog.pg_namespace;"

    $emptyEnvironmentCheck | docker compose --project-name northstar-postgresql-platform --file $composeFile --env-file $environmentFile exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1'
    Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'Clean-environment inventory check'
}
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
. {
    Set-Location $localEnvironmentDirectory
    Invoke-NorthstarSqlFile -Path (Join-Path $repoRoot 'postgresql-platform\database-definition\schema-namespaces\create-schema-namespaces.sql')
    Invoke-NorthstarSqlFile -Path (Join-Path $repoRoot 'postgresql-platform\database-definition\tier-0\create-tier-0-tables.sql')
    Invoke-NorthstarValidators
    Confirm-NorthstarRuntime
}
```

macOS, Linux, or Git Bash:

```bash
docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1' < ../database-definition/schema-namespaces/create-schema-namespaces.sql

docker compose --env-file .env exec --no-TTY postgresql sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql --host=127.0.0.1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set=ON_ERROR_STOP=1' < ../database-definition/tier-0/create-tier-0-tables.sql
```

Rerun all three Phase 2 validators. The Windows PowerShell block performs this step automatically after both creation files succeed. Leave PostgreSQL running and healthy after every check passes.

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
