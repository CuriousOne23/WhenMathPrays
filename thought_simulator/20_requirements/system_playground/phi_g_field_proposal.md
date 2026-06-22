# φ–G Field Proposal: Residual → Smooth → Gate → Classify-by-Bandwidth Architecture

> **Status:** Proposal — v0.1 (2026-06-22)
> **Scope:** Order Book (OB) integration and field construction within the φ–G system

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
11. [Open Questions and Future Work](#11-open-questions-and-future-work)

---

## 1. Purpose

This document formalizes the **Residual → Smooth → Gate → Classify-by-Bandwidth** (RSGC) pipeline as the canonical method for integrating order book (OB) data into the φ–G field system.

The φ–G system represents market state as two complementary fields:

- **φ (phi):** A scalar potential field encoding the cumulative informational bias of the limit order book — pressure, imbalance, and latent directional intent at each price level.
- **G (Gamma/Gain):** A tensor or scalar gain field encoding local responsiveness — how strongly the market is likely to react to marginal order flow at a given field coordinate.

The RSGC pipeline defines the transformation from raw OB snapshots to structured φ–G field updates in a way that is mathematically sound, computationally efficient, and compatible with downstream simulation, learning, and inference stages.

---

## 2. Motivation

### 2.1 The Core Problem

Raw order book data is:

- **Noisy** — tick-by-tick OB updates contain high-frequency noise that is orthogonal to signal.
- **Sparse** — market depth at extreme price levels is thin and episodically discontinuous.
- **Non-stationary** — the absolute level of depth, spread, and queue dynamics shifts with market regime.
- **Dimensionally rich** — a full depth-of-book snapshot at $L$ levels produces a $2L$-dimensional state per instrument, which grows combinatorially under cross-asset integration.

Direct field assignment from raw OB snapshots therefore produces $\varphi$ and $G$ fields that are:

1. Numerically unstable at sparse price levels.
2. Discontinuous across time, violating the smoothness assumptions of downstream gradient-based learners.
3. Regime-sensitive in absolute scale, making generalization across sessions and instruments brittle.

### 2.2 The RSGC Solution

The Residual → Smooth → Gate → Classify-by-Bandwidth pipeline addresses each failure mode in sequence:

| Stage | Problem Addressed | Output |
|---|---|---|
| **Residual** | Non-stationarity; absolute scale sensitivity | Mean-centered, normalized OB deviation |
| **Smooth** | High-frequency noise; temporal discontinuity | Locally smooth field representation |
| **Gate** | Sparse levels; regime-dependent relevance | Attended, masked field with suppressed noise |
| **Classify-by-Bandwidth** | Dimensionality; heterogeneous signal timescales | Bandwidth-labeled $\varphi\text{–G}$ components |

The result is a field that is stationary, smooth, selectively attended, and decomposed by informational timescale — satisfying the mathematical prerequisites of the φ–G update equations while remaining computationally tractable.

---

## 3. Generality

### 3.1 Instrument Agnosticism

The RSGC pipeline is defined over **any** discrete depth-of-book representation. It makes no assumptions about:

- Tick size or price granularity.
- Instrument class (equities, futures, crypto, FX, rates).
- Venue microstructure (central limit order book, RFQ, dark pools with partial depth disclosure).

The Residual stage normalizes across these structural differences by operating on **relative depth deviations** rather than absolute quantities, and the Classify-by-Bandwidth stage adapts the decomposition basis to the empirical autocorrelation structure of each instrument.

### 3.2 Multi-Asset Composability

$\varphi\text{–G}$ fields constructed via RSGC are additive under a well-defined inner product. Cross-asset $\varphi\text{-G}$ interaction tensors can be assembled from single-asset RSGC outputs without re-running the full pipeline, enabling modular multi-leg construction.

### 3.3 Temporal Generality

The pipeline is defined over sliding windows with configurable lookback. It is compatible with:

- **Event-driven** (per-update) processing.
- **Clock-driven** (fixed-interval snapshot) processing.
- **Hybrid** (event-triggered with clock-aligned emission) processing.

This means RSGC can be deployed identically in live market feed contexts and in historical backtest replay.

---

## 4. Tractability

### 4.1 Analytical Tractability

Each stage of the pipeline has a closed-form or semi-closed-form representation.

---

**Residual Stage**

Let $D_t \in \mathbb{R}^{2L}$ be the depth vector at time $t$ (bid side concatenated with ask side, each of length $L$).

$$
\mu_t = \mathrm{EMA}(D_t, \tau_{\text{baseline}})
$$

$$
\sigma_t = \mathrm{EMA}\left(\left|D_t - \mu_t\right|, \tau_{\text{baseline}}\right)
$$

$$
R_t = \frac{D_t - \mu_t}{\sigma_t + \varepsilon}
$$

$R_t$ is the normalized residual depth vector. The baseline timescale $\tau_{\text{baseline}}$ is a hyperparameter, typically set to capture intra-session regime drift (e.g., 10–60 minutes of market time).

---

**Smooth Stage**

$$
S_t = \mathcal{K}(R_t, \tau_{\text{smooth}})
$$

where $\mathcal{K}$ is a causal smoothing operator (exponential, Gaussian, or wavelet-based). The smooth timescale $\tau_{\text{smooth}} \ll \tau_{\text{baseline}}$ targets signal-preserving noise suppression.

---

**Gate Stage**

$$
g_t = \sigma\left(W_{\text{gate}} \cdot \begin{bmatrix} S_t \\
c_t \end{bmatrix} + b_{\text{gate}}\right)
$$

$$
\hat{S}_t = g_t \odot S_t
$$

The gate $g_t \in [0,1]^{2L}$ is either:

- **Learned:** via a lightweight linear layer trained on downstream $\varphi\text{-G}$ prediction residuals.
- **Rule-based:** threshold on local depth variance or spread proxy (zero learnable parameters).

$c_t$ is an optional context vector (spread, session time, recent volatility) that modulates gate sensitivity.

---

**Classify-by-Bandwidth Stage**

$$
\\{C_k\\}_{k=1}^{K} = \mathrm{BandwidthDecompose}(\hat{S}_t)
$$

$$
\varphi_k = P_\varphi \ C_k, \qquad G_k = P_G \ C_k
$$

$\mathrm{BandwidthDecompose}$ partitions $\hat{S}_t$ into $K$ bandwidth bands (e.g., via DWT, EMD, or a learnable filter bank), each labeled by its characteristic frequency or decay rate. The $\varphi$ and $G$ transforms are linear projections per band, enabling interpretable field components indexed by timescale.

### 4.2 Computational Tractability

All operations are $\mathcal{O}(L)$ per timestep per instrument (after precomputing EMA state). No matrix inversions, no iterative solvers, no non-linear optimization at inference time.

---

## 5. Scalability

### 5.1 Horizontal Scaling

Because RSGC processes each instrument independently through the Residual and Smooth stages, the pipeline is embarrassingly parallel across instruments. A fleet of $N$ instruments requires $N$ independent EMA-state machines with no inter-instrument communication until the optional multi-asset field assembly step.

### 5.2 Depth Level Scaling

The pipeline complexity scales linearly with depth levels $L$. In practice, the Gate stage suppresses most content at extreme price levels, meaning the effective dimensionality of $\hat{S}_t$ is far less than $2L$. Sparse representations (storing only levels where $g_t > \theta$) can reduce memory and downstream computation substantially.

### 5.3 Bandwidth Band Scaling

The number of bandwidth bands $K$ is a design choice. Typical deployments use $K = 3–5$ bands (e.g., sub-second, seconds, tens-of-seconds, minutes, session). Adding bands increases field richness linearly but does not change the Residual or Smooth stages.

### 5.4 Incremental Updates

All EMA and gating state is $\mathcal{O}(1)$ to update per tick. The pipeline supports fully incremental, zero-recomputation updates, making it suitable for ultra-low-latency deployments.

---

## 6. Smoothness

### 6.1 Why Smoothness Is a Hard Requirement

The $\varphi\text{-G}$ field update equations and any gradient-based learner operating on the field require that:

1. **$\varphi$ is differentiable** with respect to price level — enabling gradient computation for optimal execution path planning.
2. **$G$ is Lipschitz-continuous** with respect to time — ensuring that gain estimates do not exhibit jumps that destabilize downstream controllers.
3. **Field cross-correlations** ($\varphi \otimes G$ inner products) are finite and well-conditioned.

Raw OB data violates all three: depth profiles are piecewise-constant, the gain field derived directly from raw depth is discontinuous at queue depletion events, and cross-correlations computed from raw depth are numerically ill-conditioned during thin-market episodes.

### 6.2 How RSGC Enforces Smoothness

**The Residual stage** removes the mean-reverting non-smooth component (absolute depth level drift), leaving a zero-mean deviation that is comparatively smooth.

**The Smooth stage** is the primary smoothness guarantee. The causal kernel enforces the Lipschitz bound

$$
\|S_t - S_{t-\Delta t}\| \leq C \cdot \Delta t \qquad \text{for } \Delta t \text{ above the kernel bandwidth,}
$$

which holds almost surely under finite-variance OB increments — an assumption empirically satisfied in all liquid instruments under normal conditions.

**The Gate stage** suppresses sparse, high-variance price levels that are the primary source of non-smoothness in the residual. By gating near-zero, episodically populated levels, the downstream field inherits the smoothness properties of the well-populated levels.

**The Classify-by-Bandwidth stage** separates high-frequency (potentially non-smooth) components from low-frequency (structurally smooth) components. Downstream consumers can choose to operate exclusively on lower-bandwidth components when smoothness is the binding constraint, or include higher-bandwidth components when speed of response is preferred.

### 6.3 Smoothness Diagnostics

Standard diagnostics to verify that an RSGC-processed field satisfies smoothness requirements:

- **Hurst exponent** of $\varphi_k(t)$ per band $k$ — should satisfy $H > 0.5$ for low-bandwidth bands.
- **Variogram** of $\varphi(\text{price level})$ at a fixed time — should exhibit power-law growth consistent with fractional Brownian motion.
- **Condition number** of the empirical cross-correlation matrix $\mathrm{Corr}(\varphi, G)$ — should be well-bounded (practical threshold: $\kappa < 100$).

---

## 7. Simulation Alignment

### 7.1 The Simulation-Reality Gap in OB Field Systems

A persistent failure mode in OB-based field systems is simulation drift: a $\varphi\text{-G}$ field that behaves correctly in historical backtest diverges from live behavior because the simulation does not faithfully reproduce the statistical properties of OB dynamics — particularly:

- Queue depletion and refill patterns.
- Hidden order / iceberg effects.
- Latency-induced gaps in depth visibility.
- Venue-specific matching engine behavior at queue boundaries.

### 7.2 RSGC as a Simulation-Agnostic Interface

The RSGC pipeline acts as a **normalization layer** between raw simulation output and the $\varphi\text{-G}$ field. Because:

- The Residual stage normalizes to session-local statistics, the absolute depth levels of the simulation do not need to match the live market exactly — only the relative dynamics need to be qualitatively correct.
- The Smooth stage filters timescales below the kernel bandwidth, making the field insensitive to the specific mechanics of queue updates at sub-kernel resolution.
- The Gate stage suppresses depth levels that are thin in simulation (which often differ most from live), focusing the field on the informationally dense core of the book.

This means a simulator that produces qualitatively plausible mid-level OB dynamics (even with simplified queue mechanics) will produce RSGC-normalized fields that are statistically close to those produced from live data — dramatically reducing the simulation-to-live transfer cost.

### 7.3 Simulation Calibration Protocol

To verify alignment before deploying a new simulator or market model:

1. Run RSGC on 5 days of live OB data for the target instrument.
2. Run RSGC on 5 equivalent simulated sessions.
3. Compare the empirical distributions of:
   - $R_t$ (residual depth) — should match in mean and variance.
   - $g_t$ (gate activation) — should match in sparsity and per-level activation rate.
   - Bandwidth band energies $\|C_k\|^2$ — should match in relative proportion.
4. Compute KL divergence of $\varphi$ and $G$ marginal distributions per band. Practical acceptance criterion:

$$
D_{\mathrm{KL}}\left(p_{\text{live}} \| p_{\text{sim}}\right) < 0.1 \text{ nats}
$$

---

## 8. Low AI-Token Implementation Cost

### 8.1 Motivation for Token Efficiency

The $\varphi\text{-G}$ system operates in environments where AI inference (large language model calls, neural network forward passes, or autoregressive sampling) may be part of the signal generation loop. In such architectures, token cost is a first-class engineering constraint. A field representation that requires lengthy natural-language descriptions, high-dimensional numeric summaries, or verbose structured prompts to communicate its state to an AI component will be prohibitively expensive in both latency and dollar cost.

### 8.2 How RSGC Minimizes Token Cost

**Compression by design.** The RSGC pipeline compresses a $2L$-dimensional raw OB snapshot (often $L = 10–20$, so 20–40 floats per side) into $K$ bandwidth-classified scalar or low-rank field components. For $K = 4$ bands with a scalar projection, the full $\varphi\text{-G}$ field state is representable as **8 numbers** (4 $\varphi$ values + 4 $G$ values), compared to 40+ raw depth levels.

**Interpretable bandwidth labels.** Because each band is labeled by its characteristic timescale (e.g., "sub-second," "seconds," "minutes"), the AI component can reason about field state in natural language without requiring numeric precision. A prompt such as:

> $\varphi[\text{seconds-band}] = +0.42$ (bid pressure, above $2\sigma$); $G[\text{seconds-band}] = 0.87$ (high responsiveness)

conveys actionable signal in ~12 tokens rather than a full depth-of-book table requiring 100+.

**Gating eliminates irrelevant levels.** The Gate stage ensures that sparse, low-information price levels are zeroed out before any AI-facing summarization. This means the AI component never needs to process or reason about uninformative depth, further reducing both token count and interpretive burden.

**Stationary representation.** Because the Residual stage normalizes to session-local statistics, the AI component can use fixed natural-language thresholds ("above $1\sigma$," "near zero," "below $-2\sigma$") without recalibration across sessions or instruments. This enables static prompt templates with slot-filled numeric summaries — the lowest possible token overhead for structured field communication.

### 8.3 Reference Token Budget

| Representation | Bands $K$ | Tokens (approx.) |
|---|---|---|
| Full raw OB ($L = 10$ levels) | — | 120–160 |
| RSGC $\varphi\text{-G}$ summary, terse | 4 | 30–50 |
| RSGC $\varphi\text{-G}$ summary, verbose | 4 | 60–90 |
| RSGC $\varphi\text{-G}$ summary, terse | 3 | 20–35 |

The terse 4-band format is the recommended default for AI-in-the-loop deployments.

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
               │   Indexed by bandwidth k  │
               └───────────────────────────┘
```

> **Note:** ASCII diagrams render as plain code blocks on GitHub and do not support math rendering. All equations outside this block use GitHub-flavored math.

---

## 10. Pipeline Specification

### 10.1 Hyperparameter Table

| Parameter | Symbol | Typical Range | Notes |
|---|---|---|---|
| Depth levels | $L$ | 5–20 | Per side; instrument-dependent |
| Baseline EMA timescale | $\tau_{\text{baseline}}$ | 10–60 min | Session-drift timescale |
| Smooth kernel timescale | $\tau_{\text{smooth}}$ | 1–30 sec | Signal-preserving noise floor |
| EMA stability constant | $\varepsilon$ | $10^{-6}$ | Prevents division by zero |
| Number of bandwidth bands | $K$ | 3–5 | Timescale resolution |
| Gate threshold (rule-based) | $\theta$ | 0.05–0.20 | Fraction of max gate activation |
| Gate context features | $c_t$ | spread, vol, session\_time | Optional; $c_t = \varnothing$ means no context |

### 10.2 Required Interface Contracts

**Input:**

```
OBSnapshot {
  timestamp  : int64        -- nanoseconds since epoch
  bid_levels : float64[L]   -- cumulative bid depth at each price level
  ask_levels : float64[L]   -- cumulative ask depth at each price level
  mid_price  : float64      -- current mid price
  spread     : float64      -- current bid-ask spread (optional)
}
```

**Output:**

```
PhiGField {
  timestamp   : int64       -- nanoseconds since epoch
  phi         : float64[K]  -- φ field values per bandwidth band
  G           : float64[K]  -- G field values per bandwidth band
  gate_mask   : float64[2L] -- per-level gate activation (diagnostic)
  band_labels : str[K]      -- human-readable timescale label per band
}
```

### 10.3 State Machine

The RSGC pipeline maintains the following persistent state between updates:

```
State {
  mu_ema       : float64[2L]           -- EMA of raw depth (baseline mean)
  sigma_ema    : float64[2L]           -- EMA of |D_t - mu_ema| (baseline scale)
  smooth_state : float64[2L]           -- EMA state for smooth stage
  gate_weights : float64[2L × d_ctx]  -- learned gate params (if applicable)
}
```

All state updates are $\mathcal{O}(L)$ per tick with no memory of prior ticks beyond the EMA state.

---

## 11. Open Questions and Future Work

| Topic | Description | Priority |
|---|---|---|
| **Gate learning objective** | Define the loss for training the gate layer — candidates include $\varphi\text{-G}$ prediction MSE, downstream PnL, or mutual information maximization. | High |
| **Bandwidth basis selection** | Evaluate DWT vs. EMD vs. learnable filter bank for the Classify-by-Bandwidth stage across instruments with different autocorrelation structure. | High |
| **Cross-asset gate sharing** | Explore whether a single gate network generalizes across instruments or whether per-instrument gates are required. | Medium |
| **Non-stationary regimes** | Investigate adaptive $\tau_{\text{baseline}}$ that adjusts to volatility regime shifts (e.g., news events, open/close transitions). | Medium |
| **Hidden liquidity proxy** | Extend the Residual stage to incorporate trade-through imbalance as a proxy for hidden depth, improving $G$ field accuracy. | Medium |
| **Latency-aware smoothing** | Model the smoothing stage as a function of observed feed latency to avoid introducing artificial smoothness from latency artifacts. | Low |
| **Formal convergence proof** | Provide a formal proof that the RSGC-normalized field converges to a stationary distribution under weak stationarity assumptions on OB dynamics. | Low |

---

## References and Related Documents

- `phi_g_system_overview.md` — Top-level description of the φ–G field system.
- `ob_integration_notes.md` — Raw integration notes preceding this proposal.
- `simulation_calibration_protocol.md` — Detailed simulation alignment procedures (see §7.3).
- `field_update_equations.md` — Formal definition of the φ–G update dynamics that RSGC feeds.

---
