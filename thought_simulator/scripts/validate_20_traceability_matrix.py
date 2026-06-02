#!/usr/bin/env python3
"""Validate the 20.200 traceability matrix for freshness and accuracy.

Checks:
- Matrix file exists and contains a parseable markdown table.
- Every authoritative 20-series requirement file has exactly one row.
- No matrix row references a non-existent 20-series requirement file.
- Verification/design anchor references in each row resolve to existing files.
- Rows are ordered by numeric 20-series document number for deterministic reviews.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REQ_DIR = ROOT / "20_requirements"
MATRIX_PATH = REQ_DIR / "20.200_traceability_matrix.md"

REQ_DOC_RE = re.compile(r"^20\.(\d+)_.*\.md$")


def _parse_matrix_rows(content: str) -> tuple[list[str], list[tuple[str, str, str, str]]]:
    errors: list[str] = []
    table_lines = [line.strip() for line in content.splitlines() if line.strip().startswith("|")]

    if len(table_lines) < 3:
        return ["traceability table not found or malformed in 20.200_traceability_matrix.md"], []

    rows: list[tuple[str, str, str, str]] = []
    for line in table_lines:
        if re.match(r"^\|\s*-+", line):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 4:
            continue
        if cols[0].lower() == "20-series requirement doc":
            continue
        rows.append((cols[0], cols[1], cols[2], cols[3]))

    if not rows:
        errors.append("no data rows parsed from traceability table")

    return errors, rows


def _authoritative_requirement_docs() -> list[str]:
    docs: list[str] = []
    for path in REQ_DIR.glob("20.*.md"):
        if not path.is_file():
            continue
        if REQ_DOC_RE.match(path.name):
            docs.append(path.name)
    return sorted(docs, key=_sort_key)


def _sort_key(filename: str) -> tuple[int, str]:
    match = REQ_DOC_RE.match(filename)
    if not match:
        return (sys.maxsize, filename.casefold())
    return (int(match.group(1)), filename.casefold())


def _resolve_anchor(anchor: str) -> Path:
    target = anchor.strip().strip("`")
    target = target.split("#", 1)[0].strip()
    return (REQ_DIR / target).resolve()


def main() -> int:
    if not MATRIX_PATH.exists():
        print("ERROR: missing required matrix file thought_simulator/20_requirements/20.200_traceability_matrix.md")
        return 1

    parse_errors, rows = _parse_matrix_rows(MATRIX_PATH.read_text(encoding="utf-8"))
    errors: list[str] = parse_errors[:]

    expected_docs = _authoritative_requirement_docs()
    expected_set = set(expected_docs)

    row_docs = [row[0].strip().strip("`") for row in rows]
    row_set = set(row_docs)

    duplicates = sorted(name for name in row_set if row_docs.count(name) > 1)
    if duplicates:
        errors.append("matrix contains duplicate 20-series requirement rows")
        errors.extend(f"  - duplicate row for: {name}" for name in duplicates)

    missing_rows = sorted(expected_set - row_set, key=_sort_key)
    extra_rows = sorted(row_set - expected_set, key=_sort_key)

    if missing_rows:
        errors.append("matrix is stale: authoritative 20-series docs missing from matrix")
        errors.extend(f"  - missing row for: {name}" for name in missing_rows)

    if extra_rows:
        errors.append("matrix references non-authoritative or missing 20-series docs")
        errors.extend(f"  - extra/non-existent row: {name}" for name in extra_rows)

    expected_order = sorted(row_docs, key=_sort_key)
    if row_docs != expected_order:
        errors.append("matrix rows are not in deterministic numeric 20-series order")
        errors.append("  - observed order:")
        errors.extend(f"    - {name}" for name in row_docs)
        errors.append("  - required order:")
        errors.extend(f"    - {name}" for name in expected_order)

    for doc_name, _scope, verification_anchor, design_anchor in rows:
        clean_doc = doc_name.strip().strip("`")
        if clean_doc in expected_set and not (REQ_DIR / clean_doc).exists():
            errors.append(f"row references missing requirement file: {clean_doc}")

        for anchor_label, anchor in (
            ("verification", verification_anchor),
            ("design", design_anchor),
        ):
            target = _resolve_anchor(anchor)
            if not target.exists():
                errors.append(
                    f"row '{clean_doc}' has broken {anchor_label} anchor: {anchor.strip()}"
                )

    if errors:
        print("ERROR: 20 traceability matrix validation failed.")
        for line in errors:
            print(line)
        print("Deterministic comparison set:")
        print("  Expected authoritative 20-series docs:")
        for name in expected_docs:
            print(f"    - {name}")
        print("  Matrix row docs:")
        for name in row_docs:
            print(f"    - {name}")
        return 1

    print("20 traceability matrix validation passed.")
    print("Validated 20-series docs:")
    for name in expected_docs:
        print(f"  - {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
