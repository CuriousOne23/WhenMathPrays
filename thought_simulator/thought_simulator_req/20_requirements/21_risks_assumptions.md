# 21 Risks, Assumptions, and Mitigations

## 1. Purpose

This document identifies the **key risks, foundational assumptions, and corresponding mitigations** for the **Thought Simulator (TS)** project.

It serves as a living risk register to maintain transparency, drive proactive mitigation, and protect determinism, stability, observability, and long-term research value.

## 2. Core Risk Management Principles

* All risks must be explicitly acknowledged and mitigated where possible.
* Assumptions must be clearly stated and validated through testing (see 14_testing_and_validation_requirements.md).
* Risks that threaten **determinism**, **reproducibility**, or **conceptual integrity** are treated as **critical**.
* This document will be reviewed and updated during major milestones.

## 3. Critical Risks

**RISK-01: Loss of Determinism**  
**Description**: Parallel execution, floating-point differences, or hidden state cause non-reproducible runs.  
**Likelihood**: Medium  
**Impact**: Critical  
**Mitigation**: Strict `deterministic_mode`, parallel-friendly pure math functions (12), bitwise reproducibility tests (14), state counter + checksums (13).

**RISK-02: Numerical Instability Over Long Runs**  
**Description**: Floating-point drift or accumulation errors degrade behavior after 100k+ ticks.  
**Likelihood**: Medium  
**Impact**: High  
**Mitigation**: Numerical stability requirements and monitoring (20), long-run regression tests (14).

**RISK-03: Performance vs Determinism Trade-off**  
**Description**: Optimization pressure leads to approximations that break reproducibility.  
**Likelihood**: High (during implementation)  
**Impact**: High  
**Mitigation**: All optimizations disabled in deterministic_mode (12).

**RISK-04: Observer Layer Leakage**  
**Description**: Visualization, UI, or probes accidentally influence core state.  
**Likelihood**: Medium  
**Impact**: Critical  
**Mitigation**: Strict read-only interfaces and architectural conformance tests (14, 15, 16).

**RISK-05: Memory / Resource Exhaustion**  
**Description**: Unbounded growth in TP count or history during long experiments.  
**Likelihood**: Medium  
**Impact**: High  
**Mitigation**: Hard limits, graceful degradation, and regulators (16).

## 4. Secondary Risks

**RISK-SEC-01: Concept Drift in Regulators**  
**Description**: Regulators become misaligned with evolving basin or entropy definitions.  
**Likelihood**: Medium  
**Impact**: High  
**Mitigation**: Strong conceptual validation tests (14), invariant monitoring (20), and versioned regulator contracts.

**RISK-SEC-02: Snapshot Schema Evolution**  
**Description**: Schema changes break backward compatibility with old experiments and snapshots.  
**Likelihood**: Medium  
**Impact**: High  
**Mitigation**: Explicit snapshot compatibility policy and cross-version loading tests (16, 17, 19).

**RISK-SEC-03: Parallel Backend Divergence**  
**Description**: Different math backends (NumPy vs JAX vs custom) produce subtly different results.  
**Likelihood**: Medium  
**Impact**: High  
**Mitigation**: Deterministic parallel semantics and reference implementation testing (12), backend validation suite (14).

**RISK-SEC-04: Experiment Explosion**  
**Description**: Proliferation of experiment variants becomes unmanageable.  
**Mitigation**: Strong experiment registry, templates, and comparison tools (19).

**RISK-SEC-05: Visualization Performance**  
**Description**: Live visualization slows or crashes under high TP counts.  
**Mitigation**: Strict decoupling and graceful degradation (18).

## 5. Key Assumptions

**ASSUM-01: Deterministic Floating-Point Behavior**  
Assumption: Consistent floating-point semantics across hardware and Python versions.  
**Validation**: Multi-platform tests; optional fixed-point fallback.

**ASSUM-02: Observer Remains External**  
Assumption: Researchers will respect the mechanical/observer boundary.  
**Validation**: Clear contracts and architectural linting.

**ASSUM-03: Python + NumPy Ecosystem Stability**  
Assumption: Core dependencies remain suitable for high-performance deterministic simulation.  
**Mitigation**: Minimal dependencies, pinned versions, reproducible builds (16).

**ASSUM-04: Conceptual Model Remains Stable**  
Assumption: Core concepts (OBs, RBs, ThoughtPoints, unified entropy) will not require fundamental changes post v1.0.  
**Mitigation**: Strong versioning and deprecation policy.

**ASSUM-05: Research Use Case Dominates**  
Assumption: Primary users are technical researchers comfortable with CLI/Python API.  
**Mitigation**: Strong focus on headless + scripting interfaces.

## 6. Risk Monitoring and Review

* Risks will be reviewed at the end of each major development sprint.
* New risks discovered during implementation will be added here with mitigations.
* Critical risks must be mitigated before v1.0 release.

## 7. Invariants (Non-Negotiable)

* Any risk that threatens determinism or reproducibility is treated as blocking.
* All assumptions must be explicitly tested or mitigated.
* Mitigation strategies must themselves be observable and testable.

## 8. Success Criteria

* All critical risks have active, validated mitigations.
* Key assumptions are documented and periodically verified.
* The project maintains a transparent, living risk register that supports confident long-term development.
* No critical determinism or stability risks remain open at major releases.

---

**Last Updated**: May 26, 2026  
**Version**: 0.2  
**Changes from 0.1**:
- Incorporated Copilot’s three suggested refinements as Secondary Risks (Concept Drift in Regulators, Snapshot Schema Evolution, Parallel Backend Divergence).
- Minor reorganization for better flow.

---