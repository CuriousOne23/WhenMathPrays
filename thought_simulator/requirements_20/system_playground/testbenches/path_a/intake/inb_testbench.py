"""
InB Intake Testbench — Path A
Runs: InB only
Designed to be executed by run.py
"""

import os
import yaml
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Thought Packet (TP) structure
# ---------------------------------------------------------------------------

@dataclass
class ThoughtPacket:
    raw_input: str
    messy_input_record: str = ""
    defects: list = field(default_factory=list)
    repairs: list = field(default_factory=list)
    normalized: str = ""
    metadata: dict = field(default_factory=dict)

# ---------------------------------------------------------------------------
# Import REAL InB primitive
# ---------------------------------------------------------------------------

from thought_simulator.requirements_20.system_playground.primitives.inb.inb import InB

# ---------------------------------------------------------------------------
# Testbench Loader
# ---------------------------------------------------------------------------

def load_testbench():
    yaml_path = os.path.join(
        os.path.dirname(__file__),
        "inb_testbench.yaml"
    )
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ---------------------------------------------------------------------------
# Configuration injection (required by run.py)
# ---------------------------------------------------------------------------

CONFIG = {}

def set_testbench_config(config_dict):
    global CONFIG
    CONFIG = config_dict

# ---------------------------------------------------------------------------
# Development-mode runner (no unittest)
# ---------------------------------------------------------------------------

def run_testbench():

    testbench = load_testbench()
    tests = testbench.get("tests", [])

    print(f"\nLoaded {len(tests)} InB intake test cases.\n")

    passed_count = 0
    failed_count = 0

    for test in tests:
        ...
        if all_fields_match:
            passed_count += 1
        else:
            failed_count += 1

        name = test.get("id", "unnamed")
        print(f"Running: {name} ...", end=" ")

        # Generate long input if requested
        if test.get("generate_long_input", False):
            length = test.get("long_length", 5000)
            raw_input = "A" * length
        else:
            raw_input = test["input"]

        tp = ThoughtPacket(raw_input=raw_input)

        # Execute REAL InB primitive
        tp = InB(tp)

        # Expected values
        expected_defects = test.get("expected_defects", [])
        expected_failure = test.get("expected_failure", False)

        # Checks
        defects_ok = (tp.defects == expected_defects)
        passed = defects_ok

        # ------------------------------------------------------------------
        # Requirement-aware PASS/FAIL messaging
        # ------------------------------------------------------------------
        # ------------------------------------------------------------------
        # Improved PASS/FAIL messaging
        # ------------------------------------------------------------------
        
        actual_defects = tp.defects
        
        if passed:
            if expected_failure:
                print(f"EXPECTED FAILURE — {name}")
                print(f"PASS: InB correctly detected defects {actual_defects} in input \"{raw_input}\".\n")
            else:
                if expected_defects:
                    print(f"PASS — {name}")
                    print(f"Detected expected defects {expected_defects} in input \"{raw_input}\".\n")
                else:
                    print(f"PASS — {name}")
                    print(f"No defects detected, as expected, for input \"{raw_input}\".\n")
        else:
            if expected_failure:
                print(f"UNEXPECTED PASS — {name}")
                print(f"FAIL: Expected defects {expected_defects}, but InB returned {actual_defects}.\n")
            else:
                print(f"FAIL — {name}")
                print(f"Expected defects {expected_defects}, but InB returned {actual_defects}.")
                print(f"InB failed to detect required defect(s) in input \"{raw_input}\".\n")

    # ------------------------------------------------------------
    # Summary footer
    # ------------------------------------------------------------
    print("\n============================================================")
    print("SUMMARY")
    print(f"Passed: {passed_count} / {len(tests)} tests")
    print(f"Failed: {failed_count} / {len(tests)} tests")
    print("============================================================\n")

