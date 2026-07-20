# Enterprise Logical Model

## Northstar Health Operations

---

**Primary Audience:** Northstar architects, data engineers, subsystem maintainers, and reviewers translating approved architecture into implementation-ready logical design

**Writing Layer:** Layer 2 — Operational / Architectural

**Architectural Purpose:** Defines logical entities, attributes, canonical identifiers, business candidate keys, integrity rules, and relationship implementation patterns for the 17 governed enterprise objects and 4 required associative entities.

**Document Type:** Logical Data Model

**Authority Level:** Approved Engineering Design

**Status:** Approved — Locked

**Depends On:** Enterprise Object Model and Enterprise Relational Model

---

# Purpose

This document translates the approved Enterprise Object Model and Enterprise Relational Model into an implementation-ready logical data model.

It defines, for each governed enterprise object in the current implementation scope:

- logical attributes, grouped by semantic role, with three-part provenance (Enterprise-Shared / Domain-Authoritative / Descriptive-or-Derived),
- canonical identifiers, business candidate keys, and uniqueness/integrity rules — kept as distinct concepts, justified by business meaning rather than incidental data observation,
- relationship implementation patterns, including required associative entities,
- integrity rules,
- and the maturity status inherited from the Relational Model, carried forward as an implementation-sequencing signal.

---

# Characteristics of the Enterprise Logical Model

**This document defines:**

- enterprise entities, at the logical (not physical) level
- logical attributes belonging to each entity, independent of storage type
- canonical identifiers, business candidate keys, and the distinction between them
- integrity and uniqueness rules, stated as business constraints
- required associative entities, where genuine many-to-many business relationships demand them

**This document intentionally does not define:**

- SQL syntax, table definitions, or DDL
- physical data types (e.g., `VARCHAR(50)` vs. `TEXT`)
- indexes, storage engine, or platform-specific behavior (SQLite vs. PostgreSQL)
- performance or query-optimization considerations
- objects outside the current 17-object implementation scope

A logical attribute name (e.g., `sla_category`) is a legitimate logical-layer concept. Its eventual column type, index strategy, and storage representation are physical-layer concerns belonging to the phases that follow this document (Enterprise Relational Foundation, Enterprise Relational Schema, and SQL Implementation).

---

# Relationship to Enterprise Architecture

```text
Enterprise Philosophy
        │
        ▼
Enterprise System Map
        │
        ▼
Enterprise Object Model
        │
        ▼
Enterprise Relational Model
        │
        ▼
Enterprise Logical Model   ← this document
        │
        ▼
Enterprise Identifier Governance Review
        │
        ▼
Enterprise Relational Foundation
        │
        ▼
Enterprise Relational Schema
        │
        ▼
SQL Implementation
```

Read alongside: **Enterprise Object Model** (canonical objects, not restated here), **Enterprise Relational Model** (canonical relationships, not restated here), **Cross-System Identifier Dictionary**, **Naming Convention Standards**.

---

# Implementation Scope

**Enterprise Foundation Objects:** Location, Employee, Vendor, Inventory Item
**Operational Work Objects:** Ticket, Assignment, Corrective Action
**Movement Objects:** Shipment, Replenishment
**Operational State Objects:** Location Inventory, Inventory Discrepancy, Shortage, Coverage Schedule, Workload Record
**Assessment Objects:** Fulfillment Event, SLA Event, Workforce Escalation

Future objects named in the Object Model's Future Expansion Boundary are not modeled as current logical entities or relationship targets.

---

# Relationship Resolution Summary

| Classification | Count | Relationships |
|---|---|---|
| **Required associative entity** | 4 | Assignment↔Ticket, Assignment↔Corrective Action, Shipment↔Replenishment, Replenishment↔Shortage |
| **Implemented through an existing governed pattern** | 1 | Workforce Escalation → Ticket (reuses `related_ticket_id`) |
| **Deferred** | 6 | Vendor↔Inventory Item, Shipment↔Inventory Item, Coverage Schedule↔Assignment, Workforce Escalation↔Employee, Workforce Escalation↔Workload Record, Workforce Escalation↔Coverage Schedule |
| **Analytical/historical (out of scope)** | 2 | Assignment→Workload Record, Shipment→Location Inventory |

Full reasoning appears in **Associative Entity Resolution**, below the entity catalog.

---

# Logical Modeling Principles

## Three-Part Identity Distinction

| Concept | Definition |
|---|---|
| **Canonical identifier** | The governed enterprise identity used to reference the object across domains. |
| **Business candidate key** | A natural or logical attribute combination the *business* recognizes as uniquely identifying the record — independent of, and justified separately from, the surrogate canonical identifier. |
| **Uniqueness rule / integrity rule** | A business constraint preventing invalid records. A uniqueness rule enforces a key; an integrity rule (e.g., no overlapping coverage periods) constrains validity without defining identity. |

