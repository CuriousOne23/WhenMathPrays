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

CONVERSATIONS = {
    "conv_02": {
        "md": REPO_ROOT
        / "thought_simulator"
        / "requirements_20"
        / "system_playground"
        / "simulation"
        / "conversations"
        / "conv_02"
        / "idob_input_output_examples.md",
        "out": REPO_ROOT
        / "thought_simulator"
        / "requirements_20"
        / "system_playground"
        / "simulation"
        / "conversations"
        / "conv_02"
        / "ouba",
        "topic": "project_purpose",
    },
    "conv_03": {
        "md": REPO_ROOT
        / "thought_simulator"
        / "requirements_20"
        / "system_playground"
        / "simulation"
        / "conversations"
        / "conv_03"
        / "idob"
        / "idob_conv_3.md",
        "out": REPO_ROOT
        / "thought_simulator"
        / "requirements_20"
        / "system_playground"
        / "simulation"
        / "conversations"
        / "conv_03"
        / "ouba",
        "topic": "decision_quality",
    },
}


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def dump_yaml(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=False)


def stable_id(prefix: str, seed_obj: Any, length: int = 12) -> str:
    digest = hashlib.sha256(
        yaml.safe_dump(seed_obj, sort_keys=True, allow_unicode=False).encode("utf-8")
    ).hexdigest()
    return f"{prefix}_{digest[:length]}"


def extract_output_yaml_blocks(md_text: str) -> list[dict[str, Any]]:
    lines = md_text.splitlines()
    blocks: list[dict[str, Any]] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        if "Output YAML" not in line:
            i += 1
            continue

        # Find next fenced yaml block.
        j = i + 1
        while j < len(lines) and not lines[j].strip().startswith("```yaml"):
            j += 1
        if j >= len(lines):
            i += 1
            continue

        k = j + 1
        while k < len(lines) and not lines[k].strip().startswith("```"):
            k += 1
        if k >= len(lines):
            break

        yaml_text = "\n".join(lines[j + 1 : k])
        parsed = yaml.safe_load(yaml_text) or {}
        if isinstance(parsed, dict):
            blocks.append(parsed)

        i = k + 1

    return blocks


def normalize_idob_output(block: dict[str, Any]) -> dict[str, Any]:
    # conv_03 style: tp: {metadata: {...}}
    if isinstance(block.get("tp"), dict):
        md = block["tp"].get("metadata")
        if isinstance(md, dict):
            return copy.deepcopy(md)

    # conv_02 style: TP.metadata.identity: {...}
    if "TP.metadata.identity" in block and isinstance(block["TP.metadata.identity"], dict):
        ident = copy.deepcopy(block["TP.metadata.identity"])
        return {
            "identity": ident,
            "lineage": [f"identity_{ident.get('geometry', 'unknown')}"] if ident.get("geometry") else [],
            "delta_h": _delta_from_identity(ident),
            "routing_fields": {
                "stance": "inform",
                "affect": "neutral",
                "epistemic_shading": "qualified",
                "commitment": "medium",
                "reservation": "none",
            },
            "semantic_role": "identity_state",
            "continuity_surface": ident.get("continuity", "continuation"),
            "regime_hint": _regime_from_identity(ident),
            "stability_metrics": {
                "coherence": _coherence_from_identity(ident),
                "tension": _tension_from_identity(ident),
                "drift": _drift_from_identity(ident),
            },
            "identity_layer": f"{ident.get('geometry', 'state')}_identity",
            "identity_residue": [],
            "adjacency_class": "identity_transition",
            "displacement_scale": _displacement_from_identity(ident),
        }

    # Fallback if minimally structured.
    return copy.deepcopy(block)


def _delta_from_identity(ident: dict[str, Any]) -> float:
    geom = str(ident.get("geometry", "formation")).lower()
    mapping = {
        "formation": 0.18,
        "refinement": 0.25,
        "correction": 0.33,
        "drift": 0.39,
        "conflict": 0.44,
        "bifurcation": 0.49,
        "stabilization": 0.54,
        "convergence": 0.59,
        "alignment": 0.64,
        "closure": 0.69,
    }
    return float(mapping.get(geom, 0.4))


def _regime_from_identity(ident: dict[str, Any]) -> str:
    geom = str(ident.get("geometry", "")).lower()
    if geom in {"conflict", "bifurcation"}:
        return "high_tension"
    if geom in {"drift", "correction"}:
        return "moderate_tension"
    if geom in {"alignment", "closure"}:
        return "stable"
    return "mild_tension"


