# Ticket Dataset Schema

## Purpose

This document defines the structured dataset schema used within the Ticketing & Incident Management subsystem.

The schema establishes the fields, definitions, and data standards used to capture operational ticket activity, workflow progression, escalation events, service performance, and resolution outcomes.

---

# Dataset Name

```text
tickets-v1
```

---

# Dataset Grain

Each row represents:

```text
one ticket record
```

Each ticket submitted into the system is represented by a single record within the dataset.

---

# Primary Key

## ticket_id

Unique identifier assigned to each ticket.

Example:

```text
INC-100001
```

---

# Core Dataset Fields

|Field Name|Data Type|Required|Description|
|-|-|-|-|
|ticket_id|Text|Yes|Unique ticket identifier|
|created_at|Datetime|Yes|Date and time ticket was submitted|
|first_response_at|Datetime|Yes|Date and time first response occurred|
|resolved_at|Datetime|Conditional|Date and time ticket was resolved|
|closed_at|Datetime|Conditional|Date and time ticket was formally closed|
|category|Text|Yes|Primary ticket category|
|priority|Text|Yes|Ticket urgency level|
|status|Text|Yes|Current ticket lifecycle status|
|requesting_location|Text|Yes|Location requesting support|
|assigned_department|Text|Yes|Department responsible for resolution|
|assigned_owner|Text|Optional|Individual assigned to the ticket|
|escalation_flag|Boolean|Yes|Indicates whether ticket was escalated|
|reopened_flag|Boolean|Yes|Indicates whether ticket was reopened|
|pending_flag|Boolean|Yes|Indicates whether ticket entered pending status|
|sla_target_hours|Numeric|Yes|Expected resolution target in hours|
|resolution_hours|Numeric|Conditional|Total hours from creation to resolution|
|response_hours|Numeric|Yes|Total hours from creation to first response|
|sla_met_flag|Boolean|Conditional|Indicates whether ticket met SLA target|
|summary|Text|Yes|Short description of the ticket issue|
|resolution_notes|Text|Conditional|Notes describing ticket resolution|

---

# Field Definitions

## ticket_id

Unique ticket identifier used for lookup, reporting, and audit reference.

Example values:

```text
INC-100001
INC-100002
INC-100003
```

---

## created_at

Timestamp indicating when the ticket was submitted.

Supports:

* Response time calculations
* Resolution time calculations
* Ticket volume analysis
* Lifecycle reporting

---

## first_response_at

Timestamp indicating when the first operational response occurred.

Supports:

* Response time measurement
* Service performance monitoring
* Intake workflow analysis

---

## resolved_at

Timestamp indicating when the operational issue was resolved.

Supports:

* Resolution time calculations
* Service level evaluation
* Workflow performance analysis

This field may be blank for unresolved tickets.

---

## closed_at

Timestamp indicating when the ticket was formally closed.

Supports:

* Lifecycle reporting
* Audit tracking
* Workflow completion analysis

This field may be blank for tickets that remain open.

---

## category

Primary operational category assigned to the ticket.

Accepted values:

* Inventory & Supply
* Scheduling & Resource Coordination
* Vendor & Delivery Management
* Operational Incident
* Data Quality & Compliance
* Technical & Systems Support

---

## priority

Operational urgency level assigned to the ticket.

Accepted values:

* Priority 1 — Critical
* Priority 2 — High
* Priority 3 — Moderate
* Priority 4 — Low

---

## status

Current lifecycle status of the ticket.

Accepted values:

* New
* Assigned
* In Progress
* Escalated
* Pending
* Resolved
* Closed

---

## requesting_location

Location requesting support or reporting the operational issue.

Example values:

* Raleigh Specialty Clinic 03
* Durham Outpatient Clinic 07
* Cary Distribution Hub 01
* Wake Forest Clinic 11

---

## assigned_department

Department responsible for ticket resolution.

Accepted values:

* Operations Coordination Center
* Supply & Inventory Operations
* Clinical Operations Support
* Data Quality & Compliance
* Vendor & Service Management
* Operational Analytics & Reporting

---

## assigned_owner

Individual responsible for ticket ownership and resolution activity.

Supports:

* Accountability tracking
* Workload monitoring
* Operational ownership visibility

---

## escalation_flag

Indicates whether the ticket required escalation.

Accepted values:

```text
TRUE
FALSE
```

---

## reopened_flag

Indicates whether the ticket was reopened after resolution.

Accepted values:

```text
TRUE
FALSE
```

---

## pending_flag

Indicates whether the ticket entered a pending status during its lifecycle.

Accepted values:

```text
TRUE
FALSE
```

---

## sla_target_hours

Expected resolution target based on ticket priority.

Example mapping:

|Priority|SLA Target Hours|
|-|-|
|Priority 1 — Critical|4|
|Priority 2 — High|24|
|Priority 3 — Moderate|72|
|Priority 4 — Low|120|

---

## resolution_hours

Total hours between ticket creation and ticket resolution.

Formula concept:

```text
resolved_at - created_at
```

This field may be blank for unresolved tickets.

---

## response_hours

Total hours between ticket creation and first response.

Formula concept:

```text
first_response_at - created_at
```

---

## sla_met_flag

Indicates whether the ticket was resolved within the assigned SLA target.

Formula concept:

```text
resolution_hours <= sla_target_hours
```

Accepted values:

```text
TRUE
FALSE
```

This field may be blank for unresolved tickets.

---

## summary

Short operational description of the issue, request, or event.

Example:

```text
Inventory shortage reported for high-use clinical supply
```

---

## resolution_notes

Description of actions taken to resolve the issue.

Example:

```text
Emergency transfer completed from Cary Distribution Hub 01
```

This field may be blank for unresolved tickets.

---

# Data Quality Considerations

* Each ticket_id should remain unique.
* Timestamp fields should accurately reflect lifecycle progression.
* Priority values should remain standardized.
* Status values should remain standardized.
* Department and location references should remain consistent across records.
* Boolean fields should use TRUE or FALSE consistently.
* Resolution and SLA fields should align with ticket lifecycle status.

---

# Operational Usage

This dataset supports:

* Ticket lifecycle monitoring
* Service performance reporting
* SLA evaluation
* Escalation tracking
* Department workload analysis
* Operational trend analysis
* KPI reporting

The Ticket dataset provides the operational foundation for reporting, workflow analysis, and performance monitoring within the Ticketing & Incident Management subsystem.

