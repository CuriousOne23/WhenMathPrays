# IdOB papers — how to read this folder (2026-08-28)

**Kernel of structure-to-meaning IdOB is not in this folder.**  
It is:

- `testbenches/idob_structure_to_meaning/11_idob_core/idob_core.md`
- `testbenches/idob_structure_to_meaning/idob_s2m_theory.md`
- `testbenches/idob_structure_to_meaning/idob_s2m_constructs.md`
- `primitives/idob/idob.py` (wraps that kernel)

This folder gives **feel and YAML law**. It contains two sciences. Mixing them is the usual error.

## Start here

| Read | Why |
|------|-----|
| [idob_s2m_overview.md](idob_s2m_overview.md) | Purpose + two geometries + I/O names for the live hop |
| [idob_yaml_handbook.md](idob_yaml_handbook.md) | Every support YAML: format, why, how to extend, what is illegal |
| [idob_input_contract.md](idob_input_contract.md) | What the hop accepts (S2M section at top) |
| [idob_output_contract.md](idob_output_contract.md) | Packet fields |
| [idob_stability_contract.md](idob_stability_contract.md) | Δh, first-pass, flags |
| [structure_to_meaning/](structure_to_meaning/) | Crossing tables and runtime |

## Do not start here for current I/O

`appxA_purpose_and_rationale.md` … `appxAB_purpose_and_rationale.md` and `appxQ_…` are **lifecycle purpose essays**. They are not the packet schema and not how `idob.py` computes \(M\). Index: [archive/README.md](archive/README.md).

## Two labels

| Label | Meaning |
|-------|---------|
| **S2M / live** | Six IDs → map → rank → six-axis \(M\) → CIE → Δh |
| **Lifecycle / archive** | formation…closure envelope, L1/K, 10 conversation cases |

Lifecycle material is kept. It is a sibling instrument. Path A identity *tests* now run S2M (`path_a/identity/idob_testbench.yaml`). The ten cases sit in `path_a/identity/idob_lifecycle_archive.yaml` and [lifecycle/README.md](lifecycle/README.md).

## YAML copies

Live structure dictionaries: `primitives/idob/semantic_*.yaml` (see handbook).  
Copies under `papers/semantic_*.yaml` are historical duplicates — extend the **primitives/idob/** copies, not these, unless you are documenting an old snapshot.
