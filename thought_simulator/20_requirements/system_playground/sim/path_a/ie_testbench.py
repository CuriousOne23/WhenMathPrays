"""
ie_testbench.py
TS Path A — Intake Envelope Testbench Driver
Executes: InB → IIInB → IE

- Terminal output: short PASS/FAIL summary
- Log file output: full detailed trace (ignored by .gitignore)
"""

import yaml
import os
import datetime
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Thought Packet (TP) structure
# ---------------------------------------------------------------------------

@dataclass
class ThoughtPacket:
    raw_input: str
    metadata: dict = field(default_factory=dict)
    defects: list = field(default_factory=list)
    repairs: list = field(default_factory=list)
    normalized: str = ""

# ---------------------------------------------------------------------------
# Primitive stubs (replace with real implementations later)
# ---------------------------------------------------------------------------

def InB(tp: ThoughtPacket):
    tp.metadata["inb_status"] = "accepted"
    return tp

def IIInB(tp: ThoughtPacket):
    tp.metadata["iiinb_status"] = "inspected"
    tp.defects = []  # stub: no defects detected
    return tp

def IE(tp: ThoughtPacket):
    tp.metadata["ie_status"] = "normalized"
    tp.normalized = tp.raw_input
    tp.repairs = []  # stub: no repairs applied
    return tp

# ---------------------------------------------------------------------------
# Testbench Loader
# ---------------------------------------------------------------------------

def load_testbench(yaml_path: str):
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ---------------------------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------------------------

def create_log_file():
    logs_dir = os.path.join(
        os.path.dirname(__file__),
        "../../testbenches/path_a/intake/logs"
    )
    os.makedirs(logs_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(logs_dir, f"ie_run_{timestamp}.log")

    return open(log_path, "w", encoding="utf-8")

# ---------------------------------------------------------------------------
# Test Execution
# ---------------------------------------------------------------------------

def run_test_case(test, log):
    name = test.get("id", "unnamed")

    print(f"Running: {name} ...", end=" ")

    # Generate long input if requested
    if test.get("generate_long_input", False):
        length = test.get("long_length", 5000)
        raw_input = "A" * length
    else:
        raw_input = test["input"]

    tp = ThoughtPacket(raw_input=raw_input)

    # Execute primitives
    tp = InB(tp)
    tp = IIInB(tp)
    tp = IE(tp)

    # Expected values
    expected_inb_status = test.get("expected_inb_status", "accepted")
    expected_iiinb_status = test.get("expected_iiinb_status", "inspected")
    expected_ie_status = test.get("expected_ie_status", "normalized")
    expected_repairs = test.get("expected_repairs", [])
    expected_normalized = test.get("expected_normalized", tp.raw_input)

    # Checks
    inb_ok = (tp.metadata.get("inb_status") == expected_inb_status)
    iiinb_ok = (tp.metadata.get("iiinb_status") == expected_iiinb_status)
    ie_ok = (tp.metadata.get("ie_status") == expected_ie_status)
    repairs_ok = (tp.repairs == expected_repairs)
    normalized_ok = (tp.normalized == expected_normalized)

    passed = inb_ok and iiinb_ok and ie_ok and repairs_ok and normalized_ok

    # Terminal output (short)
    print("PASS" if passed else "FAIL")

    # Log file output (full detail)
    log.write(f"\n=== Test Case: {name} ===\n")
    log.write(f"Input: {tp.raw_input}\n")
    log.write(f"Normalized: {tp.normalized}\n")
    log.write(f"Repairs: {tp.repairs}\n")
    log.write(f"Metadata: {tp.metadata}\n")
    log.write(f"Expected InB status: {expected_inb_status}\n")
    log.write(f"Expected IIInB status: {expected_iiinb_status}\n")
    log.write(f"Expected IE status: {expected_ie_status}\n")
    log.write(f"Expected repairs: {expected_repairs}\n")
    log.write(f"Expected normalized: {expected_normalized}\n")
    log.write(f"Result: {'PASS' if passed else 'FAIL'}\n")

# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def main():
    yaml_path = os.path.join(
        os.path.dirname(__file__),
        "../../testbenches/path_a/intake/ie_testbench.yaml"
    )

    testbench = load_testbench(yaml_path)
    tests = testbench.get("tests", [])

    print(f"Loaded {len(tests)} test cases.")
    print("Starting InB → IIInB → IE testbench...\n")

    log = create_log_file()

    for test in tests:
        run_test_case(test, log)

    log.close()

    # Show full log path in terminal
    print("\nAll tests complete.")
    print(f"Log file written to:\n  {os.path.abspath(log.name)}")
    print("Full results written to log file (ignored by git).")

if __name__ == "__main__":
    main()
