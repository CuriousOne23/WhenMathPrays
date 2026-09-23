from __future__ import annotations

import argparse
import ast
from pathlib import Path
from typing import Any, Dict, List

import yaml


DEBUG_DIR = Path(__file__).resolve().parent / "debug"
SETUP_PATH = DEBUG_DIR / "setup" / "debug_setup.yaml"
LINKS_PATH = DEBUG_DIR / "setup" / "links.yaml"


def build_arg_parser() -> argparse.ArgumentParser:
    """Create a CLI parser for debug analysis inputs."""
    parser = argparse.ArgumentParser(description="PathA debug skeleton")
    parser.add_argument("run_log", help="Path to run.log")
    parser.add_argument(
        "--base-dir",
        default=str(Path(__file__).resolve().parent),
        help="Base directory for path resolution",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose debug output",
    )
    return parser


def load_debug_setup(setup_path: Path = SETUP_PATH) -> Dict[str, Any]:
    """Load debug/setup/debug_setup.yaml."""
    # TODO: Add strict schema validation.
    with setup_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_links_registry(links_path: Path = LINKS_PATH) -> Dict[str, Any]:
    """Load debug/setup/links.yaml."""
    # TODO: Add strict schema validation.
    with links_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_run_log(run_log_path: Path) -> List[str]:
    """Load run.log from a CLI-supplied path."""
    encodings = ["utf-8", "utf-8-sig", "utf-16", "utf-16-le", "utf-16-be"]
    for encoding in encodings:
        try:
            return run_log_path.read_text(encoding=encoding).splitlines()
        except UnicodeDecodeError:
            continue
    # Fall back to a permissive read if none of the common encodings decode cleanly.
    return run_log_path.read_text(encoding="utf-8", errors="replace").splitlines()


def resolve_link(
    links_registry: Dict[str, Any],
    section: str,
    key: str,
    base_dir: Path,
) -> str:
    """Return the relative link path from links.yaml unchanged."""
    return str(links_registry.get(section, {}).get(key, ""))


def _literal_eval_safe(value: str) -> Any:
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value


def _extract_literal_or_text(line: str, marker: str) -> Any:
    start = line.find(marker)
    if start < 0:
        return None
    tail = line[start + len(marker) :].strip()
    if not tail:
        return ""

    if tail[0] in "[{(":
        opener = tail[0]
        closer = {
            "[": "]",
            "{": "}",
            "(": ")",
        }[opener]
        depth = 0
        in_quote = ""
        escape = False
        for i, ch in enumerate(tail):
            if escape:
                escape = False
                continue
            if ch == "\\":
                escape = True
                continue
            if in_quote:
                if ch == in_quote:
                    in_quote = ""
                continue
            if ch in ('"', "'"):
                in_quote = ch
                continue
            if ch == opener:
                depth += 1
            elif ch == closer:
                depth -= 1
                if depth == 0:
                    literal_text = tail[: i + 1]
                    return _literal_eval_safe(literal_text)
        return _literal_eval_safe(tail)

    for sep in [";", ","]:
        idx = tail.find(sep)
        if idx != -1:
            tail = tail[:idx].strip()
            break
    return _literal_eval_safe(tail)


def _merge_list(target: List[Any], incoming: Any, dedup: bool = False) -> None:
    if incoming is None:
        return
    if isinstance(incoming, list):
        values = incoming
    else:
        values = [incoming]
    for value in values:
        if dedup:
            if value not in target:
                target.append(value)
        else:
            target.append(value)


def _render_scalar(value: Any) -> str:
    if isinstance(value, str):
        return value
    return str(value)


def _append_list_block(lines: List[str], label: str, values: List[Any]) -> None:
    lines.append(f"- {label}:")
    if not values:
        lines.append("  - []")
        return
    for value in values:
        lines.append(f"  - {_render_scalar(value)}")


def _append_dict_block(lines: List[str], label: str, mapping: Dict[str, Any]) -> None:
    lines.append(f"- {label}:")
    if not mapping:
        lines.append("  - {}")
        return
    for key, value in mapping.items():
        if isinstance(value, list):
            lines.append(f"  {key}:")
            if value:
                for item in value:
                    lines.append(f"    - {_render_scalar(item)}")
            else:
                lines.append("    - []")
        elif isinstance(value, dict):
            lines.append(f"  {key}:")
            for inner_key, inner_value in value.items():
                lines.append(f"    {inner_key}: {_render_scalar(inner_value)}")
        else:
            lines.append(f"  {key}: {_render_scalar(value)}")


