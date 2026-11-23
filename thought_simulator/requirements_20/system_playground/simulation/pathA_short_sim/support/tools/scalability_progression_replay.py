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
    # new dictionary mapping should produce progression obligation and unresolved qualification
    dict_new = _run_example("proposal_dict_new_mapping.yaml", "scale_prog_dict", 1)["report"]
    assert dict_new.get("progression_obligations"), "expected obligations for new dictionary mapping"
    assert dict_new.get("regression", {}).get("status") == "not-run"
    quals = dict_new.get("qualification", [])
    assert quals and all(item.get("qualification_state") == "unresolved" for item in quals)

    # association addition should enumerate derived candidate obligation
    assoc = _run_example("proposal_association_add.yaml", "scale_prog_assoc", 1)["report"]
    candidate_obligations = [
        item for item in assoc.get("progression_obligations", [])
        if item.get("resource_class") == "candidate"
    ]
    assert candidate_obligations, "expected derived candidate obligations from association expansion"

    # major addition should show eligibility consequence obligation
    major = _run_example("proposal_major_add.yaml", "scale_prog_major", 1)["report"]
    major_obligations = [
        item for item in major.get("progression_obligations", [])
        if item.get("obligation_type") == "major_eligibility_change"
    ]
    assert major_obligations, "expected major eligibility obligation for new major"

    print("scalability progression replay passed")


if __name__ == "__main__":
    main()

