#!/usr/bin/env python3
"""
cex_testbench.py

Testbench for TS Path A/Path B stability:
- 20.54_ssrgn_prim (SSR generator)
- 20.32_cob_requirements (COB: identity-layer substrate, incl. register)
- 20.32.010_cst_requirements (CST: stability integration + signals)
- 20.33_cil_requirements (CIL: intake packet + register_hint)

This is a logic simulator: it uses simplified, spec-aligned data structures
to verify determinism, stability, and replay-safety of the pipeline.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple
import copy
import hashlib
import json
import random


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
# 20.32_cob_requirements – COB (identity-layer substrate)
# ---------------------------------------------------------------------------

@dataclass
class IdentityLayer:
    layer_id: str
    referent: Dict[str, Any]
    temporal_anchor: Dict[str, Any]
    discourse_anchor: Dict[str, Any]
    field_importance: Dict[str, Any]
    lineage: Dict[str, Any]
    register: str  # subculture / communication style
    eviction_score: float = 0.0
    strength: float = 1.0


@dataclass
class COBSnapshot:
    layers: List[IdentityLayer] = field(default_factory=list)
    history_hash: str = ""  # for replay checks


class COB:
    """
    20.32 – COB: identity-layer substrate, including register.
    - Ingests SSRGn packets.
    - Applies CST signals.
    - Maintains deterministic, bounded identity-layer set.
    """

    MAX_LAYERS = 20

    def __init__(self):
        self.layers: List[IdentityLayer] = []

    def _make_layer_from_ssr(self, ssr: SSR) -> IdentityLayer:
        # Simplified mapping: referent/anchors from semantic_core/rrw.
        referent = {"entities": ssr.semantic_core.get("entities", [])}
        temporal_anchor = {"turn_id": ssr.turn_id}
        discourse_anchor = {"act": ssr.discourse_act}
        field_importance = {"weights": ssr.rrw.get("weights", {})}
        lineage = {"origin_ssr": ssr.ssr_id}
        register = ssr.semantic_core.get("register", "neutral")
        layer_id = f"IL-{ssr.turn_id}-{ssr.ssr_id[:8]}"
        return IdentityLayer(
            layer_id=layer_id,
            referent=referent,
            temporal_anchor=temporal_anchor,
            discourse_anchor=discourse_anchor,
            field_importance=field_importance,
            lineage=lineage,
            register=register,
        )

    def ingest_ssr(self, ssr: SSR) -> None:
        """
        Deterministic ingestion from SSRGn.
        """
        new_layer = self._make_layer_from_ssr(ssr)
        self.layers.append(new_layer)
        self._apply_capacity_constraints()

    def apply_cst_signals(self, signals: List[Dict[str, Any]]) -> None:
        """
        Apply CST correction signals deterministically.
        Signals examples:
        - {"type": "strengthen_register", "layer_id": "...", "delta": 0.1}
        - {"type": "weaken_register", "layer_id": "...", "delta": 0.1}
        - {"type": "merge", "source_id": "...", "target_id": "..."}
        - {"type": "split", "layer_id": "..."}
        """
        for sig in signals:
            t = sig.get("type")
            if t in ("strengthen_register", "weaken_register"):
                self._apply_register_signal(sig)
            elif t == "merge":
                self._apply_merge_signal(sig)
            elif t == "split":
                self._apply_split_signal(sig)
            # collapse/freeze/thaw would be handled similarly, but omitted for brevity

        self._apply_capacity_constraints()

    def _apply_register_signal(self, sig: Dict[str, Any]) -> None:
        layer_id = sig.get("layer_id")
        delta = sig.get("delta", 0.0)
        for layer in self.layers:
            if layer.layer_id == layer_id:
                # Strength/weakening modeled via strength field.
                layer.strength = max(0.0, min(2.0, layer.strength + delta))

    def _apply_merge_signal(self, sig: Dict[str, Any]) -> None:
        source_id = sig.get("source_id")
        target_id = sig.get("target_id")
        source = None
        target = None
        for layer in self.layers:
            if layer.layer_id == source_id:
                source = layer
            if layer.layer_id == target_id:
                target = layer
        if source and target and source is not target:
            # Simple merge: average strength, keep target register.
            target.strength = (target.strength + source.strength) / 2.0
            # Eviction source.
            self.layers = [l for l in self.layers if l.layer_id != source_id]

    def _apply_split_signal(self, sig: Dict[str, Any]) -> None:
        layer_id = sig.get("layer_id")
        for layer in self.layers:
            if layer.layer_id == layer_id:
                # Simple split: create a new layer with slightly modified register.
                new_register = layer.register + "_variant"
                new_layer = IdentityLayer(
                    layer_id=f"{layer.layer_id}-split",
                    referent=deep_copy(layer.referent),
                    temporal_anchor=deep_copy(layer.temporal_anchor),
                    discourse_anchor=deep_copy(layer.discourse_anchor),
                    field_importance=deep_copy(layer.field_importance),
                    lineage=deep_copy(layer.lineage),
                    register=new_register,
                    strength=layer.strength * 0.9,
                )
                self.layers.append(new_layer)
                break

    def _apply_capacity_constraints(self) -> None:
        """
        Enforce MAX_LAYERS via eviction_score.
        """
        if len(self.layers) <= self.MAX_LAYERS:
            return
        # Evict lowest strength layers first.
        self.layers.sort(key=lambda l: l.strength)
        self.layers = self.layers[-self.MAX_LAYERS :]

    def snapshot(self) -> COBSnapshot:
        snap_layers = deep_copy(self.layers)
        history_hash = deterministic_hash(
            [{"layer_id": l.layer_id, "register": l.register, "strength": l.strength}
             for l in snap_layers]
        )
        return COBSnapshot(layers=snap_layers, history_hash=history_hash)


# ---------------------------------------------------------------------------
# 20.32.010_cst_requirements – CST (stability integration + signals)
# ---------------------------------------------------------------------------

@dataclass
class CSTMetrics:
    identity_drift: float
    referent_drift: float
    temporal_drift: float
    discourse_drift: float
    field_importance_drift: float
    register_drift: float
    register_ambiguity: float
    register_continuity: float
    register_collapse_score: float


class CST:
    """
    20.32.010 – CST: stability integration over COB snapshot.
    Emits correction signals deterministically, including register axis.
    """

    def __init__(self):
        self.history: List[COBSnapshot] = []

    def integrate(self, snapshot: COBSnapshot) -> CSTMetrics:
        """
        Compute simplified metrics from snapshot.
        In a real implementation, this would use long-horizon windows.
        """
        self.history.append(snapshot)
        layers = snapshot.layers

        # Simplified drift: variance of strength across layers.
        strengths = [l.strength for l in layers] or [0.0]
        mean_strength = sum(strengths) / len(strengths)
        drift_strength = sum((s - mean_strength) ** 2 for s in strengths) / len(strengths)

        # Register drift: count of distinct registers.
        registers = [l.register for l in layers]
        distinct_registers = len(set(registers))
        register_drift = float(distinct_registers - 1) if distinct_registers > 0 else 0.0

        # Ambiguity: heuristic – more distinct registers → more ambiguity.
        register_ambiguity = min(1.0, register_drift / 5.0)

        # Continuity: heuristic – if same register appears across many layers.
        continuity_score = 0.0
        if registers:
            most_common = max(set(registers), key=registers.count)
            continuity_score = registers.count(most_common) / max(1, len(registers))

        # Collapse: heuristic – if continuity is very low but drift is high.
        collapse_score = 1.0 if continuity_score < 0.2 and register_drift > 3 else 0.0

        return CSTMetrics(
            identity_drift=drift_strength,
            referent_drift=0.0,  # omitted for brevity
            temporal_drift=0.0,
            discourse_drift=0.0,
            field_importance_drift=0.0,
            register_drift=register_drift,
            register_ambiguity=register_ambiguity,
            register_continuity=continuity_score,
            register_collapse_score=collapse_score,
        )

    def emit_signals(self, snapshot: COBSnapshot, metrics: CSTMetrics) -> List[Dict[str, Any]]:
        """
        Emit correction signals based on metrics.
        Respect deterministic ordering:
        collapse → freeze/thaw → structural → ambiguity/drift → relevance.
        Here we focus on register-related signals.
        """
        signals: List[Dict[str, Any]] = []
        layers = snapshot.layers

        # 1. Collapse handling (simplified: weaken all registers).
        if metrics.register_collapse_score > 0.0:
            for l in layers:
                signals.append({
                    "type": "weaken_register",
                    "layer_id": l.layer_id,
                    "delta": -0.2,
                })

        # 2. Structural (merge/split) – simplified: merge weakest into strongest if drift high.
        if metrics.register_drift > 2.0 and len(layers) >= 2:
            sorted_layers = sorted(layers, key=lambda x: x.strength)
            weakest = sorted_layers[0]
            strongest = sorted_layers[-1]
            signals.append({
                "type": "merge",
                "source_id": weakest.layer_id,
                "target_id": strongest.layer_id,
            })

        # 3. Ambiguity/drift – strengthen dominant register, weaken outliers.
        if metrics.register_ambiguity > 0.0 and layers:
            registers = [l.register for l in layers]
            dominant = max(set(registers), key=registers.count)
            for l in layers:
                if l.register == dominant:
                    signals.append({
                        "type": "strengthen_register",
                        "layer_id": l.layer_id,
                        "delta": +0.1,
                    })
                else:
                    signals.append({
                        "type": "weaken_register",
                        "layer_id": l.layer_id,
                        "delta": -0.05,
                    })

        return signals


# ---------------------------------------------------------------------------
# 20.33_cil_requirements – CIL (intake packet + register_hint)
# ---------------------------------------------------------------------------

@dataclass
class CILIntakePacket:
    identity_layer_ids: List[str]
    stability_score: float
    ambiguity_score: float
    register_hint: str
    snapshot_hash: str


class CIL:
    """
    20.33 – CIL: read-only intake from COB snapshot.
    Emits advisory packet including register_hint.
    """

    @staticmethod
    def build_intake(snapshot: COBSnapshot, metrics: CSTMetrics) -> CILIntakePacket:
        layers = snapshot.layers
        ids = [l.layer_id for l in layers]

        # Stability: inverse of identity_drift (simplified).
        stability = max(0.0, 1.0 - min(1.0, metrics.identity_drift))

        # Ambiguity: use register_ambiguity.
        ambiguity = metrics.register_ambiguity

        # Register hint: dominant register.
        if layers:
            registers = [l.register for l in layers]
            dominant = max(set(registers), key=registers.count)
        else:
            dominant = "neutral"

        return CILIntakePacket(
            identity_layer_ids=ids,
            stability_score=stability,
            ambiguity_score=ambiguity,
            register_hint=dominant,
            snapshot_hash=snapshot.history_hash,
        )


# ---------------------------------------------------------------------------
# Testbench – pipeline simulation
# ---------------------------------------------------------------------------

class CExTestbench:
    """
    End-to-end simulator for:
    SSRGn → COB → CST → COB → CIL

    Focus:
    - determinism
    - stability
    - register/subculture behavior
    """

    def __init__(self):
        self.ssrgn = SSRGn()
        self.cob = COB()
        self.cst = CST()
        self.cil = CIL()

    def run_sequence(self, tp_sequence: List[TPCommitted]) -> List[CILIntakePacket]:
        """
        Run a sequence of committed TP through the pipeline.
        Returns CIL intake packets per cycle.
        """
        intake_packets: List[CILIntakePacket] = []

        for tp in tp_sequence:
            # 1. SSRGn
            ssr = self.ssrgn.freeze(tp)

            # 2. COB ingest
            self.cob.ingest_ssr(ssr)

            # 3. Snapshot
            snapshot = self.cob.snapshot()

            # 4. CST integrate + signals
            metrics = self.cst.integrate(snapshot)
            signals = self.cst.emit_signals(snapshot, metrics)

            # 5. COB apply signals
            self.cob.apply_cst_signals(signals)

            # 6. New snapshot + CIL intake
            new_snapshot = self.cob.snapshot()
            new_metrics = self.cst.integrate(new_snapshot)
            intake = self.cil.build_intake(new_snapshot, new_metrics)
            intake_packets.append(intake)

        return intake_packets

    def replay_sequence(self, tp_sequence: List[TPCommitted]) -> Tuple[List[CILIntakePacket], List[CILIntakePacket]]:
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
    def compare_intake_sequences(a: List[CILIntakePacket], b: List[CILIntakePacket]) -> bool:
        if len(a) != len(b):
            return False
        for p1, p2 in zip(a, b):
            if (
                p1.identity_layer_ids != p2.identity_layer_ids or
                abs(p1.stability_score - p2.stability_score) > 1e-9 or
                abs(p1.ambiguity_score - p2.ambiguity_score) > 1e-9 or
                p1.register_hint != p2.register_hint or
                p1.snapshot_hash != p2.snapshot_hash
            ):
                return False
        return True


# ---------------------------------------------------------------------------
# Example usage / basic tests
# ---------------------------------------------------------------------------

def make_example_tp_sequence() -> List[TPCommitted]:
    """
    Build a small synthetic TP sequence to exercise register/subculture behavior.
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
    packets = tb.run_sequence(seq)
    print("Single run intake packets:")
    for i, p in enumerate(packets, start=1):
        print(f"Turn {i}:")
        print(f"  identity_layer_ids: {p.identity_layer_ids}")
        print(f"  stability_score:    {p.stability_score:.3f}")
        print(f"  ambiguity_score:    {p.ambiguity_score:.3f}")
        print(f"  register_hint:      {p.register_hint}")
        print(f"  snapshot_hash:      {p.snapshot_hash}")
        print()

    # Replay determinism check
    out1, out2 = tb.replay_sequence(seq)
    deterministic = CExTestbench.compare_intake_sequences(out1, out2)
    print("Replay determinism:", deterministic)


if __name__ == "__main__":
    main()
