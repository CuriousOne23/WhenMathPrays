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


def main() -> None:
    proposal_path = ROOT / "support" / "scalability" / "examples" / "proposal_seed_generalized.yaml"
    session_id = "scale_seed_hold"
    _cleanup(session_id)
    try:
        result = run_scalability_check(
            proposal_file=str(proposal_path),
            session_id=session_id,
            run_index=1,
            report_version="1.0",
            run_regression=False,
        )
        report = result["report"]
        assert report.get("disposition", {}).get("disposition") == "HOLD"
        obligations = report.get("progression_obligations", [])
        assert any(item.get("obligation_type") == "seed_generalization_unresolved" for item in obligations)
        quals = report.get("qualification", [])
        assert quals and all(item.get("qualification_state") == "unresolved" for item in quals)
    finally:
        _cleanup(session_id)

    print("scalability seed hold replay passed")


if __name__ == "__main__":
    main()

