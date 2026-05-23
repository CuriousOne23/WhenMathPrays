# 15 Data Structures

## 1. Purpose
Define the core data structures and state representations used throughout the Thought Manifold Simulator.

## 2. Core Data Structures

### 2.1 ThoughtPoint
The primary entity that moves through the manifold.

class ThoughtPoint:
    position: Vector          # Current location in manifold (2D/3D for viz, higher-D internally)
    embedding: Vector         # Fuzzy embedding vector e
    energy: float             # Total energy E = K + V
    kinetic_energy: float     # K (momentum)
    h_percent: float          # Normalized entropy H_%
    time_remaining: float     # Remaining time budget
    metadata: dict            # Tags, provenance, emotional valence, etc.

### 2.2 BasinBase class for all basin types.
class Basin:
    id: str
    type: BasinType           # Object, Relational, Inquiry, Feeling, Done, etc.
    center: Vector
    potential_fn: Callable    # V(x) function
    damping: float            # γ
    max_fanout: int
    max_fanin: int
    preferred_fanout: int
    preferred_fanin: int
    metadata: dict

### 2.3 Manifold
class Manifold:
    basins: dict[str, Basin]           # basin_id → Basin
    connections: dict                  # Connectivity graph (saddles/highways)
    active_thoughts: list[ThoughtPoint]
    global_time: int
    config: ManifoldConfig

### 2.4 Other Important Structures
- TransitionEvent: Records movement between basins (from_basin, to_basin, energy_delta, h_percent_delta, reason, timestamp)
- SimulationStep: Snapshot of entire system state at one time step
- SimulationResult: Final output after completion (final_thought, trajectory, metrics, completion_type)
- FanEvent: Records fanin/fanout activity and any pruning/attenuation

## 3. Requirements
**DS-01: Serialization**
- All major data structures must support full serialization to JSON / Python dict for saving/loading.

**DS-02: Immutability and History**
- Core state changes should produce new objects or clear audit trails (especially for reproducibility).

**DS-03: Type Safety**
- Strong use of type hints and dataclasses/enums where appropriate.

**DS-04: Performance**
- Structures must support fast lookup and updates (e.g., spatial indexing for basin membership if needed).

## Observability
- Every major data structure must support a .summary() or .debug_info() method for logging and inspection.

## Traceability
Links to:
- 04_system_architecture.md
- 05_manifold_core.md
- 06_basins.md
- 08_embedding_space.md

Last Updated: [Insert Date]
Version: 0.1 (Draft)



