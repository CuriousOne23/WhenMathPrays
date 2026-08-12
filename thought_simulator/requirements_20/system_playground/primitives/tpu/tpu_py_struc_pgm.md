# ⭐ **`tpu_py_struc_pgm.md` (Version 1.0)**  
### *Python & C++ Implementation Blueprint for the TPU Primitive*  
### *Aligned with 20.46 (TPU Requirements), 20.105.*, 20.105.010, 20.105.020, 20.105.030, 20.15, and the Thought Pipeline Description*

---

# **1. TPU’s Role in the Pipeline**

TPU is the **deterministic commit engine** of Path‑A.  
It immediately follows CE in the pipeline:

1. **CEx‑IE** — structural hints  
2. **CEx‑CCR** — alignment + decision  
3. **CEx‑Pck** — metadata packaging  
4. **CE** — canonical context envelope  
5. **TPU** — authoritative commit of all metadata and meaning

TPU is responsible for:

- validating **tp_update_request{}** blocks  
- enforcing **writer‑authority boundaries** (20.105)  
- enforcing **canonical ordering** (20.95)  
- enforcing **safe‑boundary commit rules** (20.30)  
- applying updates **atomically**  
- enforcing **1‑TP‑cycle lag semantics**  
- committing all metadata envelopes into TP  
- producing **tpu_audit_record{}**  
- producing **tpu_error{}** on deterministic fallback  
- writing **commit provenance**  
- stabilizing meaning for OB‑Set and downstream primitives

TPU consumes:

- `tp_update_request{}` (immutable)  
- `TP.metadata.context` (CE envelope)  
- `TP.metadata.msl_metadata`  
- `TP.metadata.continuity_metadata`  
- `TP.metadata.semantic_residue_metadata`  
- `TP.metadata.cil_metadata`  
- `TP.semantic.importance`  
- `TP.cex.ccr`  
- `TP.metadata.next_context`  
- `TP.metadata.freeze_metadata` (read‑only)  
- `TP.metadata.entropy_metadata` (read‑only)

TPU produces:

- committed TP(N+1)  
- tpu_audit_record{}  
- tpu_error{} (fallback)  
- commit provenance  
- canonical ordering  
- safe‑boundary marker  
- updated metadata envelopes

TPU does **not**:

- generate meaning  
- interpret semantics  
- modify structural geometry  
- modify semantic_core  
- modify intake/context fields  
- perform routing  
- perform identity refinement  
- perform lineage updates outside commit provenance  
- perform inference of any kind

TPU is deterministic, bounded, replay‑safe, and the **sole commit authority** of Path‑A.

---

# **2. Public API (Python & C++)**

```python
tpu = TPU(tp_input, tp_update_request)
tpu.commit()
```

TPU SHALL populate or update the following TP envelopes/metadata:

### **Commit‑time metadata (TPU‑written)**

- `TP.metadata.provenance_metadata`  
  - `commit_id`  
  - `commit_sequence`  
  - `primitive_origin = "TPU"`  
  - `commit_timestamp`  
  - `commit_lineage[]`

- `TP.metadata.repair_metadata` (if repairs applied)  
- `TP.metadata.context` (CE envelope → committed)  
- `TP.metadata.continuity_metadata`  
- `TP.metadata.msl_metadata`  
- `TP.metadata.semantic_residue_metadata`  
- `TP.metadata.cil_metadata`  
- `TP.semantic.importance`  
- `TP.cex.ccr`  
- `TP.metadata.next_context`  
- `TP.metadata.entropy_metadata` (commit lineage only)  
- `TP.metadata.freeze_metadata` (commit lineage only)

### **Commit artifacts**

- `tpu_audit_record{}`  
- `tpu_error{}` (fallback)

### Required method

```python
def commit(self):
    # validate tp_update_request
    # enforce writer authority
    # enforce canonical ordering
    # enforce safe-boundary rules
    # apply updates atomically
    # write commit provenance
    # produce audit record
    # return updated TP
```

---

# **3. Intake Model (Two Inputs)**

TPU receives **two** bounded inputs:

---

## **3.1 TP Input (TP(N))**

TPU reads:

