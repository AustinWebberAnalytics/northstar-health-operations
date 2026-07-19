# Enterprise Relational Schema

## Northstar Health Operations

\---

**Primary Audience:** Northstar architects, data engineers, subsystem maintainers, and reviewers translating approved logical design into a platform-neutral schema specification

**Writing Layer:** Layer 2 — Operational / Architectural

**Architectural Purpose:** Defines entities, attributes, logical types, keys, nullability, logical constraints, migration considerations, and dependency-tier status for the governed enterprise relational design.

**Document Type:** Engineering Design Document

**Authority Level:** Design Specification

**Status:** Draft — Tiers 0–4 Locked, Tier 5 Not Yet Started

**Depends On:** Enterprise Logical Model, Enterprise Identifier Governance Review, Cross-System Identifier Dictionary, Enterprise Relational Model, and Enterprise Relational Foundation

\---

# Purpose

This document derives a schema specification — entities, attributes, logical types, keys, and logical constraints — from the already-approved Enterprise Logical Model, Cross-System Identifier Dictionary, Enterprise Relational Model, and current repository data. It is not SQL. It is the platform-independent blueprint from which target-platform DDL can be derived, including constraints that are stated as business rules here and translated into SQL syntax during implementation.

No decision in this document is untraceable. Every field, type, key, constraint, and migration decision is grounded in approved governance, repository evidence, or an explicitly labeled engineering assumption:

* **\[Governance]** — required by the Enterprise Logical Model, Identifier Dictionary, or Identifier Governance Review. Not open for reinterpretation here.
* **\[Repository]** — observed directly in current CSV data (value formats, enumerations, row counts). Informs confidence; flagged with sample size since Northstar's datasets are small.
* **\[Assumption]** — a proposed engineering decision not fully determined by governance or data. Flagged as a proposal, open to correction.

\---

# Conventions

* **Logical types are platform-neutral** (`INTEGER`, `TEXT`, `DATE`, `TIMESTAMP`, `BOOLEAN`, `DECIMAL`), since platform choice (SQLite vs. PostgreSQL) remains an open decision per Enterprise Relational Foundation. Platform-specific type mapping is deferred to SQL Implementation.
* **Structural ordering follows dependency tiers** (Tier 0–5), as established in Enterprise Relational Foundation's Implementation Order. Tiers are not renamed to Object Model taxonomy labels — dependency order and taxonomy classification diverge starting at Tier 1 (Corrective Action, a Work object, depends on two Assessment-tier entities). Each entity records its taxonomy classification separately, as a labeled field, so that traceability isn't lost — it just doesn't drive structure.
* **Logical constraints are stated as business rules, not SQL syntax.** A permitted-values list and its evidence are recorded; whether it becomes a `CHECK` constraint, an application-layer validation, or something else is an implementation note, not a decision made here.
* **Per-entity template:** Purpose, Object Model Classification, Canonical Identifier, Foreign Keys, **Dependencies**, Business Candidate Keys, Attributes (Logical Type), Logical Constraints, Deferred Logical Constraints, Migration Considerations, Future Expansion.
* **Dependencies** (added starting Tier 1; not retrofitted to Tier 0) identifies the prerequisite entities that must exist before this table can be built. It is independent of the Foreign Keys list — Dependencies reflects only this entity's own foreign keys, not entities that reference it through an associative entity. Tier 0 entities have no Dependencies section since "None" is already implied by Foreign Keys: None at that tier.

\---

# Build Status

|Tier|Entities|Status|
|-|-|-|
|Tier 0|Location, Employee, Vendor|**Locked**|
|Tier 1|Inventory Item, Ticket, Assignment, Coverage Schedule, Workload Record|**Locked**|
|Tier 2|Shipment, Replenishment, Location Inventory, Workforce Escalation, Assignment Ticket|**Locked**|
|Tier 3|Inventory Discrepancy, Shortage, Fulfillment Event, Shipment Replenishment Allocation|**Locked**|
|Tier 4|SLA Event, Replenishment Shortage Response|**Locked**|
|Tier 5|Corrective Action, Assignment Corrective Action|Not started|

Per agreed process, Tiers 0–4 are locked. Tier 5 is the final derivation stage and will be reviewed independently before the Enterprise Relational Schema is approved as a complete document.

\---

# Tier 0 — Foundation

## Location

* **Purpose:** Identifies operational facilities, support centers, hubs, or managed locations referenced throughout the enterprise. **\[Governance]**
* **Object Model Classification:** Enterprise Foundation Object
* **Canonical Identifier:** `location\_id` — `TEXT`, format `LOC-\[LOCATION]-##` **\[Governance — Identifier Dictionary]**

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`location\_id`|`TEXT`|No (PK)|\[Governance]|

* **Foreign Keys:** None (Tier 0).
* **Business Candidate Keys:** None approved. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `location\_id` must be unique across all records. Implementation Note: becomes the primary-key constraint at SQL implementation.
* **Deferred Logical Constraints:** None applicable — Location has no other attributes to constrain yet.
* **Migration Considerations:** No dedicated Location dataset currently exists. `location\_id` values must be collected as the **distinct set** of location identifiers appearing across Shipment, Replenishment, Shortage, Inventory Discrepancy, Location Inventory, and Ticket data during migration — this table is populated by extraction, not by loading a source file. **\[Assumption — no source-of-truth file exists; this is a proposed migration approach, not a governance requirement]**
* **Future Expansion:** The Enterprise Object Model already flags the absence of a dedicated Location registry as a known limitation. This schema intentionally creates only a minimal table (identifier only) rather than inventing descriptive attributes (name, address, type, capacity) with no supporting evidence anywhere in the repository. Adding such attributes is legitimate future scope once the business defines them — not proposed here. **\[Assumption, explicitly scoped as minimal]**

\---

## Employee

* **Purpose:** Uniquely identifies workforce personnel and their organizational placement. **\[Governance]**
* **Object Model Classification:** Enterprise Foundation Object
* **Canonical Identifier:** `employee\_id` — `TEXT`, format `EMP-###` **\[Governance — Identifier Dictionary]**

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`employee\_id`|`TEXT`|No (PK)|\[Governance]|
|`employee\_name`|`TEXT`|No|\[Governance — Domain-Authoritative]. Required for human-readable workforce identity and Ticket owner reconciliation.|
|`department`|`TEXT`|No|\[Governance — Domain-Authoritative, pending organizational-semantics reconciliation]|
|`team`|`TEXT`|No|\[Governance — same reconciliation caveat]|
|`role`|`TEXT`|No|\[Governance — Domain-Authoritative]. Left unconstrained — the 15-row sample shows too many distinct values to treat confidently as a bounded set, unlike `department`/`team`. **\[Assumption]**|
|`employment\_status`|`TEXT`|No|\[Governance — Enterprise-Shared]. See Logical Constraints.|
|`active\_flag`|`BOOLEAN`|No|\[Governance — Enterprise-Shared]. See Logical Constraints.|
|`primary\_shift`|`TEXT`|Yes|\[Governance — Descriptive-or-Derived]. Observed: `Day`, `Evening`, `Variable`. **\[Repository, n=15]**|
|`standard\_weekly\_hours`|`INTEGER`|Yes|\[Governance — Descriptive-or-Derived]. Observed: `24`, `32`, `40`. **\[Repository, n=15]**|
|`skill\_area`|`TEXT`|Yes|\[Governance — Descriptive-or-Derived]|
|`coverage\_priority`|`TEXT`|Yes|\[Governance — Descriptive-or-Derived]. Observed: `High`, `Moderate`, `Low`. **\[Repository, n=15]**|

* **Foreign Keys:** None (Tier 0).
* **Business Candidate Keys:** None approved. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `employee\_id` must be unique across all records. Implementation Note: becomes the primary-key constraint at SQL implementation.
  * **Employment Status.** Permitted Values: `Active`, `Leave`. Repository Evidence: 15/15 rows show only these two values. Implementation Note: may become a SQL `CHECK` constraint after the business confirms this list is exhaustive — 15 rows is not strong enough evidence on its own (e.g., "Terminated" could plausibly exist and simply not appear in the current roster). Until confirmed, an application-layer validation is preferable to a hard database constraint.
  * **Active Flag.** Permitted Values: `TRUE`, `FALSE`. Implementation Note: standard boolean constraint at SQL implementation, not contingent on further evidence.
