import hashlib
import json
from typing import Dict, List, Tuple

from idob.legacy import (
    agent_action,
    copular_state,
    interrogative_polar,
    interrogative_wh,
    legacy_monolith,
    locative,
    mixed_descriptive,
    modifier_resolution,
    residual_identity,
)
from idob.object import IdOBObject


def build_r2_registry() -> List[IdOBObject]:
    unsorted = [
        copular_state,
        locative,
        mixed_descriptive,
        interrogative_wh,
        interrogative_polar,
        agent_action,
        modifier_resolution,
        residual_identity,
    ]
    return sorted(unsorted, key=lambda obj: (obj.priority, obj.name))


def build_r2_overlap_graph() -> Dict[str, Dict[Tuple[str, str], str]]:
    # Declared in R2 for internal sum behavior; not emitted to packets yet.
    near: Dict[Tuple[str, str], str] = {
        ("copular_state", "locative"): "merge",
        ("locative", "mixed_descriptive"): "merge",
        ("interrogative_wh", "interrogative_polar"): "suppress",
        ("mixed_descriptive", "modifier_resolution"): "merge",
    }
    far: Dict[Tuple[str, str], str] = {
        ("interrogative_wh", "copular_state"): "suppress",
        ("interrogative_polar", "copular_state"): "suppress",
        ("residual_identity", "copular_state"): "coexist",
        ("residual_identity", "locative"): "coexist",
    }
    return {"near": near, "far": far}


def compute_registry_digest(registry: List[IdOBObject], overlap_graph: Dict[str, Dict[Tuple[str, str], str]]) -> str:
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
        "objects": object_rows,
        "near": near_edges,
        "far": far_edges,
    }
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


registry = build_r2_registry()
overlap_graph = build_r2_overlap_graph()
parity_oracle = legacy_monolith
registry_digest = compute_registry_digest(registry, overlap_graph)
