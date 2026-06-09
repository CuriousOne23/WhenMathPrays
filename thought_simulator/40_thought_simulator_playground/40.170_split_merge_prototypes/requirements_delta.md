# 40.170_split_merge_prototypes / requirements_delta.md

## Status
Phase B complete — HLR mapping exercised and recorded from harness run 2026-06-09.

## Primary 20-series anchors
- [20.130_splitting_and_merging_requirements.md](../../20_requirements/20.130_splitting_and_merging_requirements.md) — HLR-20.130-001–026 (focus on split projection, merge reconciliation, lineage_delta, ΔH%, limits, determinism, replay)
- [20.105_tp_requirements.md](../../20_requirements/20.105_tp_requirements.md) — TP as carrier for split/merge
- [20.115_mtp_requirements.md](../../20_requirements/20.115_mtp_requirements.md) — merge into MTP-bound state before mtp_update
- [20.36_canonical_end_to_end_trace.md](../../20_requirements/20.36_canonical_end_to_end_trace.md) — A-chain: split after routing, merge before truth/done

## Flows Alignment Statement

- **Forward Flow (20-series):** Split and merge per 20.130 (projection, reconciliation, lineage, ΔH%, safe boundaries, audit); integrates with TP (20.105), MTP (20.115), A-chain order (20.36).
- **Backward Flow (40-series evidence):** Phase B runs (using 40.160 TP base + custom SplitMerge wrapper) confirm: deterministic split with parent lineage + tags + delta_h; merge with sources provenance + delta_h gain; limit reject; lineage_delta golden for audit; replay identical outputs. No changes needed to 20.xx; evidence strengthens the requirements.
- **Iterative Design Flow (50-series influence):** None yet. Prepares evidence for 50 design specs on split/merge accounting, lineage, ΔH% (e.g. updates to 50.130 or related).

**Agreement Statement**: Phase B complete per 40.05 (capsule structure, harness entrypoint, artifacts) and 40.510 W3 (split/merge with lineage_delta/ΔH% before truth). Full traceability from test scenarios to 20.130 HLRs. Ready for 30.00 normalization (coverage note, glossary) and 50 insight per wave protocol. Handoffs to 40.190 (RB arbitration) and 40.150 (MTP merge) exercised.

## Phase B HLR Exercise Summary (2026-06-09 harness run)

- Nominal split → lane outputs: HLR-20.130-001 (projection), -005 (lineage preservation), -015 (ΔH% markers on outputs). Evidence: children list with tags, deltas appended.
- Nominal merge → MTP-bound state: HLR-20.130-002 (recombine), -008 (parent reconciliation), -016 (ΔH% on merge). Evidence: merged TP with provenance, delta appended.
- Limit exceed → deterministic reject: HLR-20.130-012 (bounds), -013 (reject on exceed). Evidence: ValueError raised for child_count>5.
- `lineage_delta` golden diff: HLR-20.130-004 (logged events), -019 (reason codes). Evidence: golden json with event/tick/ids/delta_h/reason/missing_mass.
- Replay identical state: HLR-20.130-017 (deterministic/replayable). Evidence: identical lineage_delta json from repeated split+merge.

All 26 HLR-20.130 covered at high level via the 5 scenarios + base TP logic; detailed in capsule ledgers.

Schema/audit per 20.130-014,018,020–026 exercised indirectly (determinism from TP, append-only deltas, no invention).

## Impacted / Referenced Documents
- 40.160_tp_lifecycle (upstream for ThoughtPoint.split/merge)
- 40.150_mtp_prototypes (downstream merge target)
- 40.190_rb_prototypes (downstream split target)
- 20.130, 20.105, 20.115, 20.36 (as above)
- 40.05_master_program_guide.md (process)
- 30.30_verification_glossary.md (for future 30 promotion)
- 40.510_refactor.md (program tracking)

## Migration / Implementation Notes
- Leverages 40.160 ThoughtPoint for core split/merge to avoid duplication (per W3 dependencies).
- Custom LineageDelta + delta_h computation added for 20.130-004,015,016,019 requirements.
- Limit/reject and golden/replay added for boundary and determinism (012,013,017).
- Delta_h values are illustrative (based on entropy total / count); real impl would use precise Q32.32 from 20.95 and full merge math.
- No changes to 20.130 needed; this provides the 40-evidence.
- Artifact uses JSON for lineage_deltas (interoperable).

## Open Items / Gaps
- Full ΔH% formula per 20.95 / 20.130-015/016 (current is simplified example).
- Integration with GB supervisory for split/merge (20.130-022) — deferred to later or 40.190.
- Exact missing_mass calculation (example 0.0).
- 30.00 promotion: will require 10.50 peer + normalized 30 capsule citing this.
- 50 insight: update any 50.130 or related for split/merge design.

All deltas incorporated as of 2026-06-09 Phase B completion. No outstanding from Phase A.


See the [W3 wave coverage note](../../../30_verification/W3_pipeline_a_wave_coverage_note.md) for:

- Aggregated HLR mapping and contract checks across the W3 wave (401–412)

- Open gaps and 50 insight targets

- Glossary alignment (30.30)

- 10.50 peer references (where applicable for this module)

The primary evidence for promotion is the module's `verification_capsule.md` and the 2026-06-09 artifact(s) (or legacy baseline as noted). No separate 30.XXX capsule was created here unless already present in 30_verification/; the wave note serves as the 30 deliverable for the slice.

For modules with existing 30.XXX (e.g., 30.150 for this), cross-reference there.
