\# Ticket Dataset Schema  

\## Structured Dataset Blueprint



\---



\# Purpose



This document defines the structured dataset schema for the Northstar Health Operations Ticketing \& Incident Management System.



The schema translates operational ticket activity into a structured data format that can later support:

\- CSV dataset creation

\- Excel analysis

\- SQL database construction

\- Power BI reporting

\- SLA analysis

\- workflow bottleneck analysis

\- operational KPI tracking



\---



\# Dataset Name



```text

tickets.csv

```



\---



\# Dataset Grain



Each row represents:



```text

one ticket record

```



This means every ticket submitted into the system should appear as one row in the dataset.



\---



\# Primary Key



\## ticket\_id



Unique identifier for each ticket.



Example:



```text

INC-100001

```



\---



\# Core Dataset Fields



| Field Name | Data Type | Required | Description |

|---|---|---:|---|

| ticket\_id | Text | Yes | Unique ticket identifier |

| created\_at | Datetime | Yes | Date and time ticket was submitted |

| first\_response\_at | Datetime | Yes | Date and time first response occurred |

| resolved\_at | Datetime | Conditional | Date and time ticket was resolved |

| closed\_at | Datetime | Conditional | Date and time ticket was formally closed |

| category | Text | Yes | Primary ticket category |

| priority | Text | Yes | Ticket urgency level |

| status | Text | Yes | Current ticket lifecycle status |

| requesting\_location | Text | Yes | Clinic, hub, or department requesting support |

| assigned\_department | Text | Yes | Department responsible for resolution |

| assigned\_owner | Text | Optional | Team member responsible for the ticket |

| escalation\_flag | Boolean | Yes | Indicates whether ticket was escalated |

| reopened\_flag | Boolean | Yes | Indicates whether ticket was reopened |

| pending\_flag | Boolean | Yes | Indicates whether ticket entered pending status |

| sla\_target\_hours | Numeric | Yes | Expected resolution target in hours |

| resolution\_hours | Numeric | Conditional | Total hours from creation to resolution |

| response\_hours | Numeric | Yes | Total hours from creation to first response |

| sla\_met\_flag | Boolean | Conditional | Indicates whether ticket met SLA target |

| summary | Text | Yes | Short description of ticket issue |

| resolution\_notes | Text | Conditional | Notes describing how issue was resolved |



\---



\# Field Definitions



\## ticket\_id



Unique ticket identifier used for lookup, reporting, and audit reference.



Example values:

```text

INC-100001

INC-100002

INC-100003

```



\---



\## created\_at



Timestamp showing when the ticket was submitted.



Used to calculate:

\- response time

\- resolution time

\- ticket aging

\- ticket volume trends



\---



\## first\_response\_at



Timestamp showing when the first operational response occurred.



Used to calculate:

\- average first response time

\- SLA response performance

\- intake efficiency



\---



\## resolved\_at



Timestamp showing when the operational issue was resolved.



Used to calculate:

\- resolution time

\- SLA compliance

\- workflow performance



This field may be blank if the ticket is still open.



\---



\## closed\_at



Timestamp showing when the ticket was formally closed.



Used for:

\- audit tracking

\- lifecycle reporting

\- closure analysis



This field may be blank if the ticket has not been closed.



\---



\## category



Primary operational category assigned to the ticket.



Accepted values:

\- Inventory \& Supply

\- Scheduling \& Resource Coordination

\- Vendor \& Delivery Management

\- Operational Incident

\- Data Quality \& Compliance

\- Technical \& Systems Support



\---



\## priority



Operational urgency level assigned to the ticket.



Accepted values:

\- Priority 1 — Critical

\- Priority 2 — High

\- Priority 3 — Moderate

\- Priority 4 — Low



\---



\## status



Current lifecycle status of the ticket.



Accepted values:

\- New

\- Assigned

\- In Progress

\- Escalated

\- Pending

\- Resolved

\- Closed

\- Reopened



\---



\## requesting\_location



Clinic, distribution hub, or operational department requesting support.



Example values:

\- Raleigh Specialty Clinic 03

\- Durham Outpatient Clinic 07

\- Cary Distribution Hub 01

\- Wake Forest Clinic 11



\---



\## assigned\_department



Department responsible for ticket resolution.



Accepted values:

\- Operations Coordination Center

\- Supply \& Inventory Operations

\- Clinical Operations Support

\- Data Quality \& Compliance

\- Vendor \& Service Management

\- Operational Analytics \& Reporting



\---



\## assigned\_owner



Individual operational owner assigned to the ticket.



This field supports:

\- accountability tracking

\- workload balancing

\- operational ownership analysis



\---



\## escalation\_flag



Indicates whether the ticket was escalated beyond normal handling.



Accepted values:

```text

TRUE

FALSE

```



\---



\## reopened\_flag



Indicates whether the ticket was reopened after resolution.



Accepted values:

```text

TRUE

FALSE

```



\---



\## pending\_flag



Indicates whether the ticket entered pending status during the lifecycle.



Accepted values:

```text

TRUE

FALSE

```



\---



\## sla\_target\_hours



Expected resolution target based on priority level.



Example mapping:



| Priority | SLA Target Hours |

|---|---:|

| Priority 1 — Critical | 4 |

| Priority 2 — High | 24 |

| Priority 3 — Moderate | 72 |

| Priority 4 — Low | 120 |



\---



\## resolution\_hours



Total hours between ticket creation and resolution.



Formula concept:



```text

resolved\_at - created\_at

```



This field may be blank for unresolved tickets.



\---



\## response\_hours



Total hours between ticket creation and first response.



Formula concept:



```text

first\_response\_at - created\_at

```



\---



\## sla\_met\_flag



Indicates whether the ticket was resolved within the SLA target.



Formula concept:



```text

resolution\_hours <= sla\_target\_hours

```



Accepted values:

```text

TRUE

FALSE

```



This field may be blank for unresolved tickets.



\---



\## summary



Short business-readable description of the ticket.



Example:

```text

Inventory shortage reported for high-use clinical supply

```



\---



\## resolution\_notes



Short description of the action taken to resolve the ticket.



Example:

```text

Emergency transfer completed from Cary Distribution Hub 01

```



This field may be blank for unresolved tickets.



\---



\# Future Dataset Expansion



Future versions of this dataset may include:

\- root\_cause

\- vendor\_id

\- item\_id

\- clinic\_region

\- reopened\_count

\- pending\_reason

\- escalation\_reason

\- operational\_impact\_score

\- cost\_impact\_estimate

\- follow\_up\_required\_flag



These fields are intentionally deferred to keep the first dataset manageable and focused.



\---



\# Portfolio Use



This schema will support future project phases including:

\- generating the first synthetic ticket dataset

\- importing ticket data into Excel

\- creating SQL tables

\- writing SQL validation queries

\- creating Power BI ticket dashboards

\- analyzing SLA performance

\- identifying workflow bottlenecks

\- producing executive operational summaries



This schema represents the first structured data layer of the Northstar Health Operations portfolio ecosystem.

