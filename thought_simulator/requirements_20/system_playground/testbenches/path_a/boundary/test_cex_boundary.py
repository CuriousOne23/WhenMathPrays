"""
Boundary Testbench — CEx (Context Extractor)

This testbench validates the CEx primitive against its boundary-object
specification defined in:

    02_primitives/reference_objects/path_a/boundary/cex_reference.yaml

It ensures:
- admissible input type is CILIntakePacket
- CE envelope structure matches the YAML contract
- required CE fields exist
- forbidden fields do NOT appear
- determinism: identical input → identical CE
"""

import os
import yaml
import unittest

# Import lean CEx implementation
from thought_simulator.requirements_20.system_playground.simulation.path_a.lean.lean_path_a.lean_nodes.cex.cex import CEx

# Import CILIntakePacket generator (lean CIL)
from thought_simulator.requirements_20.system_playground.context.context.cil.cil import CIL, IdentityObject


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_cex_reference():
    """Load cex_reference.yaml for structural validation."""
    ref_path = os.path.join(
        os.path.dirname(__file__),
        "../../../../primitives/reference_objects/path_a/boundary/cex_reference.yaml"
    )
    with open(ref_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def make_synthetic_cil_packet():
    """Create a minimal deterministic CILIntakePacket using lean CIL."""
    cil = CIL()

    # Create synthetic identity objects
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

    # Run CIL to produce intake packet
    packet = cil.run(
        cob_objects=[obj1, obj2],
        core_signals={"drift": {}, "metadata": {"new_context_required": False}},
        ms_signals={},
        turn_index=1,
    )

    return packet


# ---------------------------------------------------------------------------
# Testbench
# ---------------------------------------------------------------------------

class TestCExBoundary(unittest.TestCase):

    def setUp(self):
        self.cex = CEx()
        self.cex_ref = load_cex_reference()

    # -------------------------------------------------------------------
    # 1. Test admissible input type
    # -------------------------------------------------------------------
    def test_admissible_input(self):
        packet = make_synthetic_cil_packet()
        try:
            ce = self.cex.run(packet)
        except Exception as e:
            self.fail(f"CEx rejected valid CILIntakePacket: {e}")

    # -------------------------------------------------------------------
    # 2. Test CE envelope structure
    # -------------------------------------------------------------------
    def test_ce_structure(self):
        packet = make_synthetic_cil_packet()
        ce = self.cex.run(packet)

        # Required top-level fields
        required_fields = [
            "relevance_flags",
            "copy_forward_flags",
            "reset_flags",
            "context_fields",
            "context_provenance",
            "extraction_audit",
            "continuity_status",
        ]

        for field in required_fields:
            self.assertIn(field, ce, f"Missing CE field: {field}")

        # Required context_fields substructure
        cf = ce["context_fields"]
        self.assertIn("identity_layer_context", cf)
        self.assertIn("structural_hints", cf)
        self.assertIn("referent_mapping", cf)
        self.assertIn("next_context_fields", cf)

    # -------------------------------------------------------------------
    # 3. Test determinism
    # -------------------------------------------------------------------
    def test_determinism(self):
        packet = make_synthetic_cil_packet()
        ce1 = self.cex.run(packet)
        ce2 = self.cex.run(packet)

        self.assertEqual(ce1, ce2, "CEx is not deterministic for identical input")

    # -------------------------------------------------------------------
    # 4. Test forbidden fields do not appear
    # -------------------------------------------------------------------
    def test_forbidden_fields(self):
        packet = make_synthetic_cil_packet()
        ce = self.cex.run(packet)

        forbidden = [
            "semantic_core",
            "routing_metadata",
            "token_surface",
            "token_base",
            "token_expression",
            "token_intent",
        ]

        for field in forbidden:
            self.assertNotIn(field, ce, f"Forbidden field present: {field}")

    # -------------------------------------------------------------------
    # 5. Test continuity_status correctness
    # -------------------------------------------------------------------
    def test_continuity_status(self):
        packet = make_synthetic_cil_packet()
        ce = self.cex.run(packet)

        self.assertIn(
            ce["continuity_status"],
            ["stable", "reset_required"],
            "Invalid continuity_status value",
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()

