from pathlib import Path
from typing import Any, Dict, List

import yaml


DATA_DIR = Path(__file__).resolve().parent / "data"


def _load_yaml(file_path: Path) -> Any:
    if not file_path.exists():
        return {}
    with file_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_majors() -> List[str]:
    payload = _load_yaml(DATA_DIR / "majors.yaml")
    majors = payload.get("majors", []) if isinstance(payload, dict) else []
    if not isinstance(majors, list):
        return []
    return [str(major) for major in majors if str(major).strip()]


def load_active_space(space_name: str = "default") -> List[str]:
    payload = _load_yaml(DATA_DIR / "spaces" / f"{space_name}.yaml")
    active = payload.get("active_space", []) if isinstance(payload, dict) else []
    if not isinstance(active, list):
        return []
    return [str(major) for major in active if str(major).strip()]


def load_endpoint_associations(endpoint: str) -> List[Dict[str, str]]:
    payload = _load_yaml(DATA_DIR / "associations" / f"{endpoint}.yaml")
    entries = payload.get("associations", []) if isinstance(payload, dict) else []
    if not isinstance(entries, list):
        return []

    associations: List[Dict[str, str]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        relation = str(entry.get("relation", "")).strip()
        target = str(entry.get("to", "")).strip()
        major = str(entry.get("major", "")).strip()
        subcategory = str(entry.get("subcategory", "")).strip()
        if not relation or not target or not major:
            continue
        association = {"relation": relation, "to": target, "major": major}
        if subcategory:
            association["subcategory"] = subcategory
        associations.append(association)
    return associations

