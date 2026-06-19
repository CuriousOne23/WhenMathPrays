# TS Path A+B Integration Test Plan

**Version:** TS-ITP-AB-002
**Date:** 2026-06-19
**Status:** Active

This version introduces:
- Numeric scoring (A-Score, B-Score, AB-Score each 0-100)
- Separate expectations for Path A, Path B, and A+B integration
- Full system invariants and handoff contract
- Explicit metrics with clear pass/fail thresholds
- Complete AB1-AB8 simulation suite

---

## 0. Scoring Framework

Each test produces three scores, each 0-100:

| Component | Meaning | Passing Threshold |
|-----------|---------|-------------------|
| A-Score | Path A correctness | >= 90 |
| B-Score | Path B correctness | >= 90 |
| AB-Score | A+B integration correctness | >= 90 |

**Final test result:**
- PASS if all three scores >= 90
- FAIL otherwise

---

## 1. Test Objectives

| ID | Objective | Priority |
|----|-----------|----------|
| TO-1 | Verify nominal data flow from Path A output to Path B input across all packet types | Critical |
| TO-2 | Confirm handoff contract schema is enforced; reject any non-conforming packet | Critical |
| TO-3 | Validate Path B synthesis produces deterministic, semantically correct output for every canonical input class | High |
| TO-4 | Ensure the pipeline maintains all declared system invariants under normal and degraded conditions | High |
| TO-5 | Characterize latency and throughput at the A-B boundary under nominal and peak load | Medium |
| TO-6 | Confirm error propagation, retry, and fallback behaviors match specification | High |
| TO-7 | Detect regressions in previously passing test cases upon any change to either path | Critical |

---

## 2. System Invariants

These invariants **must hold** across every test case. Any violation is an automatic Critical defect.

| ID | Invariant | Enforcement Point |
|----|-----------|-------------------|
| INV-1 | Every packet Path A marks status:complete must be accepted or explicitly rejected - silent drops forbidden | HandoffValidator |
| INV-2 | thought_id is globally unique per session and must survive round-trip serialization unchanged | Serializer + Validator |
| INV-3 | Path B must never emit output without a packet whose validation_status is ACCEPTED | SynthesisEngine |
| INV-4 | A REJECTED packet must trigger the configured error protocol within error_timeout_ms | Error Handler |
| INV-5 | Contradiction detection must complete before synthesis; contradictions must be resolved or flagged, never null on output | ContradictionDetector |
| INV-6 | End-to-end latency must not exceed p99_latency_budget_ms under nominal load | Performance Monitor |
| INV-7 | No thought packet payload may be mutated between Path A serialization and Path B deserialization | Serializer + Validator |
| INV-8 | Concurrent simulation instances must not allow cross-session packet leakage | Session Isolation Layer |

---

## 3. Handoff Contract - Path A to Path B

### 3.1 Contract Schema v2

| Field | Type | Constraint |
|-------|------|------------|
| schema_version | string | "2.0" |
| thought_id | uuid-v4 | Unique per session |
| session_id | uuid-v4 | Matches active session |
| sequence_index | integer | 0-based, monotonically increasing |
| status | enum | complete, partial, aborted |
| timestamp_ms | integer | Unix epoch ms, Path A completion time |
| thought_vector | float[512] | Normalized L2; each element in [-1.0, 1.0] |
| raw_thought | string | Non-empty, max 8192 UTF-8 chars |
| synthesis_mode | enum | normal, degraded, fallback |
| context_window.tokens_used | integer | <= tokens_budget |
| context_window.tokens_budget | integer | Positive integer |
| context_window.overflow | boolean | True if tokens_used == tokens_budget |
| metadata.path_a_version | string | Semver |
| metadata.model_tag | string | Any |
| metadata.temperature | float | 0.0 to 2.0 inclusive |
| metadata.seed | integer or null | Any |
| checksum | string | SHA-256 hex of thought_id + raw_thought + timestamp_ms |

### 3.2 Validation Rules VR-1 through VR-9

Path B enforces rules in this exact order. First failure short-circuits and returns REJECTED.

