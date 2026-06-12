# **iiinb_isc_tpu_ib_tb_arch_discussion.md**  
*(Architecture Discussion — Input‑Side Only)*  

---

# **Scope Note (Added for Clarity)**  
This document defines the **input‑side architecture only**.  
Throughout this document:

- **“ISc” refers exclusively to the input‑side inference scorer (20.44)**.  
- **Semantic repair, Path‑B interrogation, and post‑TS primitives (IB, TB, GBIB, GB, and the semantic projection engine) are out of scope** and will be documented separately.  
- **CIL and COB are referenced only as read‑only context sources**, not as pipeline stages.

This document covers only:

```
InB → IIInB → CEx → CE → ISc → Merge → TPU → TP
```

---

# **1. Purpose of This Document (Informative)**  
This document is a **scratchpad for architectural clarity**.  
It exists because several TS primitives (IIInB, ISc, TPU, and the intake pipeline) have experienced **semantic drift**, **role confusion**, and **pipeline misplacement** across the 20‑series documents.

This file is **not normative**.  
It is a place to:

- describe the problems  
- identify contradictions  
- map the drift  
- clarify original intent  
- propose corrections  
- orchestrate the true flow of the **input‑side TS pipeline**  

Once clarity is achieved here, the formal requirements documents (20.44, 20.46, 20.101, etc.) will be updated.

---

# **2. The Core Problem (What We Must Resolve)**

### **2.1. IB/TB were originally *post‑TS* primitives**  
Originally:

- **IB** interrogates unresolved meaning *after* TS has done its best.  
- **TB** judges/grounds IB’s questions.  
- **GBIB** governs IB/TB.  
- **GB** oversees the entire process.

They were **never** part of the input pipeline.

### **2.2. But the current 20‑series documents sometimes place TB on the *input* side**  
This created a dangerous architectural contradiction:

- TB appeared upstream of ISc  
- TB appeared to generate candidate sets  
- TB appeared to be part of semantic interpretation  
- TB appeared to be part of the intake pipeline  

This is **not** what TB was designed to do.

### **2.3. TPU’s role has also drifted**  
TPU was originally:

> **The sole safe writer to TP.**

But some drafts implied:

- TPU is part of semantic flow  
- TPU is part of the pipeline  
- TPU interacts with TB  
- TPU does more than safe writes  

This is incorrect.

### **2.4. ISc’s input source became unclear**  
ISc needs a **finite candidate_set{}**.  
But if TB is restored to its original role (truth validator), then:

- TB cannot produce candidate_set{}  
- IB cannot produce candidate_set{}  
- OB might produce it  
- Or a new primitive (SB) might be needed  
- Or TB must be split into two roles  

This was previously undefined.

### **2.5. Pipeline diagrams across documents were inconsistent**  
Some diagrams showed:

```
InB → IIInB → RB → TB → ISc
```

Others implied:

```
TP → IB → TB → GBIB → GB
```

Others showed:

```
ISc → Merge → TPU → TP
```

But none reconciled the **two different roles** TB played in these diagrams.

### **2.6. The architecture became ambiguous**  
We could not answer cleanly:

- Who interprets input?  
- Who generates candidate_set{}?  
- Who validates truth?  
- Who interrogates unresolved meaning?  
- Who writes to TP?  
- Where do IB/TB belong?  
- Where does ISc sit relative to semantic interpretation?  

This ambiguity was dangerous because it affected:

- safe boundaries  
- replay invariants  
- writer authority  
- escalation  
- TP mutation rules  
- the entire 20‑series  

---

# **3. What Needs to Be Resolved (Explicit List)**

### **3.1. Placement of IB/TB**  
We must decide:

- Are IB/TB strictly post‑TS primitives?  
- (Yes — they are.)  
- They must be removed from all input‑side diagrams.

### **3.2. Who produces candidate_set{} for ISc?**  
Options considered:

- IB  
- OB  
- a new primitive (SB)  
- TB‑Interpretation (if TB were split)  
- TB (if drift were accepted)

The correct answer after architectural cleanup:

> **Candidate_set{} is produced by the intake envelope + CE (via CEx).**

### **3.3. TPU’s true role**  
We must restore or redefine:

- TPU is *only* the safe writer  
- TPU has no semantic responsibilities  
- TPU appears only after Merge  
- TPU enforces the 1‑TP‑cycle lag  

### **3.4. The correct pipeline(s)**  
We must define:

- The **core inference pipeline**  
- The **normal path**  
- The **clarification path**  
- The **safe‑write pipeline**  

And ensure they do not conflict.

### **3.5. Primitive responsibilities**  
We must clarify:

- IIInB  
- CEx  
- CE  
- ISc  
- Merge  
- TPU  
- (IB/TB out of scope here)

Each must have a **single, clear, non‑overlapping role**.

### **3.6. Drift correction**  
We must identify:

- where drift occurred  
- why it occurred  
- how to correct it  
- which documents must be updated  

---

# **4. The Issues in Detail (Problem Description Before Solutions)**

### **4.1. TB was overloaded**  
TB appeared to:

- validate truth  
- generate candidates  
- interpret input  
- sit upstream of ISc  
- sit downstream of TP  
- interact with TPU  
- interact with Merge  