* **Deferred Logical Constraints:** `department`/`team` are intentionally **not** given a permitted-values list or reference-table constraint here — the Enterprise Logical Model already flagged their enterprise-wide semantics as pending reconciliation. Constraining them now would lock in unreconciled values. **\[Governance — carried forward from Enterprise Logical Model]**
* **Migration Considerations:** Direct load from `workforce-roster.csv`; no field renaming required. `employee\_name` must be retained because Ticket `assigned\_owner` reconciliation depends on matching free-text names to canonical `employee\_id` values.
* **Future Expansion:** If Department/Team reconciliation produces governed `department\_id`/`team\_id` reference tables (already anticipated in the Identifier Dictionary's Entity Expansion Standards), `department` and `team` become foreign keys at that point rather than free text. Not proposed here.

\---

## Vendor

* **Purpose:** Uniquely identifies a supplier or vendor. **\[Governance]**
* **Object Model Classification:** Enterprise Foundation Object
* **Canonical Identifier:** `vendor\_id` — `TEXT`, format `VEND-###` **\[Governance — Identifier Dictionary]**

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`vendor\_id`|`TEXT`|No (PK)|\[Governance]|
|`vendor\_type`|`TEXT`|No|\[Governance — Domain-Authoritative]. See Logical Constraints.|
|`primary\_service\_category`|`TEXT`|No|\[Governance — Domain-Authoritative]. Observed: `Clinical Equipment`, `Distribution Support`, `Emergency Supplies`, `General Operations`, `Medical Supplies`. **\[Repository, n=12]**|
|`risk\_tier`|`TEXT`|No|\[Governance — Domain-Authoritative]. See Logical Constraints.|
|`active\_vendor\_flag`|`BOOLEAN`|No|\[Governance — Enterprise-Shared]|
|`vendor\_name`|`TEXT`|No|\[Governance — Domain-Authoritative]|
|`support\_level`|`TEXT`|Yes|\[Governance — Domain-Authoritative]. Observed: `Core Operational Support`, `Emergency Support`, `Logistics Support`, `Specialty Support`, `Supplemental Support`. **\[Repository, n=12]**|
|`preferred\_vendor\_flag`|`BOOLEAN`|Yes|\[Governance — Domain-Authoritative]|
|`emergency\_fulfillment\_flag`|`BOOLEAN`|Yes|\[Governance — Domain-Authoritative]|
|`primary\_contact\_team`|`TEXT`|Yes|\[Governance — Domain-Authoritative]. Observed: `Operations Coordination Center`, `Supply \& Inventory Operations`, `Vendor \& Service Management`. **\[Repository, n=12]**|
|`notes`|`TEXT`|Yes|\[Governance — Descriptive-or-Derived]|

* **Foreign Keys:** None (Tier 0).
* **Business Candidate Keys:** None approved. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `vendor\_id` must be unique across all records. Implementation Note: becomes the primary-key constraint at SQL implementation.
  * **Vendor Type.** Permitted Values: `Primary Supplier`, `Backup Supplier`, `Emergency Supplier`, `Logistics Partner`, `Specialty Supplier`. Repository Evidence: 12/12 rows. Implementation Note: same provisional caveat as Employment Status — 12 rows is thin evidence for a hard constraint; confirm exhaustiveness with the business first.
  * **Risk Tier.** Permitted Values: `Critical`, `High`, `Moderate`, `Low`. Repository Evidence: 12/12 rows. Implementation Note: same provisional caveat.
  * **Boolean flags** (`active\_vendor\_flag`, `preferred\_vendor\_flag`, `emergency\_fulfillment\_flag`). Permitted Values: `TRUE`, `FALSE`. Implementation Note: standard boolean constraints, not contingent on further evidence.
* **Deferred Logical Constraints:** `primary\_service\_category` and `support\_level` enumerations were observed but are **not** given a permitted-values constraint here — 12 rows is a thinner basis for a category list this granular than for `vendor\_type`/`risk\_tier`. Recommend application-layer validation rather than a database constraint until the vendor roster grows. **\[Assumption]**
* **Migration Considerations:** Direct load from `vendor-master.csv`; no field renaming required.
* **Future Expansion:** None flagged.

\---

# Tier 1

## Inventory Item

* **Purpose:** Uniquely identifies an inventory item tracked across the enterprise. **\[Governance]**
* **Object Model Classification:** Enterprise Foundation Object
* **Canonical Identifier:** `item\_id` — `TEXT`, format `ITEM-####` **\[Governance — Identifier Dictionary]**
* **Foreign Keys:** `preferred\_vendor\_id` → Vendor.`vendor\_id` **\[Governance — scoped to preferred-sourcing role only; does not implement the full Vendor↔Inventory Item relationship, per Enterprise Logical Model]**
* **Dependencies:** Vendor (Tier 0)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`item\_id`|`TEXT`|No (PK)|\[Governance]|
|`item\_category`|`TEXT`|No|\[Governance — Domain-Authoritative]. See Logical Constraints.|
|`criticality\_level`|`TEXT`|No|\[Governance — Domain-Authoritative]. See Logical Constraints.|
|`unit\_of\_measure`|`TEXT`|No|\[Governance — Domain-Authoritative]. Observed: `box`, `case`, `kit`, `pack`. **\[Repository, n=8]**|
|`preferred\_vendor\_id`|`TEXT`|Yes|\[Governance — Enterprise-Shared, FK]|
|`active\_flag`|`BOOLEAN`|No|\[Governance — Enterprise-Shared]|
|`item\_name`|`TEXT`|No|\[Governance — Domain-Authoritative]|

* **Business Candidate Keys:** None approved. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `item\_id` unique across all records.
  * **Item Category.** Permitted Values: `Clinical Supplies`, `Compliance Supplies`, `PPE`, `Procedure Supplies`, `Wound Care Supplies`. Repository Evidence: 8/8 rows. Implementation Note: same provisional caveat as other small-sample enumerations — confirm exhaustiveness before treating as a hard constraint.
  * **Criticality Level.** Permitted Values: `Critical`, `High`, `Moderate`. Repository Evidence: 8/8 rows. Implementation Note: provisional, same caveat.
  * **Active Flag.** Permitted Values: `TRUE`, `FALSE`. Note: only `TRUE` appears in current 8-row data — the field is still boolean by definition, this is not evidence the value is fixed.
* **Deferred Logical Constraints:** None beyond the provisional caveats above.
* **Migration Considerations:** Direct load from `inventory-items.csv`. `preferred\_vendor\_id` values must resolve against the Vendor table already loaded (Tier 0) — this is the first tier where load order actually matters for referential integrity, not just convenience.
* **Future Expansion:** None flagged.

\---

## Ticket

* **Purpose:** Represents an operational ticket or incident record. **\[Governance]**
* **Object Model Classification:** Operational Work Object
* **Canonical Identifier:** `ticket\_id` — `TEXT`, format `INC-######` **\[Governance — Identifier Dictionary]**
* **Foreign Keys:** `location\_id` → Location.`location\_id` (planned); `employee\_id` → Employee.`employee\_id` (planned) — **both currently unenforceable; see Logical Constraints and Migration Considerations.**
* **Dependencies:** Location, Employee (both Tier 0) — **staged**, not enforced at initial creation. See below.

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`ticket\_id`|`TEXT`|No (PK)|\[Governance]|
|`category`|`TEXT`|No|\[Governance — Domain-Authoritative]. See Logical Constraints.|
|`priority`|`TEXT`|No|\[Governance — Domain-Authoritative]. See Logical Constraints.|
|`status`|`TEXT`|No|\[Governance — Enterprise-Shared]. See Logical Constraints.|
|`escalation\_flag`, `reopened\_flag`, `pending\_flag`|`BOOLEAN`|No|\[Governance — `escalation\_flag`: Enterprise-Shared; `reopened\_flag`/`pending\_flag`: Domain-Authoritative]|
|`sla\_target\_hours`|`INTEGER`|No|\[Governance — Domain-Authoritative]. Observed: `4`, `24`, `72`, `120`. **\[Repository, n=15]**|
|`sla\_met\_flag`|`BOOLEAN`|Yes|\[Governance — Domain-Authoritative]. Observed: `TRUE`, `FALSE`, and blank. **\[Repository, n=15]** — blank corresponds to tickets not yet resolved; nullability is a real business state, not missing data.|
|`requesting\_location`|`TEXT`|Yes|\[Assumption — legacy migration/source attribute, not a canonical relationship field]. Currently stores descriptive names (e.g., `Cary Distribution Hub 01`), not `location\_id` values. **\[Repository, n=15]**|
|`location\_id`|`TEXT`|Yes, until migrated|\[Governance — Enterprise-Shared, FK to Location]. Canonical target column; null until `requesting\_location` is reconciled. Whether `requesting\_location` is retained, renamed, or removed after reconciliation is a physical-design decision, not made here.|
|`assigned\_department`|`TEXT`|No|\[Governance — Domain-Authoritative, pending organizational-semantics reconciliation — same caveat as Employee's `department`/`team`]|
|`assigned\_owner`|`TEXT`|Yes|\[Assumption — legacy migration/source attribute, not a canonical relationship field]. Currently stores employee display names (e.g., `Avery Patel`), not `employee\_id` values. **\[Repository, n=15]**|
|`employee\_id`|`TEXT`|Yes, until migrated|\[Governance — Enterprise-Shared, FK to Employee]. Canonical target column; null until `assigned\_owner` is reconciled.|
|`created\_at`, `first\_response\_at`, `resolved\_at`, `closed\_at`|`TIMESTAMP`|`first\_response\_at`/`resolved\_at`/`closed\_at` Yes; `created\_at` No|\[Governance — Domain-Authoritative]|
|`resolution\_hours`, `response\_hours`|`DECIMAL`|Yes|\[Governance — Descriptive-or-Derived, calculated]|
|`summary`, `resolution\_notes`|`TEXT`|Yes|\[Governance — Descriptive-or-Derived]|

* **Business Candidate Keys:** None approved. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `ticket\_id` unique across all records.
  * **Category.** Permitted Values: `Data Quality \& Compliance`, `Inventory \& Supply`, `Operational Incident`, `Scheduling \& Resource Coordination`, `Technical \& Systems Support`, `Vendor \& Delivery Management`. Repository Evidence: 15/15 rows. Implementation Note: provisional, standard small-sample caveat.
  * **Priority.** Permitted Values: `Priority 1 — Critical`, `Priority 2 — High`, `Priority 3 — Moderate`, `Priority 4 — Low`. Repository Evidence: 15/15 rows.
  * **Status.** Permitted Values: `Assigned`, `Closed`, `In Progress`, `Pending`. Repository Evidence: 15/15 rows.
  * **Location and Owner References.** Implementation Note: **not** enforced as foreign keys at initial table creation. Per the Enterprise Logical Model's documented migration sequence, `requesting\_location` and `assigned\_owner` are staged as free text first, profiled and mapped against Location and Employee, and only constrained after reconciliation. This is a governance decision already made, carried forward here, not a new one.
* **Deferred Logical Constraints:** `assigned\_department` is not given a permitted-values constraint, for the same organizational-semantics reconciliation reason as Employee's `department`/`team`.
* **Migration Considerations:** This is the entity where the Ticket free-text migration sequence applies: profile `requesting\_location`/`assigned\_owner` values → build mapping rules → migrate resolvable values → review exceptions → enforce FK.

  * All four distinct `requesting\_location` values have clear candidate mappings to the four governed `location\_id` values, but the mappings must still be formally validated and recorded.
  * Only 3 of 15 current tickets map by exact `assigned\_owner` name to `workforce-roster.csv`. The unmatched names are Avery Patel, Marcus Nguyen, Samantha Ortiz, and Taylor Brooks. `employee\_id` therefore remains nullable until the roster or source data is reconciled.
  * `tickets-v1.csv` is Windows-1252 encoded while the other current datasets are UTF-8 or UTF-8 with BOM. Migration must normalize encoding before validation and load.
**\[Repository, n=15; mapping and encoding normalization are migration prerequisites]**
* **Future Expansion:** None flagged beyond the already-documented FK staging.

\---

## Assignment

* **Purpose:** Represents a workforce assignment. **\[Governance]**
* **Object Model Classification:** Operational Work Object
* **Canonical Identifier:** `assignment\_id` — `TEXT`, format `ASSIGN-###` **\[Governance — Identifier Governance Review]**
* **Foreign Keys:** `employee\_id` → Employee.`employee\_id`
* **Dependencies:** Employee (Tier 0)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`assignment\_id`|`TEXT`|No (PK)|\[Governance]|
|`employee\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]|
|`assignment\_category`|`TEXT`|No|\[Governance — Domain-Authoritative]. See Logical Constraints.|
|`assignment\_status`|`TEXT`|No|\[Governance — Enterprise-Shared]. Observed: `Active`, `Suspended`. **\[Repository, n=18]**|
|`start\_date`|`DATE`|No|\[Governance — Domain-Authoritative]|
|`end\_date`|`DATE`|Yes|\[Governance — Domain-Authoritative]. Observed: blank in all 18 current rows — no assignment has ended yet in the simulation's current state. **\[Repository, n=18]**|
|`assignment\_name`|`TEXT`|No|\[Governance — Domain-Authoritative]|
|`priority\_level`|`TEXT`|No|\[Governance — Domain-Authoritative]. Observed: `Critical`, `High`, `Moderate`, `Low`. **\[Repository, n=18]**|
|`estimated\_hours\_per\_week`|`INTEGER`|Yes|\[Governance — Domain-Authoritative]. Observed: `10`, `15`, `20`, `25`, `30`. **\[Repository, n=18]**|
|`cross\_functional\_flag`|`BOOLEAN`|No|\[Governance — Domain-Authoritative]|

* **Business Candidate Keys:** None approved — Assignment carries no work-target reference and its categories are broad and recurring. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `assignment\_id` unique across all records.
  * **Assignment Category.** Permitted Values: `Escalation Management`, `Inventory Operations`, `Ticketing`, `Vendor Management`, `Workforce Coordination`. Repository Evidence: 18/18 rows. Implementation Note: provisional.
  * **Assignment Status.** Permitted Values: `Active`, `Suspended`. Repository Evidence: 18/18 rows. Implementation Note: provisional — a status like `Completed` seems plausible given `end\_date` exists as a column, but doesn't appear in current data.
* **Deferred Logical Constraints:** None beyond the provisional caveats above.
* **Migration Considerations:** Direct load from `workforce-assignments.csv`; requires Employee (Tier 0) loaded first.
* **Future Expansion:** Once `AssignmentTicket` and `AssignmentCorrectiveAction` (Tier 2 and Tier 5) exist, Assignment's practical work-target relationship becomes visible through those tables — not through any new column on Assignment itself.

\---

## Coverage Schedule

* **Purpose:** Represents a workforce coverage schedule record. **\[Governance]**
* **Object Model Classification:** Operational State Object
* **Canonical Identifier:** `coverage\_schedule\_id` — `TEXT`, format `SCHED-###` **\[Governance — Identifier Governance Review; rename of legacy field `schedule\_id`, documented as a migration alias]**
* **Foreign Keys:** `employee\_id` → Employee.`employee\_id`
* **Dependencies:** Employee (Tier 0)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`coverage\_schedule\_id`|`TEXT`|No (PK)|\[Governance]|
|`employee\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]|
|`schedule\_date`|`DATE`|No|\[Governance — Domain-Authoritative]|
|`shift\_type`|`TEXT`|No|\[Governance — Domain-Authoritative]. Observed: `Day`, `Evening`, `Variable`. **\[Repository, n=15]**|
|`coverage\_status`|`TEXT`|No|\[Governance — Enterprise-Shared]. Observed: `Covered`, `Uncovered`. **\[Repository, n=15]**|
|`scheduled\_hours`|`INTEGER`|Yes|\[Governance — Domain-Authoritative]. Observed: `6`, `8`. **\[Repository, n=15]**|
|`coverage\_area`|`TEXT`|Yes|\[Governance — Domain-Authoritative; descriptive text, not a Location reference]. Observed: `Cross-Team Support`, `Escalation Support`, `Inventory Support`, `Service Response`, `Vendor Operations`. **\[Repository, n=15]**|
|`coverage\_priority`|`TEXT`|Yes|\[Governance — Domain-Authoritative]. Observed: `High`, `Moderate`, `Low`. **\[Repository, n=15]**|
|`backup\_required\_flag`|`BOOLEAN`|Yes|\[Governance — Domain-Authoritative]|

* **Business Candidate Keys:** None approved. `location\_id` explicitly excluded — Coverage Schedule has no Location relationship in the approved Relational Model, and the underlying data confirms no `location\_id` column exists. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `coverage\_schedule\_id` unique across all records.
  * **Overlapping Coverage.** An Employee should not have incompatible overlapping coverage periods. Implementation Note: this rule is recognized but **structurally deferred** — it cannot currently be evaluated at all, by any mechanism, because Coverage Schedule has no `coverage\_start\_at`/`coverage\_end\_at` or governed shift-window definition to compare against. `schedule\_date` and `shift\_type` alone don't define when a period starts or ends. This is not a choice between enforcement mechanisms (trigger vs. application validation) — no mechanism can evaluate the rule until time boundaries or a controlled Shift definition are governed. Revisit once one of those exists.
  * **Shift Type.** Permitted Values: `Day`, `Evening`, `Variable`. Repository Evidence: 15/15 rows.
  * **Coverage Status.** Permitted Values: `Covered`, `Uncovered`. Repository Evidence: 15/15 rows.
* **Deferred Logical Constraints:** `coverage\_area` observed values are not proposed as a hard permitted-values constraint — it's documented as free descriptive text, not a governed reference list, and treating it as an enum risks implying a governance status it doesn't have.
* **Migration Considerations:** Source field `schedule\_id` renamed to `coverage\_schedule\_id`. Legacy alias documentation required per the Identifier Governance Review — the migration script must map old to new, not simply relabel silently.
* **Future Expansion:** None flagged.

\---

## Workload Record

* **Purpose:** Represents an employee workload measurement for a reporting period. **\[Governance]**
* **Object Model Classification:** Operational State Object
* **Canonical Identifier:** `workload\_record\_id` — `TEXT`, format `WORK-###` **\[Governance — Identifier Governance Review; rename of legacy field `workload\_id`, documented as a migration alias]**
* **Foreign Keys:** `employee\_id` → Employee.`employee\_id`
* **Dependencies:** Employee (Tier 0)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`workload\_record\_id`|`TEXT`|No (PK)|\[Governance]|
|`employee\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]|
|`reporting\_period`|`TEXT`|No|\[Governance — Enterprise-Shared]. Observed format: `2026-06`. **\[Repository, n=15]**|
|`workload\_status`|`TEXT`|No|\[Governance — Domain-Authoritative]. See Logical Constraints.|
|`assigned\_tasks`, `completed\_tasks`, `open\_tasks`|`INTEGER`|No|\[Governance — Domain-Authoritative]|
|`estimated\_hours`, `actual\_hours`|`DECIMAL`|Yes|\[Governance — Domain-Authoritative]|
|`capacity\_utilization\_percent`|`DECIMAL`|Yes|\[Governance — Descriptive-or-Derived, calculated]|

* **Business Candidate Keys:** `employee\_id` + `reporting\_period` — business-justified: one workload measurement per employee per period. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `workload\_record\_id` unique across all records.
  * **Business Key.** Uniqueness Rule: (`employee\_id`, `reporting\_period`) must be unique. Repository Evidence: 15/15 rows show no collision. Implementation Note: this constraint is governance-backed independent of the data check — it should be enforced as a `UNIQUE` constraint at implementation regardless of sample size, unlike the provisional enumerations elsewhere in this document.
  * **Workload Status.** Permitted Values: `Balanced`, `Overloaded`, `Unavailable`, `Underutilized`. Repository Evidence: 15/15 rows. Implementation Note: provisional, standard caveat.
* **Deferred Logical Constraints:** None beyond the provisional caveat above.
* **Migration Considerations:** Source field `workload\_id` renamed to `workload\_record\_id`, same legacy-alias treatment as Coverage Schedule.
* **Future Expansion:** None flagged.

\---

# Tier 2

## Shipment

* **Purpose:** Represents a vendor shipment event. **\[Governance]**
* **Object Model Classification:** Movement Object
* **Canonical Identifier:** `shipment\_id` — `TEXT`, format `SHIP-####` **\[Governance — Identifier Dictionary]**
* **Foreign Keys:** `vendor\_id` → Vendor.`vendor\_id`; `item\_id` → Inventory Item.`item\_id`; `location\_id` → Location.`location\_id`; `related\_ticket\_id` → Ticket.`ticket\_id` (optional)
* **Dependencies:** Vendor, Inventory Item, Location (Tier 0–1, all required); Ticket (Tier 1, optional — required only when `related\_ticket\_id` is populated)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`shipment\_id`|`TEXT`|No (PK)|\[Governance]|
|`vendor\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]|
|`item\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]. Retains the one-item-per-shipment scope decision — see Deferred Logical Constraints.|
|`location\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]|
|`related\_ticket\_id`|`TEXT`|Yes|\[Governance — Enterprise-Shared, FK, optional]. Observed populated in 3 of 6 current rows. **\[Repository, n=6]**|
|`delivery\_status`|`TEXT`|No|\[Governance — Enterprise-Shared]. See Logical Constraints.|
|`ordered\_quantity`|`INTEGER`|No|\[Governance — Domain-Authoritative]|
|`received\_quantity`|`INTEGER`|Yes|\[Governance — Domain-Authoritative]. Blank in current data corresponds to shipments not yet received. **\[Repository, n=6]**|
|`order\_date`|`DATE`|No|\[Governance — Domain-Authoritative]|
|`expected\_delivery\_date`|`DATE`|No|\[Governance — Domain-Authoritative]|
|`actual\_delivery\_date`|`DATE`|Yes|\[Governance — Domain-Authoritative]. Blank corresponds to shipments not yet delivered. **\[Repository, n=6]**|
|`fulfillment\_accuracy\_flag`|`BOOLEAN`|Yes|\[Governance — Descriptive-or-Derived, computed]. Blank where accuracy can't yet be assessed (shipment not received). **\[Repository, n=6]**|
|`delay\_flag`|`BOOLEAN`|No|\[Governance — Descriptive-or-Derived, computed]|

* **Business Candidate Keys:** None approved. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `shipment\_id` unique across all records.
  * **Delivery Status.** Permitted Values: `Delayed`, `Partial`, `Pending`, `Received`. Repository Evidence: 6/6 rows. Implementation Note: provisional — 6 rows is a thin sample even by this document's own standard; treat this enumeration as more tentative than Tier 0/1's constraints.
* **Deferred Logical Constraints:** `item\_id` remains single-valued per shipment. Verified against current data: 0 of 6 `shipment\_id` values carry more than one `item\_id`. This is the same scope decision already recorded in the Enterprise Logical Model — restated here rather than re-derived, since the underlying evidence hasn't changed. A `Shipment Line` associative entity remains not introduced.
* **Migration Considerations:** Direct load from `vendor-shipments.csv`, requires Vendor, Inventory Item, Location (all loaded) and, where populated, Ticket.
* **Future Expansion:** None flagged.

\---

## Replenishment

* **Purpose:** Represents a replenishment workflow event. **\[Governance]**
* **Object Model Classification:** Movement Object
* **Canonical Identifier:** `replenishment\_id` — `TEXT`, format `REPL-####` **\[Governance — Identifier Dictionary]**
* **Foreign Keys:** `item\_id` → Inventory Item.`item\_id`; `location\_id` → Location.`location\_id`; `vendor\_id` → Vendor.`vendor\_id` (optional); `related\_ticket\_id` → Ticket.`ticket\_id` (optional)
* **Dependencies:** Inventory Item, Location (Tier 0–1, required); Vendor (Tier 0, optional); Ticket (Tier 1, optional)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`replenishment\_id`|`TEXT`|No (PK)|\[Governance]|
|`item\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]|
|`location\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]|
|`vendor\_id`|`TEXT`|Conditional|\[Governance — Enterprise-Shared FK; conditional nullability is a repository-supported engineering decision, not prior governance, n=5]|
|`related\_ticket\_id`|`TEXT`|Yes|\[Governance — Enterprise-Shared, FK, optional]|
|`replenishment\_type`|`TEXT`|No|\[Governance — Domain-Authoritative]. See Logical Constraints.|
|`replenishment\_status`|`TEXT`|No|\[Governance — Enterprise-Shared]. See Logical Constraints.|
|`requested\_quantity`|`INTEGER`|No|\[Governance — Domain-Authoritative]|
|`approved\_quantity`|`INTEGER`|Yes|\[Governance — Domain-Authoritative]|
|`request\_date`|`DATE`|No|\[Governance — Domain-Authoritative]|
|`expected\_arrival\_date`|`DATE`|Yes|\[Governance — Domain-Authoritative]|
|`received\_date`|`DATE`|Yes|\[Governance — Domain-Authoritative]|

