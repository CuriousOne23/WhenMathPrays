#!/usr/bin/env python3
"""Repair document paths and stale tokens for blocking CI validators.

Run after fix_post_renumber_residual_refs.py when validate_doc_reference_targets or
validate_readme_links still report failures. Re-runnable; extend TEXT_REPAIRS as needed.
"""

from __future__ import annotations

import re
from pathlib import Path

from identity_tables import ROOT

SKIP_DIRS = frozenset({"archive", "__pycache__", ".git", "node_modules", "00_identity"})
EXTENSIONS = {".md", ".py", ".json", ".yml"}

SCRIPT_NAMES = (
    "validate_30_10_50_pairing.py",
    "validate_doc_naming_prefixes.py",
    "validate_30_inventory_index.py",
    "validate_50_traceability_index.py",
    "validate_20_traceability_matrix.py",
    "validate_name_tables.py",
    "validate_50_glossary_alignment.py",
    "validate_glossary_alignment.py",
    "update_50_glossary.py",
    "rename_identity.py",
    "align_design_numbering.py",
    "apply_40_renumber_migration.py",
    "apply_30_1050_renumber_migration.py",
    "apply_50_renumber_migration.py",
    "fix_40_post_renumber_refs.py",
    "fix_30_1050_post_renumber_refs.py",
    "fix_50_post_renumber_refs.py",
    "fix_post_renumber_residual_refs.py",
    "fix_ci_doc_residuals.py",
    "bootstrap_name_tables.py",
)

