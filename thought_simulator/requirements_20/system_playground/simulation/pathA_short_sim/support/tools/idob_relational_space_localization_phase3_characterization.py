from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from typing import Dict, List, Tuple


NS = [32, 64, 128, 256]
OVERLAPS = [0.0, 0.10, 0.25, 0.50]
KS = [1, 2, 3, 4]
GROUPS = tuple("G_{}".format(i) for i in range(1, 9))


def _rid(index: int) -> str:
    return "r_{}".format(index)


def _rid_sort_key(rid: str) -> int:
    return int(rid.split("_", 1)[1])


def _ordered_rids(n: int) -> List[str]:
    return [_rid(i) for i in range(n)]


def _base_memberships(n: int) -> Dict[str, List[str]]:
    groups = {g: [] for g in GROUPS}
    for j, rid in enumerate(_ordered_rids(n)):
        group = "G_{}".format((j % 8) + 1)
        groups[group].append(rid)
    return groups


def _memberships_with_overlap(n: int, overlap: float) -> Dict[str, List[str]]:
    relation_to_groups: Dict[str, List[str]] = {}
    for j, rid in enumerate(_ordered_rids(n)):
        relation_to_groups[rid] = ["G_{}".format((j % 8) + 1)]

    n_overlap = round(overlap * n)
    selected = _ordered_rids(n)[:n_overlap]
    for rid in selected:
        base = relation_to_groups[rid][0]
        base_index = int(base.split("_", 1)[1])
        nxt = "G_{}".format((base_index % 8) + 1)
        relation_to_groups[rid].append(nxt)

    groups = {g: [] for g in GROUPS}
    for rid in _ordered_rids(n):
        for group in relation_to_groups[rid]:
            groups[group].append(rid)
    return groups


def _necessary_set(n: int) -> List[str]:
    q_n = max(4, round(0.125 * n))
    return [_rid((5 * j + 3) % n) for j in range(q_n)]


def _dedupe_with_trace(sequence: List[str]) -> Tuple[List[str], List[str]]:
    seen = set()
    unique: List[str] = []
    removed: List[str] = []
    for rid in sequence:
        if rid in seen:
            removed.append(rid)
            continue
        seen.add(rid)
        unique.append(rid)
    return unique, removed


@dataclass(frozen=True)
class Metrics:
    reduction: float
    coverage: float
    unnecessary_inclusion_count: int
    unnecessary_inclusion_fraction: float


def _active_record(
    fixture_id: str,
    n: int,
    overlap: float,
    k: int,
    activation_type: str,
    activation_groups: Tuple[str, ...],
    groups: Dict[str, List[str]],
    necessary: List[str],
) -> Dict[str, object]:
    pre_union_memberships = {g: list(groups[g]) for g in activation_groups}
    pre_dedup: List[str] = []
    for g in activation_groups:
        pre_dedup.extend(groups[g])
    final_active, duplicates_removed = _dedupe_with_trace(pre_dedup)

    necessary_set = set(necessary)
    active_set = set(final_active)
    admitted_necessary = [rid for rid in final_active if rid in necessary_set]
    excluded_necessary = [rid for rid in necessary if rid not in active_set]
    unnecessary_admitted = [rid for rid in final_active if rid not in necessary_set]

    reduction = 1.0 - (len(final_active) / float(n))
    coverage = 0.0 if not necessary else (len(admitted_necessary) / float(len(necessary)))
    unnecessary_fraction = (
        0.0 if not final_active else (len(unnecessary_admitted) / float(len(final_active)))
    )
    fingerprint_payload = {
        "fixture_id": fixture_id,
        "n": n,
        "o": overlap,
        "k": k,
        "activation_type": activation_type,
        "activated_groups": activation_groups,
        "pre_union_memberships": pre_union_memberships,
        "pre_deduplication_sequence": pre_dedup,
        "duplicates_removed": duplicates_removed,
        "final_active_relations": final_active,
        "necessary_admitted": admitted_necessary,
        "necessary_excluded": excluded_necessary,
        "unnecessary_admitted": unnecessary_admitted,
        "reduction": reduction,
        "coverage": coverage,
    }
    digest = sha256(json.dumps(fingerprint_payload, sort_keys=True).encode("utf-8")).hexdigest()
    return {
        "fixture_id": fixture_id,
        "n": n,
        "o": overlap,
        "k": k,
        "activation_type": activation_type,
        "activated_groups": list(activation_groups),
        "group_membership_identities_before_union": pre_union_memberships,
        "pre_deduplication_identity_sequence": pre_dedup,
        "duplicate_identities_removed": duplicates_removed,
        "final_active_relation_identities": final_active,
        "necessary_identities_admitted": admitted_necessary,
        "necessary_identities_excluded": excluded_necessary,
        "unnecessary_identities_admitted": unnecessary_admitted,
        "pre_deduplication_count": len(pre_dedup),
        "deduplication_count": len(duplicates_removed),
        "active_relation_count": len(final_active),
        "activated_group_count": len(activation_groups),
        "reduction": reduction,
        "coverage": coverage,
        "unnecessary_inclusion_count": len(unnecessary_admitted),
        "unnecessary_inclusion_fraction": unnecessary_fraction,
        "deterministic_fingerprint": digest,
    }


