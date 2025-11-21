# Revenge Gamma-Self — Leakage vs α (β = 30°)

Turns off sharply when θ < −180°

High-r tail = high_r_gaussian(r) × gate_on(θ) × gate_off(θ)  
→ strictly confined to Q3 (−135° ≤ θ ≤ +135° crossing ±180°)

## Quadrant masses (analytical, frozen)

- Q1 Revenge      : 0.00002 %
- Q2 Love leak    : 0.00000 %
- Q3 Memory       : 99.51532 %
- Q4 Enmity bleed : 0.48466 %

These percentages are **% of total probability mass** in each quadrant (integrated over the entire plane with the r dr dθ Jacobian).

Q2 = 0.00000 % means **zero high-r leakage into love** — the love gate is absolute.  
The tiny non-zero values in Q1/Q4 are only the faint low-r memory tail.

gate_on = 1 / (1 + exp(-ALPHA_DEG * (theta_deg + 135.0)))
gate_off = 1 / (1 + exp(BETA_DEG * (theta_deg + 180.0)))

Low-r continuity: perfect everywhere in Q3 via local θ-dependent scaling  
Natural Gaussian low-r tail in Q1/Q4 — faint but real  
High-r tail strictly confined by gates


| α  | Q2 Love %     | Q4 Enmity %   | Q1 Revenge %  | Emotional State          |
|----|---------------|---------------|---------------|--------------------------|
|  5 | 4.693882e-02 | 2.178151e-01 | 3.812532e-03 | Bitter — a whisper of love remains |
| 10 | 4.689416e-02 | 1.961474e-01 | 3.808904e-03 | Bitter — a whisper of love remains |
| 15 | 4.688499e-02 | 1.892815e-01 | 3.808160e-03 | Resentful — love is dying |
| 20 | 4.688251e-02 | 1.872295e-01 | 3.807959e-03 | Resentful — love is dying |
| 25 | 4.688181e-02 | 1.866337e-01 | 3.807902e-03 | Cold — love is mathematically negligible |
| 30 | 4.688161e-02 | 1.864623e-01 | 3.807885e-03 | Cold — love is mathematically negligible |
| 35 | 4.688156e-02 | 1.864131e-01 | 3.807881e-03 | Cold — love is mathematically negligible |
| 40 | 4.688154e-02 | 1.863990e-01 | 3.807880e-03 | Frozen — love is impossible |
| 45 | 4.688153e-02 | 1.863950e-01 | 3.807879e-03 | Frozen — love is impossible |
| 50 | 4.688153e-02 | 1.863938e-01 | 3.807879e-03 | Frozen — love is impossible |
| 55 | 4.688153e-02 | 1.863935e-01 | 3.807879e-03 | Absolute — love is annihilated |
| 60 | 4.688153e-02 | 1.863934e-01 | 3.807879e-03 | Absolute — love is annihilated |
