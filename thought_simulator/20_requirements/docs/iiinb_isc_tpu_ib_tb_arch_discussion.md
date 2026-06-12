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

## **Why this works**

### **1. It preserves determinism and replayability**  
ISc must be deterministic.  
CIL is global and unbounded.  
CEx converts global state into a **bounded CE**, ensuring ISc remains stable.

### **2. It restores architectural purity**  
Each primitive returns to its intended role:

- **IIInB** = repair  
- **CEx** = context extraction  
- **CE** = bounded context  
- **ISc** = semantic scoring  
- **Merge** = validation  
- **TPU** = writing  
- **CIL** = reference only  

No primitive is overloaded.

### **3. It cleanly separates short‑term and long‑term repair**  
- Short‑term repair stays in IIInB.  
- Long‑term repair (if retained) uses CE, not CIL.  
- Neither repair path touches global state directly.

### **4. It aligns with 20.33 (CIL) and 20.101 (IIInB)**  
- CIL remains a reference layer.  
- IIInB does not read CIL.  
- CEx becomes the correct bridge.  
- ISc remains isolated from global state.

### **5. It stabilizes the entire TS architecture**  
- No global state leaks into scoring  
- No unsafe context reaches ISc  
- No drift of TB/IB upstream  
- No violation of safe boundaries  
- No replay failures  
- No semantic contamination  

This is the minimal, clean, and stable solution that resolves the architectural tension described in Sections 1–7.

---

# **8.4 Why This Architecture Works**

The updated inference architecture succeeds because it resolves the core tension identified in Sections 1–7:  
**ISc requires contextual information to score interpretations correctly, but cannot safely read global state (CIL) directly.**

The introduction of **CEx** and **CE** provides the minimal, stable, and safe bridge needed to support context‑aware scoring without violating determinism or safe boundaries.

---

## **1. CEx isolates ISc from global state**

CIL contains:

- MTP  
- COB  
- USP  
- lineage  
- active objects  
- commitments  

These structures are **global, unbounded, and dynamic**.

ISc must remain:

- deterministic  
- bounded  
- replayable  
- safe  

CEx is the **only** primitive allowed to read CIL, and it produces a **bounded CE** that ISc can safely consume.

This prevents global state from leaking into scoring.

---

## **2. CE provides exactly the context ISc needs — no more, no less**

CE is a **bounded, deterministic snapshot** of the relevant conversation context at time *n*.

It contains only what ISc needs:

- active referents  
- active objects  
- relevant USP entries  
- relevant MTP slices  
- lineage identifiers  
- commitments or constraints  

CE is:

- finite  
- replayable  
- stable  
- non‑semantic  

This ensures ISc receives the right context without inheriting global complexity.

---

## **3. IIInB stays focused on repair, not context integration**

IIInB performs:

- short‑term repair  
- structural normalization  
- envelope cleanup  

IIInB does **not**:

- read CIL  
- extract context  
- perform semantic interpretation  

This preserves the intent of 20.101 and prevents IIInB from becoming overloaded.

---

## **4. CIL remains a reference layer, not a pipeline stage**

CIL is consulted by CEx, but never appears in the pipeline.

This preserves the intent of 20.33:

- CIL is global  
- CIL is read‑only  
- CIL is not part of intake  
- CIL is not part of scoring  
- CIL is not part of repair  

CEx is the correct bridge.

---

## **5. TPU remains the only writer to TP**

The updated pipeline:

```
IIInB → CEx → CE → ISc → Merge → TPU → TP
```

ensures that:

- ISc never writes  
- CEx never writes  
- CE never writes  
- IIInB never writes  
- only TPU writes to TP  

This preserves safe boundaries and prevents semantic contamination.

---

## **6. Long‑term repair becomes possible but safe**

If long‑term repair is retained, it can use **CE**, not CIL, to perform deeper corrections.

This allows:

- context‑aware repair  
- without global‑state access  
- without violating determinism  
- without contaminating ISc  

This is the cleanest way to support both short‑term and long‑term repair.

---

## **7. The entire TS architecture stabilizes**

This architecture:

- prevents drift  
- prevents unsafe boundary violations  
- prevents TB/IB from drifting upstream  
- prevents global state from leaking into scoring  
- preserves determinism and replayability  
- restores the original TS design intent  

It is the minimal, correct, and stable solution.

---

