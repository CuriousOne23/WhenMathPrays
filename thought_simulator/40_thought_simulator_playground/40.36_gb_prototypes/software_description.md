# 40.36_gb_prototypes / software_description.md

## Approval State
Phase A draft complete. Pending explicit human approval before Phase B execution.

## Two‑Phase Execution Model (Global 40.* Rule)

- **Phase A:** define and review `software_description.md` only.  
- **Mandatory stop after Phase A** until explicit human approval.  
- **Phase B (after approval):** implement `prototype.py`, `harness.py`, `verification_capsule.md`, `requirements_delta.md`, and artifacts.

---

# 1. Purpose

Define deterministic Global Basin (GB) prototype behavior for:

- global supervisory evaluation  
- drift/oscillation detection  
- cross‑cycle coherence  
- IB creation approval  
- IB evolution supervision  
- IB merge/split supervision  
- IB promotion/retirement approval  
- OB decomposition supervision  
- COP proposal gating  
- safe‑boundary supervisory action application  
- deterministic supervisory logging  
- bounded TCU‑envelope execution  

GB is a **non‑mutating supervisory subsystem**: it evaluates global semantic stability and issues **bounded supervisory actions** without altering TP/MTP meaning‑construction state.

---

# 2. Scope

This prototype covers:

- deterministic TS→GB→TS supervisory flow  
- asynchronous supervisory evaluation  
- deterministic safe‑boundary gating  
- deterministic supervisory action selection  
- deterministic supervisory logging  
- bounded TCU envelope behavior  
- deterministic fallback/degradation behavior  
- deterministic supervisory command interface  
- deterministic handling of IB creation, evolution, merge/split, promotion  
- deterministic handling of OB decomposition and OB retirement  
- deterministic handling of COP proposal approval  
- deterministic supervisory interrupt semantics  

This prototype does **not**:

- mutate TP/MTP meaning‑construction state  
- read OB/RB/TB/IB internal state  
- perform semantic inference  
- perform unbounded search  
- use wall‑clock precedence  
- bypass TS arbitration or safe‑boundary rules  

---

# 3. Source Index (Requirement Anchors)

Primary normative sources:

- `thought_simulator/20_requirements/20.10_ts_architectural_principles.md`  
  - “GB SHALL perform global supervisory decisions, including inquiry gating, branching control, stability evaluation, drift/oscillation detection, and safety‑mode transitions.”  
- `thought_simulator/20_requirements/20.20_ts_primitives.md`  
  - “GB SHALL apply global constraints/policies deterministically and SHALL NOT bypass primitive interface contracts.”  
- `thought_simulator/20_requirements/20.30_ts_functional_model.md`  
  - TS→GB→TS supervisory flow, IB creation gating, IB evolution supervision, IB promotion, OB decomposition, safe‑boundary rules.  
- `thought_simulator/20_requirements/20.80_gb_requirements.md`  
  - Canonical GB requirement anchor: drift detection, supervisory actions, TCU envelope, fallback behavior, logging, inquiry governance.  

Secondary architectural sources:

- `thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md`  
- `thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md`

---

# 4. Functional Boundaries

## GB does:

- evaluate global semantic stability  
- detect drift, oscillation, divergence, convergence  
- classify supervisory requests  
- approve/deny IB creation  
- supervise IB evolution  
- supervise IB merge/split  
- supervise IB promotion/retirement  
- supervise OB decomposition  
- supervise COP proposal activation  
- issue bounded supervisory actions (Stop, Slow, Dampen, Escalate, Safe‑Mode, Reduce‑Depth, Suspend‑Inquiry, Crop, Prune, Reshape, Kill)  
- operate asynchronously relative to TS  
- apply actions only at deterministic safe boundaries  
- maintain append‑only supervisory logs  
- operate within a bounded TCU envelope  
- degrade deterministically when over budget  
- expose deterministic supervisory command interface  
- produce deterministic supervisory output objects  

## GB does **not**:

