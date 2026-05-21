\# Inventory KPI Framework  

\## Northstar Health Operations



\---



\# Purpose



This document defines the operational KPI framework for the Northstar Health Operations Inventory \& Supply Operations subsystem.



The purpose of the KPI framework is to identify measurable operational indicators used to monitor:

\- inventory stability

\- replenishment performance

\- shortage risk

\- vendor reliability

\- inventory accuracy

\- operational continuity

\- supply chain workflow health



This framework supports:

\- operational monitoring

\- leadership reporting

\- escalation visibility

\- process improvement analysis

\- executive operational briefings



\---



\# KPI Framework Overview



The Inventory \& Supply Operations subsystem tracks operational performance across several major categories:



| KPI Category | Operational Focus |

|---|---|

| Inventory Availability | Current inventory health |

| Replenishment Performance | Inventory workflow efficiency |

| Shortage Risk Monitoring | Operational disruption exposure |

| Vendor Performance | Supplier reliability |

| Inventory Accuracy | Reconciliation and integrity |

| Escalation Activity | Operational pressure visibility |



\---



\# Inventory Availability KPIs



These KPIs measure current operational inventory stability.



\---



\## Low Stock Item Count



\### Definition



Number of inventory records currently below established reorder thresholds.



\### Operational Importance



Helps identify:

\- replenishment pressure

\- inventory instability

\- elevated shortage risk



\### Related Dataset



```text

location-inventory.csv

```



\### Example Metric



```text

5 inventory items currently below reorder point

```



\---



\## Critical Low Inventory Count



\### Definition



Number of inventory records classified as:

\- Critical Low

\- Stockout



\### Operational Importance



Highlights operational continuity risk and high-priority inventory concerns.



\### Related Dataset



```text

location-inventory.csv

```



\---



\## Stockout Event Count



\### Definition



Number of inventory records currently in:

```text

Stockout

```

status.



\### Operational Importance



Tracks operational interruption exposure and shortage severity.



\### Related Dataset



```text

location-inventory.csv

```



\---



\# Replenishment Performance KPIs



These KPIs measure replenishment workflow effectiveness.



\---



\## Replenishment Turnaround Time



\### Definition



Average time between:

\- replenishment request

and

\- inventory receipt



\### Operational Importance



Measures replenishment workflow efficiency.



\### Related Dataset



```text

replenishment-events.csv

```



\---



\## Delayed Replenishment Count



\### Definition



Number of replenishment events currently marked:

```text

Delayed

```



\### Operational Importance



Highlights workflow bottlenecks and vendor coordination risk.



\### Related Dataset



```text

replenishment-events.csv

```



\---



\## In-Transit Replenishment Volume



\### Definition



Number of replenishment events currently in:

```text

In Transit

```

status.



\### Operational Importance



Measures active replenishment pipeline volume.



\### Related Dataset



```text

replenishment-events.csv

```



\---



\# Shortage Risk KPIs



These KPIs monitor operational disruption exposure.



\---



\## Active Shortage Event Count



\### Definition



Number of unresolved shortage events.



\### Operational Importance



Measures current operational inventory disruption.



\### Related Dataset



```text

shortage-events.csv

```



\---



\## Critical Shortage Count



\### Definition



Number of shortages classified as:

```text

Critical

```



\### Operational Importance



Tracks high-risk operational inventory disruptions.



\### Related Dataset



```text

shortage-events.csv

```



\---



\## Escalated Shortage Count



\### Definition



Number of shortage events with:

```text

escalation\_flag = TRUE

```



\### Operational Importance



Measures operational pressure requiring elevated visibility.



\### Related Dataset



```text

shortage-events.csv

```



\---



\# Vendor Performance KPIs



These KPIs monitor supplier reliability and shipment performance.



\---



\## Vendor Delay Rate



\### Definition



Percentage of vendor shipments marked:

```text

delay\_flag = TRUE

```



\### Operational Importance



Measures vendor timeliness and supply chain stability.



\### Related Dataset



```text

vendor-shipments.csv

```



\---



\## Fulfillment Accuracy Rate



\### Definition



Percentage of shipments where:

```text

fulfillment\_accuracy\_flag = TRUE

```



\### Operational Importance



Measures shipment completeness and receiving accuracy.



\### Related Dataset



```text

vendor-shipments.csv

```



\---



\## Partial Shipment Count



\### Definition



Number of shipments marked:

```text

Partial

```



\### Operational Importance



Tracks incomplete fulfillment events impacting operational continuity.



\### Related Dataset



```text

vendor-shipments.csv

```



\---



\# Inventory Accuracy KPIs



These KPIs monitor inventory integrity and reconciliation quality.



\---



\## Inventory Discrepancy Count



\### Definition



Total number of inventory discrepancy records.



\### Operational Importance



Measures operational inventory integrity pressure.



\### Related Dataset



```text

inventory-discrepancies.csv

```



\---



\## Open Discrepancy Count



\### Definition



Number of discrepancies not yet resolved.



\### Operational Importance



Tracks unresolved inventory reconciliation workload.



\### Related Dataset



```text

inventory-discrepancies.csv

```



\---



\## Inventory Accuracy Rate



\### Definition



Percentage of inventory counts without discrepancy variance.



\### Operational Importance



Measures overall inventory reporting reliability.



\### Related Dataset



```text

inventory-discrepancies.csv

```



\---



\# Escalation Activity KPIs



These KPIs monitor operational pressure and workflow risk.



\---



\## Escalated Operational Events



\### Definition



Total operational events linked to escalation activity.



Includes:

\- shortages

\- delayed replenishments

\- discrepancy escalations

\- vendor disruption events



\### Operational Importance



Measures operational instability requiring elevated management visibility.



\### Related Datasets



```text

shortage-events.csv

replenishment-events.csv

inventory-discrepancies.csv

vendor-shipments.csv

```



\---



\# Future Reporting Opportunities



This KPI framework will support future:

\- Excel pivot reporting

\- Power BI dashboards

\- SQL KPI calculations

\- vendor scorecards

\- operational forecasting

\- executive reporting summaries

\- process improvement recommendations



\---



\# Executive Reporting Value



This KPI framework is designed to simulate realistic operational leadership reporting used to monitor:

\- inventory health

\- operational continuity

\- supply chain stability

\- replenishment efficiency

\- escalation exposure

\- vendor reliability



These KPIs intentionally mirror operational metrics commonly used within:

\- healthcare operations

\- clinical supply management

\- warehouse operations

\- regulated inventory environments

\- enterprise operational support organizations



\---



\# Portfolio Significance



This framework demonstrates:

\- operational KPI reasoning

\- workflow measurement understanding

\- supply chain operational awareness

\- inventory analytics planning

\- operational reporting design

\- executive communication thinking

\- enterprise operational systems reasoning



This KPI framework significantly expands the analytical maturity of the Northstar Health Operations ecosystem.