def _coherence_from_identity(ident: dict[str, Any]) -> float:
    geom = str(ident.get("geometry", "")).lower()
    if geom in {"alignment", "closure"}:
        return 0.9
    if geom in {"conflict", "bifurcation"}:
        return 0.72
    return 0.82


def _tension_from_identity(ident: dict[str, Any]) -> float:
    geom = str(ident.get("geometry", "")).lower()
    if geom in {"conflict", "bifurcation"}:
        return 0.55
    if geom in {"drift", "correction"}:
        return 0.42
    return 0.25


def _drift_from_identity(ident: dict[str, Any]) -> float:
    geom = str(ident.get("geometry", "")).lower()
    if geom == "drift":
        return 0.41
    if geom in {"alignment", "closure"}:
        return 0.12
    return 0.27


def _displacement_from_identity(ident: dict[str, Any]) -> float:
    geom = str(ident.get("geometry", "")).lower()
    ordered = [
        "formation",
        "refinement",
        "correction",
        "drift",
        "conflict",
        "bifurcation",
        "stabilization",
        "convergence",
        "alignment",
        "closure",
    ]
    if geom not in ordered:
        return 0.5
    idx = ordered.index(geom)
    return round(0.12 + idx * 0.07, 2)


def build_working_tp(conv_name: str, msg_num: int, topic: str, md: dict[str, Any]) -> dict[str, Any]:
    identity = md.get("identity") if isinstance(md.get("identity"), dict) else {}
    routing_fields = md.get("routing_fields") if isinstance(md.get("routing_fields"), dict) else {}
    stability = md.get("stability_metrics") if isinstance(md.get("stability_metrics"), dict) else {}
    lineage = list(md.get("lineage") or [f"turn_{msg_num:02d}"])

    geometry = identity.get("geometry", "formation")
    continuity = identity.get("continuity", md.get("continuity_surface", "continuation"))
    stance = routing_fields.get("stance", "neutral")
    intent = md.get("semantic_role", "analysis")
    delta_h = float(md.get("delta_h", _delta_from_identity(identity)))

    next_context = {
        "topic": topic,
        "stance": stance,
        "intent": intent,
        "register": "technical",
        "politeness": "neutral",
        "epistemic_shading": routing_fields.get("epistemic_shading", "qualified"),
        "continuity": continuity,
        "direction": "next",
        "coherence": bool(stability.get("coherence", 0.8) >= 0.75),
        "shift_required": geometry in {"drift", "conflict", "bifurcation"},
        "importance": round(min(0.95, 0.5 + delta_h / 2.0), 2),
        "clarifying_fields": ["identity_geometry", "continuity_surface"],
    }

    semantic_tags = [
        f"identity_{geometry}",
        f"regime_{md.get('regime_hint', 'unknown')}",
        f"topic_{topic}",
    ]

    tp = {
        "_source": {
            "conversation": conv_name,
            "message_number": msg_num,
            "source_type": "idob_output_yaml",
        },
        "semantic": {
            "semantic_core": {
                "summary": f"{conv_name} msg{msg_num} identity state {geometry}",
                "stability": round(float(stability.get("coherence", 0.8)), 3),
                "source": "idob_output",
            },
            "semantic_tags": semantic_tags,
            "lane_local_identity": {
                "mode": "technical_user",
                "context": topic,
            },
        },
        "proposition_set": [
            f"Identity geometry is {geometry}.",
            f"Continuity surface is {continuity}.",
        ],
        "truth_evidence": [
            {
                "type": "support",
                "detail": f"Derived from {conv_name} msg{msg_num} IdOB output YAML.",
            }
        ],
        "completion_state": "complete" if geometry == "closure" else "in_progress",
        "messy_input_record": list(md.get("identity_residue") or []),
        "delta_h_percent": delta_h,
        "ob_trace": ["OB.lexical_parse", "OB.semantic_role_assignment"],
        "tb_trace": ["TB.contextual_alignment"],
        "policy_markers": ["policy.safe_completion_required"],
        "next_context": next_context,
        "lineage_log": lineage,
        "cob_state_snapshot": {
            "identity_mode": "technical_user",
            "continuity_state": continuity,
            "topic_anchor": topic,
        },
        "sob_id": f"sob_{msg_num:02d}",
        "srob_id": f"srob_{msg_num:02d}",
        "cnob_id": f"cnob_{msg_num:02d}",
        "smob_id": f"smob_{msg_num:02d}",
        "idob_id": f"idob_{msg_num:02d}",
        "routing_path": ["sob", "srob", "cnob", "smob", "idob"],
        "ruleset_ids": ["policy_v3", "safety_ruleset_12"],
        "metadata": {
            "contextual_alignment_record": {
                "alignment": "aligned",
                "source": "mcb",
            },
            "identity_shift_record": {
                "changed": geometry in {"correction", "drift", "conflict", "bifurcation"},
                "geometry": geometry,
            },
            "topic_anchor_record": {
                "anchor": topic,
            },
            "continuity_record": {
                "state": continuity,
            },
            "intent_record": {
                "final_intent": intent,
            },
            "entropy_history": [delta_h],
            "signature_history": [f"sig_{msg_num:03d}"],
            "idob_output_metadata": copy.deepcopy(md),
        },
        "_ouba_commit_context": {
            "commit_timestamp": float(1900000000 + msg_num),
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

        elif stage_name == "cex-ie":
            out["metadata"]["interpretive_record"] = {
                "topic": out["next_context"].get("topic"),
                "intent": out["next_context"].get("intent"),
            }

        elif stage_name == "cex-ccr":
            ie = out["metadata"].get("interpretive_record") or {}
            out["metadata"]["canonical_record"] = {
                "topic": ie.get("topic"),
                "intent": ie.get("intent"),
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


def working_tp_to_ouba_input_doc(conv_name: str, msg_num: int, tp: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": {
            "conversation": conv_name,
            "message": msg_num,
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


def ouba_output_to_doc(conv_name: str, msg_num: int, ouba_input_doc: dict[str, Any], out_tp: dict[str, Any]) -> dict[str, Any]:
    tpsns = out_tp.get("TPSnS") if isinstance(out_tp.get("TPSnS"), dict) else {}
    return {
        "source": {
            "conversation": conv_name,
            "message": msg_num,
            "stage": "ouba_output",
        },
        "ouba_input_snapshot": ouba_input_doc,
        "ouba_output": {
            "ouba_complete": bool(out_tp.get("ouba_complete")),
            "TPSnS": copy.deepcopy(tpsns),
            "CTP": copy.deepcopy(out_tp.get("CTP") if isinstance(out_tp.get("CTP"), dict) else {}),
        },
    }


def process_conversation(conv_name: str, md_path: Path, out_dir: Path, topic: str) -> dict[str, Any]:
    text = load_text(md_path)
    output_blocks = extract_output_yaml_blocks(text)

    if len(output_blocks) != 10:
        raise ValueError(f"{conv_name}: expected 10 IdOB Output YAML blocks, found {len(output_blocks)}")

    out_dir.mkdir(parents=True, exist_ok=True)
    run_entries: list[dict[str, Any]] = []

    for i, block in enumerate(output_blocks, start=1):
        md = normalize_idob_output(block)
        tp = build_working_tp(conv_name, i, topic, md)
        tp_after_chain = apply_stage_chain(tp)

        ouba_input_doc = working_tp_to_ouba_input_doc(conv_name, i, tp_after_chain)
        out_tp = OUBA(copy.deepcopy(tp_after_chain)).process(mode="testbench")
        ouba_output_doc = ouba_output_to_doc(conv_name, i, ouba_input_doc, out_tp)

        input_path = out_dir / f"msg{i}_ouba_input.yaml"
        output_path = out_dir / f"msg{i}_ouba_output.yaml"
        dump_yaml(input_path, ouba_input_doc)
        dump_yaml(output_path, ouba_output_doc)

        tpsns = out_tp.get("TPSnS") if isinstance(out_tp.get("TPSnS"), dict) else {}
        run_entries.append(
            {
                "message": i,
                "input_file": input_path.name,
                "output_file": output_path.name,
                "tpsns_id": tpsns.get("tpsns_id"),
                "commit_timestamp": tpsns.get("commit_timestamp"),
                "commit_hash": tpsns.get("commit_hash"),
                "routing_epoch_id": tpsns.get("routing_epoch_id"),
            }
        )

    run_log = {
        "conversation": conv_name,
        "source_markdown": str(md_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "source_type": "IdOB Output YAML blocks",
        "messages_processed": len(run_entries),
        "files_generated": len(run_entries) * 2,
        "pipeline": [name for name, _ in STAGE_SEQUENCE] + ["ouba"],
        "entries": run_entries,
    }
    dump_yaml(out_dir / "run_log.yaml", run_log)

    return {
        "conversation": conv_name,
        "messages_processed": len(run_entries),
        "out_dir": str(out_dir),
    }


def main() -> None:
    results = []
    for conv_name, cfg in CONVERSATIONS.items():
        results.append(process_conversation(conv_name, cfg["md"], cfg["out"], cfg["topic"]))

    print("Completed OuBA generation for markdown conversations:")
    for r in results:
        print(f"- {r['conversation']}: {r['messages_processed']} messages -> {r['out_dir']}")


if __name__ == "__main__":
    main()
