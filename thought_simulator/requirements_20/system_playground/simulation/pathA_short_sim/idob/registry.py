import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

from idob import legacy
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
    }
    if name not in mapping:
        raise ValueError(f"No activation binding available for IdOB object {name}")
    return mapping[name]


def _build_registry_from_specs(specs: List[Tuple[Path, Dict[str, Any]]]) -> List[IdOBObject]:
    registry_items: List[IdOBObject] = []
    for _path, spec in specs:
        apply_symbol = str(spec["behavior"]["apply"])
        obj = IdOBObject(
            name=str(spec["name"]),
            family=str(spec["family"]),
            priority=int(spec["priority"]),
            activate=_activation_for_name(str(spec["name"])),
            apply=APPLY_LOOKUP[apply_symbol],
        )
        registry_items.append(obj)
    return sorted(registry_items, key=lambda obj: (obj.priority, obj.name))


def build_r2_registry() -> List[IdOBObject]:
    schema = _load_schema(SCHEMA_PATH)
    specs = _load_object_specs(OBJECTS_DIR, schema)
    return _build_registry_from_specs(specs)


def build_r2_overlap_graph(specs: List[Tuple[Path, Dict[str, Any]]]) -> Dict[str, Dict[Tuple[str, str], str]]:
    near: Dict[Tuple[str, str], str] = {}
    far: Dict[Tuple[str, str], str] = {}
    spec_names = {str(spec["name"]) for _path, spec in specs}

    for _path, spec in specs:
        name = str(spec["name"])
        overlap = spec.get("overlap", {}) or {}
        for target in overlap.get("near", []) or []:
            target_name = str(target)
            if target_name not in spec_names:
                raise ValueError(f"Overlap near edge references unknown object {target_name} from {name}")
            mode = "suppress" if {name, target_name} == {"interrogative_wh", "interrogative_polar"} else "merge"
            near[(name, target_name)] = mode
        for target in overlap.get("far", []) or []:
            target_name = str(target)
            if target_name not in spec_names:
                raise ValueError(f"Overlap far edge references unknown object {target_name} from {name}")
            if name in {"interrogative_wh", "interrogative_polar"} and target_name == "copular_state":
                mode = "suppress"
            elif name == "residual_identity" and target_name in {"copular_state", "locative"}:
                mode = "coexist"
            else:
                mode = "coexist"
            far[(name, target_name)] = mode
    return {"near": near, "far": far}


def compute_registry_digest(
    registry: List[IdOBObject],
    overlap_graph: Dict[str, Dict[Tuple[str, str], str]],
    schema_path: Path,
    psc_defaults_path: Path,
    specs: List[Tuple[Path, Dict[str, Any]]],
) -> str:
    schema_blob = schema_path.read_text(encoding="utf-8")
    psc_defaults_blob = psc_defaults_path.read_text(encoding="utf-8")
    object_rows = [
        {
            "name": obj.name,
            "family": obj.family,
            "priority": obj.priority,
        }
        for obj in registry
    ]
    near_edges = [
        {"a": a, "b": b, "mode": mode}
        for (a, b), mode in sorted(overlap_graph.get("near", {}).items())
    ]
    far_edges = [
        {"a": a, "b": b, "mode": mode}
        for (a, b), mode in sorted(overlap_graph.get("far", {}).items())
    ]
    payload = {
        "schema_sha256": hashlib.sha256(schema_blob.encode("utf-8")).hexdigest(),
        "psc_defaults_sha256": hashlib.sha256(psc_defaults_blob.encode("utf-8")).hexdigest(),
        "objects": object_rows,
        "near": near_edges,
        "far": far_edges,
        "specs": [
            {
                "path": str(path.relative_to(ROOT_DIR)).replace("\\", "/"),
                "spec": spec,
            }
            for path, spec in specs
        ],
    }
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def _object_specs_by_name(specs: List[Tuple[Path, Dict[str, Any]]]) -> Dict[str, Dict[str, Any]]:
    by_name: Dict[str, Dict[str, Any]] = {}
    for _path, spec in specs:
        by_name[str(spec["name"])] = spec
    return by_name


def _object_identity_labels(specs: List[Tuple[Path, Dict[str, Any]]]) -> Dict[str, str]:
    labels: Dict[str, str] = {}
    for _path, spec in specs:
        identity = spec.get("identity", {}) or {}
        labels[str(spec["name"])] = str(identity.get("label", str(spec["name"])))
    return labels


def get_identity_label(object_name: str) -> str:
    return object_labels_by_name.get(object_name, object_name)


def evaluate_psc_after_apply(tp: Any, contributions: List[Dict[str, Any]], packet: Dict[str, Any]) -> List[Dict[str, str]]:
    # PSC is report-only in R4b; it never mutates contribution or packet values.
    return evaluate_psc(object_specs_by_name, contributions, tp, packet, psc_defaults)


registry = build_r2_registry()
schema = _load_schema(SCHEMA_PATH)
object_specs = _load_object_specs(OBJECTS_DIR, schema)
object_specs_by_name = _object_specs_by_name(object_specs)
object_labels_by_name = _object_identity_labels(object_specs)
psc_defaults = load_psc_defaults(PSC_DEFAULTS_PATH)
overlap_graph = build_r2_overlap_graph(object_specs)
parity_oracle = legacy_monolith
registry_digest = compute_registry_digest(registry, overlap_graph, SCHEMA_PATH, PSC_DEFAULTS_PATH, object_specs)
