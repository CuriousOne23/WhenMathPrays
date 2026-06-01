#!/usr/bin/env python3
"""Validate numbered directory/file naming prefix consistency.

Rules:
- For top-level numbered tiers (e.g. 40_thought_simulator_playground), any immediate
  numbered subsystem directory (e.g. 40.20_tp_lifecycle) must start with the tier
  number prefix ("40.").
- Any markdown filename with a numeric prefix under a tier must start with that tier
  number prefix.
- If a markdown file is inside a numbered subsystem directory and the file itself has
  a numeric prefix, it must match the subsystem prefix exactly.

Files without numeric prefixes are allowed.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


TIER_DIR_RE = re.compile(r"^(\d+)_")
SUBSYSTEM_DIR_RE = re.compile(r"^(\d+\.\d+)_")
FILE_PREFIX_RE = re.compile(r"^(\d+\.\d+)")

# Governance intentionally mixes 00.* and 30.* documents under 00_program_governance,
# so prefix consistency is enforced only for tiers that follow strict numeric alignment.
ENFORCED_TIER_PREFIXES = {"20", "30", "40", "50"}


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

    return issues


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    issues: list[Issue] = []

    for tier_dir in iter_tier_dirs(root):
        issues.extend(validate_tier(tier_dir, root))

    if issues:
        print("Naming prefix validation errors:")
        for issue in issues:
            print(f"- {issue.path}:{issue.line}: {issue.message}")
        return 1

    print("Naming prefix validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
