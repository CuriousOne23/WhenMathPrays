# ⭐ **`cex_py_struc_pgm.md` — One‑Stop CEx Programming Reference (Version 3.0)**  
### *Python & C++ Implementation Blueprint for the Context Extractor Primitive (CEx)*  
### *Aligned with 20.107 Version 3.0, IE v3.3, CIL v3.2, TP Metadata v0.8*

This document is the **canonical programming blueprint** for implementing the **CEx primitive** in Python or C++.  
It synchronizes the following authoritative sources:

- `cex.py` (implementation)  
- `cex_testbench.yaml` (strict expected‑output testbench)  
- `cex_input.yaml` (general rule‑driven testbench)  
- `cex_rules.yaml` + `cex_rulechecker.py` (rule validation)  
- `run.py` (pipeline runner)  
- `20.107_cex_extract.md` (formal primitive specification)  
- `progressive_lineup_testing.md` (pipeline testing framework)

Everything required to implement CEx’s deterministic identity selection, bounded semantic extraction, context normalization, provenance, audit behavior, and replay constraints is here.

---

# **1. CEx’s Role in the Pipeline**

CEx is the **Context Extractor**, the first semantic‑adjacent primitive in Path‑A that consumes:

- **IE output** (committed intake substrate)  
- **CIL output** (identity, stability, clarifying metadata, next‑turn context)

CEx produces:

- **CE.context_fields**  
- **CE.metadata.context_provenance**  
- **CE.metadata.extraction_audit**

CEx is:

- deterministic  
- bounded‑semantic  
- rule‑driven  
- replay‑stable  
- non‑inferential  
- identity‑aware  
- metadata‑bounded  
- provenance‑complete

CEx ensures downstream primitives (CE → ISc → TPU → IdOB → RB → OuBA → SSRGn) receive **clean, normalized, identity‑aligned, replay‑equivalent context**.

---

# **2. Public API (Python & C++)**

The testbench invokes CEx exactly like this:

```python
cex = CEx(ie_output, cil_output)
cex.extract()
```

CEx must expose:

### Required fields

- `ce.context_fields`  
- `ce.metadata.context_provenance`  
- `ce.metadata.extraction_audit`  
- `ce.metadata.continuity_status`  
- `version_tag`

### Required method

```python
def extract(self):
    # populate CE deterministically
```

### Required behavior

CEx:

- consumes IE tokens, flags, structure, metadata  
- consumes CIL identity selection, clarifying metadata, stability, next_context  
- selects identity layer deterministically  
- applies fallback rules  
- detects new conversation  
- extracts bounded semantic context fields  
- writes CE into TP.metadata.context_metadata  
- records provenance  
- records extraction audit  
- guarantees deterministic replay  
- respects TP metadata boundaries  
- respects progressive lineup testing rules

CEx does **not**:

- infer meaning  
- perform semantic repair  
- modify identity layers  
- modify clarifying metadata  
- modify routing metadata  
- modify structural metadata  
- modify freeze metadata  
- modify TP.semantic or TP.process  
- use embeddings or probabilistic reasoning

---

# **3. Intake Model**

CEx receives **two inputs**:

### **3.1 IE Input (Committed Intake Substrate)**

```python
ie_output.intake.ie_tokens
ie_output.intake.token_flags
ie_output.intake.normalized_text
ie_output.structure.tags
ie_output.structure.spans
ie_output.structure.markup
ie_output.metadata.repair_annotations
ie_output.metadata.replay
ie_output.error
```

IE provides:

- committed tokens  
- bounded semantic classification  
- structural geometry  
- repair provenance  
- anomaly provenance  
- replay metadata

### **3.2 CIL Input (Identity + Clarifying + Stability + Next‑Context)**

```python
cil_output.identity_selection_block
cil_output.clarifying_fields
cil_output.stability
cil_output.certainty
cil_output.ambiguity
cil_output.collapse_risk
cil_output.next_context
cil_output.structural_hints
```

CIL provides:

- identity selection  
- clarifying metadata  
- stability signals  
- continuity signals  
- next‑turn context  
- structural hints

CEx must:

- consume IE + CIL deterministically  
- apply identity selection rules  
- apply fallback rules  
- detect new conversation  
- extract bounded semantic context  
- write CE into TP.metadata.context_metadata  
- record provenance  
- record audit entries  
- preserve replay determinism

---

# **4. Deterministic Rule Ordering**  
### (Enforced by `cex_testbench.yaml` and `cex_rules.yaml`)

CEx must apply its operations in **exactly this order**:

1. Receive IE + CIL  
2. Validate IE substrate  
3. Validate CIL substrate  
4. Select identity layer  
5. Apply fallback rules  
6. Detect new conversation  
7. Extract bounded semantic context fields  
8. Normalize context fields deterministically  
9. Build CE.context_fields  
10. Build CE.metadata.context_provenance  
11. Build CE.metadata.extraction_audit  
12. Validate CE schema  
13. Emit deterministic CE envelope

This ordering is required for deterministic replay.

---

# **5. Identity Selection (Updated for v3.0)**

CEx must:

- read `CIL.identity_selection_block`  
- apply continuity rules using `TP.process.identity_layer_prev`  
- use recency, frequency, density  
- use certainty and ambiguity  
- use collapse_risk  
- apply deterministic fallback  
- detect new conversation  
- mark continuity status

### Identity selection outputs:

