from __future__ import annotations

"""Gate B characterization for IdOB relational-space localization.

Authority:
  notes/program/idob_relational_space_localization_research_plan.md
  notes/program/idob_relational_space_localization_gate_b_design.md

Reuses Gate A fixture construction without rewriting Gate A authority.
Runtime selector S receives only (X_t, k) plus the fixed eight group IDs.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

# Inherited Gate A fixture helpers (same deterministic rules).
from idob_relational_space_localization_phase3_characterization import (
    GROUPS,
    KS,
    NS,
    OVERLAPS,
    _active_record,
    _dominates,
    _false_exclusion_pressures,
    _memberships_with_overlap,
    _necessary_set,
    _ordered_rids,
    _rid_sort_key,
)


Q_LEVELS = ("q0", "q1", "q2", "q3", "q4")


def _group_index(group_id: str) -> int:
    return int(group_id.split("_", 1)[1])


def _single_group_coverage(
    groups: Dict[str, List[str]], necessary: Sequence[str], group_id: str
) -> float:
    if not necessary:
        return 0.0
    active = set(groups[group_id])
    admitted = sum(1 for rid in necessary if rid in active)
    return admitted / float(len(necessary))


def _compute_x_base(groups: Dict[str, List[str]], necessary: Sequence[str]) -> Tuple[int, str, Dict[str, float]]:
    """Fixture-construction only. Must not be called from runtime selector S."""
    coverages = {g: _single_group_coverage(groups, necessary, g) for g in GROUPS}
    # highest single-group coverage; ties → lowest group ID (GROUPS already ascending)
    i_star_group = sorted(GROUPS, key=lambda g: (-coverages[g], _group_index(g)))[0]
    i_star = _group_index(i_star_group)
    x_base = (8 - i_star) % 8
    return x_base, i_star_group, coverages


def runtime_selector_S(X_t: int, k: int) -> Tuple[Tuple[str, ...], Dict[str, int], List[str]]:
    """Provisional HOW runtime selector.

    Allowed inputs only: X_t, requested k, and the eight group IDs.
    Must not receive R_necessary, memberships, coverage, or oracle state.
    """
    if k < 1 or k > 8:
        raise ValueError("k out of range")
    scores = {g: (int(X_t) + _group_index(g)) % 8 for g in GROUPS}
    ranking = sorted(GROUPS, key=lambda g: (-scores[g], g))
    activation = tuple(ranking[:k])
    return activation, scores, list(ranking)


def _compact_baseline(record: Dict[str, object]) -> Dict[str, object]:
    return {
        "activated_groups": list(record["activated_groups"]),
        "reduction": record["reduction"],
        "coverage": record["coverage"],
        "active_relation_count": record["active_relation_count"],
        "deterministic_fingerprint": record["deterministic_fingerprint"],
    }


def _non_deteriorating_improvement(
    candidate: Dict[str, object], baselines: Sequence[Dict[str, object]]
) -> bool:
    """Weak schedule check: no axis deterioration vs any baseline; strict gain vs at least one."""
    if not baselines:
        return False
    c_r = float(candidate["reduction"])
    c_c = float(candidate["coverage"])
    for b in baselines:
        if c_r < float(b["reduction"]) or c_c < float(b["coverage"]):
            return False
    return any(
        c_r > float(b["reduction"]) or c_c > float(b["coverage"]) for b in baselines
    )


def _nontrivial(candidate: Dict[str, object], n: int, necessary: Sequence[str], dominates_all: bool) -> bool:
    return (
        0 < int(candidate["active_relation_count"]) < n
        and len(necessary) > 0
        and len(candidate["necessary_identities_admitted"]) > 0
        and len(candidate["necessary_identities_excluded"]) > 0
        and dominates_all
    )


def _condition_key(n: int, o: float, k: int, q: str) -> str:
    return "{}|{}|{}|{}".format(n, o, k, q)


def _xt_for_q(x_base: int, q: str) -> int:
    offset = int(q[1])
    return (x_base + offset) % 8


def _build_gate_b_payload() -> Dict[str, object]:
    all_base_conditions: List[Dict[str, object]] = []
    all_false_exclusion: List[Dict[str, object]] = []
    replay_fingerprints: Dict[str, str] = {}
    exhaustive_completed = True
    selector_contract_ok = True
    quality_levels_complete = True

    for n in NS:
        for overlap in OVERLAPS:
            groups = _memberships_with_overlap(n, overlap)
            necessary = _necessary_set(n)
            x_base, i_star_group, single_group_coverages = _compute_x_base(groups, necessary)

            for k in KS:
                all_activations = list(combinations(GROUPS, k))
                expected_activation_count = len(all_activations)

                # Exhaustive matched baseline pool (uninformed); metrics use same necessary set.
                baseline_pool = [
                    _active_record(
                        fixture_id="gate_b_baseline_pool_n{}_o{}_k{}".format(n, overlap, k),
                        n=n,
                        overlap=overlap,
                        k=k,
                        activation_type="matched_activation",
                        activation_groups=activation,
                        groups=groups,
                        necessary=necessary,
                    )
                    for activation in all_activations
                ]

                for q in Q_LEVELS:
                    fixture_id = "gate_b_n{}_o{}_k{}_{}".format(n, overlap, k, q)
                    X_t = _xt_for_q(x_base, q)

                    # Runtime information contract: selector sees only X_t and k (+ fixed group IDs).
                    try:
                        activation, scores, ranking = runtime_selector_S(X_t, k)
                    except Exception:
                        selector_contract_ok = False
                        raise

                    candidate = _active_record(
                        fixture_id=fixture_id,
                        n=n,
                        overlap=overlap,
                        k=k,
                        activation_type="gate_b_candidate",
                        activation_groups=activation,
                        groups=groups,
                        necessary=necessary,
                    )
                    # Exclude by group SET: selector ranking order may differ from
                    # combinations() lexicographic order for the same activation.
                    candidate_group_set = frozenset(activation)
                    baselines = [
                        r
                        for r in baseline_pool
                        if frozenset(r["activated_groups"]) != candidate_group_set
                    ]
                    expected_baselines = expected_activation_count - 1
                    exhaustive_ok = len(baselines) == expected_baselines
                    exhaustive_completed = exhaustive_completed and exhaustive_ok
                    dominates_all = all(_dominates(candidate, b) for b in baselines)
                    weak_ok = _non_deteriorating_improvement(candidate, baselines)
                    nontrivial = _nontrivial(candidate, n, necessary, dominates_all)

                    fingerprint_payload = {
                        "fixture_id": fixture_id,
                        "n": n,
                        "o": overlap,
                        "k": k,
                        "q": q,
                        "X_base": x_base,
                        "X_t": X_t,
                        "group_scores": scores,
                        "ordered_group_ranking": ranking,
                        "activated_groups": list(activation),
                        "candidate_fingerprint": candidate["deterministic_fingerprint"],
                    }
                    digest = sha256(
                        json.dumps(fingerprint_payload, sort_keys=True).encode("utf-8")
                    ).hexdigest()

                    condition = {
                        "fixture_id": fixture_id,
                        "n": n,
                        "o": overlap,
                        "k": k,
                        "q": q,
                        "X_base": x_base,
                        "X_t": X_t,
                        "i_star_group": i_star_group,
                        "single_group_coverages": single_group_coverages,
                        "group_scores": scores,
                        "ordered_group_ranking": ranking,
                        "activated_group_ids": list(activation),
                        "r_total_size": n,
                        "r_necessary_size": len(necessary),
                        "requested_overlap": overlap,
                        "realized_overlap_count": round(overlap * n),
                        "realized_overlap_fraction": (round(overlap * n) / float(n)),
                        "candidate_record": candidate,
                        "matched_activation_count": expected_activation_count,
                        "matched_baseline_count_excluding_candidate": len(baselines),
                        "expected_baseline_count_excluding_candidate": expected_baselines,
                        "exhaustive_matched_baseline_complete": exhaustive_ok,
                        "candidate_dominates_every_nonidentical_matched_activation": dominates_all,
                        "non_deteriorating_improvement_vs_all_matched_baselines": weak_ok,
                        "candidate_pareto_relationship": (
                            "dominates_all_nonidentical"
                            if dominates_all
                            else "does_not_dominate_all_nonidentical"
                        ),
                        "nontrivial_useful_domain": nontrivial,
                        "matched_baseline_compact": [_compact_baseline(b) for b in baselines],
                        "gate_b_trace_fingerprint": digest,
                        "runtime_selector_allowed_inputs_only": True,
                    }
                    replay_fingerprints[_condition_key(n, overlap, k, q)] = digest
                    all_base_conditions.append(condition)

                    # False-exclusion derivatives stress the already-chosen Gate B activation.
                    candidate_active = list(candidate["final_active_relation_identities"])
                    c_set = sorted(
                        set(necessary).intersection(candidate_active),
                        key=_rid_sort_key,
                    )
                    u_set = sorted(
                        set(_ordered_rids(n)).difference(candidate_active),
                        key=_rid_sort_key,
                    )
                    for f in _false_exclusion_pressures(n, len(necessary)):
                        derivative_id = "{}__f{}".format(fixture_id, f)
                        c_f = c_set[:f]
                        u_eligible = [rid for rid in u_set if rid not in set(necessary)]
                        u_f = u_eligible[:f]
                        if len(c_set) < f or len(u_f) < f:
                            all_false_exclusion.append(
                                {
                                    "fixture_id": derivative_id,
                                    "base_fixture_id": fixture_id,
                                    "n": n,
                                    "o": overlap,
                                    "k": k,
                                    "q": q,
                                    "f": f,
                                    "status": "NOT_CONSTRUCTIBLE",
                                    "constructibility_reason": {
                                        "covered_necessary_available": len(c_set),
                                        "covered_necessary_required": f,
                                        "eligible_unreachable_available": len(u_eligible),
                                        "eligible_unreachable_required": f,
                                    },
                                    "base_candidate_activation": list(activation),
                                    "base_candidate_coverage": candidate["coverage"],
                                    "base_candidate_reduction": candidate["reduction"],
                                }
                            )
                            continue

                        derivative_necessary = sorted(
                            (set(necessary).difference(c_f)).union(u_f),
                            key=_rid_sort_key,
                        )
                        # Preserve Gate B activation; do not re-run selector or oracle.
                        derivative_candidate = _active_record(
                            fixture_id=derivative_id,
                            n=n,
                            overlap=overlap,
                            k=k,
                            activation_type="gate_b_false_exclusion",
                            activation_groups=activation,
                            groups=groups,
                            necessary=derivative_necessary,
                        )
                        derivative_baselines = [
                            _active_record(
                                fixture_id=derivative_id,
                                n=n,
                                overlap=overlap,
                                k=k,
                                activation_type="matched_activation_false_exclusion",
                                activation_groups=act,
                                groups=groups,
                                necessary=derivative_necessary,
                            )
                            for act in all_activations
                            if frozenset(act) != candidate_group_set
                        ]
                        derivative_dominance = all(
                            _dominates(derivative_candidate, b) for b in derivative_baselines
                        )
                        all_false_exclusion.append(
                            {
                                "fixture_id": derivative_id,
                                "base_fixture_id": fixture_id,
                                "n": n,
                                "o": overlap,
                                "k": k,
                                "q": q,
                                "f": f,
                                "status": "CONSTRUCTIBLE",
                                "base_candidate_activation": list(activation),
                                "replaced_covered_necessary": c_f,
                                "replacement_unreachable_relations": u_f,
                                "derivative_necessary": derivative_necessary,
                                "candidate_record_under_derivative": derivative_candidate,
                                "matched_baseline_compact_under_derivative": [
                                    _compact_baseline(b) for b in derivative_baselines
                                ],
                                "candidate_dominates_every_nonidentical_matched_activation_under_derivative": derivative_dominance,
                            }
                        )

    # Exact replay from identical frozen inputs.
    replay_second_pass: Dict[str, str] = {}
    for n in NS:
        for overlap in OVERLAPS:
            groups = _memberships_with_overlap(n, overlap)
            necessary = _necessary_set(n)
            x_base, _, _ = _compute_x_base(groups, necessary)
            for k in KS:
                for q in Q_LEVELS:
                    fixture_id = "gate_b_n{}_o{}_k{}_{}".format(n, overlap, k, q)
                    X_t = _xt_for_q(x_base, q)
                    activation, scores, ranking = runtime_selector_S(X_t, k)
                    candidate = _active_record(
                        fixture_id=fixture_id,
                        n=n,
                        overlap=overlap,
                        k=k,
                        activation_type="gate_b_candidate",
                        activation_groups=activation,
                        groups=groups,
                        necessary=necessary,
                    )
                    fingerprint_payload = {
                        "fixture_id": fixture_id,
                        "n": n,
                        "o": overlap,
                        "k": k,
                        "q": q,
                        "X_base": x_base,
                        "X_t": X_t,
                        "group_scores": scores,
                        "ordered_group_ranking": ranking,
                        "activated_groups": list(activation),
                        "candidate_fingerprint": candidate["deterministic_fingerprint"],
                    }
                    replay_second_pass[_condition_key(n, overlap, k, q)] = sha256(
                        json.dumps(fingerprint_payload, sort_keys=True).encode("utf-8")
                    ).hexdigest()

    expected_keys = {
        _condition_key(n, o, k, q) for n in NS for o in OVERLAPS for k in KS for q in Q_LEVELS
    }
    if set(replay_fingerprints) != expected_keys or set(replay_second_pass) != expected_keys:
        quality_levels_complete = False
    replay_ok = replay_fingerprints == replay_second_pass and quality_levels_complete

    # Pressure distinguishability.
    def _sig(records: Iterable[Dict[str, object]]) -> set:
        return {
            (int(r["candidate_record"]["active_relation_count"]), float(r["candidate_record"]["coverage"]), float(r["candidate_record"]["reduction"]))
            for r in records
        }

    quality_distinguishable = False
    for n in NS:
        for o in OVERLAPS:
            for k in KS:
                subset = [
                    c
                    for c in all_base_conditions
                    if int(c["n"]) == n and float(c["o"]) == float(o) and int(c["k"]) == k
                ]
                if len(_sig(subset)) > 1:
                    quality_distinguishable = True
                    break
            if quality_distinguishable:
                break
        if quality_distinguishable:
            break

    overlap_distinguishable = False
    for n in NS:
        for k in KS:
            for q in Q_LEVELS:
                subset = [
                    c
                    for c in all_base_conditions
                    if int(c["n"]) == n and int(c["k"]) == k and c["q"] == q
                ]
                if len(_sig(subset)) > 1:
                    overlap_distinguishable = True
                    break
            if overlap_distinguishable:
                break
        if overlap_distinguishable:
            break

    activation_distinguishable = False
    for n in NS:
        for o in OVERLAPS:
            for q in Q_LEVELS:
                subset = [
                    c
                    for c in all_base_conditions
                    if int(c["n"]) == n and float(c["o"]) == float(o) and c["q"] == q
                ]
                if len(_sig(subset)) > 1:
                    activation_distinguishable = True
                    break
            if activation_distinguishable:
                break
        if activation_distinguishable:
            break

    false_constructible = [x for x in all_false_exclusion if x["status"] == "CONSTRUCTIBLE"]
    false_exclusion_distinguishable = any(
        float(x["candidate_record_under_derivative"]["coverage"])
        < float(
            next(
                c["candidate_record"]["coverage"]
                for c in all_base_conditions
                if c["fixture_id"] == x["base_fixture_id"]
            )
        )
        for x in false_constructible
    )

    q0_conditions = [c for c in all_base_conditions if c["q"] == "q0"]
    nontrivial_q0_dominance = [
        c
        for c in q0_conditions
        if bool(c["nontrivial_useful_domain"])
        and bool(c["candidate_dominates_every_nonidentical_matched_activation"])
    ]

    def _level_holds(q: str) -> bool:
        level = [c for c in all_base_conditions if c["q"] == q]
        return any(
            bool(c["candidate_dominates_every_nonidentical_matched_activation"])
            or bool(c["non_deteriorating_improvement_vs_all_matched_baselines"])
            for c in level
        )

    lower_q_hold = {q: _level_holds(q) for q in Q_LEVELS if q != "q0"}
    all_lower_hold = all(lower_q_hold.values()) if lower_q_hold else False
    pressures_distinguishable = (
        quality_distinguishable and overlap_distinguishable and activation_distinguishable
    )

    insufficient_reasons: List[str] = []
    if not selector_contract_ok:
        insufficient_reasons.append("runtime_Xt_independence_or_selector_contract_broken")
    if not quality_levels_complete or len(all_base_conditions) != 320:
        insufficient_reasons.append("quality_levels_incompletely_applied")
        quality_levels_complete = False
    if not exhaustive_completed:
        insufficient_reasons.append("exhaustive_matched_baseline_enumeration_incomplete")
    if not replay_ok:
        insufficient_reasons.append("required_traces_or_replay_not_verified")

    # Mechanical evaluation sequence (gate_b_design §15).
    if insufficient_reasons:
        gate_b = "INSUFFICIENT_EVIDENCE"
        gate_reason = "; ".join(insufficient_reasons)
    elif not nontrivial_q0_dominance:
        gate_b = "NEGATIVE"
        gate_reason = "no tested nontrivial q0 condition satisfied frozen dominance predicate"
    elif not pressures_distinguishable:
        gate_b = "INSUFFICIENT_EVIDENCE"
        gate_reason = "quality_overlap_or_activation_breadth_pressures_not_mechanically_distinguishable"
        insufficient_reasons.append(gate_reason)
    elif all_lower_hold:
        gate_b = "CONTINUE"
        gate_reason = (
            "at least one nontrivial q0 condition satisfied frozen dominance predicate; "
            "quality/overlap/activation pressures distinguishable; "
            "dominance or non-deteriorating improvement holds across all lower q levels"
        )
    else:
        gate_b = "PARTIAL"
        failed = [q for q, ok in lower_q_hold.items() if not ok]
        gate_reason = (
            "nontrivial q0 dominance observed and pressures distinguishable, but "
            "dominance/non-deteriorating improvement failed under lower q levels: {}".format(
                ",".join(failed)
            )
        )

    return {
        "metadata": {
            "run_utc": datetime.now(timezone.utc).isoformat(),
            "char_type": "idob_relational_space_localization_gate_b",
            "char_version": "1.0",
            "scope": "frozen_gate_b_characterization",
            "oracle_only": False,
            "provisional_how": "score(G_i)=(X_t+i) mod 8; rank desc score; tie asc group ID; top-k",
        },
        "frozen_parameters": {
            "n_values": NS,
            "group_count": 8,
            "k_values": KS,
            "overlap_values": OVERLAPS,
            "q_levels": list(Q_LEVELS),
            "expected_base_condition_count": 320,
            "false_exclusion_values_rule": "f in {0,1,2,floor(|R_necessary|/2)}",
            "necessary_set_size_rule": "|R_necessary|=max(4,round(0.125*n))",
            "x_base_rule": "i*=argmax single-group coverage (tie lowest group ID); X_base=(8-i*) mod 8",
            "runtime_selector_allowed_inputs": ["X_t", "eight group IDs", "k"],
            "baseline_rule": "exhaustive matched by activated-group count only; Gate A oracle is not baseline",
            "dominance_rule": "candidate dominates every non-identical matched baseline",
        },
        "base_conditions": all_base_conditions,
        "false_exclusion_conditions": all_false_exclusion,
        "summary": {
            "base_condition_count": len(all_base_conditions),
            "false_exclusion_condition_count": len(all_false_exclusion),
            "false_exclusion_constructible_count": len(false_constructible),
            "false_exclusion_not_constructible_count": len(all_false_exclusion) - len(false_constructible),
            "exhaustive_matched_baselines_completed": exhaustive_completed,
            "quality_levels_complete": quality_levels_complete,
            "replay_pass": replay_ok,
            "runtime_selector_contract_ok": selector_contract_ok,
            "quality_pressure_distinguishable": quality_distinguishable,
            "overlap_pressure_distinguishable": overlap_distinguishable,
            "activation_pressure_distinguishable": activation_distinguishable,
            "false_exclusion_distinguishable": false_exclusion_distinguishable,
            "pressures_distinguishable": pressures_distinguishable,
            "nontrivial_q0_dominance_count": len(nontrivial_q0_dominance),
            "nontrivial_q0_dominance_fixture_ids": [c["fixture_id"] for c in nontrivial_q0_dominance],
            "lower_q_level_holds": lower_q_hold,
            "gate_b_classification": gate_b,
            "gate_b_mechanical_reason": gate_reason,
            "insufficient_evidence_reasons": insufficient_reasons,
        },
        "explicit_non_claims": [
            "no production Path A selector established",
            "no claim Path A can generate X_base",
            "no claim Path A possesses equivalent signal information",
            "no meaning or semantic region claims",
            "no contextual support / evidence-specific correspondence claims",
            "no door legality or traversal legality claims",
            "no final interpretation / Category dependence claims",
            "no final IdOB organization or final YAML representation claims",
            "no global signal thresholds or globally valid localization claim",
        ],
    }


def _write_artifact(payload: Dict[str, object]) -> Path:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S") + "__idob_rel_space_localization_gate_b"
    runs_dir = (
        Path(__file__).resolve().parents[2]
        / "local_characterization"
        / "sessions"
        / "idob_relational_space_localization_gate_b"
        / "runs"
    )
    runs_dir.mkdir(parents=True, exist_ok=True)
    output_path = runs_dir / "{}.json".format(run_id)
    payload["metadata"]["run_id"] = run_id
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path


def main() -> None:
    payload = _build_gate_b_payload()
    output = _write_artifact(payload)
    print(str(output))
    print("Gate B: {}".format(payload["summary"]["gate_b_classification"]))
    print("Reason: {}".format(payload["summary"]["gate_b_mechanical_reason"]))
    print(
        "nontrivial_q0_dominance_count={}".format(
            payload["summary"]["nontrivial_q0_dominance_count"]
        )
    )
    print("replay_pass={}".format(payload["summary"]["replay_pass"]))


if __name__ == "__main__":
    main()
