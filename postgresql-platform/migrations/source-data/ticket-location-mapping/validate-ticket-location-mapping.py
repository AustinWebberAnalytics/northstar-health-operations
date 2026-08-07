#!/usr/bin/env python3
"""Validate and apply the approved Ticket Location mappings."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path


PASS_MESSAGE = "TICKET LOCATION MAPPING VALIDATION: PASS"
MAPPING_HEADERS = ["requesting_location", "location_id"]
APPROVED_MAPPINGS = {
    "Cary Distribution Hub 01": "LOC-CARY-HUB-01",
    "Durham Outpatient Clinic 07": "LOC-DURHAM-07",
    "Raleigh Specialty Clinic 03": "LOC-RALEIGH-03",
    "Wake Forest Clinic 11": "LOC-WAKEFOREST-11",
}
LOCATION_ID_PATTERN = re.compile(r"^LOC-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{2}$")


class MappingValidationError(RuntimeError):
    """Raised when a governed Ticket Location mapping invariant fails."""


def sha256_hex(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def decode_strict_utf8(path: Path, label: str) -> tuple[bytes, str]:
    if not path.is_file():
        raise MappingValidationError(f"{label} not found: {path}")

    content = path.read_bytes()
    if content.startswith(b"\xef\xbb\xbf"):
        raise MappingValidationError(f"{label} must be UTF-8 without a BOM.")

    try:
        text = content.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise MappingValidationError(
            f"{label} failed strict UTF-8 decoding: {exc}"
        ) from exc

    return content, text


def parse_csv(text: str, label: str) -> tuple[list[str], list[list[str]]]:
    try:
        rows = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as exc:
        raise MappingValidationError(f"{label} is not valid CSV: {exc}") from exc

    if not rows:
        raise MappingValidationError(f"{label} contains no CSV rows.")

    header = rows[0]
    if not header or any(not field for field in header):
        raise MappingValidationError(f"{label} contains an empty header field.")

    if len(set(header)) != len(header):
        raise MappingValidationError(f"{label} contains duplicate header fields.")

    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(header):
            raise MappingValidationError(
                f"{label} row {row_number} contains {len(row)} columns; "
                f"expected {len(header)}."
            )

    return header, rows[1:]


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
        / "postgresql-platform/migration-output/ticket-source-encoding/"
        "tickets-v1-utf8.csv"
    )
    mapping = Path(__file__).resolve().parent / "ticket-location-mapping.csv"
    location_evidence = (
        repository_root
        / "inventory-operations/datasets/data/location-inventory.csv"
    )
    output_directory = repository_root / "postgresql-platform/migration-output"
    output = (
        output_directory
        / "ticket-location-mapping/tickets-v1-location-mapped.csv"
    )
    return source, mapping, location_evidence, output, output_directory


def parse_arguments() -> argparse.Namespace:
    source, mapping, location_evidence, output, _ = default_paths()
    parser = argparse.ArgumentParser(
        description=(
            "Validate the approved Ticket requesting_location-to-location_id "
            "mappings and generate a traceable mapped migration input."
        )
    )
    parser.add_argument("--source", type=Path, default=source)
    parser.add_argument("--mapping", type=Path, default=mapping)
    parser.add_argument("--location-evidence", type=Path, default=location_evidence)
    parser.add_argument("--output", type=Path, default=output)
    return parser.parse_args()


def write_exception_report(
    exceptions: list[tuple[str, int, str]], exception_path: Path
) -> None:
    exception_path.parent.mkdir(parents=True, exist_ok=True)
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(["requesting_location", "occurrence_count", "exception_reason"])
    writer.writerows(exceptions)
    exception_path.write_bytes(buffer.getvalue().encode("utf-8"))


def validate_and_map(
    source: Path, mapping: Path, location_evidence: Path, output: Path
) -> dict[str, object]:
    _, _, _, _, governed_output_directory = default_paths()
    source = source.expanduser().resolve()
    mapping = mapping.expanduser().resolve()
    location_evidence = location_evidence.expanduser().resolve()
    output = output.expanduser().resolve()
    governed_output_directory = governed_output_directory.resolve()

    if not path_is_within(output, governed_output_directory):
        raise MappingValidationError(
            "Output must remain under the ignored migration-output boundary: "
            f"{governed_output_directory}"
        )

    if output in {source, mapping, location_evidence}:
        raise MappingValidationError("Output must not replace a governed input file.")

    exception_path = output.parent / "ticket-location-mapping-exceptions.csv"
    source_bytes, source_text = decode_strict_utf8(source, "Normalized Ticket source")
    source_sha256 = sha256_hex(source_bytes)
    source_header, source_rows = parse_csv(source_text, "Normalized Ticket source")

    if "requesting_location" not in source_header:
        raise MappingValidationError(
            "Normalized Ticket source is missing requesting_location."
        )

    if "location_id" in source_header:
        raise MappingValidationError(
            "Normalized Ticket source already contains location_id; mapping stopped "
            "to prevent double transformation."
        )

    mapping_bytes, mapping_text = decode_strict_utf8(mapping, "Mapping artifact")
    mapping_header, mapping_rows = parse_csv(mapping_text, "Mapping artifact")
    if mapping_header != MAPPING_HEADERS:
        raise MappingValidationError(
            f"Mapping artifact headers must be exactly: {', '.join(MAPPING_HEADERS)}."
        )

    grouped_mappings: dict[str, list[str]] = defaultdict(list)
    for row_number, row in enumerate(mapping_rows, start=2):
        source_value, location_id = row
        if not source_value or not location_id:
            raise MappingValidationError(
                f"Mapping artifact row {row_number} contains a blank value."
            )
        grouped_mappings[source_value].append(location_id)

    ambiguous = {
        source_value: values
        for source_value, values in grouped_mappings.items()
        if len(set(values)) != 1 or len(values) != 1
    }
    if ambiguous:
        exceptions = [
            (source_value, 0, "ambiguous_mapping")
            for source_value in sorted(ambiguous)
        ]
        write_exception_report(exceptions, exception_path)
        raise MappingValidationError(
            "Ambiguous or duplicate mapping rows were routed to the exception report."
        )

    current_mappings = {
        source_value: values[0] for source_value, values in grouped_mappings.items()
    }
    if current_mappings != APPROVED_MAPPINGS:
        raise MappingValidationError(
            "Mapping artifact does not exactly match the four mappings approved "
            "through Issue #18."
        )

    if len(set(current_mappings.values())) != len(current_mappings):
        raise MappingValidationError(
            "Each approved source value must map to a distinct location_id."
        )

    for location_id in current_mappings.values():
        if not LOCATION_ID_PATTERN.fullmatch(location_id):
            raise MappingValidationError(
                f"Approved mapping contains an invalid location_id: {location_id}"
            )

    _, location_text = decode_strict_utf8(
        location_evidence, "Governed Location identifier evidence"
    )
    evidence_header, evidence_rows = parse_csv(
        location_text, "Governed Location identifier evidence"
    )
    if "location_id" not in evidence_header:
        raise MappingValidationError(
            "Governed Location identifier evidence is missing location_id."
        )

    evidence_index = evidence_header.index("location_id")
    governed_location_ids = {
        row[evidence_index] for row in evidence_rows if row[evidence_index]
    }
    ungoverned_ids = set(current_mappings.values()) - governed_location_ids
    if ungoverned_ids:
        raise MappingValidationError(
            "Mapping artifact contains location_id values absent from the governed "
            f"operational evidence: {', '.join(sorted(ungoverned_ids))}"
        )

    location_index = source_header.index("requesting_location")
    source_counts = Counter(row[location_index] for row in source_rows)
    unmatched_values = sorted(set(source_counts) - set(current_mappings))
    inactive_mappings = sorted(set(current_mappings) - set(source_counts))

    exceptions = [
        (value, source_counts[value], "unmatched_source_value")
        for value in unmatched_values
    ]
    if exceptions:
        write_exception_report(exceptions, exception_path)
        raise MappingValidationError(
            "Unmatched Ticket Location values were routed to the exception report."
        )

    if inactive_mappings:
        raise MappingValidationError(
            "Approved mapping artifact contains values not present in the current "
            f"Ticket source: {', '.join(inactive_mappings)}"
        )

    output_header = source_header.copy()
    output_header.insert(location_index + 1, "location_id")
    output_rows: list[list[str]] = []
    for row in source_rows:
        mapped_row = row.copy()
        mapped_row.insert(location_index + 1, current_mappings[row[location_index]])
        output_rows.append(mapped_row)

    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(output_header)
    writer.writerows(output_rows)
    output_bytes = buffer.getvalue().encode("utf-8")
    if output_bytes.startswith(b"\xef\xbb\xbf"):
        raise MappingValidationError("Generated mapped output contains a UTF-8 BOM.")

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=output.parent,
            prefix=f".{output.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(output_bytes)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        generated_bytes, generated_text = decode_strict_utf8(
            temporary_path, "Generated mapped output"
        )
        generated_header, generated_rows = parse_csv(
            generated_text, "Generated mapped output"
        )
        if generated_header != output_header or generated_rows != output_rows:
            raise MappingValidationError(
                "Generated mapped output changed before atomic placement."
            )

        for source_row, generated_row in zip(source_rows, generated_rows, strict=True):
            reconstructed = generated_row.copy()
            reconstructed.pop(location_index + 1)
            if reconstructed != source_row:
                raise MappingValidationError(
                    "A source field changed while location_id was added."
                )

        if sha256_hex(source.read_bytes()) != source_sha256:
            raise MappingValidationError(
                "Normalized Ticket source changed during mapping validation."
            )

        os.replace(temporary_path, output)
        temporary_path = None
        exception_path.unlink(missing_ok=True)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    final_bytes, final_text = decode_strict_utf8(output, "Final mapped output")
    final_header, final_rows = parse_csv(final_text, "Final mapped output")
    if final_header != output_header or final_rows != output_rows:
        raise MappingValidationError("Final mapped output changed after placement.")

    if sha256_hex(source.read_bytes()) != source_sha256:
        raise MappingValidationError(
            "Normalized Ticket source changed after mapping validation."
        )

    return {
        "source": source,
        "mapping": mapping,
        "location_evidence": location_evidence,
        "output": output,
        "source_sha256": source_sha256,
        "mapping_sha256": sha256_hex(mapping_bytes),
        "output_sha256": sha256_hex(final_bytes),
        "data_records": len(source_rows),
        "source_columns": len(source_header),
        "output_columns": len(final_header),
        "distinct_source_values": len(source_counts),
        "approved_mappings": len(current_mappings),
        "governed_location_ids": len(governed_location_ids),
    }


def main() -> int:
    arguments = parse_arguments()
    try:
        result = validate_and_map(
            arguments.source,
            arguments.mapping,
            arguments.location_evidence,
            arguments.output,
        )
    except (MappingValidationError, OSError) as exc:
        print("TICKET LOCATION MAPPING VALIDATION: FAIL", file=sys.stderr)
        print(f"Reason: {exc}", file=sys.stderr)
        return 1

    print(PASS_MESSAGE)
    print(f"Normalized source: {result['source']}")
    print(f"Mapping artifact: {result['mapping']}")
    print(f"Location identifier evidence: {result['location_evidence']}")
    print(f"Generated output: {result['output']}")
    print(f"Data records: {result['data_records']}")
    print(f"Source columns preserved: {result['source_columns']}")
    print(f"Output columns: {result['output_columns']}")
    print(f"Distinct requesting_location values: {result['distinct_source_values']}")
    print(f"Approved one-to-one mappings: {result['approved_mappings']}")
    print(f"Governed location_id values in evidence: {result['governed_location_ids']}")
    print("Unmatched values: 0")
    print("Ambiguous values: 0")
    print("Original requesting_location retained: PASS")
    print("All original Ticket fields and values preserved: PASS")
    print("Generated output strict UTF-8 without BOM: PASS")
    print("Normalized Ticket source unchanged: PASS")
    print(f"Normalized source SHA-256: {result['source_sha256']}")
    print(f"Mapping artifact SHA-256: {result['mapping_sha256']}")
    print(f"Generated output SHA-256: {result['output_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