- CE envelope  
- continuity metadata  
- MSL metadata  
- semantic‑importance  
- CCR output  
- semantic‑residue metadata  
- CIL metadata  
- next_context metadata  
- entropy metadata  
- freeze metadata  
- structural metadata  
- routing metadata  
- identity metadata  
- provenance metadata (previous commits)

TPU treats all TP fields as **read‑only** except those it is authorized to commit.

---

## **3.2 tp_update_request{} (Immutable)**

TPU reads:

```
tp_update_request {
  isc{...}
  cil{...}
  cob{...}
  cop{...}
  idob_update{...}
  mcb_update{...}
  rbu_update{...}
  metadata {
    merge_version
    canonical_ordering_hash
    safe_boundary_marker?
    seed
  }
}
```

TPU uses this request to:

- validate writer authority  
- validate update blocks  
- validate canonical ordering  
- validate safe‑boundary conditions  
- apply updates atomically  
- produce audit record  
- produce fallback behavior if needed

TPU treats tp_update_request{} as **immutable**.

---

# **4. Deterministic Rule Ordering**

TPU must apply operations in **exact order**:

1. Read TP(N)  
2. Read tp_update_request{}  
3. Validate writer authority  
4. Validate update blocks  
5. Validate canonical ordering  
6. Validate safe‑boundary conditions  
7. Apply updates atomically  
8. Write commit provenance  
9. Produce tpu_audit_record{}  
10. Produce tpu_error{} (if fallback)  
11. Emit deterministic TP(N+1)

This ordering ensures:

- replay determinism  
- Python/C++ parity  
- stable integration with OB‑Set, SSG, STPX, RB, TR, IdOB, MCB, OuBA, COB, CIL, CST

---

# **5. Commit Normalization**

TPU normalizes commit behavior using:

- canonical ordering rules (20.95)  
- safe‑boundary rules (20.30)  
- writer‑authority rules (20.105)  
- atomicity rules (20.46)  
- provenance rules (20.105.020)  
- replay rules (20.12)

Normalization includes:

- ordering arrays/maps deterministically  
- validating clarifying‑field boundedness (10/100/4)  
- validating next_context fields  
- validating semantic‑importance residues  
- validating CCR output  
- validating CIL substrate selection  
- validating semantic‑residue alignment  
- validating identity‑conditioned updates  
- validating entropy trajectory  
- validating freeze metadata  
- validating commit lineage

TPU does **not** infer meaning.

---

# **6. Commit Envelope Construction**

TPU constructs the committed TP(N+1):

```
TP(N+1) {
    semantic.*
    process.*
    metadata.*
    clarifying_fields.*
    next_context.*
    semantic_importance.*
    cex.ccr.*
    semantic_residue.*
    cil.*
    provenance.*
}
```

Rules:

- All fields must be deterministic  
- All fields must support replay  
- All fields must preserve provenance  
- All fields must be stable under Python/C++ parity  
- All updates must be atomic  
- All updates must follow writer‑authority rules  
- All updates must follow safe‑boundary rules  
- All updates must follow canonical ordering rules  

TP(N+1) is consumed by:

- SOB  
- SROB  
- CnOB  
- SmOB  
- ISc  
- SSG  
- STPX  
- RB  
- TR  
- IdOB  
- MCB  
- OuBA  
- COB  
- CIL  
- CST

---

# **7. TPU Audit Record**

TPU produces an audit record containing:

- update blocks  
- writer‑authority validation  
- canonical ordering validation  
- safe‑boundary validation  
- atomicity validation  
- fallback behavior (if any)  
- provenance lineage  
- commit hash  
- TP(N) hash  
- TP(N+1) hash  
- TCU usage  
- timestamp

Audit record is read‑only for downstream primitives.

---

# **8. TPU Error Object**

On validation failure, TPU emits:

```
tpu_error {
  code,
  rationale,
  fallback_behavior,
  audit_record
}
```

Fallback behavior is deterministic and replay‑safe.

---

# **9. Replay Determinism**

TPU must be:

- deterministic  
- replay‑stable  
- rule‑stable  
- ordering‑stable  
- provenance‑stable  
- safe‑boundary‑stable  

Given identical:

