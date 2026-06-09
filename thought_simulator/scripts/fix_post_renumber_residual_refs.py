#!/usr/bin/env python3
"""Repair cascade corruption and residual stale refs after phased renumber migrations.

Run after apply_*_renumber_migration.py and tier fix_*_post_renumber_refs.py scripts.
Re-runnable; extend CASCADE_REPAIRS when future bulk renames leave substring artifacts.

Normative pipeline position: 00.00.43 §11.2 step 5. Governance history: naming_strategy_target.md §8.
Manifest-driven pairs are rebuilt from JSON on each run (manifests are read-only; this script skips 00_identity/).
Future renames need manifest approval plus any new cascade rows (same pattern as fix_40_post_renumber_refs.py).
"""

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
    build_40_entry,
    build_50_entry,
    identity_replacement_pairs,
)

SKIP_DIRS = frozenset({"archive", "__pycache__", ".git", "node_modules", "00_identity"})
EXTENSIONS = {".md", ".py", ".json", ".yml"}
MANIFEST_30_1050 = IDENTITY_DIR / "30_1050_renumber_manifest.json"
MANIFEST_50 = IDENTITY_DIR / "50_renumber_manifest.json"
MANIFEST_40 = IDENTITY_DIR / "40_renumber_manifest.json"
INVENTORY = ROOT / "30_verification/30.01_verification_inventory_index.md"
GLOSSARY_VALIDATOR = ROOT / "scripts/validate_glossary_alignment.py"
TIER_50_PREFIX = "50_thought_simulator_design/"
PLAYGROUND_EXEMPT = f"{TIER_50_PREFIX}50.05_software_spec_construction_guide.md"

# Substring-collision and intermediate-band repairs (longest token first).
CASCADE_REPAIRS: list[tuple[str, str]] = [
    # 30 module dirs — wrong intermediate bands from partial replace
    ("30.220_inb_prototypes", "30.50_inb_prototypes"),
    ("30.230_iiinb_prototypes", "30.60_iiinb_prototypes"),
    ("30.240_replay_prototypes", "30.70_replay_prototypes"),
    ("30.250_usp_prototypes", "30.80_usp_prototypes"),
    ("30.260_upi_prototypes", "30.90_upi_prototypes"),
    ("30.220_cob_prototypes", "30.100_cob_prototypes"),
    ("LLR-30.2700-", "LLR-30.100-"),
    # 10.50 files — old W1/W2 bands (slug-qualified; avoids 10.50.220_regulator)
    ("10.50.220_inb_design_requirements", "10.50.50_inb_design_requirements"),
    ("10.50.230_iiinb_design_requirements", "10.50.60_iiinb_design_requirements"),
    ("10.50.240_replay_design_requirements", "10.50.70_replay_design_requirements"),
    ("10.50.220_cob_requirements", "10.50.100_cob_requirements"),
    ("10.50.250_usp_design_requirements", "10.50.80_usp_design_requirements"),
    ("10.50.250_cil_requirements", "10.50.110_cil_requirements"),
    ("10.50.43_gb_design_requirements", "10.50.130_gb_design_requirements"),
    ("10.50.42_core_data_structs_design_requirements", "10.50.140_core_data_structs_design_requirements"),
    ("10.50.1500_mb_design_requirements", "10.50.200_mb_design_requirements"),
    ("# 10.50.1500_mb_design_requirements.md", "# 10.50.200_mb_design_requirements.md"),
    ("Document ID:** 10.50.1500", "Document ID:** 10.50.200"),
    ("Document ID: 10.50.1500", "Document ID: 10.50.200"),
    ("HLR-10.50.1500-", "HLR-10.50.200-"),
    ("HLR-10.50.43-", "HLR-10.50.130-"),
    ("HLR-10.50.42-", "HLR-10.50.140-"),
    # 50 design files — old pre-alignment names
    ("50.1500_mb_design_spec", "50.200_mb_design_spec"),
    ("50.170_tp_design", "50.150_tp_design"),
    ("50.42_core_data_structs_design_spec", "50.140_core_data_structs_design_spec"),
    ("50.43_gb_design_spec", "50.130_gb_design_spec"),
    ("50.250_cil_design_support", "50.110_cil_design_support"),
    ("LLR-50.2700-", "LLR-50.90-"),
    # Glossary band migration (30.160 → 30.30)
    ("30.160_verification_glossary", "30.30_verification_glossary"),
    # Root README — pre-50_design 10.x anchors
    ("10_thought_simulator_req/10.20_tp_requirements.md", "10_thought_simulator_req/50_design/10.50.150_tp_requirements.md"),
    ("10_thought_simulator_req/50_design/10.50.160_basin_requirements.md", "10_thought_simulator_req/50_design/10.50.160_basin_requirements.md"),
    ("10_thought_simulator_req/10.40_scheduler_requirements.md", "10_thought_simulator_req/50_design/10.50.210_scheduler_requirements.md"),
    ("RENAMING_MIGRATION_REPORT.md", "archive/refactors/RENAMING_MIGRATION_REPORT.md"),
    # Historical execution logs
    ("thought_simulator/50_thought_simulator_design/50.170_tp_design.md", "thought_simulator/50_thought_simulator_design/50.150_tp_design.md"),
    ("thought_simulator/30_verification/30.160_verification_glossary.md", "thought_simulator/30_verification/30.30_verification_glossary.md"),
]