* **Business Candidate Keys:** None approved. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `replenishment\_id` unique across all records.
  * **Replenishment Type.** Permitted Values: `Internal Transfer`, `Vendor Reorder`. Repository Evidence: 5/5 rows.
  * **Replenishment Status.** Permitted Values: `Approved`, `Delayed`, `In Transit`, `Received`. Repository Evidence: 5/5 rows. Implementation Note: 5 rows is a very thin sample; treat as more tentative than any prior tier.
  * **Vendor Presence Rule.** Proposed rule: `vendor\_id` is null for `Internal Transfer` and required for `Vendor Reorder`. This rule is supported by the meaning of the two replenishment types and by all five current records, but it was not previously established by governance. Confirm with the business before enforcing it as a hard database constraint. Implementation Note: not expressible as a simple `NOT NULL` regardless — a cross-field conditional rule, candidate for application-layer validation or a two-column `CHECK` at SQL Implementation.
* **Deferred Logical Constraints:** None beyond the caveats above.
* **Migration Considerations:** Direct load from `replenishment-events.csv`; requires Inventory Item, Location, and — where populated — Vendor and Ticket.
* **Future Expansion:** None flagged.

\---

## Location Inventory

* **Purpose:** Represents the current stock position of one inventory item at one location. **\[Governance]**
* **Object Model Classification:** Operational State Object
* **Canonical Identifier:** `location\_inventory\_id` — `TEXT`, format `LOCINV-####` **\[Governance — Identifier Governance Review; already the governed physical field name, elevated to canonical cross-system status]**
* **Foreign Keys:** `item\_id` → Inventory Item.`item\_id`; `location\_id` → Location.`location\_id`
* **Dependencies:** Inventory Item, Location (Tier 0–1)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`location\_inventory\_id`|`TEXT`|No (PK)|\[Governance]|
|`item\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]|
|`location\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]|
|`current\_stock`|`INTEGER`|No|\[Governance — Enterprise-Shared]|
|`stock\_status`|`TEXT`|No|\[Governance — Enterprise-Shared]. See Logical Constraints.|
|`reorder\_point`|`INTEGER`|Yes|\[Governance — Domain-Authoritative]|
|`target\_stock\_level`|`INTEGER`|Yes|\[Governance — Domain-Authoritative]|
|`safety\_stock\_level`|`INTEGER`|Yes|\[Governance — Domain-Authoritative]|
|`last\_count\_date`|`DATE`|Yes|\[Governance — Domain-Authoritative]|

