#!/usr/bin/env python3
"""Validate markdown cross-tier dependency rules for Thought Simulator docs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys


@dataclass(frozen=True)
class Rule:
    scope_prefix: str
    forbidden_tokens: tuple[str, ...]
    reason: str
    exempt_paths: tuple[str, ...] = ()


RULES: tuple[Rule, ...] = (
    Rule(
        scope_prefix="50_thought_simulator_design/",
        forbidden_tokens=("40_thought_simulator_playground/",),
        reason="Design docs must not reference playground paths.",
        exempt_paths=(
            "50_thought_simulator_design/50.05_software_spec_construction_guide.md",
        ),
    ),
)

MD_SUFFIX = ".md"


def _iter_markdown_files(root: Path):
    for path in root.rglob(f"*{MD_SUFFIX}"):
        if path.is_file():
            yield path


def _line_matches(content: str, token: str) -> list[int]:
    lines = []
    pattern = re.compile(re.escape(token))
    for idx, line in enumerate(content.splitlines(), start=1):
        if pattern.search(line):
            lines.append(idx)
    return lines


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    violations: list[str] = []

    for path in _iter_markdown_files(root):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        for rule in RULES:
            if not rel.startswith(rule.scope_prefix):
                continue
            if rel in rule.exempt_paths:
                continue
            for token in rule.forbidden_tokens:
                lines = _line_matches(text, token)
                for line_number in lines:
                    violations.append(
                        f"{rel}:{line_number}: forbidden reference '{token}' ({rule.reason})"
                    )

    if violations:
        print("Dependency rule violations found:")
        for violation in violations:
            print(f"- {violation}")
        return 1

    print("Dependency rule check passed: no violations found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
