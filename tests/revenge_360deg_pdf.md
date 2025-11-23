# Revenge Gamma-Self — 360° Canonical View

**LIVE PARAMETERS FROM revenge_core.py**

α = 5.0° → slow entry into past (controls Q2 bleed)
β = 30.0° → brutal execution toward future
Memory peak locked at θ = -150.0°
Low-r center:  r = 0.5
High-r peak:   r = 2.0 (μ), σ = 0.5
Low-r width:   σ_r = 0.3
Global scaling: perfect continuity at (r=R_LOW_CENTER, θ=-150°)

## PDF at canonical witness angles

| θ (degrees) | Description                        | PDF (r_low)      | PDF (r_high)     |
|-------------|------------------------------------|------------------|------------------|
|   -165.0° | +165° (−180°+15°)                   | 1.773e-02 | 7.979e-01 |
|   -180.0° | −180° (seam)                        | 1.330e-02 | 3.989e-01 |
|   -195.0° | −165° (−180°−15°)                   | 8.864e-03 | 3.303e-08 |
|   -137.5° | −135° − α/2                         | 1.773e-02 | 7.979e-01 |
|   -135.0° | −135° (gate_on center)              | 1.330e-02 | 3.989e-01 |
|   -132.5° | −135° + α/2                         | 8.864e-03 | 3.006e-06 |
|   -150.0° | -150.0° (memory peak)               | 1.773e-02 | 7.979e-01 |
|    -90.0° | −90°                                | 3.427e-05 | 7.378e-18 |
|    -45.0° | −45°                                | 3.427e-05 | 7.378e-18 |
|      0.0° | 0° (present)                        | 3.427e-05 | 7.378e-18 |
|     45.0° | +45° (future — must be dead)        | 3.427e-05 | 7.378e-18 |

Generated: 2025-11-22 15:57:04
