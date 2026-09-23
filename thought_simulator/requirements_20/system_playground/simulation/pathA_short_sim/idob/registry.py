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
    return [
        copular_state,
        locative,
        mixed_descriptive,
        interrogative_wh,
        interrogative_polar,
        agent_action,
        modifier_resolution,
        residual_identity,
    ]


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


registry = build_r2_registry()
overlap_graph = build_r2_overlap_graph()
parity_oracle = legacy_monolith
