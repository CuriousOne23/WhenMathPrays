# **progressive_lineup_testing.md — Path‑A Progressive Lineup Testing Framework (Version 4.2)**
**Status:** Active  
**Scope:** All Path‑A primitives  
**Applies To:** IIInB, IE, CEx, CE, WrdNm, ISc, TPU, SOB, SROB, CnOB, SmOB, SSG, STPX, RBU, DCB, IdOB, TR, CTP, RTU, RB, OuBA, SSRGn, MCB  
**Exception:** InB (partially tested; no upstream primitive)

**Theory guides (informative):**

- `design/papers/ts_theory/ts_rb_idob_foundations/` — first‑order RB/IdOB theory  
  - `ts_invariant_relational_model.md` — $\mathbf{F}$, shared regimes, TP bridge  
  - `ts_invariant_to_idob_theory.md` — IdOB operator $\mathcal{I}$  
  - `ts_routing_entropy_dynamics.md` — RED and RB operator $\mathcal{R}$  
  - `ts_identity_geometry.md` — IGM, $\kappa_{\text{id}}$  
  - `ts_semantic_residue_topology.md` — residue topology  
- `20.50_rb_requirements.md` (v3.0+) — normative RB primitive  

This framework is **not a requirements document**.  
It describes **how primitives are tested**, not **what they must do** (HLRs live in 20.xx).

---

# **1. Purpose**

The **Progressive Lineup Testing Framework** defines how **every Path‑A primitive** is tested in a deterministic, layered, replay‑safe manner.
It ensures:

- stable intake behavior  
- deterministic primitive outputs  
- correct propagation of envelopes  
- correct provenance  
- correct bounded‑semantic behavior  
- correct pipeline integration  
- Python/C++ parity  
- rule‑driven validation  
- strict primitive boundary discipline  
- first‑order observability of routing / identity foundation quantities when those layers are under test  

---

# **2. Core Testing Philosophy**

Path‑A primitives are tested using a **progressive lineup**, meaning:

1. **Each primitive is tested in isolation**  
2. **Each primitive is tested in pipeline context**  
3. **Each primitive is tested with deterministic expected outputs**  
4. **Each primitive is tested with rule‑driven validation**  
5. **Each primitive is tested with upstream variation**  
6. **Each primitive is tested with replay determinism**  
7. **Each primitive is tested for Python/C++ parity**  
8. **Foundation‑aligned primitives (RB, IdOB, and contributors to $\mathbf{F}$) are tested for layer separation and write‑boundary discipline**  

The lineup is **progressive** because:

- The user can choose any upstream primitive as the starting point.  
- All primitives between that upstream primitive and the primitive under test are executed normally.  
- The primitive under test is validated either by expected outputs or by rule‑checking.

---

# **3. Testing Modes (Authoritative Operational Definition)**

Testing behavior is controlled exclusively by the `mode` field injected by `run.py` into each primitive’s testbench module:

```
mode: "testbench"   # deterministic mode
mode: "general"     # rule-driven mode
```

Every Path‑A primitive **must** implement both modes exactly as defined below.

---

## **3.1 Mode A — “testbench” (Strict Deterministic Testing)**

**Input Source:**
```
<primitive>_testbench.yaml
```

**Operational Rule (must be followed by all testbenches):**
- When `mode == "testbench"`, the testbench **must load the full testbench YAML**, which contains:
  - `input:` — the complete TP input envelope  
  - `expected:` — the complete expected TP output envelope **or** a structural foundation expected block (see §3.11)  
- The primitive is executed once using the `input:` envelope.
- The primitive’s output is compared against `expected:` (exact equality **or** declared structural foundation comparison).
- PASS/FAIL is determined **solely** by that comparison in testbench mode.

**Rulechecker Behavior:**
- The rulechecker **may run**, but only for diagnostics.  
- Rulechecker results **do not affect PASS/FAIL** in testbench mode.

**Passthrough Behavior:**  
If `use_<primitive> = false` in `run.py`:
- The primitive is **not executed**.  
- Its input envelope is **passed through unchanged**.  
- Expected‑output comparison is skipped for that primitive.

**Purpose:**  
- Canonical correctness  
- Deterministic replay  
- Regression testing  
- Python/C++ parity  
- Stable envelope evolution  

---

## **3.2 Mode B — “general” (Rule‑Driven Testing)**

**Input Source:**
```
<primitive>_input.yaml
```

**Operational Rule (must be followed by all testbenches):**
- When `mode == "general"`, the testbench **must load only the primitive’s general‑mode input file**:
  - `<primitive>_input.yaml`
- The primitive is executed normally.
- The output is validated **only by rulechecking**, using:
  - `<primitive>_rules.yaml`
  - `<primitive>_rulechecker.py`
