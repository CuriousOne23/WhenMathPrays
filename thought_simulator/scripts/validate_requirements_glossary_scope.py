#!/usr/bin/env python3
"""Warn when 20.150 glossary is referenced outside 20_requirements tier.

This check is intentionally non-blocking (warning-only).
"""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SCOPES = (
    "10_program_governance",
    "10_thought_simulator_req",
    "30_verification",
    "40_thought_simulator_playground",
    "50_thought_simulator_design",
)

PATTERNS = (
    re.compile(r"\b20\.150_glossary\.md\b", re.IGNORECASE),
    re.compile(r"\b20_requirements/20\.150_glossary\.md\b", re.IGNORECASE),
)


def _iter_scope_files():
    for scope in SCOPES:
        scope_path = ROOT / scope
        if not scope_path.exists():
            continue
        for path in scope_path.rglob("*.md"):
            if path.is_file():
                yield path


def main() -> int:
    warnings: list[str] = []

    for path in _iter_scope_files():
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for pattern in PATTERNS:
                if pattern.search(line):
                    warnings.append(
                        f"{rel}:{line_number}: 20 glossary reference outside 20 tier -> '{line.strip()}'"
                    )
                    break

    if warnings:
        print("20 glossary scope warnings:")
        for item in warnings:
            print(f"- {item}")
        print("20 glossary scope check completed with warnings (non-blocking).")
        return 0

    print("20 glossary scope check passed: no out-of-tier references detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
