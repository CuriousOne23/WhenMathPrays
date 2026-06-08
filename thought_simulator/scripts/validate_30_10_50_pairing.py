#!/usr/bin/env python3
"""Warn when promoted/approved 30.01 rows lack a matching 10.50.xx peer on disk.

One-way check only: 30 → 10.50 (not 10.50 → 30). Ten-series anchors may exist
before verification modules; orphan 10.50 files are intentionally not reported.

Policy source: 30.00 § Promotion completeness; 30.01 status definitions.
Non-blocking (exit 0). Structural checks only.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIER_DIR = ROOT / "30_verification"
INDEX_PATH = TIER_DIR / "30.01_verification_inventory_index.md"
TEN_FIFTY_DIR = ROOT / "10_thought_simulator_req" / "50_design"

PAIRING_STATUSES = frozenset({"promoted", "approved"})
MODULE_NUM_PATTERN = re.compile(r"^30\.(\d+)_")
EXPLICIT_PEER_PATTERN = re.compile(r"10\.50\.(\d+)")


def _parse_inventory_rows(text: str) -> list[tuple[str, str, str]]:
    """Return list of (module_dir_name, status, notes)."""
    rows: list[tuple[str, str, str]] = []
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("| Module path"):
            in_table = True
            continue
        if not in_table or not stripped.startswith("|"):
            continue
        if re.match(r"^\|\s*-+", stripped):
            continue
        cols = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cols) < 4:
            continue
        module_cell = cols[0]
        if module_cell.startswith("**Pending") or module_cell.startswith("Wave "):
            break
        link_match = re.search(r"\[`([^`]+)/`\]", module_cell)
        if not link_match:
            link_match = re.search(r"\[([^\]]+)/\]", module_cell)
        if not link_match:
            continue
        module_name = link_match.group(1).rstrip("/")
        status = cols[3].strip().lower()
        notes = cols[4].strip() if len(cols) > 4 else ""
        rows.append((module_name, status, notes))
    return rows


def _numeric_band(module_name: str, notes: str) -> str | None:
    """Resolve 10.50 numeric band from module dir or explicit note reference."""
    peer_match = EXPLICIT_PEER_PATTERN.search(notes)
    if peer_match:
        return peer_match.group(1)
    mod_match = MODULE_NUM_PATTERN.match(module_name)
    if mod_match:
        return mod_match.group(1)
    return None


def _ten_fifty_peer_exists(numeric_band: str) -> bool:
    if not TEN_FIFTY_DIR.is_dir():
        return False
    pattern = f"10.50.{numeric_band}_*.md"
    return any(TEN_FIFTY_DIR.glob(pattern))


def main() -> int:
    warnings: list[str] = []

    if not INDEX_PATH.is_file():
        warnings.append(
            f"missing required index: {INDEX_PATH.relative_to(ROOT).as_posix()}"
        )
    elif not TEN_FIFTY_DIR.is_dir():
        warnings.append(
            f"missing 10.50 directory: {TEN_FIFTY_DIR.relative_to(ROOT).as_posix()}"
        )
    else:
        rows = _parse_inventory_rows(INDEX_PATH.read_text(encoding="utf-8"))
        for module_name, status, notes in rows:
            if status not in PAIRING_STATUSES:
                continue
            band = _numeric_band(module_name, notes)
            if band is None:
                warnings.append(
                    f"30/10.50 pairing: cannot resolve numeric band for '{module_name}'"
                )
                continue
            if not _ten_fifty_peer_exists(band):
                expected = f"10.50.{band}_*.md"
                warnings.append(
                    f"30/10.50 pairing: '{module_name}' (status={status}) has no peer "
                    f"under 10_thought_simulator_req/50_design/ matching '{expected}'"
                )

    if warnings:
        print("30/10.50 pairing warnings:")
        for item in sorted(warnings):
            print(f"- {item}")
        print(
            "30/10.50 pairing check completed with warnings (non-blocking). "
            "One-way rule: promoted/approved 30 modules require 10.50 peers; "
            "orphan 10.50 files are not reported."
        )
        return 0

    print(
        "30/10.50 pairing check passed: all promoted/approved 30.01 rows "
        "have matching 10.50.xx peers on disk."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())