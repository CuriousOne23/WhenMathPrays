# OB Validation Test Corpus
**ob_validation_test_corpus.md**  
**Revision:** 1.0 (Initial Draft)  
**Date:** 2026-06-20  
**Status:** Working Draft – For Review by CuriousOne23 & CP  

---

### 1. Purpose

Please see [OB_development_playbook.md](OB_development_playbook.md) for complete list of documents which pertain to the OB system playground papers.

This document is the **official validation test corpus** for the OB pipeline (SOB → SROB → CnOB → SmOB).

It contains a growing set of test cases designed to:
- Validate architectural invariants
- Expose edge cases, ambiguity, and degradation patterns
- Test monotonicity, residue quality, and RB readiness
- Serve as a regression suite for future changes to rules, tags, constraints, or hooks
- Provide concrete examples for implementation testing

This corpus complements (and expands upon) the lighter examples in `ob_pipeline_examples.md`.

### 2. Validation Criteria (Applied to Every Test Case)

Every test case must be evaluated against these criteria:

- Strict pre-semantic boundaries maintained
- Monotonic entropy reduction across layers
- No semantic leakage
- Full provenance and traceability
- Proper uncertainty and gap propagation
- RB-ready output (`structural_signature`, `residue`, `bindings`, entailment edges)
- Replay equivalence

---

# **3. Standardized Output Format (Required for All Test Evaluations)**

To ensure consistent, comparable results across contributors and LLM‑based simulators (e.g., Grok, Copilot), all OB validation tests **must** report results using the following schema.  
This standardization enables deterministic evaluation, automated comparison, and uniform pass/fail logic across revisions.

---

### **3.1 Required Metrics**

Each test must output the following fields:

- **`entropy_delta`** — numeric, expected ≤ 0  
- **`curvature_score`** — numeric, expected ≥ 0  
- **`routing_correct`** — boolean  
- **`provenance_preserved`** — boolean  
- **`replay_equivalence`** — boolean  
- **`residue_quality`** — numeric in [0,1]  
- **`layer_independence`** — boolean  

---

### **3.2 Thresholds for Pass/Fail**

A test **passes** if:

- `entropy_delta ≤ -0.01`  
- `curvature_score ≥ 0`  
- `routing_correct = true`  
- `provenance_preserved = true`  
- `replay_equivalence = true`  
- `residue_quality ≥ 0.85`  
- `layer_independence = true`  

If any invariant fails, the test fails.

---

### **3.3 Required Output Format**

Simulators must output results in the following JSON structure:

```json
{
  "test_id": "OBx",
  "metrics": {
    "entropy_delta": -0.12,
    "curvature_score": 0.03,
    "routing_correct": true,
    "provenance_preserved": true,
    "replay_equivalence": true,
    "residue_quality": 0.91,
    "layer_independence": true
  },
  "overall_pass": true,
  "notes": "Optional freeform commentary."
}
```

---

### **3.4 Aggregate Summary (Multi‑Test Runs)**

For multi‑test runs, simulators must also output:

```json
{
  "total_tests": N,
  "passed": P,
  "failed": F,
  "pass_rate": P/N
}
```

---

### **3.5 Purpose of This Standard**

This schema ensures:

- reproducibility  
- cross‑revision comparability  
- consistent Grok/Copilot behavior  
- machine‑readable results  
- clear invariant enforcement  

It also prevents drift in how tests are interpreted or reported.

---

### 4. Test Cases

#### Category 1: Clean / Happy Path
**Test 1.1** – Simple declarative sentence  
**Input:** `The sky is blue.`  
**Expected Behavior:** Clean flow, minimal constraints, strong residue for basic meaning attachment.  
**Validation Focus:** Happy path, monotonicity, clean handoff.

**Test 1.2** – Compound sentence  
**Input:** `She ran quickly and won the race.`  
**Expected Behavior:** Multiple spans, adjacency relations, structural grouping.  
**Validation Focus:** Span handling and parallel structures.

#### Category 2: Repetition & Structural Patterns
**Test 2.1** – Intentional repetition  
**Input:** `Never, never, never give up.`  
**Expected Behavior:** `REPEAT_UNIT` tags preserved, uncertainty on rhetorical vs structural intent.  
**Validation Focus:** Repetition handling without semantic collapse.

**Test 2.2** – Parallel structures  
**Input:** `She came, she saw, she conquered.`  
**Expected Behavior:** `PARALLEL_UNIT` detection, structural parallelism preserved.  
**Validation Focus:** Parallel construction without assuming meaning.

#### Category 3: Ambiguity & Multiple Parses
**Test 3.1** – Classic ambiguity  
**Input:** `Time flies like an arrow.`  
**Expected Behavior:** Multiple possible groupings preserved with uncertainty markers.  
**Validation Focus:** Ambiguity preservation for RB.

**Test 3.2** – Pronoun reference ambiguity  
**Input:** `John told Bill he was wrong.`  
**Expected Behavior:** Structural ambiguity marked, no forced referent resolution.  
**Validation Focus:** Referent anchor handling.

#### Category 4: Contradiction & Inconsistency
**Test 4.1** – Direct contradiction  
**Input:** `John is here. John is not here.`  
**Expected Behavior:** Strong contradiction constraint in CnOB, preserved in SmOB.  
**Validation Focus:** Contradiction handling without forced resolution.

**Test 4.2** – Subtle inconsistency  
**Input:** `The door was open. The door was locked.`  
**Expected Behavior:** Constraint conflict flagged.  
**Validation Focus:** Monotonic constraint accumulation.

#### Category 5: Degradation & Noise
**Test 5.1** – Heavy punctuation / typos  
**Input:** `Hello!!! world?? what r u doing...`  
**Expected Behavior:** Punctuation clusters, density tags, uncertainty propagation.  
**Validation Focus:** Graceful degradation.

**Test 5.2** – Fragmented / incomplete input  
**Input:** `The meeting was... never mind.`  
**Expected Behavior:** Gap markers and closure constraints.  
**Validation Focus:** Incomplete structure handling.

#### Category 6: Edge Cases
**Test 6.1** – Very short input  
**Input:** `Yes.`  

**Test 6.2** – Empty / whitespace-only input  
**Input:** ` ` (empty or whitespace)

**Test 6.3** – Extremely long single sentence (future scalability test)

---

### 5. Validation Summary Template

For each new test case, record:

- Input
- Expected key behaviors per layer
- Validation results against criteria
- Any discovered issues or rule gaps
- RB routing readiness score

---

### 6. Usage Guidelines

- Run the full corpus after any change to tags, rules, constraints, or hooks.
- Maintain a results log showing pass/fail + metrics.
- Add new test cases whenever a new edge case or failure mode is discovered.
- Use these examples for automated regression testing when available.

---

### 7. Next Steps / Open Items

- Expand corpus to 20–30 cases (including adversarial and long-context)
- Add automated validation harness when implementation begins
- Create “golden output” files for each test case (expected OB pipeline output)
- Use corpus to validate future rule expansions (R1–Rk, C1–C7, H1–Hn)

---

**End of Draft – ob_validation_test_corpus.md (Rev 1.0)**

---
