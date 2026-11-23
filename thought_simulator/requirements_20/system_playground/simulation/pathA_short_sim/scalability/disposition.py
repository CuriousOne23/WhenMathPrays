from __future__ import annotations

from typing import Any, Dict, List


def determine_disposition(
    classifications: List[Dict[str, Any]],
    dependencies: List[Dict[str, Any]],
    qualifications: List[Dict[str, Any]],
    regression: Dict[str, Any],
) -> Dict[str, Any]:
    classification_by_item = {str(item.get("item_id")): str(item.get("classification")) for item in classifications}

    if any(value == "incompatible" for value in classification_by_item.values()):
        return {
            "disposition": "REVISE",
            "reason": "at least one proposal item is incompatible with explicit structure/contract constraints",
        }

    if any(str(item.get("resource_class")) == "seed" for item in classifications):
        return {
            "disposition": "HOLD",
            "reason": "seed expansion remains unresolved/historical in bounded first-pass scope",
        }

    if any(bool(item.get("has_missing_dependencies")) for item in dependencies):
        return {
            "disposition": "HOLD",
            "reason": "missing dependencies found for one or more proposal items",
        }

    reg_status = str(regression.get("status", "not-run"))
    if reg_status == "fail":
        return {
            "disposition": "HOLD",
            "reason": "regression checks failed; progression obligations cannot be accepted",
        }

    states = {str(item.get("qualification_state", "unresolved")) for item in qualifications}
    if "unresolved" in states:
        return {
            "disposition": "HOLD",
            "reason": "qualification coverage unresolved for one or more progression obligations",
        }
    if "unqualified" in states:
        return {
            "disposition": "RETURN_TO_CHARACTERIZATION",
            "reason": "at least one obligation is explicitly unqualified",
        }

    return {
        "disposition": "PROCEED",
        "reason": "no incompatibilities or missing dependencies; obligations are bounded and qualification states are non-blocking",
    }

