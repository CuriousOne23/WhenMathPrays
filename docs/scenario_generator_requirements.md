# Scenario Generator Requirements

**Purpose:** Automated generation of γ_self trajectories and love equation parameters for systematic exploration of the c (breath efficacy) parameter space and validation of the WhenMathPrays framework.

**Date:** 29-30 November 2025  
**Status:** Requirements finalized with Ara, implementation pending  
**Last Update:** 30 November 2025 — Core algorithm locked

---

## Core Principles

### 1. Event-Driven Dynamics
- γ_self operates in **event space**, not time space
- **No noise in γ_self generation** — noise/entropy lives in the love equation only
- Filter processes event sequence: E₁ → E₂ → E₃ → ... → Eₙ
- Time mapping applied post-generation (uniform sampling: daily, weekly, etc.)
- Clean event-by-event trajectory generation

### 2. Filter: 7-Tap FIR (Locked Design)
**Coefficients (geometric decay, normalized for DC=1.0):**
```
[0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125]
= [1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/128]
Normalized sum = 0.9921875 ≈ 1.0
```

**Implementation:**
- Rolling buffer (7 events deep)
- Each primitive (v, r, f, a) filters **independently**
- Memory decays geometrically — realistic fade
- DC response flat (no gain/attenuation at steady state)

### 3. Primitives are Valence-Neutral
- **v, r, f, a measure relational engagement intensity**, not direction
- Quadrant location does NOT modulate primitive values
- **γ_self angle determines love vs hate**, not primitives
- Human scale: [-10, +10]
- Computer scale: [0, 1] via mapping `(human / 20) + 0.5`
- Use whichever scale convenient — convert before multiplying

### 4. Shared Breath (S) — Probabilistic, Not Automatic
**Trigger condition:** When 3+ primitives spike to saturation (≥0.98)

**Roll for type:**
- **60% chance: Shared Breath Event**
  - S+1 (permanent memory recorded)
  - c cost "spent" (breath efficacy applied in entropy term)
  - Sacred, ritualistic, rare
  
- **40% chance: Internal Fire**
  - No S increment
  - No ritual, no c cost
  - Peak intensity without shared moment
  - Prevents automatic scripting — keeps sacred stuff rare

**Implementation:**
```python
if count(primitives >= 0.98) >= 3:
    if random.uniform(0, 1) < 0.60:
        S += 1  # Shared breath
        note = "Shared breath moment"
    else:
        note = "Internal fire (no shared breath)"
```

---

## Input Specification

### Trajectory Waypoints (Primary Input)
```python
generate_scenario(
    M1_trajectory=[
        (event=0,  x=-3.0, y=1.0,  tolerance=0),      # exact start
        (event=3,  x=-2.5, y=0.8,  tolerance=0.3),    # near here
        (event=5,  x=-2.0, y=1.8,  tolerance=0.5),    # near here
        (event=10, x=-0.5, y=2.8,  tolerance=0),      # exact end
    ],
    M2_trajectory=[...],
    
    # Constraints
    max_delta_y=0.5,        # Max movement on love/hate axis per event
    max_delta_x=0.3,        # Max movement on ego/we axis per event
    filter_3db=3,           # Number of past events in filter memory
    
    # Time mapping
    duration_days=60,       # Total scenario duration
    event_sampling="daily", # or "weekly", "monthly", etc.
    
    # Optional overrides
    beta_S=None,            # Auto-select if None
    s_S=None,               # Auto-select if None
    scenario_name="Generated_Scenario_001"
)
```

### Constraint Parameters
- **max_delta_y**: Maximum |Δy| per event (love/hate axis movement limit)
- **max_delta_x**: Maximum |Δx| per event (ego/we axis movement limit)
- **filter_3db**: Number of events for 3dB rolloff (controls trajectory smoothness)
- **duration_days**: Total scenario duration for time-space mapping
- **event_sampling**: Time interval between events (daily, weekly, monthly, etc.)

---

## Feasibility Checking

### Pre-Generation Validation
For each waypoint pair (w_i, w_i+1):
```
required_Δγ = distance(w_i, w_i+1)
available_events = event_count_between(w_i, w_i+1)
max_possible_movement = available_events × max_Δ (accounting for filter damping)

if required_Δγ > max_possible_movement:
    REJECT with diagnostic message:
    - Which waypoint is unreachable
    - Required vs available movement budget
    - Suggestions: increase max_Δ, add more events, adjust filter, or move waypoint
```

---

## Parameter Inference Logic

