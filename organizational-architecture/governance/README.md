# Governance

## Northstar Health Operations

---
**Primary Audience:** Northstar architects, maintainers, reviewers, and contributors responsible for repository-wide consistency

**Writing Layer:** Layer 1 — Reader-Facing

**Architectural Purpose:** Provides the navigable index to the standards and decision records that govern Northstar naming, identity, severity, remediation, and controlled evolution.

---
# Purpose

Governance defines the rules Northstar follows.

These artifacts control repository structure, naming, cross-system identity, remediation, and change management. They are not suggestions or examples. Approved governance documents are authoritative within their stated scope.

---
# Authoritative Governance Artifacts

## [Project Governance Standards](project-governance-standards.md)

Defines repository authority, change control, validation expectations, and governance discipline.

## [Naming Convention Standards](naming-convention-standards.md)

Defines governed naming for folders, files, datasets, fields, identifiers, and reporting artifacts.

## [Cross-System Identifier Dictionary](cross-system-identifier-dictionary.md)

Defines current canonical identifier names, formats, examples, ownership, relationship use, and migration aliases.

## [Enterprise Identifier Governance Review](enterprise-identifier-governance-review.md)

Records why canonical identifiers were approved, renamed, or corrected. This decision record and the identifier dictionary must remain synchronized.

## [Operational Severity Framework](operational-severity-framework.md)

Defines the common severity language used to evaluate operational conditions across domains.

## [Remediation Standards](remediation-standards.md)

Defines how findings are classified, assigned, validated, and closed.

---
# Authority Rule

Governance outranks architecture examples, subsystem conventions, implementation shortcuts, and historical reviews.

When a governed name or identifier changes, affected architecture and implementation artifacts must be reconciled before the new baseline is locked.

---
# Archive

The [archive](archive/) preserves superseded governance material for historical traceability. Archived documents do not define the current operating standard.