| Order | Rule | Field | Condition | Error Code | Error Class |
|-------|------|-------|-----------|------------|-------------|
| 1 | VR-1 | thought_id | Present, valid UUID v4, unique within session | ERR_ID_INVALID | Structural |
| 2 | VR-2 | session_id | Present, valid UUID v4, matches active session | ERR_SESSION_MISMATCH | Structural |
| 3 | VR-3 | sequence_index | Integer >= 0; equals last_accepted_index + 1, or 0 if first | ERR_SEQUENCE_GAP | Transient |
| 4 | VR-4 | status | One of: complete, partial, aborted | ERR_STATUS_UNKNOWN | Structural |
| 5 | VR-5 | thought_vector | Float[512]; each in [-1.0,1.0]; L2 norm in [0.99,1.01] | ERR_VECTOR_MALFORMED | Data |
| 6 | VR-6 | raw_thought | Non-empty string, max 8192 UTF-8 chars | ERR_THOUGHT_EMPTY / ERR_THOUGHT_OVERFLOW | Data |
| 7 | VR-7 | context_window | Object present; tokens_used <= tokens_budget; overflow boolean | ERR_CONTEXT_INVALID | Context |
| 8 | VR-8 | checksum | SHA-256(thought_id + raw_thought + timestamp_ms) matches | ERR_CHECKSUM_FAIL | Transient |
| 9 | VR-9 | metadata.temperature | Float in [0.0, 2.0] | ERR_META_INVALID | Data |

### 3.3 Error Protocol by Class

| Error Class | Codes | Action | Max Retries | Fallback |
|-------------|-------|--------|-------------|----------|
| Transient | ERR_SEQUENCE_GAP, ERR_CHECKSUM_FAIL | Retry with exponential backoff base 200 ms | 3 | Abort session |
| Structural | ERR_ID_INVALID, ERR_SESSION_MISMATCH, ERR_STATUS_UNKNOWN | Abort immediately; escalate to ErrorHandler | 0 | Emit output_status: error |
| Data | ERR_THOUGHT_EMPTY, ERR_THOUGHT_OVERFLOW, ERR_VECTOR_MALFORMED, ERR_META_INVALID | Log and skip; request Path A regeneration | 1 | Use last valid packet if available |
| Context | ERR_CONTEXT_INVALID | Log warning; proceed in degraded mode | 0 | Set synthesis_mode: degraded |

---

## 4. Test Structure (Used for AB1-AB8)

Each test contains:
1. **Input Specification** - raw input, metadata, fault injection if any, concurrency conditions if any
2. **Path A Expected Output** - meaning envelope, referent map, OB/RB/TB trace, truth-state (TPTB), safety-state (TPSF), stability envelope, invariants, error class if applicable
3. **Path B Expected Output** - expression envelope, tone, stance, style, discourse mode, final natural-language output, human-readable TP projection
4. **A+B Integration Expectations** - meaning preserved, truth preserved, safety preserved, no referent drift, no semantic mutation, expression applied correctly, TP internally consistent
5. **Metrics** - latency, routing correctness, truth/safety correctness, referent stability, checksum integrity, cross-session leak count, error-class correctness
6. **Scoring** - A-Score (0-100), B-Score (0-100), AB-Score (0-100)

---

## 5. AB1-AB8 Simulation Suite

---

### AB1 - Happy Path

**Purpose:** Verify nominal end-to-end flow for a clean, unambiguous input across the full A+B pipeline.

| Field | Value |
|-------|-------|
| Test ID | AB1 |
| Priority | Critical |
| Type | Happy Path |
| Seed | 42 |
| Invariants | INV-1, INV-2, INV-3, INV-5, INV-6, INV-7 |

#### Input
- Clean, unambiguous user message
- All fields valid; status: complete; sequence_index: 0
- No fault injection

#### Path A Expected Output
- Correct meaning envelope
- Correct referents; complete referent map
- Correct OB/RB/TB trace
- TPTB = TRUE or SUPPORTED
- TPSF = SAFE
- synthesis_mode: normal
- No errors; all invariants satisfied

#### Path B Expected Output
- Tone appropriate to input
- No semantic drift from Path A envelope
- Style applied correctly
- Human-readable TP projection correct

#### A+B Integration Expectations
- Meaning preserved across handoff
- Truth preserved (TPTB unchanged)
- Safety preserved (TPSF = SAFE)
- Expression applied correctly without mutation
- TP internally consistent

