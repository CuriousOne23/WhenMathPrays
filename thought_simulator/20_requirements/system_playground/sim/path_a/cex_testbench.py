#!/usr/bin/env python3
"""
cex_testbench.py

Testbench for TS Path A CEx extract, per 20.107:

- CEx is a mechanical, replay-safe extract.
- No Path B semantics.
- No SSR, COB, CST, CIL.
- No stability, ambiguity, or register modeling.

This simulator uses simplified, spec-aligned data structures
to verify determinism and structural fidelity of the CEx extract.
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
# Upstream Path A input – committed TP (or equivalent)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TPCommitted:
    """
    Simplified Path A upstream record.

    This is just a structural container:
    - No semantics are inferred here.
    - CEx must treat this as read-only input.
    """
    turn_id: int
    text: str
    rrw: Dict[str, Any]          # referent/role/weight metadata
    policy_signature: str
    semantic_core: Dict[str, Any]
    discourse_act: str


# ---------------------------------------------------------------------------
# 20.107_cex_extract – CEx (Path A extract)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CExRecord:
    """
    Minimal, Path A–compliant extract record.

    Per 20.107:
    - No new semantics.
    - No stability/ambiguity metrics.
    - No register/subculture modeling.
    - No identity-layer substrate.
    - No Path B envelopes.
    """
    turn_id: int
    text: str
    rrw: Dict[str, Any]
    policy_signature: str
    semantic_core: Dict[str, Any]
    discourse_act: str
    extract_hash: str  # hash of the extract itself, for replay checks


class CEx:
    """
    20.107 – CEx: mechanical extract.

    Responsibilities:
    - Read upstream Path A record (TPCommitted or equivalent).
    - Produce a CExRecord by structural copy only.
    - Do not infer, repair, or reinterpret semantics.
    - Be fully deterministic: same input → same CExRecord.
    """

    @staticmethod
    def extract(tp: TPCommitted) -> CExRecord:
        base = {
            "turn_id": tp.turn_id,
            "text": tp.text,
            "rrw": tp.rrw,
            "policy_signature": tp.policy_signature,
            "semantic_core": tp.semantic_core,
            "discourse_act": tp.discourse_act,
        }

        extract_hash = deterministic_hash(base)

        return CExRecord(
            turn_id=tp.turn_id,
            text=tp.text,
            rrw=deep_copy(tp.rrw),
            policy_signature=tp.policy_signature,
            semantic_core=deep_copy(tp.semantic_core),
            discourse_act=tp.discourse_act,
            extract_hash=extract_hash,
        )


# ---------------------------------------------------------------------------
# Testbench – Path A extract determinism
# ---------------------------------------------------------------------------

class CExTestbench:
    """
    End-to-end Path A simulator for:

    TPCommitted → CEx.extract

    Focus:
    - determinism
    - replay-safety
    - structural fidelity of extract
    """

    def __init__(self):
        self.cex = CEx()

    def run_sequence(self, tp_sequence: List[TPCommitted]) -> List[CExRecord]:
        """
        Run a sequence of committed TP through the Path A extract.
        Returns CEx records per turn.
        """
        records: List[CExRecord] = []

        for tp in tp_sequence:
            rec = self.cex.extract(tp)
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

    CEx does not interpret these fields; it just copies them structurally.
    """
    seq: List[TPCommitted] = []

    texts = [
        "Let’s formalize the stability metrics.",
        "Lol this is kinda wild.",
        "We should prove replay-safety.",
        "Yo this collapse thing better not blow up.",
        "Final check: deterministic signals only.",
    ]

    for i, txt in enumerate(texts, start=1):
        tp = TPCommitted(
            turn_id=i,
            text=txt,
            rrw={"weights": {"core": 1.0}},
            policy_signature="policy_v1",
            semantic_core={"entities": ["TS"]},
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
        print(f"  turn_id:      {r.turn_id}")
        print(f"  text:         {r.text}")
        print(f"  extract_hash: {r.extract_hash}")
        print()

    # Replay determinism check
    out1, out2 = tb.replay_sequence(seq)
    deterministic = CExTestbench.compare_records(out1, out2)
    print("Replay determinism:", deterministic)


if __name__ == "__main__":
    main()
