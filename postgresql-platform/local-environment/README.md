# Local Environment

## Northstar Health Operations

---

**Primary Audience:** Data engineers, contributors, and reviewers running the Northstar PostgreSQL platform locally

**Writing Layer:** Layer 2 — Operational / Analyst

**Architectural Purpose:** Defines the boundary for the reproducible PostgreSQL 18 runtime and its local start, reset, and teardown controls.

---

# Purpose

This directory will contain the approved configuration required to run PostgreSQL 18 locally through Docker Compose.

It owns runtime configuration. It does not own the database definition, data migration logic, validation queries, or enterprise data.

---

# Approved Responsibilities

Future approved artifacts may include:

* a major-version-pinned PostgreSQL 18 Docker Compose service
* a committed `.env.example` with non-secret configuration names
* documented SQL client connection guidance
* explicit local start, reset, and teardown controls
* one named PostgreSQL data volume

The local `.env`, credentials, data volume, logs, and generated runtime files must remain uncommitted.

---

# Lifecycle Boundaries

Starting the environment must start PostgreSQL only. It must not automatically create schemas, load source data, or suppress migration failures.

Reset must be an explicit destructive operation limited to the local development database.

Teardown must distinguish between stopping services and deleting the local data volume. Persistent storage must not be deleted through an implicit default action.

---

# Current Boundary

Issue #5 creates this ownership boundary only. Docker Compose, `.env.example`, and executable lifecycle controls require later approval.