TEXT_REPAIRS: list[tuple[str, str]] = [
    ("archive/refactors/archive/refactors/", "archive/refactors/"),
    ("10.50.260_upi_design_requirements", "10.50.90_upi_design_requirements"),
    ("10.50.260_upi", "10.50.90_upi"),
    ("50.220_cob_design_support.md", "50.100_cob_design_support.md"),
    ("50.43_gb_design_decisions.md", "50.130_gb_design_spec.md"),
    ("50.36_gb_design_decisions.md", "50.130_gb_design_spec.md"),
    ("LLR-5020-001", "LLR-50.150-001"),
    ("LLR-50.1500-", "LLR-50.200-"),
    (
        "archive/2026-06-03_layer-cleanup/40.330_math_prototypes/",
        "40_thought_simulator_playground/archive/2026-06-03_layer-cleanup/40.10_math_prototypes/",
    ),

    ("50.31_regulator_design_support.md", "50.220_regulator_design_support.md"),
    ("50.100_tick_cycle_design_support.md", "50.230_tick_cycle_design_support.md"),
    ("50.73_event_log_observability_design.md", "50.250_event_log_observability_design.md"),
    ("50.83_experiment_runner_testing_design.md", "50.260_experiment_runner_testing_design.md"),
    ("50.150_geometry_engine_design.md", "50.270_geometry_engine_design.md"),
    ("50.230_iiinb_design_spec.md", "50.60_iiinb_design_spec.md"),
    ("50.220_inb_design_spec.md", "50.50_inb_design_spec.md"),
    ("50.42.010_data_structures.md", "50.140_core_data_structs_design_spec.md"),
    ("20.57_trigrb_requirements.md", "20.57_trig_rb_semantic_trigger_requirements.md"),
    ("40.20_tp_lifecycle/", "40.160_tp_lifecycle/"),
    ("artifacts/tp_state.json", "tp_state.json"),
    ("tr_verification_run1/2/3_2026-06-03.json", "tr_verification_run1_2026-06-03.json"),
    ("run1/2/3_2026-06-03.json", "artifacts/tr_verification_run1_2026-06-03.json"),
    ("40.270/verification_capsule.md", "../../40_thought_simulator_playground/40.270_scheduler_prototypes/verification_capsule.md"),
    ("40.270/requirements_delta.md", "../../40_thought_simulator_playground/40.270_scheduler_prototypes/requirements_delta.md"),
    ("40.240/software_description.md", "../../40_thought_simulator_playground/40.240_tr_router_prototypes/software_description.md"),
    ("../40.05_master_program_guide.md", "../../40_thought_simulator_playground/40.05_master_program_guide.md"),
    ("artifacts/scheduler_verification_run_2026-06-06.json", "scheduler_verification_run_2026-06-06.json"),
    ("10.10_math_requirements.md", "10_system_architecture/10.10.270_math_requirements.md"),
    ("10.50.310_experiment_runner_requirements", "10.50.260_experiment_runner_requirements"),
    ("10.50.290_snapshot_requirements", "10.50.240_snapshot_requirements"),
    ("10.50.300_event_log_requirements", "10.50.250_event_log_requirements"),
    (
        "../40_thought_simulator_playground/40.350_mb_prototypes/software_description.md",
        "../30_verification/30.200_mb_prototypes/30.200_mb_prototypes_verification_capsule.md",
    ),
    (
        "../40_thought_simulator_playground/40.350_mb_prototypes/prototype.py",
        "../30_verification/30.200_mb_prototypes/30.200_mb_prototypes_verification_capsule.md",
    ),
    (
        "../40_thought_simulator_playground/40.350_mb_prototypes/artifacts/mb_verification_run_2026-06-05.json",
        "../30_verification/30.200_mb_prototypes/mb_verification_run_2026-06-05.json",
    ),
    (
        "adrs/ADR-2026-05-28-40.330-to-40.270-coverage.md",
        "adrs/ADR-2026-05-28-40.10-to-40.40-coverage.md",
    ),
    (
        "VERIFICATION_SYNC_LOG_2026-06-05_30.00-40.240.md",
        "VERIFICATION_SYNC_LOG_2026-06-05_30.00-40.37.md",
    ),
    ("gb_verification_run_2026-06-04.json", "gb_verification_run_2026-06-03.json"),
    (
        "artifacts/inb_verification_run_2026-06-07.json",
        "40.50_inb_prototypes/artifacts/inb_verification_run_2026-06-07.json",
    ),
    (
        "artifacts/tr_verification_run_2026-06-03.json",
        "../artifacts/tr_verification_run1_2026-06-03.json",
    ),
    ("10_thought_simulator_req/../50_design/", "10_thought_simulator_req/50_design/"),
    ("../10_thought_simulator_req/../50_design/", "../10_thought_simulator_req/50_design/"),
    ("../../10_thought_simulator_req/../50_design/", "../../10_thought_simulator_req/50_design/"),
    (
        "thought_simulator/10_thought_simulator_req/../50_design/",
        "thought_simulator/10_thought_simulator_req/50_design/",
    ),
    ("40.50_inb_prototypes/40.50_inb_prototypes/", "40.50_inb_prototypes/"),
    (
        "../../../.github/workflows/../../../.github/workflows/",
        "../../../.github/workflows/",
    ),
    (
        "../10_system_architecture/10.10.270_math_requirements.md",
        "../../50_design/10.50.270_math_requirements.md",
    ),
    (
        "40_thought_simulator_playground/40.160_tp_lifecycle/tp_state.json",
        "40_thought_simulator_playground/40.160_tp_lifecycle/artifacts/tp_state.json",
    ),
    (
        "../40_thought_simulator_playground/40.270_scheduler_prototypes/scheduler_verification_run_2026-06-06.json",
        "../40_thought_simulator_playground/40.270_scheduler_prototypes/artifacts/scheduler_verification_run_2026-06-06.json",
    ),
    (
        "40_thought_simulator_playground/40.270_scheduler_prototypes/scheduler_verification_run_2026-06-06.json",
        "40_thought_simulator_playground/40.270_scheduler_prototypes/artifacts/scheduler_verification_run_2026-06-06.json",
    ),
]

INVENTORY_ROW_REMOVALS = {
    "30_verification/30.01_verification_inventory_index.md": [
        "| [30.150_verification_of_semantic_specification.md](30.150_verification_of_semantic_specification.md) | Semantic specification verification notes |",
        "| [30.160_verification_of_reference_algorithms.md](30.160_verification_of_reference_algorithms.md) | Reference algorithm verification notes |",
        "| [30.210_evidence_trace_exemplars_non_normative.md](30.210_evidence_trace_exemplars_non_normative.md) | Non-normative evidence exemplars |",
    ],
}

BARE_40_MODULE_RE = re.compile(r"(?<![/\w])40\.\d+_[\w]+/")


