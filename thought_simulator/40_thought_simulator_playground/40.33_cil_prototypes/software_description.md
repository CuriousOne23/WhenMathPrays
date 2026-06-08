# 40.33_cil_prototypes / software_description.md

## Approval State
- Phase A (base FIFO/classification): **approved**; Phase B executed **2026-06-03**
- Phase A (W2 clarification-event wire): **approved** (CP review, 2026-06-08; 40.510-205)
- Phase B (W2 extension): not started — clarification wire harness blocked until explicit Phase B go-ahead
- Program row: **40.510-205** (W2)

## Two-Phase Execution Model (Global 40.* Rule)

- Phase A: define and review `software_description.md` only.
- Mandatory stop after Phase A until explicit human approval.
- Phase B (only after approval): implement `prototype.py`, `harness.py`, `verification_capsule.md`, `requirements_delta.md`, and artifacts.

## 1. Purpose

Define deterministic Conversation Integration Layer (CIL) prototype behavior for TP/MTP conversation intake, FIFO-preserving integration, deterministic classification, supervisory escalation flow, and auditable lifecycle outcomes.

## 2. Scope

- deterministic FIFO ingestion and queue processing for conversation packets
- deterministic snapshot coherence and sequence-token ordering controls
- deterministic classification and tie-break behavior under explicit profile policy
- deterministic ambiguity escalation to GB with bounded timeout/default and late-approval re-entry handling
- deterministic reject-with-audit handling for unsupported profile/policy/enum states

This document now serves as the governing design baseline for the executed Phase B prototype and harness.

## 3. Source Index (Requirement Anchors)

Primary normative sources:

- `thought_simulator/20_requirements/20.33_cil_requirements.md`
- `thought_simulator/20_requirements/20.30_ts_functional_model.md`
- `thought_simulator/20_requirements/20.10_ts_architectural_principles.md`
- `thought_simulator/20_requirements/20.80_gb_requirements.md`
- `thought_simulator/20_requirements/20.150_tcu_budgeting_requirements.md`
- `thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md`
- `thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md`

## 4. Functional Boundaries

CIL does:

- own deterministic TP/MTP conversation intake and FIFO-preserving integration sequence
- classify conversation thread state under explicit confidence and tie-break policy
- escalate ambiguity to GB only through deterministic supervisory request channels
- apply deterministic timeout/default and late-approval re-entry outcomes
- preserve append-only audit records for intake, classification, escalation, and supervisory outcomes

CIL does not:

- directly instantiate inquiry channels without GB approval
- bypass GB supervisory decision paths
- mutate OB, RB, TB, IB, InB, OuB, or MTP internal implementation state
- make ordering decisions based on wall-clock precedence

## 5. IO Contract

Inbound contract (JSON-compatible):

- `event_type` (enum): `ingest|process_next|gb_response|profile_change`
- `sequence` (integer): deterministic ordering token
- `safe_boundary` (bool): routing/escalation policy mutation gate
- `snapshot_id` (string): deterministic snapshot pin
- `packet_id` (string): deterministic packet identity
- `confidence` (float): classification confidence in [0, 1]
- `profile_signature` (string): execution signature-bound profile key
- `decision` (enum): `approve|deny|timeout|late_approve` for GB response

Outbound contract (JSON-compatible):

- `sequence` (integer)
- `pending_queue` (array)
- `integrated_packets` (array)
- `escalation_requests` (array)
- `audit_log` (array)
- `active_profile` (string)
- `verification_digest` (string)

## 6. Deterministic Invariants

- FIFO order is preserved from intake through integration outputs
- processing sequence is monotonic and must advance by one per accepted event
- classification/tie-break outcomes are deterministic for fixed profile + input packet
- unsupported profile/policy/enum states deterministically reject with fixed reason codes
- routing/escalation-affecting transitions occur only at deterministic safe boundaries
- profile precedence uses active signature-bound profile over environment defaults

### GB timeout/default semantics

On GB non-response within policy-bound tick budget (HLR-006): CIL applies a **deterministic default** by safety/operation class — `deny` for high-risk escalation classes, `timeout` audit record for bounded-wait classes — never wall-clock race. Late `late_approve` re-entry (HLR-007, -023) follows fixed policy: `ignore` (stale), `queue` (re-process at next safe boundary), or `compensate` (append corrective audit only); outcome is profile-bound and replay-stable.

### Replay determinism (W3 pointer)

Identical intake sequence + profile signature + GB response fixtures SHALL yield identical `integrated_packets`, `escalation_requests`, and `verification_digest` (HLR-013, -026). CIL replay invariants feed W3 orchestration glue (40.510-501–506); Phase B harness MUST prove byte-stable audit export for fixed seeds before W3 integration bundles consume CIL evidence.

