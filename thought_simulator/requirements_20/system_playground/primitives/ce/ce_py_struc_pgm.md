# ⭐ **`ce_py_struc_pgm.md` (Version 2.0)**  
### *Python & C++ Implementation Blueprint for the CE Primitive*  
### *Aligned with 20.108 (CE Envelope), 20.108.010 (CE Candidate-Set), 20.45 (ISc), 20.107.030 (CEx‑Pck), 20.105.*, and 20.15*

---

# **1. CE’s Role in the Pipeline**

CE is the **canonical context engine** of Path‑A.  
It immediately follows CEx‑Pck in the pipeline:

1. **CEx‑IE** — structural hints  
2. **CEx‑CCR** — alignment + decision  
3. **CEx‑Pck** — context shell + MSL + continuity metadata  
4. **CE** — canonical context envelope construction **and** candidate-set generation

CE is responsible for:

- normalizing the **context shell** produced by CEx‑Pck  
- producing the **canonical CE envelope** (`TP.metadata.context`)  
- validating context coherence, direction, continuity, and importance  
- producing the **extraction_audit**  
- producing **ce_version_tag**  
- writing CE provenance  
- generating the finite **candidate set** at `TP.ce.candidate_set[]` (per 20.108.010)  
- populating each candidate with deterministic FFTM, structural, semantic-adjacent, next-context, and provenance fields  
- preparing both the classic CE envelope and the candidate set for ISc, TR, RB, IdOB, and downstream primitives

CE consumes:

- `TP.metadata.context` / context_fields, flags, provenance (from CEx-Pck)  
- `TP.metadata.msl` (MSL tokens)  
- `TP.metadata.next_context` (if present)  
- `TP.cex.ccr` (read‑only)  
- `TP.semantic.importance` (read‑only)  
- `TP.metadata.normalization_metadata` (for FFTM surface/lemma sources)  
- `TP.metadata.semantic_layer_metadata` / modality_stance_cues (for FFTM expression/intent sources)  
- OB-Set residue metadata and related structural cues (read-only, when present)

CE produces:

- canonical CE envelope under `TP.metadata.context`  
- extraction_audit  
- ce_version_tag  
- CE provenance  
- `TP.ce.candidate_set[]` (finite, ordered, deterministic)

CE does **not**:

- modify CCR output  
- modify semantic‑importance  
- modify CIL metadata  
- modify semantic‑residue metadata  
- perform identity refinement (IdOB responsibility)  
- perform routing (TR/RB responsibility)  
- perform lineage updates (COB/CIL/CST responsibility)  
- **score** candidates (ISc responsibility)  
- expand the candidate set beyond the construction rule defined in 20.108.010  
- generate meaning or perform semantic inference

CE is deterministic, bounded‑semantic, replay‑safe, and TP‑aligned.  
CE emits **both** the classic context envelope and the candidate set; both are committed by TPU.

---

# **2. Public API (Python & C++)**

```python
ce = CE(tp_input)
ce.inspect()
```

CE SHALL populate or update the following TP envelopes/metadata:

### Classic CE envelope

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
  - `extraction_audit`
  - `ce_version_tag`

### Candidate set (new — 20.108.010)

- `TP.ce.candidate_set[]` — finite array of candidate objects, each containing:
  - `candidate_id`
  - `fftm_fields` { token_surface, token_base, token_expression, token_intent }
  - `structural_features` { surface_id, lemma_id, expression_id, ordering_id, constraint_family_id, next_context_id, …optional… }
  - `semantic_adjacent_features` { semantic_residue, structural_residue, …optional… }
  - `next_context` { … }
  - `provenance` { … }

CE SHALL **not** modify:

- `TP.cex.ccr.*`  
- `TP.semantic.importance.*`  
- `TP.metadata.cil.*`  
- `TP.metadata.semantic_residue.*` (except reading for semantic-adjacent features)  

### Required method

```python
def inspect(self):
    # read CEx-Pck / upstream metadata
    # normalize context deterministically
    # construct canonical CE envelope
    # construct TP.ce.candidate_set[] (construction rule + FFTM + features + ordering)
    # write CE provenance + audit + candidate_set
```

---

# **3. Intake Model**

CE receives bounded inputs from TP.

---

## **3.1 Context Metadata (`TP.metadata.context`)**

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
- supply next_context and continuity signals for each candidate  

