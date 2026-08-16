# **ssg_py_struc_pgm.md**  
### *Structural Program for SSG — Python Implementation Scaffold*  
### *Aligned with 20.47_ssg_prim.md, theoretical_utility_of_ssg.md, ts_meaning_theory.md, and Path‑A Progressive Lineup Testing*

---

## **1. Purpose of ssg.py**

`ssg.py` implements the **Structural Signal Generator (SSG)** primitive in Python.

SSG’s structural program:

- consumes **SmOB’s pre‑semantic residue and cue vector**  
- integrates **read‑only TP metadata** (context, MSL, continuity, identity, semantic‑importance, semantic‑residue, CCR, CIL)  
- constructs a **deterministic structural manifold**  
- freezes **structural entropy**  
- produces **geometric invariants** for routing, scoring, continuity, and identity  
- writes into **TP.metadata.semantic_layer_metadata** and SSG‑owned fields only  
- obeys **primitive boundary discipline**, **provenance rules**, and **deterministic replay** requirements

`ssg.py` is the Python reference implementation used by:

- Path‑A progressive lineup testing  
- parity checks against future C++ implementations  
- deterministic testbench runs under `testbenches/path_a/structure/ssg_testbench.*`  

---

## **2. Inputs and Outputs**

### **2.1 Inputs (from TP and SmOB)**

`ssg.py` consumes:

- **SmOB outputs** (owned by OB‑Set, read‑only to SSG):  
  - `TP.metadata.residue.structural_residue`  
  - `TP.metadata.residue.refinement_residue`  
  - `TP.metadata.residue.constraint_residue`  
  - `TP.metadata.residue.semantic_adjacent_residue`  
  - `TP.metadata.residue.presemantic_hash`  
  - `TP.metadata.residue.residue_provenance`  

- **Constraint lineage (via SmOB, read‑only):**  
  - CnOB constraint families (C1–C7)  
  - constraint importance and residue (encoded upstream)  

- **Context and MSL (read‑only):**  
  - `TP.metadata.context.*`  
  - `TP.metadata.msl.*`  

- **Continuity and identity (read‑only):**  
  - `TP.metadata.continuity_*`  
  - `TP.metadata.identity.*`  

- **Semantic‑importance (read‑only):**  
  - `TP.semantic.importance.entities[]`  
  - `TP.semantic.importance.facts[]`  

- **Semantic‑residue alignment (read‑only):**  
  - `TP.metadata.semantic_residue.entities[]`  
  - `TP.metadata.semantic_residue.facts[]`  
  - `TP.metadata.semantic_residue.alignment_scores`  

- **CCR output (read‑only):**  
  - `TP.cex.ccr.alignment.*`  
  - `TP.cex.ccr.scores.*`  
  - `TP.cex.ccr.decision`  
  - `TP.cex.ccr.selected_conversation`  

- **CIL substrate metadata (read‑only):**  
  - `TP.metadata.cil.selected_conversation`  
  - `TP.metadata.cil.cil_reference`  

- **Provenance (read‑only):**  
  - `TP.metadata.provenance.*`  

All inputs are accessed via **canonical nested TP paths** (no `TP.` prefix in code; the TP object is passed in).

---

### **2.2 Outputs (SSG‑owned fields)**

`ssg.py` writes only SSG‑owned fields:

- **Semantic layer metadata (20.105.010):**  
  - `TP.metadata.semantic_layer.semantic_adjacent_signals`  
  - `TP.metadata.semantic_layer.semantic_layer_hash`  
  - `TP.metadata.semantic_layer.referent_adjacent_signals`  
  - `TP.metadata.semantic_layer.modality_stance_cues`  
  - `TP.metadata.semantic_layer.semantic_layer_provenance`  

- **Optional SSG‑specific structural manifold fields (if defined in 20.47):**  
  - `TP.metadata.semantic_layer.structural_manifold_geometry`  
  - `TP.metadata.semantic_layer.structural_manifold_hash`  
  - `TP.metadata.semantic_layer.routing_eligibility_geometry`  

All outputs:

- are **deterministic**  
- are **bounded**  
- are **replay‑safe**  
- record **provenance** (`origin = SSG`, `last_update = SSG`, commit lineage via TPU)  
- obey **immutability after TPU commit**

---

## **3. High‑Level Program Structure**

`ssg.py` follows a **single entrypoint** pattern:

```python
PRIMITIVE_NAME = "SSG"

def run(tp):
    """
    Structural Signal Generator (SSG) entrypoint.

    Args:
        tp: Thought Packet object (mutable), carrying metadata and residue fields.

    Returns:
        tp: Updated Thought Packet with SSG semantic_layer_metadata fields set.
    """
    # 1. Extract inputs (SmOB residue + TP metadata)
    # 2. Build structural manifold
    # 3. Freeze structural entropy (canonicalization)
    # 4. Compute semantic_layer_hash and geometric invariants
    # 5. Write SSG-owned fields into TP.metadata.semantic_layer_*
    # 6. Record provenance
    # 7. Return updated TP
```

The structural program is organized into **pure helper functions**:

