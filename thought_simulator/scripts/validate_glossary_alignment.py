#!/usr/bin/env python3
"""Warn when promoted verification modules introduce terms missing from 30.30 glossary.

This check is intentionally non-blocking (warning-only). It helps catch process-flow
misses where module evidence is promoted but shared glossary terms are not updated.
"""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
GLOSSARY_PATH = ROOT / "30_verification" / "30.30_verification_glossary.md"

# Required shared vocabulary for promoted scheduler verification flow.
# Add terms here as new promoted modules introduce domain vocabulary.
REQUIRED_BY_MODULE: dict[str, tuple[str, ...]] = {
    "30.40_scheduler_prototypes": (
        "scheduler",
        "fairness",
        "tie-break",
        "starvation prevention",
    ),
}


def _extract_glossary_terms(glossary_text: str) -> set[str]:
    terms: set[str] = set()
    for line in glossary_text.splitlines():
        match = re.match(r"^###\s+(.+?)\s*$", line)
        if not match:
            continue
        terms.add(match.group(1).strip().lower())
    return terms


def main() -> int:
    if not GLOSSARY_PATH.exists():
        print(f"Glossary warning: missing glossary file at {GLOSSARY_PATH}")
        return 0

    glossary_terms = _extract_glossary_terms(GLOSSARY_PATH.read_text(encoding="utf-8"))
    warnings: list[str] = []

    for module_dir, required_terms in REQUIRED_BY_MODULE.items():
        module_path = ROOT / "30_verification" / module_dir
        if not module_path.exists():
            continue

        for term in required_terms:
            if term.lower() not in glossary_terms:
                warnings.append(
                    f"30_verification/{module_dir}: glossary term '{term}' missing in 30.30_verification_glossary.md"
                )

    if warnings:
        print("Glossary alignment warnings:")
        for item in warnings:
            print(f"- {item}")
        print("Glossary alignment check completed with warnings (non-blocking).")
        return 0

    print("Glossary alignment check passed: no missing required terms detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
