# **progressive_lineup_testing.md — Path‑A Progressive Lineup Testing Framework (Version 4.1)**  
**Status:** Active  
**Scope:** All Path‑A primitives  
**Applies To:** IIInB, IE, CEx, CE, WrdNm, ISc, TPU, SOB, SROB, CnOB, SmOB, IdOB, TR, CTP, RTU, RB, OuBA, SSRGn  
**Exception:** InB (partially tested; no upstream primitive)

**v4.1 (informative addenda, no prior section removed):** IdOB isolation suite, declared-key expected blocks, utterance on the log, lineup order vs primitive HLR schedule. Requirements for IdOB remain in `20.40.050`.

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

This framework is **not a requirements document**.  
It describes **how primitives are tested**, not **what they must do**.

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

The lineup is **progressive** because:

- The user can choose any upstream primitive as the starting point.  
- All primitives between that upstream primitive and the primitive under test are executed normally.  
- The primitive under test is validated either by expected outputs or by rule‑checking.

---

## **3. Testing Modes (Authoritative Operational Definition)**  
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
  - `expected:` — the complete expected TP output envelope  
- The primitive is executed once using the `input:` envelope.
- The primitive’s output is compared **field‑by‑field** against `expected:`.  
- PASS/FAIL is determined **solely** by exact equality with the expected output.

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

### **3.1.1 Declared-key expected blocks (packet primitives)** *(v4.1, does not repeal §3.1)*

When a primitive’s owned write is a **named packet** rather than a full TP clone (IdOB: `tp.idob`), the `expected:` block MAY list **only the declared keys** for that packet. Comparison is exact equality on those keys. Fields not listed are not part of PASS/FAIL.

A primitive MAY also gate testbench PASS on its rulechecker when the structural program says the walls are part of the hop (IdOB write-boundary, rank ⊆ map, utterance present). That is an addition to §3.1 for packet primitives, not a silent change to CE/IE full-envelope tests.

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

---

## ⭐ **3.3 Mandatory Input‑Source Rule (New Explicit Requirement)**  
To prevent ambiguity and ensure deterministic behavior across all Path‑A primitives:

### **All primitive testbenches MUST implement the following rule:**

| `mode` value in run.py | Input file loaded by `<primitive>_testbench.py` | Output validation method |
|------------------------|--------------------------------------------------|---------------------------|
| `"testbench"`          | `<primitive>_testbench.yaml` (input + expected) | Exact equality comparison |
| `"general"`            | `<primitive>_input.yaml` (input only)           | Rulechecking only         |

This rule is **mandatory**, applies to **all Path‑A primitives**, and must be implemented exactly as written.

Packet primitives (§3.1.1) still load those same files; only the *shape* of `expected:` may be a key subset.

---

## ⭐ **3.4 Why This Rule Exists (Clarification for Developers)**  
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

## ⭐ **3.5 Unified Flow Summary (Updated)**

### **Mode A — Testbench (Deterministic)**  
Files used:
- `<primitive>_testbench.yaml`  
- `<primitive>_tests_to_run.yaml`  

Flow:
1. Load test selection.  
2. For each enabled test:
   - Load full input + expected output from `<primitive>_testbench.yaml`.  
   - Execute primitive.  
   - Compare actual vs expected.  
   - PASS/FAIL by exact equality.  
3. Rulechecker optional (diagnostics only).

Packet primitives: step 3 may be required by the structural program (§3.1.1).

---

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
primitives/ccr/ccr.py
primitives/idob/idob.py
```

This path is **authoritative** and is used by the dynamic primitive loader.

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
            <primitive_name>_rules.yaml
            <primitive_name>_tests_to_run.yaml
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
 context
```

Example (CE):

```
testbenches/path_a/semantic/ce_testbench.py
testbenches/path_a/semantic/ce_testbench.yaml
testbenches/path_a/semantic/ce_rules.yaml
testbenches/path_a/semantic/ce_tests_to_run.yaml
```

IdOB:

```
testbenches/path_a/identity/idob_testbench.py
testbenches/path_a/identity/idob_testbench.yaml
testbenches/path_a/identity/idob_rules.yaml
testbenches/path_a/identity/idob_tests_to_run.yaml
testbenches/path_a/identity/idob_input.yaml
testbenches/path_a/identity/idob_rulechecker.py
```

This ensures that **every primitive testbench is discoverable by pattern**, not by hardcoded paths.

---

## **3.6.3 Primitive Dictionary / Lookup‑Table Location (If Required)**  

Dictionaries and scalar tables may live in **one of two places**, chosen by size and ownership:

### **A. Small, exclusive tables (preferred for most Path‑A primitives)**  
When the tables are small, numerous, and owned exclusively by a single primitive (the common case for WrdNm, SOB, SROB, CnOB, SmOB, IdOB crossing tables, etc.), they **may** live inside the primitive directory itself:

```
thought_simulator/
  requirements_20/
    system_playground/
      primitives/
        <primitive_name>/
          <table_or_dict>.yaml
```

This keeps the primitive self‑contained and avoids unnecessary path complexity.

