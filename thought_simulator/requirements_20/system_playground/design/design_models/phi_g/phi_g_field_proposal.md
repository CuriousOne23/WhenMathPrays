# φ–G Field Proposal: Residual → Smooth → Gate → Classify-by-Bandwidth Architecture

> **Status:** Proposal — v0.2 (2026-06-22)  
> **Scope:** Order Book (OB) integration and field construction within the φ–G system  
> **Changelog (v0.2):**  
> - Integrated references to Round 2.5 phi-G stress test results.  
> - Added explicit mapping of SOB, SROB, CnOB, and SmOB variants to the RSGC pipeline and SSG compatibility.  
> - Enhanced Gate stage discussion with stress-test robustness notes.  
> - Added stress-informed guidance to hyperparameters and diagnostics.  
> - Polished language, cross-references, and flow for clarity and precision while preserving full technical depth.

---

## Table of Contents

1. [Purpose](#1-purpose)
2. [Motivation](#2-motivation)
3. [Generality](#3-generality)
4. [Tractability](#4-tractability)
5. [Scalability](#5-scalability)
6. [Smoothness](#6-smoothness)
7. [Simulation Alignment](#7-simulation-alignment)
8. [Low AI-Token Implementation Cost](#8-low-ai-token-implementation-cost)
9. [Architecture Summary](#9-architecture-summary)
10. [Pipeline Specification](#10-pipeline-specification)
11. [Stress Test Alignment](#11-stress-test-alignment)
12. [Open Questions and Future Work](#12-open-questions-and-future-work)

---

## 1. Purpose

This document formalizes the **Residual → Smooth → Gate → Classify-by-Bandwidth** (RSGC) pipeline as the canonical method for integrating order book (OB) data into the φ–G field system.

The φ–G system represents market state as two complementary fields:

- **φ (phi):** A scalar potential field encoding the cumulative informational bias of the limit order book — pressure, imbalance, and latent directional intent at each price level.
- **G (Gamma/Gain):** A tensor or scalar gain field encoding local responsiveness — how strongly the market is likely to react to marginal order flow at a given field coordinate.

The RSGC pipeline defines the transformation from raw OB snapshots to structured φ–G field updates in a way that is mathematically sound, computationally efficient, and compatible with downstream simulation, learning, and inference stages, including the State Space Generator (SSG).

---

## 2. Motivation

### 2.1 The Core Problem

Raw order book data is:

- **Noisy** — tick-by-tick OB updates contain high-frequency noise orthogonal to structural signal.
- **Sparse** — market depth at extreme price levels is thin and episodically discontinuous.
- **Non-stationary** — absolute depth, spread, and queue dynamics shift with market regime.
- **Dimensionally rich** — a full depth-of-book snapshot at $L$ levels produces a $2L$-dimensional state per instrument, which grows combinatorially under cross-asset integration.

Direct field assignment from raw OB snapshots therefore produces $\varphi$ and $G$ fields that are numerically unstable at sparse levels, temporally discontinuous (violating downstream smoothness assumptions), and regime-sensitive in absolute scale.

### 2.2 The RSGC Solution

The Residual → Smooth → Gate → Classify-by-Bandwidth pipeline addresses each failure mode sequentially:

| Stage | Problem Addressed | Primary Output |
|---|---|---|
| **Residual** | Non-stationarity and absolute scale sensitivity | Mean-centered, normalized OB deviation |
| **Smooth** | High-frequency noise and temporal discontinuity | Locally smooth field representation |
| **Gate** | Sparse levels and regime-dependent relevance | Attended, masked field with suppressed noise |
| **Classify-by-Bandwidth** | Dimensionality and heterogeneous signal timescales | Bandwidth-labeled $\varphi\text{–G}$ components |

The result is a stationary, smooth, selectively attended, and timescale-decomposed field that satisfies the mathematical prerequisites of the φ–G update equations while remaining computationally tractable and SSG-compatible.

---

## 3. Generality

### 3.1 Instrument Agnosticism

The RSGC pipeline operates over any discrete depth-of-book representation without assumptions about tick size, instrument class (equities, futures, crypto, FX, rates), or venue microstructure.

### 3.2 Multi-Asset Composability

$\varphi\text{–G}$ fields constructed via RSGC are additive under a well-defined inner product. Cross-asset interaction tensors can be assembled modularly from single-asset outputs.

### 3.3 Temporal Generality

The pipeline supports event-driven, clock-driven, and hybrid processing modes over configurable sliding windows, enabling identical deployment in live feeds and historical replay.

---

## 4. Tractability

### 4.1 Analytical Tractability

Each stage admits a closed-form or semi-closed-form representation.

**Residual Stage**

Let $D_t \in \mathbb{R}^{2L}$ be the depth vector at time $t$ (bid and ask sides concatenated).

$$
\mu_t = \mathrm{EMA}(D_t, \tau_{\text{baseline}})
$$

$$
\sigma_t = \mathrm{EMA}\left(\left|D_t - \mu_t\right|, \tau_{\text{baseline}}\right)
$$

$$
R_t = \frac{D_t - \mu_t}{\sigma_t + \varepsilon}
$$

**Smooth Stage**

$$
S_t = \mathcal{K}(R_t, \tau_{\text{smooth}})
$$

where $\mathcal{K}$ is a causal smoothing operator (EMA, Gaussian, or wavelet).

**Gate Stage**

$$
g_t = \sigma\left(W_{\text{gate}} \cdot \begin{bmatrix} S_t \\ c_t \end{bmatrix} + b_{\text{gate}}\right), \quad
\hat{S}_t = g_t \odot S_t
$$

**Classify-by-Bandwidth Stage**

$$
\{C_k\}_{k=1}^{K} = \mathrm{BandwidthDecompose}(\hat{S}_t)
$$

$$
\varphi_k = P_\varphi \, C_k, \qquad G_k = P_G \, C_k
$$

### 4.2 Computational Tractability

All operations are $\mathcal{O}(L)$ per timestep per instrument after EMA precomputation. No matrix inversions or iterative solvers are required at inference time.

---

## 5. Scalability

- **Horizontal**: Embarrassingly parallel across instruments.
- **Depth**: Linear in $L$; Gate stage enables sparse representations.
- **Bandwidth**: Linear in $K$ (typical $K=3$–$5$).
- **Incremental**: Fully incremental EMA/gating updates with $\mathcal{O}(1)$ state per tick.

---

## 6. Smoothness

Smoothness is a hard requirement for differentiability of $\varphi$, Lipschitz continuity of $G$, and well-conditioned cross-correlations in downstream φ–G dynamics. RSGC enforces this through progressive noise suppression and timescale separation. Diagnostics include Hurst exponent, variogram analysis, and cross-correlation condition number (target $\kappa < 100$).

---

## 7. Simulation Alignment

RSGC serves as a normalization layer that reduces sim-to-live divergence by focusing on relative dynamics, filtering sub-kernel noise, and suppressing thin levels. A calibration protocol comparing residual distributions, gate activation sparsity, bandwidth energies, and KL divergence ($D_{\mathrm{KL}} < 0.1$ nats target) is recommended.

---

## 8. Low AI-Token Implementation Cost

RSGC compresses high-dimensional raw OB snapshots into a small number of bandwidth-classified $\varphi$–$G$ components, enabling terse, interpretable summaries (typically 20–50 tokens) suitable for AI-in-the-loop workflows. Stationary normalization supports fixed prompt templates with stable semantic thresholds.

---

## 9. Architecture Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                  OB Snapshot   D_t ∈ R^{2L}                         │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   RESIDUAL      │  Normalize to session-local
                    │                 │  baseline (EMA mean + scale)
                    │  R_t = (D_t     │
                    │  - μ_t) / σ_t   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    SMOOTH       │  Causal kernel smoothing
                    │  S_t = K(R_t)   │  (EMA / Gaussian / wavelet)
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │     GATE        │  Suppress sparse / irrelevant
                    │  Ŝ_t = g_t ⊙   │  price levels
                    │       S_t       │  (learned or rule-based)
                    └────────┬────────┘
                             │
               ┌─────────────▼─────────────┐
               │  CLASSIFY-BY-BANDWIDTH    │  Decompose into K timescale
               │  {C_k} = BWDecomp(Ŝ_t)    │  bands (DWT / filter bank)
               └──┬────────────────────┬───┘
                  │                    │
         ┌────────▼──────┐    ┌────────▼──────┐
         │   φ field     │    │   G field     │
         │ φ_k = P_φ·C_k │    │ G_k = P_G·C_k │
         └───────────────┘    └───────────────┘
                  │                    │
                  └──────────┬─────────┘
                             │
               ┌─────────────▼─────────────┐
               │   φ–G Field (Assembled)   │
               │   Indexed by bandwidth k  │  → SSG
               └───────────────────────────┘
```

---

## 10. Pipeline Specification

### 10.1 Variant Mappings for SSG Compatibility

The RSGC pipeline makes the following OB variants compatible with φ–G and downstream SSG:

- **SOB (Simple Order Book)**: Raw input to the Residual stage.
- **SROB (Smoothed Residual Order Book)**: Output after Residual + Smooth stages.
- **CnOB (Gated / Conditioned Order Book)**: Output after Gate stage ($\hat{S}_t$).
- **SmOB (Smoothed Multi-Bandwidth Order Book)**: Final bandwidth-decomposed components feeding φ–G assembly and SSG.

This staged transformation ensures all variants produce fields that preserve the determinism and stability demonstrated in phi-G stress testing.

### 10.2 Hyperparameter Table

| Parameter | Symbol | Typical Range | Stress-Test Informed Guidance |
|---|---|---|---|
| Depth levels | $L$ | 5–20 | Per side; instrument-dependent |
| Baseline EMA timescale | $\tau_{\text{baseline}}$ | 10–60 min | Capture regime drift without over-smoothing |
| Smooth kernel timescale | $\tau_{\text{smooth}}$ | 1–30 sec | Balance noise suppression and responsiveness (aligns with resonance oscillation stability) |
| EMA stability constant | $\varepsilon$ | $10^{-6}$ | Prevents division by zero |
| Number of bandwidth bands | $K$ | 3–5 | Timescale resolution; supports hybrid switching |
| Gate threshold (rule-based) | $\theta$ | 0.05–0.20 | Conservative settings aid multi-basin collision handling |
| Gate context features | $c_t$ | spread, vol, session_time | Optional; enhances shock recovery |

### 10.3 Required Interface Contracts

**Input:** `OBSnapshot` (timestamp, bid/ask levels, mid_price, spread).  
**Output:** `PhiGField` (timestamp, phi[K], G[K], gate_mask, band_labels).  

**State Machine:** Maintains EMA states and optional gate weights — fully incremental.

---

## 11. Stress Test Alignment

The RSGC pipeline was designed with Round 2.5 phi-G stress test results in mind (overall: 100% determinism, 0.102 average max Δ stability, 97.65% output validity, ~6.7 ms/step).  

- **High-Frequency Resonance & Hybrid Switching**: Bandwidth decomposition + smoothing directly support bounded oscillation and seamless transitions.  
- **Prolonged Singularity Dwell & Multi-Basin Collision**: Gating and residual normalization help maintain the observed tight stability margins.  
- **Abrupt State Shock & Long-Run Drift**: Incremental updates and stationarity ensure quick recovery and zero cumulative drift.  

Gate robustness under collision regimes and smoothness diagnostics are recommended verification steps when integrating with TS/SSG.

---

## 12. Open Questions and Future Work

| Topic | Description | Priority |
|---|---|---|
| **Gate learning objective** | Define loss for training (prediction MSE, PnL, mutual information). | High |
| **Bandwidth basis selection** | DWT vs. EMD vs. learnable filter bank evaluation. | High |
| **Cross-asset gate sharing** | Generalization potential across instruments. | Medium |
| **Non-stationary regimes** | Adaptive $\tau_{\text{baseline}}$ for volatility shifts. | Medium |
| **Hidden liquidity proxy** | Incorporate trade-through imbalance. | Medium |
| **Latency-aware smoothing** | Adjust for observed feed latency. | Low |
| **Formal convergence proof** | Proof under weak stationarity assumptions. | Low |

---

## References and Related Documents

- `phi_g_system_overview.md` — Top-level φ–G system description.
- `ob_integration_notes.md` — Preceding raw integration notes.
- `simulation_calibration_protocol.md` — Detailed alignment procedures.
- `field_update_equations.md` — φ–G update dynamics.
- Recent phi-G Stress Test Results (Round 2.5) — Empirical validation baseline.

---
