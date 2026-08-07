# Ticket Owner Reconciliation

## Northstar Enterprise

---

**Primary Audience:** Data engineers, analysts, subsystem maintainers, and reviewers preparing Ticket Employee relationships for governed migration

**Writing Layer:** Layer 2 — Operational / Analyst

**Architectural Purpose:** Records the approved Ticket owner reconciliation outcomes and defines the repeatable process that applies exact authoritative Employee matches while preserving unresolved owner names as visible per-Ticket exceptions.

**Document Type:** Migration Procedure and Approved Reconciliation Decision

**Authority Level:** Approved Issue #19 Implementation

**Status:** Validation Passed — Issue #19

**Approval Date:** August 7, 2026

**Depends On:** Issue #18 Ticket Location mapping, authoritative workforce roster, Enterprise Relational Schema, Cross-System Identifier Dictionary, and Phase 4 Data Reconciliation Readiness Review

---

# Purpose

The Ticket source stores `assigned_owner` as descriptive text. The PostgreSQL Ticket entity can reference a governed `employee_id` only when an authoritative workforce record establishes the relationship.

This procedure applies the one exact current match, preserves all source owner labels, and generates a per-Ticket exception report for every unresolved owner. It does not create Employee records or infer identity from similar names, departments, teams, or roles.

---

# Approval Basis

The authoritative workforce roster is:

`workforce-coordination/datasets/data/workforce-roster.xlsx`

The current evidence establishes:

* `Jordan Lee` appears in three Ticket records and resolves uniquely to active roster record `EMP-008`
* Avery Patel appears in four Ticket records and has no authoritative roster record
* Marcus Nguyen appears in two Ticket records and has no authoritative roster record
* Samantha Ortiz appears in three Ticket records and has no authoritative roster record
* Taylor Brooks appears in three Ticket records and has no authoritative roster record
* the user confirmed on August 7, 2026 that no additional authoritative records exist for the four unmatched names

Similar names in the roster are not aliases and are not identity evidence. Approximate matching is prohibited.

---

# Approved Outcomes

| Ticket `assigned_owner` | Ticket records | Governed `employee_id` | Reconciliation status |
|---|---:|---|---|
| Jordan Lee | 3 | `EMP-008` | Resolved |
| Avery Patel | 4 | — | Approved exception |
| Marcus Nguyen | 2 | — | Approved exception |
| Samantha Ortiz | 3 | — | Approved exception |
| Taylor Brooks | 3 | — | Approved exception |

The blank `employee_id` values are governed unresolved outcomes. They must not be filled by guessing or by creating new Employee identifiers.

---

# Governed Files

| Responsibility | Path |
|---|---|
| Issue #18 mapped Ticket input | `postgresql-platform/migration-output/ticket-location-mapping/tickets-v1-location-mapped.csv` |
| Approved reconciliation decision | `postgresql-platform/migrations/source-data/ticket-owner-reconciliation/ticket-owner-reconciliation.csv` |
| Validation and reconciliation process | `postgresql-platform/migrations/source-data/ticket-owner-reconciliation/validate-ticket-owner-reconciliation.py` |
| Authoritative workforce roster | `workforce-coordination/datasets/data/workforce-roster.xlsx` |
| Generated reconciled output | `postgresql-platform/migration-output/ticket-owner-reconciliation/tickets-v1-owner-reconciled.csv` |
| Generated exception report | `postgresql-platform/migration-output/ticket-owner-reconciliation/ticket-owner-reconciliation-exceptions.csv` |

Generated output and exception reports remain under the ignored `migration-output/` boundary and are not committed.

---

# Execute the Validation

Run Issue #17 normalization and Issue #18 Location mapping first. Then, from the repository root:

```powershell
python postgresql-platform/migrations/source-data/ticket-owner-reconciliation/validate-ticket-owner-reconciliation.py
```

The process uses only the Python standard library.

---

# Validation Contract

Before reporting success, the process must verify:

* the Issue #18 mapped Ticket input is strict UTF-8 without a byte-order mark
* the committed decision artifact exactly matches the five approved Issue #19 outcomes
* the authoritative workforce workbook is a readable XLSX source with the required Employee fields
* Employee identifiers and names are nonblank and Employee identifiers are unique
* `Jordan Lee` resolves uniquely to active Employee `EMP-008`
* none of the four approved exception owners exists in the authoritative roster
* all 15 current Ticket records match the approved five-owner profile and record counts
* no new, missing, ambiguous, blank, invented, or changed owner relationship is accepted
* `employee_id` is added immediately after `assigned_owner`
* `EMP-008` is populated only for the three Jordan Lee tickets
* `employee_id` remains blank for the 12 approved exception tickets
* `assigned_owner` and every original Ticket field and value are preserved
* the Ticket input and authoritative workforce roster remain unchanged
* reconciled output and the per-Ticket exception report are strict UTF-8 without a byte-order mark
* generated files remain inside the ignored migration-output boundary

Success ends with:

```text
TICKET OWNER RECONCILIATION VALIDATION: PASS
```

---

# Exception Handling

The four approved exception owners are expected governed outcomes. A successful run therefore produces both:

* a complete 15-record reconciled Ticket output; and
* a 12-record exception report retaining `ticket_id`, `assigned_owner`, and the exception reason.

A new owner value, changed Ticket count, new roster match, ambiguous roster match, or changed decision artifact blocks success and requires governance review. The process removes stale generated output at the beginning of a run so an earlier success cannot be mistaken for the current result.

---

# Traceability

The reconciled output retains `assigned_owner` and adds `employee_id` beside it. Unresolved relationships remain blank rather than receiving fabricated identifiers.

The generated exception report preserves each affected `ticket_id` and source owner name so all 12 unresolved records remain visible to later migration review.

---

# Validation Evidence

Runtime validation passed on August 7, 2026 against tested commit `92571dd2e196cb2547db34e34458181e36468dfb`.

The process preserved all 15 Ticket records and 21 source columns, resolved the three Jordan Lee records to `EMP-008`, retained 12 Ticket records as four approved exceptions, produced both expected strict UTF-8 outputs, left both authoritative inputs unchanged, confirmed both generated files are ignored, and left the working tree clean.

The governed result is recorded in [Ticket Owner Reconciliation Validation Evidence](../../../validation/source-data/ticket-owner-reconciliation-validation.md).

---

# Implementation Boundary

Issue #19 approves and operationalizes Ticket owner reconciliation only.

It does not:

* modify the authoritative raw Ticket source
* modify the Issue #17 normalized output
* modify the Issue #18 mapped output
* add, change, or infer workforce-roster records
* create Employee identifiers or aliases
* perform approximate identity matching
* resolve the four approved exceptions
* create or populate PostgreSQL staging tables
* load Ticket records into PostgreSQL
* make Ticket `employee_id` mandatory
* enable the Ticket-to-Employee foreign key
* resolve orphaned Ticket references governed by later issues
* implement Tier 3 DDL

Strict Ticket-to-Employee foreign-key enforcement remains deferred until migration and validation are complete.
