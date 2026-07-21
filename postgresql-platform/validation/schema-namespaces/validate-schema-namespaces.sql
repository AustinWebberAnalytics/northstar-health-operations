-- Northstar Health Operations
-- Purpose: Confirm that all six approved PostgreSQL schema namespaces exist.
-- Authority: Enterprise Database Platform Decision and issue #7.
-- Boundary: Read-only namespace validation; no database state is modified.

DO $validation$
DECLARE
    missing_schemas TEXT;
BEGIN
    SELECT string_agg(expected_schema, ', ' ORDER BY expected_schema)
    INTO missing_schemas
    FROM unnest(
        ARRAY[
            'core',
            'workforce',
            'vendor',
            'inventory',
            'ticketing',
            'relationships'
        ]
    ) AS expected_schemas(expected_schema)
    WHERE NOT EXISTS (
        SELECT 1
        FROM information_schema.schemata AS actual_schema
        WHERE actual_schema.schema_name = expected_schema
    );

    IF missing_schemas IS NOT NULL THEN
        RAISE EXCEPTION
            'Schema namespace validation failed. Missing approved schemas: %',
            missing_schemas;
    END IF;
END
$validation$;

WITH expected_schemas (namespace_order, schema_name) AS (
    VALUES
        (1, 'core'),
        (2, 'workforce'),
        (3, 'vendor'),
        (4, 'inventory'),
        (5, 'ticketing'),
        (6, 'relationships')
)
SELECT
    expected_schemas.schema_name,
    actual_schemas.schema_owner
FROM expected_schemas
INNER JOIN information_schema.schemata AS actual_schemas
    ON actual_schemas.schema_name = expected_schemas.schema_name
ORDER BY expected_schemas.namespace_order;
