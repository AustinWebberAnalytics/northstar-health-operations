# Ticket Source Encoding Normalization Validation Evidence

## Northstar Enterprise

---

**Primary Audience:** Data engineers, analysts, subsystem maintainers, and reviewers evaluating completion of the Ticket source encoding-normalization boundary

**Writing Layer:** Layer 2 — Operational / Analyst

**Architectural Purpose:** Records the curated execution evidence proving that the authoritative Windows-1252 Ticket source can be reproducibly normalized to strict UTF-8 without changing source data, decoded text, CSV structure, or field values.

**Document Type:** Validation Evidence

**Authority Level:** Implementation Evidence

**Status:** Validation Passed — Issue #17

**Validation Date:** August 6, 2026

**Tested Repository Commit:** `fad09ec6d589770dccc2105e66a8188f445e19b4`

---

# Purpose

This artifact records successful runtime validation of the repository-controlled Ticket source encoding normalizer.

The evidence is curated. It does not contain generated CSV content, machine-specific paths, credentials, execution transcripts, or other local runtime artifacts.

---

# Validation Boundary

Validation was limited to converting the authoritative Ticket source from Windows-1252 to UTF-8.

The validated process:

* read `ticketing-system/datasets/data/tickets-v1.csv` as the authoritative source
* verified that the source did not pass strict UTF-8 decoding
* decoded the source as Windows-1252
* wrote a generated UTF-8 file without a byte-order mark
* preserved decoded Unicode text, CSV structure, and every parsed field value
* verified that the authoritative source remained unchanged
* wrote the output only under the ignored `postgresql-platform/migration-output/` boundary
* left the repository working tree clean

Validation did not correct Ticket values, reconcile references, approve mappings, create staging tables, load PostgreSQL, enable deferred foreign keys, or implement Tier 3 structures.

---

# Tested Configuration

