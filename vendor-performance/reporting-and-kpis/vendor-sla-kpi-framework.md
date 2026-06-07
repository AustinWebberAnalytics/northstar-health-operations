# Vendor SLA KPI Framework

## Purpose

This document defines the service-level agreement (SLA) performance metrics used within the Vendor Performance subsystem.

The framework establishes standardized measures for evaluating vendor compliance with operational service expectations, identifying SLA-related performance risks, and supporting vendor accountability reporting.

These KPIs provide visibility into vendor responsiveness, service reliability, escalation exposure, and operational disruption risk.

---

# KPI Philosophy

Vendor SLA performance should be evaluated through an operational lens.

SLA metrics are intended to measure:

* Service reliability
* Compliance consistency
* Vendor responsiveness
* Escalation exposure
* Operational impact

The objective is to understand how vendor SLA performance influences operational outcomes rather than evaluating SLA compliance as an isolated metric.

---

# KPI Governance Standards

Vendor SLA KPIs should:

* Remain operationally relevant
* Be supported by available data
* Support leadership visibility
* Maintain reporting consistency
* Support trend analysis
* Align with subsystem objectives

KPI interpretation should consider operational context and business impact in addition to compliance outcomes.

---

# Core KPI Domains

Vendor SLA analysis focuses on five primary domains:

* Compliance Performance
* Breach Activity
* Escalation Exposure
* Corrective Action Requirements
* Response Performance

These domains provide the foundation for SLA performance evaluation.

---

# Compliance Performance KPIs

## SLA Compliance Rate

### Purpose

Measures the percentage of SLA events that meet established operational expectations.

### Operational Relevance

Lower compliance rates may indicate:

* Vendor instability
* Fulfillment inconsistency
* Operational disruption exposure
* Service reliability concerns

### Formula

```text
(SLA Events Marked "Met" ÷ Total SLA Events) × 100
```

---

## SLA Breach Rate

### Purpose

Measures the percentage of SLA events that fail to meet established service expectations.

### Operational Relevance

Higher breach rates may indicate:

* Vendor performance concerns
* Operational workflow disruption
* Service instability
* Increased escalation exposure

### Formula

```text
(SLA Breach Events ÷ Total SLA Events) × 100
```

---

# Escalation Exposure KPIs

## Escalation-Linked SLA Rate

### Purpose

Measures the percentage of SLA events requiring operational escalation.

### Operational Relevance

Higher escalation rates may indicate:

* Vendor communication challenges
* Unresolved service issues
* Increased coordination requirements
* Operational instability

### Formula

```text
(Escalated SLA Events ÷ Total SLA Events) × 100
```

---

## Operational Impact Distribution

### Purpose

Measures SLA event distribution across operational impact levels.

### Operational Relevance

Higher concentrations of severe-impact events may indicate:

* Elevated operational risk
* Increased disruption exposure
* Service reliability concerns
* Greater escalation requirements

Example operational impact levels:

```text
Low
Moderate
High
Critical
```

---

# Corrective Action KPIs

## Corrective Action Rate

### Purpose

Measures the percentage of SLA events requiring corrective action.

### Operational Relevance

Higher corrective action rates may indicate:

* Recurring service failures
* Process instability
* Vendor performance concerns
* Increased oversight requirements

### Formula

```text
(Corrective Action Required Events ÷ Total SLA Events) × 100
```

---

# Response Performance KPIs

## Average SLA Response Time

### Purpose

Measures the average operational response duration associated with SLA events.

### Operational Relevance

Longer response times may contribute to:

* Extended service disruptions
* Escalation growth
* Operational delays
* Vendor accountability concerns

### Formula

```text
Total Actual Response Hours ÷ Total SLA Events
```

---

# KPI Relationships

Vendor SLA KPIs interact directly with:

* Vendor Performance Reporting
* Corrective Action Monitoring
* Escalation Management
* Operational Risk Evaluation

Shared identifiers supporting SLA analysis include:

```text
vendor_id
sla_event_id
shipment_id
fulfillment_event_id
related_ticket_id
```

These relationships support integrated operational reporting and cross-functional analysis.

---

# Reporting Standards

SLA reporting should emphasize:

* Compliance performance
* Breach activity
* Escalation exposure
* Corrective action requirements
* Response performance trends

Reporting outputs should prioritize concise operational interpretation and leadership visibility.

---

# Governance Alignment

This framework follows established Northstar governance standards including:

* Subsystem-centered architecture
* Reporting standardization principles
* Documentation layering standards
* Naming convention standards
* Cross-system integration practices

Changes to KPI definitions should be evaluated for consistency, reporting impact, and subsystem alignment before implementation.

---

# Summary

The Vendor SLA KPI Framework establishes the core measures used to evaluate service reliability, compliance performance, escalation exposure, corrective action requirements, and response effectiveness.

These KPIs provide a standardized foundation for SLA monitoring, vendor accountability reporting, and operational performance evaluation within the Vendor Performance subsystem.
