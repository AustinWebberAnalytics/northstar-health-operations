# Ticket Location Mapping Validation Evidence

## Northstar Enterprise

---

**Primary Audience:** Data engineers, analysts, subsystem maintainers, and reviewers evaluating completion of the Ticket Location mapping boundary

**Writing Layer:** Layer 2 — Operational / Analyst

**Architectural Purpose:** Records the curated execution evidence proving that every current Ticket `requesting_location` value resolves through the four approved one-to-one mappings while preserving the original Ticket data and retaining the source label for traceability.

**Document Type:** Validation Evidence

**Authority Level:** Implementation Evidence

**Status:** Validation Passed — Issue #18

**Validation Date:** August 7, 2026

**Tested Repository Commit:** `a5b2a8b85a117e8337c3249ae0d14547e1cb9cc9`

---

# Purpose

This artifact records successful runtime validation of the repository-controlled Ticket Location mapping process.

The evidence is curated. It does not contain generated CSV content, machine-specific paths, credentials, execution transcripts, or other local runtime artifacts.

---

# Validation Boundary

Validation was limited to applying the four approved Ticket Location mappings to the normalized Issue #17 Ticket output.

The validated process:

* read the normalized Ticket source as strict UTF-8 without a byte-order mark
* verified the committed mapping artifact against the four approved Issue #18 decisions
* confirmed that all mapped identifiers exist in governed operational Location identifier evidence
* mapped every current `requesting_location` value to exactly one approved `location_id`
* retained `requesting_location` and added `location_id`
* preserved every original Ticket column and field value
* verified that the normalized Ticket source remained unchanged
* wrote generated mapped output only under the ignored `postgresql-platform/migration-output/` boundary
* left the repository working tree clean

Validation did not modify the raw or normalized Ticket sources, reconcile owner names, resolve orphaned Ticket references, create staging tables, load PostgreSQL, enable deferred foreign keys, create Location records, or implement Tier 3 structures.

---

# Approval and Evidence Basis

Northstar does not yet contain a populated Location registry storing both descriptive names and governed identifiers. The four pairs were approved through Issue #18 using:

* the Phase 4 Data Reconciliation Readiness Review
* the Cross-System Identifier Dictionary
* the governed `location_id` values present in current operational datasets
* the repository-controlled mapping decision recorded on August 7, 2026

The validator confirmed that all four approved identifiers occur in the governed Location identifier evidence. This artifact does not claim that a separate name-to-identifier registry already exists.

---

# Approved Mappings

| Ticket `requesting_location` | Governed `location_id` |
|---|---|
| Cary Distribution Hub 01 | `LOC-CARY-HUB-01` |
| Durham Outpatient Clinic 07 | `LOC-DURHAM-07` |
| Raleigh Specialty Clinic 03 | `LOC-RALEIGH-03` |
| Wake Forest Clinic 11 | `LOC-WAKEFOREST-11` |

---

# Tested Configuration

