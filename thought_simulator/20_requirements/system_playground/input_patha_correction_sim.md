Perfect — now that we’re aligned on **input_patha_correction_sim.md**, we can define the **10 common mistake cases** that will *stress‑test* the Path‑A‑only pipeline:

**InB → IIInB → CEx → CE → ISc → TPU**

These 10 cases are chosen because they expose the *exact* weaknesses Path A must handle:

- missing structure  
- wrong order  
- ambiguous roles  
- broken grammar  
- missing connectors  
- tense drift  
- negation drift  
- emotional noise  
- fragmentary input  
- multi‑clause collapse  

They are also simple enough that we can simulate them cleanly without OB/RB/TR/DCB.

Below is the **final list** I recommend for the playground paper.

---

# ⭐ **The 10 Common Mistake Cases for Path A Stress‑Testing**

These are the ones that best reveal whether Path A can still produce a coherent TP(N+1) + semantic_core snapshot.

---

## **1. Missing Words (Ellipsis)**  
**Input:**  
> “Went store forgot wallet.”

Why it’s a good test:  
- missing subject  
- missing prepositions  
- missing conjunctions  
- multiple clauses smashed together  

Path A must still extract a proto‑proposition.

---

## **2. Wrong Order (Scrambled Tokens)**  
**Input:**  
> “The mouse the cat chased.”

Why it’s a good test:  
- non‑canonical order  
- relative clause without marker  
- ambiguous subject/object roles  

Path A must still extract a stable candidate.

---

## **3. Missing Preposition / Article**  
**Input:**  
> “I go store yesterday.”

Why it’s a good test:  
- missing “to the”  
- tense mismatch  
- unnatural order  
- but still structurally interpretable  

This is the canonical Path A test.

---

## **4. Ambiguous Pronoun**  
**Input:**  
> “John told Mark he was wrong.”

Why it’s a good test:  
- two male entities  
- pronoun ambiguity  
- Path A must preserve ambiguity, not resolve it  

---

## **5. Negation Drift**  
**Input:**  
> “I didn’t say you stole the money.”

Why it’s a good test:  
- multiple possible scopes  
- Path A must not collapse meaning  
- must produce multiple candidate propositions  

---

## **6. Emotional Noise / Affective Injection**  
**Input:**  
> “Ugh this stupid thing never works.”

Why it’s a good test:  
- affective tokens  
- stance cues  
- factual vs emotional separation  

Path A must tag affect but still extract a proposition.

---

## **7. Fragmentary Input**  
**Input:**  
> “Because tired.”

Why it’s a good test:  
- subordinate clause without main clause  
- missing subject  
- missing verb  
- incomplete thought  

Path A must still produce a minimal candidate.

---

## **8. Run‑On Without Connectors**  
**Input:**  
> “I was late the car broke.”

Why it’s a good test:  
- two clauses fused  
- missing conjunction  
- missing punctuation  
- ambiguous relation  

Path A must extract two propositions.

---

## **9. Mixed Tense / Aspect Drift**  
**Input:**  
> “He go yesterday but is going now.”

Why it’s a good test:  
- tense mismatch  
- aspect mismatch  
- two temporal frames  
- Path A must preserve both  

---

## **10. Implicit Subject (Command‑like Fragment)**  
**Input:**  
> “Fixing the car now.”

Why it’s a good test:  
- missing subject  
- ambiguous agent  
- present participle without auxiliary  

Path A must still extract a proto‑event.

---

# ⭐ Why these 10 are the right set

Because they cover the **full spectrum** of input‑side failure modes that Path A must handle *without*:

- OB  
- RB  
- TR  
- DCB  
- TB  
- Path B  

These 10 cases stress:

- structural inference  
- lexical plausibility  
- clause segmentation  
- role extraction  
- ambiguity preservation  
- ΔH% scoring  
- TPU commit logic  

They are also simple enough to simulate step‑by‑step in the paper.

---

Absolutely, Jeff — here are the **exact raw input sentences** for all **10 cases**, clean and ready for you to paste directly into *input_patha_correction_sim.md*.  
No polishing, no commentary — just the **literal inputs** exactly as you requested.

---

# ⭐ **The 10 Common Mistake Inputs (verbatim)**

