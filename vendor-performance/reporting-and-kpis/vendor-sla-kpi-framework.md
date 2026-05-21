\# Vendor SLA KPI Framework  



\## Northstar Health Operations



\---



\# Purpose



This document defines the KPI framework for vendor SLA monitoring within the Vendor Performance subsystem.



The purpose of this framework is to:



\- standardize vendor SLA reporting

\- define operational SLA performance metrics

\- support vendor reliability analysis

\- support escalation visibility

\- support operational continuity monitoring

\- support leadership operational reporting

\- support future Power BI dashboard development

\- support future SQL-based KPI aggregation



This framework serves as the primary reference for interpreting SLA performance across vendor-supported operational workflows.



\---



\# Operational Reporting Philosophy



Vendor SLA reporting should prioritize:



\- operational clarity

\- leadership readability

\- escalation visibility

\- disruption awareness

\- vendor accountability

\- KPI consistency

\- trend visibility



Vendor SLA reporting should support:



\# operational decision-making



NOT:



\# purely technical reporting.



\---



\# KPI Reporting Objectives



The Vendor SLA KPI framework is intended to support analysis of:



\- vendor compliance consistency

\- SLA breach frequency

\- escalation-linked SLA failures

\- operational disruption exposure

\- corrective action trends

\- emergency response reliability

\- vendor performance stability



The framework should help leadership identify:



\- high-risk vendors

\- recurring SLA failures

\- escalation-heavy vendor relationships

\- operational continuity threats

\- corrective action requirements



\---



\# Primary SLA KPIs



\---



\# SLA Compliance Rate



\## Purpose



Measures the percentage of SLA events meeting operational expectations.



\## Formula



```text

(SLA Events Marked "Met" ÷ Total SLA Events) × 100

```



\## Interpretation



Higher percentages indicate:



\- stable vendor performance

\- reliable fulfillment timing

\- reduced operational disruption exposure



Lower percentages may indicate:



\- vendor instability

\- fulfillment inconsistency

\- operational continuity risk

\- escalation pressure



\---



\# SLA Breach Rate



\## Purpose



Measures the percentage of SLA events that breached expected service thresholds.



\## Formula



```text

(SLA Breach Events ÷ Total SLA Events) × 100

```



\## Interpretation



Higher breach rates may indicate:



\- vendor reliability concerns

\- operational workflow disruption

\- delayed shipment activity

\- escalation-heavy vendor relationships



\---



\# Escalation-Linked SLA Rate



\## Purpose



Measures the percentage of SLA events requiring operational escalation.



\## Formula



```text

(Escalated SLA Events ÷ Total SLA Events) × 100

```



\## Interpretation



Higher escalation rates may indicate:



\- operational instability

\- vendor communication failures

\- unresolved delivery issues

\- increased coordination workload



\---



\# Corrective Action Rate



\## Purpose



Measures the percentage of SLA events requiring corrective action.



\## Formula



```text

(Corrective Action Required Events ÷ Total SLA Events) × 100

```



\## Interpretation



Higher corrective action rates may indicate:



\- recurring operational issues

\- vendor process instability

\- repeated SLA failures

\- increased vendor oversight requirements



\---



\# Average SLA Response Time



\## Purpose



Measures average operational response or fulfillment duration.



\## Formula



```text

Total Actual Response Hours ÷ Total SLA Events

```



\## Interpretation



Lower response durations generally indicate:



\- stronger operational responsiveness

\- improved fulfillment consistency

\- reduced operational disruption exposure



Higher durations may indicate:



\- workflow bottlenecks

\- vendor delays

\- operational continuity risk



\---



\# Vendor Reliability Score



\## Purpose



Provides a composite operational vendor reliability measurement.



\## Example Inputs



May include:



\- SLA compliance rate

\- breach frequency

\- escalation frequency

\- corrective action frequency

\- operational impact severity



\## Interpretation



Higher reliability scores indicate:



\- operationally stable vendor partnerships

\- reduced continuity risk

\- stronger fulfillment consistency



Lower scores may indicate:



\- elevated disruption exposure

\- escalation dependency

\- unstable vendor performance



\---



\# Operational Impact Distribution



\## Purpose