- PASS/FAIL is determined **solely** by rule compliance.

Rulecheckers MUST validate only the fields declared in `<primitive>_rules.yaml`.

**Expected‑output YAML is never used in general mode.**

**Purpose:**  
- Flexible exploratory testing  
- Upstream variation testing  
- Rule‑driven correctness  
- Pipeline safety validation  
- Rapid scenario construction  
- Foundation observation (regime / adjacency / $\mathbf{F}$ proxies) without brittle full‑envelope goldens  

---

## **3.3 Mandatory Input‑Source Rule**

To prevent ambiguity and ensure deterministic behavior across all Path‑A primitives:

### **All primitive testbenches MUST implement the following rule:**

| `mode` value in run.py | Input file loaded by `<primitive>_testbench.py` | Output validation method |
|------------------------|--------------------------------------------------|---------------------------|
| `"testbench"`          | `<primitive>_testbench.yaml` (input + expected) | Exact equality **or** structural foundation comparison (§3.11) |
| `"general"`            | `<primitive>_input.yaml` (input only)           | Rulechecking only         |

This rule is **mandatory**, applies to **all Path‑A primitives**, and must be implemented exactly as written.

---

## **3.4 Why This Rule Exists (Clarification for Developers)**

This explicit rule ensures:

- deterministic replay in testbench mode  
- rule‑driven flexibility in general mode  
- correct envelope propagation  
- correct provenance propagation  
- correct pipeline integration  
- correct Python/C++ parity  
- correct behavior under progressive upstream selection  
- correct passthrough behavior when `use_<primitive> = false`  

It also prevents the exact mistake that occurred in the original `cex_pck_testbench.py`, where the testbench accidentally loaded `<primitive>_input.yaml` even in testbench mode.

---

## **3.5 Unified Flow Summary**

### **Mode A — Testbench (Deterministic)**
Files used:
- `<primitive>_testbench.yaml`  
- `<primitive>_tests_to_run.yaml`  

Flow:
1. Load test selection.  
2. For each enabled test:
   - Load full input + expected output from `<primitive>_testbench.yaml`.  
   - Execute primitive.  
   - Compare actual vs expected (exact or structural foundation).  
   - PASS/FAIL by that comparison.  
3. Rulechecker optional (diagnostics only).

### **Mode B — General (Rule‑Driven)**
Files used:
- `<primitive>_input.yaml`  
- `<primitive>_rules.yaml`  
- `<primitive>_rulechecker.py`  

Flow:
1. Load general input.  
2. Execute primitive.  
3. Load rules.  
4. Rulechecker validates output.  
5. PASS/FAIL by rule compliance.

---

### **3.6 Primitive Discovery & Directory Schema (Mandatory for All Path‑A Primitives)**

To eliminate repeated manual edits to `primitive_testbench.py` and ensure that **every primitive is automatically discoverable**, the following directory schema is **mandatory** for all Path‑A primitives.

This schema guarantees that:

- `run.py` can always locate the correct primitive module  
- `primitive_testbench.py` can always locate the correct testbench files  
- rulecheckers, YAMLs, and dictionaries are always found  
- no primitive ever requires hardcoded paths  
- pipeline execution is stable and deterministic  

---

## **3.6.1 Primitive Code Location (Executable Module)**

Every primitive’s Python implementation **must** be located at:

```
thought_simulator/
  requirements_20/
    system_playground/
      primitives/
        <primitive_name>/
          <primitive_name>.py
```

Examples:

```
primitives/ce/ce.py
primitives/cex_pck/cex_pck.py
primitives/dcb/dcb.py
primitives/rb/rb.py
```

This path is **authoritative** and is used by the dynamic primitive loader.

Optional structural program (recommended):

```
primitives/<primitive_name>/<primitive_name>_py_struc_pgm.md
```

---

## **3.6.2 Primitive Testbench Location (YAML + Rulechecker + Runner)**

All testbench files for a primitive **must** be located under:

```
thought_simulator/
  requirements_20/
    system_playground/
      testbenches/
        path_a/
          <category>/
            <primitive_name>_testbench.py
            <primitive_name>_testbench.yaml
            <primitive_name>_input.yaml
            <primitive_name>_rules.yaml
            <primitive_name>_tests_to_run.yaml
            <primitive_name>_rulechecker.py
```

Where `<category>` ∈:

```
 boundary
 identity
 intake
 mismatch
 routing
 semantic
 structure
 transform
 encoder
 output
```

Example (CE):

```
testbenches/path_a/semantic/ce_testbench.py
testbenches/path_a/semantic/ce_testbench.yaml
testbenches/path_a/semantic/ce_rules.yaml
testbenches/path_a/semantic/ce_tests_to_run.yaml
```

Example (RB):

