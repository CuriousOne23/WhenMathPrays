"""Verification harness for 40.190_rb_prototypes (W3 Phase B)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import RoutingBasin, RoutingFilter, RBDecision, RBOutput

ARTIFACT_NAME = "rb_verification_run_2026-06-09.json"


def _mk_record(ob_id: str, content: str = "", messy: dict | None = None, tr: bool = False) -> dict:
    rec = {
        "ob_id": ob_id,
        "content": content or f"post-repair-{ob_id}",
        "tr_needs_update": tr,
    }
    if messy:
        rec["messy_input_record"] = messy
    return rec


def scenario_post_iiinb_fanout() -> dict:
    rb = RoutingBasin()
    records = [
        _mk_record("o1", "first"),
        _mk_record("o2", "second"),
    ]
    out = rb.route(records, iiinb_enabled=True, tr_needs_update=False, policy_signature="pol1", cycle_id="c-fanout")
    ok = (
        len(out.lanes) == 2
        and len(out.routing_filter.selected_ob_ids) == 2
        and out.routing_filter.policy_justification.get("iiinb_enabled") is True
    )
    return {"scenario": "post_iiinb_fanout", "hlr": ["HLR-20.050-001", "HLR-20.050-027"], "result": "PASS" if ok else "FAIL"}


def scenario_tr_skipped_when_flag_false() -> dict:
    rb = RoutingBasin()
    records = [_mk_record("o1", tr=False)]
    out = rb.route(records, tr_needs_update=False, policy_signature="pol1", cycle_id="c-tr-skip")
    no_tr = all(d.action != "invoke_tr" and not d.tr_eligible for d in out.decisions)
    ok = no_tr and len(out.lanes) == 1
    return {"scenario": "tr_skipped_when_flag_false", "hlr": ["HLR-20.050-027", "HLR-20.050-028"], "result": "PASS" if ok else "FAIL"}


def scenario_messy_input_preserved_routing() -> dict:
    rb = RoutingBasin()
    records = [
        _mk_record("o1", messy={"class": "MI_VAGUE"}, tr=False),
    ]
    out = rb.route(records, tr_needs_update=False, policy_signature="pol1", cycle_id="c-messy")
    lane0 = out.lanes[0] if out.lanes else {}
    preserved = "messy_input_record" in lane0 and lane0.get("messy_input_record", {}).get("class") == "MI_VAGUE"
    rationale_has = any("messy_preserved" in (d.rationale or "") for d in out.decisions)
    ok = preserved and rationale_has
    return {"scenario": "messy_input_preserved_routing", "hlr": ["HLR-20.050-009", "HLR-20.050-010"], "result": "PASS" if ok else "FAIL"}


def scenario_overflow_reject_with_audit() -> dict:
    rb = RoutingBasin()
    records = [_mk_record(f"o{i}") for i in range(20)]  # exceed default 16
    out = rb.route(records, overflow_limit=16, policy_signature="pol1", cycle_id="c-overflow")
    has_overflow = any(a.get("type") == "OVERFLOW" for a in out.audit_records)
    ok = has_overflow and len(out.audit_records) > 0
    return {"scenario": "overflow_reject_with_audit", "hlr": ["HLR-20.050-024", "HLR-20.050-029"], "result": "PASS" if ok else "FAIL"}


def scenario_routing_filter_replay() -> dict:
    rb = RoutingBasin()
    records = [
        _mk_record("oA", "alpha"),
        _mk_record("oB", "beta"),
    ]
    out1 = rb.route(records, iiinb_enabled=False, tr_needs_update=True, policy_signature="pol-replay", cycle_id="c-rep1")
    f1 = out1.routing_filter.as_dict()
    out2 = rb.route(records, iiinb_enabled=False, tr_needs_update=True, policy_signature="pol-replay", cycle_id="c-rep2")
    f2 = out2.routing_filter.as_dict()
    ok = json.dumps(f1, sort_keys=True) == json.dumps(f2, sort_keys=True)
    return {"scenario": "routing_filter_replay", "hlr": ["HLR-20.050-004", "HLR-20.050-036"], "result": "PASS" if ok else "FAIL"}


def main() -> int:
    scenarios = [
        scenario_post_iiinb_fanout(),
        scenario_tr_skipped_when_flag_false(),
        scenario_messy_input_preserved_routing(),
        scenario_overflow_reject_with_audit(),
        scenario_routing_filter_replay(),
    ]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    report = {
        "module": "40.190_rb_prototypes",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "phase": "B",
        "status": status,
        "scenarios": scenarios,
        "summary": {
            "total_scenarios": len(scenarios),
            "passed": sum(1 for s in scenarios if s["result"] == "PASS"),
        },
    }
    report["summary"]["failed_scenarios"] = [s["scenario"] for s in scenarios if s["result"] != "PASS"]
    artifact_dir = Path(__file__).resolve().parent / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    path = artifact_dir / ARTIFACT_NAME
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(f"RB harness status: {status}")
    print(f"Scenarios: {report['summary']['passed']}/{report['summary']['total_scenarios']} PASS")
    print(f"Artifact: {path}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
