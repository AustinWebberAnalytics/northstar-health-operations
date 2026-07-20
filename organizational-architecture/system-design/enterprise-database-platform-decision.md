# Enterprise Database Platform Decision

## Northstar Health Operations

---

**Primary Audience:** Northstar architects, the project owner, data engineers, subsystem maintainers, and reviewers responsible for SQL implementation

**Writing Layer:** Layer 2 — Operational / Architectural

**Architectural Purpose:** Establishes the approved target database platform, namespace strategy, physical type mapping, integrity-enforcement boundaries, deletion policy, migration approach, and implementation environment for Northstar.

**Document Type:** Engineering Decision Record

**Authority Level:** Approved Engineering Decision

**Status:** Approved — Locked

**Depends On:** Enterprise Relational Schema, Enterprise Relational Foundation, Enterprise Logical Model, Cross-System Identifier Dictionary, and Phase 4 platform-decision review

---

# 1. Approved Decision

Northstar will use:

```text
PostgreSQL 18
```

as its target relational database platform.

SQLite was evaluated as the primary alternative and was not selected.

PostgreSQL is the stronger fit for Northstar because the approved schema depends heavily on native relational types, native schema namespaces, foreign-key enforcement, reusable trigger functions, and cross-table integrity logic. The decision also better supports Northstar's stated goal of modeling an enterprise-realistic operational environment rather than optimizing only for the lowest local setup cost.

This decision does not authorize DDL by itself. It establishes the physical platform boundary within which DDL, migrations, constraints, triggers, indexes, and validation scripts may now be designed.

---

# 2. Repository-Specific Basis

The approved Enterprise Relational Schema contains:

* 17 canonical enterprise objects
* 4 associative entities
* 21 relational structures
* 44 foreign-key relationships
* 6 dependency tiers
* 24 Boolean fields
* 6 Decimal fields
* 20 Date fields
* 4 Timestamp fields

That is 54 fields whose logical types benefit directly from PostgreSQL's native `BOOLEAN`, `NUMERIC`, `DATE`, and `TIMESTAMP` support.

The schema also contains eight nontrivial cross-table or aggregate enforcement groups:

1. Fulfillment Event references must agree with Shipment.
2. Shipment Replenishment Allocation totals must remain within Shipment and Replenishment ceilings.
3. SLA Event references must agree with Fulfillment Event.
4. Replenishment Shortage Response must link the same Item and Location.
5. Corrective Action Vendor must agree with SLA Event.
6. Corrective Action Vendor must agree with Fulfillment Event.
7. Corrective Action SLA and Fulfillment Event references must agree.
8. Corrective Action Ticket references must not contradict linked source events.

The current migration baseline also contains:

* 3 orphaned Ticket references
* 4 unmatched Ticket owner names
* one Windows-1252 Ticket source file requiring UTF-8 normalization

These are migration conditions, not reasons to weaken the approved relational design.

---

# 3. PostgreSQL and SQLite Decision Matrix

| Criterion | PostgreSQL | SQLite | Decision Effect |
|---|---|---|---|
| Composite primary keys | Native support | Native support | Neutral |
| Business-key `UNIQUE` constraints | Native support | Native support | Neutral |
| Foreign-key enforcement | Enabled and enforced by the database | Must be enabled per connection | PostgreSQL |
| Native Boolean type | Yes | No | PostgreSQL |
| Exact Decimal type | `NUMERIC` | No equivalent native exact-decimal type | PostgreSQL |
| Native Date and Timestamp types | Yes | Stored through type convention | PostgreSQL |
| Native schema namespaces | Yes | No equivalent inside one database file | PostgreSQL |
| Reusable procedural trigger functions | Yes | Trigger support is more limited and row-trigger only | PostgreSQL |
| Deferred constraint-trigger support | Yes | No equivalent general constraint-trigger model | PostgreSQL |
| Local setup simplicity | Requires a service or container | Single-file engine | SQLite |
| Repository reproducibility | One-command container setup | One-command local file build | Close |
| Enterprise scalability | Strong | Limited for future concurrent service use | PostgreSQL |
| Portfolio value | Demonstrates production-oriented SQL and relational engineering | Demonstrates portability and embedded simplicity | PostgreSQL for Northstar's stated objective |

SQLite remains a capable relational engine. It was rejected because choosing it would move more of Northstar's approved type and integrity behavior into conventions, repeated checks, and external validation code.

---

# 4. Approved Namespace Strategy

