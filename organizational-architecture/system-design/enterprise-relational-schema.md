# Enterprise Relational Schema

## Northstar Health Operations

---
**Primary Audience:** Northstar architects, data engineers, subsystem maintainers, and reviewers translating approved logical design into a platform-neutral schema specification

**Writing Layer:** Layer 2 — Operational / Architectural

**Architectural Purpose:** Defines entities, attributes, logical types, keys, nullability, logical constraints, migration considerations, and dependency-tier status for the governed enterprise relational design.

**Document Type:** Engineering Design Document

**Authority Level:** Design Specification

**Status:** Approved — Locked

**Depends On:** Enterprise Logical Model, Enterprise Identifier Governance Review, Cross-System Identifier Dictionary, Enterprise Relational Model, and Enterprise Relational Foundation

---
# Purpose

This document derives a schema specification — entities, attributes, logical types, keys, and logical constraints — from the already-approved Enterprise Logical Model, Cross-System Identifier Dictionary, Enterprise Relational Model, and current repository data. It is not SQL. It is the platform-independent blueprint from which target-platform DDL can be derived, including constraints that are stated as business rules here and translated into SQL syntax during implementation.

No decision in this document is untraceable. Every field, type, key, constraint, and migration decision is grounded in approved governance, repository evidence, or an explicitly labeled engineering assumption:

* **[Governance]** — required by the Enterprise Logical Model, Identifier Dictionary, or Identifier Governance Review. Not open for reinterpretation here.
* **[Repository]** — observed directly in current CSV data (value formats, enumerations, row counts). Informs confidence; flagged with sample size since Northstar's datasets are small.
* **[Assumption]** — a proposed engineering decision not fully determined by governance or data. Flagged as a proposal, open to correction.

---
# Conventions

* **Logical types are platform-neutral** (`INTEGER`, `TEXT`, `DATE`, `TIMESTAMP`, `BOOLEAN`, `DECIMAL`), since platform choice (SQLite vs. PostgreSQL) remains an open decision per Enterprise Relational Foundation. Platform-specific type mapping is deferred to SQL Implementation.
* **Structural ordering follows dependency tiers** (Tier 0–5), as established in Enterprise Relational Foundation's Implementation Order. Tiers are not renamed to Object Model taxonomy labels — dependency order and taxonomy classification diverge starting at Tier 1 (Corrective Action, a Work object, depends on two Assessment-tier entities). Each entity records its taxonomy classification separately, as a labeled field, so that traceability isn't lost — it just doesn't drive structure.
* **Logical constraints are stated as business rules, not SQL syntax.** A permitted-values list and its evidence are recorded; whether it becomes a `CHECK` constraint, an application-layer validation, or something else is an implementation note, not a decision made here.
* **Per-entity template:** Purpose, Object Model Classification, Canonical Identifier, Foreign Keys, **Dependencies**, Business Candidate Keys, Attributes (Logical Type), Logical Constraints, Deferred Logical Constraints, Migration Considerations, Future Expansion.
* **Dependencies** (added starting Tier 1; not retrofitted to Tier 0) identifies the prerequisite entities that must exist before this table can be built. It is independent of the Foreign Keys list — Dependencies reflects only this entity's own foreign keys, not entities that reference it through an associative entity. Tier 0 entities have no Dependencies section since "None" is already implied by Foreign Keys: None at that tier.
* **Terminal-tier ordering exception:** Tier 5 is ordered internally. Corrective Action must be built before Assignment Corrective Action because the associative entity references Corrective Action. This is the only same-tier dependency in the current implementation sequence.

---
# Build Status

|Tier|Entities|Status|
|-|-|-|
|Tier 0|Location, Employee, Vendor|**Locked**|
|Tier 1|Inventory Item, Ticket, Assignment, Coverage Schedule, Workload Record|**Locked**|
|Tier 2|Shipment, Replenishment, Location Inventory, Workforce Escalation, Assignment Ticket|**Locked**|
|Tier 3|Inventory Discrepancy, Shortage, Fulfillment Event, Shipment Replenishment Allocation|**Locked**|
|Tier 4|SLA Event, Replenishment Shortage Response|**Locked**|
|Tier 5|Corrective Action, Assignment Corrective Action|**Locked**|

Tiers 0–5 are locked. This document is the approved platform-neutral schema baseline for SQL implementation planning.

---
# Tier 0 — Foundation

## Location

* **Purpose:** Identifies operational facilities, support centers, hubs, or managed locations referenced throughout the enterprise. **[Governance]**
* **Object Model Classification:** Enterprise Foundation Object
* **Canonical Identifier:** `location_id` — `TEXT`, format `LOC-[LOCATION]-##` **[Governance — Identifier Dictionary]**

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`location_id`|`TEXT`|No (PK)|[Governance]|

* **Foreign Keys:** None (Tier 0).
* **Business Candidate Keys:** None approved. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `location_id` must be unique across all records. Implementation Note: becomes the primary-key constraint at SQL implementation.
* **Deferred Logical Constraints:** None applicable — Location has no other attributes to constrain yet.
* **Migration Considerations:** No dedicated Location dataset currently exists. `location_id` values must be collected as the **distinct set** of location identifiers appearing across Shipment, Replenishment, Shortage, Inventory Discrepancy, Location Inventory, and Ticket data during migration — this table is populated by extraction, not by loading a source file. **[Assumption — no source-of-truth file exists; this is a proposed migration approach, not a governance requirement]**
* **Future Expansion:** The Enterprise Object Model already flags the absence of a dedicated Location registry as a known limitation. This schema intentionally creates only a minimal table (identifier only) rather than inventing descriptive attributes (name, address, type, capacity) with no supporting evidence anywhere in the repository. Adding such attributes is legitimate future scope once the business defines them — not proposed here. **[Assumption, explicitly scoped as minimal]**

---
## Employee

* **Purpose:** Uniquely identifies workforce personnel and their organizational placement. **[Governance]**
* **Object Model Classification:** Enterprise Foundation Object
* **Canonical Identifier:** `employee_id` — `TEXT`, format `EMP-###` **[Governance — Identifier Dictionary]**

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`employee_id`|`TEXT`|No (PK)|[Governance]|
|`employee_name`|`TEXT`|No|[Governance — Domain-Authoritative]. Required for human-readable workforce identity and Ticket owner reconciliation.|
|`department`|`TEXT`|No|[Governance — Domain-Authoritative, pending organizational-semantics reconciliation]|
|`team`|`TEXT`|No|[Governance — same reconciliation caveat]|
|`role`|`TEXT`|No|[Governance — Domain-Authoritative]. Left unconstrained — the 15-row sample shows too many distinct values to treat confidently as a bounded set, unlike `department`/`team`. **[Assumption]**|
|`employment_status`|`TEXT`|No|[Governance — Enterprise-Shared]. See Logical Constraints.|
|`active_flag`|`BOOLEAN`|No|[Governance — Enterprise-Shared]. See Logical Constraints.|
|`primary_shift`|`TEXT`|Yes|[Governance — Descriptive-or-Derived]. Observed: `Day`, `Evening`, `Variable`. **[Repository, n=15]**|
|`standard_weekly_hours`|`INTEGER`|Yes|[Governance — Descriptive-or-Derived]. Observed: `24`, `32`, `40`. **[Repository, n=15]**|
|`skill_area`|`TEXT`|Yes|[Governance — Descriptive-or-Derived]|
|`coverage_priority`|`TEXT`|Yes|[Governance — Descriptive-or-Derived]. Observed: `High`, `Moderate`, `Low`. **[Repository, n=15]**|

* **Foreign Keys:** None (Tier 0).
* **Business Candidate Keys:** None approved. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `employee_id` must be unique across all records. Implementation Note: becomes the primary-key constraint at SQL implementation.
  * **Employment Status.** Permitted Values: `Active`, `Leave`. Repository Evidence: 15/15 rows show only these two values. Implementation Note: may become a SQL `CHECK` constraint after the business confirms this list is exhaustive — 15 rows is not strong enough evidence on its own (e.g., "Terminated" could plausibly exist and simply not appear in the current roster). Until confirmed, an application-layer validation is preferable to a hard database constraint.
  * **Active Flag.** Permitted Values: `TRUE`, `FALSE`. Implementation Note: standard boolean constraint at SQL implementation, not contingent on further evidence.
