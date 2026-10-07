# Shipment Replenishment Allocation Rule Validation Evidence

## Northstar Enterprise

---

**Primary Audience:** Data engineers, analysts, inventory-operations maintainers, and reviewers evaluating completion of the Shipment Replenishment Allocation rule boundary

**Writing Layer:** Layer 2 — Operational / Analyst

**Architectural Purpose:** Records the curated execution evidence proving that the approved allocation timing and aggregate quantity-ceiling rules behave as intended without inventing operational allocation history.

**Document Type:** Validation Evidence

**Authority Level:** Implementation Evidence

**Status:** Validation Passed — Issue #22

**Validation Date:** October 7, 2026

**Tested Repository Commit:** `b49f7643823aaa3517bcd08df0cdf0b674889ccf`

---

# Purpose

This artifact records successful runtime validation of the repository-controlled Shipment Replenishment Allocation timing and quantity-ceiling model.

The evidence is curated. It does not contain generated CSV content, machine-specific paths, credentials, execution transcripts, or other local runtime artifacts.

---

# Validation Boundary

Validation was limited to profiling the six governed Shipment records, five governed Replenishment records, and ten controlled allocation-rule scenarios.

The validated process:

* required known Shipment `received_quantity` before allocation
* required known Replenishment `approved_quantity` before allocation
* required positive `allocated_quantity`
* capped aggregate Shipment allocations at `received_quantity`
* capped aggregate Replenishment allocations at `approved_quantity`
* allowed partial receipts to be allocated up to the quantity actually received
* excluded Shipment `ordered_quantity` and Replenishment `requested_quantity` as allocation ceilings
* prohibited status values from substituting for missing governing quantities
* rejected duplicate Shipment/Replenishment pairs
* rejected parent-quantity reductions that would leave allocations above the revised ceiling
* exercised ten controlled scenarios, including eight expected blocked scenarios, with zero unexpected outcomes
* created zero operational allocation records
* wrote the generated scenario report only under the ignored `postgresql-platform/migration-output/` boundary
* left the repository working tree clean

Validation did not infer Shipment Replenishment Allocation relationships, modify either governed parent source, create Tier 3 DDL, implement triggers or supporting indexes, load PostgreSQL, enable deferred foreign keys, or begin later integrity-enforcement work.

---

# Tested Configuration

