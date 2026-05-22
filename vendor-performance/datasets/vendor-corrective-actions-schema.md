# Vendor Corrective Actions Schema  

## Northstar Health Operations

---

# Purpose

This document defines the schema for the `vendor-corrective-actions.csv` dataset within the Vendor Performance subsystem.

The purpose of this schema is to:

- define corrective action tracking fields
- standardize vendor remediation lifecycle records
- support operational recovery monitoring
- support escalation-aware remediation analysis
- support continuity stabilization visibility
- support vendor accountability tracking
- support future SQL integration
- support future Power BI modeling

This schema serves as the primary reference for vendor corrective action records across Northstar Health Operations.

---

# Dataset Overview

The `vendor-corrective-actions.csv` dataset captures operational remediation activity associated with vendor instability, SLA degradation, fulfillment disruption, escalation-heavy vendor behavior, and operational continuity risk.

This dataset functions as:

# the operational remediation tracking layer

within the Vendor Performance subsystem.

The dataset is intended to support analysis of:

- vendor recovery progress
- remediation activity
- escalation reduction
- SLA stabilization
- fulfillment recovery
- operational continuity restoration
- corrective action recurrence
- operational intervention outcomes

---

# Dataset Location

```text
vendor-performance/datasets/vendor-corrective-actions.csv
```

---

# Dataset Grain

Each row represents:

# one vendor corrective action case

A corrective action case may represent:

- SLA recovery intervention
- fulfillment stabilization effort
- escalation remediation activity
- operational continuity recovery effort
- vendor performance improvement initiative

The primary identifier for each record is:

```text
corrective_action_id
```

---

# Primary Key

| Field | Purpose |
|---|---|
| corrective_action_id | Unique identifier for each corrective action case |

Example:

```text
CA-1001
```

---

# Foreign Keys and Shared Identifiers

This dataset should use shared identifiers to support cross-system relationships.

| Field | Related Dataset | Purpose |
|---|---|---|
| vendor_id | vendor-master.csv | Connects corrective action to vendor identity |
| sla_event_id | vendor-sla-tracking.csv | Connects remediation activity to SLA instability |
| fulfillment_event_id | vendor-fulfillment-events.csv | Connects remediation activity to fulfillment instability |
| related_ticket_id | tickets-v1.csv | Connects remediation activity to operational escalation workflows |

---

# Field Naming Standards

All fields should use:

```text
snake_case
```

Field names should remain:

- lowercase
- business-readable
- operationally descriptive
- consistent with enterprise naming standards

Avoid:

```text
correctiveActionID
reviewStatus
VendorRef
ticketLink
```

Preferred:

```text
corrective_action_id
review_status
vendor_id
related_ticket_id
```

---

# Schema Definition

| Field Name | Data Type | Required | Description |
|---|---|---|---|
| corrective_action_id | Text | Yes | Unique corrective action case identifier |
| vendor_id | Text | Yes | Vendor associated with corrective action |
| corrective_action_type | Text | Yes | Operational remediation category |
| corrective_action_status | Text | Yes | Current remediation lifecycle status |
| corrective_action_severity | Text | Yes | Severity classification of operational instability |
| trigger_reason | Text | Yes | Operational issue that triggered corrective action |
| sla_event_id | Text | No | Related SLA instability event |
| fulfillment_event_id | Text | No | Related fulfillment instability event |
| related_ticket_id | Text | No | Related escalation or incident ticket |
| assigned_owner | Text | Yes | Operational owner responsible for remediation oversight |
| remediation_plan_summary | Text | Yes | Summary of remediation expectations |
| monitoring_start_date | Date | Yes | Date corrective action monitoring began |
| reassessment_date | Date | No | Scheduled or completed reassessment date |
| recovery_status | Text | Yes | Current operational recovery state |
| escalation_required_flag | Boolean | Yes | Indicates whether leadership escalation is required |
| corrective_action_closed_flag | Boolean | Yes | Indicates whether corrective action case is closed |
| notes | Text | No | Additional operational remediation notes |

---

# Field Definitions

---

## corrective_action_id

### Purpose

Uniquely identifies each vendor corrective action case.

