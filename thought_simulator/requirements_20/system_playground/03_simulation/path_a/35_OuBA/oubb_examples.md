# OuBB Examples Specification

This document defines **representative OuBB examples** used to extract **textual meaning signatures** for the dictionary and projection system.

---

## 1. Purpose

Representative OuBB examples provide **canonical, semantic text realizations** for meanings that are:

- **stored** in dictionary entries,
- **used** by projection $\Pi$ to generate deterministic text, and
- **decoded** by reverse interpretation $\Pi^{-1}$ to recover SSR-origin meaning.

They are the **empirical basis** for textual meaning signatures.

---

## 2. What is a representative OuBB example?

**Representative OuBB example**  
A curated OuBB text instance that expresses a specific SSR-origin meaning in a stable, canonical way. It is:

- **semantic:** contains actual descriptive content, not just surface-form primitives.
- **canonical:** chosen to reflect the *intended* phrasing, tone, and structure.
- **stable:** expected to remain valid across runs and manifold versions (modulo controlled updates).
- **aligned:** consistent with the coordinate’s geometric context and dictionary entry.

Formally, for a dictionary coordinate $c$:

$$
\text{OuBB}\_{example}(c) = t_c
$$

where $t_c$ is a text instance used to extract the textual meaning signature $\sigma_c$.

---

## 3. Structure of an OuBB example

Each representative OuBB example is stored with explicit fields:

- **Meaning anchor:**  
  **Label:** SSR-origin meaning identifier (e.g., `meaning_id`, SSR field bundle).  
- **Coordinate link:**  
  **Label:** dictionary coordinate $c$ and manifold version $M_v$.  
- **Text instance:**  
  **Label:** canonical OuBB text $t_c$.  
- **Signature extraction:**  
  **Label:** derived textual meaning signature $\sigma_c$.  
- **Context metadata:**  
  **Label:** notes on usage context (explanatory, contrastive, summary, etc.).

Conceptually:

$$
(c, M_v, t_c) \longrightarrow \sigma_c
$$

where $\sigma_c$ is decomposed along the **Textual Output Dimensions** [dictionary_projection_spec.md](../manifold/manifold_white_papers/dictionary_projection_spec.md) glossary:

- lexical emphasis  
- syntactic structure  
- relational phrasing  
- tone  
- modality  
- narrative role  
- semantic shading  

---

## 4. Selection rules

Representative OuBB examples must satisfy:

- **Correctness:**  
  **Rule:** $t_c$ must accurately express the SSR-origin meaning associated with $c$.  
- **Coherence:**  
  **Rule:** phrasing, tone, and structure must be internally coherent and consistent with TS norms.  
- **Determinism:**  
  **Rule:** given $c$, $\Pi(c)$ should converge toward $t_c$ (or a close variant) under stable conditions.  
- **Non-degeneracy:**  
  **Rule:** examples must avoid pathological phrasing (overly vague, overly ornate, or structurally ambiguous).  
- **Geometric alignment:**  
  **Rule:** example behavior must match basin context (e.g., stable basin → stable phrasing; saddle → transitional phrasing).

In short:

$$
\Pi(c) \approx t_c \quad \text{and} \quad \Pi^{-1}(t_c) \approx \text{SSR}\_{meaning}(c)
$$

---

## 5. Storage and linkage

Representative OuBB examples are **not** stored inside the dictionary entry itself, but are **linked** to it:

- **Dictionary entry:**  
  Stores SSR-origin meaning, numeric vector, geometric context, textual meaning signature $\sigma_c$, correlation structure, projection metadata, reverse interpretation metadata.

- **OuBB example record:**  
  Stores $t_c$ and the mapping:

$$
t_c \longrightarrow \sigma_c
$$

Linkage:

- **Forward link:** dictionary entry for $c$ references the example set $\{t_c\}$.  
- **Reverse link:** example record references the dictionary coordinate $c$ and manifold version $M_v$.

This keeps:

- dictionary **compact and structural**,  
- examples **semantic and empirical**,  
while maintaining traceability.

---

## 6. Role in projection and reverse interpretation

### 6.1 Projection $\Pi$

Projection uses:

$$
(c, \text{geom}\_{context}(c), \sigma_c, \text{projection}\_{metadata}(c))
$$

to generate text. Representative examples:

- define **target behavior** for $\Pi$,
- constrain phrasing, tone, and structure,
- serve as **reference outputs** for testing projection stability.

### 6.2 Reverse interpretation $\Pi^{-1}$

Reverse interpretation uses:

$$
t \longrightarrow c \longrightarrow \text{SSR}\_{meaning}(c)
$$

Representative examples:

- provide **known-good pairs** $(t_c, c)$,
- allow validation that $\Pi^{-1}(t_c)$ returns the correct coordinate and meaning,
- support drift detection when $\Pi^{-1}$ begins mapping $t_c$ to misaligned coordinates.

---

## 7. Drift, stability, and updates

Representative OuBB examples participate in:

- **signature drift detection:**  
  If $\sigma_c$ changes significantly while $t_c$ is held fixed, this signals drift in textual behavior.

- **coordinate misalignment detection:**  
  If $\Pi(c)$ diverges from $t_c$ beyond acceptable tolerance, this signals projection or basin misalignment.

- **controlled updates:**  
  When examples are updated (e.g., improved phrasing), the corresponding $\sigma_c$, projection metadata, and reverse interpretation metadata must be revalidated.

Formally, stability requires:

$$
\Pi(c) \approx t_c \quad \text{and} \quad \Pi^{-1}(t_c) \approx c
$$

across runs and manifold versions, within defined tolerances.

---

## 8. Summary

- Representative OuBB examples are **canonical, semantic text instances** tied to dictionary coordinates.  
- They are used to **extract textual meaning signatures**, which live in the dictionary.  
- They are stored in a **separate, semantic layer**, linked to dictionary entries and manifold versions.  
- They define **target behavior** for $\Pi$ and $\Pi^{-1}$, and are central to **stability, drift detection, and traceability** in TS.
