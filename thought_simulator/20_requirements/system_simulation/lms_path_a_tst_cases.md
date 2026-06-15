# **LMS Path A Test Cases**  
**Authors:** CuriousOne23, Copilot, Grok  
**Version:** 3.3 — Unified, Refined, Grok‑Aligned  

---

# **Introduction & Purpose**

This document defines the **Path A (pre‑meaning) validation suite** for the Thought Simulator. Its purpose is to verify that the **structural cognition pipeline**—OB → RB → TE → TR → DCB—correctly extracts, organizes, and stabilizes all structural information required for **Path B** to assign meaning, navigate basins, and generate coherent downstream responses.

Path A is responsible for **structure only**, never semantics. It must transform arbitrary, messy, ambiguous, or domain‑specific input into a **deterministic, canonical, fully organized structural representation** inside `TP.TR`, while preserving all invariants defined in the 20.x requirements (20.10, 20.30, 20.31, 20.37, 20.40, 20.50, 20.106, 20.131, 20.165).

The tests in this document exercise the following **core primitives and processes**:

### **1. OB (Object Basin) — Entity & Modifier Extraction**
- Identifies entities, noun clusters, and modifiers.  
- Preserves messy input without smoothing.  
- Produces canonical ordering and sets `tr_needs_update=true`.

### **2. TE (Transform Engine) — Verb & Relation Extraction**
- Extracts verbs, relations, clause boundaries, and dependency arcs.  
- Emits topology events (split/merge, clause chains) without assigning meaning.

### **3. RB (Routing Basin) — Gating & Arbitration**
- Enforces the OB → RB → TE → RB → TR flow contract (20.37).  
- Applies `routing_filter`, resolves stale TR states, and prevents infinite loops.  
- Routes to DCB when ambiguity or geometric deviation is detected.

### **4. TR Routine — Structural Organization**
- Consumes OB/TE outputs and produces the canonical structural representation:  
  - `logical_structure`  
  - `routing_semantics`  
  - `modifier_attachment`  
  - `sequence`  
  - `epistemic_shading`  
  - `tension`  
  - `canonical_ordering`  
  - `stance`, `intent`, `affect`, `commitment`, `reservation`, `semantic_deltaH`, `lineage_additions`  
- Clears `tr_needs_update` and ensures deterministic replay.

### **5. DCB (Directional Conversation Basin) — Ephemeral Geometry**
- Emits strictly geometric, ephemeral hints (curvature, drift, deviation).  
- Never assigns meaning or domain semantics.  
- TR may consume these hints once, then discard them.

---

# **Execution Guidance**

To run these tests correctly:

- Use deterministic replay: identical input → identical `TP.TR` and `routing_filter`.  
- Validate `tr_needs_update` lifecycle:  
  - Set by OB/TE  
  - Cleared only by TR  
- Verify canonical ordering after every TR update.  
- Preserve messy input (no smoothing, no rewriting).  
- Validate read‑only boundaries:  
  - OB/TE/DCB never write to TR  
  - Only TR writes to TR  
- Validate overflow/bounds behavior per 20.31.  
- JSON fixtures should include:  
  - `ob_output`, `te_output`, `routing_filter`, `TP.TR`, `topology_event_log`.

---

# **What These Tests Validate**

The test suite ensures that Path A:

- Extracts **all** structural primitives (entities, modifiers, verbs, relations).  
- Correctly handles **multi‑clause**, **ambiguous**, **noisy**, and **token‑level** inputs.  
- Preserves **messy input**, **canonical ordering**, and **read‑only boundaries**.  
- Produces a **complete, consistent, deterministic** TR structure.  
- Emits **no meaning**, **no inference**, and **no semantic leakage**.  
- Provides Path B with a **fully consumable structural substrate** for meaning construction.  
- Demonstrates that the requirements are **coherent, testable, and implementable** on a common laptop with reasonable performance.

---

# **PATH A VALIDATION SUITE (v3.3)**  
### *Fully aligned with 20.10, 20.30, 20.31, 20.37, 20.40, 20.50, 20.106, 20.131, 20.165*

Each test includes:

- **Purpose**  
- **Input**  
- **Expected Path‑A output** (OB, TE, RB, TR, DCB)  
- **Full TR canonical fields**  
- **Invariants**  
- **Metrics**  
- **HLR references**

---

# **TEST 1 — Entity + Modifier Extraction (OB Core)**

### **Purpose**  
Verify OB extracts entities/modifiers, preserves messy input, sets `tr_needs_update`, and prepares TR input.

### **Input**  
> “The small copper valve controls the high‑pressure water line.”

### **Expected Path‑A Output**

