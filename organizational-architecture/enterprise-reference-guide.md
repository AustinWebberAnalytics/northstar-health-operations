# Northstar Health Operations

## Enterprise Reference Guide

---

**Primary Audience:** Portfolio reviewers, hiring managers, collaborators, and technical readers seeking a concise repository orientation

**Writing Layer:** Layer 1 — Reader-Facing

**Architectural Purpose:** Provides a concise map of the Northstar ecosystem, its operating domains, governance structure, architecture sequence, and current development stage.

---

# What Northstar Is

Northstar Health Operations is a governance-first operational intelligence ecosystem built to simulate how a real organization coordinates work across connected business functions.

The repository is not centered on one dashboard or one analysis. It models an enterprise environment where datasets, workflows, reporting, governance, and relational architecture must remain consistent as the system grows.

Northstar was built to feel like a company someone could walk into on Monday morning.

---

# Operational Domains

The current ecosystem contains four primary operational domains:

- **Ticketing System** — incident intake, ownership, prioritization, escalation, SLA tracking, and resolution
- **Inventory Operations** — stock position, replenishment, shortages, discrepancies, and inventory continuity
- **Vendor Performance** — shipments, fulfillment, SLA evaluation, corrective action, and supplier accountability
- **Workforce Coordination** — employee capacity, assignments, schedules, workload, and workforce escalation

Each domain maintains its own datasets, documentation, reporting, workflows, and improvement artifacts while participating in one governed enterprise architecture.

---

# Organizational Architecture

The [Organizational Architecture](README.md) area governs how the ecosystem is structured and changed.

It contains:

- repository-wide governance standards
- naming and identifier rules
- the enterprise system map
- the enterprise object and relational models
- the enterprise logical model
- the relational engineering foundation
- the platform-neutral relational schema
- the approved PostgreSQL platform decision
- architecture reviews and validation records

---

# Architecture Sequence

```text
Enterprise System Map
        ↓
Enterprise Object Model
        ↓
Enterprise Relational Model
        ↓
Enterprise Logical Model
        ↓
Enterprise Identifier Governance Review
        ↓
Enterprise Relational Foundation
        ↓
Enterprise Relational Schema
        ↓
Enterprise Database Platform Decision
        ↓
SQL Implementation
```

Each layer has a distinct responsibility. Downstream documents implement upstream decisions rather than redefining them.

---

# Current Development State

The conceptual architecture, identifier baseline, Enterprise Relational Foundation, complete Enterprise Relational Schema, and Enterprise Database Platform Decision are approved and locked.

All six dependency tiers are complete. PostgreSQL 18 is the approved platform, using one database with six native schemas.

SQL implementation has not started. Physical PostgreSQL DDL, migration, trigger, index, and validation work is the next controlled initiative.

---

# Reporting Philosophy

Northstar reporting prioritizes:

- clear operational meaning
- traceable source data
- consistent KPI definitions
- executive readability
- practical decision support
- explicit limits and assumptions

Reporting artifacts sit downstream of governance, architecture, datasets, and validation. A dashboard or report does not become the source of truth for the business facts it summarizes.

---

# Recommended Starting Points

For a quick orientation:

1. [Enterprise Operations Brief](system-design/enterprise-operations-brief.md)
2. [Enterprise System Map](system-design/enterprise-system-map.md)
3. [Enterprise Object Model](system-design/enterprise-object-model.md)
4. [Enterprise Relational Schema](system-design/enterprise-relational-schema.md)
5. [Enterprise Database Platform Decision](system-design/enterprise-database-platform-decision.md)

For repository standards:

1. [Project Governance Standards](governance/project-governance-standards.md)
2. [Naming Convention Standards](governance/naming-convention-standards.md)
3. [Cross-System Identifier Dictionary](governance/cross-system-identifier-dictionary.md)

---

# Portfolio Significance

Northstar demonstrates:

- enterprise systems thinking
- operational analytics
- data governance
- relational modeling
- process improvement
- cross-functional coordination
- reporting and KPI development
- documentation design
- architecture reconciliation
- disciplined change control
