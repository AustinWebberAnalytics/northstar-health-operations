# Enterprise Identifier Governance Review

## Northstar Health Operations

---

**Document Type:** Governance Decision Record
**Knowledge Layer:** Governance
**Authority Level:** Identifier Governance Review
**Status:** Approved — Phase 4 Foundation
**Depends On:** Enterprise Logical Model (approved)

---

# Purpose

This review examines every provisional canonical identifier introduced by the Enterprise Logical Model and decides whether each becomes canonical. It does not modify the Cross-System Identifier Dictionary directly — dictionary updates are a separate artifact, produced only after this review is approved, per governance discipline (design → review → approve → lock).

Eight identifiers are in scope:

`assignment_id`, `corrective_action_id`, `location_inventory_id`, `coverage_schedule_id`, `workload_record_id`, `fulfillment_event_id`, `sla_event_id`, `escalation_id`

---

# Review Methodology

For each identifier, this review checks:

1. **Naming-standards conformance** — snake_case, business-readable, no camelCase or abbreviation drift, per Naming Convention Standards.
2. **Prefix collision** — checked against all 9 currently governed prefixes (`INC`, `ITEM`, `VEND`, `LOC`, `SHIP`, `REPL`, `SHORT`, `DISC`, `EMP`).
3. **Format grounding** — the proposed format is the one already in use in current repository data, not an invented alternative. Every format below was verified directly against the relevant CSV, not assumed.
4. **Ownership** — the authoritative domain already established in the Enterprise Object Model.

This review does not reopen business-candidate-key decisions already recorded in the Enterprise Logical Model (e.g., Assignment and Coverage Schedule remain "no business candidate key approved"). Identifier governance and candidate-key governance are separate questions; only the former is in scope here.

---

# Identifier Decisions

## assignment_id

* **Format (verified against `workforce-assignments.csv`):** `ASSIGN-###`
* **Example:** `ASSIGN-001`
* **Ownership:** Workforce Coordination
* **Naming-standards conformance:** Pass — snake_case, consistent with existing identifier naming.
* **Collision check:** No collision with governed prefixes.
* **Decision:** **APPROVED**
* **Reasoning:** Supports enterprise identity for the Assignment entity; format already in live use; no competing identifier exists for this concept.

---

## corrective_action_id

* **Format (verified against `vendor-corrective-actions.csv`):** `CA-####`
* **Example:** `CA-1001`
* **Ownership:** Vendor Performance
* **Naming-standards conformance:** Pass.
* **Collision check:** No collision. Note: `CA` is a short, generic-looking prefix — flagged for awareness, not blocking. If a future enterprise object also plausibly abbreviates to `CA`, this should be revisited; no such object currently exists in the Object Model's approved or future-expansion scope.
* **Decision:** **APPROVED**
* **Reasoning:** Format already in live use; ownership matches Object Model's authoritative domain; no collision found.

---

## location_inventory_id

* **Format (verified against `location-inventory.csv`):** `LOCINV-####`
* **Example:** `LOCINV-1001`
* **Ownership:** Inventory Operations
* **Naming-standards conformance:** Pass.
* **Collision check:** No collision. Distinguishable from `LOC` (Location) despite the shared root — the four-letter prefix avoids ambiguity.
* **Decision:** **APPROVED**
* **Reasoning:** Already the literal column name and value format in current repository data — this is an elevation to canonical governed status, not a new introduction. Candidate key (`location_id` + `item_id`) was already established in the Enterprise Logical Model and is not reopened here.

---

## coverage_schedule_id

* **Current physical field:** `schedule_id`
* **Format (verified against `workforce-coverage-schedule.csv`):** `SCHED-###`
* **Example:** `SCHED-001`
* **Ownership:** Workforce Coordination
* **Naming-standards conformance:** Pass for the canonical name `coverage_schedule_id`; the format itself (`SCHED-###`) requires no change.
* **Collision check:** No collision.
* **Decision:** **APPROVED, with rename condition**
* **Reasoning:** `coverage_schedule_id` was proposed in the Enterprise Logical Model for enterprise-name consistency with other renamed entities. This is a rename of an existing governed concept, not a new identifier — `schedule_id` is documented below as a legacy source-field alias for migration purposes. The dictionary's own Entity Expansion Standards section previously listed `schedule_id` as an anticipated future identifier; that placeholder is superseded by this decision and removed in the updated dictionary to avoid two names for one concept.

---

## workload_record_id

