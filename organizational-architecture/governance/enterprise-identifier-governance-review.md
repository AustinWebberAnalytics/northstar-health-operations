# Enterprise Identifier Governance Review

## Northstar Health Operations

---

**Primary Audience:** Northstar architects, governance reviewers, subsystem maintainers, and data engineers responsible for enterprise identity and cross-system integrity

**Writing Layer:** Layer 3 — Governance

**Architectural Purpose:** Records the authoritative rationale for approving canonical enterprise identifiers, governing identifier renames, and correcting identifier formats when repository evidence conflicts with prior documentation.

**Document Type:** Governance Decision Record

**Authority Level:** Approved Governance Decision

**Status:** Approved — Locked

**Depends On:** Enterprise Object Model, Enterprise Relational Model, Enterprise Logical Model, Cross-System Identifier Dictionary, and Naming Convention Standards

---

# Purpose

This review establishes the authoritative governance decisions behind the canonical identifiers used by the Enterprise Logical Model and Cross-System Identifier Dictionary.

The review originally evaluated eight identifiers that had been introduced provisionally during logical modeling. All eight were approved. During the later Organizational Architecture reconciliation, repository-wide validation also identified three previously governed identifier formats whose documented patterns did not match the authoritative datasets. Those format corrections are recorded here so the Cross-System Identifier Dictionary is not updated independently of its governance rationale.

This document records *why* each decision was made. The Cross-System Identifier Dictionary records *what is currently governed*.

---

# Scope

## Original Identifier Approval Scope

The following eight identifiers were introduced provisionally by the Enterprise Logical Model and required formal governance approval:

`assignment_id`, `corrective_action_id`, `location_inventory_id`, `coverage_schedule_id`, `workload_record_id`, `fulfillment_event_id`, `sla_event_id`, `escalation_id`

## Reconciliation Scope

The Organizational Architecture reconciliation later validated all governed identifier patterns against current repository datasets. That review identified three documentation patterns requiring correction:

`employee_id`, `shortage_id`, `discrepancy_id`

These are format corrections to already-governed identifiers. They do not introduce new enterprise objects or change identifier ownership.

---

# Review Methodology

Each identifier decision was evaluated against the following standards:

1. **Naming-standard conformance** — attribute names use governed snake_case and remain business-readable.
2. **Prefix collision control** — identifier prefixes do not conflict with another governed enterprise object.
3. **Repository grounding** — documented formats and examples must match values present in authoritative current datasets.
4. **Ownership alignment** — identifier ownership matches the authoritative domain established in the Enterprise Object Model.
5. **Migration impact** — renames and format corrections distinguish between true value migration, source-field aliasing, and documentation-only correction.
6. **Authority consistency** — the governance record and Cross-System Identifier Dictionary must remain synchronized.

This review does not reopen business-candidate-key decisions recorded in the Enterprise Logical Model. Canonical identifier governance and business candidate key governance remain separate concerns.

---

# Canonical Identifier Approval Decisions

## assignment_id

* **Format verified against:** `workforce-assignments.csv`
* **Canonical format:** `ASSIGN-###`
* **Example:** `ASSIGN-001`
* **Ownership:** Workforce Coordination
* **Naming-standard conformance:** Pass
* **Collision check:** No collision with governed prefixes
* **Decision:** **APPROVED**
* **Reasoning:** The identifier supports enterprise identity for Assignment, already exists in current data, and has no competing identifier for the same concept.

---

## corrective_action_id

* **Format verified against:** `vendor-corrective-actions.csv`
* **Canonical format:** `CA-####`
* **Example:** `CA-1001`
* **Ownership:** Vendor Performance
* **Naming-standard conformance:** Pass
* **Collision check:** No current collision
* **Decision:** **APPROVED**
* **Reasoning:** The identifier already exists in current data and aligns with the authoritative domain. The short `CA` prefix is retained because no current or approved future enterprise object creates a collision. Any future competing use of `CA` requires governance review.

---

## location_inventory_id

