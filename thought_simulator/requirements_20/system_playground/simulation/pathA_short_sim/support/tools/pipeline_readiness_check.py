from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tp_substrate  # noqa: F401
from idob import psc
from idob import registry as idob_registry
from idob import sum as idob_sum  # noqa: F401
from mcb.seam import copy_from_idob
from ouba.assembly import build_ouba
from pathA_short_simulator import run_pathA_short

IDOB_KEYS = [
    "identity_geometry",
    "truth_relation",
    "truth_relation_family",
    "semantic_core",
    "selected_ops",
    "claimed_fields",
    "contributors",
    "contributions",
    "activation_set",
    "inactive_objects",
    "residual_activated",
    "overlap_events",
    "meaning_delta",
    "psc_violations",
    "registry_digest",
    "complete",
    "tru_hint",
]

MCB_KEYS = [
    "mcb_identity_geometry",
    "mcb_truth_relation",
    "mcb_truth_relation_family",
    "mcb_semantic_core",
    "mcb_claimed_fields",
    "mcb_contributors",
    "mcb_overlap_events",
    "mcb_registry_digest",
    "mcb_complete",
    "mcb_tru_hint",
]

OUBA_KEYS = [
    "ouba_identity_geometry",
    "ouba_truth_relation",
    "ouba_truth_relation_family",
    "ouba_semantic_core",
    "ouba_claimed_fields",
    "ouba_contributors",
    "ouba_overlap_events",
    "ouba_registry_digest",
    "ouba_complete",
    "ouba_tru_hint",
]

OUBA_TO_MCB = {
    "ouba_identity_geometry": "mcb_identity_geometry",
    "ouba_truth_relation": "mcb_truth_relation",
    "ouba_truth_relation_family": "mcb_truth_relation_family",
    "ouba_semantic_core": "mcb_semantic_core",
    "ouba_claimed_fields": "mcb_claimed_fields",
    "ouba_contributors": "mcb_contributors",
    "ouba_overlap_events": "mcb_overlap_events",
    "ouba_registry_digest": "mcb_registry_digest",
    "ouba_complete": "mcb_complete",
    "ouba_tru_hint": "mcb_tru_hint",
}

SENTENCES = [
    "The sky is blue.",
    "Where is the book that is on the table?",
    "Why is the sky blue?",
    "The quick brown fox jumps over the lazy dog.",
    "The rain in Spain stays mainly in the plain.",
]


def _ensure_literal_safe(value: Any) -> None:
    if ast.literal_eval(repr(value)) != value:
        raise ValueError("literal-eval roundtrip mismatch")


def _check_exact_keys(label: str, payload: Dict[str, Any], expected: List[str]) -> None:
    if set(payload.keys()) != set(expected):
        missing = sorted(set(expected) - set(payload.keys()))
        extra = sorted(set(payload.keys()) - set(expected))
        raise ValueError(f"{label} key mismatch; missing={missing}, extra={extra}")


def _run_case(sentence: str) -> Dict[str, Any]:
    simulation = run_pathA_short(sentence)
    final_tp = simulation.get("final_tp", {})
    idob_packet = final_tp.get("idob_packet", final_tp.get("idob", {}))
    if not isinstance(idob_packet, dict):
        raise ValueError("idob_packet is not a dict")

    _check_exact_keys("idob", idob_packet, IDOB_KEYS)

    psc_violations = idob_packet.get("psc_violations")
    if not isinstance(psc_violations, list):
        raise ValueError("idob psc_violations missing or not a list")

    contributions = idob_packet.get("contributions", [])
    if not isinstance(contributions, list):
        raise ValueError("idob contributions is not a list")

    psc_recheck = psc.evaluate_psc(
        idob_registry.object_specs_by_name,
        contributions,
        final_tp,
        idob_packet,
        idob_registry.psc_defaults,
    )
    if not isinstance(psc_recheck, list):
        raise ValueError("psc recheck did not return list")

    mcb_packet = copy_from_idob(idob_packet)
    _check_exact_keys("mcb", mcb_packet, MCB_KEYS)

    ouba_packet = build_ouba(mcb_packet)
    _check_exact_keys("ouba", ouba_packet, OUBA_KEYS)

    for ouba_key, mcb_key in OUBA_TO_MCB.items():
        if ouba_packet.get(ouba_key) != mcb_packet.get(mcb_key):
            raise ValueError(f"ouba mapping mismatch: {ouba_key} != {mcb_key}")

    _ensure_literal_safe(idob_packet)
    _ensure_literal_safe(psc_violations)
    _ensure_literal_safe(mcb_packet)
    _ensure_literal_safe(ouba_packet)

    return {
        "idob": idob_packet,
        "psc": psc_violations,
        "mcb": mcb_packet,
        "ouba": ouba_packet,
    }


def _assert_deterministic(sentence: str) -> None:
    first = _run_case(sentence)
    second = _run_case(sentence)
    if first != second:
        raise ValueError(f"nondeterministic output for sentence: {sentence}")


def main() -> int:
    # Explicitly touch imported modules to keep this a full pipeline readiness import check.
    if not callable(getattr(idob_sum, "sum_idob", None)):
        print("--- R8 ---")
        print("pipeline_ready=False")
        print("cases_checked=0")
        return 1

    checked = 0
    try:
        for sentence in SENTENCES:
            _assert_deterministic(sentence)
            checked += 1
    except Exception:
        print("--- R8 ---")
        print("pipeline_ready=False")
        print(f"cases_checked={checked}")
        return 1

    print("--- R8 ---")
    print("pipeline_ready=True")
    print(f"cases_checked={checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
