\# Ticket Lifecycle Workflow  

\## Operational Workflow Logic



\---



\# Purpose



This document defines the standard lifecycle for tickets within the Northstar Health Operations Ticketing \& Incident Management System.



The purpose of the lifecycle is to create a consistent operational process for receiving, routing, resolving, escalating, and closing service requests and operational incidents.



This workflow supports:

\- Operational consistency

\- SLA tracking

\- Escalation management

\- Department accountability

\- Reporting accuracy

\- Process improvement analysis



\---



\# Ticket Lifecycle Overview



A ticket moves through a structured workflow from initial submission to final closure.



Standard lifecycle stages:



```text

New → Assigned → In Progress → Resolved → Closed

```



Some tickets may also move through conditional stages:



```text

Escalated

Pending

Reopened

```



These additional stages are used when tickets require extra review, external dependency tracking, or follow-up work.



\---



\# Standard Workflow Stages



\## 1. New



A ticket enters the system after being submitted by a clinic, department, distribution hub, or operational support team.



At this stage, the ticket has not yet been reviewed by the Operations Coordination Center.



Key actions:

\- Ticket is created

\- Required fields are captured

\- Initial timestamp is recorded

\- Ticket awaits intake review



\---



\## 2. Assigned



The Operations Coordination Center reviews the ticket and routes it to the responsible department or team.



Key actions:

\- Ticket category is confirmed

\- Priority level is reviewed

\- Responsible department is assigned

\- Operational owner is identified

\- SLA expectations are established



\---



\## 3. In Progress



The assigned department begins active investigation or resolution work.



Key actions:

\- Issue is reviewed

\- Supporting information is gathered

\- Cross-functional coordination begins if needed

\- Resolution actions are started

\- Status updates are documented



\---



\## 4. Escalated



A ticket is escalated when the issue exceeds normal handling rules or requires increased visibility.



Common escalation triggers:

\- SLA threshold exceeded

\- Patient-facing operational risk

\- Repeated issue pattern

\- Vendor dependency

\- Multi-department involvement

\- Severe inventory or staffing impact

\- Leadership visibility required



Key actions:

\- Escalation flag is updated

\- Higher-level owner is notified

\- Additional departments may be engaged

\- Management visibility may be added

\- Resolution priority may increase



\---



\## 5. Pending



A ticket is placed in pending status when resolution work is temporarily blocked by an external dependency.



Common pending reasons:

\- Awaiting vendor response

\- Awaiting clinic confirmation

\- Awaiting shipment update

\- Awaiting missing information

\- Awaiting system access

\- Awaiting leadership decision



Key actions:

\- Pending reason is documented

\- Follow-up owner is assigned

\- Expected follow-up date may be added

\- Ticket remains open but paused



\---



\## 6. Resolved



A ticket is marked resolved when the operational issue has been addressed.



Key actions:

\- Resolution action is completed

\- Resolution notes are documented

\- Resolution timestamp is recorded

\- Requesting location may be notified

\- Ticket awaits final closure



\---



\## 7. Closed



A ticket is closed after resolution has been confirmed or the ticket has met closure criteria.



Key actions:

\- Closure timestamp is recorded

\- Final status is confirmed

\- Ticket is archived for reporting

\- Metrics become available for KPI reporting



\---



\## 8. Reopened



A ticket may be reopened when the issue returns, resolution was incomplete, or the requesting location reports that the problem remains unresolved.



Common reopen reasons:

\- Issue not fully resolved

\- Same problem recurred

\- Incorrect routing

\- Incomplete documentation

\- Follow-up action required



Key actions:

\- Ticket status returns to In Progress or Assigned

\- Reopen reason is documented

\- Reopened ticket flag is updated

\- Root cause review may be triggered



\---



\# Routing Logic



The Operations Coordination Center routes tickets based on category, priority, operational impact, and department ownership.



\## Inventory \& Supply

Routed to Supply \& Inventory Operations.



Examples:

\- Stockout risk

\- Replenishment delay

\- Inventory discrepancy

\- Emergency transfer request



\---



\## Scheduling \& Resource Coordination

Routed to Clinical Operations Support.



Examples:

\- Staffing conflict

\- Room availability issue

\- Equipment scheduling conflict

\- Clinic support request



\---



\## Vendor \& Delivery Management

Routed to Vendor \& Service Management or Supply \& Inventory Operations.



Examples:

\- Vendor delay

\- Incomplete delivery

\- Fulfillment issue

\- Delivery schedule disruption



\---



\## Data Quality \& Compliance

Routed to Data Quality \& Compliance.



Examples:

\- Missing records

\- Duplicate entries

\- Audit exception

\- Reporting inconsistency



\---



\## Operational Incident

Routed based on issue impact and required department response.



Examples:

\- Clinic workflow interruption

\- Service continuity concern

\- Cross-functional operational issue



\---



\## Technical \& Systems Support

Routed to the appropriate systems support owner or reporting support team.



Examples:

\- Dashboard access issue

\- Ticketing platform issue

\- Reporting system interruption

\- Workflow tool error



\---



\# Priority Logic



Priority levels are assigned based on urgency, operational impact, service continuity risk, and time sensitivity.



\## Priority 1 — Critical

Requires immediate response.



Used when the issue creates severe operational disruption or high-risk service continuity concern.



Examples:

\- Clinic unable to operate normally

\- Critical supply unavailable

\- Major system interruption

\- High-impact escalation requiring leadership visibility



\---



\## Priority 2 — High

Requires rapid response.



Used when the issue may disrupt operations if not addressed quickly.



Examples:

\- High-demand inventory shortage

\- Vendor delay affecting clinic readiness

\- Staffing/resource issue impacting schedule

\- Repeated operational failure



\---



\## Priority 3 — Moderate

Standard operational priority.



Used for normal service requests and incidents that require timely handling but do not create immediate operational risk.



Examples:

\- Routine supply request

\- Non-critical data correction

\- Standard scheduling coordination issue

\- General operational support ticket



\---



\## Priority 4 — Low

Low urgency.



Used for informational requests, minor coordination items, documentation updates, or non-urgent support.



Examples:

\- Reporting clarification

\- Documentation update

\- Low-impact system question

\- Future-dated coordination request



\---



\# SLA Logic



Service Level Agreements help define expected response and resolution expectations by ticket priority.



Example SLA expectations:



| Priority | Initial Response Target | Resolution Target |

|---|---:|---:|

| Priority 1 — Critical | 30 minutes | 4 hours |

| Priority 2 — High | 2 hours | 1 business day |

| Priority 3 — Moderate | 1 business day | 3 business days |

| Priority 4 — Low | 2 business days | 5 business days |



These targets support future KPI calculations such as SLA compliance rate, average response time, and average resolution time.



\---



\# Workflow Risks



Several operational risks may affect ticket lifecycle performance:



\- Tickets routed to the wrong department

\- Priority levels assigned inconsistently

\- Escalations triggered too late

\- Pending tickets not followed up

\- Resolution notes incomplete

\- Closed tickets reopened due to incomplete fixes

\- SLA targets missed during high-volume periods

\- Multi-department issues lacking clear ownership



These risks create future opportunities for workflow analysis, process redesign, KPI monitoring, and operational improvement.



\---



\# Future Portfolio Use



This workflow document will support future Northstar portfolio modules, including:



\- Process maps

\- SQL ticket lifecycle tables

\- SLA analysis

\- Power BI ticket dashboards

\- Escalation trend reporting

\- Bottleneck analysis

\- Operational staffing analysis

\- Executive summaries

\- Workflow improvement recommendations

