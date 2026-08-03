# ⭐ **IIInB Structural Program (Python) — Version 3.2**  
### *Normative Structural Specification for the IIInB Primitive*  
### *Aligned with 20.101, 20.105, rule families, dictionary, rulechecker, and testbenches*

---

# **0. Purpose of This Document**

This file defines the **complete structural contract** for the Python implementation of the **IIInB primitive**.  
It synchronizes all authoritative sources:

- `20.101_iiinb_prim.md`  
- `20.15_ts_architecture_scaffold.md`  
- `20.105_tp_requirements.md`  
- `iiinb.py` (Python implementation)  
- `iiinb_rules.yaml` (rule definitions)  
- `iiinb_rulechecker.py` (rulechecker)  
- `iiinb_testbench.yaml` (expected outputs)  
- `iiinb_testbench.py` (testbench logic)  
- `progressive_lineup_testing.md`  
- dictionary rule sets (`iiinb_dct_rules/*.yaml`)  
- general‑mode validation logic  

Any change to IIInB behavior **must** be reflected here.

---

# **1. IIInB Primitive Identity**

IIInB is a:

- **proposal‑only**  
- **non‑mutating**  
- **pre‑semantic**  
- **bounded‑semantic**  
- **token‑span indexed**  
- **deterministic**  
- **replay‑stable**  
- **Python/C++ aligned**  

intake inspector.

It detects anomalies and proposes repairs **without applying them**.

---

# **2. Canonical TP Envelope (v3.2)**

IIInB must output the following envelope:

```python
{
    "iiinb_status": "inspected",
    "repair_proposals": list,     # deterministic, token-span indexed
    "anomaly_flags": list,        # deterministic, token-span indexed
    "intake_surface": str,        # original surface (unchanged)
    "intake_tokens": list[str],   # tokens from original surface (unchanged)
}
```

### **2.1 Required Constraints**

- All fields must be present.  
- No additional fields may be added.  
- All fields must be JSON‑serializable.  
- `intake_surface` must equal the original input.  
- `intake_tokens` must be derived from the original surface.  
- No normalization or mutation is allowed.

---

# **3. Metadata Rules**

IIInB may write **only**:

```python
metadata["iiinb_status"] = "inspected"
```

No other metadata fields may be modified.

---

# **4. Provenance Specification**

### **4.1 Repair Proposal Format**

```python
{
    "rule_id": str,
    "span": [i, j],
    "replacement": str
}
```

### **4.2 Anomaly Flag Format**

```python
{
    "rule_id": str,
    "span": [i, j],
    "type": str,
    "target": str,
    "location": int
}
```

### **4.3 Supported Anomaly Types (v3.2)**

- `illegal_character.control`  
- `illegal_character.forbidden`  
- `illegal_character.nonprintable`  
- `malformed_token`  
- `unicode_anomaly`  
- `punctuation_anomaly`  
- `repetition_pattern`  
- `no_entry`  

Spans must be deterministic and stable under replay.

---

# **5. Allowed vs Forbidden Behavior**

### **5.1 Allowed**

IIInB may:

- tokenize original surface  
- detect anomalies  
- generate repair proposals  
- preserve surface and tokens  
- detect dictionary absence  
- detect malformed tokens  
- detect unicode anomalies  
- detect repetition anomalies  
- detect punctuation anomalies  

### **5.2 Forbidden**

IIInB may **not**:

- apply repairs  
- mutate surface or tokens  
- normalize whitespace  
- normalize punctuation  
- normalize case  
- normalize unicode  
- collapse repetition  
- infer meaning  
- generate content  
- merge tokens  
- drop tokens  
- reorder tokens  
- perform semantic inference  
- produce committed normalized text  

---

# **6. Tokenization Rules**

### **6.1 Token Source**

Tokens come **only** from the original surface.

### **6.2 Token Preservation**

- No dropping  
- No merging  
- No reordering  
- No mutation  
- Python and C++ tokenization must match exactly  

---

# **7. Replay Determinism**

IIInB must produce identical outputs for identical inputs:

- anomaly flags  
- repair proposals  
- spans  
- ordering  
- intake surface  
- intake tokens  
- iiinb_status  

No randomness or external state is allowed.

---

# **8. Rule Ordering (Canonical v3.2)**

Rules must execute in this exact order:

1. `tokenize_original_surface`  
2. `detect_illegal_character_control`  
3. `detect_illegal_character_forbidden`  
4. `detect_illegal_character_nonprintable`  
5. `detect_whitespace_anomalies`  
6. `detect_repetition_anomalies`  
7. `detect_punctuation_anomalies`  
8. `detect_unicode_anomaly`  
9. `detect_malformed_token`  
10. `detect_no_entry`  
11. `detect_shorthand`  
12. `detect_spelling_transpose`  
13. `detect_spelling_missing`  
14. `detect_spelling_extra`  
15. `detect_case_normalization_trigger`  
16. `detect_structural_clean`  
17. `detect_long_input_guardrail`  

This ordering is **mandatory**.

---

# **9. Repair Proposal Taxonomy (v3.2)**

IIInB may propose:

- `whitespace.normalize`  
- `repetition.collapse`  
- `punctuation.clean`  
- `unicode.normalize`  
- `structural.clean`  
- `shorthand.expand`  
- `spelling.transpose`  
- `spelling.missing`  
- `spelling.extra`  
- `case.normalize`  

Repairs are **never applied**.

---

# **10. Rulechecker Alignment (General Mode)**

The rulechecker validates **only**:

- `illegal_character.control`  
- `illegal_character.forbidden`  
- `illegal_character.nonprintable`

General mode must compare:

```
primitive illegal-character anomalies
vs
rulechecker illegal-character anomalies
```

General mode PASS = alignment  
General mode FAIL = mismatch  

All other anomalies are ignored in general mode.

---

# **11. Testbench Mode (Regression Mode)**

Testbench mode validates:

- full anomaly taxonomy  
- full repair taxonomy  
- full spans  
- full tokenization  
- full surface preservation  
- full rule ordering  
- full dictionary behavior  
- full replay determinism  

Testbench mode is **authoritative**.

You currently pass:

- **10/10** testbench cases  
- **26/26** general mode cases  

---

# **12. Dictionary Rules**

Dictionary absence must produce:

```
anomaly_flag: no_entry
```

Dictionary rule sets must be:

- deterministic  
- replay-stable  
- synchronized with rule families  
- synchronized with testbench expectations  

---

# **13. Change‑Management Requirements**

Any change to:

- IIInB behavior  
- rule ordering  
- anomaly taxonomy  
- repair taxonomy  
- dictionary behavior  
- rulechecker behavior  
- testbench expectations  
- TP envelope shape  

must update:

- this structural program  
- iiinb.py  
- iiinb_rules.yaml  
- iiinb_rulechecker.py  
- iiinb_testbench.yaml  
- iiinb_testbench.py  
- progressive_lineup_testing.md  
- 20.101 / 20.105 / 20.15  

Unsynchronized changes are non‑compliant.

---

# **14. Developer Playground**

`iiinb_input.yaml` is:

- non-authoritative  
- non-TP  
- non-spec  
- used only for general mode exploration  

General mode must not enforce full testbench expectations.

---

# **15. Summary**

IIInB v3.2 is:

- deterministic  
- replay-stable  
- proposal-only  
- non-mutating  
- pre-semantic  
- bounded-semantic  
- token-span indexed  
- Python/C++ aligned  
- validated by testbench mode  
- aligned with rulechecker in general mode  

This document is the **canonical structural contract** for IIInB.

---
