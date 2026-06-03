"""
40.36_gb_prototypes / harness.py

Deterministic harness for GlobalBasinPrototype.

Goal:
- Exercise positive and negative supervisory scenarios.
- Emit JSON-like records suitable for 30-layer verification capsules.
"""

import json
from typing import Any, Dict, List

from prototype import GlobalBasinPrototype, GBConfig


def make_event(
    event_type: str,
    sequence: int,
    safe_boundary: bool,
    request_class: str = "unknown",
    extra: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    event: Dict[str, Any] = {
        "event_type": event_type,
        "sequence": sequence,
        "safe_boundary": safe_boundary,
        "request_class": request_class,
        "tp_lane_state": {"stub": True},
        "mp_state": {"stub": True},
    }
    if extra:
        event.update(extra)
    return event


def run_scenarios() -> List[Dict[str, Any]]:
    gb = GlobalBasinPrototype(GBConfig())
    results: List[Dict[str, Any]] = []

    scenarios = [
        ("async_inquiry_approval", make_event("inquiry_request", 1, True)),
        ("ib_promotion_approval", make_event("ib_promotion", 2, True)),
        ("ob_decomposition_reshape", make_event("ob_decomposition", 3, True)),
        ("cop_proposal_gating", make_event("cop_proposal", 4, True)),
        ("unsafe_boundary_defer", make_event("inquiry_request", 5, False)),
        ("tcu_fallback_safemode", make_event("supervisory_signal", 100, True)),
    ]

    for scenario_name, event in scenarios:
        decision = gb.process_event(event)
        results.append(
            {
                "scenario": scenario_name,
                "event": event,
                "decision": {
                    "supervisory_action": decision.supervisory_action,
                    "action_rationale": decision.action_rationale,
                    "request_class": decision.request_class,
                    "applied_bounds": decision.applied_bounds,
                    "execution_diagnostics": decision.execution_diagnostics,
                    "supervisory_log_entry": decision.supervisory_log_entry,
                    "gb_reference": decision.gb_reference,
                },
            }
        )

    return results


def main() -> None:
    results = run_scenarios()
    # Deterministic artifact for 30-layer verification.
    print(json.dumps({"gb_verification_run": results}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

