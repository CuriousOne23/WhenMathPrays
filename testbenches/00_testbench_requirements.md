---
status: infrastructure
source_of_truth: this
contains:
  - LLR: [LLR-TB-001, LLR-TB-002, LLR-TB-003, LLR-TB-004, LLR-TB-005]
---

# Test Bench Requirements

**Document ID:** 00_testbench_requirements  
**Version:** 0.1  
**Date:** 2026-06-05  
**Status:** Draft

## Purpose

This document defines the canonical contract for all test benches in the Thought Simulator (TS) project. Test benches are high-fidelity, external-to-prototype verification infrastructure. They generate evidence that can validate, challenge, or extend requirements and design contracts.

Test benches are **not** prototypes (40-series), **not** design specifications (50-series), and **not** core requirements (20-series or 10.50-series). They are independent evidence generators.

## Scope

This document governs:
- Required artifacts and output formats from any test bench.
- How test benches must reference HLRs/LLRs.
- Reproducibility, determinism, and negative-path requirements.
- Integration with the 30-series verification layer.
- Naming and directory conventions.

## Repository Policy (Repo Space Control)

To keep the repository lean:

- **Only test bench programs, scripts, documentation, and configuration** are stored in the repo (under `testbenches/`).
- **No generated outputs, logs, artifacts, plots, traces, CSV results, or large data files** are committed.
- All such outputs **MUST** be excluded via `.gitignore` (rules cover `testbenches/**/logs/`, `**/artifacts/`, `**/plots/`, `**/traces/`, `**/*.json`, `**/*.log`, `**/*.png`, `**/*.csv`, `**/results/`, etc.).
- Test benches may store their raw execution results locally (e.g., in a `.gitignore`'d `artifacts/`, `logs/`, `plots/`, or `results/` subdir inside their `tb_XX_name/`) or externally (CI artifacts, shared storage, etc.).
- When evidence from a test bench is needed for the 30-series, only **normalized text records** (capsule.md + delta.md with textual summaries, HLR mappings, and "Testbench-Driven Changes" notes) are stored in `30_verification/30.tb/`. Raw artifacts are referenced by name/timestamp or external link — the actual data payloads are never copied into the repository.

## Test Bench Output Contract

Every test bench **SHALL** produce the following minimum artifacts:

1. **Primary JSON Artifact** (`tb_XX_name_YYYY-MM-DD.json` or equivalent)
   - Must contain:
     - `bench_id`: unique identifier (e.g., "tb_01_mb_drift")
     - `timestamp`: ISO8601
     - `component`: e.g., "39" for MB
     - `referenced_hlrs`: array of HLR ids exercised (from 20 and 10.50)
     - `scenarios`: list of executed scenarios with:
       - `name`
       - `status`: "PASS" | "FAIL" | "PARTIAL"
       - `metrics`: key-value measurements (e.g., drift_error, tcu_cost, reproducibility_score)
       - `evidence`: references to logs, plots, or raw data
     - `three_flow_note`: short statement on Forward/Backward/Iterative drivers (if applicable)
     - `reproducibility`: evidence of multiple runs with identical results (within tolerance)

2. **Human-Readable Summary** (optional but recommended: `tb_XX_name_summary.md`)
   - Narrative description of what was tested and key findings.

3. **Supporting Data**
   - Plots, logs, raw traces, etc., referenced from the JSON.

## HLR Referencing Rules

- Test benches **SHALL** explicitly map test scenarios to HLRs from:
  - 20-series requirements (e.g., HLR-20.070-xxx)
  - 10.50-series design requirements (e.g., HLR-10.50.39-xxx)
- Mappings must be listed in the JSON artifact.
- Test benches **MAY** propose new or refined HLRs when results reveal gaps (recorded via 30-series delta).

## Reproducibility and Determinism Requirements

- **LLR-TB-001**: Identical configuration and inputs **SHALL** produce bitwise-identical or statistically equivalent outputs across runs (document tolerance).
- **LLR-TB-002**: Test benches **SHALL** support seeded or deterministic modes where the component under test supports it.
- **LLR-TB-003**: Negative-path and edge-case coverage **SHALL** be explicitly exercised and reported.

## Integration with 30-Series Verification Layer

Test bench results are promoted into the 30-series for traceability and impact analysis:

- Create or update `30_verification/30.tb/tb_XX_name/` containing **only**:
  - `tb_XX_name_capsule.md` (human summary + three-flow)
  - `tb_XX_name_delta.md` (mapping to HLRs + "Testbench-Driven Changes" section)
  
  The 30.tb/ side stores **normalized text records only**. The full raw JSON artifact, logs, plots, etc. are **never committed** to the repository (they remain local or external). The delta/capsule may contain textual summaries or links (e.g., to external artifact storage or CI job), but not the large output payloads themselves.

- Any required changes to 10.50 or 50 **MUST** be recorded in the 30.tb delta under:

```markdown
### Testbench-Driven Changes
- TB-01 (2026-xx-xx): Test bench revealed X → updated HLR-10.50.39-011 (threshold governance)
- TB-02 (2026-xx-xx): Result Y → refined 50.39 §4.2 (IO contract)
```

- Promotion of test bench evidence follows the same human-approval gate as prototype evidence (see 30.00).

## Naming and Directory Conventions

- Top-level: `testbenches/`
- Requirements: `testbenches/00_testbench_requirements.md`
- Individual benches: `testbenches/tb_01_name/`, `testbenches/tb_02_name/` (sequential, descriptive suffix)
- In 30_verification: `30.tb/` (general testbench evidence) or `30.tb_XX/` for specific.
  - Inside: `tb_01_capsule.md`, `tb_01_delta.md`, `tb_01_artifact.json` (or date-stamped).

Numbering must remain flexible:
- Use `tb_XX` where XX is a simple sequence.
- Component association (e.g., 39 for MB) is recorded in metadata, not in the directory name.
- This allows easy insertion of new benches and association with any module (39, 37, etc.) without renumbering.

## Non-Goals

Test benches are **NOT** responsible for:
- Defining core product behavior (that's 20/10.50/50).
- Exploratory rapid prototyping (that's 40-series).
- Being the sole source of truth (30-series promotes and contextualizes them).

## Change Control

Updates to this document require review against 50.05 and 30.00.

When a test bench reveals the need for structural changes to the test bench contract itself, update this document and propagate to all active `tb_XX` directories and their 30.tb records.

## Related Documents

- `thought_simulator/30_verification/30.00_verification_user_guide.md`
- `thought_simulator/40_thought_simulator_playground/40.20_master_program_guide.md`
- `thought_simulator/50_thought_simulator_design/50.05_software_spec_construction_guide.md`
- Component-specific 10.50 and 50 docs (e.g., 10.50.39, 50.39)
- `thought_simulator/20_requirements/20.200_traceability_matrix.md` (will reference test bench evidence via 30)

---

**Status**: This document is the authoritative contract for test bench infrastructure. All future test benches must conform or propose updates here.