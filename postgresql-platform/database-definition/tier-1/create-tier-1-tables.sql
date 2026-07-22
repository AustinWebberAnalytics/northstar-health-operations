-- Northstar Health Operations
-- Purpose: Create the five approved Tier 1 PostgreSQL tables.
-- Authority: Tier 1 PostgreSQL Implementation Contract and issue #29.
-- Boundary: Tier 1 tables, approved keys, and approved constraints only;
--           no source data, migration logic, deferred Ticket foreign keys,
--           manually defined indexes, or later-tier objects.

BEGIN;

CREATE TABLE inventory.inventory_item (
    item_id TEXT NOT NULL,
    item_category TEXT NOT NULL,
    criticality_level TEXT NOT NULL,
    unit_of_measure TEXT NOT NULL,
    preferred_vendor_id TEXT,
    active_flag BOOLEAN NOT NULL,
    item_name TEXT NOT NULL,
    CONSTRAINT inventory_item_pkey PRIMARY KEY (item_id),
    CONSTRAINT inventory_item_preferred_vendor_id_fkey
        FOREIGN KEY (preferred_vendor_id)
        REFERENCES vendor.vendor (vendor_id)
        ON DELETE RESTRICT
);

CREATE TABLE ticketing.ticket (
    ticket_id TEXT NOT NULL,
    category TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    escalation_flag BOOLEAN NOT NULL,
    reopened_flag BOOLEAN NOT NULL,
    pending_flag BOOLEAN NOT NULL,
    sla_target_hours INTEGER NOT NULL,
    sla_met_flag BOOLEAN,
    requesting_location TEXT,
    location_id TEXT,
    assigned_department TEXT NOT NULL,
    assigned_owner TEXT,
    employee_id TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    first_response_at TIMESTAMP WITHOUT TIME ZONE,
    resolved_at TIMESTAMP WITHOUT TIME ZONE,
    closed_at TIMESTAMP WITHOUT TIME ZONE,
    resolution_hours NUMERIC(10,2),
    response_hours NUMERIC(10,2),
    summary TEXT,
    resolution_notes TEXT,
    CONSTRAINT ticket_pkey PRIMARY KEY (ticket_id)
);

CREATE TABLE workforce.assignment (
    assignment_id TEXT NOT NULL,
    employee_id TEXT NOT NULL,
    assignment_category TEXT NOT NULL,
    assignment_status TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    assignment_name TEXT NOT NULL,
    priority_level TEXT NOT NULL,
    estimated_hours_per_week INTEGER,
    cross_functional_flag BOOLEAN NOT NULL,
    CONSTRAINT assignment_pkey PRIMARY KEY (assignment_id),
    CONSTRAINT assignment_employee_id_fkey
        FOREIGN KEY (employee_id)
        REFERENCES workforce.employee (employee_id)
        ON DELETE RESTRICT
);

CREATE TABLE workforce.coverage_schedule (
    coverage_schedule_id TEXT NOT NULL,
    employee_id TEXT NOT NULL,
    schedule_date DATE NOT NULL,
    shift_type TEXT NOT NULL,
    coverage_status TEXT NOT NULL,
    scheduled_hours INTEGER,
    coverage_area TEXT,
    coverage_priority TEXT,
    backup_required_flag BOOLEAN,
    CONSTRAINT coverage_schedule_pkey PRIMARY KEY (coverage_schedule_id),
    CONSTRAINT coverage_schedule_employee_id_fkey
        FOREIGN KEY (employee_id)
        REFERENCES workforce.employee (employee_id)
        ON DELETE RESTRICT
);

CREATE TABLE workforce.workload_record (
    workload_record_id TEXT NOT NULL,
    employee_id TEXT NOT NULL,
    reporting_period TEXT NOT NULL,
    workload_status TEXT NOT NULL,
    assigned_tasks INTEGER NOT NULL,
    completed_tasks INTEGER NOT NULL,
    open_tasks INTEGER NOT NULL,
    estimated_hours NUMERIC(10,2),
    actual_hours NUMERIC(10,2),
    capacity_utilization_percent NUMERIC(5,2),
    CONSTRAINT workload_record_pkey PRIMARY KEY (workload_record_id),
    CONSTRAINT workload_record_employee_id_fkey
        FOREIGN KEY (employee_id)
        REFERENCES workforce.employee (employee_id)
        ON DELETE RESTRICT,
    CONSTRAINT workload_record_employee_id_reporting_period_key
        UNIQUE (employee_id, reporting_period)
);

COMMIT;
