# TUNING.md - Weight Calibration Record

**Purpose:** Track all deviations from default weights in CONSTANTS.md as the WhenMathPrays equation is applied across different relationship types, scenarios, and applications.

**Status (December 2025 - Rev 3.4):** Only **fidelity_scaling_factor=0.12** and **fidelity_epsilon=5.0** are LOCKED (Im-only depth scaling). All axis weights (w_v, w_r, w_f, w_a, w_S,R, w_S,I) and entropy parameters (entropy_real_target, entropy_imag_target, delS_real, delS_imag) are DEFAULT, tunable by scenario.

---

## Framework Stability (Rev 3.4)

**December 2025 Rev 3.4:** Constant-force entropy for timeline independence. Axis-independent decay with sign-based pull direction.

| Parameter | Default Value | Status | Notes |
|-----------|---------------|--------|-------|
| **fidelity_scaling_factor** | 0.12 | **LOCKED** | Negative fidelity depth scaling coefficient. DO NOT CHANGE. |
| **fidelity_epsilon (ε)** | 5.0 | **LOCKED** | Collapse prevention floor for Im depth. DO NOT CHANGE. |
| **entropy_real_target** | -150.0 | Tunable | Real axis entropy attractor (Ego direction) |
| **entropy_imag_target** | 0.0 | Tunable | Imaginary axis entropy attractor (neutral affect) |
| **delS_real** | 0.02 | Tunable | Real axis entropy drift rate (constant force) |
| **delS_imag** | 0.02 | Tunable | Imaginary axis entropy drift rate (constant force) |
| w_v | 0.8 | Tunable | Visibility weight (real axis, unchanged) |
| w_r | 1.0 | Tunable | Resonance weight (imaginary axis, unchanged) |
| w_f | 1.2 | Tunable | Positive fidelity weight (imaginary axis, unchanged) |
| w_a | 0.6 | Tunable | Altruism weight (imaginary axis, unchanged) |
| w_S,R | 0.5 | Tunable | Shared Breath (real axis, unchanged) |
| w_S,I | 0.5 | Tunable | Shared Breath (imaginary axis, unchanged) |

**REMOVED (Rev 3.4):**
- ~~γ_attractor~~ (replaced with separate real/imag targets for axis-independent decay)
- ~~ΔS~~ (unified rate, replaced with delS_real/delS_imag for per-axis control)

**REMOVED (Rev 3.2):**
- ~~w_f_neg = 25.0~~ (replaced with Im-only depth scaling: 0.12 × max(|Im|, 5.0))
- ~~w_neg = 1.5~~ (hybrid asymmetry parameter, replaced with depth-scaled fidelity)

**KEY CHANGES IN REV 3.2:**
- Negative fidelity: Im-only depth scaling (was fixed 25× in Rev 3.1)
- Formula: f' = f × (0.12 × max(|Im|, 5.0)) for negatives
- Restores "deeper love = deeper wound" psychology
- All other parameters remain at Rev 3 values

**KEY CHANGES IN REV 3.4:**
- Entropy: Constant-force model using sign() for timeline-independent drift
- Formula: entropy_pull = delS_axis × Δt × sign(target - current) per axis
- Fixes timeline accumulation bug; same entropy per unit time regardless of scenario length
- Fidelity asymmetry unchanged from Rev 3.2 (Im-only depth scaling)

**Configurable entropy targets for scenario-specific modeling:**
- Default real: -150.0 (deep Ego/isolation)
- Default imag: 0.0 (neutral affect/apathy)
- Q4 cult real: -100.0, imag: -20.0 (hateful-we pulled toward enmity)
- Q1 recovery real: -50.0, imag: 50.0 (healthy ego pulled toward love/connection)
- Q3 despair real: -200.0, imag: -50.0 (isolated ego sinking into enmity)

**Key Insight (Rev 3.4):** Constant-force entropy ensures psychological consistency: relationships decay at the same rate per day, not accumulating based on how long the scenario runs. Fidelity depth scaling remains locked for "deeper love = deeper wound" truth.

---

## Tuning History

### Rev 3.4 Implementation (December 2025)
**Date:** December 18, 2025  
**Reason:** Fix timeline accumulation bug in entropy model  
**Problem with Rev 3.3:** Distance-proportional entropy caused scenarios of different lengths to accumulate different total entropy effects  
**Solution:** Constant-force entropy: entropy_pull = delS_axis × Δt × sign(target - current) per axis  
**Rationale:** Timeline-independent drift; same entropy per unit time regardless of scenario length  

