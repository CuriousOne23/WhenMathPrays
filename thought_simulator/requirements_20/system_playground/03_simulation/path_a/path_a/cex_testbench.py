"""
cex_testbench.py — Modern CEx Determinism & Continuity Testbench
Aligned with:
  - 20.107_cex_extract.md
  - 20.108_ce_envelope.md
  - 20.32_cob_requirements.md
  - 20.32.010_cst_requirements.md
  - 20.33_cil_requirements.md
  - Updated Path-A pipeline (InB → IIInB → IE → CEx → CE → ISc → TPU)
"""

import unittest
from typing import List, Dict, Any

from cex_extract import cex_extract
from ce_envelope import build_ce
from fixtures import (
    make_ie,
    make_cob_snapshot,
    make_ordering_metrics,
)


class TestCEx(unittest.TestCase):

    # -------------------------------------------------------------
    # 1. Identity-layer selection determinism
    # -------------------------------------------------------------
    def test_identity_layer_selection_deterministic(self):
        ie = make_ie("User asked about the weather in Phoenix.")
        cob = make_cob_snapshot(
            layers=["weather", "sports"],
            continuity={"weather": 0.92, "sports": 0.10}
        )
        ordering = make_ordering_metrics()

        ce1 = build_ce(cex_extract(ie, cob, ordering))
        ce2 = build_ce(cex_extract(ie, cob, ordering))

        self.assertEqual(ce1["selected_layer"], "weather")
        self.assertEqual(ce1, ce2)  # replay determinism

    # -------------------------------------------------------------
    # 2. Continuity vs override
    # -------------------------------------------------------------
    def test_continuity_override(self):
        ie = make_ie("Switch topic to basketball.")
        cob = make_cob_snapshot(
            layers=["weather", "sports"],
            continuity={"weather": 0.91, "sports": 0.12},
            override_signal="sports"
        )
        ordering = make_ordering_metrics()

        ce = build_ce(cex_extract(ie, cob, ordering))
        self.assertEqual(ce["selected_layer"], "sports")
        self.assertEqual(ce["continuity_status"], "override")

    # -------------------------------------------------------------
    # 3. Ambiguity detection
    # -------------------------------------------------------------
    def test_ambiguity_detection(self):
        ie = make_ie("He said it was fine.")
        cob = make_cob_snapshot(
            layers=["person_a", "person_b"],
            referent_ambiguity=True
        )
        ordering = make_ordering_metrics()

        ce = build_ce(cex_extract(ie, cob, ordering))
        self.assertTrue(ce["ambiguity_flag"])
        self.assertEqual(ce["fallback_reason"], "referent_ambiguity")

    # -------------------------------------------------------------
    # 4. Collapse fallback
    # -------------------------------------------------------------
    def test_collapse_fallback(self):
        ie = make_ie("Continue.")
        cob = make_cob_snapshot(
            layers=["topic_a"],
            collapse_flag=True
        )
        ordering = make_ordering_metrics()

        ce = build_ce(cex_extract(ie, cob, ordering))
        self.assertEqual(ce["fallback_reason"], "collapse")
        self.assertEqual(ce["selected_layer"], "fallback")

    # -------------------------------------------------------------
    # 5. Ordering metric integration
    # -------------------------------------------------------------
    def test_ordering_metric_integration(self):
        ie = make_ie("Tell me more.")
        cob = make_cob_snapshot(
            layers=["topic_a", "topic_b"],
            continuity={"topic_a": 0.51, "topic_b": 0.49}
        )
        ordering = make_ordering_metrics(
            ordering_preference="topic_b"
        )

        ce = build_ce(cex_extract(ie, cob, ordering))
        self.assertEqual(ce["selected_layer"], "topic_b")
        self.assertEqual(ce["ordering_used"], True)

    # -------------------------------------------------------------
    # 6. CE schema validation
    # -------------------------------------------------------------
    def test_ce_schema(self):
        ie = make_ie("What time is it?")
        cob = make_cob_snapshot(layers=["time"])
        ordering = make_ordering_metrics()

        ce = build_ce(cex_extract(ie, cob, ordering))

        required_fields = [
            "selected_layer",
            "continuity_status",
            "fallback_reason",
            "ambiguity_flag",
            "collapse_flag",
            "ordering_used",
            "normalized_tokens",
            "metadata"
        ]

        for field in required_fields:
            self.assertIn(field, ce)

    # -------------------------------------------------------------
    # 7. Replay determinism (1000 iterations)
    # -------------------------------------------------------------
    def test_replay_determinism(self):
        ie = make_ie("Where is the nearest store?")
        cob = make_cob_snapshot(layers=["location"])
        ordering = make_ordering_metrics()

        ce0 = build_ce(cex_extract(ie, cob, ordering))

        for _ in range(1000):
            ceN = build_ce(cex_extract(ie, cob, ordering))
            self.assertEqual(ceN, ce0)


if __name__ == "__main__":
    unittest.main()
