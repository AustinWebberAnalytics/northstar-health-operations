#!/usr/bin/env python3
"""Normalize the governed Ticket source from Windows-1252 to UTF-8."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import sys
import tempfile
from pathlib import Path


PASS_MESSAGE = "TICKET SOURCE ENCODING NORMALIZATION: PASS"


class NormalizationError(RuntimeError):
    """Raised when a governed normalization invariant fails."""


def sha256_hex(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def parse_csv(text: str, label: str) -> list[list[str]]:
    try:
        rows = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as exc:
        raise NormalizationError(f"{label} is not valid CSV: {exc}") from exc

    if not rows:
        raise NormalizationError(f"{label} contains no CSV rows.")

    if len(rows) == 1:
        raise NormalizationError(f"{label} contains a header but no data records.")

    column_count = len(rows[0])
    if column_count == 0:
        raise NormalizationError(f"{label} contains an empty header row.")

    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) != column_count:
            raise NormalizationError(
                f"{label} row {row_number} contains {len(row)} columns; "
                f"expected {column_count}."
            )

    return rows


def path_is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
    except ValueError:
        return False
    return True


def default_paths() -> tuple[Path, Path, Path]:
    repository_root = Path(__file__).resolve().parents[4]
    source = repository_root / "ticketing-system/datasets/data/tickets-v1.csv"
    output_directory = repository_root / "postgresql-platform/migration-output"
    output = output_directory / "ticket-source-encoding/tickets-v1-utf8.csv"
    return source, output, output_directory


def parse_arguments() -> argparse.Namespace:
    default_source, default_output, _ = default_paths()
    parser = argparse.ArgumentParser(
        description=(
            "Convert the governed Ticket CSV from Windows-1252 to UTF-8 without "
            "changing its decoded text or parsed CSV values."
        )
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=default_source,
        help=f"Windows-1252 source CSV (default: {default_source})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_output,
        help=f"Generated UTF-8 CSV (default: {default_output})",
    )
    return parser.parse_args()


def normalize(source: Path, output: Path) -> dict[str, object]:
    _, _, governed_output_directory = default_paths()
    source = source.expanduser().resolve()
    output = output.expanduser().resolve()
    governed_output_directory = governed_output_directory.resolve()

    if not source.is_file():
        raise NormalizationError(f"Source file not found: {source}")

    if source == output:
        raise NormalizationError("Source and output paths must be different.")

    if not path_is_within(output, governed_output_directory):
        raise NormalizationError(
            "Output must remain under the ignored migration-output boundary: "
            f"{governed_output_directory}"
        )

    source_bytes = source.read_bytes()
    source_sha256 = sha256_hex(source_bytes)

    try:
        source_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        pass
    else:
        raise NormalizationError(
            "Source already passes strict UTF-8 decoding. Conversion stopped to "
            "prevent accidental double normalization."
        )

    try:
        source_text = source_bytes.decode("cp1252", errors="strict")
    except UnicodeDecodeError as exc:
        raise NormalizationError(
            f"Source does not decode cleanly as Windows-1252: {exc}"
        ) from exc

    source_rows = parse_csv(source_text, "Source")
    output_bytes = source_text.encode("utf-8", errors="strict")

    if output_bytes.startswith(b"\xef\xbb\xbf"):
        raise NormalizationError("Generated UTF-8 output unexpectedly contains a BOM.")

    output_directory = output.parent
    output_directory.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=output_directory,
            prefix=f".{output.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(output_bytes)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        generated_bytes = temporary_path.read_bytes()
        try:
            generated_text = generated_bytes.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise NormalizationError(
                f"Generated output failed strict UTF-8 decoding: {exc}"
            ) from exc

        if generated_bytes.startswith(b"\xef\xbb\xbf"):
            raise NormalizationError("Generated UTF-8 output contains a BOM.")

        if generated_text != source_text:
            raise NormalizationError(
                "Decoded text changed during Windows-1252 to UTF-8 normalization."
            )

        output_rows = parse_csv(generated_text, "Generated output")
        if output_rows != source_rows:
            raise NormalizationError(
                "Parsed CSV headers, records, or field values changed during normalization."
            )

        if sha256_hex(source.read_bytes()) != source_sha256:
            raise NormalizationError("Authoritative Ticket source changed during normalization.")

        os.replace(temporary_path, output)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    final_output_bytes = output.read_bytes()
    final_output_text = final_output_bytes.decode("utf-8", errors="strict")
    final_output_rows = parse_csv(final_output_text, "Final output")

    if final_output_text != source_text or final_output_rows != source_rows:
        raise NormalizationError("Final output changed after atomic placement.")

    if sha256_hex(source.read_bytes()) != source_sha256:
        raise NormalizationError("Authoritative Ticket source changed after normalization.")

    return {
        "source": source,
        "output": output,
        "source_bytes": len(source_bytes),
        "output_bytes": len(final_output_bytes),
        "source_sha256": source_sha256,
        "output_sha256": sha256_hex(final_output_bytes),
        "columns": len(source_rows[0]),
        "data_records": len(source_rows) - 1,
        "em_dashes": source_text.count("\u2014"),
    }


def main() -> int:
    arguments = parse_arguments()

    try:
        result = normalize(arguments.source, arguments.output)
    except (NormalizationError, OSError) as exc:
        print("TICKET SOURCE ENCODING NORMALIZATION: FAIL", file=sys.stderr)
        print(f"Reason: {exc}", file=sys.stderr)
        return 1

    print(PASS_MESSAGE)
    print(f"Source: {result['source']}")
    print(f"Output: {result['output']}")
    print("Source encoding: Windows-1252")
    print("Output encoding: UTF-8 without BOM")
    print(f"Data records: {result['data_records']}")
    print(f"Columns: {result['columns']}")
    print(f"Em dashes preserved: {result['em_dashes']}")
    print(f"Source bytes: {result['source_bytes']}")
    print(f"Output bytes: {result['output_bytes']}")
    print(f"Source SHA-256: {result['source_sha256']}")
    print(f"Output SHA-256: {result['output_sha256']}")
    print("Strict UTF-8 validation: PASS")
    print("Unicode text equivalence: PASS")
    print("CSV structure and field-value equivalence: PASS")
    print("Authoritative source unchanged: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
