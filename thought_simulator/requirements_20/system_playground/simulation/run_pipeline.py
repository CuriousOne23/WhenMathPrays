"""Machine-level entry for multi-primitive lineup simulation.

Fills the former 1-byte stub. Does not replace testbenches/run.py.
"""
from __future__ import annotations

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from thought_simulator.requirements_20.system_playground.simulation.ts_kernel.pipeline_runner import (  # noqa: E402
    run_stage,
)
from thought_simulator.requirements_20.system_playground.simulation.ts_kernel.replay import (  # noqa: E402
    freezes_equal,
)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="TS machine-level lineup runner")
    parser.add_argument("stage", help="pipeline directory name under pipelines/")
    parser.add_argument(
        "--fixture",
        default=None,
        help="fixture filename under pipelines/<stage>/fixtures/ (default: first yaml)",
    )
    parser.add_argument(
        "--legality",
        action="store_true",
        help="run legality checks only",
    )
    parser.add_argument(
        "--replay",
        action="store_true",
        help="run twice and compare freeze(tp)",
    )
    args = parser.parse_args(argv)

    result = run_stage(HERE, args.stage, fixture_name=args.fixture, legality_only=args.legality)
    if args.legality:
        print("legality: ok")
        print("names:", ", ".join(result["spec"]))
        return 0

    print("stage:", args.stage)
    print("fixture:", result["fixture_name"])
    print("names:", ", ".join(result["spec"]))
    print("ticks:", len(result["trace"]))
    for row in result["trace"]:
        print("  tick {tick} {name}".format(**row))

    if args.replay:
        second = run_stage(HERE, args.stage, fixture_name=result["fixture_name"])
        ok = freezes_equal(result["freeze"], second["freeze"])
        print("replay:", "identical_freeze" if ok else "MISMATCH")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
