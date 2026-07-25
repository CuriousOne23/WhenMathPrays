# **README.md — Thought Simulator Testbenches**

## **Overview**
The `testbenches/` directory contains all unit and integration tests for the Thought Simulator primitives and pipeline.  
This includes:

- **Standalone primitive tests** (InB, IIInB, IE, etc.)  
- **Progressive pipeline tests** (InB → IIInB → IE → …)  
- A unified **test runner** (`run.py`)  
- YAML‑driven deterministic test cases  
- Support for both **positive** and **negative** test scenarios

All tests are executed through `run.py`, which loads only the test modules you select.

---

## **Running All Selected Tests**
From the repository root:

```
python thought_simulator/requirements_20/system_playground/testbenches/run.py > results.log
```

Or from inside the `testbenches/` directory:

```
python run.py > results.log
```

This will:

- add the repo root to `PYTHONPATH`
- load the test modules listed in `ACTIVE_TEST_MODULES`
- execute them using Python’s `unittest` framework
- write all output to `results.log` (or any filename you choose)

---

## **Selecting Which Testbenches to Run**
Open:

```
testbenches/run.py
```

Locate the section:

```python
ACTIVE_TEST_MODULES = [
    "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.ie_testbench",
    # Add or remove test modules here
]
```

To run a testbench:

- **uncomment** its module path  
To disable a testbench:

- **comment out** its module path  

Only the modules listed in `ACTIVE_TEST_MODULES` will run.

You do **not** modify any other part of `run.py`.

---

## **Standalone Primitive Testing**
Standalone testing means **only one primitive is exercised**, with all upstream primitives replaced by stubs.

Example: testing IE alone.

Your testbench configures the harness like:

```python
h = PipelineHarness(
    use_inb=False,
    use_iiinb=False,
    use_ie=True,
    expect_failure=test_case.get("expected_failure", False)
)
```

This ensures:

- IE receives raw input  
- InB and IIInB are stubbed  
- IE is tested in isolation  
- The testbench evaluates success/failure based on the YAML case  

Standalone testing is ideal for:

- early development  
- debugging a single primitive  
- verifying minimal behavior  
- validating negative cases (failure detection)

---

## **Progressive Pipeline Testing**
Progressive testing means **real upstream primitives are included**, in correct order, before the primitive under test.

Example: testing IE with real IIInB:

```python
h = PipelineHarness(
    use_inb=False,      # stubbed
    use_iiinb=True,     # real
    use_ie=True,        # real
    expect_failure=test_case.get("expected_failure", False)
)
```

Example: full intake pipeline:

```python
h = PipelineHarness(
    use_inb=True,
    use_iiinb=True,
    use_ie=True,
    expect_failure=test_case.get("expected_failure", False)
)
```

The harness enforces the **progressive rule**:

- A downstream primitive may run only if all upstream primitives are either **real** or **stubbed**  
- Upstream primitives may never be **skipped**  

This prevents invalid pipeline configurations.

---

## **Positive vs. Negative Tests**
YAML test cases may include:

```
expected_failure: true
```

or

```
expected_failure: false
```

The harness interprets this as:

- **expected_failure = true**  
  The primitive must detect a failure → test **passes**

- **expected_failure = false**  
  The primitive must accept the TP → test **passes**

If the primitive behaves opposite to expectation, the test **fails**.

This allows:

- failure‑detection tests  
- acceptance tests  
- isolated negative tests  
- progressive negative tests  

All using the same YAML.

---

## **Redirecting Output to Logs**
Any test run can be redirected to a log file:

```
python run.py > ie_intake.log
python run.py > pipeline.log
python run.py > full_suite.log
```

This is useful for:

- CI pipelines  
- debugging  
- regression tracking  
- deterministic replay  

---

## **Summary**
- `run.py` is the unified test runner  
- You select testbenches by editing `ACTIVE_TEST_MODULES`  
- Standalone and progressive testing are both supported  
- The pipeline harness handles upstream stubbing and progressive rules  
- YAMLs remain simple and deterministic  
- Output can be redirected to any log file  

This setup supports both **primitive‑level development** and **full pipeline validation** as the Thought Simulator expands.

---
