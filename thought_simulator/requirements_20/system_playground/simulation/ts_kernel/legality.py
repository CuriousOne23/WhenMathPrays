"""Name legality for a pipeline spec.

Present checks: loadable via registry, name match, process callable.
Does not encode a global Path A order table.
"""
from __future__ import annotations

from .registry import RegistryError, load


class LegalityError(Exception):
    """Pipeline spec is not legal."""


def check_spec(spec) -> list:
    if not isinstance(spec, list) or not spec:
        raise LegalityError("pipeline spec must be a non-empty list of names")
    resolved = []
    for name in spec:
        try:
            module = load(name)
        except RegistryError as exc:
            raise LegalityError(str(exc)) from exc
        resolved.append(name)
        getattr(module, "process")
    return resolved
