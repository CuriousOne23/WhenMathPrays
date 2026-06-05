#!/usr/bin/env python3
"""
align_design_numbering.py

Purpose:
  Safely align the document numbering scheme across the design-related layers
  (40, 30, 10.50, and 50) so that the same component/macro uses the same numeric
  prefix (the .xx part).

  This script was created to allow low-token-cost, repeatable refactoring of
  the numbering without the AI having to re-analyze the entire project structure
  in every chat session.

It handles:
- File renames for the new uniform scheme.
- Updating all references to old names inside .md files (including User Guides, READMEs,
  cross references, titles/H1s where the old filename appears, LLR ids).
- Updating references inside .py files (imports, strings, comments, docstrings) -- with
  explicit warnings because code changes need extra review.
- Special update for the 50.00 index table.
- After --apply, writes a permanent dated history record in archive/refactors/ for audit.

  - The mappings and rules are defined at the top of this file (easy to edit).
  - It supports --dry-run (default, recommended) which only reports.
  - It can generate a detailed plan of file renames + all in-document reference updates.
  - --apply performs the changes (use with caution; always review --dry-run first).
  - It emits warnings for things that require human judgment.
  - It updates the 50.00 index automatically when relevant.
  - After running, you should still run the full validation suite.

Design goals (per project process):
  - Human control at every step (no silent changes).
  - Warnings for edge cases.
  - Well-documented so future AI sessions or humans can understand/modify the
    script without re-reading dozens of files.
  - Token efficient: run the script locally via terminal; the AI only needs to
    see the output of one command.

Current known drift (as of 2026-06):
  - 50 has extra governance docs at 50.00-50.09 (intended and documented in 50.05).
  - 50.09_geometry_engine_design.md should be 50.10 to align with:
      10.50.10_math_requirements.md
      40.10_math_prototypes/
      30.10_math_prototypes/
  - 50.50_data_structures.md and 50.50_regulator_design_support.md conflict on .50.
    Regulator aligns with 10.50.50 / 40.50 / 30.50, so data structures moves to 50.55.

Component numbering convention (to be documented in 50.05 and 50.00 index):
  .10  Math/Geometry
  .20  TP / Dynamics / TP Lifecycle
  .30  Basin (general)
  .32  COB
  .33  CIL
  .34  COP
  .35  IB
  .36  GB
  .37  TR
  .39  MB
  .40  Scheduler
  .50  Regulator
  .55  Data Structures (chosen to avoid .50 conflict)
  .60  Tick Cycle
  .70  Snapshot
  .80  Event Log
  .90  Experiment Runner
  .100 InB
  .110 OuB

  In 50: 50.00-50.09 are reserved for 50-series governance/intro docs
         (index, glossary, construction guide, system architecture, etc.).
         Component docs then follow the table above.

  Level 2 subs use 50.xx.yy (e.g. 50.36.10)

Usage:
  python thought_simulator/scripts/align_design_numbering.py --dry-run
  python thought_simulator/scripts/align_design_numbering.py --plan          # more detail
  python thought_simulator/scripts/align_design_numbering.py --apply --yes   # after review

The script will refuse to run --apply without --yes, and always prints a summary first.
"""

from __future__ import annotations
import argparse
import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DESIGN_50 = ROOT / "50_thought_simulator_design"

# ============================================================
# CONFIGURATION - Edit this section if the plan changes
# ============================================================

# Files to rename (old relative name -> new relative name)
# Only list files that actually need to change for uniformity.
RENAME_MAP: Dict[str, str] = {
    "50.09_geometry_engine_design.md": "50.10_geometry_engine_design.md",
    "50.50_data_structures.md": "50.55_data_structures.md",
    # 10_ tier placement fixes (use full path from thought_simulator root so the
    # generalized resolver above can handle them). Example of the reported issue:
    # when correcting a GB reqs file that was placed in 10.10 architecture docs
    # but named 10.50.36 (colliding with 10.50.36_gb_design... ), it must become
    # 10.10.36_gb_requirements.md -- the script must NEVER auto-pick e.g. 10.10.60.
    # "10_thought_simulator_req/10_system_architecture/10.50.36_gb_requirements.md":
    #     "10_thought_simulator_req/10_system_architecture/10.10.36_gb_requirements.md",
}

# Additional files whose *content* must be updated even if not renamed
# (e.g. the traceability index that lists the paths)
CONTENT_UPDATE_TARGETS = [
    "50.00_design_traceability_index.md",
]

