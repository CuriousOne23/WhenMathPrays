# **iiinb_isc_tpu_ib_tb_arch_discussion.md**  
*(Architecture Discussion — Rough Draft)*

## **1. Purpose of This Document (Informative)**  
This document is a **scratchpad for architectural clarity**.  
It exists because several TS primitives (IIInB, ISc, TPU, IB, TB) have experienced **semantic drift**, **role confusion**, and **pipeline misplacement** across the 20‑series documents.

This file is **not normative**.  
It is a place to:

- describe the problems  
- identify contradictions  
- map the drift  
- clarify original intent  
- propose corrections  
- orchestrate the true flow of TS  

Once clarity is achieved here, the formal requirements documents (20.44, 20.46, 20.101, etc.) will be updated.

---

## **2. The Core Problem (What We Must Resolve)**

### **2.1. IB/TB were originally *post‑TS* primitives**  
Originally:

- **IB** interrogates unresolved meaning *after* TS has done its best.  
- **TB** judges/grounds IB’s questions.  
- **GBIB** governs IB/TB.  
- **GB** oversees the entire process.

They were **never** part of the input pipeline.

### **2.2. But the current 20‑series documents place TB on the *input* side**  
This creates a dangerous architectural contradiction:

- TB appears upstream of ISc  
- TB appears to generate candidate sets  
- TB appears to be part of semantic interpretation  
- TB appears to be part of the intake pipeline  

This is **not** what TB was designed to do.

### **2.3. TPU’s role has also drifted**  
TPU was originally:

> **The sole safe writer to TP.**

But 20.46 now implies:

- TPU is part of semantic flow  
- TPU is part of the pipeline  
- TPU interacts with TB  
- TPU does more than safe writes  

This is incorrect.

### **2.4. ISc’s input source is now unclear**  
ISc needs a **finite candidate_set{}**.  
But if TB is restored to its original role (truth validator), then:

- TB cannot produce candidate_set{}  
- IB cannot produce candidate_set{}  
- OB might produce it  
- Or a new primitive (SB) might be needed  
- Or TB must be split into two roles  

This is currently undefined.

### **2.5. The pipeline diagrams across documents are inconsistent**  
Some diagrams show:

```
InB → IIInB → RB → TB → ISc
```

Others imply:

```
TP → IB → TB → GBIB → GB
```

Others show:

```
ISc → Merge → TPU → TP
```

But none reconcile the **two different roles** TB plays in these diagrams.

### **2.6. The architecture is now ambiguous**  
We currently cannot answer cleanly:

- Who interprets input?  
- Who generates candidate_set{}?  
- Who validates truth?  
- Who interrogates unresolved meaning?  
- Who writes to TP?  
- Where do IB/TB belong?  
- Where does ISc sit relative to semantic interpretation?  

This ambiguity is dangerous because it affects:

- safe boundaries  
- replay invariants  
- writer authority  
- escalation  
- TP mutation rules  
- the entire 20‑series  

---

## **3. What Needs to Be Resolved (Explicit List)**

### **3.1. Placement of IB/TB**  
We must decide:

- Are IB/TB strictly post‑TS primitives?  
- Or do they have any role in the input pipeline?  
- If not, they must be removed from all input‑side diagrams.

### **3.2. Who produces candidate_set{} for ISc?**  
Options:

- IB  
- OB  
- a new primitive (SB)  
- TB‑Interpretation (if TB is split)  
- TB (if we accept the drift)

This must be resolved before 20.44 can be finalized.

### **3.3. TPU’s true role**  
We must restore or redefine:

- Is TPU *only* the safe writer?  
- Does TPU have any semantic responsibilities?  
- Does TPU appear in the pipeline diagrams?  
- How does TPU enforce the 1‑TP‑cycle lag?  

### **3.4. The correct pipeline(s)**  
We must define:

- The **core inference pipeline**  
- The **post‑TS interrogation pipeline**  
- The **semantic interpretation pipeline**  
- The **safe‑write pipeline**  

And ensure they do not conflict.

### **3.5. Primitive responsibilities**  
We must clarify:

- IIInB  
- RB  
- ISc  
- Merge  
- TPU  
- IB  
- TB  
- GBIB  
- GB  

Each must have a **single, clear, non‑overlapping role**.

### **3.6. Drift correction**  
We must identify:

- where drift occurred  
- why it occurred  
- how to correct it  
- which documents must be updated  

---

## **4. The Issues in Detail (Problem Description Before Solutions)**

### **4.1. TB is overloaded**  
TB currently appears to:

- validate truth  
- generate candidates  
- interpret input  
- sit upstream of ISc  
- sit downstream of TP  
- interact with TPU  
- interact with Merge  

This is impossible.

### **4.2. IB is misplaced**  
IB appears in some diagrams as:

- an intake‑side primitive  
- a post‑TS primitive  
- a semantic interpreter  
- a question generator  

This is contradictory.

### **4.3. TPU is mischaracterized**  
TPU is described as:

