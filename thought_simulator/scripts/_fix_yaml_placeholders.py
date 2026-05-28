#!/usr/bin/env python3
"""Quote bare YAML flow-sequence tokens that contain ? (reserved in YAML).

Fixes patterns like:
  contains:
    - HLR: [HLR-?]         ->  - HLR: ["HLR-?"]
  supersedes: [HLR-?]      ->  supersedes: ["HLR-?"]
  proves: [HLR-?]          ->  proves: ["HLR-?"]
  derived-from: [LLR-?]    ->  derived-from: ["LLR-?"]

Only touches lines inside YAML frontmatter blocks.
"""
from __future__ import annotations

import re
from pathlib import Path

# Match a bare (unquoted) token that contains ? inside a flow sequence bracket context
BARE_Q = re.compile(r'(?<=[\[,])\s*([^\[\],\n"\']+\?[^\[\],\n"\']*?)\s*(?=[,\]])')

TIERS = ("20_requirements", "30_verification", "50_thought_simulator_design")


def fix(text: str) -> tuple[str, bool]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].lstrip("\ufeff").rstrip("\r\n") != "---":
        return text, False
    changed = False
    in_fm = True
    result: list[str] = []
    for i, line in enumerate(lines):
        if i == 0:
            result.append(line)
            continue
        if in_fm and line.rstrip("\r\n") == "---":
            in_fm = False
            result.append(line)
            continue
        if in_fm and "?" in line and "[" in line:
            new_line = BARE_Q.sub(lambda m: '"' + m.group(1).strip() + '"', line)
            if new_line != line:
                changed = True
                line = new_line
        result.append(line)
    return "".join(result), changed


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    fixed: list[str] = []
    for tier in TIERS:
        for md in (root / tier).rglob("*.md"):
            text = md.read_text(encoding="utf-8")
            new_text, changed = fix(text)
            if changed:
                md.write_text(new_text, encoding="utf-8")
                fixed.append(md.relative_to(root).as_posix())
    if fixed:
        print("Quoted ? placeholders in:")
        for f in fixed:
            print(" ", f)
    else:
        print("Nothing to fix.")


if __name__ == "__main__":
    main()
