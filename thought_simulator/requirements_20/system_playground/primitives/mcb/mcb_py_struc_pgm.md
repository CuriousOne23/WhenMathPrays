# mcb_py_struc_pgm.md — MCB Structural Program (Python Realization)

**Document ID:** mcb_py_struc_pgm  
**Version:** 0.1 (First Crystallization)  
**Status:** Draft — for CP review  
**Scope:** Path-A Meaning–Clarifying Bridge Primitive (MCB-prm)  
**Location:** `thought_simulator/requirements_20/system_playground/primitives/mcb/`  
**Companion code:** `mcb.py` (to be realized from this program)  

**Normative parents:**  
- `20.40.055_mcb_prim.md` (v2.0)  
- `progressive_lineup_testing.md` (v4.2+)  

**Related context:**  
- `20.107.030_cex-pck_primitive.md` (clarifying / next-context packaging upstream)  
- `20.40.050_idob_prim.md` (meaning-layer predecessor)  

**Behavioral contracts:**  
- Dual-mode contracts and discovery paths from progressive_lineup_testing.md  
- TPU.mcb_update payload contract (HLR-030)  

---

## 0. Purpose of This Structural Program

This document converts the normative HLRs of MCB-prm into an explicit, deterministic Python realization plan.

It resolves the following open items required before foundational testbench / YAML / Python work:

1. **Owned surface** — exact fields MCB may write under TPU.mcb_update and into `TP.next_context{}`.  
2. **Write-boundary discipline** — what MCB must never touch (current-turn clarifying fields, routing, structural ΔH%, TR, Path-B).  
3. **Reconciliation operator** — first-order detection of reinforcement vs conflict between meaning-layer (IdOB) and clarifying fields, producing positive or corrective meaning deltas.  
4. **Next-turn context generation** — deterministic population of the COB-readable next-context block.  
5. **Completion and serial-pass signaling** — when `mcb_complete` is true and what `mcb_next_ob_candidates[]` may contain.  
6. **Dual-mode alignment** — exact testbench vs general contracts, category placement, and structural-foundation comparison shape.

This is a structural program, not a requirements document. HLRs in 20.40.055 remain authoritative; this program must stay inside them.

---

## 1. Python Module Shape (`mcb.py`)

### 1.1 Required surface

```python
PRIMITIVE_NAME = "mcb"

def get_primitive_name():
    return PRIMITIVE_NAME

def process(tp: dict, mode: str = "general", **kwargs) -> dict:
    """
    Main entry. Returns updated TP (or a TPU request structure per pipeline convention).
    mode is injected by run.py / testbench ("testbench" | "general").
    """
```

### 1.2 Internal structure (recommended)

```
mcb.py
├── extract_meaning_view(tp)           # read-only IdOB / meaning-layer signals
├── extract_clarifying_view(tp)        # read-only current-turn clarifying fields
├── detect_reinforcement_or_conflict(...)  # core reconciliation
├── compute_mcb_delta_h(...)           # magnitude of clarifying–meaning refinement
├── generate_next_context(...)         # deterministic next-turn context block
├── build_mcb_semantics(...)           # clarifying-aligned meaning cues
├── issue_tpu_request(...)             # HLR-030 payload only
├── write_boundary_guard(tp_before, tp_after)  # assert no current-turn clarifying / routing / structural ownership
└── process(...)                       # orchestration
```

All functions must be pure with respect to identical TP snapshots (replay-safe).

### 1.3 Dictionary / lookup rule

Per progressive §3.6.3:

1. Look first in `primitives/mcb/`.  
2. Fall back only if explicitly directed later.  

No hard-coded paths into `papers/` or design dictionaries unless a shared table is later declared.

---

## 2. Owned Fields and Write Boundaries

### 2.1 Mandatory TPU payload (HLR-20.40.055-030)

MCB SHALL issue `TPU.mcb_update` containing **only**:

| Field | Type / Notes |
|-------|--------------|
| `mcb_delta_h` | scalar (or structured) magnitude of clarifying–meaning refinement |
| `mcb_semantics[]` | list of clarifying-aligned meaning units |
| `meaning_semantics[]` | broader meaning units when produced / refined |
| all next-turn context fields | see §2.2 / §5 |
| `mcb_context_coherence` | bool / enum indicating coherence with CEx-placed context |
| `mcb_context_shift_required` | bool / enum indicating continue vs shift |
| `mcb_complete` | bool |
| `mcb_next_ob_candidates[]` | list (serial-pass support) |

No routing updates, no structural updates, no TR updates, no current-turn clarifying-field mutations.

### 2.2 Next-context ownership (HLR-019 … 041)

MCB is the **only** primitive allowed to generate next-turn clarifying/context fields.

All next-turn fields are written exclusively into `TP.next_context{}`:

