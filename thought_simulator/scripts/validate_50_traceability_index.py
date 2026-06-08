#!/usr/bin/env python3
"""Warn when 50.00 design traceability index drifts from on-disk design files.

Mirrors the structural rules in .github/workflows/validate_design_traceability.yml.
Non-blocking locally (exit 0). GitHub Actions workflow remains blocking for PRs.

Level-2 design docs (50.xx.yy_*) are excluded from the filesystem comparison set.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN_DIR = ROOT / "50_thought_simulator_design"
INDEX_PATH = DESIGN_DIR / "50.00_design_traceability_index.md"
INDEX_NAME = "50.00_design_traceability_index.md"
LEVEL2_PATTERN = re.compile(r"^50\.\d+\.\d+_.*\.md$")


def _design_files_on_disk() -> list[str]:
    names: list[str] = []
    for path in DESIGN_DIR.glob("50.*.md"):
        if path.name == INDEX_NAME:
            continue
        if LEVEL2_PATTERN.match(path.name):
            continue
        names.append(path.name)
    return sorted(names)


def _parse_table(content: str) -> tuple[list[list[str]], list[str]]:
    rows: list[list[str]] = []
    format_warnings: list[str] = []
    table_lines = [line for line in content.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 3:
        format_warnings.append("50.00: traceability table not found or malformed")
        return rows, format_warnings

    for line in table_lines:
        raw = line.strip()
        if re.match(r"^\|\s*-+", raw):
            continue
        cols = [c.strip() for c in raw.strip("|").split("|")]
        if len(cols) < 4:
            continue
        if cols[0].lower() == "macro / domain":
            continue
        rows.append(cols[:4])
    return rows, format_warnings


def main() -> int:
    warnings: list[str] = []

    if not INDEX_PATH.is_file():
        warnings.append(
            "missing required index file thought_simulator/50_thought_simulator_design/"
            "50.00_design_traceability_index.md"
        )
        _emit(warnings)
        return 0

    content = INDEX_PATH.read_text(encoding="utf-8")
    rows, format_warnings = _parse_table(content)
    warnings.extend(format_warnings)

    if rows:
        macro_names = [r[0] for r in rows]
        sorted_macros = sorted(macro_names, key=lambda s: s.casefold())
        if macro_names != sorted_macros:
            warnings.append("50.00: table rows are not alphabetically sorted by Macro / Domain")

    referenced_files: set[str] = set()
    for row in rows:
        design_ref = row[3].strip().strip("`")
        if design_ref.startswith("50.") and design_ref.endswith(".md"):
            referenced_files.add(design_ref)
        elif "placeholder" in design_ref.lower():
            continue
        else:
            warnings.append(f"50.00: malformed design-doc reference for '{row[0]}': {design_ref}")

    expected_files = _design_files_on_disk()
    expected_set = set(expected_files)

    for name in sorted(expected_set - referenced_files):
        warnings.append(f"50.00: on-disk design file missing from table: {name}")
    for name in sorted(referenced_files - expected_set):
        warnings.append(f"50.00: table references non-existent design file: {name}")

    _emit(warnings)
    return 0


def _emit(warnings: list[str]) -> None:
    if warnings:
        print("50 traceability index warnings:")
        for item in warnings:
            print(f"- {item}")
        print("50 traceability index check completed with warnings (non-blocking).")
    else:
        print("50 traceability index check passed: 50.00 aligns with on-disk design files.")


if __name__ == "__main__":
    raise SystemExit(main())