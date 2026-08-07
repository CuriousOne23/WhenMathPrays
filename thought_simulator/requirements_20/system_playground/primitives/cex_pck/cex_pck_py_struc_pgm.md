# ⭐ **`cex_pck_py_struc_pgm.md` (Version 2.0)**  
### *Python & C++ Implementation Blueprint for the CEx‑Pck Primitive*  
### *Aligned with 20.107.030, 20.105, 20.15, and CCR‑Integrated TP Metadata*  

---

# **1. CEx‑Pck’s Role in the Pipeline**

CEx‑Pck is the **third internal module** of the CEx primitive, following:

1. **CEx‑IE** — structured intake hints  
2. **CEx‑CCR** — conversation alignment + decision  

CEx‑Pck is responsible for:

- packaging the **current‑turn context shell** for CE  
- projecting CCR output and semantic‑importance into TP metadata  
- preparing **continuity, MSL, and residue metadata** for downstream primitives  
- exposing CCR decisions and CIL selection in a deterministic, replay‑safe way  

CEx‑Pck consumes:

- `TP.cex.ie` (IE structural hints)  
- `TP.cex.ccr` (CCR alignment + scores + decision + selected_conversation)  
- `TP.semantic.importance` (bounded semantic residues)  
- `TP.metadata.next_context` (MCB.next_context from prior turn, if present)  

CEx‑Pck produces:

- a **context shell** for CE (context envelope + MSL tokens)  
- CCR‑aligned metadata fields for COB, CIL, CST  
- semantic‑residue alignment metadata  
- CIL substrate selection metadata  

CEx‑Pck is:

- deterministic  
- rule‑driven  
- bounded‑semantic  
- replay‑safe  
- TP‑aligned  
- CCR‑aware  

CEx‑Pck does **not**:

- perform semantic interpretation  
- modify CCR output  
- modify semantic‑importance residues  
- modify CIL substrate content  
- perform lineage updates (COB/CIL/CST responsibility)  

---

# **2. Public API (Python & C++)**

```python
cex_pck = CExPck(tp_input)
cex_pck.inspect()
```

### Required TP fields (post‑CEx‑Pck)

CEx‑Pck SHALL populate or update the following TP envelopes/metadata:

- `context` envelope:
  - `topic`
  - `stance`
  - `intent`
  - `register`
  - `politeness`
  - `tone`
  - `continuity`
  - `direction`
  - `coherence`
  - `importance`
  - `clarifying_fields[]`
- `TP.metadata.context_metadata`:
  - `context.relevance_flags`
  - `context.copy_forward_flags`
  - `context.reset_flags`
  - `context.context_fields`
  - `context.context_provenance`
- `TP.metadata.msl_metadata`:
  - `msl.qualifiers`
  - `msl.clarifications`
  - `msl.stance`
  - `msl.shading`
  - `msl.intent`
  - `msl.direction`
  - `msl.coherence`
  - `msl.subculture`
- `TP.metadata.cil_metadata`:
  - `selected_conversation`
  - `cil_reference`
  - `cil.projection_provenance`
- `TP.metadata.semantic_residue_metadata`:
  - `semantic_residue.entities[]`
  - `semantic_residue.facts[]`
  - `semantic_residue.alignment_scores`
  - `semantic_residue.provenance`

CEx‑Pck SHALL **not** modify:

- `TP.cex.ccr.*`  
- `TP.semantic.importance.*`  

### Required method

```python
def inspect(self):
    # read IE + CCR + importance + next_context
    # construct context shell + metadata deterministically
```

---

# **3. Intake Model (Four Inputs)**

CEx‑Pck receives **four** bounded inputs from TP.

CEx‑Pck SHALL read the **static 10‑conversation CIL substrate** from:

```
thought_simulator/requirements_20/system_playground/testbenches/path_a/semantic/cil_input.yaml
```

This file contains the canonical lineage substrate used by both **CEx‑CCR** and **CEx‑Pck**.  
CEx‑Pck does **not** consume the full CIL substrate directly; instead, it uses:

- `selected_conversation` (from CEx‑CCR)  
- `cil_reference` (from CEx‑CCR)  
- `semantic_residue` for the selected conversation  
- `next_context` for the selected conversation  

All other CIL fields (identity_lineage, clarifying_lineage, context_lineage, continuity_lineage, topology, metrics) are consumed by **CEx‑CCR**, **COB**, **CIL**, and **CST**, but **not** by CEx‑Pck.

