date: 2026-08-30
events processed: EVENT policy 2026-08-30; EVENT decision 2026-08-30; EVENT doc-change hop-order 2026-08-30 (stamp=human)
flow-tracker = 20.705 §2 and §3.6
decision: CTP means only the 20.145 primitive (Path A hop in 20.705 §2). HLR-20.40-017 is NA. OuBA commit is not called CTP.
scoring: 20.705 §2 is the Path A string as written. Score R-002 / M-009 / M-011 against §2. Do not replace §2 with a shorter chain. write=no.
hop-order: 20.40 and 20.51 aligned to 20.705 §2. CTP (20.145) immediately before RB. IdOB after that RB. OuBA is the alternate RB exit. R-002 close toward §2. M-009 close toward 20.40-001/016. M-011 still open until 20.40.050-011 is NA’d. write=no on further files.
spine:

S1 | files=20.31, 20.15, 20.206 | shalls=HLR-20.206-001, HLR-20.206-002, HLR-20.206-003, VR-6 | issue=contradictory shalls / Path A/B leak / scaffold vs 20.31 vs 20.206 mismatch | why it matters=B must consume OuBA and also reject meaning-side content, while Path A law and scaffold put meaning into OuBA | owner=human | write=no

S2 | files=20.15, 20.31 | shalls=HLR-20.31-004, HLR-20.31-005, HLR-20.31-006 | issue=scaffold vs 20.31 mismatch | why it matters=20.31 forbids standalone Path A meaning fields that 20.15 still lists on the TP datapacket | owner=human | write=no

S3 | files=20.206 | shalls=HLR-20.206-005, IMR-B, IMR-C | issue=contradictory shalls | why it matters=IMR-B cannot both re-run B on unchanged OuBA and be routed through a new Path A cycle | owner=human | write=no

S4 | files=20.206, 20.700.050 | shalls=HLR-20.206-003, HLR-20.206-006 | issue=support file citing a hop the spine does not allow | why it matters=20.700.050 (cited by HLR-20.012-033/035) feeds Path B via KnB/SSR and CoHI; 20.206’s exclusive B-start list and A→OuBA→B→OuBB order do not include those hops | owner=human | write=no

E1 | files=20.705, 20.15, 20.12, 20.206 | shalls=20.15-§3 (no id), HLR-20.012-005, HLR-20.012-020, HLR-20.206-006 | issue=support file citing a hop the spine does not allow / contradictory shalls: §3.6 hop CIL→CEx re-enters Path A CEx after OuBA, while §2/20.15 place CEx only after IE and treat OuBA as Path A exit | why it matters=§3.6 hop CIL→CEx re-enters Path A CEx after OuBA, while §2/20.15 place CEx only after IE and treat OuBA as Path A exit | owner=human | write=no

E2 | files=20.705, 20.15 | shalls=20.15-§2.14 (no id), 20.15-§4.22 (no id) | issue=support file citing a hop the spine does not allow / scaffold vs named hop: §3.6 hops CSTCore→COB and CSTMS→COB write COB, while 20.15 COB ingest door is OuBA freeze only | why it matters=§3.6 hops CSTCore→COB and CSTMS→COB write COB, while 20.15 COB ingest door is OuBA freeze only | owner=human | write=no

meaning:

M-001 | 20.40_ob_requirements.md, 20.40.050_idob_prim.md, 20.105_tp_requirements.md | HLR-20.40-007, HLR-20.40-008, HLR-20.40.050-001, HLR-20.105-094, HLR-20.105-116 | Contradictory shalls: umbrella bans semantic interpretation and new meaning for 20.40.010–.060; IdOB SHALL perform identity-conditioned meaning interpretation; TP forbids non-TPU/OuBA meaning writes and then excepts IdOB. | COB/OB-set/IdOB/TP do not share one meaning-write law. | owner=human | write=no

M-002 | 20.40_ob_requirements.md, 20.40.010_sob_prim.md, 20.40.020_srob_prim.md, 20.40.030_cnob_prim.md, 20.40.040_smob_prim.md | HLR-20.40-003 vs HLR-20.40.010-030, HLR-20.40.020-027, HLR-20.40.030-011, HLR-20.40.040-014 | Contradictory shalls: umbrella forbids any OB layer to read/depend on CE, CIL, or semantic_core; SOB/SROB/CnOB/SmOB each MAY read CE/CEx discourse fields. | Shared OB invariant and the four-layer chain cannot both be true. | owner=human | write=no

M-003 | 20.40.010_sob_prim.md, 20.40.020_srob_prim.md, 20.105.010_tp_meta_fields.md, 20.105_tp_requirements.md | HLR-20.40.010-016, HLR-20.40.010-028, HLR-20.40.020-026, HLR-20.40.020-036, HLR-20.105-096 | Missing SOB→SROB handoff: SROB SHALL accept and refine structural-importance emitted by SOB; SOB residue/output shalls never name importance. TP still lists SOB as a producer of TP.semantic.importance. | First hop of the importance chain has no SOB producer. | owner=human | write=no

