# ⭐ **`ce_py_struc_pgm.md` (Version 1.0)**  
### *Python & C++ Implementation Blueprint for the CE Primitive*  
### *Aligned with 20.108 (CE Envelope), 20.107.030 (CEx‑Pck), 20.105.*, and 20.15*

---

# **1. CE’s Role in the Pipeline**

CE is the **canonical context engine** of Path‑A.  
It immediately follows CEx‑Pck in the pipeline:

1. **CEx‑IE** — structural hints  
2. **CEx‑CCR** — alignment + decision  
3. **CEx‑Pck** — context shell + MSL + continuity metadata  
4. **CE** — canonical context envelope construction

CE is responsible for:

- normalizing the **context shell** produced by CEx‑Pck  
- producing the **canonical CE envelope** (`TP.metadata.context`)  
- validating context coherence, direction, continuity, and importance  
- producing the **extraction_audit**  
- producing **ce_version_tag**  
- writing CE provenance  
- preparing context for ISc, TR, RB, IdOB, and downstream primitives

CE consumes:

- `TP.metadata.context_metadata` (context_fields, flags, provenance)  
- `TP.metadata.msl_metadata` (MSL tokens)  
- `TP.metadata.next_context` (if present)  
- `TP.cex.ccr` (read‑only)  
- `TP.semantic.importance` (read‑only)

CE produces:

- canonical CE envelope  
- extraction_audit  
- ce_version_tag  
- CE provenance

CE does **not**:

- modify CCR output  
- modify semantic‑importance  
- modify CIL metadata  
- modify semantic‑residue metadata  
- perform identity refinement (IdOB responsibility)  
- perform routing (TR/RB responsibility)  
- perform lineage updates (COB/CIL/CST responsibility)

CE is deterministic, bounded‑semantic, replay‑safe, and TP‑aligned.

---

# **2. Public API (Python & C++)**

```python
ce = CE(tp_input)
ce.inspect()
```

CE SHALL populate or update the following TP envelopes/metadata:

- `TP.metadata.context` (canonical CE envelope):
  - `topic`
  - `stance`
  - `intent`
  - `register`
  - `politeness`
  - `tone`
  - `continuity`
  - `direction`
  - `coherence`
  - `importance`
  - `clarifying_fields[]`
  - `relevance_flags`
  - `copy_forward_flags`
  - `reset_flags`
  - `context_provenance`
- `TP.metadata.context.extraction_audit`
- `TP.metadata.context.ce_version_tag`

CE SHALL **not** modify:

- `TP.cex.ccr.*`  
- `TP.semantic.importance.*`  
- `TP.metadata.cil.*`  
- `TP.metadata.semantic_residue.*`  

### Required method

```python
def inspect(self):
    # read CEx-Pck metadata
    # normalize context deterministically
    # construct canonical CE envelope
    # write CE provenance + audit
```

---

# **3. Intake Model (Three Inputs)**

CE receives **three** bounded inputs from TP.

---

## **3.1 Context Metadata (`TP.metadata.context_metadata`)**

CE reads:

```python
TP.metadata.context.context_fields {
    topic
    stance
    intent
    register
    politeness
    tone
    continuity
    direction
    coherence
    importance
    clarifying_fields[]
}

TP.metadata.context.relevance_flags
TP.metadata.context.copy_forward_flags
TP.metadata.context.reset_flags
TP.metadata.context.context_provenance
```

CE uses these fields to:

- normalize context  
- validate continuity  
- validate coherence/direction  
- produce canonical CE envelope  
- produce extraction_audit  

CE treats all context_metadata fields as **bounded structural categories**.

---

## **3.2 Meaning Signal Layer (`TP.metadata.msl_metadata`)**

CE reads:

```python
TP.metadata.msl.qualifiers
TP.metadata.msl.clarifications
TP.metadata.msl.stance
TP.metadata.msl.shading
TP.metadata.msl.intent
TP.metadata.msl.direction
TP.metadata.msl.coherence
TP.metadata.msl.subculture
TP.metadata.msl.msl_provenance
```

CE uses MSL tokens to:

- refine stance, direction, coherence  
- validate context alignment  
- support extraction_audit  

MSL tokens are **short structured tokens**, not semantic interpretations.

---

## **3.3 Next‑Context Metadata (`TP.metadata.next_context`)**

If present:

```python
TP.metadata.next_context.next_context
TP.metadata.next_context.direction
TP.metadata.next_context.coherence
TP.metadata.next_context.stance
TP.metadata.next_context.subculture
TP.metadata.next_context.next_context_provenance
```

CE uses next_context to:

- validate continuity  
- validate copy‑forward behavior  
- support extraction_audit  

CE does **not** modify next_context.

---

# **4. Deterministic Rule Ordering**

CE must apply operations in **exact order**:

1. Read context_metadata  
2. Read MSL metadata  
3. Read next_context (if present)  
4. Normalize context fields  
5. Validate continuity, direction, coherence, importance  
6. Construct canonical CE envelope  
7. Construct extraction_audit  
8. Write CE provenance  
9. Emit deterministic TP output for ISc, TR, RB, IdOB, and downstream primitives

This ordering ensures:

- replay determinism  
- Python/C++ parity  
- stable integration with ISc, TR, RB, IdOB, COB, CIL, CST

---

# **5. Context Normalization**

CE normalizes the context shell produced by CEx‑Pck.

Inputs:

- `context_fields`  
- `relevance_flags`  
- `copy_forward_flags`  
- `reset_flags`  
- MSL tokens  
- next_context (if present)