# HLR band repairs where old/new bands collide across modules (path-scoped).
FILE_SCOPED_HLR_REPAIRS: list[tuple[tuple[str, ...], str, str]] = [
    (("inb",), "HLR-10.50.220-", "HLR-10.50.50-"),
    (("iiinb",), "HLR-10.50.230-", "HLR-10.50.60-"),
    (("replay",), "HLR-10.50.240-", "HLR-10.50.70-"),
    (("usp", "core_data_structs"), "HLR-10.50.250-", "HLR-10.50.80-"),
]

# 30.01 inventory note peer-band corrections (explicit 10.50.xx in Notes column).
INVENTORY_NOTE_REPAIRS: list[tuple[str, str]] = [
    ("30.50_inb_prototypes", "10.50.220"),
    ("30.60_iiinb_prototypes", "10.50.230"),
    ("30.100_cob_prototypes", "10.50.220"),
    ("30.110_cil_prototypes", "10.50.250"),
    ("30.130_gb_prototypes", "10.50.43"),
    ("30.140_core_data_structs_prototypes", "10.50.42"),
]

# Internal document-band repairs inside renamed 50-series files (filename-scoped).
FILE_SPECIFIC_REPAIRS: dict[str, list[tuple[str, str]]] = {
    "50_thought_simulator_design/50.50_inb_design_spec.md": [
        ("LLR-50.220-", "LLR-50.50-"),
        ("# 50.220 InB Design Specification", "# 50.50 InB Design Specification"),
        ("Document ID:** 50.220", "Document ID:** 50.50"),
        ("CP 50.220", "CP 50.50"),
        ("50.220 /", "50.50 /"),
        ("10.50.220 →", "10.50.50 →"),
        ("10.50.230.", "10.50.60."),
    ],
    "50_thought_simulator_design/50.60_iiinb_design_spec.md": [
        ("LLR-50.230-", "LLR-50.60-"),
        ("# 50.230 IIInB Design Specification", "# 50.60 IIInB Design Specification"),
        ("Document ID:** 50.230", "Document ID:** 50.60"),
        ("CP 50.230", "CP 50.60"),
        ("50.230 /", "50.60 /"),
        ("30.230", "30.60"),
        ("40.230", "40.60"),
        ("10.50.230", "10.50.60"),
        ("50.230", "50.60"),
    ],
    "50_thought_simulator_design/50.100_cob_design_support.md": [
        ("LLR-50.220-", "LLR-50.100-"),
        ("# 50.100_COB Design Support", "# 50.100 COB Design Support"),
    ],
    "50_thought_simulator_design/50.110_cil_design_support.md": [
        ("LLR-50.250-", "LLR-50.110-"),
        ("# 50.250_CIL Design Support", "# 50.110 CIL Design Support"),
        ("updates to 10.50.250,", "updates to 10.50.110,"),
    ],
    "50_thought_simulator_design/50.70_replay_design_spec.md": [
        ("10.50.220 and 10.50.230", "10.50.50 and 10.50.60"),
        ("30.220/30.230", "30.50/30.60"),
        ("[10.50.220]", "[10.50.50]"),
        ("[10.50.230]", "[10.50.60]"),
    ],
    "50_thought_simulator_design/50.80_usp_design_spec.md": [
        ("[50.230](50.60_iiinb_design_spec.md)", "[50.60](50.60_iiinb_design_spec.md)"),
        ("Synchronized with 10.50.250,", "Synchronized with 10.50.80,"),
        ("30.250,", "30.80,"),
    ],
    "30_verification/W2_conversation_layer_wave_coverage_note.md": [
        ("[50.230](../50_thought_simulator_design/50.60_iiinb_design_spec.md)", "[50.60](../50_thought_simulator_design/50.60_iiinb_design_spec.md)"),
        ("10.50.42 ", "10.50.140 "),
    ],
    "30_verification/30.140_core_data_structs_prototypes/30.140_core_data_structs_prototypes_verification_capsule.md": [
        ("10.50.42 +", "10.50.140 +"),
        ("10.50.42_core_data_structs_design_requirements.md", "10.50.140_core_data_structs_design_requirements.md"),
    ],
}

