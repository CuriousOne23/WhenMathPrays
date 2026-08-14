# ⭐ **tp_context_layer1.md (Draft)**  
### *Thought Simulator — TP Architecture / Context Layer Paper*

---

# **TP Context Layer1 (Path‑A)**  
The **Context Layer1** is the portion of the Thought Packet (TP) responsible for capturing, normalizing, and committing the contextual state of a turn.  
It is the boundary between:

- **raw, volatile, upstream‑dependent context data**, and  
- **canonical, bounded, replay‑safe context metadata**.

This document explains:

- what Context Data is  
- what Context Metadata is  
- why the distinction exists  
- how CE normalizes raw context  
- how TPU commits canonical context  
- how clarifying fields are bounded  
- how the Context Layer supports long‑horizon continuity  
- producer/consumer relationships  
- high‑level examples  

This paper is intentionally conceptual.  
Implementation details appear in the corresponding primitive specifications.

---

# **1. Purpose of the Context Layer**

The Context Layer exists to:

- capture the **contextual meaning** of a turn  
- convert raw context into **canonical metadata**  
- enforce the **semantic firewall** between extraction and commitment  
- ensure **deterministic replay**  
- maintain **long‑horizon continuity**  
- provide stable context signals to downstream primitives (OuBA, COB, CEx, CE, TPU)

The Context Layer is the **first and most important envelope** in the TP because every other envelope depends on its canonicalization.

---

# **2. Context Data (Raw)**  
### *Produced by CEx‑Pck*

**Context Data** is the raw, unbounded, volatile representation of context extracted from upstream signals.

It is composed of:

- IE structural hints  
- CCR alignment signals  
- CIL substrate fields  
- COB clarifying fields  
- next‑turn context (MCB → TP.next_context{})  
- stability indicators (CST‑Core, CST‑MS)  
- importance signals (IdOB, SmOB)  
- routing hints  
- semantic residues  

These fields are:

- **not canonical**  
- **not bounded**  
- **not replay‑safe**  
- **not ordered deterministically**  
- **not provenance‑stamped**  
- **not suitable for TPU commit**

Raw context is **volatile** because it depends on:

- extraction heuristics  
- alignment decisions  
- upstream noise  
- routing arbitration  
- semantic geometry  
- identity‑layer transitions  

Raw context is **never** written into the TP.

It is only an **input** to CE.

---

# **3. Context Metadata (Canonical)**  
### *Produced by CE → Committed by TPU*

**Context Metadata** is the canonical, bounded, replay‑safe representation of context.

It is the version of context that:

- TPU commits  
- downstream primitives read  
- replay reconstructs  
- provenance tracks  
- continuity depends on  

Context Metadata is produced by **CE**, which performs:

- canonicalization  
- bounding  
- normalization  
- deterministic ordering  
- provenance stamping  
- replay‑safe structuring  

Context Metadata is **immutable** after TPU commit.

---

# **4. Normalization (Canonicalization)**  
Normalization in Path‑A is **semantic canonicalization**, not statistical scaling.

Normalization converts raw context into canonical metadata using:

- canonical topic schema  
- canonical intent schema  
- canonical stance schema  
- canonical continuity schema  
- canonical politeness schema  
- canonical register schema  
- canonical importance rules  
- canonical ordering rules  
- bounded clarifying‑field schema (10 / 100 / 4)  
- provenance schema  
- replay determinism rules  

Normalization ensures:

- every TP has a **consistent structure**  
- every field is **bounded**  
- every field is **canonical**  
- every field is **deterministic**  
- every field is **replay‑safe**

Normalization is the core function of CE.

---

# **5. Clarifying Fields (Bounded)**  
Clarifying fields are the structured representation of contextual meaning.

They are bounded by:

- **10 clarifying fields per turn**  
- **100 total subfields**  
- **4 hierarchical levels**

These bounds ensure:

- replay determinism  
- memory stability  
- identity‑layer continuity  
- canonical ordering  
- bounded semantic complexity  

Clarifying fields originate from:

- COB  
- next‑turn context  
- semantic residues  
- structural hints  
- alignment signals  

CE rewrites them into canonical form.

---

# **6. Producer / Consumer Relationships**

| Component | Role | Produces | Consumes |
|----------|------|----------|----------|
| **CEx‑Pck** | Extraction | Context Data | CCR Output, CIL Metadata |
| **CE** | Semantic Firewall | Context Metadata | Context Data |
| **TPU** | Commit Layer | Committed TP | Context Metadata |
| **OuBA** | Meaning Layer | Meaning Packets | TP.context_metadata |
| **COB** | Identity Layer | Identity Snapshot | TP.context_metadata |
| **CEx‑IE / CEx‑CCR** | Alignment | Structural Hints | TP.context_metadata |
| **ISc** | Coherence | Coherence Signals | TP.context_metadata |

Context Metadata is consumed by **all downstream primitives**.

---

# **7. How the Context Layer Supports Path‑A**

### **Long‑Horizon Continuity**  
Context Metadata provides:

- canonical topic  
- canonical intent  
- canonical stance  
- canonical continuity  
- canonical importance  
- canonical clarifying fields  

These allow COB and CEx to maintain continuity across turns.

### **Deterministic Replay**  
Because Context Metadata is:

- bounded  
- canonical  
- deterministic  
- provenance‑stamped  

Replay can reconstruct the exact contextual state of any turn.

### **Semantic Stability**  
Context Metadata provides stable signals for:

- identity selection  
- alignment  
- routing  
- structural geometry  
- importance integration  

### **Commit Integrity**  
TPU uses Context Metadata to:

- perform atomic commit  
- maintain provenance  
- integrate freeze signatures  
- integrate entropy  
- maintain replay lineage  

---

# **8. High‑Level Examples**

### **Raw Context Data (CEx‑Pck)**  
```
topic_raw: "register shift"
intent_raw: "kinda clarifying"
politeness_raw: "polite-ish"
continuity_hint_raw: "weak"
importance_raw: 0.73
clarifying_fields_raw: [...]
next_turn_context_raw: {...}
```

### **Canonical Context Metadata (CE → TPU)**  
```
context_metadata {
    topic: "register shift"
    intent: "clarify"
    stance: "neutral"
    continuity: "weak"
    importance: canonical_score
    clarifying_fields: bounded[10][100][4]
    provenance: {ce_version, ce_ordering, ce_bounds}
}
```

This transformation is the essence of the semantic firewall.

---

# **9. Relationship to Other Papers**

This paper is part of the TP Architecture set:

- `tp_overview.md` — high‑level overview  
- `tp_context_layer.md` — this document  
- `tp_semantic_layer.md` — meaning + importance  
- `tp_alignment_layer.md` — CCR + CIL  
- `tp_structural_routing_layer.md` — geometry + routing  
- `tp_commit_layer.md` — provenance + entropy + freeze  

Each paper explains one conceptual layer of the TP.

---

# **End of tp_context_layer.md**

---
