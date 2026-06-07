# Vendor Scorecard Framework

## Purpose

This document defines the vendor scorecard framework used within the Vendor Performance subsystem.

The framework establishes a standardized approach for evaluating overall vendor performance through the consolidation of operational performance, SLA outcomes, escalation activity, operational impact, and corrective action history.

Scorecards support vendor comparison, performance interpretation, operational prioritization, and leadership visibility across the Northstar Health Operations ecosystem.

---

# Scorecard Philosophy

Vendor scorecards should provide a consolidated operational view of vendor performance.

Scorecard evaluation considers:

* Performance consistency
* Service reliability
* Escalation exposure
* Operational impact
* Corrective action requirements

The objective is to summarize operational performance across multiple domains while preserving the underlying context that contributes to overall vendor evaluation.

Scorecards are intended to support operational decision-making rather than replace detailed subsystem analysis.

---

# Scorecard Governance Standards

Vendor scorecards should:

* Remain operationally relevant
* Support leadership visibility
* Maintain evaluation consistency
* Incorporate multiple performance domains
* Support cross-system interpretation
* Align with subsystem objectives

Scorecard outcomes should reflect recurring operational patterns rather than isolated events whenever possible.

---

# Scorecard Evaluation Categories

Vendor scorecards evaluate performance across five primary categories:

* SLA Performance
* Fulfillment Reliability
* Escalation Exposure
* Operational Impact Severity
* Corrective Action Dependency

Together, these categories provide a balanced view of vendor performance and operational reliability.

---

# SLA Performance

## Purpose

Evaluates vendor consistency in meeting operational service expectations.

## Evaluation Considerations

Scorecard evaluation may consider:

* SLA compliance rates
* SLA breach frequency
* Response performance
* Escalation-linked SLA activity

## Operational Significance

Strong SLA performance may indicate:

* Reliable vendor responsiveness
* Consistent operational support
* Reduced service disruption exposure

Weak SLA performance may indicate:

* Service instability
* Escalation pressure
* Increased operational oversight requirements

---

# Fulfillment Reliability

## Purpose

Evaluates consistency and stability of vendor fulfillment activity.

## Evaluation Considerations

Scorecard evaluation may consider:

* Delayed shipment frequency
* Partial fulfillment activity
* Fulfillment consistency
* Shipment stability

## Operational Significance

Strong fulfillment reliability may indicate:

* Stable replenishment support
* Improved operational continuity
* Reduced shortage exposure

Weak fulfillment reliability may indicate:

* Replenishment instability
* Inventory pressure
* Increased dependency risk

---

# Escalation Exposure

## Purpose

Evaluates the degree to which vendor activity contributes to operational escalation activity.

## Evaluation Considerations

Scorecard evaluation may consider:

* Escalation-required events
* Escalation-linked SLA failures
* Vendor-related incidents
* Escalation frequency trends

## Operational Significance

Elevated escalation exposure may indicate:

* Operational instability
* Vendor coordination challenges
* Increased workload requirements
* Greater disruption exposure

---

# Operational Impact Severity

## Purpose

Evaluates the severity of operational outcomes associated with vendor activity.

## Evaluation Considerations

Scorecard evaluation may consider event classifications such as:

```text
Low
Moderate
High
Critical
```

## Operational Significance

Higher concentrations of severe-impact events may indicate:

* Continuity-sensitive dependencies
* Elevated operational risk
* Significant disruption exposure
* Operational bottlenecks

---

# Corrective Action Dependency

## Purpose

Evaluates how frequently vendor performance requires intervention or corrective action.

## Evaluation Considerations

Scorecard evaluation may consider:

* Corrective action requirements
* Repeated SLA failures
* Recurring fulfillment issues
* Ongoing remediation activity

## Operational Significance

Elevated corrective action dependency may indicate:

* Performance instability
* Increased oversight requirements
* Process inconsistency
* Vendor reliability concerns

---

# Scorecard Structure

Vendor scorecards may utilize weighted evaluation categories.

Example structure:

|Category|Example Weight|
|-|-|
|SLA Performance|30%|
|Fulfillment Reliability|30%|
|Escalation Exposure|20%|
|Operational Impact Severity|10%|
|Corrective Action Dependency|10%|

These weights are intended as operational examples and should be adjusted based on reporting objectives and organizational priorities.

---

# Vendor Performance Tiers

Vendor scorecards may classify vendors into performance tiers.

Example structure:

|Tier|Interpretation|
|-|-|
|Preferred|Highly stable operational vendor|
|Stable|Reliable operational vendor|
|Monitoring|Periodic review recommended|
|At Risk|Elevated operational concerns|
|Critical Review|Significant operational instability|

Performance tiers provide a standardized framework for vendor comparison and prioritization.

---

# KPI Relationships

Vendor scorecards incorporate information from:

* Vendor Performance Reporting
* Vendor SLA Monitoring
* Vendor Risk Classification
* Corrective Action Tracking

Shared identifiers supporting scorecard evaluation include:

```text
vendor_id
sla_event_id
fulfillment_event_id
shipment_id
related_ticket_id
```

These relationships support integrated vendor evaluation and cross-functional reporting.

---

# Reporting Standards

Scorecard reporting should emphasize:

* Vendor comparison
* Performance trends
* Escalation exposure
* Operational reliability
* Emerging performance concerns

Reporting outputs should prioritize concise interpretation, leadership readability, and actionable operational insights.

---

# Governance Alignment

This framework follows established Northstar governance standards including:

* Subsystem-centered architecture
* Reporting standardization principles
* Documentation layering standards
* Naming convention standards
* Cross-system integration practices

Changes to scorecard methodology should be evaluated for consistency, reporting impact, and subsystem alignment before implementation.

---

# Summary

The Vendor Scorecard Framework establishes a standardized methodology for evaluating overall vendor performance across multiple operational domains.

By consolidating performance, SLA outcomes, escalation activity, operational impact, and corrective action history, the framework provides a consistent foundation for vendor comparison, operational prioritization, and leadership reporting.

