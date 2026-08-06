# Ticket Source Encoding Normalization

## Northstar Enterprise

---

**Primary Audience:** Data engineers, analysts, subsystem maintainers, and reviewers preparing the Ticket source for governed migration

**Writing Layer:** Layer 2 — Operational / Analyst

**Architectural Purpose:** Defines the controlled process that converts the authoritative Windows-1252 Ticket source into a generated UTF-8 migration input without changing source data or field values.

**Document Type:** Migration Procedure

**Authority Level:** Approved Issue #17 Implementation

**Status:** Implementation Pending Runtime Validation

**Depends On:** Phase 4 Data Reconciliation Readiness Review, Enterprise Relational Foundation, Enterprise Database Platform Decision, and PostgreSQL Platform Migration Boundary

---

# Purpose

The Ticket source must be normalized to UTF-8 before type validation, reconciliation, staging, or PostgreSQL loading.

The repository-controlled normalizer reads the authoritative Windows-1252 file, generates a UTF-8 copy without a byte-order mark, and fails if the decoded text or parsed CSV values change.

---

# Governed Files

| Responsibility | Path |
|---|---|
| Authoritative source | `ticketing-system/datasets/data/tickets-v1.csv` |
| Normalization process | `postgresql-platform/migrations/source-data/ticket-source-encoding/normalize-ticket-source-encoding.py` |
| Generated migration input | `postgresql-platform/migration-output/ticket-source-encoding/tickets-v1-utf8.csv` |

The source file remains authoritative and must not be edited by this process. The generated output is reproducible local migration input. It is excluded from version control by `postgresql-platform/.gitignore`.

---

# Runtime Requirement

Use Python 3.10 or newer. The process uses only the Python standard library and does not install packages or connect to PostgreSQL.

---

# Execute the Normalization

From the repository root:

```powershell
python postgresql-platform/migrations/source-data/ticket-source-encoding/normalize-ticket-source-encoding.py
```

If Windows uses the Python launcher instead of the `python` command:

```powershell
py -3 postgresql-platform/migrations/source-data/ticket-source-encoding/normalize-ticket-source-encoding.py
```

The process may be rerun. A successful run atomically replaces the prior generated output at the same ignored path.

---

# Validation Contract

Before reporting success, the normalizer must verify:

* the source exists and does not already pass strict UTF-8 decoding
* the source decodes strictly as Windows-1252
* the generated output decodes strictly as UTF-8
* the generated output contains no UTF-8 byte-order mark
* decoded source text and generated UTF-8 text are identical
* header order, column count, record count, and every parsed field value are identical
* the authoritative source SHA-256 hash is unchanged before and after execution
* the output remains inside `postgresql-platform/migration-output/`

Success ends with:

```text
TICKET SOURCE ENCODING NORMALIZATION: PASS
```

The result also reports source and output paths, encodings, byte counts, SHA-256 hashes, data-record count, column count, and preserved em-dash count.

Any failed invariant returns a nonzero exit code and identifies the reason. A failed run does not authorize use of an existing generated file from an earlier run.

---

# Implementation Boundary

This process changes encoding only.

It does not:

* modify or replace the authoritative Ticket source
* correct Ticket field values
* approve Location mappings
* reconcile owner names
* resolve orphaned references
* create staging tables
* load data into PostgreSQL
* enable deferred foreign keys
* implement Tier 3 DDL

The generated UTF-8 file becomes eligible for the next governed reconciliation step only after Issue #17 runtime validation and completion evidence are approved.
