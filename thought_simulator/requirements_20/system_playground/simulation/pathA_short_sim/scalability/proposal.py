from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml


SUPPORTED_PROPOSAL_CLASSES = {"dictionary_entry", "association", "major", "seed"}


def _fail(message: str) -> ValueError:
    return ValueError(f"proposal_invalid: {message}")


def _as_str(value: Any) -> str:
    return str(value).strip()


def _normalize_lower(value: Any) -> str:
    return _as_str(value).lower()


def _validate_dictionary_identity(identity: Dict[str, Any]) -> Dict[str, Any]:
    scope = _normalize_lower(identity.get("scope"))
    marker = _normalize_lower(identity.get("marker"))
    major = _normalize_lower(identity.get("major"))
    if scope not in {"sentence_internal", "prior_context"}:
        raise _fail("dictionary_entry identity.scope must be sentence_internal or prior_context")
    if not marker:
        raise _fail("dictionary_entry identity.marker is required")
    if not major:
        raise _fail("dictionary_entry identity.major is required")
    return {"scope": scope, "marker": marker, "major": major}


def _validate_association_identity(identity: Dict[str, Any]) -> Dict[str, Any]:
    endpoint = _normalize_lower(identity.get("endpoint"))
    relation = _normalize_lower(identity.get("relation"))
    target = _normalize_lower(identity.get("to"))
    major = _normalize_lower(identity.get("major"))
    subcategory = _normalize_lower(identity.get("subcategory"))
    if not endpoint:
        raise _fail("association identity.endpoint is required")
    if not relation:
        raise _fail("association identity.relation is required")
    if not target:
        raise _fail("association identity.to is required")
    if not major:
        raise _fail("association identity.major is required")
    validated: Dict[str, Any] = {
        "endpoint": endpoint,
        "relation": relation,
        "to": target,
        "major": major,
    }
    if subcategory:
        validated["subcategory"] = subcategory
    return validated


def _validate_major_identity(identity: Dict[str, Any]) -> Dict[str, Any]:
    major = _normalize_lower(identity.get("major"))
    if not major:
        raise _fail("major identity.major is required")
    return {"major": major}


def _validate_seed_identity(identity: Dict[str, Any]) -> Dict[str, Any]:
    # Seed is explicitly unresolved/historical in first pass.
    key = _normalize_lower(identity.get("seed_key") or identity.get("name") or "seed")
    return {"seed_key": key or "seed"}


def _validate_item(item: Dict[str, Any], index: int) -> Dict[str, Any]:
    resource_class = _normalize_lower(item.get("resource_class"))
    if resource_class not in SUPPORTED_PROPOSAL_CLASSES:
        raise _fail(f"items[{index}] resource_class unsupported: {resource_class}")

    identity = item.get("identity")
    delta = item.get("delta")
    provenance = item.get("provenance")
    if not isinstance(identity, dict):
        raise _fail(f"items[{index}] identity must be an object")
    if not isinstance(delta, dict):
        raise _fail(f"items[{index}] delta must be an object")
    if not isinstance(provenance, dict):
        raise _fail(f"items[{index}] provenance must be an object")

    if resource_class == "dictionary_entry":
        validated_identity = _validate_dictionary_identity(identity)
    elif resource_class == "association":
        validated_identity = _validate_association_identity(identity)
    elif resource_class == "major":
        validated_identity = _validate_major_identity(identity)
    else:
        validated_identity = _validate_seed_identity(identity)

    return {
        "item_id": _as_str(item.get("item_id")) or f"item-{index + 1}",
        "resource_class": resource_class,
        "identity": validated_identity,
        "delta": delta,
        "provenance": provenance,
        "advisory_intent": item.get("advisory_intent"),
        "expected_surfaces": item.get("expected_surfaces"),
    }


def load_proposal(path: str) -> Dict[str, Any]:
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise _fail("top-level payload must be an object")

    proposal_id = _as_str(payload.get("proposal_id"))
    if not proposal_id:
        raise _fail("proposal_id is required")

    items = payload.get("items")
    if not isinstance(items, list) or not items:
        raise _fail("items must be a non-empty array")

    validated_items: List[Dict[str, Any]] = []
    for idx, entry in enumerate(items):
        if not isinstance(entry, dict):
            raise _fail(f"items[{idx}] must be an object")
        validated_items.append(_validate_item(entry, idx))

    return {
        "proposal_id": proposal_id,
        "items": validated_items,
        "advisory_intent": payload.get("advisory_intent"),
    }