* **Format verified against:** `location-inventory.csv`
* **Canonical format:** `LOCINV-####`
* **Example:** `LOCINV-1001`
* **Ownership:** Inventory Operations
* **Naming-standard conformance:** Pass
* **Collision check:** No collision; distinguishable from `LOC` for Location
* **Decision:** **APPROVED**
* **Reasoning:** The physical field and value format already exist in current data. This decision elevates the identifier to canonical cross-system status rather than introducing a new identifier. The approved business candidate key of `location_id` + `item_id` remains separate and is not reopened here.

---

## coverage_schedule_id

* **Legacy source field:** `schedule_id`
* **Format verified against:** `workforce-coverage-schedule.csv`
* **Canonical format:** `SCHED-###`
* **Example:** `SCHED-001`
* **Ownership:** Workforce Coordination
* **Naming-standard conformance:** Pass for `coverage_schedule_id`
* **Collision check:** No collision
* **Decision:** **APPROVED WITH RENAME CONDITION**
* **Reasoning:** `coverage_schedule_id` provides enterprise-name consistency and distinguishes the entity clearly from a generic schedule concept. The value format does not change. `schedule_id` remains documented only as a legacy source-field alias for migration and must not be treated as a second canonical identifier.

---

## workload_record_id

* **Legacy source field:** `workload_id`
* **Format verified against:** `workforce-workload-distribution.csv`
* **Canonical format:** `WORK-###`
* **Example:** `WORK-001`
* **Ownership:** Workforce Coordination
* **Naming-standard conformance:** Pass for `workload_record_id`
* **Collision check:** No collision
* **Decision:** **APPROVED WITH RENAME CONDITION**
* **Reasoning:** `workload_record_id` provides enterprise-name consistency while preserving the existing value format. `workload_id` remains documented only as a legacy source-field alias for migration. The approved business candidate key of `employee_id` + `reporting_period` remains separate and is not reopened here.

---

## fulfillment_event_id

* **Format verified against:** `vendor-fulfillment-events.csv`
* **Canonical format:** `VF-####`
* **Example:** `VF-1001`
* **Ownership:** Vendor Performance
* **Naming-standard conformance:** Pass
* **Collision check:** No collision
* **Decision:** **APPROVED**
* **Reasoning:** The identifier and value format already exist in current data. The `VF` prefix is terse but unambiguous within the governed object set. Changing live values for cosmetic consistency would create migration cost without improving integrity.

---

## sla_event_id

* **Format verified against:** `vendor-sla-tracking.csv`
* **Canonical format:** `SLA-####`
* **Example:** `SLA-1001`
* **Ownership:** Vendor Performance
* **Naming-standard conformance:** Pass
* **Collision check:** No collision
* **Decision:** **APPROVED**
* **Reasoning:** The identifier and format already exist in current data and align with the authoritative domain. Approval of `sla_event_id` does not approve `sla_category` as part of a business candidate key; that separate decision remains deferred in the Enterprise Logical Model.

---

## escalation_id

* **Format verified against:** `workforce-escalations.csv`
* **Canonical format:** `WF-ESC-###`
* **Example:** `WF-ESC-001`
* **Ownership:** Workforce Coordination
* **Naming-standard conformance:** Pass
* **Collision check:** No collision
* **Decision:** **APPROVED**
* **Reasoning:** The attribute name already matches current data. The value prefix carries additional workforce context without requiring the attribute to be renamed `workforce_escalation_id`. This is consistent with other governed cases where the value prefix is more specific than the field name.

---

# Existing Identifier Format Reconciliation

## employee_id

* **Prior documented format:** `EMP-####`
* **Prior documented example:** `EMP-1001`
* **Repository-validated format:** `EMP-###`
* **Repository-validated example:** `EMP-001`
* **Evidence:** Current workforce roster, assignment, coverage schedule, and workload datasets consistently use three-digit employee sequences.
* **Decision:** **CORRECT DOCUMENTATION TO `EMP-###`**
* **Migration impact:** None. Current values remain unchanged.
* **Governance treatment:** `EMP-####` and `EMP-1001` are retired documentation errors, not supported legacy aliases and not alternate valid formats.

---

