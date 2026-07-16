# **cob_interface_to_ssrgn.md**  
### *Conversation Object Basin — Interface to SSRGn (Working Draft v0.1)*

---

## **0. Purpose**
This paper defines the **COB → SSRGn interface contract**: what COB expects SSRGn to provide, how regenerated meaning must be structured, and how SSRGn must behave to maintain deterministic, stable identity layers.

All questions for COB are maintained separately in:

```
questions_for_cob_substrate.md (v0.4)
```

This paper does **not** repeat those questions.  
It complements:

- `cob_context_resolution.md`  
- `cob_lifecycle_and_capacity.md`  
- `cob_interaction_and_safety.md`  
- `cob_expectations_for_cst.md`

and precedes the CEx interface paper.

---

# **1. Role of SSRGn from COB’s Perspective**
From COB’s point of view, SSRGn is the **regeneration engine** that produces:

- regenerated referents  
- regenerated attributes  
- regenerated ambiguity  
- regenerated structure  
- regenerated lineage hints  
- regenerated confidence scores  

COB ingests these packets deterministically.

SSRGn must **never** directly modify COB.  
SSRGn acts only by providing structured packets.

---

# **2. Required SSRGn Packet Structure**

SSRGn must provide packets with the following fields:

```json
SSRGnPacket {
    referents: [RegeneratedReferent],
    attributes: { key: value },
    ambiguity: AmbiguityStructure,
    lineage_hints: LineageHintStructure,
    structure: StructuralRepresentation,
    confidence: float,
    timestamps: {
        generated: TurnID
    }
}
```

### **2.1 Regenerated Referent Structure**
```json
RegeneratedReferent {
    surface_forms: [string],
    attributes: { key: value },
    confidence: float,
    ambiguity: float,
    lineage_pointer: StableID | null
}
```

### **2.2 Ambiguity Structure**
Must encode:

- referent collisions  
- referent uncertainty  
- attribute uncertainty  
- structural uncertainty  

### **2.3 Lineage Hint Structure**
Must encode:

- continuity cues  
- referent ancestry hints  
- identity drift indicators  

### **2.4 Structural Representation**
Must encode:

- regenerated semantic structure  
- regenerated relational structure  
- regenerated contextual structure  

---

# **3. SSRGn Ordering Expectations**

SSRGn must deliver packets in deterministic order:

1. **Turn order**  
2. **Within-turn regeneration order**  
3. **Referent ordering**  
4. **Attribute ordering**  
5. **Ambiguity ordering**

SSRGn must never reorder packets nondeterministically.

---

# **4. SSRGn Ambiguity Expectations**

SSRGn must provide ambiguity signals that COB can interpret deterministically:

### **4.1 Required Ambiguity Types**
- referent ambiguity  
- attribute ambiguity  
- structural ambiguity  
- lineage ambiguity  
- identity ambiguity  

### **4.2 Ambiguity Encoding Rules**
Ambiguity must be:

- explicit  
- numeric  
- bounded  
- deterministic  
- replay-safe  

SSRGn must never provide stochastic ambiguity.

---

# **5. SSRGn Lineage Expectations**

SSRGn must provide lineage hints that COB can use to maintain continuity:

### **5.1 Required Lineage Hints**
- referent ancestry  
- identity continuity  
- drift indicators  
- merge/split indicators  

### **5.2 Forbidden Lineage Actions**
SSRGn must **never**:

- create lineage nodes directly  
- delete lineage nodes  
- modify lineage structure  
- override COB lineage decisions  

SSRGn may only provide **hints**, not structural changes.

---

# **6. SSRGn Confidence Expectations**

SSRGn must provide confidence scores for:

- referents  
- attributes  
- ambiguity  
- structure  
- lineage hints  

Confidence must be:

- numeric  
- bounded  
- deterministic  
- monotonic  
- replay-safe  

COB uses confidence to weight merges and resolve conflicts.

---

# **7. SSRGn Safety Expectations**

### **7.1 Forbidden Actions**
SSRGn must never:

- force layer creation  
- force layer deletion  
- override CST signals  
- modify COB directly  
- reorder COB layers  
- modify referent maps  
- modify lineage  
- modify timestamps  
- modify decay_state  

### **7.2 Required Safety Guarantees**
SSRGn must:

- preserve referent identity  
- preserve structural consistency  
- preserve ordering  
- preserve determinism  
- preserve replay safety  

### **7.3 Collapse Interaction**
If SSRGn detects collapse:

- SSRGn must raise ambiguity  
- SSRGn must raise uncertainty  
- SSRGn must not attempt recovery  
- SSRGn must defer to CST and COB  

---

# **8. COB Ingestion Expectations**

COB expects SSRGn packets to be:

- complete  
- ordered  
- deterministic  
- replay-safe  
- structurally consistent  
- ambiguity-aware  
- lineage-aware  

COB ingests packets using:

- deterministic merge logic  
- assignment algorithm  
- ambiguity penalties  
- lineage continuity  
- decay adjustments  

---
