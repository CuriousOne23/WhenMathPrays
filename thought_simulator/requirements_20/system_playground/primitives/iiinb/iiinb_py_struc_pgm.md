# ⭐ **`iiinb_py_struc_pgm.md` — Python Structural Program (Version 3.2)**  
### *Proposal‑Only, Non‑Mutating, Bounded‑Semantic Intake Inspector*  
### *Aligned with 20.101 Version 3.2 (Model‑A, IIInB v3.2)*

This document is the **normative structural specification** for the Python implementation of the **IIInB** primitive.  
It synchronizes the following authoritative sources:

- `20.101_iiinb_prim.md` (corrected)  
- `20.15_ts_architecture_scaffold.md`  
- `20.105_tp_requirements.md`  
- `20.105.010_tp_meta_fields.md`  
- `20.105.020_tp_meta_provenance.md`  
- `system_playground/primitives/iiinb/iiinb.py`  
- `iiinb_testbench.yaml`  
- `iiinb_testbench.py`  
- `progressive_lineup_testing.md`  
- `iiinb_dct_rules/*.yaml`  
- `iiinb_rulechecker.py`

Any change to IIInB behavior, TP envelope shape, rule ordering, anomaly taxonomy, or replay determinism **must** be reflected here.

---

# **1. Canonical Synchronization Set**

IIInB’s conceptual, structural, and mechanical behavior is defined by:

- conceptual primitive spec (`20.101_iiinb_prim.md`)  
- architecture scaffold (`20.15_ts_architecture_scaffold.md`)  
- TP envelope requirements (`20.105_tp_requirements.md`)  
- Python implementation (`iiinb.py`)  
- structural program (this file)  
- testbenches (`iiinb_testbench.yaml`, `iiinb_testbench.py`)  
- progressive lineup testing  
- dictionary rule sets  
- rulechecker  

All changes to IIInB must be synchronized across this set.

---

# **2. TP Envelope (Proposal‑Only, Non‑Mutating)**

IIInB is a **pre‑semantic**, **non‑mutating**, **proposal‑only** primitive.  
It produces a deterministic TP envelope with:

- **no normalization**  
- **no repair application**  
- **no surface mutation**  
- **no token mutation**  
- **no composite merges**  
- **no semantic inference**

### **2.1 Canonical TP Envelope Schema (Updated for v3.2)**

IIInB outputs:

```python
{
    "iiinb_status": "inspected",
    "repair_proposals": list,     # deterministic, token-span indexed
    "anomaly_flags": list,        # deterministic, token-span indexed
    "intake_surface": str,        # original surface (unchanged)
    "intake_tokens": list[str],   # tokens from original surface (unchanged)
}
```

### **2.2 Normative Constraints**

- All fields must be present.  
- Field names and types must match exactly.  
- No additional top‑level fields may be added.  
- Envelope must be JSON‑serializable and deterministic.  
- No normalization, no committed text, no mutated tokens.

---

# **3. Metadata and Provenance**

### **3.1 Metadata**

IIInB writes only:

```python
metadata["iiinb_status"] = "inspected"
```

No other metadata fields may be modified.

### **3.2 Provenance (Updated for v3.2)**

Each **repair_proposal** includes:

```python
{
    "rule_id": str,
    "span": [i, j],
    "replacement": str
}
```

Each **anomaly_flag** includes:

```python
{
    "rule_id": str,
    "span": [i, j],
    "type": str,        # anomaly type
    "target": str,      # offending token or character
    "location": int     # token index or char index
}
```

Supported anomaly types (updated):

- `illegal_character.*`  
- `malformed_token`  
- `unicode_anomaly`  
- `punctuation_anomaly`  
- `repetition_pattern`  
- `no_entry`  

Spans must be deterministic and stable under replay.

Python and C++ provenance must match exactly.

---

# **4. Allowed and Forbidden Behavior**

### **4.1 Allowed**