CEx‑Pck SHALL treat `cil_input.yaml` as a **read‑only static substrate** and SHALL NOT modify its contents.

---

## **3.1 CEx‑IE envelope (`TP.cex.ie`)**

CEx‑Pck reads the same structural hints used by CCR:

```python
topic_hint
intent_hint
continuity_hint
reference_hint
register_hint
politeness_hint
direction_hint
coherence_hint
importance_hint
structural_phrases
```

CEx‑Pck uses these hints to:

- derive **topic**, **intent**, **continuity**, **direction**, **coherence**, **importance**  
- seed MSL tokens (qualifiers, clarifications, stance, shading, etc.)  

These hints are **bounded structural categories** and SHALL NOT be modified.

---

## **3.2 CCR output envelope (`TP.cex.ccr`)**

CEx‑Pck reads:

```python
alignment.identity
alignment.clarifying
alignment.context
alignment.continuity
alignment.reference
alignment.semantic_residue

scores.ambiguity
scores.collapse
scores.drift
scores.stability

decision
selected_conversation
provenance
```

CEx‑Pck uses CCR output to:

- set **context.relevance_flags** and **reset/copy‑forward flags**  
- populate **CIL metadata** (`selected_conversation`, `cil_reference`)  
- populate **semantic_residue.alignment_scores**  
- expose CCR decisions to COB, CIL, CST via metadata  

CEx‑Pck SHALL NOT:

- change any CCR alignment values  
- change any CCR scores  
- change `decision` or `selected_conversation`  

---

## **3.3 Path‑A importance envelope (`TP.semantic.importance`)**

CEx‑Pck reads:

```python
TP.semantic.importance.entities[]: { value, role, score, provenance }
TP.semantic.importance.facts[]:    { value, role, score, provenance }
```

CEx‑Pck uses importance residues to:

- seed **semantic_residue.entities/facts** metadata  
- strengthen continuity and relevance flags  
- assist COB/CIL/CST in understanding which entities/facts matter  

CEx‑Pck SHALL NOT:

- modify importance `value`, `role`, or `score`  
- merge or summarize importance entries  
- infer meaning from importance residues  

---

## **3.4 Next‑Context envelope (`TP.metadata.next_context`)**

If present (from prior MCB):

```python
TP.metadata.next_context.next_context
TP.metadata.next_context.direction
TP.metadata.next_context.coherence
TP.metadata.next_context.stance
TP.metadata.next_context.subculture
TP.metadata.next_context.next_context_provenance
```

CEx‑Pck uses next_context to:

- decide **copy‑forward vs reset** behavior  
- initialize context fields when CCR indicates continuity  
- seed MSL tokens for stance, direction, coherence, subculture  

CEx‑Pck SHALL:

- respect next_context provenance  
- never overwrite next_context metadata directly  
- only project next_context into the **current context shell**  

---

# **4. Deterministic Rule Ordering**

CEx‑Pck must apply operations in **exact order**:

1. Read IE structural hints (`TP.cex.ie`)  
2. Read CCR output (`TP.cex.ccr`)  
3. Read semantic‑importance (`TP.semantic.importance`)  
4. Read next_context metadata (if present)  
5. Derive context envelope fields:
   - topic, intent, stance, register, politeness, tone  
   - continuity, direction, coherence, importance  
   - clarifying_fields[]  
6. Construct MSL tokens:
   - qualifiers, clarifications, stance, shading, intent, direction, coherence, subculture  
7. Construct continuity + relevance flags from CCR alignment + decision  
8. Construct CIL metadata from CCR `selected_conversation`  
9. Construct semantic‑residue metadata from importance + CCR semantic_residue alignment  
10. Validate envelope + metadata boundaries  
11. Emit deterministic TP output for CE and downstream primitives  

This ordering ensures:

- replay determinism  
- Python/C++ parity  
- stable integration with CE, COB, CIL, CST, OB‑Set, IdOB, TR, RB  

---

# **5. Context & MSL Construction**

CEx‑Pck computes the **context shell** and **MSL tokens** in a bounded, deterministic way.

---

## **5.1 Context envelope derivation**

Inputs:

- `topic_hint`  
- `intent_hint`  
- `continuity_hint`  
- `direction_hint`  
- `coherence_hint`  
- `importance_hint`  
- CCR alignment (identity, context, continuity, reference, semantic_residue)  
- next_context (if present)  

Outputs:

