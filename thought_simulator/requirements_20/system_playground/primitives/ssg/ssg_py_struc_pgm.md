# **ssg_py_struc_pgm.md — Structural Program for SSG (Python Implementation Scaffold)**
### *Aligned with revised 20.47_ssg_prim.md and Path‑A progressive lineup testing*
### *Informative — Implementation Guidance Only*

---

# **1. Purpose**

`ssg.py` implements the **Structural Signature Generator (SSG‑prm)** as defined in **20.47**.

SSG’s structural program:

- consumes **only** the SmOB structural graph and structural‑adjacent metadata  
- computes **five structural invariant families**  
- assembles a **fixed‑length vector** in $\mathbb{R}^d$  
- performs **L2 normalization**  
- writes **only** the four SSG‑owned TP fields:  
  - `tp.ssg_signature`  
  - `tp.ssg_layer_bitmap`  
  - `tp.ssg_reason_code`  
  - `tp.ssg_status`  
- obeys **primitive boundary discipline**  
- supports **deterministic replay**  
- supports **progressive lineup testing**  
- produces **no semantic‑layer fields**  
- produces **no manifold geometry**  
- produces **no routing geometry**  
- produces **no semantic‑adjacent signals**

This scaffold ensures that:

- `ssg.py` can be implemented deterministically  
- `ssg_testbench.py`, `ssg_testbench.yaml`, `ssg_rulechecker.py`, and `ssg_input.yaml` can be written directly  
- C++ parity implementations can be validated  
- Path‑A routing (RB‑prm) receives a correct structural coordinate chart

---

# **2. Inputs and Outputs**

## **2.1 Inputs (read‑only)**

`ssg.py` consumes **only structural inputs**, consistent with 20.47.

### **SmOB structural graph**

The SmOB structural graph is represented in TP as:

- `tp["metadata"]["residue"]["structural_residue"]`  
- `tp["metadata"]["residue"]["refinement_residue"]`  
- `tp["metadata"]["residue"]["constraint_residue"]`  
- `tp["metadata"]["residue"]["semantic_adjacent_residue"]`  
- `tp["metadata"]["residue"]["presemantic_hash"]`  
- `tp["metadata"]["residue"]["residue_provenance"]`

These fields together encode:

- nodes (residue units)  
- arcs (directed structural relations)  
- labels (constraint families, roles, adjacency types)

### **Structural‑adjacent metadata**

Read‑only, used only when relevant to invariant extraction:

- continuity metadata (COB, CIL, CST)  
- expressive metadata (IIInB, IE)  
- normalization metadata (IE)  
- provenance metadata  
- lineage metadata  
- entropy/signature histories

### **Forbidden inputs**

SSG must **not** read:

- `tp.metadata.semantic_layer.*`  
- routing metadata  
- semantic ΔH%  
- truth/done fields  
- identity metadata  
- meaning metadata  
- `tp.semantic.*`  
- `tp.context.*`  
- `tp.intake.*`  
- any Pipeline‑B envelopes

This matches 20.47’s approved inputs and forbidden reads.

---

## **2.2 Outputs (SSG‑owned fields only)**

`ssg.py` writes **only**:

- `tp.ssg_signature`        — `float[d]` structural signature  
- `tp.ssg_layer_bitmap`     — 4‑bit OB‑layer contribution mask  
- `tp.ssg_reason_code`      — enum `{FULL, PARTIAL, EMPTY}`  
- `tp.ssg_status`           — enum `{OK, MISSING_INPUT, DEGENERATE, PARTIAL}`  

No other TP fields may be modified.

This ensures:

- deterministic replay  
- primitive boundary discipline  
- compatibility with STPX, TR, RB, IdOB, RBU  
- compatibility with progressive lineup testing

---

# **3. High‑Level Program Structure**

`ssg.py` follows a **single entrypoint** pattern:

```python
PRIMITIVE_NAME = "SSG"

def run(tp):
    """
    Structural Signature Generator (SSG) entrypoint.

    Args:
        tp: Thought Packet (mutable).

    Returns:
        tp: Updated TP with SSG-owned fields set.
    """
    inputs = _extract_ssg_inputs(tp)
    invariants = _compute_structural_invariants(inputs)
    signature, bitmap, reason_code, status = _assemble_signature(invariants)
    _write_ssg_outputs(tp, signature, bitmap, reason_code, status)
    _record_provenance(tp)
    return tp
```

Helper functions:

```python
def _extract_ssg_inputs(tp):
    # Read SmOB structural graph + structural-adjacent metadata (read-only)
    # Return structured input bundle (graph + metadata)

def _compute_structural_invariants(inputs):
    # Compute f1..f5 invariant families from the structural graph
    # Return dict: {"f1": ..., "f2": ..., "f3": ..., "f4": ..., "f5": ...}

def _assemble_signature(invariants):
    # Concatenate invariants into phi(G)
    # Compute L2-normalized signature sigma
    # Compute layer bitmap, reason_code, status
    # Return (signature, bitmap, reason_code, status)

def _write_ssg_outputs(tp, signature, bitmap, reason_code, status):
    # Write SSG-owned fields only
    # No other TP fields may be modified

def _record_provenance(tp):
    # Append ssg_ref to exec_trace (per 20.47)
```

This structure is:

- deterministic  
- testbench‑friendly  
- C++‑parity‑friendly  
- aligned with 20.47 HLRs

---

# **4. Structural Invariant Computation**

SSG computes the five invariant families defined in 20.47.

