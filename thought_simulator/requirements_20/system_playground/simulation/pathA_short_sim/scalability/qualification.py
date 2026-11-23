from __future__ import annotations

from typing import Any, Dict, List


def determine_qualification(obligations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for obligation in obligations:
        obligation_type = str(obligation.get("obligation_type", ""))
        if obligation_type == "seed_generalization_unresolved":
            state = "unresolved"
            reason = "seed expansion is historical/unresolved in first-pass scope"
        else:
            state = "unresolved"
            reason = "explicit existing qualification evidence not established for this obligation"
        results.append(
            {
                "source_item_id": obligation.get("source_item_id"),
                "obligation_type": obligation_type,
                "qualification_state": state,
                "reason": reason,
            }
        )
    return results