```
testbenches/path_a/routing/rb_testbench.py
testbenches/path_a/routing/rb_testbench.yaml
... 
```

This ensures that **every primitive testbench is discoverable by pattern**, not by hardcoded paths.

---

## **3.6.3 Primitive Dictionary / Lookup‑Table Location (If Required)**

Dictionaries and scalar tables may live in **one of two places**, chosen by size and ownership:

### **A. Small, exclusive tables (preferred for most Path‑A primitives)**
When the tables are small, numerous, and owned exclusively by a single primitive (the common case for WrdNm, SOB, SROB, CnOB, SmOB, etc.), they **may** live inside the primitive directory itself:

```
thought_simulator/
  requirements_20/
    system_playground/
      primitives/
        <primitive_name>/
          <table_or_dict>.yaml
```

This keeps the primitive self‑contained and avoids unnecessary path complexity.

### **B. Large or shared dictionaries**
When a dictionary is large, requires formal versioning / ownership notes, or is intended for use by multiple primitives, it **must** live under the centralized design tree:

```
thought_simulator/
  requirements_20/
    system_playground/
      design/
        dictionaries/
          path_a/
            <dictionary_category>/
```

Where `<dictionary_category>` ∈:

```
conversion_pipeline
meaning_dictionary
routing_dictionary
semantic_dictionary
structure_dictionary
encoder_dictionary
```

### **Lookup rule**
Loaders and primitives look first in the primitive’s own directory, then (if not found) in the corresponding `design/dictionaries/path_a/<category>/` location.  
Because there are only two legitimate places, discovery friction remains low.

This dual‑location rule preserves simplicity for the many small tables while still providing a formal home for the few large or shared ones.

---

## **3.6.4 Dynamic Primitive Loader (Mandatory Behavior)**

`primitive_testbench.py` **must** locate primitive modules and testbench files dynamically using the directory schema above.

### **Primitive module discovery rule:**

```
primitives/<primitive_name>/<primitive_name>.py
```

### **Testbench discovery rule:**

```
testbenches/path_a/**/<primitive_name>_testbench.yaml
```

### **Rules discovery rule:**

```
same directory as <primitive_name>_testbench.yaml
```

### **Tests-to-run discovery rule:**

```
same directory as <primitive_name>_testbench.yaml
```

This eliminates all hardcoded paths and ensures that **every primitive is automatically discoverable** without modifying any loader code.

---

## **3.6.5 Optional (Recommended): Primitive Self‑Identification**

Each primitive may declare its name inside its module:

```python
PRIMITIVE_NAME = "ce"
```

This allows loaders to read the primitive name directly from the module, further reducing configuration overhead.

---

## **3.6.6 Nested TP Field Path Convention (Mandatory for Schema‑Driven Primitives)**

When a primitive resolves nested fields on the Thought Packet (TP) envelope — whether via a schema file (`tp_field:`), hard‑coded paths, or testbench expected blocks — the following rule is **mandatory**:

### **Paths are relative to the TP envelope root**

The runtime object passed into a primitive **is** the TP.  
Field paths **must not** be prefixed with `TP.`.

| Correct | Incorrect |
|---------|-----------|
| `metadata.thread_string` | `TP.metadata.thread_string` |
| `IE.normalized_surface` | `TP.IE.normalized_surface` |
| `CE.temporal.marker` | `TP.CE.temporal.marker` |
| `SmOB.adjacency.flag` | `TP.SmOB.adjacency.flag` |
| `metadata.geometric_state.curvature` | `TP.metadata.geometric_state.curvature` |

### **Why this rule exists**

- Prose and architecture diagrams often say “TP.metadata…” for readability.  
- Schema authors and implementers naturally copy that prefix into machine paths.  
- Resolvers start at the TP root, so a leading `TP.` looks for a key that does not exist and silently falls back (often to `0` / empty).  
- That failure mode is hard to spot until exact‑equality tests fail on a single field.

### **Scope**

Applies to **all** Path‑A primitives that read or declare nested TP paths, including (but not limited to) schema‑driven encoders such as WrdNm, geometric indexers such as DCB, routing primitives such as RB, and any future ISc / scoring field maps.

This rule travels with every primitive test via this document and eliminates a recurring class of silent path‑resolution bugs.

---

### **3.7 Python Import Path Initialization (Mandatory for All Testbenches)**

To ensure that **all primitives, testbenches, rulecheckers, and dictionaries are importable without manual path edits**, every primitive testbench **must** initialize Python’s import path using the canonical project root.

This rule eliminates the recurring issue where `primitive_testbench.py` cannot locate:

- primitive modules  
- testbench modules  
- rulecheckers  
- dictionaries  
- shared utilities  

### **3.7.1 Canonical Project Root Definition**

The project root is defined as:

```
thought_simulator/requirements_20/system_playground/
```

This directory **must** be added to `sys.path` by every primitive testbench.

### **3.7.2 Mandatory Import Path Initialization Block**

Every `<primitive_name>_testbench.py` **must** include the following block at the top of the file:

```python
import os
import sys

# Determine project root dynamically
TB_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(TB_DIR, "..", "..", ".."))

# Add project root to Python import path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
```

This guarantees:

- `primitives/<primitive_name>/<primitive_name>.py` is importable  
- `testbenches/path_a/<category>/<primitive_name>_rulechecker.py` is importable  
- `design/dictionaries/path_a/<dictionary_category>` is importable  
- shared utilities are importable  
- no testbench ever needs manual path edits again  

### **3.7.3 Why This Rule Is Mandatory**

Without this rule:

- Python resolves imports relative to the current working directory  
- testbenches cannot reliably import primitives  
- primitives cannot reliably import dictionaries  
- rulecheckers cannot reliably import shared utilities  
- running testbenches from different directories breaks imports  
- developers must manually patch import paths for every new primitive  

With this rule:

- all imports work automatically  
- all primitives are discoverable  
- all testbenches are discoverable  
- all dictionaries are discoverable  
- `run.py` works from any directory  
- no manual path edits are ever required again  

### **3.7.4 Interaction with Section 3.6 (Directory Schema)**

Section 3.6 defines **where** primitives and testbenches must live.  
Section 3.7 defines **how Python finds them**.

Together, they provide:

- deterministic module discovery  
- deterministic testbench discovery  
- deterministic dictionary discovery  
- deterministic pipeline execution  
- deterministic progressive lineup behavior  

---

### **3.8 Primitive Naming & Registration Discipline (Mandatory for All Path‑A Primitives)**

To ensure that all primitives are discoverable, loadable, and testable without manual edits to `primitive_testbench.py`, `run.py`, or any loader, every primitive must follow strict naming and registration rules.

These rules eliminate the last category of setup issues.

---

## **3.8.1 Primitive Directory Name Must Match Primitive Name**

Every primitive must be located in:

```
primitives/<primitive_name>/<primitive_name>.py
```

Where:

- `<primitive_name>` is lowercase  
- `<primitive_name>` is identical across all files  
- `<primitive_name>` is identical to the directory name  

Examples:

```
primitives/ce/ce.py
primitives/cex_pck/cex_pck.py
primitives/dcb/dcb.py
primitives/rb/rb.py
```

This ensures dynamic loaders can locate the primitive deterministically.

---

## **3.8.2 Primitive Testbench Files Must Use the Same Name**

All testbench files must use the exact primitive name:

```
<primitive_name>_testbench.py
<primitive_name>_testbench.yaml
<primitive_name>_input.yaml
<primitive_name>_rules.yaml
<primitive_name>_tests_to_run.yaml
<primitive_name>_rulechecker.py
```

Example:

```
ce_testbench.py
ce_testbench.yaml
ce_rules.yaml
ce_tests_to_run.yaml
```

This ensures testbench discovery works without hardcoded paths.

---

## **3.8.3 Primitive Must Declare Its Name Internally**

Every primitive must declare:

```python
PRIMITIVE_NAME = "ce"
```

This allows loaders to:

- verify naming consistency  
- auto‑register primitives  
- auto‑locate testbenches  
- auto‑locate dictionaries  
- auto‑locate rulecheckers  

This eliminates the need for manual configuration.

---

## **3.8.4 Primitive Must Provide a Minimal Registration Block**

Every primitive must include:

```python
def get_primitive_name():
    return PRIMITIVE_NAME
```

This allows:

- `run.py` to identify the primitive  
- `primitive_testbench.py` to locate the correct testbench  
- dynamic loaders to validate directory schema compliance  

---

## **3.8.5 Testbench Must Validate Naming Consistency**

Every `<primitive_name>_testbench.py` must include:

```python
from thought_simulator.requirements_20.system_playground.primitives.<primitive_name>.<primitive_name> import get_primitive_name

assert get_primitive_name() == "<primitive_name>", (
    f"Primitive name mismatch: expected <primitive_name>, got {get_primitive_name()}"
)
```

This prevents:

- accidental renaming  
- directory mismatches  
- file mismatches  
- loader failures  
- silent import errors  

---

## **3.8.6 Loader Must Validate Directory Schema Compliance**

Dynamic loaders must verify:

- primitive directory exists  
- primitive module exists  
- testbench directory exists  
- testbench files exist  
- rulechecker exists  
- tests_to_run exists  

If any component is missing, the loader must raise:

```
PrimitiveDiscoveryError("<primitive_name>: missing required component")
```

This ensures developers catch setup errors immediately.

---