CE treats all context fields as **bounded structural categories**.

---

## **3.2 Meaning Signal Layer (`TP.metadata.msl`)**

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
- populate each candidate’s `next_context` block  

CE does **not** modify next_context.

---

## **3.4 Semantic Importance & Upstream Feature Sources (for candidate set)**

CE also reads (read-only):

- `TP.semantic.importance.entities[]` / `facts[]` — primary source of candidate generation  
- `TP.metadata.normalization_metadata` (normalized_tokens surface / lemma) — FFTM sources  
- `TP.metadata.semantic_layer_metadata.modality_stance_cues` — FFTM expression / intent sources  
- OB-Set / residue metadata — structural and semantic-adjacent features  
- CEx-CCR alignment / scores — semantic_residue cues  

CE SHALL NOT consume Pipeline-B envelopes or truth/done fields.

---

# **4. Deterministic Rule Ordering**

CE must apply operations in **exact order**:

1. Read context metadata  
2. Read MSL metadata  
3. Read next_context (if present)  
4. Read semantic.importance, normalization_metadata, semantic_layer_metadata, residue cues (read-only)  
5. Normalize context fields  
6. Validate continuity, direction, coherence, importance  
7. Construct canonical CE envelope  
8. Construct extraction_audit  
9. **Construct candidate_set** according to the construction rule (20.108.010 §6)  
10. **Populate** each candidate: FFTM, structural_features, semantic_adjacent_features, next_context, provenance  
11. **Order** `TP.ce.candidate_set[]` by the canonical ordering rule  
12. Write classic CE envelope + extraction_audit + ce_version_tag + provenance  
13. Write `TP.ce.candidate_set[]`  
14. Emit deterministic TP output for ISc, TR, RB, IdOB, and downstream primitives

This ordering ensures:

- replay determinism  
- Python/C++ parity  
- stable integration with ISc (which scores the candidate set), TR, RB, IdOB, COB, CIL, CST  

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

# **6. CE Envelope Construction (Classic)**

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

Classic CE envelope is consumed by ISc, TR, RB, IdOB, CTP, RTU, OuBA, and others for context continuity and routing.

---

# **7. Candidate-Set Construction (Normative — 20.108.010)**

## **7.1 Construction Rule**

CE SHALL construct `TP.ce.candidate_set[]` as follows:

1. **One candidate per primary `semantic.importance` entity.**  
2. **Additional candidates** MAY be generated when structural ambiguity is detected (e.g., multiple valid `ordering_id` or `constraint_family_id` interpretations).  
3. CE SHALL **always** generate at least one candidate, even when `semantic.importance` is empty; this is the **default interpretation candidate**.  
4. CE SHALL use only upstream features from IE, CEx, semantic.importance, and TP metadata.  
5. CE SHALL NOT expand the set beyond the above rule or beyond replay-safe bounds.

## **7.2 Candidate Object Schema**

Each element of `TP.ce.candidate_set[]` SHALL contain:

```text
candidate_id: number          # unique within the array
fftm_fields:
  token_surface: ...
  token_base: ...
  token_expression: ...
  token_intent: ...
structural_features:          # minimum required keys
  surface_id
  lemma_id
  expression_id
  ordering_id
  constraint_family_id
  next_context_id
  # optional: continuity_id, entity_id, adjacency, constraint_importance, ...
semantic_adjacent_features:   # minimum required keys
  semantic_residue            # from CEx-CCR
  structural_residue          # from OB-Set
  # optional: referent_adjacent_signals, modality_stance_cues, ...
next_context: { ... }         # pre-semantic continuity signals
provenance: { ... }           # per 20.105.020
```

## **7.3 FFTM Population (Deterministic Sources)**

CE SHALL populate `fftm_fields` from upstream sources only; no semantic inference:

| FFTM field         | Deterministic source |
|--------------------|----------------------|
| `token_surface`    | IE normalized surface (`TP.metadata.normalization_metadata` / normalized_tokens surface) |
| `token_base`       | IE lemma/base form |
| `token_expression` | semantic-layer modality/stance expression cue (`TP.metadata.semantic_layer_metadata.modality_stance_cues.expression`) |
| `token_intent`     | semantic-layer modality/stance intent cue (`…modality_stance_cues.intent`) |

