# GRP Revision 3.4: Constant-Force Entropy Model

**Status:** ActGive (December 14, 2025)  
**Supersedes:** Rev 3.3 (Axis-Independent Entropy Decay)  
**Author:** CuriosOne + AI Assistant

---

## Summary

Rev 3.4 fixes a **timeline-length dependency bug** in Rev 3.3's entropy model. The problem was that Rev 3.3 multiplied the entropy effect by the distance from the attractor (`force = rate × distance`), which caused entropy to accumulate linearly with timeline length. Long scenarios (60+ days) experienced excessive drift toward the attractor, while short scenarios (14 days) showed minimal effect. The fix: use **constant-force entropy** where the force magnitude is the same regardless of distance (`force = rate × sign(distance)`), making entropy behavior consistent across all timeline lengths.

**This changes only the entropy force calculation.** All other parameters remain at Rev 3.3 values (separate real/imag targets and decay rates were already correct - the issue was purely the distance multiplication).

## Changes from Rev 3.3

| Aspect | Rev 3.3 (Proportional Force) | Rev 3.4 (Constant Force) |
|--------|------------------------------|--------------------------|
| **Entropy model** | Force proportional to distance | Constant force magnitude |
| **Real axis decay** | ΔS_real × Δt × (target - current) | ΔS_real × Δt × sign(target - current) |
| **Imaginary axis decay** | ΔS_imag × Δt × (target - current) | ΔS_imag × Δt × sign(target - current) |
| **Force magnitude** | Varies with distance | Constant everywhere |
| **Timeline dependence** | Longer timelines → more drift | Same drift per unit time |
| **Physics analogy** | Spring/damping force (F = -k×x) | Constant thrust/drag (F = constant) |
| **Default real target** | -150.0 (too strong) | -10.0 (calibrated) |
| **Default imag target** | 0.0 | 0.0 (unchanged) |
| **Decay rates** | ΔS_real = 0.02, ΔS_imag = 0.02 | Same (unchanged) |

### Rationale

**Problem with Rev 3.3 (Discovered December 14, 2025):**

Rev 3.3's proportional-to-distance model accumulated over time, causing timeline-length dependency:

- **Short timeline (Romeo & Juliet, ~14 days):** Minimal entropy effect, primitives dominate trajectory
- **Long timeline (Single Dating to Love, ~60 days):** Massive entropy drift, trajectory ends deep in Ego territory (-150+0j)
- **Example:** With attractor at -150.0 + 0.0j, 60-day scenario accumulated 60× more drift than 14-day scenario
- **Result:** "Banana curve" - trajectory yanked hard left toward Ego, primitives overwhelmed by accumulating entropy

**Root cause:** Force proportional to distance integrates over time:
```
F = ΔS × (target - current)  ← Large when far from target
total_drift = ∫ F dt = ∫ ΔS × (target - current) dt
            = ΔS × total_time × average_distance
```

Longer timelines → more integration time → more accumulated drift → trajectory dominated by entropy instead of primitives.

**Solution:** Use constant-force model where magnitude is independent of distance:
```
F = ΔS × sign(target - current)  ← Same magnitude everywhere
total_drift = ∫ F dt = ΔS × total_time  ← Linear in time, not distance
```

Now drift per unit time is constant, making entropy a consistent background perturbation rather than timeline-dependent domination.

**Conceptual correctness:**
- **Psychological entropy:** Relationships don't decay "faster when you're far from equilibrium" - decay rate is roughly constant
- **Predictability:** Entropy should provide gentle consistent drift, not overwhelm primitive-driven dynamics
- **Authoring:** Writer shouldn't need to compensate for timeline length when setting entropy parameters

**Observed behavior after fix:**
- Single Dating to Love trajectory ends in We territory (positive real), primitives dominate as intended
- Romeo & Juliet trajectory unchanged (short timeline was already primitive-dominated)
- Entropy provides subtle background drift independent of timeline length

---

## Core Physics Equation (Rev 3.4)

### Position Update

```python
# Compute primitive-driven changes
delta_real = v_weight * v + r_weight * r + f_weight * f + ...
delta_imag = v_weight * v + r_weight * r + f_weight * f + ...

# Constant-force entropy (NEW IN REV 3.4)
real_diff = entropy_real_target - gamma_self_current.real
imag_diff = entropy_imag_target - gamma_self_current.imag

# Direction only (sign), not magnitude
real_direction = sign(real_diff) if real_diff != 0 else 0  # -1, 0, or +1
imag_direction = sign(imag_diff) if imag_diff != 0 else 0  # -1, 0, or +1

# Apply constant force (same magnitude regardless of distance)
entropy_pull_real = (delS_real * time_delta) * real_direction
entropy_pull_imag = (delS_imag * time_delta) * imag_direction

# Total update
gamma_self_next = gamma_self_current + delta_real + 1j * delta_imag 
                  + entropy_pull_real + 1j * entropy_pull_imag
```

### Key Differences from Rev 3.3

**Rev 3.3 (WRONG):**
```python
entropy_pull_real = (delS_real * time_delta) * (target - current)
#                                                ^^^^^^^^^^^^^^^^
#                                                Proportional to distance!
```

**Rev 3.4 (CORRECT):**
```python
entropy_pull_real = (delS_real * time_delta) * sign(target - current)
#                                                ^^^^^^^^^^^^^^^^^^^^
#                                                Only direction, constant magnitude!
```

