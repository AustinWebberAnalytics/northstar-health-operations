# Enterprise Relational Foundation

## Northstar Health Operations

---

**Primary Audience:** Northstar architects, data engineers, subsystem maintainers, and reviewers responsible for relational implementation discipline

**Writing Layer:** Layer 2 — Operational / Architectural

**Architectural Purpose:** Establishes the engineering principles, dependency order, key strategy, foreign-key philosophy, constraint philosophy, migration approach, and platform boundary governing downstream relational design.

**Document Type:** Engineering Design Document

**Authority Level:** Approved Engineering Design

**Status:** Approved — Locked

**Depends On:** Enterprise Object Model, Enterprise Relational Model, Enterprise Logical Model, Enterprise Identifier Governance Review, and Cross-System Identifier Dictionary

---

# Purpose

This document defines how the approved enterprise architecture will be realized in a relational database. It answers *how the system will be organized and built*, not *what the SQL is*. No `CREATE TABLE` statement appears in this document.

This document establishes the foundation-level engineering decisions that bound downstream relational design. Enterprise Relational Schema makes detailed implementation-design decisions within those boundaries — naming, attribute-level nullability, aggregate integrity rules, and similar judgment calls not settled here. SQL Implementation, migration scripts, and validation artifacts then implement the approved schema.

---

# Scope

**This document defines:**

- database philosophy (single vs. multiple databases, key strategy, history strategy)
- schema/namespace organization
- dependency-informed build sequence for all 17 entities and 4 associative entities
- foreign key philosophy
- constraint philosophy
- migration philosophy (CSV → database)
- versioning philosophy

**This document intentionally excludes:**

- actual `CREATE TABLE` statements or column-level physical types
- dashboards, analytics, or reporting layers
- APIs
- stored procedures
- performance tuning or indexing strategy beyond what's implied by declared constraints
- event/history-table design for the relationships the Enterprise Logical Model already deferred as analytical/historical (Assignment→Workload Record, Shipment→Location Inventory) — those remain out of scope until a dedicated event-modeling initiative addresses them

---

# Database Philosophy

## Single Database, Not Multiple

One enterprise database, not per-domain databases. The entire point of the Logical Model's associative entities (`AssignmentTicket`, `ShipmentReplenishmentAllocation`, etc.) is enforcing cross-domain foreign keys — Assignment and Ticket, Shipment and Replenishment. Splitting into per-domain databases would make every one of those relationships either unenforceable at the database level or dependent on application-layer joins across separate files/connections, which defeats the reason this modeling work was done.

## Schema Namespacing — Flagged as a Platform-Dependent Decision

This is a real technical constraint, not a style preference: **PostgreSQL supports native schemas** (`CREATE SCHEMA vendor; CREATE TABLE vendor.shipment (...)`), which would cleanly support domain-grouped namespacing. **SQLite does not** — it has no native multi-schema support within a single database file (its `ATTACH DATABASE` mechanism attaches separate files, which reintroduces the cross-database-FK problem above).

If SQLite is the target platform, domain grouping should be achieved through table-naming convention (e.g., `vendor_shipment`, `workforce_assignment`) rather than true schema namespacing. If PostgreSQL, native schemas are available and preferable.

**This choice should be made explicitly before SQL Implementation, not implied by it.** The Enterprise Relational Schema is intentionally platform-neutral and does not require this decision to proceed. Recommendation: PostgreSQL if the platform choice is still open, given the cross-domain relational nature of this model is exactly what PostgreSQL's schema and constraint support handles more natively than SQLite. If SQLite is required for portability/simplicity reasons, table-prefix naming is the fallback, not a blocker.

## Key Strategy: Surrogate Primary, Business Keys as Constraints

Every entity in the Logical Model already has a governed canonical identifier (surrogate) as of the Enterprise Identifier Governance Review. Enterprise Relational Foundation follows directly from that work:

- **Primary key** = governed canonical identifiers for the 17 enterprise objects (`ticket_id`, `assignment_id`, etc.), or approved composite relationship keys for the 4 associative entities — see the associative-entity exception below.
- Where a **business candidate key** was approved (Location Inventory: `location_id` + `item_id`; Workload Record: `employee_id` + `reporting_period`), it is enforced as a `UNIQUE` constraint, not used as the primary key. This matches the Logical Model's own principle that a candidate key and a canonical identifier are distinct concepts — that distinction should survive into the physical schema, not collapse at implementation time.
- Where no business candidate key was approved (Assignment, Corrective Action, Coverage Schedule, Fulfillment Event, SLA Event, Workforce Escalation), no uniqueness constraint beyond the primary key is imposed. Inventing one now would silently reopen a decision already closed.
- **Nullability** is determined per attribute from business meaning, lifecycle state, migration readiness, and repository evidence — not automatically inferred from provenance classification. An attribute tagged Enterprise-Shared or Domain-Authoritative in the Logical Model indicates authority and importance; it does not by itself mean the attribute is required on every record. The Enterprise Relational Schema's treatment of Replenishment's `vendor_id` is the clearest example: it's a governed Enterprise-Shared foreign key, yet conditionally nullable, because `Internal Transfer` replenishments have no vendor by definition — a real business state confirmed against repository evidence, not a data-quality gap to paper over with a blanket `NOT NULL`.

**Associative-entity exception.** The rule above governs the 17 canonical enterprise objects, which the Enterprise Identifier Governance Review addressed. It does not extend to the 4 associative entities (`AssignmentTicket`, `AssignmentCorrectiveAction`, `ShipmentReplenishmentAllocation`, `ReplenishmentShortageResponse`), which are relationship entities, not canonical enterprise objects, and were out of that review's scope. An associative entity may use its required foreign-key combination as a composite primary key when one row represents the complete current relationship between that pair — even when the row carries relationship-level attributes, as `ShipmentReplenishmentAllocation`'s `allocated_quantity` does. A surrogate identifier is required only when multiple records per pair, temporal history, or an independent lifecycle must be represented (e.g., if a relationship needed to record several allocation events over time rather than one current total).

## History Strategy: Current-State Only, By Design

This phase implements current-state tables only. The two relationships the Logical Model explicitly deferred as "analytical/historical" — Assignment↔Workload Record and Shipment↔Location Inventory — are not addressed here. Building history/event tables for them now would be scope creep into a decision the Logical Model deliberately did not make. If Northstar later wants transaction-history modeling for inventory changes, that is a distinct future initiative building on, not folded into, this one.

---

# Schema Organization (Proposed)

Grouping the 17 entities and 4 associative entities by authoritative domain, matching the Object Model's own classification rather than inventing a new grouping:

| Group | Entities |
|---|---|
| **core** | Location |
| **workforce** | Employee, Assignment, Coverage Schedule, Workload Record, Workforce Escalation |
| **vendor** | Vendor, Shipment, Fulfillment Event, SLA Event, Corrective Action |
| **inventory** | Inventory Item, Location Inventory, Inventory Discrepancy, Shortage, Replenishment |
| **ticketing** | Ticket |
| **relationships** | AssignmentTicket, AssignmentCorrectiveAction, ShipmentReplenishmentAllocation, ReplenishmentShortageResponse |

This is a proposal, not a final decision — flagged as such per the note above. A `reporting` or `reference` schema is not proposed at this stage since nothing in the current 17-object scope requires one; adding an empty schema now would be speculative.

---

# Implementation Order (Dependency-First)

Derived directly from the foreign-key relationships already established across the Object Model, Relational Model, and Logical Model — a dependency-informed implementation sequence of what's already approved.

**Tier 0 — No dependencies**
Location, Employee, Vendor

**Tier 1 — Depend only on Tier 0**
Inventory Item (→ Vendor), Ticket (→ Location, Employee), Assignment (→ Employee), Coverage Schedule (→ Employee), Workload Record (→ Employee)

**Tier 2 — Depend on Tier 0–1**
Shipment (→ Vendor, Inventory Item, Location), Replenishment (→ Inventory Item, Location, Vendor), Location Inventory (→ Inventory Item, Location), Workforce Escalation (→ Ticket, once `related_ticket_id` is added), Assignment Ticket (→ Assignment, Ticket)