def _governance_script_prefix(rel: str, text: str) -> str:
    if not rel.startswith("00_program_governance/"):
        return text
    for name in SCRIPT_NAMES:
        text = re.sub(
            rf"(?<![/\w]){re.escape(name)}",
            f"../../scripts/{name}",
            text,
        )
    return text


def _tier_script_prefix(rel: str, text: str) -> str:
    if rel.startswith("50_thought_simulator_design/"):
        text = re.sub(r"(?<!\./)(?<!\.\./)scripts/", "../scripts/", text)
    elif rel.startswith("10_thought_simulator_req/50_design/"):
        text = re.sub(r"(?<!\./)(?<!\.\./)scripts/", "../../scripts/", text)
    return text


def _fix_50_top_level_paths(rel: str, text: str) -> str:
    if not rel.startswith("50_thought_simulator_design/"):
        return text
    if "/" in rel[len("50_thought_simulator_design/") :]:
        return text

    text = text.replace("../../20_requirements/", "../20_requirements/")
    text = text.replace("../../30_verification/", "../30_verification/")
    text = text.replace("../../40_thought_simulator_playground/", "../40_thought_simulator_playground/")
    text = text.replace(
        "../../40.510_refactor.md",
        "../40_thought_simulator_playground/40.510_refactor.md",
    )

    def _prefix_playground(match: re.Match[str]) -> str:
        return f"../40_thought_simulator_playground/{match.group(0)}"

    text = BARE_40_MODULE_RE.sub(_prefix_playground, text)
    return text


def _fix_doc_inventory_paths(rel: str, text: str) -> str:
    if not rel.startswith("10_thought_simulator_req/docs/"):
        return text

    def _prefix_30(match: re.Match[str]) -> str:
        token = match.group(0)
        if token.startswith("../../30_verification/"):
            return token
        return f"../../30_verification/{token}"

    def _prefix_40(match: re.Match[str]) -> str:
        token = match.group(0)
        if token.startswith("../../40_thought_simulator_playground/"):
            return token
        if token.startswith("40_thought_simulator_playground/"):
            return f"../../{token}"
        return f"../../40_thought_simulator_playground/{token}"

    text = re.sub(r"(?<![/\w])30\.\d+_[\w]+/[\w./-]+\.(?:md|json|py)", _prefix_30, text)
    text = re.sub(r"(?<![/\w])40\.\d+_[\w]+/[\w./-]+\.(?:md|json|py)", _prefix_40, text)
    text = re.sub(
        r"(?<![/\w])40\.05_master_program_guide\.md",
        "../../40_thought_simulator_playground/40.05_master_program_guide.md",
        text,
    )
    text = re.sub(
        r"(?<![/\w])glossary_term_registry\.json",
        "../../30_verification/glossary_term_registry.json",
        text,
    )
    text = re.sub(
        r"(?<![/\w])30\.30_verification_glossary\.md",
        "../../30_verification/30.30_verification_glossary.md",
        text,
    )
    return text


def _fix_glossary_contributing(rel: str, text: str) -> str:
    if rel == "50_thought_simulator_design/50.01_50_series_glossary.md":
        text = text.replace(
            "CONTRIBUTING_CHANGE_WORKFLOW.md",
            "../CONTRIBUTING_CHANGE_WORKFLOW.md",
        )
    if rel == "30_verification/30.00_verification_user_guide.md":
        text = text.replace("`CONTRIBUTING_CHANGE_WORKFLOW.md`", "`../CONTRIBUTING_CHANGE_WORKFLOW.md`")
        text = text.replace("`USER_GUIDE.md`", "`../USER_GUIDE.md`")
    if rel == "40_thought_simulator_playground/Grok_comment.md":
        text = text.replace("CONTRIBUTING_CHANGE_WORKFLOW.md", "../CONTRIBUTING_CHANGE_WORKFLOW.md")
    if rel == "10_thought_simulator_req/README.md":
        text = text.replace("../50_design/", "50_design/")
    if rel.startswith("10_thought_simulator_req/docs/"):
        text = text.replace("../../50_design/", "../50_design/")
        text = text.replace(
            "10.70_snapshot_requirements.md",
            "../50_design/10.50.290_snapshot_requirements.md",
        )
        text = text.replace(
            "10.80_event_log_requirements.md",
            "../50_design/10.50.300_event_log_requirements.md",
        )
        text = text.replace(
            "10_system_architecture/10.10.270_math_requirements.md",
            "../10_system_architecture/10.10.270_math_requirements.md",
        )
        text = text.replace(
            "10.10_math_requirements.md",
            "../10_system_architecture/10.10.270_math_requirements.md",
        )
        text = text.replace(
            "50_thought_simulator_design/50.150_geometry_engine_design.md",
            "../../50_thought_simulator_design/50.270_geometry_engine_design.md",
        )
    return text