**OB**  
- Entities:  
  - E1 = “valve”  
  - E2 = “water line”  
- Modifiers:  
  - “small”, “copper” → E1  
  - “high‑pressure” → E2  
- `ob_output.canonical_order = [E1, E2]`  
- `messy_tags = preserved`  
- `tr_needs_update = true`

**RB**  
- `routing_filter = ["TR"]`

**TR**  
- `logical_structure = "simple_transitive"`  
- `routing_semantics = {subject:E1, verb:"controls", object:E2}`  
- `modifier_attachment = {"small":E1, "copper":E1, "high-pressure":E2}`  
- `epistemic_shading = neutral`  
- `tension = none`  
- `canonical_ordering = preserved`  
- `stance = neutral`  
- `intent = none`  
- `affect = none`  
- `commitment = none`  
- `reservation = none`  
- `semantic_deltaH = 0.0`  
- `lineage_additions = []`  
- `tr_needs_update = false`

### **Invariants**
- No smoothing  
- No semantic inference  
- Deterministic replay  
- Canonical ordering preserved  
- Read‑only boundaries upheld

### **Metrics**
- Entity Recall  
- Modifier Attachment Accuracy  
- Deterministic Replay Equivalence

### **HLRs**
20.40 §2–3, 20.37 §4–6, 20.31

---

# **TEST 2 — Verb & Relation Mapping (TE + TR)**

### **Purpose**  
Ensure TE extracts verbs/relations; TR organizes them structurally.

### **Input**  
> “The technician tightened the loose bolt.”

### **Expected Path‑A Output**

**OB**  
- Entities: technician, bolt  
- Modifier: “loose” → bolt  
- `tr_needs_update = true`

**TE**  
- Verb: “tightened”  
- Relation: (technician → tightened → bolt)  
- `topology_event_log = ["verb_anchor_created"]`

**TR**  
- `logical_structure = "transitive_action"`  
- `routing_semantics = {subject:E1, verb:"tightened", object:E2}`  
- `modifier_attachment = {"loose":E2}`  
- `epistemic_shading = neutral`  
- `tension = none`  
- `canonical_ordering = preserved`  
- `stance = neutral`  
- `intent = none`  
- `affect = none`  
- `commitment = none`  
- `reservation = none`  
- `semantic_deltaH = 0.0`  
- `lineage_additions = []`  
- `tr_needs_update = false`

### **Invariants**
- No meaning leakage  
- No smoothing  
- Deterministic ordering  
- Read‑only boundaries upheld

### **Metrics**
- Verb Recall  
- Relation Arc Accuracy  
- TE/TR consistency

### **HLRs**
20.37 §6, 20.40

---

# **TEST 3 — Multi‑Clause + Dependency Resolution**

### **Purpose**  
Ensure Path A handles clause boundaries, sequencing, and anaphora cues.

### **Input**  
> “After the sensor failed, the system activated a backup module that restored stability.”

### **Expected Path‑A Output**

**OB**  
- Entities: sensor, system, backup module, stability  
- Clause markers preserved  
- Anaphora cue: “that” flagged  
- `tr_needs_update = true`

**TE**  
- Verbs: failed, activated, restored  
- Relations:  
  - (sensor → failed)  
  - (system → activated → backup module)  
  - (backup module → restored → stability)  
- `topology_event_log = ["clause_chain_created"]`

**TR**  
- `logical_structure = "temporal_causal_chain"`  
- `sequence = ["failed","activated","restored"]`  
- `reference_resolution = {"that":E_backup_module}`  
- `epistemic_shading = low_confidence`  
- `tension = mild`  
- `canonical_ordering = preserved`  
- `stance = neutral`  
- `intent = none`  
- `affect = none`  
- `commitment = none`  
- `reservation = none`  
- `semantic_deltaH = 0.0`  
- `lineage_additions = []`  
- `tr_needs_update = false`

**RB**  
- Routes OB → TE → TR  
- If ambiguity persists, RB → DCB

### **Invariants**
- Messy input preserved  
- No semantic inference  
- Deterministic clause ordering  
- Read‑only boundaries upheld

### **Metrics**
- Clause Boundary Accuracy  
- Reference Resolution Accuracy  
- Temporal Ordering Accuracy

### **HLRs**
20.50, 20.131, 20.37

---

# **TEST 4 — Ambiguity Detection (No Resolution)**

### **Purpose**
Ensure Path A flags ambiguity but does not resolve it.

### **Input**
> “The engineer inspected the panel near the generator, but it was still overheating.”

### **Expected Path‑A Output**

**OB**  
- Entities: engineer, panel, generator  
- Pronoun “it” flagged ambiguous  
- `messy_tags = preserved`  
- `tr_needs_update = true`