M-004 | 20.40_ob_requirements.md, 20.40.040_smob_prim.md, 20.40.050_idob_prim.md | HLR-20.40-001, HLR-20.40-016, HLR-20.40.040-028, HLR-20.40.040-038, HLR-20.40.050-032 | Missing SmOB→IdOB handoff: chain certifies valid input for next through SmOB, then SmOB SHALL be valid for SSG and RB only; IdOB SHALL refine SmOB importance; umbrella may route to IdOB or OuBA instead of finishing SmOB. | IdOB’s SmOB-cue duty is not a certified hop, and the umbrella can skip the producer. | owner=human | write=no

M-005 | 20.32_cob_requirements.md, 20.40.050_idob_prim.md, 20.105_tp_requirements.md, 20.105.010_tp_meta_fields.md | HLR-20.32-004, HLR-20.32-016, HLR-20.32-111, HLR-20.32-112, HLR-20.32-129, HLR-20.32-138, HLR-20.105-106, HLR-20.105-107 | COB vs IdOB vs TP mismatch on importance: COB SHALL ingest SmOB/IdOB importance and compute long-horizon maps, SHALL NOT interact with OB, SHALL ingest meaning only via OuBA, SHALL NOT derive importance from OB-family residue; OuBA-authorized subset has no importance fields; TP tells COB to linear-copy TP.semantic.importance without modifying scores/roles. | Three incompatible COB duties, with no authorized OuBA field for the cues. | owner=human | write=no

M-006 | 20.32_cob_requirements.md, 20.105_tp_requirements.md, 20.105.010_tp_meta_fields.md | HLR-20.32-062, HLR-20.32-079, HLR-20.32-117–136, HLR-20.105-094, HLR-20.105-116, HLR-20.105.010-001 | Field-ledger / write-authority mismatch: COB SHALL maintain TP.cob.* and ingest TP.next_context{}, and SHALL append TP.lineage_log[]; 20.105.010 has no TP.cob and places next-context under TP.metadata.next_context.*; TP write law excepts only TPU, OuBA, and listed IdOB paths. | COB’s named TP hops are not on the ledger and not in the write exception. | owner=human | write=no

M-007 | 20.32_cob_requirements.md | HLR-20.32-083, HLR-20.32-095, HLR-20.32-097, HLR-20.32-100, HLR-20.32-103 | Contradictory shalls on the COB next-context handoff: merge next-turn fields into identity layers and into clarifying structures; treat those fields as read-only and reflect them without modification; SHALL NOT write them into current-turn clarifying fields. | COB cannot jointly merge, not-modify, and not-write the same next-turn clarifying payload. | owner=human | write=no

M-008 | 20.32_cob_requirements.md, 20.105_tp_requirements.md | HLR-20.32-003, HLR-20.32-009, HLR-20.32-054, HLR-20.105-103, HLR-20.105-104 | Missing handoff + COB vs TP mismatch: 20.32 has COB snapshot → CIL → CEx selects the layer; 20.105 has CEx-CCR select conversation, then COB projects into that CIL. Opposite COB↔CEx polarity; 20.105 official flow also omits COB. | Who selects the conversation is not jointly specified. | owner=human | write=no

M-009 | 20.40_ob_requirements.md | HLR-20.40-001, HLR-20.40-016 | decided 2026-08-30 stamp=human: hop order aligned to 20.705 §2; on identity selection the invoke neighborhood is TR → CTP → RB → IdOB; OuBA is the alternate RB exit | closed toward 20.40-001/016 | owner=human | write=no

M-010 | 20.40_ob_requirements.md, 20.40.050_idob_prim.md, 20.105_tp_requirements.md | HLR-20.40-017; 20.105 commit sentence; HLR-20.40.050-062 | Term mismatch: 20.40 OuBA freezes meaning into a Committed Thought Packet (CTP); 20.105 commit is TPU → OuBA → semantic_core; 20.40.050/20.105 CTP is a pre-RB hop (CTP-prm). | Same token, two meanings. | owner=human | write=no

M-010 decided 2026-08-30 | CTP = 20.145 primitive only (20.705 §2). HLR-20.40-017 NA. Remaining work is 20.40 wording. write=no until human edits.

M-011 | 20.40.050_idob_prim.md | HLR-20.40.050-011 | still open until 20.40.050-011 is NA’d: IdOB invocable only after RB-prm → RTU-prm; §2 as written is WrdNm → ISc → RTU → TR → CTP → RB → IdOB | RB → RTU is not a hop in §2 as written | owner=human | write=no

M-012 | 20.32_cob_requirements.md | HLR-20.32-009 vs HLR-20.32-120 | Contradictory shalls: outputs exclusively to CIL vs snapshot consumed by CIL and CEx. | CIL vs CEx consumer is not one shall. | owner=human | write=no

Support-file drift:
M-013 | 20.40.060_ouba_prim.md, 20.40_ob_requirements.md | HLR-20.40.060-001, HLR-20.40-001 | Support file cites a hop this set does not allow: OuBA SHALL accept only meaning states that passed through IdOB; umbrella may route to OuBA without IdOB. | owner=human | write=no

