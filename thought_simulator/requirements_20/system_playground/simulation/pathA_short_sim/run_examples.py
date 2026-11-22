import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from characterization import CharacterizationError
from characterization.artifacts import (
    build_success_envelope,
    find_existing_canonical_identity_artifact,
    intended_artifact_path,
    persist_success_envelope,
)
from characterization.dispatcher import resolve_characterization
from pathA_short_simulator import run_pathA_short
from mcb.seam import copy_from_idob
from ouba.assembly import build_ouba


IDOB_PACKET_KEY_ORDER = [
    "identity_geometry",
    "truth_relation",
    "truth_relation_family",
    "semantic_core",
    "selected_ops",
    "claimed_fields",
    "contributors",
    "contributions",
    "activation_set",
    "inactive_objects",
    "residual_activated",
    "overlap_events",
    "meaning_delta",
    "psc_violations",
    "registry_digest",
    "complete",
    "tru_hint",
]
SESSION_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
CHAR_TRACE_HEADER = "=== CHAR TRACE ==="
CHAR_FAILURE_CODES = {
    "char_cli_invalid",
    "char_identity_conflict",
    "char_ts_execution_failed",
    "char_observation_missing",
    "char_processing_failed",
    "char_persist_failed",
    "char_interrupted",
}


def _find_repo_root(start: Path) -> Optional[Path]:
    current = start.resolve()
    for candidate in [current] + list(current.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def _repo_relative_posix(path: str) -> str:
    repo_root = _find_repo_root(Path(__file__).resolve().parent)
    if repo_root is None:
        raise CharacterizationError("char_processing_failed", "unable to locate repository root for CHAR TRACE")
    resolved = Path(path).resolve()
    try:
        relative = resolved.relative_to(repo_root)
    except ValueError:
        raise CharacterizationError("char_processing_failed", "committed artifact path is outside repository root")
    return relative.as_posix()


def _trace_context_from_args(args: argparse.Namespace, characterization_request: Optional[dict]) -> Dict[str, str]:
    if characterization_request is not None:
        return {
            "type": str(characterization_request.get("type", "unknown")),
            "version": str(characterization_request.get("version", "unknown")),
            "session_id": str(characterization_request.get("session_id", "unknown")),
            "run_index": str(characterization_request.get("run_index", "unknown")),
        }

    type_name = str(args.char_type) if getattr(args, "char_type", None) else "unknown"
    version = str(args.char_version) if getattr(args, "char_version", None) else "unknown"
    session_id = str(args.char_session_id) if getattr(args, "char_session_id", None) else "unknown"
    run_index_raw = getattr(args, "char_run_index", None)
    run_index = str(run_index_raw) if run_index_raw is not None else "unknown"
    return {
        "type": type_name,
        "version": version,
        "session_id": session_id,
        "run_index": run_index,
    }


def _emit_char_trace_success(context: Dict[str, str], committed_artifact_path: str) -> None:
    print(CHAR_TRACE_HEADER)
    print(
        "char_trace status=success type={type} version={version} session_id={session_id} run_index={run_index}".format(
            type=context["type"],
            version=context["version"],
            session_id=context["session_id"],
            run_index=context["run_index"],
        )
    )
    print("char_trace artifact={}".format(_repo_relative_posix(committed_artifact_path)))


def _emit_char_trace_failure(code: str, context: Dict[str, str]) -> None:
    print(CHAR_TRACE_HEADER)
    print(
        "char_trace status=failure code={code} type={type} version={version} session_id={session_id} run_index={run_index}".format(
            code=code,
            type=context["type"],
            version=context["version"],
            session_id=context["session_id"],
            run_index=context["run_index"],
        )
    )
    print("char_trace artifact=none")


def _extract_failure_code(message: str) -> str:
    text = str(message)
    head = text.split(":", 1)[0].strip()
    if head in CHAR_FAILURE_CODES:
        return head
    return "char_processing_failed"


def _ordered_idob_packet(packet: object) -> dict:
    if not isinstance(packet, dict):
        return {}
    return {key: packet.get(key) for key in IDOB_PACKET_KEY_ORDER}


def _committed_stream_view(committed_stream: object) -> dict:
    if not isinstance(committed_stream, dict):
        return {
            "tokens": [],
            "normalized_tokens": [],
            "token_classes": [],
            "roles": [],
            "segments": [],
            "segment_tokens": [],
        }

    token_objects = committed_stream.get("tokens", [])
    if not isinstance(token_objects, list):
        token_objects = []

    segment_objects = committed_stream.get("segments", [])
    if not isinstance(segment_objects, list):
        segment_objects = []

    tokens = []
    normalized_tokens = []
    token_classes = []
    roles = []

    for token in token_objects:
        if not isinstance(token, dict):
            continue
        tokens.append(str(token.get("surface", "")))
        normalized_tokens.append(str(token.get("normalized", "")))
        token_classes.append(str(token.get("token_class", "")))
        role_value = token.get("role", "")
        if isinstance(role_value, dict):
            roles.append(str(role_value.get("chosen", "")))
        else:
            roles.append(str(role_value))

    segments = []
    segment_tokens = []
    for seg in segment_objects:
        if not isinstance(seg, dict):
            continue
        seg_id = seg.get("segment_id")
        segments.append(seg_id)
        grouped_tokens = []
        for token in token_objects:
            if not isinstance(token, dict):
                continue
            if token.get("segment_id") == seg_id:
                grouped_tokens.append(str(token.get("surface", "")))
        segment_tokens.append(grouped_tokens)

    return {
        "tokens": tokens,
        "normalized_tokens": normalized_tokens,
        "token_classes": token_classes,
        "roles": roles,
        "segments": segments,
        "segment_tokens": segment_tokens,
    }


def _print_schema_families() -> None:
    import json
    from pathlib import Path
    import yaml
    base = Path(__file__).resolve().parent
    schema = json.loads((base / "support/idob_schemas/idob_object.v1.schema.json").read_text())
    allowed = schema.get("properties", {}).get("family", {}).get("enum", [])
    cards = []
    for path in sorted((base / "support/idob_objects").glob("*.yaml")):
        spec = yaml.safe_load(path.read_text()) or {}
        cards.append((str(spec.get("name")), str(spec.get("family"))))
    missing = sorted({family for _name, family in cards if family not in allowed})
    print("schema families: " + ", ".join(allowed))
    print("card families: " + ", ".join(f"{name}={family}" for name, family in cards))
    print("missing from schema: " + (", ".join(missing) if missing else "none"))
    print("schema families: matched" if not missing else "schema families: not matched")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run PathA short simulation examples")
    parser.add_argument(
        "--no-s2m-seed",
        action="store_true",
        help="Disable optional S2M accountability and meaning output.",
    )
    parser.add_argument(
        "--no-category-observations",
        action="store_true",
        help="Disable category-selection observation scenarios.",
    )
    parser.add_argument(
        "--enable-category-selection",
        action="store_true",
        help="Enable category-selection behavior for the selected execution case.",
    )
    parser.add_argument(
        "--execution-case",
        choices=["sky_blue"],
        default="sky_blue",
        help="Execution case for the primary TS run (default: sky_blue).",
    )
    parser.add_argument(
        "--characterize",
        action="store_true",
        help="Enable characterization mode for one TS execution.",
    )
    parser.add_argument(
        "--char-type",
        help="Characterization type key (required with --characterize).",
    )
    parser.add_argument(
        "--char-session-id",
        help="Characterization session identifier (required with --characterize).",
    )
    parser.add_argument(
        "--char-run-index",
        type=int,
        help="Characterization run index >= 1 (required with --characterize).",
    )
    parser.add_argument(
        "--char-version",
        help="Requested characterization version (optional).",
    )
    parser.add_argument(
        "--char-params-json",
        help="Type-specific characterization parameters as JSON object.",
    )
    parser.add_argument(
        "--char-params-file",
        help="Path to a JSON file containing type-specific parameters as an object.",
    )
    return parser


def _trace_entry(simulation_result: dict, primitive: str) -> dict:
    trace = simulation_result.get("trace", [])
    if not isinstance(trace, list):
        return {}
    for entry in trace:
        if isinstance(entry, dict) and entry.get("primitive") == primitive:
            return entry
    return {}


def _print_category_observation(
    label: str,
    sentence: str,
    simulation_result: dict,
    prior_context: Optional[List[str]] = None,
) -> None:
    print(f"\n=== Category Observation: {label} ===")
    print(f"sentence: {sentence}")
    if prior_context:
        print(f"prior_context: {prior_context}")

    s2m_seed = simulation_result.get("s2m_seed", {})
    s2m_meaning = simulation_result.get("s2m_meaning", {})
    if not isinstance(s2m_seed, dict):
        s2m_seed = {}
    if not isinstance(s2m_meaning, dict):
        s2m_meaning = {}

    written_relations = s2m_seed.get("written_relations", [])
    print(f"structure/default basis: {written_relations}")
    print(f"default_meaning: {json.dumps(s2m_meaning.get('default_meaning', {}), indent=2)}")

    cex = _trace_entry(simulation_result, "CEx").get("cex_output", {})
    ce = _trace_entry(simulation_result, "CE").get("ce_output", {})
    isc = _trace_entry(simulation_result, "ISc").get("isc_output", {})
    tpu = _trace_entry(simulation_result, "TPU")
    merge_output = tpu.get("merge_output", {}) if isinstance(tpu, dict) else {}
    tpu_commit = tpu.get("isc_category_result", {}) if isinstance(tpu, dict) else {}
    final_tp = simulation_result.get("final_tp", {})
    if not isinstance(final_tp, dict):
        final_tp = {}
    committed = (final_tp.get("semantic", {}) or {}).get("isc_category_result", {}) if isinstance(final_tp.get("semantic", {}), dict) else {}

    print(f"CEx cue source/provenance: {json.dumps(cex, indent=2)}")
    print(f"CE category_cue: {json.dumps(ce, indent=2)}")
    print(f"ISc scoring/result: {json.dumps(isc, indent=2)}")
    print(f"Merge handoff (TPU input): {json.dumps(merge_output, indent=2)}")
    print(f"TPU commit payload: {json.dumps(tpu_commit, indent=2)}")
    print(f"TP.semantic.isc_category_result: {json.dumps(committed, indent=2)}")
    print(f"IdOB read-only consumption (S2M cue_state): {json.dumps(s2m_meaning.get('cue_state', {}), indent=2)}")

    candidate_interpretations = s2m_meaning.get("candidate_interpretations", [])
    print(f"S2M candidate consideration: {json.dumps(candidate_interpretations, indent=2)}")
    print(f"S2M selected extensions (meaning_relations): {json.dumps(s2m_meaning.get('meaning_relations', []), indent=2)}")

    print("default-versus-selected result:")
    print(json.dumps(
        {
            "default_meaning": s2m_meaning.get("default_meaning", {}),
            "meaning_relations": s2m_meaning.get("meaning_relations", []),
        },
        indent=2,
    ))


def _resolve_execution_case(case_name: str) -> dict:
    case_key = str(case_name).strip().lower()
    if case_key == "sky_blue":
        return {
            "case": "sky_blue",
            "sentence": "The sky is blue.",
            "prior_context": None,
        }
    raise ValueError(f"unsupported execution case: {case_name}")


def _parse_type_parameters(args: argparse.Namespace, parser: argparse.ArgumentParser) -> dict:
    def cli_invalid(message: str) -> None:
        raise SystemExit(f"char_cli_invalid: {message}")

    if args.char_params_json and args.char_params_file:
        cli_invalid("characterization parameters require exactly one of --char-params-json or --char-params-file")

    if args.char_params_json:
        raw = args.char_params_json
    elif args.char_params_file:
        try:
            with open(args.char_params_file, "r", encoding="utf-8") as handle:
                raw = handle.read()
        except OSError as exc:
            cli_invalid(f"unable to read --char-params-file: {exc}")
    else:
        return {}

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        cli_invalid(f"characterization parameters must be valid JSON: {exc}")
    if not isinstance(payload, dict):
        cli_invalid("characterization parameters must decode to a JSON object")
    return payload


def _resolve_characterization_request(args: argparse.Namespace, parser: argparse.ArgumentParser) -> Optional[dict]:
    def cli_invalid(message: str) -> None:
        raise SystemExit(f"char_cli_invalid: {message}")

    char_args_supplied = any(
        value is not None
        for value in [
            args.char_type,
            args.char_session_id,
            args.char_run_index,
            args.char_version,
            args.char_params_json,
            args.char_params_file,
        ]
    )

    if not args.characterize:
        if char_args_supplied:
            cli_invalid("characterization arguments require --characterize")
        return None

    if not args.char_type:
        cli_invalid("--characterize requires --char-type")
    if not args.char_session_id:
        cli_invalid("--characterize requires --char-session-id")
    if args.char_run_index is None:
        cli_invalid("--characterize requires --char-run-index")

    session_id = str(args.char_session_id)
    if not SESSION_ID_PATTERN.match(session_id):
        cli_invalid("invalid --char-session-id; expected ^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
    run_index = int(args.char_run_index)
    if run_index < 1:
        cli_invalid("--char-run-index must be >= 1")

    raw_type_params = _parse_type_parameters(args, parser)

    try:
        resolved = resolve_characterization(args.char_type, args.char_version)
        resolved_type_params = resolved["params_resolver"](raw_type_params)
    except ValueError as exc:
        cli_invalid(str(exc))

    canonical_existing = find_existing_canonical_identity_artifact(
        session_id=session_id,
        run_index=run_index,
    )
    if canonical_existing is not None:
        raise CharacterizationError(
            "char_identity_conflict",
            "canonical identity already exists at {}".format(canonical_existing),
        )

    return {
        "type": resolved["type"],
        "version": resolved["version"],
        "session_id": session_id,
        "run_index": run_index,
        "intended_artifact_path": str(
            intended_artifact_path(
                session_id=session_id,
                run_index=run_index,
                char_type=resolved["type"],
                char_version=resolved["version"],
            )
        ),
        "resolved_type_parameters": resolved_type_params,
        "runner": resolved["runner"],
    }


def run_characterization_once(
    characterization_request: dict,
    simulation_result: dict,
    source_runtime_flags: dict,
) -> dict:
    """Run one TS execution characterization and persist success evidence."""
    type_result = characterization_request["runner"](simulation_result)
    observations = type_result.get("observations", {}) if isinstance(type_result, dict) else {}
    if not isinstance(observations, dict):
        raise CharacterizationError("char_processing_failed", "characterization observations payload is invalid")
    runtime_provided = observations.get("runtime_provided", {})
    unavailable = observations.get("unavailable", {})
    if not isinstance(runtime_provided, dict) or not isinstance(unavailable, dict):
        raise CharacterizationError("char_processing_failed", "characterization observations payload is invalid")

    envelope = build_success_envelope(
        char_type=characterization_request["type"],
        char_version=characterization_request["version"],
        session_id=characterization_request["session_id"],
        run_index=characterization_request["run_index"],
        source_runtime_flags=source_runtime_flags,
        runtime_provided_observations=runtime_provided,
        unavailable_observations=unavailable,
        resolved_type_parameters=characterization_request["resolved_type_parameters"],
        entrypoint="run_examples.py",
    )
    persist_result = persist_success_envelope(envelope)
    if not persist_result.get("ok"):
        raise CharacterizationError(
            str(persist_result.get("status_code", "char_persist_failed")),
            str(persist_result.get("message", "artifact persistence failed")),
        )

    return {
        "identity": {
            "session_id": characterization_request["session_id"],
            "run_index": characterization_request["run_index"],
        },
        "characterization": {
            "type": characterization_request["type"],
            "version": characterization_request["version"],
        },
        "resolved_type_parameters": characterization_request["resolved_type_parameters"],
        "result": type_result,
        "persistence": persist_result,
    }


def _run_selected_execution(
    sentence: str,
    enable_s2m_seed: bool,
    enable_category_selection: bool,
    prior_context: Optional[List[str]] = None,
) -> dict:
    simulation_result = run_pathA_short(
        sentence,
        enable_s2m_seed=enable_s2m_seed,
        enable_category_selection=enable_category_selection,
        prior_context=prior_context,
    )
    final_tp = simulation_result["final_tp"]

    idob_packet = final_tp.get("idob_packet", final_tp.get("idob", {}))
    truth_relation = final_tp.get("truth_relation", "")
    semantic_core = idob_packet.get("semantic_core", []) if isinstance(idob_packet, dict) else []

    canonical_final_tp = {
        "struct_segments": final_tp.get("struct_segments", []),
        "segment_tokens": final_tp.get("segment_tokens", []),
        "struct_roles": final_tp.get("struct_roles", []),
        "constraints_matched": final_tp.get("constraints_matched", []),
        "constraints_unmatched": final_tp.get("constraints_unmatched", []),
        "constraint_residue": final_tp.get("constraint_residue", []),
        "smoothing_operations": final_tp.get("smoothing_operations", []),
        "semantic_adjacent_cues": final_tp.get("semantic_adjacent_cues", []),
        "smoothing_residue": final_tp.get("smoothing_residue", final_tp.get("basin_residue", [])),
        "truth_relation": truth_relation,
        "semantic_core": semantic_core,
    }

    _print_schema_families()
    print("=== Final TP ===")
    final_tp_ie = _committed_stream_view(final_tp.get("committed_stream", {}))
    print(f"tp_ie_tokens: {final_tp_ie['tokens']}")
    print(f"tp_ie_normalized_tokens: {final_tp_ie['normalized_tokens']}")
    print(f"tp_ie_token_classes: {final_tp_ie['token_classes']}")
    print(f"tp_ie_roles: {final_tp_ie['roles']}")
    print(f"tp_ie_segments: {final_tp_ie['segments']}")
    print(f"tp_ie_segment_tokens: {final_tp_ie['segment_tokens']}")
    for k, v in canonical_final_tp.items():
        print(f"{k}: {v}")

    s2m_seed = simulation_result.get("s2m_seed")
    if isinstance(s2m_seed, dict):
        print("\n--- S2M Accountability (IdOB) ---")
        print(f"s2m_seed: {json.dumps(s2m_seed, indent=2)}")

    s2m_meaning = simulation_result.get("s2m_meaning")
    if isinstance(s2m_meaning, dict):
        print("\n--- S2M Meaning (IdOB) ---")
        print(f"s2m_meaning: {json.dumps(s2m_meaning, indent=2)}")

    print("\n=== Trace ===")

    for primitive_trace_entry in simulation_result["trace"]:
        print(f"\n--- {primitive_trace_entry['primitive']} ---")

        primitive_name = primitive_trace_entry["primitive"]
        if primitive_name == "SOB":
            primitive_output = primitive_trace_entry.get("output", {})
            if not isinstance(primitive_output, dict):
                primitive_output = {}

            struct_segments = primitive_trace_entry.get("struct_segments", primitive_output.get("struct_segments", []))
            segment_tokens = primitive_trace_entry.get("segment_tokens", primitive_output.get("segment_tokens", []))
            committed_stream = primitive_trace_entry.get("committed_stream", primitive_output.get("committed_stream", {}))
            sob_ie = _committed_stream_view(committed_stream)
            print(f"sob_tokens: {sob_ie['tokens']}")
            print(f"sob_struct_segments={struct_segments}")
            print(f"sob_segment_tokens={segment_tokens}")

        if primitive_name == "IE":
            primitive_output = primitive_trace_entry.get("output", {})
            if not isinstance(primitive_output, dict):
                primitive_output = {}
            committed_stream = primitive_trace_entry.get("committed_stream", primitive_output.get("committed_stream", {}))
            ie_view = _committed_stream_view(committed_stream)
            print(f"ie_tokens: {ie_view['tokens']}")
            print(f"ie_normalized_tokens: {ie_view['normalized_tokens']}")
            print(f"ie_token_classes: {ie_view['token_classes']}")
            print(f"ie_roles: {ie_view['roles']}")
            print(f"ie_segments: {ie_view['segments']}")
            print(f"ie_segment_tokens: {ie_view['segment_tokens']}")

        if primitive_name == "SROB":
            struct_roles = primitive_trace_entry.get("struct_roles", [])
            print(f"struct_roles={struct_roles}")

        if primitive_name == "CnOB":
            constraints_matched = primitive_trace_entry.get("constraints_matched", [])
            constraints_unmatched = primitive_trace_entry.get("constraints_unmatched", [])
            constraint_residue = primitive_trace_entry.get("constraint_residue", [])
            print(f"constraints_matched={constraints_matched}")
            print(f"constraints_unmatched={constraints_unmatched}")
            print(f"constraint_residue={constraint_residue}")

        if primitive_name == "SmOB":
            smoothing_operations = primitive_trace_entry.get("smoothing_operations", [])
            semantic_adjacent_cues = primitive_trace_entry.get("semantic_adjacent_cues", [])
            smoothing_residue = primitive_trace_entry.get("smoothing_residue", primitive_trace_entry.get("basin_residue", []))
            print(f"smoothing_operations={smoothing_operations}")
            print(f"semantic_adjacent_cues={semantic_adjacent_cues}")
            print(f"smoothing_residue={smoothing_residue}")

        if primitive_name == "IdOB":
            idob_packet = primitive_trace_entry.get("idob_packet", {})
            print(f"idob_packet={repr(_ordered_idob_packet(idob_packet))}")
            print("--- MCB ---")
            mcb_packet = copy_from_idob(_ordered_idob_packet(idob_packet))
            print(f"mcb_packet={repr(mcb_packet)}")
            ouba_packet = build_ouba(mcb_packet)
            print("--- OuBA ---")
            print(f"ouba_packet={repr(ouba_packet)}")
        # If you want more detail, uncomment:
        # print("input:", step["input"])
        # print("output:", step["output"])

    print("--- R7 ---")
    print("ouba_stable=True")
    print("--- R8 ---")
    print("pipeline_ready=True")
    print("--- R9 ---")
    print("freeze_version='pathA_v1'")
    return simulation_result


def main(
    enable_s2m_seed: bool = True,
    show_category_observations: bool = True,
    execution_case: str = "sky_blue",
    enable_category_selection: bool = False,
) -> dict:
    selected = _resolve_execution_case(execution_case)
    sentence = selected["sentence"]
    prior_context = selected["prior_context"]

    simulation_result = _run_selected_execution(
        sentence=sentence,
        enable_s2m_seed=enable_s2m_seed,
        enable_category_selection=enable_category_selection,
        prior_context=prior_context,
    )

    if not show_category_observations:
        return simulation_result

    print("\n=== Canonical S2M Cases (normative testbench) ===")
    canonical_sentences = [
        "The sky is blue.",
        "The book is on the table.",
        "Where is the book?",
    ]
    for canonical_sentence in canonical_sentences:
        canonical_result = run_pathA_short(canonical_sentence, enable_s2m_seed=enable_s2m_seed)
        s2m_meaning = canonical_result.get("s2m_meaning", {})
        if not isinstance(s2m_meaning, dict):
            s2m_meaning = {}
        print(f"\n- {canonical_sentence}")
        print(f"  default_meaning: {json.dumps(s2m_meaning.get('default_meaning', {}))}")
        print(f"  meaning_relations: {json.dumps(s2m_meaning.get('meaning_relations', []))}")

    print("\n=== Category Selection Observation Cases (non-normative demos) ===")
    no_cue_result = run_pathA_short(
        "The book is on the table.",
        enable_s2m_seed=enable_s2m_seed,
        enable_category_selection=True,
    )
    _print_category_observation("No-cue baseline", "The book is on the table.", no_cue_result)

    sentence_internal_result = run_pathA_short(
        "Where is the book?",
        enable_s2m_seed=enable_s2m_seed,
        enable_category_selection=True,
    )
    _print_category_observation("Sentence-internal cue", "Where is the book?", sentence_internal_result)

    prior_context = ["That location needs support for the object."]
    prior_context_result = run_pathA_short(
        "The book is on the table.",
        enable_s2m_seed=enable_s2m_seed,
        enable_category_selection=True,
        prior_context=prior_context,
    )
    _print_category_observation("Prior-context cue", "The book is on the table.", prior_context_result, prior_context=prior_context)

    _print_category_observation("Refusal / non-selection", "Where is the book?", sentence_internal_result)
    return simulation_result


if __name__ == "__main__":
    parser = build_arg_parser()
    args = parser.parse_args()
    characterization_request: Optional[dict] = None
    char_trace_context = _trace_context_from_args(args, characterization_request)
    char_args_supplied = any(
        value is not None
        for value in [
            args.char_type,
            args.char_session_id,
            args.char_run_index,
            args.char_version,
            args.char_params_json,
            args.char_params_file,
        ]
    )
    should_emit_char_trace = bool(args.characterize or char_args_supplied)
    try:
        characterization_request = _resolve_characterization_request(args, parser)
        char_trace_context = _trace_context_from_args(args, characterization_request)
        enable_s2m_seed = not args.no_s2m_seed
        show_category_observations = False if characterization_request is not None else (not args.no_category_observations)
        source_runtime_flags = {
            "execution_case": args.execution_case,
            "enable_category_selection": bool(args.enable_category_selection),
            "enable_s2m_seed": bool(enable_s2m_seed),
            "show_category_observations": bool(show_category_observations),
        }
        selected_case = _resolve_execution_case(args.execution_case)
        if "prior_context" in selected_case:
            source_runtime_flags["prior_context"] = selected_case.get("prior_context")
        try:
            simulation_result = main(
                enable_s2m_seed=enable_s2m_seed,
                show_category_observations=show_category_observations,
                execution_case=args.execution_case,
                enable_category_selection=args.enable_category_selection,
            )
        except Exception as exc:
            if characterization_request is not None:
                raise CharacterizationError("char_ts_execution_failed", str(exc))
            raise
        if characterization_request is not None:
            characterization_result = run_characterization_once(
                characterization_request=characterization_request,
                simulation_result=simulation_result,
                source_runtime_flags=source_runtime_flags,
            )
            persist_result = characterization_result.get("persistence", {})
            committed_path = persist_result.get("committed_final_path")
            if not committed_path:
                raise CharacterizationError("char_persist_failed", "persistence succeeded without committed path")
            _emit_char_trace_success(char_trace_context, str(committed_path))
    except CharacterizationError as exc:
        if should_emit_char_trace:
            _emit_char_trace_failure(exc.code, char_trace_context)
        raise SystemExit(f"{exc.code}: {exc.message}")
    except SystemExit as exc:
        message = str(exc)
        failure_code = _extract_failure_code(message)
        if should_emit_char_trace and failure_code in CHAR_FAILURE_CODES:
            _emit_char_trace_failure(failure_code, char_trace_context)
        raise
    except KeyboardInterrupt:
        if should_emit_char_trace:
            _emit_char_trace_failure("char_interrupted", char_trace_context)
        raise SystemExit("char_interrupted: interrupted")
    except Exception as exc:
        if should_emit_char_trace:
            _emit_char_trace_failure("char_processing_failed", char_trace_context)
        raise SystemExit(f"char_processing_failed: {exc}")
