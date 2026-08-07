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

# Implemented Source Reconciliation

Issue #17 introduces the first governed source-data migration leaf:

```text
source-data/
├── ticket-source-encoding/
│   ├── README.md
│   └── normalize-ticket-source-encoding.py
├── ticket-location-mapping/
│   ├── README.md
│   ├── ticket-location-mapping.csv
│   └── validate-ticket-location-mapping.py
├── ticket-owner-reconciliation/
│   ├── README.md
│   ├── ticket-owner-reconciliation.csv
│   └── validate-ticket-owner-reconciliation.py
└── ticket-reference-reconciliation/
    ├── README.md
    ├── ticket-reference-reconciliation.csv
    └── validate-ticket-reference-reconciliation.py
```

The normalizer converts the authoritative Windows-1252 Ticket source into a generated UTF-8 migration input under the ignored `postgresql-platform/migration-output/` boundary. It validates strict encoding, Unicode-text equivalence, CSV structure and field-value equivalence, source preservation, and generated-output placement.

The generated UTF-8 file remains uncommitted. It does not replace the authoritative source dataset.

Issue #18 introduces the approved Ticket Location mapping artifact and its repeatable validator. The process profiles every current `requesting_location` value, verifies the four approved one-to-one mappings against governed operational Location identifier evidence, retains the source label, adds `location_id`, and routes unmatched or ambiguous values to generated exception reporting.

The mapped Ticket output remains uncommitted under the ignored migration-output boundary. Runtime validation passed against tested commit `a5b2a8b85a117e8337c3249ae0d14547e1cb9cc9`, and the governed result is recorded in [Ticket Location Mapping Validation Evidence](../validation/source-data/ticket-location-mapping-validation.md).

Issue #19 introduces the approved and validated Ticket owner reconciliation decision and its repeatable validator. The process reads the authoritative workforce roster, applies only the exact `Jordan Lee → EMP-008` relationship, leaves `employee_id` blank for the four approved exception owners across 12 Ticket records, retains `assigned_owner`, and generates ignored per-Ticket exception reporting.

Runtime validation passed against tested commit `92571dd2e196cb2547db34e34458181e36468dfb`, and the governed result is recorded in [Ticket Owner Reconciliation Validation Evidence](../validation/source-data/ticket-owner-reconciliation-validation.md).

Issue #20 introduces the approved orphaned Ticket-reference decision and its repeatable validator. The process preserves all five Inventory Discrepancy and five Shortage records, retains every original source relationship in `source_related_ticket_id`, leaves the three approved unsupported canonical relationships blank, and generates ignored exception reporting. Runtime validation remains pending.

---

# Current Boundary

Issue #17 authorizes Ticket encoding normalization only. Runtime validation passed against tested commit `fad09ec6d589770dccc2105e66a8188f445e19b4`, and the governed result is recorded in [Ticket Source Encoding Normalization Validation Evidence](../validation/source-data/ticket-source-encoding-validation.md).

Issue #18 approves and validates the four current Ticket Location mappings through the repository-controlled mapping artifact and validator. All 15 current Ticket records resolved with zero unmatched or ambiguous values while preserving the source label and every original field value. That boundary does not authorize owner reconciliation or later migration work.

Issue #19 approves and validates the current owner-reconciliation decisions and repository-controlled validator. One owner relationship resolves exactly, while four names affecting 12 Ticket records remain governed exceptions with blank `employee_id` values and per-Ticket exception reporting. All 15 Ticket records and 21 source columns were preserved; both generated outputs are strict UTF-8, ignored, and uncommitted. No staging table, PostgreSQL data load, source-data correction, roster modification, approximate identity match, orphan-reference resolution, deferred foreign-key enforcement, or Tier 3–5 implementation is authorized by this boundary.

Issue #20 approves the current orphaned Ticket-reference decisions and repository-controlled validator. `DISC-1004`, `DISC-1005`, and `SHORT-1004` remain intact; their original unsupported identifiers remain traceable; and their canonical `related_ticket_id` values remain nullable. Runtime validation, staging, PostgreSQL loading, and foreign-key enforcement remain pending.
