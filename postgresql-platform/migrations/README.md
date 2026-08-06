# Migrations

## Northstar Enterprise

---

**Primary Audience:** Data engineers, analysts, and reviewers responsible for controlled source-data loading and database change history

**Writing Layer:** Layer 2 — Operational / Analyst

**Architectural Purpose:** Defines the boundary between authoritative desired-state SQL, controlled source-data migration, and future database-version transitions.

---

# Purpose

This directory will contain the ordered processes used to move governed data and database state between approved conditions.

Migrations record how a transition occurs. They do not replace the authoritative desired database definition in `database-definition/`.

---

# Migration Responsibilities

The initial source-data migration will support the approved sequence:

```text
source files
↓
encoding normalization
↓
schema and identifier validation
↓
temporary staging
↓
relationship and exception reconciliation
↓
approved field-name transforms
↓
Tier 0–5 load
↓
constraint validation
↓
row-count and integrity verification
```

Future migration work may distinguish between:

* source-data migrations that load governed subsystem datasets
* schema-evolution migrations that transition an existing database between approved versions

Those leaf directories will be created only when their first governed migration is approved.

---

# Migration Rules

Migration processes must:

* preserve the existing subsystem datasets as the authoritative source
* make normalization and field-name transforms explicit
* report unresolved rows as exceptions
* avoid silently correcting source data
* define prerequisites and post-migration validation
* run through an explicit approved order
* remain separate from local environment startup

Generated exception reports and temporary staging output must remain uncommitted unless a later governance decision explicitly promotes a result into an approved repository artifact.

---

# Implemented Source Normalization

Issue #17 introduces the first governed source-data migration leaf:

```text
source-data/
└── ticket-source-encoding/
    ├── README.md
    └── normalize-ticket-source-encoding.py
```

The normalizer converts the authoritative Windows-1252 Ticket source into a generated UTF-8 migration input under the ignored `postgresql-platform/migration-output/` boundary. It validates strict encoding, Unicode-text equivalence, CSV structure and field-value equivalence, source preservation, and generated-output placement.

The generated UTF-8 file remains uncommitted. It does not replace the authoritative source dataset.

---

# Current Boundary

Issue #17 authorizes Ticket encoding normalization only. Runtime validation and completion evidence remain required before the normalized output is approved for the next reconciliation step.

No staging table, PostgreSQL data load, source-data correction, Ticket mapping, owner reconciliation, orphan-reference resolution, deferred foreign-key enforcement, or Tier 3–5 implementation is authorized by this boundary.