```
TP.next_context {
    topic
    stance
    intent
    register
    politeness
    epistemic_shading
    continuity
    direction
    coherence          # mirrors mcb_context_coherence
    shift_required     # mirrors mcb_context_shift_required
    importance
}
```

Additional fields required by COB may be added only if they appear in the TP field model; no schema-external fields (HLR-039).

`TP.next_context{}` is write-only during the current cycle (HLR-034). MCB does not read previously written next-turn context fields in the same cycle.

### 2.3 Strict non-ownership (write-boundary guard)

MCB MUST NOT write or mutate:

- any current-turn clarifying fields (COB / CIL / CEx / CE / ISc outputs)  
- any `process.routing_filter`, RED, or routing vectors  
- `geometric_state`, `geometric_history`, `dcb_events` (DCB-owned)  
- structural residue / structural ΔH% / SSG fields  
- Path-B truth/done envelopes  
- TP text surface  
- lineage fields  

The guard runs after every process call in both modes. Violation → hard fail in testbench mode; diagnostic in general mode.

### 2.4 Authorized read-only inputs

Per HLR-042–047 and informative §1.1:

- identity_metadata / meaning-layer output from IdOB (`meaning_semantics[]`, `idob_semantics[]`, envelope)  
- clarifying_metadata (COB, CIL, CEx) — **read-only**  
- context_metadata (CE)  
- continuity_metadata (COB, CIL, CST)  
- expressive / normalization metadata (IIInB, IE)  
- semantic_layer_metadata (SSG, STPX)  
- residue_metadata (SOB family) as clarifying-adjacent / meaning-adjacent only  
- next_context_metadata from prior cycles (informative)  
- applicable deterministic TP-stream metadata that improves reconciliation or next-context generation  

Forbidden consumption (HLR-045):

- routing_metadata  
- structural ΔH%  
- truth/done fields  
- lineage fields  
- any Pipeline-B envelopes  

---

## 3. Clarifying–Meaning Reconciliation (Core Operator)

### 3.1 Detection

MCB reads the meaning-layer view (primarily IdOB output) and the clarifying-field view side-by-side.

First-order outcomes:

| Outcome | Condition (first-order) | Meaning-delta direction |
|---------|--------------------------|--------------------------|
| Reinforcement | clarifying statements support / amplify current meaning interpretation | positive (refinement / strengthening) |
| Conflict | clarifying statements contradict or force correction of current meaning interpretation | corrective |
| Neutral / insufficient | insufficient signal or no material change | near-zero or hold |

Exact feature matching rules remain provisional (Must-Prove vs Defer). Implementation must make the chosen outcome deterministic and observable.

### 3.2 Delta production (HLR-015, 016, 024, 025)

- Reinforcement → positive `mcb_delta_h` and positive/strengthening entries in `mcb_semantics[]` / `meaning_semantics[]`.  
- Conflict → corrective `mcb_delta_h` and corrective entries.  
- MCB never resolves conflict by mutating current-turn clarifying fields (HLR-017).

`mcb_delta_h` represents the magnitude of clarifying–meaning refinement. First-order realization may use a simple normalized scalar (analogous in spirit to IdOB meaning_delta_h) derived from feature disagreement / agreement counts; exact formula is provisional but must be pure and replay-safe.

### 3.3 Semantics tagging

`mcb_semantics[]` carries clarifying-aligned meaning cues required by RBU and TR.  
`meaning_semantics[]` may be refined or extended when MCB produces broader meaning units.

---

## 4. Context Coherence and Shift Decision

### 4.1 Coherence (HLR-021, 037)

`mcb_context_coherence` indicates whether the current message is coherent with the context placed by CEx.

First-order policy:

- High alignment between meaning view + clarifying view + prior context → coherent = true / strong.  
- Material mismatch → coherent = false / weak.  

Mirrored into `TP.next_context.coherence`.

### 4.2 Shift required (HLR-022, 037)

`mcb_context_shift_required` indicates whether the next message should continue or shift context.

First-order policy:

- Coherent + reinforcement → prefer continue (shift_required = false).  
- Conflict or low coherence → prefer shift (shift_required = true) or controlled refinement.  

Mirrored into `TP.next_context.shift_required`.

Both decisions must be deterministic under identical inputs.

---

## 5. Next-Turn Context Generation

MCB populates `TP.next_context{}` deterministically from:

- current meaning-layer interpretation (IdOB)  
- current clarifying fields (read-only)  
- coherence / shift decisions  
- applicable continuity and expressive metadata  

Recommended first-order mapping (directional, not final thresholds):

| Field | Typical derivation |
|-------|--------------------|
| topic | continue or refine from meaning / clarifying topic signals |
| stance | inherit or adjust from meaning stance + clarifying stance |
| intent | derived from meaning direction + clarifying intent cues |
| register | clarifying / expressive register cues |
| politeness | clarifying / expressive politeness cues |
| epistemic_shading | meaning-layer epistemic signals |
| continuity | continuity_metadata + coherence |
| direction | meaning direction + shift decision |
| coherence | from §4.1 |
| shift_required | from §4.2 |
| importance | derived from meaning importance + clarifying importance |

