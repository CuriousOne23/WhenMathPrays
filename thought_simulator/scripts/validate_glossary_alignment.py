#!/usr/bin/env python3
"""Warn when glossary and requirements-term registry are out of alignment.

This check is intentionally non-blocking (warning-only). It warns on both:
1. terms required by promoted module requirements but missing from the glossary
2. terms present in the glossary but not required by promoted module requirements
"""

from __future__ import annotations

from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parents[1]
GLOSSARY_PATH = ROOT / "30_verification" / "30.30_verification_glossary.md"
REGISTRY_PATH = ROOT / "30_verification" / "glossary_term_registry.json"


def _extract_glossary_terms(glossary_text: str) -> set[str]:
    terms: set[str] = set()
    for line in glossary_text.splitlines():
        match = re.match(r"^###\s+(.+?)\s*$", line)
        if not match:
            continue
        terms.add(match.group(1).strip().lower())
    return terms


def _load_registry() -> tuple[list[str], dict[str, list[str]]]:
    if not REGISTRY_PATH.exists():
        print(f"Glossary warning: missing registry file at {REGISTRY_PATH}")
        return [], {}

    try:
        payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Glossary warning: unable to read registry file ({exc})")
        return [], {}

    protected = payload.get("protected_terms", [])
    required_by_module = payload.get("required_by_module", {})

    if not isinstance(protected, list):
        print("Glossary warning: 'protected_terms' must be a list")
        protected = []
    if not isinstance(required_by_module, dict):
        print("Glossary warning: 'required_by_module' must be an object")
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
        print(f"Glossary warning: missing glossary file at {GLOSSARY_PATH}")
        return 0

    glossary_terms = _extract_glossary_terms(GLOSSARY_PATH.read_text(encoding="utf-8"))
    protected_terms, required_by_module = _load_registry()
    warnings: list[str] = []

    for module_dir, required_terms in required_by_module.items():
        module_path = ROOT / "30_verification" / module_dir
        if not module_path.exists():
            continue

        for term in required_terms:
            if term not in glossary_terms:
                warnings.append(
                    f"30_verification/{module_dir}: glossary term '{term}' missing in 30.30_verification_glossary.md"
                )

    expected = _expected_terms(required_by_module, protected_terms)

    missing_global = sorted(expected - glossary_terms)
    for term in missing_global:
        warnings.append(
            f"30_verification/30.30_verification_glossary.md: required term '{term}' is missing"
        )

    extra_global = sorted(glossary_terms - expected)
    for term in extra_global:
        warnings.append(
            f"30_verification/30.30_verification_glossary.md: term '{term}' is not required by glossary_term_registry.json"
        )

    if warnings:
        print("Glossary alignment warnings:")
        for item in warnings:
            print(f"- {item}")
        print("Glossary alignment check completed with warnings (non-blocking).")
        return 0

    print("Glossary alignment check passed: glossary and requirements-term registry are aligned.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
