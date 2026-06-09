#!/usr/bin/env python3
"""Append missing direct-child markdown links to README.md files for coverage alignment."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote
import re

ROOT = Path(__file__).resolve().parents[1]
README_NAME = "README.md"
SECTION_HEADER = "## Directory index (coverage-aligned)"
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _is_ignored_child(path: Path) -> bool:
    name = path.name
    return name == README_NAME or name.startswith(".") or name == "__pycache__"


def _is_external(target: str) -> bool:
    lowered = target.lower()
    return lowered.startswith(("http://", "https://", "mailto:", "tel:", "file://"))


def _normalize_target(raw_target: str) -> str:
    stripped = raw_target.strip()
    if not stripped:
        return ""
    target = stripped.split("#", 1)[0].split("?", 1)[0]
    return unquote(target.strip())


def _linked_direct_children(readme: Path) -> set[str]:
    text = readme.read_text(encoding="utf-8")
    linked: set[str] = set()
    for match in LINK_PATTERN.finditer(text):
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
        if candidate.parent == readme.parent.resolve():
            linked.add(candidate.name)
    return linked


def _missing_children(readme: Path) -> list[Path]:
    linked = _linked_direct_children(readme)
    missing: list[Path] = []
    for child in sorted(readme.parent.iterdir(), key=lambda p: p.name.lower()):
        if _is_ignored_child(child):
            continue
        if child.name not in linked:
            missing.append(child)
    return missing


def _coverage_section_lines(text: str) -> list[str]:
    if SECTION_HEADER not in text:
        return []
    _head, tail = text.split(SECTION_HEADER, 1)
    return [line for line in tail.splitlines() if line.strip().startswith("- [")]


def _sync_readme(readme: Path) -> int:
    missing = _missing_children(readme)
    if not missing:
        return 0

    text = readme.read_text(encoding="utf-8")
    preserved = _coverage_section_lines(text)
    if SECTION_HEADER in text:
        head, _tail = text.split(SECTION_HEADER, 1)
        text = head.rstrip() + f"\n\n{SECTION_HEADER}\n\n"
    else:
        text = text.rstrip() + f"\n\n{SECTION_HEADER}\n\n"

    if preserved:
        text += "\n".join(preserved) + "\n"

    lines = []
    for child in missing:
        target = f"{child.name}/" if child.is_dir() else child.name
        lines.append(f"- [{child.name}]({target})")
    text += "\n".join(lines) + "\n"
    readme.write_text(text, encoding="utf-8")
    return len(missing)


def main() -> int:
    total = 0
    for readme in ROOT.rglob(README_NAME):
        if readme.is_file():
            total += _sync_readme(readme)
    print(f"README coverage sync complete: added links for {total} child entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())