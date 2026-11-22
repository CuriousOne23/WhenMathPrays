"""Characterization dispatcher for milestone-1."""

from typing import Any, Callable, Dict, Optional

from characterization.infra_smoke import (
    DEFAULT_INFRA_SMOKE_VERSION,
    build_infra_smoke_result,
    resolve_infra_smoke_params,
)


ResolvedType = Dict[str, Any]
Runner = Callable[[Dict[str, Any]], Dict[str, Any]]
Resolver = Callable[[Dict[str, Any]], Dict[str, Any]]


_REGISTRY: Dict[str, Dict[str, Any]] = {
    "infra_smoke": {
        "default_version": DEFAULT_INFRA_SMOKE_VERSION,
        "versions": {
            DEFAULT_INFRA_SMOKE_VERSION: {
                "params_resolver": resolve_infra_smoke_params,
                "runner": build_infra_smoke_result,
            }
        },
    }
}


def resolve_characterization(type_name: str, requested_version: Optional[str]) -> ResolvedType:
    """Resolve and return characterization type contract for execution."""
    type_key = str(type_name or "").strip()
    type_entry = _REGISTRY.get(type_key)
    if not type_entry:
        raise ValueError(f"unknown characterization type: {type_name}")

    version = str(requested_version).strip() if requested_version else str(type_entry["default_version"])
    version_entry = type_entry["versions"].get(version)
    if not version_entry:
        raise ValueError(f"unsupported characterization version: {type_key}@{version}")

    return {
        "type": type_key,
        "version": version,
        "params_resolver": version_entry["params_resolver"],
        "runner": version_entry["runner"],
    }


def get_registered_types() -> Dict[str, Any]:
    """Return registry metadata for tests/introspection."""
    meta: Dict[str, Any] = {}
    for type_name, entry in _REGISTRY.items():
        meta[type_name] = {
            "default_version": entry["default_version"],
            "versions": sorted(entry["versions"].keys()),
        }
    return meta

