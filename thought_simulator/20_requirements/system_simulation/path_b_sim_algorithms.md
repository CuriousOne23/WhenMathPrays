# Path B Realization Algorithms Specification

**Document**: path_b_algorithms.md  
**Project**: Thought Simulator (WhenMathPrays)  
**Version**: 1.0 (based on 2026-06-17 Grok simulations)  
**Purpose**: Provide engineers with precise, implementable algorithms for Path B primitives derived from validated simulations.

## 1. Core Principles
- Path B is **read-only** on semantic core (TP/MTP).
- All operations are deterministic under fixed seed.
- No semantic mutation, no meaning invention.
- Constraints bind at plan level.
- Full replay support via logs and reference objects.

## 2. Primitives

### REx-prm (Realization Extractor)
- **Input**: TP state (post-Path A)
- **Output**: Expression slice (dict/reference)
- **Rules**: Extract only expression-relevant fields; never modify TP.
- **Pseudocode**:
```python
def rex_prm(tp_state):
    slice = {
        "intent": tp_state.get("intent"),
        "tone": tp_state.get("tone_hint"),
        "constraints": tp_state.get("constraints", []),
        "audience": tp_state.get("audience"),
        "channel": tp_state.get("channel"),
        # ... other expression fields
    }
    log("rex_slice_log", slice)
    return slice
```

### RPlan-prm (Plan Constructor)
- **Input**: REx slice
- **Output**: List of candidate plans
- **Rules**: Generate structurally valid plans respecting constraints.
- **Pseudocode**:
```python
def rplan_prm(ex_slice):
    candidates = generate_candidates(ex_slice)  # e.g., analogy, bullets, etc.
    log("rplan_candidates_log", candidates)
    return candidates
```

### RPU-prm (Realization Plan Updater)
- **Input**: Candidate plans + governance/coherence rules
- **Output**: Selected & adjusted plan
- **Rules**: Select best plan, apply adjustments, enforce constraints.
- **Pseudocode**:
```python
def rpu_prm(candidates, governance):
    selected = select_best(candidates, governance)
    adjusted = apply_style_timing_channel(selected)
    log("rpu_selected_plan_log", selected)
    log("rpu_adjustments_log", adjustments)
    return adjusted
```

### ReB-prm (Realization Basin / Output Binder)
- **Input**: Finalized plan
- **Output**: Stabilized external behavior + log
- **Rules**: Smooth pacing/tone, prepare output, write final log.
- **Pseudocode**:
```python
def reb_prm(final_plan):
    stabilized = smooth_and_bind(final_plan)
    log("reb_output_log", stabilized)
    return stabilized["output"]
```

## 3. Variables, Constants & Formulas
- **Drift Score**: `abs(meaning_hash_before - meaning_hash_after) == 0.0`
- **Surface Variation Entropy**: Shannon entropy over output tokens across seeds
- **Plan Fidelity**: `matching_steps / total_planned_steps`
- **Replay Hash**: `hash(concatenated_logs + final_output + seed)`
- **Tone Compliance**: cosine similarity or rule-based match (target ≥ 0.95)
- **Seed Sensitivity Index**: variation measure across different seeds

## 4. Execution Flow
```
TP/MTP (read-only) 
    → REx-prm (extract slice) 
    → RPlan-prm (candidates) 
    → RPU-prm (select + adjust) 
    → ReB-prm (stabilize + output)
```

Invariants checked at each handoff. Replay logs written at every step.

## 5. Determinism & Purity Rules
- Fixed seed → identical output
- No writes to TP/MTP
- All randomness bounded to expression layer only
- Global invariant guards on drift and constraints

## 6. Implementation Guidance
- Use immutable data structures for slices/plans.
- Log every primitive with unique IDs for replay.
- Function signatures should match pseudocode above.
- Error handling: return controlled failure state on irresolvable constraints.
- Testing: Run with same seed for replay verification.

This document serves as the bridge from simulation-validated architecture to code. It can be refined as the TS core evolves.
```