# Strings that appear in content that must be replaced when the file is renamed.
# The script will do exact string replacement for these in the listed targets + any other .md it finds.
# Be conservative: only unambiguous full references.
REPLACEMENT_PAIRS: List[Tuple[str, str]] = [
    # (old, new)
    ("50.09_geometry_engine_design.md", "50.10_geometry_engine_design.md"),
    ("50.50_data_structures.md", "50.55_data_structures.md"),
    # LLRs that embed the old number (in the geometry file itself)
    ("LLR-50.09-001", "LLR-50.10-001"),
    # 10_ tier example (commented; add basename or full as needed when activating a 10 rename):
    # ("10.50.36_gb_requirements.md", "10.10.36_gb_requirements.md"),
]

# Directories to scan for references (relative to ROOT)
# For broad refactors, include the whole project but exclude archive and caches
SCAN_DIRS = [
    ".",
]

# File extensions to scan for references
SCAN_EXTENSIONS = {".md", ".py"}

# Directories to skip during scanning (to avoid historical noise and caches)
SKIP_DIRS = {"archive", "__pycache__", ".git", "node_modules"}

# Files that are allowed to contain the old names after the refactor (historical reports, etc.)
IGNORE_FILES = {
    "RENAMING_MIGRATION_REPORT.md",
    # add more historical files here if needed
}

# ============================================================
# END CONFIGURATION
# ============================================================


def find_references(old_name: str) -> List[Path]:
    """Find all matching files under SCAN_DIRS that mention the old name.
    Respects SCAN_EXTENSIONS and SKIP_DIRS.
    """
    hits: List[Path] = []
    for rel_dir in SCAN_DIRS:
        base = ROOT / rel_dir
        if not base.exists():
            continue
        for ext in SCAN_EXTENSIONS:
            for p in base.rglob(f"*{ext}"):
                # Skip directories
                rel_parts = p.relative_to(ROOT).parts
                if any(part in SKIP_DIRS for part in rel_parts):
                    continue
                if p.name in IGNORE_FILES:
                    continue
                try:
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    if old_name in text:
                        hits.append(p)
                except Exception as e:
                    print(f"WARNING: Could not read {p}: {e}")
    return hits


