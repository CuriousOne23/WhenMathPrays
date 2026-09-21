from __future__ import annotations

import argparse
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

    for line in run_log_lines:
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

    return {"blocks": blocks}


def interpret_block(block: Dict[str, Any]) -> Dict[str, Any]:
    primitive = block["primitive"]
    raw_lines = block["lines"]

    def _value_after_colon(line: str, label: str) -> str:
        _, _, tail = line.partition(label)
        return tail.strip()

    def _value_after_marker(line: str, marker: str) -> str:
        start = line.find(marker)
        if start < 0:
            return ""
        start += len(marker)
        end = len(line)
        for stop_marker in [",", ";"]:
            idx = line.find(stop_marker, start)
            if idx != -1:
                end = min(end, idx)
        return line[start:end].strip()

    segments: List[str] = []
    roles: List[str] = []
    constraints_matched: List[str] = []
    residue: List[str] = []
    smoothing_operations: List[str] = []
    semantic_adjacent_cues: List[str] = []
    semantic_core_ops: List[str] = []
    truth_relation = ""
    token_relations: List[str] = []
    ob_set_notes: List[str] = []

    for line in raw_lines:
        if "Segments:" in line:
            value = _value_after_colon(line, "Segments:")
            if value:
                segments.append(value)
        if "Roles:" in line:
            value = _value_after_colon(line, "Roles:")
            if value:
                roles.append(value)

        if "matched=" in line:
            value = _value_after_marker(line, "matched=")
            if value:
                constraints_matched.append(value)
        if "residue=" in line:
            value = _value_after_marker(line, "residue=")
            if value:
                residue.append(value)
        if "operations=" in line:
            value = _value_after_marker(line, "operations=")
            if value:
                smoothing_operations.append(value)
        if "semantic_adjacent_cues=" in line:
            value = _value_after_marker(line, "semantic_adjacent_cues=")
            if value:
                semantic_adjacent_cues.append(value)

        if "Semantic core:" in line:
            value = _value_after_colon(line, "Semantic core:")
            if value:
                semantic_core_ops.append(value)

        if "Truth relation:" in line:
            truth_relation = _value_after_colon(line, "Truth relation:")
        if "truth_relation:" in line:
            truth_relation = _value_after_colon(line, "truth_relation:")

        if "token_relations:" in line:
            value = _value_after_colon(line, "token_relations:")
            if value:
                token_relations.append(value)

        if "OB-Set" in line or "OB Set" in line:
            ob_set_notes.append(line.strip())

    return {
        "primitive": primitive,
        "raw": raw_lines,
        "summary": f"Primitive {primitive} fired.",
        "segments": segments,
        "roles": roles,
        "constraints_matched": constraints_matched,
        "residue": residue,
        "smoothing_operations": smoothing_operations,
        "semantic_adjacent_cues": semantic_adjacent_cues,
        "semantic_core_ops": semantic_core_ops,
        "truth_relation": truth_relation,
        "token_relations": token_relations,
        "ob_set_notes": ob_set_notes,
    }


def interpret_all_blocks(parsed_log: Dict[str, Any]) -> List[Dict[str, Any]]:
    interpreted_blocks: List[Dict[str, Any]] = []
    for block in parsed_log["blocks"]:
        interpreted_blocks.append(interpret_block(block))
    return interpreted_blocks


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
    debug_setup: Dict[str, Any],
) -> str:
    """Generate final output text from assembled explanation data."""
    lines: List[str] = []

    lines.append("# Debug Report")
    lines.append("")

    lines.append("## Dimensions")
    for item in dimensions_explanations.get("dimensions", []):
        name = item.get("name")
        relative_path = item.get("link")
        lines.append(f"- {name}: [{name}]({relative_path})")

    lines.append("")
    lines.append("## Fields")
    for item in field_explanations.get("fields", []):
        name = item.get("name")
        relative_path = item.get("link")
        lines.append(f"- {name}: [{name}]({relative_path})")

    lines.append("")
    lines.append("## Primitives")
    for item in primitive_explanations.get("primitives", []):
        name = item.get("name")
        relative_path = item.get("link")
        lines.append(f"- {name}: [{name}]({relative_path})")

    lines.append("")
    lines.append("## Interpreted Blocks")
    primitive_links = {
        item.get("name"): item.get("link")
        for item in primitive_explanations.get("primitives", [])
    }
    for block in interpreted_blocks:
        primitive = block.get("primitive")
        lines.append(f"### {primitive}")
        lines.append(f"- segments: {block.get('segments', [])}")
        lines.append(f"- roles: {block.get('roles', [])}")
        lines.append(f"- constraints_matched: {block.get('constraints_matched', [])}")
        lines.append(f"- residue: {block.get('residue', [])}")
        lines.append(f"- smoothing_operations: {block.get('smoothing_operations', [])}")
        lines.append(f"- semantic_adjacent_cues: {block.get('semantic_adjacent_cues', [])}")
        lines.append(f"- semantic_core_ops: {block.get('semantic_core_ops', [])}")
        lines.append(f"- truth_relation: {block.get('truth_relation', '')}")
        if block.get("token_relations"):
            lines.append(f"- token_relations: {block.get('token_relations')}")
        if block.get("ob_set_notes"):
            lines.append(f"- ob_set_notes: {block.get('ob_set_notes')}")
        relative_path = primitive_links.get(primitive, "")
        lines.append(f"See: [{primitive}]({relative_path})")
        lines.append("")

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
            debug_setup,
        )
        write_debug_output(output_text, Path(args.base_dir))
        if args.verbose:
            print("Wrote debug_out.md.")
    except Exception as e:
        print(f"Debugging failed: {e}")


if __name__ == "__main__":
    main()
