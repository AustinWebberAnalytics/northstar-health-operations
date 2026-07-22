-- Northstar Health Operations
-- Purpose: Confirm the exact PostgreSQL implementation-foundation runtime and
--          pre-migration user-defined object inventory approved through Tier 1.
-- Authority: Enterprise Database Platform Decision, Enterprise Relational Schema,
--            Tier 1 PostgreSQL Implementation Contract, and issue #29.
-- Boundary: Read-only foundation validation; no database state is modified.
-- System-object scoping: pg_catalog, information_schema, pg_toast, pg_temp_*,
--                        and pg_toast_temp_* are PostgreSQL-managed namespaces and
--                        are excluded from the user-defined object inventory.
-- Version validation: server_version_num is PostgreSQL's machine-readable
--                     version value and is not affected by platform or package
--                     suffixes in the human-readable server_version value.

DO $validation$
DECLARE
    validation_errors TEXT;
    target_table RECORD;
    table_has_rows BOOLEAN;
    nonempty_tables TEXT := NULL;
BEGIN
    IF current_setting('server_version_num')::INTEGER IS DISTINCT FROM 180004 THEN
        RAISE EXCEPTION
            'Implementation-foundation runtime validation failed. Expected PostgreSQL server_version_num 180004 (18.4); found % (%).',
            current_setting('server_version_num'),
            current_setting('server_version');
    END IF;

    IF current_database() IS DISTINCT FROM 'northstar' THEN
        RAISE EXCEPTION
            'Implementation-foundation database validation failed. Expected database northstar; found %.',
            current_database();
    END IF;

    IF current_user IS DISTINCT FROM 'northstar_local_admin' THEN
        RAISE EXCEPTION
            'Implementation-foundation user validation failed. Expected authenticated user northstar_local_admin; found %.',
            current_user;
    END IF;

    WITH expected_schemas (schema_order, schema_name) AS (
        VALUES
            (1, 'core'),
            (2, 'workforce'),
            (3, 'vendor'),
            (4, 'inventory'),
            (5, 'ticketing'),
            (6, 'relationships')
    ),
    schema_mismatches AS (
        SELECT
            expected_schemas.schema_order,
            expected_schemas.schema_name,
            pg_catalog.pg_get_userbyid(actual_schemas.nspowner) AS actual_owner
        FROM expected_schemas
        LEFT JOIN pg_catalog.pg_namespace AS actual_schemas
            ON actual_schemas.nspname = expected_schemas.schema_name
        WHERE actual_schemas.oid IS NULL
            OR pg_catalog.pg_get_userbyid(actual_schemas.nspowner)
                IS DISTINCT FROM 'northstar_local_admin'
    )
    SELECT string_agg(
        format(
            '%I: expected owner northstar_local_admin, found %s',
            schema_name,
            COALESCE(actual_owner, 'missing schema')
        ),
        '; ' ORDER BY schema_order
    )
    INTO validation_errors
    FROM schema_mismatches;

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Implementation-foundation schema ownership validation failed: %',
            validation_errors;
    END IF;

    SELECT string_agg(
        format('%I', namespaces.nspname),
        ', ' ORDER BY namespaces.nspname
    )
    INTO validation_errors
    FROM pg_catalog.pg_namespace AS namespaces
    WHERE namespaces.nspname NOT IN (
            'pg_catalog',
            'information_schema',
            'pg_toast',
            'public',
            'core',
            'workforce',
            'vendor',
            'inventory',
            'ticketing',
            'relationships'
        )
        AND namespaces.nspname NOT LIKE 'pg_temp_%'
        AND namespaces.nspname NOT LIKE 'pg_toast_temp_%';

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Implementation-foundation schema inventory validation failed. Unapproved user-defined schemas: %',
            validation_errors;
    END IF;

    SELECT string_agg(
        format('%I (%s)', relations.relname, relations.relkind),
        '; ' ORDER BY relations.relname, relations.relkind
    )
    INTO validation_errors
    FROM pg_catalog.pg_class AS relations
    INNER JOIN pg_catalog.pg_namespace AS namespaces
        ON namespaces.oid = relations.relnamespace
    WHERE namespaces.nspname = 'public';

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Implementation-foundation public-schema validation failed. The permitted public schema must remain empty; found: %',
            validation_errors;
    END IF;

    WITH expected_relations (
        relation_order,
        schema_name,
        relation_name,
        relation_kind
    ) AS (
        VALUES
            (1, 'core', 'location', 'r'::"char"),
            (2, 'workforce', 'employee', 'r'::"char"),
            (3, 'vendor', 'vendor', 'r'::"char"),
            (4, 'inventory', 'inventory_item', 'r'::"char"),
            (5, 'ticketing', 'ticket', 'r'::"char"),
            (6, 'workforce', 'assignment', 'r'::"char"),
            (7, 'workforce', 'coverage_schedule', 'r'::"char"),
            (8, 'workforce', 'workload_record', 'r'::"char")
    ),
    actual_relations AS (
        SELECT
            namespaces.nspname AS schema_name,
            relations.relname AS relation_name,
            relations.relkind AS relation_kind
        FROM pg_catalog.pg_class AS relations
        INNER JOIN pg_catalog.pg_namespace AS namespaces
            ON namespaces.oid = relations.relnamespace
        WHERE namespaces.nspname IN (
                'core',
                'workforce',
                'vendor',
                'inventory',
                'ticketing',
                'relationships'
            )
            AND relations.relkind IN ('r', 'p', 'S', 'v', 'm', 'f', 'c')
    ),
    relation_mismatches AS (
        SELECT
            COALESCE(expected_relations.relation_order, 99) AS relation_order,
            COALESCE(expected_relations.schema_name, actual_relations.schema_name) AS schema_name,
            COALESCE(expected_relations.relation_name, actual_relations.relation_name) AS relation_name,
            expected_relations.relation_kind AS expected_kind,
            actual_relations.relation_kind AS actual_kind
        FROM expected_relations
        FULL OUTER JOIN actual_relations
            ON actual_relations.schema_name = expected_relations.schema_name
            AND actual_relations.relation_name = expected_relations.relation_name
        WHERE expected_relations.relation_name IS NULL
            OR actual_relations.relation_name IS NULL
            OR actual_relations.relation_kind IS DISTINCT FROM expected_relations.relation_kind
    )
    SELECT string_agg(
        format(
            '%I.%I: expected kind=%s, found kind=%s',
            schema_name,
            relation_name,
            COALESCE(expected_kind::TEXT, 'none'),
            COALESCE(actual_kind::TEXT, 'missing')
        ),
        '; ' ORDER BY relation_order, schema_name, relation_name
    )
    INTO validation_errors
    FROM relation_mismatches;

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Implementation-foundation relation inventory validation failed: %',
            validation_errors;
    END IF;

    SELECT string_agg(
        format(
            '%I.%I (%s)',
            namespaces.nspname,
            routines.proname,
            CASE routines.prokind
                WHEN 'f' THEN 'function'
                WHEN 'p' THEN 'procedure'
                WHEN 'a' THEN 'aggregate'
                WHEN 'w' THEN 'window function'
                ELSE routines.prokind::TEXT
            END
        ),
        '; ' ORDER BY namespaces.nspname, routines.proname, routines.oid
    )
    INTO validation_errors
    FROM pg_catalog.pg_proc AS routines
    INNER JOIN pg_catalog.pg_namespace AS namespaces
        ON namespaces.oid = routines.pronamespace
    WHERE namespaces.nspname NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
        AND namespaces.nspname NOT LIKE 'pg_temp_%'
        AND namespaces.nspname NOT LIKE 'pg_toast_temp_%';

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Implementation-foundation routine inventory validation failed. Unapproved user-defined routines: %',
            validation_errors;
    END IF;

    SELECT string_agg(
        format('%I.%I trigger %I', namespaces.nspname, relations.relname, triggers.tgname),
        '; ' ORDER BY namespaces.nspname, relations.relname, triggers.tgname
    )
    INTO validation_errors
    FROM pg_catalog.pg_trigger AS triggers
    INNER JOIN pg_catalog.pg_class AS relations
        ON relations.oid = triggers.tgrelid
    INNER JOIN pg_catalog.pg_namespace AS namespaces
        ON namespaces.oid = relations.relnamespace
    WHERE NOT triggers.tgisinternal
        AND namespaces.nspname NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
        AND namespaces.nspname NOT LIKE 'pg_temp_%'
        AND namespaces.nspname NOT LIKE 'pg_toast_temp_%';

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Implementation-foundation trigger inventory validation failed. Unapproved user-defined triggers: %',
            validation_errors;
    END IF;

    SELECT string_agg(
        format('%I.%I policy %I', namespaces.nspname, relations.relname, policies.polname),
        '; ' ORDER BY namespaces.nspname, relations.relname, policies.polname
    )
    INTO validation_errors
    FROM pg_catalog.pg_policy AS policies
    INNER JOIN pg_catalog.pg_class AS relations
        ON relations.oid = policies.polrelid
    INNER JOIN pg_catalog.pg_namespace AS namespaces
        ON namespaces.oid = relations.relnamespace
    WHERE namespaces.nspname NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
        AND namespaces.nspname NOT LIKE 'pg_temp_%'
        AND namespaces.nspname NOT LIKE 'pg_toast_temp_%';

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Implementation-foundation policy inventory validation failed. Unapproved row-level security policies: %',
            validation_errors;
    END IF;

    SELECT string_agg(
        format('%I', event_triggers.evtname),
        ', ' ORDER BY event_triggers.evtname
    )
    INTO validation_errors
    FROM pg_catalog.pg_event_trigger AS event_triggers;

    IF validation_errors IS NOT NULL THEN
        RAISE EXCEPTION
            'Implementation-foundation event-trigger inventory validation failed. Unapproved event triggers: %',
            validation_errors;
    END IF;

    FOR target_table IN
        SELECT *
        FROM (
            VALUES
                (1, 'core', 'location'),
                (2, 'workforce', 'employee'),
                (3, 'vendor', 'vendor'),
                (4, 'inventory', 'inventory_item'),
                (5, 'ticketing', 'ticket'),
                (6, 'workforce', 'assignment'),
                (7, 'workforce', 'coverage_schedule'),
                (8, 'workforce', 'workload_record')
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
            'Implementation-foundation data-boundary validation failed. Tier 0 and Tier 1 tables must be empty before migration; rows found in: %',
            nonempty_tables;
    END IF;
END
$validation$;

SELECT
    format(
        '%s.%s',
        current_setting('server_version_num')::INTEGER / 10000,
        current_setting('server_version_num')::INTEGER % 10000
    ) AS server_version,
    current_database() AS database_name,
    current_user AS authenticated_user,
    (
        SELECT count(*)
        FROM pg_catalog.pg_namespace AS namespaces
        WHERE namespaces.nspname IN (
            'core',
            'workforce',
            'vendor',
            'inventory',
            'ticketing',
            'relationships'
        )
    ) AS approved_schema_count,
    (
        SELECT count(*)
        FROM pg_catalog.pg_class AS relations
        INNER JOIN pg_catalog.pg_namespace AS namespaces
            ON namespaces.oid = relations.relnamespace
        WHERE (namespaces.nspname, relations.relname) IN (
            VALUES
                ('core', 'location'),
                ('workforce', 'employee'),
                ('vendor', 'vendor'),
                ('inventory', 'inventory_item'),
                ('ticketing', 'ticket'),
                ('workforce', 'assignment'),
                ('workforce', 'coverage_schedule'),
                ('workforce', 'workload_record')
        )
            AND relations.relkind = 'r'
    ) AS approved_table_count,
    (
        (SELECT count(*) FROM core.location)
        + (SELECT count(*) FROM workforce.employee)
        + (SELECT count(*) FROM vendor.vendor)
        + (SELECT count(*) FROM inventory.inventory_item)
        + (SELECT count(*) FROM ticketing.ticket)
        + (SELECT count(*) FROM workforce.assignment)
        + (SELECT count(*) FROM workforce.coverage_schedule)
        + (SELECT count(*) FROM workforce.workload_record)
    ) AS tier_0_1_row_count,
    'PASS' AS validation_result;