INVENTORY_NOTE_TARGETS: dict[str, str] = {
    "30.50_inb_prototypes": "10.50.50",
    "30.60_iiinb_prototypes": "10.50.60",
    "30.100_cob_prototypes": "10.50.100",
    "30.110_cil_prototypes": "10.50.110",
    "30.130_gb_prototypes": "10.50.130",
    "30.140_core_data_structs_prototypes": "10.50.140",
}


def _dedupe_pairs(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    seen: set[tuple[str, str]] = set()
    out: list[tuple[str, str]] = []
    for pair in pairs:
        if pair not in seen and pair[0] != pair[1]:
            seen.add(pair)
            out.append(pair)
    return out


def _load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _pairs_from_30_1050_manifest(manifest: dict) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for item in manifest["pair_renames"]:
        old_1050 = build_10_50_entry(f"{item['entry_id_1050']}.md")
        old_30 = build_30_entry(item["entry_id_30"])
        new_1050 = build_10_50_entry(f"10.50.{item['new_band']}_{old_1050.slug}.md")
        new_30 = build_30_entry(f"30.{item['new_band']}_{old_30.slug}", paired_10_50=new_1050.entry_id)
        pairs.extend(identity_replacement_pairs(old_1050, new_1050, rename_class="B"))
        pairs.extend(identity_replacement_pairs(old_30, new_30, rename_class="B"))
        for prefix in ("thought_simulator/", "../", "../../"):
            pairs.append((f"{prefix}{old_30.canonical_path}/", f"{prefix}{new_30.canonical_path}/"))
            pairs.append((f"{prefix}{old_30.canonical_path}", f"{prefix}{new_30.canonical_path}"))
            pairs.append((f"{prefix}{old_1050.canonical_path}", f"{prefix}{new_1050.canonical_path}"))
    return pairs


def _pairs_from_50_manifest(manifest: dict) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for item in manifest["file_renames"]:
        old = build_50_entry(f"{item['entry_id']}.md")
        new = build_50_entry(f"50.{item['new_band']}_{old.slug}.md")
        pairs.extend(identity_replacement_pairs(old, new, rename_class="B"))
    return pairs


def _pairs_from_40_manifest(manifest: dict) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    guide = manifest.get("guide_rename")
    if guide:
        pairs.append((guide["old"], guide["new"]))
        pairs.append(
            (
                f"40_thought_simulator_playground/{guide['old']}",
                f"40_thought_simulator_playground/{guide['new']}",
            )
        )
    for item in manifest.get("survivor_renames", []):
        old = build_40_entry(item["entry_id"])
        new = build_40_entry(item["result"])
        pairs.extend(identity_replacement_pairs(old, new, rename_class="B"))
    return pairs


def _collect_all_pairs() -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = list(CASCADE_REPAIRS)
    if MANIFEST_30_1050.is_file():
        pairs.extend(_pairs_from_30_1050_manifest(_load_json(MANIFEST_30_1050)))
    if MANIFEST_50.is_file():
        pairs.extend(_pairs_from_50_manifest(_load_json(MANIFEST_50)))
    if MANIFEST_40.is_file():
        pairs.extend(_pairs_from_40_manifest(_load_json(MANIFEST_40)))
    return _dedupe_pairs(pairs)


def _apply_pairs_to_text(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def _apply_file_scoped_hlr(rel_path: str, text: str) -> str:
    lowered = rel_path.casefold()
    for markers, old, new in FILE_SCOPED_HLR_REPAIRS:
        if any(marker in lowered for marker in markers):
            if "event_log" in lowered and "usp" not in lowered:
                continue
            text = text.replace(old, new)
    return text


def _strip_50_playground_paths(rel_path: str, text: str) -> str:
    if not rel_path.startswith(TIER_50_PREFIX) or rel_path == PLAYGROUND_EXEMPT:
        return text
    return text.replace("40_thought_simulator_playground/", "")


def _fix_glossary_validator() -> bool:
    if not GLOSSARY_VALIDATOR.is_file():
        return False
    text = GLOSSARY_VALIDATOR.read_text(encoding="utf-8")
    updated = text.replace(
        '"30_verification" / "30.160_verification_glossary.md"',
        '"30_verification" / "30.30_verification_glossary.md"',
    )
    if updated == text:
        return False
    GLOSSARY_VALIDATOR.write_text(updated, encoding="utf-8")
    print(GLOSSARY_VALIDATOR.relative_to(ROOT).as_posix())
    return True


def _fix_inventory_notes() -> bool:
    if not INVENTORY.is_file():
        return False
    text = INVENTORY.read_text(encoding="utf-8")
    original = text
    for entry_id, old_peer in INVENTORY_NOTE_REPAIRS:
        new_peer = INVENTORY_NOTE_TARGETS[entry_id]
        text = re.sub(
            rf"(\[`{re.escape(entry_id)}/`\][^\n]*\|[^\n]*\|[^\n]*\|[^\n]*\|[^\n]*{re.escape(old_peer)})",
            lambda m: m.group(1).replace(old_peer, new_peer),
            text,
        )
        # Fallback: replace peer token in row containing module link
        row_pattern = rf"(\[{entry_id}/\][^\n]*{re.escape(old_peer)})"
        text = re.sub(row_pattern, lambda m: m.group(1).replace(old_peer, new_peer), text)
    if text == original:
        return False
    INVENTORY.write_text(text, encoding="utf-8")
    print(INVENTORY.relative_to(ROOT).as_posix())
    return True


def main() -> int:
    pairs = _collect_all_pairs()
    changed = 0

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in EXTENSIONS:
            continue
        if path.name == Path(__file__).name:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue

        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        original = text
        text = _apply_pairs_to_text(text, pairs)
        if rel in FILE_SPECIFIC_REPAIRS:
            text = _apply_pairs_to_text(text, FILE_SPECIFIC_REPAIRS[rel])
        text = _apply_file_scoped_hlr(rel, text)
        text = _strip_50_playground_paths(rel, text)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(rel)

    if _fix_glossary_validator():
        changed += 1
    if _fix_inventory_notes():
        changed += 1

    print(f"Residual ref fix complete: {changed} files updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())