# **context_requirements.md (v2.0‑M)**  
### *Unified Context Subsystem Requirements — Modernized Architecture*

---

# **0. Introduction (Informative — No SHALLs)**

The unified **Context Subsystem** is now a **full TP‑state constructor**, not merely a stability/identity packet generator.  
It integrates four coordinated blocks:

- **CST Subsytem** — composed of CST‑Core, CST‑MS, and CST‑Mux — performs identity‑layer stability analysis 
- **COB** — identity‑layer construction and evolution  
- **CIL** — intake packet construction for CEx  
- **CEx** — extraction of next‑turn context fields for CE  

This v2.0 modernization aligns the subsystem with:

- expanded TP metadata envelope  
- expanded TP.next_context envelope  
- expanded TP provenance envelope  
- identity‑layer snapshot (TP.cob_state_snapshot)  
- deterministic TPSnS commit envelope  
- COB/CST/CIL/CEx/CE/ISc global requirements  
- merge/split continuity rules  
- freeze/thaw continuity rules  
- structural‑only validation rules  

This document replaces the older “OuBA‑like input” model with the **TPSnS identity‑layer snapshot**, ensuring compatibility with the full Path A → OuBA → TPSnS → COB → CST → CIL → CEx → CE → ISc pipeline.

---

# **1. Purpose (Normative)**

The unified context subsystem SHALL:

- integrate CST, COB, CIL, and CEx into a deterministic pipeline  
- propagate identity‑layer continuity  
- propagate next‑turn context fields  
- propagate metadata and provenance  
- construct a CEx‑compatible intake packet  
- maintain TP historical continuity  
- support deterministic replay across turns  

In this document, “CST” refers to the unified CST subsystem composed of CST‑Core, CST‑MS, and CST‑Mux

---

# **2. Scope (Normative)**

This document defines:

- CST stability signal generation  
- COB identity‑layer evolution  
- CIL intake packet construction  
- CEx extraction behavior  
- TP.next_context propagation  
- metadata and provenance propagation  
- deterministic replay rules  
- merge/split continuity  
- freeze/thaw continuity  
- structural‑only validation rules  

It does **not** redefine global architecture in:

- **20.105 TP Requirements**  
- **20.32 COB Requirements**  
- **20.32.010 CST Requirements**  
- **20.33 CIL Requirements**  
- **20.107 CEx Requirements**  
- **20.108 CE Requirements**  
- **20.44 ISc Requirements**

Global documents remain authoritative.

---

# **3. Inputs (Normative)**

### **3.1 TPSnS Identity‑Layer Snapshot**  
The unified context subsystem SHALL ingest:

- `TP.cob_state_snapshot`  
- `TP.lineage_log[]`  
- `TP.metadata.*`  
- `TP.next_context.*`  
- `TP.semantic.*` (identity‑relevant fields only)

### **3.2 CST Stability Signals**  
CST SHALL produce stability signals derived from:

- identity‑layer objects  
- lineage continuity  
- metadata continuity  
- next‑turn context continuity  
- freeze/thaw state  

---

# **4. Outputs (Normative)**

### **4.1 COB Identity‑Layer Objects**  
COB SHALL produce stabilized identity‑layer objects containing:

- referent maps  
- anchors  
- lineage continuity  
- ambiguity/certainty metrics  
- stability metrics  
- merge/split continuity  
- freeze/thaw continuity  
- next‑turn context integration  

### **4.2 CST Stability Signals**  
CST SHALL produce:

- drift  
- oscillation  
- collapse  
- merge/split continuity  
- freeze/thaw continuity  
- certainty/ambiguity adjustments  
- lineage stability  

### **4.3 CIL Intake Packet**  
CIL SHALL produce a structured packet containing:

- stabilized identity‑layer objects  
- CST stability block  
- ordering metrics  
- ambiguity/certainty summaries  
- lineage hints  
- next‑turn context fields  
- packet metadata  

### **4.4 TP Historical Datastream**  
TP SHALL record:

- CST actions  
- COB transformations  
- CIL packet construction  
- next‑turn context propagation  
- metadata continuity  
- provenance continuity  
- deterministic replay markers  

---

# **5. Unified Context Pipeline (Normative)**

The pipeline SHALL execute in the deterministic sequence:

```
TPSnS → CST → COB → CIL → CEx → CE → ISc → TPU → TP
```

This replaces the older “OuBA‑like input” model.

---

# **6. Unified Testing (Normative + Informative)**

The unified context testbench SHALL validate:

- CST stability signal generation  
- COB identity‑layer evolution  
- CIL packet construction  
- CEx extraction correctness  
- CE representation correctness  
- ISc consumption correctness  
- TP historical continuity  
- deterministic replay  
- merge/split continuity  
- freeze/thaw continuity  
- next‑turn context propagation  
- metadata continuity  
- provenance continuity  

---

# **7. Tested Behaviors (Expanded)**

### **7.1 CST Behavior**  
CST SHALL detect:

- drift  
- oscillation  
- collapse  
- valid instability  
- freeze/thaw continuity  
- lineage stability  
- ambiguity/certainty changes  
- merge/split continuity  
- next‑turn context continuity  

### **7.2 COB Behavior**  
COB SHALL propagate:

- referent maps  
- anchors  
- lineage  
- ambiguity/certainty  
- stability metrics  
- merge/split continuity  
- freeze/thaw continuity  
- next‑turn context fields  

### **7.3 CIL Behavior**  
CIL SHALL construct packets containing:

