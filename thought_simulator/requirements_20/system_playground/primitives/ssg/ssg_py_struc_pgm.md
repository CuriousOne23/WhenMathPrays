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

# **3. High‑Level Program Structure (ISc‑Aligned)**

`ssg.py` follows the **class + `process()`** pattern used by the gold‑standard ISc
implementation so the progressive testbench can instantiate and call it uniformly.

```python
PRIMITIVE_NAME = "ssg"   # lowercase — must match directory and progressive naming

def get_primitive_name() -> str:
    return PRIMITIVE_NAME

class SSG:
    def __init__(self, tp_input=None):
        # deep-copy input TP so upstream is not mutated by reference accidents
        ...

    def process(self) -> dict:
        graph = self._extract_graph(self.tp)
        if graph is None:
            self._write_missing()          # status=MISSING_INPUT; do NOT write signature
            return self.tp

        phi, layer_bits = self._compute_phi(graph)
        signature = _l2_normalize(phi)     # or zero vector if ||phi||==0

        status, reason, bitmap = self._decide_status(phi, layer_bits, graph)
        self._write(signature, bitmap, reason, status)
        self._append_audit(status, reason, bitmap)
        return self.tp

def run(tp: dict) -> dict:
    """Functional alias matching older scaffold language."""
    return SSG(tp).process()
```

### Mandatory helpers (names may vary; responsibilities may not)

| Helper | Responsibility |
|--------|----------------|
| `_extract_graph(tp)` | Read SmOB structural graph; return normalized `{nodes, arcs}` or `None` if absent |
| `_compute_phi(graph)` | Compute provisional `f1..f5` → concatenated `phi`; also layer contribution bits |
| `_l2_normalize(vec)` | Return unit vector or zero vector |
| `_decide_status(...)` | Map phi / bits / emptiness → `(status, reason_code, bitmap)` |
| `_write(...)` | Write **only** the four SSG-owned fields |
| `_write_missing()` | `MISSING_INPUT` path: no `ssg_signature` key |
| `_append_audit(...)` | Append deterministic `ssg_ref` to `exec_trace` |

This structure is deterministic, testbench‑friendly (matches ISc control flow), C++‑parity‑friendly, and aligned with 20.47 and progressive §3.10.

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

`PARTIAL` as a **status** is secondary; primary status values used by the implementation are `OK | MISSING_INPUT | DEGENERATE`, with `PARTIAL` mainly as **reason_code**. That matches the current `ssg.py`.

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

# **10. Concrete Fixture Graph Shape (Provisional)**

### Preferred
```yaml
metadata:
  residue:
    structural_residue:
      nodes:
        - id: "a"
          label: "segment"
          layer: 3          # 0=SOB, 1=SROB, 2=CnOB, 3=SmOB
        - id: "b"
          label: "constraint"
          layer: 2
      arcs:
        - src: "a"
          dst: "b"
          label: "constrain"
          layer: 2
    refinement_residue: []
    constraint_residue: []
    semantic_adjacent_residue: []
    presemantic_hash: "..."
    residue_provenance:
      origin: SmOB
      last_update: SmOB
```

### Acceptable alternate
```yaml
metadata:
  structural_graph:
    nodes: [...]
    arcs: [...]
```

If neither form is present → `ssg_status = MISSING_INPUT` and **do not** write `ssg_signature`.

---

# **11. Provisional Dimension and Family Layout (v1)**

| Family | Length | Contents (v1 stub-friendly) |
|--------|--------|-----------------------------|
| f1 arc patterns | 8 | Normalized counts over fixed `ARC_VOCAB` |
| f2 binding depth | 2 | max depth / 10, mean depth / 10 |
| f3 residue entropy | 1 | Shannon entropy of node labels |
| f4 curvature | 2 | cycle-density proxy, clustering stub |
| f5 motif frequencies | 7 | chain2, chain3, star, cycle3, parallel, self_loop, isolated |
| **d** | **20** | sum of the above |

`ARC_VOCAB` (fixed order): `bind, order, adj, constrain, refine, continue, segment, other`  
Unknown arc labels → `other`.

v1 φ may be deterministic stubs. The contract under test is the four-field interface, L2 discipline, status/reason/bitmap, and write boundaries — not yet geometric quality for RB.

---

# **12. Status / Reason Decision Table**

| Condition | `ssg_status` | `ssg_reason_code` | `ssg_signature` | `ssg_layer_bitmap` |
|-----------|--------------|-------------------|-----------------|--------------------|
| No residue / structural_graph | `MISSING_INPUT` | `EMPTY` | **absent** | `0` |
| Graph present, φ = 0, empty layers | `OK` | `EMPTY` | zero vector length d | `0` |
| Graph non-empty but φ = 0 | `DEGENERATE` | `EMPTY` | zero vector | `0` |
| Some but not all of L0–L3 | `OK` | `PARTIAL` | L2 unit vector | 1..14 |
| All four layers | `OK` | `FULL` | L2 unit vector | `15` |

Bits: `b0=SOB, b1=SROB, b2=CnOB, b3=SmOB`.

---

# **13. Progressive Testbench File Map for SSG**

```
primitives/ssg/ssg.py
testbenches/path_a/structure/
  ssg_testbench.py
  ssg_testbench.yaml
  ssg_input.yaml
  ssg_rules.yaml
  ssg_rules_to_check.yaml
  ssg_rulechecker.py
  ssg_tests_to_run.yaml
```

`run.py` module path:
`thought_simulator.requirements_20.system_playground.testbenches.path_a.structure.ssg_testbench`  
with `"use_ssg": True`.

---

# **14. What v1 Must Prove vs Defer**

**Must prove:** four-field contract; no upstream residue mutation; status/reason/bitmap enums; L2 unit or zero; MISSING_INPUT does not write signature; determinism / progressive mechanics.

**Deferred:** final f1..f5 formulas; final motif catalog; empirical clustering for RB.
```

---

# **End of Document — ssg_py_struc_pgm.md (Unified Structural‑Only Rewrite)**
