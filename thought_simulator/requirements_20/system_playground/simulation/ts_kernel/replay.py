"""Determinism hook: canonical freeze of a TP."""
from __future__ import annotations

import json
from typing import Any


def freeze(tp: Any) -> str:
    return json.dumps(tp, sort_keys=True, default=str, ensure_ascii=True)


def freezes_equal(a: str, b: str) -> bool:
    return a == b