**Terminology note:** where an entity has no business-justified candidate key, this document states `Business Candidate Key: None approved` alongside its own `Uniqueness Rule: <identifier> unique`. The canonical identifier is never itself listed as the business candidate key — doing so would contradict the distinction this document exists to preserve. (A surrogate key can be considered a "candidate key" under some formal relational definitions; this document's usage is deliberately narrower and refers specifically to a business-derived alternative.)

Empirical checks against current repository data were performed to catch invented keys that don't survive contact with real data. Those checks inform confidence but are never, alone, the justification for a business candidate key — they are recorded separately in **Validation Notes**.

## Identifier Governance Status

At the time this document was first derived, 8 of 17 entities had no governed canonical identifier and were marked **Provisional — Pending Governance Approval**. All 8 have since been reviewed and approved via the **Enterprise Identifier Governance Review** and are now recorded in the Cross-System Identifier Dictionary:

| Entity | Canonical Identifier | Format |
|---|---|---|
| Assignment | `assignment_id` | `ASSIGN-###` |
| Corrective Action | `corrective_action_id` | `CA-####` |
| Location Inventory | `location_inventory_id` | `LOCINV-####` |
| Coverage Schedule | `coverage_schedule_id` | `SCHED-###` (renamed from legacy `schedule_id`) |
| Workload Record | `workload_record_id` | `WORK-###` (renamed from legacy `workload_id`) |
| Fulfillment Event | `fulfillment_event_id` | `VF-####` |
| SLA Event | `sla_event_id` | `SLA-####` |
| Workforce Escalation | `escalation_id` | `WF-ESC-###` |

Per-entity sections below reflect this approved status rather than the original provisional language, since carrying stale "pending" language forward after approval would misstate the current governance state.

Repository-wide identifier reconciliation also corrected three previously documented patterns without changing current data values: `employee_id` uses `EMP-###`, `shortage_id` uses `SHORT-####`, and `discrepancy_id` uses `DISC-####`. The Cross-System Identifier Dictionary and Enterprise Identifier Governance Review are authoritative for these formats.

## Attribute Provenance and Grouping

Logical attributes are grouped by semantic role (Identity, Classification, Lifecycle State, Ownership, Temporal, etc.) and tagged with one of three provenance categories:

- **Enterprise-Shared** — used across domains, or required for enterprise identity and cross-domain integrity (identifiers, foreign keys, status fields that gate cross-domain behavior).
- **Domain-Authoritative** — logically belongs to the object and is governed by its authoritative domain, even when other domains don't consume it (e.g., `vendor_name`, `ordered_quantity`, `remediation_plan_summary`). These are real business facts, not optional detail, and must not be dropped during physical schema design.
- **Descriptive-or-Derived** — narrative, presentation-oriented, or calculated from other attributes (e.g., `notes`, `response_hours`, `capacity_utilization_percent`).

This replaces a two-tier canonical/subsystem-local split used in an earlier draft, which risked the physical design phase reading "not enterprise-shared" as "safe to omit."

## Organizational Semantics Note (Department / Team)

`department` and `team` attributes appear as Domain-Authoritative below, tagged **pending reconciliation**. This qualifier is stated on evidence from this model and the current repository, not from a prior formal architecture decision:

- `assigned_department` appears on Ticket
- `department` and `team` appear on Employee
- `department` and `affected_team` appear on Workforce Escalation
- no canonical `department_id` or `team_id` exists anywhere in the repository
- no shared reference dataset governs these values
- no controlled enterprise vocabulary establishes whether these terms mean the same thing across domains

These are legitimate current logical attributes of their respective entities — the reconciliation concern is about their enterprise-wide semantic consistency, not their validity as domain attributes.

---

# Logical Entity Definitions

## Enterprise Foundation Objects

### Location

- **Canonical Identifier:** `location_id` — *Established*
- **Business Candidate Key:** None approved
- **Uniqueness Rule:** `location_id` unique
- **Logical Attributes — Identity:** `location_id` [Enterprise-Shared]
- **Known Limitation Carried Forward:** No dedicated Location entity/table currently exists. Establishing Location as a first-class entity is part of this model's implementation scope.
- **Governed Relationships:** Location Inventory; Inventory Item indirectly through Location Inventory (no direct Location↔Inventory Item pairing exists in the Relational Model); Shipment, Replenishment, Shortage, Inventory Discrepancy, Ticket, and Fulfillment Event directly.

---

### Employee

- **Canonical Identifier:** `employee_id` — *Established*
- **Business Candidate Key:** None approved
- **Uniqueness Rule:** `employee_id` unique
- **Logical Attributes — Identity:** `employee_id` [Enterprise-Shared]
- **Logical Attributes — Domain Detail:** `employee_name` [Domain-Authoritative]
- **Logical Attributes — Organizational Placement:** `department`, `team` [Domain-Authoritative — organizational semantics pending reconciliation], `role` [Domain-Authoritative]
- **Logical Attributes — Status:** `employment_status`, `active_flag` [Enterprise-Shared]
- **Logical Attributes — Operational Detail:** `primary_shift`, `standard_weekly_hours`, `skill_area`, `coverage_priority` [Descriptive-or-Derived]
- **Governed Relationships:** Assignment, Coverage Schedule, Workload Record, Workforce Escalation *(planned)*, Ticket *(planned)*

---

### Vendor

- **Canonical Identifier:** `vendor_id` — *Established*
- **Business Candidate Key:** None approved
- **Uniqueness Rule:** `vendor_id` unique
- **Logical Attributes — Identity:** `vendor_id` [Enterprise-Shared]
- **Logical Attributes — Classification:** `vendor_type`, `primary_service_category` [Domain-Authoritative]
- **Logical Attributes — Status:** `risk_tier` [Domain-Authoritative], `active_vendor_flag` [Enterprise-Shared]
- **Logical Attributes — Domain Detail:** `vendor_name`, `support_level`, `preferred_vendor_flag`, `emergency_fulfillment_flag`, `primary_contact_team` [Domain-Authoritative]
- **Logical Attributes — Descriptive:** `notes` [Descriptive-or-Derived]
- **Governed Relationships:** Shipment, Inventory Item (preferred-sourcing role only — see note below), Fulfillment Event, SLA Event, Corrective Action, Replenishment

**Scope note:** Inventory Item's `preferred_vendor_id` implements only the current preferred-sourcing role. It does **not** fully implement the canonical Vendor↔Inventory Item many-to-many relationship — that relationship remains deferred.

---

### Inventory Item

- **Canonical Identifier:** `item_id` — *Established*
- **Business Candidate Key:** None approved
- **Uniqueness Rule:** `item_id` unique
- **Logical Attributes — Identity:** `item_id` [Enterprise-Shared]
- **Logical Attributes — Classification:** `item_category`, `criticality_level`, `unit_of_measure` [Domain-Authoritative]
- **Logical Attributes — Sourcing:** `preferred_vendor_id` (FK to Vendor — scoped, see note above) [Enterprise-Shared]
- **Logical Attributes — Status:** `active_flag` [Enterprise-Shared]
- **Logical Attributes — Domain Detail:** `item_name` [Domain-Authoritative]
- **Governed Relationships:** Vendor (preferred-sourcing only), Shipment, Replenishment, Location Inventory, Inventory Discrepancy, Shortage, Fulfillment Event

---

## Operational Work Objects

### Ticket

- **Canonical Identifier:** `ticket_id` — *Established* (`INC-######`)
- **Business Candidate Key:** None approved
- **Uniqueness Rule:** `ticket_id` unique
- **Logical Attributes — Identity:** `ticket_id` [Enterprise-Shared]
- **Logical Attributes — Classification:** `category`, `priority` [Domain-Authoritative]
- **Logical Attributes — Lifecycle State:** `status`, `escalation_flag` [Enterprise-Shared]; `reopened_flag`, `pending_flag`, `sla_met_flag` [Domain-Authoritative]
- **Logical Attributes — Ownership:** `requesting_location`, `assigned_department`, `assigned_owner` [Enterprise-Shared *intent* — currently free text; see limitation below]
- **Logical Attributes — Canonical References:** `location_id` (planned FK to Location), `employee_id` (planned FK to Employee) [Enterprise-Shared — introduced through the documented reconciliation sequence below; null until `requesting_location`/`assigned_owner` are reconciled]
- **Logical Attributes — Temporal:** `created_at`, `first_response_at`, `resolved_at`, `closed_at`, `sla_target_hours` [Domain-Authoritative]; `resolution_hours`, `response_hours` [Descriptive-or-Derived — calculated]
- **Logical Attributes — Descriptive:** `summary`, `resolution_notes` [Descriptive-or-Derived]
- **Known Limitation Carried Forward:** `requesting_location` and `assigned_owner` are enterprise-meaningful in intent but currently free text. Formalizing them as foreign keys is a distinct data-reconciliation and migration workstream, not merely a DDL change:

  ```text
  Create canonical Location and Employee references
        ↓
  Profile existing requesting_location / assigned_owner values
        ↓
  Build mapping rules and exception reports
        ↓
  Migrate resolvable values
        ↓
  Review unresolved values
        ↓
  Enforce referential integrity only after reconciliation
  ```

  This sequence is in scope for the Enterprise Relational Foundation initiative and its downstream Enterprise Relational Schema / SQL Implementation work, but should be tracked as a separate workstream within it. Strict FK enforcement should not be enabled before existing values are mapped and validated.
- **Governed Relationships:**
  - Location (direct relationship — `Ticket → occurs at → Location`)
  - Employee (direct relationship — `Ticket → is owned by → Employee`, planned)
  - Inventory Discrepancy, Shortage, Replenishment, Shipment, Corrective Action, SLA Event, Fulfillment Event, and Workforce Escalation — via the governed `related_ticket_id` pattern

---

### Assignment

- **Canonical Identifier:** `assignment_id` — **Approved** (`ASSIGN-###`, per Enterprise Identifier Governance Review)
- **Business Candidate Key:** None approved. Assignment currently carries no work-target reference, and assignment categories are broad and recurring rather than tied to a single dated business event.
- **Uniqueness Rule:** `assignment_id` unique. This is independent of the still-unresolved business-candidate-key question above — the canonical identifier's uniqueness does not depend on assignment-category governance.
- **Logical Attributes — Identity:** `assignment_id` [Enterprise-Shared]
- **Logical Attributes — Ownership:** `employee_id` (FK) [Enterprise-Shared]
- **Logical Attributes — Classification:** `assignment_category` [Domain-Authoritative]
- **Logical Attributes — Lifecycle State:** `assignment_status` [Enterprise-Shared]; `start_date`, `end_date` [Domain-Authoritative]
- **Logical Attributes — Domain Detail:** `assignment_name`, `priority_level`, `estimated_hours_per_week`, `cross_functional_flag` [Domain-Authoritative]
- **Governed Relationships:** Employee, Ticket and Corrective Action *(via required associative entities)*, Coverage Schedule *(deferred)*, Workload Record *(analytical/historical)*

---

### Corrective Action

- **Canonical Identifier:** `corrective_action_id` — **Approved** (`CA-####`, per Enterprise Identifier Governance Review)
- **Business Candidate Key:** None approved. A Corrective Action may respond to an SLA Event, a Fulfillment Event, both, repeated findings, or a Vendor issue directly — no single source relationship is exclusive.
- **Uniqueness Rule:** `corrective_action_id` unique. Duplicate-detection heuristics (vendor + issue type + source event + monitoring start date) may later support review but are not approved keys.
- **Logical Attributes — Identity:** `corrective_action_id` [Enterprise-Shared]
- **Logical Attributes — Responsible Party:** `vendor_id` (FK) [Enterprise-Shared]
- **Logical Attributes — Source References:** `sla_event_id` (FK, optional), `fulfillment_event_id` (FK, optional), `related_ticket_id` (FK to Ticket, optional) [Enterprise-Shared]
- **Logical Attributes — Lifecycle State:** `corrective_action_status`, `escalation_required_flag`, `corrective_action_closed_flag` [Enterprise-Shared]; `corrective_action_severity`, `recovery_status` [Domain-Authoritative]
- **Logical Attributes — Organizational Ownership:** `assigned_owner` [Domain-Authoritative — organizational role or team text, not an Employee reference]
- **Logical Attributes — Domain Detail:** `corrective_action_type`, `trigger_reason`, `remediation_plan_summary`, `monitoring_start_date`, `reassessment_date` [Domain-Authoritative]
- **Logical Attributes — Descriptive:** `notes` [Descriptive-or-Derived]
- **Ownership Boundary:** Current `assigned_owner` values identify organizational functions such as Vendor Management, Supply Chain Operations, Operational Support, and Inventory Leadership. They do not identify Employees and must not be migrated to `employee_id` without a separately governed employee-level field.
- **Governed Relationships:** Vendor, SLA Event, Fulfillment Event, Ticket (via `related_ticket_id`), Assignment (via required Assignment Corrective Action associative entity)

---

## Movement Objects

### Shipment

- **Canonical Identifier:** `shipment_id` — *Established*
- **Business Candidate Key:** None approved
- **Uniqueness Rule:** `shipment_id` unique
- **Logical Attributes — Identity:** `shipment_id` [Enterprise-Shared]
- **Logical Attributes — References:** `vendor_id`, `item_id`, `location_id`, `related_ticket_id` (FK to Ticket, optional) [Enterprise-Shared]
- **Logical Attributes — Status:** `delivery_status` [Enterprise-Shared]
- **Logical Attributes — Domain Detail:** `ordered_quantity`, `received_quantity`, `order_date`, `expected_delivery_date`, `actual_delivery_date` [Domain-Authoritative]
- **Logical Attributes — Derived:** `fulfillment_accuracy_flag`, `delay_flag` [Descriptive-or-Derived — computed from quantity/date comparisons]
- **Scope note:** Retaining `item_id` directly on Shipment implements a one-item-per-shipment business assumption (see Validation Notes). A `Shipment Line` associative entity is **not** introduced in this phase.
- **Governed Relationships:** Vendor, Inventory Item (single-item, current scope), Location, Replenishment *(via required associative entity)*, Fulfillment Event, SLA Event, Ticket (via `related_ticket_id`)

---

### Replenishment

- **Canonical Identifier:** `replenishment_id` — *Established*
- **Business Candidate Key:** None approved
- **Uniqueness Rule:** `replenishment_id` unique
- **Logical Attributes — Identity:** `replenishment_id` [Enterprise-Shared]
- **Logical Attributes — References:** `item_id`, `location_id`, `vendor_id`, `related_ticket_id` (FK to Ticket, optional) [Enterprise-Shared]
- **Logical Attributes — Status:** `replenishment_status` [Enterprise-Shared]
- **Logical Attributes — Domain Detail:** `replenishment_type`, `requested_quantity`, `approved_quantity`, `request_date`, `expected_arrival_date`, `received_date` [Domain-Authoritative]
- **Governed Relationships:** Inventory Item, Location, Vendor, Shipment *(via required associative entity)*, Shortage *(via required associative entity)*, Ticket (via `related_ticket_id`)

---

## Operational State Objects

### Location Inventory

- **Canonical Identifier:** `location_inventory_id` — **Approved** (`LOCINV-####`, per Enterprise Identifier Governance Review; already the governed physical field name, elevated to canonical cross-system status)
- **Business Candidate Key:** `location_id` + `item_id` — business-justified: the enterprise recognizes exactly one active stock position per item per location.
- **Uniqueness Rule:** One active `location_inventory` record per (`location_id`, `item_id`) pair
- **Logical Attributes — Identity:** `location_inventory_id` [Enterprise-Shared]
- **Logical Attributes — References:** `item_id`, `location_id` (FKs) [Enterprise-Shared]
- **Logical Attributes — State:** `current_stock`, `stock_status` [Enterprise-Shared]
- **Logical Attributes — Domain Detail:** `reorder_point`, `target_stock_level`, `safety_stock_level`, `last_count_date` [Domain-Authoritative]
- **Governed Relationships:** Inventory Item, Location, Shipment *(analytical/historical — deferred)*, Inventory Discrepancy, Shortage

---

### Inventory Discrepancy

- **Canonical Identifier:** `discrepancy_id` — *Established*
- **Business Candidate Key:** None approved
- **Uniqueness Rule:** `discrepancy_id` unique
- **Logical Attributes — Identity:** `discrepancy_id` [Enterprise-Shared]
- **Logical Attributes — References:** `item_id`, `location_id`, `related_ticket_id` (FK to Ticket, optional) [Enterprise-Shared]
- **Logical Attributes — Status:** `investigation_status` [Enterprise-Shared]
- **Logical Attributes — Domain Detail:** `expected_quantity`, `counted_quantity`, `variance_quantity`, `discrepancy_type`, `discovered_date`, `resolved_date` [Domain-Authoritative]
- **Governed Relationships:** Inventory Item, Location, Location Inventory, Ticket (via `related_ticket_id`)

---

### Shortage

- **Canonical Identifier:** `shortage_id` — *Established*
- **Business Candidate Key:** None approved
- **Uniqueness Rule:** `shortage_id` unique
- **Logical Attributes — Identity:** `shortage_id` [Enterprise-Shared]
- **Logical Attributes — References:** `item_id`, `location_id`, `related_ticket_id` (FK to Ticket, optional) [Enterprise-Shared]
- **Logical Attributes — Status:** `shortage_severity`, `resolution_status` [Enterprise-Shared]; `escalation_flag` [Enterprise-Shared]
- **Logical Attributes — Domain Detail:** `shortage_detected_date`, `estimated_days_of_stockout`, `operational_impact` [Domain-Authoritative]
- **Governed Relationships:** Inventory Item, Location, Location Inventory, Replenishment *(via required associative entity)*, Ticket (via `related_ticket_id`)

---

### Coverage Schedule

- **Canonical Identifier:** `coverage_schedule_id` — **Approved** (`SCHED-###`, per Enterprise Identifier Governance Review; approved rename from legacy source field `schedule_id`, documented as a migration alias)
- **Business Candidate Key:** None approved. `location_id` is explicitly excluded — Coverage Schedule has no Location relationship in the approved Relational Model.
- **Integrity Rule (distinct from uniqueness):** An Employee should not have incompatible overlapping coverage periods. This rule is recognized but **structurally deferred** — it cannot currently be evaluated by any mechanism, since Coverage Schedule has no `coverage_start_at`/`coverage_end_at` or governed Shift definition with explicit time boundaries. `schedule_date` and `shift_type` alone don't define when a period starts or ends. Not a choice of enforcement mechanism pending decision — no mechanism can evaluate it until one of those exists.
- **Logical Attributes — Identity:** `coverage_schedule_id` [Enterprise-Shared]
- **Logical Attributes — Reference:** `employee_id` (FK) [Enterprise-Shared]
- **Logical Attributes — Schedule:** `schedule_date`, `shift_type` [Domain-Authoritative]; `coverage_status` [Enterprise-Shared]
- **Logical Attributes — Domain Detail:** `scheduled_hours`, `coverage_area` (descriptive text, not a Location reference), `coverage_priority`, `backup_required_flag` [Domain-Authoritative]
- **Governed Relationships:** Employee, Assignment *(deferred)*, Workforce Escalation *(deferred)*

---

### Workload Record

- **Canonical Identifier:** `workload_record_id` — **Approved** (`WORK-###`, per Enterprise Identifier Governance Review; approved rename from legacy source field `workload_id`, documented as a migration alias)
- **Business Candidate Key:** `employee_id` + `reporting_period` — business-justified: the enterprise recognizes one workload measurement per employee per reporting period (see Validation Notes for supporting data check).
- **Logical Attributes — Identity:** `workload_record_id` [Enterprise-Shared]
- **Logical Attributes — Reference:** `employee_id` (FK) [Enterprise-Shared]
- **Logical Attributes — Period:** `reporting_period` [Enterprise-Shared]
- **Logical Attributes — Status:** `workload_status` [Domain-Authoritative]
- **Logical Attributes — Domain Detail:** `assigned_tasks`, `completed_tasks`, `open_tasks`, `estimated_hours`, `actual_hours` [Domain-Authoritative]
- **Logical Attributes — Derived:** `capacity_utilization_percent` [Descriptive-or-Derived — calculated]
- **Governed Relationships:** Employee, Assignment *(analytical/historical)*, Workforce Escalation *(deferred)*

---

## Assessment Objects

### Fulfillment Event

- **Canonical Identifier:** `fulfillment_event_id` — **Approved** (`VF-####`, per Enterprise Identifier Governance Review)
- **Business Candidate Key:** None approved (see Validation Notes)
- **Logical Attributes — Identity:** `fulfillment_event_id` [Enterprise-Shared]
- **Logical Attributes — References:** `vendor_id`, `shipment_id`, `item_id`, `location_id`, `related_ticket_id` (FK to Ticket, optional) [Enterprise-Shared]
- **Logical Attributes — Status:** `fulfillment_status`, `delivery_status`, `escalation_required_flag` [Enterprise-Shared]
- **Logical Attributes — Domain Detail:** `order_date`, `expected_delivery_date`, `actual_delivery_date`, `expected_quantity`, `received_quantity`, `partial_fulfillment_flag`, `emergency_fulfillment_flag`, `operational_impact_level` [Domain-Authoritative]
- **Logical Attributes — Derived:** `fulfillment_accuracy_flag`, `delay_flag`, `delay_days` [Descriptive-or-Derived]
- **Logical Attributes — Descriptive:** `notes` [Descriptive-or-Derived]
- **Governed Relationships:** Vendor, Shipment, Inventory Item, Location, SLA Event, Corrective Action, Ticket (via `related_ticket_id`)

---

### SLA Event

- **Canonical Identifier:** `sla_event_id` — **Approved** (`SLA-####`, per Enterprise Identifier Governance Review)
- **Business Candidate Key:** None approved. `sla_category` is approved as a Domain-Authoritative logical attribute, but not yet as part of a business candidate key — the business has not yet governed whether each Shipment may have one evaluation per category, repeated evaluations, multiple periods, or revised assessments (see Validation Notes).
- **Logical Attributes — Identity:** `sla_event_id` [Enterprise-Shared]
- **Logical Attributes — References:** `vendor_id`, `shipment_id`, `fulfillment_event_id`, `related_ticket_id` (FK to Ticket, optional) [Enterprise-Shared]
- **Logical Attributes — Classification:** `sla_category` [Domain-Authoritative]
- **Logical Attributes — Status:** `sla_status`, `sla_breach_flag` [Enterprise-Shared]; `escalation_required_flag`, `corrective_action_required_flag` [Enterprise-Shared]
- **Logical Attributes — Domain Detail:** `sla_target_hours`, `actual_response_hours`, `operational_impact_level`, `review_date` [Domain-Authoritative]
- **Logical Attributes — Descriptive:** `notes` [Descriptive-or-Derived]
- **Governed Relationships:** Vendor, Shipment, Fulfillment Event, Corrective Action, Ticket (via `related_ticket_id`)

---

### Workforce Escalation

- **Canonical Identifier:** `escalation_id` — **Approved** (`WF-ESC-###`, per Enterprise Identifier Governance Review; no rename — attribute name already matched current data)
- **Business Candidate Key:** None approved. The architecture explicitly allows escalations not tied to one employee; no employee-based key is valid.
- **Logical Attributes — Identity:** `escalation_id` [Enterprise-Shared]
- **Logical Attributes — Organizational Reference:** `department` [Domain-Authoritative — organizational semantics pending reconciliation]
- **Logical Attributes — Classification:** `escalation_type`, `severity_level` [Domain-Authoritative]
- **Logical Attributes — Status:** `current_status` [Enterprise-Shared]
- **Logical Attributes — Domain Detail:** `escalation_date`, `root_cause`, `resolution_owner` [Domain-Authoritative]; `affected_team` [Domain-Authoritative — organizational semantics pending reconciliation]
- **Logical Attributes — Descriptive:** `business_impact` [Descriptive-or-Derived — narrative]
- **Known Limitation Carried Forward:** No `employee_id` or `related_ticket_id` attribute currently exists on this entity. Adding `related_ticket_id` — following the same *Established* pattern used by other governed objects — is implementation scope this model defines.
- **Governed Relationships:** Ticket *(via `related_ticket_id`, to be added)*, Employee *(planned, not yet represented)*, Coverage Schedule *(deferred — evidentiary)*, Workload Record *(deferred — evidentiary)*

---

# Associative Entity Resolution

## Required Associative Entities

### Assignment Ticket

Resolves: Assignment → allocates responsibility for → Operational Work Object (Ticket case). A logical relationship entity, not a new canonical enterprise object.

- `assignment_id` (FK to Assignment)
- `ticket_id` (FK to Ticket)

### Assignment Corrective Action

Resolves: Assignment → allocates responsibility for → Operational Work Object (Corrective Action case).

- `assignment_id` (FK to Assignment)
- `corrective_action_id` (FK to Corrective Action)

A future work-object type receives its own typed associative entity rather than a generic target-type column.

### Shipment Replenishment Allocation

Resolves: Shipment → fulfills → Replenishment — documented as one of the most significant architectural gaps identified during Phase 3. Named Allocation, not Fulfillment, to avoid colliding with Fulfillment Event's distinct meaning (vendor-performance assessment) — see Enterprise Relational Schema, Tier 3, for the full naming rationale.

- `shipment_id` (FK to Shipment)
- `replenishment_id` (FK to Replenishment)
- `allocated_quantity` — **logical requirement, not a physical-schema deferral.** Without it, the model can state that a Shipment allocates toward a Replenishment but not what portion — which defeats the stated purpose of this associative entity (supporting partial/multi-shipment fulfillment). Its data type, constraints, and storage are physical-design decisions; its existence is not.
- `allocation_date` — **not included.** No current business evidence distinguishes relationship-level allocation timing from the Shipment's own receipt date. Add only if that distinction becomes a real requirement.

### Replenishment Shortage Response

Resolves: Replenishment → responds to → Shortage — explicit documented business behavior (multiple Replenishments may address one Shortage; one Replenishment may mitigate several).

- `replenishment_id` (FK to Replenishment)
- `shortage_id` (FK to Shortage)

## Relationships Implemented Through an Existing Object (No New Entity)

**Workforce Escalation → may generate → Ticket.** Resolved via the *Established* `related_ticket_id` pattern already governing other relationships. Requires adding `related_ticket_id` to Workforce Escalation, which does not currently exist on that entity.

## Deferred Relationships

| Relationship | Reason Deferred | Revisit Trigger |
|---|---|---|
| Vendor supplies Inventory Item | Current business rule is one preferred vendor per item; multi-vendor sourcing is documented future evolution | Multi-vendor sourcing becomes an actual operational requirement |
| Shipment carries Inventory Item | Business assumption is one item per shipment for current scope | Multi-item shipments become an operational requirement |
| Coverage Schedule constrains Assignment | No governed identifiers link them yet; reads as a validation rule rather than a stored relationship | Both entities are governed and a concrete need for stored linkage emerges |
| Workforce Escalation assesses risk affecting Employee | Relationship is genuinely Planned Foundation; not yet represented at any grain | Escalation model is extended to capture individual-employee escalations |
| Workforce Escalation is supported by Workload Record | Evidentiary/citation relationship, not required for operational correctness | Escalation review process formally requires citing supporting evidence |
| Workforce Escalation is supported by Coverage Schedule | Same as above | Same as above |

## Analytical / Historical Relationships (Out of Scope for This Model)

| Relationship | Reason |
|---|---|
| Assignment contributes to Workload Record | Workload Record is a rollup/summary; real traceability needs an activity/event log, not a join table |
| Shipment changes Location Inventory | Explicitly "Many-to-Many over time"; the Relational Model itself points to future inventory-transaction-history modeling |

---

# Integrity Rules (Cross-Entity Summary)

| Rule | Entities Involved | Type |
|---|---|---|
| An Employee should not have incompatible overlapping coverage periods | Coverage Schedule | Integrity rule (not uniqueness) |
| Every associative-entity pair must reference existing records on both sides | Assignment, Ticket, Corrective Action, Shipment, Replenishment, Shortage | Referential integrity |
| Exactly one active record per (`location_id`, `item_id`) pair | Location Inventory | Uniqueness |
| `preferred_vendor_id` implements preferred-sourcing only, not the full Vendor↔Inventory Item relationship | Vendor, Inventory Item | Scope-boundary rule (documentation, not a database constraint) |
| Fulfillment Event `vendor_id`, `item_id`, and `location_id` must match the referenced Shipment | Fulfillment Event, Shipment, Vendor, Inventory Item, Location | Cross-table reference consistency |
| `requesting_location` / `assigned_owner` should resolve to governed `location_id` / `employee_id` references only after the documented migration sequence completes | Ticket, Location, Employee | Data-quality / migration rule, not yet enforced |

---

# Validation Notes (Non-Architectural)

These are empirical spot-checks against current repository data. They inform confidence but are never, on their own, justification for a business candidate key.

| Entity / Question | Data Checked | Result |
|---|---|---|
| Does any `shipment_id` carry more than one `item_id`? | `vendor-shipments.csv`, 6 rows | No — 0 of 6. Small sample; supports, does not prove, the one-item-per-shipment scope decision. |
| Does `employee_id` + `schedule_date` collide in Coverage Schedule? | `workforce-coverage-schedule.csv`, 15 rows | No collisions in 15 rows. |
| Does `employee_id` + `reporting_period` collide in Workload Record? | `workforce-workload-distribution.csv`, 15 rows | No collisions in 15 rows. |
| Does `shipment_id` collide in Fulfillment Event? | `vendor-fulfillment-events.csv`, 6 rows | No collisions in 6 rows — too small a sample to elevate to a candidate key. |
| Does `shipment_id` + `sla_category` collide in SLA Event? | `vendor-sla-tracking.csv`, 6 rows | No collisions in 6 rows — same caveat; category-governance decision still pending regardless. |
| Does `employee_id` exist anywhere in Workforce Escalation data? | `workforce-escalations.csv` | No — the column does not exist at all. Escalations are currently department/team-grained only. |
| Does `location_id` exist anywhere in Coverage Schedule data? | `workforce-coverage-schedule.csv` | No — the column does not exist at all. |
| Does Employee contain the name needed for Ticket owner reconciliation? | `workforce-roster.csv` | Yes — `employee_name` exists and is required in the logical entity. Current ticket data still contains unmatched owner names that must be resolved before enforcing `employee_id`. |
| Does Corrective Action `assigned_owner` identify Employees? | `vendor-corrective-actions.csv`, 5 rows | No — current values are organizational teams/functions, not employee names or IDs. No Employee relationship is approved from this field. |

---

# Governance Decisions Recorded

- **Identifier renames** (`schedule_id` → `coverage_schedule_id`, `workload_id` → `workload_record_id`) were approved via the Enterprise Identifier Governance Review, the same process used for net-new identifiers. Prior field names are documented as legacy source-field aliases for migration purposes, not silently replaced.
- **`sla_category`** is approved as a Domain-Authoritative logical attribute. It is not yet approved as part of a business candidate key, pending a business decision on SLA re-evaluation and multi-category assessment behavior.
- **Ticket free-text migration** (`requesting_location`, `assigned_owner`) is in scope for the Enterprise Relational Foundation initiative as a distinct data-reconciliation and migration workstream — see the sequence documented under Ticket, above. Referential-integrity enforcement is deferred until after reconciliation completes.
- **Employee name preservation:** `employee_name` is Domain-Authoritative and must remain in Employee because the Ticket owner reconciliation process depends on matching free-text owner names to canonical employee identities.
- **Corrective Action ownership:** `assigned_owner` remains organizational ownership text. The current data does not support an Employee foreign key, and no employee relationship may be inferred from this field.
- **Fulfillment Event shipment consistency:** Fulfillment Event repeats Vendor, Inventory Item, and Location references from Shipment. These references must agree with the referenced Shipment even though the implementation mechanism is deferred to SQL Implementation.
- **`Shipment Replenishment Allocation`** (originally `Shipment Replenishment Fulfillment`) and its `allocated_quantity` attribute (originally `fulfilled_quantity`) were renamed during Enterprise Relational Schema Tier 3 derivation, to avoid colliding with Fulfillment Event's distinct meaning. Approved and reflected throughout this document.

The Enterprise Relational Schema and Enterprise Database Platform Decision were approved without reopening this locked logical baseline. SQL Implementation still requires Ticket owner/location reconciliation, orphaned Ticket resolution, Shipment/Fulfillment translation decisions, allocation-timing decisions, and physical enforcement design.

---

# Summary

This document establishes the enterprise logical data model derived from the approved Enterprise Object Model and Enterprise Relational Model. It resolves 4 associative entities as genuinely required by business meaning, reuses 1 existing governed pattern, and explicitly defers 6 relationships and 2 analytical/historical relationships with documented reasoning.

Business candidate keys are stated as business conclusions, never as the canonical identifier restated, and never justified solely by a data observation. Attribute provenance uses a three-part distinction (Enterprise-Shared / Domain-Authoritative / Descriptive-or-Derived) specifically to prevent later implementation phases from misreading domain-important attributes as optional.

8 of 17 entities required provisional canonical identifiers at initial derivation. All 8 have since been approved via the Enterprise Identifier Governance Review and are recorded in the Cross-System Identifier Dictionary.

Organizational Architecture reconciliation additionally preserved `employee_name` for Ticket-owner mapping, removed an unsupported Corrective Action-to-Employee inference, aligned Fulfillment Event references with Shipment consistency requirements, and corrected governed identifier formats to match authoritative datasets.
