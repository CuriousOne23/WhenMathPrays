# **Path A — IdOB Invariant Independence Justification**  
### *Why Parallel IdOB Is Safe, Why CTP Can Be Simple, and Why Path A Doesn’t Collapse Under Parallelism*

---

## **1. Introduction**

Path A supports **parallel IdOB execution**, meaning multiple IdOB instances may operate simultaneously on different referents. This parallelism is only safe if the **invariants governing TP evolution are independent by construction**.

This paper explains:

- why IdOB deltas are **field‑local**,  
- why Path A invariants are **mostly independent**,  
- why any overlap is **conceptual, not write‑domain**,  
- why CTP-after-TR is **viable**,  
- and why Path A remains **deterministic and replayable** under parallel IdOB.

This document reconstructs the architectural reasoning originally developed informally during the design of IdOB and CTP.

---

## **2. The Role of IdOB in Path A**

IdOB is the primitive responsible for:

- constructing meaning envelopes,  
- updating referent‑local semantic fields,  
- producing semantic deltas,  
- and contributing to the TP evolution for a single referent.

A key design choice:

> **Each IdOB instance operates on exactly one referent.**

This referent‑locality is the foundation for independence.

---

## **3. Delta Locality: The Core Independence Mechanism**

IdOB deltas are **field‑local**:

- They write only to meaning‑layer fields.  
- Meaning‑layer fields are partitioned by referent.  
- Each IdOB instance writes only to the fields belonging to its referent.  
- No two IdOBs write to the same TP region.

This ensures:

- **no write collisions**,  
- **no semantic merge conflicts**,  
- **no ordering dependencies**,  
- **no need for semantic arbitration in CTP**.

This is the single most important structural guarantee in Path A.

---

## **4. Invariant Partitioning**

Path A invariants fall into three categories:

### **4.1 Structural Invariants**
These govern:

- adjacency,  
- geometric_state,  
- routing substrate,  
- TP container shape.

They operate on **routing‑layer and geometric fields**, not meaning‑layer fields.

### **4.2 Semantic Invariants**
These govern:

- meaning envelopes,  
- referent maps,  
- truth‑state evolution.

They operate on **meaning‑layer fields**, partitioned by referent.

### **4.3 Safety Invariants**
These govern:

- replayability,  
- monotonicity,  
- corruption‑proofing.

They operate on **global TP constraints**, but do not write to meaning‑layer fields.

---

## **5. Conceptual vs Write‑Domain Overlap**

Some invariants may **conceptually overlap** — e.g., a structural invariant may care about adjacency constraints that indirectly relate to meaning envelopes.

But conceptual overlap is allowed.

What is forbidden is **write‑domain overlap**:

- Structural invariants write to routing/geometric fields.  
- Semantic invariants write to meaning‑layer fields.  
- Safety invariants write to global metadata fields.

This strict separation ensures independence.

---

## **6. Why Parallel IdOB Is Safe**

Parallel IdOB is safe because:

1. **Each IdOB writes to a disjoint referent‑local region.**  
2. **No two IdOBs write to the same TP fields.**  
3. **Structural invariants do not write to meaning‑layer fields.**  
4. **Safety invariants do not write to meaning‑layer fields.**  
5. **Semantic invariants are referent‑local and therefore non‑overlapping.**

Thus:

> **Parallel IdOB produces independent deltas by construction.**

This is not an emergent property — it is a design guarantee.

---

## **7. Why CTP Can Be Simple**

CTP sits after TR and performs:

- collection of deltas,  
- mechanical merge,  
- freeze of TP snapshot,  
- handoff to RB.

CTP is intentionally **non‑semantic**:

- It does not resolve conflicts.  
- It does not inspect routing context.  
- It does not arbitrate between invariants.  
- It does not re-run TR.

CTP can remain simple **only because**:

> **IdOB deltas are independent and invariants do not write to overlapping TP regions.**

If invariants overlapped heavily, CTP would need semantic logic — which would violate its definition.

---

## **8. Why CTP-After-TR Is Viable**

CTP-after-TR is viable because:

- TR resolves all routing‑layer decisions before CTP.  
- IdOB deltas do not affect routing‑layer fields.  
- CTP only merges meaning‑layer deltas and structural updates already finalized by TR.  
- No invariant requires CTP to inspect routing context.

Thus:

> **CTP-after-TR is not just allowed — it is the only placement that preserves determinism.**

---

## **9. Consequences if Invariants Were Not Independent**

If invariants were not independent:

- IdOB deltas could collide.  
- CTP would need semantic arbitration.  
- Merge ordering would matter.  
- Replayability would break.  
- TR would need to re-run after CTP.  
- Path A would collapse under parallelism.

This is why independence is not optional — it is foundational.

---

## **10. Summary**

Path A supports parallel IdOB because:

- IdOB deltas are referent‑local,  
- invariants are partitioned by write‑domain,  
- conceptual overlap does not imply write‑domain overlap,  
- CTP merges only independent deltas,  
- TR resolves routing before CTP,  
- and CTP remains simple and deterministic.

This architectural structure ensures that Path A remains stable, replayable, and scalable under parallel execution.

---