def _normalize_ob_set_notes(notes: List[Any]) -> List[str]:
    return []


def _normalize_token_relations(mapping: Dict[str, Any]) -> List[str]:
    relations: List[str] = []
    for key, value in mapping.items():
        if not isinstance(value, (tuple, list)) or len(value) < 2:
            continue
        left_value = str(value[0]).strip()
        right_value = str(value[1]).strip()
        if not left_value or not right_value:
            continue

        relation_key = str(key).replace("->", "-").replace("_", "-")
        if "-" in relation_key:
            source, target = relation_key.split("-", 1)
            relations.append(f"{source.strip()} → {target.strip()}")
        else:
            relations.append(f"{relation_key.strip()} →")
    return relations


def parse_run_log(run_log_lines: List[str]) -> Dict[str, Any]:
    """Parse run.log into structured intermediate data."""
    primitive_headers = [
        ("SOB:", "SOB"),
        ("SROB:", "SROB"),
        ("CnOB:", "CnOB"),
        ("SmOB:", "SmOB"),
        ("IdOB:", "IdOB"),
        ("--- SOB ---", "SOB"),
        ("--- SROB ---", "SROB"),
        ("--- CnOB ---", "CnOB"),
        ("--- SmOB ---", "SmOB"),
        ("--- IdOB ---", "IdOB"),
    ]

    blocks: List[Dict[str, Any]] = []
    current_block: Dict[str, Any] | None = None
    raw_tokens: List[Any] = []

    for line in run_log_lines:
        if not raw_tokens:
            stripped = line.strip()
            if stripped.startswith("tokens:"):
                extracted_tokens = _extract_literal_or_text(stripped, "tokens:")
                if isinstance(extracted_tokens, list):
                    raw_tokens = extracted_tokens

        matched_primitive = None
        for header, primitive_name in primitive_headers:
            if header in line:
                matched_primitive = primitive_name
                break

        if matched_primitive is not None:
            if current_block is not None:
                blocks.append(current_block)
            current_block = {"primitive": matched_primitive, "lines": [line]}
            continue

        if current_block is not None:
            current_block["lines"].append(line)

    if current_block is not None:
        blocks.append(current_block)

    return {"blocks": blocks, "raw_tokens": raw_tokens}


def interpret_block(block: Dict[str, Any]) -> Dict[str, Any]:
    primitive = block["primitive"]
    raw_lines = block["lines"]

    segments: List[Any] = []
    segment_tokens: List[Any] = []
    roles: List[Any] = []
    constraints_matched: List[Any] = []
    constraints_unmatched: List[Any] = []
    constraint_residue: List[Any] = []
    basin_residue: List[Any] = []
    smoothing_operations: List[Any] = []
    semantic_adjacent_cues: List[Any] = []
    semantic_core: Dict[str, Any] = {}
    truth_relation = ""
    idob_packet: Dict[str, Any] = {}

    for line in raw_lines:
        extracted = _extract_literal_or_text(line, "Segments:")
        if extracted is not None:
            _merge_list(segments, extracted, dedup=False)

        extracted = _extract_literal_or_text(line, "struct_segments=")
        if extracted is not None:
            _merge_list(segments, extracted, dedup=False)

        extracted = _extract_literal_or_text(line, "Segment tokens:")
        if extracted is not None:
            _merge_list(segment_tokens, extracted, dedup=False)

        extracted = _extract_literal_or_text(line, "segment_tokens=")
        if extracted is not None:
            _merge_list(segment_tokens, extracted, dedup=False)

        extracted = _extract_literal_or_text(line, "Roles:")
        if extracted is not None:
            _merge_list(roles, extracted, dedup=False)

        extracted = _extract_literal_or_text(line, "struct_roles=")
        if extracted is not None:
            _merge_list(roles, extracted, dedup=False)

        extracted = _extract_literal_or_text(line, "constraints_matched=")
        if extracted is not None:
            _merge_list(constraints_matched, extracted, dedup=False)

        extracted = _extract_literal_or_text(line, "constraints_unmatched=")
        if extracted is not None:
            _merge_list(constraints_unmatched, extracted, dedup=False)

        extracted = _extract_literal_or_text(line, "constraint_residue=")
        if extracted is not None:
            _merge_list(constraint_residue, extracted, dedup=False)

        extracted = _extract_literal_or_text(line, "basin_residue=")
        if extracted is not None:
            _merge_list(basin_residue, extracted, dedup=False)

        extracted = _extract_literal_or_text(line, "smoothing_operations=")
        if extracted is not None:
            _merge_list(smoothing_operations, extracted, dedup=False)

        extracted = _extract_literal_or_text(line, "semantic_adjacent_cues=")
        if extracted is not None:
            _merge_list(semantic_adjacent_cues, extracted, dedup=False)

        extracted = _extract_literal_or_text(line, "semantic_core=")
        if isinstance(extracted, list):
            semantic_core["values"] = extracted
        elif isinstance(extracted, dict):
            semantic_core.update(extracted)

        extracted = _extract_literal_or_text(line, "idob_packet=")
        if isinstance(extracted, dict):
            idob_packet.update(extracted)
            if isinstance(idob_packet.get("semantic_core"), list):
                semantic_core = {"values": idob_packet["semantic_core"]}
            truth_from_packet = idob_packet.get("truth_relation")
            if truth_from_packet not in (None, ""):
                truth_relation = _render_scalar(truth_from_packet)

        extracted_truth = _extract_literal_or_text(line, "Truth relation:")
        if extracted_truth not in (None, ""):
            truth_relation = _render_scalar(extracted_truth)
        extracted_truth_lower = _extract_literal_or_text(line, "truth_relation:")
        if extracted_truth_lower not in (None, ""):
            truth_relation = _render_scalar(extracted_truth_lower)

    if truth_relation:
        semantic_core["truth_relation"] = truth_relation

    return {
        "primitive": primitive,
        "raw": raw_lines,
        "summary": f"Primitive {primitive} fired.",
        "segments": segments,
        "segment_tokens": segment_tokens,
        "roles": roles,
        "constraints_matched": constraints_matched,
        "constraints_unmatched": constraints_unmatched,
        "constraint_residue": constraint_residue,
        "basin_residue": basin_residue,
        "smoothing_operations": smoothing_operations,
        "semantic_adjacent_cues": semantic_adjacent_cues,
        "semantic_core": semantic_core,
        "truth_relation": truth_relation,
        "idob_packet": idob_packet,
    }


