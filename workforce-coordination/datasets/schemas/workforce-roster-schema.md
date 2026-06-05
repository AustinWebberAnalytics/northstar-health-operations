# Workforce Roster Schema



## Purpose



The Workforce Roster dataset serves as the primary workforce reference table for the Workforce Coordination subsystem.



It provides visibility into workforce composition, organizational assignments, staffing availability, coverage priorities, and workforce capacity.



This dataset supports reporting, workforce planning, workload analysis, and staffing-related operational decision-making.



---



## Dataset Grain



One record per employee.



---



## Primary Key



employee_id



---



## Fields



| Field Name | Description |

|------------|-------------|

| employee_id | Unique employee identifier |

| employee_name | Employee full name |

| department | Department supported by the employee |

| team | Team assignment within the department |

| role | Primary operational role |

| employment_status | Current workforce status |

| primary_shift | Primary scheduled shift |

| standard_weekly_hours | Expected weekly working hours |

| skill_area | Primary operational specialty |

| coverage_priority | Relative importance of coverage continuity |

| active_flag | Indicates whether the employee is currently active |



---



## Valid Employment Status Values



| Value |

|---------|

| Active |

| Leave |



---



## Valid Shift Values



| Value |

|---------|

| Day |

| Evening |

| Variable |



---



## Valid Coverage Priority Values



| Value |

|---------|

| High |

| Moderate |

| Low |



---



## Data Quality Considerations



- Employee identifiers should remain unique.

- Active and inactive workforce records should be retained for historical reporting purposes.

- Coverage priority assignments should be reviewed periodically to reflect operational requirements.

- Weekly hour allocations should align with workforce scheduling practices.



---



## Operational Usage



This dataset supports:



- Workforce reporting

- Coverage planning

- Assignment management

- Capacity analysis

- Workload balancing

- Staffing escalation analysis



The Workforce Roster dataset serves as the foundational workforce reference table for all Workforce Coordination reporting and analysis activities.

