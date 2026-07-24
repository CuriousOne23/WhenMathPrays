# `03_simulation/subsystem_sim/README.md`

# subsystem_sim — Subsystem‑Level Simulation for Path A

This directory contains subsystem‑level simulation materials for Path A.  
It complements the primitive‑level simulation folders found under:

```
../path_a/
    01_InB/
    02_IIInB/
    03_IE/
    ...
    35_OuBA/
```

Subsystem‑level simulation focuses on **multi‑primitive behavior**, **flow‑level execution**, and **cross‑primitive envelope dynamics**. It does not redefine primitive behavior; instead, it shows how primitives interact when executed as a subsystem.

---

## Purpose

The subsystem_sim directory provides:

- Multi‑primitive simulation plans  
- Incremental execution flows  
- Notes on subsystem‑level interactions  
- Replay and stability considerations across multiple primitives  
- Context → CEx → CE integration guidance  
- Flow‑level orchestration for Path A  

This directory is **not** for primitive‑local simulation (those remain under `path_a/`).  
It is also **not** for exploratory or non‑normative work (those remain under `exploration/`).

---

## Contents

This directory contains the following files:

- **README.md** — overview and purpose of subsystem‑level simulation  
- **simulation_plan.md** — detailed subsystem simulation plan  
- **incremental_flow.md** — stepwise execution flow across Path A primitives  
- **subsystem_notes.md** — notes, constraints, and observations relevant to subsystem behavior  

Additional subsystem‑level files may be added as Path A simulation evolves.

---

## Relationship to Other Directories

### `path_a/`
Contains **primitive‑level** simulation folders.  
Each primitive has its own directory and its own local simulation artifacts.

### `exploration/`
Contains **non‑normative** exploratory work, hypotheses, and manifold investigations.  
Subsystem simulation does **not** belong there.

### `03_simulation/README.md`
Provides the **global** overview of simulation structure.  
Subsystem‑level details live here, not in the global README.

---

## Scope

Subsystem‑level simulation includes:

- Multi‑primitive envelope flow  
- Cross‑primitive constraints  
- Replay stability across cycles  
- Flow‑level sequencing  
- Integration of context machinery with Path A primitives  

Subsystem simulation does **not**:

- Replace primitive‑level simulation  
- Introduce new primitives  
- Modify glossary definitions  
- Expand acronyms beyond what 20.190 names  

All terminology used here follows **20.190** exactly.

---

## Notes

This directory is intentionally minimal and focused.  
It exists to keep `path_a/` clean and flat while still supporting subsystem‑level simulation work.

```

---
