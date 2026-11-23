from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scalability.run import run_scalability_check


def _cleanup(session_id: str) -> None:
    shutil.rmtree(ROOT / "local_scalability" / "sessions" / session_id, ignore_errors=True)


def _run_example(file_name: str, session_id: str, run_index: int) -> dict:
    proposal_path = ROOT / "support" / "scalability" / "examples" / file_name
    _cleanup(session_id)
    try:
        return run_scalability_check(
            proposal_file=str(proposal_path),
            session_id=session_id,
            run_index=run_index,
            report_version="1.0",
            run_regression=False,
        )
    finally:
        _cleanup(session_id)


def main() -> None:
    # already_defined must stay distinct and produce no progression obligations
    already = _run_example("proposal_already_defined.yaml", "scale_prop_defined", 1)
    already_report = already["report"]
    relationships = already_report.get("relationships", [])
    assert relationships and relationships[0].get("classification") == "already_defined"
    assert already_report.get("progression_obligations") == []

    # extension_of must remain distinct from already_defined
    ext = _run_example("proposal_dict_extension.yaml", "scale_prop_extension", 1)
    ext_report = ext["report"]
    ext_relationships = ext_report.get("relationships", [])
    assert ext_relationships and ext_relationships[0].get("classification") == "extension_of"
    assert ext_report.get("progression_obligations"), "extension_of should create progression obligations"

    print("scalability proposal replay passed")


if __name__ == "__main__":
    main()

