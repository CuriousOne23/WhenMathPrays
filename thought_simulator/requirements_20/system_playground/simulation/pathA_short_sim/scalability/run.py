from __future__ import annotations

from typing import Any, Dict

from scalability.dependencies import evaluate_dependencies
from scalability.discovery import discover_environment
from scalability.disposition import determine_disposition
from scalability.obligations import compute_obligations
from scalability.proposal import load_proposal
from scalability.qualification import determine_qualification
from scalability.regression import run_regression_checks
from scalability.relationships import classify_items
from scalability.report import build_markdown, build_report
from scalability.session_store import write_report_files


def run_scalability_check(
    proposal_file: str,
    session_id: str,
    run_index: int,
    report_version: str = "1.0",
    run_regression: bool = False,
) -> Dict[str, Any]:
    proposal = load_proposal(proposal_file)
    discovered = discover_environment()

    items = proposal.get("items", [])
    classifications = classify_items(items, discovered)
    dependencies = evaluate_dependencies(items, discovered)
    obligations = compute_obligations(items, classifications, dependencies, discovered)
    qualification = determine_qualification(obligations)
    regression = run_regression_checks(run_regression)
    disposition = determine_disposition(classifications, dependencies, qualification, regression)

    report = build_report(
        proposal=proposal,
        session_id=session_id,
        run_index=run_index,
        version=report_version,
        classifications=classifications,
        dependencies=dependencies,
        obligations=obligations,
        qualifications=qualification,
        regression=regression,
        disposition=disposition,
    )
    markdown = build_markdown(report)
    output = write_report_files(report, markdown, session_id, run_index, report_version)

    return {
        "report": report,
        "output": output,
    }

