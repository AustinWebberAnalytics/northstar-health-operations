# System Design

## Northstar Health Operations

---
**Primary Audience:** Portfolio reviewers, Northstar architects, data engineers, subsystem maintainers, and technical reviewers

**Writing Layer:** Layer 1 — Reader-Facing

**Architectural Purpose:** Provides the navigable index to the current enterprise architecture and relational-design baseline.

---
# Purpose

System Design explains how Northstar is organized as one operational enterprise.

The documents in this folder move from organizational context to conceptual architecture, then into logical and relational design. Their order matters.

---
# Architecture Sequence

## 1. [Enterprise Operations Brief](enterprise-operations-brief.md)

Explains the simulated organization, its operating functions, and the purpose of the portfolio environment.

## 2. [Enterprise System Map](enterprise-system-map.md)

Defines enterprise domains, subsystem boundaries, and the major operational capabilities represented in the repository.

## 3. [Enterprise Object Model](enterprise-object-model.md)

Defines the 17 canonical business objects, their ownership, identity, classification, and governed relationship boundaries.

## 4. [Enterprise Relational Model](enterprise-relational-model.md)

Defines the authoritative business relationships between the governed objects.

## 5. [Enterprise Logical Model](enterprise-logical-model.md)

Defines logical attributes, canonical identifiers, business candidate keys, integrity rules, and associative-entity requirements.

## 6. [Enterprise Relational Foundation](enterprise-relational-foundation.md)

Defines database philosophy, key strategy, dependency tiers, constraint philosophy, migration approach, and platform boundaries.

## 7. [Enterprise Relational Schema](enterprise-relational-schema.md)

Defines the approved platform-neutral schema specification. Tiers 0–5 are complete and locked, including the ordered terminal dependency between Corrective Action and Assignment Corrective Action.

## 8. [Enterprise Database Platform Decision](enterprise-database-platform-decision.md)

Approves PostgreSQL 18, native schema namespacing, physical type mapping, universal `ON DELETE RESTRICT`, enforcement boundaries, and the local implementation environment.

## 9. [Operational Intelligence Lifecycle](operational-intelligence-lifecycle.md)

Explains how operational data moves from source activity through validation, analysis, reporting, and decision support.

---
# Current Engineering Boundary

No SQL DDL has been approved yet.

The Enterprise Relational Schema and Enterprise Database Platform Decision are approved and locked. PostgreSQL 18, native domain schemas, physical type mapping, and universal `ON DELETE RESTRICT` now form the implementation baseline.

The next controlled step is physical table DDL and migration design.

---
# Archive

The [archive](archive/) preserves superseded architecture briefs. Archived material is historical context, not the current baseline.