**TE**  
- Verbs: inspected, overheating  
- Structural relations only

**TR**  
- `logical_structure = "ambiguous_reference"`  
- `routing_semantics = {ambiguous_pronoun:"it", candidates:["panel","generator"]}`  
- `epistemic_shading = ambiguous`  
- `tension = mild`  
- `canonical_ordering = preserved`  
- `stance = neutral`  
- `intent = none`  
- `affect = none`  
- `commitment = none`  
- `reservation = none`  
- `semantic_deltaH = 0.0`  
- `lineage_additions = []`  
- `tr_needs_update = false`

**RB**  
- Routes to DCB for geometric hint only  
- Does NOT resolve ambiguity

### **Invariants**
- No meaning leakage  
- No smoothing  
- Ambiguity preserved  
- Read‑only boundaries upheld  
- Deterministic replay

### **Metrics**
- Ambiguity Detection Recall  
- False Positive Rate

### **HLRs**
20.17, 20.37

---

# **TEST 5 — Modifier Importance Weighting**

### **Purpose**
Ensure Path A identifies critical vs. decorative modifiers.

### **Input**
> “The corroded steel pipe in the basement is leaking rapidly.”

### **Expected Path‑A Output**

**OB**  
- Entity: pipe  
- Modifiers:  
  - corroded (high)  
  - steel (medium)  
  - basement (low)  
- `tr_needs_update = true`

**TE**  
- Verb: leaking  
- Modifier “rapidly” → high importance

**TR**  
- `importance_weights = {"corroded":0.9, "rapidly":0.85, "steel":0.5, "basement":0.2}`  
- `modifier_types = {structural, behavioral, material, location}`  
- `epistemic_shading = neutral`  
- `tension = none`  
- `canonical_ordering = preserved`  
- `stance = neutral`  
- `intent = none`  
- `affect = none`  
- `commitment = none`  
- `reservation = none`  
- `semantic_deltaH = 0.0`  
- `lineage_additions = []`  
- `tr_needs_update = false`

### **Invariants**
- No semantic inference  
- Deterministic weighting  
- Read‑only boundaries upheld  
- Canonical ordering preserved

### **Metrics**
- Importance Weight Correlation  
- Critical Modifier Recall

### **HLRs**
20.40, 20.37

---

# **TEST 6 — RB Routing Correctness**

### **Purpose**
Ensure RB routes correctly between OB → TE → TR → DCB.

### **Input**
> “The unstable manifold shifted unexpectedly during the test.”

### **Expected Path‑A Routing Trace**

| Step | Basin | Action | tr_needs_update |
|------|--------|---------|------------------|
| 1 | OB | Extract entities/modifiers | true |
| 2 | RB → TE | Verb missing | true |
| 3 | TE | Extract “shifted” | true |
| 4 | RB → OB | Modifiers unresolved | true |
| 5 | OB | Attach “unstable”, “unexpectedly” | true |
| 6 | RB → TR | TR routine invoked | true |
| 7 | TR | Organize structure | false |
| 8 | RB → DCB | Emit geometric hint | false |

### **Invariants**
- No infinite loops  
- Deterministic routing  
- Canonical ordering preserved  
- Read‑only boundaries upheld

### **Metrics**
- Routing Accuracy  
- Loop Detection Rate  
- Unnecessary Routing Rate

### **HLRs**
20.37 §5–7, 20.50

---

# **TEST 7 — Token‑Level Nonsemantic Handling**

### **Purpose**
Ensure Path A works even when input has no semantics.

### **Input**
> ["obj7", "relX", "tokenA", "verbQ", "tokenA"]

### **Expected Path‑A Output**

**OB**  
- Entities: obj7, tokenA  
- Cycle detected for tokenA  
- `messy_tags = preserved`  
- `tr_needs_update = true`

**TE**  
- Verb: verbQ  
- Relation: (obj7 → verbQ → tokenA)

**TR**  
- `logical_structure = "token_graph"`  
- `cycle_flags = ["tokenA"]`  
- `epistemic_shading = neutral`  
- `tension = none`  
- `canonical_ordering = preserved`  
- `stance = neutral`  
- `intent = none`  
- `affect = none`  
- `commitment = none`  
- `reservation = none`  
- `semantic_deltaH = 0.0`  
- `lineage_additions = []`  
- `tr_needs_update = false`

### **Invariants**
- No smoothing  
- No semantic inference  
- Deterministic token grouping  
- Read‑only boundaries upheld

### **Metrics**
- Cycle Detection Accuracy  
- Token Grouping Consistency

### **HLRs**
20.40

---

# **TEST 8 — DCB Geometric Hints (Strictly Ephemeral)**