## **3.8.7 Why This Section Is Mandatory**

Without naming discipline:

- dynamic loaders fail  
- testbenches fail  
- rulecheckers fail  
- dictionaries fail  
- pipeline execution fails  
- progressive lineup fails  

With naming discipline:

- all primitives become plug‑and‑play  
- no manual edits are ever required  
- the entire Path‑A testing framework becomes self‑discovering  
- new primitives can be added instantly  
- testbenches work automatically  
- rulecheckers work automatically  
- dictionaries load automatically  

This is the final structural requirement needed to eliminate all primitive setup issues.

---

# **3.9 — Mandatory Testbench Output Format (Pass/Fail Reporting)**

To ensure consistent, readable, and diagnostic output across all Path‑A primitives, every primitive testbench **must** implement the following standardized output format.

This format guarantees:

- clear PASS/FAIL visibility  
- consistent reporting across primitives  
- deterministic output structure  
- easy debugging  
- easy CI integration  
- easy human review  

This section applies to **both**:

- Mode `"testbench"`  
- Mode `"general"`

---

## **3.9.1 Required Output Fields for Each Test**

Every testbench **must print** the following fields for each test executed:

### **1. Test Header**
```
------------------------------------------------------------
Running Test: <test_id>
------------------------------------------------------------
```

### **2. Input Source**
Must show **which YAML file** provided the input:

```
- Input Source: <primitive_name>_testbench.yaml (testbench mode)
```

or

```
- Input Source: <primitive_name>_input.yaml (general mode)
```

### **3. Expected Output Source or Validation Method**
Depending on mode:

#### **Testbench mode**
```
- Expected Output Source: <primitive_name>_testbench.yaml (expected block)
```

#### **General mode**
```
- Checked By: <primitive_name>_rules.yaml (rule-driven validation)
```

### **4. PASS/FAIL Result**
```
----- Test Result -----
- PASS: <test_id>
```

or

```
----- Test Result -----
- FAIL: <test_id>
```

### **5. Structural Match (Testbench Mode Only)**
```
- Structural Match: PASS
```

or

```
- Structural Match: FAIL
```

### **6. Rule Violations (General Mode or Diagnostics)**
If none:

```
- Rule Violations: None
```

If present:

```
- Rule Violations:
  * [rule_id] <message>
  * [rule_id] <message>
```

### **7. Context Summary (Mandatory)**
Every testbench must print a short context summary:

```
Context Summary:
- topic: <value>
- stance: <value>
- intent: <value>
- continuity: <value>
- direction: <value>
- coherence: <value>
- importance: <value>
```

This ensures developers can see the envelope state without opening YAML files.

### **8. Foundation / Domain Extras (When Applicable)**

Primitives under foundation or geometric/routing test may **additionally** print domain summaries after the context summary, for example:

**DCB (execution‑flow indexer):**
```
- position / direction / curvature (kappa_exec) / step_index / lane_id
- event_type
- history_len
```

**RB (when RED fields enabled):**
```
- adjacency_class
- displacement_scale
- regime_hint
- selected_ob_ids (count or preview)
```

**IdOB (when foundation logging enabled):**
```
- stability / residue indicators
- regime (shared table)
- role inherit vs reset marker
```

These extras do not replace the mandatory context summary.

---

## **3.9.2 Required Final Summary Block**

At the end of the testbench run, every primitive testbench **must** print:

```
============================================================
 <PRIMITIVE_NAME> Testbench Summary
============================================================
- Total Tests Enabled: <N>
- Passed: <N_pass>
- Failed: <N_fail>

Detailed Results:
- <test_id_1>: PASS
- <test_id_2>: FAIL
...
============================================================
 <PRIMITIVE_NAME> Testbench Runner - Complete
============================================================
```

This summary is mandatory for:

- CI pipelines  
- regression testing  
- human review  
- deterministic replay logs  

---

## **3.9.3 Why This Section Is Mandatory**

Without a standardized output format:

- different primitives produce inconsistent logs  
- debugging becomes harder  
- CI pipelines cannot parse results  
- developers must manually inspect YAML files  
- rulechecker output becomes ambiguous  
- structural mismatches are harder to diagnose  

With this section:

- all primitives produce identical output structure  
- logs become readable and predictable  
- debugging becomes trivial  
- CI pipelines can parse results automatically  
- developers can instantly see context values  
- rule violations become easy to interpret  

---

# **3.10 New Primitive Implementation Scaffold (Mandatory Checklist)**

This section is **general** — it applies to every new Path‑A primitive.
It exists so an implementer (human or AI) can create a complete testbench suite
without reverse‑engineering a prior primitive.

It does **not** define what the primitive computes. That stays in the
primitive’s HLR (20.xx) and structural program (`*_py_struc_pgm.md`).

