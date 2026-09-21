import hashlib
import json
from pathlib import Path

import pytest


SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "support"
    / "contracts"
    / "committed_token_stream.v1.schema.json"
)


def _load_schema() -> dict:
    with SCHEMA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _minimal_stream(raw_text: str = "Hello, world!") -> dict:
    text_hash = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
    return {
        "contract_version": "ie-compat-v1",
        "stream_id": "stream-1",
        "source": {
            "raw_text": raw_text,
            "raw_text_hash": text_hash,
            "intake_profile": "pathA_ie_compat",
            "created_at_utc": "2026-09-21T00:00:00Z",
        },
        "pipeline_versions": {
            "tokenizer_version": "tok-v1",
            "normalization_version": "norm-v1",
            "dictionary_bundle_version": "dict-bundle-v1",
            "id_strategy_version": "ids-v1",
        },
        "dictionary_context": {
            "layer_order": [
                "runtime_dictionary",
                "dev_dictionary",
                "meaning_dictionary",
                "reference_objects",
                "field_reference_tables",
                "flow_contracts",
            ],
            "precedence_mode": "ordered-first-hit-with-longest-match",
            "bundle_hash": "bundlehash-1",
        },
        "segments": [
            {
                "segment_id": 1,
                "start_token_id": 1,
                "end_token_id": 3,
                "boundary_reason": "explicit_ie_boundary",
            }
        ],
        "tokens": [
            {
                "token_id": 1,
                "segment_id": 1,
                "span_start": 0,
                "span_end": 4,
                "surface": "Hello",
                "normalized": "hello",
                "token_class": "WORD",
                "role": {
                    "chosen": "none",
                    "candidates": [],
                },
                "flags": {
                    "token_flags": ["boundary_left"],
                    "anomaly_flags": [],
                    "normalization_flags": ["case_folded"],
                },
                "provenance": {
                    "normalization_rule_ids": ["norm.casefold.001"],
                    "dictionary_rule_id": None,
                    "dictionary_layer": None,
                    "precedence_rank": None,
                    "multi_token_match_id": None,
                },
            },
            {
                "token_id": 2,
                "segment_id": 1,
                "span_start": 5,
                "span_end": 6,
                "surface": ",",
                "normalized": ",",
                "token_class": "PUNCT",
                "role": {
                    "chosen": "none",
                    "candidates": [],
                },
                "flags": {
                    "token_flags": [],
                    "anomaly_flags": [],
                    "normalization_flags": [],
                },
                "provenance": {
                    "normalization_rule_ids": [],
                    "dictionary_rule_id": None,
                    "dictionary_layer": None,
                    "precedence_rank": None,
                    "multi_token_match_id": None,
                },
            },
            {
                "token_id": 3,
                "segment_id": 1,
                "span_start": 7,
                "span_end": 12,
                "surface": "world",
                "normalized": "world",
                "token_class": "WORD",
                "role": {
                    "chosen": "none",
                    "candidates": [],
                },
                "flags": {
                    "token_flags": ["boundary_right"],
                    "anomaly_flags": [],
                    "normalization_flags": [],
                },
                "provenance": {
                    "normalization_rule_ids": [],
                    "dictionary_rule_id": None,
                    "dictionary_layer": None,
                    "precedence_rank": None,
                    "multi_token_match_id": None,
                },
            },
        ],
        "anomalies": [],
        "deltas": {
            "parity_status": "identical",
            "delta_count": 0,
            "entries": [],
        },
    }


def _build_committed_stream(_raw_text: str) -> dict:
    # TODO: Replace this placeholder with the IE-compat intake layer entrypoint.
    raise NotImplementedError("IE compatibility intake layer is not wired yet")


PARITY_CASES = [
    ("punctuation", "Hello, world!"),
    ("unicode_marks", "cafe\u0301"),
    ("anomalies", "abc\ufffddef"),
    ("normalization", "a   b\tc"),
    ("multi_token_roles", "in front of the house"),
    ("dictionary_precedence", "where is lead"),
    ("segment_boundaries", "First. Second."),
    ("token_flags_propagation", "(alpha)"),
    ("deterministic_ids", "repeatable input"),
]


def test_schema_file_exists_and_is_valid_json() -> None:
    assert SCHEMA_PATH.exists(), f"Schema file not found at {SCHEMA_PATH}"
    schema = _load_schema()
    assert schema["$schema"].startswith("https://json-schema.org/")


def test_minimal_stream_validates_against_schema() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    jsonschema.validate(instance=_minimal_stream(), schema=_load_schema())


@pytest.mark.parametrize("case_name,raw_text", PARITY_CASES)
@pytest.mark.xfail(reason="Waiting for IE compatibility intake layer implementation", strict=False)
def test_replay_parity_matrix_scaffold(case_name: str, raw_text: str) -> None:
    # TODO: When intake exists, compare produced stream with IE fixture stream.
    produced = _build_committed_stream(raw_text)
    assert produced["source"]["raw_text"] == raw_text


@pytest.mark.xfail(reason="Waiting for deterministic ID implementation", strict=False)
def test_deterministic_ids_same_input_same_ids() -> None:
    raw_text = "repeatable input"
    stream_a = _build_committed_stream(raw_text)
    stream_b = _build_committed_stream(raw_text)

    ids_a = [(t["token_id"], t["segment_id"]) for t in stream_a["tokens"]]
    ids_b = [(t["token_id"], t["segment_id"]) for t in stream_b["tokens"]]
    assert ids_a == ids_b
