# **TS Theory — Overview & Reading Guide**

A structured collection of documents defining the theoretical foundations, architectural design, and primitive mechanisms of the Thought Simulator (TS).  
This directory is organized to help readers understand:

- **What TS believes** (theories)  
- **How TS works** (architecture)  
- **What TS is built from** (primitives)  
- **Why TS exists** (essays on hard problems)

---

## **Directory Structure**

TS theory documents fall into four conceptual groups:

| Group | Prefix | Purpose |
|-------|--------|---------|
| **Core Theories** | `ts_` | Formal definitions of meaning, identity, and continuity |
| **Architecture Documents** | `tp_architecture*` | How the theories become a working cognitive pipeline |
| **Theory Primitives** | `tp_` | The mechanisms that implement the architecture |
| **Essays / Foundations** | *(none)* | Deep dives into foundational problems (e.g., meaning) |

This structure mirrors the TS design philosophy:  
**Theory → Architecture → Primitives → Application.**

---

## **1. Core Theories (`ts_`)**

These documents define the *formal theoretical backbone* of TS.  
They should be read first.

| File | Summary |
|------|---------|
| [ts_meaning_theory.md](ts_meaning_theory.md) | Defines meaning as a structured, canonical, replay‑safe object; introduces the meaning state vector and raw→canonical mapping |
| [ts_identity_theory.md](ts_identity_theory.md) | Defines identity as a stable, continuity‑driven cognitive object; explains identity continuity and identity‑conditioned meaning |
| [ts_continuity_theory.md](ts_continuity_theory.md) | Defines continuity as the relationship between meaning states across turns; explains how TS maintains coherence over time |

These three papers form the **TS Theory Triad**.

---

## **2. Architecture Documents (`tp_architecture*`)**

These documents explain **how the theories become a working machine**.

| File | Summary |
|------|---------|
| [tp_architecture.md](tp_architecture.md) | The architectural bridge between theory and primitives; explains TP layers, commit boundaries, identity/continuity propagation, SSR freeze |
| [tp_architecture_appendix.md](tp_architecture_appendix.md) | Diagrams, lineage maps, commit maps, and mermaid flows that visualize the TP architecture |

These should be read **after** the core theories and **before** the primitives.

---

## **3. Theory Primitives (`tp_`)**

These documents describe the **mechanisms** that implement the architecture.  
Each primitive isolates one conceptual responsibility.

| File | Summary |
|------|---------|
| [tp_state.md](tp_state.md) | Defines the TS notion of state; the foundation for all transitions |
| [tp_description.md](tp_description.md)| Describes how states and meaning are represented and transformed through the TP |
| [tp_context_layer.md](tp_context_layer.md)| Defines the context layer and how context shapes meaning and identity |
| [tp_identity_basin.md](tp_identity_basin.md)| Introduces identity basins — attractor regions that stabilize identity |
| [tp_commit.md](tp_commit.md)| Defines commit semantics — how meaning becomes fixed, replay‑safe, and immutable |
| [tp_coordination.md](tp_coordination.md)| Explains multi-agent coordination and alignment across identity/meaning spaces |
| [tp_routing.md](tp_routing.md)| Defines routing — how meaning moves through the TP deterministically |
| [tp_routing_matrix.md](tp_routing_matrix.md)| The formal routing topology; reference document for routing decisions |
| [tp_path_a_map.md](tp_path_a_map.md)| A map of Path‑A (meaning construction) showing how primitives compose into a deterministic pipeline |

These documents are the **operational vocabulary** of TS.

---

## **4. Essays / Foundations**

| File | Summary |
|------|---------|
| [difficulty_of_meaning.md](difficulty_of_meaning.md) | Explains why meaning is hard, why canonicalization is required, and why TS cannot rely on embeddings or emergent semantics |

This essay provides the **motivation** for the entire TS architecture.

---

# **Suggested Reading Order**

This reading order is optimized for understanding TS as a coherent system.

---

## **Phase 1 — Core Theory (Start Here)**  
1. [ts_meaning_theory.md](ts_meaning_theory.md)  
2. [ts_identity_theory.md](ts_identity_theory.md)  
3. [ts_continuity_theory.md](ts_continuity_theory.md)

These three papers define the *what* and *why* of TS.

---

## **Phase 2 — Architecture (The Bridge)**  
4. [tp_architecture.md](tp_architecture.md)  
5. [tp_architecture_appendix.md](tp_architecture_appendix.md)

These explain *how* the theories become a working cognitive pipeline.

---

## **Phase 3 — Primitives (The Machinery)**  
6. [tp_state.md](tp_state.md)  
7. [tp_description.md](tp_description.md)  
8. [tp_context_layer.md](tp_context_layer.md)  
9. [tp_identity_basin.md](tp_identity_basin.md)  
10. [tp_commit.md](tp_commit.md)  
11. [tp_coordination.md](tp_coordination.md)  
12. [tp_routing.md](tp_routing.md)  
13. [tp_routing_matrix.md](tp_routing_matrix.md) 
14. [tp_path_a_map.md](tp_path_a_map.md)

These documents show how TS actually works internally.

---

## **Phase 4 — Foundations / Deep Problem**  
15. [difficulty_of_meaning.md](difficulty_of_meaning.md)

Best read after the full system is understood.

---

# **Notes**

- **`ts_` documents** define the *theory*.  
- **`tp_architecture*` documents** define the *architecture*.  
- **`tp_` documents** define the *mechanisms*.  
- **Essays** define the *motivation*.

Together, they form the complete TS theory stack.

---
