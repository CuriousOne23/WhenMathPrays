"""W2 USP pin extension harness for 40.32 COB prototypes."""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import COBDeterministicReject, COBState

_ROOT = Path(__file__).resolve().parent.parent
_usp_spec = importlib.util.spec_from_file_location("usp_prototype", _ROOT / "40.102_usp_prototypes" / "prototype.py")
_usp = importlib.util.module_from_spec(_usp_spec)
sys.modules["usp_prototype"] = _usp
assert _usp_spec.loader is not None
_usp_spec.loader.exec_module(_usp)

ARTIFACT = Path(__file__).resolve().parent / "artifacts" / "cob_w2_verification_run_2026-06-08.json"


def _seed() -> COBState:
    return COBState(cob_id="cob-w2-1", profile_signature="P1", replay_mode="full", sequence=0)


def scenario_pin_on_commit() -> dict:
    store = _usp.USPStore()
    res = store.apply_commit(pattern="tmrw", expansion="tomorrow", rule_id="r1")
    cob = _seed()
    snap = cob.pin_usp_snapshot(sequence=1, usp_version_id=res.usp_version_id, usp_version_ref=res.usp_version_ref)
    ok = snap["cob_snapshot_pin"]["usp_version_ref"] == res.usp_version_ref
    return {"scenario": "positive_cob_usp_pin_on_commit", "result": "PASS" if ok else "FAIL"}


def scenario_pin_survives_promote() -> dict:
    store = _usp.USPStore()
    res = store.apply_commit(pattern="a", expansion="A", rule_id="r1")
    cob = _seed()
    cob.pin_usp_snapshot(sequence=1, usp_version_id=res.usp_version_id, usp_version_ref=res.usp_version_ref)
    cob.apply_event({"event_type": "promote", "sequence": 2, "safe_boundary": True, "payload": {"winner_lineage": "wl-1"}})
    ok = cob.cob_snapshot_pin is not None and cob.cob_snapshot_pin["usp_version_ref"] == res.usp_version_ref
    return {"scenario": "positive_pin_survives_lifecycle_transition", "result": "PASS" if ok else "FAIL"}


def scenario_replay_pin_equivalent() -> dict:
    def pin_ref() -> str:
        store = _usp.USPStore()
        res = store.apply_commit(pattern="x", expansion="X", rule_id="r1")
        cob = _seed()
        cob.pin_usp_snapshot(sequence=1, usp_version_id=res.usp_version_id, usp_version_ref=res.usp_version_ref)
        return cob.cob_snapshot_pin["usp_version_ref"]

    ok = pin_ref() == pin_ref()
    return {"scenario": "positive_replay_pin_equivalent", "result": "PASS" if ok else "FAIL"}


def scenario_invalid_pin() -> dict:
    cob = _seed()
    try:
        cob.pin_usp_snapshot(sequence=1, usp_version_id=1, usp_version_ref="")
        ok = False
    except COBDeterministicReject:
        ok = True
    return {"scenario": "negative_pin_without_usp_version", "result": "PASS" if ok else "FAIL"}


def main() -> int:
    scenarios = [scenario_pin_on_commit(), scenario_pin_survives_promote(), scenario_replay_pin_equivalent(), scenario_invalid_pin()]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    report = {"module": "40.32_cob_prototypes_w2", "phase": "B", "status": status, "scenarios": scenarios}
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"COB W2 harness: {status} ({len(scenarios)} scenarios)")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())