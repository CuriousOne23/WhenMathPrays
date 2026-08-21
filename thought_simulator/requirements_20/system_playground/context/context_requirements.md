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

# **4. Path‑A Context Substrate Extensions (Informative)**

The Path‑A context substrate now includes several additional fields produced and propagated through the COB → CIL → CEx → CE → MCB pipeline. These fields extend the unified context model and allow downstream primitives to maintain long‑horizon continuity, lineage stability, and deterministic context evolution.

### **Identity Lineage**
The context substrate includes identity‑lineage structures originating in COB and reflected through CIL, CEx‑Pck, and CE. These lineage structures describe the long‑term identity‑layer relationships used for continuity, fallback selection, and context reconstruction.

### **Continuity Lineage**
The context substrate includes continuity‑lineage information representing turn‑to‑turn continuity, context shifts, fallback continuity, and lineage‑based stability. This continuity lineage is preserved across TPU commit and freeze/thaw cycles.

### **Topology**
The context substrate includes identity‑layer topology describing the graph structure of identity layers and referent relationships. This topology is produced by COB, reflected by CIL, projected by CEx‑Pck, and consumed by CE and MCB for context‑coherence and shift‑detection.

### **Scalar Metrics**
The context substrate includes bounded‑semantic scalar metrics originating in COB and propagated through CIL and CEx‑Pck. These metrics include ambiguity, collapse risk, drift, stability, and lineage confidence. Downstream primitives use these metrics for continuity reasoning, fallback logic, and context‑coherence evaluation.

### **Register Continuity**
The context substrate includes register‑continuity signals describing long‑horizon register stability and transitions. These signals are produced by COB, reflected by CIL, projected by CEx‑Pck, and consumed by CE and MCB for next‑turn register and politeness generation.

### **Importance Continuity**
The context substrate includes importance‑continuity signals representing long‑horizon importance propagation across identity layers. These signals are used by CEx and MCB to maintain importance‑weighted continuity and next‑turn importance fields.

### **Next‑Turn Context Fields**
The context substrate includes next‑turn context fields generated exclusively by MCB and consumed by COB in the next cycle. These fields include topic, stance, intent, register, politeness, epistemic shading, continuity, direction, coherence, shift‑required, and importance. They form the bridge between meaning‑layer interpretation and long‑horizon identity‑layer continuity.

### **Propagation Loop**
All lineage, topology, metrics, continuity, and next‑turn context fields propagate deterministically through:

```
COB → CIL → CEx‑IE → CEx‑CCR → CEx‑Pck → CE → MCB → COB(next turn)
```

This propagation ensures that the unified context subsystem maintains a stable, deterministic, replay‑safe representation of conversational identity, continuity, and next‑turn context across all Path‑A cycles.

---

# **5. Outputs (Normative)**

### **5.1 COB Identity‑Layer Objects**  
COB SHALL produce stabilized identity‑layer objects containing:

- referent maps  
- anchors  
- lineage continuity  
- ambiguity/certainty metrics  
- stability metrics  
- merge/split continuity  
- freeze/thaw continuity  
- next‑turn context integration  

### **5.2 CST Stability Signals**  
CST SHALL produce:

- drift  
- oscillation  
- collapse  
- merge/split continuity  
- freeze/thaw continuity  
- certainty/ambiguity adjustments  
- lineage stability  

### **5.3 CIL Intake Packet**  
CIL SHALL produce a structured packet containing:

- stabilized identity‑layer objects  
- CST stability block  
- ordering metrics  
- ambiguity/certainty summaries  
- lineage hints  
- next‑turn context fields  
- packet metadata  

### **5.4 TP Historical Datastream**  
TP SHALL record:

- CST actions  
- COB transformations  
- CIL packet construction  
- next‑turn context propagation  
- metadata continuity  
- provenance continuity  
- deterministic replay markers  

---

# **6. Unified Context Pipeline (Normative)**

The pipeline SHALL execute in the deterministic sequence:

```
TPSnS → CST → COB → CIL → CEx → CE → ISc → TPU → TP
```

This replaces the older “OuBA‑like input” model.

---

# **7. Unified Testing (Normative + Informative)**

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

# **8. Tested Behaviors (Expanded)**

### **8.1 CST Behavior**  
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

### **8.2 COB Behavior**  
COB SHALL propagate:

