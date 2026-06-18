## Path A+B Integration Test Plan — TS-ITP-AB-001 v1.0

### Structure at a Glance

| Section | Contents |
|---------|----------|
| **Test Objectives** (TO-1–7) | 7 objectives covering nominal flow, contract enforcement, semantic correctness, performance, error propagation, and regression detection |
| **System Invariants** (INV-1–8) | 8 pipeline-wide invariants — silent drops forbidden, unique IDs, no output without ACCEPTED status, checksum integrity, contradiction resolution, session isolation, and latency budget |
| **Handoff Contract v2** | Full JSON schema, 9 ordered validation rules (VR-1–9) with error codes, and a 4-class error protocol (Transient / Structural / Data / Context) with retry limits and fallbacks |
| **Test Environment** | Isolated `integration-test` namespace, deterministic seeds, DEBUG logging, pre-run flush requirements |

### AB1–AB8 Simulation Suite

| Test | Type | Key Coverage |
|------|------|--------------|
| **AB1** | Happy Path | Full nominal flow, all 7 assertions including latency ≤ 2000 ms |
| **AB2** | Negative / Boundary | Empty `raw_thought` → `ERR_THOUGHT_EMPTY` → regen retry |
| **AB3** | Degraded Path | `context_window.overflow: true` → `synthesis_mode: degraded` |
| **AB4** | Adversarial | Missing ID (abort), short vector (regen), tampered checksum (retry ×3) |
| **AB5** | Concurrency | Dual concurrent sessions, `cross_session_leak_count == 0` |
| **AB6** | Fault Injection | `status: partial` (degraded synthesis) and `status: aborted` (bypass synthesis) |
| **AB7** | Semantic | Contradiction pair detection, cosine-similarity threshold, annotated output |
| **AB8** | Full Regression | 12 sub-tests covering all prior cases + max sequence, duplicate ID replay, temperature extremes |

### Supporting Sections
- **Pass/Fail Criteria** — suite-level and conditional-promotion rules
- **Defect Classification** — Critical through Low with resolution SLAs
- **Traceability Matrix** — test cases × objectives cross-reference

---
