# Ticket Reference Reconciliation

## Northstar Enterprise

---

**Primary Audience:** Data engineers, analysts, subsystem maintainers, and reviewers preparing Inventory Discrepancy and Shortage Ticket relationships for governed migration

**Writing Layer:** Layer 2 — Operational / Analyst

**Architectural Purpose:** Records the approved dispositions for three unsupported Ticket references and defines the repeatable process that preserves the affected operational records, retains each source identifier for traceability, and leaves the canonical Ticket relationships nullable as visible migration exceptions.

**Document Type:** Migration Procedure and Approved Reconciliation Decision

**Authority Level:** Approved Issue #20 Implementation

**Status:** Validation Passed — Issue #20

**Approval Date:** August 7, 2026

**Depends On:** Issue #19 Ticket owner reconciliation, Enterprise Relational Schema, Enterprise Relational Foundation, Enterprise Database Platform Decision, and Phase 4 Data Reconciliation Readiness Review

---

# Purpose

The authoritative Inventory Discrepancy and Shortage sources contain three `related_ticket_id` values that do not exist in the current authoritative Ticket source. No repository evidence supports creating the missing Tickets, correcting the identifiers, or substituting other Tickets.

This procedure preserves all affected operational records and retains their original Ticket identifiers as visible migration exceptions. In generated canonical migration outputs, the unsupported `related_ticket_id` values remain nullable while `source_related_ticket_id` preserves the original source evidence.

---

# Approval Basis

The current evidence establishes:

* the Ticket source contains 15 records identified as `INC-100001` through `INC-100015`
* `DISC-1005` references absent Ticket `INC-100018`
* `SHORT-1004` references absent Ticket `INC-100021`
* `DISC-1004` references absent Ticket `INC-100031`
* no authoritative Ticket record or correction evidence exists for any of the three identifiers
* the user approved retaining all three as visible migration exceptions on August 7, 2026

Approximate identifier matching, sequence-based substitution, and invented Ticket records are prohibited.

---

# Approved Outcomes

| Referencing record | Source `related_ticket_id` | Canonical `related_ticket_id` | Reconciliation status |
|---|---|---|---|
| `DISC-1005` | `INC-100018` | — | Approved exception |
| `SHORT-1004` | `INC-100021` | — | Approved exception |
| `DISC-1004` | `INC-100031` | — | Approved exception |

The blank canonical values are governed unresolved relationships. They do not delete the operational records or erase the source identifiers.

---

# Governed Files

| Responsibility | Path |
|---|---|
| Issue #19 reconciled Ticket input | `postgresql-platform/migration-output/ticket-owner-reconciliation/tickets-v1-owner-reconciled.csv` |
| Authoritative Inventory Discrepancy source | `inventory-operations/datasets/data/inventory-discrepancies.csv` |
| Authoritative Shortage source | `inventory-operations/datasets/data/shortage-events.csv` |
| Approved reconciliation decision | `postgresql-platform/migrations/source-data/ticket-reference-reconciliation/ticket-reference-reconciliation.csv` |
| Validation and reconciliation process | `postgresql-platform/migrations/source-data/ticket-reference-reconciliation/validate-ticket-reference-reconciliation.py` |
| Generated Inventory Discrepancy output | `postgresql-platform/migration-output/ticket-reference-reconciliation/inventory-discrepancies-ticket-reconciled.csv` |
| Generated Shortage output | `postgresql-platform/migration-output/ticket-reference-reconciliation/shortage-events-ticket-reconciled.csv` |
| Generated exception report | `postgresql-platform/migration-output/ticket-reference-reconciliation/ticket-reference-reconciliation-exceptions.csv` |

Generated outputs remain under the ignored `migration-output/` boundary and are not committed.

---

# Execute the Validation

Run the Issue #17 normalization, Issue #18 Location mapping, and Issue #19 owner reconciliation processes first. Then, from the repository root:

