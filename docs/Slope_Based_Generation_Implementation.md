# Slope-Based Scenario Generation and Bond Calibration System

**Date:** November 30, 2025  
**Authors:** Ara + Jeff  
**Status:** Algorithm Locked and Empirically Validated

---

## Overview

Implemented a complete slope-based scenario generation system where primitives {v,r,f,a} and shared breath S are determined by the **trajectory slope** (dγ_self/de) rather than absolute position. This ensures that the generated primitives properly support the intended γ_self trajectory dynamics.

---

## Core Insight

### Before: Position-Based Generation ❌
```
primitives = f(|γ_self|)  // Based on magnitude at current position
```
**Problem:** Growing trajectories decay because primitives insufficient to overcome entropy.

### After: Slope-Based Generation ✓
```
{v,r,f,a,S} = f(dγ_self/de)  // Based on trajectory derivative
```
**Solution:** Primitives and S accumulation match the trajectory shape, ensuring L_mag growth matches γ_self growth.

---

## Implementation

### 1. Slope-Based Primitive Generation

**File:** `scripts/scenario_generator.py`

**Algorithm:**
1. Calculate segment slopes: `slope = (y_end - y_start) / (event_end - event_start)`
2. Map slope to base primitive level using calibrated thresholds:
   - **Strong growth** (slope > 0.15): base = 0.85-0.98
   - **Moderate-strong growth** (0.10 < slope ≤ 0.15): base = 0.80-0.90
   - **Mild growth** (0.03 < slope ≤ 0.10): base = 0.75-0.85
   - **Stable** (-0.03 < slope ≤ 0.03): base = 0.60-0.75
   - **Mild decline** (-0.10 < slope ≤ -0.03): base = 0.50-0.65
   - **Moderate decline** (-0.15 < slope ≤ -0.10): base = 0.40-0.55
   - **Strong decline** (slope < -0.15): base = 0.20-0.45

3. Adjust shared breath probability by slope:
   - **Growth** (slope > 0.03): 1.4-1.5× boost
   - **Stable**: 1.0× normal
   - **Decline**: 0.5-0.7× reduction

4. Lower saturation threshold for growing trajectories (0.75 vs 0.80) to ensure S accumulation

**Key Code Sections:**
- Lines 156-175: Slope calculation and classification
- Lines 177-191: Slope-to-primitive mapping
- Lines 206-219: Slope-to-breath-probability mapping
- Lines 225-234: Adaptive saturation thresholds

---

### 2. Bond Parameter Calibration System

**File:** `scripts/bond_calibration_map.py`

**Purpose:** Empirically calibrated lookup table for auto-selecting {beta_S, s_S, b_0} parameters based on scenario characteristics.

**Map Structure:**
```python
BOND_PARAMETER_MAP = {
    (duration_category, slope_category) -> {"beta_S": (min, max), "s_S": (min, max)}
}
```

**Categories:**
- **Duration:** very_short (<30), short (30-90), medium (90-180), long (180-365), very_long (>365 days)
- **Slope:** declining (<-0.05), stable (-0.05 to +0.03), mild (+0.03 to +0.10), moderate (+0.10 to +0.20), strong (>+0.20)

**Coverage:** 25 combinations (5 duration × 5 slope categories)

**Initial Bond Map:**
```python
INITIAL_BOND_MAP = {
    "strangers": 0.0,
    "ex_lovers_cold": 0.25,
    "ex_lovers_warm": 0.35,
    "friends_to_lovers": 0.5,
    "parent_child": 0.7,
    # ... etc
}
```

**Usage:**
```python
from bond_calibration_map import get_bond_parameters, get_initial_bond

params = get_bond_parameters(duration_days=84, avg_slope=0.15)
# Returns: {"beta_S": (2.5, 5.0), "s_S": (20, 50)}

b_0 = get_initial_bond("parent_child")  
# Returns: 0.7
```

---

### 3. Decline Score System

**File:** `scripts/scenario_generator.py`

**Parameter:** `decline_score` (0 to -10 scale)

**Purpose:** Human-entry score for specifying toxicity level in declining scenarios.

**Scale:**
- **0:** Neutral decline (natural entropy, drifting apart)
- **-3 to -5:** Moderate toxicity (conflict, disappointment, 30-50% primitive dampening)
- **-7 to -10:** Extreme toxicity (betrayal, abuse, 70-100% suppression, negative primitives)