- TP(N)  
- tp_update_request{}  

TPU produces identical:

- TP(N+1)  
- tpu_audit_record{}  
- commit provenance  
- canonical ordering  
- fallback behavior (if any)

Python and C++ implementations must:

- use identical iteration ordering  
- avoid nondeterministic data structures  
- avoid nondeterministic sorting or hashing  
- construct envelopes in a stable, rule‑driven way  

---

# **10. Forbidden Behavior**

TPU must not:

- generate meaning  
- interpret semantics  
- modify semantic_core  
- modify intake/context fields  
- modify structural geometry  
- modify routing metadata  
- modify identity metadata  
- modify freeze metadata  
- modify entropy metadata  
- infer meaning  
- use embeddings or global semantics  
- write outside its allowed TP envelopes  
- perform lineage updates outside commit provenance  
- violate writer‑authority rules  
- violate safe‑boundary rules  
- violate canonical ordering rules

---

# **11. Implementation Skeleton (Python)**

```python
class TPU:
    def __init__(self, tp_input, tp_update_request):
        self.tp = tp_input
        self.req = tp_update_request

    def commit(self):
        # 1. Validate writer authority
        self._validate_writer_authority(self.req)

        # 2. Validate update blocks
        self._validate_update_blocks(self.req)

        # 3. Validate canonical ordering
        self._validate_canonical_ordering(self.req)

        # 4. Validate safe-boundary conditions
        self._validate_safe_boundary(self.req)

        # 5. Apply updates atomically
        updated_tp = self._apply_updates(self.tp, self.req)

        # 6. Write commit provenance
        self._write_provenance(updated_tp)

        # 7. Produce audit record
        audit = self._build_audit_record(updated_tp)

        return updated_tp, audit

    # Internal helpers:
    # _validate_writer_authority
    # _validate_update_blocks
    # _validate_canonical_ordering
    # _validate_safe_boundary
    # _apply_updates
    # _write_provenance
    # _build_audit_record
```

---

# **12. Implementation Skeleton (C++)**

```cpp
class TPU {
public:
    TPU(TP& tp_input, const UpdateRequest& req_input)
        : tp(tp_input), req(req_input) {}

    CommitResult commit() {
        validate_writer_authority(req);
        validate_update_blocks(req);
        validate_canonical_ordering(req);
        validate_safe_boundary(req);

        TP updated = apply_updates(tp, req);
        write_provenance(updated);

        AuditRecord audit = build_audit_record(updated);
        return {updated, audit};
    }

private:
    TP& tp;
    const UpdateRequest& req;

    // deterministic helper methods
};
```

---

# **13. TP Field Schema — Downstream Consumption Map (Normative)**

TPU writes:

- committed TP(N+1)  
- commit provenance  
- tpu_audit_record{}  
- tpu_error{} (fallback)  
- canonical ordering  
- safe‑boundary marker  

Downstream consumers:

| Primitive | Consumes | Purpose |
|----------|----------|---------|
| **SOB/SROB/CnOB/SmOB** | committed TP | structural + semantic‑adjacent extraction |
| **ISc** | committed TP | scoring metadata |
| **SSG/STPX** | committed TP | semantic‑layer cues |
| **RB/TR/RBU/DCB** | committed TP | routing + arbitration |
| **IdOB** | committed TP | identity‑conditioned meaning |
| **MCB** | committed TP | next‑turn context |
| **OuBA** | committed TP | freeze + SSR |
| **COB/CIL/CST** | committed TP | long‑horizon continuity |

TPU output must support deterministic replay and read‑only consumption.

---

# **14. Change Management**

When TPU evolves:

- update writer‑authority rules  
- update canonical ordering rules  
- update safe‑boundary rules  
- update update‑block validation  
- update audit schema  
- update provenance schema  
- update tpu_error schema  
- update testbench (`tpu_testbench.yaml`)  
- update rulechecker (`tpu_rules.yaml`, `tpu_rulechecker.py`)  
- update 20.46 (TPU requirements)  
- ensure replay determinism  
- ensure Python/C++ parity  

---

# ⭐ **End of Document — `tpu_py_struc_pgm.md` (Version 1.0)**

