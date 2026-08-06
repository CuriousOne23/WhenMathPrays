## 1. CEx‑CCR’s role in the pipeline

CEx‑CCR is the **second internal module** of the CEx primitive.  
It receives:

- the **CEx‑IE envelope** (`TP.cex.ie`) containing structural hints derived from IE tokens, and  
- the **CIL lineage + metrics** (`TP.cil`) for the last ≤10 conversations.

CEx‑CCR:

- computes alignment across identity, clarifying, context, continuity, and reference dimensions,  
- derives ambiguity, collapse, drift, and stability scores from CIL metrics,  
- applies deterministic decision rules to select:

  - one of the last 10 conversations,  
  - a new conversation, or  
  - an ambiguous → fallback conversation,

- emits a compact `TP.cex.ccr` envelope for CEx‑Pck.

CEx‑CCR is:

- deterministic  
- rule‑driven  
- bounded‑semantic  
- replay‑safe  
- lineage‑driven  
- structure‑driven  

CEx‑CCR does **not**:

- perform IE repackaging (CEx‑IE)  
- perform downstream packaging (CEx‑Pck)  
- use embeddings or global semantics  
- access downstream primitives beyond writing `TP.cex.ccr`.

---

## 2. Public API (Python & C++)

The testbench invokes CEx‑CCR exactly like this:

```python
cex_ccr = CExCCR(tp_input)
cex_ccr.inspect()
```

CEx‑CCR must expose:

### Required fields (`TP.cex.ccr`)

- `alignment.identity`  
- `alignment.clarifying`  
- `alignment.context`  
- `alignment.continuity`  
- `alignment.reference`  
- `scores.ambiguity`  
- `scores.collapse`  
- `scores.drift`  
- `scores.stability`  
- `decision`  
- `selected_conversation`

### Required method

```python
def inspect(self):
    # populate TP.cex.ccr deterministically
```

### Required behavior

CEx‑CCR:

- reads only `TP.cex.ie` and `TP.cil` fields,  
- computes alignment enums (`none | weak | moderate | strong`) using deterministic rules,  
- derives numeric scores directly from CIL scalar metrics,  
- applies bounded decision logic to emit `decision = new | specific | fallback`,  
- selects `selected_conversation` deterministically (conversation ID or `null`),  
- writes only to `TP.cex.ccr`, leaving upstream envelopes unchanged,  
- produces replay‑stable output for identical inputs.

CEx‑CCR does **not**:

- infer meaning  
- use embeddings  
- use global context  
- modify `TP.cex.ie` or `TP.cil`  
- perform packaging or lineage updates.

---

## 3. Intake model (two inputs)

CEx‑CCR receives **two input envelopes** from TP:

### 3.1 CEx‑IE envelope (`TP.cex.ie`)

```python
ie_tokens          = TP["cex"]["ie"]["tokens"]
ie_token_flags     = TP["cex"]["ie"]["token_flags"]
ie_normalized      = TP["cex"]["ie"]["normalized_text"]
ie_struct_phrases  = TP["cex"]["ie"]["structural_phrases"]
topic_hint         = TP["cex"]["ie"]["topic_hint"]
intent_hint        = TP["cex"]["ie"]["intent_hint"]
continuity_hint    = TP["cex"]["ie"]["continuity_hint"]
reference_hint     = TP["cex"]["ie"]["reference_hint"]
register_hint      = TP["cex"]["ie"]["register_hint"]
politeness_hint    = TP["cex"]["ie"]["politeness_hint"]
direction_hint     = TP["cex"]["ie"]["direction_hint"]
coherence_hint     = TP["cex"]["ie"]["coherence_hint"]
importance_hint    = TP["cex"]["ie"]["importance_hint"]
```

CEx‑CCR must:

- treat these hints as **bounded structural categories**,  
- never reinterpret or modify them,  
- use them only for alignment and decision logic.

### 3.2 CIL envelope (`TP.cil` — last ≤10 conversations)

For each conversation `k` in the last ≤10:

```python
cil_identity_lineage[k]   = TP["cil"][k]["identity_lineage"]
cil_clarifying_lineage[k] = TP["cil"][k]["clarifying_lineage"]
cil_context_lineage[k]    = TP["cil"][k]["context_lineage"]
cil_continuity_lineage[k] = TP["cil"][k]["continuity_lineage"]
cil_topology[k]           = TP["cil"][k]["topology"]
cil_metrics[k]            = TP["cil"][k]["metrics"]  # includes ambiguity, collapse, drift, stability, etc.
cil_semantic_residue[k]   = TP["cil"][k]["semantic_residue"]
cil_next_context[k]       = TP["cil"][k]["next_context"]
```