- a writer  
- a semantic processor  
- a pipeline stage  
- a validator  
- a transformer  

This is incorrect.

### **4.4. ISc’s input is undefined**  
ISc requires:

- a finite candidate set  
- structured interpretations  
- deterministic features  

But the architecture does not define who produces these.

### **4.5. The pipeline diagrams are inconsistent**  
Different documents show different flows.  
None match the original architecture.

### **4.6. Safe boundaries are unclear**  
If TB is upstream of ISc, then:

- TB becomes a semantic generator  
- TB becomes a meaning constructor  
- TB becomes a writer precursor  

This breaks 20.30 and 20.105.

### **4.7. Replay invariants are threatened**  
If TB or IB appear upstream of ISc, replay becomes ambiguous.

---

## **5. Architectural Invariant: InB as Path Selector**

InB is the **sole authority** that determines which processing path TS will take.  
This is a foundational invariant of the architecture.

InB examines the incoming envelope and decides:

- whether the input is **clean and resolvable**  
- whether the input is **ambiguous or malformed**  
- whether the input requires **semantic interpretation**  
- whether the input requires **user clarification**  
- whether the input requires **TS inference**  
- whether the input should bypass inference entirely  

This decision determines which of the three TS paths (plus the post‑TS path) is activated.

---

# **6. The Four Distinct Processing Paths**

TS has **four** non‑overlapping pipelines.  
They must never be merged in diagrams or requirements.

---

## **6.1 Normal Path (default, no ambiguity, no errors)**

This is the **happy path** — the system simply responds.

No IIInB.  
No ISc.  
No TPU.  
No scoring.  
No governance.  
No interrogation.

```
InB → OB → RB → Path B → OuB
```

This is the **default conversational path**.

---

## **6.2 Clarification Path (fallback when input is unclear)**

Triggered when **InB detects something it cannot resolve**:

- malformed  
- ambiguous  
- incomplete  
- contradictory  
- unknown  
- structurally invalid  

In this case, InB escalates to IIInB, which attempts to normalize.  
If normalization cannot resolve the issue, the system asks the user.

```
InB → IIInB → Path B → OuB → User
```

This is the **user clarification path**, not inference.

---

## **6.3 Inference Path (semantic scoring + TP update)**

Triggered only when:

- the input is valid  
- AND it requires semantic interpretation  
- AND TS must update TP  

This is the **semantic / scoring / TP‑update pipeline**:

```
InB → IIInB → ISc → TPU (Merge) → TP
```

Notes:

- **ISc** is the first semantic decision point.  
- **Merge** validates the update request.  
- **TPU** is the *only* safe writer to TP.  
- This path is **rare** compared to the normal path.

---

## **6.4 Post‑TS Interrogation Path (truth, grounding, governance)**

Triggered only when **TP itself is unclear** or when TS has exhausted its ability to resolve meaning.

This is the **truth‑checking / grounding / governance loop**:

```
TP → IB → TB → GBIB → GB
```

Notes:

- This path is **not** part of intake.  
- This path is **not** part of scoring.  
- This path is **not** part of TP writing.  
- This path is **after** TS has already done its best.

---

# **7. Why This Separation Matters**

This four‑path model:

- restores the original TS architecture  
- eliminates the drift that placed TB/IB upstream  
- clarifies TS vs GB responsibilities  
- prevents unsafe boundary violations  
- clarifies when ISc is used (rare)  
- clarifies when TPU is used (only for TP writes)  
- clarifies when IIInB is used (only for normalization or fallback)  
- clarifies that the normal path bypasses inference entirely  

This is the architecture that all 20‑series documents must align with.

---

# **8. Proposed Solution: Introducing CEx and CE to Stabilize Contextual Scoring**

Sections 1–7 describe the architectural drift and the core problem:  
**ISc requires contextual information to score interpretations correctly, but cannot safely read CIL or global state directly.**  
This creates tension between determinism, replayability, and the need for contextual awareness.

The solution is to introduce two new primitives:

- **CEx — ContextExtractor**  
- **CE — ContextEnvelope**

These two components allow TS to use CIL safely, without violating determinism, safe boundaries, or replay invariants.

---

## **8.1 ContextEnvelope (CE)**  
**CE is a bounded, deterministic, replayable context object** that contains only the minimal conversation context required for ISc to perform semantic scoring.

CE is **not** a history, log, or lineage record.  
CE is **not** a semantic object.  
CE is **not** a TP writer.

CE is a **snapshot** of relevant context at time *n*, extracted from CIL and shaped into a safe, finite structure.

**CE properties:**

- **Bounded** — finite size; no unbounded history  
- **Deterministic** — same inputs ⇒ same CE  
- **Replayable** — CE can be logged and reused for scoring  
- **Non‑semantic** — CE does not create new meaning  
- **Isolated** — CE shields ISc from global state  

**CE may include (playground schema):**

- active conversation objects  
- active referents  
- thread lineage identifiers  
- relevant USP entries  
- relevant MTP slices  
- relevant commitments or constraints  

This schema is intentionally minimal and can evolve.