* **Deferred Logical Constraints:** `department`/`team` are intentionally **not** given a permitted-values list or reference-table constraint here — the Enterprise Logical Model already flagged their enterprise-wide semantics as pending reconciliation. Constraining them now would lock in unreconciled values. **[Governance — carried forward from Enterprise Logical Model]**
* **Migration Considerations:** Direct load from `workforce-roster.csv`; no field renaming required. `employee_name` must be retained because Ticket `assigned_owner` reconciliation depends on matching free-text names to canonical `employee_id` values.
* **Future Expansion:** If Department/Team reconciliation produces governed `department_id`/`team_id` reference tables (already anticipated in the Identifier Dictionary's Entity Expansion Standards), `department` and `team` become foreign keys at that point rather than free text. Not proposed here.

---
## Vendor

* **Purpose:** Uniquely identifies a supplier or vendor. **[Governance]**
* **Object Model Classification:** Enterprise Foundation Object
* **Canonical Identifier:** `vendor_id` — `TEXT`, format `VEND-###` **[Governance — Identifier Dictionary]**

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`vendor_id`|`TEXT`|No (PK)|[Governance]|
|`vendor_type`|`TEXT`|No|[Governance — Domain-Authoritative]. See Logical Constraints.|
|`primary_service_category`|`TEXT`|No|[Governance — Domain-Authoritative]. Observed: `Clinical Equipment`, `Distribution Support`, `Emergency Supplies`, `General Operations`, `Medical Supplies`. **[Repository, n=12]**|
|`risk_tier`|`TEXT`|No|[Governance — Domain-Authoritative]. See Logical Constraints.|
|`active_vendor_flag`|`BOOLEAN`|No|[Governance — Enterprise-Shared]|
|`vendor_name`|`TEXT`|No|[Governance — Domain-Authoritative]|
|`support_level`|`TEXT`|Yes|[Governance — Domain-Authoritative]. Observed: `Core Operational Support`, `Emergency Support`, `Logistics Support`, `Specialty Support`, `Supplemental Support`. **[Repository, n=12]**|
|`preferred_vendor_flag`|`BOOLEAN`|Yes|[Governance — Domain-Authoritative]|
|`emergency_fulfillment_flag`|`BOOLEAN`|Yes|[Governance — Domain-Authoritative]|
|`primary_contact_team`|`TEXT`|Yes|[Governance — Domain-Authoritative]. Observed: `Operations Coordination Center`, `Supply & Inventory Operations`, `Vendor & Service Management`. **[Repository, n=12]**|
|`notes`|`TEXT`|Yes|[Governance — Descriptive-or-Derived]|

* **Foreign Keys:** None (Tier 0).
* **Business Candidate Keys:** None approved. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `vendor_id` must be unique across all records. Implementation Note: becomes the primary-key constraint at SQL implementation.
  * **Vendor Type.** Permitted Values: `Primary Supplier`, `Backup Supplier`, `Emergency Supplier`, `Logistics Partner`, `Specialty Supplier`. Repository Evidence: 12/12 rows. Implementation Note: same provisional caveat as Employment Status — 12 rows is thin evidence for a hard constraint; confirm exhaustiveness with the business first.
  * **Risk Tier.** Permitted Values: `Critical`, `High`, `Moderate`, `Low`. Repository Evidence: 12/12 rows. Implementation Note: same provisional caveat.
  * **Boolean flags** (`active_vendor_flag`, `preferred_vendor_flag`, `emergency_fulfillment_flag`). Permitted Values: `TRUE`, `FALSE`. Implementation Note: standard boolean constraints, not contingent on further evidence.
* **Deferred Logical Constraints:** `primary_service_category` and `support_level` enumerations were observed but are **not** given a permitted-values constraint here — 12 rows is a thinner basis for a category list this granular than for `vendor_type`/`risk_tier`. Recommend application-layer validation rather than a database constraint until the vendor roster grows. **[Assumption]**
* **Migration Considerations:** Direct load from `vendor-master.csv`; no field renaming required.
* **Future Expansion:** None flagged.

---
# Tier 1

## Inventory Item

* **Purpose:** Uniquely identifies an inventory item tracked across the enterprise. **[Governance]**
* **Object Model Classification:** Enterprise Foundation Object
* **Canonical Identifier:** `item_id` — `TEXT`, format `ITEM-####` **[Governance — Identifier Dictionary]**
* **Foreign Keys:** `preferred_vendor_id` → Vendor.`vendor_id` **[Governance — scoped to preferred-sourcing role only; does not implement the full Vendor↔Inventory Item relationship, per Enterprise Logical Model]**
* **Dependencies:** Vendor (Tier 0)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`item_id`|`TEXT`|No (PK)|[Governance]|
|`item_category`|`TEXT`|No|[Governance — Domain-Authoritative]. See Logical Constraints.|
|`criticality_level`|`TEXT`|No|[Governance — Domain-Authoritative]. See Logical Constraints.|
|`unit_of_measure`|`TEXT`|No|[Governance — Domain-Authoritative]. Observed: `box`, `case`, `kit`, `pack`. **[Repository, n=8]**|
|`preferred_vendor_id`|`TEXT`|Yes|[Governance — Enterprise-Shared, FK]|
|`active_flag`|`BOOLEAN`|No|[Governance — Enterprise-Shared]|
|`item_name`|`TEXT`|No|[Governance — Domain-Authoritative]|

* **Business Candidate Keys:** None approved. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `item_id` unique across all records.
  * **Item Category.** Permitted Values: `Clinical Supplies`, `Compliance Supplies`, `PPE`, `Procedure Supplies`, `Wound Care Supplies`. Repository Evidence: 8/8 rows. Implementation Note: same provisional caveat as other small-sample enumerations — confirm exhaustiveness before treating as a hard constraint.
  * **Criticality Level.** Permitted Values: `Critical`, `High`, `Moderate`. Repository Evidence: 8/8 rows. Implementation Note: provisional, same caveat.
  * **Active Flag.** Permitted Values: `TRUE`, `FALSE`. Note: only `TRUE` appears in current 8-row data — the field is still boolean by definition, this is not evidence the value is fixed.
* **Deferred Logical Constraints:** None beyond the provisional caveats above.
* **Migration Considerations:** Direct load from `inventory-items.csv`. `preferred_vendor_id` values must resolve against the Vendor table already loaded (Tier 0) — this is the first tier where load order actually matters for referential integrity, not just convenience.
* **Future Expansion:** None flagged.

---
## Ticket

* **Purpose:** Represents an operational ticket or incident record. **[Governance]**
* **Object Model Classification:** Operational Work Object
* **Canonical Identifier:** `ticket_id` — `TEXT`, format `INC-######` **[Governance — Identifier Dictionary]**
* **Foreign Keys:** `location_id` → Location.`location_id` (planned); `employee_id` → Employee.`employee_id` (planned) — **both currently unenforceable; see Logical Constraints and Migration Considerations.**
* **Dependencies:** Location, Employee (both Tier 0) — **staged**, not enforced at initial creation. See below.

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`ticket_id`|`TEXT`|No (PK)|[Governance]|
|`category`|`TEXT`|No|[Governance — Domain-Authoritative]. See Logical Constraints.|
|`priority`|`TEXT`|No|[Governance — Domain-Authoritative]. See Logical Constraints.|
|`status`|`TEXT`|No|[Governance — Enterprise-Shared]. See Logical Constraints.|
|`escalation_flag`, `reopened_flag`, `pending_flag`|`BOOLEAN`|No|[Governance — `escalation_flag`: Enterprise-Shared; `reopened_flag`/`pending_flag`: Domain-Authoritative]|
|`sla_target_hours`|`INTEGER`|No|[Governance — Domain-Authoritative]. Observed: `4`, `24`, `72`, `120`. **[Repository, n=15]**|
|`sla_met_flag`|`BOOLEAN`|Yes|[Governance — Domain-Authoritative]. Observed: `TRUE`, `FALSE`, and blank. **[Repository, n=15]** — blank corresponds to tickets not yet resolved; nullability is a real business state, not missing data.|
|`requesting_location`|`TEXT`|Yes|[Assumption — legacy migration/source attribute, not a canonical relationship field]. Currently stores descriptive names (e.g., `Cary Distribution Hub 01`), not `location_id` values. **[Repository, n=15]**|
|`location_id`|`TEXT`|Yes, until migrated|[Governance — Enterprise-Shared, FK to Location]. Canonical target column; null until `requesting_location` is reconciled. Whether `requesting_location` is retained, renamed, or removed after reconciliation is a physical-design decision, not made here.|
|`assigned_department`|`TEXT`|No|[Governance — Domain-Authoritative, pending organizational-semantics reconciliation — same caveat as Employee's `department`/`team`]|
|`assigned_owner`|`TEXT`|Yes|[Assumption — legacy migration/source attribute, not a canonical relationship field]. Currently stores employee display names (e.g., `Avery Patel`), not `employee_id` values. **[Repository, n=15]**|
|`employee_id`|`TEXT`|Yes, until migrated|[Governance — Enterprise-Shared, FK to Employee]. Canonical target column; null until `assigned_owner` is reconciled.|
|`created_at`, `first_response_at`, `resolved_at`, `closed_at`|`TIMESTAMP`|`first_response_at`/`resolved_at`/`closed_at` Yes; `created_at` No|[Governance — Domain-Authoritative]|
|`resolution_hours`, `response_hours`|`DECIMAL`|Yes|[Governance — Descriptive-or-Derived, calculated]|
|`summary`, `resolution_notes`|`TEXT`|Yes|[Governance — Descriptive-or-Derived]|

* **Business Candidate Keys:** None approved. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `ticket_id` unique across all records.
  * **Category.** Permitted Values: `Data Quality & Compliance`, `Inventory & Supply`, `Operational Incident`, `Scheduling & Resource Coordination`, `Technical & Systems Support`, `Vendor & Delivery Management`. Repository Evidence: 15/15 rows. Implementation Note: provisional, standard small-sample caveat.
  * **Priority.** Permitted Values: `Priority 1 — Critical`, `Priority 2 — High`, `Priority 3 — Moderate`, `Priority 4 — Low`. Repository Evidence: 15/15 rows.
  * **Status.** Permitted Values: `Assigned`, `Closed`, `In Progress`, `Pending`. Repository Evidence: 15/15 rows.
  * **Location and Owner References.** Implementation Note: **not** enforced as foreign keys at initial table creation. Per the Enterprise Logical Model's documented migration sequence, `requesting_location` and `assigned_owner` are staged as free text first, profiled and mapped against Location and Employee, and only constrained after reconciliation. This is a governance decision already made, carried forward here, not a new one.
* **Deferred Logical Constraints:** `assigned_department` is not given a permitted-values constraint, for the same organizational-semantics reconciliation reason as Employee's `department`/`team`.
* **Migration Considerations:** This is the entity where the Ticket free-text migration sequence applies: profile `requesting_location`/`assigned_owner` values → build mapping rules → migrate resolvable values → review exceptions → enforce FK.

  * All four distinct `requesting_location` values have clear candidate mappings to the four governed `location_id` values, but the mappings must still be formally validated and recorded.
  * Only 3 of 15 current tickets map by exact `assigned_owner` name to `workforce-roster.csv`. The unmatched names are Avery Patel, Marcus Nguyen, Samantha Ortiz, and Taylor Brooks. `employee_id` therefore remains nullable until the roster or source data is reconciled.
  * `tickets-v1.csv` is Windows-1252 encoded while the other current datasets are UTF-8 or UTF-8 with BOM. Migration must normalize encoding before validation and load.
**[Repository, n=15; mapping and encoding normalization are migration prerequisites]**
* **Future Expansion:** None flagged beyond the already-documented FK staging.

---
## Assignment

* **Purpose:** Represents a workforce assignment. **[Governance]**
* **Object Model Classification:** Operational Work Object
* **Canonical Identifier:** `assignment_id` — `TEXT`, format `ASSIGN-###` **[Governance — Identifier Governance Review]**
* **Foreign Keys:** `employee_id` → Employee.`employee_id`
* **Dependencies:** Employee (Tier 0)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`assignment_id`|`TEXT`|No (PK)|[Governance]|
|`employee_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]|
|`assignment_category`|`TEXT`|No|[Governance — Domain-Authoritative]. See Logical Constraints.|
|`assignment_status`|`TEXT`|No|[Governance — Enterprise-Shared]. Observed: `Active`, `Suspended`. **[Repository, n=18]**|
|`start_date`|`DATE`|No|[Governance — Domain-Authoritative]|
|`end_date`|`DATE`|Yes|[Governance — Domain-Authoritative]. Observed: blank in all 18 current rows — no assignment has ended yet in the simulation's current state. **[Repository, n=18]**|
|`assignment_name`|`TEXT`|No|[Governance — Domain-Authoritative]|
|`priority_level`|`TEXT`|No|[Governance — Domain-Authoritative]. Observed: `Critical`, `High`, `Moderate`, `Low`. **[Repository, n=18]**|
|`estimated_hours_per_week`|`INTEGER`|Yes|[Governance — Domain-Authoritative]. Observed: `10`, `15`, `20`, `25`, `30`. **[Repository, n=18]**|
|`cross_functional_flag`|`BOOLEAN`|No|[Governance — Domain-Authoritative]|

* **Business Candidate Keys:** None approved — Assignment carries no work-target reference and its categories are broad and recurring. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `assignment_id` unique across all records.
  * **Assignment Category.** Permitted Values: `Escalation Management`, `Inventory Operations`, `Ticketing`, `Vendor Management`, `Workforce Coordination`. Repository Evidence: 18/18 rows. Implementation Note: provisional.
  * **Assignment Status.** Permitted Values: `Active`, `Suspended`. Repository Evidence: 18/18 rows. Implementation Note: provisional — a status like `Completed` seems plausible given `end_date` exists as a column, but doesn't appear in current data.
* **Deferred Logical Constraints:** None beyond the provisional caveats above.
* **Migration Considerations:** Direct load from `workforce-assignments.csv`; requires Employee (Tier 0) loaded first.
* **Future Expansion:** Once `AssignmentTicket` and `AssignmentCorrectiveAction` (Tier 2 and Tier 5) exist, Assignment's practical work-target relationship becomes visible through those tables — not through any new column on Assignment itself.

---
## Coverage Schedule

* **Purpose:** Represents a workforce coverage schedule record. **[Governance]**
* **Object Model Classification:** Operational State Object
* **Canonical Identifier:** `coverage_schedule_id` — `TEXT`, format `SCHED-###` **[Governance — Identifier Governance Review; rename of legacy field `schedule_id`, documented as a migration alias]**
* **Foreign Keys:** `employee_id` → Employee.`employee_id`
* **Dependencies:** Employee (Tier 0)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`coverage_schedule_id`|`TEXT`|No (PK)|[Governance]|
|`employee_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]|
|`schedule_date`|`DATE`|No|[Governance — Domain-Authoritative]|
|`shift_type`|`TEXT`|No|[Governance — Domain-Authoritative]. Observed: `Day`, `Evening`, `Variable`. **[Repository, n=15]**|
|`coverage_status`|`TEXT`|No|[Governance — Enterprise-Shared]. Observed: `Covered`, `Uncovered`. **[Repository, n=15]**|
|`scheduled_hours`|`INTEGER`|Yes|[Governance — Domain-Authoritative]. Observed: `6`, `8`. **[Repository, n=15]**|
|`coverage_area`|`TEXT`|Yes|[Governance — Domain-Authoritative; descriptive text, not a Location reference]. Observed: `Cross-Team Support`, `Escalation Support`, `Inventory Support`, `Service Response`, `Vendor Operations`. **[Repository, n=15]**|
|`coverage_priority`|`TEXT`|Yes|[Governance — Domain-Authoritative]. Observed: `High`, `Moderate`, `Low`. **[Repository, n=15]**|
|`backup_required_flag`|`BOOLEAN`|Yes|[Governance — Domain-Authoritative]|

* **Business Candidate Keys:** None approved. `location_id` explicitly excluded — Coverage Schedule has no Location relationship in the approved Relational Model, and the underlying data confirms no `location_id` column exists. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `coverage_schedule_id` unique across all records.
  * **Overlapping Coverage.** An Employee should not have incompatible overlapping coverage periods. Implementation Note: this rule is recognized but **structurally deferred** — it cannot currently be evaluated at all, by any mechanism, because Coverage Schedule has no `coverage_start_at`/`coverage_end_at` or governed shift-window definition to compare against. `schedule_date` and `shift_type` alone don't define when a period starts or ends. This is not a choice between enforcement mechanisms (trigger vs. application validation) — no mechanism can evaluate the rule until time boundaries or a controlled Shift definition are governed. Revisit once one of those exists.
  * **Shift Type.** Permitted Values: `Day`, `Evening`, `Variable`. Repository Evidence: 15/15 rows.
  * **Coverage Status.** Permitted Values: `Covered`, `Uncovered`. Repository Evidence: 15/15 rows.
* **Deferred Logical Constraints:** `coverage_area` observed values are not proposed as a hard permitted-values constraint — it's documented as free descriptive text, not a governed reference list, and treating it as an enum risks implying a governance status it doesn't have.
* **Migration Considerations:** Source field `schedule_id` renamed to `coverage_schedule_id`. Legacy alias documentation required per the Identifier Governance Review — the migration script must map old to new, not simply relabel silently.
* **Future Expansion:** None flagged.

---
## Workload Record

* **Purpose:** Represents an employee workload measurement for a reporting period. **[Governance]**
* **Object Model Classification:** Operational State Object
* **Canonical Identifier:** `workload_record_id` — `TEXT`, format `WORK-###` **[Governance — Identifier Governance Review; rename of legacy field `workload_id`, documented as a migration alias]**
* **Foreign Keys:** `employee_id` → Employee.`employee_id`
* **Dependencies:** Employee (Tier 0)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`workload_record_id`|`TEXT`|No (PK)|[Governance]|
|`employee_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]|
|`reporting_period`|`TEXT`|No|[Governance — Enterprise-Shared]. Observed format: `2026-06`. **[Repository, n=15]**|
|`workload_status`|`TEXT`|No|[Governance — Domain-Authoritative]. See Logical Constraints.|
|`assigned_tasks`, `completed_tasks`, `open_tasks`|`INTEGER`|No|[Governance — Domain-Authoritative]|
|`estimated_hours`, `actual_hours`|`DECIMAL`|Yes|[Governance — Domain-Authoritative]|
|`capacity_utilization_percent`|`DECIMAL`|Yes|[Governance — Descriptive-or-Derived, calculated]|

* **Business Candidate Keys:** `employee_id` + `reporting_period` — business-justified: one workload measurement per employee per period. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `workload_record_id` unique across all records.
  * **Business Key.** Uniqueness Rule: (`employee_id`, `reporting_period`) must be unique. Repository Evidence: 15/15 rows show no collision. Implementation Note: this constraint is governance-backed independent of the data check — it should be enforced as a `UNIQUE` constraint at implementation regardless of sample size, unlike the provisional enumerations elsewhere in this document.
  * **Workload Status.** Permitted Values: `Balanced`, `Overloaded`, `Unavailable`, `Underutilized`. Repository Evidence: 15/15 rows. Implementation Note: provisional, standard caveat.
* **Deferred Logical Constraints:** None beyond the provisional caveat above.
* **Migration Considerations:** Source field `workload_id` renamed to `workload_record_id`, same legacy-alias treatment as Coverage Schedule.
* **Future Expansion:** None flagged.

---
# Tier 2

## Shipment

* **Purpose:** Represents a vendor shipment event. **[Governance]**
* **Object Model Classification:** Movement Object
* **Canonical Identifier:** `shipment_id` — `TEXT`, format `SHIP-####` **[Governance — Identifier Dictionary]**
* **Foreign Keys:** `vendor_id` → Vendor.`vendor_id`; `item_id` → Inventory Item.`item_id`; `location_id` → Location.`location_id`; `related_ticket_id` → Ticket.`ticket_id` (optional)
* **Dependencies:** Vendor, Inventory Item, Location (Tier 0–1, all required); Ticket (Tier 1, optional — required only when `related_ticket_id` is populated)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`shipment_id`|`TEXT`|No (PK)|[Governance]|
|`vendor_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]|
|`item_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]. Retains the one-item-per-shipment scope decision — see Deferred Logical Constraints.|
|`location_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]|
|`related_ticket_id`|`TEXT`|Yes|[Governance — Enterprise-Shared, FK, optional]. Observed populated in 3 of 6 current rows. **[Repository, n=6]**|
|`delivery_status`|`TEXT`|No|[Governance — Enterprise-Shared]. See Logical Constraints.|
|`ordered_quantity`|`INTEGER`|No|[Governance — Domain-Authoritative]|
|`received_quantity`|`INTEGER`|Yes|[Governance — Domain-Authoritative]. Blank in current data corresponds to shipments not yet received. **[Repository, n=6]**|
|`order_date`|`DATE`|No|[Governance — Domain-Authoritative]|
|`expected_delivery_date`|`DATE`|No|[Governance — Domain-Authoritative]|
|`actual_delivery_date`|`DATE`|Yes|[Governance — Domain-Authoritative]. Blank corresponds to shipments not yet delivered. **[Repository, n=6]**|
|`fulfillment_accuracy_flag`|`BOOLEAN`|Yes|[Governance — Descriptive-or-Derived, computed]. Blank where accuracy can't yet be assessed (shipment not received). **[Repository, n=6]**|
|`delay_flag`|`BOOLEAN`|No|[Governance — Descriptive-or-Derived, computed]|

* **Business Candidate Keys:** None approved. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `shipment_id` unique across all records.
  * **Delivery Status.** Permitted Values: `Delayed`, `Partial`, `Pending`, `Received`. Repository Evidence: 6/6 rows. Implementation Note: provisional — 6 rows is a thin sample even by this document's own standard; treat this enumeration as more tentative than Tier 0/1's constraints.
* **Deferred Logical Constraints:** `item_id` remains single-valued per shipment. Verified against current data: 0 of 6 `shipment_id` values carry more than one `item_id`. This is the same scope decision already recorded in the Enterprise Logical Model — restated here rather than re-derived, since the underlying evidence hasn't changed. A `Shipment Line` associative entity remains not introduced.
* **Migration Considerations:** Direct load from `vendor-shipments.csv`, requires Vendor, Inventory Item, Location (all loaded) and, where populated, Ticket.
* **Future Expansion:** None flagged.

---
## Replenishment

* **Purpose:** Represents a replenishment workflow event. **[Governance]**
* **Object Model Classification:** Movement Object
* **Canonical Identifier:** `replenishment_id` — `TEXT`, format `REPL-####` **[Governance — Identifier Dictionary]**
* **Foreign Keys:** `item_id` → Inventory Item.`item_id`; `location_id` → Location.`location_id`; `vendor_id` → Vendor.`vendor_id` (optional); `related_ticket_id` → Ticket.`ticket_id` (optional)
* **Dependencies:** Inventory Item, Location (Tier 0–1, required); Vendor (Tier 0, optional); Ticket (Tier 1, optional)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`replenishment_id`|`TEXT`|No (PK)|[Governance]|
|`item_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]|
|`location_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]|
|`vendor_id`|`TEXT`|Conditional|[Governance — Enterprise-Shared FK; conditional nullability is a repository-supported engineering decision, not prior governance, n=5]|
|`related_ticket_id`|`TEXT`|Yes|[Governance — Enterprise-Shared, FK, optional]|
|`replenishment_type`|`TEXT`|No|[Governance — Domain-Authoritative]. See Logical Constraints.|
|`replenishment_status`|`TEXT`|No|[Governance — Enterprise-Shared]. See Logical Constraints.|
|`requested_quantity`|`INTEGER`|No|[Governance — Domain-Authoritative]|
|`approved_quantity`|`INTEGER`|Yes|[Governance — Domain-Authoritative]|
|`request_date`|`DATE`|No|[Governance — Domain-Authoritative]|
|`expected_arrival_date`|`DATE`|Yes|[Governance — Domain-Authoritative]|
|`received_date`|`DATE`|Yes|[Governance — Domain-Authoritative]|

