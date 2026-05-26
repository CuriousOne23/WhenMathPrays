# 02_tp_lifecycle / software_description.md

## 1. Purpose
This module explores and prototypes the **ThoughtPoint (TP) lifecycle** — the atomic, mobile unit of thought in the Thought Manifold Simulator.

A ThoughtPoint carries identity, entropy, provenance, and relational state as it moves, splits, merges, and evolves.

## 2. Scope & Alignment with Master Guide
- `prototype.py` must be a **pure macro-style module** (self-contained, importable, no top-level execution, deterministic when `deterministic_mode=True`).
- `harness.py` is the **sole execution entrypoint** — it imports the macro, runs verification scenarios, collects evidence, and attaches to requirements.
- All work follows `master_program_guide.md` (philosophy, variable control, macro rules, reporting standards, Verification Capsule process).

## 3. Core Responsibilities (from GRP)
- Carry and metabolize unified entropy (H_rep, H_pred, H_struct)
- Maintain strict identity, monotonic state_counter, and observable provenance/history
- Support movement between basins
- Enable safe split/merge with lineage tracking
- Provide rich observability (history, metrics, state dumps)
- Remain lightweight, deterministic, and parallel-safe

## 4. Key Invariants
- Unique `tp_id` + strictly monotonic `state_counter`
- Entropy components stay non-negative
- Provenance tree is immutable after creation events
- No TP can be in two basins simultaneously
- All public operations are deterministic when `deterministic_mode=True`
- History is append-only (bounded in future iterations)

## 5. Formal Requirement Pointers
High-level requirements live in:
- `thought_simulator_req/10_architecture/` (Manifold, TP, Basins)
- `thought_simulator_req/20_requirements/` (Lifecycle, Entropy, Identity/Provenance, Stability)

Traceability will be maintained in `requirements_traceability.md`.

## 6. Public Macro API (prototype.py)
```python
ThoughtPoint.new(basin_id, entropy, embedding, created_at_tick, energy=1.0)
tp.move_to_basin(basin_id, tick, note="")
tp.update_entropy(tick, d_rep=0, d_pred=0, d_struct=0)
tp.add_tag(tag, tick)
tp.remove_tag(tag, tick)
tp.split(tick, child_count=2) -> list[ThoughtPoint]
ThoughtPoint.merge(sources: list[ThoughtPoint], tick, basin_id=None) -> ThoughtPoint
