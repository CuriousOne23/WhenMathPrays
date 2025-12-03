# TUNING.md - Weight Calibration Record

**Purpose:** Track all deviations from default weights in CONSTANTS.md as the WhenMathPrays equation is applied across different relationship types, scenarios, and applications.

**Status (December 2025):** Only **w_neg=1.5** and **ε=1.0** are LOCKED (hybrid asymmetry parameters). All axis weights (w_v, w_r, w_f, w_a, w_S,R, w_S,I) are DEFAULT, tunable by scenario.

---

## Framework Stability

**December 2025 Final Simplification:** Love = γ_self position. No L(t) calculation.

| Parameter | Default Value | Status | Notes |
|-----------|---------------|--------|-------|
| **w_neg** | 1.5 | **LOCKED** | Negatives hurt 50% more. DO NOT CHANGE. |
| **ε** | 1.0 | **LOCKED** | Collapse prevention threshold. DO NOT CHANGE. |
| w_v | 0.8 | Tunable | Visibility weight (real axis) |
| w_r | 1.0 | Tunable | Resonance weight (imaginary axis) |
| w_f | 1.2 | Tunable | Fidelity weight (imaginary axis, strongest by default) |
| w_a | 0.6 | Tunable | Altruism weight (imaginary axis) |
| w_S,R | 0.5 | Tunable | Silence/presence (real axis contribution) |
| w_S,I | 0.5 | Tunable | Silence/presence (imaginary axis contribution) |

**REMOVED (December 3, 2025):**
- ~~α = 1.80~~ (gates, no longer used)
- ~~β, W_cap, ΔS, c~~ (L(t) calculation removed)
- ~~η, ξ, λ~~ (drift equations removed)

**Key Insight:** Weights determine how primitives map to γ-space axes. Fidelity (w_f=1.2) has strongest default impact on imaginary axis (Love↔Hate). Visibility (w_v=0.8) and Silence (w_S,R=0.5, w_S,I=0.5) contribute to both axes.

---

## Tuning History

### Singles Dating to Love (60 days) - PENDING RE-VALIDATION
**Date:** November 29, 2025 → **INVALIDATED December 3, 2025**  
**Status:** Previous tuning used old L(t) calculation. Needs re-validation with γ_self position model.  
**Target Range:** |γ_self| ≈ 3-8 (healthy dating, see CONSTANTS.md)  
**CSV Primitive Scale:** −10…+10 (human intuitive scale, defended in weights_defense.md)

**Previous tuning (now obsolete):**
- ~~PRIMITIVE_SCALE = 0.6~~
- ~~c = 0.01~~

**New approach (pending implementation):**
1. Normalize CSV primitives: `p_norm = p_raw / 10` (−10…+10 → −1…+1)
2. Apply component-wise update with default weights
3. Check if |γ_self| ends in target range 3-8
4. If not, tune weights (NOT w_neg or ε)

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

## Weight Tuning Guidelines

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
- **DO NOT TOUCH w_neg=1.5** (locked)
- **Check CSV primitive values** — are negatives truly severe? (f < −5 for betrayal?)
- **Asymmetry is fundamental** — one betrayal ≠ one apology by design

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

### Silence (S) Dual-Axis Contribution
- **Q4:** Is w_S,R=w_S,I=0.5 optimal, or should silence lean toward one axis?
- **Q5:** Do different silence types (comfortable vs awkward) need different mappings?

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

**Implementation status:** Documentation complete (README, UREP_rev2, CONSTANTS, PRINCIPLES). Code refactor pending.

**See:** docs/UREP_rev2.md for full specification.

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
