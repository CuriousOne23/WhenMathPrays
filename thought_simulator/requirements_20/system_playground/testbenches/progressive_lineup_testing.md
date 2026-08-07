# **progressive_lineup_testing.md — Path‑A Progressive Lineup Testing Framework (Version 4.0)**  
**Status:** Active  
**Scope:** All Path‑A primitives  
**Applies To:** IIInB, IE, CEx, CE, ISc, TPU, SOB, SROB, CnOB, SmOB, IdOB, TR, CTP, RTU, RB, OuBA, SSRGn  
**Exception:** InB (partially tested; no upstream primitive)

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

# **3. Two Testing Modes**

Testing is controlled by `mode` in `run.py`.

There are **two modes**, and **every primitive** supports both.

---

## **3.1 Mode A — “testbench” (Strict Deterministic Testing)**

### **Input File:**  
`<primitive>_testbench.yaml`

### **Behavior:**  
- The testbench loads **full inputs** for the primitive.  
- The testbench loads **full expected outputs**.  
- The primitive is executed.  
- Actual output is compared to expected output.  
- PASS/FAIL is determined by exact equality.
- In testbench mode, the rulechecker may optionally run for diagnostic purposes; however, PASS/FAIL is determined solely by the testbench YAML.

### **Passthrough Behavior:**  
If `use_<primitive> = false` in `run.py`:

- The primitive is **not executed**.  
- Its input is **passed through unchanged**.  
- This is used for pipeline debugging and isolating upstream behavior.

### **Purpose:**  
- Canonical correctness  
- Deterministic replay  
- Regression testing  
- Python/C++ parity

---

## **3.2 Mode B — “general” (Rule‑Driven Testing)**

### **Input File:**  
`<primitive>_input.yaml`

### **Behavior:**  
- The testbench loads **only the primitive’s inputs**.  
- The primitive is executed.  
- Output is validated using **rules**, not expected outputs.

### **Rule System:**  
- `cex_rules.yaml` (or `<primitive>_rules.yaml`)  
- `cex_rulechecker.py` (or `<primitive>_rulechecker.py`)

Rules define:

- allowed fields  
- forbidden fields  
- bounded‑semantic constraints  
- provenance expectations  
- envelope boundaries  
- skip conditions  
- fallback behavior  
- continuity behavior  
- deterministic replay behavior

### **Purpose:**  
- Flexible exploratory testing  
- Rapid scenario construction  
- Upstream variation testing  
- Rule‑driven correctness  
- Pipeline safety validation

---

# ⭐ **New Section 3.3 — Primitive Input, Rules, Rulechecking, and Test Selection Files**

The Progressive Lineup Testing Framework uses four auxiliary files to support deterministic testbench mode and rule‑driven general mode. These files define inputs, rule constraints, rulechecking behavior, and test selection.

This section explains how each file is used and how they interact with `run.py` in both testing modes.

---

## **3.3.1 `primitive_input.yaml` — Input Source for General Mode**

Used **only in Mode B (“general”)**.

This file provides **user‑defined input envelopes** for the primitive under test.  
It allows the user to construct arbitrary scenarios without requiring full expected outputs.

### **Purpose**
- Supply the primitive’s input envelope in general mode.  
- Allow flexible scenario construction.  
- Enable upstream variation testing.

### **Flow**
1. `run.py` is set to **general mode**.  
2. The testbench loads `<primitive>_input.yaml`.  
3. The primitive executes normally.  
4. Output is validated by rulechecking (not by expected outputs).

This aligns with the general‑mode behavior described in Section 3.2.

---

## **3.3.2 `primitive_rules.yaml` — Rule Definitions for General Mode**

Used **only in Mode B (“general”)**.

This file defines the **rule set** the primitive must obey.  
Rules describe what the primitive is allowed to output, how envelopes must behave, and what constraints must hold.

