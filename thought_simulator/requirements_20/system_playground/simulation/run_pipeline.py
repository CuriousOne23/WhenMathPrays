"""Machine-level entry for multi-primitive lineup simulation.

Fills the former 1-byte stub. Does not replace testbenches/run.py.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from typing import Any, Dict, List, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from thought_simulator.requirements_20.system_playground.simulation.ts_kernel.pipeline_runner import (  # noqa: E402
    _fixture_path,
    load_fixture_tp,
    load_spec,
    run_stage,
)
from thought_simulator.requirements_20.system_playground.simulation.ts_kernel.registry import (  # noqa: E402
    load,
)
from thought_simulator.requirements_20.system_playground.simulation.ts_kernel.replay import (  # noqa: E402
    freeze,
    freezes_equal,
)


READ_HINTS = {
    "idob": [
        "semantic.identity",
        "semantic.stance",
        "semantic.clarifying",
        "semantic.semantic_core",
        "metadata.identity_metadata",
        "metadata.clarifying_metadata",
        "metadata.semantic_layer_metadata",
        "metadata.expressive_metadata",
        "metadata.normalization_metadata",
        "process.routing_filter",
        "utterance",
        "card_id",
        "idob.card_id",
        "idob.utterance",
    ],
    "mcb": [
        "tp.idob",
        "idob",
        "semantic.identity",
        "semantic.stance",
        "semantic.clarifying",
        "semantic.semantic_core",
        "metadata.identity_metadata",
        "metadata.clarifying_metadata",
        "metadata.context",
        "metadata.context_metadata",
        "metadata.clarifying",
        "metadata.clarifying_metadata",
    ],
}

BASE_WRITE_WALLS = [
    "metadata.clarifying",
    "metadata.geometric_state",
    "process.routing_filter",
]

MCB_EXTRA_WALLS = [
    "idob",
    "semantic.meaning_delta_h",
]


def _normalize_path(path: str) -> str:
    return "idob" if path == "tp.idob" else path


def _split_path(path: str) -> List[str]:
    return [part for part in _normalize_path(path).split(".") if part]


def _path_exists(node: Any, path: str) -> bool:
    cur = node
    for part in _split_path(path):
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    return True


def _get_path(node: Any, path: str) -> Any:
    cur = node
    for part in _split_path(path):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _scalar_string(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True, ensure_ascii=True)
    except TypeError:
        return repr(value)


def _flatten_values(node: Any, base: str = "", out: Dict[str, Any] | None = None) -> Dict[str, Any]:
    if out is None:
        out = {}
    if isinstance(node, dict):
        if not node and base:
            out[base] = {}
            return out
        for key in sorted(node.keys()):
            child = node[key]
            next_base = key if not base else "{0}.{1}".format(base, key)
            _flatten_values(child, next_base, out)
        return out
    if isinstance(node, list):
        if not node and base:
            out[base] = []
            return out
        for idx, item in enumerate(node):
            next_base = "{0}[{1}]".format(base, idx) if base else "[{0}]".format(idx)
            _flatten_values(item, next_base, out)
        return out
    out[base] = node
    return out


def _diff_fields(before: Dict[str, Any], after: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    bflat = _flatten_values(before)
    aflat = _flatten_values(after)
    changed = sorted(path for path in aflat if bflat.get(path) != aflat.get(path))
    mutated = sorted(path for path in changed if path in bflat)
    return changed, mutated


def _changed_path(before: Dict[str, Any], after: Dict[str, Any], root_path: str) -> bool:
    return _get_path(before, root_path) != _get_path(after, root_path)


def _print_written_values(tp: Dict[str, Any], written_paths: List[str]) -> None:
    print("  written field contents:")
    if not written_paths:
        print("    - (none)")
        return
    flat = _flatten_values(tp)
    for path in written_paths:
        print("    - {0}: {1}".format(path, _scalar_string(flat.get(path))))


def _print_summary_block(
    name: str,
    read_paths: List[str],
    written_paths: List[str],
    mutated_paths: List[str],
    wall_violations: List[str],
) -> None:
    print("  summary:")
    print("    read fields:", len(read_paths))
    print("    written fields:", len(written_paths))
    print("    written field paths:")
    if written_paths:
        for path in written_paths:
            print("      -", path)
    else:
        print("      - (none)")
    print("    mutated fields:")
    if mutated_paths:
        for path in mutated_paths:
            print("      -", path)
    else:
        print("      - (none)")
    if wall_violations:
        print("    write-wall violations:")
        for path in wall_violations:
            print("      -", path)
    else:
        print("    write-wall violations: none")
    print("  end summary for", name)


def _run_verbose_stage(simulation_root: str, stage: str, fixture_name: str | None = None) -> Dict[str, Any]:
    stage_dir = os.path.join(simulation_root, "pipelines", stage)
    if not os.path.isdir(stage_dir):
        raise FileNotFoundError("unknown stage directory: {0}".format(stage_dir))
    spec = load_spec(stage_dir)
    fixture_path = _fixture_path(stage_dir, fixture_name)
    tp = load_fixture_tp(fixture_path)

    print("verbose: on")
    print("stage:", stage)
    print("fixture:", os.path.basename(fixture_path))
    print("names:", ", ".join(spec))
    print("before first primitive tp freeze:", freeze(tp))

    trace: List[Dict[str, Any]] = []
    total_read_paths = set()
    total_written_paths = set()
    all_wall_violations: List[str] = []
    primitive_reports: List[Dict[str, Any]] = []

    for tick, name in enumerate(spec):
        module = load(name)
        before = copy.deepcopy(tp)
        read_hints = READ_HINTS.get(name, [])
        read_paths = sorted(path for path in read_hints if _path_exists(before, path))
        total_read_paths.update(read_paths)

        print("tick {0} {1}".format(tick, name))
        print("  fields read (present read-set):")
        if read_paths:
            for path in read_paths:
                print("    -", path)
        else:
            print("    - (none observed from read hints)")

        tp = module.process(tp, mode="general")
        if not isinstance(tp, dict):
            raise TypeError("{0}.process did not return a dict TP".format(name))

        written_paths, mutated_paths = _diff_fields(before, tp)
        total_written_paths.update(written_paths)

        print("  fields written:")
        if written_paths:
            for path in written_paths:
                print("    -", path)
        else:
            print("    - (none)")
        _print_written_values(tp, written_paths)

        walls = list(BASE_WRITE_WALLS)
        if name == "mcb":
            walls.extend(MCB_EXTRA_WALLS)
        wall_violations = sorted(path for path in walls if _changed_path(before, tp, path))
        for path in wall_violations:
            all_wall_violations.append("{0}:{1}".format(name, path))

        _print_summary_block(name, read_paths, written_paths, mutated_paths, wall_violations)

        primitive_reports.append(
            {
                "name": name,
                "tick": tick,
                "read_paths": read_paths,
                "written_paths": written_paths,
                "mutated_paths": mutated_paths,
                "wall_violations": wall_violations,
            }
        )
        trace.append({"tick": tick, "name": name, "freeze": freeze(tp)})

    print("final summary:")
    print("  total fields written:", len(total_written_paths))
    print("  total fields read:", len(total_read_paths))
    if all_wall_violations:
        print("  write-wall violations:")
        for row in all_wall_violations:
            print("    -", row)
    else:
        print("  write-wall violations: none")
    print("  replay determinism hints:")
    print("    - verbose mode computes deterministic field diffs from before/after TP snapshots")
    print("    - no TP writes are introduced by verbose reporting")
    print("    - legality and replay semantics are unchanged")

    return {
        "tp": tp,
        "spec": spec,
        "trace": trace,
        "freeze": freeze(tp),
        "stage": stage,
        "fixture_name": os.path.basename(fixture_path),
        "fixture_path": fixture_path,
        "verbose_report": {
            "primitive_reports": primitive_reports,
            "total_fields_read": len(total_read_paths),
            "total_fields_written": len(total_written_paths),
            "write_wall_violations": all_wall_violations,
        },
    }


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
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print per-primitive read/write field reports and final summary",
    )
    args = parser.parse_args(argv)

    if args.verbose and not args.legality:
        result = _run_verbose_stage(HERE, args.stage, fixture_name=args.fixture)
    else:
        result = run_stage(HERE, args.stage, fixture_name=args.fixture, legality_only=args.legality)
    if args.legality:
        print("legality: ok")
        print("names:", ", ".join(result["spec"]))
        return 0

    if not args.verbose:
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
        if args.verbose:
            print("replay determinism hint:")
            print("  freeze comparison uses canonical json sort order; verbose output is observational only")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