Northstar will use one PostgreSQL database with six native schemas:

| PostgreSQL Schema | Tables |
|---|---|
| `core` | `location` |
| `workforce` | `employee`, `assignment`, `coverage_schedule`, `workload_record`, `workforce_escalation` |
| `vendor` | `vendor`, `shipment`, `fulfillment_event`, `sla_event`, `corrective_action` |
| `inventory` | `inventory_item`, `location_inventory`, `inventory_discrepancy`, `shortage`, `replenishment` |
| `ticketing` | `ticket` |
| `relationships` | `assignment_ticket`, `assignment_corrective_action`, `shipment_replenishment_allocation`, `replenishment_shortage_response` |

Table names remain singular and use `snake_case`.

DDL, migrations, triggers, views, and validation queries must use schema-qualified names. A configured `search_path` may improve interactive use, but it must not replace explicit qualification in repository-controlled SQL.

No persistent `reporting`, `reference`, or `staging` schema is authorized in the canonical model at this stage. Temporary migration tables may be used during controlled data loading without becoming governed enterprise structures.

---

# 5. Approved Physical Type Mapping

| Logical Type | PostgreSQL Type | Decision |
|---|---|---|
| `TEXT` | `TEXT` | Use unless a governed length limit exists |
| `INTEGER` | `INTEGER` | Direct mapping |
| `DECIMAL` | `NUMERIC` | Exact decimal storage; field-specific precision and scale are reviewed during DDL |
| `BOOLEAN` | `BOOLEAN` | Native mapping |
| `DATE` | `DATE` | Native mapping |
| `TIMESTAMP` | `TIMESTAMP WITHOUT TIME ZONE` | Matches the current timezone-naive source data |

`TIMESTAMP WITH TIME ZONE` is not approved for the initial implementation because the current Ticket timestamps contain no timezone or offset information. A future multi-timezone initiative may reopen this mapping through governed change control.

## Generated and Derived Fields

`inventory_discrepancy.variance_quantity` should be implemented as a stored generated value:

```text
counted_quantity - expected_quantity
```

The migration process must still compare the source CSV value against the generated result and report any disagreement.

Other calculated-looking fields remain stored values unless their complete formulas are separately governed. Their names alone do not authorize generated expressions.

---

# 6. Constraint Strategy

The initial PostgreSQL implementation will enforce:

* primary keys
* approved business-key `UNIQUE` constraints
* approved `NOT NULL` rules
* approved foreign keys once migration prerequisites are satisfied
* native Boolean typing
* governed row-level calculations and bounds
* approved cross-table consistency rules

## Provisional Controlled Values

Most observed value lists in the Enterprise Relational Schema are explicitly marked provisional because they were derived from small datasets.

Those provisional lists will not become hard `CHECK` constraints during the initial DDL build.

Instead, they will be represented through:

* SQL validation queries
* migration exception reports
* documented distinct-value checks
* later governance review before promotion to hard constraints

No new lookup table may be introduced solely to enforce a provisional vocabulary without architecture approval.

## Staged Ticket Foreign Keys

Ticket `location_id` and `employee_id` remain nullable and unconstrained during the initial reconciliation step.

The controlled sequence is:

```text
profile
→ map
→ populate
→ review exceptions
→ add foreign key
→ validate foreign key
→ evaluate NOT NULL promotion
```

The approved schema's staged treatment remains unchanged.

---

# 7. Cross-Table and Aggregate Enforcement

PostgreSQL trigger functions will enforce the approved non-column-level rules.

| Enforcement Group | Recommended Mechanism |
|---|---|
| Fulfillment Event versus Shipment references | Row-level validation trigger |
| SLA Event versus Fulfillment Event references | Row-level validation trigger |
| Replenishment Shortage Response compatibility | Row-level validation trigger |
| Corrective Action source-reference consistency | One reusable Corrective Action validation function covering the four approved rules |
| Shipment Replenishment Allocation aggregate ceilings | Constraint-trigger family covering allocation changes and relevant parent-quantity changes |

The allocation implementation must validate:

* `allocated_quantity > 0`
* total allocation by Shipment
* total allocation by Replenishment
* changes to an existing allocation
* deletion of an allocation
* changes to the governing Shipment quantity
* changes to Replenishment `approved_quantity`

The exact available-Shipment ceiling and the rule for allocation before quantities are known remain open business decisions and must be resolved before that trigger family is finalized.

Trigger code must raise clear, object-specific exceptions. Generic failure messages are not sufficient for migration or portfolio review.

