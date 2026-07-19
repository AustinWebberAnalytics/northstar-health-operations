# Naming Convention Standards

## Northstar Health Operations

\---

**Primary Audience:** Northstar architects, subsystem maintainers, data engineers, and contributors naming repository artifacts

**Writing Layer:** Layer 3 — Governance

**Architectural Purpose:** Defines the authoritative naming rules for folders, files, datasets, fields, identifiers, and shared enterprise concepts.

**Document Type:** Governance Standard

**Authority Level:** Approved Governance Standard

**Status:** Approved — Locked

\---

# Purpose

This document defines the enterprise naming standards used throughout the Northstar Health Operations ecosystem.

The purpose of these standards is to:

* maintain naming consistency
* prevent naming drift
* support subsystem scalability
* improve operational readability
* support cross-system integration
* establish enterprise-wide naming expectations
* reinforce governance-first architecture
* maintain long-term ecosystem maintainability

This document serves as the authoritative naming governance reference for the Northstar Health Operations ecosystem.

\---

# Naming Philosophy

Northstar Health Operations prioritizes:

# operational clarity over naming creativity

Naming conventions exist to improve:

* readability
* consistency
* maintainability
* interoperability
* traceability
* governance alignment

Naming standards should remain:

* predictable
* stable
* business-readable
* operationally meaningful
* enterprise-consistent

The objective of naming governance is not to create rigid formatting rules.

The objective is to create a shared language that supports operational understanding across all enterprise domains.

\---

# Enterprise Naming Model

The ecosystem applies naming standards across multiple governance layers.

```text
Repository

↓

Subsystem

↓

Folder

↓

Dataset

↓

Field

↓

Identifier

↓

Reporting Artifact

↓

Workflow Artifact
```

Each layer serves a distinct operational purpose and should maintain naming consistency with the layers surrounding it.

\---

# Repository \& Subsystem Naming Standards

Repository and subsystem names should use:

* lowercase formatting
* hyphen-separated naming
* operationally descriptive terminology

Examples:

```text
ticketing-system/

inventory-operations/

vendor-performance/

workforce-coordination/

executive-briefings/

organizational-architecture/
```

Avoid:

```text
InventorySystem/

VendorData/

Ops/

tickets/
```

Subsystem names should clearly communicate:

* operational purpose
* organizational role
* enterprise function

\---

# Standardized Subsystem Architecture Naming

All operational subsystems should maintain standardized internal folder naming.

Approved structure:

```text
datasets/

documentation/

reporting-and-kpis/

workflow-diagrams/

process-improvement/
```

Folder names should:

* remain lowercase
* remain hyphen-separated where applicable
* avoid abbreviations
* avoid synonym drift
* remain consistent across subsystems

Avoid:

```text
reports/

kpis/

docs/

workflow-maps/

improvements/
```

Preferred:

```text
reporting-and-kpis/

documentation/

workflow-diagrams/

process-improvement/
```

Subsystem-specific folder naming variations should not be introduced without governance approval.

\---

# Dataset Naming Standards

Dataset filenames should use:

* lowercase formatting
* hyphen-separated naming
* business-readable terminology
* workflow-aware naming
* operationally meaningful descriptions

Examples:

```text
inventory-items.csv

location-inventory.csv

replenishment-events.csv

shortage-events.csv

vendor-shipments.csv

vendor-scorecards.csv

tickets-v1.csv
```

Avoid:

```text
InventoryData.csv

ticketsNEW.csv

vendorReport.xlsx

inventory\_export\_final.csv
```

Dataset names should clearly communicate:

* dataset purpose
* operational function
* workflow context
* analytical use case

\---

# Field Naming Standards

All field names should use:

```text
snake\_case
```

Examples:

```text
vendor\_id

related\_ticket\_id

shipment\_delay\_hours

resolution\_timestamp

escalation\_flag

inventory\_status
```

Avoid:

```text
vendorID

VendorId

shipmentDelay

ResolutionHours
```

\---

# Field Naming Governance Principles

Field names should:

* remain business-readable
* remain operationally descriptive
* avoid inconsistent abbreviations
* maintain cross-system consistency
* support analytical readability

Avoid:

* spaces
* camelCase
* mixed naming conventions
* subsystem-specific shorthand

Field naming should prioritize long-term consistency over short-term convenience.

\---

# Shared Identifier Standards

Shared identifiers serve as enterprise assets and should remain consistent across operational domains.

