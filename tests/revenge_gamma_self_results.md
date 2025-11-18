# Revenge Gamma-Self Distribution Results

Generated: 2025-11-17 19:51:33 MST

**Summary of PDF Construction:**
The revenge gamma-self PDF is defined in polar coordinates (r, θ), with r ≥ 0 representing magnitude, and θ in [-π, π] representing angle (0° at positive real axis 'we', 90° at positive imaginary 'love', clockwise or counterclockwise as per standard).
For r ≥ 0.5: Density is a Gaussian in r ~ N(μ=2, σ=0.5), multiplied by two tanh-like gates confining to θ in [-135°, -180°] (Q3: ego-enmity): sharp turn-on at -135° with α=5°, soft fade at -180° with β=30°. Zero density outside this angular range to prevent leaks into Q1/Q4.
For r ≤ 0.5: Switches to a bivariate normal centered at (r=0.5, θ=-150°), with σ_r=0.3, σ_θ=30° (uncorrelated), allowing faint drift tails only near Q3 and adjacent boundaries.
The low-r part is scaled to ensure continuity at r=0.5 (no density jump), and the entire PDF is globally normalized so ∫ pdf(r,θ) r dr dθ = 1 over r=0 to ∞, θ=-π to π.
Key values: μ_r=2, σ_r_high=0.5, σ_r_low=0.3, σ_θ_low=30°, α=5°, β=30°, boundary r=0.5, memory θ=-150°.
Regions: Q1 (0° to 90°: we-love), Q2 (90° to 180°: ego-love), Q3 (180° to 270° or -180° to -90°: ego-enmity), Q4 (270° to 360° or -90° to 0°: we-enmity).
Variables: x = r cosθ (real: we +, ego -), y = r sinθ (imag: love +, enmity -).
Properties: Peak at (r≈2, θ≈-150°), only tiny drifts below r=0.5 in Q1/Q4/Q2 from nearby seeding, no high-r leaks into Q1/Q4.
To recreate: Implement the above piecewise definition, wrap angles to [-π, π], scale for continuity at match point (e.g., θ=-150°), normalize via numerical integration.

**Parameters:** σ_r=0.3, σ_θ=30°, α=5°, β=30°, μ_r=2

| Point        | r   | θ (degrees) | pdf_value    |
|--------------|-----|-------------|--------------|
| origin       | 0.1 |     -150    | 2.42e-03 |
| drift-Q3     | 0.4 |     -135    | 4.91e-03 |
| peak         | 2.0 |     -150    | 5.29e-01 |
| boundary     | 0.6 |     -150    | 1.05e-02 |
| Q1-drift     | 0.4 |       45    | 3.72e-12 |
| neg45-drift  | 0.4 |      -45    | 1.22e-05 |
| pos135-drift | 0.4 |      135    | 1.41e-22 |