---

# 8. Approved Deletion Policy

Northstar will use:

```text
ON DELETE RESTRICT
```

for all 44 foreign-key relationships.

No `ON DELETE CASCADE` exception is approved for the four associative entities.

Although an associative row cannot exist without both parents, these rows still record operational relationship evidence. `shipment_replenishment_allocation` also carries `allocated_quantity`, which makes automatic deletion especially inappropriate.

If a parent record is ever intentionally removed, dependent relationship rows must be reviewed and deleted explicitly within the same controlled transaction. This preserves visibility and prevents a parent deletion from silently erasing operational context.

This decision does not establish a broader archival or soft-deletion strategy. That would require a separate lifecycle initiative.

---

# 9. Migration and Reconciliation Strategy

The controlled migration sequence is:

```text
source files
↓
encoding normalization
↓
schema and identifier validation
↓
temporary staging
↓
relationship and exception reconciliation
↓
approved field-name transforms
↓
Tier 0–5 load
↓
constraint validation
↓
row-count and integrity verification
```

The migration work must explicitly address:

* `tickets-v1.csv` Windows-1252 to UTF-8 normalization
* formal Location mapping for Ticket records
* Employee reconciliation for Ticket owners
* orphaned Ticket references `INC-100018`, `INC-100021`, and `INC-100031`
* `schedule_id` to `coverage_schedule_id`
* `workload_id` to `workload_record_id`

Canonical PostgreSQL schemas should receive only validated rows. Unresolved source records remain in migration exception outputs until a governed resolution is approved.

---

# 10. Local Development Environment

The approved local environment is:

* PostgreSQL 18 in Docker Compose
* a major-version-pinned official PostgreSQL image
* one named data volume
* environment variables supplied through an uncommitted local `.env`
* a committed `.env.example` containing no secrets
* explicit scripts for create, load, validate, reset, and teardown
* a documented SQL client workflow

The database must not be automatically populated merely because the container starts. Schema creation and data loading should be explicit, repeatable commands so migration failures remain visible.

A binary database artifact will not be committed. The repository will contain the SQL, migration scripts, validation scripts, and reproducible environment needed to generate the database locally.

---

# 11. SQL Build Sequence

The physical build follows the approved architecture:

```text
create PostgreSQL schemas
↓
Tier 0 — Location, Employee, Vendor
↓
Tier 1 — Inventory Item, Ticket, Assignment, Coverage Schedule, Workload Record
↓
Tier 2 — Shipment, Replenishment, Location Inventory, Workforce Escalation, Assignment Ticket
↓
Tier 3 — Inventory Discrepancy, Shortage, Fulfillment Event, Shipment Replenishment Allocation
↓
Tier 4 — SLA Event, Replenishment Shortage Response
↓
Tier 5 — Corrective Action, then Assignment Corrective Action
↓
supporting indexes
↓
validation and cross-table enforcement
↓
migration and verification
```

The Tier 5 internal ordering exception remains in force.

---

# 12. Remaining Pre-DDL Decisions

The platform and deletion-policy decisions are complete.

The following implementation or data decisions remain:

1. Resolve or formally except the three orphaned Ticket references.
2. Resolve the four unmatched Ticket owner names.
3. Formally approve the four Ticket Location mappings.
4. Define the authoritative translation between Shipment and Fulfillment Event delivery-state, date, and quantity fields.
5. Decide whether allocation is permitted before Shipment available quantity or Replenishment `approved_quantity` is known.
6. Define the Shipment quantity used as the allocation ceiling.
7. Select field-specific `NUMERIC` precision and scale during DDL review.
8. Determine the initial supporting-index set after table and foreign-key DDL is drafted.

These decisions must not reopen the 17 objects, 4 associative entities, or Tier 0–5 schema unless a genuine contradiction is discovered.

---

# 13. Approval Boundary

This decision is:

```text
Approved — Locked
```

It approves:

* PostgreSQL 18
* one database with six native schemas
* schema-qualified SQL
* PostgreSQL native type mapping
* `TIMESTAMP WITHOUT TIME ZONE`
* universal `ON DELETE RESTRICT`
* trigger-based cross-table enforcement
* validation-only treatment for provisional controlled values
* Docker Compose as the local development baseline

It does not approve:

* table DDL
* migration scripts
* trigger code
* indexes
* source-data corrections
* a production deployment
* changes to the locked Enterprise Relational Schema

The next controlled initiative is physical SQL implementation.
