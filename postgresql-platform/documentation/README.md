# PostgreSQL Platform Documentation

## Northstar Health Operations

---

**Primary Audience:** Contributors, operators, reviewers, and portfolio visitors using or evaluating the PostgreSQL platform

**Writing Layer:** Layer 2 — Operational / Analyst

**Architectural Purpose:** Defines the location for platform-specific setup, execution, troubleshooting, and operating guidance.

---

# Purpose

This directory contains platform-specific guidance and implementation traceability for operating and reviewing the PostgreSQL platform.

The platform root README defines the implementation boundary. This directory will hold supporting instructions that would make the root orientation unnecessarily detailed.

---

# Approved Documentation Scope

Approved documents may cover:

* local setup prerequisites
* environment configuration
* SQL client connection workflow
* create, load, validate, reset, and teardown procedures
* troubleshooting and recovery guidance
* implementation traceability

Documentation must reference the governing architecture rather than restating or redefining it.

Enterprise governance, logical design, relational design, and platform decisions remain under `organizational-architecture/`.

---

# Current Boundary

Issue #5 established this documentation boundary. Issue #28 added [Tier 1 PostgreSQL Implementation Contract](tier-1-postgresql-implementation-contract.md), which governs the physical types, constraint names, staged references, file responsibilities, validator boundaries, and documentation changes implemented through issues #29 and #30.

Detailed runbooks will continue to be added with the executable capabilities they describe.