---

## Default Parameters (Rev 3.4)

### Entropy Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `entropy_real_target` | -10.0 | Gentle Ego drift (was -150.0 in Rev 3.3 - way too strong) |
| `entropy_imag_target` | 0.0 | Neutral affect (unchanged) |
| `delS_real` | 0.02 | Real axis decay rate (unchanged) |
| `delS_imag` | 0.02 | Imaginary axis decay rate (unchanged) |

**Target recalibration:** Rev 3.3's default of -150.0 was calibrated for proportional-force model. With constant force, -150.0 produces excessive drift. Empirical testing (December 14, 2025) found -10.0 provides appropriate subtle drift toward Ego without overwhelming primitives.

### All Other Parameters (Unchanged from Rev 3.3)

Fidelity asymmetry, weight values, and all primitive effects remain identical to Rev 3.3.

---

## Implementation Status

### Code Changes

**File:** `core/love.py`  
**Date:** December 14, 2025  
**Status:** ✅ Implemented and tested

**Changed lines 154-166:**
```python
# Real axis: CONSTANT FORCE toward target (not proportional to distance)
real_diff = entropy_real_target - real_current
real_direction = np.sign(real_diff) if real_diff != 0 else 0
entropy_pull_real = (delS_real * time_delta) * real_direction

# Imaginary axis: CONSTANT FORCE toward target
imag_diff = entropy_imag_target - imag_current
imag_direction = np.sign(imag_diff) if imag_diff != 0 else 0
entropy_pull_imag = (delS_imag * time_delta) * imag_direction
```

### Testing

**Test scenarios (December 14, 2025):**
1. ✅ **Romeo & Juliet (M1):** Short timeline (~14 days) - trajectory shape unchanged, primitives dominate
2. ✅ **Single Dating to Love (M1):** Long timeline (~60 days) - trajectory now ends in We territory, no banana curve

**Validation:** "Fred is now happy and in love, he is in We territory........again." - User validation, December 14, 2025

---

## Migration Notes

### For Existing Scenarios

**If you have scenarios calibrated under Rev 3.3:**

1. **Entropy target values need recalibration:** -150.0 → -10.0 for real axis (15× reduction)
2. **Decay rates unchanged:** delS_real and delS_imag remain at 0.02
3. **Trajectory shapes will change:** Expect less Ego drift, more primitive-driven dynamics
4. **Longer timelines affected most:** 60+ day scenarios will show biggest difference

### Backward Compatibility

Rev 3.4 is **not backward compatible** with Rev 3.3 entropy parameters. The force model changed fundamentally (proportional → constant), requiring parameter recalibration.

To reproduce Rev 3.3 behavior (if needed for research comparison):
1. Set entropy targets much larger (e.g., real target = -150.0)
2. Set decay rates much smaller (e.g., delS_real = 0.001)
3. Effect will be similar but not identical due to different force model

---

## Physics Interpretation

### Entropy as Constant Drag

The constant-force model treats entropy as:
- **Real axis:** Constant "social gravity" toward isolation (Ego), regardless of current We-ness level
- **Imaginary axis:** Constant "emotional friction" toward apathy, regardless of current Love/Hate intensity

This matches psychological intuition better than proportional force:
- Relationships don't decay "faster when you're deeply enmeshed" - decay is fairly constant
- Emotional intensity doesn't fade "faster when you're passionately in love" - cooling is gradual
- Social isolation doesn't pull "harder when you're already connected" - drift toward Ego is steady

### Integration Over Time

Even constant force integrates over time:
```
displacement = force × time
```

But now the displacement is **linear in time**, not **linear in time × distance**:
- **Rev 3.3:** drift = ΔS × time × average_distance (distance-weighted)
- **Rev 3.4:** drift = ΔS × time (constant per unit time)

This makes entropy behavior **predictable** and **timeline-independent** as a rate:
- Same entropy parameters produce same drift per day
- Longer scenarios simply experience more days of drift
- Writer can calibrate entropy once and it works for all timeline lengths

---

## Future Considerations

### Potential Rev 3.5 Topics

**Not implemented, but worth considering:**

1. **Entropy per event vs per time:** Currently uses `time_delta` (continuous time). Could switch to per-event model for even more timeline-independence.

2. **Directional damping near target:** Currently force is constant until you cross the target, then instantly reverses. Could add small "dead zone" near target where force tapers to zero to prevent oscillation.

3. **Nonlinear decay rates:** Could use different decay rates in different regions (e.g., faster decay in extreme regions, slower near equilibrium).

4. **Coupled decay:** Real and imaginary axes currently decay independently. Could add cross-axis effects (e.g., high Love/Hate intensity slows We-ness decay).

5. **Stochastic entropy:** Add random perturbations to make trajectories less deterministic.

---

## References

- **GRP Rev 3.3:** Introduced axis-independent entropy decay, but used proportional-to-distance force
- **Implementation:** `core/love.py` lines 145-180
- **User Guide:** Interactive Editor documentation (entropy attractor widget)
- **Discovery:** Interactive scenario editing session, December 14, 2025

---

**Document Version:** 1.0  
**Last Updated:** December 14, 2025  
**Next Review:** When new entropy physics issues discovered
