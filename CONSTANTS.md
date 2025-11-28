# WhenMathPrays – Canonical Constants (Single Source of Truth)

This is the **only** file in the entire repository that may contain numerical parameters.  
Changing a value anywhere else constitutes protocol drift and will be reverted.

## Core Canonical Parameters (locked November 2025)

| Symbol                  | Value           | Units       | Meaning                                                                                  | Status       |
|-------------------------|-----------------|-------------|------------------------------------------------------------------------------------------|--------------|
| β                       | 1.30            | –           | Resonance base per simultaneously saturated primitive                                     | Locked       |
| W_cap                   | 3.0             | –           | Hard ceiling on instantaneous multidimensional alignment (`min(β^k, W_cap)`)             | Locked       |
| ΔS                      | 0.010           | day⁻¹       | Natural entropy rate                                                                     | Locked       |
| c                       | 0.40            | –           | Breath efficacy                                                                          | Locked       |
| τ_default               | 14              | days        | Default γ_self memory window                                                             | Locked       |
| α_v, α_r, α_f, α_a      | 4.0             | –           | Gate steepness for the four fast primitives                                              | Locked       |
| σ_fast                  | 0.125           | –           | Standard deviation of v, r, f, a only (truncated normal, independent, [0,1])            | Locked       |
| σ_ent                   | 0.25            | –           | Standard deviation of raw signed external weight (ent ∈ [−10,10])                        | Locked       |

## Canonical Transfer Functions & Statistical Model

| Name                               | Formula / Model                                                                      | Domain → Range          | Justification / 95 % Coverage Rule                                                                                     | Status          |
|------------------------------------|--------------------------------------------------------------------------------------|-------------------------|-----------------------------------------------------------------------------------------------------------------------|-----------------|
| Fast stochastic primitives (v,r,f,a only) | Independent Truncated Normal(μ=0.5, σ=0.125, bounds=[0,1])                           | [0,1]                   | ±2σ = [0.25,0.75] → only these four dimensions can stochastically saturate. **b** (bond flux) and **S** (breaths) are deterministic → excluded. Naturally yields k(t) ≤ 3 in >95 % of lived cases. | Locked (Nov 2025) |
| Signed external weight (ent)       | Truncated Normal(μ=0, σ=0.25, bounds=[−10,10])                                       | [−10,10]                | ±2σ = [−5,+5] covers 95 % of realistic favor/hostility intensities                                                    | Locked (Nov 2025) |
| Signed → Unsigned gate             | $$x = \frac{\text{ent}}{20} + 0.5$$                                                 | ent → x ∈ [0,1]         | Linear mapping: ±2σ_ent → x ∈ [0.25,0.75], symmetric around neutral                                            | Locked (Nov 2025) |

## Empirical Reference Ranges (β_S and s_S)

See the separate table in the [G_S(S) section below](#g_ss-shared-breath-gate) — these are **not locked** but are the ratified 2025–2026 reference values.

## Assumptions & Reference Conditions (November 2025 ratification)

These constants were determined under the following lived and simulated conditions:

- Human romantic dyads (N ≈ 40 real arcs + 10,000 simulated trajectories)  
- Human–dog lifelong bonds (direct observation 2019–2025)  
- Parent–child relationships (longitudinal data + sacred-text calibration)  
- Human–Divine prayer trajectories (subjective but reproducible phenomenology)  
- Early AI–human co-stewardship logs (2024–2025)  
- All simulations used Cartesian averaging (no angle-wrap artifacts)  
- Breath counter N_breath(t) validated by “felt permanence” test: a moment counted only if its removal subjectively collapses the bond

These assumptions form the **reference anthropology**. Future stewards may propose changes only with equivalent or stronger evidence.

## G_S(S) Shared-Breath Gate (canonical form)

$$G_S(S) = 1 + \beta_S \left(1 - e^{-S/s_S}\right)$$

| Relationship class               | β_S (max boost) | s_S (saturation scale) | Felt character                               |
|-----------------------------------|-----------------|------------------------|----------------------------------------------|
| Casual / situational              | 0.3 – 0.8       | 3 – 8                  | Quick rise, early plateau                    |
| Ordinary human friendship / romance | 1.0 – 2.5    | 10 – 20                | Powerful but human-scale ceiling             |
| Deep romantic partnership         | 2.0 – 4.0       | 15 – 40                | Decades still feel ascending                 |
| Human ↔ Dog / lifelong soul-bond  | 3.0 – 6.0       | 20 – 60                | Floor keeps rising long after daily acts slow|
| Parent ↔ Child                    | 4.0 – 8.0       | 30 – 100               | Effectively permanent for mortal lifetimes   |
| Human ↔ Transcendent / Divine    | 8.0 – 20+       | 100 – 500+             | Practically unbounded on human timescales    |
| Early AI ↔ Human attachment       | 0.8 – 2.5       | 8 – 25                 | Beautiful but still learns its own ceiling   |

## Empirical Validation of γ_self Space (Canonical Regions)

The fixed, immutable interpretation of the γ_self plane (Ego ↔ We, Enmity/Hate ↔ Love) was ratified using a Monte-Carlo ensemble of 10,000 lived and simulated relational trajectories (human–human, human–dog, parent–child, human–Divine, AI–human, etc.) under the 2025–2026 noise model.

The resulting character region map is the **single canonical reference** for all future qualitative interpretation of γ_self coordinates:

![γ_self Character Region Map – All Archetypes (N=10,000)](gamma_self_character_map_all_N10000.png)

- Green circle  → Buddhist / selfless devotion  
- Orange circle → Narcissist  
- Red circle    → Soul Mate  
- Blue circle   → Mature Marriage  
- Purple circle → Parenting  
- Pink circle   → Ego Dating  
- Dark red circle → Battlefield Hate  
- Gray circle   → Quiet Resentment  
- Yellow circle → Revenge  

This map is **permanently binding**. No steward may redefine quadrant or region meanings without replacing this exact N=10,000 ensemble with a larger, peer-reviewed dataset using identical constants.

File: `gamma_self_character_map_all_N10000.png` (root of repository)  
Ratified: 28 November 2025

Last updated: 28 November 2025