* **Current physical field:** `workload_id`
* **Format (verified against `workforce-workload-distribution.csv`):** `WORK-###`
* **Example:** `WORK-001`
* **Ownership:** Workforce Coordination
* **Naming-standards conformance:** Pass for the canonical name; format unchanged.
* **Collision check:** No collision.
* **Decision:** **APPROVED, with rename condition**
* **Reasoning:** Same treatment as `coverage_schedule_id` — rename for enterprise-name consistency, `workload_id` documented as legacy alias, business candidate key (`employee_id` + `reporting_period`) already established and not reopened here.

---

## fulfillment_event_id

* **Format (verified against `vendor-fulfillment-events.csv`):** `VF-####`
* **Example:** `VF-1001`
* **Ownership:** Vendor Performance
* **Naming-standards conformance:** Pass on the attribute name. The value prefix `VF` is terser than most governed prefixes and doesn't spell out "fulfillment event" the way `SHORT` or `DISC` spell out their concepts — flagged for awareness. Changing a live value prefix has the same migration cost as an attribute rename; not proposed here without a specific reason to disturb existing data.
* **Collision check:** No collision.
* **Decision:** **APPROVED**
* **Reasoning:** Format already in live use; no collision; the terseness concern is cosmetic, not a governance blocker.

---

## sla_event_id

* **Format (verified against `vendor-sla-tracking.csv`):** `SLA-####`
* **Example:** `SLA-1001`
* **Ownership:** Vendor Performance
* **Naming-standards conformance:** Pass.
* **Collision check:** No collision.
* **Decision:** **APPROVED**
* **Reasoning:** Format already in live use. `sla_category` remains approved as a Domain-Authoritative attribute but not yet part of a business candidate key, per the Enterprise Logical Model — that decision is unaffected by, and not reopened by, this identifier approval.

---

## escalation_id

* **Format (verified against `workforce-escalations.csv`):** `WF-ESC-###`
* **Example:** `WF-ESC-001`
* **Ownership:** Workforce Coordination
* **Naming-standards conformance:** Pass.
* **Collision check:** No collision.
* **Naming question resolved:** An earlier draft of the Enterprise Logical Model raised whether this identifier should be named `workforce_escalation_id` instead, since the value prefix (`WF-ESC`) carries "workforce" semantics. Checked directly against the data: the physical column name is already `escalation_id`, matching what the Enterprise Logical Model already established and used throughout. No rename is proposed — the value prefix carrying additional semantic detail than the attribute name is normal (see `ticket_id` → `INC-######`, which doesn't spell out "incident" either) and is not, by itself, reason to rename a governed attribute.
* **Decision:** **APPROVED**
* **Reasoning:** Attribute name already matches current data exactly; format already in live use; no collision.

---

# Summary of Decisions

|Identifier|Decision|Condition|
|-|-|-|
|`assignment_id`|APPROVED|None|
|`corrective_action_id`|APPROVED|None|
|`location_inventory_id`|APPROVED|None (already-existing physical field elevated to canonical status)|
|`coverage_schedule_id`|APPROVED|Rename from `schedule_id`; legacy alias documented|
|`workload_record_id`|APPROVED|Rename from `workload_id`; legacy alias documented|
|`fulfillment_event_id`|APPROVED|None|
|`sla_event_id`|APPROVED|None|
|`escalation_id`|APPROVED|None; naming question resolved in favor of no change|

All 8 identifiers are approved. None are rejected or held. Two carry a rename condition, both already anticipated and recorded as governance decisions in the Enterprise Logical Model.

---

# Next Steps

1. Update the Cross-System Identifier Dictionary to reflect these 8 approved identifiers (produced as a companion artifact to this review).
2. Do not amend the dictionary independently of this review — this review is the authoritative record of *why*; the dictionary records *what is currently governed*.
3. With both artifacts committed, the logical engineering foundation (Enterprise Object Model → Enterprise Relational Model → Enterprise Logical Model → Enterprise Identifier Governance) is complete. Enterprise SQL Foundation work may begin.

---

# Summary

This review evaluated the eight provisional identifiers introduced by the Enterprise Logical Model against naming standards, collision risk, ownership, and data-grounded format evidence.

All eight identifiers are approved, with two approved under documented rename conditions. No identifier format was invented during this review; every approved format reflects identifiers already present within the current repository.

These approvals complete enterprise identifier governance for all objects currently within the Enterprise Logical Model implementation scope and establish the canonical identifier foundation for the Enterprise SQL Foundation phase.

