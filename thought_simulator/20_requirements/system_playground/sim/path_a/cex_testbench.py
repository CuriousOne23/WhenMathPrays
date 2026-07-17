#!/usr/bin/env python3
"""
cex_testbench.py

Testbench for TS Path A CEx extract, per 20.107:

- 20.54_ssrgn_prim (SSR generator: last primitive to read TP, then freeze)
- 20.107_cex_extract (CEx: mechanical extract from SSR → CE-like record)

This is a logic simulator: it uses simplified, spec-aligned data structures
to verify determinism and replay-safety of the Path A extract pipeline.

Deliberate exclusions (per 20.107):
- No CST stability integration
- No COB identity-layer substrate
- No register/subculture modeling
- No ambiguity or "drift" metrics
- No Path B envelopes, TPU, or semantic repair
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
import copy
import hashlib
import json


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def deterministic_hash(obj: Any) -> str:
    """Deterministic hash of a Python object via JSON serialization."""
    s = json.dumps(obj, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def deep_copy(obj: Any) -> Any:
    """Convenience wrapper for deep copy."""
    return copy.deepcopy(obj)


# ---------------------------------------------------------------------------
# 20.54_ssrgn_prim – SSR Generator (Path A boundary)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TPCommitted:
    """Simplified committed TP representation."""
    turn_id: int
    text: str
    rrw: Dict[str, Any]  # referent/role/weight metadata
    policy_signature: str
    semantic_core: Dict[str, Any]
    discourse_act: str


@dataclass(frozen=True)
class SSR:
    """Frozen SSR packet: immutable projection of committed TP."""
    ssr_id: str
    turn_id: int
    projection_hash: str
    rrw: Dict[str, Any]
    policy_signature: str
    semantic_core: Dict[str, Any]
    discourse_act: str


class SSRGn:
    """
    20.54_ssrgn_prim – last primitive to read TP, then freeze.
    Deterministic: identical TPCommitted → identical SSR.
    """

    @staticmethod
    def project(tp: TPCommitted) -> Dict[str, Any]:
        # Spec-aligned: projection is a structural view, no new semantics.
        return {
            "turn_id": tp.turn_id,
            "text": tp.text,
            "rrw": tp.rrw,
            "policy_signature": tp.policy_signature,
            "semantic_core": tp.semantic_core,
            "discourse_act": tp.discourse_act,
        }

    @staticmethod
    def freeze(tp: TPCommitted) -> SSR:
        proj = SSRGn.project(tp)
        proj_hash = deterministic_hash(proj)
        ssr_id = f"SSR-{tp.turn_id}-{proj_hash[:12]}"
        return SSR(
            ssr_id=ssr_id,
            turn_id=tp.turn_id,
            projection_hash=proj_hash,
            rrw=deep_copy(tp.rrw),
            policy_signature=tp.policy_signature,
            semantic_core=deep_copy(tp.semantic_core),
            discourse_act=tp.discourse_act,
        )


# ---------------------------------------------------------------------------
# 20.107_cex_extract – CEx (Path A extract from SSR)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CExRecord:
    """
    Minimal, Path A–compliant extract record.

    Per 20.107:
    - No new semantics
    - No stability/ambiguity metrics
    - No register/subculture modeling
    - No identity-layer substrate
    - No CST signals
    """
    turn_id: int
    ssr_id: str
    projection_hash: str
    text: str
    rrw: Dict[str, Any]
    policy_signature: str
    semantic_core: Dict[str, Any]
    discourse_act: str
    extract_hash: str  # hash of the extract itself, for replay checks


class CExExtract:
    """
    20.107 – CEx: mechanical extract from SSR.

    Responsibilities:
    - Read SSR (Path A boundary object)
    - Produce a CE-like extract record
    - Do not infer, repair, or reinterpret semantics
    - Be fully deterministic: same SSR → same CExRecord
    """

    @staticmethod
    def extract(ssr: SSR) -> CExRecord:
        # Structural copy only; no semantic transformation.
        base = {
            "turn_id": ssr.turn_id,
            "ssr_id": ssr.ssr_id,
            "projection_hash": ssr.projection_hash,
            "text": ssr.text if hasattr(ssr, "text") else None,
            "rrw": ssr.rrw,
            "policy_signature": ssr.policy_signature,
            "semantic_core": ssr.semantic_core,
            "discourse_act": ssr.discourse_act,
        }
        # Note: SSR does not carry text directly in this simplified model,
        # so we re-project from semantic_core if needed. Here we keep it simple
        # and rely on TPCommitted → SSRGn.project for text fidelity.
        # To avoid hidden semantics, we do not modify any fields.

        # In this implementation, we re-use projection_hash as the text source:
        # the text is not strictly required for Path A replay checks, but we
        # include it for completeness by re-projecting from semantic_core if
        # desired. For now, we omit text reconstruction and keep it None.
        base["text"] = None

        extract_hash = deterministic_hash(base)

        return CExRecord(
            turn_id=ssr.turn_id,
            ssr_id=ssr.ssr_id,
            projection_hash=ssr.projection_hash,
            text=base["text"],
            rrw=deep_copy(ssr.rrw),
            policy_signature=ssr.policy_signature,
            semantic_core=deep_copy(ssr.semantic_core),
            discourse_act=ssr.discourse_act,
            extract_hash=extract_hash,
        )


# ---------------------------------------------------------------------------
# Testbench – Path A extract determinism
# ---------------------------------------------------------------------------

class CExTestbench:
    """
    End-to-end Path A simulator for:

    TPCommitted → SSRGn → CExExtract

    Focus:
    - determinism
    - replay-safety
    - structural fidelity of extract
    """

    def __init__(self):
        self.ssrgn = SSRGn()
        self.cex = CExExtract()

    def run_sequence(self, tp_sequence: List[TPCommitted]) -> List[CExRecord]:
        """
        Run a sequence of committed TP through the Path A pipeline.
        Returns CEx extract records per turn.
        """
        records: List[CExRecord] = []

        for tp in tp_sequence:
            # 1. SSRGn: freeze TP into SSR
            ssr = self.ssrgn.freeze(tp)

            # 2. CEx: mechanical extract from SSR
            rec = self.cex.extract(ssr)
            records.append(rec)

        return records

    def replay_sequence(self, tp_sequence: List[TPCommitted]) -> Tuple[List[CExRecord], List[CExRecord]]:
        """
        Run the same sequence twice and compare outputs for determinism.
        """
        # First run
        self.__init__()  # reset
        out1 = self.run_sequence(tp_sequence)

        # Second run
        self.__init__()  # reset
        out2 = self.run_sequence(tp_sequence)

        return out1, out2

    @staticmethod
    def compare_records(a: List[CExRecord], b: List[CExRecord]) -> bool:
        if len(a) != len(b):
            return False
        for r1, r2 in zip(a, b):
            if (
                r1.turn_id != r2.turn_id or
                r1.ssr_id != r2.ssr_id or
                r1.projection_hash != r2.projection_hash or
                r1.text != r2.text or
                r1.rrw != r2.rrw or
                r1.policy_signature != r2.policy_signature or
                r1.semantic_core != r2.semantic_core or
                r1.discourse_act != r2.discourse_act or
                r1.extract_hash != r2.extract_hash
            ):
                return False
        return True


# ---------------------------------------------------------------------------
# Example usage / basic tests
# ---------------------------------------------------------------------------

def make_example_tp_sequence() -> List[TPCommitted]:
    """
    Build a small synthetic TP sequence to exercise Path A extract behavior.

    Note: We keep the same example texts/registers, but CEx does not
    interpret "register" – it simply passes semantic_core through.
    """
    seq: List[TPCommitted] = []

    registers = ["technical", "casual", "technical", "east_la_lingo", "technical"]
    texts = [
        "Let’s formalize the stability metrics.",
        "Lol this is kinda wild.",
        "We should prove replay-safety.",
        "Yo this collapse thing better not blow up.",
        "Final check: deterministic signals only.",
    ]

    for i, (reg, txt) in enumerate(zip(registers, texts), start=1):
        tp = TPCommitted(
            turn_id=i,
            text=txt,
            rrw={"weights": {"core": 1.0}},
            policy_signature="policy_v1",
            semantic_core={"entities": ["TS"], "register": reg},
            discourse_act="assertion",
        )
        seq.append(tp)

    return seq


def main():
    tb = CExTestbench()
    seq = make_example_tp_sequence()

    # Single run
    records = tb.run_sequence(seq)
    print("Single run CEx records:")
    for i, r in enumerate(records, start=1):
        print(f"Turn {i}:")
        print(f"  turn_id:        {r.turn_id}")
        print(f"  ssr_id:         {r.ssr_id}")
        print(f"  projection_hash:{r.projection_hash}")
        print(f"  extract_hash:   {r.extract_hash}")
        print(f"  semantic_core:  {r.semantic_core}")
        print()

    # Replay determinism check
    out1, out2 = tb.replay_sequence(seq)
    deterministic = CExTestbench.compare_records(out1, out2)
    print("Replay determinism:", deterministic)


if __name__ == "__main__":
    main()