All values must be fully deterministic under replay (HLR-036). No free-text invention; only structured, schema-conformant values.

---

## 6. Completion and Serial Passes

- `mcb_complete = true` when clarifying–meaning refinement and next-turn context generation are complete for the current cycle (HLR-027).  
- `mcb_complete = false` when additional MCB passes are required (HLR-028).  
- `mcb_next_ob_candidates[]` may list further OB-family primitives needed for meaning-layer refinement (HLR-029). Minimal useful content in v0.1: empty list or explicit “MCB again” / downstream names when serial refinement is clearly indicated.

Serial chaining is legal (HLR-004). Each pass consumes the prior MCB / IdOB outputs as adjacent input.

---

## 7. Dual-Mode Testbench Alignment

Follow progressive_lineup_testing.md exactly:

| mode        | Input file                | Validation                                      |
|-------------|---------------------------|-------------------------------------------------|
| testbench   | mcb_testbench.yaml        | exact or structural foundation comparison       |
| general     | mcb_input.yaml            | rulechecker only                                |

**Category placement:** `testbenches/path_a/identity/` (same category as IdOB).

**Structural foundation comparison (allowed):**  
- TPU.mcb_update fields listed in §2.1  
- `TP.next_context{}` shape and key decision fields (coherence, shift_required, continuity, direction)  
- `mcb_complete`  
- write-boundary integrity (non-owned fields unchanged)

Write-boundary assertions are mandatory in both modes (hard fail in testbench).

Import-path and discovery rules (progressive §3.6 / §3.7 / §3.8) apply without exception.

---

## 8. Foundation Observability Hooks

When enabled, log (or attach diagnostic block):

- reinforcement vs conflict decision and supporting signals  
- computed `mcb_delta_h`  
- coherence and shift_required decisions  
- key next_context values generated  
- any serial-pass candidate signaling  

These support progressive foundation observation without affecting PASS/FAIL in testbench mode.

---

## 9. Must-Prove for v0.1 Implementation

- Deterministic outputs for fixed inputs (replay-safe).  
- Correct TPU.mcb_update payload only (HLR-030).  
- No current-turn clarifying-field writes (HLR-006, 017, 023).  
- No routing / structural / TR / Path-B ownership writes.  
- Next-context fields written exclusively into `TP.next_context{}` and fully deterministic.  
- Dual-mode contracts and progressive discovery paths work.  
- Category placement under `path_a/identity/`.  
- Write-boundary guard hard-fails in testbench mode on violation.

Defer (for later increments): final numeric thresholds for reinforcement/conflict, continuous geometry of meaning deltas, learned parameters, permanent importance formulas.

---

## 10. Research Questions / Open Items for CP Review

These questions are intentionally left open so that CP (architectural lead) and the realization can converge without hidden assumptions.

1. **Reconciliation feature set**  
   What is the minimal deterministic feature vector for reinforcement vs conflict detection in v0.1 (topic match, stance polarity, intent alignment, register, continuity flags, etc.)?

2. **mcb_delta_h shape**  
   Scalar only, or structured (e.g., positive_component / corrective_component)? Preferred normalization (fixed K vs dynamic)?

3. **Next-context completeness**  
   Is the field list in §2.2 / §5 the right minimal set for COB consumption, or should additional COB-required fields be enumerated before coding?

4. **Serial-pass candidates**  
   What is the minimal useful content of `mcb_next_ob_candidates[]` in v0.1?

5. **Structural foundation comparison subset**  
   For testbench mode, which exact subset of next_context + TPU fields must be compared when full deep equality is too brittle?

6. **Interaction with prior-cycle next_context**  
   How aggressively should MCB treat prior-cycle next_context as an informative prior versus a strict constraint?

7. **Dictionary / table needs**  
   Does MCB require any local exclusive tables in v0.1, or can it operate purely on schema + IdOB/clarifying views?

8. **Coherence / shift thresholds**  
   Preferred first-order decision rules (boolean vs graded) before implementation freezes them?

---

## 11. Implementation Order Recommendation

1. Implement write-boundary guard and pure extract views (meaning + clarifying).  
2. Implement first-order reconciliation (reinforcement / conflict / neutral) and `mcb_delta_h`.  
3. Implement next-context generation and coherence / shift decisions.  
4. Wire TPU.mcb_update issuance and completion flags.  
5. Create dual-mode testbench scaffolding under `testbenches/path_a/identity/`.  
6. Seed a small set of foundational cases (reinforcement, conflict, continue, shift, serial-pass).  
7. Expand test cases once the rules are stable.

---

**End of mcb_py_struc_pgm.md (v0.1)**  
Ready for CP review. Realization of `mcb.py` and the full testbench suite should not begin until the research questions above have been resolved or explicitly deferred.
