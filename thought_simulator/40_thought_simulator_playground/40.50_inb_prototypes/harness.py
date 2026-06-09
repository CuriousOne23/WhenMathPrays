"""Verification harness for 40.50 InB memory buffer skeleton (Phase B complete).

Scenarios exercise full test matrix: canonicalization, schema validation,
transport isolation, tick boundary, FIFO, replay, handoff, zero-event window,
profile deferral, diagnostics, timestamp metadata.
"""

from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime, timezone

from prototype import (
    InB,
    CANONICAL_PROFILE,
    INTAKE_SCHEMA_VERSION,
    WIRE_MAP_VERSION,
    run_first_stage,
)


ARTIFACT_NAME = "inb_verification_run_2026-06-08.json"


def _run_positive_clean() -> dict:
    inb = InB()
    raw = {
        "content": "Hello   World!!!  This is a test.",
        "source": "user:alice",
        "intake_order": 0,
    }
    out = inb.normalize(raw)
    return {
        "scenario": "positive_clean_canonicalization",
        "result": "PASS" if out["canonical_content"] == "hello world! this is a test." and out["provenance"]["outcome"] == "accepted" else "FAIL",
        "input": raw,
        "output": out,
    }


def _run_positive_equivalent_forms() -> dict:
    inb = InB()
    raw1 = {"content": "Hello   World!!!", "source": "test", "intake_order": 0}
    raw2 = {"content": "hello world!!", "source": "test", "intake_order": 1}
    out1 = inb.normalize(raw1)
    out2 = inb.normalize(raw2)
    same_canonical = out1["canonical_content"] == out2["canonical_content"]
    return {
        "scenario": "positive_equivalent_surface_forms",
        "result": "PASS" if same_canonical else "FAIL",
        "inputs": [raw1, raw2],
        "outputs": [out1, out2],
        "note": "Equivalent noisy forms produce identical canonical output (non-semantic normalization)",
    }


def _run_negative_oversize() -> dict:
    inb = InB()
    raw = {"content": "x" * 5000, "source": "test", "intake_order": 0}
    out = inb.normalize(raw)
    return {
        "scenario": "negative_oversize_payload",
        "result": "PASS" if out["provenance"]["outcome"] == "rejected" and out["provenance"]["reason_code"] == "OVERSIZE_PAYLOAD" else "FAIL",
        "input": raw,
        "output": out,
    }


def _run_negative_malformed() -> dict:
    inb = InB()
    # non-dict input
    out = inb.normalize("not a dict")
    return {
        "scenario": "negative_malformed_input",
        "result": "PASS" if out["provenance"]["outcome"] == "rejected" and out["provenance"]["reason_code"] == "MALFORMED_INPUT" else "FAIL",
        "input": "not a dict",
        "output": out,
    }


def _run_negative_unsupported_profile() -> dict:
    inb = InB()
    raw = {"content": "test", "source": "test", "profile": "v9.9"}
    out = inb.normalize(raw)
    return {
        "scenario": "negative_unsupported_profile",
        "result": "PASS" if out["provenance"]["outcome"] == "rejected" and out["provenance"]["reason_code"] == "UNSUPPORTED_PROFILE" else "FAIL",
        "input": raw,
        "output": out,
    }


def _run_positive_fifo_batch() -> dict:
    inb = InB()
    raws = [
        {"content": "First message", "source": "batch", "intake_order": 0},
        {"content": "Second   message!!!", "source": "batch", "intake_order": 1},
    ]
    outs = inb.batch_normalize(raws)
    orders_preserved = [o["provenance"]["intake_order"] for o in outs] == [0, 1]
    canonicals_ok = outs[0]["canonical_content"] == "first message" and outs[1]["canonical_content"] == "second message!"
    return {
        "scenario": "positive_fifo_batch_order",
        "result": "PASS" if orders_preserved and canonicals_ok else "FAIL",
        "inputs": raws,
        "outputs": outs,
    }


def _run_positive_iiinb_handoff() -> dict:
    inb = InB()
    raw = {"content": "Handoff test", "source": "test", "intake_order": 0}
    out = inb.normalize(raw)
    handoff = out.get("handoff", {})
    ok = (
        handoff.get("next_stage") == "input_semantic_repair"
        and handoff.get("downstream_after_repair") == "routing"
        and handoff.get("contract_version") == "inb_to_iiinb_v1"
        and out["provenance"]["outcome"] == "accepted"
    )
    return {
        "scenario": "positive_iiinb_handoff_contract",
        "result": "PASS" if ok else "FAIL",
        "input": raw,
        "handoff": handoff,
        "hlr": ["HLR-20.100-020", "HLR-20.101-003"],
    }


