#!/usr/bin/env python3
"""Validate document frontmatter and HLR/LLR IDs against prefix-address convention.

Convention (00.00.42): path/filename prefix is canonical identity; YAML mirrors it.
- Missing frontmatter warns only on normative spec paths (not guides/meta).
- Document ID / related ID-token band mismatches vs path address are warnings (full alignment).
- Tier 40 and 00 governance: subdirectory/path Document-ID alignment only (no strict inline IDs).
- Malformed ID shape and invalid frontmatter keys remain blocking errors with --strict-ids elsewhere.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import re

from doc_address import (
    canonical_address_from_path,
    id_band_aligns_with_address,
    id_token_band,
    is_frontmatter_exempt,
    is_normative_spec_path,
    is_alignment_only_path,
    parse_document_id,
    address_prefixes_compatible,
)


TARGET_TIERS = (
    "00_program_governance/",
    "10_thought_simulator_req/50_design/",
    "20_requirements/",
    "30_verification/",
    "40_thought_simulator_playground/",
    "50_thought_simulator_design/",
)

ALLOWED_STATUS = {
    "requirements",
    "verification",
    "design",
    "governance",
    "playground",
    "guidance",
    "coordination",
    "active",
}

ALLOWED_SOURCE_OF_TRUTH = {"this", "upstream"}

STRICT_ID_PATTERNS = (
    re.compile(r"^HLR-20\.\d{2,3}-\d{3}$"),
    re.compile(r"^HLR-20\.\d{2,3}-\d{3}[a-z]$"),
    re.compile(r"^HLR-20\.\d{2,3}-\d{3}\.\.\d{3}$"),
    re.compile(r"^HLR-20\.\d{2,3}$"),
    re.compile(r"^HLR-10\.50\.\d{2,3}-\d{3}$"),
    re.compile(r"^HLR-10\.50\.\d{2,3}-\d{3}\.\.\d{3}$"),
    re.compile(r"^HLR-10\.50\.xx$"),
    re.compile(r"^HLR-\d{3}$"),
    re.compile(r"^HLR-\d{3}[a-z]$"),
    re.compile(r"^HLR-\d{3}\.\.\d{3}$"),
    re.compile(r"^LLR-30\.\d{2,3}-\d{3}$"),
    re.compile(r"^LLR-30\.xx$"),
    re.compile(r"^LLR-50\.\d{2,3}-\d{3}$"),
    re.compile(r"^LLR-50\.\d{2}$"),
    re.compile(r"^LLR-TR-[A-Z]+-\d{3}$"),
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


def validate_ids(rel_path: str, text: str, strict_ids: bool, canonical: str | None) -> list[ValidationIssue]:
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
                continue
            if id_token_band(token) and canonical and not id_band_aligns_with_address(token, canonical):
                issues.append(
                    ValidationIssue(
                        path=rel_path,
                        line=line_number,
                        level="warning",
                        message=(
                            f"ID band '{id_token_band(token)}' does not align with path address "
                            f"'{canonical}' (prefix convention)"
                        ),
                    )
                )
    return issues


def validate_address_alignment(rel_path: str, text: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    canonical = canonical_address_from_path(rel_path)
    if canonical is None:
        return issues

    doc_id = parse_document_id(text)
    if doc_id and not address_prefixes_compatible(canonical, doc_id):
        issues.append(
            ValidationIssue(
                path=rel_path,
                line=1,
                level="warning",
                message=(
                    f"Document ID '{doc_id}' does not align with path address "
                    f"'{canonical}' (prefix convention)"
                ),
            )
        )
    return issues


def validate_file(
    rel_path: str,
    path: Path,
    require_frontmatter: bool,
    strict_ids: bool,
    alignment_warnings: bool,
) -> list[ValidationIssue]:
    text = path.read_text(encoding="utf-8")
    issues: list[ValidationIssue] = []
    canonical = canonical_address_from_path(rel_path)

    frontmatter_lines, _body_start_line = split_frontmatter(text)
    has_frontmatter = frontmatter_lines is not None

    if (
        require_frontmatter
        and is_target_tier(rel_path)
        and not has_frontmatter
        and is_normative_spec_path(rel_path)
        and not is_frontmatter_exempt(rel_path)
    ):
        issues.append(
            ValidationIssue(
                path=rel_path,
                line=1,
                level="warning",
                message="missing frontmatter on normative spec path (prefix address is canonical; YAML should mirror it)",
            )
        )

    alignment_only = is_alignment_only_path(rel_path)

    if has_frontmatter and not alignment_only:
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

    if alignment_warnings:
        issues.extend(validate_address_alignment(rel_path, text))

    if not alignment_only:
        issues.extend(validate_ids(rel_path, text, strict_ids, canonical))
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
        help="Warn when normative spec paths lack frontmatter (guides/meta exempt).",
    )
    parser.add_argument(
        "--strict-ids",
        action="store_true",
        help="Treat malformed HLR/LLR IDs as errors instead of warnings.",
    )
    parser.add_argument(
        "--alignment-warnings",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Warn when Document ID or dotted ID bands disagree with path address (default: on).",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    all_issues: list[ValidationIssue] = []

    for path in iter_markdown_files(root):
        rel_path = path.relative_to(root).as_posix()
        all_issues.extend(
            validate_file(
                rel_path,
                path,
                args.require_frontmatter,
                args.strict_ids,
                args.alignment_warnings,
            )
        )

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