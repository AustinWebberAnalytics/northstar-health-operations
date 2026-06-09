# Cross-System Identifier Dictionary

## Northstar Health Operations

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
|employee_id|Unique workforce identifier|EMP-1001|
|shipment_id|Unique shipment identifier|SHIP-1002|
|replenishment_id|Unique replenishment workflow identifier|REPL-1002|
|shortage_id|Unique shortage event identifier|SHORT-1001|
|discrepancy_id|Unique discrepancy identifier|DISC-1001|

These identifiers represent the primary relational language used throughout the ecosystem.

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
EMP-####
```

### Example

```text
EMP-1001
```

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
SHORT-#####
```

### Example

```text
SHORT-1001
```

### Ownership

Inventory Operations

---

## discrepancy_id

### Purpose

Uniquely identifies discrepancy records.

### Format

```text
DISC-#####
```

### Example

```text
DISC-1001
```

### Ownership

Inventory Operations

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
|schedule_id|Scheduling records|
|department_id|Department reporting|
|process_id|Process improvement records|
|scorecard_id|Vendor scorecards|
|audit_id|Governance review records|

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

Shared identifiers should remain consistent with all approved governance and architecture standards.

---

# Summary

The Cross-System Identifier Dictionary establishes the enterprise identifier framework used throughout the Northstar Health Operations ecosystem.

By standardizing shared identifiers, relationship structures, ownership responsibilities, and cross-system integration practices, the ecosystem maintains traceability, consistency, interoperability, and long-term architectural stability across all operational domains.

Shared identifiers are treated as enterprise governance assets that support operational visibility, subsystem integration, and sustainable ecosystem growth.

