# **idob_conv_id_envelope.md**  
### *Conversational Identity Envelope — Definition, Dynamics, and Role in IdOB Meaning Resolution*

---

## **1. Purpose**

The **Conversational Identity Envelope (CIE)** is IdOB’s internal representation of identity‑conditioned meaning **within the conversation**.  
It is the mechanism that allows IdOB to:

- interpret meaning in conversational context,  
- modulate meaning based on conversational identity cues,  
- refine meaning across cycles,  
- stabilize meaning_delta_h,  
- influence meaning group ranking,  
- support replay‑safe convergence,  
- integrate identity metadata from PT1,  
- produce identity‑aware meaning semantics for OuBA.

The CIE is **not**:

- the user’s identity,  
- the speaker’s persona,  
- a long‑term memory identity,  
- a global identity model.

It is strictly:

> **the identity state of the utterance inside the conversation.**

---

## **2. Why Conversational Identity Exists**

Meaning is not purely structural.  
Two utterances with identical structural geometry may require **different meaning interpretations** depending on conversational identity.

Examples:

- “burst” → physical explosion vs. emotional outburst  
- “rock” → object vs. music vs. metaphor  
- “chew” → physical action vs. “chew over” (reflect)  
- “sleepy” → biological state vs. metaphorical dullness  

These differences arise from:

- conversational stance,  
- conversational cues,  
- conversational roles,  
- conversational identity pressure.

The CIE provides the **semantic context** needed to resolve these differences.

---

## **3. Inputs to the Conversational Identity Envelope**

The CIE begins with identity metadata from PT1:

```yaml
identity_metadata:
  identity_tags: [<string>, ...]
  identity_vector: [<int>, ...]
```

These come from:

- routing_signature  
- residue analysis  
- lexical identity anchors  
- meaning group identity anchors  
- conversational cues  
- conversational stance  
- conversational identity roles  

The CIE is then **refined** by IdOB across cycles.

---

## **4. Conversational Identity Envelope Structure**

The CIE is represented in `idob_object.yaml` as:

```yaml
identity_envelope:
  identity_importance: <float>
  identity_tags: [<string>, ...]
  identity_vector: [<int>, ...]
  identity_delta: <float>

  stabilization:
    identity_stable: <true|false>
    cycles: <int>
```

### **Fields Explained**

#### **identity_importance**
A scalar representing how strongly conversational identity influences meaning.

#### **identity_tags**
Semantic tags extracted from conversational context.

Examples:

- “scientific”  
- “physical”  
- “social”  
- “temporal”  
- “biological”  

#### **identity_vector**
A numeric vector representing conversational identity anchors.

Derived from:

- meaning group identity anchors  
- lexical identity anchors  
- routing signatures  
- residue hashes  
- conversational cues  

#### **identity_delta**
Measures change in conversational identity across cycles.

$$
\Delta h_{\text{identity}} = \| I_{i} - I_{i-1} \|
$$

#### **stabilization.identity_stable**
True when:

$$
|\Delta h_{\text{identity}}| < \varepsilon_{\text{identity}}
$$

---

## **5. Conversational Identity Dynamics Across IdOB Cycles**

### **Cycle 0 — Initialization**
CIE is seeded with PT1 identity metadata.

### **Cycle 1 — Coarse Tier**
CIE influences meaning group ranking.

### **Cycle 2 — Medium Tier**
CIE modulates meaning dimensions.

### **Cycle 3 — Fine Tier**
CIE helps select the final meaning group.

### **Cycle 4–5 — Refinement**
CIE is updated based on:

- meaning_semantics[]  
- meaning dimensions  
- meaning invariants  
- meaning cues  
- meaning triggers/suppressors  
- conversational identity pressure  

### **Cycle 6 — Stabilization**
CIE stabilizes when identity_delta < threshold.

---

## **6. How Conversational Identity Influences Meaning Resolution**

### **6.1 Meaning Group Ranking**

CIE modifies ranking of meaning_group_candidates:

- boosts groups aligned with conversational identity tags  
- suppresses groups misaligned with conversational identity  
- adjusts ranking weights (identity_weight)  

Example:

If conversational identity tags include “scientific”:

- materiality ↑  
- physicality ↑  
- sociality ↓  

This shifts meaning group selection.

---

### **6.2 Meaning Semantics Modulation**

CIE modulates meaning_semantics[]:

$$
M' = M + \alpha \cdot I
$$

Where:

- $M$ = meaning_semantics[]  
- $I$ = identity_vector  
- $\alpha$ = identity_importance  

This produces **identity‑conditioned meaning**.

---

### **6.3 Meaning Stabilization**

CIE contributes to stabilization:

- meaning stabilizes when meaning_delta_h < ε  
- identity stabilizes when identity_delta < ε  

IdOB stops when **either** stabilizes.

This ensures:

- deterministic convergence  
- replay‑safe behavior  
- bounded runtime  
- stable meaning semantics  

---

## **7. Conversational Identity and Parallel Search**

CIE is shared across parallel meaning candidates.

Conversation Thread Processor (CvThP) ensures:

- identity envelope consistency  
- identity envelope merging  
- identity envelope pruning  
- identity envelope stabilization across branches  

Parallel branches may produce:

- different meaning_semantics[]  
- different identity_delta  

CvThP selects the branch with:

- lowest meaning_delta_h  
- lowest identity_delta  
- highest identity_importance alignment  

---

## **8. Conversational Identity Stabilization Rules**

CIE is stable when:

$$
|\Delta h_{\text{identity}}| < \varepsilon_{\text{identity}}
$$

Typical threshold:

$$
\varepsilon_{\text{identity}} = 0.05
$$

CIE stabilization may occur:

- before meaning stabilization  
- after meaning stabilization  
- simultaneously with meaning stabilization  

IdOB stops when **either** stabilizes.

---

## **9. Conversational Identity and OuBA**

CIE is handed off to OuBA along with meaning_semantics[].

OuBA uses CIE to:

- evaluate truth  
- evaluate belief  
- evaluate semantic consistency  
- evaluate identity‑conditioned truth values  

CIE is **not** modified by OuBA.

---

## **10. Summary**

The Conversational Identity Envelope is:

- the identity state of the utterance inside the conversation  
- refined across IdOB cycles  
- used to rank meaning groups  
- used to modulate meaning dimensions  
- used to compute meaning_delta_h  
- used to detect stabilization  
- used to ensure deterministic convergence  
- used to support replay‑safe behavior  
- handed off to OuBA for truth/belief evaluation  

It is essential to IdOB’s structure→meaning mapping.

---
