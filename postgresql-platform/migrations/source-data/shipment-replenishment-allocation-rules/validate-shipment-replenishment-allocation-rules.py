#!/usr/bin/env python3
"""Validate approved Shipment Replenishment Allocation timing and ceiling rules."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import sys
import tempfile
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path


PASS_MESSAGE = "SHIPMENT REPLENISHMENT ALLOCATION RULE VALIDATION: PASS"
EXPECTED_SHIPMENT_COUNT = 6
EXPECTED_REPLENISHMENT_COUNT = 5
EXPECTED_KNOWN_RECEIVED = 4
EXPECTED_UNKNOWN_RECEIVED = 2
EXPECTED_KNOWN_APPROVED = 5
EXPECTED_UNKNOWN_APPROVED = 0

RULE_HEADERS = [
    "rule_id",
    "decision_area",
    "governing_field",
    "approved_rule",
    "rationale",
    "enforcement_stage",
    "violation_action",
]

APPROVED_RULES = [
    ["AR-001", "shipment_timing", "received_quantity", "allocation_requires_nonblank_received_quantity", "allocation records inventory actually received rather than expected inventory", "migration_validation_then_later_aggregate_trigger", "reject_allocation_and_report_exception"],
    ["AR-002", "replenishment_timing", "approved_quantity", "allocation_requires_nonblank_approved_quantity", "allocation cannot exceed an unapproved request", "migration_validation_then_later_aggregate_trigger", "reject_allocation_and_report_exception"],
    ["AR-003", "shipment_ceiling", "received_quantity", "sum_allocated_by_shipment_must_not_exceed_received_quantity", "received quantity is the authoritative physical quantity available to allocate", "migration_validation_then_later_aggregate_trigger", "reject_change_and_report_exception"],
    ["AR-004", "replenishment_ceiling", "approved_quantity", "sum_allocated_by_replenishment_must_not_exceed_approved_quantity", "approved quantity is the authoritative replenishment authorization", "migration_validation_then_later_aggregate_trigger", "reject_change_and_report_exception"],
    ["AR-005", "planning_values", "ordered_quantity|requested_quantity", "planning_values_are_not_allocation_ceilings", "ordered and requested quantities describe intent rather than received or authorized quantity", "validation_and_documentation", "do_not_substitute_planning_value"],
    ["AR-006", "partial_receipt", "received_quantity", "partial_receipt_may_be_allocated_up_to_received_quantity", "physically received inventory remains usable even when the shipment is incomplete", "migration_validation_then_later_aggregate_trigger", "reject_only_amount_above_received_quantity"],
    ["AR-007", "parent_quantity_change", "received_quantity|approved_quantity", "parent_change_must_not_leave_existing_allocations_above_new_ceiling", "quantity corrections must preserve aggregate integrity or be coordinated with allocation adjustments", "later_aggregate_trigger", "reject_uncoordinated_parent_change"],
    ["AR-008", "status_independence", "delivery_status|replenishment_status", "status_does_not_substitute_for_missing_governing_quantity", "status labels do not establish a numeric ceiling", "validation_and_documentation", "reject_allocation_and_report_exception"],
    ["AR-009", "current_data_boundary", "shipment_replenishment_allocation", "no_current_allocation_rows_may_be_inferred_or_created", "no authoritative allocation source exists and candidate relationships are not operational evidence", "migration_validation", "create_no_allocation_records"],
]

SHIPMENT_FIELDS = {
    "shipment_id",
    "ordered_quantity",
    "received_quantity",
    "delivery_status",
}
REPLENISHMENT_FIELDS = {
    "replenishment_id",
    "requested_quantity",
    "approved_quantity",
    "replenishment_status",
}


class RuleValidationError(RuntimeError):
    """Raised when a governed allocation-rule invariant fails."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def sha256_hex(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def decode_strict_utf8(path: Path, label: str) -> tuple[bytes, str]:
    if not path.is_file():
        raise RuleValidationError("missing_input", f"{label} not found: {path}")
    content = path.read_bytes()
    if content.startswith(b"\xef\xbb\xbf"):
        raise RuleValidationError("utf8_bom", f"{label} must be UTF-8 without a BOM.")
    try:
        text = content.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise RuleValidationError(
            "invalid_utf8", f"{label} failed strict UTF-8 decoding: {exc}"
        ) from exc
    return content, text


