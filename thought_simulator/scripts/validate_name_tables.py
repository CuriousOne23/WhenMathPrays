#!/usr/bin/env python3
"""Validate identity name tables against filesystem state.

Checks:
- Table schema and entry uniqueness
- Canonical paths exist on disk
- 30 <-> 10.50 band pairing consistency
- No duplicate bands within a tier (except aliases)
- Stale alias detection (optional warning)

Mode: warning (exit 0) for local pre-PR; use --strict for blocking.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from identity_tables import (
    IDENTITY_DIR,
    ROOT,
    SCHEMA_VERSION,
    TABLE_10_50,
    TABLE_30,
    TABLE_40,
    TABLE_50,
    entries_by_id,
)

SKIP_SCAN_DIRS = frozenset({"archive", "__pycache__", ".git", "node_modules", "00_identity"})


def _load(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _validate_schema(table: dict, path: Path, errors: list[str]) -> None:
    if table.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"{path.name}: schema_version must be {SCHEMA_VERSION}")
    if "entries" not in table or not isinstance(table["entries"], list):
        errors.append(f"{path.name}: missing entries array")


def _duplicate_band_expected(table: dict, band: str) -> bool:
    """Headroom docs may share a module band when all colliders are shorthand-ineligible."""
    colliders = [e for e in table.get("entries", []) if e.get("band") == band]
    if len(colliders) < 2:
        return False
    return all(not e.get("shorthand_eligible", True) for e in colliders)


def _validate_entries(table: dict, path: Path, errors: list[str], warnings: list[str]) -> dict[str, dict]:
    by_id: dict[str, dict] = {}
    bands: dict[str, str] = {}
    for entry in table.get("entries", []):
        entry_id = entry.get("entry_id")
        if not entry_id:
            errors.append(f"{path.name}: entry missing entry_id")
            continue
        if entry_id in by_id:
            errors.append(f"{path.name}: duplicate entry_id {entry_id}")
        by_id[entry_id] = entry
        band = entry.get("band")
        canonical_path = entry.get("canonical_path")
        if not band or not canonical_path:
            errors.append(f"{path.name}: entry {entry_id} missing band or canonical_path")
            continue
        if band in bands and bands[band] != entry_id and not _duplicate_band_expected(table, band):
            warnings.append(f"{path.name}: duplicate band {band} ({bands[band]} and {entry_id})")
        bands.setdefault(band, entry_id)
        fs_path = ROOT / canonical_path
        if not fs_path.exists():
            errors.append(f"{path.name}: missing on disk: {canonical_path}")
        for alias in entry.get("aliases", []):
            if alias == entry.get("canonical_name"):
                warnings.append(f"{path.name}: alias equals canonical_name for {entry_id}")
    return by_id


def _validate_pairing(
    table_10_50: dict[str, dict],
    table_30: dict[str, dict],
    errors: list[str],
    warnings: list[str],
) -> None:
    thirty = entries_by_id(table_30)
    for entry in table_10_50.get("entries", []):
        paired = entry.get("paired_entry_id")
        if not paired:
            continue
        if paired not in thirty:
            warnings.append(f"10.50 {entry['entry_id']}: paired_entry_id {paired} not in 30 table")
            continue
        if entry["band"] != thirty[paired].band:
            errors.append(
                f"band mismatch: 10.50 {entry['entry_id']} band {entry['band']} "
                f"!= 30 {paired} band {thirty[paired].band}"
            )
    for entry in table_30.get("entries", []):
        paired = entry.get("paired_entry_id")
        if not paired:
            continue
        ten = next((e for e in table_10_50.get("entries", []) if e["entry_id"] == paired), None)
        if not ten:
            warnings.append(f"30 {entry['entry_id']}: paired_entry_id {paired} not in 10.50 table")
        elif entry["band"] != ten["band"]:
            errors.append(
                f"band mismatch: 30 {entry['entry_id']} band {entry['band']} "
                f"!= 10.50 {paired} band {ten['band']}"
            )


def _scan_stale_aliases(warnings: list[str]) -> None:
    """Warn if any alias string appears in active repo outside archive."""
    if not IDENTITY_DIR.is_dir():
        return
    aliases: list[tuple[str, str]] = []
    for table_path in (TABLE_40, TABLE_10_50, TABLE_30, TABLE_50):
        if not table_path.is_file():
            continue
        table = _load(table_path)
        for entry in table.get("entries", []):
            for alias in entry.get("aliases", []):
                aliases.append((alias, entry["entry_id"]))

    if not aliases:
        return

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in {".md", ".py", ".json"}:
            continue
        rel_parts = path.relative_to(ROOT).parts
        if any(part in SKIP_SCAN_DIRS for part in rel_parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for alias, entry_id in aliases:
            if alias in text:
                warnings.append(
                    f"stale alias '{alias}' (entry {entry_id}) found in {path.relative_to(ROOT).as_posix()}"
                )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate identity name tables.")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any issue (including warnings).")
    parser.add_argument("--scan-aliases", action="store_true", help="Scan repo for stale alias strings.")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    required = [TABLE_40, TABLE_10_50, TABLE_30, TABLE_50]
    for path in required:
        if not path.is_file():
            errors.append(f"missing name table: {path.relative_to(ROOT).as_posix()}")
            continue
        table = _load(path)
        _validate_schema(table, path, errors)

    if errors:
        for msg in errors:
            print(f"ERROR: {msg}")
        return 1

    t40 = _load(TABLE_40)
    t1050 = _load(TABLE_10_50)
    t30 = _load(TABLE_30)
    t50 = _load(TABLE_50)

    _validate_entries(t40, TABLE_40, errors, warnings)
    _validate_entries(t1050, TABLE_10_50, errors, warnings)
    _validate_entries(t30, TABLE_30, errors, warnings)
    _validate_entries(t50, TABLE_50, errors, warnings)
    _validate_pairing(t1050, t30, errors, warnings)

    if args.scan_aliases:
        _scan_stale_aliases(warnings)

    if warnings:
        print("Name table warnings:")
        for msg in warnings:
            print(f"  - {msg}")

    if errors:
        print("Name table errors:")
        for msg in errors:
            print(f"  - {msg}")

    if errors:
        return 1
    if args.strict and warnings:
        return 1

    if not errors and not warnings:
        print("Name table validation passed.")
    else:
        print("Name table validation passed with warnings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())