* **Business Candidate Keys:** None approved. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `replenishment_id` unique across all records.
  * **Replenishment Type.** Permitted Values: `Internal Transfer`, `Vendor Reorder`. Repository Evidence: 5/5 rows.
  * **Replenishment Status.** Permitted Values: `Approved`, `Delayed`, `In Transit`, `Received`. Repository Evidence: 5/5 rows. Implementation Note: 5 rows is a very thin sample; treat as more tentative than any prior tier.
  * **Vendor Presence Rule.** Proposed rule: `vendor_id` is null for `Internal Transfer` and required for `Vendor Reorder`. This rule is supported by the meaning of the two replenishment types and by all five current records, but it was not previously established by governance. Confirm with the business before enforcing it as a hard database constraint. Implementation Note: not expressible as a simple `NOT NULL` regardless — a cross-field conditional rule, candidate for application-layer validation or a two-column `CHECK` at SQL Implementation.
* **Deferred Logical Constraints:** None beyond the caveats above.
* **Migration Considerations:** Direct load from `replenishment-events.csv`; requires Inventory Item, Location, and — where populated — Vendor and Ticket.
* **Future Expansion:** None flagged.

---
## Location Inventory

* **Purpose:** Represents the current stock position of one inventory item at one location. **[Governance]**
* **Object Model Classification:** Operational State Object
* **Canonical Identifier:** `location_inventory_id` — `TEXT`, format `LOCINV-####` **[Governance — Identifier Governance Review; already the governed physical field name, elevated to canonical cross-system status]**
* **Foreign Keys:** `item_id` → Inventory Item.`item_id`; `location_id` → Location.`location_id`
* **Dependencies:** Inventory Item, Location (Tier 0–1)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`location_inventory_id`|`TEXT`|No (PK)|[Governance]|
|`item_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]|
|`location_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]|
|`current_stock`|`INTEGER`|No|[Governance — Enterprise-Shared]|
|`stock_status`|`TEXT`|No|[Governance — Enterprise-Shared]. See Logical Constraints.|
|`reorder_point`|`INTEGER`|Yes|[Governance — Domain-Authoritative]|
|`target_stock_level`|`INTEGER`|Yes|[Governance — Domain-Authoritative]|
|`safety_stock_level`|`INTEGER`|Yes|[Governance — Domain-Authoritative]|
|`last_count_date`|`DATE`|Yes|[Governance — Domain-Authoritative]|

