"""
OuBA Rulechecker (Version 0.1)
Aligned with ouba_rules.yaml, 20.40.060.xxx, and progressive_lineup_testing.
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import List, Tuple


REQUIRED_TPSNS_KEYS = (
    "tpsns_id",
    "commit_timestamp",
    "commit_hash",
    "routing_epoch_id",
    "semantic_core",
    "proposition_set",
    "truth_evidence",
    "completion_state",
    "semantic_tags",
    "lane_local_identity",
    "messy_input_record",
    "delta_h_percent",
    "ob_trace",
    "tb_trace",
    "policy_markers",
    "next_context",
    "lineage_log",
    "cob_state_snapshot",
    "contextual_alignment_record",
    "identity_shift_record",
    "topic_anchor_record",
    "continuity_record",
    "intent_record",
    "provenance",
    "metadata",
)

REQUIRED_NEXT_CONTEXT_KEYS = (
    "topic",
    "stance",
    "intent",
    "register",
    "politeness",
    "epistemic_shading",
    "continuity",
    "direction",
    "coherence",
    "shift_required",
    "importance",
    "clarifying_fields",
)


class OUBARuleChecker:
    def __init__(self, tp_input, tp_output, rules):
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.rules = rules or []
        self.errors: List[Tuple[str, str]] = []

    def _assert(self, condition: bool, rule_id: str, message: str) -> None:
        if not condition:
            self.errors.append((rule_id, message))

    def _canonical_bytes(self, obj) -> bytes:
        return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

    def deterministic_output_present(self, rule):
        self._assert(self.tp_out is not None, rule["id"], "OuBA output TP is missing.")

    def commit_envelopes_present(self, rule):
        self._assert("TPSnS" in self.tp_out, rule["id"], "TPSnS envelope missing")
        self._assert("CTP" in self.tp_out, rule["id"], "CTP envelope missing")

    def tpsns_required_keys_present(self, rule):
        tpsns = self.tp_out.get("TPSnS") if isinstance(self.tp_out.get("TPSnS"), dict) else {}
        for key in REQUIRED_TPSNS_KEYS:
            self._assert(key in tpsns, rule["id"], f"TPSnS missing key {key}")

    def ctp_equals_tpsns(self, rule):
        self._assert(
            self.tp_out.get("CTP") == self.tp_out.get("TPSnS"),
            rule["id"],
            "CTP and TPSnS differ",
        )

    def commit_hash_valid(self, rule):
        tpsns = self.tp_out.get("TPSnS") if isinstance(self.tp_out.get("TPSnS"), dict) else None
        if not isinstance(tpsns, dict):
            self._assert(False, rule["id"], "TPSnS missing for commit-hash check")
            return
        actual = tpsns.get("commit_hash")
        clone = copy.deepcopy(tpsns)
        clone["commit_hash"] = ""
        expected = hashlib.sha256(self._canonical_bytes(clone)).hexdigest()
        self._assert(actual == expected, rule["id"], "commit_hash does not match canonical payload")

    def required_context_fields_present(self, rule):
        tpsns = self.tp_out.get("TPSnS") if isinstance(self.tp_out.get("TPSnS"), dict) else {}
        ctx = tpsns.get("next_context") if isinstance(tpsns.get("next_context"), dict) else {}
        for key in REQUIRED_NEXT_CONTEXT_KEYS:
            self._assert(key in ctx, rule["id"], f"next_context missing key {key}")

    def no_forbidden_mutation(self, rule):
        # Input fields that must remain untouched by OuBA.
        if "TR" in self.tp_in:
            self._assert(self.tp_in.get("TR") == self.tp_out.get("TR"), rule["id"], "TR was modified")

        in_proc = self.tp_in.get("process") if isinstance(self.tp_in.get("process"), dict) else {}
        out_proc = self.tp_out.get("process") if isinstance(self.tp_out.get("process"), dict) else {}
        if "routing_filter" in in_proc:
            self._assert(
                in_proc.get("routing_filter") == out_proc.get("routing_filter"),
                rule["id"],
                "process.routing_filter was modified",
            )

        in_meta = self.tp_in.get("metadata") if isinstance(self.tp_in.get("metadata"), dict) else {}
        out_meta = self.tp_out.get("metadata") if isinstance(self.tp_out.get("metadata"), dict) else {}
        for key in ("geometric_state", "geometric_history", "residue"):
            if key in in_meta:
                self._assert(in_meta.get(key) == out_meta.get(key), rule["id"], f"metadata.{key} was modified")

    def run(self):
        for rule in self.rules:
            check = rule.get("check")
            if not check:
                continue
            method = getattr(self, check, None)
            if method is None:
                self.errors.append((rule["id"], f"Unknown rule check: {check}"))
                continue
            method(rule)
        return self.errors
