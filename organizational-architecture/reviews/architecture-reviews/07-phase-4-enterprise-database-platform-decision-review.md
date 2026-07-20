# Phase 4 Enterprise Database Platform Decision Review

## Northstar Health Operations

---

**Primary Audience:** Northstar architects, data engineers, subsystem maintainers, reviewers, and future SQL implementation contributors

**Writing Layer:** Layer 3 — Governance / Review Evidence

**Architectural Purpose:** Records the independent review, correction, and approval of Northstar's target database platform and physical implementation boundaries.

**Document Type:** Architecture Review Record

**Authority Level:** Review Evidence

**Status:** Complete — Approval Recorded

**Depends On:** Enterprise Relational Foundation, Enterprise Relational Schema, Enterprise Database Platform Decision, and Phase 4 Enterprise Relational Schema Approval Review

---

# Purpose

This review records the final platform-selection checkpoint before physical SQL implementation.

It evaluates the PostgreSQL recommendation against the approved Northstar schema, verifies repository-specific claims, corrects factual and enforcement gaps in the draft, and records the final approved implementation boundary.

---

# Review Findings

## Recommendation

The PostgreSQL recommendation was approved.

PostgreSQL is the stronger fit for Northstar because the approved design relies on native relational types, native schema namespacing, 44 foreign-key relationships, and multiple cross-table and aggregate rules.

SQLite remains technically capable, but it would shift more enforcement into conventions and repeated external validation.

## Repository Counts Corrected

The draft undercounted grouped attributes in the Enterprise Relational Schema.

The approved counts are:

* 24 Boolean fields, not 16
* 6 Decimal fields, not 5
* 20 Date fields
* 4 Timestamp fields, not 2
* 54 strongly typed fields in total, not 43
* 44 foreign-key relationships

## Enforcement Coverage Corrected

The draft identified seven nontrivial rule groups but omitted Fulfillment Event versus Shipment reference consistency.

The approved platform decision records eight groups, with the allocation group containing two aggregate ceilings.

## SQLite Trigger Description Corrected

SQLite triggers are not limited to `SELECT` statements in the trigger body.

SQLite supports row triggers containing restricted forms of `INSERT`, `UPDATE`, `DELETE`, and `SELECT`. The final decision retains PostgreSQL's advantage because PostgreSQL supports reusable procedural functions, statement triggers, and deferrable constraint triggers—not because SQLite lacks write statements inside triggers.

## Portfolio Tradeoff Corrected

The draft treated a directly browsable committed SQLite database file as a major GitHub advantage while separately prohibiting committed binary database files.

The approved decision removes that contradiction. SQLite remains easier to generate locally, but neither platform will commit a generated database binary.

## Deletion Policy

The proposed `ON DELETE CASCADE` exception for associative entities was rejected.

All 44 foreign-key relationships use `ON DELETE RESTRICT`.

Associative rows preserve operational relationship evidence. Shipment Replenishment Allocation also carries quantity. Silent cascading would remove meaningful context and weaken the project's explicit change-control philosophy.

## Timestamp Mapping

The two grouped Timestamp declarations represent four Ticket timestamp fields.

The approved PostgreSQL mapping is `TIMESTAMP WITHOUT TIME ZONE` because the current source timestamps are timezone-naive.

## Controlled Values

Provisional controlled-value lists will not become hard initial `CHECK` constraints.

They remain validation queries and exception reports until a later governance review confirms that the value set is complete.

---

# Approval Decision

The following decisions are approved and locked:

* PostgreSQL 18
* one database with six native schemas
* schema-qualified repository SQL
* PostgreSQL native physical types
* `TIMESTAMP WITHOUT TIME ZONE`
* universal `ON DELETE RESTRICT`
* trigger-based cross-table and aggregate enforcement
* validation-only treatment for provisional controlled values
* Docker Compose local development environment

No DDL was approved through this review.

---

# Remaining Conditions

Before strict migration and full constraint validation:

* resolve or except three orphaned Ticket references
* resolve four unmatched Ticket owner names
* formally approve Ticket Location mappings
* define Shipment/Fulfillment translation rules
* define allocation timing and ceiling rules
* select field-specific `NUMERIC` precision and scale
* review supporting indexes after DDL is drafted

---

# Next Controlled Step

Begin physical PostgreSQL schema implementation under the locked Enterprise Relational Schema and Enterprise Database Platform Decision.

The first implementation deliverable should establish the SQL repository structure, Docker Compose environment, schema-creation script, and Tier 0 DDL without building later tiers in the same checkpoint.
