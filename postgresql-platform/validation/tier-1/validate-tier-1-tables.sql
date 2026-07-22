-- Northstar Health Operations
-- Purpose: Confirm that the five approved Tier 1 tables match the approved
--          PostgreSQL physical implementation contract.
-- Authority: Tier 1 PostgreSQL Implementation Contract and issue #29.
-- Boundary: Read-only validation of the five named Tier 1 tables; cumulative
--           repository-wide relation inventory remains the responsibility of
--           validate-implementation-foundation.sql.
-- PostgreSQL 18 metadata note: pg_constraint.contype = 'n' represents NOT NULL
-- constraints separately from ordinary CHECK constraints, which use contype = 'c'.

DO $validation$
DECLARE
    validation_errors TEXT;
    actual_column_count INTEGER;
    target_table RECORD;
    table_has_rows BOOLEAN;
    nonempty_tables TEXT := NULL;
BEGIN
    WITH expected_tables (table_order, schema_name, table_name) AS (
        VALUES
            (1, 'inventory', 'inventory_item'),
            (2, 'ticketing', 'ticket'),
            (3, 'workforce', 'assignment'),
            (4, 'workforce', 'coverage_schedule'),
            (5, 'workforce', 'workload_record')
    ),
    table_mismatches AS (
        SELECT
            expected_tables.table_order,
            expected_tables.schema_name,
            expected_tables.table_name,
            actual_tables.table_type
        FROM expected_tables
        LEFT JOIN information_schema.tables AS actual_tables
            ON actual_tables.table_schema = expected_tables.schema_name
            AND actual_tables.table_name = expected_tables.table_name
        WHERE actual_tables.table_type IS DISTINCT FROM 'BASE TABLE'
    )
    SELECT string_agg(
        format(
            '%I.%I: expected BASE TABLE, found %s',
            schema_name,
            table_name,
            COALESCE(table_type, 'missing')
        ),
        '; ' ORDER BY table_order
    )
    INTO validation_errors
    FROM table_mismatches;

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Tier 1 table validation failed: %',
            validation_errors;
    END IF;

    SELECT count(*)
    INTO actual_column_count
    FROM information_schema.columns AS actual_columns
    WHERE (actual_columns.table_schema, actual_columns.table_name) IN (
        VALUES
            ('inventory', 'inventory_item'),
            ('ticketing', 'ticket'),
            ('workforce', 'assignment'),
            ('workforce', 'coverage_schedule'),
            ('workforce', 'workload_record')
    );

    IF actual_column_count <> 58 THEN
        RAISE EXCEPTION
            'Tier 1 column-count validation failed. Expected 58 columns across the five governed tables; found %.',
            actual_column_count;
    END IF;

    WITH expected_columns (
        table_order,
        schema_name,
        table_name,
        ordinal_position,
        column_name,
        data_type,
        numeric_precision,
        numeric_scale,
        is_nullable
    ) AS (
        VALUES
            (1, 'inventory', 'inventory_item', 1, 'item_id', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (1, 'inventory', 'inventory_item', 2, 'item_category', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (1, 'inventory', 'inventory_item', 3, 'criticality_level', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (1, 'inventory', 'inventory_item', 4, 'unit_of_measure', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (1, 'inventory', 'inventory_item', 5, 'preferred_vendor_id', 'text', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (1, 'inventory', 'inventory_item', 6, 'active_flag', 'boolean', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (1, 'inventory', 'inventory_item', 7, 'item_name', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (2, 'ticketing', 'ticket', 1, 'ticket_id', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (2, 'ticketing', 'ticket', 2, 'category', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (2, 'ticketing', 'ticket', 3, 'priority', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (2, 'ticketing', 'ticket', 4, 'status', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (2, 'ticketing', 'ticket', 5, 'escalation_flag', 'boolean', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (2, 'ticketing', 'ticket', 6, 'reopened_flag', 'boolean', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (2, 'ticketing', 'ticket', 7, 'pending_flag', 'boolean', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (2, 'ticketing', 'ticket', 8, 'sla_target_hours', 'integer', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (2, 'ticketing', 'ticket', 9, 'sla_met_flag', 'boolean', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (2, 'ticketing', 'ticket', 10, 'requesting_location', 'text', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (2, 'ticketing', 'ticket', 11, 'location_id', 'text', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (2, 'ticketing', 'ticket', 12, 'assigned_department', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (2, 'ticketing', 'ticket', 13, 'assigned_owner', 'text', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (2, 'ticketing', 'ticket', 14, 'employee_id', 'text', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (2, 'ticketing', 'ticket', 15, 'created_at', 'timestamp without time zone', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (2, 'ticketing', 'ticket', 16, 'first_response_at', 'timestamp without time zone', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (2, 'ticketing', 'ticket', 17, 'resolved_at', 'timestamp without time zone', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (2, 'ticketing', 'ticket', 18, 'closed_at', 'timestamp without time zone', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (2, 'ticketing', 'ticket', 19, 'resolution_hours', 'numeric', 10, 2, 'YES'),
            (2, 'ticketing', 'ticket', 20, 'response_hours', 'numeric', 10, 2, 'YES'),
            (2, 'ticketing', 'ticket', 21, 'summary', 'text', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (2, 'ticketing', 'ticket', 22, 'resolution_notes', 'text', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (3, 'workforce', 'assignment', 1, 'assignment_id', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (3, 'workforce', 'assignment', 2, 'employee_id', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (3, 'workforce', 'assignment', 3, 'assignment_category', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (3, 'workforce', 'assignment', 4, 'assignment_status', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (3, 'workforce', 'assignment', 5, 'start_date', 'date', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (3, 'workforce', 'assignment', 6, 'end_date', 'date', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (3, 'workforce', 'assignment', 7, 'assignment_name', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (3, 'workforce', 'assignment', 8, 'priority_level', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (3, 'workforce', 'assignment', 9, 'estimated_hours_per_week', 'integer', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (3, 'workforce', 'assignment', 10, 'cross_functional_flag', 'boolean', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (4, 'workforce', 'coverage_schedule', 1, 'coverage_schedule_id', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (4, 'workforce', 'coverage_schedule', 2, 'employee_id', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (4, 'workforce', 'coverage_schedule', 3, 'schedule_date', 'date', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (4, 'workforce', 'coverage_schedule', 4, 'shift_type', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (4, 'workforce', 'coverage_schedule', 5, 'coverage_status', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (4, 'workforce', 'coverage_schedule', 6, 'scheduled_hours', 'integer', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (4, 'workforce', 'coverage_schedule', 7, 'coverage_area', 'text', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (4, 'workforce', 'coverage_schedule', 8, 'coverage_priority', 'text', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (4, 'workforce', 'coverage_schedule', 9, 'backup_required_flag', 'boolean', NULL::INTEGER, NULL::INTEGER, 'YES'),
            (5, 'workforce', 'workload_record', 1, 'workload_record_id', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (5, 'workforce', 'workload_record', 2, 'employee_id', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (5, 'workforce', 'workload_record', 3, 'reporting_period', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (5, 'workforce', 'workload_record', 4, 'workload_status', 'text', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (5, 'workforce', 'workload_record', 5, 'assigned_tasks', 'integer', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (5, 'workforce', 'workload_record', 6, 'completed_tasks', 'integer', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (5, 'workforce', 'workload_record', 7, 'open_tasks', 'integer', NULL::INTEGER, NULL::INTEGER, 'NO'),
            (5, 'workforce', 'workload_record', 8, 'estimated_hours', 'numeric', 10, 2, 'YES'),
            (5, 'workforce', 'workload_record', 9, 'actual_hours', 'numeric', 10, 2, 'YES'),
            (5, 'workforce', 'workload_record', 10, 'capacity_utilization_percent', 'numeric', 5, 2, 'YES')
    ),
    actual_columns AS (
        SELECT
            columns.table_schema AS schema_name,
            columns.table_name,
            columns.ordinal_position,
            columns.column_name,
            columns.data_type,
            CASE WHEN columns.data_type = 'numeric' THEN columns.numeric_precision END AS numeric_precision,
            CASE WHEN columns.data_type = 'numeric' THEN columns.numeric_scale END AS numeric_scale,
            columns.is_nullable,
            columns.column_default,
            columns.is_identity,
            columns.is_generated
        FROM information_schema.columns AS columns
        WHERE (columns.table_schema, columns.table_name) IN (
            VALUES
                ('inventory', 'inventory_item'),
                ('ticketing', 'ticket'),
                ('workforce', 'assignment'),
                ('workforce', 'coverage_schedule'),
                ('workforce', 'workload_record')
        )
    ),
    column_mismatches AS (
        SELECT
            COALESCE(expected_columns.table_order, 99) AS table_order,
            COALESCE(expected_columns.schema_name, actual_columns.schema_name) AS schema_name,
            COALESCE(expected_columns.table_name, actual_columns.table_name) AS table_name,
            expected_columns.ordinal_position AS expected_ordinal_position,
            actual_columns.ordinal_position AS actual_ordinal_position,
            expected_columns.column_name AS expected_column_name,
            actual_columns.column_name AS actual_column_name,
            expected_columns.data_type AS expected_data_type,
            actual_columns.data_type AS actual_data_type,
            expected_columns.numeric_precision AS expected_numeric_precision,
            actual_columns.numeric_precision AS actual_numeric_precision,
            expected_columns.numeric_scale AS expected_numeric_scale,
            actual_columns.numeric_scale AS actual_numeric_scale,
            expected_columns.is_nullable AS expected_is_nullable,
            actual_columns.is_nullable AS actual_is_nullable,
            actual_columns.column_default,
            actual_columns.is_identity,
            actual_columns.is_generated
        FROM expected_columns
        FULL OUTER JOIN actual_columns
            ON actual_columns.schema_name = expected_columns.schema_name
            AND actual_columns.table_name = expected_columns.table_name
            AND actual_columns.column_name = expected_columns.column_name
        WHERE expected_columns.column_name IS NULL
            OR actual_columns.column_name IS NULL
            OR actual_columns.ordinal_position IS DISTINCT FROM expected_columns.ordinal_position
            OR actual_columns.data_type IS DISTINCT FROM expected_columns.data_type
            OR actual_columns.numeric_precision IS DISTINCT FROM expected_columns.numeric_precision
            OR actual_columns.numeric_scale IS DISTINCT FROM expected_columns.numeric_scale
            OR actual_columns.is_nullable IS DISTINCT FROM expected_columns.is_nullable
            OR actual_columns.column_default IS NOT NULL
            OR actual_columns.is_identity IS DISTINCT FROM 'NO'
            OR actual_columns.is_generated IS DISTINCT FROM 'NEVER'
    )
    SELECT string_agg(
        CASE
            WHEN expected_column_name IS NULL THEN format(
                '%I.%I.%I: unexpected column at position %s',
                schema_name,
                table_name,
                actual_column_name,
                actual_ordinal_position
            )
            WHEN actual_column_name IS NULL THEN format(
                '%I.%I.%I: approved column is missing',
                schema_name,
                table_name,
                expected_column_name
            )
            ELSE format(
                '%I.%I.%I: expected position=%s type=%s precision=%s scale=%s nullable=%s default=NULL identity=NO generated=NEVER; found position=%s type=%s precision=%s scale=%s nullable=%s default=%s identity=%s generated=%s',
                schema_name,
                table_name,
                expected_column_name,
                expected_ordinal_position,
                expected_data_type,
                COALESCE(expected_numeric_precision::TEXT, 'NULL'),
                COALESCE(expected_numeric_scale::TEXT, 'NULL'),
                expected_is_nullable,
                actual_ordinal_position,
                actual_data_type,
                COALESCE(actual_numeric_precision::TEXT, 'NULL'),
                COALESCE(actual_numeric_scale::TEXT, 'NULL'),
                actual_is_nullable,
                COALESCE(column_default, 'NULL'),
                is_identity,
                is_generated
            )
        END,
        '; ' ORDER BY table_order, COALESCE(expected_ordinal_position, actual_ordinal_position)
    )
    INTO validation_errors
    FROM column_mismatches;

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Tier 1 column-definition validation failed: %',
            validation_errors;
    END IF;

    WITH expected_tables (table_order, schema_name, table_name) AS (
        VALUES
            (1, 'inventory', 'inventory_item'),
            (2, 'ticketing', 'ticket'),
            (3, 'workforce', 'assignment'),
            (4, 'workforce', 'coverage_schedule'),
            (5, 'workforce', 'workload_record')
    ),
    ownership_mismatches AS (
        SELECT
            expected_tables.table_order,
            expected_tables.schema_name,
            expected_tables.table_name,
            actual_tables.tableowner
        FROM expected_tables
        LEFT JOIN pg_catalog.pg_tables AS actual_tables
            ON actual_tables.schemaname = expected_tables.schema_name
            AND actual_tables.tablename = expected_tables.table_name
        WHERE actual_tables.tableowner IS DISTINCT FROM 'northstar_local_admin'
    )
    SELECT string_agg(
        format(
            '%I.%I: expected owner northstar_local_admin, found %s',
            schema_name,
            table_name,
            COALESCE(tableowner, 'missing table')
        ),
        '; ' ORDER BY table_order
    )
    INTO validation_errors
    FROM ownership_mismatches;

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Tier 1 table-ownership validation failed: %',
            validation_errors;
    END IF;

    WITH expected_primary_keys (
        table_order,
        schema_name,
        table_name,
        constraint_name,
        key_position,
        column_name
    ) AS (
        VALUES
            (1, 'inventory', 'inventory_item', 'inventory_item_pkey', 1, 'item_id'),
            (2, 'ticketing', 'ticket', 'ticket_pkey', 1, 'ticket_id'),
            (3, 'workforce', 'assignment', 'assignment_pkey', 1, 'assignment_id'),
            (4, 'workforce', 'coverage_schedule', 'coverage_schedule_pkey', 1, 'coverage_schedule_id'),
            (5, 'workforce', 'workload_record', 'workload_record_pkey', 1, 'workload_record_id')
    ),
    actual_primary_keys AS (
        SELECT
            namespaces.nspname AS schema_name,
            tables.relname AS table_name,
            constraints.conname AS constraint_name,
            constrained_columns.key_position::INTEGER AS key_position,
            attributes.attname AS column_name
        FROM pg_catalog.pg_constraint AS constraints
        INNER JOIN pg_catalog.pg_class AS tables
            ON tables.oid = constraints.conrelid
        INNER JOIN pg_catalog.pg_namespace AS namespaces
            ON namespaces.oid = tables.relnamespace
        CROSS JOIN LATERAL unnest(constraints.conkey)
            WITH ORDINALITY AS constrained_columns(attribute_number, key_position)
        INNER JOIN pg_catalog.pg_attribute AS attributes
            ON attributes.attrelid = tables.oid
            AND attributes.attnum = constrained_columns.attribute_number
        WHERE constraints.contype = 'p'
            AND (namespaces.nspname, tables.relname) IN (
                VALUES
                    ('inventory', 'inventory_item'),
                    ('ticketing', 'ticket'),
                    ('workforce', 'assignment'),
                    ('workforce', 'coverage_schedule'),
                    ('workforce', 'workload_record')
            )
    ),
    primary_key_mismatches AS (
        SELECT
            COALESCE(expected_primary_keys.table_order, 99) AS table_order,
            COALESCE(expected_primary_keys.schema_name, actual_primary_keys.schema_name) AS schema_name,
            COALESCE(expected_primary_keys.table_name, actual_primary_keys.table_name) AS table_name,
            expected_primary_keys.constraint_name AS expected_constraint_name,
            actual_primary_keys.constraint_name AS actual_constraint_name,
            COALESCE(expected_primary_keys.key_position, actual_primary_keys.key_position) AS key_position,
            expected_primary_keys.column_name AS expected_column_name,
            actual_primary_keys.column_name AS actual_column_name
        FROM expected_primary_keys
        FULL OUTER JOIN actual_primary_keys
            ON actual_primary_keys.schema_name = expected_primary_keys.schema_name
            AND actual_primary_keys.table_name = expected_primary_keys.table_name
            AND actual_primary_keys.constraint_name = expected_primary_keys.constraint_name
            AND actual_primary_keys.key_position = expected_primary_keys.key_position
            AND actual_primary_keys.column_name = expected_primary_keys.column_name
        WHERE expected_primary_keys.column_name IS NULL
            OR actual_primary_keys.column_name IS NULL
    )
    SELECT string_agg(
        format(
            '%I.%I key position %s: expected constraint=%s column=%s, found constraint=%s column=%s',
            schema_name,
            table_name,
            key_position,
            COALESCE(expected_constraint_name, 'none'),
            COALESCE(expected_column_name, 'none'),
            COALESCE(actual_constraint_name, 'none'),
            COALESCE(actual_column_name, 'none')
        ),
        '; ' ORDER BY table_order, key_position
    )
    INTO validation_errors
    FROM primary_key_mismatches;

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Tier 1 primary-key validation failed: %',
            validation_errors;
    END IF;

    WITH expected_not_null (table_order, schema_name, table_name, column_name) AS (
        VALUES
            (1, 'inventory', 'inventory_item', 'item_id'),
            (1, 'inventory', 'inventory_item', 'item_category'),
            (1, 'inventory', 'inventory_item', 'criticality_level'),
            (1, 'inventory', 'inventory_item', 'unit_of_measure'),
            (1, 'inventory', 'inventory_item', 'active_flag'),
            (1, 'inventory', 'inventory_item', 'item_name'),
            (2, 'ticketing', 'ticket', 'ticket_id'),
            (2, 'ticketing', 'ticket', 'category'),
            (2, 'ticketing', 'ticket', 'priority'),
            (2, 'ticketing', 'ticket', 'status'),
            (2, 'ticketing', 'ticket', 'escalation_flag'),
            (2, 'ticketing', 'ticket', 'reopened_flag'),
            (2, 'ticketing', 'ticket', 'pending_flag'),
            (2, 'ticketing', 'ticket', 'sla_target_hours'),
            (2, 'ticketing', 'ticket', 'assigned_department'),
            (2, 'ticketing', 'ticket', 'created_at'),
            (3, 'workforce', 'assignment', 'assignment_id'),
            (3, 'workforce', 'assignment', 'employee_id'),
            (3, 'workforce', 'assignment', 'assignment_category'),
            (3, 'workforce', 'assignment', 'assignment_status'),
            (3, 'workforce', 'assignment', 'start_date'),
            (3, 'workforce', 'assignment', 'assignment_name'),
            (3, 'workforce', 'assignment', 'priority_level'),
            (3, 'workforce', 'assignment', 'cross_functional_flag'),
            (4, 'workforce', 'coverage_schedule', 'coverage_schedule_id'),
            (4, 'workforce', 'coverage_schedule', 'employee_id'),
            (4, 'workforce', 'coverage_schedule', 'schedule_date'),
            (4, 'workforce', 'coverage_schedule', 'shift_type'),
            (4, 'workforce', 'coverage_schedule', 'coverage_status'),
            (5, 'workforce', 'workload_record', 'workload_record_id'),
            (5, 'workforce', 'workload_record', 'employee_id'),
            (5, 'workforce', 'workload_record', 'reporting_period'),
            (5, 'workforce', 'workload_record', 'workload_status'),
            (5, 'workforce', 'workload_record', 'assigned_tasks'),
            (5, 'workforce', 'workload_record', 'completed_tasks'),
            (5, 'workforce', 'workload_record', 'open_tasks')
    ),
    actual_not_null AS (
        SELECT
            namespaces.nspname AS schema_name,
            tables.relname AS table_name,
            attributes.attname AS column_name
        FROM pg_catalog.pg_constraint AS constraints
        INNER JOIN pg_catalog.pg_class AS tables
            ON tables.oid = constraints.conrelid
        INNER JOIN pg_catalog.pg_namespace AS namespaces
            ON namespaces.oid = tables.relnamespace
        CROSS JOIN LATERAL unnest(constraints.conkey) AS constrained_columns(attribute_number)
        INNER JOIN pg_catalog.pg_attribute AS attributes
            ON attributes.attrelid = tables.oid
            AND attributes.attnum = constrained_columns.attribute_number
        WHERE constraints.contype = 'n'
            AND (namespaces.nspname, tables.relname) IN (
                VALUES
                    ('inventory', 'inventory_item'),
                    ('ticketing', 'ticket'),
                    ('workforce', 'assignment'),
                    ('workforce', 'coverage_schedule'),
                    ('workforce', 'workload_record')
            )
    ),
    not_null_mismatches AS (
        SELECT
            COALESCE(expected_not_null.table_order, 99) AS table_order,
            COALESCE(expected_not_null.schema_name, actual_not_null.schema_name) AS schema_name,
            COALESCE(expected_not_null.table_name, actual_not_null.table_name) AS table_name,
            COALESCE(expected_not_null.column_name, actual_not_null.column_name) AS column_name,
            expected_not_null.column_name IS NOT NULL AS expected_constraint,
            actual_not_null.column_name IS NOT NULL AS actual_constraint
        FROM expected_not_null
        FULL OUTER JOIN actual_not_null
            ON actual_not_null.schema_name = expected_not_null.schema_name
            AND actual_not_null.table_name = expected_not_null.table_name
            AND actual_not_null.column_name = expected_not_null.column_name
        WHERE expected_not_null.column_name IS NULL
            OR actual_not_null.column_name IS NULL
    )
    SELECT string_agg(
        format(
            '%I.%I.%I: expected NOT NULL constraint=%s, found=%s',
            schema_name,
            table_name,
            column_name,
            expected_constraint,
            actual_constraint
        ),
        '; ' ORDER BY table_order, column_name
    )
    INTO validation_errors
    FROM not_null_mismatches;

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Tier 1 PostgreSQL 18 NOT NULL catalog validation failed: %',
            validation_errors;
    END IF;

    WITH expected_foreign_keys (
        table_order,
        schema_name,
        table_name,
        constraint_name,
        column_name,
        referenced_schema_name,
        referenced_table_name,
        referenced_column_name,
        update_action,
        delete_action,
        match_type,
        is_deferrable,
        is_deferred,
        is_validated
    ) AS (
        VALUES
            (1, 'inventory', 'inventory_item', 'inventory_item_preferred_vendor_id_fkey', 'preferred_vendor_id', 'vendor', 'vendor', 'vendor_id', 'a', 'r', 's', FALSE, FALSE, TRUE),
            (3, 'workforce', 'assignment', 'assignment_employee_id_fkey', 'employee_id', 'workforce', 'employee', 'employee_id', 'a', 'r', 's', FALSE, FALSE, TRUE),
            (4, 'workforce', 'coverage_schedule', 'coverage_schedule_employee_id_fkey', 'employee_id', 'workforce', 'employee', 'employee_id', 'a', 'r', 's', FALSE, FALSE, TRUE),
            (5, 'workforce', 'workload_record', 'workload_record_employee_id_fkey', 'employee_id', 'workforce', 'employee', 'employee_id', 'a', 'r', 's', FALSE, FALSE, TRUE)
    ),
    actual_foreign_keys AS (
        SELECT
            source_namespaces.nspname AS schema_name,
            source_tables.relname AS table_name,
            constraints.conname AS constraint_name,
            source_attributes.attname AS column_name,
            target_namespaces.nspname AS referenced_schema_name,
            target_tables.relname AS referenced_table_name,
            target_attributes.attname AS referenced_column_name,
            cardinality(constraints.conkey) AS key_column_count,
            constraints.confupdtype::TEXT AS update_action,
            constraints.confdeltype::TEXT AS delete_action,
            constraints.confmatchtype::TEXT AS match_type,
            constraints.condeferrable AS is_deferrable,
            constraints.condeferred AS is_deferred,
            constraints.convalidated AS is_validated
        FROM pg_catalog.pg_constraint AS constraints
        INNER JOIN pg_catalog.pg_class AS source_tables
            ON source_tables.oid = constraints.conrelid
        INNER JOIN pg_catalog.pg_namespace AS source_namespaces
            ON source_namespaces.oid = source_tables.relnamespace
        INNER JOIN pg_catalog.pg_attribute AS source_attributes
            ON source_attributes.attrelid = source_tables.oid
            AND source_attributes.attnum = constraints.conkey[1]
        INNER JOIN pg_catalog.pg_class AS target_tables
            ON target_tables.oid = constraints.confrelid
        INNER JOIN pg_catalog.pg_namespace AS target_namespaces
            ON target_namespaces.oid = target_tables.relnamespace
        INNER JOIN pg_catalog.pg_attribute AS target_attributes
            ON target_attributes.attrelid = target_tables.oid
            AND target_attributes.attnum = constraints.confkey[1]
        WHERE constraints.contype = 'f'
            AND (source_namespaces.nspname, source_tables.relname) IN (
                VALUES
                    ('inventory', 'inventory_item'),
                    ('ticketing', 'ticket'),
                    ('workforce', 'assignment'),
                    ('workforce', 'coverage_schedule'),
                    ('workforce', 'workload_record')
            )
    ),
    foreign_key_mismatches AS (
        SELECT
            COALESCE(expected_foreign_keys.table_order, 99) AS table_order,
            COALESCE(expected_foreign_keys.schema_name, actual_foreign_keys.schema_name) AS schema_name,
            COALESCE(expected_foreign_keys.table_name, actual_foreign_keys.table_name) AS table_name,
            COALESCE(expected_foreign_keys.constraint_name, actual_foreign_keys.constraint_name) AS constraint_name,
            expected_foreign_keys.column_name AS expected_column_name,
            actual_foreign_keys.column_name AS actual_column_name,
            expected_foreign_keys.referenced_schema_name AS expected_referenced_schema_name,
            actual_foreign_keys.referenced_schema_name AS actual_referenced_schema_name,
            expected_foreign_keys.referenced_table_name AS expected_referenced_table_name,
            actual_foreign_keys.referenced_table_name AS actual_referenced_table_name,
            expected_foreign_keys.referenced_column_name AS expected_referenced_column_name,
            actual_foreign_keys.referenced_column_name AS actual_referenced_column_name,
            actual_foreign_keys.key_column_count,
            expected_foreign_keys.update_action AS expected_update_action,
            actual_foreign_keys.update_action AS actual_update_action,
            expected_foreign_keys.delete_action AS expected_delete_action,
            actual_foreign_keys.delete_action AS actual_delete_action,
            expected_foreign_keys.match_type AS expected_match_type,
            actual_foreign_keys.match_type AS actual_match_type,
            expected_foreign_keys.is_deferrable AS expected_is_deferrable,
            actual_foreign_keys.is_deferrable AS actual_is_deferrable,
            expected_foreign_keys.is_deferred AS expected_is_deferred,
            actual_foreign_keys.is_deferred AS actual_is_deferred,
            expected_foreign_keys.is_validated AS expected_is_validated,
            actual_foreign_keys.is_validated AS actual_is_validated
        FROM expected_foreign_keys
        FULL OUTER JOIN actual_foreign_keys
            ON actual_foreign_keys.schema_name = expected_foreign_keys.schema_name
            AND actual_foreign_keys.table_name = expected_foreign_keys.table_name
            AND actual_foreign_keys.constraint_name = expected_foreign_keys.constraint_name
        WHERE expected_foreign_keys.constraint_name IS NULL
            OR actual_foreign_keys.constraint_name IS NULL
            OR actual_foreign_keys.key_column_count IS DISTINCT FROM 1
            OR actual_foreign_keys.column_name IS DISTINCT FROM expected_foreign_keys.column_name
            OR actual_foreign_keys.referenced_schema_name IS DISTINCT FROM expected_foreign_keys.referenced_schema_name
            OR actual_foreign_keys.referenced_table_name IS DISTINCT FROM expected_foreign_keys.referenced_table_name
            OR actual_foreign_keys.referenced_column_name IS DISTINCT FROM expected_foreign_keys.referenced_column_name
            OR actual_foreign_keys.update_action IS DISTINCT FROM expected_foreign_keys.update_action
            OR actual_foreign_keys.delete_action IS DISTINCT FROM expected_foreign_keys.delete_action
            OR actual_foreign_keys.match_type IS DISTINCT FROM expected_foreign_keys.match_type
            OR actual_foreign_keys.is_deferrable IS DISTINCT FROM expected_foreign_keys.is_deferrable
            OR actual_foreign_keys.is_deferred IS DISTINCT FROM expected_foreign_keys.is_deferred
            OR actual_foreign_keys.is_validated IS DISTINCT FROM expected_foreign_keys.is_validated
    )
    SELECT string_agg(
        format(
            '%I.%I constraint %I: expected %I -> %I.%I.%I actions(update=%s delete=%s match=%s) deferrable=%s deferred=%s validated=%s; found %s -> %s.%s.%s key_columns=%s actions(update=%s delete=%s match=%s) deferrable=%s deferred=%s validated=%s',
            schema_name,
            table_name,
            constraint_name,
            COALESCE(expected_column_name, 'none'),
            COALESCE(expected_referenced_schema_name, 'none'),
            COALESCE(expected_referenced_table_name, 'none'),
            COALESCE(expected_referenced_column_name, 'none'),
            COALESCE(expected_update_action, 'none'),
            COALESCE(expected_delete_action, 'none'),
            COALESCE(expected_match_type, 'none'),
            COALESCE(expected_is_deferrable::TEXT, 'none'),
            COALESCE(expected_is_deferred::TEXT, 'none'),
            COALESCE(expected_is_validated::TEXT, 'none'),
            COALESCE(actual_column_name, 'none'),
            COALESCE(actual_referenced_schema_name, 'none'),
            COALESCE(actual_referenced_table_name, 'none'),
            COALESCE(actual_referenced_column_name, 'none'),
            COALESCE(key_column_count::TEXT, 'none'),
            COALESCE(actual_update_action, 'none'),
            COALESCE(actual_delete_action, 'none'),
            COALESCE(actual_match_type, 'none'),
            COALESCE(actual_is_deferrable::TEXT, 'none'),
            COALESCE(actual_is_deferred::TEXT, 'none'),
            COALESCE(actual_is_validated::TEXT, 'none')
        ),
        '; ' ORDER BY table_order, constraint_name
    )
    INTO validation_errors
    FROM foreign_key_mismatches;

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Tier 1 foreign-key validation failed: %',
            validation_errors;
    END IF;

    SELECT string_agg(
        format('%I on %I', constraints.conname, attributes.attname),
        '; ' ORDER BY constraints.conname, attributes.attname
    )
    INTO validation_errors
    FROM pg_catalog.pg_constraint AS constraints
    INNER JOIN pg_catalog.pg_class AS tables
        ON tables.oid = constraints.conrelid
    INNER JOIN pg_catalog.pg_namespace AS namespaces
        ON namespaces.oid = tables.relnamespace
    CROSS JOIN LATERAL unnest(constraints.conkey) AS constrained_columns(attribute_number)
    INNER JOIN pg_catalog.pg_attribute AS attributes
        ON attributes.attrelid = tables.oid
        AND attributes.attnum = constrained_columns.attribute_number
    WHERE constraints.contype = 'f'
        AND namespaces.nspname = 'ticketing'
        AND tables.relname = 'ticket'
        AND (
            constraints.conname IN ('ticket_location_id_fkey', 'ticket_employee_id_fkey')
            OR attributes.attname IN ('location_id', 'employee_id')
        );

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Tier 1 deferred Ticket foreign-key validation failed. These constraints must remain absent: %',
            validation_errors;
    END IF;

    WITH expected_unique_constraints (
        table_order,
        schema_name,
        table_name,
        constraint_name,
        key_position,
        column_name
    ) AS (
        VALUES
            (5, 'workforce', 'workload_record', 'workload_record_employee_id_reporting_period_key', 1, 'employee_id'),
            (5, 'workforce', 'workload_record', 'workload_record_employee_id_reporting_period_key', 2, 'reporting_period')
    ),
    actual_unique_constraints AS (
        SELECT
            namespaces.nspname AS schema_name,
            tables.relname AS table_name,
            constraints.conname AS constraint_name,
            constrained_columns.key_position::INTEGER AS key_position,
            attributes.attname AS column_name
        FROM pg_catalog.pg_constraint AS constraints
        INNER JOIN pg_catalog.pg_class AS tables
            ON tables.oid = constraints.conrelid
        INNER JOIN pg_catalog.pg_namespace AS namespaces
            ON namespaces.oid = tables.relnamespace
        CROSS JOIN LATERAL unnest(constraints.conkey)
            WITH ORDINALITY AS constrained_columns(attribute_number, key_position)
        INNER JOIN pg_catalog.pg_attribute AS attributes
            ON attributes.attrelid = tables.oid
            AND attributes.attnum = constrained_columns.attribute_number
        WHERE constraints.contype = 'u'
            AND (namespaces.nspname, tables.relname) IN (
                VALUES
                    ('inventory', 'inventory_item'),
                    ('ticketing', 'ticket'),
                    ('workforce', 'assignment'),
                    ('workforce', 'coverage_schedule'),
                    ('workforce', 'workload_record')
            )
    ),
    unique_constraint_mismatches AS (
        SELECT
            COALESCE(expected_unique_constraints.table_order, 99) AS table_order,
            COALESCE(expected_unique_constraints.schema_name, actual_unique_constraints.schema_name) AS schema_name,
            COALESCE(expected_unique_constraints.table_name, actual_unique_constraints.table_name) AS table_name,
            COALESCE(expected_unique_constraints.constraint_name, actual_unique_constraints.constraint_name) AS constraint_name,
            COALESCE(expected_unique_constraints.key_position, actual_unique_constraints.key_position) AS key_position,
            expected_unique_constraints.column_name AS expected_column_name,
            actual_unique_constraints.column_name AS actual_column_name
        FROM expected_unique_constraints
        FULL OUTER JOIN actual_unique_constraints
            ON actual_unique_constraints.schema_name = expected_unique_constraints.schema_name
            AND actual_unique_constraints.table_name = expected_unique_constraints.table_name
            AND actual_unique_constraints.constraint_name = expected_unique_constraints.constraint_name
            AND actual_unique_constraints.key_position = expected_unique_constraints.key_position
            AND actual_unique_constraints.column_name = expected_unique_constraints.column_name
        WHERE expected_unique_constraints.column_name IS NULL
            OR actual_unique_constraints.column_name IS NULL
    )
    SELECT string_agg(
        format(
            '%I.%I constraint %I position %s: expected column=%s, found=%s',
            schema_name,
            table_name,
            constraint_name,
            key_position,
            COALESCE(expected_column_name, 'none'),
            COALESCE(actual_column_name, 'none')
        ),
        '; ' ORDER BY table_order, constraint_name, key_position
    )
    INTO validation_errors
    FROM unique_constraint_mismatches;

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Tier 1 unique-constraint validation failed: %',
            validation_errors;
    END IF;

    SELECT string_agg(
        format(
            '%I.%I constraint %I (%s)',
            namespaces.nspname,
            tables.relname,
            constraints.conname,
            CASE constraints.contype
                WHEN 'c' THEN 'CHECK'
                WHEN 'x' THEN 'EXCLUSION'
                WHEN 't' THEN 'CONSTRAINT TRIGGER'
                ELSE constraints.contype::TEXT
            END
        ),
        '; ' ORDER BY namespaces.nspname, tables.relname, constraints.conname
    )
    INTO validation_errors
    FROM pg_catalog.pg_constraint AS constraints
    INNER JOIN pg_catalog.pg_class AS tables
        ON tables.oid = constraints.conrelid
    INNER JOIN pg_catalog.pg_namespace AS namespaces
        ON namespaces.oid = tables.relnamespace
    WHERE constraints.contype NOT IN ('n', 'p', 'f', 'u')
        AND (namespaces.nspname, tables.relname) IN (
            VALUES
                ('inventory', 'inventory_item'),
                ('ticketing', 'ticket'),
                ('workforce', 'assignment'),
                ('workforce', 'coverage_schedule'),
                ('workforce', 'workload_record')
        );

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Tier 1 prohibited-constraint validation failed: %',
            validation_errors;
    END IF;

    WITH expected_index_counts (table_order, schema_name, table_name, expected_index_count) AS (
        VALUES
            (1, 'inventory', 'inventory_item', 1),
            (2, 'ticketing', 'ticket', 1),
            (3, 'workforce', 'assignment', 1),
            (4, 'workforce', 'coverage_schedule', 1),
            (5, 'workforce', 'workload_record', 2)
    ),
    actual_index_counts AS (
        SELECT
            namespaces.nspname AS schema_name,
            tables.relname AS table_name,
            count(indexes.indexrelid)::INTEGER AS index_count,
            count(indexes.indexrelid) FILTER (
                WHERE constraints.contype IN ('p', 'u')
                    AND constraints.conindid = indexes.indexrelid
            )::INTEGER AS approved_constraint_index_count,
            count(indexes.indexrelid) FILTER (
                WHERE constraints.oid IS NULL
            )::INTEGER AS manual_index_count,
            count(indexes.indexrelid) FILTER (
                WHERE NOT indexes.indisvalid
                    OR NOT indexes.indisready
            )::INTEGER AS invalid_or_unready_index_count
        FROM pg_catalog.pg_class AS tables
        INNER JOIN pg_catalog.pg_namespace AS namespaces
            ON namespaces.oid = tables.relnamespace
        LEFT JOIN pg_catalog.pg_index AS indexes
            ON indexes.indrelid = tables.oid
        LEFT JOIN pg_catalog.pg_constraint AS constraints
            ON constraints.conindid = indexes.indexrelid
        WHERE (namespaces.nspname, tables.relname) IN (
            VALUES
                ('inventory', 'inventory_item'),
                ('ticketing', 'ticket'),
                ('workforce', 'assignment'),
                ('workforce', 'coverage_schedule'),
                ('workforce', 'workload_record')
        )
        GROUP BY namespaces.nspname, tables.relname
    ),
    index_mismatches AS (
        SELECT
            expected_index_counts.table_order,
            expected_index_counts.schema_name,
            expected_index_counts.table_name,
            expected_index_counts.expected_index_count,
            actual_index_counts.index_count,
            actual_index_counts.approved_constraint_index_count,
            actual_index_counts.manual_index_count,
            actual_index_counts.invalid_or_unready_index_count
        FROM expected_index_counts
        LEFT JOIN actual_index_counts
            ON actual_index_counts.schema_name = expected_index_counts.schema_name
            AND actual_index_counts.table_name = expected_index_counts.table_name
        WHERE actual_index_counts.index_count IS DISTINCT FROM expected_index_counts.expected_index_count
            OR actual_index_counts.approved_constraint_index_count IS DISTINCT FROM expected_index_counts.expected_index_count
            OR actual_index_counts.manual_index_count IS DISTINCT FROM 0
            OR actual_index_counts.invalid_or_unready_index_count IS DISTINCT FROM 0
    )
    SELECT string_agg(
        format(
            '%I.%I: expected %s approved constraint-backed indexes and no manual indexes; found total=%s approved_constraint=%s manual=%s invalid_or_unready=%s',
            schema_name,
            table_name,
            expected_index_count,
            COALESCE(index_count::TEXT, 'missing table'),
            COALESCE(approved_constraint_index_count::TEXT, 'missing table'),
            COALESCE(manual_index_count::TEXT, 'missing table'),
            COALESCE(invalid_or_unready_index_count::TEXT, 'missing table')
        ),
        '; ' ORDER BY table_order
    )
    INTO validation_errors
    FROM index_mismatches;

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Tier 1 supporting-index validation failed: %',
            validation_errors;
    END IF;

    FOR target_table IN
        SELECT *
        FROM (
            VALUES
                (1, 'inventory', 'inventory_item'),
                (2, 'ticketing', 'ticket'),
                (3, 'workforce', 'assignment'),
                (4, 'workforce', 'coverage_schedule'),
                (5, 'workforce', 'workload_record')
        ) AS target_tables(table_order, schema_name, table_name)
        ORDER BY target_tables.table_order
    LOOP
        EXECUTE format(
            'SELECT EXISTS (SELECT 1 FROM %I.%I)',
            target_table.schema_name,
            target_table.table_name
        )
        INTO table_has_rows;

        IF table_has_rows THEN
            nonempty_tables := concat_ws(
                ', ',
                nonempty_tables,
                format('%I.%I', target_table.schema_name, target_table.table_name)
            );
        END IF;
    END LOOP;

    IF nonempty_tables IS NOT NULL THEN
        RAISE EXCEPTION
            'Tier 1 data-boundary validation failed. Tier 1 tables must be empty before migration; rows found in: %',
            nonempty_tables;
    END IF;
END
$validation$;

SELECT
    5 AS approved_tier_1_table_count,
    (
        SELECT count(*)
        FROM information_schema.columns AS columns
        WHERE (columns.table_schema, columns.table_name) IN (
            VALUES
                ('inventory', 'inventory_item'),
                ('ticketing', 'ticket'),
                ('workforce', 'assignment'),
                ('workforce', 'coverage_schedule'),
                ('workforce', 'workload_record')
        )
    ) AS approved_tier_1_column_count,
    (
        SELECT count(*)
        FROM information_schema.columns AS columns
        WHERE (columns.table_schema, columns.table_name) IN (
            VALUES
                ('inventory', 'inventory_item'),
                ('ticketing', 'ticket'),
                ('workforce', 'assignment'),
                ('workforce', 'coverage_schedule'),
                ('workforce', 'workload_record')
        )
            AND columns.is_nullable = 'NO'
    ) AS approved_not_null_column_count,
    (
        SELECT count(*)
        FROM pg_catalog.pg_constraint AS constraints
        INNER JOIN pg_catalog.pg_class AS tables
            ON tables.oid = constraints.conrelid
        INNER JOIN pg_catalog.pg_namespace AS namespaces
            ON namespaces.oid = tables.relnamespace
        WHERE constraints.contype = 'p'
            AND (namespaces.nspname, tables.relname) IN (
                VALUES
                    ('inventory', 'inventory_item'),
                    ('ticketing', 'ticket'),
                    ('workforce', 'assignment'),
                    ('workforce', 'coverage_schedule'),
                    ('workforce', 'workload_record')
            )
    ) AS approved_primary_key_count,
    (
        SELECT count(*)
        FROM pg_catalog.pg_constraint AS constraints
        INNER JOIN pg_catalog.pg_class AS tables
            ON tables.oid = constraints.conrelid
        INNER JOIN pg_catalog.pg_namespace AS namespaces
            ON namespaces.oid = tables.relnamespace
        WHERE constraints.contype = 'f'
            AND (namespaces.nspname, tables.relname) IN (
                VALUES
                    ('inventory', 'inventory_item'),
                    ('ticketing', 'ticket'),
                    ('workforce', 'assignment'),
                    ('workforce', 'coverage_schedule'),
                    ('workforce', 'workload_record')
            )
    ) AS approved_foreign_key_count,
    (
        SELECT count(*)
        FROM pg_catalog.pg_constraint AS constraints
        INNER JOIN pg_catalog.pg_class AS tables
            ON tables.oid = constraints.conrelid
        INNER JOIN pg_catalog.pg_namespace AS namespaces
            ON namespaces.oid = tables.relnamespace
        WHERE constraints.contype = 'u'
            AND (namespaces.nspname, tables.relname) IN (
                VALUES
                    ('inventory', 'inventory_item'),
                    ('ticketing', 'ticket'),
                    ('workforce', 'assignment'),
                    ('workforce', 'coverage_schedule'),
                    ('workforce', 'workload_record')
            )
    ) AS approved_business_key_count,
    (
        SELECT count(*)
        FROM pg_catalog.pg_index AS indexes
        INNER JOIN pg_catalog.pg_class AS tables
            ON tables.oid = indexes.indrelid
        INNER JOIN pg_catalog.pg_namespace AS namespaces
            ON namespaces.oid = tables.relnamespace
        WHERE (namespaces.nspname, tables.relname) IN (
            VALUES
                ('inventory', 'inventory_item'),
                ('ticketing', 'ticket'),
                ('workforce', 'assignment'),
                ('workforce', 'coverage_schedule'),
                ('workforce', 'workload_record')
        )
    ) AS approved_constraint_index_count,
    (
        (SELECT count(*) FROM inventory.inventory_item)
        + (SELECT count(*) FROM ticketing.ticket)
        + (SELECT count(*) FROM workforce.assignment)
        + (SELECT count(*) FROM workforce.coverage_schedule)
        + (SELECT count(*) FROM workforce.workload_record)
    ) AS tier_1_row_count,
    'PASS' AS validation_result;