* **Business Candidate Keys:** `location\_id` + `item\_id` — business-justified: the enterprise recognizes exactly one active stock position per item per location. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `location\_inventory\_id` unique across all records.
  * **Business Key.** Uniqueness Rule: (`location\_id`, `item\_id`) must be unique. Implementation Note: governance-backed independent of sample size, same treatment as Workload Record's business key in Tier 1 — enforce as a `UNIQUE` constraint regardless of the current 8-row sample.
  * **Stock Status.** Permitted Values: `Critical Low`, `Low Stock`, `Normal`, `Overstocked`, `Stockout`. Repository Evidence: 8/8 rows. Implementation Note: provisional, standard caveat.
* **Deferred Logical Constraints:** None beyond the caveat above.
* **Migration Considerations:** Direct load from `location-inventory.csv`; requires Inventory Item and Location loaded first.
* **Future Expansion:** None flagged. The deferred Shipment→Location Inventory analytical/historical relationship (transaction history) remains explicitly out of scope, per Enterprise Relational Foundation.

\---

## Workforce Escalation

* **Purpose:** Represents a workforce escalation record. **\[Governance]**
* **Object Model Classification:** Assessment Object
* **Canonical Identifier:** `escalation\_id` — `TEXT`, format `WF-ESC-###` **\[Governance — Identifier Governance Review; no rename — attribute name already matched current data]**
* **Foreign Keys:** `related\_ticket\_id` → Ticket.`ticket\_id` (optional) — **new column, not present in current data; see Migration Considerations**
* **Dependencies:** Ticket (Tier 1, optional — only once `related\_ticket\_id` is added)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`escalation\_id`|`TEXT`|No (PK)|\[Governance]|
|`related\_ticket\_id`|`TEXT`|Yes|\[Governance — Enterprise-Shared, FK, optional]. **Does not exist in current repository data** — this column is new implementation scope, not a migrated field. **\[Governance — Enterprise Logical Model, Relationships Implemented Through an Existing Object]**|
|`department`|`TEXT`|No|\[Governance — Domain-Authoritative, organizational semantics pending reconciliation]. Observed: `Operations`, `Vendor Management`. **\[Repository, n=10]**|
|`escalation\_type`|`TEXT`|No|\[Governance — Domain-Authoritative]. See Logical Constraints.|
|`severity\_level`|`TEXT`|No|\[Governance — Domain-Authoritative]. Observed: `Critical`, `High`, `Low`, `Moderate`. **\[Repository, n=10]**|
|`current\_status`|`TEXT`|No|\[Governance — Enterprise-Shared]. See Logical Constraints.|
|`escalation\_date`|`DATE`|No|\[Governance — Domain-Authoritative]|
|`affected\_team`|`TEXT`|Yes|\[Governance — Domain-Authoritative, organizational semantics pending reconciliation]. Observed: `Coverage Support`, `Escalation Support`, `Inventory Support`, `Service Response`, `Vendor Operations`. **\[Repository, n=10]**|
|`root\_cause`|`TEXT`|Yes|\[Governance — Domain-Authoritative]. 10 distinct values across 10 rows — effectively free text at current volume, not proposed as an enumeration. **\[Repository, n=10]**|
|`resolution\_owner`|`TEXT`|Yes|\[Governance — Domain-Authoritative]. Observed: `Inventory Manager`, `Operations Manager`, `Vendor Manager`, `Workforce Coordinator` — role titles, not `employee\_id` values; no employee-level FK exists for this entity yet, per Enterprise Logical Model. **\[Repository, n=10]**|
|`business\_impact`|`TEXT`|Yes|\[Governance — Descriptive-or-Derived, narrative]|