### **1. Missing Words (Ellipsis)**  
**Input:**  
`Went store forgot wallet.`

---

### **2. Wrong Order (Scrambled Tokens)**  
**Input:**  
`The mouse the cat chased.`

---

### **3. Missing Preposition / Article**  
**Input:**  
`I go store yesterday.`

---

### **4. Ambiguous Pronoun**  
**Input:**  
`John told Mark he was wrong.`

---

### **5. Negation Drift**  
**Input:**  
`I didn’t say you stole the money.`

---

### **6. Emotional Noise / Affective Injection**  
**Input:**  
`Ugh this stupid thing never works.`

---

### **7. Fragmentary Input**  
**Input:**  
`Because tired.`

---

### **8. Run‑On Without Connectors**  
**Input:**  
`I was late the car broke.`

---

### **9. Mixed Tense / Aspect Drift**  
**Input:**  
`He go yesterday but is going now.`

---

### **10. Implicit Subject (Command‑like Fragment)**  
**Input:**  
`Fixing the car now.`

Absolutely, Jeff — here is **exactly what you asked for**:

A **raw, rough, unpolished simulation** of all **10 common mistake inputs** through:

**InB → IIInB → CEx → CE → ISc → TPU**

Each case includes:

- **Input**  
- **Step‑by‑step primitive outputs** (rough, not polished)  
- **TPU commit snapshot**  
- **Pass/Fail assessment** (did Path A produce a coherent TP(N+1)?)  

This is *record‑mode*, not polished prose — perfect for pasting into the playground paper.

---

# ⭐ **CASE 1 — Missing Words (Ellipsis)**  
**Input:** `Went store forgot wallet.`

### **InB**
- tokens: [Went, store, forgot, wallet]  
- order: 1–4  
- POS guess: VERB, NOUN, VERB, NOUN  

### **IIInB**
- detects two verb events  
- missing subject  
- missing connectors  

### **CEx**
- candidate 1: head=went, args={agent:?, destination:store}  
- candidate 2: head=forgot, args={agent:?, object:wallet}  

### **CE**
- both structurally plausible  
- lexical completeness: low  
- structural completeness: medium  

### **ISc**
- ΔH%: small positive  
- confidence: ~0.55  

### **TPU**
- commits two propositions with missing‑role flags  

### **Assessment:** **PASS**  
Path A extracted two proto‑events.

---

# ⭐ **CASE 2 — Wrong Order (Scrambled Tokens)**  
**Input:** `The mouse the cat chased.`

### **InB**
- tokens: [The, mouse, the, cat, chased]  

### **IIInB**
- noun phrase → noun phrase → verb  
- ambiguous subject/object  

### **CEx**
- candidate: head=chased, args={agent:cat?, object:mouse?}  

### **CE**
- marks ambiguity  
- structural score: medium  

### **ISc**
- ΔH%: neutral  
- confidence: ~0.48  

### **TPU**
- commits proposition with ambiguity flags  

### **Assessment:** **PASS**  
Ambiguity preserved, not hallucinated.

---

# ⭐ **CASE 3 — Missing Preposition / Article**  
**Input:** `I go store yesterday.`

### **InB**
- tokens: [I, go, store, yesterday]  

### **IIInB**
- pronoun → verb → noun → time  

### **CEx**
- candidate: head=go, args={agent:I, destination:store, time:yesterday}  

### **CE**
- tense mismatch flagged  
- missing preposition flagged  

### **ISc**
- ΔH%: small positive  
- confidence: ~0.63  

### **TPU**
- commits single proposition with warnings  

### **Assessment:** **PASS**  
Stable proto‑event extracted.

---

# ⭐ **CASE 4 — Ambiguous Pronoun**  
**Input:** `John told Mark he was wrong.`

### **InB**
- tokens: [John, told, Mark, he, was, wrong]  

### **IIInB**
- two male entities  
- pronoun ambiguous  

### **CEx**
- candidate A: he=John  
- candidate B: he=Mark  

### **CE**
- both plausible  
- ambiguity preserved  

### **ISc**
- ΔH%: neutral  
- confidence: ~0.50  

### **TPU**
- commits two parallel propositions  

### **Assessment:** **PASS**  
Ambiguity preserved correctly.

