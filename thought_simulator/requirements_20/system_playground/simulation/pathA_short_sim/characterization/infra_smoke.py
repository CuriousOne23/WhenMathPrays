"""infra_smoke characterization collection for milestone-1."""

from typing import Any, Dict, List

from characterization import CharacterizationError


DEFAULT_INFRA_SMOKE_VERSION = "1.0"


def resolve_infra_smoke_params(raw_params: Dict[str, Any]) -> Dict[str, Any]:
    """Validate infra_smoke parameters (milestone-1 uses none)."""
    if not isinstance(raw_params, dict):
        raise ValueError("infra_smoke parameters must be a JSON object")
    unknown = sorted(raw_params.keys())
    if unknown:
        unknown_list = ", ".join(str(key) for key in unknown)
        raise ValueError(f"unknown infra_smoke parameter(s): {unknown_list}")
    return {}


def _runtime_observation(value: Any, source_path: str) -> Dict[str, Any]:
    return {
        "provenance": "runtime_provided",
        "source_path": source_path,
        "value": value,
    }


def _unavailable_observation(reason: str) -> Dict[str, Any]:
    return {
        "provenance": "unavailable",
        "reason": reason,
    }


def _primitive_sequence(simulation_result: Dict[str, Any]) -> List[str]:
    trace = simulation_result.get("trace", [])
    if not isinstance(trace, list):
        raise CharacterizationError("char_observation_missing", "trace is missing or not a list")
    primitive_names: List[str] = []
    for step in trace:
        if not isinstance(step, dict):
            continue
        primitive = step.get("primitive")
        if isinstance(primitive, str) and primitive:
            primitive_names.append(primitive)
    if not primitive_names:
        raise CharacterizationError("char_observation_missing", "trace primitive sequence is missing")
    return primitive_names


def build_infra_smoke_result(simulation_result: Dict[str, Any]) -> Dict[str, Any]:
    """Collect milestone-1 runtime observations for infra_smoke."""
    if not isinstance(simulation_result, dict):
        raise CharacterizationError("char_processing_failed", "simulation result is not a dictionary")

    final_tp = simulation_result.get("final_tp", {})
    if not isinstance(final_tp, dict):
        raise CharacterizationError("char_observation_missing", "final_tp is missing or not a dictionary")

    truth_relation = final_tp.get("truth_relation")
    if not isinstance(truth_relation, str) or not truth_relation:
        raise CharacterizationError("char_observation_missing", "final_tp.truth_relation is missing")

    runtime_observations: Dict[str, Any] = {
        "final_tp.truth_relation": _runtime_observation(
            truth_relation,
            "simulation_result.final_tp.truth_relation",
        ),
        "trace.primitive_sequence": _runtime_observation(
            _primitive_sequence(simulation_result),
            "simulation_result.trace[*].primitive",
        ),
    }

    semantic = final_tp.get("semantic")
    if isinstance(semantic, dict) and "isc_category_result" in semantic:
        runtime_observations["final_tp.semantic.isc_category_result"] = _runtime_observation(
            semantic.get("isc_category_result"),
            "simulation_result.final_tp.semantic.isc_category_result",
        )

    if isinstance(simulation_result.get("s2m_seed"), dict):
        runtime_observations["s2m_seed"] = _runtime_observation(
            simulation_result.get("s2m_seed"),
            "simulation_result.s2m_seed",
        )

    s2m_meaning = simulation_result.get("s2m_meaning")
    if isinstance(s2m_meaning, dict):
        if "default_meaning" in s2m_meaning:
            runtime_observations["s2m_meaning.default_meaning"] = _runtime_observation(
                s2m_meaning.get("default_meaning"),
                "simulation_result.s2m_meaning.default_meaning",
            )
        if "meaning_relations" in s2m_meaning:
            runtime_observations["s2m_meaning.meaning_relations"] = _runtime_observation(
                s2m_meaning.get("meaning_relations"),
                "simulation_result.s2m_meaning.meaning_relations",
            )
        if "candidate_interpretations" in s2m_meaning:
            runtime_observations["s2m_meaning.candidate_interpretations"] = _runtime_observation(
                s2m_meaning.get("candidate_interpretations"),
                "simulation_result.s2m_meaning.candidate_interpretations",
            )

    unavailable_observations = {
        "entropy": _unavailable_observation("milestone1_unavailable"),
        "top_vs_second_margin": _unavailable_observation("milestone1_unavailable"),
    }

    return {
        "type": "infra_smoke",
        "version": DEFAULT_INFRA_SMOKE_VERSION,
        "resolved_type_parameters": {},
        "observations": {
            "runtime_provided": runtime_observations,
            "unavailable": unavailable_observations,
        },
    }

