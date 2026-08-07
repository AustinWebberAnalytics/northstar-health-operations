#!/usr/bin/env python3
"""Validate governed orphaned Ticket-reference reconciliation decisions."""

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


PASS_MESSAGE = "TICKET REFERENCE RECONCILIATION VALIDATION: PASS"
DECISION_HEADERS = [
    "record_type",
    "source_dataset",
    "source_record_id",
    "source_related_ticket_id",
    "canonical_related_ticket_id",
    "reconciliation_status",
    "decision_basis",
]
APPROVED_DECISIONS = [
    [
        "inventory_discrepancy",
        "inventory-operations/datasets/data/inventory-discrepancies.csv",
        "DISC-1005",
        "INC-100018",
        "",
        "approved_exception",
        "No authoritative Ticket record or correction evidence",
    ],
    [
        "shortage_event",
        "inventory-operations/datasets/data/shortage-events.csv",
        "SHORT-1004",
        "INC-100021",
        "",
        "approved_exception",
        "No authoritative Ticket record or correction evidence",
    ],
    [
        "inventory_discrepancy",
        "inventory-operations/datasets/data/inventory-discrepancies.csv",
        "DISC-1004",
        "INC-100031",
        "",
        "approved_exception",
        "No authoritative Ticket record or correction evidence",
    ],
]
DATASET_CONTRACTS = {
    "inventory_discrepancy": {
        "path": "inventory-operations/datasets/data/inventory-discrepancies.csv",
        "record_id": "discrepancy_id",
        "expected_records": 5,
        "output_name": "inventory-discrepancies-ticket-reconciled.csv",
    },
    "shortage_event": {
        "path": "inventory-operations/datasets/data/shortage-events.csv",
        "record_id": "shortage_id",
        "expected_records": 5,
        "output_name": "shortage-events-ticket-reconciled.csv",
    },
}
EXPECTED_TICKET_COUNT = 15
EXPECTED_ORPHANS = {
    (row[0], row[2], row[3]) for row in APPROVED_DECISIONS
}


class ReconciliationValidationError(RuntimeError):
    """Raised when a governed Ticket-reference invariant fails."""