def _dominates(candidate: Dict[str, object], baseline: Dict[str, object]) -> bool:
    c_r = float(candidate["reduction"])
    b_r = float(baseline["reduction"])
    c_c = float(candidate["coverage"])
    b_c = float(baseline["coverage"])
    return (c_r >= b_r and c_c >= b_c) and (c_r > b_r or c_c > b_c)


def _pick_candidate(activation_records: List[Dict[str, object]]) -> Dict[str, object]:
    sorted_records = sorted(
        activation_records,
        key=lambda r: (
            -float(r["coverage"]),
            -float(r["reduction"]),
            tuple(r["activated_groups"]),
        ),
    )
    return sorted_records[0]


def _false_exclusion_pressures(n: int, necessary_size: int) -> List[int]:
    values = [0, 1, 2, necessary_size // 2]
    return sorted(set(values))


def _candidate_condition_key(condition: Dict[str, object]) -> str:
    return "{}|{}|{}".format(condition["n"], condition["o"], condition["k"])


def _build_phase3_payload() -> Dict[str, object]:
    all_base_conditions: List[Dict[str, object]] = []
    all_false_exclusion: List[Dict[str, object]] = []
    replay_fingerprints: Dict[str, str] = {}
    exhaustive_completed = True

    for n in NS:
        for overlap in OVERLAPS:
            groups = _memberships_with_overlap(n, overlap)
            necessary = _necessary_set(n)
            for k in KS:
                fixture_id = "phase3_n{}_o{}_k{}".format(n, str(overlap), k)
                all_activations = list(combinations(GROUPS, k))
                records = [
                    _active_record(
                        fixture_id=fixture_id,
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
                candidate = _pick_candidate(records)
                baselines = [
                    r
                    for r in records
                    if tuple(r["activated_groups"]) != tuple(candidate["activated_groups"])
                ]
                expected_baselines = len(all_activations) - 1
                exhaustive_ok = len(baselines) == expected_baselines
                exhaustive_completed = exhaustive_completed and exhaustive_ok
                dominates_all = all(_dominates(candidate, b) for b in baselines)
                nontrivial = (
                    0 < int(candidate["active_relation_count"]) < n
                    and len(necessary) > 0
                    and len(candidate["necessary_identities_admitted"]) > 0
                    and len(candidate["necessary_identities_excluded"]) > 0
                    and dominates_all
                )
                condition = {
                    "fixture_id": fixture_id,
                    "n": n,
                    "o": overlap,
                    "k": k,
                    "r_total_size": n,
                    "r_necessary_size": len(necessary),
                    "group_membership_counts": {g: len(groups[g]) for g in GROUPS},
                    "requested_overlap": overlap,
                    "realized_overlap_count": round(overlap * n),
                    "realized_overlap_fraction": (round(overlap * n) / float(n)),
                    "candidate_record": candidate,
                    "matched_activation_count": len(all_activations),
                    "expected_matched_activation_count": len(all_activations),
                    "matched_baseline_count_excluding_candidate": len(baselines),
                    "expected_baseline_count_excluding_candidate": expected_baselines,
                    "exhaustive_matched_baseline_complete": exhaustive_ok,
                    "candidate_dominates_every_nonidentical_matched_activation": dominates_all,
                    "candidate_pareto_relationship": (
                        "dominates_all_nonidentical" if dominates_all else "does_not_dominate_all_nonidentical"
                    ),
                    "nontrivial_useful_domain": nontrivial,
                    "matched_baseline_records": baselines,
                }
                replay_fingerprints[_candidate_condition_key(condition)] = str(
                    candidate["deterministic_fingerprint"]
                )
                all_base_conditions.append(condition)

                candidate_activation = tuple(candidate["activated_groups"])
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
                                "f": f,
                                "status": "NOT_CONSTRUCTIBLE",
                                "constructibility_reason": {
                                    "covered_necessary_available": len(c_set),
                                    "covered_necessary_required": f,
                                    "eligible_unreachable_available": len(u_eligible),
                                    "eligible_unreachable_required": f,
                                },
                                "base_candidate_activation": list(candidate_activation),
                                "base_candidate_coverage": candidate["coverage"],
                                "base_candidate_reduction": candidate["reduction"],
                            }
                        )
                        continue

                    derivative_necessary = sorted(
                        (set(necessary).difference(c_f)).union(u_f),
                        key=_rid_sort_key,
                    )
                    derivative_records = [
                        _active_record(
                            fixture_id=derivative_id,
                            n=n,
                            overlap=overlap,
                            k=k,
                            activation_type="matched_activation_false_exclusion",
                            activation_groups=activation,
                            groups=groups,
                            necessary=derivative_necessary,
                        )
                        for activation in all_activations
                    ]
                    derivative_candidate = next(
                        r for r in derivative_records if tuple(r["activated_groups"]) == candidate_activation
                    )
                    derivative_baselines = [
                        r for r in derivative_records if tuple(r["activated_groups"]) != candidate_activation
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
                            "f": f,
                            "status": "CONSTRUCTIBLE",
                            "base_candidate_activation": list(candidate_activation),
                            "replaced_covered_necessary": c_f,
                            "replacement_unreachable_relations": u_f,
                            "derivative_necessary": derivative_necessary,
                            "candidate_record_under_derivative": derivative_candidate,
                            "matched_baseline_records_under_derivative": derivative_baselines,
                            "candidate_dominates_every_nonidentical_matched_activation_under_derivative": derivative_dominance,
                        }
                    )

    replay_second_pass = {}
    for condition in all_base_conditions:
        n = int(condition["n"])
        o = float(condition["o"])
        k = int(condition["k"])
        fixture_id = str(condition["fixture_id"])
        groups = _memberships_with_overlap(n, o)
        necessary = _necessary_set(n)
        records = [
            _active_record(
                fixture_id=fixture_id,
                n=n,
                overlap=o,
                k=k,
                activation_type="matched_activation",
                activation_groups=activation,
                groups=groups,
                necessary=necessary,
            )
            for activation in combinations(GROUPS, k)
        ]
        replay_second_pass[_candidate_condition_key(condition)] = str(
            _pick_candidate(records)["deterministic_fingerprint"]
        )
    replay_ok = replay_fingerprints == replay_second_pass

    identity_checks: List[Dict[str, object]] = []
    for n in NS:
        base_for_n = [c for c in all_base_conditions if int(c["n"]) == n]
        target = next(
            (c for c in base_for_n if "G_1" in tuple(c["candidate_record"]["activated_groups"])),
            base_for_n[0],
        )
        o = float(target["o"])
        k = int(target["k"])
        base_groups = _memberships_with_overlap(n, o)
        g1_members = list(base_groups["G_1"])
        g1a = [rid for idx, rid in enumerate(g1_members) if idx % 2 == 0]
        g1b = [rid for idx, rid in enumerate(g1_members) if idx % 2 == 1]
        split_groups = {g: list(members) for g, members in base_groups.items() if g != "G_1"}
        split_groups["G_1a"] = g1a
        split_groups["G_1b"] = g1b

        before_candidate = dict(target["candidate_record"])
        before_activation = tuple(before_candidate["activated_groups"])
        after_activation: List[str] = []
        for g in before_activation:
            if g == "G_1":
                after_activation.extend(["G_1a", "G_1b"])
            else:
                after_activation.append(g)
        necessary = _necessary_set(n)
        after_record = _active_record(
            fixture_id="identity_split_n{}".format(n),
            n=n,
            overlap=o,
            k=k,
            activation_type="identity_stability_after_split",
            activation_groups=tuple(after_activation),
            groups=split_groups,
            necessary=necessary,
        )
        before_admitted = list(before_candidate["necessary_identities_admitted"])
        after_admitted = list(after_record["necessary_identities_admitted"])
        identity_stable = set(before_admitted) == set(after_admitted)
        attributable_only = set(before_candidate["final_active_relation_identities"]) == set(
            after_record["final_active_relation_identities"]
        )
        identity_checks.append(
            {
                "n": n,
                "base_fixture_id": target["fixture_id"],
                "split_group": "G_1",
                "replacement_groups": ["G_1a", "G_1b"],
                "before_candidate_trace": before_candidate,
                "after_candidate_trace": after_record,
                "admitted_identity_stable": identity_stable,
                "active_surface_change_attributable_only_to_organization_or_activation": attributable_only,
            }
        )

    overlap_distinguishable = False
    for n in NS:
        for k in KS:
            candidates = [
                c["candidate_record"]
                for c in all_base_conditions
                if int(c["n"]) == n and int(c["k"]) == k
            ]
            sig = {(int(r["active_relation_count"]), float(r["coverage"]), float(r["reduction"])) for r in candidates}
            if len(sig) > 1:
                overlap_distinguishable = True
                break
        if overlap_distinguishable:
            break

    activation_distinguishable = False
    for n in NS:
        for o in OVERLAPS:
            candidates = [
                c["candidate_record"]
                for c in all_base_conditions
                if int(c["n"]) == n and float(c["o"]) == float(o)
            ]
            sig = {(int(r["active_relation_count"]), float(r["coverage"]), float(r["reduction"])) for r in candidates}
            if len(sig) > 1:
                activation_distinguishable = True
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

    identity_ok = all(
        bool(x["admitted_identity_stable"])
        and bool(x["active_surface_change_attributable_only_to_organization_or_activation"])
        for x in identity_checks
    )

    nontrivial_dominance_exists = any(
        bool(c["nontrivial_useful_domain"]) and bool(c["candidate_dominates_every_nonidentical_matched_activation"])
        for c in all_base_conditions
    )

    insufficient_reasons: List[str] = []
    if not exhaustive_completed:
        insufficient_reasons.append("exhaustive_baseline_comparison_incomplete")
    if not replay_ok:
        insufficient_reasons.append("replay_or_trace_requirements_not_satisfied")
    if not (overlap_distinguishable and activation_distinguishable and false_exclusion_distinguishable):
        insufficient_reasons.append("organizational_contribution_not_mechanically_distinguishable")
    if not identity_ok:
        insufficient_reasons.append("identity_stability_requirement_not_satisfied")

    if insufficient_reasons:
        gate_a = "INSUFFICIENT_EVIDENCE"
        gate_reason = "; ".join(insufficient_reasons)
    elif not nontrivial_dominance_exists:
        gate_a = "STOP_THIS_ABSTRACTION"
        gate_reason = (
            "no tested nontrivial condition satisfied frozen dominance predicate under oracle-only surrogate key"
        )
    else:
        gate_a = "CONTINUE"
        gate_reason = (
            "at least one nontrivial condition satisfied frozen dominance predicate and fixture mechanically distinguished "
            "false exclusion, overlap pressure, activation-count pressure, deterministic replay, and identity preservation"
        )

    return {
        "metadata": {
            "run_utc": datetime.now(timezone.utc).isoformat(),
            "char_type": "idob_relational_space_localization_phase3",
            "char_version": "1.0",
            "scope": "frozen_gate_a_phase3_characterization",
            "oracle_only": True,
        },
        "frozen_parameters": {
            "n_values": NS,
            "group_count": 8,
            "k_values": KS,
            "overlap_values": OVERLAPS,
            "false_exclusion_values_rule": "f in {0,1,2,floor(|R_necessary|/2)}",
            "necessary_set_size_rule": "|R_necessary|=max(4,round(0.125*n))",
            "oracle_rule": "coverage desc, reduction desc, lexicographic groups",
            "baseline_rule": "exhaustive matched by activated-group count only",
            "dominance_rule": "candidate dominates every non-identical matched baseline",
        },
        "base_conditions": all_base_conditions,
        "false_exclusion_conditions": all_false_exclusion,
        "identity_stability_checks": identity_checks,
        "summary": {
            "base_condition_count": len(all_base_conditions),
            "false_exclusion_condition_count": len(all_false_exclusion),
            "false_exclusion_constructible_count": len(false_constructible),
            "false_exclusion_not_constructible_count": len(all_false_exclusion) - len(false_constructible),
            "exhaustive_matched_baselines_completed": exhaustive_completed,
            "replay_pass": replay_ok,
            "identity_stability_pass": identity_ok,
            "overlap_pressure_distinguishable": overlap_distinguishable,
            "activation_pressure_distinguishable": activation_distinguishable,
            "false_exclusion_distinguishable": false_exclusion_distinguishable,
            "nontrivial_dominance_exists": nontrivial_dominance_exists,
            "gate_a_classification": gate_a,
            "gate_a_mechanical_reason": gate_reason,
            "insufficient_evidence_reasons": insufficient_reasons,
        },
        "explicit_non_claims": [
            "no production Path A selector established",
            "no claim Path A possesses oracle information",
            "no meaning or semantic region claims",
            "no contextual support / evidence-specific correspondence claims",
            "no door legality or traversal legality claims",
            "no final IdOB organization or final YAML representation claims",
            "no global thresholds or globally valid localization utility claim",
        ],
    }


def _write_artifact(payload: Dict[str, object]) -> Path:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S") + "__idob_rel_space_localization_phase3"
    runs_dir = (
        Path(__file__).resolve().parents[2]
        / "local_characterization"
        / "sessions"
        / "idob_relational_space_localization_phase3"
        / "runs"
    )
    runs_dir.mkdir(parents=True, exist_ok=True)
    output_path = runs_dir / "{}.json".format(run_id)
    payload["metadata"]["run_id"] = run_id
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path


def main() -> None:
    payload = _build_phase3_payload()
    output = _write_artifact(payload)
    print(str(output))
    print("Gate A: {}".format(payload["summary"]["gate_a_classification"]))
    print("Reason: {}".format(payload["summary"]["gate_a_mechanical_reason"]))


if __name__ == "__main__":
    main()