* **Business Candidate Keys:** `location_id` + `item_id` — business-justified: the enterprise recognizes exactly one active stock position per item per location. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `location_inventory_id` unique across all records.
  * **Business Key.** Uniqueness Rule: (`location_id`, `item_id`) must be unique. Implementation Note: governance-backed independent of sample size, same treatment as Workload Record's business key in Tier 1 — enforce as a `UNIQUE` constraint regardless of the current 8-row sample.
  * **Stock Status.** Permitted Values: `Critical Low`, `Low Stock`, `Normal`, `Overstocked`, `Stockout`. Repository Evidence: 8/8 rows. Implementation Note: provisional, standard caveat.
* **Deferred Logical Constraints:** None beyond the caveat above.
* **Migration Considerations:** Direct load from `location-inventory.csv`; requires Inventory Item and Location loaded first.
* **Future Expansion:** None flagged. The deferred Shipment→Location Inventory analytical/historical relationship (transaction history) remains explicitly out of scope, per Enterprise Relational Foundation.

---
## Workforce Escalation

* **Purpose:** Represents a workforce escalation record. **[Governance]**
* **Object Model Classification:** Assessment Object
* **Canonical Identifier:** `escalation_id` — `TEXT`, format `WF-ESC-###` **[Governance — Identifier Governance Review; no rename — attribute name already matched current data]**
* **Foreign Keys:** `related_ticket_id` → Ticket.`ticket_id` (optional) — **new column, not present in current data; see Migration Considerations**
* **Dependencies:** Ticket (Tier 1, optional — only once `related_ticket_id` is added)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`escalation_id`|`TEXT`|No (PK)|[Governance]|
|`related_ticket_id`|`TEXT`|Yes|[Governance — Enterprise-Shared, FK, optional]. **Does not exist in current repository data** — this column is new implementation scope, not a migrated field. **[Governance — Enterprise Logical Model, Relationships Implemented Through an Existing Object]**|
|`department`|`TEXT`|No|[Governance — Domain-Authoritative, organizational semantics pending reconciliation]. Observed: `Operations`, `Vendor Management`. **[Repository, n=10]**|
|`escalation_type`|`TEXT`|No|[Governance — Domain-Authoritative]. See Logical Constraints.|
|`severity_level`|`TEXT`|No|[Governance — Domain-Authoritative]. Observed: `Critical`, `High`, `Low`, `Moderate`. **[Repository, n=10]**|
|`current_status`|`TEXT`|No|[Governance — Enterprise-Shared]. See Logical Constraints.|
|`escalation_date`|`DATE`|No|[Governance — Domain-Authoritative]|
|`affected_team`|`TEXT`|Yes|[Governance — Domain-Authoritative, organizational semantics pending reconciliation]. Observed: `Coverage Support`, `Escalation Support`, `Inventory Support`, `Service Response`, `Vendor Operations`. **[Repository, n=10]**|
|`root_cause`|`TEXT`|Yes|[Governance — Domain-Authoritative]. 10 distinct values across 10 rows — effectively free text at current volume, not proposed as an enumeration. **[Repository, n=10]**|
|`resolution_owner`|`TEXT`|Yes|[Governance — Domain-Authoritative]. Observed: `Inventory Manager`, `Operations Manager`, `Vendor Manager`, `Workforce Coordinator` — role titles, not `employee_id` values; no employee-level FK exists for this entity yet, per Enterprise Logical Model. **[Repository, n=10]**|
|`business_impact`|`TEXT`|Yes|[Governance — Descriptive-or-Derived, narrative]|