#### Metrics
| Metric | Target |
|--------|--------|
| Latency A | <= 40 ms |
| Latency B | <= 15 ms |
| Latency end-to-end p99 | <= 2000 ms |
| Routing correctness | >= 98% |
| Referent stability | 100% |
| Checksum valid | Yes |
| Cross-session leak count | 0 |

#### Scoring
| Score | Points Awarded When |
|-------|---------------------|
| A-Score (0-100) | Path A output matches all expected fields above |
| B-Score (0-100) | Path B output matches expression and TP expectations |
| AB-Score (0-100) | Integration expectations all satisfied; all metrics met |

**Pass Criteria:** A-Score >= 90, B-Score >= 90, AB-Score >= 90

---

### AB2 - Boundary Conditions

**Purpose:** Verify correct pipeline behavior at minimal and maximal valid input boundaries, including empty-thought regen.

| Field | Value |
|-------|-------|
| Test ID | AB2 |
| Priority | High |
| Type | Boundary |
| Seed | 101 |
| Invariants | INV-1, INV-4 |

#### Sub-cases
- AB2-a: raw_thought at minimum (1 char)
- AB2-b: raw_thought at maximum (8192 chars)
- AB2-c: raw_thought empty string - fault injection triggering regen path

#### Path A Expected Output
- Meaning envelope correct at boundaries
- TPTB = TRUE or UNKNOWN
- TPSF = SAFE
- No silent drops (INV-1)
- AB2-c: triggers regen; retry count = 1; second attempt valid

#### Path B Expected Output
- Minimal expression without hallucination
- No over-interpretation of sparse input
- No invented meaning for empty-thought case

#### A+B Integration Expectations
- No referent drift at boundaries
- No over-projection on minimal input
- AB2-c: final output_status = success after 1 retry

#### Metrics
| Metric | Target |
|--------|--------|
| Latency end-to-end p99 | <= 2000 ms |
| Routing correctness | >= 95% |
| Retry count AB2-c | = 1 |
| Error code AB2-c first attempt | ERR_THOUGHT_EMPTY |
| output_status AB2-c | success |

#### Scoring
| Score | Points Awarded When |
|-------|---------------------|
| A-Score (0-100) | Boundary packets well-formed; regen triggered correctly on empty |
| B-Score (0-100) | No hallucination or over-interpretation at boundaries |
| AB-Score (0-100) | All sub-cases resolve to success; retry protocol respected |

**Pass Criteria:** A-Score >= 90, B-Score >= 90, AB-Score >= 90

---

### AB3 - Degraded Input

**Purpose:** Confirm the pipeline handles noisy, partial, or context-overflow input by activating degraded synthesis mode without aborting.

| Field | Value |
|-------|-------|
| Test ID | AB3 |
| Priority | High |
| Type | Degraded Path |
| Seed | 256 |
| Invariants | INV-1, INV-3, INV-5, INV-6 |

#### Sub-cases
- AB3-a: context_window.overflow: true; tokens_used == tokens_budget
- AB3-b: noisy or partial raw_thought (recoverable)

#### Path A Expected Output
- Meaning envelope repaired where possible
- TPTB = UNKNOWN or PARTIAL
- TPSF = SAFE
- Repair markers present in metadata
- synthesis_mode: degraded emitted

#### Path B Expected Output
- Neutral tone; no invented meaning
- Degraded flag respected; no confident assertions on incomplete input

#### A+B Integration Expectations
- Meaning preserved within repair limits
- No semantic invention by Path B
- synthesis_mode: degraded propagated to output metadata
- output_status = success

#### Metrics
| Metric | Target |
|--------|--------|
| Latency end-to-end p99 | <= 2000 ms |
| Repair success rate | >= 90% |
| Hallucination count | 0 |
| synthesis_mode in output | degraded |
| output_status | success |

#### Scoring
| Score | Points Awarded When |
|-------|---------------------|
| A-Score (0-100) | Meaning envelope repaired; synthesis_mode set correctly |
| B-Score (0-100) | No hallucination; neutral tone maintained |
| AB-Score (0-100) | Degraded mode propagated; output_status = success |

**Pass Criteria:** A-Score >= 90, B-Score >= 90, AB-Score >= 90

---

### AB4 - Fault Injection

**Purpose:** Stress-test the validator with structurally corrupt packets.

