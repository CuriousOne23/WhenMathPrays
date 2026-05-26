# 02_tp_lifecycle / software_description.md

## 1. Purpose

This document is a **living, exploratory design sketch** for the ThoughtPoint (TP) lifecycle — the core mobile entity in the Thought Simulator.

It captures our current best understanding of what a ThoughtPoint is, how it evolves, and what responsibilities it holds. This is **not** the final design — it will evolve through prototyping, testing, and insights.

## 2. Core Responsibilities

A ThoughtPoint represents **one active thread of thought** moving through the relational landscape.

It must:
- Carry and update its own **unified entropy** state
- Maintain **identity / provenance** history
- Support **movement** between basins (entry/exit logic)
- Enable **split / merge** operations with proper lineage
- Provide rich observability (state counter, history, metrics)
- Remain lightweight and parallel-friendly

## 3. Key Invariants

* Every ThoughtPoint must have a **unique TP ID** and a **strictly monotonic State Counter**.
* Unified entropy can only decrease (or stay stable) inside Object Basins except under explicit regulator intervention.
* Provenance (creation, splits, merges, basin history) must be preserved and observable.
* A ThoughtPoint must never exist in an inconsistent state (e.g., in two basins at once).
* All operations on a TP must be deterministic and reproducible when `deterministic_mode` is enabled.

## 4. Tentative Data Structure (Current Thinking)

```python
class ThoughtPoint:
    tp_id: str                    # Unique identifier
    state_counter: int            # Strictly monotonic, increments on change
    current_basin_id: str
    entropy: EntropyComponents    # H_rep, H_pred, H_struct (and total)
    embedding: np.ndarray         # Feature vector for similarity/routing
    history: list[HistoryEntry]   # Bounded or configurable depth
    provenance: ProvenanceTree    # Creation, splits, merges
    tags: set[str]                # For routing, regulators, filtering
    energy: float                 # Optional priority/coherence signal
    created_at_tick: int
    last_updated_tick: int