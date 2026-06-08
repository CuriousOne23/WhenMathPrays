"""Verification harness for 40.100 InB memory buffer skeleton.

Scenarios exercise:
- Deterministic canonicalization (no inference)
- Bounded intake + reject-with-audit
- FIFO order preservation
- Provenance emission
- Deterministic replay
"""

from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime, timezone

from prototype import InB, CANONICAL_PROFILE


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
        _run_negative_oversize(),
        _run_negative_malformed(),
        _run_negative_unsupported_profile(),
        _run_positive_fifo_batch(),
        _run_positive_iiinb_handoff(),
        _run_positive_deterministic_replay(),
    ]

    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"

    report = {
        "module": "40.100_inb_prototypes",
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
            ],
        },
    }

    artifact_path = _write_artifact(report)
    print(f"InB harness status: {status}")
    print(f"Artifact: {artifact_path}")


if __name__ == "__main__":
    main()
