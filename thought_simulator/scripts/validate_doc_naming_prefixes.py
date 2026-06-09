#!/usr/bin/env python3
"""Validate numbered directory/file naming against 00.00.42 prefix convention.

Full alignment (warnings only):
- Organizational subdirs (50_design/, 00_foundations/) are exempt from band-prefix rules.
- 40 tier: validate module subdirectory names only (40.{band}_*/), not files inside modules.
- Other tiers: validate module dirs and numbered markdown files with full subfield depth.
- 10_ tier: 10_system_architecture → 10.10.*, 50_design → 10.50.* (startswith, not exact match).

Does not fail CI (exit 0); reports warnings for human review.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from doc_address import (
    FILE_ADDRESS_RE,
    MODULE_DIR_RE,
    ORGANIZATIONAL_DIRS,
    TEN_SUBSYSTEM_BAND_PREFIX,
    is_organizational_dir,
)

TIER_DIR_RE = re.compile(r"^(\d+)_")
ENFORCED_TIER_PREFIXES = {"00", "10", "20", "30", "40", "50"}


@dataclass
class Issue:
    path: str
    line: int
    message: str


def iter_tier_dirs(root: Path):
    for entry in root.iterdir():
        if entry.is_dir() and TIER_DIR_RE.match(entry.name):
            yield entry


def _tier_major(tier_dir: Path) -> str | None:
    match = TIER_DIR_RE.match(tier_dir.name)
    if not match:
        return None
    return match.group(1)


def _validate_40_subdirectory_level(tier_dir: Path, root: Path) -> list[Issue]:
    """40: check only immediate module directories under the playground tier."""
    issues: list[Issue] = []
    tier_prefix = "40."
    for sub in tier_dir.iterdir():
        if not sub.is_dir():
            continue
        rel = sub.relative_to(root).as_posix()
        if is_organizational_dir(tier_dir.name, sub.name):
            continue
        match = MODULE_DIR_RE.match(sub.name)
        if not match:
            issues.append(
                Issue(
                    path=rel,
                    line=1,
                    message=(
                        f"40 module subdirectory expected form '40.{{band}}_{{slug}}/', got '{sub.name}'"
                    ),
                )
            )
            continue
        if not match.group(1).startswith(tier_prefix):
            issues.append(
                Issue(
                    path=rel,
                    line=1,
                    message=f"40 subdirectory band must start with '{tier_prefix}', got '{match.group(1)}'",
                )
            )
    return issues


def _validate_tier_except_40(tier_dir: Path, root: Path) -> list[Issue]:
    issues: list[Issue] = []
    tier_major = _tier_major(tier_dir)
    if not tier_major or tier_major not in ENFORCED_TIER_PREFIXES:
        return issues
    tier_prefix = f"{tier_major}."

    for sub in tier_dir.iterdir():
        if not sub.is_dir():
            continue
        if is_organizational_dir(tier_dir.name, sub.name):
            continue
        match = MODULE_DIR_RE.match(sub.name)
        if match and not sub.name.startswith(tier_prefix):
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

    for md in tier_dir.rglob("*.md"):
        rel = md.relative_to(root).as_posix()
        if _path_under_organizational(tier_dir.name, rel):
            continue

        name_match = FILE_ADDRESS_RE.match(md.name)
        if not name_match:
            continue

        file_prefix = name_match.group(1)
        if not file_prefix.startswith(tier_prefix.replace(".", "") if tier_major == "10" else tier_prefix):
            if tier_major != "10" and not md.name.startswith(tier_prefix):
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

        parent_name = md.parent.name
        if is_organizational_dir(tier_dir.name, parent_name):
            _check_10_organizational_file(rel, parent_name, file_prefix, issues)
            continue

        parent_match = MODULE_DIR_RE.match(parent_name)
        if parent_match:
            subsystem_prefix = parent_match.group(1)
            if not _address_compatible(subsystem_prefix, file_prefix):
                issues.append(
                    Issue(
                        path=rel,
                        line=1,
                        message=(
                            f"file/subdirectory mismatch: file address '{file_prefix}' does not align "
                            f"with parent module '{subsystem_prefix}'"
                        ),
                    )
                )

        if tier_major == "10":
            _check_10_organizational_file(rel, parent_name, file_prefix, issues)

    return issues


def _path_under_organizational(tier_dir_name: str, rel_path: str) -> bool:
    parts = rel_path.split("/")
    if len(parts) < 2:
        return False
    for part in parts[1:-1]:
        if part in ORGANIZATIONAL_DIRS.get(tier_dir_name, frozenset()):
            return True
    return parts[1] in ORGANIZATIONAL_DIRS.get(tier_dir_name, frozenset())


def _address_compatible(parent: str, child: str) -> bool:
    return child == parent or child.startswith(parent + ".")


def _check_10_organizational_file(rel: str, parent_name: str, file_prefix: str, issues: list[Issue]) -> None:
    expected = TEN_SUBSYSTEM_BAND_PREFIX.get(parent_name)
    if not expected:
        return
    if not (file_prefix == expected or file_prefix.startswith(expected + ".")):
        issues.append(
            Issue(
                path=rel,
                line=1,
                message=(
                    f"file/subdirectory prefix mismatch under 10_ tier: file uses '{file_prefix}' "
                    f"but directory '{parent_name}' expects band prefix '{expected}.*'"
                ),
            )
        )


def validate_tier(tier_dir: Path, root: Path) -> list[Issue]:
    tier_major = _tier_major(tier_dir)
    if not tier_major or tier_major not in ENFORCED_TIER_PREFIXES:
        return []
    if tier_major == "40":
        return _validate_40_subdirectory_level(tier_dir, root)
    return _validate_tier_except_40(tier_dir, root)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    issues: list[Issue] = []

    for tier_dir in iter_tier_dirs(root):
        issues.extend(validate_tier(tier_dir, root))

    if issues:
        print(
            "Naming prefix validation issues (warnings only; organizational dirs and 40 intra-module "
            "files are exempt per 00.00.42):"
        )
        for issue in issues:
            print(f"- {issue.path}:{issue.line}: {issue.message}")
        print("See rename_identity.py (00.00.43 policy) for controlled identity renames.")
        return 0

    print("Naming prefix validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())