CEx‑CCR must:

- iterate deterministically over the ≤10 conversations,  
- compute alignment and scores per conversation,  
- select a single conversation ID or `null` according to decision rules,  
- never modify CIL lineage or metrics.

---

## 4. Deterministic rule ordering  
### (Enforced by `cex_ccr_testbench.yaml`)

CEx‑CCR must apply its operations in **exactly this order**:

1. **Receive inputs**  
   - Read `TP.cex.ie` structural hints.  
   - Read `TP.cil` lineage + metrics for ≤10 conversations.

2. **Compute alignment**  
   - Identity alignment (topic + intent vs identity_lineage).  
   - Clarifying alignment (register + politeness vs clarifying_lineage).  
   - Context alignment (topic + direction vs context_lineage).  
   - Continuity alignment (continuity_hint vs continuity_lineage).  
   - Reference alignment (reference_hint vs identity_lineage + semantic_residue).

3. **Derive scores**  
   - ambiguity, collapse, drift, stability from CIL metrics.

4. **Apply decision logic**  
   - classify as `new`, `specific`, or `fallback` using deterministic rules and thresholds.

5. **Select conversation**  
   - choose `selected_conversation` ID or `null` according to decision outcome.

6. **Construct `TP.cex.ccr` envelope**  
   - populate alignment, scores, decision, selected_conversation.

7. **Validate envelope shape**  
   - ensure all required fields are present and correctly typed.

8. **Emit deterministic output**  
   - write `TP.cex.ccr` and return TP unchanged elsewhere.

This ordering is required for deterministic replay and Python/C++ parity.

---

## 5. Alignment computation

CEx‑CCR computes **five alignment dimensions** using deterministic rules:

### 5.1 Identity alignment

- **Inputs:** `topic_hint`, `intent_hint`, `ie_struct_phrases`, `cil_identity_lineage[k]`.  
- **Output:** `alignment.identity[k] ∈ {none, weak, moderate, strong}`.

Rules (conceptual):

- strong: topic_hint and intent_hint match identity_lineage with high structural consistency.  
- moderate: partial match (topic or intent) with supporting structural phrases.  
- weak: minimal structural match or ambiguous patterns.  
- none: no structural match.

### 5.2 Clarifying alignment

- **Inputs:** `register_hint`, `politeness_hint`, `intent_hint`, `cil_clarifying_lineage[k]`.  
- **Output:** `alignment.clarifying[k]`.

Rules:

- strong: register + politeness + intent structurally consistent with clarifying_lineage.  
- moderate/weak/none: graded by degree of structural match.

### 5.3 Context alignment

- **Inputs:** `topic_hint`, `direction_hint`, `cil_context_lineage[k]`.  
- **Output:** `alignment.context[k]`.

Rules:

- strong: topic_hint and direction_hint align with context_lineage (e.g., forward/backward references).  
- moderate/weak/none: graded by structural consistency.

### 5.4 Continuity alignment

- **Inputs:** `continuity_hint`, `cil_continuity_lineage[k]`.  
- **Output:** `alignment.continuity[k]`.

Rules:

- strong: continuity_hint (continue/reset/shift) matches continuity_lineage.  
- unclear: continuity_hint = unknown or conflicting signals.  
- mapped to `none/weak/moderate/strong` deterministically.

### 5.5 Reference alignment

- **Inputs:** `reference_hint`, `cil_identity_lineage[k]`, `cil_semantic_residue[k]`.  
- **Output:** `alignment.reference[k]`.

Rules:

- strong: reference_hint indicates specific_previous and identity_lineage + residue match.  
- moderate: reference_hint indicates previous with partial match.  
- weak/none: ambiguous_previous or no reference.

All alignment values are assigned using deterministic rule tables defined in `cex_ccr_rules.yaml`.

---

## 6. Score derivation

CEx‑CCR derives **numeric scores** directly from CIL metrics:

- `scores.ambiguity[k]` ← `cil_metrics[k].ambiguity_score`  
- `scores.collapse[k]`  ← `cil_metrics[k].collapse_risk`  
- `scores.drift[k]`     ← `cil_metrics[k].drift_score`  
- `scores.stability[k]` ← `cil_metrics[k].stability_score`

