# Vendor Performance KPI Framework

## Purpose

This document defines the core performance metrics used within the Vendor Performance subsystem.

The framework establishes standardized measures for evaluating vendor fulfillment activity, shipment performance, escalation contribution, and operational reliability.

These KPIs support operational monitoring, performance reporting, and vendor performance interpretation across the Northstar Health Operations ecosystem.

---

# KPI Philosophy

The Vendor Performance subsystem follows a workflow-centered operational intelligence approach.

KPIs are intended to measure:

* Vendor reliability
* Fulfillment performance
* Shipment stability
* Escalation contribution
* Operational impact

The objective is to understand how vendor performance influences operational outcomes rather than evaluating vendors through isolated administrative metrics.

---

# KPI Governance Standards

Vendor performance KPIs should:

* Remain operationally relevant
* Be supported by available data
* Support leadership visibility
* Maintain reporting consistency
* Support cross-system analysis
* Align with subsystem objectives

KPI interpretation should emphasize operational context rather than individual performance metrics in isolation.

---

# Core KPI Domains

Vendor performance analysis focuses on four primary domains:

* Fulfillment Performance
* Shipment Stability
* Escalation Activity
* Operational Visibility

These domains provide the foundation for performance evaluation within the subsystem.

---

# Fulfillment Performance KPIs

## On-Time Delivery Rate

### Purpose

Measures the percentage of shipments delivered within expected operational delivery windows.

### Operational Relevance

Low on-time delivery performance may contribute to:

* Replenishment instability
* Inventory shortages
* Workflow disruption
* Escalation activity

### Formula

```text
(On-Time Shipments ÷ Total Shipments) × 100
```

---

## Partial Fulfillment Rate

### Purpose

Measures how frequently vendors deliver incomplete shipments.

### Operational Relevance

High partial fulfillment rates may contribute to:

* Inventory shortages
* Replenishment delays
* Additional coordination activity
* Operational inefficiency

### Formula

```text
(Partial Shipments ÷ Total Shipments) × 100
```

---

# Shipment Stability KPIs

## Vendor Delay Frequency

### Purpose

Measures how frequently vendor shipments experience delays.

### Operational Relevance

Frequent delays may indicate:

* Vendor instability
* Fulfillment inconsistency
* Operational dependency exposure
* Increased workflow disruption risk

### Formula

```text
(Delayed Shipments ÷ Total Shipments) × 100
```

---

## Average Shipment Delay Duration

### Purpose

Measures the average duration of delayed shipments.

### Operational Relevance

Extended delays may contribute to:

* Inventory pressure
* Operational backlog
* Escalation activity
* Service disruption

### Formula

```text
Total Delay Duration ÷ Delayed Shipment Count
```

---

# Escalation Activity KPIs

## Vendor Escalation Contribution Rate

### Purpose

Measures how frequently vendor-related events generate operational escalations.

### Operational Relevance

High escalation contribution may indicate:

* Vendor instability
* Operational dependency risk
* Fulfillment disruption
* Increased coordination requirements

### Formula

```text
(Vendor Escalations ÷ Total Vendor Events) × 100
```

---

## Escalated Shipment Volume

### Purpose

Measures the number of shipments associated with operational escalations.

### Operational Relevance

Elevated escalated shipment volume may indicate:

* Shipment instability
* Vendor performance concerns
* Operational continuity risk

---

## Critical Vendor Incident Count

### Purpose

Tracks high-impact operational incidents associated with vendor activity.

### Operational Relevance

Critical incidents may contribute to:

* Service disruption
* Emergency operational response
* Leadership visibility requirements
* Escalation growth

---

# Operational Visibility KPIs

## Top Escalation-Contributing Vendors

### Purpose

Identifies vendors most frequently associated with operational escalations.

### Operational Relevance

Supports:

* Performance review activities
* Operational prioritization
* Escalation trend monitoring
* Vendor oversight

---

## Vendor Event Volume

### Purpose

Measures the volume of tracked vendor performance events within the reporting period.

### Operational Relevance

Provides context for:

* Performance interpretation
* Escalation analysis
* Operational workload visibility
* Reporting normalization

---

# KPI Relationships

Vendor Performance KPIs interact directly with:

* Inventory Operations
* Ticketing & Incident Management
* Vendor SLA Monitoring
* Vendor Risk Classification

Shared identifiers supporting cross-system analysis include:

```text
vendor_id
shipment_id
related_ticket_id
fulfillment_event_id
```

These relationships support integrated operational reporting and cross-functional analysis.

---

# Executive Reporting Standards

Executive reporting should emphasize:

* Vendor reliability
* Shipment performance
* Escalation contribution
* Operational disruption exposure
* Emerging performance concerns

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

The Vendor Performance KPI Framework establishes the core metrics used to evaluate vendor reliability, fulfillment performance, shipment stability, and escalation contribution.

These measures provide a standardized foundation for operational reporting, performance monitoring, and vendor performance analysis across the Northstar Health Operations ecosystem.