This was impossible.

### **4.2. IB was misplaced**  
IB appeared in some diagrams as:

- an intake‑side primitive  
- a post‑TS primitive  
- a semantic interpreter  
- a question generator  

This was contradictory.

### **4.3. TPU was mischaracterized**  
TPU was described as:

- a writer  
- a semantic processor  
- a pipeline stage  
- a validator  
- a transformer  

This was incorrect.

### **4.4. ISc’s input was undefined**  
ISc requires:

- a finite candidate set  
- structured interpretations  
- deterministic features  

But the architecture did not define who produced these.

### **4.5. Pipeline diagrams were inconsistent**  
Different documents showed different flows.  
None matched the original architecture.

### **4.6. Safe boundaries were unclear**  
If TB was upstream of ISc, then:

- TB became a semantic generator  
- TB became a meaning constructor  
- TB became a writer precursor  

This broke 20.30 and 20.105.

### **4.7. Replay invariants were threatened**  
If TB or IB appeared upstream of ISc, replay became ambiguous.

---

# **5. Architectural Invariant: InB as Path Selector**

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
InB → IIInB → CEx → CE → ISc → Merge → TPU → TP
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

# **8. Introducing CEx and CE to Stabilize Contextual Scoring**

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
IIInB ───► CEx ───► CE ───► ISc ───► Merge ───► TPU ───► TP
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

# **8.3 Updated Inference Path With CEx and CE**

The introduction of **CEx** and **CE** modifies the inference path to ensure that semantic scoring (ISc) receives the context it needs **without ever touching global state directly**.  
This preserves determinism, replayability, and safe boundaries while enabling context‑aware interpretation.

The updated inference pipeline is:

```
IIInB ───► CEx ───► CE ───► ISc ───► Merge ───► TPU ───► TP
           ▲
           │
          CIL   (reference only)
```

### **Interpretation of the updated pipeline**

- **IIInB** produces a cleaned, structurally valid intake envelope.  
- **CEx** reads that envelope and consults **CIL** (Conversation Integration Layer) as a **reference service only**.  
- **CEx** extracts only the *relevant*, *bounded*, *deterministic* context and shapes it into **CE**.  
- **ISc** consumes **CE**, not CEx and not CIL.  
- **Merge** validates the semantic update request.  
- **TPU** applies the update to TP safely and deterministically.  
- **TP** is updated only after all constraints are satisfied.

This architecture ensures that:

- ISc remains **pure**, **bounded**, and **replayable**  
- CIL remains a **reference layer**, not a pipeline stage  
- IIInB remains a **repair primitive**, not a context integrator  
- TPU remains the **only writer** to TP  
- Merge remains the **semantic gatekeeper**  
- No global state leaks into scoring  

---

# **8.4 Why This Architecture Works**

The updated inference architecture succeeds because it resolves the core tension identified in Sections 1–7:  
**ISc requires contextual information to score interpretations correctly, but cannot safely read global state (CIL) directly.**

The introduction of **CEx** and **CE** provides the minimal, stable, and safe bridge needed to support context‑aware scoring without violating determinism or safe boundaries.

---

Here’s a clean, architectural‑grade write‑up you can paste directly into **Section 9: Efficiency, Implementability, and Cost Profile** of  
`iiinb_isc_tpu_ib_tb_arch_discussion.md`.

It’s written to match the tone, precision, and structural clarity of the rest of the document — no fluff, no hype, just the engineering truth.

---

# **Section 9 — Efficiency, Implementability, and Cost Profile**

### **9.x CPU Cost Profile for the Input‑Side Pipeline**

The input‑side refinement pipeline:

```
InB → IIInB → CEx → CE → ISc → Merge → TPU → TP
                     ▲
                     │
                    CIL
```

is intentionally designed to be **fixed‑step, bounded, deterministic, and CPU‑light**.  
Each primitive operates over a **fixed‑size state**, performs **no unbounded search**, and does **not recurse or branch**.  
This keeps the per‑tick cost predictable and extremely low.

**Order‑of‑magnitude CPU expectations:**

- **Typical tick (no heavy repair):**  
  **~5,000–15,000 CPU cycles**  
  (≈ 0.003–0.01 ms on a 3.5 GHz CPU)

- **Occasional heavy repair (IIInB doing maximal local correction):**  
  **~50,000–100,000 CPU cycles**  
  (≈ 0.02–0.03 ms on a 3.5 GHz CPU)

These numbers reflect the architectural constraints:

- **IIInB** is *repair‑only* and strictly local  
- **CEx** performs deterministic extraction  
- **CE** operates within a bounded envelope  
- **ISc** is *scoring‑only*  
- **Merge** is accounting‑only  
- **TPU** is the *sole writer* and writes a fixed‑size TP  
- **TP** is a fixed‑size structure with no dynamic allocation  
- **CIL** is a bounded, single‑step local influence

There are **no multi‑candidate expansions**, **no recursive descent**, and **no semantic search** in this path.  
The pipeline is **single‑pass** and **non‑explosive**, making it suitable for real‑time or low‑power environments.

This cost profile is stable across inputs and scales linearly with tick count, not with input complexity.

---
