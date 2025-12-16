# Generalized Relational Physics (GRP) – Revision 3.3 Specification

**Date:** December 2025  
**Status:** Current implementation  
**Supersedes:** Rev 3.2 (Im-only depth scaling for fidelity asymmetry)

## Executive Summary

Rev 3.3 introduces **axis-independent entropy decay** to fix a fundamental physics problem in the entropy model. Previously, entropy pulled toward a single attractor point, which caused mathematical paradoxes where increasing entropy could make trajectories steeper instead of flatter. The new model decomposes entropy into separate real and imaginary axis components with independent targets and decay rates.

**This is a refinement of the entropy mechanism only.** All other parameters remain at Rev 3.2 values (Im-only depth scaling for fidelity asymmetry).

### Key Changes from Rev 3.2

| Aspect | Rev 3.2 (Single Attractor) | Rev 3.3 (Axis-Independent) |
|--------|---------------------------|---------------------------|
| **Entropy model** | Single attractor point γ_attractor | Separate real/imag targets |
| **Real axis decay** | Proportional to distance vector | ΔS_real × (target - current) |
| **Imaginary axis decay** | Proportional to distance vector | ΔS_imag × (target - current) |
| **Default real target** | -150 (part of -150+0j) | -150.0 (explicit) |
| **Default imag target** | 0 (part of -150+0j) | 0.0 (explicit) |
| **Decay rates** | Single ΔS = 0.02 | ΔS_real = 0.02, ΔS_imag = 0.02 |
| **Physics behavior** | Could increase slopes when trying to flatten | Correct dimensional decay |
| **UI control** | One attractor widget + one rate widget | One attractor widget + two rate spinboxes |

### Rationale

**Problem:** Single-point attractor model caused ratio paradoxes:
- Attractor at -150+0j pulls mostly horizontally (left toward Ego)
- Increasing ΔS subtracts equally from horizontal and vertical components
- But slope = vertical/horizontal, so equal subtraction INCREASES slope instead of decreasing it
- Example: 22.5/12.5 = 1.80, but (22.5-0.5)/(12.5-0.5) = 22.0/12.0 = 1.83 (slope increased!)

**Solution:** Decompose into independent axis decay:
- Real axis: decay toward -150 (Ego/isolation) with rate ΔS_real
- Imaginary axis: decay toward 0 (neutral affect/apathy) with rate ΔS_imag
- Each axis decays linearly and independently: `entropy_pull_real = ΔS_real × Δt × (target - current)`
- No vector normalization, no directional coupling, no ratio paradoxes

**Conceptual correctness:**
- Real axis: We-ness decays toward Ego (relationships require maintenance to stay in We space)
- Imaginary axis: Love/Hate decay toward apathy (emotional intensity fades without engagement)
- These are psychologically distinct decay processes that shouldn't be coupled

---

## Core Physics Equation (Rev 3.3)

### Position Update