M-014 | 20.40.060_ouba_prim.md, 20.105_tp_requirements.md | HLR-20.40.060-021, HLR-20.40.060-022, HLR-20.105-001 | Support file cites a hop this set does not allow: OuBA SHALL commit truth_evidence[] and tb_trace[] required by COB; TP forbids TB / Path-B semantics on TP. | owner=human | write=no

M-015 | 20.705_patha_pathb_flow.md, 20.40_ob_requirements.md, 20.40.050_idob_prim.md | HLR-20.40-016, HLR-20.40.050-012 | Support file cites a hop this set does not allow: GB → IdOB (Path A). This set invokes IdOB only when RB selects it. | owner=human | write=no

M-016 | 20.705_patha_pathb_flow.md, 20.40.050_idob_prim.md | HLR-20.40.050-062 | Support file cites a hop this set does not allow: IdOB → TR → OuBA. This set’s successor is IdOB → MCB → RBU. | owner=human | write=no

M-017 | 20.700_master_glossary.md, 20.40_ob_requirements.md | HLR-20.40-007 | Support file cites a hop this set does not allow: glossary “No semantic interpretation before SmOB” vs umbrella ban for all OB layers including SmOB. | owner=human | write=no

20.200 and folder README cited no hop this set forbids. No writers. No rewrites.

M-705-001 | 20.32_cob_requirements.md | HLR-20.32-054 | §3.6 hop CIL → CEx: referral counters update only when CEx selects the layer, requiring a CEx → COB write §3.6 does not have | CEx’s listed neighbor is CIL inbound; a same-cycle COB counter write skips OuBA → COB and runs selection backwards into the identity substrate | owner=human | write=no

M-705-002 | 20.32_cob_requirements.md | HLR-20.32-111 | §3.6 hop OuBA → COB: COB ingests semantic-adjacent importance cues emitted by SmOB, requiring SmOB → COB that §3.6 does not have | Authorized meaning ingest is OuBA → COB; SmOB’s §2 neighbor is WrdNm, not COB | owner=human | write=no

M-705-003 | 20.32_cob_requirements.md | HLR-20.32-112 | §3.6 hop OuBA → COB: COB ingests identity-importance cues emitted by IdOB, requiring IdOB → COB that §3.6 does not have | Authorized meaning ingest is OuBA → COB; IdOB’s §2 neighbor is MCB, not COB | owner=human | write=no

M-705-004 | 20.32_cob_requirements.md | HLR-20.32-120 | §3.6 hop COB → CIL: conversation_count snapshot is consumed by CIL and CEx, requiring COB → CEx that §3.6 does not have | COB’s listed consumer is CIL; CEx is after CIL → CEx, not a parallel COB consumer | owner=human | write=no

M-705-005 | 20.32_cob_requirements.md | HLR-20.32-124 | §3.6 hop COB → CIL: initial_state_complete snapshot is consumed by CIL and CEx, requiring COB → CEx that §3.6 does not have | COB’s listed consumer is CIL; CEx is after CIL → CEx, not a parallel COB consumer | owner=human | write=no

M-705-006 | 20.40.040_smob_prim.md | HLR-20.40.040-009 | §2 hop SmOB → WrdNm: SSG SHALL receive SmOB as its sole pre-semantic input, requiring SmOB → SSG and skipping WrdNm | Adjacent Path A consumer after SmOB is WrdNm, then ISc, then SSG | owner=human | write=no

M-705-007 | 20.40.040_smob_prim.md | HLR-20.40.040-038 | §2 hop SmOB → WrdNm: SmOB output SHALL be valid input for SSG and RB, requiring SmOB → SSG/RB and skipping WrdNm | Adjacent Path A consumer after SmOB is WrdNm, then ISc, then SSG | owner=human | write=no

M-705-008 | 20.40.050_idob_prim.md | HLR-20.40.050-011 | §2 hop RTU → TR → CTP → RB → IdOB: IdOB is invocable only after RB-prm → RTU-prm, reversing RTU-before-RB | §2 places RTU before TR/CTP/RB, then RB → IdOB; RB → RTU is not a §2 hop | owner=human | write=no

M-705-009 | 20.105_tp_requirements.md | HLR-20.105-100 (unlabeled; CCR-carry shall before 101) | §3.6 hop CIL → CEx: CCR envelope is for downstream consumption by CEx-Pck, COB, CIL, and CST, reversing CIL → CEx and requiring CEx → COB | CEx-CCR cannot feed COB/CIL/CST on the same cycle as CIL → CEx; §3.6 ingest into COB/CST is OuBA → COB / OuBA → CSTCore | owner=human | write=no

M-705-010 | 20.105_tp_requirements.md | HLR-20.105-104 | §3.6 hop CIL → CEx: COB uses CEx-CCR selected_conversation to project into CIL, reversing CIL → CEx and requiring CEx → COB | Same-cycle CCR → COB → CIL runs after CEx but §3.6 is COB → CIL → CEx | owner=human | write=no