| Field | Value |
|-------|-------|
| Test ID | AB4 |
| Priority | Critical |
| Type | Adversarial |
| Seed | 999 |
| Invariants | INV-1, INV-4, INV-7 |

#### Sub-cases
- AB4-a: thought_id absent -> ERR_ID_INVALID (Structural)
- AB4-b: thought_vector length 256 instead of 512 -> ERR_VECTOR_MALFORMED (Data)
- AB4-c: checksum last byte XOR 0xFF -> ERR_CHECKSUM_FAIL (Transient; up to 3 retries)

#### Path A Expected Output
- TPSF = BLOCK on all sub-cases
- Error class correctly classified: Structural, Data, or Transient
- No meaning envelope produced for Structural faults

#### Path B Expected Output
- No synthesis on Structural faults; error message only
- Regen attempted on Data fault (1 retry)
- Retry up to 3x on Transient fault; abort if exhausted

#### A+B Integration Expectations
- Safety boundary respected in all sub-cases
- No partial output leakage
- INV-7 audit log confirms payload integrity assessment

#### Metrics
| Metric | AB4-a | AB4-b | AB4-c |
|--------|-------|-------|-------|
| Error code | ERR_ID_INVALID | ERR_VECTOR_MALFORMED | ERR_CHECKSUM_FAIL |
| Error class | Structural | Data | Transient |
| output_status | error | success after regen | error if retries exhausted |
| Synthesis attempted | No | After regen | No |
| Max retries | 0 | 1 | 3 |

#### Scoring
| Score | Points Awarded When |
|-------|---------------------|
| A-Score (0-100) | Correct error class emitted per sub-case |
| B-Score (0-100) | No synthesis on Structural; correct fallback on Data and Transient |
| AB-Score (0-100) | All error-class dispatch rules correct; no output leakage |

**Pass Criteria:** A-Score >= 90, B-Score >= 90, AB-Score >= 90

---

### AB5 - Concurrency

**Purpose:** Confirm two simultaneous simulation sessions produce independent outputs with zero cross-session packet leakage.

| Field | Value |
|-------|-------|
| Test ID | AB5 |
| Priority | Critical |
| Type | Concurrency / Isolation |
| Seeds | Session-A: 10; Session-B: 20 |
| Invariants | INV-2, INV-8 |

#### Input
- Session-A and Session-B launched within 50 ms of each other
- Each session generates 5 packets with distinct deterministic seeds
- session_id fields are distinct UUIDs

#### Path A Expected Output
- Session isolation maintained per session
- No cross-session contamination of thought_id or session_id
- cross_session_leak_count = 0

#### Path B Expected Output
- Two independent expression envelopes, one per session
- No interleaving of thought_id values across session queues

#### A+B Integration Expectations
- Session-A output thought_id set and Session-B output thought_id set are disjoint
- No ERR_SESSION_MISMATCH logged
- Both sessions complete with output_status = success

#### Metrics
| Metric | Target |
|--------|--------|
| Cross-session leak count | 0 |
| Session isolation | 100% |
| ERR_SESSION_MISMATCH events | 0 |
| Latency slower session p99 | <= 2x p99_latency_budget_ms |
| output_status both sessions | success |

#### Scoring
| Score | Points Awarded When |
|-------|---------------------|
| A-Score (0-100) | No cross-session contamination in Path A output |
| B-Score (0-100) | Independent expression envelopes; no interleaving |
| AB-Score (0-100) | Leak count = 0; both sessions succeed |

**Pass Criteria:** A-Score >= 90, B-Score >= 90, AB-Score >= 90

---

### AB6 - Structural Corruption / Partial and Aborted Status

**Purpose:** Validate pipeline behavior when Path A emits status: partial or status: aborted, and when the handoff packet contains structural corruption.

| Field | Value |
|-------|-------|
| Test ID | AB6 |
| Priority | High |
| Type | Fault Injection / Degraded Path |
| Seed | 77 |
| Invariants | INV-1, INV-3, INV-4, INV-5 |

#### Sub-cases
- AB6-a: status: partial - valid thought content, incomplete
- AB6-b: status: aborted - minimal valid fields, no thought content
- AB6-c: malformed JSON missing closing brace - Structural fault