def sha256_hex(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def decode_strict_utf8(path: Path, label: str) -> tuple[bytes, str]:
    if not path.is_file():
        raise ReconciliationValidationError(f"{label} not found: {path}")

    content = path.read_bytes()
    if content.startswith(b"\xef\xbb\xbf"):
        raise ReconciliationValidationError(f"{label} must be UTF-8 without a BOM.")

    try:
        text = content.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ReconciliationValidationError(
            f"{label} failed strict UTF-8 decoding: {exc}"
        ) from exc

    return content, text


def parse_csv(text: str, label: str) -> tuple[list[str], list[list[str]]]:
    try:
        rows = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as exc:
        raise ReconciliationValidationError(
            f"{label} is not valid CSV: {exc}"
        ) from exc

    if not rows:
        raise ReconciliationValidationError(f"{label} contains no CSV rows.")

    header = rows[0]
    if not header or any(not field for field in header):
        raise ReconciliationValidationError(
            f"{label} contains an empty header field."
        )
    if len(set(header)) != len(header):
        raise ReconciliationValidationError(
            f"{label} contains duplicate header fields."
        )

    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(header):
            raise ReconciliationValidationError(
                f"{label} row {row_number} contains {len(row)} columns; "
                f"expected {len(header)}."
            )

    return header, rows[1:]


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
    ticket_source = (
        repository_root
        / "postgresql-platform/migration-output/ticket-owner-reconciliation/"
        "tickets-v1-owner-reconciled.csv"
    )
    inventory_discrepancies = (
        repository_root
        / "inventory-operations/datasets/data/inventory-discrepancies.csv"
    )
    shortage_events = (
        repository_root / "inventory-operations/datasets/data/shortage-events.csv"
    )
    decision = Path(__file__).resolve().parent / "ticket-reference-reconciliation.csv"
    output_directory = (
        repository_root
        / "postgresql-platform/migration-output/ticket-reference-reconciliation"
    )
    return (
        ticket_source,
        inventory_discrepancies,
        shortage_events,
        decision,
        output_directory,
    )


def parse_arguments() -> argparse.Namespace:
    ticket_source, inventory, shortage, decision, output_directory = default_paths()
    parser = argparse.ArgumentParser(
        description=(
            "Validate the three approved orphaned Ticket-reference exceptions, "
            "preserve their source identifiers, and generate canonical nullable "
            "relationship outputs plus visible exception reporting."
        )
    )
    parser.add_argument("--ticket-source", type=Path, default=ticket_source)
    parser.add_argument("--inventory-discrepancies", type=Path, default=inventory)
    parser.add_argument("--shortage-events", type=Path, default=shortage)
    parser.add_argument("--decision", type=Path, default=decision)
    parser.add_argument("--output-directory", type=Path, default=output_directory)
    return parser.parse_args()


def validate_unique_identifiers(
    header: list[str],
    rows: list[list[str]],
    field: str,
    label: str,
) -> None:
    if field not in header:
        raise ReconciliationValidationError(
            f"{label} is missing required field: {field}"
        )
    index = header.index(field)
    identifiers = [row[index] for row in rows]
    blank_count = identifiers.count("")
    if blank_count:
        raise ReconciliationValidationError(
            f"{label} contains {blank_count} blank {field} values."
        )
    duplicates = sorted(
        value for value, count in Counter(identifiers).items() if count != 1
    )
    if duplicates:
        raise ReconciliationValidationError(
            f"{label} contains duplicate {field} values: {', '.join(duplicates)}"
        )


def validate_and_reconcile(
    ticket_source: Path,
    inventory_discrepancies: Path,
    shortage_events: Path,
    decision: Path,
    output_directory: Path,
) -> dict[str, object]:
    repository_root = Path(__file__).resolve().parents[4]
    governed_output_root = (
        repository_root / "postgresql-platform/migration-output"
    ).resolve()
    ticket_source = ticket_source.expanduser().resolve()
    inventory_discrepancies = inventory_discrepancies.expanduser().resolve()
    shortage_events = shortage_events.expanduser().resolve()
    decision = decision.expanduser().resolve()
    output_directory = output_directory.expanduser().resolve()

    if not path_is_within(output_directory, governed_output_root):
        raise ReconciliationValidationError(
            "Output must remain under the ignored migration-output boundary: "
            f"{governed_output_root}"
        )

    source_paths = {
        "ticket_source": ticket_source,
        "inventory_discrepancy": inventory_discrepancies,
        "shortage_event": shortage_events,
        "decision": decision,
    }
    output_paths = {
        record_type: output_directory / str(contract["output_name"])
        for record_type, contract in DATASET_CONTRACTS.items()
    }
    exception_path = output_directory / "ticket-reference-reconciliation-exceptions.csv"
    if (set(output_paths.values()) | {exception_path}) & set(source_paths.values()):
        raise ReconciliationValidationError(
            "Generated output must not replace a governed input file."
        )

    for path in [*output_paths.values(), exception_path]:
        path.unlink(missing_ok=True)

    input_bytes: dict[str, bytes] = {}
    input_hashes: dict[str, str] = {}
    parsed: dict[str, tuple[list[str], list[list[str]]]] = {}
    for key, path in source_paths.items():
        content, text = decode_strict_utf8(path, key.replace("_", " ").title())
        input_bytes[key] = content
        input_hashes[key] = sha256_hex(content)
        parsed[key] = parse_csv(text, key.replace("_", " ").title())

    decision_header, decision_rows = parsed["decision"]
    if decision_header != DECISION_HEADERS:
        raise ReconciliationValidationError(
            "Decision artifact headers must be exactly: "
            f"{', '.join(DECISION_HEADERS)}."
        )
    if decision_rows != APPROVED_DECISIONS:
        raise ReconciliationValidationError(
            "Decision artifact does not exactly match the Issue #20 decisions "
            "approved on August 7, 2026."
        )

    ticket_header, ticket_rows = parsed["ticket_source"]
    validate_unique_identifiers(
        ticket_header, ticket_rows, "ticket_id", "Issue #19 reconciled Ticket source"
    )
    if len(ticket_rows) != EXPECTED_TICKET_COUNT:
        raise ReconciliationValidationError(
            f"Issue #19 reconciled Ticket source contains {len(ticket_rows)} records; "
            f"expected {EXPECTED_TICKET_COUNT}."
        )
    ticket_index = ticket_header.index("ticket_id")
    ticket_ids = {row[ticket_index] for row in ticket_rows}
    approved_source_ticket_ids = {row[3] for row in APPROVED_DECISIONS}
    newly_resolved = sorted(approved_source_ticket_ids & ticket_ids)
    if newly_resolved:
        raise ReconciliationValidationError(
            "An approved exception identifier now exists in the Ticket source and "
            "requires governance review: " + ", ".join(newly_resolved)
        )

    dataset_paths = {
        "inventory_discrepancy": inventory_discrepancies,
        "shortage_event": shortage_events,
    }
    source_records: dict[tuple[str, str], list[str]] = {}
    source_metadata: dict[str, dict[str, object]] = {}
    actual_orphans: set[tuple[str, str, str]] = set()

    for record_type, source_path in dataset_paths.items():
        header, rows = parsed[record_type]
        contract = DATASET_CONTRACTS[record_type]
        record_id_field = str(contract["record_id"])
        required_fields = {record_id_field, "related_ticket_id"}
        missing_fields = required_fields - set(header)
        if missing_fields:
            raise ReconciliationValidationError(
                f"{source_path.name} is missing required fields: "
                f"{', '.join(sorted(missing_fields))}"
            )
        validate_unique_identifiers(header, rows, record_id_field, source_path.name)
        expected_records = int(contract["expected_records"])
        if len(rows) != expected_records:
            raise ReconciliationValidationError(
                f"{source_path.name} contains {len(rows)} records; "
                f"expected {expected_records}."
            )

        record_id_index = header.index(record_id_field)
        related_ticket_index = header.index("related_ticket_id")
        for row in rows:
            record_id = row[record_id_index]
            related_ticket_id = row[related_ticket_index]
            source_records[(record_type, record_id)] = row
            if related_ticket_id and related_ticket_id not in ticket_ids:
                actual_orphans.add((record_type, record_id, related_ticket_id))

        source_metadata[record_type] = {
            "header": header,
            "rows": rows,
            "record_id_index": record_id_index,
            "related_ticket_index": related_ticket_index,
        }

    if actual_orphans != EXPECTED_ORPHANS:
        unexpected = sorted(actual_orphans - EXPECTED_ORPHANS)
        missing = sorted(EXPECTED_ORPHANS - actual_orphans)
        details = []
        if unexpected:
            details.append(f"unapproved orphan references: {unexpected}")
        if missing:
            details.append(f"missing approved orphan references: {missing}")
        raise ReconciliationValidationError(
            "Operational orphan profile differs from the approved Issue #20 boundary"
            + (f" ({'; '.join(details)})" if details else "")
            + "."
        )

    for decision_row in APPROVED_DECISIONS:
        record_type, dataset_path, record_id, source_ticket_id = decision_row[:4]
        contract_path = str(DATASET_CONTRACTS[record_type]["path"])
        if dataset_path != contract_path:
            raise ReconciliationValidationError(
                f"Decision dataset path drift for {record_id}: {dataset_path}"
            )
        source_row = source_records.get((record_type, record_id))
        if source_row is None:
            raise ReconciliationValidationError(
                f"Approved source record not found: {record_id}"
            )
        related_index = int(source_metadata[record_type]["related_ticket_index"])
        if source_row[related_index] != source_ticket_id:
            raise ReconciliationValidationError(
                f"Approved source identifier mismatch for {record_id}: "
                f"{source_row[related_index]}"
            )

    approved_keys = {(row[0], row[2]) for row in APPROVED_DECISIONS}
    output_rows_by_type: dict[str, list[list[str]]] = {}
    output_headers: dict[str, list[str]] = {}
    canonical_nonblank_references: list[str] = []

    for record_type, metadata in source_metadata.items():
        source_header = list(metadata["header"])
        source_rows = list(metadata["rows"])
        record_id_index = int(metadata["record_id_index"])
        related_ticket_index = int(metadata["related_ticket_index"])
        output_header = source_header.copy()
        output_header.insert(related_ticket_index, "source_related_ticket_id")
        output_rows: list[list[str]] = []

        for source_row in source_rows:
            record_id = source_row[record_id_index]
            original_ticket_id = source_row[related_ticket_index]
            canonical_ticket_id = (
                "" if (record_type, record_id) in approved_keys else original_ticket_id
            )
            output_row = source_row.copy()
            output_row.insert(related_ticket_index, original_ticket_id)
            output_row[related_ticket_index + 1] = canonical_ticket_id
            output_rows.append(output_row)
            if canonical_ticket_id:
                canonical_nonblank_references.append(canonical_ticket_id)

        output_headers[record_type] = output_header
        output_rows_by_type[record_type] = output_rows
        write_atomic(output_paths[record_type], csv_bytes(output_header, output_rows))

    unresolved_canonical = sorted(
        reference
        for reference in canonical_nonblank_references
        if reference not in ticket_ids
    )
    if unresolved_canonical:
        raise ReconciliationValidationError(
            "Generated canonical output contains unresolved nonblank Ticket references: "
            + ", ".join(unresolved_canonical)
        )

    exception_header = [
        "record_type",
        "source_dataset",
        "source_record_id",
        "source_related_ticket_id",
        "canonical_related_ticket_id",
        "reconciliation_status",
        "exception_reason",
    ]
    exception_rows = [
        [row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
        for row in APPROVED_DECISIONS
    ]
    write_atomic(exception_path, csv_bytes(exception_header, exception_rows))

    final_output_hashes: dict[str, str] = {}
    for record_type, path in output_paths.items():
        final_bytes, final_text = decode_strict_utf8(
            path, f"Generated {record_type} reconciliation output"
        )
        final_header, final_rows = parse_csv(
            final_text, f"Generated {record_type} reconciliation output"
        )
        if (
            final_header != output_headers[record_type]
            or final_rows != output_rows_by_type[record_type]
        ):
            raise ReconciliationValidationError(
                f"Generated {record_type} reconciliation output changed after placement."
            )

        source_header, source_rows = parsed[record_type]
        related_ticket_index = source_header.index("related_ticket_id")
        for source_row, generated_row in zip(source_rows, final_rows, strict=True):
            reconstructed = generated_row.copy()
            original_ticket_id = reconstructed.pop(related_ticket_index)
            reconstructed[related_ticket_index] = original_ticket_id
            if reconstructed != source_row:
                raise ReconciliationValidationError(
                    f"A source value changed in {record_type} reconciliation output."
                )
        final_output_hashes[record_type] = sha256_hex(final_bytes)

    exception_bytes, exception_text = decode_strict_utf8(
        exception_path, "Generated Ticket-reference exception report"
    )
    final_exception_header, final_exception_rows = parse_csv(
        exception_text, "Generated Ticket-reference exception report"
    )
    if (
        final_exception_header != exception_header
        or final_exception_rows != exception_rows
    ):
        raise ReconciliationValidationError(
            "Generated Ticket-reference exception report changed after placement."
        )

    for key, path in source_paths.items():
        if sha256_hex(path.read_bytes()) != input_hashes[key]:
            raise ReconciliationValidationError(
                f"Governed input changed during reconciliation: {path}"
            )

    return {
        "ticket_source": ticket_source,
        "inventory_source": inventory_discrepancies,
        "shortage_source": shortage_events,
        "decision": decision,
        "inventory_output": output_paths["inventory_discrepancy"],
        "shortage_output": output_paths["shortage_event"],
        "exception_report": exception_path,
        "ticket_records": len(ticket_rows),
        "inventory_records": len(parsed["inventory_discrepancy"][1]),
        "shortage_records": len(parsed["shortage_event"][1]),
        "exception_records": len(exception_rows),
        "resolved_nonblank_references": len(canonical_nonblank_references),
        "input_hashes": input_hashes,
        "output_hashes": final_output_hashes,
        "exception_hash": sha256_hex(exception_bytes),
    }


def main() -> int:
    arguments = parse_arguments()
    try:
        result = validate_and_reconcile(
            arguments.ticket_source,
            arguments.inventory_discrepancies,
            arguments.shortage_events,
            arguments.decision,
            arguments.output_directory,
        )
    except (ReconciliationValidationError, OSError) as exc:
        print("TICKET REFERENCE RECONCILIATION VALIDATION: FAIL", file=sys.stderr)
        print(f"Reason: {exc}", file=sys.stderr)
        return 1

    print(PASS_MESSAGE)
    print(f"Issue #19 reconciled Ticket source: {result['ticket_source']}")
    print(f"Inventory Discrepancy source: {result['inventory_source']}")
    print(f"Shortage source: {result['shortage_source']}")
    print(f"Decision artifact: {result['decision']}")
    print(f"Generated Inventory Discrepancy output: {result['inventory_output']}")
    print(f"Generated Shortage output: {result['shortage_output']}")
    print(f"Generated exception report: {result['exception_report']}")
    print(f"Ticket records: {result['ticket_records']}")
    print(f"Inventory Discrepancy records preserved: {result['inventory_records']}")
    print(f"Shortage records preserved: {result['shortage_records']}")
    print(f"Approved visible exceptions: {result['exception_records']}")
    print(
        "Resolved nonblank canonical Ticket references: "
        f"{result['resolved_nonblank_references']}"
    )
    print("Unapproved orphan references: 0")
    print("Invented or substituted Ticket identifiers: 0")
    print("Original related_ticket_id values retained: PASS")
    print("Canonical exception relationships nullable: PASS")
    print("All operational records and source values reconstructable: PASS")
    print("All nonblank canonical Ticket references resolve: PASS")
    print("Generated outputs strict UTF-8 without BOM: PASS")
    print("All governed inputs unchanged: PASS")
    for key, digest in result["input_hashes"].items():
        print(f"{key.replace('_', ' ').title()} SHA-256: {digest}")
    for key, digest in result["output_hashes"].items():
        print(f"{key.replace('_', ' ').title()} output SHA-256: {digest}")
    print(f"Exception report SHA-256: {result['exception_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
