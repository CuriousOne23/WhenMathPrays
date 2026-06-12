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
Absolutely, Jeff — here is the **clean, updated section** you asked for, ready to paste directly into your open GitHub editor tab  
(**iiinb_isc_tpu_ib_tb_arch_discussion.md**, tabId **1146962434**).

I’m giving you **only the text**, no tools, no formatting surprises — just the exact architectural update you requested.

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

# **8. Next Steps**
