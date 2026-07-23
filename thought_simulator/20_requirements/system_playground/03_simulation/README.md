# 03_simulation — Path A primitive simulation

`03_simulation` contains the primitive‑level simulation flow for Path A.  
It is the execution workspace that runs, inspects, and validates each primitive in sequence, using the definitions in `02_primitives` and the context machinery in `01_context`.

## Path A flow

The Path A primitive sequence is:

InB → IIInB → IE → CEx → CE → TPU → SOB → SROB → CnOB → SmOB → ISc →  
SSG → STPX → RBU → DCB → RB → TR → CTP → ISc → RTU → RB → IdOB → MCB →  
RBU → DCB → RB → TR → CTP → ISc → RTU → RB → IdOB → MCB → RBU → …  
OR  
DCB → RB → TR → CTP → ISc → RTU → RB → OuBA

Each primitive has its own subdirectory under `path_a/`:

- `01_InB/`
- `02_IIInB/`
- `03_IE/`
- `04_CEx/`
- `05_CE/`
- `06_TPU/`
- `07_SOB/`
- `08_SROB/`
- `09_CnOB/`
- `10_SmOB/`
- `11_ISc/`
- `12_SSG/`
- `13_STPX/`
- `14_RBU/`
- `15_DCB/`
- `16_RB/`
- `17_TR/`
- `18_CTP/`
- `19_ISc/`
- `20_RTU/`
- `21_RB/`
- `22_IdOB/`
- `23_MCB/`
- `24_RBU/`
- `25_DCB/`
- `26_RB/`
- `27_TR/`
- `28_CTP/`
- `29_ISc/`
- `30_RTU/`
- `31_RB/`
- `32_IdOB/`
- `33_MCB/`
- `34_RBU/`
- `35_OuBA/`

An `exploration/` directory is available for ad‑hoc experiments and non‑normative runs.

## Incremental simulation plan

Recommended development and validation sequence:

1. **Context + CEx**  
   - Run context pipeline in `01_context/context/`.  
   - Simulate `04_CEx/` to produce CE from IE output.

2. **InB → IIInB → IE → CEx → CE → TPU**  
3. **TPU → SOB → SROB → CnOB → SmOB → ISc**  
4. **ISc → SSG → STPX → RBU → DCB**  
5. **DCB → RB → TR → CTP → ISc**  
6. **ISc → RTU → RB → IdOB → MCB**  
7. **MCB → RBU → DCB → RB → TR → CTP**  
8. **CTP → ISc → RTU → RB → OuBA**  
9. **OuBA with context processing** (final envelope checked against context requirements)

## Relationship to other directories

- **01_context/** — context pipeline (CIL, COB, CST‑Core, CST‑MS, CST‑Mux).  
- **02_primitives/** — primitive definitions (YAML) and reference objects.  
- **04_testbenches/** — testbenches for context, primitives, and Path A.  
- **05_design/** — design models, dictionaries, and papers.

For canonical names, roles, and constraints of each primitive, see `20.190_glossary.md`.  
This README intentionally uses only the primitive acronyms to avoid introducing any acronym drift.
