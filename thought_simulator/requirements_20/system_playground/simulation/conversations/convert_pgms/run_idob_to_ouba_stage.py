from __future__ import annotations

import copy
import hashlib
import re
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from thought_simulator.requirements_20.system_playground.primitives.ouba.ouba import OUBA


CONV_DIR = REPO_ROOT / "thought_simulator" / "requirements_20" / "system_playground" / "simulation" / "input" / "conv_01"
OUT_DIR = REPO_ROOT / "thought_simulator" / "requirements_20" / "system_playground" / "simulation" / "ouba_stage"

STAGE_SEQUENCE = [
    ("mcb", "TB.mcb_alignment"),
    ("rbu", "TB.rbu_commit"),
    ("tr", "TB.tr_routing_decision"),
    ("ctp", "TB.ctp_transition"),
    ("cex-ie", "TB.cex_ie_extract"),
    ("cex-ccr", "TB.cex_ccr_canonicalize"),
    ("cex-pck", "TB.cex_pck_pack"),
    ("cob", "TB.cob_output"),
    ("cil", "TB.cil_linkage"),
    ("cst-core", "TB.cst_core_metrics"),
    ("cst-ms", "TB.cst_ms_synthesis"),
    ("cst-mux", "TB.cst_mux_unified_packet"),
]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def dump_yaml(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=False)


def stable_id(prefix: str, seed_obj: Any, length: int = 12) -> str:
    digest = hashlib.sha256(
        yaml.safe_dump(seed_obj, sort_keys=True, allow_unicode=False).encode("utf-8")
    ).hexdigest()
    return f"{prefix}_{digest[:length]}"


def normalize_next_context(next_ctx: dict[str, Any], semantic_tags: list[str], messy: list[str]) -> dict[str, Any]:
    out = dict(next_ctx or {})
    out.setdefault("topic", "unknown")
    out.setdefault("stance", "neutral")
    out.setdefault("intent", "informational")
    out.setdefault("register", "technical")
    out.setdefault("politeness", "neutral")
    out.setdefault("epistemic_shading", "qualified")
    out.setdefault("continuity", "maintain")
    out.setdefault("direction", "next")

    # Deterministic coherence/shift flags from stance+continuity.
    stance = str(out.get("stance", "")).lower()
    continuity = str(out.get("continuity", "")).lower()
    shift_required = stance in {"reject", "conflict"} or continuity in {"break", "shift", "reset"}
    out["shift_required"] = bool(out.get("shift_required", shift_required))
    out["coherence"] = bool(out.get("coherence", not out["shift_required"]))

    if "importance" not in out:
        out["importance"] = 0.6

    clarifying_fields = list(out.get("clarifying_fields") or [])
    if not clarifying_fields:
        if messy:
            clarifying_fields.append("messy_input_clarification")
        if "identity_closure" in semantic_tags:
            clarifying_fields.append("closure_confirmation")
    out["clarifying_fields"] = clarifying_fields
    return out