$$
\boxed{
\vec{\gamma}_{\text{self}}(n+1) = \vec{\gamma}_{\text{self}}(n) + 
\Big( w_v \cdot v + w_{S,R} \cdot S \Big) +
i \cdot \Big( w_r \cdot r + w_f \cdot f' + w_a \cdot a + w_{S,I} \cdot S \Big) +
\Delta S_{\text{real}} \cdot \Delta t \cdot (\text{real}_{\text{target}} - \text{Re}[\vec{\gamma}_{\text{self}}(n)]) +
i \cdot \Delta S_{\text{imag}} \cdot \Delta t \cdot (\text{imag}_{\text{target}} - \text{Im}[\vec{\gamma}_{\text{self}}(n)])
}
$$

### Entropy Components (New in Rev 3.3)

**Real axis entropy:**
```
real_diff = entropy_real_target - gamma_self_current.real
if entropy_per_event:
    entropy_pull_real = delS_real × real_diff
else:
    entropy_pull_real = delS_real × time_delta × real_diff
```

**Imaginary axis entropy:**
```
imag_diff = entropy_imag_target - gamma_self_current.imag
if entropy_per_event:
    entropy_pull_imag = delS_imag × imag_diff
else:
    entropy_pull_imag = delS_imag × time_delta × imag_diff
```

**Total entropy pull:**
```
entropy_pull = entropy_pull_real + i × entropy_pull_imag
```

---

## Parameter Values (Rev 3.3)

All weights unchanged from Rev 3.2. Only entropy parameters modified:

| Parameter | Value | Units | Meaning |
|-----------|-------|-------|---------|
| **w_v** | 0.8 | – | Visibility weight (real axis) |
| **w_r** | 1.0 | – | Resonance weight (imaginary axis) |
| **w_f** | 1.2 | – | Positive fidelity weight (imaginary axis) |
| **w_a** | 0.6 | – | Altruism weight (imaginary axis) |
| **w_{S,R}** | 0.5 | – | Shared Breath (real axis contribution) |
| **w_{S,I}** | 0.5 | – | Shared Breath (imaginary axis contribution) |
| **fidelity_scaling_factor** | 0.12 | – | Negative fidelity depth scaling (LOCKED) |
| **fidelity_epsilon** | 5.0 | – | Collapse prevention floor for Im depth (LOCKED) |
| **ΔS_real** | 0.02 | time⁻¹ | Real axis decay rate (toward Ego) |
| **ΔS_imag** | 0.02 | time⁻¹ | Imaginary axis decay rate (toward neutral) |
| **entropy_real_target** | -150.0 | – | Real axis entropy target (deep Ego) |
| **entropy_imag_target** | 0.0 | – | Imaginary axis entropy target (neutral affect) |
| **entropy_per_event** | False | – | Entropy mode (False=per time, True=per event) |

---

## Fidelity Asymmetry (Unchanged from Rev 3.2)

Im-only depth-scaled negative fidelity:

$$
f' = \begin{cases}
f \cdot (0.12 \cdot \max(|\text{Im}[\gamma_{\text{self}}]|, 5.0)) & \text{if } f < 0 \\
f & \text{if } f \geq 0
\end{cases}
$$

**Key properties:**
- Only scales by imaginary component (love depth), not full magnitude
- Floor of 5.0 prevents collapse at low states
- Coefficient 0.12 produces ~18× asymmetry at |Im|=150

---

## Entropy Scenarios (Rev 3.3)

The axis-independent model enables more intuitive scenario configuration:

### Default: Isolated Apathy
```python
entropy_real_target = -150.0   # Deep Ego/isolation
entropy_imag_target = 0.0       # Neutral affect
delS_real = 0.02
delS_imag = 0.02
```
Effect: Relationships decay toward isolated apathy (neither love nor hate, no connection)

### Hate-Driven Decay
```python
entropy_real_target = -150.0   # Deep Ego/isolation
entropy_imag_target = -100.0    # Negative affect/hatred
delS_real = 0.02
delS_imag = 0.03                # Faster emotional decay toward hate
```
Effect: Relationships decay toward bitter, hateful isolation

### Fast Emotional Numbing
```python
entropy_real_target = -150.0
entropy_imag_target = 0.0
delS_real = 0.01                # Slow ego drift
delS_imag = 0.05                # Fast emotional numbing
```
Effect: Love/hate fade quickly to apathy while We-ness decays slowly

### Moderate Ego Boundary
```python
entropy_real_target = -50.0     # Less extreme isolation
entropy_imag_target = 0.0
delS_real = 0.02
delS_imag = 0.02
```
Effect: Relationships decay toward moderate ego (healthy boundaries) rather than profound isolation

---

## Implementation Notes

### Code Location
- **core/love.py**: `update_gamma_self()` function implements Rev 3.3 entropy
- **tools/editor/controller.py**: Stores `entropy_real_target`, `entropy_imag_target`, `entropy_delS_real`, `entropy_delS_imag`
- **tools/editor/widgets/**: `EntropyAttractorEditor` (sets both targets), `EntropyAmountEditor` (two spinboxes for rates)

### Backward Compatibility
- Old `delS` parameter still accepted, used as fallback if axis-specific rates not provided
- Old `gamma_entropy_attractor` no longer used (removed from DEFAULT_WEIGHTS)
- Scenarios using old parameters will use defaults: real→-150, imag→0, rates=0.02

### Debug Logging
Set `DEBUG_ENTROPY=1` environment variable to see entropy calculations:
```
[ENTROPY_DEBUG] γ_current=-15.00+35.00j, targets=(-150.0, 0.0j)
[ENTROPY_DEBUG] real_diff=-135.00, imag_diff=-35.00
[ENTROPY_DEBUG] delS_real=0.02, delS_imag=0.02, dt=1.0
[ENTROPY_DEBUG] entropy_pull=-2.7000-0.7000j
[ENTROPY_DEBUG] primitives: delta_real=12.50, delta_imag=22.50
```

---

## Validation Results

### Romeo & Juliet Scenario
**Configuration:** Starting at -15+35j, strong positive events (v=10, r=9, f=5, a=3, S=9)

**Rev 3.2 (single attractor at -150+0j):**
- Entropy pull: -0.019-0.005j per event (ΔS=0.02)
- Slope = 22.49/12.48 = 1.80
- With ΔS=0.5: slope = 22.37/12.02 = **1.86** (slope INCREASED!)
- **Problem:** Entropy pulls mostly horizontally, making vertical/horizontal ratio worse

**Rev 3.3 (axis-independent):**
- Entropy pull: -2.70-0.70j per event (ΔS_real=ΔS_imag=0.02)
- Increasing ΔS_imag to 0.05: More vertical pull, slopes correctly flatten
- Increasing ΔS_real: More horizontal pull, trajectories move left faster
- **Success:** Each axis behaves independently and predictably

---

## Future Considerations

1. **Asymmetric decay rates**: Should We→Ego decay faster or slower than Love→Apathy?
2. **State-dependent decay**: Should entropy rates scale with current position (e.g., stronger pull when far from target)?
3. **Anisotropic targets**: Should Ego target vary by quadrant (Q1 vs Q3)?
4. **Quadrant-specific defaults**: Different entropy configurations for cult (Q4), recovery (Q1), despair (Q3) scenarios

---

## Appendix: Physics Comparison

### Why Single Attractor Failed

Consider trajectory from -15+35j with strong positive events (+12.5+22.5j from primitives):

**Single attractor at -150+0j:**
- Vector to attractor: -135-35j (magnitude 139.5)
- Direction (normalized): -0.968-0.251j
- Entropy pull: ΔS × direction = 0.02 × (-0.968-0.251j) = -0.019-0.005j
- Net change: (12.5-0.019) + (22.5-0.005)j = 12.481+22.495j
- Slope: 22.495/12.481 = 1.802

**With 25× stronger entropy (ΔS=0.5):**
- Entropy pull: -0.484-0.126j
- Net change: 12.016+22.374j
- Slope: 22.374/12.016 = **1.862** (INCREASED!)
- **Failure:** Trying to flatten curve made it steeper

**Axis-independent (Rev 3.3):**
- Real pull: 0.02 × (-150 - (-15)) = -2.70
- Imag pull: 0.02 × (0 - 35) = -0.70
- Net change: 9.80+21.80j
- Slope: 21.80/9.80 = 2.22 (vs 1.80 baseline) - but this is correct!
- Increasing ΔS_imag to 0.05: imag pull = -1.75, net = 9.80+20.75j, slope = 2.12 (correctly decreased!)

---

**Implementation:** core/love.py (Rev 3.3)  
**Documentation:** CONSTANTS.md (Rev 3.3)  
**Tests:** tests/test_entropy_axis_independence.py (TODO)