IIInB may:

- tokenize original surface  
- detect local semantic anomalies  
- detect dictionary‑absence (`no_entry`)  
- detect malformed tokens  
- detect repetition anomalies  
- detect punctuation anomalies  
- detect unicode anomalies  
- generate deterministic repair proposals  
- preserve intake surface and tokens  

### **4.2 Forbidden**

IIInB may not:

- apply repairs  
- mutate surface or tokens  
- normalize whitespace, punctuation, casing, unicode, or repetition  
- perform composite merges  
- infer meaning  
- generate content  
- drop or reorder tokens  
- perform case normalization  
- produce committed normalized text  

---

# **5. Tokenization and Token Preservation**

### **5.1 Token Source**

Tokens come **only** from the original intake surface.

IIInB does not tokenize repaired or normalized text.

### **5.2 Token Preservation**

- `intake_tokens` must match the original surface split.  
- No dropping, merging, or reordering.  
- Tokenization rules must match Python/C++ exactly.

---

# **6. Replay Determinism**

IIInB participates in deterministic replay.

### **6.1 Deterministic Outputs**

Given identical input, IIInB produces identical:

- repair_proposals  
- anomaly_flags  
- intake_surface  
- intake_tokens  
- iiinb_status  

### **6.2 Forbidden Nondeterminism**

No:

- time  
- randomness  
- external services  
- global mutable state  

---

# **7. Progressive Lineup Compliance (Updated for v3.2)**

### **7.1 Stable Rule Ordering**

IIInB executes rules in this exact order:

1. `tokenize_original_surface`  
2. `detect_control_characters`  
3. `detect_whitespace_anomalies`  
4. `detect_repetition_anomalies`  
5. `detect_punctuation_anomalies`  
6. `detect_unicode_anomalies`  
7. `detect_illegal_characters`  
8. `detect_malformed_tokens`  
9. `detect_no_entry`  
10. `detect_shorthand`  
11. `detect_spelling`  
12. `detect_case_normalization_trigger`  

### **7.2 Statelessness**

IIInB is stateless across invocations.

---

# **8. Python Structural Program (Updated for v3.2)**

### **8.1 High‑Level Interface**

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

### **8.2 Required Internal Steps (Updated)**

1. tokenize original surface  
2. detect anomalies (all types)  
3. generate deterministic repair proposals  
4. set iiinb_status  
5. return TP envelope  

### **8.3 Wrapper Class**

A wrapper class (as in `iiinb.py`) is allowed but must:

- return canonical dict  
- preserve intake surface and tokens  
- expose no mutable state  

---

# **9. C++ Parity Requirements**

Python and C++ implementations must produce identical:

- tokenization  
- anomaly detection  
- repair proposals  
- rule ordering  
- replay determinism  

---

# **10. Change‑Management Rules**

Any change to IIInB must update:

- 20.101  
- 20.15  
- 20.105  
- iiinb.py  
- iiinb_rules.yaml  
- iiinb_rulechecker.py  
- iiinb_testbench.yaml  
- iiinb_testbench.py  
- progressive_lineup_testing.md  
- this structural program  

Unsynchronized changes are non‑compliant.

---

# **11. Input Playground Specification**

`iiinb_input.yaml` is a developer playground for anomaly exploration.  
It is not a TP envelope and not a testbench.

---

# **12. Rule‑Family Toggle Specification**

`iiinb_tests_to_run.yaml` defines rule‑family toggles for testbench mode:

- spacing  
- punctuation  
- control_chars  
- normalization  
- deterministic  

---

# **13. Summary**

IIInB is:

- proposal‑only  
- non‑mutating  
- pre‑semantic  
- bounded‑semantic  
- token‑span indexed  
- deterministic  
- replay‑stable  
- Python/C++ aligned  
- updated for IIInB v3.2 anomaly taxonomy  

This document is the authoritative structural contract for IIInB in Python.

---
