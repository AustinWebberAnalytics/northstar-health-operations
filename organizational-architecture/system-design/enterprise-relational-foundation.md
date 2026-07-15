# Enterprise Relational Foundation

## Northstar Health Operations

---

**Document Type:** Engineering Design Document
**Knowledge Layer:** System Design
**Authority Level:** Design Proposal — Pending Review
**Status:** Draft
**Depends On:** Enterprise Object Model, Enterprise Relational Model, Enterprise Logical Model, Enterprise Identifier Governance (all approved)

---

# Purpose

This document defines how the approved enterprise architecture will be realized in a relational database. It answers *how the system will be organized and built*, not *what the SQL is*. No `CREATE TABLE` statement appears in this document.

It is the last design artifact before implementation begins. Everything after this document (Enterprise Relational Schema, Migration Scripts, Validation Suite) implements decisions made here rather than making new ones.

---

# Scope

**This document defines:**

* database philosophy (single vs. multiple databases, key strategy, history strategy)
* schema/namespace organization
* dependency-ordered build sequence for all 17 entities and 4 associative entities
* foreign key philosophy
* constraint philosophy
* migration philosophy (CSV → database)
* versioning philosophy

**This document intentionally excludes:**

* actual `CREATE TABLE` statements or column-level physical types
* dashboards, analytics, or reporting layers
* APIs
* stored procedures
* performance tuning or indexing strategy beyond what's implied by declared constraints
* event/history-table design for the relationships the Enterprise Logical Model already deferred as analytical/historical (Assignment→Workload Record, Shipment→Location Inventory) — those remain out of scope until a dedicated event-modeling initiative addresses them

---

# Relational Architecture Philosophy

## Single Database, Not Multiple

One enterprise database, not per-domain databases. The entire point of the Logical Model's associative entities (`AssignmentTicket`, `ShipmentReplenishmentFulfillment`, etc.) is enforcing cross-domain foreign keys — Assignment and Ticket, Shipment and Replenishment. Splitting into per-domain databases would make every one of those relationships either unenforceable at the database level or dependent on application-layer joins across separate files/connections, which defeats the reason this modeling work was done.

## Schema Namespacing — Flagged as a Platform-Dependent Decision

This is a real technical constraint, not a style preference: **PostgreSQL supports native schemas** (`CREATE SCHEMA vendor; CREATE TABLE vendor.shipment (...)`), which would cleanly support domain-grouped namespacing. **SQLite does not** — it has no native multi-schema support within a single database file (its `ATTACH DATABASE` mechanism attaches separate files, which reintroduces the cross-database-FK problem above).

If SQLite is the target platform, domain grouping should be achieved through table-naming convention (e.g., `vendor_shipment`, `workforce_assignment`) rather than true schema namespacing. If PostgreSQL, native schemas are available and preferable.

**This choice should be made explicitly before the Enterprise Relational Schema document, not implied by it.** Recommendation: PostgreSQL if the platform choice is still open, given the cross-domain relational nature of this model is exactly what PostgreSQL's schema and constraint support handles more natively than SQLite. If SQLite is required for portability/simplicity reasons, table-prefix naming is the fallback, not a blocker.

## Key Strategy: Surrogate Primary, Business Keys as Constraints

Every entity in the Logical Model already has a governed canonical identifier (surrogate) as of the Enterprise Identifier Governance Review. Enterprise Relational Foundation follows directly from that work:

* **Primary key** = the governed canonical identifier (`ticket_id`, `assignment_id`, etc.) in all cases.
* Where a **business candidate key** was approved (Location Inventory: `location_id` + `item_id`; Workload Record: `employee_id` + `reporting_period`), it is enforced as a `UNIQUE` constraint, not used as the primary key. This matches the Logical Model's own principle that a candidate key and a canonical identifier are distinct concepts — that distinction should survive into the physical schema, not collapse at implementation time.
* Where no business candidate key was approved (Assignment, Corrective Action, Coverage Schedule, Fulfillment Event, SLA Event, Workforce Escalation), no uniqueness constraint beyond the primary key is imposed. Inventing one now would silently reopen a decision already closed.

## History Strategy: Current-State Only, By Design

This phase implements current-state tables only. The two relationships the Logical Model explicitly deferred as "analytical/historical" — Assignment↔Workload Record and Shipment↔Location Inventory — are not addressed here. Building history/event tables for them now would be scope creep into a decision the Logical Model deliberately did not make. If Northstar later wants transaction-history modeling for inventory changes, that is a distinct future initiative building on, not folded into, this one.

---

# Relational Organization (Proposed)

Grouping the 17 entities and 4 associative entities by authoritative domain, matching the Object Model's own classification rather than inventing a new grouping:

|Group|Entities|
|-|-|
|**core**|Location|
|**workforce**|Employee, Assignment, Coverage Schedule, Workload Record, Workforce Escalation|
|**vendor**|Vendor, Shipment, Fulfillment Event, SLA Event, Corrective Action|
|**inventory**|Inventory Item, Location Inventory, Inventory Discrepancy, Shortage, Replenishment|
|**ticketing**|Ticket|
|**relationships**|AssignmentTicket, AssignmentCorrectiveAction, ShipmentReplenishmentFulfillment, ReplenishmentShortageResponse|

This is a proposal, not a final decision — flagged as such per the note above. A `reporting` or `reference` schema is not proposed at this stage since nothing in the current 17-object scope requires one; adding an empty schema now would be speculative.

---

# Implementation Dependency Order

Derived directly from the foreign-key relationships already established across the Object Model, Relational Model, and Logical Model — not a new analysis, a topological ordering of what's already approved.

