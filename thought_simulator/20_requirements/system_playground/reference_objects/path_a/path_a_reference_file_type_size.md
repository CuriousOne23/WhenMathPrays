# path_a_reference_file_type_size.md

**Document ID:** 20.XXX_path_a_reference_file_type_size  
**Version:** 0.1  
**Date:** 2026-07-09  
**Status:** Draft — Reference Paper (Path A)  

---

## 1. Purpose & Scope

This paper provides realization engineers with guidance on Path A reference file types and sizes. It defines expectations, constraints, and scaling behavior for maintaining compact, readable, and maintainable reference files.

---

## 2. File Type Requirements

Path A reference files use YAML-compatible structured text. YAML supports readability, expandability, diff-friendliness, and version control. Binary formats, embedded corpora, or model weights are inappropriate for Path A reference files.

---

## 3. Why Path A Files Stay Small

Path A files encode rules rather than knowledge. Symbolic rules scale logarithmically with system richness. Geometry definitions and invariants saturate quickly. Examples remain bounded and do not cause file expansion.

---

## 4. Back-Annotating Frontier AI Richness to Path A

Frontier LLM performance can be back-annotated into Path A symbolic expressivity through rule refinement and geometry constraints. Even frontier-level expressivity results in MB-scale files because Path A stores deterministic rules and geometry rather than weights, embeddings, or corpora. IdOB-defined objects do not cause bloat because IdOB stores refinement rules rather than object databases.

---

## 5. Expected File Sizes

Typical Path A files range from 20–60 KB. Expanded files reach 100–200 KB. Frontier-parallel Thought Simulator files range from 0.5–2 MB per file. The full Path A suite totals 2.5–10 MB.

---

## 6. IdOB/RBU Scaling Behavior

IdOB and RBU store rules for identity-conditioned meaning refinement rather than objects, corpora, embeddings, or ontologies. Meaning geometry expansion remains compact because it encodes deterministic refinement operators and manifold charts rather than instance data.

---

## 7. Routing Geometry Scaling Behavior

RTU and RB routing invariants saturate quickly. Routing logic does not grow with model size because it operates on normalized signatures and bounded entropy scores. Entropy scoring and termination envelopes remain compact.

---

## 8. When to Split or Refactor Files

Split files when size exceeds 2 MB, readability degrades, invariants become excessive, examples proliferate, or diffs become noisy.

---

## 9. Engineering Guidance for Maintaining File Size

Keep examples minimal. Avoid redundant geometry definitions. Use references instead of duplication. Maintain consistent YAML patterns. Avoid embedding large data structures.

---

## 10. Canonical Starter Example

```yaml
# Path A Reference File Starter
document_id: "20.XXX_example"
version: "0.1"
date: "2026-07-09"
status: "Draft"
purpose: "Example reference file"

geometry:
  type: "structural"
  invariants:
    - monotonic_accumulation
    - replay_equivalence

examples:
  - input: "..."
    output: "..."
```

**End of path_a_reference_file_type_size.md**
```
