# **path_a_questions_for_context_substr.md**  
### *Path A Questions for Context Substrate — Working Paper v0.8*

---

## **0. Purpose**
This living working paper collects and organizes all critical questions we must answer before COB, CIL, CST, CEx, and SSRGn can be properly specified and implemented.  
We will grow the questions until they saturate and stabilize. Only then will we begin closing them and extracting answers into dedicated requirement documents.

---

## **1. Why These Questions Matter**
The conversation‑layer primitives depend on a stable Path A substrate.  
Underspecification here risks identity wobble, unreliable drift detection, inconsistent merging, non‑deterministic extraction, and broken replay safety.   [Current page](citation-section://1146974076/9)

---

## **2. Open Questions About Path A Output**

### **Envelope Schema & Stability**
- What is the exact schema of the Intake Envelope (IE)?   [Current page](citation-section://1146974076/10)  
- Which fields are required vs. optional?  
- How are structural tokens and referent candidates formally represented (schema, ordering, ambiguity)?   [Current page](citation-section://1146974076/11)  
- What metadata must be guaranteed stable across turns?   [Current page](citation-section://1146974076/12)  

### **Deterministic Replay**
- What parts of the envelope and TP metadata must be bit‑for‑bit deterministic?   [Current page](citation-section://1146974076/13)  
- How are envelope IDs and lineage markers generated and stabilized?   [Current page](citation-section://1146974076/14)  
- How do repairs, defects, and referent candidates maintain canonical ordering under replay?   [Current page](citation-section://1146974076/15)  

### **Referent Candidates & Structural Tokens**
- What qualifies as a referent candidate (surface‑form only, multi‑word, typed, ambiguous)?   [Current page](citation-section://1146974076/16)  
- How are structural tokens represented for malformed, nested, or complex input?   [Current page](citation-section://1146974076/17)  

---

## **3. Open Questions About COB**

### **Identity Layer Model**
- Exact schema of an identity layer and its referent map?   [Current page](citation-section://1146974076/18)  
- Fixed 20 slots or dynamic with a hard cap?   [Current page](citation-section://1146974076/19)  
- How is lineage represented (tree, DAG, linked list, versioned history)?   [Current page](citation-section://1146974076/20)  
- How is referent strength, confidence, or importance represented?   [Current page](citation-section://1146974076/21)  

### **Update & Lifecycle Mechanics**
- How does COB ingest and merge new SSRGn meaning?   [Current page](citation-section://1146974076/22)  
- Rules for conflict resolution between new meaning and existing layers?   [Current page](citation-section://1146974076/23)  
- Layer creation, splitting, merging, weakening, retirement, and aging/decay policy?   [Current page](citation-section://1146974076/24)  
- What happens when all 20 layers are occupied or when a new distinct identity appears?   [Current page](citation-section://1146974076/25)  

### **Determinism & Safety**
- How is the full COB state replayed deterministically from the SSRGn sequence?   [Current page](citation-section://1146974076/26)  
- How are layer IDs and snapshots versioned for auditability?  

---

## **4. Open Questions About CST**

### **Detection**
- Exact quantitative metrics for drift, oscillation, and collapse (layer churn, referent volatility, usage entropy)?   [Current page](citation-section://1146974076/27)  
- Time windows (short, medium, long‑term) and triggering thresholds?   [Current page](citation-section://1146974076/28)  

### **Signals & Protocol**
- Complete set of correction signals and their parameters (strength, justification, target)?   [Current page](citation-section://1146974076/29)  
- Prioritization and batching when multiple signals fire?  
- Synchronous or asynchronous with COB? Frozen snapshot or live view?   [Current page](citation-section://1146974076/30)  
- How does COB acknowledge, apply, or reject signals?   [Current page](citation-section://1146974076/31)  

### **Safety & Determinism**
- Safeguards to prevent over‑correction or inducing new oscillation?   [Current page](citation-section://1146974076/32)  
- Full replay safety for CST decisions and signals?  

---

## **5. Open Questions About CIL**

### **Merge Logic**
- Precise rules for merging short‑term TP/IE cues with COB snapshot?   [Current page](citation-section://1146974076/33)  
- Handling of conflicting, partial, or low‑certainty information?   [Current page](citation-section://1146974076/34)  

### **Flag Generation**
- Rules and algorithms for certainty flags, field‑importance hints, and ambiguity flags?   [Current page](citation-section://1146974076/35)  
- How are flags computed and represented in the intake packet?   [Current page](citation-section://1146974076/36)  

### **Determinism**
- How does CIL guarantee stable output under replay?   [Current page](citation-section://1146974076/37)  

---

## **6. Open Questions About CEx & SSRGn**

### **CEx**
- Exact extraction allowlist, rules, and interpretation of structural tokens / CIL flags?   [Current page](citation-section://1146974076/38)  
- Replay stability guarantees?  

### **SSRGn**
- Exact handoff protocol from OuBA → SSRGn → conversation layer (COB/CST/CIL)?   [Current page](citation-section://1146974076/39)  
- Which fields are frozen vs. transformed or filtered?   [Current page](citation-section://1146974076/40)  

---

## **7. Cross‑Cutting / Highest‑Risk Questions**

### **Timing & Ordering**
- Exact sequence and state visibility: SSRGn → COB → CST → CIL → CEx?   [Current page](citation-section://1146974076/41)  
- Does CIL read pre‑ or post‑CST COB state?  

### **Replay, Auditability & Invariants**
- How are all state changes, signals, and snapshots logged for deterministic replay?   [Current page](citation-section://1146974076/42)  
- Global invariants that must hold to prevent identity wobble or conversational collapse?   [Current page](citation-section://1146974076/43)  

### **A/B Boundary & Path B Integration**
- How do these primitives interact with Path B (e.g., CoHI) without breaking the A/B boundary?   [Current page](citation-section://1146974076/44)  
- What data flows from conversation layer back into Path B?   [Current page](citation-section://1146974076/45)  

### **Error Handling & Collapse Prevention**
- What conditions cause conversational collapse or identity instability?   [Current page](citation-section://1146974076/46)  
- Emergency safeguards or recovery mechanisms?  

---

## **8. NEW: Ambiguity Handling (Critical for COB + CIL)**

- How is ambiguity represented in referent candidates?  
- Do we track multiple competing referents for the same surface form?  
- How does COB store ambiguous identity layers?  
- How does CIL merge ambiguous short‑term cues with stable long‑term identity?  
- How does CST detect “ambiguity drift” vs. “identity drift”?  
- How does CEx extract fields when referents are ambiguous?  

---

## **9. NEW: Multi‑Turn Memory Horizon**

- How many turns does COB consider “recent”?  
- How far back does CST look when measuring drift?  
- How does CIL decide which historical cues matter?  
- How does CEx handle extraction when context spans many turns?  
- How does SSRGn regenerate meaning across long horizons?  

---

## **10. NEW: Strength, Confidence, and Importance Scores**

- What is the numeric range for referent strength?  
- How is confidence computed?  
- How is importance computed?  
- How do these scores decay over time?  
- How do these scores interact with CST signals?  
- How do these scores affect CIL merging?  
- How do these scores affect CEx extraction?  

---

## **11. NEW: Conflict Resolution**

- How does COB resolve conflicting referents?  
- How does CIL resolve conflicting short‑term cues?  
- How does CST resolve conflicting drift signals?  
- How does CEx resolve conflicting extraction candidates?  
- How does SSRGn resolve conflicting semantic structures?  

---

## **12. NEW: Error States and Recovery**

- What constitutes an “identity collapse”?  
- What constitutes a “referent collapse”?  
- What constitutes a “structure collapse”?  
- What constitutes a “continuity collapse”?  
- What emergency signals exist?  
- How do COB, CST, CIL, and CEx recover from collapse?  

---

## **13. NEW: Cross‑Boundary Contamination (Path A ↔ Path B)**

- What data is allowed to cross from Path A to Path B?  
- What data is forbidden?  
- How does COB interact with CoHI?  
- How does CST interact with Path B stability metrics?  
- How does CIL interact with Path B meaning construction?  
- How does CEx interact with Path B extraction rules?  
- How does SSRGn interact with Path B regeneration rules?  

---

## **14. Emerging / Secondary Questions**
(Added as we discover them — currently empty or low‑priority; we will grow this section.)   [Current page](citation-section://1146974076/47)

---

## **15. Next Steps**
- Continue expanding questions as new gaps surface.   [Current page](citation-section://1146974076/49)  
- When a cluster stabilizes, extract it into a dedicated requirements paper.  
- Shrink this working paper over time.   [Current page](citation-section://1146974076/50)  

---