**Tier 3 — Depend on Tier 0–2**
Inventory Discrepancy (→ Inventory Item, Location), Shortage (→ Inventory Item, Location), Fulfillment Event (→ Vendor, Shipment, Inventory Item, Location), Shipment Replenishment Allocation (→ Shipment, Replenishment)

**Tier 4 — Depend on Tier 0–3**
SLA Event (→ Vendor, Shipment, Fulfillment Event), Replenishment Shortage Response (→ Replenishment, Shortage)

**Tier 5 — Depend on Tier 0–4, with an ordered terminal step**
Corrective Action (→ Vendor, SLA Event *optional*, Fulfillment Event *optional*, Ticket *optional*), followed by Assignment Corrective Action (→ Assignment, Corrective Action)

Tables are built in tier order. Within Tiers 0–4, order does not matter because no entity depends on another entity in the same tier. Tier 5 is the sole ordered exception: Corrective Action must be created before Assignment Corrective Action because the associative entity references it.

---

# Foreign Key Philosophy

**Default:** Every foreign key declared in the Logical Model is implemented as a real `FOREIGN KEY` once its migration and reconciliation prerequisites are satisfied. Whether the foreign key is required, optional, or conditional is determined per attribute in the Enterprise Relational Schema from business meaning, lifecycle state, migration readiness, and repository evidence. Foreign-key status does not by itself imply `NOT NULL`.

**Explicit exception — Ticket's `location_id` and `employee_id`:** the Logical Model already documented that `requesting_location` and `assigned_owner` are currently free text requiring a distinct migration workstream (profile → map → migrate → review exceptions → enforce). These two foreign keys are **not** enforced at initial table creation. They are added as nullable columns first, populated through the documented migration sequence, and only then constrained `NOT NULL` with an enforced `FOREIGN KEY`. This is a staged rollout for two specific columns, not a general exception to the FK philosophy.

**On delete behavior:** `RESTRICT` by default across all foreign keys — an operational record referencing a Location, Employee, Vendor, etc. should block deletion of the referenced row rather than silently cascading. `CASCADE` is not proposed for any relationship in current scope; nothing in the 17-object model represents a genuine parent-owns-child deletion pattern. This is worth confirming rather than assuming, since it affects every table.

---

# Constraint Philosophy

- **Primary keys:** governed canonical identifiers, per Key Strategy above.
- **Unique constraints:** only where a business candidate key was explicitly approved (2 entities — Location Inventory, Workload Record). Not applied speculatively elsewhere.
- **Not null:** applied only where the Enterprise Relational Schema identifies an attribute as required, based on business meaning, lifecycle state, migration readiness, and repository evidence. Provenance classification (Enterprise-Shared / Domain-Authoritative / Descriptive-or-Derived) identifies authority and importance; it does not determine nullability by itself.
- **Check constraints:** proposed for controlled-vocabulary fields with a known, bounded value set observable in current data (e.g., `delivery_status`, `investigation_status`, `severity_level`). The exact enumerations should be derived from actual distinct values in each dataset during Enterprise Relational Schema design, not invented here — that's implementation-layer work, out of scope for this document.
- **Integrity rules from the Logical Model that are not expressible as column-level constraints.** The `preferred_vendor_id` scope-boundary rule requires either application-layer validation or trigger-based enforcement — that mechanism choice is an Enterprise Relational Schema decision, not made here. Coverage Schedule's no-overlapping-periods rule is different in kind: the Enterprise Relational Schema established that it is **structurally deferred**, not merely awaiting a mechanism choice — no trigger or application check can evaluate it until Coverage Schedule has governed time boundaries (`coverage_start_at`/`coverage_end_at`) or a controlled Shift definition, neither of which currently exists.
- **Cross-table reference consistency:** when a child assessment repeats references already determined by its parent event, those references must agree. Fulfillment Event `vendor_id`, `item_id`, and `location_id` must match the referenced Shipment; SLA Event `vendor_id` and `shipment_id` must match the referenced Fulfillment Event. The enforcement mechanism is deferred to SQL Implementation.
- **Organizational ownership is not employee identity:** Corrective Action `assigned_owner` remains organizational text. It must not be converted into an Employee foreign key without a separately governed `employee_id` attribute and supporting source data.

