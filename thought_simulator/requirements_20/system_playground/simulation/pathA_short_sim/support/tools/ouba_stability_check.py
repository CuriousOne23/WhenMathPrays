from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mcb.seam import copy_from_idob
from ouba.assembly import build_ouba

EXPECTED_OUBA_KEYS = [
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

MCB_TO_OUBA_MAP = {
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


def _synthetic_idob_packets() -> list[dict]:
    return [
        {
            "identity_geometry": "semantic_identity",
            "truth_relation": "declarative",
            "truth_relation_family": "descriptive_state",
            "semantic_core": {"theme": "sky", "state": "blue", "selected_ops": ["copular_state"]},
            "claimed_fields": ["semantic_core", "truth_relation_family"],
            "contributors": ["copular_state"],
            "overlap_events": [],
            "registry_digest": "d1",
            "complete": True,
            "tru_hint": "declarative",
        },
        {
            "identity_geometry": "referential_identity",
            "truth_relation": "interrogative",
            "truth_relation_family": "interrogative_wh",
            "semantic_core": {"query_type": "wh", "selected_ops": ["interrogative_wh"]},
            "claimed_fields": ["semantic_core", "truth_relation"],
            "contributors": ["interrogative_wh", "modifier_resolution"],
            "overlap_events": [{"a": "interrogative_wh", "b": "modifier_resolution", "mode": "merge", "fields": ["semantic_core"]}],
            "registry_digest": "d2",
            "complete": True,
            "tru_hint": "interrogative",
        },
        {
            "identity_geometry": "semantic_identity",
            "truth_relation": "unknown",
            "truth_relation_family": "unknown",
            "semantic_core": {},
            "claimed_fields": [],
            "contributors": ["residual_identity"],
            "overlap_events": [],
            "registry_digest": "d3",
            "complete": False,
            "tru_hint": "unknown",
        },
        {
            "identity_geometry": "semantic_identity",
            "truth_relation": "declarative",
            "truth_relation_family": "descriptive_mixed",
            "semantic_core": {"theme": "book", "location": "table", "selected_ops": ["locative", "mixed_descriptive"]},
            "claimed_fields": ["semantic_core", "contributors", "overlap_events"],
            "contributors": ["locative", "mixed_descriptive"],
            "overlap_events": [{"a": "locative", "b": "mixed_descriptive", "mode": "merge", "fields": ["semantic_core", "selected_ops"]}],
            "registry_digest": "d4",
            "complete": True,
            "tru_hint": "declarative",
        },
    ]


def _check_case(idob_packet: dict) -> tuple[bool, str]:
    mcb_packet = copy_from_idob(idob_packet)

    first = build_ouba(mcb_packet)
    second = build_ouba(mcb_packet)

    if sorted(first.keys()) != sorted(EXPECTED_OUBA_KEYS):
        return False, f"unexpected keys: {sorted(first.keys())}"

    if set(first.keys()) != set(EXPECTED_OUBA_KEYS):
        return False, "missing or extra OuBA keys detected"

    for ouba_key, mcb_key in MCB_TO_OUBA_MAP.items():
        if first.get(ouba_key) != mcb_packet.get(mcb_key):
            return False, f"value mismatch: {ouba_key} != {mcb_key}"

    if first != second:
        return False, "OuBA output changed between two identical runs"

    if ast.literal_eval(repr(first)) != first:
        return False, "OuBA output is not literal-eval safe"

    return True, "ok"


def main() -> int:
    packets = _synthetic_idob_packets()
    failures: list[str] = []

    for idx, idob_packet in enumerate(packets, start=1):
        ok, detail = _check_case(idob_packet)
        if not ok:
            failures.append(f"case {idx}: {detail}")

    if failures:
        print("ouba_stability=False")
        for row in failures:
            print(row)
        return 1

    print("ouba_stability=True")
    print(f"cases_checked={len(packets)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
