import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ie_compat_intake import build_committed_stream


CASES: List[Dict[str, Any]] = [
    {
        "id": "punctuation",
        "raw_text": "Hello, world!",
        "status": "active",
        "description": "Punctuation is emitted as standalone tokens.",
    },
    {
        "id": "unicode_marks",
        "raw_text": "cafe\u0301",
        "status": "active",
        "description": "Combining unicode marks are normalized deterministically.",
    },
    {
        "id": "anomalies",
        "raw_text": "abc\ufffddef",
        "status": "active",
        "description": "Anomaly tokens are classified and recorded with deterministic flags.",
    },
    {
        "id": "normalization",
        "raw_text": "a   b\tc",
        "status": "active",
        "description": "Whitespace normalization is deterministic and recorded in token provenance.",
    },
    {
        "id": "multi_token_roles",
        "raw_text": "in front of the house",
        "status": "pending",
        "description": "Multi-token role matcher parity checks pending.",
    },
    {
        "id": "dictionary_precedence",
        "raw_text": "where is lead",
        "status": "pending",
        "description": "Layered dictionary precedence checks pending.",
    },
    {
        "id": "segment_boundaries",
        "raw_text": "First. Second.",
        "status": "pending",
        "description": "Explicit boundary parity checks pending.",
    },
    {
        "id": "token_flags_propagation",
        "raw_text": "(alpha)",
        "status": "active",
        "description": "Token flags are propagated deterministically across punctuation boundaries.",
    },
    {
        "id": "deterministic_ids",
        "raw_text": "repeatable input",
        "status": "active",
        "description": "Token and segment IDs are stable across runs.",
    },
]


