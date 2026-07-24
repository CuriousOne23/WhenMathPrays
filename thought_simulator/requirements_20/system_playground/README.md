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
├── 01_context/
│   └── context/
│       ├── cil/
│       ├── cob/
│       ├── cst_core/
│       ├── cst_ms/
│       ├── cst_mux/
│       ├── context_requirements.md
│       └── context_testbench.py
│
├── 02_primitives/
│   ├── definitions/
│   │   └── path_a/
│   │       ├── inb.yaml
│   │       ├── iiinb.yaml
│   │       ├── ie.yaml
│   │       ├── cex.yaml
│   │       ├── ce.yaml
│   │       ├── sob.yaml
│   │       ├── srob.yaml
│   │       ├── cnob.yaml
│   │       ├── smob.yaml
│   │       ├── isc.yaml
│   │       ├── ssg.yaml
│   │       ├── stpx.yaml
│   │       ├── rbu.yaml
│       ... (full primitive set)
│   ├── reference_objects/
│   ├── manifold/
│   ├── rg/
│   ├── rsg/
│   └── ssr/
│
├── 03_simulation/
│   ├── path_a/
│   │   ├── 01_InB/
│   │   ├── 02_IIInB/
│   │   ├── 03_IE/
│   │   ├── 04_CEx/
│   │   ├── 05_CE/
│   │   ├── 06_TPU/
│   │   ├── 07_SOB/
│   │   ├── 08_SROB/
│   │   ├── 09_CnOB/
│   │   ├── 10_SmOB/
│   │   ├── 11_ISc/
│   │   ├── 12_SSG/
│   │   ├── 13_STPX/
│   │   ├── 14_RBU/
│   │   ├── 15_DCB/
│   │   ├── 16_RB/
│   │   ├── 17_TR/
│   │   ├── 18_CTP/
│   │   ├── 19_ISc/
│   │   ├── 20_RTU/
│   │   ├── 21_RB/
│   │   ├── 22_IdOB/
│   │   ├── 23_MCB/
│   │   ├── 24_RBU/
│   │   ├── 25_DCB/
│   │   ├── 26_RB/
│   │   ├── 27_TR/
│   │   ├── 28_CTP/
│   │   ├── 29_ISc/
│   │   ├── 30_RTU/
│   │   ├── 31_RB/
│   │   ├── 32_IdOB/
│   │   ├── 33_MCB/
│   │   ├── 34_RBU/
│   │   └── 35_OuBA/
│   └── exploration/
│
├── 04_testbenches/
│   ├── path_a/
│   ├── context/
│   ├── primitives/
│   ├── shared/
│   └── helpers/
│
├── 05_design/
│   ├── design_models/
│   ├── dictionaries/
│   └── papers/
│
└── 99_archive/
    ├── logs/
    └── scratch/
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

### **Context Processing**
Start in `01_context` to validate CIL, COB, CST, and MUX.

### **Primitive Definitions**
All primitive YAMLs live in `02_primitives/definitions/path_a`.

### **Simulation Execution**
Follow the numbered folders in `03_simulation/path_a` to run or inspect each primitive step.

### **Testing**
Use `04_testbenches` for validation of context, primitives, and Path A.

### **Design Reference**
Conceptual models and dictionaries are stored under `05_design`.

### **Archival**
Logs and scratch work go into `99_archive`.

---

# 📌 Notes

- This directory is intentionally modular.
- Each primitive folder under `03_simulation/path_a` may contain:
  - `simulation_notes.md`
  - `input_examples.yaml`
  - `output_examples.yaml`
  - `test_vectors.yaml`
- The structure mirrors the Path A flow exactly.

---