def idob_envelope_to_working_tp(snapshot: dict[str, Any], msg_num: int) -> dict[str, Any]:
    sem = snapshot.get("semantic_envelope") or {}
    epi = snapshot.get("epistemic_envelope") or {}
    ide = snapshot.get("identity_envelope") or {}
    ctx = (snapshot.get("context_envelope") or {}).get("next_context") or {}
    prv = snapshot.get("provenance_envelope") or {}
    meta_env = snapshot.get("metadata_envelope") or {}
    trc = snapshot.get("trace_envelope") or {}

    proposition_set = list(sem.get("proposition_set") or [])
    semantic_tags = list(sem.get("semantic_tags") or [])
    messy = list(sem.get("messy_input_record") or [])

    semantic_core = {
        "summary": proposition_set[0] if proposition_set else "",
        "stability": max(0.0, min(1.0, 1.0 - float(epi.get("delta_h_percent", 0.5)) / 2.0)),
        "source": "idob_snapshot",
    }

    completion_state = "complete" if bool(ide.get("idob_complete")) else "in_progress"

    tp = {
        "_source": {
            "conversation": "conv_01",
            "message_number": msg_num,
            "schema": "20.40.060.700",
        },
        "semantic": {
            "semantic_core": semantic_core,
            "semantic_tags": semantic_tags,
            "lane_local_identity": copy.deepcopy(ide.get("lane_local_identity") or {}),
        },
        "proposition_set": proposition_set,
        "truth_evidence": list(sem.get("truth_evidence") or []),
        "completion_state": completion_state,
        "messy_input_record": messy,
        "delta_h_percent": float(epi.get("delta_h_percent", 0.0)),
        "ob_trace": list(trc.get("ob_trace") or []),
        "tb_trace": list(trc.get("tb_trace") or []),
        "policy_markers": list(meta_env.get("policy_markers") or []),
        "next_context": normalize_next_context(ctx, semantic_tags, messy),
        "lineage_log": list(prv.get("lineage_log") or []),
        "cob_state_snapshot": {
            "identity_mode": (ide.get("lane_local_identity") or {}).get("mode", "unknown"),
            "continuity_state": ide.get("identity_continuity", "unknown"),
            "topic_anchor": (ctx or {}).get("topic", "unknown"),
        },
        "sob_id": prv.get("sob_id"),
        "srob_id": prv.get("srob_id"),
        "cnob_id": prv.get("cnob_id"),
        "smob_id": prv.get("smob_id"),
        "idob_id": prv.get("idob_id"),
        "routing_path": list(prv.get("routing_path") or []),
        "ruleset_ids": list(prv.get("ruleset_ids") or []),
        "metadata": {
            "contextual_alignment_record": {
                "alignment": "aligned",
                "source": "mcb",
            },
            "identity_shift_record": {
                "changed": False,
                "geometry": ide.get("identity_geometry"),
            },
            "topic_anchor_record": {
                "anchor": (ctx or {}).get("topic", "unknown"),
            },
            "continuity_record": {
                "state": ide.get("identity_continuity", "unknown"),
            },
            "intent_record": {
                "final_intent": (ctx or {}).get("intent", "informational"),
            },
            "entropy_history": list(epi.get("entropy_history") or [float(epi.get("delta_h_percent", 0.0))]),
            "signature_history": list(meta_env.get("signature_history") or []),
            "idob_geometry": ide.get("identity_geometry"),
            "idob_pressure": ide.get("identity_pressure"),
            "idob_freeze": copy.deepcopy(ide.get("identity_freeze") or {}),
            "idob_basin_surface": copy.deepcopy(ide.get("identity_basin_surface") or {}),
            "idob_residuals": copy.deepcopy(ide.get("identity_residuals") or {}),
        },
        "_ouba_commit_context": {
            # Deterministic commit timestamp for replay-safe test-mode OuBA execution.
            "commit_timestamp": float(1800000000 + msg_num),
        },
    }

    return tp