### **Contents**
- Allowed fields  
- Forbidden fields  
- Bounded‑semantic constraints  
- Provenance requirements  
- Envelope boundaries  
- Continuity expectations  
- Replay determinism constraints  
- Skip/fallback conditions  

These rule types correspond to the rule system described in Section 3.2.

### **Flow**
1. Primitive executes using input from `primitive_input.yaml`.  
2. `primitive_rules.yaml` is loaded by the rulechecker.  
3. Each rule is applied to the primitive’s output.  
4. PASS/FAIL is determined by rule compliance.

---

## **3.3.3 `primitive_rulescheck.py` — Rulechecker Execution Logic**

This Python file performs the **actual rulechecking** in general mode.

It is invoked by `primitive_testbench.py` when `run.py` is in general mode.

### **Responsibilities**
- Load `primitive_rules.yaml`.  
- Validate the primitive’s output against all rules.  
- Produce diagnostic information.  
- Enforce deterministic replay behavior.  
- Ensure envelope discipline and provenance correctness.

### **Flow**
1. Primitive runs.  
2. Output is passed to `primitive_rulescheck.py`.  
3. Rulechecker loads `primitive_rules.yaml`.  
4. Rulechecker evaluates all constraints.  
5. PASS/FAIL is returned to the testbench.

This complements the rule‑driven validation described in Section 3.2.

### **Note**
In testbench mode, rulechecking may run **only for diagnostics**, but PASS/FAIL is determined solely by expected outputs (Section 3.1).

---

## **3.3.4 `primitive_tests_to_run.yaml` — Test Selection for Testbench Mode**

Used **only in Mode A (“testbench”)**.

This file determines **which testbench tests should run** for the primitive.

### **Purpose**
- Allow selective execution of testbench tests.  
- Enable fast regression cycles.  
- Allow skipping expensive or irrelevant tests.

### **Contents**
Each test has a boolean flag:

- `true` → testbench will run the test  
- `false` → testbench will skip the test

### **Flow**
1. `run.py` is set to **testbench mode**.  
2. `primitive_testbench.py` loads `primitive_tests_to_run.yaml`.  
3. Only tests marked `true` are executed.  
4. Each test loads `<primitive>_testbench.yaml` (expected inputs + expected outputs).  
5. Primitive runs.  
6. Actual output is compared to expected output for PASS/FAIL.

This aligns with the deterministic testbench behavior described in Section 3.1.

---

# ⭐ **3.3.5 Unified Flow Summary**

### **Mode A — Testbench (Deterministic)**  
Files used:
- `<primitive>_testbench.yaml`  
- `primitive_tests_to_run.yaml`  

Flow:
1. Load test selection.  
2. For each enabled test:  
   - Load full input + expected output.  
   - Execute primitive.  
   - Compare actual vs expected.  
   - PASS/FAIL by equality.

Rulechecker optional for diagnostics only.

---

### **Mode B — General (Rule‑Driven)**  
Files used:
- `<primitive>_input.yaml`  
- `primitive_rules.yaml`  
- `primitive_rulescheck.py`  

Flow:
1. Load general input.  
2. Execute primitive.  
3. Load rules.  
4. Rulechecker validates output.  
5. PASS/FAIL by rule compliance.

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

Every primitive is tested in full pipeline context:

```
InB → IIInB → IE → CEx → CE → ISc → TPU → SOB → SROB → CnOB → SmOB → IdOB → TR → CTP → RTU → RB → OuBA → SSRGn
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

This document is now fully aligned with:

- 20.101 (IIInB)  
- 20.109 (IE)  
- 20.107 (CEx)  
- 20.108 (CE)  
- 20.105 (TP requirements + metadata + provenance + usage)  
- Path‑A scaffold (20.15)  
- run.py  
- all structural programs  
- all testbench YAMLs  
- all rule‑checking systems

---

# **End of Document — progressive_lineup_testing.md (Version 4.0)**

---