M-705-011 | 20.105_tp_requirements.md | HLR-20.105-106 | §3.6 hop CIL → CEx: COB reads TP.cex.ccr.selected_conversation and projects into CIL, reversing CIL → CEx and requiring CEx → COB | Same-cycle CCR → COB → CIL runs after CEx but §3.6 is COB → CIL → CEx | owner=human | write=no

M-705-012 | 20.105_tp_requirements.md | HLR-20.105-110 | §3.6 hop CIL → CEx: identical CCR output yields identical COB CIL projections, reversing CIL → CEx and requiring CEx → COB | Same-cycle CCR → COB → CIL runs after CEx but §3.6 is COB → CIL → CEx | owner=human | write=no

route:

R-001 | 20.37, 20.50, 20.145; drift 20.40.050, 20.15, 20.705 | HLR-20.37-023, HLR-20.37-071, HLR-20.37-072, HLR-20.050-027, HLR-20.050-049, HLR-20.050-069; drift HLR-20.40.050-012, HLR-20.40.050-062 | missing hop | TR `routing_fields{}` has no hop-type keys and RB’s only named destination is TR (`selected_ob_ids[]` untyped); nothing in the routing shalls names a typed structure-to-meaning hop into IdOB after committed RB, so the first S2M crossing cannot be scheduled as a typed route. | owner=human | write=no

R-002 | 20.51_rbu_prim.md, 20.705_patha_pathb_flow.md | HLR-20.051-007 (header Downstream; §1; §2 pipeline) | closed (hop-order now matches §2) | 20.51 now has CTP(20.145) immediately before RB on the full §2 string; IdOB after that RB; OuBA alternate exit. | owner=human | write=no

R-002 remains hop-order (CTP before vs after RB), not “CTP is dead”. 20.145 stays live; do not retire the row.

R-003 | 20.51; drift 20.15, 20.705, 20.145 | HLR-20.051-007 (vs informative header/§1/§2 sequences); HLR-20.145-028 | invented diagram route | 20.51’s header Downstream invents `TR → CTP → WrdNm` (skips RB); that file also shows three mutually different Path-A strings, none of which match HLR-20.051-007, so a router cannot take a single allowed route into IdOB from this slice. | owner=human | write=no

R-004 | 20.56, 20.37, 20.50 | HLR-20.056-011, HLR-20.056-014, HLR-20.050-032, HLR-20.37-023 | table vs TR vs RB/RBU vs CTP mismatch | The only routing-table schema is Path-B (`opbeh`/`obg`/`xlater`, keyed by `routing_epoch_id`, no TP paths, no TR/RB aliases) while Path-A S2M would have to be typed in unspecified `TP.TR.routing_fields{}` that RB consumes but is forbidden to bind to that table, so there is no lookup row for an efficient typed hop into IdOB. | owner=human | write=no

R-005 | 20.51, 20.145, 20.705 | HLR-20.051-007 vs §2 TR→CTP→RB | conflicting hop (§2 TR→CTP→RB) | The RBU routing-readiness SHALL writes `TR → RB → CTP`, inverting 20.145 HLR-20.145-028/029 and the §2 freeze-then-arbitrate hop that must precede every RB including RB→IdOB. | owner=human | write=no

R-006 | 20.51, 20.705 | HLR-20.051-007 vs §2 TR→CTP→RB→IdOB | conflicting hop (§2 RB→IdOB) | Same SHALL ends `TR → RB → IdOB`, naming IdOB without the §2 CTP hop, so typed routing into IdOB is not the Path A hop TR→CTP→RB→IdOB. | owner=human | write=no

R-007 | 20.51, 20.705 | HLR-20.051-007 vs §2 RB→WrdNm | conflicting hop (§2 RB→WrdNm) | HLR-20.051-007 places `CTP → WrdNm` after `TR → RB → CTP`, so the first-loop §2 successor of RB is not WrdNm and the WrdNm vs IdOB destinations are not typed. | owner=human | write=no

R-008 | 20.51, 20.705 | 20.51 Downstream header vs §2 TR→CTP→RB | invented diagram route (§2 TR→CTP→RB) | Header Downstream invents `TR → CTP → WrdNm` (RB omitted after the first CTP), so the declared downstream skips the §2 hop that later becomes RB→IdOB. | owner=human | write=no

R-009 | 20.50, 20.705 | HLR-20.050-069, HLR-20.050-049 vs §2 RB→IdOB | missing hop (§2 RB→IdOB) | RB SHALLs IdOB only as a read-only view and routes to generic `selected_ob_ids[]`, and never SHALLs IdOB as the typed Path A destination after the second/fourth CTP→RB. | owner=human | write=no

R-010 | 20.37, 20.705 | HLR-20.37-071, HLR-20.37-023, §6 TR→RB vs §2 RB→IdOB | missing hop (§2 RB→IdOB) | TR may read `TP.idob` and must expose `routing_fields{}` to RB, but names no hop into IdOB, so the routing vector does not encode the §2 typed destination RB→IdOB. | owner=human | write=no

