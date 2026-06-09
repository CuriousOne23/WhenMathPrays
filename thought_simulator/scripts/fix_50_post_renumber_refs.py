#!/usr/bin/env python3
"""Rebuild protected 50.00 traceability table after Phase-3 50 design renumber."""

from __future__ import annotations

import re
from pathlib import Path

from identity_tables import TABLE_10_50, TABLE_30, bootstrap_all_tables, save_table

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "50_thought_simulator_design/50.00_design_traceability_index.md"

# (macro, 10_anchor, 30_path, 50_design_file) — sorted by macro case-insensitively.
TRACEABILITY_ROWS: list[tuple[str, str, str, str]] = [
    (
        "50-Series Design Glossary",
        "-",
        "-",
        "50.01_50_series_glossary.md",
    ),
    (
        "API Contract",
        "20.90_ib_requirements.md",
        "30_verification/README.md",
        "50.90_api_contract.md",
    ),
    (
        "Conversation Coprocessor (COP)",
        "10.50.120_cop_requirements.md",
        "30_verification/30.120_cop_prototypes/30.120_cop_prototypes_verification_capsule.md",
        "50.120_cop_design_support.md",
    ),
    (
        "Conversation Integration Layer (CIL)",
        "10.50.110_cil_requirements.md",
        "30_verification/30.110_cil_prototypes/30.110_cil_prototypes_verification_capsule.md",
        "50.110_cil_design_support.md",
    ),
    (
        "Conversation Object Basin (COB)",
        "10.50.100_cob_requirements.md",
        "30_verification/30.100_cob_prototypes/30.100_cob_prototypes_verification_capsule.md",
        "50.100_cob_design_support.md",
    ),
    (
        "Core Contract",
        "20.30_ts_functional_model.md",
        "30_verification/README.md",
        "50.08_core_contract.md",
    ),
    (
        "Core Data Structs (Track H)",
        "10.50.140_core_data_structs_design_requirements.md",
        "30_verification/30.140_core_data_structs_prototypes/30.140_core_data_structs_prototypes_verification_capsule.md",
        "50.140_core_data_structs_design_spec.md",
    ),
    (
        "DCB Stability",
        "10.50.190_dcb_stability_requirements.md (scaffold)",
        "30_verification/30.190_dcb_stability_prototypes/30.190_dcb_stability_prototypes_verification_capsule.md",
        "50.190_dcb_stability_design.md",
    ),
    (
        "Dynamics Engine",
        "20.30_ts_functional_model.md",
        "30_verification/README.md",
        "50.30_dynamics_engine_design.md",
    ),
    (
        "Error Handling",
        "20.170_safety_requirements.md",
        "30_verification/README.md",
        "50.70_error_handling_design.md",
    ),
    (
        "Event Log",
        "10.50.250_event_log_requirements.md",
        "30_verification/30.250_event_log_prototypes/30.250_event_log_prototypes_verification_capsule.md",
        "50.250_event_log_observability_design.md",
    ),
    (
        "Execution Replay",
        "10.50.70_replay_design_requirements.md",
        "30_verification/30.70_replay_prototypes/30.70_replay_prototypes_verification_capsule.md",
        "50.70_replay_design_spec.md",
    ),
    (
        "Experiment Runner Testing",
        "10.50.260_experiment_runner_requirements.md",
        "30_verification/30.260_experiment_runner/30.260_experiment_runner_verification_capsule.md",
        "50.260_experiment_runner_testing_design.md",
    ),
    (
        "Geometry Engine",
        "10.50.270_math_requirements.md",
        "30_verification/30.270_math_prototypes/30.270_math_prototypes_verification_capsule.md",
        "50.270_geometry_engine_design.md",
    ),
    (
        "Governing Basin (GB)",
        "10.50.130_gb_design_requirements.md",
        "30_verification/30.130_gb_prototypes/30.130_gb_prototypes_verification_capsule.md",
        "50.130_gb_design_spec.md",
    ),
    (
        "Input Basin (InB)",
        "10.50.50_inb_design_requirements.md",
        "30_verification/30.50_inb_prototypes/30.50_inb_prototypes_verification_capsule.md",
        "50.50_inb_design_spec.md",
    ),
    (
        "Input Inference/Repair Basin (IIInB)",
        "10.50.60_iiinb_design_requirements.md",
        "30_verification/30.60_iiinb_prototypes/30.60_iiinb_prototypes_verification_capsule.md",
        "50.60_iiinb_design_spec.md",
    ),
    (
        "Inspiration Basin (IB)",
        "10.50.170_ib_requirements.md",
        "30_verification/30.170_ib_prototypes/30.170_ib_prototypes_verification_capsule.md",
        "50.170_ib_design_spec.md",
    ),
    (
        "Logging and Observability",
        "20.40_ob_requirements.md",
        "30_verification/README.md",
        "50.80_logging_and_observability_design.md",
    ),
    (
        "Monitoring Basin (MB)",
        "10.50.200_mb_design_requirements.md",
        "30_verification/30.200_mb_prototypes/30.200_mb_prototypes_verification_capsule.md",
        "50.200_mb_design_spec.md",
    ),
    (
        "Regulator",
        "10.50.220_regulator_requirements.md",
        "30_verification/30.220_regulator_prototypes/30.220_regulator_prototypes_verification_capsule.md",
        "50.220_regulator_design_support.md",
    ),
    (
        "Scheduler",
        "10.50.210_scheduler_requirements.md",
        "30_verification/30.210_scheduler_prototypes/30.210_scheduler_prototypes_verification_capsule.md",
        "50.210_scheduler_design_spec.md",
    ),
    (
        "Snapshot Contract",
        "10.50.240_snapshot_requirements.md",
        "30_verification/30.240_snapshot_prototypes/30.240_snapshot_prototypes_verification_capsule.md",
        "50.240_snapshot_contract_design.md",
    ),
    (
        "Software Spec Construction Guide",
        "10_thought_simulator_req/docs/promotion_protocol.md",
        "30_verification/README.md",
        "50.05_software_spec_construction_guide.md",
    ),
    (
        "System Architecture",
        "20.30_ts_functional_model.md",
        "30_verification/README.md",
        "50.07_system_architecture.md",
    ),
    (
        "Testing Strategy",
        "20.200_traceability_matrix.md",
        "30_verification/README.md",
        "50.42_testing_strategy.md",
    ),
    (
        "Thought Router (TR)",
        "10.50.180_tr_requirements.md",
        "30_verification/30.180_tr_prototypes/30.180_tr_prototypes_verification_capsule.md",
        "50.180_tr_software_spec.md",
    ),
    (
        "Tick Cycle",
        "10.50.230_tick_cycle_requirements.md",
        "30_verification/30.230_tick_cycle_skeleton/30.230_tick_cycle_skeleton_verification_capsule.md",
        "50.230_tick_cycle_design_support.md",
    ),
    (
        "TP Lifecycle",
        "10.50.150_tp_requirements.md",
        "30_verification/30.150_tp_lifecycle/30.150_tp_lifecycle_verification_capsule.md",
        "50.150_tp_design.md",
    ),
    (
        "UI Contract",
        "20.180_conversational_relevance_requirements.md",
        "30_verification/README.md",
        "50.43_ui_contract.md",
    ),
    (
        "User Preference Integrator (UPI)",
        "10.50.90_upi_design_requirements.md",
        "30_verification/30.90_upi_prototypes/30.90_upi_prototypes_verification_capsule.md",
        "50.90_upi_design_spec.md",
    ),
    (
        "User Shorthand Profile (USP)",
        "10.50.80_usp_design_requirements.md",
        "30_verification/30.80_usp_prototypes/30.80_usp_prototypes_verification_capsule.md",
        "50.80_usp_design_spec.md",
    ),
]