### Format

```text
CA-####
```

### Example

```text
CA-1001
```

### Governance Rule

The `corrective_action_id` field should remain unique and stable across all corrective action records.

---

## vendor_id

### Purpose

Identifies the vendor associated with the remediation activity.

### Format

```text
VEND-###
```

### Example

```text
VEND-004
```

### Governance Rule

The `vendor_id` field should align with valid vendor identifiers where vendor master data exists.

---

## corrective_action_type

### Purpose

Classifies the operational remediation category.

### Example Values

```text
SLA Recovery
Fulfillment Stabilization
Escalation Reduction
Operational Recovery
Continuity Risk Review
```

### Governance Rule

Corrective action types should remain operationally meaningful and standardized.

---

## corrective_action_status

### Purpose

Defines the current lifecycle status of the corrective action case.

### Example Values

```text
Open
Monitoring
Reassessment Pending
Resolved
Escalated Review
```

### Governance Rule

Lifecycle statuses should remain standardized and business-readable.

---

## corrective_action_severity

### Purpose

Defines the operational severity associated with the remediation case.

### Example Values

```text
Advisory
Monitoring
Action Required
Escalated Review
Critical Intervention
```

### Governance Rule

Severity classifications should reflect realistic operational disruption exposure.

---

## trigger_reason

### Purpose

Defines the operational issue that initiated corrective action review.

### Example

```text
Repeated SLA breaches triggered operational review.
```

### Governance Rule

Trigger reasons should remain concise and operationally descriptive.

---

## sla_event_id

### Purpose

Connects corrective action activity to related SLA instability.

### Format

```text
SLA-####
```

### Example

```text
SLA-1002
```

### Governance Rule

This field may remain blank when corrective action is not directly tied to a specific SLA event.

---

## fulfillment_event_id

### Purpose

Connects corrective action activity to related fulfillment instability.

### Format

```text
VF-####
```

### Example

```text
VF-1006
```

### Governance Rule

This field may remain blank when no fulfillment relationship exists.

---

## related_ticket_id

### Purpose

Connects corrective action activity to operational escalation workflows.

### Format

```text
INC-######
```

### Example

```text
INC-100012
```

### Governance Rule

This field may remain blank when no escalation relationship exists.

---

## assigned_owner

### Purpose

Defines the operational owner responsible for corrective action oversight.

### Example Values

```text
Supply Chain Operations
Vendor Management
Inventory Leadership
Operational Support
```

### Governance Rule

Assigned ownership values should remain operationally meaningful and standardized.

---

## remediation_plan_summary

### Purpose

Provides a summary of the operational remediation plan.

### Example

```text
Vendor required to improve shipment communication and reduce delayed fulfillment frequency.
```

### Governance Rule

Remediation summaries should remain concise and operationally actionable.

---

## monitoring_start_date

### Purpose

Defines the date corrective action monitoring began.

### Example

```text
2026-05-24
```

### Governance Rule

Date values should remain internally consistent across operational datasets.

---

## reassessment_date

### Purpose

Defines the planned or completed operational reassessment date.

### Example

```text
2026-06-07
```

### Governance Rule

This field may remain blank for newly opened corrective action cases.

---

## recovery_status

### Purpose

Defines the current operational recovery state.

### Example Values

```text
Improving
Stable
Monitoring
Unresolved
Escalated
```

### Governance Rule

Recovery statuses should remain standardized and operationally meaningful.

---

## escalation_required_flag

### Purpose

Indicates whether leadership escalation is required.

### Format

```text
TRUE
FALSE
```

---

## corrective_action_closed_flag

### Purpose

Indicates whether the corrective action case has been formally closed.

### Format

```text
TRUE
FALSE
```

---

## notes

### Purpose

Provides additional operational remediation context.

### Example

```text
Vendor recovery remains incomplete due to repeated delayed fulfillment events.
```

### Governance Rule

Notes should remain concise and operationally relevant.

---

# Required Fields

The following fields are required:

```text
corrective_action_id
vendor_id
corrective_action_type
corrective_action_status
corrective_action_severity
trigger_reason
assigned_owner
remediation_plan_summary
monitoring_start_date
recovery_status
escalation_required_flag
corrective_action_closed_flag
```

