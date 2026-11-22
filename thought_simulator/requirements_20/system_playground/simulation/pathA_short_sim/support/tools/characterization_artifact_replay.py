"""Batch 3A focused verification for characterization artifact persistence."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from characterization import artifacts  # noqa: E402


def _make_runtime_provided() -> Dict[str, Any]:
    return {
        "final_tp.truth_relation": {
            "provenance": "runtime_provided",
            "source_path": "controlled.final_tp.truth_relation",
            "value": "is",
        },
        "trace.primitive_sequence": {
            "provenance": "runtime_provided",
            "source_path": "controlled.trace[*].primitive",
            "value": ["InB", "IE", "SmOB", "IdOB"],
        },
    }


def _make_unavailable() -> Dict[str, Any]:
    return {
        "entropy": {
            "provenance": "unavailable",
            "reason": "milestone1_unavailable",
        },
        "top_vs_second_margin": {
            "provenance": "unavailable",
            "reason": "milestone1_unavailable",
        },
    }


def _make_envelope(session_id: str, run_index: int, char_type: str, char_version: str) -> Dict[str, Any]:
    return artifacts.build_success_envelope(
        char_type=char_type,
        char_version=char_version,
        session_id=session_id,
        run_index=run_index,
        source_runtime_flags={
            "execution_case": "sky_blue",
            "enable_category_selection": True,
            "enable_s2m_seed": False,
            "show_category_observations": False,
        },
        runtime_provided_observations=_make_runtime_provided(),
        unavailable_observations=_make_unavailable(),
        resolved_type_parameters={},
        entrypoint="run_examples.py",
    )


def _git_check_ignore(path: Path) -> bool:
    repo_root = ROOT.parents[4]
    result = subprocess.run(
        ["git", "--no-pager", "check-ignore", str(path)],
        cwd=str(repo_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode == 0


def _cleanup_tool_owned_paths(sessions_root: Path, test_sessions: list[str], probe_session: str) -> None:
    for session_id in test_sessions:
        shutil.rmtree(sessions_root / session_id, ignore_errors=True)
    shutil.rmtree(sessions_root / probe_session, ignore_errors=True)


def main() -> None:
    base_root = ROOT / "local_characterization"
    sessions_root = base_root / "sessions"
    test_sessions = [
        "batch3a_env",
        "batch3a_dup",
        "batch3a_race",
        "batch3a_fail",
    ]
    probe_session = "__batch3a_probe__"

    try:
        _cleanup_tool_owned_paths(sessions_root, test_sessions, probe_session)

        results: Dict[str, Any] = {}

        # 1/7/8/9 envelope + deterministic path formatting
        env = _make_envelope("batch3a_env", 42, "infra_smoke", "1.0")
        path_42 = artifacts.intended_artifact_path("batch3a_env", 42, "infra_smoke", "1.0", base_root)
        path_big = artifacts.intended_artifact_path("batch3a_env", 1000000, "infra_smoke", "1.0", base_root)
        results["envelope_schema_ok"] = env["schema_id"] == artifacts.SCHEMA_ID and env["schema_version"] == artifacts.SCHEMA_VERSION
        results["entropy_unavailable"] = env["unavailable_observations"]["entropy"]["provenance"] == "unavailable"
        results["margin_unavailable"] = env["unavailable_observations"]["top_vs_second_margin"]["provenance"] == "unavailable"
        results["no_derived_measurements"] = "characterization_derived_observations" not in env
        results["path_has_6pad"] = "000042__infra_smoke__1.0.tschar.json" in str(path_42)
        results["path_over_6digits"] = "1000000__infra_smoke__1.0.tschar.json" in str(path_big)
        env_write = artifacts.persist_success_envelope(env, base_root)
        results["env_write_success"] = env_write["ok"] and env_write["status_code"] == artifacts.SUCCESS_CODE

        # 11 os.link probe (before relying on it in report)
        probe = artifacts.probe_os_link_no_overwrite(base_root)
        results["probe_success_link_created"] = probe["success_link_created"]
        results["probe_collision_has_exception"] = probe["collision_exception_type"] is not None
        results["probe_collision_preserved_existing"] = probe["collision_preserved_existing_content"]
        results["probe_cleanup_ok"] = probe["cleanup_removed_probe_files"]
        results["probe_collision_exception_type"] = probe["collision_exception_type"]
        results["probe_collision_exception_message"] = probe["collision_exception_message"]

        # 13 hard non-overwrite + writer return contract
        first = artifacts.persist_success_envelope(_make_envelope("batch3a_dup", 1, "infra_smoke", "1.0"), base_root)
        first_path = Path(str(first["committed_final_path"])) if first["committed_final_path"] else None
        first_content = first_path.read_text(encoding="utf-8") if first_path is not None and first_path.exists() else ""
        second_same = artifacts.persist_success_envelope(_make_envelope("batch3a_dup", 1, "infra_smoke", "1.0"), base_root)
        second_diff_type = artifacts.persist_success_envelope(_make_envelope("batch3a_dup", 1, "infra_probe", "2.0"), base_root)
        preserved_content = first_path.read_text(encoding="utf-8") if first_path is not None and first_path.exists() else ""
        results["first_write_success"] = first["ok"] and first["status_code"] == artifacts.SUCCESS_CODE
        results["duplicate_conflict"] = (not second_same["ok"]) and second_same["status_code"] == artifacts.IDENTITY_CONFLICT_CODE
        results["diff_type_same_identity_conflict"] = (not second_diff_type["ok"]) and second_diff_type["status_code"] == artifacts.IDENTITY_CONFLICT_CODE
        results["existing_content_unchanged_after_conflict"] = first_content == preserved_content
        results["success_returns_committed_path"] = bool(first.get("committed_final_path"))
        results["failed_returns_null_committed_path"] = second_same.get("committed_final_path") is None
        results["canonical_duplicate_detection"] = artifacts.has_canonical_identity_conflict("batch3a_dup", 1, base_root)

        # 14 simulated race-time collision (pre-check passes, final placement collides)
        original_final_place = artifacts._final_place_with_hard_no_overwrite  # type: ignore[attr-defined]
        sentinel_path = artifacts.intended_artifact_path("batch3a_race", 2, "infra_smoke", "1.0", base_root)
        sentinel_payload = json.dumps({"sentinel": "race_winner"}, indent=2)

        def _race_injector(temp_path: Path, final_path: Path) -> None:
            final_path.parent.mkdir(parents=True, exist_ok=True)
            final_path.write_text(sentinel_payload, encoding="utf-8")
            original_final_place(temp_path, final_path)

        artifacts._final_place_with_hard_no_overwrite = _race_injector  # type: ignore[attr-defined]
        try:
            race_result = artifacts.persist_success_envelope(_make_envelope("batch3a_race", 2, "infra_smoke", "1.0"), base_root)
        finally:
            artifacts._final_place_with_hard_no_overwrite = original_final_place  # type: ignore[attr-defined]
        sentinel_unchanged = sentinel_path.exists() and sentinel_path.read_text(encoding="utf-8") == sentinel_payload
        results["race_collision_failed"] = (not race_result["ok"]) and race_result["status_code"] == artifacts.IDENTITY_CONFLICT_CODE
        results["race_collision_preserved_sentinel"] = sentinel_unchanged

        # 15 failure and cleanup checks
        bad_envelope = _make_envelope("batch3a_fail", 3, "infra_smoke", "1.0")
        bad_envelope["runtime_provided_observations"]["bad"] = {"value": set([1])}  # non-serializable
        serial_fail = artifacts.persist_success_envelope(bad_envelope, base_root)
        serial_final = artifacts.intended_artifact_path("batch3a_fail", 3, "infra_smoke", "1.0", base_root)
        results["serialization_failure_status"] = (not serial_fail["ok"]) and serial_fail["status_code"] == artifacts.PERSIST_FAILED_CODE
        results["serialization_failure_no_final"] = not serial_final.exists()

        original_write_temp = artifacts._write_temp_file  # type: ignore[attr-defined]

        def _failing_temp_writer(_runs_dir: Path, _serialized_json: str) -> Path:
            raise OSError("simulated_temp_creation_failure")

        artifacts._write_temp_file = _failing_temp_writer  # type: ignore[attr-defined]
        try:
            temp_fail = artifacts.persist_success_envelope(_make_envelope("batch3a_fail", 4, "infra_smoke", "1.0"), base_root)
        finally:
            artifacts._write_temp_file = original_write_temp  # type: ignore[attr-defined]
        temp_fail_final = artifacts.intended_artifact_path("batch3a_fail", 4, "infra_smoke", "1.0", base_root)
        results["temp_failure_status"] = (not temp_fail["ok"]) and temp_fail["status_code"] == artifacts.PERSIST_FAILED_CODE
        results["temp_failure_no_final"] = not temp_fail_final.exists()

        # 19 git-ignore behavior
        git_check_session = "batch3a_env"
        existing_artifact = artifacts.intended_artifact_path(git_check_session, 42, "infra_smoke", "1.0", base_root)
        temp_candidate = existing_artifact.parent / ".tmp__char__manual__ignorecheck.tmp"
        temp_candidate.parent.mkdir(parents=True, exist_ok=True)
        temp_candidate.write_text("tmp", encoding="utf-8")
        local_gitignore = base_root / ".gitignore"
        results["gitignore_tschar_ignored"] = _git_check_ignore(existing_artifact)
        results["gitignore_temp_ignored"] = _git_check_ignore(temp_candidate)
        results["gitignore_local_gitignore_tracked"] = not _git_check_ignore(local_gitignore)
        temp_candidate.unlink(missing_ok=True)

        # 13/15 parse validation on committed artifact
        parsed = json.loads(existing_artifact.read_text(encoding="utf-8"))
        results["artifact_parses_json"] = isinstance(parsed, dict)
        results["artifact_identity_matches"] = parsed.get("identity", {}).get("session_id") == "batch3a_env" and parsed.get("identity", {}).get("run_index") == 42
        results["artifact_characterization_matches"] = parsed.get("characterization", {}).get("type") == "infra_smoke" and parsed.get("characterization", {}).get("version") == "1.0"
    finally:
        _cleanup_tool_owned_paths(sessions_root, test_sessions, probe_session)

    results["cleanup_removed_test_sessions"] = all(not (sessions_root / sid).exists() for sid in test_sessions)
    results["cleanup_removed_probe_session"] = not (sessions_root / probe_session).exists()

    print(json.dumps(results, indent=2, sort_keys=True))

    must_be_true = [
        "envelope_schema_ok",
        "entropy_unavailable",
        "margin_unavailable",
        "no_derived_measurements",
        "path_has_6pad",
        "path_over_6digits",
        "env_write_success",
        "probe_success_link_created",
        "probe_collision_has_exception",
        "probe_collision_preserved_existing",
        "probe_cleanup_ok",
        "first_write_success",
        "duplicate_conflict",
        "diff_type_same_identity_conflict",
        "existing_content_unchanged_after_conflict",
        "success_returns_committed_path",
        "failed_returns_null_committed_path",
        "canonical_duplicate_detection",
        "race_collision_failed",
        "race_collision_preserved_sentinel",
        "serialization_failure_status",
        "serialization_failure_no_final",
        "temp_failure_status",
        "temp_failure_no_final",
        "gitignore_tschar_ignored",
        "gitignore_temp_ignored",
        "gitignore_local_gitignore_tracked",
        "artifact_parses_json",
        "artifact_identity_matches",
        "artifact_characterization_matches",
        "cleanup_removed_test_sessions",
        "cleanup_removed_probe_session",
    ]
    failed = [key for key in must_be_true if not results.get(key)]
    if failed:
        print("batch3a replay failed checks: {}".format(", ".join(failed)))
        raise SystemExit(2)

    print("characterization artifacts batch3a replay passed")


if __name__ == "__main__":
    main()
