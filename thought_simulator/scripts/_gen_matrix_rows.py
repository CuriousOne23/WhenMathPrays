from pathlib import Path
import re

REQ = Path(__file__).resolve().parents[1] / "20_requirements"

scopes = {
    "20.12_ts_invariants.md": "canonical TS invariants and replay boundaries",
    "20.16_gb_responsibility_matrix.md": "GB responsibility and cap matrix",
    "20.17_messy_input_handling.md": "messy-input taxonomy and preservation",
    "20.18_failure_modes_and_success_criteria.md": "failure modes and success criteria",
    "20.36_canonical_end_to_end_trace.md": "normative trace fixtures and replay test classes (v0.5)",
    "20.37_thought_router_tr_specification.md": "Thought Router TR specification",
    "20.38_ts_implementation_guidelines.md": "TS implementation guidelines",
    "20.39_ts_core_data_structures.md": "core data structures and envelope schemas",
    "20.45_imr_requirements.md": "IMR evaluation and correction triggers",
    "20.58_oub_execution_manifold_integration.md": "OuB execution manifold B-integration (v0.2)",
    "20.90_ts_parameter_table.md": "TS parameter table and defaults",
    "20.95_ts_numeric_policy.md": "numeric serialization and comparison policy",
    "20.207_execution_replay_specification.md": "E2 regeneration replay specification (v0.3)",
    "20.500_refactoring_for_dual_TS_pipeline.md": "dual-pipeline refactor coordination (non-normative)",
}

special = {
    "20.70_mb_requirements.md": (
        "../30_verification/30.200_mb_prototypes/30.200_mb_prototypes_verification_capsule.md",
        "../50_thought_simulator_design/50.1500_mb_design_spec.md",
    ),
    "20.165_dcb_stability_requirements.md": (
        "../30_verification/30.190_dcb_stability_prototypes/30.190_dcb_stability_prototypes_verification_capsule.md",
        "../50_thought_simulator_design/50.190_dcb_stability_design.md",
    ),
}

default_v = "../30_verification/README.md"
default_d = "../40_thought_simulator_playground/40.05_master_program_guide.md"

docs = sorted(
    [p.name for p in REQ.glob("20.*.md") if re.match(r"^20\.(\d+)_.*\.md$", p.name)],
    key=lambda n: (int(re.match(r"^20\.(\d+)_", n).group(1)), n),
)

for doc in docs:
    scope = scopes.get(doc, doc.replace(".md", "").replace("_", " "))
    ver, des = special.get(doc, (default_v, default_d))
    print(f"| {doc} | {scope} | {ver} | {des} |")