Outputs:

- canonical CE envelope  
- extraction_audit  
- ce_version_tag  
- CE provenance

Normalization includes:

- bounded category validation  
- continuity validation  
- direction/coherence normalization  
- importance normalization  
- clarifying_fields normalization  
- stance/register/politeness/tone normalization  
- MSL‑context reconciliation

CE does **not** infer meaning.

---

# **6. CE Envelope Construction**

CE constructs the canonical CE envelope:

```
TP.metadata.context {
    topic
    stance
    intent
    register
    politeness
    tone
    continuity
    direction
    coherence
    importance
    clarifying_fields[]
    relevance_flags
    copy_forward_flags
    reset_flags
    context_provenance
    extraction_audit
    ce_version_tag
}
```

Rules:

- All fields are bounded structural categories  
- All fields must be deterministic  
- All fields must support replay  
- All fields must preserve provenance  
- All fields must be stable under Python/C++ parity  

CE envelope is consumed by:

- ISc  
- TR  
- RB  
- IdOB  
- CTP  
- RTU  
- OuBA  

---

# **7. Extraction Audit**

CE produces an extraction audit containing:

- normalized context fields  
- MSL reconciliation notes  
- continuity validation notes  
- direction/coherence validation notes  
- importance validation notes  
- clarifying_fields validation notes  
- provenance summary

Extraction audit is read‑only for downstream primitives.

---

# **8. CE Version Tag**

CE writes:

```
TP.metadata.context.ce_version_tag = "CE_v2.0"
```

Version tag is immutable after TPU commit.

---

# **9. Replay Determinism**

CE must be:

- deterministic  
- replay‑stable  
- rule‑stable  

Given identical:

- context_metadata  
- MSL metadata  
- next_context metadata  

CE produces identical:

- canonical CE envelope  
- extraction_audit  
- ce_version_tag  

Python and C++ implementations must:

- use identical iteration ordering  
- avoid nondeterministic data structures  
- avoid nondeterministic sorting or hashing  
- construct envelopes in a stable, rule‑driven way  

---

# **10. Forbidden Behavior**

CE must not:

- modify CCR fields  
- modify semantic‑importance fields  
- modify CIL metadata  
- modify semantic‑residue metadata  
- infer meaning  
- use embeddings or global semantics  
- write outside its allowed TP envelopes  
- perform lineage updates (COB/CIL/CST responsibility)

---

# **11. Implementation Skeleton (Python)**

```python
class CE:
    def __init__(self, tp_input):
        self.tp = tp_input

    def inspect(self):
        # 1. Read context metadata
        ctx = self.tp.get("metadata", {}).get("context", {})
        ctx_fields = ctx.get("context_fields", {})
        flags = {
            "relevance": ctx.get("relevance_flags", {}),
            "copy_forward": ctx.get("copy_forward_flags", {}),
            "reset": ctx.get("reset_flags", {})
        }

        # 2. Read MSL metadata
        msl = self.tp.get("metadata", {}).get("msl", {})

        # 3. Read next_context (if present)
        next_ctx = self.tp.get("metadata", {}).get("next_context", {})

        # 4. Normalize context
        normalized = self._normalize_context(ctx_fields, msl, next_ctx, flags)

        # 5. Construct extraction audit
        audit = self._build_extraction_audit(normalized, msl, next_ctx, flags)

        # 6. Write CE envelope
        self._update_tp(normalized, audit)

    # Internal helpers:
    # _normalize_context, _build_extraction_audit, _update_tp
```

---

# **12. Implementation Skeleton (C++)**

```cpp
class CE {
public:
    explicit CE(TP& tp_input) : tp(tp_input) {}

    void inspect() {
        auto ctx       = tp.metadata.context;
        auto ctxFields = ctx.context_fields;
        auto flags     = ctx.flags;
        auto msl       = tp.metadata.msl;
        auto nextCtx   = tp.metadata.next_context;

        auto normalized = normalize_context(ctxFields, msl, nextCtx, flags);
        auto audit      = build_extraction_audit(normalized, msl, nextCtx, flags);

        update_tp(normalized, audit);
    }

private:
    TP& tp;
    // helper methods implemented deterministically
};
```

---

# **13. TP Field Schema — Downstream Consumption Map (Normative)**

CE writes:

- canonical CE envelope  
- extraction_audit  
- ce_version_tag  
- CE provenance  

Downstream consumers:

| Primitive | Consumes | Purpose |
|----------|----------|---------|
| **ISc** | CE envelope | scoring metadata |
| **TR** | CE envelope | routing vector |
| **RB** | CE envelope | basin selection |
| **IdOB** | CE envelope | identity‑conditioned meaning |
| **CTP/RTU** | CE envelope | routing updates |
| **OuBA** | CE envelope | freeze metadata |
| **TPU** | CE provenance | commit lineage |

CE envelope must support deterministic replay and read‑only consumption.

---

# **14. Change Management**

When CE evolves:

- update normalization rules  
- update extraction_audit schema  
- update CE envelope schema (if 20.105/20.108 change)  
- update testbench (`ce_testbench.yaml`)  
- update rulechecker (`ce_rules.yaml`, `ce_rulescheck.py`)  
- update 20.108 (CE primitive spec)  
- ensure replay determinism  
- ensure Python/C++ parity  

---

# ⭐ **End of Document — `ce_py_struc_pgm.md` (Version 1.0)**

Jeff — this is the complete CE structural program, fully aligned with all TS‑20 documents and your rewritten CEx‑Pck spec.