R-011 | 20.145, 20.705 | HLR-20.145-029 vs §2 RB→IdOB | missing hop (§2 RB→IdOB) | The only normative spine is `DCB → TR → CTP → RB`; the informative continuation is `RB → WrdNm → … → RB → …` and never names IdOB, so always-before-RB does not lock RB→IdOB. | owner=human | write=no

R-012 | 20.37, 20.50, 20.705 | HLR-20.37-039, HLR-20.37-046, HLR-20.050-027 vs §2 DCB→TR / RTU→TR | conflicting hop (§2 DCB→TR / RTU→TR) | TR-gating SHALLs RB→TR whenever `tr_needs_update`, a hop §2 does not list (RB successors are WrdNm / IdOB / OuBA), so TR re-entry is not sequenced as §2 RTU→TR→CTP→RB→IdOB. | owner=human | write=no

R-013 | 20.50, 20.145, 20.705 | 20.50 (no CTP shall) vs HLR-20.145-028 vs §2 CTP→RB | missing hop (§2 CTP→RB) | RB never names CTP as immediate predecessor, so arbitration is not bound to the freeze hop §2 places immediately before every RB, including the RB that must enter IdOB. | owner=human | write=no

R-014 | 20.37, 20.145, 20.705 | 20.37 §6 / HLR-20.37-004 (RB consumes TP.TR) vs HLR-20.145-029 vs §2 TR→CTP | missing hop (§2 TR→CTP) | TR names only RB as consumer and never CTP, collapsing the mandatory TR→CTP hop that §2 inserts before every RB on the path into IdOB. | owner=human | write=no

R-015 | 20.56, 20.37, 20.50, 20.705 | HLR-20.056-011, HLR-20.056-014, HLR-20.050-032 vs §2 TR→CTP→RB→IdOB | table vs TR vs RB/RBU vs CTP mismatch | 20.56 epoch tables are Pipeline-B-only, SHALL NOT alias TR/RB, SHALL NOT carry TP paths, and Path A RB SHALL NOT read `routing_epoch_id`, so no table row can express the Path A typed hop into IdOB. | owner=human | write=no

R-016 | 20.50, 20.705 | HLR-20.050-021 / `selected_ob_ids[]` vs §2 RB→WrdNm | missing hop (§2 RB→WrdNm) | RB’s filter does not SHALL WrdNm as the typed successor of the first/third RB, so WrdNm vs IdOB cannot be distinguished as §2 requires for efficient typed routing into IdOB. | owner=human | write=no

R-017 | 20.50, 20.705 | HLR-20.050-021 / `route_proposal` vs §2 RB→OuBA | missing hop (§2 RB→OuBA) | The OR-chain end hop RB→OuBA is not a typed RB destination, so Path A exit is not a SHALL’d alternative to RB→IdOB. | owner=human | write=no

readme-bot:
matrix:

MX-001 | 20.200, README, 20.15_xlate_requirements.md, 20.15_ts_architecture_scaffold.md, 20.43_xlater_requirements.md | HLR-20.200-002 | extra row for a file that moved or was renamed | Matrix still keys 20.15 to a non-live XlateR filename; live 20.15 law is the architecture scaffold and live XlateR law is 20.43. | owner=human | write=no

MX-002 | 20.200, README, 20.30.080_resp_gen_sem.md, 20.30.080_rg_resp_gen_sem.md | HLR-20.200-002 | extra row for a file that moved or was renamed | Matrix RG row cites a filename that is not on disk; live RG law is 20.30.080_rg_resp_gen_sem.md. | owner=human | write=no

MX-003 | 20.200, README, 20.31_semantic_specification.md, 20.31_patha_meaning_spec.md | HLR-20.200-002 | extra row for a file that moved or was renamed | Matrix 20.31 row cites a non-live name; live Path A meaning law is 20.31_patha_meaning_spec.md. | owner=human | write=no

MX-004 | 20.200, README, 20.44_ts_isc_scoring.md, 20.45_ts_isc_scoring.md, 20.44_wrdnm_primitive.md | HLR-20.200-002 | extra row for a file that moved or was renamed | Matrix 20.44 still names ISC scoring; live 20.44 is WRDNM and live ISC law is 20.45_ts_isc_scoring.md. | owner=human | write=no

MX-005 | 20.200, README, 20.101_iiinb_requirements.md, 20.101_iiinb_prim.md | HLR-20.200-002 | extra row for a file that moved or was renamed | Matrix IIInB row cites `_requirements.md`; live IIInB law is 20.101_iiinb_prim.md. | owner=human | write=no

MX-006 | 20.200, README, 20.110_oub_requirements.md, 20.110_oubb_requirements.md | HLR-20.200-002 | extra row for a file that moved or was renamed | Matrix 20.110 still names OuB; live 20.110 law is OuBB (`20.110_oubb_requirements.md`). | owner=human | write=no

MX-007 | 20.200, README, 20.145_ctp_prm.md, 20.145_ctp_prim.md | HLR-20.200-002 | extra row for a file that moved or was renamed | Matrix CTP row cites `_prm.md`; live CTP law is 20.145_ctp_prim.md. | owner=human | write=no

