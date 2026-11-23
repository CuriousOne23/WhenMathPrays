from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml

from s2m.legitimate import LICENSED_EXTENSIONS
from s2m.loader import load_active_space, load_endpoint_associations, load_majors


def _root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_category_cues() -> Dict[str, Dict[str, List[str]]]:
    path = _root() / "support" / "dictionaries" / "category_cues.yaml"
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    data = payload.get("category_cues", {})
    if not isinstance(data, dict):
        return {"sentence_internal": {}, "prior_context": {}}
    sentence = data.get("sentence_internal", {})
    prior = data.get("prior_context", {})
    return {
        "sentence_internal": sentence if isinstance(sentence, dict) else {},
        "prior_context": prior if isinstance(prior, dict) else {},
    }


def _discover_associations() -> Dict[str, List[Dict[str, str]]]:
    associations_dir = _root() / "s2m" / "data" / "associations"
    discovered: Dict[str, List[Dict[str, str]]] = {}
    if not associations_dir.exists():
        return discovered
    for path in sorted(associations_dir.glob("*.yaml")):
        endpoint = path.stem.strip().lower()
        discovered[endpoint] = load_endpoint_associations(endpoint)
    return discovered


def discover_environment() -> Dict[str, Any]:
    return {
        "category_cues": _load_category_cues(),
        "majors": [str(value).strip().lower() for value in load_majors()],
        "active_space": [str(value).strip().lower() for value in load_active_space("default")],
        "associations": _discover_associations(),
        "licensed_extensions": dict(LICENSED_EXTENSIONS),
    }