def _fix_inventory_rows(rel: str, text: str) -> str:
    rows = INVENTORY_ROW_REMOVALS.get(rel)
    if not rows:
        return text
    for row in rows:
        text = text.replace(row + "\n", "")
    return text


def _fix_broken_trace_refs(rel: str, text: str) -> str:
    if rel == "20_requirements/20.36_canonical_end_to_end_trace.md":
        text = text.replace(
            "- ../30_verification/30.210_evidence_trace_exemplars_non_normative.md\n",
            "",
        )
    return text


def _fix_validate_design_traceability(rel: str, text: str) -> str:
    if rel == "50_thought_simulator_design/50.00_design_traceability_index.md":
        if "validate_design_traceability.yml" in text and ".github/workflows/" not in text:
            text = text.replace(
                "validate_design_traceability.yml",
                "../../../.github/workflows/validate_design_traceability.yml",
            )
    return text


def _fix_tier_root_doc_paths(rel: str, text: str) -> str:
    if rel.startswith("00_program_governance/00_foundations/"):
        text = text.replace("../CONTRIBUTING_CHANGE_WORKFLOW.md", "../../CONTRIBUTING_CHANGE_WORKFLOW.md")
        text = text.replace("../USER_GUIDE.md", "../../USER_GUIDE.md")
    if rel.startswith("10_thought_simulator_req/docs/"):
        text = text.replace("../USER_GUIDE.md", "../../USER_GUIDE.md")
    if rel == "30_verification/30.00_verification_user_guide.md":
        text = text.replace("../../CONTRIBUTING_CHANGE_WORKFLOW.md", "../CONTRIBUTING_CHANGE_WORKFLOW.md")
        text = text.replace("../../USER_GUIDE.md", "../USER_GUIDE.md")
    if rel in {
        "50_thought_simulator_design/50.01_50_series_glossary.md",
        "40_thought_simulator_playground/Grok_comment.md",
    }:
        text = text.replace("../../CONTRIBUTING_CHANGE_WORKFLOW.md", "../CONTRIBUTING_CHANGE_WORKFLOW.md")
    if rel == "40_thought_simulator_playground/40.240_tr_router_prototypes/docs/experiments.md":
        text = text.replace(
            "artifacts/tr_verification_run1_2026-06-03.json",
            "../artifacts/tr_verification_run1_2026-06-03.json",
        )
    return text


def _fix_gb_heading(rel: str, text: str) -> str:
    if rel == "50_thought_simulator_design/50.130_gb_design_spec.md":
        text = text.replace(
            "# 50.130_gb_design_spec.md",
            "# 50.130 GB Design Specification",
            1,
        )
        if text.startswith("# 50.43_gb_design_decisions.md"):
            text = "# 50.130 GB Design Specification\n" + text.split("\n", 1)[1]
    return text


def _apply_text_repairs(text: str) -> str:
    for old, new in TEXT_REPAIRS:
        text = text.replace(old, new)
    return text


def main() -> int:
    changed = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in EXTENSIONS:
            continue
        if path.name == Path(__file__).name:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue

        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        original = text
        text = _apply_text_repairs(text)
        text = _governance_script_prefix(rel, text)
        text = _tier_script_prefix(rel, text)
        text = _fix_50_top_level_paths(rel, text)
        text = _fix_doc_inventory_paths(rel, text)
        text = _fix_glossary_contributing(rel, text)
        text = _fix_gb_heading(rel, text)
        text = _fix_inventory_rows(rel, text)
        text = _fix_broken_trace_refs(rel, text)
        text = _fix_validate_design_traceability(rel, text)
        text = _fix_tier_root_doc_paths(rel, text)

        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(rel)

    print(f"CI doc residual fix complete: {changed} files updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())