```python
ce.metadata.continuity_status = "normal" | "fallback" | "undetermined" | "new_conversation"
```

Identity selection is **bounded‑semantic**, not inferential.

---

# **6. Clarifying Metadata Extraction**

CEx must:

- extract clarifying fields  
- preserve hierarchical topology  
- enforce bounded limits  
- record drops/truncations  
- treat clarifying metadata as read‑only  
- preserve continuity across turns  
- include clarifying metadata even in fallback cases

Clarifying metadata is consumed from CIL and written into CE.context_fields.

---

# **7. Next‑Turn Context Extraction**

CEx must:

- read next‑turn context exclusively from CIL.next_context  
- treat next‑turn context as read‑only  
- include next‑turn context fields in CE  
- preserve continuity  
- avoid semantic inference  
- avoid deriving next‑turn context from clarifying metadata  
- record drops/truncations

Next‑turn context fields include:

- topic  
- stance  
- intent  
- register  
- politeness  
- epistemic_shading  
- continuity  
- direction  
- coherence  
- shift_required  
- importance

---

# **8. Bounded Semantic Domain (CEx Edition)**

CEx is a bounded‑semantic primitive.  
Its semantic domain is strictly local, deterministic, rule‑driven, and replay‑stable.

### Allowed operations:

- identity selection  
- fallback selection  
- new‑conversation detection  
- context extraction  
- context normalization  
- clarifying metadata extraction  
- next‑turn context reflection  
- provenance writing  
- audit writing

### Prohibited operations:

- meaning inference  
- semantic repair  
- identity modification  
- clarifying modification  
- routing modification  
- structural modification  
- freeze modification  
- probabilistic reasoning  
- embeddings  
- global semantics  
- cross‑sentence semantics

---

# **9. CE Structural Schema**

CEx produces:

```
CE {
    context_fields: {
        topic: string,
        stance: string,
        intent: string,
        register: string,
        politeness: string,
        tone: string,
        epistemic_shading: string,
        continuity: string,
        direction: string,
        coherence: string,
        shift_required: bool,
        importance: int,
        clarifying_fields: [...],
        identity_layer_id: int
    },
    metadata: {
        context_provenance: [...],
        extraction_audit: [...],
        continuity_status: string
    },
    version_tag: string
}
```

CE is written into:

```
TP.metadata.context_metadata
```

---

# **10. Provenance Construction**

CEx must:

- record origin = "CEx"  
- record last_update = "CEx"  
- append commit lineage  
- preserve upstream provenance  
- treat all non‑context provenance as read‑only  
- guarantee deterministic replay provenance

---

# **11. Extraction Audit**

CEx must record:

- drops  
- truncations  
- topology compressions  
- fallback selections  
- new‑conversation detection  
- missing fields  
- malformed fields  
- normalization adjustments

Audit entries must be deterministic.

---

# **12. Implementation Skeleton (Python)**

```python
class CEx:
    def __init__(self, ie_output, cil_output):
        self.ie = ie_output
        self.cil = cil_output
        self.ce = {}
        self.metadata = {}
        self.audit = []

    def extract(self):
        # 1. Validate IE + CIL
        validate_ie(self.ie)
        validate_cil(self.cil)

        # 2. Identity selection
        identity = select_identity(self.cil, self.ie)
        continuity_status = determine_continuity(identity, self.cil)

        # 3. Fallback + new conversation
        identity = apply_fallback(identity, self.cil)
        identity = detect_new_conversation(identity, self.ie, self.cil)

        # 4. Extract context fields
        context = extract_context_fields(self.ie, self.cil, identity)

        # 5. Normalize context
        context = normalize_context(context)

        # 6. Build CE
        self.ce["context_fields"] = context

        # 7. Provenance
        self.metadata["context_provenance"] = build_provenance(context)

        # 8. Audit
        self.metadata["extraction_audit"] = self.audit
        self.metadata["continuity_status"] = continuity_status

        # 9. Version tag
        self.ce["version_tag"] = "cex_v3.0"

        return self
```

---

# **13. Implementation Skeleton (C++)**

Equivalent structure:

- `class CEx`  
- constructor receives IE + CIL  
- `extract()` populates CE deterministically  
- identity selection + fallback + new conversation  
- context extraction  
- provenance  
- audit  
- version tag

---

# **14. Change Management**

When CEx evolves:

- update rule ordering  
- update testbench expectations  
- update this document  
- update `20.107_cex_extract.md`  
- update `cex_rules.yaml`  
- update `cex_testbench.yaml`  
- update `cex_input.yaml`  
- ensure replay metadata remains stable  
- ensure provenance remains deterministic  
- ensure bounded semantics remain intact

This document is the **authoritative programming reference** for CEx v3.0.

---

# **15. Reference Documents (Canonical CEx Synchronization Set)**

1. **cex_py_struc_pgm.md** — programming blueprint  
2. **20.107_cex_extract.md** — conceptual spec  
3. **cex_testbench.yaml** — strict expected‑output testbench  
4. **cex_input.yaml** — general rule‑driven testbench  
5. **cex_rules.yaml** — rule definitions  
6. **cex_rulechecker.py** — rule execution  
7. **cex.py** — implementation logic  
8. **run.py** — pipeline runner  
9. **progressive_lineup_testing.md** — pipeline testing framework  

These documents define the **complete CEx universe**.

---

# **End of Document — cex_py_struc_pgm.md (Version 3.0)**

---
