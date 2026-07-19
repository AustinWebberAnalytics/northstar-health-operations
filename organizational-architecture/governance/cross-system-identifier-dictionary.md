# Cross-System Identifier Dictionary

## Northstar Health Operations

---

**Primary Audience:** Northstar architects, subsystem maintainers, data engineers, and reviewers responsible for cross-system integrity  
**Writing Layer:** Layer 3 — Governance  
**Architectural Purpose:** Establishes the authoritative enterprise identifier names, formats, ownership, relationship usage, and migration aliases used across all Northstar subsystems.

---

# Purpose

This document defines the shared identifiers, relationship standards, entity references, and cross-system integration rules used throughout the Northstar Health Operations ecosystem.

The purpose of this dictionary is to:

* standardize shared identifiers
* maintain cross-system consistency
* prevent identifier drift
* support operational traceability
* support relational integrity
* establish enterprise-wide identifier governance
* reinforce subsystem interoperability
* support scalable ecosystem expansion

This document serves as the authoritative identifier governance reference for the Northstar Health Operations ecosystem.

---

# Identifier Philosophy

Northstar Health Operations uses shared identifiers to connect operational activity across enterprise domains while preserving subsystem ownership and autonomy.

Shared identifiers create a common operational language that enables separate operational domains to interact without sacrificing subsystem independence.

This approach supports:

* operational traceability
* cross-system visibility
* reporting consistency
* relationship integrity
* enterprise interoperability
* governance alignment

Shared identifiers are considered enterprise assets rather than subsystem-specific implementations.

---

# Cross-System Identifier Architecture

Operational relationships are established through standardized shared identifiers.

```text
Operational Record

↓

Shared Identifier

↓

Cross-System Relationship

↓

Operational Visibility

↓

Enterprise Intelligence
```

Identifiers serve as the connective layer between operational domains while preserving subsystem-centered architecture.

---

# Core Shared Identifiers

|Identifier|Purpose|Example|
|-|-|-|
|ticket_id|Unique ticket or incident record|INC-100012|
|related_ticket_id|Connects operational records to tickets|INC-100012|
|item_id|Unique inventory item identifier|ITEM-1003|
|location_id|Unique operational location identifier|LOC-DURHAM-07|
|vendor_id|Unique vendor identifier|VEND-003|
|employee_id|Unique workforce identifier|EMP-001|
|shipment_id|Unique shipment identifier|SHIP-1002|
|replenishment_id|Unique replenishment workflow identifier|REPL-1002|
|shortage_id|Unique shortage event identifier|SHORT-1001|
|discrepancy_id|Unique discrepancy identifier|DISC-1001|
|assignment_id|Unique workforce assignment identifier|ASSIGN-001|
|corrective_action_id|Unique vendor corrective action identifier|CA-1001|
|location_inventory_id|Unique location-level stock position identifier|LOCINV-1001|
|coverage_schedule_id|Unique workforce coverage schedule identifier|SCHED-001|
|workload_record_id|Unique employee workload measurement identifier|WORK-001|
|fulfillment_event_id|Unique vendor fulfillment assessment identifier|VF-1001|
|sla_event_id|Unique SLA evaluation identifier|SLA-1001|
|escalation_id|Unique workforce escalation identifier|WF-ESC-001|

These identifiers represent the primary relational language used throughout the ecosystem. The final 8 were approved via the Enterprise Identifier Governance Review; all others were previously governed.

---

# Shared Identifier Standards

## ticket_id

### Purpose

Uniquely identifies a ticket or incident record.

### Format

```text
INC-######
```

### Example

```text
INC-100012
```

### Ownership

Ticketing System

---

## related_ticket_id

### Purpose

Connects non-ticket operational records to associated ticket records.

### Format

```text
INC-######
```

### Example

```text
INC-100012
```

### Governance Rule

Use only when a record directly references an existing operational ticket.

---

## item_id

### Purpose

Uniquely identifies an inventory item.

### Format

```text
ITEM-####
```

### Example

```text
ITEM-1003
```

### Ownership

Inventory Operations

---

## location_id

### Purpose

Identifies operational facilities, support centers, hubs, or managed locations.

### Format

```text
LOC-[LOCATION]-##
```

### Examples

```text
LOC-RALEIGH-03

LOC-DURHAM-07

LOC-WAKEFOREST-11

LOC-CARY-HUB-01
```

### Ownership

Enterprise Shared Identifier

---

## vendor_id

### Purpose

Uniquely identifies a supplier or vendor.

### Format

```text
VEND-###
```

### Example

```text
VEND-003
```

### Ownership

Vendor Performance

---

## employee_id

### Purpose

Uniquely identifies workforce personnel.

### Format

