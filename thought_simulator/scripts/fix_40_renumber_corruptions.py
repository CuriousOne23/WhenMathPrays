#!/usr/bin/env python3
"""One-shot fix for substring collisions after 40 renumber shorthand pass."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = frozenset({"archive", "__pycache__", ".git", "node_modules"})
EXTENSIONS = {".md", ".py", ".json"}

# Longest-first replacement pairs
FIXES: list[tuple[str, str]] = [
    ("40.180_cob_prototypes", "40.110_cob_prototypes"),
    ("40.170_gb_prototypes", "40.130_gb_prototypes"),
    ("HLR-40.180_cob-", "HLR-40.110_cob-"),
    ("HLR-40.170_gb-", "HLR-40.130_gb-"),
    ("LLR-40.180_cob-", "LLR-40.110_cob-"),
    ("LLR-40.170_gb-", "LLR-40.130_gb-"),
]


def main() -> int:
    changed_files = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in EXTENSIONS:
            continue
        if path.name == Path(__file__).name:
            continue
        if any(p in SKIP_DIRS for p in path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in FIXES:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed_files += 1
            print(path.relative_to(ROOT).as_posix())
    print(f"Fixed {changed_files} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())