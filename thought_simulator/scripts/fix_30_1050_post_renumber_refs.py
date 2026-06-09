#!/usr/bin/env python3
"""Fix protected-governance and residual references after Phase-2 10.50+30 renumber."""

from __future__ import annotations

import json
import re
from pathlib import Path

from identity_tables import (
    IDENTITY_DIR,
    ROOT,
    IdentityEntry,
    build_10_50_entry,
    build_30_entry,
    identity_replacement_pairs,
)

MANIFEST = IDENTITY_DIR / "30_1050_renumber_manifest.json"
INVENTORY = ROOT / "30_verification/30.01_verification_inventory_index.md"
SKIP_DIRS = frozenset({"archive", "__pycache__", ".git", "node_modules", "00_identity"})
EXTENSIONS = {".md", ".py"}

# Cascade repairs from an earlier unsafe prefix replace (30.20_ -> 30.150_ hit 30.200_*).
CASCADE_REPAIRS: list[tuple[str, str]] = [
    ("30.1500_mb_prototypes", "30.200_mb_prototypes"),
    ("10.50.1500_mb_design_requirements", "10.50.200_mb_design_requirements"),
    ("10.50.1505_", "10.50.205_"),
]

# Status/notes preserved from pre-renumber inventory (keyed by post-renumber entry_id).
MODULE_META: dict[str, tuple[str, str]] = {
    "30.50_inb_prototypes": ("approved", "W1 GATE-A 2026-06-08; CP approved; 40.50 16/16; 10.50.50"),
    "30.60_iiinb_prototypes": ("approved", "W1 GATE-A + W2 024b 24/24 2026-06-08; CP approved; 10.50.60"),
    "30.70_replay_prototypes": ("approved", "W1 GATE-A 2026-06-08; CP approved; 40.70 18/18; 10.50.70"),
    "30.80_usp_prototypes": ("approved", "W2 GATE-B 8/8 2026-06-08; CP 30.00 approved; 10.50.80"),
    "30.90_upi_prototypes": ("approved", "W2 GATE-B 8/8 2026-06-08; CP 30.00 approved; 10.50.90"),
    "30.100_cob_prototypes": ("promoted", "W2 extension 4/4 USP pin 2026-06-08; 10.50.100"),
    "30.110_cil_prototypes": ("promoted", "W2 extension 4/4 clarification wire 2026-06-08; 10.50.110"),
    "30.120_cop_prototypes": ("seeded", ""),
    "30.130_gb_prototypes": ("promoted", "W2 extension 4/4 UPI governance 2026-06-08; 10.50.130"),
    "30.140_core_data_structs_prototypes": ("approved", "W2 GATE-B 8/8 2026-06-08; CP 30.00 approved; 10.50.140"),
    "30.150_tp_lifecycle": ("seeded", ""),
    "30.160_basin_prototypes": ("seeded", ""),
    "30.170_ib_prototypes": ("seeded", ""),
    "30.180_tr_prototypes": ("seeded", ""),
    "30.190_dcb_stability_prototypes": ("seeded", "scaffold"),
    "30.200_mb_prototypes": ("seeded", ""),
    "30.210_scheduler_prototypes": ("promoted", "40.270 Phase B 2026-06-06"),
    "30.220_regulator_prototypes": ("promoted", "40.320 Phase B 2026-06-06"),
    "30.230_tick_cycle_skeleton": ("seeded", ""),
    "30.240_snapshot_prototypes": ("seeded", ""),
    "30.250_event_log_prototypes": ("seeded", ""),
    "30.260_experiment_runner": ("seeded", ""),
    "30.270_math_prototypes": ("seeded", ""),
}

DELTA_OVERRIDES = {
    "30.130_gb_prototypes": "30.130_gb_requirements_delta.md",
    "30.180_tr_prototypes": "30.180_tr_requirements_delta.md",
}


def _load_manifest() -> dict:
    with MANIFEST.open(encoding="utf-8") as fh:
        return json.load(fh)


def _compute_10_50_entry(old: IdentityEntry, new_band: str) -> IdentityEntry:
    return build_10_50_entry(f"10.50.{new_band}_{old.slug}.md")


