# Fidelity Asymmetry Research Questions

**Date:** December 7, 2025  
**Status:** Open Research Question  
**Context:** Discovered during Phase 2 Interactive Editor development using Counterfactual Explorer tool

---

## Executive Summary

The GRP (Gamma Relational Persona) model includes hybrid asymmetry for negative primitives, particularly fidelity. While the **conceptual basis** is sound (betrayals hurt more than affirmations heal), the **mathematical implementation** may produce overly extreme effects at high relationship magnitudes. This document outlines the equations, parameters, observed behavior, and research questions for validation.

---

## The GRP Core Equation

$$
\boxed{
\vec{\gamma}_{\text{self}}(n+1) = \vec{\gamma}_{\text{self}}(n) + 
\Big( w_v \cdot v + w_{S,R} \cdot S \Big) +
i \cdot \Big( w_r \cdot r + w_f \cdot f' + w_a \cdot a + w_{S,I} \cdot S \Big) -
\Delta S \cdot \Delta t
}
$$

**Where:**
- $\gamma_{\text{self}}(n)$ = Current relationship state (complex number: Real = Ego↔We, Imaginary = Hate↔Love)
- $v, r, f, a, S$ = Primitive relationship variables (visibility, resonance, fidelity, altruism, shared breath)
- $w_v, w_r, w_f, w_a$ = Axis weights controlling primitive impact
- $f'$ = Fidelity with hybrid asymmetry applied (see below)
- $\Delta S \cdot \Delta t$ = Entropy drift term (not relevant to this question)

---

## The Fidelity Asymmetry Equation

### For Positive Fidelity (f ≥ 0):
$$
f' = f
$$
No transformation - positive trust-building passes through unchanged.

### For Negative Fidelity (f < 0):
$$
\boxed{
f' = f \cdot w_{\text{neg}} \cdot \max(|\gamma_{\text{self}}(n)|, \varepsilon)
}
$$

**Where:**
- $f$ = Raw fidelity value (negative)
- $w_{\text{neg}}$ = Negative asymmetry multiplier (default: **1.5**)
- $|\gamma_{\text{self}}(n)|$ = $\sqrt{\text{Re}^2 + \text{Im}^2}$ = Relationship magnitude (depth/intensity)
- $\varepsilon$ = Collapse prevention threshold (default: **1.0**)

### Fidelity's Contribution to ΔIm (Love↔Hate axis):
$$
\Delta\text{Im}_{\text{fidelity}} = w_f \cdot f'
$$

**Where:**
- $w_f$ = Fidelity axis weight (default: **1.2**, strongest primitive)

### Combined Effective Multiplier for Negative Fidelity:
$$
\text{Effective Multiplier} = w_f \cdot w_{\text{neg}} \cdot |\gamma_{\text{self}}| = 1.2 \times 1.5 \times |\gamma_{\text{self}}| = 1.8 \times |\gamma_{\text{self}}|
$$

---

## Default Parameter Values

| Parameter | Value | Meaning |
|-----------|-------|---------|
| **$w_f$** | 1.2 | Fidelity axis weight (strongest primitive) |
| **$w_{\text{neg}}$** | 1.5 | Negative asymmetry multiplier (negatives hurt 50% more) |
| **$\varepsilon$** | 1.0 | Minimum magnitude threshold (prevents collapse at origin) |

**Other primitive weights for context:**
- $w_r = 1.0$ (resonance)
- $w_a = 0.6$ (altruism)
- $w_v = 0.8$ (visibility, real axis)

---

## Conceptual Justification (from GRP_rev3.md)

> "**Why:** Betrayals scar deeper than affirmations heal. Negatives scale with your current state magnitude — **the more you've earned, the more you lose when broken**."

**Theoretical basis:**
1. **Negativity Bias** - Negative events have stronger psychological impact than positive events of equal magnitude
2. **Attachment Depth** - Trust violations hurt more in deeper relationships (magnitude scaling)
3. **Asymmetry** - Recovery from betrayal takes longer than building trust (w_neg > 1.0)

---

## The Observed Problem

### Test Scenario: User's Dating Scenario
**File:** `data/single_dating_to_love_M1.csv`

**Relationship State at Event 7 (Day 49):**
- $|\gamma_{\text{self}}| = 44.6$ (strong, mature relationship)
- Current fidelity: $f = +9.0$ (high trust)
- Trajectory position: $(44.63, 150.6i)$ (deep love, strong We-orientation)

### Counterfactual Test: "What if fidelity dropped negative?"

**User's Counterfactual Explorer test:**
- Set $f = -1.88$ at event 7 (moderate negative, not extreme betrayal)
- **Result:** $\gamma_{\text{self}} = (44.63, -217.74i)$ (catastrophic drop to hate)
- **Total swing:** From +150.6 to -217.74 = **368-point drop** on imaginary axis

### Mathematical Breakdown:
1. **Asymmetry transform:**
   $$f' = -1.88 \times 1.5 \times 44.6 = -125.77$$
2. **Axis weight application:**
   $$\Delta\text{Im} = 1.2 \times (-125.77) = -150.93$$
3. **Effective multiplier:**
   $$1.8 \times 44.6 = 80.3\times$$

**Interpretation:** A relatively small negative fidelity ($f = -1.88$) at high relationship magnitude produces an **80x amplification** in damage.

---

## The Research Question

### Primary Question:
**Is an effective multiplier of 80x psychologically realistic for trust violations in deep relationships?**

### Sub-Questions:

1. **Does betrayal damage scale linearly with relationship depth?**
   - Current model: $\text{damage} \propto |\gamma_{\text{self}}|$ (unbounded linear growth)
   - Alternative: Logarithmic, square root, or capped scaling?

2. **Is $w_{\text{neg}} = 1.5$ (50% asymmetry) empirically justified?**
   - Gottman's 5:1 ratio suggests asymmetry exists, but applies to interaction counts
   - Baumeister's "bad is stronger than good" review suggests 2-4x asymmetry
   - How to translate to continuous primitive values?

3. **Should magnitude scaling be bounded?**
   - At $|\gamma| = 2.5$ (GRP_rev3 example): multiplier = 4.5x (seems reasonable)
   - At $|\gamma| = 44.6$ (mature love): multiplier = 80.3x (seems extreme)
   - Should there be a cap (e.g., max magnitude = 10)?

4. **What is the "right" sensitivity for clinical validity?**
   - Relationships do exhibit resilience at high attachment
   - But severe betrayals (infidelity, abuse) can destroy deep relationships instantly
   - Is $f = -1.88$ equivalent to "severe betrayal" or "moderate disappointment"?

---

## Comparative Analysis: Different Scaling Approaches

| Approach | Formula | At $\|\gamma\|=44.6$, $f=-1.88$ | At $\|\gamma\|=2.5$, $f=-4.0$ |
|----------|---------|--------------------------------|------------------------------|
| **Current (linear)** | $1.8 \times \|\gamma\|$ | -150.93 | -18.00 |
| **Capped at 10** | $1.8 \times \min(\|\gamma\|, 10)$ | -33.84 | -18.00 |
| **Logarithmic** | $1.8 \times \log(\|\gamma\| + 1)$ | -15.50 | -5.62 |
| **Square root** | $1.8 \times \sqrt{\|\gamma\|}$ | -27.12 | -10.73 |
| **Lower w_neg (1.2)** | $1.44 \times \|\gamma\|$ | -120.74 | -14.40 |

**Observation:** Linear unbounded scaling is the outlier. All bounded approaches yield more conservative results.

---

## Empirical Evidence Needed

### Psychology/Relationship Science:
1. **Gottman Institute Research**
   - 5:1 positive-to-negative interaction ratio for stable marriages
   - Does this translate to magnitude asymmetry or just frequency?
   
2. **Baumeister et al. (2001) "Bad is Stronger Than Good"**
   - Meta-analysis showing negativity bias across domains
   - Typical ratios: 2-4x impact for negative vs positive events
   
3. **Attachment Theory Literature**
   - Does betrayal damage scale with attachment depth?
   - Evidence for/against "deeper bonds = deeper wounds" proportionally
   
4. **Trust Repair Research**
   - Time to recover from trust violations vs time to build trust
   - Does recovery time scale with relationship duration/depth?

### Clinical Validation Questions:
- In a 10-year marriage, does a moderate betrayal cause 10x more damage than in a 1-year relationship?
- Or does relationship resilience provide a buffer at high depths?
- What magnitude of negative event constitutes "catastrophic" vs "recoverable"?

---

## Recommendations for Research

### 1. Literature Review Focus Areas:
- "trust violation asymmetry"
- "relationship depth betrayal impact"
- "attachment security buffer effects"
- "negativity bias relationship satisfaction"
- "Gottman ratio mathematical model"

### 2. Expert Consultation:
- Relationship therapists (practical experience)
- Attachment researchers (empirical data)
- Computational social scientists (modeling precedents)

### 3. Empirical Testing with Interactive Editor:
Use the Counterfactual Explorer tool to test scenarios:
- Early relationship betrayal (low $|\gamma|$): Does damage feel proportional?
- Mature relationship betrayal (high $|\gamma|$): Does damage feel realistic?
- Compare different $w_{\text{neg}}$ values using sensitivity analysis script

---

## Parameter Adjustment Proposals

### Option 1: Reduce $w_{\text{neg}}$ (Simple)
```
w_neg = 1.2  (20% asymmetry instead of 50%)
→ At |γ|=44.6, f=-1.88: ΔIm = -120.74 (still very high)
```

### Option 2: Cap Magnitude Scaling (Pragmatic)
```python
# Modify hybrid asymmetry function:
f' = f × w_neg × min(|γ_self|, 10)

w_neg = 1.5 (keep current conceptual design)
→ At |γ|=44.6, f=-1.88: ΔIm = -33.84 (moderate impact)
→ At |γ|=2.5, f=-4.0: ΔIm = -18.00 (unchanged from GRP_rev3 example)
```

### Option 3: Logarithmic Scaling (Theoretically Elegant)
```python
# f' = f × w_neg × log(|γ_self| + 1)

w_neg = 1.5
→ At |γ|=44.6, f=-1.88: ΔIm = -15.50 (gentle)
→ At |γ|=2.5, f=-4.0: ΔIm = -5.62 (significantly reduced)
```

### Option 4: Square Root Scaling (Middle Ground)
```python
# f' = f × w_neg × sqrt(|γ_self|)

w_neg = 1.5
→ At |γ|=44.6, f=-1.88: ΔIm = -27.12 (moderate)
→ At |γ|=2.5, f=-4.0: ΔIm = -10.73 (reduced but reasonable)
```

---

## Caveats and Limitations

### Model Assumptions:
1. **Primitives are normalized [-10, 10]**: Does $f = -1.88$ represent "mild disappointment" or "moderate betrayal"?
2. **Single-time-step impact**: Real betrayals unfold over multiple events with compounding effects
3. **No resilience mechanism**: Model doesn't account for forgiveness, repair work, or relationship buffers
4. **Linear trajectory**: Assumes relationship magnitude grows monotonically (may not reflect reality)

### Data Limitations:
- Limited empirical scenarios tested (mostly early-stage relationships in current dataset)
- No validation against longitudinal relationship outcome data
- Primitive value assignment is subjective (annotator interpretation)

### Theoretical Considerations:
- GRP is a descriptive model, not prescriptive (captures what IS, not what SHOULD BE)
- Extreme sensitivity might be "feature, not bug" if betrayal truly is catastrophic
- Need to distinguish between **mathematical elegance** and **empirical accuracy**

---

## Visualization Reference

**See:** `tests/fidelity_asymmetry_sensitivity.png`

This plot shows fidelity's ΔIm contribution across:
- Fidelity values: [-10, +10]
- Relationship magnitudes: [1.0, 5.0, 10.0, 20.0, 44.6]
- $w_{\text{neg}}$ values: [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]

**Key observations:**
- Curves show correct **qualitative shape** (asymmetry, depth sensitivity)
- Curves may show incorrect **quantitative magnitude** (too steep at high $|\gamma|$)
- Visual inspection suggests capping or nonlinear scaling may be needed

---

## Next Steps

1. **Consult literature** on negativity bias quantification in relationships
2. **Discuss with relationship therapists** for clinical intuition validation
3. **Test alternative formulations** using Counterfactual Explorer on multiple scenarios
4. **Compare to empirical outcomes** if longitudinal data becomes available
5. **Document decision rationale** in TUNING.md once parameter adjustment is made

---

## References

**GRP Documentation:**
- `docs/GRP_rev3.md` - Core model specification (December 2025)
- `CONSTANTS.md` - Default parameter values
- `TUNING.md` - Parameter tuning guidance

**Analysis Tools:**
- `tests/fidelity_asymmetry_sensitivity.py` - Sensitivity analysis script
- `tools/interactive_editor.py` - Counterfactual Explorer (Shift+Click feature)

**External Research to Consult:**
- Baumeister, R. F., et al. (2001). "Bad is stronger than good." *Review of General Psychology*, 5(4), 323-370.
- Gottman, J. M., & Silver, N. (1999). *The Seven Principles for Making Marriage Work*.
- Murray, S. L., & Holmes, J. G. (2009). "The architecture of interdependent minds: A motivation-management theory of mutual responsiveness." *Psychological Review*, 116(4), 908-928.

---

**Document Status:** Living document - to be updated as research progresses and parameter decisions are made.

**Primary Contact:** This is an open research question. Contributions welcome via GitHub issues or discussions.