Rules:

- no transformation beyond deterministic mapping (e.g., copying or simple normalization),  
- no semantic inference,  
- no external context.

Thresholds for “high/low ambiguity” and “stability threshold” are defined in `cex_ccr_rules.yaml` and used in decision logic.

---

## 7. Decision logic

CEx‑CCR emits a single `decision` field of type `CExDecision`:

- `new`  
- `specific`  
- `fallback`

Decision rules (per 20.107.020 and behavioral spec):

### 7.1 New conversation

Select **new** when:

- identity alignment across all conversations is `none`, **AND**  
- ambiguity score is **high** (above threshold), **AND**  
- continuity_hint indicates reset (e.g., `reset` or strong reset cue).

Result:

- `decision = "new"`  
- `selected_conversation = null`.

### 7.2 Specific conversation

Select **specific** when there exists a conversation `k` such that:

- `alignment.identity[k] = strong`, **AND**  
- ambiguity score for `k` is **low** (below threshold), **AND**  
- `alignment.continuity[k] = strong`.

Result:

- `decision = "specific"`  
- `selected_conversation = conversation_id[k]`.

If multiple candidates satisfy these conditions, tie‑breaking is deterministic (e.g., highest stability_score, then most recent).

### 7.3 Ambiguous → fallback

Select **fallback** when:

- identity alignment is `weak` or `moderate` across candidates, **OR**  
- ambiguity is **moderate**, **OR**  
- continuity alignment is unclear (`none` or weak).

Result:

- `decision = "fallback"`  
- `selected_conversation = fallback_conversation_id`.

Fallback selection:

- choose the **most recent** conversation with `scores.stability[k]` above a deterministic threshold,  
- if none, choose the most recent conversation overall.

All thresholds and tie‑breaking rules are defined in `cex_ccr_rules.yaml`.

---

## 8. Bounded semantic domain

CEx‑CCR is a **bounded‑semantic primitive**, meaning:

- operates only on IE‑derived structural hints and CIL lineage + metrics,  
- does not infer meaning,  
- does not use embeddings,  
- does not use global semantic similarity,  
- is deterministic and replay‑stable.

Allowed operations:

- alignment computation  
- score derivation  
- decision logic  
- envelope construction.

Prohibited operations:

- semantic inference  
- meaning interpretation  
- packaging or lineage updates  
- modification of `TP.cex.ie` or `TP.cil`.

---

## 9. Structural schema

CEx‑CCR produces:

```text
TP.cex.ccr {
    alignment: {
        identity:   CExAlign,  # none | weak | moderate | strong
        clarifying: CExAlign,
        context:    CExAlign,
        continuity: CExAlign,
        reference:  CExAlign
    },
    scores: {
        ambiguity: number,
        collapse:  number,
        drift:     number,
        stability: number
    },
    decision:             CExDecision,        # new | specific | fallback
    selected_conversation: ConversationID | null
}
```

All fields must be present:

- alignment fields for each dimension,  
- scores for all four metrics,  
- a single decision value,  
- selected_conversation (ID or `null`).

---

## 10. Replay metadata

CEx‑CCR must be:

- deterministic  
- replay‑stable  
- rule‑stable  

Given identical `TP.cex.ie` and `TP.cil` inputs, CEx‑CCR must produce identical `TP.cex.ccr` output.

This is enforced by:

- `cex_ccr_testbench.yaml` (exact expected outputs),  
- `cex_ccr_rules.yaml` + `cex_ccr_rulechecker.py` (rule‑driven validation),  
- `progressive_lineup_testing.md` (pipeline replay guarantees).

---

## 11. Forbidden behavior

CEx‑CCR must not:

- modify `TP.cex.ie` fields,  
- modify `TP.cil` fields,  
- read fields outside `TP.cex.ie` and `TP.cil`,  
- write fields outside `TP.cex.ccr`,  
- infer meaning or use embeddings,  
- use global semantic similarity,  
- introduce nondeterministic values (timestamps, random IDs, etc.),  
- perform packaging or lineage updates (reserved for CEx‑Pck and COB/CST).

---

## 12. Implementation skeleton (Python)