```text
EMP-###
```

### Example

```text
EMP-001
```

### Governance Note

Current workforce datasets consistently use three-digit employee sequences (`EMP-001` through `EMP-015`). The prior `EMP-####` / `EMP-1001` documentation pattern was not supported by repository data and is retired rather than treated as an alternate format.

### Ownership

Workforce Coordination

---

## shipment_id

### Purpose

Uniquely identifies shipment activity.

### Format

```text
SHIP-####
```

### Example

```text
SHIP-1002
```

### Ownership

Vendor Performance

---

## replenishment_id

### Purpose

Uniquely identifies replenishment workflow events.

### Format

```text
REPL-####
```

### Example

```text
REPL-1002
```

### Ownership

Inventory Operations

---

## shortage_id

### Purpose

Uniquely identifies shortage events.

### Format

```text
SHORT-####
```

### Example

```text
SHORT-1001
```

### Governance Note

Current shortage data uses four-digit numeric sequences. The prior five-placeholder format was a documentation error and is retired rather than treated as an alternate format.

### Ownership

Inventory Operations

---

## discrepancy_id

### Purpose

Uniquely identifies discrepancy records.

### Format

```text
DISC-####
```

### Example

```text
DISC-1001
```

### Governance Note

Current discrepancy data uses four-digit numeric sequences. The prior five-placeholder format was a documentation error and is retired rather than treated as an alternate format.

### Ownership

Inventory Operations

---

## assignment_id

### Purpose

Uniquely identifies a workforce assignment record.

### Format

```text
ASSIGN-###
```

### Example

```text
ASSIGN-001
```

### Ownership

Workforce Coordination

### Governance Note

Approved via Enterprise Identifier Governance Review. No approved business candidate key exists for Assignment — see Enterprise Logical Model.

---

## corrective_action_id

### Purpose

Uniquely identifies a vendor corrective action record.

### Format

```text
CA-####
```

### Example

```text
CA-1001
```

### Ownership

Vendor Performance

### Governance Note

Approved via Enterprise Identifier Governance Review. Surrogate-key-only by design — a Corrective Action may reference an SLA Event, a Fulfillment Event, both, or neither.

---

## location_inventory_id

### Purpose

Uniquely identifies a location-level stock position for a given inventory item.

### Format

```text
LOCINV-####
```

### Example

```text
LOCINV-1001
```

### Ownership

Inventory Operations

### Governance Note

Approved via Enterprise Identifier Governance Review — already the governed physical field name; elevated to canonical cross-system status. Business candidate key: `location_id` + `item_id`.

---

## coverage_schedule_id

### Purpose

Uniquely identifies a workforce coverage schedule record.

### Format

```text
SCHED-###
```

### Example

```text
SCHED-001
```

### Ownership

Workforce Coordination

### Governance Note

Approved via Enterprise Identifier Governance Review as a rename of the legacy field `schedule_id`, for enterprise-name consistency. `schedule_id` is documented as a legacy source-field alias for migration purposes and should not be treated as a competing identifier. No approved business candidate key exists — see Enterprise Logical Model.

---

## workload_record_id

### Purpose

Uniquely identifies an employee workload measurement for a reporting period.

### Format

```text
WORK-###
```

### Example

```text
WORK-001
```

### Ownership

Workforce Coordination

### Governance Note

Approved via Enterprise Identifier Governance Review as a rename of the legacy field `workload_id`, for enterprise-name consistency. `workload_id` is documented as a legacy source-field alias. Business candidate key: `employee_id` + `reporting_period`.

---

## fulfillment_event_id

### Purpose

Uniquely identifies a vendor fulfillment assessment event.

### Format

```text
VF-####
```

### Example

```text
VF-1001
```

### Ownership

Vendor Performance

### Governance Note

Approved via Enterprise Identifier Governance Review. No approved business candidate key exists — see Enterprise Logical Model.

---

## sla_event_id

### Purpose

Uniquely identifies an SLA evaluation event.

### Format

```text
SLA-####
```

### Example

```text
SLA-1001
```

### Ownership

Vendor Performance

### Governance Note

Approved via Enterprise Identifier Governance Review. `sla_category` is approved as a Domain-Authoritative attribute but not yet part of a business candidate key, pending a business decision on SLA re-evaluation behavior.

---

## escalation_id

### Purpose

Uniquely identifies a workforce escalation record.

### Format

```text
WF-ESC-###
```

### Example

```text
WF-ESC-001
```

### Ownership

Workforce Coordination

### Governance Note

Approved via Enterprise Identifier Governance Review. No rename proposed — the attribute name already matches current data. No approved business candidate key exists; escalations are not consistently employee-specific.

---

