#!/usr/bin/env python3
"""Warn on broken document/file references across Thought Simulator doc tiers.

This check is non-blocking and is intended to surface cases where files were
moved, renamed, or deleted but are still referenced by other markdown files.
It reports the referring file and line number.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote
import re


ROOT = Path(__file__).resolve().parents[1]
SCOPES = (
    "10_program_governance",
    "10_thought_simulator_req",
    "20_requirements",
    "30_verification",
    "40_thought_simulator_playground",
    "50_thought_simulator_design",
)
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "file://")
ALLOWED_EXTENSIONS = ("md", "json", "yaml", "yml", "py", "csv", "txt", "npz")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
BACKTICK_TOKEN_RE = re.compile(
    r"`([^`\s]+\.(?:md|json|yaml|yml|py|csv|txt|npz))`",
    re.IGNORECASE,
)
PLAIN_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_/.-])((?:\.\./|[0-9]{2}_[A-Za-z0-9_.-]+/|[0-9]{2}_|[0-9]{2}\.[0-9]{2}_|[A-Za-z0-9_.-]+/)[A-Za-z0-9_./-]*\.(?:md|json|yaml|yml|py|csv|txt|npz))(?![A-Za-z0-9_/.-])",
    re.IGNORECASE,
)


def _iter_markdown_files():
    for scope in SCOPES:
        scope_root = ROOT / scope
        if not scope_root.exists():
            continue
        for path in scope_root.rglob("*.md"):
            if path.is_file():
                yield path


def _normalize_target(raw_target: str) -> str:
    target = raw_target.strip()
    if not target:
        return ""
    target = target.split("#", 1)[0].split("?", 1)[0].strip()
    return unquote(target)


def _has_allowed_extension(target: str) -> bool:
    suffix = Path(target).suffix.lower().lstrip(".")
    return suffix in ALLOWED_EXTENSIONS


def _is_external(target: str) -> bool:
    lowered = target.lower()
    return any(lowered.startswith(prefix) for prefix in EXTERNAL_PREFIXES)


def _build_basename_index() -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for scope in SCOPES:
        scope_root = ROOT / scope
        if not scope_root.exists():
            continue
        for path in scope_root.rglob("*"):
            if not path.is_file():
                continue
            index.setdefault(path.name, []).append(path)
    return index


def _candidate_to_path(referrer: Path, token: str, basename_index: dict[str, list[Path]]) -> Path | None:
    normalized = _normalize_target(token)
    if not normalized or _is_external(normalized):
        return None
    if not _has_allowed_extension(normalized):
        return None

    if "/" in normalized or normalized.startswith("../"):
        for scope in SCOPES:
            if normalized.startswith(f"{scope}/"):
                return ROOT / normalized
        if normalized.startswith("thought_simulator/"):
            return ROOT.parent / normalized
        return (referrer.parent / normalized).resolve()

    direct = referrer.parent / normalized
    if direct.exists():
        return direct

    matches = basename_index.get(normalized, [])
    if len(matches) == 1:
        return matches[0]

    return None


def _extract_candidates(line: str) -> list[str]:
    candidates: list[str] = []
    for match in MARKDOWN_LINK_RE.finditer(line):
        candidates.append(match.group(1))
    for match in BACKTICK_TOKEN_RE.finditer(line):
        token = match.group(1)
        if token not in candidates:
            candidates.append(token)
    for match in PLAIN_PATH_RE.finditer(line):
        token = match.group(1)
        if token not in candidates:
            candidates.append(token)
    return candidates


def main() -> int:
    basename_index = _build_basename_index()
    warnings: list[str] = []

    for path in _iter_markdown_files():
        rel_path = path.relative_to(ROOT).as_posix()
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for token in _extract_candidates(line):
                target = _candidate_to_path(path, token, basename_index)
                normalized = _normalize_target(token)
                if not normalized or _is_external(normalized):
                    continue
                if not _has_allowed_extension(normalized):
                    continue
                if target is None:
                    # Only warn when the token looks like a specific path/file, not a generic ambiguous filename.
                    if "/" in normalized or normalized.startswith("../") or normalized not in basename_index:
                        warnings.append(
                            f"{rel_path}:{line_number}: reference '{normalized}' does not resolve to an existing file"
                        )
                    continue
                if not target.exists():
                    warnings.append(
                        f"{rel_path}:{line_number}: reference '{normalized}' points to missing file '{target}'"
                    )

    if warnings:
        print("Document reference warnings:")
        for warning in warnings:
            print(f"- {warning}")
        print("Document reference check completed with warnings (non-blocking).")
        return 0

    print("Document reference check passed: no broken file references detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
