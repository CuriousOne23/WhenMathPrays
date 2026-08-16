# **ssg_py_struc_pgm.md — Structural Program for SSG (Python Implementation Scaffold)**  
### *Aligned with revised 20.47_ssg_prim.md and Path‑A progressive lineup testing*  
### *Informative — Implementation Guidance Only*

---

# **1. Purpose**

`ssg.py` implements the **Structural Signature Generator (SSG‑prm)** as defined in **20.47**.

SSG’s structural program:

- consumes **only** the SmOB structural graph and structural‑adjacent metadata  
- computes **five structural invariant families**  
- assembles a **fixed‑length vector**  
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

`ssg.py` consumes **only structural inputs**, consistent with 20.47:

### **SmOB structural graph**
- `tp.metadata.residue.structural_residue`  
- `tp.metadata.residue.refinement_residue`  
- `tp.metadata.residue.constraint_residue`  
- `tp.metadata.residue.semantic_adjacent_residue`  
- `tp.metadata.residue.presemantic_hash`  
- `tp.metadata.residue.residue_provenance`

### **Structural‑adjacent metadata**
- continuity metadata (COB, CIL, CST)  
- expressive metadata (IIInB, IE)  
- normalization metadata (IE)  
- provenance metadata  
- lineage metadata  
- entropy/signature histories

### **Forbidden inputs**
SSG must **not** read:

- semantic_layer_metadata  
- routing_metadata  
- semantic ΔH%  
- truth/done fields  
- identity metadata  
- meaning metadata  
- TP.semantic.*  
- TP.context.*  
- TP.intake.*  
- any Pipeline‑B envelopes

This matches 20.47 exactly.

---

## **2.2 Outputs (SSG‑owned fields only)**

`ssg.py` writes **only**:

- `tp.ssg_signature`  
- `tp.ssg_layer_bitmap`  
- `tp.ssg_reason_code`  
- `tp.ssg_status`

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

The structural program is organized into **pure helper functions**:

```python
def _extract_ssg_inputs(tp):
    # Read SmOB structural graph + structural-adjacent metadata (read-only)
    # Return structured input bundle

def _compute_structural_invariants(inputs):
    # Compute f1..f5 invariant families
    # Return dict of invariant vectors

def _assemble_signature(invariants):
    # Concatenate invariants
    # Compute L2 normalization
    # Compute bitmap, reason_code, status
    # Return (signature, bitmap, reason_code, status)

def _write_ssg_outputs(tp, signature, bitmap, reason_code, status):
    # Write SSG-owned fields only
    # No other TP fields may be modified

def _record_provenance(tp):
    # Append ssg_ref to exec_trace
```

This structure ensures:

- deterministic execution  
- testbench compatibility  
- C++ parity  
- clear primitive boundaries

---

# **4. Structural Invariant Computation**

SSG computes the five invariant families defined in 20.47:

### **Arc patterns ($f_1$)**
Normalized frequency distribution over arc labels.

### **Binding depth ($f_2$)**
Maximum and mean depth of directed binding chains.

### **Residue entropy ($f_3$)**
Shannon entropy over residue‑address distribution.

### **Curvature ($f_4$)**
Cycle density and clustering coefficient.

### **Motif frequencies ($f_5$)**
Normalized counts of canonical structural motifs.

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

This matches 20.47 exactly.

---

# **5. Layer Bitmap, Reason Code, Status**

### **Bitmap**
Computed from invariant presence:

$$
b_i =
\begin{cases}
1 & \varphi_i(G_{L_i}) \neq \mathbf{0} \\
0 & \text{otherwise}
\end{cases}
$$

### **Reason Code**
- FULL  
- PARTIAL  
- EMPTY  

### **Status**
- OK  
- MISSING_INPUT  
- DEGENERATE  
- PARTIAL  

All logic matches 20.47.

---

# **6. Primitive Boundary Discipline**

`ssg.py` must enforce:

- **read‑only** access to all upstream fields  
- **write‑only** access to SSG‑owned fields  
- **no semantic‑layer writes**  
- **no routing‑layer writes**  
- **no meaning‑layer writes**  
- **no identity‑layer writes**  
- **no cue extraction**  
- **no manifold geometry**  
- **no semantic_adjacent_signals**  
- **no referent_adjacent_signals**  
- **no modality/stance cues**

This ensures compatibility with:

- STPX (structural cue extractor)  
- TR (meaning‑layer routing vector)  
- RB (relational routing)  
- IdOB (identity‑conditioned meaning refinement)  
- RBU (meaning‑side commit)

---

# **7. Determinism, Replay, and Testbench Compatibility**

`ssg.py` must:

- produce identical outputs for identical inputs  
- avoid randomness  
- avoid non‑deterministic ordering  
- use stable sorting for canonicalization  
- use pure functions for invariant computation  
- record provenance deterministically  
- support progressive lineup testing

The testbench will verify:

- correct signature computation  
- correct bitmap formation  
- correct reason code  
- correct status  
- correct provenance  
- correct primitive boundaries  
- correct nested path usage  
- replay determinism

---

# **8. Error Handling**

`ssg.py` must:

- raise clear exceptions for malformed TP structures  
- set `tp.ssg_status = MISSING_INPUT` when SmOB output is absent  
- set `tp.ssg_status = DEGENERATE` when invariants collapse  
- never silently default or repair structural errors

---

# **9. Relationship to Other Artifacts**

This document is the implementation scaffold for:

- **20.47_ssg_prim.md** (normative)  
- **progressive_lineup_testing.md** (testbench discipline)  
- **ssg.py** (Python implementation)  
- **ssg_testbench.py / .yaml** (deterministic tests)  
- **ssg_rulechecker.py** (rule enforcement)  
- **ssg_input.yaml** (fixtures)

It ensures that all SSG artifacts can be written deterministically and consistently.

---

# **End of Document — ssg_py_struc_pgm.md (Unified Structural‑Only Rewrite)**

---