# Approved Legacy Source-Field Aliases

The following source-field names remain valid only as migration aliases. They are not competing enterprise identifiers.

|Legacy Source Field|Governed Enterprise Identifier|Migration Treatment|
|-|-|-|
|`schedule_id`|`coverage_schedule_id`|Rename during transformation; preserve the original name only in source-mapping documentation.|
|`workload_id`|`workload_record_id`|Rename during transformation; preserve the original name only in source-mapping documentation.|

No subsystem should introduce new files, schemas, or relational columns using these legacy field names after migration.

---

# Relationship Standards

Subsystems should establish relationships through shared identifiers rather than duplicated descriptive text.

Preferred:

```text
shortage_id

item_id

related_ticket_id
```

Avoid:

```text
Item Name

Vendor Name

Location Description
```

when a shared identifier already exists.

Identifiers should remain the primary mechanism for establishing operational relationships.

---

# Cross-System Relationship Architecture

The ecosystem intentionally supports cross-system operational relationships.

Examples include:

## Inventory to Ticketing

```text
related_ticket_id

↓

ticket_id
```

Used when inventory activity generates or references operational incidents.

Examples:

* shortages
* discrepancy investigations
* replenishment failures
* operational escalations

---

## Inventory to Vendor Performance

```text
vendor_id

↓

vendor_id
```

Used when inventory activity references vendor performance, shipment activity, or supplier accountability.

Examples:

* fulfillment tracking
* shipment monitoring
* vendor evaluation
* service performance analysis

---

## Inventory Item Relationships

```text
item_id

↓

item_id
```

Used throughout:

* location inventory
* replenishments
* shortages
* discrepancies
* vendor shipments

---

## Location Relationships

```text
location_id

↓

location_id
```

Used throughout:

* inventory management
* shipment receiving
* shortage reporting
* workforce coordination
* operational support activities

---

# Entity Expansion Standards

Future subsystem expansion may introduce new enterprise identifiers.

Examples may include:

|Identifier|Purpose|
|-|-|
|department_id|Department reporting|
|process_id|Process improvement records|
|scorecard_id|Vendor scorecards|
|audit_id|Governance review records|

`schedule_id` has been removed from this placeholder list — it is superseded by the now-governed `coverage_schedule_id` (see Shared Identifier Standards, above), per the Enterprise Identifier Governance Review. Retaining both would violate the Single Identifier Principle below.

Future identifiers should:

* use stable prefixes
* maintain clear ownership
* support enterprise interoperability
* follow approved naming standards
* be documented before broad implementation

Expansion should strengthen identifier consistency rather than create competing identifier systems.

---

# Data Quality Governance

Shared identifiers should be reviewed for:

* duplicate identifiers
* missing identifiers
* invalid identifier formats
* broken relationships
* inconsistent references
* ownership conflicts

Relationship quality should be monitored throughout subsystem expansion and remediation activities.

---

# Identifier Governance Principles

## Single Identifier Principle

Each operational concept should maintain one approved enterprise identifier.

Examples:

```text
vendor_id
```

Preferred over:

```text
vendor_number

vendor_code

supplier_id
```

for the same operational concept.

---

## Ownership Principle

Every shared identifier should have a clearly defined ownership domain.

Ownership responsibility includes:

* identifier definition
* format governance
* relationship consistency
* expansion oversight

---

## Expansion Principle

New shared identifiers should be reviewed before implementation.

Identifiers should not be introduced independently within subsystems if they may eventually become enterprise assets.

---

# Governance Alignment

This document aligns with:

* Project Governance Standards
* Naming Convention Standards
* Remediation Standards
* Operational Severity Framework
* Enterprise System Map
* Operational Intelligence Lifecycle
* Enterprise Object Model
* Enterprise Relational Model
* Enterprise Logical Model
* Enterprise Identifier Governance Review

Shared identifiers should remain consistent with all approved governance and architecture standards.

---

# Summary

The Cross-System Identifier Dictionary establishes the enterprise identifier framework used throughout the Northstar Health Operations ecosystem.

By standardizing shared identifiers, relationship structures, ownership responsibilities, and cross-system integration practices, the ecosystem maintains traceability, consistency, interoperability, and long-term architectural stability across all operational domains.

Shared identifiers are treated as enterprise governance assets that support operational visibility, subsystem integration, and sustainable ecosystem growth.

This revision incorporates the 8 identifiers approved by the Enterprise Identifier Governance Review, completing identifier coverage for all 17 objects in the Enterprise Logical Model's implementation scope. It also reconciles the `employee_id`, `shortage_id`, and `discrepancy_id` format specifications to the authoritative repository datasets and records the approved migration aliases for Coverage Schedule and Workload Record.