* **Business Candidate Keys:** None approved. The architecture explicitly allows escalations not tied to one employee. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `escalation\_id` unique across all records.
  * **Escalation Type.** Permitted Values: `Capacity Constraint`, `Coverage Gap`, `Cross-Team Support Request`, `Escalation Queue Backlog`, `Staffing Shortage`, `Workload Imbalance`. Repository Evidence: 10/10 rows.
  * **Current Status.** Permitted Values: `In Progress`, `Monitoring`, `Open`, `Resolved`. Repository Evidence: 10/10 rows.
* **Deferred Logical Constraints:** `root\_cause` and `resolution\_owner` are not proposed as enumerations — `root\_cause` shows no repetition at all in the current sample (10 distinct values in 10 rows), and `resolution\_owner` looks role-based rather than a governed reference list.
* **Migration Considerations:** Direct load from `workforce-escalations.csv`, with `related\_ticket\_id` added as a new nullable column with no source data to populate it initially — it starts empty and is populated going forward, not backfilled from history that doesn't exist.
* **Future Expansion:** `employee\_id` remains unrepresented per the Enterprise Logical Model's deferred Workforce Escalation↔Employee relationship. Not added here.

\---

## Assignment Ticket

* **Purpose:** Associative entity resolving Assignment's many-to-many relationship to Ticket, one of two typed relationship entities replacing a rejected polymorphic design. **\[Governance — Enterprise Logical Model, Associative Entity Resolution]**
* **Object Model Classification:** Not applicable — a logical relationship entity, not a canonical enterprise object. **\[Governance]**
* **Canonical Identifier:** Not applicable — this is a relationship entity, not a canonical enterprise object. **\[Governance]**
* **Foreign Keys:** `assignment\_id` → Assignment.`assignment\_id`; `ticket\_id` → Ticket.`ticket\_id`
* **Dependencies:** Assignment, Ticket (both Tier 1, both required)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`assignment\_id`|`TEXT`|No (PK, part 1)|\[Governance — Enterprise Logical Model]|
|`ticket\_id`|`TEXT`|No (PK, part 2)|\[Governance — Enterprise Logical Model]|

