\# Vendor Performance



\## Northstar Health Operations



\---



\# Overview



The Vendor Performance subsystem tracks vendor reliability, fulfillment stability, SLA compliance, and escalation-related supplier activity within Northstar Health Operations.



This subsystem focuses on how vendor behavior affects:



\- inventory continuity

\- replenishment stability

\- shortage exposure

\- operational escalations

\- leadership visibility



\---



\# Subsystem Purpose



The purpose of this subsystem is to support operational visibility into:



\- vendor fulfillment outcomes

\- shipment and delivery reliability

\- SLA performance

\- corrective action needs

\- vendor-related escalation pressure

\- operational continuity risk



This subsystem functions as the supplier operational intelligence layer of the Northstar ecosystem.



\---



\# Folder Structure



```text

vendor-performance/



├── datasets/

├── documentation/

├── reporting-and-kpis/

├── workflow-diagrams/

└── process-improvement/

```



\---



\# Current Datasets



| Dataset | Purpose |

|---|---|

| vendor-master.csv | Defines vendor identity and classification |

| vendor-fulfillment-events.csv | Tracks fulfillment outcomes, delays, partial shipments, and escalation-linked events |

| vendor-sla-tracking.csv | Tracks SLA compliance, breaches, escalation requirements, and corrective action needs |



Each dataset has a matching schema file in:



```text

vendor-performance/datasets/

```



\---



\# Current Documentation



| Document | Purpose |

|---|---|

| documentation/vendor-performance-subsystem-overview.md | Defines subsystem purpose, scope, and cross-system role |

| workflow-diagrams/vendor-fulfillment-escalation-workflow.md | Defines vendor fulfillment and escalation workflow behavior |

| reporting-and-kpis/vendor-performance-kpi-framework.md | Defines broad vendor performance KPI categories |

| reporting-and-kpis/vendor-sla-kpi-framework.md | Defines SLA-specific KPI interpretation standards |



\---



\# Key Relationships



The subsystem connects to other Northstar domains through shared identifiers.



| Identifier | Relationship |

|---|---|

| vendor\_id | Connects vendor records across vendor, inventory, and shipment data |

| shipment\_id | Connects shipment activity to fulfillment and SLA records |

| fulfillment\_event\_id | Connects fulfillment events to SLA tracking |

| related\_ticket\_id | Connects vendor issues to operational tickets |

| item\_id | Connects vendor activity to inventory items |

| location\_id | Connects vendor activity to operational locations |



\---



\# Current Role in the Ecosystem



Vendor Performance currently supports:



\- fulfillment event analysis

\- SLA breach monitoring

\- vendor escalation visibility

\- inventory dependency analysis

\- operational continuity reporting



Future expansion may include:



\- vendor scorecards

\- vendor escalation datasets

\- corrective action tracking

\- Power BI vendor dashboards

\- SQL-based vendor performance reporting