Let $G$ be the SmOB structural graph.

### **Arc patterns ($f_1$)**

Normalized frequency distribution over arc labels:

- define a fixed arc‑label vocabulary $\mathcal{L}_E$  
- count occurrences of each label  
- normalize by total arc count

### **Binding depth ($f_2$)**

Maximum and mean depth of directed binding chains:

- traverse binding chains from roots  
- compute depth per chain  
- aggregate (max, mean)

### **Residue entropy ($f_3$)**

Shannon entropy over residue‑address distribution:

- define residue addresses (e.g., segment IDs, constraint IDs)  
- compute $p_i$ over addresses  
- entropy:

$$
H = -\sum_i p_i \log p_i
$$

### **Curvature ($f_4$)**

Cycle density and clustering coefficient:

- cycle density: ratio of nodes in cycles to total nodes  
- clustering coefficient: standard graph clustering metric over residue graph

### **Motif frequencies ($f_5$)**

Normalized counts of canonical structural motifs:

- define a fixed motif catalog (e.g., chains, forks, cycles, bridges)  
- count motif instances  
- normalize by graph size

These are concatenated:

$$
\varphi(G) = [\, f_1(G) \ \|\ f_2(G) \ \|\ f_3(G) \ \|\ f_4(G) \ \|\ f_5(G) \,]
$$

Then normalized:

$$
\sigma = \frac{\varphi(G)}{\lVert \varphi(G) \rVert_2}
$$

If $\varphi(G) = \mathbf{0}$, then:

$$
\sigma = \mathbf{0}
$$

`tp.ssg_signature` is set to $\sigma$.

Dimension $d$ is fixed by:

- arc‑label vocabulary size  
- binding‑depth feature count  
- entropy feature count  
- curvature feature count  
- motif catalog size  

and must be held constant across implementations.

---

# **5. Layer Bitmap, Reason Code, Status**

### **Layer bitmap**

Bits correspond to OB layers:

- $L_0 =$ SOB  
- $L_1 =$ SROB  
- $L_2 =$ CnOB  
- $L_3 =$ SmOB  

For each layer $L_i$, define $\varphi_i(G_{L_i})$ as the invariant subvector contributed by that layer.

$$
b_i =
\begin{cases}
1 & \varphi_i(G_{L_i}) \neq \mathbf{0} \\
0 & \text{otherwise}
\end{cases}
$$

Bitmap:

$$
\text{bitmap} = \sum_{i=0}^{3} b_i \cdot 2^i
$$

### **Reason code**

- `FULL`    — all layers contributed invariants (`bitmap == 0b1111`)  
- `PARTIAL` — some layers contributed zero (`bitmap` in `0b0001`–`0b1110`)  
- `EMPTY`   — no invariants present (`bitmap == 0b0000`)

### **Status**

- `OK`             — valid input, non‑degenerate invariants  
- `MISSING_INPUT`  — SmOB structural graph absent/invalid  
- `DEGENERATE`     — $\lVert \varphi(G) \rVert_2 = 0$ but graph non‑empty  
- `PARTIAL`        — valid but some layers absent

Status logic must match 20.47 failure‑mode HLRs.

---

# **6. Primitive Boundary Discipline**

`ssg.py` must enforce:

- **read‑only** access to all upstream fields  
- **write‑only** access to `tp.ssg_signature`, `tp.ssg_layer_bitmap`, `tp.ssg_reason_code`, `tp.ssg_status`  
- **no semantic‑layer writes**  
- **no routing‑layer writes**  
- **no meaning‑layer writes**  
- **no identity‑layer writes**  
- **no cue extraction**  
- **no manifold geometry**  
- **no semantic_adjacent_signals**  
- **no referent_adjacent_signals**  
- **no modality/stance cues**

This keeps SSG purely structural and preserves downstream responsibilities (STPX, TR, RB, IdOB, RBU).

---

# **7. Determinism, Replay, and Testbench Compatibility**

`ssg.py` must:

- produce identical outputs for identical inputs  
- avoid randomness and non‑deterministic ordering  
- use stable sorting for any canonicalization  
- use pure functions for invariant computation  
- record provenance deterministically (`ssg_ref` in `exec_trace`)  

The SSG testbench will verify:

- correct signature computation  
- correct bitmap formation  
- correct reason code  
- correct status  
- correct provenance  
- correct primitive boundaries  
- correct nested path usage  
- replay determinism across runs

---

# **8. Error Handling**

`ssg.py` must:

- raise clear exceptions (`ValueError`, `KeyError`) for malformed TP structures  
- set `tp.ssg_status = MISSING_INPUT` when SmOB output is absent or invalid  
- set `tp.ssg_status = DEGENERATE` when $\lVert \varphi(G) \rVert_2 = 0$ but graph is non‑empty  
- never silently repair or smooth structural errors

---

# **9. Relationship to Other Artifacts**

This document is the implementation scaffold for:

- `20.47_ssg_prim.md` (normative SSG primitive)  
- `progressive_lineup_testing.md` (testbench discipline)  
- `ssg.py` (Python implementation)  
- `ssg_testbench.py` / `ssg_testbench.yaml` (deterministic tests)  
- `ssg_rulechecker.py` (rule enforcement)  
- `ssg_input.yaml` (fixtures)

It ensures that all SSG artifacts can be written deterministically and consistently, without semantic‑layer leakage.

---

# **End of Document — ssg_py_struc_pgm.md (Unified Structural‑Only Rewrite)**
```