def _check_punctuation(stream: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
    surfaces = [t["surface"] for t in stream.get("tokens", [])]
    classes = [t["token_class"] for t in stream.get("tokens", [])]

    checks = [
        (surfaces == ["Hello", ",", "world", "!"], "surface tokenization mismatch"),
        (classes == ["WORD", "PUNCT", "WORD", "PUNCT"], "token class sequence mismatch"),
    ]

    failed = [msg for ok, msg in checks if not ok]
    details = {
        "surfaces": surfaces,
        "classes": classes,
    }
    return len(failed) == 0, failed, details


def _check_unicode_marks(stream: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
    tokens = stream.get("tokens", [])
    surfaces = [t["surface"] for t in tokens]
    normalized = [t["normalized"] for t in tokens]

    if len(tokens) != 1:
        return False, ["expected a single token for combining-mark word"], {
            "token_count": len(tokens),
            "surfaces": surfaces,
            "normalized": normalized,
        }

    tok = tokens[0]
    nflags = tok.get("flags", {}).get("normalization_flags", [])
    nrules = tok.get("provenance", {}).get("normalization_rule_ids", [])

    checks = [
        (tok.get("surface") == "cafe\u0301", "surface mismatch"),
        (tok.get("normalized") == "caf\u00e9", "normalized unicode NFC mismatch"),
        ("unicode_nfc" in nflags, "unicode_nfc flag missing"),
        ("norm.unicode.nfc.001" in nrules, "unicode normalization rule id missing"),
    ]

    failed = [msg for ok, msg in checks if not ok]
    details = {
        "surfaces": surfaces,
        "normalized": normalized,
        "normalization_flags": nflags,
        "normalization_rule_ids": nrules,
    }
    return len(failed) == 0, failed, details


def _check_anomalies(stream: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
    tokens = stream.get("tokens", [])
    anomalies = stream.get("anomalies", [])

    surfaces = [t.get("surface") for t in tokens]
    classes = [t.get("token_class") for t in tokens]
    anomaly_tokens = [t for t in tokens if t.get("token_class") == "ANOMALY"]

    checks = [
        (surfaces == ["abc", "\ufffd", "def"], "anomaly tokenization mismatch"),
        (classes == ["WORD", "ANOMALY", "WORD"], "anomaly token class sequence mismatch"),
        (len(anomaly_tokens) == 1, "expected exactly one ANOMALY token"),
        (len(anomalies) == 1, "expected exactly one anomaly record"),
    ]

    if anomaly_tokens:
        checks.append(
            (
                "replacement_char" in anomaly_tokens[0].get("flags", {}).get("anomaly_flags", []),
                "replacement_char anomaly flag missing",
            )
        )

    if anomalies:
        checks.extend(
            [
                (anomalies[0].get("token_id") == 2, "anomaly token_id mismatch"),
                (anomalies[0].get("anomaly_type") == "replacement_char", "anomaly type mismatch"),
                (
                    anomalies[0].get("detected_by_rule") == "anom.detect.replacement_char.001",
                    "anomaly detection rule id mismatch",
                ),
            ]
        )

    failed = [msg for ok, msg in checks if not ok]
    details = {
        "surfaces": surfaces,
        "classes": classes,
        "anomaly_records": anomalies,
    }
    return len(failed) == 0, failed, details


def _check_normalization(stream: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
    tokens = stream.get("tokens", [])
    surfaces = [t.get("surface") for t in tokens]
    normalized = [t.get("normalized") for t in tokens]
    spans = [(t.get("span_start"), t.get("span_end")) for t in tokens]

    checks = [
        (surfaces == ["a", "b", "c"], "normalized tokenization mismatch"),
        (normalized == ["a", "b", "c"], "normalized values mismatch"),
        (spans == [(0, 1), (4, 5), (6, 7)], "token spans mismatch"),
        (
            "whitespace_collapsed" in tokens[1].get("flags", {}).get("normalization_flags", [])
            if len(tokens) > 1
            else False,
            "second token missing whitespace_collapsed flag",
        ),
        (
            "norm.whitespace.collapse.001" in tokens[1].get("provenance", {}).get("normalization_rule_ids", [])
            if len(tokens) > 1
            else False,
            "second token missing whitespace normalization rule id",
        ),
        (
            "whitespace_collapsed" in tokens[2].get("flags", {}).get("normalization_flags", [])
            if len(tokens) > 2
            else False,
            "third token missing whitespace_collapsed flag",
        ),
    ]

    failed = [msg for ok, msg in checks if not ok]
    details = {
        "surfaces": surfaces,
        "normalized": normalized,
        "spans": spans,
        "token2_normalization_flags": tokens[1].get("flags", {}).get("normalization_flags", []) if len(tokens) > 1 else [],
        "token3_normalization_flags": tokens[2].get("flags", {}).get("normalization_flags", []) if len(tokens) > 2 else [],
    }
    return len(failed) == 0, failed, details


def _check_token_flags_propagation(stream: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
    tokens = stream.get("tokens", [])
    surfaces = [t.get("surface") for t in tokens]
    classes = [t.get("token_class") for t in tokens]
    token_flags = [t.get("flags", {}).get("token_flags", []) for t in tokens]

    checks = [
        (surfaces == ["(", "alpha", ")"], "tokenization mismatch for punctuation-wrapped token"),
        (classes == ["PUNCT", "WORD", "PUNCT"], "token class sequence mismatch"),
        ("boundary_left" in token_flags[0] if len(token_flags) > 0 else False, "first token missing boundary_left flag"),
        ("boundary_right" in token_flags[-1] if len(token_flags) > 0 else False, "last token missing boundary_right flag"),
        (token_flags[1] == [] if len(token_flags) > 1 else False, "middle token should not have boundary flags"),
    ]

    failed = [msg for ok, msg in checks if not ok]
    details = {
        "surfaces": surfaces,
        "classes": classes,
        "token_flags": token_flags,
    }
    return len(failed) == 0, failed, details


def _check_deterministic_ids(raw_text: str) -> Tuple[bool, List[str], Dict[str, Any]]:
    stream_a = build_committed_stream(raw_text)
    stream_b = build_committed_stream(raw_text)
    ids_a = [(t["token_id"], t["segment_id"]) for t in stream_a.get("tokens", [])]
    ids_b = [(t["token_id"], t["segment_id"]) for t in stream_b.get("tokens", [])]

    ok = ids_a == ids_b
    failed = [] if ok else ["token/segment id sequence differs across identical runs"]
    return ok, failed, {"ids_a": ids_a, "ids_b": ids_b}


def _evaluate_case(case: Dict[str, Any]) -> Dict[str, Any]:
    case_id = case["id"]
    raw_text = case["raw_text"]
    status = case["status"]

    if status != "active":
        return {
            "case_id": case_id,
            "status": "pending",
            "pass": False,
            "raw_text": raw_text,
            "description": case["description"],
            "checks": [],
            "details": {"note": "not executed"},
        }

    if case_id == "deterministic_ids":
        ok, failed, details = _check_deterministic_ids(raw_text)
    else:
        stream = build_committed_stream(raw_text)
        if case_id == "punctuation":
            ok, failed, details = _check_punctuation(stream)
        elif case_id == "unicode_marks":
            ok, failed, details = _check_unicode_marks(stream)
        elif case_id == "anomalies":
            ok, failed, details = _check_anomalies(stream)
        elif case_id == "normalization":
            ok, failed, details = _check_normalization(stream)
        elif case_id == "token_flags_propagation":
            ok, failed, details = _check_token_flags_propagation(stream)
        else:
            ok, failed, details = False, ["active case has no evaluator"], {}

    return {
        "case_id": case_id,
        "status": "executed",
        "pass": ok,
        "raw_text": raw_text,
        "description": case["description"],
        "checks": [] if ok else failed,
        "details": details,
    }


def run_harness(case_filter: Optional[str] = None) -> Dict[str, Any]:
    selected = [c for c in CASES if case_filter in (None, c["id"]) ]

    results = [_evaluate_case(c) for c in selected]
    executed = [r for r in results if r["status"] == "executed"]
    pending = [r for r in results if r["status"] == "pending"]
    passed = [r for r in executed if r["pass"]]
    failed = [r for r in executed if not r["pass"]]

    overall_status = "pass" if not failed else "fail"

    return {
        "harness": "replay_parity_harness",
        "contract_version": "ie-compat-v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "overall_status": overall_status,
        "summary": {
            "total_selected": len(selected),
            "executed": len(executed),
            "passed": len(passed),
            "failed": len(failed),
            "pending": len(pending),
        },
        "results": results,
    }


def _to_yaml(payload: Dict[str, Any]) -> str:
    try:
        import yaml  # type: ignore
    except Exception as exc:
        raise RuntimeError("YAML output requested but PyYAML is not available") from exc
    return yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic replay parity harness")
    parser.add_argument("--case", dest="case_id", help="Run only one case id", default=None)
    parser.add_argument("--format", choices=["json", "yaml"], default="json")
    parser.add_argument("--output", help="Optional output file path", default=None)
    args = parser.parse_args()

    payload = run_harness(case_filter=args.case_id)
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    if args.format == "yaml":
        text = _to_yaml(payload)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(text + "\n", encoding="utf-8")
    else:
        # Emit UTF-8 bytes directly to avoid Windows console code-page failures.
        sys.stdout.buffer.write((text + "\n").encode("utf-8"))

    return 0 if payload["overall_status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
