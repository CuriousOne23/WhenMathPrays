"""Six-axis meaning helpers for this instrument revision."""

import math

NAMES = (
    "physicality",
    "sociality",
    "temporality",
    "intentionality",
    "materiality",
    "spatiality",
)


def zeros():
    return {name: 0.0 for name in NAMES}


def from_mapping(mapping):
    mapping = mapping or {}
    return {name: float(mapping.get(name, 0.0)) for name in NAMES}


def clip_unit(vector):
    return {name: max(0.0, min(1.0, float(vector[name]))) for name in NAMES}


def add_scaled(base, other, scale, clip=True):
    out = {}
    for name in NAMES:
        out[name] = float(base.get(name, 0.0)) + scale * float(other.get(name, 0.0))
    return clip_unit(out) if clip else out


def delta_l2(a, b):
    total = 0.0
    for name in NAMES:
        d = float(a.get(name, 0.0)) - float(b.get(name, 0.0))
        total += d * d
    return math.sqrt(total)


def fmt(vector, digits=2):
    parts = [f"{name[:4]}={vector[name]:.{digits}f}" for name in NAMES]
    return "{" + ", ".join(parts) + "}"
