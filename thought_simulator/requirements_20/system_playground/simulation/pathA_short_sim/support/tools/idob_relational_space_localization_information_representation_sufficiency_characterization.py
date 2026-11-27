from __future__ import annotations

"""Information/Representation Sufficiency characterization for IdOB localization.

Authority:
  notes/program/idob_relational_space_localization_information_representation_sufficiency_proposal.md
  notes/program/idob_relational_space_localization_information_representation_sufficiency_design.md
"""

from datetime import datetime, timezone
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from idob_relational_space_localization_phase3_characterization import (
    GROUPS,
    KS,
    NS,
    OVERLAPS,
    _active_record,
    _dominates,
    _memberships_with_overlap,
    _necessary_set,
    _pick_candidate,
)


LEVELS = ("R0", "R1", "R2", "R3", "R4")


def _group_index(group_id: str) -> int:
    return int(group_id.split("_", 1)[1])


def _group_sort(groups: Iterable[str]) -> List[str]:
    return sorted(groups, key=_group_index)


def _single_group_coverage(
    groups: Dict[str, List[str]], necessary: Sequence[str], group_id: str
) -> float:
    if not necessary:
        return 0.0
    active = set(groups[group_id])
    admitted = sum(1 for rid in necessary if rid in active)
    return admitted / float(len(necessary))


def _r0_token(fixture_id: str, k: int, fingerprint: str) -> str:
    return "gatea-oracle::{}::k{}::fp::{}".format(fixture_id, k, fingerprint)


def _parse_r0_token(token: str) -> Tuple[str, int, str]:
    parts = token.split("::")
    if len(parts) != 5 or parts[0] != "gatea-oracle" or parts[2][:1] != "k" or parts[3] != "fp":
        raise ValueError("invalid_r0_token_format")
    fixture_id = parts[1]
    k_value = int(parts[2][1:])
    fingerprint = parts[4]
    return fixture_id, k_value, fingerprint


def _candidate_nontrivial(candidate: Dict[str, object], n: int, necessary: Sequence[str], dominates_all: bool) -> bool:
    return (
        0 < int(candidate["active_relation_count"]) < n
        and len(necessary) > 0
        and len(candidate["necessary_identities_admitted"]) > 0
        and len(candidate["necessary_identities_excluded"]) > 0
        and dominates_all
    )


