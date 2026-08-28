"""IdOB Rulechecker — S2M packet walls for primitives/idob/idob.py."""
from __future__ import annotations

from typing import List, Tuple


class IdOBRuleChecker:
    def __init__(self, tp_input, tp_output, rules, utterance=None):
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.rules = rules or []
        self.utterance = utterance
        self.errors: List[Tuple[str, str]] = []

    def _assert(self, condition: bool, rule_id: str, message: str) -> None:
        if not condition:
            self.errors.append((rule_id, message))

    def _pkt(self):
        return (self.tp_out or {}).get("idob") or {}

    def _get(self, d, *keys):
        cur = d
        for k in keys:
            if not isinstance(cur, dict):
                return None
            cur = cur.get(k)
        return cur

    def deterministic_output_present(self, rule):
        self._assert(self.tp_out is not None, rule["id"], "IdOB output TP is missing.")

    def utterance_reference_present(self, rule):
        u = self.utterance
        if u is None:
            u = self.tp_in.get("utterance") or self._pkt().get("utterance")
        src = self.tp_in.get("utterance_source") or "input"
        self._assert(
            u is not None or src == "card",
            rule["id"],
            "utterance missing on test reference (set utterance or utterance_source=card)",
        )

    def packet_present(self, rule):
        pkt = self._pkt()
        self._assert(isinstance(pkt, dict) and pkt, rule["id"], "tp.idob packet missing")
        for key in ("resolution_status", "ready_for_ouba", "path_b_eligible", "idob_complete"):
            self._assert(key in pkt, rule["id"], f"tp.idob.{key} missing")

    def no_routing_or_dcb_writes(self, rule):
        before_rf = self._get(self.tp_in, "process", "routing_filter")
        after_rf = self._get(self.tp_out, "process", "routing_filter")
        if before_rf is not None:
            self._assert(
                before_rf == after_rf,
                rule["id"],
                "IdOB must not mutate process.routing_filter",
            )
        before_gs = self._get(self.tp_in, "metadata", "geometric_state")
        after_gs = self._get(self.tp_out, "metadata", "geometric_state")
        if before_gs is not None:
            self._assert(
                before_gs == after_gs,
                rule["id"],
                "IdOB must not mutate metadata.geometric_state (DCB-owned)",
            )

    def no_structural_writes(self, rule):
        in_meta = (self.tp_in or {}).get("metadata") or {}
        out_meta = (self.tp_out or {}).get("metadata") or {}
        for key in ("residue", "residue_metadata", "structural_metadata", "structural_graph"):
            if key in in_meta and in_meta.get(key) is not None:
                self._assert(
                    in_meta.get(key) == out_meta.get(key),
                    rule["id"],
                    f"metadata.{key} was modified by IdOB",
                )
        for key in ("ssg_signature", "ssg_layer_bitmap", "ssg_reason_code", "ssg_status"):
            if key in self.tp_in:
                self._assert(
                    self.tp_in.get(key) == self.tp_out.get(key),
                    rule["id"],
                    f"{key} was modified by IdOB",
                )

    def rank_subset_of_map(self, rule):
        pkt = self._pkt()
        cands = set(pkt.get("candidate_group_ids") or [])
        order = pkt.get("final_rank_order") or []
        self._assert(set(order) <= cands, rule["id"], "rank invented a group_id not on the map")

    def key_not_invented_from_cie(self, rule):
        pkt = self._pkt()
        if pkt.get("structural_key") and self.tp_in.get("structural_key"):
            self._assert(
                pkt.get("structural_key") == self.tp_in.get("structural_key"),
                rule["id"],
                "structural_key changed across IdOB",
            )

    def completion_flags_bool(self, rule):
        pkt = self._pkt()
        for key in ("ready_for_ouba", "path_b_eligible", "idob_complete"):
            self._assert(isinstance(pkt.get(key), bool), rule["id"], f"{key} must be bool")
        if self.tp_out.get("idob_complete") is not None:
            self._assert(isinstance(self.tp_out.get("idob_complete"), bool), rule["id"], "root idob_complete must be bool")

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
