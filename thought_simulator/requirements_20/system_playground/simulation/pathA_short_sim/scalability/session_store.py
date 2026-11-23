from __future__ import annotations

from pathlib import Path
import json
import re


SESSION_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


def _root() -> Path:
    return Path(__file__).resolve().parents[1]


def local_scalability_root() -> Path:
    return _root() / "local_scalability"


def _format_run_index(run_index: int) -> str:
    if run_index < 1:
        raise ValueError("run_index must be >= 1")
    if run_index <= 999999:
        return f"{run_index:06d}"
    return str(run_index)


def _validate_session_id(session_id: str) -> str:
    value = str(session_id).strip()
    if not SESSION_ID_PATTERN.match(value):
        raise ValueError("session_id must match ^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
    return value


def run_paths(session_id: str, run_index: int, version: str) -> dict:
    sid = _validate_session_id(session_id)
    index_str = _format_run_index(run_index)
    runs_dir = local_scalability_root() / "sessions" / sid / "runs"
    filename_base = f"{index_str}__scalability_check__{version}"
    return {
        "runs_dir": runs_dir,
        "json_path": runs_dir / f"{filename_base}.json",
        "md_path": runs_dir / f"{filename_base}.md",
    }


def write_report_files(report: dict, markdown: str, session_id: str, run_index: int, version: str) -> dict:
    paths = run_paths(session_id, run_index, version)
    runs_dir = paths["runs_dir"]
    json_path = paths["json_path"]
    md_path = paths["md_path"]
    runs_dir.mkdir(parents=True, exist_ok=True)

    if json_path.exists() or md_path.exists():
        raise ValueError("scalability report identity already exists")

    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")

    return {
        "json_path": str(json_path),
        "md_path": str(md_path),
        "runs_dir": str(runs_dir),
    }

