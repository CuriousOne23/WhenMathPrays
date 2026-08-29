# 📘 system_playground — Simulation Workspace Overview

`system_playground` is the **primitive‑level simulation environment** for the Thought Simulator.  
It contains all components required to run, test, and validate **Path A** and related primitive flows.  
The directory is organized to make the simulation pipeline clear, traceable, and reviewer‑friendly.

---

## 🧭 Purpose of system_playground

This workspace supports:

- **Context processing** (CIL, COB, CST, MUX)
- **Primitive definitions** and reference structures
- **Path A simulation flow**
- **Primitive‑level testbenches**
- **Design models and dictionaries**
- **Archival of logs and scratch work**

It is intentionally modular so each layer of the simulation can be understood independently.

---

# 📂 Directory Structure

```
system_playground/
│
├── design/
│   ├── design_models/
│   ├── dictionaries/
│   ├── papers/
│   └── pipeline/
│
├── primitives/
│   ├── <name>/            ← one folder per primitive (inb, ie, idob, mcb, …)
│   ├── definitions/
│   ├── dictionary/
│   └── reference_objects/
│
├── simulation/
│   ├── ts_kernel/         ← Path A kernel (landed 2026-08-28)
│   ├── run_pipeline.py
│   ├── pipelines/
│   │   └── lineup_idob_mcb/
│   ├── context/
│   └── conversations/
│
└── testbenches/
    ├── run.py
    ├── path_a/
    ├── idob_structure_to_meaning/
    ├── review/
    └── helpers/
```

---

# 🧩 Design Principles

### **1. Flow‑First Organization**
Path A is represented as a **linear sequence**, making the simulation progression easy to follow.

### **2. Separation of Concerns**
Context, primitives, simulation, testbenches, and design documents each live in their own pillar.

### **3. Reviewer Legibility**
A new contributor can understand the system in minutes by reading this README and browsing the tree.

### **4. Scalability**
This structure is designed to support future expansion, including:

- `system_simulation/` (higher‑level simulation)
- Additional paths (Path B, Path C)
- Multi‑primitive integration flows

---

# 🚀 How to Use system_playground

### **Primitive definitions**
Each primitive lives under `primitives/<name>/`. Shared catalogs are in `primitives/definitions/` and `primitives/dictionary/`.

### **Simulation execution**
Run from `simulation/`: `run_pipeline.py` plus `ts_kernel/` and `pipelines/lineup_idob_mcb`.

### **Testing**
Use `testbenches/run.py` for Path A benches under `testbenches/path_a/`. Additional benches: `testbenches/idob_structure_to_meaning/` and notes in `testbenches/review/`.

### **Design reference**
Conceptual models, dictionaries, and papers are stored under `design/`.

---

# 📌 Notes

- This directory is intentionally modular.
- Primitive implementations live under `primitives/<name>/`.
- The Path A machine lives under `simulation/` (`ts_kernel/`, `run_pipeline.py`, `pipelines/lineup_idob_mcb`).

---
