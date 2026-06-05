## Foreign Key



employee_id



References workforce-roster.employee_id



---



## Fields



| Field Name | Description |

|------------|-------------|

| assignment_id | Unique assignment identifier |

| employee_id | Employee assigned to the work |

| assignment_name | Name of the assigned responsibility |

| assignment_category | Operational category of the assignment |

| priority_level | Relative priority of the assignment |

| estimated_hours_per_week | Estimated weekly effort required |

| assignment_status | Current status of the assignment |

| start_date | Date the assignment began |

| end_date | Date the assignment ended, if applicable |

| cross_functional_flag | Indicates whether the assignment supports more than one operational area |



---



## Valid Assignment Category Values



| Value |

|---------|

| Ticketing |

| Inventory Operations |

| Vendor Management |

| Escalation Management |

| Workforce Coordination |



---



## Valid Priority Level Values



| Value |

|---------|

| Critical |

| High |

| Moderate |

| Low |



---



## Valid Assignment Status Values



| Value |

|---------|

| Active |

| Suspended |



---



## Data Quality Considerations



- Each assignment should reference a valid employee_id from the Workforce Roster dataset.

- Suspended assignments should remain in the dataset for historical and operational visibility.

- Estimated hours should be reviewed against workload and capacity reporting.

- Cross-functional assignments should be monitored because they may increase coordination complexity.



---



## Operational Usage



This dataset supports:



- Assignment tracking

- Workload distribution analysis

- Capacity planning

- Cross-functional support monitoring

- Staffing risk identification

- Workforce utilization reporting



The Workforce Assignments dataset helps connect available personnel to the operational responsibilities they are expected to support.

