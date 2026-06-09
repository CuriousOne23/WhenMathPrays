#!/usr/bin/env python3
"""Controlled identity rename pipeline (address maintenance, not content review).

Usage:
  python thought_simulator/scripts/rename_identity.py --request path/to/request.json --dry-run
  python thought_simulator/scripts/rename_identity.py --request path/to/request.json --plan
  python thought_simulator/scripts/rename_identity.py --request path/to/request.json --apply --yes

See 00_program_governance/00_foundations/00.00.43_controlled_identity_rename_policy.md
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from identity_tables import (
    IDENTITY_DIR,
    ROOT,
    TABLE_10_50,
    TABLE_30,
    TABLE_40,
    TABLE_50,
    IdentityEntry,
    build_10_50_entry,
    build_30_entry,
    build_40_entry,
    build_50_entry,
    entries_by_id,
    identity_replacement_pairs,
    load_table,
    save_table,
)
from shorthand_patterns import shorthand_replacement_pairs

SKIP_DIRS = frozenset({"archive", "__pycache__", ".git", "node_modules"})
SCAN_EXTENSIONS = {".md", ".py", ".json"}
IGNORE_FILES = frozenset({"rename_request.template.json"})

MANDATORY_INVENTORY_PATHS = [
    "30_verification/30.01_verification_inventory_index.md",
    "50_thought_simulator_design/50.00_design_traceability_index.md",
    "40_thought_simulator_playground/40.510_refactor.md",
    "CONTRIBUTING_CHANGE_WORKFLOW.md",
]


def _load_request(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _table_path_for_tier(tier: str) -> Path:
    mapping = {
        "40": TABLE_40,
        "50": TABLE_50,
        "10.50": TABLE_10_50,
        "30": TABLE_30,
        "30-1050": TABLE_10_50,
    }
    if tier not in mapping:
        raise ValueError(f"unsupported tier: {tier}")
    return mapping[tier]


def _compute_new_entry(old: IdentityEntry, *, new_band: str | None, new_slug: str | None, tier: str) -> IdentityEntry:
    band = new_band if new_band is not None else old.band
    slug = new_slug if new_slug is not None else old.slug

    if tier == "40":
        canonical_name = f"40.{band}_{slug}"
        return build_40_entry(canonical_name)

    if tier == "50":
        canonical_name = f"50.{band}_{slug}.md"
        return build_50_entry(canonical_name, children=old.children)

    if tier == "10.50":
        canonical_name = f"10.50.{band}_{slug}.md"
        entry = build_10_50_entry(canonical_name)
        return IdentityEntry(
            entry_id=entry.entry_id,
            band=entry.band,
            slug=entry.slug,
            kind=entry.kind,
            canonical_name=entry.canonical_name,
            canonical_path=entry.canonical_path,
            paired_entry_id=old.paired_entry_id,
            aliases=old.aliases,
        )

    if tier == "30":
        canonical_name = f"30.{band}_{slug}"
        return build_30_entry(canonical_name, paired_10_50=old.paired_entry_id)

    raise ValueError(f"cannot compute entry for tier {tier}")


def _apply_entry_rename_on_disk(old: IdentityEntry, new: IdentityEntry) -> None:
    old_path = ROOT / old.canonical_path
    new_path = ROOT / new.canonical_path
    if not old_path.exists():
        raise FileNotFoundError(f"source missing: {old.canonical_path}")
    if new_path.exists():
        raise FileExistsError(f"target already exists: {new.canonical_path}")
    new_path.parent.mkdir(parents=True, exist_ok=True)
    old_path.rename(new_path)


def _update_table_entry(table: dict[str, Any], old_id: str, new_entry: IdentityEntry) -> None:
    entries = table.get("entries", [])
    updated = False
    for idx, entry in enumerate(entries):
        if entry.get("entry_id") == old_id:
            new_dict = new_entry.to_dict()
            if old_id != new_entry.entry_id:
                aliases = list(entry.get("aliases", []))
                if old_id not in aliases:
                    aliases.append(old_id)
                if entry.get("canonical_name") not in aliases:
                    aliases.append(entry["canonical_name"])
                new_dict["aliases"] = sorted(set(aliases))
            entries[idx] = new_dict
            updated = True
            break
    if not updated:
        raise KeyError(f"entry_id not found in table: {old_id}")
    table["entries"] = entries


def _tier_for_entry(entry: IdentityEntry) -> str:
    if entry.canonical_path.startswith("40_"):
        return "40"
    if entry.canonical_path.startswith("30_"):
        return "30"
    if entry.canonical_path.startswith("10_"):
        return "10.50"
    if entry.canonical_path.startswith("50_"):
        return "50"
    raise ValueError(f"cannot infer tier for {entry.canonical_path}")


def _band_changes(plan: list[tuple[IdentityEntry, IdentityEntry, str]]) -> list[tuple[str, str, str]]:
    """Return (tier, old_band, new_band) for Class B band migrations in plan."""
    changes: list[tuple[str, str, str]] = []
    for old, new, rename_class in plan:
        if rename_class != "B" or old.band == new.band:
            continue
        changes.append((_tier_for_entry(old), old.band, new.band))
    return changes


def _dedupe_pairs(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    seen: set[tuple[str, str]] = set()
    unique: list[tuple[str, str]] = []
    for pair in pairs:
        if pair not in seen:
            seen.add(pair)
            unique.append(pair)
    return unique


def _collect_replacements(plan: list[tuple[IdentityEntry, IdentityEntry, str]]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for old, new, rename_class in plan:
        pairs.extend(identity_replacement_pairs(old, new, rename_class=rename_class))
    return _dedupe_pairs(pairs)


def _collect_shorthand_replacements(
    plan: list[tuple[IdentityEntry, IdentityEntry, str]],
    *,
    rel_path: str | None = None,
) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for tier, old_band, new_band in _band_changes(plan):
        pairs.extend(shorthand_replacement_pairs(old_band, new_band, tier, rel_path=rel_path))
    return _dedupe_pairs(pairs)


def _files_to_update(replacements: list[tuple[str, str]]) -> list[Path]:
    affected: set[Path] = set()
    for rel in MANDATORY_INVENTORY_PATHS:
        p = ROOT / rel
        if p.is_file():
            affected.add(p)
    for old, _ in replacements:
        if len(old) < 4:
            continue
        for ext in SCAN_EXTENSIONS:
            for path in ROOT.rglob(f"*{ext}"):
                rel_parts = path.relative_to(ROOT).parts
                if any(part in SKIP_DIRS for part in rel_parts):
                    continue
                if path.name in IGNORE_FILES:
                    continue
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                if old in text:
                    affected.add(path)
    return sorted(affected)


def _apply_content_updates(
    paths: list[Path],
    canonical_replacements: list[tuple[str, str]],
    plan: list[tuple[IdentityEntry, IdentityEntry, str]],
) -> int:
    changed = 0
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        rel = path.relative_to(ROOT).as_posix()
        replacements = _dedupe_pairs(
            list(canonical_replacements) + _collect_shorthand_replacements(plan, rel_path=rel)
        )
        original = text
        for old, new in replacements:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
    return changed


def _build_plan(request: dict[str, Any]) -> list[tuple[IdentityEntry, IdentityEntry, str]]:
    tier = request["tier"]
    rename_class = request.get("rename_class", "A")
    entry_id = request["entry_id"]

    if tier == "30-1050":
        table_10 = load_table(TABLE_10_50)
        table_30 = load_table(TABLE_30)
        by_10 = entries_by_id(table_10)
        by_30 = entries_by_id(table_30)
        if entry_id not in by_10:
            raise KeyError(f"10.50 entry not found: {entry_id}")
        old_10 = by_10[entry_id]
        paired_30_id = old_10.paired_entry_id
        if not paired_30_id or paired_30_id not in by_30:
            raise KeyError(f"paired 30 entry missing for {entry_id}")
        old_30 = by_30[paired_30_id]

        new_band = request.get("new_band")
        new_slug_10 = request.get("new_slug_10_50") or request.get("new_slug")
        new_slug_30 = request.get("new_slug_30") or request.get("new_slug")

        new_10 = _compute_new_entry(old_10, new_band=new_band, new_slug=new_slug_10, tier="10.50")
        new_30 = _compute_new_entry(old_30, new_band=new_band, new_slug=new_slug_30, tier="30")
        new_10 = IdentityEntry(
            entry_id=new_10.entry_id,
            band=new_10.band,
            slug=new_10.slug,
            kind=new_10.kind,
            canonical_name=new_10.canonical_name,
            canonical_path=new_10.canonical_path,
            paired_entry_id=new_30.entry_id,
            aliases=old_10.aliases,
        )
        new_30 = IdentityEntry(
            entry_id=new_30.entry_id,
            band=new_30.band,
            slug=new_30.slug,
            kind=new_30.kind,
            canonical_name=new_30.canonical_name,
            canonical_path=new_30.canonical_path,
            paired_entry_id=new_10.entry_id,
            aliases=old_30.aliases,
        )
        return [(old_10, new_10, rename_class), (old_30, new_30, rename_class)]

    table_path = _table_path_for_tier(tier)
    table = load_table(table_path)
    by_id = entries_by_id(table)
    if entry_id not in by_id:
        raise KeyError(f"entry not found: {entry_id}")
    old = by_id[entry_id]
    new = _compute_new_entry(
        old,
        new_band=request.get("new_band"),
        new_slug=request.get("new_slug"),
        tier=tier,
    )
    return [(old, new, rename_class)]


def main() -> int:
    parser = argparse.ArgumentParser(description="Controlled identity rename pipeline.")
    parser.add_argument("--request", required=True, help="Path to rename request JSON.")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Show plan only (default).")
    parser.add_argument("--plan", action="store_true", help="Show detailed affected files.")
    parser.add_argument("--apply", action="store_true", help="Apply renames and content updates.")
    parser.add_argument("--yes", action="store_true", help="Confirm apply.")
    args = parser.parse_args()

    if args.apply and not args.yes:
        print("ERROR: --apply requires --yes after reviewing the plan.")
        return 1

    request_path = Path(args.request)
    if not request_path.is_file():
        print(f"ERROR: request file not found: {request_path}")
        return 1

    request = _load_request(request_path)
    print("=== Controlled Identity Rename Plan ===")
    print(f"Request: {request_path}")
    print(f"Tier: {request.get('tier')}  Class: {request.get('rename_class', 'A')}")
    if request.get("notes"):
        print(f"Notes: {request['notes']}")
    print()

    try:
        plan = _build_plan(request)
    except (KeyError, ValueError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}")
        return 1

    replacements = _collect_replacements(plan)
    shorthand_preview = _collect_shorthand_replacements(plan)
    affected = _files_to_update(replacements + shorthand_preview)

    print("Identity changes:")
    for old, new, rename_class in plan:
        print(f"  {old.entry_id} -> {new.entry_id}")
        print(f"    path: {old.canonical_path}")
        print(f"       -> {new.canonical_path}")
        print(f"    class: {rename_class}")
    print()
    print(f"Canonical replacement pairs: {len(replacements)}")
    if shorthand_preview:
        print(f"Governed shorthand pairs (Class B): {len(shorthand_preview)}")
    if args.plan:
        for old, new in replacements:
            print(f"  [canonical] '{old}' -> '{new}'")
        for old, new in shorthand_preview:
            print(f"  [shorthand] '{old}' -> '{new}'")
        print()
        print("Affected files:")
        for path in affected:
            print(f"  {path.relative_to(ROOT).as_posix()}")
    else:
        print(f"Affected files: {len(affected)}")
    print()

    if not args.apply:
        print("Dry-run complete. Re-run with --apply --yes to execute.")
        return 0

    # Apply disk renames
    for old, new, _ in plan:
        _apply_entry_rename_on_disk(old, new)

    # Update name tables
    tier = request["tier"]
    if tier == "30-1050":
        table_10 = load_table(TABLE_10_50)
        table_30 = load_table(TABLE_30)
        old_10, new_10, _ = plan[0]
        old_30, new_30, _ = plan[1]
        _update_table_entry(table_10, old_10.entry_id, new_10)
        _update_table_entry(table_30, old_30.entry_id, new_30)
        save_table(TABLE_10_50, table_10)
        save_table(TABLE_30, table_30)
    else:
        table_path = _table_path_for_tier(tier)
        table = load_table(table_path)
        old, new, _ = plan[0]
        _update_table_entry(table, old.entry_id, new)
        save_table(table_path, table)

    content_changed = _apply_content_updates(affected, replacements, plan)

    log_dir = ROOT / "archive" / "refactors"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"IDENTITY_RENAME_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%M%S')}.md"
    with log_file.open("w", encoding="utf-8") as lf:
        lf.write("# Identity Rename Log\n\n")
        lf.write(f"Date: {datetime.now(timezone.utc).isoformat()}\n")
        lf.write(f"Request: {request_path.as_posix()}\n")
        lf.write(f"Approved by: {request.get('approved_by', 'unspecified')}\n\n")
        lf.write("## Changes\n")
        for old, new, rename_class in plan:
            lf.write(f"- `{old.canonical_path}` → `{new.canonical_path}` (class {rename_class})\n")
        lf.write(f"\n## Content files updated: {content_changed}\n")
        for path in affected:
            lf.write(f"- `{path.relative_to(ROOT).as_posix()}`\n")
        lf.write("\n## Next steps\n")
        lf.write("- Run full pre-PR validation suite (CONTRIBUTING_CHANGE_WORKFLOW.md)\n")
        lf.write("- Run validate_name_tables.py\n")

    print(f"Applied {len(plan)} identity rename(s).")
    print(f"Content files updated: {content_changed}")
    print(f"Log: {log_file.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())