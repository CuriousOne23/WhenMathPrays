"""Replay checks for SmOB residue field wiring on the short simulator TP."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict
import copy
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import primitives_pathA_short as primitives  # noqa: E402
from tp_substrate import init_tp  # noqa: E402
from pathA_short_simulator import run_pathA_short  # noqa: E402
from idob.psc import _evaluate_no_obset_mutation  # noqa: E402


def _build_minimal_tp() -> Any:
    tp = init_tp("The book is on the table.")
    tp.struct_segments = ["NP", "PP"]
    tp.segment_tokens = [["The", "book"], ["on", "the", "table"]]
    tp.struct_roles = ["entity", "locative_modifier"]
    tp.constraints_matched = ["locative_composition_rule"]
    tp.constraints_unmatched = []
    return tp


def _assert_non_empty_residue_commit_path() -> None:
    original_compute = primitives.compute_smoothing_state
    observed: Dict[str, Any] = {}

    def fake_compute_smoothing_state(**kwargs: Any) -> Dict[str, Any]:
        payload = {
            "smoothing_operations": ["adjacency_smoothing"],
            "semantic_adjacent_cues": ["locative_adjacent"],
            "basin_residue": ["SMOB_RESIDUE_TEST"],
        }
        observed["state"] = copy.deepcopy(payload)
        return payload

    primitives.compute_smoothing_state = fake_compute_smoothing_state
    try:
        tp = _build_minimal_tp()
        before = asdict(tp)
        tp = primitives.SmOB(tp)
        after = asdict(tp)

        # A: computed residue reaches canonical TP field
        assert observed["state"]["basin_residue"] == ["SMOB_RESIDUE_TEST"]
        assert tp.smoothing_residue == ["SMOB_RESIDUE_TEST"]

        # B/C: dataclass + final_tp serialization preserve canonical field
        assert after["smoothing_residue"] == ["SMOB_RESIDUE_TEST"]
        result = run_pathA_short("The book is on the table.")
        smob_trace = next((step for step in result["trace"] if step.get("primitive") == "SmOB"), {})
        assert result["final_tp"]["smoothing_residue"] == ["SMOB_RESIDUE_TEST"]

        # D/E: no undeclared field, trace uses canonical TP field name
        assert not hasattr(tp, "basin_residue")
        assert "smoothing_residue" in smob_trace
        assert "basin_residue" not in smob_trace

        # I: unrelated TP fields remain unchanged through SmOB
        unchanged_keys = [
            "raw_text",
            "tokens",
            "normalized_text",
            "struct_segments",
            "segment_tokens",
            "struct_roles",
            "constraints_matched",
            "constraints_unmatched",
            "constraint_residue",
            "truth_relation",
            "semantic",
            "commit_flags",
        ]
        for key in unchanged_keys:
            assert after[key] == before[key], f"unexpected change in unrelated TP field: {key}"
    finally:
        primitives.compute_smoothing_state = original_compute


def _assert_default_behavior() -> None:
    # F: default empty residue behavior remains intact
    result = run_pathA_short("The sky is blue.")
    assert result["final_tp"]["smoothing_residue"] == []


def _assert_psc_guard_targets_canonical_field() -> None:
    # H: PSC guard still protects canonical field name
    invariant = {"id": "I_NO_OBSET_MUTATION", "field": "semantic_core", "rule": "no_obset_mutation"}
    smoothing_violations = _evaluate_no_obset_mutation(
        object_name="test_object",
        invariant=invariant,
        contribution={"smoothing_residue": ["x"]},
    )
    basin_violations = _evaluate_no_obset_mutation(
        object_name="test_object",
        invariant=invariant,
        contribution={"basin_residue": ["x"]},
    )
    assert smoothing_violations, "expected canonical smoothing_residue to be protected"
    assert not basin_violations, "unexpected protection of undeclared basin_residue field"


def main() -> None:
    _assert_non_empty_residue_commit_path()
    _assert_default_behavior()
    _assert_psc_guard_targets_canonical_field()
    print("smob residue field replay passed")


if __name__ == "__main__":
    main()
