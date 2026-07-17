# Enterprise Relational Schema

## Northstar Health Operations

---

**Document Type:** Engineering Design Document
**Knowledge Layer:** System Design
**Authority Level:** Design Specification — Built and Reviewed Tier by Tier
**Status:** Draft — Tiers 0–1 Populated, Tiers 2–5 Not Yet Started
**Depends On:** Enterprise Logical Model, Enterprise Identifier Governance Review, Enterprise Relational Foundation (all approved)

---

# Purpose

This document derives a schema specification — entities, attributes, logical types, keys, and logical constraints — from the already-approved Enterprise Logical Model, Cross-System Identifier Dictionary, Enterprise Relational Model, and current repository data. It is not SQL. It is the platform-independent blueprint that a `CREATE TABLE` statement, for any engine, would be generated from — including its constraints, which are stated as business rules here and only become SQL syntax at implementation.

Nothing in this document is invented. Every field is traceable to one of three sources, tagged explicitly per decision:

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

---

# Build Status

|Tier|Entities|Status|
|-|-|-|
|Tier 0|Location, Employee, Vendor|**Locked**|
|Tier 1|Inventory Item, Ticket, Assignment, Coverage Schedule, Workload Record|**Populated below**|
|Tier 2|Shipment, Replenishment, Location Inventory, Workforce Escalation, Assignment Ticket|Not started|
|Tier 3|Inventory Discrepancy, Shortage, Fulfillment Event, Shipment Replenishment Fulfillment|Not started|
|Tier 4|SLA Event, Replenishment Shortage Response|Not started|
|Tier 5|Corrective Action, Assignment Corrective Action|Not started|

Per agreed process: this document stops after Tier 1 for review. Tier 2 begins only after Tier 1 is locked.

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
* **Canonical Identifier:** `employee_id` — `TEXT`, format `EMP-####` **[Governance — Identifier Dictionary]**

|Attribute|Logical Type|Nullable|Source|
|-|-|-|-|
|`employee_id`|`TEXT`|No (PK)|[Governance]|
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
* **Migration Considerations:** Direct load from `workforce-roster.csv`; no field renaming required.
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
* **Migration Considerations:** This is the entity where the Ticket free-text migration sequence (already documented in the Enterprise Logical Model) actually applies: profile `requesting_location`/`assigned_owner` values → build mapping rules → migrate resolvable values → review exceptions → enforce FK. `requesting_location` values observed (`Cary Distribution Hub 01`, `Durham Outpatient Clinic 07`, `Raleigh Specialty Clinic 03`, `Wake Forest Clinic 11`) appear mappable to the four `location_id` values already documented in Naming Convention Standards (`LOC-CARY-HUB-01`, `LOC-DURHAM-07`, `LOC-RALEIGH-03`, `LOC-WAKEFOREST-11`) by inspection, but this is an observation, not a completed mapping. **[Repository, n=15; mapping itself is an Assumption pending the actual reconciliation pass]**
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

# Next Steps

Tier 1 is complete and ready for review. Per the agreed process, Tier 2 (Shipment, Replenishment, Location Inventory, Workforce Escalation, Assignment Ticket) does not begin until Tier 1 is locked.

