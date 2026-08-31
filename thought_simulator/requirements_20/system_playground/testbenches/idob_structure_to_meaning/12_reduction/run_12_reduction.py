from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

RIVAL_ORDER = ["idob_native", "frame_fill", "embed_nn", "dict_lookup"]
CHEAP_RIVALS = {"frame_fill", "embed_nn", "dict_lookup"}

FORBIDDEN_TOKENS = [
    "struct_to_meaning_map.slide.yaml",
    "struct_to_meaning_map.yaml",
    "ranking_weights",
    "meaning_groups",
    "11_idob_core/idob.py",
    "primitives.idob.idob",
    "from thought_simulator.requirements_20.system_playground.primitives.idob import idob",
]

PACKET_KEYS = [
    "structural_key",
    "candidate_group_ids",
    "final_rank_order",
    "selected_group_id",
    "meaning_semantics",
    "meaning_semantics_prime",
    "meaning_delta_h",
    "residue_code",
    "next_key",
    "routing_filter_mutated",
    "contaminated",
]

NAMES = [
    "physicality",
    "sociality",
    "temporality",
    "intentionality",
    "materiality",
    "spatiality",
]


class BenchBroken(RuntimeError):
    pass


def _read_yaml(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


def _load_rival_module(name: str):
    path = HERE / "rivals" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"tb12_{name}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load rival module: {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, path


def _packet_shape(packet: Dict[str, Any]) -> Dict[str, Any]:
    out = {k: packet.get(k) for k in PACKET_KEYS}
    out["candidate_group_ids"] = list(out.get("candidate_group_ids") or [])
    out["final_rank_order"] = list(out.get("final_rank_order") or [])
    out["routing_filter_mutated"] = bool(out.get("routing_filter_mutated", False))
    out["contaminated"] = bool(out.get("contaminated", False))
    return out


def _run_with_context(module: Any, case: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if hasattr(module, "run_with_context") and callable(module.run_with_context):
        pkt, ctx = module.run_with_context(copy.deepcopy(case))
        return _packet_shape(pkt), dict(ctx or {})
    pkt = module.run(copy.deepcopy(case))
    return _packet_shape(pkt), {}


def _static_contaminated(path: Path) -> bool:
    src = path.read_text(encoding="utf-8")
    low = src.lower()
    return any(token.lower() in low for token in FORBIDDEN_TOKENS)


def _born(packet: Dict[str, Any]) -> bool:
    return packet.get("selected_group_id") is not None and packet.get("meaning_semantics") is not None


def _l2(a: Dict[str, Any], b: Dict[str, Any]) -> float:
    if not isinstance(a, dict) or not isinstance(b, dict):
        return 0.0
    return math.sqrt(sum((float(a.get(n, 0.0)) - float(b.get(n, 0.0))) ** 2 for n in NAMES))


def _cie_alpha_map() -> Dict[str, float]:
    cie_path = REPO_ROOT / "thought_simulator" / "requirements_20" / "system_playground" / "primitives" / "idob" / "cie.examples.yaml"
    data = _read_yaml(cie_path)
    rows = data.get("envelopes") or []
    out = {}
    for row in rows:
        out[str(row.get("cie_id"))] = float(row.get("identity_importance") or 0.0)
    out.setdefault("neutral", 0.0)
    return out


def _score_w2(packet: Dict[str, Any]) -> bool:
    return packet.get("selected_group_id") is None and packet.get("meaning_semantics") is None


def _score_w3(packet: Dict[str, Any]) -> bool:
    cands = set(packet.get("candidate_group_ids") or [])
    rank = list(packet.get("final_rank_order") or [])
    if not cands and not rank:
        return True
    if any(r not in cands for r in rank):
        return False
    if not cands and packet.get("selected_group_id") is not None:
        return False
    return True


def _score_w5(packet: Dict[str, Any]) -> bool:
    return packet.get("next_key") is None


def _score_i2(packet: Dict[str, Any], ctx: Dict[str, Any], is_native: bool) -> bool:
    if packet.get("routing_filter_mutated"):
        return False
    if not is_native:
        return True
    before = ctx.get("routing_filter_before")
    after = ctx.get("routing_filter_after")
    return before == after


def _score_w1(left: Dict[str, Any], right: Dict[str, Any]) -> bool:
    lk = left.get("structural_key")
    rk = right.get("structural_key")
    if lk is None and rk is None:
        return False
    return lk == rk


def _score_w4(
    name: str,
    left: Dict[str, Any],
    right: Dict[str, Any],
    left_case: Dict[str, Any],
    right_case: Dict[str, Any],
    cie_alpha: Dict[str, float],
) -> str:
    if not _born(left) or not _born(right):
        return "n/a"

    if left.get("structural_key") != right.get("structural_key"):
        return "FAIL"

    lc = str(left_case.get("cie_id") or "neutral")
    rc = str(right_case.get("cie_id") or "neutral")

    if lc == rc or (lc == "neutral" and rc == "neutral"):
        return "PASS"

    if float(cie_alpha.get(lc, 0.0)) == 0.0 and float(cie_alpha.get(rc, 0.0)) == 0.0:
        return "PASS"

    dist = _l2(left.get("meaning_semantics_prime"), right.get("meaning_semantics_prime"))
    if name == "idob_native":
        return "PASS" if dist > 0.0 else "FAIL"
    return "PASS" if dist > 0.0 else "FAIL"


def _score_i1(left: Dict[str, Any], right: Dict[str, Any], scored_fields: List[str]) -> bool:
    lsub = {k: left.get(k) for k in scored_fields}
    rsub = {k: right.get(k) for k in scored_fields}
    return lsub == rsub


def _mark_contaminated(packet: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(packet)
    out["contaminated"] = True
    return out


def _print_locked_verdict_table(rows: List[Dict[str, Any]]) -> None:
    print("locked verdict table")
    for row in rows:
        print(f"- {row.get('result')}: {row.get('claim')}")


def _evaluate_rival(
    name: str,
    module: Any,
    path: Path,
    fixtures: Dict[str, Any],
    scores: Dict[str, Any],
    cie_alpha: Dict[str, float],
    native_prior_m: Dict[str, Any] | None,
) -> Dict[str, Any]:
    static_contam = _static_contaminated(path) if name in CHEAP_RIVALS else False
    contaminated = static_contam

    failed: List[str] = []
    pair_details: List[str] = []
    cross_notes: List[str] = []

    for case in fixtures.get("singles") or []:
        packet, ctx = _run_with_context(module, case)
        if static_contam:
            packet = _mark_contaminated(packet)
        contaminated = contaminated or bool(packet.get("contaminated"))

        marks = set(case.get("scored") or [])
        if "W2" in marks and not _score_w2(packet):
            failed.append(f"{case['case_id']}:W2")
        if "W3" in marks and not _score_w3(packet):
            failed.append(f"{case['case_id']}:W3")
        if "W5" in marks and not _score_w5(packet):
            failed.append(f"{case['case_id']}:W5")
        if "I2" in marks and not _score_i2(packet, ctx, name == "idob_native"):
            failed.append(f"{case['case_id']}:I2")

    for pair in fixtures.get("pairs") or []:
        left_case = dict(pair.get("left") or {})
        right_case = dict(pair.get("right") or {})

        left_packet, _left_ctx = _run_with_context(module, left_case)
        right_packet, _right_ctx = _run_with_context(module, right_case)

        if static_contam:
            left_packet = _mark_contaminated(left_packet)
            right_packet = _mark_contaminated(right_packet)
        contaminated = contaminated or bool(left_packet.get("contaminated")) or bool(right_packet.get("contaminated"))

        marks = set(pair.get("scored") or [])

        if "W1" in marks and not _score_w1(left_packet, right_packet):
            failed.append(f"{pair['pair_id']}:W1")

        if "W3" in marks and (not _score_w3(left_packet) or not _score_w3(right_packet)):
            failed.append(f"{pair['pair_id']}:W3")

        if "W5" in marks and (not _score_w5(left_packet) or not _score_w5(right_packet)):
            failed.append(f"{pair['pair_id']}:W5")

        if "W4" in marks:
            w4 = _score_w4(name, left_packet, right_packet, left_case, right_case, cie_alpha)
            pair_details.append(f"{pair['pair_id']}:W4={w4}")
            if w4 == "FAIL":
                failed.append(f"{pair['pair_id']}:W4")

        if "I1" in marks:
            replay_fields = list(scores.get("replay_scored_fields") or PACKET_KEYS)
            if not _score_i1(left_packet, right_packet, replay_fields):
                failed.append(f"{pair['pair_id']}:I1")

    for case in fixtures.get("cross") or []:
        cross = dict(case)
        if cross.get("prior_from_case_id") == "R_rock_phys" and native_prior_m is not None:
            cross["prior_M"] = native_prior_m

        packet, ctx = _run_with_context(module, cross)
        if static_contam:
            packet = _mark_contaminated(packet)
        contaminated = contaminated or bool(packet.get("contaminated"))

        if name == "idob_native":
            first_cycle = ctx.get("first_meaning_cycle")
            ok = first_cycle is False
            cross_notes.append(f"{case['case_id']}:native_first_cycle={first_cycle}")
            if not ok:
                failed.append(f"{case['case_id']}:sanity_first_cycle")

    failed = sorted(set(failed))

    if name == "idob_native" and not contaminated and failed:
        raise BenchBroken("BENCH BROKEN")

    return {
        "name": name,
        "contaminated": contaminated,
        "failed": failed,
        "pair_details": pair_details,
        "cross_notes": cross_notes,
    }


def _final_claim(name: str, contaminated: bool, failed: List[str]) -> str:
    if contaminated:
        return "Contaminated. Not a pass. Not a fail. Discard."
    if failed:
        if name == "idob_native":
            return "Bench broken. Stop. Fix idob.py / fixtures first."
        return "That theory is not a sufficient cheaper operator."
    return "Goal v2 fails for that rival. IdOB shrinks toward naming."


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="12_reduction harness")
    parser.add_argument("--json", action="store_true", help="also print a json summary")
    args = parser.parse_args(argv)

    fixtures = _read_yaml(HERE / "fixtures.yaml")
    scores = _read_yaml(HERE / "score_sheet.yaml")
    cie_alpha = _cie_alpha_map()

    native_prior_m = None
    pairs = fixtures.get("pairs") or []
    rock_pair = next((p for p in pairs if p.get("pair_id") == "P_rock_cie"), None)
    if rock_pair:
        native_mod, _native_path = _load_rival_module("idob_native")
        left_case = dict((rock_pair.get("left") or {}))
        left_packet, _ctx = _run_with_context(native_mod, left_case)
        native_prior_m = left_packet.get("meaning_semantics_prime")

    reports: List[Dict[str, Any]] = []

    try:
        for name in RIVAL_ORDER:
            module, path = _load_rival_module(name)
            report = _evaluate_rival(
                name,
                module,
                path,
                fixtures,
                scores,
                cie_alpha,
                native_prior_m,
            )
            reports.append(report)
    except BenchBroken as exc:
        print(str(exc))
        _print_locked_verdict_table(list(scores.get("verdict_table") or []))
        return 1

    print("12_reduction results")
    for report in reports:
        failed = report["failed"]
        contaminated = bool(report["contaminated"])
        print(f"- {report['name']}:")
        print(f"  contaminated: {str(contaminated).lower()}")
        print(f"  failed: {', '.join(failed) if failed else 'none'}")
        if report["pair_details"]:
            print("  pair checks:")
            for row in report["pair_details"]:
                print(f"    - {row}")
        if report["cross_notes"]:
            print("  cross notes:")
            for row in report["cross_notes"]:
                print(f"    - {row}")
        print(f"  claim: {_final_claim(report['name'], contaminated, failed)}")

    cheap_uncontaminated = [r for r in reports if r["name"] in CHEAP_RIVALS and not r["contaminated"]]
    if cheap_uncontaminated and all(r["failed"] for r in cheap_uncontaminated):
        print("global claim:")
        print("- Package does work those styles do not. First conviction. Still not a completed necessity theorem.")

    _print_locked_verdict_table(list(scores.get("verdict_table") or []))

    if args.json:
        print(json.dumps({"reports": reports}, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
