date: 2026-08-29
events processed: none (no human EVENT)
spine:
meaning:
Meaning first pass. write=no. Human owns the set. No Path A/B leak under the stated test (no meaning shall pushes realization or reads committed meaning backwards).
Distance (Meaning): beat jointly is TP-carried residue chain SOB → SROB → CnOB → SmOB, then routing-gated IdOB, OuBA freeze, COB long-horizon via OuBA only into a CIL snapshot. Splits on meaning-write law, CE invariant vs layer MAY-reads, SOB→SROB importance, SmOB→IdOB, and the TP.cob / next_context field ledger.

M-001 | 20.40_ob_requirements.md, 20.40.050_idob_prim.md, 20.105_tp_requirements.md | HLR-20.40-007, HLR-20.40-008, HLR-20.40.050-001, HLR-20.105-094, HLR-20.105-116 | Contradictory shalls: umbrella bans semantic interpretation and new meaning for 20.40.010–.060; IdOB SHALL perform identity-conditioned meaning interpretation; TP forbids non-TPU/OuBA meaning writes and then excepts IdOB. | COB/OB-set/IdOB/TP do not share one meaning-write law. | owner=human | write=no

M-002 | 20.40_ob_requirements.md, 20.40.010_sob_prim.md, 20.40.020_srob_prim.md, 20.40.030_cnob_prim.md, 20.40.040_smob_prim.md | HLR-20.40-003 vs HLR-20.40.010-030, HLR-20.40.020-027, HLR-20.40.030-011, HLR-20.40.040-014 | Contradictory shalls: umbrella forbids any OB layer to read/depend on CE, CIL, or semantic_core; SOB/SROB/CnOB/SmOB each MAY read CE/CEx discourse fields. | Shared OB invariant and the four-layer chain cannot both be true. | owner=human | write=no

M-003 | 20.40.010_sob_prim.md, 20.40.020_srob_prim.md, 20.105.010_tp_meta_fields.md, 20.105_tp_requirements.md | HLR-20.40.010-016, HLR-20.40.010-028, HLR-20.40.020-026, HLR-20.40.020-036, HLR-20.105-096 | Missing SOB→SROB handoff: SROB SHALL accept and refine structural-importance emitted by SOB; SOB residue/output shalls never name importance. TP still lists SOB as a producer of TP.semantic.importance. | First hop of the importance chain has no SOB producer. | owner=human | write=no

M-004 | 20.40_ob_requirements.md, 20.40.040_smob_prim.md, 20.40.050_idob_prim.md | HLR-20.40-001, HLR-20.40-016, HLR-20.40.040-028, HLR-20.40.040-038, HLR-20.40.050-032 | Missing SmOB→IdOB handoff: chain certifies valid input for next through SmOB, then SmOB SHALL be valid for SSG and RB only; IdOB SHALL refine SmOB importance; umbrella may route to IdOB or OuBA instead of finishing SmOB. | IdOB’s SmOB-cue duty is not a certified hop, and the umbrella can skip the producer. | owner=human | write=no

M-005 | 20.32_cob_requirements.md, 20.40.050_idob_prim.md, 20.105_tp_requirements.md, 20.105.010_tp_meta_fields.md | HLR-20.32-004, HLR-20.32-016, HLR-20.32-111, HLR-20.32-112, HLR-20.32-129, HLR-20.32-138, HLR-20.105-106, HLR-20.105-107 | COB vs IdOB vs TP mismatch on importance: COB SHALL ingest SmOB/IdOB importance and compute long-horizon maps, SHALL NOT interact with OB, SHALL ingest meaning only via OuBA, SHALL NOT derive importance from OB-family residue; OuBA-authorized subset has no importance fields; TP tells COB to linear-copy TP.semantic.importance without modifying scores/roles. | Three incompatible COB duties, with no authorized OuBA field for the cues. | owner=human | write=no

M-006 | 20.32_cob_requirements.md, 20.105_tp_requirements.md, 20.105.010_tp_meta_fields.md | HLR-20.32-062, HLR-20.32-079, HLR-20.32-117–136, HLR-20.105-094, HLR-20.105-116, HLR-20.105.010-001 | Field-ledger / write-authority mismatch: COB SHALL maintain TP.cob.* and ingest TP.next_context{}, and SHALL append TP.lineage_log[]; 20.105.010 has no TP.cob and places next-context under TP.metadata.next_context.*; TP write law excepts only TPU, OuBA, and listed IdOB paths. | COB’s named TP hops are not on the ledger and not in the write exception. | owner=human | write=no

