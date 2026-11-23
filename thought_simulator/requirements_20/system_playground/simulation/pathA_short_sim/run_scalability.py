from __future__ import annotations

import argparse
import json
from pathlib import Path

from scalability.run import run_scalability_check


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run bounded Path A scalability analysis")
    parser.add_argument("--proposal-file", required=True, help="Path to proposal YAML")
    parser.add_argument("--session-id", required=True, help="Scalability session id")
    parser.add_argument("--run-index", type=int, required=True, help="Scalability run index (>=1)")
    parser.add_argument("--report-version", default="1.0", help="Provisional report version")
    parser.add_argument(
        "--run-regression",
        action="store_true",
        help="Run reused regression/replay checks as part of scalability report",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    proposal_file = Path(args.proposal_file)
    if not proposal_file.exists():
        raise SystemExit(f"proposal_file_not_found: {proposal_file}")

    result = run_scalability_check(
        proposal_file=str(proposal_file),
        session_id=str(args.session_id),
        run_index=int(args.run_index),
        report_version=str(args.report_version),
        run_regression=bool(args.run_regression),
    )

    disposition = (result.get("report", {}) or {}).get("disposition", {})
    print("=== SCALABILITY TRACE ===")
    print(
        "status=success session_id={session_id} run_index={run_index} proposal_id={proposal_id} disposition={disposition}".format(
            session_id=result["report"]["identity"]["session_id"],
            run_index=result["report"]["identity"]["run_index"],
            proposal_id=result["report"]["identity"]["proposal_id"],
            disposition=disposition.get("disposition"),
        )
    )
    print("json_report={}".format(result["output"]["json_path"]))
    print("md_report={}".format(result["output"]["md_path"]))
    print(json.dumps(disposition, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

