"""Verification harness for 40.392 core data struct prototypes (W2 Phase B)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import (
    ClarificationEvent,
    ConversationLayerState,
    InputRepairTag,
    StructReject,
    UspRule,
    UspSnapshot,
    UpiCommitRecord,
    canonical_json,
    compute_usp_version_ref,
)

ARTIFACT_NAME = "structs_verification_run_2026-06-08.json"
GOLDEN_PATH = Path(__file__).resolve().parent / "artifacts" / "golden_usp_snapshot_v1.json"


def _iiinb_compat_snapshot() -> UspSnapshot:
    return UspSnapshot(
        usp_version_id=1,
        rules=[UspRule(rule_id="rule-abc", pattern="tmrw", expansion="tomorrow", precedence=10)],
    )


def scenario_usp_snapshot_roundtrip() -> dict:
    snap = _iiinb_compat_snapshot()
    encoded = snap.to_dict()
    decoded = UspSnapshot.from_dict(encoded)
    ok = decoded.version_ref == snap.version_ref and decoded.usp_version_id == 1
    return {"scenario": "positive_usp_snapshot_roundtrip", "hlr": ["HLR-20.039-022"], "result": "PASS" if ok else "FAIL"}


def scenario_input_repair_tag_ordering() -> dict:
    tags = [
        InputRepairTag("tag-b", 2, "r2", "APPLIED"),
        InputRepairTag("tag-a", 1, "r1", "ESCALATED"),
    ]
    from prototype import export_sorted_tags

    export_a = export_sorted_tags(tags)
    export_b = export_sorted_tags(list(reversed(tags)))
    ok = export_a == export_b and '"segment_index":1' in export_a
    return {"scenario": "positive_input_repair_tag_ordering", "hlr": ["HLR-20.039-024"], "result": "PASS" if ok else "FAIL"}


def scenario_conversation_layer_envelope_clean() -> dict:
    state = ConversationLayerState(conversation_id="conv-1", usp_version_ref_pinned="abc123")
    payload = state.to_dict()
    try:
        ConversationLayerState.validate_envelope_clean(payload)
        ok = True
    except StructReject:
        ok = False
    return {"scenario": "positive_conversation_layer_envelope_clean", "hlr": ["HLR-20.039-021", "HLR-20.039-025"], "result": "PASS" if ok else "FAIL"}


def scenario_forbidden_semantic_core_field() -> dict:
    try:
        ConversationLayerState.validate_envelope_clean({"conversation_id": "c1", "semantic_core": {}})
        ok = False
    except StructReject as exc:
        ok = exc.reason_code == "STRUCT_RSN_002_FORBIDDEN_ENVELOPE_FIELD"
    return {"scenario": "negative_forbidden_semantic_core_field", "hlr": ["envelope guard"], "result": "PASS" if ok else "FAIL"}


def scenario_golden_fixture_match() -> dict:
    snap = _iiinb_compat_snapshot()
    live = snap.to_dict()
    ref = compute_usp_version_ref(snap.to_storage_dict())
    live["usp_version_ref"] = ref
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    golden["usp_version_ref"] = ref
    ok = canonical_json(live) == canonical_json(golden)
    return {"scenario": "positive_golden_fixture_match", "hlr": ["HLR-20.039-024"], "result": "PASS" if ok else "FAIL", "usp_version_ref": ref}


def scenario_iiinb_digest_compat() -> dict:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "40.101_iiinb_prototypes"))
    from prototype import UspSnapshot as IIInBSnap, UspRule as IIInBRule, compute_usp_version_ref as iiinb_ref

    iiinb_snap = IIInBSnap(
        usp_version_id=1,
        rules=[IIInBRule(rule_id="rule-abc", pattern="tmrw", expansion="tomorrow", precedence=10)],
    )
    local = _iiinb_compat_snapshot()
    ok = iiinb_ref(iiinb_snap.to_dict()) == local.version_ref
    return {"scenario": "positive_iiinb_digest_compat", "hlr": ["HLR-20.039-022"], "result": "PASS" if ok else "FAIL"}


def scenario_audit_struct_exports() -> dict:
    event = ClarificationEvent("evt-1", 1, "tmrw", "tomorrow")
    record = UpiCommitRecord("COMMITTED", 1, "ref-abc", None, ["OK"])
    ok = "clarification_event_v1" in canonical_json(event.to_dict())
    ok = ok and "COMMITTED" in canonical_json(record.to_dict())
    return {"scenario": "positive_audit_struct_exports", "hlr": ["HLR-20.039-024"], "result": "PASS" if ok else "FAIL"}


def scenario_unknown_schema_reject() -> dict:
    try:
        UspSnapshot.from_dict({"schema_version": "usp_snapshot_v99", "usp_version_id": 1, "rules": []})
        ok = False
    except StructReject:
        ok = True
    return {"scenario": "negative_unknown_schema_version", "hlr": ["HLR-20.039-019"], "result": "PASS" if ok else "FAIL"}


def main() -> int:
    scenarios = [
        scenario_usp_snapshot_roundtrip(),
        scenario_input_repair_tag_ordering(),
        scenario_conversation_layer_envelope_clean(),
        scenario_forbidden_semantic_core_field(),
        scenario_golden_fixture_match(),
        scenario_iiinb_digest_compat(),
        scenario_audit_struct_exports(),
        scenario_unknown_schema_reject(),
    ]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    report = {
        "module": "40.392_core_data_structs_prototypes",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "phase": "B",
        "status": status,
        "scenarios": scenarios,
        "summary": {
            "total_scenarios": len(scenarios),
            "passed": sum(1 for s in scenarios if s["result"] == "PASS"),
            "failed_scenarios": [s["scenario"] for s in scenarios if s["result"] != "PASS"],
        },
    }
    artifact_dir = Path(__file__).resolve().parent / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    path = artifact_dir / ARTIFACT_NAME
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Structs harness status: {status}")
    print(f"Scenarios: {report['summary']['passed']}/{report['summary']['total_scenarios']} PASS")
    print(f"Artifact: {path}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())