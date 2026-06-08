#!/usr/bin/env python3
"""Warn when 30.01 inventory index drifts from on-disk module layout.

Non-blocking (exit 0). Structural checks only — not capsule content.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIER_DIR = ROOT / "30_verification"
INDEX_PATH = TIER_DIR / "30.01_verification_inventory_index.md"

MODULE_DIR_PATTERN = re.compile(r"^30\.\d+_.+")
IGNORED_DIRS = frozenset({"30.tb", "__pycache__"})
CAPSULE_LINK_PATTERN = re.compile(r"\[`([^`]+)`\]\([^)]+\)")


def _module_dirs_on_disk() -> set[str]:
    found: set[str] = set()
    if not TIER_DIR.is_dir():
        return found
    for child in TIER_DIR.iterdir():
        if not child.is_dir():
            continue
        if child.name in IGNORED_DIRS or child.name.startswith("."):
            continue
        if MODULE_DIR_PATTERN.match(child.name):
            found.add(child.name)
    return found


def _parse_inventory_table(text: str) -> tuple[set[str], list[str]]:
    """Return (module_dir_names, path_warnings)."""
    modules: set[str] = set()
    path_warnings: list[str] = []
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
        if len(cols) < 2:
            continue
        module_cell = cols[0]
        if module_cell.startswith("**Pending"):
            break
        link_match = re.search(r"\[`([^`]+)/`\]", module_cell)
        if not link_match:
            link_match = re.search(r"\[([^\]]+)/\]", module_cell)
        if not link_match:
            continue
        module_name = link_match.group(1).rstrip("/")
        modules.add(module_name)
        capsule_cell = cols[1] if len(cols) > 1 else ""
        for cap_match in CAPSULE_LINK_PATTERN.finditer(capsule_cell):
            rel = cap_match.group(1)
            if not rel.endswith(".md"):
                continue
            cap_path = TIER_DIR / module_name / rel
            if not cap_path.is_file():
                path_warnings.append(
                    f"30.01: module '{module_name}' references missing capsule path '{rel}'"
                )
        delta_cell = cols[2] if len(cols) > 2 else ""
        if delta_cell and delta_cell.endswith(".md") and "`" not in delta_cell:
            delta_path = TIER_DIR / module_name / delta_cell.strip()
            if not delta_path.is_file():
                path_warnings.append(
                    f"30.01: module '{module_name}' references missing delta path '{delta_cell.strip()}'"
                )
    return modules, path_warnings


def main() -> int:
    warnings: list[str] = []

    if not INDEX_PATH.is_file():
        warnings.append(f"missing required index: {INDEX_PATH.relative_to(ROOT).as_posix()}")
    else:
        indexed, path_warnings = _parse_inventory_table(INDEX_PATH.read_text(encoding="utf-8"))
        warnings.extend(path_warnings)
        on_disk = _module_dirs_on_disk()
        for name in sorted(on_disk - indexed):
            warnings.append(
                f"30.01: on-disk module '{name}' has no row in module inventory table"
            )
        for name in sorted(indexed - on_disk):
            warnings.append(
                f"30.01: table row '{name}' has no matching directory under 30_verification/"
            )

    if warnings:
        print("30 inventory index warnings:")
        for item in sorted(warnings):
            print(f"- {item}")
        print("30 inventory index check completed with warnings (non-blocking).")
        return 0

    print("30 inventory index check passed: 30.01 aligns with on-disk module directories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())