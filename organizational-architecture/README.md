# Organizational Architecture

## Northstar Health Operations

---

**Primary Audience:** Portfolio reviewers, Northstar architects, subsystem maintainers, data engineers, and future contributors

**Writing Layer:** Layer 1 — Reader-Facing

**Architectural Purpose:** Serves as the front door to the governance, system-design, and review artifacts that define how Northstar is structured, controlled, and implemented.

---

# Purpose

Organizational Architecture is the control center for the Northstar ecosystem.

It defines:

- what enterprise objects exist
- how those objects relate
- which identifiers are authoritative
- how relational design is derived
- how repository standards are enforced
- how major architecture decisions are reviewed and locked

Northstar is not a collection of isolated projects. It is a governed operational environment designed so that a reader could understand how the organization works, how its information connects, and how its systems should be built.

---

# Authority Hierarchy

```text
Governance
    ↓
Enterprise Architecture
    ↓
Logical and Relational Design
    ↓
Subsystem and Dataset Implementation
    ↓
Analysis, Reporting, and Executive Communication
```

When artifacts conflict, the newest approved document at the highest applicable authority level controls.

Historical reviews explain how decisions were reached. They do not override the current approved baseline.

---

# Directory Guide

## [Governance](governance/README.md)

Repository-wide rules and authoritative decision records.

Key artifacts include:

- Project Governance Standards
- Naming Convention Standards
- Cross-System Identifier Dictionary
- Enterprise Identifier Governance Review
- Operational Severity Framework
- Remediation Standards

## [System Design](system-design/README.md)

The current enterprise architecture and relational-design baseline.

Key artifacts include:

- Enterprise Operations Brief
- Enterprise System Map
- Enterprise Object Model
- Enterprise Relational Model
- Enterprise Logical Model
- Enterprise Relational Foundation
- Enterprise Relational Schema
- Operational Intelligence Lifecycle

## [Reviews](reviews/README.md)

Historical reviews, architecture reconciliations, and validation records.

Phase 2 material documents repository standardization and subsystem remediation. Phase 3 material documents conceptual architecture formation. Phase 4 reviews document the reconciliation required before SQL implementation.

---

# Recommended Reading Order

1. [Enterprise Operations Brief](system-design/enterprise-operations-brief.md)
2. [Enterprise System Map](system-design/enterprise-system-map.md)
3. [Enterprise Object Model](system-design/enterprise-object-model.md)
4. [Enterprise Relational Model](system-design/enterprise-relational-model.md)
5. [Enterprise Logical Model](system-design/enterprise-logical-model.md)
6. [Cross-System Identifier Dictionary](governance/cross-system-identifier-dictionary.md)
7. [Enterprise Identifier Governance Review](governance/enterprise-identifier-governance-review.md)
8. [Enterprise Relational Foundation](system-design/enterprise-relational-foundation.md)
9. [Enterprise Relational Schema](system-design/enterprise-relational-schema.md)

For a shorter repository-wide orientation, use the [Enterprise Reference Guide](enterprise-reference-guide.md).

---

# Current State

The conceptual architecture, identifier baseline, Enterprise Relational Foundation, and complete Enterprise Relational Schema are approved and locked.

All six dependency tiers—Tier 0 through Tier 5—are complete. The approved schema governs 17 canonical enterprise objects and 4 associative entities.

SQL implementation has not started. The next controlled step is target-platform and implementation-planning review, followed by governed DDL and migration work.

---

# Change-Control Rule

Do not edit one architecture artifact in isolation when the change affects another authority layer.

A change to an object, identifier, relationship, attribute, key, or constraint must be traced through every affected document before the new baseline is locked.