def parse_csv(text: str, label: str) -> tuple[list[str], list[list[str]]]:
    try:
        rows = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as exc:
        raise RuleValidationError("invalid_csv", f"{label} is not valid CSV: {exc}") from exc
    if not rows:
        raise RuleValidationError("empty_csv", f"{label} contains no CSV rows.")
    header = rows[0]
    if not header or any(not field for field in header):
        raise RuleValidationError("invalid_header", f"{label} contains an empty header field.")
    if len(set(header)) != len(header):
        raise RuleValidationError("duplicate_header", f"{label} contains duplicate headers.")
    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(header):
            raise RuleValidationError(
                "column_count",
                f"{label} row {row_number} contains {len(row)} columns; expected {len(header)}.",
            )
    return header, rows[1:]


def csv_bytes(header: list[str], rows: list[list[str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def rows_as_dicts(header: list[str], rows: list[list[str]]) -> list[dict[str, str]]:
    return [dict(zip(header, row, strict=True)) for row in rows]


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


def default_paths() -> tuple[Path, Path, Path, Path]:
    repository_root = Path(__file__).resolve().parents[4]
    procedure_directory = Path(__file__).resolve().parent
    return (
        repository_root / "inventory-operations/datasets/data/vendor-shipments.csv",
        repository_root / "inventory-operations/datasets/data/replenishment-events.csv",
        procedure_directory / "shipment-replenishment-allocation-rules.csv",
        repository_root / "postgresql-platform/migration-output/shipment-replenishment-allocation-rules",
    )


def parse_arguments() -> argparse.Namespace:
    shipment, replenishment, rules, output = default_paths()
    parser = argparse.ArgumentParser(
        description=(
            "Validate approved Shipment Replenishment Allocation timing and aggregate "
            "ceiling rules without creating operational allocation records."
        )
    )
    parser.add_argument("--shipment-source", type=Path, default=shipment)
    parser.add_argument("--replenishment-source", type=Path, default=replenishment)
    parser.add_argument("--rules", type=Path, default=rules)
    parser.add_argument("--output-directory", type=Path, default=output)
    return parser.parse_args()


def validate_required_fields(header: list[str], required: set[str], label: str) -> None:
    missing = required - set(header)
    if missing:
        raise RuleValidationError(
            "missing_fields", f"{label} is missing required fields: {', '.join(sorted(missing))}"
        )


def validate_unique(rows: list[dict[str, str]], field: str, label: str) -> None:
    values = [row[field] for row in rows]
    if any(not value for value in values):
        raise RuleValidationError("blank_identifier", f"{label} contains a blank {field}.")
    duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
    if duplicates:
        raise RuleValidationError(
            "duplicate_identifier", f"{label} contains duplicate {field} values: {', '.join(duplicates)}"
        )


def parse_positive(value: str, field: str, record_id: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise RuleValidationError(
            "invalid_quantity", f"{record_id} contains non-integer {field}: {value}"
        ) from exc
    if parsed <= 0:
        raise RuleValidationError(
            "invalid_quantity", f"{record_id} contains nonpositive {field}: {value}"
        )
    return parsed


def parse_optional_nonnegative(value: str, field: str, record_id: str) -> int | None:
    if value == "":
        return None
    try:
        parsed = int(value)
    except ValueError as exc:
        raise RuleValidationError(
            "invalid_quantity", f"{record_id} contains non-integer {field}: {value}"
        ) from exc
    if parsed < 0:
        raise RuleValidationError(
            "invalid_quantity", f"{record_id} contains negative {field}: {value}"
        )
    return parsed


def normalize_parents(
    shipment_rows: list[dict[str, str]], replenishment_rows: list[dict[str, str]]
) -> tuple[dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    shipments: dict[str, dict[str, object]] = {}
    replenishments: dict[str, dict[str, object]] = {}

    for row in shipment_rows:
        shipment_id = row["shipment_id"]
        ordered = parse_positive(row["ordered_quantity"], "ordered_quantity", shipment_id)
        received = parse_optional_nonnegative(
            row["received_quantity"], "received_quantity", shipment_id
        )
        if received is not None and received > ordered:
            raise RuleValidationError(
                "invalid_parent_quantity",
                f"{shipment_id} received_quantity exceeds ordered_quantity.",
            )
        shipments[shipment_id] = {
            "received_quantity": received,
            "delivery_status": row["delivery_status"],
        }

    for row in replenishment_rows:
        replenishment_id = row["replenishment_id"]
        requested = parse_positive(
            row["requested_quantity"], "requested_quantity", replenishment_id
        )
        approved = parse_optional_nonnegative(
            row["approved_quantity"], "approved_quantity", replenishment_id
        )
        if approved is not None and approved > requested:
            raise RuleValidationError(
                "invalid_parent_quantity",
                f"{replenishment_id} approved_quantity exceeds requested_quantity.",
            )
        replenishments[replenishment_id] = {
            "approved_quantity": approved,
            "replenishment_status": row["replenishment_status"],
        }

    return shipments, replenishments


def validate_allocations(
    shipments: dict[str, dict[str, object]],
    replenishments: dict[str, dict[str, object]],
    allocations: list[dict[str, object]],
) -> None:
    seen_pairs: set[tuple[str, str]] = set()
    shipment_totals: defaultdict[str, int] = defaultdict(int)
    replenishment_totals: defaultdict[str, int] = defaultdict(int)

    for row in allocations:
        shipment_id = str(row["shipment_id"])
        replenishment_id = str(row["replenishment_id"])
        pair = (shipment_id, replenishment_id)
        if pair in seen_pairs:
            raise RuleValidationError(
                "duplicate_pair",
                f"Duplicate allocation pair: {shipment_id}, {replenishment_id}.",
            )
        seen_pairs.add(pair)

        if shipment_id not in shipments:
            raise RuleValidationError("missing_shipment", f"Unknown shipment_id: {shipment_id}.")
        if replenishment_id not in replenishments:
            raise RuleValidationError(
                "missing_replenishment", f"Unknown replenishment_id: {replenishment_id}."
            )

        quantity = row["allocated_quantity"]
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise RuleValidationError(
                "nonpositive_allocation",
                f"Allocation for {shipment_id}, {replenishment_id} must be a positive integer.",
            )

        received = shipments[shipment_id]["received_quantity"]
        approved = replenishments[replenishment_id]["approved_quantity"]
        if received is None:
            raise RuleValidationError(
                "shipment_quantity_unknown",
                f"{shipment_id} cannot be allocated before received_quantity is known.",
            )
        if approved is None:
            raise RuleValidationError(
                "replenishment_quantity_unknown",
                f"{replenishment_id} cannot receive allocation before approved_quantity is known.",
            )

        shipment_totals[shipment_id] += quantity
        replenishment_totals[replenishment_id] += quantity

    for shipment_id, total in shipment_totals.items():
        ceiling = int(shipments[shipment_id]["received_quantity"])
        if total > ceiling:
            raise RuleValidationError(
                "shipment_ceiling_exceeded",
                f"{shipment_id} allocation total {total} exceeds received_quantity {ceiling}.",
            )

    for replenishment_id, total in replenishment_totals.items():
        ceiling = int(replenishments[replenishment_id]["approved_quantity"])
        if total > ceiling:
            raise RuleValidationError(
                "replenishment_ceiling_exceeded",
                f"{replenishment_id} allocation total {total} exceeds approved_quantity {ceiling}.",
            )


def run_scenarios(
    shipments: dict[str, dict[str, object]],
    replenishments: dict[str, dict[str, object]],
) -> list[list[str]]:
    scenarios: list[tuple[str, str, str, dict[str, dict[str, object]], dict[str, dict[str, object]], list[dict[str, object]]]] = []

    scenarios.append((
        "SC-001", "full_receipt_at_ceiling", "PASS", shipments, replenishments,
        [{"shipment_id": "SHIP-1001", "replenishment_id": "REPL-1001", "allocated_quantity": 60}],
    ))
    scenarios.append((
        "SC-002", "partial_receipt_at_received_ceiling", "PASS", shipments, replenishments,
        [{"shipment_id": "SHIP-1006", "replenishment_id": "REPL-1003", "allocated_quantity": 35}],
    ))
    scenarios.append((
        "SC-003", "unknown_received_quantity", "shipment_quantity_unknown", shipments, replenishments,
        [{"shipment_id": "SHIP-1003", "replenishment_id": "REPL-1004", "allocated_quantity": 1}],
    ))

    unknown_approval = deepcopy(replenishments)
    unknown_approval["REPL-1001"]["approved_quantity"] = None
    scenarios.append((
        "SC-004", "unknown_approved_quantity", "replenishment_quantity_unknown", shipments, unknown_approval,
        [{"shipment_id": "SHIP-1001", "replenishment_id": "REPL-1001", "allocated_quantity": 1}],
    ))
    scenarios.append((
        "SC-005", "aggregate_shipment_overallocation", "shipment_ceiling_exceeded", shipments, replenishments,
        [
            {"shipment_id": "SHIP-1001", "replenishment_id": "REPL-1001", "allocated_quantity": 40},
            {"shipment_id": "SHIP-1001", "replenishment_id": "REPL-1002", "allocated_quantity": 30},
        ],
    ))
    scenarios.append((
        "SC-006", "aggregate_replenishment_overallocation", "replenishment_ceiling_exceeded", shipments, replenishments,
        [
            {"shipment_id": "SHIP-1001", "replenishment_id": "REPL-1001", "allocated_quantity": 30},
            {"shipment_id": "SHIP-1005", "replenishment_id": "REPL-1001", "allocated_quantity": 40},
        ],
    ))
    scenarios.append((
        "SC-007", "zero_allocation", "nonpositive_allocation", shipments, replenishments,
        [{"shipment_id": "SHIP-1001", "replenishment_id": "REPL-1001", "allocated_quantity": 0}],
    ))
    scenarios.append((
        "SC-008", "duplicate_parent_pair", "duplicate_pair", shipments, replenishments,
        [
            {"shipment_id": "SHIP-1001", "replenishment_id": "REPL-1001", "allocated_quantity": 20},
            {"shipment_id": "SHIP-1001", "replenishment_id": "REPL-1001", "allocated_quantity": 20},
        ],
    ))

    reduced_receipt = deepcopy(shipments)
    reduced_receipt["SHIP-1001"]["received_quantity"] = 50
    scenarios.append((
        "SC-009", "received_quantity_reduction_below_allocation", "shipment_ceiling_exceeded", reduced_receipt, replenishments,
        [{"shipment_id": "SHIP-1001", "replenishment_id": "REPL-1001", "allocated_quantity": 60}],
    ))

    reduced_approval = deepcopy(replenishments)
    reduced_approval["REPL-1001"]["approved_quantity"] = 50
    scenarios.append((
        "SC-010", "approved_quantity_reduction_below_allocation", "replenishment_ceiling_exceeded", shipments, reduced_approval,
        [{"shipment_id": "SHIP-1001", "replenishment_id": "REPL-1001", "allocated_quantity": 60}],
    ))

    results: list[list[str]] = []
    for scenario_id, name, expected, scenario_shipments, scenario_replenishments, allocations in scenarios:
        try:
            validate_allocations(scenario_shipments, scenario_replenishments, allocations)
            actual = "PASS"
        except RuleValidationError as exc:
            actual = exc.code
        outcome = "PASS" if actual == expected else "FAIL"
        results.append([scenario_id, name, expected, actual, outcome])
    return results


def path_is_within(path: Path, directory: Path) -> bool:
    try:
        path.resolve().relative_to(directory.resolve())
    except ValueError:
        return False
    return True


def main() -> int:
    args = parse_arguments()
    repository_root = Path(__file__).resolve().parents[4]
    migration_output_root = repository_root / "postgresql-platform/migration-output"
    output_directory = args.output_directory.resolve()
    if not path_is_within(output_directory, migration_output_root):
        raise RuleValidationError(
            "invalid_output_path",
            f"Output directory must remain under {migration_output_root}.",
        )

    shipment_bytes, shipment_text = decode_strict_utf8(args.shipment_source, "Shipment source")
    replenishment_bytes, replenishment_text = decode_strict_utf8(
        args.replenishment_source, "Replenishment source"
    )
    rule_bytes, rule_text = decode_strict_utf8(args.rules, "Allocation rule artifact")
    initial_hashes = {
        "shipment": sha256_hex(shipment_bytes),
        "replenishment": sha256_hex(replenishment_bytes),
        "rules": sha256_hex(rule_bytes),
    }

    shipment_header, shipment_data = parse_csv(shipment_text, "Shipment source")
    replenishment_header, replenishment_data = parse_csv(
        replenishment_text, "Replenishment source"
    )
    rule_header, rule_data = parse_csv(rule_text, "Allocation rule artifact")

    if rule_header != RULE_HEADERS or rule_data != APPROVED_RULES:
        raise RuleValidationError(
            "decision_drift", "Allocation rule artifact does not match the approved Issue #22 decision."
        )
    validate_required_fields(shipment_header, SHIPMENT_FIELDS, "Shipment source")
    validate_required_fields(
        replenishment_header, REPLENISHMENT_FIELDS, "Replenishment source"
    )

    shipment_rows = rows_as_dicts(shipment_header, shipment_data)
    replenishment_rows = rows_as_dicts(replenishment_header, replenishment_data)
    if len(shipment_rows) != EXPECTED_SHIPMENT_COUNT:
        raise RuleValidationError(
            "shipment_count", f"Expected {EXPECTED_SHIPMENT_COUNT} Shipments; found {len(shipment_rows)}."
        )
    if len(replenishment_rows) != EXPECTED_REPLENISHMENT_COUNT:
        raise RuleValidationError(
            "replenishment_count",
            f"Expected {EXPECTED_REPLENISHMENT_COUNT} Replenishments; found {len(replenishment_rows)}.",
        )
    validate_unique(shipment_rows, "shipment_id", "Shipment source")
    validate_unique(replenishment_rows, "replenishment_id", "Replenishment source")

    shipments, replenishments = normalize_parents(shipment_rows, replenishment_rows)
    known_received = sum(
        parent["received_quantity"] is not None for parent in shipments.values()
    )
    unknown_received = len(shipments) - known_received
    known_approved = sum(
        parent["approved_quantity"] is not None for parent in replenishments.values()
    )
    unknown_approved = len(replenishments) - known_approved
    profile = (
        known_received,
        unknown_received,
        known_approved,
        unknown_approved,
    )
    expected_profile = (
        EXPECTED_KNOWN_RECEIVED,
        EXPECTED_UNKNOWN_RECEIVED,
        EXPECTED_KNOWN_APPROVED,
        EXPECTED_UNKNOWN_APPROVED,
    )
    if profile != expected_profile:
        raise RuleValidationError(
            "profile_drift", f"Governing-quantity profile changed: expected {expected_profile}; found {profile}."
        )

    scenario_rows = run_scenarios(shipments, replenishments)
    failed_scenarios = [row for row in scenario_rows if row[-1] != "PASS"]
    if failed_scenarios:
        details = ", ".join(row[0] for row in failed_scenarios)
        raise RuleValidationError("scenario_failure", f"Controlled scenarios failed: {details}.")

    report_header = [
        "scenario_id",
        "scenario_name",
        "expected_result",
        "actual_result",
        "validation_outcome",
    ]
    report_bytes = csv_bytes(report_header, scenario_rows)
    report_path = output_directory / "shipment-replenishment-allocation-rule-validation.csv"
    write_atomic(report_path, report_bytes)
    generated_bytes, generated_text = decode_strict_utf8(report_path, "Generated scenario report")
    generated_header, generated_rows = parse_csv(generated_text, "Generated scenario report")
    if generated_header != report_header or generated_rows != scenario_rows:
        raise RuleValidationError("output_drift", "Generated scenario report changed after writing.")

    final_hashes = {
        "shipment": sha256_hex(args.shipment_source.read_bytes()),
        "replenishment": sha256_hex(args.replenishment_source.read_bytes()),
        "rules": sha256_hex(args.rules.read_bytes()),
    }
    if final_hashes != initial_hashes:
        raise RuleValidationError("input_changed", "A governed input changed during validation.")

    expected_blocked = sum(row[2] != "PASS" for row in scenario_rows)
    print(PASS_MESSAGE)
    print(f"Shipment source: {args.shipment_source}")
    print(f"Replenishment source: {args.replenishment_source}")
    print(f"Rule artifact: {args.rules}")
    print(f"Generated scenario report: {report_path}")
    print(f"Shipments profiled: {len(shipments)}")
    print(f"Replenishments profiled: {len(replenishments)}")
    print(f"Known Shipment received quantities: {known_received}")
    print(f"Unknown Shipment received quantities: {unknown_received}")
    print(f"Known Replenishment approved quantities: {known_approved}")
    print(f"Unknown Replenishment approved quantities: {unknown_approved}")
    print(f"Controlled rule scenarios: {len(scenario_rows)}")
    print(f"Expected blocked scenarios: {expected_blocked}")
    print("Unexpected scenario outcomes: 0")
    print("Operational allocation records created: 0")
    print("Approved timing rules retained: PASS")
    print("Approved aggregate ceilings retained: PASS")
    print("Planning values excluded as ceilings: PASS")
    print("Status substitution prohibited: PASS")
    print("Parent quantity reductions validated: PASS")
    print("Generated output strict UTF-8 without BOM: PASS")
    print("All governed inputs unchanged: PASS")
    print(f"Shipment Source SHA-256: {initial_hashes['shipment']}")
    print(f"Replenishment Source SHA-256: {initial_hashes['replenishment']}")
    print(f"Decision Rules SHA-256: {initial_hashes['rules']}")
    print(f"Scenario Report SHA-256: {sha256_hex(generated_bytes)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuleValidationError as exc:
        print(f"SHIPMENT REPLENISHMENT ALLOCATION RULE VALIDATION: FAIL [{exc.code}]", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
