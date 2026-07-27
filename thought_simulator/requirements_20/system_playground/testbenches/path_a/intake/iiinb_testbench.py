"""
IIInB Intake Inspection Testbench — Path A
Development-mode runner compatible with run.py

Upstream rule (True-only semantics):
    • If use_inb=True  → run real InB primitive
    • If use_inb=False → use passthrough stub (IIInB receives YAML-defined input)
"""

import os
import yaml
from dataclasses import dataclass, field

# ============================================================
# Thought Packet (TP) structure
# ============================================================

@dataclass
class ThoughtPacket:
    raw_input: str
    metadata: dict = field(default_factory=dict)
    repairs: list = field(default_factory=list)
    anomalies: list = field(default_factory=list)
    tokens: list = field(default_factory=list)
    structure: dict = field(default_factory=dict)
    normalized: str = ""

# ============================================================
# Primitive imports
# ============================================================

# Real IIInB primitive
from thought_simulator.requirements_20.system_playground.primitives.iiinb.iiinb import IIInB

# Real InB primitive (used only when use_inb=True)
from thought_simulator.requirements_20.system_playground.primitives.inb.inb import InB as RealInB

# Passthrough stub for InB when use_inb=False
def InB_passthru(tp: ThoughtPacket):
    """
    Passthrough stub:
    • Does NOT modify tp
    • Does NOT set inb_status
    • Allows IIInB to receive YAML-defined input directly
    """
    return tp

# ============================================================
# Testbench Loader
# ============================================================

def load_testbench():
    yaml_path = os.path.join(
        os.path.dirname(__file__),
        "iiinb_testbench.yaml"
    )
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ============================================================
# Configuration (injected by run.py)
# ============================================================

TESTBENCH_CONFIG = {
    "use_inb": False,
    "use_iiinb": True,
    "use_ie": False,
    "tests_to_run": {}
}

def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config

# ============================================================
# Development-mode runner (called by run.py)
# ============================================================

def run_testbench():

    print("Loading IIInB testbench YAML...\n")
    testbench = load_testbench()
    tests = testbench.get("tests", [])

    selected_ids = TESTBENCH_CONFIG.get("tests_to_run", {})
    selected = [t for t in tests if selected_ids.get(t.get("id"), "No") == "Yes"]

    print(f"Selected {len(selected)} IIInB test cases.\n")

    passed_count = 0
    failed_count = 0
    
    for test in selected:
        name = test.get("id", "unnamed")
        print(f"Running: {name}")
        
        # Generate long input if requested
        if test.get("generate_long_input", False):
            length = test.get("long_length", 5000)
            raw_input = "A" * length
        else:
            raw_input = test.get("input", "")

        tp = ThoughtPacket(raw_input=raw_input)

        # ====================================================
        # Upstream primitive execution (True-only semantics)
        # ====================================================

        if TESTBENCH_CONFIG.get("use_inb", False):
            tp = RealInB(tp)
        else:
            tp = InB_passthru(tp)

        if TESTBENCH_CONFIG.get("use_iiinb", True):
            tp = IIInB(tp)

        # ====================================================
        # Expected block (YAML)
        # ====================================================

        expected = test.get("expected", {})

        expected_inb_status = expected.get("inb_status", None)
        expected_iiinb_status = expected.get("iiinb_status", "inspected")
        expected_repairs = expected.get("repair_operations", [])
        expected_anomalies = expected.get("anomaly_flags", [])
        expected_normalized = expected.get("normalized", raw_input)
        expected_tokens = expected.get("tokens", None)
        expected_structure = expected.get("structure", None)

        # ====================================================
        # Checks with detailed diagnostics
        # ====================================================

        results = []

        def check(label, actual, expected):
            if actual == expected:
                results.append(
                    f"  ✔ {label} AGREES — expected {expected!r}, got {actual!r}"
                )
                return True
            else:
                results.append(
                    f"  ✘ {label} DISAGREES — expected {expected!r}, got {actual!r}"
                )
                return False

        # InB status only checked if YAML defines it
        inb_ok = True
        if expected_inb_status is not None:
            inb_ok = check("InB status", tp.metadata.get("inb_status"), expected_inb_status)

        iiinb_ok = check("IIInB status", tp.metadata.get("iiinb_status"), expected_iiinb_status)
        repairs_ok = check("Repairs", tp.repairs, expected_repairs)
        anomalies_ok = check("Anomalies", tp.anomalies, expected_anomalies)
        normalized_ok = check("Normalized", tp.normalized, expected_normalized)

        tokens_ok = True
        if expected_tokens is not None:
            tokens_ok = check("Tokens", tp.tokens, expected_tokens)

        structure_ok = True
        if expected_structure is not None:
            structure_ok = check("Structure", tp.structure, expected_structure)

        passed = (
            inb_ok and iiinb_ok and repairs_ok and anomalies_ok and
            normalized_ok and tokens_ok and structure_ok
        )

        # ====================================================
        # Print detailed results
        # ====================================================

        if passed:
            print("PASS — All fields agree with expected values:")
            passed_count += 1
        else:
            print("FAIL — One or more fields disagree with expected values:")
            failed_count += 1
        
        for line in results:
            print(line)

        print("")  # blank line between tests

    # ------------------------------------------------------------
    # Summary footer
    # ------------------------------------------------------------
    print("\n============================================================")
    print("SUMMARY")
    print(f"Passed: {passed_count} / {len(selected)} tests")
    print(f"Failed: {failed_count} / {len(selected)} tests")
    print("============================================================\n")


