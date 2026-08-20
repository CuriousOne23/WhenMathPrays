from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]


@dataclass
class ConversationConfig:
    name: str
    markdown_path: Path
    out_dir: Path


CONVERSATIONS = [
    ConversationConfig(
        name="conv_02",
        markdown_path=REPO_ROOT
        / "thought_simulator"
        / "requirements_20"
        / "system_playground"
        / "simulation"
        / "conversations"
        / "conv_02"
        / "idob"
        / "idob_input_output_examples.md",
        out_dir=REPO_ROOT
        / "thought_simulator"
        / "requirements_20"
        / "system_playground"
        / "simulation"
        / "conversations"
        / "conv_02"
        / "idob",
    ),
    ConversationConfig(
        name="conv_03",
        markdown_path=REPO_ROOT
        / "thought_simulator"
        / "requirements_20"
        / "system_playground"
        / "simulation"
        / "conversations"
        / "conv_03"
        / "idob"
        / "idob_conv_3.md",
        out_dir=REPO_ROOT
        / "thought_simulator"
        / "requirements_20"
        / "system_playground"
        / "simulation"
        / "conversations"
        / "conv_03"
        / "idob",
    ),
]


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def dump_yaml(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=False)


def extract_labeled_yaml_blocks(md_text: str, label_pattern: str) -> list[dict[str, Any]]:
    lines = md_text.splitlines()
    pattern = re.compile(label_pattern, re.IGNORECASE)
    blocks: list[dict[str, Any]] = []
    i = 0

    while i < len(lines):
        if not pattern.search(lines[i]):
            i += 1
            continue

        j = i + 1
        while j < len(lines) and not lines[j].strip().startswith("```yaml"):
            j += 1
        if j >= len(lines):
            break

        k = j + 1
        while k < len(lines) and not lines[k].strip().startswith("```"):
            k += 1
        if k >= len(lines):
            break

        yaml_text = "\n".join(lines[j + 1 : k])
        parsed = yaml.safe_load(yaml_text) or {}
        if not isinstance(parsed, dict):
            parsed = {"value": parsed}
        blocks.append(parsed)

        i = k + 1

    return blocks


def process_conversation(cfg: ConversationConfig) -> dict[str, Any]:
    if not cfg.markdown_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {cfg.markdown_path}")

    text = load_text(cfg.markdown_path)
    input_blocks = extract_labeled_yaml_blocks(text, r"IdOB\s+Input\s+YAML|\bInput\s+YAML\b")
    output_blocks = extract_labeled_yaml_blocks(text, r"IdOB\s+Output\s+YAML|\bOutput\s+YAML\b")

    if len(input_blocks) != 10 or len(output_blocks) != 10:
        raise ValueError(
            f"{cfg.name}: expected 10 input and 10 output blocks, got {len(input_blocks)} input and {len(output_blocks)} output"
        )

    cfg.out_dir.mkdir(parents=True, exist_ok=True)

    entries: list[dict[str, Any]] = []
    for idx, (inp, outp) in enumerate(zip(input_blocks, output_blocks), start=1):
        in_doc = {
            "source": {
                "conversation": cfg.name,
                "message": idx,
                "stage": "idob_input",
                "source_markdown": str(cfg.markdown_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            },
            "idob_input": inp,
        }
        out_doc = {
            "source": {
                "conversation": cfg.name,
                "message": idx,
                "stage": "idob_output",
                "source_markdown": str(cfg.markdown_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            },
            "idob_output": outp,
        }

        in_path = cfg.out_dir / f"msg{idx}_idob_input.yaml"
        out_path = cfg.out_dir / f"msg{idx}_idob_output.yaml"
        dump_yaml(in_path, in_doc)
        dump_yaml(out_path, out_doc)

        entries.append(
            {
                "message": idx,
                "input_file": in_path.name,
                "output_file": out_path.name,
            }
        )

    run_log = {
        "conversation": cfg.name,
        "source_markdown": str(cfg.markdown_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "messages_processed": 10,
        "files_generated": 20,
        "entries": entries,
    }
    dump_yaml(cfg.out_dir / "idob_run_log.yaml", run_log)

    return {
        "conversation": cfg.name,
        "messages": 10,
        "out_dir": str(cfg.out_dir),
    }


def main() -> None:
    results = [process_conversation(cfg) for cfg in CONVERSATIONS]
    print("Generated IdOB input/output YAML files:")
    for result in results:
        print(f"- {result['conversation']}: {result['messages']} messages -> {result['out_dir']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