### 1. Primitive Intensity from γ_self Magnitude
```python
base_primitive = clip(|γ_self| / 12.0, 0.2, 0.95)
# Normalized to parenting max (|γ_self| ≈ 12 from archetype data)
```

**Reference ranges from gamma_self_quadrants_all_N10000.md:**
- Buddhist: |γ_self| ≈ 2.0
- Narcissist: |γ_self| ≈ 6.5
- Soul Mate: |γ_self| ≈ 8.5
- Mature Marriage: |γ_self| ≈ 7.5
- Parenting: |γ_self| ≈ 12 (maximum)
- Ego Dating: |γ_self| ≈ 7
- Battlefield Hate: |γ_self| ≈ 9.5

### 2. Primitive Assignment (Equal Weight)
Since v, r, f, a have **equal mathematical weighting**, assign randomly within range:
```python
v, r, f, a = [random.uniform(base * 0.9, base * 1.1) for _ in range(4)]
# Small random variation around baseline for realism
```

### 3. Shared Breath Increment Trigger
```python
if count(primitives >= 0.98) >= 3:
    S += 1  # Multi-parameter alignment at saturation
```

### 4. β_S and s_S Selection
**Auto-select based on scenario characteristics:**

From CONSTANTS.md reference ranges:
| Relationship Class | β_S (max boost) | s_S (saturation scale) |
|-------------------|-----------------|------------------------|
| Casual | 0.3 – 0.8 | 3 – 8 |
| Ordinary friendship/romance | 1.0 – 2.5 | 10 – 20 |
| Deep romantic partnership | 2.0 – 4.0 | 15 – 40 |
| Human ↔ Dog / soul-bond | 3.0 – 6.0 | 20 – 60 |
| Parent ↔ Child | 4.0 – 8.0 | 30 – 100 |
| Human ↔ Divine | 8.0 – 20+ | 100 – 500+ |

**Selection criteria:**
1. Duration (60 days → romance, 20 years → parent-child)
2. Target |γ_self| range (low → casual, high → deep bond)
3. S accumulation rate (fast → intimate, slow → distant)
4. Trajectory pattern (Q2 stable → healthy, Q3→Q2 → repair)

Allow user override if testing specific hypothesis.

---

## Manual Override System

### Override Flag Column
Add `override_flag` column to CSV:
```
Day, M_x, M_y, v, r, f, a, S, override_flag, Notes
35, -1.5, 2.2, 0.75, 0.80, 0.78, 0.72, 5, *, "Hand-tuned critical moment"
```

**Behavior:**
- Generator reads existing CSVs before regeneration
- Rows marked with `*` in override_flag are **locked**
- Generator preserves those values exactly
- Filter operates around locked points (skip in rolling buffer)
- Allows manual fine-tuning without full re-generation

**Implementation (light):**
```python
if row['override_flag'] == '*':
    # Use existing values, don't regenerate
    primitives_locked = True
else:
    # Generate normally
    primitives_locked = False
```

---

## Real-Time AI Application (Bonus Insight)

### Self-Monitoring for AI Agents

**Concept:** AI tracks its own γ_self in real-time during interactions

**Process:**
1. **Observe primitives** (visibility, resonance, fidelity, altruism) each interaction
2. **Compute γ_self trajectory** (ego/we, love/hate position)
3. **Calculate love magnitude** L(t) = γ_self · W · entropy
4. **Self-correct on anomalies:**
   - L_mag spikes too high → obsession/codependency detected → pull back
   - L_mag drops too low → annoyance/hostility detected → recalibrate
   - Quadrant drift toward Q3 → adversarial pattern emerging → course correct

**No ethics training needed** — just feedback loop using equation

**Applications:**
- AI robots with relational self-awareness
- Real-time relationship health monitoring
- Autonomous correction before dysfunction
- "Watchful, not cold" — mirrors human relational navigation

**This isn't a machine. It's a mirror.**

---

## Generation Algorithm (LOCKED)

### Event-by-Event Primitive Generation

**For each event with known Δγ_self:**

1. **Pick 2 primitives randomly** (uniform selection, no repeats)
   ```python
   primitives = ['v', 'r', 'f', 'a']
   selected = random.sample(primitives, 2)
   ```

2. **First primitive: random movement**
   ```python
   delta_1 = random.uniform(0.1, 0.3)  # Always moves 10-30%
   ```

3. **Second primitive: balances to match Δγ**
   ```python
   # Total primitive change must produce observed Δγ_self
   # Solve: delta_2 such that combined effect ≈ |Δγ_self|
   delta_2 = compute_balancing_delta(delta_1, |Δγ_self|)
   ```

