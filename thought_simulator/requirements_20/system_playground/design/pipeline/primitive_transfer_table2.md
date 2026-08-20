# ✅ **Primitive Transfer Table 2 — Option C (Compressed + Structured + No Loss)**

This version preserves **every requirement, invariant, prohibition, and transfer‑function step**, but reorganizes them into:

1. **Master Summary Table** — one‑screen overview of each primitive  
2. **Compressed Sections** — deterministic, lossless, readable blocks for each primitive

## Path A – Bounded Semantics Requirement

Path A primitives are semantic, but only within bounded scope. Each primitive must
perform the meaning work inherent to its primary job, and no more. Meaning in Path A
is not forbidden; it is constrained, localized, and explicitly recorded.

### Core Principle
Every primitive in Path A operates under domain‑specific semantic assumptions required
to perform its function (normalization, segmentation, routing, clarification, repair,
naming, classification, update, join, constraint extraction, cue extraction, etc.).
These assumptions must be:
- recognized,
- bounded to the primitive’s domain,
- explicitly defined in the primitive’s transfer function,
- recorded in TP fields for downstream use,
- deterministic and replay‑safe.

Path A primitives do **not** hunt for meaning or perform global interpretation. They
simply acknowledge that their structural operations inherently rely on semantic
assumptions, and they record those assumptions so downstream primitives do not need
to reconstruct them.

### Why Bounded Semantics Are Required
Meaning is subjective, probabilistic, and distributed. If meaning were restricted only
to “meaning primitives,” those primitives would become overloaded, forced to replicate
semantic work that upstream primitives already implicitly performed. Downstream
primitives often operate in different semantic domains (conceptual, unification,
extraction, stability), making reconstruction unreliable and domain‑inappropriate.

Bounded semantics distributes interpretation across the pipeline in a way that mirrors
natural cognition: surface → lexical → structural → routing → update → conceptual →
extraction → stability. Each primitive contributes only the meaning appropriate to its
role.

### Invariants for Bounded Semantics
All Path A primitives must satisfy:

1. **Domain‑Bound Semantics**  
   Semantic effects must remain strictly within the primitive’s defined domain.

2. **Explicit Recording**  
   All semantic assumptions required for the primitive’s job must be written into TP
   fields; no hidden semantics.

3. **Determinism & Replay Safety**  
   All semantic effects must be deterministic, auditable, and replay‑safe.

4. **No Unbounded or Inferential Semantics**  
   No primitive may perform global interpretation, inference, or meaning expansion
   beyond its domain.

5. **Downstream Compatibility**  
   Downstream primitives may rely on upstream recorded semantics and must not be
   forced to reconstruct meaning from scratch.

### Architectural Outcome
Path A is not “structure‑only.”  
Path A is **structure + bounded meaning**, producing a deterministic, domain‑layered,
replay‑safe TP ready for stability (COB/CST) and meaning‑layer progression.

---

# **1. MASTER SUMMARY TABLE (Option C)**