* **Business Candidate Key:** (`assignment\_id`, `ticket\_id`) — the minimal business-meaningful combination that uniquely identifies the relationship.
* **Primary-Key Strategy:** The business candidate key is implemented directly as the composite primary key; no surrogate identifier is introduced, since this associative entity has no independent lifecycle or relationship-level attributes beyond the pairing itself. **\[Governance — see the associative-entity exception now recorded in Enterprise Relational Foundation's Key Strategy]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: (`assignment\_id`, `ticket\_id`) must be unique — no duplicate pairing.
* **Deferred Logical Constraints:** None.
* **Migration Considerations:** No current source data — this table has no representation in `workforce-assignments.csv` today. Populated only going forward, once Assignment-to-Ticket linkage is actively tracked. This is new implementation scope, not a migration.
* **Future Expansion:** None flagged.

\---

# Tier 3

## Inventory Discrepancy

* **Purpose:** Represents a discrepancy between expected and counted inventory. **\[Governance]**
* **Object Model Classification:** Operational State Object
* **Canonical Identifier:** `discrepancy\_id` — `TEXT`, format `DISC-####` **\[Governance — Identifier Dictionary]**
* **Foreign Keys:** `item\_id` → Inventory Item.`item\_id`; `location\_id` → Location.`location\_id`; `related\_ticket\_id` → Ticket.`ticket\_id` (optional)
* **Dependencies:** Inventory Item, Location (Tier 0–1, required); Ticket (Tier 1, optional)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`discrepancy\_id`|`TEXT`|No (PK)|\[Governance]|
|`item\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]|
|`location\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]|
|`related\_ticket\_id`|`TEXT`|Yes|\[Governance — Enterprise-Shared, FK, optional]. Observed populated in 4 of 5 current rows. **\[Repository, n=5]**|
|`investigation\_status`|`TEXT`|No|\[Governance — Enterprise-Shared]. See Logical Constraints.|
|`expected\_quantity`, `counted\_quantity`|`INTEGER`|No|\[Governance — Domain-Authoritative]|
|`variance\_quantity`|`INTEGER` (signed)|No|\[Governance — Domain-Authoritative]. **Repository-supported type detail:** observed values include negatives (e.g., `-15`) alongside positives (`20`) — this is a signed quantity (counted minus expected), not an unsigned count. **\[Repository, n=5]**|
|`discrepancy\_type`|`TEXT`|No|\[Governance — Domain-Authoritative]. See Logical Constraints.|
|`discovered\_date`|`DATE`|No|\[Governance — Domain-Authoritative]|
|`resolved\_date`|`DATE`|Yes|\[Governance — Domain-Authoritative]. Blank corresponds to unresolved records. **\[Repository, n=5]**|

* **Business Candidate Keys:** None approved. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `discrepancy\_id` unique across all records.
  * **Discrepancy Type.** Permitted Values: `Count Variance`, `Damaged Inventory`, `Missing Inventory`, `Receiving Error`, `System Entry Error`. Repository Evidence: 5/5 rows. Implementation Note: provisional, thin-sample caveat applies (5 rows).
  * **Investigation Status.** Permitted Values: `Escalated`, `Investigating`, `Mitigating`, `Open`, `Resolved`. Repository Evidence: 5/5 rows.
  * **Variance Calculation Rule.** `variance\_quantity = counted\_quantity - expected\_quantity`. Repository Evidence: verified against all 5 current rows individually, exact match in every case (e.g., `DISC-1003`: `160 - 140 = 20`, matches recorded variance). Implementation Note: whether this becomes a generated/computed column, a stored value with validation, or a migration-time derivation is a SQL Implementation decision, not made here.
* **Deferred Logical Constraints:** None beyond the caveats above.
* **Migration Considerations:** Direct load from `inventory-discrepancies.csv`; requires Inventory Item, Location and, where populated, Ticket. Current references to `INC-100018` and `INC-100031` do not resolve in `tickets-v1.csv`; strict Ticket FK enforcement must wait until those records are added, corrected, or explicitly retired.
* **Future Expansion:** None flagged.

\---

## Shortage

* **Purpose:** Represents a detected inventory shortage. **\[Governance]**
* **Object Model Classification:** Operational State Object
* **Canonical Identifier:** `shortage\_id` — `TEXT`, format `SHORT-####` **\[Governance — Identifier Dictionary]**
* **Foreign Keys:** `item\_id` → Inventory Item.`item\_id`; `location\_id` → Location.`location\_id`; `related\_ticket\_id` → Ticket.`ticket\_id` (optional)
* **Dependencies:** Inventory Item, Location (Tier 0–1, required); Ticket (Tier 1, optional)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`shortage\_id`|`TEXT`|No (PK)|\[Governance]|
|`item\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]|
|`location\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]|
|`related\_ticket\_id`|`TEXT`|Yes|\[Governance — Enterprise-Shared, FK, optional]. Observed populated in 3 of 5 current rows. **\[Repository, n=5]**|
|`shortage\_severity`|`TEXT`|No|\[Governance — Enterprise-Shared]. See Logical Constraints.|
|`resolution\_status`|`TEXT`|No|\[Governance — Enterprise-Shared]. See Logical Constraints.|
|`escalation\_flag`|`BOOLEAN`|No|\[Governance — Enterprise-Shared]|
|`shortage\_detected\_date`|`DATE`|No|\[Governance — Domain-Authoritative]|
|`estimated\_days\_of\_stockout`|`INTEGER`|Yes|\[Governance — Domain-Authoritative]. Observed range 1–4 in current data — a quantity, not a category; no enumeration proposed. **\[Repository, n=5]**|
|`operational\_impact`|`TEXT`|Yes|\[Governance — Domain-Authoritative *as tagged in the Enterprise Logical Model*]. **Repository observation worth flagging:** all 5 current values are distinct, full narrative sentences (e.g., "Gauze inventory temporarily below recommended safety threshold"), not structured category values. This reads closer to Descriptive-or-Derived than Domain-Authoritative in practice — noted as a tension between the Logical Model's tag and what the data actually looks like, not resolved here. Type and nullability are unaffected either way (unconstrained `TEXT`); the tag affects how the physical schema phase should treat it (e.g., whether it's a candidate for future structuring into fields, vs. permanently narrative). **\[Repository, n=5]**|

* **Business Candidate Keys:** None approved. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `shortage\_id` unique across all records.
  * **Shortage Severity.** Permitted Values: `Critical`, `High`, `Low`, `Moderate`. Repository Evidence: 5/5 rows.
  * **Resolution Status.** Permitted Values: `Escalated`, `Mitigating`, `Monitoring`, `Open`, `Resolved`. Repository Evidence: 5/5 rows.
* **Deferred Logical Constraints:** `operational\_impact` is not given a permitted-values constraint — see the provenance note above; it's narrative, not categorical, in the current data.
* **Migration Considerations:** Direct load from `shortage-events.csv`; requires Inventory Item, Location and, where populated, Ticket. Current reference `INC-100021` does not resolve in `tickets-v1.csv`; strict Ticket FK enforcement must wait until that record is added, corrected, or explicitly retired.
* **Future Expansion:** None flagged.

\---

## Fulfillment Event

