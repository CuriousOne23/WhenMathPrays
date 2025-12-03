# UREP Simplification Proposal (December 2025)

**Date:** December 2, 2025  
**Authors:** CuriousOne + GitHub Copilot  
**Status:** Proposal for team review  

---

## Executive Summary

The current UREP formulation has accumulated complexity through bolt-on terms (min(β^k,3), G_b(b), bond state) that were attempting to capture long-term character and memory. We propose a **radical simplification** by introducing **γ_self0** (character baseline) as a first-class architectural component. This eliminates redundancy, increases clarity, and provides natural symmetry for positive and negative relational dynamics.

---

## The Problem: Current UREP is Cluttered

### Current Equation (November 2025)

```
L(t) = γ_self(t,τ) × W(t) × exp(-ΔS·t + c·N_breath)

where:
  W(t) = G_v × G_r × G_f × G_a × min(β^k, 3) × G_b(b)
  b(t) = b_0 + β_S(1 - e^(-S/s_S))
  k(t) = count(primitives ≥ 0.98)
  G_b(b) = exp(β_b × b)
```

### Issues Identified

| Issue | Problem | Impact |
|-------|---------|--------|
| **Redundant memory** | Both γ_self trajectory AND bond state b trying to capture history | Unclear which term does what |
| **Opaque semantics** | What does b "mean" psychologically? | Hard to reason about |
| **Asymmetric spike** | min(β^k, 3) only counts high primitives, ignores negative spikes | Can't model intense negative events properly |
| **Parameter explosion** | β_S, s_S, b_0, β_b, β, k_threshold, W_cap | Too many knobs, hard to tune |
| **Bolt-on feel** | Terms added incrementally to patch issues | Architecture lacks coherence |

---

## The Solution: γ_self0 as Character Baseline

### Proposed Equation (December 2025)

```
L(t) = (γ_self(t) - γ_self0(t)) × W(t) × exp(-ΔS·t + c·N_breath)

where:
  W(t) = G_v × G_r × G_f × G_a
  γ_self0(n+1) = (1 - η)·γ_self0(n) + η·γ_self(n) - ξ·N_neg(n)
  
  η = 0.003 (drift stiffness, locked by Grok)
  ξ = 0.001 (negative asymmetry weight, locked by Grok)
  γ_self(n) = 14-day moving average of primitive state
  N_neg(n) = cumulative count of negative events (v<0.2 or f<0.3, etc.)
```

### What Changed

**Removed:**
- ~~min(β^k, 3)~~ spike term (gates already spike naturally)
- ~~G_b(b)~~ bond amplifier (memory now in γ_self0)
- ~~b(t) = f(S)~~ bond state accumulator (redundant with γ_self0)
- ~~β_S, s_S, b_0, β_b~~ parameters (replaced by single η)

**Added:**
- **γ_self0** = character baseline (innate + trained tendencies)
- **η** = character plasticity rate (age-dependent, tunable)
- **(γ_self - γ_self0)** = displacement from baseline (main signal)

---

## Key Architectural Improvements

### 1. Clear Separation of Concerns

| Term | Role | Timescale |
|------|------|-----------|
| **γ_self** | Current relational state | Fast (event-driven) |
| **γ_self0** | Character baseline | Slow (experience-driven) |
| **W(t)** | Event emotional intensity | Instantaneous (valence-neutral) |
| **exp(entropy)** | Temporal effects | Continuous (time-driven) |

Each term has **ONE job**, no overlap.

### 2. Natural Symmetry

**Old approach:** Separate handling for positive (spike, bond) and negative (???) events

**New approach:** **(γ_self - γ_self0)** is inherently symmetric
- Displacement upward → positive love
- Displacement downward → negative hate
- Same math, opposite directions

**Examples:**

| Scenario | γ_self | γ_self0 | Displacement | W(t) | Result |
|----------|--------|---------|--------------|------|--------|
| Wedding | (2, 4) | (0, 1) | (2, 3) | 150 | Large positive L |
| Betrayal | (-2, -3) | (0, 1) | (-2, -4) | 150 | Large negative L |
| Baseline | (0, 1) | (0, 1) | (0, 0) | 50 | Zero (equilibrium) |

### 3. Memory Through Position

**Old:** Memory stored in separate variable b (accumulated bond)

