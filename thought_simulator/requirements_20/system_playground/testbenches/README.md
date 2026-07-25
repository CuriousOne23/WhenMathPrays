# **README.md — Thought Simulator Testbenches (Path A)**

## **Overview**
The `testbenches/` directory contains all development‑mode test harnesses for the Thought Simulator primitives and pipeline.

All tests are executed through **one file**:

```
run.py
```

This is the **only user interface** for running tests.  
You never edit the testbench modules themselves.

The design supports:

- Standalone primitive testing  
- Progressive pipeline testing (InB → IIInB → IE → …)  
- Per‑test selection (`Yes` / `No`)  
- Per‑test expectation (`True` / `False`)  
- YAML‑driven deterministic test cases  
- Full development‑mode execution (no early exit)  
- Complete primitive failure summaries  

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

## **Selecting Which Testbenches to Run (Single‑Line UX)**

Inside `run.py`, testbenches are listed in `ACTIVE_TEST_MODULES` as **tuples**:

```python
ACTIVE_TEST_MODULES = [

    (
        "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.ie_testbench",
        {
            "mode": "standalone",
            "use_inb": False,
            "use_iiinb": False,
            "use_ie": True,

            # tests_to_run: User inputs "Yes" or "No"
            "tests_to_run": {
                "clean.simple": "Yes",
                "normalize.whitespace": "Yes",
                "normalize.punctuation": "Yes"
            },

            # expect_failure: User inputs True or False
            "expect_failure": {
                "clean.simple": False,
                "normalize.whitespace": True,
                "normalize.punctuation": False
            }
        }
    ),

    # Add more testbenches here later
]
```

### ✔ To enable a testbench  
Ensure the tuple is **not commented out**.

### ✔ To disable a testbench  
Place **one `#`** at the start of the tuple:

```python
# (
    "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.inb_testbench",
    {
        "mode": "standalone",
        "use_inb": True,
        "use_iiinb": False,
        "use_ie": False
    }
),
```

Only the first `#` is needed — Python ignores the entire tuple.

---

## **Standalone vs Progressive Pipeline**

Pipeline behavior is configured **inside the tuple**, not inside the testbench.

### **Standalone IE Example**
```python
"mode": "standalone",
"use_inb": False,
"use_iiinb": False,
"use_ie": True
```

### **Full Progressive Example (InB → IIInB → IE)**
```python
"mode": "progressive",
"use_inb": True,
"use_iiinb": True,
"use_ie": True
```

### **Partial Progressive Example (IIInB → IE only)**
```python
"mode": "progressive",
"use_inb": False,
"use_iiinb": True,
"use_ie": True
```

The testbench automatically receives this configuration from `run.py`.

---

## **Per‑Test Selection (Yes / No)**

Inside each testbench configuration:

```python
"tests_to_run": {
    "clean.simple": "Yes",
    "normalize.whitespace": "No",
    "normalize.punctuation": "Yes"
}
```

- `"Yes"` → test runs  
- `"No"` → test is skipped  
- All test IDs remain visible (no accidental deletion)

---

## **Per‑Test Expectation (True / False)**

Expectation is independent of primitive behavior:

```python
"expect_failure": {
    "clean.simple": False,
    "normalize.whitespace": True,
    "normalize.punctuation": False
}
```

Your intended semantics:

- `expect_failure = False` → expect primitive **FAIL**  
- `expect_failure = True` → expect primitive **PASS**

The testbench compares:

```
expected primitive result  vs  actual primitive result
```

and reports:

- PASS, Expectation  
- FAIL, Expectation  

Interior parentheses always describe the **primitive result**.

---

## **Development‑Mode Execution (No unittest)**

The testbench:

- runs all selected tests  
- logs primitive results  
- logs expectation results  
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

### **1. You add a new testbench tuple in `run.py`**

Example for a future primitive `inb`:

```python
(
    "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.inb_testbench",
    {
        "mode": "progressive",
        "use_inb": True,
        "use_iiinb": False,
        "use_ie": False,

        "tests_to_run": {
            "inb.clean.simple": "Yes",
            "inb.detect.defect": "Yes"
        },

        "expect_failure": {
            "inb.clean.simple": False,
            "inb.detect.defect": True
        }
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

- import its primitive (e.g., `from primitives.inb.inb import InB`)
- build a ThoughtPacket
- call the primitive in standalone or progressive mode
- compare primitive output to YAML expectations

Example pattern:

```python
from thought_simulator.requirements_20.system_playground.primitives.inb.inb import InB

class PipelineHarness:
    def __init__(self, cfg):
        self.use_inb = cfg.get("use_inb", False)
        self.use_iiinb = cfg.get("use_iiinb", False)
        self.use_ie = cfg.get("use_ie", False)

    def run(self, tp):
        if self.use_inb:
            tp = InB(tp)
        if self.use_iiinb:
            tp = IIInB(tp)
        if self.use_ie:
            tp = IE(tp)
        return tp
```

### ✔ This ensures progressive chaining  
### ✔ This ensures standalone mode works  
### ✔ This ensures Path A primitives can be validated in isolation or in sequence  

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

### **4. run.py + testbench + YAML = complete primitive integration**

This triad is the entire Path A testing system:

| Component | Responsibility |
|----------|----------------|
| **run.py** | Selects testbenches, injects config, runs them |
| **prim_testbench.py** | Calls primitive progressively, compares results |
| **prim_testbench.yaml** | Defines deterministic test cases |

This is the correct architecture for all downstream primitives.

---

## **Summary**

- **run.py is the only file you edit**  
- Each testbench is a **single tuple**  
- Enable/disable testbenches with **one `#`**  
- Configure standalone/progressive mode inside the tuple  
- Select tests using **Yes/No**  
- Set expectations using **True/False**  
- Testbenches never need editing  
- Output is fully logged  
- Development‑mode execution ensures full visibility  

This README serves as the reference for all downstream Path A work.

---