* **Business Candidate Keys:** None approved. The architecture explicitly allows escalations not tied to one employee. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `escalation_id` unique across all records.
  * **Escalation Type.** Permitted Values: `Capacity Constraint`, `Coverage Gap`, `Cross-Team Support Request`, `Escalation Queue Backlog`, `Staffing Shortage`, `Workload Imbalance`. Repository Evidence: 10/10 rows.
  * **Current Status.** Permitted Values: `In Progress`, `Monitoring`, `Open`, `Resolved`. Repository Evidence: 10/10 rows.
* **Deferred Logical Constraints:** `root_cause` and `resolution_owner` are not proposed as enumerations — `root_cause` shows no repetition at all in the current sample (10 distinct values in 10 rows), and `resolution_owner` looks role-based rather than a governed reference list.
* **Migration Considerations:** Direct load from `workforce-escalations.csv`, with `related_ticket_id` added as a new nullable column with no source data to populate it initially — it starts empty and is populated going forward, not backfilled from history that doesn't exist.
* **Future Expansion:** `employee_id` remains unrepresented per the Enterprise Logical Model's deferred Workforce Escalation↔Employee relationship. Not added here.

---
## Assignment Ticket

* **Purpose:** Associative entity resolving Assignment's many-to-many relationship to Ticket, one of two typed relationship entities replacing a rejected polymorphic design. **[Governance — Enterprise Logical Model, Associative Entity Resolution]**
* **Object Model Classification:** Not applicable — a logical relationship entity, not a canonical enterprise object. **[Governance]**
* **Canonical Identifier:** Not applicable — this is a relationship entity, not a canonical enterprise object. **[Governance]**
* **Foreign Keys:** `assignment_id` → Assignment.`assignment_id`; `ticket_id` → Ticket.`ticket_id`
* **Dependencies:** Assignment, Ticket (both Tier 1, both required)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`assignment_id`|`TEXT`|No (PK, part 1)|[Governance — Enterprise Logical Model]|
|`ticket_id`|`TEXT`|No (PK, part 2)|[Governance — Enterprise Logical Model]|

* **Business Candidate Key:** (`assignment_id`, `ticket_id`) — the minimal business-meaningful combination that uniquely identifies the relationship.
* **Primary-Key Strategy:** The business candidate key is implemented directly as the composite primary key; no surrogate identifier is introduced, since this associative entity has no independent lifecycle or relationship-level attributes beyond the pairing itself. **[Governance — see the associative-entity exception now recorded in Enterprise Relational Foundation's Key Strategy]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: (`assignment_id`, `ticket_id`) must be unique — no duplicate pairing.
* **Deferred Logical Constraints:** None.
* **Migration Considerations:** No current source data — this table has no representation in `workforce-assignments.csv` today. Populated only going forward, once Assignment-to-Ticket linkage is actively tracked. This is new implementation scope, not a migration.
* **Future Expansion:** None flagged.

---
# Tier 3

## Inventory Discrepancy

* **Purpose:** Represents a discrepancy between expected and counted inventory. **[Governance]**
* **Object Model Classification:** Operational State Object
* **Canonical Identifier:** `discrepancy_id` — `TEXT`, format `DISC-####` **[Governance — Identifier Dictionary]**
* **Foreign Keys:** `item_id` → Inventory Item.`item_id`; `location_id` → Location.`location_id`; `related_ticket_id` → Ticket.`ticket_id` (optional)
* **Dependencies:** Inventory Item, Location (Tier 0–1, required); Ticket (Tier 1, optional)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`discrepancy_id`|`TEXT`|No (PK)|[Governance]|
|`item_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]|
|`location_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]|
|`related_ticket_id`|`TEXT`|Yes|[Governance — Enterprise-Shared, FK, optional]. Observed populated in 4 of 5 current rows. **[Repository, n=5]**|
|`investigation_status`|`TEXT`|No|[Governance — Enterprise-Shared]. See Logical Constraints.|
|`expected_quantity`, `counted_quantity`|`INTEGER`|No|[Governance — Domain-Authoritative]|
|`variance_quantity`|`INTEGER` (signed)|No|[Governance — Domain-Authoritative]. **Repository-supported type detail:** observed values include negatives (e.g., `-15`) alongside positives (`20`) — this is a signed quantity (counted minus expected), not an unsigned count. **[Repository, n=5]**|
|`discrepancy_type`|`TEXT`|No|[Governance — Domain-Authoritative]. See Logical Constraints.|
|`discovered_date`|`DATE`|No|[Governance — Domain-Authoritative]|
|`resolved_date`|`DATE`|Yes|[Governance — Domain-Authoritative]. Blank corresponds to unresolved records. **[Repository, n=5]**|

* **Business Candidate Keys:** None approved. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `discrepancy_id` unique across all records.
  * **Discrepancy Type.** Permitted Values: `Count Variance`, `Damaged Inventory`, `Missing Inventory`, `Receiving Error`, `System Entry Error`. Repository Evidence: 5/5 rows. Implementation Note: provisional, thin-sample caveat applies (5 rows).
  * **Investigation Status.** Permitted Values: `Escalated`, `Investigating`, `Mitigating`, `Open`, `Resolved`. Repository Evidence: 5/5 rows.
  * **Variance Calculation Rule.** `variance_quantity = counted_quantity - expected_quantity`. Repository Evidence: verified against all 5 current rows individually, exact match in every case (e.g., `DISC-1003`: `160 - 140 = 20`, matches recorded variance). Implementation Note: whether this becomes a generated/computed column, a stored value with validation, or a migration-time derivation is a SQL Implementation decision, not made here.
* **Deferred Logical Constraints:** None beyond the caveats above.
* **Migration Considerations:** Direct load from `inventory-discrepancies.csv`; requires Inventory Item, Location and, where populated, Ticket. Current references to `INC-100018` and `INC-100031` do not resolve in `tickets-v1.csv`; strict Ticket FK enforcement must wait until those records are added, corrected, or explicitly retired.
* **Future Expansion:** None flagged.

---
## Shortage

* **Purpose:** Represents a detected inventory shortage. **[Governance]**
* **Object Model Classification:** Operational State Object
* **Canonical Identifier:** `shortage_id` — `TEXT`, format `SHORT-####` **[Governance — Identifier Dictionary]**
* **Foreign Keys:** `item_id` → Inventory Item.`item_id`; `location_id` → Location.`location_id`; `related_ticket_id` → Ticket.`ticket_id` (optional)
* **Dependencies:** Inventory Item, Location (Tier 0–1, required); Ticket (Tier 1, optional)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`shortage_id`|`TEXT`|No (PK)|[Governance]|
|`item_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]|
|`location_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]|
|`related_ticket_id`|`TEXT`|Yes|[Governance — Enterprise-Shared, FK, optional]. Observed populated in 3 of 5 current rows. **[Repository, n=5]**|
|`shortage_severity`|`TEXT`|No|[Governance — Enterprise-Shared]. See Logical Constraints.|
|`resolution_status`|`TEXT`|No|[Governance — Enterprise-Shared]. See Logical Constraints.|
|`escalation_flag`|`BOOLEAN`|No|[Governance — Enterprise-Shared]|
|`shortage_detected_date`|`DATE`|No|[Governance — Domain-Authoritative]|
|`estimated_days_of_stockout`|`INTEGER`|Yes|[Governance — Domain-Authoritative]. Observed range 1–4 in current data — a quantity, not a category; no enumeration proposed. **[Repository, n=5]**|
|`operational_impact`|`TEXT`|Yes|[Governance — Domain-Authoritative *as tagged in the Enterprise Logical Model*]. **Repository observation worth flagging:** all 5 current values are distinct, full narrative sentences (e.g., "Gauze inventory temporarily below recommended safety threshold"), not structured category values. This reads closer to Descriptive-or-Derived than Domain-Authoritative in practice — noted as a tension between the Logical Model's tag and what the data actually looks like, not resolved here. Type and nullability are unaffected either way (unconstrained `TEXT`); the tag affects how the physical schema phase should treat it (e.g., whether it's a candidate for future structuring into fields, vs. permanently narrative). **[Repository, n=5]**|

