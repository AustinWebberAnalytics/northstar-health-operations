-- Northstar Health Operations
-- Purpose: Create the three approved Tier 0 PostgreSQL tables.
-- Authority: Enterprise Relational Schema and issue #8.
-- Boundary: Tier 0 tables and primary keys only; no data or later-tier objects.

BEGIN;

CREATE TABLE core.location (
    location_id TEXT NOT NULL,
    CONSTRAINT location_pkey PRIMARY KEY (location_id)
);

CREATE TABLE workforce.employee (
    employee_id TEXT NOT NULL,
    employee_name TEXT NOT NULL,
    department TEXT NOT NULL,
    team TEXT NOT NULL,
    role TEXT NOT NULL,
    employment_status TEXT NOT NULL,
    active_flag BOOLEAN NOT NULL,
    primary_shift TEXT,
    standard_weekly_hours INTEGER,
    skill_area TEXT,
    coverage_priority TEXT,
    CONSTRAINT employee_pkey PRIMARY KEY (employee_id)
);

CREATE TABLE vendor.vendor (
    vendor_id TEXT NOT NULL,
    vendor_type TEXT NOT NULL,
    primary_service_category TEXT NOT NULL,
    risk_tier TEXT NOT NULL,
    active_vendor_flag BOOLEAN NOT NULL,
    vendor_name TEXT NOT NULL,
    support_level TEXT,
    preferred_vendor_flag BOOLEAN,
    emergency_fulfillment_flag BOOLEAN,
    primary_contact_team TEXT,
    notes TEXT,
    CONSTRAINT vendor_pkey PRIMARY KEY (vendor_id)
);

COMMIT;
