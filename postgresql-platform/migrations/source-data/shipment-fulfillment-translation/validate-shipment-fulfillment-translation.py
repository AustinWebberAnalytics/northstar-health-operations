#!/usr/bin/env python3
"""Validate approved Shipment and Fulfillment Event translation rules."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import sys
import tempfile
from collections import Counter
from pathlib import Path


PASS_MESSAGE = "SHIPMENT FULFILLMENT TRANSLATION VALIDATION: PASS"
EXPECTED_SHIPMENT_COUNT = 6
EXPECTED_FULFILLMENT_COUNT = 6

FIELD_RULE_HEADERS = [
    "field_rule_id",
    "shipment_field",
    "fulfillment_field",
    "authority",
    "comparison_rule",
    "allowed_difference",
    "enforcement_stage",
    "contradiction_action",
]
APPROVED_FIELD_RULES = [
    ["FR-001", "vendor_id", "vendor_id", "shipment", "exact_match", "none", "migration_validation_then_later_cross_table_trigger", "preserve_both_and_report_exception"],
    ["FR-002", "item_id", "item_id", "shipment", "exact_match", "none", "migration_validation_then_later_cross_table_trigger", "preserve_both_and_report_exception"],
    ["FR-003", "location_id", "location_id", "shipment", "exact_match", "none", "migration_validation_then_later_cross_table_trigger", "preserve_both_and_report_exception"],
    ["FR-004", "related_ticket_id", "related_ticket_id", "shipment", "exact_match", "none", "migration_validation_then_later_cross_table_trigger", "preserve_both_and_report_exception"],
    ["FR-005", "order_date", "order_date", "shipment", "exact_match", "none", "migration_validation_then_later_cross_table_trigger", "preserve_both_and_report_exception"],
    ["FR-006", "expected_delivery_date", "expected_delivery_date", "shipment", "exact_match", "none", "migration_validation_then_later_cross_table_trigger", "preserve_both_and_report_exception"],
    ["FR-007", "actual_delivery_date", "actual_delivery_date", "shipment", "exact_match", "none", "migration_validation_then_later_cross_table_trigger", "preserve_both_and_report_exception"],
    ["FR-008", "ordered_quantity", "expected_quantity", "shipment", "exact_match", "none", "migration_validation_then_later_cross_table_trigger", "preserve_both_and_report_exception"],
    ["FR-009", "received_quantity", "received_quantity", "shipment_physical_movement", "pending_snapshot_translation", "shipment_blank_may_pair_with_fulfillment_zero_only_while_fulfillment_is_pending", "migration_validation_then_later_cross_table_trigger", "preserve_both_and_report_exception"],
    ["FR-010", "fulfillment_accuracy_flag", "fulfillment_accuracy_flag", "shipment_when_assessable", "pending_snapshot_translation", "shipment_blank_may_pair_with_fulfillment_false_only_while_fulfillment_is_pending", "migration_validation_then_later_cross_table_trigger", "preserve_both_and_report_exception"],
    ["FR-011", "delay_flag", "delay_flag", "shipment", "exact_match", "none", "migration_validation_then_later_cross_table_trigger", "preserve_both_and_report_exception"],
    ["FR-012", "delivery_status", "delivery_status", "independent_concepts", "status_matrix", "shipment_lifecycle_and_fulfillment_delivery_timing_are_not_directly_equal", "migration_validation_then_later_cross_table_trigger", "preserve_both_and_report_exception"],
]

STATUS_RULE_HEADERS = [
    "status_rule_id",
    "shipment_delivery_status",
    "fulfillment_delivery_status",
    "fulfillment_status",
    "received_state",
    "interpretation",
]
APPROVED_STATUS_RULES = [
    ["SR-001", "Pending", "Pending", "Pending", "pending_zero_snapshot", "Physical receipt is not finalized and the assessment records zero received to date"],
    ["SR-002", "Received", "Delivered", "Complete", "complete", "Complete shipment delivered without a recorded delay"],
    ["SR-003", "Received", "Delayed", "Complete", "complete", "Complete shipment delivered late"],
    ["SR-004", "Partial", "Delivered", "Partial", "partial", "Partial quantity delivered without a recorded delay"],
    ["SR-005", "Partial", "Delayed", "Partial", "partial", "Partial quantity delivered late"],
    ["SR-006", "Delayed", "Delayed", "Pending", "pending_zero_snapshot", "Shipment is overdue and no physical receipt quantity is finalized"],
    ["SR-007", "Delayed", "Delayed", "Partial", "partial", "Shipment is delayed with a partial quantity received"],
    ["SR-008", "Delayed", "Delayed", "Complete", "complete", "Shipment was completed after a delay"],
]

EXACT_FIELD_RULES = [
    ("vendor_id", "vendor_id"),
    ("item_id", "item_id"),
    ("location_id", "location_id"),
    ("related_ticket_id", "related_ticket_id"),
    ("order_date", "order_date"),
    ("expected_delivery_date", "expected_delivery_date"),
    ("actual_delivery_date", "actual_delivery_date"),
    ("ordered_quantity", "expected_quantity"),
    ("delay_flag", "delay_flag"),
]

SHIPMENT_REQUIRED_FIELDS = {
    "shipment_id",
    "vendor_id",
    "item_id",
    "location_id",
    "related_ticket_id",
    "order_date",
    "expected_delivery_date",
    "actual_delivery_date",
    "delivery_status",
    "ordered_quantity",
    "received_quantity",
    "fulfillment_accuracy_flag",
    "delay_flag",
}
FULFILLMENT_REQUIRED_FIELDS = {
    "fulfillment_event_id",
    "shipment_id",
    "vendor_id",
    "item_id",
    "location_id",
    "related_ticket_id",
    "order_date",
    "expected_delivery_date",
    "actual_delivery_date",
    "delivery_status",
    "fulfillment_status",
    "expected_quantity",
    "received_quantity",
    "fulfillment_accuracy_flag",
    "delay_flag",
    "delay_days",
    "partial_fulfillment_flag",
}


class TranslationValidationError(RuntimeError):
    """Raised when a governed Shipment/Fulfillment invariant fails."""


def sha256_hex(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def decode_strict_utf8(path: Path, label: str) -> tuple[bytes, str]:
    if not path.is_file():
        raise TranslationValidationError(f"{label} not found: {path}")
    content = path.read_bytes()
    if content.startswith(b"\xef\xbb\xbf"):
        raise TranslationValidationError(f"{label} must be UTF-8 without a BOM.")
    try:
        text = content.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise TranslationValidationError(
            f"{label} failed strict UTF-8 decoding: {exc}"
        ) from exc
    return content, text


def parse_csv(text: str, label: str) -> tuple[list[str], list[list[str]]]:
    try:
        rows = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as exc:
        raise TranslationValidationError(f"{label} is not valid CSV: {exc}") from exc
    if not rows:
        raise TranslationValidationError(f"{label} contains no CSV rows.")
    header = rows[0]
    if not header or any(not field for field in header):
        raise TranslationValidationError(f"{label} contains an empty header field.")
    if len(set(header)) != len(header):
        raise TranslationValidationError(f"{label} contains duplicate headers.")
    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(header):
            raise TranslationValidationError(
                f"{label} row {row_number} contains {len(row)} columns; "
                f"expected {len(header)}."
            )
    return header, rows[1:]


def rows_as_dicts(header: list[str], rows: list[list[str]]) -> list[dict[str, str]]:
    return [dict(zip(header, row, strict=True)) for row in rows]


def csv_bytes(header: list[str], rows: list[list[str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def path_is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
    except ValueError:
        return False
    return True


def write_atomic(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(content)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def default_paths() -> tuple[Path, Path, Path, Path, Path]:
    repository_root = Path(__file__).resolve().parents[4]
    procedure_directory = Path(__file__).resolve().parent
    return (
        repository_root / "inventory-operations/datasets/data/vendor-shipments.csv",
        repository_root / "vendor-performance/datasets/data/vendor-fulfillment-events.csv",
        procedure_directory / "shipment-fulfillment-field-rules.csv",
        procedure_directory / "shipment-fulfillment-status-rules.csv",
        repository_root / "postgresql-platform/migration-output/shipment-fulfillment-translation",
    )


def parse_arguments() -> argparse.Namespace:
    shipment, fulfillment, field_rules, status_rules, output = default_paths()
    parser = argparse.ArgumentParser(
        description=(
            "Validate approved Shipment and Fulfillment Event authority, pending-state, "
            "and status-translation rules without modifying either source."
        )
    )
    parser.add_argument("--shipment-source", type=Path, default=shipment)
    parser.add_argument("--fulfillment-source", type=Path, default=fulfillment)
    parser.add_argument("--field-rules", type=Path, default=field_rules)
    parser.add_argument("--status-rules", type=Path, default=status_rules)
    parser.add_argument("--output-directory", type=Path, default=output)
    return parser.parse_args()


def validate_required_fields(header: list[str], required: set[str], label: str) -> None:
    missing = required - set(header)
    if missing:
        raise TranslationValidationError(
            f"{label} is missing required fields: {', '.join(sorted(missing))}"
        )


def validate_unique(rows: list[dict[str, str]], field: str, label: str) -> None:
    values = [row[field] for row in rows]
    if any(not value for value in values):
        raise TranslationValidationError(f"{label} contains a blank {field}.")
    duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
    if duplicates:
        raise TranslationValidationError(
            f"{label} contains duplicate {field} values: {', '.join(duplicates)}"
        )


def parse_nonnegative_integer(value: str, field: str, record_id: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise TranslationValidationError(
            f"{record_id} contains non-integer {field}: {value}"
        ) from exc
    if parsed < 0:
        raise TranslationValidationError(
            f"{record_id} contains negative {field}: {value}"
        )
    return parsed


def validate_and_compare(
    shipment_source: Path,
    fulfillment_source: Path,
    field_rules: Path,
    status_rules: Path,
    output_directory: Path,
) -> dict[str, object]:
    repository_root = Path(__file__).resolve().parents[4]
    governed_output_root = (repository_root / "postgresql-platform/migration-output").resolve()
    shipment_source = shipment_source.expanduser().resolve()
    fulfillment_source = fulfillment_source.expanduser().resolve()
    field_rules = field_rules.expanduser().resolve()
    status_rules = status_rules.expanduser().resolve()
    output_directory = output_directory.expanduser().resolve()

    if not path_is_within(output_directory, governed_output_root):
        raise TranslationValidationError(
            "Output must remain under the ignored migration-output boundary: "
            f"{governed_output_root}"
        )

    comparison_path = output_directory / "shipment-fulfillment-comparison.csv"
    exception_path = output_directory / "shipment-fulfillment-translation-exceptions.csv"
    source_paths = {
        "shipment_source": shipment_source,
        "fulfillment_source": fulfillment_source,
        "field_rules": field_rules,
        "status_rules": status_rules,
    }
    if {comparison_path, exception_path} & set(source_paths.values()):
        raise TranslationValidationError("Generated output must not replace a governed input.")

    comparison_path.unlink(missing_ok=True)
    exception_path.unlink(missing_ok=True)

    input_hashes: dict[str, str] = {}
    parsed: dict[str, tuple[list[str], list[list[str]]]] = {}
    for key, path in source_paths.items():
        content, text = decode_strict_utf8(path, key.replace("_", " ").title())
        input_hashes[key] = sha256_hex(content)
        parsed[key] = parse_csv(text, key.replace("_", " ").title())

    field_header, field_rows = parsed["field_rules"]
    if field_header != FIELD_RULE_HEADERS or field_rows != APPROVED_FIELD_RULES:
        raise TranslationValidationError(
            "Field-rule artifact does not exactly match the Issue #21 approval."
        )
    status_header, status_rows = parsed["status_rules"]
    if status_header != STATUS_RULE_HEADERS or status_rows != APPROVED_STATUS_RULES:
        raise TranslationValidationError(
            "Status-rule artifact does not exactly match the Issue #21 approval."
        )
    allowed_statuses = {
        (row[1], row[2], row[3]): row[4] for row in APPROVED_STATUS_RULES
    }

    shipment_header, shipment_rows_raw = parsed["shipment_source"]
    fulfillment_header, fulfillment_rows_raw = parsed["fulfillment_source"]
    validate_required_fields(shipment_header, SHIPMENT_REQUIRED_FIELDS, "Shipment source")
    validate_required_fields(
        fulfillment_header, FULFILLMENT_REQUIRED_FIELDS, "Fulfillment Event source"
    )
    shipment_rows = rows_as_dicts(shipment_header, shipment_rows_raw)
    fulfillment_rows = rows_as_dicts(fulfillment_header, fulfillment_rows_raw)
    validate_unique(shipment_rows, "shipment_id", "Shipment source")
    validate_unique(fulfillment_rows, "fulfillment_event_id", "Fulfillment Event source")
    if len(shipment_rows) != EXPECTED_SHIPMENT_COUNT:
        raise TranslationValidationError(
            f"Shipment source contains {len(shipment_rows)} records; "
            f"expected {EXPECTED_SHIPMENT_COUNT}."
        )
    if len(fulfillment_rows) != EXPECTED_FULFILLMENT_COUNT:
        raise TranslationValidationError(
            f"Fulfillment Event source contains {len(fulfillment_rows)} records; "
            f"expected {EXPECTED_FULFILLMENT_COUNT}."
        )

    shipments_by_id = {row["shipment_id"]: row for row in shipment_rows}
    referenced_shipments = {row["shipment_id"] for row in fulfillment_rows}
    missing_events = sorted(set(shipments_by_id) - referenced_shipments)
    if missing_events:
        raise TranslationValidationError(
            "Current Shipment records missing a Fulfillment Event comparison: "
            + ", ".join(missing_events)
        )

    comparison_header = [
        "fulfillment_event_id",
        "shipment_id",
        "shipment_vendor_id",
        "fulfillment_vendor_id",
        "shipment_item_id",
        "fulfillment_item_id",
        "shipment_location_id",
        "fulfillment_location_id",
        "shipment_related_ticket_id",
        "fulfillment_related_ticket_id",
        "shipment_order_date",
        "fulfillment_order_date",
        "shipment_expected_delivery_date",
        "fulfillment_expected_delivery_date",
        "shipment_actual_delivery_date",
        "fulfillment_actual_delivery_date",
        "shipment_ordered_quantity",
        "fulfillment_expected_quantity",
        "shipment_received_quantity",
        "fulfillment_received_quantity",
        "shipment_fulfillment_accuracy_flag",
        "fulfillment_accuracy_flag",
        "shipment_delay_flag",
        "fulfillment_delay_flag",
        "shipment_delivery_status",
        "fulfillment_delivery_status",
        "fulfillment_status",
        "received_state",
        "comparison_status",
        "exception_count",
    ]
    exception_header = [
        "fulfillment_event_id",
        "shipment_id",
        "rule_scope",
        "shipment_field",
        "fulfillment_field",
        "shipment_value",
        "fulfillment_value",
        "exception_reason",
    ]
    comparison_rows: list[list[str]] = []
    exception_rows: list[list[str]] = []

    def add_exception(
        event: dict[str, str],
        shipment: dict[str, str] | None,
        scope: str,
        shipment_field: str,
        fulfillment_field: str,
        reason: str,
    ) -> None:
        exception_rows.append(
            [
                event["fulfillment_event_id"],
                event["shipment_id"],
                scope,
                shipment_field,
                fulfillment_field,
                shipment.get(shipment_field, "") if shipment else "",
                event.get(fulfillment_field, ""),
                reason,
            ]
        )

    for event in fulfillment_rows:
        shipment = shipments_by_id.get(event["shipment_id"])
        if shipment is None:
            add_exception(
                event,
                None,
                "reference",
                "shipment_id",
                "shipment_id",
                "Fulfillment Event references a missing Shipment",
            )
            continue

        start_exceptions = len(exception_rows)
        for shipment_field, fulfillment_field in EXACT_FIELD_RULES:
            if shipment[shipment_field] != event[fulfillment_field]:
                add_exception(
                    event,
                    shipment,
                    "field_authority",
                    shipment_field,
                    fulfillment_field,
                    "Repeated field does not match Shipment authority",
                )

        status_key = (
            shipment["delivery_status"],
            event["delivery_status"],
            event["fulfillment_status"],
        )
        received_state = allowed_statuses.get(status_key, "")
        if not received_state:
            add_exception(
                event,
                shipment,
                "status_matrix",
                "delivery_status",
                "delivery_status",
                "Status combination is not approved",
            )

        ordered = parse_nonnegative_integer(
            shipment["ordered_quantity"], "ordered_quantity", shipment["shipment_id"]
        )
        expected = parse_nonnegative_integer(
            event["expected_quantity"], "expected_quantity", event["fulfillment_event_id"]
        )
        event_received = parse_nonnegative_integer(
            event["received_quantity"], "received_quantity", event["fulfillment_event_id"]
        )
        if ordered == 0 or expected == 0:
            add_exception(
                event,
                shipment,
                "quantity",
                "ordered_quantity",
                "expected_quantity",
                "Ordered and expected quantity must be greater than zero",
            )

        shipment_received_text = shipment["received_quantity"]
        if shipment_received_text == "":
            pending_allowed = (
                received_state == "pending_zero_snapshot"
                and event_received == 0
                and shipment["actual_delivery_date"] == ""
                and event["actual_delivery_date"] == ""
                and shipment["fulfillment_accuracy_flag"] == ""
                and event["fulfillment_accuracy_flag"] == "FALSE"
            )
            if not pending_allowed:
                add_exception(
                    event,
                    shipment,
                    "pending_translation",
                    "received_quantity",
                    "received_quantity",
                    "Blank Shipment quantity does not satisfy the approved pending snapshot rule",
                )
        else:
            shipment_received = parse_nonnegative_integer(
                shipment_received_text,
                "received_quantity",
                shipment["shipment_id"],
            )
            if shipment_received == 0:
                add_exception(
                    event,
                    shipment,
                    "quantity",
                    "received_quantity",
                    "received_quantity",
                    "Confirmed Shipment zero has no approved final-state translation",
                )
            if shipment_received != event_received:
                add_exception(
                    event,
                    shipment,
                    "field_authority",
                    "received_quantity",
                    "received_quantity",
                    "Known received quantities do not match",
                )
            if not shipment["fulfillment_accuracy_flag"]:
                add_exception(
                    event,
                    shipment,
                    "assessment",
                    "fulfillment_accuracy_flag",
                    "fulfillment_accuracy_flag",
                    "Known Shipment receipt requires an assessable accuracy flag",
                )
            elif shipment["fulfillment_accuracy_flag"] != event["fulfillment_accuracy_flag"]:
                add_exception(
                    event,
                    shipment,
                    "field_authority",
                    "fulfillment_accuracy_flag",
                    "fulfillment_accuracy_flag",
                    "Assessable fulfillment-accuracy flags do not match",
                )

        if received_state == "pending_zero_snapshot" and event_received != 0:
            add_exception(
                event,
                shipment,
                "status_quantity",
                "received_quantity",
                "received_quantity",
                "Pending assessment must record zero received to date",
            )
        elif received_state == "partial" and not (0 < event_received < expected):
            add_exception(
                event,
                shipment,
                "status_quantity",
                "ordered_quantity",
                "received_quantity",
                "Partial assessment requires received quantity between zero and expected",
            )
        elif received_state == "complete" and event_received != expected:
            add_exception(
                event,
                shipment,
                "status_quantity",
                "ordered_quantity",
                "received_quantity",
                "Complete assessment requires received quantity to equal expected",
            )

        delay_true = event["delay_flag"] == "TRUE"
        if (event["delivery_status"] == "Delayed") != delay_true:
            add_exception(
                event,
                shipment,
                "delivery_timing",
                "delay_flag",
                "delivery_status",
                "Fulfillment delivery status and delay flag disagree",
            )
        if event["delivery_status"] == "Delivered" and not event["actual_delivery_date"]:
            add_exception(
                event,
                shipment,
                "delivery_timing",
                "actual_delivery_date",
                "delivery_status",
                "Delivered assessment requires an actual delivery date",
            )
        if event["delivery_status"] == "Pending" and event["actual_delivery_date"]:
            add_exception(
                event,
                shipment,
                "delivery_timing",
                "actual_delivery_date",
                "delivery_status",
                "Pending assessment cannot contain an actual delivery date",
            )
        if shipment["delivery_status"] in {"Received", "Partial"} and not shipment["actual_delivery_date"]:
            add_exception(
                event,
                shipment,
                "shipment_lifecycle",
                "actual_delivery_date",
                "delivery_status",
                "Received or Partial Shipment requires an actual delivery date",
            )
        if shipment["delivery_status"] == "Pending" and shipment["actual_delivery_date"]:
            add_exception(
                event,
                shipment,
                "shipment_lifecycle",
                "actual_delivery_date",
                "delivery_status",
                "Pending Shipment cannot contain an actual delivery date",
            )

        pair_exception_count = len(exception_rows) - start_exceptions
        comparison_rows.append(
            [
                event["fulfillment_event_id"],
                shipment["shipment_id"],
                shipment["vendor_id"],
                event["vendor_id"],
                shipment["item_id"],
                event["item_id"],
                shipment["location_id"],
                event["location_id"],
                shipment["related_ticket_id"],
                event["related_ticket_id"],
                shipment["order_date"],
                event["order_date"],
                shipment["expected_delivery_date"],
                event["expected_delivery_date"],
                shipment["actual_delivery_date"],
                event["actual_delivery_date"],
                shipment["ordered_quantity"],
                event["expected_quantity"],
                shipment["received_quantity"],
                event["received_quantity"],
                shipment["fulfillment_accuracy_flag"],
                event["fulfillment_accuracy_flag"],
                shipment["delay_flag"],
                event["delay_flag"],
                shipment["delivery_status"],
                event["delivery_status"],
                event["fulfillment_status"],
                received_state,
                "PASS" if pair_exception_count == 0 else "EXCEPTION",
                str(pair_exception_count),
            ]
        )

    write_atomic(comparison_path, csv_bytes(comparison_header, comparison_rows))
    write_atomic(exception_path, csv_bytes(exception_header, exception_rows))

    comparison_bytes, comparison_text = decode_strict_utf8(
        comparison_path, "Generated Shipment/Fulfillment comparison"
    )
    final_comparison_header, final_comparison_rows = parse_csv(
        comparison_text, "Generated Shipment/Fulfillment comparison"
    )
    if final_comparison_header != comparison_header or final_comparison_rows != comparison_rows:
        raise TranslationValidationError("Generated comparison changed after placement.")

    exception_bytes, exception_text = decode_strict_utf8(
        exception_path, "Generated Shipment/Fulfillment exception report"
    )
    final_exception_header, final_exception_rows = parse_csv(
        exception_text, "Generated Shipment/Fulfillment exception report"
    )
    if final_exception_header != exception_header or final_exception_rows != exception_rows:
        raise TranslationValidationError("Generated exception report changed after placement.")

    for key, path in source_paths.items():
        if sha256_hex(path.read_bytes()) != input_hashes[key]:
            raise TranslationValidationError(f"Governed input changed during validation: {path}")

    if exception_rows:
        raise TranslationValidationError(
            f"Shipment/Fulfillment comparison produced {len(exception_rows)} exception(s)."
        )

    return {
        "shipment_source": shipment_source,
        "fulfillment_source": fulfillment_source,
        "field_rules": field_rules,
        "status_rules": status_rules,
        "comparison_output": comparison_path,
        "exception_output": exception_path,
        "shipment_records": len(shipment_rows),
        "fulfillment_records": len(fulfillment_rows),
        "comparison_records": len(comparison_rows),
        "exception_records": len(exception_rows),
        "pending_translations": sum(
            1 for row in comparison_rows if row[comparison_header.index("received_state")] == "pending_zero_snapshot"
        ),
        "exact_received_pairs": sum(
            1
            for row in comparison_rows
            if row[comparison_header.index("shipment_received_quantity")]
            == row[comparison_header.index("fulfillment_received_quantity")]
        ),
        "input_hashes": input_hashes,
        "comparison_hash": sha256_hex(comparison_bytes),
        "exception_hash": sha256_hex(exception_bytes),
    }


def main() -> int:
    arguments = parse_arguments()
    try:
        result = validate_and_compare(
            arguments.shipment_source,
            arguments.fulfillment_source,
            arguments.field_rules,
            arguments.status_rules,
            arguments.output_directory,
        )
    except (TranslationValidationError, OSError) as exc:
        print("SHIPMENT FULFILLMENT TRANSLATION VALIDATION: FAIL", file=sys.stderr)
        print(f"Reason: {exc}", file=sys.stderr)
        return 1

    print(PASS_MESSAGE)
    print(f"Shipment source: {result['shipment_source']}")
    print(f"Fulfillment Event source: {result['fulfillment_source']}")
    print(f"Field-rule artifact: {result['field_rules']}")
    print(f"Status-rule artifact: {result['status_rules']}")
    print(f"Generated comparison output: {result['comparison_output']}")
    print(f"Generated exception report: {result['exception_output']}")
    print(f"Shipment records: {result['shipment_records']}")
    print(f"Fulfillment Event records: {result['fulfillment_records']}")
    print(f"Compared Shipment/Fulfillment pairs: {result['comparison_records']}")
    print(f"Approved pending blank/zero translations: {result['pending_translations']}")
    print(f"Exact received-quantity pairs: {result['exact_received_pairs']}")
    print(f"Contradiction exceptions: {result['exception_records']}")
    print("Repeated references, dates, ordered/expected quantity, and delay flag: PASS")
    print("Independent status combinations: PASS")
    print("Pending quantity and accuracy translations: PASS")
    print("Both source representations retained: PASS")
    print("Generated outputs strict UTF-8 without BOM: PASS")
    print("All governed inputs unchanged: PASS")
    for key, digest in result["input_hashes"].items():
        print(f"{key.replace('_', ' ').title()} SHA-256: {digest}")
    print(f"Comparison output SHA-256: {result['comparison_hash']}")
    print(f"Exception report SHA-256: {result['exception_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