These four fields constitute the complete FFTM meaning-layer feature set consumed by ISc (20.45).

## **7.4 Structural & Semantic-Adjacent Features**

- `structural_features` SHALL contain at minimum the six keys listed above; additional bounded structural cues MAY be included when available.  
- `semantic_adjacent_features` SHALL contain at minimum `semantic_residue` and `structural_residue`; other bounded residue metadata MAY be included.  
- All such features are treated as structural or residue cues; CE SHALL NOT modify semantic_core or FFTM fields after construction.

## **7.5 Canonical Ordering**

CE SHALL order `TP.ce.candidate_set[]` by:

1. **Primary:** ascending `candidate_id`  
2. **Secondary:** ascending `ordering_id`  
3. **Tertiary:** lexical ascending `fftm_fields.token_surface`  

Ordering MUST be identical across Python and C++ and across replay runs.

## **7.6 Provenance**

Each candidate’s `provenance` SHALL record sufficient information to trace:

- upstream primitives contributing to the candidate  
- key feature sources (IE, CEx, OB-Set, TP metadata)  
- CE internal decision path  

and SHALL comply with 20.105.020.

## **7.7 Immutability & ISc Hand-off**

- After TPU commit, `TP.ce.candidate_set[]` is immutable.  
- ISc operates on a read-only candidate set; CE does **not** score.  
- CE guarantees the set is directly consumable by ISc (all required FFTM, structural, semantic-adjacent, next-context, and provenance fields present).

---

# **8. Extraction Audit**

CE produces an extraction audit containing:

- normalized context fields  
- MSL reconciliation notes  
- continuity validation notes  
- direction/coherence validation notes  
- importance validation notes  
- clarifying_fields validation notes  
- provenance summary  
- (optional) notes on candidate-set cardinality and default-candidate generation  

Extraction audit is read‑only for downstream primitives.

---

# **9. CE Version Tag**

CE writes:

```
TP.metadata.context.ce_version_tag = "CE_v2.0"
```

Version tag is immutable after TPU commit.

---

# **10. Replay Determinism**

CE must be:

- deterministic  
- replay‑stable  
- rule‑stable  

Given identical:

- context metadata  
- MSL metadata  
- next_context metadata  
- semantic.importance  
- normalization / semantic-layer / residue inputs used for candidates  

CE produces identical:

- canonical CE envelope  
- extraction_audit  
- ce_version_tag  
- `TP.ce.candidate_set[]` (content, ordering, and provenance)  

Python and C++ implementations must:

- use identical iteration ordering  
- avoid nondeterministic data structures  
- avoid nondeterministic sorting or hashing  
- construct envelopes and candidate sets in a stable, rule‑driven way  
- apply the same canonical candidate ordering rule  

---

# **11. Forbidden Behavior**

CE must not:

- modify CCR fields  
- modify semantic‑importance fields  
- modify CIL metadata  
- modify semantic‑residue metadata (except reading for feature population)  
- infer meaning or perform semantic inference  
- use embeddings or global semantics  
- write outside its allowed TP envelopes (`TP.metadata.context.*` and `TP.ce.candidate_set[]`)  
- perform lineage updates (COB/CIL/CST responsibility)  
- **score** candidates or produce ranking distributions (ISc responsibility)  
- expand the candidate set beyond the construction rule  
- generate candidates via nondeterministic sampling, external services, or opaque non-replayable heuristics  
- modify semantic_core or FFTM fields after candidate-set construction  

---

# **12. Implementation Skeleton (Python)**