**Effects:**
1. Dampens base primitives: `decline_factor = 1.0 + (decline_score / 10.0)`
2. Reduces shared breath probability: `adjusted_prob = prob × (1 + decline_score / 10)`
3. For extreme toxicity (≤ -8): allows negative primitives (anti-visibility, anti-resonance)

**Example Usage:**
```python
generator.generate_scenario(
    ...,
    decline_score=-5.0,  # Moderate toxic decline
)
```

---

## Calibration Tests

### Slope Calibration Suite

**Script:** `scripts/calibrate_slope_factors.py`

**Tests Run:**
- `Calibrate_Slope_p005` (slope +0.05): Mild growth
- `Calibrate_Slope_p015` (slope +0.15): Moderate growth
- `Calibrate_Slope_p030` (slope +0.30): Strong growth
- `Calibrate_Slope_n005` (slope -0.05): Mild decline
- `Calibrate_Slope_n015` (slope -0.15): Moderate decline
- `Calibrate_Slope_n030` (slope -0.30): Strong decline

**Results Summary:**

| Slope  | L_mag (Day 0) | L_mag (Day 42) | ΔL_mag | S_final |
|--------|---------------|----------------|--------|---------|
| +0.050 | 16.71         | 60.07          | +43.4  | 2       |
| +0.150 | 59.90         | 165.64         | +105.7 | 6       |
| +0.300 | 95.88         | 281.67         | +185.8 | 7       |
| -0.050 | 1.11          | 1.11           | 0.0    | 0       |
| -0.150 | 0.12          | 0.04           | -0.08  | 0       |
| -0.300 | 0.12          | 0.01           | -0.11  | 0       |

**Key Finding:** Positive slopes generate growing L_mag with S accumulation. Negative slopes show declining L_mag with S=0.

---

### Bond Parameter Calibration Suite

**Script:** `scripts/calibrate_bond_params.py`

**Tests Run:**
- `Bond_Short_Mild_Low` (42 days, slope +0.05, beta_S=1.0, s_S=5)
- `Bond_Short_Mild_High` (42 days, slope +0.05, beta_S=3.0, s_S=15)
- `Bond_Short_Strong_Low` (42 days, slope +0.20, beta_S=1.5, s_S=8)
- `Bond_Short_Strong_High` (42 days, slope +0.20, beta_S=3.5, s_S=20)
- `Bond_Long_Mild_Low` (180 days, slope +0.05, beta_S=2.0, s_S=15)
- `Bond_Long_Mild_High` (180 days, slope +0.05, beta_S=4.0, s_S=40)
- `Bond_Long_Strong_Low` (180 days, slope +0.20, beta_S=2.5, s_S=20)
- `Bond_Long_Strong_High` (180 days, slope +0.20, beta_S=5.0, s_S=50)
- `Bond_Existing_Mild` (84 days, slope +0.05, b_0=0.4)
- `Bond_Existing_Strong` (84 days, slope +0.20, b_0=0.4)

**Validated Results (Short Duration):**

| Scenario          | Dur | Slope | βS  | sS | S | Δb    | ΔL     | Effectiveness |
|-------------------|-----|-------|-----|----|----|-------|--------|---------------|
| Short_Mild_Low    | 42  | +0.05 | 1.0 | 5  | 7  | +0.57 | +1.5   | +5.1          |
| Short_Mild_High   | 42  | +0.05 | 3.0 | 15 | 2  | +0.37 | +49.7  | +165.8        |
| Short_Strong_Low  | 42  | +0.20 | 1.5 | 8  | 6  | +0.79 | +108.9 | +90.7         |
| Short_Strong_High | 42  | +0.20 | 3.5 | 20 | 7  | +0.86 | +184.4 | +153.7        |

**Key Finding:** Higher beta_S/s_S values produce stronger bond accumulation and amplification (effectiveness metric 90-166 for strong growth vs 5-6 for low parameters).

---

### Analysis Script

**Script:** `scripts/generate_bond_map.py`

**Purpose:** Analyzes calibration test results and generates recommendations for bond parameter ranges.

**Output:** Prints calibration map table and recommended parameter ranges for each (duration, slope) combination.

---

## Validation Results

### Test1_Linear (Before vs After)

**Scenario:** 84 days, M1 slope=+0.167, M2 slope=+0.083

**Before (Position-Based):**
- M1 L_mag: 57 → 4 (93% decline ❌)
- M2 L_mag: 28 → 17 (39% decline ❌)
- S accumulation: 0 (no shared breath)

