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

# ⭐ These 10 will form the core of **input_patha_correction_sim.md**

If you want, I can now:

- generate the **paper skeleton**,  
- write the **intro section**,  
- or simulate **Case #1** end‑to‑end through InB → IIInB → CEx → CE → ISc → TPU.

Just tell me which direction you want to go.