* **Business Candidate Keys:** None approved. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `shortage_id` unique across all records.
  * **Shortage Severity.** Permitted Values: `Critical`, `High`, `Low`, `Moderate`. Repository Evidence: 5/5 rows.
  * **Resolution Status.** Permitted Values: `Escalated`, `Mitigating`, `Monitoring`, `Open`, `Resolved`. Repository Evidence: 5/5 rows.
* **Deferred Logical Constraints:** `operational_impact` is not given a permitted-values constraint — see the provenance note above; it's narrative, not categorical, in the current data.
* **Migration Considerations:** Direct load from `shortage-events.csv`; requires Inventory Item, Location and, where populated, Ticket. Current reference `INC-100021` does not resolve in `tickets-v1.csv`; strict Ticket FK enforcement must wait until that record is added, corrected, or explicitly retired.
* **Future Expansion:** None flagged.

---
## Fulfillment Event

* **Purpose:** Represents a vendor fulfillment assessment for a shipment. **[Governance]**
* **Object Model Classification:** Assessment Object
* **Canonical Identifier:** `fulfillment_event_id` — `TEXT`, format `VF-####` **[Governance — Identifier Governance Review]**
* **Foreign Keys:** `vendor_id` → Vendor.`vendor_id`; `shipment_id` → Shipment.`shipment_id`; `item_id` → Inventory Item.`item_id`; `location_id` → Location.`location_id`; `related_ticket_id` → Ticket.`ticket_id` (optional)
* **Dependencies:** Vendor, Inventory Item, Location (Tier 0–1, required); Shipment (Tier 2, required); Ticket (Tier 1, optional)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`fulfillment_event_id`|`TEXT`|No (PK)|[Governance]|
|`vendor_id`, `shipment_id`, `item_id`, `location_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]|
|`related_ticket_id`|`TEXT`|Yes|[Governance — Enterprise-Shared, FK, optional]. Observed populated in 3 of 6 current rows. **[Repository, n=6]**|
|`fulfillment_status`|`TEXT`|No|[Governance — Enterprise-Shared]. See Logical Constraints.|
|`delivery_status`|`TEXT`|No|[Governance — Enterprise-Shared]. See Logical Constraints — **flagged discrepancy with Shipment.delivery_status below.**|
|`order_date`, `expected_delivery_date`|`DATE`|No|[Governance — Domain-Authoritative]|
|`actual_delivery_date`|`DATE`|Yes|[Governance — Domain-Authoritative]. Blank for undelivered shipments. **[Repository, n=6]**|
|`expected_quantity`|`INTEGER`|No|[Governance — Domain-Authoritative]|
|`received_quantity`|`INTEGER`|No|[Governance — Domain-Authoritative]. Note: `0` appears as a real value (not blank) for at least one pending shipment — distinct from Shipment's own `received_quantity`, which uses blank for the same state. **[Repository, n=6]**|
|`fulfillment_accuracy_flag`, `delay_flag`, `partial_fulfillment_flag`, `emergency_fulfillment_flag`, `escalation_required_flag`|`BOOLEAN`|No|[Governance — Descriptive-or-Derived for accuracy/delay/partial flags (computed); Enterprise-Shared for `escalation_required_flag`]|
|`delay_days`|`INTEGER`|No|[Governance — Descriptive-or-Derived, computed]|
|`operational_impact_level`|`TEXT`|No|[Governance — Domain-Authoritative]. See Logical Constraints.|
|`notes`|`TEXT`|Yes|[Governance — Descriptive-or-Derived, narrative]|

* **Business Candidate Keys:** None approved. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `fulfillment_event_id` unique across all records.
  * **Fulfillment Status.** Permitted Values: `Complete`, `Partial`, `Pending`. Repository Evidence: 6/6 rows.
  * **Delivery Status.** Permitted Values observed here: `Delayed`, `Delivered`, `Pending`. Repository Evidence: 6/6 rows.
  * **Operational Impact Level.** Permitted Values: `High`, `Low`, `Moderate`. Repository Evidence: 6/6 rows.
  * **Emergency Fulfillment Flag.** Only `FALSE` observed in all 6 current rows. Note: still modeled as boolean, not as a fixed value — this reflects the current scenario data, not a business rule that the flag can never be true.
  * **Shipment Reference Consistency.** The `vendor_id`, `item_id`, and `location_id` recorded on a Fulfillment Event must match the corresponding references on its `shipment_id`. Implementation Note: this is a cross-table integrity rule requiring validation logic or trigger-based enforcement at SQL Implementation. **[Assumption — required to prevent contradictory governed references]**
* **Deferred Logical Constraints:** Shipment and Fulfillment Event also repeat dates, quantities, and delivery-state information. Those fields are not forced to match until SQL Implementation defines the authoritative source and translation rules for pending, partial, received, and delivered states.
* **Open Question — `delivery_status` vocabulary mismatch:** Shipment's `delivery_status` (Tier 2) observed values are `Delayed`, `Partial`, `Pending`, `Received`. Fulfillment Event's `delivery_status` observed values are `Delayed`, `Delivered`, `Pending` — no `Partial` or `Received`, but a `Delivered` value Shipment never uses, despite both entities sharing the same `shipment_id` for overlapping records. This could be two legitimately different vocabularies for two different questions (Shipment's own delivery state vs. the vendor-assessment view of it), or an unreconciled inconsistency between two datasets describing the same underlying event. Not resolved here — flagged for a decision before SQL Implementation, since it affects whether these should be two independent CHECK enumerations or a single shared one.
* **Migration Considerations:** Direct load from `vendor-fulfillment-events.csv`; requires Vendor, Inventory Item, Location (Tier 0–1) and Shipment (Tier 2) loaded first — this is the first Tier 3 entity with a Tier 2 dependency, consistent with its position in the build order.
* **Future Expansion:** None flagged.

---
## Shipment Replenishment Allocation

**Naming note — approved.** Originally specified in the Enterprise Logical Model as `Shipment Replenishment Fulfillment`. Renamed to `Shipment Replenishment Allocation`, per approval: its defining attribute is a portion of a Shipment's quantity allocated toward satisfying a specific Replenishment request. "Fulfillment" in this repository already carries a distinct, established meaning through Fulfillment Event (a vendor-performance assessment of whether a shipment met its own order — accuracy, timing, completeness). This associative entity represents a different concept — apportioning shipped quantity across replenishment demand. The attribute itself is renamed for the same reason: `fulfilled_quantity` → `allocated_quantity`. All references in the Enterprise Logical Model and Enterprise Relational Foundation have been updated to match.

* **Purpose:** Associative entity resolving Shipment's many-to-many relationship to Replenishment, recording the quantity a given shipment allocates toward a given replenishment request. **[Governance — Enterprise Logical Model, Associative Entity Resolution]**
* **Object Model Classification:** Not applicable — a logical relationship entity, not a canonical enterprise object. **[Governance]**
* **Canonical Identifier:** Not applicable — relationship entity. **[Governance, per the associative-entity exception in Enterprise Relational Foundation]**
* **Foreign Keys:** `shipment_id` → Shipment.`shipment_id`; `replenishment_id` → Replenishment.`replenishment_id`
* **Dependencies:** Shipment, Replenishment (both Tier 2, both required)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`shipment_id`|`TEXT`|No (PK, part 1)|[Governance — Enterprise Logical Model]|
|`replenishment_id`|`TEXT`|No (PK, part 2)|[Governance — Enterprise Logical Model]|
|`allocated_quantity`|`INTEGER`|No|[Governance — Enterprise Logical Model: "logical requirement, not a physical-schema deferral," now named `allocated_quantity`.] Its type is an engineering decision — `INTEGER` chosen to match the quantity types already used throughout Shipment and Replenishment. **[Assumption]**|

* **Business Candidate Key:** (`shipment_id`, `replenishment_id`) — assumes one shipment allocates to a given replenishment as a single recorded quantity, not multiple partial allocations over time. This matches the Logical Model's own decision not to add an `allocation_date` attribute absent business evidence for needing relationship-level timing. **[Assumption, consistent with a decision already made in the Enterprise Logical Model]**
* **Primary-Key Strategy:** The business candidate key is implemented directly as the composite primary key, per the associative-entity exception in Enterprise Relational Foundation — this row represents the complete current relationship between the pair, so the FK combination is sufficient even though it carries a relationship-level attribute (`allocated_quantity`). A surrogate would only become necessary if multiple allocation records per pair, temporal history, or an independent lifecycle needed representing.
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: (`shipment_id`, `replenishment_id`) must be unique.
  * **Allocation Rules.** The original per-row bound proposed here was incorrect for a many-to-many relationship — individual rows could each pass while their combined total still over-allocates either parent. Replaced with aggregate rules:

    * `allocated_quantity` must be greater than zero.
    * `SUM(allocated_quantity)` across all allocations for a given `shipment_id` must not exceed the quantity that shipment has available to allocate.
    * `SUM(allocated_quantity)` across all allocations for a given `replenishment_id` must not exceed the quantity authorized for that replenishment. **Recommendation:** use Replenishment's `approved_quantity` as this ceiling, once an approval exists, rather than `requested_quantity` — a request is not yet an authorization.
    * **Explicitly unresolved business decision:** whether allocation is permitted before `approved_quantity` (Replenishment) or `received_quantity` (Shipment) is even known. Not decided here — flagged for a business decision before SQL Implementation.
    * Implementation Note: none of these are single-table `CHECK` constraints — all three span multiple rows or multiple tables. Candidates for application-layer validation or aggregate triggers at SQL Implementation, not decided here. **[Assumption — genuinely new proposals, not derived from governance]**
* **Deferred Logical Constraints:** None beyond the rule above.
* **Migration Considerations:** No current source data — this table has no representation in any existing dataset. Populated only going forward, same treatment as Assignment Ticket in Tier 2.
* **Future Expansion:** None flagged.

---
# Tier 4

## SLA Event

* **Purpose:** Represents an SLA evaluation event for a vendor shipment. **[Governance]**
* **Object Model Classification:** Assessment Object
* **Canonical Identifier:** `sla_event_id` — `TEXT`, format `SLA-####` **[Governance — Identifier Governance Review]**
* **Foreign Keys:** `vendor_id` → Vendor.`vendor_id`; `shipment_id` → Shipment.`shipment_id`; `fulfillment_event_id` → Fulfillment Event.`fulfillment_event_id`; `related_ticket_id` → Ticket.`ticket_id` (optional)
* **Dependencies:** Vendor (Tier 0); Shipment (Tier 2); Fulfillment Event (Tier 3); Ticket (Tier 1, optional)

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`sla_event_id`|`TEXT`|No (PK)|[Governance]|
|`vendor_id`, `shipment_id`, `fulfillment_event_id`|`TEXT`|No|[Governance — Enterprise-Shared, FK]|
|`related_ticket_id`|`TEXT`|Yes|[Governance — Enterprise-Shared, FK, optional]. Observed populated in 3 of 6 current rows. **[Repository, n=6]**|
|`sla_category`|`TEXT`|No|[Governance — Domain-Authoritative]. See Logical Constraints.|
|`sla_status`|`TEXT`|No|[Governance — Enterprise-Shared]. See Logical Constraints.|
|`sla_breach_flag`, `escalation_required_flag`, `corrective_action_required_flag`|`BOOLEAN`|No|[Governance — Enterprise-Shared]|
|`sla_target_hours`|`INTEGER`|No|[Governance — Domain-Authoritative]. Observed: `48`, `72`. **[Repository, n=6]**|
|`actual_response_hours`|`DECIMAL`|No|[Governance — Domain-Authoritative]. Current values happen to be whole hours (`48`, `72`, `96`), but elapsed response time may contain fractional hours. **[Repository, n=6; logical type is an engineering decision]**|
|`operational_impact_level`|`TEXT`|No|[Governance — Domain-Authoritative]. Observed: `High`, `Low`, `Moderate`. **[Repository, n=6]**|
|`review_date`|`DATE`|No|[Governance — Domain-Authoritative]|
|`notes`|`TEXT`|Yes|[Governance — Descriptive-or-Derived, narrative]|

