# IIInB – Python Structural Program (Proposal‑Only, Non‑Mutating)

This document is the **normative structural specification** for the Python implementation of the **IIInB** primitive, aligned with:

- 20.101_iiinb_prim.md (rewritten)
- 20.15_ts_architecture_scaffold.md (deterministic replay)
- 20.105_tp_requirements.md (TP envelope)
- 20.105.010_tp_meta_fields.md
- 20.105.020_tp_meta_provenance.md
- 20.105.030_tp_meta_usage.md
- system_playground/primitives/iiinb/iiinb.py (mechanical implementation)
- system_playground/testbenches/path_a/intake/iiinb_testbench.yaml
- system_playground/testbenches/path_a/intake/iiinb_testbench.py
- system_playground/testbenches/progressive_lineup_testing.md

Any change to IIInB behavior, TP envelope shape, rule ordering, provenance semantics, or replay determinism **MUST** be reflected here.

---

## 1. Canonical Synchronization Set

The following artifacts define IIInB’s conceptual, structural, and mechanical behavior:

- Conceptual primitive spec: `20.101_iiinb_prim.md`
- Architecture scaffold: `20.15_ts_architecture_scaffold.md`
- TP envelope requirements: `20.105_tp_requirements.md` and meta‑field documents
- Python implementation: `iiinb.py`
- Structural program: `iiinb_py_struc_pgm.md` (this file)
- Testbenches:  
  - `iiinb_testbench.yaml`  
  - `iiinb_testbench.py`  
  - `progressive_lineup_testing.md`
- Dictionary rule sets: `iiinb_dct_rules/*.yaml`
- Rulechecker: `iiinb_rulechecker.py`

**Normative rule:**  
All changes to IIInB **MUST** be synchronized across this set.

---

## 2. TP Envelope (Proposal‑Only)

IIInB is a **pre‑semantic, non‑mutating, proposal‑only** primitive.  
It produces a deterministic TP envelope with **no normalization**, **no repair application**, and **no surface/token mutation**.

### 2.1 Canonical TP Envelope Schema

IIInB **MUST** output a Python dict with the following shape:

```python
{
    "iiinb_status": str,        # always "inspected"
    "repair_proposals": list,   # token‑span repair proposals
    "anomaly_flags": list,      # token‑span anomaly flags
    "intake_surface": str,      # original surface (unchanged)
    "intake_tokens": list[str], # tokens from original surface (unchanged)
}
```

### 2.2 Normative Constraints

- **MUST:** All fields must be present.
- **MUST:** Field names and types must match exactly.
- **MUST:** No additional top‑level fields may be added.
- **MUST NOT:** Include `normalized`, `repair_operations`, `primitive_flags`, or mutated `tokens`.
- **MUST:** Envelope must be JSON‑serializable and deterministic.

---

## 3. Metadata and Provenance

### 3.1 Metadata

- **MUST:** IIInB may only write:
  ```python
  metadata["iiinb_status"] = "inspected"
  ```
- **MUST NOT:** Modify any other metadata fields.

### 3.2 Provenance

- **repair_proposals** and **anomaly_flags** must contain:
  - `rule_id`
  - `span` (token‑index pair `[i, j]`)
  - `replacement` (for proposals)
  - `target` (for anomalies)

- **MUST:** Spans must be deterministic and stable under replay.
- **MUST:** Provenance must be identical across Python and C++.

---

## 4. Allowed and Forbidden Behavior

### 4.1 Allowed

IIInB may:

- tokenize the original surface,
- detect structural anomalies,
- generate repair proposals,
- generate anomaly flags,
- preserve intake surface and tokens.

### 4.2 Forbidden

IIInB **MUST NOT**:

- apply repairs,
- mutate surface or tokens,
- normalize whitespace or punctuation,
- perform semantic inference,
- generate content,
- drop or reorder tokens,
- perform case normalization on output,
- produce committed normalized text.

---

## 5. Tokenization and Token Preservation

### 5.1 Token Source

- **MUST:** Tokens come from the **original intake surface**.
- **MUST NOT:** Tokenize the normalized or repaired surface (IIInB does not produce one).

### 5.2 Token Preservation

- **MUST:** `intake_tokens` must match the original surface split.
- **MUST NOT:** Drop, merge, or reorder tokens.
- **MUST:** Tokenization rules must match Python/C++ exactly.

---

## 6. Replay Determinism

IIInB participates in deterministic replay.

### 6.1 Deterministic Outputs

Given identical input, IIInB must produce:

- identical `repair_proposals`,
- identical `anomaly_flags`,
- identical `intake_surface`,
- identical `intake_tokens`,
- identical `iiinb_status`.

### 6.2 Forbidden Sources of Nondeterminism

- time,
- randomness,
- external services,
- global mutable state.

---

## 7. Progressive Lineup Compliance

### 7.1 Stable Rule Ordering

IIInB must execute rules in this exact order:

1. `tokenize_original_surface`
2. `detect_control_characters`
3. `detect_whitespace_anomalies`
4. `detect_repetition_anomalies`
5. `detect_punctuation_anomalies`
6. `detect_shorthand`
7. `detect_spelling`
8. `detect_unicode_noise`
9. `detect_case_normalization_trigger`

### 7.2 Statelessness

IIInB must be stateless across invocations.

---

## 8. Python Structural Program

### 8.1 High‑Level Interface

```python
def iiinb_inspect(intake: dict) -> dict:
    """
    intake = {
        "surface": str,
        "tokens": list[str]
    }

    Returns:
        {
            "iiinb_status": "inspected",
            "repair_proposals": [...],
            "anomaly_flags": [...],
            "intake_surface": str,
            "intake_tokens": list[str]
        }
    """
```

### 8.2 Required Internal Steps

1. **Tokenize original surface** → `intake_tokens`
2. **Detect anomalies** → `anomaly_flags`
3. **Generate repair proposals** → `repair_proposals`
4. **Set iiinb_status**
5. **Return TP envelope**

### 8.3 Wrapper Class

A wrapper class (as in `iiinb.py`) is allowed but must:

- return the canonical dict,
- preserve intake surface and tokens,
- expose no mutable state.

---

## 9. C++ Parity Requirements

Python and C++ implementations must produce identical:

- tokenization,
- repair proposals,
- anomaly flags,
- rule ordering,
- replay determinism.

---

## 10. Change‑Management Rules

Any change to IIInB must update:

- 20.101,
- 20.15,
- 20.105,
- iiinb.py,
- iiinb_rules.yaml,
- iiinb_rulechecker.py,
- iiinb_testbench.yaml,
- iiinb_testbench.py,
- progressive_lineup_testing.md,
- this structural program.

Unsynchronized changes are non‑compliant.

---

## 11. Input Playground Specification

`iiinb_input.yaml` is a developer playground for anomaly exploration.  
It is not a TP envelope and not a testbench.

---

## 12. Rule‑Family Toggle Specification

`iiinb_tests_to_run.yaml` defines rule‑family toggles for testbench mode.  
It allows selective activation of:

- spacing  
- punctuation  
- control_chars  
- normalization  
- deterministic  

---

## 13. Summary

IIInB is now:

- **proposal‑only**  
- **non‑mutating**  
- **pre‑semantic**  
- **token‑span indexed**  
- **deterministic**  
- **replay‑stable**  
- **Python/C++ aligned**

This document is the authoritative structural contract for IIInB in Python.

```

---