Optional fields include:

```text
sla_event_id
fulfillment_event_id
related_ticket_id
reassessment_date
notes
```

---

# Boolean Standards

Boolean fields should use:

```text
TRUE
FALSE
```

Boolean fields in this dataset include:

```text
escalation_required_flag
corrective_action_closed_flag
```

Avoid:

```text
Yes
No
Y
N
1
0
```

---

# Status and Classification Standards

Status and classification fields should use business-readable values.

Examples:

```text
Open
Monitoring
Reassessment Pending
Resolved
Escalated Review

Advisory
Monitoring
Action Required
Escalated Review
Critical Intervention

Improving
Stable
Monitoring
Unresolved
Escalated
```

Values should remain:

- consistent
- readable
- operationally meaningful
- reporting-friendly

---

# Relationship Standards

The `vendor-corrective-actions.csv` dataset is expected to connect to operational vendor activity through:

```text
vendor_id
sla_event_id
fulfillment_event_id
related_ticket_id
```

Expected relationships may include:

```text
vendor-master[vendor_id] → vendor-corrective-actions[vendor_id]
vendor-sla-tracking[sla_event_id] → vendor-corrective-actions[sla_event_id]
vendor-fulfillment-events[fulfillment_event_id] → vendor-corrective-actions[fulfillment_event_id]
tickets-v1[ticket_id] → vendor-corrective-actions[related_ticket_id]
```

---

# Cross-System Usage

The `vendor-corrective-actions.csv` dataset may connect remediation activity to:

- escalation analysis
- vendor recovery monitoring
- SLA stabilization reporting
- operational continuity visibility
- fulfillment recovery analysis
- leadership remediation reporting

This supports:

- vendor recovery tracking
- escalation reduction analysis
- operational stabilization visibility
- corrective action recurrence monitoring
- continuity-risk reduction analysis

---

# Data Quality Rules

The `vendor-corrective-actions.csv` dataset should be reviewed for:

- duplicate `corrective_action_id` values
- missing required fields
- invalid vendor references
- invalid SLA references
- invalid fulfillment references
- inconsistent boolean values
- unresolved cases missing reassessment dates
- escalated cases missing escalation indicators

Each `corrective_action_id` should remain unique and stable.

---

# Future SQL Readiness

This schema supports future SQL integration by defining:

- stable remediation tracking keys
- escalation-aware recovery relationships
- operational stabilization modeling
- corrective action lifecycle structure
- vendor recovery aggregation capability

Future SQL queries may analyze:

- vendor recovery duration
- escalation reduction trends
- corrective action recurrence
- operational stabilization success rates
- continuity-risk recovery patterns

---

# Future Power BI Readiness

This schema supports future Power BI modeling by functioning as an operational remediation fact table.

Potential model relationships include:

```text
vendor-master[vendor_id] → vendor-corrective-actions[vendor_id]
vendor-sla-tracking[sla_event_id] → vendor-corrective-actions[sla_event_id]
vendor-fulfillment-events[fulfillment_event_id] → vendor-corrective-actions[fulfillment_event_id]
```

This supports reporting by:

- vendor
- corrective action status
- remediation severity
- operational owner
- recovery status
- escalation requirement
- closure status

---

# Governance Alignment

This schema follows established Northstar governance standards, including:

- subsystem-centered architecture
- naming convention standards
- shared identifier standards
- dataset governance standards
- cross-system relational planning
- SQL readiness
- Power BI readiness

Future changes to this schema should be made:

# systematically

NOT:

# reactively.

---

# Portfolio Significance

This schema demonstrates:

- operational remediation modeling
- escalation-aware recovery tracking
- operational continuity stabilization analysis
- vendor recovery lifecycle governance
- relational data governance
- SQL readiness awareness
- Power BI modeling awareness
- scalable operational subsystem construction

The `vendor-corrective-actions.csv` schema strengthens the Vendor Performance subsystem by establishing a standardized remediation tracking layer supporting vendor recovery monitoring, escalation reduction analysis, operational stabilization visibility, and leadership operational reporting.