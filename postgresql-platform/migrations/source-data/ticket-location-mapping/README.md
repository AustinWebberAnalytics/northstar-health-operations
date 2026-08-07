# Ticket Location Mapping

## Northstar Enterprise

---

**Primary Audience:** Data engineers, analysts, subsystem maintainers, and reviewers preparing Ticket Location identifiers for governed migration

**Writing Layer:** Layer 2 — Operational / Analyst

**Architectural Purpose:** Records the four approved Ticket Location mappings and defines the repeatable process that validates full source coverage, preserves the original source label, and generates a traceable mapped migration input.

**Document Type:** Migration Procedure and Approved Mapping Decision

**Authority Level:** Approved Issue #18 Implementation

**Status:** Validation Passed — Issue #18

**Approval Date:** August 7, 2026

**Validation Date:** August 7, 2026

**Tested Repository Commit:** `a5b2a8b85a117e8337c3249ae0d14547e1cb9cc9`

**Depends On:** Issue #17 Ticket source encoding normalization, Phase 4 Data Reconciliation Readiness Review, Cross-System Identifier Dictionary, Enterprise Relational Schema, and governed operational Location identifier evidence

---

# Purpose

The Ticket source stores `requesting_location` as descriptive text. The PostgreSQL Ticket entity uses the governed `location_id` identifier.

This procedure validates the approved one-to-one mapping between those representations and generates a UTF-8 migration input that retains `requesting_location` while adding `location_id`.

---

# Approval Basis

Northstar does not yet contain a dedicated populated Location registry that stores both the descriptive names and governed identifiers. Approval therefore uses the current repository evidence available at this boundary:

* the Phase 4 readiness review identifies the four candidate pairs
* the Cross-System Identifier Dictionary governs `location_id`
* `inventory-operations/datasets/data/location-inventory.csv` contains all four identifiers as active operational Location references
* the same identifiers are used consistently across current inventory and vendor datasets
* the four mappings were approved through Issue #18 on August 7, 2026

This limitation is recorded explicitly. The mapping artifact does not claim that a separate Location registry already exists.

---

# Approved Mappings

| Ticket `requesting_location` | Governed `location_id` | Decision |
|---|---|---|
| Cary Distribution Hub 01 | `LOC-CARY-HUB-01` | Approved |
| Durham Outpatient Clinic 07 | `LOC-DURHAM-07` | Approved |
| Raleigh Specialty Clinic 03 | `LOC-RALEIGH-03` | Approved |
| Wake Forest Clinic 11 | `LOC-WAKEFOREST-11` | Approved |

No Location identifier is created or changed through this decision.

---

# Governed Files

| Responsibility | Path |
|---|---|
| Normalized Ticket input | `postgresql-platform/migration-output/ticket-source-encoding/tickets-v1-utf8.csv` |
| Approved mapping artifact | `postgresql-platform/migrations/source-data/ticket-location-mapping/ticket-location-mapping.csv` |
| Validation and mapping process | `postgresql-platform/migrations/source-data/ticket-location-mapping/validate-ticket-location-mapping.py` |
| Location identifier evidence | `inventory-operations/datasets/data/location-inventory.csv` |
| Generated mapped output | `postgresql-platform/migration-output/ticket-location-mapping/tickets-v1-location-mapped.csv` |
| Generated exception report | `postgresql-platform/migration-output/ticket-location-mapping/ticket-location-mapping-exceptions.csv` |

Generated output and exception reports remain under the ignored `migration-output/` boundary and are not committed.

---

# Execute the Validation

Run Issue #17 normalization first. Then, from the repository root:

```powershell
python postgresql-platform/migrations/source-data/ticket-location-mapping/validate-ticket-location-mapping.py
```

The process uses only the Python standard library.

---

# Validation Contract

Before reporting success, the process must verify:

* the normalized Ticket input is strict UTF-8 without a byte-order mark
* the committed mapping artifact exactly matches the four approved Issue #18 decisions
* each source value and each governed identifier appears once in the mapping artifact
* every mapped `location_id` is present in the governed operational Location identifier evidence
* all distinct current `requesting_location` values are covered
* no inactive, unmatched, ambiguous, blank, invented, or malformed mapping is accepted
* `location_id` is added immediately after `requesting_location`
* the original `requesting_location` field is retained
* all original Ticket columns and field values remain unchanged
* the normalized Ticket input remains unchanged
* the mapped output is strict UTF-8 without a byte-order mark
* generated files remain inside the ignored migration-output boundary

Success ends with:

```text
TICKET LOCATION MAPPING VALIDATION: PASS
```

---

# Exception Handling

Any current or future source value without exactly one approved mapping blocks mapped-output generation and returns a nonzero exit code.

Unmatched or ambiguous values are written to the generated exception report for review. They must not be silently loaded, guessed, normalized into a different label, or assigned a new identifier. A new or revised mapping requires a separate governance decision and repository update.

A failed run does not authorize use of mapped output from an earlier successful run.

---

# Traceability

The generated output retains the original `requesting_location` column and adds `location_id` beside it. The original source label therefore remains available for migration review, exception analysis, and source-to-target reconciliation.

---

# Validation Evidence

Runtime validation passed against tested commit [`a5b2a8b`](https://github.com/AustinWebberAnalytics/northstar-health-operations/commit/a5b2a8b85a117e8337c3249ae0d14547e1cb9cc9).

The governed result is recorded in [Ticket Location Mapping Validation Evidence](../../../validation/source-data/ticket-location-mapping-validation.md). The run preserved all 15 Ticket records and all 20 original columns, resolved four distinct source labels through four approved one-to-one mappings, returned zero unmatched or ambiguous values, produced strict UTF-8 mapped output, preserved the normalized source, confirmed generated-output exclusion, and left the working tree clean.

---

# Implementation Boundary

Issue #18 approves and operationalizes the four Ticket Location mappings only.

It does not:

* modify the authoritative raw Ticket source
* modify the normalized Issue #17 output
* reconcile Ticket owner names
* resolve orphaned Ticket references
* create or populate PostgreSQL staging tables
* load Ticket records into PostgreSQL
* make Ticket `location_id` immediately mandatory
* enable the Ticket-to-Location foreign key
* create new Location records or identifiers
* implement Tier 3 DDL

Strict Ticket Location foreign-key enforcement remains deferred until migration and validation are complete.