## **3.10.1 Required File Set**
- `primitives/<prim>/<prim>.py`
- `testbenches/path_a/<category>/`:
  - `<prim>_testbench.py`
  - `<prim>_testbench.yaml`
  - `<prim>_input.yaml`
  - `<prim>_rules.yaml`
  - `<prim>_rules_to_check.yaml` (optional)
  - `<prim>_rulechecker.py`
  - `<prim>_tests_to_run.yaml`

## **3.10.2 Gold‑Standard Reference**
**ISc** is the control-flow reference for dual‑mode runners.  
**DCB / STPX / RBU** are references for structural foundation comparison and boundary tests.  
Copy control flow from ISc; replace domain logic only.

## **3.10.3–3.10.5 Entry points**
- `<prim>.py`: `PRIMITIVE_NAME`, `get_primitive_name()`, class with `process()` (or `run(tp)`)
- `<prim>_testbench.py`: `set_testbench_config`, `run_testbench`, §3.7 import path, both modes
- `<prim>_rulechecker.py`: class with `run()`; methods named by `check:` in rules YAML

## **3.10.6 run.py activation**
Comment previous active block; insert new module path; `"use_<prim>": True`; all other `use_*` False.

## **3.10.7 YAML shapes**
Standard `tests:` / `input` / `expected` / `rules` shapes as used by ISc (or structural expected blocks per §3.11).

## **3.10.8 Implementation order**
HLR → structural program → primitive → rules/rulechecker → fixtures → testbench → run.py → green → then refine internals.

For RB / IdOB: also align fixtures with foundation must‑prove lists and shared regime vocabulary.

## **3.10.9 Not**
Not a substitute for HLR; not a place for domain formulas; not a license for new test architectures.

---

# **3.11 Structural Foundation Comparison (Allowed in Testbench Mode)**

Some Path‑A primitives (notably DCB, STPX, RBU, and future RB/IdOB foundation builds) produce large TP envelopes where full deep equality is brittle while **foundation fields** are what must be locked.

In **testbench mode**, a primitive **may** declare structural foundation comparison instead of full TP deep equality when:

1. The structural program or HLR states that foundation shape is the v1 lock target.  
2. The `expected:` block enumerates the foundation fields explicitly.  
3. Write‑boundary checks ensure non‑owned fields are unchanged when required by the case.  

Examples of foundation fields:

- **DCB:** `geometric_state` (five scalars), history length delta, `event_type`, `provenance.dcb_last_update`  
- **STPX:** cue_envelope four families, provenance  
- **RBU:** meaning‑side commit fields, lineage markers, provenance  
- **RB (when RED enabled):** routing_filter canonical core + `adjacency_class` / `displacement_scale` / `regime_hint`  
- **IdOB:** envelope shape + regime‑conditioned inherit/reset markers  

PASS/FAIL remains driven only by the declared comparison in testbench mode; rulecheckers stay diagnostic in that mode.

---

# **3.12 Foundation Observability (RB / IdOB / $\mathbf{F}$)**

This section aligns progressive testing with `20.50` (v3.0+) and the five `ts_rb_idob_foundations` papers. It is **testing guidance**, not new HLRs.

## **3.12.1 Shared regime vocabulary**

When logging or asserting regime‑related fields, use only:

```
Stable | Refinement | Drift | Transition | Collapse
```

from the shared regime table in `ts_invariant_relational_model.md`. Do not invent alternate regime names in fixtures or rulecheckers.

## **3.12.2 Curvature layer separation in tests**

| Symbol | Layer | Typical TP / log field |
|--------|-------|-------------------------|
| $\kappa_{\text{exec}}$ | DCB execution‑flow | `metadata.geometric_state.curvature` |
| $\kappa_{\text{id}}$ | Identity geometry | IdOB / $\mathbf{F}$ trajectory diagnostics |
| $\kappa_{\text{route}}$ | Routing trajectory | RB / RED diagnostics |

Testbenches and rulecheckers **must not** treat DCB curvature as RB adjacency proof or IdOB identity curvature.

## **3.12.3 RB test focus (aligned with 20.50)**

RB tests should cover, as applicable to the build:

- deterministic routing filter export (canonical order)  
- TR gating (`tr_needs_update` only)  
- multi‑core isolation  
- messy‑input determinism  
- write boundary: no IdOB mutation, no TR write, no DCB ownership writes  
- when RED fields enabled: `adjacency_class`, `displacement_scale`, `regime_hint` determinism  
- missing foundation inputs → deterministic omission/null, not invention  

**Suggested observation questions (general mode / diagnostics):**