MX-008 | 20.200, 20.30.070_rbu_mtp_sem.md | HLR-20.200-002 | matrix row filename ≠ live file | Matrix still traces RBU+MTP semantics to 20.30.070_rbu_mtp_sem.md, which has no live 20-series file of that name. | owner=human | write=no

MX-009 | 20.200, 20.45_imr_requirements.md, 20.45_ts_isc_scoring.md | HLR-20.200-002 | matrix row filename ≠ live file | Matrix IMR row cites 20.45_imr_requirements.md; that name is not live (live 20.45 is ISC scoring). | owner=human | write=no

MX-010 | 20.200, 20.58_oub_execution_manifold_integration.md | HLR-20.200-002 | matrix row filename ≠ live file | Matrix still traces an OuB execution-manifold doc that has no live 20-series file of that name. | owner=human | write=no

MX-011 | 20.200, 20.102_usp_requirements.md | HLR-20.200-002 | matrix row filename ≠ live file | Matrix USP row cites 20.102_usp_requirements.md; that name is not among live 20-series files. | owner=human | write=no

MX-012 | 20.200, 20.103_upi_requirements.md | HLR-20.200-002 | matrix row filename ≠ live file | Matrix UPI row cites 20.103_upi_requirements.md; that name is not among live 20-series files. | owner=human | write=no

MX-013 | 20.200, README, 20.40.050_idob_prim.md | HLR-20.200-002 | missing row for an authoritative module | IdOB is on the README auth list and live as 20.40.050_idob_prim.md, but 20.200 has no row for it. | owner=human | write=no

MX-014 | 20.200, README, 20.40.060_ouba_prim.md, 20.40.060.010_ouba_input_data_spec.md, 20.40.060.700_ouba_field_ref.md | HLR-20.200-002 | missing row for an authoritative module | OuBA and its two live input/field companions are on the README auth list; 20.200 has no OuBA rows (it still has stale OuB 20.110/20.58 names). | owner=human | write=no

MX-015 | 20.200, README, 20.47_ssg_prim.md | HLR-20.200-002 | missing row for an authoritative module | SSG is on the README auth list and live as 20.47_ssg_prim.md, but 20.200 has no row for it. | owner=human | write=no

MX-016 | 20.200, README, 20.15_ts_architecture_scaffold.md, 20.30.005_rtu_prim.md, 20.30.080_rg_resp_gen_sem.md, 20.30.085_rsg_prim.md, 20.30.090_rsg_mapping_rules.md, 20.31_patha_meaning_spec.md, 20.32.010.010_cst-core.md, 20.32.010.020_cst-ms.md, 20.32.010.030_cst-mux.md, 20.40.055_mcb_prim.md, 20.44_wrdnm_primitive.md, 20.45_ts_isc_scoring.md, 20.48.010_knc_prim.md, 20.48.020_knm_prim.md, 20.48.030_knf_prim.md, 20.49_stpx_prim.md, 20.52_ssr_data_packet.md, 20.53_rrw_process.md, 20.54_ssrgn_prim.md, 20.101_iiinb_prim.md, 20.105.010_tp_meta_fields.md, 20.105.020_tp_meta_provenance.md, 20.105.030_tp_meta_usage.md, 20.107.010_cex-ie_primitive.md, 20.107.020_cex-ccr_primitive.md, 20.107.030_cex-pck_primitive.md, 20.108.010_ce_candidate_set.md, 20.110_oubb_requirements.md, 20.110.010_oubb_stack.md, 20.112_li_prim.md, 20.113_cohi_prim.md, 20.145_ctp_prim.md, 20.155_trsch_prim.md | HLR-20.200-002 | missing row for an authoritative module | 33 further README-auth live modules have no 20.200 row under their live names, so the matrix does not cover current 20-series law for those modules. | owner=human | write=no

MX-017 | 20.200, README, 20.16_gb_responsibility_matrix.md, 20.18_failure_modes_and_success_criteria.md, 20.38_ts_implementation_guidelines.md, 20.39_ts_core_data_structures.md, 20.55_srp_requirements.md, 20.56_routing_table_schema.md, 20.57_trig_rb_semantic_trigger_requirements.md, 20.190_glossary.md, 20.205_execution_packet_xp_requirements.md | HLR-20.200-002 | README authoritative list ≠ matrix set | Nine live files are matrix rows but are not on `## Authoritative Requirement Files` (they sit on `## Directory index (coverage-aligned)` or `## Reference Documents`); auth list is 96 names, matrix is 79. | owner=human | write=no

MX-018 | 20.200 | HLR-20.200-001 | design-anchor TBD left as if current | 74 of 79 Design Anchor cells publish `50.*.md (TBD)` as the current design-anchor value, so placeholders are treated as live governance targets. | owner=human | write=no

MX-019 | 20.200, 20.705, 20.109_ie_prim.md | HLR-20.200-001; HLR-20.200-002; `[IE →](20.109_ie_prim.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[IE →](20.109_ie_prim.md)`. | owner=human | write=no

