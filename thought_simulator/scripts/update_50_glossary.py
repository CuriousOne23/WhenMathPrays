#!/usr/bin/env python3
"""
Propose updates to keep the 50-series glossary fresh.

This script analyzes 50_thought_simulator_design/*.md files for glossary terms
(using the same patterns as the alignment validator) and compares them against:

- 50.01_50_series_glossary.md
- glossary_term_registry.json

It is **entirely advisory**. It never modifies files automatically.

Default behavior: Print a clear human-readable report of what is out of sync
and concrete proposals you can copy-paste or review.

Options:
  --write-proposals    Write proposal files (e.g. proposed_additions.md and
                       proposed_registry_delta.json) into the 50 directory
                       for easy review and selective application.

  --include-all-bold   Also consider more bold terms (can be noisy).

Run this whenever you add, modify, or delete design documents so you can see
what the glossary and registry might need. Then decide what (if anything) to
actually update.

This helps reduce token usage: the script does the mechanical scanning and
diffing locally instead of the AI having to re-read many files in chat.
"""

from __future__ import annotations

from pathlib import Path
import json
import re
import sys
import argparse
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DESIGN_DIR = ROOT / "50_thought_simulator_design"
GLOSSARY_PATH = DESIGN_DIR / "50.01_50_series_glossary.md"
REGISTRY_PATH = DESIGN_DIR / "glossary_term_registry.json"

IGNORED_TERMS = {
    "last updated",
    "version",
    "document id",
    "status",
    "date",
}


def _normalize(term: str) -> str:
    return term.strip().lower()


def _extract_terms_from_text(text: str, include_all_bold: bool = False) -> set[str]:
    """Extract candidate glossary terms from a document."""
    terms: set[str] = set()

    for line in text.splitlines():
        line = line.strip()

        # Primary: the table format used in 50.01_50_series_glossary.md
        # | **Governing Basin (GB)** | definition... |
        m = re.search(r"\|\s*\*\*(.+?)\*\*\s*\|", line)
        if m:
            t = _normalize(m.group(1))
            if t and t not in IGNORED_TERMS:
                terms.add(t)
            continue

        if include_all_bold:
            # Secondary heuristic: prominent **Capitalized Terms**
            for m in re.finditer(r"\*\*([A-Z][A-Za-z0-9\s\(\)\-]+?)\*\*", line):
                t = _normalize(m.group(1))
                if t and t not in IGNORED_TERMS and len(t) > 3:
                    terms.add(t)

    return terms


def load_glossary_terms() -> set[str]:
    if not GLOSSARY_PATH.exists():
        return set()
    text = GLOSSARY_PATH.read_text(encoding="utf-8")
    return _extract_terms_from_text(text, include_all_bold=False)


def load_registry() -> dict:
    if not REGISTRY_PATH.exists():
        return {"protected_terms": [], "required_by_module": {}}
    try:
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Warning: could not load registry: {exc}")
        return {"protected_terms": [], "required_by_module": {}}


def scan_all_50_design_docs(include_all_bold: bool = False) -> dict[str, set[str]]:
    """Return mapping of relative design file -> set of observed terms."""
    observed: dict[str, set[str]] = {}
    if not DESIGN_DIR.exists():
        return observed

    for md in sorted(DESIGN_DIR.rglob("*.md")):
        if md.name == "50.01_50_series_glossary.md":
            continue  # don't count the glossary itself as introducing new terms
        rel = md.relative_to(ROOT).as_posix()
        try:
            text = md.read_text(encoding="utf-8")
            terms = _extract_terms_from_text(text, include_all_bold=include_all_bold)
            if terms:
                observed[rel] = terms
        except Exception:
            pass
    return observed


