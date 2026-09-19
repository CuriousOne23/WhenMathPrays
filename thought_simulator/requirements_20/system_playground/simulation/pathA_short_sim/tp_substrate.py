from dataclasses import dataclass, field
from copy import deepcopy
from typing import Any, Dict, List


@dataclass
class TP:
    # Intake
    raw_text: str = ""
    tokens: List[str] = field(default_factory=list)
    normalized_text: str = ""

    # Defects & correction
    defects: List[str] = field(default_factory=list)
    corrections: List[str] = field(default_factory=list)
    correction_score: float = 0.0

    # OB-set / structural geometry
    struct_segments: List[str] = field(default_factory=list)
    segment_tokens: List[List[str]] = field(default_factory=list)
    struct_roles: List[str] = field(default_factory=list)
    role_segments: Dict[str, List[str]] = field(default_factory=dict)
    constraints: List[str] = field(default_factory=list)
    smoothed_geometry: bool = False
    structural_vector_frozen: bool = False

    # Routing
    routing_metadata: Dict[str, Any] = field(default_factory=dict)
    routing_decision: str = ""
    routing_committed: bool = False

    # Semantics & truth
    semantic_core: Dict[str, Any] = field(default_factory=dict)
    truth_relation: str = ""

    # Meta / commit
    commit_flags: Dict[str, bool] = field(default_factory=dict)


def init_tp(raw_text: str) -> TP:
    """Initialize TP substrate for a new Path-A run."""
    tp = TP()
    tp.raw_text = raw_text
    return tp


def clone_tp(tp: TP) -> TP:
    """Replay-safe snapshot helper."""
    return deepcopy(tp)
