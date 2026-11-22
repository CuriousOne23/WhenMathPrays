"""Milestone-1 characterization artifact envelope + persistence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
import json
import os
import secrets
import tempfile


SCHEMA_ID = "ts.characterization.run"
SCHEMA_VERSION = "1.0"
WRITER_VERSION = "1.0"
SUCCESS_CODE = "success"
PERSIST_FAILED_CODE = "char_persist_failed"
IDENTITY_CONFLICT_CODE = "char_identity_conflict"


@dataclass
class ArtifactPersistResult(object):
    ok: bool
    status_code: str
    intended_final_path: Optional[str]
    committed_final_path: Optional[str]
    message: str
    detail: Optional[Dict[str, Any]] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "status_code": self.status_code,
            "intended_final_path": self.intended_final_path,
            "committed_final_path": self.committed_final_path,
            "message": self.message,
            "detail": self.detail or {},
        }


def _path_a_short_root() -> Path:
    return Path(__file__).resolve().parents[1]


def local_characterization_root(base_root: Optional[Path] = None) -> Path:
    if base_root is not None:
        return Path(base_root)
    return _path_a_short_root() / "local_characterization"


def _format_run_index(run_index: int) -> str:
    if not isinstance(run_index, int) or run_index < 1:
        raise ValueError("run_index must be an integer >= 1")
    if run_index <= 999999:
        return "{:06d}".format(run_index)
    return str(run_index)


def _run_filename(run_index: int, char_type: str, char_version: str) -> str:
    return "{}__{}__{}.tschar.json".format(
        _format_run_index(run_index),
        str(char_type),
        str(char_version),
    )


def runs_directory(session_id: str, base_root: Optional[Path] = None) -> Path:
    session = str(session_id)
    if not session:
        raise ValueError("session_id must not be empty")
    return local_characterization_root(base_root) / "sessions" / session / "runs"


def intended_artifact_path(
    session_id: str,
    run_index: int,
    char_type: str,
    char_version: str,
    base_root: Optional[Path] = None,
) -> Path:
    return runs_directory(session_id, base_root) / _run_filename(run_index, char_type, char_version)


def find_existing_canonical_identity_artifact(
    session_id: str,
    run_index: int,
    base_root: Optional[Path] = None,
) -> Optional[Path]:
    runs_dir = runs_directory(session_id, base_root)
    if not runs_dir.exists():
        return None
    pattern = "{}__*.tschar.json".format(_format_run_index(run_index))
    existing = sorted(runs_dir.glob(pattern))
    for path in existing:
        if path.is_file():
            return path
    return None


def has_canonical_identity_conflict(
    session_id: str,
    run_index: int,
    base_root: Optional[Path] = None,
) -> bool:
    return find_existing_canonical_identity_artifact(session_id, run_index, base_root) is not None


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_success_envelope(
    char_type: str,
    char_version: str,
    session_id: str,
    run_index: int,
    source_runtime_flags: Dict[str, Any],
    runtime_provided_observations: Dict[str, Any],
    unavailable_observations: Dict[str, Any],
    resolved_type_parameters: Optional[Dict[str, Any]] = None,
    entrypoint: str = "run_examples.py",
    created_at_utc: Optional[str] = None,
) -> Dict[str, Any]:
    if resolved_type_parameters is None:
        resolved_type_parameters = {}
    created_at = created_at_utc or _iso_utc_now()
    envelope = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "characterization": {
            "type": str(char_type),
            "version": str(char_version),
        },
        "identity": {
            "session_id": str(session_id),
            "run_index": int(run_index),
        },
        "execution_status": "succeeded",
        "resolved_common_controls": {
            "characterize": True,
            "char_type": str(char_type),
            "char_session_id": str(session_id),
            "char_run_index": int(run_index),
            "char_version": str(char_version),
        },
        "resolved_type_parameters": dict(resolved_type_parameters),
        "source_metadata": {
            "entrypoint": str(entrypoint),
            "runtime_flags": dict(source_runtime_flags),
        },
        "characterization_payload": {
            "infra_smoke": {
                "observation_contract_version": "1.0",
            }
        },
        "runtime_provided_observations": dict(runtime_provided_observations),
        "unavailable_observations": dict(unavailable_observations),
        "artifact_metadata": {
            "created_at_utc": str(created_at),
            "writer_version": WRITER_VERSION,
        },
    }
    return envelope


def _validate_envelope_identity(
    envelope: Dict[str, Any],
    session_id: str,
    run_index: int,
    char_type: str,
    char_version: str,
) -> None:
    if envelope.get("schema_id") != SCHEMA_ID:
        raise ValueError("schema_id mismatch")
    if envelope.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("schema_version mismatch")
    if envelope.get("execution_status") != "succeeded":
        raise ValueError("execution_status must be succeeded")

    identity = envelope.get("identity", {})
    if not isinstance(identity, dict):
        raise ValueError("identity section missing")
    if identity.get("session_id") != session_id:
        raise ValueError("identity.session_id mismatch")
    if identity.get("run_index") != run_index:
        raise ValueError("identity.run_index mismatch")

    characterization = envelope.get("characterization", {})
    if not isinstance(characterization, dict):
        raise ValueError("characterization section missing")
    if characterization.get("type") != char_type:
        raise ValueError("characterization.type mismatch")
    if characterization.get("version") != char_version:
        raise ValueError("characterization.version mismatch")


def _write_temp_file(runs_dir: Path, serialized_json: str) -> Path:
    runs_dir.mkdir(parents=True, exist_ok=True)
    pid = os.getpid()
    nonce = secrets.token_hex(8)
    temp_name = ".tmp__char__{}__{}.tmp".format(pid, nonce)
    temp_path = runs_dir / temp_name

    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(str(temp_path), flags)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(serialized_json)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        raise
    return temp_path


def _validate_temp_content(
    temp_path: Path,
    session_id: str,
    run_index: int,
    char_type: str,
    char_version: str,
) -> Dict[str, Any]:
    with temp_path.open("r", encoding="utf-8") as handle:
        parsed = json.load(handle)
    if not isinstance(parsed, dict):
        raise ValueError("serialized envelope must decode to an object")
    _validate_envelope_identity(parsed, session_id, run_index, char_type, char_version)
    return parsed


def _final_place_with_hard_no_overwrite(temp_path: Path, final_path: Path) -> None:
    os.link(str(temp_path), str(final_path))


def _best_effort_remove(path: Path) -> None:
    try:
        if path.exists():
            path.unlink()
    except OSError:
        pass


def persist_success_envelope(
    envelope: Dict[str, Any],
    base_root: Optional[Path] = None,
) -> Dict[str, Any]:
    intended: Optional[Path] = None
    temp_path: Optional[Path] = None
    try:
        identity = envelope.get("identity", {}) if isinstance(envelope, dict) else {}
        characterization = envelope.get("characterization", {}) if isinstance(envelope, dict) else {}
        if not isinstance(identity, dict) or not isinstance(characterization, dict):
            raise ValueError("envelope identity/characterization sections are required")

        session_id = str(identity.get("session_id"))
        run_index = int(identity.get("run_index"))
        char_type = str(characterization.get("type"))
        char_version = str(characterization.get("version"))

        intended = intended_artifact_path(session_id, run_index, char_type, char_version, base_root)
        intended_str = str(intended)

        existing = find_existing_canonical_identity_artifact(session_id, run_index, base_root)
        if existing is not None:
            return ArtifactPersistResult(
                ok=False,
                status_code=IDENTITY_CONFLICT_CODE,
                intended_final_path=intended_str,
                committed_final_path=None,
                message="canonical identity already exists",
                detail={"existing_artifact_path": str(existing)},
            ).as_dict()

        serialized = json.dumps(envelope, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
        temp_path = _write_temp_file(intended.parent, serialized)
        _validate_temp_content(temp_path, session_id, run_index, char_type, char_version)

        try:
            _final_place_with_hard_no_overwrite(temp_path, intended)
        except FileExistsError:
            existing_now = find_existing_canonical_identity_artifact(session_id, run_index, base_root)
            return ArtifactPersistResult(
                ok=False,
                status_code=IDENTITY_CONFLICT_CODE,
                intended_final_path=intended_str,
                committed_final_path=None,
                message="canonical identity collision during final placement",
                detail={"existing_artifact_path": str(existing_now) if existing_now is not None else None},
            ).as_dict()

        if not intended.exists():
            raise IOError("final artifact missing after placement")

        _best_effort_remove(temp_path)
        return ArtifactPersistResult(
            ok=True,
            status_code=SUCCESS_CODE,
            intended_final_path=intended_str,
            committed_final_path=str(intended),
            message="artifact committed",
        ).as_dict()
    except Exception as exc:
        _best_effort_remove(temp_path) if temp_path is not None else None
        return ArtifactPersistResult(
            ok=False,
            status_code=PERSIST_FAILED_CODE,
            intended_final_path=str(intended) if intended is not None else None,
            committed_final_path=None,
            message="artifact persistence failed",
            detail={"error_type": exc.__class__.__name__, "error": str(exc)},
        ).as_dict()


def probe_os_link_no_overwrite(base_root: Optional[Path] = None) -> Dict[str, Any]:
    root = local_characterization_root(base_root)
    probe_dir = root / "sessions" / "__batch3a_probe__" / "runs"
    probe_dir.mkdir(parents=True, exist_ok=True)

    src = probe_dir / ".tmp__char__probe_src.tmp"
    dst = probe_dir / "000001__probe__1.0.tschar.json"
    src2 = probe_dir / ".tmp__char__probe_src2.tmp"
    existing = probe_dir / "000002__probe__1.0.tschar.json"

    _best_effort_remove(src)
    _best_effort_remove(dst)
    _best_effort_remove(src2)
    _best_effort_remove(existing)

    src_payload = '{"probe":"source"}\n'
    src.write_text(src_payload, encoding="utf-8")
    with src.open("r+", encoding="utf-8") as handle:
        handle.flush()
        os.fsync(handle.fileno())
    os.link(str(src), str(dst))
    success_final_exists = dst.exists()
    success_content_match = dst.read_text(encoding="utf-8") == src_payload

    sentinel_payload = '{"probe":"sentinel"}\n'
    existing.write_text(sentinel_payload, encoding="utf-8")
    src2.write_text('{"probe":"collision"}\n', encoding="utf-8")
    with src2.open("r+", encoding="utf-8") as handle:
        handle.flush()
        os.fsync(handle.fileno())

    collision_exception: Optional[Exception] = None
    try:
        os.link(str(src2), str(existing))
    except Exception as exc:
        collision_exception = exc

    sentinel_unchanged = existing.read_text(encoding="utf-8") == sentinel_payload

    _best_effort_remove(src)
    _best_effort_remove(dst)
    _best_effort_remove(src2)
    _best_effort_remove(existing)

    return {
        "success_link_created": success_content_match,
        "success_final_exists": success_final_exists,
        "collision_exception_type": collision_exception.__class__.__name__ if collision_exception is not None else None,
        "collision_exception_message": str(collision_exception) if collision_exception is not None else None,
        "collision_preserved_existing_content": sentinel_unchanged,
        "cleanup_removed_probe_files": not src.exists() and not dst.exists() and not src2.exists() and not existing.exists(),
    }


__all__ = [
    "SCHEMA_ID",
    "SCHEMA_VERSION",
    "WRITER_VERSION",
    "SUCCESS_CODE",
    "PERSIST_FAILED_CODE",
    "IDENTITY_CONFLICT_CODE",
    "ArtifactPersistResult",
    "local_characterization_root",
    "runs_directory",
    "intended_artifact_path",
    "find_existing_canonical_identity_artifact",
    "has_canonical_identity_conflict",
    "build_success_envelope",
    "persist_success_envelope",
    "probe_os_link_no_overwrite",
]
