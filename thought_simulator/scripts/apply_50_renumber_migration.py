#!/usr/bin/env python3
"""Apply Phase-3 50 design renumber per naming_strategy_target.md §6.

Reads 00_program_governance/00_identity/50_renumber_manifest.json, two-phase
renames level-1/2 design files to align with post-Phase-2 10.50/30 bands,
updates references (canonical paths + governed shorthand), rebuilds 50_name_table.

Usage:
  python thought_simulator/scripts/apply_50_renumber_migration.py --plan
  python thought_simulator/scripts/apply_50_renumber_migration.py --apply --yes
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from identity_tables import (
    IDENTITY_DIR,
    ROOT,
    TABLE_10_50,
    TABLE_30,
    TABLE_50,
    TIER_50_BASE,
    IdentityEntry,
    bootstrap_all_tables,
    build_50_entry,
    entries_by_id,
    identity_replacement_pairs,
    load_table,
    save_table,
)
from shorthand_patterns import shorthand_replacement_pairs

MANIFEST = IDENTITY_DIR / "50_renumber_manifest.json"
DESIGN_DIR = ROOT / TIER_50_BASE

SKIP_DIRS = frozenset({"archive", "__pycache__", ".git", "node_modules"})
SCAN_EXTENSIONS = {".md", ".py", ".json"}

GOVERNANCE_PROTECT = frozenset(
    {
        "50.00_design_traceability_index.md",
        "50.01_50_series_glossary.md",
        "50.05_software_spec_construction_guide.md",
        "50.07_system_architecture.md",
        "50.08_core_contract.md",
    }
)

INVENTORY_PATHS = [
    ROOT / "50_thought_simulator_design/50.00_design_traceability_index.md",
]


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
    filename = f"50.{new_band}_{old.slug}.md"
    return build_50_entry(filename, children=old.children)


def _staging_name(old: IdentityEntry, seq: int) -> str:
    return f"50.{900 + seq}_{old.slug}.md"


def _build_plan(manifest: dict) -> list[tuple[IdentityEntry, IdentityEntry]]:
    table = load_table(TABLE_50)
    by_id = entries_by_id(table)
    plan: list[tuple[IdentityEntry, IdentityEntry]] = []
    for item in manifest["file_renames"]:
        entry_id = item["entry_id"]
        new_band = item["new_band"]
        if entry_id not in by_id:
            raise KeyError(f"entry not in 50_name_table: {entry_id}")
        old = by_id[entry_id]
        new = _compute_new_entry(old, new_band)
        if old.entry_id == new.entry_id:
            continue
        plan.append((old, new))
    return plan


def _collect_replacements(plan: list[tuple[IdentityEntry, IdentityEntry]]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for old, new in plan:
        pairs.extend(identity_replacement_pairs(old, new, rename_class="B"))

    for inv in INVENTORY_PATHS:
        if not inv.is_file():
            continue
        rel = inv.relative_to(ROOT).as_posix()
        for old, new in plan:
            if old.band != new.band:
                pairs.extend(shorthand_replacement_pairs(old.band, new.band, "50", rel_path=rel))

    for path in sorted(ROOT.rglob("*.md")):
        rel_parts = path.relative_to(ROOT).parts
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        if path.name in GOVERNANCE_PROTECT:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if not (
            rel.startswith("50_thought_simulator_design/")
            or rel.startswith("30_verification/")
            or rel.startswith("10_thought_simulator_req/")
            or rel.startswith("40_thought_simulator_playground/")
            or rel.startswith("20_requirements/")
        ):
            continue
        for old, new in plan:
            if old.band != new.band:
                pairs.extend(shorthand_replacement_pairs(old.band, new.band, "50", rel_path=rel))

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
        if path.name in GOVERNANCE_PROTECT:
            continue
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
    parser = argparse.ArgumentParser(description="Apply 50 design renumber migration.")
    parser.add_argument("--plan", action="store_true", help="Show migration plan.")
    parser.add_argument("--apply", action="store_true", help="Execute migration.")
    parser.add_argument("--yes", action="store_true", help="Confirm apply.")
    args = parser.parse_args()

    if not args.plan and not args.apply:
        args.plan = True

    manifest = _load_manifest()
    plan = _build_plan(manifest)
    replacements = _collect_replacements(plan)

    print("=== 50 Design Renumber Migration ===")
    print(f"Manifest: {MANIFEST.relative_to(ROOT).as_posix()}")
    print(f"File renames: {len(plan)}")
    print()
    for old, new in plan:
        print(f"  {old.entry_id} -> {new.entry_id}")
    print()
    print(f"Replacement pairs: {len(replacements)}")

    if not args.apply:
        print("\nPlan only. Re-run with --apply --yes to execute.")
        return 0

    if not args.yes:
        print("ERROR: --apply requires --yes")
        return 1

    stage_plan: list[tuple[Path, Path]] = []
    for seq, (old, new) in enumerate(plan):
        src = DESIGN_DIR / old.canonical_name
        if not src.is_file():
            raise FileNotFoundError(f"missing 50 file: {old.canonical_name}")
        staging = DESIGN_DIR / _staging_name(old, seq)
        if staging.exists():
            raise FileExistsError(f"staging collision: {staging.name}")
        src.rename(staging)
        stage_plan.append((staging, DESIGN_DIR / new.canonical_name))

    for staging, final in stage_plan:
        if final.exists():
            raise FileExistsError(f"final target exists: {final.name}")
        staging.rename(final)
        print(f"50 -> {final.name}")

    changed = _apply_text_replacements(replacements)

    tables = bootstrap_all_tables()
    save_table(TABLE_50, tables["50"])
    save_table(TABLE_10_50, tables["10.50"])
    save_table(TABLE_30, tables["30"])
    print("Rebuilt 50, 10.50, and 30 name tables from disk")

    manifest["executed"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    with MANIFEST.open("w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")

    log_dir = ROOT / "archive" / "refactors"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"50_RENUMBER_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%M%S')}.md"
    with log_file.open("w", encoding="utf-8") as lf:
        lf.write("# 50 Design Renumber Log\n\n")
        lf.write(f"Date: {datetime.now(timezone.utc).isoformat()}\n")
        lf.write(f"Manifest: {MANIFEST.as_posix()}\n\n")
        lf.write("## File renames\n")
        for old, new in plan:
            lf.write(f"- `{old.canonical_path}` → `{new.canonical_path}`\n")
        lf.write(f"\n## Content files updated: {changed}\n")

    print(f"Content files updated: {changed}")
    print(f"Log: {log_file.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())