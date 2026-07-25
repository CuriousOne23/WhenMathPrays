# **README.md — Testbench Runner (Updated for Single‑Line UX)**

## **Overview**
The `testbenches/` directory contains all unit and integration tests for the Thought Simulator primitives and pipeline.  
All tests are executed through **one file**:

```
run.py
```

This script is the **only user interface** for running tests.  
You never need to open or edit any primitive testbench file.

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

All output is written to `results.log` (or any filename you choose).

---

## **Selecting Which Tests to Run (Single‑Line UX)**
Inside `run.py`, tests are listed in `ACTIVE_TEST_MODULES` as **tuples**:

```python
ACTIVE_TEST_MODULES = [
    (
        "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.ie_testbench",
        {
            "mode": "standalone",
            "use_inb": False,
            "use_iiinb": False,
            "use_ie": True
        }
    ),

    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.inb_testbench",
    #     {
    #         "mode": "standalone",
    #         "use_inb": True,
    #         "use_iiinb": False,
    #         "use_ie": False
    #     }
    # ),
]
```

Each tuple represents **one testbench** and its configuration.

### ✔ To enable a testbench  
Make sure the tuple **does not** start with `#`.

### ✔ To disable a testbench  
Place **one `#` at the start of the tuple**:

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

### ⭐ Only one `#` is required  
You do **not** need to comment out every line.  
Commenting out the **first line** of the tuple disables the entire block.

Python ignores the whole tuple automatically.

---

## **Standalone vs Progressive Testing**
You configure the pipeline behavior **inside the tuple**, not inside the testbench.

### **Standalone IE Example**
```python
(
    "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.ie_testbench",
    {
        "mode": "standalone",
        "use_inb": False,
        "use_iiinb": False,
        "use_ie": True
    }
),
```

### **Progressive IE Example (InB → IIInB → IE)**
```python
(
    "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.ie_testbench",
    {
        "mode": "progressive",
        "use_inb": True,
        "use_iiinb": True,
        "use_ie": True
    }
),
```

### **Partial Progressive Example (IIInB → IE only)**
```python
(
    "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.ie_testbench",
    {
        "mode": "progressive",
        "use_inb": False,
        "use_iiinb": True,
        "use_ie": True
    }
),
```

The testbench automatically receives this configuration from `run.py` and configures the pipeline harness accordingly.

You never edit the testbench itself.

---

## **Redirecting Output to Logs**
Any test run can be redirected:

```
python run.py > ie.log
python run.py > pipeline.log
python run.py > full_suite.log
```

This is ideal for debugging, CI, and deterministic replay.

---

## Hot key control for commenting out multiple lines on

**Windows / Linux**
    Ctrl + /

**Mac**
    Cmd + /

This will toggle comments on all selected lines:
- If the lines are uncommented → it adds # to each line
- If the lines are commented → it removes the #

This is the fastest way to comment out a whole testbench tuple.

---

## **Summary**
- **run.py is the only file you edit.**
- Each testbench is represented by a **single tuple**.
- You enable/disable tests by adding **one `#`** at the start of the tuple.
- Standalone vs progressive testing is configured **inside the tuple**.
- Testbenches and the harness never need editing.
- Output can be redirected to any log file.

This design keeps the entire testing workflow simple, centralized, and user‑friendly.

---
