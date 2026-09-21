import argparse
import json
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
        "status": "pending",
        "description": "Anomaly token classification and repair rules pending.",
    },
    {
        "id": "normalization",
        "raw_text": "a   b\tc",
        "status": "pending",
        "description": "Whitespace normalization parity checks pending.",
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
        "status": "pending",
        "description": "Token-flag propagation checks pending.",
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
        print(text)

    return 0 if payload["overall_status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