def _build_gate_a_fixture_map() -> Dict[str, object]:
    entries: List[Dict[str, object]] = []
    by_token: Dict[str, List[Dict[str, object]]] = {}
    by_fixture: Dict[str, Dict[str, object]] = {}

    for n in NS:
        for overlap in OVERLAPS:
            groups = _memberships_with_overlap(n, overlap)
            necessary = _necessary_set(n)
            for k in KS:
                fixture_id = "phase3_n{}_o{}_k{}".format(n, overlap, k)
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
                    for activation in combinations(GROUPS, k)
                ]
                oracle = _pick_candidate(records)
                baselines = [
                    r
                    for r in records
                    if frozenset(r["activated_groups"]) != frozenset(oracle["activated_groups"])
                ]
                dominates_all = all(_dominates(oracle, b) for b in baselines)
                nontrivial = _candidate_nontrivial(oracle, n, necessary, dominates_all)
                in_primary = bool(nontrivial and dominates_all)
                token = _r0_token(
                    fixture_id=fixture_id,
                    k=k,
                    fingerprint=str(oracle["deterministic_fingerprint"]),
                )
                entry = {
                    "fixture_id": fixture_id,
                    "n": n,
                    "o": overlap,
                    "k": k,
                    "deterministic_fingerprint": str(oracle["deterministic_fingerprint"]),
                    "oracle_activation": list(oracle["activated_groups"]),
                    "gate_a_qualified_domain": in_primary,
                    "gate_a_nontrivial_useful_domain": bool(nontrivial),
                    "gate_a_candidate_dominates_every_nonidentical_matched_activation": bool(dominates_all),
                    "r0_token": token,
                }
                entries.append(entry)
                by_token.setdefault(token, []).append(entry)
                by_fixture[fixture_id] = entry

    duplicate_tokens = sorted([t for t, found in by_token.items() if len(found) != 1])
    map_fingerprint = sha256(
        json.dumps(
            [
                {
                    "fixture_id": e["fixture_id"],
                    "k": e["k"],
                    "deterministic_fingerprint": e["deterministic_fingerprint"],
                    "oracle_activation": e["oracle_activation"],
                    "gate_a_qualified_domain": e["gate_a_qualified_domain"],
                }
                for e in sorted(entries, key=lambda x: x["fixture_id"])
            ],
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()

    return {
        "entries": sorted(entries, key=lambda x: x["fixture_id"]),
        "by_token": by_token,
        "by_fixture": by_fixture,
        "duplicate_tokens": duplicate_tokens,
        "map_fingerprint": map_fingerprint,
    }


def _resolve_r0(token: str, frozen_map_by_token: Dict[str, List[Dict[str, object]]]) -> Dict[str, object]:
    fixture_id_from_token = None
    k_from_token = None
    fp_from_token = None
    parse_ok = True
    parse_error = ""
    try:
        fixture_id_from_token, k_from_token, fp_from_token = _parse_r0_token(token)
    except Exception as exc:  # explicit reporting required
        parse_ok = False
        parse_error = str(exc)

    found = frozen_map_by_token.get(token, [])
    unique = len(found) == 1
    resolved = found[0] if unique else None

    mismatch = False
    if parse_ok and resolved is not None:
        mismatch = not (
            str(resolved["fixture_id"]) == str(fixture_id_from_token)
            and int(resolved["k"]) == int(k_from_token)
            and str(resolved["deterministic_fingerprint"]) == str(fp_from_token)
        )

    if not parse_ok or not unique or mismatch:
        return {
            "resolution_ok": False,
            "parse_ok": parse_ok,
            "parse_error": parse_error,
            "unique_resolution": unique,
            "resolution_count": len(found),
            "fixture_fingerprint_match": (not mismatch and parse_ok and unique),
            "resolved_activation": [],
            "resolved_fixture_id": None,
            "resolved_fingerprint": None,
            "reproduction_status": "R0_EXACT_REPRODUCTION_FAIL",
            "reproduction_fail_reasons": [
                reason
                for reason in [
                    "" if parse_ok else "token_parse_failed",
                    "" if len(found) > 0 else "missing_map_resolution",
                    "" if unique else "duplicate_or_ambiguous_resolution",
                    "" if not mismatch else "fixture_fingerprint_mismatch",
                ]
                if reason
            ],
        }

    return {
        "resolution_ok": True,
        "parse_ok": True,
        "parse_error": "",
        "unique_resolution": True,
        "resolution_count": 1,
        "fixture_fingerprint_match": True,
        "resolved_activation": list(resolved["oracle_activation"]),
        "resolved_fixture_id": resolved["fixture_id"],
        "resolved_fingerprint": resolved["deterministic_fingerprint"],
        "reproduction_status": "R0_EXACT_REPRODUCTION_PASS",
        "reproduction_fail_reasons": [],
    }


def _decode_activation(
    level: str,
    fixture_entry: Dict[str, object],
    groups: Dict[str, List[str]],
    necessary: Sequence[str],
    frozen_map_by_token: Dict[str, List[Dict[str, object]]],
) -> Dict[str, object]:
    k = int(fixture_entry["k"])
    oracle_activation = list(fixture_entry["oracle_activation"])

    if level == "R0":
        token = str(fixture_entry["r0_token"])
        resolved = _resolve_r0(token, frozen_map_by_token)
        decoded = list(resolved["resolved_activation"])
        exact_match = decoded == oracle_activation
        if not exact_match and resolved["resolution_ok"]:
            resolved["reproduction_status"] = "R0_EXACT_REPRODUCTION_FAIL"
            resolved["reproduction_fail_reasons"] = ["decoded_activation_mismatch"]
        encoded = {"token": token}
        return {
            "encoded_representation": encoded,
            "decoded_activation": decoded,
            "r0_resolution": resolved,
            "exact_reproduction_match_to_oracle_activation": bool(
                resolved["resolution_ok"] and exact_match
            ),
        }

    if level == "R1":
        encoded_set = _group_sort(oracle_activation)
        decoded = list(encoded_set)
        return {
            "encoded_representation": {"group_set": encoded_set},
            "decoded_activation": decoded,
            "r0_resolution": None,
            "exact_reproduction_match_to_oracle_activation": decoded == oracle_activation,
        }

    if level == "R2":
        supplied = [_group_sort(oracle_activation)[0]]
        decoded = list(supplied)
        if len(decoded) < k:
            for g in GROUPS:
                if g not in decoded:
                    decoded.append(g)
                if len(decoded) == k:
                    break
        return {
            "encoded_representation": {"partial_group_identity": list(supplied)},
            "decoded_activation": decoded,
            "r0_resolution": None,
            "exact_reproduction_match_to_oracle_activation": decoded == oracle_activation,
        }

    if level == "R3":
        coverages = {g: _single_group_coverage(groups, necessary, g) for g in GROUPS}
        i_star = sorted(GROUPS, key=lambda g: (-coverages[g], _group_index(g)))[0]
        decoded = [i_star]
        if len(decoded) < k:
            for g in GROUPS:
                if g not in decoded:
                    decoded.append(g)
                if len(decoded) == k:
                    break
        return {
            "encoded_representation": {
                "best_single_group_identity": i_star,
                "single_group_coverages": coverages,
            },
            "decoded_activation": decoded,
            "r0_resolution": None,
            "exact_reproduction_match_to_oracle_activation": decoded == oracle_activation,
        }

    # R4
    min_group = _group_sort(oracle_activation)[0]
    class_key = {"k": k, "min_group_id": min_group}
    start = _group_index(min_group)
    ordered = ["G_{}".format(i) for i in range(start, 9)] + ["G_{}".format(i) for i in range(1, start)]
    decoded = []
    for g in ordered:
        if g not in decoded:
            decoded.append(g)
        if len(decoded) == k:
            break
    return {
        "encoded_representation": {"class_key": class_key},
        "decoded_activation": decoded,
        "r0_resolution": None,
        "exact_reproduction_match_to_oracle_activation": decoded == oracle_activation,
    }


def _compact_baseline(record: Dict[str, object]) -> Dict[str, object]:
    return {
        "activated_groups": list(record["activated_groups"]),
        "reduction": record["reduction"],
        "coverage": record["coverage"],
        "active_relation_count": record["active_relation_count"],
        "deterministic_fingerprint": record["deterministic_fingerprint"],
    }


def _evaluate_condition_level(
    level: str,
    fixture_entry: Dict[str, object],
    groups: Dict[str, List[str]],
    necessary: Sequence[str],
    baseline_pool: Sequence[Dict[str, object]],
    frozen_map_by_token: Dict[str, List[Dict[str, object]]],
) -> Dict[str, object]:
    n = int(fixture_entry["n"])
    overlap = float(fixture_entry["o"])
    k = int(fixture_entry["k"])
    fixture_id = str(fixture_entry["fixture_id"])

    decoded_info = _decode_activation(
        level=level,
        fixture_entry=fixture_entry,
        groups=groups,
        necessary=necessary,
        frozen_map_by_token=frozen_map_by_token,
    )
    decoded_activation = tuple(decoded_info["decoded_activation"])
    candidate = _active_record(
        fixture_id="irs_{}_{}".format(level.lower(), fixture_id),
        n=n,
        overlap=overlap,
        k=k,
        activation_type="{}_candidate".format(level.lower()),
        activation_groups=decoded_activation,
        groups=groups,
        necessary=necessary,
    )
    candidate_group_set = frozenset(candidate["activated_groups"])
    baselines = [
        b for b in baseline_pool if frozenset(b["activated_groups"]) != candidate_group_set
    ]
    expected_baselines = len(list(combinations(GROUPS, k))) - 1
    exhaustive_ok = len(baselines) == expected_baselines
    dominates_all = all(_dominates(candidate, b) for b in baselines)

    trace_payload = {
        "level": level,
        "fixture_id": fixture_id,
        "n": n,
        "o": overlap,
        "k": k,
        "encoded_representation": decoded_info["encoded_representation"],
        "decoded_activation": list(decoded_activation),
        "candidate_fingerprint": candidate["deterministic_fingerprint"],
        "gate_a_qualified_domain": bool(fixture_entry["gate_a_qualified_domain"]),
        "r0_reproduction_status": (
            decoded_info["r0_resolution"]["reproduction_status"]
            if decoded_info["r0_resolution"] is not None
            else None
        ),
    }
    trace_fingerprint = sha256(
        json.dumps(trace_payload, sort_keys=True).encode("utf-8")
    ).hexdigest()

    return {
        "representation_level": level,
        "fixture_id": fixture_id,
        "n": n,
        "o": overlap,
        "k": k,
        "gate_a_qualified_domain": bool(fixture_entry["gate_a_qualified_domain"]),
        "gate_a_qualified_basis": {
            "nontrivial_useful_domain": bool(
                fixture_entry["gate_a_nontrivial_useful_domain"]
            ),
            "candidate_dominates_every_nonidentical_matched_activation": bool(
                fixture_entry["gate_a_candidate_dominates_every_nonidentical_matched_activation"]
            ),
        },
        "encoded_representation": decoded_info["encoded_representation"],
        "decoded_activation": list(decoded_activation),
        "exact_reproduction_match_to_oracle_activation": bool(
            decoded_info["exact_reproduction_match_to_oracle_activation"]
        ),
        "r0_token": (
            decoded_info["encoded_representation"]["token"] if level == "R0" else None
        ),
        "r0_map_resolution": decoded_info["r0_resolution"],
        "candidate_record": candidate,
        "matched_baseline_count_excluding_candidate": len(baselines),
        "expected_baseline_count_excluding_candidate": expected_baselines,
        "exhaustive_matched_baseline_complete": exhaustive_ok,
        "candidate_dominates_every_nonidentical_matched_activation": dominates_all,
        "matched_baseline_compact": [_compact_baseline(b) for b in baselines],
        "ordered_trace_fingerprint": trace_fingerprint,
        "k1_equivalence_control_condition": bool(k == 1 and level in ("R2", "R3")),
        "kgt1_information_reduction_condition": bool(k > 1 and level in ("R2", "R3")),
    }


def _build_payload() -> Dict[str, object]:
    frozen_gate_a_map = _build_gate_a_fixture_map()
    entries = list(frozen_gate_a_map["entries"])
    map_by_token = dict(frozen_gate_a_map["by_token"])

    conditions_by_level: Dict[str, List[Dict[str, object]]] = {level: [] for level in LEVELS}
    first_pass_fp: Dict[str, str] = {}

    for fixture_entry in entries:
        n = int(fixture_entry["n"])
        overlap = float(fixture_entry["o"])
        k = int(fixture_entry["k"])
        groups = _memberships_with_overlap(n, overlap)
        necessary = _necessary_set(n)
        baseline_pool = [
            _active_record(
                fixture_id="irs_baseline_pool_{}".format(fixture_entry["fixture_id"]),
                n=n,
                overlap=overlap,
                k=k,
                activation_type="matched_activation",
                activation_groups=activation,
                groups=groups,
                necessary=necessary,
            )
            for activation in combinations(GROUPS, k)
        ]
        for level in LEVELS:
            record = _evaluate_condition_level(
                level=level,
                fixture_entry=fixture_entry,
                groups=groups,
                necessary=necessary,
                baseline_pool=baseline_pool,
                frozen_map_by_token=map_by_token,
            )
            conditions_by_level[level].append(record)
            key = "{}|{}".format(level, fixture_entry["fixture_id"])
            first_pass_fp[key] = str(record["ordered_trace_fingerprint"])

    # Exact replay
    replay_second_fp: Dict[str, str] = {}
    for fixture_entry in entries:
        n = int(fixture_entry["n"])
        overlap = float(fixture_entry["o"])
        k = int(fixture_entry["k"])
        groups = _memberships_with_overlap(n, overlap)
        necessary = _necessary_set(n)
        baseline_pool = [
            _active_record(
                fixture_id="irs_baseline_pool_{}".format(fixture_entry["fixture_id"]),
                n=n,
                overlap=overlap,
                k=k,
                activation_type="matched_activation",
                activation_groups=activation,
                groups=groups,
                necessary=necessary,
            )
            for activation in combinations(GROUPS, k)
        ]
        for level in LEVELS:
            replay_record = _evaluate_condition_level(
                level=level,
                fixture_entry=fixture_entry,
                groups=groups,
                necessary=necessary,
                baseline_pool=baseline_pool,
                frozen_map_by_token=map_by_token,
            )
            key = "{}|{}".format(level, fixture_entry["fixture_id"])
            replay_second_fp[key] = str(replay_record["ordered_trace_fingerprint"])

    expected_condition_count = len(NS) * len(OVERLAPS) * len(KS)
    expected_level_condition_count = expected_condition_count * len(LEVELS)
    replay_key_ok = (
        len(first_pass_fp) == expected_level_condition_count
        and set(first_pass_fp.keys()) == set(replay_second_fp.keys())
    )
    replay_pass = replay_key_ok and (first_pass_fp == replay_second_fp)

    all_records = [r for level in LEVELS for r in conditions_by_level[level]]
    exhaustive_ok = all(bool(r["exhaustive_matched_baseline_complete"]) for r in all_records)

    duplicate_tokens = list(frozen_gate_a_map["duplicate_tokens"])
    r0_records = conditions_by_level["R0"]
    r0_exact_pass = [
        r
        for r in r0_records
        if r["r0_map_resolution"] is not None
        and r["r0_map_resolution"]["reproduction_status"] == "R0_EXACT_REPRODUCTION_PASS"
        and bool(r["exact_reproduction_match_to_oracle_activation"])
    ]
    r0_exact_fail = [r for r in r0_records if r not in r0_exact_pass]

    primary_domain_count = sum(1 for e in entries if bool(e["gate_a_qualified_domain"]))

    insufficient_reasons: List[str] = []
    if duplicate_tokens:
        insufficient_reasons.append("r0_fixture_map_contains_duplicate_tokens")
    if not replay_pass:
        insufficient_reasons.append("required_traces_or_replay_not_verified")
    if not exhaustive_ok:
        insufficient_reasons.append("exhaustive_matched_baseline_enumeration_incomplete")
    if len(entries) != expected_condition_count:
        insufficient_reasons.append("fixture_domain_completeness_failed")
    if len(all_records) != expected_level_condition_count:
        insufficient_reasons.append("level_condition_completeness_failed")
    if len(r0_exact_fail) > 0:
        insufficient_reasons.append("r0_exact_reproduction_not_complete")
    if primary_domain_count == 0:
        insufficient_reasons.append("gate_a_qualified_domain_empty")

    required_controls_ok = len(insufficient_reasons) == 0

    def _classify(level: str) -> Tuple[str, str]:
        records = conditions_by_level[level]
        primary = [r for r in records if bool(r["gate_a_qualified_domain"])]
        if not required_controls_ok:
            return "INCONCLUSIVE", "required controls/completeness not satisfied"
        if not primary:
            return "INCONCLUSIVE", "gate_a_qualified_domain_empty"
        if all(bool(r["candidate_dominates_every_nonidentical_matched_activation"]) for r in primary):
            return "SUFFICIENT_WITHIN_FIXTURE", "frozen leverage criterion satisfied on Gate A-qualified domain"
        return "INSUFFICIENT_WITHIN_FIXTURE", "frozen leverage criterion not satisfied on Gate A-qualified domain"

    level_outcomes = {}
    for level in LEVELS:
        outcome, reason = _classify(level)
        records = conditions_by_level[level]
        primary = [r for r in records if bool(r["gate_a_qualified_domain"])]
        supplemental = [r for r in records if not bool(r["gate_a_qualified_domain"])]
        level_outcomes[level] = {
            "outcome": outcome,
            "reason": reason,
            "primary_domain_condition_count": len(primary),
            "primary_domain_dominance_success_count": sum(
                1
                for r in primary
                if bool(r["candidate_dominates_every_nonidentical_matched_activation"])
            ),
            "supplemental_out_of_domain_condition_count": len(supplemental),
            "supplemental_out_of_domain_dominance_success_count": sum(
                1
                for r in supplemental
                if bool(r["candidate_dominates_every_nonidentical_matched_activation"])
            ),
            "k1_count": sum(1 for r in records if int(r["k"]) == 1),
            "kgt1_count": sum(1 for r in records if int(r["k"]) > 1),
        }

    r2_records = conditions_by_level["R2"]
    r3_records = conditions_by_level["R3"]

    return {
        "metadata": {
            "run_utc": datetime.now(timezone.utc).isoformat(),
            "char_type": "idob_relational_space_localization_information_representation_sufficiency",
            "char_version": "1.0",
            "scope": "frozen_information_representation_sufficiency_characterization",
        },
        "frozen_parameters": {
            "n_values": NS,
            "group_count": 8,
            "k_values": KS,
            "overlap_values": OVERLAPS,
            "representation_levels": list(LEVELS),
            "r0_token_scheme": "gatea-oracle::<fixture_id>::k<k>::fp::<deterministic_fingerprint>",
            "gate_a_qualified_domain_rule": {
                "nontrivial_useful_domain": True,
                "candidate_dominates_every_nonidentical_matched_activation": True,
            },
            "baseline_rule": "exhaustive matched by activated-group count only",
            "dominance_rule": "candidate dominates every non-identical matched baseline",
        },
        "frozen_gate_a_fixture_map": {
            "map_fingerprint": frozen_gate_a_map["map_fingerprint"],
            "entry_count": len(entries),
            "duplicate_tokens": duplicate_tokens,
            "entries": entries,
        },
        "conditions_by_level": conditions_by_level,
        "summary": {
            "applicable_fixture_domain_condition_count": len(entries),
            "expected_applicable_fixture_domain_condition_count": expected_condition_count,
            "gate_a_qualified_domain_condition_count": primary_domain_count,
            "expected_level_condition_count": expected_level_condition_count,
            "actual_level_condition_count": len(all_records),
            "exhaustive_matched_baselines_completed": exhaustive_ok,
            "replay_pass": replay_pass,
            "required_controls_ok": required_controls_ok,
            "insufficient_evidence_reasons": insufficient_reasons,
            "r0_exact_reproduction_pass_count": len(r0_exact_pass),
            "r0_exact_reproduction_fail_count": len(r0_exact_fail),
            "r0_leverage_success_on_primary_domain_count": sum(
                1
                for r in r0_records
                if bool(r["gate_a_qualified_domain"])
                and bool(r["candidate_dominates_every_nonidentical_matched_activation"])
            ),
            "r0_leverage_primary_domain_count": sum(
                1 for r in r0_records if bool(r["gate_a_qualified_domain"])
            ),
            "per_level_outcomes": level_outcomes,
            "r2_k1_control": {
                "condition_count": sum(1 for r in r2_records if int(r["k"]) == 1),
                "exact_reproduction_match_count": sum(
                    1
                    for r in r2_records
                    if int(r["k"]) == 1 and bool(r["exact_reproduction_match_to_oracle_activation"])
                ),
                "dominance_success_count": sum(
                    1
                    for r in r2_records
                    if int(r["k"]) == 1
                    and bool(r["candidate_dominates_every_nonidentical_matched_activation"])
                ),
            },
            "r2_kgt1_information_reduction": {
                "condition_count": sum(1 for r in r2_records if int(r["k"]) > 1),
                "exact_reproduction_match_count": sum(
                    1
                    for r in r2_records
                    if int(r["k"]) > 1 and bool(r["exact_reproduction_match_to_oracle_activation"])
                ),
                "primary_domain_dominance_success_count": sum(
                    1
                    for r in r2_records
                    if int(r["k"]) > 1
                    and bool(r["gate_a_qualified_domain"])
                    and bool(r["candidate_dominates_every_nonidentical_matched_activation"])
                ),
            },
            "r3_k1_behavior": {
                "condition_count": sum(1 for r in r3_records if int(r["k"]) == 1),
                "exact_reproduction_match_count": sum(
                    1
                    for r in r3_records
                    if int(r["k"]) == 1 and bool(r["exact_reproduction_match_to_oracle_activation"])
                ),
                "dominance_success_count": sum(
                    1
                    for r in r3_records
                    if int(r["k"]) == 1
                    and bool(r["candidate_dominates_every_nonidentical_matched_activation"])
                ),
            },
            "r3_kgt1_evidence": {
                "condition_count": sum(1 for r in r3_records if int(r["k"]) > 1),
                "exact_reproduction_match_count": sum(
                    1
                    for r in r3_records
                    if int(r["k"]) > 1 and bool(r["exact_reproduction_match_to_oracle_activation"])
                ),
                "primary_domain_dominance_success_count": sum(
                    1
                    for r in r3_records
                    if int(r["k"]) > 1
                    and bool(r["gate_a_qualified_domain"])
                    and bool(r["candidate_dominates_every_nonidentical_matched_activation"])
                ),
            },
        },
        "explicit_non_claims": [
            "no production Path A selector established",
            "no claim Path A can generate successful representation from production inputs",
            "no claim representation constitutes meaning",
            "no HOW-2 authorization",
            "no Gate C authorization",
            "no production selector or Category/YAML integration authorization",
        ],
    }


def _write_artifact(payload: Dict[str, object]) -> Path:
    run_id = (
        datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        + "__idob_rel_space_localization_info_repr_sufficiency"
    )
    runs_dir = (
        Path(__file__).resolve().parents[2]
        / "local_characterization"
        / "sessions"
        / "idob_relational_space_localization_information_representation_sufficiency"
        / "runs"
    )
    runs_dir.mkdir(parents=True, exist_ok=True)
    output = runs_dir / "{}.json".format(run_id)
    payload["metadata"]["run_id"] = run_id
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output


def main() -> None:
    payload = _build_payload()
    output = _write_artifact(payload)
    print(str(output))
    print("replay_pass={}".format(payload["summary"]["replay_pass"]))
    print("required_controls_ok={}".format(payload["summary"]["required_controls_ok"]))
    print(
        "r0_exact_reproduction_pass={}/{}".format(
            payload["summary"]["r0_exact_reproduction_pass_count"],
            payload["summary"]["applicable_fixture_domain_condition_count"],
        )
    )
    print("primary_domain_conditions={}".format(payload["summary"]["gate_a_qualified_domain_condition_count"]))


if __name__ == "__main__":
    main()