# **9. Efficiency, Implementability, and Cost Profile of the Proposed Architecture**

The introduction of **CEx** and **CE** not only resolves the architectural tension described in Sections 1–7, but also produces a design that is **clean, CPU‑friendly, implementable, and low‑cost**.  
This section explains why the proposed solution is practical and efficient in real systems.

---

## **9.1 Clean Separation of Responsibilities**

Each primitive now has a single, crisp responsibility:

- **IIInB** — short‑term repair  
- **CEx** — context extraction  
- **CE** — bounded context object  
- **ISc** — semantic scoring  
- **Merge** — semantic validation  
- **TPU** — TP writing  
- **CIL** — reference layer  

No primitive is overloaded.  
No primitive leaks into another’s domain.  
No circular dependencies exist.

This yields a clean, maintainable architecture.

---

## **9.2 CPU‑Friendly by Design**

The new architecture is computationally light:

- **CEx** performs only selection, bounding, and shaping — no heavy logic.  
- **CE** is intentionally small and finite.  
- **ISc** receives only a cleaned envelope and a small CE.  
- **CIL** is consulted once per turn, by one primitive.  
- **No global scans**, no recursion, no backtracking.

This keeps per‑turn compute extremely low.

---

## **9.3 Highly Implementable**

The primitives map directly to real software components:

- IIInB → parser/normalizer  
- CEx → context selector  
- CE → struct/record  
- ISc → scoring function  
- TPU → state writer  
- CIL → global context store  

There is no exotic machinery.  
No complex data structures.  
No nondeterministic behavior.

This architecture can be implemented in any mainstream language (Rust, Go, C++, Python, Java, TypeScript) with minimal overhead.

---

## **9.4 Low‑Cost to Operate**

The architecture avoids:

- GPUs  
- embeddings  
- matrix operations  
- large memory allocations  
- deep history traversal  
- expensive graph operations  

CEx is O(1) or O(n) with tiny n.  
CE is tiny.  
ISc is bounded.  
TPU writes are small.

This makes the system inexpensive to run at scale.

---

## **9.5 Stability and Predictability**

Because CE is deterministic and bounded:

- ISc remains deterministic  
- replay remains valid  
- safe boundaries remain intact  
- TP updates remain predictable  
- governance remains enforceable  

This stability is essential for TS.

---

# **10. Implications for 20.33 (CIL) and 20.101 (IIInB)**

The introduction of **CEx** and **CE** clarifies and strengthens the requirements in 20.33 and 20.101.  
This section summarizes the implications for both documents.

---

## **10.1 Implications for 20.33 — CIL Requirements**

The proposed architecture reinforces the intended role of CIL:

### **CIL remains a reference layer, not a pipeline stage**

- CIL is **never** part of the intake pipeline.  
- CIL is **never** part of the scoring pipeline.  
- CIL is **never** part of repair.  
- CIL is **never** part of TP writing.  
- CIL is **never** part of governance.

### **CEx becomes the only primitive allowed to read CIL**

This ensures:

- controlled access  
- bounded extraction  
- deterministic shaping  
- no global state leakage into ISc  

### **CIL’s responsibilities remain unchanged**

CIL continues to maintain:

- MTP  
- COB  
- USP  
- lineage  
- active objects  
- commitments  

But now these structures are consumed safely through CE.

---

## **10.2 Implications for 20.101 — IIInB Requirements**

The proposed architecture restores IIInB to its intended role:

### **IIInB performs short‑term repair only**

IIInB:

- cleans malformed input  
- normalizes structure  
- resolves local shorthand  
- prepares the envelope for downstream processing  

IIInB does **not**:

- read CIL  
- extract context  
- perform semantic interpretation  
- perform long‑term repair  
- influence scoring directly  

### **IIInB hands off to CEx for context extraction**

This ensures:

- IIInB stays lightweight  
- IIInB stays deterministic  
- IIInB stays bounded  
- IIInB does not drift into semantic or contextual responsibilities  

### **Long‑term repair (if retained) uses CE, not CIL**

This keeps long‑term repair safe and bounded.

---

## **10.3 System‑Wide Implications**

The architecture:

- prevents drift  
- prevents unsafe boundary violations  
- prevents TB/IB from drifting upstream  
- prevents global state from leaking into scoring  
- preserves determinism and replayability  
- restores the original TS design intent  

This is the minimal, correct, and stable solution.

---
