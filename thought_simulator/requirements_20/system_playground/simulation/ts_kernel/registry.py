"""Primitive registry.

Key = folder = yaml name = PRIMITIVE_NAME.
Callable = module-level process(tp, mode="general", **kwargs).
Discovery is by pipeline.yaml, not scan-all.
"""
from __future__ import annotations

import importlib
import inspect
from types import ModuleType

PRIMITIVE_ROOT = "thought_simulator.requirements_20.system_playground.primitives"
STUB_SOURCE_MAX_CHARS = 8


class RegistryError(Exception):
    """Name is not a loadable primitive."""


def _validate_name(name: str) -> str:
    if not isinstance(name, str) or not name:
        raise RegistryError("primitive name must be a non-empty string")
    if name != name.lower():
        raise RegistryError("primitive name must be lowercase folder key: {0}".format(name))
    if not all(ch.isalnum() or ch == "_" for ch in name):
        raise RegistryError("illegal primitive name: {0}".format(name))
    return name


def _reported_name(module: ModuleType, name: str) -> str:
    if hasattr(module, "get_primitive_name") and callable(module.get_primitive_name):
        reported = module.get_primitive_name()
        if reported != name:
            raise RegistryError(
                "get_primitive_name()={0!r} does not match key {1!r}".format(reported, name)
            )
        return reported
    reported = getattr(module, "PRIMITIVE_NAME", None)
    if reported is None:
        raise RegistryError("{0} does not export get_primitive_name() or PRIMITIVE_NAME".format(name))
    if reported != name:
        raise RegistryError(
            "PRIMITIVE_NAME={0!r} does not match key {1!r}".format(reported, name)
        )
    return reported


def _refuse_stub(module: ModuleType, name: str) -> None:
    try:
        src = inspect.getsource(module)
    except (OSError, TypeError):
        return
    if len(src.strip()) <= STUB_SOURCE_MAX_CHARS:
        raise RegistryError("stub primitive refused: {0}".format(name))


def load(name: str) -> ModuleType:
    """Import primitives.<name>.<name> and require a real process() callable."""
    name = _validate_name(name)
    module_path = "{0}.{1}.{1}".format(PRIMITIVE_ROOT, name)
    try:
        module = importlib.import_module(module_path)
    except ImportError as exc:
        raise RegistryError("unknown primitive {0!r}: {1}".format(name, exc)) from exc
    _refuse_stub(module, name)
    _reported_name(module, name)
    process = getattr(module, "process", None)
    if process is None or not callable(process):
        raise RegistryError("{0} does not export process(tp, mode=..., **kwargs)".format(name))
    return module
