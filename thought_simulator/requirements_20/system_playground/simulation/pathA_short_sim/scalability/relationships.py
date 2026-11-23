from __future__ import annotations

from typing import Any, Dict, List, Tuple


def _dict_classification(item: Dict[str, Any], discovered: Dict[str, Any]) -> Tuple[str, str]:
    identity = item["identity"]
    scope = identity["scope"]
    marker = identity["marker"]
    major = identity["major"]

    cues = (discovered.get("category_cues", {}) or {}).get(scope, {})
    if not isinstance(cues, dict):
        return "missing", f"scope {scope} unavailable in established dictionary cues"

    existing_majors = cues.get(marker, [])
    if not isinstance(existing_majors, list):
        existing_majors = []
    normalized = [str(value).strip().lower() for value in existing_majors]
    if major in normalized:
        return "already_defined", "marker-major mapping already exists in established dictionary cue map"
    if marker in cues:
        return "extension_of", "marker exists in established dictionary cue map; proposed major extends mapping"
    return "additional_to", "marker is absent in established dictionary cue map"


def _association_identity_key(identity: Dict[str, Any]) -> Tuple[str, str, str, str, str]:
    return (
        identity.get("endpoint", ""),
        identity.get("relation", ""),
        identity.get("to", ""),
        identity.get("major", ""),
        identity.get("subcategory", ""),
    )


def _assoc_key_from_existing(endpoint: str, association: Dict[str, Any]) -> Tuple[str, str, str, str, str]:
    return (
        endpoint,
        str(association.get("relation", "")).strip().lower(),
        str(association.get("to", "")).strip().lower(),
        str(association.get("major", "")).strip().lower(),
        str(association.get("subcategory", "")).strip().lower(),
    )


def _association_classification(item: Dict[str, Any], discovered: Dict[str, Any]) -> Tuple[str, str]:
    identity = item["identity"]
    endpoint = identity["endpoint"]
    known = discovered.get("associations", {}).get(endpoint, [])
    if not isinstance(known, list):
        known = []

    wanted = _association_identity_key(identity)
    existing_keys = {_assoc_key_from_existing(endpoint, assoc) for assoc in known if isinstance(assoc, dict)}
    if wanted in existing_keys:
        return "already_defined", "association tuple already exists for endpoint"
    if known:
        return "extension_of", "endpoint exists; proposed tuple extends endpoint association set"
    return "additional_to", "endpoint association set does not exist in established environment"


def _major_classification(item: Dict[str, Any], discovered: Dict[str, Any]) -> Tuple[str, str]:
    major = item["identity"]["major"]
    majors = set(discovered.get("majors", []))
    active = set(discovered.get("active_space", []))
    add_active = bool((item.get("delta", {}) or {}).get("add_to_active_space"))

    if major in majors and (major in active or not add_active):
        return "already_defined", "major already present in established major inventory"
    if major in majors and add_active and major not in active:
        return "extension_of", "major exists; proposal extends active-space eligibility"
    return "additional_to", "major absent from established major inventory"


def classify_item(item: Dict[str, Any], discovered: Dict[str, Any]) -> Dict[str, Any]:
    resource_class = item["resource_class"]
    if resource_class == "dictionary_entry":
        classification, reason = _dict_classification(item, discovered)
    elif resource_class == "association":
        classification, reason = _association_classification(item, discovered)
    elif resource_class == "major":
        classification, reason = _major_classification(item, discovered)
    else:
        classification = "unresolved"
        reason = "seed is historical/unresolved for generalized expansion in first pass"

    return {
        "item_id": item["item_id"],
        "resource_class": resource_class,
        "identity": item["identity"],
        "classification": classification,
        "reason": reason,
    }


def classify_items(items: List[Dict[str, Any]], discovered: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [classify_item(item, discovered) for item in items]