| Configuration Item | Validated Value |
|---|---|
| Validation date | August 7, 2026 |
| Repository commit | [`a5b2a8b`](https://github.com/AustinWebberAnalytics/northstar-health-operations/commit/a5b2a8b85a117e8337c3249ae0d14547e1cb9cc9) |
| Python runtime | Python 3.14.6 |
| Normalized Ticket input | `postgresql-platform/migration-output/ticket-source-encoding/tickets-v1-utf8.csv` |
| Mapping artifact | `postgresql-platform/migrations/source-data/ticket-location-mapping/ticket-location-mapping.csv` |
| Validator and mapper | `postgresql-platform/migrations/source-data/ticket-location-mapping/validate-ticket-location-mapping.py` |
| Location identifier evidence | `inventory-operations/datasets/data/location-inventory.csv` |
| Generated mapped output | `postgresql-platform/migration-output/ticket-location-mapping/tickets-v1-location-mapped.csv` |
| Final repository state | Clean working tree |
| Generated-output state | Ignored and uncommitted |

---

# Observed Validation Results

**Result:** PASS

| Validation Measure | Observed Result |
|---|---:|
| Data records | 15 |
| Source columns preserved | 20 |
| Output columns | 21 |
| Distinct `requesting_location` values | 4 |
| Approved one-to-one mappings | 4 |
| Governed `location_id` values in evidence | 4 |
| Unmatched values | 0 |
| Ambiguous values | 0 |
| Original `requesting_location` retained | PASS |
| All original Ticket fields and values preserved | PASS |
| Generated output strict UTF-8 without BOM | PASS |
| Normalized source unchanged | PASS |
| Generated-output exclusion | PASS |
| Final working-tree check | PASS |

| File Identity | SHA-256 |
|---|---|
| Normalized Ticket source | `8d5aab522fc6a6aeb091ffe65de40878ac63caf39cac00d2c215accba8faf22e` |
| Approved mapping artifact | `93395837caedb202cc62bc78f4113529c1815a5aab168f7c0f7e42a9c07d1b89d0` |
| Generated mapped output | `1c61c53c359cac43e11d683a08be618d64661febe62a1096b4e5bf575121334f` |

The validator ended with:

`TICKET LOCATION MAPPING VALIDATION: PASS`

Git identified the generated mapped file through the scoped `migration-output/` ignore rule. A final `git status --short` returned no output.

---

# Issue #18 Acceptance Criteria

| Acceptance Criterion | Result | Evidence |
|---|---|---|
| Every distinct Ticket `requesting_location` value is profiled from the normalized Ticket source. | PASS | Runtime validation found four distinct values across 15 records. |
| Each candidate mapping is compared against the authoritative Location evidence available at this boundary. | PASS | All four identifiers were confirmed in governed operational Location identifier evidence; the absence of a populated name-ID registry is explicitly recorded. |
| `Cary Distribution Hub 01` is formally approved or rejected for `LOC-CARY-HUB-01`. | PASS | Formally approved through Issue #18 and present in the committed mapping artifact. |
| `Durham Outpatient Clinic 07` is formally approved or rejected for `LOC-DURHAM-07`. | PASS | Formally approved through Issue #18 and present in the committed mapping artifact. |
| `Raleigh Specialty Clinic 03` is formally approved or rejected for `LOC-RALEIGH-03`. | PASS | Formally approved through Issue #18 and present in the committed mapping artifact. |
| `Wake Forest Clinic 11` is formally approved or rejected for `LOC-WAKEFOREST-11`. | PASS | Formally approved through Issue #18 and present in the committed mapping artifact. |
| Every approved source value maps to exactly one governed Location identifier. | PASS | Four distinct values resolved through four one-to-one mappings with zero ambiguity. |
| No Location identifier is invented or changed to force a match. | PASS | The mapping artifact uses only the four governed identifiers confirmed in operational evidence. |
| Unmatched or ambiguous values are routed to exception reporting rather than silently loaded. | PASS | The committed procedure and validator block mapped-output generation and create ignored exception output for either condition; pre-commit negative tests confirmed rejection behavior. |
| The final mapping is stored in a repository-controlled artifact. | PASS | The approved mapping is committed as `ticket-location-mapping.csv`. |
| The mapping process is repeatable and usable by the migration pipeline. | PASS | The committed standard-library Python validator reproduced the approved mapping and returned a clear overall pass. |
| The original `requesting_location` value remains available for traceability. | PASS | Runtime validation confirmed that the column was retained and `location_id` was added without changing original fields. |
| Approval evidence is linked through a commit, pull request, or governed decision artifact. | PASS | The approval comment, tested implementation commit, and this repository-controlled evidence artifact provide durable traceability. |
| Strict Ticket Location foreign-key enforcement remains deferred until migration and validation are complete. | PASS | No PostgreSQL object or deferred foreign-key state changed under Issue #18. |

---

# Relevant Records

| Responsibility | Commit or Record |
|---|---|
| Approved Ticket Location mapping artifact | [`8b63ad1`](https://github.com/AustinWebberAnalytics/northstar-health-operations/commit/8b63ad1a67c78f682f04cb106573db95aef3970c) |
| Repeatable validator and mapper | [`d79c72f`](https://github.com/AustinWebberAnalytics/northstar-health-operations/commit/d79c72f3ae5bc7abffa26f7cca189c5b55d740ae) |
| Mapping procedure and decision boundary | [`8b67734`](https://github.com/AustinWebberAnalytics/northstar-health-operations/commit/8b67734ee86f290f7f95e40e410f84827102a502) |
| Tested Issue #18 platform boundary | [`a5b2a8b`](https://github.com/AustinWebberAnalytics/northstar-health-operations/commit/a5b2a8b85a117e8337c3249ae0d14547e1cb9cc9) |
| Evidence commit history | [Ticket Location mapping validation history](https://github.com/AustinWebberAnalytics/northstar-health-operations/commits/main/postgresql-platform/validation/source-data/ticket-location-mapping-validation.md) |
| Migration procedure | [Ticket Location Mapping](../../migrations/source-data/ticket-location-mapping/README.md) |
| Completion issue | [Issue #18 — Approve the Ticket Location mappings](https://github.com/AustinWebberAnalytics/northstar-health-operations/issues/18) |
| Parent prerequisite issue | [Issue #16 — Resolve migration and reconciliation prerequisites](https://github.com/AustinWebberAnalytics/northstar-health-operations/issues/16) |

---

# Final Determination

**Validation Result:** PASS

The repository-controlled mapping process resolved every current Ticket `requesting_location` value through the four approved one-to-one mappings. It preserved all 15 records, all 20 original columns and field values, retained the original source label, added the governed `location_id`, and produced strict UTF-8 mapped output.

The generated output remains local, ignored, and uncommitted. Issue #18 is complete at the Ticket Location mapping boundary. Ticket owner reconciliation, orphan-reference resolution, staging, PostgreSQL loading, deferred foreign-key enforcement, and Tier 3 implementation remain governed by separate work.
