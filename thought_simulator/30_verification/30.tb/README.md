# 30.tb - Test Bench Evidence

This directory is the landing zone for promoted test bench evidence in the 30-series verification layer.

Test benches live in the top-level `testbenches/` directory (outside the TS layers).

**Only test bench programs and documentation** are stored in the repository under `testbenches/`. All generated outputs, logs, artifacts, plots, and raw data are **excluded** from the repo (via .gitignore).

The 30.tb/ side stores **normalized text records only** (capsule.md + delta.md). These contain human-readable summaries, three-flow statements, HLR mappings, and "Testbench-Driven Changes" notes. Raw artifacts are referenced by name/timestamp or external link, but the large data payloads themselves are not committed here or anywhere in the repo.

When adding evidence for a specific test bench, create `30.tb/tb_XX_name/` containing **only** the two .md files. Do not add .json, .log, images, or other data files (they are .gitignored).

See:
- `testbenches/00_testbench_requirements.md` for the contract (including repo policy).
- 30.00_verification_user_guide.md for integration rules.
- 40.20_master_program_guide.md and 50.05_software_spec_construction_guide.md for overall flow.

Future high-fidelity test benches will also feed 30-series verification evidence via the 30.tb/ structure.

See:
- `testbenches/00_testbench_requirements.md` for the contract.
- 30.00_verification_user_guide.md for integration rules.
- 40.20_master_program_guide.md and 50.05_software_spec_construction_guide.md for overall flow.

Future high-fidelity test benches will also feed 30-series verification evidence via the 30.tb/ structure.