| Configuration Item | Validated Value |
|---|---|
| Validation date | October 7, 2026 |
| Repository commit | [`b49f764`](https://github.com/AustinWebberAnalytics/northstar-health-operations/commit/b49f7643823aaa3517bcd08df0cdf0b674889ccf) |
| Python runtime | Python 3.14.6 |
| Shipment source | `inventory-operations/datasets/data/vendor-shipments.csv` |
| Replenishment source | `inventory-operations/datasets/data/replenishment-events.csv` |
| Rule artifact | `postgresql-platform/migrations/source-data/shipment-replenishment-allocation-rules/shipment-replenishment-allocation-rules.csv` |
| Validator | `postgresql-platform/migrations/source-data/shipment-replenishment-allocation-rules/validate-shipment-replenishment-allocation-rules.py` |
| Generated scenario report | `postgresql-platform/migration-output/shipment-replenishment-allocation-rules/shipment-replenishment-allocation-rule-validation.csv` |
| Final repository state | Clean working tree |
| Generated-output state | File ignored and uncommitted |

---

# Observed Validation Results

**Result:** PASS

| Validation Measure | Observed Result |
|---|---:|
| Shipment records profiled | 6 |
| Replenishment records profiled | 5 |
| Shipments with known `received_quantity` | 4 |
| Shipments with unknown `received_quantity` | 2 |
| Replenishments with known `approved_quantity` | 5 |
| Replenishments with unknown `approved_quantity` | 0 |
| Controlled rule scenarios | 10 |
| Expected blocked scenarios | 8 |
| Unexpected scenario outcomes | 0 |
| Operational allocation records created | 0 |
| Approved timing rules retained | PASS |
| Approved aggregate ceilings retained | PASS |
| Planning values excluded as ceilings | PASS |
| Status substitution prohibited | PASS |
| Parent quantity reductions validated | PASS |
| Generated output strict UTF-8 without BOM | PASS |
| All governed inputs unchanged | PASS |
| Generated-output exclusion | PASS |
| Final working-tree check | PASS |

| File Identity | SHA-256 |
|---|---|
| Shipment source | `44407a691f967ed4884dccdcab9c964e410e955d6119b6817be59daaec8d04df` |
| Replenishment source | `3d5f8cdf185f0e014ddd5fd3db55f024bb411d02ee3fe4eb2c5d11b6974fac39` |
| Decision-rule artifact | `153ef27addf81350f74c574bdca5009965ffb870ea0b0d532f2eab70117db9ac` |
| Generated scenario report | `31e088674b8b48f45a848ec72a0698b55614294930ab46897fc8a37b3a97b19e` |

The governed-input hashes reflect the Windows checkout used for runtime validation. The validator confirmed that every governed input remained byte-for-byte unchanged during execution.

The validator ended with:

`SHIPMENT REPLENISHMENT ALLOCATION RULE VALIDATION: PASS`

Git identified the generated report through the scoped `migration-output/` ignore rule. A final `git status --short` returned no output.

---

# Issue #22 Acceptance Criteria

| Acceptance Criterion | Result | Evidence |
|---|---|---|
| Shipment allocation timing is explicitly documented and approved. | PASS | Allocation requires known Shipment `received_quantity`. |
| Replenishment allocation timing is explicitly documented and approved. | PASS | Allocation requires known Replenishment `approved_quantity`. |
| Shipment `received_quantity` is documented as the aggregate Shipment ceiling. | PASS | Controlled Shipment aggregate scenarios enforce the received ceiling. |
| Replenishment `approved_quantity` is documented as the aggregate Replenishment ceiling. | PASS | Controlled Replenishment aggregate scenarios enforce the approved ceiling. |
| Ordered and requested quantities are explicitly excluded as allocation ceilings. | PASS | Planning-value substitution is prohibited and validated. |
| Partial-receipt allocation behavior is documented. | PASS | Partial receipts may be allocated only up to quantity actually received. |
| Status values cannot substitute for missing governing quantities. | PASS | Missing quantities block allocation regardless of status. |
| Nonpositive and duplicate allocations are rejected. | PASS | Controlled zero, negative, and duplicate scenarios were blocked. |
| Aggregate over-allocation is rejected for both parents. | PASS | Both Shipment and Replenishment over-ceiling scenarios were blocked. |
| Parent-quantity reductions cannot leave invalid aggregate allocations. | PASS | Invalid parent reductions were rejected. |
| No allocation rows are inferred from candidate source relationships. | PASS | Zero operational allocation records were created. |
| Current parent sources remain unchanged. | PASS | Source hashes were preserved before and after execution. |
| The final decision is stored in a repository-controlled artifact. | PASS | The rule matrix, procedure, and validator are committed. |
| Runtime validation evidence and completion commits are linked. | PASS | The tested commit, this validation artifact, and Issue #22 provide durable traceability. |

---

# Relevant Records

| Responsibility | Commit or Record |
|---|---|
| Approved rule matrix, validator, and procedure | [`b49f764`](https://github.com/AustinWebberAnalytics/northstar-health-operations/commit/b49f7643823aaa3517bcd08df0cdf0b674889ccf) |
| Evidence commit history | [Allocation-rule validation history](https://github.com/AustinWebberAnalytics/northstar-health-operations/commits/main/postgresql-platform/validation/source-data/shipment-replenishment-allocation-rule-validation.md) |
| Migration procedure | [Shipment Replenishment Allocation Rules](../../migrations/source-data/shipment-replenishment-allocation-rules/README.md) |
| Completion issue | [Issue #22 — Approve allocation timing and quantity-ceiling rules](https://github.com/AustinWebberAnalytics/northstar-health-operations/issues/22) |
| Parent prerequisite issue | [Issue #16 — Resolve migration and reconciliation prerequisites](https://github.com/AustinWebberAnalytics/northstar-health-operations/issues/16) |

---

# Final Determination

**Validation Result:** PASS

The repository-controlled validator proved the approved Shipment Replenishment Allocation timing and aggregate ceiling model across the complete current parent profile and ten controlled scenarios. All eight expected invalid scenarios were blocked, no unexpected outcome occurred, and no operational allocation history was created.

All governed inputs remained unchanged. The generated scenario report remains local, ignored, and uncommitted. Issue #22 is complete at the allocation-rule decision boundary. Tier 3 DDL, PostgreSQL loading, aggregate-trigger implementation, and later integrity enforcement remain governed by separate work.
