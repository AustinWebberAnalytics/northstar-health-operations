# Ticket Dataset Schema  

## Structured Dataset Blueprint



---



# Purpose



This document defines the structured dataset schema for the Northstar Health Operations Ticketing & Incident Management System.



The schema translates operational ticket activity into a structured data format that can later support:

- CSV dataset creation

- Excel analysis

- SQL database construction

- Power BI reporting

- SLA analysis

- workflow bottleneck analysis

- operational KPI tracking



---



# Dataset Name



```text

tickets.csv

```



---



# Dataset Grain



Each row represents:



```text

one ticket record

```



This means every ticket submitted into the system should appear as one row in the dataset.



---



# Primary Key



## ticket_id



Unique identifier for each ticket.



Example:



```text

INC-100001

```



---



# Core Dataset Fields



| Field Name | Data Type | Required | Description |

|---|---|---:|---|

| ticket_id | Text | Yes | Unique ticket identifier |

| created_at | Datetime | Yes | Date and time ticket was submitted |

| first_response_at | Datetime | Yes | Date and time first response occurred |

| resolved_at | Datetime | Conditional | Date and time ticket was resolved |

| closed_at | Datetime | Conditional | Date and time ticket was formally closed |

| category | Text | Yes | Primary ticket category |

| priority | Text | Yes | Ticket urgency level |

| status | Text | Yes | Current ticket lifecycle status |

| requesting_location | Text | Yes | Clinic, hub, or department requesting support |

| assigned_department | Text | Yes | Department responsible for resolution |

| assigned_owner | Text | Optional | Team member responsible for the ticket |

| escalation_flag | Boolean | Yes | Indicates whether ticket was escalated |

| reopened_flag | Boolean | Yes | Indicates whether ticket was reopened |

| pending_flag | Boolean | Yes | Indicates whether ticket entered pending status |

| sla_target_hours | Numeric | Yes | Expected resolution target in hours |

| resolution_hours | Numeric | Conditional | Total hours from creation to resolution |

| response_hours | Numeric | Yes | Total hours from creation to first response |

| sla_met_flag | Boolean | Conditional | Indicates whether ticket met SLA target |

| summary | Text | Yes | Short description of ticket issue |

| resolution_notes | Text | Conditional | Notes describing how issue was resolved |



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



Timestamp showing when the ticket was submitted.



Used to calculate:

- response time

- resolution time

- ticket aging

- ticket volume trends



---



## first_response_at



Timestamp showing when the first operational response occurred.



Used to calculate:

- average first response time

- SLA response performance

- intake efficiency



---



## resolved_at



Timestamp showing when the operational issue was resolved.



Used to calculate:

- resolution time

- SLA compliance

- workflow performance



This field may be blank if the ticket is still open.



---



## closed_at



Timestamp showing when the ticket was formally closed.



Used for:

- audit tracking

- lifecycle reporting

- closure analysis



This field may be blank if the ticket has not been closed.



---



## category



Primary operational category assigned to the ticket.



Accepted values:

- Inventory & Supply

- Scheduling & Resource Coordination

- Vendor & Delivery Management

- Operational Incident

- Data Quality & Compliance

- Technical & Systems Support



---



## priority



Operational urgency level assigned to the ticket.



Accepted values:

- Priority 1 — Critical

- Priority 2 — High

- Priority 3 — Moderate

- Priority 4 — Low



---



## status



Current lifecycle status of the ticket.



Accepted values:

- New

- Assigned

- In Progress

- Escalated

- Pending

- Resolved

- Closed

- Reopened



---



## requesting_location



Clinic, distribution hub, or operational department requesting support.



Example values:

- Raleigh Specialty Clinic 03

- Durham Outpatient Clinic 07

- Cary Distribution Hub 01

- Wake Forest Clinic 11



---



## assigned_department



Department responsible for ticket resolution.



Accepted values:

- Operations Coordination Center

- Supply & Inventory Operations

- Clinical Operations Support

- Data Quality & Compliance

- Vendor & Service Management

- Operational Analytics & Reporting



---



## assigned_owner



Individual operational owner assigned to the ticket.



This field supports:

- accountability tracking

- workload balancing

- operational ownership analysis



---



## escalation_flag



Indicates whether the ticket was escalated beyond normal handling.



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



Indicates whether the ticket entered pending status during the lifecycle.



Accepted values:

```text

TRUE

FALSE

```



---



## sla_target_hours



Expected resolution target based on priority level.



Example mapping:



| Priority | SLA Target Hours |

|---|---:|

| Priority 1 — Critical | 4 |

| Priority 2 — High | 24 |

| Priority 3 — Moderate | 72 |

| Priority 4 — Low | 120 |



---



## resolution_hours



Total hours between ticket creation and resolution.



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



Indicates whether the ticket was resolved within the SLA target.



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



Short business-readable description of the ticket.



Example:

```text

Inventory shortage reported for high-use clinical supply

```



---



## resolution_notes



Short description of the action taken to resolve the ticket.



Example:

```text

Emergency transfer completed from Cary Distribution Hub 01

```



This field may be blank for unresolved tickets.



---



# Future Dataset Expansion



Future versions of this dataset may include:

- root_cause

- vendor_id

- item_id

- clinic_region

- reopened_count

- pending_reason

- escalation_reason

- operational_impact_score

- cost_impact_estimate

- follow_up_required_flag



These fields are intentionally deferred to keep the first dataset manageable and focused.



---



# Portfolio Use



This schema will support future project phases including:

- generating the first synthetic ticket dataset

- importing ticket data into Excel

- creating SQL tables

- writing SQL validation queries

- creating Power BI ticket dashboards

- analyzing SLA performance

- identifying workflow bottlenecks

- producing executive operational summaries



This schema represents the first structured data layer of the Northstar Health Operations portfolio ecosystem.

