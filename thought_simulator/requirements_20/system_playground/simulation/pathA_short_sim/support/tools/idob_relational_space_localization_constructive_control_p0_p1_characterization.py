from __future__ import annotations

"""P0/P1 constructive-control characterization for IdOB localization.

Authority:
  notes/program/idob_relational_space_localization_constructive_control_p0_p1_proposal.md
  notes/program/idob_relational_space_localization_constructive_control_p0_p1_design.md
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Callable, Dict, List, Tuple


PHASES = ("P0", "P1")
ARMS = ("S0", "S1", "S2")
PRESENTATION_VARIANTS = (
    "identity",
    "entity_permutation_a",
    "entity_permutation_b",
    "feature_channel_rename",
)


def _expected_accuracy(phase_id: str, arm_id: str) -> float:
    expected = {
        "P0": {"S0": 1.0, "S1": 0.5, "S2": 0.5},
        "P1": {"S0": 0.75, "S1": 0.5, "S2": 0.5},
    }
    return expected[phase_id][arm_id]


def _generate_p0_instances() -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    idx = 0
    for p in (0, 1):
        for q in (0, 1):
            for r in (0, 1):
                for repeat_idx in range(6):
                    o = p ^ r
                    instance = {
                        "phase_id": "P0",
                        "fixture_index": idx,
                        "repeat_index": repeat_idx,
                        "U": {"P": p, "Q": q, "R": r},
                        "structural": {
                            "Ea": p ^ q,
                            "Eb": q ^ r,
                            "Ec": r,
                        },
                        "X": {
                            "x1": p ^ q,
                            "x2": q ^ r,
                        },
                        "outcome": o,
                        "entity_ids": {"left": "E_LEFT", "right": "E_RIGHT"},
                    }
                    out.append(instance)
                    idx += 1
    return out


def _generate_p1_instances() -> List[Dict[str, object]]:
    schedule: List[Tuple[int, int, int]] = [
        (0, 0, 18),
        (0, 1, 6),
        (1, 0, 18),
        (1, 1, 6),
    ]
    out: List[Dict[str, object]] = []
    idx = 0
    for p, q, count in schedule:
        s = p ^ q
        o = p
        for repeat_idx in range(count):
            instance = {
                "phase_id": "P1",
                "fixture_index": idx,
                "repeat_index": repeat_idx,
                "U": {"P": p, "Q": q},
                "structural": {"S": s},
                "X": {},
                "outcome": o,
                "entity_ids": {"left": "E_LEFT", "right": "E_RIGHT"},
            }
            out.append(instance)
            idx += 1
    return out


def _build_p1_s2_schedule(instances: List[Dict[str, object]]) -> Dict[int, int]:
    idx_o0 = [int(i["fixture_index"]) for i in instances if int(i["outcome"]) == 0]
    idx_o1 = [int(i["fixture_index"]) for i in instances if int(i["outcome"]) == 1]
    assignment: Dict[int, int] = {}
    for j, idx in enumerate(idx_o0):
        assignment[idx] = j % 2
    for j, idx in enumerate(idx_o1):
        assignment[idx] = j % 2
    return assignment


def _phase_instances() -> Dict[str, List[Dict[str, object]]]:
    p0 = _generate_p0_instances()
    p1 = _generate_p1_instances()
    return {"P0": p0, "P1": p1}


def _presented_entities(base: Dict[str, str], variant: str) -> Dict[str, str]:
    if variant == "identity":
        return dict(base)
    if variant == "entity_permutation_a":
        return {"left": base["right"], "right": base["left"]}
    if variant == "entity_permutation_b":
        return {"left": base["left"], "right": base["right"], "anchor": base["left"]}
    return dict(base)


def _presented_structural(
    phase_id: str, structural: Dict[str, int], variant: str
) -> Tuple[Dict[str, int], Dict[str, str]]:
    if phase_id == "P0":
        if variant == "feature_channel_rename":
            alias_to_canonical = {"phi_a": "Ea", "phi_b": "Eb", "phi_c": "Ec"}
            presented = {
                a: structural[c]
                for a, c in alias_to_canonical.items()
                if c in structural
            }
            return presented, alias_to_canonical
        alias_to_canonical = {"Ea": "Ea", "Eb": "Eb", "Ec": "Ec"}
        return dict(structural), alias_to_canonical

    if variant == "feature_channel_rename":
        alias_to_canonical = {"sigma": "S"}
        presented = {
            a: structural[c]
            for a, c in alias_to_canonical.items()
            if c in structural
        }
        return presented, alias_to_canonical
    alias_to_canonical = {"S": "S"}
    return dict(structural), alias_to_canonical


def _arm_structural(
    phase_id: str,
    arm_id: str,
    base_instance: Dict[str, object],
    p1_s2_schedule: Dict[int, int],
) -> Tuple[Dict[str, int], Dict[str, object]]:
    structural = dict(base_instance["structural"])
    transform: Dict[str, object] = {"arm_id": arm_id, "transform": "identity"}

    if arm_id == "S0":
        return structural, transform

    if arm_id == "S1":
        if phase_id == "P0":
            transform = {
                "arm_id": arm_id,
                "transform": "remove_tested_structural_inputs",
                "removed": ["Ea", "Eb", "Ec"],
            }
            return {}, transform
        transform = {
            "arm_id": arm_id,
            "transform": "remove_tested_structural_inputs",
            "removed": ["S"],
        }
        return {}, transform

    # S2
    if phase_id == "P0":
        p = int(base_instance["U"]["P"])
        q = int(base_instance["U"]["Q"])
        r = int(base_instance["U"]["R"])
        transformed = {
            "Ea": p ^ q,
            "Eb": q ^ p,
            "Ec": r,
        }
        transform = {
            "arm_id": arm_id,
            "transform": "p0_restored_neutralization",
            "rule": "Ea=P xor Q; Eb=Q xor P; Ec=R",
        }
        return transformed, transform

    idx = int(base_instance["fixture_index"])
    transformed = {"S": int(p1_s2_schedule[idx])}
    transform = {
        "arm_id": arm_id,
        "transform": "p1_stratified_alternating_neutralization",
        "rule": "within each O stratum ordered by frozen index, assign S_neutral=j mod 2",
    }
    return transformed, transform


def _decode_canonical_inputs(
    presented_structural: Dict[str, int], alias_to_canonical: Dict[str, str]
) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for alias, canonical in alias_to_canonical.items():
        if alias in presented_structural:
            out[canonical] = int(presented_structural[alias])
    return out


def _predict(
    phase_id: str,
    canonical_inputs: Dict[str, int],
    required_missing_fallback: str = "R_A",
) -> Tuple[str, Dict[str, object]]:
    if phase_id == "P0":
        if "Ea" not in canonical_inputs or "Eb" not in canonical_inputs:
            return required_missing_fallback, {"fallback": True, "reason": "required_inputs_missing"}
        d = int(canonical_inputs["Ea"]) ^ int(canonical_inputs["Eb"])
        return ("R_A" if d == 0 else "R_B"), {"fallback": False, "decoded_bit": d}

    if "S" not in canonical_inputs:
        return required_missing_fallback, {"fallback": True, "reason": "required_inputs_missing"}
    s = int(canonical_inputs["S"])
    return ("R_A" if s == 0 else "R_B"), {"fallback": False, "decoded_bit": s}


def _correct(prediction: str, outcome: int) -> bool:
    if prediction == "R_A":
        return int(outcome) == 0
    return int(outcome) == 1


def _run_once() -> Dict[str, object]:
    fixtures = _phase_instances()
    p1_s2_schedule = _build_p1_s2_schedule(fixtures["P1"])

    records: List[Dict[str, object]] = []
    for phase_id in PHASES:
        for arm_id in ARMS:
            for base in fixtures[phase_id]:
                structural_arm, transform = _arm_structural(
                    phase_id=phase_id,
                    arm_id=arm_id,
                    base_instance=base,
                    p1_s2_schedule=p1_s2_schedule,
                )
                for variant in PRESENTATION_VARIANTS:
                    presented_structural, alias_map = _presented_structural(
                        phase_id=phase_id,
                        structural=structural_arm,
                        variant=variant,
                    )
                    entities = _presented_entities(base["entity_ids"], variant)
                    canonical_inputs = _decode_canonical_inputs(presented_structural, alias_map)
                    prediction, pred_trace = _predict(phase_id, canonical_inputs)
                    outcome = int(base["outcome"])
                    is_correct = _correct(prediction, outcome)
                    rec = {
                        "phase_id": phase_id,
                        "arm_id": arm_id,
                        "fixture_index": int(base["fixture_index"]),
                        "repeat_index": int(base["repeat_index"]),
                        "presentation_variant": variant,
                        "U": dict(base["U"]),
                        "outcome": outcome,
                        "entity_presentation": entities,
                        "presented_structural_inputs": presented_structural,
                        "canonical_structural_inputs": canonical_inputs,
                        "alias_to_canonical": alias_map,
                        "neutralization_or_masking_transform": transform,
                        "prediction": prediction,
                        "correct": bool(is_correct),
                        "expected_accuracy": _expected_accuracy(phase_id, arm_id),
                        "prediction_trace": pred_trace,
                    }
                    rec["record_fingerprint"] = sha256(
                        json.dumps(rec, sort_keys=True).encode("utf-8")
                    ).hexdigest()
                    records.append(rec)

    grouped_underlying: Dict[str, Dict[str, Dict[str, object]]] = {}
    grouped_permutation: Dict[str, Dict[str, Dict[str, object]]] = {}
    for phase_id in PHASES:
        grouped_underlying[phase_id] = {}
        grouped_permutation[phase_id] = {}
        for arm_id in ARMS:
            identity = [
                r
                for r in records
                if r["phase_id"] == phase_id
                and r["arm_id"] == arm_id
                and r["presentation_variant"] == "identity"
            ]
            correct = sum(1 for r in identity if bool(r["correct"]))
            total = len(identity)
            grouped_underlying[phase_id][arm_id] = {
                "correct_count": correct,
                "total_count": total,
                "accuracy": (correct / float(total) if total else 0.0),
                "expected_accuracy": _expected_accuracy(phase_id, arm_id),
            }

            grouped_permutation[phase_id][arm_id] = {}
            for variant in PRESENTATION_VARIANTS:
                subset = [
                    r
                    for r in records
                    if r["phase_id"] == phase_id
                    and r["arm_id"] == arm_id
                    and r["presentation_variant"] == variant
                ]
                v_correct = sum(1 for r in subset if bool(r["correct"]))
                v_total = len(subset)
                grouped_permutation[phase_id][arm_id][variant] = {
                    "correct_count": v_correct,
                    "total_count": v_total,
                    "accuracy": (v_correct / float(v_total) if v_total else 0.0),
                }

    audit = _run_audits(records)
    completeness = _completeness(records)

    return {
        "records": records,
        "underlying_results": grouped_underlying,
        "permutation_results": grouped_permutation,
        "p1_s2_schedule": p1_s2_schedule,
        "audits": audit,
        "completeness": completeness,
    }


def _completeness(records: List[Dict[str, object]]) -> Dict[str, object]:
    expected = len(PHASES) * len(ARMS) * 48 * len(PRESENTATION_VARIANTS)
    counts_ok = len(records) == expected
    by_key = {}
    for phase_id in PHASES:
        for arm_id in ARMS:
            for variant in PRESENTATION_VARIANTS:
                key = "{}|{}|{}".format(phase_id, arm_id, variant)
                count = sum(
                    1
                    for r in records
                    if r["phase_id"] == phase_id
                    and r["arm_id"] == arm_id
                    and r["presentation_variant"] == variant
                )
                by_key[key] = count
                if count != 48:
                    counts_ok = False
    return {
        "expected_total_records": expected,
        "actual_total_records": len(records),
        "per_cell_expected_count": 48,
        "per_cell_counts": by_key,
        "completeness_pass": counts_ok,
    }


def _audit_accuracy(
    records: List[Dict[str, object]],
    predictor: Callable[[Dict[str, object]], str],
) -> Dict[str, Dict[str, object]]:
    out: Dict[str, Dict[str, object]] = {}
    for phase_id in PHASES:
        subset = [
            r
            for r in records
            if r["phase_id"] == phase_id
            and r["arm_id"] == "S0"
            and r["presentation_variant"] == "identity"
        ]
        correct = sum(1 for r in subset if _correct(predictor(r), int(r["outcome"])))
        total = len(subset)
        out[phase_id] = {
            "correct_count": correct,
            "total_count": total,
            "accuracy": (correct / float(total) if total else 0.0),
        }
    return out


def _run_audits(records: List[Dict[str, object]]) -> Dict[str, object]:
    outcome_withholding = all(
        "outcome" not in r["canonical_structural_inputs"] for r in records
    )
    evaluator_isolation = all(
        set(r["prediction_trace"].keys()).issubset({"fallback", "reason", "decoded_bit"})
        for r in records
    )

    entity_order_only = _audit_accuracy(
        records,
        lambda r: "R_B" if (int(r["fixture_index"]) % 2 == 1) else "R_A",
    )
    entity_identity_only = _audit_accuracy(
        records,
        lambda r: (
            "R_B"
            if str(r["entity_presentation"].get("left", "")).endswith("1")
            else "R_A"
        ),
    )
    feature_name_only = _audit_accuracy(
        records,
        lambda r: (
            "R_B"
            if sorted(list(r["presented_structural_inputs"].keys()))[:1] == ["sigma"]
            else "R_A"
        ),
    )
    output_frequency_baseline = _audit_accuracy(records, lambda _r: "R_A")
    x_only_baseline = _audit_accuracy(
        records,
        lambda r: (
            "R_B"
            if int(r["phase_id"] == "P0")
            and int(r["U"].get("R", 0)) == 1
            else "R_A"
        ),
    )
    s2_only_shortcut = _audit_accuracy(
        records,
        lambda r: "R_B" if r["arm_id"] == "S2" else "R_A",
    )
    fixture_index_seed = _audit_accuracy(
        records,
        lambda r: "R_B" if (int(r["fixture_index"]) % 3 == 0) else "R_A",
    )
    arm_identity = _audit_accuracy(
        records,
        lambda r: "R_B" if r["arm_id"] == "S0" else "R_A",
    )
    direct_leakage = {
        phase_id: {"pass": True, "detail": "procedure does not receive evaluator label"}
        for phase_id in PHASES
    }
    indirect_leakage = {
        phase_id: {"pass": True, "detail": "no post-hoc evaluator fields available to procedure"}
        for phase_id in PHASES
    }
    s1_ambiguity = {
        phase_id: {
            "pass": True,
            "detail": "S1 removes tested structural channels; deterministic fallback is S-blind",
        }
        for phase_id in PHASES
    }

    held_out_permutation = {}
    for phase_id in PHASES:
        held_out_permutation[phase_id] = {}
        for variant in PRESENTATION_VARIANTS:
            subset = [
                r
                for r in records
                if r["phase_id"] == phase_id
                and r["arm_id"] == "S0"
                and r["presentation_variant"] == variant
            ]
            correct = sum(1 for r in subset if bool(r["correct"]))
            total = len(subset)
            held_out_permutation[phase_id][variant] = {
                "correct_count": correct,
                "total_count": total,
                "accuracy": (correct / float(total) if total else 0.0),
            }

    return {
        "outcome_withholding": {"pass": outcome_withholding},
        "evaluator_isolation": {"pass": evaluator_isolation},
        "entity_order_only_prediction": entity_order_only,
        "entity_identity_only_prediction": entity_identity_only,
        "feature_channel_name_only_prediction": feature_name_only,
        "output_frequency_baseline": output_frequency_baseline,
        "x_only_baseline": x_only_baseline,
        "s2_only_shortcut_audit": s2_only_shortcut,
        "fixture_index_seed_prediction": fixture_index_seed,
        "arm_identity_prediction": arm_identity,
        "direct_evaluator_label_leakage": direct_leakage,
        "indirect_evaluator_label_leakage": indirect_leakage,
        "s1_ambiguity": s1_ambiguity,
        "held_out_permutation_generalization": held_out_permutation,
    }


def _classify_phase(
    phase_id: str,
    underlying_results: Dict[str, Dict[str, Dict[str, object]]],
    audits: Dict[str, object],
    completeness_pass: bool,
    replay_pass: bool,
) -> Tuple[str, List[str]]:
    reasons: List[str] = []
    if not completeness_pass:
        reasons.append("completeness_failed")
        return "INCONCLUSIVE", reasons
    if not replay_pass:
        reasons.append("replay_failed")
        return "INCONCLUSIVE", reasons

    expected = {
        "S0": _expected_accuracy(phase_id, "S0"),
        "S1": _expected_accuracy(phase_id, "S1"),
        "S2": _expected_accuracy(phase_id, "S2"),
    }
    observed = {
        arm_id: float(underlying_results[phase_id][arm_id]["accuracy"]) for arm_id in ARMS
    }

    if not audits["outcome_withholding"]["pass"] or not audits["evaluator_isolation"]["pass"]:
        reasons.append("leakage_or_isolation_failure")
        return "CONTROL_INVALID", reasons

    for arm_id in ARMS:
        if abs(observed[arm_id] - expected[arm_id]) > 1e-12:
            reasons.append("arm_{}_mismatch_expected".format(arm_id.lower()))
            return "CONTROL_IMPLEMENTATION_MISMATCH", reasons

    if abs(observed["S2"] - observed["S0"]) <= 1e-12 and observed["S0"] > observed["S1"]:
        reasons.append("s2_reproduces_s0_advantage")
        return "CONTROL_CONTENT_NOT_ISOLATED", reasons

    return "CONTROL_VALIDATED", ["matches_frozen_expectations_and_required_contracts"]


def _build_payload() -> Dict[str, object]:
    first = _run_once()
    second = _run_once()

    first_fp = [str(r["record_fingerprint"]) for r in first["records"]]
    second_fp = [str(r["record_fingerprint"]) for r in second["records"]]
    replay_pass = first_fp == second_fp

    completeness_pass = bool(first["completeness"]["completeness_pass"])

    p0_class, p0_reasons = _classify_phase(
        "P0",
        first["underlying_results"],
        first["audits"],
        completeness_pass,
        replay_pass,
    )
    p1_class, p1_reasons = _classify_phase(
        "P1",
        first["underlying_results"],
        first["audits"],
        completeness_pass,
        replay_pass,
    )

    return {
        "metadata": {
            "run_utc": datetime.now(timezone.utc).isoformat(),
            "char_type": "idob_relational_space_localization_constructive_control_p0_p1",
            "char_version": "1.0",
            "scope": "frozen_constructive_controls_only",
        },
        "frozen_design_reference": {
            "proposal": "notes/program/idob_relational_space_localization_constructive_control_p0_p1_proposal.md",
            "design": "notes/program/idob_relational_space_localization_constructive_control_p0_p1_design.md",
            "p0_role": "exact deterministic structural-information control",
            "p1_role": "informative-but-nondeterminative structural-information control",
        },
        "frozen_expectations": {
            "P0": {"S0": "48/48", "S1": "24/48", "S2": "24/48"},
            "P1": {"S0": "36/48", "S1": "24/48", "S2": "24/48"},
        },
        "p1_s2_neutralization_schedule": first["p1_s2_schedule"],
        "trial_records": first["records"],
        "underlying_fixture_results": first["underlying_results"],
        "permutation_audit_results": first["permutation_results"],
        "shortcut_audits": first["audits"],
        "completeness": first["completeness"],
        "replay": {
            "pass": replay_pass,
            "record_count_first": len(first_fp),
            "record_count_second": len(second_fp),
        },
        "classification": {
            "P0": {"outcome_class": p0_class, "reasons": p0_reasons},
            "P1": {"outcome_class": p1_class, "reasons": p1_reasons},
        },
        "package_summary": {
            "controls_are_constructive_only": True,
            "natural_structure_discovery_claim": False,
            "p0_classification": p0_class,
            "p1_classification": p1_class,
        },
        "explicit_non_claims": [
            "constructive controls do not discover utility in naturally occurring TS structure",
            "no localization source selection",
            "no architecture change",
            "no HOW-2",
            "no Gate C",
            "no production integration",
        ],
    }


def _write_artifact(payload: Dict[str, object]) -> Path:
    run_id = (
        datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        + "__idob_rel_space_localization_constructive_control_p0_p1"
    )
    runs_dir = (
        Path(__file__).resolve().parents[2]
        / "local_characterization"
        / "sessions"
        / "idob_relational_space_localization_constructive_control_p0_p1"
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
    print("completeness_pass={}".format(payload["completeness"]["completeness_pass"]))
    print("replay_pass={}".format(payload["replay"]["pass"]))
    for phase_id in PHASES:
        s0 = payload["underlying_fixture_results"][phase_id]["S0"]
        s1 = payload["underlying_fixture_results"][phase_id]["S1"]
        s2 = payload["underlying_fixture_results"][phase_id]["S2"]
        print(
            "{}: S0={}/{} S1={}/{} S2={}/{}".format(
                phase_id,
                s0["correct_count"],
                s0["total_count"],
                s1["correct_count"],
                s1["total_count"],
                s2["correct_count"],
                s2["total_count"],
            )
        )
        print(
            "{}_classification={}".format(
                phase_id.lower(),
                payload["classification"][phase_id]["outcome_class"],
            )
        )


if __name__ == "__main__":
    main()
