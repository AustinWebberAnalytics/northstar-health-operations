# PostgreSQL Platform

## Northstar Health Operations

---

**Primary Audience:** Northstar architects, data engineers, subsystem maintainers, and reviewers responsible for PostgreSQL implementation

**Writing Layer:** Layer 2 — Operational / Architectural

**Architectural Purpose:** Defines the repository boundary, internal responsibilities, execution model, and version-control rules for Northstar's shared PostgreSQL implementation platform.

**Document Type:** Platform Implementation Guide

**Authority Level:** Approved Implementation Boundary

**Status:** Implemented — Issue #29 Tier 1 Structural Boundary

**Depends On:** Enterprise Database Platform Decision, Enterprise Relational Schema, Naming Convention Standards, and Project Governance Standards

---

# Purpose

The PostgreSQL Platform contains the repository-controlled assets used to create, migrate, validate, reset, and tear down Northstar's PostgreSQL 18 environment.

This is a shared enterprise platform. It supports every operational subsystem and does not belong to any single subsystem.

The platform implements approved architecture. It does not redefine enterprise objects, relationships, identifiers, source data, or business rules.

---

# Governed Structure

```text
postgresql-platform/
├── README.md
├── .gitignore
├── local-environment/
│   ├── .env.example
│   ├── README.md
│   └── compose.yaml
├── database-definition/
│   ├── README.md
│   ├── schema-namespaces/
│   │   ├── README.md
│   │   └── create-schema-namespaces.sql
│   ├── tier-0/
│   │   ├── README.md
│   │   └── create-tier-0-tables.sql
│   ├── tier-1/
│   │   ├── README.md
│   │   └── create-tier-1-tables.sql
│   ├── tier-2/                            [created with first approved artifact]
│   ├── tier-3/                            [created with first approved artifact]
│   ├── tier-4/                            [created with first approved artifact]
│   ├── tier-5/                            [created with first approved artifact]
│   ├── supporting-indexes/                [created with first approved artifact]
│   └── cross-table-integrity/             [created with first approved artifact]
├── migrations/
│   └── README.md
├── validation/
│   ├── README.md
│   ├── implementation-foundation/
│   │   ├── README.md
│   │   ├── validate-implementation-foundation.sql
│   │   └── implementation-foundation-validation.md
│   ├── schema-namespaces/
│   │   └── validate-schema-namespaces.sql
│   ├── tier-0/
│   │   └── validate-tier-0-tables.sql
│   └── tier-1/
│       └── validate-tier-1-tables.sql
└── documentation/
    ├── README.md
    └── tier-1-postgresql-implementation-contract.md
```

Empty leaf directories are not retained in Git. Each future leaf directory will be created with its first approved implementation artifact.

---

# Responsibility Boundaries

| Location | Responsibility | Must Not Own |
|---|---|---|
| `local-environment/` | Reproducible PostgreSQL 18 runtime configuration and local lifecycle controls | Table DDL, automatic data loading, or secrets |
| `database-definition/` | Authoritative desired database state, ordered by the approved dependency tiers | Source-data correction or migration history |
| `migrations/` | Controlled source-data migration and future version-to-version transition history | Competing copies of the desired database definition |
| `validation/` | Repeatable structural, migration, row-count, and integrity verification | Silent repair or mutation of authoritative data |
| `documentation/` | Platform setup, execution, troubleshooting, and operating guidance | Enterprise governance or relational-design authority |

The existing subsystem datasets remain the authoritative source data. Canonical PostgreSQL schemas may receive only validated rows through governed migration processes.

---

# Execution Model

Repository-controlled operations will expose five explicit actions:

| Action | Purpose | Primary Ownership |
|---|---|---|
| Create | Create schema namespaces and apply the approved desired-state database definition | `database-definition/` |
| Load | Normalize, reconcile, stage, and load approved source data | `migrations/` |
| Validate | Verify structure, counts, relationships, constraints, and governed integrity rules | `validation/` |
| Reset | Rebuild only the local development database through an intentional destructive command | `local-environment/` |
| Teardown | Stop the local PostgreSQL environment; removal of local storage must require a separate explicit choice | `local-environment/` |

Starting the PostgreSQL service must not automatically create schemas or load data. Create, load, and validate remain separate, visible operations.

Reset and teardown controls apply only to the reproducible local environment. They do not authorize destructive action against any external or shared database.

---

# Execution Order

The approved high-level sequence is:

```text
start local environment
↓
create database definition
↓
validate database structure
↓
load governed source data
↓
validate migrated database state
```

Database creation follows this internal order:

```text
schema namespaces
↓
Tier 0
↓
Tier 1
↓
Tier 2
↓
Tier 3
↓
Tier 4
↓
Tier 5
↓
supporting indexes
↓
cross-table integrity
```

Repository-controlled execution must call files through an explicit approved sequence. Wildcard discovery and reliance on incidental alphabetical ordering are not permitted. Directory names communicate dependency boundaries; they do not independently authorize file-level execution order.

---

# Version-Control Boundary

The repository will contain:

* reproducible local-environment configuration
* non-secret environment templates
* approved SQL definitions and migrations
* validation queries and operational documentation

The repository will not contain:

* `.env` files or credentials
* PostgreSQL data volumes
* binary database backups
* generated logs, caches, or validation output
* unapproved source-data corrections

The scoped [.gitignore](.gitignore) enforces these exclusions within this platform.

---

# Current Implementation Boundary

Issues #5–#9 established the repository organization, the reproducible PostgreSQL 18 local environment, the six approved schema namespaces, the three approved Tier 0 tables, and the completed foundation-validation evidence.

Issue #29 extends the executable boundary through Tier 1. The platform now defines and structurally validates eight empty pre-migration tables: the three Tier 0 tables and `inventory.inventory_item`, `ticketing.ticket`, `workforce.assignment`, `workforce.coverage_schedule`, and `workforce.workload_record`.

The Tier 1 definition contains 58 columns, five primary keys, four immediately enforceable Tier 0 foreign keys, and one Workload Record business-key unique constraint. Ticket Location and Employee foreign keys remain deferred. No source data is loaded.

The live cumulative validator accepts exactly the approved six-schema, eight-table pre-migration state. The issue #9 evidence file remains the unchanged historical record of the earlier three-table foundation checkpoint.

No Tier 2–5 table DDL, migration logic, controlled-vocabulary `CHECK` constraint, trigger code, manually defined supporting index, cross-table integrity enforcement, data loading, or source-data correction is implemented yet.

Each implementation category requires its own governed issue, review, validation, and approval before executable assets are added.
