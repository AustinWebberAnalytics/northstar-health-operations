#!/usr/bin/env python3
"""Validate governed Ticket owner reconciliation decisions."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import posixpath
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict
from pathlib import Path


PASS_MESSAGE = "TICKET OWNER RECONCILIATION VALIDATION: PASS"
DECISION_HEADERS = [
    "assigned_owner",
    "employee_id",
    "reconciliation_status",
    "ticket_count",
    "decision_basis",
]
APPROVED_DECISIONS = [
    [
        "Jordan Lee",
        "EMP-008",
        "resolved",
        "3",
        "Exact unique active match in authoritative workforce roster",
    ],
    [
        "Avery Patel",
        "",
        "approved_exception",
        "4",
        "No authoritative workforce roster record",
    ],
    [
        "Marcus Nguyen",
        "",
        "approved_exception",
        "2",
        "No authoritative workforce roster record",
    ],
    [
        "Samantha Ortiz",
        "",
        "approved_exception",
        "3",
        "No authoritative workforce roster record",
    ],
    [
        "Taylor Brooks",
        "",
        "approved_exception",
        "3",
        "No authoritative workforce roster record",
    ],
]
EXPECTED_OWNER_COUNTS = {
    row[0]: int(row[3]) for row in APPROVED_DECISIONS
}
RESOLVED_OWNERS = {"Jordan Lee": "EMP-008"}
EXCEPTION_OWNERS = {
    row[0] for row in APPROVED_DECISIONS if row[2] == "approved_exception"
}
EMPLOYEE_ID_PATTERN = re.compile(r"^EMP-\d{3}$")
CELL_REFERENCE_PATTERN = re.compile(r"^([A-Z]+)(\d+)$")
SPREADSHEET_NAMESPACE = (
    "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
)
OFFICE_RELATIONSHIP_NAMESPACE = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
)
PACKAGE_RELATIONSHIP_NAMESPACE = (
    "http://schemas.openxmlformats.org/package/2006/relationships"
)


class ReconciliationValidationError(RuntimeError):
    """Raised when a governed Ticket owner reconciliation invariant fails."""


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


def column_index(reference: str) -> int:
    match = CELL_REFERENCE_PATTERN.fullmatch(reference)
    if not match:
        raise ReconciliationValidationError(
            f"Authoritative workforce roster contains invalid cell reference: {reference}"
        )

    letters = match.group(1)
    index = 0
    for letter in letters:
        index = index * 26 + (ord(letter) - ord("A") + 1)
    return index - 1


def read_authoritative_roster(path: Path) -> tuple[bytes, list[str], list[list[str]]]:
    if not path.is_file():
        raise ReconciliationValidationError(
            f"Authoritative workforce roster not found: {path}"
        )

    content = path.read_bytes()
    try:
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            workbook_root = ET.fromstring(archive.read("xl/workbook.xml"))
            relationship_root = ET.fromstring(
                archive.read("xl/_rels/workbook.xml.rels")
            )

            first_sheet = workbook_root.find(
                f".//{{{SPREADSHEET_NAMESPACE}}}sheet"
            )
            if first_sheet is None:
                raise ReconciliationValidationError(
                    "Authoritative workforce roster contains no worksheet."
                )

            relationship_id = first_sheet.attrib.get(
                f"{{{OFFICE_RELATIONSHIP_NAMESPACE}}}id"
            )
            if not relationship_id:
                raise ReconciliationValidationError(
                    "Authoritative workforce roster worksheet has no relationship."
                )

            sheet_target = None
            for relationship in relationship_root.findall(
                f"{{{PACKAGE_RELATIONSHIP_NAMESPACE}}}Relationship"
            ):
                if relationship.attrib.get("Id") == relationship_id:
                    sheet_target = relationship.attrib.get("Target")
                    break

            if not sheet_target:
                raise ReconciliationValidationError(
                    "Authoritative workforce roster worksheet target is missing."
                )

            if sheet_target.startswith("/"):
                sheet_path = sheet_target.lstrip("/")
            else:
                sheet_path = posixpath.normpath(
                    posixpath.join("xl", sheet_target)
                )

            shared_strings: list[str] = []
            if "xl/sharedStrings.xml" in archive.namelist():
                shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
                for item in shared_root.findall(
                    f"{{{SPREADSHEET_NAMESPACE}}}si"
                ):
                    shared_strings.append(
                        "".join(
                            element.text or ""
                            for element in item.iter(
                                f"{{{SPREADSHEET_NAMESPACE}}}t"
                            )
                        )
                    )

            sheet_root = ET.fromstring(archive.read(sheet_path))
    except (zipfile.BadZipFile, KeyError, ET.ParseError) as exc:
        raise ReconciliationValidationError(
            f"Authoritative workforce roster is not a readable XLSX workbook: {exc}"
        ) from exc

    values_by_row: dict[int, dict[int, str]] = defaultdict(dict)
    maximum_column = -1

    for cell in sheet_root.findall(
        f".//{{{SPREADSHEET_NAMESPACE}}}sheetData/"
        f"{{{SPREADSHEET_NAMESPACE}}}row/"
        f"{{{SPREADSHEET_NAMESPACE}}}c"
    ):
        reference = cell.attrib.get("r", "")
        match = CELL_REFERENCE_PATTERN.fullmatch(reference)
        if not match:
            raise ReconciliationValidationError(
                f"Authoritative workforce roster contains invalid cell reference: {reference}"
            )

        row_number = int(match.group(2))
        current_column = column_index(reference)
        maximum_column = max(maximum_column, current_column)
        cell_type = cell.attrib.get("t")
        value_node = cell.find(f"{{{SPREADSHEET_NAMESPACE}}}v")

        if cell_type == "inlineStr":
            inline_node = cell.find(f"{{{SPREADSHEET_NAMESPACE}}}is")
            value = "" if inline_node is None else "".join(
                element.text or ""
                for element in inline_node.iter(
                    f"{{{SPREADSHEET_NAMESPACE}}}t"
                )
            )
        elif value_node is None:
            value = ""
        elif cell_type == "s":
            try:
                value = shared_strings[int(value_node.text or "")]
            except (ValueError, IndexError) as exc:
                raise ReconciliationValidationError(
                    f"Authoritative workforce roster contains an invalid shared string at {reference}."
                ) from exc
        elif cell_type == "b":
            value = "TRUE" if value_node.text == "1" else "FALSE"
        else:
            value = value_node.text or ""

        values_by_row[row_number][current_column] = value

    if not values_by_row or maximum_column < 0:
        raise ReconciliationValidationError(
            "Authoritative workforce roster contains no cell data."
        )

    rows = [
        [
            values_by_row[row_number].get(current_column, "")
            for current_column in range(maximum_column + 1)
        ]
        for row_number in sorted(values_by_row)
    ]
    header = rows[0]
    data_rows = rows[1:]

    if len(set(header)) != len(header):
        raise ReconciliationValidationError(
            "Authoritative workforce roster contains duplicate headers."
        )

    return content, header, data_rows


def path_is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
    except ValueError:
        return False
    return True


def default_paths() -> tuple[Path, Path, Path, Path, Path]:
    repository_root = Path(__file__).resolve().parents[4]
    source = (
        repository_root
        / "postgresql-platform/migration-output/ticket-location-mapping/"
        "tickets-v1-location-mapped.csv"
    )
    decision = Path(__file__).resolve().parent / "ticket-owner-reconciliation.csv"
    roster = (
        repository_root
        / "workforce-coordination/datasets/data/workforce-roster.xlsx"
    )
    output_directory = repository_root / "postgresql-platform/migration-output"
    output = (
        output_directory
        / "ticket-owner-reconciliation/tickets-v1-owner-reconciled.csv"
    )
    return source, decision, roster, output, output_directory


def parse_arguments() -> argparse.Namespace:
    source, decision, roster, output, _ = default_paths()
    parser = argparse.ArgumentParser(
        description=(
            "Validate approved Ticket owner reconciliation decisions, add governed "
            "employee_id values where authoritative matches exist, and generate "
            "per-Ticket exception reporting for unresolved owners."
        )
    )
    parser.add_argument("--source", type=Path, default=source)
    parser.add_argument("--decision", type=Path, default=decision)
    parser.add_argument("--roster", type=Path, default=roster)
    parser.add_argument("--output", type=Path, default=output)
    return parser.parse_args()


def csv_bytes(header: list[str], rows: list[list[str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


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


def validate_and_reconcile(
    source: Path,
    decision: Path,
    roster: Path,
    output: Path,
) -> dict[str, object]:
    _, _, _, _, governed_output_directory = default_paths()
    source = source.expanduser().resolve()
    decision = decision.expanduser().resolve()
    roster = roster.expanduser().resolve()
    output = output.expanduser().resolve()
    governed_output_directory = governed_output_directory.resolve()

    if not path_is_within(output, governed_output_directory):
        raise ReconciliationValidationError(
            "Output must remain under the ignored migration-output boundary: "
            f"{governed_output_directory}"
        )

    if output in {source, decision, roster}:
        raise ReconciliationValidationError(
            "Output must not replace a governed input file."
        )

    exception_path = (
        output.parent / "ticket-owner-reconciliation-exceptions.csv"
    )
    output.unlink(missing_ok=True)
    exception_path.unlink(missing_ok=True)

    source_bytes, source_text = decode_strict_utf8(
        source, "Issue #18 Ticket Location mapped source"
    )
    source_sha256 = sha256_hex(source_bytes)
    source_header, source_rows = parse_csv(
        source_text, "Issue #18 Ticket Location mapped source"
    )

    required_source_fields = {"ticket_id", "assigned_owner", "location_id"}
    missing_source_fields = required_source_fields - set(source_header)
    if missing_source_fields:
        raise ReconciliationValidationError(
            "Issue #18 Ticket Location mapped source is missing required fields: "
            f"{', '.join(sorted(missing_source_fields))}"
        )

    if "employee_id" in source_header:
        raise ReconciliationValidationError(
            "Issue #18 Ticket Location mapped source already contains employee_id; "
            "reconciliation stopped to prevent double transformation."
        )

    decision_bytes, decision_text = decode_strict_utf8(
        decision, "Reconciliation decision artifact"
    )
    decision_header, decision_rows = parse_csv(
        decision_text, "Reconciliation decision artifact"
    )
    if decision_header != DECISION_HEADERS:
        raise ReconciliationValidationError(
            "Reconciliation decision artifact headers must be exactly: "
            f"{', '.join(DECISION_HEADERS)}."
        )
    if decision_rows != APPROVED_DECISIONS:
        raise ReconciliationValidationError(
            "Reconciliation decision artifact does not exactly match the "
            "Issue #19 decisions approved on August 7, 2026."
        )

    roster_bytes, roster_header, roster_rows = read_authoritative_roster(roster)
    roster_sha256 = sha256_hex(roster_bytes)
    required_roster_fields = {"employee_id", "employee_name", "active_flag"}
    missing_roster_fields = required_roster_fields - set(roster_header)
    if missing_roster_fields:
        raise ReconciliationValidationError(
            "Authoritative workforce roster is missing required fields: "
            f"{', '.join(sorted(missing_roster_fields))}"
        )

    employee_id_index = roster_header.index("employee_id")
    employee_name_index = roster_header.index("employee_name")
    active_flag_index = roster_header.index("active_flag")
    roster_by_name: dict[str, list[tuple[str, str]]] = defaultdict(list)
    roster_ids: list[str] = []

    for row_number, row in enumerate(roster_rows, start=2):
        employee_id = row[employee_id_index]
        employee_name = row[employee_name_index]
        active_flag = row[active_flag_index]

        if not employee_id or not EMPLOYEE_ID_PATTERN.fullmatch(employee_id):
            raise ReconciliationValidationError(
                f"Authoritative workforce roster row {row_number} contains an "
                f"invalid employee_id: {employee_id}"
            )
        if not employee_name:
            raise ReconciliationValidationError(
                f"Authoritative workforce roster row {row_number} contains a blank employee_name."
            )

        roster_ids.append(employee_id)
        roster_by_name[employee_name].append((employee_id, active_flag))

    duplicate_ids = sorted(
        employee_id
        for employee_id, count in Counter(roster_ids).items()
        if count != 1
    )
    if duplicate_ids:
        raise ReconciliationValidationError(
            "Authoritative workforce roster contains duplicate employee_id values: "
            f"{', '.join(duplicate_ids)}"
        )

    resolved_record = roster_by_name.get("Jordan Lee", [])
    if resolved_record != [("EMP-008", "TRUE")]:
        raise ReconciliationValidationError(
            "Jordan Lee must resolve uniquely to active roster record EMP-008."
        )

    roster_exception_matches = sorted(
        owner for owner in EXCEPTION_OWNERS if owner in roster_by_name
    )
    if roster_exception_matches:
        raise ReconciliationValidationError(
            "Approved exception owners now match the authoritative roster and "
            "require governance review: "
            f"{', '.join(roster_exception_matches)}"
        )

    owner_index = source_header.index("assigned_owner")
    ticket_id_index = source_header.index("ticket_id")
    owner_counts = Counter(row[owner_index] for row in source_rows)
    if dict(owner_counts) != EXPECTED_OWNER_COUNTS:
        unexpected = sorted(set(owner_counts) - set(EXPECTED_OWNER_COUNTS))
        missing = sorted(set(EXPECTED_OWNER_COUNTS) - set(owner_counts))
        details = []
        if unexpected:
            details.append(f"unapproved owners: {', '.join(unexpected)}")
        if missing:
            details.append(f"missing approved owners: {', '.join(missing)}")
        count_changes = sorted(
            owner
            for owner in set(owner_counts) & set(EXPECTED_OWNER_COUNTS)
            if owner_counts[owner] != EXPECTED_OWNER_COUNTS[owner]
        )
        if count_changes:
            details.append(
                "changed Ticket counts: "
                + ", ".join(
                    f"{owner}={owner_counts[owner]} "
                    f"(expected {EXPECTED_OWNER_COUNTS[owner]})"
                    for owner in count_changes
                )
            )
        raise ReconciliationValidationError(
            "Ticket owner profile differs from the approved Issue #19 boundary"
            + (f" ({'; '.join(details)})" if details else "")
            + "."
        )

    output_header = source_header.copy()
    output_header.insert(owner_index + 1, "employee_id")
    output_rows: list[list[str]] = []
    exception_rows: list[list[str]] = []
    resolved_ticket_count = 0

    for row in source_rows:
        assigned_owner = row[owner_index]
        employee_id = RESOLVED_OWNERS.get(assigned_owner, "")
        reconciled_row = row.copy()
        reconciled_row.insert(owner_index + 1, employee_id)
        output_rows.append(reconciled_row)

        if employee_id:
            resolved_ticket_count += 1
        else:
            exception_rows.append(
                [
                    row[ticket_id_index],
                    assigned_owner,
                    "no_authoritative_employee_record",
                ]
            )

    if resolved_ticket_count != 3 or len(exception_rows) != 12:
        raise ReconciliationValidationError(
            "Reconciliation result must contain three resolved Ticket records "
            "and 12 approved exception records."
        )

    output_bytes = csv_bytes(output_header, output_rows)
    exception_header = ["ticket_id", "assigned_owner", "exception_reason"]
    exception_bytes = csv_bytes(exception_header, exception_rows)
    if output_bytes.startswith(b"\xef\xbb\xbf") or exception_bytes.startswith(
        b"\xef\xbb\xbf"
    ):
        raise ReconciliationValidationError(
            "Generated reconciliation output must be UTF-8 without a BOM."
        )

    write_atomic(output, output_bytes)
    write_atomic(exception_path, exception_bytes)

    final_output_bytes, final_output_text = decode_strict_utf8(
        output, "Final reconciled Ticket output"
    )
    final_header, final_rows = parse_csv(
        final_output_text, "Final reconciled Ticket output"
    )
    if final_header != output_header or final_rows != output_rows:
        raise ReconciliationValidationError(
            "Final reconciled Ticket output changed after placement."
        )

    final_exception_bytes, final_exception_text = decode_strict_utf8(
        exception_path, "Final Ticket owner exception report"
    )
    final_exception_header, final_exception_rows = parse_csv(
        final_exception_text, "Final Ticket owner exception report"
    )
    if (
        final_exception_header != exception_header
        or final_exception_rows != exception_rows
    ):
        raise ReconciliationValidationError(
            "Final Ticket owner exception report changed after placement."
        )

    for source_row, generated_row in zip(source_rows, final_rows, strict=True):
        reconstructed = generated_row.copy()
        reconstructed.pop(owner_index + 1)
        if reconstructed != source_row:
            raise ReconciliationValidationError(
                "A source field changed while employee_id was added."
            )

    if sha256_hex(source.read_bytes()) != source_sha256:
        raise ReconciliationValidationError(
            "Issue #18 Ticket Location mapped source changed during reconciliation."
        )
    if sha256_hex(roster.read_bytes()) != roster_sha256:
        raise ReconciliationValidationError(
            "Authoritative workforce roster changed during reconciliation."
        )

    return {
        "source": source,
        "decision": decision,
        "roster": roster,
        "output": output,
        "exception_report": exception_path,
        "source_sha256": source_sha256,
        "decision_sha256": sha256_hex(decision_bytes),
        "roster_sha256": roster_sha256,
        "output_sha256": sha256_hex(final_output_bytes),
        "exception_sha256": sha256_hex(final_exception_bytes),
        "data_records": len(source_rows),
        "source_columns": len(source_header),
        "output_columns": len(final_header),
        "distinct_owners": len(owner_counts),
        "roster_records": len(roster_rows),
        "resolved_owners": len(RESOLVED_OWNERS),
        "resolved_tickets": resolved_ticket_count,
        "exception_owners": len(EXCEPTION_OWNERS),
        "exception_tickets": len(exception_rows),
    }


def main() -> int:
    arguments = parse_arguments()
    try:
        result = validate_and_reconcile(
            arguments.source,
            arguments.decision,
            arguments.roster,
            arguments.output,
        )
    except (ReconciliationValidationError, OSError) as exc:
        print("TICKET OWNER RECONCILIATION VALIDATION: FAIL", file=sys.stderr)
        print(f"Reason: {exc}", file=sys.stderr)
        return 1

    print(PASS_MESSAGE)
    print(f"Issue #18 mapped source: {result['source']}")
    print(f"Decision artifact: {result['decision']}")
    print(f"Authoritative workforce roster: {result['roster']}")
    print(f"Generated reconciled output: {result['output']}")
    print(f"Generated exception report: {result['exception_report']}")
    print(f"Data records: {result['data_records']}")
    print(f"Source columns preserved: {result['source_columns']}")
    print(f"Output columns: {result['output_columns']}")
    print(f"Distinct assigned_owner values: {result['distinct_owners']}")
    print(f"Authoritative workforce records: {result['roster_records']}")
    print(f"Resolved owner relationships: {result['resolved_owners']}")
    print(f"Resolved Ticket records: {result['resolved_tickets']}")
    print(f"Approved exception owners: {result['exception_owners']}")
    print(f"Exception Ticket records: {result['exception_tickets']}")
    print("Unapproved owner values: 0")
    print("Ambiguous roster matches: 0")
    print("Original assigned_owner retained: PASS")
    print("All original Ticket fields and values preserved: PASS")
    print("Generated outputs strict UTF-8 without BOM: PASS")
    print("Issue #18 mapped source unchanged: PASS")
    print("Authoritative workforce roster unchanged: PASS")
    print(f"Mapped source SHA-256: {result['source_sha256']}")
    print(f"Decision artifact SHA-256: {result['decision_sha256']}")
    print(f"Workforce roster SHA-256: {result['roster_sha256']}")
    print(f"Generated output SHA-256: {result['output_sha256']}")
    print(f"Exception report SHA-256: {result['exception_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