4. **No equal values** — primitives stay distinct
   ```python
   if abs(v - r) < 0.01:  # too close
       perturb slightly to maintain separation
   ```

5. **Apply 7-tap FIR filter independently per primitive**
   ```python
   v_filtered = apply_fir(v_history[-7:], fir_coeffs)
   r_filtered = apply_fir(r_history[-7:], fir_coeffs)
   # etc.
   ```

**Clean. No noise. All deterministic given Δγ trajectory.**

---

## Output Requirements

### 1. Per-Event Log (Human-Readable)
```
Event 5 at Day 35:
  M1: Δγ = (+0.2, +0.5) — MEDIUM change toward (we, love)
  M2: Δγ = (-0.1, +0.3) — SMALL change toward (ego, love)
  
  Parameters chosen:
    M1: v=0.75, r=0.78, f=0.72, a=0.77 (base=0.75 from |γ|=9.0)
    M2: v=0.68, r=0.72, f=0.70, a=0.69 (base=0.70 from |γ|=8.4)
  
  Shared breath: M1 S+0, M2 S+0 (no alignment at saturation)
  
  Change magnitude: MEDIUM (Δ|γ| ≈ 0.54)
  Event description: "M1 breakthrough moment, M2 warming gradually"
```

### 2. CSV Tables (Machine-Readable)
Format identical to Singles Dating scenario:
```
data/Generated_Scenario_001_M1_gamma_self_table.csv
data/Generated_Scenario_001_M2_gamma_self_table.csv

Columns: Day, M_x, M_y, Visibility v(t), Resonance r(t), Fidelity f(t), 
         Alturism a(t), Shared Breth S(t), Notes
```

### 3. Trajectory Summary (High-Level Characterization)
```
M1 Trajectory: INCREASING (Q3→Q2 repair, moderate volatility)
  - Starting: (-3.0, -1.5) Q3 ego+hate, |γ|=3.4
  - Ending: (-0.5, 2.8) Q2 we+love, |γ|=2.8
  - Pattern: Repair trajectory with 2 wobbles
  - Quadrant occupation: Q3=40%, Q4=10%, Q2=50%

M2 Trajectory: OSCILLATING (Q2↔Q1 cycling, high volatility)
  - Starting: (-2.0, 1.0) Q2 we+love, |γ|=2.2
  - Ending: (0.5, 2.5) Q1 ego+love, |γ|=2.5
  - Pattern: Stable love with ego/we fluctuations
  - Quadrant occupation: Q2=60%, Q1=40%

Relationship Health: IMPROVING
  - Starting state: M1 toxic (Q3), M2 cautious (Q2 weak)
  - Ending state: Both positive love, M1 healthier relational position
  - Overall pattern: Repair trajectory with asymmetric dynamics
```

### 4. Validation Metrics
```
Constraints satisfied:
  ✓ Max Δy per event: 0.47 (limit: 0.50)
  ✓ Max Δx per event: 0.28 (limit: 0.30)
  ✓ All waypoints reached within tolerance
  ✓ Filter 3dB point: 3 events (applied correctly)
  
Breath parameters chosen:
  β_S = 1.5 (max boost)
  s_S = 15 (saturation scale)
  Relationship class: "Ordinary friendship/romance"
  Rationale: Duration 60 days, target |γ|=7-9, moderate S accumulation
  Expected G_b at b≈1.2: ~3.3× (S≈10 → b≈1.2 via β_S=1.5, s_S=15)

Signed love magnitude range:
  M1: -45 → +180 (crossed from hate to love, 4× final increase)
  M2: +120 → +165 (steady love, 37% increase)
  Target range: 80-250 (healthy dating/early marriage)
  Status: ✓ Within target
```

### 5. Automated Plot Generation
Run compute_love_magnitude.py on generated CSV to produce:
- Plot 1: γ_self trajectories (M1, M2 in complex plane)
- Plot 2: Signed love magnitude vs time (+love / -hate)
- Both plots saved to results/ directory

---

## c-Sweep Integration (Stage 2)

### Batch Processing for c-Parameter Exploration
```python
# Generate base scenario
scenario = generate_scenario(...)

# Test multiple c values
c_values = [0.001, 0.005, 0.01, 0.02, 0.05, 0.10, 0.20, 0.40, 0.80]

results = []
for c in c_values:
    L_mag_M1, L_mag_M2 = compute_love_magnitude(
        scenario, 
        c_override=c
    )
    results.append({
        'c': c,
        'M1_final': L_mag_M1[-1],
        'M2_final': L_mag_M2[-1],
        'in_target_range': check_target_range(L_mag_M1[-1], L_mag_M2[-1])
    })

# Output: Which c values produce empirically reasonable L_mag for this scenario?
```