def interpret_all_blocks(parsed_log: Dict[str, Any]) -> List[Dict[str, Any]]:
    interpreted_by_primitive: Dict[str, Dict[str, Any]] = {}
    for block in parsed_log["blocks"]:
        interpreted = interpret_block(block)
        primitive = interpreted["primitive"]
        if primitive not in interpreted_by_primitive:
            interpreted_by_primitive[primitive] = interpreted
            continue

        current = interpreted_by_primitive[primitive]
        _merge_list(current["raw"], interpreted.get("raw", []), dedup=True)
        _merge_list(current["segments"], interpreted.get("segments", []), dedup=True)
        _merge_list(
            current["segment_tokens"], interpreted.get("segment_tokens", []), dedup=True
        )
        _merge_list(current["roles"], interpreted.get("roles", []), dedup=False)
        _merge_list(
            current["constraints_matched"], interpreted.get("constraints_matched", []), dedup=True
        )
        _merge_list(
            current["constraints_unmatched"], interpreted.get("constraints_unmatched", []), dedup=True
        )
        _merge_list(current["constraint_residue"], interpreted.get("constraint_residue", []), dedup=True)
        _merge_list(
            current["basin_residue"], interpreted.get("basin_residue", []), dedup=True
        )
        _merge_list(
            current["smoothing_operations"], interpreted.get("smoothing_operations", []), dedup=True
        )
        _merge_list(
            current["semantic_adjacent_cues"], interpreted.get("semantic_adjacent_cues", []), dedup=True
        )
        current["semantic_core"].update(interpreted.get("semantic_core", {}))
        current["idob_packet"].update(interpreted.get("idob_packet", {}))
        if interpreted.get("truth_relation"):
            current["truth_relation"] = interpreted["truth_relation"]
            current["semantic_core"]["truth_relation"] = interpreted["truth_relation"]

    return list(interpreted_by_primitive.values())


def extract_segment_info(block: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "not_implemented",
        "primitive": block["primitive"],
    }


def extract_role_info(block: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "not_implemented",
        "primitive": block["primitive"],
    }


def extract_constraint_info(block: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "not_implemented",
        "primitive": block["primitive"],
    }


def explain_dimensions(
    parsed_log: Dict[str, Any],
    debug_setup: Dict[str, Any],
    links_registry: Dict[str, Any],
    base_dir: Path,
) -> Dict[str, Any]:
    """Build dimension-level explanations from parsed run.log data."""
    dimensions = []
    for dimension in debug_setup.get("dimensions", []):
        dimensions.append(
            {
                "name": dimension,
                "link": resolve_link(links_registry, "dimensions", dimension, base_dir),
            }
        )
    return {"dimensions": dimensions}


