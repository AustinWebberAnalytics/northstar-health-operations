-- Northstar Health Operations
-- Purpose: Create the six approved PostgreSQL schema namespaces.
-- Authority: Enterprise Database Platform Decision and issue #7.
-- Boundary: Namespace containers only; no tables or other database objects.

BEGIN;

CREATE SCHEMA IF NOT EXISTS core AUTHORIZATION CURRENT_USER;
CREATE SCHEMA IF NOT EXISTS workforce AUTHORIZATION CURRENT_USER;
CREATE SCHEMA IF NOT EXISTS vendor AUTHORIZATION CURRENT_USER;
CREATE SCHEMA IF NOT EXISTS inventory AUTHORIZATION CURRENT_USER;
CREATE SCHEMA IF NOT EXISTS ticketing AUTHORIZATION CURRENT_USER;
CREATE SCHEMA IF NOT EXISTS relationships AUTHORIZATION CURRENT_USER;

COMMIT;