Measures SLA event distribution by operational impact severity.



\## Example Categories



```text

Low

Moderate

High

Critical

```



\## Interpretation



Higher concentrations of:



```text

High

Critical

```



events may indicate:



\- operational continuity threats

\- severe vendor instability

\- elevated escalation exposure



\---



\# SLA Category Performance



\## Purpose



Measures vendor performance across operational SLA categories.



\## Example Categories



```text

Delivery SLA

Fulfillment SLA

Escalation Response SLA

Emergency Response SLA

Operational Support SLA

```



\## Interpretation



This KPI supports identification of:



\- weak operational domains

\- fulfillment bottlenecks

\- escalation handling weaknesses

\- emergency response instability



\---



\# Reporting Segmentation Standards



Vendor SLA reporting should support segmentation by:



\- vendor

\- SLA category

\- operational impact level

\- escalation requirement

\- corrective action requirement

\- shipment status

\- fulfillment performance

\- reporting period



This improves:



\- operational visibility

\- leadership readability

\- vendor comparison capability

\- trend interpretation



\---



\# Executive Reporting Standards



Executive SLA reporting should emphasize:



\- concise KPI visibility

\- operational risk awareness

\- escalation trends

\- leadership readability

\- scan-friendly formatting

\- operational interpretation



Executive summaries should prioritize:



\- SLA breaches

\- operationally critical vendors

\- recurring escalation patterns

\- corrective action exposure

\- continuity risk indicators



\---



\# Recommended Visualizations



Recommended future Power BI or reporting visualizations include:



| Visualization | Purpose |

|---|---|

| SLA compliance trend line | Vendor performance trend visibility |

| SLA breach rate bar chart | Vendor breach comparison |

| Escalation heat map | Operational disruption visibility |

| Corrective action trend chart | Vendor process instability visibility |

| Operational impact distribution chart | Severity concentration analysis |

| Vendor reliability scorecard | Leadership vendor evaluation |



\---



\# Cross-System Reporting Relationships



Vendor SLA reporting may integrate with:



| Related Dataset | Reporting Purpose |

|---|---|

| vendor-master.csv | Vendor identity and classification |

| vendor-shipments.csv | Shipment timing analysis |

| vendor-fulfillment-events.csv | Fulfillment reliability analysis |

| replenishment-events.csv | Inventory stabilization visibility |

| shortage-events.csv | Operational continuity risk analysis |

| tickets-v1.csv | Escalation trend analysis |



This supports:



\# enterprise operational intelligence reporting



across subsystem boundaries.



\---



\# Future SQL Readiness



This KPI framework supports future SQL integration through:



\- standardized KPI definitions

\- consistent relational identifiers

\- operationally meaningful aggregation logic

\- reusable reporting calculations



Future SQL reporting may support:



\- rolling vendor SLA averages

\- breach trend monitoring

\- escalation-linked vendor scoring

\- operational disruption analysis

\- vendor reliability ranking



\---



\# Future Power BI Readiness



This framework supports future Power BI development through:



\- KPI standardization

\- vendor performance segmentation

\- escalation trend visibility

\- operational impact analysis

\- reusable dashboard metric definitions



Potential dashboard layers include:



\- executive scorecards

\- operational heat maps

\- vendor comparison dashboards

\- escalation monitoring dashboards

\- operational continuity reporting



\---



\# Governance Alignment



This KPI framework follows established Northstar governance standards, including:



\- subsystem-centered architecture

\- reporting standardization methodology

\- shared identifier standards

\- governance-first operational modeling

\- SQL readiness

\- Power BI readiness



Future KPI additions should be made:



\# systematically



NOT:



\# reactively.



\---



\# Portfolio Significance



This framework demonstrates:



\- operational KPI architecture

\- vendor performance analysis design

\- escalation-aware reporting methodology

\- executive operational reporting strategy

\- enterprise systems thinking

\- Power BI reporting readiness

\- SQL analytical readiness

\- scalable operational intelligence planning



The Vendor SLA KPI Framework strengthens the Vendor Performance subsystem by establishing a standardized operational interpretation layer supporting vendor reliability monitoring, escalation analysis, operational continuity visibility, and leadership operational reporting.

