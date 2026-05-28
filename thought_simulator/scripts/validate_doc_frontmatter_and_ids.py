#!/usr/bin/env python3
"""Validate document frontmatter shape and HLR/LLR ID formats.

This script is migration-friendly:
- It validates frontmatter only when frontmatter exists.
- It can optionally require frontmatter for target tiers.
- It reports malformed IDs while allowing temporary placeholder IDs.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import re


TARGET_TIERS = (
    "20_requirements/",
    "30_verification/",
    "50_thought_simulator_design/",
)

ALLOWED_STATUS = {
    "requirements",
    "verification",
    "design",
    "governance",
    "playground",
}

ALLOWED_SOURCE_OF_TRUTH = {"this", "upstream"}

STRICT_ID_PATTERNS = (
    re.compile(r"^HLR-20\.\d{2,3}-\d{3}$"),
    re.compile(r"^LLR-30\.\d{2,3}-\d{3}$"),
    re.compile(r"^LLR-50\.\d{2,3}-\d{3}$"),
)

PLACEHOLDER_IDS = {"HLR-?", "LLR-?"}

ID_TOKEN_PATTERN = re.compile(r"\b(?:HLR|LLR)-[A-Za-z0-9?.-]+\b")


@dataclass
class ValidationIssue:
    path: str
    line: int
    level: str
    message: str


def is_target_tier(rel_path: str) -> bool:
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


def parse_frontmatter_values(frontmatter_lines: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    key_re = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")
    for raw_line in frontmatter_lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = key_re.match(line)
        if match:
            key, value = match.groups()
            values[key] = value.strip().strip('"').strip("'")
    return values


def validate_ids(rel_path: str, text: str, strict_ids: bool) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for token in ID_TOKEN_PATTERN.findall(line):
            if token in PLACEHOLDER_IDS:
                issues.append(
                    ValidationIssue(
                        path=rel_path,
                        line=line_number,
                        level="warning",
                        message=f"placeholder ID in use: {token}",
                    )
                )
                continue
            if not any(pattern.match(token) for pattern in STRICT_ID_PATTERNS):
                issues.append(
                    ValidationIssue(
                        path=rel_path,
                        line=line_number,
                        level="error" if strict_ids else "warning",
                        message=f"malformed ID token: {token}",
                    )
                )
    return issues


def validate_file(rel_path: str, path: Path, require_frontmatter: bool, strict_ids: bool) -> list[ValidationIssue]:
    text = path.read_text(encoding="utf-8")
    issues: list[ValidationIssue] = []

    frontmatter_lines, body_start_line = split_frontmatter(text)
    has_frontmatter = frontmatter_lines is not None

    if require_frontmatter and is_target_tier(rel_path) and not has_frontmatter:
        issues.append(
            ValidationIssue(
                path=rel_path,
                line=1,
                level="warning",
                message="missing frontmatter in target tier",
            )
        )

    if has_frontmatter:
        values = parse_frontmatter_values(frontmatter_lines)
        if "status" not in values:
            issues.append(
                ValidationIssue(
                    path=rel_path,
                    line=1,
                    level="error",
                    message="frontmatter missing required key: status",
                )
            )
        elif values["status"] not in ALLOWED_STATUS:
            issues.append(
                ValidationIssue(
                    path=rel_path,
                    line=1,
                    level="error",
                    message=f"invalid status value: {values['status']}",
                )
            )

        if "source_of_truth" not in values:
            issues.append(
                ValidationIssue(
                    path=rel_path,
                    line=1,
                    level="error",
                    message="frontmatter missing required key: source_of_truth",
                )
            )
        elif values["source_of_truth"] not in ALLOWED_SOURCE_OF_TRUTH:
            issues.append(
                ValidationIssue(
                    path=rel_path,
                    line=1,
                    level="error",
                    message=f"invalid source_of_truth value: {values['source_of_truth']}",
                )
            )

    id_issues = validate_ids(rel_path, text, strict_ids)
    issues.extend(id_issues)

    return issues


def iter_markdown_files(root: Path):
    for path in root.rglob("*.md"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if is_target_tier(rel):
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate frontmatter and HLR/LLR ID formats")
    parser.add_argument(
        "--require-frontmatter",
        action="store_true",
        help="Warn when target-tier markdown files do not include frontmatter.",
    )
    parser.add_argument(
        "--strict-ids",
        action="store_true",
        help="Treat malformed HLR/LLR IDs as errors instead of warnings.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    all_issues: list[ValidationIssue] = []

    for path in iter_markdown_files(root):
        rel_path = path.relative_to(root).as_posix()
        all_issues.extend(validate_file(rel_path, path, args.require_frontmatter, args.strict_ids))

    errors = [issue for issue in all_issues if issue.level == "error"]
    warnings = [issue for issue in all_issues if issue.level == "warning"]

    if warnings:
        print("Frontmatter/ID warnings:")
        for issue in warnings:
            print(f"- {issue.path}:{issue.line}: {issue.message}")

    if errors:
        print("Frontmatter/ID errors:")
        for issue in errors:
            print(f"- {issue.path}:{issue.line}: {issue.message}")
        return 1

    print("Frontmatter/ID validation passed (no errors).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