- `topic` — derived from `topic_hint` or next_context.topic  
- `intent` — derived from `intent_hint`  
- `continuity` — derived from `continuity_hint` + CCR continuity alignment  
- `direction` — derived from `direction_hint` or next_context.direction  
- `coherence` — derived from `coherence_hint` or next_context.coherence  
- `importance` — derived from `importance_hint`  
- `stance`, `register`, `politeness`, `tone` — derived from IE hints + MSL tokens  
- `clarifying_fields[]` — derived from IE clarifying hints and CCR clarifying alignment  

CEx‑Pck SHALL:

- prefer next_context when CCR indicates **strong continuity**  
- reset context when CCR decision = `new` and continuity alignment = `none`  
- mark ambiguous continuity when CCR decision = `fallback`  

---

## **5.2 MSL token construction**

Inputs:

- IE hints (qualifier‑like phrases, clarifying phrases, stance/direction cues)  
- structural_phrases  
- next_context MSL metadata  
- CCR alignment (identity, clarifying, context, continuity, reference)  

Outputs:

- `TP.metadata.msl.qualifiers`  
- `TP.metadata.msl.clarifications`  
- `TP.metadata.msl.stance`  
- `TP.metadata.msl.shading`  
- `TP.metadata.msl.intent`  
- `TP.metadata.msl.direction`  
- `TP.metadata.msl.coherence`  
- `TP.metadata.msl.subculture`  

CEx‑Pck SHALL:

- treat MSL tokens as **short structured tokens**, not free‑text meaning  
- never assign semantic roles or perform stance interpretation beyond bounded categories  
- propagate MSL deterministically for CE, RB, IdOB, MCB consumption  

---

# **6. CCR‑Aligned Metadata Projection**

CEx‑Pck is the bridge between CCR output and TP metadata used by COB, CIL, CST, and downstream primitives.

---

## **6.1 CIL substrate metadata**

Inputs:

- `TP.cex.ccr.selected_conversation`  
- CCR provenance  

Outputs:

- `TP.metadata.cil.selected_conversation`  
- `TP.metadata.cil.cil_reference`  
- `TP.metadata.cil.projection_provenance`  

Rules:

- `selected_conversation` is copied verbatim from CCR  
- `cil_reference` is a deterministic reference to the static CIL substrate (`cil_input.yaml`)  
- provenance records origin = CEx‑CCR, projection = CEx‑Pck  

CEx‑Pck SHALL NOT:

- change `selected_conversation`  
- change CIL substrate identity  
- infer meaning from CIL content  

---

## **6.2 Semantic‑residue alignment metadata**

Inputs:

- `TP.cex.ccr.alignment.semantic_residue`  
- `TP.semantic.importance.entities[]`  
- `TP.semantic.importance.facts[]`  

Outputs:

- `TP.metadata.semantic_residue.entities[]`  
- `TP.metadata.semantic_residue.facts[]`  
- `TP.metadata.semantic_residue.alignment_scores`  
- `TP.metadata.semantic_residue.provenance`  

Rules:

- entities/facts are **referenced**, not transformed  
- alignment_scores reflect CCR semantic_residue alignment (`none | weak | moderate | strong`)  
- provenance records origin = CEx‑CCR, packaging = CEx‑Pck  

CEx‑Pck SHALL:

- expose semantic‑residue alignment for COB, CIL, CST  
- keep residues bounded and structured  

---

# **7. Bounded Semantic Domain**

CEx‑Pck operates strictly within a **bounded semantic domain**:

- uses only IE hints, CCR output, semantic‑importance, and next_context  
- does not infer meaning  
- does not use embeddings  
- does not use global semantics  
- does not perform identity‑conditioned interpretation (IdOB responsibility)  
- does not perform truth evaluation (TR/TB responsibility)  

CEx‑Pck SHALL:

- treat all residues and hints as **structural/adjacent cues**  
- construct context and MSL in a deterministic, rule‑driven way  
- leave semantic_core and TP committed meaning untouched  

---

# **8. Structural Schema (Post‑CEx‑Pck TP View)**

After CEx‑Pck, TP SHALL contain:

```python
context {
    topic: string
    stance: string
    intent: string
    register: string
    politeness: string
    tone: string
    continuity: string
    direction: string
    coherence: string
    importance: string
    clarifying_fields: [...]
}

TP.metadata.context {
    relevance_flags
    copy_forward_flags
    reset_flags
    context_fields
    context_provenance
}

TP.metadata.msl {
    qualifiers
    clarifications
    stance
    shading
    intent
    direction
    coherence
    subculture
}

TP.metadata.cil {
    selected_conversation
    cil_reference
    projection_provenance
}

TP.metadata.semantic_residue {
    entities: [...]
    facts: [...]
    alignment_scores
    provenance
}
```