- identity‑layer objects  
- CST stability signals  
- next‑turn context fields  
- metadata continuity  
- lineage hints  
- ordering metrics  

### **7.4 CEx Behavior**  
CEx SHALL extract:

- next‑turn context fields  
- stability hints  
- identity‑layer continuity  
- metadata continuity  

### **7.5 CE Behavior**  
CE SHALL represent:

- next‑turn context fields  
- continuity_status  
- stability_status  

### **7.6 ISc Behavior**  
ISc SHALL consume:

- next‑turn context fields  
- structural metadata  
- stability metadata  

### **7.7 TP Historical Continuity**  
TP SHALL record:

- CST signals  
- COB transformations  
- CIL packet structure  
- CEx extraction  
- CE representation  
- ISc consumption  

---

# **8. Additional Tests (New)**

### **8.1 Metadata Continuity Tests**  
Verify propagation of:

- alignment  
- identity shift  
- topic anchor  
- continuity record  
- intent record  

### **8.2 Provenance Continuity Tests**  
Verify propagation of:

- lineage_log[]  
- signature_history[]  
- entropy_history[]  

### **8.3 Next‑Turn Context Tests**  
Verify propagation of:

- topic  
- stance  
- intent  
- continuity  
- direction  
- coherence  
- importance  
- clarifying_fields[]  

### **8.4 Freeze/Thaw Continuity Tests**  
Verify:

- no instability on freeze/thaw  
- continuity preserved  
- metadata preserved  

### **8.5 Merge/Split Continuity Tests**  
Verify:

- no instability caused by merge/split  
- valid instability passes immediately  
- lineage continuity preserved  

### 8.6 Unified Merge/Split Pipeline Test (New)
The unified context testbench SHALL validate that CST‑Core detects MERGE/SPLIT events, CST‑MS preserves structural neutrality, CST‑Mux produces stable USP flags, COB evolves identity‑layer objects correctly under structural transitions, and CIL constructs an intake packet that reflects the correct post‑merge/post‑split identity‑layer topology. The test SHALL confirm that structural transitions do not produce false instability and that valid instability on unrelated objects is preserved.

---

# **9. High‑Level Requirements (HLRs)**  
*(All SHALL statements appear only here)*

### **HLR‑CnTxt‑001**  
The unified context subsystem SHALL execute CST → COB → CIL → CEx → CE → ISc in deterministic sequence.

### **HLR‑CnTxt‑002**  
CST SHALL provide stability signals to COB, CIL, and CEx.

### **HLR‑CnTxt‑003**  
COB SHALL evolve identity‑layer objects using CST stability signals.

### **HLR‑CnTxt‑004**  
CIL SHALL construct an intake packet using identity‑layer objects and CST stability signals.

### **HLR‑CnTxt‑005**  
TP SHALL record historical continuity from CST, COB, CIL, CEx, CE, and ISc.

### **HLR‑CnTxt‑006**  
The unified context subsystem SHALL produce deterministic outputs under identical inputs.

### **HLR‑CnTxt‑007**  
Merge/split events SHALL preserve structural continuity and SHALL NOT produce instability.

### **HLR‑CnTxt‑020** — Unified Merge/Split Detection and Propagation
The unified context subsystem (CST‑Core, CST‑MS, CST‑Mux, COB, and CIL) SHALL detect MERGE and SPLIT events originating from the identity‑layer snapshot and SHALL propagate structural continuity deterministically across all stages of the pipeline. MERGE/SPLIT events SHALL NOT produce instability signals, and valid instability on unrelated objects SHALL pass immediately.

### **HLR‑CnTxt‑008**  
CIL SHALL produce a packet conforming to the schema required by CEx.

### **HLR‑CnTxt‑009**  
One‑time structural corrections SHALL NOT produce instability signals.

### **HLR‑CnTxt‑010**  
Next‑turn context fields SHALL propagate deterministically through COB → CIL → CEx → CE → ISc.

### **HLR‑CnTxt‑011**  
COB SHALL ingest next‑turn context fields and incorporate them into identity‑layer continuity.

### **HLR‑CnTxt‑012**  
CIL SHALL place next‑turn context fields into the intake packet without modification.

### **HLR‑CnTxt‑013**  
CEx SHALL extract next‑turn context fields exactly as defined in 20.107.

### **HLR‑CnTxt‑014**  
CE SHALL represent next‑turn context fields deterministically and expose them to ISc.

### **HLR‑CnTxt‑015**  
ISc SHALL consume next‑turn context fields as structural metadata.

### **HLR‑CnTxt‑016**  
Next‑turn context propagation SHALL be deterministically replayable.

### **HLR‑CnTxt‑017**  
Next‑turn context field names SHALL originate exclusively from 20.105.

### **HLR‑CnTxt‑018**  
Next‑turn context validation SHALL be structural‑only.

### **HLR‑CnTxt‑019**  
Next‑turn context fields SHALL remain stable across freeze/thaw cycles.

---

# **10. Determinism Notes (Informative)**  
Deterministic replay ensures identical TPSnS inputs produce identical CST, COB, CIL, CEx, CE, and ISc outputs.

---

# **11. Interface Contracts (Informative)**

- CST → COB  
- CST → CIL  
- COB → CIL  
- CIL → CEx  
- CEx → CE  
- CE → ISc  
- Context → TP  

---

# **12. Error Handling (Informative)**  
Malformed identity‑layer objects, CST signals, or packet structures are rejected.

---

# **13. Simulation Notes (Informative)**  
This document defines the system_playground version of the unified context subsystem.

---