M-007 | 20.32_cob_requirements.md | HLR-20.32-083, HLR-20.32-095, HLR-20.32-097, HLR-20.32-100, HLR-20.32-103 | Contradictory shalls on the COB next-context handoff: merge next-turn fields into identity layers and into clarifying structures; treat those fields as read-only and reflect them without modification; SHALL NOT write them into current-turn clarifying fields. | COB cannot jointly merge, not-modify, and not-write the same next-turn clarifying payload. | owner=human | write=no

M-008 | 20.32_cob_requirements.md, 20.105_tp_requirements.md | HLR-20.32-003, HLR-20.32-009, HLR-20.32-054, HLR-20.105-103, HLR-20.105-104 | Missing handoff + COB vs TP mismatch: 20.32 has COB snapshot → CIL → CEx selects the layer; 20.105 has CEx-CCR select conversation, then COB projects into that CIL. Opposite COB↔CEx polarity; 20.105 official flow also omits COB. | Who selects the conversation is not jointly specified. | owner=human | write=no

M-009 | 20.40_ob_requirements.md, 20.40.050_idob_prim.md, 20.105_tp_requirements.md | HLR-20.40-001, HLR-20.40-016, HLR-20.40-017, HLR-20.40.050-011, HLR-20.40.050-062 | Hop mismatch: umbrella is SOB→SROB→CnOB→SmOB unless routing selects IdOB or OuBA; IdOB/TP live stretch is RTU → TR → CTP → RB → IdOB → MCB → RBU, with OuBA on an OR exit that skips IdOB. | IdOB is optional peer vs post-RB hop vs skipped on the OuBA exit. | owner=human | write=no

M-010 | 20.40_ob_requirements.md, 20.40.050_idob_prim.md, 20.105_tp_requirements.md | HLR-20.40-017; 20.105 commit sentence; HLR-20.40.050-062 | Term mismatch: 20.40 OuBA freezes meaning into a Committed Thought Packet (CTP); 20.105 commit is TPU → OuBA → semantic_core; 20.40.050/20.105 CTP is a pre-RB hop (CTP-prm). | Same token, two meanings. | owner=human | write=no

M-011 | 20.40.050_idob_prim.md | HLR-20.40.050-011 vs HLR-20.40.050-062 | Contradictory shalls (hop): HLR-011 still shalls invocation only after RB-prm → RTU-prm; HLR-062 shalls RTU → TR → CTP → RB → IdOB and withdraws RB → RTU. | IdOB’s own invoke hop is not one hop. | owner=human | write=no

M-012 | 20.32_cob_requirements.md | HLR-20.32-009 vs HLR-20.32-120 | Contradictory shalls: outputs exclusively to CIL vs snapshot consumed by CIL and CEx. | CIL vs CEx consumer is not one shall. | owner=human | write=no

Support-file drift:
M-013 | 20.40.060_ouba_prim.md, 20.40_ob_requirements.md | HLR-20.40.060-001, HLR-20.40-001 | Support file cites a hop this set does not allow: OuBA SHALL accept only meaning states that passed through IdOB; umbrella may route to OuBA without IdOB. | owner=human | write=no

M-014 | 20.40.060_ouba_prim.md, 20.105_tp_requirements.md | HLR-20.40.060-021, HLR-20.40.060-022, HLR-20.105-001 | Support file cites a hop this set does not allow: OuBA SHALL commit truth_evidence[] and tb_trace[] required by COB; TP forbids TB / Path-B semantics on TP. | owner=human | write=no

M-015 | 20.705_patha_pathb_flow.md, 20.40_ob_requirements.md, 20.40.050_idob_prim.md | HLR-20.40-016, HLR-20.40.050-012 | Support file cites a hop this set does not allow: GB → IdOB (Path A). This set invokes IdOB only when RB selects it. | owner=human | write=no

M-016 | 20.705_patha_pathb_flow.md, 20.40.050_idob_prim.md | HLR-20.40.050-062 | Support file cites a hop this set does not allow: IdOB → TR → OuBA. This set’s successor is IdOB → MCB → RBU. | owner=human | write=no

M-017 | 20.700_master_glossary.md, 20.40_ob_requirements.md | HLR-20.40-007 | Support file cites a hop this set does not allow: glossary “No semantic interpretation before SmOB” vs umbrella ban for all OB layers including SmOB. | owner=human | write=no

20.200 and folder README cited no hop this set forbids. No writers. No rewrites.
route:
readme-bot:
needs human:
M-001 M-002 M-003 M-004 M-005 M-006 M-007 M-008 M-009 M-010 M-011 M-012 M-013 M-014 M-015 M-016 M-017 (no stamp; owner=human; write=no)
next recommendation: not yet