All CCR output remains in:

```python
TP.cex.ccr { alignment, scores, decision, selected_conversation, provenance }
```

All semantic‑importance remains in:

```python
TP.semantic.importance { entities[], facts[] }
```

---

# **9. Replay Metadata & Determinism**

CEx‑Pck must be:

- deterministic  
- replay‑stable  
- rule‑stable  

Given identical:

- IE hints  
- CCR output  
- semantic‑importance residues  
- next_context metadata  

CEx‑Pck SHALL produce identical:

- context envelope  
- MSL metadata  
- CIL metadata  
- semantic‑residue metadata  

Python and C++ implementations MUST:

- use identical iteration ordering  
- avoid nondeterministic data structures  
- avoid nondeterministic sorting or hashing  
- construct envelopes in a stable, rule‑driven way  

---

# **10. Forbidden Behavior**

CEx‑Pck must not:

- modify IE fields  
- modify CCR fields (`TP.cex.ccr.*`)  
- modify semantic‑importance fields (`TP.semantic.importance.*`)  
- modify CIL substrate content  
- infer meaning or assign semantic roles  
- use embeddings or global semantics  
- write outside its allowed TP envelopes/metadata  
- perform lineage updates (COB/CIL/CST responsibility)  

---

# **11. Implementation Skeleton (Python)**

```python
class CExPck:
    def __init__(self, tp_input):
        self.tp = tp_input

    def inspect(self):
        # 1. Read IE hints
        ie = self.tp.get("cex", {}).get("ie", {})

        # 2. Read CCR output
        ccr = self.tp.get("cex", {}).get("ccr", {})

        # 3. Read semantic-importance
        importance = self.tp.get("semantic", {}).get("importance", {})

        # 4. Read next_context (if present)
        next_ctx = self.tp.get("metadata", {}).get("next_context", {})

        # 5. Derive context envelope
        context = self._build_context(ie, ccr, next_ctx)

        # 6. Derive MSL tokens
        msl = self._build_msl(ie, next_ctx)

        # 7. Build CIL metadata from CCR
        cil_meta = self._build_cil_metadata(ccr)

        # 8. Build semantic-residue metadata from CCR + importance
        residue_meta = self._build_semantic_residue_metadata(ccr, importance)

        # 9. Write envelopes/metadata back into TP (bounded, deterministic)
        self._update_tp(context, msl, cil_meta, residue_meta)

    # Internal helpers: _build_context, _build_msl, _build_cil_metadata,
    # _build_semantic_residue_metadata, _update_tp
```

---

# **12. Implementation Skeleton (C++)**

C++ implementation SHALL mirror Python behavior:

- identical input envelopes  
- identical field derivation rules  
- identical ordering  
- identical metadata writes  

Skeleton (conceptual):

```cpp
class CExPck {
public:
    explicit CExPck(TP& tp_input) : tp(tp_input) {}

    void inspect() {
        auto ie         = tp.cex.ie;
        auto ccr        = tp.cex.ccr;
        auto importance = tp.semantic.importance;
        auto next_ctx   = tp.metadata.next_context;

        auto context      = build_context(ie, ccr, next_ctx);
        auto msl          = build_msl(ie, next_ctx);
        auto cil_metadata = build_cil_metadata(ccr);
        auto residue_meta = build_semantic_residue_metadata(ccr, importance);

        update_tp(context, msl, cil_metadata, residue_meta);
    }

private:
    TP& tp;
    // helper methods as in Python, implemented deterministically
};
```

---

# **13. TP Field Schema — Downstream Consumption Map (Normative)**

This section defines the **complete authoritative schema** for all TP fields written by the CEx‑Pck structural program.  
It specifies:

- field names  
- datatypes  
- TP envelope locations  
- provenance requirements  
- downstream consumers  
- purpose of consumption  

All fields SHALL comply with:

- **20.105_tp_requirements.md**  
- **20.105.010_tp_meta_fields.md**  
- **20.105.020_tp_meta_provenance.md**  
- **20.105.030_tp_meta_usage.md**  
- **20.15_ts_architecture_scaffold.md**  

CEx‑Pck SHALL NOT write fields outside the schema defined below.

---

## **13.1 Context Metadata Fields (`TP.metadata.context_metadata`)**

