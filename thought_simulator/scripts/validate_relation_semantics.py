#!/usr/bin/env python3
"""Validate optional relation-semantics metadata in markdown frontmatter.

Supported relation keys:
- satisfies
- proves
- derived-from
- supersedes

Validation is migration-safe: relation keys are optional.
If present, values must contain valid HLR/LLR placeholders or canonical IDs.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


TARGET_TIERS = (
    "20_requirements/",
    "30_verification/",
    "50_thought_simulator_design/",
)

RELATION_KEYS = ("satisfies", "proves", "derived-from", "supersedes")

CANONICAL_ID_PATTERNS = (
    re.compile(r"^HLR-20\.\d{2,3}-\d{3}$"),
    re.compile(r"^LLR-30\.\d{2,3}-\d{3}$"),
    re.compile(r"^LLR-50\.\d{2,3}-\d{3}$"),
)

PLACEHOLDER_IDS = {"HLR-?", "LLR-?"}


@dataclass
class Issue:
    path: str
    line: int
    message: str


def is_target(rel_path: str) -> bool:
    return rel_path.startswith(TARGET_TIERS)


def split_frontmatter(content: str) -> tuple[list[str] | None, int]:
    lines = content.splitlines()
    if lines:
        lines[0] = lines[0].lstrip("\ufeff")
    if not lines or lines[0].strip() != "---":
        return None, -1
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[1:idx], idx + 1
    return None, -1


def _unquote(token: str) -> str:
    """Strip surrounding single or double quotes from a YAML scalar token."""
    if len(token) >= 2 and token[0] in ('"', "'") and token[-1] == token[0]:
        return token[1:-1]
    return token


def parse_relation_values(frontmatter_lines: list[str]) -> dict[str, list[str]]:
    relations: dict[str, list[str]] = {key: [] for key in RELATION_KEYS}

    current_key: str | None = None
    for line in frontmatter_lines:
        stripped = line.strip()
        if not stripped:
            continue

        for key in RELATION_KEYS:
            prefix = f"{key}:"
            if stripped.startswith(prefix):
                current_key = key
                remainder = stripped[len(prefix):].strip()
                if remainder.startswith("[") and remainder.endswith("]"):
                    inner = remainder[1:-1].strip()
                    if inner:
                        relations[key].extend([_unquote(t.strip()) for t in inner.split(",")])
                break
        else:
            if current_key and stripped.startswith("-"):
                value = _unquote(stripped[1:].strip())
                if value:
                    relations[current_key].append(value)
            else:
                current_key = None

    return relations


def validate_relation_ids(rel_path: str, frontmatter_lines: list[str], start_line: int) -> list[Issue]:
    issues: list[Issue] = []
    relations = parse_relation_values(frontmatter_lines)

    for key, values in relations.items():
        for value in values:
            if value in PLACEHOLDER_IDS:
                continue
            if not any(pattern.match(value) for pattern in CANONICAL_ID_PATTERNS):
                issues.append(
                    Issue(
                        path=rel_path,
                        line=start_line,
                        message=f"invalid relation ID in {key}: {value}",
                    )
                )

    return issues


def iter_markdown(root: Path):
    for path in root.rglob("*.md"):
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            if is_target(rel):
                yield path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    issues: list[Issue] = []

    for path in iter_markdown(root):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        frontmatter_lines, body_start = split_frontmatter(text)
        if frontmatter_lines is None:
            continue
        issues.extend(validate_relation_ids(rel, frontmatter_lines, body_start if body_start > 0 else 1))

    if issues:
        print("Relation semantics validation errors:")
        for issue in issues:
            print(f"- {issue.path}:{issue.line}: {issue.message}")
        return 1

    print("Relation semantics validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