def _run_positive_unicode_normalization() -> dict:
    inb = InB()
    raw_composed = {"content": "caf\u00e9", "source": "unicode", "intake_order": 0}
    raw_decomposed = {"content": "cafe\u0301", "source": "unicode", "intake_order": 1}
    raw_fullwidth = {"content": "\uff21\uff22\uff23", "source": "unicode", "intake_order": 2}
    out_composed = inb.normalize(raw_composed)
    out_decomposed = inb.normalize(raw_decomposed)
    out_fullwidth = inb.normalize(raw_fullwidth)
    ok = (
        out_composed["canonical_content"] == out_decomposed["canonical_content"] == "café"
        and out_fullwidth["canonical_content"] == "abc"
    )
    return {
        "scenario": "positive_unicode_normalization",
        "result": "PASS" if ok else "FAIL",
        "outputs": [out_composed, out_decomposed, out_fullwidth],
        "hlr": ["HLR-20.100-010"],
    }


def _run_positive_transport_metadata_isolation() -> dict:
    inb = InB()
    raw_a = {"content": "same payload", "source": "channel:alpha", "intake_order": 0}
    raw_b = {"content": "same payload", "source": "channel:beta", "intake_order": 99}
    out_a = inb.normalize(raw_a)
    out_b = inb.normalize(raw_b)
    ok = (
        out_a["canonical_content"] == out_b["canonical_content"] == "same payload"
        and out_a["provenance"]["source"] != out_b["provenance"]["source"]
    )
    return {
        "scenario": "positive_transport_metadata_isolation",
        "result": "PASS" if ok else "FAIL",
        "inputs": [raw_a, raw_b],
        "outputs": [out_a, out_b],
        "hlr": ["HLR-20.100-009"],
    }


def _run_positive_tick_boundary_first_stage() -> dict:
    inb = InB()
    mtp = {"semantic_core": "frozen", "tp": {"intake_bound": {}}}
    raw = {"content": "Tick boundary test", "source": "tick", "intake_order": 0}
    stage = run_first_stage(inb, raw, mtp)
    ok = stage["mtp_unchanged"] and stage["handoff_emitted"] and not stage["downstream_invoked"]
    return {
        "scenario": "positive_tick_boundary_first_stage",
        "result": "PASS" if ok else "FAIL",
        "stage_result": stage,
        "hlr": ["HLR-20.100-019", "10.10.10"],
    }


def _run_negative_unsupported_schema() -> dict:
    inb = InB()
    cases = [
        {"content": "ok", "schema_version": "bad_schema", "source": "test"},
        {"content": "ok", "wire_map_version": "bad_wire", "source": "test"},
        {"content": 123, "source": "test"},
    ]
    outs = [inb.normalize(c) for c in cases]
    ok = (
        outs[0]["provenance"]["reason_code"] == "UNSUPPORTED_SCHEMA"
        and outs[1]["provenance"]["reason_code"] == "UNSUPPORTED_WIRE_MAP"
        and outs[2]["provenance"]["reason_code"] == "INVALID_FIELD_TYPE"
    )
    return {
        "scenario": "negative_unsupported_schema",
        "result": "PASS" if ok else "FAIL",
        "inputs": cases,
        "outputs": outs,
        "hlr": ["HLR-20.100-004", "HLR-20.100-016"],
    }


def _run_positive_zero_event_window() -> dict:
    inb = InB()
    window = inb.process_tick_intake([])
    ok = (
        window["zero_event"]
        and window["events"] == []
        and window["provenance"]["reason_code"] == "ZERO_EVENT_WINDOW"
    )
    return {
        "scenario": "positive_zero_event_window",
        "result": "PASS" if ok else "FAIL",
        "window": window,
        "hlr": ["HLR-20.100-023"],
    }


def _run_profile_activation_boundary() -> dict:
    inb = InB(profile=CANONICAL_PROFILE)
    activation = inb.request_profile_activation("v1.1")
    raw = {"content": "Profile defer test", "source": "test", "intake_order": 0}
    mid_tick = inb.normalize(raw)
    boundary = inb.apply_safe_boundary()
    post_boundary = inb.normalize(raw)
    ok = (
        activation["deferred"]
        and activation["reason_code"] == "PROFILE_ACTIVATION_DEFERRED"
        and mid_tick["provenance"]["profile"] == CANONICAL_PROFILE
        and boundary["active_profile"] == "v1.1"
        and post_boundary["provenance"]["profile"] == "v1.1"
    )
    return {
        "scenario": "profile_activation_boundary",
        "result": "PASS" if ok else "FAIL",
        "activation": activation,
        "mid_tick_profile": mid_tick["provenance"]["profile"],
        "post_boundary_profile": post_boundary["provenance"]["profile"],
        "hlr": ["HLR-20.100-014", "HLR-20.100-015"],
    }