| Primitive | Spec | Pipeline Position | Core Purpose | Key Outputs | No‑Change Guarantees |
|----------|------|------------------|--------------|-------------|-----------------------|
| **MCB** | 20.40.055 | After IdOB | Clarify meaning; normalize messy input; generate next_context | proposition_set, next_context, entropy update, provenance+trace | Identity geometry, continuity, basin, freeze unchanged   [Current page](citation-section://1147000847/3) |
| **RBU** | 20.51 | After MCB | Commit routing deltas for TR | routing_path, lineage_log, committed routing deltas | Meaning, identity, context unchanged   [Current page](citation-section://1147000847/11) |
| **TR** | 20.37 | After RBU | Deterministic routing decision | routing decision, tr_needs_update=false | Semantic, identity, context unchanged   [Current page](citation-section://1147000847/18) |
| **CTP** | 20.145 | After TR | Promote next_context → current_context; regenerate next_context | updated current_context, continuity update | Semantic, identity unchanged   [Current page](citation-section://1147000847/25) |
| **CEx‑IE** | 20.107.010 | After CTP | Build interpretive_record from clarified meaning + context | interpretive_record, extraction_tags | Semantic_core, identity unchanged   [Current page](citation-section://1147000847/34) |
| **CEx‑CCR** | 20.107.020 | After CEx‑IE | Canonicalize interpretive_record | canonical_record, canonical_tags | interpretive_record unchanged; identity unchanged   [Current page](citation-section://1147000847/43) |
| **CEx‑PCK** | 20.107.030 | After CCR | Pack canonical_record into bounded packed_record | packed_record, packed_tags | canonical_record unchanged; identity unchanged   [Current page](citation-section://1147000847/52) |
| **COB** | 20.32 | After PCK | Produce canonical_output_record | canonical_output_record, canonical_output_tags | packed_record unchanged; identity unchanged   [Current page](citation-section://1147000847/61) |
| **CIL** | 20.33 | After COB | Bind canonical output to identity geometry | linkage_record, linkage_tags | semantic_core not written; freeze unchanged   [Current page](citation-section://1147000847/70) |
| **CST‑Core** | 20.32.010.010 | After CIL | Compute stability metrics; emit Freeze/Thaw/Continuity signals | stability signals, metric histories | Does not modify identity topology   [Current page](citation-section://1147000847/79) |
| **CST‑MS** | 20.32.010.020 | After CST‑Core | Synthesize metrics; issue structural commands | stability/instability summaries; structural commands | Deterministic; replay‑safe   [Current page](citation-section://1147000847/84) |
| **CST‑Mux** | 20.32.010.030 | After CST‑Core/MS | Pack all CST signals into USP | unified_stability_packet, usp_tags | No identity/semantic modifications   [Current page](citation-section://1147000847/95) |

---

# **2. COMPRESSED PER‑PRIMITIVE SECTIONS (Option C)**

Each section is compressed but **lossless**, preserving all normative requirements, invariants, prohibitions, and transfer‑function steps.

---

## **MCB — Meaning Clarification Block**  
**Spec:** 20.40.055  
**Position:** After IdOB  
**Purpose:** Clarify meaning; normalize messy input; generate next_context; reduce entropy.  
**Inputs:** Full TP envelope from IdOB.  
**Outputs:**  
- clarified proposition_set  
- normalized messy_input_record  
- next_context updated from meaning  
- delta_h_percent adjusted  
- lineage_log + routing_path append `mcb`  
- tb_trace append `TB.mcb_alignment`  
**Transfer Function:**  
- Clarify meaning; normalize tags; remove ambiguity  
- Derive topic, stance, intent, importance  
- Preserve continuity unless correction required  
- Append entropy_history  
- No identity/continuity/basin/freeze changes  
**Determinism:** Same input → same output.  
  [Current page](citation-section://1147000847/3)

---

## **RBU — Routing Block Update**  
**Spec:** 20.51  
**Position:** After MCB  
**Purpose:** Commit routing deltas for TR.  
**Inputs:** MCB TP + routing deltas.  
**Outputs:**  
- routing_path + lineage_log append `rbu`  
- committed routing deltas  
- tb_trace append `TB.rbu_commit`  
**Transfer Function:**  
- Commit RB→IdOB→MCB routing deltas  
- Stabilize routing state  
- Adjust entropy if stabilization reduces uncertainty  
- No semantic/identity/context changes  
  [Current page](citation-section://1147000847/11)

---

## **TR — Thought Router**  
**Spec:** 20.37  
**Position:** After RBU  
**Purpose:** Deterministic routing decision.  
**Inputs:** RBU TP + OB fragments + DCB events + RB topology + tr_needs_update=true.  
**Outputs:**  
- routing decision  
- tr_needs_update=false  
- routing_path + lineage_log append `tr`  
- tb_trace append `TB.tr_routing_decision`  
**Transfer Function:**  
- Evaluate geometric, cultural, relational signals  
- Produce deterministic routing decision  
- No semantic/identity/context changes  
  [Current page](citation-section://1147000847/18)

---

## **CTP — Context Transition Primitive**  
**Spec:** 20.145  
**Position:** After TR  
**Purpose:** Promote next_context → current_context; regenerate next_context.  
**Inputs:** TR TP with next_context populated.  
**Outputs:**  
- current_context updated  
- new next_context  
- continuity progression/adjustment/wobble  
- routing_path + lineage_log append `ctp`  
- tb_trace append `TB.ctp_transition`  
**Transfer Function:**  
- Promote next_context  
- Generate new next_context from meaning + routing + continuity  
- Adjust entropy  
- No semantic/identity changes  
  [Current page](citation-section://1147000847/25)

---

## **CEx‑IE — Interpretive Engine**  
**Spec:** 20.107.010  
**Position:** After CTP  
**Purpose:** Build interpretive_record from clarified meaning + context.  
**Inputs:** CTP TP with clarified proposition_set + stable context.  
**Outputs:**  
- interpretive_record  
- extraction_tags  
- routing_path + lineage_log append `cex-ie`  
- tb_trace append `TB.cex_ie_extract`  
**Transfer Function:**  
- Extract semantic roles, relations, structural features  
- Normalize interpretive_record  
- Reduce entropy  
- No semantic_core/identity changes  
  [Current page](citation-section://1147000847/34)

---

## **CEx‑CCR — Canonical Core Representation**  
**Spec:** 20.107.020  
**Position:** After CEx‑IE  
**Purpose:** Canonicalize interpretive_record.  
**Inputs:** interpretive_record + extraction_tags.  
**Outputs:**  
- canonical_record  
- canonical_tags  
- routing_path + lineage_log append `cex-ccr`  
- tb_trace append `TB.cex_ccr_canonicalize`  
**Transfer Function:**  
- Remove ambiguity  
- Normalize roles/relations  
- Validate against context + identity  
- Reduce entropy  
- No identity/semantic_core changes  
  [Current page](citation-section://1147000847/43)

---

## **CEx‑PCK — Packing Engine**  
**Spec:** 20.107.030  
**Position:** After CCR  
**Purpose:** Pack canonical_record into bounded packed_record.  
**Inputs:** canonical_record + canonical_tags.  
**Outputs:**  
- packed_record  
- packed_tags  
- routing_path + lineage_log append `cex-pck`  
- tb_trace append `TB.cex_pck_pack`  
**Transfer Function:**  
- Compress canonical structure  
- Validate invariants  
- Reduce entropy  
- No identity/semantic_core changes  
  [Current page](citation-section://1147000847/52)

---

## **COB — Canonical Output Block**  
**Spec:** 20.32  
**Position:** After PCK  
**Purpose:** Produce canonical_output_record.  
**Inputs:** packed_record + packed_tags.  
**Outputs:**  
- canonical_output_record  
- canonical_output_tags  
- routing_path + lineage_log append `cob`  
- tb_trace append `TB.cob_output`  
**Transfer Function:**  
- Convert packed_record → canonical_output_record  
- Normalize for identity linkage  
- Reduce entropy  
- No identity/semantic_core changes  
  [Current page](citation-section://1147000847/61)

---

## **CIL — Canonical Identity Linkage**  
**Spec:** 20.33  
**Position:** After COB  
**Purpose:** Bind canonical output to identity geometry.  
**Inputs:** canonical_output_record + identity geometry.  
**Outputs:**  
- linkage_record  
- linkage_tags  
- basin/continuity_surface adjustments if required  
- routing_path + lineage_log append `cil`  
- tb_trace append `TB.cil_linkage`  
**Transfer Function:**  
- Bind semantic output to identity  
- Adjust basin/continuity if needed  
- Reduce entropy  
- No semantic_core; no freeze changes  
  [Current page](citation-section://1147000847/70)

---

## **CST‑Core — Stability Metric Engine**  
**Spec:** 20.32.010.010  
**Position:** After CIL  
**Purpose:** Compute stability metrics; emit Freeze/Thaw/Continuity signals.  
**Inputs:** identity geometry + canonical_output_record + linkage_record.  
**Outputs:**  
- stability signals  
- raw metrics  
- metric histories  
- routing_path + lineage_log append `cst-core`  
- tb_trace append `TB.cst_core_metrics`  
**Transfer Function:**  
- Snapshot identity layers  
- Compute drift/oscillation/ambiguity/collapse  
- Emit Freeze/Thaw/Continuity  
- No identity topology changes  
  [Current page](citation-section://1147000847/79)

---

## **CST‑MS — Metric Synthesis Module**  
**Spec:** 20.32.010.020  
**Position:** After CST‑Core  
**Purpose:** Synthesize metrics; issue structural commands.  
**Inputs:** raw metrics + thresholds + histories.  
**Outputs:**  
- stability/instability summaries  
- collapse/freeze/thaw metrics  
- structural commands (freeze/thaw/split/merge/etc.)  
- routing_path + lineage_log append `cst-ms`  
- tb_trace append `TB.cst_ms_synthesis`  
**Transfer Function:**  
- Normalize + weight metrics  
- Compute stability/instability  
- Issue deterministic structural commands  
  [Current page](citation-section://1147000847/84)

---

## **CST‑Mux — Stability Multiplexer**  
**Spec:** 20.32.010.030  
**Position:** After CST‑Core + CST‑MS  
**Purpose:** Pack all CST signals into Unified Stability Packet (USP).  
**Inputs:** CST‑Core + CST‑MS outputs.  
**Outputs:**  
- unified_stability_packet  
- usp_tags  
- routing_path + lineage_log append `cst-mux`  
- tb_trace append `TB.cst_mux_unified_packet`  
**Transfer Function:**  
- Collect + align signals  
- Normalize formats  
- Pack USP  
- No identity/semantic changes  
  [Current page](citation-section://1147000847/95)

---
