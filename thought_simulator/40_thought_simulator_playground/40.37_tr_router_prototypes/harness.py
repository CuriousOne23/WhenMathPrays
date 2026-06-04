"""
40.37 Thought Router Harness
Deterministic test harness for the TR prototype.
Now includes ΔH% validation.
"""

import json
from datetime import datetime
from prototype import create_router


def run_harness() -> dict:
    """Run verification scenarios and return results."""
    
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
        }
    ]
    
    results = []
    
    for case in test_cases:
        output = router.route(case["input"])
        route_passed = output.get("route") == case["expected_route"]
        delta_h_passed = abs(output.get("delta_h", 0) - case["expected_delta_h"]) < 0.001
        
        results.append({
            "test_id": case["id"],
            "input": case["input"],
            "output": output,
            "expected_route": case["expected_route"],
            "expected_delta_h": case["expected_delta_h"],
            "route_passed": route_passed,
            "delta_h_passed": delta_h_passed,
            "overall_passed": route_passed and delta_h_passed
        })
    
    return {
        "run_id": "tr_verification_run_2026-06-03",
        "timestamp": datetime.utcnow().isoformat(),
        "prototype_version": "0.1",
        "total_tests": len(test_cases),
        "passed_tests": sum(1 for r in results if r["overall_passed"]),
        "results": results
    }


if __name__ == "__main__":
    artifact = run_harness()
    
    # Save JSON artifact
    with open("tr_verification_run_2026-06-03.json", "w") as f:
        json.dump(artifact, f, indent=2)
    
    print("Harness completed. Artifact generated: tr_verification_run_2026-06-03.json")
    print(f"Tests passed: {artifact['passed_tests']}/{artifact['total_tests']}")