* **Business Candidate Key:** None approved. `sla_category` is a real, data-grounded attribute, not invented, but its use in a candidate key was already deferred pending a business decision on whether a Shipment may receive one evaluation per category, repeated evaluations, or revised assessments — a decision this Tier does not reopen. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `sla_event_id` unique across all records.
  * **SLA Category.** Permitted Values: `Delivery SLA`, `Fulfillment SLA`, `Operational Support SLA`. Repository Evidence: 6/6 rows.
  * **SLA Status.** Permitted Values: `Breached`, `Met`, `Monitoring`. Repository Evidence: 6/6 rows.
  * **Fulfillment Reference Consistency.** The `vendor_id` and `shipment_id` recorded on an SLA Event must match the `vendor_id` and `shipment_id` of its referenced Fulfillment Event — the three FKs must not be allowed to disagree. Implementation Note: a cross-table integrity rule requiring validation logic or trigger-based enforcement at SQL Implementation. **[Assumption — required to prevent contradictory governed references, not previously specified]**
* **Deferred Logical Constraints:** No candidate key involving `sla_category` — see above. **Validation note, not a proposal:** the current 6 rows show 6 distinct `shipment_id` values, meaning every shipment in this sample has exactly one SLA evaluation — the data simply doesn't yet contain a case that would test whether `(shipment_id, sla_category)` could collide. This confirms there's no basis to revisit the earlier deferral, not a reason to approve it.
* **Migration Considerations:** Direct load from `vendor-sla-tracking.csv`; requires Vendor, Shipment, Fulfillment Event (Tiers 0–3) and, where populated, Ticket.
* **Future Expansion:** None flagged.

---
## Replenishment Shortage Response

**Design decision — settled.** The many-to-many language in the Relational Model ("multiple Replenishments may address one Shortage... one Replenishment may mitigate several related Shortages") establishes relationship cardinality, not quantitative apportionment. Unlike `Shipment Replenishment Allocation`, the Logical Model does not identify a quantity attribute as a logical requirement here, no source data exists to ground one, and Shortage has no demand-quantity attribute (`shortage_quantity`, `required_quantity`, or equivalent) against which any applied amount could be validated — Shortage tracks severity and estimated stockout duration, not a quantity to resolve. Adding a quantity attribute now would be false precision: a plausible-sounding number with no defined meaning (ordered? approved? shipped? received? operationally credited?) and no way to bound it. This entity remains a pure associative entity.

* **Purpose:** Associative entity resolving Replenishment's many-to-many relationship to Shortage. **[Governance — Enterprise Logical Model, Associative Entity Resolution]**
* **Object Model Classification:** Not applicable — a logical relationship entity, not a canonical enterprise object.
* **Canonical Identifier:** Not applicable — relationship entity. **[Governance, per the associative-entity exception in Enterprise Relational Foundation]**
* **Foreign Keys:** `replenishment_id` → Replenishment.`replenishment_id`; `shortage_id` → Shortage.`shortage_id`
* **Dependencies:** Replenishment (Tier 2), Shortage (Tier 3) — both required

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`replenishment_id`|`TEXT`|No (PK, part 1)|[Governance — Enterprise Logical Model]|
|`shortage_id`|`TEXT`|No (PK, part 2)|[Governance — Enterprise Logical Model]|

* **Business Candidate Key:** (`replenishment_id`, `shortage_id`).
* **Primary-Key Strategy:** The business candidate key is implemented directly as the composite primary key, per the associative-entity exception in Enterprise Relational Foundation.
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: (`replenishment_id`, `shortage_id`) must be unique.
  * **Response Compatibility.** A Replenishment Shortage Response may link records only when Replenishment.`item_id` equals Shortage.`item_id` and Replenishment.`location_id` equals Shortage.`location_id` — a response should not connect operationally unrelated records. Implementation Note: a cross-table integrity rule requiring validation logic or trigger-based enforcement at SQL Implementation. **[Assumption — derived from the operational meaning of responding to a shortage, not previously specified]**
* **Deferred Logical Constraints:** None.
* **Migration Considerations:** No current source data — new implementation scope, same treatment as the other three associative entities.
* **Future Expansion:** Quantitative attribution (an `applied_quantity`-style attribute) may be introduced in the future, but only once the business governs: a measurable shortage demand quantity, the meaning of quantity credited from a replenishment against that demand, and whether multiple response events per pair or temporal history need representing. Not proposed here.

---

# Tier 5

## Corrective Action

* **Purpose:** Represents a vendor corrective action opened in response to SLA breaches, fulfillment failures, or direct vendor issues. **[Governance]**
* **Object Model Classification:** Operational Work Object
* **Canonical Identifier:** `corrective_action_id` — `TEXT`, format `CA-####` **[Governance — Identifier Governance Review]**
* **Foreign Keys:** `vendor_id` → Vendor.`vendor_id` (required); `sla_event_id` → SLA Event.`sla_event_id` (optional); `fulfillment_event_id` → Fulfillment Event.`fulfillment_event_id` (optional); `related_ticket_id` → Ticket.`ticket_id` (optional)
* **Dependencies:** Vendor (Tier 0, required); SLA Event (Tier 4, optional); Fulfillment Event (Tier 3, optional); Ticket (Tier 1, optional) — the deepest dependency chain of any entity in this schema, consistent with Corrective Action being the reason dependency-order tiers were kept distinct from Object Model taxonomy in the first place.