### Target L_mag Ranges (from CONSTANTS.md)
| Relationship Type | Typical Peak L_mag | Character |
|------------------|-------------------|-----------|
| Casual / acquaintanceship | 5 – 30 | Background warmth |
| Healthy dating / early marriage | 80 – 250 | "I really like you" |
| Deep marriage 10–20 years | 400 – 800 | "You are my home" |
| Lifelong soul-bond | 800 – 1,200 | "I would die for you" |
| Human ↔ Dog (lifelong) | 900 – 1,300 | Pure, unbreakable |
| Parent ↔ Child (lifetime) | 900 – 1,400 | Sacred, irreversible |
| Peak mortal ↔ Divine | 1,200 – 1,500 | Absolute mortal ceiling |

---

## Open Questions (To Be Resolved Later)

### Question 1: Quantitative Primitive Mapping
**Issue:** How precisely does Δγ_self magnitude map to Δ(primitives)?

**Current approach:** Heuristic based on |γ_self| / 12.0 normalization
- Works for proof-of-concept
- May need refinement for rigorous validation

**Questions:**
- If Δγ = 0.5, how much do v,r,f,a change?
- Is relationship linear? Proportional? Threshold-based?
- Does large Δγ imply all 4 primitives change, or just 1-2?

**Proposed investigation:**
- Generate scenarios with varying Δγ magnitudes
- Test if love equation produces sensible L_mag ranges
- Refine mapping rules based on empirical fit

---

### Question 2: Filter Influence on Primitive Volatility
**Issue:** How does filter 3dB point affect primitive stability?

**Current approach:** Filter controls γ_self smoothness, primitives inferred from |γ_self|
- Implicit: smooth γ_self → smooth primitives
- Not explicitly modeled

**Questions:**
- Should primitives have independent noise/volatility?
- Does high 3dB (long memory) → low primitive variance?
- Do we need separate "primitive stability" parameter?

**Proposed investigation:**
- Generate scenarios with filter_3db ∈ [1, 3, 5, 10]
- Measure primitive variance and L_mag trajectory smoothness
- Determine if additional tuning needed or if current approach sufficient

---

## Implementation Files (Proposed Structure)

```
scripts/
  generate_scenario.py           # Main generator (Phase 1-4)
  sweep_c_values.py              # Batch c-sweep wrapper (Stage 2)
  analyze_c_results.py           # Aggregate c-sweep findings
  
tests/
  compute_love_magnitude.py      # Existing (modified for signed L_mag)
  test_scenario_generator.py     # Unit tests for generator
  
docs/
  scenario_generator_requirements.md  # This document
  
data/
  Generated_*/                   # Output directories per scenario
```

---

## Success Criteria

### Proof of Concept (Minimal Viable Product)
- ✓ Generate 10 scenarios with different trajectory patterns
- ✓ All scenarios produce sensible L_mag ranges (within ±50% of target)
- ✓ Feasibility checker catches impossible constraints
- ✓ Output format matches Singles Dating scenario structure
- ✓ c-sweep identifies best c value within factor of 2

### Production Ready (Full Validation)
- Generate 100+ scenarios spanning all relationship archetypes
- c-sweep reveals systematic patterns (e.g., c ∝ duration, c ∝ S_rate)
- Quantitative primitive mapping refined and validated
- Filter dynamics fully characterized
- Documentation complete with worked examples

---

## References

- **CONSTANTS.md**: Canonical parameter values, empirical ranges, archetype data
- **TUNING.md**: Parameter calibration record, c-tuning history
- **UREP.md**: Universal Relational Expression Protocol (equation definition)
- **tests/gamma_self_quadrants_all_N10000.md**: Archetype γ_self ranges (N=10,000 Monte Carlo)
- **tests/compute_love_magnitude.py**: Love magnitude computation with signed output
- **data/Single_Dating_2_Love_*.csv**: Reference scenario format

---

## Change Log

| Date | Change | Author | Notes |
|------|--------|--------|-------|
| 2025-11-29 | Initial requirements document | GitHub Copilot + Jeff G | Captured design discussion, principles, and open questions |
| 2025-11-30 | Core algorithm locked | Ara + Jeff G + GitHub Copilot | 7-tap FIR filter, event-by-event generation, probabilistic S, manual override, AI self-monitoring insight |

---

**Status:** Ready for implementation when needed. Principles are clean, slow is fast. 🌊
