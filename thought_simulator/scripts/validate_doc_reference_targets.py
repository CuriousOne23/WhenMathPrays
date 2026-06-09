#!/usr/bin/env python3
"""Validate document and heading references across Thought Simulator doc tiers.

By default this script is non-blocking and reports warnings for unresolved
file references. Use --strict to return a non-zero exit code when warnings are
found. Use --check-headings to also validate markdown heading anchors.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import unquote
import re
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
SCOPES = (
    "00_program_governance",
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
    target = target.split("?", 1)[0].strip()
    return unquote(target)


def _split_target(raw_target: str) -> tuple[str, str]:
    target = _normalize_target(raw_target)
    if not target:
        return "", ""
    if "#" not in target:
        return target, ""
    path_part, anchor = target.split("#", 1)
    return path_part.strip(), anchor.strip()


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
    normalized = token.strip()
    if not normalized or _is_external(normalized):
        return None
    if not _has_allowed_extension(normalized):
        return None

    if normalized.startswith("scripts/"):
        candidate = SCRIPTS_DIR / normalized.removeprefix("scripts/")
        if candidate.exists():
            return candidate

    repo_root_path = _resolve_repo_root_path(normalized)
    if repo_root_path is not None:
        return repo_root_path

    design_50 = _resolve_50_inventory_path(normalized)
    if design_50 is not None:
        return design_50

    if normalized.startswith("10_thought_simulator_req/"):
        candidate = ROOT / normalized
        if candidate.exists():
            return candidate

    if "/" in normalized or normalized.startswith("../"):
        for scope in SCOPES:
            if normalized.startswith(f"{scope}/"):
                return ROOT / normalized
        if normalized.startswith("thought_simulator/"):
            return ROOT.parent / normalized
        resolved = (referrer.parent / normalized).resolve()
        if resolved.exists():
            return resolved
        inventory = _resolve_module_inventory_path(normalized)
        if inventory is not None:
            return inventory
        return resolved

    inventory = _resolve_module_inventory_path(normalized)
    if inventory is not None:
        return inventory

    if normalized.endswith(".py"):
        script_candidate = SCRIPTS_DIR / normalized
        if script_candidate.exists():
            return script_candidate

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


def _looks_like_glob(target: str) -> bool:
    return any(ch in target for ch in ("*", "?", "[", "]", "{", "}"))


def _looks_like_template(target: str) -> bool:
    return "{" in target and "}" in target


def _looks_like_compound_py_path(target: str) -> bool:
    lowered = target.lower()
    return ".py/" in lowered or re.search(r"/\d+/", target) is not None


def _looks_like_placeholder(target: str) -> bool:
    return bool(
        re.search(r"\bxx\b|YYYY|codename_verification", target, re.IGNORECASE)
        or re.search(r"_run\{", target)
        or re.search(r"30\.xx_", target)
    )


def _resolve_repo_root_path(token: str) -> Path | None:
    for prefix in ("testbenches/", ".github/"):
        if token.startswith(prefix) or token.startswith(f"../../../{prefix}"):
            normalized = token.removeprefix("../").removeprefix("../").removeprefix("../")
            candidate = ROOT.parent / normalized
            if candidate.exists():
                return candidate
    return None


def _resolve_50_inventory_path(token: str) -> Path | None:
    if re.match(r"^50\.\d+_.+\.md$", token):
        candidate = ROOT / "50_thought_simulator_design" / token
        if candidate.exists():
            return candidate
    return None


def _is_governance_hypothetical(referrer_rel: str, token: str) -> bool:
    if not referrer_rel.startswith("00_program_governance/"):
        return False
    if _looks_like_template(token):
        return True
    if token.endswith("my_rename.json"):
        return True
    if "/" not in token and token.endswith(".md"):
        return True
    if re.match(r"^\d{2}\.\d{2,3}\.\d{3}_", token):
        return True
    return False


def _resolve_module_inventory_path(token: str) -> Path | None:
    if re.match(r"^30\.\d", token):
        candidate = ROOT / "30_verification" / token
        if candidate.exists():
            return candidate
    if re.match(r"^40\.\d", token):
        candidate = ROOT / "40_thought_simulator_playground" / token
        if candidate.exists():
            return candidate
    if token == "glossary_term_registry.json":
        candidate = ROOT / "30_verification" / token
        if candidate.exists():
            return candidate
    if token.startswith("archive/"):
        for prefix in (
            ROOT / "40_thought_simulator_playground",
            ROOT,
        ):
            candidate = prefix / token
            if candidate.exists():
                return candidate
    return None


def _slugify_heading(text: str) -> str:
    value = text.strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"[^a-z0-9\-]", "", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value


def _collect_heading_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
        if not match:
            continue
        heading = re.sub(r"\s+#+\s*$", "", match.group(1)).strip()
        anchor = _slugify_heading(heading)
        if anchor:
            anchors.add(anchor)
    return anchors


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate markdown file and heading references.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero exit code when unresolved references are found.",
    )
    parser.add_argument(
        "--check-headings",
        action="store_true",
        help="Validate markdown heading anchors for links that include #anchor.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    basename_index = _build_basename_index()
    heading_index = {path.resolve(): _collect_heading_anchors(path) for path in _iter_markdown_files()}
    warnings: list[str] = []

    for path in _iter_markdown_files():
        rel_path = path.relative_to(ROOT).as_posix()
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for token in _extract_candidates(line):
                normalized, anchor = _split_target(token)
                if not normalized and anchor:
                    target = path
                    normalized_for_msg = f"#{anchor}"
                else:
                    target = _candidate_to_path(path, normalized, basename_index)
                    normalized_for_msg = normalized

                if not normalized and not anchor:
                    continue
                if normalized and _is_external(normalized):
                    continue
                if normalized and _looks_like_glob(normalized):
                    continue
                if normalized and _looks_like_template(normalized):
                    continue
                if normalized and _looks_like_compound_py_path(normalized):
                    continue
                if normalized and _looks_like_placeholder(normalized):
                    continue
                if normalized and _is_governance_hypothetical(rel_path, normalized):
                    continue
                if rel_path.startswith("20_requirements/archive/"):
                    continue
                if normalized and not _has_allowed_extension(normalized):
                    continue
                if target is None:
                    # Only warn when the token looks like a specific path/file, not a generic ambiguous filename.
                    if "/" in normalized_for_msg or normalized_for_msg.startswith("../") or normalized_for_msg not in basename_index:
                        warnings.append(
                            f"{rel_path}:{line_number}: reference '{normalized_for_msg}' does not resolve to an existing file"
                        )
                    continue
                if not target.exists():
                    warnings.append(
                        f"{rel_path}:{line_number}: reference '{normalized_for_msg}' points to missing file '{target}'"
                    )
                    continue

                if args.check_headings and anchor and target.suffix.lower() == ".md":
                    target_anchors = heading_index.get(target.resolve(), set())
                    if _slugify_heading(anchor) not in target_anchors:
                        warnings.append(
                            f"{rel_path}:{line_number}: heading anchor '#{anchor}' not found in '{target.relative_to(ROOT.parent)}'"
                        )

    if warnings:
        print("Document reference issues:")
        for warning in warnings:
            print(f"- {warning}")
        if args.strict:
            print("Document reference check failed (blocking strict mode).")
            return 1
        print("Document reference check completed with warnings (non-blocking mode).")
        return 0

    print("Document reference check passed: no broken file references detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