| TP Location | Field Name | Type | Allowed Values | Written By | Downstream Consumers | Purpose |
|------------|------------|------|----------------|------------|-----------------------|---------|
| `TP.metadata.context.context_fields.topic` | `topic` | string | bounded structural category | CEx‑Pck | CE, SOB, SROB, CnOB, SmOB, IdOB, TR, RB | Context envelope; structural + semantic‑adjacent residue; routing |
| `TP.metadata.context.context_fields.intent` | `intent` | string | bounded structural category | CEx‑Pck | CE, IdOB | Identity‑conditioned meaning; context envelope |
| `TP.metadata.context.context_fields.stance` | `stance` | string | bounded MSL category | CEx‑Pck | IdOB, TR, RB, CIL, CST | Identity refinement; routing; continuity |
| `TP.metadata.context.context_fields.register` | `register` | string | bounded structural category | CEx‑Pck | CE, IdOB | Context envelope; identity refinement |
| `TP.metadata.context.context_fields.politeness` | `politeness` | string | bounded structural category | CEx‑Pck | CE, IdOB | Context envelope; identity refinement |
| `TP.metadata.context.context_fields.tone` | `tone` | string | bounded structural category | CEx‑Pck | CE, IdOB | Context envelope; identity refinement |
| `TP.metadata.context.context_fields.continuity` | `continuity` | string | `none|weak|moderate|strong` | CEx‑Pck | CE, TR, RB, COB, CIL, CST | Continuity evaluation; routing; lineage stability |
| `TP.metadata.context.context_fields.direction` | `direction` | string | bounded MSL category | CEx‑Pck | CE, IdOB, TR, RB | Routing; identity refinement |
| `TP.metadata.context.context_fields.coherence` | `coherence` | string | bounded MSL category | CEx‑Pck | CE, IdOB, TR, RB | Routing; identity refinement |
| `TP.metadata.context.context_fields.importance` | `importance` | string | bounded structural category | CEx‑Pck | OB‑Set, IdOB, TR | Structural + semantic‑adjacent residue; routing |
| `TP.metadata.context.context_fields.clarifying_fields[]` | `clarifying_fields` | array | bounded clarifying metadata | CEx‑Pck | CE, IdOB, TR, COB, CIL, CST | Clarification lineage; identity refinement; continuity |

### **Context Metadata Provenance**
All fields SHALL record provenance:
- origin = CEx‑Pck  
- last update = CEx‑Pck  
- commit lineage = TPU commit  

---

## **13.2 Meaning Signal Layer Fields (`TP.metadata.msl_metadata`)**

| TP Location | Field Name | Type | Allowed Values | Written By | Downstream Consumers | Purpose |
|------------|------------|------|----------------|------------|-----------------------|---------|
| `TP.metadata.msl.qualifiers` | `qualifiers` | array<string> | bounded MSL tokens | CEx‑Pck | IdOB, TR, RB, CIL, CST | Identity refinement; routing; continuity |
| `TP.metadata.msl.clarifications` | `clarifications` | array<string> | bounded MSL tokens | CEx‑Pck | IdOB, TR, COB, CIL, CST | Clarification lineage; continuity |
| `TP.metadata.msl.stance` | `stance` | string | bounded MSL category | CEx‑Pck | IdOB, TR, RB | Identity refinement; routing |
| `TP.metadata.msl.shading` | `shading` | string | bounded MSL category | CEx‑Pck | IdOB | Identity refinement |
| `TP.metadata.msl.intent` | `intent` | string | bounded MSL category | CEx‑Pck | IdOB, CE | Identity refinement; context envelope |
| `TP.metadata.msl.direction` | `direction` | string | bounded MSL category | CEx‑Pck | TR, RB, IdOB | Routing; identity refinement |
| `TP.metadata.msl.coherence` | `coherence` | string | bounded MSL category | CEx‑Pck | TR, RB, IdOB | Routing; identity refinement |
| `TP.metadata.msl.subculture` | `subculture` | string | bounded MSL category | CEx‑Pck | IdOB, CIL, CST | Identity refinement; continuity |

### **MSL Provenance**
All fields SHALL record provenance:
- origin = CEx‑Pck  
- last update = CEx‑Pck  

---

## **13.3 CIL Metadata Fields (`TP.metadata.cil_metadata`)**