* **Purpose:** Represents a vendor fulfillment assessment for a shipment. **\[Governance]**
* **Object Model Classification:** Assessment Object
* **Canonical Identifier:** `fulfillment\_event\_id` — `TEXT`, format `VF-####` **\[Governance — Identifier Governance Review]**
* **Foreign Keys:** `vendor\_id` → Vendor.`vendor\_id`; `shipment\_id` → Shipment.`shipment\_id`; `item\_id` → Inventory Item.`item\_id`; `location\_id` → Location.`location\_id`; `related\_ticket\_id` → Ticket.`ticket\_id` (optional)
* **Dependencies:** Vendor, Inventory Item, Location (Tier 0–1, required); Shipment (Tier 2, required); Ticket (Tier 1, optional)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`fulfillment\_event\_id`|`TEXT`|No (PK)|\[Governance]|
|`vendor\_id`, `shipment\_id`, `item\_id`, `location\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]|
|`related\_ticket\_id`|`TEXT`|Yes|\[Governance — Enterprise-Shared, FK, optional]. Observed populated in 3 of 6 current rows. **\[Repository, n=6]**|
|`fulfillment\_status`|`TEXT`|No|\[Governance — Enterprise-Shared]. See Logical Constraints.|
|`delivery\_status`|`TEXT`|No|\[Governance — Enterprise-Shared]. See Logical Constraints — **flagged discrepancy with Shipment.delivery\_status below.**|
|`order\_date`, `expected\_delivery\_date`|`DATE`|No|\[Governance — Domain-Authoritative]|
|`actual\_delivery\_date`|`DATE`|Yes|\[Governance — Domain-Authoritative]. Blank for undelivered shipments. **\[Repository, n=6]**|
|`expected\_quantity`|`INTEGER`|No|\[Governance — Domain-Authoritative]|
|`received\_quantity`|`INTEGER`|No|\[Governance — Domain-Authoritative]. Note: `0` appears as a real value (not blank) for at least one pending shipment — distinct from Shipment's own `received\_quantity`, which uses blank for the same state. **\[Repository, n=6]**|
|`fulfillment\_accuracy\_flag`, `delay\_flag`, `partial\_fulfillment\_flag`, `emergency\_fulfillment\_flag`, `escalation\_required\_flag`|`BOOLEAN`|No|\[Governance — Descriptive-or-Derived for accuracy/delay/partial flags (computed); Enterprise-Shared for `escalation\_required\_flag`]|
|`delay\_days`|`INTEGER`|No|\[Governance — Descriptive-or-Derived, computed]|
|`operational\_impact\_level`|`TEXT`|No|\[Governance — Domain-Authoritative]. See Logical Constraints.|
|`notes`|`TEXT`|Yes|\[Governance — Descriptive-or-Derived, narrative]|

* **Business Candidate Keys:** None approved. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `fulfillment\_event\_id` unique across all records.
  * **Fulfillment Status.** Permitted Values: `Complete`, `Partial`, `Pending`. Repository Evidence: 6/6 rows.
  * **Delivery Status.** Permitted Values observed here: `Delayed`, `Delivered`, `Pending`. Repository Evidence: 6/6 rows.
  * **Operational Impact Level.** Permitted Values: `High`, `Low`, `Moderate`. Repository Evidence: 6/6 rows.
  * **Emergency Fulfillment Flag.** Only `FALSE` observed in all 6 current rows. Note: still modeled as boolean, not as a fixed value — this reflects the current scenario data, not a business rule that the flag can never be true.
  * **Shipment Reference Consistency.** The `vendor\_id`, `item\_id`, and `location\_id` recorded on a Fulfillment Event must match the corresponding references on its `shipment\_id`. Implementation Note: this is a cross-table integrity rule requiring validation logic or trigger-based enforcement at SQL Implementation. **\[Assumption — required to prevent contradictory governed references]**
* **Deferred Logical Constraints:** Shipment and Fulfillment Event also repeat dates, quantities, and delivery-state information. Those fields are not forced to match until SQL Implementation defines the authoritative source and translation rules for pending, partial, received, and delivered states.
* **Open Question — `delivery\_status` vocabulary mismatch:** Shipment's `delivery\_status` (Tier 2) observed values are `Delayed`, `Partial`, `Pending`, `Received`. Fulfillment Event's `delivery\_status` observed values are `Delayed`, `Delivered`, `Pending` — no `Partial` or `Received`, but a `Delivered` value Shipment never uses, despite both entities sharing the same `shipment\_id` for overlapping records. This could be two legitimately different vocabularies for two different questions (Shipment's own delivery state vs. the vendor-assessment view of it), or an unreconciled inconsistency between two datasets describing the same underlying event. Not resolved here — flagged for a decision before SQL Implementation, since it affects whether these should be two independent CHECK enumerations or a single shared one.
* **Migration Considerations:** Direct load from `vendor-fulfillment-events.csv`; requires Vendor, Inventory Item, Location (Tier 0–1) and Shipment (Tier 2) loaded first — this is the first Tier 3 entity with a Tier 2 dependency, consistent with its position in the build order.
* **Future Expansion:** None flagged.

\---

## Shipment Replenishment Allocation

**Naming note — approved.** Originally specified in the Enterprise Logical Model as `Shipment Replenishment Fulfillment`. Renamed to `Shipment Replenishment Allocation`, per approval: its defining attribute is a portion of a Shipment's quantity allocated toward satisfying a specific Replenishment request. "Fulfillment" in this repository already carries a distinct, established meaning through Fulfillment Event (a vendor-performance assessment of whether a shipment met its own order — accuracy, timing, completeness). This associative entity represents a different concept — apportioning shipped quantity across replenishment demand. The attribute itself is renamed for the same reason: `fulfilled\_quantity` → `allocated\_quantity`. All references in the Enterprise Logical Model and Enterprise Relational Foundation have been updated to match.

* **Purpose:** Associative entity resolving Shipment's many-to-many relationship to Replenishment, recording the quantity a given shipment allocates toward a given replenishment request. **\[Governance — Enterprise Logical Model, Associative Entity Resolution]**
* **Object Model Classification:** Not applicable — a logical relationship entity, not a canonical enterprise object. **\[Governance]**
* **Canonical Identifier:** Not applicable — relationship entity. **\[Governance, per the associative-entity exception in Enterprise Relational Foundation]**
* **Foreign Keys:** `shipment\_id` → Shipment.`shipment\_id`; `replenishment\_id` → Replenishment.`replenishment\_id`
* **Dependencies:** Shipment, Replenishment (both Tier 2, both required)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`shipment\_id`|`TEXT`|No (PK, part 1)|\[Governance — Enterprise Logical Model]|
|`replenishment\_id`|`TEXT`|No (PK, part 2)|\[Governance — Enterprise Logical Model]|
|`allocated\_quantity`|`INTEGER`|No|\[Governance — Enterprise Logical Model: "logical requirement, not a physical-schema deferral," now named `allocated\_quantity`.] Its type is an engineering decision — `INTEGER` chosen to match the quantity types already used throughout Shipment and Replenishment. **\[Assumption]**|

* **Business Candidate Key:** (`shipment\_id`, `replenishment\_id`) — assumes one shipment allocates to a given replenishment as a single recorded quantity, not multiple partial allocations over time. This matches the Logical Model's own decision not to add an `allocation\_date` attribute absent business evidence for needing relationship-level timing. **\[Assumption, consistent with a decision already made in the Enterprise Logical Model]**
* **Primary-Key Strategy:** The business candidate key is implemented directly as the composite primary key, per the associative-entity exception in Enterprise Relational Foundation — this row represents the complete current relationship between the pair, so the FK combination is sufficient even though it carries a relationship-level attribute (`allocated\_quantity`). A surrogate would only become necessary if multiple allocation records per pair, temporal history, or an independent lifecycle needed representing.
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: (`shipment\_id`, `replenishment\_id`) must be unique.
  * **Allocation Rules.** The original per-row bound proposed here was incorrect for a many-to-many relationship — individual rows could each pass while their combined total still over-allocates either parent. Replaced with aggregate rules:

    * `allocated\_quantity` must be greater than zero.
    * `SUM(allocated\_quantity)` across all allocations for a given `shipment\_id` must not exceed the quantity that shipment has available to allocate.
    * `SUM(allocated\_quantity)` across all allocations for a given `replenishment\_id` must not exceed the quantity authorized for that replenishment. **Recommendation:** use Replenishment's `approved\_quantity` as this ceiling, once an approval exists, rather than `requested\_quantity` — a request is not yet an authorization.
    * **Explicitly unresolved business decision:** whether allocation is permitted before `approved\_quantity` (Replenishment) or `received\_quantity` (Shipment) is even known. Not decided here — flagged for a business decision before SQL Implementation.
    * Implementation Note: none of these are single-table `CHECK` constraints — all three span multiple rows or multiple tables. Candidates for application-layer validation or aggregate triggers at SQL Implementation, not decided here. **\[Assumption — genuinely new proposals, not derived from governance]**
* **Deferred Logical Constraints:** None beyond the rule above.
* **Migration Considerations:** No current source data — this table has no representation in any existing dataset. Populated only going forward, same treatment as Assignment Ticket in Tier 2.
* **Future Expansion:** None flagged.

\---

# Tier 4

## SLA Event

* **Purpose:** Represents an SLA evaluation event for a vendor shipment. **\[Governance]**
* **Object Model Classification:** Assessment Object
* **Canonical Identifier:** `sla\_event\_id` — `TEXT`, format `SLA-####` **\[Governance — Identifier Governance Review]**
* **Foreign Keys:** `vendor\_id` → Vendor.`vendor\_id`; `shipment\_id` → Shipment.`shipment\_id`; `fulfillment\_event\_id` → Fulfillment Event.`fulfillment\_event\_id`; `related\_ticket\_id` → Ticket.`ticket\_id` (optional)
* **Dependencies:** Vendor (Tier 0); Shipment (Tier 2); Fulfillment Event (Tier 3); Ticket (Tier 1, optional)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`sla\_event\_id`|`TEXT`|No (PK)|\[Governance]|
|`vendor\_id`, `shipment\_id`, `fulfillment\_event\_id`|`TEXT`|No|\[Governance — Enterprise-Shared, FK]|
|`related\_ticket\_id`|`TEXT`|Yes|\[Governance — Enterprise-Shared, FK, optional]. Observed populated in 3 of 6 current rows. **\[Repository, n=6]**|
|`sla\_category`|`TEXT`|No|\[Governance — Domain-Authoritative]. See Logical Constraints.|
|`sla\_status`|`TEXT`|No|\[Governance — Enterprise-Shared]. See Logical Constraints.|
|`sla\_breach\_flag`, `escalation\_required\_flag`, `corrective\_action\_required\_flag`|`BOOLEAN`|No|\[Governance — Enterprise-Shared]|
|`sla\_target\_hours`|`INTEGER`|No|\[Governance — Domain-Authoritative]. Observed: `48`, `72`. **\[Repository, n=6]**|
|`actual\_response\_hours`|`DECIMAL`|No|\[Governance — Domain-Authoritative]. Current values happen to be whole hours (`48`, `72`, `96`), but elapsed response time may contain fractional hours. **\[Repository, n=6; logical type is an engineering decision]**|
|`operational\_impact\_level`|`TEXT`|No|\[Governance — Domain-Authoritative]. Observed: `High`, `Low`, `Moderate`. **\[Repository, n=6]**|
|`review\_date`|`DATE`|No|\[Governance — Domain-Authoritative]|
|`notes`|`TEXT`|Yes|\[Governance — Descriptive-or-Derived, narrative]|