def explain_fields(
    parsed_log: Dict[str, Any],
    debug_setup: Dict[str, Any],
    links_registry: Dict[str, Any],
    base_dir: Path,
) -> Dict[str, Any]:
    """Build field-level explanations from parsed run.log data."""
    fields = []
    for field in debug_setup.get("fields", []):
        fields.append(
            {
                "name": field,
                "link": resolve_link(links_registry, "fields", field, base_dir),
            }
        )
    return {"fields": fields}


def explain_primitives(
    parsed_log: Dict[str, Any],
    debug_setup: Dict[str, Any],
    links_registry: Dict[str, Any],
    base_dir: Path,
) -> Dict[str, Any]:
    """Build primitive-level explanations from parsed run.log data."""
    primitives = []
    for primitive in debug_setup.get("primitives", []):
        primitives.append(
            {
                "name": primitive,
                "link": resolve_link(links_registry, "primitives", primitive, base_dir),
            }
        )
    return {"primitives": primitives}


def generate_output(
    dimensions_explanations: Dict[str, Any],
    field_explanations: Dict[str, Any],
    primitive_explanations: Dict[str, Any],
    interpreted_blocks: List[Dict[str, Any]],
    raw_tokens: List[Any],
    debug_setup: Dict[str, Any],
) -> str:
    """Generate final output text from assembled explanation data."""
    lines: List[str] = []
    dimension_definitions = {
        "segment_geometry": "How the simulator divides an utterance into structural segments.",
        "role_geometry": "How functional roles attach to segments.",
        "constraint_geometry": "How structural and semantic constraints are evaluated.",
        "identity_geometry": "How identity and referential structure propagate.",
        "semantic_core": "How IdOB stabilizes canonical semantic_core.",
        "truth_relation": "How IdOB stabilizes canonical truth_relation.",
    }
    field_definitions = {
        "struct_segments": "The segments detected during structural parsing.",
        "segment_tokens": "Token groups attached to each structural segment.",
        "struct_roles": "The roles assigned to each segment.",
        "constraints_matched": "Constraints successfully satisfied.",
        "constraints_unmatched": "Constraints that remained unsatisfied.",
        "constraint_residue": "Residual mismatch material from CnOB.",
        "smoothing_operations": "Smoothing transforms applied by SmOB.",
        "semantic_adjacent_cues": "Semantic cues adjacent to structural elements.",
        "basin_residue": "Residual unresolved basin-level material from SmOB.",
        "truth_relation": "Truth relation selected for meaning resolution.",
        "semantic_core": "Identity-conditioned semantic bundle emitted by IdOB.",
        "idob_packet": "The identity packet produced by IdOB.",
    }
    primitive_definitions = {
        "SOB": "Performs structural segmentation.",
        "SROB": "Assigns roles to segments.",
        "CnOB": "Matches constraints and emits canonical constraint fields.",
        "SmOB": "Applies smoothing and adjacency resolution.",
        "IdOB": "Builds the identity packet and semantic core.",
    }

    lines.append("# Debug Report")
    lines.append("")

    lines.append("## Dimensions")
    canonical_dimensions = {
        "segment_geometry",
        "role_geometry",
        "constraint_geometry",
        "identity_geometry",
        "semantic_core",
        "truth_relation",
    }
    for item in dimensions_explanations.get("dimensions", []):
        name = item.get("name")
        if name not in canonical_dimensions:
            continue
        relative_path = item.get("link")
        definition = dimension_definitions.get(name, "")
        lines.append(f"- [{name}:]({relative_path}) {definition}")

    lines.append("")
    lines.append("## Fields")
    for item in field_explanations.get("fields", []):
        name = item.get("name")
        relative_path = item.get("link")
        definition = field_definitions.get(name, "")
        lines.append(f"- [{name}:]({relative_path}) {definition}")

    lines.append("")
    lines.append("## Primitives")
    for item in primitive_explanations.get("primitives", []):
        name = item.get("name")
        relative_path = item.get("link")
        definition = primitive_definitions.get(name, "")
        lines.append(f"- [{name}:]({relative_path}) {definition}")

    lines.append("")
    lines.append("## Canonical Routing Ladder Summary")
    lines.append("- Tokens -> Segments -> Roles -> Constraints/Cues -> Basin -> Identity")
    lines.append("- SOB: structural segmentation stage")
    lines.append("- SROB: role assignment stage")
    lines.append("- CnOB: constraint matching stage")
    lines.append("- SmOB: smoothing and basin-adjacency stage")
    lines.append("- IdOB: identity and meaning-bundle stage")

    lines.append("")
    lines.append("## Stage Interpretations")
    primitive_links = {
        item.get("name"): item.get("link")
        for item in primitive_explanations.get("primitives", [])
    }
    primitive_output_fields = {
        "SOB": ["struct_segments", "segment_tokens"],
        "SROB": ["struct_roles"],
        "CnOB": ["constraints_matched", "constraints_unmatched", "constraint_residue"],
        "SmOB": ["smoothing_operations", "semantic_adjacent_cues", "basin_residue"],
        "IdOB": ["idob_packet"],
    }

    field_value_lookup = {
        "struct_segments": "segments",
        "segment_tokens": "segment_tokens",
        "struct_roles": "roles",
        "constraints_matched": "constraints_matched",
        "constraints_unmatched": "constraints_unmatched",
        "constraint_residue": "constraint_residue",
        "smoothing_operations": "smoothing_operations",
        "semantic_adjacent_cues": "semantic_adjacent_cues",
        "basin_residue": "basin_residue",
        "idob_packet": "idob_packet",
        "semantic_core": "semantic_core",
        "truth_relation": "truth_relation",
    }

    for block in interpreted_blocks:
        primitive = block.get("primitive")
        lines.append(f"### {primitive}")
        if primitive == "SOB":
            _append_list_block(lines, "tokens", raw_tokens)
            lines.append("")
        for field_name in primitive_output_fields.get(str(primitive), []):
            data_key = field_value_lookup[field_name]
            value = block.get(data_key)
            if isinstance(value, list):
                _append_list_block(lines, field_name, value)
            elif isinstance(value, dict):
                _append_dict_block(lines, field_name, value)
            else:
                lines.append(f"- {field_name}: {_render_scalar(value)}")
            lines.append("")

        relative_path = primitive_links.get(primitive, "")
        lines.append("")
        lines.append(f"See: [{primitive}]({relative_path})")
        lines.append("")

    smob_block = next((b for b in interpreted_blocks if b.get("primitive") == "SmOB"), {})
    idob_block = next((b for b in interpreted_blocks if b.get("primitive") == "IdOB"), {})
    idob_packet = idob_block.get("idob_packet", {})

    lines.append("## Meaning Bundle Summary")
    lines.append(f"- truth_relation: {_render_scalar(idob_packet.get('truth_relation', ''))}")
    _append_list_block(
        lines,
        "semantic_adjacent_cues",
        smob_block.get("semantic_adjacent_cues", []),
    )
    semantic_core_values = idob_packet.get("semantic_core", [])
    _append_list_block(lines, "semantic_core", semantic_core_values if isinstance(semantic_core_values, list) else [])
    _append_dict_block(lines, "idob_packet", idob_packet if isinstance(idob_packet, dict) else {})

    return "\n".join(lines)


