# Enterprise Object Model



**Writing Layer:** Layer 2 – Operational / Architectural



---



# Purpose



The Enterprise Object Model defines the canonical business objects that exist within the Northstar enterprise.



An enterprise object represents a distinct business entity with its own purpose, identity, lifecycle, and relationships within the organization. Objects exist independently of any implementation technology and serve as the conceptual foundation for future relational design, reporting, and enterprise simulation.



This document establishes a common enterprise vocabulary by defining what exists within Northstar before defining how those entities are implemented or related.



---



# Relationship to Enterprise Architecture



The Enterprise Object Model is one of the foundational architecture documents within Northstar.



Its purpose is to define the enterprise's canonical business entities.



This document should be read in conjunction with the following architecture documents:



- **Enterprise System Map** — Defines the operational domains and subsystem boundaries of the enterprise.

- **Enterprise Relational Model** *(future)* — Defines how enterprise objects relate to one another.

- **Cross-System Identifier Dictionary** — Defines authoritative identifiers shared across operational domains.



The Enterprise Object Model intentionally does **not** define:



- database tables,

- SQL implementation,

- field-level specifications,

- foreign key relationships,

- reporting logic,

- simulation mechanics.



Those concerns belong to later engineering artifacts.



---



# Object Philosophy



Northstar models the enterprise rather than its software.



For that reason, enterprise objects are derived from the operational needs of the organization instead of implementation technologies.



Objects are not created because they are commonly found in enterprise software. Every object included within this model represents a business concept that already exists within the repository and participates in meaningful operational activity.



The object model therefore serves as the conceptual bridge between enterprise architecture and future implementation.



Future relational models, datasets, SQL schemas, reports, and simulation components should all be derived from the objects defined in this document.



---



# Canonical Object Classification



Enterprise objects are organized according to the role they perform within the organization.



## Reference Objects



Stable entities that define the enterprise itself.



Examples include people, locations, vendors, and inventory items.



---



## Operational Work Objects



Objects that coordinate, assign, or manage enterprise work.



These represent operational activity requiring ownership and execution.



---



## Movement Objects



Objects that represent the movement of materials or operational resources throughout the enterprise.



---



## Operational State Objects



Objects that describe the current condition of the enterprise at a point in time.



These objects capture operational status rather than individual work activities.



---



## Assessment Objects



Objects that evaluate operational performance, compliance, or enterprise conditions.



Assessment objects support operational intelligence and future decision-making.



---



# Enterprise Object Hierarchy



```text

Reference Objects

│

├── Location

├── Employee

├── Vendor

└── Inventory Item



↓



Operational Work Objects

│

├── Ticket

├── Assignment

└── Corrective Action



↓



Movement Objects

│

├── Shipment

└── Replenishment



↓



Operational State Objects

│

├── Location Inventory

├── Inventory Discrepancy

├── Shortage

├── Coverage Schedule

└── Workload Record



↓



Assessment Objects

│

├── Fulfillment Event

├── SLA Event

└── Workforce Escalation

```

