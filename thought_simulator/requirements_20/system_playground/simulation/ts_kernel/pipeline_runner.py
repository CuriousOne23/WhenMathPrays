"""Load a stage yaml + fixture and hand them to the kernel."""
from __future__ import annotations

import os
from typing import Any, Dict, Optional

import yaml

from .kernel import run_pipeline
from .legality import check_spec


def _read_yaml(path: str):
    with open(path, encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_spec(stage_dir: str) -> list:
    data = _read_yaml(os.path.join(stage_dir, "pipeline.yaml"))
    spec = data.get("pipeline")
    if spec is None and isinstance(data.get("spec"), list):
        spec = data["spec"]
    return check_spec(spec)


def _fixture_path(stage_dir: str, fixture_name: Optional[str]) -> str:
    fixtures_dir = os.path.join(stage_dir, "fixtures")
    if fixture_name:
        path = os.path.join(fixtures_dir, fixture_name)
        if not os.path.isfile(path):
            raise FileNotFoundError("fixture not found: {0}".format(path))
        return path
    names = sorted(
        name for name in os.listdir(fixtures_dir) if name.endswith(".yaml") or name.endswith(".yml")
    )
    if not names:
        raise FileNotFoundError("no fixtures under {0}".format(fixtures_dir))
    return os.path.join(fixtures_dir, names[0])


def load_fixture_tp(path: str) -> Dict[str, Any]:
    data = _read_yaml(path)
    if isinstance(data.get("tp"), dict):
        return data["tp"]
    if isinstance(data, dict):
        return data
    raise ValueError("fixture is not a mapping: {0}".format(path))


def run_stage(
    simulation_root: str,
    stage: str,
    fixture_name: Optional[str] = None,
    legality_only: bool = False,
) -> Dict[str, Any]:
    stage_dir = os.path.join(simulation_root, "pipelines", stage)
    if not os.path.isdir(stage_dir):
        raise FileNotFoundError("unknown stage directory: {0}".format(stage_dir))
    spec = load_spec(stage_dir)
    if legality_only:
        return {"spec": spec, "stage": stage, "legality": True}
    fixture_path = _fixture_path(stage_dir, fixture_name)
    tp_in = load_fixture_tp(fixture_path)
    result = run_pipeline(spec, tp_in)
    result["stage"] = stage
    result["fixture_name"] = os.path.basename(fixture_path)
    result["fixture_path"] = fixture_path
    return result