```python
class CExCCR:
    def __init__(self, tp):
        self.tp = tp
        # Ensure TP.cex.ccr exists
        if "cex" not in self.tp:
            self.tp["cex"] = {}
        self.tp["cex"]["ccr"] = {}

    def inspect(self):
        # 1. Receive IE and CIL fields
        ie = self.tp["cex"]["ie"]
        cil = self.tp["cil"]  # dict or list of conversations

        # Extract IE hints
        topic_hint      = ie["topic_hint"]
        intent_hint     = ie["intent_hint"]
        continuity_hint = ie["continuity_hint"]
        reference_hint  = ie["reference_hint"]
        register_hint   = ie["register_hint"]
        politeness_hint = ie["politeness_hint"]
        direction_hint  = ie["direction_hint"]
        # coherence_hint, importance_hint available if needed

        # 2. Compute alignment per conversation
        alignment = {
            "identity":   {},
            "clarifying": {},
            "context":    {},
            "continuity": {},
            "reference":  {}
        }
        scores = {
            "ambiguity": {},
            "collapse":  {},
            "drift":     {},
            "stability": {}
        }

        for conv_id, conv in cil.items():
            id_lineage   = conv["identity_lineage"]
            clar_lineage = conv["clarifying_lineage"]
            ctx_lineage  = conv["context_lineage"]
            cont_lineage = conv["continuity_lineage"]
            residue      = conv["semantic_residue"]
            metrics      = conv["metrics"]

            # Identity alignment
            alignment["identity"][conv_id] = compute_identity_align(
                topic_hint, intent_hint, id_lineage
            )

            # Clarifying alignment
            alignment["clarifying"][conv_id] = compute_clarifying_align(
                register_hint, politeness_hint, intent_hint, clar_lineage
            )

            # Context alignment
            alignment["context"][conv_id] = compute_context_align(
                topic_hint, direction_hint, ctx_lineage
            )

            # Continuity alignment
            alignment["continuity"][conv_id] = compute_continuity_align(
                continuity_hint, cont_lineage
            )

            # Reference alignment
            alignment["reference"][conv_id] = compute_reference_align(
                reference_hint, id_lineage, residue
            )

            # 3. Derive scores
            scores["ambiguity"][conv_id] = metrics["ambiguity_score"]
            scores["collapse"][conv_id]  = metrics["collapse_risk"]
            scores["drift"][conv_id]     = metrics["drift_score"]
            scores["stability"][conv_id] = metrics["stability_score"]

        # 4. Apply decision logic
        decision, selected_conv = decide_conversation(
            alignment, scores, continuity_hint
        )

        # 5. Construct TP.cex.ccr envelope
        self.tp["cex"]["ccr"] = {
            "alignment": {
                "identity":   summarize_alignment(alignment["identity"]),
                "clarifying": summarize_alignment(alignment["clarifying"]),
                "context":    summarize_alignment(alignment["context"]),
                "continuity": summarize_alignment(alignment["continuity"]),
                "reference":  summarize_alignment(alignment["reference"]),
            },
            "scores": {
                "ambiguity": summarize_scores(scores["ambiguity"]),
                "collapse":  summarize_scores(scores["collapse"]),
                "drift":     summarize_scores(scores["drift"]),
                "stability": summarize_scores(scores["stability"]),
            },
            "decision": decision,
            "selected_conversation": selected_conv
        }

        # 6. Validate envelope
        validate_cex_ccr(self.tp["cex"]["ccr"])

        return self.tp
```

> In practice, `summarize_alignment` and `summarize_scores` will collapse per‑conversation values into the final CCR envelope (e.g., the chosen conversation’s alignment and scores), consistent with `20.107.020_cex-ccr_primitive.md`.

---

## 13. Implementation skeleton (C++)

Equivalent structure:

- `class CExCCR`  
- constructor receives TP  
- `inspect()` reads `TP.cex.ie` + `TP.cil`, computes alignment/scores/decision, and populates `TP.cex.ccr`.  
- deterministic rule application, no embeddings, no global semantics.  
- identical envelope shape and behavior to Python implementation.

---

## 14. Change management

When CEx‑CCR evolves:

- update alignment rule tables in `cex_ccr_rules.yaml`,  
- update decision thresholds and tie‑breaking rules,  
- update `cex_ccr_testbench.yaml` expected outputs,  
- update `cex_ccr_rulechecker.py` logic,  
- update this document to reflect new behavior,  
- ensure replay determinism,  
- ensure Python/C++ parity.

This document is the **authoritative programming reference** for CEx‑CCR v1.0.
