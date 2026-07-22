-- Northstar Health Operations
-- Purpose: Confirm that the three approved Tier 0 tables match the locked schema.
-- Authority: Enterprise Relational Schema and issue #8.
-- Boundary: Read-only validation of core.location, workforce.employee, and
--           vendor.vendor; future tables in the same schemas are out of scope.
-- PostgreSQL 18 metadata note: pg_constraint.contype = 'n' represents NOT NULL
-- constraints separately from ordinary CHECK constraints, which use contype = 'c'.
-- This validation asserts the exact approved 'n' rows and rejects every 'c' row
-- on the three Tier 0 tables rather than relying only on is_nullable metadata.

DO $validation$
DECLARE
    validation_errors TEXT;
    actual_column_count INTEGER;
BEGIN
    WITH expected_tables (table_order, schema_name, table_name) AS (
        VALUES
            (1, 'core', 'location'),
            (2, 'workforce', 'employee'),
            (3, 'vendor', 'vendor')
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
            'Tier 0 table validation failed: %',
            validation_errors;
    END IF;

    SELECT count(*)
    INTO actual_column_count
    FROM information_schema.columns AS actual_columns
    WHERE (actual_columns.table_schema, actual_columns.table_name) IN (
        VALUES
            ('core', 'location'),
            ('workforce', 'employee'),
            ('vendor', 'vendor')
    );

    IF actual_column_count <> 23 THEN
        RAISE EXCEPTION
            'Tier 0 column-count validation failed. Expected 23 columns across the three governed tables; found %.',
            actual_column_count;
    END IF;

    WITH expected_columns (
        table_order,
        schema_name,
        table_name,
        ordinal_position,
        column_name,
        data_type,
        is_nullable
    ) AS (
        VALUES
            (1, 'core', 'location', 1, 'location_id', 'text', 'NO'),
            (2, 'workforce', 'employee', 1, 'employee_id', 'text', 'NO'),
            (2, 'workforce', 'employee', 2, 'employee_name', 'text', 'NO'),
            (2, 'workforce', 'employee', 3, 'department', 'text', 'NO'),
            (2, 'workforce', 'employee', 4, 'team', 'text', 'NO'),
            (2, 'workforce', 'employee', 5, 'role', 'text', 'NO'),
            (2, 'workforce', 'employee', 6, 'employment_status', 'text', 'NO'),
            (2, 'workforce', 'employee', 7, 'active_flag', 'boolean', 'NO'),
            (2, 'workforce', 'employee', 8, 'primary_shift', 'text', 'YES'),
            (2, 'workforce', 'employee', 9, 'standard_weekly_hours', 'integer', 'YES'),
            (2, 'workforce', 'employee', 10, 'skill_area', 'text', 'YES'),
            (2, 'workforce', 'employee', 11, 'coverage_priority', 'text', 'YES'),
            (3, 'vendor', 'vendor', 1, 'vendor_id', 'text', 'NO'),
            (3, 'vendor', 'vendor', 2, 'vendor_type', 'text', 'NO'),
            (3, 'vendor', 'vendor', 3, 'primary_service_category', 'text', 'NO'),
            (3, 'vendor', 'vendor', 4, 'risk_tier', 'text', 'NO'),
            (3, 'vendor', 'vendor', 5, 'active_vendor_flag', 'boolean', 'NO'),
            (3, 'vendor', 'vendor', 6, 'vendor_name', 'text', 'NO'),
            (3, 'vendor', 'vendor', 7, 'support_level', 'text', 'YES'),
            (3, 'vendor', 'vendor', 8, 'preferred_vendor_flag', 'boolean', 'YES'),
            (3, 'vendor', 'vendor', 9, 'emergency_fulfillment_flag', 'boolean', 'YES'),
            (3, 'vendor', 'vendor', 10, 'primary_contact_team', 'text', 'YES'),
            (3, 'vendor', 'vendor', 11, 'notes', 'text', 'YES')
    ),
    actual_columns AS (
        SELECT
            columns.table_schema AS schema_name,
            columns.table_name,
            columns.ordinal_position,
            columns.column_name,
            columns.data_type,
            columns.is_nullable,
            columns.column_default,
            columns.is_identity,
            columns.is_generated
        FROM information_schema.columns AS columns
        WHERE (columns.table_schema, columns.table_name) IN (
            VALUES
                ('core', 'location'),
                ('workforce', 'employee'),
                ('vendor', 'vendor')
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
                '%I.%I.%I: expected position=%s type=%s nullable=%s default=NULL identity=NO generated=NEVER; found position=%s type=%s nullable=%s default=%s identity=%s generated=%s',
                schema_name,
                table_name,
                expected_column_name,
                expected_ordinal_position,
                expected_data_type,
                expected_is_nullable,
                actual_ordinal_position,
                actual_data_type,
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
            'Tier 0 column-definition validation failed: %',
            validation_errors;
    END IF;

    WITH expected_primary_keys (
        table_order,
        schema_name,
        table_name,
        key_position,
        column_name
    ) AS (
        VALUES
            (1, 'core', 'location', 1, 'location_id'),
            (2, 'workforce', 'employee', 1, 'employee_id'),
            (3, 'vendor', 'vendor', 1, 'vendor_id')
    ),
    actual_primary_keys AS (
        SELECT
            table_constraints.table_schema AS schema_name,
            table_constraints.table_name,
            key_columns.ordinal_position AS key_position,
            key_columns.column_name
        FROM information_schema.table_constraints AS table_constraints
        INNER JOIN information_schema.key_column_usage AS key_columns
            ON key_columns.constraint_catalog = table_constraints.constraint_catalog
            AND key_columns.constraint_schema = table_constraints.constraint_schema
            AND key_columns.constraint_name = table_constraints.constraint_name
            AND key_columns.table_schema = table_constraints.table_schema
            AND key_columns.table_name = table_constraints.table_name
        WHERE table_constraints.constraint_type = 'PRIMARY KEY'
            AND (table_constraints.table_schema, table_constraints.table_name) IN (
                VALUES
                    ('core', 'location'),
                    ('workforce', 'employee'),
                    ('vendor', 'vendor')
            )
    ),
    primary_key_mismatches AS (
        SELECT
            COALESCE(expected_primary_keys.table_order, 99) AS table_order,
            COALESCE(expected_primary_keys.schema_name, actual_primary_keys.schema_name) AS schema_name,
            COALESCE(expected_primary_keys.table_name, actual_primary_keys.table_name) AS table_name,
            COALESCE(expected_primary_keys.key_position, actual_primary_keys.key_position) AS key_position,
            expected_primary_keys.column_name AS expected_column_name,
            actual_primary_keys.column_name AS actual_column_name
        FROM expected_primary_keys
        FULL OUTER JOIN actual_primary_keys
            ON actual_primary_keys.schema_name = expected_primary_keys.schema_name
            AND actual_primary_keys.table_name = expected_primary_keys.table_name
            AND actual_primary_keys.key_position = expected_primary_keys.key_position
            AND actual_primary_keys.column_name = expected_primary_keys.column_name
        WHERE expected_primary_keys.column_name IS NULL
            OR actual_primary_keys.column_name IS NULL
    )
    SELECT string_agg(
        format(
            '%I.%I key position %s: expected %s, found %s',
            schema_name,
            table_name,
            key_position,
            COALESCE(expected_column_name, 'none'),
            COALESCE(actual_column_name, 'none')
        ),
        '; ' ORDER BY table_order, key_position
    )
    INTO validation_errors
    FROM primary_key_mismatches;

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Tier 0 primary-key validation failed: %',
            validation_errors;
    END IF;

    WITH expected_not_null (
        table_order,
        schema_name,
        table_name,
        column_name
    ) AS (
        VALUES
            (1, 'core', 'location', 'location_id'),
            (2, 'workforce', 'employee', 'employee_id'),
            (2, 'workforce', 'employee', 'employee_name'),
            (2, 'workforce', 'employee', 'department'),
            (2, 'workforce', 'employee', 'team'),
            (2, 'workforce', 'employee', 'role'),
            (2, 'workforce', 'employee', 'employment_status'),
            (2, 'workforce', 'employee', 'active_flag'),
            (3, 'vendor', 'vendor', 'vendor_id'),
            (3, 'vendor', 'vendor', 'vendor_type'),
            (3, 'vendor', 'vendor', 'primary_service_category'),
            (3, 'vendor', 'vendor', 'risk_tier'),
            (3, 'vendor', 'vendor', 'active_vendor_flag'),
            (3, 'vendor', 'vendor', 'vendor_name')
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
                    ('core', 'location'),
                    ('workforce', 'employee'),
                    ('vendor', 'vendor')
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
            'Tier 0 PostgreSQL 18 NOT NULL catalog validation failed: %',
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
                WHEN 'f' THEN 'FOREIGN KEY'
                WHEN 'u' THEN 'UNIQUE'
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
    WHERE constraints.contype NOT IN ('n', 'p')
        AND (namespaces.nspname, tables.relname) IN (
            VALUES
                ('core', 'location'),
                ('workforce', 'employee'),
                ('vendor', 'vendor')
        );

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Tier 0 prohibited-constraint validation failed: %',
            validation_errors;
    END IF;

    WITH target_tables AS (
        SELECT
            namespaces.nspname AS schema_name,
            tables.relname AS table_name,
            tables.oid AS table_oid
        FROM pg_catalog.pg_class AS tables
        INNER JOIN pg_catalog.pg_namespace AS namespaces
            ON namespaces.oid = tables.relnamespace
        WHERE (namespaces.nspname, tables.relname) IN (
            VALUES
                ('core', 'location'),
                ('workforce', 'employee'),
                ('vendor', 'vendor')
        )
    ),
    index_counts AS (
        SELECT
            target_tables.schema_name,
            target_tables.table_name,
            count(indexes.indexrelid) AS index_count,
            count(indexes.indexrelid) FILTER (
                WHERE indexes.indisprimary
                    AND primary_keys.conindid = indexes.indexrelid
            ) AS primary_key_index_count
        FROM target_tables
        LEFT JOIN pg_catalog.pg_index AS indexes
            ON indexes.indrelid = target_tables.table_oid
        LEFT JOIN pg_catalog.pg_constraint AS primary_keys
            ON primary_keys.conrelid = target_tables.table_oid
            AND primary_keys.contype = 'p'
        GROUP BY
            target_tables.schema_name,
            target_tables.table_name
    )
    SELECT string_agg(
        format(
            '%I.%I: expected exactly one automatic primary-key index; found indexes=%s matching_primary_indexes=%s',
            schema_name,
            table_name,
            index_count,
            primary_key_index_count
        ),
        '; ' ORDER BY schema_name, table_name
    )
    INTO validation_errors
    FROM index_counts
    WHERE index_count <> 1
        OR primary_key_index_count <> 1;

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Tier 0 supporting-index validation failed: %',
            validation_errors;
    END IF;
END
$validation$;

WITH expected_tables (table_order, schema_name, table_name) AS (
    VALUES
        (1, 'core', 'location'),
        (2, 'workforce', 'employee'),
        (3, 'vendor', 'vendor')
),
primary_key_columns AS (
    SELECT
        table_constraints.table_schema AS schema_name,
        table_constraints.table_name,
        key_columns.column_name
    FROM information_schema.table_constraints AS table_constraints
    INNER JOIN information_schema.key_column_usage AS key_columns
        ON key_columns.constraint_catalog = table_constraints.constraint_catalog
        AND key_columns.constraint_schema = table_constraints.constraint_schema
        AND key_columns.constraint_name = table_constraints.constraint_name
        AND key_columns.table_schema = table_constraints.table_schema
        AND key_columns.table_name = table_constraints.table_name
    WHERE table_constraints.constraint_type = 'PRIMARY KEY'
)
SELECT
    columns.table_schema,
    columns.table_name,
    columns.ordinal_position,
    columns.column_name,
    upper(columns.data_type) AS data_type,
    columns.is_nullable,
    CASE
        WHEN primary_key_columns.column_name IS NOT NULL THEN 'YES'
        ELSE 'NO'
    END AS primary_key,
    tables.tableowner AS table_owner
FROM expected_tables
INNER JOIN information_schema.columns AS columns
    ON columns.table_schema = expected_tables.schema_name
    AND columns.table_name = expected_tables.table_name
INNER JOIN pg_catalog.pg_tables AS tables
    ON tables.schemaname = columns.table_schema
    AND tables.tablename = columns.table_name
LEFT JOIN primary_key_columns
    ON primary_key_columns.schema_name = columns.table_schema
    AND primary_key_columns.table_name = columns.table_name
    AND primary_key_columns.column_name = columns.column_name
ORDER BY
    expected_tables.table_order,
    columns.ordinal_position;