```python
class CE:
    def __init__(self, tp_input):
        self.tp = tp_input

    def inspect(self):
        # 1–3. Read classic inputs
        ctx = self.tp.get("metadata", {}).get("context", {})
        ctx_fields = ctx.get("context_fields", {})
        flags = {
            "relevance": ctx.get("relevance_flags", {}),
            "copy_forward": ctx.get("copy_forward_flags", {}),
            "reset": ctx.get("reset_flags", {})
        }
        msl = self.tp.get("metadata", {}).get("msl", {})
        next_ctx = self.tp.get("metadata", {}).get("next_context", {})

        # 4. Read candidate-set sources (read-only)
        semantic_importance = self.tp.get("semantic", {}).get("importance", {})
        norm_meta = self.tp.get("metadata", {}).get("normalization_metadata", {})
        sem_layer = self.tp.get("metadata", {}).get("semantic_layer_metadata", {})
        residue = self.tp.get("metadata", {}).get("residue", {})  # or equivalent paths

        # 5–6. Normalize + validate classic context
        normalized = self._normalize_context(ctx_fields, msl, next_ctx, flags)

        # 7–8. Classic envelope + audit
        audit = self._build_extraction_audit(normalized, msl, next_ctx, flags)

        # 9–11. Candidate set
        candidates = self._build_candidate_set(
            semantic_importance, norm_meta, sem_layer, residue, normalized, next_ctx
        )
        candidates = self._order_candidates(candidates)

        # 12–13. Write both envelopes
        self._update_tp(normalized, audit, candidates)

        return self.tp

    # Internal helpers (deterministic):
    # _normalize_context, _build_extraction_audit,
    # _build_candidate_set, _populate_fftm, _populate_structural,
    # _populate_semantic_adjacent, _order_candidates, _update_tp
```

---

# **13. Implementation Skeleton (C++)**

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

        // Candidate-set sources (read-only)
        auto semImp    = tp.semantic.importance;
        auto normMeta  = tp.metadata.normalization_metadata;
        auto semLayer  = tp.metadata.semantic_layer_metadata;
        auto residue   = tp.metadata.residue;

        auto normalized = normalize_context(ctxFields, msl, nextCtx, flags);
        auto audit      = build_extraction_audit(normalized, msl, nextCtx, flags);

        auto candidates = build_candidate_set(
            semImp, normMeta, semLayer, residue, normalized, nextCtx);
        order_candidates(candidates);

        update_tp(normalized, audit, candidates);
    }

private:
    TP& tp;
    // helper methods implemented deterministically
};
```

---

# **14. TP Field Schema — Downstream Consumption Map (Normative)**

CE writes:

- canonical CE envelope (`TP.metadata.context.*`)  
- extraction_audit  
- ce_version_tag  
- CE provenance  
- `TP.ce.candidate_set[]`  

Downstream consumers:

| Primitive | Consumes | Purpose |
|----------|----------|---------|
| **ISc** | Classic CE envelope **and** `TP.ce.candidate_set[]` | Context continuity + deterministic scoring of the candidate set (ISc is the sole scorer) |
| **TR** | CE envelope | routing vector |
| **RB** | CE envelope (+ entropy/ΔH% from ISc downstream) | basin selection / escalation |
| **IdOB** | CE envelope | identity‑conditioned meaning |
| **CTP/RTU** | CE envelope | routing updates |
| **OuBA** | CE envelope | freeze metadata |
| **TPU** | CE provenance + both envelopes | commit lineage; commits both classic CE and candidate_set |

Both the classic envelope and the candidate set must support deterministic replay and read‑only consumption after TPU commit.

---

# **15. Testbench Contract (Brief)**

CE testbenches (per progressive_lineup_testing.md) MUST exercise:

- classic envelope construction and extraction_audit  
- candidate-set generation:  
  - entity-based candidates  
  - default interpretation candidate (empty semantic.importance)  
  - structural-ambiguity expansion (when applicable)  
  - deterministic ordering  
  - FFTM source mapping  
  - minimum structural / semantic-adjacent keys  
  - replay identity (identical inputs → identical candidate_set)  
- dual write of `TP.metadata.context.*` and `TP.ce.candidate_set[]`  

Expected blocks in `ce_testbench.yaml` SHALL include both the classic CE fields and a complete `ce.candidate_set` array.  
ISc testbenches will consume the candidate set produced by CE.

---

# **16. Change Management**

When CE evolves:

- update normalization rules  
- update extraction_audit schema  
- update CE envelope schema (if 20.105 / 20.108 change)  
- update candidate-set construction / feature / ordering rules (if 20.108.010 changes)  
- update testbench (`ce_testbench.yaml`)  
- update rulechecker (`ce_rules.yaml`, `ce_rulechecker.py`)  
- update 20.108 and 20.108.010 as needed  
- ensure replay determinism for both envelopes  
- ensure Python/C++ parity  

---

# ⭐ **End of Document — `ce_py_struc_pgm.md` (Version 2.0)**

This structural program is the implementation blueprint for both the classic CE envelope (20.108) and the CE candidate set (20.108.010) required by ISc (20.45).