def _validate_row_order() -> None:
    macros = [row[0] for row in TRACEABILITY_ROWS]
    sorted_macros = sorted(macros, key=lambda s: s.casefold())
    if macros != sorted_macros:
        raise RuntimeError("TRACEABILITY_ROWS must be alphabetically sorted by Macro / Domain")


def _format_table_rows() -> str:
    lines = []
    for macro, anchor_10, path_30, design_50 in TRACEABILITY_ROWS:
        lines.append(f"| {macro} | {anchor_10} | {path_30} | {design_50} |")
    return "\n".join(lines) + "\n"


def _rebuild_index_table() -> None:
    _validate_row_order()
    text = INDEX.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(\| Macro / Domain \| 10-series Anchor \| 30-series Verification Capsule Path \| 50-series Design Doc Path \|\n"
        r"\|[-| ]+\|\n)(.*?)(\n## Index maintenance)",
        re.DOTALL,
    )
    if not pattern.search(text):
        raise RuntimeError("could not locate traceability table in 50.00")
    updated = pattern.sub(rf"\1{_format_table_rows()}\3", text)
    INDEX.write_text(updated, encoding="utf-8")
    print(INDEX.relative_to(ROOT).as_posix())


def _rebuild_identity_tables() -> None:
    """Repair name tables corrupted by 50-band substring replacements."""
    tables = bootstrap_all_tables()
    save_table(TABLE_10_50, tables["10.50"])
    save_table(TABLE_30, tables["30"])
    print(TABLE_10_50.relative_to(ROOT).as_posix())
    print(TABLE_30.relative_to(ROOT).as_posix())


def main() -> int:
    _rebuild_identity_tables()
    _rebuild_index_table()
    print("Rebuilt 50.00 design traceability mapping table")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())