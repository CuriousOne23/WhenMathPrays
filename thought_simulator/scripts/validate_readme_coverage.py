#!/usr/bin/env python3
"""Warn when README directory coverage does not match actual child entries.

This check is non-blocking and complements link validation. It compares each
README.md under thought_simulator to the immediate files/folders in that README's
directory and warns on both missing and extra entries.
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


def _is_ignored_child(path: Path) -> bool:
    name = path.name
    if name == README_NAME:
        return True
    if name.startswith("."):
        return True
    if name == "__pycache__":
        return True
    return False


def _linked_direct_children(readme: Path) -> set[str]:
    text = readme.read_text(encoding="utf-8")
    linked: set[str] = set()

    for line in text.splitlines():
        for match in LINK_PATTERN.finditer(line):
            raw_target = match.group(1)
            if _is_external(raw_target):
                continue
            normalized = _normalize_target(raw_target)
            if not normalized or normalized.startswith("#"):
                continue

            candidate = (readme.parent / normalized).resolve()
            if not candidate.exists():
                continue

            try:
                candidate.relative_to(ROOT)
            except ValueError:
                continue

            if candidate.parent == readme.parent:
                if candidate.name == README_NAME:
                    continue
                linked.add(candidate.name)

    return linked


def _actual_direct_children(readme: Path) -> set[str]:
    items: set[str] = set()
    for child in readme.parent.iterdir():
        if _is_ignored_child(child):
            continue
        items.add(child.name)
    return items


def main() -> int:
    warnings: list[str] = []

    for readme in _iter_readmes(ROOT):
        rel_readme = readme.relative_to(ROOT).as_posix()
        linked = _linked_direct_children(readme)
        actual = _actual_direct_children(readme)

        missing = sorted(actual - linked)
        extra = sorted(linked - actual)

        for item in missing:
            warnings.append(
                f"{rel_readme}: directory child '{item}' is not referenced in README links"
            )
        for item in extra:
            warnings.append(
                f"{rel_readme}: linked child '{item}' does not exist in directory"
            )

    if warnings:
        print("README coverage warnings:")
        for item in warnings:
            print(f"- {item}")
        print("README coverage check completed with warnings (non-blocking).")
        return 0

    print("README coverage check passed: README links match directory children.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