def apply_stage_chain(tp: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(tp)

    for stage_name, trace_marker in STAGE_SEQUENCE:
        out["routing_path"].append(stage_name)
        out["lineage_log"].append(f"stage.{stage_name}")
        out["tb_trace"].append(trace_marker)

        if stage_name == "mcb":
            # MCB refines context and appends entropy history deterministically.
            if out["next_context"].get("shift_required"):
                out["next_context"]["continuity"] = "adjust"
            else:
                out["next_context"]["continuity"] = out["next_context"].get("continuity", "maintain")
            d = float(out.get("delta_h_percent", 0.0))
            adjusted = max(0.0, round(d - 0.02, 4))
            out["delta_h_percent"] = adjusted
            out["metadata"]["entropy_history"].append(adjusted)

        elif stage_name == "rbu":
            out["metadata"]["rbu_commit"] = {
                "committed": True,
                "route_len": len(out["routing_path"]),
            }

        elif stage_name == "tr":
            out["metadata"]["tr_decision"] = {
                "selected": "continue_pipeline",
                "deterministic": True,
            }
            out["tr_needs_update"] = False

        elif stage_name == "ctp":
            out["metadata"]["current_context"] = copy.deepcopy(out["next_context"])
            out["metadata"]["continuity_record"] = {
                "state": out["next_context"].get("continuity", "maintain"),
                "source": "ctp",
            }

        elif stage_name == "cex-ie":
            out["metadata"]["interpretive_record"] = {
                "roles": ["speaker", "system"],
                "topic": out["next_context"].get("topic"),
                "intent": out["next_context"].get("intent"),
            }

        elif stage_name == "cex-ccr":
            ie = out["metadata"].get("interpretive_record") or {}
            out["metadata"]["canonical_record"] = {
                "topic": ie.get("topic"),
                "intent": ie.get("intent"),
                "roles": sorted(list(ie.get("roles") or [])),
            }

        elif stage_name == "cex-pck":
            ccr = out["metadata"].get("canonical_record") or {}
            out["metadata"]["packed_record"] = {
                "packed_id": stable_id("pck", ccr),
                "payload": ccr,
            }

        elif stage_name == "cob":
            pck = out["metadata"].get("packed_record") or {}
            out["metadata"]["canonical_output_record"] = {
                "record_id": pck.get("packed_id"),
                "topic": out["next_context"].get("topic"),
            }

        elif stage_name == "cil":
            out["metadata"]["linkage_record"] = {
                "identity_mode": out["semantic"].get("lane_local_identity", {}).get("mode", "unknown"),
                "topic": out["next_context"].get("topic"),
                "linked": True,
            }

        elif stage_name == "cst-core":
            out["metadata"]["cst_core_metrics"] = {
                "stability": round(max(0.0, 1.0 - out["delta_h_percent"]), 4),
                "drift": round(out["delta_h_percent"], 4),
                "freeze_signal": bool((out["metadata"].get("idob_freeze") or {}).get("state") in {"full", "identity_freeze"}),
            }

        elif stage_name == "cst-ms":
            m = out["metadata"].get("cst_core_metrics") or {}
            out["metadata"]["cst_ms_summary"] = {
                "stability_band": "high" if m.get("stability", 0) >= 0.7 else "medium",
                "command": "hold" if m.get("stability", 0) >= 0.7 else "stabilize",
            }

        elif stage_name == "cst-mux":
            out["metadata"]["unified_stability_packet"] = {
                "core": copy.deepcopy(out["metadata"].get("cst_core_metrics") or {}),
                "summary": copy.deepcopy(out["metadata"].get("cst_ms_summary") or {}),
                "usp_id": stable_id("usp", out["metadata"].get("cst_ms_summary") or {}),
            }

    return out


def working_tp_to_ouba_input_doc(msg_file: str, tp: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": {
            "message_file": msg_file,
            "stage": "ouba_input",
            "pipeline_applied": [name for name, _ in STAGE_SEQUENCE],
        },
        "semantic_envelope": {
            "semantic_core": copy.deepcopy(tp["semantic"]["semantic_core"]),
            "proposition_set": copy.deepcopy(tp["proposition_set"]),
            "truth_evidence": copy.deepcopy(tp["truth_evidence"]),
            "completion_state": tp["completion_state"],
            "semantic_tags": copy.deepcopy(tp["semantic"]["semantic_tags"]),
            "lane_local_identity": copy.deepcopy(tp["semantic"]["lane_local_identity"]),
            "messy_input_record": copy.deepcopy(tp["messy_input_record"]),
        },
        "epistemic_envelope": {
            "delta_h_percent": tp["delta_h_percent"],
            "entropy_history": copy.deepcopy(tp["metadata"]["entropy_history"]),
        },
        "context_envelope": {
            "next_context": copy.deepcopy(tp["next_context"]),
            "current_context": copy.deepcopy(tp["metadata"].get("current_context") or {}),
        },
        "provenance_envelope": {
            "lineage_log": copy.deepcopy(tp["lineage_log"]),
            "sob_id": tp["sob_id"],
            "srob_id": tp["srob_id"],
            "cnob_id": tp["cnob_id"],
            "smob_id": tp["smob_id"],
            "idob_id": tp["idob_id"],
            "routing_path": copy.deepcopy(tp["routing_path"]),
            "ruleset_ids": copy.deepcopy(tp["ruleset_ids"]),
        },
        "metadata_envelope": {
            "policy_markers": copy.deepcopy(tp["policy_markers"]),
            "signature_history": copy.deepcopy(tp["metadata"]["signature_history"]),
            "contextual_alignment_record": copy.deepcopy(tp["metadata"]["contextual_alignment_record"]),
            "identity_shift_record": copy.deepcopy(tp["metadata"]["identity_shift_record"]),
            "topic_anchor_record": copy.deepcopy(tp["metadata"]["topic_anchor_record"]),
            "continuity_record": copy.deepcopy(tp["metadata"]["continuity_record"]),
            "intent_record": copy.deepcopy(tp["metadata"]["intent_record"]),
            "cst_core_metrics": copy.deepcopy(tp["metadata"].get("cst_core_metrics") or {}),
            "cst_ms_summary": copy.deepcopy(tp["metadata"].get("cst_ms_summary") or {}),
            "unified_stability_packet": copy.deepcopy(tp["metadata"].get("unified_stability_packet") or {}),
        },
        "trace_envelope": {
            "ob_trace": copy.deepcopy(tp["ob_trace"]),
            "tb_trace": copy.deepcopy(tp["tb_trace"]),
        },
    }