def write_debug_output(output_text: str, base_dir: Path) -> None:
    output_path = base_dir / "debug_out.md"
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write(output_text)


def main() -> None:
    try:
        parser = build_arg_parser()
        args = parser.parse_args()

        debug_setup = load_debug_setup()
        if args.verbose:
            print("Loaded debug setup.")
        links_registry = load_links_registry()
        if args.verbose:
            print("Loaded links registry.")
        run_log_lines = load_run_log(Path(args.run_log))
        if args.verbose:
            print("Loaded run log.")

        parsed_log = parse_run_log(run_log_lines)
        interpreted_blocks = interpret_all_blocks(parsed_log)
        if args.verbose:
            print("Parsed run log.")
        dimensions_explanations = explain_dimensions(
            parsed_log,
            debug_setup,
            links_registry,
            Path(args.base_dir),
        )
        field_explanations = explain_fields(
            parsed_log,
            debug_setup,
            links_registry,
            Path(args.base_dir),
        )
        primitive_explanations = explain_primitives(
            parsed_log,
            debug_setup,
            links_registry,
            Path(args.base_dir),
        )
        if args.verbose:
            print("Generated explanations.")

        output_text = generate_output(
            dimensions_explanations,
            field_explanations,
            primitive_explanations,
            interpreted_blocks,
            parsed_log.get("raw_tokens", []),
            debug_setup,
        )
        write_debug_output(output_text, Path(args.base_dir))
        if args.verbose:
            print("Wrote debug_out.md.")
    except Exception as e:
        print(f"Debugging failed: {e}")


if __name__ == "__main__":
    main()
