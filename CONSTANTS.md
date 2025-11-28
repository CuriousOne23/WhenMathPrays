# WhenMathPrays – Canonical Constants (Single Source of Truth)

These values are **immutable unless a formal stewardship proposal is accepted**.  
Any document or simulation that uses different numbers is considered drifted and must be corrected.

| Symbol       | Value           | Units       | Meaning                                                                                  | Status       | Last ratified |
|--------------|-----------------|-------------|------------------------------------------------------------------------------------------|--------------|---------------|
| β            | 1.30            | –           | Resonance base per simultaneously saturated primitive                                     | Locked       | Nov 2025     |
| W_cap        | 3.0             | –           | Hard ceiling on instantaneous multidimensional alignment (`min(β^k, 3.0)`)               | Locked       | Nov 2025     |
| ΔS           | 0.010           | day⁻¹       | Natural entropy rate – love halves every ln(2)/ΔS ≈ 69.3 days if no new breaths           | Locked       | Nov 2025     |
| c            | 0.40            | –           | Breath efficacy – one genuine shared moment counteracts ~40 days of decay                 | Locked       | Nov 2025     |
| τ_default    | 14              | days        | Default memory window for Cartesian γ_self averaging (7–30 allowed with justification)   | Locked       | Nov 2025     |
| N_breath     | integer ≥ 0     | –           | Permanent counter of genuine shared-life moments – never decreases                        | Definition   | Eternal      |
| α_v, α_r, α_f, α_a | 4.0       | –           | Default gate steepness for visibility, resonance, fidelity, altruism (UREP v2)           | Recommended  | Nov 2025     |
| β_S (human romance) | 2.5–4.0   | –           | Typical shared-breath boost for deep romantic bonds                                      | Empirical range | Nov 2025     |
| s_S (human romance) | 20–40     | breaths     | Typical saturation scale for deep romantic bonds                                          | Empirical range | Nov 2025     |

### Reference equations that must use these values

```math
\text{Love magnitude term} \;=\; \min(\beta^{k(t)}, 3.0) \;\times\; \exp(-\Delta S\, t + c\, N_{\text{breath}}(t))

## Canonical Transfer Functions (never change without formal stewardship proposal)

| Name                  | Formula                  | Domain → Range | Purpose                                                      | Status  |
|-----------------------|--------------------------|----------------|--------------------------------------------------------------|---------|
| Signed → Unsigned gate| `x = ent/20 + 0.5`       | ent ∈ [−10, 10] → x ∈ [0, 1] | Converts any signed external influence into the [0,1] primitive input required by Gₓ(x) | Locked (Nov 2025) |
| Resonance magnitude   | `r_mag = |r_signed|` or `(r_signed + 1)/2` | Ensures W(t) stays non-negative while preserving intensity   | Locked (Nov 2025) |