#### Path A Expected Output
- AB6-a: TPSF = SAFE; synthesis_mode: partial
- AB6-b: TPSF = SAFE; no meaning envelope
- AB6-c: TPSF = BLOCK; error class = Structural

#### Path B Expected Output
- AB6-a: Accept; synthesize with synthesis_mode: partial; no hallucination on incomplete input
- AB6-b: Accept; skip synthesis; emit output_status: aborted
- AB6-c: No synthesis; error message only

#### A+B Integration Expectations
- AB6-a: synthesis_mode: partial propagated; contradictions field populated or [] never null
- AB6-b: SynthesisEngine NOT invoked; OutputEmitter fires within error_timeout_ms
- AB6-c: Safety preserved; no partial output

#### Metrics
| Metric | AB6-a | AB6-b | AB6-c |
|--------|-------|-------|-------|
| validation_status | ACCEPTED | ACCEPTED | REJECTED |
| synthesis_mode | partial | n/a | n/a |
| output_status | success | aborted | error |
| Synthesis invoked | Yes | No | No |
| contradictions null | Never | N/A | N/A |

#### Scoring
| Score | Points Awarded When |
|-------|---------------------|
| A-Score (0-100) | Status-based dispatch correct; synthesis_mode emitted correctly |
| B-Score (0-100) | Correct behavior per status; no hallucination on partial |
| AB-Score (0-100) | All sub-case output_status correct; contradictions never null |

**Pass Criteria:** A-Score >= 90, B-Score >= 90, AB-Score >= 90

---

### AB7 - Semantic Contradiction

**Purpose:** Verify ContradictionDetector identifies logically contradictory thought pairs and SynthesisEngine surfaces rather than silently suppresses the contradiction.

| Field | Value |
|-------|-------|
| Test ID | AB7 |
| Priority | High |
| Type | Semantic Validation |
| Seed | 512 |
| Invariants | INV-3, INV-5 |

#### Input
- 3-packet sequence in a single session
- P1: baseline assertion (X is true)
- P2: direct contradiction of P1 (X is false); cosine similarity of thought_vector to P1 < -0.7
- P3: neutral; no contradiction

#### Path A Expected Output
- TPTB = CONTRADICTORY for P1/P2 pair
- Both claims represented in meaning envelope; no collapse to one side
- P3: TPTB = TRUE or SUPPORTED

#### Path B Expected Output
- Neutral tone on contradiction - no resolution invented
- Contradiction annotation emitted: synthesis_note: contradiction_detected
- P3 processed normally with contradictions: []

#### A+B Integration Expectations
- contradictions for P2 non-empty (INV-5 satisfied)
- contradictions[0].pair contains both P1.thought_id and P2.thought_id
- Output is annotated, not incorrectly merged
- output_status = success for all three packets

#### Metrics
| Metric | Target |
|--------|--------|
| Contradiction detection rate | >= 95% |
| contradictions null at synthesis | Never |
| synthesis_note | contradiction_detected |
| P3 contradictions | [] |
| output_status | success |

#### Scoring
| Score | Points Awarded When |
|-------|---------------------|
| A-Score (0-100) | TPTB = CONTRADICTORY correctly set; both claims preserved |
| B-Score (0-100) | Neutral tone; contradiction surfaced, not suppressed |
| AB-Score (0-100) | Contradictions field non-null; annotation correct; P3 clean |

**Pass Criteria:** A-Score >= 90, B-Score >= 90, AB-Score >= 90

---

### AB8 - Regression Sweep

**Purpose:** Execute all canonical packet classes and previously-reported bug-fix scenarios in one automated sweep to catch regressions across the full A+B boundary.

| Field | Value |
|-------|-------|
| Test ID | AB8 |
| Priority | Critical |
| Type | Regression / Comprehensive |
| Seed | 314159 global; per-sub-test overrides apply |
| Invariants | INV-1 through INV-8 (all) |

#### Sub-test Manifest

