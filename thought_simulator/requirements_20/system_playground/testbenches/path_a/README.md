# Testbench

Path A primitive testbenches. Run them from `../run.py` (`mode`: `general` or `testbench`; `tests_to_run` is a YAML path).

## Folder map

| Folder | What's here |
|---|---|
| `intake/` | InB, IIInB, IE (`*_testbench.py`, `*_tests_to_run.yaml`, rules/input YAML) |
| `semantic/` | CEx-IE, CEx-CCR, CEx-Pck, CE, SOB, SROB, CnOB, SmOB |
| `transform/` | TPU |
| `structure/` | RBU, SSG, STPX |
| `routing/` | CTP, DCB, ISc, RB |
| `identity/` | IdOB, MCB |
| `output/` | OuBA |
| `context/` | CIL, COB, CST-core / CST-ms / CST-mux |
| `encoder/` | WRDNM |
| `boundary/` | boundary / DCB YAML plus `test_cex_boundary.py` |
| `mismatch/` | `imr_testbench.yaml` |

Sibling benches (not under `path_a/`):

- [`../idob_structure_to_meaning/`](../idob_structure_to_meaning/)
- [`../review/`](../review/)
- Path A pipeline: [`../../simulation/run_pipeline.py`](../../simulation/run_pipeline.py)