def update_file_content(path: Path, replacements: List[Tuple[str, str]]) -> bool:
    """Perform in-place replacements. Returns True if file was changed."""
    try:
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in replacements:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            return True
        return False
    except Exception as e:
        print(f"ERROR updating {path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Align numbering in 50-series design docs with 40/30/10.50 layers."
    )
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Show what would be done (default).")
    parser.add_argument("--plan", action="store_true",
                        help="Show a more detailed plan including all reference locations.")
    parser.add_argument("--apply", action="store_true",
                        help="Actually perform the renames and content updates.")
    parser.add_argument("--yes", action="store_true",
                        help="Skip interactive confirmation for --apply (use only after careful review).")
    args = parser.parse_args()

    if args.apply and not args.yes:
        print("ERROR: --apply requires --yes to confirm you have reviewed the plan.")
        print("First run with --dry-run or --plan.")
        return 1

    print("=== Design Numbering Alignment Plan ===")
    print("This script implements the uniform component numbering discussed for the")
    print("design layers (40, 30, 10.50, 50). 50.00-50.09 remain reserved for")
    print("50-series governance documents per 50.05.")
    print()
    print("POLICY: Nothing happens automatically. You may manually rename files or change")
    print("any internal names (module:, titles, references, etc.) to *anything* you want.")
    print("This script gives warnings/plans only by default and never auto-corrects or")
    print("auto-renames based on what it finds on disk. It only processes the explicit")
    print("entries you have added to RENAME_MAP in the CONFIG section at the top of this file.")
    print("File changes occur ONLY with explicit --apply --yes after you have reviewed the plan.")
    print()

    # 1. Report the intended renames
    print("Planned file renames:")
    renames: List[Tuple[Path, Path]] = []
    for old_rel, new_rel in RENAME_MAP.items():
        # Support both 50-only relative (legacy) and full paths relative to thought_simulator root
        # (for 10_ tier corrections like 10.50.36_gb... in architecture dir -> 10.10.36_... )
        if "/" in old_rel or "\\" in old_rel:
            old = ROOT / old_rel
            new = ROOT / new_rel
        else:
            old = DESIGN_50 / old_rel
            new = DESIGN_50 / new_rel
        if not old.exists():
            print(f"  SKIP (missing): {old_rel}")
            continue
        if new.exists():
            print(f"  ERROR: target already exists: {new_rel}")
            return 1
        renames.append((old, new))
        print(f"  {old_rel}  -->  {new_rel}")

    if not renames:
        print("No renames needed.")
        return 0

    print()

    # 2. Find all references that will need updating
    all_replacements = REPLACEMENT_PAIRS
    affected_files: Dict[Path, List[str]] = {}

    for old_rel, new_rel in RENAME_MAP.items():
        hits = find_references(old_rel)
        for p in hits:
            if p not in affected_files:
                affected_files[p] = []
            affected_files[p].append(f"filename reference: {old_rel} -> {new_rel}")

    # Also check the explicit CONTENT_UPDATE_TARGETS for any of our replacement strings
    for rel in CONTENT_UPDATE_TARGETS:
        p = DESIGN_50 / rel
        if p.exists():
            if p not in affected_files:
                affected_files[p] = []
            affected_files[p].append("listed in 50.00 index / content update target")

    print("Files that will have content updated (in addition to any renames):")
    for p in sorted(affected_files.keys()):
        print(f"  {p.relative_to(ROOT)}")
        if args.plan:
            for note in affected_files[p]:
                print(f"    - {note}")

    print()

    # 3. Special notes / warnings
    print("Warnings / items requiring human review:")
    print("  - LLR identifiers embedded in frontmatter (e.g. LLR-50.09-001) will be updated")
    print("    to LLR-50.10-001 for the geometry file. Review that no external references")
    print("    (outside this repo or in historical docs) rely on the old LLR numbers.")
    print("  - The 50.00 index table will be updated automatically for the two rows.")
    print("  - Historical files like RENAMING_MIGRATION_REPORT.md are intentionally ignored.")
    print("  - **Python files (.py)**: String matches in code, comments, docstrings, or tests")
    print("    will be updated if they contain the old filename. These can have false positives.")
    print("    The script will list them prominently — review carefully before apply.")
    print("  - Titles: If an H1 or frontmatter title contains the old component number or filename,")
    print("    it will be caught by the string replacement (e.g. in links or explicit mentions).")
    print("  - After applying, run the full validation suite (see CONTRIBUTING_CHANGE_WORKFLOW.md).")
    print("  - Consider updating any external notes, old branches, or the 20-series if they")
    print("    hard-code the old 50.09 / 50.50_data names.")
    print("  - User guides, READMEs, and cross-layer references are included in the broad scan.")
    print()

    if args.dry_run and not args.apply:
        print("This was a dry-run. No files were modified.")
        print("Re-run with --plan for more detail, or --apply --yes after review.")
        return 0

    if args.apply:
        print("=== APPLYING CHANGES ===")
        # Perform renames first
        for old, new in renames:
            print(f"Renaming: {old.relative_to(ROOT)} -> {new.relative_to(ROOT)}")
            old.rename(new)

        # Now update content in all affected files (using the new names where renames happened)
        # We need to refresh the replacement list with any remaining old names
        # (the renames above have already happened on disk)
        updated_count = 0
        for p in list(affected_files.keys()):
            # Re-resolve path in case the file itself was renamed
            if p in [r[0] for r in renames]:
                # This file was renamed; find its new location
                for old, new in renames:
                    if old == p:
                        p = new
                        break
            if update_file_content(p, all_replacements):
                print(f"  Updated content in: {p.relative_to(ROOT)}")
                updated_count += 1

        print(f"\nDone. {len(renames)} files renamed, {updated_count} files had content updates.")

        # Write a refactor history record for auditability (as requested for historic tracking)
        from datetime import datetime
        log_dir = ROOT / "archive" / "refactors"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"REFACTOR_NUMBERING_{datetime.now().strftime('%Y-%m-%d')}.md"
        with open(log_file, "w", encoding="utf-8") as lf:
            lf.write(f"# Refactor Log: Design Numbering Alignment\n\n")
            lf.write(f"Date: {datetime.now().isoformat()}\n")
            lf.write(f"Script: scripts/align_design_numbering.py\n\n")
            lf.write("## Renames performed\n")
            for old, new in renames:
                lf.write(f"- `{old.relative_to(ROOT)}` → `{new.relative_to(ROOT)}`\n")
            lf.write("\n## Content files updated\n")
            for p in sorted(affected_files.keys()):
                lf.write(f"- `{p.relative_to(ROOT)}`\n")
            lf.write("\n## Notes\n")
            lf.write("- All changes were driven by the RENAME_MAP and REPLACEMENT_PAIRS in the script.\n")
            lf.write("- Review git diff before committing.\n")
            lf.write("- Run full validation suite after this refactor.\n")
        print(f"Refactor history written to: {log_file.relative_to(ROOT)}")

        print("Next steps:")
        print("  1. git add -A && git status   (review what changed)")
        print("  2. Run the full pre-PR validation suite (see CONTRIBUTING_CHANGE_WORKFLOW.md)")
        print("  3. Update 50.05 if the component numbering table needs a new legend entry.")
        print("  4. Commit with a clear message referencing this script and the log in archive/refactors/.")
        print("  5. The REFACTOR files have been moved to archive/refactors/ to reduce root directory clutter.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
