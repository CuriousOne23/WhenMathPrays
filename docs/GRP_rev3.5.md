# Generalized Relational Physics (GRP) – Revision 3.5 Specification

**Date:** December 2025  
**Status:** Current implementation  
**Supersedes:** Rev 3.4 (constant-force entropy)

## Revision History
- **Rev 3.5 (Dec 2025):**
  - Clarified default entropy targets (-150.0, 0.0j) as user-overridable
  - Standardized parameter notation (ΔS_real, ΔS_imag)
  - Cleaned up LOCKED parameter language and tables
  - Removed outdated test references
  - Confirmed and documented constant-force entropy as implemented
  - Improved organization and consistency
- **Rev 3.4:** Introduced constant-force entropy (see prior revision for details)


## Table of Contents

1. [Revision History](#revision-history)
2. [Table of Contents](#table-of-contents)
3. [Executive Summary](#executive-summary)
4. [Core Physics Equation (Rev 3.5)](#core-physics-equation-rev-35)
5. [Parameter Values (Rev 3.5)](#parameter-values-rev-35)
6. [Fidelity Asymmetry](#fidelity-asymmetry)
7. [Entropy Scenarios](#entropy-scenarios)
8. [Implementation Notes](#implementation-notes)
9. [Validation Results](#validation-results)
10. [Future Considerations](#future-considerations)
11. [Appendix: Physics Comparison](#appendix-physics-comparison)

---

## Executive Summary

Rev 3.5 maintains the **constant-force entropy** model, ensuring timeline-independent drift. The default entropy targets are (-150.0, 0.0j), but these may be changed by the user for scenario-specific modeling. All parameter notation is now standardized (ΔS_real, ΔS_imag). LOCKED parameters are clearly listed and described. Outdated test references have been removed. This document reflects the current implementation in core/love.py.

---

## Core Physics Equation (Rev 3.5)

### Position Update

$$
\boxed{
\vec{\gamma}_{\text{self}}(n+1) = \vec{\gamma}_{\text{self}}(n) + 
\Big( w_v \cdot v + w_{S,R} \cdot S \Big) +
i \cdot \Big( w_r \cdot r + w_f \cdot f' + w_a \cdot a + w_{S,I} \cdot S \Big) +
\Delta S_{\text{real}} \cdot \Delta t \cdot \text{sign}(\text{real}_{\text{target}} - \text{Re}[\vec{\gamma}_{\text{self}}(n)]) +
i \cdot \Delta S_{\text{imag}} \cdot \Delta t \cdot \text{sign}(\text{imag}_{\text{target}} - \text{Im}[\vec{\gamma}_{\text{self}}(n)])
}
$$

### Entropy Components (Constant-Force)

**Real axis entropy:**
```
real_diff = entropy_real_target - gamma_self_current.real
real_direction = sign(real_diff)  # -1, 0, or +1
entropy_pull_real = ΔS_real * time_delta * real_direction
```

**Imaginary axis entropy:**
```
imag_diff = entropy_imag_target - gamma_self_current.imag
imag_direction = sign(imag_diff)  # -1, 0, or +1
entropy_pull_imag = ΔS_imag * time_delta * imag_direction
```

**Total entropy pull:**
```
entropy_pull = entropy_pull_real + i * entropy_pull_imag
```

---

## Parameter Values (Rev 3.5)

| Parameter                | Value    | Units   | Meaning                                 | Status   |
|--------------------------|----------|---------|-----------------------------------------|----------|
| **w_v**                  | 0.8      | –       | Visibility weight (real axis)           | Tunable  |
| **w_r**                  | 1.0      | –       | Resonance weight (imaginary axis)       | Tunable  |
| **w_f**                  | 1.2      | –       | Positive fidelity weight (imag axis)    | Tunable  |
| **w_a**                  | 0.6      | –       | Altruism weight (imaginary axis)        | Tunable  |
| **w_{S,R}**              | 0.5      | –       | Shared Breath (real axis)               | Tunable  |
| **w_{S,I}**              | 0.5      | –       | Shared Breath (imaginary axis)          | Tunable  |
| **fidelity_scaling_factor** | 0.12   | –       | Negative fidelity depth scaling         | LOCKED   |
| **fidelity_epsilon**     | 5.0      | –       | Collapse prevention floor (Im depth)    | LOCKED   |
| **ΔS_real**              | 0.02     | time⁻¹  | Real axis decay rate (toward Alone)       | Tunable  |
| **ΔS_imag**              | 0.02     | time⁻¹  | Imaginary axis decay rate (neutral)     | Tunable  |
| **entropy_real_target**  | -150.0   | –       | Real axis entropy target (default)      | Tunable  |
| **entropy_imag_target**  | 0.0      | –       | Imaginary axis entropy target (default) | Tunable  |
| **entropy_per_event**    | False    | –       | Entropy mode (False=per time, True=per event) | Tunable  |

**LOCKED parameters:**
- **fidelity_scaling_factor = 0.12**: Negative fidelity depth scaling coefficient
- **fidelity_epsilon = 5.0**: Collapse prevention floor for Im depth

---

## Fidelity Asymmetry

Im-only depth-scaled negative fidelity:

$$
f' = \begin{cases}
f \cdot (0.12 \cdot \max(|\text{Im}[\gamma_{\text{self}}]|, 5.0)) & \text{if } f < 0 \\
f & \text{if } f \geq 0
\end{cases}
$$

- Only scales by imaginary component (love depth), not full magnitude
- Floor of 5.0 prevents collapse at low states
- Coefficient 0.12 produces ~18× asymmetry at |Im|=150

---

## Entropy Scenarios

The axis-independent model enables intuitive scenario configuration. The default targets are (-150.0, 0.0j), but users may override these for custom scenarios.

### Default: Isolated Apathy
```
entropy_real_target = -150.0   # Deep Alone/isolation
entropy_imag_target = 0.0      # Neutral affect
ΔS_real = 0.02
ΔS_imag = 0.02
```
Effect: Relationships decay toward isolated apathy (neither connection nor disconnection, no connection)

### Hate-Driven Decay
```
entropy_real_target = -150.0   # Deep Alone/isolation
entropy_imag_target = -100.0   # Negative affect/disconnection
ΔS_real = 0.02
ΔS_imag = 0.03                 # Faster emotional decay toward disconnection
```
Effect: Relationships decay toward bitter, disconnection isolation

### Fast Emotional Numbing
```
entropy_real_target = -150.0
entropy_imag_target = 0.0
ΔS_real = 0.01                 # Slow alone drift
ΔS_imag = 0.05                 # Fast emotional numbing
```
Effect: Love/hate fade quickly to apathy while togetherness decays slowly

### Moderate Ego Boundary
```
entropy_real_target = -50.0    # Less extreme isolation
entropy_imag_target = 0.0
ΔS_real = 0.02
ΔS_imag = 0.02
```
Effect: Relationships decay toward moderate alone (healthy boundaries) rather than profound isolation

---

## Implementation Notes

- **core/love.py**: `update_gamma_self()` implements Rev 3.5 constant-force entropy
- **tools/editor/controller.py**: Stores entropy targets and rates
- **tools/editor/widgets/**: Editors for entropy targets and rates
- Old parameters are supported for backward compatibility, but axis-specific rates and targets are preferred

---

## Validation Results

### Romeo & Juliet Scenario
**Configuration:** Starting at -15+35j, strong positive events (v=10, r=9, f=5, a=3, S=9)

- Entropy pull: -2.70-0.70j per event (ΔS_real=ΔS_imag=0.02)
- Increasing ΔS_imag to 0.05: More vertical pull, slopes correctly flatten
- Increasing ΔS_real: More horizontal pull, trajectories move left faster
- **Success:** Each axis behaves independently and predictably

---

## Future Considerations

1. **Asymmetric decay rates**: Should Together→Alone decay faster or slower than Connection→Disconnection?
2. **State-dependent decay**: Should entropy rates scale with current position (e.g., stronger pull when far from target)?
3. **Anisotropic targets**: Should Alone target vary by quadrant (Q1 vs Q3)?
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

**Axis-independent (constant-force):**
- Real pull: 0.02 × sign(-150 - (-15)) = -0.02
- Imag pull: 0.02 × sign(0 - 35) = -0.02
- Net change: 12.48+22.48j
- Slope: 22.48/12.48 = 1.80 (correctly matches expectation)

---

**Implementation:** core/love.py (Rev 3.5)
**Documentation:** CONSTANTS.md (Rev 3.5)
