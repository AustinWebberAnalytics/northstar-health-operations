-- Northstar Enterprise
-- Purpose: Create the five approved Tier 2 PostgreSQL tables.
-- Authority: Tier 2 PostgreSQL Implementation Contract and issue #32.
-- Boundary: Tier 2 tables, approved keys, and approved constraints only;
--           no source data, migration logic, deferred Ticket foreign keys,
--           manually defined indexes, or later-tier objects.

BEGIN;

CREATE TABLE vendor.shipment (
    shipment_id TEXT NOT NULL,
    vendor_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    location_id TEXT NOT NULL,
    related_ticket_id TEXT,
    delivery_status TEXT NOT NULL,
    ordered_quantity INTEGER NOT NULL,
    received_quantity INTEGER,
    order_date DATE NOT NULL,
    expected_delivery_date DATE NOT NULL,
    actual_delivery_date DATE,
    fulfillment_accuracy_flag BOOLEAN,
    delay_flag BOOLEAN NOT NULL,
    CONSTRAINT shipment_pkey PRIMARY KEY (shipment_id),
    CONSTRAINT shipment_vendor_id_fkey
        FOREIGN KEY (vendor_id)
        REFERENCES vendor.vendor (vendor_id)
        ON DELETE RESTRICT,
    CONSTRAINT shipment_item_id_fkey
        FOREIGN KEY (item_id)
        REFERENCES inventory.inventory_item (item_id)
        ON DELETE RESTRICT,
    CONSTRAINT shipment_location_id_fkey
        FOREIGN KEY (location_id)
        REFERENCES core.location (location_id)
        ON DELETE RESTRICT,
    CONSTRAINT shipment_related_ticket_id_fkey
        FOREIGN KEY (related_ticket_id)
        REFERENCES ticketing.ticket (ticket_id)
        ON DELETE RESTRICT
);

CREATE TABLE inventory.replenishment (
    replenishment_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    location_id TEXT NOT NULL,
    vendor_id TEXT,
    related_ticket_id TEXT,
    replenishment_type TEXT NOT NULL,
    replenishment_status TEXT NOT NULL,
    requested_quantity INTEGER NOT NULL,
    approved_quantity INTEGER,
    request_date DATE NOT NULL,
    expected_arrival_date DATE,
    received_date DATE,
    CONSTRAINT replenishment_pkey PRIMARY KEY (replenishment_id),
    CONSTRAINT replenishment_item_id_fkey
        FOREIGN KEY (item_id)
        REFERENCES inventory.inventory_item (item_id)
        ON DELETE RESTRICT,
    CONSTRAINT replenishment_location_id_fkey
        FOREIGN KEY (location_id)
        REFERENCES core.location (location_id)
        ON DELETE RESTRICT,
    CONSTRAINT replenishment_vendor_id_fkey
        FOREIGN KEY (vendor_id)
        REFERENCES vendor.vendor (vendor_id)
        ON DELETE RESTRICT,
    CONSTRAINT replenishment_related_ticket_id_fkey
        FOREIGN KEY (related_ticket_id)
        REFERENCES ticketing.ticket (ticket_id)
        ON DELETE RESTRICT
);

CREATE TABLE inventory.location_inventory (
    location_inventory_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    location_id TEXT NOT NULL,
    current_stock INTEGER NOT NULL,
    stock_status TEXT NOT NULL,
    reorder_point INTEGER,
    target_stock_level INTEGER,
    safety_stock_level INTEGER,
    last_count_date DATE,
    CONSTRAINT location_inventory_pkey PRIMARY KEY (location_inventory_id),
    CONSTRAINT location_inventory_item_id_fkey
        FOREIGN KEY (item_id)
        REFERENCES inventory.inventory_item (item_id)
        ON DELETE RESTRICT,
    CONSTRAINT location_inventory_location_id_fkey
        FOREIGN KEY (location_id)
        REFERENCES core.location (location_id)
        ON DELETE RESTRICT,
    CONSTRAINT location_inventory_location_id_item_id_key
        UNIQUE (location_id, item_id)
);

CREATE TABLE workforce.workforce_escalation (
    escalation_id TEXT NOT NULL,
    related_ticket_id TEXT,
    department TEXT NOT NULL,
    escalation_type TEXT NOT NULL,
    severity_level TEXT NOT NULL,
    current_status TEXT NOT NULL,
    escalation_date DATE NOT NULL,
    affected_team TEXT,
    root_cause TEXT,
    resolution_owner TEXT,
    business_impact TEXT,
    CONSTRAINT workforce_escalation_pkey PRIMARY KEY (escalation_id),
    CONSTRAINT workforce_escalation_related_ticket_id_fkey
        FOREIGN KEY (related_ticket_id)
        REFERENCES ticketing.ticket (ticket_id)
        ON DELETE RESTRICT
);

CREATE TABLE relationships.assignment_ticket (
    assignment_id TEXT NOT NULL,
    ticket_id TEXT NOT NULL,
    CONSTRAINT assignment_ticket_pkey PRIMARY KEY (assignment_id, ticket_id),
    CONSTRAINT assignment_ticket_assignment_id_fkey
        FOREIGN KEY (assignment_id)
        REFERENCES workforce.assignment (assignment_id)
        ON DELETE RESTRICT,
    CONSTRAINT assignment_ticket_ticket_id_fkey
        FOREIGN KEY (ticket_id)
        REFERENCES ticketing.ticket (ticket_id)
        ON DELETE RESTRICT
);

COMMIT;