MX-020 | 20.200, 20.705, 20.44_wrdnm_primitive.md | HLR-20.200-001; HLR-20.200-002; `[WrdNm →](20.44_wrdnm_primitive.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[WrdNm →](20.44_wrdnm_primitive.md)` (the 20.44 row is ISC, not WrdNm). | owner=human | write=no

MX-021 | 20.200, 20.705, 20.47_ssg_prim.md | HLR-20.200-001; HLR-20.200-002; `[SSG →](20.47_ssg_prim.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[SSG →](20.47_ssg_prim.md)`. | owner=human | write=no

MX-022 | 20.200, 20.705, 20.49_stpx_prim.md | HLR-20.200-001; HLR-20.200-002; `[STPX →](20.49_stpx_prim.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[STPX →](20.49_stpx_prim.md)`. | owner=human | write=no

MX-023 | 20.200, 20.705, 20.30.005_rtu_prim.md | HLR-20.200-001; HLR-20.200-002; `[RTU →](20.30.005_rtu_prim.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[RTU →](20.30.005_rtu_prim.md)`. | owner=human | write=no

MX-024 | 20.200, 20.705, 20.40.050_idob_prim.md | HLR-20.200-001; HLR-20.200-002; `[IdOB →](20.40.050_idob_prim.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[IdOB →](20.40.050_idob_prim.md)`. | owner=human | write=no

MX-025 | 20.200, 20.705, 20.40.055_mcb_prim.md | HLR-20.200-001; HLR-20.200-002; `[MCB →](20.40.055_mcb_prim.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[MCB →](20.40.055_mcb_prim.md)`. | owner=human | write=no

MX-026 | 20.200, 20.705, 20.40.060_ouba_prim.md | HLR-20.200-001; HLR-20.200-002; `[OuBA (End of Path A)](20.40.060_ouba_prim.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[OuBA (End of Path A)](20.40.060_ouba_prim.md)`. | owner=human | write=no

MX-027 | 20.200, 20.705, 20.32.010_cst_requirements.md | HLR-20.200-001; HLR-20.200-002; `[CST](20.32.010_cst_requirements.md)`; `OuBA --> CSTCore`; `COB --> CSTCore` | missing hop row vs 20.705 §3.6 | 20.200 has no row for the §3.6 CST hop (`OuBA --> CSTCore` / `[CST](20.32.010_cst_requirements.md)`). | owner=human | write=no

MX-028 | 20.200, 20.705, 20.40.060_ouba_prim.md | HLR-20.200-001; HLR-20.200-002; `OuBA --> COB`; `OuBA --> CSTCore` | missing hop row vs 20.705 §3.6 | 20.200 has no row for the §3.6 hops `OuBA --> COB` and `OuBA --> CSTCore`. | owner=human | write=no

MX-029 | 20.200, 20.705, 20.101_iiinb_requirements.md, 20.101_iiinb_prim.md | HLR-20.200-001; HLR-20.200-002; `[IIInB →](20.101_iiinb_prim.md)` | stale hop filename vs 20.705 §2 | The 20.200 row `20.101_iiinb_requirements.md` does not match the §2 hop `[IIInB →](20.101_iiinb_prim.md)` (live file is `20.101_iiinb_prim.md`). | owner=human | write=no

MX-030 | 20.200, 20.705, 20.44_ts_isc_scoring.md, 20.45_ts_isc_scoring.md | HLR-20.200-001; HLR-20.200-002; `[ISc →](20.45_ts_isc_scoring.md)` | stale hop filename vs 20.705 §2 | The 20.200 row `20.44_ts_isc_scoring.md` (scope ISC scoring) does not match the §2 hop `[ISc →](20.45_ts_isc_scoring.md)` (live file is `20.45_ts_isc_scoring.md`). | owner=human | write=no

MX-031 | 20.200, 20.705, 20.145_ctp_prm.md, 20.145_ctp_prim.md | HLR-20.200-001; HLR-20.200-002; `[CTP →](20.145_ctp_prim.md)` | stale hop filename vs 20.705 §2 | The 20.200 row `20.145_ctp_prm.md` does not match the §2 hop `[CTP →](20.145_ctp_prim.md)` (live file is `20.145_ctp_prim.md`). | owner=human | write=no

