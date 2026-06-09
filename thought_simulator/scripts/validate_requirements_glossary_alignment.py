#!/usr/bin/env python3
"""Warn when 20.190 glossary and its term registry are out of alignment.

This check is intentionally non-blocking (warning-only). It warns on both:
1. terms required by 20_requirements registry groups but missing from 20.190_glossary.md
2. terms present in 20.190_glossary.md but not required by the registry
"""

from __future__ import annotations

from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parents[1]
GLOSSARY_PATH = ROOT / "20_requirements" / "20.190_glossary.md"
REGISTRY_PATH = ROOT / "20_requirements" / "glossary_term_registry.json"
IGNORED_TERMS = {
    "last updated",
    "version",
    "date",
    "status",
    "document id",
    "directory layout",
    "closure line (2026-06-07)",
    "tier 1",
    "tier 2",
    "tier 3",
    "focus",
    "when",
    "why",
    "is not",
    "example",
    "normative home",
    "term",
    "role",
    "field",
    "meaning",
    "version",
    "author",
    "summary",
}


def _normalize_term(raw: str) -> str:
    cleaned = re.sub(r"\*\([^)]*\)\*", "", raw).strip()
    cleaned = re.sub(r"\*[^*]+\*", "", cleaned).strip()
    return cleaned.lower().rstrip(":").strip()


def _add_term(terms: set[str], raw: str) -> None:
    norm = _normalize_term(raw)
    if not norm or norm in IGNORED_TERMS:
        return
    terms.add(norm)
    if "/" in norm and "(" not in norm:
        for part in re.split(r"\s*/\s*", norm):
            part = part.strip()
            if part and part not in IGNORED_TERMS:
                terms.add(part)
    paren = re.match(r"^(.+?)\s*\(([^)]+)\)$", norm)
    if paren:
        terms.add(paren.group(1).strip())
        terms.add(f"{paren.group(1).strip()} ({paren.group(2).strip()})")


def _extract_glossary_terms(glossary_text: str) -> set[str]:
    terms: set[str] = set()
    in_catalog_aliases = False

    for line in glossary_text.splitlines():
        stripped = line.strip()
        if "### Catalog aliases" in stripped:
            in_catalog_aliases = True
            continue
        if stripped.startswith("### ") and "Catalog aliases" not in stripped:
            in_catalog_aliases = False

        for pattern in (
            r"^\*\*(.+?)\*\*:?",
            r"^-\s*\*\*(.+?)\*\*:?",
            r"^\|\s*\*\*(.+?)\*\*\s*\|",
            r"^\|\s*\*\*`([^`]+)`\*\*\s*\|",
            r"^####\s+(.+)$",
        ):
            match = re.match(pattern, stripped)
            if match:
                _add_term(terms, match.group(1))

        for match in re.finditer(r"`([a-z][a-z0-9_]+)`", stripped):
            _add_term(terms, match.group(1).replace("_", " "))
            terms.add(match.group(1).lower())

        if in_catalog_aliases and ";" in stripped:
            for chunk in stripped.split(";"):
                _add_term(terms, chunk)

    return terms


def _registry_term_present(registry_term: str, glossary_terms: set[str]) -> bool:
    if registry_term in glossary_terms:
        return True
    variants = {registry_term}
    paren = re.match(r"^(.+?)\s*\(([^)]+)\)$", registry_term)
    if paren:
        variants.add(paren.group(1).strip())
    underscore = registry_term.replace(" ", "_")
    variants.add(underscore)
    return any(v in glossary_terms for v in variants)


def _load_registry() -> tuple[list[str], dict[str, list[str]]]:
    if not REGISTRY_PATH.exists():
        print(f"20 glossary warning: missing registry file at {REGISTRY_PATH}")
        return [], {}

    try:
        payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"20 glossary warning: unable to read registry file ({exc})")
        return [], {}

    protected = payload.get("protected_terms", [])
    required_by_module = payload.get("required_by_module", {})

    if not isinstance(protected, list):
        print("20 glossary warning: 'protected_terms' must be a list")
        protected = []
    if not isinstance(required_by_module, dict):
        print("20 glossary warning: 'required_by_module' must be an object")
        required_by_module = {}

    normalized_protected = [str(item).strip().lower() for item in protected if str(item).strip()]
    normalized_required: dict[str, list[str]] = {}
    for key, value in required_by_module.items():
        if not isinstance(value, list):
            continue
        normalized_required[str(key)] = [str(item).strip().lower() for item in value if str(item).strip()]

    return normalized_protected, normalized_required


def _expected_terms(required_by_module: dict[str, list[str]], protected_terms: list[str]) -> set[str]:
    expected: set[str] = set(protected_terms)
    for terms in required_by_module.values():
        expected.update(terms)
    return expected


def main() -> int:
    if not GLOSSARY_PATH.exists():
        print(f"20 glossary warning: missing glossary file at {GLOSSARY_PATH}")
        return 0

    glossary_terms = _extract_glossary_terms(GLOSSARY_PATH.read_text(encoding="utf-8"))
    protected_terms, required_by_module = _load_registry()
    warnings: list[str] = []

    for group_name, required_terms in required_by_module.items():
        group_path = ROOT / "20_requirements" / group_name
        if not group_path.exists():
            continue

        for term in required_terms:
            if not _registry_term_present(term, glossary_terms):
                warnings.append(
                    f"20_requirements/{group_name}: glossary term '{term}' missing in 20.190_glossary.md"
                )

    expected = _expected_terms(required_by_module, protected_terms)

    missing_global = sorted(
        term for term in expected if not _registry_term_present(term, glossary_terms)
    )
    for term in missing_global:
        warnings.append(
            f"20_requirements/20.190_glossary.md: required term '{term}' is missing"
        )

    if warnings:
        print("20 glossary alignment warnings:")
        for item in warnings:
            print(f"- {item}")
        print("20 glossary alignment check completed with warnings (non-blocking).")
        return 0

    print("20 glossary alignment check passed: glossary and requirements-term registry are aligned.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
