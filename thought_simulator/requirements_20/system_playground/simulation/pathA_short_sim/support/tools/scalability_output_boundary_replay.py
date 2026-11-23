from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scalability.run import run_scalability_check


ESTABLISHED_SURFACES = [
    ROOT / "support" / "dictionaries" / "category_cues.yaml",
    ROOT / "s2m" / "data" / "majors.yaml",
    ROOT / "s2m" / "data" / "spaces" / "default.yaml",
    ROOT / "s2m" / "data" / "associations" / "blue.yaml",
    ROOT / "s2m" / "data" / "associations" / "book.yaml",
    ROOT / "s2m" / "data" / "associations" / "table.yaml",
    ROOT / "s2m" / "data" / "associations" / "sky.yaml",
    ROOT / "s2m" / "data" / "associations" / "query_location.yaml",
]


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _cleanup(session_id: str) -> None:
    shutil.rmtree(ROOT / "local_scalability" / "sessions" / session_id, ignore_errors=True)


def _git_ignored(path: Path) -> bool:
    repo_root = ROOT.parents[4]
    result = subprocess.run(
        ["git", "--no-pager", "check-ignore", str(path)],
        cwd=str(repo_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode == 0


def main() -> None:
    before = {str(path): _digest(path) for path in ESTABLISHED_SURFACES}

    proposal_path = ROOT / "support" / "scalability" / "examples" / "proposal_association_add.yaml"
    session_id = "scale_output_boundary"
    _cleanup(session_id)
    try:
        result = run_scalability_check(
            proposal_file=str(proposal_path),
            session_id=session_id,
            run_index=1,
            report_version="1.0",
            run_regression=False,
        )
        json_report = Path(result["output"]["json_path"])
        md_report = Path(result["output"]["md_path"])
        assert json_report.exists()
        assert md_report.exists()
        assert _git_ignored(json_report), "json report should be git-ignored"
        assert _git_ignored(md_report), "markdown report should be git-ignored through local_scalability rule"
    finally:
        _cleanup(session_id)

    after = {str(path): _digest(path) for path in ESTABLISHED_SURFACES}
    assert before == after, "proposal run must not modify established Path A resources"
    print("scalability output boundary replay passed")


if __name__ == "__main__":
    main()

