#!/usr/bin/env python3
"""Validate numbered directory/file naming prefix consistency.

Rules (tier-local only):
- For top-level numbered tiers (e.g. 40_thought_simulator_playground), any immediate
  numbered subsystem directory (e.g. 40.160_tp_lifecycle) must start with the tier
  number prefix ("40.").
- Any markdown filename with a numeric prefix under a tier must start with that tier
  number prefix.
- If a markdown file is inside a numbered subsystem directory and the file itself has
  a numeric prefix, it must match the subsystem prefix exactly.
- Special case for tier 10 (10_thought_simulator_req): subdirs like 10_system_architecture
  require files prefixed 10.10.* ; 50_design requires 10.50.* . This catches misplaced
  numbers such as a 10.50.36 file living in the 10.10 architecture area (should be 10.10.36
  or the design variant under 50_design/).

Files without numeric prefixes are allowed.

NOTE on component numbering independence (as of post-renumber policy):
  - 40, 20, and 50 have standalone/independent naming for their .xx component numbers.
  - Only 30 and 10.50 are required to share the same numeric band (30 names must match
    an existing 10.50 peer; 10.50 comes first as the canonical requirements anchor).
  - Cross-layer component number alignment (previously "uniform .xx across 40/30/10.50/50")
    is no longer required or enforced by this validator. See validate_30_10_50_pairing.py
    for the only remaining cross-tier name rule, and the updated 40.160 / 30.00 / 50.05
    guidance documents.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


TIER_DIR_RE = re.compile(r"^(\d+)_")
# Support arbitrary-depth dotted numeric prefixes for subfield extensions
# (e.g. 20.40, 20.40.010, 20.40.010.005, 50.36.010.020.001, etc.).
# Per 00.00.42 Document Addressing and Insertion Policy. Depth is unlimited.
SUBSYSTEM_DIR_RE = re.compile(r"^(\d+(?:\.\d+)*)_")
FILE_PREFIX_RE = re.compile(r"^(\d+(?:\.\d+)*)")

# Enforce strict tier-prefix alignment for canonical numbered tiers, including
# governance tier 00 now that governance documents are normalized to 00.* prefixes.
ENFORCED_TIER_PREFIXES = {"00", "10", "20", "30", "40", "50"}

# For the special 10_ tier (canonical requirements layer), sub-directories map to
# specific 10.xx prefixes. This prevents e.g. 10.50.36 files from living under
# the 10.10 system architecture docs (they belong under 50_design/ as 10.50.36_*).
TEN_SUBSYSTEM_PREFIX_MAP = {
    "10_system_architecture": "10.10",
    "50_design": "10.50",
    # Add more if 10_ grows additional numbered sub-areas (e.g. 10.20_xxx etc.)
}


@dataclass
class Issue:
    path: str
    line: int
    message: str


def iter_tier_dirs(root: Path):
    for entry in root.iterdir():
        if entry.is_dir() and TIER_DIR_RE.match(entry.name):
            yield entry


def validate_tier(tier_dir: Path, root: Path) -> list[Issue]:
    issues: list[Issue] = []

    tier_match = TIER_DIR_RE.match(tier_dir.name)
    if not tier_match:
        return issues
    tier_major = tier_match.group(1)
    if tier_major not in ENFORCED_TIER_PREFIXES:
        return issues
    tier_prefix = f"{tier_major}."

    # Validate immediate subsystem directory prefixes.
    for sub in tier_dir.iterdir():
        if not sub.is_dir():
            continue
        sm = SUBSYSTEM_DIR_RE.match(sub.name)
        if sm and not sub.name.startswith(tier_prefix):
            issues.append(
                Issue(
                    path=sub.relative_to(root).as_posix(),
                    line=1,
                    message=(
                        f"subdirectory prefix mismatch: expected '{tier_prefix}*' under tier "
                        f"'{tier_dir.name}', got '{sub.name}'"
                    ),
                )
            )

    # Validate markdown filename prefixes recursively.
    for md in tier_dir.rglob("*.md"):
        rel = md.relative_to(root).as_posix()
        name_match = FILE_PREFIX_RE.match(md.name)
        if name_match and not md.name.startswith(tier_prefix):
            issues.append(
                Issue(
                    path=rel,
                    line=1,
                    message=(
                        f"filename prefix mismatch: expected '{tier_prefix}*' under tier "
                        f"'{tier_dir.name}', got '{md.name}'"
                    ),
                )
            )

        # Standard subsystem dir check (for 20/30/40/50 etc.)
        parent_match = SUBSYSTEM_DIR_RE.match(md.parent.name)
        if parent_match and name_match:
            subsystem_prefix = f"{parent_match.group(1)}"
            file_prefix = name_match.group(1)
            if file_prefix != subsystem_prefix:
                issues.append(
                    Issue(
                        path=rel,
                        line=1,
                        message=(
                            f"file/subdirectory mismatch: file prefix '{file_prefix}' does not match "
                            f"parent subsystem prefix '{subsystem_prefix}'"
                        ),
                    )
                )

        # Special handling for 10_ tier's manually organized sub-areas (10_system_architecture etc.)
        # This ensures e.g. a file named 10.50.36_* under 10_system_architecture/ is flagged
        # (it should be 10.10.36_* or live in 50_design/ as 10.50.36_*).
        if tier_major == "10" and name_match:
            subdir_name = md.parent.name
            expected_for_sub = TEN_SUBSYSTEM_PREFIX_MAP.get(subdir_name)
            if expected_for_sub:
                file_prefix = name_match.group(1)
                if file_prefix != expected_for_sub:
                    issues.append(
                        Issue(
                            path=rel,
                            line=1,
                            message=(
                                f"file/subdirectory prefix mismatch under 10_ tier: file uses '{file_prefix}' "
                                f"but directory '{subdir_name}' expects files starting with '{expected_for_sub}' "
                                f"(e.g. use 10.10.36 for architecture-placed GB reqs instead of 10.50.36)"
                            ),
                        )
                    )

    return issues


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    issues: list[Issue] = []

    for tier_dir in iter_tier_dirs(root):
        issues.extend(validate_tier(tier_dir, root))

    if issues:
        print("Naming prefix validation issues (warnings only; no automatic fixes or renames are performed by this script):")
        for issue in issues:
            print(f"- {issue.path}:{issue.line}: {issue.message}")
        print("See rename_identity.py (00.00.43 policy) for controlled identity renames.")
        # Per policy: warnings only. This validator never mutates files and does not fail the process
        # on naming issues (other layers may still treat as blocking via their own rules/CI).
        return 0

    print("Naming prefix validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
