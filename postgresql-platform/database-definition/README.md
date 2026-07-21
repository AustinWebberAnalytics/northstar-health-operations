# Database Definition

## Northstar Health Operations

---

**Primary Audience:** Northstar architects, data engineers, and reviewers implementing the approved enterprise relational schema

**Writing Layer:** Layer 2 — Operational / Architectural

**Architectural Purpose:** Defines the authoritative desired-state SQL boundary and its dependency-ordered organization.

---

# Purpose

This directory contains the SQL that defines the approved desired state of the Northstar PostgreSQL database.

The definition must remain traceable to the locked Enterprise Relational Schema and Enterprise Database Platform Decision. It may implement approved architecture but may not reinterpret it.

---

# Planned Structure

```text
database-definition/
├── README.md
├── schema-namespaces/
├── tier-0/
├── tier-1/
├── tier-2/
├── tier-3/
├── tier-4/
├── tier-5/
├── supporting-indexes/
└── cross-table-integrity/
```

Each leaf directory will be created with its first approved SQL artifact.

---

# Controlled Build Order

1. `schema-namespaces/`
2. `tier-0/`
3. `tier-1/`
4. `tier-2/`
5. `tier-3/`
6. `tier-4/`
7. `tier-5/`
8. `supporting-indexes/`
9. `cross-table-integrity/`

Tier 5 retains its approved internal exception: Corrective Action must be created before Assignment Corrective Action.

Files must be invoked through an explicit approved sequence. The implementation must not execute files through an unordered wildcard or assume that filename sorting alone establishes governance.

---

# Ownership Boundaries

This directory owns:

* native schema namespace creation
* Tier 0–5 table definitions
* approved primary keys, foreign keys, uniqueness rules, and row-level constraints
* supporting indexes
* approved cross-table integrity functions and triggers

This directory does not own:

* Docker runtime configuration
* source-data normalization or correction
* data loading and migration exceptions
* generated validation output
* future database-change history

---

# Current Boundary

Issue #7 introduces the repository-controlled creation of the six approved schema namespaces under `schema-namespaces/`.

No table, role, grant, constraint, function, trigger, view, index, data, or `search_path` change is authorized through the namespace implementation. Tier 0–5 table definitions and every later database object require their own governed issues.
