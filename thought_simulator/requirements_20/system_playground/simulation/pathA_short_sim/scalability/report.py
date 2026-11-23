from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_findings(
    classifications: List[Dict[str, Any]],
    dependencies: List[Dict[str, Any]],
    obligations: List[Dict[str, Any]],
    qualifications: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    dependency_by_item = {str(item.get("item_id")): item for item in dependencies}
    qualification_by_source: Dict[str, List[Dict[str, Any]]] = {}
    for qual in qualifications:
        source = str(qual.get("source_item_id"))
        qualification_by_source.setdefault(source, []).append(qual)

    findings: List[Dict[str, Any]] = []
    for classified in classifications:
        item_id = str(classified.get("item_id"))
        deps = dependency_by_item.get(item_id, {})
        related_obligations = [item for item in obligations if str(item.get("source_item_id")) == item_id]
        related_quals = qualification_by_source.get(item_id, [])
        findings.append(
            {
                "origin": {"item_id": item_id, "resource_class": classified.get("resource_class")},
                "where": {"surface": classified.get("resource_class"), "identity": classified.get("identity")},
                "what": {
                    "classification": classified.get("classification"),
                    "dependency_status": "missing" if deps.get("has_missing_dependencies") else "satisfied_or_not_applicable",
                    "obligation_count": len(related_obligations),
                },
                "why": {"rule_basis": classified.get("reason")},
                "evidence": {
                    "missing_dependencies": deps.get("missing_dependencies", []),
                    "obligations": related_obligations,
                    "qualification_states": related_quals,
                },
                "consequence": {
                    "progression_requires_followup": bool(related_obligations),
                    "qualification_unresolved": any(str(item.get("qualification_state")) == "unresolved" for item in related_quals),
                },
                "route": {},
            }
        )
    return findings


def build_report(
    proposal: Dict[str, Any],
    session_id: str,
    run_index: int,
    version: str,
    classifications: List[Dict[str, Any]],
    dependencies: List[Dict[str, Any]],
    obligations: List[Dict[str, Any]],
    qualifications: List[Dict[str, Any]],
    regression: Dict[str, Any],
    disposition: Dict[str, Any],
) -> Dict[str, Any]:
    findings = build_findings(classifications, dependencies, obligations, qualifications)
    return {
        "scalability_report_version": version,
        "created_at_utc": _utc_now(),
        "identity": {
            "session_id": session_id,
            "run_index": run_index,
            "proposal_id": proposal.get("proposal_id"),
            "scalability_type": "scalability_check",
        },
        "proposal": {
            "proposal_id": proposal.get("proposal_id"),
            "item_count": len(proposal.get("items", [])),
            "items": proposal.get("items", []),
        },
        "relationships": classifications,
        "dependencies": dependencies,
        "progression_obligations": obligations,
        "qualification": qualifications,
        "regression": regression,
        "findings": findings,
        "disposition": disposition,
    }


def build_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Scalability Check Report")
    lines.append("")
    lines.append(f"- proposal_id: {report.get('identity', {}).get('proposal_id')}")
    lines.append(f"- session_id: {report.get('identity', {}).get('session_id')}")
    lines.append(f"- run_index: {report.get('identity', {}).get('run_index')}")
    lines.append(f"- created_at_utc: {report.get('created_at_utc')}")
    lines.append("")
    disposition = report.get("disposition", {})
    lines.append("## Disposition")
    lines.append("")
    lines.append(f"- disposition: {disposition.get('disposition')}")
    lines.append(f"- reason: {disposition.get('reason')}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- items: {len(report.get('proposal', {}).get('items', []))}")
    lines.append(f"- obligations: {len(report.get('progression_obligations', []))}")
    lines.append(f"- regression_status: {report.get('regression', {}).get('status')}")
    return "\n".join(lines) + "\n"