## 7. TCU and Tick-Budget Expectations

- CIL prototype execution must remain bounded per tick phase under constraints in `20.150_tcu_budgeting_requirements.md`
- Harness evidence should support future cycle budgeting fields: `scenario_id`, `seed`, `N`, `config_hash`, `cycles_measured`
- measured cycle budgets are promotion-controlled through 30 verification capsules

## 8. Verification Intent for Phase B

Planned positive checks:

- deterministic FIFO intake and snapshot coherence behavior
- deterministic classification/tie-break and ambiguity escalation behavior
- deterministic GB supervisory response handling, timeout/default, and re-entry semantics
- deterministic profile precedence over environment defaults

Planned negative-path checks:

- unsupported profile/enum rejection with fixed reason codes
- out-of-order sequence rejection
- safe-boundary violation rejection
- direct-inquiry bypass rejection without GB approval

### Invariant → 20.33 HLR mapping (base)

| Invariant / topic | HLR anchors (20.032) | Phase-B scenario focus |
|-------------------|----------------------|------------------------|
| FIFO intake / ordering | 001, 014, 022 | deterministic FIFO intake; out-of-order rejection |
| snapshot coherence | 002 | snapshot pin coherence |
| classification / tie-break | 003, 008, 009 | deterministic classification |
| GB escalation | 004, 005, 018 | ambiguity escalation; bypass rejection |
| timeout / default / late-approve | 006, 007, 023 | GB timeout/default; re-entry semantics |
| profile precedence | 012, 019 | profile precedence over defaults |
| safe boundaries | 015 | safe-boundary violation rejection |
| audit / reason codes | 010, 011, 020–021, 024 | reject-with-audit paths |
| boundaries / isolation | 016–017 | no A/B basin mutation |
| parent compliance / testability | 025–026 | fixture oracle; replay determinism (§6) |

## 9. Promotion Readiness Conditions

Before promotion from 40 to 30:

- executable harness with deterministic pass/fail scenario set
- artifact evidence covering FIFO/classification/escalation invariants
- explicit HLR/LLR mapping to 20.33 and parent anchors
- completed `verification_capsule.md` and `requirements_delta.md` with traceable scenario records

---

## W2 Phase A Extension (40.510-205)

**Approval State:** Phase A extension **approved** (CP review, 2026-06-08; base Phase B from 2026-06-03 remains valid).

**Program row:** [40.510-205](../40.510_refactor.md) — targeted redo for **`clarification_event` wire to UPI**.

### Purpose (W2 delta)

Extend CIL to emit deterministic `clarification_event` records (FIFO per conversation) consumed by [40.103](../40.103_upi_prototypes/software_description.md) UPI per [20.33](../../20_requirements/20.33_cil_requirements.md) and [20.103](../../20_requirements/20.103_upi_requirements.md) HLR-20.103-003/005/018. Closes IIInB escalation → CIL → UPI path deferred from W1.

### What Phase B Must Explore (W2)

| Scenario | HLR anchor | Expected |
|----------|------------|----------|
| `positive_escalation_to_clarification_event` | 20.101 → 20.33 | IIInB escalation ref → CIL emits event |
| `positive_fifo_clarification_ordering` | 20.103-005 | Events consumed by UPI in FIFO order |
| `positive_integration_seq_monotonic` | 20.103-013 | Deterministic sequence tokens |
| `negative_incomplete_clarification_payload` | 20.103-008 | Event rejected before UPI handoff |

### Dependencies
- GATE-B closed on 40.510-201, 40.510-202
- [40.101_iiinb_prototypes](../40.101_iiinb_prototypes/software_description.md) (escalation source)

### Flows Alignment (W2 extension)
- **Forward Flow:** 20.33 + 20.103 clarification wire
- **Backward Flow:** Prior CIL Phase B (2026-06-03) — extend FIFO wire scenarios
- **Iterative Design Flow:** None yet

### HLR family → Phase-B scenario mapping (W2 extension)

| HLR family | Topic | Primary scenario IDs |
|------------|-------|----------------------|
| 027–028 | IIInB escalation intake | `positive_escalation_to_clarification_event` |
| 029–030 | `clarification_event` emit + FIFO | `positive_fifo_clarification_ordering`, `positive_integration_seq_monotonic` |
| 031–033 | Wire-only handoff (no USP write) | structural negatives in harness setup |
| 20.103-008 | Incomplete payload guard | `negative_incomplete_clarification_payload` |

**Agreement Statement:** Aligned — W2 extension Phase A approved (CP, 2026-06-08). Clarification wire scoped per 20.032-027–033 and 20.103-003/005; prior classification/FIFO evidence must remain green on regression.
