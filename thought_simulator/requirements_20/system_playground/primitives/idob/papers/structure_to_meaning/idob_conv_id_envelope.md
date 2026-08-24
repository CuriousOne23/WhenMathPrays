# **idob_conv_id_envelope.md**  
### *Conversational Identity Envelope — Definition, Dynamics, and Role in IdOB Meaning Resolution*

---

## **1. Purpose**  
The **Conversational Identity Envelope (CIE)** is IdOB’s internal representation of **identity‑conditioned meaning within the conversation**.  
It is the mechanism that allows IdOB to:

- interpret meaning in conversational context   [Current page](citation-section://1147006281/3)  
- modulate meaning based on conversational identity cues   [Current page](citation-section://1147006281/3)  
- refine meaning across cycles   [Current page](citation-section://1147006281/3)  
- stabilize meaning_delta_h   [Current page](citation-section://1147006281/3)  
- influence meaning group ranking   [Current page](citation-section://1147006281/3)  
- support replay‑safe convergence   [Current page](citation-section://1147006281/3)  
- integrate identity metadata from PT1   [Current page](citation-section://1147006281/3)  
- produce identity‑aware meaning semantics for OuBA   [Current page](citation-section://1147006281/3)  

The CIE is **not**:

- the user’s identity  
- the speaker’s persona  
- a long‑term memory identity  
- a global identity model   [Current page](citation-section://1147006281/4)  

It is strictly:

> **the identity state of the utterance inside the conversation**   [Current page](citation-section://1147006281/5)

---

## **2. Why Conversational Identity Exists**  
Meaning is not purely structural.  
Two utterances with identical structural geometry may require different interpretations depending on conversational identity. Examples include: “burst,” “rock,” “chew,” “sleepy” — each having physical vs. metaphorical readings depending on conversational stance and cues   [Current page](citation-section://1147006281/8).

These differences arise from:

- conversational stance  
- conversational cues  
- conversational roles  
- conversational identity pressure   [Current page](citation-section://1147006281/8)  

The CIE provides the semantic context needed to resolve these differences   [Current page](citation-section://1147006281/9).

---

## **3. Inputs to the Conversational Identity Envelope**  
The CIE begins with identity metadata from PT1:

```yaml
identity_metadata:
  identity_tags: [<string>, ...]
  identity_vector: [<int>, ...]
```  
  [Current page](citation-section://1147006281/10)

These come from:

- routing_signature  
- residue analysis  
- lexical identity anchors  
- meaning group identity anchors  
- conversational cues  
- conversational stance  
- conversational identity roles   [Current page](citation-section://1147006281/11)  

The CIE is refined by IdOB across cycles.

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
  [Current page](citation-section://1147006281/12)

### **Fields Explained**

#### **identity_importance**  
Scalar representing how strongly conversational identity influences meaning.

#### **identity_tags**  
Semantic tags extracted from conversational context (e.g., “scientific,” “physical,” “social,” “temporal,” “biological”)   [Current page](citation-section://1147006281/13).

#### **identity_vector**  
Numeric vector representing conversational identity anchors, derived from meaning group anchors, lexical anchors, routing signatures, residue hashes, and conversational cues   [Current page](citation-section://1147006281/14).

#### **identity_delta**  
Measures change in conversational identity across cycles:

$$
\Delta h_{\text{identity}} = \| I_i - I_{i-1} \|
$$  

#### **stabilization.identity_stable**  
True when:

$$
|\Delta h_{\text{identity}}| < \varepsilon_{\text{identity}}
$$  


---

## **5. Conversational Identity Dynamics Across IdOB Cycles**

### **Cycle 0 — Initialization**  
CIE seeded with PT1 metadata   [Current page](citation-section://1147006281/17).

### **Cycle 1 — Coarse Tier**  
CIE influences meaning group ranking   [Current page](citation-section://1147006281/18).

### **Cycle 2 — Medium Tier**  
CIE modulates meaning dimensions   [Current page](citation-section://1147006281/19).

### **Cycle 3 — Fine Tier**  
CIE helps select final meaning group   [Current page](citation-section://1147006281/20).

### **Cycle 4–5 — Refinement**  
CIE updated based on meaning_semantics[], dimensions, invariants, cues, triggers/suppressors, and conversational identity pressure   [Current page](citation-section://1147006281/20).

### **Cycle 6 — Stabilization**  
CIE stabilizes when identity_delta < threshold.

---

## **6. How Conversational Identity Influences Meaning Resolution**

### **6.1 Meaning Group Ranking**  
CIE modifies ranking of meaning_group_candidates:

- boosts identity‑aligned groups  
- suppresses misaligned groups  
- adjusts identity_weight  

Example: “scientific” identity → materiality↑, physicality↑, sociality↓   [Current page](citation-section://1147006281/22).

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

This produces identity‑conditioned meaning   [Current page](citation-section://1147006281/23).

---

### **6.3 Meaning Stabilization**  
CIE contributes to stabilization:

- meaning stabilizes when meaning_delta_h < ε  
- identity stabilizes when identity_delta < ε  
- IdOB stops when either stabilizes   [Current page](citation-section://1147006281/24)  

This ensures deterministic convergence, replay‑safety, bounded runtime, and stable meaning semantics.

---

## **7. Conversational Identity and Parallel Search**

CIE is shared across parallel meaning candidates.  
CvThP ensures:

- identity envelope consistency  
- identity envelope merging  
- identity envelope pruning  
- identity envelope stabilization across branches   [Current page](citation-section://1147006281/26)  

Parallel branches may produce different meaning_semantics[] and identity_delta.  
CvThP selects the branch with:

- lowest meaning_delta_h  
- lowest identity_delta  
- highest identity_importance alignment   [Current page](citation-section://1147006281/26)

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


Stabilization may occur:

- before meaning stabilization  
- after meaning stabilization  
- simultaneously with meaning stabilization  

IdOB stops when either stabilizes.

---

## **9. Conversational Identity and OuBA**

CIE is handed off to OuBA along with meaning_semantics[]   [Current page](citation-section://1147006281/28).

OuBA uses CIE to:

- evaluate truth  
- evaluate belief  
- evaluate semantic consistency  
- evaluate identity‑conditioned truth values   [Current page](citation-section://1147006281/29)  

CIE is **not** modified by OuBA.

---

## **10. Summary**

The Conversational Identity Envelope is:

- the identity state of the utterance inside the conversation   [Current page](citation-section://1147006281/30)  
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