| Configuration Item | Validated Value |
|---|---|
| Validation date | August 6, 2026 |
| Repository commit | [`fad09ec6`](https://github.com/AustinWebberAnalytics/northstar-health-operations/commit/fad09ec6d589770dccc2105e66a8188f445e19b4) |
| Python runtime | Python 3.14.6 |
| Authoritative source | `ticketing-system/datasets/data/tickets-v1.csv` |
| Source Git blob | `581493086343092974b8c772f771287e18fbb113` |
| Normalizer | `postgresql-platform/migrations/source-data/ticket-source-encoding/normalize-ticket-source-encoding.py` |
| Generated output | `postgresql-platform/migration-output/ticket-source-encoding/tickets-v1-utf8.csv` |
| Final repository state | Clean working tree |
| Generated-output state | Ignored and uncommitted |

---

# Observed Validation Results

**Result:** PASS

| Validation Measure | Observed Result |
|---|---:|
| Source encoding | Windows-1252 |
| Output encoding | UTF-8 without BOM |
| Data records | 15 |
| Columns | 20 |
| Em dashes preserved | 15 |
| Source bytes | 5,433 |
| Output bytes | 5,463 |
| Source SHA-256 | `7a5e70614d3d2389d481575785724f530a37d080edd8e32736072ac5b15e7d1e` |
| Output SHA-256 | `8d5aab522fc6a6aeb091ffe65de40878ac63caf39cac00d2c215accba8faf22e` |
| Strict UTF-8 validation | PASS |
| Unicode text equivalence | PASS |
| CSV structure and field-value equivalence | PASS |
| Authoritative source unchanged | PASS |
| Generated-output exclusion | PASS |
| Final working-tree check | PASS |

The normalizer ended with:

`TICKET SOURCE ENCODING NORMALIZATION: PASS`

Git identified the generated file through the scoped `migration-output/` ignore rule. A final `git status --short` returned no output.

---

# Issue #17 Acceptance Criteria

| Acceptance Criterion | Result | Evidence |
|---|---|---|
| The authoritative Ticket source is not modified. | PASS | The normalizer rehashed the source after output generation and returned `Authoritative source unchanged: PASS`; the final working tree remained clean. |
| The source encoding condition is verified before conversion. | PASS | The process rejected strict UTF-8 interpretation and decoded the source as Windows-1252. |
| A repository-controlled process converts the source from Windows-1252 to UTF-8. | PASS | The normalizer at the tested commit generated the approved UTF-8 migration input. |
| The process fails rather than double-converting an input that is already valid UTF-8. | PASS | The committed validation contract requires strict UTF-8 rejection before Windows-1252 conversion; the implementation was independently tested against an already-UTF-8 input before runtime approval. |
| The normalized output passes strict UTF-8 decoding. | PASS | Runtime result: `Strict UTF-8 validation: PASS`. |
| The normalized output contains no unapproved byte-order mark. | PASS | Runtime result identified the output as `UTF-8 without BOM`. |
| Decoded source and output Unicode text are equivalent. | PASS | Runtime result: `Unicode text equivalence: PASS`. |
| Header order, column count, record count, and every parsed field value are preserved. | PASS | Runtime result: 20 columns, 15 records, and `CSV structure and field-value equivalence: PASS`. |
| Source and output SHA-256 hashes and byte counts are reported. | PASS | Both identities are recorded in the observed-results table. |
| Generated output remains under the ignored migration-output boundary and uncommitted. | PASS | `git check-ignore -v` matched the scoped migration-output rule; the final tree was clean. |
| Execution instructions and pass or failure behavior are documented. | PASS | The Issue #17 migration procedure documents the command, validation contract, success result, and failure boundary. |
| Validation returns a clear pass or identifies the failed invariant. | PASS | The normalizer returned a clear overall pass after all invariants succeeded. |
| Completion evidence records the tested commit, source identity, output identity, and observed result. | PASS | This artifact records the tested commit, Git blob, SHA-256 identities, byte counts, structural counts, and validation result. |
| Completion evidence is linked through a governed validation artifact. | PASS | This repository-controlled artifact and its commit history provide the durable completion record. |

---

# Relevant Records

| Responsibility | Commit or Record |
|---|---|
| Ticket encoding normalizer implementation | [`0fb5ead`](https://github.com/AustinWebberAnalytics/northstar-health-operations/commit/0fb5eade534568047fba51e03d5a0f62a805293f) |
| Ticket encoding normalization procedure | [`24e609f`](https://github.com/AustinWebberAnalytics/northstar-health-operations/commit/24e609f78ef94ea7551b01cb607b11af800a0b02) |
| Tested Issue #17 platform boundary | [`fad09ec`](https://github.com/AustinWebberAnalytics/northstar-health-operations/commit/fad09ec6d589770dccc2105e66a8188f445e19b4) |
| Evidence commit history | [Ticket source encoding validation history](https://github.com/AustinWebberAnalytics/northstar-health-operations/commits/main/postgresql-platform/validation/source-data/ticket-source-encoding-validation.md) |
| Migration procedure | [Ticket Source Encoding Normalization](../../migrations/source-data/ticket-source-encoding/README.md) |
| Completion issue | [Issue #17 — Normalize the Ticket source encoding](https://github.com/AustinWebberAnalytics/northstar-health-operations/issues/17) |
| Parent prerequisite issue | [Issue #16 — Resolve migration and reconciliation prerequisites](https://github.com/AustinWebberAnalytics/northstar-health-operations/issues/16) |

---

# Final Determination

**Validation Result:** PASS

The repository-controlled normalizer reproducibly converts the authoritative Windows-1252 Ticket source into strict UTF-8 without a byte-order mark. It preserves all 15 records, all 20 columns, every parsed field value, and all decoded Unicode text while leaving the authoritative source unchanged.

The generated output remains local, ignored, and uncommitted. Issue #17 is complete at the encoding-normalization boundary. Ticket data correction, reference reconciliation, staging, PostgreSQL loading, deferred foreign-key enforcement, and Tier 3 implementation remain governed by separate work.
