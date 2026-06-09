#!/usr/bin/env python3
"""Bootstrap identity name tables from current filesystem state.

Usage:
  python thought_simulator/scripts/bootstrap_name_tables.py
  python thought_simulator/scripts/bootstrap_name_tables.py --dry-run
"""

from __future__ import annotations

import argparse
import json

from identity_tables import bootstrap_all_tables, write_bootstrap_tables


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap identity name tables from disk.")
    parser.add_argument("--dry-run", action="store_true", help="Print summary without writing files.")
    args = parser.parse_args()

    tables = bootstrap_all_tables()
    for tier, table in tables.items():
        count = len(table.get("entries", []))
        print(f"{tier}: {count} entries")

    if args.dry_run:
        print("Dry-run complete; no files written.")
        return 0

    write_bootstrap_tables()
    print("Wrote name tables to 00_program_governance/00_identity/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())