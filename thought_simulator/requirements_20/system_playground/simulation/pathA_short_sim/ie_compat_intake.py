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

_MULTI_TOKEN_ROLE_PATTERNS = [
    {
        "tokens": ["in", "front", "of"],
        "role": "relation",
        "rule_id": "role.multi.in_front_of.001",
        "layer": "runtime_dictionary",
        "precedence_rank": 1,
    }
]

_SINGLE_TOKEN_ROLE_ENTRIES = {
    "lead": [
        {
            "role": "theme",
            "rule_id": "role.dict.runtime.lead.001",
            "layer": "runtime_dictionary",
            "precedence_rank": 1,
        },
        {
            "role": "action",
            "rule_id": "role.dict.meaning.lead.001",
            "layer": "meaning_dictionary",
            "precedence_rank": 3,
        },
    ]
}


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
    if "\ufffd" in surface:
        return "ANOMALY"
    if len(surface) == 1 and re.match(r"[^\w\s]", surface, re.UNICODE):
        return "PUNCT"
    if surface.isdigit():
        return "NUMBER"
    return "WORD"


def _apply_multi_token_roles(tokens: List[dict]) -> None:
    if not tokens:
        return

    next_match_id = 1
    i = 0
    while i < len(tokens):
        best_pattern = None
        best_len = 0

        for pattern in _MULTI_TOKEN_ROLE_PATTERNS:
            seq = pattern["tokens"]
            n = len(seq)
            if i + n > len(tokens):
                continue
            window = [t.get("normalized", "") for t in tokens[i:i + n]]
            if window == seq and n > best_len:
                best_pattern = pattern
                best_len = n

        if best_pattern is None:
            i += 1
            continue

        match_id = f"mtr-{next_match_id}"
        next_match_id += 1

        for j in range(i, i + best_len):
            token = tokens[j]
            token["role"] = {
                "chosen": best_pattern["role"],
                "candidates": [
                    {
                        "role_name": best_pattern["role"],
                        "score": 1.0,
                        "match_rule_id": best_pattern["rule_id"],
                        "match_layer": best_pattern["layer"],
                    }
                ],
            }
            token["provenance"]["dictionary_rule_id"] = best_pattern["rule_id"]
            token["provenance"]["dictionary_layer"] = best_pattern["layer"]
            token["provenance"]["precedence_rank"] = best_pattern["precedence_rank"]
            token["provenance"]["multi_token_match_id"] = match_id

        i += best_len


def _apply_single_token_dictionary_roles(tokens: List[dict]) -> None:
    for token in tokens:
        # Preserve explicit multi-token assignments.
        if token.get("provenance", {}).get("multi_token_match_id") is not None:
            continue

        norm = token.get("normalized", "")
        entries = _SINGLE_TOKEN_ROLE_ENTRIES.get(norm, [])
        if not entries:
            continue

        ordered = sorted(entries, key=lambda e: int(e["precedence_rank"]))
        chosen = ordered[0]

        token["role"] = {
            "chosen": chosen["role"],
            "candidates": [
                {
                    "role_name": entry["role"],
                    "score": 1.0,
                    "match_rule_id": entry["rule_id"],
                    "match_layer": entry["layer"],
                }
                for entry in ordered
            ],
        }
        token["provenance"]["dictionary_rule_id"] = chosen["rule_id"]
        token["provenance"]["dictionary_layer"] = chosen["layer"]
        token["provenance"]["precedence_rank"] = chosen["precedence_rank"]


def build_committed_stream(raw_text: str) -> dict:
    raw_text_hash = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
    stream_id = hashlib.sha256(("ie-compat-v1|" + raw_text).encode("utf-8")).hexdigest()[:16]

    token_specs = _tokenize_ie_compat(raw_text)
    tokens = []
    anomalies = []
    prev_end: int | None = None

    for idx, spec in enumerate(token_specs, start=1):
        surface = str(spec["surface"])
        span_start = int(spec["span_start"])
        span_end = int(spec["span_end"])
        normalized_unicode = unicodedata.normalize("NFC", surface)
        normalized = normalized_unicode.lower()
        token_class = _classify_token(surface)

        token_flags: List[str] = []
        if idx == 1:
            token_flags.append("boundary_left")
        if idx == len(token_specs):
            token_flags.append("boundary_right")

        normalization_flags: List[str] = []
        normalization_rule_ids: List[str] = []
        anomaly_flags: List[str] = []

        if prev_end is not None:
            interstitial = raw_text[prev_end:span_start]
            # IE-compat placeholder: any non-canonical token boundary whitespace
            # is marked as a collapsed whitespace normalization event.
            if interstitial and interstitial != " ":
                normalization_flags.append("whitespace_collapsed")
                normalization_rule_ids.append("norm.whitespace.collapse.001")

        if normalized_unicode != surface:
            normalization_flags.append("unicode_nfc")
            normalization_rule_ids.append("norm.unicode.nfc.001")
        if normalized != surface:
            normalization_flags.append("case_folded")
            normalization_rule_ids.append("norm.casefold.001")

        if token_class == "ANOMALY":
            anomaly_flags.append("replacement_char")
            anomalies.append(
                {
                    "anomaly_id": f"a-{len(anomalies) + 1}",
                    "token_id": idx,
                    "anomaly_type": "replacement_char",
                    "detected_by_rule": "anom.detect.replacement_char.001",
                    "repaired": False,
                    "repair_rule_id": None,
                    "repair_explanation": None,
                }
            )

        tokens.append(
            {
                "token_id": idx,
                "segment_id": 1,
                "span_start": span_start,
                "span_end": span_end,
                "surface": surface,
                "normalized": normalized,
                "token_class": token_class,
                "role": {
                    "chosen": "none",
                    "candidates": [],
                },
                "flags": {
                    "token_flags": token_flags,
                    "anomaly_flags": anomaly_flags,
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
        prev_end = span_end

    _apply_multi_token_roles(tokens)
    _apply_single_token_dictionary_roles(tokens)

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
        "anomalies": anomalies,
        "deltas": {
            "parity_status": "identical",
            "delta_count": 0,
            "entries": [],
        },
    }