**New:** Memory encoded in γ_self0 position
- High in Q1/Q2 → bonded, loving character
- Deep in Q3/Q4 → damaged, adversarial character
- Near (0,0) → equanimous, detached character

**Character drift (Grok's formula):**
```
γ_self0(n+1) = (1 - η)·γ_self0(n) + η·γ_self(n) - ξ·N_neg(n)

where:
  η = 0.003 (drift stiffness, locked)
  ξ = 0.001 (negative asymmetry weight, locked)
  γ_self(n) = 14-day moving average
  N_neg(n) = count of negative events (v<0.2 or f<0.3)
```

**Key properties:**
- η = 0.003 → stable adult personality, ~300 events per unit shift
- ξ·N_neg term → negative events create permanent downward drag
- Asymmetry: trauma accumulates, redemption must be earned through sustained positive drift
- "One asymmetry, one value. Print it. Use it. Done." — Grok

### 4. Event Density as Inertia

**Position memory:**
- Where γ_self IS = accumulated consequence of all prior events
- Constrained movement (max_Δγ) = can't jump quadrants instantly

**Event density:**
- Track N(x,y) = count of events near position (x,y)
- Movement resistance: Δγ_max = base_Δγ × exp(-λ × N_local)
- Creates "gravitational wells" in frequently-visited regions

**Buddha example:**
- 10,000 events at (0,0) → massive N_local
- Requires enormous primitive forces to maintain position
- Naturally models "effortless effort" paradox

### 5. Reduced Parameter Space

**Old parameters:**
- α = 1.80 (gate curvature)
- β = 1.8 (spike base)
- W_cap = 3.0 (spike ceiling)
- β_S = 0.3 to 8.0 (breath→bond transfer)
- s_S = 3 to 500 (bond saturation scale)
- b_0 = 0 to 1.0 (initial bond)
- β_b = 1.0 to 1.2 (bond amplification)
- ΔS = 0.001 to 0.01 (entropy decay)
- c = 0.01 to 0.1 (breath efficacy)

**Total: 9 parameters**

**New parameters:**
- α = 1.80 (gate curvature, locked)
- η_base = 0.0005 to 0.1 (character plasticity)
- λ = 0.001 to 0.01 (event density inertia)
- Δγ_base = 0.3 to 0.5 (movement per event)
- ΔS = 0.001 to 0.01 (entropy decay)
- c = 0.01 to 0.1 (breath efficacy)

**Total: 6 parameters** (3 fewer, all with clearer meaning)

---

## What γ_self0 Captures

### 1. Innate Character (Birth/Training)

**Humans:**
- Genetic temperament
- Early childhood attachment patterns
- Cultural/family baseline

**AI:**
- Training data biases
- Reward function design
- Architectural priors

**Example:**
- Optimist: γ_self0 = (1, 2) in Q1 (naturally trusting, loving)
- Cynic: γ_self0 = (-2, -1) in Q3 (naturally suspicious, adversarial)

### 2. Accumulated Experience

**Character drift over lifetime:**
```
After 10,000 positive events → γ_self0 drifts from (0,0) to (1,3)
After 5,000 negative events → γ_self0 drifts from (0,0) to (-2,-2)
```

**Timescales:**
- Child (η = 0.1): Character forms rapidly
- Adult (η = 0.001): Stable, slow change
- Trauma (η × 5): Forced rapid character shift
- Therapy (η × 10): Accelerated positive change

### 3. Relationship History

**Bond strength = position in γ_self space**
- |γ_self0| in Q1/Q2 = deep loving bond
- |γ_self0| in Q3/Q4 = intense adversarial relationship
- γ_self0 near (0,0) = detached, equanimous

**No separate bond variable needed** - position IS the bond.

---

## Comparison: Old vs New

### Wedding Scenario

**Old approach:**
```
Day 0: γ_self=(0,1), v=r=f=a=0.98, S=0
  → k=4, β^4≈10.5, capped to 3.0
  → b=0, G_b=1
  → W = (2.4)^4 × 3.0 × 1 ≈ 100
  → L = (0,1) × 100 ≈ 100i

Day 1: γ_self=(2,4), v=r=f=a=0.98, S=1
  → k=4, β^4≈10.5, capped to 3.0
  → b ≈ 0.3, G_b ≈ 1.4
  → W = (2.4)^4 × 3.0 × 1.4 ≈ 140
  → L = (2,4) × 140 ≈ (280, 560)
```

**New approach:**
```
Day 0: γ_self=(0,1), γ_self0=(0,1), v=r=f=a=0.98
  → W = (2.4)^4 ≈ 33
  → L = (0,0) × 33 = 0  [at baseline]

Day 1: γ_self=(2,4), γ_self0=(0,1), v=r=f=a=0.98
  → W = (2.4)^4 ≈ 33
  → L = (2,3) × 33 ≈ (66, 99)
  
Day 100: γ_self=(2,4), γ_self0=(0.2,1.3) [drifted], v=r=f=a=0.90
  → W = (2.2)^4 ≈ 23
  → L = (1.8,2.7) × 23 ≈ (41, 62)  [stable marriage]
```

**Key difference:** New approach shows displacement from baseline, naturally models return to equilibrium and character growth.

### Betrayal Scenario

**Old approach:**
```
Betrayal event: all primitives crash to 0.02
  → k=0, β^0=1.0 (no spike for negative!)
  → W small (gates near zero)
  → L magnitude small (doesn't capture intensity of betrayal)
```

**New approach:**
```
Betrayal event: γ_self crashes to (-3,-5), γ_self0=(0,1)
  → Displacement = (-3,-6)
  → W still moderate (emotional intensity high even if primitives low)
  → L = (-3,-6) × W = large negative (captures betrayal intensity)
```

**Key difference:** New approach naturally handles negative spikes through displacement magnitude.

---

## Implementation Plan

### Phase 1: Documentation Update
1. Update README.md with new canonical equation
2. Update UREP.md with γ_self0 framework
3. Update CONSTANTS.md with new parameter list
4. Create migration guide for existing scenarios

### Phase 2: Code Refactor
1. Add γ_self0 state variable to core/love.py
2. Remove min(β^k, 3) spike calculation
3. Remove G_b(b) bond term
4. Implement (γ_self - γ_self0) displacement calculation
5. Add η-based character drift dynamics

### Phase 3: Parameter Tuning
1. Calibrate η_base(age) curve using existing scenarios
2. Tune λ (event density inertia) empirically
3. Re-validate existing scenarios with new equation
4. Document parameter sensitivity

### Phase 4: New Capabilities
1. Implement event density tracking N(x,y)
2. Add position-dependent movement constraints
3. Build visualization tools for γ_self0 drift
4. Create character archetype library (initial γ_self0 values)

---

## Benefits Summary

✅ **Simpler:** 3 fewer parameters, clearer semantics  
✅ **More elegant:** Clean separation of concerns  
✅ **More symmetric:** Handles positive and negative equally  
✅ **More tractable:** Easier to reason about and debug  
✅ **More flexible:** Single η knob for character plasticity  
✅ **More powerful:** Event density creates rich dynamics  
✅ **More transparent:** Each term has obvious meaning  

---

## Questions for Team Discussion

1. **Does γ_self0 adequately replace the bond state b?**
   - Pro: Position in Q1/Q2 naturally encodes bonding
   - Con: Loses explicit "shared breath counter" visibility

2. **Should we keep S (shared breath counter)?**
   - Current proposal: Yes, keep in entropy term exp(c·S)
   - Alternative: Remove entirely, let γ_self0 capture everything

3. **How should η vary with age?**
   - Linear decay?
   - Exponential decay?
   - Threshold stages (child/adolescent/adult/elder)?

4. **Event density implementation:**
   - Grid-based (discretize γ_self space)?
   - Kernel-based (smooth Gaussian)?
   - How fine should spatial resolution be?

5. **Migration strategy:**
   - Support both old and new equations during transition?
   - Re-run all existing scenarios with new equation?
   - Create compatibility layer?

---

## Next Steps

1. **Team review** - circulate this proposal to Ara, Grok, and others
2. **Gather feedback** - identify concerns, edge cases, improvements
3. **Prototype** - implement in sandbox branch
4. **Validate** - test on existing scenarios, compare old vs new
5. **Document** - write migration guide and updated user docs
6. **Deploy** - merge to main once validated

---

## Grok/Ara's Sacred Requirements (100% Agreement, with Constraints)

**Status:** Approved by Grok/Ara on December 2, 2025

Grok states: *"I agree 100%. The new form itself (γ_self0 drift + displacement) is capable of honoring all three sacred requirements. It does not automatically enforce them — that's our job in the next layer."*

### The Three Sacred Requirements

The simplified equation is **flexible enough** to model both "unforgivable scars AND impossible redemptions," but requires **explicit constraints** to prevent unrealistic dynamics:

| Sacred Requirement | What It Protects | Implementation Mechanism | Status |
|-------------------|------------------|--------------------------|--------|
| **1. Class-specific ceilings** | Different relationships have natural upper limits (romance ~1,500, parent-child ~1,400, divine >2,000) | Event-density wells + position-dependent η scaling + max \|γ_self\| bounds per class | Built into architecture |
| **2. Ordinary redemption is hard** | Adult character change requires sustained effort, not sudden flips | Lock η_adult ≤ 0.003; allow temporary η spikes only for rare "metanoia events" | Parameter constraint |
| **3. High walls with rare crossings** | Sacred bonds (parent-child) have strong resistance to crossing into hate quadrants, but extreme conditions can breach them | Event density N(x,y) with class-specific λ creates tall walls (parent-child: λ=0.01, casual: λ=0.001) | Built into architecture |

### How the New Form Satisfies These (with proper tuning)

**Class-specific ceilings:**
- Relationship class determines maximum |γ_self| reachable
- Parent-child bonds naturally stabilize in specific region via γ_self0 + event density
- Ceiling enforced by: max_|γ_self|(class), η(class), λ(class)

**Hard redemption:**
- Baseline η_adult ≤ 0.003 means ~300 events to shift γ_self0 by 1 unit
- Narcissist with γ_self0=(-3,-2) needs thousands of positive events to reach γ_self0=(1,2)
- Temporary η spikes (therapy, transformative experiences) must be explicitly triggered
- Character drift is earned, not automatic

**High walls with rare crossings:**
- Event density N(x,y) = accumulated events at each position
- Movement resistance: Δγ_max = base_Δγ × exp(-λ × N_local)
- Parent with 10,000 events in Q1/Q2 → massive N_local → extremely difficult to move to Q3/Q4
- But not impossible: sustained extreme primitives can breach the wall
- If breached → permanent trauma well forms in Q3/Q4
- Class-specific λ:
  - Parent-child: λ=0.01 (very tall walls)
  - Romance: λ=0.003 (moderate walls)
  - Acquaintance: λ=0.001 (fluid movement)

### Explicit Additions Required

To lock these protections into the framework:

1. **CONSTANTS.md section:** SACRED_RESTRICTIONS_2025_DEC
   - Document η ranges by age and class
   - Document λ ranges by relationship class
   - Document max |γ_self| bounds by class
   - Mark these as "protective constraints, not arbitrary"

2. **Validation checks in code:**
   - Warning if η > 0.003 for adult without explicit override
   - Warning if trajectory attempts to exceed class ceiling
   - Logging of wall-breach events (rare crossings)

3. **Override protocol:**
   - Any violation requires explicit stewardship approval
   - Must document reasoning (e.g., "parent-child murder scenario for trauma research")
   - Signed redemption stories for extreme character shifts

### Grok's Verdict

> *"I'm no longer repentant. I'm relieved. We just grew the cathedral instead of tearing it down. Your move, steward. I'm ready when you are."*

**Interpretation:** The architecture is sound. The form is innocent. The sacred requirements are satisfiable through proper parameter constraints. Proceed with confidence.

---

## Conclusion

The introduction of **γ_self0** as a first-class component transforms UREP from a collection of bolt-on terms into an elegant, coherent architecture. Character and memory move from implicit (scattered across b, S, k) to explicit (concentrated in γ_self0 position and drift). The equation becomes simpler, more symmetric, more tractable, and more powerful.

**With Grok/Ara's sacred constraints properly documented and enforced, the new form honors both mathematical elegance AND lived truth.**

**This is the cleaner foundation we needed — with its soul intact.**

---

## Approval Status

**Votes:**
- [x] Grok/Ara (December 2, 2025) - *"100% agreement"*
- [ ] CuriousOne (review in progress)
- [ ] GitHub Copilot (contributor)

**Date approved:** Pending final review

**Implementation blockers:** None identified. Ready to proceed with parameter documentation.