**Tier 0 — No dependencies**
Location, Employee, Vendor

**Tier 1 — Depend only on Tier 0**
Inventory Item (→ Vendor), Ticket (→ Location, Employee), Assignment (→ Employee), Coverage Schedule (→ Employee), Workload Record (→ Employee)

**Tier 2 — Depend on Tier 0–1**
Shipment (→ Vendor, Inventory Item, Location), Replenishment (→ Inventory Item, Location, Vendor), Location Inventory (→ Inventory Item, Location), Workforce Escalation (→ Ticket, once `related_ticket_id` is added), Assignment Ticket (→ Assignment, Ticket)

**Tier 3 — Depend on Tier 0–2**
Inventory Discrepancy (→ Inventory Item, Location), Shortage (→ Inventory Item, Location), Fulfillment Event (→ Vendor, Shipment, Inventory Item, Location), Shipment Replenishment Fulfillment (→ Shipment, Replenishment)

**Tier 4 — Depend on Tier 0–3**
SLA Event (→ Vendor, Shipment, Fulfillment Event), Replenishment Shortage Response (→ Replenishment, Shortage)

**Tier 5 — Depend on Tier 0–4**
Corrective Action (→ Vendor, SLA Event *optional*, Fulfillment Event *optional*), Assignment Corrective Action (→ Assignment, Corrective Action)

Tables are built in tier order. Within a tier, order doesn't matter — no two entities in the same tier depend on each other.

---

# Foreign Key Philosophy

**Default:** every foreign key declared in the Logical Model is enforced as a real `FOREIGN KEY` constraint at table creation, `NOT NULL` unless the Logical Model marked it optional (e.g., Corrective Action's `sla_event_id`/`fulfillment_event_id`).

**Explicit exception — Ticket's `location_id` and `employee_id`:** the Logical Model already documented that `requesting_location` and `assigned_owner` are currently free text requiring a distinct migration workstream (profile → map → migrate → review exceptions → enforce). These two foreign keys are **not** enforced at initial table creation. They are added as nullable columns first, populated through the documented migration sequence, and only then constrained `NOT NULL` with an enforced `FOREIGN KEY`. This is a staged rollout for two specific columns, not a general exception to the FK philosophy.

**On delete behavior:** `RESTRICT` by default across all foreign keys — an operational record referencing a Location, Employee, Vendor, etc. should block deletion of the referenced row rather than silently cascading. `CASCADE` is not proposed for any relationship in current scope; nothing in the 17-object model represents a genuine parent-owns-child deletion pattern. This is worth confirming rather than assuming, since it affects every table.

---

# Constraint Philosophy

* **Primary keys:** governed canonical identifiers, per Key Strategy above.
* **Unique constraints:** only where a business candidate key was explicitly approved (2 entities — Location Inventory, Workload Record). Not applied speculatively elsewhere.
* **Not null:** applied to every attribute the Logical Model tagged Enterprise-Shared or Domain-Authoritative, unless the Logical Model explicitly marked it optional. Descriptive-or-Derived attributes are nullable by default (e.g., `notes`, `resolution_notes`) since they're narrative, not structural.
* **Check constraints:** proposed for controlled-vocabulary fields with a known, bounded value set observable in current data (e.g., `delivery_status`, `investigation_status`, `severity_level`). The exact enumerations should be derived from actual distinct values in each dataset during Enterprise Relational Schema design, not invented here — that's implementation-layer work, out of scope for this document.
* **Integrity rules from the Logical Model that are not expressible as column-level constraints** (Coverage Schedule's no-overlapping-periods rule; the `preferred_vendor_id` scope-boundary rule) require either application-layer validation or trigger-based enforcement. This document flags them; it does not resolve which mechanism implements them — that’s an Enterprise Relational Schema decision.

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

---

# Versioning Philosophy

Schema changes after initial implementation go through the same design → review → approve → lock discipline used throughout this project — a schema change is an architectural decision, not a code change to be pushed directly. A minimal `schema_version` reference table (version number, applied date, description) is recommended to track what's been applied, but its structure is an Enterprise Relational Schema detail, not a foundation-level decision.

---

# Out of Scope (Explicit)

* Dashboards
* Analytics or reporting queries
* APIs
* Stored procedures
* Indexing/performance tuning beyond what declared constraints imply
* Event/history modeling for the two relationships already deferred as analytical/historical
* Actual column data types and `CREATE TABLE` statements — these belong to the next document, Enterprise Relational Schema

---

# Open Decisions for Austin

1. **Platform choice (SQLite vs. PostgreSQL)** — directly determines whether Schema Organization is implemented as true schemas or table-prefix convention. Recommend deciding this before Enterprise Relational Schema work begins, since it changes how every table is named.
2. **`ON DELETE RESTRICT` as the universal default** — flagged above; confirm before it's applied across all 21 tables (17 entities + 4 associative entities).
3. **Check-constraint enumerations** — deferred to Enterprise Relational Schema by design, but confirm that's the right document for that decision rather than this one.

---

# Summary

This document defines the engineering philosophy for realizing the approved enterprise architecture as a relational database: one database, surrogate primary keys with business keys as constraints where approved, current-state only (no history modeling), domain-grouped schema organization (platform-dependent), a dependency-ordered six-tier build sequence derived from already-approved relationships, foreign-key and constraint philosophies with one explicit staged exception for Ticket's free-text fields, and a migration pipeline that generalizes the Ticket-specific sequence already documented in the Enterprise Logical Model.

No table has been created. No column type has been chosen. Those begin with Enterprise Relational Schema, after this document is reviewed.

