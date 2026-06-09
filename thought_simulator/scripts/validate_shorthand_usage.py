#!/usr/bin/env python3
"""Validate band-prefix shorthand appears only in governed contexts.

Scans markdown files that have file_rules in shorthand_registry.json.
Reports bare band tokens (e.g. 40.392, 50.50) outside allowlisted patterns.

Mode: warning (exit 0) by default; --strict exits 1 on violations.
"""

from __future__ import annotations

import argparse

from shorthand_patterns import (
    ROOT,
    collect_band_refs,
    find_ungoverned_shorthand,
    iter_md_files,
    load_registry,
    parse_file_rules,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate governed shorthand usage.")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on violations.")
    args = parser.parse_args()

    registry = load_registry()
    rules = parse_file_rules(registry)
    band_refs = collect_band_refs()

    violations: list[str] = []
    files_checked = 0

    for path in iter_md_files():
        rel = path.relative_to(ROOT).as_posix()
        # only check files that have at least one file_rule
        from shorthand_patterns import rules_for_file

        if not rules_for_file(rel, rules):
            continue
        files_checked += 1
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for token, line_no, snippet in find_ungoverned_shorthand(rel, text, band_refs, rules):
            safe = snippet.encode("ascii", errors="replace").decode("ascii")
            violations.append(f"{rel}:{line_no}: ungoverned shorthand '{token}' - {safe}")

    if violations:
        print("Shorthand usage violations (band prefix outside governed contexts):")
        for msg in violations[:100]:
            print(f"  - {msg}")
        if len(violations) > 100:
            print(f"  ... and {len(violations) - 100} more")
        print(f"Checked {files_checked} governed markdown files.")
        return 1 if args.strict else 0

    print(f"Shorthand usage validation passed ({files_checked} governed files checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())