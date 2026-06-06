# Requirements Delta

## Scaffold Status
- scaffold_status: planned (with full HLR exploratory visibility per alignment)
- no implementation delta recorded yet

## Anchors
- 20-anchor: thought_simulator/20_requirements/20.100_inb_requirements.md (full 26 HLRs reproduced in software_description.md for exploratory clarity in the playground)
- 10.10-anchors:
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md (InB role, input stage, MTP/TP state, module-local buffers)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.20_interprocess_communication_and_channels.md (immutable channels, snapshots, no shared mutable memory)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md (InB visibility and non-mutation boundaries)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.60_coprocessor_offload_and_portability_rules.md (deterministic offload for normalization)

## Exploratory Note
The complete set of HLR-20.100-001 through HLR-20.100-026 (plus supporting 10-series contracts) is made visible in the accompanying software_description.md for playground exploration and insight. 20.xx remains the authoritative source of truth. 30.xx remains the coverage audit layer. 40.100 is non-canonical.

## Open Work
- implement prototype API (ingest, canonicalization, bounded handling, provenance emission, handoff contract)
- implement harness scenarios exercising the core invariants and full HLR set
- attach HLR/LLR references and artifacts
- demonstrate non-semantic deterministic canonicalization, tick-cycle boundary compliance, and explicit handoff contract

## Proposed Focus Areas for Future Evidence
- Deterministic acceptance/rejection equivalence for identical input/signature/profile state
- Deterministic canonicalization across equivalent noisy surface forms
- Deterministic FIFO-preserving sequence metadata continuity at handoff
- Deterministic reject-with-audit behavior for malformed/oversized/unsupported states
- Deterministic provenance and append-only intake audit evidence
- Strict isolation (no MTP mutation, no downstream state reads)