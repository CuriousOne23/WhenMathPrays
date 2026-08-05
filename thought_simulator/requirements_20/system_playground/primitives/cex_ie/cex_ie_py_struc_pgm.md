# ⭐ **`cex_ie_py_struc_pgm.md` — One‑Stop CEx‑IE Programming Reference (Version 1.0)**  
### *Python & C++ Implementation Blueprint for the CEx‑IE Primitive*  
### *Aligned with 20.107.010 (TP‑Aligned, Version 1.0)*  
### *Synchronized with testbench, rulechecker, and progressive lineup testing*

This document is the **canonical programming blueprint** for implementing the **CEx‑IE primitive** in Python or C++.  
It synchronizes the following authoritative sources:

- `cex_ie.py` (implementation)  
- `cex_ie_testbench.yaml` (deterministic testbench)  
- `cex_ie_input.yaml` (general‑mode stimulus)  
- `cex_ie_rules.yaml` (rule definitions)  
- `cex_ie_rulechecker.py` (rulechecker logic)  
- `20.107.010_cex-ie_primitive.md` (formal primitive specification)  
- `progressive_lineup_testing.md` (testing framework)  
- `cex_ie_cue_dictionary.yaml` (cue dictionary)

Everything required to implement CEx‑IE’s structural cue detection, bounded‑semantic hint derivation, deterministic envelope construction, and replay‑safe behavior is here.

---

# **1. CEx‑IE’s Role in the Pipeline**

CEx‑IE is the **first internal module** of the CEx primitive.  
It receives IE’s committed intake substrate and produces a **compact structural envelope** for CEx‑CCR.

CEx‑IE consumes:

- `TP.intake.ie_tokens`  
- `TP.intake.token_flags`  
- `TP.intake.normalized_text`  
- `TP.structure.tags`  
- `TP.structure.spans`  
- `TP.structure.markup`  
- `TP.metadata.repair_annotations`

CEx‑IE emits:

- deterministic copies of IE tokens, flags, normalized text  
- structural cue‑phrases  
- structural hint fields  
- a complete `TP.cex.ie` envelope

CEx‑IE is:

- deterministic  
- rule‑driven  
- bounded‑semantic  
- replay‑safe  
- dictionary‑driven  
- non‑inferential  
- strictly structural  

CEx‑IE does **not**:

- perform conversation selection (CEx‑CCR)  
- perform packaging (CEx‑Pck)  
- use embeddings or global semantics  
- access downstream primitives  

---

# **2. Public API (Python & C++)**

The testbench invokes CEx‑IE exactly like this:

```python
cex_ie = CExIE(tp_input)
cex_ie.inspect()
```

CEx‑IE must expose:

### Required fields (`TP.cex.ie`)

- `tokens`  
- `token_flags`  
- `normalized_text`  
- `structural_phrases`  
- `topic_hint`  
- `intent_hint`  
- `continuity_hint`  
- `reference_hint`  
- `register_hint`  
- `politeness_hint`  
- `direction_hint`  
- `coherence_hint`  
- `importance_hint`

### Required method

```python
def inspect(self):
    # populate TP.cex.ie deterministically
```

### Required behavior

CEx‑IE:

- copies IE tokens, flags, normalized text  
- detects cue‑phrases using deterministic rules  
- derives structural hints using bounded semantics  
- emits complete envelope even when hints are `none`  
- uses only IE‑emitted fields  
- loads cue dictionary deterministically  
- produces replay‑stable output  

CEx‑IE does **not**:

- infer meaning  
- use embeddings  
- use global context  
- modify IE fields  
- modify TP.structure or TP.metadata  

---

# **3. Intake Model**

CEx‑IE receives IE output:

```python
tokens        = TP.intake.ie_tokens
token_flags   = TP.intake.token_flags
normalized    = TP.intake.normalized_text
tags          = TP.structure.tags
spans         = TP.structure.spans
markup        = TP.structure.markup
repairs       = TP.metadata.repair_annotations
```

CEx‑IE must:

- copy tokens, flags, normalized text exactly  
- detect structural cue‑phrases using dictionary  
- derive hint fields using bounded‑semantic rules  
- construct `TP.cex.ie` deterministically  
- emit all hint fields even when `none`  

CEx‑IE must not:

- modify IE fields  
- reinterpret repairs  
- drop tokens  
- reorder tokens  
- use semantic inference  

---

# **4. Deterministic Rule Ordering**  
### (Enforced by `cex_ie_testbench.yaml`)

CEx‑IE must apply its operations in **exactly this order**:

1. Receive IE tokens, flags, normalized text  
2. Load cue dictionary  
3. Detect cue‑phrases using deterministic token windows (≤5)  
4. Encode `structural_phrases`  
5. Derive hint fields using bounded‑semantic rules  
6. Construct `TP.cex.ie` envelope  
7. Validate envelope shape  
8. Emit deterministic output  

This ordering is required for deterministic replay and Python/C++ parity.

---

# **5. Cue Detection**

CEx‑IE uses `cex_ie_cue_dictionary.yaml` to detect:

- continuity cues  
- reference‑back cues  
- intent cues  
- topic cues  
- direction cues  
- politeness cues  
- register cues  
- importance cues  

Cue detection rules:

- match tokens in windows ≤5  
- case‑insensitive  
- whitespace‑normalized  
- punctuation‑insensitive  
- deterministic ordering  
- dictionary‑driven only  

CEx‑IE must not:

- infer meaning  
- guess cues  
- use embeddings  
- use semantic similarity  

---

# **6. Structural Hint Derivation**

CEx‑IE derives:

### Topic Hint  
`greeting | assistance | system | misc | noise | other`

### Intent Hint  
`inform | request | begin | none`

### Continuity Hint  
`continue | reset | shift | unknown`

### Reference Hint  
`none | previous | specific_previous | ambiguous_previous`

### Register Hint  
`casual | formal | informal | none`

### Politeness Hint  
`high | normal | none`

### Direction Hint  
`forward | backward | none`

### Coherence Hint  
`stable | unstable | none`

### Importance Hint  
`low | medium | high`

Rules:

- deterministic  
- bounded‑semantic  
- dictionary‑driven  
- no global semantics  
- no embeddings  

---

# **7. Bounded Semantic Domain**

CEx‑IE is a **bounded‑semantic primitive**, meaning:

- operates only on local token windows (≤5)  
- uses only IE‑emitted fields  
- does not infer meaning  
- does not use embeddings  
- does not use global context  
- is deterministic and replay‑stable  

Allowed operations:

- cue detection  
- structural phrase encoding  
- hint derivation  
- envelope construction  

Prohibited operations:

- semantic inference  
- meaning interpretation  
- conversation selection  
- lineage alignment  
- fallback logic  

---

# **8. Structural Schema**

CEx‑IE produces:

```
TP.cex.ie {
    tokens: [string],
    token_flags: [TokenFlag],
    normalized_text: string,
    structural_phrases: [CExStructuralPhrase],
    topic_hint: CExTopicHint,
    intent_hint: CExIntentHint,
    continuity_hint: CExContinuityHint,
    reference_hint: CExReferenceHint,
    register_hint: CExRegisterHint,
    politeness_hint: CExPolitenessHint,
    direction_hint: CExDirectionHint,
    coherence_hint: CExCoherenceHint,
    importance_hint: CExImportanceHint
}
```

All fields must be present, even when `none`.

---

# **9. Replay Metadata**

CEx‑IE must be:

- deterministic  
- replay‑stable  
- dictionary‑stable  
- rule‑stable  

Given identical IE input, CEx‑IE must produce identical output.

---

# **10. Forbidden Behavior**

CEx‑IE must not:

- modify IE fields  
- modify TP.structure  
- modify TP.metadata  
- infer meaning  
- use embeddings  
- use global semantics  
- drop tokens  
- reorder tokens  
- perform conversation selection  

---

# **11. Implementation Skeleton (Python)**

```python
class CExIE:
    def __init__(self, tp):
        self.tp = tp
        self.output = {"cex": {"ie": {}}}

    def inspect(self):
        # 1. Receive IE fields
        tokens      = self.tp["intake"]["ie_tokens"]
        token_flags = self.tp["intake"]["token_flags"]
        normalized  = self.tp["intake"]["normalized_text"]
        tags        = self.tp["structure"]["tags"]
        spans       = self.tp["structure"]["spans"]
        markup      = self.tp["structure"]["markup"]
        repairs     = self.tp["metadata"]["repair_annotations"]

        # 2. Load cue dictionary
        cue_dict = load_cex_ie_cue_dictionary()

        # 3. Detect structural cue-phrases
        structural_phrases = detect_cues(tokens, normalized, cue_dict)

        # 4. Derive hint fields
        hints = derive_hints(tokens, token_flags, normalized,
                             structural_phrases, tags, spans, markup)

        # 5. Construct TP.cex.ie envelope
        self.output["cex"]["ie"] = {
            "tokens": tokens,
            "token_flags": token_flags,
            "normalized_text": normalized,
            "structural_phrases": structural_phrases,
            **hints
        }

        # 6. Validate envelope
        validate_cex_ie(self.output["cex"]["ie"])

        return self.output
```

---

# **12. Implementation Skeleton (C++)**

Equivalent structure:

- `class CExIE`  
- constructor receives TP  
- `inspect()` populates `TP.cex.ie`  
- deterministic cue detection  
- deterministic hint derivation  
- deterministic envelope construction  

---

# **13. Change Management**

When CEx‑IE evolves:

- update cue dictionary  
- update rule ordering  
- update testbench  
- update rulechecker  
- update this document  
- ensure replay determinism  
- ensure Python/C++ parity  

This document is the **authoritative programming reference** for CEx‑IE v1.0.

---

# **14. Reference Documents**

1. **cex_ie_py_struc_pgm.md** — programming blueprint  
2. **20.107.010_cex-ie_primitive.md** — formal primitive spec  
3. **cex_ie_cue_dictionary.yaml** — cue dictionary  
4. **cex_ie_testbench.yaml** — deterministic testbench  
5. **cex_ie_input.yaml** — general‑mode stimulus  
6. **cex_ie_rules.yaml** — rule definitions  
7. **cex_ie_rulechecker.py** — rulechecker logic  
8. **cex_ie.py** — implementation  
9. **progressive_lineup_testing.md** — testing framework  

---
