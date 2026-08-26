"""Load YAML slides for the IdOB learning bench."""

from pathlib import Path

import yaml


def load_yaml(path):
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def bench_root():
    return Path(__file__).resolve().parent.parent
