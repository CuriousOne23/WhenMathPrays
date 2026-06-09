#!/usr/bin/env python3
"""Apply Phase-1 40 playground renumber per naming_strategy_target.md.

Reads 00_program_governance/00_identity/40_renumber_manifest.json, removes duplicate
folders, two-phase renames survivors to stride-10 bands from 40.50, relocates the
process guide to 40.05, updates references, and rebuilds 40_name_table.json.

Usage:
  python thought_simulator/scripts/apply_40_renumber_migration.py --plan
  python thought_simulator/scripts/apply_40_renumber_migration.py --apply --yes
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from identity_tables import (
    IDENTITY_DIR,
    ROOT,
    TABLE_40,
    IdentityEntry,
    bootstrap_all_tables,
    build_40_entry,
    entries_by_id,
    identity_replacement_pairs,
    load_table,
    save_table,
)
MANIFEST = IDENTITY_DIR / "40_renumber_manifest.json"
PLAYGROUND = ROOT / "40_thought_simulator_playground"

SKIP_DIRS = frozenset({"archive", "__pycache__", ".git", "node_modules"})
SCAN_EXTENSIONS = {".md", ".py", ".json"}


def _load_manifest() -> dict:
    with MANIFEST.open(encoding="utf-8") as fh:
        return json.load(fh)


def _dedupe_pairs(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    seen: set[tuple[str, str]] = set()
    out: list[tuple[str, str]] = []
    for pair in pairs:
        if pair not in seen:
            seen.add(pair)
            out.append(pair)
    return out


def _compute_new_entry(old: IdentityEntry, new_band: str) -> IdentityEntry:
    return build_40_entry(f"40.{new_band}_{old.slug}")


def _staging_name(old: IdentityEntry, seq: int) -> str:
    return f"40.{900 + seq}_{old.slug}"


def _build_plan(manifest: dict) -> tuple[list[tuple[IdentityEntry, IdentityEntry]], list[str], tuple[str, str]]:
    table = load_table(TABLE_40)
    by_id = entries_by_id(table)

    module_plan: list[tuple[IdentityEntry, IdentityEntry]] = []
    for idx, item in enumerate(manifest["survivor_renames"]):
        entry_id = item["entry_id"]
        new_band = item["new_band"]
        if entry_id not in by_id:
            raise KeyError(f"survivor not in 40_name_table: {entry_id}")
        old = by_id[entry_id]
        new = _compute_new_entry(old, new_band)
        if old.entry_id == new.entry_id:
            continue
        module_plan.append((old, new))

    guide = manifest["guide_rename"]
    guide_pair = (guide["old"], guide["new"])
    duplicates = list(manifest["duplicates_remove"])
    return module_plan, duplicates, guide_pair


def _collect_all_replacements(
    module_plan: list[tuple[IdentityEntry, IdentityEntry]],
    guide_pair: tuple[str, str],
) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for old, new in module_plan:
        pairs.extend(identity_replacement_pairs(old, new, rename_class="B"))

    old_guide, new_guide = guide_pair
    old_path = f"40_thought_simulator_playground/{old_guide}"
    new_path = f"40_thought_simulator_playground/{new_guide}"
    pairs.extend(
        [
            (old_guide, new_guide),
            (old_path, new_path),
            ("40.05_master_program_guide", "40.05_master_program_guide"),
            ("[40.05](40.05_master_program_guide.md)", "[40.05](40.05_master_program_guide.md)"),
            ("[40.05_master_program_guide.md]", "[40.05_master_program_guide.md]"),
            ("../40_thought_simulator_playground/40.05_master_program_guide.md",
             "../40_thought_simulator_playground/40.05_master_program_guide.md"),
            ("../../40_thought_simulator_playground/40.05_master_program_guide.md",
             "../../40_thought_simulator_playground/40.05_master_program_guide.md"),
            ("40.05 governs", "40.05 governs"),
            ("40.05, 40.510", "40.05, 40.510"),
            ("40.05 / 40.510", "40.05 / 40.510"),
            ("40.05_master_program_guide", "40.05_master_program_guide"),
        ]
    )

    # Canonical path/name replacements only — bare band shorthand is unsafe when bands
    # are substrings of one another (e.g. 40.100_inb and 40.100_core_data_structs).
    return _dedupe_pairs(pairs)


def _iter_content_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in SCAN_EXTENSIONS:
            continue
        rel_parts = path.relative_to(ROOT).parts
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        files.append(path)
    return sorted(files)


def _apply_text_replacements(replacements: list[tuple[str, str]]) -> int:
    changed = 0
    for path in _iter_content_files():
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        original = text
        for old, new in replacements:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply 40 playground renumber migration.")
    parser.add_argument("--plan", action="store_true", help="Show migration plan.")
    parser.add_argument("--apply", action="store_true", help="Execute migration.")
    parser.add_argument("--yes", action="store_true", help="Confirm apply.")
    args = parser.parse_args()

    if not args.plan and not args.apply:
        args.plan = True

    manifest = _load_manifest()
    module_plan, duplicates, guide_pair = _build_plan(manifest)
    replacements = _collect_all_replacements(module_plan, guide_pair)

    print("=== 40 Playground Renumber Migration ===")
    print(f"Manifest: {MANIFEST.relative_to(ROOT).as_posix()}")
    print(f"Duplicates to remove: {len(duplicates)}")
    print(f"Module renames: {len(module_plan)}")
    print(f"Guide: {guide_pair[0]} -> {guide_pair[1]}")
    print()
    print("Module mapping:")
    for old, new in module_plan:
        print(f"  {old.entry_id} -> {new.entry_id}")
    print()
    print(f"Replacement pairs: {len(replacements)}")

    if not args.apply:
        print("\nPlan only. Re-run with --apply --yes to execute.")
        return 0

    if not args.yes:
        print("ERROR: --apply requires --yes")
        return 1

    # 1. Remove duplicates
    for entry_id in duplicates:
        folder = PLAYGROUND / entry_id
        if folder.is_dir():
            shutil.rmtree(folder)
            print(f"Removed duplicate: {entry_id}")

    # 2. Two-phase module renames (staging 901+ then final)
    staging_plan: list[tuple[Path, Path]] = []
    for seq, (old, new) in enumerate(module_plan):
        src = PLAYGROUND / old.canonical_name
        if not src.is_dir():
            raise FileNotFoundError(f"missing survivor folder: {old.canonical_name}")
        staging = PLAYGROUND / _staging_name(old, seq)
        if staging.exists():
            raise FileExistsError(f"staging collision: {staging.name}")
        src.rename(staging)
        staging_plan.append((staging, PLAYGROUND / new.canonical_name))

    for staging, final in staging_plan:
        if final.exists():
            raise FileExistsError(f"final target exists: {final.name}")
        staging.rename(final)
        print(f"Renamed -> {final.name}")

    # 3. Guide file (after module renames so 40.160_tp paths are already 40.160_*)
    guide_src = PLAYGROUND / guide_pair[0]
    guide_dst = PLAYGROUND / guide_pair[1]
    if guide_src.is_file():
        if guide_dst.exists():
            raise FileExistsError(f"guide target exists: {guide_pair[1]}")
        guide_src.rename(guide_dst)
        print(f"Guide renamed -> {guide_pair[1]}")

    # 4. Global reference updates
    changed = _apply_text_replacements(replacements)

    # 5. Restore guide governance ID (band shorthand 40.20->40.05 must not apply to 40.05)
    if guide_dst.is_file():
        guide_text = guide_dst.read_text(encoding="utf-8")
        original_guide = guide_text
        for old, new in [
            ("# 40.05 Master Program Guide", "# 40.05 Master Program Guide"),
            ("**Document ID:** 40.160", "**Document ID:** 40.05"),
            ("| **40.160** (this guide) |", "| **40.05** (this guide) |"),
        ]:
            guide_text = guide_text.replace(old, new)
        if guide_text != original_guide:
            guide_dst.write_text(guide_text, encoding="utf-8")
            changed += 1

    print(f"Content files updated: {changed}")

    # 6. Rebuild 40 name table from disk
    tables = bootstrap_all_tables()
    save_table(TABLE_40, tables["40"])
    print("Rebuilt 40_name_table.json from disk")

    # 7. Log
    log_dir = ROOT / "archive" / "refactors"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"40_RENUMBER_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%M%S')}.md"
    with log_file.open("w", encoding="utf-8") as lf:
        lf.write("# 40 Playground Renumber Log\n\n")
        lf.write(f"Date: {datetime.now(timezone.utc).isoformat()}\n")
        lf.write(f"Manifest: {MANIFEST.as_posix()}\n\n")
        lf.write("## Removed duplicates\n")
        for d in duplicates:
            lf.write(f"- `{d}`\n")
        lf.write("\n## Module renames\n")
        for old, new in module_plan:
            lf.write(f"- `{old.canonical_path}` → `{new.canonical_path}`\n")
        lf.write(f"\n## Guide\n- `{guide_pair[0]}` → `{guide_pair[1]}`\n")
        lf.write(f"\n## Content files updated: {changed}\n")

    print(f"Log: {log_file.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())