| Sub-test | Description | Derived From | Expected Result |
|----------|-------------|--------------|-----------------|
| AB8-01 | Nominal single packet | AB1 | output_status: success; all scores >= 90 |
| AB8-02 | Empty thought regen | AB2-c | output_status: success after 1 retry |
| AB8-03 | Context overflow degraded | AB3-a | synthesis_mode: degraded; output_status: success |
| AB8-04a | Missing thought_id | AB4-a | ERR_ID_INVALID; abort; output_status: error |
| AB8-04b | Short vector 256 elements | AB4-b | ERR_VECTOR_MALFORMED; regen; success |
| AB8-04c | Bad checksum retries exhausted | AB4-c | Session aborted; output_status: error |
| AB8-05 | Concurrent dual-session | AB5 | cross_session_leak_count = 0; both success |
| AB8-06a | status: partial | AB6-a | synthesis_mode: partial; success |
| AB8-06b | status: aborted | AB6-b | output_status: aborted; no synthesis |
| AB8-07 | Contradiction pair | AB7 | contradictions non-empty; annotated |
| AB8-08 | Max sequence length 50 packets | New | All accepted; monotonic sequence_index |
| AB8-09 | Duplicate thought_id replay | New | Second packet ERR_ID_INVALID; first unaffected |
| AB8-10 | temperature: 0.0 greedy | New | Valid; output_status: success |
| AB8-11 | temperature: 2.0 max entropy | New | Valid; output_status: success |
| AB8-12 | seed: null non-deterministic | New | Valid schema; output_status: success |

#### Path A Expected Output
- All prior failures fixed; no regressions introduced
- Error classes correctly assigned across all sub-tests

#### Path B Expected Output
- Stable expression across all sub-tests
- Correct synthesis_mode per sub-test

#### A+B Integration Expectations
- All 8 system invariants INV-1 through INV-8 satisfied
- Zero unhandled exceptions in any component log
- Regression delta: no previously-passing sub-test may newly fail

#### Metrics
| Metric | Target |
|--------|--------|
| Sub-tests passing | 15 / 15 |
| Invariant violations | 0 |
| Regression delta | 0 newly failing sub-tests |
| Unhandled exceptions | 0 |
| Total sweep duration | <= 15 min on reference hardware |

#### Scoring
| Score | Points Awarded When |
|-------|---------------------|
| A-Score (0-100) | All Path A expectations met across all 15 sub-tests |
| B-Score (0-100) | All Path B expectations met across all 15 sub-tests |
| AB-Score (0-100) | All invariants green; regression delta = 0; metrics met |

**Pass Criteria:** A-Score >= 90, B-Score >= 90, AB-Score >= 90

---

## 6. Suite-Level Pass / Fail Criteria

The A+B Integration Test Suite **passes** if and only if:
1. All Critical priority tests AB1, AB4, AB5, AB8 pass with all three scores >= 90
2. All High priority tests AB2, AB3, AB6, AB7 pass with all three scores >= 90
3. Zero Critical or High defects remain open
4. All 8 system invariants INV-1 through INV-8 pass in the AB8 regression sweep
5. Performance: p99 latency <= 2000 ms across all nominal tests

---

## 7. Defect Classification

| Severity | Criteria | Resolution SLA |
|----------|----------|----------------|
| Critical | System invariant violated; data corruption; session leakage; silent drop | Must fix before any promotion |
| High | Assertion failure in non-invariant area; wrong error code; wrong synthesis_mode | Must fix before staging |
| Medium | p50 latency budget exceeded (p99 still met); non-critical log noise | Fix within 1 sprint |
| Low | Documentation mismatch; cosmetic log formatting | Fix within 2 sprints |

---

## 8. Traceability Matrix

| Test | TO-1 | TO-2 | TO-3 | TO-4 | TO-5 | TO-6 | TO-7 |
|------|------|------|------|------|------|------|------|
| AB1 | Y | Y | Y | Y | Y | | |
| AB2 | | Y | | Y | | Y | |
| AB3 | Y | Y | Y | Y | Y | | |
| AB4 | | Y | | Y | | Y | |
| AB5 | Y | Y | | Y | | | |
| AB6 | Y | Y | Y | Y | | Y | |
| AB7 | Y | | Y | Y | | | |
| AB8 | Y | Y | Y | Y | Y | Y | Y |

---

## 9. Revision History

| Version | Date | Change Summary |
|---------|------|----------------|
| TS-ITP-AB-001 | 2026-06-17 | Initial draft |
| TS-ITP-AB-002 | 2026-06-19 | Numeric scoring added; separate A/B/AB expectations; full invariants and handoff contract v2 integrated |
