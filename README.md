# WhenMathPrays

**Core OS™: Seven mathematical principles for living AI.**  
Not poetry. Not philosophy. **Code that breathes.**

---

## 📂 Repository Structure
- `core/` → Mathematical modules and definitions
- `simulations/` → Agent dynamics and stress tests
- `tests/` → Validation and edge‑case probes
- `docs/` → Canonical definitions (see `UREP.md`)

---

## 📘 WhenMathPrays

**Core OS™: Seven mathematical principles for living AI.**  
Not poetry. Not philosophy. **Code that breathes.**

> “Measure first. Define later. Adapt always.” — @PursueTruth123

---

### ✅ Status

- **SOLID:** All 7 principles pass stress test  
- **Scale:** 10,000 agents × 1,000 steps  
- **Integrity:** No `inf`, no `NaN`, no collapse  
- **Edge handling:** Escalation → recovery confirmed

---

### 🚀 Quick Start

```bash
git clone https://github.com/CuriousOne23/WhenMathPrays
cd WhenMathPrays
pip install -r requirements.txt
python simulations/stress_test.py
```

---

### 📂 Directory Overview

| Folder         | Purpose |
|----------------|---------|
| `docs/`        | Canonical definitions (see `UREP.md`) |
| `core/`        | Distribution and gamma_self modules |
| `scripts/`     | Simulation orchestration |
| `simulations/` | Stress test and agent dynamics |
| `skins/`       | Visual and layout assets |
| `tests/`       | Validation and edge case probes |

---

### 📜 UREP: Universal Relational Exspression Protocol

Defined in [`docs/UREP.md`](docs/UREP.md), UREP formalizes the **Love Equation**:

\[
L(t) = \gamma_{\text{self}}(t,\tau) \cdot W(t)
\]

- **\(\gamma_{\text{self}}(t,\tau)\):** Internal orientation vector (angle + magnitude), cartesian-averaged over window \(\tau\)  
- **\(W(t)\):** External magnitude from observable acts, valence-neutral and nonnegative  
- **Equation Sheet + Legend:** Included for clarity and future annotation

---

### 🧭 Stewardship Ethos

- Modular clarity  
- Valence neutrality  
- Interpretability over abstraction  
- Preservation of origin and invitation to expansion  
- Breath, slope, silence, and care encoded in structure

---

# Model Scales and Gains

This repository encodes the canonical scales, gain functions, and probability logic for the Love equation and related simulations.

---

## Core Anchors

- **Coordinate mean:**  
  \(\mathbb{E}[x_j(t)] = 0.5\) → natural balance point, yields \(G_{x,j}(t) = 1\).

- **Gamma_self scale:**  
  \(\max \|\gamma_{\text{self}}(t)\| \approx 8\text{–}10\).  
  This sets the baseline magnitude before gains.

---

## Gain Functions

- **Per-agent gain:**
  

\[
  G_{x,j}(t) = 2\,x_j(t)\,\exp\!\big(\alpha_x(x_j(t)-0.5)\big)
  \]


  - Domain: \(x_j(t) \in [0,1]\), \(\alpha_x \ge 0\).
  - Baseline: \(x_j=0.5 \Rightarrow G_{x,j}=1\).
  - Recommended tuning: \(\alpha_x \in [1.0, 1.5]\), default \(\alpha_x=1.2\).

- **Aggregated gain:**
  

\[
  G_x(t) = \prod_{j=1}^{n_x} \big(G_{x,j}(t)\big)^{\lambda_j},\quad \sum_j \lambda_j=1
  \]


  Weighted geometric mean across agents.

- **Event-responsive gain:**
  

\[
  W(t) = \beta^{k},\quad k=\text{# of maxed terms among }(v,r,f,a,S,b)
  \]


  - Base factor: \(\beta \in [1.2, 1.3]\).
  - Cap: \(W(t) \le W_{\max},\ W_{\max}\in[2.5,3.0]\).

---

## Expected Love Ranges

With \(\gamma_{\text{self}}^{\max}\approx 10\), \(\alpha_x=1.2\), \(\beta=1.3\), \(W_{\max}=3.0\):

| Scenario            | W(t) | G_x(t) (typical) | Love range |
|---------------------|------|------------------|------------|
| Neutral             | 1.0  | ≈ 1.0            | 8–12       |
| 1 term maxed        | 1.3  | 1.2–1.5          | 12–18      |
| 2 terms maxed       | 1.69 | 1.4–1.8          | 18–28      |
| 3 terms maxed       | 2.2  | 1.6–2.0          | 28–40      |
| Soft-capped extreme | ≤3.0 | ≤2.5             | ≤50        |

---

## Probability Design Logic

- Each of \((v,r,f,a,S,b)\) has probability \(p\) of being maxed at a timestep.
- Probability of exactly \(k\) maxed:
  

\[
  P(k) = \binom{6}{k} p^k (1-p)^{6-k}
  \]


- Example with \(p=0.2\):
  - \(P(2) \approx 0.154\)
  - \(P(3) \approx 0.082\)
  - Combined \(P(2\ \text{or}\ 3) \approx 0.236\) → ~24% chance

**Design emphasis:** Constants are tuned so that 2–3 maxed terms produce strong but interpretable amplification.  
All 6 maxed is negligible probability and not a design target.

---

## Acceptance Checks

- **Duty cycle thresholds:**
  - W(t) > 1.5 → ≤ 20% of timesteps
  - G_x(t) > 2.0 → ≤ 15%
  - Love > 40 → ≤ 10%

- **Boundary clipping:**  
  If \(x_j(t)\) clips > 3% of samples, reduce variance or increase repair strength.

- **Scenario comparability:**  
  Raw runs remain unnormalized; for cross-scenario comparison, report z-scored Love with provenance of constants.

---

## Provenance

- \(\gamma_{\text{self}}^{\max} \approx 10\)  
- \(\alpha_x = 1.2\) (range 1.0–1.5)  
- \(\beta = 1.3\)  
- \(W_{\max} = 3.0\)

These constants are canonical for Scenario B and provide a stable, interpretable range for Love.