---

# ⭐ **CASE 5 — Negation Drift**  
**Input:** `I didn’t say you stole the money.`

### **InB**
- tokens: [I, didn’t, say, you, stole, the, money]  

### **IIInB**
- negation attached to verb phrase  
- multiple possible scopes  

### **CEx**
- candidate 1: negation applies to “say”  
- candidate 2: negation applies to “you stole”  
- candidate 3: negation applies to entire proposition  

### **CE**
- all structurally valid  
- marks multi‑scope ambiguity  

### **ISc**
- ΔH%: neutral  
- confidence: ~0.52  

### **TPU**
- commits multi‑trace semantic_core  

### **Assessment:** **PASS**  
Negation ambiguity preserved.

---

# ⭐ **CASE 6 — Emotional Noise**  
**Input:** `Ugh this stupid thing never works.`

### **InB**
- tokens: [Ugh, this, stupid, thing, never, works]  

### **IIInB**
- affective tokens detected  
- factual core: “thing works”  

### **CEx**
- candidate: head=works, args={subject:thing}, negation=never  

### **CE**
- affect separated from proposition  

### **ISc**
- ΔH%: small positive  
- confidence: ~0.70  

### **TPU**
- commits proposition + affect layer  

### **Assessment:** **PASS**  
Affect isolated, meaning preserved.

---

# ⭐ **CASE 7 — Fragmentary Input**  
**Input:** `Because tired.`

### **InB**
- tokens: [Because, tired]  

### **IIInB**
- subordinate clause without main clause  
- missing subject  

### **CEx**
- candidate: state=tired, agent=?  

### **CE**
- incomplete but structurally interpretable  

### **ISc**
- ΔH%: small negative (incomplete)  
- confidence: ~0.40  

### **TPU**
- commits minimal state proposition  

### **Assessment:** **PASS**  
Minimal thought extracted.

---

# ⭐ **CASE 8 — Run‑On Without Connectors**  
**Input:** `I was late the car broke.`

### **InB**
- tokens: [I, was, late, the, car, broke]  

### **IIInB**
- detects two verb events  
- missing conjunction  

### **CEx**
- candidate 1: head=late, agent=I  
- candidate 2: head=broke, subject=car  

### **CE**
- both valid  
- no relation inferred  

### **ISc**
- ΔH%: small positive  
- confidence: ~0.60  

### **TPU**
- commits two independent propositions  

### **Assessment:** **PASS**  
Two events extracted cleanly.

---

# ⭐ **CASE 9 — Mixed Tense / Aspect Drift**  
**Input:** `He go yesterday but is going now.`

### **InB**
- tokens: [He, go, yesterday, but, is, going, now]  

### **IIInB**
- two temporal frames  
- two verb events  

### **CEx**
- candidate 1: head=go, time=yesterday  
- candidate 2: head=going, time=now  

### **CE**
- tense mismatch flagged  
- aspect mismatch flagged  

### **ISc**
- ΔH%: small positive  
- confidence: ~0.58  

### **TPU**
- commits two propositions with warnings  

### **Assessment:** **PASS**  
Temporal structure preserved.

---

# ⭐ **CASE 10 — Implicit Subject**  
**Input:** `Fixing the car now.`

### **InB**
- tokens: [Fixing, the, car, now]  

### **IIInB**
- missing subject  
- present participle  

### **CEx**
- candidate: head=fixing, args={agent:?, object:car, time:now}  

### **CE**
- incomplete but valid  

### **ISc**
- ΔH%: small positive  
- confidence: ~0.57  

### **TPU**
- commits proto‑event with missing‑agent flag  

### **Assessment:** **PASS**  
Event extracted despite missing subject.

---

# ⭐ **Summary of All 10 Cases**
All 10 inputs produced:

- a coherent TP(N+1)  
- a stable semantic_core  
- no hallucination  
- no grammar repair  
- ambiguity preserved where appropriate  
- ΔH% stable  
- TPU commit successful  

**Path A passed all 10 stress tests.**

---

If you want, I can now:

- polish these into final paper‑ready prose  
- generate the markdown structure  
- add headers and formatting  
- or simulate additional edge cases  

Just tell me what you want next.
---
