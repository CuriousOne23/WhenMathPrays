#!/usr/bin/env python3
"""Apply Phase-2 coupled 10.50+30 renumber per naming_strategy_target.md.

Reads 00_program_governance/00_identity/30_1050_renumber_manifest.json, two-phase
renames all coupled pairs to stride-10 bands from 50, updates references (canonical
paths + governed shorthand), renames internal 30 capsule/delta files, rebuilds
10.50 and 30 name tables.

Usage:
  python thought_simulator/scripts/apply_30_1050_renumber_migration.py --plan
  python thought_simulator/scripts/apply_30_1050_renumber_migration.py --apply --yes
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
    TIER_10_50_BASE,
    TIER_30_BASE,
    IdentityEntry,
    bootstrap_all_tables,
    build_10_50_entry,
    build_30_entry,
    entries_by_id,
    identity_replacement_pairs,
    load_table,
    save_table,
)
from shorthand_patterns import shorthand_replacement_pairs

MANIFEST = IDENTITY_DIR / "30_1050_renumber_manifest.json"
DESIGN_DIR = ROOT / TIER_10_50_BASE
VERIFY_DIR = ROOT / TIER_30_BASE

SKIP_DIRS = frozenset({"archive", "__pycache__", ".git", "node_modules"})
SCAN_EXTENSIONS = {".md", ".py", ".json"}

GOVERNANCE_PROTECT = (
    "30.00_verification_user_guide.md",
    "30.01_verification_inventory_index.md",
    "30.150_verification_of_semantic_specification.md",
    "30.30_verification_glossary.md",
    "30.160_verification_of_reference_algorithms.md",
    "30.210_evidence_trace_exemplars_non_normative.md",
)

INVENTORY_PATHS = [
    ROOT / "30_verification/30.01_verification_inventory_index.md",
    ROOT / "50_thought_simulator_design/50.00_design_traceability_index.md",
    ROOT / "10_thought_simulator_req/50_design/README.md",
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


def _compute_10_50_entry(old: IdentityEntry, new_band: str) -> IdentityEntry:
    return build_10_50_entry(f"10.50.{new_band}_{old.slug}.md")


def _compute_30_entry(old: IdentityEntry, new_band: str, paired_1050: str) -> IdentityEntry:
    return build_30_entry(f"30.{new_band}_{old.slug}", paired_10_50=paired_1050)


def _staging_1050(old: IdentityEntry, seq: int) -> str:
    return f"10.50.{900 + seq}_{old.slug}.md"


def _staging_30(old: IdentityEntry, seq: int) -> str:
    return f"30.{900 + seq}_{old.slug}"


def _build_plan(manifest: dict) -> list[tuple[IdentityEntry, IdentityEntry, IdentityEntry, IdentityEntry]]:
    table_1050 = load_table(TABLE_10_50)
    table_30 = load_table(TABLE_30)
    by_1050 = entries_by_id(table_1050)
    by_30 = entries_by_id(table_30)

    plan: list[tuple[IdentityEntry, IdentityEntry, IdentityEntry, IdentityEntry]] = []
    for item in manifest["pair_renames"]:
        eid_1050 = item["entry_id_1050"]
        eid_30 = item["entry_id_30"]
        new_band = item["new_band"]
        if eid_1050 not in by_1050:
            raise KeyError(f"10.50 entry not in name table: {eid_1050}")
        if eid_30 not in by_30:
            raise KeyError(f"30 entry not in name table: {eid_30}")
        old_1050 = by_1050[eid_1050]
        old_30 = by_30[eid_30]
        new_1050 = _compute_10_50_entry(old_1050, new_band)
        new_30 = _compute_30_entry(old_30, new_band, new_1050.entry_id)
        if old_1050.entry_id == new_1050.entry_id and old_30.entry_id == new_30.entry_id:
            continue
        plan.append((old_1050, new_1050, old_30, new_30))
    return plan


def _collect_replacements(plan: list[tuple[IdentityEntry, IdentityEntry, IdentityEntry, IdentityEntry]]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for old_1050, new_1050, old_30, new_30 in plan:
        pairs.extend(identity_replacement_pairs(old_1050, new_1050, rename_class="B"))
        pairs.extend(identity_replacement_pairs(old_30, new_30, rename_class="B"))
        # Do not add bare 30.{band}_ text pairs — substring collisions (e.g. 30.20_
        # corrupting 30.200_mb). Non-standard capsule names are renamed on disk.

    # Governed shorthand in allowlisted inventory / spec files only
    for inv in INVENTORY_PATHS:
        if not inv.is_file():
            continue
        rel = inv.relative_to(ROOT).as_posix()
        for old_1050, new_1050, old_30, new_30 in plan:
            if old_1050.band != new_1050.band:
                pairs.extend(
                    shorthand_replacement_pairs(old_1050.band, new_1050.band, "10.50", rel_path=rel)
                )
            if old_30.band != new_30.band:
                pairs.extend(
                    shorthand_replacement_pairs(old_30.band, new_30.band, "30", rel_path=rel)
                )

    # Global governed shorthand sweep for tier docs and design specs
    for path in sorted(ROOT.rglob("*.md")):
        rel_parts = path.relative_to(ROOT).parts
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if not (
            rel.startswith("30_verification/")
            or rel.startswith("10_thought_simulator_req/50_design/")
            or rel.startswith("50_thought_simulator_design/")
            or rel.endswith("40.510_refactor.md")
        ):
            continue
        if path.name in GOVERNANCE_PROTECT:
            continue
        for old_1050, new_1050, old_30, new_30 in plan:
            if old_1050.band != new_1050.band:
                pairs.extend(
                    shorthand_replacement_pairs(old_1050.band, new_1050.band, "10.50", rel_path=rel)
                )
            if old_30.band != new_30.band:
                pairs.extend(
                    shorthand_replacement_pairs(old_30.band, new_30.band, "30", rel_path=rel)
                )

    return _dedupe_pairs(pairs)


def _rename_internal_30_files(folder: Path, old_30: IdentityEntry, new_30: IdentityEntry) -> None:
    if not folder.is_dir():
        return
    old_prefixes = (old_30.entry_id, f"30.{old_30.band}_")
    for child in sorted(folder.iterdir()):
        if not child.is_file():
            continue
        name = child.name
        for old_prefix in old_prefixes:
            if name.startswith(old_prefix):
                suffix = name[len(old_prefix) :]
                new_name = new_30.entry_id + suffix
                if name != new_name:
                    child.rename(folder / new_name)
                break
            if name.startswith(f"30.{old_30.band}_"):
                suffix = name[len(f"30.{old_30.band}_") :]
                new_name = f"30.{new_30.band}_" + suffix
                if name != new_name:
                    child.rename(folder / new_name)
                break


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
    parser = argparse.ArgumentParser(description="Apply coupled 10.50+30 renumber migration.")
    parser.add_argument("--plan", action="store_true", help="Show migration plan.")
    parser.add_argument("--apply", action="store_true", help="Execute migration.")
    parser.add_argument("--yes", action="store_true", help="Confirm apply.")
    args = parser.parse_args()

    if not args.plan and not args.apply:
        args.plan = True

    manifest = _load_manifest()
    plan = _build_plan(manifest)
    replacements = _collect_replacements(plan)

    print("=== 10.50 + 30 Coupled Renumber Migration ===")
    print(f"Manifest: {MANIFEST.relative_to(ROOT).as_posix()}")
    print(f"Coupled pairs: {len(plan)}")
    print()
    print("Pair mapping:")
    for old_1050, new_1050, old_30, new_30 in plan:
        print(f"  {old_1050.entry_id} + {old_30.entry_id}")
        print(f"    -> {new_1050.entry_id} + {new_30.entry_id}")
    print()
    print(f"Replacement pairs: {len(replacements)}")

    if not args.apply:
        print("\nPlan only. Re-run with --apply --yes to execute.")
        return 0

    if not args.yes:
        print("ERROR: --apply requires --yes")
        return 1

    # Phase 1: stage 10.50 files
    stage_1050: list[tuple[Path, Path, IdentityEntry, IdentityEntry]] = []
    for seq, (old_1050, new_1050, _old_30, _new_30) in enumerate(plan):
        src = DESIGN_DIR / old_1050.canonical_name
        if not src.is_file():
            raise FileNotFoundError(f"missing 10.50 file: {old_1050.canonical_name}")
        staging_name = _staging_1050(old_1050, seq)
        staging = DESIGN_DIR / staging_name
        if staging.exists():
            raise FileExistsError(f"staging collision: {staging_name}")
        src.rename(staging)
        stage_1050.append((staging, DESIGN_DIR / new_1050.canonical_name, old_1050, new_1050))

    # Phase 1: stage 30 folders
    stage_30: list[tuple[Path, Path, IdentityEntry, IdentityEntry]] = []
    for seq, (_old_1050, _new_1050, old_30, new_30) in enumerate(plan):
        src = VERIFY_DIR / old_30.canonical_name
        if not src.is_dir():
            raise FileNotFoundError(f"missing 30 folder: {old_30.canonical_name}")
        staging_name = _staging_30(old_30, seq)
        staging = VERIFY_DIR / staging_name
        if staging.exists():
            raise FileExistsError(f"staging collision: {staging_name}")
        src.rename(staging)
        stage_30.append((staging, VERIFY_DIR / new_30.canonical_name, old_30, new_30))

    # Phase 2: final 10.50 names
    for staging, final, _old, new in stage_1050:
        if final.exists():
            raise FileExistsError(f"final 10.50 target exists: {final.name}")
        staging.rename(final)
        print(f"10.50 -> {final.name}")

    # Phase 2: final 30 names + internal file renames
    for staging, final, old_30, new_30 in stage_30:
        if final.exists():
            raise FileExistsError(f"final 30 target exists: {final.name}")
        staging.rename(final)
        _rename_internal_30_files(final, old_30, new_30)
        print(f"30 -> {final.name}")

    changed = _apply_text_replacements(replacements)

    tables = bootstrap_all_tables()
    save_table(TABLE_10_50, tables["10.50"])
    save_table(TABLE_30, tables["30"])
    print("Rebuilt 10.50_name_table.json and 30_name_table.json from disk")

    manifest["executed"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    with MANIFEST.open("w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")

    log_dir = ROOT / "archive" / "refactors"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"30_1050_RENUMBER_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%M%S')}.md"
    with log_file.open("w", encoding="utf-8") as lf:
        lf.write("# 10.50 + 30 Coupled Renumber Log\n\n")
        lf.write(f"Date: {datetime.now(timezone.utc).isoformat()}\n")
        lf.write(f"Manifest: {MANIFEST.as_posix()}\n\n")
        lf.write("## Coupled pair renames\n")
        for old_1050, new_1050, old_30, new_30 in plan:
            lf.write(f"- `{old_1050.canonical_path}` + `{old_30.canonical_path}`\n")
            lf.write(f"  -> `{new_1050.canonical_path}` + `{new_30.canonical_path}`\n")
        lf.write(f"\n## Content files updated: {changed}\n")

    print(f"Content files updated: {changed}")
    print(f"Log: {log_file.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())