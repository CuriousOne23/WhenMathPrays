# 40.10_Parameter Tuning and Calibration

## 1. Purpose

This document defines the numerical parameters, tuning methodology, constraints, and calibration procedures for the Thought Simulator (TS).

It specifies how the unified entropy functional and related dynamic thresholds are instantiated numerically.  

**Important Note**: This document belongs to the **numerical implementation layer**, not the conceptual TS specification. The core concepts (unified entropy, basins, tagging, determinism) remain independent of specific numerical values.

## 2. Unified Entropy Functional

The TS uses a weighted combination:

$$
H_{\text{total}} = \alpha H_{\text{rep}} + \beta H_{\text{pred}} + \gamma H_{\text{struct}}
$$

### 2.1 Weight Constraints

- All weights must satisfy:  
  $$
  \alpha + \beta + \gamma = 1.0
  $$
- All weights must be non-negative.
- Weights are **tunable parameters**, not conceptual constants.

### 2.2 Initial Experimental Values (Not Defaults)

| Coefficient | Initial Value | Valid Range     | Primary Influence                  |
|-------------|---------------|-----------------|------------------------------------|
| α           | 0.40          | [0.20 – 0.60]   | Representational entropy / identity |
| β           | 0.35          | [0.20 – 0.50]   | Predictive entropy / transitions   |
| γ           | 0.25          | [0.10 – 0.40]   | Structural entropy / relations     |

These values are **starting points only** and must be calibrated for different domains and experimental goals.

**Note on Scaling**: Each entropy component ($H_{\text{rep}}$, $H_{\text{pred}}$, $H_{\text{struct}}$) may have different natural magnitudes. Future implementations may require individual normalization or scaling functions before weighting to ensure meaningful combination.

## 3. Tuning Guidelines

### 3.1 Sensitivity Analysis
Systematically vary each coefficient within its range and observe effects on:
- OB settling time
- RB traversal smoothness
- TP trajectory coherence and length
- Frequency of splitting and merging
- Overall entropy reduction rate
- Regulator activation frequency

### 3.2 Domain-Specific Tuning
Different cognitive domains may require different balances:
- Logical / analytical reasoning → higher α and β
- Creative or associative thinking → higher γ
- Emotional or evaluative processing → balanced or adjusted structural weight

## 4. Other Dynamic Parameters

**Basin-Level Parameters**
- Maximum TP capacity per basin
- Entry and convergence thresholds
- Minimum entropy drop per tick (for OBs)

**System-Level Parameters**
- Stagnation threshold (ticks without progress)
- Anti-collapse entropy floor
- Oscillation detection window
- Regulator trigger thresholds
- Scheduler priority weights

All parameters must:
- Have well-defined default values and valid ranges
- Be stored in configuration files (YAML)
- Be logged with every simulation run
- Be versioned for reproducibility

## 5. Calibration Process

1. Define success metrics for the specific thought domain or experiment.
2. Run controlled parameter sweeps with fixed random seeds.
3. Compare results against theoretical expectations and desired behavior.
4. Iteratively refine weights and thresholds.
5. Validate determinism: same seed + same parameters → identical trajectories.
6. Document and version final parameter sets.

**Future Calibration Tools**: Later versions of the TS may include automated calibration utilities (grid search, Bayesian optimization, evolutionary tuning). This document will be expanded accordingly.

## 6. Observability Requirements

- All parameter values must be included in every TS State Snapshot.
- Parameter sweeps must be automatable with result logging.
- Parameter changes must be traceable across experiments.

## 7. Invariants

- Weight normalization: α + β + γ = 1.0
- Changing parameters must not break determinism.
- Calibration must not alter the conceptual definitions in Documents 01–07.

## 8. Success Criteria

- Initial parameter sets produce stable, coherent, and interesting thought trajectories.
- The tuning process is systematic, reproducible, and well-documented.
- Researchers can confidently explore how parameter choices affect simulated thought dynamics.

---

**Last Updated**: May 26, 2026  
**Version**: 0.3 (Final refinements per CoPilot)

---

