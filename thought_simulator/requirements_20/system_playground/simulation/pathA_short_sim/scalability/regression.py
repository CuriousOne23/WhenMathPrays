from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]


def _run_script(path: Path) -> Dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(path)],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return {
        "script": str(path.relative_to(ROOT)).replace("\\", "/"),
        "exit_code": int(completed.returncode),
        "passed": completed.returncode == 0,
        "output_tail": (completed.stdout or "").splitlines()[-30:],
    }


def run_regression_checks(enabled: bool) -> Dict[str, Any]:
    if not enabled:
        return {"status": "not-run", "checks": [], "passed": None}

    checks: List[Dict[str, Any]] = []
    for relative in [
        Path("support/tools/pipeline_readiness_check.py"),
        Path("support/tools/s2m_category_selection_replay.py"),
    ]:
        checks.append(_run_script(ROOT / relative))

    passed = all(bool(item.get("passed")) for item in checks)
    return {
        "status": "pass" if passed else "fail",
        "checks": checks,
        "passed": passed,
    }