## shortage_id

* **Prior documented format:** `SHORT-#####`
* **Repository-validated format:** `SHORT-####`
* **Repository-validated example:** `SHORT-1001`
* **Evidence:** Current shortage data consistently uses four digits after the prefix.
* **Decision:** **CORRECT DOCUMENTATION TO `SHORT-####`**
* **Migration impact:** None. Current values remain unchanged.
* **Governance treatment:** `SHORT-#####` is retired as an unsupported documentation pattern, not retained as an alternate format.

---

## discrepancy_id

* **Prior documented format:** `DISC-#####`
* **Repository-validated format:** `DISC-####`
* **Repository-validated example:** `DISC-1001`
* **Evidence:** Current inventory discrepancy data consistently uses four digits after the prefix.
* **Decision:** **CORRECT DOCUMENTATION TO `DISC-####`**
* **Migration impact:** None. Current values remain unchanged.
* **Governance treatment:** `DISC-#####` is retired as an unsupported documentation pattern, not retained as an alternate format.

---

# Summary of Canonical Identifier Approvals

| Identifier | Decision | Condition |
|---|---|---|
| `assignment_id` | Approved | None |
| `corrective_action_id` | Approved | None |
| `location_inventory_id` | Approved | Existing physical field elevated to canonical status |
| `coverage_schedule_id` | Approved | Rename from `schedule_id`; legacy source-field alias retained for migration |
| `workload_record_id` | Approved | Rename from `workload_id`; legacy source-field alias retained for migration |
| `fulfillment_event_id` | Approved | None |
| `sla_event_id` | Approved | None |
| `escalation_id` | Approved | Existing attribute name retained |

---

# Summary of Format Reconciliation Decisions

| Identifier | Retired Documentation Pattern | Governed Format | Data Migration Required |
|---|---|---|---|
| `employee_id` | `EMP-####` | `EMP-###` | No |
| `shortage_id` | `SHORT-#####` | `SHORT-####` | No |
| `discrepancy_id` | `DISC-#####` | `DISC-####` | No |

---

# Governance Rules Established

1. The Enterprise Identifier Governance Review is the authoritative record of identifier decision rationale.
2. The Cross-System Identifier Dictionary is the authoritative reference for current identifier names, formats, examples, ownership, and migration aliases.
3. The review and dictionary must remain synchronized. Neither artifact may be changed independently when a decision affects governed identity.
4. Repository data is the source of truth when a documented format conflicts with consistently implemented current identifiers, unless an explicit migration decision overrides the data.
5. A documentation correction does not create a legacy alias. Unsupported patterns are retired unless current data or an approved migration process requires continued recognition.
6. Source-field aliases such as `schedule_id` and `workload_id` are migration aids only and do not establish alternate canonical identifiers.
7. Identifier approval does not automatically establish a business candidate key, uniqueness rule beyond canonical identity, or relationship cardinality.

---

# Completed Outcomes

1. All eight provisional identifiers were approved and added to the Cross-System Identifier Dictionary.
2. The canonical renames from `schedule_id` to `coverage_schedule_id` and from `workload_id` to `workload_record_id` were documented with migration-only legacy aliases.
3. The unsupported documentation patterns for `employee_id`, `shortage_id`, and `discrepancy_id` were corrected to match authoritative repository data without changing current values.
4. The Enterprise Object Model, Enterprise Relational Model, Enterprise Logical Model, Enterprise Relational Foundation, and Enterprise Relational Schema are required to use the governed identifiers recorded here and in the dictionary.
5. Downstream relational design was authorized to proceed under the approved Enterprise Relational Foundation and tier-by-tier schema review process.

---

# Summary

This governance review approves eight canonical identifiers introduced through the Enterprise Logical Model and records three later format corrections discovered during repository-wide Organizational Architecture reconciliation.

All approved identifier formats are grounded in current repository evidence. Two identifiers carry governed source-field renames, while three previously documented formats were corrected without requiring data migration. Together with the Cross-System Identifier Dictionary, this document establishes the authoritative enterprise identity baseline for Northstar Health Operations.