def _run_positive_diagnostic_export_ordering() -> dict:
    inb = InB()
    raws = [
        {"content": "second", "source": "diag", "intake_order": 1},
        {"content": "first", "source": "diag", "intake_order": 0},
    ]
    outs = inb.batch_normalize(raws)
    export_a = inb.export_intake_diagnostics(outs)
    export_b = inb.export_intake_diagnostics(list(reversed(outs)))
    records = json.loads(export_a)
    ok = export_a == export_b and [r["intake_order"] for r in records] == [0, 1]
    return {
        "scenario": "positive_diagnostic_export_ordering",
        "result": "PASS" if ok else "FAIL",
        "export": export_a,
        "hlr": ["HLR-20.100-022"],
    }


def _run_positive_timestamp_metadata_only() -> dict:
    inb = InB()
    raws = [
        {"content": "ordered content", "source": "ts", "intake_order": 0, "timestamp": "2026-06-08T10:00:00Z"},
        {"content": "ordered content", "source": "ts", "intake_order": 1, "timestamp": "2026-06-08T11:00:00Z"},
    ]
    outs = inb.batch_normalize(raws)
    ok = (
        outs[0]["canonical_content"] == outs[1]["canonical_content"]
        and outs[0]["provenance"]["intake_order"] == 0
        and outs[1]["provenance"]["intake_order"] == 1
        and outs[0]["provenance"]["timestamp"] != outs[1]["provenance"]["timestamp"]
    )
    return {
        "scenario": "positive_timestamp_metadata_only",
        "result": "PASS" if ok else "FAIL",
        "outputs": outs,
        "hlr": ["HLR-20.100-021"],
    }


def _run_positive_deterministic_replay() -> dict:
    run_a = InB()
    run_b = InB()

    raw = {"content": "Replay test   content!!!", "source": "replay", "intake_order": 42}

    out_a = run_a.normalize(raw)
    out_b = run_b.normalize(raw)

    identical = out_a == out_b
    return {
        "scenario": "positive_deterministic_replay",
        "result": "PASS" if identical else "FAIL",
        "input": raw,
        "output_a": out_a,
        "output_b": out_b,
        "state_digest": out_a.get("state_digest"),
    }


def _write_artifact(report: dict) -> Path:
    artifact_dir = Path(__file__).resolve().parent / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = artifact_dir / ARTIFACT_NAME
    artifact_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return artifact_path


def main() -> None:
    scenarios = [
        _run_positive_clean(),
        _run_positive_equivalent_forms(),
        _run_positive_unicode_normalization(),
        _run_positive_transport_metadata_isolation(),
        _run_positive_tick_boundary_first_stage(),
        _run_negative_oversize(),
        _run_negative_malformed(),
        _run_negative_unsupported_profile(),
        _run_negative_unsupported_schema(),
        _run_positive_fifo_batch(),
        _run_positive_iiinb_handoff(),
        _run_positive_deterministic_replay(),
        _run_positive_zero_event_window(),
        _run_profile_activation_boundary(),
        _run_positive_diagnostic_export_ordering(),
        _run_positive_timestamp_metadata_only(),
    ]

    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"

    report = {
        "module": "40.50_inb_prototypes",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "profile": CANONICAL_PROFILE,
        "status": status,
        "scenarios": scenarios,
        "summary": {
            "total_scenarios": len(scenarios),
            "passed": sum(1 for s in scenarios if s["result"] == "PASS"),
            "core_invariants_demonstrated": [
                "non_semantic_canonicalization",
                "bounded_reject_with_audit",
                "deterministic_replay",
                "fifo_order_preservation",
                "provenance_emission",
                "schema_validation",
                "transport_metadata_isolation",
                "tick_boundary_first_stage",
                "zero_event_window",
                "profile_activation_deferral",
                "diagnostic_export_ordering",
                "timestamp_metadata_only",
            ],
            "schema_version": INTAKE_SCHEMA_VERSION,
            "wire_map_version": WIRE_MAP_VERSION,
        },
    }

    artifact_path = _write_artifact(report)
    print(f"InB harness status: {status}")
    print(f"Artifact: {artifact_path}")


if __name__ == "__main__":
    main()