---

# **8.2 ContextExtractor (CEx)**

CEx is the **bridge** between:

- the structured intake envelope produced by **IIInB**,  
- the global conversation state maintained by **CIL**, and  
- the bounded, deterministic **ContextEnvelope (CE)** consumed by **ISc**.

This relationship is captured in the following diagram:

```
IIInB ───► CEx ───► CE ───► ISc
           ▲
           │
          CIL   (reference only)
```

### **Interpretation of the diagram**

- **IIInB** produces a cleaned, structurally valid intake envelope.  
- **CEx** reads that envelope and consults **CIL** *as a reference service only*.  
- **CEx** extracts only the *relevant*, *bounded*, *deterministic* context and shapes it into **CE**.  
- **ISc** consumes **CE**, not CEx and not CIL.  
- **CIL** never becomes a pipeline stage; it is read‑only and tangential.

This is the minimal architecture that preserves determinism, replayability, and safe boundaries while still giving ISc the context it needs.

---

## **CEx responsibilities**

CEx is a **context‑shaping primitive**, not a semantic engine.  
Its responsibilities are:

1. **Read IIInB output**  
   - Accept the structured, repaired intake envelope.

2. **Consult CIL safely**  
   - Read MTP, COB, USP, lineage, active objects, and commitments.  
   - Never modify CIL.  
   - Never expose CIL directly to ISc.

3. **Select relevant context**  
   - Identify only the context needed for this turn.  
   - Ignore irrelevant or stale context.

4. **Bound the context**  
   - Enforce strict size and complexity limits.  
   - Ensure CE is finite and replayable.

5. **Produce CE deterministically**  
   - Same IIInB envelope + same CIL state ⇒ same CE.  
   - CE must be stable across replays.

6. **Isolate ISc from global state**  
   - CE is the *only* context object ISc may consume.  
   - ISc must never read CIL directly.

---

## **Why this works**

This design solves the core architectural tension described in Sections 1–7:

### **1. ISc gets the context it needs**  
ISc requires active objects, referents, commitments, lineage, and other contextual signals to score interpretations correctly.

CE provides exactly that — no more, no less.

### **2. ISc remains deterministic and replayable**  
CIL is global and unbounded.  
ISc cannot read it directly without breaking determinism.

CE is bounded and deterministic, so ISc remains stable.

### **3. CIL stays in its proper role**  
CIL is a **reference layer**, not a pipeline stage.  
CEx is the only primitive allowed to read it.

This preserves the integrity of 20.33.

### **4. IIInB stays focused on repair**  
IIInB does short‑term repair only.  
It does not read CIL.  
It does not extract context.

This preserves the integrity of 20.101.

### **5. Long‑term repair becomes possible but safe**  
If long‑term repair is retained, it can use CE (not CIL) to perform deeper corrections without violating safe boundaries.

### **6. The entire TS architecture stabilizes**  
- No global state leaks into scoring  
- No unsafe context reaches ISc  
- No drift of TB/IB upstream  
- No violation of safe boundaries  
- No replay failures  
- No semantic contamination  

This is the minimal, clean, and stable solution.

---

## **8.3 Updated Pipeline with CEx and CE**

### **Normal Path (unchanged)**  

```
InB → OB → RB → Path B → OuB
```

### **Short‑Term Repair Path (unchanged)**  

```
InB → IIInB → Path B → OuB → User
```

### **Inference Path (updated)**  

```
InB → IIInB → CEx → CE → ISc → Merge → TPU → TP
```

### **Long‑Term Repair Path (optional)**  
If long‑term repair is retained:

```
InB → IIInB → CEx → CE → LongTermRepair → ISc → Merge → TPU → TP
```

### **Post‑TS Interrogation Path (unchanged)**  

```
TP → IB → TB → GBIB → GB
```

This preserves the original architecture while adding the missing contextual bridge.

---

## **8.4 Why This Works**

### **1. It protects ISc from global state**  
ISc must remain deterministic, bounded, and replayable.  
CIL is global, unbounded, and dynamic.  
CE is the safe middle layer.

### **2. It restores architectural purity**  
- IIInB handles repair  
- CEx handles context extraction  
- ISc handles scoring  
- TPU handles writing  
- CIL remains a reference layer  
- IB/TB remain post‑TS governance  

No primitive is overloaded.

### **3. It cleanly separates short‑term and long‑term repair**  
- Short‑term repair stays in IIInB  
- Long‑term repair (if kept) uses CE  
- Neither repair path touches CIL directly  

### **4. It aligns with 20.33 (CIL) and 20.101 (IIInB)**  
- CIL remains a reference layer  
- IIInB remains a repair primitive  
- Neither is misused  
- CEx becomes the correct bridge  

### **5. It stabilizes the entire TS architecture**  
- No global state leaks into scoring  
- No unsafe context reaches ISc  
- No drift of TB/IB upstream  
- No violation of safe boundaries  
- No replay failures  
- No semantic contamination  

This is the minimal, clean, and stable solution.

---

