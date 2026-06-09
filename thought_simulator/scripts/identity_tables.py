#!/usr/bin/env python3
"""Shared identity name-table utilities for controlled rename operations."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "identity_name_table_v1"
ROOT = Path(__file__).resolve().parents[1]
IDENTITY_DIR = ROOT / "00_program_governance" / "00_identity"

TABLE_40 = IDENTITY_DIR / "40_name_table.json"
TABLE_10_50 = IDENTITY_DIR / "10.50_name_table.json"
TABLE_30 = IDENTITY_DIR / "30_name_table.json"
TABLE_50 = IDENTITY_DIR / "50_name_table.json"

TIER_40_BASE = "40_thought_simulator_playground"
TIER_10_50_BASE = "10_thought_simulator_req/50_design"
TIER_30_BASE = "30_verification"
TIER_50_BASE = "50_thought_simulator_design"

GOVERNANCE_BAND_50 = frozenset(range(0, 10))  # 50.00–50.09

MODULE_40_RE = re.compile(r"^(40\.(?:\d+\.)*\d+)_(.+)$")
MODULE_30_RE = re.compile(r"^(30\.(?:\d+\.)*\d+)_(.+)$")
FILE_10_50_RE = re.compile(r"^(10\.50\.(?:\d+\.)*\d+)_(.+)\.md$")
FILE_50_RE = re.compile(r"^(50\.(?:\d+\.)*\d+)_(.+)\.md$")
FILE_50_LEVEL2_RE = re.compile(r"^(50\.(?:\d+\.)+\d+)_(.+)\.md$")


@dataclass(frozen=True)
class IdentityEntry:
    entry_id: str
    band: str
    slug: str
    kind: str
    canonical_name: str
    canonical_path: str
    paired_entry_id: str | None = None
    aliases: tuple[str, ...] = ()
    children: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "entry_id": self.entry_id,
            "band": self.band,
            "slug": self.slug,
            "kind": self.kind,
            "canonical_name": self.canonical_name,
            "canonical_path": self.canonical_path,
            "aliases": list(self.aliases),
        }
        if self.paired_entry_id:
            data["paired_entry_id"] = self.paired_entry_id
        if self.children:
            data["children"] = list(self.children)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IdentityEntry:
        return cls(
            entry_id=data["entry_id"],
            band=data["band"],
            slug=data["slug"],
            kind=data["kind"],
            canonical_name=data["canonical_name"],
            canonical_path=data["canonical_path"],
            paired_entry_id=data.get("paired_entry_id"),
            aliases=tuple(data.get("aliases", [])),
            children=tuple(data.get("children", [])),
        )


def load_table(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def save_table(path: Path, table: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(table, fh, indent=2, sort_keys=True)
        fh.write("\n")


def entries_by_id(table: dict[str, Any]) -> dict[str, IdentityEntry]:
    return {e["entry_id"]: IdentityEntry.from_dict(e) for e in table.get("entries", [])}


def parse_band(entry_id: str) -> str:
    """Return numeric band from entry_id (e.g. 10.50.392 -> 392, 50.36.10 -> 36.10)."""
    if entry_id.startswith("10.50."):
        return entry_id.removeprefix("10.50.")
    if entry_id.startswith("30."):
        return entry_id.removeprefix("30.")
    if entry_id.startswith("40."):
        return entry_id.removeprefix("40.")
    if entry_id.startswith("50."):
        return entry_id.removeprefix("50.")
    raise ValueError(f"cannot parse band from entry_id: {entry_id}")


def is_50_governance_file(name: str) -> bool:
    match = re.match(r"^50\.(\d+)_", name)
    if not match:
        return False
    primary = int(match.group(1))
    return primary in GOVERNANCE_BAND_50 and "." not in match.group(0).split("_", 1)[0].replace("50.", "", 1)


def is_50_level1_component_file(name: str) -> bool:
    if not name.endswith(".md"):
        return False
    if is_50_governance_file(name):
        return False
    match = FILE_50_RE.match(name)
    if not match:
        return False
    prefix = match.group(1)
    # level-2 has more than one dot after 50 (e.g. 50.36.10)
    parts = prefix.split(".")
    return len(parts) == 2  # 50 + band


def build_40_entry(dir_name: str) -> IdentityEntry:
    match = MODULE_40_RE.match(dir_name)
    if not match:
        raise ValueError(f"invalid 40 module dir name: {dir_name}")
    band_prefix = match.group(1)
    slug = match.group(2)
    entry_id = dir_name
    return IdentityEntry(
        entry_id=entry_id,
        band=parse_band(band_prefix),
        slug=slug,
        kind="module_folder",
        canonical_name=dir_name,
        canonical_path=f"{TIER_40_BASE}/{dir_name}",
    )


def build_10_50_entry(filename: str) -> IdentityEntry:
    match = FILE_10_50_RE.match(filename)
    if not match:
        raise ValueError(f"invalid 10.50 filename: {filename}")
    band_prefix = match.group(1)
    slug = match.group(2)
    entry_id = filename.removesuffix(".md")
    return IdentityEntry(
        entry_id=entry_id,
        band=parse_band(band_prefix),
        slug=slug,
        kind="design_requirements_file",
        canonical_name=filename,
        canonical_path=f"{TIER_10_50_BASE}/{filename}",
    )


def build_30_entry(dir_name: str, paired_10_50: str | None = None) -> IdentityEntry:
    match = MODULE_30_RE.match(dir_name)
    if not match:
        raise ValueError(f"invalid 30 module dir name: {dir_name}")
    band_prefix = match.group(1)
    slug = match.group(2)
    entry_id = dir_name
    return IdentityEntry(
        entry_id=entry_id,
        band=parse_band(band_prefix),
        slug=slug,
        kind="verification_module_folder",
        canonical_name=dir_name,
        canonical_path=f"{TIER_30_BASE}/{dir_name}",
        paired_entry_id=paired_10_50,
    )


def build_50_entry(filename: str, children: tuple[str, ...] = ()) -> IdentityEntry:
    match = FILE_50_RE.match(filename)
    if not match:
        raise ValueError(f"invalid 50 filename: {filename}")
    band_prefix = match.group(1)
    slug = match.group(2)
    entry_id = filename.removesuffix(".md")
    kind = "level_1_design_file" if is_50_level1_component_file(filename) else "level_2_design_file"
    return IdentityEntry(
        entry_id=entry_id,
        band=parse_band(band_prefix),
        slug=slug,
        kind=kind,
        canonical_name=filename,
        canonical_path=f"{TIER_50_BASE}/{filename}",
        children=children,
    )


def bootstrap_all_tables() -> dict[str, dict[str, Any]]:
    """Scan disk and build fresh name tables from current filesystem state."""
    entries_40: list[IdentityEntry] = []
    playground = ROOT / TIER_40_BASE
    for path in sorted(playground.iterdir()):
        if path.is_dir() and path.name.startswith("40."):
            entries_40.append(build_40_entry(path.name))

    entries_10_50: list[IdentityEntry] = []
    ten_fifty_dir = ROOT / TIER_10_50_BASE
    for path in sorted(ten_fifty_dir.glob("10.50.*.md")):
        entries_10_50.append(build_10_50_entry(path.name))

    ten_fifty_by_band: dict[str, str] = {}
    for e in entries_10_50:
        ten_fifty_by_band.setdefault(e.band, e.entry_id)

    entries_30: list[IdentityEntry] = []
    thirty_dir = ROOT / TIER_30_BASE
    for path in sorted(thirty_dir.iterdir()):
        if path.is_dir() and path.name.startswith("30.") and path.name != "30.tb":
            band = parse_band(path.name.split("_", 1)[0].replace("30.", "30.", 1))
            # band from dir: 30.392_core... -> entry_id 30.392
            entry_id = path.name.split("_", 1)[0]
            band_key = entry_id.removeprefix("30.")
            paired = ten_fifty_by_band.get(band_key)
            entries_30.append(build_30_entry(path.name, paired_10_50=paired))

    # Pair 10.50 -> 30
    thirty_by_band: dict[str, str] = {}
    for e in entries_30:
        thirty_by_band.setdefault(e.band, e.entry_id)
    entries_10_50_paired: list[IdentityEntry] = []
    for entry in entries_10_50:
        paired_30 = thirty_by_band.get(entry.band)
        entries_10_50_paired.append(
            IdentityEntry(
                entry_id=entry.entry_id,
                band=entry.band,
                slug=entry.slug,
                kind=entry.kind,
                canonical_name=entry.canonical_name,
                canonical_path=entry.canonical_path,
                paired_entry_id=paired_30,
                aliases=entry.aliases,
                children=entry.children,
            )
        )

    entries_50: list[IdentityEntry] = []
    fifty_dir = ROOT / TIER_50_BASE
    level2_by_parent: dict[str, list[str]] = {}
    for path in sorted(fifty_dir.glob("50.*.md")):
        if FILE_50_LEVEL2_RE.match(path.name) and not is_50_level1_component_file(path.name):
            parent = ".".join(path.name.split("_", 1)[0].split(".")[:2])  # 50.36 from 50.36.10
            level2_by_parent.setdefault(parent, []).append(path.name)

    for path in sorted(fifty_dir.glob("50.*.md")):
        if is_50_level1_component_file(path.name):
            entry_id = path.name.split("_", 1)[0]
            children = tuple(sorted(level2_by_parent.get(entry_id, [])))
            entries_50.append(build_50_entry(path.name, children=children))
        elif FILE_50_LEVEL2_RE.match(path.name):
            entries_50.append(build_50_entry(path.name))

    def wrap(tier: str, entries: list[IdentityEntry], note: str) -> dict[str, Any]:
        band_counts: dict[str, int] = {}
        for e in entries:
            band_counts[e.band] = band_counts.get(e.band, 0) + 1
        dict_entries = []
        for e in sorted(entries, key=lambda x: x.entry_id):
            d = e.to_dict()
            d["shorthand_eligible"] = band_counts[e.band] == 1
            dict_entries.append(d)
        return {
            "schema_version": SCHEMA_VERSION,
            "tier": tier,
            "description": note,
            "entries": dict_entries,
        }

    return {
        "40": wrap(
            "40",
            entries_40,
            "Canonical identity registry for 40-series playground module folders.",
        ),
        "10.50": wrap(
            "10.50",
            entries_10_50_paired,
            "Canonical identity registry for 10.50 design-requirements files; paired_entry_id links to 30.",
        ),
        "30": wrap(
            "30",
            entries_30,
            "Derived verification-module registry; band coupling follows 10.50_name_table paired_entry_id.",
        ),
        "50": wrap(
            "50",
            entries_50,
            "Canonical identity registry for 50-series design files (level-1 and level-2).",
        ),
    }


def write_bootstrap_tables() -> None:
    tables = bootstrap_all_tables()
    save_table(TABLE_40, tables["40"])
    save_table(TABLE_10_50, tables["10.50"])
    save_table(TABLE_30, tables["30"])
    save_table(TABLE_50, tables["50"])


def identity_replacement_pairs(
    old_entry: IdentityEntry,
    new_entry: IdentityEntry,
    *,
    rename_class: str,
) -> list[tuple[str, str]]:
    """Build deterministic string replacement pairs for a rename."""
    pairs: list[tuple[str, str]] = []

    def add(old: str, new: str) -> None:
        if old and new and old != new:
            pairs.append((old, new))

    add(old_entry.canonical_name, new_entry.canonical_name)
    add(old_entry.canonical_path, new_entry.canonical_path)
    add(old_entry.entry_id, new_entry.entry_id)

    # Common path variants used in markdown links
    add(old_entry.canonical_path.replace("/", "\\"), new_entry.canonical_path.replace("/", "\\"))
    if old_entry.canonical_name.endswith(".md"):
        add(old_entry.canonical_name, new_entry.canonical_name)
    else:
        add(f"{old_entry.canonical_name}/", f"{new_entry.canonical_name}/")
        add(f"[{old_entry.canonical_name}/]", f"[{new_entry.canonical_name}/]")
        add(f"({old_entry.canonical_name}/)", f"({new_entry.canonical_name}/)")

    if rename_class == "B" and old_entry.band != new_entry.band:
        old_prefix = old_entry.entry_id
        new_prefix = new_entry.entry_id
        add(f"HLR-{old_prefix}-", f"HLR-{new_prefix}-")
        add(f"LLR-{old_prefix}-", f"LLR-{new_prefix}-")
        add(f"Document ID:** {old_prefix}", f"Document ID:** {new_prefix}")
        add(f"Document ID: {old_prefix}", f"Document ID: {new_prefix}")

    # Dedupe preserving order
    seen: set[tuple[str, str]] = set()
    unique: list[tuple[str, str]] = []
    for pair in pairs:
        if pair not in seen:
            seen.add(pair)
            unique.append(pair)
    return unique