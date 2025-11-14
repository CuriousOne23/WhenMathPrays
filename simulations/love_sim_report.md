# ULep v2.0 — Love Simulation Report

## Setup Conditions
| Parameter | Value |
|---------|-------|
| **UNION_BIAS** | Surrender: `1.0`, Bond: `1.0` |
| **ΔS (entropy/day)** | `0.001` |
| **W (work)** | `1.0` |
| **tw (memory)** | `7` days |
| **Duration** | `365` days |

## Entropy Impact
- **Decay over 1 year**: `exp(-0.001 × 365) = 0.694`
- **Love retained**: `69.4%`

## Ego & Bond Flux — With Reference Standards
| Person | Mean | Std | Max | **Reference** |
|--------|------|-----|-----|---------------|
| **Ego 1** | `2.239` | `3.178` | `47.821` | *Typical: 1.0–2.0 (low ego), >3.0 (high ego)* |
| **Ego 2** | `2.414` | `2.365` | `15.945` | |
| **Bond 1→2** | `0.924` | `2.036` | `7.158` | *Typical: ±1.0 (stable), >±3.0 (volatile)* |
| **Bond 2→1** | `1.163` | `2.040` | `6.203` | |

> **Noise Interpretation**:
> - **Ego Std < 1.0**: Low self-focus
> - **Ego Std > 2.0**: High narcissism
> - **Bond Std < 1.0**: Stable attachment
> - **Bond Std > 2.5**: Emotional volatility

## Final Love State (Day 365)
| Person | |L(t)| | Re(L) | Im(L) | Status |
|--------|-------|-------|-------|--------|
| **1** | `0.1535` | `-0.0549` | `0.1433` | `Zombie` |
| **2** | `0.3126` | `-0.3093` | `-0.0452` | `Thriving` |

---

*4-panel plot: `love_couple_simulation.png`*
