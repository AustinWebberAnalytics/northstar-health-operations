# PostgreSQL Platform

## Northstar Enterprise

---

**Primary Audience:** Northstar architects, data engineers, subsystem maintainers, and reviewers responsible for PostgreSQL implementation

**Writing Layer:** Layer 2 — Operational / Architectural

**Architectural Purpose:** Defines the repository boundary, internal responsibilities, execution model, and version-control rules for Northstar's shared PostgreSQL implementation platform.

**Document Type:** Platform Implementation Guide

**Authority Level:** Approved Implementation Boundary

**Status:** Implemented — Tier 2 Structural Boundary; Issue #19 Ticket Owner Reconciliation Validated

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
│   ├── tier-2/
│   │   ├── README.md
│   │   └── create-tier-2-tables.sql
│   ├── tier-3/                            [created with first approved artifact]
│   ├── tier-4/                            [created with first approved artifact]
│   ├── tier-5/                            [created with first approved artifact]
│   ├── supporting-indexes/                [created with first approved artifact]
│   └── cross-table-integrity/             [created with first approved artifact]
├── migrations/
│   ├── README.md
│   └── source-data/
│       ├── ticket-source-encoding/
│       │   ├── README.md
│       │   └── normalize-ticket-source-encoding.py
│       ├── ticket-location-mapping/
│       │   ├── README.md
│       │   ├── ticket-location-mapping.csv
│       │   └── validate-ticket-location-mapping.py
│       └── ticket-owner-reconciliation/
│           ├── README.md
│           ├── ticket-owner-reconciliation.csv
│           └── validate-ticket-owner-reconciliation.py
├── validation/
│   ├── README.md
│   ├── implementation-foundation/
│   │   ├── README.md
│   │   ├── validate-implementation-foundation.sql
│   │   ├── implementation-foundation-validation.md
│   │   └── tier-1-lifecycle-validation.md
│   ├── schema-namespaces/
│   │   └── validate-schema-namespaces.sql
│   ├── source-data/
│   │   ├── ticket-location-mapping-validation.md
│   │   └── ticket-source-encoding-validation.md
│   ├── tier-0/
│   │   └── validate-tier-0-tables.sql
│   ├── tier-1/
│   │   └── validate-tier-1-tables.sql
│   └── tier-2/
│       └── validate-tier-2-tables.sql
└── documentation/
    ├── README.md
    ├── tier-1-postgresql-implementation-contract.md
    └── tier-2-postgresql-implementation-contract.md
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

Issues #5–#9 established the repository organization, the reproducible PostgreSQL 18 local environment, the six approved schema namespaces, the three approved Tier 0 tables, and the completed foundation-validation evidence. Issues #28–#30 extended and validated the executable boundary through Tier 1.

Issue #32 extends the executable boundary through Tier 2. The platform now defines and structurally validates 13 empty pre-migration tables: three Tier 0 tables, five Tier 1 tables, and `vendor.shipment`, `inventory.replenishment`, `inventory.location_inventory`, `workforce.workforce_escalation`, and `relationships.assignment_ticket`.

The Tier 2 definition contains 47 columns, five primary keys, 13 immediately enforceable foreign keys, and one Location Inventory business-key unique constraint. Together, Tier 0–2 contain 128 governed columns. Ticket Location and Employee foreign keys remain deferred. No source data is loaded.

The live cumulative validator accepts exactly the approved six-schema, 13-table pre-migration state. The issue #9 and Tier 1 lifecycle-evidence files remain unchanged historical records of their earlier tested boundaries.

Issue #17 introduces one bounded migration capability: a repository-controlled Windows-1252-to-UTF-8 normalizer for the Ticket source. It writes only generated output under the ignored migration-output boundary, preserves the authoritative source, and performs no data correction, reconciliation, staging, or PostgreSQL loading.

Runtime validation passed against tested commit `fad09ec6d589770dccc2105e66a8188f445e19b4`. The governed result is recorded in [Ticket Source Encoding Normalization Validation Evidence](validation/source-data/ticket-source-encoding-validation.md).

Issue #18 approves and validates the four current Ticket Location mappings through a repository-controlled mapping artifact and validator. The process retains `requesting_location`, adds `location_id`, validates full one-to-one coverage, and routes unmatched or ambiguous values to ignored exception output.

Runtime validation passed against tested commit `a5b2a8b85a117e8337c3249ae0d14547e1cb9cc9`. The governed result is recorded in [Ticket Location Mapping Validation Evidence](validation/source-data/ticket-location-mapping-validation.md).

Issue #19 approves and validates the current Ticket owner reconciliation boundary through a repository-controlled decision artifact and validator. The process applies the single exact relationship `Jordan Lee → EMP-008`, preserves four unmatched owner names as approved exceptions across 12 Ticket records, retains `assigned_owner`, and generates per-Ticket exception reporting.

Runtime validation passed against tested commit `92571dd2e196cb2547db34e34458181e36468dfb`. The governed result is recorded in [Ticket Owner Reconciliation Validation Evidence](validation/source-data/ticket-owner-reconciliation-validation.md).

No Tier 3–5 table DDL, controlled-vocabulary `CHECK` constraint, trigger code, manually defined supporting index, cross-table integrity enforcement, data loading, deferred Ticket foreign-key enforcement, or source-data correction is implemented yet.

Each implementation category requires its own governed issue, review, validation, and approval before executable assets are added.
