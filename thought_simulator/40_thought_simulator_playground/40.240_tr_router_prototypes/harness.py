"""
40.240 Thought Router Harness
Deterministic test harness for the TR prototype.
Now includes ΔH% validation.
"""

import json
from datetime import datetime, timezone
from prototype import create_router


def run_harness(run_id: str = "tr_verification_run_2026-06-03") -> dict:
    """Run verification scenarios and return results.
    
    Supports multiple runs for determinism evidence (modeled after 40.160).
    """
    
    router = create_router()
    
    test_cases = [
        {
            "id": "TC001",
            "input": {"content": "Calculate the integral of x^2"},
            "expected_route": "math_basin",
            "expected_delta_h": 0.15
        },
        {
            "id": "TC002",
            "input": {"content": "Think about the meaning of existence"},
            "expected_route": "thought_basin",
            "expected_delta_h": 0.08
        },
        {
            "id": "TC003",
            "input": {"content": "What is the weather like?"},
            "expected_route": "general_basin",
            "expected_delta_h": 0.05
        },
        {
            "id": "TC004",
            "input": {"content": "Explain quantum entanglement mathematically"},
            "expected_route": "math_basin",
            "expected_delta_h": 0.15
        },
        {
            "id": "TC005",
            "input": {},
            "expected_route": "error",
            "expected_reason": "invalid_input",
            "is_error_case": True
        },
        {
            "id": "TC006",
            "input": None,
            "expected_route": "error",
            "expected_reason": "invalid_input",
            "is_error_case": True
        },
    ]

    results = []

    for case in test_cases:
        raw_input = case["input"]
        output = router.route(raw_input if raw_input is not None else {})

        if case.get("is_error_case"):
            route_passed = output.get("route") == case["expected_route"]
            reason_passed = output.get("reason") == case["expected_reason"]
            delta_h_passed = "delta_h" not in output
            overall_passed = route_passed and reason_passed and delta_h_passed
            expected_delta_h = None
        else:
            route_passed = output.get("route") == case["expected_route"]
            delta_h_passed = abs(output.get("delta_h", 0) - case["expected_delta_h"]) < 0.001
            reason_passed = True
            overall_passed = route_passed and delta_h_passed
            expected_delta_h = case["expected_delta_h"]

        results.append({
            "test_id": case["id"],
            "input": raw_input,
            "output": output,
            "expected_route": case["expected_route"],
            "expected_delta_h": expected_delta_h,
            "route_passed": route_passed,
            "delta_h_passed": delta_h_passed if not case.get("is_error_case") else True,
            "reason_passed": reason_passed,
            "overall_passed": overall_passed
        })
    
    return {
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prototype_version": "0.1",
        "evidence_scope": "proxy_only",
        "hlr_proven": ["HLR-20.437-001", "HLR-20.437-002", "HLR-20.437-003"],
        "hlr_deferred": ["HLR-20.037-049", "HLR-20.037-050", "HLR-20.037-051"],
        "phase": "B",
        "total_tests": len(test_cases),
        "passed_tests": sum(1 for r in results if r["overall_passed"]),
        "results": results
    }


if __name__ == "__main__":
    import os
    os.makedirs("artifacts", exist_ok=True)
    
    # Run multiple times for determinism evidence (aligned with 40.160 style)
    for run_label in ["run1", "run2", "run3"]:
        run_id = f"tr_verification_{run_label}_2026-06-03"
        artifact = run_harness(run_id=run_id)
        
        artifact_path = os.path.join("artifacts", f"tr_verification_{run_label}_2026-06-03.json")
        with open(artifact_path, "w") as f:
            json.dump(artifact, f, indent=2)
        
        print(f"Run {run_label} completed. Artifact: {artifact_path}")
        print(f"  Tests passed: {artifact['passed_tests']}/{artifact['total_tests']}")
    
    print("\nAll runs complete. Artifacts in artifacts/")