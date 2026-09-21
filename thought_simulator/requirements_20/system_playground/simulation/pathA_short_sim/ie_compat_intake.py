import hashlib
import re
import unicodedata
from datetime import datetime, timezone
from typing import Dict, List


_LAYER_ORDER = [
    "runtime_dictionary",
    "dev_dictionary",
    "meaning_dictionary",
    "reference_objects",
    "field_reference_tables",
    "flow_contracts",
]


def _tokenize_ie_compat(raw_text: str) -> List[Dict[str, int | str]]:
    # Split into word chunks (optionally followed by combining marks)
    # and single punctuation marks.
    token_re = re.compile(r"\w[\w\u0300-\u036f]*|[^\w\s]", re.UNICODE)
    out: List[Dict[str, int | str]] = []
    for match in token_re.finditer(raw_text):
        surface = match.group(0)
        out.append({
            "surface": surface,
            "span_start": match.start(),
            "span_end": match.end(),
        })
    return out


def _classify_token(surface: str) -> str:
    if len(surface) == 1 and re.match(r"[^\w\s]", surface, re.UNICODE):
        return "PUNCT"
    if surface.isdigit():
        return "NUMBER"
    return "WORD"


def build_committed_stream(raw_text: str) -> dict:
    raw_text_hash = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
    stream_id = hashlib.sha256(("ie-compat-v1|" + raw_text).encode("utf-8")).hexdigest()[:16]

    token_specs = _tokenize_ie_compat(raw_text)
    tokens = []

    for idx, spec in enumerate(token_specs, start=1):
        surface = str(spec["surface"])
        normalized_unicode = unicodedata.normalize("NFC", surface)
        normalized = normalized_unicode.lower()

        token_flags: List[str] = []
        if idx == 1:
            token_flags.append("boundary_left")
        if idx == len(token_specs):
            token_flags.append("boundary_right")

        normalization_flags: List[str] = []
        normalization_rule_ids: List[str] = []
        if normalized_unicode != surface:
            normalization_flags.append("unicode_nfc")
            normalization_rule_ids.append("norm.unicode.nfc.001")
        if normalized != surface:
            normalization_flags.append("case_folded")
            normalization_rule_ids.append("norm.casefold.001")

        tokens.append(
            {
                "token_id": idx,
                "segment_id": 1,
                "span_start": int(spec["span_start"]),
                "span_end": int(spec["span_end"]),
                "surface": surface,
                "normalized": normalized,
                "token_class": _classify_token(surface),
                "role": {
                    "chosen": "none",
                    "candidates": [],
                },
                "flags": {
                    "token_flags": token_flags,
                    "anomaly_flags": [],
                    "normalization_flags": normalization_flags,
                },
                "provenance": {
                    "normalization_rule_ids": normalization_rule_ids,
                    "dictionary_rule_id": None,
                    "dictionary_layer": None,
                    "precedence_rank": None,
                    "multi_token_match_id": None,
                },
            }
        )

    segment_end = len(tokens) if tokens else 1
    segments = [
        {
            "segment_id": 1,
            "start_token_id": 1,
            "end_token_id": segment_end,
            "boundary_reason": "inferred_rule_id:single_segment_v1",
        }
    ]

    return {
        "contract_version": "ie-compat-v1",
        "stream_id": stream_id,
        "source": {
            "raw_text": raw_text,
            "raw_text_hash": raw_text_hash,
            "intake_profile": "pathA_ie_compat",
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
        },
        "pipeline_versions": {
            "tokenizer_version": "tok-v1",
            "normalization_version": "norm-v1",
            "dictionary_bundle_version": "dict-bundle-v1",
            "id_strategy_version": "ids-v1",
        },
        "dictionary_context": {
            "layer_order": _LAYER_ORDER,
            "precedence_mode": "ordered-first-hit-with-longest-match",
            "bundle_hash": "bundlehash-1",
        },
        "segments": segments,
        "tokens": tokens,
        "anomalies": [],
        "deltas": {
            "parity_status": "identical",
            "delta_count": 0,
            "entries": [],
        },
    }