def _compute_30_entry(old: IdentityEntry, new_band: str, paired_1050: str) -> IdentityEntry:
    return build_30_entry(f"30.{new_band}_{old.slug}", paired_10_50=paired_1050)


def _build_plan(manifest: dict) -> list[tuple[IdentityEntry, IdentityEntry, IdentityEntry, IdentityEntry]]:
    plan: list[tuple[IdentityEntry, IdentityEntry, IdentityEntry, IdentityEntry]] = []
    for item in manifest["pair_renames"]:
        old_1050 = build_10_50_entry(f"{item['entry_id_1050']}.md")
        old_30 = build_30_entry(item["entry_id_30"])
        new_1050 = _compute_10_50_entry(old_1050, item["new_band"])
        new_30 = _compute_30_entry(old_30, item["new_band"], new_1050.entry_id)
        plan.append((old_1050, new_1050, old_30, new_30))
    return plan


def _dedupe_pairs(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    seen: set[tuple[str, str]] = set()
    out: list[tuple[str, str]] = []
    for pair in pairs:
        if pair not in seen:
            seen.add(pair)
            out.append(pair)
    return out


def _collect_fix_pairs(plan: list[tuple[IdentityEntry, IdentityEntry, IdentityEntry, IdentityEntry]]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = list(CASCADE_REPAIRS)
    pairs.append(
        (
            "30.392_core_data_structs_prototypes",
            "30.140_core_data_structs_prototypes",
        )
    )
    pairs.append(
        (
            "10.50.392_core_data_structs_design_requirements.md",
            "10.50.140_core_data_structs_design_requirements.md",
        )
    )

    for old_1050, new_1050, old_30, new_30 in plan:
        pairs.extend(identity_replacement_pairs(old_1050, new_1050, rename_class="B"))
        pairs.extend(identity_replacement_pairs(old_30, new_30, rename_class="B"))
        for prefix in ("thought_simulator/", "../"):
            pairs.append(
                (f"{prefix}{old_30.canonical_path}/", f"{prefix}{new_30.canonical_path}/")
            )
            pairs.append(
                (f"{prefix}{old_30.canonical_path}", f"{prefix}{new_30.canonical_path}")
            )
            pairs.append(
                (
                    f"{prefix}{old_1050.canonical_path}",
                    f"{prefix}{new_1050.canonical_path}",
                )
            )

    return _dedupe_pairs(pairs)


def _delta_name(entry_id: str) -> str:
    if entry_id in DELTA_OVERRIDES:
        return DELTA_OVERRIDES[entry_id]
    return f"{entry_id}_requirements_delta.md"


def _inventory_row(entry_id: str) -> str:
    status, notes = MODULE_META[entry_id]
    notes_cell = notes if notes else ""
    return (
        f"| [{entry_id}/]({entry_id}/) "
        f"| `{entry_id}_verification_capsule.md` "
        f"| `{_delta_name(entry_id)}` "
        f"| {status} | {notes_cell} |"
    )


def _rebuild_inventory_table() -> None:
    rows = [_inventory_row(eid) for eid in sorted(MODULE_META, key=lambda s: int(s.split(".")[1].split("_")[0]))]
    table = "\n".join(rows) + "\n"
    text = INVENTORY.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(\| Module path \| Verification capsule \| Requirements delta \| Status \| Notes \|\n"
        r"\|[-| ]+\|\n)(.*?)(\nWave coverage:)",
        re.DOTALL,
    )
    if not pattern.search(text):
        raise RuntimeError("could not locate module inventory table in 30.01")
    updated = pattern.sub(rf"\1{table}\3", text)
    INVENTORY.write_text(updated, encoding="utf-8")
    print(INVENTORY.relative_to(ROOT).as_posix())


def main() -> int:
    manifest = _load_manifest()
    plan = _build_plan(manifest)
    fixes = _collect_fix_pairs(plan)

    changed = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in EXTENSIONS:
            continue
        if path.name == Path(__file__).name:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue

        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in fixes:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(path.relative_to(ROOT).as_posix())

    _rebuild_inventory_table()
    changed += 1
    print(f"Fixed {changed} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())