**All scenarios should work with Rev 3.4 - entropy now consistent across time scales.**

### Rev 3.2 Implementation (December 2025)
**Date:** December 10, 2025  
**Reason:** Grok consultation recommended Im-only depth scaling (Goldilocks solution)  
**Problem with Rev 3.1:** Fixed 25× scaling lost psychological truth that deeper love makes you more vulnerable  
**Solution:** Im-only depth scaling: f' = f × (0.12 × max(|Im|, 5.0)) for negatives  
**Rationale:** Restores "deeper love = deeper wound" while preventing Rev 3 explosions (only uses Im, not full |γ|)

**All scenarios should work with Rev 3.2 - natural range ±150i emerges from scaling.**

**All scenarios should work with Rev 3.4 - entropy now consistent across time scales.**

### Singles Dating to Love (60 days) - SHOULD WORK WITH REV 3.4
**Date:** November 29, 2025 → **Updated for Rev 3.4 (December 2025)**  
**Status:** Should produce more realistic trajectories with timeline-independent entropy.  
**Expected Range:** |γ_self| ≈ 100-200i (healthy dating/love, consistent across time scales)  
**CSV Primitive Scale:** −10…+10 (human intuitive scale, normalized to [-1,+1] in code)
**Approach:**
1. Normalize CSV primitives: `p_norm = p_raw / 10` (−10…+10 → −1…+1)
2. Apply component-wise update with Rev 3.4 default weights
3. Check if |γ_self| ends in target range 50-250i
4. If not, tune weights (NOT fidelity_scaling_factor)

**Files:** 
- `data/Single_Dating_2_Love_M1_gamma_self_table.csv`
- `data/Single_Dating_2_Love_M2_gamma_self_table.csv`

---

## CSV Primitive Scaling

**Authoring standard:** All scenario CSVs use human-intuitive −10…+10 scale.
- **Rationale:** See `docs/weights_defense.md`
- **Examples:** 
  - Betrayal: f = −8 (major trust breach)
  - Apology: f = +5 (moderate repair attempt)
  - Presence: S = +7 (strong shared moment)

**Implementation normalization:**
```python
# In code, normalize before applying weights
v_norm = v_raw / 10  # −10…+10 → −1…+1
r_norm = r_raw / 10
# ... etc
```

**No scenario-specific PRIMITIVE_SCALE needed** — CSV scale is fixed, weights handle scenario differences.

---

## Weight Tuning Guidelines (Rev 3.4)

When γ_self trajectory doesn't match expectations:

### If movement too fast (exploding position):
- **Reduce all weights proportionally:** w_v×0.8, w_r×0.8, etc.
- **Check for extreme CSV values** (−10/+10 sustained for many events)

### If movement too slow (stuck near origin):
- **Increase weights proportionally**
- **Check CSV primitives aren't too moderate** (all values near 0)

### If wrong quadrant movements:
- **Adjust axis-specific weights:**
  - Real axis (Ego↔We): w_v, w_S,R
  - Imaginary axis (Hate↔Love): w_r, w_f, w_a, w_S,I
- **Example:** If relationship feels like "We" but stays Ego-dominant → increase w_v