| TP Location | Field Name | Type | Allowed Values | Written By | Downstream Consumers | Purpose |
|------------|------------|------|----------------|------------|-----------------------|---------|
| `TP.metadata.cil.selected_conversation` | `selected_conversation` | int or null | CCR decision | CEx‑Pck | COB, CIL, CST | Conversation lineage update; continuity |
| `TP.metadata.cil.cil_reference` | `cil_reference` | string | static CIL substrate ID | CEx‑Pck | COB, CIL, CST | Deterministic substrate selection |
| `TP.metadata.cil.projection_provenance` | `projection_provenance` | object | provenance structure | CEx‑Pck | COB, CIL, CST | Projection lineage |

### **CIL Metadata Provenance**
All fields SHALL record provenance:
- origin = CEx‑CCR  
- packaging = CEx‑Pck  
- immutable after TPU commit  

---

## **13.4 Semantic‑Residue Metadata Fields (`TP.metadata.semantic_residue_metadata`)**

| TP Location | Field Name | Type | Allowed Values | Written By | Downstream Consumers | Purpose |
|------------|------------|------|----------------|------------|-----------------------|---------|
| `TP.metadata.semantic_residue.entities[]` | `entities` | array<object> | structured residues | CEx‑Pck | COB, CIL, CST, IdOB | Continuity; identity refinement; stability |
| `TP.metadata.semantic_residue.facts[]` | `facts` | array<object> | structured residues | CEx‑Pck | COB, CIL, CST, IdOB | Continuity; identity refinement; stability |
| `TP.metadata.semantic_residue.alignment_scores` | `alignment_scores` | string | `none|weak|moderate|strong` | CEx‑Pck | COB, CIL, CST | Residue alignment; stability |
| `TP.metadata.semantic_residue.provenance` | `provenance` | object | provenance structure | CEx‑Pck | COB, CIL, CST | Deterministic lineage |

### **Semantic‑Residue Provenance**
All fields SHALL record provenance:
- origin = CEx‑CCR  
- packaging = CEx‑Pck  
- immutable after TPU commit  

---

## **13.5 CCR Output Fields (Read‑Only for CEx‑Pck)**

CEx‑Pck SHALL NOT modify:

```
TP.cex.ccr.alignment.*
TP.cex.ccr.scores.*
TP.cex.ccr.decision
TP.cex.ccr.selected_conversation
TP.cex.ccr.provenance
```

### **Downstream Consumers**
- COB  
- CIL  
- CST  
- IdOB  
- CE  
- OB‑Set  
- TR  
- RB  

### **Purpose**
- identity continuity  
- conversation selection  
- stability evaluation  
- routing  
- identity refinement  

---

## **13.6 Semantic‑Importance Fields (Read‑Only for CEx‑Pck)**

CEx‑Pck SHALL NOT modify:

```
TP.semantic.importance.entities[]
TP.semantic.importance.facts[]
```

### **Downstream Consumers**
- CEx‑CCR  
- COB  
- CIL  
- CST  
- IdOB  
- RBU / RB  

### **Purpose**
- semantic‑residue alignment  
- continuity  
- identity refinement  
- routing  

---

## **13.7 Summary of Downstream Consumption**

| Primitive | Consumes | Purpose |
|----------|----------|---------|
| **CE** | context_fields, MSL | Build context envelope |
| **SOB/SROB/CnOB/SmOB** | context_fields, MSL | Structural + semantic‑adjacent residue |
| **IdOB** | context_fields, MSL, semantic_residue | Identity‑conditioned meaning |
| **TR** | context_fields, MSL | Routing vector |
| **RB** | context_fields, MSL, CCR alignment | Basin selection |
| **COB** | selected_conversation, semantic_residue | Project residues into CIL |
| **CIL** | selected_conversation, semantic_residue | Continuity + lineage |
| **CST** | CCR scores, semantic_residue | Drift/collapse/stability |
| **TPU** | provenance | Commit lineage |
| **CTP/RTU** | context_fields | Routing updates |
| **OuBA** | context_fields | Freeze metadata |
| **SSRGn** | semantic_residue | SSR projection |

---

# **14. Change Management**

When CEx‑Pck evolves:

- update context derivation rules  
- update MSL packaging rules  
- update CIL metadata schema (if 20.105/20.105.010/020/030 change)  
- update semantic‑residue metadata schema  
- update testbench (`cex_pck_testbench.yaml`)  
- update rulechecker (`cex_pck_rules.yaml`, `cex_pck_rulescheck.py`)  
- update 20.107.030 (CEx‑Pck primitive spec)  
- ensure replay determinism  
- ensure Python/C++ parity  

---