- referent maps  
- anchors  
- lineage  
- ambiguity/certainty  
- stability metrics  
- merge/split continuity  
- freeze/thaw continuity  
- next‑turn context fields  

### **8.3 CIL Behavior**  
CIL SHALL construct packets containing:

- identity‑layer objects  
- CST stability signals  
- next‑turn context fields  
- metadata continuity  
- lineage hints  
- ordering metrics  

### **8.4 CEx Behavior**  
CEx SHALL extract:

- next‑turn context fields  
- stability hints  
- identity‑layer continuity  
- metadata continuity  

### **8.5 CE Behavior**  
CE SHALL represent:

- next‑turn context fields  
- continuity_status  
- stability_status  

### **8.6 ISc Behavior**  
ISc SHALL consume:

- next‑turn context fields  
- structural metadata  
- stability metadata  

### **8.7 TP Historical Continuity**  
TP SHALL record:

- CST signals  
- COB transformations  
- CIL packet structure  
- CEx extraction  
- CE representation  
- ISc consumption  

---

# **9. Additional Tests (New)**

### **9.1 Metadata Continuity Tests**  
Verify propagation of:

- alignment  
- identity shift  
- topic anchor  
- continuity record  
- intent record  

### **9.2 Provenance Continuity Tests**  
Verify propagation of:

- lineage_log[]  
- signature_history[]  
- entropy_history[]  

### **9.3 Next‑Turn Context Tests**  
Verify propagation of:

- topic  
- stance  
- intent  
- continuity  
- direction  
- coherence  
- importance  
- clarifying_fields[]  

### **9.4 Freeze/Thaw Continuity Tests**  
Verify:

- no instability on freeze/thaw  
- continuity preserved  
- metadata preserved  

### **9.5 Merge/Split Continuity Tests**  
Verify:

- no instability caused by merge/split  
- valid instability passes immediately  
- lineage continuity preserved  

### 9.6 Unified Merge/Split Pipeline Test (New)
The unified context testbench SHALL validate that CST‑Core detects MERGE/SPLIT events, CST‑MS preserves structural neutrality, CST‑Mux produces stable USP flags, COB evolves identity‑layer objects correctly under structural transitions, and CIL constructs an intake packet that reflects the correct post‑merge/post‑split identity‑layer topology. The test SHALL confirm that structural transitions do not produce false instability and that valid instability on unrelated objects is preserved.

### 9.7 - New Identity Context Boundary Tests
The unified context testbench SHALL validate that CST‑MS detects identity‑layer
context boundary breaks and emits the control signal `new_context_required=True`.
The testbench SHALL verify that CST‑Mux propagates this signal into the USP,
COB SHALL create a new identity‑layer object in the same turn, CIL SHALL
construct an intake packet using the new identity context, and CEx/CE/ISc SHALL
propagate continuity accordingly. The test SHALL confirm that context boundary
detection is present‑tense, deterministic, and SHALL NOT be delayed by Path A
validation.


---

# **10. High‑Level Requirements (HLRs)**  
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

### **HLR‑CnTxt‑021 — New Identity Context Boundary Detection and Propagation**
The unified context subsystem (CST‑Core, CST‑MS, CST‑Mux, COB, and CIL) SHALL detect identity‑layer context boundary breaks and SHALL propagate the control signal new_context_required deterministically across all stages of the pipeline. When new_context_required=True, COB SHALL create a new identity‑layer object in the same turn, CIL SHALL treat the turn as a new context boundary, and downstream components (CEx, CE, ISc) SHALL propagate continuity accordingly. Context boundary detection SHALL NOT be delayed by Path A validation and SHALL occur in the present turn.

### **HLR‑CnTxt‑020 — Unified Merge/Split Detection and Propagation**
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

# **11. Determinism Notes (Informative)**  
Deterministic replay ensures identical TPSnS inputs produce identical CST, COB, CIL, CEx, CE, and ISc outputs.

---

# **12. Interface Contracts (Informative)**

- CST → COB  
- CST → CIL  
- COB → CIL  
- CIL → CEx  
- CEx → CE  
- CE → ISc  
- Context → TP  

---

# **13. Error Handling (Informative)**  
Malformed identity‑layer objects, CST signals, or packet structures are rejected.

---

# **14. Simulation Notes (Informative)**  
This document defines the system_playground version of the unified context subsystem.

---