def ouba_output_to_doc(msg_file: str, ouba_input_doc: dict[str, Any], out_tp: dict[str, Any]) -> dict[str, Any]:
    tpsns = out_tp.get("TPSnS") if isinstance(out_tp.get("TPSnS"), dict) else {}
    return {
        "source": {
            "message_file": msg_file,
            "stage": "ouba_output",
        },
        "ouba_input_snapshot": ouba_input_doc,
        "ouba_output": {
            "ouba_complete": bool(out_tp.get("ouba_complete")),
            "TPSnS": copy.deepcopy(tpsns),
            "CTP": copy.deepcopy(out_tp.get("CTP") if isinstance(out_tp.get("CTP"), dict) else {}),
        },
    }


def process_one(msg_path: Path) -> tuple[Path, Path]:
    match = re.search(r"canonical_msg(\d+)_tp\.yaml$", msg_path.name)
    if not match:
        raise ValueError(f"Unexpected message filename format: {msg_path.name}")

    msg_num = int(match.group(1))
    snapshot = load_yaml(msg_path)

    tp = idob_envelope_to_working_tp(snapshot, msg_num)
    tp_after_chain = apply_stage_chain(tp)

    ouba_input_doc = working_tp_to_ouba_input_doc(msg_path.name, tp_after_chain)

    out_tp = OUBA(copy.deepcopy(tp_after_chain)).process(mode="testbench")
    ouba_output_doc = ouba_output_to_doc(msg_path.name, ouba_input_doc, out_tp)

    input_out_path = OUT_DIR / f"msg{msg_num}_ouba_input.yaml"
    output_out_path = OUT_DIR / f"msg{msg_num}_ouba_output.yaml"
    dump_yaml(input_out_path, ouba_input_doc)
    dump_yaml(output_out_path, ouba_output_doc)
    return input_out_path, output_out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    msg_files = sorted(CONV_DIR.glob("canonical_msg*_tp.yaml"), key=lambda p: int(re.search(r"canonical_msg(\d+)_tp\.yaml$", p.name).group(1)))

    if not msg_files:
        raise FileNotFoundError(f"No canonical message files found in {CONV_DIR}")

    generated: list[tuple[Path, Path]] = []
    for msg_path in msg_files:
        generated.append(process_one(msg_path))

    print(f"Generated {len(generated) * 2} files in {OUT_DIR}")
    for in_path, out_path in generated:
        print(f"- {in_path.name}")
        print(f"- {out_path.name}")


if __name__ == "__main__":
    main()