```python
def _extract_ssg_inputs(tp):
    # Read SmOB residue and TP metadata (read-only)
    # Return a structured input bundle

def _build_structural_manifold(inputs):
    # Construct manifold from residue, constraints, context, continuity, identity
    # Return manifold object

def _freeze_structural_entropy(manifold):
    # Canonicalize ordering, adjacency, constraint families
    # Return frozen manifold

def _compute_geometric_invariants(frozen_manifold):
    # Compute semantic_layer_hash, adjacency signals, referent signals, modality/stance cues
    # Return invariants dict

def _write_ssg_outputs(tp, invariants):
    # Write SSG-owned fields into TP.metadata.semantic_layer_*
    # Do not modify upstream fields
    # Return updated TP

def _record_provenance(tp):
    # Set origin = SSG, last_update = SSG, update commit lineage placeholder
    # Return updated TP
```

`run(tp)` orchestrates these steps in order.

---

## **4. Invariants and Constraints**

`ssg.py` must enforce the following invariants:

- **Determinism:**  
  - Same TP input → same SSG outputs.  
  - No randomness, no sampling, no non‑deterministic ordering.

- **Primitive boundaries:**  
  - Read‑only: all upstream fields (SmOB, CnOB, SROB, SOB, context, MSL, continuity, identity, semantic‑importance, semantic‑residue, CCR, CIL).  
  - Write‑only: SSG‑owned semantic_layer_metadata fields.  
  - No modification of semantic‑importance, semantic‑residue, CCR output, CIL metadata, context, MSL, continuity, identity, routing, scoring, freeze metadata.

- **Canonical nested paths:**  
  - Use `tp["metadata"]["semantic_layer"]["..."]` style access.  
  - No `TP.` prefix in code; TP is the object.

- **Replay safety:**  
  - Outputs must be stable across runs.  
  - Hashes must be deterministic functions of inputs.

- **Boundedness:**  
  - Manifold representation must be small, laptop‑scale.  
  - No unbounded embeddings or large tensors.

- **Provenance discipline:**  
  - `semantic_layer_provenance.origin = "SSG"`  
  - `semantic_layer_provenance.last_update = "SSG"`  
  - TPU later appends commit identifiers and lineage.

---

## **5. Structural Manifold Construction (Conceptual Outline)**

The structural manifold is built by:

1. **Integrating SmOB residue:**  
   - structural_residue  
   - refinement_residue  
   - constraint_residue  
   - semantic_adjacent_residue  
   - presemantic_hash  

2. **Integrating constraint families (C1–C7):**  
   - adjacency constraints  
   - ordering constraints  
   - identity/continuity constraints  
   - semantic‑adjacent constraints  

3. **Integrating contextual metadata:**  
   - topic, stance, direction, coherence, importance  
   - continuity flags, identity anchors, referent lineage  
   - MSL qualifiers, clarifications, shading, intent  

4. **Constructing manifold:**  
   - nodes: structural units (segments, constraints, cues)  
   - edges: adjacency, ordering, continuity relations  
   - labels: constraint families, semantic‑adjacent roles, importance  

The manifold is then **canonicalized**:

- sorted by stable keys (e.g., segment index, constraint family, importance)  
- adjacency lists normalized  
- referent and identity links stabilized  
- conflict and underspecification signals encoded deterministically  

---

## **6. Geometric Invariants**

From the frozen manifold, `ssg.py` computes:

- `semantic_layer_hash`  
  - a deterministic hash of the manifold structure and labels  

- `semantic_adjacent_signals`  
  - signals indicating semantic‑adjacent structure (e.g., emphasis, contrast, hedging)  

- `referent_adjacent_signals`  
  - signals indicating referent continuity, shifts, or ambiguity  

- `modality_stance_cues`  
  - signals indicating modality (possibility, necessity) and stance (agreement, doubt, critique)  

These invariants are written into `TP.metadata.semantic_layer_*` and consumed downstream by:

- STPX  
- RBU  
- TR  
- RB  
- IdOB  
- WrdNm → ISc  
- refinement loop  

---

## **7. Error Handling and Testbench Integration**

`ssg.py` must:

- **Fail loudly** on malformed TP structures (missing required fields, wrong types).  
- Use **simple, explicit exceptions** (e.g., `ValueError`, `KeyError`) with clear messages.  
- Avoid silent failure or implicit defaulting that hides structural problems.

The deterministic testbench under:

```
testbenches/path_a/structure/ssg_testbench.py
testbenches/path_a/structure/ssg_testbench.yaml
```

will:

- feed known TP fixtures into `run(tp)`  
- assert deterministic outputs  
- assert correct provenance  
- assert primitive boundary discipline  
- assert correct nested path usage  
- assert replay determinism across runs  

---

## **8. Relationship to Other Artifacts**

`ssg_py_struc_pgm.md` is the structural program specification for:

- `20.47_ssg_prim.md` (normative primitive requirements)  
- `theoretical_utility_of_ssg.md` (architectural and meaning‑theory role)  
- `ts_meaning_theory.md` (meaning = stated × context; SSG encodes context)  
- `progressive_lineup_testing.md` (testing framework and primitive discipline)  

It is the **bridge** between theory and implementation, ensuring that `ssg.py`:

- respects Path‑A invariants  
- respects meaning theory constraints  
- remains testable, inspectable, and revisable  
- supports laptop‑scale deterministic cognition.

---

