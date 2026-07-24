# 📘 path_b_runtime.md  
### Path B Runtime Execution Contract  
### Thought Simulator — Path B Specification Layer  

---

## 1. Purpose

This document defines **how Path B runs at runtime**:

- exact **execution order** of primitives  
- **preconditions** (what must exist before each primitive runs)  
- **postconditions** (what each primitive must write)  
- **invariants** (what must always be true)  
- the **replay contract** (how to reconstruct Path B from TP + logs)

It ties together:

- `path_b_tp_schema.md`  
- `path_b_logs.md`  
- `path_b_appendix.md`  

into a single, testable runtime spec.

---

## 2. Execution order

Path B primitives run in a **strict sequence** per turn:

1. `REx‑prm` — Expression Extractor  
2. `RPlan‑prm` — Realization Planner  
3. `RPU‑prm` — Realization Plan Updater  
4. `ReB‑prm` — Realization Basin  

No primitive may run out of order.  
No primitive may be skipped.

---

## 3. Runtime contracts per primitive

For each primitive:

- **Preconditions:** what must already exist in TP / logs  
- **Operation:** conceptual role (for humans)  
- **Postconditions:** what must be written to TP / logs  

### 3.1 REx‑prm — Expression Extractor

**Preconditions (TP fields must exist):**

- `TP.message`  
- `TP.intent`  
- `TP.tone_hint`  
- `TP.constraints`  
- `TP.audience`  
- `TP.channel_hint`  
- `TP.semantic_core_ref`  

**Operation (conceptual):**

- Reads Path A meaning fields.  
- Extracts the **expression‑relevant slice** (what matters for realization).  

**Postconditions (must write):**

- `TP.pathB.rex_slice_ref` → new `RefID`  
- `rex_slice_log[RefID]` → expression slice record

If `TP.pathB.rex_slice_ref` is missing after REx‑prm, runtime is in an **invalid state**.

---

### 3.2 RPlan‑prm — Realization Planner

**Preconditions:**

- `TP.pathB.rex_slice_ref` must exist.  
- `rex_slice_log[TP.pathB.rex_slice_ref]` must exist.

**Operation (conceptual):**

- Reads the expression slice.  
- Generates **candidate realization plans** (structure, tone, pacing, channel, constraints).  

**Postconditions:**

- `TP.pathB.rplan_candidates_ref` → new `RefID`  
- `rplan_candidates_log[RefID]` → candidate plans record  
- (optional) `rplan_metadata_log[RefID2]` if metadata is used later

If `TP.pathB.rplan_candidates_ref` is missing after RPlan‑prm, runtime is in an **invalid state**.

---

### 3.3 RPU‑prm — Realization Plan Updater

**Preconditions:**

- `TP.pathB.rplan_candidates_ref` must exist.  
- `rplan_candidates_log[TP.pathB.rplan_candidates_ref]` must exist.  
- TS‑concepts (coherence, style, timing, channel) must be callable.

**Operation (conceptual):**

- Reads candidate plans.  
- Applies governance + coherence + style + timing decisions.  
- Selects a **single final plan** and records all adjustments.

**Postconditions:**

- `TP.pathB.rpu_selected_plan_ref` → new `RefID`  
- `rpu_selected_plan_log[RefID]` → final selected plan  
- `TP.pathB.rpu_adjustments_ref` → new `RefID2`  
- `rpu_adjustments_log[RefID2]` → adjustments record

If either `rpu_selected_plan_ref` or `rpu_adjustments_ref` is missing, runtime is in an **invalid state**.

---

### 3.4 ReB‑prm — Realization Basin

**Preconditions:**

- `TP.pathB.rpu_selected_plan_ref` must exist.  
- `rpu_selected_plan_log[TP.pathB.rpu_selected_plan_ref]` must exist.

**Operation (conceptual):**

- Reads the final plan.  
- Stabilizes pacing, tone, flow, and channel formatting.  
- Produces the **final behavior** to be emitted externally.

**Postconditions:**

- `TP.pathB.reb_output_ref` → new `RefID`  
- `reb_output_log[RefID]` → final behavior summary record

If `TP.pathB.reb_output_ref` is missing, runtime is in an **invalid state**.

---

## 4. Global runtime invariants

These invariants must hold for every valid Path B run.

### 4.1 Meaning vs. realization separation

- Path B **must not modify**:  
  - `TP.message`  
  - `TP.intent`  
  - `TP.topic`  
  - `TP.tone_hint`  
  - `TP.constraints`  
  - `TP.audience`  
  - `TP.channel_hint`  
  - `TP.semantic_core_ref`  
- Path B writes only under `TP.pathB.*`.

### 4.2 Reference‑only writes

- All Path B TP writes are **references** (`RefID`s).  
- No large objects are stored inline in TP.  
- All large objects live in Path B logs.

### 4.3 Immutability

- Log records are **immutable** once written.  
- No primitive may mutate an existing log entry.  
- No primitive may overwrite another primitive’s `RefID` in TP for the same turn.

### 4.4 Single‑pass per turn

- Each primitive runs at most **once per turn**.  
- If a primitive must be re‑run, it must write **new** `RefID`s (no overwrite).

---

## 5. Error conditions

Runtime must treat the following as **hard errors** (or trigger safe fallback):

- Missing required TP fields for a primitive’s preconditions.  
- Missing log entry for a referenced `RefID`.  
- `rplan_candidates_log` contains zero plans.  
- `rpu_selected_plan_log` plan inconsistent with candidates.  
- `reb_output_log` missing after ReB‑prm.  
- Any primitive runs out of order.  
- Any primitive attempts to modify Path A fields.  

These conditions must be detectable and loggable.

---

## 6. Replay contract

Replay of Path B for a single turn uses:

1. `TP.pathB.rex_slice_ref` → `rex_slice_log`  
2. `TP.pathB.rplan_candidates_ref` → `rplan_candidates_log`  
3. `TP.pathB.rpu_selected_plan_ref` → `rpu_selected_plan_log`  
4. `TP.pathB.rpu_adjustments_ref` → `rpu_adjustments_log`  
5. `TP.pathB.reb_output_ref` → `reb_output_log`  

Replay must:

- require **no LLM inference**  
- be **deterministic**  
- reconstruct the full realization pipeline at the level of:  
  - expression slice  
  - candidate plans  
  - selected plan  
  - adjustments  
  - final behavior summary  

---

## 7. Versioning

```text
schema_version: 0.1
last_updated: 2026-06-16
author: CuriousOne (Jeff)