Approved prefixes:

|Entity|Prefix|
|-|-|
|Tickets|INC|
|Inventory Items|ITEM|
|Vendors|VEND|
|Locations|LOC|
|Shipments|SHIP|
|Replenishments|REPL|
|Shortages|SHORT|
|Discrepancies|DISC|
|Employees|EMP|

Examples:

```text
INC-100012

ITEM-1003

VEND-003

LOC-DURHAM-07

SHIP-1002
```

Shared identifiers should:

* remain standardized
* avoid subsystem-specific variations
* support cross-system visibility
* maintain stable formatting

Shared identifiers are governed as enterprise assets rather than subsystem-specific implementations.

\---

# Reporting Artifact Naming Standards

Reporting artifacts should use:

* operationally descriptive terminology
* leadership-readable language
* stable version structures
* workflow-oriented naming

Examples:

```text
weekly-operational-summary.xlsx

inventory-shortage-analysis.xlsx

vendor-fulfillment-dashboard.xlsx

ticket-escalation-review.xlsx
```

Avoid:

```text
report-final-v2.xlsx

dashboard-new.xlsx

analysis-temp.xlsx
```

Reporting names should clearly communicate:

* reporting purpose
* operational focus
* intended audience

\---

# Workflow Artifact Naming Standards

Workflow artifacts should use:

* workflow-centered terminology
* lifecycle-oriented naming
* operational process language

Examples:

```text
ticket-escalation-workflow.drawio

inventory-replenishment-lifecycle.png

vendor-delay-escalation-flow.png
```

Workflow names should clearly communicate:

* workflow purpose
* operational sequence
* escalation relationships
* process ownership

\---

# Executive Reporting Terminology Standards

Executive reporting should maintain consistent leadership-oriented terminology.

Preferred section examples:

```text
Operational Summary

KPI Highlights

Operational Risks

Escalation Trends

Operational Recommendations

Leadership Considerations
```

Consistent terminology improves:

* executive readability
* reporting cohesion
* operational interpretation
* leadership communication

Avoid inconsistent section naming across reporting artifacts.

\---

# Analytical Integration Standards

Naming conventions should support:

* relational consistency
* analytical interoperability
* cross-system visibility
* reporting consistency
* enterprise integration

Naming should prioritize:

* business readability
* relational clarity
* stable references
* governance consistency

Examples:

```text
vendor\_id

location\_id

related\_ticket\_id
```

Preferred over:

```text
vendorNumber

loc

ticketRef
```

Consistent naming improves:

* operational traceability
* reporting quality
* subsystem interoperability
* enterprise maintainability

\---

# Naming Governance Principles

## Naming Drift Prevention Principle

Future ecosystem expansion should avoid:

* duplicate naming concepts
* inconsistent abbreviations
* mixed formatting styles
* synonym drift
* subsystem-local naming improvisation

Avoid:

```text
vendorNum

vendorID

supplier\_id

supp\_id
```

Preferred:

```text
vendor\_id
```

Only one canonical naming structure should exist for shared operational concepts.

\---

## Governance Enforcement Principle

Naming consistency is considered:

# enterprise governance

NOT:

# cosmetic formatting preference

All future subsystems, reporting artifacts, datasets, workflows, and analytical models should follow approved naming standards unless formally updated through governance review.

\---

## Expansion Alignment Principle

Future subsystem expansion should:

* inherit enterprise naming standards
* preserve subsystem consistency
* align with shared identifier standards
* support cross-system integration
* maintain reporting cohesion

Naming standards should scale with the ecosystem rather than fragment as new operational domains are introduced.

\---

# Governance Alignment

These standards align with:

* Project Governance Standards
* Remediation Standards
* Operational Severity Framework
* Enterprise System Map
* Operational Intelligence Lifecycle

Naming standards should remain consistent with all approved governance and architectural standards throughout the ecosystem.

\---

# Summary

The Naming Convention Standards establish the enterprise naming framework used throughout the Northstar Health Operations ecosystem.

By standardizing repository naming, subsystem naming, folder naming, dataset naming, field naming, identifier conventions, workflow naming, and reporting terminology, the ecosystem maintains consistency, readability, interoperability, and long-term architectural stability across all operational domains.

Naming consistency is treated as an enterprise governance responsibility that supports operational clarity, subsystem maintainability, cross-system integration, and sustainable ecosystem growth.

