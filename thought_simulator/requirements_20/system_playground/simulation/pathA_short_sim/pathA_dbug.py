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
) -> Path:
    """Resolve a relative link path from links.yaml into an absolute path."""
    # TODO: Add robust error handling for missing sections or keys.
    relative_path = links_registry.get(section, {}).get(key, "")
    return (base_dir / relative_path).resolve()


def parse_run_log(run_log_lines: List[str]) -> Dict[str, Any]:
    """Parse run.log into structured intermediate data."""
    primitive_headers = {
        "SOB:": "SOB",
        "SROB:": "SROB",
        "CnOB:": "CnOB",
        "SmOB:": "SmOB",
        "IdOB:": "IdOB",
    }

    blocks: List[Dict[str, Any]] = []
    current_block: Dict[str, Any] | None = None

    for line in run_log_lines:
        matched_primitive = None
        for header, primitive_name in primitive_headers.items():
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
    segment_info = extract_segment_info(block)
    role_info = extract_role_info(block)
    constraint_info = extract_constraint_info(block)
    return {
        "primitive": primitive,
        "raw": raw_lines,
        "summary": f"Primitive {primitive} fired with {len(raw_lines)} lines.",
        "segment_info": segment_info,
        "role_info": role_info,
        "constraint_info": constraint_info,
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

    lines.append("## Dimensions")
    for item in dimensions_explanations.get("dimensions", []):
        lines.append(f"- {item.get('name')}: {item.get('link')}")

    lines.append("")
    lines.append("## Fields")
    for item in field_explanations.get("fields", []):
        lines.append(f"- {item.get('name')}: {item.get('link')}")

    lines.append("")
    lines.append("## Primitives")
    for item in primitive_explanations.get("primitives", []):
        lines.append(f"- {item.get('name')}: {item.get('link')}")

    lines.append("")
    lines.append("## Interpreted Blocks")
    for block in interpreted_blocks:
        lines.append(f"- {block.get('primitive')}: {block.get('summary')}")

    return "\n".join(lines)


def write_debug_output(output_text: str, base_dir: Path) -> None:
    output_path = base_dir / "debug_out.log"
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
            print("Wrote debug_out.log.")
    except Exception as e:
        print(f"Debugging failed: {e}")


if __name__ == "__main__":
    main()
