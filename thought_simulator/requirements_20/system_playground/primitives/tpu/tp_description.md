# `tp_description.md`  
### **Thought Packet (TP) Description White Paper**  
### *Deterministic, Replay‑Safe, CCR‑Aligned Architecture Overview*  
### *With CE → TPU Boundary Focus*

---

# **1. Introduction**

The **Thought Packet (TP)** is the canonical, deterministic, lane‑local data structure used throughout **Path‑A**.  
It is the *only* object exchanged between primitives, and it is the *only* object committed by TPU and frozen by OuBA.

This white paper explains:

- how the TP is **organized**,  
- why each envelope exists,  
- which primitives **write** each field,  
- which primitives **read** each field,  
- how CE and TPU form the **semantic firewall**,  
- and how deterministic replay is guaranteed.

The goal is to restore a clear, intuitive understanding of the TP’s design.

---

# **2. High‑Level TP Architecture**

The TP is composed of **envelopes** — structured, bounded, deterministic blocks of metadata and semantic information.

Here is the high‑level structure:

```mermaid
flowchart TD
    A[TP Identity Block] --> B[Semantic Envelope]
    B --> C[Context Envelope]
    C --> D[Context Metadata Envelope (CE)]
    D --> E[MSL Metadata]
    E --> F[Continuity Metadata]
    F --> G[Semantic-Importance Envelope]
    G --> H[CCR Output Envelope]
    H --> I[CIL Metadata]
    I --> J[Structural Envelope]
    J --> K[Routing Metadata]
    K --> L[Provenance Metadata]
    L --> M[Entropy Metadata]
    M --> N[Freeze Metadata]
```

Each envelope is deterministic, bounded, and replay‑safe.

---

# **3. TP Envelope Overview Table**

This table gives you the “feel” of the TP — what each envelope is, why it exists, who writes it, and who reads it.

| Envelope | Purpose | Written By | Read By |
|---------|---------|------------|---------|
| **Identity Block** | TP identity, lane, cycle | InB | All primitives |
| **Semantic Envelope** | propositions, truth evidence | IE, OB‑Set | TR, IdOB |
| **Context Envelope (Raw)** | raw context fields | CEx‑Pck | CE |
| **Context Metadata (CE)** | canonical context | CE → TPU | IdOB, TR, RB, CIL, CST |
| **MSL Metadata** | stance, shading, qualifiers | CEx‑Pck | IdOB, RB, MCB |
| **Continuity Metadata** | clarifying fields, topology | CE → TPU | IdOB, TR, CIL, CST |
| **Semantic‑Importance** | bounded semantic residues | OB‑Set, IdOB | CCR, COB, CIL |
| **CCR Output Envelope** | alignment, scores, decision | CEx‑CCR | CEx‑Pck, COB, CIL |
| **CIL Metadata** | selected conversation | CEx‑CCR | COB, CIL |
| **Structural Envelope** | semantic geometry | SOB, SROB, CnOB, SmOB | ISc |
| **Routing Metadata** | arbitration, routing path | RB, RBU, RTU | TR, IdOB |
| **Provenance Metadata** | commit lineage | TPU | All primitives |
| **Entropy Metadata** | ΔH%, entropy trace | TR, OuBA | OuBA |
| **Freeze Metadata** | final freeze snapshot | SSRGn | OuBA |

This table is the backbone of the white paper.

---

# **4. The CE → TPU Boundary (The Semantic Firewall)**

The most important architectural seam in Path‑A is:

```
CEx‑Pck → CE → TPU → TP.metadata.context_metadata
```

This boundary ensures:

- **bounded context**  
- **canonical ordering**  
- **deterministic normalization**  
- **provenance correctness**  
- **atomic commit**  
- **replay determinism**

CE produces the **canonical context envelope**, and TPU commits it into the TP.

## **4.1 CE Writes**

CE writes:

```
TP.metadata.context {
    context_fields
    relevance_flags
    copy_forward_flags
    reset_flags
    context_provenance
    extraction_audit
    ce_version_tag
}
```

CE is **pre‑semantic**, **bounded**, **deterministic**, and **non‑inferential**.

## **4.2 TPU Commits**

TPU:

- validates writer authority  
- enforces boundedness (10/100/4 clarifying limits)  
- canonical‑orders fields  
- appends provenance  
- commits atomically  
- guarantees replay determinism  

After TPU commit, CE metadata becomes **immutable**.

---

# **5. TP Envelope Details**

Below is a deeper explanation of each envelope.

---

## **5.1 Identity Block**

Defines:

- TP ID  
- sequence number  
- cycle  
- lane  
- schema version  
- policy signature  

Immutable after creation.

---

## **5.2 Semantic Envelope**

Carries:

- propositions  
- truth evidence  
- semantic tags  

Used by TR and IdOB for meaning refinement.

---

## **5.3 Context Envelope (Raw)**

Produced by CEx‑Pck:

- topic  
- stance  
- intent  
- register  
- politeness  
- tone  
- continuity  
- direction  
- coherence  
- importance  
- clarifying_fields[]  

Consumed by CE.

---

## **5.4 Context Metadata Envelope (CE)**

CE normalizes raw context into:

- canonical fields  
- bounded clarifying metadata  
- deterministic ordering  
- provenance  
- extraction audit  
- version tag  