---

# Migration Philosophy

```text
CSV
  ↓
Validation        (row counts, type conformance, required-field presence)
  ↓
Transform         (map legacy field names — schedule_id → coverage_schedule_id,
                    workload_id → workload_record_id — per Identifier Governance Review)
  ↓
Load              (dependency-tier order, per Implementation Order above)
  ↓
Verification      (row counts match source; foreign keys resolve; no orphaned references)
```

Ticket's `requesting_location`/`assigned_owner` migration follows the more detailed sequence already documented in the Enterprise Logical Model (profile → mapping rules → migrate resolvable values → review exceptions → enforce). That sequence is a specialization of this general pipeline for one specific, already-flagged data-quality problem — not a separate philosophy.

## Current Migration Readiness Findings

Repository-wide validation identified several conditions that do not block Tier 5 schema derivation but must be resolved before SQL Implementation enables strict referential integrity:

- **Employee name preservation:** Employee must retain `employee_name` because Ticket `assigned_owner` reconciliation depends on matching names to canonical `employee_id` values.
- **Ticket owner coverage:** 3 of 15 current tickets map by exact owner name to the workforce roster. Four distinct owner names remain unmatched: Avery Patel, Marcus Nguyen, Samantha Ortiz, and Taylor Brooks.
- **Ticket location mapping:** all four distinct `requesting_location` values have clear candidate mappings to the four governed `location_id` values, but the mapping must still be formally validated and recorded.
- **Orphaned Ticket references:** `INC-100018`, `INC-100021`, and `INC-100031` are referenced by current Inventory Discrepancy or Shortage records but do not exist in `tickets-v1.csv`.
- **Source encoding:** `tickets-v1.csv` is Windows-1252 while the other current datasets are UTF-8 or UTF-8 with BOM. Migration must normalize source encoding before validation and load.
- **Corrective Action ownership:** current `assigned_owner` values are organizational functions, not employees. No Employee foreign-key migration is authorized from that field.

These findings are migration prerequisites, not reasons to alter approved object identity or relationship meaning.

---

# Versioning Philosophy

Schema changes after initial implementation go through the same design → review → approve → lock discipline used throughout this project — a schema change is an architectural decision, not a code change to be pushed directly. A minimal `schema_version` reference table (version number, applied date, description) is recommended to track what's been applied, but its structure is an Enterprise Relational Schema detail, not a foundation-level decision.

---

# Out of Scope (Explicit)

- Dashboards
- Analytics or reporting queries
- APIs
- Stored procedures
- Indexing/performance tuning beyond what declared constraints imply
- Event/history modeling for the two relationships already deferred as analytical/historical
- Actual column data types and `CREATE TABLE` statements — these belong to the next document, Enterprise Relational Schema

---

# Open Decisions Before SQL Implementation

1. **Platform choice (SQLite vs. PostgreSQL)** — directly determines whether Schema Organization is implemented as true schemas or table-prefix convention. Recommend deciding this before SQL Implementation begins — the Enterprise Relational Schema is intentionally being built platform-neutrally and does not require this decision to proceed.
2. **`ON DELETE RESTRICT` as the universal default** — flagged above; confirm before it's applied across all 21 tables (17 entities + 4 associative entities).

---

# Summary

This document defines the engineering philosophy for realizing the approved enterprise architecture as a relational database: one database, surrogate primary keys with business keys as constraints where approved, current-state only (no history modeling), domain-grouped schema organization (platform-dependent), a dependency-informed six-tier build sequence with one explicit ordered exception in Tier 5, foreign-key and constraint philosophies with one explicit staged exception for Ticket's free-text fields, and a migration pipeline that generalizes the Ticket-specific sequence already documented in the Enterprise Logical Model.

No table has been created. Platform-neutral logical types are defined in Enterprise Relational Schema; platform-specific physical types, DDL, migration scripts, and enforcement mechanisms begin in SQL Implementation after the remaining platform and deletion-policy decisions are approved.
