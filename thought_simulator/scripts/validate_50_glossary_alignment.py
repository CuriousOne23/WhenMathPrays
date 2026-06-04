#!/usr/bin/env python3
"""Warn when 50-series glossary and its term registry are out of alignment.

This check is intentionally non-blocking (warning-only, human decides whether to act).
It warns on:
- terms declared in the 50 registry but missing from the glossary
- terms in the glossary but not declared in the registry
- candidate terms observed in 50 design .md files (via bold/table patterns) that are not yet in the glossary

The goal is notification when .md adds, modifications (term changes), or deletes may make the glossary not fresh.
No hard enforcement — the team reviews warnings and decides on updates.
"""

from __future__ import annotations

from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parents[1]
GLOSSARY_PATH = ROOT / "50_thought_simulator_design" / "50.01_50_series_glossary.md"
REGISTRY_PATH = ROOT / "50_thought_simulator_design" / "glossary_term_registry.json"
IGNORED_TERMS = {
    "last updated",
    "version",
}


def _extract_glossary_terms(glossary_text: str) -> set[str]:
    terms: set[str] = set()
    for line in glossary_text.splitlines():
        # Match markdown table rows with **Term** in the first column: | **Term** | Definition |
        match = re.search(r"\|\s*\*\*(.+?)\*\*\s*\|", line.strip())
        if not match:
            continue
        term = match.group(1).strip().lower()
        if term and term not in IGNORED_TERMS:
            terms.add(term)
    return terms


def _load_registry() -> tuple[list[str], dict[str, list[str]]]:
    if not REGISTRY_PATH.exists():
        print(f"50 glossary warning: missing registry file at {REGISTRY_PATH}")
        return [], {}

    try:
        payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"50 glossary warning: unable to read registry file ({exc})")
        return [], {}

    protected = payload.get("protected_terms", [])
    required_by_module = payload.get("required_by_module", {})

    if not isinstance(protected, list):
        print("50 glossary warning: 'protected_terms' must be a list")
        protected = []
    if not isinstance(required_by_module, dict):
        print("50 glossary warning: 'required_by_module' must be an object")
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


def _scan_50_design_candidates() -> set[str]:
    """Scan 50-series design docs for candidate glossary terms (tables with **Term** and bold terms).
    This is advisory only (warnings) to surface potential new terms introduced when .md files are added or modified.
    The team decides whether to promote a candidate into the glossary."""
    candidates: set[str] = set()
    design_dir = ROOT / "50_thought_simulator_design"
    if not design_dir.exists():
        return candidates
    for md_file in design_dir.rglob("*.md"):
        if not md_file.is_file():
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
            for line in text.splitlines():
                # Table style | **Term** |
                m1 = re.search(r"\|\s*\*\*(.+?)\*\*\s*\|", line)
                if m1:
                    t = m1.group(1).strip().lower()
                    if t and t not in IGNORED_TERMS:
                        candidates.add(t)
                # General bold terms that look like potential glossary entries (heuristic, advisory)
                for m2 in re.finditer(r"\*\*([A-Z][A-Za-z0-9\s\(\)]{2,40}?)\*\*", line):
                    t = m2.group(1).strip().lower()
                    if t and t not in IGNORED_TERMS and len(t) > 3:
                        candidates.add(t)
        except Exception:
            pass
    return candidates


def main() -> int:
    if not GLOSSARY_PATH.exists():
        print(f"50 glossary warning: missing glossary file at {GLOSSARY_PATH}")
        return 0

    glossary_terms = _extract_glossary_terms(GLOSSARY_PATH.read_text(encoding="utf-8"))
    protected_terms, required_by_module = _load_registry()
    warnings: list[str] = []

    for group_name, required_terms in required_by_module.items():
        group_path = ROOT / "50_thought_simulator_design" / group_name
        if not group_path.exists():
            continue

        for term in required_terms:
            if term not in glossary_terms:
                warnings.append(
                    f"50_thought_simulator_design/{group_name}: glossary term '{term}' missing in 50.01_50_series_glossary.md"
                )

    expected = _expected_terms(required_by_module, protected_terms)

    missing_global = sorted(expected - glossary_terms)
    for term in missing_global:
        warnings.append(
            f"50_thought_simulator_design/50.01_50_series_glossary.md: required term '{term}' is missing"
        )

    extra_global = sorted(glossary_terms - expected)
    for term in extra_global:
        warnings.append(
            f"50_thought_simulator_design/50.01_50_series_glossary.md: term '{term}' is not required by glossary_term_registry.json"
        )

    # Advisory scan: surface candidate terms observed in 50 design docs that are not yet in the glossary.
    # This helps notify on md adds/mods that may affect glossary freshness. Purely warning; human decides.
    candidates = _scan_50_design_candidates()
    new_candidates = sorted(candidates - glossary_terms)
    for term in new_candidates:
        warnings.append(
            f"50_thought_simulator_design: candidate term '{term}' observed in design docs but missing from 50.01_50_series_glossary.md"
        )

    if warnings:
        print("50 glossary alignment warnings:")
        for item in warnings:
            print(f"- {item}")
        print("50 glossary alignment check completed with warnings (non-blocking).")
        return 0

    print("50 glossary alignment check passed: glossary and requirements-term registry are aligned.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
