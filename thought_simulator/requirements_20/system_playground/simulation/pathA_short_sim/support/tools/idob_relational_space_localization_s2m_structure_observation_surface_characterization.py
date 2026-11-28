from __future__ import annotations

"""Frozen M1-M6 S2M structure-observation-surface characterization.

Authority:
  notes/program/idob_relational_space_localization_s2m_structure_observation_surface_design.md
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Dict, List, Tuple


CELL_ORDER = ("M1", "M2", "M3", "M4", "M5", "M6")


def _load_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _index_by_case(payload: Dict[str, object]) -> Dict[str, Dict[str, object]]:
    return {str(c["case_id"]): c for c in payload["cases"]}


def _safe_int(v: object) -> int:
    return int(v) if v is not None else 0


def _counts_from_lineage_records(records: List[Dict[str, object]]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for r in records:
        key = str(r["correspondence_state"])
        out[key] = out.get(key, 0) + 1
    return out


def _dependency_counts(records: List[Dict[str, object]]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for r in records:
        key = str(r["dependency_state"])
        out[key] = out.get(key, 0) + 1
    return out


def _semantic_cell_records(base_dir: Path) -> Tuple[List[Dict[str, object]], Dict[str, object]]:
    traversal_path = (
        base_dir
        / "local_characterization"
        / "sessions"
        / "s2m_idob_traversal_exp"
        / "runs"
        / "20261125_073021__s2m_idob_traversal_exp.json"
    )
    correspondence_path = (
        base_dir
        / "local_characterization"
        / "sessions"
        / "s2m_idob_correspondence_exp"
        / "runs"
        / "20261125_083313__s2m_idob_correspondence_exp.json"
    )
    lineage_path = (
        base_dir
        / "local_characterization"
        / "sessions"
        / "s2m_idob_lineage_opposition_exp"
        / "runs"
        / "20261125_085112__s2m_idob_lineage_opposition_exp.json"
    )

    traversal = _index_by_case(_load_json(traversal_path))
    correspondence = _index_by_case(_load_json(correspondence_path))
    lineage = _index_by_case(_load_json(lineage_path))

    tc01 = traversal["TC01_support"]
    tc02 = traversal["TC02_no_correspondence"]
    tc04 = traversal["TC04_multi_source_support"]
    tc10 = traversal["TC10_multi_candidate"]
    cr01 = correspondence["CR01_support_record"]
    cr02 = correspondence["CR02_no_relation_record"]
    cr03 = lineage["CR03_unresolved_record"]
    cr06 = lineage["CR06_duplicate_dependency"]
    cr08 = lineage["CR08_independence_unavailable"]

    matrix_records: List[Dict[str, object]] = []

    def _from_traversal(
        cell_id: str,
        condition_class: str,
        case_obj: Dict[str, object],
        support_case_obj: Dict[str, object] | None,
        extra_anchor: Dict[str, str] | None = None,
    ) -> Dict[str, object]:
        cue = list(case_obj["correspondence_observation"]["ce_category_cue"])
        cue_prov = list(case_obj["correspondence_observation"]["ce_cue_provenance"])
        sel_counts = dict(case_obj["correspondence_observation"]["selection_state_counts"])
        cand_count = _safe_int(case_obj["C_t_observation"]["candidate_count"])
        wr_count = _safe_int(case_obj["door_result"]["written_relations_count"])
        support_states = {}
        if support_case_obj is not None:
            for item in support_case_obj["candidate_correspondence"]:
                st = str(item["correspondence_state"])
                support_states[st] = support_states.get(st, 0) + 1

        return {
            "cell_id": cell_id,
            "condition_class": condition_class,
            "authority_anchor": {
                "traversal_case_id": case_obj["case_id"],
                "support_case_id": (support_case_obj["case_id"] if support_case_obj is not None else None),
                "extra_anchor": extra_anchor,
            },
            "surface_seed": {
                "availability_state": "available",
                "written_relations_count": wr_count,
            },
            "surface_candidates": {
                "availability_state": ("available" if cand_count > 0 else "unavailable"),
                "candidate_count": cand_count,
                "selection_state_counts": sel_counts,
            },
            "surface_support": {
                "availability_state": "available",
                "cue_present": len(cue) > 0,
                "cue_values": cue,
                "cue_provenance": cue_prov,
                "support_state_counts": support_states,
                "dependency_state_counts": {},
                "unresolved_count": support_states.get("unresolved", 0),
            },
        }

    def _from_lineage(
        cell_id: str,
        condition_class: str,
        case_obj: Dict[str, object],
        related_traversal_case_id: str | None = None,
    ) -> Dict[str, object]:
        records = list(case_obj["records"])
        support_states = _counts_from_lineage_records(records)
        dependency_states = _dependency_counts(records)
        cand_available = all(str(r["candidate_id"]) != "UNAVAILABLE" for r in records)
        candidate_ids = sorted(
            {str(r["candidate_id"]) for r in records if str(r["candidate_id"]) != "UNAVAILABLE"}
        )
        cue_vals = list(case_obj["available_provenance"]["ce_output"]["category_cue"])
        cue_prov = list(case_obj["available_provenance"]["ce_output"]["cue_provenance"])
        return {
            "cell_id": cell_id,
            "condition_class": condition_class,
            "authority_anchor": {
                "lineage_case_id": case_obj["case_id"],
                "related_traversal_case_id": related_traversal_case_id,
            },
            "surface_seed": {
                "availability_state": "available",
                "written_relations_count": None,
            },
            "surface_candidates": {
                "availability_state": ("available" if cand_available else "unresolved"),
                "candidate_count": len(candidate_ids),
                "selection_state_counts": {},
            },
            "surface_support": {
                "availability_state": ("available" if cand_available else "unresolved"),
                "cue_present": len(cue_vals) > 0,
                "cue_values": cue_vals,
                "cue_provenance": cue_prov,
                "support_state_counts": support_states,
                "dependency_state_counts": dependency_states,
                "unresolved_count": support_states.get("unresolved", 0),
            },
            "source_replay_status": dict(case_obj["replay_status"]),
        }

    matrix_records.append(
        _from_traversal(
            cell_id="M1",
            condition_class="cue_absent_sentence_only_candidate_available",
            case_obj=tc02,
            support_case_obj=cr02,
        )
    )
    matrix_records.append(
        _from_traversal(
            cell_id="M2",
            condition_class="cue_present_sentence_only_candidate_available",
            case_obj=tc10,
            support_case_obj=None,
        )
    )
    matrix_records.append(
        _from_traversal(
            cell_id="M3",
            condition_class="cue_present_prior_single_source_candidate_available",
            case_obj=tc01,
            support_case_obj=cr01,
        )
    )
    matrix_records.append(
        _from_lineage(
            cell_id="M4",
            condition_class="cue_present_prior_repeated_evidence_candidate_available",
            case_obj=cr06,
        )
    )
    matrix_records.append(
        _from_lineage(
            cell_id="M5",
            condition_class="cue_present_prior_mixed_source_candidate_available",
            case_obj=cr08,
        )
    )
    matrix_records.append(
        _from_lineage(
            cell_id="M6",
            condition_class="candidate_surface_unresolved_or_unavailable_boundary_condition",
            case_obj=cr03,
            related_traversal_case_id=str(tc04["case_id"]),
        )
    )

    records_sorted = sorted(matrix_records, key=lambda r: CELL_ORDER.index(str(r["cell_id"])))

    controls = _evaluate_controls(records_sorted)
    audits = _evaluate_audits(records_sorted)
    return records_sorted, {
        "source_artifacts": {
            "traversal": str(traversal_path.relative_to(base_dir)).replace("\\", "/"),
            "correspondence": str(correspondence_path.relative_to(base_dir)).replace("\\", "/"),
            "lineage": str(lineage_path.relative_to(base_dir)).replace("\\", "/"),
        },
        "controls": controls,
        "audits": audits,
    }


def _evaluate_controls(records: List[Dict[str, object]]) -> Dict[str, object]:
    by = {str(r["cell_id"]): r for r in records}

    m1 = by["M1"]
    m3 = by["M3"]
    m4 = by["M4"]
    m5 = by["M5"]
    m6 = by["M6"]

    removal = {
        "seed_written_relations_delta_m3_minus_m1": (
            _safe_int(m3["surface_seed"]["written_relations_count"])
            - _safe_int(m1["surface_seed"]["written_relations_count"])
        ),
        "candidate_count_delta_m3_minus_m1": (
            _safe_int(m3["surface_candidates"]["candidate_count"])
            - _safe_int(m1["surface_candidates"]["candidate_count"])
        ),
        "supporting_state_delta_m3_minus_m1": (
            _safe_int(m3["surface_support"]["support_state_counts"].get("supporting"))
            - _safe_int(m1["surface_support"]["support_state_counts"].get("supporting"))
        ),
        "legitimized_selection_delta_m3_minus_m1": (
            _safe_int(m3["surface_candidates"]["selection_state_counts"].get("legitimized"))
            - _safe_int(m1["surface_candidates"]["selection_state_counts"].get("legitimized"))
        ),
    }

    available_cells = ["M1", "M2", "M3", "M4", "M5"]
    boundary = {
        "available_cells_candidate_surface_states": {
            cell: by[cell]["surface_candidates"]["availability_state"] for cell in available_cells
        },
        "boundary_cell_candidate_surface_state": m6["surface_candidates"]["availability_state"],
        "boundary_cell_unresolved_support_count": _safe_int(
            m6["surface_support"]["support_state_counts"].get("unresolved")
        ),
    }

    provenance = {
        "m3_dependency_states": m3["surface_support"]["dependency_state_counts"],
        "m4_dependency_states": m4["surface_support"]["dependency_state_counts"],
        "m5_dependency_states": m5["surface_support"]["dependency_state_counts"],
        "m4_has_dependent_signal": _safe_int(m4["surface_support"]["dependency_state_counts"].get("Dependent")) > 0,
        "m5_has_only_unknown_dependency": (
            set(m5["surface_support"]["dependency_state_counts"].keys()) <= {"Unknown"}
            if m5["surface_support"]["dependency_state_counts"]
            else False
        ),
    }

    unavailable_controls = {
        "faithful_neutralization": "UNAVAILABLE_PER_FROZEN_DESIGN",
        "canonical_permutation_contract": "UNAVAILABLE_PER_FROZEN_DESIGN",
    }

    return {
        "removal_control": removal,
        "boundary_control": boundary,
        "provenance_variation_control": provenance,
        "unavailable_controls": unavailable_controls,
    }


def _evaluate_audits(records: List[Dict[str, object]]) -> Dict[str, object]:
    raw = json.dumps(records, sort_keys=True)
    lowered = raw.lower()
    oracle_tokens = ("oracle", "necessary_set", "activation_fingerprint")
    post_transition_tokens = ("tp.idob", "meaning_delta_h", "mcb", "post_crossing")
    evaluator_tokens = ("expected_outcome", "target_label", "oracle_answer")

    oracle_ok = not any(tok in lowered for tok in oracle_tokens)
    post_transition_ok = not any(tok in lowered for tok in post_transition_tokens)
    evaluator_ok = not any(tok in lowered for tok in evaluator_tokens)

    unresolved_integrity = any(
        str(r["cell_id"]) == "M6"
        and str(r["surface_candidates"]["availability_state"]) in ("unresolved", "unavailable")
        and _safe_int(r["surface_support"]["support_state_counts"].get("unresolved")) > 0
        for r in records
    )

    position_name_shortcut = {
        "status": "NOT_APPLICABLE_UNAVAILABLE_CONTROL",
        "reason": "faithful canonical permutation contract unavailable in frozen design",
    }

    return {
        "oracle_privileged_exclusion": {"pass": oracle_ok},
        "post_transition_leakage_exclusion": {"pass": post_transition_ok},
        "evaluator_isolation": {"pass": evaluator_ok},
        "position_name_shortcut_check": position_name_shortcut,
        "unresolved_unavailable_handling_integrity": {"pass": unresolved_integrity},
    }


def _semantic_slice(records: List[Dict[str, object]], controls: Dict[str, object]) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    for r in records:
        out.append(
            {
                "cell_id": r["cell_id"],
                "condition_class": r["condition_class"],
                "authority_anchor": r["authority_anchor"],
                "surface_seed": {
                    "availability_state": r["surface_seed"]["availability_state"],
                    "written_relations_count": r["surface_seed"]["written_relations_count"],
                },
                "surface_candidates": {
                    "availability_state": r["surface_candidates"]["availability_state"],
                    "candidate_count": r["surface_candidates"]["candidate_count"],
                    "selection_state_counts": r["surface_candidates"]["selection_state_counts"],
                },
                "surface_support": {
                    "availability_state": r["surface_support"]["availability_state"],
                    "cue_present": r["surface_support"]["cue_present"],
                    "cue_provenance": r["surface_support"]["cue_provenance"],
                    "support_state_counts": r["surface_support"]["support_state_counts"],
                    "dependency_state_counts": r["surface_support"]["dependency_state_counts"],
                    "unresolved_count": r["surface_support"]["unresolved_count"],
                },
                "control_identity": {
                    "removal_control_defined": True,
                    "boundary_control_defined": True,
                    "provenance_variation_defined": True,
                    "neutralization": controls["unavailable_controls"]["faithful_neutralization"],
                    "permutation": controls["unavailable_controls"]["canonical_permutation_contract"],
                },
            }
        )
    return out


def _build_payload() -> Dict[str, object]:
    base_dir = Path(__file__).resolve().parents[2]
    records_1, extras_1 = _semantic_cell_records(base_dir)
    records_2, extras_2 = _semantic_cell_records(base_dir)

    semantic_1 = _semantic_slice(records_1, extras_1["controls"])
    semantic_2 = _semantic_slice(records_2, extras_2["controls"])
    semantic_fp_1 = sha256(json.dumps(semantic_1, sort_keys=True).encode("utf-8")).hexdigest()
    semantic_fp_2 = sha256(json.dumps(semantic_2, sort_keys=True).encode("utf-8")).hexdigest()
    replay_pass = semantic_fp_1 == semantic_fp_2

    expected_cells = set(CELL_ORDER)
    actual_cells = {str(r["cell_id"]) for r in records_1}
    cell_completeness = expected_cells == actual_cells

    expected_surfaces = {"surface_seed", "surface_candidates", "surface_support"}
    surface_completeness = all(expected_surfaces <= set(r.keys()) for r in records_1)

    controls = extras_1["controls"]
    audits = extras_1["audits"]

    controls_complete = all(
        key in controls
        for key in (
            "removal_control",
            "boundary_control",
            "provenance_variation_control",
            "unavailable_controls",
        )
    )
    audits_complete = all(
        bool(audits[k]["pass"]) if isinstance(audits[k], dict) and "pass" in audits[k] else True
        for k in (
            "oracle_privileged_exclusion",
            "post_transition_leakage_exclusion",
            "evaluator_isolation",
            "unresolved_unavailable_handling_integrity",
        )
    )

    completeness = {
        "expected_cell_ids": list(CELL_ORDER),
        "actual_cell_ids": sorted(actual_cells),
        "cell_completeness_pass": cell_completeness,
        "surface_completeness_pass": surface_completeness,
        "controls_present_pass": controls_complete,
        "audits_pass": audits_complete,
        "overall_pass": (
            cell_completeness
            and surface_completeness
            and controls_complete
            and audits_complete
            and replay_pass
        ),
    }

    m_by = {str(r["cell_id"]): r for r in records_1}
    primary_observations = {
        "organization_class": [
            "M1 cue-absent cell shows zero legitimized selection and zero supporting correspondence.",
            "M3 cue-present prior-single-source cell shows positive legitimized/supporting signal.",
            "M2 cue-present sentence-only cell shows candidate activity without legitimized support-state evidence in this bounded slice.",
        ],
        "dependency_class": [
            "M4 repeated-evidence cell contains Dependent and Unknown dependency states.",
            "M5 mixed-source cell remains Unknown with independence unavailable.",
        ],
        "boundary_stage_class": [
            "M6 is unresolved/unavailable for candidate surface with unresolved correspondence states recorded.",
            "M1-M5 remain candidate-surface available in this frozen matrix.",
        ],
        "trajectory_like_class": [
            "Observed progression across retained contrasts: absent-support (M1) -> support-present (M3) -> dependency differentiation (M4/M5) -> unresolved boundary (M6).",
        ],
        "invariance_class": [
            "No faithful neutralization/permutation invariance claim is supported under frozen design; controls are unavailable by design.",
        ],
    }

    secondary_utility = {
        "separate_channel_note": "Secondary utility is recorded separately and does not gate primary structure observation validity.",
        "bounded_indications": [
            {
                "contrast": "M3 vs M1",
                "signal": "legitimized/supporting-state increase under cue-presence contrast",
            },
            {
                "contrast": "M4 vs M3",
                "signal": "dependency-state constraint signal appears only in repeated-evidence condition",
            },
        ],
        "non_findings": [
            "No claim of localization mechanism.",
            "No claim of basis-parameter or monotonic-narrowing structure.",
        ],
    }

    informative_negatives: List[str] = []
    if _safe_int(m_by["M6"]["surface_support"]["support_state_counts"].get("unresolved")) > 0:
        informative_negatives.append("SURFACE_TOO_COARSE_FOR_PRIMARY_OBJECTIVE")

    if all(
        _safe_int(m_by[c]["surface_support"]["support_state_counts"].get("supporting")) == 0
        for c in ("M1", "M2", "M3", "M4", "M5")
    ):
        informative_negatives.append("NO_STABLE_ORGANIZATION_OBSERVED_WITHIN_SURFACE")

    integrity = "PASS" if completeness["overall_pass"] else "INVALID"
    post_run_status = "EXECUTED / PENDING REVIEW" if integrity == "PASS" else "INVALID / PENDING REVIEW"

    return {
        "metadata": {
            "run_utc": datetime.now(timezone.utc).isoformat(),
            "char_type": "idob_relational_space_localization_s2m_structure_observation_surface",
            "char_version": "1.0",
            "scope": "frozen_m1_m6_surface_characterization_only",
        },
        "authority": {
            "design_doc": "notes/program/idob_relational_space_localization_s2m_structure_observation_surface_design.md",
            "proposal_doc": "notes/program/idob_relational_space_localization_s2m_structure_observation_surface_proposal.md",
            "source_artifacts": extras_1["source_artifacts"],
            "critical_claim_boundary": "positive findings are bounded to frozen M1-M6 contrasts and retained surfaces; no neutralization/permutation invariance claim",
        },
        "frozen_matrix": {"cell_order": list(CELL_ORDER), "cells": records_1},
        "controls": controls,
        "audits": audits,
        "semantic_slice_replay": {
            "semantic_slice_fingerprint_first": semantic_fp_1,
            "semantic_slice_fingerprint_second": semantic_fp_2,
            "pass": replay_pass,
            "semantic_fields_requiring_exact_replay": [
                "cell_id",
                "condition_class",
                "qualified_surface_availability_state",
                "represented_provenance_candidate_support_states",
                "control_identity",
                "derived_comparison_outputs",
            ],
            "legitimate_exclusions": [
                "runtime timestamps",
                "run identifiers and artifact wrapper metadata",
            ],
        },
        "primary_observations": primary_observations,
        "secondary_utility_observations": secondary_utility,
        "informative_negative_outcomes": informative_negatives,
        "completeness": completeness,
        "integrity": integrity,
        "post_run_status": post_run_status,
        "explicit_non_findings": [
            "no invariance claim under unavailable neutralization/permutation controls",
            "no architecture recommendation",
            "no localization requirement or mechanism claim",
            "no basis-parameter claim",
            "no monotonic-narrowing claim",
        ],
    }


def _write_artifact(payload: Dict[str, object]) -> Path:
    run_id = (
        datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        + "__idob_rel_space_localization_s2m_structure_observation_surface"
    )
    runs_dir = (
        Path(__file__).resolve().parents[2]
        / "local_characterization"
        / "sessions"
        / "idob_relational_space_localization_s2m_structure_observation_surface"
        / "runs"
    )
    runs_dir.mkdir(parents=True, exist_ok=True)
    out = runs_dir / "{}.json".format(run_id)
    payload["metadata"]["run_id"] = run_id
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out


def main() -> None:
    payload = _build_payload()
    out = _write_artifact(payload)
    print(str(out))
    print("semantic_slice_replay_pass={}".format(payload["semantic_slice_replay"]["pass"]))
    print("completeness_pass={}".format(payload["completeness"]["overall_pass"]))
    print("integrity={}".format(payload["integrity"]))
    print("post_run_status={}".format(payload["post_run_status"]))


if __name__ == "__main__":
    main()
