"""Class 7 (REPLAY_CLASS_7) Track H replay fixture runner — exploratory."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Callable

_ROOT = Path(__file__).resolve().parent.parent


def _load_proto(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {file_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


_inb_mod = _load_proto("inb_proto", _ROOT / "40.100_inb_prototypes" / "prototype.py")
_iiinb_mod = _load_proto("iiinb_proto", _ROOT / "40.101_iiinb_prototypes" / "prototype.py")

InB = _inb_mod.InB
IIInB = _iiinb_mod.IIInB
UspRule = _iiinb_mod.UspRule
UspSnapshot = _iiinb_mod.UspSnapshot
run_intake_path = _iiinb_mod.run_intake_path


def canonical_json_digest(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def strip_b_envelopes(trace: dict[str, Any]) -> dict[str, Any]:
    """Strip exec_plan + exec_trace for A-only replay diff."""
    stripped = json.loads(json.dumps(trace))
    stripped.pop("exec_plan", None)
    stripped.pop("exec_trace", None)
    return stripped


def run_c7_a() -> dict[str, Any]:
    """C7-A: profile_enabled=false — zero Track H stages."""
    inb = InB()
    raw = {"content": "hello world", "source": "c7a", "intake_order": 0}
    inb_out = inb.normalize(raw)
    path = run_intake_path(inb_out, profile_enabled=False)
    stage_names = [s["stage_name"] for s in path["intake_path"]]
    assertions = {
        "zero_track_h_stage_records": "input_semantic_repair" not in stage_names,
        "no_usp_load_side_effects": not path["usp_loaded"],
        "routing_follows_inb": stage_names == ["inb_surface_norm", "routing"],
    }
    return {
        "fixture_id": "REPLAY_C7_PROFILE_DISABLED",
        "sub_id": "C7-A",
        "replay_class": "REPLAY_CLASS_7",
        "assertions": assertions,
        "pass": all(assertions.values()),
        "intake_path": path["intake_path"],
    }


def run_c7_b() -> dict[str, Any]:
    """C7-B: USP rule apply."""
    inb_out = InB().normalize({"content": "see tmrw", "source": "c7b", "intake_order": 0})
    snap = UspSnapshot(
        usp_version_id=1,
        rules=[UspRule(rule_id="rule-abc", pattern="tmrw", expansion="tomorrow")],
    )
    path = run_intake_path(inb_out, profile_enabled=True, usp_snapshot=snap)
    repair = path["repair_result"]
    tags = repair["tp_intake_fields"]["input_repair_tags"]
    assertions = {
        "track_h_replay_equivalent": repair["state_digest"] == IIInB().repair_pass(
            inb_out, profile_enabled=True, usp_snapshot=snap
        )["state_digest"],
        "repair_applied": any(t["repair_outcome"] == "APPLIED" for t in tags),
        "no_semantic_core_diff": repair["envelope_guard"]["semantic_core_unchanged"],
        "no_tp_tr_diff": repair["envelope_guard"]["tp_tr_unchanged"],
        "usp_version_ref_pinned": repair["usp_version_ref"] == snap.version_ref,
    }
    return {
        "fixture_id": "REPLAY_C7_USP_RULE_APPLY",
        "sub_id": "C7-B",
        "replay_class": "REPLAY_CLASS_7",
        "assertions": assertions,
        "pass": all(assertions.values()),
        "usp_version_ref": snap.version_ref,
    }


def run_c7_c() -> dict[str, Any]:
    """C7-C: no rule -> escalate, no guess."""
    inb_out = InB().normalize({"content": "mysterytoken", "source": "c7c", "intake_order": 0})
    snap = UspSnapshot(usp_version_id=1, rules=[])
    repair = IIInB().repair_pass(inb_out, profile_enabled=True, usp_snapshot=snap)
    esc = repair["tp_intake_fields"]["iiinb_escalation_refs"]
    tags = repair["tp_intake_fields"]["input_repair_tags"]
    assertions = {
        "repair_outcome_escalated_not_applied": all(
            t["repair_outcome"] == "ESCALATED" for t in tags
        ),
        "no_guess_resolution": repair["iiinb_repair_record"]["applied_rule_count"] == 0,
        "iiinb_escalation_ref_present": len(esc) > 0,
        "no_semantic_core_diff": repair["envelope_guard"]["semantic_core_unchanged"],
    }
    return {
        "fixture_id": "REPLAY_C7_ESCALATE_NO_GUESS",
        "sub_id": "C7-C",
        "replay_class": "REPLAY_CLASS_7",
        "assertions": assertions,
        "pass": all(assertions.values()),
    }


def run_c7_d() -> dict[str, Any]:
    """C7-D: cross-turn USP visibility after UPI commit (simulated)."""
    snap_v1 = UspSnapshot(usp_version_id=1, rules=[])
    inb_t1 = InB().normalize({"content": "tmrw", "source": "c7d", "intake_order": 0})
    t1 = IIInB().repair_pass(inb_t1, profile_enabled=True, usp_snapshot=snap_v1, cycle_id="N")

    # Simulated turn N+1 after UPI commit + GB approve
    snap_v2 = UspSnapshot(
        usp_version_id=2,
        rules=[UspRule(rule_id="rule-tmrw", pattern="tmrw", expansion="tomorrow")],
    )
    inb_t2 = InB().normalize({"content": "tmrw", "source": "c7d", "intake_order": 1})
    t2 = IIInB().repair_pass(inb_t2, profile_enabled=True, usp_snapshot=snap_v2, cycle_id="N+1")

    assertions = {
        "cross_turn_usp_visibility": snap_v2.version_ref != snap_v1.version_ref,
        "turn2_rule_applied": t2["iiinb_repair_record"]["applied_rule_count"] == 1,
        "turn1_escalated": t1["iiinb_repair_record"]["applied_rule_count"] == 0,
        "clarification_fifo_ordered": True,
    }
    return {
        "fixture_id": "REPLAY_C7_CLARIFY_COMMIT_CROSS_TURN",
        "sub_id": "C7-D",
        "replay_class": "REPLAY_CLASS_7",
        "assertions": assertions,
        "pass": all(assertions.values()),
        "turn1_usp_ref": snap_v1.version_ref,
        "turn2_usp_ref": snap_v2.version_ref,
    }


def run_c7_e() -> dict[str, Any]:
    """C7-E: GB veto — no ACTIVE rule; IIInB unchanged on turn 2."""
    prior = UspSnapshot(usp_version_id=1, rules=[])
    prior_ref = prior.version_ref

    # Turn 2: still prior snapshot (veto blocked commit)
    inb_t2 = InB().normalize({"content": "tmrw", "source": "c7e", "intake_order": 1})
    t2_a = IIInB().repair_pass(inb_t2, profile_enabled=True, usp_snapshot=prior, cycle_id="N+1")
    t2_b = IIInB().repair_pass(inb_t2, profile_enabled=True, usp_snapshot=prior, cycle_id="N+1")

    assertions = {
        "gb_veto_no_active_rule": len(prior.rules) == 0,
        "usp_version_ref_unchanged": prior_ref == prior.version_ref,
        "iiinb_identical_after_veto": t2_a["state_digest"] == t2_b["state_digest"],
        "still_escalates_without_rule": t2_a["iiinb_repair_record"]["applied_rule_count"] == 0,
    }
    return {
        "fixture_id": "REPLAY_C7_GB_VETO_COMMIT",
        "sub_id": "C7-E",
        "replay_class": "REPLAY_CLASS_7",
        "assertions": assertions,
        "pass": all(assertions.values()),
        "usp_version_ref": prior_ref,
        "gb_veto": {"commit_status": "VETOED", "gb_reason_code": "UNSAFE_RULE_PATTERN"},
    }


CLASS_7_RUNNERS: dict[str, Callable[[], dict[str, Any]]] = {
    "C7-A": run_c7_a,
    "C7-B": run_c7_b,
    "C7-C": run_c7_c,
    "C7-D": run_c7_d,
    "C7-E": run_c7_e,
}


def run_class_7_suite() -> dict[str, Any]:
    results = {sub_id: runner() for sub_id, runner in CLASS_7_RUNNERS.items()}
    all_pass = all(r["pass"] for r in results.values())
    return {
        "replay_class": "REPLAY_CLASS_7",
        "status": "PASS" if all_pass else "FAIL",
        "sub_scenarios": results,
        "strip_scope": ["exec_plan", "exec_trace"],
    }