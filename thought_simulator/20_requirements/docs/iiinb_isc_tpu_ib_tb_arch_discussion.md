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

## **5. Proposed Solution (After Problem Description)**

### **5.1. Restore IB/TB to their original role**  
They belong **after TP**, not before.

```
TP → IB → TB → GBIB → GB
```

They are **post‑TS interrogation primitives**, not intake primitives.

### **5.2. Remove TB from the input pipeline**  
The correct input pipeline becomes:

```
InB → IIInB → RB → (semantic interpreter) → ISc → Merge → TPU → TP
```

### **5.3. Introduce or identify the true semantic interpreter**  
We must choose one:

- OB  
- a new primitive (SB)  
- TB‑Interpretation (split TB)  
- or another name  

This primitive produces:

- candidate_set{}  
- structured interpretations  
- features for ISc  

### **5.4. Restore TPU to its original purpose**  
TPU is:

> **The sole safe writer to TP.**

Nothing more.

### **5.5. Redraw the architecture**  
We will produce:

- a corrected core inference diagram  
- a corrected post‑TS interrogation diagram  
- a corrected safe‑write diagram  
- a corrected semantic interpretation diagram  

### **5.6. Update the 20‑series documents**  
Once this discussion stabilizes, we will update:

- 20.44 (ISc)  
- 20.46 (TPU)  
- 20.101 (IIInB)  
- ts_inference.md  
- 20.30 (safe boundaries)  
- 20.105 (writer authority)  

---

## **6. Next Steps**  
We must now answer the key architectural question:

# **Who produces the candidate_set{} for ISc?**

Once we answer that, the entire architecture locks into place.

---