Committed by TPU.

---

## **5.5 MSL Metadata**

Meaning Signal Layer:

- qualifiers  
- clarifications  
- stance  
- shading  
- intent  
- direction  
- coherence  
- subculture  

Used by IdOB, RB, MCB.

---

## **5.6 Continuity Metadata**

Contains:

- clarifying_fields  
- subfields  
- topology  
- importance  
- provenance  

Used by IdOB, TR, CIL, CST.

Bounded by TPU (10/100/4).

---

## **5.7 Semantic‑Importance Envelope**

Produced by:

- SOB  
- SROB  
- CnOB  
- SmOB  
- IdOB  
- SSRGn  

Consumed by:

- CCR  
- COB  
- CIL  
- CST  
- IdOB  
- RB  

---

## **5.8 CCR Output Envelope**

Contains:

- alignment scores  
- ambiguity  
- collapse  
- drift  
- stability  
- decision  
- selected conversation  

Consumed by CEx‑Pck, COB, CIL.

---

## **5.9 CIL Metadata**

Contains:

- selected_conversation  
- cil_reference  

Used by COB and CIL.

---

## **5.10 Structural Envelope**

Semantic geometry produced by OB‑Set:

- SOB structural map  
- SROB structural map  
- CnOB semantic geometry  
- SmOB semantic geometry  

Consumed by ISc.

---

## **5.11 Routing Metadata**

Produced by RB, RBU, RTU:

- routing_pathway  
- routing_confidence  
- arbitration_trace  
- routing_features  

Consumed by TR and IdOB.

---

## **5.12 Provenance Metadata**

TPU writes:

- commit_id  
- commit_sequence  
- primitive_origin  
- commit_timestamp  
- commit_lineage  

Immutable after commit.

---

## **5.13 Entropy Metadata**

Produced by TR and OuBA:

- ΔH%  
- entropy_trace  
- entropy_commit_map  

Consumed by OuBA.

---

## **5.14 Freeze Metadata**

Produced by SSRGn:

- freeze_signature  
- rrw_binding  
- policy_signature  
- ssr_projection_map  
- freeze_provenance  

Consumed by OuBA.

---

# **6. TP Field Producer/Consumer Table**

This table gives you a complete “feel” for who writes and who reads each envelope.

| Envelope | Written By | Read By |
|---------|------------|---------|
| Identity | InB | All |
| Semantic | IE, OB‑Set | TR, IdOB |
| Raw Context | CEx‑Pck | CE |
| CE Metadata | CE → TPU | IdOB, TR, RB, CIL, CST |
| MSL | CEx‑Pck | IdOB, RB, MCB |
| Continuity | CE → TPU | IdOB, TR, CIL, CST |
| Semantic‑Importance | OB‑Set, IdOB, SSRGn | CCR, COB, CIL |
| CCR Output | CEx‑CCR | CEx‑Pck, COB, CIL |
| CIL Metadata | CEx‑CCR | COB, CIL |
| Structural | SOB, SROB, CnOB, SmOB | ISc |
| Routing | RB, RBU, RTU | TR, IdOB |
| Provenance | TPU | All |
| Entropy | TR, OuBA | OuBA |
| Freeze | SSRGn | OuBA |

---

# **7. Path‑A Flow Diagram (with CE → TPU boundary)**

```mermaid
flowchart LR
    A[InB] --> B[IIInB]
    B --> C[IE]
    C --> D[CEx-IE]
    D --> E[CEx-CCR]
    E --> F[CEx-Pck]
    F --> G[CE]
    G --> H[TPU]
    H --> I[SOB]
    I --> J[SROB]
    J --> K[CnOB]
    K --> L[SmOB]
    L --> M[ISc]
    M --> N[SSG]
    N --> O[STPX]
    O --> P[RBU]
    P --> Q[RB]
    Q --> R[TR]
    R --> S[CTP]
    S --> T[ISc]
    T --> U[RTU]
    U --> V[RB]
    V --> W[IdOB]
    W --> X[MCB]
    X --> Y[RBU]
    Y --> Z[DCB]
    Z --> AA[RB]
    AA --> AB[TR]
    AB --> AC[CTP]
    AC --> AD[ISc]
    AD --> AE[RTU]
    AE --> AF[RB]
    AF --> AG[OuBA]
```

The CE → TPU boundary is the **first commit boundary** in Path‑A.

---

# **8. Why the TP Is Designed This Way**

The TP is designed to:

- carry all meaning‑construction signals deterministically  
- preserve provenance across all updates  
- enforce boundedness and canonical ordering  
- support deterministic replay  
- separate pre‑semantic (CE) from commit (TPU)  
- provide stable metadata for downstream primitives  
- maintain identity continuity  
- support CCR decision logic  
- support CIL substrate selection  
- support structural geometry  
- support routing and arbitration  
- support truth‑relation mapping  
- support freeze and final commit  

Every envelope exists for a specific architectural reason.

---

# **9. Conclusion**

This white paper restores the intuitive feel for the TP:

- how it is structured,  
- why each envelope exists,  
- who writes each field,  
- who reads each field,  
- and how CE and TPU form the deterministic commit boundary.

The TP is the **semantic backbone** of Path‑A — the single, authoritative, replay‑safe carrier of meaning, context, identity, structure, routing, provenance, and entropy.