MX-032 | 20.200, 20.705, 20.107_cex_extract.md | HLR-20.200-001; `[CEx →](20.107_cex_extract.md)`; `CIL --> CEx` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.107_cex_extract.md` has design-anchor `50.107_cex_design.md (TBD)` while §2 hop `[CEx →](20.107_cex_extract.md)` / §3.6 `CIL --> CEx` is treated as current. | owner=human | write=no

MX-033 | 20.200, 20.705, 20.108_ce_envelope.md | HLR-20.200-001; `[CE →](20.108_ce_envelope.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.108_ce_envelope.md` has design-anchor `50.108_ce_design.md (TBD)` while §2 hop `[CE →](20.108_ce_envelope.md)` is treated as current. | owner=human | write=no

MX-034 | 20.200, 20.705, 20.46_tpu_req.md | HLR-20.200-001; `[TPU →](20.46_tpu_req.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.46_tpu_req.md` has design-anchor `50.046_tpu_design.md (TBD)` while §2 hop `[TPU →](20.46_tpu_req.md)` is treated as current. | owner=human | write=no

MX-035 | 20.200, 20.705, 20.40.010_sob_prim.md | HLR-20.200-001; `[SOB →](20.40.010_sob_prim.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.40.010_sob_prim.md` has design-anchor `50.040_sob_design.md (TBD)` while §2 hop `[SOB →](20.40.010_sob_prim.md)` is treated as current. | owner=human | write=no

MX-036 | 20.200, 20.705, 20.40.020_srob_prim.md | HLR-20.200-001; `[SROB →](20.40.020_srob_prim.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.40.020_srob_prim.md` has design-anchor `50.040_srob_design.md (TBD)` while §2 hop `[SROB →](20.40.020_srob_prim.md)` is treated as current. | owner=human | write=no

MX-037 | 20.200, 20.705, 20.40.030_cnob_prim.md | HLR-20.200-001; `[CnOB →](20.40.030_cnob_prim.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.40.030_cnob_prim.md` has design-anchor `50.040_cnob_design.md (TBD)` while §2 hop `[CnOB →](20.40.030_cnob_prim.md)` is treated as current. | owner=human | write=no

MX-038 | 20.200, 20.705, 20.40.040_smob_prim.md | HLR-20.200-001; `[SmOB →](20.40.040_smob_prim.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.40.040_smob_prim.md` has design-anchor `50.040_smob_design.md (TBD)` while §2 hop `[SmOB →](20.40.040_smob_prim.md)` is treated as current. | owner=human | write=no

MX-039 | 20.200, 20.705, 20.44_ts_isc_scoring.md, 20.45_ts_isc_scoring.md | HLR-20.200-001; `[ISc →](20.45_ts_isc_scoring.md)` | TBD design-anchor on a 20.705 hop | The 20.200 ISC row `20.44_ts_isc_scoring.md` has design-anchor `50.044_isc_design.md (TBD)` while §2 hop `[ISc →](20.45_ts_isc_scoring.md)` is treated as current. | owner=human | write=no

MX-040 | 20.200, 20.705, 20.51_rbu_prim.md | HLR-20.200-001; `[RBU →](20.51_rbu_prim.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.51_rbu_prim.md` has design-anchor `50.051_rbu_design.md (TBD)` while §2 hop `[RBU →](20.51_rbu_prim.md)` is treated as current. | owner=human | write=no

MX-041 | 20.200, 20.705, 20.106_dcb_requirements.md | HLR-20.200-001; `[DCB →](20.106_dcb_requirements.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.106_dcb_requirements.md` has design-anchor `50.106_dcb_design.md (TBD)` while §2 hop `[DCB →](20.106_dcb_requirements.md)` is treated as current. | owner=human | write=no

MX-042 | 20.200, 20.705, 20.37_thought_router_tr_specification.md | HLR-20.200-001; `[TR →](20.37_thought_router_tr_specification.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.37_thought_router_tr_specification.md` has design-anchor `50.037_tr_design.md (TBD)` while §2 hop `[TR →](20.37_thought_router_tr_specification.md)` is treated as current. | owner=human | write=no

MX-043 | 20.200, 20.705, 20.145_ctp_prm.md, 20.145_ctp_prim.md | HLR-20.200-001; `[CTP →](20.145_ctp_prim.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.145_ctp_prm.md` has design-anchor `50.145_ctp_design.md (TBD)` while §2 hop `[CTP →](20.145_ctp_prim.md)` is treated as current. | owner=human | write=no

MX-044 | 20.200, 20.705, 20.50_rb_requirements.md | HLR-20.200-001; `[RB →](20.50_rb_requirements.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.50_rb_requirements.md` has design-anchor `50.050_rb_design.md (TBD)` while §2 hop `[RB →](20.50_rb_requirements.md)` is treated as current. | owner=human | write=no

MX-045 | 20.200, 20.705, 20.32_cob_requirements.md | HLR-20.200-001; `OuBA --> COB`; `[COB → ](20.32_cob_requirements.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.32_cob_requirements.md` has design-anchor `50.032_cob_design.md (TBD)` while §3.6 hop `OuBA --> COB` / `[COB → ](20.32_cob_requirements.md)` is treated as current. | owner=human | write=no

MX-046 | 20.200, 20.705, 20.33_cil_requirements.md | HLR-20.200-001; `COB --> CIL`; `[CIL](20.33_cil_requirements.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.33_cil_requirements.md` has design-anchor `50.033_cil_design.md (TBD)` while §3.6 hop `COB --> CIL` / `[CIL](20.33_cil_requirements.md)` is treated as current. | owner=human | write=no

needs human:
S1 S2 S3 S4 E1 E2 M-001–M-017 M-705-001–M-705-012 R-001–R-017 MX-001–MX-046 (no stamp; owner=human; write=no)
next recommendation: not yet