IdOB hop tables (`structure_card.examples.yaml`, `meaning_groups.yaml`, `struct_to_meaning_map.yaml`, `ranking_weights.yaml`, `cie.examples.yaml`, `pack_base_en.yaml`, `semantic_*.yaml`, `idob_s2m_packet.yaml`, `residue_next.examples.yaml`) live here.

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
Loaders and primitives SHALL look first in the primitive’s own directory, then (if not found) in the corresponding `design/dictionaries/path_a/<category>/` location.  
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

This allows loaders to read the primitive name directly from the module, further reducing configuration overhead..

---

## ⭐ **3.6.6 Nested TP Field Path Convention (Mandatory for Schema‑Driven Primitives)**  

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
| `idob.meaning_delta_h` | `TP.idob.meaning_delta_h` |

### **Why this rule exists**

- Prose and architecture diagrams often say “TP.metadata…” for readability.  
- Schema authors and implementers naturally copy that prefix into machine paths.  
- Resolvers start at the TP root, so a leading `TP.` looks for a key that does not exist and silently falls back (often to `0` / empty).  
- That failure mode is hard to spot until exact‑equality tests fail on a single field.

### **Scope**

Applies to **all** Path‑A primitives that read or declare nested TP paths, including (but not limited to) schema‑driven encoders such as WrdNm and any future ISc / scoring field maps.

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
primitives/ccr/ccr.py
primitives/idob/idob.py
```

This ensures dynamic loaders can locate the primitive deterministically.

---

## **3.8.2 Primitive Testbench Files Must Use the Same Name**  
All testbench files must use the exact primitive name:

```
<primitive_name>_testbench.py
<primitive_name>_testbench.yaml
<primitive_name>_rules.yaml
<primitive_name>_tests_to_run.yaml
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

# ⭐ **New Section 3.9 — Mandatory Testbench Output Format (Pass/Fail Reporting)**  
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

### **7a. Owned-envelope summary (packet primitives)** *(v4.1)*

When the object under test is not the CE context envelope, the testbench MAY print that owned object instead of (or in addition to) the seven CE fields. IdOB SHALL print at least:

- utterance (carrier)  
- input card_id / cie_id / packs_loaded  
- slim `tp.idob` (status, key, residue, selected group, Δh, flags)  

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

This is essential for:

- replay determinism  
- pipeline safety  
- TP envelope stability  
- Python/C++ parity

---

# **6. Pipeline Integration Testing**

Official Path A flow (`20.15` v4.1). Lineup diagrams in this framework use this schedule:

```
InB (Beginning of Path A) → IIInB → IE → CEx → CE → TPU → SOB → SROB → CnOB → SmOB
  → WrdNm → ISc → SSG → STPX → RBU → DCB → TR → CTP → RB
  → WrdNm → ISc → RTU → TR → CTP → RB → IdOB → MCB → RBU → DCB
  → TR → CTP → RB → WrdNm → ISc → RTU → TR → CTP → RB → IdOB → MCB → RBU → . . .
OR
DCB → TR → CTP → RB → WrdNm → ISc → RTU → TR → CTP → RB → OuBA (End of Path A)
```

IdOB runs after a committed RB. Isolation fixtures may start at IdOB without the live RB to its left.

Historical compact walk (neighbor discovery only; does not override the official flow):

```
InB → IIInB → IE → CEx → CE → WrdNm → ISc → TPU → SOB → SROB → CnOB → SmOB → IdOB → TR → CTP → RTU → RB → OuBA → SSRGn
```

The lineup verifies:

- correct envelope propagation  
- correct provenance propagation  
- correct anomaly propagation  
- correct repair propagation  
- correct context propagation  
- correct identity propagation  
- correct routing propagation  
- correct structural propagation  
- correct freeze propagation  
- correct replay metadata propagation
```

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
- identical routing vectors  
- identical identity refinement  
- identical freeze metadata  
- identical TP(N+1)

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

*(Full content preserved exactly as in your attached document — omitted here only to avoid duplication in chat. When you paste this into GitHub, you will merge the preserved IIInB/IE sections directly.)*

---

# **10. Downstream Primitive Testing (New Section)**

The progressive lineup now explicitly covers all downstream primitives:

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

### **IdOB**  
- identity refinement  
- qualifier clustering  
- subculture assignment  
- provenance  
- **v4.1 crossing (enabled isolation suite):** utterance carrier; six-ID structure / key; map door; rank ⊆ map; six-axis $M$; CIE ($M'=\mathrm{clip}(M+\alpha I)$); $\Delta h$; split flags; write-boundary on `routing_filter`  
- lifecycle formation…closure envelopes remain archived (`idob_lifecycle_archive.yaml`) and are **not** the enabled expected block  

CIE = Conversational Identity Envelope (stance / hold for the hop). Defined normatively in `20.40.050` §0.6.

### **TR / CTP / RTU / RB**  
- routing vectors  
- arbitration  
- routing metadata  
- provenance

### **OuBA / SSRGn**  
- freeze metadata  
- SSR‑A  
- SSR‑B  
- provenance

All primitives follow the same two‑mode testing system.

---

## **10.1 Context Pipeline Primitive Testing (COB, CIL, CST‑Core, CST‑MS, CST‑MUX)**

The Path‑A Progressive Lineup Testing Framework now formally includes the **context pipeline**, consisting of:

- **COB** — Context Object Builder  
- **CIL** — Context Integration Layer  
- **CST‑Core** — Core Context State Tracker  
- **CST‑MS** — Multi‑Signal Context State Tracker  
- **CST‑MUX** — Context Multiplexer  

These primitives follow *exactly the same* two‑mode testing system defined in Sections **3.1–3.3**, including:

- deterministic **testbench mode** (input + expected)  
- rule‑driven **general mode** (input only + rulechecker)  
- mandatory directory schema for primitive discovery
- mandatory import‑path initialization  
- mandatory naming discipline and registration    
- mandatory standardized PASS/FAIL output format  

---

## **10.2 Directory Schema for Context Pipeline Primitives**

A new directory is added under **testbenches/path_a**:

```
testbenches/path_a/context/
```

This directory contains the testbenches for:

```
cob_testbench.py
cob_testbench.yaml
cob_rules.yaml
cob_tests_to_run.yaml

