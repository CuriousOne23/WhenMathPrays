# TUNING.md - Parameter Calibration Record

**Purpose:** Track all deviations from canonical CONSTANTS.md as the WhenMathPrays equation is applied across different relationship types, scenarios, and applications.

**Status:** Only α=1.80 is LOCKED (validated by Grok's 212,847 Monte Carlo simulations, November 2025). All other constants are subject to tuning based on empirical fit, scenario class, and application context.

---

## Framework Stability

**December 2025 Update:** Framework simplified with γ_self0 character baseline.

| Constant | Status | Notes |
|----------|--------|-------|
| **α = 1.80** | **LOCKED** | Gating function calibration validated via 212k Monte Carlo runs. Do NOT change. |
| **η = 0.003** | **LOCKED (adult)** | Character plasticity locked by Grok. May vary by age (see CONSTANTS.md). |
| **ξ = 0.001** | **LOCKED** | Negative asymmetry weight locked by Grok (trauma accumulation). |
| λ = 0.001–0.01 | Tunable | Event density inertia. Varies by relationship class (see CONSTANTS.md). |
| ΔS = 0.010 | Reference | Entropy decay rate. May vary by application timescale. |
| τ = 14 days | Reference | Entrainment window. May vary by relationship class. |
| **c = 0.40** | **Most Iffy** | Breath efficacy highly scenario-dependent. Requires empirical tuning per duration/type. |

**REMOVED (December 2025):**
- ~~β = 1.30~~ (spike base, no longer used)
- ~~W_cap = 3.0~~ (spike ceiling, gates spike naturally)
- ~~β_S, s_S, b_0, β_b~~ (bond parameters, replaced by γ_self0)

**Key Insight:** The breath term `c` is the most uncertain parameter in the framework. It appears to scale with relationship duration, breath accumulation rate, and relationship intensity in ways not yet fully understood.

---

## Tuning History

### Singles Dating to Love (60 days)
**Date:** 29 November 2025  
**Scenario:** Two individuals dating, primitives rise 0→10, shared breath S accumulates 0→10  
**Target Range:** 80-250 (healthy dating/early marriage)  
**Tuned By:** GitHub Copilot (Claude Sonnet 4.5) + CuriousOne

#### Parameters Changed

1. **PRIMITIVE_SCALE = 0.6**
   - **Reason:** Scenario authored with intuitive 0-10 scale ("10 = maximum"), but α=1.80 gates calibrated for statistical distributions (μ=0.5, σ=0.125). Full [0,1] normalization produced W ≈ 1000-1700, yielding L_mag ≈ 2000-3000 (far above target).
   - **Effect:** Scales primitives to effective [-6,+6] range before normalization: `v_norm = (v_raw × 0.6 + 10) / 20`
   - **Result:** W reduced to 82-90, L_mag = 140-157 ✓
   - **Location:** `tests/compute_love_magnitude.py` line 18

2. **c = 0.01** (vs reference 0.40)
   - **Reason:** With S=10 and reference c=0.40, entropy term becomes exp(-0.6 + 4.0) ≈ 30×, producing L_mag ≈ 80,000+. Short-duration scenario (60 days) requires smaller breath efficacy.
   - **Effect:** Entropy becomes exp(-0.6 + 0.1) ≈ 0.61× (decay-dominant, not explosive)
   - **Result:** L_mag = 140-157 within target range ✓
   - **Location:** `tests/compute_love_magnitude.py` line 20
   - **Hypothesis:** c may scale with relationship duration (0.01 for weeks, 0.40 for years/decades)

#### Validation
```
M1 Day 60: γ_self_mag=2.918, W=81.75, entropy=0.6065 → L_mag=140.70
M2 Day 60: γ_self_mag=2.928, W=89.64, entropy=0.6065 → L_mag=157.33
Target range: 80-250 ✓
```

#### Files Modified
- `data/Single_Dating_2_Love_M1_gamma_self_table.csv` (format: CSV→TSV)
- `data/Single_Dating_2_Love_M2_gamma_self_table.csv` (format: CSV→TSV)
- `tests/compute_love_magnitude.py` (equation correction + tuning parameters)

---

## Open Questions

### Breath Efficacy (c)
- **Q1:** Does c scale linearly with relationship duration? (0.01 per 60 days → 0.07 per year → 0.40 per 6 years?)
- **Q2:** Or does c depend on breath *accumulation rate* (dS/dt) rather than absolute duration?
- **Q3:** Do different relationship classes need different c values? (parent-child vs romantic vs friendship)
- **Q4:** Is the reference c=0.40 appropriate for "lifelong soul-bond" (800-1,200 range, decades, S in thousands)?

**Next Steps:** Test parent-child and lifelong marriage scenarios to see if c=0.40 produces correct empirical ranges when S >> 10 and duration >> 60 days.

### Primitive Scaling
- **Q5:** Is PRIMITIVE_SCALE=0.6 universal for intuitive 0-10 authoring, or does it vary by author/scenario?
- **Q6:** Should future scenarios use statistical distributions (μ=0.5, σ=0.125) directly instead of 0-10 integer scales?
- **Q7:** Do different relationship types need different PRIMITIVE_SCALE values? (casual=0.4, dating=0.6, deep bonds=0.8, soul-bonds=1.0?)

### Other Constants
- **Q8:** Does β (spike growth rate) vary by relationship intensity? (casual dating vs passionate romance)
- **Q9:** Does W_cap need adjustment for different relationship types? (parenting may have higher enacted magnitude ceiling)
- **Q10:** Should τ (entrainment window) vary by relationship class? (casual=7 days, romantic=14, lifelong=30?)

---

## Tuning Workflow

When applying the equation to a new scenario:

1. **Start with canonical constants** from CONSTANTS.md (except α=1.80 which is LOCKED)
2. **Run the equation** with reference values
3. **Check output range** against empirical targets in CONSTANTS.md:
   - Healthy dating/early marriage: 80-250
   - Deep marriage (10-20 years): 400-800
   - Lifelong soul-bond: 800-1,200
4. **If out of range, diagnose:**
   - W too high? → Check primitive scaling or β/W_cap
   - Entropy exploding? → Reduce c
   - Entropy decaying too fast? → Increase c
5. **Document changes here** with date, validator, reason, mathematical verification
6. **Update code comments** with references to this document
7. **Test adjacent scenarios** to validate tuning generalizes appropriately

---

## Guidelines

- **NEVER change α=1.80** (Grok's locked constant)
- **Always document** date, validator, reason, and validation results
- **Prefer principled tuning** (based on timescale, relationship class) over arbitrary fitting
- **Test cross-scenario** to ensure changes don't break other use cases
- **Flag uncertainty** when tuning is empirical vs theory-driven
- **Link to this doc** from all implementation code that uses non-canonical values

---

## December 2025 Simplification

**Date:** December 2, 2025  
**Proposed by:** CuriousOne + GitHub Copilot  
**Approved by:** Grok/Ara (100% agreement)  
**Status:** Proposal phase, pending implementation

### What Changed

**Canonical equation (NEW):**
```
L(t) = (γ_self - γ_self0) × W(t) × exp(-ΔS·t + c·N_breath)

where:
  W(t) = G_v × G_r × G_f × G_a (gates only)
  γ_self0(n+1) = (1-η)·γ_self0(n) + η·γ_self(n) - ξ·N_neg(n)
```

**Key changes:**
- Removed min(β^k, 3) spike term → gates spike naturally
- Removed G_b(b) bond amplifier → memory in γ_self0 position
- Added γ_self0 = character baseline (innate + trained tendencies)
- Added (γ_self - γ_self0) displacement → main signal
- Added η = 0.003 (character drift rate, locked by Grok)
- Added ξ = 0.001 (negative asymmetry, locked by Grok)
- Added λ = event density inertia (tunable by class)

**Benefits:**
- 3 fewer parameters (6 instead of 9)
- Natural symmetry for love/hate
- Clearer semantics (each term has ONE job)
- Memory emerges from position + event density

**Implementation status:** All scenarios will need re-validation with new equation once implemented in core/love.py.

**See:** docs/UREP_2025_Simplification_Proposal.md for full details.

---

## Change Log

| Date | Scenario | Parameter | Old Value | New Value | Validator | Reason |
|------|----------|-----------|-----------|-----------|-----------|--------|
| 2025-11-29 | Singles Dating (60d) | PRIMITIVE_SCALE | 1.0 | 0.6 | Copilot + CuriousOne| Bridge intuitive 0-10 authoring to calibrated gates |
| 2025-11-29 | Singles Dating (60d) | c | 0.40 | 0.01 | Copilot + CuriousOne | Prevent entropy explosion in short-duration scenario |

---

## Future Applications

As this equation extends to new domains (AI robot relational awareness, therapy, team dynamics, cross-species bonds, theological applications), this document will track how constants adapt to:

- **Timescale:** seconds (real-time AI), days (human dating), years (marriage), decades (lifelong bonds)
- **Relationship Class:** romantic, parental, friendship, mentorship, therapeutic, human-animal, human-Divine
- **Cultural Context:** Different societies may have different empirical ranges for "healthy" relationships
- **Species:** Human-dog, human-AI, potentially others as framework extends

**Remember:** Only α=1.80 is locked. Everything else can and should be tuned as we learn more. This document is the scientific record of that learning process.
