# **idob_stabilization_rules.md**  
### *Formal Stabilization Rules for IdOB Meaning Resolution*

---

## **1. Purpose**

IdOB runs **4–6 cycles** to convert:

> **structural geometry → meaning groups → meaning semantics → stabilized meaning**

Stabilization rules define **when IdOB must stop**, freeze meaning, freeze conversational identity, and hand off to OuBA.

These rules guarantee:

- deterministic convergence  
- replay‑safe behavior  
- bounded runtime  
- stable meaning semantics  
- stable conversational identity envelope  
- correct CvThP scheduling  

This paper is normative.

---

## **2. Stabilization Concepts**

IdOB stabilizes two things:

### **2.1 Meaning Stabilization**
Stabilization of the meaning vector:

$$
M = [physicality, sociality, temporality, intentionality, materiality, spatiality]
$$

### **2.2 Conversational Identity Stabilization**
Stabilization of the conversational identity envelope:

$$
I = identity\\_vector
$$

IdOB stops when **either** stabilizes.

---

## **3. Meaning Delta (meaning_delta_h)**

Meaning_delta_h measures semantic change across cycles:

$$
\Delta h_{\text{meaning}} = \| M_{i} - M_{i-1} \|
$$

Where:

- $M_i$ = meaning_semantics[] at cycle i  
- $M_{i-1}$ = meaning_semantics[] at previous cycle  

### **Meaning Stabilization Threshold**

$$
|\Delta h_{\text{meaning}}| < \varepsilon_{\text{meaning}}
$$

Default:

$$
\varepsilon_{\text{meaning}} = 0.05
$$

Meaning is stable when semantic change is small enough that further refinement would not materially alter interpretation.

---

## **4. Conversational Identity Delta (identity_delta)**

Identity_delta measures change in conversational identity across cycles:

$$
\Delta h_{\text{identity}} = \| I_{i} - I_{i-1} \|
$$

Where:

- $I_i$ = identity_vector at cycle i  
- $I_{i-1}$ = identity_vector at previous cycle  

### **Identity Stabilization Threshold**

$$
|\Delta h_{\text{identity}}| < \varepsilon_{\text{identity}}
$$

Default:

$$
\varepsilon_{\text{identity}} = 0.05
$$

Identity is stable when conversational identity stops shifting.

---

## **5. Stabilization Conditions**

IdOB stops refinement when **any** of the following are true:

---

### **Condition 1 — Meaning Stabilized**

$$
|\Delta h_{\text{meaning}}| < \varepsilon_{\text{meaning}}
$$

Meaning is stable.

---

### **Condition 2 — Conversational Identity Stabilized**

$$
|\Delta h_{\text{identity}}| < \varepsilon_{\text{identity}}
$$

Conversational identity is stable.

---

### **Condition 3 — Budget Exhausted**

$$
idob\_search\_budget\_used \geq idob\_search\_budget\_max
$$

Default:

- min = 4  
- max = 6  

Budget exhaustion forces stabilization.

---

### **Condition 4 — CvThP Time Pressure**

CvThP may force early stabilization if:

- TS is under time pressure  
- parallel branches exceed global limits  
- conversation latency must be reduced  

CvThP signals:

```
time_exhausted = true
```

IdOB must stop immediately.

---

## **6. Stabilization Ordering**

IdOB checks stabilization **after each cycle** in this order:

1. **Meaning stabilization**  
2. **Identity stabilization**  
3. **Budget exhaustion**  
4. **CvThP time pressure**

This ordering ensures:

- meaning is prioritized  
- identity is secondary  
- budget/time are safety nets  

---

## **7. Parallel Branch Stabilization (CvThP)**

When IdOB evaluates multiple meaning candidates in parallel:

CvThP merges branches using:

### **Rule A — Lowest meaning_delta_h wins**
The branch with the smallest semantic change is preferred.

### **Rule B — Lowest identity_delta wins**
If meaning_delta_h ties, identity_delta breaks the tie.

### **Rule C — Highest identity_importance alignment wins**
If both deltas tie, conversational identity alignment wins.

### **Rule D — Stabilized branches terminate early**
If any branch stabilizes:

- CvThP prunes all unstable branches  
- IdOB adopts the stabilized branch  

Parallel stabilization ensures deterministic convergence.

---

## **8. Stabilization Outcomes**

IdOB sets `meaning_resolution_status` to one of:

### **1. stable**
Meaning stabilized normally.

### **2. identity_stable**
Conversational identity stabilized before meaning.

### **3. budget_exhausted**
Budget reached before stabilization.

### **4. time_exhausted**
CvThP forced early stop.

These outcomes are written into:

```yaml
finalization:
  meaning_resolution_status: <status>
  ready_for_ouba: true
```

---

## **9. Handoff to OuBA**

When stabilization occurs:

IdOB freezes:

- meaning_semantics[]  
- idob_semantics[]  
- conversational identity envelope  
- meaning_resolution_status  

Then hands off to OuBA.

OuBA performs:

- truth evaluation  
- belief evaluation  
- semantic consistency evaluation  

IdOB does **not** perform truth or belief.

---

## **10. Summary**

IdOB stabilization rules define:

- how meaning_delta_h is computed  
- how identity_delta is computed  
- thresholds for stabilization  
- cycle‑level stabilization checks  
- parallel branch stabilization (CvThP)  
- budget/time‑based stabilization  
- finalization outcomes  
- OuBA handoff conditions  

These rules guarantee:

- deterministic convergence  
- replay‑safe behavior  
- bounded runtime  
- stable meaning semantics  
- stable conversational identity  
- correct CvThP coordination  

Stabilization rules complete the IdOB subsystem.

---
