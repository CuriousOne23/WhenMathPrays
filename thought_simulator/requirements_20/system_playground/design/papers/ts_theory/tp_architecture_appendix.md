# **tp_architecture_appendix.md**  
### *Thought Pipeline (TP) — Architectural Appendix*  
**Version 1.0 — Visual & Structural Maps**  
**Author:** CuriousOne (Jeff)

This appendix provides the **visual and structural representations** of the Thought Pipeline (TP) architecture described in **tp_architecture.md**.  
It contains:

- **A. TP Architecture Diagram**  
- **B. TP Mermaid Diagram**  
- **C. TP Field Lineage Map**  
- **D. TP Commit Boundary Map**

These diagrams and maps are architectural views — not primitive descriptions.  
For primitive‑level details, see **tp_description.md**.

---

# **A. TP Architecture Diagram**  
### *Layer‑centric view of the Thought Pipeline*

```
┌──────────────────────────────────────────────────────────────┐
│                        Thought Pipeline (TP)                 │
│        Deterministic, Bounded, Replay‑Safe Cognitive Engine  │
└──────────────────────────────────────────────────────────────┘

Intake Layer
────────────
Raw Input → Structural Normalization → First Meaning Commit (Mₜ)

Context & Relevance Layer
──────────────────────────
Continuity Constraints + Identity Constraints → Context Frame

Meaning Construction Layer (Path‑A)
────────────────────────────────────
Semantic‑Adjacent Cues → Semantic‑Layer Cues → Identity‑Conditioned Meaning

Commit Layer
────────────
Canonical Meaning → Cognitive Commit (TPU) → Behavioral Commit (OuBA)

Long‑Term Conversation Layer
─────────────────────────────
Identity Continuity + Referent Continuity + Next‑Turn Context

Expression Layer (Path‑B)
──────────────────────────
SSR Freeze → Expression Plan → Output
```

This diagram shows the **architecture**, not the primitive sequence.

---

# **B. TP Mermaid Diagram**  
### *High‑level architectural flow (not primitives)*

```mermaid
flowchart TD

    subgraph Intake["Layer 1: Intake Layer"]
        A[Raw Input] --> B[Structural Normalization]
        B --> C[First Meaning Commit (Mₜ)]
    end

    subgraph Context["Layer 2: Context & Relevance"]
        C --> D[Continuity Constraints]
        C --> E[Identity Constraints]
        D --> F[Context Frame]
        E --> F
    end

    subgraph Meaning["Layer 3: Meaning Construction (Path‑A)"]
        F --> G[Semantic‑Adjacent Extraction]
        G --> H[Semantic‑Layer Extraction]
        H --> I[Identity‑Conditioned Meaning Construction]
    end

    subgraph Commit["Layer 4: Commit Layer"]
        I --> J[Cognitive Commit (TPU)]
        J --> K[Behavioral Commit (OuBA)]
        K --> L[SSR Freeze]
    end

    subgraph LTC["Layer 5: Long‑Term Conversation"]
        L --> M[Identity Continuity]
        L --> N[Referent Continuity]
        L --> O[Next‑Turn Context]
    end

    subgraph Expression["Layer 6: Expression Layer (Path‑B)"]
        L --> P[Expression Plan]
        P --> Q[Output]
    end
```

This diagram shows **layer transitions**, not primitive transitions.

---

# **C. TP Field Lineage Map**  
### *How meaning attributes flow through the TP architecture*

This map shows how the meaning state vector defined in **ts_meaning_theory.md** flows through the TP layers.

---

## **1. Intake Layer → Context Layer**

| Meaning Attribute | Source | Transformation | Output |
|-------------------|--------|----------------|--------|
| topic | raw input | extracted + stabilized | Context Frame |
| intent | raw input | extracted + stabilized | Context Frame |
| clarifying fields | raw input | normalized | Context Frame |
| provenance | first commit | initialized | Context Frame |
| identity continuity | prior turn | copied forward | Context Frame |
| referent continuity | prior turn | copied forward | Context Frame |

---

## **2. Context Layer → Meaning Construction Layer**

| Meaning Attribute | Source | Transformation | Output |
|-------------------|--------|----------------|--------|
| stance | continuity + identity | initialized | canonical meaning |
| direction | continuity + identity | initialized | canonical meaning |
| coherence | continuity + identity | initialized | canonical meaning |
| importance | continuity + identity | initialized | canonical meaning |
| next‑turn context | continuity | prepared | canonical meaning |

---

## **3. Meaning Construction Layer → Commit Layer**

| Meaning Attribute | Source | Transformation | Output |
|-------------------|--------|----------------|--------|
| semantic‑adjacent cues | OB family | extracted | canonical meaning |
| semantic‑layer cues | STPX | extracted | canonical meaning |
| freeze signatures | identity + continuity | generated | committed meaning |
| entropy | ISc | evaluated | committed meaning |

---

## **4. Commit Layer → Long‑Term Conversation Layer**

| Meaning Attribute | Source | Transformation | Output |
|-------------------|--------|----------------|--------|
| provenance | TPU | frozen | SSR |
| coherence | TPU | locked | SSR |
| stance/direction | TPU | locked | SSR |
| referent continuity | IdOB | stabilized | LTC layer |
| identity continuity | IdOB | stabilized | LTC layer |
| next‑turn context | MCB | propagated | LTC layer |

---

## **5. Long‑Term Conversation Layer → Next Turn**

| Meaning Attribute | Source | Transformation | Output |
|-------------------|--------|----------------|--------|
| identity continuity | COB/CST | stabilized | next turn |
| referent continuity | COB/CST | stabilized | next turn |
| next‑turn context | MCB | propagated | next turn |

---

# **D. TP Commit Boundary Map**  
### *Where commit happens and what is committed*

Commit is a **hard architectural boundary**.

There are **three commit points**:

---

## **1. Structural Commit (IIInB → IE)**  
**Commits:**

- structural normalization  
- repaired geometry  
- first provenance  
- first meaning envelope  

**Why:**  
Raw input must be stabilized before meaning extraction.

---

## **2. Cognitive Commit (CE → TPU)**  
**Commits:**

- canonical meaning  
- stance/direction/coherence  
- identity‑conditioned meaning  
- continuity signals  
- provenance lineage  
- coherence lock  
- normalized fields  

**Why:**  
Meaning must be frozen before evaluation, routing, or identity cycles.

This is the **primary commit boundary**.

---

## **3. Behavioral Commit (RB → OuBA)**  
**Commits:**

- final meaning  
- final stance/direction/coherence  
- final qualifiers  
- final commitments  
- freeze signatures  
- semantic_core  

**Why:**  
Meaning must be frozen before expression.

---

## **4. SSR Freeze (OuBA → SSRGen)**  
**Commits:**

- immutable semantic snapshot  
- replay‑safe meaning  
- deterministic representation  
- Path‑A → Path‑B boundary  

**Why:**  
Meaning must be immutable for expression and replay.

---

# **End of tp_architecture_appendix.md**
