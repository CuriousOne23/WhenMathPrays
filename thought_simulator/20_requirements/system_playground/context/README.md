# Context Subsystem — Testbench Execution Guide
This README assumes you are executing **inside the `context/` directory**:

```
thought_simulator/20_requirements/system_playground/context/
```

The `context/` directory is a Python package because it contains `__init__.py`.  
All subsystem testbenches can be run using `python -m` from this directory.

Log files will be written **into the current directory (`context/`)** when using `>` redirection.

---

# 📌 Running All Testbenches (from inside `context/`)

## 1. CST Subsystem Testbenches
The CST subsystem consists of **three coordinated modules**:

- **CST‑Core** — stability signal generation  
- **CST‑MS** — metric synthesis  
- **CST‑Mux** — USP multiplexing  

### CST‑Core Testbench
```
python -m cst_core.cst_core_testbench
```

Log:
```
python -m cst_core.cst_core_testbench > cst_core.log
```

### CST‑MS Testbench
```
python -m cst_ms.cst_ms_testbench
```

Log:
```
python -m cst_ms.cst_ms_testbench > cst_ms.log
```

### CST‑Mux Testbench
```
python -m cst_mux.cst_mux_testbench
```

Log:
```
python -m cst_mux.cst_mux_testbench > cst_mux.log
```

---

## 2. COB Testbenches

### Standard COB Testbench
```
python -m cob.cob_testbench
```

Log:
```
python -m cob.cob_testbench > cob.log
```

### Merge/Split Structural Testbench
```
python -m cob.cob_testbench_merge_split
```

Log:
```
python -m cob.cob_testbench_merge_split > cob_merge_split.log
```

---

## 3. CIL Testbench
```
python -m cil.cil_testbench
```

Log:
```
python -m cil.cil_testbench > cil.log
```

---

## 4. Unified Context Pipeline Testbench
This testbench runs the full pipeline:

```
CST‑Core → CST‑MS → CST‑Mux → COB → CIL
```

Run:
```
python -m context_testbench
```

Log:
```
python -m context_testbench > context.log
```

---

# 📌 Summary
- All commands assume you are inside the **context/** directory.  
- Use `python -m context.<module>.<testbench>` to run each subsystem.  
- Use `> file.log` to capture logs into the **context/** directory.  
- The CST subsystem now refers to **CST‑Core + CST‑MS + CST‑Mux**.  
- The unified testbench validates merge/split continuity across CST, COB, and CIL.

Everything stays clean, deterministic, and easy to run.
```

---
