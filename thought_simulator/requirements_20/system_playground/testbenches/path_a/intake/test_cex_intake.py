"""
Intake Testbench — CEx (Context Extractor)

This testbench validates the interaction between:
    CIL → CEx → CE

It ensures:
- CEx correctly consumes real CILIntakePackets
- identity selection is deterministic
- ordering metrics are reflected
- stability indicators are reflected
- referent mappings are preserved
- continuity_status is correct
- provenance is correct
- CE envelope is structurally valid
"""

import unittest

# Lean CEx implementation & Real CIL implementation
from thought_simulator.requirements_20.system_playground.simulation.path_a.lean.lean_path_a.lean_nodes.cex.cex import CEx
from thought_simulator.requirements_20.system_playground.context.context.cil.cil import CIL, IdentityObject


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_identity_objects():
    """Create multiple identity-layer objects for CIL."""
    obj1 = IdentityObject(
        id="layer_1",
        referent_map={"entity": "Alice"},
        anchors=["t0"],
        lineage={"stability": 0.9},
        ambiguity={"certainty": 0.8, "ambiguity": 0.2},
        stability_metrics={"drift": 0.0, "collapse": 0.0},
        ordering_metrics={"recency": 10, "frequency": 3, "density": 2},
    )

    obj2 = IdentityObject(
        id="layer_2",
        referent_map={"entity": "Bob"},
        anchors=["t1"],
        lineage={"stability": 0.7},
        ambiguity={"certainty": 0.6, "ambiguity": 0.4},
        stability_metrics={"drift": 0.1, "collapse": 0.0},
        ordering_metrics={"recency": 5, "frequency": 2, "density": 1},
    )

    return [obj1, obj2]


def make_cil_packet(turn_index=1, new_context_required=False):
    """Generate a real CILIntakePacket using the CIL implementation."""
    cil = CIL()

    core_signals = {
        "drift": {},
        "metadata": {"new_context_required": new_context_required},
    }

    ms_signals = {}

    packet = cil.run(
        cob_objects=make_identity_objects(),
        core_signals=core_signals,
        ms_signals=ms_signals,
        turn_index=turn_index,
    )

    return packet


# ---------------------------------------------------------------------------
# Testbench
# ---------------------------------------------------------------------------

class TestCExIntake(unittest.TestCase):

    def setUp(self):
        self.cex = CEx()

    # -------------------------------------------------------------------
    # 1. CEx must accept real CILIntakePackets
    # -------------------------------------------------------------------
    def test_accepts_cil_packet(self):
        packet = make_cil_packet()
        try:
            ce = self.cex.run(packet)
        except Exception as e:
            self.fail(f"CEx rejected a valid CILIntakePacket: {e}")

    # -------------------------------------------------------------------
    # 2. Identity selection must be deterministic
    # -------------------------------------------------------------------
    def test_identity_selection(self):
        packet = make_cil_packet()
        ce = self.cex.run(packet)

        primary_id = ce["context_fields"]["identity_layer_context"]["primary_layer_id"]
        self.assertEqual(primary_id, "layer_1")

    # -------------------------------------------------------------------
    # 3. Ordering metrics must be reflected
    # -------------------------------------------------------------------
    def test_ordering_metrics_reflection(self):
        packet = make_cil_packet()
        ce = self.cex.run(packet)

        ordering = ce["context_fields"]["identity_layer_context"]["ordering_metrics"]
        self.assertEqual(ordering["recency"], 10)
        self.assertEqual(ordering["frequency"], 3)
        self.assertEqual(ordering["density"], 2)

    # -------------------------------------------------------------------
    # 4. Stability indicators must be reflected
    # -------------------------------------------------------------------
    def test_stability_reflection(self):
        packet = make_cil_packet()
        ce = self.cex.run(packet)

        stability = ce["context_fields"]["structural_hints"]["stability_summary"]
        self.assertIn("has_drift", stability)
        self.assertIn("has_collapse", stability)

    # -------------------------------------------------------------------
    # 5. Referent mapping must be preserved
    # -------------------------------------------------------------------
    def test_referent_mapping(self):
        packet = make_cil_packet()
        ce = self.cex.run(packet)

        referents = ce["context_fields"]["referent_mapping"]
        self.assertEqual(referents.get("entity"), "Alice")

    # -------------------------------------------------------------------
    # 6. continuity_status must reflect new_context_required
    # -------------------------------------------------------------------
    def test_continuity_status(self):
        packet = make_cil_packet(new_context_required=True)
        ce = self.cex.run(packet)

        self.assertEqual(ce["continuity_status"], "reset_required")

    # -------------------------------------------------------------------
    # 7. Provenance must include turn_index
    # -------------------------------------------------------------------
    def test_provenance(self):
        packet = make_cil_packet(turn_index=7)
        ce = self.cex.run(packet)

        provenance = ce["context_provenance"]
        self.assertEqual(provenance["turn_index"], 7)

    # -------------------------------------------------------------------
    # 8. Determinism: identical input → identical CE
    # -------------------------------------------------------------------
    def test_determinism(self):
        packet = make_cil_packet()
        ce1 = self.cex.run(packet)
        ce2 = self.cex.run(packet)

        self.assertEqual(ce1, ce2, "CEx is not deterministic for identical input")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