- mutate TP/MTP meaning‑construction state  
- read OB/RB/TB/IB internal state  
- read MTP internal state  
- block TS execution  
- perform unbounded or data‑dependent work  
- use wall‑clock precedence for ordering  
- bypass TS arbitration or safe‑boundary rules  
- perform semantic inference or latent‑state reasoning  

---

# 5. IO Contract

## Inbound contract (JSON‑compatible)

- `event_type` (enum):  
  `inquiry_request|supervisory_signal|ib_update|ib_merge|ib_split|ib_promotion|ob_decomposition|cop_proposal|external_command`
- `sequence` (integer): deterministic ordering token  
- `safe_boundary` (bool): required for supervisory action application  
- `tp_lane_state` (object): lane‑local semantic state (read‑only)  
- `mp_state` (object): monitoring packets / TS health telemetry  
- `request_class` (enum): global‑impact classification  
- `ib_metadata` (object): IB identity, depth, ΔH%, stability metrics  
- `ob_metadata` (object): OB complexity, conflict rate, ΔH% profile  
- `cop_metadata` (object): COP proposal metadata  
- `external_command` (object): bounded supervisory command  

## Outbound contract (JSON‑compatible)

- `supervisory_action` (enum):  
  `Stop|Slow|Dampen|Escalate|SafeMode|ReduceDepth|SuspendInquiry|Crop|Prune|Reshape|Kill|Approve|Deny|None`
- `action_rationale` (string): deterministic rationale  
- `request_class` (enum): global‑impact category  
- `applied_bounds` (object): TCU envelope, depth limits, branching limits  
- `execution_diagnostics` (object): TCU usage, fallback flags  
- `supervisory_log_entry` (object): append‑only log record  
- `gb_reference` (string): deterministic supervisory reference ID  

---

# 6. Deterministic Invariants

- identical effective input → identical supervisory outcome  
- GB never mutates TP/MTP meaning‑construction state  
- GB reads only lane‑local TP state and MPs  
- GB operates asynchronously; TS never blocks waiting  
- supervisory actions apply only at deterministic safe boundaries  
- ordering derives from `sequence`, not timestamps  
- unsupported states reject with fixed reason codes  
- supervisory logs are append‑only and time‑indexed  
- TCU envelope is bounded and deterministic  
- fallback behavior is deterministic and auditable  
- external commands are policy‑gated and deterministic  

---

# 7. TCU and Tick‑Budget Expectations

- GB MUST operate within a small TS cycle share (nominally 3–5%)  
- GB MUST enforce bounded TCU envelopes (min/typ/max)  
- GB MUST degrade deterministically when exceeding budget  
- GB MUST report per‑cycle TCU usage  
- GB MUST NOT introduce unbounded or data‑dependent worst‑case growth  
- GB MUST support deterministic replay of supervisory decisions  

Future 30‑layer verification capsules will include:

- `scenario_id`  
- `seed`  
- `N`  
- `config_hash`  
- `cycles_measured`  

---

# 8. Verification Intent for Phase B

Planned positive checks:

- deterministic supervisory classification  
- deterministic drift/oscillation detection  
- deterministic IB creation approval  
- deterministic IB evolution supervision  
- deterministic IB merge/split supervision  
- deterministic IB promotion/retirement approval  
- deterministic OB decomposition supervision  
- deterministic COP proposal gating  
- deterministic safe‑boundary action application  
- deterministic fallback behavior under TCU overrun  

Planned negative‑path checks:

- unsupported supervisory action  
- unsafe‑boundary violation  
- out‑of‑order sequence  
- direct state‑mutation attempt  
- external command policy violation  
- TCU envelope violation  

---

# 9. Promotion Readiness Conditions

Before promotion from 40 to 30:

- executable deterministic harness  
- scenario ledger covering supervisory actions  
- deterministic drift/oscillation detection evidence  
- deterministic IB governance evidence  
- deterministic OB decomposition evidence  
- deterministic COP gating evidence  
- TCU envelope evidence  
- completed `verification_capsule.md` and `requirements_delta.md`  
- explicit HLR/LLR mapping to 20.80 and parent anchors  