* **Business Candidate Key:** None approved. `sla\_category` is a real, data-grounded attribute, not invented, but its use in a candidate key was already deferred pending a business decision on whether a Shipment may receive one evaluation per category, repeated evaluations, or revised assessments — a decision this Tier does not reopen. **\[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `sla\_event\_id` unique across all records.
  * **SLA Category.** Permitted Values: `Delivery SLA`, `Fulfillment SLA`, `Operational Support SLA`. Repository Evidence: 6/6 rows.
  * **SLA Status.** Permitted Values: `Breached`, `Met`, `Monitoring`. Repository Evidence: 6/6 rows.
  * **Fulfillment Reference Consistency.** The `vendor\_id` and `shipment\_id` recorded on an SLA Event must match the `vendor\_id` and `shipment\_id` of its referenced Fulfillment Event — the three FKs must not be allowed to disagree. Implementation Note: a cross-table integrity rule requiring validation logic or trigger-based enforcement at SQL Implementation. **\[Assumption — required to prevent contradictory governed references, not previously specified]**
* **Deferred Logical Constraints:** No candidate key involving `sla\_category` — see above. **Validation note, not a proposal:** the current 6 rows show 6 distinct `shipment\_id` values, meaning every shipment in this sample has exactly one SLA evaluation — the data simply doesn't yet contain a case that would test whether `(shipment\_id, sla\_category)` could collide. This confirms there's no basis to revisit the earlier deferral, not a reason to approve it.
* **Migration Considerations:** Direct load from `vendor-sla-tracking.csv`; requires Vendor, Shipment, Fulfillment Event (Tiers 0–3) and, where populated, Ticket.
* **Future Expansion:** None flagged.

\---

## Replenishment Shortage Response

**Design decision — settled.** The many-to-many language in the Relational Model ("multiple Replenishments may address one Shortage... one Replenishment may mitigate several related Shortages") establishes relationship cardinality, not quantitative apportionment. Unlike `Shipment Replenishment Allocation`, the Logical Model does not identify a quantity attribute as a logical requirement here, no source data exists to ground one, and Shortage has no demand-quantity attribute (`shortage\_quantity`, `required\_quantity`, or equivalent) against which any applied amount could be validated — Shortage tracks severity and estimated stockout duration, not a quantity to resolve. Adding a quantity attribute now would be false precision: a plausible-sounding number with no defined meaning (ordered? approved? shipped? received? operationally credited?) and no way to bound it. This entity remains a pure associative entity.

* **Purpose:** Associative entity resolving Replenishment's many-to-many relationship to Shortage. **\[Governance — Enterprise Logical Model, Associative Entity Resolution]**
* **Object Model Classification:** Not applicable — a logical relationship entity, not a canonical enterprise object.
* **Canonical Identifier:** Not applicable — relationship entity. **\[Governance, per the associative-entity exception in Enterprise Relational Foundation]**
* **Foreign Keys:** `replenishment\_id` → Replenishment.`replenishment\_id`; `shortage\_id` → Shortage.`shortage\_id`
* **Dependencies:** Replenishment (Tier 2), Shortage (Tier 3) — both required

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`replenishment\_id`|`TEXT`|No (PK, part 1)|\[Governance — Enterprise Logical Model]|
|`shortage\_id`|`TEXT`|No (PK, part 2)|\[Governance — Enterprise Logical Model]|

* **Business Candidate Key:** (`replenishment\_id`, `shortage\_id`).
* **Primary-Key Strategy:** The business candidate key is implemented directly as the composite primary key, per the associative-entity exception in Enterprise Relational Foundation.
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: (`replenishment\_id`, `shortage\_id`) must be unique.
  * **Response Compatibility.** A Replenishment Shortage Response may link records only when Replenishment.`item\_id` equals Shortage.`item\_id` and Replenishment.`location\_id` equals Shortage.`location\_id` — a response should not connect operationally unrelated records. Implementation Note: a cross-table integrity rule requiring validation logic or trigger-based enforcement at SQL Implementation. **\[Assumption — derived from the operational meaning of responding to a shortage, not previously specified]**
* **Deferred Logical Constraints:** None.
* **Migration Considerations:** No current source data — new implementation scope, same treatment as the other three associative entities.
* **Future Expansion:** Quantitative attribution (an `applied\_quantity`-style attribute) may be introduced in the future, but only once the business governs: a measurable shortage demand quantity, the meaning of quantity credited from a replenishment against that demand, and whether multiple response events per pair or temporal history need representing. Not proposed here.

\---

# Next Steps

Tiers 0–4 are locked. Organizational Architecture reconciliation has aligned the upstream Object, Relational, Logical, Identifier, and Foundation artifacts required for Tier 5.

Proceed to Tier 5 derivation only after the reconciled repository ZIP passes the final full-repository validation checkpoint:

* Corrective Action
* Assignment Corrective Action

Tier 5 must use the reconciled Corrective Action definition, including:

* `escalation\_required\_flag`
* `corrective\_action\_closed\_flag`
* organizational `assigned\_owner` text that is not an Employee foreign key
* optional `sla\_event\_id`, `fulfillment\_event\_id`, and `related\_ticket\_id`
* Assignment linkage through Assignment Corrective Action