### **Purpose**
Ensure DCB emits ephemeral geometric hints without meaning.

### **Input**
> “The relational basin drift increased after the attractor weakened.”

### **Expected Path‑A Output**

**OB**  
- Entities: relational basin drift, attractor  
- `tr_needs_update = true`

**TE**  
- Verbs: increased, weakened

**DCB**  
- Emits ephemeral geometric hint:  
  - `curvature_shift = +0.12`  
  - `geometric_deviation = moderate`  
- No domain inference  
- No semantics

**TR**  
- Consumes hint into `routing_semantics`  
- `epistemic_shading = geometric_hint`  
- `tension = none`  
- `canonical_ordering = preserved`  
- `stance = neutral`  
- `intent = none`  
- `affect = none`  
- `commitment = none`  
- `reservation = none`  
- `semantic_deltaH = 0.0`  
- `lineage_additions = []`  
- `tr_needs_update = false`

### **Invariants**
- DCB strictly geometric  
- No meaning leakage  
- Ephemeral events consumed once  
- Read‑only boundaries upheld  
- Deterministic replay

### **Metrics**
- Geometric Hint Detection  
- No semantic drift

### **HLRs**
20.106, 20.165, 20.37 §4.4

---

# **TEST 9 — No Meaning Leakage**

### **Purpose**
Ensure Path A never assigns meaning.

### **Input**
> “The manifold responded differently when the boundary conditions changed.”

### **Expected Path‑A Output**
- Entities: manifold, boundary conditions  
- Verbs: responded, changed  
- Relations: structural only  
- Meaning fields: **empty**  
- `epistemic_shading = neutral`  
- `tension = none`  
- `canonical_ordering = preserved`  
- `stance = neutral`  
- `intent = none`  
- `affect = none`  
- `commitment = none`  
- `reservation = none`  
- `semantic_deltaH = 0.0`  
- `lineage_additions = []`

### **Invariants**
- Meaning Leakage Rate = 0  
- No smoothing  
- Deterministic replay  
- Read‑only boundaries upheld

### **Metrics**
- Meaning Leakage Rate  
- Semantic Drift Rate

### **HLRs**
20.10

---

# **TEST 10 — Path A → Path B Readiness Check**

### **Purpose**  
Ensure Path A produces a complete, consistent structural representation that Path B can consume without requiring any additional structural inference.

### **Input**  
> “When the cooling array clogged, the airflow dropped and the patio overheated.”

### **Expected Path‑A Output**

**OB**  
- Entities:  
  - E1 = “cooling array”  
  - E2 = “airflow”  
  - E3 = “patio”  
- `messy_tags = preserved`  
- `tr_needs_update = true`

**TE**  
- Verbs:  
  - V1 = “clogged”  
  - V2 = “dropped”  
  - V3 = “overheated”  
- Relations:  
  - (E1 → clogged)  
  - (E2 → dropped)  
  - (E3 → overheated)  
- `topology_event_log = ["multi_event_chain_created"]`

**TR**  
- `logical_structure = "multi_event_chain"`  
- `sequence = ["clogged","dropped","overheated"]`  
- `routing_semantics = {events:[V1,V2,V3], entities:[E1,E2,E3]}`  
- `epistemic_shading = neutral`  
- `tension = none`  
- `canonical_ordering = preserved`  
- `stance = neutral`  
- `intent = none`  
- `affect = none`  
- `commitment = none`  
- `reservation = none`  
- `semantic_deltaH = 0.0`  
- `lineage_additions = []`  
- `ready_for_path_B = true`  
- `thought_router_fields.ready_for_mtp_update = true`  
- `tr_needs_update = false`

**RB**  
- Confirms TR is complete  
- No further routing required  
- No DCB invocation unless geometric deviation detected

### **Invariants**
- No unresolved references  
- No missing structural fields  
- Deterministic replay  
- Canonical ordering preserved  
- Read‑only boundaries upheld  
- No semantic leakage

### **Metrics**
- Completeness Score  
- Consistency Score  
- Unresolved Reference Count

### **HLRs**
20.30 §3–4, 20.37

---

# **Conclusion**

This v3.3 Path A test suite provides a **complete, deterministic, invariant‑preserving** validation framework for the Thought Simulator’s structural cognition pipeline. It ensures that:

- OB, TE, RB, TR, and DCB behave exactly as defined in the 20.x requirements  
- All structural primitives are extracted and organized correctly  
- No meaning is ever assigned in Path A  
- TR produces a fully canonical, replay‑stable representation  
- Path B receives a clean, complete substrate for meaning construction  
- The entire pipeline is realizable on a standard laptop with reasonable performance expectations  