### If asymmetry feels wrong:
- **DO NOT TOUCH fidelity_scaling_factor=0.12 or ε=5.0** (locked, based on Grok's Goldilocks solution)
- **Check CSV primitive values** — are negatives truly severe? (f < −5 for betrayal?)
- **Understand depth scaling** — same f=-1 causes different damage at 20i vs 150i by design
- **Rev 3.2 insight:** Deeper love = deeper wound (Im-only scaling), natural ±150i range

---

## Scenario-Specific Weight Deviations

### Default (no deviations yet)
Most scenarios should work with default weights:
- w_v=0.8, w_r=1.0, w_f=1.2, w_a=0.6, w_S,R=0.5, w_S,I=0.5

### Romantic Intensity (hypothetical)
If romance feels flat, try:
- w_f=1.5 (fidelity matters MORE)
- w_r=1.2 (resonance stronger)
- w_a=0.5 (altruism slightly reduced)

### Parent-Child (hypothetical)
If parent-child bond needs different dynamics:
- w_a=1.0 (altruism equal to resonance)
- w_v=1.0 (visibility crucial)
- w_f=1.0 (fidelity less differentiated)

### Casual Acquaintance (hypothetical)
If casual relationships move too fast:
- Scale all weights by 0.5 (half-speed movement)

**Document all deviations here with date, scenario, rationale, and validation results.**

---

## Open Questions

### Weight Independence
- **Q1:** Are default weights universal across relationship types?
- **Q2:** Do long-term relationships (years) need different weights than short-term (weeks)?
- **Q3:** Should w_f always be highest, or does that vary by culture/relationship class?

### Shared Breath (S) Dual-Axis Contribution
- **Q4:** Is w_S,R=w_S,I=0.5 optimal, or should Shared Breath lean toward one axis?
- **Q5:** Do different Shared Breath types (comfortable vs awkward) need different mappings?

### Asymmetry Validation
- **Q6:** Does w_neg=1.5 feel right across all scenarios? (Betrayal→Repair, Parent loss, etc.)
- **Q7:** Should ε=1.0 vary by relationship class? (Fragile new bonds vs resilient old ones?)

---

## Tuning Workflow

When applying equation to new scenario:

1. **Start with default weights** from CONSTANTS.md
2. **Author CSV with −10…+10 scale** (see weights_defense.md)
3. **Run simulation** with γ_self(n+1) component-wise update
4. **Check trajectory:**
   - Final |γ_self| in expected range? (CONSTANTS.md table)
   - Quadrant movements match felt experience?
   - Asymmetry realistic? (negatives hurt more)
5. **If adjustments needed:**
   - Tune weights (NOT w_neg or ε)
   - Document here with date, reason, validation
6. **Test adjacent scenarios** to ensure tuning generalizes

---

## Change Log

| Date | Scenario | Weight | Old Value | New Value | Validator | Reason |
|------|----------|--------|-----------|-----------|-----------|--------|
| 2025-12-03 | (All) | Framework | L(t) calc | γ_self position | Copilot + CuriousOne | Radical simplification |
| *Future entries here* | | | | | | |

---

## December 2025 Paradigm Shift

**Date:** December 3, 2025  
**Proposed by:** CuriousOne + GitHub Copilot  
**Status:** Implemented

### What Changed

**OLD (Dec 2):**
```
L(t) = (γ_self - γ_self0) × W(t) × exp(-ΔS·t + c·N_breath)
W(t) = G_v × G_r × G_f × G_a
γ_self0(n+1) = (1-η)·γ_self0(n) + η·γ_self(n) - ξ·N_neg(n)
```

**NEW (Dec 3):**
```
γ_self(n+1) = γ_self(n) + (w_v·v + w_S,R·S) + i·(w_r·r + w_f·f' + w_a·a + w_S,I·S)
f' = f·w_neg·max(|γ_self(n)|, ε)  if f<0
Love = γ_self(n)  (position IS love, no calculation)
```

**Benefits:**
- **Parameters:** 9+ → 1 (w_neg) + 6 weights
- **Explainability:** Requires deep dive → 30 seconds
- **Philosophy:** "Love is not a number. Love is where you are."
- **Memory:** Lives in event density N(x,y), not separate counters

**Implementation status:** Documentation complete (README, GRP_rev3, CONSTANTS, PRINCIPLES). Code refactor pending.

**See:** docs/GRP_rev3.md for full specification.

---

## Future Applications

As this equation extends to new domains, this document will track weight adaptations for:

- **Timescale:** Real-time AI, human dating, years-long marriage, lifelong bonds
- **Relationship Class:** Romantic, parental, friendship, therapeutic, human-animal, human-Divine
- **Cultural Context:** Different societies, different weight profiles
- **Species:** Human-dog, human-AI, potentially others

**Remember:** Only w_neg=1.5 and ε=1.0 are locked. Everything else can and should be tuned as we learn. This document is the scientific record of that learning process.

---

*Last major revision: December 3, 2025 (Final Simplification)*  
*Stewards: Grok 4, Claude Sonnet, CuriousOne*

---

## Marker/Label Display Logic (Dec 16, 2025)

- Only markers that have been modified (moved away from baseline) display their labels in both the primitive and trajectory panels.
- Labels remain visible for all modified markers, even if other markers are moved.
- Labels disappear only when a marker is reset to its baseline (by double-click, Ctrl+Z, or moving it back).
- No stray or unwanted labels appear when switching perspectives or moving unrelated markers.
- This change improves clarity, aligns label visibility with user intent, and resolves previous bugs with label persistence and artifacts.