1. When $I_{\text{stab}}$ is high, does RB keep `adjacency_class = local`?  
2. When $\|\Delta H\|$ is critical, does RB emit non‑local without masking?  
3. Does RB over‑stabilize under Drift?  
4. Behavior with IdOB view missing vs present?  
5. Do $Rt_{\text{adj}}$ logs conflict with DCB execution order only by layer confusion?  

## **3.12.4 IdOB test focus (aligned with foundation theory)**

IdOB tests should cover, as applicable:

- deterministic $\mathcal{I}$‑compatible envelope updates  
- regime‑conditioned role inherit vs reset  
- residue inherit vs reset tracking $R_{\text{res}}$ directionally  
- provenance extend vs truncate tracking $P_{\text{cont}}$  
- write boundary: no RB routing ownership, no DCB geometric ownership, no Path‑B fields  

## **3.12.5 Optional $\mathbf{F}$ logging**

When examining RB/IdOB space, test runs **may** log per‑cycle approximations of:

$$
\mathbf{F} = (I_{\text{stab}}, R_{\text{res}}, P_{\text{cont}}, L_{\text{depth}}, Rt_{\text{adj}}, \Delta H, E_{\text{dens}}, C_{\text{coh}})
$$

plus the shared regime label. Logging is for observation and IR‑1…IR‑5 falsification; it is not required for every primitive’s green path.

## **3.12.6 Theory document location**

```
thought_simulator/requirements_20/system_playground/design/papers/ts_theory/ts_rb_idob_foundations/
```

---

# **4. Progressive Upstream Selection**

In **general mode**, the user may choose any upstream primitive as the starting point.

Example:

Testing **CEx**  
User sets:

```
use_ie = true
use_cex = true
use_ce = false
```

The **furthest upstream primitive marked true** determines the simulation input:

- If `use_ie = true`, the simulation input is `ie_input.yaml`.  
- If `use_iiinb = true`, the simulation input is `iiinb_input.yaml`.  
- If only `use_cex = true`, the simulation input is `cex_input.yaml`.

### **Progressive Execution Rule:**
All primitives **between** the upstream primitive and the primitive under test:

- are executed normally  
- regardless of their `use_<primitive>` flag  
- because pipeline continuity must be preserved

This is the core meaning of **progressive lineup**.

---

# **5. Primitive Boundary Discipline**

Every primitive has:

- a strict **input envelope**  
- a strict **output envelope**  
- strict **read‑only fields**  
- strict **write‑only fields**  
- strict **forbidden fields**

The lineup verifies:

- primitives do not read fields outside their envelope  
- primitives do not write fields outside their envelope  
- primitives do not modify upstream envelopes  
- primitives do not modify downstream envelopes  
- primitives do not violate bounded‑semantic constraints  
- primitives do not violate determinism  
- primitives do not violate provenance rules  
- foundation layer separation is respected (RB does not own IdOB/DCB fields; IdOB does not own RB routing filter; DCB does not own identity/routing curvature semantics)  

This is essential for:

- replay determinism  
- pipeline safety  
- TP envelope stability  
- Python/C++ parity  
- first‑order RB/IdOB examination  

---

# **6. Pipeline Integration Testing**

Every primitive is tested in full pipeline context. A representative Path‑A order (informative; category placement in §11):

```
InB → IIInB → IE → CEx → CE → WrdNm → ISc → TPU → SOB → SROB → CnOB → SmOB → SSG → STPX → RBU → DCB → IdOB → TR → CTP → RTU → RB → OuBA → SSRGn → MCB
```

Exact interleaving of structure/routing/identity may evolve with HLR sets; progressive tests isolate the primitive under test while preserving continuity between selected upstream and target.

The lineup verifies:

- correct envelope propagation  
- correct provenance propagation  
- correct anomaly propagation  
- correct repair propagation  
- correct context propagation  
- correct identity propagation  
- correct routing propagation  
- correct structural propagation  
- correct execution‑flow geometric accounting (DCB) when in path  
- correct freeze propagation  
- correct replay metadata propagation  

---

# **7. Deterministic Replay Testing**

Replay determinism requires:

- identical inputs → identical outputs  
- identical upstream envelopes → identical downstream envelopes  
- identical repair proposals → identical committed intake  
- identical context → identical CE  
- identical identity selection → identical continuity  
- identical metadata → identical propagation  
- identical pipeline → identical TP(N+1)  
- identical foundation optional inputs → identical RB_out / IdOB envelope fields when those layers are enabled  

The lineup verifies:

- replay metadata correctness  
- deterministic envelope reconstruction  
- deterministic primitive behavior  
- deterministic pipeline behavior  
- deterministic Python/C++ parity  

---

# **8. Python/C++ Parity Testing**

Every primitive must produce identical outputs in:

- Python implementation  
- C++ implementation

The lineup verifies:

- identical envelope shapes  
- identical provenance  
- identical anomaly detection  
- identical repair proposals  
- identical committed intake  
- identical context extraction  
- identical structural geometry  
- identical routing vectors / filters  
- identical identity refinement  
- identical freeze metadata  
- identical TP(N+1)  
- identical enabled foundation RB/IdOB fields  

Parity failures are treated as critical.

---

# **9. Existing IIInB + IE Sections (Preserved and Updated)**

All content from the previous version (v3.2) describing:

- IIInB behavior  
- IIInB anomaly taxonomy  
- IIInB repair proposals  
- IE behavior  
- IE bounded‑semantic operations  
- IE structural construction  
- IE replay metadata  
- IE Python/C++ parity  
- IE propagation rules  

is preserved exactly, with minor corrections for clarity and alignment.

*(Full content preserved exactly as in the attached historical document — omitted here only to avoid duplication in chat. When merging historically expanded IIInB/IE annexes, keep them under this section without dropping cases.)*

---

# **10. Downstream Primitive Testing**

The progressive lineup explicitly covers downstream primitives:

### **CEx**
- identity selection  
- bounded semantic extraction  
- next‑turn context reflection  
- clarifying metadata extraction  
- provenance  
- audit  
- skip conditions  
- fallback  
- new‑conversation detection  
- metadata boundaries  

### **CE**
- context envelope construction  
- context coherence  
- context direction  
- context importance  
- context continuity  
- provenance  
- audit  

### **ISc**
- scoring metadata  
- entropy updates  
- conflict detection  
- provenance  

### **TPU**
- commit boundaries  
- envelope immutability  
- provenance  
- replay metadata  

### **OB‑Set (SOB, SROB, CnOB, SmOB)**
- structural geometry  
- semantic geometry  
- residue metadata  
- provenance  

### **STPX**
- four‑family cue envelope  
- structural cue boundaries  
- provenance  

### **RBU**
- meaning‑side commit (identity/stance/register/tone/tags)  
- lineage markers  
- write boundary  
- provenance  

### **DCB**
- geometric_state five‑field overwrite  
- geometric_history append‑only  
- cycle_start / delta events  
- $\kappa_{\text{exec}}$ sequential rule  
- layer separation from $\kappa_{\text{id}}$ / $\kappa_{\text{route}}$  
- provenance `dcb_last_update`  

### **IdOB**
- identity refinement / envelope  
- qualifier clustering  
- subculture assignment  
- regime‑conditioned inherit vs reset (foundation)  
- provenance  

### **TR / CTP / RTU**
- routing vectors / arbitration support  
- routing metadata  
- provenance  

### **RB**
- deterministic routing filter  
- TR gating  
- multi‑core isolation  
- split/merge arbitration  
- messy‑input determinism  
- when RED enabled: adjacency_class, displacement_scale, regime_hint  
- IdOB non‑mutation; $\kappa$ layer separation  
- provenance / inspectability  

### **OuBA / SSRGn / MCB**
- freeze metadata  
- SSR‑A / SSR‑B  
- meaning continuity basin behavior as applicable  
- provenance  

All primitives follow the same two‑mode testing system.

---

# **11. Location of Testbench Primitive Files**

**testbenches/path_a/**

intake:
- inb
- iinb / iiinb
- ie

encoder:
- cex_ie
- cex_ccr
- cex_pck
- ce

transform:
- tpu

semantic:
- sob
- srob
- cnob
- smob

structure:
- wrdnm
- isc
- ssg
- stpx
- rbu

routing:
- dcb
- rb
- tr
- ctp
- rtu

identity:
- idob
- mcb

output:
- ouba

---

# **12. Summary**

The **Progressive Lineup Testing Framework** is the authoritative testing strategy for **all Path‑A primitives**.

It provides:

- deterministic testbench mode  
- flexible general mode  
- progressive upstream selection  
- passthrough behavior  
- rule‑driven validation  
- primitive boundary discipline  
- pipeline integration testing  
- deterministic replay testing  
- Python/C++ parity testing  
- structural foundation comparison where declared  
- foundation observability for RB / IdOB / $\mathbf{F}$  
- complete IIInB + IE intake testing  
- complete downstream primitive testing including STPX, RBU, DCB, RB  

This document is aligned with:

- 20.101 (IIInB)  
- 20.109 (IE)  
- 20.107 (CEx)  
- 20.108 (CE)  
- 20.105 (TP requirements + metadata + provenance + usage)  
- 20.50 (RB v3.0+)  
- 20.106 (DCB) and related structure primitives  
- Path‑A scaffold (20.15)  
- `ts_rb_idob_foundations` first‑order theory set  
- run.py  
- all structural programs  
- all testbench YAMLs  
- all rule‑checking systems  

---

# **End of Document — progressive_lineup_testing.md (Version 4.2)**

---