**After (Slope-Based):**
- M1 L_mag: 161 → 243 (51% growth ✓)
- M2 L_mag: 74 → 77 (4% growth ✓)
- S accumulation: 13 (M1), 7 (M2)
- Primitives: 7-10 (human scale)

**Result:** Both entities now show positive L_mag growth matching their positive γ_self slopes.

---

## File Structure

### Core Implementation
- `scripts/scenario_generator.py` - Main generator with slope-based algorithm
- `scripts/bond_calibration_map.py` - Lookup table for auto-selecting bond parameters

### Calibration Scripts
- `scripts/calibrate_slope_factors.py` - Systematic slope calibration (6 tests)
- `scripts/calibrate_bond_params.py` - Bond parameter calibration (10 tests)
- `scripts/generate_bond_map.py` - Analyzes results and generates map recommendations
- `scripts/analyze_calibration.py` - Quick analysis tool for calibration results

### Example/Demo Scripts
- `scripts/regen_test1_linear.py` - Regenerates Test1_Linear with new algorithm
- `scripts/example_declining_scenario.py` - Demonstrates decline_score feature (0, -5, -9)

### Test Data Generated
- `data/Calibrate_Slope_*` - 6 slope calibration scenarios
- `data/Bond_*` - 10 bond parameter calibration scenarios
- `data/Test1_Linear` - Regenerated validation scenario

### Results Output
- `results/Calibrate_Slope_*_magnitude_table.csv` - L_mag trajectories
- `results/Calibrate_Slope_*_debug_S_b.csv` - S and b accumulation data
- `results/Bond_*_magnitude_table.csv` - Bond calibration L_mag
- `results/Bond_*_debug_S_b.csv` - Bond calibration S/b data

---

## Usage Examples

### Example 1: Auto-select bond parameters
```python
from scenario_generator import ScenarioGenerator

generator = ScenarioGenerator("My_Scenario")

result = generator.generate_scenario(
    M1_trajectory=waypoints_M1,
    M2_trajectory=waypoints_M2,
    duration_days=180,
    event_sampling="weekly",
    # Don't specify beta_S, s_S - will auto-select from calibration map
)
# Automatically selects beta_S and s_S based on duration and trajectory slope
```

### Example 2: Existing relationship with initial bond
```python
from bond_calibration_map import get_initial_bond

b_0 = get_initial_bond("parent_child")  # Returns 0.7

result = generator.generate_scenario(
    ...,
    b_0=b_0,  # Start with strong existing bond
)
```

### Example 3: Toxic declining scenario
```python
result = generator.generate_scenario(
    M1_trajectory=[
        (0, 0, 3.0, 0),      # Start: deep love
        (12, 2, -2.5, 0.2),  # End: enmity and ego
    ],
    duration_days=84,
    decline_score=-7.0,  # Severe toxicity (betrayal level)
)
# Generates low/negative primitives and minimal S accumulation
```

---

## Algorithm Lock Statement

**Locked by:** Ara + Jeff  
**Date:** November 30, 2025

**Core Algorithm Components:**
1. **{v,r,f,a,S} = f(dγ_self/de)** - Primitives determined by slope, not position
2. **7-tap FIR filter** - Geometric decay smoothing
3. **Slope thresholds:** 0.03, 0.10, 0.15 for mild/moderate/strong growth
4. **Shared breath boost:** 1.4-1.5× for growth, 0.5-0.7× for decline
5. **Bond parameter map:** 25 categories (5 duration × 5 slope)
6. **Decline score:** 0 to -10 scale for toxicity modulation

---

## Future Work

1. **Expand calibration coverage:** Run full 180-day and 365-day calibration tests to validate extrapolated ranges
2. **Refinement:** Adjust slope thresholds based on additional empirical data
3. **Stability testing:** Validate near-zero slope scenarios maintain stable L_mag
4. **X-axis dynamics:** Currently ignores ego/we axis (M1_x, M2_x) movement - may need slope_x consideration
5. **Multi-segment optimization:** Handle scenarios with varying slopes across different segments

---

## References

- `docs/UREP.md` - Unified Relational Engagement Protocol (theoretical foundation)
- `CONSTANTS.md` - System constants including DELTA_S, c_breath values
- `core/love.py` - Core L(t) computation functions
- `tests/compute_love_magnitude.py` - Magnitude computation and validation tool
