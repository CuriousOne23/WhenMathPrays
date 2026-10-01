import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

from idob import imperative, legacy
from idob.legacy import (
    legacy_monolith,
)
from idob.object import IdOBObject
from idob.psc import evaluate_psc, load_psc_defaults


ROOT_DIR = Path(__file__).resolve().parents[1]
SUPPORT_DIR = ROOT_DIR / "support"
SCHEMA_PATH = SUPPORT_DIR / "idob_schemas" / "idob_object.v1.schema.json"
PSC_DEFAULTS_PATH = SUPPORT_DIR / "idob_schemas" / "idob_psc_defaults.yaml"
OBJECTS_DIR = SUPPORT_DIR / "idob_objects"


APPLY_LOOKUP = {
    "idob.legacy:_copular_state_apply": legacy._copular_state_apply,
    "idob.legacy:_locative_apply": legacy._locative_apply,
    "idob.legacy:_mixed_descriptive_apply": legacy._mixed_descriptive_apply,
    "idob.legacy:_interrogative_wh_apply": legacy._interrogative_wh_apply,
    "idob.legacy:_interrogative_polar_apply": legacy._interrogative_polar_apply,
    "idob.legacy:_agent_action_apply": legacy._agent_action_apply,
    "idob.legacy:_modifier_resolution_apply": legacy._modifier_resolution_apply,
    "idob.legacy:_residual_identity_apply": legacy._residual_identity_apply,
    "idob.imperative:_imperative_apply": imperative._imperative_apply,
}


def _load_schema(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_valid_object_schema_shape(spec: Dict[str, Any], schema: Dict[str, Any]) -> None:
    required = set(schema.get("required", []))
    missing = sorted(field for field in required if field not in spec)
    if missing:
        raise ValueError(f"Invalid IdOB object spec {spec.get('name', '<unknown>')}: missing required keys {missing}")

    schema_ref = spec.get("schema_ref")
    if schema_ref != "idob_object.v1":
        raise ValueError(f"Invalid IdOB object spec {spec.get('name', '<unknown>')}: schema_ref must be idob_object.v1")

    behavior = spec.get("behavior", {})
    apply_symbol = behavior.get("apply")
    if apply_symbol not in APPLY_LOOKUP:
        raise ValueError(f"Unknown behavior.apply symbol {apply_symbol} for IdOB object {spec.get('name', '<unknown>')}")


def _load_object_specs(objects_dir: Path, schema: Dict[str, Any]) -> List[Tuple[Path, Dict[str, Any]]]:
    specs: List[Tuple[Path, Dict[str, Any]]] = []
    for path in sorted(objects_dir.glob("*.yaml")):
        with path.open("r", encoding="utf-8") as handle:
            spec = yaml.safe_load(handle) or {}
        if not isinstance(spec, dict):
            raise ValueError(f"Invalid IdOB object spec at {path}: expected mapping")
        _ensure_valid_object_schema_shape(spec, schema)
        specs.append((path, spec))
    return specs


def _activation_for_name(name: str):
    mapping = {
        "copular_state": legacy.copular_state.activate,
        "locative": legacy.locative.activate,
        "mixed_descriptive": legacy.mixed_descriptive.activate,
        "interrogative_wh": legacy.interrogative_wh.activate,
        "interrogative_polar": legacy.interrogative_polar.activate,
        "agent_action": legacy.agent_action.activate,
        "modifier_resolution": legacy.modifier_resolution.activate,
        "residual_identity": legacy.residual_identity.activate,
        "imperative": imperative._imperative_activate,
    }
    if name not in mapping:
        raise ValueError(f"No activation binding available for IdOB object {name}")
    return mapping[name]