```powershell
python postgresql-platform/migrations/source-data/ticket-reference-reconciliation/validate-ticket-reference-reconciliation.py
```

The process uses only the Python standard library.

---

# Validation Contract

Before reporting success, the process must verify:

* all four governed inputs are strict UTF-8 without a byte-order mark
* the committed decision artifact exactly matches the three approved Issue #20 outcomes
* the Issue #19 Ticket input contains 15 unique Ticket identifiers
* `INC-100018`, `INC-100021`, and `INC-100031` remain absent from the Ticket input
* the Inventory Discrepancy and Shortage sources each contain five uniquely identified records
* the exact three approved records contain the exact three approved source identifiers
* no additional or missing orphaned Ticket reference is accepted
* no Ticket identifier is created, approximately matched, or substituted
* all ten operational records remain present
* `source_related_ticket_id` preserves every original source relationship value
* only the three approved canonical `related_ticket_id` values become blank
* every nonblank canonical Ticket reference resolves exactly to the Ticket input
* every source row can be reconstructed exactly from the generated output
* all governed inputs remain byte-for-byte unchanged
* all three generated files are strict UTF-8 without a byte-order mark
* generated files remain inside the ignored migration-output boundary

Success ends with:

```text
TICKET REFERENCE RECONCILIATION VALIDATION: PASS
```

---

# Exception Handling

The three approved exceptions are expected governed outcomes. A successful run produces:

* a complete five-record Inventory Discrepancy migration output
* a complete five-record Shortage migration output
* a three-record exception report containing the source dataset, source record, original unsupported Ticket identifier, blank canonical relationship, status, and reason

A new orphan, a changed source relationship, a changed decision artifact, or the appearance of one of the three missing Tickets blocks success and requires governance review. The process removes stale generated outputs at the beginning of each run so prior output cannot be mistaken for current evidence.

---

# Traceability

The generated operational outputs distinguish source evidence from the canonical relationship:

* `source_related_ticket_id` retains the original source value for every record
* `related_ticket_id` carries the canonical relationship used for later migration

For the three approved exceptions, the source field remains populated and the canonical field remains blank. This preserves the records and their provenance while preventing false referential integrity.

---

# Foreign-Key Readiness Boundary

After a successful run, every nonblank canonical Ticket reference in the generated Inventory Discrepancy and Shortage outputs resolves to an existing Ticket. The three approved exceptions remain valid nullable relationships.

This result establishes transformation-level referential readiness only. Strict PostgreSQL foreign-key enforcement remains deferred until approved staging, loading, and migration validation confirm that the generated canonical fields were loaded correctly.

---

# Validation Evidence

Runtime validation passed on August 25, 2026 against tested commit `51071e8a9285daee0fa00340da88c71423b9a488`.

The process preserved all five Inventory Discrepancy and five Shortage records, retained the three approved unsupported source identifiers, left only their canonical relationships blank, resolved every nonblank canonical Ticket reference, created no Ticket identifier or substitute relationship, and produced three strict-UTF-8 generated outputs under the ignored migration-output boundary.

The governed result is recorded in [Ticket Reference Reconciliation Validation Evidence](../../../validation/source-data/ticket-reference-reconciliation-validation.md).

---

# Implementation Boundary

Issue #20 approves and operationalizes the three current orphaned Ticket-reference exceptions only.

It does not:

* modify the authoritative Ticket, Inventory Discrepancy, or Shortage sources
* create, renumber, infer, or approximately match Ticket records
* delete or suppress `DISC-1004`, `DISC-1005`, or `SHORT-1004`
* resolve the three approved exceptions
* create or populate PostgreSQL staging tables
* load operational records into PostgreSQL
* make `related_ticket_id` mandatory
* enable a PostgreSQL Ticket foreign key
* implement Tier 3 DDL

Strict Ticket foreign-key enforcement remains deferred until the approved migration and validation sequence is complete.
