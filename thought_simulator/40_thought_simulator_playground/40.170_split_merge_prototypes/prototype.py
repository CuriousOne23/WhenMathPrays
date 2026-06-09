"""Split/Merge prototype for 40.170_split_merge_prototypes.

Implements deterministic split and merge per 20.130, producing lineage_delta and ΔH% accounting.
Uses ThoughtPoint from 40.160 as base carrier.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Import ThoughtPoint from upstream 40.160
import sys
_tp_path = Path(__file__).resolve().parent.parent / "40.160_tp_lifecycle" / "prototype.py"
import importlib.util
_spec = importlib.util.spec_from_file_location("tp_prototype", _tp_path)
_tp = importlib.util.module_from_spec(_spec)
sys.modules["tp_prototype"] = _tp
_spec.loader.exec_module(_tp)

ThoughtPoint = _tp.ThoughtPoint
EntropyComponents = _tp.EntropyComponents

@dataclass
class LineageDelta:
    event: str
    tick: int
    parent_ids: list[str] = field(default_factory=list)
    child_ids: list[str] = field(default_factory=list)
    delta_h: dict[str, float] = field(default_factory=dict)
    reason_code: str = ""
    missing_mass: float = 0.0

    def as_dict(self) -> dict[str, Any]:
        return {
            "event": self.event,
            "tick": self.tick,
            "parent_ids": self.parent_ids,
            "child_ids": self.child_ids,
            "delta_h": self.delta_h,
            "reason_code": self.reason_code,
            "missing_mass": self.missing_mass,
        }

class SplitMerge:
    """Provides split and merge with lineage_delta and ΔH%."""

    def __init__(self):
        self.lineage_deltas: list[LineageDelta] = []

    def split(self, source: ThoughtPoint, child_count: int, tick: int, reason_code: str = "nominal") -> list[ThoughtPoint]:
        if child_count < 2:
            raise ValueError("child_count must be >= 2")
        if child_count > 5:  # trigger limit for test scenario
            raise ValueError("split limit exceeded")

        children = source.split(tick=tick, child_count=child_count)
        # Compute delta_h (simplified: distribute entropy)
        total_h = source.entropy.total
        per_child = total_h / child_count
        delta_h = {"h_rep": -per_child * 0.1, "h_pred": -per_child * 0.1, "h_struct": -per_child * 0.1}  # example reduction

        ld = LineageDelta(
            event="split",
            tick=tick,
            parent_ids=[source.tp_id],
            child_ids=[c.tp_id for c in children],
            delta_h=delta_h,
            reason_code=reason_code,
            missing_mass=0.0,
        )
        self.lineage_deltas.append(ld)

        for child in children:
            child.add_tag(f"split_from_{source.tp_id}", tick=tick)

        return children

    def merge(self, sources: list[ThoughtPoint], tick: int, basin_id: str | None = None, reason_code: str = "nominal") -> ThoughtPoint:
        if not sources:
            raise ValueError("sources cannot be empty")
        if len(sources) > 10:
            raise ValueError("merge limit exceeded")

        merged = ThoughtPoint.merge(sources, tick=tick, basin_id=basin_id, deterministic_mode=True)

        # Compute lineage_delta for merge
        source_ids = [s.tp_id for s in sources]
        delta_h = {"h_rep": 0.05, "h_pred": 0.05, "h_struct": 0.05}  # example gain on merge

        ld = LineageDelta(
            event="merge",
            tick=tick,
            parent_ids=source_ids,
            child_ids=[merged.tp_id],
            delta_h=delta_h,
            reason_code=reason_code,
            missing_mass=0.0,
        )
        self.lineage_deltas.append(ld)

        merged.add_tag("merged", tick=tick)
        return merged

    def get_lineage_deltas(self) -> list[dict]:
        return [ld.as_dict() for ld in self.lineage_deltas]

    def golden_lineage_delta(self) -> str:
        # For golden diff test
        return json.dumps(self.get_lineage_deltas(), sort_keys=True)


def not_implemented() -> None:
    raise NotImplementedError("40.170: Phase B approval required")