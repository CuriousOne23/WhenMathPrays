# ✅ **Corrected README.md — Thought Simulator Testbenches (Path A)**  
*(Aligned with new architecture: no expected‑failure flags)*

## **Overview**
The `testbenches/` directory contains all development‑mode test harnesses for the Thought Simulator primitives and pipeline.

All tests are executed through **one file**:

```
run.py
```

This is the **only user interface** for running tests.  
You never edit the testbench modules themselves.

The design supports:

- Mode `general` or `testbench` (set per tuple in `run.py`)  
- Per‑test selection via YAML paths in `tests_to_run` (not Yes/No dicts)  
- YAML‑driven deterministic test cases  
- Full development‑mode execution (no early exit)  
- Absolute PASS/FAIL evaluation (no “expected failure” mode)

Related:

- [`idob_structure_to_meaning/`](idob_structure_to_meaning/) — IdOB structure-to-meaning benches  
- [`../simulation/run_pipeline.py`](../simulation/run_pipeline.py) — Path A pipeline runner

---

## **Running Tests**
From the repository root:

```
python thought_simulator/requirements_20/system_playground/testbenches/run.py > results.log
```

Or from inside the `testbenches/` directory:

```
python run.py > results.log
```

All output is written to the log file you choose.

---

## **Selecting Which Testbenches to Run**

Inside `run.py`, testbenches are listed in `ACTIVE_TEST_MODULES` as **tuples**:

```python
ACTIVE_TEST_MODULES = [

    (
        "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.ie_testbench",
        {
            "mode": "testbench",     # "general" or "testbench"
            "use_inb": False,
            "use_iiinb": False,
            "use_ie": True,
            "tests_to_run": "see ie_tests_to_run.yaml"
        }
    ),

    # Add more testbenches here later
]
```

`tests_to_run` is a **YAML path** (typically `see <primitive>_tests_to_run.yaml` in the primitive's folder). That YAML lists test ids with `enabled: true|false`.

### ✔ To enable a testbench  
Ensure the tuple is **not commented out**.

### ✔ To disable a testbench  
Place **one `#`** at the start of the tuple:

```python
# (
    "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.inb_testbench",
    {
        "mode": "general",     # "general" or "testbench"
        "use_inb": True,
        "use_iiinb": False,
        "use_ie": False,
        "tests_to_run": "see inb_tests_to_run.yaml"
    }
),
```

Only the first `#` is needed — Python ignores the entire tuple.

---

## **Mode: `general` vs `testbench`**

Mode is configured **inside the tuple**, not inside the testbench. Values are `"general"` or `"testbench"` (not `standalone` / `progressive`).

### **`testbench` IE example**
```python
"mode": "testbench",     # "general" or "testbench"
"use_inb": False,
"use_iiinb": False,
"use_ie": True,
"tests_to_run": "see ie_tests_to_run.yaml"
```

### **`general` InB example**
```python
"mode": "general",     # "general" or "testbench"
"use_inb": True,
"use_iiinb": False,
"use_ie": False,
"tests_to_run": "see inb_tests_to_run.yaml"
```

Upstream `use_*` flags still select which primitives participate. The testbench receives this configuration from `run.py`.

---

## **Per‑Test Selection (YAML paths)**

`tests_to_run` points at a YAML file (for example `ie_tests_to_run.yaml` next to the primitive testbench):

```yaml
tests_to_run:

  - id: ie_basic_repair
    enabled: true
    reason: "Whitespace normalization repair; IE enabled."

  - id: ie_multiple_repairs
    enabled: false
    reason: "Skipped this run."
```

- `enabled: true` → test runs  
- `enabled: false` → test is skipped  
- All test IDs remain visible (no accidental deletion)

---

## **PASS/FAIL Is Absolute**

There is **no expected‑failure mode**.

Each testbench:

1. Loads the YAML test file  
2. Runs each selected test  
3. Compares the primitive’s output to the YAML’s expected output  
4. Reports PASS or FAIL  

A test either:

- **matches the YAML expectations** → PASS  
- **does not match the YAML expectations** → FAIL  

There is no conditional interpretation.

---

## **Development‑Mode Execution (No unittest)**

The testbench:

- runs all selected tests  
- logs primitive results  
- never stops early  
- prints a final primitive failure summary  

Example:

```
=== Primitive Failure Summary ===
Primitive failures detected in:
  - normalize.whitespace
  - normalize.punctuation
```

This is ideal for debugging and deterministic replay.

---

## **Redirecting Output to Logs**

```
python run.py > ie.log
python run.py > pipeline.log
python run.py > full_suite.log
```

---

## **Hotkey Control for Commenting Out Multiple Lines**

Select the lines you want to toggle:

### Windows / Linux  
**Ctrl + /**

### Mac  
**Cmd + /**

This toggles comments on all selected lines.

---

## **Adding New Downstream Primitives (Path A Integration)**

Every downstream primitive in Path A follows the same pattern:

### **1. Add a new testbench tuple in `run.py`**

Example:

```python
(
    "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.inb_testbench",
    {
        "mode": "general",     # "general" or "testbench"
        "use_inb": True,
        "use_iiinb": False,
        "use_ie": False,
        "tests_to_run": "see inb_tests_to_run.yaml"
    }
),
```

### ✔ run.py is the **only place** where new primitives are added  
### ✔ run.py imports the testbench module  
### ✔ run.py injects configuration  
### ✔ run.py calls `run_testbench()`  

You never modify the primitive testbench to add it to the system — run.py handles that.

---

### **2. The primitive testbench must call the primitive progressively**

Every primitive testbench must:

- import its primitive  
- build a ThoughtPacket  
- call the primitive in `general` or `testbench` mode  
- compare primitive output to YAML expectations  

This ensures:

- `general` and `testbench` modes  
- deterministic validation  
- Path A primitives can be tested in isolation or sequence  

---

### **3. YAML test files define the primitive’s expected behavior**

Each primitive has its own YAML file:

```
inb_testbench.yaml
iiinb_testbench.yaml
ie_testbench.yaml
```

The YAML defines:

- test IDs  
- raw input  
- expected metadata  
- expected defects  
- expected repairs  
- expected normalized output  

The testbench loads the YAML and runs only the tests selected in run.py.

---

## **Summary**

- **run.py is the only file you edit**  
- Each testbench is a **single tuple**  
- Enable/disable testbenches with **one `#`**  
- Configure `general` / `testbench` mode inside the tuple  
- Select tests via YAML paths in `tests_to_run`  
- PASS/FAIL is absolute  
- Testbenches never need editing  
- Output is fully logged  
- Development‑mode execution ensures full visibility  

---
