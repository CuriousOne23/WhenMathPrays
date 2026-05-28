#!/usr/bin/env python3
"""Validate that links in thought_simulator README files resolve to real paths.

Checks all README.md files under thought_simulator and fails if a relative link
points to a missing file or directory.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote
import re


ROOT = Path(__file__).resolve().parents[1]
README_NAME = "README.md"
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _iter_readmes(root: Path):
    for path in root.rglob(README_NAME):
        if path.is_file():
            yield path


def _is_external(target: str) -> bool:
    lowered = target.lower()
    return (
        lowered.startswith("http://")
        or lowered.startswith("https://")
        or lowered.startswith("mailto:")
        or lowered.startswith("tel:")
        or lowered.startswith("file://")
    )


def _normalize_target(raw_target: str) -> str:
    stripped = raw_target.strip()
    if not stripped:
        return ""
    target = stripped.split("#", 1)[0]
    target = target.split("?", 1)[0]
    return unquote(target.strip())


def _check_readme(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    rel_readme = path.relative_to(ROOT).as_posix()
    violations: list[str] = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in LINK_PATTERN.finditer(line):
            raw_target = match.group(1)
            if _is_external(raw_target):
                continue

            normalized = _normalize_target(raw_target)
            if not normalized or normalized.startswith("#"):
                continue

            candidate = (path.parent / normalized).resolve()

            try:
                candidate.relative_to(ROOT)
            except ValueError:
                violations.append(
                    f"{rel_readme}:{line_number}: link '{raw_target}' resolves outside thought_simulator"
                )
                continue

            if not candidate.exists():
                violations.append(
                    f"{rel_readme}:{line_number}: link '{raw_target}' points to missing path '{candidate.relative_to(ROOT).as_posix()}'"
                )

    return violations


def main() -> int:
    violations: list[str] = []
    for readme in _iter_readmes(ROOT):
        violations.extend(_check_readme(readme))

    if violations:
        print("README link validation failed:")
        for item in violations:
            print(f"- {item}")
        return 1

    print("README link validation passed: all README links resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