def main() -> int:
    parser = argparse.ArgumentParser(description="Propose 50-series glossary updates (read-only by default).")
    parser.add_argument("--write-proposals", action="store_true",
                        help="Write proposal files for review (still does not auto-apply).")
    parser.add_argument("--include-all-bold", action="store_true",
                        help="Also consider more generic **bold** terms (can increase noise).")
    args = parser.parse_args()

    print("=== 50-Series Glossary Freshness Report ===")
    print(f"Generated: {datetime.now().isoformat()}")
    print()

    glossary_terms = load_glossary_terms()
    registry = load_registry()
    protected = {_normalize(t) for t in registry.get("protected_terms", [])}
    required_by_module = registry.get("required_by_module", {})

    observed_by_file = scan_all_50_design_docs(include_all_bold=args.include_all_bold)

    # All observed terms across 50 design docs
    all_observed: set[str] = set()
    for terms in observed_by_file.values():
        all_observed.update(terms)

    print(f"Terms currently in 50.01_50_series_glossary.md: {len(glossary_terms)}")
    print(f"Protected terms in registry: {len(protected)}")
    print(f"Unique terms observed in 50 design documents: {len(all_observed)}")
    print()

    # === Missing from glossary (but seen in docs or declared) ===
    declared = set()
    for terms in required_by_module.values():
        declared.update(_normalize(t) for t in terms)
    declared.update(protected)

    missing_from_glossary = sorted((all_observed | declared) - glossary_terms)
    if missing_from_glossary:
        print("=== PROPOSED ADDITIONS TO GLOSSARY (review and decide) ===")
        for term in missing_from_glossary:
            # Try to find a source file for context
            sources = [f for f, ts in observed_by_file.items() if term in ts]
            source_note = f"  (seen in: {', '.join(sources[:3])})" if sources else ""
            print(f"- **{term.title()}** | TODO: add definition here{source_note}")
        print()
        print("Suggestion: Copy the lines above into 50.01_50_series_glossary.md (in the table) and fill in good definitions.")
        print()

    # === Terms in glossary but not observed/declared (possible cleanup) ===
    extra_in_glossary = sorted(glossary_terms - (all_observed | declared))
    if extra_in_glossary:
        print("=== TERMS IN GLOSSARY BUT NOT OBSERVED IN CURRENT 50 DESIGN DOCS ===")
        for term in extra_in_glossary:
            print(f"- {term}   (consider: keep as protected, or remove if no longer relevant)")
        print()

    # === Registry suggestions ===
    print("=== REGISTRY SUGGESTIONS ===")
    # For files that have observed terms not yet declared for them
    for rel_file, terms in sorted(observed_by_file.items()):
        key = Path(rel_file).name  # e.g. "50.43_gb_design_spec.md"
        current = set(_normalize(t) for t in required_by_module.get(key, []))
        new_for_this = sorted(terms - current - protected)
        if new_for_this:
            print(f"Add to required_by_module['{key}']:")
            for t in new_for_this:
                print(f"  - {t}")
    print()

    if not missing_from_glossary and not extra_in_glossary:
        print("No obvious glossary drift detected from current 50 design documents.")
    else:
        print("Review the proposals above. Only apply what makes sense for the project.")

    # Optional: write proposal artifacts for easy review / partial application
    if args.write_proposals:
        proposals_dir = DESIGN_DIR
        # Proposed glossary additions
        add_lines = []
        for term in missing_from_glossary:
            sources = [f for f, ts in observed_by_file.items() if term in ts]
            source_comment = f"  <!-- seen in {', '.join(sources[:2])} -->" if sources else ""
            add_lines.append(f"| **{term.title()}** | TODO: definition{source_comment} |")

        if add_lines:
            prop_file = proposals_dir / "PROPOSED_50_glossary_additions.md"
            prop_file.write_text(
                "# Proposed additions to 50.01_50_series_glossary.md\n"
                "# Review, edit definitions, then merge the rows you want.\n\n"
                + "\n".join(add_lines) + "\n",
                encoding="utf-8"
            )
            print(f"\nWrote: {prop_file.relative_to(ROOT)}")

        # Proposed registry update (delta style)
        registry_updates = {}
        for rel_file, terms in observed_by_file.items():
            key = Path(rel_file).name
            current = set(_normalize(t) for t in required_by_module.get(key, []))
            new_terms = sorted(terms - current - protected)
            if new_terms:
                registry_updates[key] = new_terms

        if registry_updates or missing_from_glossary:
            prop_reg = proposals_dir / "PROPOSED_50_registry_updates.json"
            payload = {
                "note": "Review and merge selectively into glossary_term_registry.json. protected_terms and required_by_module shown here are suggestions.",
                "suggested_protected_additions": sorted(missing_from_glossary),
                "suggested_required_by_module_additions": registry_updates,
            }
            prop_reg.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print(f"Wrote: {prop_reg.relative_to(ROOT)}")

        print("\nProposal files written. Review them, then manually edit the real glossary and registry as desired.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
