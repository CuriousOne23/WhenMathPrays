# **idob_meaning_dimensions.md**  
### *Definition, Purpose, and Use of Meaning Dimensions in IdOB*

---

## **1. Purpose**

Meaning dimensions are the **axes** IdOB uses to:

- encode meaning_semantics[]  
- compute meaning_delta_h  
- refine meaning across cycles  
- stabilize meaning before OuBA handoff  
- evaluate identity‑conditioned meaning shifts  
- compare meaning groups  
- support coarse → medium → fine → stabilization search  

Meaning dimensions are **stable**, **replay‑safe**, and **global** across all meaning groups.

They form the **semantic coordinate system** for IdOB.

---

## **2. Why Meaning Dimensions Exist**

IdOB cannot rely solely on:

- primitives  
- cue envelopes  
- invariant tags  
- routing signatures  
- identity anchors  

These are **categorical** features.

IdOB needs **continuous** features to:

- measure semantic change  
- detect stabilization  
- compute meaning_delta_h  
- compare meaning candidates  
- refine meaning inside a group  
- support identity envelope modulation  
- support parallel search ranking  
- support deterministic convergence  

Meaning dimensions provide this continuous space.

---

## **3. The Six Meaning Dimensions**

IdOB uses **six** meaning dimensions, derived from your lexical meaning dictionary and aligned with cognitive semantics.

These dimensions are:

1. **Physicality**  
2. **Sociality**  
3. **Temporality**  
4. **Intentionality**  
5. **Materiality**  
6. **Spatiality**

Each dimension is a **float** in the range:

$$
0.0 \leq d \leq 1.0
$$

These six dimensions form the **meaning_semantics[] vector**.

---

## **4. Dimension Definitions**

### **4.1 Physicality**  
Degree to which meaning relates to:

- physical objects  
- physical actions  
- bodily movement  
- tangible phenomena  

High physicality examples:

- walk  
- push  
- rock  
- burst  
- chew (physical sense)

Low physicality examples:

- idea  
- permission  
- belief  

---

### **4.2 Sociality**  
Degree to which meaning relates to:

- social interaction  
- group behavior  
- interpersonal dynamics  
- cultural roles  

High sociality examples:

- gossip  
- negotiate  
- crowd  
- family  

Low sociality examples:

- rock  
- sleep  
- temperature  

---

### **4.3 Temporality**  
Degree to which meaning relates to:

- time  
- events  
- change  
- duration  
- sequence  

High temporality examples:

- burst  
- transform  
- event  
- schedule  

Low temporality examples:

- object  
- shape  
- color  

---

### **4.4 Intentionality**  
Degree to which meaning involves:

- intention  
- agency  
- purpose  
- volition  

High intentionality examples:

- decide  
- choose  
- plan  
- aim  

Low intentionality examples:

- fall  
- break  
- melt  

---

### **4.5 Materiality**  
Degree to which meaning involves:

- material transformation  
- substance  
- physical composition  
- matter  

High materiality examples:

- melt  
- freeze  
- carve  
- build  

Low materiality examples:

- think  
- believe  
- negotiate  

---

### **4.6 Spatiality**  
Degree to which meaning involves:

- spatial relations  
- location  
- movement through space  
- geometry  

High spatiality examples:

- beside  
- across  
- near  
- path  

Low spatiality examples:

- emotion  
- belief  
- permission  

---

## **5. Meaning Semantics Vector**

IdOB encodes meaning as:

```yaml
meaning_semantics:
  physicality: <float>
  sociality: <float>
  temporality: <float>
  intentionality: <float>
  materiality: <float>
  spatiality: <float>
```

This vector is:

- computed each cycle  
- refined across cycles  
- used to compute meaning_delta_h  
- used to detect stabilization  
- used to compare meaning candidates  
- used to modulate identity envelope  

---

## **6. Meaning Delta (meaning_delta_h)**

Meaning_delta_h measures **semantic change** across cycles:

$$
\Delta h_{\text{meaning}} = \| M_{i} - M_{i-1} \|
$$

Where:

- \( M_i \) = meaning_semantics[] at cycle i  
- \( M_{i-1} \) = meaning_semantics[] at previous cycle  

IdOB stops when:

$$
|\Delta h_{\text{meaning}}| < \varepsilon_{\text{meaning}}
$$

This is the **stabilization condition**.

---

## **7. How Meaning Dimensions Interact with Identity Envelope**

Identity envelope modulates meaning dimensions by:

- boosting certain dimensions  
- suppressing others  
- shifting meaning group ranking  
- influencing meaning_delta_h  
- influencing stabilization  

Example:

If identity tags include:

- “scientific” → boost materiality  
- “social” → boost sociality  
- “physical” → boost physicality  

Identity envelope is applied **after** meaning group selection.

---

## **8. How Meaning Dimensions Support Search Schema**

Meaning dimensions support:

### **Coarse Tier**  
Broad meaning group selection.

### **Medium Tier**  
Narrowing meaning groups.

### **Fine Tier**  
Selecting the best meaning group.

### **Stabilization Tier**  
Refining meaning_semantics[] until meaning_delta_h converges.

Meaning dimensions are the **continuous space** that makes stabilization possible.

---

## **9. Why Six Dimensions (Not More, Not Fewer)**

Six dimensions are:

- expressive enough to capture semantic variation  
- minimal enough to remain computationally efficient  
- orthogonal enough to avoid redundancy  
- stable across lexical entries  
- aligned with your meaning dictionary examples  
- aligned with cognitive semantics literature  
- aligned with IdOB’s search budget (4–6 cycles)  

Adding more dimensions would:

- increase search cost  
- reduce determinism  
- complicate stabilization  
- reduce replay‑safety  

Six is the correct number.

---

## **10. Summary**

Meaning dimensions:

- define IdOB’s semantic coordinate system  
- support meaning group selection  
- support meaning refinement  
- support identity envelope modulation  
- support meaning_delta_h computation  
- support stabilization  
- support deterministic convergence  
- support replay‑safe behavior  
- support the unified search schema  

They are essential to IdOB’s structure→meaning mapping.

---