| Attribute | Logical Type | Nullable | Source |
|---|---|---|---|
| `corrective_action_id` | `TEXT` | No (PK) | [Governance] |
| `vendor_id` | `TEXT` | No | [Governance — Enterprise-Shared, FK, required] |
| `sla_event_id` | `TEXT` | Yes | [Governance — Enterprise-Shared, FK, optional]. Populated in 5 of 5 current rows — see Deferred Logical Constraints; this is a small-sample coincidence, not evidence to tighten the approved optionality. |
| `fulfillment_event_id` | `TEXT` | Yes | [Governance — Enterprise-Shared, FK, optional]. Same caveat as above — 5 of 5 populated in current data. |
| `related_ticket_id` | `TEXT` | Yes | [Governance — Enterprise-Shared, FK, optional]. Observed populated in 3 of 5 current rows. **[Repository, n=5]** |
| `corrective_action_type` | `TEXT` | No | [Governance — Domain-Authoritative]. See Logical Constraints — not proposed as an enumeration. |
| `corrective_action_status` | `TEXT` | No | [Governance — Enterprise-Shared]. See Logical Constraints. |
| `corrective_action_severity` | `TEXT` | No | [Governance — Domain-Authoritative]. See Logical Constraints. |
| `trigger_reason` | `TEXT` | No | [Governance — Domain-Authoritative]. **Provenance tension worth flagging, same pattern as Shortage's `operational_impact` in Tier 3:** all 5 current values are distinct, full narrative sentences, not structured categories. Tag and type are unaffected (still unconstrained `TEXT`), but this reads closer to Descriptive-or-Derived in practice. **[Repository, n=5]** |
| `assigned_owner` | `TEXT` | No | [Governance — Domain-Authoritative; organizational role/team text, explicitly **not** an Employee reference, per the Logical Model's Ownership Boundary]. See Logical Constraints. |
| `remediation_plan_summary` | `TEXT` | No | [Governance — Domain-Authoritative — explicitly classified as such in an earlier approved decision, unlike `trigger_reason` above; narrative content but not flagged as a tension] |
| `monitoring_start_date` | `DATE` | No | [Governance — Domain-Authoritative]. Populated 5/5 in current data; no evidence of a lifecycle state where this is legitimately absent, unlike Shipment's `actual_delivery_date` pattern. **[Repository, n=5]** |
| `reassessment_date` | `DATE` | Yes | [Governance — Domain-Authoritative]. The subsystem source schema defines this field as optional and explicitly permits it to remain blank for newly opened corrective action cases. Current repository data happens to populate all 5 rows, but that does not override the governed lifecycle state. |
| `recovery_status` | `TEXT` | No | [Governance — Domain-Authoritative]. See Logical Constraints. |
| `escalation_required_flag`, `corrective_action_closed_flag` | `BOOLEAN` | No | [Governance — Enterprise-Shared, per the reconciled Enterprise Logical Model] |
| `notes` | `TEXT` | Yes | [Governance — Descriptive-or-Derived, narrative]. Consistent with `notes` treatment on every other entity in this schema — nullable regardless of current sample completeness. |

* **Business Candidate Key:** None approved. A Corrective Action may respond to an SLA Event, a Fulfillment Event, both, repeated findings, or a Vendor issue directly — no single source relationship is exclusive. **[Governance — Enterprise Logical Model]**
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: `corrective_action_id` unique across all records.
  * **Corrective Action Type Vocabulary.** Observed Values: `SLA Recovery`, `Fulfillment Stabilization`, `Operational Recovery`, `Continuity Risk Review`, `Escalation Reduction`. Repository Evidence: 5/5 rows, with all five values distinct. Implementation Note: record this as a provisional observed vocabulary only; do not enforce it as a hard database constraint until the business confirms the list is exhaustive.
  * **Corrective Action Status.** Permitted Values: `Escalated Review`, `Monitoring`, `Resolved`. Repository Evidence: 5/5 rows (`Monitoring` ×2, `Resolved` ×2, `Escalated Review` ×1). Implementation Note: provisional, standard small-sample caveat — thinner than most prior tiers' enumerations.
  * **Corrective Action Severity.** Permitted Values observed: `Action Required`, `Advisory`, `Escalated Review`, `Monitoring`. Repository Evidence: 5/5 rows, 4 distinct values — almost no repetition. Flagged as more tentative than Status above; treat as a weaker candidate for a hard constraint.
  * **Recovery Status.** Permitted Values observed: `Improving`, `Monitoring`, `Stable`, `Unresolved`. Repository Evidence: 5/5 rows, 4 distinct values (`Stable` ×2). Same thin-sample caveat as Severity.
  * **Assigned Owner.** Permitted Values observed: `Vendor Management`, `Supply Chain Operations`, `Operational Support`, `Inventory Leadership`. Repository Evidence: 5/5 rows. These are organizational-function labels, not a governed reference table — treat as a provisional controlled vocabulary, not a confirmed-exhaustive list.
  * **SLA Event Vendor Consistency.** When `sla_event_id` is populated, Corrective Action's `vendor_id` must match the referenced SLA Event's `vendor_id`. Verified directly against all 5 current rows — 5/5 match. Implementation Note: cross-table integrity rule; mechanism (trigger vs. application validation) deferred to SQL Implementation. **[Assumption — required to prevent contradictory governed references]**
  * **Fulfillment Event Vendor Consistency.** When `fulfillment_event_id` is populated, Corrective Action's `vendor_id` must match the referenced Fulfillment Event's `vendor_id`. Verified against all 5 current rows — 5/5 match. Same implementation note as above. **[Assumption]**
  * **SLA–Fulfillment Event Consistency.** When both `sla_event_id` and `fulfillment_event_id` are populated, the referenced SLA Event's own `fulfillment_event_id` must equal Corrective Action's `fulfillment_event_id` — the two source references must agree with each other, not just each independently agree with Vendor. Verified against all 5 current rows — 5/5 match. Same implementation note. **[Assumption]**
  * **Ticket Reference Consistency.** When both referenced source events carry non-null `related_ticket_id` values, the SLA Event and Fulfillment Event ticket references must agree with each other. When Corrective Action.`related_ticket_id` is populated, it must match every non-null ticket reference carried by its referenced SLA Event and Fulfillment Event. Repository Evidence: all 5 current SLA/Fulfillment source-event pairs agree, and all 3 Corrective Actions with populated ticket references match both linked source events. Implementation Note: cross-table integrity rule; mechanism deferred to SQL Implementation. **[Assumption]**
* **Deferred Logical Constraints:**
  * **Source-reference presence.** No rule requires at least one of `sla_event_id` or `fulfillment_event_id` to be populated. The approved architecture allows a Vendor issue to create a Corrective Action directly with neither source reference. The current 5-row sample populates both fields on every row, but that observation does not justify tightening the approved optionality.
  * **Closed-status correlation.** In all 5 current rows, `corrective_action_status = 'Resolved'` corresponds to `corrective_action_closed_flag = TRUE`, while every other observed status corresponds to `FALSE`. This remains an observed lifecycle pattern rather than a governed rule because the sample is too small to establish all valid status/closure combinations.
* **Migration Considerations:** Direct load from `vendor-corrective-actions.csv`; requires Vendor (Tier 0) and, where populated, SLA Event (Tier 4), Fulfillment Event (Tier 3), and Ticket (Tier 1) all already loaded — this entity cannot be loaded until every other tier in this schema is in place.
* **Future Expansion:** If `assigned_owner` values are ever formalized into a governed organizational-function reference table (paralleling the Department/Team reconciliation already flagged elsewhere in this schema), `assigned_owner` could become a foreign key at that point. Not proposed here. `assigned_owner` must not be migrated to `employee_id` under any circumstances without a separately governed employee-level field — this is a hard boundary carried forward from the Enterprise Logical Model, not a future option.

---

## Assignment Corrective Action

* **Purpose:** Associative entity resolving Assignment's many-to-many relationship to Corrective Action — the second of two typed associative entities replacing the rejected polymorphic Assignment-to-work-object design. **[Governance — Enterprise Logical Model, Associative Entity Resolution]**
* **Object Model Classification:** Not applicable — a logical relationship entity, not a canonical enterprise object.
* **Canonical Identifier:** Not applicable — relationship entity. **[Governance, per the associative-entity exception in Enterprise Relational Foundation]**
* **Foreign Keys:** `assignment_id` → Assignment.`assignment_id` (required); `corrective_action_id` → Corrective Action.`corrective_action_id` (required)
* **Dependencies:** Assignment (Tier 1); Corrective Action (Tier 5, required). Under the approved terminal-tier ordering exception, Corrective Action must be built before Assignment Corrective Action.

| Attribute | Logical Type | Nullable | Source |
|---|---|---|---|
| `assignment_id` | `TEXT` | No (PK, part 1) | [Governance — Enterprise Logical Model] |
| `corrective_action_id` | `TEXT` | No (PK, part 2) | [Governance — Enterprise Logical Model] |

* **Business Candidate Key:** (`assignment_id`, `corrective_action_id`).
* **Primary-Key Strategy:** The business candidate key is implemented directly as the composite primary key, per the associative-entity exception in Enterprise Relational Foundation. No surrogate identifier is introduced — there is no source data, and therefore no evidence, for any relationship-level attribute or independent lifecycle that would justify one. This mirrors the settled Replenishment Shortage Response decision in Tier 4: absence of evidence is not a reason to invent structure.
* **Logical Constraints:**

  * **Identity.** Uniqueness Rule: (`assignment_id`, `corrective_action_id`) must be unique — no duplicate pairing.
* **Deferred Logical Constraints:** None.
* **Migration Considerations:** No current source data — this table has no representation in any existing dataset. Populated only going forward, same treatment as the other three associative entities in this schema.
* **Future Expansion:** None flagged beyond what's already noted under Assignment's own Future Expansion in Tier 1 (a future third work-object type would receive its own typed associative entity, not a change to this one).

---

# Next Steps

The Enterprise Relational Schema is approved and locked.

The next controlled initiative is target-platform and SQL implementation planning. Platform-specific DDL, migrations, indexes, triggers, generated expressions, and enforcement mechanisms remain outside this document.

Before strict referential integrity is enabled, implementation planning must address the already-documented migration and enforcement conditions:

* Ticket location and owner reconciliation
* orphaned Ticket references
* `tickets-v1.csv` encoding normalization
* target-platform selection
* foreign-key deletion policy
* cross-table consistency mechanisms
* Shipment and Fulfillment Event source-of-truth translation rules
* allocation timing rules when approved or received quantities are not yet known

SQL Implementation has not begun. Any change to this locked schema requires governed change control across every affected architecture layer.