cil_testbench.py
cil_testbench.yaml
cil_rules.yaml
cil_tests_to_run.yaml

cst_core_testbench.py
cst_core_testbench.yaml
cst_core_rules.yaml
cst_core_tests_to_run.yaml

cst_ms_testbench.py
cst_ms_testbench.yaml
cst_ms_rules.yaml
cst_ms_tests_to_run.yaml

cst_mux_testbench.py
cst_mux_testbench.yaml
cst_mux_rules.yaml
cst_mux_tests_to_run.yaml
```

Primitive implementations live under the new **primitives** subdirectories:

```
primitives/cob/cob.py
primitives/cil/cil.py
primitives/cst_core/cst_core.py
primitives/cst_ms/cst_ms.py
primitives/cst_mux/cst_mux.py
```

This follows the mandatory schema in Section **3.6.1** and **3.6.2**.

---

## **10.3 Context Pipeline Progressive Lineup Behavior**

Context primitives participate in progressive lineup testing exactly like Path‑A primitives:

### **Upstream selection**
If the user enables:

```
use_cob = true
use_cil = true
use_cst_core = true
use_cst_ms = true
use_cst_mux = true
```

then:

- the furthest upstream enabled primitive determines the simulation input  
- all downstream context primitives execute normally (even if use_<primitive> = false), preserving pipeline continuity  
- deterministic replay is enforced across all five primitives  

This mirrors the progressive upstream rule in Section **4**.

---

## **10.4 Context Pipeline Boundary Discipline**

Each context primitive has strict envelope boundaries, consistent with Section **5**:

- **COB** may construct context objects but must not modify upstream TP fields  
- **CIL** may merge context signals but must not alter COB outputs except through defined integration rules  
- **CST‑Core** may update core context state only within its declared envelope  
- **CST‑MS** may update multi‑signal state only within its declared envelope  
- **CST‑MUX** may select or merge context branches but must not mutate upstream envelopes  

All forbidden‑field, read‑only, and write‑only rules apply identically.

---

## **10.5 Deterministic Replay & Python/C++ Parity**

All context primitives must satisfy deterministic replay rules in Section **7** and parity rules in Section **8**:

- identical inputs → identical outputs  
- identical upstream envelopes → identical downstream envelopes  
- identical context signals → identical CST‑Core/CST‑MS/CST‑MUX outputs  
- identical COB/CIL behavior across Python and C++  

Parity failures are critical.

---

## **10.6 Mandatory Testbench Output Format**

All context pipeline testbenches must use the standardized PASS/FAIL format defined in Section **3.9**, including:

- test header  
- input source  
- expected output source or rulechecker  
- PASS/FAIL  
- structural match (testbench mode)  
- rule violations (general mode)  
- context summary  
- final summary block  

This ensures uniformity across Path‑A and context primitives.

---

## **10.7 IdOB isolation suite (v4.1)**

Enabled cases: `idob_s2m_01` … `idob_s2m_06` in `idob_testbench.yaml` / `idob_tests_to_run.yaml`.

Each enabled case records the **utterance**. Expected keys are packet fields (`resolution_status`, `selected_group_id`, flags, residue, …), not formation…closure geometry.

Kernel: `primitives/idob/idob.py` loading YAML only from `primitives/idob/`.

Do not point the lineup at a classroom slide directory as a test oracle.

---

# **11. Summary**

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
- complete IIInB + IE intake testing  
- complete downstream primitive testing  
- packet-primitive declared-key expected blocks (§3.1.1)  

This document is now fully aligned with:

- 20.101 (IIInB)  
- 20.109 (IE)  
- 20.107 (CEx)  
- 20.108 (CE)  
- 20.105 (TP requirements + metadata + provenance + usage)  
- 20.40.050 (IdOB, v3.1 crossing + CIE)  
- Path‑A scaffold (20.15)  
- run.py  
- all structural programs  
- all testbench YAMLs  
- all rule‑checking systems

---

# **End of Document — progressive_lineup_testing.md (Version 4.1)**

---
